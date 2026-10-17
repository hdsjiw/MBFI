from typing import Sequence

from app.config.capacity_policy import (
    CAPACITY_POLICY,
    CAPACITY_POLICY_VERSION,
    RISK_CEILING_ORDER,
)
from app.schemas.capacity import (
    CapacityEvidence,
    CapacityRequest,
    CapacityResponse,
    FinancialStatusAnswer,
)


class InvalidCapacityAnswers(ValueError):
    pass


def evaluate_capacity(request: CapacityRequest) -> CapacityResponse:
    answers = _validate_answers(request.answers)
    answer_by_id = {answer.question_id: answer for answer in answers}
    constraint_flags: list[str] = []
    evidence: list[CapacityEvidence] = []
    ceilings: list[str] = []

    _add_evidence(evidence, answer_by_id["F01"], "AGE_CATEGORY_RECORDED")
    _add_evidence(evidence, answer_by_id["F02"], "FINANCIAL_ASSET_CATEGORY_RECORDED")
    _add_evidence(evidence, answer_by_id["F03"], "INCOME_CATEGORY_RECORDED")
    _add_evidence(evidence, answer_by_id["F04"], "EXPENSE_CATEGORY_RECORDED")
    _add_evidence(evidence, answer_by_id["F07"], "GOAL_SIZE_CATEGORY_RECORDED")

    f05_option = _option_letter(answer_by_id["F05"])
    if f05_option == "A":
        constraint_flags.append("LOW_SAVING_CAPACITY")
    elif f05_option == "B":
        constraint_flags.append("LIMITED_SAVING_CAPACITY")
    _add_evidence(evidence, answer_by_id["F05"], "SAVING_CAPACITY_ASSESSMENT")
    ceilings.append(CAPACITY_POLICY.f05_risk_ceiling.get(f05_option, "UNDETERMINED"))

    f06_option = _option_letter(answer_by_id["F06"])
    if f06_option in {"A", "B"}:
        constraint_flags.append("DEBT_BURDEN_CONSTRAINT")
    elif f06_option == "C":
        constraint_flags.append("DEBT_BURDEN_PRESENT")
    _add_evidence(evidence, answer_by_id["F06"], "DEBT_BURDEN_ASSESSMENT")
    ceilings.append(CAPACITY_POLICY.f06_risk_ceiling.get(f06_option, "UNDETERMINED"))

    f08_option = _option_letter(answer_by_id["F08"])
    goal_horizon = {
        "A": "WITHIN_1_YEAR",
        "B": "ONE_TO_THREE_YEARS",
        "C": "THREE_TO_SEVEN_YEARS",
        "D": "AFTER_7_YEARS",
    }[f08_option]
    if f08_option == "A":
        constraint_flags.append("SHORT_GOAL_HORIZON")
    elif f08_option == "B":
        constraint_flags.append("LIMITED_GOAL_HORIZON")
    _add_evidence(evidence, answer_by_id["F08"], "GOAL_HORIZON_ASSESSMENT")
    ceilings.append(CAPACITY_POLICY.f08_risk_ceiling.get(f08_option, "UNDETERMINED"))

    risk_ceiling = _most_restrictive_ceiling(ceilings)
    has_constraint = bool(constraint_flags)
    liquidity_assessment = (
        "CONSTRAINED" if has_constraint else "INSUFFICIENT_DATA"
    )
    capacity_status = (
        "CONSTRAINED_WITH_MISSING_DATA"
        if has_constraint
        else "INFORMATION_INSUFFICIENT"
    )
    return CapacityResponse(
        capacity_status=capacity_status,
        constraint_flags=constraint_flags,
        risk_ceiling=risk_ceiling,
        liquidity_assessment=liquidity_assessment,
        goal_horizon=goal_horizon,
        missing_data=list(CAPACITY_POLICY.missing_data),
        evidence=evidence,
        policy_version=CAPACITY_POLICY_VERSION,
    )


def _validate_answers(
    answers: Sequence[FinancialStatusAnswer],
) -> list[FinancialStatusAnswer]:
    expected_ids = {f"F{index:02d}" for index in range(1, 9)}
    received_ids = [answer.question_id for answer in answers]
    if len(received_ids) != len(set(received_ids)):
        raise InvalidCapacityAnswers("duplicate financial status responses are not allowed")
    if set(received_ids) != expected_ids:
        raise InvalidCapacityAnswers("all F01-F08 responses are required")

    for answer in answers:
        if not answer.option_id.startswith(f"{answer.question_id}-"):
            raise InvalidCapacityAnswers(
                f"invalid option {answer.option_id} for {answer.question_id}"
            )
    return list(answers)


def _option_letter(answer: FinancialStatusAnswer) -> str:
    return answer.option_id[-1]


def _add_evidence(
    evidence: list[CapacityEvidence],
    answer: FinancialStatusAnswer,
    signal: str,
) -> None:
    evidence.append(
        CapacityEvidence(
            question_id=answer.question_id,
            option_id=answer.option_id,
            signal=signal,
        )
    )


def _most_restrictive_ceiling(ceilings: Sequence[str]) -> str:
    known_ceilings = [
        ceiling for ceiling in ceilings if ceiling in RISK_CEILING_ORDER
    ]
    if not known_ceilings:
        return "UNDETERMINED"
    return min(known_ceilings, key=RISK_CEILING_ORDER.get)

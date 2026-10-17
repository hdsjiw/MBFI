from dataclasses import dataclass


REPORT_POLICY_VERSION = "report-v1-provisional"


@dataclass(frozen=True)
class TypeReportTemplate:
    type_id: str
    label: str
    summary: str
    strengths: str
    consideration: str


TYPE_REPORT_TEMPLATES: dict[str, TypeReportTemplate] = {
    "stable-guardian": TypeReportTemplate(
        "stable-guardian",
        "안정 수호형",
        "변동성보다 예측 가능성과 안정적인 금융 관리를 중시하는 경향입니다.",
        "손실 가능성을 신중하게 살피고 생활의 안정성을 우선할 수 있습니다.",
        "유동성·목표 기간·Capacity를 확인하지 않은 상품 선택은 피해야 합니다.",
    ),
    "steady-accumulator": TypeReportTemplate(
        "steady-accumulator",
        "차곡차곡 축적형",
        "현재 소비와 미래 자산 축적 사이에서 꾸준한 준비를 중시하는 경향입니다.",
        "규칙적인 저축과 장기 목표를 세우는 데 강점이 있을 수 있습니다.",
        "저축 여력과 단기 현금 필요성을 함께 확인해야 합니다.",
    ),
    "planning-designer": TypeReportTemplate(
        "planning-designer",
        "계획 설계형",
        "목표와 계획을 세우고 금융 행동을 체계적으로 관리하려는 경향입니다.",
        "지출과 목표를 구조화해 실행 순서를 정하는 데 강점이 있을 수 있습니다.",
        "계획의 정교함이 실제 현금흐름과 Capacity를 대신하지는 않습니다.",
    ),
    "balanced-growth": TypeReportTemplate(
        "balanced-growth",
        "균형 성장형",
        "안정성과 장기적인 성장을 함께 고려하려는 경향입니다.",
        "한 가지 선택에 치우치기보다 조건을 비교하려는 태도를 보일 수 있습니다.",
        "균형이라는 표현이 모든 투자 위험을 감당할 수 있다는 뜻은 아닙니다.",
    ),
    "long-term-growth": TypeReportTemplate(
        "long-term-growth",
        "장기 성장형",
        "장기 목표와 성장 가능성을 중요하게 보는 경향입니다.",
        "긴 시간의 계획을 세우고 변동성을 장기 관점에서 바라볼 수 있습니다.",
        "실제 위험 한도와 유동성 제약이 우선되어야 합니다.",
    ),
    "active-investor": TypeReportTemplate(
        "active-investor",
        "적극 투자형",
        "시장투자와 성장 기회를 적극적으로 검토하려는 경향입니다.",
        "시장 정보를 탐색하고 장기 자산 형성 수단을 비교할 수 있습니다.",
        "높은 선호 점수가 높은 위험 감내 여력을 의미하지는 않습니다.",
    ),
    "present-focused": TypeReportTemplate(
        "present-focused",
        "현재 만족형",
        "현재의 필요와 만족을 미래 계획보다 가깝게 두는 경향입니다.",
        "현재 생활의 우선순위를 분명하게 인식할 수 있습니다.",
        "작은 금액이라도 목표와 비상 상황을 위한 여유를 점검할 필요가 있습니다.",
    ),
    "intuitive-investor": TypeReportTemplate(
        "intuitive-investor",
        "감각 투자형",
        "시장 기회와 직관적인 판단에 관심을 보일 수 있는 경향입니다.",
        "새로운 투자 아이디어를 탐색하고 기회를 빠르게 인식할 수 있습니다.",
        "사전 계획과 Capacity 확인 없이 판단을 실행하지 않도록 주의해야 합니다.",
    ),
}

DIMENSION_LABELS = {
    "Risk": "위험 감수 성향",
    "Accumulation": "소비·축적 성향",
    "Planning": "금융관리 성향",
    "Investment": "시장투자 선호",
}

DIMENSION_INTERPRETATIONS = {
    "Risk": {
        "LOW": "가격 변동과 손실 가능성에 신중하게 반응하는 점수대입니다.",
        "MEDIUM": "조건에 따라 변동성을 받아들일 수 있는 중간 점수대입니다.",
        "HIGH": "가격 변동을 감수할 가능성이 상대적으로 높은 점수대입니다.",
    },
    "Accumulation": {
        "LOW": "현재 소비와 유연한 사용을 상대적으로 가깝게 두는 점수대입니다.",
        "MEDIUM": "현재 소비와 미래 축적을 함께 고려하는 점수대입니다.",
        "HIGH": "미래 자산 축적과 저축·투자를 상대적으로 우선하는 점수대입니다.",
    },
    "Planning": {
        "LOW": "금융 계획과 지출 점검 행동이 아직 뚜렷하지 않을 수 있는 점수대입니다.",
        "MEDIUM": "필요한 상황에서 금융 계획과 점검을 수행할 수 있는 점수대입니다.",
        "HIGH": "목표·예산·지출을 계획적으로 관리하려는 점수대입니다.",
    },
    "Investment": {
        "LOW": "시장투자보다 원금 보존과 전통적인 저축 수단을 선호할 수 있는 점수대입니다.",
        "MEDIUM": "조건에 따라 저축과 시장투자를 함께 검토할 수 있는 점수대입니다.",
        "HIGH": "장기 자산 형성에서 시장투자를 적극적으로 검토할 수 있는 점수대입니다.",
    },
}

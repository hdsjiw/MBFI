import pytest
from pydantic import ValidationError

from app.config.preference_prototypes import (
    PREFERENCE_PROTOTYPES,
    PROTOTYPE_CONFIG_VERSION,
)
from app.schemas.preference_classification import (
    PreferenceClassificationRequest,
    PreferenceDimensions,
)
from app.services.preference_classification import classify_preference


def request_for(coordinates: tuple[float, float, float, float]):
    return PreferenceClassificationRequest(
        dimensions=PreferenceDimensions(
            risk=coordinates[0],
            accumulation=coordinates[1],
            planning=coordinates[2],
            investment=coordinates[3],
        )
    )


@pytest.mark.parametrize("prototype", PREFERENCE_PROTOTYPES)
def test_each_provisional_representative_point_selects_itself(prototype) -> None:
    result = classify_preference(request_for(prototype.coordinates))

    assert result.primary.type_id == prototype.type_id
    assert result.primary.label == prototype.label
    assert result.primary.distance == 0
    assert result.prototype_config_version == PROTOTYPE_CONFIG_VERSION
    assert result.classification_status == "PROVISIONAL"


def test_midpoint_between_two_types_is_marked_as_boundary() -> None:
    first = PREFERENCE_PROTOTYPES[0]
    second = PREFERENCE_PROTOTYPES[1]
    midpoint = tuple(
        (left + right) / 2
        for left, right in zip(first.coordinates, second.coordinates)
    )

    result = classify_preference(request_for(midpoint))

    assert result.boundary is True
    assert result.primary.distance == result.secondary.distance
    assert {result.primary.type_id, result.secondary.type_id} == {
        first.type_id,
        second.type_id,
    }


def test_exact_prototype_is_not_boundary_when_second_place_is_far() -> None:
    result = classify_preference(request_for(PREFERENCE_PROTOTYPES[0].coordinates))

    assert result.boundary is False
    assert result.secondary.distance - result.primary.distance > 5


def test_equal_distance_is_resolved_by_type_id_order() -> None:
    first = PREFERENCE_PROTOTYPES[0]
    second = PREFERENCE_PROTOTYPES[1]
    midpoint = tuple(
        (left + right) / 2
        for left, right in zip(first.coordinates, second.coordinates)
    )

    result = classify_preference(request_for(midpoint))

    assert result.primary.type_id == min(first.type_id, second.type_id)


@pytest.mark.parametrize(
    "invalid_dimensions",
    [
        {"risk": -1, "accumulation": 50, "planning": 50, "investment": 50},
        {"risk": 50, "accumulation": 50, "planning": 50, "investment": 101},
    ],
)
def test_dimensions_must_be_between_zero_and_one_hundred(invalid_dimensions) -> None:
    with pytest.raises(ValidationError):
        PreferenceClassificationRequest(dimensions=invalid_dimensions)

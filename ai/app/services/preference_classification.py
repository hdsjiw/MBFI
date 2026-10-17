from dataclasses import dataclass
from math import sqrt

from app.config.preference_prototypes import (
    BOUNDARY_DISTANCE_GAP,
    PREFERENCE_PROTOTYPES,
    PROTOTYPE_CONFIG_VERSION,
    PreferencePrototype,
)
from app.schemas.preference_classification import (
    PreferenceClassification,
    PreferenceClassificationRequest,
    PreferenceClassificationResponse,
    RankedPreferenceType,
)


@dataclass(frozen=True)
class RankedPrototype:
    prototype: PreferencePrototype
    distance: float


def euclidean_distance(
    dimensions: tuple[float, float, float, float],
    prototype: tuple[float, float, float, float],
) -> float:
    return sqrt(sum((value - target) ** 2 for value, target in zip(dimensions, prototype)))


def classify_preference(
    request: PreferenceClassificationRequest,
) -> PreferenceClassificationResponse:
    dimensions = request.dimensions
    coordinates = (
        dimensions.risk,
        dimensions.accumulation,
        dimensions.planning,
        dimensions.investment,
    )
    ranked = sorted(
        (
            RankedPrototype(
                prototype=prototype,
                distance=euclidean_distance(coordinates, prototype.coordinates),
            )
            for prototype in PREFERENCE_PROTOTYPES
        ),
        key=lambda item: (item.distance, item.prototype.type_id),
    )
    primary, secondary = ranked[:2]
    distance_gap = secondary.distance - primary.distance
    classification = PreferenceClassification(
        prototype_config_version=PROTOTYPE_CONFIG_VERSION,
        classification_status="PROVISIONAL",
        boundary=distance_gap <= BOUNDARY_DISTANCE_GAP,
        boundary_distance_gap=distance_gap,
        primary=_ranked_type(primary),
        secondary=_ranked_type(secondary),
    )
    return PreferenceClassificationResponse(
        **classification.model_dump(),
        dimensions=dimensions,
    )


def _ranked_type(item: RankedPrototype) -> RankedPreferenceType:
    return RankedPreferenceType(
        type_id=item.prototype.type_id,
        label=item.prototype.label,
        distance=item.distance,
    )

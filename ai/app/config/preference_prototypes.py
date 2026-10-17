from dataclasses import dataclass

PROTOTYPE_CONFIG_VERSION = "prototype-v0-provisional"
BOUNDARY_DISTANCE_GAP = 5.0


@dataclass(frozen=True)
class PreferencePrototype:
    type_id: str
    label: str
    risk: float
    accumulation: float
    planning: float
    investment: float

    @property
    def coordinates(self) -> tuple[float, float, float, float]:
        return (self.risk, self.accumulation, self.planning, self.investment)


# These are provisional representative points for implementation validation.
# They are not validated financial research values or production type thresholds.
PREFERENCE_PROTOTYPES: tuple[PreferencePrototype, ...] = (
    PreferencePrototype("stable-guardian", "안정 수호형", 25, 35, 55, 20),
    PreferencePrototype("steady-accumulator", "차곡차곡 축적형", 35, 85, 55, 30),
    PreferencePrototype("planning-designer", "계획 설계형", 35, 55, 90, 45),
    PreferencePrototype("balanced-growth", "균형 성장형", 55, 65, 65, 65),
    PreferencePrototype("long-term-growth", "장기 성장형", 75, 75, 80, 85),
    PreferencePrototype("active-investor", "적극 투자형", 85, 55, 45, 90),
    PreferencePrototype("present-focused", "현재 만족형", 35, 20, 25, 20),
    PreferencePrototype("intuitive-investor", "감각 투자형", 55, 35, 25, 80),
)

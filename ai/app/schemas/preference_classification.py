from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PreferenceDimensions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk: float = Field(ge=0, le=100)
    accumulation: float = Field(ge=0, le=100)
    planning: float = Field(ge=0, le=100)
    investment: float = Field(ge=0, le=100)


class PreferenceClassificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dimensions: PreferenceDimensions


class RankedPreferenceType(BaseModel):
    type_id: str
    label: str
    distance: float = Field(ge=0)


class PreferenceClassification(BaseModel):
    prototype_config_version: str
    classification_status: Literal["PROVISIONAL"]
    boundary: bool
    boundary_distance_gap: float = Field(ge=0)
    primary: RankedPreferenceType
    secondary: RankedPreferenceType


class PreferenceClassificationResponse(PreferenceClassification):
    dimensions: PreferenceDimensions

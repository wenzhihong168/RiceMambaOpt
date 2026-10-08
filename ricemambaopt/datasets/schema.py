"""Validated, framework-independent process and quality records."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from types import MappingProxyType
from typing import Mapping


class StudyRole(str, Enum):
    DEVELOPMENT = "development"
    HOLDOUT = "holdout"
    PROSPECTIVE = "prospective"


def _finite_mapping(name: str, values: Mapping[str, float]) -> Mapping[str, float]:
    if not values or any(not key.strip() or not isfinite(value) for key, value in values.items()):
        raise ValueError(f"{name} must contain finite values with non-empty names")
    return MappingProxyType(dict(values))


@dataclass(frozen=True, slots=True)
class ProcessBounds:
    time_seconds: tuple[float, float]
    speed_rpm: tuple[float, float]

    def __post_init__(self) -> None:
        for name, bounds in (("time_seconds", self.time_seconds), ("speed_rpm", self.speed_rpm)):
            low, high = bounds
            if not all(isfinite(value) for value in bounds) or low < 0 or low >= high:
                raise ValueError(f"{name} bounds must satisfy 0 <= low < high")

    def contains(self, time_seconds: float, speed_rpm: float) -> bool:
        return (
            self.time_seconds[0] <= time_seconds <= self.time_seconds[1]
            and self.speed_rpm[0] <= speed_rpm <= self.speed_rpm[1]
        )


@dataclass(frozen=True, slots=True)
class MillingObservation:
    sample_id: str
    batch_id: str
    cultivar: str
    time_seconds: float
    speed_rpm: float
    quality_targets: Mapping[str, float]
    role: StudyRole

    def __post_init__(self) -> None:
        for name in ("sample_id", "batch_id", "cultivar"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if not isfinite(self.time_seconds) or self.time_seconds < 0:
            raise ValueError("time_seconds must be finite and non-negative")
        if not isfinite(self.speed_rpm) or self.speed_rpm < 0:
            raise ValueError("speed_rpm must be finite and non-negative")
        object.__setattr__(
            self, "quality_targets", _finite_mapping("quality_targets", self.quality_targets)
        )


@dataclass(frozen=True, slots=True)
class InverseDesignRequest:
    cultivar: str
    targets: Mapping[str, float]
    weights: Mapping[str, float] = field(default_factory=dict)
    bounds: ProcessBounds = field(
        default_factory=lambda: ProcessBounds((0.0, 1.0), (0.0, 1.0))
    )

    def __post_init__(self) -> None:
        if not self.cultivar.strip():
            raise ValueError("cultivar must not be empty")
        targets = _finite_mapping("targets", self.targets)
        weights = dict(self.weights) if self.weights else {name: 1.0 for name in targets}
        if set(weights) != set(targets):
            raise ValueError("weights must match target names")
        if any(not isfinite(value) or value <= 0 for value in weights.values()):
            raise ValueError("weights must be finite and positive")
        object.__setattr__(self, "targets", targets)
        object.__setattr__(self, "weights", MappingProxyType(weights))

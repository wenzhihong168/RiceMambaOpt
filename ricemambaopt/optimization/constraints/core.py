"""Named bound and linear constraints with auditable residuals."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from types import MappingProxyType
from typing import Mapping

from ...datasets.schema import ProcessBounds


@dataclass(frozen=True, slots=True)
class LinearConstraint:
    name: str
    time_coefficient: float
    speed_coefficient: float
    relation: str
    limit: float

    def __post_init__(self) -> None:
        if not self.name.strip() or self.relation not in {"<=", ">="}:
            raise ValueError("constraint requires a name and relation '<=' or '>='")
        if any(
            not isfinite(value)
            for value in (self.time_coefficient, self.speed_coefficient, self.limit)
        ):
            raise ValueError("constraint coefficients and limit must be finite")

    def violation(self, time_seconds: float, speed_rpm: float) -> float:
        value = self.time_coefficient * time_seconds + self.speed_coefficient * speed_rpm
        return max(0.0, value - self.limit) if self.relation == "<=" else max(0.0, self.limit - value)


@dataclass(frozen=True, slots=True)
class ConstraintResult:
    feasible: bool
    violations: Mapping[str, float]

    def __post_init__(self) -> None:
        if any(value < 0 or not isfinite(value) for value in self.violations.values()):
            raise ValueError("violations must be finite and non-negative")
        object.__setattr__(self, "violations", MappingProxyType(dict(self.violations)))

    @property
    def total_violation(self) -> float:
        return sum(self.violations.values())


@dataclass(frozen=True, slots=True)
class ConstraintSet:
    bounds: ProcessBounds
    linear: tuple[LinearConstraint, ...] = ()

    def evaluate(self, time_seconds: float, speed_rpm: float) -> ConstraintResult:
        if not isfinite(time_seconds) or not isfinite(speed_rpm):
            raise ValueError("process settings must be finite")
        violations = {
            "time_lower": max(0.0, self.bounds.time_seconds[0] - time_seconds),
            "time_upper": max(0.0, time_seconds - self.bounds.time_seconds[1]),
            "speed_lower": max(0.0, self.bounds.speed_rpm[0] - speed_rpm),
            "speed_upper": max(0.0, speed_rpm - self.bounds.speed_rpm[1]),
        }
        for constraint in self.linear:
            if constraint.name in violations:
                raise ValueError(f"duplicate constraint name: {constraint.name}")
            violations[constraint.name] = constraint.violation(time_seconds, speed_rpm)
        active = {name: value for name, value in violations.items() if value > 0}
        return ConstraintResult(not active, active)

    def project_to_bounds(self, time_seconds: float, speed_rpm: float) -> tuple[float, float]:
        return (
            min(max(time_seconds, self.bounds.time_seconds[0]), self.bounds.time_seconds[1]),
            min(max(speed_rpm, self.bounds.speed_rpm[0]), self.bounds.speed_rpm[1]),
        )

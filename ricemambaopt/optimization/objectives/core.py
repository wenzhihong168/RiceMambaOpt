"""Auditable target-matching objectives."""

from __future__ import annotations

from math import isfinite
from typing import Mapping


def weighted_normalized_squared_error(
    predicted: Mapping[str, float],
    target: Mapping[str, float],
    scales: Mapping[str, float],
    weights: Mapping[str, float] | None = None,
) -> float:
    keys = set(target)
    if not keys or set(predicted) != keys or set(scales) != keys:
        raise ValueError("predicted, target, and scales must share non-empty keys")
    resolved_weights = dict(weights) if weights is not None else {name: 1.0 for name in keys}
    if set(resolved_weights) != keys:
        raise ValueError("weights must match target keys")
    numerator, denominator = 0.0, 0.0
    for name in sorted(keys):
        values = (predicted[name], target[name], scales[name], resolved_weights[name])
        if any(not isfinite(value) for value in values) or scales[name] <= 0 or resolved_weights[name] <= 0:
            raise ValueError("values must be finite; scales and weights must be positive")
        residual = (predicted[name] - target[name]) / scales[name]
        numerator += resolved_weights[name] * residual * residual
        denominator += resolved_weights[name]
    return numerator / denominator

"""Multi-target regression metrics with explicit normalization."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Iterable, Mapping, Sequence


def _paired(y_true: Iterable[float], y_pred: Iterable[float]) -> tuple[tuple[float, ...], tuple[float, ...]]:
    left, right = tuple(y_true), tuple(y_pred)
    if not left or len(left) != len(right):
        raise ValueError("inputs must be non-empty and aligned")
    if any(not isfinite(value) for value in (*left, *right)):
        raise ValueError("inputs must contain finite values")
    return left, right


@dataclass(frozen=True, slots=True)
class RegressionMetrics:
    mae: float
    rmse: float
    r2: float
    bias: float


def regression_metrics(y_true: Iterable[float], y_pred: Iterable[float]) -> RegressionMetrics:
    left, right = _paired(y_true, y_pred)
    residuals = [predicted - actual for actual, predicted in zip(left, right)]
    mean_true = sum(left) / len(left)
    denominator = sum((value - mean_true) ** 2 for value in left)
    numerator = sum(value * value for value in residuals)
    r2 = 1 - numerator / denominator if denominator else (1.0 if numerator == 0 else 0.0)
    return RegressionMetrics(
        mae=sum(abs(value) for value in residuals) / len(residuals),
        rmse=sqrt(numerator / len(residuals)),
        r2=r2,
        bias=sum(residuals) / len(residuals),
    )


def per_target_metrics(
    y_true: Mapping[str, Sequence[float]], y_pred: Mapping[str, Sequence[float]]
) -> Mapping[str, RegressionMetrics]:
    if set(y_true) != set(y_pred) or not y_true:
        raise ValueError("true and predicted target sets must match and be non-empty")
    return {name: regression_metrics(y_true[name], y_pred[name]) for name in sorted(y_true)}


def joint_normalized_rmse(
    y_true: Mapping[str, Sequence[float]],
    y_pred: Mapping[str, Sequence[float]],
    scales: Mapping[str, float],
) -> float:
    if set(y_true) != set(y_pred) or set(y_true) != set(scales) or not y_true:
        raise ValueError("targets and scales must have identical non-empty keys")
    normalized = []
    for name in sorted(y_true):
        scale = scales[name]
        if not isfinite(scale) or scale <= 0:
            raise ValueError("normalization scales must be finite and positive")
        normalized.append(regression_metrics(y_true[name], y_pred[name]).rmse / scale)
    return sqrt(sum(value * value for value in normalized) / len(normalized))

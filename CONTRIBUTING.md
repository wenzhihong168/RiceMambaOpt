# Contributing

Contributions should improve leakage-safe prediction, feasible inverse design, or reproducible process optimization without redistributing experimental data.

## Suitable contributions

- Configuration schemas for cultivars, quality targets, equipment bounds, and optimization objectives.
- Evaluation utilities for forward prediction, inverse recovery, feasibility, and Pareto analysis.
- Tests for fold-specific augmentation, routing, constraints, and deterministic search.
- Corrections that keep repository claims aligned with the published article.

## Evaluation safeguards

- Freeze validation and holdout samples before fitting TabDDPM or any preprocessing transform.
- Report all nine quality targets rather than only a pooled score.
- Evaluate target error and process feasibility together.
- Keep prospective validation separate from retrospective model selection.

## Pull requests

Use a focused branch and document the affected pipeline stage, data partition, optimization bounds, and validation performed. Do not commit raw observations, generated training tables, or large checkpoints.

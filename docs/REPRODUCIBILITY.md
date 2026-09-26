# Reproducibility scope

RiceMambaOpt combines leakage-controlled tabular augmentation, cultivar-aware forward prediction, and constrained inverse process design.

## Data protocol

- Freeze the 100-sample holdout before preprocessing, augmentation, or tuning.
- Fit TabDDPM independently inside each training fold.
- Generate synthetic observations from training data only.
- Preserve cultivar identity in split manifests and evaluation tables.

## Optimization protocol

- Record target profiles before inverse optimization.
- Enforce equipment bounds and process-feasibility penalties during search.
- Save initialization points, convergence criteria, and final feasible solutions.
- Keep the 12-profile prospective validation outside model recalibration.

## Determinism controls

Record seeds, software versions, TabDDPM checkpoints, MoE routing settings, optimization bounds, and every reported split manifest.

## Release boundary

Experimental measurements, synthetic caches, checkpoints, and optimization traces are intentionally excluded from version control.

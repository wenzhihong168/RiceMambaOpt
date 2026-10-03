# Failure Analysis

RiceMambaOpt failures may arise in forward prediction, uncertainty estimation, or constrained search. An apparently accurate target match is still a failure when the process is infeasible.

## Error taxonomy

| Failure class | Diagnostic view | Minimum context |
|:---|:---|:---|
| Target-specific prediction error | Signed residual by attribute | Cultivar and process settings |
| Cultivar shift | Metric by cultivar | Training support |
| Synthetic-data distortion | Real versus generated distributions | Training fold and TabDDPM ID |
| Uncertainty failure | Coverage and width by target | Nominal interval |
| Infeasible recommendation | Constraint residuals | Equipment bounds |
| Optimization instability | Solution variation across starts | Seed and search budget |

## Required stratification

Report each of the nine attributes by cultivar and study role. Inverse-design analysis separates retrospective recovery, independent holdout, and prospective target attainment.

## Case review

For every infeasible or high-error recommendation, record the requested targets, predicted and measured attributes, proposed time and speed, uncertainty, active constraints, initialization, convergence state, and nearest observed process settings.

## Corrective-action rule

Changes to augmentation, model fitting, objective weights, or search strategy must use frozen partitions and bounds. Prospective observations may evaluate a correction only after its recommendation is fixed.

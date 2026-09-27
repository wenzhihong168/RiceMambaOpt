# Evaluation Metrics

RiceMambaOpt couples nine-target forward prediction with constrained inverse design. Predictive accuracy and process feasibility must be evaluated together.

| Stage | Primary metrics | Required breakdown |
|:---|:---|:---|
| Forward prediction | R², RMSE, MAE | Each quality attribute and cultivar |
| Probabilistic output | Gaussian NLL, interval coverage and width | Each quality attribute |
| Inverse recovery | Time MAE, speed MAE, recovery R² | Cultivar and target profile |
| Target attainment | Attribute error, joint normalized RMSE | Retrospective and prospective sets |
| Feasibility | Bound-violation rate, constraint penalty | Constraint type |
| Multi-objective search | Pareto dominance and hypervolume | Search budget and reference point |

## Leakage controls

Fit TabDDPM, normalization, feature selection, and model tuning on development data only. The independent holdout and prospective samples must not influence augmentation, early stopping, optimization weights, or target selection.

## Inverse-design reporting

Report requested targets, recovered time and speed, predicted attributes, measured attributes when available, and every active constraint. A low target error is not successful if the proposed process is infeasible.

## Minimum result record

Record cultivar, split manifest, augmentation seed, model checkpoint, target scaling, equipment bounds, objective weights, optimizer initialization, search budget, and prospective measurement status.

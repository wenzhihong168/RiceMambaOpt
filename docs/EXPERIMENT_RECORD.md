# Experiment Record

Use one immutable record for every RiceMambaOpt prediction or inverse-design experiment.

## Identity

| Field | Value |
|:---|:---|
| Experiment ID |  |
| Git revision |  |
| Observation-schema version |  |
| Split-manifest hash |  |
| TabDDPM checkpoint and seed |  |
| Model and search seeds |  |
| Hardware and software environment |  |

## Pipeline configuration

- Cultivars and nine-target definition:
- Fold-specific augmentation ratio and quality checks:
- MoE routing and Mamba configuration:
- Heteroscedastic objective and target scaling:
- Equipment bounds and feasibility constraints:
- Inverse objective weights, initializations, and search budget:

## Evaluation record

Report forward metrics per target and cultivar. For inverse design, record requested targets, recovered settings, predicted values, measured values when available, uncertainty, and constraint residuals. Keep holdout and prospective results separate.

## Release gate

- [ ] TabDDPM used development-fold observations only.
- [ ] Independent holdout and prospective profiles remained frozen.
- [ ] All nine target metrics are reported.
- [ ] Every returned process setting satisfies hard constraints.
- [ ] Raw observations and generated training tables are excluded.

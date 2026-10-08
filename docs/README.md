# Documentation

Technical notes for the public RiceMambaOpt research repository.

| Document | Purpose |
|:---|:---|
| [Data interface](DATA_INTERFACE.md) | Defines milling observations, quality targets, and inverse-design requests |
| [Experiment record](EXPERIMENT_RECORD.md) | Captures TabDDPM, MoE-Mamba, constraints, and search settings |
| [Evaluation metrics](METRICS.md) | Covers forward prediction, uncertainty, recovery, feasibility, and Pareto quality |
| [Artifact manifest](ARTIFACT_MANIFEST.md) | Links observations, synthetic data, models, optimization, and figures |
| [Failure analysis](FAILURE_ANALYSIS.md) | Reviews target errors, cultivar shift, infeasible solutions, and search instability |
| [Reproducibility scope](REPRODUCIBILITY.md) | States leakage controls and prospective-validation boundaries |
| [Release checklist](RELEASE_CHECKLIST.md) | Verifies augmentation, feasibility, prospective evidence, and public artifacts |

## Recommended order

Freeze study roles and equipment bounds first, generate synthetic data inside training folds only, record forward and inverse configurations, evaluate predictive accuracy with feasibility, then audit prospective and unstable solutions.

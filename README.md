<div align="center">

# RiceMambaOpt

**Constraint-aware forward prediction and inverse design for moderate rice milling**

[![Paper](https://img.shields.io/badge/Paper-Foods_2026-6A994E?style=flat-square)](https://doi.org/10.3390/foods15162812)
[![Open Access](https://img.shields.io/badge/Open_Access-CC_BY_4.0-2A9D8F?style=flat-square)](https://doi.org/10.3390/foods15162812)
[![Targets](https://img.shields.io/badge/Quality_targets-9-D97706?style=flat-square)](#model-design)
[![Repository](https://img.shields.io/badge/Repository-public-2563EB?style=flat-square)](#codebase-blueprint)

<sub>TabDDPM · MoE–Mamba · heteroscedastic prediction · constrained inverse optimization</sub>

</div>

RiceMambaOpt links cultivar-aware quality prediction with process-feasibility-constrained inverse design, balancing starch digestibility, sensory quality, and executable milling conditions.

The central objective is not only to predict how milling changes rice quality, but also to solve the reverse engineering problem: given a desired nutritional and sensory profile, identify a time-speed combination that the equipment can actually execute. The framework therefore combines data augmentation, multi-output regression, uncertainty estimation, multi-objective search, and explicit physical constraints within one process-design pipeline.

## At a glance

<table align="center">
  <tr align="center">
    <th>Process inputs</th><th>Forward model</th><th>Predicted targets</th><th>Inverse output</th>
  </tr>
  <tr align="center">
    <td>Cultivar · milling time · speed</td>
    <td>TabDDPM + MoE–Mamba</td>
    <td>9 physicochemical, digestibility,<br>and sensory attributes</td>
    <td>Feasible time–speed<br>recommendations</td>
  </tr>
</table>

<table align="center">
  <tr align="center">
    <th>Original samples</th><th>Development set</th><th>Independent holdout</th><th>Prospective validation</th>
  </tr>
  <tr align="center">
    <td><b>500</b></td><td><b>400</b></td><td><b>100</b></td><td><b>12 profiles · 36 samples</b></td>
  </tr>
</table>

## Model design

1. **Leakage-controlled augmentation** — fold-specific TabDDPM expands sparse tabular observations without accessing validation or holdout samples.
2. **Structured tokenization** — cultivar, milling time, speed, and process-dose features are embedded as process-aware tokens.
3. **Selective state-space learning** — two Mamba blocks capture nonlinear interactions with compact linear-complexity computation.
4. **Cultivar-aware routing** — three specialized experts use top-1 routing to model cultivar-dependent processing responses.
5. **Probabilistic prediction** — the output head estimates the mean and log variance of nine quality attributes.
6. **Constrained inverse design** — multi-start optimization searches the equipment-feasible domain while balancing target error and process constraints.
7. **Mechanistic interpretation** — SHAP and Pareto analysis expose cultivar-specific process–quality trade-offs.

## Architecture

RiceMambaOpt couples two directions in a single framework: a cultivar-aware MoE–Mamba predicts nine quality attributes from processing conditions, and a constrained optimizer searches backward from desired quality to executable milling parameters.

TabDDPM expands the sparse tabular design space within each training fold, while the MoE layer routes observations toward cultivar-sensitive experts. Mamba blocks model cumulative process effects, and the heteroscedastic output head represents target-dependent predictive variance. During inverse design, the trained forward model becomes a differentiable process surrogate constrained by allowable milling time, speed, and energy input.

<p align="center">
  <img src="assets/architecture.png" alt="RiceMambaOpt architecture"><br>
  <sub>Figure 4. Forward quality prediction and constrained inverse design.</sub>
</p>

## Published results

<table align="center">
  <tr align="center">
    <th>Mean R²</th><th>Holdout time recovery</th><th>Prospective target attainment</th><th>Joint nRMSE</th>
  </tr>
  <tr align="center">
    <td><b>0.975 ± 0.008</b></td><td><b>R² 0.986 · MAE 0.960 s</b></td><td><b>10/12 profiles</b></td><td><b>6.2 ± 1.1%</b></td>
  </tr>
</table>

<table align="center">
  <tr align="center"><th>Model</th><th>Mean R² ± SD</th></tr>
  <tr align="center"><td>Shared MLP</td><td>0.838 ± 0.026</td></tr>
  <tr align="center"><td>Transformer</td><td>0.911 ± 0.016</td></tr>
  <tr align="center"><td>Mamba without MoE</td><td>0.949 ± 0.012</td></tr>
  <tr align="center"><td>MoE-MLP without Mamba</td><td>0.956 ± 0.011</td></tr>
  <tr align="center"><td><b>RiceMambaOpt</b></td><td><b>0.975 ± 0.008</b></td></tr>
</table>

### Data structure and augmentation

The correlation map summarizes how milling time, speed, and cultivar relate to physicochemical, digestibility, and sensory outcomes. It provides the empirical basis for treating the task as a coupled multi-output problem.

The matrix shows that the nine outputs are neither independent nor uniformly controlled by the same process variable. Digestibility indicators form a related biochemical group, while sensory attributes respond to a different combination of cultivar, mechanical intensity, and exposure time. Modeling these dependencies jointly allows the system to exploit shared process information without assuming that every quality target follows the same trend.

<p align="center">
  <img src="assets/process-quality-correlation.png" alt="Process-quality correlation matrix"><br>
  <sub>Figure 2. Global correlation structure between process parameters and quality indicators.</sub>
</p>

TabDDPM is evaluated by comparing the joint structure of real and augmented observations. The visualization checks whether augmentation expands coverage without erasing cultivar-specific clusters.

This check is essential because synthetic tabular samples are useful only if they preserve the relationships that define the processing problem. Correlation structure and low-dimensional embeddings are examined together: the first tests pairwise consistency, while the second reveals whether augmented samples remain aligned with the cultivar-specific manifolds present in the original observations.

<p align="center">
  <img src="assets/augmentation-consistency.png" alt="Real and augmented data consistency"><br>
  <sub>Figure 3. Distributional consistency of real and augmented data.</sub>
</p>

### Forward prediction

Across nine targets, the proposed model improves the mean coefficient of determination over MLP, Transformer, and ablated Mamba/MoE variants. The comparison isolates the contribution of selective state-space modeling and cultivar-aware routing.

RiceMambaOpt achieved a mean R² of 0.975 ± 0.008, compared with 0.911 ± 0.016 for the Transformer baseline, 0.949 ± 0.012 for Mamba without MoE, and 0.956 ± 0.011 for MoE-MLP without Mamba. The consistent gain across physicochemical, digestibility, and sensory endpoints indicates that the improvement is not confined to a single easy-to-predict target.

<p align="center">
  <img src="assets/model-comparison.png" alt="Forward-model comparison"><br>
  <sub>Figure 5. Model-wise R² across nine quality indicators.</sub>
</p>

Predicted-versus-observed plots and residual distributions provide a target-level view of calibration and error spread. This complements the aggregate mean R² with the behavior of individual physicochemical and sensory outputs.

The close alignment around the identity line shows that the forward model preserves both low- and high-value regions for the principal targets, while the residual panels expose remaining heteroscedasticity and target-specific error. These diagnostics are particularly important for inverse design, because a biased forward surrogate would direct the optimizer toward process settings that appear optimal numerically but fail when reproduced experimentally.

<p align="center">
  <img src="assets/forward-prediction.png" alt="Forward prediction and error distributions"><br>
  <sub>Figure 6. Forward fitting and error distributions.</sub>
</p>

### Inverse design

The Pareto frontier makes the trade-off between rapidly digestible starch and palatability explicit. Rather than returning a single unconstrained optimum, the model identifies a physically meaningful balance region for the Qiuguang cultivar.

The frontier demonstrates that gains in palatability eventually require a disproportionate increase in RDS, so the two objectives cannot be optimized independently. The highlighted balance zone represents a decision region in which sensory improvement remains substantial without moving immediately into the steepest part of the digestibility penalty.

<p align="center">
  <img src="assets/pareto-frontier.png" alt="RiceMambaOpt Pareto frontier"><br>
  <sub>Figure 7. RDS–palatability Pareto frontier.</sub>
</p>

Holdout recovery compares inferred milling settings with their experimental counterparts. Agreement and error distributions show strong recovery of milling time and a wider, but equipment-compatible, tolerance for milling speed.

On the independent holdout set, milling-time recovery achieved an MAE of 0.960 s and an R² of 0.986. Milling-speed recovery was less precise, with an MAE of 19.522 r/min and an R² of 0.851, consistent with a broader region of process equivalence at higher speeds. The Bland–Altman views make the magnitude and direction of these recovery errors visible across the operating range.

<p align="center">
  <img src="assets/inverse-agreement.png" alt="Inverse-prediction agreement"><br>
  <sub>Figure 8. Agreement analysis for inverse recovery of time and speed.</sub>
</p>

### Physical feasibility

The constraint layer separates executable recommendations from mathematically attractive but physically invalid solutions. The feasible region explicitly enforces milling-time, speed, and minimum-energy limits during inverse search.

Without these constraints, optimization can produce negative processing times, speeds beyond the equipment range, or low-energy combinations that cannot remove bran effectively. The constrained model redirects the search toward feasible alternatives, even when this requires accepting a slightly larger target error. This makes the inverse solution an engineering recommendation rather than a purely numerical optimum.

<p align="center">
  <img src="assets/constraint-feasibility.png" alt="Physical-constraint feasibility map"><br>
  <sub>Figure 9. Optimization space before and after physical constraints.</sub>
</p>

### Cultivar-specific interpretation

Reverse SHAP analysis explains why the optimizer selects different time–speed combinations for indica, glutinous, and japonica rice. Sensory attributes primarily drive milling speed, whereas amylose and RDS more strongly regulate milling duration.

The cultivar-specific profiles show that the same target vector can lead to different processing decisions because genetic background changes the attainable quality landscape. Appearance and palatability dominate speed selection in different cultivars, while RDS consistently influences time through its relationship with mechanical exposure and thermal accumulation. The analysis therefore interprets the optimizer as a conditional decision system rather than a universal lookup table.

<p align="center">
  <img src="assets/reverse-shap.png" alt="Cultivar-specific reverse SHAP analysis"><br>
  <sub>Figure 10. Cultivar-specific decision drivers for milling speed and time.</sub>
</p>

Published tables: [forward benchmark](results/forward_model_benchmark.csv) · [inverse recovery](results/inverse_recovery.csv) · [cultivar optimization](results/cultivar_optimization.csv) · [constraint ablation](results/constraint_ablation.csv)

## Codebase blueprint

```text
RiceMambaOpt/
├── assets/                         # architecture and published result figures
├── results/                        # machine-readable published tables
├── configs/
│   ├── data/                       # cultivar and split definitions
│   ├── model/                      # TabDDPM and MoE–Mamba settings
│   └── optimization/               # targets, bounds, and penalties
├── data/
│   ├── raw/                        # local experimental observations
│   ├── processed/                  # standardized model-ready tables
│   └── splits/                     # leakage-controlled split manifests
├── ricemambaopt/
│   ├── datasets/                   # schemas and tabular transforms
│   ├── models/
│   │   ├── tabddpm/                # conditional diffusion augmentation
│   │   ├── mamba/                  # selective state-space backbone
│   │   ├── moe/                    # cultivar-aware expert routing
│   │   └── uncertainty/            # heteroscedastic output heads
│   ├── optimization/
│   │   ├── objectives/             # digestibility and sensory targets
│   │   ├── constraints/            # equipment-feasibility penalties
│   │   └── search/                 # multi-start inverse optimization
│   ├── interpretability/           # SHAP and Pareto analysis
│   ├── evaluation/                 # holdout and prospective metrics
│   └── utils/                      # seeds, logging, serialization
├── scripts/                        # future train/optimize/validate commands
├── tests/
│   ├── unit/
│   └── integration/
└── README.md
```

The repository now includes a dependency-light public utility layer for validated process records, multi-target metrics, named feasibility constraints, and normalized inverse-design objectives, with unit tests and CI. The trained TabDDPM/MoE-Mamba models, checkpoints, and experimental data are not included in this release.

<details>
<summary><b>Citation</b></summary>

```bibtex
@article{li2026ricemambaopt,
  title   = {Synergistic Optimization of In Vitro Digestibility and Sensory Quality of Moderately Milled Rice Based on the RiceMambaOpt Model},
  author  = {Li, Zijun and Wen, Zhihong and Ma, Mengting and Niu, Wenshu and Sui, Zhongquan and Corke, Harold},
  journal = {Foods},
  volume  = {15},
  number  = {16},
  pages   = {2812},
  year    = {2026},
  doi     = {10.3390/foods15162812}
}
```

</details>

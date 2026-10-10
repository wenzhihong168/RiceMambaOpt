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

Developed in collaboration with **Shanghai Jiao Tong University**, the project treats moderate rice milling as a bidirectional engineering problem. The forward direction estimates the quality profile produced by a cultivar and a set of process conditions. The inverse direction starts from a desired profile and searches for feasible operating parameters. Connecting the two directions allows predictive modeling to support process design rather than remaining a descriptive analysis.

## Research overview

Moderate milling must reconcile objectives that do not necessarily improve together. Increasing mechanical intensity can alter bran removal, appearance, texture, palatability, and starch digestibility, but the response depends on cultivar and on the interaction between milling time and rotational speed. A process setting that improves one quality attribute may degrade another, and two settings with similar total intensity may not be equivalent if their time-speed combinations differ.

The available experimental data are also sparse relative to the continuous operating space. Nine correlated targets must be predicted from a limited number of cultivar-specific observations. Directly optimizing a flexible neural network on this setting risks overfitting, while an unconstrained inverse optimizer can exploit model error by proposing settings outside the equipment range or below the energy required for meaningful processing.

RiceMambaOpt addresses these issues through four linked components: fold-specific tabular diffusion augmentation, a cultivar-aware mixture-of-experts state-space predictor, a heteroscedastic output layer, and a constrained multi-objective optimizer. The forward model supplies a differentiable surrogate of the milling process. The inverse stage searches that surrogate only within a declared feasible region and reports trade-offs instead of presenting one mathematically optimal point as universally best.

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

## Process formulation

### Inputs, outputs, and process dose

Each record contains cultivar identity, milling time, milling speed, and derived process-dose information. The prediction target is a nine-dimensional vector spanning physicochemical properties, in vitro digestibility indicators, and sensory attributes. Modeling the targets jointly allows the network to learn shared process responses while retaining target-specific means and variances.

Cultivar is treated as more than a demographic label. It changes the attainable quality landscape and the sensitivity of each outcome to mechanical processing. The same desired profile may therefore require different settings for indica, glutinous, and japonica rice. Expert routing conditions the forward model on this heterogeneity rather than assuming one universal time-speed response surface.

The process-dose representation describes how duration and rotational speed combine to produce cumulative mechanical exposure. It supports both prediction and feasibility checking. During inverse design, time, speed, and dose constraints are evaluated together so that a candidate is not accepted merely because each variable is individually within range.

### Leakage-controlled data augmentation

TabDDPM is fitted only within the training portion of each fold. Synthetic observations are generated after the split, and validation or holdout records are never used to learn the augmentation distribution. This order matters because a diffusion model fitted on the complete dataset can transfer information about the held-out distribution into training even when the downstream predictor never sees the original holdout rows.

Augmented samples are evaluated against the real training distribution using correlation structure and low-dimensional embeddings. These checks do not prove that every synthetic row is physically realizable, but they help identify whether augmentation has erased cultivar structure, distorted target relationships, or collapsed the diversity of the original observations. The independent holdout and prospective experiment remain real-data evaluations.

### Forward prediction as a probabilistic surrogate

The MoE–Mamba network predicts the conditional mean and log variance of each quality attribute. The mean describes the expected profile at a proposed process setting; the variance expresses target-dependent uncertainty and heteroscedastic error. This distinction is important because some quality outcomes may be measured or predicted more consistently than others across the operating space.

The surrogate is evaluated before it is used for inverse design. High average predictive performance is not sufficient if residuals are biased in the region favored by the optimizer. Predicted-versus-observed plots, residual distributions, target-level metrics, and prospective confirmation are therefore used to assess whether the model remains credible near candidate solutions.

## Architecture

RiceMambaOpt couples two directions in a single framework: a cultivar-aware MoE–Mamba predicts nine quality attributes from processing conditions, and a constrained optimizer searches backward from desired quality to executable milling parameters.

TabDDPM expands the sparse tabular design space within each training fold, while the MoE layer routes observations toward cultivar-sensitive experts. Mamba blocks model cumulative process effects, and the heteroscedastic output head represents target-dependent predictive variance. During inverse design, the trained forward model becomes a differentiable process surrogate constrained by allowable milling time, speed, and energy input.

<p align="center">
  <img src="assets/architecture.png" alt="RiceMambaOpt architecture"><br>
  <sub>Figure 4. Forward quality prediction and constrained inverse design.</sub>
</p>

### Structured tokenization and selective state-space learning

Cultivar, time, speed, and derived process descriptors are embedded as structured tokens. Two selective state-space blocks model nonlinear dependencies among the process variables and quality responses while maintaining a compact computation path. The state-space representation is particularly useful for cumulative process effects because it can retain and selectively update latent process information without requiring a large fully connected network.

The expert layer contains cultivar-sensitive submodels and uses sparse top-1 routing. Only one expert is active for a sample, which encourages specialization and limits redundant computation. The router is part of the predictive model and must be evaluated for load balance and stability; an expert that receives too few observations may become poorly estimated even if the aggregate metric remains favorable.

### Multi-output uncertainty head

The final head produces nine means and nine log variances. Training with a heteroscedastic objective allows the model to assign different residual scales to different targets and observations. The variance is not a complete measure of epistemic uncertainty, but it prevents the inverse objective from treating every predicted quality component as equally precise.

During optimization, target deviations can be normalized by their scales so that an attribute with a large numeric range does not dominate the objective. This normalization also makes the multi-target error easier to compare across candidate solutions. The repository's utility layer exposes named objectives and feasibility checks so that the optimization contract remains inspectable.

### Constrained inverse optimization

The inverse stage treats the trained forward model as a surrogate function from process conditions to quality. Multiple starting points are used because the objective is nonlinear and may contain several local optima. Candidate settings are scored by their normalized distance from the desired quality vector together with explicit penalties for violating process constraints.

Hard bounds restrict milling time and speed to the equipment domain. A minimum-dose or energy constraint excludes numerically attractive combinations that are unlikely to produce the intended degree of milling. Multi-objective analysis then retains non-dominated solutions, exposing the trade-off between digestibility and palatability instead of hiding it behind one arbitrary scalar weight.

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

## Evaluation design

### Development and independent holdout

The reported dataset contains 500 original experimental observations. Four hundred are used for model development and 100 form an independent holdout. All augmentation and preprocessing operations are fitted within the development data. The holdout is reserved for testing both forward prediction and inverse recovery under conditions not used to fit the surrogate.

Forward performance is reported for each of the nine targets and summarized by the mean coefficient of determination. The complete model reaches a mean R² of 0.975 ± 0.008, compared with 0.911 ± 0.016 for the Transformer baseline, 0.949 ± 0.012 for Mamba without the expert layer, and 0.956 ± 0.011 for the MoE-MLP without Mamba. These comparisons isolate the contribution of selective state-space modeling and cultivar-aware routing under the reported split.

### Inverse recovery

Inverse recovery begins from an observed quality profile and asks whether the optimizer can reconstruct the process conditions that generated it. This is stricter than forward prediction because small surrogate errors can be amplified when the model is optimized backward. Milling-time recovery achieves an MAE of 0.960 seconds and R² of 0.986 on the holdout, while speed recovery is less precise with an MAE of 19.522 r/min and R² of 0.851.

The difference between time and speed recovery suggests that multiple speeds may produce similar profiles in parts of the operating range. A lower speed R² therefore should not automatically be read as complete inverse failure; it may reflect a wider equivalence region. Agreement plots and feasibility checks help distinguish interchangeable settings from truly implausible recommendations.

### Prospective confirmation

The prospective evaluation tests 12 target profiles using 36 experimental samples. Ten of the 12 profiles satisfy the predefined target-attainment criteria, with a joint normalized RMSE of 6.2 ± 1.1%. This experiment is important because it evaluates process settings selected by the inverse system rather than only reusing historical observations.

The prospective sample remains limited and should be interpreted as an initial confirmation of the inverse-design workflow. It does not establish robustness across all cultivars, equipment, batches, storage conditions, or target combinations. Broader prospective studies should enrich the regions in which the optimizer predicts high value but the training data are sparse.

### Constraint ablation

The constraint analysis compares the feasible optimizer with versions in which physical restrictions are relaxed. Without constraints, the numerical objective can be improved by moving toward negative durations, unsupported speeds, or insufficient process dose. These solutions reveal a general risk in surrogate-based optimization: the optimizer actively searches for regions where the model is weak.

Explicit feasibility rules convert the output from an unconstrained mathematical optimum into an executable engineering recommendation. The cost is that the best feasible solution may have slightly larger target error. This trade-off is desirable because a physically impossible low-error point has no experimental value.

## Interpreting the findings

The forward results show that state-space learning and cultivar-aware expert routing contribute complementary information. Mamba represents cumulative and nonlinear process effects, whereas the expert layer adapts those effects to cultivar-specific response surfaces. Their joint improvement across physicochemical, digestibility, and sensory targets suggests that the gain is not confined to one outcome group.

The Pareto analysis reframes optimization as decision support. Rapidly digestible starch and palatability cannot be assumed to improve together, so a single optimum depends on how the objectives are weighted. Presenting the non-dominated frontier allows researchers to choose a balance region that matches the intended product rather than accepting a hidden preference encoded by the model developer.

Reverse SHAP analysis further shows how target attributes influence selected process parameters. These attributions describe the learned inverse decision surface and should not be treated as mechanistic proof. Their value is diagnostic: they reveal whether cultivar, digestibility, appearance, and sensory objectives affect time and speed in plausible directions and help identify recommendations that warrant experimental review.

## Research contribution

RiceMambaOpt contributes an integrated forward-and-inverse framework for food-process design. It combines sparse-data augmentation, multi-target probabilistic prediction, cultivar-aware routing, constrained search, and prospective evaluation within one traceable workflow.

The work also makes physical feasibility part of the model specification. Many inverse-learning studies report target matching without verifying whether the proposed control variables are executable. Here, process bounds and minimum-dose conditions are explicit, named, and evaluated through ablation.

A third contribution is the separation of prediction, optimization, and experimental confirmation. Strong forward R² supports the surrogate but does not prove inverse validity; holdout recovery tests reversibility; and prospective profiles test whether recommended settings produce the intended result in new experiments. These evidence layers answer different questions and are presented separately.

## Scope and limitations

The current experiments cover a finite set of cultivars, milling conditions, quality assays, and equipment settings. The learned response surface may not transfer to a new machine, grain batch, storage state, moisture level, or cultivar without recalibration. Synthetic augmentation cannot replace experimental coverage of regions that are absent from the original design.

The nine targets do not capture every nutritional, sensory, economic, or manufacturing consideration. Objective weights and feasibility thresholds must be chosen for the intended application. The optimizer should not be used beyond the declared process domain, and high-uncertainty or boundary solutions should be confirmed experimentally before operational use.

The public repository provides validated process records, multi-target metrics, named constraints, inverse-objective utilities, figures, result tables, and the planned codebase structure. It does not include the complete trained TabDDPM/MoE–Mamba implementation, checkpoints, or the underlying experimental dataset.

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

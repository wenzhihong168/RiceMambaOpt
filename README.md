<div align="center">

# RiceMambaOpt

**Constraint-aware forward prediction and inverse design for moderate rice milling**

[![Paper](https://img.shields.io/badge/Paper-Foods_2026-6A994E?style=flat-square)](https://doi.org/10.3390/foods15162812)
[![Open Access](https://img.shields.io/badge/Open_Access-CC_BY_4.0-2A9D8F?style=flat-square)](https://doi.org/10.3390/foods15162812)
[![Code](https://img.shields.io/badge/Code-structure_only-6B7280?style=flat-square)](#repository-layout)

</div>

RiceMambaOpt links cultivar-aware quality prediction with process-feasibility-constrained inverse optimization across digestibility and sensory objectives.

## Architecture

<p align="center">
  <img src="assets/architecture.png" width="820" alt="RiceMambaOpt architecture">
</p>

## Results

| Mean R² | Joint nRMSE | Prospective target attainment |
|:---:|:---:|:---:|
| **0.944 ± 0.021** | **6.2 ± 1.1%** | **10/12 profiles** |

<p align="center">
  <img src="assets/pareto-frontier.png" width="720" alt="RiceMambaOpt Pareto frontier">
</p>

## Repository layout

```text
RiceMambaOpt/
├── assets/                 # architecture and result figures
├── configs/                # split and optimization settings
├── data/                   # tabular process interfaces
├── models/
│   ├── augmentation/       # fold-specific TabDDPM
│   ├── predictor/          # cultivar-aware MoE-Mamba
│   └── inverse_design/     # constrained process search
├── evaluation/             # real-sample and prospective evaluation
└── README.md
```

> Model implementation is not included in this release.

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

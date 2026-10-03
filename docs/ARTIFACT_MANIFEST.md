# Artifact Manifest

Every RiceMambaOpt result should preserve the chain from experimental observation to feasible process recommendation.

| Artifact | Visibility | Required identity |
|:---|:---:|:---|
| Observation inventory | Private | Batch, cultivar, protocol, content hash |
| Split manifest | Private | Development, holdout, prospective roles |
| TabDDPM checkpoint | Controlled | Fold, seed, training-only source hash |
| Synthetic cache | Private | Generator ID, sampling config, content hash |
| Forward checkpoint | Controlled | Model config, target schema, weight hash |
| Optimization trace | Private | Request, bounds, seed, search budget |
| Result table | Public-safe | Checkpoint, targets, feasibility, evaluation role |
| Figure | Public | Source-table hash and rendering revision |

## Required metadata

Each record stores `artifact_id`, parent IDs, Git revision, schema version, configuration hash, content hash, creation time, and access class.

## Lineage rule

Every inverse-design result references a frozen forward checkpoint and request specification. Prospective measurements link to, but never replace, the pre-registered recommendation that produced them.

## Integrity checks

- Synthetic artifacts descend only from the matching development fold.
- Holdout and prospective observations have no path into model fitting.
- Feasibility residuals accompany every recommended setting.
- Replaced artifacts receive new IDs rather than overwriting history.

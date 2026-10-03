# Data Interface

This specification connects local milling experiments to forward prediction and constrained inverse design without publishing source measurements.

## Observation record

| Field group | Required content |
|:---|:---|
| Identity | Stable `sample_id` and experimental batch identifier |
| Process inputs | Cultivar, milling time, speed, and versioned process-dose features |
| Quality targets | Nine named attributes with units and valid ranges |
| Study role | Development, independent holdout, or prospective validation |
| Replication | Profile identifier and replicate index where applicable |
| Provenance | Instrument, protocol, schema version, and measurement status |

## Inverse-design request

Each request records cultivar, desired quality vector, target mask, attribute weights, equipment bounds, feasibility constraints, optimizer budget, and seed. Returned solutions include proposed settings, predicted attributes, uncertainty, and every constraint residual.

## Validation checks

- Time and speed use declared units and remain within equipment bounds.
- Quality attributes preserve their individual scales before normalization.
- Replicates and derived samples inherit the parent split.
- Holdout and prospective records are inaccessible to TabDDPM fitting.
- Inverse solutions are rejected when any hard constraint is violated.

## Public boundary

Schemas, synthetic fixtures, and validators may be released. Raw observations, generated training tables, private manifests, and optimization traces remain local.

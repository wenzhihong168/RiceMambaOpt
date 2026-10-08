# Release Checklist

Complete this checklist before publishing a RiceMambaOpt result, model artifact, or implementation update.

## Evidence

- [ ] Observation schema, nine target definitions, units, and cultivar roles are versioned.
- [ ] Development, independent holdout, and prospective study roles are frozen.
- [ ] TabDDPM artifacts descend only from their matching training folds.
- [ ] Forward results are reported by target and cultivar.
- [ ] Inverse results include requested targets, uncertainty, settings, and constraint residuals.

## Optimization review

- [ ] Equipment bounds and hard constraints are declared before search.
- [ ] Multi-start settings, seeds, convergence status, and search budget are recorded.
- [ ] Infeasible or unstable recommendations have been reviewed.
- [ ] Prospective measurements did not influence their originating recommendation.

## Repository quality

- [ ] Model, augmentation, optimization, environment, and metric versions are recorded.
- [ ] Raw observations and generated training tables remain private.
- [ ] Documentation and citation metadata match the released scope.
- [ ] Checkpoints, traces, logs, and credentials follow the declared access boundary.
- [ ] The tagged revision reproduces every public-safe result artifact.

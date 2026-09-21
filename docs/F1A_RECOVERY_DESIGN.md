# F1a recovery design — prospective synthetic benchmark

Status: **PROSPECTIVE_SYNTHETIC_RECOVERY_DESIGN**

This document freezes the first recovery design for the F1a endogenous transmission experiment. It is committed before the authoritative benchmark implementation/result is accepted. The current F1a stage on `main` remains **SYNTHETIC_EXECUTABLE** until every declared promotion gate passes.

## Scientific question

The benchmark asks a deliberately narrow identifiability question:

> If a synthetic generator uses a known conditional probability `q_transmit` for a realised Share to traverse one explicit eligible directed edge and become a realised recipient ExposureEvent, can the benchmark recover that known probability from its own synthetic provenance?

This is not a question about the real probability that a person, post, platform, or social edge transmits information.

## Why condition on realised Share

The F1a runtime architecture already has a stochastic Share outcome produced by the existing cognitive decision path. Estimating an edge-transmission probability from all decisions would mix two distinct processes:

1. whether the sender shares;
2. whether a realised Share is transmitted to an eligible recipient.

The first recovery benchmark therefore conditions on **realised Share-edge opportunities**. Its estimator is

`q_hat = realised endogenous exposures / realised Share-edge opportunities`.

The authoritative fixture uses the already documented extreme synthetic sender bias so every scheduled sender Decision exercises the Share=true path. This is a software/design fixture, not a behavioral parameter estimate.

A future design that jointly estimates sharing propensity and transmission probability would be a separate identification problem and requires its own prospective contract.

## Synthetic generator

The recovery-only policy is not an active CBD runtime mechanism. It will live under the calibration namespace and implement the existing transmission-policy interface.

For each realised Share and eligible edge:

- draw one Bernoulli outcome with probability `q_transmit`;
- if successful, enqueue the existing recipient `ExposureEvent`;
- use a transmission RNG stream isolated from the cognitive Simulator RNG;
- use a deterministic seed derivation based on master seed plus grid-cell/replicate indices.

The dyad A→B is intentional. It removes degree, competition, ranking, and recipient-selection confounding from the first recovery question.

## Frozen parameter and design grid

Synthetic `q_transmit` values:

- 0.10
- 0.25
- 0.50
- 0.75
- 0.90

Core Share-edge opportunity counts:

- 50
- 100

Non-gating stress count:

- 25

Controlled abstract delays:

- 1.0
- 4.0

Replicates per grid cell: **200**.

The Decision spacing is 10 abstract time units, larger than the maximum delay, so each generated Exposure completes before the next scheduled Share opportunity. Delay therefore tests scheduler timing without creating event overlap as a second identification problem.

## Prospective recovery criterion

A replicate counts as recovered when

`abs(q_hat - q_true) <= 0.10`.

A core grid cell passes when at least **0.80** of its 200 replicates recover `q_true`.

This threshold is a CBD synthetic design convention, not a claim about acceptable empirical error.

Before running the benchmark, exact binomial coverage for the idealized estimator was checked analytically over the frozen q grid. The minimum probability of landing within ±0.10 is approximately:

| Opportunities | Minimum exact-binomial recovery probability over q grid | Role |
| ---: | ---: | --- |
| 25 | 0.754348 | stress only |
| 50 | 0.881080 | core |
| 100 | 0.964800 | core |

Thus N=25 is intentionally retained as a difficult non-gating condition. Making it a core 0.80 gate would prospectively demand performance that the benchmark's own idealized sampling model does not support for all q values.

## Deterministic controls

Two boundary controls are required outside the main recovery grid:

- `q_transmit = 0`: zero generated exposures;
- `q_transmit = 1`: every realised Share-edge opportunity generates exactly one Exposure, matching the exposure count of the existing forced pass-through F1a policy.

These are structural controls, not parameter-recovery cells.

## Familiarity consistency

The benchmark does not estimate `alpha_f`. After a replicate produces K realised recipient exposures, B's final Familiarity must equal the existing M0 update applied K times from the declared initial state.

This checks that the recovery-only transmission layer routes through the existing cognitive transition rather than mutating Familiarity directly.

## Delay consistency

Delay is not estimated in this phase. For every generated child exposure, the trace must satisfy

`child_time - parent_time = configured_delay`.

Across complete-horizon runs, changing delay from 1 to 4 must not change the expected transmission proportion; it changes only timing.

## Sensitivity scope

The first benchmark has one stochastic process parameter (`q_transmit`) and two controlled design factors (opportunity count and abstract delay). A frozen factorial grid plus an explicit stress regime is therefore used instead of introducing a new global-sensitivity software dependency.

Expected qualitative relations are frozen prospectively:

- mean exposure proportion increases with `q_transmit`;
- increasing opportunity count improves recovery precision but does not change the generating probability;
- delay shifts event times but not the full-horizon expected exposure proportion.

If later F1a versions introduce multiple uncertain network, ranking, delay-distribution, or behavioral parameters, a broader global sensitivity design should be reconsidered.

## Required outputs

The authoritative result must report every core and stress cell, including failures. At minimum it reports q-hat mean, bias, MAE, RMSE, recovery probability, mean exposure count, delay-realization error, familiarity-consistency error, the minimum core recovery probability, and an all-core-cells-pass flag.

Stress failures must not be hidden by aggregate averages.

## Interpretation boundary

A passing benchmark would establish only a **best-case synthetic recovery result** for the declared generator/estimator and would support promotion of F1a from `SYNTHETIC_EXECUTABLE` to `RECOVERY_TESTED`.

It would not show that:

- stochastic Bernoulli transmission is the true dissemination mechanism;
- the q grid contains realistic human or platform values;
- realised exposures are observable in a future empirical dataset;
- delay values correspond to seconds, minutes, hours, or days;
- a recipient decides or shares after exposure;
- the full endogenous feedback loop is closed;
- CBD is a formal System Dynamics model.

The next ladder stage after a successful recovery benchmark would still be **EMPIRICALLY_CONSTRAINED**, which requires a separate evidence and measurement bridge.

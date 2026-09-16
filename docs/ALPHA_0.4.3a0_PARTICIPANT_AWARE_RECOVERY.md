# Alpha 0.4.3a0 Phase H — participant-aware / hierarchical design recovery

Status: hierarchical validation tooling and screening contract only. No human data collection, active recognition mechanism, Pencode or UI.

## 1. Why Phase G is not yet a human-subject design

Phase G established that an aggregate binomial design with 640 target and 640 foil responses per Hsimp × bias operating-point cell can discriminate EVSD from symmetric 2HT in the frozen synthetic parameter grid.

Those 640 responses are not 640 independent participants and are not a prescription for one participant.

Recognition data collected from the same participant across conditions and response-bias blocks are clustered. Participants also differ in sensitivity and response criterion.

For nonlinear signal-detection models, ignoring participant or item variability can bias parameter estimates. Hierarchical models address this by estimating population-level parameters while representing participant-level variation and measurement noise.

## 2. Participant structure

Phase H keeps the Phase G aggregate anchor fixed:

- 640 target responses per Hsimp × bias cell;
- 640 foil responses per Hsimp × bias cell;
- 5 bias operating points;
- 2 Hsimp conditions.

It redistributes that aggregate information across four candidate allocations:

| Allocation | Participants | target + foil / participant / Hsimp × bias cell | Total responses / participant |
| --- | ---: | ---: | ---: |
| P40_X16 | 40 | 16 + 16 | 320 |
| P64_X10 | 64 | 10 + 10 | 200 |
| P80_X8 | 80 | 8 + 8 | 160 |
| P128_X5 | 128 | 5 + 5 | 100 |

Every allocation preserves exactly 640 target and 640 foil responses per population-level operating-point cell.

The simulator treats:

- Hsimp as within-participant;
- the five bias settings as repeated participant blocks;
- the held-out evaluation sample as a new independent participant cohort.

A future human protocol must counterbalance or randomize block order. Phase H does not yet simulate fatigue, learning or carryover.

## 3. Participant heterogeneity

Two participant-level random effects are introduced.

### EVSD

Population memory:

`d_j`

Participant memory:

`d_pj = d_j × exp(u_p)`.

Population criterion at bias point k:

`c_k`.

Participant criterion:

`c_pk = c_k + v_p`.

### symmetric 2HT

Population detection:

`Ddet_j`.

Participant detection:

`logit(Ddet_pj) = logit(Ddet_j) + u_p`.

Population uncertain-state guessing at bias point k:

`g_k`.

Participant guessing:

`logit(g_pk) = logit(g_k) + v_p`.

Random effects:

`u_p ~ Normal(0, sigma_memory)`

`v_p ~ Normal(0, sigma_bias)`.

For this first hierarchical gate their correlation is fixed to zero. Correlated participant random effects are deferred.

## 4. Heterogeneity stress grid

Phase H uses three synthetic heterogeneity regimes:

| Regime | sigma_memory | sigma_bias |
| --- | ---: | ---: |
| low | 0.10 | 0.10 |
| moderate | 0.25 | 0.25 |
| high | 0.40 | 0.40 |

These are stress-test values, not empirical estimates for the target population.

The weak / medium / strong memory grids and the five operating points remain exactly those used in Phase G.

## 5. Hierarchical likelihood

The raw response counts remain the fitting surface.

For each participant, Hsimp condition and bias block:

- hits are binomial target responses;
- false alarms are binomial foil responses.

The conditional response likelihood is integrated over `u_p` and `v_p` using Gauss-Hermite quadrature.

The default screening fitter uses five quadrature nodes on each random-effect dimension.

Each candidate has:

- 2 population memory parameters;
- 5 population bias parameters;
- `sigma_memory`;
- `sigma_bias`.

Total:

`9 population-level parameters`.

The random participant effects are integrated rather than counted as ordinary independent fixed parameters.

## 6. Model comparison

Training comparison:

`marginal AIC`.

Predictive comparison:

marginal predictive log likelihood in an independently simulated **new participant cohort**.

A replicate is assigned EVSD or 2HT only if both diagnostics favor the same family.

Otherwise:

`INCONCLUSIVE`.

This deliberately tests population-level generalization rather than memorization of participant-specific random effects.

## 7. Staged recovery

A full 72-cell hierarchical screen is computationally more expensive than the aggregate benchmark.

Phase H therefore separates screening from confirmation.

### Screening

- 4 participant allocations;
- 3 heterogeneity regimes;
- 3 memory regimes;
- 2 generator families;
- 72 cells;
- 50 replicates per cell.

The screening result is **not** sufficient to authorize a human protocol.

Its purpose is to identify:

- participant allocations that remain viable;
- worst heterogeneity regions;
- cells requiring confirmation.

### Confirmation

Before protocol design:

- selected/worst cells must be rerun at 200 replicates;
- the existing CEM recovery convention remains `>=0.80`;
- model-selection error and inconclusiveness remain separately reported.

## 8. Literature basis

Rouder and Lu's hierarchical signal-detection tutorial demonstrates why unmodeled participant/item variability can bias nonlinear recognition-memory estimates and advocates hierarchical treatment of participant variability, item variability and measurement error (PMID 16447374).

Recent hierarchical binary SDT work likewise emphasizes that aggregating across participants and other factors can bias inference, while partial pooling can improve population- and individual-level estimation (PMID 38806791).

Benjamin, Diaz and Wee show that criterion placement itself can vary and contribute substantially to recognition-memory variability (DOI 10.1037/a0014351).

Simulation work on hierarchical state-trace models illustrates the more general requirement to perform model recovery while explicitly representing subject- and trial-level dependencies.

## 9. Boundaries

Phase H currently models:

- participant memory heterogeneity;
- participant response-bias heterogeneity;
- repeated measurements across Hsimp and bias blocks;
- new-cohort prediction.

It does not yet model:

- item random effects;
- fatigue;
- learning/practice;
- block-order carryover;
- missingness;
- dropout;
- correlated memory/bias random effects.

These omissions must remain visible when the eventual human protocol is designed.

## 10. Human-data gate

Human data collection remains blocked.

Phase H tooling may merge only if:

- contract/schema validate;
- every participant allocation preserves the 640+640 aggregate anchor;
- hierarchical random effects are shared across repeated participant measurements;
- raw participant-level counts are fit directly;
- random effects are marginalized rather than ignored;
- held-out prediction uses a new participant cohort;
- screening and 200-replicate confirmation are separated;
- deterministic smoke recovery passes;
- no active EVSD/2HT state, Pencode or UI is introduced;
- active registries, evidence snapshot and public release remain unchanged;
- full CI passes.

After merge, the next explicit gate is the **authoritative 72-cell screening execution**. Only after screening may a smaller set of participant allocations/heterogeneity cells advance to 200-replicate confirmation.

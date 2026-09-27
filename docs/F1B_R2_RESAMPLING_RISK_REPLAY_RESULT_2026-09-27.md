# F1b R2 Resampling-Risk Replay Result

Status: **STAGE B COMPLETE / NON-AUTHORITATIVE / 224 STREAMS UNRESOLVED AT 199**

Issue: #213  
Scientific source: `4d3418938e11984f4f94ca2ae83d609fc9648d9a`

## Purpose

Replay the exact retained first-199 bootstrap attempts from the completed paired KL V2 characterization through the prospectively frozen resampling-risk controller.

No synthetic dataset was regenerated.

No bootstrap refit was rerun.

No bootstrap attempt was added.

## Controller

Frozen controller:
- alpha = 0.05;
- epsilon = 0.001;
- half-spend = 1000;
- replay horizon = 199 retained attempts.

Spending sequence:

`epsilon_n = epsilon * n / (1000 + n)`.

The controller is the internal Python implementation validated in PR #214 against the Gandy-style recurrence and the current `simctest` default parameterization.

## Exact replay source

Retained paired source:
- artifact ID: `10938668225`;
- exact JSON SHA-256:
  `b2727462b5bd09e5570090a42d7c90da8866e02100e0f4ccad551d8958a3d301`;
- 750 restriction runs;
- 199 retained bootstrap attempts per run;
- 0 retained bootstrap-refit failures.

The Stage-B runner verified this exact SHA-256 before parsing.

## Exact replay execution

Temporary replay PR: #216  
Actions run: `36343709630`

Replay artifact:
- artifact ID: `10938984164`;
- ZIP SHA-256:
  `0a7f6308aa0bd21866a4559d4dec38210b2225fa3f23f3e45da4abcbba76574b`;
- exact JSON SHA-256:
  `47d9321432208f56ad5ecc3077547601122196373d54c40a4c02bde91218635b`;
- exact JSON size: 1,803,618 bytes.

## Global result

Across all 750 retained streams:

- resolved by n=49: 326 / 750 = 43.47%;
- resolved by n=99: 372 / 750 = 49.60%;
- resolved by n=199: 526 / 750 = 70.13%;
- unresolved at n=199: 224 / 750 = 29.87%.

Among the 526 resolved streams:

- sequential reject: 119;
- sequential not-reject: 407;
- disagreement with retained fixed-199 decision: 0.

The zero disagreement applies only to streams that reached a sequential decision.

It does not convert unresolved streams into fixed-size decisions.

## Unresolved fixed-199 context

The 224 unresolved streams remain unresolved.

For descriptive context only, their retained fixed-199 states are:

- fixed-199 reject: 140;
- fixed-199 non-reject: 84.

Their retained plus-one p-values span approximately:

- minimum: 0.01;
- median: 0.04;
- maximum: 0.125.

These fixed-199 states are not used to classify the sequentially unresolved streams.

## Lower-boundary behavior through 199

All 119 sequential reject decisions:

- stop at n=173;
- have S_n = 0;
- hit the lower boundary.

At n=173 the frozen lower boundary first reaches 0.

At n=199:
- lower boundary = 0;
- upper boundary = 25.

Therefore a stream with one or more exceedances cannot reach the lower reject boundary by n=199 under this epsilon=0.001 controller.

This explains why many fixed-199 rejections remain sequentially unresolved.

## Role context

### CBD departure detection

360 runs:
- resolved by 49: 149;
- resolved by 99: 178;
- resolved by 199: 229;
- unresolved at 199: 131.

Resolved decisions:
- reject: 31;
- not-reject: 198.

### ADD departure diagnostic

240 runs:
- resolved by 49: 60;
- resolved by 99: 71;
- resolved by 199: 166;
- unresolved at 199: 74.

Resolved decisions:
- reject: 88;
- not-reject: 78.

### ADD specificity negative control

120 runs:
- resolved by 49: 92;
- resolved by 99: 97;
- resolved by 199: 103;
- unresolved at 199: 17.

All 103 resolved decisions are not-reject.

### CBD null

20 runs:
- resolved by 49: 15;
- resolved by 99: 16;
- resolved by 199: 18;
- unresolved at 199: 2.

All 18 resolved decisions are not-reject.

### ADD null

10 runs:
- resolved by 49: 10;
- resolved by 99: 10;
- resolved by 199: 10;
- unresolved at 199: 0.

All decisions are not-reject.

## KL target context

Null target 0:
- resolved by 199: 28 / 30;
- unresolved: 2.

KL 0.001:
- resolved by 199: 179 / 240;
- unresolved: 61.

KL 0.002:
- resolved by 199: 160 / 240;
- unresolved: 80.

KL 0.003:
- resolved by 199: 159 / 240;
- unresolved: 81.

The resampling-risk controller therefore does not simply resolve stronger departures more quickly; decision difficulty depends on the realized resampling p-value relative to alpha.

## Reproducibility checkpoint

Because Actions artifacts may expire, the repository result retains all 750 canonical stream checkpoints.

For each retained run the checkpoint contains:
- run ID;
- dataset SHA-256;
- bootstrap stream seed;
- observed statistic;
- canonical SHA-256 of the first-199 attempt sequence.

Canonical attempt hash:
- JSON array;
- `null` for failed attempts;
- compact separators;
- `allow_nan=false`;
- UTF-8 bytes;
- SHA-256.

The repository also retains the 224 unresolved run IDs.

This checkpoint is provenance.

It does not replace the exact replay artifact.

## Interpretation

The replay demonstrates that a 199-draw fixed-size result is not equivalent to a resampling-risk-controlled decision at epsilon=0.001.

Approximately 30% of retained streams are still unresolved at 199.

Therefore the previous descriptive similarity between 99 and 199 draws cannot by itself justify selecting either count as authoritative under the new decision-quality criterion.

The resampling-risk guarantee is conditional on the retained bootstrap mechanism.

It does not bound:
- model misspecification;
- parametric-bootstrap approximation error;
- scientific Type-I error;
- detection power;
- human-sample uncertainty.

## Next gate

Any extension beyond 199 must be prospectively frozen before generating a single new bootstrap attempt.

That separate gate must specify:
- an explicit maximum attempt cap;
- continuation from the same stream identity;
- unchanged epsilon/spending rule, unless a separate methodological justification changes it;
- `SEQUENTIAL_UNRESOLVED_AT_CAP` for streams that still do not stop.

The cap must not be selected by looking for the point at which all 224 current unresolved streams would happen to stop.

## Methodological basis

Gandy (2009) defines resampling risk as the probability that the Monte Carlo implementation and the theoretical resampling p-value give decisions on different sides of the threshold, and provides a sequential procedure with a uniform user-specified error bound.

The current `simctest` implementation uses the same default family:
- level 0.05;
- epsilon 0.001;
- half-spend 1000.

## Boundary

`STAGE A CONTROLLER = VALIDATED`

`STAGE B EXACT REPLAY = COMPLETE`

`RESOLVED BY 199 = 526 / 750`

`UNRESOLVED AT 199 = 224 / 750`

`UNRESOLVED = NOT RECODED`

`NEW BOOTSTRAP ATTEMPTS = NOT YET AUTHORIZED`

`DRAW COUNT = NOT SELECTED`

`POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`

# F1b R2 Bootstrap Calibration Pilot Result — 49×5

Status: **NON_AUTHORITATIVE_R2_BOOTSTRAP_CHARACTERIZATION_RESULT**

Issue: #150  
Parent: #145  
Scientific source commit: `41646ae89e000423c01f9d4d3221f9adefa7b19a`  
GitHub execution run: `36299032582`

## Frozen design

The result uses the prospectively merged pilot config:

- participants: 24
- items: 36
- missingness: 0
- fit-scale multiplier: 1×
- bootstrap draws: 49
- evaluation replicates: 5
- one controlled departure:
  `CBD_ADD_INTERSECTION_ANCHOR_1 / STANDALONE_ACCURACY_MAIN_EFFECT / + / RMS 0.25`

Total evaluation trials: **25**.

The run used config SHA-256:

`35c84547c8de98b969f1d206a29de43bf925a771af995ebdfbc3534feaa9245c`

and controlled-departure config SHA-256:

`e5603e0115d98abbb2df549671592fda14818abb5e990a0b5afad8641e5a2a1e`.

The temporary workflow branch was not intended for merge. Measured pilot wall time recorded by the execution wrapper was **52 seconds**.

## Execution integrity

Across all 25 trials:

- fit failures: **0**
- bootstrap calibration failures: **0**
- bootstrap fit failures: **0**
- successful bootstrap draws per successful test: **49/49**

Therefore the 49-draw path executed cleanly at the declared 24×36 design.

## Null calibration checks

### CBD_ANCHOR_1 → CBD complement restriction

- rejections: **1/5**
- observed rejection fraction: **0.200**
- Wilson 95%: **[0.036, 0.624]**

### CBD_ANCHOR_2 → CBD complement restriction

- rejections: **0/5**
- observed rejection fraction: **0.000**
- Wilson 95%: **[0.000, 0.434]**

### ADD_ANCHOR → ADD restriction

- rejections: **0/5**
- observed rejection fraction: **0.000**
- Wilson 95%: **[0.000, 0.434]**

With only five evaluation replicates per identity these values cannot establish 5% false-rejection control. The isolated rejection under CBD_ANCHOR_1 is a reason to expand calibration, not evidence that the test is miscalibrated.

## Controlled departure check

The generated departure achieved nearest-CBD RMS distance:

`0.24999999999999994`

with nearest-ADD RMS distance approximately zero, as required by the specificity design.

### CBD departure detection

- rejections: **5/5**
- observed detection fraction: **1.000**
- Wilson 95%: **[0.566, 1.000]**

The selected +0.25 standalone-accuracy departure therefore produced a strong pilot response against the CBD restriction.

### ADD specificity negative control

- ADD rejections: **1/5**
- observed rejection fraction: **0.200**
- Wilson 95%: **[0.036, 0.624]**

One of five ADD-specificity trials rejected even though the departure is algebraically ADD-compatible. This is not enough to quantify specificity, but it prevents treating the pilot as a clean false-rejection validation.

## Pilot verdict

The pilot answers its low-cost feasibility questions as follows:

- **execution stability:** PASS at the pilot level — no fit/calibration/bootstrap-fit failures;
- **gross universal null pathology:** not observed;
- **basic CBD response at the selected 0.25 departure:** observed in 5/5 trials;
- **ADD specificity:** broadly preserved in 4/5 trials, with one false rejection requiring further characterization;
- **false-rejection calibration:** unresolved because N=5 is intentionally too small.

Therefore:

`49_DRAWS_EXECUTION_FEASIBILITY = SUPPORTED_FOR_FURTHER_DESIGN_SEARCH`

but:

`49_DRAWS_CALIBRATION = NOT_FROZEN`

`5_EVALUATION_REPLICATES = NOT_FROZEN`

`FALSE_REJECTION_CONTROL = UNRESOLVED`

`DETECTION_POWER = UNRESOLVED`

`AUTHORITATIVE_CORE_GRID = NOT_FROZEN`

`HUMAN_N = NOT_FROZEN`

`PARTICIPANT_RECRUITMENT = NOT_AUTHORIZED`

`RUNTIME_F1B = NOT_AUTHORIZED`

## Next admissible step

Expand the non-authoritative R2 bootstrap characterization in a staged way, prioritizing null-calibration and specificity replication before treating departure detection as a power result.

The current pilot does not justify selecting 49 over 99/199 bootstrap draws.

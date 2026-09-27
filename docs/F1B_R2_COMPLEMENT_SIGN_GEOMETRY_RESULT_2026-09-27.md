# F1b R2 Complement-Relation Sign Geometry — Result

Status: **COMPLETED / NON-AUTHORITATIVE DETERMINISTIC DIAGNOSTIC**

Issue: #163  
Scientific source: `1d4282e745245d2d87ce904a1b742137c10d2e46`  
Execution run: `36311702420`  
Temporary PR: #165

## Integrity

Stage A executed exactly the frozen deterministic design:

- 12 complement-relation cases;
- 18 B×A×R cells per case;
- 216 cell rows;
- no stochastic dataset generation;
- no model fitting;
- no bootstrap calibration.

The exact Actions result is artifact `10928807813`.

- artifact ZIP SHA-256: `259a11f674b7bf6b86594907b721cfa09292bbfba43101d6b53ef0b48ff5ec05`;
- exact JSON SHA-256: `1f1322d7bbdd51093bbe0477fbbb7205595aeba9f2cf995526c9ffcb299ca1d9`.

The repository retains all 12 case summaries, including the general coefficients and nearest-CBD parameters needed to reconstruct every one of the 216 deterministic cell rows.

## Main result

Equal nearest-CBD RMS distance in utility/logit space does **not** imply equal probability-scale or information-scale separation for the two complement-relation signs.

### CBD_ANCHOR_1

| RMS | probability RMS +/− | mean KL +/− | information distance +/− | scalar step +/− |
|---:|---:|---:|---:|---:|
| 0.10 | 0.940 | 0.932 | 0.974 | 1.647 |
| 0.25 | 0.755 | 0.603 | 0.782 | 6.471 |
| 0.50 | 0.504 | 0.289 | 0.552 | 1.060 |

### CBD_ANCHOR_2

| RMS | probability RMS +/− | mean KL +/− | information distance +/− | scalar step +/− |
|---:|---:|---:|---:|---:|
| 0.10 | 0.930 | 0.920 | 0.968 | 1.704 |
| 0.25 | 0.715 | 0.547 | 0.746 | 6.224 |
| 0.50 | 0.477 | 0.258 | 0.525 | 1.109 |

At RMS 0.25 and 0.50, the plus direction is therefore materially less separated from its nearest CBD probability distribution even though the utility-space RMS distance is identical by construction.

This deterministic asymmetry is directionally consistent with the stochastic detection asymmetry retained from #158. It follows that the stochastic plus/minus difference cannot be attributed solely to bootstrap randomness or mixed-effects fitting.

## Probability saturation

At RMS 0.10, none of the complement cases has generator probabilities outside [0.05, 0.95].

At RMS 0.25:

- both minus cases: 0/18 cells outside [0.05, 0.95];
- both plus cases: 6/18 cells outside [0.05, 0.95].

For the plus cases, minimum Bernoulli variance falls to approximately:

- 0.00685 at CBD_ANCHOR_1;
- 0.00768 at CBD_ANCHOR_2.

At RMS 0.50, all signs have 6/18 saturated cells, but the plus direction still has only about one-half of the probability-RMS separation and roughly one-quarter to three-tenths of the mean KL of the minus direction.

Therefore logistic saturation explains part, but not all, of the sign asymmetry.

For Bernoulli outcomes, variance is (p(1-p)), so probability values close to zero or one carry substantially less local information for the same logit displacement. The Stage A information-weighted metric captures exactly this local effect.

## Nearest-CBD projection bounds

A second deterministic issue is now visible.

The nearest-CBD projection uses the same AP-A fixed-effect bounds as the current fitter:

- sharing bias: [-5, 5];
- baseline logit: [-4, 4];
- beta_accuracy: [-5, 5];
- beta_reward: [-5, 5].

The retained nearest-CBD solutions are boundary-active in many medium/large departure cases.

Examples:

- RMS 0.25 minus: beta_accuracy reaches +5;
- RMS 0.25 plus: beta_reward reaches +5;
- RMS 0.50 minus: beta_accuracy and beta_reward reach their lower bounds;
- RMS 0.50 plus: beta_accuracy reaches −5 and beta_reward +5.

CBD_ANCHOR_2 minus is already beta_accuracy-bound at RMS 0.10.

This matters because #145 intentionally defined nearest-CBD distance using the current AP-A fitter bounds. The resulting geometry is therefore a distance to the **bounded computational CBD surface**, not demonstrably to an unconstrained scientific manifold.

The current repository contains no separate scientific justification that these numerical fitter bounds define the substantive support of CBD parameters.

## Consequence

Stage A answers the original question:

`DETERMINISTIC SIGN GEOMETRY ASYMMETRY = PRESENT`

But it also reveals that two components are entangled:

1. nonlinear logit→probability information geometry;
2. active AP-A projection bounds.

It would therefore be premature to proceed directly to paired 49/99/199 bootstrap characterization.

## Next gate

Before Stage B, freeze a deterministic projection-bound sensitivity audit.

That audit should:

- keep the same 12 complement cases and original general coefficient paths;
- compare nearest-CBD projection under the current fitter bounds against prospectively widened diagnostic bounds;
- report whether nearest-CBD RMS, nearest parameters, probability RMS, KL and sign ratios materially change;
- identify which current cases are boundary-limited;
- not change the operational fitter or the already-retained #158 result.

Only after separating bound-induced geometry from intrinsic CBD-manifold/logistic geometry should a paired same-dataset bootstrap comparison be designed.

## Boundary

`STAGE A = COMPLETE / DETERMINISTIC ONLY`

`CURRENT DEPARTURE DEFINITION = UNCHANGED`

`PROJECTION-BOUND SENSITIVITY = REQUIRED NEXT`

`PAIRED BOOTSTRAP STAGE = NOT YET FROZEN`

`49 DRAWS = NOT AUTHORITATIVELY FROZEN`

`20 REPLICATES = NOT AUTHORITATIVELY FROZEN`

`AUTHORITATIVE POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`

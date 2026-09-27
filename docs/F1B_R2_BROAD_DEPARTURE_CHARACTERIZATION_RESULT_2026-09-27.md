# F1b R2 Broad Controlled-Departure Characterization — Result

Status: **COMPLETED / NON-AUTHORITATIVE DESIGN CHARACTERIZATION**

Issue: #158  
Parent design: #145  
Frozen design merge: `1f44579628e63c69714d90549e4fd39aa74dc5ab`  
Execution run: `36309694914`  
Temporary execution PR: #161

## Execution integrity

The frozen 49×20 design completed in four replicate shards and was recombined with the integrated fail-closed partition combiner.

- controlled-departure cases: 36;
- aggregate restriction cells: 75;
- exact restriction trials: 1500;
- evaluation replicates covered: 0–19 exactly once;
- fit failures: 0;
- bootstrap-calibration failures: 0;
- bootstrap-fit failures: 0.

The exact combined Actions result is artifact `10928507819`.

- artifact ZIP SHA-256: `473ce154643c7a2a1f47af4b7011292f668f5bb11993e20cfd09f4ce87a1e41d`;
- combined JSON SHA-256: `21e5bb861987a1090c3c8fcfb7736795862c65637e771df026eff8ba2a304d8e`.

All 75 aggregate cells, including achieved/nearest-ADD distances and held-out predictive deltas, are retained in the repository TSV.

## Fresh-seed null characterization

| Null | Rejections | Rate |
|---|---:|---:|
| ADD null | 0/20 | 0.00 |
| CBD anchor 1 | 1/20 | 0.05 |
| CBD anchor 2 | 0/20 | 0.00 |

With only 20 replicates per null, these remain coarse characterization rates, not validation of exact alpha.

## Standalone-accuracy ADD specificity

The 12 standalone-accuracy cells are exactly ADD-compatible by construction.

Across those cells:

- ADD rejections: 9/240;
- pooled rate: 0.0375;
- Wilson 95% interval: approximately [0.0199, 0.0697];
- maximum rejections in any one 20-replicate cell: 2.

No gross ADD-specificity pathology is visible in this stage.

## CBD departure detection

Pooled by axis and requested nearest-CBD RMS distance:

| Axis | 0.10 | 0.25 | 0.50 |
|---|---:|---:|---:|
| Standalone accuracy | 8/80 | 62/80 | 80/80 |
| Combined violation | 9/80 | 58/80 | 80/80 |
| Complement relation | 17/80 | 35/80 | 59/80 |

The standalone and combined axes show the expected strong increase from 0.10 to 0.25 to 0.50.

The complement-relation axis is different and must not be pooled away as if it behaved identically.

## Complement-relation sign asymmetry

Pooling both CBD anchors:

| Distance | minus sign | plus sign |
|---|---:|---:|
| 0.10 | 8/40 | 9/40 |
| 0.25 | 24/40 | 11/40 |
| 0.50 | 38/40 | 21/40 |

The strongest cell-level differences are:

- CBD_ANCHOR_2 at 0.25: 14/20 minus versus 2/20 plus;
- CBD_ANCHOR_2 at 0.50: 19/20 minus versus 10/20 plus;
- CBD_ANCHOR_1 at 0.50: 19/20 minus versus 11/20 plus.

One cell series is non-monotone:

`CBD_ANCHOR_2 × COMPLEMENT_RELATION_VIOLATION × plus`

- RMS 0.10: 5/20;
- RMS 0.25: 2/20;
- RMS 0.50: 10/20.

This is a required diagnostic finding, not a reason to select the easier sign.

## Held-out predictive diagnostics

The stored deltas are:

`general predictive log likelihood − restricted predictive log likelihood`.

Positive values therefore favor the general model on the held-out split.

For CBD complement testing, the same sign asymmetry appears in predictive diagnostics:

- complement minus, RMS 0.25: mean participant delta ≈ +0.628 and item delta ≈ +0.211;
- complement plus, RMS 0.25: mean participant delta ≈ −0.322 and item delta ≈ −0.130;
- complement minus, RMS 0.50: mean participant delta ≈ +0.693 and item delta ≈ +0.646;
- complement plus, RMS 0.50: mean participant delta ≈ +0.158 and item delta ≈ +0.237.

The asymmetry is therefore not confined to bootstrap rejection counts.

For standalone ADD-specificity cells, held-out ADD deltas remain predominantly negative or near zero, consistent with the data generator staying on the ADD surface.

## ADD diagnostics on non-standalone departures

These are descriptive only because complement/combined departures are not required to stay ADD-compatible.

Pooled ADD rejection:

| Axis | 0.10 | 0.25 | 0.50 |
|---|---:|---:|---:|
| Combined violation | 16/80 | 47/80 | 78/80 |
| Complement relation | 35/80 | 78/80 | 80/80 |

This confirms that many larger complement/combined departures move away from ADD as well, but it does not turn the exercise into model classification.

## Cross-shard numerical reproducibility

Each execution shard regenerated the deterministic controlled-departure design on a separate GitHub runner.

Across nominally identical case identities:

- maximum achieved-CBD-distance range: approximately `1.86e-11`;
- maximum nearest-ADD-distance range: approximately `1.38e-11`;
- frozen design-generation tolerance: `1e-6`.

The observed floating-point drift is many orders of magnitude below the frozen tolerance and does not threaten this characterization. For a future authoritative run, pre-materializing the exact departure coefficients would nevertheless be preferable if bitwise cross-run identity is required.

## Scientific interpretation

The broad characterization establishes three things:

1. the 49-draw bootstrap pipeline is computationally stable across the complete frozen grid;
2. the corrected standalone ADD negative control behaves plausibly at this resolution;
3. CBD departure detection is strongly geometry-dependent, especially for the complement-relation direction and its sign.

It does **not** establish a final bootstrap draw count, exact type-I-error control, authoritative power, a final core grid, or human sample size.

The complement sign asymmetry is large enough that moving directly to an authoritative power/N calculation would be premature.

## Next gate

Before any authoritative R2 or human-N freeze, prospectively define a focused complement-relation diagnostic that separates:

- genuine geometry/sign asymmetry of the restricted manifold;
- finite-replicate Monte Carlo variation;
- bootstrap-draw discretization/stability;
- penalized hierarchical fitter behavior;
- any residual sensitivity to anchor and random-effect scale.

The next diagnostic must use a fresh seed and preserve both signs.

## Boundary

`49 BOOTSTRAP DRAWS = NOT AUTHORITATIVELY FROZEN`

`20 EVALUATION REPLICATES = NOT AUTHORITATIVELY FROZEN`

`EXACT ALPHA CONTROL = NOT VALIDATED`

`AUTHORITATIVE POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`

# F1b R2 paired inference-method M2 result — 2026-09-28

Issue: #259

Status: **M2 COMPLETE / ALL FOUR METHODS ELIGIBLE / NO METHOD SELECTED**

## Execution

The first M2 attempt (#269) failed closed before any new bootstrap draw because the retained M1 artifact status literal was bound incorrectly.

PR #270 corrected only that provenance literal and added a regression test.

Rerun #271 then executed the unchanged frozen M2 design:
- 80/80 shard jobs successful;
- 840 scientific runs;
- 3,360 method-specific sequential streams;
- runtime numerical lineage: Haswell;
- zero bootstrap refit failures.

Combined evidence:
- workflow run: `36450594439`;
- artifact ID: `10987519941`;
- artifact ZIP SHA-256:
  `4023ffe01d0891ea0045248f35f0b0f1c8d3265f7a702251203c753b1752e313`;
- combined JSON SHA-256:
  `b9034afd6b6837c8433e0d42fd90911a7b560e18225de7d551f559330742c808`;
- combined JSON size: 6,432,851 bytes;
- combined row-identity SHA-256:
  `b21ee68fd61a0f1364c0722e73ff472119075ae32ee380021b8a671df76c4707`.

Temporary PR #271 was closed unmerged after evidence capture.

## M2 eligibility

All four prospectively tested inference variants satisfy every frozen M2 criterion:

### POPULATION
- decision: `M2_ELIGIBLE`;
- resolved: 808 / 840;
- unresolved-at-cap: 32;
- refit failures: 0;
- overall resolution: 0.9619;
- minimum role × missingness resolution: 0.90.

### HIERARCHICAL_0.5X
- decision: `M2_ELIGIBLE`;
- resolved: 793 / 840;
- unresolved-at-cap: 47;
- refit failures: 0;
- overall resolution: 0.9440;
- minimum role × missingness resolution: 0.90.

### HIERARCHICAL_1X
- decision: `M2_ELIGIBLE`;
- resolved: 819 / 840;
- unresolved-at-cap: 21;
- refit failures: 0;
- overall resolution: 0.9750;
- minimum role × missingness resolution: 0.95.

### HIERARCHICAL_2X
- decision: `M2_ELIGIBLE`;
- resolved: 816 / 840;
- unresolved-at-cap: 24;
- refit failures: 0;
- overall resolution: 0.9714;
- minimum role × missingness resolution: 0.95.

No method fails:
- M1 eligibility inheritance;
- refit stability;
- global sequential resolution;
- role × missingness sequential resolution.

## No method winner

The M2 criteria are feasibility and interpretability criteria, not a ranking rule.

The highest global resolution rate therefore does not select HIERARCHICAL_1X.

Pairwise decision concordance among streams resolved by both methods is:
- POPULATION vs HIERARCHICAL_0.5X: 1.0000;
- POPULATION vs HIERARCHICAL_1X: 0.9632;
- POPULATION vs HIERARCHICAL_2X: 0.8457;
- HIERARCHICAL_0.5X vs HIERARCHICAL_1X: 0.9961;
- HIERARCHICAL_0.5X vs HIERARCHICAL_2X: 0.8765;
- HIERARCHICAL_1X vs HIERARCHICAL_2X: 0.9107.

These differences show that inference-scale choice remains scientifically consequential.

## Hierarchical scale sensitivity

The retained M1 scale-sensitivity signal remains present after sequential resolution.

For CBD departure detection at KL=0.003:

Missingness 0:
- 0.5× expected-direction bounds: [0.5000, 0.5833];
- 1×: [0.5000, 0.5000];
- 2×: [0.2333, 0.3167].

Missingness 0.15:
- 0.5×: [0.4667, 0.6000];
- 1×: [0.4333, 0.4667];
- 2×: [0.2500, 0.3333].

This is evidence for continued scale characterization, not for selecting the scale with the largest observed rate.

## Consequence for S4

The S4 broad scientific matrix is independently frozen at:
- 15,000 scientific runs;
- 100 deterministic replicates per cell × missingness;
- worst-case component MCSE <= 0.05.

Because every M2 method is eligible, the broad method set must contain all four methods.

Therefore the broad characterization has:

`15,000 × 4 = 60,000 method executions`.

This number is a design consequence, not a post-hoc expansion.

## Boundary

`M2 = COMPLETE / RETAINED`

`M2 ELIGIBLE METHODS = 4 / 4`

`METHOD SELECTED = NO`

`HIERARCHICAL SCALE SENSITIVITY = RETAINED`

`S4 BROAD SCIENTIFIC MATRIX = 15,000 RUNS`

`S4 BROAD METHOD EXECUTIONS = 60,000`

`POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

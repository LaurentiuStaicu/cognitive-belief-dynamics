# F1b R2 paired inference-method M1 result — 2026-09-28

Issue: #259

Status: **M1 COMPLETE / ALL FOUR METHODS ELIGIBLE / HIERARCHICAL SCALE SENSITIVE / NO METHOD SELECTED**

## Execution

Temporary execution:
- PR #266 — closed unmerged;
- workflow run `36439940794`;
- execution head `4500ca5faca0a4d9355ae1e8ea44db4da3495448`;
- qualified main baseline `54566e16bb64538ea6ab6205858b1194b5a2d510`;
- ordinary CBD validation #595 — success.

M1 evidence:
- 20/20 scientific shards — success;
- combined artifact ID `10979254047`;
- artifact ZIP SHA-256:
  `d419d54197e84b0ad41c24aedde7ef2f41ff4eee09e9e071a8405176b05ff054`;
- combined JSON SHA-256:
  `dda3978acbf13ae9dba4d548ae8355413b29c8cac24ad86d5b8905de56d81042`;
- combined JSON size: 5,667,170 bytes.

Every completed shard passed runtime `Haswell` verification and the pairing checks.

## Frozen M1 design

M1 used:
- missingness 0.00 and 0.15;
- all 72 frozen departure cells;
- 5 departure replicates/cell/regime;
- 20 replicates for each of the three null identities/regime;
- 840 scientific restriction runs;
- 4 inference variants;
- 3,360 paired method executions;
- exactly 199 bootstrap attempts/execution;
- >=180 successful refits required;
- no continuation beyond draw index 198.

The four variants were:
- `POPULATION`;
- `HIERARCHICAL_0.5X`;
- `HIERARCHICAL_1X`;
- `HIERARCHICAL_2X`.

## M1 verdict

Overall:

`M1_HAS_ELIGIBLE_METHODS`

Eligible:
- `POPULATION`;
- `HIERARCHICAL_0.5X`;
- `HIERARCHICAL_1X`;
- `HIERARCHICAL_2X`.

For every variant:
- operational failure rate = 0;
- operational check = PASS;
- null gross-pathology check = PASS;
- ADD specificity check = PASS;
- strong-departure signal-separation check = PASS;
- missingness-degradation check = PASS.

Therefore no method may be removed using the prospectively frozen M1 A–E rules.

## Descriptive screening values

These are fixed-199 M1 screening rates, not terminal sequential outcomes and not validated power.

### POPULATION
Null false rejection:
- missingness 0: 0.100;
- missingness 0.15: 0.083.

ADD specificity false rejection:
- 0: 0.117;
- 0.15: 0.150.

Strong expected-direction rejection:
- CBD: 0.550 / 0.533;
- ADD: 0.675 / 0.725.

### HIERARCHICAL_0.5X
Null false rejection:
- 0: 0.100;
- 0.15: 0.067.

ADD specificity false rejection:
- 0: 0.083;
- 0.15: 0.100.

Strong expected-direction rejection:
- CBD: 0.567 / 0.567;
- ADD: 0.675 / 0.675.

### HIERARCHICAL_1X
Null false rejection:
- 0: 0.050;
- 0.15: 0.067.

ADD specificity false rejection:
- 0: 0.050;
- 0.15: 0.067.

Strong expected-direction rejection:
- CBD: 0.500 / 0.517;
- ADD: 0.675 / 0.650.

### HIERARCHICAL_2X
Null false rejection:
- 0: 0.017;
- 0.15: 0.017.

ADD specificity false rejection:
- 0: 0.017;
- 0.15: 0.033.

Strong expected-direction rejection:
- CBD: 0.250 / 0.283;
- ADD: 0.575 / 0.550.

The rates are listed in missingness order 0 / 0.15.

## Hierarchical scale sensitivity

M1 sets:

`HIERARCHICAL_SCALE_SENSITIVE = true`.

The sensitivity threshold was max-minus-min > 0.20 across 0.5× / 1× / 2×.

The flag is driven by strong CBD departure detection at KL=0.003:

Missingness 0:
- 0.5× = 0.567;
- 1× = 0.500;
- 2× = 0.250;
- range = 0.317.

Missingness 0.15:
- 0.5× = 0.567;
- 1× = 0.517;
- 2× = 0.283;
- range = 0.283.

Other flagged strata remain below the 0.20 threshold:
- ADD specificity range = 0.067 in each missingness regime;
- strong ADD departure range = 0.100 / 0.125.

This is meaningful inference-scale sensitivity.

It is not a license to select 0.5× or 1× because their M1 detection rate is higher. All three hierarchical scale variants passed every predeclared A–E eligibility rule.

## Interpretation before M2

The scale-sensitivity flag does not automatically select a fitted random-effect scale.

Dropping `HIERARCHICAL_2X` now because it produced lower fixed-199 CBD detection would introduce a post-hoc performance rule that was not part of M1.

Therefore the non-selective interpretation is:

- retain all four M1-eligible inference variants;
- carry the hierarchical scale-sensitivity flag forward;
- bind M2 method membership exactly to the M1 eligible set;
- let M2 characterize sequential resolution / unresolved-at-cap behavior without relabelling M1 non-rejections as terminal decisions.

M2 must preserve:
- the qualified resampling-risk controller;
- n=199 prefix identity;
- first new draw index 199 for streams unresolved by the sequential boundary at n=199;
- stop-on-boundary;
- stop-on-bootstrap-refit-failure;
- the 10,000-attempt cap unless a separate prospective contract explicitly changes the scientific question;
- identical scientific datasets across methods;
- common random numbers across hierarchical scale variants;
- the distinct population bootstrap namespace.

## S4 boundary

M1 is a screening stage, not the final Monte Carlo characterization.

The broad target remains:
- n_eval = 100 per departure cell;
- worst-case component MCSE <= 0.05.

This follows the already frozen S4 design criterion. The current 5-replicate M1 departure screening cannot substitute for the later n=100/cell characterization.

## Boundary

`M1 = COMPLETE / RETAINED`

`M1 ELIGIBLE METHODS = ALL FOUR`

`HIERARCHICAL SCALE SENSITIVE = YES`

`METHOD SELECTED = NO`

`M1 FIXED-199 OUTCOMES = NOT TERMINAL SEQUENTIAL DECISIONS`

`M2 = REQUIRED BEFORE BROAD CHARACTERIZATION`

`POWER VALIDATED = NO`

`BROAD N_EVAL=100/CELL = NOT EXECUTED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`

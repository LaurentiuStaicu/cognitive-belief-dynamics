# F1b R2 paired inference-method smoke result — 2026-09-28

Issue: #259

Status: **SMOKE PASS / POPULATION + HIERARCHICAL PIPELINES OPERATIONAL / NO METHOD SELECTED**

## Purpose

Verify that the newly added population-level restriction comparator and the existing hierarchical restriction engine can operate on the exact same retained scientific datasets before a larger paired characterization is designed.

This smoke does not estimate calibration, specificity or power.

## Frozen source

Retained homogeneous H1 source:
- artifact ID `10961527329`;
- JSON SHA-256:
  `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`.

Evaluation replicate:
- `0`.

Selected structurally before execution:
- ADD null;
- CBD null at CBD_ANCHOR_1;
- standalone-accuracy / + sign / KL 0.002 / CBD_ADD_INTERSECTION_ANCHOR_1, tested independently against CBD and ADD.

Totals:
- 3 unique datasets;
- 4 restriction runs;
- 2 inference methods;
- 8 method executions.

## Methods

- `HIERARCHICAL_1X`;
- `POPULATION`.

Each execution used:
- 5 bootstrap draws;
- 5 required successful refits;
- alpha 0.05 only as an API parameter.

Five draws are intentionally inadequate for scientific decision interpretation.

## Result

PASS:
- 3/3 regenerated dataset fingerprints exactly match retained H1;
- 4/4 hierarchical first-five bootstrap prefixes exactly match retained H1;
- 8/8 method executions completed;
- every execution had 5/5 successful bootstrap refits;
- population and hierarchical bootstrap namespaces are distinct;
- all required diagnostics are finite;
- runtime OpenBLAS cores were `Haswell, Haswell`.

No scientific/config/controller source was changed by the execution PR.

## Cost smoke

Measured method-call wall time across the four restriction runs:
- hierarchical 1× total: 1.0426 s;
- population total: 0.6759 s;
- population/hierarchical ratio: ~0.648.

This is only a small smoke-cost observation.

It is not a method-selection criterion and must not be extrapolated linearly to the future full characterization without a dedicated cost study.

The workflow also paid one-time setup/design-regeneration overhead that is not represented by the method-call timers.

## Scientific interpretation

The smoke establishes only:
- both inference pipelines are operational;
- exact observed-dataset pairing is feasible;
- deterministic method-specific bootstrap namespaces are feasible;
- the hierarchical current pipeline remains bitwise consistent with the retained H1 first-five bootstrap prefix on the selected runs.

It does not establish:
- false-rejection control;
- specificity;
- detection probability;
- population superiority;
- hierarchical superiority;
- variance-scale robustness;
- missingness robustness;
- power;
- evaluation-replicate adequacy.

## Next step

Freeze a prospective paired method-characterization design before executing additional bootstrap work.

That design must:
- use identical scientific datasets across inference methods;
- include POPULATION and HIERARCHICAL 0.5× / 1× / 2×;
- include missingness 0 and 0.15;
- retain KL 0.001 / 0.002 / 0.003;
- predeclare method-selection criteria;
- characterize computational cost before committing to the full n=100/cell broad characterization.

## Boundary

`PAIRED METHOD SMOKE = PASS / RETAINED`

`METHOD SELECTED = NO`

`POWER VALIDATED = NO`

`N_EVAL FROZEN = NO`

`MISSINGNESS 0.15 CHARACTERIZED = NO`

`HIERARCHICAL SCALE SENSITIVITY = NOT YET CHARACTERIZED FOR RESTRICTION TARGET`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`

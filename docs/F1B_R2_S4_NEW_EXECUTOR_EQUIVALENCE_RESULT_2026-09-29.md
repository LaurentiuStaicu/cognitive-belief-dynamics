# F1b R2 S4 new-executor equivalence result — 2026-09-29

Issue: #259

Status: **12/12 EXACT MATCH / BROAD EXECUTOR QUALIFIED / FRESH-REPLICATE PREFLIGHT STILL REQUIRED**

The S4 new-executor equivalence gate was merged in PR #287.

The first temporary replay (#288) failed after numerical execution because the final selected-row digest was serialized differently in selection and result construction. PR #290 corrected only that bookkeeping representation and added a regression test. The numerical executor, selected rows, artifacts, RNG, controller, cap and numerical lineage were unchanged.

Rerun #291 then passed completely and was closed unmerged.

Execution evidence:
- workflow run: `36533726273`;
- artifact ID: `11017014561`;
- artifact ZIP SHA-256: `050a9eb57ea50b4b2ed3b82a422ce30a3f7255645986e44bf2f19eab0aeb721d`;
- result JSON SHA-256: `701cd31d4c93f1e17be362db5d3bdb0ca2032decfa8fff93c364c0395f160f89`;
- runtime OpenBLAS cores: `Haswell`, `Haswell`;
- elapsed execution time: 848.59 seconds.

## Exact replay result

Frozen selection:
- 12 retained M2 method rows;
- 7 unique scientific runs;
- four inference methods;
- three retained terminal-status classes.

Selection SHA-256:
`41062e2bf501799a41b78d412b33551685045b98b9a67c9d50a9a26131c16b36`.

Result:
- exact matches: 12;
- mismatches: 0.

Reproduced evidence SHA-256:
`8de59c440b348efe72f901bdbd36b85f1e7db485ede96ffc74d438b11159f24d`.

The new S4 executor reproduces the retained M2 evidence exactly for the frozen equivalence sample.

## Provenance

The replay pins:
- executor Git blob: `ab1eb088c8551733909d3f1fb7acdb8c59e7da44`;
- H1 source SHA-256: `618b52162e98d25d41ac9cc7a6411ccfbf3c95775412a46b759e1514e90ed37e`;
- M2 combined SHA-256: `b9034afd6b6837c8433e0d42fd90911a7b560e18225de7d551f559330742c808`;
- S4 manifest SHA-256: `f0691a0dc153f2ee1463f5115feeff448b49e7d2fb7accd6568a0fb8c43a5f01`.

## Consequence

The broad executor is qualified for the next operational preflight.

This does not yet authorize W0.

Before W0, a fresh-replicate preflight must execute deterministic S4 runs outside the retained M2 prefix:
- departure replicate 5;
- null replicate 20;
- both missingness regimes;
- all scientific role families;
- all four methods.

The preflight is structural/operational, not a power sample. Scientifically unfavorable outcomes do not constitute preflight failure.

## Version boundary

The next planned public scientific-core release remains `v0.2.0` under Issue #277.

This equivalence result does not close the release blocker.

The blocker remains the completed, retained and scientifically interpreted broad S4 characterization.

## Boundary

`NEW EXECUTOR EQUIVALENCE = 12 / 12 EXACT`

`BROAD EXECUTOR = QUALIFIED`

`FRESH PREFLIGHT = STILL REQUIRED`

`W0 = NOT YET AUTHORIZED`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`

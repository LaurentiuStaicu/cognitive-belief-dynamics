# F1b R2 S4 method-binding result — 2026-09-28

Issue: #259

Status: **METHOD BINDING COMPLETE / 60,000 BROAD METHOD IDENTITIES / BROAD EXECUTION NOT YET RUN**

The S4 method-binding gate was merged in PR #278 and executed in temporary PR #279, which was closed unmerged.

Execution evidence:
- workflow run: `36467231113`;
- artifact ID: `10990660300`;
- artifact ZIP SHA-256: `e8f954a9598d0cef67f2e4e24343000ec5cee709fa75e8a0c9590f657b33166e`;
- binding JSON SHA-256: `5dacc358d97ed38807991bf7bfd77be26bfd766a95627645e6bdf212de96402a`;
- binding JSON size: 1,814 bytes.

The exact retained sources are:
- M2 combined JSON SHA-256: `b9034afd6b6837c8433e0d42fd90911a7b560e18225de7d551f559330742c808`;
- M2 row-identity SHA-256: `b21ee68fd61a0f1364c0722e73ff472119075ae32ee380021b8a671df76c4707`;
- S4 matrix manifest SHA-256: `f0691a0dc153f2ee1463f5115feeff448b49e7d2fb7accd6568a0fb8c43a5f01`;
- S4 scientific-run-ID SHA-256: `851e7336387901ca15d2486ed8efc19cd090ffac869b760352106a3f455f2b43`.

## Bound broad design

The exact method list is:
1. POPULATION;
2. HIERARCHICAL_0.5X;
3. HIERARCHICAL_1X;
4. HIERARCHICAL_2X.

The broad characterization is therefore fixed at:
- 15,000 scientific runs;
- 4 methods;
- 60,000 method executions;
- worst-case component MCSE target 0.05.

No method is selected as winner.

Hierarchical scale sensitivity remains part of the scientific result and must remain visible in broad S4.

## Next gate

Before any broad execution, validate the exact M2 → S4 deterministic prefix bridge.

The broad S4 matrix contains all 840 M2 scientific runs:
- departure replicates 0..4;
- null replicates 0..19;
- both missingness regimes.

The next gate must determine whether the 3,360 retained M2 method rows can be imported as exact prefix evidence by checking scientific-run identity, dataset SHA, method/scale, RNG namespace, controller identity, numerical lineage and terminal evidence.

A row that fails the bridge must be recomputed rather than dropped or replaced.

## Version boundary

The next planned public scientific-core release is v0.2.0 under Issue #277.

This binding does not close that release blocker.

v0.2.0 remains blocked until broad S4 is executed, retained and scientifically interpreted.

## Boundary

`METHOD BINDING = COMPLETE / RETAINED`

`S4 SCIENTIFIC RUNS = 15,000`

`S4 METHODS = 4`

`S4 METHOD EXECUTIONS = 60,000`

`BROAD EXECUTION = NOT YET PERFORMED`

`METHOD SELECTED = NO`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`

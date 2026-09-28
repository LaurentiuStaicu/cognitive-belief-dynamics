# F1b R2 OpenBLAS Q1 qualification result — 2026-09-28

Issue: #227

Status: **Q1 PASSED / NON-AUTHORITATIVE / Q2 REQUIRED**

Temporary execution:
- PR #229 — closed unmerged;
- workflow run `36391781169`;
- execution head `2766ccdad7fa92943f60d5c79ca5d0b1314d6641`;
- qualified main baseline `0723d33a74dbdb0479faca9fa61124f95bf546bc`.

Candidate numerical execution lineage:

`OPENBLAS_CORETYPE=Haswell`

## Q1 design

The four predeclared diagnostic sentinels from #223 were replayed on four independent GitHub-hosted Ubuntu runners each.

Total executions:

`4 sentinels × 4 replicas = 16`

Every execution:
- ran the merged Q0 environment verifier;
- confirmed both reported OpenBLAS instances as `Haswell`;
- downloaded the exact retained paired source;
- regenerated the sentinel dataset using the unchanged Stage-C1 path;
- replayed draw indices 0..198 only;
- required exact dataset fingerprint;
- required exact retained observed statistic, not merely the historical `1e-10` tolerance;
- required exact retained first-199 attempt-sequence SHA-256;
- confirmed the scientific process itself reported `Haswell`.

## Result

`16 / 16 PASS`

Across all 16 executions:
- Q0 runtime cores: `Haswell, Haswell`;
- scientific-process runtime cores: `Haswell, Haswell`;
- dataset fingerprint match: exact;
- observed-statistic delta: exactly `0.0`;
- complete first-199 attempt-sequence hash: exact;
- first divergent draw: none.

The runs covered four reported CPU models:
- AMD EPYC 7763;
- AMD EPYC 9V74;
- Intel Xeon Platinum 8573C;
- Intel Xeon Platinum 8370C.

Software identity was constant:
- Python 3.12.14;
- NumPy 2.5.3;
- SciPy 1.18.1.

The exact retained result is stored at:

`model/results/f1b_r2_openblas_q1_qualification_2026-09-28.json`

That result also records the 16 artifact IDs, artifact ZIP SHA-256 values, sentinel identities and canonical retained hashes.

## Interpretation

Q1 establishes that the candidate `Haswell` OpenBLAS execution contract reproducibly restores the retained/source numerical trajectory across all four diagnostic strata and across multiple CPU families.

It does not yet qualify all 224 unresolved streams.

Therefore:

`Q1 = PASS`

`Q2 = REQUIRED`

`STAGE_C1 V1 = FAILED / RETAINED`

`STAGE_C2 = BLOCKED`

No scientific fitter, package, seed, tolerance, draw ordering or controller setting changed. No draw index >=199 was generated. No power, human-N, recruitment or runtime F1b claim is made.

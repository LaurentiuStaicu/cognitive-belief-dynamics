# F1b R2 R08_09 SkylakeX source-lineage result — 2026-09-28

Issue: #227

Status: **SOURCE-SHARD HYPOTHESIS PASSED / HISTORICAL SOURCE HETEROGENEITY SUPPORTED / STAGE C2 BLOCKED**

Temporary execution:
- PR #232 — execution-only, do not merge;
- workflow run `36394804631`;
- execution head `ae65162a152cf3afc12f54c5ab887e4750596da7`;
- main baseline `a091605be31f7035217253b5e8c453af14cdcdd1`.

Exact retained paired source:
- artifact ID `10938668225`;
- JSON SHA-256 `b2727462b5bd09e5570090a42d7c90da8866e02100e0f4ccad551d8958a3d301`.

## Why this test was required

The Q2 Haswell full replay reproduced 175/224 Stage-C1-eligible streams exactly and failed 49/224.

Those 49 failures were exactly the eligible streams with evaluation replicate 8 or 9. The boundary matched the historical paired-source execution shard `R08_09`.

The follow-up therefore tested the predeclared hypothesis that those 49 retained source streams belong to a distinct numerical execution lineage reproducible under the OpenBLAS `SkylakeX` path.

## Safety correction before evidence collection

The first PR #232 attempt forced `OPENBLAS_CORETYPE=SkylakeX` on every sampled runner.

Some runners then terminated with exit code 132 after reporting `Core: SkylakeX`. Those executions never produced a scientific replay result and are not evidence for or against the hypothesis.

The workflow was corrected before interpreting a result:
1. probe the natural OpenBLAS core without an override;
2. treat non-`SkylakeX` runners as sampling misses;
3. only on naturally `SkylakeX`-capable runners, start a fresh process with `OPENBLAS_CORETYPE=SkylakeX`;
4. verify the scientific process itself reports only `SkylakeX`.

## Predeclared test

Target:
- exactly 49 Stage-C1-eligible streams;
- evaluation replicate in `{8, 9}`;
- retained draw indices 0..198 only.

For every target stream require:
- exact dataset fingerprint;
- exact retained/source observed statistic;
- exact complete first-199 attempt-sequence SHA-256.

Acceptance:

`49 / 49 exact source reproductions`

No draw index >=199 was generated.

## Result

Sixteen GitHub-hosted Ubuntu runners were sampled.

- 9 were non-`SkylakeX` sampling misses and did not execute the scientific replay;
- 7 were naturally `SkylakeX`-capable and completed the full 49-stream replay.

All seven eligible executions passed:

`7 independent executions × 49 streams = 343 / 343 exact source reproductions`

For every eligible execution:
- natural OpenBLAS runtime core: `SkylakeX, SkylakeX`;
- scientific-process runtime core: `SkylakeX, SkylakeX`;
- exact dataset fingerprints: 49/49;
- exact observed statistics: 49/49;
- exact first-199 attempt-sequence hashes: 49/49;
- first divergent draw: none.

Eligible CPU models included:
- AMD EPYC 9V45 96-Core Processor;
- Intel Xeon 6973P-C;
- Intel Xeon Platinum 8370C;
- Intel Xeon Platinum 8573C.

The canonical SHA-256 of the ordered 49-row comparison payload was identical in all seven eligible artifacts:

`042882f5895871152923f443cd8158b7d080441b00497ac423b3d955c547ed2f`

The combined result JSON SHA-256 is:

`1df20dbedba22f3a0745e323a4d5bd351e5dccce95979db17ffd910144231d19`

Combined Actions artifact:
- ID `10957358993`;
- ZIP SHA-256 `b39699cd8bf28beb78df330a49af0d0710eaee701767e1455b1cfdc3836ad46e`.

The retained machine-readable result is:

`model/results/f1b_r2_r08_09_skylakex_source_lineage_2026-09-28.json`

It records all seven eligible artifact IDs and ZIP digests.

## Interpretation

The simple source-shard hypothesis passes.

The existing combined paired-source artifact contains at least two reproducible numerical trajectories:

- the 175 eligible streams from evaluation replicates 0–7 are reproducible under the prospectively tested Haswell path;
- the 49 eligible streams from evaluation replicates 8–9 are reproducible under the SkylakeX path.

The historical source-shard runner core names were not recorded at source-generation time, so this result does not claim direct observation of the original runners' OpenBLAS core selection. It establishes exact reproducibility of the two retained numerical trajectories under the two identified OpenBLAS paths.

This means the existing combined source must not be treated as one homogeneous numerical execution lineage.

## Consequence for continuation

Do not repair continuation by reproducing each historical shard under a different core.

That would preserve the historical heterogeneous artifact rather than establish a prospective reproducible scientific execution lineage.

The next gate must instead define and generate a new versioned paired source under one homogeneous, runtime-verified numerical environment. Downstream bootstrap/resampling-risk checkpoints derived from the heterogeneous paired source cannot be silently inherited by that new source; their lineage must be rebuilt or requalified prospectively.

Therefore:

`STAGE-C1 V1 = FAILED / RETAINED`

`Q1 HASWELL SENTINELS = PASS / HISTORICAL`

`Q2 HASWELL FULL REPLAY = FAIL 175/224 / RETAINED`

`R08_09 SKYLAKEX SOURCE-LINEAGE TEST = PASS 49/49 ON 7/7 ELIGIBLE RUNNERS`

`EXISTING PAIRED SOURCE = NUMERICALLY HETEROGENEOUS`

`HOMOGENEOUS FUTURE EXECUTION LINEAGE = NOT YET SELECTED`

`STAGE C2 = BLOCKED`

No scientific model form, fitter settings, package versions, seed derivation, tolerance, draw ordering or controller parameters were changed. No power, human-N, recruitment or runtime F1b claim is made.

# F1b R2 KL V2 Paired Bootstrap Draw-Stability Result

Status: **COMPLETE / NON-AUTHORITATIVE / NO DRAW COUNT SELECTED**

Issue: #206  
Scientific source: `6ad6be092fd3e6b9ec17c3935e19711710690beb`

## Purpose

This stage isolates the effect of bootstrap draw count by holding the synthetic dataset and bootstrap random stream fixed.

The draw counts are:

- 49;
- 99;
- 199.

For each dataset × restriction identity, one 199-attempt bootstrap stream is generated and the 49- and 99-draw results are exact prefixes of that same stream.

The experiment therefore compares draw count under common random inputs rather than comparing independently generated datasets.

## Pre-result integrity correction

The first attempted paired execution was invalidated before result inspection because the stable dataset identity did not explicitly contain the paired characterization/version identity.

That execution is not retained.

PR #209 then added two fail-closed guards before the corrected run:

1. every null and departure dataset identity explicitly contains the frozen characterization ID;
2. the current KL V2 config SHA-256 must match the config SHA-256 retained by the deterministic V2 qualification result.

The corrected scientific source is:

`6ad6be092fd3e6b9ec17c3935e19711710690beb`

## Exact execution

Corrected temporary execution:
- PR #210;
- Actions run `36339370047`;
- five two-replicate shards.

The original combined job later failed only in temporary summary code because `os.environ` was referenced without importing `os`.

No scientific shard failed.

PR #211 / run `36340881516` therefore recovered the combined result by downloading the five immutable shard artifacts and rerunning only the repository combiner.

No dataset or bootstrap fit was rerun in recovery.

## Exact retained artifact

Recovered combined artifact:
- artifact ID: `10938668225`;
- ZIP SHA-256:
  `008bc62bc5048011cd015fa133111627e7a88b35bb5eb194b8e3dca062d547d7`;
- exact JSON SHA-256:
  `b2727462b5bd09e5570090a42d7c90da8866e02100e0f4ccad551d8958a3d301`;
- exact JSON size: 9,013,672 bytes.

The exact artifact contains all:
- 390 unique datasets;
- 750 dataset×restriction runs;
- 2,250 draw-count snapshots;
- 2,250 paired draw-count comparisons.

The repository retains the compact scientific summary plus exact hashes/provenance instead of duplicating the full artifact.

## Operational integrity

Across the full corrected experiment:

- observed-fit failures: 0;
- bootstrap-calibration failures: 0;
- bootstrap-refit failures: 0;
- valid draw-count snapshots: 2,250 / 2,250.

Thus all three draw counts were operationally stable under the frozen thresholds.

## Global paired stability

### 49 vs 99

- comparisons: 750;
- discordant decisions: 37;
- concordance: 95.07%;
- not-reject → reject: 32;
- reject → not-reject: 5;
- mean absolute p-value difference: 0.02532;
- maximum absolute p-value difference: 0.18.

### 49 vs 199

- comparisons: 750;
- discordant decisions: 43;
- concordance: 94.27%;
- not-reject → reject: 37;
- reject → not-reject: 6;
- mean absolute p-value difference: 0.03179;
- maximum absolute p-value difference: 0.24.

### 99 vs 199

- comparisons: 750;
- discordant decisions: 16;
- concordance: 97.87%;
- not-reject → reject: 10;
- reject → not-reject: 6;
- mean absolute p-value difference: 0.01711;
- maximum absolute p-value difference: 0.12.

The descriptive pattern is therefore clear: in this paired experiment, 99 and 199 are closer to one another than either comparison involving 49.

This is not yet a selection rule.

## Null context

CBD nulls:
- 49 draws: 1 / 20 rejected;
- 99 draws: 0 / 20;
- 199 draws: 0 / 20.

ADD null:
- 49 draws: 0 / 10;
- 99 draws: 0 / 10;
- 199 draws: 0 / 10.

The one 49-draw CBD-null rejection occurs at `CBD_NULL_ANCHOR_2`.

With only 10 replicates per null anchor, these counts are descriptive and do not validate exact alpha.

## ADD specificity negative control

Standalone-accuracy departures are exactly ADD-compatible by construction.

ADD rejection under this specificity role is:

- 49 draws: 2 / 120 = 1.67%;
- 99 draws: 4 / 120 = 3.33%;
- 199 draws: 6 / 120 = 5.00%.

These are descriptive specificity outcomes, not an alpha validation study.

## CBD departure detection context

Across all 360 V2 departure datasets:

- 49 draws: 95 / 360 = 26.39%;
- 99 draws: 112 / 360 = 31.11%;
- 199 draws: 111 / 360 = 30.83%.

By axis:

Standalone accuracy:
- 49: 33 / 120;
- 99: 36 / 120;
- 199: 35 / 120.

Complement relation:
- 49: 35 / 120;
- 99: 44 / 120;
- 199: 43 / 120.

Combined violation:
- 49: 27 / 120;
- 99: 32 / 120;
- 199: 33 / 120.

By KL target:

0.001:
- 49: 16 / 120;
- 99: 19 / 120;
- 199: 18 / 120.

0.002:
- 49: 28 / 120;
- 99: 35 / 120;
- 199: 35 / 120.

0.003:
- 49: 51 / 120;
- 99: 58 / 120;
- 199: 58 / 120.

These are characterization rates only.

They do not establish statistical power because the stage uses 10 evaluation replicates per scientific identity and was designed for paired draw stability, not authoritative power estimation.

## ADD departure-diagnostic context

For complement and combined departures, ADD is a diagnostic restriction rather than a specificity negative control.

Rejections are:

- 49 draws: 130 / 240 = 54.17%;
- 99 draws: 139 / 240 = 57.92%;
- 199 draws: 142 / 240 = 59.17%.

No claim is made that larger rejection rate is automatically better.

## 99 vs 199 stratified stability

The 99↔199 comparison remains highly concordant across the principal strata.

By role:
- CBD departure detection: 353 / 360 concordant = 98.06%;
- ADD departure diagnostic: 233 / 240 = 97.08%;
- ADD specificity negative control: 118 / 120 = 98.33%;
- CBD null: 20 / 20 = 100%;
- ADD null: 10 / 10 = 100%.

By axis:
- standalone accuracy: 235 / 240 = 97.92%;
- complement relation: 236 / 240 = 98.33%;
- combined violation: 233 / 240 = 97.08%.

By KL target:
- 0.001: 235 / 240 = 97.92%;
- 0.002: 235 / 240 = 97.92%;
- 0.003: 234 / 240 = 97.50%.

By sign:
- minus: 348 / 360 = 96.67%;
- plus: 356 / 360 = 98.89%.

The exact artifact retains all case-level paired transitions and p-value/critical-value differences.

## Why no draw count is selected here

Issue #206 prospectively froze the experiment but did not freeze a quantitative rule such as:

- minimum acceptable decision concordance;
- maximum acceptable discordance;
- maximum acceptable p-value drift;
- acceptable Monte Carlo decision-instability probability;
- cost-versus-stability loss function.

Choosing such a threshold after observing 97.87% concordance would be post-result rule construction.

Therefore this result may state:

- 99 and 199 were more similar than comparisons involving 49 in this experiment.

It may not state:

- 99 is now authoritative;
- 199 is now authoritative;
- 49 is formally rejected by a predeclared threshold.

A separate prospective decision gate is required.

## Methodological interpretation

Common random numbers are used here to make the alternative draw-count configurations experience common stochastic inputs. This is a standard simulation-comparison technique intended to reduce irrelevant between-configuration noise in differences.

The bootstrap p-values use the plus-one Monte Carlo convention already implemented in the restriction engine.

With no failed refits, nominal minimum p-value increments are approximately:
- 49 draws: 1/50 = 0.02;
- 99 draws: 1/100 = 0.01;
- 199 draws: 1/200 = 0.005.

The finer resolution at larger draw counts is one reason decision differences near alpha = 0.05 can occur even under exact pairing.

## Next gate

The next step must be prospectively specified before any draw count is selected.

Acceptable next forms include:

1. a theory-based draw-count decision rule defined independently of these observed concordance values; or
2. a further paired characterization at larger draw counts, with a prospectively frozen stopping/stability rule.

The project should not select 99 merely because it is cheaper than 199, nor select 199 merely because it is largest.

## Boundary

`KL V2 = DETERMINISTICALLY QUALIFIED`

`PAIRED DRAW-STABILITY CHARACTERIZATION = COMPLETE`

`49 / 99 / 199 = CHARACTERIZED, NOT AUTHORITATIVELY SELECTED`

`STATISTICAL POWER = NOT VALIDATED`

`AUTHORITATIVE BOOTSTRAP DRAW COUNT = NOT FROZEN`

`AUTHORITATIVE EVALUATION COUNT = NOT FROZEN`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`

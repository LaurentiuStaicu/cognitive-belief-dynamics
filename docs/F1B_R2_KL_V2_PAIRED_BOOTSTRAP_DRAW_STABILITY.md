# F1b R2 KL V2 Paired Bootstrap Draw-Stability Characterization

Status: **IMPLEMENTED / PREDECLARED / NOT YET EXECUTED / NON-AUTHORITATIVE**

Issue: #206  
Baseline: `cb86665da328c4ff51415cc6dcffef055577e3bd`

## Purpose

Characterize the effect of bootstrap draw count while holding the synthetic dataset and bootstrap random stream fixed.

The historical 49 / 99 / 199 screen used independent synthetic datasets across draw counts because draw count was part of the dataset RNG key.

That result remains historical evidence for its original stage.

This new stage is a different experiment: a paired draw-stability characterization.

## Qualified scientific design

Use all 36 cases from:

`F1B.R2.KL_CONTROLLED_DEPARTURE.V2`

with:
- KL targets 0.001 / 0.002 / 0.003;
- all three axes;
- both signs;
- both applicable anchors.

Retain three null restriction identities:
- CBD_ANCHOR_1;
- CBD_ANCHOR_2;
- ADD_ANCHOR.

Per evaluation replicate:
- 3 null restriction tests;
- 36 departure datasets × 2 restrictions;
- total 75 restriction-test identities.

## Evaluation replication

Use exactly 10 paired evaluation replicates.

This is a design-search count for draw stability only.

It is not an authoritative power or calibration sample.

Unique datasets:
- 30 null datasets;
- 360 departure datasets;
- total 390.

Restriction runs:
- 750.

Draw-count snapshots:
- 2250.

## Draw-count grid

Freeze:
- 49;
- 99;
- 199.

Minimum successful bootstrap refits:
- 45;
- 90;
- 180.

Alpha:
- 0.05.

These thresholds are retained from the prior R2 bootstrap screen for continuity.

No draw count is authoritative.

## Pairing construction

For each dataset × restriction:

1. generate the synthetic dataset once;
2. fit the observed restriction pair once;
3. compute held-out diagnostics once;
4. initialize one draw-count-independent bootstrap stream;
5. run bootstrap attempts 0…198 once;
6. derive:
   - 49 from attempts 0…48;
   - 99 from attempts 0…98;
   - 199 from attempts 0…198.

Therefore every smaller draw count is an exact prefix of every larger count.

A failed refit at attempt k remains the same failed attempt in every prefix containing k.

## Dataset seed identity

Fresh master seed:

`2026092704`

Dataset seeds depend on:
- master seed;
- a stable SHA-256 scientific identity;
- evaluation replicate.

They do not depend on:
- draw count;
- total evaluation-replicate count;
- execution shard;
- list order.

Python's process-randomized `hash()` is not used.

The 36 V2 cases are sorted only for deterministic output presentation; dataset identity is keyed by case ID, not by list position.

## Shared departure dataset

For each V2 case × replicate:
- one AP-GENERAL dataset is generated;
- the CBD restriction test and ADD restriction test both receive the same dataset object/fingerprint.

This removes data-generation noise from the restriction comparison as well as from the draw-count comparison.

## Dataset fingerprint

Every dataset retains SHA-256 over the canonical byte representation of:

1. share;
2. belief;
3. accuracy cue;
4. reward context;
5. participant ID;
6. item ID.

Integer arrays are normalized to little-endian int64 and continuous arrays to little-endian float64 before hashing.

The fingerprint is an audit identifier, not a random seed.

## Bootstrap stream identity

The common bootstrap seed depends on:
- master seed;
- dataset ID;
- restriction.

It does not depend on draw count.

Inside the existing bootstrap engine, each attempt is already keyed by:
- bootstrap seed;
- restriction index;
- draw index.

Thus the prefix relation is exact.

## Failure semantics

Observed fit failure:
- shared across all three draw counts;
- retained as `fit_failure=true`;
- not recoded as a calibration failure.

Bootstrap refit failure:
- attached to its exact attempt index;
- inherited by every longer prefix containing that attempt.

Calibration failure:
- evaluated separately at 49 / 99 / 199 using 45 / 90 / 180 successful-refit thresholds.

Do not delete failed cases from denominators.

## Paired comparisons

For every dataset × restriction, compare:
- 49 ↔ 99;
- 99 ↔ 199;
- 49 ↔ 199.

Retain:
- decision concordance;
- transition direction;
- absolute p-value difference;
- absolute critical-value difference;
- bootstrap-fit-failure difference;
- successful-draw difference;
- calibration-failure transition.

Aggregate:
- globally;
- by restriction;
- role;
- axis;
- KL target;
- sign;
- anchor.

## Aggregate rejection context

The harness also reports rejection rates and Wilson 95% intervals by draw count, restriction, role, axis and target.

These are descriptive context only.

Ten replicates per cell cannot validate exact alpha or detection power.

## Execution partitioning

Partition only by evaluation replicate:

- R00_01;
- R02_03;
- R04_05;
- R06_07;
- R08_09.

Every shard carries all:
- null identities;
- V2 cases;
- restrictions;
- draw-count prefixes.

Draw-count sharding is forbidden.

The combiner fails closed on:
- replicate overlap;
- incomplete coverage;
- duplicate restriction run;
- unexpected unique-dataset count;
- missing draw snapshot;
- provenance mismatch.

## Why pairing is scientifically preferable here

The scientific contrast is bootstrap draw count.

Using common synthetic datasets and nested bootstrap random streams removes avoidable independent Monte Carlo variation from that contrast.

Common random numbers are a standard simulation comparison technique, but they do not guarantee variance reduction in every system. Therefore the actual paired differences are reported rather than assumed to be small.

## Monte Carlo resolution

With the plus-one p-value convention and no failed refits, nominal p-value resolution is approximately:
- 49 draws → 1/50 = 0.02;
- 99 draws → 1/100 = 0.01;
- 199 draws → 1/200 = 0.005.

This is one reason the three counts are characterized rather than treated as interchangeable.

## Decision boundary

This implementation does not choose a draw count.

After the paired characterization is retained, a separate prospectively documented decision gate may assess whether any count is sufficiently stable for a later non-authoritative stage.

Do not select:
- the cheapest count merely because it is cheap;
- the count with the largest rejection rate;
- a count using unpaired historical rates as though they were paired evidence.

## Boundary

`KL V2 = DETERMINISTICALLY QUALIFIED`

`PAIRED BOOTSTRAP HARNESS = IMPLEMENTED / NOT YET EXECUTED`

`DRAW GRID = 49 / 99 / 199 / DESIGN SEARCH ONLY`

`EVALUATION REPLICATES = 10 / DESIGN SEARCH ONLY`

`AUTHORITATIVE DRAW COUNT = NOT FROZEN`

`AUTHORITATIVE EVALUATION COUNT = NOT FROZEN`

`STATISTICAL POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`

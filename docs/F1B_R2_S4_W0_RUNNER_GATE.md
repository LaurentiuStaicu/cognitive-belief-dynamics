# F1b R2 S4 W0 runner and combine gate

Issue: #259

Status: **W0 EXECUTION HARNESS IMPLEMENTED / NUMERICAL W0 NOT YET RUN**

## Purpose

This gate implements the operational harness that will execute the already frozen W0 scientific matrix after the W0 plan itself is retained.

It does not alter:
- W0 scientific identities;
- the four M2-eligible methods;
- imported M2 evidence;
- the sequential controller;
- the n=10,000 cap;
- numerical lineage;
- the v0.2.0 release boundary.

## Per-shard behavior

Each W0 shard:
- contains only deterministic W0 scientific runs assigned by the retained 250-shard topology;
- keeps all four methods for one scientific run together;
- imports exact retained M2 terminal rows for prefix-bridge-qualified scientific runs;
- executes only non-imported scientific runs with the qualified S4 broad executor;
- regenerates each new scientific dataset once and applies all four methods to the same dataset/missingness mask;
- preserves Haswell numerical lineage;
- preserves the 199-draw prefix and sequential controller;
- stops on first refit failure;
- retains unresolved-at-cap outcomes.

Imported evidence is normalized into the same broad-row schema but retains:

`evidence_origin = RETAINED_M2_IMPORT`

New evidence uses:

`evidence_origin = S4_NEW_EXECUTION`

No imported row is recomputed.

## Shard result contract

A shard result must:
- have one unique scientific-run identity per scientific row;
- have exactly four method rows per scientific run;
- preserve identical dataset SHA-256 across the four methods;
- preserve the expected imported/new origin;
- retain failures and unresolved outcomes;
- refuse duplicate method-row identities;
- refuse non-W0 replicate identities;
- refuse wrong shard assignment.

## Wave combine

The W0 combine requires exactly 250 shard results with indices 0..249.

It validates:
- exact per-shard counts against the retained W0 plan;
- exact 3,750 scientific runs;
- exact 15,000 method rows;
- exact W0 scientific-run digest;
- exact W0 method-row digest;
- exact 3,360 imported method-row digest;
- exact 11,640 new method-row digest;
- exact four-method coverage per scientific run;
- exact paired dataset SHA across methods.

The combined artifact retains all 15,000 rows so per-shard artifacts may later be treated as transient execution evidence after successful wave retention.

The combine reports descriptive status/decision counts and operational terminal-n summaries, but:

`scientific_interpretation_authorized = false`

and:

`method_selected = false`

## Authorization sequence

1. retain fresh-preflight result;
2. retain W0 execution plan;
3. merge this runner/combine gate;
4. run W0 as a temporary execution workflow;
5. retain W0 combined result;
6. only then authorize W1.

## Version boundary

The planned next release remains v0.2.0.

W0 completion alone will not close the release blocker.

The blocker closes only after W0-W3 and final S4 combination are complete, retained and scientifically interpreted.

## Boundary

`W0 RUNNER = IMPLEMENTED`

`W0 COMBINER = IMPLEMENTED`

`W0 NUMERICAL EXECUTION = NOT YET RUN`

`SCIENTIFIC INTERPRETATION = NOT AUTHORIZED`

`METHOD SELECTED = NO`

`POWER = NOT VALIDATED`

`v0.2.0 BLOCKER = OPEN`

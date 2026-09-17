# ADR 0026 — OA-7 DecisionAutopsy and append-only revision trail

Status: Proposed.

## Context

PR #72 added read-only evaluation of persisted ObservedOutcome records against the structured trigger frozen prospectively in an ImplementationPlan. Post-merge CI #274 passed on main.

The final major OA-7 block must support retrospective learning without silently rewriting the original prediction, plan, observation, trigger or prior retrospective analysis.

The Reality Loop contract already reserves a canonical DecisionAutopsy object with:

- case_id;
- implementation_plan_id;
- decision_analysis_id;
- observed_outcome_ids;
- findings;
- revision_proposals;
- prior_prediction_mutated = false;
- optional revision_of_autopsy_id.

## Decision

CEM implements DecisionAutopsy as a human-authored, append-only object persisted in the canonical IndexedDB reality_loop_objects store.

The user must explicitly:

- select one or more persisted ObservedOutcome records;
- write one or more findings;
- declare a revision-proposal target;
- write the rationale;
- write the proposed change;
- declare the proposal status.

The application does not infer or generate findings, rationales, proposed changes, translations or proposal status.

Free text is preserved verbatim in both RO/EN copy fields in this slice, matching the existing manual ObservedOutcome boundary.

## Revision semantics

A revision never edits an existing DecisionAutopsy.

When revision_of_autopsy_id is present, the new DecisionAutopsy must reference an already persisted parent with the same:

- case_id;
- implementation_plan_id;
- decision_analysis_id.

The parent must predate the new record. The prior record remains byte-for-byte unchanged.

This follows the W3C PROV model in which a revision is a kind of derivation and the result of each revision is represented as a new entity rather than a mutation of the old entity.

References:

- https://www.w3.org/TR/prov-dm/#term-revision
- https://www.w3.org/TR/prov-o/#wasRevisionOf
- https://www.w3.org/TR/prov-primer/#section-derivation

CEM remains W3C-PROV-inspired rather than claiming full PROV conformance.

## Observation boundary

Every referenced ObservedOutcome must already be present in the persisted input set and must match the same case, ImplementationPlan and ProspectiveSnapshot.

The DecisionAutopsy creation time must not predate the recording time of any referenced observation.

The observation metadata remains distinct from retrospective findings. OGC OMS continues to provide the conceptual basis for keeping observation acts/results separate from later analysis.

Reference:

- https://www.ogc.org/standards/om/

## Proposal status boundary

RevisionProposal.status may be PROPOSED, ACCEPTED or REJECTED only when explicitly declared by the user.

These statuses are retrospective workflow metadata. They do not automatically:

- change a model assumption;
- mutate DecisionAnalysis;
- modify ImplementationPlan;
- change an Indicator;
- execute THEN / STOP / REASSESS;
- create a new prospective plan;
- recalibrate M0;
- alter evidence state.

A later implementation may turn an accepted proposal into a separately authorized new prospective object, but this ADR does not do so.

## Persistence boundary

The browser controller queries reality_loop_objects by implementation_plan_id and partitions the resulting persisted records into ObservedOutcome and DecisionAutopsy objects.

Before append, it re-reads:

- the referenced persisted ImplementationPlan;
- the persisted observations for that plan;
- the persisted prior autopsies for that plan.

The new DecisionAutopsy is then appended with IndexedDB add(), retaining the existing no-overwrite behavior.

## Scientific boundary

No model equation, coefficient, evidence state, intervention ranking, semantic relation, reference trajectory, calibration state or release version changes.

A DecisionAutopsy is a structured record of human retrospective reasoning. It is not evidence that a causal interpretation, model assumption or policy intervention is correct.

## Regression requirements

- DecisionAutopsy requires at least one persisted ObservedOutcome;
- provenance references must match the frozen plan;
- prior_prediction_mutated is always false;
- future observation records relative to autopsy creation fail closed;
- a revision parent must already exist and have matching provenance;
- revision creates a new id and leaves the parent unchanged;
- browser regression appends an initial autopsy and a child revision from IndexedDB-backed observations;
- browser regression proves both the original autopsy and frozen ImplementationPlan remain byte-for-byte unchanged after the child revision;
- full OA and browser CI remain green.

## OA-7 closure gate

If this PR and post-merge CI are green, OA-7 has a complete minimal Reality Loop:

prospective plan → frozen trigger → persisted observation → read-only trigger evaluation → human DecisionAutopsy → append-only revision trail.

A final OA-7 closure audit may then verify contract/UI/provenance consistency before moving to the next optimization stage.

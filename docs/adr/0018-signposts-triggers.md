# ADR 0018 — OA-7 signposts and trigger drafts

Status: Proposed.

## Context

OA-7 Reality Loop places signposts/triggers after Indicator objects and before adaptive-plan runtime.

DAP/DAPP distinguishes signposts from triggers: signposts identify information or variables to monitor, while triggers are critical signpost levels or events that indicate a contingent response may be needed. The monitoring signal should ideally be available before the decision point.

Sources:

- Walker, Marchau & Kwakkel, Dynamic Adaptive Planning: https://link.springer.com/chapter/10.1007/978-3-030-05252-2_3
- Haasnoot et al., Dynamic adaptive policy pathways: https://doi.org/10.1016/j.gloenvcha.2012.12.006
- Haasnoot, Warren & Kwakkel, Dynamic Adaptive Policy Pathways: https://link.springer.com/chapter/10.1007/978-3-030-05252-2_4

## Decision

Each operational OA-7 Indicator object receives one read-only Signpost definition.

Users may create an ephemeral TriggerDraft with:

- signpost/Indicator reference;
- comparator LT/LTE/GTE/GT;
- threshold in the probability domain [0,1];
- origin = USER_DECLARED.

## Evaluation boundary

A TriggerDraft is never evaluated against the current M0 simulation value.

It is fixed to:

- `NOT_EVALUATED_NO_OBSERVED_OUTCOME`;
- `NOT_BOUND_TO_ADAPTIVE_ACTION`.

This prevents a simulated result from masquerading as monitoring evidence.

## Automation boundary

CEM performs no background monitoring and does not claim that a trigger has occurred.

No external source is polled, no notification is scheduled, and no contingent action is executed in this slice.

## Persistence boundary

Trigger drafts are ephemeral to the current rendered planner view and are not written to Workspace v1.

Changing/rebuilding the inspected plan surface may discard them. Durable adaptive plans require a later explicit storage migration.

## Scientific boundary

No trigger threshold is inferred from the model or evidence base. Thresholds are user declarations only.

No model equation, coefficient, intervention score, bundle ranking, evidence status, reference run or release metadata changes.

## Next slice

After this PR and post-merge CI are green, the roadmap permits the separate adaptive-plan slice using NOW/WATCH/IF/THEN/STOP/REASSESS. Only that later slice may bind trigger conditions to contingent actions.

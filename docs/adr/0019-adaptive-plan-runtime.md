# ADR 0019 — OA-7 adaptive plan draft runtime

Status: Proposed.

## Context

OA-7 Reality Loop orders the adaptive-plan runtime after signposts/triggers and before ObservedOutcome and Decision Autopsy.

Dynamic Adaptive Planning separates plan design from implementation. The design phase defines the initial plan, monitoring program, triggers and contingent actions; contingent actions are only taken during implementation if monitoring later confirms a trigger. DAPP similarly specifies immediate actions, developments to monitor, trigger conditions and later actions while keeping reassessment available when assumptions or objectives cease to hold.

Sources:

- Walker, Marchau & Kwakkel, Dynamic Adaptive Planning: https://link.springer.com/chapter/10.1007/978-3-030-05252-2_3
- Haasnoot, Warren & Kwakkel, Dynamic Adaptive Policy Pathways: https://link.springer.com/chapter/10.1007/978-3-030-05252-2_4
- Haasnoot et al., Dynamic adaptive policy pathways: https://doi.org/10.1016/j.gloenvcha.2012.12.006

## Decision

The runtime introduces an ephemeral `AdaptivePlanDraft` using exactly:

- NOW
- WATCH
- IF
- THEN
- STOP
- REASSESS

NOW is derived from the inspected bundle. WATCH is derived from the selected Signpost. IF is derived from the user-declared TriggerDraft. THEN, STOP and REASSESS are user-authored prospective actions.

## Readiness

Each step has explicit readiness:

- `DEFINED`
- `MISSING_TRIGGER`
- `MISSING_ACTION`

The runtime fails incomplete rather than inventing missing trigger conditions or actions.

## Execution boundary

The entire plan is fixed to:

- `DESIGN_ONLY_NO_OBSERVED_OUTCOME`;
- `NO_AUTOMATIC_ACTIONS`;
- `EPHEMERAL_NOT_WORKSPACE`.

No step is executed. The runtime does not infer that a trigger occurred from the M0 simulation result, does not stop an intervention, does not switch bundles, and does not create a revision automatically.

Only a later ObservedOutcome slice may supply retrospective observation records that can be compared with a trigger condition. Even then, automatic action execution is not implied.

## Persistence boundary

The adaptive plan remains ephemeral in this slice. A durable `ImplementationPlan` requires the explicit Workspace/storage migration reserved by the OA-7 contract.

## Scientific boundary

No adaptive action is inferred from the scientific model or evidence base. THEN, STOP and REASSESS text is user-declared planning content.

No model equation, coefficient, intervention score, bundle ranking, evidence status, reference run or release metadata changes.

## Regression requirements

- exactly six canonical phases in order;
- WATCH binds only to an operational Indicator;
- IF binds only to a TriggerDraft;
- missing trigger/actions remain explicit;
- completed actions remain design-only;
- no `executed` state or ObservedOutcome ID appears;
- browser and existing accessibility/reflow gates remain green.

## Next roadmap item

After this PR and green post-merge CI, the next OA-7 item is ObservedOutcome runtime in a separate PR. Decision Autopsy remains later.
# ADR 0014 — OA-6D Information Priority and Adaptive Reassessment

Status: Proposed for OA-6D integration.

## Context

R7 authorizes an information-priority layer and adaptive reassessment after OA-6A/B/C, while explicitly deferring numeric EVPI/EVSI until defensible probability distributions and a declared utility/value model exist.

Dynamic Adaptive Planning and Dynamic Adaptive Policy Pathways distinguish monitoring signposts from trigger conditions and contingency actions. A plan can specify what to monitor, the condition that should provoke reassessment, and the action to reconsider without claiming that the trigger will occur or that the system predicts its timing.

Relevant research:

- Haasnoot M, Kwakkel JH, Walker WE, ter Maat J. Dynamic adaptive policy pathways. Global Environmental Change. 2013. https://doi.org/10.1016/j.gloenvcha.2012.12.006
- Walker WE, Marchau VAWJ, Kwakkel JH. Dynamic Adaptive Planning. In: Decision Making under Deep Uncertainty. 2019. https://link.springer.com/chapter/10.1007/978-3-030-05252-2_3
- Haasnoot M et al. Designing a monitoring system to detect signals to adapt to uncertain climate change. Global Environmental Change. https://www.sciencedirect.com/science/article/pii/S095937801830445X
- NICE research recommendations process: modelling sensitivity to parameter or structural assumptions can help identify important uncertainties, while value-of-information analysis is optional rather than mandatory. https://www.nice.org.uk/process/pmg45/chapter/nice-research-recommendations-process

## Decision 1 — qualitative information triage

OA-6D does not compute a numeric value of information.

The uncertainty registry is triaged into four descriptive classes:

- `DECISION_SENSITIVE_NOW` — a direct top-choice switch is observed across the currently declared finite response scenarios;
- `CLARIFY_USER_ASSUMPTION` — the object is user-controlled and should be clarified as a preference/cost/timing assumption before being treated as scientific uncertainty;
- `RESEARCH_OR_MONITOR` — the uncertainty is at least partly reducible, but no direct current scenario switch is observed;
- `CONTEXT_LIMITATION` — the issue is structural/model-scope and may require model extension rather than additional data alone.

The engine emits `QUALITATIVE_TRIAGE_NO_NUMERIC_VOI`. It has no information-value score, probability, expected utility, expected regret, EVPI or EVSI.

A displayed order is UI grouping only, never a cardinal or evidential ranking.

## Decision 2 — decision sensitivity

For the first executable OA-6D scope, direct decision sensitivity is supported only where OA-6B already provides a valid finite-scenario comparison: `UNC.PLANNER.RESPONSE.PROFILES`.

If the current selected bundle is not top-ranked in every feasible declared response scenario, or OA-6B records a top-set switch relative to the selected reference profile, the response-profile uncertainty is marked `DECISION_SENSITIVE_NOW`.

Other registry objects remain explicitly classified by role and reducibility. OA-6D does not invent sensitivity experiments for continuous user weights, user costs or structural omissions merely to obtain a ranking.

## Decision 3 — signpost and trigger recording

OA-6D adds a versioned, bounded local store for prospective reassessment rules.

Each record contains:

- associated canonical OA-6A uncertainty ID;
- signpost type: metric, event, evidence update, scheduled review, or other;
- indicator/signpost description;
- trigger condition;
- action to reconsider;
- basis: user-defined, empirical, conceptual, or executable;
- optional rationale and source/provenance note;
- optional earliest/latest reassessment points;
- creation timestamp.

The store is:

- local-only;
- schema-versioned;
- bounded to 50 records;
- fail-closed on corrupt or future-version documents;
- user-clearable and individually removable.

It remains outside Workspace/Case provenance and outside scientific model artifacts.

## Automation boundary

OA-6D records prospective reassessment logic only.

CEM does not:

- monitor external sources in the background;
- decide autonomously that a signpost has crossed a trigger;
- predict when the trigger will occur;
- execute or change an intervention plan automatically;
- schedule notifications or external actions from these local records.

A saved trigger is therefore a user-authored conditional instruction for future review, not an automated monitor.

## Monitoring quality boundary

The UI prompts the user to make the signpost and trigger explicit, but OA-6D does not certify monitoring quality. The DAPP monitoring literature emphasizes measurability, timeliness, reliability, convincibility and institutional connectivity; future extensions may encode these as audit fields after a separate contract.

## Scientific-output boundary

OA-6D changes no file under `model/`, no equation, coefficient, intervention artifact, reference run, evidence status, semantic identity/status or release metadata.

Information-priority results are decision-audit metadata over existing OA-6A/B objects. Reassessment records are local user data.

## Accessibility and privacy

The UI uses native forms, labels, select controls, inputs, textarea and buttons. Priority class is always written as text rather than color alone.

Recorded values are HTML-escaped before rendering. Records remain in browser local storage until individually removed or cleared.

## Regression gate

OA-6D must prove:

1. canonical budget=2 / weight=50% / step=2 response-profile switch produces `DECISION_SENSITIVE_NOW`;
2. the default robust 3/3 case does not become a numeric VOI ranking;
3. user-controlled objective/cost/timing assumptions remain `CLARIFY_USER_ASSUMPTION`;
4. structural scope remains `CONTEXT_LIMITATION`;
5. corrupt/future local documents fail closed;
6. local records can be added, removed and cleared;
7. browser interaction preserves planner state and mobile/reflow behavior;
8. full existing scientific-output reproduction remains unchanged.

## Next slice

After OA-6D integration and green post-merge CI, OA-6E may perform the final Decision Under Uncertainty closure audit. Numeric VOI remains out of scope unless a future contract introduces valid probabilities and a utility/value model.

# CEM Quality Matrix — OA-0

Status: cross-cutting quality gate definition. A green CI run is necessary but not by itself sufficient for major OA integration.

| Axis | Required question | Minimum evidence before merge |
| --- | --- | --- |
| Scientific integrity | Did the change preserve or explicitly gate scientific meaning? | canonical fixtures/invariants; review of claim boundaries |
| Epistemic integrity | Is status/scope/uncertainty explicit and non-strengthened? | schema/status tests; UI wording audit |
| Cognitive usability | Can the intended user understand what to do and what the result means? | task-based browser test; later usability evidence for major IA changes |
| Decision integrity | Are objectives, assumptions, trade-offs and uncertainty visible? | decision audit fixture; no unconditional recommendation language |
| Real-world boundary | Is simulation distinct from implementation and observation? | schema separation + UI labels |
| Visual hierarchy | Is the primary content/action recognizable without excessive chrome? | screenshot audit against Visual Language |
| Accessibility | Keyboard, scaling, semantics, contrast and non-drag alternatives? | automated checks + manual gate for major surfaces |
| Internationalization | RO/EN behavior and terminology remain equivalent? | bilingual browser tests |
| Provenance | Can an analytical result be traced to inputs/model/version? | provenance fixture/export test |
| Reproducibility | Can the result/state be regenerated or round-tripped? | deterministic fixture, checksum or round-trip test |
| Persistence | Can saved user work survive restart/version change? | migration/recovery tests when persistence exists |
| Security | Are untrusted inputs and dependencies handled safely? | schema validation, code/dependency scanning as applicable |
| Privacy | Is personal work local/minimized by default? | no mandatory remote transmission; documented storage |
| Maintainability | Does the change avoid duplicate scientific logic? | architecture review; source-of-truth test |
| Performance | Did startup/interaction cost remain acceptable? | budget/benchmark once established |
| Portability | Can work move across supported CEM versions/platforms? | portable schema/export + parity tests |
| Platform fidelity | Does native implementation use platform patterns? | elementary HIG/portal review when applicable |

## Major-release acceptance

Before an OA milestone is declared complete:

1. all applicable matrix axes are reviewed;
2. any `N/A` entry includes a reason;
3. unresolved failures are explicit blockers or documented deferrals;
4. scientific and product maturity are reported separately.

## Software maturity versus scientific maturity

CEM must not collapse these into one badge.

Software maturity examples:

- PROTOTYPE
- TESTED
- STABLE

Scientific maturity examples:

- CONCEPTUAL
- CANDIDATE
- UNCALIBRATED
- CALIBRATED_WITHIN_SCOPE
- VALIDATED_WITHIN_SCOPE

A stable UI may present an uncalibrated scientific object, provided the status remains explicit.

## Accessibility target

Web target: WCAG 2.2 AA.

At minimum, major surfaces require:

- keyboard-only completion;
- visible/unobscured focus;
- pointer targets meeting or safely satisfying WCAG 2.2 minimum target-size rules;
- single-pointer alternative for non-essential dragging;
- 200% text without horizontal application overflow except intentionally scrollable scientific plots/tables;
- light/dark review;
- no color-only scientific meaning;
- chart/table or textual alternatives;
- reduced-motion respect where motion exists.

Native targets will be re-audited with current GTK/Granite accessibility guidance in OA-9.

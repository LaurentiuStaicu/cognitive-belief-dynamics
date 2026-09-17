# OA-8 Keyboard + Assistive Technology Manual Audit

Status: DEFERRED_POST_V1

Target: Cognitive Epistemic Model web application, WCAG 2.2 AA trust-hardening track.

## Project scheduling decision

The detailed manual keyboard + assistive-technology execution is intentionally deferred until after v1 (or immediately before any release claim that depends on manual AT evidence), so module development can proceed without repeatedly re-auditing a rapidly changing interface.

This status is **not a PASS** and must not be used as evidence of complete WCAG 2.2 AA conformance. Automated accessibility, keyboard, reflow and semantic regression gates remain active during pre-v1 development. The task matrix below is preserved as the required execution protocol when the deferred audit resumes.

This record is intentionally not a conformance statement. Automated browser checks are prerequisites only. W3C guidance states that no evaluation tool alone can determine accessibility and that knowledgeable human evaluation is required. WAI-ARIA APG also recommends testing relevant browser + assistive-technology combinations because interoperability varies.

Authoritative references:

- https://www.w3.org/WAI/test-evaluate/
- https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/
- https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
- https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/

## 1. Preconditions

Before manual execution, all of these must be green on the exact audited commit:

- Verify model and web;
- `npm run test:a11y`;
- CodeQL Python;
- CodeQL JavaScript/TypeScript.

Record the exact commit SHA and do not mix results across commits.

## 2. Required environment record

For every execution record:

- audit date/time;
- commit SHA;
- operating system and version;
- browser name and version;
- screen reader / assistive technology name and version;
- language tested (`ro`, `en`);
- display scaling / zoom;
- evaluator;
- deviations from default AT/browser configuration.

## 3. Keyboard-only audit

Run without mouse/pointer interaction after page load.

For every primary surface (Understand, Analyze, Act, Library) and each exposed secondary view:

1. Reach every operable control using `Tab` / `Shift+Tab`.
2. Confirm the focus order follows the visual/logical reading order.
3. Confirm focus is always visible and not hidden by sticky/overlay content.
4. Confirm `Enter` / `Space` activate buttons and disclosure-like controls as expected.
5. Confirm native form controls remain operable with expected arrow-key behavior.
6. Confirm no keyboard trap exists; focus can leave every component.
7. Confirm opening Search, Inspector, Theory links, planning controls and revision/autopsy controls moves focus predictably.
8. Confirm closing/dismissing any transient surface returns focus to a logical initiating control when applicable.
9. Confirm no functionality requires pointer dragging only.
10. Repeat critical flows in both Romanian and English.

Record each surface as PASS / FAIL / NOT_APPLICABLE with notes and reproduction steps for every FAIL.

## 4. Screen-reader / AT audit matrix

Primary Linux matrix for the project's current desktop development environment:

| Combination | Status | Notes |
| --- | --- | --- |
| Orca + Firefox | DEFERRED_POST_V1 | Primary semantic/navigation audit not completed |
| Orca + Chromium | DEFERRED_POST_V1 | Cross-browser AT spot-check not completed |

If another platform becomes a supported target before v1, add at least one relevant browser + AT combination for that platform rather than assuming Linux results generalize.

## 5. Screen-reader tasks

For each AT/browser combination:

1. Verify application title, document language and major landmarks are announced meaningfully.
2. Navigate headings and landmarks without using visual orientation.
3. Verify Search input, result count, result links and Universal Inspector expose useful names/roles/states.
4. Verify pressed/selected/current states of primary and secondary navigation are conveyed.
5. Verify Theory Reader heading hierarchy and status text are understandable in reading order.
6. Verify tables expose headers and cell relationships where tables are present.
7. Verify form labels, required fields, errors and status messages are announced.
8. Verify dynamic transitions in Active Understanding do not silently change content without a usable focus/announcement path.
9. Verify planning / ObservedOutcome / DecisionAutopsy controls expose identity, state and validation messages without requiring visual color cues.
10. Verify graphs/visualizations have a usable non-visual alternative or clearly documented textual/tabular equivalent.
11. Verify language switching updates pronunciation/language metadata appropriately where supported.
12. Verify there are no misleading ARIA roles/states that contradict native semantics.

Do not require exact spoken wording: equivalent information conveyed by different screen readers may differ.

## 6. Result classification

Use only:

- `PASS` — manually verified for the recorded environment and task;
- `FAIL` — reproducible barrier found;
- `NOT_APPLICABLE` — criterion/task does not apply, with reason;
- `NOT_TESTED` — not executed.

When the deferred audit resumes, document-level status must change from `DEFERRED_POST_V1` to `PENDING_MANUAL_EXECUTION` until every required task in the primary matrix has an explicit result.

## 7. Finding format

For each failure record:

- finding ID (`OA8-AT-###`);
- surface/view;
- environment;
- user action sequence;
- expected accessible behavior;
- observed behavior;
- affected WCAG 2.2 criterion(s), if known;
- severity as blocker / major / minor for release triage only;
- screenshot/transcript/log reference when useful;
- remediation commit/PR once fixed;
- retest result.

## 8. Closure rule for the deferred audit

This manual audit is complete only when:

- keyboard-only manual traversal is recorded for all exposed surfaces;
- the primary AT matrix is executed;
- all blocker/major findings are fixed or explicitly accepted with documented rationale;
- fixes are retested on the exact post-fix commit;
- the final record states the evaluated scope and environments.

Passing this audit still describes only the tested scope/environments; it does not imply universal assistive-technology interoperability.

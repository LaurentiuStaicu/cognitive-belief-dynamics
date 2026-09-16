# OA-6E — Decision Under Uncertainty Closure Audit

Status: **CANDIDATE FOR CLOSURE**

Date: 2026-09-16

R7 baseline: `e62324dcd4551dafe423387b6e8217e1eac021e6`

OA-6D integrated baseline for this audit: `cf9c711cb284159d2af890ca7689ee41fdb8f4ba`

## 1. Scope

OA-6E is the closure audit defined by R7. It introduces no new uncertainty method, model equation, intervention effect, probability model, utility model, scientific relation or decision rule.

The audit verifies the complete OA-6 chain:

- OA-6A — uncertainty contract and registry;
- OA-6B — deterministic robustness and regret;
- OA-6C — Decision Under Uncertainty UI;
- OA-6D — qualitative information priority and adaptive reassessment.

## 2. Scientific-output invariant

The following artifacts have identical Git blob hashes at the R7 baseline and after OA-6D:

| Artifact | Git blob SHA |
| --- | --- |
| `web/public/model/interventions.json` | `90092a231d6fe6bb341efd02d381473af2ecd235` |
| `web/public/model/runs.json` | `4fbd9656f4c006644e151c31e47fc78683b99f90` |
| `web/public/model/explanations.json` | `1ae3bc4b580f39160f7574c5626f63bffdd59322` |
| `model/variables.json` | `0aa7f4482634f2f8f733ca42d996d2d6fda39ae4` |
| `model/links.json` | `d81ba2c8c07a3ad5165feaa7be55397b74a366ed` |

OA-6 added the uncertainty contract/schema and decision-audit code, but did not change the baseline intervention table, reference runs, explanations, canonical variables or canonical links.

The closure test recomputes Git blob hashes in CI so this invariant cannot silently drift during OA-6E.

## 3. Probability and value boundary

The executable OA-6 system retains the R7 boundary:

- low/reference/high remain finite declared sensitivity scenarios;
- scenario frequency is a count/denominator, not a probability;
- no probability weights are inferred;
- no probability-of-best output exists;
- no confidence interval is inferred from scenario spread;
- no expected outcome is calculated from unweighted profiles;
- no EVPI or EVSI calculation exists;
- qualitative information priority is explicitly `QUALITATIVE_TRIAGE_NO_NUMERIC_VOI`;
- numeric VOI remains deferred until a future scientific contract supplies defensible probabilities and a declared utility/value model.

The closure test scans executable OA-6 surfaces for prohibited positive formulations and separately requires the explicit RO/EN boundary language.

## 4. Terminology separation

Three concepts remain separate:

1. **Scientific/evidential uncertainty** — represented in the OA-6A registry.
2. **Decision robustness / decision sensitivity** — represented by OA-6B/C/D.
3. **Learner confidence** — represented only in OA-5 Active Understanding.

OA-6 does not reuse learner-confidence state as scientific confidence or decision probability.

## 5. Bilingual semantic parity

The registry requires non-empty Romanian and English labels and limitations for every uncertainty object and for every finite-scenario label.

The browser closure gate switches the complete Decision Under Uncertainty surface between RO and EN and verifies that semantic structure counts remain unchanged:

- uncertainty ledger entries;
- information-priority entries;
- scenario rows;
- robustness alternatives;
- adaptive reassessment form.

Translation may differ linguistically, but the decision objects, IDs, counts and boundaries must be the same.

## 6. Accessibility, keyboard and reflow

OA-6E extends the browser gate to verify:

- a native information-priority button is operable with keyboard Enter;
- keyboard activation moves focus to the associated reassessment indicator;
- the complete planning / Decision Under Uncertainty view remains one-dimensional at 320 CSS px;
- the same planning view remains within the viewport at 200% root text size;
- semantic information is expressed through text, tables and labels rather than color alone.

This closes the explicit R7 requirement for keyboard operation and 320 CSS px / 200% text reflow.

## 7. Adaptive-planning boundary

Dynamic adaptive planning literature treats monitoring/signposts and trigger rules as a way to adapt plans as uncertainty resolves, rather than as a claim that the future is predicted. OA-6D follows the bounded version of that architecture: it records a user-authored signpost, trigger condition and action to reconsider, but performs no background monitoring and no automatic execution.

Background:
- Kwakkel, Haasnoot & Walker, *Developing dynamic adaptive policy pathways*, Climatic Change (2015): https://link.springer.com/article/10.1007/s10584-014-1210-4
- Marchau et al., *Decision Making under Deep Uncertainty: From Theory to Practice*: https://link.springer.com/book/10.1007/978-3-030-05252-2

## 8. Closure criteria

OA-6 may close only when all of the following are green on the PR and again after merge:

- Python scientific tests;
- installed-resource validation;
- published-reference reproduction;
- all web unit/contract suites including `test:oa6e`;
- TypeScript strict build and Vite build;
- Playwright browser regression;
- scientific artifact hash invariant;
- RO/EN semantic parity;
- 320 CSS px and 200% planning reflow;
- keyboard activation;
- no prohibited probability/expected-value language in executable OA-6 surfaces.

## 9. Residual limitations

OA-6 remains a decision-support layer over an illustrative, uncalibrated planner. It does not establish that the displayed intervention bundle is an optimal real-world policy or that OA-6 improves human decision quality.

Human evaluation remains necessary before making claims about decision-support effectiveness.

## 10. Exit gate

If the OA-6E PR and post-merge CI are both fully green, **OA-6 / Decision Under Uncertainty is formally closed**.

No OA-7 implementation should begin before that post-merge gate.

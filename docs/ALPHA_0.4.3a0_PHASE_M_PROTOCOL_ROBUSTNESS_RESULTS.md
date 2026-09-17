# Alpha 0.4.3a0 Phase M — authoritative protocol robustness result and M1 closeout

Status: **authoritative Phase M result integrated; `PROTOCOL_ROBUSTNESS_FAIL`; M1 closed at the pre-human software/research boundary.**

This document records the prospectively frozen Phase M synthetic robustness result. The failure is preserved as observed. No failed profile was deleted, no threshold was changed, and no model was tuned after seeing this result.

## 1. Provenance

The Phase M contract and tooling were merged to `main` at:

`2be27f09d054448abb9005ccf29c0017990a4ccc`.

The one-shot authoritative execution harness was then merged to `main` at:

`af338ed1fe94cc8d59578e50471eb1ccc5886df2`.

GitHub Actions authoritative run:

`35229760477`.

Workflow:

`M1 Phase M authoritative protocol robustness`.

The run completed successfully as software execution on 2026-09-17 and produced the complete frozen matrix:

- 9 prospectively specified nuisance profiles;
- 2 generator families per profile;
- 18 cells total;
- 200 independent replicates per cell;
- 3,600 recovery replicates total.

Persistent result files:

- `model/benchmarks/results/m1_e4_protocol_robustness_authoritative_2026-09-17.json`;
- `model/benchmarks/results/m1_e4_protocol_robustness_authoritative_2026-09-17.provenance.json`;
- `model/benchmarks/results/m1_e4_protocol_robustness_authoritative_2026-09-17.sha256`;
- `model/benchmarks/results/m1_e4_protocol_robustness_authoritative_2026-09-17.shards.sha256`.

Authoritative source aggregate JSON SHA-256:

`479767bc8f75a689060529c803d7796b2588340f7690915dd9fd481b2e6b9f80`.

The aggregate workflow artifact digest is:

`sha256:6acac279de1a289541de77bbb64c19bca9d58761ecc9c8a368d3b164ed0f1ada`.

## 2. Frozen gate

The formal rule was preregistered before authoritative execution:

`recovery_probability >= 0.80`

for **all 18 cells**.

The Wilson 95% lower-bound condition `>= 0.80` was preregistered as a secondary Monte Carlo-precision sensitivity only. It does not replace the formal point-estimate gate.

## 3. Authoritative result

Verdict:

`PROTOCOL_ROBUSTNESS_FAIL`.

Three of the 18 prospectively frozen cells fail the formal recovery gate:

- `ITEM_MODERATE__EVSD`: recovery `0.780`, Wilson 95% lower bound `0.718`;
- `ITEM_HIGH__EVSD`: recovery `0.560`, Wilson 95% lower bound `0.491`;
- `COMBINED_ADVERSE__EVSD`: recovery `0.585`, Wilson 95% lower bound `0.516`.

The minimum recovery probability across the full matrix is `0.560`. The minimum Wilson lower bound is `0.4907167533`.

Across all 3,600 replicates:

- correct-family selections: 3,169;
- wrong-family selections: 25;
- inconclusive selections: 406.

All three formal failures are also failures of the preregistered secondary Wilson sensitivity.

## 4. Complete 18-cell matrix

| Profile | Truth | Correct | Recovery | Wilson 95% | Wrong family | Inconclusive | Formal gate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `COMBINED_ADVERSE` | EVSD | 117/200 | 0.585 | 0.516–0.651 | 6 | 77 | FAIL |
| `COMBINED_ADVERSE` | 2HT | 177/200 | 0.885 | 0.833–0.922 | 0 | 23 | PASS |
| `ITEM_HIGH` | EVSD | 112/200 | 0.560 | 0.491–0.627 | 13 | 75 | FAIL |
| `ITEM_HIGH` | 2HT | 173/200 | 0.865 | 0.811–0.905 | 0 | 27 | PASS |
| `ITEM_MODERATE` | EVSD | 156/200 | 0.780 | 0.718–0.831 | 3 | 41 | FAIL |
| `ITEM_MODERATE` | 2HT | 190/200 | 0.950 | 0.910–0.973 | 0 | 10 | PASS |
| `LATENT_ASSOCIATED_ATTRITION` | EVSD | 180/200 | 0.900 | 0.851–0.934 | 1 | 19 | PASS |
| `LATENT_ASSOCIATED_ATTRITION` | 2HT | 190/200 | 0.950 | 0.910–0.973 | 0 | 10 | PASS |
| `MAR_LIKE_ATTRITION` | EVSD | 179/200 | 0.895 | 0.845–0.930 | 1 | 20 | PASS |
| `MAR_LIKE_ATTRITION` | 2HT | 189/200 | 0.945 | 0.904–0.970 | 0 | 11 | PASS |
| `REFERENCE` | EVSD | 187/200 | 0.935 | 0.892–0.962 | 0 | 13 | PASS |
| `REFERENCE` | 2HT | 194/200 | 0.970 | 0.936–0.986 | 0 | 6 | PASS |
| `RHO_NEGATIVE` | EVSD | 178/200 | 0.890 | 0.839–0.926 | 1 | 21 | PASS |
| `RHO_NEGATIVE` | 2HT | 197/200 | 0.985 | 0.957–0.995 | 0 | 3 | PASS |
| `RHO_POSITIVE` | EVSD | 191/200 | 0.955 | 0.917–0.976 | 0 | 9 | PASS |
| `RHO_POSITIVE` | 2HT | 191/200 | 0.955 | 0.917–0.976 | 0 | 9 | PASS |
| `SERIAL_DEGRADATION` | EVSD | 179/200 | 0.895 | 0.845–0.930 | 0 | 21 | PASS |
| `SERIAL_DEGRADATION` | 2HT | 189/200 | 0.945 | 0.904–0.970 | 0 | 11 | PASS |

## 5. Descriptive pattern

The three formal failures occur under EVSD truth when crossed item heterogeneity is introduced: moderate item heterogeneity, high item heterogeneity, and the combined adverse profile containing high item heterogeneity together with correlated participant effects, serial degradation, and latent-associated attrition.

This asymmetry is reported descriptively. It does **not** establish that 2HT is the human recognition architecture, that EVSD is false in humans, or that the true human process belongs to either candidate family. Phase M is a synthetic robustness-to-misspecification experiment, not human model selection.

## 6. Scientific interpretation

The authoritative result supports one narrow conclusion:

> Under the prospectively frozen Phase M synthetic stress surface, the current P64_X10 participant-aware EVSD-vs-2HT discrimination pipeline does not maintain the preregistered 0.80 correct-family recovery threshold in every cell when the fitted candidates omit the added nuisance structures.

The result therefore shows that the current prospective human-discrimination design is **not recruitment-ready at the tested allocation and analysis specification**.

It does not:

- identify a human cognitive architecture;
- identify or activate `Pencode`;
- validate 64 participants as a human sample size;
- authorize recruitment or imply ethics/IRB approval;
- modify M0 or M1.E1–M1.E3;
- justify post-hoc tuning of the frozen Phase M gate.

## 7. M1 closeout

The prospectively specified Phase M contract explicitly allowed M1 to close at the pre-human boundary after either PASS or FAIL, provided the authoritative result was preserved.

M1 is therefore closed at that boundary with the following state:

- M1.E1, M1.E2 and M1.E3 remain the active executable M1 surface;
- M1.E4 remains a documented pre-human research program and is not activated in runtime;
- `Pencode` remains blocked / not identified;
- EVSD and 2HT remain unresolved candidate families;
- human recruitment remains outside the current CEM development track;
- the failed Phase M result is retained as a constraint on any future external validation program.

Any future human-validation redesign must be a separate prospective program. It must not rewrite this result retrospectively.

## 8. Development transition

With M1 closed at the scientifically justified pre-human boundary, application development may proceed without waiting for human calibration. The next product work is the already authorized interface simplification and suite-level uniformization. This transition changes presentation and interaction architecture, not the frozen scientific meaning of M1.

No software version bump or evidence-snapshot change is part of this Phase M result integration.

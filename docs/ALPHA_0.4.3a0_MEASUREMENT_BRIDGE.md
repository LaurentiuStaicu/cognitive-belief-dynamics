# Alpha 0.4.3a0 Phase B — M1.E4 SDT measurement bridge

Status: measurement-contract only. No executable recognition/encoding mechanism, active M1.E4 registry promotion or UI is introduced by this phase.

## 1. Question

Phase A selected `Drecog` — signal-detection recognition sensitivity — as the direct empirical validation construct for the planned M1.E4 Headline Recognition Gate.

Phase B asks a narrower question:

> What does `Drecog` measure, how should CEM compute it reproducibly, and what can it legitimately constrain about any future executable encoding state?

The answer is deliberately conservative:

**`Drecog` identifies recognition discriminability under an explicit SDT measurement convention. It does not identify an item-level encoding probability.**

## 2. Source task and terminology

Shulman, Markowitz & Rogers (2024), Study 3, used a 24-item recognition task minutes after headline exposure. Participants saw a three-word phrase and reported whether it had appeared in the previously viewed headlines.

The paper reports higher sensitivity for the simpler-headline condition:

- simple: `d′ = 1.23`, SD = 0.81;
- complex: `d′ = 0.80`, SD = 0.77;
- `t(483)=6.01`, `p<0.001`, Cohen's `d=0.55`.

The source prose uses “hit” unusually broadly when describing correct responses. CEM must not copy that wording into its measurement ontology. For reproducibility, CEM uses the standard yes/no SDT contingency definitions:

| Probe truth | Response “seen” | Response “not seen” |
| --- | --- | --- |
| target / previously presented | hit | miss |
| foil / not previously presented | false alarm | correct rejection |

This terminology follows standard SDT usage.

## 3. Raw measurement quantities

A future M1.E4 recognition task must retain the four raw cell counts before any summary measure is calculated:

- `Nhit`;
- `Nmiss`;
- `Nfa`;
- `Ncr`.

From them:

`H = Nhit / (Nhit + Nmiss)`

`F = Nfa / (Nfa + Ncr)`

CEM must never store only `Drecog` if raw recognition outcomes are available.

The source paper states that Study 3 used 24 probes, but Phase B does **not** infer an unreported target/foil split. Future synthetic tasks must register `Ntarget` and `Nfoil` explicitly.

## 4. Reference d-prime measurement convention

For a yes/no equal-variance Gaussian SDT reference model:

`Drecog = Phi^-1(H*) - Phi^-1(F*)`

where `Phi^-1` is the standard-normal inverse CDF.

Because raw rates of exactly 0 or 1 produce infinite z values, CEM selects the Hautus log-linear correction as its open reference convention:

`H* = (Nhit + 0.5) / (Nhit + Nmiss + 1)`

`F* = (Nfa + 0.5) / (Nfa + Ncr + 1)`

The correction is applied consistently, not only when a rate happens to be extreme.

This is a **CEM measurement convention**, selected for reproducibility and finite estimates. It is not a claim that the Shulman authors used the same correction. Exact source-code reproduction must be verified separately before CEM may claim numerical identity with the published participant-level d-prime computation.

## 5. Response criterion must remain separate

The same corrected rates also permit an auxiliary criterion diagnostic:

`Crecog = -0.5 × [Phi^-1(H*) + Phi^-1(F*)]`

`Crecog` is not an M1.E4 model state. It is a measurement diagnostic used to prevent a liberal/conservative “seen” response tendency from being mistaken for recognition sensitivity.

Therefore:

`Drecog != Crecog`.

A future model-discrimination test should reject candidate explanations that reproduce a condition difference only by shifting response criterion while leaving recognition discriminability unchanged.

## 6. Identifiability result

A single `Drecog` value does not uniquely determine hit rate and false-alarm rate.

Under the equal-variance reference model, if `Crecog` is also known, the pair becomes invertible:

`z(H*) = Drecog/2 - Crecog`

`z(F*) = -Drecog/2 - Crecog`.

But even the pair `(Drecog, Crecog)` does **not** uniquely identify an encoding mechanism.

It describes recognition-performance geometry, not how an individual headline was encoded.

## 7. Why Pencode remains blocked

An item-level `Pencode` would imply a generative claim such as:

> each exposure produces an encoded/not-encoded event with some probability.

The current evidence does not identify that probability.

Many distinct latent mechanisms can produce the same hit/false-alarm pattern:

- continuous memory-strength differences;
- mixtures of successfully and unsuccessfully encoded items;
- recollection/familiarity combinations;
- attention failures;
- unequal target/foil evidence variances;
- different response-criterion structures.

Recognition-memory research explicitly treats these as competing psychological interpretations rather than consequences that follow uniquely from a single d-prime score.

Therefore Phase B assigns:

`Pencode.status = NOT_IDENTIFIED_BY_CURRENT_MEASUREMENT`.

No default conversion such as logistic(`Drecog`), normal-CDF(`Drecog`) or `Drecog / constant` is scientifically permitted.

## 8. SDT-native bridge quantity

Phase B permits one conceptual bridge quantity:

### Msep — standardized recognition-evidence separation

Under the **reference equal-variance SDT measurement model only**:

`Msep = (mu_target - mu_foil) / sigma`

and numerically:

`Msep = Drecog`.

This equality is a definition inside the reference measurement model, not an empirical discovery about encoding.

`Msep` is:

- dimensionless;
- condition/task-level;
- a representation of evidence-distribution separation.

It is not:

- an encoding probability;
- a probability at all;
- a per-headline state;
- directly observed neural memory strength;
- attention;
- recollection;
- familiarity;
- belief.

Msep remains **MEASUREMENT_MODEL_ONLY** and may not enter the active CEM state vector in Phase B.

## 9. Equal-variance assumption boundary

The common d-prime formula assumes equal-variance Gaussian signal/noise evidence distributions.

Recognition-memory research often observes asymmetric ROCs and greater variance for studied-item evidence than foil evidence. Unequal-variance SDT models can fit such data, but a single yes/no operating point does not supply the multi-criterion ROC information needed to identify a richer variance model.

Therefore CEM uses equal-variance SDT only as a transparent reference measurement convention compatible with the published d-prime summary.

It must not claim:

- that recognition memory truly has equal target/foil variance;
- that `Drecog` fully specifies the recognition-memory process;
- that `Msep` is a biological encoding state.

## 10. Measurement validation contract

### VAL.M1.M01 — SDT reconstruction

Given registered hit, miss, false-alarm and correct-rejection counts, the reference measurement transform must produce finite `Drecog` and `Crecog`.

### VAL.M1.M02 — sensitivity direction

For otherwise comparable probe structures and response criterion, a condition with better target/foil discrimination must have higher `Drecog`.

### VAL.M1.MN01 — criterion is not sensitivity

A pure response-criterion shift must not be represented as an encoding/sensitivity change.

### VAL.M1.MN02 — d-prime does not identify Pencode

No deterministic mapping from `Drecog` alone to item-level `Pencode` is permitted.

### VAL.M1.MN03 — raw cells are not disposable

If recognition responses are simulated or ingested, hit/miss/false-alarm/correct-rejection counts must remain reconstructable rather than retaining only the summary d-prime.

### VAL.M1.MN04 — equal variance is a reference assumption

The CEM measurement layer must label the equal-variance Gaussian assumption and may not present it as established recognition-memory physiology.

### VAL.M1.MN05 — source wording does not redefine SDT cells

CEM uses standard SDT hit and false-alarm definitions even though the source article's prose uses “hit” more broadly when describing correct responses.

## 11. Consequence for the future executable mechanism

Phase B does **not** authorize `recognition.py`, `encoding.py`, `Pencode`, `beta_simp` or a UI.

The next scientific phase must compare explicit generative candidates capable of producing the registered recognition measurement:

1. an SDT-native continuous evidence-strength candidate;
2. an optional discrete/mixture encoding candidate only if it introduces explicit guessing/criterion/lure assumptions and has additional identifying evidence.

The candidate comparison must be judged at the raw response level and at the derived `Drecog` level.

A model is not accepted merely because an arbitrary parameter can be tuned to equal 1.23 or 0.80.

## 12. Phase B promotion gate

Phase B may merge only if:

- the measurement contract validates against schema;
- the standard SDT cell ontology is explicit;
- no unreported Study 3 target/foil split is invented;
- the log-linear extreme-rate convention is labeled as CEM's reference convention rather than source reproduction;
- `Drecog` and `Crecog` are mathematically separated;
- `Pencode` remains not identified;
- `Msep` remains measurement-model-only;
- the equal-variance assumption is explicitly bounded;
- planned measurement validation IDs remain absent from the active validation registry;
- no runtime or UI module is added;
- active variables, links, references, empirical targets and evidence snapshot remain unchanged;
- retained M0/M1.E1/M1.E2/M1.E3 outputs remain byte-reproducible;
- full CI passes.

## 13. Forbidden changes

No:

- active M1.E4 registry promotion;
- active `Msep`, `Crecog` or `Pencode` variable;
- `Pencode=f(Drecog)` shortcut;
- runtime recognition/encoding module;
- recognition UI;
- beta-simplicity value;
- hidden attention state;
- source-exact-reproduction claim without source-code verification;
- change to Alpha 0.4.2a0 release metadata;
- change to `EVIDENCE.M1.2026-09-16.r1`.

Phase B ends with a measurement bridge and an identifiability boundary, not an executable cognitive mechanism.

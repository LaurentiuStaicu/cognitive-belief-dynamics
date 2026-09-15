# Romanian Theory Editorial Style Guide

This guide applies to the Romanian Theory Reader corpus.

## Goal

Romanian text should read as native explanatory prose, not as an English technical text with Romanian inflections. Scientific precision and traceability to code must be preserved.

## Default rule

Use a natural Romanian equivalent when one exists and is unambiguous. Retain the English expression when it is:

- a literal identifier from code or data;
- a widely established technical label whose translation would reduce traceability;
- introduced once because readers may need the English term to locate the research literature.

When useful, introduce the Romanian form first and the English term in parentheses.

## Preferred forms

- baseline → model/nivel de referință
- ground truth → adevărul din simulare / adevărul cunoscut de mediul simulat
- pool → set / set factual / set disponibil
- ranking → ordonare algoritmică / sistem de recomandare și ordonare
- pattern → tipar
- outcome → rezultat
- task-specific → specific sarcinii
- nested model/null → model inclus / model nul inclus / modele incluse unul în altul
- forecast → prognoză
- planner → planificator
- seed → sămânță aleatoare
- source weight → pondere acordată sursei
- framing → încadrare / formă de prezentare, except where the English research label is required
- sharing → distribuire, except the literal model variable `Share`
- engagement → interacțiune, except literal variables such as `EngageIntent`
- deskilling → pierderea competenței, with `deskilling` optionally in parentheses at first use
- human in the loop → om în buclă, with the English phrase optionally in parentheses
- lateral reading → verificare laterală a surselor, with the English term optionally in parentheses

## Terms retained for scientific traceability

The following may remain in English when they identify a literature or implementation construct:

- Type 1 / Type 2
- predictive processing / predictive coding
- continued influence effect
- illusory truth effect when paired with its Romanian explanation
- `InformationUnit`, `SemanticProposition`, `PresentedMessage`
- variable and function identifiers such as `Share`, `EngageIntent`, `reward_context`, `semantic_signature`
- epistemic status constants such as EMPIRICAL, EXECUTABLE, CONCEPTUAL, INTERPRETIVE

## Sentence style

Prefer concrete causal sentences over nominalized formulations. State the distinction first, then the limitation. Avoid long chains of English noun phrases translated word-for-word.

Prefer:

> Expunerea nu este același lucru cu atenția. Un conținut poate fi afișat fără să fie procesat suficient pentru a influența o judecată ulterioară.

Avoid:

> Expunerea observabilă nu este echivalentă cu procesarea atențional-encodantă ulterioară.

## Epistemic language

Use verbs that match the evidence:

- `arată` for direct empirical results;
- `susține` for converging evidence;
- `este compatibil cu` when multiple explanations remain possible;
- `sugerează` for weaker or indirect evidence;
- `ipoteză` for an untested proposed mechanism;
- `nu demonstrează` when preventing an overinterpretation.

Avoid `dovedește` unless the logical context genuinely warrants it.

## Translation symmetry

Romanian and English chapters should make the same scientific claims. Translation may change syntax and examples for readability but must not change:

- epistemic status;
- causal direction;
- scope or population;
- strength of evidence;
- stated limitations;
- whether a mechanism is executable or conceptual.

## Readability test

Before merge, every Romanian paragraph should pass this question:

> Could a Romanian reader with scientific literacy understand the paragraph without mentally translating it back into English?

If not, rewrite it.
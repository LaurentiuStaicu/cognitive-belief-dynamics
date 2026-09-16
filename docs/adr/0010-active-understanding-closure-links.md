# ADR 0010 — OA-5D Active Understanding closure links and focus

Status: Proposed for OA-5D closure.

## Context

R6 requires OA-5D to close the Active Understanding foundation only after all three concept families are present, local history is clearable, and the learning surface cross-links to Theory, Search and Universal Inspector.

OA-5A/B/C already provide the challenge contract, Predict -> Reveal -> Explain interaction, bounded local history and the registered M1.E3 Challenge Model. The remaining integration gap is that challenge anchors primarily open the Scientific Registry.

## Decision

Every AU-1/AU-2/AU-3 reveal/explanation surface exposes three additional canonical continuations:

- Theory: the first registered THEORY worked-example anchor resolves to its existing Theory Reader chapter;
- Search: the first canonical semantic target becomes the exact global lexical query;
- Universal Inspector: the first canonical relation is opened directly when available, otherwise the canonical search target is used.

The M1.E3 Challenge Model links to its already-existing Theory chapter, Hneg semantic entity and Paccess semantic entity.

Search and Inspector actions remount only their own global surfaces. They do not remount Active Understanding, so the current Predict/Reveal state remains intact.

Focus moves only after an explicit user action:

- Search action -> native search input;
- Inspector action -> top-level complementary Inspector;
- Theory deep link -> focusable Theory article after the requested chapter loads.

No custom composite widget or modal is introduced.

## Scientific boundary

OA-5D adds no equation, coefficient, comparator, empirical target, semantic identity, evidence status, scientific confidence score or model-selection result.

The cross-links expose existing canonical objects only.

## Accessibility basis

This slice follows W3C/WAI guidance that functionality remain keyboard-operable, focus order be meaningful, Search be represented as a search landmark and Universal Inspector remain a top-level complementary landmark.

Full manual screen-reader certification remains part of OA-8 Trust Hardening; OA-5D does not claim it.

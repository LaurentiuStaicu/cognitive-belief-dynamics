# Development handoff — 2026-09-13

Recovered source: cognitive-epistemic-model-v0.2-stage.zip, saved September 13.
Version remains 0.2.0a0. This is staging, not a validated scientific release.

## Work completed in the continuation

- Recovered M0 simulator, 20 conceptual modules, 7 variables and 3 links.
- Included registries and schemas in the Python wheel; default validation reads
  installed package resources. `--root` retains external checkout validation.
- Rejected duplicate module, variable and link IDs before resolving references.
- Fixed mixed event sorting: chronological order, with input order preserved
  for simultaneous events. Previously the documented demo raised TypeError.
- Python suite: 17 tests passed, including regression cases for both fixes.

## Scope and next work

The web folder is an initial structure viewer, not a complete application.
No public application URL or Windows/Flatpak binaries exist in this snapshot.
The requested OS-independent access button must target a verified deployment.

Next: build and inspect the browser viewer, add reproducible web dependencies
and automated Python/package/web checks, then complete RO/EN explanations,
Visual ODD and run/replay views. Synchronize web registries from the canonical
model directory rather than maintaining independent copies. Add final license
files and source/evidence metadata before tagging a public release.

Preserve the distinction between conceptual Track A/B, the interpretive Jungian
extension, and executable M0. None is a fixed population category; no prevalence
estimate or empirical validation follows from passing software tests.

Event ties are resolved by input order, a computational convention whose effect
must be considered in future scenario design; no psychological priority is implied.

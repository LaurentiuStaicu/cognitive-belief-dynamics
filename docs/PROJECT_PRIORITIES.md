# Project priorities and v1 direction

User requirement confirmed 2026-09-13. Preserve this order in every continuation:

1. Understanding mechanisms comes first. Show variables/factors, interactions,
   explanatory graphics and sufficiently detailed descriptions. Explain what each
   quantity means, what it does not mean, its model dependencies, dynamics,
   assumptions and evidence. Do not reduce this to a control dashboard.
2. Prioritize factors to address, conditional on the chosen objective and context,
   using interactions, feasibility, costs and uncertainty rather than isolated scores.
3. Plan necessary actions and their timing, eventually including dependencies,
   responsibilities, resources, monitoring and reassessment.

The initial screen is Understanding. The laboratory follows it; graph, scenarios,
process and evidence registry remain directly accessible. Explanatory model paths
are distinct from the three evidence-registry links. Neither is labelled a fully
validated causal map. Broader conceptual modules remain visible as future scope.

## elementary OS direction

Near v1, build a native elementary OS application distributed as Flatpak, following
 the approach of the user's World3 application. Target GTK and Granite, Meson,
Gettext, native controls, theme/font preferences, portals for file access, desktop
entry, icon, AppStream metadata and a reproducible Flatpak build. Verify supported
SDK/runtime versions at that stage; do not freeze them from historical examples.
Web access remains available across operating systems. Current CSS is a web
adaptation, not a native GTK implementation or an AppCenter compliance claim.

Current visual decisions: system UI font first with Inter fallback, a shared
neutral surface palette, system light/dark preference, semantic colors, 6px-based
spacing with >=12px content margins and label separation where applicable, visible
keyboard focus, readable text at 200%, restrained typography, no network font
requirement. Native implementation must inherit the actual system font and theme.

Charts use distinct stroke patterns as well as color, labelled step axes and
exact-value tables. These are project accessibility decisions, not a claim that
the HIG mandates a particular scientific chart palette. Preserve clear legends,
units, temporal resolution and uncertainty. Do not confuse a graphical dependency
with an empirically established causal effect. Extensive educational prose is core
content; concise button labels do not justify removing that content.

Official sources consulted 2026-09-13:
- https://docs.elementary.io/hig/reference/text
- https://docs.elementary.io/hig/widgets/creating-layouts.md
- https://docs.elementary.io/develop/writing-apps/our-first-app.md
- https://docs.elementary.io/develop/apis/color-scheme
- https://blog.elementary.io/look-and-feel-changes-elementary-os-6/

The 2021 typography article documents the move to Inter historically. It is not
used to assert a fixed current platform font or runtime. Prefer system settings.

## v1 acceptance gates

Detailed bilingual explanations and navigable mechanism maps; explicit evidence
and uncertainty; justified scope and calibration of priorities; actionable plans;
keyboard, scaling and theme QA; equivalent scientific outputs across web/native;
reproducible Flatpak packaging and elementary OS installation tests; final licenses.

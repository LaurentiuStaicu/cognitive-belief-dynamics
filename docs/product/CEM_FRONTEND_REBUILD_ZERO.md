# CEM frontend rebuild — clean-slate product contract

Status: prototype gate. MOD.15, Flatpak, human calibration, new mechanisms and Full Model Atlas expansion remain blocked.

## Product question

The normal product exists to help a new user answer: **Through what mechanisms can information influence perception, memory, belief, judgment and action; what evidence supports each link; under what conditions does it change; what competing explanations exist; and what interventions have been studied?**

The product is question/pathway-first. Technical registries are implementation infrastructure, not the normal interface.

## Clean-slate boundary

The new web entry point must not mount, wrap, hide, or route into the prior InfoClar shell, old navigation, old four-quadrant layout, old dashboard, old Mechanism Explorer, old Full Model Atlas, legacy rails, inspector, Search UI or registry-facing components. Their history remains in Git. Scientific model code, M1/MOD.14 results, Semantic Spine, evidence/theory/source registries, scientific exports, domain logic, translations and non-visual adapters remain authoritative and unchanged.

## World3 → CEM design token mapping

Reference audited from `world3-empirical-flatpak/web/src/style.css` and `web/src/main.ts` on `main`.

| World3 token / convention | CEM v2 token / convention | Rule |
| --- | --- | --- |
| `Inter, ui-sans-serif, system-ui...` | identical font stack | no alternate product font |
| page `#f5f6f8` / muted surface `#f8f9fb` | `--page`, `--surface-muted` | same suite background family |
| `--surface: #fff` | `--surface: #fff` | normal panels/drawers |
| `--border: #dfe3e8` | `--border: #dfe3e8` | same subtle separators |
| `--text-muted: #687384` | `--text-muted: #687384` | secondary copy |
| `--accent: #5d5fef` | `--accent: #5d5fef` | focus/active accents, not epistemic meaning |
| `--shadow: 0 8px 28px rgba(35,45,60,.08)` | identical `--shadow` | primary raised surfaces only |
| panel radius `14px` | `--radius-panel: 14px` | pathway workspace, evidence blocks |
| control radius `8–10px` | `--radius-control: 9px` | buttons/selects/language switch |
| sticky header, ~76px | same header height and visual treatment | product-specific controls inside |
| EN/RO segmented control | identical interaction pattern | English first-run default |
| desktop breakpoint `1120px` | `1120px` | reflow context drawer / insight strip |
| mobile breakpoint `620px` | `620px` | pathway becomes vertical sequence |
| dark mode via `prefers-color-scheme` | same mechanism and contrast family | no separate theme language |

CEM intentionally does **not** copy World3's 2-column/2×2 product layout. World3 is temporal/scenario-first; CEM is mechanism/pathway-first.

## Prototype vertical slice

Only one path is allowed before expansion:

`Repeated exposure → Familiarity → Belief judgment → Sharing / action`

Secondary factors remain collapsed/on demand: prior knowledge, veracity cues, source context and correction.

The pathway must be visually traceable end-to-end without horizontal scrolling at 1440×900 and 1366×768. On mobile it becomes a single vertical sequence. Mechanism nodes contain only a natural-language label and one short explanatory sentence. Detailed evidence, uncertainty and limitations live in the dismissible context drawer.

## Evidence discipline

The 2026 Ye et al. systematic review/meta-analysis is the anchor for the illusory-truth phenomenon: 182 studies, 366 effect sizes, N=31,184, PEESE-adjusted g=0.37 (95% CI 0.30–0.44), substantial within- and between-study heterogeneity. This estimate constrains claims about the phenomenon; it must not become a universal CEM coefficient or an individual prediction.

The reader must distinguish the robust experimental endpoint effect (repetition can raise judged truth on average) from the exact mediation and functional form used inside CEM, which remain more uncertain/model-specific.

## Prototype acceptance gate

Before expansion to additional questions, automated browser checks and manual screenshots at 1440×900, 1366×768 and mobile must show that a new user can: identify CEM's problem, choose the repetition question, follow cause → mechanism → outcome, distinguish empirical/model/conceptual relations, inspect effect magnitude and uncertainty, see moderators and limitations, inspect at least one studied intervention, and open a clean theory reader without encountering internal codes.

If the path is not immediately traceable, the prototype fails and expansion stops.
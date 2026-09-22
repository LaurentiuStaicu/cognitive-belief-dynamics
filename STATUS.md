# Scientific status

## Release status

Cognitive Belief Dynamics (CBD) v0.1.1 is the current scientific-core maintenance release. It preserves the v0.1.0 scientific model and retained benchmark results while repairing verification coverage, provenance checks, canonical status reporting, reproducibility metadata, evidence metadata, and repository presentation. The version identifies a frozen software and model-artifact snapshot; it does not represent a claim that the full cognitive model has been empirically validated, population-calibrated, or established as a general model of human cognition.

The repository is intentionally maintained as a scientific model core. The v0.1.1 snapshot contains the canonical model specification, computational engine, schemas, empirical/evidence contracts, calibration/recovery diagnostics, synthetic recovery benchmarks, integrity hashes, reproducibility constraints, and scripts needed to reproduce retained model-building results. These diagnostic/recovery surfaces must not be interpreted as empirical population calibration. No model equation, retained benchmark value, threshold, or seed is changed by the v0.1.1 maintenance release. The retained evidence **set** is unchanged, while its metadata snapshot advances from `EVIDENCE.M1.2026-09-16.r1` to the content-audited `EVIDENCE.M1.2026-09-21.r2`. It does not include an end-user product layer.

## Canonical modeling paradigm

**Cognitive Belief Dynamics (CBD) is an event-driven cognitive state-transition and agent-level stochastic dynamical model informed by systems thinking; it is not currently a formal System Dynamics model.**

CBD contains persistent agent states, memory, saturation, decay, nonlinear transformations, temporal ordering, and stochastic decisions. These features make it a dynamical model. The frozen v0.1.1 release remains an open-loop baseline in which event schedules are externally supplied and Share does not automatically generate future exposure. Post-v0.1.1 `main` now also contains an optional F1a research layer classified `RECOVERY_TESTED`: when explicitly invoked, a realised Share can be routed through a synthetic directed network/transmission policy into a delayed recipient `ExposureEvent`, which is then processed by the unchanged `Simulator.step()` familiarity mechanism. A prospectively frozen, calibration-only synthetic benchmark recovered known conditional `q_transmit` values in all 20 core cells with minimum recovery probability 0.885; the retained authoritative result is byte-reproducible. The layer remains inactive by default and not empirically constrained, does not generate recipient decisions, and does not by itself close the full Share→Exposure→Decision→Share loop. It therefore does not justify formal System Dynamics classification.

This paradigm statement is canonical for the project. CBD must not be converted into System Dynamics, an agent-based network model, or another paradigm merely for methodological uniformity with the rest of the model suite. A paradigm change is justified only if the scientific question requires endogenous feedback, interaction, or emergence that the present event-driven state-transition architecture cannot represent adequately. Any such change must be explicit, scientifically justified, documented in this file before integration, and accompanied by a revised system boundary, state/update specification, evidence bridge, verification plan, and validation strategy.

## Post-release F1a research state

The first progressive-endogenization experiment is recorded in `model/experiments/f1a_endogenous_transmission_experiment.json` and documented in `docs/ODD_ENDOGENOUS_SCHEDULER.md`. Its current ladder stage is **RECOVERY_TESTED**. The prospective recovery design and authoritative result are retained in `model/benchmarks/f1a_transmission_recovery_core.json` and `model/benchmarks/results/f1a_transmission_recovery_authoritative_2026-09-21.json`, with the promotion decision in `model/experiments/f1a_recovery_promotion_2026-09-21.json`. All 20 frozen core cells passed the declared 0.80 gate, with minimum recovery 0.885; N=25 stress cells were explicitly non-gating and include recovery below 0.80. This is a best-case synthetic identifiability result only. `q_transmit` remains calibration-only, not an empirical or active runtime parameter. The next possible ladder stage is `EMPIRICALLY_CONSTRAINED`, which requires a separate evidence and measurement bridge; no automatic further promotion is allowed.

A post-recovery empirical-observability audit is now recorded in `docs/F1A_EMPIRICAL_OBSERVABILITY_AUDIT.md` and `model/experiments/f1a_empirical_observability_contract.json`. It finds that current open candidates such as Bluesky and SNAP Higgs can constrain topology, activity timing and downstream action structure, but do not directly observe the recipient-specific impression/cognitive-exposure numerator and negative-opportunity denominator required by the present `q_transmit` estimand. These are partial empirical component constraints only; F1a remains `RECOVERY_TESTED` and `q_transmit` remains calibration-only.

A subsequent platform-view bridge design (`docs/F1A_PLATFORM_VIEW_BRIDGE_DESIGN.md`; `model/experiments/f1a_platform_view_bridge_contract.json`) records a stronger restricted-data opportunity without changing that stage. A public SOMAR codebook compatibility audit (`docs/F1A_SOMAR_PUBLIC_CODEBOOK_AUDIT.md`; `model/experiments/f1a_somar_public_codebook_audit.json`) further confirms that the potential-exposure, actual-exposure and engagement URL tables share compatible high-level unit, owner-type, population and study-period structure. Numerical pairing remains unauthorized until variable-level count semantics, repeated-view handling, suppression/missingness rules and subset compatibility are resolved. SOMAR/FIES publicly documents separate potential-audience, actual-view and engagement surfaces, including URL-level potential exposure (ICPSR 300450), URL-level actual views (300470), URL-level engagement with views/audience (300475), participant/day domain views (300446), participant×network exposure (300458), and participant-level connections/views/engagement (300396). These support distinct `PotentialDelivery` and `PlatformView` measurement constructs, but the public descriptions do not establish event-level sender→recipient Share-to-View lineage or a validated PlatformView→CBD ExposureEvent mapping. Numerical component ratios remain codebook-gated and are not equivalent to `q_transmit`.

## Current scientific boundary

CBD combines several epistemic levels that must remain distinct. The source/data content audit for this release is retained in `model/audits/content_audit_2026-09-21.json`; a passing audit means the declared metadata and internal numerical relationships were checked, not that every conceptual mechanism is empirically validated:



- **Executable:** explicitly implemented mathematical or computational relations.
- **Empirical:** claims linked to external evidence within the scope recorded by the model contracts.
- **Conceptual:** model organization or candidate mechanisms that do not yet have a complete measurement/calibration bridge.
- **Interpretive:** theoretical framing that is not encoded as a universal empirical law.

MOD.14 includes a normative proposition-level Bayesian reference operator and explicit uncertainty calculation. It is not a calibrated population model, not a claim that the brain literally implements Bayes' rule, and not a truth oracle.

M1.E4 currently has retained synthetic model-recovery and protocol-robustness results. In the participant-aware confirmation benchmark, all 18 primary P64_X10 cells meet the declared 0.80 recovery gate, with a minimum observed recovery of 0.92. These are synthetic identifiability/discrimination results only. They do not establish EVSD or 2HT as the true human recognition architecture, identify Pencode, or constitute human validation.

Separately, the authoritative Phase M protocol-robustness stress gate closed with `PROTOCOL_ROBUSTNESS_FAIL`: 3 of 18 prospectively frozen cells fell below the 0.80 recovery gate (`ITEM_MODERATE__EVSD` = 0.780, `ITEM_HIGH__EVSD` = 0.560, `COMBINED_ADVERSE__EVSD` = 0.585), with a minimum recovery probability of 0.56. This does not erase the participant-aware confirmation result; it shows that candidate-family recovery is not robust across all frozen stress conditions. Phase M remains synthetic and does not select a human recognition architecture, identify Pencode, validate a human sample size, or authorize participant recruitment.

## Not established in v0.1.1

The following are outside the validated scope of this release:

- population calibration of the full model;
- human-participant validation of M1.E4;
- identification or estimation of Pencode;
- authorization of participant recruitment;
- a general-purpose truth, prediction, diagnostic, or decision system;
- an end-user application or production-ready interface.

Future releases should update this file whenever the scientific boundary changes. A version increment should never be used as a substitute for an explicit validation statement.

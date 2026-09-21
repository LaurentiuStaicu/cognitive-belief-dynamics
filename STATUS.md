# Scientific status

## Release status

Cognitive Belief Dynamics (CBD) v0.1.1 is the current scientific-core maintenance release. It preserves the v0.1.0 scientific model and retained benchmark results while repairing verification coverage, provenance checks, canonical status reporting, reproducibility metadata, and repository presentation. The version identifies a frozen software and model-artifact snapshot; it does not represent a claim that the full cognitive model has been empirically validated, population-calibrated, or established as a general model of human cognition.

The repository is intentionally maintained as a scientific model core. The v0.1.1 snapshot contains the canonical model specification, computational engine, schemas, empirical/evidence contracts, calibration artifacts, synthetic recovery benchmarks, integrity hashes, reproducibility constraints, and scripts needed to reproduce retained model-building results. No model equation, retained benchmark value, threshold, seed, or evidence snapshot is changed by the v0.1.1 maintenance release. It does not include an end-user product layer.

## Canonical modeling paradigm

**Cognitive Belief Dynamics (CBD) is an event-driven cognitive state-transition and agent-level stochastic dynamical model informed by systems thinking; it is not currently a formal System Dynamics model.**

CBD contains persistent agent states, memory, saturation, decay, nonlinear transformations, temporal ordering, and stochastic decisions. These features make it a dynamical model, but the current implementation does not contain the closed endogenous feedback structure required to classify it as System Dynamics in the strict sense. In particular, actions such as Share do not automatically generate future exposure, and event schedules remain externally supplied.

This paradigm statement is canonical for the project. CBD must not be converted into System Dynamics, an agent-based network model, or another paradigm merely for methodological uniformity with the rest of the model suite. A paradigm change is justified only if the scientific question requires endogenous feedback, interaction, or emergence that the present event-driven state-transition architecture cannot represent adequately. Any such change must be explicit, scientifically justified, documented in this file before integration, and accompanied by a revised system boundary, state/update specification, evidence bridge, verification plan, and validation strategy.

## Current scientific boundary

CBD combines several epistemic levels that must remain distinct:

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

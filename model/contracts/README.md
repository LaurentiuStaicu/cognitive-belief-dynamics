# Model contracts

Files in this directory are **pre-executable scientific contracts**.

They can reserve names, evidence sources, provenance, planned empirical targets,
planned validation patterns and promotion gates before those objects enter the
active Cognitive Epistemic Model registry.

A contract in this directory does **not** mean that its mechanism exists in the
simulator.

For Alpha 0.4.2a0:

- `m1_e3_evidence_contract.json` is the Phase A evidence/schema contract for the
  planned Headline Access Gate.
- `Hneg`, `Paccess`, `Access`, `PreviewImpression`,
  `TARGET.M1.E3.ROBERTSON_2023` and `VAL.M1.004/N04/N05/N06` remain planned
  objects only.
- the active evidence snapshot remains unchanged until a later approved phase
  actually promotes evidence into the active registry.
- no runtime equation or UI may be inferred from this contract.

Contract schemas and tests are merge gates intended to prevent planning metadata
from silently becoming executable scientific claims.


For Alpha 0.4.3a0:

- `m1_e4_evidence_contract.json` is the Phase A evidence/schema contract for the
  planned Headline Recognition Gate.
- the selected validation construct is `Drecog` (signal-detection recognition
  sensitivity), not a directly observed attention state;
- `Aattn` and event-level `Pencode` are explicitly deferred;
- `Hsimp` is reserved as precomputed controlled stimulus metadata, with no
  runtime LIWC dependency;
- the first comparator is conditioned on the existing `PreviewImpression`
  event and does not require M1.E3 `Access`;
- Shulman Study 4 and Mattis et al. 2025 are mandatory context boundaries;
- no M1.E4 object enters the active variable, validation, target or evidence
  registries in Phase A;
- the active evidence snapshot and public Alpha 0.4.2a0 release remain unchanged.


Alpha 0.4.3a0 Phase B adds a second pre-executable contract:

- `m1_e4_measurement_contract.json` defines the SDT measurement bridge from
  raw recognition cells to `Drecog` and an auxiliary response-criterion
  diagnostic `Crecog`.
- CEM uses standard hit/miss/false-alarm/correct-rejection terminology and does
  not infer an unreported target/foil split from the 24-item source task.
- the open reference estimator uses equal-variance Gaussian yes/no SDT with a
  Hautus log-linear correction, explicitly labeled as a CEM convention rather
  than exact reproduction of the source implementation.
- `Msep` is measurement-model-only and numerically equals `Drecog` only
  inside that reference model.
- `Pencode` is explicitly **not identified** by the current measurement and no
  deterministic `Drecog → Pencode` shortcut is permitted.
- no active registry, evidence snapshot, runtime, UI or release metadata is
  promoted in Phase B.

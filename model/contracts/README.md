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


Alpha 0.4.3a0 Phase C adds a third pre-executable contract:

- `m1_e4_generative_candidate_contract.json` freezes two formal recognition
  candidate families without selecting a winner.
- C1 is an equal-variance continuous SDT evidence-strength model with memory
  parameter `d` and response criterion `c`.
- C2 is a symmetric two-high-threshold model with detection parameter `Ddet`
  and uncertain-state guessing parameter `g`.
- both candidates must reconstruct the same nondegenerate single H/F operating
  point, demonstrating that one point cannot identify the model family.
- a more general asymmetric 2HT model remains deferred because `Do`, `Dn`
  and `g` are underidentified from only H and F.
- future discrimination requires multiple operating points / ROC information or
  an explicit bias manipulation with invariant candidate memory parameters.
- future fitting must operate on raw target/foil response counts, with Drecog and
  Crecog retained as diagnostics rather than the only fitting target.
- `Pencode` remains not identified and cannot be equated with either `d` or
  `Ddet`.
- no active model, registry, runtime, UI, evidence snapshot or release metadata
  is promoted in Phase C.


Alpha 0.4.3a0 Phase D adds the preregistration-ready model-discrimination protocol:

- `m1_e4_discrimination_protocol.json` defines the minimum dataset and decision
  rules required before EVSD versus 2HT selection is permitted.
- the primary route is an experimentally manipulated binary-bias ROC with at
  least three nondegenerate operating points per Hsimp condition; five or more
  are preferred.
- a six-point confidence ROC is supplemental and may not serve as the sole
  decisive evidence.
- prospective candidate-recovery simulation is mandatory; CEM uses >=0.80
  recovery across the preregistered core grid as a design convention, not a
  universal literature threshold.
- future fitting must use raw target/foil response counts with binomial
  likelihoods, candidate-specific bias invariance, parameter-count-aware fit
  diagnostics and held-out prediction when feasible.
- discordant diagnostics yield `INCONCLUSIVE_MODEL_DISCRIMINATION`.
- `Pencode` remains not identified and inactive.
- no model winner, active registry, runtime, UI, evidence snapshot or release
  metadata is promoted in Phase D.


Alpha 0.4.3a0 Phase E adds an executable synthetic validation benchmark without
promoting an active cognitive mechanism:

- `m1_e4_candidate_recovery_benchmark.json` freezes the recovery-analysis
  contract.
- the executable benchmark lives in
  `calibration/m1_e4_candidate_recovery.py`, outside the active simulation path.
- every synthetic dataset is generated by EVSD or 2HT and then fit by **both**
  candidates.
- train AIC and independent held-out predictive log likelihood must agree for a
  decisive EVSD/2HT label; otherwise the replicate is `INCONCLUSIVE`.
- model recovery is reported as a generator-by-selected confusion matrix, while
  parameter recovery is reported separately.
- the authoritative full config uses 200 replicates for every generator × memory
  regime × trial-count cell and evaluates the 0.80 design convention per cell.
- CI runs only a deterministic smoke benchmark and cannot certify the full
  design-recovery gate.
- no active registry, UI, Pencode, evidence snapshot or release metadata is
  changed in Phase E.


Alpha 0.4.3a0 Phase H adds participant-aware hierarchical validation tooling:

- `m1_e4_participant_aware_recovery.json` freezes the participant/repeated-
  measures recovery contract.
- the Phase G 640+640 aggregate anchor is preserved while response counts are
  redistributed across 40, 64, 80 or 128 participants.
- participant memory ability and response-bias tendency are random effects shared
  across repeated Hsimp conditions and bias blocks.
- random effects are marginalized with Gauss-Hermite quadrature.
- held-out predictive fit uses a new independent participant cohort.
- screening (50 replicates/cell) is separated from 200-replicate confirmation.
- human data collection, model activation, Pencode and UI remain blocked.


Alpha 0.4.3a0 Phase J adds a prospective confirmation contract:

- `m1_e4_participant_confirmation.json` freezes the 200-replicate confirmation
  gate before execution.
- all 18 P64_X10 cells are mandatory;
- all lower-recovery boundary ties from P40_X16, P80_X8 and P128_X5 are retained;
- the exact surface contains 29 cells;
- point-estimate recovery >=0.80 remains the formal gate;
- Wilson 95% lower bounds are reported prospectively as a separate robustness
  flag;
- cell-specific SHA-256-derived RNG permits deterministic parallel execution;
- confirmation cannot execute before Phase I is merged.


## Optimization-track product contracts

OA product contracts and deterministic fixtures may also live in this directory, but they are **not scientific-model promotion contracts**.

- `workspace_fixture_v1.json` and `semantic_index_fixture_v1.json` are OA regression fixtures.
- `active_understanding_v1.json` is the OA-5A learning-interaction contract. It references existing canonical model/semantic artifacts, adds no equation or evidence status, and does not promote a cognitive mechanism.

Their schemas/tests are product-integrity gates and must preserve the scientific boundaries defined by the optimization architecture.


OA-6A adds the first Decision Under Uncertainty product contract:

- `decision_uncertainty_v1.json` is a schema-validated registry of uncertainty and decision-assumption metadata for the existing intervention planner.
- low/reference/high remain finite sensitivity scenarios with `probability_status = NOT_AVAILABLE`;
- objective weight, effort units and activation timing are explicitly decision assumptions rather than scientific parameters;
- the registry records the planner's structural-scope limitation separately;
- no equal scenario weights, confidence intervals, expected values or probability-of-best claims are inferred;
- a fail-closed probability guard requires explicit normalized weights before any later probability-bearing finite-scenario consumer can proceed;
- OA-6A changes no intervention score, equation, evidence status, reference run or release metadata.


OA-7 begins the Reality Loop with a pre-executable product contract:

- `reality_loop_v1.json` reserves distinct `SimulationResult`, `DecisionAnalysis`, `ImplementationPlan` and `ObservedOutcome` objects;
- Action Canvas follows Problem -> target mechanism -> intervention -> proximal result -> intermediate result -> final outcome;
- Indicator objects and the adaptive NOW/WATCH/IF/THEN/STOP/REASSESS vocabulary are schema-bound;
- real-world plans require explicit population, context and primary outcome fields;
- observations are append-only retrospective records and cannot mutate the frozen prospective snapshot;
- Decision Autopsy may propose a new revision but `prior_prediction_mutated` is fixed to false;
- the current Workspace v1 schema is intentionally unchanged; runtime persistence requires a later explicit migration;
- the contract fixture is synthetic product metadata and promotes no scientific mechanism, equation, evidence status or recommendation.

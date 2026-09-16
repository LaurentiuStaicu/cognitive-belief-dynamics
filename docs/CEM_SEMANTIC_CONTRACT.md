# CEM Semantic Contract — OA-0

Status: planning contract. No runtime semantic migration occurs in OA-0.

## 1. Purpose

The Semantic Spine gives the same scientific object one stable identity across Theory, Mechanisms, Structure, Registry, Search, Workspace, provenance and future GTK/native surfaces.

It is intentionally smaller than a general ontology.

## 2. Design rules

1. Stable identifiers outlive labels and translations.
2. Labels are localized presentation; IDs are canonical identity.
3. Scientific status is explicit data, not inferred from CSS or prose.
4. Computational dependency and empirical support are different relations.
5. Provenance relations are different from scientific/semantic relations.
6. Existing registries remain authoritative until an OA-1 adapter proves lossless migration.
7. No UI code may manufacture a stronger epistemic status than the source entity carries.
8. New semantic types are added only when an existing type cannot express a required distinction.

## 3. Initial entity vocabulary

### Concept

Non-executable explanatory concept.

### Construct

Theoretical construct that may have one or more operationalizations.

### Variable

Registered state/input/output quantity with an ontology role and model scope.

### Claim

Human-readable proposition whose support, limits and scope can be inspected.

### Mechanism

Candidate explanatory process. A mechanism may be conceptual or executable.

### Formula

Functional form used by an executable model.

### Assumption

Condition accepted for an analysis/model/decision but not itself established by execution.

### Evidence

Bibliographic or empirical evidence item with provenance and review scope.

### EmpiricalTarget

Observable pattern used to test/discriminate model behavior.

### Validation

Test or criterion evaluating a specified prediction/invariant.

### Model

Versioned scientific specification such as M0 or an M1 comparator.

### Scenario

Frozen or parameterized model execution context.

### Prediction

Prospective expected result, including a user's prediction where applicable.

### Intervention

Candidate action represented in a decision analysis; not automatically a recommendation.

### Outcome

Defined result construct.

### Indicator

Operational measure used to monitor an outcome or signpost.

### Observation

Recorded real-world or experimental result, distinct from simulated result.

### Decision

Recorded selection/commitment with objective, assumptions and provenance.

## 4. Initial relation vocabulary

### DEPENDS_ON

Computational or definitional dependency. Does not imply empirical causation.

### SUPPORTS

Evidence/claim support relation.

### CONTRADICTS

Evidence/claim inconsistency or counterevidence relation.

### LIMITS

Boundary/limitation relation.

### OPERATIONALIZES

Connects a construct/mechanism to a measurable or executable representation.

### TESTS

Connects validation/experiment to claim, mechanism or prediction.

### PREDICTS

Model/mechanism to prospective prediction.

### TARGETS

Intervention to intended mechanism/construct/outcome.

### MEASURES

Indicator/metric to construct/outcome.

### DERIVED_FROM

Semantic derivation between versions/outputs.

### GENERATED_BY

Result to analysis/execution activity.

### SUPERSEDES

Explicit replacement relation preserving historical identity.

## 5. Epistemic status vocabulary

Initial statuses:

- EMPIRICAL_PHENOMENON
- EMPIRICAL_OBSERVATION
- CANDIDATE_MECHANISM
- REFERENCE_FORM
- UNCALIBRATED_FORM
- CONCEPTUAL
- INTERPRETIVE
- VALIDATED_WITHIN_SCOPE

OA-1 must define allowed status/entity combinations and migration rules from current registry fields.

## 6. Required common metadata

Where applicable:

- id
- entity_type
- labels (RO/EN)
- description
- epistemic_status
- model_scope
- evidence_refs
- assumptions
- limitations
- related_entities
- provenance_ref
- introduced_in
- superseded_by

Fields may be optional by type, but identity and type are always required.

## 7. Stable ID convention

Candidate convention:

`<family>.<scope>.<descriptive_slug>`

Examples:

- `variable.m0.familiarity`
- `mechanism.m0.repetition_familiarity`
- `claim.repetition.perceived_truth`
- `formula.m0.familiarity_update`
- `validation.m0.repetition_differential`

OA-1 must map existing IDs without breaking external links or registry references. Where old IDs are already stable and meaningful, aliases are preferred over destructive renaming.

## 8. Separation from provenance

Semantic relations answer questions such as:

- What does this variable depend on?
- What evidence supports this claim?
- What mechanism operationalizes this phenomenon?

Provenance answers:

- Which analysis generated this result?
- Which model/evidence snapshot/settings were used?
- Which version revised an earlier entity?

OA-1/OA-2 may map provenance to W3C PROV concepts, but the semantic layer remains CEM-native.

## 9. OA-1 migration gate

OA-1 cannot merge until:

- every current registered variable/link/module/reference/validation has a lossless semantic representation or explicit deferral;
- old IDs/deep links remain resolvable;
- generated web artifacts remain scientifically identical;
- semantic status cannot strengthen the current scientific status;
- RO/EN labels retain parity;
- schema validation and regression tests pass.

## 10. Explicit non-goals

OA-1 does not require:

- RDF;
- OWL;
- SPARQL;
- graph database;
- automatic causal discovery;
- automatic literature inference;
- automatic claim strengthening;
- merging all current model JSON into one monolithic file.

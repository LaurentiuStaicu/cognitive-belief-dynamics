from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def repository_json_paths() -> list[Path]:
    roots = [
        ROOT / ".atm",
        ROOT / ".github",
        ROOT / "model",
        ROOT / "releases",
        ROOT / "schemas",
    ]
    paths: list[Path] = []
    for base in roots:
        if not base.exists():
            continue
        paths.extend(path for path in base.rglob("*.json") if path.is_file())
    return sorted(set(paths))


def test_all_repository_json_artifacts_parse() -> None:
    paths = repository_json_paths()
    assert paths
    failures = []
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - diagnostic branch
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    assert failures == []


def test_all_json_schemas_are_valid_draft_2020_12_schemas() -> None:
    paths = sorted((ROOT / "schemas").glob("*.schema.json"))
    assert paths
    failures = []
    for path in paths:
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # pragma: no cover - diagnostic branch
            failures.append(f"{path.relative_to(ROOT)}: {exc}")
    assert failures == []


def test_each_scientific_contract_has_an_explicit_schema_mapping() -> None:
    mappings = {
        "m1_e3_evidence_contract.json": "m1_e3_evidence_contract.schema.json",
        "m1_e4_candidate_recovery_benchmark.json": "m1_e4_candidate_recovery_benchmark.schema.json",
        "m1_e4_discrimination_protocol.json": "m1_e4_discrimination_protocol.schema.json",
        "m1_e4_evidence_contract.json": "m1_e4_evidence_contract.schema.json",
        "m1_e4_generative_candidate_contract.json": "m1_e4_generative_candidate_contract.schema.json",
        "m1_e4_measurement_contract.json": "m1_e4_measurement_contract.schema.json",
        "m1_e4_participant_aware_recovery.json": "m1_e4_participant_aware_recovery.schema.json",
        "m1_e4_participant_confirmation.json": "m1_e4_participant_confirmation.schema.json",
        "world_model_v1.json": "world_model.schema.json",
    }
    contract_dir = ROOT / "model" / "contracts"
    actual = {path.name for path in contract_dir.glob("*.json")}
    assert actual == set(mappings)

    for contract_name, schema_name in mappings.items():
        contract = json.loads((contract_dir / contract_name).read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(schema).iter_errors(contract),
            key=lambda error: list(error.path),
        )
        assert errors == [], (
            contract_name
            + ": "
            + "; ".join(error.message for error in errors)
        )


def test_benchmark_provenance_index_preserves_known_run_ids() -> None:
    text = (
        ROOT / "model" / "benchmarks" / "results" / "PROVENANCE.md"
    ).read_text(encoding="utf-8")
    for run_id in (
        "35064052116",
        "35065350252",
        "35069251436",
        "35081097627",
        "35229760477",
    ):
        assert run_id in text
    assert "not invented" in text.lower()


def test_atm_repository_manifest_paths_resolve() -> None:
    manifest = json.loads((ROOT / ".atm" / "repository.json").read_text(encoding="utf-8"))

    file_paths = [
        manifest["version_source"]["path"],
        manifest["status_source"],
        *manifest["required_paths"],
        *manifest["retrieval"]["canonical"],
    ]
    for path in file_paths:
        assert (ROOT / path).is_file(), path

    for group in ("structural", "evidence", "tabular", "implementation"):
        for path in manifest["retrieval"][group]:
            assert (ROOT / path).exists(), path


def test_exposure_count_does_not_assert_arbitrary_upper_bound() -> None:
    variables = json.loads((ROOT / "model" / "variables.json").read_text(encoding="utf-8"))
    nexp = next(item for item in variables if item["id"] == "VAR.EXPOSURE.COUNT")
    assert "range" not in nexp
    assert "non-negative integer" in nexp["domain_note"]
    assert "No scientific upper bound" in nexp["domain_note"]


def test_canonical_registry_schemas_reject_unknown_top_level_fields() -> None:
    for name in (
        "module.schema.json",
        "variable.schema.json",
        "link.schema.json",
        "reference.schema.json",
        "subsystem.schema.json",
        "process.schema.json",
        "empirical_target.schema.json",
    ):
        schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
        assert schema.get("additionalProperties") is False, name


def test_conceptual_module_registry_retains_complete_mod01_to_mod20_surface() -> None:
    modules = json.loads((ROOT / "model" / "modules.json").read_text(encoding="utf-8"))
    assert {item["id"] for item in modules} == {f"MOD.{i:02d}" for i in range(1, 21)}

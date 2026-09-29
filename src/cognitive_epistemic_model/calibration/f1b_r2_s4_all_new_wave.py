from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
import statistics
from typing import Any

from .f1b_r2_paired_method_m2_sequential_resolution import (
    EXPECTED_METHODS_M2,
    REFIT_FAILURE,
    UNRESOLVED_AT_CAP,
    stable_shard,
)
from .f1b_r2_s4_broad_executor import EVIDENCE_ORIGIN_NEW, PREFIX_EXECUTION_FAILURE

GATE_ID = "F1B.R2.S4.ALL_NEW_WAVE.EXECUTION_GATE.V1"
STATUS = "NON_AUTHORITATIVE_S4_ALL_NEW_WAVE_EXECUTION_DESIGN"
PLAN_STATUS = "NON_AUTHORITATIVE_S4_ALL_NEW_WAVE_EXECUTION_PLAN_COMPLETE"
SHARD_STATUS = "NON_AUTHORITATIVE_S4_ALL_NEW_WAVE_SHARD_COMPLETE"
COMBINED_STATUS = "NON_AUTHORITATIVE_S4_ALL_NEW_WAVE_COMBINED_COMPLETE"
EXPECTED_METHODS = tuple(EXPECTED_METHODS_M2)
FROZEN_WAVES = {
    "W1": (25, 49, "42a1803705c0c4f7efbfae0983a7c57f20036c76cd933c99af3fcd4e3cd9087c", "2191e0aceb072c20bca90dab1b6db3ed8bffef997bf2ead8ec2ace2ac4a81957", "36d294a165ec1e8a8baffac70516ce7fceab149998079b534998503f3f578175", 5, 27, "W2"),
    "W2": (50, 74, "a24dea39afdb03b91784248755d9ddad94466bbab8391044308eeeb8c9eff617", "a338bd644ee62a474cf417aa0396a0ff2df4a310618e63ffb644c8f5f3cc8ba2", "399b4feecc51731f4691ca7168eb61625834cc1dc74e2fb66d3f6fe23ffe2475", 6, 27, "W3"),
    "W3": (75, 99, "e0b7126a2342a65427a03f1a45d42990093e89f2c3ab0eeb661544b5548ff3ce", "81ed9d1c0ea527da9d1501c5652e529e87f50e73c7eb3a2b876fad0d02393998", "d27bce0c8c17022644bcaaa6f0bb4b2be19239cf8074ab54ae75c982feb058e2", 4, 27, None),
}


def canonical_json_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def method_row_id(run_id: str, method: str) -> str:
    return f"{run_id}|METHOD={method}"


def wave_spec(config: dict, wave_id: str, *, require_authorized: bool = True) -> dict:
    if wave_id not in FROZEN_WAVES:
        raise ValueError("unsupported S4 all-new wave")
    if require_authorized and wave_id not in config["authorized_wave_ids"]:
        raise ValueError(f"S4 all-new wave not authorized: {wave_id}")
    return config["waves"][wave_id]


def validate_config(config: dict) -> None:
    if config["gate_id"] != GATE_ID or config["status"] != STATUS:
        raise ValueError("S4 all-new gate identity/status changed")
    if int(config["issue"]) != 259:
        raise ValueError("S4 all-new issue changed")
    w0 = config["retained_sources"]["w0_retention"]
    if w0["status"] != "NON_AUTHORITATIVE_S4_W0_COMBINED_COMPLETE_RETAINED":
        raise ValueError("S4 all-new requires retained W0 combine")
    if w0["w1_authorized_after_retention"] is not True:
        raise ValueError("S4 W1 authorization changed")
    matrix = config["retained_sources"]["s4_matrix_result"]
    if int(matrix["scientific_run_count"]) != 15000:
        raise ValueError("S4 all-new matrix count changed")
    if matrix["scientific_run_ids_sha256"] != "851e7336387901ca15d2486ed8efc19cd090ffac869b760352106a3f455f2b43":
        raise ValueError("S4 all-new matrix identity changed")
    if tuple(config["authorized_wave_ids"]) != ("W1",):
        raise ValueError("only W1 may be authorized at this gate")
    if set(config["waves"]) != set(FROZEN_WAVES):
        raise ValueError("S4 all-new wave set changed")
    for wave_id, frozen in FROZEN_WAVES.items():
        actual = config["waves"][wave_id]
        keys = (
            "replicate_start", "replicate_end", "scientific_run_ids_sha256",
            "method_row_ids_sha256", "shard_plan_sha256",
            "minimum_scientific_runs_per_shard", "maximum_scientific_runs_per_shard",
            "next_wave_id",
        )
        if tuple(actual[k] for k in keys) != frozen:
            raise ValueError(f"S4 all-new wave contract changed: {wave_id}")
        if int(actual["scientific_run_count"]) != 3750 or int(actual["method_row_count"]) != 15000:
            raise ValueError(f"S4 all-new wave count changed: {wave_id}")
    execution = config["execution"]
    required = {
        "shard_count": 250,
        "matrix_indices": "0..249",
        "fail_fast": False,
        "max_parallel": 20,
        "imported_evidence_allowed": False,
        "evidence_origin": EVIDENCE_ORIGIN_NEW,
        "all_four_methods_same_scientific_run_same_shard": True,
        "new_rows_use_broad_executor": True,
        "numerical_lineage": "Haswell",
        "sequential_prefix_attempts": 199,
        "sequential_max_total_attempts": 10000,
        "stop_on_first_refit_failure": True,
        "wave_combine_requires_all_250_shards": True,
        "scientific_interpretation_after_wave": False,
    }
    if any(execution[k] != v for k, v in required.items()):
        raise ValueError("S4 all-new execution contract changed")
    p = config["w1_preflight"]
    expected = ("W1", 11, 15, 60,
        "da11844e3c88b0f2dd95c039efb1f7f0ba398d3d48518d4c136a039c084e25a2",
        "a6917767655c652a0977e8455f069db50e95fa6f91d9a7fd9de7d48bdb6f99da")
    keys = ("wave_id", "shard_index", "scientific_run_count", "method_row_count", "scientific_run_ids_sha256", "method_row_ids_sha256")
    if tuple(p[k] for k in keys) != expected:
        raise ValueError("S4 W1 preflight changed")
    if p["full_w1_authorized_after_preflight_retention"] is not True:
        raise ValueError("S4 W1 preflight authorization changed")
    if config["release"]["release_blocker_closed"] is not False:
        raise ValueError("S4 all-new cannot close v0.2.0 blocker")
    if any(bool(v) for v in config["boundary"].values()):
        raise ValueError("S4 all-new boundary was weakened")


def build_wave_plan(s4_manifest: dict, config: dict, *, wave_id: str) -> dict:
    validate_config(config)
    spec = wave_spec(config, wave_id)
    if s4_manifest["status"] != "NON_AUTHORITATIVE_S4_BROAD_SCIENTIFIC_MATRIX_MANIFEST":
        raise ValueError("S4 all-new raw manifest status changed")
    if int(s4_manifest["scientific_run_count"]) != 15000:
        raise ValueError("S4 all-new raw manifest count changed")
    rows = [r for r in s4_manifest["rows"] if int(spec["replicate_start"]) <= int(r["evaluation_replicate"]) <= int(spec["replicate_end"])]
    run_ids = sorted(str(r["scientific_run_id"]) for r in rows)
    if len(rows) != 3750 or len(set(run_ids)) != 3750:
        raise ValueError("S4 all-new wave coverage changed")
    if canonical_json_sha256(run_ids) != spec["scientific_run_ids_sha256"]:
        raise ValueError("S4 all-new run-ID digest changed")
    method_ids = sorted(method_row_id(r, m) for r in run_ids for m in EXPECTED_METHODS)
    if canonical_json_sha256(method_ids) != spec["method_row_ids_sha256"]:
        raise ValueError("S4 all-new method-row digest changed")
    shard_plan = []
    for i in range(250):
        local = sorted(str(r["scientific_run_id"]) for r in rows if stable_shard(str(r["scientific_run_id"]), 250) == i)
        if not local:
            raise ValueError("S4 all-new wave contains empty shard")
        n = len(local)
        shard_plan.append({
            "shard_index": i, "scientific_run_count": n,
            "imported_scientific_run_count": 0, "new_scientific_run_count": n,
            "imported_method_row_count": 0, "new_method_execution_count": n * 4,
            "scientific_run_ids_sha256": canonical_json_sha256(local),
        })
    counts = [r["scientific_run_count"] for r in shard_plan]
    if [min(counts), max(counts)] != [spec["minimum_scientific_runs_per_shard"], spec["maximum_scientific_runs_per_shard"]]:
        raise ValueError("S4 all-new shard range changed")
    digest_rows = [{k: r[k] for k in (
        "shard_index", "scientific_run_count", "imported_scientific_run_count",
        "new_scientific_run_count", "imported_method_row_count", "new_method_execution_count")}
        for r in shard_plan]
    if canonical_json_sha256(digest_rows) != spec["shard_plan_sha256"]:
        raise ValueError("S4 all-new shard-plan digest changed")
    return {
        "gate_id": config["gate_id"], "status": PLAN_STATUS, "authoritative": False,
        "issue": int(config["issue"]), "wave_id": wave_id,
        "replicate_start": spec["replicate_start"], "replicate_end": spec["replicate_end"],
        "scientific_run_count": 3750, "method_row_count": 15000,
        "imported_scientific_run_count": 0, "imported_method_row_count": 0,
        "new_scientific_run_count": 3750, "new_method_execution_count": 15000,
        "scientific_run_ids_sha256": spec["scientific_run_ids_sha256"],
        "method_row_ids_sha256": spec["method_row_ids_sha256"],
        "shard_count": 250, "shard_plan_sha256": spec["shard_plan_sha256"],
        "shard_plan": shard_plan, "execution_authorized": True,
        "scientific_interpretation_authorized": False, "method_selected": False,
        "power_validated": False, "release_0_2_0_blocker_closed": False,
    }


def validate_shard_scientific_rows(rows: list[dict], *, config: dict, wave_id: str, shard_index: int) -> None:
    validate_config(config)
    spec = wave_spec(config, wave_id)
    if not 0 <= int(shard_index) < 250 or not rows:
        raise ValueError("S4 all-new invalid/empty shard")
    ids = [str(r["scientific_run_id"]) for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("S4 all-new shard scientific IDs are not unique")
    for row in rows:
        rep = int(row["evaluation_replicate"])
        if not int(spec["replicate_start"]) <= rep <= int(spec["replicate_end"]):
            raise ValueError("S4 all-new shard contains wrong-wave replicate")
        if stable_shard(str(row["scientific_run_id"]), 250) != int(shard_index):
            raise ValueError("S4 all-new shard assignment changed")


def build_shard_result(scientific_rows: list[dict], method_rows: list[dict], *, config: dict, wave_id: str, shard_index: int) -> dict:
    validate_shard_scientific_rows(scientific_rows, config=config, wave_id=wave_id, shard_index=shard_index)
    scientific_ids = sorted(str(r["scientific_run_id"]) for r in scientific_rows)
    expected_ids = sorted(method_row_id(r, m) for r in scientific_ids for m in EXPECTED_METHODS)
    actual_ids = [method_row_id(str(r["scientific_run_id"]), str(r["inference_method"])) for r in method_rows]
    if len(actual_ids) != len(expected_ids) or len(set(actual_ids)) != len(actual_ids) or sorted(actual_ids) != expected_ids:
        raise ValueError("S4 all-new shard method-row coverage changed")
    by_run: dict[str, list[dict]] = defaultdict(list)
    for row in method_rows:
        by_run[str(row["scientific_run_id"])].append(row)
    if set(by_run) != set(scientific_ids):
        raise ValueError("S4 all-new shard scientific coverage changed")
    allowed = {"SEQUENTIAL_RESOLVED_AT_PREFIX", "SEQUENTIAL_RESOLVED", UNRESOLVED_AT_CAP, REFIT_FAILURE, PREFIX_EXECUTION_FAILURE}
    status_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    for rows in by_run.values():
        if {str(r["inference_method"]) for r in rows} != set(EXPECTED_METHODS):
            raise ValueError("S4 all-new shard method set changed")
        if len({str(r["dataset_sha256"]) for r in rows}) != 1:
            raise ValueError("S4 all-new paired methods saw different datasets")
        if any(str(r["evidence_origin"]) != EVIDENCE_ORIGIN_NEW for r in rows):
            raise ValueError("S4 all-new imported evidence is forbidden")
        for row in rows:
            status = str(row["status"])
            if status not in allowed:
                raise ValueError("S4 all-new shard unsupported terminal status")
            status_counts[status] += 1
            if row["decision"] is not None:
                decision_counts[str(row["decision"])] += 1
            if status == UNRESOLVED_AT_CAP and (row["decision"] is not None or int(row["terminal_n"]) != 10000):
                raise ValueError("S4 all-new unresolved row invalid")
            if status in {REFIT_FAILURE, PREFIX_EXECUTION_FAILURE} and row["decision"] is not None:
                raise ValueError("S4 all-new failure row has decision")
    return {
        "status": SHARD_STATUS, "authoritative": False, "wave_id": wave_id,
        "shard_index": int(shard_index), "scientific_run_count": len(scientific_rows),
        "method_row_count": len(method_rows), "imported_scientific_run_count": 0,
        "new_scientific_run_count": len(scientific_rows), "imported_method_row_count": 0,
        "new_method_execution_count": len(method_rows),
        "scientific_run_ids_sha256": canonical_json_sha256(scientific_ids),
        "method_row_ids_sha256": canonical_json_sha256(sorted(actual_ids)),
        "status_counts": dict(sorted(status_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "evidence_origin_counts": {EVIDENCE_ORIGIN_NEW: len(method_rows)}, "rows": method_rows,
        "scientific_interpretation_authorized": False, "method_selected": False,
        "power_validated": False,
    }


def combine_wave_shards(shards: list[dict], *, plan: dict, config: dict, wave_id: str) -> dict:
    validate_config(config)
    spec = wave_spec(config, wave_id)
    if plan["status"] != PLAN_STATUS or plan["wave_id"] != wave_id:
        raise ValueError("S4 all-new plan identity changed")
    if len(shards) != 250:
        raise ValueError("S4 all-new combine requires exactly 250 shards")
    by_index = {int(s["shard_index"]): s for s in shards}
    expected = {int(s["shard_index"]): s for s in plan["shard_plan"]}
    if set(by_index) != set(range(250)) or set(expected) != set(range(250)):
        raise ValueError("S4 all-new shard-index coverage changed")
    all_rows: list[dict] = []
    scientific_ids: set[str] = set()
    shard_identity: list[str] = []
    for i in range(250):
        shard, want = by_index[i], expected[i]
        if shard["status"] != SHARD_STATUS or shard["authoritative"] is not False or shard["wave_id"] != wave_id:
            raise ValueError("S4 all-new shard identity changed")
        if any(int(shard[k]) != int(want[k]) for k in ("scientific_run_count", "new_scientific_run_count", "new_method_execution_count")):
            raise ValueError("S4 all-new shard count changed")
        if int(shard["imported_scientific_run_count"]) or int(shard["imported_method_row_count"]):
            raise ValueError("S4 all-new shard imported evidence")
        if shard["scientific_interpretation_authorized"] is not False or shard["method_selected"] is not False or shard["power_validated"] is not False:
            raise ValueError("S4 all-new shard boundary weakened")
        rows = list(shard["rows"])
        local_runs = sorted({str(r["scientific_run_id"]) for r in rows})
        local_methods = sorted(method_row_id(str(r["scientific_run_id"]), str(r["inference_method"])) for r in rows)
        if canonical_json_sha256(local_runs) != shard["scientific_run_ids_sha256"] or canonical_json_sha256(local_methods) != shard["method_row_ids_sha256"]:
            raise ValueError("S4 all-new shard digest changed")
        if scientific_ids.intersection(local_runs):
            raise ValueError("S4 all-new scientific run appears in multiple shards")
        scientific_ids.update(local_runs)
        all_rows.extend(rows)
        shard_identity.append(f"{i:03d}|{shard['scientific_run_ids_sha256']}|{shard['method_row_ids_sha256']}")
    if len(scientific_ids) != 3750 or len(all_rows) != 15000:
        raise ValueError("S4 all-new combined coverage changed")
    if canonical_json_sha256(sorted(scientific_ids)) != spec["scientific_run_ids_sha256"]:
        raise ValueError("S4 all-new combined scientific digest changed")
    method_ids = [method_row_id(str(r["scientific_run_id"]), str(r["inference_method"])) for r in all_rows]
    if len(set(method_ids)) != 15000 or canonical_json_sha256(sorted(method_ids)) != spec["method_row_ids_sha256"]:
        raise ValueError("S4 all-new combined method digest changed")
    if any(str(r["evidence_origin"]) != EVIDENCE_ORIGIN_NEW for r in all_rows):
        raise ValueError("S4 all-new combined imported evidence")
    by_run: dict[str, list[dict]] = defaultdict(list)
    for row in all_rows:
        by_run[str(row["scientific_run_id"])].append(row)
    for run_id, rows in by_run.items():
        if {str(r["inference_method"]) for r in rows} != set(EXPECTED_METHODS) or len({str(r["dataset_sha256"]) for r in rows}) != 1:
            raise ValueError(f"S4 all-new combined pairing changed: {run_id}")
    status_counts = Counter(str(r["status"]) for r in all_rows)
    allowed = {"SEQUENTIAL_RESOLVED_AT_PREFIX", "SEQUENTIAL_RESOLVED", UNRESOLVED_AT_CAP, REFIT_FAILURE, PREFIX_EXECUTION_FAILURE}
    if not set(status_counts).issubset(allowed):
        raise ValueError("S4 all-new combined unsupported terminal status")
    decision_counts = Counter(str(r["decision"]) for r in all_rows if r["decision"] is not None)
    method_summaries = {}
    for method in EXPECTED_METHODS:
        rows = [r for r in all_rows if str(r["inference_method"]) == method]
        terminal = [int(r["terminal_n"]) for r in rows]
        method_summaries[method] = {
            "row_count": len(rows),
            "status_counts": dict(sorted(Counter(str(r["status"]) for r in rows).items())),
            "decision_counts": dict(sorted(Counter(str(r["decision"]) for r in rows if r["decision"] is not None).items())),
            "evidence_origin_counts": {EVIDENCE_ORIGIN_NEW: len(rows)},
            "terminal_n_summary": {"minimum": min(terminal), "median": statistics.median(terminal), "maximum": max(terminal)},
        }
    ordered = sorted(all_rows, key=lambda r: (str(r["scientific_run_id"]), EXPECTED_METHODS.index(str(r["inference_method"]))))
    next_wave = spec["next_wave_id"]
    return {
        "status": COMBINED_STATUS, "authoritative": False, "issue": int(config["issue"]),
        "wave_id": wave_id, "shard_count": 250, "scientific_run_count": 3750,
        "method_row_count": 15000, "imported_scientific_run_count": 0,
        "imported_method_row_count": 0, "new_scientific_run_count": 3750,
        "new_method_execution_count": 15000,
        "scientific_run_ids_sha256": canonical_json_sha256(sorted(scientific_ids)),
        "method_row_ids_sha256": canonical_json_sha256(sorted(method_ids)),
        "shard_identity_digest_sha256": canonical_json_sha256(sorted(shard_identity)),
        "row_content_sha256": canonical_json_sha256(ordered),
        "status_counts": dict(sorted(status_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "evidence_origin_counts": {EVIDENCE_ORIGIN_NEW: 15000},
        "method_summaries": method_summaries, "rows": ordered,
        "scientific_interpretation_authorized": False, "method_selected": False,
        "power_validated": False, "next_wave_id": next_wave,
        "next_wave_authorized_after_retention": next_wave is not None,
        "release_0_2_0_blocker_closed": False,
    }

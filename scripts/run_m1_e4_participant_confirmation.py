from __future__ import annotations

import argparse
import json
from pathlib import Path

from cognitive_epistemic_model.calibration.m1_e4_participant_confirmation import (
    run_confirmation_cell,
    summarize_confirmation,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run frozen Phase J M1.E4 participant-aware confirmation cells."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("model/benchmarks/m1_e4_participant_confirmation_200.json"),
    )
    parser.add_argument("--cell-id", action="append", default=None)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--replicates",
        type=int,
        default=None,
        help="Smoke/debug override only; authoritative runs must use the frozen config.",
    )
    args = parser.parse_args()

    confirmation = json.loads(args.config.read_text())
    screening = json.loads(
        Path(confirmation["source_screening_config"]).read_text()
    )

    if args.replicates is not None:
        if args.replicates <= 0:
            raise SystemExit("--replicates must be positive")
        confirmation = {**confirmation, "replicates_per_cell": args.replicates}

    selected = confirmation["selected_cells"]
    if args.cell_id:
        wanted = set(args.cell_id)
        selected = [row for row in selected if row["cell_id"] in wanted]
        missing = wanted - {row["cell_id"] for row in selected}
        if missing:
            raise SystemExit(f"unknown cell ids: {sorted(missing)}")

    results = [
        run_confirmation_cell(
            confirmation_config=confirmation,
            screening_config=screening,
            selected_cell=cell,
        )
        for cell in selected
    ]

    if len(results) == len(confirmation["selected_cells"]):
        payload = summarize_confirmation(confirmation, results)
    else:
        payload = {
            "benchmark_id": confirmation["benchmark_id"],
            "replicates_per_cell": confirmation["replicates_per_cell"],
            "partial_execution": True,
            "results": sorted(results, key=lambda row: row["cell_id"]),
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

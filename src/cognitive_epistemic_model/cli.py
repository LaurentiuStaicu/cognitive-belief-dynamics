from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from . import __version__
from .events import DecisionEvent, ExposureEvent
from .simulation import Simulator
from .state import AgentState


def main() -> None:
    parser = argparse.ArgumentParser(prog="cemodel")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    val = sub.add_parser("validate")
    val.add_argument("--root", help="Validate an external model checkout; defaults to bundled registries")
    args = parser.parse_args()

    if args.cmd == "validate":
        from pathlib import Path
        from .registry import validate_model_dir
        if args.root:
            root = Path(args.root)
            counts = validate_model_dir(root / "model", root / "schemas")
        else:
            from importlib.resources import as_file, files
            with as_file(files("cognitive_epistemic_model") / "data") as root:
                counts = validate_model_dir(root / "model", root / "schemas")
        print(json.dumps(counts, indent=2))
        return

    if args.cmd == "demo":
        agent = AgentState(agent_id="A1", prior_belief={"C1": 0.5})
        sim = Simulator({"A1": agent}, seed=7)
        sim.run([
            ExposureEvent(0, "A1", "C1", "S1"),
            ExposureEvent(1, "A1", "C1", "S1"),
            DecisionEvent(2, "A1", "C1", "S1", evidence_signal=0.0),
        ])
        print(json.dumps([asdict(x) for x in sim.log], indent=2))

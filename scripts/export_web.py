"""Export canonical registries and deterministic reference runs for the static viewer."""
from cognitive_epistemic_model import __version__
from cognitive_epistemic_model.calibration.diagnostics import (
    local_identifiability_report,
    prediction_robustness_report,
)
from cognitive_epistemic_model.editorial import reference_editorial_experiment
from cognitive_epistemic_model.events import (
    CorrectionEvent,
    DecisionEvent,
    ExposureEvent,
    SourceFeedbackEvent,
)
from cognitive_epistemic_model.explanations import explain_reference_run
from cognitive_epistemic_model.interventions import export_interventions
from cognitive_epistemic_model.simulation import Simulator
from cognitive_epistemic_model.state import AgentState, ModelParams
from dataclasses import asdict
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "web/public/model"


def reference_run(kind):
    agent = AgentState(agent_id="A1", prior_belief={"C1": 0.3})
    sim = Simulator({"A1": agent}, seed=7)
    frames = []
    for time in range(13):
        events = []
        if time in (1, 2, 3, 4):
            events.append(ExposureEvent(time, "A1", "C1", "S1"))
        if kind == "correction" and time == 5:
            events.append(CorrectionEvent(time, "A1", "C1"))
        if kind == "source" and time in (2, 4, 6, 8):
            events.append(SourceFeedbackEvent(time, "A1", "S1", False))
        events.append(
            DecisionEvent(
                time,
                "A1",
                "C1",
                "S1",
                evidence_signal=0.6 if kind == "source" else 0.0,
                reward_context=0.5,
                accuracy_cue=kind == "accuracy" and time >= 5,
            )
        )
        start = len(sim.log)
        sim.run(events)
        frames.append(
            {
                "time": time,
                "familiarity": agent.f("C1"),
                "correction": agent.c("C1"),
                "reliability": agent.t("S1"),
                "events": [asdict(e) for e in sim.log[start:]],
                **sim.log[-1].observation,
            }
        )
    return {
        "id": kind,
        "purpose": "MECHANISM_TEST_DEMONSTRATION",
        "seed": 7,
        "prior": 0.3,
        "parameters": asdict(ModelParams()),
        "frames": frames,
    }


def export():
    DEST.mkdir(parents=True, exist_ok=True)
    evidence_snapshot = json.loads(
        (ROOT / "model" / "evidence_snapshot.json").read_text()
    )["id"]
    version_payload = {
        "version": __version__,
        "software_version": __version__,
        "channel": "Alpha",
        "model": "M1",
        "model_specification": "M1",
        "baseline_model_specification": "M0",
        "evidence_snapshot": evidence_snapshot,
        "release_tag": "v" + __version__,
    }
    (DEST / "version.json").write_text(json.dumps(version_payload, indent=2) + "\n")

    for name in (
        "variables",
        "links",
        "modules",
        "validation_tests",
        "references",
        "subsystems",
        "processes",
        "evidence_snapshot",
        "empirical_targets",
    ):
        (DEST / f"{name}.json").write_bytes(
            (ROOT / "model" / f"{name}.json").read_bytes()
        )

    (DEST / "interventions.json").write_text(
        json.dumps(export_interventions(), separators=(",", ":")) + "\n"
    )

    runs = [
        reference_run(k)
        for k in ("repetition", "correction", "source", "accuracy")
    ]
    (DEST / "explanations.json").write_text(
        json.dumps(
            {
                "model_version": __version__,
                "model_specification": "M0",
                "purpose": "EXPLANATION_OF_REFERENCE_RUNS",
                "scope": "Latent-score decomposition, not causal attribution",
                "runs": [explain_reference_run(r) for r in runs],
            },
            indent=2,
        )
        + "\n"
    )
    (DEST / "runs.json").write_text(
        json.dumps(
            {
                "model_version": __version__,
                "model_specification": "M0",
                "purpose": "MECHANISM_TEST_DEMONSTRATION",
                "runs": runs,
            },
            indent=2,
        )
        + "\n"
    )

    (DEST / "m1_editorial.json").write_text(
        json.dumps(
            {
                "model_version": __version__,
                "model_specification": "M1",
                "baseline_model_specification": "M0",
                "experiment": reference_editorial_experiment(),
            },
            indent=2,
        )
        + "\n"
    )

    diagnostics = {
        "software_version": __version__,
        "model_specification": "M0",
        "identifiability": local_identifiability_report(),
        "prediction_robustness": prediction_robustness_report(),
    }
    (DEST / "diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, allow_nan=False) + "\n"
    )


if __name__ == "__main__":
    export()

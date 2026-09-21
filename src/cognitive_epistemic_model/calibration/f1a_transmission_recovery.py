from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import TYPE_CHECKING

import numpy as np

from ..endogenous import EndogenousRunResult, run_endogenous
from ..events import DecisionEvent, Event, ExposureEvent
from ..network import StaticDirectedNetwork
from ..simulation import Simulator
from ..state import AgentState
from ..transmission import ForcedPassThroughPolicy, TransmissionProposal
from ..updates import update_familiarity

if TYPE_CHECKING:
    from ..simulation import LogEntry


@dataclass(frozen=True)
class RecoveryBernoulliTransmissionPolicy:
    """Calibration-only Bernoulli edge-transmission generator.

    q_transmit is a synthetic parameter for recovery experiments only. This
    class is intentionally kept in the calibration namespace and is not an
    active CBD runtime policy.
    """

    q_transmit: float
    delay: float
    rng: np.random.Generator
    policy_id: str = "POLICY.F1A.RECOVERY_BERNOULLI.V1"

    def __post_init__(self) -> None:
        if not 0.0 <= self.q_transmit <= 1.0:
            raise ValueError("q_transmit must be in [0, 1]")
        if self.delay <= 0:
            raise ValueError("synthetic transmission delay must be strictly positive")

    def propose(
        self,
        event: Event,
        completed_log: "LogEntry",
        network: StaticDirectedNetwork,
    ) -> tuple[TransmissionProposal, ...]:
        if not isinstance(event, DecisionEvent):
            return ()
        observation = completed_log.observation
        if observation is None or observation.get("share") is not True:
            return ()

        proposals: list[TransmissionProposal] = []
        for recipient_id in network.eligible_recipients(event.agent_id):
            if self.rng.random() >= self.q_transmit:
                continue
            proposals.append(
                TransmissionProposal(
                    event=ExposureEvent(
                        time=event.time + self.delay,
                        agent_id=recipient_id,
                        claim_id=event.claim_id,
                        source_id=event.source_id,
                    ),
                    sender_id=event.agent_id,
                    recipient_id=recipient_id,
                    delay=self.delay,
                    policy_id=self.policy_id,
                )
            )
        return tuple(proposals)


def exact_binomial_recovery_probability(
    opportunities: int,
    q_transmit: float,
    tolerance: float,
) -> float:
    if opportunities <= 0:
        raise ValueError("opportunities must be positive")
    if not 0.0 <= q_transmit <= 1.0:
        raise ValueError("q_transmit must be in [0, 1]")
    if tolerance < 0.0:
        raise ValueError("tolerance must be non-negative")

    return float(
        sum(
            comb(opportunities, exposures)
            * q_transmit**exposures
            * (1.0 - q_transmit) ** (opportunities - exposures)
            for exposures in range(opportunities + 1)
            if abs(exposures / opportunities - q_transmit) <= tolerance + 1e-12
        )
    )


def _seed_sequence(
    master_seed: int,
    *,
    stream: int,
    q_transmit: float,
    opportunities: int,
    delay: float,
    replicate: int,
) -> np.random.SeedSequence:
    return np.random.SeedSequence(
        [
            int(master_seed),
            int(stream),
            int(round(q_transmit * 10000.0)),
            int(opportunities),
            int(round(delay * 1000.0)),
            int(replicate),
        ]
    )


def _cognitive_seed(
    master_seed: int,
    *,
    q_transmit: float,
    opportunities: int,
    delay: float,
    replicate: int,
) -> int:
    sequence = _seed_sequence(
        master_seed,
        stream=0xC0D,
        q_transmit=q_transmit,
        opportunities=opportunities,
        delay=delay,
        replicate=replicate,
    )
    return int(sequence.generate_state(1, dtype=np.uint32)[0])


def _transmission_rng(
    master_seed: int,
    *,
    q_transmit: float,
    opportunities: int,
    delay: float,
    replicate: int,
) -> np.random.Generator:
    sequence = _seed_sequence(
        master_seed,
        stream=0xF1A,
        q_transmit=q_transmit,
        opportunities=opportunities,
        delay=delay,
        replicate=replicate,
    )
    return np.random.default_rng(sequence)


def _decision_events(
    opportunities: int,
    *,
    spacing: float,
    claim_id: str,
    source_id: str,
) -> tuple[DecisionEvent, ...]:
    if opportunities <= 0:
        raise ValueError("opportunities must be positive")
    if spacing <= 0:
        raise ValueError("decision spacing must be positive")
    return tuple(
        DecisionEvent(
            time=float(index) * spacing,
            agent_id="A",
            claim_id=claim_id,
            source_id=source_id,
            evidence_signal=0.0,
        )
        for index in range(opportunities)
    )


def _count_endogenous_exposures(result: EndogenousRunResult) -> int:
    return sum(
        item.origin == "ENDOGENOUS" and item.event_type == "ExposureEvent"
        for item in result.trace
    )


def _max_delay_error(result: EndogenousRunResult, expected_delay: float) -> float:
    by_notice = {item.notice_id: item for item in result.trace}
    errors: list[float] = []
    for item in result.trace:
        if item.origin != "ENDOGENOUS" or item.event_type != "ExposureEvent":
            continue
        if item.parent_notice_id is None:
            raise RuntimeError("endogenous exposure is missing parent provenance")
        parent = by_notice[item.parent_notice_id]
        errors.append(abs((item.scheduled_time - parent.scheduled_time) - expected_delay))
    return max(errors, default=0.0)


def _expected_familiarity(exposures: int, alpha_f: float) -> float:
    value = 0.0
    for _ in range(exposures):
        value = update_familiarity(value, alpha_f)
    return value


def run_recovery_replicate(
    *,
    q_transmit: float,
    opportunities: int,
    delay: float,
    master_seed: int,
    replicate: int,
    decision_spacing: float,
    sender_sharing_bias: float,
    claim_id: str = "C1",
    source_id: str = "S1",
) -> dict:
    if delay >= decision_spacing:
        raise ValueError("delay must be smaller than decision spacing in the frozen recovery design")

    agents = {
        "A": AgentState(agent_id="A", sharing_bias=float(sender_sharing_bias)),
        "B": AgentState(agent_id="B"),
    }
    simulator = Simulator(
        agents,
        seed=_cognitive_seed(
            master_seed,
            q_transmit=q_transmit,
            opportunities=opportunities,
            delay=delay,
            replicate=replicate,
        ),
    )
    network = StaticDirectedNetwork(nodes=("A", "B"), edges=(("A", "B"),))
    policy = RecoveryBernoulliTransmissionPolicy(
        q_transmit=float(q_transmit),
        delay=float(delay),
        rng=_transmission_rng(
            master_seed,
            q_transmit=q_transmit,
            opportunities=opportunities,
            delay=delay,
            replicate=replicate,
        ),
    )
    result = run_endogenous(
        simulator,
        _decision_events(
            opportunities,
            spacing=float(decision_spacing),
            claim_id=claim_id,
            source_id=source_id,
        ),
        network=network,
        policy=policy,
    )

    decision_logs = [entry for entry in result.log if entry.event_type == "DecisionEvent"]
    if len(decision_logs) != opportunities:
        raise RuntimeError("unexpected number of realised Share opportunities")
    if not all(
        entry.observation is not None and entry.observation.get("share") is True
        for entry in decision_logs
    ):
        raise RuntimeError("frozen recovery fixture requires every sender Share to be realised")

    exposures = _count_endogenous_exposures(result)
    q_hat = exposures / opportunities
    expected_familiarity = _expected_familiarity(exposures, simulator.params.alpha_f)
    familiarity_error = abs(agents["B"].f(claim_id) - expected_familiarity)

    return {
        "q_true": float(q_transmit),
        "q_hat": float(q_hat),
        "opportunities": int(opportunities),
        "realised_exposures": int(exposures),
        "delay": float(delay),
        "delay_realization_error": _max_delay_error(result, float(delay)),
        "final_familiarity": float(agents["B"].f(claim_id)),
        "expected_familiarity": float(expected_familiarity),
        "familiarity_consistency_error": float(familiarity_error),
    }


def run_forced_pass_through_control(
    *,
    opportunities: int,
    delay: float,
    decision_spacing: float,
    sender_sharing_bias: float,
    simulator_seed: int,
    claim_id: str = "C1",
    source_id: str = "S1",
) -> dict:
    agents = {
        "A": AgentState(agent_id="A", sharing_bias=float(sender_sharing_bias)),
        "B": AgentState(agent_id="B"),
    }
    simulator = Simulator(agents, seed=int(simulator_seed))
    result = run_endogenous(
        simulator,
        _decision_events(
            opportunities,
            spacing=float(decision_spacing),
            claim_id=claim_id,
            source_id=source_id,
        ),
        network=StaticDirectedNetwork(nodes=("A", "B"), edges=(("A", "B"),)),
        policy=ForcedPassThroughPolicy(delay=float(delay)),
    )
    return {
        "opportunities": int(opportunities),
        "realised_exposures": int(_count_endogenous_exposures(result)),
        "delay_realization_error": _max_delay_error(result, float(delay)),
    }


def _cell_summary(
    *,
    q_transmit: float,
    opportunities: int,
    delay: float,
    replicates: int,
    tolerance: float,
    recovery_gate: float,
    role: str,
    master_seed: int,
    decision_spacing: float,
    sender_sharing_bias: float,
    claim_id: str,
    source_id: str,
) -> dict:
    runs = [
        run_recovery_replicate(
            q_transmit=q_transmit,
            opportunities=opportunities,
            delay=delay,
            master_seed=master_seed,
            replicate=replicate,
            decision_spacing=decision_spacing,
            sender_sharing_bias=sender_sharing_bias,
            claim_id=claim_id,
            source_id=source_id,
        )
        for replicate in range(replicates)
    ]
    q_hat = np.asarray([row["q_hat"] for row in runs], dtype=float)
    errors = q_hat - float(q_transmit)
    recovery_probability = float(np.mean(np.abs(errors) <= tolerance + 1e-12))

    return {
        "role": role,
        "q_true": float(q_transmit),
        "opportunities": int(opportunities),
        "delay": float(delay),
        "replicates": int(replicates),
        "q_hat_mean": float(np.mean(q_hat)),
        "q_hat_bias": float(np.mean(errors)),
        "q_hat_mae": float(np.mean(np.abs(errors))),
        "q_hat_rmse": float(np.sqrt(np.mean(errors**2))),
        "recovery_probability": recovery_probability,
        "mean_realised_exposures": float(
            np.mean([row["realised_exposures"] for row in runs])
        ),
        "maximum_delay_realization_error": float(
            max(row["delay_realization_error"] for row in runs)
        ),
        "maximum_familiarity_consistency_error": float(
            max(row["familiarity_consistency_error"] for row in runs)
        ),
        "passes_recovery_gate": (
            recovery_probability >= recovery_gate if role == "core" else None
        ),
    }


def run_recovery_benchmark(config: dict, *, authoritative: bool = True) -> dict:
    seed = int(config["seed"])
    replicates = int(config["replicates_per_grid_cell"])
    if replicates <= 0:
        raise ValueError("replicates_per_grid_cell must be positive")

    q_grid = tuple(float(x) for x in config["generator"]["grid"])
    design = config["observation_design"]
    core_counts = tuple(int(x) for x in design["core_opportunity_counts"])
    stress_counts = tuple(int(x) for x in design["stress_opportunity_counts"])
    delays = tuple(float(x) for x in design["abstract_delays"])
    spacing = float(design["decision_spacing"])
    sender_bias = float(design["sender_sharing_bias"])
    claim_id = str(design["claim_id"])
    source_id = str(design["source_id"])

    tolerance = float(config["estimator"]["absolute_error_tolerance"])
    gate = float(config["recovery_gate"]["minimum_recovery_probability_each_core_cell"])

    cells: list[dict] = []
    for role, counts in (("stress", stress_counts), ("core", core_counts)):
        for opportunities in counts:
            for delay in delays:
                for q_transmit in q_grid:
                    cells.append(
                        _cell_summary(
                            q_transmit=q_transmit,
                            opportunities=opportunities,
                            delay=delay,
                            replicates=replicates,
                            tolerance=tolerance,
                            recovery_gate=gate,
                            role=role,
                            master_seed=seed,
                            decision_spacing=spacing,
                            sender_sharing_bias=sender_bias,
                            claim_id=claim_id,
                            source_id=source_id,
                        )
                    )

    core_cells = [row for row in cells if row["role"] == "core"]
    stress_cells = [row for row in cells if row["role"] == "stress"]

    controls_config = config["deterministic_controls"]
    q_zero_cfg = controls_config["q_zero"]
    q_one_cfg = controls_config["q_one"]

    q_zero = run_recovery_replicate(
        q_transmit=float(q_zero_cfg["q_transmit"]),
        opportunities=int(q_zero_cfg["opportunities"]),
        delay=float(q_zero_cfg["delay"]),
        master_seed=seed,
        replicate=0,
        decision_spacing=spacing,
        sender_sharing_bias=sender_bias,
        claim_id=claim_id,
        source_id=source_id,
    )
    q_one = run_recovery_replicate(
        q_transmit=float(q_one_cfg["q_transmit"]),
        opportunities=int(q_one_cfg["opportunities"]),
        delay=float(q_one_cfg["delay"]),
        master_seed=seed,
        replicate=0,
        decision_spacing=spacing,
        sender_sharing_bias=sender_bias,
        claim_id=claim_id,
        source_id=source_id,
    )
    forced = run_forced_pass_through_control(
        opportunities=int(q_one_cfg["opportunities"]),
        delay=float(q_one_cfg["delay"]),
        decision_spacing=spacing,
        sender_sharing_bias=sender_bias,
        simulator_seed=seed,
        claim_id=claim_id,
        source_id=source_id,
    )

    q_zero_pass = q_zero["realised_exposures"] == int(q_zero_cfg["required_exposures"])
    q_one_pass = q_one["realised_exposures"] == int(q_one_cfg["required_exposures"])
    forced_match_pass = (
        q_one["realised_exposures"] == forced["realised_exposures"]
        if q_one_cfg["must_match_forced_pass_through_count"]
        else True
    )
    delay_pass = (
        max(
            [row["maximum_delay_realization_error"] for row in cells]
            + [q_zero["delay_realization_error"], q_one["delay_realization_error"], forced["delay_realization_error"]]
        )
        <= 1e-12
    )
    familiarity_pass = (
        max(row["maximum_familiarity_consistency_error"] for row in cells) <= 1e-12
    )

    coverage = {
        str(n): min(
            exact_binomial_recovery_probability(n, q, tolerance)
            for q in q_grid
        )
        for n in (*stress_counts, *core_counts)
    }

    monotonic_checks: list[dict] = []
    for opportunities in (*stress_counts, *core_counts):
        for delay in delays:
            subset = sorted(
                (
                    row for row in cells
                    if row["opportunities"] == opportunities and row["delay"] == delay
                ),
                key=lambda row: row["q_true"],
            )
            means = [row["q_hat_mean"] for row in subset]
            monotonic_checks.append(
                {
                    "opportunities": opportunities,
                    "delay": delay,
                    "q_hat_means": means,
                    "non_decreasing": all(
                        right + 1e-12 >= left
                        for left, right in zip(means, means[1:])
                    ),
                }
            )

    minimum_core = min(row["recovery_probability"] for row in core_cells)
    all_core_pass = all(bool(row["passes_recovery_gate"]) for row in core_cells)
    controls_pass = q_zero_pass and q_one_pass and forced_match_pass
    structural_checks_pass = controls_pass and delay_pass and familiarity_pass

    return {
        "benchmark_id": config["benchmark_id"],
        "status": (
            "AUTHORITATIVE_SYNTHETIC_RECOVERY_RESULT"
            if authoritative
            else "SMOKE_NON_AUTHORITATIVE"
        ),
        "authoritative": bool(authoritative),
        "seed": seed,
        "replicates_per_grid_cell": replicates,
        "recovery_definition": {
            "estimator": config["estimator"]["name"],
            "absolute_error_tolerance": tolerance,
            "minimum_core_cell_recovery_probability": gate,
        },
        "prospective_exact_binomial_minimum_coverage": coverage,
        "core_grid_results": core_cells,
        "stress_grid_results": stress_cells,
        "minimum_core_grid_recovery_probability": float(minimum_core),
        "all_core_grid_cells_pass": bool(all_core_pass),
        "controls": {
            "q_zero": {**q_zero, "pass": bool(q_zero_pass)},
            "q_one": {**q_one, "pass": bool(q_one_pass)},
            "forced_pass_through": forced,
            "q_one_matches_forced_pass_through": bool(forced_match_pass),
            "all_controls_pass": bool(controls_pass),
        },
        "structural_checks": {
            "delay_realization_pass": bool(delay_pass),
            "familiarity_consistency_pass": bool(familiarity_pass),
            "all_structural_checks_pass": bool(structural_checks_pass),
        },
        "sensitivity_checks": {
            "mean_exposure_proportion_monotonicity": monotonic_checks,
            "all_monotonic": all(row["non_decreasing"] for row in monotonic_checks),
        },
        "promotion_candidate": bool(
            authoritative and all_core_pass and structural_checks_pass
        ),
        "interpretation_boundary": (
            "Best-case synthetic recovery benchmark only. A passing result can support "
            "RECOVERY_TESTED status for F1a but does not establish an empirical transmission "
            "mechanism, realistic q values, empirical delay semantics, or ACTIVE status."
        ),
    }

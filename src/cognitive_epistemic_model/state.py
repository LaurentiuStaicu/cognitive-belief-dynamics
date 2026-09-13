from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentState:
    agent_id: str
    familiarity: dict[str, float] = field(default_factory=dict)
    correction_access: dict[str, float] = field(default_factory=dict)
    reliability_estimate: dict[str, float] = field(default_factory=dict)
    prior_belief: dict[str, float] = field(default_factory=dict)
    accuracy_baseline: float = 0.5
    sharing_bias: float = 0.0

    def f(self, claim_id: str) -> float:
        return self.familiarity.get(claim_id, 0.0)

    def c(self, claim_id: str) -> float:
        return self.correction_access.get(claim_id, 0.0)

    def t(self, source_id: str) -> float:
        return self.reliability_estimate.get(source_id, 0.5)

    def b0(self, claim_id: str) -> float:
        return self.prior_belief.get(claim_id, 0.5)


@dataclass(frozen=True)
class ModelParams:
    alpha_f: float = 0.35
    alpha_c: float = 0.70
    lambda_c: float = 0.08
    alpha_t: float = 0.25
    beta_f: float = 0.8
    beta_source_evidence: float = 1.2
    beta_correction: float = 1.6
    beta_accuracy_cue: float = 1.0
    beta_reward: float = 1.0

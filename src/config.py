"""
System constants and resource constraints for EchoNode-Harmony.

All mobile targets adhere to Σ-SEPA v4.0 specifications.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MobileConstraints:
    """Σ-SEPA v4.0 edge-device resource budget."""
    max_memory_mb: float = 150.0
    max_latency_ms: float = 800.0
    max_power_watts: float = 4.1


@dataclass(frozen=True)
class ConvergenceParams:
    """Parameters governing Σ-PAS ethical convergence."""
    kappa: float = 0.22            # Restoring force coefficient
    alpha_base: float = 0.08       # Base learning rate
    alpha_decay: float = 0.998     # Per-step decay (ensures Robbins-Monro Σα²<∞)
    noise_sigma: float = 0.012     # Stochastic noise amplitude
    initial_s: float = 0.30        # Starting alignment score
    target_s: float = 1.0          # Perfect alignment


@dataclass(frozen=True)
class SwarmConfig:
    """Default swarm topology."""
    default_node_count: int = 7
    heartbeat_interval_sec: float = 1.1
    erps_dimensions: int = 3       # [intent_score, reflection_depth, ethical_gradient]
    erps_growth_rate: float = 0.08
    reflection_gain: float = 0.22  # How much each reflection step moves S_t


# Formal verification pipeline (stubs — real provers will be integrated)
PROVERS = ["Lean4", "Z3", "Coq", "Isabelle/HOL"]

# Singleton configs
MOBILE = MobileConstraints()
CONVERGENCE = ConvergenceParams()
SWARM = SwarmConfig()

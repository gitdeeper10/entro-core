"""
ENTRO-CORE: Nonlinear Control Law (Eq. 5)
u(t) = w₁·σ(Ψ_norm - θ) + w₂·tanh(dΨ/dt) + w₃·tanh(d²Ψ/dt²)
"""

import math


def sigmoid(x: float) -> float:
    """σ(x) = 1 / (1 + e⁻ˣ)"""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    exp_x = math.exp(x)
    return exp_x / (1.0 + exp_x)


def tanh(x: float) -> float:
    """Hyperbolic tangent using math.tanh for stability"""
    # Use built-in math.tanh for numerical stability
    return math.tanh(x)


def compute_control(
    psi_norm: float,
    dpsi_dt: float,
    d2psi_dt2: float,
    w1: float = 0.5,
    w2: float = 0.3,
    w3: float = 0.2,
    theta: float = 1.4
) -> float:
    """
    Compute control signal u(t) from state components
    
    Returns:
        u(t) in [0, 1]
    """
    perception = sigmoid(psi_norm - theta)
    reflex = tanh(dpsi_dt)
    intuition = tanh(d2psi_dt2)
    
    u = w1 * perception + w2 * reflex + w3 * intuition
    return max(0.0, min(1.0, u))


class ControlLaw:
    """Controller with state tracking"""
    
    def __init__(self, w1=0.5, w2=0.3, w3=0.2, theta=1.4):
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.theta = theta
    
    def __call__(self, psi_norm: float, dpsi_dt: float, d2psi_dt2: float) -> float:
        return compute_control(psi_norm, dpsi_dt, d2psi_dt2, self.w1, self.w2, self.w3, self.theta)
    
    def get_components(self, psi_norm: float, dpsi_dt: float, d2psi_dt2: float) -> tuple:
        """Return individual components (perception, reflex, intuition)"""
        return (
            sigmoid(psi_norm - self.theta),
            tanh(dpsi_dt),
            tanh(d2psi_dt2)
        )

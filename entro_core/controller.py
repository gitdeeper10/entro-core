"""
ENTRO-CORE: Closed-Loop Controller (Section V)
Seven-stage pipeline: State → Ψ → Derivatives → Normalize → Control → Actuate → Feedback
"""

from typing import Optional
from dataclasses import dataclass

from entro_core.state import StateTracker, EntropyState
from entro_core.normalize import normalize_psi, PSI_CRITICAL, NORM_REFERENCE
from entro_core.control_law import sigmoid, tanh
from entro_core.actuator import ActuationStrategy, apply_actuation


@dataclass
class ControlOutput:
    """Output of the ENTRO-CORE controller"""
    u: float                    # Raw control signal [0, 1]
    action: float               # Actuated action [0, 1]
    psi_norm: float             # Normalized Ψ
    dpsi_dt: float              # Entropy velocity
    d2psi_dt2: float            # Entropy acceleration
    perception: float           # w₁·σ(Ψ_norm - θ)
    reflex: float               # w₂·tanh(dΨ/dt)
    intuition: float            # w₃·tanh(d²Ψ/dt²)
    is_active: bool             # True if u > 0.1


class ENTROCOREController:
    """
    Complete ENTRO-CORE closed-loop controller
    
    Seven-stage pipeline:
    1. State Input - Receive raw telemetry
    2. Ψ Estimation - Compute Ψ from telemetry
    3. Derivative Computation - Calculate dΨ/dt, d²Ψ/dt²
    4. Normalization - Logistic normalization (Eq. 4)
    5. Control Law - Compute u(t) (Eq. 5)
    6. Actuation Mapping - Translate to action a(t)
    7. Feedback - Apply and loop
    """
    
    def __init__(
        self,
        w1: float = 0.5,
        w2: float = 0.3,
        w3: float = 0.2,
        theta: float = 1.4,
        psi_c: float = PSI_CRITICAL,
        norm_ref: float = NORM_REFERENCE,
        strategy: ActuationStrategy = ActuationStrategy.LINEAR
    ):
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.theta = theta
        self.psi_c = psi_c
        self.norm_ref = norm_ref
        self.strategy = strategy
        
        self.tracker = StateTracker()
        self.last_output: Optional[ControlOutput] = None
    
    def step(self, psi_raw: float, timestamp: Optional[float] = None) -> ControlOutput:
        """
        Execute one control step
        
        Args:
            psi_raw: Raw Ψ measurement from system
            timestamp: Optional timestamp
        
        Returns:
            ControlOutput with control signal and action
        """
        # Clamp input to avoid overflow
        psi_raw = max(-1000.0, min(1000.0, psi_raw))
        
        # Stage 1-3: Update state and compute derivatives
        state = self.tracker.update(psi_raw, timestamp)
        
        # Clamp derivatives to avoid overflow
        dpsi_dt = max(-10.0, min(10.0, state.dpsi_dt))
        d2psi_dt2 = max(-10.0, min(10.0, state.d2psi_dt2))
        
        # Stage 4: Normalize Ψ
        psi_norm = normalize_psi(state.psi, self.psi_c, self.norm_ref)
        
        # Stage 5: Compute control law components
        perception = sigmoid(psi_norm - self.theta)
        reflex = tanh(dpsi_dt)
        intuition = tanh(d2psi_dt2)
        
        # Stage 5: Compute u(t)
        u = (self.w1 * perception + 
             self.w2 * reflex + 
             self.w3 * intuition)
        u = max(0.0, min(1.0, u))
        
        # Stage 6: Actuation mapping
        action = apply_actuation(u, self.strategy)
        
        # Stage 7: Prepare output
        output = ControlOutput(
            u=u,
            action=action,
            psi_norm=psi_norm,
            dpsi_dt=dpsi_dt,
            d2psi_dt2=d2psi_dt2,
            perception=self.w1 * perception,
            reflex=self.w2 * reflex,
            intuition=self.w3 * intuition,
            is_active=u > 0.1
        )
        
        self.last_output = output
        return output
    
    def reset(self):
        """Reset controller state"""
        self.tracker.reset()
        self.last_output = None
    
    def get_status(self) -> dict:
        """Get current controller status"""
        if self.last_output is None:
            return {"status": "not initialized"}
        
        return {
            "u": self.last_output.u,
            "action": self.last_output.action,
            "psi_norm": self.last_output.psi_norm,
            "is_active": self.last_output.is_active,
            "strategy": self.strategy.value,
            "weights": {"w1": self.w1, "w2": self.w2, "w3": self.w3},
            "theta": self.theta
        }


# Convenience function
def create_controller(
    strategy: str = "linear",
    w1: float = 0.5,
    w2: float = 0.3,
    w3: float = 0.2,
    theta: float = 1.4
) -> ENTROCOREController:
    """Create a configured ENTRO-CORE controller"""
    strat_map = {
        "linear": ActuationStrategy.LINEAR,
        "exponential": ActuationStrategy.EXPONENTIAL,
        "quadratic": ActuationStrategy.QUADRATIC,
        "threshold": ActuationStrategy.THRESHOLD
    }
    return ENTROCOREController(
        w1=w1, w2=w2, w3=w3, theta=theta,
        strategy=strat_map.get(strategy, ActuationStrategy.LINEAR)
    )


if __name__ == "__main__":
    # Test the controller
    controller = create_controller("exponential")
    
    # Simulate a sequence of Ψ values
    psi_values = [0.5, 0.8, 1.2, 1.6, 1.9, 2.1, 1.8, 1.4, 1.1, 0.9]
    
    print("=" * 60)
    print("ENTRO-CORE Controller Test")
    print("=" * 60)
    print(f"{'Ψ_raw':>8} | {'Ψ_norm':>8} | {'u(t)':>8} | {'Action':>8} | {'Active':>6}")
    print("-" * 60)
    
    for psi in psi_values:
        out = controller.step(psi)
        print(f"{psi:8.2f} | {out.psi_norm:8.3f} | {out.u:8.3f} | {out.action:8.3f} | {out.is_active!s:6}")
    
    print("=" * 60)

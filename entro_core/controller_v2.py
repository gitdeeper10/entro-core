"""
ENTRO-CORE v2: Stabilizing Controller with Negative Feedback

u(t) = -tanh( k_p·(Ψ - Ψ*) + k_d·dΨ/dt + k_a·d²Ψ/dt² )

where:
- Ψ* = 0 (target equilibrium)
- Negative sign ensures stabilization
- Tanh provides bounded output [-1, 1] mapped to [0, 1] for actuation
"""

import math
from typing import Tuple, Optional


def sigmoid(x: float) -> float:
    """σ(x) = 1 / (1 + e⁻ˣ)"""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    exp_x = math.exp(x)
    return exp_x / (1.0 + exp_x)


def tanh(x: float) -> float:
    """Hyperbolic tangent using math.tanh"""
    return math.tanh(x)


def normalize_psi(psi_raw: float, psi_c: float = 2.0, ref: float = 10.0) -> float:
    """Logistic normalization"""
    if psi_raw <= 0:
        return 0.0
    return psi_c * (1.0 - 1.0 / (1.0 + psi_raw / ref))


class ENTROCOREControllerV2:
    """
    ENTRO-CORE v2: Stabilizing Controller
    
    u_raw = -tanh( k_p·e + k_d·e_dot + k_a·e_ddot )
    where e = Ψ - Ψ* (Ψ* = 0)
    
    The negative sign provides stabilizing negative feedback.
    """
    
    def __init__(
        self,
        kp: float = 0.8,      # Proportional gain (error)
        kd: float = 0.3,      # Derivative gain (velocity)
        ka: float = 0.1,      # Acceleration gain (intuition)
        psi_star: float = 0.0, # Target equilibrium
        use_tanh: bool = True,  # Use tanh for bounded output
        strategy: str = "linear"
    ):
        self.kp = kp
        self.kd = kd
        self.ka = ka
        self.psi_star = psi_star
        self.use_tanh = use_tanh
        self.strategy = strategy
        
        # History for derivative calculation
        self._psi_history = []
        self._timestamp_history = []
        self._max_history = 10
    
    def compute_error(self, psi: float) -> float:
        """Compute error e = Ψ - Ψ*"""
        return psi - self.psi_star
    
    def compute_control_raw(self, psi: float, dpsi: float, d2psi: float) -> float:
        """
        Compute raw control signal before activation
        
        u_raw = -( k_p·e + k_d·e_dot + k_a·e_ddot )
        """
        e = self.compute_error(psi)
        u_raw = -(self.kp * e + self.kd * dpsi + self.ka * d2psi)
        return u_raw
    
    def activate(self, u_raw: float) -> float:
        """Apply activation function and map to [0, 1]"""
        if self.use_tanh:
            # tanh outputs [-1, 1], map to [0, 1]
            u = (tanh(u_raw) + 1.0) / 2.0
        else:
            # Sigmoid maps to [0, 1] directly
            u = sigmoid(u_raw)
        
        return max(0.0, min(1.0, u))
    
    def step(self, psi_raw: float, timestamp: Optional[float] = None):
        """
        Execute one control step
        
        Returns:
            Object with u (control signal), action, is_active
        """
        import time
        if timestamp is None:
            timestamp = time.time()
        
        # Normalize Ψ (optional - can use raw or normalized)
        psi = normalize_psi(psi_raw)  # Use normalized for consistent scale
        
        # Update history
        self._psi_history.append(psi)
        self._timestamp_history.append(timestamp)
        
        if len(self._psi_history) > self._max_history:
            self._psi_history = self._psi_history[-self._max_history:]
            self._timestamp_history = self._timestamp_history[-self._max_history:]
        
        # Compute derivatives
        dpsi = 0.0
        d2psi = 0.0
        
        if len(self._psi_history) >= 2:
            dt = self._timestamp_history[-1] - self._timestamp_history[-2]
            if dt > 0:
                dpsi = (self._psi_history[-1] - self._psi_history[-2]) / dt
        
        if len(self._psi_history) >= 3:
            dt = self._timestamp_history[-1] - self._timestamp_history[-2]
            if dt > 0:
                prev_dpsi = (self._psi_history[-2] - self._psi_history[-3]) / dt
                d2psi = (dpsi - prev_dpsi) / dt
        
        # Compute control
        u_raw = self.compute_control_raw(psi, dpsi, d2psi)
        u = self.activate(u_raw)
        
        # Apply actuation strategy
        if self.strategy == "exponential":
            action = 1.0 - math.exp(-5.0 * u)
        elif self.strategy == "quadratic":
            action = u * u
        elif self.strategy == "threshold":
            action = 0.0 if u < 0.3 else u
        else:  # linear
            action = u
        
        class Result:
            pass
        
        result = Result()
        result.u = u
        result.action = action
        result.is_active = u > 0.1
        result.psi_norm = psi
        result.dpsi = dpsi
        result.d2psi = d2psi
        result.u_raw = u_raw
        
        return result
    
    def reset(self):
        """Reset controller history"""
        self._psi_history = []
        self._timestamp_history = []


def create_controller_v2(strategy: str = "linear", kp: float = 0.8, kd: float = 0.3, ka: float = 0.1) -> ENTROCOREControllerV2:
    """Factory function for ENTRO-CORE v2 controller"""
    return ENTROCOREControllerV2(kp=kp, kd=kd, ka=ka, strategy=strategy)


if __name__ == "__main__":
    # Quick test
    controller = create_controller_v2("linear")
    
    print("=" * 50)
    print("ENTRO-CORE v2 Quick Test")
    print("=" * 50)
    
    test_psi = [0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 1.8, 1.5, 1.2, 1.0, 0.8, 0.5]
    
    print(f"{'Ψ':>8} | {'u(t)':>8} | {'Action':>8} | {'Active':>6}")
    print("-" * 40)
    
    for psi in test_psi:
        result = controller.step(psi)
        print(f"{psi:8.2f} | {result.u:8.3f} | {result.action:8.3f} | {result.is_active!s:6}")
    
    print("=" * 50)

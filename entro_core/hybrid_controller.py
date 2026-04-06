"""
ENTRO-CORE Hybrid Controller: Regime-Switching Control

u = { u_PID if Ψ < Ψ_threshold
    { u_ENTRO if Ψ >= Ψ_threshold

This combines the strengths of both controllers:
- PID: optimal for normal operation (Ψ small)
- ENTRO-CORE: prevents collapse in critical regime (Ψ near Ψ_c)
"""

import math
from entro_core.controller import create_controller as create_entro_v1
from entro_core.controller_v2 import create_controller_v2


class PIDController:
    """Simple PID for baseline comparison"""
    def __init__(self, dt=0.1, kp=0.8, ki=0.2, kd=0.3):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.integral = 0.0
        self.prev_error = 0.0
    
    def step(self, psi):
        error = -psi
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        u = self.kp * error + self.ki * self.integral + self.kd * derivative
        u = max(0.0, min(1.0, u))
        self.prev_error = error
        
        class Result:
            pass
        result = Result()
        result.u = u
        result.action = u
        result.is_active = u > 0.1
        return result
    
    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0


class HybridController:
    """
    Regime-switching controller:
    - Uses PID for normal operation (Ψ < threshold)
    - Uses ENTRO-CORE v1 for critical regime (Ψ >= threshold)
    """
    
    def __init__(self, threshold: float = 1.5, dt: float = 0.1):
        self.threshold = threshold
        self.pid = PIDController(dt=dt)
        self.entro = create_entro_v1("exponential")
        self.current_mode = "PID"
        self.last_psi = 0.0
    
    def step(self, psi_raw):
        """Execute one control step with regime switching"""
        
        # Decide which controller to use
        if psi_raw < self.threshold:
            self.current_mode = "PID"
            result = self.pid.step(psi_raw)
        else:
            self.current_mode = "ENTRO-CORE"
            result = self.entro.step(psi_raw)
        
        # Store for analysis
        result.mode = self.current_mode
        result.psi = psi_raw
        
        return result
    
    def reset(self):
        self.pid.reset()
        self.entro.reset()
        self.current_mode = "PID"


def create_hybrid_controller(threshold: float = 1.5) -> HybridController:
    """Factory function for hybrid controller"""
    return HybridController(threshold=threshold)


if __name__ == "__main__":
    # Quick test
    controller = create_hybrid_controller(threshold=1.5)
    
    print("=" * 50)
    print("Hybrid Controller Test")
    print("=" * 50)
    
    test_values = [0.5, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 1.8, 1.5, 1.2, 1.0, 0.8]
    
    print(f"{'Ψ':>8} | {'Mode':>12} | {'u(t)':>8}")
    print("-" * 35)
    
    for psi in test_values:
        result = controller.step(psi)
        print(f"{psi:8.2f} | {result.mode:12} | {result.u:8.3f}")
    
    print("=" * 50)

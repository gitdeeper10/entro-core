"""
ENTRO-CORE: System Dynamics Simulation - FIXED VERSION
المشكلة كانت في توقيت تحديث Ψ و u(t)
"""

import sys
import os
import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entro_core.controller import create_controller


@dataclass
class SimulationConfig:
    gamma: float = 0.3
    k: float = 0.5
    noise_std: float = 0.05
    dt: float = 0.1
    duration: float = 50.0
    psi_0: float = 1.0
    dpsi_0: float = 0.2


class SystemDynamics:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.reset()
    
    def reset(self):
        self.t = 0.0
        self.psi = self.config.psi_0
        self.dpsi = self.config.dpsi_0
        self.history = []
    
    def step(self, u: float) -> Tuple[float, float, float]:
        dt = self.config.dt
        noise = random.gauss(0, self.config.noise_std)
        
        # d²Ψ/dt² = −γ·dΨ/dt − k·Ψ + u + noise
        d2psi = (-self.config.gamma * self.dpsi - 
                 self.config.k * self.psi + u + noise)
        
        self.dpsi += d2psi * dt
        self.psi += self.dpsi * dt
        self.t += dt
        
        # Clamp
        self.psi = max(-3.0, min(5.0, self.psi))
        self.dpsi = max(-3.0, min(3.0, self.dpsi))
        
        self.history.append((self.t, self.psi, self.dpsi, u))
        
        return self.t, self.psi, self.dpsi


def simulate(controller, name: str, config: SimulationConfig = None) -> dict:
    if config is None:
        config = SimulationConfig()
    
    system = SystemDynamics(config)
    times = [0.0]
    psi_vals = [config.psi_0]
    dpsi_vals = [config.dpsi_0]
    u_vals = [0.0]
    
    num_steps = int(config.duration / config.dt)
    
    for _ in range(num_steps):
        # Get control signal from current psi
        result = controller.step(system.psi)
        u = result.u
        
        t, psi, dpsi = system.step(u)
        
        times.append(t)
        psi_vals.append(psi)
        dpsi_vals.append(dpsi)
        u_vals.append(u)
    
    # Calculate metrics
    iae = sum(abs(p) * config.dt for p in psi_vals)
    control_effort = sum(abs(u) for u in u_vals) * config.dt
    peak_psi = max(psi_vals)
    
    # Settling time (within ±0.2)
    settling_time = config.duration
    for i in range(len(psi_vals)):
        if all(abs(psi_vals[i + j]) <= 0.2 for j in range(min(20, len(psi_vals)-i-1))):
            settling_time = times[i]
            break
    
    return {
        "name": name,
        "IAE": iae,
        "control_effort": control_effort,
        "peak_psi": peak_psi,
        "settling_time": settling_time,
        "times": times,
        "psi": psi_vals,
        "u": u_vals
    }


class UncontrolledController:
    def step(self, psi):
        class Dummy:
            u = 0.0
            action = 0.0
            is_active = False
        return Dummy()


class PIDController:
    def __init__(self, dt):
        self.kp = 0.8
        self.ki = 0.2
        self.kd = 0.3
        self.dt = dt
        self.integral = 0.0
        self.prev_error = 0.0
    
    def step(self, psi):
        error = -psi  # Target = 0
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt if self.dt > 0 else 0
        u = self.kp * error + self.ki * self.integral + self.kd * derivative
        u = max(0.0, min(1.0, u))
        self.prev_error = error
        
        class Dummy:
            pass
        result = Dummy()
        result.u = u
        result.action = u
        result.is_active = u > 0.1
        return result


def main():
    config = SimulationConfig(duration=50.0, dt=0.1)
    
    print("=" * 60)
    print("ENTRO-CORE Simulation (Fixed)")
    print("=" * 60)
    print(f"Duration: {config.duration}s, dt={config.dt}s")
    print(f"Initial: Ψ(0)={config.psi_0}, dΨ/dt(0)={config.dpsi_0}")
    print()
    
    results = []
    
    # 1. Uncontrolled
    print("Running: Uncontrolled...")
    results.append(simulate(UncontrolledController(), "Uncontrolled", config))
    
    # 2. PID
    print("Running: PID...")
    pid = PIDController(config.dt)
    results.append(simulate(pid, "PID", config))
    
    # 3. ENTRO-CORE variants
    for strategy in ["linear", "exponential", "quadratic"]:
        print(f"Running: ENTRO-CORE ({strategy})...")
        controller = create_controller(strategy)
        results.append(simulate(controller, f"ENTRO-CORE ({strategy})", config))
    
    print()
    print("=" * 80)
    print("PERFORMANCE METRICS COMPARISON")
    print("=" * 80)
    print(f"{'Controller':<25} {'IAE':>10} {'Control Effort':>14} {'Peak Ψ':>10} {'Settling Time':>14}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['name']:<25} {r['IAE']:10.3f} {r['control_effort']:14.3f} {r['peak_psi']:10.3f} {r['settling_time']:14.2f}s")
    
    print("=" * 80)
    
    # Find best
    best = min(results, key=lambda x: x['IAE'])
    print(f"\n✅ Best controller by IAE: {best['name']} (IAE={best['IAE']:.3f})")


if __name__ == "__main__":
    main()

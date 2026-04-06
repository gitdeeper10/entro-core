"""
ENTRO-CORE: System Dynamics Simulation (Eq. 8)
d²Ψ/dt² = −γ·dΨ/dt − k·Ψ + u(t) + ξ(t)
Without numpy - pure Python
"""

import math
import random
import csv
from typing import List, Tuple, Dict
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entro_core.controller import create_controller


@dataclass
class SimulationConfig:
    gamma: float = 0.3
    k: float = 0.5
    noise_std: float = 0.1
    dt: float = 0.1
    duration: float = 50.0
    psi_0: float = 1.0
    dpsi_0: float = 0.2


@dataclass
class SimulationResult:
    times: List[float]
    psi: List[float]
    dpsi: List[float]
    u: List[float]
    action: List[float]
    controller_name: str
    metrics: Dict[str, float]


class SystemDynamics:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.reset()
    
    def reset(self):
        self.t = 0.0
        self.psi = self.config.psi_0
        self.dpsi = self.config.dpsi_0
        self.history_t = [0.0]
        self.history_psi = [self.psi]
        self.history_dpsi = [self.dpsi]
    
    def step(self, u: float) -> Tuple[float, float, float]:
        dt = self.config.dt
        # d²Ψ/dt² = −γ·dΨ/dt − k·Ψ + u + noise
        noise = random.gauss(0, self.config.noise_std)
        d2psi = (-self.config.gamma * self.dpsi - 
                 self.config.k * self.psi + u + noise)
        
        self.dpsi += d2psi * dt
        self.psi += self.dpsi * dt
        self.t += dt
        
        # Clamp
        self.psi = max(-5.0, min(10.0, self.psi))
        self.dpsi = max(-5.0, min(5.0, self.dpsi))
        
        self.history_t.append(self.t)
        self.history_psi.append(self.psi)
        self.history_dpsi.append(self.dpsi)
        
        return self.t, self.psi, self.dpsi
    
    def get_history(self):
        return self.history_t, self.history_psi, self.history_dpsi


def simulate_controller(controller, controller_name: str, config: SimulationConfig = None) -> SimulationResult:
    if config is None:
        config = SimulationConfig()
    
    system = SystemDynamics(config)
    times = [0.0]
    psi_vals = [config.psi_0]
    dpsi_vals = [config.dpsi_0]
    u_vals = [0.0]
    action_vals = [0.0]
    
    num_steps = int(config.duration / config.dt)
    
    for step in range(num_steps):
        result = controller.step(system.psi)
        u = result.u
        action = result.action
        
        t, psi, dpsi = system.step(u)
        
        times.append(t)
        psi_vals.append(psi)
        dpsi_vals.append(dpsi)
        u_vals.append(u)
        action_vals.append(action)
    
    # Calculate metrics
    iae = sum(abs(p) * config.dt for p in psi_vals)
    control_effort = sum(abs(u) for u in u_vals) * config.dt
    peak_psi = max(psi_vals)
    
    overshoot = 0.0
    for p in psi_vals:
        if p > 1.0:
            overshoot = max(overshoot, p - 1.0)
    
    # Settling time (within ±0.2)
    settling_time = config.duration
    window = int(2.0 / config.dt)
    for i in range(len(psi_vals) - window):
        if all(abs(psi_vals[i + j]) <= 0.2 for j in range(window)):
            settling_time = times[i]
            break
    
    metrics = {
        "IAE": iae,
        "control_effort": control_effort,
        "peak_psi": peak_psi,
        "overshoot": overshoot,
        "settling_time": settling_time
    }
    
    return SimulationResult(
        times=times, psi=psi_vals, dpsi=dpsi_vals,
        u=u_vals, action=action_vals,
        controller_name=controller_name, metrics=metrics
    )


def simulate_uncontrolled(config: SimulationConfig = None) -> SimulationResult:
    class DummyController:
        def step(self, psi):
            class Dummy:
                u = 0.0
                action = 0.0
                is_active = False
            return Dummy()
    return simulate_controller(DummyController(), "Uncontrolled", config)


def simulate_pid(config: SimulationConfig = None) -> SimulationResult:
    class PIDController:
        def __init__(self, kp, ki, kd, dt):
            self.kp = kp
            self.ki = ki
            self.kd = kd
            self.dt = dt
            self.integral = 0.0
            self.prev_error = 0.0
        
        def step(self, psi):
            error = -psi
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
    
    if config is None:
        config = SimulationConfig()
    
    pid = PIDController(kp=0.8, ki=0.2, kd=0.3, dt=config.dt)
    return simulate_controller(pid, "PID", config)


def run_comparison(config: SimulationConfig = None):
    if config is None:
        config = SimulationConfig()
    
    print("=" * 60)
    print("ENTRO-CORE Simulation Comparison")
    print("=" * 60)
    print(f"Duration: {config.duration}s, dt={config.dt}s")
    print(f"Initial: Ψ(0)={config.psi_0}, dΨ/dt(0)={config.dpsi_0}")
    print()
    
    results = {}
    
    print("Running: Uncontrolled...")
    results["uncontrolled"] = simulate_uncontrolled(config)
    
    print("Running: PID...")
    results["pid"] = simulate_pid(config)
    
    print("Running: ENTRO-CORE (Linear)...")
    results["entro_core_linear"] = simulate_controller(create_controller("linear"), "ENTRO-CORE (Linear)", config)
    
    print("Running: ENTRO-CORE (Exponential)...")
    results["entro_core_exp"] = simulate_controller(create_controller("exponential"), "ENTRO-CORE (Exponential)", config)
    
    print("Running: ENTRO-CORE (Quadratic)...")
    results["entro_core_quad"] = simulate_controller(create_controller("quadratic"), "ENTRO-CORE (Quadratic)", config)
    
    print()
    return results


def print_metrics_table(results):
    print("=" * 80)
    print("PERFORMANCE METRICS COMPARISON")
    print("=" * 80)
    print(f"{'Controller':<25} {'IAE':>10} {'Control Effort':>14} {'Peak Ψ':>10} {'Settling Time':>14}")
    print("-" * 80)
    
    for name, result in results.items():
        m = result.metrics
        print(f"{result.controller_name:<25} {m['IAE']:10.3f} {m['control_effort']:14.3f} {m['peak_psi']:10.3f} {m['settling_time']:14.2f}s")
    
    print("=" * 80)


def export_to_csv(results, filename="simulation/results/comparison.csv"):
    import os
    os.makedirs("simulation/results", exist_ok=True)
    
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["controller", "time", "psi", "dpsi", "u", "action"])
        for name, result in results.items():
            for t, psi, dpsi, u, action in zip(result.times, result.psi, result.dpsi, result.u, result.action):
                writer.writerow([result.controller_name, t, psi, dpsi, u, action])
    
    print(f"✅ Exported to {filename}")


if __name__ == "__main__":
    config = SimulationConfig(duration=50.0, dt=0.1)
    results = run_comparison(config)
    print_metrics_table(results)
    export_to_csv(results)

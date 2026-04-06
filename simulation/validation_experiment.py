"""
ENTRO-CORE: Validation Experiment
Comparison: Uncontrolled vs PID vs ENTRO-CORE

System Dynamics (Explicit Definition):
d²Ψ/dt² = −γ·dΨ/dt − k·Ψ + u(t) + ξ(t)
"""

import sys
import os
import math
import random
from dataclasses import dataclass, field
from typing import List, Tuple, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entro_core.controller import create_controller


@dataclass
class ExperimentConfig:
    """Experimental configuration"""
    duration: float = 30.0      # seconds
    dt: float = 0.1             # time step
    gamma: float = 0.3          # damping
    k: float = 0.5              # restoring force
    noise_std: float = 0.05     # process noise
    psi_0: float = 1.0          # initial Ψ
    dpsi_0: float = 0.2         # initial dΨ/dt


class DynamicalSystem:
    """Second-order dynamical system: d²Ψ/dt² = −γ·dΨ/dt − k·Ψ + u + ξ"""
    
    def __init__(self, config: ExperimentConfig):
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
        
        # d²Ψ/dt² = −γ·dΨ/dt − k·Ψ + u + ξ
        d2psi = (-self.config.gamma * self.dpsi - 
                 self.config.k * self.psi + u + noise)
        
        self.dpsi += d2psi * dt
        self.psi += self.dpsi * dt
        self.t += dt
        
        # Bounds
        self.psi = max(-2.0, min(4.0, self.psi))
        self.dpsi = max(-3.0, min(3.0, self.dpsi))
        
        self.history.append((self.t, self.psi, self.dpsi, u))
        return self.t, self.psi, self.dpsi
    
    def get_trajectory(self) -> Tuple[List[float], List[float], List[float]]:
        times = [h[0] for h in self.history]
        psi_vals = [h[1] for h in self.history]
        u_vals = [h[3] for h in self.history]
        return times, psi_vals, u_vals


class UncontrolledController:
    def step(self, psi):
        class Dummy:
            u = 0.0
            action = 0.0
            is_active = False
        return Dummy()


class PIDController:
    def __init__(self, dt: float, kp: float = 0.8, ki: float = 0.2, kd: float = 0.3):
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


def run_single_run(controller, config: ExperimentConfig) -> Dict:
    """Run single experiment and return metrics"""
    system = DynamicalSystem(config)
    
    if hasattr(controller, 'reset'):
        controller.reset()
    
    num_steps = int(config.duration / config.dt)
    
    for _ in range(num_steps):
        result = controller.step(system.psi)
        system.step(result.u)
    
    times, psi_vals, u_vals = system.get_trajectory()
    
    # Metrics
    iae = sum(abs(p) * config.dt for p in psi_vals)
    control_effort = sum(abs(u) for u in u_vals) * config.dt
    peak_psi = max(psi_vals)
    
    # Settling time (within ±0.2)
    settling_time = config.duration
    for i, p in enumerate(psi_vals):
        window = min(20, len(psi_vals) - i - 1)
        if window > 0 and all(abs(psi_vals[i + j]) <= 0.2 for j in range(window)):
            settling_time = times[i]
            break
    
    return {
        "IAE": iae,
        "control_effort": control_effort,
        "peak_psi": peak_psi,
        "settling_time": settling_time,
        "final_psi": psi_vals[-1] if psi_vals else 0,
        "trajectory": (times, psi_vals, u_vals)
    }


def run_validation_experiment(n_runs: int = 5) -> List[Dict]:
    """Run multiple runs for statistical significance"""
    config = ExperimentConfig(duration=30.0, dt=0.1)
    
    print("=" * 70)
    print("ENTRO-CORE VALIDATION EXPERIMENT")
    print("=" * 70)
    print(f"Duration: {config.duration}s, dt={config.dt}s")
    print(f"Initial: Ψ(0)={config.psi_0}, dΨ/dt(0)={config.dpsi_0}")
    print(f"System: d²Ψ/dt² = −{config.gamma}·dΨ/dt − {config.k}·Ψ + u + ξ")
    print(f"Noise: σ={config.noise_std}")
    print(f"Runs per controller: {n_runs}")
    print()
    
    controllers = [
        ("Uncontrolled", lambda: UncontrolledController()),
        ("PID", lambda: PIDController(config.dt)),
        ("ENTRO-CORE (Linear)", lambda: create_controller("linear")),
        ("ENTRO-CORE (Exponential)", lambda: create_controller("exponential")),
        ("ENTRO-CORE (Quadratic)", lambda: create_controller("quadratic")),
    ]
    
    all_results = []
    
    for name, controller_factory in controllers:
        print(f"Running: {name}...")
        run_results = []
        
        for run in range(n_runs):
            random.seed(run)
            controller = controller_factory()
            result = run_single_run(controller, config)
            run_results.append(result)
        
        # Aggregate metrics
        iae_values = [r["IAE"] for r in run_results]
        effort_values = [r["control_effort"] for r in run_results]
        peak_values = [r["peak_psi"] for r in run_results]
        settling_values = [r["settling_time"] for r in run_results]
        
        avg_iae = sum(iae_values) / n_runs
        std_iae = math.sqrt(sum((v - avg_iae)**2 for v in iae_values) / n_runs)
        avg_effort = sum(effort_values) / n_runs
        avg_peak = sum(peak_values) / n_runs
        avg_settling = sum(settling_values) / n_runs
        
        all_results.append({
            "name": name,
            "IAE_mean": avg_iae,
            "IAE_std": std_iae,
            "control_effort_mean": avg_effort,
            "peak_psi_mean": avg_peak,
            "settling_time_mean": avg_settling,
            "raw_results": run_results
        })
        
        print(f"  IAE: {avg_iae:.3f} ± {std_iae:.3f}")
        print(f"  Settling: {avg_settling:.2f}s")
    
    print()
    return all_results


def print_comparison_table(results: List[Dict]):
    """Print formatted comparison table"""
    print("=" * 80)
    print("PERFORMANCE METRICS COMPARISON (mean ± std)")
    print("=" * 80)
    print(f"{'Controller':<25} {'IAE':>12} {'Control Effort':>14} {'Peak Ψ':>10} {'Settling Time':>14}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['name']:<25} {r['IAE_mean']:10.3f} ± {r['IAE_std']:.3f} "
              f"{r['control_effort_mean']:14.3f} "
              f"{r['peak_psi_mean']:10.3f} "
              f"{r['settling_time_mean']:14.2f}s")
    
    print("=" * 80)
    
    # Find best by IAE
    best = min(results, key=lambda x: x['IAE_mean'])
    print(f"\n✅ Best controller by IAE: {best['name']} (IAE={best['IAE_mean']:.3f})")
    
    # Improvement calculation
    uncontrolled = next(r for r in results if r['name'] == "Uncontrolled")
    improvement = (uncontrolled['IAE_mean'] - best['IAE_mean']) / uncontrolled['IAE_mean'] * 100
    print(f"📈 Improvement over uncontrolled: {improvement:.1f}%")


def export_trajectory_csv(results: List[Dict], filename: str = "simulation/results/trajectories.csv"):
    """Export trajectories for plotting"""
    import os
    os.makedirs("simulation/results", exist_ok=True)
    
    with open(filename, 'w') as f:
        f.write("controller,time,psi,u\n")
        for r in results:
            if r['raw_results']:
                times, psi_vals, u_vals = r['raw_results'][0]['trajectory']
                for t, psi, u in zip(times, psi_vals, u_vals):
                    f.write(f"{r['name']},{t},{psi},{u}\n")
    
    print(f"✅ Trajectories exported to {filename}")


def main():
    results = run_validation_experiment(n_runs=5)
    print_comparison_table(results)
    export_trajectory_csv(results)
    
    print("\n" + "=" * 80)
    print("✅ VALIDATION EXPERIMENT COMPLETE")
    print("=" * 80)
    print("\n📊 Interpretation:")
    print("  - Lower IAE = better regulation")
    print("  - Lower settling time = faster response")
    print("  - Lower control effort = more efficient")
    print("=" * 80)


if __name__ == "__main__":
    main()

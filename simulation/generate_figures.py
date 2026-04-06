"""
Generate comparison figures for hybrid controller validation
Outputs CSV data that can be plotted externally or used in LaTeX
"""

import sys
import os
import random
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entro_core.hybrid_controller import HybridController, PIDController
from entro_core.controller import create_controller


class CriticalSystem:
    def __init__(self, psi_0=1.8, dpsi_0=0.3, noise_std=0.0):
        self.psi = psi_0
        self.dpsi = dpsi_0
        self.t = 0.0
        self.noise_std = noise_std
        self.history = []
    
    def step(self, u, dt=0.1):
        noise = random.gauss(0, self.noise_std) if self.noise_std > 0 else 0
        d2psi = -0.2 * self.dpsi + 0.1 * (2.0 - self.psi) + u + noise
        self.dpsi += d2psi * dt
        self.psi += self.dpsi * dt
        self.t += dt
        self.psi = max(-0.5, min(3.0, self.psi))
        self.history.append((self.t, self.psi, u))
        return self.psi
    
    def get_trajectory(self):
        times = [h[0] for h in self.history]
        psi_vals = [h[1] for h in self.history]
        return times, psi_vals


def run_simulation(controller, name, psi_0=1.8, duration=20.0, dt=0.1, noise_std=0.0):
    """Run simulation and return trajectory"""
    system = CriticalSystem(psi_0=psi_0, noise_std=noise_std)
    
    if hasattr(controller, 'reset'):
        controller.reset()
    
    steps = int(duration / dt)
    for _ in range(steps):
        result = controller.step(system.psi)
        system.step(result.u, dt)
    
    return system.get_trajectory()


def generate_comparison_data(filename="simulation/results/trajectories_comparison.csv"):
    """Generate CSV with trajectories for all controllers"""
    import os
    os.makedirs("simulation/results", exist_ok=True)
    
    # Initialize controllers
    controllers = {
        "Uncontrolled": None,
        "PID Only": PIDController(dt=0.1),
        "ENTRO-CORE v1": create_controller("exponential"),
        "Hybrid (threshold=1.7)": HybridController(threshold=1.7),
    }
    
    print("=" * 60)
    print("Generating comparison trajectories...")
    print("=" * 60)
    
    all_trajectories = {}
    
    for name, controller in controllers.items():
        print(f"  Running: {name}...")
        if controller is None:
            # Uncontrolled
            system = CriticalSystem(psi_0=1.8)
            steps = int(20.0 / 0.1)
            for _ in range(steps):
                system.step(0.0)
            times, psi_vals = system.get_trajectory()
        else:
            times, psi_vals = run_simulation(controller, name, psi_0=1.8, duration=20.0)
        
        all_trajectories[name] = (times, psi_vals)
    
    # Write CSV
    with open(filename, 'w') as f:
        f.write("time,uncontrolled,pid,entro_core,hybrid\n")
        
        # Find max length
        max_len = max(len(t) for t, _ in all_trajectories.values())
        
        for i in range(max_len):
            time_val = all_trajectories["Uncontrolled"][0][i] if i < len(all_trajectories["Uncontrolled"][0]) else ""
            uncontrolled_val = all_trajectories["Uncontrolled"][1][i] if i < len(all_trajectories["Uncontrolled"][1]) else ""
            pid_val = all_trajectories["PID Only"][1][i] if i < len(all_trajectories["PID Only"][1]) else ""
            entro_val = all_trajectories["ENTRO-CORE v1"][1][i] if i < len(all_trajectories["ENTRO-CORE v1"][1]) else ""
            hybrid_val = all_trajectories["Hybrid (threshold=1.7)"][1][i] if i < len(all_trajectories["Hybrid (threshold=1.7)"][1]) else ""
            
            f.write(f"{time_val},{uncontrolled_val},{pid_val},{entro_val},{hybrid_val}\n")
    
    print(f"\n✅ Trajectories saved to {filename}")
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("FINAL VALUES (t = 20s)")
    print("=" * 60)
    for name, (times, psi_vals) in all_trajectories.items():
        final_psi = psi_vals[-1] if psi_vals else 0
        print(f"  {name:25} → Ψ_final = {final_psi:.3f}")
    print("=" * 60)
    
    return all_trajectories


def generate_noise_sensitivity_data():
    """Test hybrid controller under different noise levels"""
    print("\n" + "=" * 60)
    print("NOISE SENSITIVITY ANALYSIS")
    print("=" * 60)
    
    noise_levels = [0.0, 0.02, 0.05, 0.1, 0.15]
    hybrid = HybridController(threshold=1.7)
    
    results = []
    
    for noise in noise_levels:
        system = CriticalSystem(psi_0=1.8, noise_std=noise)
        hybrid.reset()
        
        steps = int(20.0 / 0.1)
        for _ in range(steps):
            result = hybrid.step(system.psi)
            system.step(result.u)
        
        final_psi = system.psi
        results.append((noise, final_psi))
        print(f"  Noise σ = {noise:.2f} → Final Ψ = {final_psi:.3f}")
    
    print("=" * 60)
    return results


if __name__ == "__main__":
    generate_comparison_data()
    generate_noise_sensitivity_data()

"""
Fixed simulation for hybrid controller validation
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
        # نموذج أبسط وأكثر استقراراً
        d2psi = -0.3 * self.dpsi - 0.5 * (self.psi - 0) + u + noise
        self.dpsi += d2psi * dt
        self.psi += self.dpsi * dt
        self.t += dt
        # حدود أوسع
        self.psi = max(-1.0, min(3.0, self.psi))
        self.dpsi = max(-2.0, min(2.0, self.dpsi))
        self.history.append((self.t, self.psi, u))
        return self.psi
    
    def get_trajectory(self):
        times = [h[0] for h in self.history]
        psi_vals = [h[1] for h in self.history]
        return times, psi_vals


def run_simulation(controller, name, psi_0=1.8, duration=20.0, dt=0.1, noise_std=0.0):
    system = CriticalSystem(psi_0=psi_0, noise_std=noise_std)
    
    if hasattr(controller, 'reset'):
        controller.reset()
    
    steps = int(duration / dt)
    for _ in range(steps):
        result = controller.step(system.psi)
        system.step(result.u, dt)
    
    return system.get_trajectory()


def main():
    import os
    os.makedirs("simulation/results", exist_ok=True)
    
    controllers = {
        "Uncontrolled": None,
        "PID Only": PIDController(dt=0.1),
        "ENTRO-CORE v1": create_controller("exponential"),
        "Hybrid (threshold=1.7)": HybridController(threshold=1.7),
    }
    
    print("=" * 60)
    print("Generating comparison trajectories (FIXED)...")
    print("=" * 60)
    
    results = {}
    
    for name, controller in controllers.items():
        print(f"  Running: {name}...")
        if controller is None:
            system = CriticalSystem(psi_0=1.8)
            steps = int(20.0 / 0.1)
            for _ in range(steps):
                system.step(0.0)
            times, psi_vals = system.get_trajectory()
        else:
            times, psi_vals = run_simulation(controller, name, psi_0=1.8, duration=20.0)
        
        results[name] = (times, psi_vals)
    
    # Write CSV
    with open("simulation/results/trajectories_fixed.csv", 'w') as f:
        f.write("time,uncontrolled,pid,entro_core,hybrid\n")
        
        max_len = max(len(t) for t, _ in results.values())
        
        for i in range(max_len):
            time_val = results["Uncontrolled"][0][i] if i < len(results["Uncontrolled"][0]) else ""
            uncontrolled_val = results["Uncontrolled"][1][i] if i < len(results["Uncontrolled"][1]) else ""
            pid_val = results["PID Only"][1][i] if i < len(results["PID Only"][1]) else ""
            entro_val = results["ENTRO-CORE v1"][1][i] if i < len(results["ENTRO-CORE v1"][1]) else ""
            hybrid_val = results["Hybrid (threshold=1.7)"][1][i] if i < len(results["Hybrid (threshold=1.7)"][1]) else ""
            
            f.write(f"{time_val},{uncontrolled_val},{pid_val},{entro_val},{hybrid_val}\n")
    
    print("\n✅ Trajectories saved to simulation/results/trajectories_fixed.csv")
    
    # Print final values
    print("\n" + "=" * 60)
    print("FINAL VALUES (t = 20s)")
    print("=" * 60)
    for name, (times, psi_vals) in results.items():
        final_psi = psi_vals[-1] if psi_vals else 0
        print(f"  {name:25} → Ψ_final = {final_psi:.3f}")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
اختبار الـ Hybrid Controller في السيناريو الحرج
"""

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entro_core.hybrid_controller import HybridController, PIDController
from entro_core.controller import create_controller


class CriticalSystem:
    def __init__(self, psi_0=1.8, dpsi_0=0.3):
        self.psi = psi_0
        self.dpsi = dpsi_0
        self.t = 0.0
    
    def step(self, u, dt=0.1):
        d2psi = -0.2 * self.dpsi + 0.1 * (2.0 - self.psi) + u
        self.dpsi += d2psi * dt
        self.psi += self.dpsi * dt
        self.t += dt
        return self.psi


def run_test(controller, name):
    system = CriticalSystem(psi_0=1.8, dpsi_0=0.3)
    
    for _ in range(200):
        result = controller.step(system.psi)
        system.step(result.u)
    
    return system.psi


print("=" * 60)
print("HYBRID CONTROLLER TEST - Critical Scenario")
print("Ψ₀ = 1.8, near collapse")
print("=" * 60)

# Test different controllers
controllers = {
    "PID Only": PIDController(dt=0.1),
    "ENTRO-CORE v1": create_controller("exponential"),
    "Hybrid (threshold=1.5)": HybridController(threshold=1.5),
    "Hybrid (threshold=1.3)": HybridController(threshold=1.3),
    "Hybrid (threshold=1.7)": HybridController(threshold=1.7),
}

results = {}

for name, controller in controllers.items():
    final_psi = run_test(controller, name)
    results[name] = final_psi
    print(f"{name:25} → Final Ψ = {final_psi:.3f}")

print("=" * 60)
print("\n📊 Best result:", min(results, key=lambda x: results[x]))
print("=" * 60)

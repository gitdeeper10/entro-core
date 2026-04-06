"""
اختبار ENTRO-CORE في سيناريو حرج: Ψ قريب من الانهيار
"""

import sys
import os
import math
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entro_core.controller import create_controller
from entro_core.controller_v2 import create_controller_v2
from entro_core.normalize import normalize_psi


class CriticalSystem:
    """نظام يبدأ قريباً من الانهيار"""
    
    def __init__(self, psi_0=1.8, dpsi_0=0.3):
        self.psi = psi_0
        self.dpsi = dpsi_0
        self.t = 0.0
        self.history = []
    
    def step(self, u, dt=0.1):
        # نموذج مبسط: Ψ يتجه نحو 2.0 بدون تحكم
        d2psi = -0.2 * self.dpsi + 0.1 * (2.0 - self.psi) + u
        self.dpsi += d2psi * dt
        self.psi += self.dpsi * dt
        self.t += dt
        self.history.append((self.t, self.psi, u))
        return self.psi


print("=" * 60)
print("ENTRO-CORE: CRITICAL SCENARIO TEST")
print("Ψ starts near collapse (1.8)")
print("=" * 60)

# controllers
controllers = {
    "No Control": None,
    "PID": None,  # سنضيف لاحقاً
    "ENTRO-CORE v1": create_controller("exponential"),
    "ENTRO-CORE v2": create_controller_v2("exponential", kp=1.0, kd=0.5, ka=0.2)
}

results = {}

for name, controller in controllers.items():
    if controller is None:
        system = CriticalSystem(psi_0=1.8, dpsi_0=0.3)
        for _ in range(200):
            system.step(0)
        final_psi = system.psi
        results[name] = final_psi
        print(f"{name:20} → Final Ψ = {final_psi:.3f}")
    else:
        system = CriticalSystem(psi_0=1.8, dpsi_0=0.3)
        for _ in range(200):
            result = controller.step(system.psi)
            system.step(result.u)
        final_psi = system.psi
        results[name] = final_psi
        print(f"{name:20} → Final Ψ = {final_psi:.3f}")

print("=" * 60)
print("\n📊 Interpretation:")
print("  - Without control: Ψ → 2.0 (collapse)")
print("  - With ENTRO-CORE: Should prevent collapse")
print("=" * 60)

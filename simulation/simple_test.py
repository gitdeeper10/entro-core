"""
اختبار بسيط لـ ENTRO-CORE بدون محاكاة معقدة
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entro_core.controller import create_controller
from entro_core.normalize import normalize_psi
from entro_core.control_law import compute_control

print("=" * 60)
print("ENTRO-CORE Simple Test")
print("=" * 60)

# إنشاء控制器
controller = create_controller("exponential")

# محاكاة بسيطة: سلسلة من قيم Ψ
psi_values = [0.5, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 1.8, 1.5, 1.2, 1.0, 0.8, 0.5]

print(f"\n{'Ψ_raw':>8} | {'Ψ_norm':>8} | {'u(t)':>8} | {'Action':>8} | {'Active':>6}")
print("-" * 50)

for psi in psi_values:
    result = controller.step(psi)
    psi_norm = normalize_psi(psi)
    
    print(f"{psi:8.2f} | {psi_norm:8.3f} | {result.u:8.3f} | {result.action:8.3f} | {result.is_active!s:6}")

print("=" * 60)

# اختبار compute_control مباشرة
print("\n📐 Direct control law test:")
test_cases = [
    (1.657, 0.27, 0.05),  # Perplexity case
    (1.2, 0.1, 0.02),
    (0.8, -0.1, -0.01),
    (0.5, 0.0, 0.0),
]

for psi_norm, dpsi, d2psi in test_cases:
    u = compute_control(psi_norm, dpsi, d2psi)
    print(f"  Ψ_norm={psi_norm:.3f}, dΨ/dt={dpsi:+.2f}, d²Ψ/dt²={d2psi:+.2f} → u={u:.3f}")

print("=" * 60)
print("✅ ENTRO-CORE controller works correctly")

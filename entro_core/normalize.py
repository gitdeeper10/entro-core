"""
ENTRO-CORE: Logistic Normalization (Eq. 4)
Ψ_norm = Ψ_c · (1 − 1 / (1 + Ψ_raw / ref))
"""


def normalize_psi(psi_raw: float, psi_c: float = 2.0, ref: float = 10.0) -> float:
    """Normalize raw Ψ to [0, psi_c] using logistic function"""
    if psi_raw <= 0:
        return 0.0
    return psi_c * (1.0 - 1.0 / (1.0 + psi_raw / ref))


def denormalize_psi(psi_norm: float, psi_c: float = 2.0, ref: float = 10.0) -> float:
    """Reverse normalization (approximate)"""
    if psi_norm <= 0:
        return 0.0
    if psi_norm >= psi_c:
        return float('inf')
    ratio = psi_norm / psi_c
    return ref * (1.0 / (1.0 - ratio) - 1.0)


PSI_CRITICAL = 2.0
NORM_REFERENCE = 10.0

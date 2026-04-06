"""
ENTRO-CORE: System State Representation
E-LAB-03 | DOI: 10.5281/zenodo.19431029

Three-component state vector: (Ψ, dΨ/dt, d²Ψ/dt²)
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import time


@dataclass
class EntropyState:
    """Three-component entropy state vector"""
    psi: float          # Ψ(t) - Entropy state
    dpsi_dt: float      # dΨ/dt - Entropy velocity
    d2psi_dt2: float    # d²Ψ/dt² - Entropy acceleration
    timestamp: Optional[float] = None
    
    def is_critical(self, psi_c: float = 2.0) -> bool:
        return self.psi >= psi_c
    
    def is_stable(self, threshold: float = 1.5) -> bool:
        return self.psi < threshold
    
    def as_tuple(self) -> Tuple[float, float, float]:
        return (self.psi, self.dpsi_dt, self.d2psi_dt2)


class StateTracker:
    """Tracks entropy state and computes derivatives"""
    
    def __init__(self, history_size: int = 10):
        self.history_size = history_size
        self._history = []
    
    def update(self, psi: float, timestamp: Optional[float] = None) -> EntropyState:
        if timestamp is None:
            timestamp = time.time()
        
        self._history.append((timestamp, psi))
        if len(self._history) > self.history_size:
            self._history = self._history[-self.history_size:]
        
        # Compute derivatives
        dpsi_dt = 0.0
        d2psi_dt2 = 0.0
        
        if len(self._history) >= 2:
            t1, p1 = self._history[-2]
            t2, p2 = self._history[-1]
            dt = max(0.001, t2 - t1)
            dpsi_dt = (p2 - p1) / dt
        
        if len(self._history) >= 3:
            t1, p1 = self._history[-3]
            t2, p2 = self._history[-2]
            t3, p3 = self._history[-1]
            dt1 = max(0.001, t2 - t1)
            dt2 = max(0.001, t3 - t2)
            v1 = (p2 - p1) / dt1
            v2 = (p3 - p2) / dt2
            d2psi_dt2 = (v2 - v1) / ((dt1 + dt2) / 2)
        
        return EntropyState(psi, dpsi_dt, d2psi_dt2, timestamp)
    
    def reset(self):
        self._history = []

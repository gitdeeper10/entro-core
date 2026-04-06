"""
ENTRO-CORE: Actuation Mapping Strategies (Section IV)
- Linear: a = u
- Exponential: a = 1 - exp(-5u)
- Quadratic: a = u²
- Threshold: a = 0 if u < 0.3 else u
"""

import math
from enum import Enum


class ActuationStrategy(Enum):
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    QUADRATIC = "quadratic"
    THRESHOLD = "threshold"


def linear(u: float) -> float:
    """Linear mapping: a = u"""
    return max(0.0, min(1.0, u))


def exponential(u: float, beta: float = 5.0) -> float:
    """Exponential mapping: a = 1 - exp(-β·u)"""
    u_clamped = max(0.0, min(1.0, u))
    return 1.0 - math.exp(-beta * u_clamped)


def quadratic(u: float) -> float:
    """Quadratic mapping: a = u²"""
    u_clamped = max(0.0, min(1.0, u))
    return u_clamped * u_clamped


def threshold(u: float, limit: float = 0.3) -> float:
    """Threshold mapping: a = 0 if u < limit else u"""
    u_clamped = max(0.0, min(1.0, u))
    return 0.0 if u_clamped < limit else u_clamped


def apply_actuation(u: float, strategy: ActuationStrategy) -> float:
    """Apply selected actuation strategy"""
    if strategy == ActuationStrategy.LINEAR:
        return linear(u)
    elif strategy == ActuationStrategy.EXPONENTIAL:
        return exponential(u)
    elif strategy == ActuationStrategy.QUADRATIC:
        return quadratic(u)
    elif strategy == ActuationStrategy.THRESHOLD:
        return threshold(u)
    else:
        return linear(u)


# Strategy mapping dictionary
STRATEGIES = {
    "linear": linear,
    "exponential": exponential,
    "quadratic": quadratic,
    "threshold": threshold
}


def get_strategy(name: str):
    """Get strategy function by name"""
    return STRATEGIES.get(name.lower(), linear)

"""Closed-form soundness rules for Decoded Quantum Interferometry (DQI) candidates.

Mazumder and Niroula, arXiv:2610.06753. Notation: a max-LINSAT instance has m constraints
over n variables in F_q, rate alpha = n/m, accepted density rho (the fraction of F_q each
constraint accepts) and a decoder that corrects lam*m Hamming errors in the dual code.

- Prange completion satisfies n constraints exactly and the rest at random:
  Q_Pr = rho + (1 - rho) alpha.
- The DQI semicircle law: Q_DQI(lam, rho) = (sqrt(lam(1-rho)) + sqrt(rho(1-lam)))^2,
  saturating at 1 once lam > 1 - rho.
- DQI beats Prange exactly when lam > lambda_crit(alpha, rho).

These are asymptotic statements. They screen a candidate; they do not prove it.
"""

from __future__ import annotations

import math


def _unit(name: str, value: float) -> float:
    if not 0 < value < 1:
        raise ValueError(f"{name} must lie strictly between 0 and 1, got {value}")
    return float(value)


def q_prange(alpha: float, rho: float) -> float:
    """Satisfied fraction of Prange completion: rho + (1 - rho) alpha."""
    alpha, rho = _unit("alpha", alpha), _unit("rho", rho)
    return rho + (1 - rho) * alpha


def q_dqi(lam: float, rho: float) -> float:
    """Semicircle-law satisfied fraction of DQI at decoding radius lam (= l/m)."""
    rho = _unit("rho", rho)
    if not 0 <= lam <= 1:
        raise ValueError(f"lam must lie in [0, 1], got {lam}")
    if lam > 1 - rho:
        return 1.0
    return (math.sqrt(lam * (1 - rho)) + math.sqrt(rho * (1 - lam))) ** 2


def margin(lam: float, alpha: float, rho: float) -> float:
    """DQI's asymptotic margin over Prange completion, Q_DQI - Q_Pr."""
    return q_dqi(lam, rho) - q_prange(alpha, rho)


def lambda_crit(alpha: float, rho: float) -> float:
    """The decoding radius at which DQI's semicircle value equals Prange completion."""
    rho = _unit("rho", rho)
    pr = q_prange(alpha, rho)
    return (math.sqrt((1 - rho) * pr) - math.sqrt(rho * (1 - pr))) ** 2


def rho_crit(alpha: float) -> float:
    """The density at which lambda_crit reaches the Singleton reach alpha/2: below it no
    licensed radius beats Prange."""
    alpha = _unit("alpha", alpha)
    return 0.5 * (1 - math.sqrt(2 * (1 - alpha) / (2 - alpha)))

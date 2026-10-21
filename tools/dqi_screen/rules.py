"""Closed-form soundness rules for Decoded Quantum Interferometry (DQI) candidates.

Mazumder and Niroula, arXiv:2610.06753. Notation: a max-LINSAT instance has m constraints
over n variables in F_q, rate alpha = n/m, accepted density rho (the fraction of F_q each
constraint accepts) and a decoder that corrects lam*m Hamming errors in the dual code.

- Prange completion satisfies n constraints exactly and the rest at random:
  Q_Pr = rho + (1 - rho) alpha.
- The DQI semicircle law: Q_DQI(lam, rho) = (sqrt(lam(1-rho)) + sqrt(rho(1-lam)))^2,
  saturating at 1 once lam > 1 - rho.
- DQI beats Prange exactly when lam > lambda_crit(alpha, rho).
- The cosine objective cos(2 pi v / q) needs only signed {0, +-1} error patterns, so its reach
  is bounded by signed-pattern packing (Proposition 13), not by the Hamming bounds.

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


# ---------------------------------------------------------------------------
# Licensed Hamming reach: upper bounds on lam for the dual code (redundancy alpha).

UNIVERSAL_CAP = (math.sqrt(2) - 1) / 2  # max over alpha of margin_cap(alpha)


def licensed_radius(min_distance: int) -> int:
    """Largest radius l with 2l + 1 < d (worst-case unique decoding)."""
    if min_distance < 1:
        raise ValueError(f"min_distance must be at least 1, got {min_distance}")
    return (min_distance - 2) // 2


def singleton_reach(alpha: float) -> float:
    """Singleton: d <= n + 1, so a licensed lam is below alpha/2."""
    return _unit("alpha", alpha) / 2


def distance_reach(delta: float) -> float:
    """A code of relative distance delta decodes up to delta/2."""
    if not 0 < delta <= 1:
        raise ValueError(f"delta must lie in (0, 1], got {delta}")
    return delta / 2


def q_ary_entropy(x: float, q: int) -> float:
    """H_q(x) = x log_q(q-1) - x log_q x - (1-x) log_q(1-x)."""
    if q < 2:
        raise ValueError(f"q must be at least 2, got {q}")
    if not 0 <= x <= 1:
        raise ValueError(f"x must lie in [0, 1], got {x}")
    value = 0.0
    if x > 0:
        value += x * math.log(q - 1) - x * math.log(x)
    if x < 1:
        value -= (1 - x) * math.log(1 - x)
    return value / math.log(q)


def q_ary_entropy_inverse(y: float, q: int) -> float:
    """The x in [0, 1 - 1/q] with H_q(x) = y, by bisection (H_q increases there)."""
    if not 0 <= y <= 1:
        raise ValueError(f"y must lie in [0, 1], got {y}")
    lo, hi = 0.0, 1 - 1 / q
    for _ in range(200):
        mid = (lo + hi) / 2
        if q_ary_entropy(mid, q) < y:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-15:
            break
    return (lo + hi) / 2


def sphere_packing_reach(alpha: float, q: int) -> float:
    """Hamming bound: q^(m-n) balls of radius lam*m fit in F_q^m, so H_q(lam) <= alpha."""
    return q_ary_entropy_inverse(_unit("alpha", alpha), q)


def plotkin_reach(alpha: float, q: int) -> float:
    """Plotkin: delta <= (1 - 1/q) alpha for the dual code, so lam <= (1 - 1/q) alpha / 2."""
    return (1 - 1 / q) * _unit("alpha", alpha) / 2


def binary_entropy(x: float) -> float:
    """H_2(x) in bits."""
    return q_ary_entropy(x, 2)


def signed_packing_reach(alpha: float, q: int) -> float:
    """Proposition 13(i): a decoder licensed for {+-1} error patterns at reach lam <= 1/2 needs
    alpha >= (H_2(lam) + lam) / log_2 q. The largest such lam, by bisection on [0, 1/2]
    (H_2(lam) + lam increases there); 1/2 when alpha log_2 q >= 3/2. The cosine objective's
    reach bound: the Hamming bounds above do not limit signed patterns."""
    budget = _unit("alpha", alpha) * math.log2(q)
    if budget >= 1.5:
        return 0.5
    lo, hi = 0.0, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        if binary_entropy(mid) + mid < budget:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-15:
            break
    return (lo + hi) / 2


def _log2_binomial(m: int, k: int) -> float:
    return (math.lgamma(m + 1) - math.lgamma(k + 1) - math.lgamma(m - k + 1)) / math.log(2)


def packing_radius(m: int, n: int, q: int, letters: int) -> int:
    """Finite-length packing: the largest radius l at which the error patterns of weight l with
    entries from `letters` nonzero values (q - 1 for Hamming errors, 2 for signed {+-1} ones)
    number at most q^n, C(m, l) letters^l <= q^n; m when every radius passes. A decoder that
    recovers each pattern of weight <= l from its syndrome (B^T y in F_q^n) needs them distinct,
    so a larger radius is impossible at this (m, n, q). The count C(m, l) letters^l rises up to
    its mode and falls after, and the ball of radius l contains the patterns at the mode once l
    passes it, so the largest radius is below the mode or is m."""
    if not 0 <= n <= m or letters < 1:
        raise ValueError(f"need 0 <= n <= m and letters >= 1, got m={m}, n={n}, letters={letters}")
    budget = n * math.log2(q)
    tol = 1e-9 * (1 + budget)  # lgamma rounding: never reject a radius on it

    def fits(k: int) -> bool:
        return _log2_binomial(m, k) + k * math.log2(letters) <= budget + tol

    mode = min(m, (m + 1) * letters // (letters + 1))
    if fits(mode):
        return m
    lo, hi = 0, mode  # fits(lo), not fits(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if fits(mid):
            lo = mid
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------------------
# Margin cap, cosine objective, finite length, existential and subfield rules.


def margin_cap(alpha: float) -> float:
    """Proposition 8: within licensed reach DQI beats Prange by at most sqrt(u(1-u)) - u, u = alpha/2."""
    u = _unit("alpha", alpha) / 2
    return math.sqrt(u * (1 - u)) - u


def cosine_objective(lam: float) -> float:
    """Semicircle value per row of the cosine objective cos(2 pi v / q) at radius lam.

    Proposition 13(ii): the general law F_bar + sigma max_{t <= lam} (gamma t + 2 sqrt(t(1-t)))
    with mean 0, sigma = 1/sqrt(2) and skewness 0, i.e. sqrt(2 lam(1-lam)) for lam <= 1/2 and
    1/sqrt(2) beyond (the paper states the law for lam <= 1/2; a lower degree is always
    available). Prange's value is alpha, so this meets it exactly at lambda_crit_cos."""
    if not 0 <= lam <= 1:
        raise ValueError(f"lam must lie in [0, 1], got {lam}")
    t = min(lam, 0.5)
    return math.sqrt(2 * t * (1 - t))


def lambda_crit_cos(alpha: float) -> float | None:
    """Threshold radius for the cosine objective, where sqrt(2 lam(1-lam)) = alpha:
    (1 - sqrt(1 - 2 alpha^2)) / 2. None when alpha >= 1/sqrt(2), the largest cosine value,
    where no radius beats Prange."""
    alpha = _unit("alpha", alpha)
    if 2 * alpha * alpha >= 1:
        return None
    return (1 - math.sqrt(1 - 2 * alpha * alpha)) / 2


def restart_length(alpha: float, mu: float, R: float, N: float = 2**40, eta: float = 0.05) -> float | None:
    """Theorem 10: the instance length m needed before N Prange restarts (objective range R:
    1 count, 2 cosine) fail to close DQI's margin mu, at confidence 1 - eta:
    (1-alpha) R^2 ln(N/eta) / (2 mu^2). None when mu <= 0 (no length suffices)."""
    alpha = _unit("alpha", alpha)
    if mu <= 0:
        return None
    return (1 - alpha) * R * R * math.log(N / eta) / (2 * mu * mu)


def _kl(x: float, rho: float) -> float:
    value = x * math.log(x / rho)
    if x < 1:
        value += (1 - x) * math.log((1 - x) / (1 - rho))
    return value


def existential_line(alpha: float, rho: float, q: int) -> float:
    """R3: the satisfied fraction Q* some assignment reaches by counting, D_KL(Q* || rho) =
    alpha ln q, when q^alpha rho < 1; otherwise 1 (a perfect assignment exists)."""
    alpha, rho = _unit("alpha", alpha), _unit("rho", rho)
    budget = alpha * math.log(q)
    if budget + math.log(rho) >= 0:
        return 1.0
    lo, hi = rho, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if _kl(mid, rho) < budget:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-15:
            break
    return (lo + hi) / 2


def subfield_rate(alpha: float, b: int, c: int) -> float:
    """R4: rate of the instance read over the subfield, min(1, b alpha / c)."""
    if b < 1 or c < 1:
        raise ValueError(f"b and c must be positive, got {b}, {c}")
    return min(1.0, b * _unit("alpha", alpha) / c)


def subfield_baseline(rho: float, alpha_sub: float, m: int) -> float:
    """Prange completion over the subfield: rho + (1 - rho) floor(alpha_sub m) / m."""
    rho = _unit("rho", rho)
    if not 0 <= alpha_sub <= 1 or m < 1:
        raise ValueError(f"need 0 <= alpha_sub <= 1 and m >= 1, got {alpha_sub}, {m}")
    return rho + (1 - rho) * math.floor(alpha_sub * m + 1e-9) / m


def subfield_blocks_at_half(alpha: float, b: int, c: int) -> bool:
    """At rho = 1/2 the subfield baseline beats DQI at every licensed radius iff alpha >= 2c^2/(b^2+c^2)."""
    if b < 1 or c < 1:
        raise ValueError(f"b and c must be positive, got {b}, {c}")
    return _unit("alpha", alpha) >= 2 * c * c / (b * b + c * c)

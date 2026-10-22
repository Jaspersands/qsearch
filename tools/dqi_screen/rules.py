"""Closed-form soundness rules for Decoded Quantum Interferometry (DQI) candidates.

Mazumder and Niroula, arXiv:2610.06753. Notation: a max-LINSAT instance has m constraints
in F_q whose matrix B has rank n (the number of variables when B has full column rank), rate
alpha = n/m, accepted density rho (the fraction of F_q each constraint accepts) and a decoder
that corrects lam*m Hamming errors in the dual code.

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


def plotkin_distance(m: int, n: int, q: int) -> int:
    """Finite-length Plotkin bound for the dual code, a linear [m, k = m - n] code over F_q: its
    minimum distance is at most the average nonzero weight, d <= m (q-1) q^(k-1) / (q^k - 1),
    rounded down. Exact integers; when q^k - 1 > m (q - 1) the bound is floor(m (q - 1) / q)."""
    if not 0 <= n < m or q < 2:
        raise ValueError(f"need 0 <= n < m and q >= 2, got m={m}, n={n}, q={q}")
    k = m - n
    total = m * (q - 1)
    if k * math.log2(q) > math.log2(total) + 1:  # q^k > 2 total: the excess over total/q is below one
        return total // q
    return total * q ** (k - 1) // (q**k - 1)


def griesmer_distance(m: int, n: int, q: int) -> int:
    """Largest distance allowed by Griesmer for a linear [m, k=m-n]_q code.

    The exact bound is sum(i=0..k-1, ceil(d/q**i)) <= m. Once a term is one,
    all remaining terms are one, so the search costs O(log(m) * log_q(m)).
    """
    if not 0 <= n < m or q < 2:
        raise ValueError(f"need 0 <= n < m and q >= 2, got m={m}, n={n}, q={q}")
    k = m - n

    def fits(distance: int) -> bool:
        total, term, remaining = 0, distance, k
        while remaining and term > 1:
            total += term
            if total > m:
                return False
            term = (term + q - 1) // q
            remaining -= 1
        return total + remaining <= m

    lo, hi = 1, n + 2  # distance one fits; Singleton excludes hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if fits(mid):
            lo = mid
        else:
            hi = mid
    return lo


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


_EXACT_BITS = 2**15  # packing_radius sums exact integers while q^n has at most this many bits


def packing_radius(m: int, n: int, q: int, letters: int) -> int:
    """Finite-length sphere packing (the Hamming bound): the largest radius l whose ball, the
    error patterns of weight at most l with entries from `letters` nonzero values (q - 1 for
    Hamming errors, 2 for signed {+-1} ones), holds at most q^n patterns:
    sum_{i <= l} C(m, i) letters^i <= q^n; m when all (letters + 1)^m patterns fit. A decoder
    that recovers each pattern of weight <= l from its syndrome (B^T y in F_q^n) needs them all
    distinct, so a larger radius is impossible at this (m, n, q). Exact integers while q^n has at
    most _EXACT_BITS bits; beyond, the floating-point ball of _packing_radius_float."""
    if not 0 <= n <= m or q < 2 or letters < 1:
        raise ValueError(f"need 0 <= n <= m, q >= 2 and letters >= 1, got m={m}, n={n}, q={q}, letters={letters}")
    budget = n * math.log2(q)
    if m * math.log2(letters + 1) < budget - 1:  # every pattern fits, with a margin for rounding
        return m
    if budget > _EXACT_BITS:
        return _packing_radius_float(m, n, q, letters)
    # The ball outgrows q^n by l ~ budget (C(m, l) >= 2^l for l <= m/2), so the scan stays short.
    cap, total, term = q**n, 0, 1  # term = C(m, l) letters^l
    for radius in range(m + 1):
        total += term
        if total > cap:
            return radius - 1
        term = term * (m - radius) * letters // (radius + 1)
    return m


def _ball_peak(m: int, radius: int, letters: int) -> tuple[int, float]:
    """The index and log2 of the largest term C(m, i) letters^i with i <= radius: the terms rise
    up to the mode floor((m + 1) letters / (letters + 1)) and fall after it."""
    top = min(radius, (m + 1) * letters // (letters + 1))
    return top, _log2_binomial(m, top) + top * math.log2(letters)


def _log2_ball(m: int, radius: int, letters: int) -> float:
    """log2 sum_{i <= radius} C(m, i) letters^i in floating point: the sum runs outward from its
    largest term and stops at a term below 2^-100 of it (the at most m terms left beyond are
    smaller still)."""
    if m > 2**53:
        raise ValueError("inputs too large to screen in floating point: packing length m exceeds 2^53")
    log2_letters = math.log2(letters)
    top, peak = _ball_peak(m, radius, letters)
    total = 1.0
    terms = 0
    for step, end in ((-1, -1), (1, radius + 1)):
        i = top + step
        while i != end:
            terms += 1
            if terms > 100_000:
                raise ValueError("inputs too large to screen in floating point: packing sum exceeds 100000 terms")
            rel = _log2_binomial(m, i) + i * log2_letters - peak
            if rel < -100:
                break
            total += 2.0**rel
            i += step
    return peak + math.log2(total)


def _packing_radius_float(m: int, n: int, q: int, letters: int) -> int:
    """packing_radius in floating point, by bisection on the ball size; it never rejects a
    radius on lgamma rounding (a tolerance of 1e-9 relative)."""
    if m > 2**53:
        raise ValueError("inputs too large to screen in floating point: packing length m exceeds 2^53")
    budget = n * math.log2(q)
    tol = 1e-9 * (1 + budget)
    if m * math.log2(letters + 1) <= budget + tol:
        return m

    def fits(radius: int) -> bool:
        peak = _ball_peak(m, radius, letters)[1]
        if peak > budget + tol:
            return False
        if peak + math.log2(radius + 1) <= budget:  # radius + 1 terms, none above the peak
            return True
        return _log2_ball(m, radius, letters) <= budget + tol

    lo, hi = 0, m  # fits(lo), not fits(hi)
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
    (1-alpha) R^2 ln(N/eta) / (2 mu^2). None when mu <= 0 (no length suffices); OverflowError
    when mu is so small that the length is beyond a float."""
    alpha = _unit("alpha", alpha)
    if mu <= 0:
        return None
    length = (1 - alpha) * R * R * math.log(N / eta) / 2 / mu / mu  # never mu * mu, which underflows to 0
    if not math.isfinite(length):
        raise OverflowError(f"the restart length overflows a float at margin mu = {mu:.3g}")
    return length


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


_EXACT_TILT_LIMIT = 2**16  # sum over F_q up to here; the von Mises limit beyond


def _tilt(t: float, q: int) -> tuple[float, float]:
    """(D(P_t || uniform), 1 - E_t cos) for P_t(v) proportional to exp(t cos(2 pi v / q)): an exact sum
    over F_q for small q, else the q -> infinity (von Mises) limit by midpoint quadrature on [0, pi]
    where exp(t (cos - 1)) is not negligible. With w = exp(t (cos - 1)) and its mean <w>, the
    divergence is -ln <w> - t (1 - E_t cos)."""
    import numpy as np

    if q <= _EXACT_TILT_LIMIT:
        gap = 2 * np.sin(np.pi * np.arange(q) / q) ** 2  # 1 - cos(2 pi v / q)
        weight = np.exp(-t * gap)
        mean = weight.mean()
    else:
        width = min(math.pi, 40 / math.sqrt(t)) if t > 0 else math.pi
        points = 4001
        theta = (np.arange(points) + 0.5) * width / points
        gap = 2 * np.sin(theta / 2) ** 2
        weight = np.exp(-t * gap)
        mean = weight.sum() * width / points / math.pi  # uniform measure on [0, pi]
    one_minus_mu = float((gap * weight).sum() / weight.sum())
    return float(-math.log(mean) - t * one_minus_mu), one_minus_mu


def cosine_existential_line(alpha: float, q: int) -> float:
    """Proposition 13(iii): the largest mean of cos(2 pi v / q) over distributions on F_q within
    relative entropy alpha ln q of uniform, attained by the exponential tilt P_t; t by bisection
    so that D(P_t || uniform) = alpha ln q (the divergence increases with t)."""
    budget = _unit("alpha", alpha) * math.log(q)
    lo, hi = 0.0, 1.0
    while _tilt(hi, q)[0] < budget:
        lo, hi = hi, 2 * hi
        if hi > 1e300:
            return 1.0
    for _ in range(200):
        mid = (lo + hi) / 2 if hi < 4 * max(lo, 1.0) else math.sqrt(max(lo, 1.0) * hi)
        if _tilt(mid, q)[0] < budget:
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-13 * hi:
            break
    return 1 - _tilt((lo + hi) / 2, q)[1]


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
    return 1 - (1 - rho) * (m - math.floor(alpha_sub * m + 1e-9)) / m


def subfield_blocks_at_half(alpha: float, b: int, c: int) -> bool:
    """At rho = 1/2 the subfield baseline beats DQI at every licensed radius iff alpha >= 2c^2/(b^2+c^2)."""
    if b < 1 or c < 1:
        raise ValueError(f"b and c must be positive, got {b}, {c}")
    return _unit("alpha", alpha) >= 2 * c * c / (b * b + c * c)

"""Matched classical sampling audit for the relative-decoding spin-chain target.

Whole-worldline heat baths, not time-slice Glauber updates. The analytic
certificate concerns computational-basis Gibbs samples, NOT a prepared TFD.
Outward rational interval arithmetic certifies conditional update TV bounds
within the reserved per-update allowance; PRNG coins remain uncertified.
Dense calculations are bounded independent controls, never sampler inputs.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from math import ceil, comb, exp, lgamma, log, sqrt, tanh
from pathlib import Path
import random
import sys
import time

import numpy as np
from flint import nmod_mat
from scipy.linalg import expm
from scipy.special import expit, logsumexp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from theorems.parity_block_usd_prange import affine_system, uniform_affine_solution

REPORT = ROOT / "research/classical_baselines/relative_gibbs_worldline.json"
SPINS = np.array([1, -1])


@dataclass(frozen=True)
class ChainTarget:
    F: tuple
    transverse: tuple
    longitudinal: tuple
    central: tuple
    coupled: tuple
    bonds: tuple

    def __post_init__(self):
        F = self.F
        if (not F or not F[0] or any(len(row) != len(F[0]) for row in F)
                or any(type(x) is not int or x not in (0, 1) for row in F for x in row)):
            raise ValueError("nonempty canonical binary parity matrix required")
        for name in ("transverse", "longitudinal", "central", "coupled", "bonds"):
            values = getattr(self, name)
            if len(values) != self.n - (name == "bonds") or not np.all(np.isfinite(values)):
                raise ValueError("finite coefficient arrays of the exact lengths required")

    @property
    def n(self):
        return len(self.F[0])

    @property
    def r(self):
        return len(self.F)

    @property
    def norm_bound(self):
        return sum(abs(x) for name in ("transverse", "longitudinal", "central", "coupled", "bonds")
                   for x in getattr(self, name))

    def parity(self, central_spins):
        z = np.asarray(central_spins)
        if z.shape != (self.r,) or not np.all(np.isin(z, (-1, 1))):
            raise ValueError("one sign per central spin required")
        return np.prod(np.where(np.asarray(self.F), z[:, None], 1), axis=0)

    def diagonal_energy(self, q, central_spins):
        q = np.asarray(q)
        if q.shape[0] != self.n or not np.all(np.isin(q, (-1, 1))):
            raise ValueError("native chain signs required")
        c = self.parity(central_spins)
        if q.ndim == 1:
            return float(np.dot(self.central, c) + np.dot(np.asarray(self.longitudinal)
                         + np.asarray(self.coupled)*c, q) + np.dot(self.bonds, q[:-1]*q[1:]))
        return np.dot(self.central, c) + (np.asarray(self.longitudinal)
               + np.asarray(self.coupled)*c) @ q + np.asarray(self.bonds) @ (q[:-1]*q[1:])

    def path_field(self, i, paths, central_spins):
        field = np.full(paths.shape[1], self.longitudinal[i] + self.coupled[i]*self.parity(central_spins)[i], dtype=float)
        if i:
            field += self.bonds[i-1]*paths[i-1]
        if i+1 < self.n:
            field += self.bonds[i]*paths[i+1]
        return field

    def central_field(self, a, paths, central_spins):
        c = self.parity(central_spins)
        # Remove the current spin from each incident parity before conditioning.
        return float(np.dot(np.asarray(self.F)[a]*c*central_spins[a],
                            np.asarray(self.central)+np.asarray(self.coupled)*paths.mean(axis=1)))


def validate_temperature(beta):
    if not np.isfinite(beta) or beta < 0:
        raise ValueError("finite nonnegative inverse temperature required")


def influence_bounds(model, beta):
    """Symmetric block-influence majorant, independent of the Trotter length."""
    validate_temperature(beta)
    n, r = model.n, model.r
    F = np.asarray(model.F)
    C = np.zeros((n+r, n+r))
    for i, J in enumerate(model.bonds):
        C[i, i+1] = C[i+1, i] = tanh(beta*abs(J))
    for i in range(n):
        for a in np.flatnonzero(F[:, i]):
            C[i, n+a] = C[n+a, i] = tanh(beta*abs(model.coupled[i]))
    strength = np.abs(model.central)+np.abs(model.coupled)
    for a in range(r):
        for b in range(a):
            C[n+a, n+b] = C[n+b, n+a] = tanh(beta*float(np.dot(F[a]*F[b], strength)))
    return C


def regular_influence_bound(column_degree, row_degree, beta_J):
    if type(column_degree) is not int or type(row_degree) is not int or min(column_degree, row_degree) < 1:
        raise ValueError("positive integer incidence bounds required")
    validate_temperature(beta_J)
    return max((2+column_degree)*tanh(beta_J),
               row_degree*tanh(beta_J)+row_degree*(column_degree-1)*tanh(2*beta_J))


def trotter_bound(beta, norm_bound, slices):
    """Trace distance upper bound from symmetric splitting and Gibbs entropy.

    Analytic real-arithmetic formula; floating evaluation is not an interval
    certificate. See the companion note for the log-Lipschitz proof.
    """
    validate_temperature(beta)
    if not np.isfinite(norm_bound) or norm_bound < 0 or type(slices) is not int or slices < 1:
        raise ValueError("nonnegative norm bound and positive slice count required")
    a = beta*norm_bound
    if not a:
        return 0.0
    log_bound = 1.5*log(a)+a/slices-log(slices)-0.5*log(3)
    return exp(min(0.0, log_bound))


def sampling_budget(model, beta, epsilon):
    validate_temperature(beta)
    if not 0 < epsilon < 1:
        raise ValueError("TV budget must lie strictly between zero and one")
    alpha = float(influence_bounds(model, beta).sum(axis=0).max())
    if alpha >= 1:
        raise ValueError("NO mixing certificate: influence bound is at least one")
    # Leave a separate epsilon/3 allowance for numerical conditional updates.
    a, err = beta*model.norm_bound, epsilon/3
    slices = max(1, ceil(a), ceil(exp(1)*a**1.5/(sqrt(3)*err)))
    blocks = model.n+model.r
    updates = ceil(blocks*log(blocks/err)/(1-alpha))
    mixing = blocks*exp(-(1-alpha)*updates/blocks)
    return {"alpha": alpha, "slices": slices, "updates": updates,
            "mixing_TV_bound": mixing, "Trotter_TV_bound": trotter_bound(beta, model.norm_bound, slices),
            "conditional_TV_tolerance_per_update": err/updates,
            "roundoff_certified": False,
            "analytic_real_arithmetic_only": True}


def rational_value(x) -> Fraction:
    if isinstance(x, bool) or not isinstance(x, (int, float, Fraction, np.floating, np.integer)):
        raise ValueError("finite numeric value required for rational conversion")
    if isinstance(x, (float, np.floating)) and not math.isfinite(float(x)):
        raise ValueError("nonfinite float cannot be converted to Fraction")
    return Fraction(x) if isinstance(x, (int, Fraction)) else Fraction(str(float(x)))


def enclose_dyadic(value: Fraction, bits: int, upper: bool) -> Fraction:
    value = Fraction(value)
    if type(bits) is not int or bits < 1:
        raise ValueError("dyadic precision bits must be a positive integer")
    scale = 1 << bits
    q, r = divmod(value.numerator * scale, value.denominator)
    return Fraction(q + int(upper and bool(r)), scale)


def exp_interval(x, bits: int = 80) -> tuple[Fraction, Fraction]:
    """Outward rational interval [lo, hi] containing exp(x) for rational x."""
    x = rational_value(x)
    if type(bits) is not int or bits < 16:
        raise ValueError("interval precision bits must be an integer >= 16")
    if x == 0:
        return Fraction(1), Fraction(1)
    if x < 0:
        lo, hi = exp_interval(-x, bits + 6)
        return enclose_dyadic(Fraction(1) / hi, bits, False), enclose_dyadic(Fraction(1) / lo, bits, True)
    s = 0
    y = x
    while y > Fraction(1, 2):
        y /= 2
        s += 1
    work = bits + s + 16
    bound = Fraction(1, 1 << work)
    lo_sum = hi_sum = term = Fraction(1)
    k = 1
    while True:
        term = term * y / k
        lo_sum = enclose_dyadic(lo_sum + term, work + 8, False)
        hi_sum = enclose_dyadic(hi_sum + term, work + 8, True)
        if 2 * term <= bound and k >= 4:
            break
        k += 1
    rem = 2 * (term * y / (k + 1))
    lo, hi = lo_sum, enclose_dyadic(hi_sum + rem, work + 8, True)
    for _ in range(s):
        lo = enclose_dyadic(lo * lo, work, False)
        hi = enclose_dyadic(hi * hi, work, True)
    return enclose_dyadic(lo, bits, False), enclose_dyadic(hi, bits, True)


def tanh_interval(x, bits: int = 80) -> tuple[Fraction, Fraction]:
    """Outward rational interval [lo, hi] containing tanh(x) for x >= 0."""
    x = rational_value(x)
    if x < 0:
        raise ValueError("nonnegative argument required for tanh_interval")
    if x == 0:
        return Fraction(0), Fraction(0)
    e_lo, e_hi = exp_interval(-2 * x, bits + 6)
    lo = max(Fraction(0), enclose_dyadic((1 - e_hi) / (1 + e_hi), bits, False))
    hi = min(Fraction(1), enclose_dyadic((1 - e_lo) / (1 + e_lo), bits, True))
    return lo, hi


def logistic_interval(x, bits: int = 80) -> tuple[Fraction, Fraction]:
    """Outward rational interval [lo, hi] containing 1 / (1 + exp(-x))."""
    x = rational_value(x)
    e_lo, e_hi = exp_interval(-x, bits + 6)
    lo = max(Fraction(0), enclose_dyadic(Fraction(1) / (1 + e_hi), bits, False))
    hi = min(Fraction(1), enclose_dyadic(Fraction(1) / (1 + e_lo), bits, True))
    return lo, hi


def ratio_interval(a_bounds: tuple[Fraction, Fraction], b_bounds: tuple[Fraction, Fraction], bits: int = 80) -> tuple[Fraction, Fraction]:
    """Outward enclosure of A / (A + B) for nonnegative intervals A and B."""
    a_lo, a_hi = a_bounds
    b_lo, b_hi = b_bounds
    if min(a_lo, a_hi, b_lo, b_hi) < 0 or a_lo + b_lo <= 0:
        raise ValueError("positive nonnegative weight intervals required")
    lo = enclose_dyadic(a_lo / (a_lo + b_hi), bits, False)
    hi = enclose_dyadic(a_hi / (a_hi + b_lo), bits, True)
    return max(Fraction(0), lo), min(Fraction(1), hi)


def draw_interval_bernoulli(p_interval: tuple[Fraction, Fraction], coin_source, max_coin_bits: int = 96) -> dict:
    """Resolve a Bernoulli(p) draw from an outward interval [p_lo, p_hi] using dyadic coins."""
    p_lo, p_hi = Fraction(p_interval[0]), Fraction(p_interval[1])
    if not (0 <= p_lo <= p_hi <= 1):
        raise ValueError("valid probability interval [p_lo, p_hi] in [0,1] required")
    if type(max_coin_bits) is not int or max_coin_bits < 8:
        raise ValueError("max_coin_bits must be an integer >= 8")
    lo, hi = Fraction(0), Fraction(1)
    coins_used = 0
    decided_outside_uncertainty = False
    outcome = 0
    for _ in range(max_coin_bits):
        if hi <= p_lo:
            outcome = 1
            decided_outside_uncertainty = True
            break
        if lo >= p_hi:
            outcome = 0
            decided_outside_uncertainty = True
            break
        bit = int(coin_source.getrandbits(1))
        coins_used += 1
        mid = (lo + hi) / 2
        if bit == 0:
            hi = mid
        else:
            lo = mid
    else:
        if hi <= p_lo:
            outcome = 1
            decided_outside_uncertainty = True
        elif lo >= p_hi:
            outcome = 0
            decided_outside_uncertainty = True
        else:
            midpoint = (p_lo + p_hi) / 2
            outcome = int((lo + hi) / 2 < midpoint)
    tv_upper = min(Fraction(1), (p_hi - p_lo) + Fraction(1, 1 << max_coin_bits))
    return {
        "outcome": outcome,
        "p_lower_exact": str(p_lo),
        "p_upper_exact": str(p_hi),
        "interval_width_exact": str(p_hi - p_lo),
        "coins_used": coins_used,
        "decided_outside_uncertainty": decided_outside_uncertainty,
        "conditional_TV_upper_exact": str(tv_upper),
    }


def interval_ring_messages(field, gamma, dt, bits: int = 64):
    """Multiplicative O(M) periodic worldline backward messages using outward intervals."""
    field_q = [rational_value(f) for f in field]
    gamma_q, dt_q = rational_value(gamma), rational_value(dt)
    if not field_q or min(gamma_q, dt_q) < 0:
        raise ValueError("nonempty field and nonnegative gamma, dt required")
    if type(bits) is not int or bits < 16:
        raise ValueError("interval precision bits must be an integer >= 16")
    M = len(field_q)
    work = bits + 2 * M + 16
    t_lo, t_hi = tanh_interval(dt_q * gamma_q, work)
    one = (Fraction(1), Fraction(1))
    K = [[one, (t_lo, t_hi)], [(t_lo, t_hi), one]]
    local = [
        [exp_interval(-dt_q * f, work), exp_interval(dt_q * f, work)]
        for f in field_q
    ]
    back = [[[(Fraction(0), Fraction(0)) for _ in range(2)] for _ in range(M)] for _ in range(2)]
    for a0 in range(2):
        for s in range(2):
            back[a0][M - 1][s] = K[s][a0]
    for j in range(M - 2, -1, -1):
        for a0 in range(2):
            for s in range(2):
                lo_acc = hi_acc = Fraction(0)
                for sp in range(2):
                    k_lo, k_hi = K[s][sp]
                    l_lo, l_hi = local[j + 1][sp]
                    b_lo, b_hi = back[a0][j + 1][sp]
                    lo_acc += enclose_dyadic(k_lo * l_lo * b_lo, work, False)
                    hi_acc += enclose_dyadic(k_hi * l_hi * b_hi, work, True)
                back[a0][j][s] = (enclose_dyadic(lo_acc, work, False), enclose_dyadic(hi_acc, work, True))
    initial = [
        (
            enclose_dyadic(local[0][a0][0] * back[a0][0][a0][0], work, False),
            enclose_dyadic(local[0][a0][1] * back[a0][0][a0][1], work, True),
        )
        for a0 in range(2)
    ]
    return K, local, back, initial, work


def interval_ring_path(field, gamma, dt, *, bits: int = 64, coin_source=None, prescribed=None, max_coin_bits: int = 96):
    """Outward-interval periodic worldline conditional sampler and probability auditor."""
    K, local, back, initial, work = interval_ring_messages(field, gamma, dt, bits=bits)
    M = len(local)
    if prescribed is not None:
        prescribed = tuple(prescribed)
        if len(prescribed) != M or any(x not in (-1, 1) for x in prescribed):
            raise ValueError("a complete sign path is required")
    elif coin_source is None:
        raise ValueError("an explicit coin source is required when prescribed is None")
    values = []
    prob_lo, prob_hi = Fraction(1), Fraction(1)
    step_tv_sum = Fraction(0)
    coins_total = 0
    for j in range(M):
        if j == 0:
            w_plus, w_minus = initial[0], initial[1]
        else:
            a0, prev = values[0], values[-1]
            w_plus = (
                enclose_dyadic(K[prev][0][0] * local[j][0][0] * back[a0][j][0][0], work, False),
                enclose_dyadic(K[prev][0][1] * local[j][0][1] * back[a0][j][0][1], work, True),
            )
            w_minus = (
                enclose_dyadic(K[prev][1][0] * local[j][1][0] * back[a0][j][1][0], work, False),
                enclose_dyadic(K[prev][1][1] * local[j][1][1] * back[a0][j][1][1], work, True),
            )
        if w_plus[0] + w_minus[0] == 0:
            if prescribed is not None:
                return np.asarray(prescribed), (Fraction(0), Fraction(0)), Fraction(0), 0
            raise ArithmeticError("ambiguous zero-weight periodic branch in interval_ring_path")
        p_plus_bounds = ratio_interval(w_plus, w_minus, bits=bits)
        if prescribed is not None:
            val = int(prescribed[j] == -1)
            chosen_bounds = p_plus_bounds if val == 0 else ratio_interval(w_minus, w_plus, bits=bits)
            prob_lo = enclose_dyadic(prob_lo * chosen_bounds[0], bits, False)
            prob_hi = enclose_dyadic(prob_hi * chosen_bounds[1], bits, True)
            step_tv_sum += (p_plus_bounds[1] - p_plus_bounds[0]) + Fraction(1, 1 << max_coin_bits)
        else:
            draw = draw_interval_bernoulli(p_plus_bounds, coin_source, max_coin_bits=max_coin_bits)
            val = 0 if draw["outcome"] == 1 else 1
            step_tv_sum += Fraction(draw["conditional_TV_upper_exact"])
            coins_total += draw["coins_used"]
        values.append(val)
    return SPINS[values], (prob_lo, min(Fraction(1), prob_hi)), min(Fraction(1), step_tv_sum), coins_total


def interval_central_update(model, a, paths, central_spins, beta, *, bits: int = 64, coin_source=None, max_coin_bits: int = 96):
    """Outward-interval central spin logistic update and TV error certificate."""
    validate_temperature(beta)
    if type(a) is not int or not 0 <= a < model.r:
        raise ValueError("valid central spin index required")
    c = model.parity(central_spins)
    M = paths.shape[1]
    beta_q = rational_value(beta)
    field_q = Fraction(0)
    for i in range(model.n):
        if model.F[a][i]:
            sign_without_a = int(c[i] * central_spins[a])
            mean_q = Fraction(int(paths[i].sum()), M)
            g_i = rational_value(model.central[i]) + rational_value(model.coupled[i]) * mean_q
            field_q += sign_without_a * g_i
    p_plus_bounds = logistic_interval(-2 * beta_q * field_q, bits=bits)
    if coin_source is None:
        tv_upper = min(Fraction(1), (p_plus_bounds[1] - p_plus_bounds[0]) + Fraction(1, 1 << max_coin_bits))
        return None, p_plus_bounds, tv_upper, 0
    draw = draw_interval_bernoulli(p_plus_bounds, coin_source, max_coin_bits=max_coin_bits)
    spin = 1 if draw["outcome"] == 1 else -1
    return spin, p_plus_bounds, Fraction(draw["conditional_TV_upper_exact"]), draw["coins_used"]


def interval_pin_given_paths(model, beta, paths, coin_source, *, bits: int = 64, max_coin_bits: int = 96):
    """Outward-interval source pinning step with certified Bernoulli pin intervals."""
    validate_temperature(beta)
    M = paths.shape[1]
    beta_q = rational_value(beta)
    selected = []
    preferred = []
    pin_tv_sum = Fraction(0)
    coins_total = 0
    for i in range(model.n):
        mean_q = Fraction(int(paths[i].sum()), M)
        g_i = rational_value(model.central[i]) + rational_value(model.coupled[i]) * mean_q
        pref = -1 if g_i > 0 else 1
        preferred.append(pref)
        p_bounds = tanh_interval(beta_q * abs(g_i), bits=bits)
        draw = draw_interval_bernoulli(p_bounds, coin_source, max_coin_bits=max_coin_bits)
        pin_tv_sum += Fraction(draw["conditional_TV_upper_exact"])
        coins_total += draw["coins_used"]
        if draw["outcome"] == 1:
            selected.append(i)
    selected = tuple(selected)
    system = pin_system(model, selected, preferred)
    if system["rank"] != len(selected):
        return {"selected": selected, "rank": system["rank"], "ABSTAIN": True, "R": None,
                "pin_rounding_TV_upper_exact": str(min(Fraction(1), pin_tv_sum)),
                "coins_used": coins_total}
    word = uniform_affine_solution(system, model.r, coin_source)
    R = [1 - 2 * ((word >> a) & 1) for a in range(model.r)]
    return {"selected": selected, "rank": system["rank"], "ABSTAIN": False, "R": R,
            "pin_rounding_TV_upper_exact": str(min(Fraction(1), pin_tv_sum)),
            "coins_used": coins_total}


def certified_interval_update_audit(model, beta, epsilon, *, bits: int = 64, max_coin_bits: int = 96, seed: int = 1986):
    """Verify outward-interval conditional updates stay within the per-update TV budget."""
    budget = sampling_budget(model, beta, epsilon)
    M = budget["slices"]
    per_update_tol = rational_value(budget["conditional_TV_tolerance_per_update"])
    coin_source = random.Random(seed)
    paths = np.ones((model.n, M), dtype=int)
    central = np.ones(model.r, dtype=int)
    max_update_tv = Fraction(0)
    total_coins = 0
    for i in range(model.n):
        field = model.path_field(i, paths, central)
        paths[i], _, step_tv, coins = interval_ring_path(
            field, abs(model.transverse[i]), Fraction(rational_value(beta), M),
            bits=bits, coin_source=coin_source, max_coin_bits=max_coin_bits
        )
        max_update_tv = max(max_update_tv, step_tv)
        total_coins += coins
    for a in range(model.r):
        spin, _, step_tv, coins = interval_central_update(
            model, a, paths, central, beta,
            bits=bits, coin_source=coin_source, max_coin_bits=max_coin_bits
        )
        central[a] = spin
        max_update_tv = max(max_update_tv, step_tv)
        total_coins += coins
    pinned = interval_pin_given_paths(model, beta, paths, coin_source, bits=bits, max_coin_bits=max_coin_bits)
    if max_update_tv > per_update_tol:
        raise ArithmeticError("outward interval conditional update TV exceeded per-update budget")
    return {
        "bits": bits,
        "max_coin_bits": max_coin_bits,
        "slices": M,
        "updates_budgeted": budget["updates"],
        "per_update_TV_tolerance_exact": str(per_update_tol),
        "max_observed_single_update_TV_upper_exact": str(max_update_tv),
        "total_chain_update_rounding_TV_upper_exact": str(min(Fraction(1), budget["updates"] * max_update_tv)),
        "pin_rounding_TV_upper_exact": pinned["pin_rounding_TV_upper_exact"],
        "interval_conditional_TV_within_per_update_budget": bool(max_update_tv <= per_update_tol),
        "coins_used_in_one_full_sweep_and_pin": total_coins + pinned["coins_used"],
        "interval_arithmetic_certified": True,
        "prng_is_not_a_certified_fair_coin_source": True,
    }


def ring_messages(field, gamma, dt):
    """O(M) forward/backward preparation for a periodic two-state path."""
    field = np.asarray(field, dtype=float)
    if field.ndim != 1 or not len(field) or not np.all(np.isfinite(field)):
        raise ValueError("nonempty finite path field required")
    if not np.isfinite(gamma) or not np.isfinite(dt) or min(gamma, dt) < 0:
        raise ValueError("nonnegative finite transverse magnitude and time step required")
    t = tanh(dt*gamma)
    off = log(t) if t else -np.inf
    K = np.array([[0.0, off], [off, 0.0]])
    local = -dt*field[:, None]*SPINS
    back = np.empty((2, len(field), 2))
    back[:, -1, :] = K.T
    for j in range(len(field)-2, -1, -1):
        v = K[None, :, :]+local[j+1][None, None, :]+back[:, j+1, None, :]
        back[:, j, :] = np.logaddexp(v[:, :, 0], v[:, :, 1])
    initial = local[0]+np.array([back[a, 0, a] for a in range(2)])
    return K, local, back, initial


def ring_path(field, gamma, dt, rng=None, prescribed=None):
    """Sample without enumerating paths; prescribed paths audit the same law."""
    K, local, back, initial = ring_messages(field, gamma, dt)
    if prescribed is not None:
        prescribed = tuple(prescribed)
        if len(prescribed) != len(field) or any(x not in (-1, 1) for x in prescribed):
            raise ValueError("a complete sign path is required")
    elif rng is None:
        raise ValueError("an explicit random generator is required")
    values, log_probability = [], 0.0
    for j in range(len(field)):
        weights = initial if j == 0 else K[values[-1]]+local[j]+back[values[0], j]
        normalizer = np.logaddexp(weights[0], weights[1])
        if not np.isfinite(normalizer):
            return np.asarray(prescribed), -np.inf
        value = int(prescribed[j] == -1) if prescribed is not None else int(rng.random() >= exp(weights[0]-normalizer))
        log_probability += weights[value]-normalizer
        values.append(value)
    return SPINS[values], float(log_probability)


def heatbath_paths(model, beta, budget, seed):
    M = budget["slices"]
    rng = np.random.default_rng(seed)
    paths, central = np.ones((model.n, M), dtype=int), np.ones(model.r, dtype=int)
    for _ in range(budget["updates"]):
        block = int(rng.integers(model.n+model.r))
        if block < model.n:
            paths[block], _ = ring_path(model.path_field(block, paths, central),
                                        abs(model.transverse[block]), beta/M, rng)
        else:
            a = block-model.n
            pplus = expit(-2*beta*model.central_field(a, paths, central))
            central[a] = 1 if rng.random() < pplus else -1
    return paths, central


def sample(model, beta, epsilon, seed=123):
    budget = sampling_budget(model, beta, epsilon)
    started = time.monotonic()
    paths, central = heatbath_paths(model, beta, budget, seed)
    return {"input": asdict(model), "beta": beta, "epsilon": epsilon, "seed": seed,
            "budget": budget, "q_sample": paths[:, 0].tolist(), "R_sample": central.tolist(),
            "central_parities": model.parity(central).tolist(),
            "elapsed_seconds": time.monotonic()-started,
            "dense_or_counting_oracle_calls": 0, "prepared_quantum_state": False,
            "sample_has_rigorous_floating_point_error_certificate": False}


def identity_source(model):
    return ChainTarget(tuple(tuple(int(i == j) for j in range(model.n)) for i in range(model.n)),
                       model.transverse, model.longitudinal, model.central, model.coupled, model.bonds)


def pinning_parameters(model, beta, paths):
    g = np.asarray(model.central)+np.asarray(model.coupled)*paths.mean(axis=1)
    return np.tanh(beta*np.abs(g)), np.where(g > 0, -1, 1)


def pin_system(model, selected, preferred):
    equations = tuple((sum(model.F[a][i] << a for a in range(model.r)), int(preferred[i] == -1))
                      for i in selected)
    return affine_system(equations, model.r)


def pin_given_paths(model, beta, paths, rng):
    probabilities, preferred = pinning_parameters(model, beta, paths)
    selected = tuple(i for i, p in enumerate(probabilities) if rng.random() < p)
    system = pin_system(model, selected, preferred)
    if system["rank"] != len(selected):
        return {"selected": selected, "rank": system["rank"], "ABSTAIN": True, "R": None}
    word = uniform_affine_solution(system, model.r, rng)
    R = [1-2*((word >> a) & 1) for a in range(model.r)]
    return {"selected": selected, "rank": system["rank"], "ABSTAIN": False, "R": R}


def pinning_error_bound(model, beta, distance_lower):
    """Distance is an explicit proof premise, not inferred from successful pins."""
    validate_temperature(beta)
    n, d = model.n, distance_lower
    if type(d) is not int or not 1 <= d <= n:
        raise ValueError("an explicit valid positive distance lower-bound premise is required")
    p = tanh(beta*max(abs(c)+abs(h) for c, h in zip(model.central, model.coupled)))
    ratio = (n-d)*p/(d+1)
    if not p:
        log_A, A = None, 0.0
    elif ratio >= 1:
        log_A, A = None, 1.0
    else:
        log_A = lgamma(n+1)-lgamma(d+1)-lgamma(n-d+1)+d*log(p)-log(1-ratio)
        A = exp(min(0, log_A))
    tv = min(1.0, A+2*A/(1-A)) if A < 1 else 1.0
    return {"distance_lower_PREMISE": d, "p_max": p, "weight_sum_log_upper": log_A,
            "weight_sum_upper_capped_at_one": A, "pinning_TV_bound_including_ABSTAIN": tv,
            "distance_verified_by_this_function": False, "roundoff_certified": False}


def sample_via_source(model, beta, epsilon, distance_lower, seed=1986):
    """epsilon budgets mixing/Trotter/numerics; pinning adds its reported error."""
    source = identity_source(model)
    budget = sampling_budget(source, beta, epsilon)
    pin_bound = pinning_error_bound(model, beta, distance_lower)
    started = time.monotonic()
    paths, _ = heatbath_paths(source, beta, budget, seed)
    pinned = pin_given_paths(model, beta, paths, random.Random(seed+1))
    return {"input": asdict(model), "source_is_identity_parity": True, "seed": seed, "beta": beta,
            "requested_source_Trotter_numerics_budget": epsilon,
            "source_budget": budget, "pinning_bound": pin_bound, "pinning": pinned,
            "q_sample": None if pinned["ABSTAIN"] else paths[:, 0].tolist(),
            "analytic_TV_bound_excluding_roundoff": min(1.0, budget["mixing_TV_bound"]
                  +budget["Trotter_TV_bound"]+pin_bound["pinning_TV_bound_including_ABSTAIN"]),
            "source_central_sample_discarded": True, "retry_after_ABSTAIN": False,
            "elapsed_seconds": time.monotonic()-started, "roundoff_certified": False,
            "dense_or_counting_oracle_calls": 0, "prepared_TFD": False}


def project_path_law(law, n, M):
    out = np.zeros(2**law.ndim)
    for state in np.ndindex(law.shape):
        word = tuple(value//(2**(M-1)) for value in state[:n])+state[n:]
        out[np.ravel_multi_index(word, (2,)*law.ndim)] += law[state]
    return out


def exact_pinning_control(model, beta, M=2):
    """Every source path, pin set and affine solution; ABSTAIN remains an output."""
    source = identity_source(model)
    law = path_law(source, beta, M)
    qlaw = law.sum(axis=tuple(range(model.n, 2*model.n)))
    paths = np.array(list(product((1, -1), repeat=M)))
    out = np.zeros(2**(model.n+model.r)+1)
    all_R = list(product((1, -1), repeat=model.r))
    for state in np.ndindex(qlaw.shape):
        q = paths[list(state)]
        probabilities, preferred = pinning_parameters(model, beta, q)
        for flags in product((0, 1), repeat=model.n):
            mass = qlaw[state]*np.prod(np.where(flags, probabilities, 1-probabilities))
            selected = tuple(i for i, x in enumerate(flags) if x)
            system = pin_system(model, selected, preferred)
            if system["rank"] < len(selected):
                out[-1] += mass
                continue
            solutions = [R for R in all_R if all(model.parity(R)[i] == preferred[i] for i in selected)]
            assert len(solutions) == 2**(model.r-len(selected))
            for R in solutions:
                word = tuple(int(x == -1) for x in q[:, 0])+tuple(int(x == -1) for x in R)
                out[np.ravel_multi_index(word, (2,)*(model.n+model.r))] += mass/len(solutions)
    target = project_path_law(path_law(model, beta, M), model.n, M)
    return {"beta": beta, "output_mass": float(out.sum()), "ABSTAIN_mass": float(out[-1]),
            "TV_including_ABSTAIN": float((abs(out[:-1]-target).sum()+out[-1])/2),
            "TV_after_UNCHARGED_postselection_countercontrol": float(abs(out[:-1]/(1-out[-1])-target).sum()/2),
            "output_law": out.tolist(), "target_Trotter_law": target.tolist()}


def repetition_control(n=32):
    # Kernel exactly {0, all-ones}: a known easy code, not an advantage candidate.
    return ChainTarget(tuple(tuple(int(j == i or j == n-1) for j in range(n)) for i in range(n-1)),
                       (1.0,)*n, (1.0,)*n, (1.0,)*n, (1.0,)*n, (1.0,)*(n-1))


def dense_target(model):
    """Exponential independent oracle, explicitly forbidden to the live sampler."""
    if model.n+model.r > 10:
        raise ValueError("dense reference cap exceeded")
    words = list(product((1, -1), repeat=model.n+model.r))
    diag = np.array([model.diagonal_energy(w[:model.n], w[model.n:]) for w in words])
    G = np.zeros((len(words), len(words)))
    for z in range(len(words)):
        for i, gamma in enumerate(model.transverse):
            G[z, z ^ (1 << (model.n+model.r-1-i))] = abs(gamma)
    return np.diag(diag), G


def dense_gibbs(model, beta, slices=None):
    V, G = dense_target(model)
    if slices is None:
        E = expm(-beta*(V-G))
    else:
        S = np.diag(np.exp(-beta*np.diag(V)/(2*slices)))
        E = np.linalg.matrix_power(S @ expm(beta*G/slices) @ S, slices)
    return E/np.trace(E)


def path_law(model, beta, slices):
    if type(slices) is not int or slices < 1 or model.n*slices+model.r > 12:
        raise ValueError("exhaustive path reference cap exceeded")
    paths = np.array(list(product((1, -1), repeat=slices)))
    shape = (len(paths),)*model.n+(2,)*model.r
    logs = np.empty(shape)
    for state in np.ndindex(shape):
        q, R = paths[list(state[:model.n])], SPINS[list(state[model.n:])]
        weight = -beta*float(np.mean(model.diagonal_energy(q, R)))
        for i, gamma in enumerate(model.transverse):
            flips = int(np.count_nonzero(q[i] != np.roll(q[i], 1)))
            if flips:
                t = tanh(beta*abs(gamma)/slices)
                weight += flips*log(t) if t else -np.inf
        logs[state] = weight
    return np.exp(logs-logsumexp(logs))


def exact_influences(law):
    """Exhaust every boundary pair, not a sampled autocorrelation proxy."""
    C = np.zeros((law.ndim, law.ndim))
    for i in range(law.ndim):
        for j in range(law.ndim):
            if i == j:
                continue
            others = [k for k in range(law.ndim) if k not in (i, j)]
            for context in product(*(range(law.shape[k]) for k in others)):
                index = [slice(None)]*law.ndim
                for k, value in zip(others, context):
                    index[k] = value
                conditionals = []
                for value in range(law.shape[j]):
                    index[j] = value
                    p = law[tuple(index)]
                    if p.sum() == 0:
                        continue
                    conditionals.append(p/p.sum())
                for a, p in enumerate(conditionals):
                    for q in conditionals[:a]:
                        C[i, j] = max(C[i, j], float(abs(p-q).sum()/2))
    return C


def exact_transition(law):
    if law.size > 512:
        raise ValueError("transition reference cap exceeded")
    P = np.zeros((law.size, law.size))
    for state in np.ndindex(law.shape):
        row = np.ravel_multi_index(state, law.shape)
        for i in range(law.ndim):
            index = list(state)
            index[i] = slice(None)
            probabilities = law[tuple(index)]
            if probabilities.sum() == 0:
                raise ValueError("reference transition expects full path support")
            probabilities = probabilities/probabilities.sum()
            for value, probability in enumerate(probabilities):
                index[i] = value
                P[row, np.ravel_multi_index(tuple(index), law.shape)] += probability/law.ndim
    return P


def packing_radius_upper(n, rank):
    """Necessary, never sufficient, radius for injective low-weight syndromes."""
    if type(n) is not int or type(rank) is not int or not 0 <= rank <= n or n < 1:
        raise ValueError("integer length and valid parity rank required")
    volume = 0
    for d in range(n+1):
        volume += comb(n, d)
        if volume > 2**rank:
            return d-1
    return n


def quantum_window_upper(n, rank, eta, J0=1.0):
    """Optimistic envelope for ONLY the published norm/Taylor certificate."""
    if not 0 < eta < 1 or not np.isfinite(J0) or J0 <= 0:
        raise ValueError("positive strength and 0<eta<1 required")
    d = packing_radius_upper(n, rank)
    ell, k = log(1/eta), d+1
    beta = ((sqrt(k+ell/6)-sqrt(ell/2))**2/(J0*(5*n-1))) if k >= ell/3 else None
    return {"n": n, "parity_rank_upper": rank, "packing_radius_upper": d,
            "eta": eta, "optimistic_beta_upper": beta,
            "actual_decoder_supplied": False, "norm_bound_used": J0*(5*n-1),
            "bound_on_ALL_quantum_algorithms": False}


def regular_control(n=24, seed=261006667):
    """Explicit regular incidence input; no distance or decoder promise."""
    if type(n) is not int or n < 8 or n % 2:
        raise ValueError("even control size at least eight required")
    rng, r = np.random.default_rng(seed), n//2
    for _ in range(10000):
        sockets = rng.permutation(np.repeat(np.arange(r), 6)).reshape(n, 3)
        if any(len(set(row)) != 3 for row in sockets):
            continue
        F = np.zeros((r, n), dtype=int)
        for i, row in enumerate(sockets):
            F[row, i] = 1
        if nmod_mat(F.tolist(), 2).rank() == r:
            return ChainTarget(tuple(tuple(map(int, row)) for row in F),
                               (1.0,)*n, (1.0,)*n, (1.0,)*n, (1.0,)*n, (1.0,)*(n-1))
    raise RuntimeError("control generation exhausted; no selected result may be substituted")


def small_control():
    return ChainTarget(((1, 1, 0), (0, 1, 1)), (0.7, -1.0, 0.4),
                       (0.2, -0.3, 0.5), (-0.8, 0.6, 0.3), (0.9, -0.4, 0.7), (-0.8, 0.6))


def run_audit():
    dependencies = [Path(__file__), ROOT/"theorems/parity_block_usd_prange.py",
                    ROOT/"theorems/ternary_certified_noise_sampler.py", ROOT/"theorems/ternary_measured_lattice_decoder.py"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}
    model, beta = small_control(), 0.08
    rho = dense_gibbs(model, beta)
    rows = []
    for M in (1, 2, 4, 8, 16):
        approx = dense_gibbs(model, beta, M)
        rows.append({"slices": M, "trace_distance": float(abs(np.linalg.eigvalsh(rho-approx)).sum()/2),
                     "computational_TV": float(abs(np.diag(rho)-np.diag(approx)).sum()/2),
                     "analytic_bound": trotter_bound(beta, model.norm_bound, M)})
    law = path_law(model, beta, 2)
    C, actual = influence_bounds(model, beta), exact_influences(law)
    P = exact_transition(law)
    pi = law.ravel()
    detailed = float(abs(pi[:, None]*P-pi[None, :]*P.T).max())
    budget = sampling_budget(model, beta, 0.05)
    # All starting states, not a favorable initial trace.
    power = np.linalg.matrix_power(P, budget["updates"])
    worst_tv = float(abs(power-pi[None, :]).sum(axis=1).max()/2)
    windows = []
    for n in (64, 256, 1024, 4096):
        row = quantum_window_upper(n, n//2, 0.005)
        row["regular_3_6_alpha_upper_at_optimistic_beta"] = regular_influence_bound(3, 6, row["optimistic_beta_upper"])
        windows.append(row)
    live = sample(regular_control(), 0.02, 0.05)
    pin_controls = []
    for beta_pin in (0.08, 0.7):
        control = exact_pinning_control(model, beta_pin)
        control["bound"] = pinning_error_bound(model, beta_pin, 3)
        pin_controls.append(control)
    rep = repetition_control()
    pin_live = sample_via_source(rep, 0.03, 0.1, rep.n)
    pin_live["distance_witness"] = {"kernel_dimension": rep.n-int(nmod_mat(rep.F, 2).rank()),
                                    "all_ones_in_kernel": all(sum(row) % 2 == 0 for row in rep.F)}
    pin_live["direct_target_alpha_fails"] = float(influence_bounds(rep, 0.03).sum(axis=0).max())
    pin_live["known_easy_repetition_code_calibration_ONLY"] = True
    interval_audit = certified_interval_update_audit(model, beta, 0.05, bits=64, max_coin_bits=96, seed=1986)
    if hashes != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}:
        raise RuntimeError("producer changed during audit")
    return {"schema_version": 2, "status": "MATCHED_CLASSICAL_WINDOW_AND_INTERVAL_UPDATE_BOUNDS_REVIEW_PENDING",
            "source_sha256": hashes,
            "literature": ["https://arxiv.org/abs/2610.06667", "https://arxiv.org/abs/2609.35101",
                           "https://arxiv.org/abs/2002.02232"],
            "bounded_noncommuting_control": asdict(model), "beta_control": beta,
            "Trotter_controls": rows, "influence_bound": C.tolist(), "exhaustive_influence": actual.tolist(),
            "influence_bound_violation": float(max(0, (actual-C).max())),
            "detailed_balance_residual": detailed, "worst_start_TV_after_certified_updates": worst_tv,
            "mixing_bound": budget["mixing_TV_bound"], "optimistic_quantum_windows": windows,
            "regular_3_6_asymptotic": {"packing_implies_tau_less_than": "1/8", "published_beta_J_upper": "1/40",
                                       "classical_alpha_upper": "3/4", "integer_entropy_witness": [2**20, 7**7]},
            "live_classical_sample": live,
            "source_pinning_controls": pin_controls, "source_pinning_live": pin_live,
            "outward_interval_conditional_update_audit": interval_audit,
            "source_pinning_general_claim": "For this Pauli-chain family, the published beta<tau/(5J0), d>2tau*N window admits computational-basis classical sampling by easy-source worldlines and sparse pinning. Local derivation review pending; not a TFD simulation or a claim about other transduction sources.",
            "scope": {"computational_basis_samples_only": True, "TFD_dequantized": False,
                      "all_relative_decoding_families_dequantized": False, "quantum_advantage_claimed": False,
                      "independent_review_complete": False, "roundoff_certified": False,
                      "interval_conditional_update_bounds_certified": True,
                      "prng_coins_certified_random": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_audit()
    print(json.dumps({k: report[k] for k in ("status", "influence_bound_violation", "detailed_balance_residual",
                                           "worst_start_TV_after_certified_updates",
                                           "outward_interval_conditional_update_audit")}))
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")


if __name__ == "__main__":
    main()

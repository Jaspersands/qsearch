"""Three-point anisotropic residual DQI, using ONE polynomial syndrome.

Local derivation REVIEW PENDING. Known Fourier/Prony primitives. This changes
the explicit problem; it is not an advantage claim or a compiled circuit.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import random
import sys
import time

import numpy as np
from flint import nmod_mat
from flint.utils.flint_exceptions import DomainError

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.nonlinear_residual_lift import canonical, evaluate, load_reference
from theorems.prime_character_finite_readout import (
    mean_tail_lower, propose_weights, rayleigh_interval, sqrt_interval,
)
from theorems.prime_character_interleaved_probe import decode_burst, syndrome
from theorems.prime_character_opi import interpolate, ring

REPORT = ROOT/"research/phase_workbench/cubic_orbit_decoder.json"


@dataclass(frozen=True)
class Domain:
    p: int
    n: int
    zeta: int
    eta: int
    orbits: tuple[tuple[int, int, int], ...]

    @classmethod
    def create(cls, p, n, M=None):
        ring(p)
        if p % 3 != 1 or p > 4093:
            raise ValueError("reference needs p=1 mod3 and p<=4093; not a theorem field limit")
        if type(n) is not int or n < 3 or n % 3:
            raise ValueError("positive dimension divisible by three required")
        maximum = (p-1)//3
        M = maximum if M is None else M
        if type(M) is not int or not 1 <= M <= maximum or n > 3*M:
            raise ValueError("distinct physical orbits must contain the polynomial dimension")
        zeta = next(pow(g, maximum, p) for g in range(2, p) if pow(g, maximum, p) != 1)
        eta = next(a for a in range(2, p) if pow(a, (p-1)//2, p) == p-1)
        seen, orbits = set(), []
        for a in range(1, p):
            if a not in seen:
                orbit = tuple(a*pow(zeta, j, p) % p for j in range(3))
                orbits.append(orbit)
                seen.update(orbit)
        return cls(p, n, zeta, eta, tuple(orbits[:M]))

    @property
    def M(self):
        return len(self.orbits)

    @property
    def K(self):
        return self.n//3

    def specification(self):
        return {"p": self.p, "n": self.n, "M": self.M, "zeta": self.zeta,
                "eta_nonsquare": self.eta, "orbits": [list(o) for o in self.orbits]}


def orbit_syndrome(domain, labels):
    p = domain.p
    if len(labels) != domain.M:
        raise ValueError("one three-frequency vector per physical orbit required")
    for row in labels:
        canonical(row, 3, p)
    folded = [[sum(u*pow(a, r, p) for u, a in zip(label, orbit)) % p
               for label, orbit in zip(labels, domain.orbits)] for r in range(3)]
    nodes = [pow(o[0], 3, p) for o in domain.orbits]
    return [[sum(value*pow(z, j, p) for value, z in zip(row, nodes)) % p
             for j in range(domain.K)] for row in folded]


def scalar_errors(domain, labels):
    error = [0]*(domain.p-1)
    for orbit, label in zip(domain.orbits, labels):
        for a, value in zip(orbit, label):
            error[a-1] = value
    return error


def decode_orbits(domain, cap, rows):
    if type(cap) is not int or not 1 <= cap < domain.K or len(rows) != 3:
        raise ValueError("three syndrome rows and a cap strictly below K required")
    p = domain.p
    decoded = decode_burst(p, p-1, domain.K, cap, rows)
    if decoded["status"] != "VERIFIED_UNIQUE_BURST":
        return {"status": "ABSTAIN", "decoder": decoded}
    by_cube = {pow(o[0], 3, p): i for i, o in enumerate(domain.orbits)}
    if any(j+1 not in by_cube for j in decoded["support"]):
        return {"status": "ABSTAIN_OUTSIDE_PUBLIC_ORBITS", "decoder": decoded}
    labels = [[0]*3 for _ in domain.orbits]
    for j in decoded["support"]:
        i = by_cube[j+1]
        a = domain.orbits[i][0]
        row_values = [decoded["error_rows"][r][j]*pow(a, -r, p) % p for r in range(3)]
        labels[i] = [sum(row_values[r]*pow(domain.zeta, -l*r, p) for r in range(3))
                     *pow(3, -1, p) % p for l in range(3)]
    if orbit_syndrome(domain, labels) != rows:
        raise ArithmeticError("unfolding changed the original polynomial syndrome")
    return {"status": "VERIFIED_UNIQUE_ORBIT_LABEL", "labels": labels,
            "decoder": decoded, "uniqueness_cap": cap, "extra_quantum_copies": 0,
            "original_polynomial_output_registers": 1,
            "three_rows_are_correlated_parts_of_one_syndrome": True}


def cap_columns(domain, cap, support, labels):
    if len(support) != len(labels) or len(set(support)) != len(support):
        raise ValueError("distinct support with one value vector per orbit required")
    if type(cap) is not int or not 0 <= cap < domain.K:
        raise ValueError("cap below K required")
    for i, label in zip(support, labels):
        if type(i) is not int or not 0 <= i < domain.M:
            raise ValueError("public orbit index required")
        canonical(label, 3, domain.p)
    return [[sum(u*pow(a, k, domain.p) for u, a in zip(label, domain.orbits[i])) % domain.p
             for i, label in zip(support, labels)] for k in range(domain.n-3*cap)]


def rank_failure_bound(p, m, n, degree, cap):
    """Projective-nullvector count, including the saturated random-column case."""
    ring(p)
    if (any(type(v) is not int for v in (m, n, degree, cap)) or m < 2
            or (p-1) % m or n % m or not m <= n <= p-1
            or not 0 <= degree <= cap < n//m):
        raise ValueError("valid orbit size, syndrome dimension and radii required")
    L = n-m*cap
    if L < degree:
        raise ValueError("at least D cap equations needed for this certificate")
    bound = Q(0)
    terms = []
    for t in range(1, degree+1):
        rank_random = min(L, (m-1)*t)
        kernel = t-min(L, m*t)+rank_random
        term = Q(comb(degree, t)*(p**kernel-1), (p-1)*p**rank_random)
        bound += term
        terms.append({"support": t, "random_column_rank": rank_random,
                      "admissible_nullvector_dimension": kernel, "term_exact": str(term)})
    return {"p": p, "orbit_size": m, "degree": degree, "cap": cap,
            "cap_equations": L, "failure_upper_exact": str(min(Q(1), bound)),
            "terms": terms, "uniform_first_m_minus_one_frequencies_required": True,
            "each_last_frequency_must_be_nonzero": True,
            "folded_rows_assumed_independent_uniform": False}


def score_certificate():
    p, M, n, D, threshold = 2053, 684, 204, 50, 493
    rank = rank_failure_bound(p, 3, n, D, D+1)
    bad = Q(rank["failure_upper_exact"])
    rho = Q(p-1, 2*p)
    source = rayleigh_interval(M, rho, propose_weights(M, rho, D))
    conditional = max(Q(0), Q(source["ambient_Rayleigh_lower_exact"])-sqrt_interval(bad)[1])
    mean = (1-bad)*conditional
    ordinary_degree = (n-3)//6
    return {"p": p, "M": M, "n": n, "degree": D, "guard_cap": D+1,
            "rank": rank, "source_Rayleigh": source,
            "conditional_mean_lower_exact": str(conditional),
            "one_attempt_mean_lower_ABORT_score_zero": str(mean),
            "threshold": threshold, "one_attempt_tail_lower_exact": str(mean_tail_lower(M, mean, threshold)),
            "ordinary_scalar_guarantee_degree": ordinary_degree,
            "ordinary_source_Rayleigh": rayleigh_interval(M, rho, propose_weights(M, rho, ordinary_degree)),
            "compiled_circuit": False, "additional_compilation_TV_error_must_be_charged": True,
            "classical_separation_or_novelty_claimed": False}


def local_fourier(p, b, eta, allowed):
    """Bounded state control; v is the LAST frequency."""
    ring(p)
    if p > 19 or not 0 < b < p or pow(eta, (p-1)//2, p) != p-1:
        raise ValueError("small nondegenerate anisotropic control required")
    canonical(tuple(allowed), (p-1)//2, p)
    if len(set(allowed)) != len(allowed):
        raise ValueError("actual halfset required")
    x, y, z = np.indices((p, p, p))
    indicator = np.isin((z+b*(x*x-eta*y*y)) % p, allowed).astype(float)
    rho = (p-1)/(2*p)
    centered = (indicator-rho)/np.sqrt(rho*(1-rho))
    return indicator, np.fft.fftn(centered)/p**3


def source_phase_control():
    """Check the coherent Gauss PHASE, not just a basis sampling distribution."""
    p, b, eta = 13, 5, 2
    allowed = (1, 3, 4, 7, 9, 10)
    _, actual = local_fourier(p, b, eta, allowed)
    rho = (p-1)/(2*p)
    h = (np.isin(np.arange(p), allowed).astype(float)-rho)/np.sqrt(rho*(1-rho))
    spectrum = np.fft.fft(h)/p
    u0, u1 = np.indices((p, p))
    predicted = np.zeros((p, p, p), complex)
    for v in range(1, p):
        phase = ((-u0*u0+pow(eta, -1, p)*u1*u1)*pow(4*b*v, -1, p)) % p
        # The two Gauss prefactors multiply to chi(eta)=-1. This sign is
        # relative to the inactive orbit and may NOT be dropped globally.
        predicted[:, :, v] = -spectrum[v]/p*np.exp(2j*np.pi*phase/p)
    empty = np.zeros_like(predicted)
    empty[0, 0, 0] = 1
    frame = np.column_stack((empty.ravel(), predicted.ravel()))
    return {"p": p, "eta": eta, "b": b, "allowed": list(allowed),
            "complex_amplitude_max_error": float(np.max(abs(predicted-actual))),
            "local_isometry_gram_error": float(np.max(abs(frame.conj().T@frame-np.eye(2)))),
            "omitting_anisotropic_Gauss_sign_state_distance": float(np.linalg.norm(-predicted-actual)),
            "empty_plus_active_overlap_if_sign_omitted": float(abs(np.vdot(
                (empty+actual).ravel()/np.sqrt(2), (empty-predicted).ravel()/np.sqrt(2)))),
            "active_has_zero_last_frequency_mass": float(np.sum(abs(predicted[:, :, 0])**2)),
            "subset_flag_is_recoverable_from_nonzero_last_frequency": True,
            "local_postselection_needed": False,
            "analytic_state_preparation_identity_NOT_compiled_circuit": True}


def rank_control():
    domain = Domain.create(13, 12)
    uv = tuple(product(range(13), repeat=2))
    records = []
    for fixed in ((1, 1), (2, 7), (0, 0)):
        columns = []
        for i, v in enumerate(fixed):
            columns.append(np.array([[sum(u*pow(a, k, 13) for u, a in
                                           zip((s, t, v), domain.orbits[i])) % 13
                                      for k in range(3)] for s, t in uv]))
        cross = np.cross(columns[0][:, None, :], columns[1][None, :, :]) % 13
        failed = int(np.all(cross == 0, axis=2).sum())
        records.append({"last_frequencies": list(fixed), "draws": 13**4, "failed": failed,
                        "actual_failure_exact": str(Q(failed, 13**4)),
                        "satisfies_source_premise": all(fixed)})
    return {"rows": records, "bound": rank_failure_bound(13, 3, 12, 2, 3),
            "exhaustive_small_control_only": True}


def norm_control():
    p, eta = 7, 3
    counts = [0]*p
    for x, y in product(range(p), repeat=2):
        counts[(x*x-eta*y*y) % p] += 1
    return {"p": p, "eta": eta, "norm_preimage_counts": counts,
            "nonzero_isotropic_vectors": counts[0]-1,
            "local_norm_is_surjective_and_not_a_hardness_assumption": True,
            "split_form_counterexample": {"eta": 1, "direction": [1, 1, 0],
                                          "residual_along_line": [0]*p},
            "no_Fp_affine_line_in_anisotropic_halfset_is_not_general_hardness": True}


def orbit_norm(domain, coefficients):
    c = canonical(coefficients, len(coefficients), domain.p)
    R = ring(domain.p)
    P = R(list(c))
    rotated = R([v*pow(domain.zeta, j, domain.p) % domain.p for j, v in enumerate(c)])
    return P*P-domain.eta*rotated*rotated


def recover_orbit_norm(domain, norm_coefficients):
    """Invert T(P^2), then check an ordinary polynomial square root exactly."""
    q = canonical(norm_coefficients, len(norm_coefficients), domain.p)
    R = ring(domain.p)
    square = R([value*pow((1-domain.eta*pow(domain.zeta, j, domain.p)) % domain.p,
                         -1, domain.p) % domain.p for j, value in enumerate(q)])
    common = {"inverse_square_coefficients": [int(square[j]) for j in range(max(1, square.degree()+1))],
              "polynomial_norm_factor_choice_is_not_needed": True,
              "optimization_of_halfset_score_solved": False}
    try:
        root = square.sqrt()
    except DomainError:
        return {**common, "status": "NO_POLYNOMIAL_SQUARE_ROOT"}
    c = [int(root[j]) for j in range(max(1, root.degree()+1))]
    if orbit_norm(domain, c) != R(list(q)):
        raise ArithmeticError("square-root inverse did not replay the orbit norm")
    return {**common, "status": "VERIFIED_ORBIT_NORM_ROOT", "coefficients": c,
            "root_may_be_negated": bool(root), "full_polynomial_replay": True}


def norm_compatibility_control():
    """An unrestricted polynomial norm need not have a cubic-covariant factor."""
    domain = Domain.create(13, 12)
    target = ring(13)([1, 0, -domain.eta])
    hits = [list(c) for c in product(range(13), repeat=2) if orbit_norm(domain, c) == target]
    leading = [(1-domain.eta*pow(domain.zeta, 2*j, 13)) % 13 for j in range(3)]
    if hits or not all(leading):
        raise ArithmeticError("norm-covariance counterexample failed")
    inverse = recover_orbit_norm(domain, [int(target[j]) for j in range(3)])
    return {"p": 13, "eta": domain.eta, "zeta": domain.zeta,
            "unrestricted_norm_U": [1], "unrestricted_norm_V": [0, 1],
            "norm_polynomial": [int(target[j]) for j in range(3)],
            "all_degree_below_two_orbit_norm_preimages": hits,
            "degree_d_leading_factors_mod_three": leading,
            "exact_coefficient_inverse": inverse,
            "nonzero_leading_factor_forces_degree_at_most_one": True,
            "counterexample_is_to_unrestricted_norm_substitution_only": True,
            "paired_or_triple_optimization_infeasibility_claimed": False}


def observable_control():
    """A 13-vertex kernel witness creates a score alias across five orbits."""
    domain = Domain.create(19, 12)
    p, M = domain.p, domain.M
    points = [a for orbit in domain.orbits[:4] for a in orbit]+[domain.orbits[4][2]]
    weights = []
    for a in points:
        denominator = 1
        for b in points:
            if b != a:
                denominator = denominator*(a-b) % p
        weights.append(pow(denominator, -1, p))
    labels = [[[0]*3 for _ in range(M)] for _ in range(3)]
    for j in range(6):
        labels[0][j//3][j % 3] = weights[j]
        labels[1][2+j//3][j % 3] = -weights[6+j] % p
    labels[2][0][2] = labels[2][2][2] = 1
    target = [tuple(v for j in range(domain.K) for v in
                    [orbit_syndrome(domain, label)[r][j] for r in range(3)]) for label in labels]
    if len(set(target)) != 3:
        raise ArithmeticError("calibration intended a score alias, not a norm alias")
    C = []
    for i in range(M):
        indicator, _ = local_fourier(p, i+1, domain.eta, tuple((i+j) % p for j in range((p-1)//2)))
        C.append(np.fft.fftn(indicator)/p**3)

    # Recover a possible one-orbit observable frequency from the first three
    # moments, then verify all moments. This is not a decoder for source labels.
    inverse = [nmod_mat([[pow(a, k, p) for a in o] for k in range(3)], p).inv()
               for o in domain.orbits]
    source_matrix = np.zeros((3, 3), complex)
    target_matrix = np.zeros((3, 3), complex)
    for j in range(3):
        for k in range(3):
            difference = [[(x-y) % p for x, y in zip(a, b)] for a, b in zip(labels[j], labels[k])]
            supported = [i for i, row in enumerate(difference) if any(row)]
            if not supported:
                source_matrix[j, k] = (p-1)/(2*p)
            elif len(supported) == 1:
                i = supported[0]
                source_matrix[j, k] = C[i][tuple(difference[i])]/M
            delta = [(a-b) % p for a, b in zip(target[j], target[k])]
            if not any(delta):
                target_matrix[j, k] = (p-1)/(2*p)
                continue
            for i, orbit in enumerate(domain.orbits):
                solution = inverse[i]*nmod_mat([[v] for v in delta[:3]], p)
                u = [int(solution[l, 0]) for l in range(3)]
                if all(sum(v*pow(a, power, p) for v, a in zip(u, orbit)) % p == d
                       for power, d in enumerate(delta)):
                    target_matrix[j, k] += C[i][tuple(u)]/M
    alias = target_matrix[0, 1]-source_matrix[0, 1]
    if abs(alias) < 1e-12:
        raise ArithmeticError("constructed observable alias disappeared")
    amplitudes = np.array([0.5, 0.5*alias.conjugate()/abs(alias), 1/np.sqrt(2)], complex)
    accepted = [decode_orbits(domain, 3, orbit_syndrome(domain, label))["status"]
                == "VERIFIED_UNIQUE_ORBIT_LABEL" for label in labels]
    guarded = amplitudes*np.array(accepted)
    source_mean = float(np.vdot(amplitudes, source_matrix@amplitudes).real)
    unsafe_mean = float(np.vdot(amplitudes, target_matrix@amplitudes).real)
    guarded_source = float(np.vdot(guarded, source_matrix@guarded).real)
    guarded_target = float(np.vdot(guarded, target_matrix@guarded).real)
    return {"p": p, "n": domain.n, "M": M, "source_support_radius": 2, "guard_cap": 3,
            "labels": labels, "kernel_points": points, "kernel_values": weights,
            "source_norm": float(np.vdot(amplitudes, amplitudes).real),
            "target_norm": float(np.vdot(amplitudes, amplitudes).real),
            "source_mean": source_mean, "unsafe_mean": unsafe_mean,
            "unsafe_mean_error": abs(unsafe_mean-source_mean), "accepted_labels": accepted,
            "retained_mass": float(np.vdot(guarded, guarded).real),
            "guarded_source_unnormalized_mean": guarded_source,
            "guarded_target_unnormalized_mean": guarded_target,
            "guarded_mean_error": abs(guarded_source-guarded_target),
            "adversarial_sparse_control_not_uniform_frequency_pilot": True,
            "native_failure_probability_bound_does_not_apply_to_this_control": True}


def cubic_information_map(domain, positions):
    """Exact 3x3 cyclic Lagrange maps on K distinct cubic orbits."""
    I = tuple(positions)
    p, M, K = domain.p, domain.M, domain.K
    if len(I) != K or len(set(I)) != K or any(type(i) is not int or not 0 <= i < M for i in I):
        raise ValueError("exactly K distinct public orbit indices required")
    a0 = [o[0] for o in domain.orbits]
    nodes = [pow(a0[j], 3, p) for j in I]
    weights = []
    for z in nodes:
        den = 1
        for other in nodes:
            if z != other:
                den = den*(z-other) % p
        weights.append(pow(den, -1, p))
    L = np.zeros((M, K), dtype=np.int64)
    indexed = {i: j for j, i in enumerate(I)}
    for i in range(M):
        if i in indexed:
            L[i, indexed[i]] = 1
            continue
        z = pow(a0[i], 3, p)
        num = 1
        for node in nodes:
            num = num*(z-node) % p
        for j, node in enumerate(nodes):
            L[i, j] = num*pow(z-node, -1, p)*weights[j] % p
    inv3 = pow(3, -1, p)
    ratio = np.array([[a0[i]*pow(a0[j], -1, p) % p for j in I] for i in range(M)], dtype=np.int64)
    C = np.zeros((3, M, K), dtype=np.int64)
    for s in range(3):
        rt = (ratio*pow(domain.zeta, s, p)) % p
        C[s] = (L*((1+rt+rt*rt) % p)*inv3) % p
    return C


def cubic_orbit_values(domain, coefficients):
    c = canonical(coefficients, domain.n, domain.p)
    p = domain.p
    return (
        np.array([evaluate(c, o[0], p) for o in domain.orbits], dtype=np.int64),
        np.array([evaluate(c, o[1], p) for o in domain.orbits], dtype=np.int64),
        np.array([evaluate(c, o[2], p) for o in domain.orbits], dtype=np.int64),
    )


def cubic_orbit_residuals(domain, multipliers, x, y, w):
    p, eta = domain.p, domain.eta
    b = np.asarray(multipliers, dtype=np.int64)
    return (w + b*((x*x - eta*(y*y % p)) % p)) % p


def independent_cubic_score(domain, multipliers, allowed, coefficients):
    c = canonical(coefficients, domain.n, domain.p)
    p, eta = domain.p, domain.eta
    return sum(
        (evaluate(c, o[2], p) + b*(evaluate(c, o[0], p)**2 - eta*evaluate(c, o[1], p)**2)) % p in row
        for o, b, row in zip(domain.orbits, multipliers, allowed)
    )


def coefficients_from_cubic_information(domain, positions, x, y, w):
    """Reconstruct P(X) = P_0(X^3) + X P_1(X^3) + X^2 P_2(X^3) from K orbits."""
    I = tuple(positions)
    p, K = domain.p, domain.K
    a0 = [domain.orbits[i][0] for i in I]
    nodes = [pow(a, 3, p) for a in a0]
    inv_a0 = [pow(a, -1, p) for a in a0]
    inv3 = pow(3, -1, p)
    parts = []
    for r_idx in range(3):
        vals = []
        for j, i in enumerate(I):
            s_val = (int(x[i])
                     + int(y[i])*pow(domain.zeta, -r_idx, p)
                     + int(w[i])*pow(domain.zeta, -2*r_idx, p)) % p
            vals.append(int(s_val*pow(inv_a0[j], r_idx, p)*inv3 % p))
        poly_r, _ = interpolate(p, nodes, vals)
        parts.append([int(poly_r[k]) for k in range(K)])
    result = []
    for k in range(K):
        result.extend((parts[0][k], parts[1][k], parts[2][k]))
    return tuple(result)


def sample_cubic_information_witness(domain, multipliers, allowed, positions, seed):
    I = tuple(positions)
    C = cubic_information_map(domain, I)
    p, eta = domain.p, domain.eta
    rng = random.Random(seed)
    b = np.asarray(multipliers, dtype=np.int64)
    x_I = np.array([rng.randrange(p) for _ in I], dtype=np.int64)
    y_I = np.array([rng.randrange(p) for _ in I], dtype=np.int64)
    r_I = np.array([rng.choice(sorted(allowed[i])) for i in I], dtype=np.int64)
    w_I = (r_I - b[list(I)]*((x_I*x_I - eta*(y_I*y_I % p)) % p)) % p
    x = (C[0]@x_I + C[2]@y_I + C[1]@w_I) % p
    y = (C[1]@x_I + C[0]@y_I + C[2]@w_I) % p
    w = (C[2]@x_I + C[1]@y_I + C[0]@w_I) % p
    return coefficients_from_cubic_information(domain, I, x, y, w)


def cubic_intrinsic_greedy_search(domain, multipliers, allowed, coefficients, *,
                                  positions=None, max_sweeps=2, batch=512):
    """Exact quartic root_x/root_y and quadratic residual moves on K cubic orbits."""
    if type(max_sweeps) is not int or max_sweeps < 1 or type(batch) is not int or batch < 1:
        raise ValueError("positive sweep and batch budgets required")
    I = tuple(range(domain.K)) if positions is None else tuple(positions)
    p, M, eta = domain.p, domain.M, domain.eta
    b = np.asarray(multipliers, dtype=np.int64)
    allowed_sorted = tuple(tuple(sorted(r)) for r in allowed)
    table = np.zeros((M, p), dtype=bool)
    for i, row in enumerate(allowed_sorted):
        table[i, list(row)] = True

    start = time.perf_counter()
    C = cubic_information_map(domain, I)
    x, y, w = cubic_orbit_values(domain, coefficients)
    res0 = cubic_orbit_residuals(domain, b, x, y, w)
    if not all(table[i, res0[i]] for i in I):
        raise ValueError("starting polynomial must pass every information orbit")
    initial = current = int(table[np.arange(M), res0].sum())
    setup_seconds = time.perf_counter()-start
    row_idx = np.arange(M)[None, :]
    proposed, improvements, scans = 0, 0, 0
    stopped = "SWEEP_BUDGET_EXHAUSTED"
    for sweep in range(max_sweeps):
        changed = False
        for j, anchor in enumerate(I):
            ux, uy, uw = C[0, :, j], C[1, :, j], C[2, :, j]
            vx, vy, vw = C[2, :, j], C[0, :, j], C[1, :, j]
            qx, qy, qw = C[1, :, j], C[2, :, j], C[0, :, j]
            bj = int(b[anchor])
            for kind in ("root_x", "root_y", "residual"):
                c0 = cubic_orbit_residuals(domain, b, x, y, w)
                if kind == "root_x":
                    old_sym = int(x[anchor])
                    symbols = np.arange(p, dtype=np.int64)
                    lx1, lx2 = (ux - 2*bj*old_sym*qx) % p, (-bj*qx) % p
                    ly1, ly2 = (uy - 2*bj*old_sym*qy) % p, (-bj*qy) % p
                    lw1, lw2 = (uw - 2*bj*old_sym*qw) % p, (-bj*qw) % p
                    c1 = (lw1 + 2*b*((x*lx1 - eta*(y*ly1 % p)) % p)) % p
                    c2 = (lw2 + b*((lx1*lx1 + 2*x*lx2 - eta*((ly1*ly1 + 2*y*ly2) % p)) % p)) % p
                    c3 = (2*b*((lx1*lx2 - eta*(ly1*ly2 % p)) % p)) % p
                    c4 = (b*((lx2*lx2 - eta*(ly2*ly2 % p)) % p)) % p
                    curve = np.stack((c0, c1, c2, c3, c4))
                elif kind == "root_y":
                    old_sym = int(y[anchor])
                    symbols = np.arange(p, dtype=np.int64)
                    lx1, lx2 = (vx + 2*bj*eta*old_sym*qx) % p, (bj*eta*qx) % p
                    ly1, ly2 = (vy + 2*bj*eta*old_sym*qy) % p, (bj*eta*qy) % p
                    lw1, lw2 = (vw + 2*bj*eta*old_sym*qw) % p, (bj*eta*qw) % p
                    c1 = (lw1 + 2*b*((x*lx1 - eta*(y*ly1 % p)) % p)) % p
                    c2 = (lw2 + b*((lx1*lx1 + 2*x*lx2 - eta*((ly1*ly1 + 2*y*ly2) % p)) % p)) % p
                    c3 = (2*b*((lx1*lx2 - eta*(ly1*ly2 % p)) % p)) % p
                    c4 = (b*((lx2*lx2 - eta*(ly2*ly2 % p)) % p)) % p
                    curve = np.stack((c0, c1, c2, c3, c4))
                else:
                    old_sym = int(c0[anchor])
                    symbols = np.array(allowed_sorted[anchor], dtype=np.int64)
                    c1 = (qw + 2*b*((x*qx - eta*(y*qy % p)) % p)) % p
                    c2 = (b*((qx*qx - eta*(qy*qy % p)) % p)) % p
                    curve = np.stack((c0, c1, c2))
                best, chosen = current, old_sym
                for offset in range(0, len(symbols), batch):
                    part = symbols[offset:offset+batch]
                    deltas = (part - old_sym) % p
                    val = np.zeros((len(deltas), M), dtype=np.int64)
                    for row in reversed(curve):
                        val = (val*deltas[:, None] + row) % p
                    scores = table[row_idx, val].sum(axis=1)
                    proposed += len(part)
                    loc = int(np.argmax(scores))
                    if int(scores[loc]) > best:
                        best, chosen = int(scores[loc]), int(part[loc])
                scans += 1
                if best > current:
                    d = (chosen - old_sym) % p
                    if kind == "root_x":
                        dx, dy, dw = d, 0, (-bj*(2*old_sym*d + d*d)) % p
                    elif kind == "root_y":
                        dx, dy, dw = 0, d, (bj*eta*(2*old_sym*d + d*d)) % p
                    else:
                        dx, dy, dw = 0, 0, d
                    x = (x + ux*dx + vx*dy + qx*dw) % p
                    y = (y + uy*dx + vy*dy + qy*dw) % p
                    w = (w + uw*dx + vw*dy + qw*dw) % p
                    current, changed = best, True
                    improvements += 1
        if not changed:
            stopped = "COMPLETE_INTRINSIC_COORDINATE_FIXED_POINT"
            break
    result = coefficients_from_cubic_information(domain, I, x, y, w)
    cx, cy, cw = cubic_orbit_values(domain, result)
    if (not np.array_equal(x, cx) or not np.array_equal(y, cy) or not np.array_equal(w, cw)
            or independent_cubic_score(domain, b, allowed_sorted, result) != current):
        raise ArithmeticError("final cubic-orbit polynomial reconstruction failed")
    return {
        "status": stopped,
        "initial_score": initial,
        "final_score": current,
        "information_orbits": list(I),
        "strict_improvements": improvements,
        "coefficients": list(result),
        "work": {
            "candidate_evaluations": proposed,
            "predicate_lookups": proposed*M,
            "complete_coordinate_scans": scans,
            "sweeps_completed": sweep+1,
            "setup_seconds": setup_seconds,
            "total_seconds": time.perf_counter()-start,
            "restarts": 0,
            "hidden_oracle_or_lift": False,
        },
        "original_Horner_and_full_three_point_replay": True,
        "full_classical_portfolio_complete": False,
    }


def cubic_classical_portfolio(domain, multipliers, allowed, *, seed=62947):
    """Predeclared cubic-orbit classical portfolio: initial I0 search + re-anchoring escape."""
    I0 = tuple(range(domain.K))
    c_init = sample_cubic_information_witness(domain, multipliers, allowed, I0, seed)
    run0 = cubic_intrinsic_greedy_search(domain, multipliers, allowed, c_init,
                                         positions=I0, max_sweeps=2)
    x0, y0, w0 = cubic_orbit_values(domain, run0["coefficients"])
    r0 = cubic_orbit_residuals(domain, multipliers, x0, y0, w0)
    passing = [i for i, row in enumerate(allowed) if int(r0[i]) in row]
    rng = random.Random(seed + 101)
    I_reanchored = tuple(sorted(rng.sample(passing, domain.K)))
    run_re = cubic_intrinsic_greedy_search(domain, multipliers, allowed, run0["coefficients"],
                                           positions=I_reanchored, max_sweeps=1)
    best_run = run_re if run_re["final_score"] >= run0["final_score"] else run0
    return {
        "seed": seed,
        "initial_information_set_score": run0["initial_score"],
        "first_manifold_final_score": run0["final_score"],
        "reanchored_escape_final_score": run_re["final_score"],
        "best_score": best_run["final_score"],
        "best_coefficients": best_run["coefficients"],
        "runs": [
            {"run_label": "primary_information_set_I0", **run0},
            {"run_label": "reanchored_information_set_escape", **run_re},
        ],
        "original_Horner_and_full_three_point_replay": True,
        "full_classical_portfolio_complete": False,
    }


def native_control(reference):
    parent, allowed, provenance = load_reference(reference)
    domain = Domain.create(2053, 204)
    if parent.p != domain.p:
        raise ValueError("frozen field mismatch")
    rng = random.Random(62947)
    support = sorted(rng.sample(range(domain.M), 50))
    labels = [[0]*3 for _ in domain.orbits]
    for i in support:
        indicator = np.zeros(domain.p)
        indicator[list(allowed[i])] = 1
        weights = abs(np.fft.fft(indicator)[1:])**2
        labels[i] = [rng.randrange(domain.p), rng.randrange(domain.p),
                     rng.choices(range(1, domain.p), weights=weights, k=1)[0]]
    rows = orbit_syndrome(domain, labels)
    scalar = scalar_errors(domain, labels)
    original = syndrome(domain.p, scalar, domain.n)
    if any(original[r::3] != rows[r] for r in range(3)):
        raise ArithmeticError("three rows are not the original polynomial's syndrome")
    decoded = decode_orbits(domain, 51, rows)
    if decoded["status"] != "VERIFIED_UNIQUE_ORBIT_LABEL" or decoded["labels"] != labels:
        raise ArithmeticError("fixed native basis draw failed; do not reroll")
    ordinary = decode_burst(domain.p, domain.p-1, domain.n, 150, [original])
    bad = [[row[2]]*3 for row in labels]
    bad_decoder = decode_orbits(domain, 51, orbit_syndrome(domain, bad))
    # A planted algebraic round trip checks the native-size square-consistency
    # inverse. It is not a witness found for the optimization task.
    polynomial = [rng.randrange(domain.p) for _ in range(domain.n)]
    polynomial[-1] = 1
    norm = orbit_norm(domain, polynomial)
    inverse = recover_orbit_norm(domain, [int(norm[j]) for j in range(norm.degree()+1)])
    if inverse["status"] != "VERIFIED_ORBIT_NORM_ROOT":
        raise ArithmeticError("native polynomial square inverse failed")
    recovered = inverse["coefficients"]
    if recovered not in (polynomial, [(-v) % domain.p for v in polynomial]):
        raise ArithmeticError("native polynomial square inverse returned a different root")
    multipliers = tuple(parent.multipliers[:domain.M])
    allowed_orbits = tuple(tuple(sorted(r)) for r in allowed[:domain.M])
    portfolio = cubic_classical_portfolio(domain, multipliers, allowed_orbits, seed=62947)
    return {"domain": domain.specification(), "parent_provenance": provenance,
            "changed_problem": "first684 tables/multipliers; r=P(a*zeta^2)+b*(P(a)^2-eta*P(a*zeta)^2), n204",
            "seed": 62947, "support": support, "source_labels": labels, "syndromes": rows,
            "decoder": decoded, "actual_scalar_weight": sum(v != 0 for v in scalar),
            "ordinary_scalar_decoder_status": ordinary["status"],
            "valid_pilot_but_correlated_frequency_countercontrol": bad_decoder,
            "planted_polynomial_norm_round_trip": {
                "original_coefficients": polynomial, "inverse": inverse,
                "optimization_search_or_high_score_witness": False},
            "classical_intrinsic_portfolio": portfolio,
            "basis_draw_only_NOT_quantum_execution_or_failure_rate_estimate": True,
            "multipliers": list(multipliers),
            "published_chain_and_paired_scores_NOT_comparable": True,
            "strong_classical_portfolio_NOT_run": True}


def run_audit(reference):
    result = {"schema": "cubic-orbit-decoder-v2", "status": "LOCAL_DERIVATION_REVIEW_PENDING",
              "certificate": score_certificate(), "rank_control": rank_control(),
              "norm_control": norm_control(), "source_phase_control": source_phase_control(),
              "norm_compatibility_control": norm_compatibility_control(),
              "observable_control": observable_control(),
              "native": native_control(reference), "accepted_speedup_candidate": False}
    paths = (Path(__file__), ROOT/"theorems/prime_character_interleaved_probe.py",
             ROOT/"theorems/prime_character_finite_readout.py",
             ROOT/"theorems/nonlinear_residual_lift.py", ROOT/"theorems/prime_character_opi.py")
    result["dependencies"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in paths}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run_audit(args.reference)
    if args.write:
        REPORT.write_text(json.dumps(result, indent=2)+"\n")
    portfolio = result["native"]["classical_intrinsic_portfolio"]
    print(json.dumps({"status": result["status"],
                      "mean_lower": float(Q(result["certificate"]["one_attempt_mean_lower_ABORT_score_zero"])),
                      "bad_mass_upper": float(Q(result["certificate"]["rank"]["failure_upper_exact"])),
                      "native_scalar_weight": result["native"]["actual_scalar_weight"],
                      "decoder": result["native"]["decoder"]["status"],
                      "classical_initial_score": portfolio["initial_information_set_score"],
                      "classical_best_score": portfolio["best_score"],
                      "unsafe_mean_error": result["observable_control"]["unsafe_mean_error"],
                      "guarded_mean_error": result["observable_control"]["guarded_mean_error"],
                      "strong_classical_portfolio_NOT_run": True}, indent=2))


if __name__ == "__main__":
    main()

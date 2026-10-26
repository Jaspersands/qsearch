"""Balanced signed pilots for public log-Cauchy decoding.

Constructive proof candidate, independent review pending. No speedup admission.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import fmpz, fmpz_mat, fq_default_poly_ctx, nmod_mat
import numpy as np

from theorems.explicit_quadratic_opi import field, element, encoded
from theorems.nonlinear_filter_pinning import enclose
from theorems.prime_character_finite_readout import sqrt_interval

REPORT = ROOT / "research/phase_workbench/balanced_signed_mpi.json"


def license_box(evaluations, positive_cap, negative_cap, moment=1):
    if any(type(x) is not int or x < 0 for x in
           (evaluations, positive_cap, negative_cap, moment)):
        raise ValueError("nonnegative integer degree budgets required")
    required = positive_cap+negative_cap+moment+1
    if evaluations < required:
        raise ValueError("rational cross-product degree does not certify separation")
    return {"evaluations": evaluations, "positive_cap": positive_cap,
            "negative_cap": negative_cap, "moment_order": moment,
            "strict_root_bound_required": required, "prime_group_order_required": False}


def multinomial_box(trials, plus_cap, minus_cap, active_probability):
    """Exact probability for counts of {+, -, 0}; no floating tail estimate."""
    if type(trials) is not int or trials < 0:
        raise ValueError("nonnegative trial count required")
    if type(plus_cap) is not int or type(minus_cap) is not int:
        raise ValueError("integer count caps required")
    t = active_probability
    if not isinstance(t, Q) or not 0 < t < 1:
        raise ValueError("exact active probability in (0,1) required")
    if min(plus_cap, minus_cap) < 0:
        return Q(0)
    plus, denominator = (t/2).as_integer_ratio()
    zero = denominator-2*plus
    start, total = zero**trials, 0
    for a in range(min(trials, plus_cap)+1):
        term = start
        for b in range(min(trials-a, minus_cap)+1):
            total += term
            if b < min(trials-a, minus_cap):
                term, remainder = divmod(term*(trials-a-b)*plus, (b+1)*zero)
                if remainder:
                    raise ArithmeticError("multinomial integer recurrence failed")
        if a < min(trials, plus_cap):
            start, remainder = divmod(start*(trials-a)*plus, (a+1)*zero)
            if remainder:
                raise ArithmeticError("multinomial integer recurrence failed")
    return Q(total, denominator**trials)


def mean_certificate(length, evaluations, cap, t):
    if type(length) is not int or length < 1:
        raise ValueError("positive number of coordinates required")
    budget = license_box(evaluations, cap, cap)
    Z = multinomial_box(length, cap, cap, t)
    edge = multinomial_box(length-1, cap-1, cap, t)
    lo, hi = sqrt_interval(2*t*(1-t), 192)
    lower, upper = enclose(lo*edge/Z), enclose(hi*edge/Z, upper=True)
    # A row-sum upper bound on the old uniform-sign degree<=cap Jacobi matrix.
    off = [sqrt_interval(Q((k+1)*(length-k), 2), 192)[1]
           for k in range(min(cap, length))]
    old_upper = max((([Q(0)]+off)[k]+(off+[Q(0)])[k]
                     for k in range(len(off)+1)), default=Q(0))/length
    return {"length": length, "license": budget, "active_probability": str(t),
            "normalization_lower": str(enclose(Z)), "normalization_upper": str(enclose(Z, upper=True)),
            "edge_probability_lower": str(enclose(edge)), "edge_probability_upper": str(enclose(edge, upper=True)),
            "mean_cosine_lower": str(lower), "mean_cosine_upper": str(upper),
            "ideal_tail": {"threshold": "3/10",
                           "probability_lower": str(max(Q(0), (lower-Q(3, 10))/Q(7, 10))),
                           "proof": "mean <= threshold*(1-tail)+tail; score_fraction <=1"},
            "old_radial_degree_cap_mean_upper": str(enclose(old_upper, upper=True)),
            "source_preparation": "conditional multinomial class weights and uniform ternary arrangements",
            "postselection_assumed_free": False,
            "optional_heralded_source_expected_attempts_upper": str(enclose(1/Z, upper=True))}


@lru_cache(maxsize=4)
def presentation(bits):
    """Explicit field/log tables, cost O(2^bits); never treated as free advice."""
    if type(bits) is not int or not 3 <= bits <= 16:
        raise ValueError("reference table implementation supports 3..16 bits")
    F, order = field(bits), (1 << bits)-1
    factors = [int(p) for p, _ in fmpz(order).factor()]
    generator = F.gen()
    if any(generator**(order//p) == F.one() for p in factors):
        generator = next(element(bits, x) for x in range(2, order+1)
                         if all(element(bits, x)**(order//p) != F.one() for p in factors))
    powers, logs, value = [], [-1]*(order+1), F.one()
    for j in range(order):
        word = encoded(value)
        if logs[word] != -1:
            raise ArithmeticError("generator did not have full multiplicative order")
        logs[word] = j
        powers.append(value)
        value *= generator
    if value != F.one() or any(x < 0 for x in logs[1:]):
        raise ArithmeticError("incomplete logarithm table")
    return tuple(powers), tuple(logs), encoded(generator)


def points(bits, length, evaluations):
    presentation(bits)
    if (type(length) is not int or type(evaluations) is not int
            or length < 1 or evaluations < 1 or length+evaluations > 1 << bits):
        raise ValueError("distinct disjoint supports must fit the field")
    return tuple(range(length)), tuple(range(length, length+evaluations))


def walsh(vector, modulus):
    result = [int(v) % modulus for v in vector]
    if not result or len(result) & (len(result)-1):
        raise ValueError("power-of-two transform length required")
    step = 1
    while step < len(result):
        for start in range(0, len(result), 2*step):
            for j in range(start, start+step):
                a, b = result[j], result[j+step]
                result[j], result[j+step] = (a+b) % modulus, (a-b) % modulus
        step *= 2
    return result


@lru_cache(maxsize=4)
def trace_indices(bits):
    masks = [sum(int((element(bits, 1 << b)*element(bits, 1 << i)).trace()) << i
                 for i in range(bits)) for b in range(bits)]
    indices = [0]
    for word in range(1, 1 << bits):
        low = word & -word
        indices.append(indices[word ^ low] ^ masks[low.bit_length()-1])
    if len(set(indices)) != 1 << bits:
        raise ArithmeticError("degenerate trace pairing")
    return tuple(indices)


def log_cauchy_product(bits, vector):
    """Exact full convolution with log(0):=0; restrict disjoint rows afterward."""
    if len(vector) != 1 << bits:
        raise ValueError("zero-extended full-field input required")
    order = (1 << bits)-1
    _, logs, _ = presentation(bits)
    transformed = walsh(vector, order)
    for s, index in enumerate(trace_indices(bits)):
        transformed[index] = transformed[index]*(logs[s] if s else 0) % order
    # q=2^h equals 1 modulo q-1, so no inverse scale is needed.
    return tuple(walsh(transformed, order))


def fast_public_matvec(bits, supports, evaluations, x):
    """Compute B @ x mod N via log_cauchy_product with zero-extension and restriction."""
    presentation(bits)
    order = (1 << bits)-1
    if len(x) != len(evaluations) or any(type(int(v)) is not int for v in x):
        raise ValueError("one integer coordinate per evaluation point required")
    if len(set(supports+evaluations)) != len(supports)+len(evaluations):
        raise ValueError("distinct disjoint supports and evaluations required")
    extended = [0]*(1 << bits)
    for z, value in zip(evaluations, x):
        extended[z] = int(value) % order
    full = log_cauchy_product(bits, extended)
    return tuple(full[t] for t in supports)


def module_and_rank_audit(bits, length, evaluations):
    """Verify exact F_N rank for prime N and Z_N Smith-normal-form invariants for composite N."""
    supports, eval_pts = points(bits, length, evaluations)
    order = (1 << bits)-1
    prime = bool(fmpz(order).is_prime())
    _, logs, _ = presentation(bits)
    B = [[logs[t ^ z] for z in eval_pts] for t in supports]
    record = {
        "bits": bits,
        "cyclic_order": order,
        "order_is_prime": prime,
        "rows": length,
        "columns": evaluations,
        "log_table_entries_charged": 1 << bits,
    }
    if prime:
        rank = int(nmod_mat(B, order).rank())
        top_rank = int(nmod_mat(B[:evaluations], order).rank()) if length >= evaluations else rank
        record.update({
            "field_rank": rank,
            "full_column_rank": rank == evaluations,
            "first_n_rows_rank": top_rank,
            "first_n_rows_invertible_over_Z_N": top_rank == evaluations,
        })
        if evaluations <= 16:
            stacked = B + [[order if i == j else 0 for j in range(evaluations)]
                           for i in range(evaluations)]
            snf = fmpz_mat(stacked).snf()
            record["Z_N_smith_invariant_factors"] = [
                math.gcd(int(snf[j, j]), order) for j in range(evaluations)
            ]
        return record

    stacked = B + [[order if i == j else 0 for j in range(evaluations)]
                   for i in range(evaluations)]
    snf = fmpz_mat(stacked).snf()
    invariants = [math.gcd(int(snf[j, j]), order) for j in range(evaluations)]
    nonunit_witness = None
    unit_basis_exists = False
    for rows_idx in combinations(range(length), evaluations):
        sub = [B[i] for i in rows_idx]
        det_mod = int(fmpz_mat(sub).det()) % order
        g = math.gcd(det_mod, order)
        if g == 1:
            unit_basis_exists = True
        elif det_mod != 0 and nonunit_witness is None:
            nonunit_witness = {
                "row_indices": list(rows_idx),
                "determinant_mod_N": det_mod,
                "gcd_with_N": g,
                "invertible_over_Z_N": False,
            }
    record.update({
        "Z_N_smith_invariant_factors": invariants,
        "free_rank_n_submodule_over_Z_N": all(d == 1 for d in invariants),
        "invertible_n_by_n_information_set_exists": unit_basis_exists,
        "nonzero_nonunit_determinant_witness": nonunit_witness,
        "nonzero_composite_determinant_implies_invertible": False,
    })
    return record


def fft_line_search(B, centers, x_init, order, *, basis_inv=None, sweeps=2):
    """Exact O(N log N) coordinate line-search in original or systematic basis (arXiv:2610.06753 D.1)."""
    m, n = B.shape
    x = np.array(x_init, dtype=np.int64, copy=True)
    G = B if basis_inv is None else (B @ basis_inv) % order
    r = (B @ x - centers) % order
    initial_score = float(np.cos(2*np.pi*r/order).mean())
    row_idx = np.arange(N_val := order)
    del row_idx
    improvements = 0
    scans = 0
    for _ in range(sweeps):
        changed = False
        for j in range(n):
            col = G[:, j]
            weights = np.exp(2j*np.pi*r/order)
            hist = (np.bincount(col, weights=weights.real, minlength=order)
                    + 1j*np.bincount(col, weights=weights.imag, minlength=order))
            scores = np.fft.ifft(hist).real * (order/m)
            scans += 1
            best_d = int(np.argmax(scores))
            if best_d != 0 and float(scores[best_d]) > float(scores[0]) + 1e-12:
                if basis_inv is None:
                    x[j] = (x[j] + best_d) % order
                else:
                    x = (x + best_d * basis_inv[:, j]) % order
                r = (r + best_d * col) % order
                improvements += 1
                changed = True
        if not changed:
            break
    check_r = (B @ x - centers) % order
    if not np.array_equal(r, check_r):
        raise ArithmeticError("incremental residual drifted from exact B @ x - c mod N")
    final_score = float(np.cos(2*np.pi*r/order).mean())
    return {
        "initial_mean_cosine": initial_score,
        "final_mean_cosine": final_score,
        "strict_improvements": improvements,
        "coordinate_scans": scans,
        "candidate_shifts_evaluated": scans*order,
        "fft_butterflies_charged": scans*order*int(math.ceil(math.log2(order))),
        "assignment": x.tolist(),
    }


def row_subset_lll_attack(B, B_top_inv, G, centers, x_base, order, *, k=20, d=20):
    """LLL + Babai nearest-plane rounding on a (k+d)-row modular sublattice, scored on all m rows."""
    m, n = B.shape
    s = k + d
    if k < 1 or d < 1 or k > n or n + d > m:
        raise ValueError("valid systematic block k and extra row count d required")
    r_base = (B @ x_base - centers) % order
    A_extra = G[n:n+d, :k]
    L = np.zeros((s, s), dtype=np.int64)
    L[:k, :k] = np.eye(k, dtype=np.int64)
    L[:k, k:] = A_extra.T
    L[k:, k:] = order * np.eye(d, dtype=np.int64)
    L_lll = np.array([[int(v) for v in row] for row in fmpz_mat(L.tolist()).lll().tolist()],
                     dtype=np.float64)
    target = np.concatenate([-r_base[:k], -r_base[n:n+d]]).astype(np.float64)
    B_orth = np.zeros_like(L_lll)
    for i in range(s):
        v = L_lll[i].copy()
        for j in range(i):
            v -= (np.dot(L_lll[i], B_orth[j]) / np.dot(B_orth[j], B_orth[j])) * B_orth[j]
        B_orth[i] = v
    coeffs = np.zeros(s, dtype=np.int64)
    rem = target.copy()
    for i in range(s-1, -1, -1):
        c_i = int(np.round(np.dot(rem, B_orth[i]) / np.dot(B_orth[i], B_orth[i])))
        coeffs[i] = c_i
        rem -= c_i * L_lll[i]
    lattice_vec = coeffs @ L_lll.astype(np.int64)
    dy = lattice_vec[:k] % order
    x_lat = (x_base + B_top_inv[:, :k] @ dy) % order
    r_lat = (B @ x_lat - centers) % order
    subset_indices = list(range(k)) + list(range(n, n+d))
    subset_cos = float(np.cos(2*np.pi*r_lat[subset_indices]/order).mean())
    full_cos = float(np.cos(2*np.pi*r_lat/order).mean())
    return {
        "systematic_coordinates_k": k,
        "extra_rows_d": d,
        "lattice_dimension": s,
        "local_subset_residual_rms": float(np.sqrt(np.mean(rem**2))),
        "local_subset_mean_cosine_NOT_global_score": subset_cos,
        "full_m_row_mean_cosine": full_cos,
        "assignment": x_lat.tolist(),
    }


def matched_classical_portfolio(bits=13, length=6000, evaluations=420, seed=261006753):
    """Predeclared matched classical portfolio on the frozen public log-Cauchy instance."""
    t0 = time.perf_counter()
    supports, eval_pts = points(bits, length, evaluations)
    order = (1 << bits)-1
    _, logs, _ = presentation(bits)
    B = np.array([[logs[t ^ z] for z in eval_pts] for t in supports], dtype=np.int64)
    rng = random.Random(seed)
    centers = np.array([rng.randrange(order) for _ in range(length)], dtype=np.int64)
    centers_sha256 = hashlib.sha256(centers.tobytes()).hexdigest()

    rank_info = module_and_rank_audit(bits, length, evaluations)
    if not rank_info["first_n_rows_invertible_over_Z_N"]:
        raise ArithmeticError("predeclared information set I0=(0..n-1) is not invertible")

    # 1. Exact information-set solve on I0 = 0..n-1
    B_I0_inv = np.array(
        [[int(v) for v in row] for row in nmod_mat(B[:evaluations, :].tolist(), order).inv().tolist()],
        dtype=np.int64,
    )
    x_info0 = (B_I0_inv @ centers[:evaluations]) % order
    fast_prod0 = fast_public_matvec(bits, supports, eval_pts, x_info0.tolist())
    explicit_prod0 = (B @ x_info0) % order
    if tuple(explicit_prod0.tolist()) != fast_prod0:
        raise ArithmeticError("fast_public_matvec disagreed with explicit B @ x mod N")
    r_info0 = (explicit_prod0 - centers) % order
    info0_mean = float(np.cos(2*np.pi*r_info0/order).mean())
    info0_outside_mean = float(np.cos(2*np.pi*r_info0[evaluations:]/order).mean())

    # 2. Original-basis FFT line search from x=0 and from x_info0
    orig_from_zero = fft_line_search(B, centers, np.zeros(evaluations, dtype=np.int64), order, sweeps=2)
    orig_from_info0 = fft_line_search(B, centers, x_info0, order, sweeps=1)

    # 3. Systematic-basis FFT line search on I0 (G0 = B @ B_I0^{-1} mod N)
    sys_I0 = fft_line_search(B, centers, x_info0, order, basis_inv=B_I0_inv, sweeps=2)

    # 4. Second disjoint information set I1 = n..2n-1 + systematic-basis FFT
    B_I1_inv = np.array(
        [[int(v) for v in row] for row in nmod_mat(B[evaluations:2*evaluations, :].tolist(), order).inv().tolist()],
        dtype=np.int64,
    )
    x_info1 = (B_I1_inv @ centers[evaluations:2*evaluations]) % order
    sys_I1 = fft_line_search(B, centers, x_info1, order, basis_inv=B_I1_inv, sweeps=2)

    # 5. Row-subset LLL + Babai nearest-plane rounding on s=40 rows, then systematic FFT polish
    G0 = (B @ B_I0_inv) % order
    lll_run = row_subset_lll_attack(B, B_I0_inv, G0, centers, x_info0, order, k=20, d=20)
    lll_polished = fft_line_search(B, centers, np.array(lll_run["assignment"], dtype=np.int64),
                                   order, basis_inv=B_I0_inv, sweeps=2)

    runs = [
        {"method": "information_set_pinning_I0",
         "initial_mean_cosine": info0_mean,
         "final_mean_cosine": info0_mean,
         "pinned_rows_mean_cosine": 1.0,
         "outside_rows_mean_cosine": info0_outside_mean,
         "candidate_shifts_evaluated": 1},
        {"method": "original_basis_fft_from_zero",
         **{k: orig_from_zero[k] for k in ("initial_mean_cosine", "final_mean_cosine",
                                           "strict_improvements", "coordinate_scans",
                                           "candidate_shifts_evaluated")}},
        {"method": "original_basis_fft_from_pinned_I0",
         **{k: orig_from_info0[k] for k in ("initial_mean_cosine", "final_mean_cosine",
                                            "strict_improvements", "coordinate_scans",
                                            "candidate_shifts_evaluated")}},
        {"method": "systematic_basis_fft_I0",
         **{k: sys_I0[k] for k in ("initial_mean_cosine", "final_mean_cosine",
                                   "strict_improvements", "coordinate_scans",
                                   "candidate_shifts_evaluated")}},
        {"method": "systematic_basis_fft_I1",
         **{k: sys_I1[k] for k in ("initial_mean_cosine", "final_mean_cosine",
                                   "strict_improvements", "coordinate_scans",
                                   "candidate_shifts_evaluated")}},
        {"method": "row_subset_lll_babai_rounding",
         "initial_mean_cosine": info0_mean,
         "final_mean_cosine": lll_run["full_m_row_mean_cosine"],
         "local_subset_mean_cosine_NOT_global": lll_run["local_subset_mean_cosine_NOT_global_score"],
         "local_subset_residual_rms": lll_run["local_subset_residual_rms"],
         "polished_mean_cosine": lll_polished["final_mean_cosine"],
         "candidate_shifts_evaluated": lll_polished["candidate_shifts_evaluated"]},
    ]
    best_x = np.array(sys_I0["assignment"], dtype=np.int64)
    best_fast = fast_public_matvec(bits, supports, eval_pts, best_x.tolist())
    best_r = (np.array(best_fast, dtype=np.int64) - centers) % order
    best_score = float(np.cos(2*np.pi*best_r/order).mean())
    if abs(best_score - sys_I0["final_mean_cosine"]) > 1e-12:
        raise ArithmeticError("best portfolio witness failed fast_public_matvec replay")

    return {
        "bits": bits,
        "cyclic_order": order,
        "length": length,
        "evaluations": evaluations,
        "center_seed": seed,
        "centers_sha256": centers_sha256,
        "module_and_rank": rank_info,
        "composite_module_control": module_and_rank_audit(4, 8, 4),
        "fast_matvec_crosschecked_against_explicit_matrix": True,
        "runs": runs,
        "best_method": "systematic_basis_fft_I0",
        "best_mean_cosine": best_score,
        "best_assignment": best_x.tolist(),
        "target_threshold": 0.3,
        "threshold_reached": best_score >= 0.3,
        "all_runs_and_nonimproving_controls_retained": True,
        "full_m_row_objective_scored_on_every_candidate": True,
        "elapsed_seconds_diagnostic": time.perf_counter()-t0,
        "classical_hardness_or_quantum_speedup_proved": False,
    }


def spectrum_control(bits):
    order = (1 << bits)-1
    _, logs, _ = presentation(bits)
    values = [0]+list(logs[1:])
    transformed = walsh(values, order)
    if any(transformed[index] != values[s] for s, index in enumerate(trace_indices(bits))):
        raise ArithmeticError("logarithm Walsh identity failed")
    return {"bits": bits, "cyclic_order": order, "all_frequencies_checked": order+1,
            "zero_eigenvalues_of_full_completion": values.count(0),
            "exact_identity": "sum_x (-1)^Tr(s*x) log_g(x) = log_g(s) mod(q-1), with log_g(0):=0",
            "full_transform_matvec_butterflies": (order+1)*bits,
            "restricted_matrix_rank_inferred": False,
            "optimization_dequantized": False}


def syndrome(bits, supports, evaluations, error):
    _, logs, _ = presentation(bits)
    order = (1 << bits)-1
    if len(error) != len(supports) or any(type(x) is not int for x in error):
        raise ValueError("integer pattern on the given support required")
    if len(set(supports+evaluations)) != len(supports)+len(evaluations):
        raise ValueError("distinct disjoint field points required")
    return tuple(sum(sign*logs[t ^ z] for t, sign in zip(supports, error)) % order for z in evaluations)


def decode(bits, supports, evaluations, observed, cap):
    """Input is only the public points and syndrome; no error or hidden advice."""
    license_box(len(evaluations), cap, cap, 0)
    if len(observed) != len(evaluations):
        raise ValueError("one syndrome entry per evaluation point required")
    order = (1 << bits)-1
    if any(type(s) is not int or not 0 <= s < order for s in observed):
        raise ValueError("canonical cyclic syndrome required")
    if len(set(supports+evaluations)) != len(supports)+len(evaluations):
        raise ValueError("distinct disjoint points required")
    powers, _, _ = presentation(bits)
    R = fq_default_poly_ctx(field(bits))
    interpolant, modulus = R.zero(), R.one()
    values = tuple(powers[s] for s in observed)
    zs = tuple(element(bits, z) for z in evaluations)
    for z, value in zip(zs, values):
        interpolant += modulus*((value-interpolant(z))/modulus(z))
        modulus *= R([-z, field(bits).one()])
    r0, r1, v0, v1 = modulus, interpolant, R.zero(), R.one()
    while r1 and r1.degree() > cap:
        quotient, remainder = divmod(r0, r1)
        r0, r1, v0, v1 = r1, remainder, v1, v0-quotient*v1
    if not r1 or not v1:
        return None
    common = r1.gcd(v1)
    numerator, denominator = r1//common, v1//common
    scale = denominator.leading_coefficient()
    numerator, denominator = numerator/scale, denominator/scale
    if (numerator.degree() > cap or denominator.degree() > cap
            or not numerator.is_monic() or not denominator.is_monic()):
        return None
    if any(denominator(z) == 0 or numerator(z) != value*denominator(z) for z, value in zip(zs, values)):
        return None
    answer, positive, negative = [], 0, 0
    for t in supports:
        x = element(bits, t)
        # fq_default(0) is truthy in python-flint; field zero needs equality.
        a, b = numerator(x) == 0, denominator(x) == 0
        if a and b:
            return None
        answer.append(int(a)-int(b))
        positive += int(a)
        negative += int(b)
    if positive != numerator.degree() or negative != denominator.degree():
        return None
    answer = tuple(answer)
    return answer if syndrome(bits, supports, evaluations, answer) == tuple(observed) else None


def small_control(bits=4):
    """Composite-order exact-label and explicit target-state validation only."""
    m, n, cap, t = 4, 4, 1, Q(1, 3)
    supports, evaluations = points(bits, m, n)
    order = (1 << bits)-1
    patterns = [y for y in product((-1, 0, 1), repeat=m) if y.count(1) <= cap and y.count(-1) <= cap]
    syndromes = {y: syndrome(bits, supports, evaluations, y) for y in patterns}
    if len(set(syndromes.values())) != len(patterns):
        raise ArithmeticError("balanced-box injectivity failed")
    comparisons = 0
    for y in patterns:
        if decode(bits, supports, evaluations, syndromes[y], cap) != y:
            raise ArithmeticError("syndrome-only reconstruction failed")
        for i in range(m):
            for sign in (-1, 1):
                u = list(y)
                u[i] += sign
                image = syndrome(bits, supports, evaluations, tuple(u))
                for other in patterns:
                    comparisons += 1
                    if image == syndromes[other] and tuple(u) != other:
                        raise ArithmeticError("score-observable alias")
    centers = np.arange(m)*2
    assignments = np.array(list(product(range(order), repeat=n)), dtype=np.int64)
    _, logs, _ = presentation(bits)
    B = np.array([[logs[a ^ z] for z in evaluations] for a in supports], dtype=np.int64)
    values = (assignments @ B.T-centers) % order
    amplitude = np.zeros(len(assignments), dtype=np.complex128)
    Z = multinomial_box(m, cap, cap, t)
    for y in patterns:
        active = sum(bool(v) for v in y)
        weight = float((1-t)**(m-active)*(t/2)**active/Z)**.5
        amplitude += weight*np.exp(2j*np.pi*(values @ np.array(y))/order)
    masses = abs(amplitude)**2
    score = np.cos(2*np.pi*values/order).mean(axis=1)
    cert = mean_certificate(m, n, cap, t)
    return {"bits": bits, "cyclic_order": order, "order_is_prime": bool(fmpz(order).is_prime()),
            "decoded_patterns": len(patterns), "observable_pairs_checked": comparisons,
            "target_assignments_enumerated": len(assignments),
            "target_norm": float(masses.mean()), "target_mean_cosine": float((masses*score).mean()),
            "source_mean_interval": [cert["mean_cosine_lower"], cert["mean_cosine_upper"]],
            "scope": "finite validation, not an advantage experiment"}


def native_control():
    bits, m, n, cap = 13, 6000, 420, 209
    supports, evaluations = points(bits, m, n)
    rng = random.Random(261006753)
    selected = rng.sample(range(m), 380)
    error = [0]*m
    for i, position in enumerate(selected):
        error[position] = 1 if i < 190 else -1
    observed = syndrome(bits, supports, evaluations, tuple(error))
    fast = log_cauchy_product(bits, tuple(error)+(0,)*((1 << bits)-m))
    if tuple(fast[z] for z in evaluations) != observed:
        raise ArithmeticError("fast classical convolution disagrees with direct syndrome")
    recovered = decode(bits, supports, evaluations, observed, cap)
    if recovered != tuple(error):
        raise ArithmeticError("native balanced decoding failed")
    outside = tuple(int(i < cap+1) for i in range(m))
    rejected = decode(bits, supports, evaluations, syndrome(bits, supports, evaluations, outside), cap)
    if rejected is not None:
        raise ArithmeticError("unique out-of-box source was incorrectly accepted")
    _, _, generator = presentation(bits)
    return {"bits": bits, "cyclic_order": (1 << bits)-1, "length": m, "evaluations": n,
            "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs())),
            "generator_encoding": generator, "support_points": list(supports),
            "evaluation_points": list(evaluations), "positive_cap": cap, "negative_cap": cap,
            "positive_errors": 190, "negative_errors": 190,
            "positive_positions": sorted(i for i, e in enumerate(error) if e == 1),
            "negative_positions": sorted(i for i, e in enumerate(error) if e == -1),
            "syndrome": list(observed), "exact_recovery": True,
            "outside_positive_count": cap+1, "outside_control_rejected": True,
            "log_table_entries_charged": 1 << bits,
            "optimizer_matrix_rank_claimed": False,
            "paper_instance_seed_reproduced": False,
            "scope": "public decoder control, not a quantum optimizer execution"}


def readout_alias_control():
    """Norm injectivity alone does not license a score expectation."""
    bits, supports, evaluations = 4, (0, 1, 2, 3), (4, 8, 14)
    patterns = [y for y in product((-1, 0, 1), repeat=4)
                if y.count(1) <= 1 and y.count(-1) <= 1]
    images = {syndrome(bits, supports, evaluations, y) for y in patterns}
    y, shifted, other = (-1, 0, 0, 0), (-1, -1, 0, 0), (0, 0, -1, 1)
    left, right = (syndrome(bits, supports, evaluations, v) for v in (shifted, other))
    if len(images) != len(patterns) or left != right:
        raise ArithmeticError("readout countercontrol failed")
    return {"bits": bits, "supports": list(supports), "evaluations": list(evaluations),
            "cap_each_sign": 1, "box_injective": True, "patterns_checked": len(patterns),
            "source": list(y), "coordinate": 1, "added_frequency": -1,
            "shifted": list(shifted), "different_box_pattern": list(other),
            "shared_syndrome": list(left), "mean_license_valid": False}


def report():
    cert = mean_certificate(6000, 420, 209, Q(13, 200))
    portfolio = matched_classical_portfolio()
    return {"schema": "balanced_signed_mpi_v2",
            "status": "constructive_source_and_readout_proof_candidate; independent_review_pending",
            "source": "https://arxiv.org/abs/2610.06753",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "native_mean": cert, "native_decoder": native_control(),
            "matched_classical_portfolio": portfolio,
            "prime_control": small_control(3), "composite_control": small_control(4),
            "readout_alias_countercontrol": readout_alias_control(),
            "classical_spectrum": [spectrum_control(h) for h in (3, 4, 13)],
            "asymptotic": {"group": "Z_(2^h-1), h arbitrary >=3",
                           "Mersenne_prime_infinitude_assumed": False,
                           "density": "n/m -> alpha, 0<alpha<1",
                           "achievable_limit_supremum": "sqrt(2*alpha*(1-alpha)) for alpha<=1/2; 1/sqrt(2) thereafter",
                           "qualification": "choose fixed active probability t<alpha; approach alpha from below; no endpoint tail claim"},
            "blocked": ["independent proof and novelty review", "stronger structural classical attacks",
                        "meaningful external problem reduction", "full coherent precision and gate budget"],
            "quantum_optimizer_executed": False, "speedup_claim_admitted": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"output": str(args.output),
                      "mean_lower": float(Q(result["native_mean"]["mean_cosine_lower"])),
                      "old_radial_upper": float(Q(result["native_mean"]["old_radial_degree_cap_mean_upper"])),
                      "best_classical_portfolio_mean": result["matched_classical_portfolio"]["best_mean_cosine"],
                      "native_errors_recovered": 380, "composite_order_checked": 15,
                      "speedup_claim_admitted": False}))


if __name__ == "__main__":
    main()

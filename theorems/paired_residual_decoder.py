"""Single-polynomial paired DQI with an observable-guarded collaborative decoder.

Local application REVIEW PENDING. Known Prony/DQI primitives, a changed explicit
optimization problem, and no classical separation or large quantum execution.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import random
import sys

import numpy as np
from flint import nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.nonlinear_residual_lift import canonical, evaluate, load_reference
from theorems.prime_character_finite_readout import (
    mean_tail_lower, propose_weights, rayleigh_interval, sqrt_interval,
)
from theorems.prime_character_interleaved_probe import decode_burst, syndrome
from theorems.prime_character_opi import ring

REPORT = ROOT / "research/phase_workbench/paired_residual_decoder.json"


def parameters(p, M, n):
    ring(p)
    if any(type(v) is not int for v in (M, n)) or not 1 <= M <= (p-1)//2:
        raise ValueError("distinct nonzero plus/minus pairs required")
    if not 2 <= n <= 2*M or n % 2:
        raise ValueError("even polynomial dimension bounded by the physical vertices required")


def fold_errors(p, M, left, right):
    canonical(left, M, p)
    canonical(right, M, p)
    return ([int((u+v) % p) for u, v in zip(left, right)],
            [int((i+1)*(u-v) % p) for i, (u, v) in enumerate(zip(left, right))])


def pair_syndrome(p, M, n, left, right):
    parameters(p, M, n)
    A, B = fold_errors(p, M, left, right)
    z = [(i+1)**2 % p for i in range(M)]
    return [[sum(e*pow(x, j, p) for e, x in zip(row, z)) % p for j in range(n//2)]
            for row in (A, B)]


def decode_pairs(p, M, n, cap, rows):
    """Reuse the existing whole-ball Prony verifier, with square-node padding."""
    parameters(p, M, n)
    if type(cap) is not int or not 1 <= cap < n//2:
        raise ValueError("positive pair cap below the per-row syndrome length required")
    if len(rows) != 2:
        raise ValueError("exactly the even and odd rows of ONE polynomial required")
    # The old primitive scans all nonzero nodes. Zero padding is public, not
    # extra quantum copies or an input-dependent support supplied to decoding.
    decoded = decode_burst(p, p-1, n//2, cap, rows)
    if decoded["status"] != "VERIFIED_UNIQUE_BURST":
        return {"status": "ABSTAIN", "decoder": decoded}
    by_square = {(a*a) % p: a for a in range(1, M+1)}
    if any(i+1 not in by_square for i in decoded["support"]):
        return {"status": "ABSTAIN_OUTSIDE_PUBLIC_PAIRS", "decoder": decoded}
    left, right = [0]*M, [0]*M
    inv2 = pow(2, -1, p)
    for i in decoded["support"]:
        a = by_square[i+1]
        A, B = (row[i] for row in decoded["error_rows"])
        left[a-1] = (A+B*pow(a, -1, p))*inv2 % p
        right[a-1] = (A-B*pow(a, -1, p))*inv2 % p
    if pair_syndrome(p, M, n, left, right) != rows:
        raise ArithmeticError("original single-polynomial syndrome replay failed")
    return {"status": "VERIFIED_UNIQUE_PAIR_LABEL", "left": left, "right": right,
            "decoder": decoded, "uniqueness_cap": cap,
            "extra_quantum_copies": 0, "original_polynomial_output_registers": 1}


def cap_rank(p, n, cap, support, left, right):
    """Rank of the factored cap matrix for controls; not the decoder input."""
    if len(support) != len(left) or len(left) != len(right):
        raise ValueError("one value per supported pair required")
    q = n//2-cap
    if q < 0:
        raise ValueError("cap exceeds a syndrome row")
    if not support:
        return 0
    if q == 0:
        return 0
    rows = [[(u+v)*pow(a*a % p, j, p) % p for a, u, v in zip(support, left, right)]
            for j in range(q)]
    rows += [[a*(u-v)*pow(a*a % p, j, p) % p for a, u, v in zip(support, left, right)]
             for j in range(q)]
    return nmod_mat(rows, p).rank()


def failure_bound(p, n, degree, cap):
    """Uniform in support and every fixed NONZERO right-frequency vector."""
    ring(p)
    if any(type(x) is not int for x in (n, degree, cap)) or n % 2 or not 0 <= degree <= cap < n//2:
        raise ValueError("even syndrome budget and valid source/decoder radii required")
    m = n-2*cap
    if m < degree:
        raise ValueError("not enough cap equations to certify every source shell")
    value = sum((Q(comb(degree, t)*(p**(2*t-m)-1), (p-1)*p**t)
                 for t in range(m//2+1, degree+1)), Q(0))
    return min(Q(1), value)


def score_certificate(p=2053, M=1026, n=204, degree=67, threshold=719):
    parameters(p, M, n)
    if type(degree) is not int or not 0 <= degree <= M:
        raise ValueError("valid source-shell degree required")
    cap = degree+1
    bad = failure_bound(p, n, degree, cap)
    rho = Q(p-1, 2*p)
    source = rayleigh_interval(M, rho, propose_weights(M, rho, degree))
    mu = Q(source["ambient_Rayleigh_lower_exact"])
    root = sqrt_interval(bad)[1]
    conditional = max(Q(0), mu-root)
    unconditional = (1-bad)*conditional
    ordinary_degree = (n-2)//4
    ordinary = rayleigh_interval(M, rho, propose_weights(M, rho, ordinary_degree))
    return {"p": p, "M": M, "n": n, "degree": degree, "observable_guard_cap": cap,
            "cap_equations": n-2*cap, "source_Rayleigh": source,
            "rank_failure_upper_exact": str(bad), "rank_failure_sqrt_upper": str(root),
            "herald_success_lower_exact": str(1-bad),
            "conditional_mean_lower_exact": str(conditional),
            "one_attempt_mean_lower_ABORT_score_zero": str(unconditional),
            "threshold": threshold, "one_attempt_tail_lower_exact": str(mean_tail_lower(M, unconditional, threshold)),
            "ordinary_pairwise_guarantee_degree": ordinary_degree,
            "ordinary_pairwise_source_Rayleigh": ordinary,
            "same_as_published_chain_benchmark": False,
            "ideal_mathematical_algorithm_not_compiled_circuit": True,
            "extra_compilation_TV_error_must_be_subtracted_from_mean": True,
            "full_unheralded_target_filter_law_claimed": False,
            "classical_separation_or_novelty_claimed": False}


def local_fourier(p, multiplier, allowed):
    """Small exact-state numerical control, Fourier convention E[f chi(-e)]."""
    ring(p)
    if p > 31:
        raise ValueError("dense local calibration is deliberately bounded")
    canonical(tuple(allowed), (p-1)//2, p)
    if len(set(allowed)) != len(allowed) or not 0 < multiplier < p:
        raise ValueError("valid explicit half-set and nonzero multiplier required")
    x = np.arange(p)[:, None]
    y = np.arange(p)[None, :]
    indicator = np.isin((y+multiplier*x*x) % p, allowed).astype(float)
    rho = (p-1)/(2*p)
    centered = (indicator-rho)/np.sqrt(rho*(1-rho))
    return indicator, np.fft.fft2(centered)/(p*p)


def rank_control():
    """Exhaustive nonzero-right law and a deliberately invalid zero-right law."""
    p, n, cap = 11, 8, 3
    records = []
    for right in ((1, 1), (2, 7), (0, 0)):
        failed = 0
        for left in product(range(p), repeat=2):
            failed += cap_rank(p, n, cap, (1, 2), left, right) < 2
        records.append({"right": list(right), "uniform_left_draws": p*p, "failed": failed,
                        "actual_failure_exact": str(Q(failed, p*p)),
                        "satisfies_nonzero_right_premise": all(right)})
    return {"rows": records, "proved_upper_for_nonzero_right": str(failure_bound(p, n, 2, cap)),
            "calibration_only": True}


def sparse_expectation(p, labels, amplitudes, shifts):
    """Sparse Fourier observable, aggregating collisions instead of deleting them."""
    labels = np.asarray(labels, dtype=np.int64)
    width = labels.shape[1]
    if p**width >= 2**63:
        raise ValueError("bounded sparse reference key would overflow")
    radix = np.array([p**j for j in range(width)], dtype=np.int64)
    keys = labels@radix
    unique, inverse = np.unique(keys, return_inverse=True)
    merged = np.zeros(len(unique), dtype=complex)
    np.add.at(merged, inverse, amplitudes)
    vectors = np.stack([(unique//int(w)) % p for w in radix], axis=1)
    total = 0j
    for shift, coefficient in shifts:
        query = ((vectors-np.asarray(shift)) % p)@radix
        index = np.searchsorted(unique, query)
        valid = index < len(unique)
        matched = np.zeros(len(unique), dtype=bool)
        matched[valid] = unique[index[valid]] == query[valid]
        total += coefficient*np.vdot(merged[matched], merged[index[matched]])
    if abs(total.imag) > 1e-9:
        raise ArithmeticError("Hermitian score acquired an imaginary expectation")
    return float(np.vdot(merged, merged).real), float(total.real)


def guarded_observable_control():
    """A bounded sparse pure-state test where norm alone does not transfer mean.

    Two disjoint degree-two source terms on four pairs; the fifth pair's
    observable creates aliases outside the old exact moment window.
    """
    p, M, n, cap = 11, 5, 8, 3
    predicates, fouriers = zip(*(local_fourier(p, i+1, tuple((i+j*j) % p for j in range(1, 6)))
                                 for i in range(M)))
    frequencies = tuple(product(range(p), range(1, p)))
    labels, amplitudes, guarded = [], [], []
    for support in ((0, 1), (2, 3)):
        for first, second in product(frequencies, repeat=2):
            label = [0]*(2*M)
            amplitude = 1/np.sqrt(2)
            for i, (u, v) in zip(support, (first, second)):
                label[2*i:2*i+2] = (u, v)
                amplitude *= fouriers[i][u, v]
            left = [first[0], second[0]]
            right = [first[1], second[1]]
            good = cap_rank(p, n, cap, tuple(i+1 for i in support), left, right) == 2
            labels.append(label)
            amplitudes.append(amplitude)
            guarded.append(amplitude if good else 0j)
    points = [a for i in range(1, M+1) for a in (i, p-i)]
    V = np.array([[pow(a, j, p) for j in range(n)] for a in points], dtype=np.int64)
    target = np.asarray(labels, dtype=np.int64)@V % p
    source_shifts, target_shifts = [], []
    for i, predicate in enumerate(predicates):
        C = np.fft.fft2(predicate)/(p*p*M)
        for u, v in [(0, 0), *frequencies]:
            shift = [0]*(2*M)
            shift[2*i:2*i+2] = (u, v)
            source_shifts.append((shift, C[u, v]))
            target_shifts.append(((np.asarray(shift)@V % p).tolist(), C[u, v]))
    source_norm, source_mean = sparse_expectation(p, labels, amplitudes, source_shifts)
    target_norm, unsafe_mean = sparse_expectation(p, target, amplitudes, target_shifts)
    kept_norm, guarded_source = sparse_expectation(p, labels, guarded, source_shifts)
    target_kept, guarded_target = sparse_expectation(p, target, guarded, target_shifts)
    return {"p": p, "M": M, "n": n, "degree": 2, "guard_cap": cap,
            "source_nonzero_label_slots": len(labels), "source_norm": source_norm,
            "unguarded_target_norm": target_norm, "source_mean": source_mean,
            "unsafe_target_mean": unsafe_mean, "unsafe_mean_transfer_error": abs(unsafe_mean-source_mean),
            "kept_source_norm": kept_norm, "kept_target_norm": target_kept,
            "rejected_mass": source_norm-kept_norm,
            "guarded_source_unnormalized_mean": guarded_source,
            "guarded_target_unnormalized_mean": guarded_target,
            "guarded_mean_identity_error": abs(guarded_target-guarded_source),
            "known_failure_mass_exact": str(Q(p-1, p*p)),
            "sparse_pure_state_calibration_NOT_large_quantum_execution": True}


def native_controls(reference):
    parent, allowed, provenance = load_reference(reference)
    p, M, n, degree = 2053, 1026, 204, 67
    if parent.p != p:
        raise ValueError("unexpected frozen parent field")
    rng = random.Random(61831)
    support = sorted(rng.sample(range(M), degree))
    left, right = [0]*M, [0]*M
    for i in support:
        # This is a floating basis draw, not a certified randomness device.
        indicator = np.zeros(p)
        indicator[list(allowed[i])] = 1
        spectrum = np.fft.fft(indicator)
        weights = abs(spectrum[1:])**2
        right[i] = rng.choices(range(1, p), weights=weights, k=1)[0]
        left[i] = rng.randrange(p)
    rows = pair_syndrome(p, M, n, left, right)
    recovered = decode_pairs(p, M, n, degree+1, rows)
    scalar_error = [0]*(p-1)
    for i, (u, v) in enumerate(zip(left, right), 1):
        scalar_error[i-1], scalar_error[p-i-1] = u, v
    scalar_syndrome = syndrome(p, scalar_error, n)
    if scalar_syndrome[::2] != rows[0] or scalar_syndrome[1::2] != rows[1]:
        raise ArithmeticError("folded rows changed the original polynomial syndrome")
    ordinary = decode_burst(p, p-1, n, 2*degree, [scalar_syndrome])
    if recovered["status"] != "VERIFIED_UNIQUE_PAIR_LABEL" or (recovered["left"], recovered["right"]) != (left, right):
        raise ArithmeticError("saved fixed-seed basis recovery failed; no reroll permitted")
    # A nonzero-probability bad source outcome must remain an explicit failure.
    bad_rows = pair_syndrome(p, M, n, right, right)
    bad = decode_pairs(p, M, n, degree+1, bad_rows)

    # Feasible information-set comparator for the CHANGED problem, not a lift.
    K = n//2
    values, points = [], []
    for i in range(K):
        x = rng.randrange(p)
        r = rng.choice(sorted(allowed[i]))
        points.extend((i+1, p-i-1))
        values.extend((x, (r-parent.multipliers[i]*x*x) % p))
    V = nmod_mat([[pow(a, j, p) for j in range(n)] for a in points], p)
    c = V.solve(nmod_mat([[x] for x in values], p))
    coefficients = [int(c[j, 0]) for j in range(n)]
    passes = []
    for i in range(M):
        x = evaluate(coefficients, i+1, p)
        y = evaluate(coefficients, p-i-1, p)
        passes.append((y+parent.multipliers[i]*x*x) % p in allowed[i])
    if not all(passes[:K]):
        raise ArithmeticError("feasible interpolation comparator lost a forced pair")
    return {"parent_provenance": provenance,
            "changed_problem": "first1026 halfsets/multipliers; tests on P(i+1),P(-(i+1)); n204",
            "seed": 61831, "source_support_zero_based": support,
            "source_left": left, "source_right": right, "syndromes": rows,
            "decoder": recovered, "ordinary_scalar_decoder_status": ordinary["status"],
            "actual_scalar_weight": sum(v != 0 for v in scalar_error),
            "bad_source_control_status": bad["status"],
            "bad_source_control_decoder": bad["decoder"],
            "basis_draw_NOT_coherent_execution_or_failure_probability_estimate": True,
            "one_information_set_comparator": {"coefficients": coefficients, "passing_tests": sum(passes),
                "forced_pairs": K, "tests": M, "strong_classical_portfolio_NOT_run": True},
            "published_chain_scores_NOT_comparable": True}


def run_audit(reference):
    result = {"schema": "paired-residual-decoder-v1", "status": "LOCAL_DERIVATION_REVIEW_PENDING",
              "certificate": score_certificate(), "rank_control": rank_control(),
              "guarded_observable_control": guarded_observable_control(),
              "native": native_controls(reference), "accepted_speedup_candidate": False}
    result["dependencies"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (Path(__file__), ROOT/"theorems/prime_character_interleaved_probe.py",
                     ROOT/"theorems/prime_character_finite_readout.py",
                     ROOT/"theorems/nonlinear_residual_lift.py")}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run_audit(args.reference)
    if args.write:
        REPORT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"],
        "ideal_one_attempt_mean_lower": float(Q(result["certificate"]["one_attempt_mean_lower_ABORT_score_zero"])),
        "bad_mass_upper": float(Q(result["certificate"]["rank_failure_upper_exact"])),
        "decoder": result["native"]["decoder"]["status"],
        "guarded_mean_error": result["guarded_observable_control"]["guarded_mean_identity_error"],
        "unsafe_mean_error": result["guarded_observable_control"]["unsafe_mean_transfer_error"],
        "classical_information_set_score": result["native"]["one_information_set_comparator"]["passing_tests"]
    }, indent=2))


if __name__ == "__main__":
    main()

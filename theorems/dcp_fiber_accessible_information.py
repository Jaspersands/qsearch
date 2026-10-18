"""All-POVM information certificates from the actual fiber's fourth moment.

Holevo information is not an accessible-information lower bound. The native
weighted fourth-moment problem remains open; finite controls are not a decoder.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from math import log2
from pathlib import Path
from random import Random
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_nonlinear_fiber_pairing import phase_value

REPORT = ROOT / "research/phase_workbench/dcp_fiber_accessible_information.json"


def fiber_geometry(labels, phase_bits, syndrome):
    A = matrix(labels)
    n, m = len(A), len(A[0])
    integer(phase_bits, "bounded phase bits", 3, 24)
    if m > 12 or n > 4:
        raise ValueError("UNKNOWN: explicit fiber calibration cap; no fiber oracle supplied")
    q = 1 << phase_bits
    if any(a >= q for row in A for a in row):
        raise ValueError("canonical full original labels required")
    y = tuple(syndrome)
    if len(y) != n:
        raise ValueError("one mod4 syndrome component per row required")
    for v in y:
        integer(v, "mod4 syndrome", 0, 3)
    assignments = [x for x in range(1 << m) if phase_value(A, x, 4) == y]
    if not assignments:
        raise ValueError("zero-probability syndrome has no normalized fiber ensemble")
    if len(assignments)**2 > 100000:
        raise ValueError("UNKNOWN: explicit pair-moment calibration cap")
    frequencies = [phase_value(A, x, q) for x in assignments]
    if len(set(frequencies)) != len(frequencies):
        raise ValueError("noninjective frequency map: uniform average-state premise fails")
    groups = defaultdict(list)
    for i, a in enumerate(frequencies):
        for j, b in enumerate(frequencies):
            groups[tuple((u+v) % q for u, v in zip(a, b))].append((i, j))
    return A, assignments, frequencies, dict(groups)


def weighted_fourth_moment(groups, weights):
    w = tuple(Fraction(v) for v in weights)
    norm2 = sum(v*v for v in w)
    if not w or not norm2:
        raise ValueError("nonzero weights required")
    if any(not 0 <= i < len(w) or not 0 <= j < len(w) for g in groups.values() for i, j in g):
        raise ValueError("moment group / weight dimension mismatch")
    return sum(sum(w[i]*w[j] for i, j in pairs)**2 for pairs in groups.values())/norm2**2


def moment_certificate(labels, phase_bits, syndrome):
    A, F, frequencies, groups = fiber_geometry(labels, phase_bits, syndrome)
    D = len(F)
    sidon = all(len({tuple(sorted(p)) for p in pairs}) == 1 for pairs in groups.values())
    multiplicity = max(map(len, groups.values()))
    # Cauchy on each ordered-pair bucket covers arbitrary COMPLEX coefficients.
    upper = Fraction(2*D-1, D) if sidon else Fraction(multiplicity)
    uniform = weighted_fourth_moment(groups, [1]*D)
    if not 1 <= uniform <= upper <= D:
        raise ArithmeticError("fourth-moment certificate contradicted by uniform witness")
    return {"full_labels": [list(r) for r in A], "phase_bits": phase_bits,
            "measured_syndrome": list(syndrome), "enumerated_assignments": F,
            "full_frequencies": [list(f) for f in frequencies], "fiber_dimension": D,
            "Born_syndrome_probability_exact": str(Fraction(D, 1 << len(A[0]))),
            "full_frequency_map_injective_on_fiber": True,
            "Sidon_unordered_pair_sums_including_diagonals": sidon,
            "maximum_ordered_pair_sum_multiplicity": multiplicity,
            "uniform_weight_fourth_moment_exact": str(uniform),
            "all_complex_weight_fourth_moment_upper_exact": str(upper),
            "single_block_uniform_prior_all_POVM_information_upper_bits": log2(float(upper)),
            "clean_block_Holevo_information_bits": log2(D),
            "independent_secret_blind_dephasing_also_covered": True,
            "uniform_weight_moment_is_a_bound_for_every_measurement": False,
            "applies_to_nonuniform_posterior_or_adaptive_multi_packet_chain": False,
            "fiber_or_measurement_inverse_supplied": False,
            "selected_matrix_is_native_average_evidence": False,
            "efficient_decoder_supplied": False}


def finite_POVM_control(labels, phase_bits, syndrome):
    c = moment_certificate(labels, phase_bits, syndrome)
    n, D = len(labels), c["fiber_dimension"]
    Q = 1 << (phase_bits-2)
    K = Q**n
    if K*D*D > 200000:
        raise ValueError("UNKNOWN: full uniform-secret POVM calibration cap")
    frequencies = c["full_frequencies"]
    states = np.array([[np.exp(2j*np.pi*sum(a*b for a, b in zip(f, s))/(1 << phase_bits))/np.sqrt(D)
                        for f in frequencies] for s in product(range(Q), repeat=n)])
    if not np.allclose(states.T@states.conj()/K, np.eye(D)/D, atol=1e-12):
        raise ArithmeticError("uniform fiber average-state assertion failed")
    rng = np.random.default_rng(17019)
    random_basis, _ = np.linalg.qr(rng.normal(size=(D, D))+1j*rng.normal(size=(D, D)))
    bases = {"computational": np.eye(D),
             "index_inverse_DFT": np.exp(-2j*np.pi*np.outer(np.arange(D), np.arange(D))/D)/np.sqrt(D),
             "seeded_complex_basis": random_basis}
    measurements = []
    for name, U in bases.items():
        probabilities = np.abs(states@U.T)**2
        marginal = probabilities.mean(axis=0)
        active = probabilities > 1e-30
        ratios = probabilities/np.maximum(marginal, 1e-300)
        info = float(np.sum(probabilities[active]*np.log2(ratios[active]))/K)
        if info > c["single_block_uniform_prior_all_POVM_information_upper_bits"]+1e-11:
            raise ArithmeticError("actual Born measurement refutes all-POVM bound")
        measurements.append({"basis": name, "mutual_information_bits": info,
                             "basis_entries_enumerated": D*D, "likelihood_entries_enumerated": K*D,
                             "measurement_is_gate_compiled": False})
    return c | {"abstract_finite_POVM_controls": measurements,
                "all_uniform_residual_secrets_enumerated": K}


def native_additive_alias_bound(n, width_multiple):
    integer(n, "native components", 4, 4096)
    integer(width_multiple, "original width multiplier", 3, 4)
    m, t = width_multiple*n, n+8
    # Nonzero integer four-vertex differences lie in {-2,-1,0,1,2}^m.
    # Odd coordinates give a uniform mod-q linear form; all-even vectors use q/2.
    numerator = 5**m-3**m+(3**m-1)*2**n
    exact = Fraction(numerator, 1 << (t*n))
    exponent = n*n+n-1 if width_multiple == 3 else n*n-2*n-1
    if exact > Fraction(1, 1 << exponent):
        raise ArithmeticError("native full-source additive-alias union bound failed")
    return {"components": n, "original_phase_bits": t, "original_phase_qubits": m,
            "nonzero_integer_four_vertex_alias_probability_power_of_two_upper_exponent": exponent,
            "native_labels_IID_uniform_on_full_original_modulus": True,
            "holds_simultaneously_for_every_measured_syndrome": True,
            "remaining_moment_problem": "weighted INTEGER Boolean parallelograms within the actual mod4 fiber",
            "constant_or_polylog_all_POVM_information_bound_proved_for_native_fibers": False,
            "native_all_POVM_information_bound_follows_from_uniform_weight_count": False}


def build_report():
    controls = [finite_POVM_control(A, t, y) for A, t, y in (
        (((1, 5, 13, 29),), 6, (1,)),
        (((1, 17, 33, 49),), 6, (1,)),
        (((4, 8, 16),), 5, (0,)))]
    rng = Random(19017)
    fragments = []
    for n in (2, 3, 4):
        A = tuple(tuple(rng.randrange(1 << (n+8)) for _ in range(3*n)) for _ in range(n))
        y = phase_value(A, rng.randrange(1 << (3*n)), 4)
        fragments.append(moment_certificate(A, n+8, y))
    return {"status": "ALL_POVM_FIBER_MOMENT_LEMMA_NATIVE_WEIGHTED_BOUND_OPEN",
            "selected_controls": controls, "selected_native_fragments": fragments,
            "native_additive_alias_bounds": [native_additive_alias_bound(n, w) for w in (3, 4) for n in (8, 32, 128, 256)],
            "uniform_secret_prior_required": True, "single_block_scope": True,
            "arbitrary_finite_POVMs_covered_by_lemma": True,
            "large_Holevo_guarantees_large_accessible_information": False,
            "native_weighted_fourth_moment_bound_resolved": False,
            "known_dyadic_control_refutes_universal_constant_information_bound": True,
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "novelty_claim": False, "actual_natural_source_noise_certified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "finite_POVM_controls": 3,
                      "native_fragments": 3, "native_weighted_bound_resolved": False}))


if __name__ == "__main__":
    main()

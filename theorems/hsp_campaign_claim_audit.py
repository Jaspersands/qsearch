"""Scoped corrections to campaign HSP and hidden-shift impossibility claims.

Uses exact algebra, public arithmetic, matched classical attacks and verified
primary-source parameter regimes. No new quantum speedup is claimed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from flint import fmpq, fmpz
import numpy as np
from scipy.linalg import hadamard

from ternary_measured_lattice_decoder import integer, exact_json

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/HSP_CAMPAIGN_CLAIM_AUDIT.md"
REPORT = ROOT/"research/reductions/hsp_campaign_claim_audit.json"
IDS = ("NEG-UNITRIANGULAR-SUPERCHARACTER-BARRIER",
       "NEG-DIHEDRAL-HSP-SUBSET-SUM-COMMUTANT-BARRIER",
       "NEG-BENT-FUNCTION-HIDDEN-SHIFT-DUAL-DEQUANTIZATION-BARRIER",
       "NEG-LEGENDRE-HIDDEN-SHIFT-CLASSICAL-PRF-DEMARCATION",
       "NEG-HEISENBERG-UNIPOTENT-REPRESENTATION-BOUNDARY")


def nilpotent_parameter_control(extension_degree):
    integer(extension_degree, "positive binary field extension degree", 1)
    r = extension_degree
    return {"family": "U4(F_(2^r))", "extension_degree": r, "field_order": 2**r,
            "group_order": 2**(6*r), "group_encoding_bits": 6*r, "nilpotency_class": 3,
            "only_prime_factor_of_group_order": 2,
            "published_constant_class_bounded_prime_factor_theorem_applies": True,
            "source": "https://arxiv.org/abs/2304.08376",
            "hidden_subgroup_center_bypass_is_a_general_no_go": False,
            "all_growing_nilpotency_classes_solved": False,
            "new_algorithm_or_physical_receiver_implemented": False}


def unitriangular_bypass_control():
    I = np.eye(4, dtype=np.int64)

    def elementary(i, j):
        g = I.copy()
        g[i, j] = 1
        return g

    def inverse(g):
        N = (g-I) % 2
        return (I+N+N@N+N@N@N) % 2

    def commutator(g, h):
        return (g@h@inverse(g)@inverse(h)) % 2

    a, b, c = elementary(0, 1), elementary(1, 2), elementary(2, 3)
    second, third = commutator(a, b), commutator(commutator(a, b), c)
    if not np.array_equal(second, elementary(0, 2)) or not np.array_equal(third, elementary(0, 3)):
        raise ArithmeticError("unitriangular class3 commutator control failed")
    return {"prime": 2, "hidden_cyclic_generator": a.tolist(), "second_commutator": second.tolist(),
            "third_commutator": third.tolist(), "generator_squared": ((a@a) % 2).tolist(),
            "nonidentity_center_intersection": False,
            "constant_class_bounded_prime_factor_algorithm_still_applies": True,
            "explicit_generator_is_given_to_the_hidden_subgroup_algorithm": False}


def heisenberg_weak_direction_control(p):
    integer(p, "odd prime", 3)
    if not fmpz(p).is_prime():
        raise ValueError("prime required")
    probability = fmpq(p-1, p*p)
    half_budget = (p*p+2*(p-1)-1)//(2*(p-1))
    return {"prime": p, "nontrivial_1D_weak_sample_probability": str(probability),
            "first_nontrivial_1D_sample_expected_copies": str(1/probability),
            "half_success_copy_count_union_lower": half_budget,
            "naive_weak_direction_then_dechirp_is_polylog_prime": False,
            "known_polynomial_Heisenberg_algorithms_excluded": False}


def cubic(y):
    return (y&1)*((y >> 1)&1)*((y >> 2)&1)


def mm_value(x, y):
    return ((x&y).bit_count() % 2) ^ cubic(y)


def mm_dual(u, v):
    return ((u&v).bit_count() % 2) ^ cubic(u)


def recover_explicit_mm_shift(width, shifted_evaluator):
    integer(width, "MM half-width at least3", 3)
    calls = 0

    def query(x, y):
        nonlocal calls
        value = shifted_evaluator(x, y)
        if type(value) is not int or value not in (0, 1):
            raise ValueError("binary shifted evaluator required")
        calls += 1
        return value

    origin = query(0, 0)
    b = sum((query(1 << i, 0)^origin) << i for i in range(width))
    a = sum((query(0, (1 << i)^b)^cubic(1 << i)) << i for i in range(width))
    return {"recovered_x_shift": a, "recovered_y_shift": b, "shifted_function_queries": calls,
            "access": "chosen classical queries plus known explicit MM evaluator",
            "legal_under_random_sample_only_access": False}


def mm_control(width, a, b, enumerate_walsh=False):
    integer(width, "MM half-width at least3", 3)
    if type(a) is not int or type(b) is not int or not 0 <= a < 2**width or not 0 <= b < 2**width:
        raise ValueError("actual binary shift halves required")
    result = recover_explicit_mm_shift(width, lambda x, y: mm_value(x^a, y^b))
    if (result["recovered_x_shift"], result["recovered_y_shift"]) != (a, b):
        raise ArithmeticError("matched classical MM shift reconstruction failed")
    result.update({"half_width": width, "function_degree": 3, "dual_degree": 3,
                   "known_dual_CZ_terms": width, "known_dual_CCZ_terms": 1,
                   "higher_degree_forces_exponential_dual_circuit": False,
                   "accepted_speedup_candidate": False})
    if enumerate_walsh:
        if width != 3:
            raise ValueError("complete Walsh calibration is capped at width3")
        values = np.array([(-1)**mm_value(z&7, z >> 3) for z in range(64)], dtype=np.int64)
        spectrum = hadamard(64)@values
        expected = np.array([8*(-1)**mm_dual(z&7, z >> 3) for z in range(64)])
        if not np.array_equal(spectrum, expected):
            raise ArithmeticError("explicit cubic bent dual formula failed")
        # Shift by y1: derivative is x1 + y2*y3, not affine.
        witness = [mm_value(0, y^1)^mm_value(0, y) for y in (0, 2, 4, 6)]
        result.update({"complete_Walsh_entries": spectrum.tolist(), "dual_sign_bits": [mm_dual(z&7, z >> 3) for z in range(64)],
                       "nonaffine_derivative_witness_y": (0, 2, 4, 6), "derivative_values": witness,
                       "four_point_affine_test_XOR": sum(witness) % 2})
    return result


def dyadic_dcp_control(bits):
    integer(bits, "positive supplied phase-state count", 1)
    return {"bits": bits, "modulus": 2**bits, "labels": tuple(1 << j for j in range(bits)),
            "subset_sum_is_binary_encoding_bijection": True,
            "commutant_dimension": 2**bits,
            "exact_inverse_QFT_recovery_probability": "1",
            "inverse_QFT_controlled_rotation_count": bits*(bits-1)//2,
            "ordered_IID_source_event_probability_exponent": -bits*bits,
            "source_probability_base": 2,
            "structured_source_was_assumed_supplied": True,
            "generic_random_DCP_decoder_supplied": False,
            "NP_completeness_inferred_from_commutant_dimension": False}


def legendre_information_control(p, failure_bits=8):
    integer(p, "odd prime Legendre modulus", 3)
    integer(failure_bits, "positive collision confidence", 1)
    if not fmpz(p).is_prime():
        raise ValueError("prime modulus required for the character identity")
    count = (p-1).bit_length()+failure_bits
    collision = fmpq(p-3, 2*p)
    union = min(fmpq(1), (p-1)*collision**count)
    if union > fmpq(1, 2**failure_bits):
        raise ArithmeticError("classical sample identifiability union bound failed")
    r = {"prime": p, "oracle_outputs_include_zero_symbol": True, "distinct_shift_agreements": (p-3)//2,
         "single_uniform_query_collision_probability": str(collision), "random_classical_samples": count,
         "ambiguity_union_upper": str(union), "failure_target": str(fmpq(1, 2**failure_bits)),
         "efficient_classical_shift_decoder_supplied": False,
         "query_identifiability_is_a_runtime_bound": False,
         "all_quantum_processing_of_classical_samples_excluded": False}
    if p <= 101:
        chi = tuple(int(fmpz(x).jacobi(p)) for x in range(p))
        rows = []
        for delta in range(1, p):
            correlation = sum(chi[x]*chi[(x+delta) % p] for x in range(p))
            agrees = sum(chi[x] == chi[(x+delta) % p] for x in range(p))
            if correlation != -1 or agrees != (p-3)//2:
                raise ArithmeticError("exact shifted Legendre identity failed")
            rows.append({"nonzero_shift_difference": delta, "correlation": correlation, "agreements": agrees})
        r["complete_shift_difference_census"] = rows
    else:
        r["large_domain_was_materialized"] = False
    return r


def counted_jacobi(a, modulus):
    integer(modulus, "odd Jacobi modulus at least3", 3)
    if modulus % 2 == 0 or type(a) is not int:
        raise ValueError("integer argument and odd Jacobi modulus required")
    a, n, sign, steps = a % modulus, modulus, 1, 0
    while a:
        while a % 2 == 0:
            a //= 2
            steps += 1
            if n % 8 in (3, 5):
                sign = -sign
        if a % 4 == n % 4 == 3:
            sign = -sign
        a, n = n % a, a
        steps += 1
    return sign if n == 1 else 0, steps


def jacobi_control(a, modulus):
    value, steps = counted_jacobi(a, modulus)
    reference = int(fmpz(a).jacobi(modulus))
    if value != reference:
        raise ArithmeticError("public Jacobi arithmetic disagrees with FLINT")
    return {"argument": a, "odd_modulus": modulus, "modulus_bits": modulus.bit_length(),
            "Jacobi_value": value, "binary_reciprocity_steps": steps,
            "factorization_subroutine_called": False, "matches_independent_FLINT_Jacobi": True,
            "zero_symbol_support_must_be_accounted_for": True,
            "arbitrary_composite_Gauss_cancellation_formula_validated": False,
            "physical_reversible_gate_compiler_supplied": False}


def nonprimitive_shift_control(modulus):
    integer(modulus, "bounded nonprimitive Jacobi modulus", 3)
    if modulus > 101 or modulus % 2 == 0:
        raise ValueError("bounded odd counterexample modulus required")
    values = tuple(int(fmpz(x).jacobi(modulus)) for x in range(modulus))
    classes = {}
    for s in range(modulus):
        table = tuple(values[(x+s) % modulus] for x in range(modulus))
        classes.setdefault(table, []).append(s)
    sizes = {len(c) for c in classes.values()}
    if len(sizes) != 1:
        raise ArithmeticError("translation equivalence classes have inconsistent size")
    return {"modulus": modulus, "Jacobi_table": values, "identical_shift_oracle_classes": tuple(classes.values()),
            "uniform_full_shift_success_upper_even_with_coherent_queries": str(fmpq(len(classes), modulus)),
            "identifiability_is_a_computational_hardness_claim": False,
            "accepted_speedup_candidate": False}


def build_report():
    archived = json.loads((ROOT/"research/registry/quarantined_campaign_negatives.json").read_text())
    active = json.loads((ROOT/"research/registry/negative_results.json").read_text())
    by_id = {row["id"]: row for row in archived}
    if not set(IDS).issubset(by_id) or any(row["id"] in IDS for row in active):
        raise ValueError("the reviewed HSP overclaims are not safely quarantined")
    originals = [by_id[key]["original_record"] for key in IDS]
    return {"status": "HSP_CAMPAIGN_GENERAL_NO_GO_OVERCLAIMS_QUARANTINED",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(), "quarantined_ids": IDS,
            "original_records_sha256": hashlib.sha256(json.dumps(originals, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "nilpotent_parameter_controls": [nilpotent_parameter_control(r) for r in (1, 8, 64, 256)],
            "unitriangular_center_bypass_control": unitriangular_bypass_control(),
            "Heisenberg_weak_direction_controls": [heisenberg_weak_direction_control(p) for p in (7, 31, 2**31-1)],
            "explicit_cubic_MM_controls": [mm_control(m, (1 << (m-1))+3, (1 << (m-2))+1, m == 3) for m in (3, 64, 512)],
            "structured_dyadic_DCP_controls": [dyadic_dcp_control(m) for m in (4, 32, 128)],
            "Legendre_classical_information_controls": [legendre_information_control(p) for p in (7, 13, 31, 101, 2**31-1, 2**127-1)],
            "public_Jacobi_controls": [jacobi_control(a, n) for a, n in ((17, 45), (-13, 105), (1234567, (2**61-1)*(2**127-1)))],
            "nonprimitive_Jacobi_controls": [nonprimitive_shift_control(n) for n in (9, 25, 45)],
            "primary_sources": ["https://arxiv.org/abs/2304.08376", "https://arxiv.org/abs/quant-ph/0501044", "https://arxiv.org/abs/0811.3208"],
            "general_DHSP_polynomial_decoder_supplied": False, "general_hidden_shift_speedup_supplied": False,
            "remaining_campaign_claims_verified": False, "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    r = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(r), indent=2)+"\n")
    print(json.dumps({"status": r["status"], "additional_quarantined_records": 5,
                      "exact_algebra_and_access_controls": 26,
                      "remaining_campaign_claims_verified": False, "new_quantum_speedup_established": False}, indent=2))


if __name__ == "__main__":
    main()

"""Exact literature-linked falsifiers for missing module-to-ideal bridges.

No cryptographic attack or hardness theorem. Known principal ideals do not
erase module geometry, and homogeneous SVP does not identify an affine key.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from sympy import Matrix, eye, zeros
from sympy.matrices.normalforms import hermite_normal_form

from structured_edcp_upstream_mixing import negacyclic_mul
from native_rlwe_primal_babai import negacyclic

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/module_ideal_metric_audit.json"
DERIVATION = ROOT / "research/MODULE_IDEAL_METRIC_AUDIT.md"
SOURCES = ROOT / "research/literature_audits/module_ideal_metric_sources.json"


def _integer(v, name, minimum=1):
    if type(v) is not int or v < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def multiply(a, b):
    if len(a) != len(b) or not a or len(a) & (len(a)-1):
        raise ValueError("equal nonempty power-two negacyclic vectors required")
    if any(type(x) is not int for x in (*a, *b)):
        raise ValueError("exact integer coefficients required")
    return tuple(negacyclic_mul(a, b))


def ring_power(a, exponent):
    _integer(exponent, "nonnegative exponent", 0)
    if not a or len(a) & (len(a)-1) or any(type(v) is not int for v in a):
        raise ValueError("exact power-two negacyclic coefficient vector required")
    result = (1,)+(0,)*(len(a)-1)
    while exponent:
        if exponent & 1:
            result = multiply(result, a)
        a = multiply(a, a)
        exponent >>= 1
    return result


def field_base_control():
    sqrt2, unit, inverse = (0, 1, 0, -1), (1, 1, 0, -1), (-1, 1, 0, -1)
    one = (1, 0, 0, 0)
    if multiply(sqrt2, sqrt2) != (2, 0, 0, 0) or multiply(unit, inverse) != one:
        raise ArithmeticError("zeta8 square/unit identity fails")
    norm = lambda a: int(Matrix(negacyclic(a)).det())
    rows = []
    for exponent in (0, 1, 2, 8, 64):
        value = ring_power(unit, exponent)
        back = ring_power(inverse, exponent)
        A = Matrix(negacyclic(value))
        H = hermite_normal_form(A)
        if multiply(value, back) != one or A.det() != 1 or H != eye(4):
            raise ArithmeticError("distinct unit powers do not generate the same unit ideal")
        rows.append({"exponent": exponent, "coefficients": list(map(str, value)),
                     "inverse_coefficients": list(map(str, back)), "field_norm": "1",
                     "principal_ideal_integer_HNF": [[int(a) for a in H.row(i)] for i in range(4)],
                     "ideal_norm": "1"})
    return {"ring": "Z[x]/(x^4+1)=Z[zeta8]", "sqrt2_coefficients": list(sqrt2),
            "sqrt2_square": [2, 0, 0, 0], "sqrt2_field_norm": str(norm(sqrt2)),
            "sqrt2_is_not_a_unit": True, "unit_coefficients": list(unit),
            "unit_inverse_coefficients": list(inverse), "unit_power_controls": rows,
            "nonunit_principal_ideal_controls": [
                {"rational_generator": a, "ideal_norm": str(a**4),
                 "cannot_be_generated_by_a_unit_power": True} for a in (2, 3)],
            "exponent_is_not_determined_by_ideal_or_ideal_norm": True,
            "claimed_zeta8_base_case_as_stated_falsified": True,
            "general_PIP_algorithms_or_repair_of_the_paper_excluded": False}


def module_metric_control(K, degree, *, explicit_matrices=False):
    _integer(K, "positive shear"); _integer(degree, "ring degree", 2)
    if degree & (degree-1):
        raise ValueError("power-two cyclotomic coefficient degree required")
    if type(explicit_matrices) is not bool:
        raise ValueError("explicit matrix control must be Boolean")
    if explicit_matrices and degree > 16:
        raise ValueError("explicit matrix controls are capped, not partial certificates")
    N = K*K+1
    result = {"ring": f"Z[x]/(x^{degree}+1)", "ring_degree": degree,
              "ring_module_rank": 2, "shear": str(K), "scalar_modulus": str(N),
              "hard_shape_ring_basis": [[str(N), str(K)], ["0", "1"]],
              "easy_shape_ring_basis": [[str(N), "0"], ["0", "1"]],
              "same_successive_diagonal_ideals": [str(N), "1"],
              "same_determinant_ideal": str(N),
              "same_integer_Smith_invariants": ["1"]*degree+[str(N)]*degree,
              "unimodular_ring_basis_change": [["0", "1"], ["1", str(-K)]],
              "orthogonal_ring_basis": [[str(K), "1"], ["1", str(-K)]],
              "coefficient_Gram_of_orthogonal_basis": f"{N}*I_{2*degree}",
              "integer_lattice_determinant_absolute_hex": format(N**degree, "x"),
              "hard_shape_shortest_coefficient_norm_squared_exact": str(N),
              "easy_shape_shortest_coefficient_norm_squared_exact": "1",
              "shortest_length_ratio_squared_exact": str(N),
              "canonical_all_embeddings_norm_squared_multiplier": degree,
              "explicit_metric_lifting_counterexample_not_random_MLWE_source": True,
              "both_families_have_polynomial_time_classical_short_bases": True,
              "general_module_SVP_hardness_proved": False}
    if explicit_matrices:
        I, O = eye(degree), zeros(degree)
        B = (N*I).row_join(K*I).col_join(O.row_join(I))
        U = O.row_join(I).col_join(I.row_join(-K*I))
        C = (K*I).row_join(I).col_join(I.row_join(-K*I))
        if B*U != C or C.T*C != N*eye(2*degree) or abs(int(U.det())) != 1:
            raise ArithmeticError("full module lattice basis/metric identity fails")
        if hermite_normal_form(C) != B:
            raise ArithmeticError("orthogonal and original bases have different integer lattices")
        serialize = lambda A: [[str(a) for a in A.row(i)] for i in range(A.rows)]
        result["exact_coefficient_basis_matrices"] = {"original": serialize(B),
            "unimodular_change": serialize(U), "orthogonal": serialize(C)}
    return result


def homogeneous_affine_control(q):
    _integer(q, "odd modulus", 5)
    if not q % 2:
        raise ValueError("odd modulus required")
    public_A, public_target = 1, 2
    kernel_vector, secret = (1, -1), (1, 1)
    syndrome = lambda v: (public_A*v[0]+v[1]) % q
    # No integer vector of squared norm1 belongs to this kernel. The supplied
    # vector has squared norm2, so it is an EXACT SVP output for all q>=5.
    if any(syndrome(v) == 0 for v in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        raise ArithmeticError("shortest norm control fails")
    bounded_secrets = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)
                       if syndrome((x, y)) == public_target]
    if syndrome(kernel_vector) != 0 or bounded_secrets != [secret]:
        raise ArithmeticError("homogeneous/affine syndrome counterexample fails")
    return {"modulus": str(q), "public_A": public_A, "public_target": public_target,
            "kernel_basis": [[str(q), "-1"], ["0", "1"]],
            "exact_SVP_output": list(kernel_vector), "kernel_shortest_squared_norm": "2",
            "SVP_approximation_factor": "1", "factor_less_than_q_over_two": True,
            "short_secret_in_affine_coset": list(secret),
            "unique_secret_under_coordinate_bound_one": True,
            "SVP_output_syndrome": 0, "secret_syndrome": public_target,
            "direct_SVP_vector_identification_is_not_secret_recovery": True,
            "a_separate_BDD_or_embedding_reduction_is_required": True,
            "random_MLWE_failure_probability_or_cryptographic_hardness_proved": False}


def native_public_kernel_control(A, q, *, explicit_matrix=False):
    """Rank-two public graph kernel; determinant ideal is independent of A."""
    _integer(q, "public modulus", 2)
    degree = len(A)
    if degree < 2 or degree & (degree-1) or any(type(v) is not int or not 0 <= v < q for v in A):
        raise ValueError("canonical public coefficients and power-two degree>=2 required")
    if type(explicit_matrix) is not bool or explicit_matrix and degree > 16:
        raise ValueError("Boolean whole-matrix control at degree<=16 required")
    c = {"ring_degree": degree, "modulus": str(q), "canonical_public_A": list(map(str, A)),
         "kernel_relation": "g=A*f modq", "ring_module_rank": 2,
         "public_ring_basis": [[str(q), "A"], ["0", "1"]],
         "determinant_ideal_scalar_generator": str(q),
         "determinant_ideal_shortest_coefficient_generator_squared_norm": str(q*q),
         "shortest_determinant_generator_projected_log_embedding_is_exactly_zero": True,
         "public_integer_lattice_determinant_absolute_hex": format(q**degree, "x"),
         "determinant_ideal_contains_no_public_A_information": True,
         "iid_small_entry_module_matrix_is_not_this_public_kernel_source": True,
         "arbitrary_module_decoder_or_lattice_attack_refuted": False}
    if explicit_matrix:
        I, O, M = eye(degree), zeros(degree), Matrix(negacyclic(A))
        B = (q*I).row_join(M).col_join(O.row_join(I))
        H = I.row_join(-M)
        if H*B % q != zeros(degree, 2*degree) or B.det() != q**degree:
            raise ArithmeticError("public module kernel basis identity fails")
        c["exact_coefficient_basis"] = [[str(v) for v in B.row(i)] for i in range(2*degree)]
    return c


def rectangular_public_kernel_control(A, q):
    """Complete capped k-by-ell public module basis, without a secret basis."""
    _integer(q, "public modulus", 2)
    k, ell = len(A), len(A[0]) if A else 0
    if not k or not ell or any(len(row) != ell for row in A):
        raise ValueError("nonempty rectangular public ring matrix required")
    d = len(A[0][0])
    if d < 2 or d & (d-1) or d*(k+ell) > 64:
        raise ValueError("complete power-two coefficient basis size<=64 required")
    if any(len(v) != d or any(type(x) is not int or not 0 <= x < q for x in v)
           for row in A for v in row):
        raise ValueError("canonical complete public ring coefficients required")
    M = Matrix.vstack(*(Matrix.hstack(*(Matrix(negacyclic(v)) for v in row)) for row in A))
    B = (q*eye(k*d)).row_join(-M).col_join(zeros(ell*d, k*d).row_join(eye(ell*d)))
    H = eye(k*d).row_join(M)
    if H*B % q != zeros(k*d, (k+ell)*d) or B.det() != q**(k*d):
        raise ArithmeticError("complete rectangular public kernel basis fails")
    return {"modulus": str(q), "ring_degree": d, "public_rows": k, "public_columns": ell,
            "canonical_public_A": [[[str(x) for x in v] for v in row] for row in A],
            "known_determinant_ideal_scalar_generator": str(q**k),
            "coefficient_lattice_determinant_absolute_hex": format(q**(k*d), "x"),
            "exact_coefficient_basis": [[str(v) for v in B.row(i)] for i in range(B.rows)],
            "complete_homogeneous_syndrome_basis_verified": True,
            "shortest_determinant_generator_projected_log_embedding_is_exactly_zero": True,
            "secret_short_basis_not_supplied": True}


def run_controls():
    return {"status": "EXACT_LITERATURE_BRIDGE_FALSIFIERS_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "literature_source_record_sha256": hashlib.sha256(SOURCES.read_bytes()).hexdigest(),
            "literature_ids": ["LIT-LUO-MODULE-LATTICE-IV-2605.17412"],
            "zeta8_base_case_control": field_base_control(),
            "module_metric_controls": [module_metric_control(K, d, explicit_matrices=d <= 8)
                for K, d in ((2, 2), (4, 4), (16, 8), (2**32, 64), (2**128, 256))],
            "homogeneous_affine_controls": [homogeneous_affine_control(q) for q in (5, 17, 3329)],
            "native_public_kernel_source_theorem": {
                "scope": "Every public A over a power-two cyclotomic ring: kernel {(x,y):A*x+y=0 modq}, A with k rows and ell columns",
                "public_module_rank": "k+ell", "known_determinant_ideal": "(q^k)",
                "known_shortest_determinant_generators": "q^k times signed ring monomials",
                "shortest_determinant_generator_projected_log_embedding_is_exactly_zero": True,
                "valid_for_every_public_matrix_not_a_sampling_fit": True,
                "same_fact_for_any_unimodular_basis_change_of_this_kernel": True,
                "different_source_specific_target_ideals_or_decoding_reductions_not_excluded": True},
            "native_public_kernel_controls": [native_public_kernel_control(A, q, explicit_matrix=True)
                for A, q in (((0, 0), 5), ((1, 2), 5), ((3, 1, 4, 1), 17),
                              ((0, 1, 2, 3, 4, 5, 6, 7), 3329))],
            "rectangular_public_kernel_controls": [
                rectangular_public_kernel_control([[(1, 2)], [(3, 4)]], 5),
                rectangular_public_kernel_control([[(1, 2), (2, 3), (3, 4)],
                                                    [(4, 0), (0, 1), (1, 2)]], 5)],
            "scopes": {
                "stated_zeta8_base_case_algebra_falsified": True,
                "diagonal_ideal_data_is_not_a_uniform_metric_certificate": True,
                "homogeneous_short_vector_is_not_an_affine_secret_without_a_reduction": True,
                "all_PIP_or_module_SVP_algorithms_refuted": False,
                "random_MLWE_average_case_claim_refuted_by_engineered_metric_examples": False,
                "real_cryptographic_break_or_security_guarantee_established": False},
            "speedup_claim_allowed": False, "candidate_record_accepted": False,
            "novelty_claim": False, "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true")
    args = p.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
        print(json.dumps({"status": report["status"], "metric_controls": len(report["module_metric_controls"]),
                          "base_case_falsified": True, "cryptographic_attack_claimed": False}))
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

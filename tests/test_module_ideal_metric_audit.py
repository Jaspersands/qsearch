from copy import deepcopy
import hashlib
import json
import subprocess

import pytest
from sympy import Matrix, ZZ, eye
from sympy.matrices.normalforms import smith_normal_form

from module_ideal_metric_audit import (
    DERIVATION, REPORT, SOURCES, field_base_control, homogeneous_affine_control,
    module_metric_control, multiply, ring_power, native_public_kernel_control,
    rectangular_public_kernel_control,
)
from native_rlwe_primal_babai import negacyclic


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


def test_sqrt_two_is_not_a_unit_and_one_plus_sqrt_two_is():
    a, u, inverse = (0, 1, 0, -1), (1, 1, 0, -1), (-1, 1, 0, -1)
    assert multiply(a, a) == (2, 0, 0, 0)
    assert Matrix(negacyclic(a)).det() == 4
    assert multiply(u, inverse) == (1, 0, 0, 0)
    assert Matrix(negacyclic(u)).det() == 1


@pytest.mark.parametrize("e", [0, 1, 2, 8, 64, 256])
def test_unit_power_has_norm_one_and_integral_inverse_not_ideal_norm_two_to_e(e):
    v = ring_power((1, 1, 0, -1), e)
    inverse = ring_power((-1, 1, 0, -1), e)
    assert multiply(v, inverse) == (1, 0, 0, 0)
    assert Matrix(negacyclic(v))*Matrix(negacyclic(inverse)) == eye(4)
    assert Matrix(negacyclic(v)).det() == 1


def test_actual_field_base_artifact_has_nonunit_ideals_and_distinct_same_ideal_powers(artifact):
    c = field_base_control()
    assert c == artifact["zeta8_base_case_control"]
    assert len({tuple(a["coefficients"]) for a in c["unit_power_controls"]}) == 5
    assert {a["ideal_norm"] for a in c["unit_power_controls"]} == {"1"}
    assert c["nonunit_principal_ideal_controls"][0]["ideal_norm"] == "16"
    assert c["nonunit_principal_ideal_controls"][1]["ideal_norm"] == "81"
    assert not c["general_PIP_algorithms_or_repair_of_the_paper_excluded"]


@pytest.mark.parametrize("K", [1, 2, 4, 16, 65536])
@pytest.mark.parametrize("degree", [2, 4, 8])
def test_exact_module_metric_family_has_same_smith_but_distinct_shortest_lengths(K, degree):
    c = module_metric_control(K, degree, explicit_matrices=True)
    matrices = c["exact_coefficient_basis_matrices"]
    B, U, C = (Matrix([[int(x) for x in row] for row in matrices[k]])
               for k in ("original", "unimodular_change", "orthogonal"))
    N = K*K+1
    assert B*U == C and abs(U.det()) == 1
    assert C.T*C == N*eye(2*degree)
    S = smith_normal_form(B, domain=ZZ)
    assert [abs(int(S[i, i])) for i in range(2*degree)] == [1]*degree+[N]*degree
    assert c["shortest_length_ratio_squared_exact"] == str(N)
    assert c["same_successive_diagonal_ideals"] == [str(N), "1"]
    assert not c["general_module_SVP_hardness_proved"]


def test_large_exact_family_uses_bit_length_accounting_not_decimal_limit_hacks(artifact):
    r = module_metric_control(2**128, 256)
    assert r == artifact["module_metric_controls"][-1]
    assert int(r["integer_lattice_determinant_absolute_hex"], 16) == (2**256+1)**256
    assert "exact_coefficient_basis_matrices" not in r
    assert r["both_families_have_polynomial_time_classical_short_bases"]


@pytest.mark.parametrize("q", [5, 9, 17, 101, 3329])
def test_exact_homogeneous_short_vector_does_not_satisfy_unique_affine_secret(q):
    r = homogeneous_affine_control(q)
    assert sum(r["exact_SVP_output"]) % q == 0
    assert sum(r["short_secret_in_affine_coset"]) % q == 2
    assert r["SVP_approximation_factor"] == "1"
    assert r["unique_secret_under_coordinate_bound_one"]
    assert r["a_separate_BDD_or_embedding_reduction_is_required"]
    assert not r["random_MLWE_failure_probability_or_cryptographic_hardness_proved"]


@pytest.mark.parametrize("K,degree", [(True, 4), (0, 4), (-1, 4), (2, 3), (2, True), (2, 1)])
def test_module_family_rejects_noninteger_or_noncyclotomic_inputs(K, degree):
    with pytest.raises(ValueError):
        module_metric_control(K, degree)


def test_bounded_explicit_matrix_request_rejects_instead_of_truncating():
    with pytest.raises(ValueError):
        module_metric_control(2, 32, explicit_matrices=True)


@pytest.mark.parametrize("a", [(), (1, 0, 0), (True, 0), (1.0, 0)])
def test_zero_power_does_not_skip_ring_schema_validation(a):
    with pytest.raises(ValueError):
        ring_power(a, 0)


def test_explicit_matrix_flag_is_not_a_truthy_string():
    with pytest.raises(ValueError):
        module_metric_control(2, 4, explicit_matrices="yes")


@pytest.mark.parametrize("q", [True, 3, 4, 6, 5.0])
def test_affine_counterexample_rejects_inputs_outside_proved_scope(q):
    with pytest.raises(ValueError):
        homogeneous_affine_control(q)


def test_pinned_literature_claims_are_not_a_security_or_attack_recommendation(artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert artifact["literature_source_record_sha256"] == hashlib.sha256(SOURCES.read_bytes()).hexdigest()
    source = json.loads(SOURCES.read_text())
    assert source["primary_url"] == "https://arxiv.org/html/2605.17412v1"
    assert source["paper_is_not_treated_as_an_established_cryptographic_break"]
    assert artifact["scopes"]["stated_zeta8_base_case_algebra_falsified"]
    assert not artifact["scopes"]["random_MLWE_average_case_claim_refuted_by_engineered_metric_examples"]
    assert not artifact["candidate_record_accepted"]


@pytest.mark.parametrize("a,b", [(a, b) for a in range(5) for b in range(5)])
def test_entire_small_uniform_public_source_has_the_same_scalar_determinant(a,b):
    r = native_public_kernel_control((a, b), 5, explicit_matrix=True)
    B = Matrix([[int(v) for v in row] for row in r["exact_coefficient_basis"]])
    assert B.det() == 25
    assert r["determinant_ideal_scalar_generator"] == "5"
    assert r["determinant_ideal_shortest_coefficient_generator_squared_norm"] == "25"
    assert r["shortest_determinant_generator_projected_log_embedding_is_exactly_zero"]


def test_public_source_theorem_does_not_require_an_unknown_small_secret_basis(artifact):
    r = artifact["native_public_kernel_source_theorem"]
    assert r["known_determinant_ideal"] == "(q^k)"
    assert r["valid_for_every_public_matrix_not_a_sampling_fit"]
    assert r["different_source_specific_target_ideals_or_decoding_reductions_not_excluded"]
    A = [[(1, 2), (2, 3), (3, 4)], [(4, 0), (0, 1), (1, 2)]]
    c = rectangular_public_kernel_control(A, 5)
    B = Matrix([[int(v) for v in row] for row in c["exact_coefficient_basis"]])
    assert B.det() == 5**4
    assert c["known_determinant_ideal_scalar_generator"] == "25"
    assert c["secret_short_basis_not_supplied"]


CHECKER = "research/certificates/module_ideal_metric_audit_crosscheck.js"


def test_independent_integer_field_metric_and_affine_checker():
    r = subprocess.run(["node", CHECKER], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["status"] == "PASS"


@pytest.mark.parametrize("case", ["unit", "norm", "matrix", "lambda", "Smith", "secret", "scope", "source", "public_source", "rectangular"])
def test_independent_checker_rejects_tampered_claims(artifact, tmp_path, case):
    r = deepcopy(artifact)
    if case == "unit":
        r["zeta8_base_case_control"]["unit_inverse_coefficients"][0] += 1
    elif case == "norm":
        r["zeta8_base_case_control"]["unit_power_controls"][1]["ideal_norm"] = "2"
    elif case == "matrix":
        r["module_metric_controls"][0]["exact_coefficient_basis_matrices"]["unimodular_change"][0][0] = "1"
    elif case == "lambda":
        r["module_metric_controls"][-1]["shortest_length_ratio_squared_exact"] = "1"
    elif case == "Smith":
        r["module_metric_controls"][0]["same_integer_Smith_invariants"][0] = "2"
    elif case == "secret":
        r["homogeneous_affine_controls"][0]["short_secret_in_affine_coset"] = [1, -1]
    elif case == "scope":
        r["scopes"]["random_MLWE_average_case_claim_refuted_by_engineered_metric_examples"] = True
    elif case == "public_source":
        r["native_public_kernel_controls"][0]["determinant_ideal_scalar_generator"] = "7"
    elif case == "rectangular":
        r["rectangular_public_kernel_controls"][0]["exact_coefficient_basis"][0][2] = "1"
    else:
        r["literature_source_record_sha256"] = "wrong"
    p = tmp_path/"bad.json"
    p.write_text(json.dumps(r))
    result = subprocess.run(["node", CHECKER, str(p)], capture_output=True, text=True)
    assert result.returncode != 0

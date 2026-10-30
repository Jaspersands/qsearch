"""Physical and exact controls for the corrected, non-exhaustive coset scope."""

from fractions import Fraction
from itertools import permutations
import json
import math

import numpy as np
import pytest

from theorems import coset_multiplicity_carrier_trilemma as audit


@pytest.mark.parametrize("n", [3, 4, 5, 6])
def test_nonorthonormal_coordinates_are_not_physical_unitaries(n):
    perm = list(range(n))
    perm[0], perm[-1] = perm[-1], perm[0]
    v = audit.standard_rep_matrix(tuple(perm), n)
    gram = np.eye(n-1)+np.ones((n-1, n-1))
    assert np.array_equal(v@v, np.eye(n-1))
    assert np.array_equal(v.T@gram@v, gram)
    assert not np.array_equal(v.T@v, np.eye(n-1))
    physical = audit.orthonormal_standard_matrix(tuple(perm), n)
    assert np.allclose(physical.T@physical, np.eye(n-1))
    assert np.allclose(physical, physical.T)
    old_state = np.kron(physical, np.eye(n-1))
    assert np.linalg.eigvalsh(old_state).min() < -0.99
    assert np.trace(old_state) == pytest.approx((n-1)*(n-3))


@pytest.mark.parametrize("n", [3, 4, 5, 6, 7, 8])
def test_physical_born_probabilities_and_true_mutual_information(n):
    record = audit.verify_commutant_zero_information(n)
    assert record["physical_states_and_probabilities_verified"]
    assert record["zero_information_verified"]
    assert record["probability_variation"] < 1e-12
    probabilities = np.asarray(record["conditional_born_probabilities"])
    assert np.allclose(probabilities.sum(axis=1), 1)
    expected = 1/((n-1)*(n-2))
    assert np.allclose(probabilities[:, 0], expected)
    assert record["mutual_information_bits_numeric"] < 1e-12
    assert Fraction(record["single_copy_irrep_probability_exact"]) == Fraction(
        2*(n-1)*(n-2), math.factorial(n))


@pytest.mark.parametrize("n", [3, 4, 5, 6])
def test_commutator_identity_with_both_ordered_products(n):
    d = n-1
    k = np.zeros((d*d, d*d), dtype=np.int64)
    for i in range(n):
        for j in range(i+1, n):
            perm = list(range(n))
            perm[i], perm[j] = perm[j], perm[i]
            v = audit.standard_rep_matrix(tuple(perm), n)
            k += np.kron(v, v)
    forward = sum(int(k[0, m]*k[m*d, 1]) for m in range(d))
    reverse = sum(int(k[0, m*d+1]*k[m*d, 0]) for m in range(d))
    assert forward == math.comb(n-1, 2)+2
    assert reverse == math.comb(n-2, 2)  # The old written proof incorrectly said zero.
    assert forward-reverse == n
    record = audit.verify_three_copy_commutator(n)
    assert record["observed_witness_entry"] == n
    assert not record["general_circuit_lower_bound"]


@pytest.mark.parametrize("n", range(2, 7))
@pytest.mark.parametrize("k", [0, 1, 2, 3, 5])
def test_rencontres_count_matches_independent_factorial_enumeration(n, k):
    numerator = sum((sum(i == x for i, x in enumerate(p))-1)**(2*k)
                    for p in permutations(range(n)))
    assert numerator % math.factorial(n) == 0
    assert audit.compute_commutant_dimension(n, k) == numerator//math.factorial(n)


def test_exact_dimension_not_stirling_estimate_and_not_circuit_bound():
    profiles = audit.build_scaling_profiles((3, 4, 5, 6, 16, 32))
    for row in profiles:
        n = row["n"]
        lower = Fraction(row["identity_term_dimension_lower_bound_exact"])
        assert lower == Fraction((n-1)**(2*n), math.factorial(n))
        assert lower <= row["commutant_dimension_k_n"]
        assert row["dimension_lower_bound_verified"]
        assert not row["general_circuit_lower_bound_proved"]
        assert "racah_complexity_exponential" not in row
        assert row["dimension_lower_bound_log2_numeric"] == pytest.approx(float(math.log2(lower)))
    row = next(row for row in profiles if row["n"] == 16)
    assert row["dimension_lower_bound_log2_numeric"] == pytest.approx(80.77035858958996)
    assert row["commutator_evidence"] == "ANALYTICAL_IDENTITY"


@pytest.mark.parametrize("n", [3, 4])
def test_noncommuting_pair_sums_have_normalized_constructive_select_access(n):
    record = audit.pair_class_sum_access_control(n)
    assert record["unitarity_max_residual"] < 1e-12
    assert record["prepared_block_max_residual"] < 1e-12
    assert record["standard_subspace_commutator_max"] > 0.01
    assert record["unnormalized_class_sum_block_encoding_normalization"] == math.comb(n, 2)
    assert record["normalized_class_sum_block_encoding_normalization"] == 1
    assert record["verifier_uses_dense_tables"]
    assert not record["analytic_access_plan_uses_dense_tables"]
    assert not record["uniform_gate_compiler_implemented"]
    assert not record["arbitrary_Racah_transform_compiled"]
    assert not record["hard_coset_decoder_compiled"]


@pytest.mark.parametrize("call", [
    lambda: audit.verify_three_copy_commutator(True),
    lambda: audit.verify_three_copy_commutator(13),
    lambda: audit.verify_commutant_zero_information(9),
    lambda: audit.compute_commutant_dimension(257, 1),
    lambda: audit.compute_commutant_dimension(3, -1),
    lambda: audit.pair_class_sum_access_control(5),
    lambda: audit.pair_class_sum_access_control(3, 4),
    lambda: audit.standard_rep_matrix((0, 0, 2), 3),
])
def test_allocation_and_input_gates(call):
    with pytest.raises(ValueError):
        call()


def test_report_retracts_general_claims_without_promoting_countercontrols():
    report = audit.build_report()
    assert report["status"] == "PASS"
    assert report["negative_result_status"] == "QUARANTINED_OVERBROAD_NO_GO"
    metrics = report["headline_metrics"]
    for field in ("general_circuit_lower_bound_proved", "exhaustive_trilemma_proved",
                  "speedup_claim_allowed", "accepted_speedup_candidate"):
        assert not metrics[field]
    assert "pillars" not in report
    assert metrics["all_commutant_zero_information_verified"]
    assert metrics["all_commutator_witnesses_verified"]


def test_report_writer_uses_quarantine_instead_of_reactivating_negative(tmp_path, monkeypatch):
    from theorems import nonabelian_barrier_scope_audit as scope
    calls = []
    monkeypatch.setattr(scope, "quarantine_reviewed_negatives", lambda: calls.append("quarantine"))
    monkeypatch.setattr(audit, "REPORT", tmp_path/"report.json")
    audit.write_report()
    audit.write_report(write_registry=False)
    assert calls == ["quarantine"]
    report = json.loads(audit.REPORT.read_text())
    assert report["negative_result_status"] == "QUARANTINED_OVERBROAD_NO_GO"
    assert not hasattr(audit, "register_negative_result")


def test_failed_access_control_cannot_produce_pass_report(monkeypatch):
    broken = audit.pair_class_sum_access_control()
    broken["prepared_block_max_residual"] = 1
    monkeypatch.setattr(audit, "pair_class_sum_access_control", lambda: broken)
    report = audit.build_report()
    assert report["status"] == "FAIL"
    assert not report["headline_metrics"]["bounded_pair_access_verified"]


def test_signed_young_action_and_exact_noncommuting_simulation_reference():
    from sympy import Matrix, eye, kronecker_product, sqrt

    z = Matrix([[1, 0], [0, -1]])
    s2 = Matrix([[-1, sqrt(3)], [sqrt(3), 1]])/2
    assert z*z == s2*s2 == eye(2)
    assert z*s2*z == s2*z*s2
    wrong_orientation = Matrix([[1, sqrt(3)], [sqrt(3), -1]])/2
    assert z*wrong_orientation*z != wrong_orientation*z*wrong_orientation
    transpositions = [z, s2, z*s2*z]
    a = sum((kronecker_product(t, t) for t in transpositions), Matrix.zeros(4))/3
    x = Matrix([[0, 1], [1, 0]])
    assert a == (kronecker_product(x, x)+kronecker_product(z, z))/2
    assert a**3 == a  # exp(-itA)=I-i sin(t)A+(cos(t)-1)A^2.
    left, right = kronecker_product(a, eye(2)), kronecker_product(eye(2), a)
    commutator = left*right-right*left
    assert (commutator.T*commutator).trace() == 4

from itertools import product
import json
import math

from flint import fmpq, fmpz
import numpy as np
import pytest

from hsp_campaign_claim_audit import (
    IDS, ROOT, build_report, counted_jacobi, cubic, dyadic_dcp_control,
    heisenberg_weak_direction_control, jacobi_control, legendre_information_control,
    mm_control, mm_dual, mm_value, nilpotent_parameter_control,
    nonprimitive_shift_control, recover_explicit_mm_shift, unitriangular_bypass_control,
)


@pytest.mark.parametrize("r", (1, 8, 64, 256))
def test_growing_binary_extension_field_is_covered_not_growing_nilpotency_class(r):
    c = nilpotent_parameter_control(r)
    assert c["group_order"] == c["field_order"]**6 == 2**(6*r)
    assert c["group_encoding_bits"] == 6*r and c["nilpotency_class"] == 3
    assert c["only_prime_factor_of_group_order"] == 2
    assert c["published_constant_class_bounded_prime_factor_theorem_applies"]
    assert not c["all_growing_nilpotency_classes_solved"]
    assert not c["new_algorithm_or_physical_receiver_implemented"]


def test_class3_center_bypass_is_not_an_impossibility_theorem():
    c = unitriangular_bypass_control()
    I = np.eye(4, dtype=int)
    a, second, third = (np.array(c[k]) for k in ("hidden_cyclic_generator", "second_commutator", "third_commutator"))
    assert np.array_equal((a@a) % 2, I)
    assert a[0, 1] == second[0, 2] == third[0, 3] == 1
    assert not np.array_equal(second, I) and not np.array_equal(third, I)
    assert not c["nonidentity_center_intersection"]
    assert c["constant_class_bounded_prime_factor_algorithm_still_applies"]
    assert not c["explicit_generator_is_given_to_the_hidden_subgroup_algorithm"]


@pytest.mark.parametrize("a,b", tuple(product(range(8), repeat=2)))
def test_exact_cubic_mm_shift_recovery_with_only_chosen_classical_queries(a, b):
    result = recover_explicit_mm_shift(3, lambda x, y: mm_value(x^a, y^b))
    assert (result["recovered_x_shift"], result["recovered_y_shift"]) == (a, b)
    assert result["shifted_function_queries"] == 7
    assert not result["legal_under_random_sample_only_access"]


def test_cubic_bent_dual_and_nonlinear_derivative_are_complete_integer_identities():
    r = mm_control(3, 7, 3, enumerate_walsh=True)
    for u, v in product(range(8), repeat=2):
        value = sum((-1)**(mm_value(x, y)^((x&u).bit_count() % 2)^((y&v).bit_count() % 2)) for x, y in product(range(8), repeat=2))
        assert value == 8*(-1)**mm_dual(u, v)
    assert r["derivative_values"] == [0, 0, 0, 1]
    assert r["four_point_affine_test_XOR"] == 1
    assert not r["higher_degree_forces_exponential_dual_circuit"]
    assert not r["accepted_speedup_candidate"]


@pytest.mark.parametrize("m", (64, 512))
def test_explicit_high_degree_family_is_classically_recovered_without_a_table(m):
    a, b = (1 << (m-1))+3, (1 << (m-2))+1
    r = mm_control(m, a, b)
    assert r["recovered_x_shift"] == a and r["recovered_y_shift"] == b
    assert r["shifted_function_queries"] == 2*m+1
    assert "complete_Walsh_entries" not in r
    assert r["known_dual_CZ_terms"] == m and r["known_dual_CCZ_terms"] == 1


def test_dyadic_phase_bank_is_an_inverse_qft_control_not_a_free_random_source():
    m, N = 4, 16
    c = dyadic_dcp_control(m)
    assert {sum(k*b for k, b in zip(c["labels"], bits)) for bits in product(range(2), repeat=m)} == set(range(N))
    for s in range(N):
        state = np.array([np.exp(2j*np.pi*s*sum(c["labels"][j]*((x >> j)&1) for j in range(m))/N)/math.sqrt(N) for x in range(N)])
        output = np.fft.fft(state)/math.sqrt(N)
        assert abs(output[s])**2 > 1-1e-12
    assert c["ordered_IID_source_event_probability_exponent"] == -16
    assert c["structured_source_was_assumed_supplied"] and not c["generic_random_DCP_decoder_supplied"]


@pytest.mark.parametrize("p", (7, 13, 31, 101))
def test_exact_legendre_agreement_counts_support_information_not_runtime_bounds(p):
    c = legendre_information_control(p)
    chi = [0 if x == 0 else (1 if pow(x, (p-1)//2, p) == 1 else -1) for x in range(p)]
    assert len(c["complete_shift_difference_census"]) == p-1
    for d in range(1, p):
        assert sum(chi[x]*chi[(x+d) % p] for x in range(p)) == -1
        assert sum(chi[x] == chi[(x+d) % p] for x in range(p)) == (p-3)//2
    assert fmpq(c["ambiguity_union_upper"]) <= fmpq(1, 256)
    assert not c["query_identifiability_is_a_runtime_bound"]
    assert not c["efficient_classical_shift_decoder_supplied"]


def test_127_bit_legendre_information_ledger_does_not_materialize_the_domain():
    p = 2**127-1
    c = legendre_information_control(p)
    assert c["random_classical_samples"] == 135
    assert not c["large_domain_was_materialized"]
    assert fmpq(c["ambiguity_union_upper"]) < fmpq(1, 256)
    assert not c["all_quantum_processing_of_classical_samples_excluded"]


def test_public_jacobi_binary_reciprocity_matches_independent_arithmetic():
    for n in range(3, 128, 2):
        for a in range(-20, 20):
            value, steps = counted_jacobi(a, n)
            assert value == int(fmpz(a).jacobi(n))
            assert steps <= 4*n.bit_length()**2
    n = (2**61-1)*(2**127-1)
    r = jacobi_control(1234567, n)
    assert r["modulus_bits"] == 188 and not r["factorization_subroutine_called"]
    assert not r["physical_reversible_gate_compiler_supplied"]
    assert not r["arbitrary_composite_Gauss_cancellation_formula_validated"]


@pytest.mark.parametrize("n,success", ((9, "1/3"), (25, "1/5"), (45, "1/3")))
def test_nonprimitive_oracle_equivalence_blocks_full_shift_identification_even_quantum(n, success):
    r = nonprimitive_shift_control(n)
    values = r["Jacobi_table"]
    for C in r["identical_shift_oracle_classes"]:
        assert all(tuple(values[(x+s) % n] for x in range(n)) == tuple(values[(x+C[0]) % n] for x in range(n)) for s in C)
    assert r["uniform_full_shift_success_upper_even_with_coherent_queries"] == success
    assert not r["identifiability_is_a_computational_hardness_claim"]
    assert not r["accepted_speedup_candidate"]


@pytest.mark.parametrize("p", (7, 31, 2**31-1))
def test_naive_weak_direction_preprocessing_is_not_a_free_heisenberg_parameter(p):
    r = heisenberg_weak_direction_control(p)
    probability = fmpq(p-1, p*p)
    budget = r["half_success_copy_count_union_lower"]
    assert fmpq(r["nontrivial_1D_weak_sample_probability"]) == probability
    assert (budget-1)*probability < fmpq(1, 2) <= budget*probability
    assert not r["known_polynomial_Heisenberg_algorithms_excluded"]


def test_reviewed_hsp_records_are_preserved_and_no_longer_active():
    archive = json.loads((ROOT/"research/registry/quarantined_campaign_negatives.json").read_text())
    active = json.loads((ROOT/"research/registry/negative_results.json").read_text())
    assert len(archive) >= 8
    assert set(IDS).issubset({r["id"] for r in archive})
    assert not set(IDS).intersection(r["id"] for r in active)
    r = build_report()
    assert len(r["quarantined_ids"]) == 5
    assert not r["general_DHSP_polynomial_decoder_supplied"]
    assert not r["general_hidden_shift_speedup_supplied"]
    assert not r["accepted_speedup_candidate"]


@pytest.mark.parametrize("call", (lambda: nilpotent_parameter_control(0), lambda: mm_control(2, 0, 0),
                                 lambda: mm_control(3, 8, 0), lambda: legendre_information_control(9),
                                 lambda: counted_jacobi(3, 10), lambda: dyadic_dcp_control(True),
                                 lambda: nonprimitive_shift_control(105)))
def test_invalid_access_and_algebra_parameters_rejected(call):
    with pytest.raises(ValueError):
        call()

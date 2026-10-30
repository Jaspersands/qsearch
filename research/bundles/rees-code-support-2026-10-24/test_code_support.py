from fractions import Fraction as F

import numpy as np
import pytest

import code_support as c


@pytest.fixture(scope="module")
def report():
    return c.audit()


def test_corrected_growth_preserves_all_histories_and_extracts_a_pure_source(report):
    assert report["growth_probability_max_error"] < 1e-12
    assert report["growth_instrument_operator_error"] < 1e-12
    assert report["corrected_failure_antisymmetry_error"] < 1e-12
    assert report["final_extracted_wedge_trace_distance"] < 1e-12


def test_failure_correction_is_not_optional(report):
    assert report["uncorrected_failure_antisymmetry_leakage"] == pytest.approx(4/9)


def test_reading_the_full_ancilla_index_breaks_the_failure_correction(report):
    assert report["fine_grained_ancilla_measurement_leakage"] > .1


def test_actual_degenerate_code_source_has_the_right_rees_hidden_subgroup(report):
    assert report["flat_code_hidden_order"] == 9
    assert report["actual_rees_addresses_checked"] == 81
    assert report["rees_hidden_overlap_max_error"] < 1e-12


def test_nonnormal_code_stabilizer_is_not_replaced_by_its_normal_core(report):
    assert report["nonnormal_code_hidden_order"] == 3
    assert report["nonnormal_code_normal_core_order"] == 1
    assert F(report["nonnormal_rees_hidden_overlap_error_exact"]) == 0


def test_determinant_and_operator_gap_transfer(report):
    assert report["determinant_identity_max_error"] < 1e-12
    assert report["principal_angle_gap_max_excess"] < 1e-12


def test_support_is_not_general_mixed_conjugation(report):
    assert report["nonflat_support_wedge_overlap_modulus"] == pytest.approx(1)
    assert report["nonflat_support_false_conjugation_distance"] > .17


def test_stopping_early_does_not_certify_rank_or_purity(report):
    assert report["understated_rank_output_purity"] == pytest.approx(1/3)


@pytest.mark.parametrize("rank", [2, 3, 4])
def test_one_shot_exponential_postselection_is_not_the_streaming_cost(rank):
    rho = np.eye(rank)/rank
    projector = c.antisymmetric_projector(rank, rank)
    success = np.trace(projector @ c.tensor_power(rho, rank)).real
    assert success == pytest.approx(rank**(-rank))


def test_correct_mixed_marginals_do_not_supply_independent_growth_inputs():
    rho = np.eye(3)/3
    correlated = np.zeros((9, 9), dtype=complex)
    for j in range(3):
        correlated[3*j+j, 3*j+j] = 1/3
    assert np.allclose(c.trace_last(correlated, 3), rho)
    projector = c.antisymmetric_projector(3, 2)
    assert abs(np.trace(projector @ correlated)) < 1e-12
    assert np.trace(projector @ np.kron(rho, rho)).real == pytest.approx(1/3)


@pytest.mark.parametrize("rank", [2, 3, 7])
def test_constant_operator_gap_does_not_remove_rank_copy_lower_bound(rank):
    dimension = rank+2
    first = np.diag([1]*rank + [0, 0]).astype(complex)
    shared = np.diag([1]*(rank-1) + [0, 0, 0]).astype(complex)
    vector = np.zeros(dimension)
    vector[rank:] = 1/np.sqrt(2)
    second = shared + np.outer(vector, vector)
    action = np.eye(dimension, dtype=complex)
    action[rank, rank] = np.exp(2j*np.pi/3)
    assert np.linalg.norm(first-action @ first @ action.conj().T) < 1e-12
    assert np.linalg.norm(second-action @ second @ action.conj().T, ord=2) == pytest.approx(np.sqrt(3)/2)
    assert c.trace_distance(first/rank, second/rank) == pytest.approx(1/rank)
    for copies in (1, 2, 3, 9):
        exact_distance = 1-(1-F(1, rank))**copies
        assert exact_distance <= F(copies, rank)
    if rank <= 3:
        assert c.trace_distance(c.tensor_power(first/rank, 2), c.tensor_power(second/rank, 2)) == pytest.approx(1-(1-1/rank)**2)


def plan(**changes):
    args = dict(rank=8, receiver_leaves=7, design_size=6, cover_order_bits=31,
                support_operator_gap=F(1, 4), error=F(1, 20))
    return c.source_plan(**(args | changes))


def test_complete_cap_and_error_allocations():
    result = plan()
    sources = result["independent_wedge_sources"]
    attempts = sum(row["attempt_cap"] for row in result["growth_stages"])
    assert result["native_copy_cap"] == sources*(1+attempts)
    assert result["growth_measurement_cap"] == sources*attempts
    assert result["controlled_original_action_calls"] == sources*8
    assert result["growth_measurement_cap"] * F(result["per_growth_instrument_half_diamond_budget"]) == F(1, 160)
    assert result["controlled_original_action_calls"] * F(result["per_original_action_half_diamond_budget"]) == F(1, 160)
    bits = c.ceil_log2(8*sources*7/F(1, 20))
    for row in result["growth_stages"]:
        assert F(row["success_probability"])*row["attempt_cap"] >= bits
    assert sources*7*F(1, 2**bits) <= F(1, 160)
    assert sum(F(result[name]) for name in ("source_amplification_budget", "extraction_abort_budget",
               "growth_implementation_budget", "original_action_implementation_budget",
               "public_addresses_and_receiver_budget")) == F(1, 20)


def test_rank_one_has_no_growth_or_division_by_zero():
    result = plan(rank=1)
    assert result["growth_stages"] == []
    assert result["growth_measurement_cap"] == result["controlled_register_swaps_cap"] == 0
    assert result["per_growth_instrument_half_diamond_budget"] is None
    assert result["native_copy_cap"] == result["independent_wedge_sources"]


@pytest.mark.parametrize("change", [{"rank": 16}, {"support_operator_gap": F(1, 8)}, {"error": F(1, 100)}])
def test_rank_gap_and_accuracy_costs_are_visible(change):
    assert plan(**change)["native_copy_cap"] > plan()["native_copy_cap"]


@pytest.mark.parametrize("change", [{"rank": True}, {"rank": 0}, {"rank": 2.5},
                                  {"support_operator_gap": 0}, {"error": .1}])
def test_bad_contracts_rejected(change):
    with pytest.raises(ValueError):
        plan(**change)


def test_primitive_is_attributed_and_conditional_result_not_promoted(report):
    scope = report["scope"]
    assert scope["antisymmetrization_primitive_is_prior_art"]
    assert scope["conditional_code_support_reduction"]
    for key in ("arbitrary_mixed_conjugation_solver", "quantum_receiver_executed", "independent_review", "novelty_or_speedup_claim"):
        assert not scope[key]
    assert not plan()["promises_certified"]
    assert not plan()["spectral_nondegeneracy_required"]

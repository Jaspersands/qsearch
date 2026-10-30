from fractions import Fraction as F

import pytest

from contrast_source import (broken_symmetry_falsifier, centered_tail_reference,
    classical_colored_support, classical_sample_plan, coarsen_reference,
    contract_plan, empty_control, full_rank_control, high_rank_bias_falsifier,
    noncommuting_control, predecessor, source_plan)


@pytest.mark.parametrize("dimension,rank,gap", [(2**128, 3, F(1, 10)),
    (2**1024, 20, F(1, 100)), (10000, 1, F(1)), (2**50, 7, F(1, 2))])
def test_large_dimension_contract(dimension, rank, gap):
    plan = contract_plan(dimension, rank, gap, F(1, 32))
    assert plan["branch"] == "CENTERED_CONTRAST"
    assert plan["rank_cap"] == 2*rank
    assert plan["unknown_background_upper"] < plan["bin_width"]/2
    assert plan["coarsening_trace_norm_upper"] < gap/16
    assert plan["near_boundary_rank_upper"] == 2*rank
    assert plan["bad_grid_probability_upper"] <= plan["error"]/32
    assert plan["boundary_margin"] < plan["bin_width"]/4
    assert not plan["state_rank_cap_supplied"]


@pytest.mark.parametrize("dimension,rank", [(2, 1), (27, 3), (257, 2)])
def test_small_branch_is_actually_polynomial(dimension, rank):
    plan = contract_plan(dimension, rank, F(1, 4), F(1, 16))
    assert plan["branch"] == "POLYNOMIAL_DIMENSION"
    assert plan["rank_cap"] == dimension <= plan["dimension_switch_threshold"]
    assert plan["dimension_switch_threshold"] < 130*rank/plan["orbit_gap"]


def test_branch_switch_not_hidden_dimension_loop():
    initial = contract_plan(2**256, 3, F(1, 2), F(1, 16))
    boundary = int(initial["dimension_switch_threshold"])
    assert contract_plan(boundary, 3, F(1, 2), F(1, 16))["branch"] == "POLYNOMIAL_DIMENSION"
    assert contract_plan(boundary+1, 3, F(1, 2), F(1, 16))["branch"] == "CENTERED_CONTRAST"


@pytest.mark.parametrize("offset_fraction", [F(0), F(1, 4), F(1, 2), F(3, 4)])
def test_huge_background_exact_compressed_spectrum(offset_fraction):
    control = full_rank_control()
    plan, dimension = control["plan"], control["dimension"]
    b = F(4, 5*dimension)
    ref = coarsen_reference([(b+F(1, 15), 3), (b, dimension-3)], plan,
        int(offset_fraction*plan["grid_choices"]), proof_background=b)
    assert ref["retained_rank"] == 3
    assert ref["near_boundary_rank"] <= plan["rank_cap"]
    assert ref["proof_trace_norm_loss"] <= plan["coarsening_trace_norm_upper"]
    assert ref["contrast_trace"] <= 1
    assert ref["centered_tail"] == 0
    assert control["full_state_rank"] > 2**200


def test_nonzero_trace_tail_is_not_replaced_by_exact_rank_assumption():
    dimension, rank, gap = 2**128, 3, F(1, 10)
    plan = contract_plan(dimension, rank, gap, F(1, 16))
    noise, weight = gap/512, F(4, 5)
    b = weight/dimension
    buckets = [(b+(1-weight-noise)/rank, rank), (b+noise/3, 3), (b, dimension-6)]
    ref = coarsen_reference(buckets, plan, plan["grid_choices"]//3, proof_background=b)
    assert ref["centered_tail"] == noise > 0
    assert ref["retained_rank"] == rank
    assert ref["proof_trace_norm_loss"] <= plan["coarsening_trace_norm_upper"]


def test_tail_handles_negative_spikes_and_multiplicities():
    assert centered_tail_reference([(F(1, 8), 2), (F(3, 8), 2)], F(1, 4), 1) == F(3, 8)
    assert centered_tail_reference([(F(1, 8), 2), (F(3, 8), 2)], F(1, 4), 3) == F(1, 8)


def test_empty_filter_is_whole_group_not_abort():
    result = empty_control()
    assert result["all_bins_empty"]
    assert result["proof_trace_norm_loss"] == 0
    assert result["empty_decision_if_promises_hold"] == "RETURN_WHOLE_PUBLIC_GROUP"


def test_high_rank_bias_is_rejected_despite_real_gap():
    result = high_rank_bias_falsifier()
    assert result["both_eigenvalues_below_cutoff"]
    assert result["optimal_centered_rank_residual"] > result["allowed_residual"]
    dimension, alpha = result["dimension"], result["true_translation_gap"]
    plan = contract_plan(dimension, 3, alpha, F(1, 16))
    with pytest.raises(ValueError, match="compressibility"):
        coarsen_reference([((1+alpha)/dimension, dimension//2),
                           ((1-alpha)/dimension, dimension//2)], plan, 0,
                          proof_background=(1-alpha)/dimension)


def test_no_false_arbitrary_noise_correction():
    result = broken_symmetry_falsifier()
    assert result["formerly_symmetric_generator_is_now_outside_H"]
    assert result["actual_outside_distance"] == F(1, 2**39)
    assert result["new_gap_promise_is_false"]


def test_nondiagonal_nonnormal_control():
    result = noncommuting_control()
    assert result["branch"] == "CENTERED_CONTRAST"
    assert result["noncommuting_approximant_commutator_norm"] > 1e-8
    assert result["approximation_trace_residual"] <= float(result["allowed_trace_residual"])
    assert result["coarsening_trace_error"] <= float(result["coarsening_error_bound"])
    assert result["minimum_outside_distance"] >= float(result["promised_gap"])
    assert result["maximum_outside_wedge_modulus"] < 1-float(result["promised_gap"])**2/8
    assert result["original_packet_and_expected_H_equal"]
    assert result["hidden_subgroup_order"] == result["retained_rank"] == 3
    assert result["hidden_subgroup_is_nonnormal"]


def test_unchanged_whole_run_ledger_on_large_dimension_branch():
    params = dict(orbit_gap=F(1, 10), error=F(1, 32), receiver_leaves=8,
                  design_size=6, cover_order_bits=16)
    new = source_plan(dimension=2**256, contrast_rank=3, **params)
    old = predecessor().source_plan(rank_cap=6, **params)
    for key in ("raw_copy_cap", "qpe_bits", "spectral_attempt_cap", "growth_stage_cap",
                "original_controlled_action_cap", "total_allocated_error_upper"):
        assert new[key] == old[key]
    assert new["raw_copy_cap"] > 10**30
    assert not new["quantum_execution"]
    assert not new["accepted_speedup_candidate"]


def test_classical_cap_grows_with_log_dimension_not_dimension():
    plans = [contract_plan(2**bits, 3, F(1, 10), F(1, 16)) for bits in (128, 256, 512)]
    caps = [classical_sample_plan(plan, F(1, 32))["sample_cap"] for plan in plans]
    assert caps[0] < caps[1] < caps[2] < 4*caps[0]
    assert classical_sample_plan(plans[0], F(1, 32))["basis_must_be_known"]


def test_classical_colored_support_with_exact_counts():
    plan = contract_plan(16, 3, F(1, 10), F(1, 16))
    offset = plan["grid_choices"]//3
    counts = {1: 1, 5: 2, 9: 3}
    colors = classical_colored_support(counts, 6, plan, offset)
    ref = coarsen_reference([(F(1, 6), 1), (F(1, 3), 1), (F(1, 2), 1), (F(0), 13)],
                            plan, offset, proof_background=0)
    assert colors == {label: row["bin"] for label, row in zip(counts, ref["rows"][:3])}
    with pytest.raises(ValueError, match="every sample"):
        classical_colored_support(counts, 7, plan, offset)


@pytest.mark.parametrize("dimension,rank,gap,error", [(0, 1, F(1, 2), F(1, 2)),
    (16, 0, F(1, 2), F(1, 2)), (16, 17, F(1, 2), F(1, 2)),
    (16, 2, 0.1, F(1, 2)), (16, 2, F(1, 2), 0), (True, 1, F(1, 2), F(1, 2))])
def test_invalid_public_contracts_rejected(dimension, rank, gap, error):
    with pytest.raises(ValueError):
        contract_plan(dimension, rank, gap, error)


@pytest.mark.parametrize("offset", [-1, True, F(1, 2), 2**100])
def test_invalid_grid_indices_rejected(offset):
    plan = contract_plan(4, 1, F(1, 2), F(1, 16))
    with pytest.raises(ValueError):
        coarsen_reference([(F(1, 4), 4)], plan, offset, proof_background=0)

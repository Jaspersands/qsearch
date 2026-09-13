"""Retained sources must not be silently marginalized or made free oracles."""

from fractions import Fraction
import math

import pytest

from isotypic_instruments import coarse_source_walsh_information_contract
from coset_binary_carrier_instruments import (
    _coarse_source_character_data, _coherent_walsh_histogram_law,
    audit_coarse_source_contraction, audit_complex_source_mixtures,
    coarse_source_joint_laws, source_count_weight_controls,
)
from involution_character_arithmetic import coherent_source_count_decision
from symmetric_character import integer_partitions


FLAGS = dict(one_uniform_full_mask_query=True, common_central_unitary=True,
    phase_and_common_partition_fixed_before_sources=True,
    walsh_readout_up_to_category_known_bit_flips=True,
    only_categories_and_walsh_bits_retained=True, physical_inputs_discarded=True)


def test_all_source_labels_and_complex_phases_are_covered_but_not_all_copy_counts():
    full = coarse_source_walsh_information_contract(1024, 17528, None, **FLAGS)
    coarse = coarse_source_walsh_information_contract(1024, 17528, 2, **FLAGS)
    assert full["trace_distance_upper_bound_power_of_two"] < -1600
    assert full["all_irrep_labels_retained"]
    assert full["covers_arbitrary_classical_full_source_walsh_decisions"]
    assert full["covers_arbitrary_complex_central_phases"]
    assert full["off_coset_radius_upper_bound"] == coarse["off_coset_radius_upper_bound"]
    assert int(full["category_count_upper_bound"]) == 2**1023
    assert not full["all_copy_counts_obstructed"]
    assert not full["copy_count_is_available_resource_budget"]
    assert not full["covers_multiple_queries_or_final_coherent_povm"]
    assert not full["positive_mixture_is_efficient_classical_sampler"]
    assert not full["novelty_established"]
    assert coarse_source_walsh_information_contract(1024, 8764, None, **FLAGS)["bound_is_vacuous"]
    for flag in FLAGS:
        row = coarse_source_walsh_information_contract(128, 1428, None, **dict(FLAGS, **{flag: False}))
        assert not row["applicable"]
        assert row["trace_distance_upper_bound_power_of_two"] is None
        with pytest.raises(ValueError):
            coarse_source_walsh_information_contract(128, 1428, None, **dict(FLAGS, **{flag: 1}))


@pytest.mark.parametrize("n,k,r", ((6, 2, None), (9, 3, 2), (True, 3, 2), (8, True, 2), (8, 0, 2), (8, 2, True), (8, 2, 0)))
def test_bad_access_contracts_are_not_coerced(n, k, r):
    with pytest.raises(ValueError):
        coarse_source_walsh_information_contract(n, k, r, **FLAGS)


def test_full_transcript_dyadic_bounds_round_outward_without_float_underflow():
    for n, k, r in ((16, 80, 2), (64, 588, None), (128, 1428, 128)):
        row = coarse_source_walsh_information_contract(n, k, r, **FLAGS)
        mixture = Fraction(4*k*k*int(row["category_count_upper_bound"]), math.prod(range(1, n, 2)))
        remainder = math.factorial(n) * Fraction(row["off_coset_radius_upper_bound"])**k
        for squared, field in ((mixture, "mixture_upper_bound_power_of_two"), (remainder**2, "remainder_upper_bound_power_of_two")):
            exponent = row[field]
            assert min(Fraction(1), squared) <= Fraction(2)**(2*exponent)


def test_exact_coarse_laws_match_independent_histograms_and_positive_diagonals():
    audit = audit_coarse_source_contraction()
    assert audit["verified"]
    assert audit["independent_matrix_histogram_laws_checked"] == 36
    assert audit["exact_coset_diagonal_mixtures_checked"] == 40
    assert audit["all_irrep_column_envelopes_checked"] == 750
    assert audit["minimum_class_size_checks"] > 1200
    assert not audit["formal_proof_verification"]


def test_complex_raw_readout_does_not_require_phase_homogeneous_categories():
    audit = audit_complex_source_mixtures()
    assert audit["verified"]
    assert audit["independent_raw_source_histogram_laws_checked"] == 72
    assert audit["coset_diagonal_positive_mixtures_checked"] == 72
    assert audit["phase_need_not_be_constant_in_raw_category"]
    assert not audit["arbitrary_phase_theorem_formally_verified"]


def test_source_retention_gains_are_charged_against_source_only_and_full_pair_baselines():
    control = source_count_weight_controls(6, 3, (2, 4, 8))
    for row in control["copy_sweep"]:
        assert row["complete_paired_category_bit_distance"] >= row["source_count_and_weight_distance"] >= row["weight_only_distance"]
        assert row["source_count_and_weight_distance"] >= row["source_count_only_distance"]
        assert row["gain_over_discarding_source_counts"] > 0
        assert row["full_pair_likelihood_baseline"]["total_variation"] >= row["pair_event_count_baseline"]["total_variation"]
        assert not row["complete_paired_table_beats_full_pair_likelihood"]
        assert not row["ideal_table_is_compiled_classifier"]
        assert not row["speedup_claim_allowed"]
    # This apparent improvement must not be flattened into an all-readout failure.
    assert control["copy_sweep"][1]["complete_paired_table_beats_pair_event_count"]


def test_zero_source_mass_and_nonexact_positive_mixture_are_preserved():
    meta = _coarse_source_character_data(3, 1, "irrep")[0]
    zeros = [j for j, mass in enumerate(meta["alternative_category_masses"]) if Fraction(mass) == 0]
    assert zeros
    full, mixtures, errors = coarse_source_joint_laws(3, 1, 2, "irrep")
    for counts, probability in full[1].items():
        if any(counts[2*j] + counts[2*j+1] for j in zeros):
            assert probability == 0
    assert full[0] != mixtures[0]
    for actual, mixture, error in zip(full, mixtures, errors):
        assert sum(actual.values()) == sum(mixture.values()) == 1
        assert sum(abs(actual[key]-mixture[key]) for key in actual)/2 <= error


def test_executable_source_count_decisions_match_every_actual_s4_histogram():
    histograms, p0, p1, _ = _coherent_walsh_histogram_law(4, 2, 3, "negative_character_reflection")
    partitions = integer_partitions(4)
    expected = source_count_weight_controls(4, 2, (3,))["copy_sweep"][0]["declared_rules"]
    for rule in expected:
        totals = [0.0, 0.0]
        for counts, a, b in zip(histograms, p0, p1):
            labels, bits = [], []
            for j, count in enumerate(counts):
                labels.extend([partitions[j//2]]*count)
                bits.extend([j%2]*count)
            row = coherent_source_count_decision(tuple(labels), tuple(bits), rule["relation"])
            complement = coherent_source_count_decision(tuple(labels), tuple(bits), rule["relation"], complement=True)
            assert row["accept_hidden_class"] != complement["accept_hidden_class"]
            assert not row["uses_fitted_table"]
            if row["accept_hidden_class"]:
                totals[0] += a
                totals[1] += b
        assert totals == pytest.approx([rule["null_acceptance_probability"], rule["alternative_acceptance_probability"]])


@pytest.mark.parametrize("labels,bits,relation,complement", (((), (), "equal", False), (((4,),), (2,), "less", False), (((4,),), (0,), "fitted", False), (((4,),), (0,), "equal", 1)))
def test_terminal_decision_rejects_unphysical_or_fitted_inputs(labels, bits, relation, complement):
    with pytest.raises(ValueError):
        coherent_source_count_decision(labels, bits, relation, complement=complement)

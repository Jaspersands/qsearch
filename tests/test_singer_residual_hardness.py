from fractions import Fraction

import numpy as np
import pytest

from singer_residual_hardness import (
    _coords, _sqrt_upper, classical_control, injectivization_gate,
    positive_hyperplane_reconstruct, public_field, reconstruction_query_law,
    run_controls, singer_parameters, sparse_membership_gate, spectral_control,
    trace_reconstruct,
)


def exact(row):
    return Fraction(int(row["numerator"]), int(row["denominator"]))


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_classical_geometry_leaves_residual_dlog_not_a_new_quantum_algorithm(report):
    assert len(report["classical_geometry_controls"]) == 22
    for r in report["classical_geometry_controls"]:
        assert r["normal_line_verified_by_secret_only_for_calibration"]
        assert not r["source_table_built_by_decoder"]
        assert not r["inverse_or_discrete_log_called_by_decoder"]
        assert r["residual_already_solved_quantumly_by_Shor"]
        assert not r["polynomial_time_classical_full_recovery_claim"]
        assert r["oracle_evaluations"] == len(r["queries"])
        if r["base_prime"] == 2:
            assert r["oracle_evaluations"] == r["extension_degree"]
        if r["bounded_exhaustive_residual_shift_control"] is not None:
            assert r["bounded_exhaustive_residual_shift_control"] == int(r["hidden_shift_calibration"])


@pytest.mark.parametrize("q,m", [(2, 3), (2, 4), (3, 3), (5, 2)])
def test_geometry_reconstruction_matches_every_small_unfiltered_projective_shift(q, m):
    v, _, _ = singer_parameters(q, m)
    for s in range(v):
        row = classical_control(q, m, s, 42013+s)
        assert row["normal_line_verified_by_secret_only_for_calibration"]
        assert row["bounded_exhaustive_residual_shift_control"] == s


def test_full_trace_values_are_a_stronger_interface_than_membership_bits():
    K, alpha, _ = public_field(3, 3)
    beta = alpha**11
    value_queries = []

    def values(i):
        value_queries.append(i)
        return int((beta*alpha**i).trace())

    recovered, r = trace_reconstruct(K, alpha, values, full_trace_values=True)
    assert recovered == beta
    assert value_queries == [0, 1, 2]
    assert r["method"] == "full-trace-linear-system"
    with pytest.raises(ValueError):
        trace_reconstruct(K, alpha, lambda i: int(values(i) == 0))


def test_large_exponents_survive_json_without_binary64_rounding(report):
    import json
    rows = json.loads(json.dumps(report))["classical_geometry_controls"]
    for r in rows:
        assert type(r["hidden_shift_calibration"]) is str
    row = next(r for r in rows if r["extension_degree"] == 64 and int(r["hidden_shift_calibration"]) > 1)
    assert int(row["hidden_shift_calibration"]) == (2**64-1)//2


def test_known_small_characteristic_dlog_is_not_compared_only_to_exhaustive_search(report):
    for r in report["classical_geometry_controls"]:
        baseline = r["classical_residual_comparator"]
        assert baseline["prime_characteristic"] == r["base_prime"]
        assert baseline["absolute_extension_degree"] == r["extension_degree"]
        assert baseline["quasipolynomial_for_fixed_characteristic"]
        assert not baseline["implemented_here"]
        assert not baseline["runtime_measurement_claim"]
    for r in report["growing_base_field_ledgers"]:
        baseline = r["classical_residual_comparator"]
        assert baseline["prime_characteristic"] == 2
        assert baseline["absolute_extension_degree"] == 3*r["base_field_bits"]


def test_failed_rank_collection_is_reported_without_normalized_away_source_failure():
    K, alpha, _ = public_field(3, 3)
    normal, r = positive_hyperplane_reconstruct(K, alpha, lambda i: 0, 42011, 5)
    assert normal is None
    assert r["budget_exhausted"]
    assert r["oracle_evaluations"] == 5
    assert r["rank"] == 0


@pytest.mark.parametrize("q,m", [(2, 3), (3, 3), (5, 3), (2, 8)])
def test_projective_rank_progress_law_by_literal_point_count(q, m):
    K, alpha, _ = public_field(q, m)
    v, k, _ = singer_parameters(q, m)
    beta = alpha**3
    points = [alpha**i for i in range(v) if (beta*alpha**i).trace() == 0]
    assert len(points) == k
    rows = []
    probabilities = reconstruction_query_law(q, m)["rank_progress_probabilities"]
    from flint import nmod_mat
    for rank in range(m-1):
        outside = [point for point in points if nmod_mat(rows+[_coords(point, m)], q).rank() > rank]
        assert Fraction(len(outside), v) == exact(probabilities[rank])
        rows.append(_coords(outside[0], m))


def test_sparse_membership_gate_and_offset_cost_do_not_transfer_to_full_oracles(report):
    bounds = []
    for r in report["growing_base_field_ledgers"]:
        b = r["base_field_bits"]
        gate, inject = r["query_gate"], r["injectivization"]
        q, v, k, lam = 1 << b, *singer_parameters(1 << b, 3)
        assert gate["queries"] == b*b
        density = Fraction(k, v)
        bits = gate["dyadic_square_root_precision_bits"]
        expected = min(Fraction(1), (_sqrt_upper(Fraction(1, v), bits)+2*b*b*_sqrt_upper(density, bits))**2)
        assert exact(gate["average_shift_recovery_success_upper"]) == expected
        assert not gate["general_full_oracle_DHSP_lower_bound"]
        assert not gate["white_box_normal_or_trace_value_oracle_covered"]
        assert int(inject["necessary_boolean_offsets_for_any_injective_tuple"]) == q
        influence = exact(inject["exact_nonzero_shift_influence"])
        assert influence == Fraction(2*(k-lam), v)
        sufficient = int(inject["sufficient_random_offsets_for_failure_at_most_one_over_64"])
        assert sufficient*influence >= 2*v.bit_length()+6
        bounds.append(expected)
    assert bounds[-1] < Fraction(1, 10**28)


def test_any_injective_sparse_boolean_tuple_needs_density_cost():
    values, v = [1, 0, 0, 1, 0, 0, 0], 7
    # This cardinality bound does not require the difference-set property.
    from itertools import product
    for offsets in product(range(v), repeat=2):
        outputs = [tuple(values[(x+j) % v] for j in offsets) for x in range(v)]
        assert len(set(outputs)) < v


def test_full_physical_spectral_state_not_leading_term_controls_success(report):
    for r in report["spectral_normalization_controls"]:
        assert r["flat_nontrivial_fourier_magnitude_residual"] < 1e-10
        v = r["domain_size"]
        for branch in r["zero_character_controls"]:
            p = branch["executed_target_success"]
            assert p == pytest.approx(branch["complete_normalized_target_formula"])
            assert branch["final_norm"] == pytest.approx(1)
            assert sum(branch["final_probabilities"]) == pytest.approx(1)
            assert p+(v-1)*branch["each_non_target_probability_formula"] == pytest.approx(1)
            assert 0 <= p <= 1+1e-12
    paley = next(r for r in report["spectral_normalization_controls"] if r["domain_size"] == 11)
    assert exact(paley["leading_fourier_target_term_NOT_probability"]) > 1
    bent = next(r for r in report["spectral_normalization_controls"] if r["group"] == "boolean")
    assert bent["zero_character_controls"][0]["executed_target_success"] == pytest.approx(Fraction(49, 64))
    assert bent["zero_character_controls"][1]["executed_target_success"] == pytest.approx(1)
    assert exact(bent["unnormalized_r_instead_of_sqrt_r_norm_countercontrol"]) > 1


def test_no_table_or_flatness_is_promoted_to_a_phase_compiler_or_breakthrough(report):
    assert not any(report["claim_gate"].values())
    for r in report["spectral_normalization_controls"]:
        assert r["phase_correction_tables_only_for_calibration"]
        assert not r["efficient_coherent_phase_recipe_proved_by_this_module"]


def test_native_one_query_fourier_controls_obey_sparse_membership_gate(report):
    for r in report["spectral_normalization_controls"]:
        v, k = r["domain_size"], r["difference_set_size"]
        bound = exact(sparse_membership_gate(v, k, 1)["average_shift_recovery_success_upper"])
        # Shift covariance makes each native success its uniform-shift mean.
        for row in r["zero_character_controls"]:
            assert row["executed_target_success"] <= float(bound)+1e-12
    sparse = next(r for r in report["spectral_normalization_controls"] if r["domain_size"] == 183)
    assert exact(sparse_membership_gate(183, 14, 1)["average_shift_recovery_success_upper"]) < 1
    assert sparse["difference_set_size"] == 14


def test_membership_linear_decode_cannot_be_silently_extended_to_odd_characteristic():
    K, alpha, _ = public_field(3, 3)
    v = singer_parameters(3, 3)[0]
    patterns = [tuple(int((alpha**(s+i)).trace() == 0) for i in range(3)) for s in range(v)]
    assert len(set(patterns)) < v
    # Full trace values, unlike zero/nonzero bits, preserve the whole linear form.
    value_patterns = [tuple(int((alpha**(s+i)).trace()) for i in range(3)) for s in range(26)]
    assert len(set(value_patterns)) == 26


@pytest.mark.parametrize("q,m", [(True, 3), (6, 3), (2, 1)])
def test_invalid_field_parameters_rejected(q, m):
    with pytest.raises(ValueError):
        singer_parameters(q, m)


def test_malformed_or_ungranted_interfaces_rejected():
    K, alpha, _ = public_field(2, 3)
    for oracle in (lambda i: 2, lambda i: True):
        with pytest.raises(ValueError):
            trace_reconstruct(K, alpha, oracle)
    with pytest.raises(ValueError):
        public_field(4, 3)
    with pytest.raises(ValueError):
        public_field(2, 65)
    with pytest.raises(ValueError):
        sparse_membership_gate(7, 7, 2)
    with pytest.raises(ValueError):
        spectral_control([1, 1, 0, 0, 0, 0, 0], "cyclic", 1)

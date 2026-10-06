from fractions import Fraction

import pytest

from dcp_subset_sum_terminal_catalogue import (
    certified_binary_bound,
    data_generator_bound,
    exact_catalogue_bound,
    exact_source_controls,
    generator_certificate,
    hadamard_index_bound,
    is_bad_tuple,
    rank_terms,
    terminal_lattice_controls,
    weighted_bad_tuple_controls,
)


def test_generators_preserve_integer_lattice_not_just_rational_span():
    certificate = generator_certificate(
        [(1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (1, 0, 0, 0)], 4
    )
    assert certificate["initial_saturation_index"] == 2
    assert certificate["final_saturation_index"] == 1
    assert certificate["same_span_index_drop_factors"] == [2]
    assert certificate["data_generator_count"] <= data_generator_bound(4)
    assert certificate["exact_original_lattice_preserved"]


def test_reordering_does_not_charge_all_intermediate_rank_histories():
    patterns = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0),
                (1, 1, 0, 0), (0, 0, 0, 1), (0, 0, 0, 0)]
    for sequence in (patterns, list(reversed(patterns)), patterns * 4):
        certificate = generator_certificate(sequence, 4)
        assert certificate["rank"] == 4
        assert certificate["final_saturation_index"] == 1
        assert certificate["data_generator_count"] <= data_generator_bound(4)


def test_exhaustive_terminal_lattice_certificates_and_bad_cube_gaps():
    controls = terminal_lattice_controls()
    assert sum(row["reachable_lattices_checked"] for row in controls) == 163
    assert sum(row["bad_distinct_row_lattices_checked"] for row in controls) > 0


def test_rank_one_certificate_and_exact_hadamard_rounding():
    certificate = generator_certificate([(0, 0, 0), (1, 1, 1)], 3)
    assert certificate["data_generator_count"] == data_generator_bound(1) == 0
    for rank in range(1, 40):
        h = hadamard_index_bound(rank)
        assert h * h <= rank**rank < (h + 1)**2


@pytest.mark.parametrize("n,c", [(1, 0), (2, -1), (2, 0), (2, 1), (3, 0)])
def test_exhaustive_source_factorial_excess_is_nonnegative_and_bounded(n, c):
    rows = exact_source_controls(n, c)
    assert all(r["control_passed"] for r in rows)


def test_binary_exponent_bound_is_exactly_conservative_in_small_cases():
    for n in range(1, 12):
        for c in (-1, 0, 2):
            if n + c < 1:
                continue
            for k in range(2, 9):
                exponent = certified_binary_bound(n, k, c)
                power = Fraction(1 << exponent) if exponent >= 0 else Fraction(1, 1 << -exponent)
                assert exact_catalogue_bound(n, k, c) <= power


def test_planted_weighting_includes_next_order_and_same_witness_terms():
    result = weighted_bad_tuple_controls()
    assert result["per_instance_inequality_checks"] == 768
    assert result["planted_target_change_of_measure_checked"]
    assert result["legal_target_law_is_joint_conditioning"]
    assert result["per_label_legal_event_squared_bound_checked"]
    inverse = result["expected_inverse_legal_fraction"]
    assert Fraction(int(inverse["numerator"]), int(inverse["denominator"])) <= Fraction(3, 2)
    # The affine Boolean square is nongeneric; every extension stays so.
    assert is_bad_tuple((0, 1, 2, 3), 3)
    assert is_bad_tuple((0, 1, 2, 3, 4), 3)
    assert not is_bad_tuple((0, 1, 2, 4), 3)


def test_per_label_legal_probability_is_not_the_joint_legal_law():
    result = weighted_bad_tuple_controls()
    row = next(r for r in result["rows"] if r["moment_order"] == 4)
    def rational(record):
        return Fraction(int(record["numerator"]), int(record["denominator"]))

    uniform = rational(row["uniform_target_bad_event_probability"])
    per_label = rational(row["per_label_uniform_legal_bad_event_probability"])
    inverse = rational(result["expected_inverse_legal_fraction"])
    assert uniform > 0
    assert per_label != uniform
    assert per_label**2 <= inverse * uniform


def test_two_fifths_power_schedule_survives_old_threshold_but_new_bound_vanishes():
    n = 1 << 24
    k = 776
    assert k**3 > n
    assert certified_binary_bound(n, k, 2) < -1_000_000
    assert rank_terms(n, k, 2)[-1]["boolean_growth_ratio"] == "1/2"


def test_invalid_contract_is_rejected():
    with pytest.raises(ValueError):
        generator_certificate([(1, 2)], 2)
    with pytest.raises(ValueError):
        rank_terms(1, 2, -1)
    with pytest.raises(ValueError):
        rank_terms(4, 1)

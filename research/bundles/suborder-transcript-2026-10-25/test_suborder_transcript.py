from pathlib import Path
import json
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from suborder_transcript import degree_envelope, simultaneous_intertwiner, transcript_from_points
from controls_suborder import (
    inseparable_half_control, map_data, primitive_degree_countercontrol, supplied_transcript_control,
    right_order_inseparability_control, unknown_depth_control,
)
from calibration_controls import vector_operations
from kernel_output import inverse_mod, mod, odd_maximal_order, odd_maximal_split


@pytest.mark.parametrize("phi", [[1, 1, 0, 0], [3, 4, 0, 0], [-1, 0, 2, 0], [-1, -1, 2, 2]])
@pytest.mark.parametrize("prime", [3, 7, 13])
def test_supplied_primitive_maps_have_correct_suborder_transcripts(phi, prime):
    result = supplied_transcript_control(phi, prime)
    assert result["primitive_map"] and result["projective_action_correct"]
    assert result["known_source_calls"] == result["known_suborder_calls"] == 8
    assert result["unknown_isogeny_calls"] == 0
    assert result["coordinate_table_entries"] == 2*prime**2
    assert not result["actual_curve_points_generated"]


@pytest.mark.parametrize("multiple", [2, 11, 44, 121])
def test_nonprimitive_and_p_divisible_suborder_scales_work(multiple):
    result = supplied_transcript_control([1, 1, 0, 0], 5, multiple)
    assert result["degree_envelope"]["query_modulus"] % 11 != 0
    assert result["degree_envelope"]["degree_multiple"] % result["supplied_degree"] == 0


def test_scalar_multiples_cannot_reveal_isogeny_degree():
    assert primitive_degree_countercontrol()["second_map_violates_envelope_without_primitivity"]


def test_inseparable_component_does_not_require_a_ramified_split():
    assert inseparable_half_control()["half_polarization_integral"]


def test_arbitrary_local_basis_changes_preserve_intertwining():
    order, prime = odd_maximal_order(11), 7
    source = odd_maximal_split(11, prime)
    target_change = Matrix([[2, 1], [3, 2]])
    source_change = Matrix([[1, 4], [0, 1]])
    a = [mod(inverse_mod(source_change, prime)*x*source_change, prime) for x in source]
    b = [mod(target_change*x*inverse_mod(target_change, prime), prime) for x in source]
    result = simultaneous_intertwiner(order, a, b, prime, 1)
    expected = mod(target_change*source_change, prime)
    first = next(int(x) for x in expected if x)
    assert result["matrix"] == mod(pow(first, -1, prime)*expected, prime)
    assert not result["global_map_verified"]


def test_local_algebra_failure_is_rejected():
    order, source = odd_maximal_order(11), odd_maximal_split(11, 5)
    broken = list(source)
    broken[0] = 2*eye(2)
    with pytest.raises(ValueError, match="unit"):
        simultaneous_intertwiner(order, source, broken, 5, 1)


def test_nonfaithful_data_rejected():
    order = odd_maximal_order(11)
    with pytest.raises(ValueError, match="invertible"):
        simultaneous_intertwiner(order, [eye(2)]*4, [eye(2)]*4, 5, 1)


@pytest.mark.parametrize("prime,scale", [(4, 1), (5, 5), (5, 0)])
def test_invalid_auxiliary_inputs_rejected(prime, scale):
    with pytest.raises(ValueError):
        simultaneous_intertwiner(odd_maximal_order(11), [eye(2)]*4, [eye(2)]*4, prime, scale)


def test_budget_guard_precedes_endomorphism_calls():
    def forbidden(_):
        pytest.fail("large tables must be refused before evaluator calls")
    operations = vector_operations(65537, 2)
    with pytest.raises(ValueError, match="budget"):
        transcript_from_points(odd_maximal_order(11), 65537, 1,
            ((1, 0), (0, 1)), ((1, 0), (0, 1)), [forbidden]*4, [forbidden]*4, operations, operations)


@pytest.mark.parametrize("scale,p", [(0, 11), (2, 9), (2, 3), (True, 11)])
def test_invalid_envelope_inputs_rejected(scale, p):
    with pytest.raises(ValueError):
        degree_envelope(scale, p)


def test_trivial_separable_component_does_not_invent_an_hsp():
    assert degree_envelope(11**12, 11)["query_modulus"] == 1
    assert degree_envelope(11**12, 11)["degree_multiple"] == 11


@pytest.mark.parametrize("prime", [2, 3, 5])
@pytest.mark.parametrize("exponent", [1, 2, 3, 4])
def test_depth_need_not_have_the_old_content_parity(prime, exponent):
    for depth in range(exponent+1):
        for vector in ((1, 0), (0, 1), (1, prime), (prime, 1), (1, 1)):
            result = unknown_depth_control(prime, exponent, depth, vector)
            assert result["recovered_depth"] == depth
            assert result["containment_calls"] == 2*(exponent+1)


def test_right_order_does_not_require_selecting_the_inseparable_branch():
    assert right_order_inseparability_control()["right_orders_equal_as_rational_lattices"]


def test_full_rank_at_each_prime_does_not_certify_global_consistency():
    order = odd_maximal_order(11)
    for prime in (3, 5, 7):
        source = odd_maximal_split(11, prime)
        # Different independent local choices are not a global geometric witness.
        change = Matrix([[1, prime-1], [0, 1]])
        target = [mod(change*x*inverse_mod(change, prime), prime) for x in source]
        result = simultaneous_intertwiner(order, source, target, prime, 1)
        assert result["solution_dimension"] == 1
        assert not result["global_map_verified"]


def test_receipt_is_json_serializable_and_keeps_execution_gates_closed():
    from replay_suborder import evidence
    record = json.loads(json.dumps(evidence()))
    assert not any(record["scope_flags"].values())
    assert len(record["supplied_map_controls"]) == 15

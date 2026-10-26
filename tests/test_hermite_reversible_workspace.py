from copy import deepcopy
from itertools import product

import pytest

from theorems.hermite_compact_decoder import leading, module_interpolant
from theorems.hermite_reversible_workspace import (
    collision_step, controls, fixed_width_linear, interpolate_traced,
    reduce_traced, undo_reduction, uncompute_interpolation, vector_roundtrip,
    workspace_ledger,
)


def test_fixed_width_linear_map_is_a_bijection_even_off_the_valid_degree_subspace():
    for root in (1, 2):
        images = set()
        for vector in product(range(3), repeat=3):
            out = fixed_width_linear(vector, root, 3)
            images.add(tuple(out))
            assert fixed_width_linear(out, root, 3, inverse=True) == list(vector)
        assert len(images) == 27
    with pytest.raises(ValueError, match="nonzero"):
        fixed_width_linear([1, 2, 0], 0, 3)


def test_discarding_top_degree_is_not_an_ordinary_polynomial_product():
    # Still a bijection modulo X^3, but the ordinary product needs an X^3 term.
    assert fixed_width_linear([0, 0, 1], 1, 3) == [0, 0, 2]
    assert fixed_width_linear([1, 2, 0], 1, 3) == [2, 2, 2]


def test_cancellation_history_reverses_and_recomputes_its_choices():
    original = [[[1], [0, 1]], [[], [1]]]
    basis = deepcopy(original)
    history = reduce_traced(basis, [0, 0], 5)
    assert len(history) == 1
    assert collision_step(basis, [0, 0], 5) is None
    undo_reduction(basis, [0, 0], 5, history)
    assert basis == original


def test_inconsistent_zero_cancellation_history_does_not_clear():
    basis = [[[1], [0, 1]], [[], [1]]]
    history = reduce_traced(basis, [0, 0], 5)
    history[0]["factor"] = 0
    with pytest.raises(ArithmeticError, match="history"):
        undo_reduction(basis, [0, 0], 5, history)


def test_history_is_reversible_data_not_an_authentication_certificate():
    original = [[[1], [0, 1]], [[], [1]]]
    basis = deepcopy(original)
    history = reduce_traced(basis, [0, 0], 5)
    history[0]["factor"] = 2
    undo_reduction(basis, [0, 0], 5, history)
    assert basis != original
    assert basis == [[[1], [0, 2]], [[], [1]]]


@pytest.mark.parametrize("seed", [0, 1, 4])
def test_interpolation_trace_returns_to_identity_and_matches_original(seed):
    p, ell, order, radius = 7, 4, 1, 1
    word = [(i*i+seed*i+seed) % p for i in range((p-1)*ell)]
    trace = interpolate_traced(p, ell, order, radius, word)
    report = uncompute_interpolation(trace, word)
    assert report["basis_restored_to_identity"]
    assert report["history_records_recomputed_and_clearable"] >= 18
    reference = module_interpolant(p, ell, order, radius, word)
    assert [list(leading(row, trace["weights"])) for row in trace["basis"]] == reference["basis_leading_pairs"]


def test_cache_tail_is_required_for_clean_history_reversal():
    p, ell, order = 7, 4, 1
    word = [(i*i+i+1) % p for i in range((p-1)*ell)]
    trace = interpolate_traced(p, ell, order, 1, word)
    changed = deepcopy(trace)
    record = next(record for block in changed["interpolation_history"] for record in block
                  if record["pivot"] is not None)
    record["cache_tails"][0] = (record["cache_tails"][0]+1) % p
    with pytest.raises(ArithmeticError):
        uncompute_interpolation(changed, word)


def test_triangular_vectors_clear_frobenius_free_positions():
    # L=D^[1] over F5, degree<17: four genuinely free Frobenius coordinates.
    pieces = [[], [], [1]]
    for t in (0, 5, 10, 15):
        report = vector_roundtrip(5, 17, pieces, t, homogeneous=True)
        assert report["free_coordinates"] == 4
        assert report["output"] == [int(i == t) for i in range(17)]
        assert report["scratch_all_zero"]


def test_checkpoint_scratch_is_not_replicated_and_scope_is_explicit():
    small = workspace_ledger(31, 24, 4, 10)
    assert not small["sufficient_log_absorption_condition"]
    large = workspace_ledger(1000000007, 256, 15, 430000004)
    assert large["sufficient_log_absorption_condition"]
    assert not large["complete_quantum_circuit_compiled"]
    assert not large["new_quantum_algorithm_claim_allowed"]


def test_native_trace_and_all_implicit_directions_cleanly_reverse():
    report = controls()
    trace = report["native_trace"]
    assert trace["basis_restored_to_identity"]
    assert trace["interpolation_records"] == 600
    assert trace["matches_independent_crt_profile"]
    assert trace["triangular_vectors_checked"] == 13
    assert trace["all_vector_scratch_cleared"]
    assert trace["all_vectors_match_reference"]
    assert not report["new_quantum_algorithm_claim_allowed"]

from fractions import Fraction
from itertools import combinations, product
from math import comb
import random

import pytest

from theorems.folded_rs_decoder import affine_solution
from theorems.hermite_pinned_decoder import (
    HermiteSyndrome, block_weight, decode, differential_space, dual_block,
    jet, operator_matrix, parameters, pin_budget, pin_failure_bound,
    pin_space, resource_ledger, source_herald, controls, sparse_moment_control,
)


def in_space(p, polynomial, space):
    if space is None:
        return False
    rows = [[v[i] for v in space["basis"]] for i in range(len(polynomial))]
    rhs = [(x-y) % p for x, y in zip(polynomial, space["offset"])]
    if not space["basis"]:
        return not any(rhs)
    return affine_solution(p, rows, rhs, len(space["basis"])) is not None


@pytest.mark.parametrize("p,ell", [(3, 1), (5, 2), (7, 4), (11, 8)])
def test_explicit_residue_duality_and_fixed_right_inverse(p, ell):
    code = HermiteSyndrome(p, ell)
    assert code.duality_verified()
    rng = random.Random(p+ell)
    word = [rng.randrange(p) for _ in range(code.width)]
    assert code.transform(code.transform(word), inverse=True) == word
    syndrome = code.syndrome(word)
    e0, y = code.received(syndrome)
    assert code.syndrome(e0) == syndrome
    assert code.transform(y) == [-x % p for x in e0]
    assert code.received(syndrome) == (e0, y)
    assert any(x for row in dual_block(p, ell, 1) for x in row)


def test_hasse_not_ordinary_derivatives_in_small_characteristic():
    f = [0]*6
    f[5] = 1
    assert jet(f, 2, 6, 5) == [2, 0, 0, 0, 0, 1]
    rows, bound = operator_matrix(5, 17, [[0], [1]])
    space = affine_solution(5, rows, [0]*len(rows), 17)
    assert len(space["basis"]) == 4
    assert bound["unpivoted_degree_indices"] == [0, 5, 10, 15]
    assert bound["kernel_dimension_bound"] == 4


@pytest.mark.parametrize("p,k,order", [(3, 10, 2), (5, 17, 3), (7, 23, 4)])
def test_differential_pivot_certificate_against_actual_rank(p, k, order):
    rng = random.Random(p*k)
    for _ in range(12):
        coefficients = [[rng.randrange(p) for _ in range(5)] for _ in range(order+1)]
        rows, bound = operator_matrix(p, k, coefficients)
        space = affine_solution(p, rows, [0]*len(rows), k)
        assert len(space["basis"]) <= bound["kernel_dimension_bound"]
        assert bound["kernel_dimension_bound"] <= order*((k+p-1)//p)
        f = [rng.randrange(p) for _ in range(k)]
        actual = [sum(a*b for a, b in zip(row, f)) % p for row in rows]
        for point in range(p):
            lhs = jet(actual, point, 1, p)[0]
            rhs = sum(jet(poly, point, 1, p)[0]*jet(f, point, order+1, p)[j]
                      for j, poly in enumerate(coefficients)) % p
            assert lhs == rhs


def test_characteristic_order_guard():
    with pytest.raises(ValueError, match="order"):
        operator_matrix(3, 6, [[1]]*4)
    with pytest.raises(ValueError, match="nonzero"):
        operator_matrix(5, 6, [[0], [0]])


@pytest.mark.parametrize("args", [(9, 4, 1, 1), (7, 7, 1, 1), (7, 4, 4, 1),
                                 (13, 8, 2, 4), (7, 4, 1, -1)])
def test_invalid_or_uncertified_parameters_rejected(args):
    with pytest.raises(ValueError):
        parameters(*args)


def test_extra_radius_is_checked_not_silently_dropped():
    parameters(13, 8, 2, 3)
    with pytest.raises(ValueError, match="root"):
        parameters(13, 8, 2, 5)


@pytest.mark.parametrize("p,ell,order,radius", [(5, 4, 1, 0), (7, 4, 1, 1),
                                             (13, 8, 2, 3)])
def test_interpolant_contains_nearby_word_and_local_jet_constraints(p, ell, order, radius):
    k = ell*(p-1)//2
    rng = random.Random(p)
    polynomial = [rng.randrange(p) for _ in range(k)]
    received = [x for a in range(1, p) for x in jet(polynomial, a, ell, p)]
    for i in range(radius):
        received[i*ell:(i+1)*ell] = [rng.randrange(p) for _ in range(ell)]
    info = differential_space(p, ell, order, radius, received)
    assert in_space(p, polynomial, info["affine_space"])
    q = info["interpolant"]
    for i, point in enumerate(range(1, p)):
        for t in range(ell-order):
            value = jet(q[0], point, t+1, p)[t]
            for j in range(order+1):
                value += sum(jet(q[j+1], point, t-u+1, p)[t-u]
                             * comb(j+u, j)*received[i*ell+j+u] for u in range(t+1))
            assert value % p == 0


def test_exhaustive_small_ball_has_no_false_unique_decodes():
    code = HermiteSyndrome(5, 2)
    # Radius zero exercises all 625 code syndromes without list enumeration in decode.
    for syndrome in product(range(5), repeat=code.k):
        result = decode(code, list(syndrome), {}, order=0, radius=0)
        if result["error"] is not None:
            assert result["error"] == [0]*code.width
            assert not any(syndrome)


def test_public_pins_resolve_affine_space_and_wrong_pins_can_fail():
    space = {"offset": [0]*7, "basis": [[int(j == t) for j in range(7)] for t in (0, 5)]}
    assert len(pin_space(5, 4, space, {})["basis"]) == 2
    assert len(pin_space(5, 4, space, {0: [0]*4})["basis"]) == 1
    assert not pin_space(5, 4, space, {0: [0]*4, 1: [0]*4})["basis"]
    assert pin_space(5, 4, space, {0: [0, 1, 0, 0]}) is None
    with pytest.raises(ValueError):
        pin_space(5, 4, space, {4: [0]*4})


def test_rank_exposure_bound_by_exhaustive_pin_subsets():
    p, ell, k = 7, 3, 9
    for degrees in ((0, 7), (0, 1, 2), (2, 3, 8)):
        space = {"offset": [0]*k, "basis": [[int(j == t) for j in range(k)] for t in degrees]}
        for count in range(p):
            bad = sum(bool(pin_space(p, ell, space, {i: [0]*ell for i in r})["basis"])
                      for r in combinations(range(p-1), count))
            assert Fraction(bad, comb(p-1, count)) <= pin_failure_bound(p-1, ell, k, len(degrees), count)


def test_pin_budget_and_half_rate_guard():
    r = pin_budget(1000, 8, 4000, 12, 20)
    assert pin_failure_bound(1000, 8, 4000, 12, r) <= Fraction(1, 2**20)
    assert pin_failure_bound(1000, 8, 4000, 12, r-1) > Fraction(1, 2**20)
    assert pin_budget(1000, 8, 4000, 0, 20) == 0
    with pytest.raises(ValueError):
        pin_failure_bound(10, 4, 21, 1, 1)


def test_unexecuted_asymptotic_ledger_retains_costs_and_claim_gates():
    ledger = resource_ledger()
    assert ledger["guard_radius"] == ledger["source_cap"]+2
    assert ledger["random_pins"] < ledger["parameters"]["n"]//1000
    assert ledger["tight_linear_workspace_claim"] is False
    assert ledger["native_parameters_executed"] is False
    assert ledger["end_to_end_quantum_claim_allowed"] is False
    assert ledger["conditional_total_failure_upper"]["float"] < 0.01


def test_syndrome_decoder_replay_without_error_support():
    code = HermiteSyndrome(7, 4)
    error = [0]*code.width
    error[8:12] = [2, 3, 1, 6]
    result = decode(code, code.syndrome(error), {2: error[8:12]}, order=1, radius=1)
    assert result["error"] == error
    assert result["status"] == "UNIQUE_IN_GUARDED_BALL"
    assert block_weight(result["error"], code.ell) == 1
    assert result["hidden_support_or_polynomial_supplied"] is False
    assert result["coefficient_field_enumeration_used"] is False


def test_native_ambiguous_syndrome_control_and_claim_scope():
    report = controls()
    native = report["native"]
    assert native["error_weights"] == [8, 8]
    assert native["unique_decoding_radius"] == 7
    assert native["unpinned"]["status"] == "ABSTAIN_AMBIGUOUS"
    assert native["pinned"][0]["interpolant"] == native["pinned"][1]["interpolant"]
    assert native["pinned"][0]["interpolant"] == native["unpinned"]["interpolant"]
    for error, decoded in zip(native["two_errors"], native["pinned"]):
        assert source_herald(error, decoded, 24, 8)
        assert not source_herald(error, decoded, 24, 7)
    assert not source_herald(native["two_errors"][1], native["pinned"][0], 24, 8)
    with pytest.raises(ValueError, match="guard"):
        source_herald(native["two_errors"][0], native["pinned"][0], 24, 9)
    assert report["new_quantum_algorithm_claim_allowed"] is False
    assert report["native_quantum_circuit_executed"] is False
    assert report["novelty_established"] is False
    negative = report["guard_negative"]
    assert negative["error_weights"] == [7, 7]
    assert negative["source_norm_squared"] == negative["fourier_source_norm_squared"] == 2
    assert negative["first_moment"] == negative["fourier_first_moment"] == 0
    assert negative["second_moment"] == 8
    assert negative["fourier_second_moment"] == 12
    positive = report["guarded_moment_control"]
    for name in ("source_norm_squared", "first_moment", "second_moment"):
        assert positive[name] == positive["fourier_"+name]


def test_moment_control_refuses_nonlocal_or_nonhermitian_observables():
    code = HermiteSyndrome(3, 1)
    with pytest.raises(ValueError, match="one block"):
        sparse_moment_control(code, [[0, 0]], [[1, 1], [2, 2]], [])
    with pytest.raises(ValueError, match="inverses"):
        sparse_moment_control(code, [[0, 0]], [[1, 0]], [])

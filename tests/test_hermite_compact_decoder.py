from itertools import product
from math import comb
import random

import pytest

from theorems.folded_rs_decoder import affine_solution
from theorems.hermite_pinned_decoder import HermiteSyndrome, operator_matrix, jet
from theorems.hermite_compact_decoder import (
    CompactHermite, DescendingSystem, controls, decode, divide_linear, leading,
    module_interpolant, multiply, subtract, times_linear, weak_popov, workspace_ledger,
)


@pytest.mark.parametrize("p,ell", [(3, 1), (5, 2), (7, 4), (11, 8)])
def test_cardinal_right_inverse_matches_independent_dense_inverse(p, ell):
    compact, dense = CompactHermite(p, ell), HermiteSyndrome(p, ell)
    rng = random.Random(p*ell)
    for _ in range(3):
        syndrome = [rng.randrange(p) for _ in range(compact.k)]
        assert compact.received(syndrome) == dense.received(syndrome)
        error = [rng.randrange(p) for _ in range(compact.width)]
        assert compact.syndrome(error) == dense.syndrome(error)
        assert compact.transform(error) == dense.transform(error)
        assert compact.transform(error, inverse=True) == dense.transform(error, inverse=True)
    assert not hasattr(compact, "g")
    assert not hasattr(compact, "right")


def test_polynomial_arithmetic():
    for p in (3, 5, 7):
        for a in range(p):
            polynomial = [2, 1, 2]
            grown = times_linear(polynomial, a, p)
            assert divide_linear(grown, a, p) == polynomial
            assert grown == multiply(polynomial, [-a % p, 1], p)
        assert subtract([1, 2], [1, 2], 1, 0, p) == []
    with pytest.raises(ArithmeticError):
        divide_linear([1, 0, 1], 0, 7)


def test_shifted_popov_minimal_row_property_by_bounded_combinations():
    p, weights = 5, [-4, 0]
    original = [[[1, 0, 1], [1]], [[2, 1], [0, 1]]]
    basis, count, _ = weak_popov(original, weights, p)
    assert count >= 0
    assert len({leading(row, weights)[1] for row in basis}) == 2
    minimum = min(leading(row, weights)[0] for row in basis)
    for a, b in product(range(p), repeat=2):
        if a == b == 0:
            continue
        row = [subtract([a*x % p for x in xpoly], ypoly, -b % p, 0, p)
               for xpoly, ypoly in zip(basis[0], basis[1])]
        assert leading(row, weights)[0] >= minimum


@pytest.mark.parametrize("p,ell,order,radius", [(5, 4, 1, 0), (7, 4, 1, 1),
                                             (13, 8, 2, 3), (17, 16, 3, 5)])
def test_module_interpolant_all_constraints_and_degree_bounds(p, ell, order, radius):
    rng = random.Random(p)
    received = [rng.randrange(p) for _ in range((p-1)*ell)]
    info = module_interpolant(p, ell, order, radius, received)
    q, spec = info["interpolant"], info["parameters"]
    assert len(q[0]) <= spec["a"]+spec["k"]
    assert all(len(poly) <= spec["a"]+j+1 for j, poly in enumerate(q[1:]))
    assert len(set(pair[1] for pair in info["basis_leading_pairs"])) == order+2
    for i, point in enumerate(range(1, p)):
        for t in range(ell-order):
            value = jet(q[0], point, t+1, p)[t]
            for j in range(order+1):
                value += sum(jet(q[j+1], point, t-u+1, p)[t-u]
                             * comb(j+u, j)*received[i*ell+j+u] for u in range(t+1))
            assert value % p == 0
    assert info["dense_scalar_interpolation_matrix_stored"] is False
    assert info["selection"] == "fewest_pivots"


def test_descending_small_characteristic_free_coordinates_and_pins():
    system = DescendingSystem(5, 17, [[], [], [1]])
    assert system.free == [0, 5, 10, 15]
    assert system.solve({}, 4)["remaining_dimension"] == 4
    polynomial = [0]*17
    for i, value in zip(system.free, (1, 2, 3, 4)):
        polynomial[i] = value
    pins = {i: jet(polynomial, i+1, 4, 5) for i in range(4)}
    result = system.solve(pins, 4)
    assert result["polynomial"] == polynomial
    assert result["stored_echelon_field_entries"] == 20
    assert result["peak_constraint_batch_field_entries"] <= 2*17


@pytest.mark.parametrize("p,k", [(3, 7), (5, 12), (7, 16)])
def test_descending_solver_matches_dense_identity_space(p, k):
    rng = random.Random(p*k)
    for _ in range(8):
        operator = [[rng.randrange(p) for _ in range(4)] for _ in range(3)]
        rows, _ = operator_matrix(p, k, operator)
        f = [rng.randrange(p) for _ in range(k)]
        q0 = [-sum(x*y for x, y in zip(row, f)) % p for row in rows]
        dense = affine_solution(p, rows, [-x % p for x in q0], k)
        system = DescendingSystem(p, k, [q0]+operator)
        result = system.solve({}, 2)
        assert result["status"] in ("UNIQUE_AFFINE_SOLUTION", "ABSTAIN_AMBIGUOUS")
        assert result["remaining_dimension"] == len(dense["basis"])
        if not dense["basis"]:
            assert result["polynomial"] == f
        ell = (k+p-2)//(p-1)
        pins = {i: jet(f, i+1, ell, p) for i in range(p-1)}
        pinned = system.solve(pins, ell)
        assert pinned["polynomial"] == f


def test_skipped_equations_and_wrong_pins_are_rechecked():
    # Multiplication operator fixes f=0. There are no free coordinates.
    system = DescendingSystem(5, 3, [[], [1]])
    assert system.solve({0: [1, 0]}, 2)["status"] == "ABSTAIN_INCONSISTENT"
    # Output degree higher than the operator can produce is inconsistent.
    system = DescendingSystem(5, 3, [[0, 0, 0, 1], [1]])
    assert system.solve({}, 2)["status"] == "ABSTAIN_INCONSISTENT"


def test_compact_syndrome_decoding_without_dense_storage():
    code = CompactHermite(7, 4)
    error = [0]*code.width
    error[8:12] = [2, 3, 1, 6]
    result = decode(code, code.syndrome(error), {2: error[8:12]}, order=1, radius=1)
    assert result["error"] == error
    assert result["status"] == "UNIQUE_IN_GUARDED_BALL"
    assert result["dense_affine_basis_stored"] is False
    assert result["dense_syndrome_right_inverse_stored"] is False


def test_workspace_contract_preserves_reversible_cost_and_fixed_multiplicity_scope():
    ledger = workspace_ledger(31, 24, 4, 10)
    assert ledger["logarithmic_reversible_overhead_removed"] is False
    assert ledger["original_tight_linear_quantum_space_proved"] is False
    assert ledger["quantum_algorithm_claim_allowed"] is False
    assert "ell=1" in ledger["fixed_ell_scope"]


def test_native_ambiguity_replay_and_shortest_row_negative():
    report = controls()
    assert report["error_weights"] == [8, 8]
    assert report["unique_decoding_radius"] == 7
    assert report["unpinned"]["status"] == "ABSTAIN_AMBIGUOUS"
    for output, error in zip(report["pinned"], report["two_errors"]):
        assert output["status"] == "UNIQUE_IN_GUARDED_BALL"
        assert output["error"] == error
        assert output["reduced_system"]["peak_constraint_batch_field_entries"] <= report["n"]*report["ell"]
        assert output["interpolant"] == report["unpinned"]["interpolant"]
    rejected = report["shortest_interpolant_same_eight_pins"]
    assert rejected["status"] == "ABSTAIN_AMBIGUOUS"
    assert rejected["reduced_system"]["dimension_before_pins"] == 24
    assert rejected["reduced_system"]["remaining_dimension"] == 4
    assert report["unpinned"]["reduced_system"]["dimension_before_pins"] == 1
    assert report["new_quantum_algorithm_claim_allowed"] is False
    assert report["native_quantum_circuit_executed"] is False

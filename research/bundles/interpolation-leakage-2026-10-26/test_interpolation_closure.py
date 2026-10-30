"""Local exact controls, not discovery of geometric automorphisms or maps."""

from itertools import product
from pathlib import Path
from random import Random
import sys

import pytest
from sympy import Matrix, Rational, eye, zeros

from interpolation_closure import (
    adjoint, category_basis, category_contains, cross_completion_rank,
    cross_escape_from_source_coordinates, cross_is_new, interpolation_diamond,
    leaf_candidates, target_basis, target_contains, target_escape_from_source_coordinates,
    terminal_generators,
)
from source_split import SearchBudgetExceeded


@pytest.mark.parametrize("q", [3, 5, 17])
def test_known_category_is_closed_under_multiplication_and_adjoint(q):
    basis = category_basis(q)
    assert abs(Matrix.hstack(*(Matrix(list(x)) for x in basis)).det()) == q**7
    assert abs(target_basis(q).det()) == q**3
    for x in basis:
        assert category_contains(x, q)
        assert category_contains(adjoint(x), q)
        for y in basis:
            assert category_contains(x*y, q)


@pytest.mark.parametrize("q", [3, 5, 17])
def test_terminal_iso_ambiguity_and_pullbacks_stay_in_known_q_local_order(q):
    psi, auxiliary = interpolation_diamond(q, (1, 2, 1, 1))
    assert category_contains(psi, q, 4)
    assert category_contains(adjoint(psi)/auxiliary, q, 4)
    for automorphism in terminal_generators():
        assert adjoint(automorphism)*automorphism == eye(16)
        assert category_contains(automorphism, q, 4)
        assert category_contains(automorphism*psi, q, 4)
        pullback = adjoint(psi)*automorphism*psi/auxiliary
        assert category_contains(pullback, q, 4)
        for i in range(4, 8):
            for j in range(4, 8):
                assert target_contains(pullback[2*i:2*i+2, 2*j:2*j+2], q)


def test_q_denominator_invalidates_the_closure_argument():
    q = 5
    z = Matrix([[q, 0], [0, 0]])
    assert target_contains(z, q)
    assert not target_contains(z/q, q)
    assert target_contains(z/6, q)


@pytest.mark.parametrize("q", [3, 5, 17])
def test_new_cross_map_can_complete_order_even_with_degree_divisible_by_q(q):
    old = Matrix.diag(q, 1)
    new = Matrix.diag(1, q)
    assert new.det() == old.det() == q
    assert not cross_is_new(old, q)
    assert cross_is_new(new, q)
    assert cross_completion_rank(old, q) == 2
    assert cross_completion_rank(new, q) == 4


def test_all_mod_three_cross_maps_obey_exact_escape_criterion():
    for values in product(range(3), repeat=4):
        eta = Matrix(2, 2, values)
        assert cross_completion_rank(eta, 3) == (4 if cross_is_new(eta, 3) else 2)


def test_source_target_swap_is_not_an_available_product_automorphism():
    # This is a legitimate local symplectic matrix, but would geometrically
    # require an isomorphism E0=E. Local symplecticity cannot grant that map.
    swap = zeros(4)
    swap[:2, 2:] = eye(2)
    swap[2:, :2] = eye(2)
    assert adjoint(swap)*swap == eye(4)
    assert not category_contains(swap, 5)


def test_unknown_partial_quotient_symmetry_is_not_covered_by_terminal_closure():
    q = 5
    eta = Matrix.diag(1, q)
    extra = zeros(4)
    extra[2:, :2] = eta
    assert not category_contains(extra, q)
    assert cross_completion_rank(eta, q) == 4


@pytest.mark.parametrize("q,roots", [(9, (1, 2, 1, 1)), (5, (0, 0, 0, 0)), (5, (1, 2, 0, 0))])
def test_invalid_auxiliary_data_rejected(q, roots):
    with pytest.raises(ValueError):
        interpolation_diamond(q, roots)


def test_nonintegral_cross_matrix_is_not_silently_reduced():
    with pytest.raises(ValueError, match="integral"):
        cross_completion_rank(Matrix.diag(Rational(1, 5), 1), 5)


def test_cross_escape_is_detected_from_known_source_trace_coordinates():
    assert cross_escape_from_source_coordinates(Matrix([0, 1, 5, 0]), 5)
    assert not cross_escape_from_source_coordinates(Matrix([5, 0, 10, 0]), 5)
    with pytest.raises(ValueError, match="integral"):
        cross_escape_from_source_coordinates(Matrix([Rational(1, 5), 0, 0, 0]), 5)


def test_target_escape_uses_different_scalar_and_nonscalar_divisibilities():
    assert not target_escape_from_source_coordinates(Matrix([5, 25, 0, 50]), 5)
    assert target_escape_from_source_coordinates(Matrix([5, 5, 0, 0]), 5)
    assert target_escape_from_source_coordinates(Matrix([1, 25, 0, 0]), 5)


@pytest.mark.parametrize("q", [3, 5, 17, 2**61-1, 1000000009])
def test_new_integral_element_yields_at_most_two_candidates_without_enumeration(q):
    result = leaf_candidates(Matrix.diag(0, 1), q, Random(7))
    assert result["status"] == "CANDIDATES"
    assert set(result["lines"]) == {(1, 0), (0, 1)}
    assert result["native_certification_performed"] is False
    result = leaf_candidates(Matrix([[0, 1], [0, 0]]), q)
    assert result["lines"] == [(1, 0)]


def test_fractional_element_can_identify_a_unique_leaf():
    result = leaf_candidates(Matrix([[0, Rational(1, 5)], [0, 0]]), 5)
    assert result["lines"] == [(1, 0)]
    # Nilpotent residue pole alone is not sufficient to preserve the lattice.
    bad = leaf_candidates(Matrix([[0, Rational(1, 5)], [1, 0]]), 5)
    assert bad["status"] == "INCONSISTENT_WITH_NEIGHBOR_PROMISE"


def test_old_element_and_sampling_timeout_are_not_negative_evidence():
    assert leaf_candidates(eye(2)+5*Matrix([[0, 1], [0, 0]]), 5)["status"] == "NO_NEW_LOCAL_INFORMATION"
    with pytest.raises(SearchBudgetExceeded, match="UNKNOWN"):
        leaf_candidates(Matrix.diag(0, 1), 5, Random(0), trials=0)


@pytest.mark.parametrize("q,direction", [(3, 0), (5, None), (17, 2)])
def test_actual_quaternion_neighbor_fixtures_survive_one_map_filter(q, direction):
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root / "native-nonbass-realization-2026-10-26"))
    from native_realization import fixture
    from kernel_output import action, lift_split, odd_maximal_split
    f = fixture(q, direction)
    split = lift_split(f["source"], odd_maximal_split(11, q), q)
    expected = (0, 1) if direction is None else (1, direction)
    informative = 0
    for i in range(4):
        x = f["target_basis"][:, i]
        if all(v.q == 1 for v in f["r_basis"].inv()*x):
            continue
        representative = action(q*x, split)/q
        result = leaf_candidates(representative, q, Random(11))
        assert result["status"] == "CANDIDATES"
        assert expected in result["lines"]
        assert len(result["lines"]) <= 2
        informative += 1
    assert informative


def test_receipt_does_not_promote_local_controls_to_native_execution():
    from replay_leakage import receipt
    result = receipt()
    assert result["large_prime_selector_candidate_count"] == 2
    scope = result["execution_scope"]
    assert scope["exact_supplied_local_coordinate_controls"] is True
    assert all(not value for key, value in scope.items()
               if key != "exact_supplied_local_coordinate_controls")

"""Exact classical-filter controls; surviving a rank cap is NOT hardness."""
from dataclasses import replace
from fractions import Fraction
from itertools import product

from flint import fq_default_ctx
import pytest

import theorems.polynomial_orbit_module as module
from theorems.polynomial_orbit_module import (
    MooreMinor, _class_nine_generators, _ut3_generators, baseline_report,
    discover_orbit_module, orbit_module_budget, verify_evaluation_rank,
)
from theorems.ut5_matrix_phase_alignment import _identity, _lists, _matrix, _product


@pytest.mark.parametrize("p", [2, 3, 5, 2**127-1])
def test_linear_module_including_small_characteristic(p):
    evaluator = lambda x, field: x[0]
    result = discover_orbit_module(p, 3, evaluator, 1, _ut3_generators(3), 3, seed=29)
    assert result.closed and result.rank == 3
    assert verify_evaluation_rank(result, evaluator)
    assert result.processed_candidates == 7
    assert result.relation_tests <= result.processed_candidates
    assert result.error_bound <= Fraction(1, 100)
    assert result.randomness == "seeded_diagnostic"
    # Independent exact degree-one representation: coefficients are first inverse rows.
    vectors = [_lists(_matrix(g, p).inv())[0] for g in result.basis_transforms]
    for g, action in zip(result.original_generators, result.generator_actions):
        for j, b in enumerate(result.basis_transforms):
            expected = _lists(_matrix(_product(g, b, p), p).inv())[0]
            assert expected == [sum(action[i][j]*v[t] for i, v in enumerate(vectors)) % p
                                for t in range(3)]


def test_degree_p_lift_and_small_characteristic_relative_to_dimension():
    polynomial = MooreMinor(5, 6, (0, 1, 3, 4, 5))
    result = discover_orbit_module(5, 6, polynomial, polynomial.degree_bound, _ut3_generators(6), 3, seed=29)
    assert polynomial.degree_bound == 781
    assert len(polynomial.indices) == polynomial.prime  # Old no-carry guard is not available.
    assert polynomial.dimension > polynomial.prime
    assert result.closed and result.rank == 3
    assert verify_evaluation_rank(result, polynomial)
    assert polynomial.verify_representation(result)


def test_noncommuting_action_and_all_stabilizers_against_formal_minor_coefficients():
    p = 5
    polynomial = MooreMinor(p, 3, (0, 1))
    result = discover_orbit_module(p, 3, polynomial, polynomial.degree_bound, _ut3_generators(3), 3, seed=11)
    a, b = [_matrix(g, p) for g in result.generator_actions]
    commutator = a*b*a.inv()*b.inv()
    assert a*b != b*a
    count = 0
    for u, v, w in product(range(p), repeat=3):
        g = ((1, u, w), (0, 1, v), (0, 0, 1))
        action = a**u*b**v*commutator**((w-u*v) % p)
        fixes_target = [int(action[i, 0]) for i in range(3)] == [1, 0, 0]
        formal_fix = polynomial.exterior_coefficients(g) == polynomial.exterior_coefficients(_identity(3))
        assert fixes_target == formal_fix == (v == w == 0)
        count += fixes_target
    assert count == p  # A nonnormal subgroup, not just the group's common invariants.


def test_large_prime_requires_base_field_linear_algebra_not_extension_coefficients():
    p = 2**127-1
    polynomial = MooreMinor(p, 3, (0, 1))
    result = discover_orbit_module(p, 3, polynomial, p+1, _ut3_generators(3), 3, seed=29)
    assert result.extension_degree == 2 and result.rank == 3
    assert len(result.evaluation_points) >= 2
    assert verify_evaluation_rank(result, polynomial)
    assert polynomial.verify_representation(result)
    assert len(result.faithful_generators[0]) == 6


def test_actual_class_nine_group_has_rank_ten_despite_huge_degree():
    polynomial = MooreMinor(43, 10, tuple(range(9)))
    result = discover_orbit_module(43, 10, polynomial, polynomial.degree_bound,
                                   _class_nine_generators(43), 10, seed=29)
    assert polynomial.degree_bound == 11966490760401
    assert 43 <= (polynomial.dimension-1)*len(polynomial.indices)  # Mixed derivative guard fails.
    assert result.rank == 10 and result.processed_candidates == 21
    assert verify_evaluation_rank(result, polynomial)
    assert polynomial.verify_representation(result)
    assert len(result.faithful_generators[0]) == 20


@pytest.mark.parametrize("constant,rank", [(0, 0), (3, 1)])
def test_constant_and_zero_circuits_keep_the_original_group_block(constant, rank):
    evaluator = lambda x, field: constant
    generators = _ut3_generators(3)
    result = discover_orbit_module(5, 3, evaluator, 0, generators, 1, seed=29)
    assert result.closed and result.rank == rank and result.error_bound == 0
    assert verify_evaluation_rank(result, evaluator)
    for g, original in zip(result.faithful_generators, generators):
        assert [list(row[:3]) for row in g[:3]] == original
        assert tuple(sum(a*b for a, b in zip(row, result.target)) % 5 for row in g) == result.target


def test_nonfaithful_orbit_action_is_not_quotiented_away():
    result = discover_orbit_module(5, 3, lambda x, field: x[2], 1, _ut3_generators(3), 1, seed=29)
    assert result.generator_actions == (((1,),), ((1,),))
    g, h = [_matrix(g, 5) for g in result.faithful_generators]
    assert g*h != h*g  # Original UT3 remains, even though its orbit action is trivial.


def test_trivial_group_still_tests_whether_the_polynomial_is_zero():
    evaluator = lambda x, field: x[0]**5-x[0]
    result = discover_orbit_module(5, 1, evaluator, 5, [], 1, seed=29)
    assert result.rank == 1 and result.processed_candidates == result.relation_tests == 1
    assert result.generator_actions == result.faithful_generators == ()
    assert verify_evaluation_rank(result, evaluator)
    assert all((x**5-x) % 5 == 0 for x in range(5))  # Base-field function is misleading.


def test_rank_cap_preserves_exact_independence_and_forbids_representation():
    evaluator = lambda x, field: x[0]**126
    result = discover_orbit_module(127, 3, evaluator, 126, _ut3_generators(3), 5, seed=29)
    assert result.status == "RANK_CAP_EXCEEDED" and result.rank == 6
    assert verify_evaluation_rank(result, evaluator)
    assert not result.closed and not result.generator_actions
    with pytest.raises(ValueError, match="not a representation"):
        _ = result.faithful_generators
    with pytest.raises(ValueError, match="not a representation"):
        _ = result.target


def test_a_new_point_falsifies_dependence_inferred_from_an_old_point(monkeypatch):
    _, k, _ = orbit_module_budget(5, 1, 1, 2)
    # First point (1,0) cannot distinguish x0 and x0-x1. Next point (0,1) does.
    draws = iter([1]+[0]*(2*k-1)+[0]*k+[1]+[0]*(k-1))
    class ScriptedRandom:
        def randrange(self, p):
            return next(draws, 0)
    monkeypatch.setattr(module.random, "Random", lambda seed: ScriptedRandom())
    evaluator = lambda x, field: x[0]
    result = discover_orbit_module(5, 2, evaluator, 1, [((1, 1), (0, 1))], 2, seed=29)
    assert result.rank == 2 and result.relation_tests == 3
    assert verify_evaluation_rank(result, evaluator)
    assert result.generator_actions == (((0, 4), (1, 2)),)


def test_independence_certificate_does_not_certify_closure(monkeypatch):
    class AlwaysZero:
        def randrange(self, p):
            return 0
    monkeypatch.setattr(module.random, "Random", lambda seed: AlwaysZero())
    polynomial = MooreMinor(5, 3, (0, 1))
    result = discover_orbit_module(5, 3, polynomial, 6, _ut3_generators(3), 3, seed=29)
    assert result.rank == 0 and result.status == "CLOSED_MONTE_CARLO"
    assert verify_evaluation_rank(result, polynomial)  # Empty family is independent.
    assert not polynomial.verify_representation(result)  # Closure was nevertheless WRONG.
    assert result.randomness == "seeded_diagnostic"  # Ideal-random error bound cannot apply here.


def test_certificate_replay_and_formal_checker_reject_tampering():
    polynomial = MooreMinor(5, 3, (0, 1))
    result = discover_orbit_module(5, 3, polynomial, 6, _ut3_generators(3), 3, seed=29)
    assert not verify_evaluation_rank(replace(result, basis_sketches=()), polynomial)
    assert not polynomial.verify_representation(replace(result, generator_actions=()))
    wrong = (tuple(map(tuple, _identity(3))),)*2
    assert not polynomial.verify_representation(replace(result, generator_actions=wrong))


def test_foreign_extension_field_result_is_rejected():
    wrong = fq_default_ctx(7, 2)
    with pytest.raises(ValueError, match="fields must match"):
        discover_orbit_module(5, 1, lambda x, field: wrong.gen(), 1, [], 1, seed=29)


@pytest.mark.parametrize("args", [
    (4, 1, 1, 2), (True, 1, 1, 2), (5, -1, 1, 2), (5, True, 1, 2),
    (5, 1, -1, 2), (5, 1, 1, 0), (5, 1, 1, True),
])
def test_invalid_budget_contracts_are_rejected(args):
    with pytest.raises(ValueError):
        orbit_module_budget(*args)


@pytest.mark.parametrize("generators", [[[[1]]], [[[1, 0], [0, 0]]],
                                        [[[1, 5], [0, 1]]], [[[1, True], [0, 1]]]])
def test_invalid_generators_are_rejected(generators):
    with pytest.raises(ValueError):
        discover_orbit_module(5, 2, lambda x, field: x[0], 1, generators, 2, seed=29)


def test_budget_depends_on_log_degree_and_number_of_candidates_not_group_order():
    degree = 2**4096
    cap, k, error = orbit_module_budget(127, degree, 2, 10, Fraction(1, 2**40))
    assert cap == 21 and k < 600 and error <= Fraction(1, 2**40)
    assert Fraction(degree*cap, 127**(k-1)) > Fraction(1, 2**40)
    for epsilon in (0.01, Fraction(0), Fraction(1)):
        with pytest.raises(ValueError):
            orbit_module_budget(5, 1, 1, 2, epsilon)


def test_live_report_does_not_promote_rank_cap_or_claim_a_solver():
    report = baseline_report()
    assert [c["rank"] for c in report["controls"]] == [3, 3, 10]
    assert all(c["exact_exterior_generator_identities_verified"] for c in report["controls"])
    assert not any(c["stabilizer_backend_executed"] for c in report["controls"])
    assert report["class_nine_group"]["derived_dimensions"] == [19, 17, 10, 0]
    assert report["rank_cap_control"]["hardness_inferred"] is False

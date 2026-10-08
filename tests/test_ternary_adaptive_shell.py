from itertools import product

from flint import fmpq
import pytest

from ternary_pair_collimation import LowProblem
from ternary_pair_lattice import embed, word_coordinates
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import (
    adaptive_pair, block_minimum_energy, coefficient_interval,
    compile_adaptive, native_cut, nearest_order,
)


def view(A=(1, 7, 11, 18), Q=27):
    return LowProblem((Q,), tuple(((a,), (b,)) for a, b in zip(A[::2], A[1::2])), 0)


def prepared(problem):
    policy = frozen_policy(problem, _serialized_prepared(public_charts(problem, 83950)))
    return policy, compile_adaptive(policy)


def test_integer_intervals_are_inclusive_exact_at_negative_half_ties_and_tiny_radii():
    for x in (fmpq(-7, 2), fmpq(-1, 2), fmpq(1, 2), fmpq(5, 3), fmpq(0)):
        for R in (fmpq(0), fmpq(1, 4), fmpq(1, 10**30), fmpq(5), fmpq(100)):
            lo, hi = coefficient_interval(x, R)
            expected = [c for c in range(-20, 21) if (x-c)**2 <= R]
            assert list(range(lo, hi+1)) == expected
            sequence = list(nearest_order(x, lo, hi))
            assert sorted(sequence) == expected
            assert [(x-c)**2 for c in sequence] == sorted((x-c)**2 for c in sequence)
    assert coefficient_interval(fmpq(0), fmpq(-1)) == (1, 0)
    assert list(nearest_order(fmpq(0), 1, 0)) == []


def test_rank_zero_one_and_two_block_projectors_use_exact_range_constraints():
    z = fmpq(0)
    assert block_minimum_energy((z, z, z), z, z) == 0
    assert block_minimum_energy((z, z, z), fmpq(1), z) is None
    gram = (fmpq(1, 6), fmpq(-1, 6), fmpq(1, 6))
    assert block_minimum_energy(gram, fmpq(1), fmpq(-1)) == 6
    assert block_minimum_energy(gram, fmpq(1), fmpq(1)) is None
    assert block_minimum_energy((z, z, fmpq(2)), z, fmpq(4)) == 8
    assert block_minimum_energy((fmpq(2), fmpq(1), fmpq(3)), fmpq(2), fmpq(3)) == fmpq(18, 5)
    with pytest.raises(ValueError):
        block_minimum_energy((fmpq(1), fmpq(2), fmpq(1)), z, z)
    with pytest.raises(ValueError):
        block_minimum_energy((1,0,1),1,2)


def test_all81_tiny_native_label_arrays_all729_targets_and_all_cuts_match_full_fibers():
    total_pairs = 0
    for A in product(range(9), repeat=2):
        problem = view(A, 9); policy, compiled = prepared(problem)
        for target in range(9):
            expected = [w for w in product(range(3), repeat=1) if problem.value(w) == (target,)]
            for cut in ("sphere", "simplex", "projector"):
                answer = adaptive_pair(problem, (target,), policy, compiled, 1000, cut, False)
                assert answer["complete_fiber"]
                assert sorted(answer["witnesses"]) == expected
                assert bool(answer["pair"]) == (len(expected) >= 2)
                assert answer["cost"]["coefficient_nodes"] == sum(answer["cost"]["nodes_by_row"])
                assert answer["cost"]["training_words"] == 0
                if cut == "sphere": total_pairs += bool(answer["pair"])
    assert total_pairs == 25


@pytest.mark.parametrize("A,Q", [((1,7,11,18),27), ((9,23,41,37,65,19),81), ((0,0,0,0),27)])
def test_every_target_complete_enumeration_matches_real_native_fiber_for_larger_controls(A,Q):
    problem = view(A,Q); policy, compiled = prepared(problem)
    fibers = {t: [] for t in range(Q)}
    for word in product(range(3), repeat=problem.width): fibers[problem.value(word)[0]].append(word)
    for target, expected in fibers.items():
        for cut in ("sphere", "simplex", "projector"):
            answer = adaptive_pair(problem, (target,), policy, compiled, 100_000, cut, False)
            assert answer["complete_fiber"]
            assert sorted(answer["witnesses"]) == expected
            assert answer["cost"]["leaf_points"] == len(expected)
            assert all(trace["exact_original_norm"] == str(6*problem.width) for trace in answer["traces"])


def test_projector_cuts_never_remove_any_true_word_at_any_partial_depth():
    problem = view((9,23,41,37,65,19),81); policy, compiled = prepared(problem)
    for word in product(range(3), repeat=problem.width):
        z = word_coordinates(word)
        e = embed(tuple(1-3*x for x in z))
        projected = (fmpq(0),)*(3*problem.width); spent = fmpq(0)
        for i in range(2*problem.width-1,-1,-1):
            gs = compiled["gs"][i]; norm = compiled["basis"]["gs_q"][i]
            rho = sum((x*y for x,y in zip(e,gs)), fmpq(0))/norm
            projected = tuple(a+rho*b for a,b in zip(projected,gs)); spent += rho*rho*norm
            assert sum((x*x for x in projected), fmpq(0)) == spent
            assert native_cut(projected,spent,fmpq(6*problem.width)-spent)[0]
            assert native_cut(projected,spent,fmpq(6*problem.width)-spent,compiled["prefix_block_projectors"][i])[0]
            lo, hi = compiled["native_rho_ranges"][i]
            assert lo <= rho <= hi


def test_block_energy_bounds_must_not_be_added_across_correlated_blocks():
    # Prefix span generated by three copies of (1,-1,0); all three restrictions
    # describe the SAME vector. Summing minimum energies triples its norm.
    gram = (fmpq(1,6),fmpq(-1,6),fmpq(1,6))
    energies = [block_minimum_energy(gram,fmpq(1),fmpq(-1)) for _ in range(3)]
    assert max(energies) == 6 and sum(energies) == 18


def test_caps_cannot_certify_empty_and_larger_budget_preserves_a_fixed_search_prefix():
    problem = view(); policy, compiled = prepared(problem)
    for target in range(27):
        capped = adaptive_pair(problem,(target,),policy,compiled,1,"sphere",False)
        if not capped["complete_fiber"]:
            assert capped["status"].startswith("NODE_CAP")
            assert capped["cost"]["coefficient_nodes"] == 1
        whole = adaptive_pair(problem,(target,),policy,compiled,1000,"sphere",False)
        assert whole["complete_fiber"]
        assert set(capped["witnesses"]) <= set(whole["witnesses"])
    target = next(t for t in range(27) if sum(problem.value(w)==(t,) for w in product(range(3),repeat=2))>=2)
    stopped = adaptive_pair(problem,(target,),policy,compiled,1000)
    assert stopped["pair"] and not stopped["complete_fiber"]
    assert stopped["status"] == "VERIFIED_ADAPTIVE_PAIR_NO_COVERAGE_THEOREM"


def test_invalid_budgets_access_and_cut_names_fail_closed():
    problem = view(); policy, compiled = prepared(problem)
    for cap in (0,-1,True,1.5):
        with pytest.raises(ValueError): adaptive_pair(problem,(0,),policy,compiled,cap)
    with pytest.raises(ValueError): adaptive_pair(problem,(0,),policy,compiled,cut="heuristic-prune")
    with pytest.raises(ValueError): adaptive_pair(view((1,2,3,4)),(0,),policy,compiled)
    with pytest.raises(ValueError): coefficient_interval(0,fmpq(1))
    with pytest.raises(ValueError): compile_adaptive(policy,-1)

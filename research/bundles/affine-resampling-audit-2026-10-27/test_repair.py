from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import sys

import pytest
from flint import nmod_mat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bounds import (fixed_bank_isolation, pair_overlap, prime_source_locality,
                    stationary_hitting)
from repair import BlockRepair, frozen_basis, frozen_zero_coordinate
from small_prime import P, build_control


@pytest.mark.parametrize("p", [3, 5, 7, 11])
def test_block_repair_all_syndromes(p):
    solver = BlockRepair(p, [[1, 1, 0, 0], [0, 0, 1, 2]], [(0, 1), (2, 3)])
    for target in product(range(p), repeat=2):
        result = solver.solve(target)
        assert result["status"] == "VERIFIED_FULL_SUPPORT_WITNESS"
        assert solver.fiber.verifies(result["witness"], target)
        assert not result["uniform_output_law"]


def test_actual_native_all_fibers_and_syndromes():
    problem, _, data = build_control()
    B = data["original_parity"]
    blocks = [tuple(range(i, i+16)) for i in range(0, 176, 16)]
    solver = BlockRepair(P, B, blocks)
    assert not solver.issues
    for block, direction in zip(blocks, solver.directions):
        local = nmod_mat([[row[j] for j in block] for row in B], P)
        assert local.rank() == 15
        assert all(direction)
        # Residues of (dx/y)/(x-a) agree up to one nonzero scalar.
        residues = [pow(data["evaluation_points"][j]["y"], -1, P) for j in block]
        ratio = direction[0]*pow(residues[0], -1, P) % P
        assert all(v == ratio*r % P for v, r in zip(direction, residues))
    targets = [[0]*43, [1]*43, list(range(43))]
    targets += [[int(i == j) for i in range(43)] for j in range(43)]
    for target in targets:
        assert problem.verifies(solver.solve(target)["witness"], target)


def test_native_permutation_scaling_and_row_change():
    _, _, data = build_control()
    B = data["original_parity"]
    perm = list(reversed(range(176)))
    multipliers = [j % (P-1)+1 for j in range(176)]
    changed = [[row[perm[j]]*multipliers[j] % P for j in range(176)] for row in B]
    changed[0] = [(x+3*y) % P for x, y in zip(changed[0], changed[1])]
    inverse = {old: new for new, old in enumerate(perm)}
    blocks = [[inverse[j] for j in range(i, i+16)] for i in range(0, 176, 16)]
    solver = BlockRepair(P, changed, blocks)
    target = list(range(43))
    assert solver.fiber.verifies(solver.solve(target)["witness"], target)


@pytest.mark.parametrize("blocks", [[], [()], [(0,), (0,)], [(0,)], [(False,), (1,)]])
def test_bad_block_partition_rejected(blocks):
    with pytest.raises(ValueError):
        BlockRepair(5, [[1, 1]], blocks)


def test_missing_local_direction_is_not_unsat():
    solver = BlockRepair(5, [[1, 0]], [(0,), (1,)])
    result = solver.solve([1])
    assert result["witness"] is None
    assert not result["infeasibility_established"]
    assert solver.fiber.verifies([1, 1], [1])


def test_no_guarantee_outside_field_cutoff():
    solver = BlockRepair(3, [[1, 1, 1]], [(0, 1, 2)])
    assert solver.fiber.verifies([1, 1, 1], [0])
    assert solver.solve([0])["status"] == "UNKNOWN_NO_BLOCK_CERTIFICATE"
    assert "block length is not smaller than the field" in solver.issues


@pytest.mark.parametrize("p", [3, 5, 7, 11])
def test_frozen_state_has_full_rank_kernel_basis_and_other_solution(p):
    control = frozen_basis(p)
    m, v = control["m"], control["v"]
    directions = [[(v[i]+int(i == j)-int(i == m-1)) % p for i in range(m)]
                  for j in range(m-1)]
    assert nmod_mat(directions, p).rank() == m-1
    assert all(sum(row) % p == 0 for row in directions)
    assert control["kernel_basis_determinant"] == 1
    for j, row in enumerate(directions):
        for t in range(1, p):
            index = frozen_zero_coordinate(p, j, t)
            assert (1+t*row[index]) % p == 0
    other = [1]*m
    if p == 3:
        other[:3] = [2]*3
    else:
        other[:2] = [3, p-1]
    assert all(other) and sum(other) % p == control["syndrome"]
    assert other != list(control["state"])
    assert not control["native_AG_instance"]


def test_frozen_native_prime_compressed_certificate():
    control = frozen_basis(1019)
    assert control["m"] == 2037 and control["kernel_basis_determinant"] == 1
    for j in range(control["m"]-1):
        for t in (1, 2, 509, 1018):
            index = frozen_zero_coordinate(1019, j, t)
            assert index != j and index != control["m"]-1
            assert (1+t*control["v"][index]) % 1019 == 0


@pytest.mark.parametrize("p", [3, 5, 7])
def test_pairwise_independence_does_not_give_empty_lll_graph(p):
    omega = [(a, b, (-a-b) % p) for a, b in product(range(p), repeat=2)]
    assert sum(x[0] == 0 for x in omega)*p == len(omega)
    assert sum(x[0] == x[1] == 0 for x in omega)*p*p == len(omega)
    conditioned = [x for x in omega if x[1] and x[2]]
    assert Fraction(sum(x[0] == 0 for x in conditioned), len(conditioned)) == Fraction(1, p-1)


def test_exact_affine_line_resampling_oracle():
    p, s, direction = 5, 1, (1, -1, 0)
    omega = [(a, b, (s-a-b) % p) for a, b in product(range(p), repeat=2)]
    event = [x for x in omega if x[0] == 0]
    outputs = Counter(tuple((x[i]+t*direction[i]) % p for i in range(3))
                      for x in event for t in range(p))
    assert set(outputs) == set(omega) and set(outputs.values()) == {1}
    assert all((x[2]+t*direction[2]) % p == x[2] for x in event for t in range(p))
    assert any(x[1] and (x[1]+t*direction[1]) % p == 0 for x in event for t in range(p))


@pytest.mark.parametrize("p,m", [(3, 3), (5, 5), (7, 4)])
def test_exact_counts_and_pair_overlap(p, m):
    for s in range(p):
        omega = [a+((s-sum(a)) % p,) for a in product(range(p), repeat=m-1)]
        valid = [a for a in omega if all(a)]
        hit = stationary_hitting(p, 1, m, m)
        mass = Fraction(len(valid), len(omega))
        assert mass <= hit["full_support_mass_upper"]
        assert hit["first_hit_expectation_lower"] >= hit["simpler_expectation_lower"]
        overlap = pair_overlap(p, 1, m, m, 2)["conditional_overlap_upper"]
        for t in range(1, p):
            count = sum((x[0]+t) % p != 0 and (x[1]-t) % p != 0 for x in valid)
            assert Fraction(count, len(valid)) <= overlap


@pytest.mark.parametrize("e", [8, 16, 32, 64, 128])
def test_source_probability_transfer_and_claim_scope(e):
    result = prime_source_locality(e)
    assert result["prime_count_condition"]
    assert 0 < result["unconditioned_prime_bad_upper"] <= result["good_cube_prime_bad_upper"] < 1
    assert result["one_degree_ratio_upper_for_unconditioned_bound"] < Fraction(1, 10000)
    assert not result["applies_to_handpicked_11I_minus_E"]
    assert not result["native_higher_input_generated"]
    assert not result["general_classical_lower_bound"]
    assert result["excluded_move_weight"] == 2*e


def test_fixed_bank_bound_is_not_search_lower_bound():
    result = fixed_bank_isolation(16384, 17*16384-3)
    assert result["nonisolated_fraction_upper"] < Fraction(6, 1000000)
    assert not result["first_hit_lower_bound"]
    assert not result["applies_to_state_adaptive_direction_selection"]


@pytest.mark.parametrize("params", [(4, 1, 3, 3), (5, 4, 3, 1), (5, 2, 3, 3), (5, True, 3, 1)])
def test_invalid_bounds_rejected(params):
    with pytest.raises(ValueError):
        stationary_hitting(*params)


def test_stationary_hitting_does_not_claim_adaptive_repair_bound():
    result = stationary_hitting(1019, 43, 176, 93)
    assert result["requires_uniform_initial_state_and_uniform_time_marginals"]
    assert not result["applies_to_adaptive_focused_repair"]
    assert not result["distance_verified_by_helper"]


def test_first_hit_bound_for_exact_stationary_walk_not_independent_samples():
    p = 3
    omega = [(a, b, (-a-b) % p) for a, b in product(range(p), repeat=2)]
    valid = {x for x in omega if all(x)}
    mass = Fraction(len(valid), len(omega))
    directions = ((1, -1, 0), (1, 0, -1))
    law = {x: Fraction(1, len(omega)) for x in omega}
    unhit = law.copy()
    hit = Fraction(0)
    for time in range(8):
        assert set(law.values()) == {Fraction(1, len(omega))}
        hit += sum(unhit.pop(x, 0) for x in valid)
        assert hit <= min(Fraction(1), (time+1)*mass)
        next_law, next_unhit = Counter(), Counter()
        for current, following in ((law, next_law), (unhit, next_unhit)):
            for x, probability in current.items():
                for v in directions:
                    for t in range(p):
                        y = tuple((a+t*b) % p for a, b in zip(x, v))
                        following[y] += probability/Fraction(p*len(directions))
        law, unhit = dict(next_law), dict(next_unhit)
    assert hit > mass


def test_source_conditioning_uses_probability_under_prime_law():
    result = prime_source_locality(8)
    assert result["good_cube_prime_bad_upper"] == (
        result["uniform_class_bad_upper"]*result["prime_class_max_mass_transfer"]
        /(1-result["cube_rejection_bound"]))
    assert result["good_cube_prime_special_11I_minus_effective_upper"] < result["good_cube_prime_bad_upper"]

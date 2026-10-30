from dataclasses import replace
from fractions import Fraction as F
from itertools import combinations
from math import comb
import random

import pytest
from flint import fmpz_mod_ctx, fmpz_mod_mat

import exterior_sde as sde


LARGE = 2**128 - 275


def labels(setup, seed=305):
    rng = random.Random(seed)
    return [tuple(rng.randrange(setup.prime) for _ in range(setup.width))
            for _ in range(setup.required_columns)]


def stats():
    return dict(exterior_nodes=0, contraction_checks=0,
                represented_node_checks=0, maximum_dependence_dimension=0)


def test_exact_bank_sizes():
    assert sde.collision_arity(2, 3) == 16
    assert sde.collision_arity(3, 3) == 112
    assert sde.collision_arity(4, 2) == 441
    assert sde.collision_arity(5, 2) == 9477
    assert sde.plan(LARGE, 4, 1).required_columns == 4096
    assert sde.plan(13, 4, 1).required_columns == 262144


@pytest.mark.parametrize("p,degree,width", [
    (7, 3, 1), (13, 3, 2), (43, 3, 3), (17, 4, 1), (41, 4, 2),
    (11, 5, 1), (101, 5, 2), (13, 9, 2), (17, 6, 2), (11, 8, 2),
    (2**127-295, 4, 3), (LARGE, 5, 2),
])
def test_verified_original_moments(p, degree, width):
    setup = sde.plan(p, degree, width)
    columns = labels(setup)
    witness = sde.solve(columns, setup, rng=random.Random(819))
    sde.verify_witness(p, degree, columns, witness.weights)
    ctx = fmpz_mod_ctx(p)
    matrix = fmpz_mod_mat(list(map(list, zip(*columns))), ctx)
    powers = fmpz_mod_mat([[pow(s, degree, p)] for s in witness.weights], ctx)
    residual = matrix * powers
    assert all(int(residual[j, 0]) == 0 for j in range(width))
    assert witness.statistics["exterior_nodes"] == witness.statistics["contraction_checks"]
    assert witness.statistics["exterior_nodes"] == witness.statistics["represented_node_checks"]
    assert witness.acquired_columns == setup.required_columns
    assert not witness.root_runtime_locally_clocked


@pytest.mark.parametrize("p,mode", [(13, "degree_bounded_accumulation"),
                                    (LARGE, "ternary_accumulation")])
def test_every_accumulation_round_is_reached(p, mode):
    setup = sde.plan(p, 4, 1)
    columns = [(1,)] * setup.required_columns
    witness = sde.solve(columns, setup, rng=random.Random(305))
    assert setup.mode == mode
    assert not witness.statistics["zero_representation_early_exit"]
    assert witness.statistics["exterior_nodes"] == (178923 if p == 13 else 2795)
    assert witness.statistics["enumerated_field_elements"] == (13 if p == 13 else 0)
    sde.verify_witness(p, 4, columns, witness.weights)


def test_even_degree_cannot_absorb_minus_sign_without_a_root():
    context = sde.PowerClasses(13, 4, random.Random(5), 128)
    columns = [(1,)] * sde.collision_arity(4, 1)
    collision = sde.exterior_collision(columns, context, stats())
    assert any(collision.value) and collision.negative
    wrong = [0] * len(columns)
    for i, root in collision.positive.items():
        wrong[i] = root
    for i, root in collision.negative.items():
        wrong[i] = -root % 13
    with pytest.raises(ArithmeticError):
        sde.verify_witness(13, 4, columns, wrong)
    with pytest.raises(ValueError):
        context.root(12)


@pytest.mark.parametrize("d,p", [(2, 5), (3, 7), (4, 17), (5, 11), (6, 13)])
def test_contraction_kernel_dimension_and_projection_injectivity(d, p):
    context = sde.PowerClasses(p, d, random.Random(48), 128)
    for degree in range(1, d+1):
        keys = tuple(combinations(range(d), degree))
        targets = tuple(combinations(range(d), degree-1))
        matrix_columns = []
        for selected in keys:
            values = {key: (int(key == selected),) for key in keys}
            result = sde.contract(values, degree, context.representatives, p, 1)
            matrix_columns.append([result[key][0] for key in targets])
        rows = list(map(list, zip(*matrix_columns)))
        rank = fmpz_mod_mat(rows, fmpz_mod_ctx(p)).rref()[1]
        expected_nullity = comb(d-1, degree) if degree < d else 0
        assert len(keys) - rank == expected_nullity
        projection = [[int(key == selected) for key in keys]
                      for selected in combinations(range(d-1), degree)]
        augmented_rank = fmpz_mod_mat(rows + projection, fmpz_mod_ctx(p)).rref()[1]
        assert augmented_rank == len(keys)


def test_wedge_sign_is_observable_not_optional():
    # e_1 wedge e_0 = -e_0 wedge e_1; contraction must preserve that sign.
    reps = (1, 2, 4)
    correct = sde.contract({(0, 1): (6,)}, 2, reps, 7, 1)
    incorrect = sde.contract({(0, 1): (1,)}, 2, reps, 7, 1)
    assert correct[(0,)] == [2] and incorrect[(0,)] == [5]


def test_all_zero_labels_still_charge_the_complete_bank_and_suffix():
    setup = sde.plan(17, 4, 2)
    columns = [(0, 0)] * (setup.required_columns + 7)
    witness = sde.solve(columns, setup, rng=random.Random(3))
    assert witness.acquired_columns == len(columns)
    assert any(witness.weights)
    assert not any(witness.weights[setup.required_columns:])
    with pytest.raises(ValueError):
        sde.solve([(0, 0)], setup)


class Fixed:
    def __init__(self, value):
        self.value = value

    def randrange(self, *args):
        return self.value


def test_generator_abort_is_not_a_fallback_enumeration():
    with pytest.raises(RuntimeError, match="generator cap"):
        sde.PowerClasses(17, 4, Fixed(1), 3)


def test_ternary_abort_has_no_enumeration_fallback():
    context = sde.PowerClasses(LARGE, 4, random.Random(3), 128)
    context.rng = Fixed(0)
    with pytest.raises(RuntimeError, match="Fermat sampling"):
        sde.scalar_row(context, "ternary_accumulation", 3)
    with pytest.raises(ValueError, match="degree bound"):
        sde.scalar_row(context, "degree_bounded_accumulation", 3)


def test_public_scalar_row_check():
    context = sde.PowerClasses(LARGE, 4, random.Random(3), 128)
    row, _, failure, enumerated = sde.scalar_row(context, "ternary_accumulation", 128)
    assert row[0] == 1 and sum(pow(x, 4, LARGE) for x in row) % LARGE == 0
    assert failure == F(7, 8)**128 and enumerated == 0


def test_faulty_roots_cannot_pass_node_checks(monkeypatch):
    original = sde.PowerClasses.classify

    def corrupted(self, value):
        index, root = original(self, value)
        return index, (root + 1) % self.p or 1

    monkeypatch.setattr(sde.PowerClasses, "classify", corrupted)
    setup = sde.plan(41, 4, 2)
    with pytest.raises(ArithmeticError):
        sde.solve(labels(setup), setup, rng=random.Random(3))


def test_faulty_scalar_row_is_rejected(monkeypatch):
    monkeypatch.setattr(sde, "scalar_row", lambda *args: ((0, 0, 0), 0, F(0), 0))
    setup = sde.plan(LARGE, 4, 1)
    with pytest.raises(ArithmeticError, match="scalar combining"):
        sde.solve([(1,)] * setup.required_columns, setup)


def test_forged_plan_cannot_reduce_source_bill():
    setup = sde.plan(17, 4, 1)
    with pytest.raises(ValueError, match="pre-acquisition"):
        sde.solve(labels(setup), replace(setup, required_columns=1))


@pytest.mark.parametrize("bad", [15, 2, True])
def test_invalid_prime(bad):
    with pytest.raises(ValueError):
        sde.plan(bad, 2, 1)


@pytest.mark.parametrize("bad", [0, 17, 1.5, True])
def test_invalid_degree(bad):
    with pytest.raises(ValueError):
        sde.plan(17, bad, 1)


@pytest.mark.parametrize("bad", [0, -1, True])
def test_invalid_width(bad):
    with pytest.raises(ValueError):
        sde.plan(17, 4, bad)


def test_canonical_input_contract():
    setup = sde.plan(7, 3, 1)
    for bad in ([(True,)]*12, [(7,)]*12, [(-1,)]*12, [(1, 2)]*12):
        with pytest.raises(ValueError):
            sde.solve(bad, setup)
    with pytest.raises(ValueError):
        sde.verify_witness(7, 3, [(1,)]*12, (0,)*12)


def test_rng_range_is_checked():
    with pytest.raises(ValueError, match="noncanonical"):
        sde.PowerClasses(17, 4, Fixed(17), 3)


@pytest.mark.parametrize("p,d", [(13, 4), (29, 4), (13, 6), (17, 8), (19, 6)])
def test_degree_bounded_scalar_row_without_existence_oracle(p, d):
    context = sde.PowerClasses(p, d, random.Random(52), 128)
    row, trials, bound, enumerated = sde.scalar_row(context, "degree_bounded_accumulation", 128)
    assert 1 <= len(row) <= d+1 and row[0] == 1
    assert sum(pow(s, d, p) for s in row) % p == 0
    assert enumerated == p and trials == 0 and bound == 0


@pytest.mark.parametrize("seed", range(8))
def test_general_index_collision_with_adversarial_repeated_columns(seed):
    p, d, width = 101, 5, 2
    context = sde.PowerClasses(p, d, random.Random(seed), 128)
    count = sde.collision_arity(d, width)
    columns = [(i % p, (3*i + 1) % p) for i in range(count)]
    random.Random(seed).shuffle(columns)
    collision = sde.exterior_collision(columns, context, stats())
    assert collision.positive and not collision.positive.keys() & collision.negative.keys()
    for j in range(width):
        positive = sum(columns[i][j] * pow(s, d, p) for i, s in collision.positive.items()) % p
        negative = sum(columns[i][j] * pow(s, d, p) for i, s in collision.negative.items()) % p
        assert positive == negative == collision.value[j]


def test_public_plan_is_label_independent_and_bijective_case_is_linear():
    setup = sde.plan(11, 3, 4)
    assert setup.index == 1 and setup.required_columns == 5
    columns = [tuple(int(i == j) for j in range(4)) for i in range(5)]
    witness = sde.solve(columns, setup, rng=random.Random(3))
    assert witness.weights[-1] != 0
    assert witness.statistics["power_class_draws"] == 0


def test_scalar_row_too_long_is_rejected_before_truncation(monkeypatch):
    setup = sde.plan(LARGE, 4, 1)
    monkeypatch.setattr(sde, "scalar_row", lambda *args: ((1,)*5, 0, F(0), 0))
    with pytest.raises(ArithmeticError, match="scalar combining"):
        sde.solve([(1,)]*setup.required_columns, setup, rng=random.Random(3))

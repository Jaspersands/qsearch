from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from systematic import SystematicFiber, distance_bound


CASES = [
    (3, [[1, 1, 1, 1]]),
    (3, [[1, 0, 1, 2], [0, 1, 1, 1]]),
    (5, [[1, 2, 4]]),
    (3, [[1, 0, 0]]),
    (3, [[1, 0], [0, 1]]),
    (3, [[0, 1, 1, 2], [1, 0, 2, 2]]),
]


@pytest.mark.parametrize("p,rows", CASES)
def test_every_syndrome_exact_probability_and_uniform_output(p, rows):
    fiber = SystematicFiber(p, rows, relation="full_support")
    native = Counter()
    for word in product(range(1, p), repeat=fiber.m):
        target = tuple(sum(a*b for a, b in zip(row, word)) % p for row in rows)
        native[target] += 1
    delta = min(sum(bool(sum(a*rows[i][j] for i, a in enumerate(coeffs)) % p)
                    for j in range(fiber.m))
                for coeffs in product(range(p), repeat=fiber.k) if any(coeffs))
    bound = distance_bound(p, fiber.m, fiber.k, delta)
    for target in product(range(p), repeat=fiber.k):
        accepted = Counter()
        for values in product(range(1, p), repeat=len(fiber.free)):
            word = tuple(fiber.from_free(target, values))
            assert all(sum(a*b for a, b in zip(row, word)) % p == s
                       for row, s in zip(rows, target))
            if all(word):
                assert fiber.verifies(word, target)
                accepted[word] += 1
        assert len(accepted) == native[target]
        assert all(multiplicity == 1 for multiplicity in accepted.values())
        systematic = Fraction(native[target], (p-1)**(fiber.m-fiber.k))
        affine = Fraction(native[target], p**(fiber.m-fiber.k))
        assert systematic == affine*bound["exact_success_ratio_if_nonempty"]
        correction = systematic/Fraction(p-1, p)**fiber.k - 1
        assert abs(correction) <= bound["tail_upper"]
        assert systematic >= bound["systematic_success_lower"]


def test_empty_fiber_and_false_distance_promise_are_not_certified_by_sampling():
    fiber = SystematicFiber(3, [[1, 0, 0]], relation="full_support")
    false = distance_bound(3, 3, 1, 3)
    assert false["systematic_success_lower"] > 0
    assert false["distance_verified_by_helper"] is False
    result = fiber.sample([0], seed=27, attempts=7)
    assert result["status"] == "UNKNOWN_ATTEMPT_CAP"
    assert result["hardness_evidence"] is False
    assert result["field_draws"] == 14


def test_square_matrix_and_nonidentity_pivots():
    fiber = SystematicFiber(5, [[1, 2], [3, 4]], relation="full_support")
    result = fiber.sample([3, 2], seed=27)
    assert result["witness"] == [1, 1]
    assert result["field_draws"] == 0
    assert fiber.sample([0, 0], seed=27, attempts=1)["witness"] is None


def test_seeded_replay_and_native_verification():
    fiber = SystematicFiber(3, [[1, 1, 1, 1]], relation="full_support")
    for syndrome in range(3):
        result = fiber.sample([syndrome], seed=20261027)
        assert result == fiber.sample([syndrome], seed=20261027)
        assert fiber.verifies(result["witness"], [syndrome])
        assert result["seeded_replay_is_not_distributional_evidence"] is True


@pytest.mark.parametrize("args", [(2, 4, 1, 4), (9, 4, 1, 4),
                                  (3, 4, 5, 2), (3, 4, 1, 5),
                                  (3, 0, 0, 0), (3, 4, True, 2)])
def test_invalid_bound_inputs(args):
    with pytest.raises(ValueError):
        distance_bound(*args)


def test_nonzero_free_contract():
    fiber = SystematicFiber(3, [[1, 1]], relation="full_support")
    for values in ([0], [3], [1, 2]):
        with pytest.raises(ValueError):
            fiber.from_free([1], values)
    with pytest.raises(ValueError):
        fiber.sample([1], seed=27, attempts=0)
    with pytest.raises(ValueError):
        SystematicFiber(3, [[1, 1]], relation="oracle")


@pytest.mark.parametrize("e", [8, 16, 32, 64])
def test_tower_tail_bound(e):
    p = 100003
    bound = distance_bound(p, 22*e, 5*e+3, 12*e-3)
    assert bound["tail_upper"] < Fraction(1, p**(e-5))
    assert bound["systematic_success_lower"] > 0
    assert bound["systematic_success_lower"] > bound["affine_success_lower"]

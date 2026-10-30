"""Exact controller regressions; scripted bits do not certify fair randomness."""

from collections import deque
from fractions import Fraction
from math import gcd
import random

from flint import fq_default_ctx, fq_default_poly_ctx
import pytest

from theorems import invariant_gram_selector as selector
from theorems.power_sde_budget import RandomnessExhausted


def _zero_controller(p, **kwargs):
    arity = 13 + gcd(3, p - 1)
    kwargs.setdefault("bit_source", random.Random(33))
    return selector.FiliformGramController(p, (0,) * arity, (0,) * arity,
                                          **kwargs)


def _pairing(gram, x, y, p):
    return sum(x[i] * gram[i][j] * y[j]
               for i in range(len(gram)) for j in range(len(gram))) % p


@pytest.mark.parametrize("p", (5, 7, (1 << 127) - 1))
@pytest.mark.parametrize("rank", range(8))
@pytest.mark.parametrize("last", (1, 2))
def test_witt_complements_preserve_rank_and_mixed_radicals(p, rank, last):
    size = 7
    change = tuple(tuple(int(i == j) if j <= i else (i + 2 * j + 1) % p
                         for j in range(size)) for i in range(size))
    diagonal = tuple((last if i == rank - 1 else 1) if i < rank else 0
                     for i in range(size))
    gram = tuple(tuple(sum(diagonal[k] * change[k][i] * change[k][j]
                           for k in range(size)) % p
                       for j in range(size)) for i in range(size))
    assert len(selector._basis(gram, p)) == rank

    controller = _zero_controller(p)
    space = controller._totally_isotropic(gram, 3)
    assert len(space) == len(selector._basis(space, p)) == 3
    assert all(_pairing(gram, x, y, p) == 0 for x in space for y in space)
    assert controller.conic_calls <= 3
    assert controller.root_calls <= 3


@pytest.mark.parametrize("p", (5, 7, (1 << 127) - 1))
@pytest.mark.parametrize("gram,rank", (
    (((0, 1, 0), (1, 0, 0), (0, 0, 0)), 2),
    (((0, 1, 1), (1, 0, 1), (1, 1, 0)), 3),
    (((1, 1, 0), (1, 1, 0), (0, 0, 0)), 1),
    (((0, 1, 2), (1, 0, 3), (2, 3, 0)), 3),
))
def test_off_diagonal_forms_are_diagonalized_and_selected_exactly(p, gram, rank):
    diagonal = selector._diagonalize(gram, p)
    vectors = [v for _, v in diagonal]
    assert len(diagonal) == len(selector._basis(vectors, p)) == 3
    assert sum(coefficient != 0 for coefficient, _ in diagonal) == rank
    for i, (coefficient, x) in enumerate(diagonal):
        for j, (_, y) in enumerate(diagonal):
            assert _pairing(gram, x, y, p) == (coefficient if i == j else 0)

    witness = _zero_controller(p).select(gram)
    assert any(witness.coordinates) and any(witness.scales)
    assert _pairing(gram, witness.coordinates, witness.coordinates, p) == 0


class _ZeroBits:
    def getrandbits(self, width):
        return 0


@pytest.mark.parametrize("failure_bits", (1, 8))
def test_conic_exhaustion_consumes_one_shot_without_root_calls(failure_bits):
    controller = _zero_controller(7, failure_bits=failure_bits,
                                  bit_source=_ZeroBits())
    # At x=0 the conic y**2=-1 has no solution over F7.
    with pytest.raises(RandomnessExhausted, match="conic search exhausted"):
        controller.select(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    assert controller.root_calls == 0
    assert controller.conic_calls == 1
    assert controller.rng.calls == controller.rng.bit_draws == controller.attempt_cap
    assert controller.rng.random_bits == 3 * controller.attempt_cap

    calls = controller.rng.calls
    with pytest.raises(ValueError, match="only one Gram outcome"):
        controller.select(((0, 0, 0), (0, 0, 0), (0, 0, 0)))
    assert controller.rng.calls == calls


@pytest.mark.parametrize("failure_bits", (1, 2, 3, 8, 32, 128, 1024))
def test_failure_allocation_has_exact_uniform_and_bit_budgets(failure_bits):
    controller = _zero_controller(5, failure_bits=failure_bits)
    cap = 3 * (failure_bits + 6)
    calls = 50 * cap
    rejection = failure_bits + 2 + (calls - 1).bit_length()
    algebraic = 22 * Fraction(2, 3) ** cap
    integer = Fraction(calls, 2 ** rejection)
    target = Fraction(1, 2 ** failure_bits)

    assert controller.attempt_cap == cap
    assert controller.rng.call_cap == calls
    assert controller.rng.rejection_cap == rejection
    assert controller.abort_bound == algebraic + integer
    assert algebraic < Fraction(22, 64) * target
    assert integer <= target / 4
    assert controller.abort_bound < Fraction(19, 32) * target < target
    assert controller.rng.calls == controller.rng.random_bits == 0


class _ScriptedBits:
    def __init__(self):
        self.values = deque()

    def getrandbits(self, width):
        assert self.values, "unexpected random draw"
        value = self.values.popleft()
        assert type(value) is int and 0 <= value < 2 ** width
        return value


def _retain_all_but_last(p, roots):
    """Interpolate 1 on retained roots and 0 on the discarded root."""
    ring = fq_default_poly_ctx(fq_default_ctx(p, 1, fq_type="FMPZ_MOD",
                                            check_prime=False))
    polynomial, denominator = ring([1]), 1
    for root in roots[:-1]:
        polynomial *= ring([-root, 1])
        denominator = denominator * (roots[-1] - root) % p
    polynomial = ring([1]) - polynomial * pow(denominator, -1, p)
    return tuple(int(polynomial[i]) for i in range(len(roots)))


def test_actual_root_backend_reaches_exact_47k_draw_path(monkeypatch):
    bits = _ScriptedBits()
    original_root = selector.bounded_power_root
    root_calls = []

    def delayed_root(p, degree, value, *, rng, split_attempt_cap):
        assert p == 7 and degree in (2, 3)
        assert not bits.values
        roots = [x for x in range(1, p) if pow(x, degree, p) == value]
        assert len(roots) == degree
        # Every stage fails K-1 times, then retains exactly one fewer root.
        for remaining in range(degree, 1, -1):
            bits.values.extend([0] * (remaining * (split_attempt_cap - 1)))
            bits.values.extend(_retain_all_but_last(p, roots))
            roots = roots[:-1]
        result = original_root(p, degree, value, rng=rng,
                               split_attempt_cap=split_attempt_cap)
        assert not bits.values
        assert result.root == roots[0]
        assert result.proper_splits == degree - 1
        assert result.split_trials == (degree - 1) * split_attempt_cap
        assert result.random_field_elements == (
            split_attempt_cap * (degree * (degree + 1) // 2 - 1))
        root_calls.append((degree, result))
        return result

    class DelayedConics(selector.FiliformGramController):
        def _isotropic(self, gram):
            diagonal = selector._diagonalize(gram, self.prime)
            if all(coefficient for coefficient, _ in diagonal):
                (a, _), (b, _), (c, _) = diagonal[:3]
                p = self.prime
                squares = [(-c - a * x * x) * pow(b, -1, p) % p
                           for x in range(p)]
                bad = next(x for x, y in enumerate(squares)
                           if y and pow(y, (p - 1) // 2, p) != 1)
                good = next(x for x, y in enumerate(squares)
                            if y and pow(y, (p - 1) // 2, p) == 1)
                assert not bits.values
                bits.values.extend([bad] * (self.attempt_cap - 1) + [good])
            return super()._isotropic(gram)

    monkeypatch.setattr(selector, "bounded_power_root", delayed_root)
    controller = DelayedConics(7, (1,) * 16, (1,) * 16,
                               failure_bits=1, bit_source=bits)
    gram = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    witness = controller.select(gram)
    cap = controller.attempt_cap

    assert not bits.values
    assert controller.root_calls == len(root_calls) == 11
    assert [degree for degree, _ in root_calls].count(3) == 7
    assert [degree for degree, _ in root_calls].count(2) == 4
    assert controller.conic_calls == 4
    assert sum(result.random_field_elements for _, result in root_calls) == 43 * cap
    assert witness.uniform_calls == controller.rng.bit_draws == 47 * cap
    assert witness.uniform_calls < controller.rng.call_cap == 50 * cap
    assert witness.random_bits == 3 * witness.uniform_calls
    assert any(witness.scales)
    assert sum(s ** 3 for s in witness.scales) % 7 == 0
    assert sum(s ** 2 for s in witness.scales) % 7 == 0
    assert _pairing(gram, witness.coordinates, witness.coordinates, 7) == 0

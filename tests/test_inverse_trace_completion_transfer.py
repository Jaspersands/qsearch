"""Exact distribution controls for a conditional reduction, not a sampler.

The native-field histogram control enumerates the syndrome space. That is
exponential in nK and is confined to F16; no scalability claim follows.
"""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import prod

import pytest


def stats(prefix, residual, syndrome=0):
    """Count full fibers and the unconditioned uniform-completion law."""
    assert len(prefix) == len(residual)
    q = len(prefix)
    assert q > 0 and q & (q - 1) == 0
    a, b = sum(prefix), sum(residual)
    assert a > 0 and b > 0
    counts = [prefix[syndrome ^ h] for h in range(q)]
    f = [Fraction(q * x, a) for x in counts]
    g = [Fraction(q * x, b) for x in residual]
    full = sum(x * y for x, y in zip(counts, residual))
    vu = sum((x - 1) ** 2 for x in g) / q
    vt = sum((x - 1) ** 2 for x in f) / q
    c = Fraction(q * full, a * b)
    tv = None if not full else sum(
        abs(Fraction(x, a) - Fraction(x * y, full))
        for x, y in zip(counts, residual)
    ) / 2
    abort = sum(Fraction(x, a) for x, y in zip(counts, residual) if not y)
    return f, g, c, vu, vt, tv, abort


def le_sqrt_sum(value, a, b):
    """Compare value <= sqrt(a)+sqrt(b) without floating point."""
    assert a >= 0 and b >= 0
    if value <= 0:
        return True
    remainder = value * value - a - b
    return remainder <= 0 or remainder * remainder <= 4 * a * b


def verify_transfer(prefix, residual, syndrome=0):
    f, g, c, vu, vt, tv, abort = stats(prefix, residual, syndrome)
    q = len(prefix)
    assert (c - 1) ** 2 <= vu * vt
    if vu * vt < 1:
        assert c > 0
    if c == 0:
        assert tv is None
        return
    assert tv == sum(x * abs(1 - y / c) for x, y in zip(f, g)) / (2 * q)
    assert le_sqrt_sum(tv, vu / 4, vu * vt)
    assert abort <= tv


def test_exhaustive_histograms_no_independence_or_positive_fiber_assumption():
    histograms = [x for x in product(range(3), repeat=4) if sum(x)]
    for prefix in histograms:
        for residual in histograms:
            for syndrome in range(4):
                verify_transfer(prefix, residual, syndrome)


@pytest.mark.parametrize("copies", [2, 3, 7, 19])
def test_deterministic_witness_does_not_supply_the_sampling_contract(copies):
    # Equal completion counts make the prefix transfer exact, but selecting
    # one completion per syndrome still loses most of the target mass.
    prefix, residual = (1, 1), (copies, copies)
    assert stats(prefix, residual)[5] == 0
    actual = {(h, 0): Fraction(1, 2) for h in range(2)}
    target = {(h, j): Fraction(1, 2 * copies)
              for h in range(2) for j in range(copies)}
    tv = sum(abs(actual.get(x, 0) - target[x]) for x in target) / 2
    assert tv == 1 - Fraction(1, copies)


def test_empty_fiber_abort_is_not_silently_conditioned_away():
    *_, tv, abort = stats((1, 1), (2, 0))
    assert tv == abort == Fraction(1, 2)
    actual = {"abort": Fraction(1, 2), "a": Fraction(1, 4), "b": Fraction(1, 4)}
    target = {"abort": 0, "a": Fraction(1, 2), "b": Fraction(1, 2)}
    assert sum(abs(actual[x] - target[x]) for x in actual) / 2 == tv
    conditioned = {x: actual[x] / (1 - abort) for x in ("a", "b")}
    assert conditioned == {x: target[x] for x in ("a", "b")}


def test_disjoint_support_does_not_create_a_normalized_target():
    f, g, c, vu, vt, tv, abort = stats((1, 0), (0, 1))
    assert c == 0 and tv is None and abort == 1
    assert vu * vt == 1
    assert sum(f) == sum(g) == 2


@pytest.mark.parametrize("prefix", [(1, 1, 1, 1), (1, 2, 0, 3), (0, 1, 2, 0)])
@pytest.mark.parametrize("residual", [(1, 2, 3, 4), (0, 0, 2, 1), (3, 0, 0, 2)])
def test_output_level_identity_and_approximate_kernel_composition(prefix, residual):
    exact, noisy, target = Counter(), Counter(), Counter()
    errors = (Fraction(1, 3), Fraction(0), Fraction(1, 7), Fraction(1))
    full = sum(x * y for x, y in zip(prefix, residual))
    if not full:
        _, _, c, _, _, tv, abort = stats(prefix, residual)
        assert c == 0 and tv is None and abort == 1
        return
    for h, count in enumerate(prefix):
        for prefix_id in range(count):
            if not residual[h]:
                exact["abort"] += Fraction(1, sum(prefix))
                noisy["abort"] += Fraction(1, sum(prefix))
                continue
            noisy["abort"] += errors[h] / sum(prefix)
            for completion_id in range(residual[h]):
                output = (h, prefix_id, completion_id)
                mass = Fraction(1, sum(prefix) * residual[h])
                exact[output] += mass
                noisy[output] += mass * (1 - errors[h])
                target[output] += Fraction(1, full)
    assert sum(exact.values()) == sum(noisy.values()) == sum(target.values()) == 1
    support = exact.keys() | noisy.keys() | target.keys()
    tv = sum(abs(exact[x] - target[x]) for x in support) / 2
    actual_error = sum(abs(noisy[x] - target[x]) for x in support) / 2
    f, _, _, _, vt, predicted, _ = stats(prefix, residual)
    assert tv == predicted
    # Empty-fiber kernels already output ABORT, so their error is zero.
    effective = [e if count else 0 for e, count in zip(errors, residual)]
    induced = sum(x * e for x, e in zip(f, effective)) / 4
    average = sum(effective) / 4
    assert actual_error <= tv + induced
    assert le_sqrt_sum(actual_error - tv - average, vt / 4, 0)


def test_prefix_adaptive_bad_kernel_is_not_a_fixed_kernel_guarantee():
    f, _, _, _, vt, _, _ = stats((1, 1), (1, 1))
    assert vt == 0
    # Each fixed kernel fails on one of two uniform syndromes. Choosing
    # that kernel after seeing h makes every actual call fail instead.
    errors = ((1, 0), (0, 1))
    assert all(Fraction(sum(row), 2) == Fraction(1, 2) for row in errors)
    adaptive = sum(f[h] * errors[h][h] for h in range(2)) / 2
    assert adaptive == 1


@pytest.mark.parametrize("syndrome", range(4))
def test_affine_syndrome_changes_the_tilt(syndrome):
    prefix, residual = (1, 2, 4, 8), (0, 1, 3, 7)
    verify_transfer(prefix, residual, syndrome)
    c = stats(prefix, residual, syndrome)[2]
    expected = Fraction(4 * sum(prefix[syndrome ^ h] * residual[h] for h in range(4)),
                        sum(prefix) * sum(residual))
    assert c == expected
    if syndrome:
        assert c != stats(prefix, residual, 0)[2]


def test_average_kernel_error_requires_prefix_distribution_payment():
    prefix = (1, 0, 0, 0)
    f, _, _, _, vt, _, _ = stats(prefix, (1, 1, 1, 1))
    errors = (1, 0, 0, 0)
    uniform_error = Fraction(sum(errors), 4)
    induced_error = sum(x * e for x, e in zip(f, errors)) / 4
    assert uniform_error == Fraction(1, 4)
    assert induced_error == 1
    assert le_sqrt_sum(induced_error - uniform_error, vt / 4, 0)


def test_error_transfer_for_all_bounded_kernels_and_histograms():
    for prefix in product(range(3), repeat=4):
        if not sum(prefix):
            continue
        f, _, _, _, vt, _, _ = stats(prefix, (1, 1, 1, 1))
        for errors in product((Fraction(0), Fraction(1, 3), Fraction(1)), repeat=4):
            average = sum(errors) / 4
            induced = sum(x * e for x, e in zip(f, errors)) / 4
            assert le_sqrt_sum(induced - average, vt / 4, 0)


def multiply(a, b):
    # F16 = F2[z]/(z^4+z+1), used only for independent bounded identities.
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 16:
            a ^= 0b10011
    return out


def inverse(a):
    if not a:
        return 0
    result = 1
    for _ in range(14):
        result = multiply(result, a)
    assert multiply(a, result) == 1
    return result


def trace(a):
    result = 0
    for _ in range(4):
        result ^= a
        a = multiply(a, a)
    assert result in (0, 1)
    return result


def histogram(points, targets):
    # Native n=4, N=16, K=2: encode (sum x, sum alpha*x) as two nibbles.
    counts = Counter({0: 1})
    for point, bit in zip(points, targets):
        accepted = [x for x in range(16) if trace(inverse(x)) == bit]
        assert len(accepted) == 8
        contributions = [x | multiply(point, x) << 4 for x in accepted]
        updated = Counter()
        for old, weight in counts.items():
            for add in contributions:
                updated[old ^ add] += weight
        counts = updated
    assert sum(counts.values()) == 8 ** len(points)
    return tuple(counts.get(h, 0) for h in range(256))


@pytest.mark.parametrize("targets", [(0,) * 16, (1,) * 16, (0, 1) * 8,
                                     tuple(i.bit_count() % 2 for i in range(16))])
@pytest.mark.parametrize("syndrome", [0, 19, 255])
def test_native_inverse_trace_histograms(targets, syndrome):
    # U has K+ceil(4K/n)=4 positions. The counts are not planted witnesses.
    residual = histogram(range(4), targets[:4])
    prefix = histogram(range(4, 16), targets[4:])
    verify_transfer(prefix, residual, syndrome)
    f, g, c, vu, vt, tv, _ = stats(prefix, residual, syndrome)
    assert c > 0
    assert vu <= Fraction(9 ** 4, 16 ** 2)
    assert vt <= Fraction(9 ** 12, 16 ** 10)
    assert sum(f) == sum(g) == 256
    assert tv is not None and 0 <= tv <= 1


@pytest.mark.parametrize("n", [17, 31, 61])
def test_native_asymptotic_bound_parameters_not_sampler_executions(n):
    size, checks = n * n, n * n // 8
    slack = (4 * checks + n - 1) // n
    m, ell = checks + slack, size - checks - slack
    vu = Fraction(9 ** m, 1 << (n * (m - checks)))
    vt = Fraction(9 ** ell, 1 << (n * (ell - checks)))
    assert prod((vu, vt)) < 1
    # The exact-kernel transfer error is below 1/32 in these three regimes.
    # Compare sqrt(vu)/2+sqrt(vu*vt) < 1/32 using exact rational arithmetic.
    bound = Fraction(1, 32)
    remainder = bound * bound - vu / 4 - vu * vt
    assert remainder > 0 and remainder * remainder > vu * vu * vt

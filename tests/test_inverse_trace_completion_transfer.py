"""Exact distribution controls for a conditional reduction, not a sampler.

The native-field histogram control enumerates the syndrome space. That is
exponential in nK and is confined to F16; no scalability claim follows.
"""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, isqrt, prod

import pytest

from theorems.inverse_trace_gibbs_target import residual_variance_bound


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


@pytest.mark.parametrize("targets", [(0,) * 16, (1,) * 16, (0, 1) * 8,
                                     tuple(i.bit_count() % 2 for i in range(16))])
@pytest.mark.parametrize("length", [3, 4])
def test_support_bound_transfer_for_every_native_f16_syndrome(targets, length):
    residual = histogram(range(length), targets[:length])
    prefix = histogram(range(length, 16), targets[length:])
    bu = residual_variance_bound(4, length, 2)
    bt = residual_variance_bound(4, 16-length, 2)
    expected_vu = {3: Fraction(1, 4), 4: Fraction(53, 2048)}[length]
    expected_vt = {3: Fraction(16777217, 562949953421312),
                   4: Fraction(4194305, 35184372088832)}[length]
    assert bu*bt < 1
    for syndrome in range(256):
        f, g, c, vu, vt, tv, abort = stats(prefix, residual, syndrome)
        assert vu == expected_vu <= bu
        assert vt == expected_vt <= bt
        assert (c-1)**2 <= vu*vt and c > 0
        assert tv == sum(x*abs(1-y/c) for x, y in zip(f, g))/512
        assert le_sqrt_sum(tv, bu/4, bu*bt)
        assert abort <= tv
    if length == 3:
        assert any(count == 0 for count in residual)
    else:
        assert all(residual)


def binary_field_reference(bits):
    """Independent, table-sized arithmetic for exhaustive F4/F8/F16 controls."""
    modulus = {2: 0b111, 3: 0b1011, 4: 0b10011}[bits]
    q = 1 << bits

    def mul(a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
            if a & q:
                a ^= modulus
        return out

    def tr(a):
        out = 0
        for _ in range(bits):
            out ^= a
            a = mul(a, a)
        assert out in (0, 1)
        return out

    inverses = [0]+[next(y for y in range(1, q) if mul(x, y) == 1)
                    for x in range(1, q)]
    return mul, tr, [tr(x) for x in inverses]


@pytest.mark.parametrize("bits,length,checks", [(2, 3, 1), (3, 4, 2), (4, 4, 1)])
def test_support_sensitive_variance_all_targets_syndromes_and_fourier_supports(bits, length, checks):
    q = 1 << bits
    mul, tr, predicate = binary_field_reference(bits)
    powers = [[1] for _ in range(length)]
    for point, row in enumerate(powers):
        for _ in range(checks-1):
            row.append(mul(row[-1], point))
    columns = [[sum(mul(x, a) << (bits*k) for k, a in enumerate(row))
                for x in range(q)] for row in powers]
    counts = [[0]*(q**checks) for _ in range(1 << length)]
    for word in product(range(q), repeat=length):
        syndrome = target = 0
        for i, x in enumerate(word):
            syndrome ^= columns[i][x]
            target |= predicate[x] << i
        counts[target][syndrome] += 1
    spectra = []
    for bit in (0, 1):
        roots = [x for x in range(q) if predicate[x] == bit]
        assert len(roots) == q//2
        r = [Fraction(sum(1-2*tr(mul(u, x)) for x in roots), q//2)
             for u in range(q)]
        assert r[0] == 1 and sum(x*x for x in r[1:]) == 1
        spectra.append([x*x for x in r])
    assert spectra[0] == spectra[1]
    root = isqrt(q)
    root += int(root*root < q)
    beta = min(Fraction(1), Fraction(1+2*root, q))
    assert max(spectra[0][1:]) <= beta*beta
    support_sums = Counter()
    for coefficients in product(range(q), repeat=checks):
        if not any(coefficients):
            continue
        values = []
        for row in powers:
            value = 0
            for a, c in zip(row, coefficients):
                value ^= mul(a, c)
            values.append(value)
        support = tuple(i for i, value in enumerate(values) if value)
        assert len(support)-(length-checks) > 0
        support_sums[support] += prod(spectra[0][value] for value in values)
    assert all(value <= beta**(2*(length-checks)) for value in support_sums.values())
    bound = residual_variance_bound(bits, length, checks)
    mean = Fraction((q//2)**length, q**checks)
    for row in counts:
        assert sum(row) == (q//2)**length
        variance = sum((Fraction(c)/mean-1)**2 for c in row)/(q**checks)
        assert variance == sum(support_sums.values()) <= bound


def power_two(exponent):
    return Fraction(1 << exponent) if exponent >= 0 else Fraction(1, 1 << -exponent)


def assert_transfer_upper(bound, vu, vt):
    # Pay the prefix-distribution term with an outward integer-square-root bound.
    exponent = vt.numerator.bit_length()-vt.denominator.bit_length()
    step = power_two(exponent//2-80)
    scaled = vt/(4*step*step)
    root = isqrt(scaled.numerator//scaled.denominator)
    if root*root*scaled.denominator < scaled.numerator:
        root += 1
    prefix = root*step
    assert prefix*prefix >= vt/4
    assert (prefix-step)**2 < vt/4
    remaining = bound-prefix
    assert remaining >= 0
    remainder = remaining*remaining-vu/4-vu*vt
    assert remainder >= 0 and remainder*remainder >= vu*vu*vt


@pytest.mark.parametrize("bits,length,vu_m,vu_e,vt_m,vt_e,t_m,t_e", [
    (17, 40, 1032751, -20, 1725834, -3051, 1016244, -11),
    (17, 45, 1075167, -90, 1551312, -2977, 1036903, -46),
    (31, 126, 1000143, -48, 1905417, -20247, 1000072, -25),
    (31, 136, 1000380, -328, 1627453, -19959, 1000190, -165),
    (61, 477, 1000001, -231, 1397227, -162046, 1414214, -117),
    (61, 496, 1000001, -1333, 1181580, -160929, 1414214, -668),
])
def test_outward_rational_support_variance_and_transfer_budgets(
        bits, length, vu_m, vu_e, vt_m, vt_e, t_m, t_e):
    size, checks = bits*bits, bits*bits//8
    assert length in (checks+(3*checks+2*bits-1)//(2*bits),
                      checks+(4*checks+bits-1)//bits)
    vu = residual_variance_bound(bits, length, checks)
    vt = residual_variance_bound(bits, size-length, checks)
    assert vu*vt < 1
    for value, mantissa, exponent in ((vu, vu_m, vu_e), (vt, vt_m, vt_e)):
        unit = power_two(exponent)/10**6
        assert (mantissa-1)*unit < value <= mantissa*unit
    assert_transfer_upper(Fraction(t_m, 10**6)*power_two(t_e), vu, vt)


@pytest.mark.parametrize("bits,mantissa,exponent", [
    (17, 1769465, -7), (31, 1469067, -34), (61, 1559843, -161),
])
def test_original_residual_forecasts_remain_separate(bits, mantissa, exponent):
    size, checks = bits*bits, bits*bits//8
    length = checks+(4*checks+bits-1)//bits
    vu = Fraction(9**length, 1 << (bits*(length-checks)))
    vt = Fraction(9**(size-length), 1 << (bits*(size-length-checks)))
    assert_transfer_upper(Fraction(mantissa, 10**6)*power_two(exponent), vu, vt)


@pytest.mark.parametrize("bits,length,checks", [(2, 3, 1), (4, 3, 2), (5, 4, 3),
                                               (6, 5, 4), (17, 40, 36)])
def test_exact_minimum_formula_retains_vacuous_variance(bits, length, checks):
    q = 1 << bits
    root = isqrt(q)
    root += int(root*root < q)
    beta = min(Fraction(1), Fraction(1+2*root, q))
    support = sum(comb(length, w) for w in range(length-checks+1, length+1))
    expected = min(Fraction(9**length, q**(length-checks)),
                   support*beta**(2*(length-checks)))
    actual = residual_variance_bound(bits, length, checks)
    assert isinstance(actual, Fraction) and actual == expected
    if bits in (4, 5, 6):
        assert actual > 1
        prefix = residual_variance_bound(bits, bits*bits-length, checks)
        assert actual*prefix < 1
        assert_transfer_upper(Fraction(1), actual, prefix)


def test_variance_bound_is_not_a_pointwise_syndrome_bound():
    counts = histogram(range(3), (0,)*3)
    mean = Fraction(sum(counts), 256)
    squared_errors = [(Fraction(c)/mean-1)**2 for c in counts]
    bound = residual_variance_bound(4, 3, 2)
    assert sum(squared_errors)/256 <= bound < max(squared_errors)


@pytest.mark.parametrize("args", [(1, 3, 1), (129, 3, 1), (True, 3, 1),
                                  (4.0, 3, 1), (4, 17, 1), (4, 1, 1),
                                  (4, 3, 0), (4, 3, 3), (4, 3, 4),
                                  (4, 3, True), (4, 3, 1.0)])
def test_residual_variance_parameter_guards(args):
    with pytest.raises(ValueError):
        residual_variance_bound(*args)

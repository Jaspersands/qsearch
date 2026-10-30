"""Bounded exact controls, not a general proof, PIP backend, or hardness claim.

Pairs represent a + b*s in Q(s), s**2 = 2.  The compact evaluator uses only
the ramified prime (s): modulus 2**m means precision (s)**(2*m).  Separate
fixed controls cover conductor 5 and lattice division at (7, s-3).
"""

from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd

import pytest
from sympy import Matrix, eye
from sympy.matrices.normalforms import hermite_normal_form


MAX_PRECISION = 1024
MAX_INPUT_BITS = 2048
MAX_EXPONENT_BITS = 2048
MAX_BINARY_STEPS = 4096
MAX_FACTORS = 16
MAX_LOCAL_STEPS = 32


@dataclass
class Audit:
    max_bits: int = 0
    modular_bits: int = 0
    binary_steps: int = 0
    multiplications: int = 0
    normalization_steps: int = 0
    normalized_factors: int = 0
    modulus_allocations: int = 0
    valuation: int | None = None
    denominator_inversions: list = field(default_factory=list)
    unit_inversions: list = field(default_factory=list)

    def observe(self, *values, modular=False):
        bits = max((value.bit_length() for value in values), default=0)
        self.max_bits = max(self.max_bits, bits)
        if modular:
            self.modular_bits = max(self.modular_bits, bits)


def _checked_pair(pair, audit):
    if len(pair) != 2:
        raise ValueError("expected a coefficient pair")
    for value in pair:
        if not isinstance(value, (int, Fraction)):
            raise TypeError("only int/Fraction coefficients")
        if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_INPUT_BITS:
            raise ValueError("coefficient resource cap")
        audit.observe(value.numerator, value.denominator)
    return tuple(Fraction(value) for value in pair)


def _v2(nonzero):
    if not nonzero:
        raise ValueError("v2(0) is not finite")
    return (nonzero & -nonzero).bit_length() - 1


def _valuation(pair, audit):
    a, b = pair
    # Inputs were capped before constructing this common denominator.
    denominator = a.denominator // gcd(a.denominator, b.denominator) * b.denominator
    aa = a.numerator * (denominator // a.denominator)
    bb = b.numerator * (denominator // b.denominator)
    audit.observe(denominator, aa, bb)
    if not (aa or bb):
        raise ValueError("zero is not a powerproduct factor")
    candidates = ([2 * _v2(aa)] if aa else []) + ([2 * _v2(bb) + 1] if bb else [])
    return min(candidates) - 2 * _v2(denominator)


def _local_unit(pair, valuation, audit):
    if abs(valuation) > MAX_LOCAL_STEPS:
        raise ValueError("local normalization resource cap")
    a, b = pair
    for _ in range(abs(valuation)):
        # Division by s is (a,b) -> (b,a/2), including even denominators.
        a, b = (b, a / 2) if valuation > 0 else (2 * b, a)
        audit.normalization_steps += 1
        audit.observe(a.numerator, a.denominator, b.numerator, b.denominator)
    assert _valuation((a, b), audit) == 0
    assert a.denominator % 2 == b.denominator % 2 == 1
    audit.normalized_factors += 1
    return a, b


def _unit_residue(pair, modulus, audit):
    if any(value.denominator % 2 == 0 for value in pair):
        raise ValueError("even denominator must be normalized before inversion")
    residue = []
    for value in pair:
        audit.denominator_inversions.append(value.denominator)
        inverse = pow(value.denominator, -1, modulus)
        numerator = value.numerator * inverse
        audit.observe(inverse, numerator)
        residue.append(numerator % modulus)
    assert residue[0] % 2 == 1
    return tuple(residue)


def _mul_mod(left, right, modulus, audit):
    a, b = left
    c, d = right
    assert all(0 <= x < modulus for x in (a, b, c, d))
    ac, bd, ad, bc = a * c, b * d, a * d, b * c
    real, radical = ac + 2 * bd, ad + bc
    audit.observe(ac, bd, 2 * bd, ad, bc, real, radical, modular=True)
    audit.multiplications += 1
    return real % modulus, radical % modulus


def _inverse_unit(residue, modulus, audit):
    a, b = residue
    if a % 2 == 0:
        raise ValueError("cannot invert a nonunit residue")
    norm = a * a - 2 * b * b
    audit.unit_inversions.append(residue)
    inverse = pow(norm, -1, modulus)
    audit.observe(a * a, b * b, 2 * b * b, norm, inverse,
                  a * inverse, -b * inverse, modular=True)
    return a * inverse % modulus, -b * inverse % modulus


def _power_unit(base, exponent, modulus, audit):
    if exponent.bit_length() > MAX_EXPONENT_BITS:
        raise ValueError("exponent resource cap")
    if exponent < 0:
        base = _inverse_unit(base, modulus, audit)
    result, remaining = (1, 0), abs(exponent)
    while remaining:
        audit.binary_steps += 1
        if remaining & 1:
            result = _mul_mod(result, base, modulus, audit)
        remaining >>= 1
        if remaining:
            base = _mul_mod(base, base, modulus, audit)
    return result


def _compact_residue(terms, m, audit=None):
    """Consume bounded factors, never their expanded signed powerproduct."""
    audit = Audit() if audit is None else audit
    if not 1 <= m <= MAX_PRECISION:
        raise ValueError("precision resource cap")
    if len(terms) > MAX_FACTORS:
        raise ValueError("factor resource cap")
    if any(not isinstance(exponent, int) for _, exponent in terms):
        raise TypeError("integer exponents required")
    if any(exponent.bit_length() > MAX_EXPONENT_BITS for _, exponent in terms):
        raise ValueError("exponent resource cap")
    if sum(exponent.bit_length() for _, exponent in terms) > MAX_BINARY_STEPS:
        raise ValueError("binary work resource cap")
    checked = [(_checked_pair(pair, audit), exponent) for pair, exponent in terms]
    valued = [(pair, exponent, _valuation(pair, audit)) for pair, exponent in checked]
    total = 0
    for _, exponent, valuation in valued:
        contribution = exponent * valuation
        total += contribution
        audit.observe(exponent, contribution, total)
    audit.valuation = total
    # Neither denominator inversion nor exponentiation precedes cancellation.
    if total < 0:
        raise ValueError("negative total valuation")
    if total >= 2 * m:
        return (0, 0)
    if any(exponent and abs(valuation) > MAX_LOCAL_STEPS for _, exponent, valuation in valued):
        raise ValueError("local normalization resource cap")
    modulus = 1 << m
    audit.modulus_allocations += 1
    audit.observe(modulus)
    result = (1, 0)
    for pair, exponent, valuation in valued:
        if exponent:
            unit = _local_unit(pair, valuation, audit)
            residue = _unit_residue(unit, modulus, audit)
            result = _mul_mod(result, _power_unit(residue, exponent, modulus, audit), modulus, audit)
    # Here total < 2*m, so even this residual uniformizer power is bounded.
    a, b = result
    shift = total // 2
    raw = (b << (shift + 1), a << shift) if total % 2 else (a << shift, b << shift)
    audit.observe(*raw, modular=True)
    return tuple(value % modulus for value in raw)


def _mul_exact(left, right):
    a, b = left
    c, d = right
    return a * c + 2 * b * d, a * d + b * c


def _epsilon_recurrence(exponent):
    """Independent expansion oracle, deliberately restricted to small powers."""
    if abs(exponent) > 24:
        raise ValueError("recurrence resource cap")
    a, b = 1, 0
    for _ in range(abs(exponent)):
        a, b = (a + 2 * b, a + b) if exponent > 0 else (-a + 2 * b, a - b)
    assert max(a.bit_length(), b.bit_length()) <= 2 * abs(exponent) + 1
    return a, b


def _columns(*pairs):
    return Matrix.hstack(*(Matrix(pair) for pair in pairs))


def _hnf(matrix):
    # Matrix inversion can retain domain QQ even when all entries are integers.
    assert all(value.q == 1 for value in matrix)
    integral = Matrix(matrix.rows, matrix.cols, [int(value) for value in matrix])
    return hermite_normal_form(integral)


# Each ratio is epsilon; the last three have even rational denominators.
CANCELLING_FACTORS = (
    ((2, 2), (2, 0)),
    ((2, 1), (0, 1)),
    ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 2), 0)),
    ((1, Fraction(1, 2)), (0, Fraction(1, 2))),
    ((Fraction(1, 6), Fraction(1, 6)), (Fraction(1, 6), 0)),
)


def test_ramified_valuation_matches_integral_local_division_and_denominators():
    for a in range(-8, 9):
        for b in range(-8, 9):
            if not (a or b):
                continue
            aa, bb, divisions = a, b, 0
            while aa % 2 == 0:
                assert divisions < MAX_LOCAL_STEPS
                aa, bb = bb, aa // 2
                divisions += 1
            audit = Audit()
            assert _valuation(_checked_pair((a, b), audit), audit) == divisions
            for denominator in (2, 4, 6, 10):
                pair = _checked_pair((Fraction(a, denominator), Fraction(b, denominator)), audit)
                valuation = _valuation(pair, audit)
                assert valuation == divisions - 2 * _v2(denominator)
                unit = _local_unit(pair, valuation, audit)
                assert unit[0].numerator % 2 == 1
                restored = unit
                for _ in range(abs(valuation)):
                    restored = _mul_exact(restored, (0, 1) if valuation > 0 else (0, Fraction(1, 2)))
                assert restored == pair


@pytest.mark.parametrize("factors", CANCELLING_FACTORS)
def test_small_signed_products_match_independent_recurrence(factors):
    for exponent in range(-24, 25):
        audit = Audit()
        actual = _compact_residue(((factors[0], exponent), (factors[1], -exponent)), 7, audit)
        assert actual == tuple(value % 128 for value in _epsilon_recurrence(exponent))
        assert audit.valuation == 0
        assert audit.binary_steps == 2 * exponent.bit_length()


@pytest.mark.parametrize("m", (1, 2, 7, 16))
def test_distinct_rational_denominators_survive_local_cancellation(m):
    factors = ((Fraction(1, 6), Fraction(1, 10)), (Fraction(1, 2), 0))
    modulus = 1 << m
    for sign in (-1, 1):
        audit = Audit()
        a, b = _compact_residue(((factors[0], sign), (factors[1], -sign)), m, audit)
        # The quotient is 1/3+s/5; its inverse is (75-45*s)/7.
        if sign > 0:
            assert 3 * a % modulus == 1 and 5 * b % modulus == 1
        else:
            assert 7 * a % modulus == 75 % modulus
            assert 7 * b % modulus == -45 % modulus
        assert audit.valuation == 0 and audit.normalization_steps == 4
        assert audit.binary_steps == 2 and len(audit.unit_inversions) == 1
        assert 3 in audit.denominator_inversions and 5 in audit.denominator_inversions


@pytest.mark.parametrize("factors", CANCELLING_FACTORS)
@pytest.mark.parametrize("m", (2, 7, 16, 128))
def test_huge_cancelling_nonunits_are_consumed_without_expansion(factors, m):
    for small_tail in (0, 7, -7):
        exponent = (1 << 128) + small_tail
        for sign in (-1, 1):
            audit = Audit()
            terms = ((factors[0], sign * exponent), (factors[1], -sign * exponent))
            actual = _compact_residue(terms, m, audit)
            # epsilon**(2**m) == 1 mod 2**m; expand only the tiny tail.
            expected = tuple(value % (1 << m) for value in _epsilon_recurrence(sign * small_tail))
            assert actual == expected
            assert audit.valuation == 0
            assert audit.binary_steps == 2 * exponent.bit_length()
            assert audit.normalized_factors == 2
            assert audit.normalization_steps <= 4
            assert len(audit.unit_inversions) == 1
            assert all(a % 2 for a, _ in audit.unit_inversions)
            assert len(audit.denominator_inversions) == 4
            assert all(d % 2 for d in audit.denominator_inversions)
            assert audit.modular_bits <= 2 * m + 2
            assert audit.max_bits <= max(2 * m + 2, exponent.bit_length() + 3)
            assert audit.multiplications <= 4 * exponent.bit_length() + 2


@pytest.mark.parametrize("m", (2, 5, 9))
def test_positive_valuation_and_precision_boundary(m):
    exponent = 1 << 128
    for valuation in range(2 * m + 2):
        audit = Audit()
        terms = (((2, 0), -exponent), ((2, 2), exponent), ((0, 1), valuation))
        actual = _compact_residue(terms, m, audit)
        assert audit.valuation == valuation
        if valuation >= 2 * m:
            assert actual == (0, 0)
            assert audit.binary_steps == audit.modulus_allocations == audit.normalized_factors == 0
            assert not audit.unit_inversions and not audit.denominator_inversions
        else:
            power = 1 << (valuation // 2)
            assert actual == ((0, power) if valuation % 2 else (power, 0))
            assert audit.binary_steps == 2 * exponent.bit_length() + valuation.bit_length()
    assert _compact_residue((((0, 1), -1), ((2, 0), 1)), m) == (0, 1)
    audit = Audit()
    assert _compact_residue((((0, 1), exponent),), m, audit) == (0, 0)
    assert audit.valuation == exponent
    assert audit.binary_steps == audit.modulus_allocations == audit.normalized_factors == 0
    assert not audit.unit_inversions and not audit.denominator_inversions


def test_invalid_nonunits_are_never_inverted_before_cancellation():
    exponent = 1 << 128
    for terms in ((((0, 1), -1),), (((2, 0), -exponent), ((2, 2), exponent - 1))):
        audit = Audit()
        with pytest.raises(ValueError, match="negative total valuation"):
            _compact_residue(terms, 7, audit)
        assert audit.binary_steps == audit.modulus_allocations == audit.normalized_factors == 0
        assert not audit.unit_inversions and not audit.denominator_inversions
    audit = Audit()
    for residue in ((2, 0), (0, 1), (0, 0)):
        with pytest.raises(ValueError, match="nonunit"):
            _inverse_unit(residue, 128, audit)
    with pytest.raises(ValueError, match="even denominator"):
        _unit_residue((Fraction(1, 2), Fraction(1, 2)), 128, audit)
    assert not audit.unit_inversions and not audit.denominator_inversions


def test_resource_caps_precede_modulus_allocation_and_exponentiation():
    unit = ((1, 1), 1)
    too_many_bits = 1 << MAX_INPUT_BITS
    high_valuation = (1 << (MAX_LOCAL_STEPS // 2 + 1), 0)
    cases = (
        ((unit,), 0),
        ((unit,), MAX_PRECISION + 1),
        ((unit,) * (MAX_FACTORS + 1), 7),
        ((((1, 1), 1 << MAX_EXPONENT_BITS),), 7),
        ((((1, 1), 1 << (MAX_EXPONENT_BITS - 1)),) * 3, 7),
        ((((too_many_bits, 1), 1),), 7),
        ((((Fraction(1, too_many_bits), 1), 1),), 7),
        (((high_valuation, 1), (high_valuation, -1)), 7),
    )
    for terms, m in cases:
        audit = Audit()
        with pytest.raises(ValueError, match="resource cap"):
            _compact_residue(terms, m, audit)
        assert audit.modulus_allocations == audit.binary_steps == audit.normalized_factors == 0
        assert not audit.unit_inversions and not audit.denominator_inversions
    with pytest.raises(ValueError, match="recurrence resource cap"):
        _epsilon_recurrence(25)
    with pytest.raises(ValueError, match="zero"):
        _compact_residue((((0, 0), 1),), 7)
    assert _compact_residue((), 7) == (1, 0)


@pytest.mark.parametrize("m", (2, 3, 4, 6, 9, 16, 32))
def test_coprime_conductor_family_basis_extension_and_order_stability(m):
    f = 1 << m
    d = 1 - f * f // 2
    beta = (1, -f // 2)
    j_basis = ((2, f), (0, 2 * f))
    i_basis = ((d, 0), (-f * f, f))
    # d/(2+f*s) = beta/2, checked in Q(s) before applying it to J.
    multiplier = (Fraction(1, 2), Fraction(-f, 4))
    assert _mul_exact(multiplier, j_basis[0]) == (d, 0)
    assert tuple(_mul_exact(multiplier, column) for column in j_basis) == i_basis
    assert tuple(2 * value for value in multiplier) == beta
    extension = _columns(*i_basis, *(_mul_exact((0, 1), column) for column in i_basis))
    beta_o = _columns(beta, _mul_exact((0, 1), beta))
    assert _hnf(extension) == _hnf(beta_o)
    assert beta_o.det() == d and d % 2 == 1 and gcd(d, f) == 1
    basis = _columns(*i_basis)
    r_basis = Matrix.diag(1, f)
    in_r = r_basis.inv() * basis
    assert all(value.q == 1 for value in in_r)
    assert abs(in_r.det()) == abs(d)
    action = basis.inv() * _columns(*(_mul_exact((0, f), column) for column in i_basis))
    assert action == Matrix([[f * f, 2 * f * f], [d, -f * f]])
    assert all(value.q == 1 for value in action)
    # I' + f*O = R, in R coordinates, not merely after extending to O.
    conductor = _columns((f, 0), (0, f))
    assert _hnf(in_r.row_join(r_basis.inv() * conductor)) == eye(2)


@pytest.mark.parametrize("m", (2, 3, 4, 5))
def test_small_compact_generator_generates_the_exact_r_ideal(m):
    f = 1 << m
    d = 1 - f * f // 2
    generator = _mul_exact((1, -f // 2), _epsilon_recurrence(f // 2))
    assert generator[0] % 2 == 1 and generator[1] % f == 0
    generated_r_ideal = _columns(generator, _mul_exact((0, f), generator))
    assert _hnf(generated_r_ideal) == _hnf(_columns((d, 0), (-f * f, f)))


@pytest.mark.parametrize("m", (2, 3, 4, 5, 6))
def test_conductor_condition_iff_in_bounded_positive_and_negative_ranges(m):
    f = 1 << m
    for exponent in range(-2 * f, 2 * f + 1):
        audit = Audit()
        a, b = _compact_residue((((1, -f // 2), 1), ((1, 1), exponent)), m, audit)
        assert a % 2 == 1
        assert (b == 0) == (exponent % f == f // 2)
        assert audit.binary_steps == 1 + exponent.bit_length()


@pytest.mark.parametrize("m", (32, 128, 512, 1024))
def test_large_conductor_condition_without_expanding_the_generator(m):
    f = 1 << m
    for multiple in (-(1 << 128), -1, 0, 1, 1 << 128):
        for offset in (-1, 0, 1, f // 2 - 1, f // 2):
            exponent = f // 2 + multiple * f + offset
            audit = Audit()
            a, b = _compact_residue((((1, -f // 2), 1), ((1, 1), exponent)), m, audit)
            assert a % 2 == 1
            assert (b == 0) == (exponent % f == f // 2)
            assert audit.valuation == 0
            assert audit.binary_steps == 1 + exponent.bit_length()
            assert audit.modular_bits <= 2 * m + 2
            assert audit.max_bits <= max(2 * m + 2, exponent.bit_length())
            assert audit.multiplications <= 2 * exponent.bit_length() + 3


def test_conductor_five_matched_nonprincipal_ideal_control():
    r_basis = Matrix.diag(1, 5)
    i_basis = ((2, 0), (0, 5))
    basis = _columns(*i_basis)
    in_r = r_basis.inv() * basis
    assert in_r.det() == 2
    action = basis.inv() * _columns(*(_mul_exact((0, 5), column) for column in i_basis))
    assert action == Matrix([[0, 25], [2, 0]])
    extension = _columns(*i_basis, *(_mul_exact((0, 1), column) for column in i_basis))
    assert _hnf(extension) == _hnf(_columns((0, 1), (2, 0)))
    conductor = r_basis.inv() * _columns((5, 0), (0, 5))
    assert _hnf(in_r.row_join(conductor)) == eye(2)
    square = _columns(*(
        _mul_exact(left, right) for left in i_basis for right in i_basis
    ))
    assert _hnf(square) == 2 * r_basis  # I**2 = 2*R certifies invertibility.
    # A principal I has |Norm(a+5*b*s)| = [R:I] = 2, impossible mod 5.
    squares = {a * a % 5 for a in range(5)}
    assert squares == {0, 1, 4}
    assert squares.isdisjoint({2, -2 % 5})

    # This fixed field has 24 units; this is not a generic local/DLog solver.
    def multiply5(left, right):
        a, b = left
        c, d = right
        return (a * c + 2 * b * d) % 5, (a * d + b * c) % 5

    units = {(a, b) for a in range(5) for b in range(5) if (a, b) != (0, 0)}
    assert len(units) == 24
    assert all((a * a - 2 * b * b) % 5 != 0 for a, b in units)
    powers, power = [], (1, 0)
    for _ in range(24):
        powers.append(power)
        power = multiply5(power, (1, 1))
        if power == (1, 0):
            break
    assert power == (1, 0) and len(powers) == len(set(powers)) == 12
    assert powers[3] == (2, 0)
    scalars = {(a, 0) for a in range(1, 5)}
    gamma = {multiply5(power, scalar) for power in powers for scalar in scalars}
    assert gamma == set(powers) and len(gamma) == 12
    beta = (0, 1)
    assert beta in units and beta not in gamma
    beta_gamma = {multiply5(beta, unit) for unit in gamma}
    assert gamma.isdisjoint(beta_gamma) and gamma | beta_gamma == units
    assert all(multiply5(beta, power) not in scalars for power in powers)


@pytest.mark.parametrize("a", range(1, 7))
def test_split_seven_local_unit_division_needs_one_extra_digit(a):
    # Cap before constructing powers, roots, or lattices; never enumerate O/p**a.
    if not 1 <= a <= 6:
        raise ValueError("split-seven precision resource cap")
    audit = Audit()
    roots, moduli = [3], [7]
    prime = _hnf(Matrix([[7, -3], [0, 1]]))
    ideals = [prime]
    for _ in range(a):
        root, modulus = roots[-1], moduli[-1]
        defect = root * root - 2
        assert defect % modulus == 0
        correction = -(defect // modulus) * pow(2 * root, -1, 7)
        digit = correction % 7
        lifted, next_modulus = root + digit * modulus, 7 * modulus
        audit.observe(root * root, defect, correction, digit * modulus, lifted, next_modulus)
        assert 0 <= lifted < next_modulus and lifted % modulus == root
        assert lifted * lifted % next_modulus == 2
        audit.observe(lifted * lifted)
        next_ideal = _hnf(Matrix([[next_modulus, -lifted], [0, 1]]))
        product = _columns(*(
            _mul_exact(tuple(ideals[-1].col(i)), tuple(prime.col(j)))
            for i in range(2) for j in range(2)
        ))
        assert _hnf(product) == next_ideal
        assert next_ideal.det() == next_modulus
        assert all((x + lifted * y) % next_modulus == 0 for x, y in (
            tuple(next_ideal.col(i)) for i in range(2)
        ))
        roots.append(lifted)
        moduli.append(next_modulus)
        ideals.append(next_ideal)
    assert len(roots) == len(moduli) == len(ideals) == a + 1 <= 7
    assert moduli[-1] <= 7**7 and audit.max_bits <= 40

    r_a, r_next = roots[-2:]
    modulus, next_modulus = moduli[-2:]
    p_a, p_next = ideals[-2:]
    u = (Fraction(3, 7), Fraction(-1, 7))
    assert all(coefficient.denominator == 7 for coefficient in u)
    assert _mul_exact(u, (3, 1)) == (1, 0)
    assert gcd(3 + r_a, 7) == 1
    with pytest.raises(ValueError):
        pow(7, -1, modulus)
    assert (3 - r_next) % 7 == 0
    residue = ((3 - r_next) // 7) % modulus
    assert residue == pow(3 + r_a, -1, modulus)
    assert residue % 7 == 6  # A local unit despite its nonintegral coefficients.
    assert _hnf((7 * eye(2)).row_join(p_next)) == prime

    # In 7*x = B*z, B's bottom row forces z_2 = 7*t; its first
    # diagonal entry is divisible by 7, so this gives the entire kernel.
    assert tuple(p_next.row(1)) == (0, 1)
    kernel = _hnf(p_next * Matrix.diag(1, 7) / 7)
    assert kernel == p_a
    assert all(value.q == 1 for value in p_next.inv() * (7 * kernel))
    # Multiplication by 7 in Z/7**(a+1) has image of size 7**a.
    assert kernel.det() == next_modulus // gcd(7, next_modulus) == modulus

    root_lifts = [r_a + digit * modulus for digit in range(7)]
    assert all(root * root % modulus == 2 for root in root_lifts)
    assert [root for root in root_lifts if root * root % next_modulus == 2] == [r_next]
    candidates = {((3 - root) // 7) % modulus for root in root_lifts}
    assert candidates == {
        ((3 - r_a) // 7 + digit * (modulus // 7)) % modulus for digit in range(7)
    }
    assert len(candidates) == 7
    assert all((7 * value - (3 - r_a)) % modulus == 0 for value in candidates)
    assert {value for value in candidates if (7 * value - (3 - r_next)) % next_modulus == 0} == {residue}

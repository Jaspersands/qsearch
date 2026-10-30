from collections import Counter
from dataclasses import FrozenInstanceError, is_dataclass
from fractions import Fraction
from itertools import product
import random

from flint import fq_default_ctx, fq_default_poly_ctx
import pytest

from theorems import bounded_power_roots as solver


class ScriptedRandom:
    def __init__(self, p, values):
        self.p = p
        self.values = iter(values)
        self.calls = 0

    def randrange(self, start, stop):
        assert (start, stop) == (0, self.p)
        self.calls += 1
        return next(self.values)


class ConstantRandom:
    def __init__(self, value):
        self.value = value
        self.calls = 0

    def randrange(self, start, stop):
        assert start == 0
        self.calls += 1
        return self.value


class CountingRandom:
    def __init__(self, p, seed):
        self.p = p
        self.source = random.Random(seed)
        self.calls = 0

    def randrange(self, start, stop):
        assert (start, stop) == (0, self.p)
        self.calls += 1
        return self.source.randrange(start, stop)


def _ring(p):
    return fq_default_poly_ctx(fq_default_ctx(p, 1, fq_type="FMPZ_MOD", check_prime=False))


def _selector(p, roots, selected):
    """Test-only interpolation: evaluations are 1 on selected roots, 0 elsewhere."""
    ring = _ring(p)
    h = ring([0])
    for root in selected:
        basis, denominator = ring([1]), 1
        for other in roots:
            if other != root:
                basis *= ring([-other, 1])
                denominator = denominator*(root-other) % p
        h += basis*pow(denominator, -1, p)
    return [int(h[i]) for i in range(len(roots))]


def _check_counts(result, rng, d, cap):
    assert result.random_field_elements == rng.calls
    assert 0 <= result.proper_splits <= d-1
    assert result.proper_splits <= result.split_trials <= (d-1)*cap
    assert 2*result.split_trials <= result.random_field_elements <= d*result.split_trials
    assert result.random_field_elements <= cap*(d*(d+1)//2-1)
    assert isinstance(result.abort_bound, Fraction)
    assert result.abort_bound == (d-1)*Fraction(2, 3)**cap


@pytest.mark.parametrize("p,d", ((2**128-275, 4), (2**61-1, 5), (2**61-1, 6)))
@pytest.mark.parametrize("seed", (0, 20261028))
def test_large_field_roots_are_exact_with_reproducible_random_streams(p, d, seed):
    a = pow(123456789, d, p)
    rng = CountingRandom(p, seed)
    result = solver.bounded_power_root(p, d, a, rng=rng)
    assert type(result.root) is int and 0 < result.root < p
    assert pow(result.root, d, p) == a
    _check_counts(result, rng, d, 64)
    repeated = solver.bounded_power_root(p, d, a, rng=CountingRandom(p, seed))
    assert repeated == result


def test_large_quartic_control_rejects_minus_one_and_two_as_fourth_powers():
    p = 2**128-275
    assert p % 8 == 5
    assert pow(p-1, (p-1)//2, p) == 1  # -1 is a square, not a fourth power.
    for a in (p-1, 2):
        assert pow(a, (p-1)//4, p) != 1
        rng = ConstantRandom(0)
        with pytest.raises(ValueError, match="dth-power residue"):
            solver.bounded_power_root(p, 4, a, rng=rng)
        assert rng.calls == 0


@pytest.mark.parametrize("p", (3, 5, 7, 11, 13, 17, 19))
def test_every_small_admissible_degree_and_nonzero_residue(p):
    # Exhaustive field enumeration is confined to tests, never the primitive.
    for d in range(2, p):
        if (p-1) % d:
            continue
        roots_by_power = {}
        for root in range(1, p):
            roots_by_power.setdefault(pow(root, d, p), []).append(root)
        for a in range(1, p):
            assert (pow(a, (p-1)//d, p) == 1) == (a in roots_by_power)
            if a not in roots_by_power:
                rng = ConstantRandom(0)
                with pytest.raises(ValueError, match="dth-power residue"):
                    solver.bounded_power_root(p, d, a, rng=rng)
                assert rng.calls == 0
                continue
            roots = roots_by_power[a]
            assert len(roots) == d
            for root in roots:
                rng = ScriptedRandom(p, _selector(p, roots, [root]))
                result = solver.bounded_power_root(p, d, a, rng=rng, split_attempt_cap=1)
                assert result.root == root
                assert pow(result.root, d, p) == a
                assert (result.split_trials, result.proper_splits) == (1, 1)
                assert result.random_field_elements == d
                _check_counts(result, rng, d, 1)


@pytest.mark.parametrize("cap", (1, 3))
@pytest.mark.parametrize("abort_last", (False, True))
def test_worst_case_descent_reaches_exact_total_cap(cap, abort_last):
    p, d = 7, 6
    roots = list(range(1, p))
    stream = []
    for m in range(d, 1, -1):
        stream.extend([0]*(m*(cap-1)))
        stream.extend([0]*m if abort_last and m == 2 else _selector(p, roots, roots[:-1]))
        roots = roots[:-1]
    rng = ScriptedRandom(p, stream)
    result = solver.bounded_power_root(p, d, 1, rng=rng, split_attempt_cap=cap)
    assert result.root == (None if abort_last else 1)
    assert result.split_trials == (d-1)*cap
    assert result.proper_splits == d-1-int(abort_last)
    assert result.random_field_elements == cap*sum(range(2, d+1)) == len(stream)
    _check_counts(result, rng, d, cap)


@pytest.mark.parametrize("cap", (1, 4, 17))
def test_constant_zero_rng_exhausts_first_stage_without_retrying_forever(cap):
    rng = ConstantRandom(0)
    result = solver.bounded_power_root(13, 4, 3, rng=rng, split_attempt_cap=cap)
    assert result.root is None
    assert result.split_trials == cap
    assert result.proper_splits == 0
    assert result.random_field_elements == 4*cap
    _check_counts(result, rng, 4, cap)


def test_constant_polynomials_reject_both_trivial_gcds():
    # h=0 and h=3 give gcd=1; h=1 gives gcd=f over F_7.
    rng = ScriptedRandom(7, [0]*6 + [1]+[0]*5 + [3]+[0]*5)
    result = solver.bounded_power_root(7, 6, 1, rng=rng, split_attempt_cap=3)
    assert result.root is None
    assert (result.split_trials, result.proper_splits, result.random_field_elements) == (3, 0, 18)


@pytest.mark.parametrize("p,roots", ((3, (1, 2)), (5, (1, 4)), (5, (1, 2, 3)),
                                    (5, (1, 2, 3, 4)), (7, (1, 2, 4))))
def test_exact_split_probability_and_independent_evaluations(p, roots):
    ring = _ring(p)
    f = ring([1])
    for root in roots:
        f *= ring([-root, 1])
    m = len(roots)
    seen_evaluations = set()
    proper = 0
    for coefficients in product(range(p), repeat=m):
        values = tuple(sum(c*pow(root, i, p) for i, c in enumerate(coefficients)) % p
                       for root in roots)
        seen_evaluations.add(values)
        square_count = sum(pow(value, (p-1)//2, p) == 1 for value in values)
        candidate = f.gcd(ring(list(coefficients)).pow_mod((p-1)//2, f)-1)
        assert candidate.degree() == square_count
        proper += 0 < candidate.degree() < m
    assert len(seen_evaluations) == p**m  # The evaluation map is bijective.
    q = Fraction(p-1, 2*p)
    probability = Fraction(proper, p**m)
    assert probability == 1-q**m-(1-q)**m
    assert probability >= 2*q*(1-q) >= Fraction(4, 9) > Fraction(1, 3)
    if (p, m) == (3, 2):
        assert probability == Fraction(4, 9)


@pytest.mark.parametrize("p", (3, 5))
@pytest.mark.parametrize("cap", (1, 2))
def test_exact_abort_probability_over_all_quadratic_trial_streams(p, cap):
    outcomes = Counter()
    for stream in product(range(p), repeat=2*cap):
        rng = ScriptedRandom(p, stream)
        result = solver.bounded_power_root(p, 2, 1, rng=rng, split_attempt_cap=cap)
        outcomes[result.root] += 1
        _check_counts(result, rng, 2, cap)
    q = Fraction(p-1, 2*p)
    assert Fraction(outcomes[None], p**(2*cap)) == (q*q+(1-q)**2)**cap
    assert Fraction(outcomes[None], p**(2*cap)) <= Fraction(2, 3)**cap
    assert set(outcomes) == {None, 1, p-1}
    assert outcomes[1] == outcomes[p-1]


@pytest.mark.parametrize("parameter,bad", (
    ("p", True), ("p", 13.0), ("p", "13"), ("p", -13), ("p", 1), ("p", 2), ("p", 14),
    ("d", True), ("d", 4.0), ("d", -4), ("d", 0), ("d", 1), ("d", 5), ("d", 13),
    ("a", True), ("a", 3.0), ("a", -10), ("a", 0), ("a", 13), ("a", 16),
    ("split_attempt_cap", True), ("split_attempt_cap", 2.0),
    ("split_attempt_cap", -1), ("split_attempt_cap", 0),
))
def test_invalid_parameters_are_rejected_before_random_sampling(parameter, bad):
    rng = ConstantRandom(0)
    arguments = dict(p=13, d=4, a=3, rng=rng, split_attempt_cap=2)
    arguments[parameter] = bad
    with pytest.raises(ValueError):
        solver.bounded_power_root(**arguments)
    assert rng.calls == 0


@pytest.mark.parametrize("rng", (None, object(), 1, random.Random))
def test_missing_or_malformed_rng_is_rejected(rng):
    with pytest.raises((ValueError, TypeError)):
        solver.bounded_power_root(13, 4, 3, rng=rng)


def test_noncallable_rng_and_wrong_signature_are_rejected():
    class NoncallableRandom:
        randrange = 1

    class WrongSignatureRandom:
        def randrange(self, stop):
            return 0

    with pytest.raises(ValueError, match="callable randrange"):
        solver.bounded_power_root(13, 4, 3, rng=NoncallableRandom())
    with pytest.raises(TypeError):
        solver.bounded_power_root(13, 4, 3, rng=WrongSignatureRandom())


@pytest.mark.parametrize("bad", (True, False, -1, 13, 14, 0.0, "0", None, Fraction(1)))
def test_noncanonical_rng_output_is_rejected_immediately(bad):
    rng = ConstantRandom(bad)
    with pytest.raises(ValueError, match="rng returned a noncanonical"):
        solver.bounded_power_root(13, 4, 3, rng=rng)
    assert rng.calls == 1


def test_invalid_later_coefficient_and_rng_budget_exhaustion_do_not_retry():
    rng = ScriptedRandom(13, [0, 0, 13])
    with pytest.raises(ValueError, match="rng returned a noncanonical"):
        solver.bounded_power_root(13, 4, 3, rng=rng)
    assert rng.calls == 3

    class BudgetRandom:
        calls = 0

        def randrange(self, start, stop):
            self.calls += 1
            raise RuntimeError("external RNG bit budget exhausted")

    rng = BudgetRandom()
    with pytest.raises(RuntimeError, match="external RNG bit budget exhausted"):
        solver.bounded_power_root(13, 4, 3, rng=rng)
    assert rng.calls == 1


def test_backend_disables_primality_validation_and_uses_degree_one(monkeypatch):
    contexts = []

    def checked_context(p, degree, **kwargs):
        assert degree == 1
        assert kwargs == {"fq_type": "FMPZ_MOD", "check_prime": False}
        contexts.append(p)
        return fq_default_ctx(p, degree, **kwargs)

    monkeypatch.setattr(solver, "fq_default_ctx", checked_context)
    result = solver.bounded_power_root(7, 2, 1, rng=ScriptedRandom(7, [0, 1]),
                                       split_attempt_cap=1)
    assert result.root == 1
    assert contexts == [7]


def test_every_trial_uses_one_deterministic_pow_mod_and_gcd(monkeypatch):
    p, d, cap = 5, 4, 2
    roots = list(range(1, p))
    stream = []
    for m in range(d, 1, -1):
        stream.extend([0]*m + _selector(p, roots, roots[:-1]))
        roots = roots[:-1]
    calls = []

    # Deliberately expose no roots, factor, random-element, or primality API.
    class TracedPolynomial:
        def __init__(self, polynomial):
            self.polynomial = polynomial

        def degree(self):
            return self.polynomial.degree()

        def __getitem__(self, index):
            return self.polynomial[index]

        def __sub__(self, other):
            return TracedPolynomial(self.polynomial-other)

        def pow_mod(self, exponent, modulus):
            assert exponent == (p-1)//2
            calls.append(("pow_mod", modulus.degree()))
            return TracedPolynomial(self.polynomial.pow_mod(exponent, modulus.polynomial))

        def gcd(self, other):
            calls.append(("gcd", self.degree()))
            return TracedPolynomial(self.polynomial.gcd(other.polynomial))

    def traced_ring(field):
        ring = fq_default_poly_ctx(field)
        return lambda coefficients: TracedPolynomial(ring(coefficients))

    monkeypatch.setattr(solver, "fq_default_poly_ctx", traced_ring)
    rng = ScriptedRandom(p, stream)
    result = solver.bounded_power_root(p, d, 1, rng=rng, split_attempt_cap=cap)
    assert result.root == 1
    assert calls == [(operation, m) for m in (4, 4, 3, 3, 2, 2)
                     for operation in ("pow_mod", "gcd")]
    assert len(calls) == 2*result.split_trials
    _check_counts(result, rng, d, cap)


@pytest.mark.parametrize("bad_factor", ([0, 1], [-2, 1], [-1, 2]))
def test_faulty_backend_cannot_return_an_unverified_root(monkeypatch, bad_factor):
    ring = _ring(7)

    class BrokenPolynomial:
        def degree(self):
            return 2

        def pow_mod(self, exponent, modulus):
            return ring([0])

        def gcd(self, other):
            return ring(bad_factor)

    monkeypatch.setattr(solver, "fq_default_poly_ctx", lambda field: lambda c: BrokenPolynomial())
    with pytest.raises(ArithmeticError, match="invalid root|monic linear factor"):
        solver.bounded_power_root(7, 2, 1, rng=ConstantRandom(0), split_attempt_cap=1)


def test_result_is_a_frozen_dataclass_with_exact_unclipped_bound():
    result = solver.bounded_power_root(7, 6, 1, rng=ConstantRandom(0), split_attempt_cap=1)
    assert is_dataclass(result)
    assert result.abort_bound == Fraction(10, 3)
    with pytest.raises(FrozenInstanceError):
        result.root = 1

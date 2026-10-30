from fractions import Fraction
from math import comb

import pytest
from flint import fmpz_mat

from bridge_controls import (CyclotomicRing, evaluate_mod, exact_phase_fidelity,
                             fermat_null_polynomial, newton_dilation,
                             newton_dilation_matrix, parameters)


@pytest.mark.parametrize("p,t", [(2, 1), (2, 5), (3, 1), (3, 2), (5, 1), (5, 4), (127, 3)])
def test_scope_is_not_decided_by_nilpotence_alone(p, t):
    data = parameters(p, t, n=17)
    assert data["class"] == t*(p-1)
    assert data["class_less_than_p"] == (t == 1)
    assert data["q"] <= 2**data["class"]
    assert data["hidden_index_log_p"] == 17*data["class"]
    assert data["normalizer_order_log_p"] == 18
    assert not data["growing_modulus_fixed_class_bridge_established"]


@pytest.mark.parametrize("p,t,n", [(4, 2, 1), (True, 2, 1), (3, 0, 1), (3, 2, 0)])
def test_wrong_input_rejected(p, t, n):
    with pytest.raises(ValueError):
        parameters(p, t, n)


@pytest.mark.parametrize("p,t", [(2, 2), (2, 5), (3, 2), (3, 3), (5, 2), (7, 2)])
def test_all_scalar_evaluations_lose_nonzero_coefficients(p, t):
    coefficients = fermat_null_polynomial(p, t)
    q = p**t
    assert coefficients[1] != 0 and coefficients[p] != 0
    assert p <= parameters(p, t)["class"]
    assert all(evaluate_mod(coefficients, x, q) == 0 for x in range(q))


def test_null_polynomial_not_imported_at_exponent_one():
    with pytest.raises(ValueError):
        fermat_null_polynomial(3, 1)


@pytest.mark.parametrize("degree,scale", [(2, 2), (3, 2), (4, 2), (7, 3)])
def test_newton_dilation_as_exact_integer_identity(degree, scale):
    coefficients = newton_dilation(degree, scale)
    for t in range(2*degree+3):
        assert sum(a*comb(t, j) for j, a in enumerate(coefficients) if j <= t) == comb(scale*t, degree)
    assert coefficients[-1] == scale**degree


def test_binomial_evaluation_repairs_coefficient_separation():
    # Evaluation at 1,...,c for positive binomial degrees is unit triangular.
    for c in (3, 4, 8):
        assert all(comb(i, j) == 0 for i in range(1, c+1) for j in range(i+1, c+1))
        assert all(comb(i, i) == 1 for i in range(1, c+1))


@pytest.fixture(scope="module")
def ring():
    return CyclotomicRing(3, 2)


def test_ramification_and_exact_lower_central_sizes(ring):
    assert ring.power(ring.zeta, 3) == ring.one
    assert ring.lam(3) == ring.zero
    assert ring.power(ring.pi, 4) == ring.zero
    assert ring.power(ring.pi, 3) != ring.zero
    assert [len(ring.ideal(k)) for k in range(5)] == [81, 27, 9, 3, 1]
    rotation = (ring.zero, 1)
    for k in range(4):
        current = ring.ideal(k)
        next_ideal = {ring.commutator(rotation, (x, 0))[0] for x in current}
        assert next_ideal == ring.ideal(k+1)


def test_fermat_countercoefficients_obey_actual_filtration(ring):
    coefficients = fermat_null_polynomial(3, 2)
    assert ring.scalar(coefficients[3]) in ring.ideal(2)  # gamma_3
    assert ring.scalar(coefficients[1]) != ring.zero     # retained grade one
    assert ring.scalar(coefficients[1]) not in {x for x, j in ring.hidden(0) if j == 0}


def test_newton_repair_breaks_the_top_grade_dilation(ring):
    coefficients = newton_dilation(4, 2)
    assert coefficients == [0, 0, 1, 12, 16]
    central = ring.power(ring.pi, 3)
    assert ring.mul(central, ring.scalar(coefficients[2])) != ring.zero
    assert ring.mul(central, ring.scalar(3)) == ring.zero
    # The lower-binomial contribution survives on the original ring, at t=2.
    full = ring.mul(central, ring.scalar(comb(4, 4)))
    guessed_diagonal = ring.mul(central, ring.scalar(16*comb(2, 4)))
    assert full != guessed_diagonal


def test_no_linear_basis_change_restores_scalar_weights(ring):
    dilation = newton_dilation_matrix(4, 4)
    identity = fmpz_mat([[int(i == j) for j in range(4)] for i in range(4)])
    nilpotent = dilation-identity
    assert any(int(nilpotent[i, j]) % 3 for i in range(4) for j in range(4))
    assert all(int((nilpotent**2)[i, j]) % 3 == 0 for i in range(4) for j in range(4))
    assert all(int((dilation**3-identity)[i, j]) % 3 == 0 for i in range(4) for j in range(4))
    central = ring.power(ring.pi, 3)
    assert ring.mul(central, ring.scalar(comb(4, 4))) != ring.zero
    assert comb(1, 4) == 0
    assert all(pow(4, j, 3) == 1 for j in range(1, 5))


@pytest.mark.parametrize("p", [2, 3, 5, 7, 11, 13])
def test_nontrivial_unipotent_repair_obstruction_at_every_prime(p):
    dilation = newton_dilation_matrix(p, 1+p)
    for i in range(p):
        for j in range(p):
            assert int(dilation[i, j]) % p == int(i == j)+int(i == 0 and j == p-1)
    # Coefficients may all be the same central order-p element, even for t=2.
    other = CyclotomicRing(p, 2)
    central = other.power(other.pi, other.L-1)
    assert central != other.zero
    assert other.mul(central, other.scalar(p)) == other.zero
    assert p <= other.L


@pytest.mark.parametrize("degree,a,b", [(4, 2, 4), (7, 3, 2)])
def test_newton_matrices_compose_as_substitutions(degree, a, b):
    assert newton_dilation_matrix(degree, a)*newton_dilation_matrix(degree, b) == newton_dilation_matrix(degree, a*b)


def test_group_inverses_commutators_and_hidden_subgroups(ring):
    identity = (ring.zero, 0)
    generators = [(ring.one, 0), (ring.zeta, 0), (ring.zero, 1)]
    for x in ring.elements():
        for a in range(3):
            g = x, a
            assert ring.group_mul(g, ring.group_inverse(g)) == identity
            for y, b in generators:
                expected = ring.add(ring.mul(ring.sub(ring.one, ring.power(ring.zeta, b)), x),
                                    ring.mul(ring.sub(ring.power(ring.zeta, a), ring.one), y))
                assert ring.commutator(g, (y, b)) == (expected, 0)
    for secret in (0, 1, 3):
        hidden = ring.hidden(secret)
        assert len(hidden) == 3
        assert all(ring.group_mul(g, h) in hidden for g in hidden for h in hidden)


def test_original_group_not_an_exponent_three_field_group(ring):
    g, power = (ring.one, 0), (ring.zero, 0)
    for _ in range(3):
        power = ring.group_mul(power, g)
    assert power == (ring.scalar(3), 0) != (ring.zero, 0)
    for _ in range(6):
        power = ring.group_mul(power, g)
    assert power == (ring.zero, 0)


def test_original_secret_digits_are_destroyed_by_reduction_mod_p(ring):
    left, right = ring.hidden(0), ring.hidden(3)
    assert left != right
    reduce = lambda subgroup: {(tuple(c % 3 for c in x), j) for x, j in subgroup}
    assert reduce(left) == reduce(right)
    assert ring.pairing_matrix() == [[0, 1], [1, 8]]
    p0, p3 = ring.phase(ring.zeta, 0), ring.phase(ring.zeta, 3)
    assert p0 == (Fraction(0),)*3
    assert p3 == (Fraction(0), Fraction(1, 3), Fraction(0))
    assert exact_phase_fidelity(p0, p3) == Fraction(1, 3)


def test_pairing_additivity_and_non_degeneracy(ring):
    elements = ring.elements()
    for x in elements:
        characters = {ring.character_exponent(x, y) for y in elements}
        assert (characters == {Fraction(0)}) == (x == ring.zero)
        for y in (ring.one, ring.zeta):
            assert ring.character_exponent(x, y) == ring.character_exponent(y, x)
            assert ring.character_exponent(x, ring.add(y, ring.one)) == (
                ring.character_exponent(x, y)+ring.character_exponent(x, ring.one)) % 1


@pytest.mark.parametrize("p,t", [(2, 3), (3, 1), (5, 1), (5, 2)])
def test_other_ramified_pairings_and_nilpotence(p, t):
    other = CyclotomicRing(p, t)
    assert other.pairing_matrix()
    assert other.power(other.pi, other.L) == other.zero
    assert other.power(other.pi, other.L-1) != other.zero


def test_normalizer_scope_on_actual_group(ring):
    for secret in (0, 1, 3):
        generator = (ring.scalar(secret), 1)
        actual = set()
        for x in ring.elements():
            for a in range(3):
                g = (x, a)
                conjugate = ring.group_mul(ring.group_mul(g, generator), ring.group_inverse(g))
                if conjugate == generator:
                    actual.add(g)
        center = ring.ideal(ring.L-1)
        expected = {(ring.add(ring.mul(ring.lam(a), ring.scalar(secret)), w), a)
                    for a in range(3) for w in center}
        assert actual == expected
        assert len(actual) == 9 < 243


def test_control_caps_are_explicit():
    with pytest.raises(ValueError, match="enumeration cap"):
        CyclotomicRing(5, 2).elements()
    with pytest.raises(ValueError):
        newton_dilation(0, 2)
    with pytest.raises(ValueError):
        exact_phase_fidelity([Fraction(0)], [Fraction(1, 127)])

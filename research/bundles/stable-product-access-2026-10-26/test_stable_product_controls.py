import pytest
from sympy import Matrix, Rational, diag, eye, expand, symbols
from sympy.matrices.normalforms import hermite_normal_form

from stable_product_controls import (
    GRAM_I, GRAM_J, GRAM_O, OMEGA_I, OMEGA_J, OMEGA_O, PAIRING,
    check_local, index_form, intertwiner, paired_local_isomorphism,
    rational_charts, stable_certificate, stable_isomorphism, vanishes_mod,
)


def test_actual_order_and_ideal_bases():
    for basis, action in ((eye(2), OMEGA_O),
                          (Matrix([[2, 0], [0, 1]]), OMEGA_I),
                          (Matrix([[2, -1], [0, 1]]), OMEGA_J)):
        assert OMEGA_O*basis == basis*action
        assert action**2-action+6*eye(2) == Matrix.zeros(2)


def test_ideal_times_conjugate_is_two_O():
    # Products of (2,w) with (2,w-1), in the basis (1,w).
    products = Matrix([[4, -2, 0, -6], [0, 2, 2, 0]])
    assert hermite_normal_form(products) == 2*eye(2)


def test_general_intertwiner_and_positive_index_identity():
    x, y = symbols("x y")
    transform = intertwiner(x, y)
    assert OMEGA_I*transform == transform*OMEGA_O
    assert expand(transform.det()-index_form(x, y)) == 0
    assert expand(8*index_form(x, y)-(4*x+y)**2-23*y*y) == 0
    assert (transform.T*GRAM_I*transform-index_form(x, y)*GRAM_O).applyfunc(expand) == Matrix.zeros(2)


def test_intertwiner_formula_is_exhaustive():
    x, y, z, t = symbols("x y z t")
    transform = Matrix([[x, z], [y, t]])
    residual = OMEGA_I*transform-transform*OMEGA_O
    assert residual[0, 0] == -3*y-z
    assert residual[1, 0] == 2*x+y-t
    assert residual.subs({z: -3*y, t: 2*x+y}) == Matrix.zeros(2)


def test_rational_isometries_do_not_supply_integral_isomorphism():
    for transform in rational_charts():
        assert transform.det() == 1
        assert OMEGA_I*transform == transform*OMEGA_O
        assert transform.T*PAIRING*transform == PAIRING
        assert transform.T*GRAM_I*transform == GRAM_O
        assert any(entry.q != 1 for entry in transform)


def test_all_small_moduli_including_ramified_and_denominator_primes():
    for modulus in range(2, 257):
        assert all(check_local(modulus)["checks"].values())


@pytest.mark.parametrize("modulus", [2**512, 3**200, 23**120, 2**256*3**100*23**30])
def test_large_prime_powers_and_mixed_modulus(modulus):
    assert all(check_local(modulus)["checks"].values())


@pytest.mark.parametrize("small,large", [(2, 6), (4, 24), (9, 72), (23, 46*23),
                                         (40, 840), (2**80*23, 2**120*23**3*3**10)])
def test_inverse_system_compatibility(small, large):
    assert large % small == 0
    assert vanishes_mod(paired_local_isomorphism(large)-paired_local_isomorphism(small), small)


def test_stable_product_isomorphism_and_polarization_mismatch():
    transform = stable_isomorphism()
    assert transform.det() == 1
    assert all(entry.q == 1 for entry in transform.inv())
    assert diag(OMEGA_O, OMEGA_O)*transform == transform*diag(OMEGA_I, OMEGA_J)
    assert not stable_certificate()["product_metric_preserved"]


def test_minimum_proof_identities_not_a_finite_hardness_search():
    x, y = symbols("x y")
    for gram, sign in ((GRAM_I, 1), (GRAM_J, -1)):
        norm = (Matrix([[x, y]])*gram*Matrix([x, y]))[0]/2
        assert expand(8*norm-(4*x+sign*y)**2-23*y*y) == 0
        assert norm.subs({x: 1, y: 0}) == 2
    assert GRAM_O[0, 0]/2 == 1


def test_no_positive_form_fixed_by_the_native_unipotent():
    a, b, d = symbols("a b d")
    gram = Matrix([[a, b], [b, d]])
    shear = Matrix([[1, 1], [0, 1]])
    difference = shear.T*gram*shear-gram
    assert difference[0, 1] == a  # Invariance forces a=0, contradicting positivity.


def test_rational_entries_cannot_be_truncated_into_a_modular_certificate():
    with pytest.raises(ValueError, match="integral entries"):
        vanishes_mod(Matrix([[Rational(1, 2)]]), 5)


@pytest.mark.parametrize("modulus", [0, 1, -3, 2.0, True])
def test_invalid_moduli_rejected(modulus):
    with pytest.raises(ValueError):
        paired_local_isomorphism(modulus)

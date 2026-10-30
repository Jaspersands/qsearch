"""Exact genus-two controls, NOT a geometric quotient or efficient HSP oracle.

Quaternion arithmetic and torsion matrices use the existing char-11 fixtures.
No large torsion field is constructed. The saved orders are exact resource
countercontrols for six specified lifts, not a lower bound on all lifts.
"""

import itertools
import json
from math import gcd, prod
from pathlib import Path

import pytest
from flint import fmpz
from sympy import Matrix, eye as real_eye
from sympy.matrices.normalforms import smith_normal_form

from tests.test_siegel_repolarization import (
    ONE, PHI, ROOTS, ZERO, add, adj, compile_word, divide_exact, eye,
    mul, polarization, qa, qc, qm, qs, reduce, scale,
)


def norm(q):
    answer = qm(qc(q), q)
    assert answer[1:] == (0, 0, 0)
    return answer[0]


def trace(s):
    assert s[0][0][1:] == s[1][1][1:] == (0, 0, 0)
    return s[0][0][0] + s[1][1][0]


def shear(q, ell):
    return ((ONE, qs(ell, q)), (ZERO, ONE))


def avoid_odd_primes(s, ell, primes):
    """Proof-control implementation; known quaternion coordinates only."""
    a, b, n0 = s[0][0][0], s[0][1], trace(s) + 2
    value, modulus, choices = ZERO, 1, []
    for r in primes:
        assert r % 2 and r != ell and fmpz(r).is_prime()
        direction = ONE if a % r else b
        candidates = range(3) if a % r else range(2)
        for z in candidates:
            q = qs(z, direction)
            n = n0 + 2 * ell * qm(qc(q), b)[0] + a * ell**2 * norm(q)
            if n % r:
                break
        else:
            raise AssertionError("local avoidance lemma failed")
        choices.append((r, q, bool(a % r)))
        inverse = pow(modulus, -1, r)
        value = tuple(x + modulus * ((y - x) * inverse % r)
                      for x, y in zip(value, q))
        modulus *= r
    return value, choices


@pytest.mark.parametrize("root", ROOTS)
def test_plus_construction_and_secret_prime_avoidance(root):
    sigma, _ = compile_word(root)
    s, h, unit = mul(adj(sigma), sigma), polarization(sigma), eye(2)
    t = trace(s)
    n = t + 2
    eta = add(h, unit)
    h_inverse = add(scale(t, unit), scale(-1, h))
    mu = add(h_inverse, unit)
    assert mul(eta, eta) == scale(n, h)
    assert mul(eta, mu) == mul(mu, eta) == scale(n, unit)
    assert mul(mul(adj(mu), h), mu) == scale(n, unit)
    correction = divide_exact(add(s, scale(-1, unit)), 61)
    determinant = correction[0][0][0] * correction[1][1][0] - norm(correction[0][1])
    assert t - 2 == -(61**2) * determinant
    assert (n - 4) % 61**2 == 0
    assert (t - 2) % 61 == 0  # The minus construction has the forbidden factor.


@pytest.mark.parametrize("index,prime", [(0, 19), (2, 19), (4, 5), (4, 13), (5, 73)])
def test_kernel_image_is_maximal_isotropic_and_weak_mask_independent(index, prime):
    sigma, _ = compile_word(ROOTS[index])
    s, h = mul(adj(sigma), sigma), polarization(sigma)
    assert (trace(s) + 2) % prime == 0
    eta = reduce(add(h, eye(2)), prime)
    eta_source = reduce(add(s, eye(2)), prime)
    base = reduce(PHI, prime)
    assert eta * base == base * eta_source
    image = (base * eta_source).transpose().rref()[0]
    assert eta.rank() == 2
    assert (eta * eta).rank() == 0
    from tests.test_siegel_repolarization import form
    assert (eta.transpose() * form(2, prime) * eta).rank() == 0
    for mask in [1, 2, prime - 1]:
        assert gcd(mask, prime) == 1
        assert (mask * base * eta_source).transpose().rref()[0] == image


def test_nonfree_primary_kernel_and_mark_transport_on_actual_integral_fixture():
    phi = Matrix([[1, 2], [-2, 1]])
    sigma = Matrix([[1, 10], [0, 1]])
    s = sigma.T * sigma
    h = phi * s * phi.inv()
    assert h == Matrix([[89, 34], [34, 13]])
    n, eta = 104, h + real_eye(2)
    u = Matrix([[5, 2], [8, 3]])
    quotient = Matrix([[2, 10], [10, -2]])
    assert u.det() == -1 and u.T * u == h
    assert quotient.T * quotient == n * real_eye(2)
    assert quotient * eta == n * u
    snf = smith_normal_form(eta)
    assert [abs(int(snf[i, i])) for i in range(2)] == [2, 52]
    image = {tuple(int(x) % 8 for x in eta * Matrix(v))
             for v in itertools.product(range(8), repeat=2)}
    kernel = {v for v in itertools.product(range(8), repeat=2)
              if all(int(x) % 8 == 0 for x in eta * Matrix(v))}
    assert image == kernel and len(kernel) == 8
    # Each real coordinate acts on two elliptic torsion coordinates.
    assert len(kernel)**2 == 8**2
    assert all(tuple(4 * x % 8 for x in v) == (0, 0) for v in kernel)
    assert any(tuple(2 * x % 8 for x in v) != (0, 0) for v in kernel)
    # Thus type (Z/2)^2 x (Z/4)^2, not the free (Z/8)^2.
    assert all(sum(x*y for x, y in zip(v, w)) % 8 == 0
               for v, w in itertools.product(kernel, repeat=2))
    for r in [3, 7, 17]:
        inverse = pow(n, -1, r)
        marked = u * phi * sigma.inv()
        computed = inverse * quotient * phi * (s + real_eye(2)) * sigma.inv()
        for mask in [1, 2, r - 1]:
            assert all(int(x) % r == 0 for x in mask * (computed - marked))
    with pytest.raises(ValueError):
        pow(n, -1, 13)  # Overlapping marks need extra division-torsion input.


@pytest.mark.parametrize("root", ROOTS)
@pytest.mark.parametrize("q", [ONE, (0, 1, 0, 0), (2, -1, 3, -2)])
def test_congruence_shear_norm_identity(root, q):
    sigma, sigma_inverse = compile_word(root)
    s = mul(adj(sigma), sigma)
    a, b = s[0][0][0], s[0][1]
    changed = mul(sigma, shear(q, 61))
    new_s = mul(adj(changed), changed)
    n = trace(new_s) + 2
    assert n == trace(s) + 2 + 2*61*qm(qc(q), b)[0] + a*61**2*norm(q)
    assert a * n == norm(qa(qs(a * 61, q), b)) + (a + 1)**2
    assert reduce(changed, 61) == reduce(sigma, 61)
    elementary = ((ZERO, q), (ZERO, ZERO))
    transported = mul(mul(PHI, elementary), adj(PHI))
    v = add(eye(2), scale(-1, transported))
    assert mul(v, add(eye(2), transported)) == eye(2)
    changed_inverse = mul(shear(qs(-1, q), 61), sigma_inverse)
    psi, new_psi = mul(PHI, sigma_inverse), mul(PHI, changed_inverse)
    new_h = polarization(changed)
    assert mul(v, psi) == new_psi
    assert mul(mul(adj(v), new_h), v) == polarization(sigma)
    operator = mul(add(new_s, eye(2)), changed_inverse)
    assert operator == add(adj(changed), changed_inverse)
    assert mul(adj(operator), operator) == scale(n, eye(2))
    assert mul(PHI, operator) == mul(add(new_h, eye(2)), new_psi)


def test_stale_marking_after_lift_change_is_not_even_projectively_correct():
    phi = Matrix([[1, 2], [-2, 1]])
    sigma = Matrix([[1, 10], [0, 1]])
    congruence = Matrix([[1, 5], [0, 1]])
    changed = sigma * congruence
    s, new_s = sigma.T * sigma, changed.T * changed
    new_h = phi * new_s * phi.inv()
    v = phi * congruence.inv() * phi.inv()
    u = Matrix([[5, 2], [8, 3]]) * v.inv()
    assert u.T * u == new_h
    n = int(new_s.trace() + 2)
    assert n == 229
    quotient = u * (real_eye(2) + new_h.inv())
    assert all(x.is_Integer for x in quotient)
    assert quotient.T * quotient == n * real_eye(2)
    inverse = pow(n, -1, 3)
    correct = inverse * quotient * phi * (new_s + real_eye(2)) * changed.inv()
    stale = inverse * quotient * phi * (s + real_eye(2)) * sigma.inv()
    assert all(int(x) % 3 == 0 for x in correct - u * phi * changed.inv())
    assert all(any(int(x) % 3 for x in correct - mask * stale) for mask in [1, 2])


def test_fixed_mark_and_characteristic_avoidance_including_zero_diagonal_branch():
    # Lower identity-congruence shear has a=26, so the r=13 branch is linear.
    sigma = ((ONE, ZERO), (qs(5, ONE), ONE))
    s = mul(adj(sigma), sigma)
    primes = [3, 7, 11, 13, 17, 29]
    assert (trace(s) + 2) % 29 == 0
    q, choices = avoid_odd_primes(s, 5, primes)
    assert next(quadratic for r, _, quadratic in choices if r == 13) is False
    changed = mul(sigma, shear(q, 5))
    n = trace(mul(adj(changed), changed)) + 2
    assert gcd(n, 5 * prod(primes)) == 1
    assert reduce(changed, 5) == reduce(sigma, 5)
    for r, residue, _ in choices:
        assert all((x-y) % r == 0 for x, y in zip(q, residue))


def test_norm_search_requires_the_conjugate_orientation():
    sigma = ((ONE, (0, 5, 0, 0)), (ZERO, ONE))
    q = (0, 1, 0, 0)
    s = mul(adj(sigma), sigma)
    changed = mul(sigma, shear(q, 5))
    actual = trace(mul(adj(changed), changed)) + 2
    assert actual == 104
    wrong = trace(s) + 2 + 2*5*qm(q, s[0][1])[0] + 25*norm(q)
    assert wrong == 4


@pytest.mark.parametrize("r,root_minus_one", [(13, 5), (17, 4), (29, 12), (101, 10)])
def test_identity_lifts_can_force_expensive_new_prime_divisors(r, root_minus_one):
    assert root_minus_one**2 % r == r-1
    ell = 61
    k = 2 * root_minus_one * pow(ell, -1, r) % r
    n = 4 + ell**2 * k**2
    assert n % r == 0
    assert gcd(n, ell) == 1


def test_fixed_single_small_prime_does_not_make_multiplier_affordable():
    def exact_order(base, modulus, order):
        assert pow(base, order, modulus) == 1
        assert all(pow(base, order // int(r), modulus) != 1
                   for r, _ in fmpz(order).factor())

    exact_order(2, 61**2, 3660)
    exact_order(3, 61, 10)
    exact_order(4, 61, 30)
    assert pow(4, 10, 61) != 1  # 4 is not in the subgroup generated by 3.
    for root in ROOTS:
        sigma, _ = compile_word(root)
        a = mul(adj(sigma), sigma)[0][0][0]
        assert a > 1 and (a + 1)**2 > 4*a  # N=4 impossible after upper shear.
    assert (3662 + 1)//2 - 2 == 1829
    for exponent in range(2, 21):
        exact_order(-11, 2**exponent, 2**(exponent - 2))


def test_cayley_scalar_identity_does_not_extend_to_general_dimension():
    sigma = Matrix([[1, 1, 0], [0, 1, 1], [0, 0, 1]])
    h = sigma.T * sigma
    assert h.det() == 1
    candidate = (h + real_eye(3))**2 * h.inv()
    assert candidate != candidate[0, 0] * real_eye(3)


def test_saved_six_lift_resource_countercontrols():
    path = Path(__file__).resolve().parents[1] / "research/classical_baselines/siegel_cayley_costs.json"
    report = json.loads(path.read_text())
    assert report["status"] == "CONDITIONAL_CONSTRUCTION_NOT_EFFICIENT_ORACLE"
    assert report["characteristic"] == 11 and report["ell"] == 61
    # #E(F_11)=12 implies trace zero, hence scalar Frob^2=[-11].
    count = 1 + sum((y*y - (x*x*x-x)) % 11 == 0
                    for x, y in itertools.product(range(11), repeat=2))
    assert count == 12
    assert len(report["lifts"]) == len(ROOTS)
    for i, row in enumerate(report["lifts"]):
        assert row["root"] == [list(x) for x in ROOTS[i]]
        sigma, _ = compile_word(ROOTS[i])
        n = trace(mul(adj(sigma), sigma)) + 2
        assert row["N"] == n
        assert prod(term["prime"]**term["exponent"] for term in row["primary_costs"]) == n
        for term in row["primary_costs"]:
            r, a, order = term["prime"], term["exponent"], term["full_torsion_extension_degree"]
            assert fmpz(r).is_prime() and a > 0
            assert pow(-11, order, r**a) == 1
            # Exact minimality certificate, without constructing any field.
            for factor, _ in fmpz(order).factor():
                assert pow(-11, order // int(factor), r**a) != 1
        assert row["largest_primary_extension_degree"] == max(
            term["full_torsion_extension_degree"] for term in row["primary_costs"])

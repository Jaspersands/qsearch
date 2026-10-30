from copy import deepcopy
from math import gcd, prod

import pytest
from sympy import Matrix, ZZ, eye, diag, symbols, expand
from sympy.matrices.normalforms import smith_normal_form

from smooth_repolarization import (
    Quadratic, certificate, coin_witness, evaluate, matmul, norm_matrix,
    resource_plan, transpose, verify_certificate,
)


@pytest.mark.parametrize("trace", [3, 4, 5, 6, 7, 8, 11, 18, 63, 257, 3723])
def test_ring_certificate(trace):
    plan = resource_plan(trace, 61, 103)
    record = certificate(trace, plan["denominator"])
    assert all(verify_certificate(record).values())


@pytest.mark.parametrize("trace", range(3, 33))
def test_coin_certificate_at_smallest_allowed_even_denominator(trace):
    d = trace if trace % 2 == 0 else trace+1
    x, y = coin_witness(trace, d)
    assert x >= 0 and y >= 0 and (trace+2)*x+(trace-2)*y == d*d


def test_octonion_identity_independent_of_quadratic_relation():
    vector = (1, 2, 3, 5, 7, 11, 13, 17)
    c = Matrix(norm_matrix(vector))
    assert c.T*c == c*c.T == sum(x*x for x in vector)*eye(8)


def test_eight_square_identity_symbolically_in_all_coefficients():
    vector = symbols("a0:8")
    c = Matrix(norm_matrix(vector))
    target = sum(x*x for x in vector)*eye(8)
    assert all(expand(x) == 0 for x in c.T*c-target)
    assert all(expand(x) == 0 for x in c*c.T-target)


def test_gaussian_surface_and_polarization_orientation():
    # E:y^2=x^3-x in characteristic 103 is supersingular (103 = 3 mod 4).
    # These are exact endomorphism matrices, not elliptic point calculations.
    phi = Matrix([[6,-5,0,0], [5,6,0,0], [0,0,6,5], [0,0,-5,6]])
    sigma = Matrix([[1,0,61,0], [0,1,0,61], [0,0,1,0], [0,0,0,1]])
    s = sigma.T*sigma
    h = phi*s*phi.T/61
    u = phi*sigma.inv()*phi.T/61
    assert all(x.q == 1 for x in h) and all(x.q == 1 for x in u)
    assert phi.T*phi == 61*eye(4)
    assert h*h-3723*h+eye(4) == Matrix.zeros(4)
    assert u.T*h*u == eye(4)
    record = certificate(3723, 30030)
    integer_h = tuple(tuple(int(x) for x in h.row(i)) for i in range(4))
    c, e = (Matrix(evaluate(record[name], integer_h)) for name in ("C", "E"))
    h8 = diag(*([h]*8))
    assert e.T*h8*e == 30030**2*eye(32)
    assert e*c == c*e == 30030**2*eye(32)
    # Omitting H^-1 gives a wrong polarized source, even though C is integral.
    assert c*h8*c.T != 30030**2*eye(32)


def test_prime_square_kernel_really_needs_prime_square_points():
    h = ((1,0,1,-2), (0,1,2,1), (1,2,6,0), (-2,1,0,6))
    e = Matrix(evaluate(certificate(7,30)["E"], h))
    smith = smith_normal_form(e, domain=ZZ)
    invariants = [abs(int(smith[i,i])) for i in range(32)]
    assert max(invariants) == 450
    for prime in (3, 5):
        full_kernel = prod(gcd(s, prime*prime) for s in invariants)
        prime_order_part = prod(gcd(s, prime) for s in invariants)
        assert full_kernel == prime**32
        assert prime_order_part < full_kernel
    # E has all 2-torsion in its kernel: a non-free maximal isotropic in X[4].
    assert prod(gcd(s,4) for s in invariants) == 2**32
    assert all(s % 2 == 0 and s % 4 != 0 for s in invariants)


def test_classical_scaled_transport_has_larger_polarized_multiplier():
    phi = Matrix([[6,-5,0,0], [5,6,0,0], [0,0,6,5], [0,0,-5,6]])
    swap = Matrix([[0,0,1,0], [0,0,0,1], [1,0,0,0], [0,1,0,0]])
    a = swap*diag(Matrix([[1,-2],[2,1]]), Matrix([[1,-2],[2,1]]))
    b = phi*a*phi.T
    assert a.T*a == 5*eye(4)
    assert b.T*b == 61**2*5*eye(4)
    weak_basis = 3*phi
    assert b*weak_basis == 61*weak_basis*a
    assert b.T*b != 5*eye(4)


def test_prime_by_prime_loop_counterexample():
    # G = E[r] inside E[r^2], maximal isotropic of order r^2.
    # The proposed first step r*G is zero, not an order-r isotropic kernel.
    r, modulus = 3, 9
    generators = ((r,0), (0,r))
    scaled = [tuple(r*x % modulus for x in v) for v in generators]
    assert scaled == [(0,0), (0,0)]
    assert all((a[0]*b[1]-a[1]*b[0]) % modulus == 0
               for a in generators for b in generators)


def test_transport_on_auxiliary_level_and_scalar_cancellation():
    record = certificate(7,30)
    h = ((1,0,1,-2), (0,1,2,1), (1,2,6,0), (-2,1,0,6))
    c, e = (Matrix(evaluate(record[name], h)) for name in ("C", "E"))
    order, scalar = 49, 17
    v = Matrix(range(32))
    transported = c*v*pow(30**2, -1, order)
    assert all(int(x) % order == 0 for x in e*transported-v)
    scaled_transport = c*(scalar*v)*pow(30**2, -1, order)
    assert scaled_transport == scalar*transported
    with pytest.raises(ValueError):
        pow(30**2, -1, 25)


@pytest.mark.parametrize("bits", [8, 32, 128, 256, 1024])
def test_public_plan_charges_bounded_prime_squares_not_large_power(bits):
    t = 2**bits+3
    plan = resource_plan(t, 2**127-1, 103)
    d, primes = plan["denominator"], plan["denominator_primes"]
    assert d == prod(primes) and len(primes) == len(set(primes))
    assert d > t+2 and gcd(d, (2**127-1)*103) == 1
    assert plan["weak_evaluation_orders"] == [r*r for r in primes]
    assert set(primes).isdisjoint(plan["marking_primes"])
    assert plan["marking_product"]**2 > plan["projective_bound_squared"]
    assert max(plan["weak_evaluation_orders"]) < (100*bits)**2
    assert not plan["quantum_speedup_admitted"]
    assert not plan["geometric_backend_executed"]


def test_corrupted_certificate_fails():
    record = deepcopy(certificate(7,30))
    c = [list(row) for row in record["C"]]
    c[0][0] = c[0][0]+1
    record["C"] = tuple(map(tuple,c))
    assert not verify_certificate(record)["C_adjoint_C"]


def test_ring_and_scope_rejections():
    with pytest.raises(ValueError):
        Quadratic(3)+Quadratic(4)
    with pytest.raises(ValueError):
        Quadratic(2)
    with pytest.raises(ValueError):
        coin_witness(7,7)
    with pytest.raises(ValueError):
        coin_witness(7,2)
    with pytest.raises(ValueError):
        coin_witness(True,6)
    with pytest.raises(ValueError):
        norm_matrix([1,2])
    with pytest.raises(ValueError):
        evaluate(certificate(7,30)["E"], ((2,0),(0,3)))
    with pytest.raises(ValueError):
        resource_plan(7,61,2)


def test_integrality_is_not_a_positivity_test():
    # The certificate is formal algebra. Its verifier does not prove that H
    # is a geometric polarization or that source points/evaluators exist.
    h = Quadratic(7,0,1)
    assert h*h-7*h+1 == Quadratic(7)
    assert all(verify_certificate(certificate(7,30)).values())

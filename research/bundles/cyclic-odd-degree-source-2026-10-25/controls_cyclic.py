"""Finite arithmetic/phase controls only, not geometric or quantum execution."""

from math import gcd, prod
import sys

import numpy as np
from sympy import Matrix, eye, zeros
from sympy.ntheory.modular import crt

from cyclic_source import ROOT, checked_factors, mod
from kernel_output import (
    action, alternating_form, inverse_mod, matrix_multiply, matrix_star,
    odd_maximal_order, odd_maximal_split, product_actions,
)


def split_fixture(characteristic, n, factors):
    """Small-prime initial split, then exact Hensel/CRT lift of its coefficients."""
    factors = checked_factors(n, factors)
    moduli, aa, bb = [], [], []
    for p, e in factors:
        base = odd_maximal_split(characteristic, p)
        j = mod(2*base[2]-eye(2), p)
        a, b = int(j[0, 0]), int(j[0, 1])
        modulus = p
        while modulus < p**e:
            error = (a*a+b*b+characteristic)//modulus
            if a % p:
                a += modulus*((-error*pow(2*a, -1, p)) % p)
            else:
                b += modulus*((-error*pow(2*b, -1, p)) % p)
            modulus *= p
        moduli.append(modulus)
        aa.append(a)
        bb.append(b)
    a, b = int(crt(moduli, aa)[0]), int(crt(moduli, bb)[0])
    i, j = Matrix([[0, -1], [1, 0]]), Matrix([[a, b], [b, -a]])
    half = pow(2, -1, n)
    h = half*(eye(2)+j)
    return tuple(mod(x, n) for x in (eye(2), i, h, i*h))


def doubled(vector):
    vector = Matrix(vector)
    return Matrix.vstack(Matrix.hstack(vector, zeros(2, 1)),
                         Matrix.hstack(zeros(2, 1), vector))


def preserves_doubled(matrix, vector, n):
    """Arithmetic predicate used by tests, never supplied to a hidden solver."""
    x, y = map(int, vector)
    if gcd(x, y, n) != 1:
        raise ValueError("primitive line required")
    moved = mod(Matrix(matrix)*doubled(vector), n)
    return all((x*int(moved[start+1, j])-y*int(moved[start, j])) % n == 0
               for start in (0, 2) for j in (0, 1))


def local_lines(p, e):
    m = p**e
    return [(z, 1) for z in range(m)] + [(1, p*z) for z in range(m//p)]


def square_phase_control(p, e, frequency, slope):
    """Enumerative numerical check of the derived local Fourier formula."""
    m = p**e
    squares = sorted({a*a % m for a in range(m) if gcd(a, m) == 1})
    state = np.zeros(m, dtype=complex)
    for t in squares:
        state[t] = np.exp(2j*np.pi*((frequency*slope*t) % m)/m)/np.sqrt(len(squares))
    probabilities = abs(np.fft.fft(state)/np.sqrt(m))**2
    return {"modulus": m, "square_unit_count": len(squares),
            "correct_frequency": frequency*slope % m,
            "correct_probability": float(probabilities[frequency*slope % m]),
            "predicted_probability": len(squares)/m,
            "normalization": float(probabilities.sum()),
            "quantum_execution": False, "size_enumerative_not_scalable": True}


def cyclic_degree25_control():
    """Maps in End(E), not generated curve points or a geometric quotient."""
    sys.path.insert(0, str(ROOT / "prime-only-source-2026-10-25"))
    sys.path.insert(0, str(ROOT / "source-pullback-2026-10-23"))
    from prime_source import prime_certificate, verify_prime_certificate
    from pullback import column_basis

    order, n = odd_maximal_order(11), 25
    unit, i = order.unit, eye(4)[:, 1]
    j = 2*eye(4)[:, 2]-unit
    alpha = 3*unit+4*i
    assert order.multiply(order.star(alpha), alpha) == n*unit
    zero = zeros(4, 1)
    phi = Matrix.vstack(alpha, zero, zero, alpha)
    sigma = Matrix.vstack(unit, n*j, zero, unit)
    s = matrix_multiply(order, matrix_star(order, sigma), sigma)
    h = matrix_multiply(order, matrix_multiply(order, phi, s), matrix_star(order, phi))/n
    assert all(x.q == 1 for x in h)
    t = int((order.traces*(h[:4, :]+h[12:, :]))[0]/2)
    assert t == 6877
    assert matrix_star(order, h) == h
    phi5 = mod(action(alpha, odd_maximal_split(11, 5)), 5)
    assert column_basis(phi5, 5).cols == 1
    primes = (3, 7, 13, 17, 19, 23, 29)
    multiplier = prod(primes)
    certificate = prime_certificate(t, multiplier)
    assert all(verify_prime_certificate(certificate).values())
    records = []
    for r in primes+(31,):
        split = odd_maximal_split(11, r)
        hr = mod(action(h, product_actions(split)), r)
        sr = mod(action(s, product_actions(split)), r)
        weak = mod(2*action(phi, product_actions(split)), r)
        assert mod(weak*sr*inverse_mod(weak, r)-hr, r) == zeros(4)
        assert mod(hr*hr-t*hr+eye(4), r) == zeros(4)
        # These are modular Tate actions, not exact integer representatives of H.
        c, f = (mod(Matrix.vstack(*[
            Matrix.hstack(*[entry.u*eye(4)+entry.v*hr for entry in row])
            for row in certificate[k]
        ]), r) for k in ("C", "F"))
        form, h8 = alternating_form(16), Matrix.diag(*([hr]*8))
        assert mod(f*c-multiplier*eye(32), r) == zeros(32)
        assert mod(c*f-multiplier*eye(32), r) == zeros(32)
        assert mod(f.T*form*h8*f-multiplier*form, r) == zeros(32)
        if r in primes:
            kernel = column_basis(c, r)
            assert kernel.cols == column_basis(f, r).cols == 16
            assert mod(f*kernel, r) == zeros(32, 16)
            assert mod(kernel.T*form*kernel, r) == zeros(16)
            records.append({"prime": r, "kernel_dimension": 16,
                            "isotropic": True, "nonsemisimple_possible": (t*t-4) % r == 0})
    return {"characteristic": 11, "elliptic_degree": n, "trace": t,
            "multiplier": multiplier, "phi_mod5_rank": 1,
            "local_kernels": records, "nonquotient_identity_check_prime": 31,
            "curve_points_generated": False, "quotient_executed": False}

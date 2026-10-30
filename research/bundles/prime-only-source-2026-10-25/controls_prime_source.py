"""Exact arithmetic realizations, not theta points or geometric quotients."""

from math import prod

from sympy import Matrix, diag, eye, zeros

from prime_source import ROOT, prime_certificate, verify_prime_certificate
from smooth_repolarization import evaluate

import sys
sys.path.insert(0, str(ROOT / "source-pullback-2026-10-23"))
from pullback import column_basis
from kernel_output import alternating_form, mod


def integral_control():
    # Gaussian endomorphisms in characteristic 11 (j=1728). This encodes
    # maps in a known order; it does not construct elliptic/torsion points.
    phi = Matrix([[2,-1,0,0], [1,2,0,0], [0,0,2,1], [0,0,-1,2]])
    sigma = eye(4)
    sigma[:2, 2:] = 5*eye(2)
    s = sigma.T*sigma
    h = phi*s*phi.T/5
    assert phi.T*phi == 5*eye(4)
    assert all(x.q == 1 for x in h)
    assert h*h-27*h+eye(4) == zeros(4)
    primes = (3, 7, 13, 17, 19, 23, 29)
    n = prod(primes)
    certificate = prime_certificate(27, n)
    checks = verify_prime_certificate(certificate)
    assert all(checks.values())
    exact_h = tuple(tuple(int(x) for x in h.row(i)) for i in range(4))
    c, f = (Matrix(evaluate(certificate[key], exact_h)) for key in ("C", "F"))
    form, h8 = alternating_form(16), diag(*([h]*8))
    assert f*c == c*f == n*eye(32)
    assert f.T*form*h8*f == n*form
    records = []
    for r in primes:
        weak = mod(2*phi, r)
        assert mod(weak*s*weak.inv_mod(r), r) == mod(h, r)
        kernel = column_basis(c, r)
        rank = column_basis(f, r).cols
        assert kernel.cols == rank == 16
        assert mod(f*kernel, r) == zeros(32, 16)
        assert mod(kernel.T*form*kernel, r) == zeros(16)
        assert column_basis(2*c, r).cols == 16
        records.append({"prime": r, "kernel_dimension": kernel.cols,
                        "F_rank": rank, "isotropic": True,
                        "quadratic_discriminant_zero": (27*27-4) % r == 0})
    # Explicitly exercise the ramified, nonsemisimple quadratic case.
    assert mod(h+eye(4), 29) != zeros(4)
    assert mod((h+eye(4))**2, 29) == zeros(4)
    mark, mask = 31, 7
    z = diag(*([mask*phi*sigma.inv()]*8))
    transported = mod(pow(n, -1, mark)*c*z, mark)
    assert mod(f*transported-z, mark) == zeros(32)
    assert mod(f*(pow(n, -2, mark)*c*z)-z, mark) != zeros(32)
    return {"trace": 27, "multiplier": n, "quotient_primes": list(primes),
            "formal_checks": checks, "local_kernels": records,
            "marking_prime": mark, "common_mask_preserved": True,
            "wrong_squared_inverse_rejected": True,
            "geometric_points_generated": False, "quotient_executed": False}

"""Exact arithmetic controls with supplied maps/kernels; no geometric source."""

from math import prod
import sys

from sympy import Matrix, eye, zeros
from sympy.ntheory.modular import crt

from double_level_source import ROOT, checked_factors, lift_dyadic_split, split_at_two
from half_norm import half_certificate, verify_half_certificate
from local_baseline import (
    classical_local_direction, content_depth, kernel_ideal_from_local_data, local_frame,
)

sys.path.insert(0, str(ROOT / "cyclic-odd-degree-source-2026-10-25"))
sys.path.insert(0, str(ROOT / "source-pullback-2026-10-23"))
from controls_cyclic import split_fixture
from kernel_output import (
    action, alternating_form, inverse_mod, matrix_multiply, matrix_star, mod,
    odd_maximal_order, odd_maximal_split, product_actions,
)
from pullback import column_basis


def full_split_fixture(characteristic, n, factors):
    """Small odd-prime fixture plus actual dyadic algebra lifting."""
    factors = checked_factors(n, factors)
    order, moduli, components = odd_maximal_order(characteristic), [], []
    for p, e in factors:
        m = p**e
        if p == 2:
            split, precision = split_at_two(order), 2
            while precision < m:
                split = lift_dyadic_split(order, split, precision)
                precision *= 2
        else:
            split = split_fixture(characteristic, m, ((p, e),))
        moduli.append(m)
        components.append(split)
    return tuple(Matrix(2, 2, [int(crt(moduli, [part[i][j] for part in components])[0])
                              for j in range(4)]) for i in range(4))


def preserves_kernel(query, p, e, a, vector):
    if type(a) is not int or not 0 <= 2*a <= e:
        raise ValueError("valid Smith content exponent required")
    frame = local_frame(vector, p, e)
    change = Matrix.diag(frame, frame)
    divisors = (p**a, p**(e-a), p**a, p**(e-a))
    generators = change*Matrix.diag(*divisors)
    moved = mod(inverse_mod(change, p**e)*Matrix(query)*generators, p**e)
    return all(int(moved[i, j]) % divisors[i] == 0 for i in range(4) for j in range(4))


def classical_control(p, e, a, vector):
    equal = lambda query: preserves_kernel(query, p, e, a, vector)
    content = content_depth(p, e, equal)
    assert content["content_exponent"] == a
    direction = None
    if content["depth"]:
        direction = classical_local_direction(p, e, content["depth"], equal)
        x, y = direction["vector"]
        assert (x*int(vector[1])-y*int(vector[0])) % (p**content["depth"]) == 0
    return {"prime": p, "exponent": e, "content": content, "direction": direction,
            "supplied_kernel_control": True, "native_source_executed": False,
            "quantum_execution": False, "speedup_established": False}


def even_isogeny_control():
    """phi=1+i, degree2, with an integral half-polarization and odd kernels."""
    order, n = odd_maximal_order(11), 2
    unit, i = order.unit, eye(4)[:, 1]
    j = 2*eye(4)[:, 2]-unit
    alpha = unit+i
    assert order.multiply(order.star(alpha), alpha) == n*unit
    zero = zeros(4, 1)
    identity = Matrix.vstack(unit, zero, zero, unit)
    phi = Matrix.vstack(alpha, zero, zero, alpha)
    sigma = Matrix.vstack(unit, 2*n*j, zero, unit)
    s = matrix_multiply(order, matrix_star(order, sigma), sigma)
    h = matrix_multiply(order, matrix_multiply(order, phi, s), matrix_star(order, phi))/n
    half = (h-identity)/2
    assert all(x.q == 1 for x in half)
    t = int((order.traces*(h[:4, :]+h[12:, :]))[0]/2)
    assert t == 178
    assert matrix_multiply(order, half, half) == ((t-2)//4)*h
    primes = (3, 5, 7, 13, 17)
    d = prod(primes)
    certificate = half_certificate(t, d)
    assert all(verify_half_certificate(certificate).values())
    records = []
    for r in primes+(19,):
        split = product_actions(odd_maximal_split(11, r))
        hr, ar, sr = (mod(action(x, split), r) for x in (h, half, s))
        weak = mod(2*action(phi, split), r)
        assert mod(weak*sr*inverse_mod(weak, r)-hr, r) == zeros(4)
        assert mod(2*ar+eye(4)-hr, r) == zeros(4)
        c, f = (mod(Matrix.vstack(*[
            Matrix.hstack(*[entry.u*eye(4)+entry.v*ar for entry in row])
            for row in certificate[k]
        ]), r) for k in ("C", "F"))
        form, h8 = alternating_form(16), Matrix.diag(*([hr]*8))
        assert mod(f*c-d*eye(32), r) == zeros(32)
        assert mod(c*f-d*eye(32), r) == zeros(32)
        assert mod(f.T*form*h8*f-d*form, r) == zeros(32)
        if r in primes:
            kernel = column_basis(c, r)
            assert kernel.cols == column_basis(f, r).cols == 16
            assert mod(f*kernel, r) == zeros(32, 16)
            assert mod(kernel.T*form*kernel, r) == zeros(16)
            records.append({"prime": r, "kernel_dimension": 16, "isotropic": True,
                            "nonsemisimple": (t*t-4) % r == 0})
    return {"degree": n, "trace": t, "half_parameter": (t-2)//4, "multiplier": d,
            "local_kernels": records, "integral_half_polarization": True,
            "weak_query_orders": list(primes+(19,)),
            "supplied_map_not_recovered": True, "geometric_quotients_executed": False,
            "torsion_points_generated": False}


def mixed_even_ideal_control():
    """Supplied phi=2(1+i)(3+4i), degree200, not an unknown-kernel recovery."""
    order, n, factors = odd_maximal_order(11), 200, ((2, 3), (5, 2))
    i, unit = eye(4)[:, 1], order.unit
    psi = order.multiply(unit+i, 3*unit+4*i)
    phi = 2*psi
    assert order.multiply(order.star(phi), phi) == n*unit
    actions = full_split_fixture(11, n, factors)
    two_action = mod(action(psi, actions), 2)
    v2 = next(v for v in ((1, 0), (0, 1), (1, 1))
              if mod(two_action*Matrix(v), 2) == zeros(2, 1))
    directions = {2: v2, 5: (4, 3)}
    assert mod(action(psi, actions)*Matrix(directions[5]), 25) == zeros(2, 1)
    ideal = kernel_ideal_from_local_data(order, actions, n, factors, {2: 1, 5: 0}, directions)
    principal = Matrix.hstack(*[order.multiply(eye(4)[:, i], phi) for i in range(4)])
    assert abs(principal.det()) == abs(ideal.det()) == n*n
    assert all(x.q == 1 for x in ideal.inv()*principal)
    assert all(x.q == 1 for x in principal.inv()*ideal)
    return {"degree": n, "scalar_content": 2, "residual_degree": 50,
            "ideal_index": int(abs(ideal.det())),
            "ideal_equals_original_principal_left_ideal": True,
            "dyadic_direction": list(v2), "odd_direction": [4, 3],
            "supplied_map_not_recovered": True, "geometric_execution": False}

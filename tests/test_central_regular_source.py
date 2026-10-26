"""Ordinary coset-to-central-sector controls, not new oracle candidates."""

from itertools import product

import numpy as np
import pytest

from theorems.class_three_monomial_jet import ClassThreeStructure


def _fixture(family):
    if family == "class_three":
        p, width, carrier_width = 5, 4, 3
        structure = ClassThreeStructure(
            p, (((0, 1), (p-1, 0)),), (((0, 1), (p-1, 0)),), (((1,), (0,)),))
        def multiply(a, b):
            parts = structure.multiply_fixture((a[:2], a[2:3], a[3:]),
                                               (b[:2], b[2:3], b[3:]))
            return parts[0]+parts[1]+parts[2]
        def inverse(a):
            return tuple(-x % p for x in a)
        generator, twist = (1, 1, 2, 1), (0, 1, 0, 0)
    elif family == "vector_center":
        p, width, carrier_width = 3, 4, 2
        def multiply(a, b):
            x, y, z, w = a
            u, v, c, d = b
            return ((x+u) % p, (y+v) % p, (z+c+x*v) % p, (w+d) % p)
        def inverse(a):
            x, y, z, w = a
            return (-x % p, -y % p, (-z+x*y) % p, -w % p)
        generator, twist = (1, 1, 1, 2), (0, 1, 0, 0)
    else:
        p, width, carrier_width = 3, 3, 1
        def multiply(a, b):
            return tuple((x+y) % p for x, y in zip(a, b))
        def inverse(a):
            return tuple(-x % p for x in a)
        generator, twist = (1, 1, 2), (2, 0, 1)
    normal = list(product(range(p), repeat=width))
    powers, twists = [(0,)*width], [(0,)*width]
    for _ in range(p-1):
        powers.append(multiply(powers[-1], generator))
        twists.append(multiply(twists[-1], twist))
    assert multiply(powers[-1], generator) == (0,)*width
    assert multiply(twists[-1], twist) == (0,)*width
    return p, carrier_width, normal, multiply, inverse, powers, twists


@pytest.mark.parametrize("family", ["class_three", "vector_center", "abelian"])
def test_ordinary_hiding_source_has_complete_uniform_reducible_central_sectors(family):
    p, split, normal, multiply, inverse, powers, twists = _fixture(family)
    quotient = list(product(range(p), repeat=2))
    center = list(product(range(p), repeat=len(normal[0])-split))
    carriers = list(product(range(p), repeat=split))
    carrier_index = {x: i for i, x in enumerate(carriers)}
    omega, order, dim = np.exp(2j*np.pi/p), len(normal), len(carriers)

    # G=N x F_p^2; H={(h^u,(u,0))}. Assign actual gH labels by right H action.
    # A nonlinear public normal-first section is used independently below.
    labels = {}
    for q, n in product(quotient, normal):
        if (q, n) in labels:
            continue
        label = len(labels)//p
        for u, h in enumerate(powers):
            key = (((q[0]+u) % p, q[1]), multiply(n, h))
            assert key not in labels
            labels[key] = label
    assert len(labels) == len(quotient)*order
    def section(q):
        return twists[q[0]*q[1] % p]
    label_rows = {q: np.array([labels[(q, multiply(n, section(q)))] for n in normal])
                  for q in quotient}
    assert all(len(set(row)) == order for row in label_rows.values())

    transform, wrong = [np.zeros((order, order), dtype=complex) for _ in range(2)]
    for j, n in enumerate(normal):
        inv = inverse(n)
        for k, chi in enumerate(center):
            transform[k*dim+carrier_index[inv[:split]], j] = (
                omega**(sum(a*b for a, b in zip(chi, inv[split:])) % p)/np.sqrt(len(center)))
            wrong[k*dim+carrier_index[n[:split]], j] = (
                omega**(sum(a*b for a, b in zip(chi, n[split:])) % p)/np.sqrt(len(center)))
    np.testing.assert_allclose(transform.conj().T @ transform, np.eye(order), atol=2e-13)

    def potential(q, projection):
        u = (q[0]+projection*q[1]) % p
        base = ((q[0]-u) % p, q[1])
        return multiply(multiply(section(base), powers[u]), inverse(section(q)))
    def sector(chi, g):
        result = np.zeros((dim, dim), dtype=complex)
        for j, x in enumerate(carriers):
            out = multiply(g, x+(0,)*len(center[0]))
            result[carrier_index[out[:split]], j] = (
                omega**(sum(a*b for a, b in zip(chi, out[split:])) % p))
        return result

    group_order = len(quotient)*order
    saw_wrong_inversion = False
    for q, r in [((0, 1), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (2, 1)), ((0, 1), (1, 2))]:
        # This equality table is the actual trace of the uniform-query
        # hiding-output register. It is not supplied as a potential oracle.
        raw = (label_rows[q][:, None] == label_rows[r][None, :])/group_order
        actual = transform @ raw @ transform.conj().T
        incorrect = wrong @ raw @ wrong.conj().T
        for k, chi in enumerate(center):
            addresses = slice(k*dim, (k+1)*dim)
            block = actual[addresses, addresses]
            for projection in (0, 1):
                g = multiply(inverse(potential(q, projection)), potential(r, projection))
                expected = sector(chi, g)/group_order if q[1] == r[1] else np.zeros((dim, dim))
                np.testing.assert_allclose(block, expected, atol=2e-13)
            for ell in range(len(center)):
                if ell != k:
                    np.testing.assert_allclose(actual[addresses, ell*dim:(ell+1)*dim], 0, atol=2e-13)
            if q == r:
                # Every q-diagonal block is identical, as verified by the
                # injective label rows. Sum ALL q, not just one coset.
                mass = len(quotient)*np.trace(block).real
                assert mass == pytest.approx(1/len(center))
                assert mass != pytest.approx(dim*dim/order)
            saw_wrong_inversion |= np.linalg.norm(incorrect[addresses, addresses]-expected) > 1e-6
    assert saw_wrong_inversion
    assert len(center)*(1/len(center)) == pytest.approx(1)


def test_nontransverse_hidden_center_invalidates_uniform_label_claim():
    p = 3
    elements = list(product(range(p), repeat=3))
    labels = list(product(range(p), repeat=2))
    omega = np.exp(2j*np.pi/p)
    # N=F_p^3 with carrier x and center (z,w); H={(0,z,0)}.
    # The actual gH equality table hides a NONTRIVIAL central intersection.
    raw = np.array([[float(a[0] == b[0] and a[2] == b[2])
                     for b in elements] for a in elements])/len(elements)
    transform = np.zeros((len(elements), len(elements)), dtype=complex)
    for j, (x, z, w) in enumerate(elements):
        for k, (lam, mu) in enumerate(labels):
            transform[k*p+(-x % p), j] = omega**((-lam*z-mu*w) % p)/p
    actual = transform @ raw @ transform.conj().T
    masses = [np.trace(actual[k*p:(k+1)*p, k*p:(k+1)*p]).real for k in range(len(labels))]
    expected = [1/p if lam == 0 else 0 for lam, _ in labels]
    np.testing.assert_allclose(masses, expected, atol=1e-13)
    assert not np.allclose(masses, np.full(len(labels), 1/len(labels)))
    assert sum(masses) == pytest.approx(1)

"""Independent source/sign controls and exact public-controller falsifiers.

Small dense matrices appear ONLY in reference tests. No hidden coefficients
or oracle truth are passed to align_public_jets.
"""
from dataclasses import replace
from itertools import product
from math import factorial
import random

import numpy as np
import pytest
import sympy as sp

from theorems.affine_phase_channel_audit import coset_mixture
from theorems.affine_phase_erasure import square_weights
from theorems.ut5_matrix_phase_alignment import (
    align_public_jets, public_jet_maps, symplectic_pair, verify_alignment,
)
from theorems.ut5_scalar_phase_compiler import compile_scalar_packet


def matvec(matrix, vector, p):
    return [sum(a*b for a, b in zip(row, vector)) % p for row in matrix]


def batch(p, r, m, seed):
    rng = random.Random(seed)
    labels, scales = [], []
    for _ in range(m+3):
        block = [[rng.randrange(1, p) for _ in range(r)]
                 for _ in range((r+1)**2)]
        beta = square_weights(p, block, rng)
        multiplier = rng.randrange(1, p)
        scales.extend(multiplier*pow(b, (p+1)//4, p) % p for b in beta)
        labels.extend(block)
    assert len({s for s in scales if s}) > 1
    outcomes = [[rng.randrange(p) for _ in range(m)] for _ in labels]
    return labels, scales, outcomes


def exp_matrix(value, p):
    result = np.eye(5, dtype=object)
    power = result.copy()
    for k in range(1, 5):
        power = power @ value % p
        result = (result+pow(factorial(k), -1, p)*power) % p
    return result


def section(q):
    matrix = np.zeros((5, 5), dtype=object)
    for i, x in enumerate(q):
        matrix[i, i+1] = x
    return matrix


def potential(q, p, hidden=None):
    hidden = section([1]*4) if hidden is None else hidden
    remainder = [(x-q[0]) % p for x in q]
    return (exp_matrix(section(remainder), p) @ exp_matrix(q[0]*hidden, p) @
            exp_matrix(-section(q), p)) % p


def heisenberg_rep(p, lam, a, b, z):
    matrix = np.zeros((p, p), dtype=complex)
    for j in range(p):
        matrix[(j+b) % p, j] = np.exp(2j*np.pi*((lam*(z+a*j)) % p)/p)
    return matrix


def weyl(p, x, z):
    matrix = np.zeros((p, p), dtype=complex)
    for j in range(p):
        phase = (x*z*pow(2, -1, p)+z*j) % p
        matrix[(j+x) % p, j] = np.exp(2j*np.pi*phase/p)
    return matrix


def test_ut5_normal_factor_and_actual_potential_degree():
    q = sp.symbols("q0:4")
    X = sp.zeros(5)
    for i in range(4):
        X[i, i+1] = q[i]
    H = X.subs(dict.fromkeys(q, 1))
    remainder = X-q[0]*H

    def exp(value):
        return sum((value**k/sp.factorial(k) for k in range(1, 5)), sp.eye(5))

    F = (exp(remainder)*exp(q[0]*H)*exp(-X)).applyfunc(sp.expand)
    Z = F-sp.eye(5)
    Q = (Z-Z**2/2).applyfunc(sp.expand)
    assert sp.expand(Q[0, 2]-q[0]*(q[0]-q[1])/2) == 0
    assert sp.expand(Q[2, 4]-q[0]*(q[2]-q[3])/2) == 0
    coordinates = [(0, 2), (2, 4), (0, 3), (1, 3), (1, 4), (0, 4)]
    degrees = [sp.Poly(Q[i, j], *q).total_degree() for i, j in coordinates]
    assert max(degrees[:2]) == 2
    assert max(degrees[2:]) == 4
    E13, E35 = sp.zeros(5), sp.zeros(5)
    E13[0, 2], E35[2, 4] = 1, 1
    assert (E13*E35-E35*E13)[0, 4] == 1


@pytest.mark.parametrize("p", [5, 7])
def test_actual_group_increment_and_weyl_log_convention(p):
    rng = random.Random(p)
    H = section([1]*4)
    H[0, 2], H[2, 4], H[0, 4] = 1, 2, 3
    for _ in range(20):
        q, t = [rng.randrange(p) for _ in range(4)], rng.randrange(p)
        qp = [(x+t) % p for x in q]
        F, Fp = potential(q, p, H), potential(qp, p, H)
        inverse = np.eye(5, dtype=object)
        Z = F-np.eye(5, dtype=object)
        for k in range(1, 5):
            inverse = (inverse+(-1)**k*np.linalg.matrix_power(Z, k)) % p
        delta = inverse @ Fp % p
        assert np.array_equal(exp_matrix(section(q), p) @ exp_matrix(t*H, p) % p,
                              delta @ exp_matrix(section(qp), p) % p)
        lam = rng.randrange(1, p)
        mu = [rng.randrange(p) for _ in range(3)]
        def central_phase(g):
            return sum(c*int(g[i, j]) for c, (i, j) in zip(mu, ((0, 3), (1, 3), (1, 4)))) % p
        def rho(g):
            return (np.exp(2j*np.pi*central_phase(g)/p)*
                    heisenberg_rep(p, lam, int(g[0, 2]), int(g[2, 4]), int(g[0, 4])))
        np.testing.assert_allclose(rho(F).conj().T @ rho(Fp), rho(delta), atol=1e-13)
        a, b, z = [int(F[i, j]) for i, j in ((0, 2), (2, 4), (0, 4))]
        c = (z-a*b*pow(2, -1, p)) % p
        np.testing.assert_allclose(rho(F), np.exp(2j*np.pi*((lam*c+central_phase(F)) % p)/p)*weyl(p, b, lam*a % p), atol=1e-13)


def test_explicit_normal_qft_is_unitary_and_has_the_active_kernel_orientation():
    p = 5
    normal = list(product(range(p), repeat=3))
    output = ([(lam, i, j) for lam in range(1, p) for i, j in product(range(p), repeat=2)] +
              [(0, a, b) for a, b in product(range(p), repeat=2)])
    fourier = np.zeros((p**3, p**3), dtype=complex)
    for row, (lam, i, j) in enumerate(output):
        for col, (a, b, z) in enumerate(normal):
            if lam:
                if i == (j+b) % p:
                    fourier[row, col] = np.exp(-2j*np.pi*((lam*(z+a*j)) % p)/p)/p
            else:
                fourier[row, col] = np.exp(-2j*np.pi*((i*a+j*b) % p)/p)/p**1.5
    np.testing.assert_allclose(fourier @ fourier.conj().T, np.eye(p**3), atol=1e-13)
    lam, delta = 2, (1, 3, 4)
    reps, shifted = [], []
    for a, b, z in normal:
        reps.append(heisenberg_rep(p, lam, a, b, z))
        ap, bp, zp = delta
        shifted.append(heisenberg_rep(p, lam, (a+ap) % p, (b+bp) % p, (z+zp+a*bp) % p))
    actual = np.einsum("nij,nkl->ijkl", np.array(reps).conj(), shifted)/p**3
    expected = np.einsum("ik,jl->ijkl", np.eye(p), heisenberg_rep(p, lam, *delta))/p
    np.testing.assert_allclose(actual, expected, atol=1e-13)
    # Plancherel central lambda is uniform, including the p^2 one-dimensional irreps.
    masses = [sum((p if lam else 1)**2/p**3 for lam0, i, j in output
                  if lam0 == lam and (not lam or (i == 0 and j == 0)))
              for lam in range(p)]
    np.testing.assert_allclose(masses, [1/p]*p)
    # Without H intersect N=1 the label law is not Plancherel: H=Z kills all
    # nonzero central labels. No extension to arbitrary H is licensed here.
    central_cosets = np.array([[int(a == ap and b == bp)/p**3
                               for ap, bp, zp in normal] for a, b, z in normal])
    transformed = fourier @ central_cosets @ fourier.conj().T
    assert np.trace(transformed[:(p-1)*p*p, :(p-1)*p*p]) == pytest.approx(0, abs=1e-13)
    assert np.trace(transformed) == pytest.approx(1)


@pytest.mark.parametrize("r,m,seed", [(1, 4, 17), (1, 4, 29), (2, 8, 37)])
def test_public_alignment_is_symplectic_and_canonical(r, m, seed):
    p = 7
    labels, scales, outcomes = batch(p, r, m, seed)
    alignment = align_public_jets(p, labels, scales, outcomes)
    assert verify_alignment(alignment)
    assert alignment.maps.jet_width == 2*r*(m+1)
    assert len(alignment.maps.active_indices) >= 2*(m+3)
    K = list(zip(*alignment.maps.quadratic))
    assert all(symplectic_pair(v, w, p) == 0 for v, w in product(K, repeat=2))
    broken = [list(row) for row in alignment.symplectic]
    broken[0][0] = (broken[0][0]+1) % p
    assert not verify_alignment(replace(alignment, symplectic=tuple(map(tuple, broken))))


def test_independent_batches_preserve_the_same_unknown_jet_not_random_slopes():
    p, r, m = 7, 1, 4
    rng = random.Random(91)
    linear = [[rng.randrange(p) for _ in range(m)] for _ in range(2*r)]
    hessian = []
    for _ in range(2*r):
        matrix = [[rng.randrange(p) for _ in range(m)] for _ in range(m)]
        hessian.append([[(matrix[i][j]+matrix[j][i]) % p for j in range(m)] for i in range(m)])
    constant = [rng.randrange(p) for _ in range(2*r)]
    T = linear + [hessian[c][j] for j in range(m) for c in range(2*r)]

    def Q(q):
        return [(constant[c]+sum(a*b for a, b in zip(linear[c], q))+
                 pow(2, -1, p)*sum(hessian[c][j][k]*q[j]*q[k] for j, k in product(range(m), repeat=2))) % p
                for c in range(2*r)]

    for seed in (17, 29):
        labels, scales, outcomes = batch(p, r, m, seed)
        alignment = align_public_jets(p, labels, scales, outcomes)
        R, D = alignment.maps.carrier_width, alignment.maps.jet_width

        def displacement(q):
            x, z = [], []
            for i in alignment.maps.active_indices:
                value = Q([(y+scales[i]*v) % p for y, v in zip(outcomes[i], q)])
                x.extend(value[:r])
                z.extend(labels[i][j]*value[r+j] % p for j in range(r))
            return matvec(alignment.symplectic, x+z, p)

        origin = displacement([0]*m)
        for _ in range(30):
            q = [rng.randrange(p) for _ in range(m)]
            actual = [(x-y) % p for x, y in zip(displacement(q), origin)]
            assert actual[:D] == matvec(T, q, p)
            assert actual[D:R] == [0]*(R-D)


def test_full_carrier_measurement_fails_but_retained_linear_support_is_scalar():
    p, R = 5, 2
    omega = np.exp(2j*np.pi/p)

    def gauge(q):
        A, B, psi = [2*q+1, 3], [q*q+q, 3*q*q], q**4+2*q
        return omega**(psi % p)*np.kron(weyl(p, A[0] % p, B[0] % p), weyl(p, A[1], B[1] % p))

    W = [gauge(q) for q in range(p)]
    density = np.block([[a.conj().T @ b for b in W] for a in W])/p**(1+R)
    assert np.trace(density) == pytest.approx(1)
    assert np.linalg.eigvalsh(density).min() > -1e-13
    for spectator in range(p):
        addresses = [q*p*p+r*p+spectator for q, r in product(range(p), repeat=2)]
        branch = density[np.ix_(addresses, addresses)]
        assert np.trace(branch) == pytest.approx(1/p)
        phases = []
        for q, r in product(range(p), repeat=2):
            A, B, psi = [2*q+1, 3], [q*q+q, 3*q*q], q**4+2*q
            phi = psi+pow(2, -1, p)*sum(a*b for a, b in zip(A, B))
            phases.append((-phi-B[0]*r-B[1]*spectator) % p)
        expected = coset_mixture(p, 2, [(1, -2 % p)], phases)
        np.testing.assert_allclose(branch*p, expected, atol=1e-13)
    # Fixing both carrier coordinates instead loses all off-diagonal q terms.
    addresses = [q*p*p for q in range(p)]
    np.testing.assert_allclose(density[np.ix_(addresses, addresses)]*p**2, np.eye(p)/p, atol=1e-13)


@pytest.mark.parametrize("leaking_spectator", [False, True])
def test_proper_support_scalarization_and_spectator_leakage(leaking_spectator):
    # The channel identity is field-general. This small reference is not
    # a class-four HSP instance or a prime-scaling experiment.
    p = 3
    omega, half = np.exp(2j*np.pi/p), pow(2, -1, p)
    points = list(product(range(p), repeat=2))
    def components(q):
        x, y = q
        return [1+x+y, 1+int(leaking_spectator)*x], [x*x+y, x*y+1], x*y+y*y
    def gauge(q):
        A, B, psi = components(q)
        return omega**(psi % p)*np.kron(*(weyl(p, a % p, b % p) for a, b in zip(A, B)))
    gauges = [gauge(q) for q in points]
    density = np.block([
        [left.conj().T @ right if (q[0]-r[0]-q[1]+r[1]) % p == 0 else np.zeros((p*p, p*p))
         for r, right in zip(points, gauges)] for q, left in zip(points, gauges)])/p**4
    assert np.trace(density) == pytest.approx(1)
    assert np.linalg.eigvalsh(density).min() > -1e-13
    for s in range(p):
        addresses = [i*p*p+j*p+s for i in range(len(points)) for j in range(p)]
        branch = density[np.ix_(addresses, addresses)]
        assert np.trace(branch) == pytest.approx(1/p)
        phases = []
        for q in points:
            A, B, psi = components(q)
            for j in range(p):
                phases.append((-psi-half*sum(a*b for a, b in zip(A, B))-B[0]*j-B[1]*s) % p)
        intended = coset_mixture(p, 3, [(1, 1, -2 % p)], phases)
        if leaking_spectator:
            # Outcome probabilities remain uniform despite total loss of
            # the intended U direction. A trace check alone cannot catch it.
            np.testing.assert_allclose(branch*p, np.eye(p**3)/p**3, atol=1e-13)
            assert np.linalg.norm(branch*p-intended) > 0.1
        else:
            np.testing.assert_allclose(branch*p, intended, atol=1e-13)


def test_full_carrier_readout_keeps_only_the_kernel_of_a_noninjective_jet():
    p = 3
    omega, half = np.exp(2j*np.pi/p), pow(2, -1, p)
    points = list(product(range(p), repeat=2))
    def components(q):
        x, y = q
        return [1+x, 1], [x+y*y, x*y], x*x+y
    def gauge(q):
        A, B, psi = components(q)
        return omega**(psi % p)*np.kron(*(weyl(p, a % p, b % p) for a, b in zip(A, B)))
    gauges = [gauge(q) for q in points]
    density = np.block([[a.conj().T @ b for b in gauges] for a in gauges])/p**4
    for t in product(range(p), repeat=2):
        addresses = [i*p*p+t[0]*p+t[1] for i in range(len(points))]
        branch = density[np.ix_(addresses, addresses)]
        assert np.trace(branch) == pytest.approx(1/p**2)
        phases = []
        for q in points:
            A, B, psi = components(q)
            phases.append((-psi-half*sum(a*b for a, b in zip(A, B))-sum(b*j for b, j in zip(B, t))) % p)
        expected = coset_mixture(p, 2, [(0, 1)], phases)
        np.testing.assert_allclose(branch*p**2, expected, atol=1e-13)


def test_quartic_cancellation_does_not_make_all_displacement_coefficients_commute():
    p, m = 7, 4
    labels, scales, outcomes = batch(p, 1, m, 17)
    active = [i for i, s in enumerate(scales) if s]
    R, half = len(active), pow(2, -1, p)
    # Q_W=(q0*(q2-q3)/2, q0*(q0-q1)/2), from the real UT5 potential.
    quadratic = [0]*R + [labels[i][0]*scales[i]**2*half % p for i in active]
    source = active[0]
    pairings = []
    for value in range(p):
        outcomes[source][0] = value
        linear = [scales[i]*outcomes[i][0]*half % p for i in active]+[0]*R
        pairings.append(symplectic_pair(quadratic, linear, p))
    assert len(set(pairings)) == p
    assert pairings.count(0) == 1


@pytest.mark.parametrize("defect", ["zero_label", "bad_quartic", "constant_scale", "zero_outcomes"])
def test_public_invalid_sources_are_rejected(defect):
    p, r, m = 7, 1, 4
    labels, scales, outcomes = batch(p, r, m, 17)
    if defect == "zero_label":
        labels[0][0] = 0
    elif defect == "bad_quartic":
        source = next(i for i, s in enumerate(scales) if s)
        scales[source] = 0
    elif defect == "constant_scale":
        labels = [[1], [p-1]]*(m+3)
        scales = [1]*len(labels)
        outcomes = [[random.Random(i).randrange(p) for _ in range(m)] for i in range(len(labels))]
    else:
        outcomes = [[0]*m for _ in labels]
    with pytest.raises(ValueError):
        align_public_jets(p, labels, scales, outcomes)


def test_deterministic_alignment_and_large_prime_arithmetic():
    p, r, m = 2**127-1, 1, 1
    # Explicit cancelling pairs avoid the separate machine-word square backend.
    scales = [s for s in range(1, 5) for _ in range(2)]
    labels = [[x] for _ in range(4) for x in (1, p-1)]
    outcomes = [[i*i % p] for i in range(8)]
    result = align_public_jets(p, labels, scales, outcomes)
    assert verify_alignment(result)
    assert result == align_public_jets(p, labels, scales, outcomes)
    assert result.transvections <= 2*(2*r+result.maps.jet_width)


def test_insufficient_target_embedding_width_is_rejected():
    with pytest.raises(ValueError, match="carrier width"):
        align_public_jets(7, [[1], [6], [1], [6]], [1, 1, 2, 2], [[0], [1], [2], [4]])


def test_cubic_noncentral_terms_are_outside_the_alignment_guarantee():
    p, r, m = 7, 1, 4
    labels, scales, outcomes = batch(p, r, m, 17)
    alignment = align_public_jets(p, labels, scales, outcomes)
    R = alignment.maps.carrier_width
    # An illicit Q_W(q)=(q0^3,0) has no linear/quadratic jet at zero. The
    # resulting X displacement need not vanish: class-four structure matters.
    def displacement(t):
        x = [pow(outcomes[i][0]+scales[i]*t, 3, p) for i in alignment.maps.active_indices]
        return matvec(alignment.symplectic, x+[0]*R, p)[:R]
    origin = displacement(0)
    assert any(displacement(t) != origin for t in range(p))


def test_controller_has_no_hidden_truth_arguments():
    import inspect
    assert list(inspect.signature(align_public_jets).parameters) == [
        "p", "labels", "scales", "outcomes"]
    assert list(inspect.signature(compile_scalar_packet).parameters) == [
        "alignment", "labels", "scales", "outcomes", "central_characters", "spectator_outcome"]


@pytest.mark.parametrize("p,r,m", [(7, 1, 4), (11, 1, 4), (7, 2, 2)])
def test_public_symbolic_compiler_matches_unknown_gauges_in_independent_batches(p, r, m):
    rng = random.Random(57)
    previous_basis, theta = None, None
    for seed in (17, 29):
        labels, scales, outcomes = batch(p, r, m, seed)
        alignment = align_public_jets(p, labels, scales, outcomes)
        R, D = alignment.maps.carrier_width, alignment.maps.jet_width
        mu = [[rng.randrange(p) for _ in range(3*r)] for _ in labels]
        spectator = [rng.randrange(p) for _ in range(R-D)]
        packet = compile_scalar_packet(alignment, labels, scales, outcomes, mu, spectator)
        assert packet.degree == 3
        assert max(len(parameters) for _, parameters in packet.terms) == 2
        assert packet.lifted_parameter_count == 1+len(packet.parameter_basis)*(len(packet.parameter_basis)+3)//2
        if previous_basis is None:
            previous_basis = packet.parameter_basis
            theta = [rng.randrange(p) for _ in packet.parameter_basis]
        else:
            assert packet.parameter_basis == previous_basis

        def unknown_Q(q):
            value = [0]*(6*r)
            for (coordinate, alpha), coefficient in zip(packet.parameter_basis, theta):
                term = coefficient
                for x, exponent in zip(q, alpha):
                    term = term*pow(x, exponent, p) % p
                value[coordinate] = (value[coordinate]+term) % p
            return value

        for _ in range(12):
            q = [rng.randrange(p) for _ in range(m)]
            retained = [rng.randrange(p) for _ in range(D)]
            x, z, psi = [], [], 0
            for i in alignment.maps.active_indices:
                value = unknown_Q([(a+scales[i]*b) % p for a, b in zip(outcomes[i], q)])
                x.extend(value[:r])
                z.extend(labels[i][j]*value[r+j] % p for j in range(r))
                psi += sum(c*v for c, v in zip(labels[i]+mu[i], value[2*r:]))
            displacement = matvec(alignment.symplectic, x+z, p)
            A, B = displacement[:R], displacement[R:]
            expected = (-psi-pow(2, -1, p)*sum(a*b for a, b in zip(A, B))-
                        sum(b*t for b, t in zip(B, retained+spectator))) % p
            assert packet.evaluate_fixture(q+retained, theta) == expected


def test_ut5_weights_remove_scalar_quartics_with_the_same_public_cancellation():
    p, m = 7, 4
    labels, scales, outcomes = batch(p, 1, m, 17)
    alignment = align_public_jets(p, labels, scales, outcomes)
    spectator = [0]*(alignment.maps.carrier_width-alignment.maps.jet_width)
    packet = compile_scalar_packet(alignment, labels, scales, outcomes, [[1, 2, 3]]*len(labels), spectator)
    degrees = [2, 2, 4, 3, 2, 3]
    assert all(sum(alpha) <= degrees[c] for c, alpha in packet.parameter_basis)
    direction = next(j for j in range(m) if sum(
        label[0]*pow(s, 3, p)*y[j] for label, s, y in zip(labels, scales, outcomes)) % p)
    exponent = tuple(4*int(j == direction) for j in range(m))
    corner_quartic = packet.parameter_basis.index((2, exponent))
    # The hidden corner-quartic coefficient is not set to zero. Its q^4
    # coefficient cancels publicly, while translated lower terms survive.
    terms = [(alpha, value) for (alpha, parameter), value in packet.terms.items()
             if parameter == (corner_quartic,)]
    assert terms
    assert max(sum(alpha) for alpha, _ in terms) <= 3
    assert any(sum(alpha) == 3 for alpha, _ in terms)
    assert all(sum(alpha) <= 3 for alpha, _ in packet.terms)


def test_symbolic_packet_rejects_mismatched_public_transcript():
    labels, scales, outcomes = batch(7, 1, 4, 17)
    alignment = align_public_jets(7, labels, scales, outcomes)
    mu = [[1, 2, 3] for _ in labels]
    spectator = [0]*(alignment.maps.carrier_width-alignment.maps.jet_width)
    changed = [list(y) for y in outcomes]
    source = alignment.maps.active_indices[0]
    changed[source][0] = (changed[source][0]+1) % 7
    with pytest.raises(ValueError):
        compile_scalar_packet(alignment, labels, scales, changed, mu, spectator)
    with pytest.raises(ValueError, match="central"):
        compile_scalar_packet(alignment, labels, scales, outcomes, [[0]]*len(labels), spectator)
    with pytest.raises(ValueError, match="spectator"):
        compile_scalar_packet(alignment, labels, scales, outcomes, mu, spectator+[0])


def test_symbolic_phase_map_is_linear_in_the_lift_not_the_hidden_parameters():
    p = 7
    labels, scales, outcomes = batch(p, 1, 1, 9)
    alignment = align_public_jets(p, labels, scales, outcomes)
    mu = [[1, 2, 3] for _ in labels]
    spectator = [2]*(alignment.maps.carrier_width-alignment.maps.jet_width)
    packet = compile_scalar_packet(alignment, labels, scales, outcomes, mu, spectator)
    # A concrete mixed finite difference in theta kills any accidental
    # assumption of linearity in the unlifted hidden coefficients.
    mixed = [(alpha, pair, coefficient) for (alpha, pair), coefficient in packet.terms.items()
             if len(pair) == 2 and pair[0] != pair[1]]
    assert mixed
    left, right = mixed[0][1]
    a, b = [0]*len(packet.parameter_basis), [0]*len(packet.parameter_basis)
    a[left], b[right] = 1, 1
    combined = [x+y for x, y in zip(a, b)]
    rng = random.Random(1)
    differences = []
    for _ in range(30):
        point = [rng.randrange(p) for _ in range(packet.width)]
        differences.append((packet.evaluate_fixture(point, combined)-packet.evaluate_fixture(point, a)-
                            packet.evaluate_fixture(point, b)) % p)
    assert any(differences)


@pytest.mark.parametrize("scales", [(1, 2), (1, 0)])
@pytest.mark.parametrize("full_support", [True, False])
def test_matrix_source_shear_has_uniform_outcomes_without_rare_postselection(scales, full_support):
    p = 5
    omega = np.exp(2j*np.pi/p)
    gauges = [[omega**((j+1)*q**3 % p)*weyl(p, (q*q+j*q) % p, ((j+2)*q*q+1) % p)
               for q in range(p)] for j in range(2)]
    sources = [np.block([[a.conj().T @ b if full_support or q == qp else np.zeros((p, p))
                         for qp, b in enumerate(W)] for q, a in enumerate(W)])/p**2
               for W in gauges]
    source = np.kron(*sources)
    for Y in product(range(p), repeat=2):
        addresses = []
        for q, c0, c1 in product(range(p), repeat=3):
            q0, q1 = [(y+s*q) % p for y, s in zip(Y, scales)]
            addresses.append((q0*p+c0)*p*p+q1*p+c1)
        branch = source[np.ix_(addresses, addresses)]/p
        assert np.trace(branch) == pytest.approx(1/p**2)
        if Y in ((0, 0), (1, 3), (4, 2)):
            combined = [np.kron(*(W[(y+s*q) % p] for W, y, s in zip(gauges, Y, scales)))
                        for q in range(p)]
            expected = np.block([[a.conj().T @ b if full_support or q == qp else np.zeros((p*p, p*p))
                                  for qp, b in enumerate(combined)] for q, a in enumerate(combined)])/p**3
            np.testing.assert_allclose(branch*p*p, expected, atol=1e-13)


def test_symbolic_compiler_matches_actual_ut5_matrix_potentials():
    p, m = 7, 4
    labels, scales, outcomes = batch(p, 1, m, 17)
    alignment = align_public_jets(p, labels, scales, outcomes)
    R, D = alignment.maps.carrier_width, alignment.maps.jet_width
    mu = [[1, 2, 3] for _ in labels]
    spectator = [i % p for i in range(R-D)]
    packet = compile_scalar_packet(alignment, labels, scales, outcomes, mu, spectator)
    q = sp.symbols("q0:4")
    X = sp.Matrix(section(q).tolist())
    H = section([1]*4)
    H[0, 2], H[2, 4] = 1, 2
    symbolic_H = sp.Matrix(H.tolist())
    def exp(value):
        return sum((value**k/sp.factorial(k) for k in range(1, 5)), sp.eye(5))
    remainder = X-q[0]*sp.Matrix(section([1]*4).tolist())
    F = (exp(remainder)*exp(q[0]*symbolic_H)*exp(-X)).applyfunc(sp.expand)
    Z = F-sp.eye(5)
    Q = (Z-Z**2/2).applyfunc(sp.expand)
    coordinates = [(2, 4), (0, 2), (0, 4), (0, 3), (1, 3), (1, 4)]
    polynomials = [sp.Poly(Q[i, j], *q) for i, j in coordinates]
    theta = []
    for coordinate, alpha in packet.parameter_basis:
        coefficient = polynomials[coordinate].coeff_monomial(alpha)
        num, den = coefficient.as_numer_denom()
        theta.append(int(num)*pow(int(den), -1, p) % p)
    rng = random.Random(18)
    for _ in range(12):
        point = [rng.randrange(p) for _ in range(m+D)]
        x, z, psi = [], [], 0
        for i in alignment.maps.active_indices:
            value = potential([(y+scales[i]*a) % p for y, a in zip(outcomes[i], point[:m])], p, H)
            a, b, corner = [int(value[j, k]) for j, k in ((0, 2), (2, 4), (0, 4))]
            x.append(b)
            z.append(labels[i][0]*a % p)
            psi += labels[i][0]*(corner-a*b*pow(2, -1, p))
            psi += sum(character*int(value[j, k]) for character, (j, k) in zip(mu[i], coordinates[3:]))
        displacement = matvec(alignment.symplectic, x+z, p)
        A, B = displacement[:R], displacement[R:]
        expected = (-psi-pow(2, -1, p)*sum(a*b for a, b in zip(A, B))-
                    sum(b*t for b, t in zip(B, point[m:]+spectator))) % p
        assert packet.evaluate_fixture(point, theta) == expected

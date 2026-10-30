"""Decisive shadow-structure controls, not a general quaternion decoder.

CT access to actual finite amplitudes is an input to this investigation.
No generic CT-overlap proof is repeated here. The native fixture uses the
Lipschitz order, norm-25 generators 5 and 3+4i, and on-grid straddle packets.
Its finite coefficient law is the centered, bin-integrated conditional
sampler from the source note (orthogonal bases make its factors independent).
The tests do not claim a growing-dimensional backend or a hardness reduction.
mpmath calculations are numerical controls, not interval certificates.
"""

from itertools import permutations

import mpmath as mp
import numpy as np
import sympy as sp


RIGHT_ALPHA = sp.Matrix([
    [3, -4, 0, 0],
    [4, 3, 0, 0],
    [0, 0, 3, 4],
    [0, 0, -4, 3],
])


def _anf_degree(table):
    coefficients = list(table)
    bits = (len(table) - 1).bit_length()
    assert len(table) == 1 << bits
    for bit in range(bits):
        for mask in range(1 << bits):
            if mask & (1 << bit):
                coefficients[mask] ^= coefficients[mask ^ (1 << bit)]
    return max(mask.bit_count() for mask, value in enumerate(coefficients) if value)


def _finite_bin_probabilities(width=32, cutoff=6):
    half_count = int(mp.ceil(width * cutoff)) + 2
    scale = mp.sqrt(mp.pi) / width

    def mass(left, right):
        if left >= 0:
            return (mp.erfc(scale * left) - mp.erfc(scale * right)) / 2
        if right <= 0:
            return (mp.erfc(-scale * right) - mp.erfc(-scale * left)) / 2
        return (mp.erf(scale * right) - mp.erf(scale * left)) / 2

    root = mass(-half_count - mp.mpf("0.5"), half_count + mp.mpf("0.5"))
    probabilities = {
        z: mass(z - mp.mpf("0.5"), z + mp.mpf("0.5")) / root
        for z in range(-half_count, half_count + 1)
    }
    return half_count, probabilities


def test_native_dense_stabilizer_phase_has_unbounded_carry_degree():
    assert RIGHT_ALPHA.T * RIGHT_ALPHA == 25 * sp.eye(4)
    assert RIGHT_ALPHA[:, 0] == sp.Matrix([3, 4, 0, 0])
    assert RIGHT_ALPHA.det() == 25**2
    rotation = RIGHT_ALPHA / 5
    grid_bits = 40
    spacing = sp.Rational(1, 5 * 2**grid_bits)
    assert rotation / spacing == 2**grid_bits * RIGHT_ALPHA

    # Z on bit grid_bits+j of the first coordinate of |+>^q is a
    # FULL-support stabilizer. Along z=(n,0,0,0), its phase is bit_j(3*n).
    # Uniform proof in the Boolean ring: c_2=n_0*n_1 and
    # c_(j+1)=n_j*n_(j-1)+c_j*(n_j+n_(j-1)). If c_j has top monomial
    # product_(i<j) n_i, only n_j*c_j can contribute product_(i<=j) n_i;
    # the other terms have degree <=j. This proves deg(c_j)=j inductively.
    # bit_j(3*n)=n_j+n_(j-1)+c_j thus has degree j for every j>=2.
    for j in range(1, 9):
        table = [((3 * n) >> j) & 1 for n in range(1 << (j + 1))]
        assert _anf_degree(table) == j
        if j >= 2:
            for n in range(1 << (j + 2)):
                carry = (n & 1) * ((n >> 1) & 1)
                for bit in range(2, j + 1):
                    left, right = (n >> bit) & 1, (n >> (bit - 1)) & 1
                    carry = (left * right) ^ (carry * (left ^ right))
                actual = ((3*n) >> (j + 1)) & 1
                assert actual == (((n >> (j + 1)) & 1) ^ ((n >> j) & 1) ^ carry)
    # This refutes a quadratic pullback, not efficient evaluation by every method.


def test_binary_affine_support_is_not_an_integer_lattice_coset():
    support = {n for n in range(8) if n.bit_count() % 2 == 0}
    assert support == {0, 3, 5, 6}
    assert all(x ^ y in support for x in support for y in support)
    assert (3 + 3) % 8 in support
    assert (3 + 5) % 8 in support
    assert (5 + 5) % 8 not in support
    # A residue-class lattice coset containing zero would be a subgroup.
    assert sp.gcd(3, 5) == 1


def test_even_one_binary_phase_is_not_an_arithmetic_quadratic_chirp():
    phases = [(-1) ** ((n >> 2) & 1) for n in range(8)]
    # Any exp(i*(a*n*n+b*n+c)) has multiplicative third difference one.
    third_difference = phases[4] * phases[2]**3 / (phases[3]**3 * phases[1])
    assert third_difference == -1
    # Keeping digits as variables DOES leave an ordinary Gaussian exponent
    # quadratic; the Boolean domain and weighted sum remain, not a theta sum.
    bits = sp.symbols("b0:4")
    coordinate = sum(2**j * bit for j, bit in enumerate(bits))
    assert sp.Poly(coordinate**2, *bits).total_degree() == 2


def test_exponentially_small_amplitude_error_can_change_score_by_one():
    dimension = sp.Integer(2)**100
    amplitude0 = 1 / sp.sqrt(dimension)
    amplitude1 = sp.sqrt(2) / sp.sqrt(dimension)
    score0 = (dimension + 1) * amplitude0**2 - 1
    score1 = (dimension + 1) * amplitude1**2 - 1
    assert amplitude1 - amplitude0 < sp.Rational(1, 2)**50
    assert score1 - score0 == 1 + 1 / dimension
    assert score1 - score0 > 1
    assert amplitude1**2 - amplitude0**2 == 1 / dimension


def test_sparse_marginal_does_not_make_full_scaled_projector_sparse():
    qubits = 6
    for measured in (2, qubits):
        block = np.ones((2**measured, 2**measured)) / 2**measured
        projector = np.kron(block, np.eye(2**(qubits - measured)))
        assert np.all(np.count_nonzero(projector, axis=1) == 2**measured)
        assert np.allclose(projector @ projector, projector)
        if measured == qubits:
            dimension = 2**qubits
            score_operator = (dimension + 1) * projector - np.eye(dimension)
            assert np.isclose(np.linalg.eigvalsh(score_operator)[-1], dimension)
            assert np.all(np.count_nonzero(score_operator, axis=1) == dimension)


def test_native_two_orientation_subclass_has_a_bounded_diagonal_decoder():
    # Both ideals have reduced norm 25: O*5 and O*(3+4i). With grid spacing
    # 1/(5*2^40), straddle centers are exactly grid labels. Integrality in
    # physical coordinates is an efficiently computable diagonal predicate.
    with mp.workdps(85):
        half_count, probabilities = _finite_bin_probabilities()
        residues = [mp.fsum(p for z, p in probabilities.items() if z % 5 == j)
                    for j in range(5)]
        assert abs(mp.fsum(probabilities.values()) - 1) < mp.mpf("1e-80")
        assert all(p > 0 for p in probabilities.values())
        assert max(abs(p - mp.mpf(1)/5) for p in residues) < mp.mpf("1e-45")

        pair01 = mp.fsum(residues[z] * residues[(2*z) % 5] for z in range(5))
        pair23 = mp.fsum(residues[z] * residues[(3*z) % 5] for z in range(5))
        integer_probability = pair01 * pair23
        assert abs(integer_probability - mp.mpf(1)/25) < mp.mpf("1e-44")
        # In orientation zero the predicate is identically one. In orientation
        # one this is its probability, and an upper bound on cross fidelity.
        assert integer_probability < mp.mpf("0.041")
        assert integer_probability**6 < mp.mpf("5e-9")
        assert (2*half_count + 1)**4 > 10**9  # Polynomial is not small in practice.

    mod5 = np.array(RIGHT_ALPHA.tolist(), dtype=np.int64) % 5
    kernel_count = 0
    for z0 in range(5):
        for z1 in range(5):
            for z2 in range(5):
                for z3 in range(5):
                    z = np.array([z0, z1, z2, z3])
                    in_kernel = np.all((mod5 @ z) % 5 == 0)
                    assert in_kernel == (z1 == 2*z0 % 5 and z3 == 3*z2 % 5)
                    kernel_count += int(in_kernel)
    assert kernel_count == 25  # Index 25, not index 5.


def test_arithmetic_mub_replacement_can_have_large_native_source_variance():
    # A uniform complete D+1 MUB ensemble is a projective 2-design, so the
    # same inverse channel applies. Its computational basis alone contributes
    # (D+1)*sum p_k^3 - 2*sum p_k^2 + 1/(D+1) to E[X^2] at rho=P_phi.
    # All remaining contributions are nonnegative. This is NOT the full
    # N-qudit Clifford ensemble; it is the extension-field/MUB replacement.
    with mp.workdps(85):
        half_count, probabilities = _finite_bin_probabilities()
        coordinate_span = 2 * 7 * half_count * 2**40 + 1
        prime = int(sp.nextprime(coordinate_span))
        dimension = prime**4
        support_size = (2*half_count + 1)**4
        collision2 = mp.fsum(p**2 for p in probabilities.values())**4
        collision3 = mp.fsum(p**3 for p in probabilities.values())**4
        contribution = (dimension + 1)*collision3 - 2*collision2 + mp.mpf(1)/(dimension + 1)
        variance_lower = contribution - 1  # E[X]=1 by the 2-design identity.
        universal_lower = mp.mpf(dimension + 1)/support_size**2 - 3
        assert variance_lower >= universal_lower
        assert universal_lower > mp.mpf("1e40")

    # Independent exact single-prime-qudit sanity check: target |0>.
    p = sp.symbols("p", integer=True, positive=True)
    mean = p/(p + 1) + p/(p + 1)/p
    second = p**2/(p + 1) + p/(p + 1)/p**2
    assert sp.simplify(mean - 1) == 0
    assert sp.simplify(second - mean**2 - (p - 1)**2/p) == 0


def _permutation_trace(matrices, permutation):
    visited = set()
    result = sp.Integer(1)
    for start in range(len(matrices)):
        if start in visited:
            continue
        cycle = sp.eye(matrices[0].rows)
        index = start
        while index not in visited:
            visited.add(index)
            cycle *= matrices[index]
            index = permutation[index]
        result *= sp.trace(cycle)
    return sp.simplify(result)


def test_source_proxy_errors_are_small_in_born_weighted_mean_square():
    # This does not license replacing one specified record's score to 1/D
    # precision. It does license a close target proxy in an ensemble estimator.
    dimension = 4
    phi = sp.Matrix([1, 0, 0, 0])
    proxy = sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5), 0, 0])
    input_ket = sp.ones(dimension, 1) / 2
    rho = input_ket * input_ket.T
    difference = phi*phi.T - proxy*proxy.T
    cycle_sum = sum(_permutation_trace([rho, difference, difference], permutation)
                    for permutation in permutations(range(3)))
    moment = sp.Rational(dimension + 1, dimension + 2) * cycle_sum
    expected = sp.Rational(dimension + 1, dimension + 2) * (
        sp.trace(difference**2) + 2*sp.trace(rho*difference**2)
    )
    assert moment == expected
    fidelity = (phi.dot(proxy))**2
    ket_error_squared = (phi - proxy).dot(phi - proxy)
    assert moment <= 4*(1 - fidelity) <= 4*ket_error_squared

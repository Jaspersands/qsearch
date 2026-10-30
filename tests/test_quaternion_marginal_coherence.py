"""Bounded controls for discarding one complete quaternion embedding.

For the positive Gaussian comb in QUATERNION_COVARIANT_RECEIVER, let
p_x = exp(-2*pi*||x||**2/s**2)/Z and Sigma = sum_x p_x |b_x><b_x|,
where b_x is the packet on the retained embeddings. Write D = ||.||_1/2.
If coefficient mass outside radius R is <= tau, the full packet Gram
operator is <= Theta, and every discarded-block separation inside R is
>= Delta, then

  D(Tr_block |Psi><Psi|, Sigma) <= sqrt(Theta*tau) + eta + tau,
  eta = sum_{j>=1} (2*j+3)**4 exp(-pi*j*j*Delta**2/(4*nu**2)).

The native normalized norm-ideal promise gives Delta=(2*R)**(1-d).
The packing sum is <= epsilon when pi*Delta**2/(4*nu**2) is at least
4*log(5)+log(2/epsilon), for 0<epsilon<=1. No enumeration or coefficient
l1 factor is needed. Truncating the coefficients is an analytical step,
not a claim that overlapping packet labels are a physical projector.

Tests below are finite algebra/Gram controls, not a proof of the infinite
theorem, a source backend, or a classical simulator of arbitrary POVMs.
Numerical checks use 80-digit arithmetic with explicit roundoff allowances;
mpmath eigensolvers are not interval certificates. The one shell-series
truncation has a separate analytic remainder. All finite Gram sums are exact
finite fixtures; none is presented as an unbounded lattice enumeration.
"""

from itertools import product

import mpmath as mp
import sympy as sp


def _gram(points, nu):
    return mp.matrix([
        [mp.exp(-mp.pi * mp.fsum((a-b)**2 for a, b in zip(x, y))
                / (4*nu**2)) for y in points]
        for x in points
    ])


def _sqrt_psd(matrix):
    values, vectors = mp.eigsy(matrix)
    assert min(values) > 0  # All fixtures use distinct retained centers.
    return vectors * mp.diag([mp.sqrt(value) for value in values]) * vectors.T


def _trace(matrix):
    return mp.fsum(matrix[i, i] for i in range(matrix.rows))


def _distance(first, second):
    values = mp.eigsy(first-second, eigvals_only=True)
    return mp.fsum(abs(value) for value in values) / 2


def _marginal(discarded, retained, coefficients, nu):
    environment = _gram(discarded, nu)
    kept = _gram(retained, nu)
    columns = _sqrt_psd(kept)
    count = len(coefficients)
    kernel = mp.matrix([
        [coefficients[i]*coefficients[j]*environment[i, j]
         for j in range(count)] for i in range(count)
    ])
    normalizer = mp.fsum(kernel[i, j]*kept[j, i]
                         for i in range(count) for j in range(count))
    mixture = columns * mp.diag([c*c for c in coefficients]) * columns.T
    reduced = columns * kernel * columns.T / normalizer
    cross_bound = mp.fsum(kernel[i, j] for i in range(count)
                         for j in range(count) if i != j)
    return reduced, mixture, normalizer, cross_bound, environment, kept


def test_integral_unit_product_bound_needs_a_total_radius_cutoff():
    root = sp.sqrt(2)
    unit, conjugate = 1+root, 1-root
    assert sp.expand(unit*conjugate) == -1
    previous_small = sp.Integer(1)
    for power in range(1, 7):
        large = sp.expand(unit**power)
        small = sp.expand((-conjugate)**power)
        assert sp.simplify(large*small) == 1
        total_squared = sp.expand(large**2+small**2)
        assert total_squared.is_Integer and total_squared >= 2
        # With 2R equal to the total norm, small >= (2R)^(-1).
        assert sp.simplify(small**2*total_squared-1) == sp.expand(small**4)
        assert 0 < small < previous_small
        previous_small = small
    # The same order contains units with arbitrarily small one-block images.
    assert sp.Abs(conjugate) < 1
    assert previous_small < sp.Rational(1, 100)


def test_fractional_ideal_normalization_restores_the_product_certificate():
    # F=Q(sqrt(2)), O=O_F[1,i,j,k], I=O*alpha, alpha=(1+i)/2.
    # nrd(I)=(1/2)*O_F since nrd(alpha)=1/2 and nrd(O)=O_F.
    q = sp.Rational(1, 2)
    alpha = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2), 0, 0])
    assert alpha.dot(alpha) == q
    normalized = alpha / sp.sqrt(q)
    assert normalized.dot(normalized) == 1
    assert normalized[0].is_rational is False
    # In degree two the product of the unnormalized lengths is 1/2, not >=1.
    assert q**2 < 1  # Squared product, when the wrong q=1 is used.
    assert sp.simplify(q**2 / q**2) == 1

    rotation = sp.Matrix([[1, -1, 0, 0], [1, 1, 0, 0],
                          [0, 0, 1, 1], [0, 0, -1, 1]]) / sp.sqrt(2)
    assert rotation.T*rotation == sp.eye(4)
    root = sp.sqrt(2)
    for coefficients in ((1, 0), (1, 1), (3, 2), (-1, 2)):
        a, b = coefficients
        plus, minus = a+b*root, a-b*root
        first = rotation * sp.Matrix([plus, 1, 0, 0])
        second = rotation * sp.Matrix([minus, 1, 0, 0])
        norm_product = sp.simplify(first.dot(first)*second.dot(second))
        assert norm_product.is_Integer and norm_product >= 1


def test_hamilton_coordinates_must_include_the_norm_isometry():
    # For B=(-2,-3), raw basis coefficients do not have Hamilton norm.
    coordinates = sp.Matrix(sp.symbols("x0:4", real=True))
    embedding = sp.diag(1, sp.sqrt(2), sp.sqrt(3), sp.sqrt(6))
    hamilton = embedding*coordinates
    reduced_norm = coordinates[0]**2 + 2*coordinates[1]**2 \
        + 3*coordinates[2]**2 + 6*coordinates[3]**2
    assert sp.expand(hamilton.dot(hamilton)-reduced_norm) == 0
    assert sp.expand(coordinates.dot(coordinates)-reduced_norm) != 0


def test_partial_trace_gram_and_actual_normalizer_bound():
    with mp.workdps(80):
        root, nu = mp.sqrt(2), mp.mpf(3)/4
        discarded = [(0, 0, 0, 0), (1, 0, 0, 0),
                     (1+root, 0, 0, 0), (0, 1, 0, 0)]
        retained = [(0, 0, 0, 0), (1, 0, 0, 0),
                    (1-root, 0, 0, 0), (0, 1, 0, 0)]
        weights = [mp.exp(-mp.pi*mp.fsum(v*v for v in x+y)/16)
                   for x, y in zip(discarded, retained)]
        scale = mp.sqrt(mp.fsum(w*w for w in weights))
        coefficients = [w/scale for w in weights]
        rho, sigma, normalizer, bound, environment, kept = _marginal(
            discarded, retained, coefficients, nu)
        tolerance = mp.mpf("1e-65")
        assert abs(_trace(rho)-1) < tolerance
        assert abs(_trace(sigma)-1) < tolerance
        assert min(mp.eigsy(rho, eigvals_only=True)) > 0
        assert normalizer > 1  # Coefficient normalization alone is wrong.
        assert abs(_trace(normalizer*rho)-normalizer) < tolerance
        q = normalizer-1
        assert 0 < q < bound
        distance = _distance(rho, sigma)
        assert 0 < distance <= (bound+q)/(2*normalizer) + tolerance
        assert distance <= bound + tolerance
        row_max = max(mp.fsum(environment[i, j] for j in range(len(weights))
                              if i != j) for i in range(len(weights)))
        assert bound <= row_max + tolerance
        for i in range(len(weights)):
            for j in range(len(weights)):
                full_distance = mp.fsum((a-b)**2 for a, b in
                                       zip(discarded[i]+retained[i],
                                           discarded[j]+retained[j]))
                assert abs(environment[i, j]*kept[i, j]
                           - mp.exp(-mp.pi*full_distance/(4*nu**2))) < tolerance


def test_four_dimensional_packing_avoids_count_times_pair_overlap():
    with mp.workdps(80):
        epsilon = mp.mpf("0.001")
        a = 4*mp.log(5)+mp.log(2/epsilon)
        b = a-4*mp.log(5)
        cutoff = 12
        shell_partial = mp.fsum((2*j+3)**4 * mp.exp(-a*j*j)
                               for j in range(1, cutoff+1))
        # (2j+3)^4 <= exp(4*log(5)*j^2); then j^2 >= j.
        shell_tail = mp.exp(-b*(cutoff+1)) / (1-mp.exp(-b))
        majorant = mp.exp(-b)/(1-mp.exp(-b))
        assert shell_partial+shell_tail <= majorant <= epsilon
        assert shell_tail < mp.mpf("1e-40")
        for j in range(1, cutoff+1):
            assert 2*j+3 <= 5**(j*j)

        # A four-dimensional 9^4 grid, using separability, not a dense matrix.
        axis = range(-4, 5)
        largest_axis_row = max(mp.fsum(mp.exp(-a*(i-j)**2) for j in axis)
                               for i in axis)
        row_max = largest_axis_row**4-1
        naive_count_bound = (9**4-1)*mp.exp(-a)
        assert 0 < row_max < shell_partial < epsilon < naive_count_bound


def test_coherent_coefficient_tail_uses_full_gram_not_probability_projection():
    with mp.workdps(80):
        points = [(mp.mpf(j), 0, 0, 0) for j in range(-3, 4)]
        gram = _gram(points, mp.mpf(3)/5)
        weights = [mp.exp(-mp.pi*mp.fsum(v*v for v in x)/8) for x in points]
        c = mp.matrix(weights) / mp.sqrt(mp.fsum(w*w for w in weights))
        head = mp.matrix([c[j] if abs(points[j][0]) <= 1 else 0
                          for j in range(len(points))])
        tail = c-head
        tau = (tail.T*tail)[0]
        full_norm = (c.T*gram*c)[0]
        head_norm = (head.T*gram*head)[0]
        overlap = (c.T*gram*head)[0] / mp.sqrt(full_norm*head_norm)
        pure_distance = mp.sqrt(1-overlap**2)
        theta = max(mp.fsum(gram[i, j] for j in range(len(points)))
                    for i in range(len(points)))
        tolerance = mp.mpf("1e-65")
        assert full_norm > 1
        assert (tail.T*gram*tail)[0] > tau  # Packets are not orthogonal labels.
        assert pure_distance <= mp.sqrt((tail.T*gram*tail)[0]/full_norm) + tolerance
        assert pure_distance <= mp.sqrt(theta*tau) + tolerance


def test_one_real_coordinate_does_not_replace_a_whole_embedding():
    with mp.workdps(80):
        nu = mp.mpf(1)/3
        # In degree two, centers 0 and i agree in every real-part coordinate.
        retained_after_scalar = [(0,)*7, (1, 0, 0, 0, 1, 0, 0)]
        coefficients = [1/mp.sqrt(2)]*2
        rho, sigma, _, _, _, _ = _marginal(
            [(0,), (0,)], retained_after_scalar, coefficients, nu)
        b = mp.exp(-mp.pi*2/(4*nu**2))
        assert abs(_distance(rho, sigma)-(1-b)/2) < mp.mpf("1e-65")
        assert _distance(rho, sigma) > mp.mpf("0.49")

        block = [(0, 0, 0, 0), (0, 1, 0, 0)]
        rho, sigma, _, _, _, _ = _marginal(block, block, coefficients, nu)
        e = mp.exp(-mp.pi/(4*nu**2))
        expected = e*(1-e*e)/(2*(1+e*e))
        assert abs(_distance(rho, sigma)-expected) < mp.mpf("1e-65")
        assert _distance(rho, sigma) < mp.mpf("0.001")


def test_tensor_hybrid_and_explicit_tail_error_budget():
    with mp.workdps(80):
        # Equal two-packet coefficients diagonalize in the same +/- basis.
        e, b = mp.mpf(1)/5, mp.mpf(1)/3
        rho = [(1+b)*(1+e)/(2*(1+e*b)), (1-b)*(1-e)/(2*(1+e*b))]
        sigma = [(1+b)/2, (1-b)/2]
        one = mp.fsum(abs(x-y) for x, y in zip(rho, sigma))/2
        for copies in (1, 2, 3, 5):
            distance = mp.fsum(abs(mp.fprod(rho[i] for i in indices)
                                   - mp.fprod(sigma[i] for i in indices))
                               for indices in product(range(2), repeat=copies))/2
            assert distance <= copies*one + mp.mpf("1e-65")
        for epsilon in (mp.mpf(1), mp.mpf("0.01"), mp.mpf("1e-20")):
            tau, eta, theta = epsilon**2/32, epsilon/2, 2
            assert mp.sqrt(theta*tau)+eta+tau < epsilon

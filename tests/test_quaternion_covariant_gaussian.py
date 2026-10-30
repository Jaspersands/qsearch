"""Bounded controls for the covariant Gaussian source, not a source backend.

Conventions match QUATERNION_COVARIANT_RECEIVER: packet amplitude
nu**(-N/2) * exp(-pi*||u-m||**2/(2*nu**2)). Tests use scalar Gaussian
integrals, finite Gram matrices, and one exact four-dimensional fixture.
Every infinite sum or quadrature truncation has an explicit analytic tail
cap, separate from numerical roundoff. mpmath is not interval arithmetic.
These controls do not prove uniform growing-dimensional CLEAN preparation,
implement a receiver, or turn the nonlinear RMS comparison into a gate.
"""

from itertools import product

import mpmath as mp
import sympy as sp


def _mass(left, right, center=0, nu=1):
    """Squared packet mass on one interval, with stable same-tail subtraction."""
    assert left <= right and nu > 0
    a = mp.sqrt(mp.pi) * (left - center) / nu
    b = mp.sqrt(mp.pi) * (right - center) / nu
    if a >= 0:
        return (mp.erfc(a) - mp.erfc(b)) / 2
    if b <= 0:
        return (mp.erfc(-b) - mp.erfc(-a)) / 2
    return (mp.erf(b) - mp.erf(a)) / 2


def _window(center, h, nu, cutoff):
    half_count = int(mp.ceil(cutoff * nu / h)) + 1
    first = int(mp.floor(center / h)) - half_count
    return first * h, (first + 2 * half_count + 1) * h


def _restricted_overlap(x, y, box_x, box_y, nu=1):
    left, right = max(box_x[0], box_y[0]), min(box_x[1], box_y[1])
    if left >= right:
        return mp.mpf(0)
    root_x = _mass(*box_x, center=x, nu=nu)
    root_y = _mass(*box_y, center=y, nu=nu)
    return (
        mp.exp(-mp.pi * (x - y) ** 2 / (4 * nu**2))
        * _mass(left, right, center=(x + y) / 2, nu=nu)
        / mp.sqrt(root_x * root_y)
    )


def test_packet_normalizer_and_gradient_gram_identities():
    nu_symbol = sp.Symbol("nu", positive=True)
    displacement = sp.symbols("r0:4", real=True)
    radius_squared = sum(value**2 for value in displacement)
    overlap = sp.exp(-sp.pi * radius_squared / (4 * nu_symbol**2))
    gradient_gram = -sum(sp.diff(overlap, value, 2) for value in displacement)
    expected = (
        2 * sp.pi / nu_symbol**2
        - sp.pi**2 * radius_squared / (4 * nu_symbol**4)
    ) * overlap
    assert sp.simplify(gradient_gram - expected) == 0

    with mp.workdps(80):
        nu, cap = mp.mpf(7) / 5, 8
        roundoff = mp.mpf("1e-65")
        tail = mp.erfc(mp.sqrt(mp.pi) * cap)
        second_tail = cap * mp.exp(-mp.pi * cap**2) / mp.pi + tail / (2 * mp.pi)

        def phi(t):
            return mp.exp(-mp.pi * t**2 / (2 * nu**2)) / mp.sqrt(nu)

        for separation in (mp.mpf(0), nu / 2, 2 * nu):
            kernel = mp.exp(-mp.pi * separation**2 / (4 * nu**2))
            packet_product = lambda t: phi(t + separation / 2) * phi(t - separation / 2)
            integral = mp.quad(packet_product, [-cap * nu, 0, cap * nu])
            assert abs(integral - kernel) <= kernel * tail + roundoff
            derivative_integral = mp.quad(
                lambda t: mp.pi**2 / nu**4 * (t**2 - separation**2 / 4) * packet_product(t),
                [-cap * nu, 0, cap * nu],
            )
            derivative_expected = (
                mp.pi / (2 * nu**2) - mp.pi**2 * separation**2 / (4 * nu**4)
            ) * kernel
            derivative_tail = mp.pi**2 / nu**4 * kernel * (
                nu**2 * second_tail + separation**2 * tail / 4
            )
            assert abs(derivative_integral - derivative_expected) <= derivative_tail + roundoff
            if separation == 2 * nu:
                assert derivative_integral < 0  # Off-diagonal derivative entries need not be positive.

        separation, width = nu / 2, 3 * nu
        weight = mp.exp(-mp.pi * separation**2 / width**2)
        coefficient_normalizer = 1 + weight**2
        kernel = mp.exp(-mp.pi * separation**2 / (4 * nu**2))
        norm_squared = 1 + 2 * weight * kernel / coefficient_normalizer
        measured = mp.quad(
            lambda t: (phi(t) + weight * phi(t - separation)) ** 2 / coefficient_normalizer,
            [-cap * nu, 0, separation, separation + cap * nu],
        )
        # Cauchy--Schwarz bounds the omitted squared sum by the two packet tails.
        assert abs(measured - norm_squared) <= 2 * tail + roundoff
        assert 1 < norm_squared <= 1 + kernel
        assert norm_squared - 1 > mp.mpf("0.5")  # Z alone is not the physical normalizer.
        assert abs(measured / norm_squared - 1) <= 2 * tail + roundoff


def test_tail_gram_row_bound_does_not_pay_the_coefficient_l1_norm():
    with mp.workdps(80):
        spacing, cutoff, count = 4, 1, 13
        centers = tuple(spacing * index for index in range(-(count // 2), count // 2 + 1))
        p = mp.erfc(mp.sqrt(mp.pi) * cutoff)
        theta_cap = 4
        exponent = mp.pi * spacing**2 / 4
        eta_partial = 2 * mp.fsum(mp.exp(-exponent * j**2) for j in range(1, theta_cap + 1))
        # 2*sum_{j>K} exp(-a*j^2) <= 2*integral_K^infinity <= exp(-a*K^2)/(a*K).
        eta_tail = mp.exp(-exponent * theta_cap**2) / (exponent * theta_cap)
        eta = eta_partial + eta_tail
        assert eta_tail < mp.mpf("1e-85")
        gram = []
        for x in centers:
            row = []
            for y in centers:
                if x == y:
                    row.append(p)
                    continue
                midpoint = mp.mpf(x + y) / 2
                full_overlap = mp.exp(-mp.pi * (x - y) ** 2 / 4)
                # The two removed intervals are disjoint; their complement is exact.
                entry = full_overlap * (
                    1 - _mass(x - cutoff, x + cutoff, midpoint)
                    - _mass(y - cutoff, y + cutoff, midpoint)
                )
                assert 0 <= entry <= full_overlap
                row.append(entry)
            gram.append(row)
        row_max = max(mp.fsum(row) for row in gram)
        squared_error = mp.fsum(mp.fsum(row) for row in gram) / count
        roundoff = mp.mpf("1e-65")
        assert p < squared_error <= row_max + roundoff
        assert row_max <= p + eta + roundoff
        # The triangle bound is valid but loses the uniform guarantee as count grows.
        triangle_squared = count * p  # (sum |c_x|)^2*p for c_x=1/sqrt(count).
        assert triangle_squared > 10 * (p + eta)


def test_full_cells_bound_prefix_precision_but_partial_cells_do_not():
    with mp.workdps(100):
        nu, h, cutoff, center = mp.mpf(1), mp.mpf(1) / 8, 1, mp.mpf(3) / 32
        left, right = _window(center, h, nu, cutoff)
        count = int((right - left) / h)
        depth = (count - 1).bit_length()
        floor_mass = (h / nu) * mp.exp(-mp.pi * (cutoff + 3) ** 2)
        epsilon = mp.mpf("1e-8")
        precision_bits = int(mp.ceil(mp.log(16 * depth**2 / (floor_mass * epsilon**2), 2)))
        integral_error = mp.power(2, -precision_bits)
        assert integral_error <= floor_mass * epsilon**2 / (16 * depth**2)
        assert _mass(left, right, center) >= 1 - mp.erfc(mp.sqrt(mp.pi) * cutoff)
        nonempty, empty, endpoint_probabilities = 0, 0, set()
        for level in range(depth):
            block_size = 1 << (depth - level)
            for prefix in range(1 << level):
                start = prefix * block_size
                stop = min(start + block_size, count)
                if start >= stop:
                    empty += 1  # Padded branches are recognized by integer endpoints.
                    continue
                nonempty += 1
                split = min(start + block_size // 2, stop)
                denominator = _mass(left + start * h, left + stop * h, center)
                numerator = _mass(left + start * h, left + split * h, center)
                probability = numerator / denominator
                assert denominator >= floor_mass
                if probability in (0, 1):
                    endpoint_probabilities.add(int(probability))
                for numerator_sign, denominator_sign in product((-1, 1), repeat=2):
                    approximate = (numerator + numerator_sign * integral_error) / (
                        denominator + denominator_sign * integral_error
                    )
                    approximate = min(mp.mpf(1), max(mp.mpf(0), approximate))
                    rotation_error_squared = (mp.sqrt(probability) - mp.sqrt(approximate)) ** 2 + (
                        mp.sqrt(1 - probability) - mp.sqrt(1 - approximate)
                    ) ** 2
                    assert rotation_error_squared <= (epsilon / depth) ** 2
        assert nonempty > depth and empty > 0 and 1 in endpoint_probabilities
        for index in range(count):
            assert _mass(left + index * h, left + (index + 1) * h, center) >= floor_mass

        # A terminal sliver has no corresponding lower bound, even within this same window.
        sliver = h * mp.power(2, -180)
        partial_mass = _mass(right - sliver, right, center)
        assert 0 < partial_mass < floor_mass * mp.mpf("1e-20")


def test_rounded_center_floor_jump_and_same_window_translation_bound():
    with mp.workdps(80):
        h, nu, cutoff = mp.mpf(1) / 4, mp.mpf(1), 1
        box_zero = _window(mp.mpf(0), h, nu, cutoff)
        root = _mass(*box_zero)
        edge_mass = _mass(-box_zero[0], box_zero[1])
        jump_squared = 2 * edge_mass / root
        assert jump_squared > mp.mpf("1e-4")
        p = mp.erfc(mp.sqrt(mp.pi) * cutoff)
        for bits in (20, 60):
            rounded = -mp.power(2, -bits)
            box_rounded = _window(rounded, h, nu, cutoff)
            assert box_rounded != box_zero
            discontinuous_error = 2 * (1 - _restricted_overlap(0, rounded, box_zero, box_rounded))
            assert abs(discontinuous_error - jump_squared) < 10 * abs(rounded)
            same_window_error = 2 * (1 - _restricted_overlap(0, rounded, box_rounded, box_rounded))
            assert 0 <= same_window_error <= 2 * mp.pi / (1 - p) * rounded**2
            assert discontinuous_error > 1000 * same_window_error


def test_four_h_support_and_exact_inverse_coefficient_rounding():
    nu, h, cutoff, dimension = sp.Integer(1), sp.Rational(1, 4), sp.Rational(9, 8), 4
    basis = 128 * sp.eye(dimension)
    basis[1, 0] = -h
    inverse = basis.inv()
    coefficient = sp.Matrix([1, 0, 0, 0])
    center = basis * coefficient
    rounded = center + sp.Matrix([0, h, 0, 0])
    assert (rounded - center).norm() == h
    half_count = sp.ceiling(cutoff * nu / h) + 1
    boxes = [
        ((sp.floor(value / h) - half_count) * h, (sp.floor(value / h) + half_count + 1) * h)
        for value in rounded
    ]
    for index, (left, right) in enumerate(boxes):
        assert left <= center[index] - cutoff * nu
        assert right >= center[index] + cutoff * nu
        assert max(center[index] - left, right - center[index]) <= cutoff * nu + 4 * h
    assert boxes[1][1] - center[1] > cutoff * nu + 3 * h  # The old support constant can fail.
    radius_squared = dimension * (cutoff * nu + 4 * h) ** 2
    inverse_frobenius_squared = sum(value**2 for value in inverse)
    assert radius_squared * inverse_frobenius_squared <= sp.Rational(1, 64)
    # All 16 corners suffice for affine coordinate bounds on every occupied cell.
    for corner in product(*boxes):
        point = sp.Matrix(corner)
        assert (point - center).dot(point - center) <= radius_squared
        reconstructed = inverse * point
        assert all(abs(value) <= sp.Rational(1, 8) for value in reconstructed - coefficient)
        assert reconstructed.applyfunc(lambda value: sp.floor(value + sp.Rational(1, 2))) == coefficient


def test_center_dependent_packet_normalizers_cannot_be_left_constant():
    with mp.workdps(80):
        centers = (mp.mpf(0), mp.mpf(21) / 2)
        boxes = tuple(_window(center, 1, 1, 1) for center in centers)
        assert boxes[0][1] < boxes[1][0]
        roots = tuple(_mass(*box, center=center) for center, box in zip(centers, boxes))
        p = mp.erfc(mp.sqrt(mp.pi))
        assert all(1 - p <= root <= 1 for root in roots)
        assert roots[1] - roots[0] > mp.mpf("1e-7")
        weights = (mp.mpf(3) / 5, mp.mpf(4) / 5)
        unnormalized_squared = mp.fsum(c**2 * root for c, root in zip(weights, roots))
        wrong_common_squared = unnormalized_squared / roots[0]
        correct_squared = mp.fsum(c**2 for c in weights)
        assert unnormalized_squared < 1 < wrong_common_squared
        assert abs(correct_squared - 1) < mp.mpf("1e-70")
        normalization_change_squared = mp.fsum(
            c**2 * (1 - mp.sqrt(root)) ** 2 for c, root in zip(weights, roots)
        )
        assert normalization_change_squared <= p**2


def test_rms_map_is_nonexpansive_but_not_a_linear_quantum_operation():
    # Each pair represents equal half-cells of a unit-volume cell, not qubit amplitudes.
    def rms(values):
        result = []
        for index in range(0, len(values), 2):
            value = sp.sqrt((values[index] ** 2 + values[index + 1] ** 2) / 2)
            result.extend((value, value))
        return sp.Matrix(result)

    def norm_squared(values):
        return sp.simplify(values.dot(values) / 2)

    f, g = sp.Matrix([3, 4, 0, 2]), sp.Matrix([1, 0, 2, 1])
    assert norm_squared(rms(f)) == norm_squared(f)
    assert norm_squared(rms(g)) == norm_squared(g)
    assert norm_squared(rms(f) - rms(g)) < norm_squared(f - g)
    first, second = sp.Matrix([sp.sqrt(2), 0]), sp.Matrix([0, sp.sqrt(2)])
    assert first.dot(second) == 0
    assert rms(first) == rms(second) == sp.ones(2, 1)
    assert rms(first + second) != rms(first) + rms(second)
    # A positive smooth cell profile also checks the RMS-to-mean Poincare step.
    x = sp.Symbol("x", real=True)
    profile = 1 + sp.cos(sp.pi * x) / 2
    mean = sp.integrate(profile, (x, 0, 1))
    squared_mean = sp.integrate(profile**2, (x, 0, 1))
    variance = squared_mean - mean**2
    energy = sp.integrate(sp.diff(profile, x) ** 2, (x, 0, 1))
    rms_error = 2 * sp.sqrt(squared_mean) * (sp.sqrt(squared_mean) - mean)
    assert variance == energy / sp.pi**2 == sp.Rational(1, 8)
    assert 0 < rms_error <= 2 * variance

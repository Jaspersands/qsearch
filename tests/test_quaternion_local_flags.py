"""Exact controls for PUBLIC split-residue ideals, not hidden-isogeny oracles.

The recovery routine takes only an explicit ideal image. Exhaustive finite
groups below verify the proof on bounded cases; they are not the algorithm.
"""

from itertools import product

import pytest
from sympy import GF, Matrix, Rational
from sympy.polys.matrices import DomainMatrix


ZERO = (0, 0, 0, 0)
IDENTITY = (1, 0, 0, 1)
MATRIX_UNITS = tuple(tuple(int(i == j) for i in range(4)) for j in range(4))


def _multiply(a, b, p):
    return (
        (a[0] * b[0] + a[1] * b[2]) % p,
        (a[0] * b[1] + a[1] * b[3]) % p,
        (a[2] * b[0] + a[3] * b[2]) % p,
        (a[2] * b[1] + a[3] * b[3]) % p,
    )


def _det(a, p):
    return (a[0] * a[3] - a[1] * a[2]) % p


def _canonical_span(rows, p):
    reduced, pivots = DomainMatrix.from_list([list(row) for row in rows], GF(p)).rref()
    return tuple(tuple(int(x) % p for x in row) for row in reduced.to_Matrix().tolist()[:len(pivots)])


def _common_right_kernel(public_ideal_image, p):
    rows = [list(row) for matrix in public_ideal_image for row in (matrix[:2], matrix[2:])]
    kernel = DomainMatrix.from_list(rows, GF(p)).nullspace().to_Matrix().tolist()
    if not kernel:
        return ()
    return _canonical_span(kernel, p)


def _left_ideal_image(generator, p):
    return tuple(_multiply(unit, generator, p) for unit in MATRIX_UNITS)


def _all_invertible(p):
    if p not in (2, 3, 5):
        raise ValueError("finite group control cap")
    return tuple(a for a in product(range(p), repeat=4) if _det(a, p))


def _annihilates(a, vector, p):
    return (a[0] * vector[0] + a[1] * vector[1]) % p == 0 and (
        a[2] * vector[0] + a[3] * vector[1]
    ) % p == 0


def _preserves_line(a, v, p):
    w = ((a[0] * v[0] + a[1] * v[1]) % p, (a[2] * v[0] + a[3] * v[1]) % p)
    return (v[0] * w[1] - v[1] * w[0]) % p == 0


@pytest.mark.parametrize("p", (2, 3, 5))
def test_public_ideal_recovers_every_rank_one_flag_and_its_right_stabilizer(p):
    group = _all_invertible(p)
    assert len(group) == (p * p - 1) * (p * p - p)
    for line in ((0, 1), *((1, t) for t in range(p))):
        row = (-line[1] % p, line[0])
        generator = (*row, *row)
        image = _left_ideal_image(generator, p)
        space = _canonical_span(image, p)
        assert len(space) == 2
        kernel = _common_right_kernel(image, p)
        assert kernel == (line,)
        # Independent bounded vector enumeration does not use the kernel solver.
        direct_kernel = {
            v for v in product(range(p), repeat=2) if _annihilates(generator, v, p)
        }
        assert direct_kernel == {((k * line[0]) % p, (k * line[1]) % p) for k in range(p)}
        stabilizer = []
        for g in group:
            right_image = tuple(_multiply(x, g, p) for x in image)
            right_fixed = _canonical_span(right_image, p) == space
            assert right_fixed == _preserves_line(g, line, p)
            if right_fixed:
                stabilizer.append(g)
            # A left ideal is invariant under EVERY invertible left multiplier.
            assert _canonical_span(tuple(_multiply(g, x, p) for x in image), p) == space
        assert len(stabilizer) == p * (p - 1) ** 2
        assert len(group) // len(stabilizer) == p + 1


@pytest.mark.parametrize("p", (2, 3, 5))
def test_recovery_uses_only_basis_span_not_a_chosen_generator_or_basis(p):
    a = (1, 1, 0, 0)
    b = (0, 0, 1, 1)
    assert a != b
    left = _left_ideal_image(a, p)
    right = _left_ideal_image(b, p)
    assert _canonical_span(left, p) == _canonical_span(right, p)
    expected = _common_right_kernel(left, p)
    assert _common_right_kernel(right, p) == expected
    basis = _canonical_span(left, p)
    mixed = tuple((x + y) % p for x, y in zip(*basis))
    changed = (mixed, basis[1], ZERO, mixed)
    assert _canonical_span(changed, p) == basis
    assert _common_right_kernel(changed, p) == expected
    # Rows and columns have different roles: a and b have different images.
    assert a[:2] != b[:2]
    assert all(_annihilates(x, expected[0], p) for x in changed)


@pytest.mark.parametrize("p", (2, 3, 5))
def test_zero_and_full_rank_images_do_not_fabricate_a_hidden_line(p):
    zero_image = _left_ideal_image(ZERO, p)
    full_image = _left_ideal_image(IDENTITY, p)
    assert _common_right_kernel(zero_image, p) == ((1, 0), (0, 1))
    assert _common_right_kernel(full_image, p) == ()
    assert len(_canonical_span(zero_image, p)) == 0
    assert len(_canonical_span(full_image, p)) == 4
    for g in _all_invertible(p):
        assert _canonical_span(_left_ideal_image(g, p), p) == _canonical_span(full_image, p)


@pytest.mark.parametrize("p", (2, 3, 5))
def test_ambient_reduction_is_not_the_abstract_ideal_quotient(p):
    # I=p*O: I/p*I has dimension four, but its image in O/p*O is zero.
    integral_ideal_basis = tuple(tuple(p * x for x in e) for e in MATRIX_UNITS)
    ambient_image = tuple(tuple(x % p for x in e) for e in integral_ideal_basis)
    abstract_coordinates = MATRIX_UNITS
    assert len(_canonical_span(abstract_coordinates, p)) == 4
    assert len(_canonical_span(ambient_image, p)) == 0
    assert len(_common_right_kernel(ambient_image, p)) == 2
    # Silently replacing the image by a saturated lattice changes the problem.
    assert _common_right_kernel(abstract_coordinates, p) == ()


def test_exhaustive_reference_has_a_resource_cap():
    with pytest.raises(ValueError, match="control cap"):
        _all_invertible(101)


def test_left_module_generators_are_not_a_scalar_matrix_basis():
    p = 3
    e11, e12, e21, _ = MATRIX_UNITS
    assert len(_canonical_span((e11,), p)) == 1
    assert len(_canonical_span(_left_ideal_image(e11, p), p)) == 2
    assert _common_right_kernel((e11,), p) == ((0, 1),)
    assert _multiply(e21, e11, p) == e21
    # Individual rank-one generators can together generate the WHOLE ideal.
    assert _det(e11, p) == _det(e12, p) == 0
    assert _common_right_kernel((e11, e12), p) == ()
    full = _left_ideal_image(e11, p) + _left_ideal_image(e12, p)
    assert len(_canonical_span(full, p)) == 4


def test_prime_power_stabilizer_is_not_always_a_borel():
    modulus = 4
    row_module = {(a, b) for a in range(4) for b in (0, 2)}
    kernel = {
        (x, y) for x, y in product(range(4), repeat=2)
        if all((a * x + b * y) % 4 == 0 for a, b in row_module)
    }
    assert kernel == {(0, 0), (0, 2)}  # Not a free rank-one Z/4 module.
    for g in product(range(4), repeat=4):
        if _det(g, modulus) % 2 == 0:
            continue
        moved = {
            ((a * g[0] + b * g[2]) % 4, (a * g[1] + b * g[3]) % 4)
            for a, b in row_module
        }
        assert (moved == row_module) == (g[1] % 2 == 0)
    assert (1, 2, 0, 1)[1] != 0  # A nontriangular stabilizer element.
    # Over the fraction field a full lattice has zero kernel; its row module
    # still has a proper integral stabilizer. Kernel alone loses the level.
    assert Matrix.diag(1, 2).nullspace() == []
    swap = Matrix([[0, 1], [1, 0]])
    change = Matrix.diag(1, 2) * swap * Matrix.diag(1, Rational(1, 2))
    assert any(value.q != 1 for value in change)


def test_one_local_flag_and_target_norm_do_not_determine_the_global_ideal():
    a = Matrix([[1, 0], [0, 15]])
    b = Matrix([[1, 3], [0, 15]])
    assert a.det() == b.det() == 15
    local_a = tuple(int(x) % 3 for x in a)
    local_b = tuple(int(x) % 3 for x in b)
    assert local_a == local_b
    assert _common_right_kernel(_left_ideal_image(local_a, 3), 3) == ((0, 1),)
    # A = C*B would require the unique rational multiplier C=A*B^-1.
    # Its nonintegrality proves M2(Z)*A != M2(Z)*B, despite equal local data.
    assert a * b.inv() == Matrix([[1, Rational(-1, 5)], [0, 1]])
    assert any(value.q != 1 for value in a * b.inv())

"""Exact source-audit controls, not a general rejection of quaternion HSVP.

The formulas tested are printed in the 2026-02-13 public version of
ePrint 2025/1448. The publisher's later text has not been inspected.
"""

import pytest
from sympy import Matrix, Rational, symbols, expand


# Hurwitz order in the standard Hamilton basis [1,i,j,k], as columns.
HURWITZ = Matrix([
    [1, 0, 0, Rational(1, 2)],
    [0, 1, 0, Rational(1, 2)],
    [0, 0, 1, Rational(1, 2)],
    [0, 0, 0, Rational(1, 2)],
])
CANONICAL_GRAM = 2 * HURWITZ.T * HURWITZ


def _in_lattice(basis, vector):
    return all(value.q == 1 for value in basis.inv() * vector)


def test_hurwitz_norm_integrality_and_canonical_embedding_normalization():
    a, b, c, d = z = Matrix(symbols("a b c d"))
    x = HURWITZ * z
    norm = (x.T * x)[0]
    assert expand(norm - (a*a + b*b + c*c + d*(a+b+c) + d*d)) == 0
    assert HURWITZ.det() == Rational(1, 2)
    assert CANONICAL_GRAM.det() == 4
    # Definition 12 with L=Q(i) repeats both complex embeddings, so
    # squared Euclidean length is twice the Hamilton reduced norm.
    assert expand((z.T * CANONICAL_GRAM * z)[0] - 2 * norm) == 0


@pytest.mark.parametrize("t", (1, 2, 3, 9, 17))
def test_actual_covolume_scales_with_index_not_reduced_norm(t):
    ideal_basis = t * HURWITZ
    index = abs((HURWITZ.inv() * ideal_basis).det())
    norm_ideal = t*t  # nrd(t*O)=t^2*Z, since nrd(O)=Z.
    assert index == t**4 == norm_ideal**2
    gram = 2 * ideal_basis.T * ideal_basis
    actual_covolume = 2 * t**4
    assert gram.det() == actual_covolume**2
    printed_covolume = norm_ideal * 2
    assert (printed_covolume == actual_covolume) == (t == 1)
    assert actual_covolume == norm_ideal**2 * 2
    # Fourth powers suffice to compare HSVP scales exactly, without floats.
    assert (actual_covolume // 2) == t**4
    assert (printed_covolume // 2) == t**2


def test_nine_order_counterexample_is_membership_failure_not_only_a_bad_bound():
    ideal = 9 * HURWITZ
    x = Matrix([3, 0, 0, 0])
    assert _in_lattice(HURWITZ, x)
    assert ideal.inv() * x == Matrix([Rational(1, 3), 0, 0, 0])
    assert not _in_lattice(ideal, x)
    assert _in_lattice(ideal, Matrix([9, 0, 0, 0]))
    # For a scalar r, Hurwitz coordinates are (r,0,0,0), so
    # (9*O) intersect Q = 9*Z = (3*Z)^2 as ideals of Z.
    r = symbols("r")
    assert HURWITZ.inv() * Matrix([r, 0, 0, 0]) == Matrix([r, 0, 0, 0])
    assert 3*3 == 9
    # x=3 is the shortest nonzero vector and a 1-HSVP solution in 3*Z.
    assert abs(int(x[0])) == Matrix([[3]]).det()
    assert 3 % 2 == 1  # Support avoids the Hurwitz reduced discriminant 2.
    assert 2 * ideal.T * ideal == 81 * CANONICAL_GRAM
    assert (2 * ideal.T * ideal).det() == 13122**2
    assert 81 * 2 == 162 != 13122


def test_ambient_membership_does_not_follow_from_a_square_root_ideal():
    # This is the specific logical implication used in the printed Theorem 8.
    # A repaired norm constant cannot repair membership of x itself.
    for m in (3, 5, 7):
        x = Matrix([m, 0, 0, 0])
        assert not _in_lattice(m*m * HURWITZ, x)
        assert _in_lattice(m*m * HURWITZ, Matrix([m*m, 0, 0, 0]))


def test_repaired_center_ideal_has_membership_and_homogeneous_hsvp_factor():
    # Search I intersect Q=tZ itself, not a square-root ideal. Under the
    # actual canonical metric, c=sqrt(2), Delta_Q=1, Delta_O=2.
    # Thus the repaired factor has fourth power 2, independent of t.
    for t in (1, 3, 9, 17):
        ideal = t * HURWITZ
        x = Matrix([t, 0, 0, 0])
        assert _in_lattice(ideal, x)
        squared_length = 2 * (x.T * x)[0]
        covolume = 2 * t**4
        assert squared_length**2 / covolume == 2
        assert (2 * ideal.T * ideal).det() == covolume**2

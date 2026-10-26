"""Exact quaternion controls for the proposed elementary action construction.

No curves, torsion points, canonicalizer or quantum source are implemented.
Use Z[i,j], i^2=-1, j^2=-11, ij=-ji, a suborder of the known endomorphism
ring of y^2=x^3-x in characteristic 11. Its index is prime to our odd
torsion primes. The split matrices are torsion-coordinate witnesses only.
"""

import itertools

import pytest
from flint import nmod_mat


ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)
QI = (0, 1, 0, 0)
QJ = (0, 0, 1, 0)
QK = (0, 0, 0, 1)


def qa(x, y):
    return tuple(a + b for a, b in zip(x, y))


def qs(c, x):
    return tuple(c * a for a in x)


def qc(x):
    return (x[0], -x[1], -x[2], -x[3])


def qm(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (a*e-b*f-11*c*g-11*d*h,
            a*f+b*e+11*(c*h-d*g),
            a*g+c*e-b*h+d*f,
            a*h+d*e+b*g-c*f)


def eye(n):
    return tuple(tuple(ONE if i == j else ZERO for j in range(n)) for i in range(n))


def scale(c, a):
    return tuple(tuple(qs(c, v) for v in row) for row in a)


def add(a, b):
    return tuple(tuple(qa(x, y) for x, y in zip(ar, br)) for ar, br in zip(a, b))


def mul(a, b):
    def entry(i, j):
        out = ZERO
        for k in range(len(a)):
            out = qa(out, qm(a[i][k], b[k][j]))
        return out
    return tuple(tuple(entry(i, j) for j in range(len(a))) for i in range(len(a)))


def adj(a):
    return tuple(tuple(qc(a[j][i]) for j in range(len(a))) for i in range(len(a)))


def divide_exact(a, d):
    if any(v % d != 0 for row in a for q in row for v in q):
        raise ValueError("not integral in the fixture order")
    return tuple(tuple(tuple(v // d for v in q) for q in row) for row in a)


def split_basis(prime):
    # Bounded fixture enumeration, NOT a uniform quaternion splitting algorithm.
    a, b = next((a, b) for a in range(prime) for b in range(prime)
                if (a*a+b*b+11) % prime == 0)
    unit = nmod_mat([[1, 0], [0, 1]], prime)
    i = nmod_mat([[0, -1], [1, 0]], prime)
    j = nmod_mat([[a, b], [b, -a]], prime)
    return (unit, i, j, i*j)


def reduce(a, prime):
    basis = split_basis(prime)
    n = len(a)
    rows = [[0] * (2*n) for _ in range(2*n)]
    for i, j in itertools.product(range(n), repeat=2):
        for r, s in itertools.product(range(2), repeat=2):
            rows[2*i+r][2*j+s] = sum(a[i][j][k] * int(basis[k][r, s]) for k in range(4))
    return nmod_mat(rows, prime)


def lift_entry(r, s, c, prime):
    basis = split_basis(prime)
    linear = nmod_mat([[int(basis[k][i, j]) for k in range(4)]
                       for i in range(2) for j in range(2)], prime)
    rhs = nmod_mat([[c if (i, j) == (r, s) else 0]
                    for i in range(2) for j in range(2)], prime)
    answer = linear.inv() * rhs
    return tuple(int(answer[k, 0]) for k in range(4))


def primitive_word(n, i, j, c, prime):
    if i == j or n < 2:
        raise ValueError("distinct physical indices and at least two factors required")
    if i // 2 != j // 2:
        matrix = [list(row) for row in eye(n)]
        matrix[i // 2][j // 2] = lift_entry(i % 2, j % 2, c, prime)
        return [tuple(tuple(row) for row in matrix)]
    k = 2 * ((i // 2 + 1) % n)
    # [e_ik(c),e_kj(1)] = e_ij(c); all four factors cross elliptic blocks.
    a = primitive_word(n, i, k, c, prime)[0]
    b = primitive_word(n, k, j, 1, prime)[0]
    return [a, b, add(scale(2, eye(n)), scale(-1, a)),
            add(scale(2, eye(n)), scale(-1, b))]


def evaluate(word):
    out = eye(len(word[0]))
    for factor in word:
        out = mul(out, factor)
    return out


def inverse(word):
    unit = eye(len(word[0]))
    return evaluate([add(scale(2, unit), scale(-1, factor)) for factor in reversed(word)])


def compile_word(specification, prime=61, n=2):
    word = [factor for i, j, c in specification
            for factor in primitive_word(n, i, j, c, prime)]
    return evaluate(word), inverse(word)


def form(n, prime):
    return nmod_mat([[1 if r % 2 == 0 and c == r+1 else
                      -1 if r % 2 == 1 and c == r-1 else 0
                      for c in range(2*n)] for r in range(2*n)], prime)


def field_adj(a, prime):
    j = form(a.nrows() // 2, prime)
    return j.inv() * a.transpose() * j


def kernel(a, prime):
    basis, dimension = reduce(a, prime).nullspace()
    rows = [[int(basis[r, c]) for r in range(basis.nrows())] for c in range(dimension)]
    normal, rank = nmod_mat(rows, prime).rref()
    assert rank == dimension
    return tuple(tuple(int(normal[r, c]) for c in range(normal.ncols())) for r in range(rank))


PHI = (((6, 5, 0, 0), ZERO), (ZERO, (6, -5, 0, 0)))
ROOTS = [((0, 1, 1),), ((1, 0, 1),), ((2, 3, 1),), ((3, 2, 1),),
         ((0, 2, 1), (3, 1, -1)), ((0, 3, 1), (2, 1, 1))]


def polarization(sigma):
    t = divide_exact(add(mul(adj(sigma), sigma), scale(-1, eye(2))), 61)
    return add(eye(2), mul(mul(PHI, t), adj(PHI)))


def test_quaternion_multiplication_and_involution():
    assert qm(QI, QI) == qs(-1, ONE)
    assert qm(QJ, QJ) == qs(-11, ONE)
    assert qm(QI, QJ) == QK == qs(-1, qm(QJ, QI))
    for a, b in itertools.product([ONE, QI, QJ, QK, (2, 3, -4, 5)], repeat=2):
        assert qc(qm(a, b)) == qm(qc(b), qc(a))
        assert qm(qc(a), a) == (a[0]**2+a[1]**2+11*a[2]**2+11*a[3]**2, 0, 0, 0)


@pytest.mark.parametrize('prime', [3, 5, 7, 13, 61])
def test_split_representation_respects_multiplication_and_rosati(prime):
    for a, b in itertools.product([ONE, QI, QJ, QK], repeat=2):
        assert reduce(((qm(a, b),),), prime) == reduce(((a,),), prime) * reduce(((b,),), prime)
        assert reduce(((qc(a),),), prime) == field_adj(reduce(((a,),), prime), prime)


@pytest.mark.parametrize('prime', [3, 5, 13])
@pytest.mark.parametrize('n', [2, 3])
def test_all_elementary_physical_transvections_have_actual_unit_lifts(prime, n):
    for i, j in itertools.permutations(range(2*n), 2):
        for c in [1, prime-1]:
            word = primitive_word(n, i, j, c, prime)
            sigma, sigma_inv = evaluate(word), inverse(word)
            target = reduce(eye(n), prime)
            target[i, j] = c
            assert reduce(sigma, prime) == target
            assert mul(sigma, sigma_inv) == mul(sigma_inv, sigma) == eye(n)
            assert len(word) == (1 if i // 2 != j // 2 else 4)


@pytest.mark.parametrize('root', ROOTS)
def test_repolarization_is_integral_invertible_and_restores_multiplier(root):
    sigma, sigma_inv = compile_word(root)
    reduced = reduce(sigma, 61)
    assert field_adj(reduced, 61) * reduced == reduce(eye(2), 61)
    h = polarization(sigma)
    psi = mul(PHI, sigma_inv)
    assert h == adj(h)
    assert mul(mul(adj(psi), h), psi) == scale(61, eye(2))
    inverse_s = mul(sigma_inv, adj(sigma_inv))
    correction = divide_exact(add(inverse_s, scale(-1, eye(2))), 61)
    h_inv = add(eye(2), mul(mul(PHI, correction), adj(PHI)))
    assert mul(h, h_inv) == mul(h_inv, h) == eye(2)


def test_raw_labels_change_even_for_an_identity_congruence_lift():
    sigma = ((ONE, (61, 0, 0, 0)), (ZERO, ONE))
    sigma_inv = ((ONE, (-61, 0, 0, 0)), (ZERO, ONE))
    assert reduce(sigma, 61) == reduce(eye(2), 61)
    psi, h = mul(PHI, sigma_inv), polarization(sigma)
    assert kernel(psi, 61) == kernel(PHI, 61)
    assert h != eye(2)
    u = divide_exact(mul(psi, adj(PHI)), 61)
    u_inv = divide_exact(mul(mul(PHI, sigma), adj(PHI)), 61)
    assert mul(u, u_inv) == eye(2)
    assert mul(u, PHI) == psi
    assert mul(mul(adj(u), h), u) == eye(2)
    assert reduce(psi, 7) != reduce(PHI, 7)


def test_local_mark_and_pairing_isomorphisms_do_not_prove_global_integrality():
    sigma, sigma_inv = compile_word(ROOTS[0])
    psi, h = mul(PHI, sigma_inv), polarization(sigma)
    assert kernel(psi, 61) != kernel(PHI, 61)
    numerator = mul(psi, adj(PHI))
    # The candidate global map is numerator/61. Its 61-adic denominator is real.
    assert reduce(numerator, 61) != nmod_mat(4, 4, 61)
    assert (3*5*7*13*17)**2 > 8 * 2**3 * 61**2
    for prime in [3, 5, 7, 13, 17]:
        base, marked = reduce(PHI, prime), reduce(psi, prime)
        local_u = marked * base.inv()
        assert local_u * base == marked
        assert field_adj(local_u, prime) * reduce(h, prime) * local_u == reduce(eye(2), prime)


def test_unknown_common_weak_scalars_cancel_in_polarization_transport():
    sigma, _ = compile_word(ROOTS[-1])
    s = mul(adj(sigma), sigma)
    h = polarization(sigma)
    for prime in [3, 5, 7, 13, 17]:
        for scalar in range(1, prime):
            weak_basis = scalar * reduce(PHI, prime)
            assert weak_basis * reduce(s, prime) * weak_basis.inv() == reduce(h, prime)


def test_arbitrary_unpolarized_lift_does_not_satisfy_symplectic_contract():
    sigma, _ = compile_word(((0, 2, 1),))
    a = reduce(sigma, 61)
    assert field_adj(a, 61) * a != reduce(eye(2), 61)
    with pytest.raises(ValueError, match='not integral'):
        polarization(sigma)

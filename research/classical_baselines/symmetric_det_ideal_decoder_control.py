"""One exact Sage ideal-label falsifier; not an actual-source quantum run."""
import json
from sage.all import GF, PolynomialRing, binomial, diagonal_matrix, matrix, set_random_seed, vector


def pairs(n):
    return [(i, j) for i in range(n) for j in range(i, n)]


def sym(v, n):
    out = matrix(v.base_ring(), n, n)
    for a, (i, j) in zip(v, pairs(n)):
        out[i, j] = out[j, i] = a
    return out


def decode(labels, n):
    """Public decoder: labels and dimension only, with no producer secrets."""
    field = labels[0].base_ring()
    N = n * (n + 1) // 2
    h = int(binomial(n + 3, 4))
    monomials = pairs(N)
    train = matrix(field, [[v[i] * v[j] for i, j in monomials] for v in labels[:h]])
    assert train.rank() == h
    ring = PolynomialRing(field, N, 'y')
    ys = ring.gens()
    quadrics = [sum(c * ys[i] * ys[j] for c, (i, j) in zip(row, monomials))
                for row in train.right_kernel().basis()]
    frame = labels[h:h + n]
    tangents = []
    for v in frame:
        jac = matrix(field, [[q.derivative(y)(*v) for y in ys] for q in quadrics])
        tangent = jac.right_kernel()
        assert tangent.dimension() == n
        tangents.append(tangent)
    mixed = {}
    for i in range(n):
        for j in range(i + 1, n):
            intersection = tangents[i].intersection(tangents[j])
            assert intersection.dimension() == 1
            mixed[i, j] = intersection.basis()[0]
    cols = [frame[i] if i == j else mixed[i, j] for i, j in pairs(n)]
    basis = matrix(field, cols).transpose()
    assert basis.is_invertible()
    coefficients = basis.solve_right(labels[h + n])
    assert all(coefficients)
    U = basis * diagonal_matrix(coefficients)
    D = diagonal_matrix(field, [1 if i == j else 2 for i, j in pairs(n)])
    candidate = D.inverse() * U.transpose() * D
    return candidate, U, {'training_rank': int(train.rank()),
                          'quadratic_ideal_dimension': len(quadrics),
                          'tangent_dimensions': [int(t.dimension()) for t in tangents],
                          'frame_rank': int(basis.rank())}


def run():
    n, p, seed = 3, 65537, 20261106
    set_random_seed(seed)
    field = GF(p)
    N = n * (n + 1) // 2
    h = int(binomial(n + 3, 4))
    for _ in range(100):
        L = matrix(field, N, N, [field.random_element() for _ in range(N * N)])
        if L.is_invertible():
            break
    else:
        raise AssertionError('producer invertible-map cap exhausted')
    D = diagonal_matrix(field, [1 if i == j else 2 for i, j in pairs(n)])
    Ladj = D.inverse() * L.transpose() * D
    labels = []
    for _ in range(h + n + 1):
        for _ in range(100):
            u = vector(field, [field.random_element() for _ in range(n)])
            t = field.random_element()
            if u and t:
                break
        else:
            raise AssertionError('producer nonzero-point cap exhausted')
        v = vector(field, [t * u[i] * u[j] for i, j in pairs(n)])
        labels.append(Ladj * v)
    candidate, U, ledger = decode(labels, n)
    # Truth is used only here, after the public decoder has returned.
    ring = PolynomialRing(field, N, 'x')
    xs = vector(ring, ring.gens())
    truth = sym(L.change_ring(ring) * xs, n).determinant()
    recovered = sym(candidate.change_ring(ring) * xs, n).determinant()
    monomial = truth.monomials()[0]
    def proportional(poly):
        scale = poly.monomial_coefficient(monomial) / truth.monomial_coefficient(monomial)
        return bool(scale and poly == scale * truth), scale
    correct, scale = proportional(recovered)
    wrong_adjoint = sym(U.transpose().change_ring(ring) * xs, n).determinant()
    wrong_inverse = sym((D.inverse() * U.inverse().transpose() * D).change_ring(ring) * xs, n).determinant()
    assert correct
    assert not proportional(wrong_adjoint)[0]
    assert not proportional(wrong_inverse)[0]
    return {'scope': 'One exact ideal-label decoder control; no actual contaminated-source or quantum execution',
            'n': n, 'p': p, 'seed': seed, 'labels': len(labels), **ledger,
            'exact_projective_polynomial_identity': correct,
            'projective_scale': int(scale), 'ignored_trace_factor_rejected': True,
            'wrong_inverse_transpose_rejected': True}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))

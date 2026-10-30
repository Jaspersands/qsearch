"""Symbolic elliptic module control, not the genus41 matrix adapter."""

from itertools import combinations_with_replacement

from flint import nmod_mat
from sympy import Matrix, Poly, eye, symbols, zeros


u, v = symbols("u v")
SHIFTS = (0, 1, 1, 2)


def reduce_polynomial(value, prime=17):
    return Poly(value, u, v, modulus=prime).as_expr()


def actions(prime=17):
    # Basis(1,x,y,xy) over F_p[u,v], with affine u=1 and v=x^2.
    x = Matrix([[0, u*v, 0, 0], [1, 0, 0, 0],
                [0, 0, 0, u*v], [0, 0, 1, 0]])
    y = Matrix([[0, 0, 2*u**2, u*v**2+2*u**2*v],
                [0, 0, v+2*u, 2*u**2], [1, 0, 0, 0], [0, 1, 0, 0]])
    return [u*eye(4), v*eye(4), x, y]


def certify(matrices, prime=17):
    for matrix in matrices:
        for i in range(4):
            for j in range(4):
                polynomial = Poly(matrix[i, j], u, v, modulus=prime)
                assert polynomial.is_zero or all(sum(monomial) == 1+SHIFTS[j]-SHIFTS[i]
                                                 for monomial, _ in polynomial.terms())
    for a in matrices:
        for b in matrices:
            assert (a*b-b*a).applyfunc(lambda z: reduce_polynomial(z, prime)) == zeros(4)
    U, V, X, Y = matrices
    assert U == u*eye(4) and V == v*eye(4)
    for relation in (X*X-U*V, Y*Y-V*X-2*U*X-2*U*U):
        assert relation.applyfunc(lambda z: reduce_polynomial(z, prime)) == zeros(4)
    one = Matrix([1, 0, 0, 0])
    assert X*one == Matrix([0, 1, 0, 0])
    assert Y*one == Matrix([0, 0, 1, 0])
    assert X*Y*one == Matrix([0, 0, 0, 1])
    return True


def graded_coordinates(vector, degree, prime=17):
    coordinates = []
    for value, shift in zip(vector, SHIFTS):
        polynomial = Poly(value, u, v, modulus=prime)
        assert polynomial.is_zero or all(sum(monomial)+shift == degree for monomial, _ in polynomial.terms())
        for power in range(degree-shift+1):
            coordinates.append(int(polynomial.coeff_monomial(u**power*v**(degree-shift-power))) % prime)
    return coordinates


def degree_control(degree, prime=17):
    matrices = actions(prime)
    rows = []
    for monomial in combinations_with_replacement(range(4), degree):
        vector = Matrix([1, 0, 0, 0])
        for index in monomial:
            vector = (matrices[index]*vector).applyfunc(lambda z: reduce_polynomial(z, prime))
        rows.append(graded_coordinates(vector, degree, prime))
    rank = nmod_mat(rows, prime).rank()
    expected = 1 if degree == 0 else 4*degree
    assert rank == expected
    return {"degree": degree, "free_piece_dimension": len(rows[0]),
            "generated_rank": rank, "monomials_used_only_in_small_control": len(rows)}


if __name__ == "__main__":
    import json
    assert certify(actions())
    print(json.dumps({"status": "EXACT_ELLIPTIC_MODULE_CONTROL_ONLY",
                      "degree_checks": [degree_control(j) for j in range(8)],
                      "native_genus41_adapter_implemented": False}, indent=2))

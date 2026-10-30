"""Known Schur quotient lifts a complete AG code by one rational point.

The algorithm consumes only a matrix. Its geometric interpretation requires
the COMPLETE AG-code promise; passing dimension checks does not prove it.
"""

from flint import fmpz, nmod_mat


def rows(matrix):
    return [[int(matrix[i, j]) for j in range(matrix.ncols())]
            for i in range(matrix.nrows())]


def span(matrix):
    reduced, rank = matrix.rref()
    return nmod_mat(rows(reduced)[:rank], matrix.modulus())


def orthogonal(matrix):
    kernel, dimension = matrix.nullspace()
    return nmod_mat([[int(kernel[i, j]) for i in range(matrix.ncols())]
                     for j in range(dimension)], matrix.modulus())


def schur(left, right):
    p = left.modulus()
    return span(nmod_mat([[int(left[i, x])*int(right[j, x]) % p
                           for x in range(left.ncols())]
                          for i in range(left.nrows()) for j in range(right.nrows())], p))


def lift_point(parity_rows, prime, point_index=0):
    data = [list(row) for row in parity_rows]
    if (type(prime) is not int or not 3 <= prime < 2**63 or not fmpz(prime).is_prime()
            or len(data) < 2 or not data[0] or any(len(row) != len(data[0]) for row in data)
            or any(type(x) is not int or not 0 <= x < prime for row in data for x in row)):
        raise ValueError("canonical full-rank matrix over a verified odd prime required")
    B = nmod_mat(data, prime)
    k, m = B.nrows(), B.ncols()
    if (B.rank() != k or type(point_index) is not int or not 0 <= point_index < m
            or not any(row[point_index] for row in data)):
        raise ValueError("independent rows and a nonzero selected column required")
    full_square = schur(B, B)
    w = full_square.nrows()
    d, g = w-k, w-2*k+1
    if g < 1 or d < 2*g+1 or m < 2*d+4:
        raise ValueError("inferred AG degrees outside the proved point-lift range")
    keep = [i for i in range(m) if i != point_index]
    V0 = nmod_mat([[row[i] for i in keep] for row in data], prime)
    coefficients = orthogonal(nmod_mat([[row[point_index] for row in data]], prime))
    Vminus = coefficients*V0
    W = schur(V0, V0)
    lifted = orthogonal(schur(Vminus, orthogonal(W)))
    if V0.rank() != k or Vminus.rank() != k-1 or lifted.nrows() != k+1:
        raise ValueError("point lift failed its necessary dimension checks")
    extension = next((row for row in rows(lifted)
                      if nmod_mat(rows(V0)+[row], prime).rank() == k+1), None)
    if extension is None:
        raise ArithmeticError("missing strict extension of the original punctured code")
    adapted = nmod_mat(rows(V0)+[extension], prime)
    if nmod_mat(rows(adapted)+rows(lifted), prime).rank() != k+1:
        raise ArithmeticError("adapted basis does not span the computed quotient")
    new_square = schur(adapted, adapted)
    if new_square.nrows() != 2*(d+1)+1-g:
        raise ValueError("lifted square failed its necessary AG dimension check")
    projective = []
    for index, row in enumerate(rows(adapted)):
        row.insert(point_index, int(index == k))
        projective.append(row)
    if schur(nmod_mat(projective, prime), nmod_mat(projective, prime)).nrows() != new_square.nrows():
        raise ValueError("recovered point violates the lifted quadratic relations")
    return {
        "original_matrix": data, "point_index": point_index,
        "inferred_genus_under_AG_promise": g, "inferred_degree_under_AG_promise": d,
        "punctured_original": rows(V0), "shortened_original": rows(Vminus),
        "punctured_square": rows(W), "lifted_punctured": rows(adapted),
        "lifted_projective_points_as_columns": projective,
        "lifted_dimension": k+1, "lifted_degree_under_AG_promise": d+1,
        "lifted_square_dimension": new_square.nrows(),
        "lifted_quadratic_relation_dimension": (k+1)*(k+2)//2-new_square.nrows(),
        "geometric_interpretation_requires_complete_AG_promise": True,
        "AG_promise_verified_by_dimension_checks": False,
        "curve_ideal_generators_explicitly_emitted": False,
        "graded_algebra_backend_implemented": False,
        "native_search_solved_by_lift": False,
        "quantum_advantage_established": False,
    }

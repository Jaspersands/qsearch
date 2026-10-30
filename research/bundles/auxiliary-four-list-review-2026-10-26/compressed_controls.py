"""Independent genus-two reconstruction and failure controls over F_17."""

from itertools import combinations, combinations_with_replacement
import importlib.util
import json

from flint import nmod_mat
from sympy import Matrix, Poly, eye, symbols, zeros


P = 17
u, v, x, z, y = symbols("u v x z y")
VARIABLES = (u, v, x, z, y)
SHIFTS = (0, 1, 1, 1, 2, 2)
E = [eye(6)[:, i] for i in range(6)]
QUADRICS = (x*x-u*z, x*z-u*v, z*z-v*x, y*y-v*z-u*x-u*u)


def reduced(value):
    return Poly(value, u, v, modulus=P).as_expr()


def reduce_matrix(value):
    return value.applyfunc(reduced)


def exponents(n, degree):
    result = []
    for word in combinations_with_replacement(range(n), degree):
        result.append(tuple(word.count(i) for i in range(n)))
    return result


def quotient_dimension(relations, variables, degree):
    mons = exponents(len(variables), degree)
    positions = {mon: i for i, mon in enumerate(mons)}
    rows = []
    if degree >= 2:
        for relation in relations:
            terms = Poly(relation, *variables, modulus=P).terms()
            for multiplier in exponents(len(variables), degree-2):
                row = [0] * len(mons)
                for mon, coefficient in terms:
                    combined = tuple(a+b for a, b in zip(mon, multiplier))
                    row[positions[combined]] = int(coefficient) % P
                rows.append(row)
    rank = nmod_mat(rows, P).rank() if rows else 0
    return len(mons)-rank


def free_coordinates(vector, degree):
    result = []
    for value, shift in zip(vector, SHIFTS):
        poly = Poly(value, u, v, modulus=P)
        assert poly.is_zero or all(sum(mon)+shift == degree for mon, _ in poly.terms())
        for i in range(degree-shift+1):
            result.append(int(poly.coeff_monomial(u**i*v**(degree-shift-i))) % P)
    return result


def from_coordinates(coordinates, degree):
    result, offset = [], 0
    for shift in SHIFTS:
        value = 0
        for i in range(degree-shift+1):
            value += coordinates[offset] * u**i * v**(degree-shift-i)
            offset += 1
        result.append(value)
    assert offset == len(coordinates)
    return Matrix(result)


def symmetric_table(entries):
    result = {}
    for (i, j), value in entries.items():
        result[i, j] = result[j, i] = value
    return result


def cubic_system(table):
    def known_product(i, value):
        result = value[0] * E[i+1]
        for j in range(3):
            result += value[j+1] * table[i, j]
        return result

    rows, right, distinct = [], [], []
    for i, j in combinations(range(3), 2):
        for k in range(3):
            row = [0] * 6
            for a in range(2):
                row[2*i+a] += int(table[j, k][4+a])
                row[2*j+a] -= int(table[i, k][4+a])
            rhs = known_product(j, table[i, k])-known_product(i, table[j, k])
            rows.append([c % P for c in row])
            right.append(free_coordinates(rhs, 3))
            if k not in (i, j):
                distinct.append(row)
    return rows, right, distinct


def solve_full_column(matrix, right):
    n = len(matrix[0])
    augmented = [[c % P for c in a+b] for a, b in zip(matrix, right)]
    for column in range(n):
        pivot = next(i for i in range(column, len(augmented)) if augmented[i][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = pow(augmented[column][column], -1, P)
        augmented[column] = [scale*c % P for c in augmented[column]]
        for i in range(len(augmented)):
            if i != column:
                factor = augmented[i][column]
                augmented[i] = [(a-factor*b) % P for a, b in zip(augmented[i], augmented[column])]
    assert all(not any(row) for row in augmented[n:])
    solution = [row[n:] for row in augmented[:n]]
    for row, rhs in zip(matrix, right):
        assert [sum(a*solution[i][j] for i, a in enumerate(row)) % P
                for j in range(len(rhs))] == rhs
    return solution


def reconstruct(table):
    rows, right, distinct = cubic_system(table)
    solution = solve_full_column(rows, right)
    matrices = []
    for i in range(3):
        columns = [E[i+1]] + [table[i, j] for j in range(3)]
        columns += [from_coordinates(solution[2*i+a], 3) for a in range(2)]
        matrices.append(reduce_matrix(Matrix.hstack(*columns)))
    return matrices, {"equations": len(rows), "unknowns": 6, "rhs_coordinates": len(right[0]),
                      "rank": nmod_mat(rows, P).rank(),
                      "distinct_triples_only_rank": nmod_mat(distinct, P).rank()}


def certify(matrices):
    X, Z, Y = matrices
    for action in matrices:
        for i in range(6):
            for j in range(6):
                polynomial = Poly(action[i, j], u, v, modulus=P)
                assert polynomial.is_zero or all(sum(mon) == 1+SHIFTS[j]-SHIFTS[i]
                                                 for mon, _ in polynomial.terms())
    assert all(reduce_matrix(a*b-b*a) == zeros(6) for a in matrices for b in matrices)
    relations = (X*X-u*Z, X*Z-u*v*eye(6), Z*Z-v*X,
                 Y*Y-v*Z-u*X-u*u*eye(6))
    assert all(reduce_matrix(relation) == zeros(6) for relation in relations)
    assert X*E[0] == E[1] and Z*E[0] == E[2] and Y*E[0] == E[3]
    assert reduce_matrix(X*Y*E[0]) == E[4] and reduce_matrix(Z*Y*E[0]) == E[5]


def main():
    affine = Poly(x**5+x+1, x, modulus=P)
    assert affine.gcd(affine.diff()).degree() == 0
    table = symmetric_table({(0, 0): u*E[2], (0, 1): u*v*E[0],
                             (0, 2): E[4], (1, 1): v*E[1],
                             (1, 2): E[5], (2, 2): v*E[2]+u*E[1]+u*u*E[0]})
    matrices, cubic_record = reconstruct(table)
    certify(matrices)
    X, Z, Y = matrices
    expected = [u*E[5], u*v*E[3], u*v*E[3], v*E[4],
                u*v*v*E[0]+u*u*E[1]+u*u*E[2],
                u*u*v*E[0]+v*v*E[1]+u*u*E[2]]
    assert all(reduce_matrix(action[:, 4+a]-expected[2*i+a]) == zeros(6, 1)
               for i, action in enumerate(matrices) for a in range(2))

    degree_records = []
    cached = {(0,)*5: E[0]}
    all_actions = [u*eye(6), v*eye(6), X, Z, Y]
    for degree in range(8):
        rows = []
        for mon in exponents(5, degree):
            if degree:
                index = next(i for i, power in enumerate(mon) if power)
                previous = list(mon)
                previous[index] -= 1
                cached[mon] = reduce_matrix(all_actions[index]*cached[tuple(previous)])
            rows.append(free_coordinates(cached[mon], degree))
        direct = quotient_dimension(QUADRICS, VARIABLES, degree)
        generated = nmod_mat(rows, P).rank()
        expected_dimension = 1 if degree == 0 else 6*degree-1
        assert direct == generated == len(rows[0]) == expected_dimension
        degree_records.append({"degree": degree, "macaulay_quotient": direct,
                               "module_generated_rank": generated})

    # Mix generators with each other and the parameters, and rescale one.
    transform = Matrix.hstack(E[0], E[1]+2*E[2]+3*u*E[0],
                              5*E[2]+v*E[0], E[3]+4*E[1], E[4], E[5])
    inverse = reduce_matrix(transform.inv_mod(P)) if not transform.free_symbols else None
    if inverse is None:
        inverse = transform.inv().applyfunc(lambda c: Poly(c, u, v).as_expr())
        inverse = inverse.applyfunc(lambda c: sum((int(co.numerator)*pow(int(co.denominator), -1, P) % P)
                                                  * u**mon[0] * v**mon[1]
                                                  for mon, co in Poly(c, u, v).terms()))
    changed = [reduce_matrix(inverse*a*transform) for a in
               (X+2*Z+3*u*eye(6), 5*Z+v*eye(6), Y+4*X)]
    changed_table = symmetric_table({(i, j): changed[i][:, j+1]
                                     for i in range(3) for j in range(i, 3)})
    rebuilt, changed_record = reconstruct(changed_table)
    assert all(reduce_matrix(a-b) == zeros(6) for a, b in zip(rebuilt, changed))
    assert all(reduce_matrix(a*b-b*a) == zeros(6) for a in rebuilt for b in rebuilt)

    bad_quadrics = [q.subs({v: -x, y: u+x}, simultaneous=True).expand() for q in QUADRICS]
    bad_hilbert = [quotient_dimension(bad_quadrics, (u, x, z), degree) for degree in range(5)]
    assert bad_hilbert == [1, 3, 2, 1, 1]
    zero = zeros(6, 1)
    bad_table = symmetric_table({(0, 0): E[4], (0, 1): E[5], (0, 2): zero,
                                 (1, 1): zero, (1, 2): -E[5], (2, 2): zero})
    bad_matrix, _, _ = cubic_system(bad_table)
    bad_rank = nmod_mat(bad_matrix, P).rank()
    assert bad_rank == 5
    assert all(q.subs({u: 1, v: 0, x: 0, z: 0, y: 1}) == 0 for q in QUADRICS)

    rows, _, _ = cubic_system(table)
    # Recover signed rows before reducing to each prime.
    rows_signed = [[a if a <= P//2 else a-P for a in row] for row in rows]
    ranks_by_characteristic = {str(p): nmod_mat(rows_signed, p).rank() for p in (2, 3, 5, 17)}
    assert set(ranks_by_characteristic.values()) == {6}
    spec = importlib.util.spec_from_file_location("parent_compressed_control", "compressed_inputs/control.py")
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    relabel = Matrix.diag(1, -1, -1, 1)
    relabelled_actions = [relabel*a*relabel for a in parent.actions()]
    assert parent.certify(relabelled_actions)
    one4 = Matrix([1, 0, 0, 0])
    assert relabelled_actions[2]*one4 == Matrix([0, -1, 0, 0])
    assert relabelled_actions[3]*one4 == Matrix([0, 0, -1, 0])
    b, g = 42, 41
    equations, unknowns, rhs = b*(b-1)//2*b, b*g, 4+3*b+2*g
    print(json.dumps({"status": "INDEPENDENT_SMALL_GENUS_TWO_CONTROL_ONLY",
                      "curve": "y^2=x^5+x+1 over F_17, H=6 infinity",
                      "squarefree": True, "cubic": cubic_record,
                      "degree_checks": degree_records, "changed_basis_cubic": changed_record,
                      "bad_pencil": {"forms": ["v+x", "v+y-u"],
                                     "common_point": [1, 0, 0, 0, 1],
                                     "quotient_dimensions_0_to_4": bad_hilbert,
                                     "cubic_rank": bad_rank, "cubic_cokernel": 6-bad_rank},
                      "abstract_good_coefficient_ranks_by_characteristic": ranks_by_characteristic,
                      "parent_demo_certificate_countercontrol": {
                          "conjugation": "diag(1,-1,-1,1)",
                          "demo_certify_accepts": True,
                          "named_beta_basis_relations_hold": False,
                          "written_strong_certificate_accepts": False},
                      "genus41_counts_only": {"equations": equations, "unknowns": unknowns,
                                               "rhs": rhs, "dense_coefficients": equations*unknowns,
                                               "dense_augmented_entries": equations*(unknowns+rhs),
                                               "streamed_pivot_augmented_entries": unknowns*(unknowns+rhs)},
                      "native_backend_implemented": False}, indent=2))


if __name__ == "__main__":
    main()

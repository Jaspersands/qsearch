"""ONE finite n=4 control, not an all-n classification or learner.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python.
It constructs the PROPOSED top space from q-linears and E_ij (not an
empirical Bell distribution), computes its infinitesimal symplectic
stabilizer, and falsifies the commutator-common-kernel shortcut.
The independent symbolic proof is in the dated cubic-axis review.
"""

import json
from itertools import combinations
from sage.all import GF, matrix, vector


def infinitesimal_stabilizer(n, space):
    """Shared finite-control linear algebra on a supplied exterior top space."""
    size = 2 * n
    field = GF(2)
    triples = list(combinations(range(size), 3))
    indices = {triple: i for i, triple in enumerate(triples)}
    basis = space.basis()
    normals = space.basis_matrix().right_kernel().basis_matrix()

    symplectic_basis = []
    for i in range(n):
        for j in range(n):
            operator = matrix(field, size)
            operator[i, j] = 1
            operator[n + j, n + i] = 1
            symplectic_basis.append(operator)
    for upper in (True, False):
        for i in range(n):
            for j in range(i, n):
                operator = matrix(field, size)
                if upper:
                    operator[i, n + j] = operator[j, n + i] = 1
                else:
                    operator[n + i, j] = operator[n + j, i] = 1
                symplectic_basis.append(operator)

    def act(operator, form):
        result = vector(field, len(triples))
        for triple, coefficient in zip(triples, form):
            if not coefficient:
                continue
            for old in triple:
                for new in range(size):
                    if operator[old, new]:
                        target = tuple(sorted((set(triple) - {old}) | {new}))
                        if len(target) == 3:
                            result[indices[target]] += 1
        return result

    columns = []
    for operator in symplectic_basis:
        column = []
        for form in basis:
            column.extend(normals * act(operator, form))
        columns.append(column)
    coefficients = matrix(field, columns).transpose().right_kernel().basis()
    lie = []
    for coefficient in coefficients:
        operator = matrix(field, size)
        for bit, term in zip(coefficient, symplectic_basis):
            if bit:
                operator += term
        lie.append(operator)
    return lie


def main():
    n = 4
    size = 2 * n
    field = GF(2)
    triples = list(combinations(range(size), 3))
    indices = {triple: i for i, triple in enumerate(triples)}

    def wedge_terms(terms):
        result = vector(field, len(triples))
        for term in terms:
            if len(set(term)) == 3:
                result[indices[tuple(sorted(term))]] += 1
        return result

    q_linears = [wedge_terms([(i, n + i, k) for i in range(n)])
                 for k in range(size)]
    cubics = [wedge_terms([(i, j, n + i), (i, j, n + j)])
              for i, j in combinations(range(n), 2)]
    space = matrix(field, q_linears + cubics).row_space()
    lie = infinitesimal_stabilizer(n, space)

    commutator_rows = []
    for left, right in combinations(lie, 2):
        commutator_rows.extend((left * right + right * left).rows())
    common_kernel = matrix(field, commutator_rows).right_kernel()
    axis = vector(field, [0] * n + [1] * n)
    result = {
        "scope": "finite n=4 top-space control only; no Bell/source/learner theorem",
        "n": n,
        "top_space_dimension": int(space.dimension()),
        "lie_dimension": len(lie),
        "commutator_common_kernel_dimension": int(common_kernel.dimension()),
        "target_axis_in_kernel": axis in common_kernel,
        "all_lie_operators_preserve_axis_line": all(
            operator * axis in [0 * axis, axis] for operator in lie),
        "commutator_shortcut_falsified": common_kernel.dimension() != 1,
    }
    assert result["top_space_dimension"] == 13
    assert result["lie_dimension"] == 6
    assert result["commutator_common_kernel_dimension"] == 8
    assert result["commutator_shortcut_falsified"]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

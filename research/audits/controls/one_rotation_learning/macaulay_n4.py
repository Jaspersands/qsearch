"""ONE exact n=4 support-to-axis covariance/Macaulay control.

The 256 Bell labels are enumerated ONLY as finite validation truth.
The decoder receives the transformed support and known symplectic form.
It obtains K3 by evaluation and performs the prescribed degree-3 Macaulay
algorithm; it NEVER enumerates coefficient assignments or rank-one matrices.
No quantum learner, support-gap experiment, or all-n theorem is executed.
"""

import json
from itertools import combinations
from pathlib import Path
from sage.all import GF, VectorSpace, identity_matrix, matrix, vector

from lie_n4 import infinitesimal_stabilizer

FIELD = GF(2)
N_QUBITS = 4
N_BITS = 2 * N_QUBITS
MASK = (1 << N_QUBITS) - 1
GATES = [("H", 0), ("S", 1), ("CX", 1, 2), ("CX", 3, 0)]


def bits(label, dimension):
    return vector(FIELD, [(label >> i) & 1 for i in range(dimension)])


def packed(value):
    return sum(int(bit) << i for i, bit in enumerate(value))


def monomials(dimension, degree):
    return [sum(1 << i for i in term)
            for k in range(degree + 1)
            for term in combinations(range(dimension), k)]


def canonical_support(label):
    x, z = label & MASK, label >> N_QUBITS
    return ((x & z).bit_count() % 2 == 0
            and ((x & z) == 0 or (x & (z ^ MASK)) == 0))


def bell_pullback(label):
    """Affine Bell relabeling, copied from the independent Bell control."""
    x, z = label & MASK, label >> N_QUBITS
    for gate in reversed(GATES):
        name, j = gate[:2]
        if name == "H":
            flip = ((x ^ z) >> j) & 1
            x ^= flip << j
            z ^= flip << j
        elif name == "S":
            z ^= (((x >> j) & 1) ^ 1) << j
        else:
            k = gate[2]
            x ^= ((x >> j) & 1) << k
            z ^= ((z >> k) & 1) << j
    return x | (z << N_QUBITS)


def physical_pauli_forward(label):
    """Independent forward Pauli conjugation; no Bell affine offset."""
    x, z = label & MASK, label >> N_QUBITS
    for gate in GATES:
        name, j = gate[:2]
        if name == "H":
            x_bit, z_bit = (x >> j) & 1, (z >> j) & 1
            x = (x & ~(1 << j)) | (z_bit << j)
            z = (z & ~(1 << j)) | (x_bit << j)
        elif name == "S":
            z ^= ((x >> j) & 1) << j
        else:
            target = gate[2]
            x ^= ((x >> j) & 1) << target
            z ^= ((z >> target) & 1) << j
    return x | (z << N_QUBITS)


def decode(support, n):
    size = 2 * n
    j_form = matrix(FIELD, size)
    for i in range(n):
        j_form[i, n + i] = j_form[n + i, i] = 1

    mons = monomials(size, 3)
    evaluation = matrix(FIELD, [
        [int(label & monomial == monomial) for monomial in mons]
        for label in support])
    k3 = evaluation.right_kernel()
    quadratic_indices = [i for i, monomial in enumerate(mons)
                         if monomial.bit_count() <= 2]
    k2_dimension = evaluation.matrix_from_columns(
        quadratic_indices).right_kernel().dimension()
    cubic_indices = [i for i, monomial in enumerate(mons)
                     if monomial.bit_count() == 3]
    top = k3.basis_matrix().matrix_from_columns(cubic_indices).row_space()
    lie = infinitesimal_stabilizer(n, top)
    assert all(left * right == right * left
               for left, right in combinations(lie, 2))

    square_map = matrix(FIELD, [(operator * operator).list()
                               for operator in lie]).transpose()
    nilpotents = []
    for coefficient in square_map.right_kernel().basis():
        operator = matrix(FIELD, size)
        for bit, term in zip(coefficient, lie):
            if bit:
                operator += term
        assert operator * operator == 0
        nilpotents.append(operator)
    common_kernel = matrix(FIELD, [row for operator in nilpotents
                                   for row in operator.rows()]).right_kernel()
    assert all(left * j_form * right == 0
               for left in common_kernel.basis()
               for right in common_kernel.basis())

    def intrinsic_diagonal(operator):
        product = j_form * operator
        return j_form * vector(FIELD, [product[i, i] for i in range(size)])

    lambdas = [intrinsic_diagonal(operator) for operator in nilpotents]
    covectors = [list(value * j_form) for value in lambdas]
    coefficient_count = len(nilpotents)
    cmons = monomials(coefficient_count, 3)
    cindex = {monomial: i for i, monomial in enumerate(cmons)}
    equations = []
    for row in range(size):
        for column in range(size):
            equation = vector(FIELD, len(cmons))
            for i, operator in enumerate(nilpotents):
                equation[cindex[1 << i]] += operator[row, column]
            for i in range(coefficient_count):
                for j in range(coefficient_count):
                    equation[cindex[(1 << i) | (1 << j)]] += (
                        lambdas[i][row] * covectors[j][column])
            equations.append(equation)
    equation_space = matrix(FIELD, equations).row_space()

    macaulay_rows = list(equation_space.basis())
    for equation in equation_space.basis():
        for variable in range(coefficient_count):
            product = vector(FIELD, len(cmons))
            for monomial, coefficient in zip(cmons, equation):
                if coefficient:
                    product[cindex[monomial | (1 << variable)]] += coefficient
            macaulay_rows.append(product)
    macaulay = matrix(FIELD, macaulay_rows).row_space().basis_matrix()
    degree_three = [i for i, monomial in enumerate(cmons)
                    if monomial.bit_count() == 3]
    low_combinations = macaulay.matrix_from_columns(
        degree_three).transpose().right_kernel().basis_matrix()
    quadratic_relations = (low_combinations * macaulay).row_space().basis_matrix()
    affine = [i for i, monomial in enumerate(cmons) if monomial.bit_count() <= 1]
    quadratic = [i for i, monomial in enumerate(cmons) if monomial.bit_count() == 2]
    quadratic_block = quadratic_relations.matrix_from_columns(quadratic)
    assert quadratic_block.is_square() and quadratic_block.is_invertible()
    rewritten = quadratic_block.inverse() * quadratic_relations
    products = rewritten.matrix_from_columns(affine)
    pair_index = {cmons[index]: row for row, index in enumerate(quadratic)}
    algebra_dimension = coefficient_count + 1
    algebra_identity = identity_matrix(FIELD, algebra_dimension)
    multiplication = []
    for variable in range(coefficient_count):
        columns = []
        columns.append(vector(FIELD, [int(j == variable + 1)
                                      for j in range(algebra_dimension)]))
        for other in range(coefficient_count):
            if variable == other:
                columns.append(columns[0])
            else:
                columns.append(products.row(pair_index[(1 << variable) | (1 << other)]))
        operator = matrix(FIELD, columns).transpose()
        assert operator * operator == operator
        multiplication.append(operator)
    assert all(left * right == right * left
               for left, right in combinations(multiplication, 2))

    # At most algebra_dimension live subspaces; no coefficient-assignment search.
    joint_spaces = [(VectorSpace(FIELD, algebra_dimension), ())]
    maximum_live_spaces = 1
    for operator in multiplication:
        refined = []
        for eigenvalue in (0, 1):
            eigenspace = (operator - eigenvalue * algebra_identity).right_kernel()
            for subspace, labels in joint_spaces:
                intersection = subspace.intersection(eigenspace)
                if intersection.dimension():
                    refined.append((intersection, labels + (eigenvalue,)))
        joint_spaces = refined
        maximum_live_spaces = max(maximum_live_spaces, len(joint_spaces))
    assert len(joint_spaces) == algebra_dimension
    assert all(subspace.dimension() == 1 for subspace, _ in joint_spaces)
    candidates = []
    ranks = []
    for _, coefficients in joint_spaces:
        operator = matrix(FIELD, size)
        for bit, term in zip(coefficients, nilpotents):
            if bit:
                operator += term
        rank = int(operator.rank())
        ranks.append(rank)
        assert rank in (0, 1)
        if rank:
            candidates.append(packed(intrinsic_diagonal(operator)))
    return sorted(candidates), {
        "k2_dimension": int(k2_dimension),
        "k3_dimension": int(k3.dimension()),
        "top_dimension": int(top.dimension()),
        "lie_dimension": len(lie),
        "square_zero_dimension": len(nilpotents),
        "common_kernel_dimension": int(common_kernel.dimension()),
        "initial_rank_one_equation_dimension": int(equation_space.dimension()),
        "macaulay_degree_at_most_two_relation_dimension": quadratic_relations.nrows(),
        "quotient_algebra_dimension": algebra_dimension,
        "maximum_joint_eigenspaces": maximum_live_spaces,
        "recovered_matrix_ranks": sorted(ranks),
        "coefficient_assignments_enumerated": 0,
    }


def main():
    support = [label for label in range(1 << N_BITS)
               if canonical_support(bell_pullback(label))]
    candidates, details = decode(support, N_QUBITS)

    # Independent validation truth, supplied ONLY after decoding.
    original_axes = [1 << (N_QUBITS + i) for i in range(N_QUBITS)]
    original_axes.append(MASK << N_QUBITS)
    expected = sorted(physical_pauli_forward(axis) for axis in original_axes)
    forward = matrix(FIELD, [bits(physical_pauli_forward(1 << i), N_BITS)
                             for i in range(N_BITS)]).transpose()
    affine_offset = bell_pullback(0)
    pullback_linear = matrix(FIELD, [bits(bell_pullback(1 << i) ^ affine_offset, N_BITS)
                                     for i in range(N_BITS)]).transpose()
    assert pullback_linear * forward == identity_matrix(FIELD, N_BITS)
    wrong_covariance = sorted(packed(forward.inverse().transpose() * bits(axis, N_BITS))
                              for axis in original_axes)
    assert affine_offset != 0
    assert candidates == expected
    assert candidates != wrong_covariance
    assert len(candidates) == N_QUBITS + 1
    assert details["k3_dimension"] == 14 and details["top_dimension"] == 13
    assert details["quotient_algebra_dimension"] == 6
    result = {
        "scope": "ONE finite n=4 affine support-to-Macaulay control only",
        "n": N_QUBITS,
        "gates": GATES,
        "bell_labels_enumerated_for_validation_truth": 1 << N_BITS,
        "support_size": len(support),
        "nontrivial_affine_pullback_offset": affine_offset,
        "candidate_axes": candidates,
        "independent_forward_pauli_axes": expected,
        "wrong_inverse_transpose_axes": wrong_covariance,
        "forward_covariance_verified": True,
        "inverse_transpose_countercontrol_rejected": True,
        **details,
        "claims": {"full_quantum_learner": False, "asymptotic_from_control": False,
                   "quantum_execution": False, "coefficient_assignment_search": False},
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()

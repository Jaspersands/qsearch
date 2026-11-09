"""Exact finite 3-neighbor/local-data control; not a nonisometry algorithm.

Algebra interpreter: /opt/anaconda3/envs/qsearch-cas/bin/python.
"""
import json
from pathlib import Path
from sage.all import GF, QQ, ZZ, diagonal_matrix, kronecker_symbol, matrix, vector

p, q = 17, 3
A = diagonal_matrix(QQ, [1, p**2, -p**4])
P = matrix(QQ, [[3, 0, QQ(1)/3], [0, 1, 0], [0, 0, QQ(1)/3]])
B = P.transpose()*A*P
assert B == matrix(QQ, [[9, 0, 1], [0, 289, 0], [1, 0, -9280]])
assert all(entry.denominator() == 1 for entry in B.list())
assert P.det() == 1 and A.det() == B.det() == -(p**6)
x = vector(ZZ, [1, 0, 1])
norm_x = x.dot_product(A*x)
assert norm_x == -83520 and norm_x % 9 == 0 and any(a % 3 for a in x)

# Columns generate {y in Z^3: y1-y3=0 mod 3}, not merely a rational subspace.
kernel = matrix(QQ, [[3, 0, 1], [0, 1, 0], [0, 0, 1]])
assert kernel.det() == 3
assert kernel.inverse() == matrix(QQ, [[QQ(1)/3, 0, -QQ(1)/3], [0, 1, 0], [0, 0, 1]])
assert (A*x).change_ring(GF(3)) == vector(GF(3), [1, 0, -1])
assert P.inverse()*kernel == diagonal_matrix(QQ, [1, 1, 3])
assert P.column(2) == x/3
# Clear one common denominator before comparing the two integer lattices.
generators = matrix(ZZ, (3*kernel).transpose().rows()+[x])
target_generators = matrix(ZZ, (3*P).transpose())
joined_HNF = [list(map(int, row)) for row in generators.hermite_form().rows() if any(row)]
target_HNF = [list(map(int, row)) for row in target_generators.hermite_form().rows() if any(row)]
assert joined_HNF == target_HNF

symbols = {'(17/3)': int(kronecker_symbol(17, 3)),
           '(17/2)': int(kronecker_symbol(17, 2)),
           '(-1/17)': int(kronecker_symbol(-1, 17))}
assert list(symbols.values()) == [-1, 1, 1]
valuations = [int(A[j, j].valuation(p)) for j in range(3)]
units = [A[j, j]/p**valuations[j] for j in range(3)]
assert valuations == [0, 2, 4] and units == [1, 1, -1]
assert all(GF(p)(unit).is_square() for unit in units)
assert A.det().valuation(q) == 0
reflection = diagonal_matrix(QQ, [-1, 1, 1])
assert reflection.transpose()*A*reflection == A and reflection.det() == -1

result = {
    'status': 'PASS', 'scope': 'One exact classical basis/lattice/local-symbol fixture, not a numerical nonisometry proof.',
    'p': p, 'neighbor_prime': q,
    'A': [[int(a) for a in row] for row in A.rows()],
    'P_columns': [[str(a) for a in P.column(j)] for j in range(3)],
    'B': [[int(a) for a in row] for row in B.rows()],
    'det_P': str(P.det()), 'det_A_equals_det_B': str(A.det()),
    'neighbor_vector': list(map(int, x)), 'A_norm_x': int(norm_x),
    'A_norm_divisible_by_q_squared': True, 'vector_nonzero_mod_q': True,
    'kernel_lattice': {'condition': 'y1-y3=0 modulo3', 'index_in_Z3': 3,
        'joining_x_over_3_gives_P_lattice': True, 'cleared_denominator_row_HNF': joined_HNF,
        'kernel_index_in_neighbor': 3},
    'local_data': {'Kronecker_symbols': symbols, 'p_Jordan_valuations': valuations,
        'p_Jordan_unit_parts': [str(a) for a in units], 'unit_parts_square_mod_p': True,
        'q_unimodular': True, 'orientation_reversing_integral_A_automorphism_checked': True},
    'source_dependent_inference': {
        'sources': ['kirschmer.txt Theorem5.4.4', 'kirschmer.txt Lemma5.4.9'],
        'argument': 'A quadratic Hecke character for Q(sqrt17), if shown to annihilate all local lattice spinor norms, distinguishes this 3-neighbor because its value on the neighbor idele is (17/3)=-1. Lemma5.4.9 supplies the neighbor spinor norm; Theorem5.4.4 supplies odd-prime local spinor norms.',
        'full_adelic_annihilation_proved_by_this_control': False,
        'nonisometry_numerically_proved': False},
    'claim_gates': {'full_algorithm': False, 'speedup': False, 'full_genus_classification': False,
        'general_no_go': False, 'extrapolation_from_fixture': False, 'quantum_execution': False,
        'novelty': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'determinant': str(A.det()), 'B': result['B'],
    'kernel_lattice': result['kernel_lattice'], 'local_data': result['local_data']}, indent=2))

"""Exact classical nondivision regular-module control, not a quantum solver."""
from pathlib import Path
import json
import random
from sage.all import (QQ, CyclotomicField, QuaternionAlgebra, matrix, vector,
                      block_diagonal_matrix, pari, next_prime)

# Existing classical quadratic-form baseline for Hamilton norm 3.
qf = pari('qfsolve(matdiagonal([1,1,1,1,-3]))')
qfv = [int(t) for t in qf]
assert sum(t*t for t in qfv[:4]) == 3*qfv[4]*qfv[4]
assert qfv[4] != 0

F = CyclotomicField(12)
z = F.gen()
theta = 2 + z
P = theta.minpoly()
assert P.degree() == 4 and P[0] == 13
H = QuaternionAlgebra(QQ, -1, -1, names=('i', 'j', 'k'))
qi, qj, qk = H.gens()
qb = [H(1), qi, qj, qk]

def flat_a(a):
    return vector(QQ, [t for row in range(2) for col in range(2)
                       for t in a[row, col].coefficient_tuple()])

def rho(a):
    """Explicit classical split map over supplied F, where z^3 squares to -1."""
    out = matrix(F, 4, 4)
    ii = z**3
    for row in range(2):
        for col in range(2):
            aa, bb, cc, dd = a[row, col].coefficient_tuple()
            block = matrix(F, [[aa+bb*ii, -cc-dd*ii],
                               [cc-dd*ii, aa-bb*ii]])
            out[2*row:2*row+2, 2*col:2*col+2] = block
    return out

def flat_v(v):
    return vector(QQ, [c for t in v for c in F(t).vector()])

basis = []
for row in range(2):
    for col in range(2):
        for q in qb:
            a = matrix(H, 2, 2)
            a[row, col] = q
            basis.append(a)
images = [rho(a) for a in basis]
# Finite check of the explicit paid split-map interface, not a source oracle.
for ai, a in enumerate(basis):
    for bi, b in enumerate(basis):
        assert rho(a*b) == images[ai]*images[bi]

e11 = matrix(H, [[1, 0], [0, 0]])
e22 = matrix(H, [[0, 0], [0, 1]])
assert e11*e22 == 0 and e11 != 0 and e22 != 0
left_ideal_rank = matrix(QQ, [flat_a(a*e11) for a in basis]).rank()
assert left_ideal_rank == 8  # regular module dimension is 16.

generator = random.Random(731)
for trial in range(16):
    w = vector(F, [sum(generator.randrange(64)*z**k for k in range(4))
                   for _ in range(4)])
    B = matrix(QQ, [flat_v(r*w) for r in images]).transpose()
    if B.det() != 0:
        break
else:
    raise AssertionError('Finite cyclic-vector control exhausted its cap')

coords = B.solve_right(flat_v(theta*w))
x = sum((coords[j]*basis[j] for j in range(16)), matrix(H, 2, 2))
assert rho(x)*w == theta*w
assert rho(x).charpoly() == P.change_ring(F)
assert rho(x).det() == 13

mult_theta = matrix(QQ, [(theta*z**k).vector() for k in range(4)]).transpose()
theta_operator = block_diagonal_matrix([mult_theta]*4)
transport = B.inverse()*theta_operator*B
right = matrix(QQ, [flat_a(a*x) for a in basis]).transpose()
left = matrix(QQ, [flat_a(x*a) for a in basis]).transpose()
assert transport == right and transport != left
assert right.charpoly() == P**4
assert right.det() == 13**4

# Rational reduction certificate of a nonzero determinant.
determinant = B.det()
modulus = next_prime(100)
while determinant.numerator() % modulus == 0 or determinant.denominator() % modulus == 0:
    modulus = next_prime(modulus)
assert determinant.numerator() % modulus != 0

result = {
    'status': 'PASS',
    'scope': 'One exact classical split-map/regular-module control; no native quantum solver.',
    'classical_qfsolve_vector': qfv,
    'algebra': 'M2((-1,-1)_Q), degree4, not a division algebra',
    'field': 'Q(zeta12)',
    'theta': '2+zeta12',
    'theta_minpoly': str(P),
    'reduced_norm': 13,
    'regular_module_dimension': 16,
    'proper_left_ideal_dimension': left_ideal_rank,
    'split_map_basis_products_checked': 256,
    'cyclic_vector_trial': trial+1,
    'det_B': str(determinant),
    'nonzero_modulus': int(modulus),
    'right_multiplication_orientation': True,
    'left_multiplication_shortcut_rejected': True,
    'regular_charpoly_is_reduced_charpoly_to_degree': True,
    'full_solver_execution': False,
    'quantum_execution': False,
    'novelty_or_speedup': False,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: classical norm baseline, nondivision regular module and right orientation.')

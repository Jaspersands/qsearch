"""One exact binary-exponent Kummer control, not a general LS implementation."""
import json
from pathlib import Path
from sage.all import GF, QQ, ZZ, Matrix, NumberField, PolynomialRing, next_prime, vector

M = ZZ(2)**40 + 172
delta, g, k = 6, 2, 6
v = 6*M + 2
C = Matrix(ZZ, [[-1, -M], [3, 3*M+1]])
w = vector(ZZ, [-3*M-1, 3])
assert C.det() == -1 and C*w == vector(ZZ, [1, 0])
# Exponents are integer pairs throughout; no polynomial of degree M is made.
image_T = C*vector(ZZ, [1, 0])
image_Y = C*vector(ZZ, [0, 1])
assert image_T == vector(ZZ, [-1, 3])
assert image_Y == vector(ZZ, [-M, 3*M+1])
assert 6*image_Y-v*image_T == vector(ZZ, [2, 0])
assert C*vector(ZZ, [-3*M-1, 3]) == vector(ZZ, [1, 0])

P = PolynomialRing(QQ, 'x')
K = NumberField(P.gen()**2-2, 'alpha')
alpha = K.gen()
small_beta = [K(1), K(1), K(2), 1+alpha, alpha-1, K(-1)]
compact_c = [-M, -1, 0, 0, 0, 0]
assert (1+alpha)*(alpha-1) == 1
assert alpha**2 == 2 and (K(-1))**2 == 1
# beta_4 and beta_5 are tied powers 0,1; neither cancels.
assert small_beta[3] != 0 and small_beta[4] != 0

# Evaluate original degree-6 multiplication matrices in the FULL finite ring.
# Reducibility is harmless; every inverted input is checked to be a unit.
p = next_prime(ZZ(2)**160)
F = GF(p)
R = PolynomialRing(F, 'y')
t = F(7)
ring = R.quotient(R.gen()**6 - F(2)*t**int(v), 'ybar')
ybar = ring.gen()
q = ybar**3 / t**int(3*M+1)
units = [ybar, ring(t), ring(2), 1+q, q-1, ring(-1)]
q_derivative_coefficient = 3*v - 6*(3*M+1)
assert q_derivative_coefficient == 0
scaled_derivatives = [F(v)*ybar, ring(6)*t, ring(0),
                      F(q_derivative_coefficient)*q,
                      F(q_derivative_coefficient)*q, ring(0)]
vectors = [list((du/u).lift()) for du,u in zip(scaled_derivatives, units)]
vectors = [row+[F(0)]*(6-len(row)) for row in vectors]
E = Matrix(F, vectors).transpose()
assert E.row(0) == vector(F, [v, 6, 0, 0, 0, 0])
assert all(a == 0 for row in E.rows()[1:] for a in row)

residue = ZZ(-F(v)/F(6))
lattice_basis = Matrix(ZZ, [[1,residue,0,0,0,0], [0,p,0,0,0,0],
                          [0,0,1,0,0,0], [0,0,0,1,0,0],
                          [0,0,0,0,1,0], [0,0,0,0,0,1]])
assert all(E*vector(F, row) == 0 for row in lattice_basis.rows())
reduced = lattice_basis.LLL(delta=QQ(3)/4)
B_control = 3*M+1  # Independently known true Alg-basis bound for this one case.
cutoff = ZZ(2)**(k-1)*k*B_control
radius = 2*cutoff
assert p > k*radius*max(v, ZZ(6))
short_rows = [row for row in reduced.rows() if row.dot_product(row) <= cutoff**2]
assert len(short_rows) == 5
assert all(row.dot_product(row) > radius**2 for row in reduced.rows()[5:])
alg_expected = Matrix(ZZ, [[3,-3*M-1,0,0,0,0], [0,0,1,0,0,0],
                          [0,0,0,1,0,0], [0,0,0,0,1,0], [0,0,0,0,0,1]])
alg_actual = Matrix(ZZ, short_rows)
assert alg_actual.row_module() == alg_expected.row_module()

# Exact small-field relation certificate, rather than claiming to run LS:
# alpha has nonzero valuation at the prime over2; epsilon=alpha+1>1 is a
# non-torsion unit, alpha-1=epsilon^-1, and -1 has exact order2.
# Free-Z degree, alpha valuation, epsilon power, and parity are all retained.
equations = Matrix(ZZ, [[3*M+1,3,0,0,0,0,0],
                        [-M,-1,2,0,0,0,0],
                        [0,0,0,1,-1,0,0],
                        [0,0,0,0,0,1,-2]])
extended_kernel = equations.right_kernel().basis_matrix()
actual_rel = Matrix(ZZ, [list(row[:6]) for row in extended_kernel.rows()])
expected_rel = Matrix(ZZ, [[6,-v,-1,0,0,0], [0,0,0,1,1,0], [0,0,0,0,0,2]])
assert actual_rel.row_module() == expected_rel.row_module()
unit_sign = vector(ZZ, [0,0,0,0,0,1])
assert unit_sign not in actual_rel.row_module()
assert 2*unit_sign in actual_rel.row_module()
assert unit_sign in actual_rel.row_space().change_ring(QQ)
lc_false = vector(ZZ, [1,-M,0,0,0,0])
assert sum(c*e for c,e in zip(compact_c,lc_false)) == 0
assert vector(ZZ, [3*M+1,3,0,0,0,0]).dot_product(lc_false) == 1
assert vector(ZZ, [0,0,1,0,0,0]) in alg_actual.row_module()
assert vector(ZZ, [0,0,1,0,0,0]) not in actual_rel.row_module()
assert v % 257 == 0 and 6 % 257 != 0

out = {
    'scope': 'One exact native Kummer case; no general LS or theorem-sized execution',
    'M': int(M), 'M_bits': int(M.nbits()), 'delta': delta, 'constant_degree': g,
    'v': int(v), 'coordinate_matrix': [[int(a) for a in row] for row in C.rows()],
    'compact_alpha_powers': [int(a) for a in compact_c],
    'small_beta': [str(a) for a in small_beta],
    'good_prime': int(p), 'good_prime_bits': int(p.nbits()),
    'evaluated_derivative_rank': int(E.rank()), 'alg_rank': len(short_rows),
    'control_only_alg_bound': int(B_control), 'lll_cutoff': int(cutoff),
    'full_rel_basis': [[int(a) for a in row] for row in expected_rel.rows()],
    'full_rel_rank': int(actual_rel.rank()), 'sign_relation_not_saturated': True,
    'lc_only_false_vector': [int(a) for a in lc_false],
    'derivative_only_constant2_false_positive': True,
    'small_characteristic_false_Y': 257,
    'expanded_large_powers': False, 'general_LS_executed': False,
    'quantum_executed': False, 'asymptotic_claim_from_control': False,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({name:out[name] for name in ['M_bits','delta','constant_degree','alg_rank',
                 'full_rel_rank','sign_relation_not_saturated','expanded_large_powers']}))

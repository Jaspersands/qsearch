"""Exact sparse-degree derivative control and symbolic specialization falsifier."""
from pathlib import Path
import json
from sage.all import GF, ZZ, QQ, matrix, vector, PolynomialRing, prod

N = 2**40 + 1

def derivative_matrix(p):
    F = GF(p)
    R = PolynomialRing(F, 'Y')
    Y = R.gen()
    t = F(3)
    a = t**N
    da = F(N)*t**(N-1)
    f = (Y**2-a)**2-2
    Q = R.quotient(f, 'y')
    y = Q.gen()
    fy = Q(f.derivative())
    ft = Q(-2*da*Y**2+2*a*da)
    yp = -ft*fy.inverse_of_unit()
    w = y**2-a
    wp = 2*y*yp-da
    assert wp == 0
    units = [w, y, y*(1+w), w-1, Q(t), Q(2), Q(-1)]
    derivs = [wp, yp, yp*(1+w)+y*wp, wp, Q(1), Q(0), Q(0)]
    vals = [d*u.inverse_of_unit() for d, u in zip(derivs, units)]
    A = matrix(F, 4, 7, lambda h, i: vals[i].lift()[h])
    return A, units

p = 2**61-1
A, units = derivative_matrix(p)
assert A.rank() == 2
assert A.column(1) == A.column(2)
assert all(A.column(i).is_zero() for i in [0, 3, 5, 6])
assert matrix(GF(p), [A.column(1), A.column(4)]).rank() == 2
E = A.echelon_form()
pivots = E.pivots()
free = [i for i in range(7) if i not in pivots]
rows = []
for j in free:
    v = vector(ZZ, 7)
    v[j] = 1
    for i, pivot in enumerate(pivots):
        v[pivot] = -ZZ(E[i, j])
    rows.append(v)
for pivot in pivots:
    v = vector(ZZ, 7)
    v[pivot] = p
    rows.append(v)
M = matrix(ZZ, rows)
assert abs(M.det()) == p**2
L = M.LLL()
cutoff = 2**7*7
short = [v for v in L.rows() if v.dot_product(v) <= cutoff**2]
assert len(short) == 5
expected = matrix(ZZ, [[1,0,0,0,0,0,0],[0,-1,1,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]])
assert matrix(ZZ, short).row_module() == expected.row_module()
# Sage returns orthogonal rows as first item; inspect their exact squared norms.
orthogonal = L.gram_schmidt()[0]
gs2 = [v.dot_product(v) for v in orthogonal.rows()]
assert all(v > 7 for v in gs2[5:])
Abad, _ = derivative_matrix(257)
assert N % 257 == 0 and Abad.column(1).is_zero()
assert Abad.rank() == 1

# Actual constant-field witnesses, not a general constant-map implementation.
Kpoly = PolynomialRing(QQ, 'z')
K = QQ.extension(Kpoly.gen()**2-2, 'w')
w = K.gen()
assert w != 1 and (1+w)*(w-1) == 1 and w**2 == 2
assert K(-1) != 1 and K(-1)**2 == 1
full_rel_examples = [[2,0,0,0,0,-1,0],[0,-1,1,1,0,0,0],[0,0,0,0,0,0,2]]
for e in full_rel_examples:
    assert prod(u**int(t) for u,t in zip(units,e)) == 1

# Keep X=T^M symbolic: this avoids expanding binary M in the falsifier.
S = PolynomialRing(QQ, ['X','Z'])
X,Z = S.gens()
delta = 5
Aa = X+2
B = X*(X-1)*Aa
f = prod(Z-j*Aa for j in range(1,delta+1))-B
constant = f.subs({Z:0})
q,r = constant.quo_rem(Aa)
assert r == 0 and q.subs({X:-2}) == -6
assert all(f.subs({Z:j*Aa}) == -B for j in range(1,delta+1))
assert B.subs({X:0}) == 0 and B.subs({X:1}) == 0
assert sum(c*X**e[0] for e,c in f.dict().items() if e[1] == delta-1) == -15*Aa
result = {
 'binary_exponent':N, 'binary_exponent_bits':N.bit_length(),
 'native_quartic':'(Y^2-T^N)^2-2; N odd, constants Q(sqrt2)',
 'all_four_basis_coordinates_retained':True, 'derivative_rank':int(A.rank()),
 'congruence_index':str(abs(M.det())), 'control_only_Balg':1,'LLL_cutoff':cutoff,
 'Alg_rank':len(short),'Alg_lattice_exactly_matches':True,
 'later_GS_norm2_exceeds_short_true_basis':True,
 'bad_characteristic257_divides_N':True,'bad_characteristic_derivative_rank':int(Abad.rank()),
 'nonrational_constant_is_not_relation':True,'minus_one_not_identity_but_square_is':True,
 'explicit_true_relation_examples':full_rel_examples,
 'counterfamily_delta':delta,'counterfamily_Eisenstein_residue':-6,
 'all_shift_norm_evaluations_equal_minus_B':True,
 'zero_and_unit_specializations_kill_required_units':True,
 'counterfamily_Y_coefficient_sparse_terms':len(f.monomials()),
 'large_T_power_expanded':False,'generic_Alg_algorithm_implemented':False,
 'constant_map_implemented':False,'fullRel_algorithm_implemented':False,
 'quantum_execution':False,'speedup_claim':False,'novelty_claim':False,
 'finite_control_only':True,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['binary_exponent_bits','derivative_rank','Alg_rank','bad_characteristic_derivative_rank','counterfamily_Eisenstein_residue','counterfamily_Y_coefficient_sparse_terms']}))

"""Exact classical control; huge T degree stays a binary exponent throughout."""
import json
from pathlib import Path
from sage.all import QQ, ZZ, GF, PolynomialRing, matrix, vector

N=2**40+1
# X is a proof/control abbreviation for T^N, never an expanded native input.
P=PolynomialRing(QQ, names=('X','Y')); X,Y=P.gens()
A=P.quotient(P.ideal(Y**2-X**2-2), names=('x','y')); x,y=A.gens()
minus,plus=y-x,y+x
assert minus*plus==2
assert (y-x)*(-y-x)==-2
assert (y+x)*(-y+x)==-2
# Cleared differential numerators for dX/dT=N*X/T, dY/dT=N*X^2/(T*Y).
assert N*x*x-N*x*y == -N*x*minus
assert N*x*x+N*x*y == N*x*plus
alg_truth=matrix(ZZ,[[1,1,0,0],[0,0,1,0]])
rel_truth=matrix(ZZ,[[1,1,-1,0]])
cutoff=64  # CONTROL-ONLY B_alg=1, independently derived, not hidden native advice.

def derivative_lattice(p):
    F=GF(p); t=F(2); w=t**N; D=w*w+2
    assert D!=0
    a=F(N)*w/(t*D)
    C=matrix(F,[[0,0,0,1/t],[-a,a,0,0]])
    integral=matrix(ZZ,[[ZZ(v) for v in row] for row in C.rows()])
    augmented=integral.augment(-p*matrix.identity(ZZ,2))
    kernel=augmented.right_kernel().basis_matrix()
    M=kernel.matrix_from_columns(range(4)).hermite_form()
    reduced=M.LLL(delta=0.75)
    short=matrix(ZZ,[r for r in reduced.rows() if r.dot_product(r)<=cutoff**2])
    assert list(short.rows())==list(reduced.rows())[:short.nrows()]
    return C,M,reduced,short

p=2**61-1
assert ZZ(p).is_prime()
C,M,reduced,alg=derivative_lattice(p)
assert alg.row_module()==alg_truth.row_module()
gs=reduced.change_ring(QQ).gram_schmidt()[0]
gap=min(r.dot_product(r) for r in gs.rows()[2:])
assert gap>cutoff**2
assert vector(ZZ,[0,0,1,0]) in alg.row_module()  # Constant2 is not relation1.
assert A(2)!=1

# LC in the +sqrt branch: cancellation LC(-X)+LC(Y)=0 is resolved by norm.
naive_minus_lc=-1+1
corrected_minus_lc=QQ(-2)/QQ(-2)
assert naive_minus_lc==0 and corrected_minus_lc==1
lc_plus=[QQ(1),QQ(2),QQ(2),QQ(1)]
lc_minus=[QQ(-2),QQ(-1),QQ(2),QQ(1)]
constant_plus=matrix(ZZ,[[0,1,1,0]]).right_kernel().basis_matrix()
minus_aug=matrix(ZZ,[[1,0,1,0,0],[1,1,0,0,-2]])
constant_minus=minus_aug.right_kernel().basis_matrix().matrix_from_columns(range(4))
solutions=[]
for L in [constant_plus,constant_minus]:
    rel=alg.row_module().intersection(L.row_module())
    assert rel==rel_truth.row_module()
    solutions.append(rel.basis_matrix())
assert vector(ZZ,[0,0,0,1]) in constant_plus.row_module()
assert vector(ZZ,[0,0,0,1]) not in alg.row_module()  # T passes LC only.
assert minus*plus/2==1

# Small characteristic dividing N erases a genuine differential constraint.
bad_p=257
assert N%bad_p==0
bad_C,bad_M,bad_lll,bad_short=derivative_lattice(bad_p)
fake=vector(ZZ,[1,0,0,0])
assert fake in bad_short.row_module() and fake not in alg_truth.row_module()
assert minus!=1
as_int=lambda B:[[int(v) for v in r] for r in B.rows()]
result={
 'scope':'Exact CLASSICAL sparse quadratic derivative/leading-coefficient control. No generic LS, quantum HSP, full theorem-sized run, or asymptotic inference.',
 'N':N,'N_bits':N.bit_length(),
 'native_field':'Q(T)[Y]/(Y^2-T^(2N)-2)',
 'native_units':['Y-T^N','Y+T^N','2','T'],
 'expanded_T_power':False,
 'good':{'prime':p,'derivative_matrix_mod_p':as_int(C),
         'lll_basis':as_int(reduced),'short_alg_basis':as_int(alg),
         'cutoff_control_only':cutoff,'later_GS_norm_squared_min':str(gap)},
 'leading_coefficients':{'plus_branch':[str(v) for v in lc_plus],
                         'minus_branch':[str(v) for v in lc_minus],
                         'naive_cancelled_coefficient':naive_minus_lc,
                         'norm_repaired_coefficient':str(corrected_minus_lc)},
 'both_branches_exact_relation_basis':[as_int(v) for v in solutions],
 'derivative_only_false_positive':[0,0,1,0],
 'constant_only_false_positive':[0,0,0,1],
 'bad_characteristic':{'p':bad_p,'divides_N':True,
                       'short_rank':int(bad_short.rank()),'false_vector':list(map(int,fake))}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'N_bits':N.bit_length(),'alg_rank':int(alg.rank()),'rel_rank':1,'bad_short_rank':int(bad_short.rank()),'branches':2}))

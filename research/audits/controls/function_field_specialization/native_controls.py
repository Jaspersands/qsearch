"""Exact classical controls for specialization, LLL and nonreduced labels."""
import json
from pathlib import Path
from sage.all import GF, ZZ, PolynomialRing, matrix, vector, prod

Fp=GF(5)
P=PolynomialRing(Fp,'T'); T=P.gen(); F=P.fraction_field()
units=[F(T),F(2*T**2),F(2)]
valuation=[int(u.numerator().valuation(T)-u.denominator().valuation(T)) for u in units]
constants=[Fp(u/F(T)**v) for u,v in zip(units,valuation)]
constant_logs=[int(c.log(Fp(2))) for c in constants]
assert valuation==[1,2,0] and constant_logs==[0,1,1]
truth=matrix(ZZ,[[-2,1,-1],[0,0,4]])
for e in truth.rows(): assert prod(u**int(n) for u,n in zip(units,e))==1
assert vector(ZZ,[0,0,1]) not in truth.row_module()
assert vector(ZZ,[0,0,4]) in truth.row_module() and units[2]!=1
K=GF(5**5,name='a'); a=K.multiplicative_generator()
N=int(a.multiplicative_order()); assert N==3124
cutoff=96  # Tight B=4 is PROVED FOR THIS CONTROL, not supplied to native algorithm.

def finite_lattice(point):
    values=[point, K(2)*point**2, K(2)]
    logs=[int(v.log(a)) for v in values]  # Classical small-field DLogs, NOT HSP.
    ker=matrix(ZZ,[logs+[-N]]).right_kernel().basis_matrix()
    M=ker.matrix_from_columns([0,1,2]).hermite_form()
    reduced=M.LLL(delta=0.75)
    small=[row for row in reduced.rows() if row.dot_product(row)<=cutoff**2]
    assert reduced.rows()[:len(small)]==small
    return logs,M,reduced,matrix(ZZ,small)

logs,M,reduced,small=finite_lattice(a)
assert small.nrows()==2 and small.row_module()==truth.row_module()
assert 781**2 > 5*cutoff**2 and N//4==781
bad_logs,bad_M,bad_reduced,bad_small=finite_lattice(K(1))
assert bad_small.rank()==3
fake=vector(ZZ,[1,0,0])
assert fake in bad_M.row_module() and prod(u**int(n) for u,n in zip(units,fake))!=1
# Inseparable generic Y^3-T specializes at T=1 to a NONREDUCED ring.
P3=PolynomialRing(GF(3),'Y'); Y=P3.gen()
B=P3.quotient(Y**3-1,names='z'); z=B.gen()
assert z!=1 and z**2!=1 and z**3==1
assert z-1!=0 and (z-1)**3==0
period=int(3**3*prod(3**j-1 for j in range(1,4)))
assert period==11232 and period%3==0 and z**period==1
as_int=lambda A:[[int(x) for x in row] for row in A.rows()]
result={'scope':'Exact classical source-first factor/constant-log, finite DLog and LLL controls. No quantum HSP or full theorem-sized algorithm run.',
 'native_units':['T','2*T^2','2'], 'classical_valuation_row':valuation,
 'classical_constant_log_row_mod4':constant_logs,'true_relation_basis':as_int(truth),
 'good':{'field_cardinality':3125,'finite_logs':logs,'finite_basis':as_int(M),
         'lll_basis':as_int(reduced),'cutoff_control_only':cutoff,'short_prefix':as_int(small),
         'fake_gap_squared_lower_bound':'781^2/5','exact_nonsaturated_lattice_recovered':True},
 'legal_bad_point':{'T':'1','finite_logs':bad_logs,'lll_basis':as_int(bad_reduced),
                   'short_rank':int(bad_small.rank()),'false_relation':[1,0,0]},
 'nilpotent_guard':{'ring':'F3[Y]/(Y^3-1)','Y_order':3,'Y_minus_1_nonzero_nilpotent':True,
                   'root_projection_would_give_order':1,'known_GL_period':period}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,separators=(',',':')))

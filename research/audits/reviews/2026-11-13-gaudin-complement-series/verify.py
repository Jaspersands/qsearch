from sage.all import QQ, PolynomialRing, matrix, diagonal_matrix, identity_matrix
from itertools import combinations
from pathlib import Path
import json
R=PolynomialRing(QQ,names=('a','b','c','d')); F=R.fraction_field()
a,b,c,d=map(F,R.gens()); eps=(a,b,c,d)
states=list(combinations(range(4),2)); dim=len(states)
energy=[sum(eps[j] for j in S) for S in states]
E=diagonal_matrix(F,energy)
tau=matrix(F,dim,dim,lambda i,j: QQ(1)/2 if len(set(states[i])&set(states[j]))==1 else 0)
def comm(A,B):return A*B-B*A
K0=matrix(F,dim,dim)
for i in range(dim):
 for j in range(dim):
  if i!=j and tau[i,j]!=0:K0[i,j]=tau[i,j]/(energy[j]-energy[i])
assert K0.transpose()==-K0 and comm(E,K0)==-tau
B0=comm(tau,K0)
K1=matrix(F,dim,dim)
for i in range(dim):
 for j in range(dim):
  if i!=j:K1[i,j]=B0[i,j]/(energy[j]-energy[i])
assert K1.transpose()==-K1
complements=[states.index(tuple(j for j in range(4) if j not in S)) for S in states]
assert all(K0[complements[j],j]==0 and K1[complements[j],j]==0 for j in range(dim))
assert comm(E,comm(E,K1))+comm(E,comm(tau,K0))+comm(tau,comm(E,K0))==0
v=states.index((0,1)); w=states.index((2,3))
Delta=energy[w]-energy[v]
Pi=(a-c)*(a-d)*(b-c)*(b-d)
source2=comm(E,comm(tau,K1))+comm(tau,comm(E,K1))+comm(tau,comm(tau,K0))
K2wv=-source2[w,v]/Delta**2
expected=-(QQ(3)/4)*Delta/Pi
assert K2wv==expected
middle=[j for j in range(dim) if j not in (v,w)]
reported=(QQ(1)/2)*sum((energy[w]+energy[u]-2*energy[v])*K1[u,v]+(energy[u]+energy[v]-2*energy[w])*K1[w,u]+K0[u,v]+K0[w,u] for u in middle)
assert reported==source2[w,v]
assert (tau*K0*tau)[w,v]==0
assert source2[w,v]==(QQ(3)/4)*Delta**3/Pi
p=a-c; q=a-d; r=b-c; s=b-d; kappa=c-d; lam=a-b
assert kappa**2+lam**2+2*p*s+2*q*r==Delta**2
C=matrix(F,dim,dim,lambda i,j:1 if i==complements[j] else 0)
assert C*E*C==sum(eps)*identity_matrix(F,dim)-E
assert C*tau*C==tau
assert C*K0*C==-K0 and C*K1*C==K1
result={
 'scope':'One symbolic four-site complement entry; rational functions, no numerical instances or parameter sweep',
 'variables':['a','b','c','d'],
 'states':[[j+1 for j in S] for S in states],
 'tau':'one half the adjacency of J(4,2)',
 'entry':{'bra':[3,4],'ket':[1,2]},
 'Delta':'c+d-a-b','Pi':'(a-c)(a-d)(b-c)(b-d)',
 'K0_and_K1_complement_entries_zero':True,
 'first_order_double_commutator_recursion_verified':True,
 'reported_second_order_recursion_matches_full_expansion':True,
 'tau_K0_tau_complement_entry_zero':True,
 'second_order_source_factorization':str(source2[w,v].factor()),
 'K2_complement_entry_factorization':str(K2wv.factor()),
 'target_formula_exact':True,
 'reported_auxiliary_polynomial_identity_exact':True,
 'complement_symmetry_of_E_tau_K0_K1_verified':True
}
Path('research/audits/reviews/2026-11-13-gaudin-complement-series/result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

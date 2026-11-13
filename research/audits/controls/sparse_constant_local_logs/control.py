from sage.all import *
import json
from pathlib import Path
R=PolynomialRing(QQ,'t'); t=R.gen(); F=R.fraction_field(); S=PolynomialRing(F,'y'); y=S.gen()
M=3
E=F.extension(y**2-2*t**(2*M+1),'z'); z=E.gen()
u=[z,E(t),E(2),z/E(t**M)]
A=matrix(ZZ,[[2*M+1,2,0,1]])
C=matrix(ZZ,[[2*M+1,2,0,1],[1,0,2,1]])
L=C.right_kernel().basis_matrix()
for row in L:
    assert prod(a**int(e) for a,e in zip(u,row))==1
K=QuadraticField(2,'a'); a=K.gen(); lc=[a,K(1),K(2),a]
for row in L:
    assert prod(x**int(e) for x,e in zip(lc,row))==1
assert A.right_kernel().rank()==3 and L.nrows()==2
assert A*vector(ZZ,[0,0,1,0])==0 and C*vector(ZZ,[0,0,1,0])!=0
rows=[]
for p in [3,1093,3511]:
    assert is_prime(p)
    r2=int(power_mod(2,p-1,p**2)); r3=int(power_mod(2,p-1,p**3))
    if p>3: assert r2==1 and r3!=1
    rows.append({'prime':p,'two_power_p_minus_one_mod_p2':r2,'mod_p3':r3,'mod_p2_false_torsion':r2==1})
out={'scope':'EXACT_FINITE_CONTROL_ONLY; no asymptotic precision lower bound or classical hardness', 'M':M,'alg_rank':3,'rel_rank':2,'rel_basis':[list(map(int,row)) for row in L], 'residue_degree':1,'compatible_Puiseux_LC_field_degree':2,'non_torsion_constant':2,'prime_controls':rows,'claim_gates':{'full_classical_Rel_closed':False,'polynomial_precision_refuted':False,'quantum_speedup':False,'no_go_for_all_local_logs':False}}
Path(__file__).with_name('result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,separators=(',',':')))

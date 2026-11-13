
from sage.all import *
from itertools import combinations
from pathlib import Path
import json
sets=list(combinations(range(4),2))
def inertia(B):
    B=matrix(AA,B);ans=[0,0,0]
    while B.nrows():
        n=B.nrows();inds=[i for i in range(n) if B[i,i]!=0]
        if not inds:
            off=next(((i,j) for i in range(n) for j in range(i+1,n) if B[i,j]!=0),None)
            if off is None:ans[2]+=n;break
            i,j=off;P=identity_matrix(AA,n);P[j,i]=1;B=P.transpose()*B*P;inds=[i]
        i=inds[0];order=[i]+[j for j in range(n) if j!=i];B=B.matrix_from_rows_and_columns(order,order);p=B[0,0];ans[0 if p>0 else 1]+=1
        B=B[1:,1:]-B[1:,:1]*B[:1,1:]/p
    return ans
rows=[]
for eps,g in [([-3,-1,1,3],QQ(1)/4),([-20,-1,1,20],QQ(1)),([-3,-1,2,17],QQ(1))]:
    H=matrix(QQ,6,6,lambda i,j: sum(eps[k] for k in sets[i]) if i==j else (-g if len(set(sets[i])&set(sets[j]))==1 else 0))
    E=min(H.charpoly().roots(AA,multiplicities=False))
    v=(H.change_ring(AA)-E).right_kernel().basis()[0]
    if v[0]<0:v=-v
    assert all(t>0 for t in v) and H*v==E*v
    A=matrix(AA,4);B=matrix(AA,4)
    for (i,j),x in zip(sets,v):A[i,j]=A[j,i]=x;B[i,j]=B[j,i]=x*x
    row={'eps':eps,'g':str(g),'ground_energy_approx':float(E),'amplitude_inertia':inertia(A),'born_inertia':inertia(B)}
    rows.append(row);print(row,flush=True)
    if row['born_inertia'][0]>1:break
V=matrix(QQ,[[1,0],[1,1],[0,1],[-1,1]])
A=matrix(QQ,4);B=matrix(QQ,4)
for i,j in combinations(range(4),2):A[i,j]=A[j,i]=V.matrix_from_rows([i,j]).det()**2;B[i,j]=B[j,i]=A[i,j]**2
assert inertia(A)==[1,2,1] and inertia(B)==[2,2,0]
result={'native_cases':rows,'generic_dpp_weights':[str(A[i,j]) for i,j in sets],'generic_amplitude_inertia':inertia(A),'generic_square_inertia':inertia(B),'scope':'Exact finite falsifiers only; no all-input gap/closure inference.'}
p=Path('research/audits/controls/bcs_born_stability');p.mkdir(exist_ok=True);(p/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print('DONE',flush=True)

from sage.all import QQ, CyclotomicField, matrix, identity_matrix, prod
from pathlib import Path
import json
from copy import copy
F=CyclotomicField(4); ii=F.gen()
checks={'principal_pfaffians':0,'covariance_entries':0,'prefix_probabilities':0}
for ell in range(2,6):
 L=ell+1
 for z in [QQ(1)/2,QQ(2)]:
  J=matrix(F,L,L,lambda a,b: 1 if a<b else -1 if a>b else 0)
  U=identity_matrix(F,L)
  for j in range(ell-1):
   R=identity_matrix(F,L);R[j,j]=QQ(3)/5;R[j+1,j+1]=QQ(3)/5;R[j,j+1]=-QQ(4)/5;R[j+1,j]=QQ(4)/5
   U=R*U
  D=identity_matrix(F,L);D[0,0]=ii;U=D*U
  Z=U*(z*J)*U.transpose()
  v={}
  for bits in range(1<<L):
   S=[j for j in range(L) if bits>>j&1]
   if len(S)%2: v[bits]=F(0)
   else:
    assert J.matrix_from_rows_and_columns(S,S).pfaffian()==1
    checks['principal_pfaffians']+=1
    v[bits]=Z.matrix_from_rows_and_columns(S,S).pfaffian()
  norm=sum(a.conjugate()*a for a in v.values())
  I=identity_matrix(F,L);A=(I-Z).augment(-ii*(I+Z))/2
  M=-ii*(identity_matrix(F,2*L)-2*A.conjugate_transpose()*(A*A.conjugate_transpose()).inverse()*A)
  order=[q for j in range(L) for q in (j,L+j)]
  M=M.matrix_from_rows_and_columns(order,order)
  def act(w,a):
   j=a//2;out={s:F(0) for s in range(1<<L)}
   for bits,value in w.items():
    sign=(-1)**((bits&((1<<j)-1)).bit_count())
    factor=1 if a%2==0 else ii if bits>>j&1 else -ii
    out[bits^(1<<j)]+=sign*factor*value
   return out
  for a in range(2*L):
   for b in range(a+1,2*L):
    w=act(act(v,b),a)
    observed=ii*sum(v[s].conjugate()*w[s] for s in v)/norm
    assert observed==M[a,b],(ell,z,a,b,observed,M[a,b])
    checks['covariance_entries']+=1
  for k in range(L+1):
   for pat in range(1<<k):
    signs=[1 if not(pat>>j&1) else -1 for j in range(k)]
    C=copy(M[:2*k,:2*k])
    for j,s in enumerate(signs):C[2*j,2*j+1]+=s;C[2*j+1,2*j]-=s
    predicted=F(prod(signs))*C.pfaffian()/2**k
    actual=sum(v[s].conjugate()*v[s] for s in v if s&((1<<k)-1)==pat)/norm
    assert predicted==actual,(ell,z,k,pat,predicted,actual)
    checks['prefix_probabilities']+=1
result={'status':'passed','checks':checks,'scope':'Exact Q(i) finite convention controls only, no all-size theorem or runtime claim.'}
Path('research/audits/controls/folded_product/result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

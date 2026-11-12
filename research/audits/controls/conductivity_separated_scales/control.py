from sage.all import QQ, matrix, vector
from pathlib import Path
import json
L=8; N=L*L
D=matrix(QQ,2*N,N)
idx=lambda x,y:(x%L)*L+y%L
for x in range(L):
 for y in range(L):
  q=idx(x,y)
  for j in range(2):
   D[2*q+j,q]=-1
   D[2*q+j,idx(x+(j==0),y+(j==1))]+=1
K=D.transpose()*D
Inv=(K+matrix(QQ,N,N,lambda i,j:QQ(1)/N)).inverse()
proj=lambda v:D*(Inv*(D.transpose()*v))
sig=[]; av=[]; bv=[]; hv=[]
for x in range(L):
 for y in range(L):
  h=int(x<L//2); s=h*(-1)**x+(1-h)*(-1)**y
  for j in range(2):
   sig.append(s); av.append(QQ(h*(-1)**x if j==0 else 0)/L)
   bv.append(QQ((1-h)*(-1)**y if j==0 else 0)/L)
   hv.append(QQ(h if j==0 else 0)/L)
vA=vector(QQ,av);vB=vector(QQ,bv);hh=vector(QQ,hv)
S=lambda v:vector(QQ,[a*b for a,b in zip(sig,v)])
e=proj(vB); u=proj(hh); w=proj(S(proj(vA+vB)))
assert proj(vA)==vA
assert vA.dot_product(vA)==QQ(1)/2
assert e.dot_product(e)<=QQ(1)/(2*L)
assert S(vA)==hh
assert u.dot_product(u)==QQ(1)/4
assert (w-u).dot_product(w-u)<=e.dot_product(e)
result=dict(L=L,projection_vA_exact=True,norm_vA_squared=str(vA.dot_product(vA)),norm_error_squared=str(e.dot_product(e)),error_squared_bound=str(QQ(1)/(2*L)),norm_u_squared=str(u.dot_product(u)),T2=str(w.dot_product(w)),scope='One exact transcription control; asymptotics require the proof, not this finite example.')
Path(__file__).with_name('result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))

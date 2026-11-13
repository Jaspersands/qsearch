from sage.all import *
import json
from pathlib import Path
F=QuadraticField(-1,'I'); I=F.gen()
def gate(N,j,d):
 D=2**N; A=matrix(F,D,D)
 for x in range(D):
  y=x
  if ((x>>j)&1)!=((x>>(j+1))&1): y=x^(1<<j)^(1<<(j+1))
  A[x,x]+=1/(1+I*d); A[y,x]+=I*d/(1+I*d)
 assert A.conjugate_transpose()*A==identity_matrix(F,D)
 return A
def word(vel):
 vel=list(vel); N=len(vel); W=[]
 for k in range(N-1,0,-1):
  for j in range(k):
   assert vel[j]>vel[j+1]
   W.append((j,vel[j]-vel[j+1])); vel[j],vel[j+1]=vel[j+1],vel[j]
 return W
def calc(N):
 W=word(range(N-1,-1,-1)); U=identity_matrix(F,2**N); C=identity_matrix(QQ,2**N)
 for j,d in W:
  A=gate(N,j,d); U=A*U
  B=matrix(QQ,2**N,2**N,lambda x,y: QQ(A[x,y]*A[x,y].conjugate()))
  C=B*C
 return W,U,C
r={}
W,U,C=calc(3); x=2
p=[QQ(z*z.conjugate()) for z in U.column(x)]; c=list(C.column(x))
tv=sum(abs(a-b) for a,b in zip(p,c))/2
assert tv==QQ(1)/10
r['three_spin']={'input_bit_positions':[1],'word':[(int(j),int(d)) for j,d in W], 'quantum':{str(i):str(p[i]) for i in range(8) if p[i]},'local_coin':{str(i):str(c[i]) for i in range(8) if c[i]},'tv':str(tv)}
A=gate(3,0,1); B=gate(3,1,2); Cg=gate(3,0,1)
assert A*B*Cg==gate(3,1,1)*gate(3,0,2)*gate(3,1,1)
assert A*gate(3,1,1)*A!=gate(3,1,1)*A*gate(3,1,1)
W,U,C=calc(4); single=[1<<j for j in range(4)]; T=U.matrix_from_rows_and_columns(single,single)
assert T.conjugate_transpose()*T==identity_matrix(F,4)
pairs=list(Subsets(range(4),2)); input_pair=[0,2]; x=sum(1<<j for j in input_pair)
qp={}; dp={}
for S in pairs:
 y=sum(1<<j for j in S); a=U[y,x]; b=T.matrix_from_rows_and_columns(list(S),input_pair).det()
 qp[str(list(S))]=QQ(a*a.conjugate());dp[str(list(S))]=QQ(b*b.conjugate())
assert sum(qp.values())==sum(dp.values())==1
r['four_spin']={'input_bit_positions':input_pair,'word':[(int(j),int(d)) for j,d in W], 'quantum':{k:str(v) for k,v in qp.items()},'single_particle_dpp':{k:str(v) for k,v in dp.items()},'dpp_tv':str(sum(abs(qp[k]-dp[k]) for k in qp)/2)}
a=QQ(12)/125; b=QQ(117)/500; c=QQ(9)/100
assert a*a==qp['[0, 1]']*qp['[2, 3]'] and b*b==qp['[0, 2]']*qp['[1, 3]'] and c*c==qp['[0, 3]']*qp['[1, 2]']
assert b>a+c
r['four_spin']['plucker_triangle']={'a':str(a),'b':str(b),'c':str(c),'violation':str(b-a-c),'scope':'No pure two-particle Slater Born law for ANY orbital matrix, by the Plucker triangle necessity.'}
r['scope']='Exact native finite controls. Local-coin and particular single-particle-DPP tests only; no general classical lower bound or quantum advantage.'
Path(__file__).with_name('result.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))

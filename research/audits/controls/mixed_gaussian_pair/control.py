"""Exact classical CAS consistency controls, not the full learner.
Run /opt/anaconda3/envs/qsearch-cas/bin/python control.py.
"""
from sage.all import QQ, QuadraticField, matrix, identity_matrix, zero_matrix, block_matrix, prod
from itertools import combinations
from pathlib import Path
import json
K=QuadraticField(-1,'I'); ii=K.gen()
I2=identity_matrix(K,2); X=matrix(K,[[0,1],[1,0]]);Y=matrix(K,[[0,-ii],[ii,0]]);Z=matrix(K,[[1,0],[0,-1]])
def kron(ms):
 a=matrix(K,[[1]])
 for b in ms:a=a.tensor_product(b)
 return a
def majoranas(n):
 return [kron([Z]*j+[a]+[I2]*(n-j-1)) for j in range(n) for a in [X,-Y]]
def pf(A):
 if A.nrows()==0:return QQ(1)
 return A.pfaffian()
def sub(A,I):return A.matrix_from_rows_and_columns(I,I)
def density(G):
 n=G.nrows()//2;gam=majoranas(n);d=2**n;out=identity_matrix(K,d)
 for k in range(1,n+1):
  for inds in combinations(range(2*n),2*k):
   coef=pf(sub(G,list(inds)))
   if coef:
    P=identity_matrix(K,d)
    for j in inds:P=P*gam[j]
    out+=K(coef)*(-ii)**k*P
 return out/d
def pair(v):return matrix(QQ,[[0,v],[-v,0]])
def blockdiag(*As):
 sizes=[a.nrows() for a in As];M=zero_matrix(QQ,sum(sizes));pos=0
 for a in As:M[pos:pos+a.nrows(),pos:pos+a.ncols()]=a;pos+=a.nrows()
 return M
def givens(n,i,j,c=QQ(3)/5,s=QQ(4)/5):
 O=identity_matrix(QQ,n);O[i,i]=O[j,j]=c;O[i,j]=s;O[j,i]=-s;return O
p=QQ(1)/5;q=1-p
A=blockdiag(pair(QQ(1)/3),pair(-QQ(1)/2),pair(QQ(2)/5))
O=givens(6,0,2)*givens(6,1,4)
B=O*blockdiag(pair(-QQ(1)/4),pair(QQ(1)/5),pair(-QQ(1)/3))*O.transpose()
G=p*A+q*B;E=QQ(2)/5*(A-B)
rho=p*density(A)+q*density(B);gam=majoranas(3)
assert rho.trace()==1 and rho==rho.conjugate_transpose()
H={I:2*(p*pf(sub(A,list(I)))+q*pf(sub(B,list(I)))-pf(sub(G,list(I)))) for I in combinations(range(6),4)}
assert all(v==2*pf(sub(E,list(I))) for I,v in H.items())
# Sixth cumulant computed directly from raw moments using the wedge sum.
def sign_concat(I,J):return (-1)**sum(a>b for a in I for b in J)
M6=p*pf(A)+q*pf(B)
wM4=sum(sign_concat(I,tuple(j for j in range(6) if j not in I))*G[I[0],I[1]]*(p*pf(sub(A,[j for j in range(6) if j not in I]))+q*pf(sub(B,[j for j in range(6) if j not in I]))) for I in combinations(range(6),2))
J6=6*M6-6*wM4+12*pf(G)
assert J6==QQ(3)/2*6*pf(E)
assert pf(E)!=0
Adj=zero_matrix(QQ,6)
for a,b in combinations(range(6),2):
 inds=tuple(j for j in range(6) if j not in (a,b));Adj[a,b]=(-1)**(a+b+1)*H[inds]/2;Adj[b,a]=-Adj[a,b]
assert Adj==-pf(E)*E.inverse()
assert Adj.det()==pf(E)**4
recon=-abs(pf(E))*Adj.inverse();assert recon in [E,-E]
assert abs(pf(E))*Adj.inverse()!=E or pf(E)<0
# Recover physical cross entries by the stated wedge-Lefschetz map (W=I).
L=matrix(QQ,20,6);triples=list(combinations(range(6),3))
for z,(a,b,c) in enumerate(triples):L[z,c]+=recon[a,b];L[z,b]-=recon[a,c];L[z,a]+=recon[b,c]
assert L.rank()==6
# Eight-dimensional test exercises the cross-vector and final entry formulas.
E8=blockdiag(pair(QQ(1)/10),pair(QQ(1)/5),pair(QQ(3)/10),pair(QQ(2)/5))
O8=givens(8,0,6)*givens(8,3,7);E8=O8*E8*O8.transpose()
def H8(a,b,c,d):
 I=[a,b,c,d]
 if len(set(I))<4:return QQ(0)
 sg=(-1)**sum(I[j]>I[k] for j in range(4) for k in range(j+1,4))
 return 2*sg*pf(sub(E8,sorted(I)))
U8=sub(E8,list(range(6)));assert pf(U8)!=0
Ad8=zero_matrix(QQ,6)
for a,b in combinations(range(6),2):
 co=[j for j in range(6) if j not in (a,b)];Ad8[a,b]=(-1)**(a+b+1)*H8(*co)/2;Ad8[b,a]=-Ad8[a,b]
Uhat=-abs(pf(U8))*Ad8.inverse()
L8=matrix(QQ,20,6)
for z,(a,b,c) in enumerate(triples):L8[z,c]+=Uhat[a,b];L8[z,b]-=Uhat[a,c];L8[z,a]+=Uhat[b,c]
cross=zero_matrix(QQ,6,8)
for v in range(8):cross[:,v]=L8.solve_right(matrix(QQ,20,1,[H8(a,b,c,v)/2 for a,b,c in triples]))
i,j=max(combinations(range(6),2),key=lambda ij:abs(Uhat[ij]))
Ehat=matrix(QQ,8,8,lambda v,w:(H8(i,j,v,w)/2+cross[i,v]*cross[j,w]-cross[i,w]*cross[j,v])/Uhat[i,j])
assert Ehat in [E8,-E8]
# Rank-two difference is exactly a single Gaussian, not merely moment-matched.
D2=blockdiag(pair(QQ(1)/4),zero_matrix(QQ,4));Ga=G+q*D2;Gb=G-p*D2
assert p*density(Ga)+q*density(Gb)==density(G)
# Shared lowrank output channel with rational sqrt(R).
C=zero_matrix(QQ,4,2);C[0,0]=C[1,1]=QQ(4)/5
BB=zero_matrix(QQ,2);D=(identity_matrix(QQ,2)+BB*BB).inverse()
R=identity_matrix(QQ,4)-C*D*C.transpose();rootR=matrix.diagonal(QQ,[QQ(3)/5,QQ(3)/5,1,1])
assert rootR*rootR==R
A0=-C*BB*D*C.transpose();noise=block_matrix([[A0,C],[-C.transpose(),BB]])
Lm=block_matrix([[rootR],[zero_matrix(QQ,2,4)]])
CP=identity_matrix(K,6)-Lm*Lm.transpose()+ii*noise
assert CP[:4,:4]-CP[:4,4:]*CP[4:,4:].inverse()*CP[4:,:4]==zero_matrix(K,4)
Ca=blockdiag(pair(QQ(1)/3),pair(-QQ(1)/2))
Uc=givens(4,0,2);Cb=Uc*blockdiag(pair(-QQ(1)/5),pair(QQ(2)/5))*Uc.transpose()
core=p*density(Ca)+q*density(Cb)
outA=Lm*Ca*Lm.transpose()+noise;outB=Lm*Cb*Lm.transpose()+noise
expected=p*density(outA)+q*density(outB)
# In our Gamma=-i Tr(ca cb) convention, source CJ covariance is [Z,-L;L^T,0].
CJG=block_matrix([[noise,-Lm],[Lm.transpose(),zero_matrix(QQ,4)]])
cjg=density(CJG); dout=8;din=4
W=matrix.diagonal(K,[(-1)**((o.bit_count()%2)*(r.bit_count()%2)) for o in range(dout) for r in range(din)])
S=matrix.diagonal(K,[1,ii]);cz=matrix.diagonal(K,[1,1,1,-1]);V=(X.tensor_product(X))*(S.conjugate_transpose().tensor_product(S))*cz
Vfull=identity_matrix(K,dout).tensor_product(V)
cj=Vfull.conjugate_transpose()*W*cjg*W*Vfull
actual=zero_matrix(K,dout)
for a in range(din):
 for b in range(din):
  actual+=core[a,b]*cj.matrix_from_rows_and_columns([o*din+a for o in range(dout)],[o*din+b for o in range(dout)])/din
assert actual==expected/(din**2)
assert actual.trace()==QQ(1)/(din**2)
# Ordinary Bell without the required reference correction is not the channel.
wrong=zero_matrix(K,dout)
for a in range(din):
 for b in range(din):wrong+=core[a,b]*(W*cjg*W).matrix_from_rows_and_columns([o*din+a for o in range(dout)],[o*din+b for o in range(dout)])/din
assert wrong!=actual
result={'status':'PASS','scope':'Exact finite classical algebra only; no fulllearner or quantumexecution.','exterior_square_exact':True,'sixth_cumulant_t':'3/2','pfaffian':str(pf(E)),'adjugate_minus_sign':True,'lefschetz_rank':6,'eight_majorana_full_inverse':True,'rank_two_difference_exactly_gaussian':True,'schur_complement_zero':True,'CJ_input_modes':2,'CJ_output_modes':3,'CJ_success':'1/16','ordinary_CJ_output_exact':True,'missing_reference_correction_rejected':True,'full_learner_execution':False,'quantum_execution':False,'speedup_or_novelty':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','CJ_success':'1/16','pfaffian':str(pf(E))}))

"""Exact finite falsifiers, not execution of the copy learner.
Run with /opt/anaconda3/envs/qsearch-cas/bin/python.
Uses classical Fock amplitudes as a supplied-description baseline.
"""
from pathlib import Path
from itertools import combinations
import json
from sage.all import QQ, QuadraticField, matrix, vector, prod, identity_matrix
F=QuadraticField(-1,'ii'); ii=F.gen()

def state(cs,ss,alpha,beta):
    v={0:F(1)}
    for j,(c,s) in enumerate(zip(cs,ss)):
        v={z|(3<<(2*j) if b else 0):a*(s if b else c)
           for z,a in v.items() for b in (0,1)}
    v={z:beta*a for z,a in v.items()};v[0]=v.get(0,0)+alpha
    return {z:a for z,a in v.items() if a}

def norm(v):return sum(a.conjugate()*a for a in v.values())
def inner(v,w):return sum(a.conjugate()*w.get(z,0) for z,a in v.items())
def majorana(v,a):
    j,odd=divmod(a,2);o={}
    for z,amp in v.items():
        sign=(-1)**((z&((1<<j)-1)).bit_count())
        o[z^(1<<j)]=amp*sign*(ii*(-1 if z&(1<<j) else 1) if odd else 1)
    return o

def op(v,ids):
    for a in reversed(ids):v=majorana(v,a)
    return v

def cov(v,n):
    C=matrix(QQ,2*n);N=norm(v)
    for a,b in combinations(range(2*n),2):
        C[a,b]=QQ(ii*inner(v,op(v,(a,b)))/N);C[b,a]=-C[a,b]
    return C

def annihilate(v,j):
    return {z^(1<<j):amp*(-1)**((z&((1<<j)-1)).bit_count())
            for z,amp in v.items() if z&(1<<j)}

def rdm2(v,modes):
    pairs=list(combinations(modes,2));ws=[annihilate(annihilate(v,a),b) for a,b in pairs]
    return matrix(F,len(pairs),lambda i,j:inner(ws[i],ws[j])/norm(v)),pairs

def occupation(v,predicate):return QQ(sum(a.conjugate()*a for z,a in v.items() if predicate(z))/norm(v))

def rotate(v,a,b,c,s):
    w=op(v,(a,b));return {z:c*v.get(z,0)+s*w.get(z,0) for z in v.keys()|w.keys() if c*v.get(z,0)+s*w.get(z,0)}

def check_cov(cs,ss,alpha,beta):
    v=state(cs,ss,alpha,beta);n=2*len(cs);C=cov(v,n);N=norm(v)
    A2=QQ((alpha*beta).conjugate()*(alpha*beta)/(N*N))
    values=[]
    for j,c in enumerate(cs):
        pj=prod(cs[l]**2 for l in range(len(cs)) if l!=j)
        nu2=1-4*A2*(1-c*c)*(1-pj);values.append(nu2)
        block=C[4*j:4*j+4,4*j:4*j+4]
        assert -block*block==nu2*identity_matrix(QQ,4)
    for j,k in combinations(range(len(cs)),2):
        R=prod(cs[l]**2 for l in range(len(cs)) if l not in (j,k))
        assert values[j]-values[k]==4*A2*(cs[j]**2-cs[k]**2)*(1-R)
        assert C[4*j:4*j+4,4*k:4*k+4].is_zero()
    return v,C,values

cs=[QQ(3)/5]*3+[QQ(5)/13];ss=[QQ(4)/5]*3+[QQ(12)/13]
v,C,values=check_cov(cs,ss,F(-13)/3,F(1))
assert values[0]==values[1]==values[2] and values[0]!=values[3]
# This engineered native state already has its group covariance in complex normal form.
for a,b in combinations(range(12),2):
    if a//2!=b//2:assert C[a,b]==0
R,pairs=rdm2(v,range(6));Omega=vector(F,[1 if a//2==b//2 else 0 for a,b in pairs])
p=occupation(v,lambda z:bool(z&1));q=occupation(v,lambda z:bool(z&1 and z&4));z=p-q
assert z>0 and R==q*identity_matrix(F,len(pairs))+z*Omega.column()*Omega.row()
assert R.charpoly()==(R.charpoly().parent().gen()-q)**14*(R.charpoly().parent().gen()-q-3*z)
catfailure=occupation(v,lambda z:0<(z&63).bit_count()<6)
assert catfailure<=3*z
# Nontrivial hidden Gaussian rotation: recover the 12D covariance cluster projector ONLY from Crot.
vr=rotate(v,0,12,QQ(3)/5,QQ(4)/5);Cr=cov(vr,8);H=-Cr*Cr
factors=H.charpoly().factor();roots={-f[0]/f[1]:e for f,e in factors};assert sorted(roots.values())==[4,12]
lambda12=next(x for x,m in roots.items() if m==12);lambda4=next(x for x,m in roots.items() if m==4)
P=(H-lambda4*identity_matrix(QQ,16))/(lambda12-lambda4)
assert P*P==P and P.rank()==12 and P.transpose()==P
assert any(P[i,j] for i in range(12) for j in range(12,16))
# Complex phase and near-cancelling branches, without taking a numerical limit.
check_cov([QQ(3)/5,QQ(5)/13,QQ(8)/17],[QQ(4)/5,QQ(12)/13,QQ(15)/17],F(1),ii)
_,_,cancel=check_cov([QQ(99)/101]*3,[QQ(20)/101]*3,F(-1),F(1))
c=QQ(99)/101
assert cancel[0]==(c/(1+c+c*c))**2
assert cancel[0]>=c*c/9 and cancel[0]<QQ(1)/9
# At zero covariance, R2 alone has no pairing signal. The prior two-Fock quartic control pays the fallback.
cat={0:F(1),63:ii};Ccat=cov(cat,6);Rcat,_=rdm2(cat,range(6))
assert Ccat.is_zero() and Rcat==QQ(1)/2*identity_matrix(F,15)
# A coherent compression keeps GHZ phase; every proper occupation-reduced coherence vanishes.
def cnot(v,c,t):return {z^((1<<t) if z&(1<<c) else 0):amp for z,amp in v.items()}
phase=[]
for sign in (1,-1):
    a={0:F(1),63:F(sign)}
    for j in range(1,6):a=cnot(a,0,j)
    assert set(a)=={0,1}
    xmean=inner(a,{z^1:amp for z,amp in a.items()})/norm(a)
    assert xmean==sign;phase.append(str(xmean))
out={'status':'PASS','scope':'exact finite classical supplied-description controls only',
 'equal_group_pairs':3,'physical_modes':8,'R2_dimension':15,'p':str(p),'q':str(q),'z':str(z),'gap':str(3*z),
 'cat_failure':str(catfailure),'covariance_squared_cluster_multiplicities':sorted(roots.values()),
 'measured_projector_rank':P.rank(),'complex_phase_identity':True,'near_cancellation_nu_squared':str(cancel[0]),
 'zero_covariance_R2_is_scalar':True,'coherent_GHZ_memory_X':phase,
 'full_learner_executed':False,'copy_noise_simulated':False,'quantum_execution':False,'asymptotic_proof_from_control':False,'novelty':False,'classical_separation':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

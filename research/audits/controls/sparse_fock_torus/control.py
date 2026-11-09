"""Exact p11 Paley-state low-moment falsifier, not a learning benchmark."""
from pathlib import Path
from itertools import combinations
import json
from sage.all import QQ, QuadraticField, matrix, vector, binomial, WeylCharacterRing

F=QuadraticField(-1,'ii'); ii=F.gen()
n=11; w=5; lam=2
D={int(x*x % n) for x in range(1,n)}
words=[sum(1<<((x+a)%n) for x in D) for a in range(n)]
assert len(set(words))==n
A=matrix(QQ,[[int(bool(z & (1<<j))) for j in range(n)] for z in words])
assert A*A.transpose()==(w-lam)*matrix.identity(QQ,n)+lam*matrix.ones(QQ,n)
assert A.rank()==n and min((a^b).bit_count() for a,b in combinations(words,2))==6
psi={z:F(1) for z in words}
pairs=list(combinations(range(2*n),2))

def majorana(v,a):
    j,odd=divmod(a,2); out={}
    for z,amp in v.items():
        sign=(-1)**((z & ((1<<j)-1)).bit_count())
        phase=sign*(ii*(-1 if z & (1<<j) else 1) if odd else 1)
        out[z^(1<<j)]=phase*amp
    return out

def gram(v):
    norm=sum(a.conjugate()*a for a in v.values())
    images=[]; means=[]
    for a,b in pairs:
        x={z:ii*t for z,t in majorana(majorana(v,b),a).items()}
        images.append(x)
        means.append(QQ(sum(t.conjugate()*x.get(z,0) for z,t in v.items())/norm))
    G=matrix(QQ,len(pairs))
    for r,x in enumerate(images):
        for s in range(r,len(pairs)):
            y=images[s]
            raw=sum(t.conjugate()*y.get(z,0) for z,t in x.items())/norm
            G[r,s]=G[s,r]=QQ((raw+raw.conjugate())/2)-means[r]*means[s]
    return vector(QQ,means),G

mu,G=gram(psi)
J=matrix(QQ,2*n)
for j in range(n): J[2*j,2*j+1]=1;J[2*j+1,2*j]=-1
vJ=vector(QQ,[J[a,b] for a,b in pairs])
L=matrix(QQ,len(pairs))
for r,(a,b) in enumerate(pairs):
    for s,(c,d) in enumerate(pairs):
        L[r,s]=J[a,b]*J[c,d]-J[a,c]*J[b,d]+J[a,d]*J[b,c]
assert mu==-vJ/n
assert G==matrix.identity(QQ,len(pairs))-L/n-vJ.column()*vJ.row()/n**2
cp=G.charpoly(); t=cp.parent().gen()
assert cp==t*(t-QQ(12)/11)**120*(t-QQ(10)/11)**110
assert G.right_kernel().dimension()==1 and G*vJ==0

# A genuine passive rotation changes the state, but no measured mean/Gram.
rot={}
for z,amp in psi.items():
    b0,b1=bool(z&1),bool(z&2)
    if b0==b1:
        rot[z]=rot.get(z,0)+amp
    else:
        rot[z]=rot.get(z,0)+QQ(3)/5*amp
        rot[z^3]=rot.get(z^3,0)+(QQ(4)/5 if b1 else -QQ(4)/5)*amp
mu2,G2=gram(rot)
assert mu2==mu and G2==G
overlap=sum(psi.get(z,0).conjugate()*a for z,a in rot.items())/n
assert overlap==QQ(43)/55

def occupied(v,S):
    mask=sum(1<<j for j in S)
    norm=sum(a.conjugate()*a for a in v.values())
    return QQ(sum(a.conjugate()*a for z,a in v.items() if z & mask==mask)/norm)

sextic=next((S,occupied(psi,S),occupied(rot,S)) for S in combinations(range(n),3)
            if occupied(psi,S)!=occupied(rot,S))
# Independent Weyl-dimension check of the known Cartan-product formula.
weights=[0]*(n-1); weights[w-1]=2
dimension=int(WeylCharacterRing('A10',style='coroots')(*weights).degree())
hilbert=int(binomial(n,w))
formula=QQ(hilbert**2)*(n+1)/((w+1)*(n-w+1))
assert dimension==formula==60984 and QQ(hilbert)/dimension==QQ(1)/132
result={
    'status':'passed','n':n,'w':w,'source_support':len(psi),'source_min_distance':6,
    'incidence_rank':int(A.rank()),'variance_gram_dimension':len(pairs),
    'variance_spectrum':{'0':1,'12/11':120,'10/11':110},
    'passive_rotated_all_means_and_gram_equal':True,'rotation_overlap':'43/55',
    'higher_data_distinguishes':{'occupation_triple':list(sextic[0]),
       'original':str(sextic[1]),'rotated':str(sextic[2])},
    'hilbert_dimension':hilbert,'cartan_square_dimension':dimension,'ipr_upper_bound':'1/132',
    'general_learning_impossibility':False,'haar_tail_established_by_sampling':False,
    'quantum_execution':False,'classical_hardness':False,'novelty':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))

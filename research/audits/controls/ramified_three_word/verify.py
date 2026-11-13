from sage.all import *
from itertools import product
from collections import deque
from pathlib import Path
import json
R=PolynomialRing(QQ,'X'); X=R.gen(); K=NumberField(X**2-2,'pi'); pi=K.gen(); P=K.primes_above(2)[0]
gens=[pi,1+pi,1+2*pi,K(5)]
H=[[int(K.hilbert_symbol(a,b,P)==-1) for b in gens] for a in gens]
assert matrix(GF(2),H).rank()==4
reps=[K(prod(gens[i] for i in range(4) if (m>>i)&1)) for m in range(16)]
def hb(a,b):return sum(((a>>i)&1)*((b>>j)&1)*H[i][j] for i in range(4) for j in range(4))%2
fingerprints={tuple(hb(m,1<<i) for i in range(4)):m for m in range(16)}
neg=fingerprints[tuple(int(K.hilbert_symbol(K(-1),g,P)==-1) for g in gens)]
INF=1000
def defect(a):
 a=K(a); val=int(a.valuation(P))
 if val%2:return 0
 a=a/pi**val; best=0
 for i in range(1,8,2):
  for j in range(4):
   c=a-(i+j*pi)**2; best=max(best,INF if c==0 else int(c.valuation(P)))
 return INF if best>=5 else best
df=[defect(a) for a in reps]; units=list(range(0,16,2))
u,v=0,3; initial=(0,2,1); target=(4,8)
def data(a):
 C,D=neg^a[0]^a[1],neg^a[1]^a[2]
 h,k=min(4+u,2*(u+df[C])),min(4+v,2*(v+df[D]))
 return C,D,min(h,2*u+k),min(k,2*v+h)
def allowed(C,diff):return [x for x in units if 2*df[x]>=min(4+diff,2*(diff+df[C])) and not hb(C,x)]
def state(x,z):return (initial[0]^x,initial[1]^x^z,initial[2]^z)
def moves(vtx):
 x,z=vtx;C,D,_,_=data(state(x,z))
 return [(x^a,z) for a in allowed(C,u)]+[(x,z^a) for a in allowed(D,v)]
def distances(start):
 dist={start:0};prev={};todo=deque([start])
 while todo:
  a=todo.popleft()
  for b in moves(a):
   if b not in dist:dist[b]=dist[a]+1;prev[b]=a;todo.append(b)
 return dist,prev
C,D,aa,bb=data(initial);B=state(*target);Cb,Db,cc,dd=data(B)
assert (aa,bb)==(cc,dd)==(2,6)
assert 2*df[4]>=aa and 2*df[8]>=bb
assert (hb(C,4),hb(D,8),hb(4,8))==(1,1,0)
assert aa+bb==8 # source Theorem3.1(iv) strictly >2e, so inactive
reach212=set()
for t in allowed(D,v):
 if 4 in allowed(C^t,u) and 8^t in allowed(D^4,v):reach212.add(t)
reach121=set()
for t in allowed(C,u):
 if 8 in allowed(D^t,v) and 4^t in allowed(C^8,u):reach121.add(t)
assert not reach212 and not reach121
word=[(12,2),(23,4),(12,6),(23,12)]
a=initial
for where,eta in word:
 Cnow,Dnow,_,_=data(a)
 assert eta in allowed(Cnow,u) if where==12 else eta in allowed(Dnow,v)
 a=(a[0]^eta,a[1]^eta,a[2]) if where==12 else (a[0],a[1]^eta,a[2]^eta)
assert a==B
dist,_=distances((0,0));assert dist[target]==4
iso=[]
for x,z in product(units,repeat=2):
 Cb,Db,cc,dd=data(state(x,z))
 if (cc,dd)==(aa,bb) and 2*df[x]>=aa and 2*df[z]>=bb and not(hb(C,x)^hb(D,z)^hb(x,z)) and (aa+bb<=8 or not hb(C,x)):
  iso.append((x,z))
assert set(dist)==set(iso)
diameter=max(max(distances(a)[0].values()) for a in dist)
result={'scope':'One exact Q2(sqrt2) example and its fixed 16-state isometry graph; no all-field completeness claim',
 'field':'pi^2=2','e':2,'f':1,'A':['1','1+pi','2*pi'],'B':['1+2*pi','25+15*pi','10*pi'],
 'generators':[str(x) for x in gens],'hilbert_bits':H,'unit_defects':{str(i):('infinity' if df[i]==INF else df[i]) for i in units},
 'negative_one_mask':neg,'alpha':[int(aa/2),int(bb/2)],'hasse_difference_bits':[hb(C,4),hb(D,8),hb(4,8)],
 'three_word_parameters':{'23_12_23':sorted(reach212),'12_23_12':sorted(reach121)},'four_word_masks':word,
 'target_minimal_word_length':dist[target],'fixed_graph_vertices':len(dist),'fixed_graph_diameter':diameter,
 'fixed_graph_distance_counts':{str(d):list(dist.values()).count(d) for d in sorted(set(dist.values()))},'PASS':True}
out=Path(__file__).with_name('result.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

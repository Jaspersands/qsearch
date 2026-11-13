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
results=[]; counter=None
for last in [0,1]:
 u,v=-2,last+2
 def data(a):
  C,D=neg^a[0]^a[1],neg^a[1]^a[2]
  h,k=min(4+u,2*(u+df[C])),min(4+v,2*(v+df[D]))
  return C,D,min(h,2*u+k),min(k,2*v+h)
 def valid(a):
  C,D,_,_=data(a)
  return u+df[C]>=0 and v+df[D]>=0
 def allowed(C,diff):return [x for x in units if 2*df[x]>=min(4+diff,2*(diff+df[C])) and not hb(C,x)]
 starts=0; comparisons=0; maxdist=0; histogram={}; extremal=None
 for b,c in product(units,repeat=2):
  initial=(0,b,c^(last%2))
  if not valid(initial):continue
  starts+=1
  def state(x,z):return (initial[0]^x,initial[1]^x^z,initial[2]^z)
  def moves(vtx):
   x,z=vtx;C,D,_,_=data(state(x,z))
   ans=[(x^a,z) for a in allowed(C,u)]+[(x,z^a) for a in allowed(D,v)]
   assert all(valid(state(*q)) for q in ans)
   return ans
  dist={(0,0):0}; prev={}; todo=deque([(0,0)])
  while todo:
   a=todo.popleft()
   for q in moves(a):
    if q not in dist:dist[q]=dist[a]+1;prev[q]=a;todo.append(q)
  C,D,aa,bb=data(initial); iso=[]
  for x,z in product(units,repeat=2):
   target=state(x,z)
   if not valid(target):continue
   Cb,Db,cc,dd=data(target)
   if (cc,dd)!=(aa,bb):continue
   if 2*df[x]<aa or 2*df[z]<bb:continue
   if hb(C,x)^hb(D,z)^hb(x,z):continue
   if aa+bb>8 and hb(C,x):continue
   iso.append((x,z));comparisons+=1
   d=dist.get((x,z))
   if d is None or d>4:
    counter={'R':[0,-2,last],'initial_masks':initial,'target_masks':target,'x':x,'z':z,'alpha':[aa/2,bb/2],'distance':d,'reached':len(dist),'isometric_prefix':len(iso)}
    break
   histogram[str(d)]=histogram.get(str(d),0)+1
   if d>maxdist:
    maxdist=d;extremal={'initial_masks':initial,'target_masks':target,'x':x,'z':z,'distance':d}
  if counter:break
  assert set(dist)==set(iso)
 results.append({'R':[0,-2,last],'valid_start_tuples':starts,'isometric_ordered_endpoint_pairs':comparisons,'max_minimal_word_length':maxdist,'distance_counts':histogram,'extremal':extremal})
 if counter:break
result={'scope':'Only Q2(sqrt2), R=(0,-2,0), then R=(0,-2,1) if first has no counterexample. No universal four-word inference.','hilbert_bits':H,'unit_defects':{str(i):('infinity' if df[i]==INF else df[i]) for i in units},'results':results,'counterexample':counter,'PASS':counter is None}
Path(__file__).with_name('result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

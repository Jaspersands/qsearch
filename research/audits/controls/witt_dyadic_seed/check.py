from sage.all import ZZ, PolynomialRing, Integers, GF
from itertools import product
from pathlib import Path
import json
P=PolynomialRing(ZZ,names=('x0','x1','x2','y0','y1','y2'));x=P.gens()[:3];y=P.gens()[3:]
def ghost(v,j): return sum(2**i*v[i]**(2**(j-i)) for i in range(j+1))
S=[];M=[]
for j in range(3):
 S.append(P((ghost(x,j)+ghost(y,j)-sum(2**i*S[i]**(2**(j-i)) for i in range(j)))/2**j))
 M.append(P((ghost(x,j)*ghost(y,j)-sum(2**i*M[i]**(2**(j-i)) for i in range(j)))/2**j))
 assert S[-1].total_degree()<=2**j and M[-1].total_degree()<=2**(j+1)
k=GF(4,'a');a=k.gen()
C=PolynomialRing(Integers(8),'t');t=C.gen();R=C.quotient(t*t+t+1,'w');w=R.gen()
tau={k(0):R(0),k(1):R(1),a:w,a+1:w*w}
assert all(z**4==z for z in tau.values())
def phi(v): return sum((2**i)*tau[c**(2**((-i)%2))] for i,c in enumerate(v))
def naive(v): return sum((2**i)*tau[c] for i,c in enumerate(v))
def key(z):
 p=z.lift();return tuple(int(p[i]) for i in range(2))
V=list(product(list(k),repeat=3))
assert len({key(phi(v)) for v in V})==64
Sk=[s.change_ring(k) for s in S];Mk=[m.change_ring(k) for m in M]
checks=0;negative=None
for v in V:
 for u in V:
  args=v+u
  vs=tuple(s(*args) for s in Sk);vm=tuple(m(*args) for m in Mk)
  assert phi(vs)==phi(v)+phi(u)
  assert phi(vm)==phi(v)*phi(u)
  if negative is None and naive(vs)!=naive(v)+naive(u):
   negative={'left':[str(c) for c in v],'right':[str(c) for c in u],'sum':[str(c) for c in vs],'wrong_image':key(naive(vs)),'actual_sum':key(naive(v)+naive(u))}
  checks+=2
assert negative is not None
out={'status':'passed','field':'F4','length':3,'ring':'Z8[w]/(w^2+w+1)','bijection_points':64,'operation_equalities':checks,'addition_degrees':[int(s.total_degree()) for s in S],'multiplication_degrees':[int(m.total_degree()) for m in M],'untwisted_negative_control':negative,'scope':'finite arithmetic/interface falsifier, not length9 search implementation or asymptotic proof'}
Path(__file__).with_name('result.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: Witt F4 length3 bijection, 8192 exact operation equalities, untwisted negative control')

from sage.all import *
from itertools import permutations, product, combinations
from collections import defaultdict
import json
K=QuadraticField(-1,'ii');ii=K.gen();N=3
v=vector(K,[1,2,2]);H=identity_matrix(K,3)-2*v.column()*v.row()/9
Us=[H,H*diagonal_matrix(K,[1,ii,1])*H]
Gs=[matrix(K,[[1,1/8,1/8],[1/8,1,z/8],[1/8,z.conjugate()/8,1]]) for z in [K(1),ii]]
def hist(o):return tuple(o.count(j) for j in range(3))
def ordered(U,G,ids,o):
 s=len(ids);z=K(0)
 for a in permutations(ids):
  for b in permutations(ids):z+=prod(U[o[j],a[j]]*U[o[j],b[j]].conjugate()*G[b[j],a[j]] for j in range(s))
 return z/factorial(s)
def prefix(U,G,ids,o):
 D={(frozenset(),frozenset()):K(1)}
 for y in o:
  E=defaultdict(lambda:K(0))
  for (A,B),z in D.items():
   for i in ids:
    if i in A:continue
    for j in ids:
     if j not in B:E[(A|{i},B|{j})]+=z*U[y,i]*U[y,j].conjugate()*G[j,i]
  D=E
 return sum(z for (A,B),z in D.items() if A==B)*factorial(len(ids)-len(o))/factorial(len(ids))
results=[]
for u,U in enumerate(Us):
 assert U.conjugate_transpose()*U==identity_matrix(K,3)
 for g,G in enumerate(Gs):
  d=QQ(1)/2;rho=1-d;Gamma=(G-d*identity_matrix(K,3))/rho
  for ids in ([0],[0,1],[0,1,2]):
   for r in range(len(ids)+1):
    for o in product(range(3),repeat=r):
     p=prefix(U,Gamma,ids,o);assert p.imag()==0 and p.real()>=0
     if r<len(ids):assert sum(prefix(U,Gamma,ids,o+(j,)) for j in range(3))==p
     else:assert p==ordered(U,Gamma,ids,o)
  truth=defaultdict(lambda:K(0));mix=defaultdict(lambda:K(0))
  for o in product(range(3),repeat=3):truth[hist(o)]+=ordered(U,G,list(range(3)),o)
  for s in range(4):
   for active in combinations(range(3),s):
    inactive=[i for i in range(3) if i not in active]
    for a in product(range(3),repeat=s):
     pa=ordered(U,Gamma,active,a)
     for b in product(range(3),repeat=3-s):
      pb=prod(U[y,i]*U[y,i].conjugate() for i,y in zip(inactive,b))
      mix[hist(a+b)]+=rho**s*d**(3-s)*pa*pb
  assert sum(truth.values())==1 and all(x.imag()==0 and x.real()>=0 for x in truth.values())
  assert dict(truth)==dict(mix)
  results.append({'U':u,'Gram':g,'outcomes':{str(k):str(z) for k,z in sorted(truth.items())}})
assert results[0]['outcomes']!=results[1]['outcomes']
print(json.dumps({'status':'PASS_EXACT_FINITE_ONLY','cases':results},indent=2))

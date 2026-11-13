from sage.all import ZZ, Integers, matrix, PolynomialRing, QQ, NumberField
import json
from pathlib import Path
K=6
M=2**K
Z=Integers(M)
cases=[('unramified',1,1),('split',1,0),('ramified',0,-2),('nonmaximal_ramified',0,-8),('nonmaximal_unramified',0,-5),('nonmaximal_split',0,-4)]
results=[]
for label,T,N in cases:
 def mul(u,v):
  a,b=u;c,d=v
  return (Z(a*c-N*b*d),Z(a*d+b*c+T*b*d))
 def norm(u):
  a,b=u
  return Z(a*a+T*a*b+N*b*b)
 gens=[]
 for j in (1,2):
  gens.extend([(Z(1+2**j),Z(0)),(Z(1),Z(2**j))])
 if T%2==0:
  r=N%2
  gens.append((Z(1-r),Z(1)))
 assert all(int(norm(u))%2 for u in gens)
 span={1:(Z(1),Z(0))}
 for g in gens:
  for c,u in list(span.items()):
   v=mul(u,g)
   span[int(norm(v))%8]=v
 actual={int(norm((Z(a),Z(b))))%8 for a in range(M) for b in range(M) if int(norm((Z(a),Z(b))))%2}
 assert set(span)==actual,(label,span,actual)
 witnesses=[]
 for eta in sorted(actual):
  u=span[eta]
  ratio=norm(u)/Z(eta)
  # Finite tiny-ring falsifier only: root enumeration is NOT the theorem algorithm.
  roots=[Z(z) for z in range(1,M,2) if Z(z*z)==ratio]
  assert roots
  v=tuple(x/roots[0] for x in u)
  assert norm(v)==Z(eta)
  assert any(int(x)%2 for x in v)
  witnesses.append({'eta':eta,'coefficients':[int(x) for x in v]})
 # Independently verify all deep units have square roots INSIDE this order at tiny precision.
 squares={mul((Z(a),Z(b)),(Z(a),Z(b))) for a in range(M) for b in range(M) if int(norm((Z(a),Z(b))))%2}
 tail={(Z(1+8*a),Z(8*b)) for a in range(M//8) for b in range(M//8)}
 assert tail<=squares,label
 results.append({'case':label,'T':T,'N':N,'norm_squareclasses':sorted(actual),'witnesses':witnesses,'tail_square_count':len(tail)})
# Existing coupled Q2 example: genuine integral binary move, no diagonal-component match.
A=matrix(ZZ,[[1,0],[0,4]])
U=matrix(ZZ,[[1,-4],[1,1]])
assert U.transpose()*A*U==5*A
assert U.det()==5
# The j=2e root branch already occurs at e=1 with residue degree2.
P=PolynomialRing(QQ,'z');z=P.gen()
F=NumberField(z*z+z+1,'w');w=F.gen()
prime=F.prime_above(2)
assert prime.ramification_index()==1 and prime.residue_class_degree()==2
root=1+2*w
assert root*root==-3
assert F.ideal(-4).valuation(prime)==2
residue=prime.residue_field();rw=residue(w)
assert rw*rw+rw==residue(1)
out={'status':'passed','precision':K,'cases':results,'binary_move':{'A':[[1,0],[0,4]],'U':[[1,-4],[1,1]],'det':5},'root_boundary_control':{'e':1,'f':2,'c':-3,'initial_y':1,'error_valuation':2,'root':'1+2w, w^2+w+1=0'},'scope':'exact finite norm-image and in-order root falsifiers; no asymptotic or general ternary proof'}
Path(__file__).with_name('result.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 6 quadratic orders, all unit norm squareclasses, in-order deep roots, binary move')

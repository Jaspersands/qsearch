"""Exact algebraic-constant-field control suggested by the independent audit."""
import json
from pathlib import Path
from sage.all import QQ, ZZ, PolynomialRing, NumberField, matrix, vector
P = PolynomialRing(QQ, names=('a','x','y'))
a,x,y = P.gens()
A = P.quotient(P.ideal(a*a-2,x*y-1), names=('ab','xb','yb'))
ab,xb,yb = A.gens()
units = [xb,ab,1+ab,A(2),xb**2*ab]
inverses = [yb,ab/2,ab-1,A(QQ(1)/2),yb**2*ab/2]
assert all(u*v==1 for u,v in zip(units,inverses))
T = PolynomialRing(QQ,'t'); t=T.gen()
K=NumberField(t*t-2,'r'); r=K.gen()
rho=A.hom([r,K(1),K(1)],K)
assert rho(ab)**2==2 and rho(ab) not in QQ
images=[rho(u) for u in units]
assert images == [K(1),r,1+r,K(2),r]
prime2=K.ideal(r)
valuations=[int(K.ideal(u).valuation(prime2)) for u in images]
assert valuations == [0,1,0,2,1]
# In Omega_A, 2a da=0 implies da=0 since a is a unit. Thus the free
# dx/x row is [1,0,0,0,2]. Once valuations cancel, the remaining unit
# is (1+r)^e3, of infinite order because its positive real embedding >1.
rows=matrix(ZZ,[[1,0,0,0,2], valuations,[0,0,1,0,0]])
expected=matrix(ZZ,[[-2,-1,0,0,1],[0,-2,0,1,0]])
assert rows.right_kernel() == expected.row_module()
for e in expected.rows():
 v=A(1)
 for i,n in enumerate(e): v *= units[i]**int(n) if n>=0 else inverses[i]**int(-n)
 assert v==1
result={'scope':'One exact nontrivial-constant-field control; no full relation algorithm or asymptotic evidence.',
 'A':'Q[a,x,y]/(a^2-2,xy-1)', 'B':'Q[r]/(r^2-2)',
 'specialization':'x=y=1, a maps to r; no rational assignment to a',
 'dlog_row':[1,0,0,0,2], 'prime_over_2_valuations':valuations,
 'relation_basis':[[int(z) for z in row] for row in expected.rows()],
 'inverse_and_relation_products_checked':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,separators=(',',':')))

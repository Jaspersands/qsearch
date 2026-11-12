from sage.all import QQ, PolynomialRing, matrix, vector
from pathlib import Path
import json
R = PolynomialRing(QQ, 'x'); x = R.gen()
a = x*(x-1)*(x-2)
f = 1+a*(x-3)**2
b = 1-(x-1)*(x-2)
U,V,W = x,x,x*(x-3)
s = (x-3).inverse_mod(f)
triples = [(x**i,R(0),R(0)) for i in range(2)] + [(R(0),x**i,R(0)) for i in range(4)] + [(R(0),R(0),x**i) for i in range(3)]
cols=[]
for u,v,w in triples:
    rf=(v-s*w)%f; ra=(v-b*u)%a
    cols.append(vector(QQ,[rf[i] for i in range(5)]+[ra[i] for i in range(3)]))
M=matrix(QQ,cols).transpose()
B=M.stack(matrix(QQ,1,9,[0]*8+[1]))
assert f.discriminant()!=0 and a.discriminant()!=0 and a.gcd(f)==1
assert (f-b*b)%a==0 and (s*s+a)%f==0
assert (V-s*W)%f==0 and (V-b*U)%a==0
assert V*V-f*U*U == -a*W*W
assert M.rank()==8 and B.det()!=0
assert U.gcd(W)==x and U.resultant(W)==0
assert (f-1)%W==0
# This is an actual integer pencil draw u=1 from a reduced degree-g input.
a0=(f-b*b)//a
b0=(-b)%a0
c0=(f-b0*b0)//a0
assert a0.degree()==2 and a0.is_monic() and a0.discriminant()!=0
assert c0-2*b0-a0==a and -b0-a0==b
assert a0.gcd(f)==1
out={'scope':'Exact native genus2 counterexample to determinant-only extraction acceptance; not a full-algorithm counterexample','f':str(f),'a':str(a),'b':str(b),'s':str(s),'U':str(U),'V':str(V),'W':str(W),'M_shape':list(M.dimensions()),'M_rank':int(M.rank()),'B_det':str(B.det()),'disc_f':str(f.discriminant()),'disc_a':str(a.discriminant()),'Res_a_f':str(a.resultant(f)),'gcd_U_W':str(U.gcd(W)),'Res_U_W':str(U.resultant(W)),'true_half_pair':[str(W),'-1'],'reduced_input':[str(a0),str(b0)],'pencil_scalar':1,'all_assertions_passed':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,sort_keys=True))

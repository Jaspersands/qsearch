import sympy as sp
T={(1,2):(5,1),(1,3):(6,1),(1,4):(7,1),(1,5):(8,-1),(2,3):(8,1),(2,4):(6,1),(2,6):(7,-1),(3,4):(5,-1),(3,5):(7,-1),(4,6):(8,-1)}
def br(x,y):
    z=[0]*8
    for (a,b),(c,s) in T.items(): z[c-1]+=s*(x[a-1]*y[b-1]-x[b-1]*y[a-1])
    return [sp.expand(w) for w in z]
l,m,n,r=sp.symbols('l m n r')
def v(**k):
    out=[0]*8
    for kk,val in k.items(): out[int(kk[1])-1]=val
    return out
D={1:v(e5=l,e6=m),2:v(e5=-n,e6=r),3:v(e5=-r,e6=-n),4:v(e5=m,e6=-l),5:v(e7=m,e8=n),6:v(e7=l,e8=r),7:[0]*8,8:[0]*8}
def Dv(x): return [sp.expand(sum(x[j-1]*D[j][i] for j in range(1,9))) for i in range(8)]
E=lambda j:[1 if i==j-1 else 0 for i in range(8)]
bad=[(a,b) for a in range(1,9) for b in range(a+1,9) if any(sp.simplify(p-q-w)!=0 for p,q,w in zip(Dv(br(E(a),E(b))),br(Dv(E(a)),E(b)),br(E(a),Dv(E(b)))))]
print("derivation failures:",bad)

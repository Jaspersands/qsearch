# brute-force RC existence for tiny p (no WLOG normalisation), from Definition plus-rc
import itertools, sys
def prim(p):
    from sympy import primefactors
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in primefactors(p-1)): return g
def exists(p,D,Delta,Omega):
    g=prim(p); cl={}
    x=1
    for k in range(p-1): cl[x]=k%D; x=x*g%p
    Om=set(Omega)
    others=[i for i in Delta if i!=0]
    for beta0 in [0]:   # translation WLOG only (to keep brute force tractable): beta_0=0
      for bs in itertools.product(range(p),repeat=len(others)):
        beta={0:0}; beta.update(dict(zip(others,bs)))
        ok=True
        for j in range(D):
            good=False
            for a in range(p):
                if j==0 and (a==0 or cl[a]!=0): continue
                if all(((a+beta[i])%p==0) or ((cl[(a+beta[i])%p]+i+j)%D in Om) for i in Delta):
                    good=True;break
            if not good: ok=False;break
        if ok: return True
    return False
CASES=[(7,3,[0,1,2],[0]),(13,3,[0,1,2],[0]),(5,4,[0,1,2,3],[0]),(13,4,[0,1,2,3],[0]),(17,4,[0,1,2,3],[0]),(41,4,[0,1,2,3],[0]),(11,5,[0,1,2,3,4],[0]),(19,9,[0,3,6],[0]),(37,9,[0,3,6],[0]),(13,6,[0,2,4],[0,3]),(7,6,[0,3],[0]),(19,9,[0,3,6],[0,1]),(37,9,[0,1],[0,4]),(13,6,[0,1,2,3,4,5],[0,1]),(13,4,[0,1,2,3],[0,2])]
for (p,D,De,Om) in CASES:
    print(p,D,De,Om,exists(p,D,De,Om))

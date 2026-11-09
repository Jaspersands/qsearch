import sys
from sympy import isprime, primitive_root
def ind_table(p,k):
    g=primitive_root(p); ind=[None]*p; x=1
    for e in range(p-1):
        ind[x]=e%k; x=x*g%p
    return ind
def find(p,k):
    """return a contraction (alpha,beta) with beta0=0, alpha0=1, or None"""
    ind=ind_table(p,k)
    ok=lambda u,m: u%p==0 or ind[u%p]==m%k
    # cells: alpha_j+beta_i in Q_{-(i+j)} or 0
    cand0=[x for x in range(p)]
    beta=[0]
    # column candidates after row 0 (beta0=0): x in Q_{-j} or 0 ; alpha0 fixed=1
    cols={j:[x for x in range(p) if ok(x,-j)] for j in range(1,k)}
    sys.setrecursionlimit(10000)
    def rec(i,cols):
        if i==k:
            return True
        for b in range(p):
            if b in beta: continue
            if not ok(1+b,-i): continue
            new={}
            for j,c in cols.items():
                nc=[x for x in c if ok(x+b,-(i+j))]
                if not nc: break
                new[j]=nc
            else:
                beta.append(b)
                if rec(i+1,new):
                    return True
                beta.pop()
        return False
    if rec(1,cols): return beta
    return None
if __name__=="__main__":
    k=int(sys.argv[1]); P=int(sys.argv[2])
    E=[]
    for p in range(k+1,P+1,k):
        if not isprime(p): continue
        if find(p,k) is None: E.append(p)
    bnd=k**3-3*k**2+2*k
    allp=[p for p in range(k+1,bnd+1,k) if isprime(p)]
    print("kappa",k,"E2 up to",P,":",E)
    print("Stepanov bound: all p<=",bnd," :",allp, "subset of E2?", set(allp)<=set(E))

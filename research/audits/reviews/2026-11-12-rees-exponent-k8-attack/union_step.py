#!/opt/anaconda3/bin/python
"""Two-level union-target steps RC(kappa; Z_kappa -> K) at a prime p (exact, exhaustive).

A step for target K (0 in K) is (alpha, beta) in F_p^kappa x F_p^kappa with
  A(i,j) = alpha_j + beta_i  in  {0} u U_{k in K} Q_{k-i-j}   for all i,j in Z_kappa,
  A(0,0) != 0  (its class is then automatically in K).
Q_m = xi^m Q_0, Q_0 = kappa-th powers, xi a primitive root.  WLOG beta_0 = 0 (shift).
Backtracking over beta_1..beta_{kappa-1}; alpha_j candidate sets are intersected.
Output: for each K (0 in K), whether a step exists, plus a witness.
"""
import sys, itertools

def prim_root(p):
    fs=[q for q in range(2,p) if (p-1)%q==0 and all(q%r for r in range(2,q))]
    for g in range(2,p):
        if all(pow(g,(p-1)//f,p)!=1 for f in fs): return g

def setup(p,k):
    g=prim_root(p)
    ind={}
    x=1
    for e in range(p-1):
        ind[x]=e%k; x=x*g%p
    return g,ind

def allowed_set(p,k,ind,K,i,j):
    cls={(kk-i-j)%k for kk in K}
    return frozenset([0]+[x for x in range(1,p) if ind[x] in cls])

def search(p,k,K,want_all=False):
    g,ind=setup(p,k)
    A=[[allowed_set(p,k,ind,K,i,j) for j in range(k)] for i in range(k)]
    # beta_0 = 0: alpha_j in A[0][j]; alpha_0 must be nonzero (A(0,0) != 0)
    X0=[set(A[0][j]) for j in range(k)]
    X0[0].discard(0)
    sols=[]
    beta=[0]*k
    def rec(i,X):
        if i==k:
            sols.append((list(beta),[min(x) for x in X]))
            return not want_all
        for b in range(p):
            Y=[]
            ok=True
            for j in range(k):
                s={x for x in X[j] if (x+b)%p in A[i][j]}
                if not s: ok=False;break
                Y.append(s)
            if ok:
                beta[i]=b
                if rec(i+1,Y): return True
        return False
    rec(1,X0)
    return g,sols

if __name__=='__main__':
    p=int(sys.argv[1]); k=int(sys.argv[2])
    maxK=int(sys.argv[3]) if len(sys.argv)>3 else k
    found=[]
    for r in range(1,maxK+1):
        for rest in itertools.combinations(range(1,k),r-1):
            K=(0,)+rest
            g,s=search(p,k,K)
            if s:
                beta,alpha=s[0]
                # verify
                _,ind=setup(p,k)
                ok=all(((alpha[j]+beta[i])%p==0) or (ind[(alpha[j]+beta[i])%p] in {(kk-i-j)%k for kk in K}) for i in range(k) for j in range(k)) and (alpha[0]+beta[0])%p!=0
                found.append(K)
                print('K=',K,'EXISTS xi=',g,'alpha=',alpha,'beta=',beta,'verified=',ok)
            else:
                print('K=',K,'none')
            sys.stdout.flush()

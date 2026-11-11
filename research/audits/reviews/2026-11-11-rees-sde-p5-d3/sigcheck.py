# Independent check of the cloud session's criterion on one 10-label set:
# L feasible <=> (nonzero g with <g,l> in {0,+-1} on L) or Sigma_L = {H y : y in {0,+-1}^L} contains a 3-dim subspace.
import itertools, numpy as np, sys
p=5; S={0,1,4}
L=[tuple(int(c) for c in w) for w in sys.argv[1].split()]
n=len(L)
# S-functional?
sf=[g for g in itertools.product(range(p),repeat=3) if any(g) and all(sum(a*b for a,b in zip(g,l))%p in S for l in L)]
print('S-functionals', len(sf))
# relation matrix H: basis of {lam : sum lam_l l = 0}
M=np.array(L).T % p  # 3 x n
def nullspace(M):
    M=M.copy()%p; r,c=M.shape; piv=[]; row=0
    for j in range(c):
        pr=next((i for i in range(row,r) if M[i,j]),None)
        if pr is None: continue
        M[[row,pr]]=M[[pr,row]]; M[row]=(M[row]*pow(int(M[row,j]),p-2,p))%p
        for i in range(r):
            if i!=row and M[i,j]: M[i]=(M[i]-M[i,j]*M[row])%p
        piv.append(j); row+=1
    free=[j for j in range(c) if j not in piv]; B=[]
    for f in free:
        x=np.zeros(c,int); x[f]=1
        for i,pj in enumerate(piv): x[pj]=(-M[i,f])%p
        B.append(x)
    return np.array(B)
H=nullspace(M); r=H.shape[0]; assert ((H@M.T)%p==0).all() and r==n-3
pw=p**np.arange(r)
Ys=np.array(list(itertools.product([0,1,4],repeat=n)))
sig=set(((Ys@H.T)%p)@pw)
print('r',r,'|Sigma|',len(sig))
def idx(v): return int((np.array(v)%p)@pw)
allv=np.array(list(itertools.product(range(p),repeat=r)))
inS=np.zeros(p**r,bool); inS[list(sig)]=True
# star: nonzero s with all multiples in Sigma (Sigma = -Sigma, so s and 2s suffice)
ids=allv@pw
star=[tuple(v) for v,i in zip(allv,ids) if i and inS[i] and inS[idx(2*v)]]
proj=[s for s in star if next(x for x in s if x)==1]
print('star',len(star),'proj',len(proj))
inStar=np.zeros(p**r,bool); inStar[[idx(s) for s in star]]=True
P=np.array(proj); found=False
for a,s1 in enumerate(P):
    # T1: projective s (after s1) with s + c s1 in star for all c
    T=[s2 for s2 in P[a+1:] if all(inStar[idx(s2+c*s1)] for c in range(1,p))]
    for b,s2 in enumerate(T):
        for s3 in T[b+1:]:
            if all(inStar[idx(s3+c1*s1+c2*s2)] for c1 in range(p) for c2 in range(1,p)):
                # s3 independent of s1,s2 is implied by s3 in T (projective, after) unless in span; check rank
                if np.linalg.matrix_rank(np.array([s1,s2,s3])) == 3:
                    found=(s1,s2,s3); break
        if found: break
    if found: break
print('FEASIBLE subspace' if found else 'INFEASIBLE', found if found else '')

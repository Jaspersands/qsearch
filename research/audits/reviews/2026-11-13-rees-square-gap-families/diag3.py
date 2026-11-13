"""For each prime p = 1 mod k up to N and each (C1) orbit parameter t (t not in mu_k), record
(c = ind zeta, theta, #z in F_p^* \ (S u T) with both sides bijective, |B|), aggregated by (c, theta)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__)); from verify import primroot
k=int(sys.argv[1]); N=int(sys.argv[2])
def isprime(n): return n>1 and all(n%d for d in range(2,int(n**.5)+1))
agg={}
for p in range(k+1,N+1,k):
    if not isprime(p): continue
    g=primroot(p); h=(p-1)//k
    ind=[0]*p; x=1
    for e in range(p-1): ind[x]=e%k; x=x*g%p
    zeta=pow(g,h,p); zp=[pow(zeta,d,p) for d in range(k)]; c=ind[zeta]; mu=set(zp)
    Bcache={}
    def B(th):
        if th not in Bcache:
            s=set()
            for z in range(1,p):
                if z in mu: continue
                U=[(j*(th-c)-ind[(1-z*zp[(-j)%k])%p])%k for j in range(k)]
                if len(set(U))==k: s.add(z)
            Bcache[th]=s
        return Bcache[th]
    for t in range(2,p):
        if t in mu: continue
        F=[ind[(zp[d]-t)%p] for d in range(k)]
        th=(F[1]-F[0])%k
        if any(F[d]!=(F[0]+d*th)%k for d in range(k)): continue
        Bs=B(th); T=set(t*s%p for s in zp)
        both=sum(1 for z in Bs if z not in T and (t*pow(z,p-2,p)%p) in Bs)
        key=(c,th); a=agg.setdefault(key,[0,0,0,0]); a[0]+=1; a[1]+=both; a[2]+=len(Bs); a[3]+=len(Bs)**2/p
for key in sorted(agg):
    a=agg[key]
    print("c=%d theta=%d  nC1(t)=%d  sum both=%d  mean|B|=%.1f  indep.pred both=%.1f"%(key[0],key[1],a[0],a[1],a[2]/a[0],a[3]))

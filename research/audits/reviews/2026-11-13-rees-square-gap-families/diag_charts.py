"""Diagnostic: for Mobius-orbit (C1) configurations, count charts z with S-side bijective,
T-side bijective, and both, against the independent-uniform prediction p*k!/k^k."""
import sys, math
sys.path.insert(0, __import__("os").path.dirname(__file__)); from verify import primroot
k=int(sys.argv[1]); p=int(sys.argv[2])
g=primroot(p); h=(p-1)//k
ind=[0]*p; x=1
for e in range(p-1): ind[x]=e%k; x=x*g%p
zeta=pow(g,h,p); zp=[pow(zeta,d,p) for d in range(k)]; c=ind[zeta]
mu=set(zp)
full=(1<<k)-1
for t in range(1,p):
    if t in mu: continue
    F=[ind[(zp[d]-t)%p] for d in range(k)]
    th=(F[1]-F[0])%k
    if any(F[d]!=(F[0]+d*th)%k for d in range(k)): continue
    u=[F[j] for j in range(k)]
    v=[(i*c+F[(-i)%k]-F[0])%k for i in range(k)]
    T=[t*s%p for s in zp]
    nS=nT=nB=0; prodS=prodT=0
    for z in range(p):
        if z in mu or z in T: continue
        U=[(u[j]-ind[(zp[j]-z)%p])%k for j in range(k)]
        V=[(v[i]-ind[(T[i]-z)%p])%k for i in range(k)]
        bs=len(set(U))==k; bt=len(set(V))==k
        nS+=bs; nT+=bt; nB+=bs and bt
    e1=p*math.factorial(k)/k**k
    print("t=%d theta=%d c=%d  S-bij %d  T-bij %d  both %d   pred single %.1f both %.2f"%(t,th,c,nS,nT,nB,e1,e1*math.factorial(k)/k**k))

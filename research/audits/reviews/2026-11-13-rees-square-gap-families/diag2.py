import sys, math, os
sys.path.insert(0, os.path.dirname(__file__)); from verify import primroot
k=int(sys.argv[1]); p=int(sys.argv[2]); C1only=int(sys.argv[3])
g=primroot(p); h=(p-1)//k
ind=[0]*p; x=1
for e in range(p-1): ind[x]=e%k; x=x*g%p
zeta=pow(g,h,p); zp=[pow(zeta,d,p) for d in range(k)]; c=ind[zeta]
mu=set(zp)
cnt=0
for t in range(2,p):
    if t in mu: continue
    F=[ind[(zp[d]-t)%p] for d in range(k)]
    th=(F[1]-F[0])%k
    isc1 = all(F[d]==(F[0]+d*th)%k for d in range(k))
    if C1only and not isc1: continue
    # generic separable parts even if not C1: use row0/col0 decomposition
    u=[F[j] for j in range(k)]
    v=[(i*c+F[(-i)%k]-F[0])%k for i in range(k)]
    T=[t*s%p for s in zp]
    Sb=set(); Tb=set()
    for z in range(1,p):
        if z in mu or z in T: continue
        U=[(u[j]-ind[(zp[j]-z)%p])%k for j in range(k)]
        V=[(v[i]-ind[(T[i]-z)%p])%k for i in range(k)]
        if len(set(U))==k: Sb.add(z)
        if len(set(V))==k: Tb.add(z)
    inv=lambda z: t*pow(z,p-2,p)%p
    print("t=%d C1=%d th=%d |Sb|=%d |Tb|=%d |Sb&Tb|=%d  |iota(Sb)&Tb|=%d  pred %.2f"%(t,isc1,th,len(Sb),len(Tb),len(Sb&Tb),len(set(map(inv,Sb))&Tb),len(Sb)*len(Tb)/p))
    cnt+=1
    if cnt>=8: break

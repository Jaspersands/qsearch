import itertools, random, numpy as np
rng = random.Random(5)
p, n = 7, 2
om = np.exp(2j*np.pi/p)
pts = list(itertools.product(range(p), repeat=n)); idx = {x:i for i,x in enumerate(pts)}
# random cubic P (coefficients for monomials deg1..3)
mons = [m for d in range(1,4) for m in itertools.product(range(4), repeat=n) if sum(m)==d]
coef = {m: rng.randrange(p) for m in mons}
for m in coef:
    if sum(m)==3 and coef[m]==0: coef[m]=rng.randrange(1,p)
Pv = np.array([sum(c*np.prod([pow(x[j],m[j],p) for j in range(n)]) for m,c in coef.items())%p for x in pts])
u0 = (1,3); U = {((t*u0[0])%p,(t*u0[1])%p) for t in range(p)}
N = p**n
rho = np.zeros((N,N),complex)
for i,x in enumerate(pts):
    for u in U:
        y = ((x[0]+u[0])%p,(x[1]+u[1])%p); j = idx[y]
        rho[i,j] = om**((Pv[i]-Pv[j])%p)/N
print("trace", np.trace(rho).real, "purity", np.trace(rho@rho).real, "expected", p**-(n-1))
def W(a,b):
    M = np.zeros((N,N),complex)
    for i,x in enumerate(pts):
        y = tuple((x[j]+a[j])%p for j in range(n))
        M[idx[y],i] = om**(sum(b[j]*x[j] for j in range(n))%p)
    return M
Ws = {(a,b): W(a,b) for a in pts for b in pts}
# Weyl characteristic support
cf = {k: abs(np.trace(rho@M)) for k,M in Ws.items()}
print("mass of |Tr(rho W)|^2 on a in U:", sum(v**2 for (a,b),v in cf.items() if a in U), "total", sum(v**2 for v in cf.values()))
# Bell sampling on rho x rho: P(a,b) = p^-n Tr(W^dag rho W rho^T)
rT = rho.T
Pb = {k: (np.trace(M.conj().T@rho@M@rT)/N).real for k,M in Ws.items()}
print("Bell total", sum(Pb.values()))
keys = list(Ws)
def add(k1,k2): return (tuple((k1[0][j]+k2[0][j])%p for j in range(n)), tuple((k1[1][j]+k2[1][j])%p for j in range(n)))
q = {k:0.0 for k in keys}
for k1 in keys:
    for k2 in keys:
        c = add(k2, (tuple((-v)%p for v in k1[0]), tuple((-v)%p for v in k1[1])))
        q[c] += Pb[k1]*Pb[k2]
massU = sum(v for (a,b),v in q.items() if a in U)
print("Bell-difference mass on a in U:", massU, " (uniform would be", p**-(n-1), ")")
qa = {}
for (a,b),v in q.items(): qa[a] = qa.get(a,0)+v
top = sorted(qa.items(), key=lambda t:-t[1])[:10]
print("top a-marginals:", [(a, round(v,4), a in U) for a,v in top])

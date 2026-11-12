# Dixmier--Lister checks for Section 3.4 of main-core.tex (2026-11-12 harsh Sec. 3 referee).
# Independent of the repo's artifacts.  Run: nice -n 19 $E/sage dl_checks.sage
import itertools, time, sys

T = {(1,2):(5,1),(1,3):(6,1),(1,4):(7,1),(1,5):(8,-1),(2,3):(8,1),(2,4):(6,1),(2,6):(7,-1),
     (3,4):(5,-1),(3,5):(7,-1),(4,6):(8,-1)}

def C(i,j):
    """structure vector of [e_i,e_j] (1-based) as dict k->coef"""
    if (i,j) in T:
        k,s = T[(i,j)]; return {k:s}
    if (j,i) in T:
        k,s = T[(j,i)]; return {k:-s}
    return {}

def br_vec(x, y, R):
    out = [R(0)]*8
    for i in range(8):
        if x[i] == 0: continue
        for j in range(8):
            if y[j] == 0: continue
            for k,s in C(i+1,j+1).items():
                out[k-1] += s*x[i]*y[j]
    return vector(R, out)

E = [vector(ZZ, [1 if j==i else 0 for j in range(8)]) for i in range(8)]

# ---- Jacobi over ZZ
jac = all(br_vec(E[a], br_vec(E[b],E[c],ZZ),ZZ) + br_vec(E[b], br_vec(E[c],E[a],ZZ),ZZ) + br_vec(E[c], br_vec(E[a],E[b],ZZ),ZZ) == 0
          for a in range(8) for b in range(8) for c in range(8))
print("Jacobi over Z:", jac)

# ---- centre over QQ
cvars = [var('c%d'%i) for i in range(8)]
Rq = QQ
cen = []
M = matrix(QQ, [[br_vec(E[i], E[j], QQ)[k] for j in range(8)] for i in range(8) for k in range(8)])
# central z: sum_j z_j [e_i,e_j] = 0 for all i
print("centre dim over Q:", M.right_kernel().dimension(), "basis:", M.right_kernel().basis())
for p in [3,5,7,11,13]:
    print("  centre dim mod %d:" % p, M.change_ring(GF(p)).right_kernel().dimension())

# ---- derivation equations: unknown D[a][b] = coefficient of e_b in D e_a, index 8*a+b
rows = []
for i in range(8):
    for j in range(i+1,8):
        for k in range(8):
            row = [0]*64
            # D([e_i,e_j])_k
            for l,s in C(i+1,j+1).items():
                row[8*(l-1)+k] += s
            # - [D e_i, e_j]_k = - sum_l D[i][l] c_{l j}^k
            for l in range(8):
                for kk,s in C(l+1,j+1).items():
                    if kk-1 == k: row[8*i+l] -= s
            # - [e_i, D e_j]_k
            for l in range(8):
                for kk,s in C(i+1,l+1).items():
                    if kk-1 == k: row[8*j+l] -= s
            rows.append(row)
Meq = matrix(ZZ, rows)
print("derivation system: %d equations in %d unknowns" % (Meq.nrows(), Meq.ncols()))
print("rank over Q:", Meq.rank())
for p in primes(2,30):
    print("  rank mod %d: %d  (derivation dim %d)" % (p, Meq.change_ring(GF(p)).rank(), 64-Meq.change_ring(GF(p)).rank()))

# paper's parametrisation: lambda, mu, nu, rho and x_1..x_4 in span(e7,e8)
def Dparam(lam,mu,nu,rho,X):
    D = [[0]*8 for _ in range(8)]
    def setv(a, d):
        for k,v in d.items(): D[a-1][k-1] += v
    setv(1,{5:lam,6:mu}); setv(2,{5:-nu,6:rho}); setv(3,{5:-rho,6:-nu}); setv(4,{5:mu,6:-lam})
    for a in range(4):
        setv(a+1,{7:X[a][0],8:X[a][1]})
    setv(5,{7:mu,8:nu}); setv(6,{7:lam,8:rho})
    return vector(ZZ, [D[a][b] for a in range(8) for b in range(8)])
basisD = []
for idx in range(4):
    v = [0,0,0,0]; v[idx]=1
    basisD.append(Dparam(v[0],v[1],v[2],v[3],[[0,0]]*4))
for a in range(4):
    for t in range(2):
        X = [[0,0] for _ in range(4)]; X[a][t] = 1
        basisD.append(Dparam(0,0,0,0,X))
BD = matrix(ZZ, basisD)
print("paper parametrisation: rank", BD.rank(), "; all satisfy equations:", (Meq*BD.transpose()) == 0)
print("kernel over Q equals span of paper parametrisation:", Meq.right_kernel().dimension() == 12 and BD.rank()==12)

# ---- integer certificates: for each of the 32 coefficients (e_1..e_4 parts of D e_a), the least N in
# {1,...,72} with N*unit in the Z-row lattice of Meq
Rlat = Meq.row_module()
Ns = []
for a in range(8):
    for b in range(4):
        u = vector(ZZ, [1 if t == 8*a+b else 0 for t in range(64)])
        Nmin = None
        for N in range(1,73):
            if N*u in Rlat:
                Nmin = N; break
        Ns.append(Nmin)
print("least integer multipliers for the 32 coefficients:", sorted(set(Ns)), " (None = not found up to 72)")
print("all multipliers have prime factors in {2,3}:", all(N is not None and all(q in (2,3) for q,_ in factor(N)) for N in Ns))

# ---- u-basis table over Q(i)
Rx.<X> = QQ[]
K.<I> = NumberField(X^2+1)
EK = [vector(K, list(e)) for e in E]
u1 = I*EK[0]+EK[3]; u2 = EK[2]-I*EK[1]; u3 = EK[3]-I*EK[0]; u4 = EK[2]+I*EK[1]
vp = EK[4]+I*EK[5]; vm = EK[4]-I*EK[5]; e7 = EK[6]; e8 = EK[7]
b = lambda x,y: br_vec(x,y,K)
table = {
 "[u1,u2]=2v+": b(u1,u2)==2*vp, "[u3,u4]=2v-": b(u3,u4)==2*vm, "[u1,u3]=2i e7": b(u1,u3)==2*I*e7,
 "[u2,u4]=-2i e8": b(u2,u4)==-2*I*e8, "[u1,u4]=0": b(u1,u4)==0, "[u2,u3]=0": b(u2,u3)==0,
 "[u1,v+]=-2i e8": b(u1,vp)==-2*I*e8, "[u2,v+]=-2e7": b(u2,vp)==-2*e7, "[u3,v-]=2i e8": b(u3,vm)==2*I*e8,
 "[u4,v-]=-2e7": b(u4,vm)==-2*e7, "[U+,v-]=0": b(u1,vm)==0 and b(u2,vm)==0, "[U-,v+]=0": b(u3,vp)==0 and b(u4,vp)==0,
 "[v+,v-]=0": b(vp,vm)==0,
}
print("u-basis table over Q(i):", table, "ALL:", all(table.values()))

# ---- sign automorphism
sg = [1,-1,1,-1,-1,1,-1,-1]
ok = all((sg[i]*sg[j] == sg[k-1]*1) for (i1,j1),(k,s) in T.items() for i,j in [(i1-1,j1-1)])
print("sign automorphism (fix e1,e3,e6; negate others) preserves table:", ok, "; acts on e7,e8 by", sg[6], sg[7])

# ---- Prop 3.7 by Groebner elimination over GF(p): possible central scalars zeta (over the algebraic closure)
def central_scalars(p, timeout_note=""):
    F = GF(p)
    names = ['a%d%d'%(j,l) for j in range(4) for l in range(4)] + ['b%d%d'%(j,l) for j in range(4) for l in range(2)] + ['w','z']
    R = PolynomialRing(F, names, order='degrevlex')
    g = R.gens()
    A = [[g[4*j+l] for l in range(4)] for j in range(4)]
    B = [[g[16+2*j+l] for l in range(2)] for j in range(4)]
    w, z = g[24], g[25]
    phi = [None]*8
    for j in range(4):
        phi[j] = vector(R, A[j] + B[j] + [0,0])
    phi[4] = br_vec(phi[0],phi[1],R); phi[5] = br_vec(phi[0],phi[2],R)
    phi[6] = br_vec(phi[0],phi[3],R); phi[7] = br_vec(phi[1],phi[2],R)
    eqs = []
    for i in range(8):
        for j in range(i+1,8):
            lhs = br_vec(phi[i],phi[j],R)
            rhs = vector(R,[0]*8)
            for k,s in C(i+1,j+1).items(): rhs += s*phi[k-1]
            eqs += list(lhs-rhs)
    e7v = vector(R,[0]*6+[1,0]); e8v = vector(R,[0]*7+[1])
    eqs += list(phi[6]-z*e7v) + list(phi[7]-z*e8v)
    eqs.append(w*matrix(R,A).det()-1)
    I_ = R.ideal([e for e in eqs if e != 0])
    t0 = time.time()
    el = I_.elimination_ideal([v for v in g if v != z])
    return el.gens(), time.time()-t0

import sys as _sys
MODE = _sys.argv[1] if len(_sys.argv) > 1 else "elim"
if MODE == "none":
    print("Groebner parts skipped (mode none)")
elif MODE == "elim":
    for p in [5,7,11,13]:
        gens, dt = central_scalars(p)
        print("Prop 3.7 elimination ideal in zeta over GF(%d):" % p, [factor(q) for q in gens], "(%.1fs)" % dt)
        sys.stdout.flush()
else:
    # fixed-zeta unit-ideal test: is there an automorphism over the algebraic closure of GF(p)
    # acting on the centre by the scalar zeta?
    def fixed(p, zeta):
        F = GF(p)
        names = ['a%d%d'%(j,l) for j in range(4) for l in range(4)] + ['b%d%d'%(j,l) for j in range(4) for l in range(2)] + ['w']
        R = PolynomialRing(F, names, order='degrevlex')
        g = R.gens()
        A = [[g[4*j+l] for l in range(4)] for j in range(4)]
        B = [[g[16+2*j+l] for l in range(2)] for j in range(4)]
        w = g[24]
        phi = [None]*8
        for j in range(4):
            phi[j] = vector(R, A[j] + B[j] + [0,0])
        phi[4] = br_vec(phi[0],phi[1],R); phi[5] = br_vec(phi[0],phi[2],R)
        phi[6] = br_vec(phi[0],phi[3],R); phi[7] = br_vec(phi[1],phi[2],R)
        eqs = []
        for i in range(8):
            for j in range(i+1,8):
                lhs = br_vec(phi[i],phi[j],R)
                rhs = vector(R,[0]*8)
                for k,s in C(i+1,j+1).items(): rhs += s*phi[k-1]
                eqs += list(lhs-rhs)
        e7v = vector(R,[0]*6+[1,0]); e8v = vector(R,[0]*7+[1])
        eqs += list(phi[6]-zeta*e7v) + list(phi[7]-zeta*e8v)
        eqs.append(w*matrix(R,A).det()-1)
        I_ = R.ideal([e for e in eqs if e != 0])
        return I_.groebner_basis() == [1]
    for p in [5,7]:
        for zeta in range(1,p):
            t0 = time.time()
            try:
                alarm(300)
                unit = fixed(p, zeta)
                cancel_alarm()
                print("p=%d zeta=%d: no automorphism over closure: %s (%.1fs)" % (p, zeta, unit, time.time()-t0))
            except AlarmInterrupt:
                print("p=%d zeta=%d: NOT computed (timeout 300s)" % (p, zeta))
            sys.stdout.flush()

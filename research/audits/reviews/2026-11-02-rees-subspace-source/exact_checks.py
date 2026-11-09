"""Independent exact/float checks for main.tex Theorem thm:subspace-source and
its composition with the zero-moment projective Rees source.

Run: /opt/anaconda3/bin/python -B exact_checks.py  (from this folder).
Part A: LCU growth instrument with and without recovery (float, exact linear algebra).
Part B: principal-angle identities and the delta^2/2 overlap gap (float).
Part C: whole exterior source on the Rees cover of Heis(F_p), p=3,5, left-regular R,
        nonnormal H with nontrivial determinant character (float, dense matrices).
Part D: exact (Fraction) tail of the growth clock versus r*2^-B.
Part E: re-derive the paper's quoted budgets from T independently of the module.
"""
import itertools, math, sys
from fractions import Fraction
import numpy as np

rng = np.random.default_rng(20261102)
TOL = 1e-9
out = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

# ---------- shared helpers ----------
def perm_op(d, k, perm):
    """Operator permuting k tensor factors of C^d: factor i -> position perm[i]."""
    D = d**k; M = np.zeros((D, D))
    for idx in itertools.product(range(d), repeat=k):
        new = [0]*k
        for i, j in enumerate(perm): new[j] = idx[i]
        a = np.ravel_multi_index(idx, (d,)*k); b = np.ravel_multi_index(new, (d,)*k)
        M[b, a] = 1
    return M

def sign(perm):
    s, seen = 1, set()
    for i in range(len(perm)):
        if i in seen: continue
        j, L = i, 0
        while j not in seen: seen.add(j); j = perm[j]; L += 1
        s *= (-1)**(L-1)
    return s

def antisym(d, k):
    A = sum(sign(p)*perm_op(d, k, p) for p in itertools.permutations(range(k)))
    return A/math.factorial(k)

def kron(*ms):
    r = np.array([[1.0+0j]])
    for m in ms: r = np.kron(r, m)
    return r

def rand_frame(d, r):
    Q, _ = np.linalg.qr(rng.normal(size=(d, r))+1j*rng.normal(size=(d, r)))
    return Q

def wedge(Q):
    d, r = Q.shape; v = 0
    for p in itertools.permutations(range(r)):
        v = v + sign(p)*kron(*[Q[:, [p[i]]] for i in range(r)])
    return (v/math.sqrt(math.factorial(r))).ravel()

def ptrace_last(rho, d, k):
    """Trace out the last C^d factor of a (k+1)-factor operator."""
    D = d**k
    return np.einsum('aibi->ab', rho.reshape(D, d, D, d))

# ---------- Part A ----------
def part_A():
    log("== Part A: LCU growth instrument ==")
    for d, r in [(3, 2), (3, 3), (4, 3), (4, 2)]:
        Q = rand_frame(d, r); PV = Q@Q.conj().T; rho = PV/r
        for k in range(1, r):
            Ak = antisym(d, k); Ak1 = antisym(d, k+1)
            PVk = Ak@kron(*[PV]*k)@Ak  # projector onto wedge^k V
            # random mixed sigma in wedge^k V
            X = rng.normal(size=(d**k, 3))+1j*rng.normal(size=(d**k, 3))
            X = PVk@X; sig = X@X.conj().T; sig /= np.trace(sig)
            joint = np.kron(sig, rho)
            m = k+1  # ancilla dimension: j=0..k, j=k means identity arm
            F = np.exp(2j*np.pi*np.outer(range(m), range(m))/m)/math.sqrt(m)
            arms = []
            for j in range(m):
                if j == k: arms.append(np.eye(d**(k+1)))
                else:
                    p = list(range(k+1)); p[j], p[k] = p[k], p[j]
                    arms.append(-perm_op(d, k+1, p))
            S = sum(np.kron(np.diag(np.eye(m)[j]), arms[j]) for j in range(m))
            W = np.kron(F.conj().T, np.eye(d**(k+1)))@S@np.kron(F, np.eye(d**(k+1)))
            P0 = np.kron(np.diag(np.eye(m)[0]), np.eye(d**(k+1)))
            anc0 = np.zeros((m, m)); anc0[0, 0] = 1
            full = np.kron(anc0, joint)
            succ = P0@W@full@W.conj().T@P0
            ps = np.trace(succ).real
            want = (r-k)/(r*(k+1))
            # success state equals Ak1 joint Ak1 / ps
            succ_reg = succ.reshape(m, d**(k+1), m, d**(k+1))[0, :, 0, :]
            e_succ = np.abs(succ_reg-Ak1@joint@Ak1).max()
            rej = (np.eye(m*d**(k+1))-P0)@W@full@W.conj().T@(np.eye(m*d**(k+1))-P0)
            rec = W.conj().T@rej@W   # prescribed recovery
            rr = rec.reshape(m, d**(k+1), m, d**(k+1))
            anc_leak = np.abs(rec-np.kron(anc0, rr[0, :, 0, :])).max()
            Ic = np.eye(d**(k+1))-Ak1
            e_rej = np.abs(rr[0, :, 0, :]-Ic@joint@Ic).max()
            kept = ptrace_last(rr[0, :, 0, :], d, k)
            e_inv = np.abs(PVk@kept@PVk-kept).max()
            # without recovery: trace ancilla and fresh register
            norec = sum(rej.reshape(m, d**(k+1), m, d**(k+1))[j, :, j, :] for j in range(m))
            kept_nr = ptrace_last(norec, d, k)
            leak_nr = np.abs(PVk@kept_nr@PVk-kept_nr).max()
            log(f"d={d} r={r} k={k}: p_succ={ps:.12f} want={want:.12f} |succ-A(.)A|={e_succ:.1e} "
                f"recovery: ancilla_leak={anc_leak:.1e} |rej-(I-A)(.)(I-A)|={e_rej:.1e} "
                f"kept_outside_wedgeV={e_inv:.1e}; NO recovery: kept_outside_wedgeV={leak_nr:.2e}")
            assert abs(ps-want) < TOL and e_succ < TOL and anc_leak < TOL and e_rej < TOL and e_inv < TOL
        # completion is Omega_V
        Om = wedge(Q)
        Ar = antisym(d, r)
        st = Ar@kron(*[PV]*r)@Ar
        st = st/np.trace(st)
        log(f"d={d} r={r}: top state == |Omega_V><Omega_V| err={np.abs(st-np.outer(Om, Om.conj())).max():.1e}; "
            f"naive one-shot success {np.trace(Ar@kron(*[rho]*r)).real:.6f} vs r^-r={r**-r:.6f}")

# ---------- Part B ----------
def part_B():
    log("== Part B: principal angles, TD, overlap gap ==")
    worst_ratio = 0
    for trial in range(400):
        d = int(rng.integers(2, 8)); r = int(rng.integers(1, d+1))
        Q = rand_frame(d, r)
        # random unitary, sometimes near identity
        Z = rng.normal(size=(d, d))+1j*rng.normal(size=(d, d)); Hm = (Z+Z.conj().T)/2
        t = [1e-2, 1e-1, 1, 3][trial % 4]
        w, Vv = np.linalg.eigh(Hm); U = Vv@np.diag(np.exp(1j*t*w))@Vv.conj().T
        P = Q@Q.conj().T; Pu = U@P@U.conj().T
        td = 0.5*np.abs(np.linalg.eigvalsh((P-Pu)/r)).sum()
        cosines = np.clip(np.linalg.svd(Q.conj().T@U@Q, compute_uv=False), 0, 1)
        sines = np.sort(np.clip(np.linalg.svd((np.eye(d)-Q@Q.conj().T)@U@Q, compute_uv=False), 0, 1))
        ov = abs(np.linalg.det(Q.conj().T@U@Q))
        assert abs(td-sines.sum()/r) < 1e-8, (td, sines)
        assert abs(ov-np.prod(cosines)) < 1e-8
        if r <= 3 and d <= 5:
            assert abs(abs(np.vdot(wedge(Q), kron(*[U]*r)@wedge(Q)))-ov) < 1e-8
        assert ov <= 1-td**2/2+1e-12 and ov <= (1-td**2)**(r/2)+1e-12
        if td > 1e-6: worst_ratio = max(worst_ratio, (1-ov)/(td**2/2))
    log(f"400 random (d<=7,r<=d) cases: TD=(1/r)sum sin, overlap=prod cos, overlap<=1-TD^2/2 all hold; "
        f"max (1-overlap)/(TD^2/2) observed = {worst_ratio:.3f} (>=1 required)")
    # tightness at r=1 small angle
    th = 1e-3; log(f"r=1, theta=1e-3: (1-cos)/(sin^2/2) = {(1-math.cos(th))/(math.sin(th)**2/2):.8f} (gap delta^2/2 tight to 2nd order)")

# ---------- Part C: Heisenberg group and Rees cover ----------
def heis(p):
    G = [(x, y, z) for x in range(p) for y in range(p) for z in range(p)]
    inv2 = pow(2, -1, p)
    def mul(a, b):  # BCH on L=span(X,Y,Z), [X,Y]=Z
        return ((a[0]+b[0]) % p, (a[1]+b[1]) % p,
                (a[2]+b[2]+inv2*(a[0]*b[1]-a[1]*b[0])) % p)
    def inv(a): return ((-a[0]) % p, (-a[1]) % p, (-a[2]) % p)
    return G, mul, inv

def part_C():
    log("== Part C: exterior source on the Rees cover of Heis(F_p) ==")
    for p, design, Hname in [(3, (1, 1, 1, 2, 2, 2), "<X>"), (5, (1, 2, 3, 4), "<X>"),
                             (5, (1, 2, 3, 4), "<X,Z>"), (3, (1, 1, 1, 2, 2, 2), "<Z>")]:
        G, mul, inv = heis(p); idx = {g: i for i, g in enumerate(G)}; n = len(G)
        # sanity: design moments
        assert all(sum(s**j for s in design) % p == 0 for j in (1, 2)) and len(set(design)) >= 2
        if Hname == "<X>": Hgen = [(1, 0, 0)]
        elif Hname == "<X,Z>": Hgen = [(1, 0, 0), (0, 0, 1)]
        else: Hgen = [(0, 0, 1)]
        H = {(0, 0, 0)}
        while True:
            new = {mul(a, b) for a in H for b in Hgen} | H
            if new == H: break
            H = new
        H = sorted(H)
        # left regular rep L(g)|x> = |g x>
        def L(g):
            M = np.zeros((n, n))
            for x in G: M[idx[mul(g, x)], idx[x]] = 1
            return M
        Lm = {g: L(g) for g in G}
        # character chi of H: chi(exp(aX + cZ)) = w^(a) on <X>, w^(a+c) on <X,Z>, w^c on <Z>
        w = np.exp(2j*np.pi/p)
        def chi(h):
            return w**((h[0]+h[2]) % p)
        # right cosets H g give one chi-isotypic vector each (L(h)v = chi(h)v)
        reps, seen = [], set()
        for g in G:
            if g in seen: continue
            reps.append(g); seen |= {mul(h, g) for h in H}
        vecs = []
        for g in reps:
            v = np.zeros(n, complex)
            for h in H: v[idx[mul(h, g)]] += np.conj(chi(h))
            vecs.append(v/np.linalg.norm(v))
        Bm = np.array(vecs).T
        r = 2
        Q, _ = np.linalg.qr(Bm@(rng.normal(size=(len(reps), r))+1j*rng.normal(size=(len(reps), r))))
        PV = Q@Q.conj().T
        f = {g: np.linalg.det(Q.conj().T@Lm[g]@Q) for g in G}
        stab = [g for g in G if np.abs(Lm[g]@PV@Lm[g].T-PV).max() < 1e-9]
        ray = [g for g in G if abs(abs(f[g])-1) < 1e-9]
        assert sorted(stab) == H and sorted(ray) == H
        dets = {h: f[h] for h in H}
        nontriv = max(abs(dets[h]-1) for h in H)
        assert all(abs(dets[h]-chi(h)**r) < 1e-9 for h in H)
        tds = [0.5*np.abs(np.linalg.eigvalsh((PV-Lm[g]@PV@Lm[g].T)/r)).sum() for g in G if g not in H]
        delta = min(tds); gam_true = 1-max(abs(f[g]) for g in G if g not in H)
        assert gam_true >= delta**2/2-1e-12
        normal = all(sorted(mul(mul(g, h), inv(g)) for h in H) == H for g in G)
        log(f"p={p} H={Hname} |H|={len(H)} normal={normal} rank r={r}: stab(V)=ray-stab(Omega)=H; "
            f"max|det-1| on H={nontriv:.3f}; delta=min TD={delta:.4f}; true overlap gap={gam_true:.4f} >= delta^2/2={delta**2/2:.4f}")
        # Rees cover A = tL + t^2 gamma_2 : coordinates (x1,y1,z1 ; z2) ; class 2 BCH
        inv2 = pow(2, -1, p)
        A = [(x, y, z1, z2) for x in range(p) for y in range(p) for z1 in range(p) for z2 in range(p)]
        def amul(a, b):  # [tX,tY]=t^2 Z ; tZ central
            return ((a[0]+b[0]) % p, (a[1]+b[1]) % p, (a[2]+b[2]) % p,
                    (a[3]+b[3]+inv2*(a[0]*b[1]-a[1]*b[0])) % p)
        def ainv(a): return tuple((-t) % p for t in a)
        def E(s, a):  # E_s(t x + t^2 z2) = s x + s^2 z2 ; group hom
            return ((s*a[0]) % p, (s*a[1]) % p, (s*a[2]+s*s*a[3]) % p)
        # hom check
        for _ in range(200):
            a, b = A[rng.integers(len(A))], A[rng.integers(len(A))]
            for s in set(design): assert E(s, amul(a, b)) == mul(E(s, a), E(s, b))
        # hlift from Lemma homogeneous: C_1 in h (grade 1), C_2 in h cap gamma_2
        hset = set(H)
        def in_hlift(a):
            g1 = (a[0], a[1], a[2]) in hset  # exp(C1) with C1 = (x,y,z1) in h, since h is a subspace and log is coordinates
            g2 = (0, 0, a[3]) in hset
            return g1 and g2
        Ht = [a for a in A if in_hlift(a)]
        N = len(A)
        # verify Ht is the kernel of the full tuple condition E_s(C) in h for all s != 0
        assert sorted(Ht) == sorted(a for a in A if all(E(s, a) in hset for s in range(1, p)))
        for label, pts in [("zero-moment design", design), ("plain c distinct points (1,2)", (1, 2))]:
            for k in (1, 3):
                F = {a: np.prod([f[E(s, a)] for s in pts])**k for a in A}
                in_err = max(abs(F[a]-1) for a in Ht)
                off = max(abs(F[a]) for a in A if a not in set(Ht))
                if label.startswith("zero"):
                    Aidx = {a: i for i, a in enumerate(A)}
                    sig = np.zeros((N, N), complex); tau = np.zeros((N, N))
                    for a in A:
                        for b in A:
                            c = amul(ainv(b), a); sig[Aidx[a], Aidx[b]] = F[c]/N
                            tau[Aidx[a], Aidx[b]] = (1.0 if c in set(Ht) else 0.0)/N
                    td = 0.5*np.abs(np.linalg.eigvalsh(sig-tau)).sum()
                    bound = math.sqrt(N)*(1-gam_true)**k/2
                    # left-coset structure: tau = mixture of |aH~><aH~|
                    cos = {}
                    for a in A: cos.setdefault(frozenset(amul(a, h) for h in Ht), None)
                    tau2 = np.zeros((N, N))
                    for C in cos:
                        v = np.zeros(N)
                        for a in C: v[Aidx[a]] = 1/math.sqrt(len(Ht))
                        tau2 += np.outer(v, v)/len(cos)
                    log(f"   {label} {pts} k={k}: |F-1| on H~={in_err:.1e}, max|F| off H~={off:.4f}, "
                        f"TD(sigma,tau)={td:.4e} <= sqrt(N)(1-g)^k/2={bound:.4e}; tau==left-coset mixture err={np.abs(tau-tau2).max():.1e}")
                    assert in_err < 1e-9 and td <= bound+1e-12 and np.abs(tau-tau2).max() < 1e-12
                else:
                    m1 = [sum(x**j for x in pts) % p for j in (1, 2)]
                    verdict = "cancelled (accident: moments mod p=%s, or k%%p==0)" % m1 if in_err < 1e-9 else "NOT cancelled => in-coset phases != 1, wrong density"
                    log(f"   {label} k={k}: |F-1| on H~={in_err:.3f}: {verdict}")

# ---------- Part D: exact clock tail ----------
def part_D():
    log("== Part D: exact growth-clock tail vs r*2^-B ==")
    worst = 0
    for r in range(2, 9):
        ps = [Fraction(r-k, r*(k+1)) for k in range(1, r)]
        for B in range(1, 7):
            Ncap = r*r*B
            # distribution of total attempts = sum of geometrics, truncated at Ncap
            dist = {0: Fraction(1)}
            for pk in ps:
                nd = {}
                for t, pr in dist.items():
                    q = Fraction(1)
                    for j in range(1, Ncap-t+1):
                        nd[t+j] = nd.get(t+j, 0)+pr*q*pk; q *= (1-pk)
                dist = nd
            tail = 1-sum(dist.values())
            bound = Fraction(r, 2**B)
            assert tail <= bound
            worst = max(worst, float(tail/bound))
    log(f"r=2..8, B=1..6: exact Pr(timeout per output) <= r*2^-B always; max tail/bound = {worst:.3e}")

# ---------- Part E: budgets ----------
def part_E():
    log("== Part E: paper budgets re-derived from T ==")
    sys.path.insert(0, "../../../..")
    import json
    rep = json.load(open("../../../../research/reductions/rees_subspace_source.json"))
    for prof in rep["profiles"]:
        b = prof["budget"]; r = prof["rank"]; T = int(b["ideal_target_copies"])
        beta = Fraction(1, 24)
        if r == 1: Bt, N = 0, 0
        else:
            Bt = 0
            while Fraction(2**Bt) < Fraction(r*T)/beta: Bt += 1
            N = r*r*Bt
        raw = T*(N+1)
        log(f"r={r}: T bits={T.bit_length()} B={Bt} N={N} raw=T(N+1) ceil_log2={(raw-1).bit_length()} "
            f"artifact N={b['growth_attempts_per_output']} raw_bits={prof['raw_copy_cap_ceil_log2']} "
            f"base R calls<=rT bits={(r*T-1).bit_length()} growth instruments TN bits={(T*N-1).bit_length() if N else 0}")
        assert N == b["growth_attempts_per_output"] and (raw-1).bit_length() == prof["raw_copy_cap_ceil_log2"]
    pts = rep["public_group_profile"]["design_points"]; pp = rep["public_group_profile"]["p"]; cc = rep["public_group_profile"]["class"]
    mom = [sum(x**j for x in pts) % pp for j in range(1, cc+1)]
    log(f"p={pp} c={cc} design {pts}: exact power sums j=1..{cc} mod p = {mom}; distinct={len(set(pts))}, all nonzero={all(x % pp for x in pts)}")
    assert all(m == 0 for m in mom) and len(set(pts)) >= cc
    ib = rep["profiles"][0]["budget"]["ideal_source_budget"]
    log(f"per lifted source: M={ib['design_copies_per_block']} design copies x k={ib['blocks_per_leaf']} blocks = "
        f"{ib['copies_per_leaf']} exterior states (paper's coset-copy lift uses c=9)")

if __name__ == "__main__":
    part_A(); part_B(); part_C(); part_D(); part_E()
    log("ALL CHECKS PASSED")
    open("exact_checks.out", "w").write("\n".join(out)+"\n")

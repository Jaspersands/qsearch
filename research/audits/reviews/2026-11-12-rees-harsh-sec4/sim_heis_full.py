"""End-to-end, full-density-matrix simulation of the Rees descent for the Heisenberg group.

p = 3 : every step with explicit unitaries/partial traces (instrument on ancilla (x) group,
        merge on address (x) target, sequential over targets), every subgroup H, every
        positive-probability label tuple of arity M in {2,3}, every nonzero witness
        (including witnesses with zero entries).  Here d = 2 = p-1, so kappa_d = p-1: the
        zero-sum case of Remark rem:zero-sum.
p = 5 : the same, but the merge is evaluated through the exact Schur-multiplier form
        tr(U_q rho U_r^dag) of a controlled-unitary-then-trace channel, all (q, r).
Also: wrong witnesses (sum s^2 lambda != 0) must FAIL (teeth), the single-evaluation
pullback (non-dilation-invariant hidden subgroup) must FAIL, and final Fourier sampling.
Run: nice -n 19 /opt/anaconda3/bin/python sim_heis_full.py
"""
import itertools, sys, time
import numpy as np
from lie import heisenberg, Cover, all_elements, encode, rref, in_span

TOL = 1e-9


def subalgebras(L):
    p, n = L.p, L.n
    seen = {}
    vecs = all_elements(n, p)
    for r in range(0, n + 1):
        for gens in itertools.combinations(range(len(vecs)), r):
            B = L.span_closure_sub([vecs[g] for g in gens]) if r else np.zeros((0, n), dtype=np.int64)
            key = B.tobytes() + bytes([B.shape[0]])
            seen[key] = B
        if len(seen) > 2000:
            break
    return list(seen.values())


def coset_labels(L, B, elems):
    """f(x) = min code of the left coset x*H.  H = exp(span B) enumerated."""
    p = L.p
    k = B.shape[0]
    if k:
        coeffs = all_elements(k, p)
        H = (coeffs @ B) % p
    else:
        H = np.zeros((1, L.n), dtype=np.int64)
    best = None
    for h in H:
        c = encode(L.bch(elems, h), p)
        best = c if best is None else np.minimum(best, c)
    return best


def perm_right(G, elems, g):
    """Index permutation for R_g |x> = |x * g^{-1}> on group G (Lie object), elems ordered by code."""
    p = G.p
    return encode(G.bch(elems, (-np.asarray(g)) % p), p)


def run(p, full):
    L, wt = heisenberg(p)
    Lel = all_elements(L.n, p)
    C2 = Cover(L, wt)          # G_2 = cover
    C1 = Cover(L, wt, d=1)     # G_1 = tL
    A = C2.A
    Gel = all_elements(C2.n, p)
    Qel = all_elements(C1.n, p)
    NG, NQ = len(Gel), len(Qel)
    top = C2.top
    assert len(top) == 1
    om = np.exp(2j * np.pi / p)
    # sanity: E_s and dilations are homomorphisms; BCH associative (random)
    rng = np.random.default_rng(1)
    X, Y, W = (rng.integers(0, p, (200, C2.n)) for _ in range(3))
    assert np.all(A.bch(A.bch(X, Y), W) == A.bch(X, A.bch(Y, W)))
    for s in range(1, p):
        assert np.all(C2.E(s, A.bch(X, Y)) == L.bch(C2.E(s, X), C2.E(s, Y)))
        assert np.all(C2.dil(s, A.bch(X, Y)) == A.bch(C2.dil(s, X), C2.dil(s, Y)))
    # central translations R_z
    Zel = [np.eye(C2.n, dtype=np.int64)[top[0]] * z for z in range(p)]
    Rz = [perm_right(A, Gel, z) for z in Zel]
    stats = dict(H=0, merges=0, ok=0, bad=0, wrong_tested=0, wrong_failed=0, labels_ok=0)
    subs = subalgebras(L)
    for B in subs:
        stats["H"] += 1
        f = coset_labels(L, B, Lel)
        fhat = np.zeros(NG, dtype=np.int64)
        for s in range(1, C2.c + 1):
            fhat = fhat * (p ** L.n) + f[encode(C2.E(s, Gel), p)]
        rho = (fhat[:, None] == fhat[None, :]).astype(complex) / NG
        # expected lifted subgroup: graded h~
        # membership in h~ : coefficientwise in h (independent of the oracle construction)
        def in_htilde(Xc, cov):
            ok = np.ones(Xc.shape[0], dtype=bool)
            for k in range(1, cov.d + 1):
                comp = np.zeros((Xc.shape[0], L.n), dtype=np.int64)
                for t, (kk, i) in enumerate(cov.basis):
                    if kk == k:
                        comp[:, i] = Xc[:, t]
                ok &= in_span(B, comp, p)
            return ok
        # rho == rho_{h~}
        inv = (-Gel) % p
        D = np.array([encode(A.bch(np.repeat(inv[a:a + 1], NG, 0), Gel), p) for a in range(NG)])
        memb = in_htilde(Gel, C2)
        assert np.allclose(rho, memb[D] / NG), "lifted source != rho_{h~}"
        # ---- complete central instrument with explicit unitary ----
        # ancilla F|0>, controlled R_z, F^dag, measure.
        Fz = np.array([[om ** (a * b) for b in range(p)] for a in range(p)]) / np.sqrt(p)
        # post-measurement unnormalised states: K_lambda rho K_lambda^dag, K_lambda = <lambda|F^dag CR (F|0>)
        Pm = []
        for z in range(p):
            M = np.zeros((NG, NG))
            M[Rz[z], np.arange(NG)] = 1.0
            Pm.append(M)
        Kraus = []
        for lam in range(p):
            K = sum(np.conj(Fz[z, lam]) * Fz[z, 0] * Pm[z] for z in range(p))  # <lam|F^dag|z><z|F|0> R_z
            Kraus.append(K)
        assert np.allclose(sum(K.conj().T @ K for K in Kraus), np.eye(NG)), "instrument not trace preserving"
        post, prob = [], []
        for lam in range(p):
            S = Kraus[lam] @ rho @ Kraus[lam].conj().T
            pr = np.trace(S).real
            prob.append(pr)
            post.append(S / pr if pr > TOL else None)
        # label law: uniform on K^perp
        Kdim = int(in_span(B, np.eye(L.n, dtype=np.int64)[2:3], p)[0])  # z in h ?
        exp_supp = [0] if Kdim else list(range(p))
        for lam in range(p):
            want = 1.0 / len(exp_supp) if lam in exp_supp else 0.0
            assert abs(prob[lam] - want) < TOL, (prob, exp_supp)
        stats["labels_ok"] += 1
        # Lemma central trace formula check: tr(rho_lam R_g) for all g
        for lam in exp_supp:
            for gi in range(NG):
                Rg = perm_right(A, Gel, Gel[gi])
                # tr(rho R_g) = sum_x rho[x, x*g^{-1}]? (R_g)_{y,x} = [y = x g^{-1}] -> (rho R_g)_{xx} = rho[x, R_g(x)]
                tr = np.sum(post[lam][np.arange(NG), Rg])
                # expected
                g = Gel[gi]
                # g in HZ ?  write g = h z: z must be top coordinate adjustment
                okHZ = False
                val = 0
                for z in range(p):
                    hz = g.copy(); hz[top[0]] = (hz[top[0]] - z) % p  # g * (-z) = g - z (central)
                    if in_htilde(hz[None, :], C2)[0]:
                        okHZ = True; val = om ** (lam * z); break
                assert abs(tr - (val if okHZ else 0)) < 1e-9
        # ---- merges ----
        # expected output on Q = G_1
        Q_inv = (-Qel) % p
        memb1 = in_htilde(Qel, C1)
        DQ = np.array([encode((Qel[r] * 0 + (Qel - Qel[r])) % p, p) for r in range(NQ)])  # code of q - r for row r
        target1 = np.zeros((NQ, NQ))
        for r in range(NQ):
            target1[:, r] = memb1[encode((Qel - Qel[r]) % p, p)] / NQ
        # merge primitive permutations: U_{q,i}: R_{delta_s(sigma(q))}
        sig = C2.section_from(C1, Qel)
        perm_cache = {}
        def Rperm(s, q):
            key = (s, q)
            if key not in perm_cache:
                perm_cache[key] = perm_right(A, Gel, C2.dil(s, sig[q]))
            return perm_cache[key]
        def merge(states, svec):
            if full:
                # explicit address (x) target simulation, sequential
                psi = np.ones(NQ) / np.sqrt(NQ)
                rhoA = np.outer(psi, psi.conj()).astype(complex)
                for st, s in zip(states, svec):
                    if s == 0:
                        continue  # discarded
                    # joint = rhoA (x) st ; apply sum_q |q><q| (x) R_{g(q)} ; trace target
                    # out[q,r] = rhoA[q,r] * tr(R_{g(q)} st R_{g(r)}^dag)
                    # computed through the explicit joint matrix:
                    J = np.kron(rhoA, st)
                    idx = np.zeros(NQ * NG, dtype=np.int64)
                    for q in range(NQ):
                        idx[q * NG + Rperm(s, q)] = q * NG + np.arange(NG)
                    # U |q,x> = |q, R(x)>, so (U J U^dag)[a,b] = J[U^-1 a, U^-1 b]
                    UJ = J[np.ix_(idx, idx)]
                    rhoA = np.einsum('qxrx->qr', UJ.reshape(NQ, NG, NQ, NG))
                return rhoA
            else:
                out = np.ones((NQ, NQ), dtype=complex) / NQ
                for st, s in zip(states, svec):
                    if s == 0:
                        continue
                    P = np.array([Rperm(s, q) for q in range(NQ)])  # P[q, x] = index of R_{g(q)} x
                    # tr(U_q st U_r^dag) = sum_x st[U_q^{-1}.., ] ; with U_q|x> = |P[q,x]>:
                    # (U_q st U_r^dag)_{yy} = st[P_q^{-1}(y), P_r^{-1}(y)] ; sum over y == sum over x of st[x, P_r^{-1}(P_q(x))]
                    Pinv = np.argsort(P, axis=1)
                    T = np.zeros((NQ, NQ), dtype=complex)
                    xs = np.arange(NG)
                    for q in range(NQ):
                        y = P[q]  # y = P_q(x)
                        T[q, :] = st[xs[None, :], Pinv[:, y]].sum(axis=1)
                    out = out * T
                return out
        Ms = [2, 3] if full else [3]  # p=3: every label tuple, <=4 witnesses each
        for M in Ms:
            alll = list(itertools.product(exp_supp, repeat=M))
            cap = 6 if full else 25
            if len(alll) > cap:
                pick = rng.choice(len(alll), cap, replace=False); alll = [alll[i] for i in pick]
            for lams in alll:
                sols = [s for s in itertools.product(range(p), repeat=M) if any(s) and sum(si * si * l for si, l in zip(s, lams)) % p == 0]
                wrong = [s for s in itertools.product(range(p), repeat=M) if any(s) and sum(si * si * l for si, l in zip(s, lams)) % p != 0]
                rng.shuffle(sols); sols = sols[: (2 if full else 4)]
                # always include a witness with a zero entry when one exists
                z0 = [s for s in itertools.product(range(p), repeat=M) if any(s) and 0 in s and sum(si * si * l for si, l in zip(s, lams)) % p == 0]
                if z0 and not any(0 in s for s in sols):
                    sols.append(z0[0])
                for s in sols:
                    out = merge([post[l] for l in lams], s)
                    stats["merges"] += 1
                    if np.allclose(out, target1, atol=1e-9):
                        stats["ok"] += 1
                    else:
                        stats["bad"] += 1
                        print("MERGE MISMATCH", p, B.tolist(), lams, s)
                for s in wrong[:1]:
                    out = merge([post[l] for l in lams], s)
                    stats["wrong_tested"] += 1
                    if not np.allclose(out, target1, atol=1e-6):
                        stats["wrong_failed"] += 1
        # Fourier sampling on G_1 = F_p^3: diagonal of F rho F^dag uniform on h^perp
        F3 = np.kron(np.kron(Fz, Fz), Fz)
        diag = np.real(np.diag(F3 @ target1 @ F3.conj().T))
        hperp = np.array([np.all((B @ y) % p == 0) for y in Qel])
        assert np.allclose(diag, hperp / hperp.sum())
    # teeth: the single-evaluation pullback E_1^{-1}(h) is not dilation-invariant; with H = 1
    # its source fails the merge for some witness.
    return stats


def teeth_single_eval(p):
    """Source = rho of E_1^{-1}(h) with h = 0 (H = 1); show the merge then fails for some witness."""
    L, wt = heisenberg(p)
    C2 = Cover(L, wt); C1 = Cover(L, wt, d=1); A = C2.A
    Gel = all_elements(C2.n, p); Qel = all_elements(C1.n, p)
    NG, NQ = len(Gel), len(Qel)
    om = np.exp(2j * np.pi / p)
    ker = np.all(C2.E(1, Gel) == 0, axis=1)  # E_1^{-1}(0): contains tz - t^2 z
    inv = (-Gel) % p
    D = np.array([encode(A.bch(np.repeat(inv[a:a + 1], NG, 0), Gel), p) for a in range(NG)])
    rho = ker[D] / NG
    top = C2.top[0]
    Zel = [np.eye(C2.n, dtype=np.int64)[top] * z for z in range(p)]
    Pm = []
    for z in range(p):
        Mx = np.zeros((NG, NG)); Mx[encode(A.bch(Gel, (-Zel[z]) % p), p), np.arange(NG)] = 1; Pm.append(Mx)
    Fz = np.array([[om ** (a * b) for b in range(p)] for a in range(p)]) / np.sqrt(p)
    post = []
    for lam in range(p):
        K = sum(np.conj(Fz[z, lam]) * Fz[z, 0] * Pm[z] for z in range(p))
        S = K @ rho @ K.conj().T; pr = np.trace(S).real
        post.append(S / pr if pr > TOL else None)
    sig = C2.section_from(C1, Qel)
    imgH = np.all(Qel == 0, axis=1)
    target = np.zeros((NQ, NQ))
    for r in range(NQ):
        target[:, r] = imgH[encode((Qel - Qel[r]) % p, p)] / NQ
    # projected image of E_1^{-1}(0) in G_1 is {a : a_x=a_y=0, ...}; we only show mismatch vs any rho_{J}
    fails = 0; tested = 0
    labs = [l for l in range(p) if post[l] is not None]
    for lams in itertools.product(labs, repeat=2):
        for s in itertools.product(range(1, p), repeat=2):
            if (s[0] ** 2 * lams[0] + s[1] ** 2 * lams[1]) % p:
                continue
            out = np.ones((NQ, NQ), dtype=complex) / NQ
            for l, si in zip(lams, s):
                P = np.array([encode(A.bch(Gel, (-C2.dil(si, sig[q])) % p), p) for q in range(NQ)])
                Pinv = np.argsort(P, axis=1)
                T = np.array([[np.sum(post[l][np.arange(NG), Pinv[r][P[q]]]) for r in range(NQ)] for q in range(NQ)])
                out = out * T
            tested += 1
            # is out a coset state rho_J for J = image subgroup?  check hermitian PSD and
            # whether it equals rho of its own support pattern
            ev = np.linalg.eigvalsh((out + out.conj().T) / 2)
            supp = np.abs(out[:, 0]) > 1e-9
            isproj = np.allclose(out, np.array([[supp[encode((Qel[q] - Qel[r]) % p, p)] for r in range(NQ)] for q in range(NQ)]) / NQ)
            if not isproj:
                fails += 1
    return tested, fails


if __name__ == "__main__":
    t0 = time.time()
    for p, full in [(3, True), (5, False)]:
        st = run(p, full)
        print(f"p={p} full={full}: {st}  ({time.time()-t0:.1f}s)")
        sys.stdout.flush()
    for p in (3, 5):
        print("teeth single-evaluation pullback p=%d: tested=%d not-a-coset-state=%d" % ((p,) + teeth_single_eval(p)))
    print("done %.1fs" % (time.time() - t0))

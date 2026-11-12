"""Class-3 exact entry checks of Lemma lem:central and Proposition prop:descent on the Rees cover
of the filiform algebra <x,y,z,u | [x,y]=z, [x,z]=u> over F_5 and F_7.

All matrix entries are computed from their definitions (oracle tuple f^, Pi_lambda = sum_z chi R_z,
R_g as right translations by BCH), NOT from the paper's formulas:
  rho[a,b]        = [f^(a) = f^(b)] / N                      (Lemma lifted-source construction)
  p_lambda        = tr(Pi_lambda rho)
  rho_lambda[u,v] = (Pi rho Pi)[u,v] / p_lambda,  (R_z rho R_z')[u,v] = rho[u*z, v*(-z')]
  merge entry     = (1/|Q|) prod_i tr(R_{g_i(q)} rho_i R_{g_i(r)}^dag),  tr(R_b M R_a^dag) = sum_x M[x*b, x*a]
Expected: labels uniform on K_d^perp; output entry = 1_{H_{d-1}}(r^{-1} q)/|Q| for EVERY label tuple
and EVERY nonzero witness of sum s_i^d lambda_i = 0 (random ones, ones with zeros, repeated labels).
Teeth: wrong witnesses and a non-dilation-invariant source must fail.
Stage 3 sources come from the actual oracle; stage 2 sources are rho_{H_2} built directly.
Random (q, r) entries only: a finite falsification test.
Run: nice -n 19 /opt/anaconda3/bin/python sim_filiform.py [p ...]
"""
import itertools, sys, time
import numpy as np
from lie import filiform4, Cover, all_elements, encode, in_span, rref

rng = np.random.default_rng(20261112)


def coset_ids(G, Hbasis, elems):
    p = G.p
    k = Hbasis.shape[0]
    H = (all_elements(k, p) @ Hbasis) % p if k else np.zeros((1, G.n), dtype=np.int64)
    best = None
    for h in H:
        c = encode(G.bch(elems, h), p)
        best = c if best is None else np.minimum(best, c)
    return best, H


def graded_basis(L, hB, cov):
    """basis (cover coords) of the graded lift  sum_k t^k (h cap gamma_k) inside cover level cov.d"""
    p = L.p
    gam = L.lcs()
    rows = []
    for k in range(1, cov.d + 1):
        # h cap gamma_k
        Gk = gam[k - 1]
        # intersection via null space of [h; -Gk]
        M = np.vstack([hB, Gk]) if hB.shape[0] and Gk.shape[0] else None
        inter = []
        if M is not None:
            from lie import null_space
            N = null_space(M.T % p, p)
            for v in N:
                w = (v[: hB.shape[0]] @ hB) % p
                if np.any(w):
                    inter.append(w)
        if inter:
            I = rref(np.array(inter), p)
            for w in I:
                row = np.zeros(cov.n, dtype=np.int64)
                for t, (kk, i) in enumerate(cov.basis):
                    if kk == k:
                        row[t] = w[i]
                rows.append(row)
    return rref(np.array(rows), p) if rows else np.zeros((0, cov.n), dtype=np.int64)


class Source:
    """A source rho (as label function ids over all group elements) on cover level `cov`."""

    def __init__(self, cov, ids):
        self.cov, self.ids = cov, ids
        self.p = cov.p
        self.A = cov.A
        self.X = all_elements(cov.n, cov.p)
        self.N = len(self.X)
        self.top = cov.top
        self.Z = all_elements(len(self.top), self.p)
        self.Zc = np.zeros((len(self.Z), cov.n), dtype=np.int64)
        self.Zc[:, self.top] = self.Z
        self.om = np.exp(2j * np.pi / self.p)

    def ids_of(self, Y):
        return self.ids[encode(Y, self.p)]

    def label_law(self):
        p = self.p
        trRz = np.array([np.mean(self.ids_of(self.A.bch(self.X, z)) == self.ids) for z in self.Zc])  # (1/N)#{f(x*z)=f(x)}
        lams = self.Z
        prob = np.array([np.real(np.sum(self.om ** (-(self.Z @ lam) % p) * trRz)) / len(self.Z) for lam in lams])
        return lams, prob

    def tr_merge(self, lam, plam, b, a):
        """tr(R_b rho_lam R_a^dag) = sum_x rho_lam[x*b, x*a]"""
        p = self.p
        xb = self.A.bch(self.X, b)
        xa = self.A.bch(self.X, a)
        U = [self.ids_of(self.A.bch(xb, z)) for z in self.Zc]
        V = [self.ids_of(self.A.bch(xa, (-z) % p)) for z in self.Zc]
        tot = 0j
        for i, z in enumerate(self.Z):
            for j, z2 in enumerate(self.Z):
                cnt = np.count_nonzero(U[i] == V[j])
                if cnt:
                    tot += self.om ** (int(-(lam @ (z + z2))) % p) * cnt
        return tot / (plam * len(self.Z) ** 2 * self.N)


def solutions(lams, d, p, M):
    S = []
    for s in itertools.product(range(p), repeat=M):
        if any(s):
            v = sum(pow(si, d, p) * l for si, l in zip(s, lams)) % p
            if not np.any(v):
                S.append(s)
    return S


def merge_check(src, lower, lowerHB, d, M, npairs, nwit, label=""):
    """Run merges of M sources at level d; compare random output entries with rho_{H_{d-1}}."""
    p = src.p
    cov = src.cov
    lams_all, prob = src.label_law()
    # K_d^perp test: support and uniformity
    supp = prob > 1e-9
    KB = graded_basis(src.cov.L, src._hB, cov)  # lifted subgroup basis at this level
    Kd = [row for row in KB if all(row[t] == 0 for t in range(cov.n) if t not in cov.top)]
    Kd = np.array([[row[t] for t in cov.top] for row in Kd], dtype=np.int64).reshape(-1, len(cov.top))
    perp = np.array([np.all((Kd @ lam) % p == 0) for lam in lams_all]) if Kd.shape[0] else np.ones(len(lams_all), bool)
    assert np.array_equal(supp, perp), "label support != K^perp"
    assert np.allclose(prob[supp], 1.0 / supp.sum()), "labels not uniform on K^perp"
    res = dict(level=d, Kdim=int(Kd.shape[0]), merges=0, entries=0, bad=0, wrong=0, wrong_failed=0)
    Qel_n = lower.n
    memb = lambda Y: in_span(lowerHB, Y, p)
    good = np.nonzero(supp)[0]
    Hlow = (all_elements(lowerHB.shape[0], p) @ lowerHB) % p if lowerHB.shape[0] else np.zeros((1, lower.n), np.int64)
    for trial in range(nwit):
        li = rng.choice(good, size=M)
        if trial == 0 and M >= 2:
            li[1] = li[0]  # repeated labels
        lams = [lams_all[i] for i in li]
        sols = solutions(lams, d, p, M)
        assert sols, "no nonzero solution at this arity (choose larger M)"
        withzero = [s for s in sols if 0 in s]
        pick = [sols[rng.integers(len(sols))]]
        if withzero:
            pick.append(withzero[rng.integers(len(withzero))])
        wrongs = [s for s in itertools.product(range(1, p), repeat=M) if np.any(sum(pow(si, d, p) * l for si, l in zip(s, lams)) % p)]
        if wrongs:
            pick.append(("WRONG", wrongs[rng.integers(len(wrongs))]))
        for s in pick:
            wrong = isinstance(s, tuple) and len(s) == 2 and s[0] == "WRONG"
            sv = s[1] if wrong else s
            ok_all = True
            for pr in range(npairs):
                r = rng.integers(0, p, lower.n)
                if pr % 2 == 0:
                    h = Hlow[rng.integers(len(Hlow))]
                    q = lower.A.bch(r, h)
                    if pr % 4 == 2:  # perturb in the top grade of the lower level -> near miss
                        w = np.zeros(lower.n, np.int64); w[lower.top[rng.integers(len(lower.top))]] = rng.integers(1, p)
                        q = lower.A.bch(q, w)
                else:
                    q = rng.integers(0, p, lower.n)
                expect = float(memb(lower.A.bch((-r) % p, q)[None, :])[0])
                val = 1.0 + 0j
                for lam, si in zip(lams, sv):
                    if si == 0:
                        continue
                    plam = prob[encode(lam, p)]
                    b = cov.dil(int(si), cov.section_from(lower, q))
                    a = cov.dil(int(si), cov.section_from(lower, r))
                    val *= src.tr_merge(lam, plam, b, a)
                res["entries"] += 1
                if abs(val - expect) > 1e-8:
                    ok_all = False
                    if not wrong:
                        res["bad"] += 1
                        print("  MISMATCH", label, d, [l.tolist() for l in lams], sv, q.tolist(), r.tolist(), val, expect)
            if wrong:
                res["wrong"] += 1
                res["wrong_failed"] += int(not ok_all)
            else:
                res["merges"] += 1
    return res


def run(p, Hs, npairs=16, nwit=3):
    L, wt = filiform4(p)
    C3, C2, C1 = Cover(L, wt), Cover(L, wt, d=2), Cover(L, wt, d=1)
    Lel = all_elements(L.n, p)
    X3 = all_elements(C3.n, p)
    out = []
    for name, gens in Hs:
        t0 = time.time()
        hB = L.span_closure_sub(gens) if gens else np.zeros((0, L.n), np.int64)
        f, _ = coset_ids(L, hB, Lel)
        fhat = np.zeros(len(X3), dtype=np.int64)
        for s in range(1, 4):
            fhat = fhat * (p ** L.n) + f[encode(C3.E(s, X3), p)]
        src3 = Source(C3, fhat); src3._hB = hB
        H2B = graded_basis(L, hB, C2)
        H1B = graded_basis(L, hB, C1)
        # sanity: oracle source equals rho of graded lift (random entries)
        H3B = graded_basis(L, hB, C3)
        idx = rng.integers(0, len(X3), (4000, 2))
        diff = C3.A.bch((-X3[idx[:, 0]]) % p, X3[idx[:, 1]])
        assert np.array_equal(fhat[idx[:, 0]] == fhat[idx[:, 1]], in_span(H3B, diff, p)), "Lemma homogeneous fails"
        # dilation invariance of the lifted subgroup
        for th in range(2, p):
            assert np.all(in_span(H3B, C3.dil(th, H3B), p))
        k3 = 4 if p == 7 else 3   # arity at stage 3 (kappa_3 = 3 at p=7, 1 at p=5)
        r3 = merge_check(src3, C2, H2B, 3, k3, npairs, nwit, name)
        # stage 2 with directly built rho_{H_2}
        X2 = all_elements(C2.n, p)
        ids2, _ = coset_ids(C2.A, H2B, X2)
        src2 = Source(C2, ids2); src2._hB = hB
        r2 = merge_check(src2, C1, H1B, 2, 5, npairs, nwit, name)
        print(f"p={p} H={name}: stage3 {r3}  stage2 {r2}  ({time.time()-t0:.0f}s)")
        sys.stdout.flush()
        out.append((name, r3, r2))
    return out


def teeth_nonhomogeneous(p, npairs=12):
    """Source of the pullback E_1^{-1}(h)  cap  E_2^{-1}(h) (two points, class 3): not dilation-invariant
    for h = F_p(x+z+u) (Section example-class3 analogue). Expect merges to fail for some witnesses."""
    L, wt = filiform4(p)
    C3, C2 = Cover(L, wt), Cover(L, wt, d=2)
    Lel = all_elements(L.n, p); X3 = all_elements(C3.n, p)
    hB = L.span_closure_sub([[1, 0, 1, 1]])
    f, _ = coset_ids(L, hB, Lel)
    fhat = np.zeros(len(X3), dtype=np.int64)
    for s in (1, 2):
        fhat = fhat * (p ** L.n) + f[encode(C3.E(s, X3), p)]
    src = Source(C3, fhat)
    lams_all, prob = src.label_law()
    good = np.nonzero(prob > 1e-9)[0]
    H2B = graded_basis(L, hB, C2)
    fails = tested = 0
    for trial in range(4):
        li = rng.choice(good, size=3); lams = [lams_all[i] for i in li]
        sols = [s for s in solutions(lams, 3, p, 3) if all(s)]
        if not sols:
            continue
        s = sols[rng.integers(len(sols))]
        bad = False
        for pr in range(npairs):
            r = rng.integers(0, p, C2.n)
            H2 = (all_elements(H2B.shape[0], p) @ H2B) % p
            q = C2.A.bch(r, H2[rng.integers(len(H2))]) if pr % 2 == 0 else rng.integers(0, p, C2.n)
            # compare with rho of the image of the (non-invariant) pulled-back subgroup: entries must be a 0/1 pattern
            val = 1.0 + 0j
            for lam, si in zip(lams, s):
                plam = prob[encode(lam, p)]
                val *= src.tr_merge(lam, plam, C3.dil(int(si), C3.section_from(C2, q)), C3.dil(int(si), C3.section_from(C2, r)))
            if min(abs(val), abs(val - 1)) > 1e-8:
                bad = True
        tested += 1; fails += int(bad)
    return tested, fails


if __name__ == "__main__":
    ps = [int(a) for a in sys.argv[1:]] or [5]
    Hs = [
        ("1", []),
        ("<x+z+u>", [[1, 0, 1, 1]]),
        ("<u>", [[0, 0, 0, 1]]),
        ("<z+u>", [[0, 0, 1, 1]]),
        ("<y,u>", [[0, 1, 0, 0], [0, 0, 0, 1]]),
        ("<x+2y+3z>", [[1, 2, 3, 0]]),
        ("<y+z, u>", [[0, 1, 1, 0], [0, 0, 0, 1]]),
        ("<x,u>", [[1, 0, 0, 0], [0, 0, 0, 1]]),
        ("<y,z,u>", [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
    ]
    T0 = time.time()
    for p in ps:
        if p == 7:
            run(p, [Hs[1], Hs[3], Hs[4]], npairs=8, nwit=2)
        else:
            run(p, Hs)
        if p == 5: print("weak teeth (0/1-pattern only; superseded by teeth_twopoint.py) p=%d: tested=%d failed=%d" % ((p,) + teeth_nonhomogeneous(p)))
    print("done %.0fs" % (time.time() - T0))

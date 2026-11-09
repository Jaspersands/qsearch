#!/usr/bin/env python
"""s3 (9 Nov 2026 proof check): exact check of the merge step that a Schedule-3 node feeds
(Lemma lem:central and Prop prop:descent of main.tex, as used by Lemma s3-node(d)) on a toy
instance: the graded Heisenberg group G_2 = (t L + t^2 [L,L], *) over F_p, p = 3 and 5, with
M = 2 and M = 3 targets.  Elements (x, y, z), BCH product z + z' + (x y' - y x')/2, dilation
delta_s(x, y, z) = (s x, s y, s^2 z), section sigma(x, y) = (x, y, 0), R_g|a> = |a g^{-1}>.
For each hidden subgroup H it checks
  * delta_s is an automorphism acting on Z by s^2, and whether H is homogeneous;
  * Lemma central: label law uniform on K^perp; tr(rho_lambda R_g) = chi_lambda(z) on g = hz in HZ, 0 off HZ;
  * the channel of Prop descent, built literally (uniform address superposition, controlled right
    actions R_{delta_{s_i}(sigma(q))} on the active targets, partial trace), returns exactly
    rho_{HZ/Z} for every label tuple in (K^perp)^M and every valid nonzero witness s.
A nonhomogeneous H = exp(F_p (tx + t^2 z)) is run as a negative control (hypothesis of Prop descent
violated: valid witnesses with sum s_i lambda_i != 0 must fail).
Floating point with tolerance 1e-9; a finite check can falsify, not prove."""
import itertools
import numpy as np

def run(p, Ms):
    inv2 = pow(2, p - 2, p)
    els = [(x, y, z) for x in range(p) for y in range(p) for z in range(p)]
    idx = {g: i for i, g in enumerate(els)}
    n = len(els)
    def mul(a, b):
        return ((a[0] + b[0]) % p, (a[1] + b[1]) % p, (a[2] + b[2] + inv2 * (a[0] * b[1] - a[1] * b[0])) % p)
    def inv(a): return ((-a[0]) % p, (-a[1]) % p, (-a[2]) % p)
    def delta(s, g): return ((s * g[0]) % p, (s * g[1]) % p, (s * s * g[2]) % p)
    # delta_s automorphism, s^2 on the centre
    for s in range(1, p):
        for a in els:
            for b in els:
                assert delta(s, mul(a, b)) == mul(delta(s, a), delta(s, b))
    for a in els:
        assert mul(a, inv(a)) == (0, 0, 0)
    def Rmat(g):
        Mx = np.zeros((n, n)); gi = inv(g)
        for a in els: Mx[idx[mul(a, gi)], idx[a]] = 1.0
        return Mx
    def pinv(g):  # R_g[x, a] = 1 iff a = x g
        return np.array([idx[mul(x, g)] for x in els], dtype=np.int64)
    w = np.exp(2j * np.pi / p)
    chi = lambda lam, z: w ** ((lam * z) % p)
    Zs = [(0, 0, z) for z in range(p)]
    Pi = {lam: sum(chi(lam, -z[2]) * Rmat(z) for z in Zs) / p for lam in range(p)}
    def closure(gens):
        S = {(0, 0, 0)}; frontier = [(0, 0, 0)]
        while frontier:
            new = []
            for a in frontier:
                for g in gens:
                    b = mul(a, g)
                    if b not in S: S.add(b); new.append(b)
            frontier = new
        return S
    Hs = {"exp(F tx)": [(1, 0, 0)], "trivial": [], "Z": [(0, 0, 1)], "exp(F tx + F t^2z)": [(1, 0, 0), (0, 0, 1)],
          "exp(F ty)": [(0, 1, 0)], "G": [(1, 0, 0), (0, 1, 0)], "exp(F(tx+ty))": [(1, 1, 0)],
          "NONHOMOG exp(F(tx+t^2z))": [(1, 0, 1)]}
    qs = [(x, y) for x in range(p) for y in range(p)]
    nq = len(qs)
    sigma = lambda q: (q[0], q[1], 0)
    allok = True
    for name, gens in Hs.items():
        H = closure(gens)
        homog = all({delta(s, h) for h in H} == H for s in range(1, p))
        assert homog == (not name.startswith("NONHOMOG"))
        rhoH = sum(Rmat(h) for h in H) / n
        K = [z for z in Zs if z in H]
        Kperp = [lam for lam in range(p) if all((z[2] * lam) % p == 0 for z in K)]
        probs = {lam: np.trace(Pi[lam] @ rhoH).real for lam in range(p)}
        law_ok = all(abs(probs[l] - (len(K) / p if l in Kperp else 0.0)) < 1e-12 for l in range(p))
        rho = {l: Pi[l] @ rhoH @ Pi[l] / probs[l] for l in Kperp}
        # Lemma central trace formula
        HZ = {mul(h, z) for h in H for z in Zs}
        tr_ok = True
        for l in Kperp:
            for g in els:
                val = np.trace(rho[l] @ Rmat(g))
                if g in HZ:
                    zs = [z for h in H for z in range(p) if mul(h, (0, 0, z)) == g]
                    exp_val = chi(l, zs[0])
                    assert all(abs(chi(l, z) - exp_val) < 1e-12 for z in zs)   # independent of decomposition
                else:
                    exp_val = 0.0
                if abs(val - exp_val) > 1e-9: tr_ok = False
        Hbar = {(h[0], h[1]) for h in H}
        target = np.array([[(1.0 / nq) if (((q[0] - r[0]) % p, (q[1] - r[1]) % p) in Hbar) else 0.0
                            for r in qs] for q in qs])
        # T[l, s][q, r] = tr(R_{delta_s sigma(q)} rho_l R_{delta_s sigma(r)}^dagger), built from the matrices
        T = {}
        for l in Kperp:
            for s in range(1, p):
                Pq = [pinv(delta(s, sigma(q))) for q in qs]
                Tm = np.empty((nq, nq), dtype=complex)
                for a in range(nq):
                    for b in range(nq):
                        Tm[a, b] = rho[l][Pq[a], Pq[b]].sum()
                T[l, s] = Tm
        # spot-check the permutation-index formula against literal matrix products
        l0 = Kperp[-1]
        for (a, b) in [(0, 0), (1, nq - 1), (nq - 1, 2 % nq)]:
            A = Rmat(delta(1, sigma(qs[a]))); Bm = Rmat(delta(1, sigma(qs[b])))
            assert abs(np.trace(A @ rho[l0] @ Bm.conj().T) - T[l0, 1][a, b]) < 1e-9
        for M in Ms:
            nvalid = nvalid_fail = ninvalid = ninvalid_diff = 0
            for lams in itertools.product(Kperp, repeat=M):
                for svec in itertools.product(range(p), repeat=M):
                    if not any(svec): continue
                    valid = sum(si * si * li for si, li in zip(svec, lams)) % p == 0
                    out = np.full((nq, nq), 1.0 / nq, dtype=complex)
                    for si, li in zip(svec, lams):
                        if si: out = out * T[li, si]
                    err = np.abs(out - target).max()
                    if valid:
                        nvalid += 1
                        if err > 1e-9: nvalid_fail += 1
                    else:
                        ninvalid += 1
                        if err > 1e-9: ninvalid_diff += 1
            ok_here = law_ok and tr_ok and (nvalid_fail == 0 if homog else True)
            if homog: allok &= ok_here
            else: allok &= (law_ok and tr_ok and nvalid_fail > 0)
            print(f"p={p} M={M} H={name}: |H|={len(H)} |K|={len(K)} |K^perp|={len(Kperp)} homogeneous={homog} "
                  f"law uniform on K^perp [{law_ok}] trace formula [{tr_ok}]; valid witnesses {nvalid}, "
                  f"failing {nvalid_fail}; invalid witnesses {ninvalid}, differing {ninvalid_diff}")
    return allok

res = [run(3, [2, 3]), run(5, [2, 3])]
print("ALL OK (homogeneous: every valid witness gives rho_(HZ/Z); nonhomogeneous control fails as expected)"
      if all(res) else "SOME FAIL")

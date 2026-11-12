"""Hostile-referee checks for 2026-11-12-rees-h3z-cyclic-proof.md (Theorem C').

Independent of the proof folder's code except where stated (Part 5 reuses common.py's SDA,
sampler and stage-1 decoder ON PURPOSE, to test them adversarially; Part 5 also cross-checks the
stage-1 decoder against an independent re-implementation of Lemma D written here).

Group law (a,b,c)(a',b',c') = (a+a', b+b', c+c'+ab').  Finite checks only falsify (TRAPS 7).

Parts:
  1  sympy: power formula, delta_mu endomorphism, Lemma 2.3 sigma identity, Lemma 2.2 increment,
     iota homomorphism, k*X3 = 2 c_k - k^2 ab, the c-bound claim of Sec. 0 (counterexample k<0).
  2  explicit physical preparation (numpy, group law only): coset segment from a uniformly random
     point of D, QFT over Z_N0 of the central register, P(rho) = 1/N0 for every coset, the chirp
     phase, then psi; brute-force Gram <psi|R_k psi> by group-element lookup vs Lemma 2.2 formula,
     zero for k notin K; and the analytic 1-A <= |tau|/|I| + max|delta|/N.
  3  toy end-to-end physical Phi (brute-force Gram from group-element lookups), adversarial h:
     TV(P_y, P*_alpha) <= ||Phi-Phi*|| <= sqrt(pointwise analytic bound); cross-line zeros;
     non-primitive mu control (orthogonality must fail).
  4  constants of the proof: no-wrap, union terms b=1..400, p_bad, Lemma P' constants, enumeration
     constant, parameter inequalities and TV budget b=1..200, V and E[1/|I|] geometry.
  5  adversarial decoding at real sizes b=6 and b=10 (see decode_adv in this file).
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python referee_checks.py PART [args]
"""
import math, random, sys, cmath
from fractions import Fraction
import numpy as np

def mul(g, h): return (g[0] + h[0], g[1] + h[1], g[2] + h[2] + g[0] * h[1])
def inv(g): return (-g[0], -g[1], -g[2] + g[0] * g[1])
def pw(g, t):
    if t >= 0:
        r = (0, 0, 0)
        for _ in range(t): r = mul(r, g)
        return r
    return pw(inv(g), -t)
def C2(t): return t * (t - 1) // 2

# ------------------------------------------------------------------ Part 1
def part1():
    import sympy as sp
    a, b, c, mu, t, s, u1, u2, k, tau, p1, p2, p3 = sp.symbols('a b c mu t s u1 u2 k tau p1 p2 p3')
    C = lambda n: n * (n - 1) / 2
    M = lambda g, h: (g[0] + h[0], g[1] + h[1], g[2] + h[2] + g[0] * h[1])
    I = lambda g: (-g[0], -g[1], -g[2] + g[0] * g[1])
    P = lambda g, n: (n * g[0], n * g[1], n * g[2] + C(n) * g[0] * g[1])
    h = (a, b, c)
    out = []
    # power formula: h^(t+1) = h^t h
    out.append(('power formula h^{t+1} = h^t h', [sp.simplify(x - y) for x, y in zip(P(h, t + 1), M(P(h, t), h))]))
    # delta_mu endomorphism
    d = lambda g: (mu * g[0], mu * g[1], mu ** 2 * g[2])
    g1 = (u1, u2, s); g2 = (p1, p2, p3)
    out.append(('delta_mu endomorphism', [sp.expand(x - y) for x, y in zip(d(M(g1, g2)), M(d(g1), d(g2)))]))
    # Lemma 2.3
    kk = M(d((u1 + t * a, u2 + t * b, 0)), I(d((u1, u2, 0))))
    S = t * a * u2 + C(t) * a * b + t * c
    sig = -mu ** 2 * S + C(mu) * t * (2 * c - a * b)
    out.append(('Lemma 2.3 sigma identity', [sp.expand(x - y) for x, y in zip(kk, M(P(h, mu * t), (0, 0, sig)))]))
    # Lemma 2.2 increment: central(x h^tau) - central(x) = tau c + C(tau,2) ab + x1 tau b
    x = (p1, p2, p3)
    out.append(('Lemma 2.2 increment', [sp.expand(M(x, P(h, tau))[2] - p3 - (tau * c + C(tau) * a * b + p1 * tau * b))]))
    # y k^-1 with y = g h^t z^s, k = h^tau z^sigma -> g h^{t-tau} z^{s-sigma}
    g = (p1, p2, p3); sg = sp.Symbol('sg')
    y = M(M(g, P(h, t)), (0, 0, s)); kinv = I(M(P(h, tau), (0, 0, sg)))
    rhs = M(M(g, P(h, t - tau)), (0, 0, s - sg))
    out.append(('y k^-1 = g h^{t-tau} z^{s-sigma}', [sp.expand(x - y_) for x, y_ in zip(M(y, kinv), rhs)]))
    # iota homomorphism
    v1, v2, t2, s2 = sp.symbols('v1 v2 t2 s2')
    io = lambda t_, s_: (t_ * v1, t_ * v2, s_ + C(t_) * v1 * v2)
    out.append(('iota homomorphism', [sp.expand(x - y_) for x, y_ in zip(M(io(t, s), io(t2, s2)), io(t + t2, s + s2))]))
    # k X3 = 2 c_k - k^2 a b, c_k = third coord of h^k
    ck = P(h, k)[2]
    out.append(('k*X3 = 2 c_k - k^2 ab', [sp.expand(k * (2 * c - a * b) - (2 * ck - k ** 2 * a * b))]))
    for name, diffs in out: print(f'  {name}: differences {diffs}')
    # Sec. 0 claim: |kc + C(k,2)ab| < 2^bb, |ka|,|kb| < 2^bb  =>  |c| < 2^bb + 2^(2bb-1).  Exhaustive small bb.
    for bb in (2, 3, 4):
        worst = None; worst_pos = None
        Bd = 1 << bb
        for kk_ in range(-Bd, Bd):
            if kk_ == 0: continue
            for aa in range(-Bd + 1, Bd):
                if abs(kk_ * aa) >= Bd: continue
                for bq in range(-Bd + 1, Bd):
                    if abs(kk_ * bq) >= Bd or (aa == 0 and bq == 0): continue
                    # all c with |k c + C(k,2) a b| < 2^bb
                    for ck_ in range(-Bd + 1, Bd):
                        num = ck_ - C2(kk_) * aa * bq
                        if num % kk_: continue
                        cc = num // kk_
                        X3 = 2 * cc - aa * bq
                        if worst is None or abs(cc) > worst[0]: worst = (abs(cc), (aa, bq, cc), kk_, X3)
                        if kk_ > 0 and (worst_pos is None or abs(cc) > worst_pos[0]): worst_pos = (abs(cc), (aa, bq, cc), kk_)
        print(f'  b={bb}: max |c| over all generators h^k = {worst[0]} at h={worst[1]}, k={worst[2]} '
              f'(claimed bound 2^b+2^(2b-1) = {Bd + (1 << (2 * bb - 1))}, promise 2^(2b+1) = {1 << (2 * bb + 1)}); '
              f'max over k>0: {worst_pos[0]}')
    # max |X3| (sign-symmetric in h^{+-1}) vs the bound 2^(2b+3) and the sharper 2^(2b)+2^(b+1)
    for bb in (2, 3, 4):
        Bd = 1 << bb; mx = 0
        for kk_ in range(-Bd, Bd):
            if kk_ == 0: continue
            for aa in range(-Bd + 1, Bd):
                if abs(kk_ * aa) >= Bd: continue
                for bq in range(-Bd + 1, Bd):
                    if abs(kk_ * bq) >= Bd or (aa == 0 and bq == 0): continue
                    for ck_ in range(-Bd + 1, Bd):
                        num = ck_ - C2(kk_) * aa * bq
                        if num % kk_: continue
                        mx = max(mx, abs(2 * (num // kk_) - aa * bq))
        print(f'  b={bb}: max |X3| = {mx}; 2^(2b)+2^(b+1) = {(1 << 2 * bb) + (1 << (bb + 1))}; proof bound 2^(2b+3) = {1 << (2 * bb + 3)}')

# ------------------------------------------------------------------ Part 2 / 3 helpers
def coset_from_point(y, h, P, R):
    """Physical coset gH cap D for the uniformly random point y of D = [-P,P)^2 x [-R,R).
    Returns g (= y h^{t_min}), list of t-offsets, list of elements, good flag."""
    w = (h[0], h[1])
    # all t with pi(y h^t) in the square (interval), then keep those with central coord in [-R,R)
    lo, hi = -10 ** 9, 10 ** 9
    for yi, wi in ((y[0], w[0]), (y[1], w[1])):
        if wi == 0: continue
        if wi > 0: l, u = -((yi + P) // wi), (P - 1 - yi) // wi
        else: l, u = -((P - 1 - yi) // (-wi)), (yi + P) // (-wi)
        lo, hi = max(lo, l), min(hi, u)
    elems = []; hp = pw(h, lo) if lo != 0 else (0, 0, 0)
    e = mul(y, hp)
    for t in range(lo, hi + 1):
        elems.append(e); e = mul(e, h)
    inD = [x for x in elems if -R <= x[2] < R]
    good = len(inD) == len(elems)
    return elems, inD, good

def physical_psi(h, P, R, N0, N, rng, want_good=True):
    """Explicit preparation: uniform y in D -> coset; QFT_N0 of central register; sample rho with its
    exact probability; return dict psi over group elements (p, r) and diagnostics."""
    while True:
        y = (rng.randrange(-P, P), rng.randrange(-P, P), rng.randrange(-R, R))
        elems, inD, good = coset_from_point(y, h, P, R)
        if good or not want_good: break
    L = len(inD)
    # state sum_t |pi_t>|c_t mod N0>/sqrt(L).  QFT_N0 |c> = N0^-1/2 sum_rho e(rho c/N0)|rho>.
    cs = np.array([x[2] % N0 for x in inD], dtype=np.int64)
    # amplitude of |pi_t, rho> = e(rho c_t/N0)/sqrt(L N0); P(rho) = sum_t 1/(L N0) because pi_t distinct
    pis = [(x[0], x[1]) for x in inD]
    assert len(set(pis)) == L
    rhos = np.arange(N0, dtype=np.int64)
    amp = np.exp(2j * np.pi * ((rhos[:, None] * cs[None, :]) % N0) / N0) / math.sqrt(L * N0)   # [rho, t]
    Prho = (np.abs(amp) ** 2).sum(axis=1)
    rho = int(rng.randrange(N0))
    chi = amp[rho] / np.linalg.norm(amp[rho])
    # chi_t / chi_0 must be e(theta (c_t - c_0))
    ph_ok = max(abs(chi[t] / chi[0] - cmath.exp(2j * math.pi * ((rho * (inD[t][2] - inD[0][2])) % N0) / N0)) for t in range(L))
    # psi(p_t, r) = chi_t * e(-theta r)/sqrt(N), r in [0,N)
    psi = {}
    for t in range(L):
        for r in range(N):
            psi[(pis[t][0], pis[t][1], r)] = chi[t] * cmath.exp(-2j * math.pi * ((rho * r) % N0) / N0) / math.sqrt(N)
    return dict(psi=psi, rho=rho, inD=inD, L=L, Prho_dev=float(np.abs(Prho - 1.0 / N0).max()), ph_err=ph_ok, good=good)

def gram_bruteforce(psi, k):
    """<psi | R_k psi> = sum_y conj psi(y) psi(y k^-1), lookups only."""
    ki = inv(k); acc = 0j
    for y, amp in psi.items():
        z = mul(y, ki)
        v = psi.get(z)
        if v is not None: acc += amp.conjugate() * v
    return acc

def lemma22(inD, h, rho, N0, N, tau, sigma):
    """Lemma 2.2 closed form: e(theta sigma) (|I|N)^-1 sum_{t, t-tau in I} (N-|delta_t|)_+,
    delta_t = sigma + tau c + C(tau,2) ab + p_{t-tau,1} tau b."""
    a, b, c = h; L = len(inD); acc = 0
    for t in range(L):
        if not (0 <= t - tau < L): continue
        dlt = sigma + tau * c + C2(tau) * a * b + inD[t - tau][0] * tau * b
        acc += max(0, N - abs(dlt))
    return cmath.exp(2j * math.pi * ((rho * sigma) % N0) / N0) * acc / (L * N), acc

def part2(seed=11):
    rng = random.Random(seed)
    cases = [(2, 3, 5), (0, 3, -4), (3, 0, 7), (4, 4, 1), (-3, 2, -9), (1, -1, 0), (2, 3, 3)]
    P, R, N0, N = 16, 512, 1 << 11, 200
    worst_gram = 0.0; worst_rho = 0.0; worst_ph = 0.0; worst_out = 0.0; bound_viol = 0; nk = 0
    for h in cases:
        st = physical_psi(h, P, R, N0, N, rng)
        worst_rho = max(worst_rho, st['Prho_dev']); worst_ph = max(worst_ph, st['ph_err'])
        psi = st['psi']; inD = st['inD']; L = st['L']; a, b, c = h; w = (a, b)
        for tau in (0, 1, -1, 2, -3, 5):
            for sigma in (0, 1, -7, 40, -150):
                k = mul(pw(h, tau), (0, 0, sigma))
                g_bf = gram_bruteforce(psi, k)
                g_cf, cnt = lemma22(inD, h, st['rho'], N0, N, tau, sigma)
                worst_gram = max(worst_gram, abs(g_bf - g_cf)); nk += 1
                # analytic 1 - A <= |tau|/|I| + max|delta|/N
                A = cnt / (L * N)
                md = max([abs(sigma + tau * c + C2(tau) * a * b + inD[t - tau][0] * tau * b)
                          for t in range(L) if 0 <= t - tau < L] or [0])
                if 1 - A > abs(tau) / L + md / N + 1e-12: bound_viol += 1
        for k in ((1, 0, 0), (0, 1, 0), (1, 1, 3), (w[1], -w[0], 0) if w != (0, 0) else (1, 0, 0)):
            if k[0] * w[1] - k[1] * w[0] == 0: continue      # k in K: skip
            worst_out = max(worst_out, abs(gram_bruteforce(psi, k)))
    print(f'  {len(cases)} h, P={P}, R={R}, N0={N0}, N={N}: max |P(rho)-1/N0| = {worst_rho:.2e}; '
          f'max chirp-phase error = {worst_ph:.2e}')
    print(f'  {nk} pairs (tau,sigma): max |brute-force Gram - Lemma 2.2| = {worst_gram:.2e}; '
          f'violations of 1-A <= |tau|/|I| + max|delta|/N: {bound_viol}')
    print(f'  k notin K: max |<psi|R_k psi>| = {worst_out:.2e}')
    # bad-coset frequency vs V/R and the V bound
    viol = 0; trials = 3000; bad = 0
    for _ in range(trials):
        h = (rng.randint(-7, 7), rng.randint(-7, 7), rng.randint(-200, 200))
        if h[:2] == (0, 0): continue
        bb = 3
        Pp = 1 << (2 * bb + 3); Rr = 50 * Pp * Pp
        y = (rng.randrange(-Pp, Pp), rng.randrange(-Pp, Pp), rng.randrange(-Rr, Rr))
        elems, inD, good = coset_from_point(y, h, Pp, Rr)
        spread = max(x[2] for x in elems) - min(x[2] for x in elems)
        V = 4 * Pp * Pp + (1 << (2 * bb + 3)) * Pp
        viol += spread > V; bad += not good
    print(f'  V bound (b=3, |a|,|b|<=7, |c|<=200 < 2^(2b+1), P=2^(2b+3)): {viol} violations of spread <= V in {trials}; '
          f'bad cosets {bad}/{trials} (bound V/R = {V / Rr:.4f})')

# ------------------------------------------------------------------ Part 3
def fejer(L, x):
    s = math.sin(math.pi * x)
    if abs(s) < 1e-13: return float(L * L)
    return (math.sin(math.pi * L * x) / s) ** 2

def lines_of_box(w, Mb):
    base = {}
    for u1 in range(Mb):
        for u2 in range(Mb):
            t = 0
            while 0 <= u1 - (t + 1) * w[0] < Mb and 0 <= u2 - (t + 1) * w[1] < Mb: t += 1
            base[(u1, u2)] = ((u1 - t * w[0], u2 - t * w[1]), t)
    return base

def part3(seed=5):
    rng = random.Random(seed)
    Mb = 4; P, N0 = 32, 1 << 20
    hs = [(1, 2, 3), (0, 1, 5), (1, 0, -4), (2, 2, 1), (0, 2, 3), (-1, 1, 7), (2, 1, 1)]
    print('| h | mu | Theta\' | |I_1|,|I_2| | N | TV(P,P*) | ||Phi-Phi*|| | sqrt(pointwise bound) | max cross-line |G| | sum P |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    allok = True
    for idx, h in enumerate(hs + [None]):
        nonprim = h is None
        if nonprim: h = (2, 2, 1)                  # control: non-primitive mu
        a, b, c = h; w = (a, b); X3 = 2 * c - a * b
        R = 4 * P * P + 64 * P                     # covers the central spread on the square for these h
        R = 1 << (R.bit_length())
        assert N0 >= 2 * R
        # mu primitive (or not, for the control); rho2 tuned so ||Theta|| ~ 2^-16
        mus = (2, 2) if nonprim else rng.choice([(1, 2), (2, -1), (1, -2), (2, 3), (3, -1)])
        rho1 = rng.randrange(N0)
        m1, m2 = mus
        # rho2 with rho1 m1^2 + rho2 m2^2 = small mod N0 (m2 odd needed for exact inverse; else nearest)
        if m2 % 2:
            rho2 = ((-rho1 * m1 * m1 + rng.randint(1, 30)) * pow(m2 * m2, -1, N0)) % N0
        else:
            rho2 = rng.randrange(N0)
        rhos = (rho1, rho2)
        Th = (rho1 * m1 * m1 + rho2 * m2 * m2) % N0; Thp = (Th if Th <= N0 // 2 else Th - N0) / N0
        A = sum(r * C2(m) for r, m in zip(rhos, mus)) % N0
        N = 1500
        facs = []
        for i in range(2):
            # physical prep but with prescribed rho (rho is exactly uniform and independent of the coset,
            # so fixing it is legitimate for a per-instance inequality check)
            while True:
                y = (rng.randrange(-P, P), rng.randrange(-P, P), rng.randrange(-R, R))
                elems, inD, good = coset_from_point(y, h, P, R)
                if good: break
            L = len(inD); rho = rhos[i]
            psi = {}
            for t in range(L):
                for r in range(N):
                    psi[(inD[t][0], inD[t][1], r)] = cmath.exp(2j * math.pi * ((rho * (inD[t][2] - r)) % N0) / N0) / math.sqrt(L * N)
            facs.append((psi, inD, L))
        us = [(u1, u2) for u1 in range(Mb) for u2 in range(Mb)]
        nU = len(us)
        G = np.ones((nU, nU), complex); Gi = [np.zeros((nU, nU), complex) for _ in range(2)]
        for i in range(2):
            psi = facs[i][0]; mu = mus[i]
            for x_ in range(nU):
                for y_ in range(nU):
                    u, up = us[x_], us[y_]
                    xu = (mu * u[0], mu * u[1], 0); xup = (mu * up[0], mu * up[1], 0)
                    Gi[i][x_, y_] = gram_bruteforce(psi, mul(xup, inv(xu)))
            G *= Gi[i]
        F = np.array([[cmath.exp(2j * math.pi * (y[0] * u[0] + y[1] * u[1]) / Mb) for y in us] for u in us])
        Pact = np.real(np.einsum('uy,uv,vy->y', F.conj(), G, F)) / Mb ** 4
        base = lines_of_box(w, Mb); lines = {}
        for u in us: lines.setdefault(base[u][0], []).append(base[u][1])
        Pid = np.array([sum(fejer(len(ts), (y[0] * w[0] + y[1] * w[1]) / Mb + A * X3 / N0) for ts in lines.values())
                        for y in us]) / Mb ** 4
        TV = 0.5 * np.abs(Pact - Pid).sum()
        iu = {u: j for j, u in enumerate(us)}
        dist2 = 0.0; bnd = 0.0
        for u in us:
            r, t = base[u]
            Gu = G[iu[r], iu[u]]
            dist2 += 2 - 2 * (cmath.exp(-2j * math.pi * ((A * t * X3) % N0) / N0) * Gu).real
            S = t * a * r[1] + C2(t) * a * b + t * c
            term = 4 * math.pi ** 2 * (Thp * S) ** 2
            for i in range(2):
                inD, L = facs[i][1], facs[i][2]; tau = mus[i] * t
                sig = -mus[i] ** 2 * S + C2(mus[i]) * t * X3
                md = max([abs(sig + tau * c + C2(tau) * a * b + inD[tt - tau][0] * tau * b)
                          for tt in range(L) if 0 <= tt - tau < L] or [0])
                term += 2 * (abs(tau) / L + md / N)
            bnd += term
        dist2 /= nU; bnd /= nU
        cross = max(abs(G[iu[u], iu[v]]) for u in us for v in us if base[u][0] != base[v][0])
        ok = TV <= math.sqrt(max(dist2, 0)) + 1e-9 and dist2 <= bnd + 1e-9
        if not nonprim:
            ok = ok and cross < 1e-12
            allok = allok and ok
        tag = ' (control: mu non-primitive)' if nonprim else ''
        print(f'| {h}{tag} | {mus} | {Thp:.2e} | {facs[0][2]},{facs[1][2]} | {N} | {TV:.4f} | {math.sqrt(max(dist2,0)):.4f} | '
              f'{math.sqrt(bnd):.4f} | {cross:.2e} | {Pact.sum():.6f} |', flush=True)
    print('ALL PRIMITIVE-MU INEQUALITIES HOLD' if allok else 'VIOLATION FOUND')

# ------------------------------------------------------------------ Part 4
def part4():
    lg = math.log2
    # no-wrap and the second Lemma D condition
    for n, B3exp in ((7, 3),):
        print(f'  stage-1 no-wrap 2^(2(n-1)) n gamma 2 B3 = 2^12*7*2^(-2b-19)*2^(2b+4) = {2**12*7*2.0**(-19+4):.4f} (independent of b)')
    # union terms, exact via logs, b = 1..400
    def union(b, n, Bs, gam_exp, F_exp, m=4):
        c = 2 ** n * math.sqrt(n)
        t1 = sum(lg(c * 2.0 ** e + 1) for e in Bs)
        t2 = m * lg(c * (2.0 ** gam_exp + 2.0 ** (Bs[0] + Bs[1] - F_exp)))
        return t1 + t2
    u1 = [(b, union(b, 7, [b, b, 2 * b + 3], -2 * b - 19, 3 * b + 26)) for b in range(1, 401)]
    u2 = [(b, union(b, 6, [b, 2 * b + 2], -2 * b - 21, 4 * b + 30)) for b in range(1, 401)]
    print(f'  stage-1 union term: max log2 = {max(x[1] for x in u1):.3f} at b={max(u1, key=lambda x: x[1])[0]}; '
          f'b=400: {u1[-1][1]:.3f}; first non-decrease at b = {[u1[i][0] for i in range(len(u1)-1) if u1[i][1] <= u1[i+1][1]][:3]}')
    print(f'  stage-2 union term: max log2 = {max(x[1] for x in u2):.3f} at b={max(u2, key=lambda x: x[1])[0]}; '
          f'b=400: {u2[-1][1]:.3f}; monotone decreasing: {all(u2[i][1] > u2[i+1][1] for i in range(len(u2)-1))}')
    print(f'  second Lemma D condition 2^(n-1) sqrt(n) gamma: stage 1 = {2**6*math.sqrt(7)*2.0**(-21):.2e} (b=1), '
          f'stage 2 = {2**5*math.sqrt(6)*2.0**(-23):.2e} (b=1)')
    # p_bad stage 2 from the C1(iii)-type bound with ell=(d,s0), |d|<2^b, |s0|<2^(2b+2), g<=2^b
    for b in (1, 2, 6, 10, 50):
        gF = 2.0 ** (2 * b + 9); s = 2.0 ** b + 2.0 ** (2 * b + 2)
        FF = 2.0 ** (4 * b + 30); g_ = 2.0 ** b
        pb = s / (2 * gF) + g_ / (2 * gF * FF) + g_ * s / (2 * gF * gF) + g_ * g_ / (2 * gF * gF * FF)
        pb1 = 2.0 ** -7 + 2.0 ** -14
        print(f'  b={b}: stage-2 p_bad <= {pb:.5f} (claimed 0.0044); stage-1 p_bad <= {pb1:.5f}; '
              f'P(correct v | ideal) >= {1 - 4 * pb1 - 2 ** max(x[1] for x in u1):.4f}; P(l^ ok) >= {1 - 4 * pb - 2 ** max(x[1] for x in u2):.4f}')
    # Lemma P' constants for K = 6b+67 (b = 1..200): RS (3.5)/(3.6) and RS Cor. 3 variants
    worst = (9, None); worst3 = (9, None)
    for b in range(1, 201):
        K = 6 * b + 67; Leps = 2 * (K + 1) * math.log(2)   # ln eps^-2, eps = 2^-(K+1)
        lnQ = math.log(2) + Leps + math.log(Leps)            # Q = 2 eps^-2 ln eps^-2 (ceil negligible)
        QlnQ_over = 2 * Leps / lnQ                           # (Q/ln Q) / eps^-2
        cRS = 2 / (1 + math.log(2) / lnQ) - 1.25506          # [pi(2Q)-pi(Q)] / (Q/lnQ) lower bound
        cRS3 = 0.6                                            # RS Cor. 3: pi(2x)-pi(x) > 3x/(5 ln x), x >= 20.5
        for cc, store in ((cRS, 'rs'), (cRS3, 'rs3')):
            S1 = cc * QlnQ_over * 2                           # times 2 eps^2 (1-o(1)) ; o(1) terms are 2^-100-ish
            ratio = 4 * (1 + 0.01 / 4) ** 2                   # 6Q/(eps^2 N0) <= 1/100 relative
            pz = 1 / (1 / S1 + ratio)
            if store == 'rs' and pz < worst[0]: worst = (pz, b, S1, cc)
            if store == 'rs3' and pz < worst3[0]: worst3 = (pz, b, S1)
    print(f'  Lemma P\': worst over b=1..200 with RS (3.5)/(3.6): P(Z>0) >= {worst[0]:.4f} (b={worst[1]}, S1 >= {worst[2]:.3f}, '
          f'prime-count constant {worst[3]:.4f}); with RS Cor. 3 (0.6): {worst3[0]:.4f} (S1 >= {worst3[2]:.3f})')
    # enumeration constant: 1.74 Q (2 sqrt3 eps)^2 / ln eps^-2 = 1.74*2*12 = 41.76
    print(f'  enumeration: 1.74*Q*(2 sqrt3 eps)^2 = {1.74*2*12:.2f} ln eps^-2 (claimed <= 42 ln eps^-2); '
          f'box/count constant check; after Markov cap: '
          f'{worst[0] - 0.05:.4f} (claimed 0.17); ratio (5.66x+1)/(x/3) <= 20 for x>=1, 6.66 for x<1 -> 20^3 = 8000 OK')
    # parameters and TV budget, b = 1..200 (common.params of the proof folder, read-only import)
    sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/2026-11-12-rees-h3z-cyclic-proof')
    from common import params
    bad = []; maxtv = 0; Bfit = []
    for b in range(1, 201):
        p = params(b); eta = 2.0 ** -10
        Mb, mu, P, N, R, N0, Q, K = p['Mb'], p['mu_max'], p['P'], p['N'], p['R'], p['N0'], p['Q'], p['K']
        eps_inv = 1 << (K + 1)
        conds = {
            'P>=19.2 mu Mb/eta^2': P * 10 >= 192 * mu * Mb * 2 ** 20,
            'P>=2^(2b+3)': P >= 1 << (2 * b + 3),
            'N>=16D/eta^2': N >= 16 * ((9 * mu * mu * Mb * Mb) // 2 + 2 * P * mu * Mb) * 2 ** 20,
            'R>=10P^2/eta': R >= 10 * P * P * 2 ** 10,
            'N0>=2R': N0 >= 2 * R,
            'N0>=600Q/eps^2': N0 >= 600 * Q * eps_inv ** 2,
            'Mb|N0': N0 % Mb == 0,
            'Mb>=2^(2b+3)': Mb >= 1 << (2 * b + 3),
            'mu_max^2>=4Q/sqrt3': mu * mu * 17320508 >= 4 * Q * 10 ** 7,
            'Q>=2^100': Q >= 1 << 100,
            'Q>=2eps^-2 ln eps^-2': Q * 10 ** 9 >= 2 * eps_inv ** 2 * int(2 * (K + 1) * math.log(2) * 10 ** 9),
            'B>=bits(R)': p['B'] >= R.bit_length() + 1,
            'B>=stage2 box': p['B'] >= 10 * b + 62,
        }
        for k_, v_ in conds.items():
            if not v_: bad.append((b, k_))
        phase = 4 * math.pi ** 2 * (2.5 * 2.0 ** (2 * p['logMb'] - K)) ** 2
        trunc = 4 * (1.2 * Fraction(mu * Mb, P) + Fraction((9 * mu * mu * Mb * Mb) // 2 + 2 * P * mu * Mb, N))
        trunc = float(trunc)
        tv = math.sqrt(phase + trunc) + float(Fraction(10 * P * P, R))
        maxtv = max(maxtv, tv / eta)
        Bfit.append((b, p['B']))
    print(f'  parameter inequalities b=1..200: {len(bad)} failures {bad[:5]}; max TV/eta_s = {maxtv:.4f} (must be <= 2)')
    print(f'  B(b): ' + ', '.join(f'{b}:{B}' for b, B in Bfit if b in (1, 6, 10, 50, 100, 200)) +
          f'; B(200)-B(100) = {Bfit[199][1] - Bfit[99][1]} (linear slope ~18-20/b)')
    # E[1/|I|] geometry: (#lines meeting the square) / (4P^2) vs 1.1 |w|_inf / P, adversarial w
    P_ = 256
    pts = np.array([(x, y) for x in range(-P_, P_) for y in range(-P_, P_)], dtype=np.int64)
    worst_r = 0
    for w in ((1, 255), (255, 255), (255, 254), (0, 1), (1, 0), (128, 128), (0, 128), (3, -2), (100, -37)):
        a, b = w; d = math.gcd(a, b)
        key = (pts[:, 0] * b - pts[:, 1] * a)            # omega value; plus the Z_d class
        if d > 1:
            # class of p in Z^2/Zw: (omega, coordinate mod d along w/d direction) -- count via canonical rep
            v = (a // d, b // d)
            # p = s v + q v_perp-ish; class determined by omega and floor-shift; use exact canonical form:
            # shift p by multiples of w until first coordinate of projection on v lies in [0, d*|v|^2)
            proj = pts[:, 0] * v[0] + pts[:, 1] * v[1]
            nv = v[0] ** 2 + v[1] ** 2
            # p + j w changes proj by j d nv; canonical j index = floor(proj / (d nv)); class = (omega, proj mod d nv) is
            # too fine; distinct classes = distinct (omega, (proj mod d*nv)//nv) pairs  [since omega fixes p mod Zv]
            cls = key * (d + 1) + ((proj % (d * nv)) // nv)
            nlines = len(np.unique(cls))
        else:
            nlines = len(np.unique(key))
        ratio = nlines / (4 * P_ * P_) / (max(abs(a), abs(b)) / P_)
        worst_r = max(worst_r, ratio)
        print(f'  w={w}: #lines meeting [-P,P)^2 (P={P_}) = {nlines}; (#lines/4P^2)/(|w|_inf/P) = {ratio:.4f} (proof uses <= 1.1/(1+V/R) slack)')

# ------------------------------------------------------------------ Part 5: adversarial decoding
def decode_lemmaD(samples, Bexp, Den, F, log_gamma, dX):
    """Independent re-implementation of Lemma D (fpylll LLL): rows (omega_j e_j | c_kj), (0 | Den e_k)."""
    from fpylll import IntegerMatrix, LLL
    m = len(samples); n = dX + m
    gD = Den >> (-log_gamma)
    om = [gD >> e for e in Bexp]
    rows = []
    for j in range(dX):
        r = [0] * n; r[j] = om[j]
        for k, (y, A) in enumerate(samples):
            r[dX + k] = (y[j] * (Den // F)) if j < 2 else A
        rows.append(r)
    for k in range(m):
        r = [0] * n; r[dX + k] = Den; rows.append(r)
    M = IntegerMatrix.from_matrix(rows); LLL.reduction(M)
    for i in range(min(2, n)):
        vec = [int(M[i, j]) for j in range(n)]
        Xp = [vec[j] // om[j] for j in range(dX)]
        assert all(vec[j] % om[j] == 0 for j in range(dX))
        if Xp[0] or Xp[1]:
            g = math.gcd(Xp[0], Xp[1]); v = (Xp[0] // g, Xp[1] // g)
            return v if (v[0] > 0 or (v[0] == 0 and v[1] > 0)) else (-v[0], -v[1])
    return None

def part5(trials=20, seed=99, bs=(6, 10)):
    sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/2026-11-12-rees-h3z-cyclic-proof')
    import common as cm
    rng = random.Random(seed)
    # exact self-test of the proof's sampler at large fiber gcd (adversarial w), Mb = 64
    Mb, N0 = 64, 1 << 20
    for w, X3, A in (((16, 48), 5, 777), ((0, 32), 3, 12345), ((32, 0), -7, 99991), ((63, 62), 11, 4321)):
        base = lines_of_box(w, Mb); lines = {}
        for u in base: lines.setdefault(base[u][0], []).append(base[u][1])
        ys = [(y1, y2) for y1 in range(Mb) for y2 in range(Mb)]
        ex = np.array([sum(fejer(len(ts), (y[0] * w[0] + y[1] * w[1]) / Mb + A * X3 / N0) for ts in lines.values()) for y in ys]) / Mb ** 4
        S = 30000; cnt = {}
        for _ in range(S):
            y = cm.sample_ideal(rng, w, X3, A, N0, Mb); cnt[y] = cnt.get(y, 0) + 1
        emp = np.array([cnt.get(y, 0) / S for y in ys])
        draw = rng.choices(range(len(ys)), weights=ex.tolist(), k=S); c2 = np.bincount(draw, minlength=len(ys)) / S
        print(f'  sampler self-test w={w}: sum P* = {ex.sum():.6f}; TV(emp, exact) = {0.5*np.abs(emp-ex).sum():.4f}; '
              f'null TV = {0.5*np.abs(c2-ex).sum():.4f}')
    for b in bs:
        p = cm.params(b)
        N0, Mb, K = p['N0'], p['Mb'], p['K']
        Bb = 1 << b
        hs = {
            'big |a|,|b|, c=1': (Bb - 1, Bb - 1, 1),
            'v=(2^b-1, -(2^b-2)) huge primitive': (Bb - 1, -(Bb - 2), 3),
            'a=0, b=1': (0, 1, 0),
            'a=1, b=0': (1, 0, 0),
            'a=0, b=2^b-1, c=-(2^b-1)': (0, Bb - 1, -(Bb - 1)),
            'w=2^(b-1)(1,1): fiber gcd 2^(b-1)': (Bb // 2, Bb // 2, 7),
            'w=(0,2^(b-1)): fiber gcd 2^(b-1)': (0, Bb // 2, 5),
            'w=(3,1)*2^(b-2)': (3 * (Bb // 4), Bb // 4, -11),
            'max |X3|: h^-1 small, h=(a,b,ab-c\')': (Bb - 1, Bb - 1, (Bb - 1) ** 2 + (Bb - 1)),
            'X3=0 with large c': (Bb - 2, Bb - 1, (Bb - 2) * (Bb - 1) // 2),
            'at the note bound |c|<2^(2b+1) (outside the true promise)': (-(Bb - 1), Bb - 1, -((1 << (2 * b + 1)) - 1)),
            'beyond promise: c = 2^(2b+1)+2^(2b) (X3 ~ 2^(2b+2.6))': (Bb - 1, -(Bb - 1), (1 << (2 * b + 1)) + (1 << 2 * b)),
        }
        print(f'\n  b={b} (log2 Mb={p["logMb"]}, K={K}, log2 N0={p["n0"]}); {trials} trials per (h, alpha-mode); '
              f'counts = correct direction from 4 samples (proof decoder / independent decoder)')
        print('| h | X3 bits | alpha from SDA | alpha=0 | alpha=1/2 | alpha=1/N0 | alpha uniform | disagreements |')
        print('|---|---|---|---|---|---|---|---|')
        for name, h in hs.items():
            a, bq, c = h; w = (a, bq); X3 = 2 * c - a * bq
            vt = cm.prim(w); vt = vt if (vt[0] > 0 or (vt[0] == 0 and vt[1] > 0)) else (-vt[0], -vt[1])
            row = []; dis = 0
            for mode in ('sda', 'zero', 'half', 'one', 'unif'):
                ok1 = ok2 = 0
                for _ in range(trials):
                    samples = []
                    for _k in range(4):
                        if mode == 'sda':
                            while True:
                                rho = [rng.randrange(N0), rng.randrange(N0)]
                                r = cm.sda_iso_full(rho, N0, p['logeps'], p['Q'])
                                if r[0] is not None: break
                            mu = r[:2]
                            assert math.gcd(mu[0], mu[1]) == 1
                            A = sum(rr * C2(m) for rr, m in zip(rho, mu)) % N0
                        elif mode == 'zero': A = 0
                        elif mode == 'half': A = N0 // 2
                        elif mode == 'one': A = 1
                        else: A = rng.randrange(N0)
                        y = cm.sample_ideal(rng, w, X3, A, N0, Mb)
                        samples.append((y, A))
                    v1, _ = cm.decode_stage1(samples, b, N0, Mb, p['log_gamma1'])
                    if v1 is not None: v1 = v1 if (v1[0] > 0 or (v1[0] == 0 and v1[1] > 0)) else (-v1[0], -v1[1])
                    v2 = decode_lemmaD(samples, [b, b, 2 * b + 3], N0, Mb, p['log_gamma1'], 3)
                    ok1 += v1 == vt; ok2 += v2 == vt; dis += v1 != v2
                row.append(f'{ok1}/{ok2}')
            print(f'| {name} {h} | {abs(X3).bit_length()} | ' + ' | '.join(row) + f' | {dis} |', flush=True)
        # stage 2 adversarial: ell = (d, s0) extremes, Lemma D d_X = 2 on the exact abelian law
        FA = p['FA']; ok = 0; tot = 0; dis = 0
        ells = [(Bb - 1, (1 << (2 * b + 2)) - 1), (1, -((1 << (2 * b + 2)) - 1)), (Bb // 2, Bb // 2 * 3), (1, 0), (Bb - 1, 0), (2, 1)]
        for ell in ells:
            for _ in range(trials):
                ys = [cm.sample_ideal(rng, ell, 0, 0, 1, FA) for _ in range(4)]
                lh = cm.decode_stage2(ys, [Bb, 1 << (2 * b + 2)], FA, p['log_gamma2'])
                l2 = decode_lemmaD([(y, 0) for y in ys], [b, 2 * b + 2], FA, FA, p['log_gamma2'], 2)
                tv_ = cm.prim(ell); tv_ = tv_ if (tv_[0] > 0 or (tv_[0] == 0 and tv_[1] > 0)) else (-tv_[0], -tv_[1])
                if lh is not None: lh = lh if (lh[0] > 0 or (lh[0] == 0 and lh[1] > 0)) else (-lh[0], -lh[1])
                ok += lh == tv_; tot += 1; dis += lh != l2
        print(f'  stage 2 (d_X=2), extreme ell {ells}: {ok}/{tot} correct (independent decoder disagreements: {dis})')

if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else '1'
    args = [int(x) for x in sys.argv[2:]]
    {'1': part1, '2': part2, '3': part3, '4': part4, '5': part5}[part](*args)

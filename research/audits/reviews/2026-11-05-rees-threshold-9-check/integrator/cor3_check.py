"""Integrator's independent re-check of Corollary 3 (report 2026-11-05-rees-threshold-9.md, Sec. 2.3)
and of Remark 5 step 1 / step 4.  Written from the proof text, not from verify_corollary.py.

Usage:  python cor3_check.py conditions KMAX     (ranges (A),(B),(C) for L0 in {6, 5.5}, kappa <= KMAX, mpmath)
        python cor3_check.py star                (direct evaluation of (*) and of the exact (C) quantity at kappa = 729, 1677)
        python cor3_check.py barrier             (Remark 5 step 1 and step 4 at p <= kappa^kappa/2)
All arithmetic in mpmath (dps 30 for the conditions, 60 elsewhere); logs natural.
"""
import sys
import mpmath as mp
from mpmath import mpf, log, exp, sqrt, ceil, binomial, factorial

def conds(k, L0):
    """Return slacks (sA, sB, sC); a condition holds (strictly) iff its slack > 0.
    The slack is in natural-log units for (A) and (B) (how much the needed inequality holds by),
    and 1 - G for (C).  Side conditions are folded in (slack = -inf if violated)."""
    k = mpf(k); lk = log(k)
    c0 = L0 * exp(-L0)
    cmain = 1 / (1 - exp(-L0))
    # (A): needed: ln(delta) + 2 R Lambda < -cmain*mu - ln 3, with
    #   delta <= 3.1 k Kbar k^Kbar / k^(k/2), 2 R Lambda <= 8 c0 k + 10 (ln k + 1.5), mu <= k e^-L0
    if lk + mpf('1.5') > L0:
        KA = 16 * c0 * k + 20 * (lk + mpf('1.5')) + 1
        if KA > k / 2:
            sA = -mp.inf
        else:
            lhs = (k / 2 - KA) * lk
            rhs = log(mpf('3.1') * k * KA) + 8 * c0 * k + 10 * (lk + mpf('1.5')) + cmain * k * exp(-L0) + log(3)
            sA = lhs - rhs
    else:
        sA = mp.inf  # range (A) empty
    # (B): needed: k*delta*e^Lambda <= 0.5/e (so that F > 1 - 2 e^-1.5 - 0.19 > 0) with Lambda <= sqrt(8k)
    Lm = sqrt(8 * k)
    KB = mpf('3.6') * Lm + 1
    if KB > k:
        sB = -mp.inf
    else:
        val = log(mpf('3.1')) + 2 * lk + log(KB) + (KB - k / 2) * lk + Lm
        sB = log(mpf('0.5') / mp.e) - val
    # (C): TH2 Theorem 5, m = 2, at lambda = sqrt(8k), p = sqrt(8k) k^k (worst point of the range)
    p = Lm * k ** k
    eps = 8 * k ** 4 / sqrt(p)
    if (k - 1) * eps > 1:
        sC = -mp.inf
    else:
        W2 = 16 + 24 / Lm + 11 / Lm ** 2 + 1 / Lm ** 3
        d = 2 * (k - 1) * (eps + 4 / p)
        G = k * (3 / Lm ** 2 + 1 / Lm ** 3) + k * W2 * d
        sC = 1 - G
    return sA, sB, sC

def run_conditions(KMAX):
    mp.mp.dps = 30
    for L0 in (mpf(6), mpf('5.5')):
        last = {'A': None, 'B': None, 'C': None}
        last_m1 = None   # last failure with a margin of 1 (as in verify_corollary.py)
        minslack = [mp.inf, mp.inf, mp.inf]; minslack_at = [None] * 3
        cut = 729 if L0 == 6 else 1677
        for k in range(30, KMAX + 1):
            s = conds(k, L0)
            for i, nm in enumerate('ABC'):
                if not s[i] > 0:
                    last[nm] = k
            if not (s[0] >= 1 and s[1] >= 1 and s[2] > mpf('0.1')):
                last_m1 = k
            if k >= cut:
                for i in range(3):
                    if s[i] < minslack[i]:
                        minslack[i] = s[i]; minslack_at[i] = k
        print(f"L0={L0}: kappa in [30,{KMAX}]: last strict failure A={last['A']} B={last['B']} C={last['C']};"
              f" last failure with margin (1,1,0.1)={last_m1}")
        print(f"   min slack for kappa>={cut}: A={mp.nstr(minslack[0],6)}@{minslack_at[0]}"
              f" B={mp.nstr(minslack[1],6)}@{minslack_at[1]} C={mp.nstr(minslack[2],6)}@{minslack_at[2]}")
    # tail sample beyond KMAX
    for L0 in (mpf(6), mpf('5.5')):
        out = []
        for e in range(6, 16):
            for k in (10 ** e, 3 * 10 ** e):
                s = conds(k, L0)
                out.append(all(x > 1 for x in s[:2]) and s[2] > mpf('0.1'))
        print(f"L0={L0}: tail sample kappa = 1e6..3e15 all hold: {all(out)}")
    # constants quoted in the proof
    mp.mp.dps = 30
    for L0 in (mpf(6), mpf('5.5'), mpf(5)):
        c0 = L0 * exp(-L0)
        sec = 4 * log(mp.e / 4) + 1   # coefficient of Lambda in the second error, per R
        print(f"L0={L0}: c_main={mp.nstr(1/(1-exp(-L0)),6)} 16c0={mp.nstr(16*c0,6)}"
              f" second-error exponent/R at Lambda=L0: {mp.nstr(sec*L0 + 1 - log(4),6)}"
              f" (sec coef {mp.nstr(sec,6)}, const {mp.nstr(1-log(4),6)});"
              f" first error vs main: ln3 - 4*ln(4/e) = {mp.nstr(log(3) - 4*log(4/mp.e),6)} (<0 needed)")
    print("(B) item 2: 3.6*ln(3.6/e) =", mp.nstr(mpf('3.6') * log(mpf('3.6') / mp.e), 6), "(>= 1 needed)")
    print("(B) total: 1 - 2e^-1.5 - 0.5/e =", mp.nstr(1 - 2 * exp(mpf('-1.5')) - mpf('0.5') / mp.e, 6))
    print("(C) 16c0 at L0=6: K_A <= 0.2383k tail:", mp.nstr(16 * 6 * exp(-6), 8))

def Ekm(k, m, p):
    return (m - 1 - mpf(m) / k + mpf(k) ** (-m)) * sqrt(p) + mpf(m) / k - m * mpf(k) ** (-m)

def eta(k, m, p):
    return mpf(k) ** m * Ekm(k, m, p) / (p - m)

def star(k, L, L0):
    """Lower bound (*) of the proof, with R, K as in ranges (A)/(B), evaluated exactly (mpmath)."""
    k = int(k)
    lk = log(k)
    u = exp(-L); mu = k * u
    p = L * mpf(k) ** k + 1
    if L < lk + mpf('1.5'):
        R = 2 * int(ceil(2 * mu + 2)) - 1
        K = int(ceil(4 * R * L))
    else:
        R = 1
        K = int(ceil(mpf('3.6') * L))
    assert R <= k and R * L <= K <= k
    delta = mpf('3.1') * k * K * mpf(k) ** K / sqrt(p)
    side = (k - 1) * eta(k, K, p)
    assert side <= 1, side
    t0 = (1 - u) ** k - binomial(k, R + 1) * u ** (R + 1)
    t1 = mp.fsum(binomial(k, r) * (mp.e * r * L / K) ** K for r in range(1, R + 1))
    t2 = delta * mp.fsum(binomial(k, r) * exp(r * L) for r in range(1, R + 1))
    return t0 - t1 - t2, R, K, delta

def G2_exact(k, p):
    """TH2 Theorem 5, m = 2, with TH2's own delta_k (not the closed-form bound)."""
    lam = (p - 1) / mpf(k) ** k
    A4 = lam + 3 * lam ** 2
    W2 = 16 + 24 / lam + 11 / lam ** 2 + 1 / lam ** 3
    dmax = mpf(0)
    for kk in range(1, 5):
        e = mpf(k) ** kk * Ekm(k, kk, p) / (p - kk)
        if e >= 1:
            return mp.inf
        d = max((1 + e) ** (k - 1) - 1, 1 - ((1 - mpf(kk) / p) * (1 - e)) ** (k - 1))
        dmax = max(dmax, d)
    return k * (A4 / lam ** 4 + W2 * dmax)

def run_star():
    mp.mp.dps = 60
    for k, L0 in ((729, mpf(6)), (1677, mpf('5.5'))):
        lo = mpf(L0); hi = sqrt(8 * mpf(k))
        worst = None
        n = 0
        L = lo
        while L <= hi:
            v, R, K, d = star(k, L, L0)
            n += 1
            if worst is None or v < worst[0]:
                worst = (v, L, R, K)
            L += mpf('0.01')
        print(f"kappa={k}: (*) on Lambda in [{L0}, sqrt(8k)={mp.nstr(hi,6)}] step 0.01, {n} points:"
              f" min={mp.nstr(worst[0],6)} at Lambda={mp.nstr(worst[1],5)} (R={worst[2]}, K={worst[3]})")
        # (C): G_2 with TH2's exact delta_k at the left end and above
        for fac in (1, 2, 10, 1000):
            p = fac * hi * mpf(k) ** k + 1
            print(f"   G_2 exact at p = {fac}*sqrt(8k)k^k+1: {mp.nstr(G2_exact(k, p), 8)}")

def run_barrier():
    mp.mp.dps = 60
    # step 1: eta_{k-1} >= 1 at p = k^k/2 (eta_m decreasing in p, so this is the worst p <= k^k/2)
    worst = None
    for k in range(3, 401):
        p = mpf(k) ** k / 2
        e = eta(k, k - 1, p)
        if worst is None or e < worst[0]:
            worst = (e, k)
    print(f"Remark 5 step 1: min over 3<=k<=400 of eta_(k-1) at p=k^k/2: {mp.nstr(worst[0],6)} at k={worst[1]}")
    # monotonicity of eta_m in m, k = 3..60, p in {k^k/2, 10 k^k}
    bad = 0
    for k in range(3, 61):
        for p in (mpf(k) ** k / 2, 10 * mpf(k) ** k):
            prev = mpf(0)
            for m in range(1, k + 1):
                e = eta(k, m, p)
                if e < prev:
                    bad += 1
                prev = e
    print(f"eta_m nondecreasing in m (3<=k<=60, two p each): violations={bad}")
    # step 4 (i),(ii) for every a,b>=1 with eta_{a+b} < 1, k = 3..40, several p <= k^k/2 (and real p >= 7)
    cnt = 0; fails = 0; maxratio = mpf(0)
    for k in range(3, 41):
        top = mpf(k) ** k / 2
        ps = [p for p in (mpf(7), mpf(31), mpf(1009), top / 1000, top / 10, top) if 7 <= p <= top]
        for p in ps:
            def rho(m):
                return (p - m) / (p * mpf(k) ** m)
            for m in range(2, k + 1):
                em = eta(k, m, p)
                if not em < 1:
                    break
                for a in range(1, m):
                    b = m - a
                    ea, eb = eta(k, a, p), eta(k, b, p)
                    lo_ok = rho(a) * rho(b) * (1 - ea) * (1 - eb) >= rho(m) * (1 - em)
                    hi_ok = rho(a) * rho(b) * (1 + ea) * (1 + eb) <= rho(m) * (1 + em)
                    r = (rho(a) * rho(b) * (1 + ea) * (1 + eb) / rho(m) - 1) / em
                    maxratio = max(maxratio, r)
                    cnt += 1
                    if not (lo_ok and hi_ok):
                        fails += 1
    print(f"Remark 5 step 4 (i),(ii): {cnt} pairs (3<=k<=40), failures={fails}; "
          f"max of (rho_a rho_b (1+eta_a)(1+eta_b)/rho_m - 1)/eta_m = {mp.nstr(maxratio,6)} (proof: <= 0.4)")

if __name__ == '__main__':
    if sys.argv[1] == 'conditions':
        run_conditions(int(sys.argv[2]))
    elif sys.argv[1] == 'star':
        run_star()
    elif sys.argv[1] == 'barrier':
        run_barrier()

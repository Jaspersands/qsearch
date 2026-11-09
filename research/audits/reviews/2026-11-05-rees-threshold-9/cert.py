"""Joint-moment Bonferroni certificate for the two-level contraction (threshold-9, Theorem 1).

Setting (appendix-schedule2.tex, subsection app:s2-TA): y_0 = 0, y_1..y_{k-1} uniform on F_p,
X_j(y) = {x : x + y_i in Q_{-(i+j)} for all i}, n_j = |X_j(y)|.  For S a set of r columns,
M_S = sum_{j in S} n_j, and {M_S = 0} = {n_j = 0 for all j in S}.

Theorem 1.  With u_m(r) >= E C(M_S, m) >= l_m(r) (Lemma 2 below),
    F = 1 + sum_{r even, 2 <= r < R} C(k,r) L_r  -  sum_{r odd, r <= R} C(k,r) U_r  > 0
(R odd, L_r = sum_{m <= K_r} [m even] l_m - [m odd] u_m with K_r odd,
        U_r = sum_{m <= K_r} [m even] u_m - [m odd] l_m with K_r even)
implies that some y has every X_j(y) nonempty, so p is not in E_2(k).

Lemma 2.  E C(M_S, m) = sum over m-subsets T of D_S = union_{j in S} Q_{-j} of
prod_{i=1}^{k-1} N_i(T)/p, and |N_i(T) - (p-m)/k^m| <= E_k(m,p) (lem:app-s2-weil-count).

Usage:
    python cert.py point k Lambda            # F at p = Lambda*k^k + 1 (real p), best R, K_r
    python cert.py table _ _ k1,k2,...       # pointwise window on a 1% grid (argv[2], argv[3] unused)
    python cert.py interval k L1 L2 steps    # rigorous interval cover of p in [L1 k^k+1, L2 k^k+1]
"""
import sys
import mpmath as mp

mp.mp.dps = 120  # raised in __main__ for large k


def Ek(k, m, p):
    """Exact error of lem:app-s2-weil-count, closed form; 0 for m <= 1."""
    if m <= 1:
        return mp.mpf(0)
    k = mp.mpf(k)
    return (m - 1 - m / k + k ** (-m)) * mp.sqrt(p) + m / k - m * k ** (-m)


def eta(k, m, p):
    return mp.mpf(k) ** m * Ek(k, m, p) / (p - m)


def gbinom(x, m):
    """x(x-1)...(x-m+1)/m!, increasing in x for x >= m-1."""
    out = mp.mpf(1)
    for t in range(m):
        out *= (x - t)
    return out / mp.factorial(m)


def prepare(k, p_lo, p_hi, mcap):
    """Per-m data valid on [p_lo, p_hi]: lists of (eta_m at p_lo, rho_lo^(k-1), rho_hi^(k-1))."""
    data = []
    K = mp.mpf(k)
    for m in range(0, mcap + 1):
        e = eta(k, m, p_lo)                # eta decreasing in p
        if e >= 1:
            break
        rlo = ((p_lo - m) / (p_lo * K ** m)) ** (k - 1)   # rho increasing in p
        rhi = ((p_hi - m) / (p_hi * K ** m)) ** (k - 1)
        data.append((e, rlo, rhi))
    return data


def best_LU(k, r, p_lo, p_hi, data):
    """Best L_r (r even, K odd) or U_r (r odd, K even) over admissible K.
    l_m = binom(r h_lo, m) rho_lo^(k-1) (1-eta)^(k-1) <= E C(M_S,m) <= u_m = binom(r h_hi, m) rho_hi^(k-1) (1+eta)^(k-1)."""
    want_lower = (r % 2 == 0)
    xlo = r * (p_lo - 1) / k
    xhi = r * (p_hi - 1) / k
    blo = mp.mpf(1); bhi = mp.mpf(1)
    best = None; bestK = None
    acc = mp.mpf(0)
    for m, (e, rlo, rhi) in enumerate(data):
        if m > 0:
            if xlo < m - 1:
                break
            blo = blo * (xlo - (m - 1)) / m
            bhi = bhi * (xhi - (m - 1)) / m
        if m == 0:
            l = u = mp.mpf(1)
        else:
            u = bhi * rhi * (1 + e) ** (k - 1)
            l = blo * rlo * (1 - e) ** (k - 1)
        if want_lower:
            acc += l if m % 2 == 0 else -u
            if m % 2 == 1 and (best is None or acc > best):
                best, bestK = acc, m
        else:
            acc += u if m % 2 == 0 else -l
            if m % 2 == 0 and (best is None or acc < best):
                best, bestK = acc, m
    if want_lower:
        best = mp.mpf(0) if best is None else max(best, mp.mpf(0))   # P >= 0 is also a lower bound
    else:
        best = mp.mpf(1) if best is None else min(best, mp.mpf(1))   # P <= 1 is also an upper bound
    return best, bestK


def bestF(k, p_lo, p_hi, Rmax=None):
    """max over odd R of F_R = 1 + sum_{r<=R} (-1)^r C(k,r) [L_r or U_r]."""
    if Rmax is None:
        Rmax = k if k % 2 == 1 else k - 1
    data = prepare(k, p_lo, p_hi, 4 * k)
    Km = len(data) - 1
    tot = mp.mpf(1)
    best = None
    Ks = {}
    for r in range(1, Rmax + 1):
        v, K = best_LU(k, r, p_lo, p_hi, data)
        Ks[r] = K
        c = mp.binomial(k, r)
        tot += c * v if r % 2 == 0 else -c * v
        if r % 2 == 1:
            if best is None or tot > best[0]:
                best = (tot, r, dict(Ks), Km)
            elif r > best[1] + 40:
                break
    return best


def point(k, Lam):
    p = mp.mpf(Lam) * mp.mpf(k) ** k + 1
    return bestF(k, p, p)


def lam_star(k, lo=0.05, hi=None):
    """Smallest Lambda (bisection, pointwise) with F > 0; assumes one crossing."""
    if hi is None:
        hi = 4.0 * k
    f = lambda L: point(k, L)[0] > 0
    if not f(hi):
        return None
    for _ in range(40):
        mid = (lo + hi) / 2
        if f(mid):
            hi = mid
        else:
            lo = mid
    return hi


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "point":
        k = int(sys.argv[2]); L = float(sys.argv[3])
        val, R, Ks, Km = point(k, L)
        print(f"k={k} Lambda={L} F={mp.nstr(val, 8)} R={R} Kmax={Km} K_r={Ks}")
    elif cmd == "table":
        # pointwise window: first Lambda on a 1%-geometric grid with F > 0, and the end of that window
        ks = [int(x) for x in sys.argv[4].split(",")]
        for k in ks:
            mp.mp.dps = 60 + k
            L = mp.mpf("0.5"); first = None; last = None; info = None
            while L <= 4 * k:
                val, R, Ks, Km = point(k, L)
                if val > 0:
                    if first is None:
                        first = L; info = (R, Ks, Km)
                    last = L
                elif first is not None:
                    break
                L *= mp.mpf("1.01")
            if first is None:
                print(f"k={k} no Lambda in [0.5, {4*k}] certified", flush=True); continue
            R, Ks, Km = info
            mu = k * mp.e ** (-first)
            print(f"k={k} window Lambda in [{mp.nstr(first,5)}, {mp.nstr(last,5)}] R={R} Kmax={Km} "
                  f"mu={mp.nstr(mu,4)} ln k={float(mp.log(k)):.3f} K_r={Ks}", flush=True)
    elif cmd == "interval":
        k = int(sys.argv[2]); L1 = mp.mpf(sys.argv[3]); L2 = mp.mpf(sys.argv[4]); steps = int(sys.argv[5])
        kk = mp.mpf(k) ** k
        ratio = (L2 / L1) ** (mp.mpf(1) / steps)
        L = L1
        worst = None
        for s in range(steps):
            Ln = L * ratio
            val, R, Ks, Km = bestF(k, L * kk + 1, Ln * kk + 1)
            if worst is None or val < worst[0]:
                worst = (val, L, Ln, R)
            if val <= 0:
                print(f"FAIL k={k} interval Lambda in [{mp.nstr(L,8)}, {mp.nstr(Ln,8)}] F={mp.nstr(val,6)}")
                break
            L = Ln
        else:
            print(f"OK k={k} Lambda in [{mp.nstr(L1,8)}, {mp.nstr(L2,8)}] steps={steps} "
                  f"min F={mp.nstr(worst[0],6)} at [{mp.nstr(worst[1],6)},{mp.nstr(worst[2],6)}] R={worst[3]}")

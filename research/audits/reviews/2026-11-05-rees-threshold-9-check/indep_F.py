"""Independent referee implementation of Theorem 1 (threshold-9 report), written from the
report's statement, not from cert.py.  E_kappa(m,p) is taken from the *sum* form of
lem:app-s2-weil-count (not the closed form), binomials via mpmath's gamma-based binomial,
every odd R scanned (no early stop).

Usage: python indep_F.py compare            # vs cert.point at k=100,200
       python indep_F.py literal            # 'literal' Theorem 1 (no eta<1 for r odd) on E_2 members
       python indep_F.py star               # (star) bound and true F at k=729
       python indep_F.py o2small            # Remark 5 two-part inequalities, k=3..7, all primes p<=k^k/2
       python indep_F.py consts             # numeric constants of Corollary 3
"""
import sys, math, glob, re
import mpmath as mp

HERE = "/Users/jaspersands/Developer/qsearch/research/audits/reviews/"


def E_sum(k, l, p):
    if l == 0:
        return mp.mpf(0)
    k = mp.mpf(k); sp = mp.sqrt(p)
    return k ** (-l) * mp.fsum(mp.binomial(l, s) * (k - 1) ** s * ((s - 1) * sp + (l - s)) for s in range(1, l + 1))


def brackets(k, p, mcap, enforce_eta=True):
    """list over m of (eta, rho^(k-1)); stops at first eta>=1 if enforce_eta."""
    out = []
    for m in range(0, mcap + 1):
        eta = mp.mpf(k) ** m * E_sum(k, m, p) / (p - m)
        if enforce_eta and eta >= 1:
            break
        rho = (p - m) / (p * mp.mpf(k) ** m)
        out.append((eta, rho ** (k - 1)))
    return out


def rbinom(x, m):
    # NOTE: mp.binomial(x, m) silently returns 1/m! for x around 1e2000 (mpmath 1.3), so use the product.
    out = mp.mpf(1)
    for t in range(m):
        out *= (x - t) / (t + 1)
    return out


def LU(k, p, r, br):
    h = (p - 1) / k
    even = (r % 2 == 0)
    s = mp.mpf(0); best = None
    for m, (eta, rk) in enumerate(br):
        if m > r * h:
            break
        b = rbinom(r * h, m)
        l = b * rk * (1 - eta) ** (k - 1)
        u = b * rk * (1 + eta) ** (k - 1)
        if m == 0:
            l = u = mp.mpf(1)
        if even:
            s += l if m % 2 == 0 else -u
            if m % 2 == 1:
                best = s if best is None else max(best, s)
        else:
            s += u if m % 2 == 0 else -l
            if m % 2 == 0:
                best = s if best is None else min(best, s)
    if even:
        return mp.mpf(0) if best is None else max(best, 0)
    return mp.mpf(1) if best is None else min(best, 1)


def F(k, p, mcap=None, enforce_eta=True, rmax=None):
    if mcap is None:
        mcap = 4 * k
    br = brackets(k, p, mcap, enforce_eta)
    rmax = k if rmax is None else min(rmax, k)
    vals = [None] + [LU(k, p, r, br) for r in range(1, rmax + 1)]
    best = None; tot = mp.mpf(1)
    for r in range(1, rmax + 1):
        c = mp.binomial(k, r)
        tot += c * vals[r] if r % 2 == 0 else -c * vals[r]
        if r % 2 == 1 and (best is None or tot > best[0]):
            best = (tot, r)
    return best, len(br) - 1


def compare():
    sys.path.insert(0, HERE + "2026-11-05-rees-threshold-9")
    import cert
    for k, dps in [(100, 160), (200, 260)]:
        mp.mp.dps = dps
        for L in ["4.2", "4.6", "5", "6"]:
            p = mp.mpf(L) * mp.mpf(k) ** k + 1
            (f, R), Km = F(k, p)
            c = cert.point(k, float(L))
            print(f"k={k} L={L} indep F={mp.nstr(f,10)} R={R} Kmax={Km} | cert F={mp.nstr(c[0],10)} R={c[1]} Kmax={c[3]} "
                  f"reldiff={mp.nstr(abs(f-c[0])/abs(f),3)}", flush=True)


def members():
    mem = set()
    for f in glob.glob(HERE + "2026-11-04-rees-threshold-5/*.out") + glob.glob(HERE + "2026-11-02-rees-schedules/small-prime/*.out") \
            + glob.glob(HERE + "2026-11-05-rees-threshold-8/*.out"):
        for line in open(f):
            m = re.match(r"INFEASIBLE k=(\d+) p=(\d+)", line)
            if m:
                mem.add((int(m.group(1)), int(m.group(2))))
    return sorted(mem)


def literal():
    """Theorem 1 as literally stated: eta_m<1 required only for r even.  For r odd allow any K_r
    (up to 2k) using l_m = C rho^(k-1) (1-eta)^(k-1) even when eta_m >= 1."""
    mp.mp.dps = 60
    mem = members()
    hits = 0; n = 0
    for k, p in mem:
        p = mp.mpf(p)
        br_all = brackets(k, p, min(2 * k, int(p) - 1), enforce_eta=False)
        br_ok = brackets(k, p, min(2 * k, int(p) - 1), enforce_eta=True)
        vals = [None]
        for r in range(1, k + 1):
            vals.append(LU(k, p, r, br_ok if r % 2 == 0 else br_all))
        tot = mp.mpf(1); best = None
        for r in range(1, k + 1):
            c = mp.binomial(k, r)
            tot += c * vals[r] if r % 2 == 0 else -c * vals[r]
            if r % 2 == 1 and (best is None or tot > best):
                best = tot
        n += 1
        if best > 0:
            hits += 1
            if hits <= 8:
                print(f"LITERAL THEOREM 1 'CERTIFIES' E_2 MEMBER k={k} p={int(p)} F={mp.nstr(best,6)} U_1={mp.nstr(vals[1],6)}")
    print(f"literal reading: members={n} falsely certified={hits}")


def star():
    k = 729
    mp.mp.dps = 900
    for L in ["6", "7", "8.08", "8.1", "20", "76"]:
        Lam = mp.mpf(L); p = Lam * mp.mpf(k) ** k + 1
        u = mp.e ** (-Lam); mu = k * u
        if Lam < mp.log(k) + 1.5:
            R = 2 * int(mp.ceil(2 * mu + 2)) - 1; K = int(mp.ceil(4 * R * Lam))
        else:
            R = 1; K = int(mp.ceil(3.6 * Lam))
        delta = 3.1 * k * K * mp.mpf(k) ** K / mp.sqrt(p)
        star = (1 - u) ** k - mp.binomial(k, R + 1) * u ** (R + 1) \
            - mp.fsum(mp.binomial(k, r) * (mp.e * r * Lam / K) ** K for r in range(1, R + 1)) \
            - delta * mp.fsum(mp.binomial(k, r) * mp.e ** (r * Lam) for r in range(1, R + 1))
        if R == 1:
            star = 1 - k * (u + (mp.e * Lam / K) ** K + delta * mp.e ** Lam)
        print(f"k={k} Lambda={L} R={R} K={K} (star) lower bound={mp.nstr(star,6)} delta={mp.nstr(delta,3)}", flush=True)
    for L in ["6", "8.1"]:
        p = mp.mpf(L) * mp.mpf(k) ** k + 1
        (f, R), Km = F(k, p, mcap=k, rmax=41)
        print(f"k={k} Lambda={L} true Theorem-1 F={mp.nstr(f,6)} R={R} Kmax={Km}", flush=True)


def o2small():
    """Two-part inequalities of Remark 5 for k=3..8 at every prime p<=k^k/2, p=1 mod k (o2_compat.py skips these)."""
    mp.mp.dps = 30
    n = bad = 0
    for k in range(3, 8):
        lim = k ** k // 2
        for p in range(k + 1, lim + 1, k):
            if not all(p % q for q in range(2, int(p ** 0.5) + 1)):
                continue
            pp = mp.mpf(p)
            eta = [mp.mpf(k) ** m * E_sum(k, m, pp) / (pp - m) for m in range(0, min(2 * k, p))]
            Km = max(m for m in range(len(eta)) if eta[m] < 1)
            for m in range(2, Km + 1):
                for a in range(1, m):
                    b = m - a; n += 1
                    up = (1 + eta[a]) * (1 + eta[b]) * (pp - a) * (pp - b) / (pp * (pp - m))
                    lo = (1 - eta[a]) * (1 - eta[b])
                    if up > 1 + eta[m] or lo < 1 - eta[m]:
                        bad += 1; print("FAIL", k, p, a, b)
        print(f"k={k} done (primes up to {lim})", flush=True)
    print(f"o2small pairs={n} failures={bad}")


def consts():
    print("3.6*ln(e/3.6) =", 3.6 * (1 - math.log(3.6)))
    print("4*ln(e/4) =", 4 * (1 - math.log(4)), " ln(e/4)=", 1 - math.log(4))
    print("-0.5448*6-0.3862 =", -0.5448 * 6 - 0.3862, " exact coeffs:", 4 * (1 - math.log(4)) + 1, 1 - math.log(4))
    print("1/(1-e^-6) =", 1 / (1 - math.exp(-6)))
    print("e^-1.5 =", math.exp(-1.5), " 0.5/e =", 0.5 / math.e)
    c0 = 6 * math.exp(-6)
    for k in [10 ** 6 + 1, 2 * 10 ** 6, 3 * 10 ** 6, 10 ** 7]:
        KA = 16 * c0 * k + 20 * (math.log(k) + 1.5) + 1
        print(f"k={k}: Kbar_A/k = {KA / k:.6f}  (report claims <= 0.2381)  (1/2-KA/k)*ln k = {(0.5 - KA / k) * math.log(k):.4f}")
    print("8c0 + 1.0025 e^-6 =", 8 * c0 + 1.0025 * math.exp(-6))
    k = 729
    print("k=729: kappa(8kappa)^-1.5 =", k * (8 * k) ** -1.5, " 3/8 + that =", 3 / 8 + k * (8 * k) ** -1.5)


if __name__ == "__main__":
    {"compare": compare, "literal": literal, "star": star, "o2small": o2small, "consts": consts}[sys.argv[1]]()

"""Algebra check of Theorem 1's double Bonferroni on laws where everything is exact.

Model: n_0..n_{k-1} i.i.d. Binomial(H, q).  Then E C(M_S, m) = C(rH, m) q^m exactly and
P(all n_j > 0) = (1 - (1-q)^H)^k.  We feed brackets [ (1-d) E, (1+d) E ] into the same
assembly as cert.bestF (cert.best_LU logic re-implemented on a generic bracket) and check
F <= P(all > 0).  Also checks a mixed (non-independent) law: n_j = B_j * Z with a shared
Bernoulli Z, where the joint moments are again exact.
"""
import itertools, math
import mpmath as mp

mp.mp.dps = 400


def assemble(k, bracket, Km, Rmax):
    """bracket(r, m) -> (l, u).  Returns max over odd R of the Theorem 1 lower bound."""
    tot = mp.mpf(1); best = None
    for r in range(1, Rmax + 1):
        want_lower = (r % 2 == 0)
        acc = mp.mpf(0); bv = None
        for m in range(0, Km + 1):
            l, u = bracket(r, m)
            if want_lower:
                acc += l if m % 2 == 0 else -u
                if m % 2 == 1 and (bv is None or acc > bv):
                    bv = acc
            else:
                acc += u if m % 2 == 0 else -l
                if m % 2 == 0 and (bv is None or acc < bv):
                    bv = acc
        bv = max(bv, mp.mpf(0)) if want_lower else min(bv, mp.mpf(1))
        c = mp.binomial(k, r)
        tot += c * bv if want_lower else -c * bv
        if r % 2 == 1 and (best is None or tot > best):
            best = tot
    return best


def run():
    nfail = 0; n = 0; pos = 0
    for k in [5, 10, 30, 60, 120, 200]:
        for H in [50, 400]:
            for lam in [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]:
                q = mp.mpf(lam) / H
                for d in [mp.mpf(0), mp.mpf(10) ** -12, mp.mpf(10) ** -4]:
                    def br(r, m, q=q, H=H, d=d):
                        e = mp.binomial(r * H, m) * q ** m
                        return ((1 - d) * e, (1 + d) * e)
                    Km = min(k // 2, 120)
                    F = assemble(k, br, Km, k if k % 2 else k - 1)
                    truth = (1 - (1 - q) ** H) ** k
                    n += 1
                    if F > truth + mp.mpf(10) ** -100:
                        nfail += 1
                        print(f"FAIL k={k} H={H} lam={lam} d={d} F={mp.nstr(F,10)} truth={mp.nstr(truth,10)}")
                    if F > 0:
                        pos += 1
                print(f"k={k} H={H} lam={lam} truth={mp.nstr((1 - (1 - q) ** H) ** k, 6)} "
                      f"F(d=0)={mp.nstr(assemble(k, lambda r, m: (mp.binomial(r*H, m)*q**m,)*2, min(k//2,120), k if k%2 else k-1), 6)}",
                      flush=True)
    # correlated law: n_j = B_j Z, Z ~ Bernoulli(z) shared, B_j iid Bin(H,q).  M_S = Z * sum B_j.
    for k in [10, 40]:
        for z in [0.5, 0.9]:
            for lam in [1.0, 3.0, 6.0]:
                H = 200; q = mp.mpf(lam) / H; z = mp.mpf(z)
                def br(r, m):
                    e = (mp.mpf(1) if m == 0 else z) * mp.binomial(r * H, m) * q ** m
                    return (e, e)
                F = assemble(k, br, min(k // 2, 60), k if k % 2 else k - 1)
                truth = z * (1 - (1 - q) ** H) ** k
                n += 1
                if F > truth + mp.mpf(10) ** -100:
                    nfail += 1
                    print(f"FAIL corr k={k} z={z} lam={lam} F={mp.nstr(F,10)} truth={mp.nstr(truth,10)}")
    print(f"cases={n} failures={nfail} positive_F={pos}")


if __name__ == "__main__":
    run()

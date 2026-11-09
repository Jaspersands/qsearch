"""Exact |Good(beta)| minima (rem:sde-block-steered, rem:sde-worst-case).

Good(beta) = {s in F_p : beta_b + s in Q^o_{-c_b} for all b}, Q_c = g^c P,
P = nonzero kappa-th powers.  E_cg(J,kappa): some J' <= J, classes not all
equal, pairwise distinct beta, with Good empty.  G_J(p) = least |Good| over that
data; G*_J(p) also allows all classes equal and J' = 1.
Normalisation: translate so beta_1 = 0; scale (classes shift uniformly, and
all class patterns are enumerated) so beta_2 = 1; then beta_3 = t ranges over
F_p minus {0,1}, handled for all t at once by an FFT correlation.
"""
import itertools, sys, time
import numpy as np
import sympy

def coset_sets(p, kappa):
    g = sympy.primitive_root(p)
    cos = np.full(p, -1, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        cos[x] = e % kappa
        x = x * g % p
    A = []  # A[c] = indicator of Q^o_{-c}
    for c in range(kappa):
        ind = np.zeros(p, dtype=np.int64)
        ind[cos == ((-c) % kappa)] = 1
        ind[0] = 1
        A.append(ind)
    return A

def minima(p, kappa):
    A = coset_sets(p, kappa)
    h = (p - 1) // kappa
    res = {"G1": h + 1}
    # J' = 2: beta = (0,1)
    g2_ne, g2_all = None, None
    for c1, c2 in itertools.product(range(kappa), repeat=2):
        val = int(np.sum(A[c1] * np.roll(A[c2], -1)))  # s in A_c1, s+1 in A_c2
        if c1 != c2:
            g2_ne = val if g2_ne is None else min(g2_ne, val)
        else:
            g2_all = val if g2_all is None else min(g2_all, val)
    res["G2_noteq"] = g2_ne
    res["G2_eq"] = g2_all
    # J' = 3: beta = (0,1,t), t not in {0,1}
    n = 1
    while n < 2 * p:
        n *= 2
    g3_ne, g3_all = None, None
    for c1, c2, c3 in itertools.product(range(kappa), repeat=3):
        f = A[c1] * np.roll(A[c2], -1)          # f(s) = [s in A_c1][s+1 in A_c2]
        gg = A[c3]
        # corr(t) = sum_s f(s) gg(s+t mod p)
        F = np.fft.rfft(np.concatenate([f, np.zeros(n - p)]))
        Gd = np.fft.rfft(np.concatenate([gg, gg, np.zeros(n - 2 * p)]))
        # sum_s f(s) gg2(s+t) for t in [0,p) where gg2 = gg repeated twice
        corr = np.fft.irfft(np.conj(F) * Gd, n)[:p]
        corr = np.rint(corr).astype(np.int64)
        vals = corr[2:]  # t in {2..p-1}
        m = int(vals.min())
        if len({c1, c2, c3}) > 1:
            g3_ne = m if g3_ne is None else min(g3_ne, m)
        else:
            g3_all = m if g3_all is None else min(g3_all, m)
    res["G3_noteq"] = g3_ne
    res["G3_eq"] = g3_all
    return res

def weil(p, kappa, J):
    return kappa ** (-J) * (p - J - (kappa ** J - 1) * (J - 1) * np.sqrt(p))

if __name__ == "__main__":
    t0 = time.time()
    # sanity: brute force at a few small primes
    def brute(p, kappa):
        A = coset_sets(p, kappa)
        best_ne, best_all = None, None
        for c in itertools.product(range(kappa), repeat=3):
            for b in itertools.combinations(range(p), 3):
                for perm in [b]:
                    cnt = sum(1 for s in range(p) if all(A[c[i]][(perm[i] + s) % p] for i in range(3)))
                    if len(set(c)) > 1:
                        best_ne = cnt if best_ne is None else min(best_ne, cnt)
                    else:
                        best_all = cnt if best_all is None else min(best_all, cnt)
        return best_ne, best_all
    for p, k in [(7, 2), (11, 2), (13, 3), (19, 3), (31, 3)]:
        m = minima(p, k)
        print("brute check", p, k, brute(p, k), (m["G3_noteq"], m["G3_eq"]))
    out = {}
    for kappa, pmax in [(2, 5000), (3, 11000)]:
        Ecg = []
        G3, G3s = {}, {}
        for p in sympy.primerange(3, pmax + 1):
            if (p - 1) % kappa:
                continue
            m = minima(p, kappa)
            g3 = min(m["G2_noteq"], m["G3_noteq"])
            g3s = min(g3, m["G1"], m["G2_eq"], m["G3_eq"])
            G3[p], G3s[p] = g3, g3s
            if g3 == 0:
                Ecg.append(p)
        out[kappa] = (Ecg, G3, G3s)
        print(f"kappa={kappa}: E_cg(3,{kappa}) up to {pmax} = {Ecg}  [{time.time()-t0:.1f}s]")
        sys.stdout.flush()
    claim33 = [7,13,19,31,37,43,61,67,73,79,97,103,109,127,139,151,157,163,181,193,211,241]
    print("E_cg(3,3) matches paper list:", out[3][0] == claim33)
    # G*_3 >= 1 exactly when p >= 11 (kappa=2), exactly when p not in E_cg(3,3) (kappa=3)
    E2, G3_2, G3s_2 = out[2]
    print("kappa=2: primes with G*_3 = 0:", [p for p, v in G3s_2.items() if v == 0])
    E3, G3_3, G3s_3 = out[3]
    print("kappa=3: primes with G*_3 = 0 == E_cg(3,3):", sorted(p for p, v in G3s_3.items() if v == 0) == E3)
    # thresholds: G*_3 >= p/10 (kappa=2, p>=256), G*_3 >= p/54 (kappa=3, p>=2750)
    bad2 = [(p, v) for p, v in G3s_2.items() if p >= 256 and v < p / 10]
    bad3 = [(p, v) for p, v in G3s_3.items() if p >= 2750 and v < p / 54]
    print("kappa=2 violations of G*_3>=p/10 for 256<=p<=5000:", bad2)
    print("kappa=3 violations of G*_3>=p/54 for 2750<=p<=11000:", bad3)
    print("min ratio G*_3/p, kappa=2, p>=256:", min(v / p for p, v in G3s_2.items() if p >= 256),
          " kappa=3, p>=2750:", min(v / p for p, v in G3s_3.items() if p >= 2750))
    # smallest p beyond which the Weil bound alone gives the claims
    for kappa, frac, start in [(2, 10, 5000), (3, 54, 11000)]:
        print(f"Weil J=3 bound >= p/{frac} at p={start}:", weil(start, kappa, 3) >= start / frac,
              " (also J=2):", weil(start, kappa, 2) >= start / frac)
    # where do the i.i.d. claims start: smallest p in range from which G_3(p) never drops below p/10, p/54
    print(f"total {time.time()-t0:.1f}s")

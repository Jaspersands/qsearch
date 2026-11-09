"""Second-moment certificate for the two-level (alpha, beta) contraction.

Problem (small-prime report, section 1): find alpha_0..alpha_{k-1},
beta_0..beta_{k-1} in F_p with alpha_j + beta_i in A_{-(i+j)} = Q_{-(i+j)} U {0}
for all i, j and alpha_0 + beta_0 != 0.  Q_m = g^m H, H = (F_p^*)^k.

Unnormalised form used here: y_0 = beta_0 = 0, y = (y_1..y_{k-1}) uniform in
F_p^{k-1}.  For column j in Z_k let
    n_j(y) = #{x : x + y_i in Q_{-(i+j)} for all i = 0..k-1}   (strict cosets).
If n_j(y) >= 1 for every j, then alpha_j := any such x and beta := y give a
contraction (alpha_0 in Q_0 != 0).

Exact moments (proved in the report, section 2):
    E[n_j]   = h^k / p^(k-1)
    E[n_j^2] = E[n_j] + h p^-(k-1) sum_c r_c prod_{b != -c} m_b
with m_b = #{v in Q_b : v+1 in Q_b}, r_c = #{w in Q_0, w != 1 : w-1 in Q_c}.
Both are independent of j.  Paley-Zygmund + union bound: if
    Phi := k (1 - E[n]^2 / E[n^2]) < 1
then a fraction >= 1 - Phi of all y works.

Modes
  check KAPPA PMAX        brute-force E[n], E[n^2] over all y, compare to formula
  exc                     R and Phi at every listed exceptional prime (k = 4, 5)
  scan KAPPA PMAX         largest prime <= PMAX with Phi >= 1, count certified
  sample KAPPA P TRIALS   empirical fraction of good y vs the 1 - Phi bound
"""
import sys
from fractions import Fraction

import numpy as np
from sympy import primerange, primitive_root


def coset_index(p, k):
    """idx[x] = log_g(x) mod k for x in 1..p-1, idx[0] = -1."""
    g = primitive_root(p)
    idx = np.full(p, -1, dtype=np.int64)
    v = 1
    for e in range(p - 1):
        idx[v] = e % k
        v = v * g % p
    return idx


def cyclotomic_data(p, k, idx=None):
    if idx is None:
        idx = coset_index(p, k)
    v = np.arange(1, p - 1)  # v and v+1 both nonzero
    a, b = idx[v], idx[v + 1]
    same = a == b
    m = np.bincount(a[same], minlength=k)
    w = np.arange(2, p)  # w != 0, 1
    sel = idx[w] == 0
    r = np.bincount(idx[w[sel] - 1], minlength=k)
    return [int(t) for t in m], [int(t) for t in r]


def moments(p, k, m=None, r=None):
    """Exact (E[n], E[n^2]) as Fractions."""
    if m is None:
        m, r = cyclotomic_data(p, k)
    h = (p - 1) // k
    s = 0
    for c in range(k):
        prod = 1
        for bb in range(k):
            if bb != (-c) % k:
                prod *= m[bb]
        s += r[c] * prod
    e1 = Fraction(h ** k, p ** (k - 1))
    e2 = e1 + Fraction(h * s, p ** (k - 1))
    return e1, e2


def phi(p, k, **kw):
    e1, e2 = moments(p, k, **kw)
    return k * (1 - e1 * e1 / e2), e2 / (e1 * e1)


def brute(p, k):
    """E[n_j], E[n_j^2] for every j by enumerating all y in F_p^{k-1}."""
    idx = coset_index(p, k)
    x = np.arange(p)
    tot1 = np.zeros(k)
    tot2 = np.zeros(k)
    good = 0
    for flat in range(p ** (k - 1)):
        y = [0]
        t = flat
        for _ in range(k - 1):
            y.append(t % p)
            t //= p
        cnt = []
        for j in range(k):
            ok = np.ones(p, dtype=bool)
            for i in range(k):
                ok &= idx[(x + y[i]) % p] == (-(i + j)) % k
            cnt.append(int(ok.sum()))
        cnt = np.array(cnt)
        tot1 += cnt
        tot2 += cnt ** 2
        good += bool((cnt > 0).all())
    N = p ** (k - 1)
    return tot1 / N, tot2 / N, good / N


def main():
    mode = sys.argv[1]
    if mode == "check":
        k, pmax = int(sys.argv[2]), int(sys.argv[3])
        for p in primerange(3, pmax + 1):
            if (p - 1) % k:
                continue
            e1, e2 = moments(p, k)
            b1, b2, good = brute(p, k)
            ok = np.allclose(b1, float(e1)) and np.allclose(b2, float(e2))
            f, R = phi(p, k)
            print(f"k={k} p={p} formula E1={float(e1):.6f} E2={float(e2):.6f} "
                  f"brute E1={b1.round(6).tolist()} E2={b2.round(6).tolist()} "
                  f"match={ok} goodfrac={good:.6f} 1-Phi={1 - float(f):.6f}")
            if not ok:
                raise SystemExit("MISMATCH")
            if good + 1e-12 < 1 - float(f):
                raise SystemExit("BOUND VIOLATED")
    elif mode == "exc":
        exc = {4: [5, 13, 17, 29, 37, 53], 5: [11, 31, 41, 61, 71, 101, 131, 151, 181]}
        for k, ps in exc.items():
            for p in ps:
                f, R = phi(p, k)
                print(f"k={k} p={p} R={float(R):.4f} Phi={float(f):.4f} "
                      f"certified={f < 1}")
                if f < 1:
                    raise SystemExit("CONTRADICTION: certificate at exceptional prime")
    elif mode == "scan":
        k, pmax = int(sys.argv[2]), int(sys.argv[3])
        last_fail, ncert, nfail = None, 0, 0
        for p in primerange(3, pmax + 1):
            if (p - 1) % k:
                continue
            f, R = phi(p, k)
            if f < 1:
                ncert += 1
            else:
                nfail += 1
                last_fail = p
        print(f"k={k} pmax={pmax} certified={ncert} uncertified={nfail} "
              f"largest_uncertified={last_fail}")
    elif mode == "sample":
        k, p, trials = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        rng = np.random.default_rng(1)
        idx = coset_index(p, k)
        x = np.arange(p)
        good = 0
        for _ in range(trials):
            y = [0] + [int(t) for t in rng.integers(0, p, k - 1)]
            allok = True
            for j in range(k):
                ok = np.ones(p, dtype=bool)
                for i in range(k):
                    ok &= idx[(x + y[i]) % p] == (-(i + j)) % k
                if not ok.any():
                    allok = False
                    break
            good += allok
        f, R = phi(p, k)
        print(f"k={k} p={p} trials={trials} goodfrac={good / trials:.4f} "
              f"bound 1-Phi={1 - float(f):.4f}")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()

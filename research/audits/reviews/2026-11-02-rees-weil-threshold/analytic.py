"""Analytic threshold T_A(kappa) for the second-moment certificate Phi < 1.

Sufficient condition (proved in the report, section 3), with L <= 1 dropped:
    U(p) := k^k p^(k-1)/(p-1)^k + exp(Emax(Delta(p))) < k/(k-1),
    Delta(p) = ((k-1)(k-2) sqrt(p) + 2(k-1)) / (p - k - 1),
    Emax(D) = max_{0 <= s <= sqrt(k) D} ( -A s^2 + B s ),
    A = 1/2 - D/3 - 1/(k(1-D)),  B = D/(sqrt(k)(1-D)),
and Delta(p) <= DELTA_MAX = 1/2.  U is decreasing in real p > k+1, so T_A is
found by bisection over reals and the condition holds for every p >= T_A.

Modes
  table                 T_A(k) for k = 2..12 against T_W(k) and (k-1)k^k, and
                        the sampler threshold T_S(k) (U(p) <= 1 + 1/(8k))
  verify KAPPA PMAX     at every prime p = 1 mod k up to PMAX: check the
                        Jacobi-sum bound |delta_b|, |eta_c| <= Delta(p), the
                        identities sum m_b = sum r_c = (p-k-1)/k, and that
                        U(p) >= the exact R(p) whenever Delta(p) <= DELTA_MAX
"""
import math
import sys

from sympy import primerange

from second_moment import cyclotomic_data, moments

DELTA_MAX = 0.5


def delta(p, k):
    return ((k - 1) * (k - 2) * math.sqrt(p) + 2 * (k - 1)) / (p - k - 1)


def emax(D, k):
    A = 0.5 - D / 3 - 1 / (k * (1 - D))
    B = D / (math.sqrt(k) * (1 - D))
    smax = math.sqrt(k) * D
    best = max(0.0, -A * smax * smax + B * smax)
    if A > 0:
        s = B / (2 * A)
        if s <= smax:
            best = max(best, B * B / (4 * A))
    return best


def U(p, k):
    return k ** k * p ** (k - 1) / (p - 1) ** k + math.exp(emax(delta(p, k), k))


def ok(p, k):
    return delta(p, k) <= DELTA_MAX and U(p, k) < k / (k - 1)


def ok_sampler(p, k):
    """U(p) <= 1 + 1/(8k): then P_y(some n_j < E[n]/2) <= 4k(R-1) <= 1/2."""
    return delta(p, k) <= DELTA_MAX and U(p, k) <= 1 + 1 / (8 * k)


def T_A(k, test=ok):
    lo, hi = k + 2.0, 64.0 * k ** (k + 2) + 1e4
    assert test(hi, k)
    for _ in range(200):
        mid = (lo + hi) / 2
        if test(mid, k):
            hi = mid
        else:
            lo = mid
    return hi


def T_W(k):
    A = (k - 2) * k ** k + 1
    return ((A + math.sqrt(A * A + 4 * k ** k)) / 2) ** 2


def main():
    mode = sys.argv[1]
    if mode == "table":
        print("k  T_A(k)        (k-1)k^k      T_W(k)        T_W/T_A      "
              "1.5k^((k+1)/2)  T_S(k)        old sampler 4((k-1)k^k+1)^2")
        for k in range(2, 13):
            ta = T_A(k)
            ts = T_A(k, ok_sampler)
            print(f"{k:<2} {ta:<13.6g} {(k - 1) * k ** k:<13.6g} {T_W(k):<13.6g} "
                  f"{T_W(k) / ta:<12.4g} {1.5 * k ** ((k + 1) / 2):<15.4g} {ts:<13.6g} "
                  f"{4 * ((k - 1) * k ** k + 1) ** 2:.4g}")
    elif mode == "verify":
        k, pmax = int(sys.argv[2]), int(sys.argv[3])
        worst, n = 0.0, 0
        for p in primerange(k + 2, pmax + 1):
            if (p - 1) % k:
                continue
            m, r = cyclotomic_data(p, k)
            mu = (p - k - 1) / k ** 2
            assert sum(m) * k == p - k - 1 and sum(r) * k == p - k - 1, p
            d = max(abs(x / mu - 1) for x in m + r)
            D = delta(p, k)
            assert d <= D + 1e-12, (p, d, D)
            worst = max(worst, d / D)
            if D <= DELTA_MAX:
                e1, e2 = moments(p, k, m=m, r=r)
                R = float(e2 / (e1 * e1))
                assert U(p, k) >= R - 1e-12, (p, U(p, k), R)
            n += 1
        print(f"k={k} primes={n} up to {pmax}: all checks passed; "
              f"max |dev|/Delta = {worst:.4f}")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()

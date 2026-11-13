"""Euler characteristic of the open stratum M (normalised beta_0=0, alpha_0=1) and the
Deligne-Betti barrier of the analytic report, section 3.

#M(F_q) = P(q)/(q(q-1)) with P the chromatic polynomial of K_{k,k}
(vertices alpha_j and -beta_i; an edge forbids alpha_j + beta_i = 0).
chi_c(M) = value of the counting polynomial at q = 1 = (P(t)/t)'(1)  (polynomial count,
Orlik-Solomon / Bjorner-Ekedahl).  beta_k := |chi_c(M)|.
Barrier: p^(k-1) <= (k^(k^2-1) - 1) beta_k  =>  no Deligne-Betti term-by-term certificate.
Modes:  table K0 K1 ;  brute K pmax  (checks the point count formula by enumeration)
"""
import sys
from math import comb, log
import sympy as sp

t = sp.symbols('t')

def chrom_Kkk(k):
    # P_{K_{m,n}}(t) = sum_j S(m,j) (t)_j (t-j)^n
    P = 0
    for j in range(1, k + 1):
        P += sp.functions.combinatorial.numbers.stirling(k, j) * sp.ff(t, j) * (t - j) ** k
    return sp.expand(P)

def beta(k):
    P = chrom_Kkk(k)
    Q = sp.cancel(P / (t * (t - 1)))
    return sp.Integer(Q.subs(t, 1)), sp.Poly(Q, t)

def table(K0, K1):
    print("k | chi_c(M) | beta^(1/(k-1)) | log_k T_Del | log_k k^(k+1) | T_Del / k^(k+1)")
    for k in range(K0, K1 + 1):
        b, _ = beta(k)
        B = abs(int(b))
        lt = (log(k ** (k * k - 1) - 1) + log(B)) / ((k - 1) * log(k))
        print(f"{k} | {int(b)} | {B ** (1.0 / (k - 1)):.4f} | {lt:.4f} | {k + 1} | "
              f"{k ** (lt - k - 1):.4f}")

def brute(k, pmax):
    _, Q = beta(k)
    import itertools
    for p in sp.primerange(3, pmax + 1):
        cnt = 0
        for a in itertools.product(range(p), repeat=k - 1):
            al = (1,) + a
            for b in itertools.product(range(p), repeat=k - 1):
                be = (0,) + b
                if all((al[j] + be[i]) % p for i in range(k) for j in range(k)):
                    cnt += 1
        print(f"k={k} p={p}: enumerated {cnt}, formula {Q.eval(p)}, match={cnt == Q.eval(p)}")

if __name__ == "__main__":
    if sys.argv[1] == "table":
        table(int(sys.argv[2]), int(sys.argv[3]))
    else:
        brute(int(sys.argv[2]), int(sys.argv[3]))

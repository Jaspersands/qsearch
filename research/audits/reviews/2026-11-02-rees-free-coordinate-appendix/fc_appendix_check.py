"""Independent exact checks for docs/papers/rees-hsp/appendix-free-coordinate.tex.

AI session, 2026-11-02.  Written from the appendix, not from the report's scripts (it imports
nothing from them).  Every comparison is exact (Python integers and fractions.Fraction); ln 2 is
used only through the rational bounds LN2_LO < ln 2 < LN2_UP.  These are checks of displayed
inequalities and of finite cases, not proofs.

Run:  /opt/anaconda3/bin/python -I -B -u fc_appendix_check.py > fc_appendix_check_out.txt
"""
from fractions import Fraction as F
from itertools import product
from math import gcd, log2
import sys

LN2_LO = F(6931471805599453, 10 ** 16)
LN2_UP = F(6931471805599454, 10 ** 16)


def lg(x):
    x = F(x)
    return log2(x.numerator) - log2(x.denominator)


def ceil_frac(x):
    x = F(x)
    return -((-x.numerator) // x.denominator)


def ceil_log(base, x):
    """least integer k >= 0 with base^k >= x (x a positive Fraction)."""
    k = 0
    while F(base) ** k < x:
        k += 1
    return k


def clog2(x):
    return ceil_log(2, F(x))


def is_prime(n):
    if n < 2:
        return False
    for q in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def beta(p, k, M, n0, a):
    h = (p - 1) // k
    q = F(h + 1, p)
    L = M - n0
    return 4 / (F(h) ** (n0 - 1) * q ** a) + F(p ** a - 1, (p - 1)) / F(p) ** L


# ---------------------------------------------------------------- part (ii) inequalities
def check_part_ii():
    print("== part (ii): displayed inequalities")
    for u in range(2, 121):
        assert 16 * u * u - 1 >= 15 * u * u  # h >= (16u^2-1)/u >= 15u
        first = F(4 * u) ** (u - 1) * 4 / (F(15) ** (2 * u) * F(u) ** (u + 1))
        assert first == F(4, 225) ** u / u ** 2
        second = F(4 * u) ** (u - 1) * 2 / F(16 * u * u) ** (u + 1)
        assert second == F(2 * 4 ** (u - 1), 16 ** (u + 1)) / F(u) ** (u + 3)
        assert first + second <= F(1, 64)
        if u == 2:
            assert first + second < F(15, 100000)
        for c in range(2, u + 1):
            M = 4 * u
            T = (M ** (c - 1) - 1) // (M - 1)
            B = clog2(64 * M ** (c - 1))
            assert T <= M ** (c - 1) and 3 * T * F(1, 2 ** B) <= F(3, 64)
            node = (first + second) / F(4 * u) ** (u - 1)  # per-node bound, p = 16u^2
            assert T * node <= F(1, 64)
            assert B <= 7 + (u - 1) * clog2(4 * u)
    print("   u = 2..120: h >= 15u; tree bank sum = (4/225)^u/u^2 + 2*4^(u-1)/(16^(u+1)u^(u+3)) <= 1/64;"
          " 3T2^-B <= 3/64 and B <= 7+(u-1)ceil(log2 4u) for c = 2..u: OK")
    # node bound beta <= 4*15^(-2u) u^(-u-1) + 2 p^(-u-1) at the least prime >= 16u^2 and at two
    # Mersenne primes, for every kappa <= u dividing p-1 and every a <= u-1
    for u in range(2, 31):
        bound_first = 4 / (F(15) ** (2 * u) * F(u) ** (u + 1))
        p0 = 16 * u * u
        while not is_prime(p0):
            p0 += 1
        for p in [p0, 2 ** 61 - 1, 2 ** 127 - 1]:
            for k in range(1, u + 1):
                if (p - 1) % k:
                    continue
                q = F((p - 1) // k + 1, p)
                assert q >= F(1, k)
                for a in range(0, u):
                    b = beta(p, k, 4 * u, 2 * u + 1, a)
                    assert b <= bound_first + 2 / F(p) ** (u + 1), (u, p, k, a)
    print("   u = 2..30: beta(4u, 2u+1; a) <= 4*15^(-2u)u^(-u-1) + 2p^(-u-1) for all kappa <= u, kappa | p-1,"
          " a <= u-1, at the least prime >= 16u^2, 2^61-1, 2^127-1; q >= 1/kappa: OK")


# ---------------------------------------------------------------- part (iii) budgets
def explicit_choice(p, k, g, tau):
    """n0 = 1 + ceil((g log(1/q) + log(8/tau))/log h), M = n0 + g + ceil(log_p(2/tau)), exactly."""
    h = (p - 1) // k
    q = F(h + 1, p)
    n0 = 1 + ceil_log(h, F(1) / q ** g * 8 / tau)
    M = n0 + g + ceil_log(p, 2 / tau)
    return M, n0


def least_choice(p, k, g, tau):
    """least M (with some n0) such that beta(M, n0; g) <= tau."""
    h = (p - 1) // k
    q = F(h + 1, p)
    best = None
    for n0 in range(1, 1000):
        first = 4 / (F(h) ** (n0 - 1) * q ** g)
        if first > tau:
            continue
        L = 0
        while first + F(p ** g - 1, p - 1) / F(p) ** L > tau:
            L += 1
        if best is None or L + n0 < best[0]:
            best = (L + n0, n0)
        if n0 > best[0]:
            break
    return best


def IS_B(d, a):
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** d.bit_length()


def budget_iii(p, glist, eps, mode):
    """Theorem (iii) budget.  glist = (g_1, ..., g_c); mode 'explicit' or 'least'."""
    c = len(glist)
    g = {d: glist[d - 1] for d in range(1, c + 1)}
    m = g[1]
    t = ceil_log(p, 3 / F(eps))
    S = m + t
    M, n0, kind, n = {}, {}, {}, {}
    acc = 1
    for d in range(2, c + 1):
        n[d] = acc
        k = gcd(d, p - 1)
        if k == 1:
            M[d], kind[d] = g[d] + 1, "lin"
        elif k == p - 1:
            assert d == p - 1
            M[d], kind[d] = IS_B(d, g[d]), "S1"
        else:
            tau = F(eps) / (9 * (c - 1) * S * n[d])
            if mode == "explicit":
                M[d], n0[d] = explicit_choice(p, k, g[d], tau)
            else:
                M[d], n0[d] = least_choice(p, k, g[d], tau)
            assert beta(p, k, M[d], n0[d], g[d]) <= tau
            kind[d] = "FCS"
        acc *= M[d]
    P = acc
    fcs = [d for d in kind if kind[d] == "FCS"]
    N = S * sum(n[d] for d in fcs)
    B = clog2(F(27 * N) / F(eps)) if N else 0
    caps = {}
    for d in fcs:
        k = gcd(d, p - 1)
        q = F((p - 1) // k + 1, p)
        caps[d] = ceil_frac(2 * B * LN2_UP / q ** g[d])
        # the cap is at least the theorem's ceil(2B ln2 q^-g) and at most one more
        assert caps[d] >= 2 * B * LN2_LO / q ** g[d]
    rank = F(p ** m - 1, (p - 1)) / F(p) ** S
    bank = S * sum(n[d] * beta(p, gcd(d, p - 1), M[d], n0[d], g[d]) for d in fcs)
    capsum = 3 * N * F(1, 2 ** B) if N else F(0)
    total = rank + bank + capsum + F(eps) / 3
    assert rank <= F(eps) / 3 and bank <= F(eps) / 9 and capsum <= F(eps) / 9 and total <= F(eps)
    Q = c * S * P
    total_trials = S * sum(n[d] * caps[d] for d in fcs)
    return dict(M=M, kind=kind, S=S, P=P, Q=Q, B=B, N=N, caps=caps, total_trials=total_trials,
                rank=rank, bank=bank, capsum=capsum, total=total)


def check_part_iii():
    print("\n== part (iii): class-nine profile g = (19,17,16,14,12,9,6,3,1), eps = 1/3")
    g9 = [19, 17, 16, 14, 12, 9, 6, 3, 1]
    table = {11: (42.3, 28.3, 47.0), 1031: (36.6, 33.4, 50.8), 5281: (39.1, 33.8, 52.2),
             2 ** 31 - 1: (35.9, 31.0, 49.8), 2 ** 61 - 1: (34.1, 33.5, 51.0), 2 ** 127 - 1: (34.0, 31.0, 49.5)}
    worst = 0
    for p in [11, 1031, 5281, 2 ** 31 - 1, 2 ** 61 - 1, 2 ** 127 - 1]:
        for mode in ["least", "explicit"]:
            r = budget_iii(p, g9, F(1, 3), mode)
            mx = max(r["caps"].values())
            argmx = max(r["caps"], key=lambda d: r["caps"][d])
            ps = "2^%d-1" % ((p + 1).bit_length() - 1) if p > 10 ** 6 and ((p + 1) & p) == 0 else str(p)
            print(f"   p={ps:>8s} {mode:8s}: log2Q={lg(r['Q']):6.1f} max log2 trials/node={lg(mx):5.1f}"
                  f" (grade {argmx}) log2 total trials={lg(r['total_trials']):5.1f} B={r['B']}"
                  f" err total={float(r['total']):.3f} <= 1/3")
            print("        arities " + " ".join(f"{d}:{r['kind'][d]}{r['M'][d]}" for d in sorted(r["M"])))
            if mode == "least":
                tq, tt, ttot = table[p]
                assert abs(round(lg(r["Q"]), 1) - tq) < 0.051, (p, lg(r["Q"]), tq)
                assert abs(round(lg(mx), 1) - tt) < 0.051, (p, lg(mx), tt)
                assert abs(round(lg(r["total_trials"]), 1) - ttot) < 0.051, (p, lg(r["total_trials"]), ttot)
                worst = max(worst, lg(mx))
    print(f"   table tab:fcs-budget, columns (iii), reproduced from the least public arities: OK;"
          f" largest per-node trial cap 2^{worst:.2f}")


# ---------------------------------------------------------------- small exhaustive cases
def powers(p, k):
    return sorted({pow(x, k, p) for x in range(1, p)})


def rref(rows, p):
    """rows: list of lists (a x M).  Returns (R as list of nonzero rows, pivots)."""
    A = [list(r) for r in rows]
    piv = []
    ri = 0
    M = len(A[0]) if A else 0
    for col in range(M):
        sel = None
        for i in range(ri, len(A)):
            if A[i][col] % p:
                sel = i
                break
        if sel is None:
            continue
        A[ri], A[sel] = A[sel], A[ri]
        inv = pow(A[ri][col], p - 2, p)
        A[ri] = [(v * inv) % p for v in A[ri]]
        for i in range(len(A)):
            if i != ri and A[i][col] % p:
                f = A[i][col]
                A[i] = [(A[i][j] - f * A[ri][j]) % p for j in range(M)]
        piv.append(col)
        ri += 1
        if ri == len(A):
            break
    return A[:ri], piv


def check_moment():
    print("\n== Lemma lem:fc-moment, exhaustive over C in F_p^(r x n)")
    for p, k, r, n in [(5, 2, 1, 3), (7, 3, 2, 2), (7, 2, 2, 2), (13, 4, 1, 3), (11, 5, 2, 2), (13, 3, 1, 3)]:
        P = powers(p, k)
        Dset = set(P) | {0}
        h = len(P)
        q = F(h + 1, p)
        xs = list(product(P, repeat=n))
        tot = 0
        tot2 = 0
        bad = 0
        cnt = 0
        EN = F(h) ** n * q ** r
        for flat in product(range(p), repeat=r * n):
            C = [flat[i * n:(i + 1) * n] for i in range(r)]
            N = sum(1 for x in xs if all(sum(C[i][j] * x[j] for j in range(n)) % p in Dset for i in range(r)))
            tot += N
            tot2 += N * N
            cnt += 1
            if N < EN / 2:
                bad += 1
        mean = F(tot, cnt)
        var = F(tot2, cnt) - mean ** 2
        assert mean == EN
        assert var == F(h) ** (n + 1) * (q ** r - q ** (2 * r))
        assert var <= h * EN
        cheb = 4 / (F(h) ** (n - 1) * q ** r)
        assert F(bad, cnt) <= cheb
        # oblivious identity: Pr_C[Cx in D^r] = q^r for every fixed x != 0, including x not in D^n
        for x in [tuple([1] + [0] * (n - 1)), tuple(range(1, n + 1)), tuple([p - 1] * n)]:
            hits = 0
            for flat in product(range(p), repeat=r * n):
                C = [flat[i * n:(i + 1) * n] for i in range(r)]
                if all(sum(C[i][j] * x[j] for j in range(n)) % p in Dset for i in range(r)):
                    hits += 1
            assert F(hits, p ** (r * n)) == q ** r
        print(f"   (p,kappa,r,n)=({p},{k},{r},{n}): E N = h^n q^r, Var N = h^(n+1)(q^r-q^2r) <= h E N exact;"
              f" bad fraction {float(F(bad, cnt)):.4f} <= Chebyshev {float(min(cheb, 1)):.4f}; oblivious identity OK")


def check_banks():
    print("\n== Lemmas lem:fc-rref and lem:fc-node, exhaustive over banks X in F_p^(a x M)")
    for p, k, a, M, n0 in [(5, 2, 1, 5, 3), (7, 3, 1, 5, 3), (13, 2, 1, 4, 3), (13, 4, 1, 4, 2), (5, 2, 2, 4, 2),
                           (7, 3, 2, 3, 1)]:
        P = powers(p, k)
        Dset = set(P) | {0}
        h = len(P)
        q = F(h + 1, p)
        bad = 0
        total = 0
        law = {}  # (r, pivots) -> {C: count}
        pattern_fail = 0
        rc_acc = F(0)
        rc_cnt = 0
        for flat in product(range(p), repeat=a * M):
            X = [flat[i * M:(i + 1) * M] for i in range(a)]
            R, piv = rref(X, p)
            r = len(piv)
            pr = piv[-1] + 1 if r else 0
            nprime = M - pr
            total += 1
            if piv != list(range(a)):
                pattern_fail += 1
            if nprime < n0:
                bad += 1
                continue
            Fcols = list(range(pr, M))
            C = tuple(tuple((-R[i][j]) % p for j in Fcols) for i in range(r))
            law.setdefault((r, tuple(piv)), {})
            law[(r, tuple(piv))][C] = law[(r, tuple(piv))].get(C, 0) + 1
            if r == 0:
                continue
            N = sum(1 for x in product(P, repeat=nprime)
                    if all(sum(C[i][j] * x[j] for j in range(nprime)) % p in Dset for i in range(r)))
            if F(N, h ** nprime) < q ** r / 2:
                bad += 1
            if piv == list(range(a)):
                # Prop. prop:rc-lower: acceptance of a uniform kernel vector, generic pattern
                Rp = [[R[i][j] for j in range(a, M)] for i in range(a)]
                nn = M - a
                acc = 0
                for x in product(range(p), repeat=nn):
                    if not any(x) or not all(v in Dset for v in x):
                        continue
                    if all((-sum(Rp[i][j] * x[j] for j in range(nn))) % p in Dset for i in range(a)):
                        acc += 1
                rc_acc += F(acc, p ** nn)
                rc_cnt += 1
        # conditional law of C given (r, pi): uniform on F_p^(r x n')
        for (r, piv), dist in law.items():
            nprime = M - (piv[-1] + 1 if r else 0)
            if r == 0:
                continue
            assert len(dist) == p ** (r * nprime) and len(set(dist.values())) == 1, (p, k, a, M, r, piv)
        b = beta(p, k, M, n0, a)
        assert F(bad, total) <= b
        assert F(pattern_fail, total) <= F(1, p - 1)
        nn = M - a
        assert rc_acc / rc_cnt == (q ** nn - F(1, p) ** nn) * q ** a
        print(f"   (p,kappa,a,M,n0)=({p},{k},{a},{M},{n0}): {total} banks; C uniform given (r,pi) for every"
              f" pattern; bad fraction {float(F(bad, total)):.4f} <= beta {float(b):.4f}; generic-pattern failure"
              f" {float(F(pattern_fail, total)):.4f} <= 1/(p-1); uniform-kernel mean acceptance = (q^n-p^-n)q^a")


if __name__ == "__main__":
    check_part_ii()
    check_part_iii()
    check_moment()
    check_banks()
    print("\nALL CHECKS PASSED")
    sys.stdout.flush()

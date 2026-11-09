"""Exact budget for the combined per-grade SDE rule of the Rees composition.

Companion to research/audits/reviews/2026-11-02-rees-combined-schedule.md.
All counts are exact integers or Fractions; log2 values are printed for reading.

Rules compared (grades d = 2..c, kappa_d = gcd(d, p-1), g_d public):
  S1-paper : M_d = B_d(g_d) at every grade (main.tex Schedule 1 as written).
  S1-gcd   : M_d = B_{kappa_d}(g_d) (IS at the reduced degree, Bezout lift;
             kappa_d = 1 gives g_d + 1, the linear case).
  W        : S1-gcd, except Schedule 2 (g_d+1)((kappa_d-1)g_d+1) when
             kappa_d >= 2 and p >= 16 kappa_d^(2 kappa_d + 2).  Worst case, no label law.
  W+3      : W, except Schedule 3 (4 u_d columns, u_d = max(2, kappa_d, g_d+1))
             at grades with p >= 16 u_d^2 when that arity is smaller; tree restarts.
  S3-tree  : main.tex Theorem random-column as stated (one u for the whole tree).
"""
from fractions import Fraction as F
from math import gcd, log2
import sys

import sympy


def clog2(x):
    """ceil(log2(x)) for a positive integer or Fraction."""
    x = F(x)
    k = 0
    while F(2) ** k < x:
        k += 1
    while k > 0 and F(2) ** (k - 1) >= x:
        k -= 1
    return k


def B(d, a):
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** d.bit_length()  # bit_length(d) = ceil(log2(d+1))


def s2_ok(p, k):
    return k >= 2 and p >= 16 * k ** (2 * k + 2)


def s2_arity(k, g):
    return (g + 1) * ((k - 1) * g + 1)


def u_of(k, g):
    return max(2, k, g + 1)


def s3_ok(p, k, g):
    return p >= 16 * u_of(k, g) ** 2


def bank_bound(p, k, g, M):
    """Public upper bound on the Schedule-3 bank event at one node: 4/mu + Pr[rank < a], with a <= g."""
    h = (p - 1) // k
    return F(4 * h * p ** g, (h + 1) ** M - 1) + F(p ** g - 1, (p - 1) * p ** M)


def lg(x):
    x = F(x)
    if x == 0:
        return float("-inf")
    return log2(x.numerator) - log2(x.denominator)


def choose(rule, p, c, g):
    """Per-grade (schedule, arity). g[d] for d = 1..c (g[1] = m)."""
    out = {}
    for d in range(2, c + 1):
        k = gcd(d, p - 1)
        if rule == "S1-paper":
            out[d] = ("S1", B(d, g[d]))
            continue
        cand = [("S1" if k >= 2 else "lin", B(k, g[d]))]
        if rule in ("W", "W+3") and s2_ok(p, k):
            cand.append(("S2", s2_arity(k, g[d])))
        if rule == "W+3" and s3_ok(p, k, g[d]):
            cand.append(("S3", 4 * u_of(k, g[d])))
        out[d] = min(cand, key=lambda t: t[1])
    return out


def nodes_per_tree(c, M):
    """n_d = prod_{2 <= d' < d} M_{d'}: stage-d merges per terminal sample."""
    n, acc = {}, 1
    for d in range(2, c + 1):
        n[d] = acc
        acc *= M[d]
    return n, acc  # acc = P, leaves per terminal sample


def budget_worst_case(p, c, g, eps, rule):
    m = g[1]
    sch = choose(rule, p, c, g)
    M = {d: sch[d][1] for d in sch}
    n, P = nodes_per_tree(c, M)
    t = 0
    while F(p) ** t < 3 / eps:
        t += 1
    S = m + t
    Nmerge = S * sum(n.values())
    NS2 = S * sum(n[d] for d in sch if sch[d][0] == "S2")
    Ninstr = S * P + Nmerge + S
    qmax = max([m] + [M[d] * g[d] for d in M])
    eta = eps / (3 * Ninstr * qmax)
    rank = F(p ** m - 1, (p - 1) * p ** S)
    kcap = clog2(3 * NS2 / eps) if NS2 else 0
    solver = NS2 * F(1, 2 ** kcap) if NS2 else F(0)
    approx = Ninstr * (eps / (3 * Ninstr))
    total = rank + solver + approx
    assert rank <= eps / 3 and solver <= eps / 3 and total <= eps
    return dict(rule=rule, sch=sch, S=S, t=t, P=P, Q=c * S * P, Nmerge=Nmerge, NS2=NS2,
                Ninstr=Ninstr, eta_bits=clog2(1 / eta), rank=rank, solver=solver,
                approx=approx, total=total, kcap=kcap, trees=None)


def budget_restart(p, c, g, eps, sch):
    """Tree-restart budget (main.tex random-column (ii), generalised to mixed per-grade arities)."""
    m = g[1]
    sch = dict(sch)
    while True:
        M = {d: sch[d][1] for d in sch}
        n, P = nodes_per_tree(c, M)
        n_s3 = sum(n[d] for d in sch if sch[d][0] == "S3")
        n_s2 = sum(n[d] for d in sch if sch[d][0] == "S2")
        Bcap = clog2(64 * max(1, 3 * n_s3 + n_s2))
        bank = {d: n[d] * bank_bound(p, gcd(d, p - 1), g[d], M[d]) for d in sch if sch[d][0] == "S3"}
        if sum(bank.values(), F(0)) <= F(1, 64):
            break
        worst = max(bank, key=bank.get)  # raise the worst S3 arity by one column (public data only)
        sch[worst] = ("S3", sch[worst][1] + 1)
    classical = (3 * n_s3 + n_s2) * F(1, 2 ** Bcap)
    tree_abort = classical + sum(bank.values(), F(0))
    assert tree_abort <= F(1, 16)
    mp = m + clog2(3 / eps)
    trees = 4 * mp
    Ntree_merge = sum(n.values())
    Ninstr = trees * (P + Ntree_merge + 1)
    rank = F(p ** m - 1, (p - 1) * p ** mp)
    few = F(1, 2 ** (2 * mp))  # Hoeffding e^{-3.78 m'} <= 2^{-2m'}
    approx = eps / 3
    total = rank + few + approx
    assert rank <= eps / 3 and few <= eps / 3 and total <= eps
    s3_trials = {d: 4 * gcd(d, p - 1) ** M[d] * Bcap for d in sch if sch[d][0] == "S3"}
    return dict(sch=sch, P=P, Q=c * trees * P, trees=trees, mp=mp, Bcap=Bcap, tree_abort=tree_abort,
                bank=sum(bank.values(), F(0)), Ninstr=Ninstr, rank=rank, solver=few, approx=approx,
                total=total, s3_trials=s3_trials)


def s3_tree(p, c, g, eps):
    """main.tex Theorem random-column with u = max(c, max_{d>=2} g_d + 1)."""
    u = max(c, max(g[d] for d in range(2, c + 1)) + 1)
    if p < 16 * u * u:
        return None
    sch = {d: ("S3", 4 * u) for d in range(2, c + 1)}
    return budget_restart(p, c, g, eps, sch), u


def fmt_sch(sch):
    return " ".join(f"{d}:{s}{'' if s in ('S1',) else ''}" for d, (s, _) in sorted(sch.items()))


def report(label, p, c, glist, eps):
    assert sympy.isprime(p) and p > c, p
    g = {d + 1: glist[d] for d in range(c)}
    print(f"\n-- {label}: c={c} g={tuple(glist)} p={p} eps={eps}")
    print("   kappa_d: " + " ".join(f"{d}:{gcd(d, p - 1)}" for d in range(2, c + 1)))
    base = budget_worst_case(p, c, g, eps, "S1-paper")
    rows = [base, budget_worst_case(p, c, g, eps, "S1-gcd"), budget_worst_case(p, c, g, eps, "W")]
    for r in rows:
        print(f"   {r['rule']:8s} log2Q={lg(r['Q']):8.1f} save={lg(base['Q']) - lg(r['Q']):7.1f} "
              f"S={r['S']} NS2={r['NS2']} kcap={r['kcap']} log2Ninstr={lg(r['Ninstr']):7.1f} "
              f"eta_bits={r['eta_bits']} rank={float(r['rank']):.2e} solver={float(r['solver']):.2e} "
              f"approx={float(r['approx']):.2e} total<=eps={r['total'] <= eps}")
        print(f"            schedules {fmt_sch(r['sch'])}; arities "
              + " ".join(f"{d}:{r['sch'][d][1]}" if r['sch'][d][1] < 10 ** 6 else f"{d}:2^{lg(r['sch'][d][1]):.1f}"
                         for d in sorted(r['sch'])))
    w3 = choose("W+3", p, c, g)
    if any(s == "S3" for s, _ in w3.values()):
        r = budget_restart(p, c, g, eps, w3)
        print(f"   W+3      log2Q={lg(r['Q']):8.1f} save={lg(base['Q']) - lg(r['Q']):7.1f} trees={r['trees']} "
              f"B={r['Bcap']} tree_abort={float(r['tree_abort']):.2e} bank={float(r['bank']):.2e} "
              f"total<=eps={r['total'] <= eps}")
        print(f"            schedules {fmt_sch(r['sch'])}; arities "
              + " ".join(f"{d}:{r['sch'][d][1]}" for d in sorted(r['sch']))
              + "; log2 S3 trials/node " + " ".join(f"{d}:{lg(v):.1f}" for d, v in sorted(r['s3_trials'].items())))
    else:
        print("   W+3      = W (no grade meets p >= 16 u_d^2 with a smaller arity)")
    st = s3_tree(p, c, g, eps)
    if st:
        r, u = st
        print(f"   S3-tree  u={u} log2Q={lg(r['Q']):8.1f} save={lg(base['Q']) - lg(r['Q']):7.1f} "
              f"log2 trials/node max={max(lg(v) for v in r['s3_trials'].values()):.1f}")
    else:
        u = max(c, max(g[d] for d in range(2, c + 1)) + 1)
        print(f"   S3-tree  not applicable (u={u}, needs p >= {16 * u * u})")


def no_saving_scan(c, glist, pmax):
    """Primes c < p <= pmax at which W saves nothing over S1-paper, and over S1-gcd."""
    g = {d + 1: glist[d] for d in range(c)}
    none_paper, none_gcd = [], []
    for p in sympy.primerange(c + 1, pmax + 1):
        qp = budget_worst_case(p, c, g, F(1, 3), "S1-paper")["Q"]
        qg = budget_worst_case(p, c, g, F(1, 3), "S1-gcd")["Q"]
        qw = budget_worst_case(p, c, g, F(1, 3), "W")["Q"]
        assert qw <= qg <= qp
        if qw == qp:
            none_paper.append(p)
        if qw == qg:
            none_gcd.append(p)
    return none_paper, none_gcd


def arity_order_check():
    """Schedule 2 arity < B_kappa(a) whenever kappa >= 2 (so W never prefers S1 where S2 is valid)."""
    for k in range(2, 13):
        for a in range(1, 200):
            assert s2_arity(k, a) < B(k, a), (k, a)
            assert B(k, a) <= B(min(12, 2 * k), a)
    for d in range(1, 13):
        for k in [x for x in range(1, d + 1) if d % x == 0]:
            for a in range(1, 60):
                assert B(k, a) <= B(d, a)
    print("arity order: (a+1)((k-1)a+1) < B_k(a) for 2<=k<=12, a<200; B_k(a) <= B_d(a) for k | d <= 12: OK")


def zero_sum_obstruction():
    """thm:power-sde (iii): at kappa = p-1 witnesses are nonempty zero-sum subsequences.
    The multiset {e_j x (p-1) : j <= a} has no nonempty zero-sum subsequence, so a worst-case
    schedule needs M >= a(p-1)+1 = D(C_p^a) columns (Olson); checked by brute force."""
    from itertools import product
    for p, a in [(3, 1), (3, 2), (3, 3), (5, 1), (5, 2), (7, 1), (7, 2)]:
        cols = [tuple(1 if i == j else 0 for i in range(a)) for j in range(a) for _ in range(p - 1)]
        ok = True
        for y in product((0, 1), repeat=len(cols)):  # s_i^{p-1} in {0,1}
            if any(y) and all(sum(y[i] * cols[i][r] for i in range(len(cols))) % p == 0 for r in range(a)):
                ok = False
                break
        print(f"   p={p} d=kappa={p - 1} a={a}: {len(cols)} columns, no nonzero witness: {ok}; "
              f"D(C_p^a)={a * (p - 1) + 1}; S1 arity B_kappa(a)=2^{lg(B(p - 1, a)):.1f}; "
              f"S2 condition p>=16k^(2k+2): {s2_ok(p, p - 1)}")
        assert ok


def s3_without_prime_condition():
    """Remark only: the Schedule-3 second-moment bound holds at every p; p >= 16u^2 only fixes M = 4u.
    Smallest M with the public bank bound <= 1/64 at a <= g, and the per-trial acceptance floor."""
    for p, d, g in [(5, 4, 1), (5, 4, 3), (5, 2, 3), (7, 3, 3), (7, 6, 2), (11, 2, 6), (11, 5, 3)]:
        k = gcd(d, p - 1)
        M = 1
        while bank_bound(p, k, g, M) > F(1, 64):
            M += 1
        h = (p - 1) // k
        acc = F((h + 1) ** M - 1, 2 * p ** M)
        print(f"   p={p} d={d} kappa={k} g={g}: M={M} (worst-case floor kappa*g+1={k * g + 1}, "
              f"16u^2 condition {s3_ok(p, k, g)}); log2 acceptance floor={lg(acc):.1f}")


def m_exponent(p, c):
    """Exponent of m in Q under W with g_d = m at every grade: 1 + sum_d e_d."""
    e = 1
    for d in range(2, c + 1):
        k = gcd(d, p - 1)
        e += 2 if s2_ok(p, k) else (1 if k == 1 else k * k.bit_length())
    return e


def sup_exponent(c):
    """sup over primes p > c of the W exponent. It is attained at kappa_d = d for all d (p = 1 mod lcm(2..c))
    at the smallest such prime, because the exponent only falls as p passes thresholds."""
    L = 1
    for d in range(2, c + 1):
        L = L * d // gcd(L, d)
    p = 1 + L
    while not sympy.isprime(p):
        p += L
    paper = 1 + sum(d * d.bit_length() for d in range(2, c + 1))
    # check against every prime below 2*10^5 (covers the kappa=2,3 thresholds)
    worst = max(m_exponent(q, c) for q in sympy.primerange(c + 1, 200000))
    assert worst == m_exponent(p, c) or worst <= m_exponent(p, c)
    return paper, p, m_exponent(p, c), worst


if __name__ == "__main__":
    eps = F(1, 3)
    g9 = [19, 17, 16, 14, 12, 9, 6, 3, 1]
    print("== check: S1-paper at the class-9 profile reproduces main.tex (20 samples, Q <= 2^1573, N_instr <= 2^1570)")
    r = budget_worst_case(11, 9, {d + 1: g9[d] for d in range(9)}, eps, "S1-paper")
    print(f"   S={r['S']} ceil log2 Q={clog2(r['Q'])} ceil log2 Ninstr={clog2(r['Ninstr'])}")
    assert r["S"] == 20 and clog2(r["Q"]) == 1573 and clog2(r["Ninstr"]) == 1570
    arity_order_check()

    print("\n== class-9 profile (rees_hsp_reduction.json), eps = 1/3")
    p_all = sympy.nextprime(16 * 9 ** 20)
    while (p_all - 1) % 2520:
        p_all = sympy.nextprime(p_all)
    for p in [11, 13, 31, 1031, 2521, 5281, 105019, 2 ** 31 - 1, 2 ** 61 - 1, p_all, 2 ** 127 - 1]:
        report("class 9", p, 9, g9, eps)
    report("class 9, eps=1e-6", 2 ** 61 - 1, 9, g9, F(1, 10 ** 6))

    print("\n== small cases")
    for c, gl, ps in [(2, [4, 3], [3, 5, 7, 1031]), (3, [6, 4, 2], [5, 7, 11, 13, 1031, 105019]),
                      (4, [8, 5, 3, 1], [5, 7, 13, 1033]), (5, [10, 7, 5, 3, 1], [7, 11, 31, 1031])]:
        for p in ps:
            if sympy.isprime(p) and p > c:
                report(f"c={c}", p, c, gl, eps)

    print("\n== primes where W saves nothing")
    for c, gl, pmax in [(9, g9, 3000), (3, [6, 4, 2], 3000), (2, [4, 3], 3000)]:
        np_, ng = no_saving_scan(c, gl, pmax)
        print(f"   c={c} g={tuple(gl)} primes <= {pmax}: no saving over S1-paper at {np_[:40]}"
              f"{' ...' if len(np_) > 40 else ''} ({len(np_)} primes)")
        print(f"      no saving over S1-gcd at {len(ng)} primes, largest {max(ng) if ng else None}; "
              f"first prime with a saving over S1-gcd: "
              f"{min(set(sympy.primerange(c + 1, pmax + 1)) - set(ng)) if len(ng) < len(list(sympy.primerange(c + 1, pmax + 1))) else None}")

    print("\n== query exponent in m (g_d = m), worst prime: paper Schedule 1 vs W")
    for c in range(2, 10):
        paper, p0, e0, worst = sup_exponent(c)
        print(f"   c={c}: paper {paper}; W at first prime p=1 mod lcm(2..c), p={p0}: {e0}; max over primes < 2e5: {worst}")

    print("\n== thm:power-sde (iii) zero-sum obstruction (kappa = p-1)")
    zero_sum_obstruction()
    print("\n== remark: Schedule 3 bank bound without p >= 16u^2 (exponential classical time; not part of the rule)")
    s3_without_prime_condition()
    sys.stdout.flush()

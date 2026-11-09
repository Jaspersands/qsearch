"""Exact budget of the free-coordinate kernel sampler (FCS) inside the Rees composition.

Companion to research/audits/reviews/2026-11-02-rees-schedule3-cost.md.  Reuses the Rule-W and
old Schedule-3 (W+3) budgets of ../2026-11-02-rees-schedules/combined/combined_budget.py.

Per grade d (kappa = gcd(d, p-1), h = (p-1)/kappa, q = (h+1)/p, worst-case hidden a <= g_d):
  FCS-k : k public coordinate blocks g_d = g_1 + ... + g_k; level j is an FCS node of dimension
          bound g_j with arity M_j; the grade arity is M_1 * ... * M_k.  Needs h >= 2 and the
          i.i.d. uniform label law.  Per-node bank bound beta(n0, M) = 4/(h^(n0-1) q^g) +
          (p^g - 1)/((p-1) p^(M-n0)); trial cap ceil(2 ln2 B / q^g).
Rule W+FCS(T): per grade, the smallest arity among Rule W's option and every FCS-k (k = 1..3)
  whose worst-case trial cap per grade node is <= T.  Error split (union bound, no restarts):
  rank eps/3; S2 Las Vegas eps/9; FCS bank events eps/9; FCS caps (trials, roots, fair-bit
  field sampling: three events of probability <= 2^-B per level node) eps/9;
  approximation eps/3.
"""
from fractions import Fraction as F
from math import gcd, log, log2
import os
import sys

import sympy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "2026-11-02-rees-schedules", "combined"))
import combined_budget as cb  # noqa: E402

LN2_UP = F(6931471805599454, 10 ** 16)


def lg(x):
    return cb.lg(x)


def fcs_level(p, k, gdim, tau):
    """Smallest arity M (and its n0) for one FCS node of dimension bound gdim with bank bound <= tau."""
    h = (p - 1) // k
    q = F(h + 1, p)
    best = None
    piv_num = F(p ** gdim - 1, p - 1)
    for n0 in range(1, 400):
        bank = 4 / (F(h) ** (n0 - 1) * q ** gdim)
        if bank >= tau:
            continue
        L = gdim
        while bank + piv_num / F(p) ** L > tau:
            L += 1
        M = L + n0
        if best is None or M < best[0]:
            best = (M, n0, bank + piv_num / F(p) ** L)
        if best and n0 > best[0]:
            break
    return best


def trial_cap(p, k, gdim, B):
    h = (p - 1) // k
    q = F(h + 1, p)
    x = 2 * LN2_UP * B / q ** gdim
    return x.numerator // x.denominator + (1 if x.denominator > 1 else 0)


def split(g, kk):
    base, extra = divmod(g, kk)
    return [base + (1 if j < extra else 0) for j in range(kk)]


def fcs_grade(p, k, g, kk, tau, B):
    """FCS-kk at one grade node: returns (arity, bank bound, trial cap, levels)."""
    dims = [x for x in split(g, kk) if x > 0]
    levels = []  # from the top level (one node) down to level one (many nodes)
    mult = 1
    tot_bank = F(0)
    tot_trials = 0
    for gdim in reversed(dims):
        res = fcs_level(p, k, gdim, F(tau) / (len(dims) * mult))
        M, n0, b = res
        levels.append((gdim, M, n0, mult))
        tot_bank += mult * b
        tot_trials += mult * trial_cap(p, k, gdim, B)
        mult *= M
    return mult, tot_bank, tot_trials, list(reversed(levels))


def budget(p, c, glist, eps, T=None, B=None, kmax=3):
    """Rule W+FCS(T) budget.  B (the per-node cap exponent) is fixed by iteration."""
    g = {d + 1: glist[d] for d in range(c)}
    m = g[1]
    t = 0
    while F(p) ** t < 3 / eps:
        t += 1
    S = m + t
    w = cb.choose("W", p, c, g)
    Bguess = 1 if B is None else B
    for _ in range(12):
        sch, n, acc = {}, {}, 1
        for d in range(2, c + 1):
            n[d] = acc
            k = gcd(d, p - 1)
            h = (p - 1) // k
            best = (w[d][1], w[d][0], None)
            if k >= 2 and h >= 2:
                tau = eps / 9 / ((c - 1) * S * n[d])
                for kk in range(1, kmax + 1):
                    if kk > g[d]:
                        break
                    M, bank, trials, levels = fcs_grade(p, k, g[d], kk, tau, Bguess)
                    if T is not None and trials > T:
                        continue
                    if M < best[0]:
                        best = (M, f"FCS{kk}", dict(bank=bank, trials=trials, levels=levels))
            sch[d] = best
            acc *= best[0]
        P = acc
        # number of FCS level-nodes (each has a trial cap and a root-extraction cap)
        Nfcs = S * sum(n[d] * sum(l[3] for l in sch[d][2]["levels"]) for d in sch if sch[d][2])
        Bnew = cb.clog2(27 * Nfcs / eps) if Nfcs else 1
        if Bnew <= Bguess:
            break
        Bguess = Bnew
    B = Bguess
    # recompute trial caps at the final B (arity choice does not depend on B)
    for d in sch:
        if sch[d][2]:
            k = gcd(d, p - 1)
            sch[d][2]["trials"] = sum(l[3] * trial_cap(p, k, l[0], B) for l in sch[d][2]["levels"])
    NS2 = S * sum(n[d] for d in sch if sch[d][1] == "S2")
    kcap = cb.clog2(9 * NS2 / eps) if NS2 else 0
    Nmerge = S * sum(n.values())
    Ninstr = S * P + Nmerge + S
    rank = F(p ** m - 1, (p - 1) * p ** S)
    s2 = NS2 * F(1, 2 ** kcap) if NS2 else F(0)
    bank = S * sum(n[d] * sch[d][2]["bank"] for d in sch if sch[d][2])
    arith = 3 * Nfcs * F(1, 2 ** B) if Nfcs else F(0)
    approx = eps / 3
    total = rank + s2 + bank + arith + approx
    assert rank <= eps / 3 and s2 <= eps / 9 and bank <= eps / 9 and arith <= eps / 9 and total <= eps
    trials_total = S * sum(n[d] * sch[d][2]["trials"] for d in sch if sch[d][2])
    maxnode = max([sch[d][2]["trials"] for d in sch if sch[d][2]] or [0])
    return dict(sch=sch, S=S, P=P, Q=c * S * P, B=B, NS2=NS2, kcap=kcap, Ninstr=Ninstr, rank=rank,
                s2=s2, bank=bank, arith=arith, total=total, trials_total=trials_total, maxnode=maxnode, n=n)


def old_w3(p, c, glist, eps):
    g = {d + 1: glist[d] for d in range(c)}
    w3 = cb.choose("W+3", p, c, g)
    if not any(s == "S3" for s, _ in w3.values()):
        return None
    r = cb.budget_restart(p, c, g, eps, w3)
    return r


def fmt(sch):
    out = []
    for d in sorted(sch):
        M, name, info = sch[d]
        if info and len(info["levels"]) > 1:
            out.append(f"{d}:{name}({'x'.join(str(l[1]) for l in info['levels'])})")
        else:
            out.append(f"{d}:{name}:{M}" if M < 10 ** 6 else f"{d}:{name}:2^{lg(M):.0f}")
    return " ".join(out)


def report(label, p, c, glist, eps):
    g = {d + 1: glist[d] for d in range(c)}
    print(f"\n-- {label}: c={c} g={tuple(glist)} p={p} eps={eps}")
    print("   kappa_d: " + " ".join(f"{d}:{gcd(d, p - 1)}" for d in range(2, c + 1)))
    W = cb.budget_worst_case(p, c, g, eps, "W")
    print(f"   W         log2Q={lg(W['Q']):7.1f}  (worst case, no label law)")
    o = old_w3(p, c, glist, eps)
    if o:
        mx = max(lg(v) for v in o["s3_trials"].values())
        print(f"   W+3 (old) log2Q={lg(o['Q']):7.1f}  max log2 trials/node={mx:6.1f}  arities "
              + " ".join(f"{d}:{o['sch'][d][1]}" for d in sorted(o['sch'])))
    else:
        print("   W+3 (old) not applicable (no grade with p >= 16u^2 and a smaller arity)")
    rows = []
    for T in [None, 2 ** 40, 2 ** 30, 2 ** 20]:
        r = budget(p, c, glist, eps, T=T)
        rows.append(r)
        tl = "inf" if T is None else f"2^{lg(T):.0f}"
        print(f"   W+FCS(T<={tl:>4s}) log2Q={lg(r['Q']):7.1f}  max log2 trials/node={lg(r['maxnode']) if r['maxnode'] else 0:6.1f}  "
              f"log2 total trials={lg(r['trials_total']) if r['trials_total'] else 0:6.1f}  B={r['B']}  "
              f"err: rank {float(r['rank']):.1e} S2 {float(r['s2']):.1e} bank {float(r['bank']):.1e} "
              f"caps {float(r['arith']):.1e} total<=eps {r['total'] <= eps}")
        print(f"        {fmt(r['sch'])}")
    return W, o, rows


def single_node_table():
    """Per-node comparison at fixed (p, kappa, g): old trials 4 kappa^(4u) B vs FCS-1 cap, at B = 40."""
    print("\n== single node, B = 40: old Schedule 3 (M = 4u, 4 kappa^M B trials) vs FCS-1 (bank bound <= 2^-60)")
    p = 194522647344910884721
    for k, gd in [(2, 17), (3, 16), (4, 14), (5, 12), (6, 9), (7, 6), (8, 3), (9, 1)]:
        u = max(2, k, gd + 1)
        old = 4 * k ** (4 * u) * 40
        M, n0, b = fcs_level(p, k, gd, F(1, 2 ** 60))
        cap = trial_cap(p, k, gd, 40)
        print(f"   kappa={k} g={gd:2d}: old M={4 * u:3d} log2 trials={lg(old):6.1f} | FCS-1 M={M:3d} (n0={n0}) "
              f"log2 cap={lg(cap):5.1f} log2 kappa^g={lg(F(k) ** gd):5.1f}")


def small_prime_table():
    """FCS-1 at small primes (the 16u^2 condition is not needed; h >= 2 is)."""
    print("\n== FCS-1 at small primes (single node, bank bound <= 1/64): arity and log2 trial cap at B = 20")
    for p, d, gd in [(5, 2, 3), (5, 4, 1), (7, 3, 3), (7, 2, 6), (7, 6, 2), (11, 2, 6), (11, 5, 3), (13, 4, 4),
                     (13, 6, 3), (31, 3, 8)]:
        k = gcd(d, p - 1)
        h = (p - 1) // k
        if h < 2:
            print(f"   p={p} d={d} kappa={k} g={gd}: h = 1 (zero-sum case kappa = p-1), FCS does not apply")
            continue
        M, n0, b = fcs_level(p, k, gd, F(1, 64))
        print(f"   p={p:2d} d={d} kappa={k} g={gd}: FCS-1 M={M:3d} (n0={n0}; worst-case floor kappa*g+1={k * gd + 1}; "
              f"IS arity B_kappa(g)=2^{lg(cb.B(k, gd)):.1f}); log2 cap={lg(trial_cap(p, k, gd, 20)):5.1f}")


def drop_in_check(p, c, glist, eps):
    """Theorem part (ii): main.tex's hypotheses (p >= 16u^2, M = 4u, u = max(c, max g_d + 1)) with the
    FCS sampler and n0 = 2u + 1.  Exact per-tree bank sum (a_d <= g_d) and per-node trial caps."""
    g = {d + 1: glist[d] for d in range(c)}
    u = max(c, max(g[d] for d in range(2, c + 1)) + 1)
    if p < 16 * u * u:
        return None
    M = 4 * u
    n0 = 2 * u + 1
    nodes = sum((4 * u) ** (d - 2) for d in range(2, c + 1))
    B = cb.clog2(64 * (4 * u) ** (c - 1))
    bank = F(0)
    caps = {}
    for d in range(2, c + 1):
        k = gcd(d, p - 1)
        h = (p - 1) // k
        q = F(h + 1, p)
        nd = (4 * u) ** (d - 2)
        bank += nd * (4 / (F(h) ** (n0 - 1) * q ** g[d]) + F(p ** g[d] - 1, (p - 1) * p ** (M - n0)))
        caps[d] = (trial_cap(p, k, g[d], B), 4 * k ** M * B)
    assert bank <= F(1, 64)
    mx_new = max(v[0] for v in caps.values())
    mx_old = max(v[1] for v in caps.values())
    print(f"   p={p}: u={u} M=4u={M} n0={n0} nodes/tree={nodes} B={B}: log2 bank sum per tree {lg(bank):.1f} <= -6; "
          f"max log2 trials/node FCS {lg(mx_new):.1f} vs old 4 kappa^M B {lg(mx_old):.1f}")


def generic_u_check():
    """Proof inequality of part (ii): (4u)^(u-1) * (4 * 15^(-2u) u^(-u-1) + 2 (16u^2)^(-u-1)) <= 1/64."""
    for u in range(2, 61):
        val = F(4 * u) ** (u - 1) * (4 * F(1, 15 ** (2 * u) * u ** (u + 1)) + 2 * F(1, (16 * u * u) ** (u + 1)))
        assert val <= F(1, 64), u
    print("   (4u)^(u-1) (4*15^(-2u) u^(-u-1) + 2 (16u^2)^(-u-1)) <= 1/64 for 2 <= u <= 60: OK (exact)")


if __name__ == "__main__":
    eps = F(1, 3)
    g9 = [19, 17, 16, 14, 12, 9, 6, 3, 1]
    single_node_table()
    small_prime_table()
    print("\n== part (ii) drop-in: main.tex hypotheses, M = 4u, n0 = 2u+1, class-9 profile")
    generic_u_check()
    p_all0 = sympy.nextprime(16 * 9 ** 20)
    while (p_all0 - 1) % 2520:
        p_all0 = sympy.nextprime(p_all0)
    for p in [5281, 105019, 2 ** 31 - 1, 2 ** 61 - 1, p_all0, 2 ** 127 - 1]:
        drop_in_check(p, 9, [19, 17, 16, 14, 12, 9, 6, 3, 1], F(1, 3))
    print("\n== class-9 profile, eps = 1/3")
    p_all = sympy.nextprime(16 * 9 ** 20)
    while (p_all - 1) % 2520:
        p_all = sympy.nextprime(p_all)
    for p in [11, 13, 31, 1031, 2521, 5281, 105019, 2 ** 31 - 1, 2 ** 61 - 1, p_all, 2 ** 127 - 1]:
        report("class 9", p, 9, g9, eps)
    report("class 9, eps=1e-6", 2 ** 61 - 1, 9, g9, F(1, 10 ** 6))
    print("\n== small cases")
    for c, gl, ps in [(2, [4, 3], [5, 7, 1031]), (3, [6, 4, 2], [7, 13, 1031, 105019]),
                      (4, [8, 5, 3, 1], [7, 13, 1033]), (5, [10, 7, 5, 3, 1], [11, 31, 1031])]:
        for p in ps:
            report(f"c={c}", p, c, gl, eps)
    sys.stdout.flush()

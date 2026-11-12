"""Checks of Lemma 3.2 (lem:homogeneous), Prop 3.4 (prop:single-evaluation) and
Remark 3.5 (rem:fewer-points), linear-algebra level, for EVERY Lie subalgebra hh of
small algebras (exhaustive where feasible), every point set of the relevant size, and
every dilation.

For each hh:
  H1  hlift (from intersections only) == P_S := cap_{s in S} E_s^{-1}(hh) for every
      c-subset S of F_p^x   (Lemma 3.2, first expression)
  H2  hlift == cap_{s in F_p^x} E_s^{-1}(hh)                        (second expression)
  H3  hlift is a Lie subalgebra of A and delta_theta-stable for all theta (Lemma 3.2)
  H4  for every k < c and every k-subset S: [all dilations preserve P_S] <=> [gamma_{k+1} <= hh],
      and in that case P_S == hlift                                (Remark 3.5)
  H5  for every s, theta != 1: delta_theta preserves E_s^{-1}(hh) <=> gamma_2 <= hh  (Prop 3.4)
  H6  negative controls: a c-tuple containing 0, or with a repeated point, gives P != hlift
      for hh = 0 whenever the true class is c >= 2.
  H7  (single theta, k>=2) count of (hh,S,theta!=1) with delta_theta preserving P_S although
      gamma_{k+1} not in hh  -- shows that Remark 3.5 needs "every dilation".
"""
import random, sys, time
from itertools import combinations
from lie import *


def stable(cov, B, th):
    return all(in_span(cov.dil_coords(th, b), B, cov.p) for b in B) if B else True


def subalgebra_cov(cov, B):
    els = [cov.from_coords(b) for b in B]
    for x in els:
        for y in els:
            if not elem_in_coords_space(cov, cov.br(x, y), B):
                return False
    return True


def check_alg(L, exhaustive=True, nrand=300, rng=None, max_sets=None):
    p, c = L.p, L.c
    cov = Cover(L)
    units = list(range(1, p))
    if exhaustive:
        subs = (B for B in all_subspaces(L.m, p) if L.is_subalgebra(B))
    else:
        def gen():
            yield []
            for k in range(1, c + 1):
                yield L.gam(k)
            for _ in range(nrand):
                g = rng.randrange(1, 4)
                yield L.closure([[rng.randrange(p) for _ in range(L.m)] for _ in range(g)])
        subs = gen()
    stats = dict(H1=0, H2=0, H3=0, H4=0, H5=0, H7_single_theta_preserves=0, nsub=0)
    fails = []
    csets = list(combinations(units, c))
    if max_sets and len(csets) > max_sets:
        csets = rng.sample(csets, max_sets)
    for hh in subs:
        hh = span_basis(hh, p) if hh else []
        stats["nsub"] += 1
        hl = cov.hlift_coords(hh)
        # H1
        for S in csets:
            P = cov.pullback_coords(hh, S)
            if not same_space(P, hl, p) or len(P) != len(hl):
                fails.append(("H1", hh, S))
            else:
                stats["H1"] += 1
        # H2
        Pall = cov.pullback_coords(hh, units)
        if same_space(Pall, hl, p) and len(Pall) == len(hl):
            stats["H2"] += 1
        else:
            fails.append(("H2", hh))
        # H3
        if subalgebra_cov(cov, hl) and all(stable(cov, hl, th) for th in units):
            stats["H3"] += 1
        else:
            fails.append(("H3", hh))
        # H4
        for k in range(1, c):
            cond = all(in_span(v, hh, p) for v in L.gam(k + 1)) if hh else not L.gam(k + 1)
            ksets = list(combinations(units, k))
            if max_sets and len(ksets) > max_sets:
                ksets = rng.sample(ksets, max_sets)
            for S in ksets:
                P = cov.pullback_coords(hh, S)
                alls = all(stable(cov, P, th) for th in units)
                ok = (alls == cond) and (not cond or (same_space(P, hl, p) and len(P) == len(hl)))
                if ok:
                    stats["H4"] += 1
                else:
                    fails.append(("H4", hh, S, alls, cond))
                if k >= 2 and not cond:
                    stats["H7_single_theta_preserves"] += sum(1 for th in units[1:] if stable(cov, P, th))
        # H5
        cond2 = all(in_span(v, hh, p) for v in L.gam(2)) if hh else not L.gam(2)
        for s in units:
            P = cov.pullback_coords(hh, [s])
            for th in units[1:]:
                if stable(cov, P, th) == cond2:
                    stats["H5"] += 1
                else:
                    fails.append(("H5", hh, s, th))
    # H6 negative controls (hh = 0)
    neg = {}
    if c >= 2:
        S0 = [0] + list(range(1, c))
        Srep = [1] * 2 + list(range(2, c))
        for name, S in (("with0", S0), ("repeat", Srep)):
            P = cov.pullback_coords([], S)
            neg[name] = (len(P), len(cov.hlift_coords([])))
    return stats, fails, neg


def main():
    rng = random.Random(7)
    plan = [
        (heisenberg(3), True, None), (heisenberg(5), True, None), (heisenberg(7), True, None),
        (free23(5), True, None),
        (filiform(5, 5), True, None),            # class 4, p = 5 = c+1 edge case
        (free32(3), False, None), (free32(5), False, None),
        (free23(7), False, None),
        (filiform(7, 7), False, 6),               # class 6, p = 7 = c+1 edge case
        (dixmier_lister(5), False, None), (dixmier_lister(7), False, 8),
    ]
    total_fail = 0
    for L, exh, ms in plan:
        t0 = time.time()
        stats, fails, neg = check_alg(L, exhaustive=exh, nrand=200, rng=rng, max_sets=ms)
        total_fail += len(fails)
        print(L.name, "p=%d" % L.p, "class=%d" % L.c, "exhaustive" if exh else "random+adversarial",
              stats, "fails=%d" % len(fails), "neg(dimP,dimhlift)=", neg, "%.1fs" % (time.time() - t0))
        for f in fails[:5]:
            print("   FAIL", f)
        sys.stdout.flush()
    print("TOTAL FAILURES:", total_fail)


if __name__ == "__main__":
    main()

"""Exact-circuit family EC: ALG-T leaf, control fan-in, single-pass success of plain (Lemma 2)
and lookahead back substitution, and (small r) the EXACT success probability over t in P^r.

Since every e_l = 0, tau_{l-1} = Pi_{l-1}(tau_l): the s-draws do not affect lower levels, and a
pass succeeds iff every level's Good set is nonempty at the offsets of tau_L = -sum t_s sigma_s.
So the success probability is a function of t only; exact = enumeration of P^r.

Usage: ec_test.py kappa J p Lmax passes seed [Lmin step nopad]
nopad=1: no padding and no end-to-end ALG-T run (the padding comes after the circuits and is
never scanned by the forward pass, so the leaf is the same; used for large L).
"""
import itertools
import random
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa
import subquad_u as SQ  # noqa
from families_u import ec_bank  # noqa
from lookahead import Ctl  # noqa

k, J, p, Lmax, passes, seed = map(int, sys.argv[1:7])
Lmin = int(sys.argv[7]) if len(sys.argv) > 7 else 2
step = int(sys.argv[8]) if len(sys.argv) > 8 else (2 if Lmax > 8 else 1)
nopad = len(sys.argv) > 9 and sys.argv[9] == '1'
rng = random.Random(seed)
Fd = SQ.Field(p, k)
Par = SQ.Params(J, k)


def exact_success(ctl):
    """Fraction of t in P^{src} for which every level has nonempty Good (valid since e = 0)."""
    assert all(not any(c) for c in ctl.ce)
    C = np.array(ctl.cs, dtype=np.int64)          # nsrc x n  (coordinates of sources)
    Pv = np.array(Fd.P, dtype=np.int64)
    nsrc = C.shape[0]
    tables = []
    for R in ctl.rounds:
        nb = len(R.blocks)
        tab = np.zeros((p,) * (nb - 1), dtype=bool)
        for beta in itertools.product(range(p), repeat=nb - 1):
            tab[beta] = len(ctl.good_set([0] + list(beta), R.bclass)) > 0
        tables.append(tab)
    tot = ok = 0
    # enumerate t in chunks over the first few sources
    rest = nsrc - min(nsrc, 6)
    head = list(itertools.product(range(len(Pv)), repeat=nsrc - rest))
    for tail in itertools.product(range(len(Pv)), repeat=rest):
        T = np.array([list(h) + list(tail) for h in head], dtype=np.int64)
        tv = Pv[T]                                  # N x nsrc
        tau = (-(tv @ C)) % p                       # N x n
        good = np.ones(len(T), dtype=bool)
        for R, tab in zip(ctl.rounds, tables):
            idx = tuple(tau[:, R.start + i] for i in range(R.end - R.start))
            good &= tab[idx]
        tot += len(T)
        ok += int(good.sum())
    return ok / tot


print("kappa=%d J=%d p=%d  EC family, budget M = F(r)" % (k, J, p), flush=True)
for L in range(Lmin, Lmax + 1, step):
    r = (J - 1) * L
    M = Par.F(r) if not nopad else r + J * L
    cols = ec_bank(rng, Fd, J, L, M)
    st = SQ.init_state(Fd, cols)
    status = SQ.forward_fast(Fd, cols, J, rng, st, rule="first")
    assert status == "ok", status
    rounds, Ub, B = st["rounds"], st["Ub"], st["B"]
    assert len(rounds) == L and all(not any(R.e) for R in rounds)
    ctl = Ctl(Fd, cols, rounds, Ub, B)
    sm = ctl.summary()
    res = {}
    for mode in ("plain", "look"):
        succ = 0
        for _ in range(passes):
            x, ev = ctl.backward(rng, mode)
            if x is not None:
                assert SQ.check(Fd, cols, x)
                succ += 1
        res[mode] = succ / passes
    ex = exact_success(ctl) if (len(Fd.P) ** r <= 3 * 10 ** 6) else None
    # ALG-T end to end with 30 passes, lookahead mode
    if nopad:
        xx, leafkind = 0, "not run (nopad)"
    else:
        stt = SQ.new_stats()
        SQ.LEAF_MODE[0] = "look"
        xx = SQ.solve_T(Fd, cols, Par, rng, stt)
        leafkind = [kk for kk in stt if kk.startswith("leaf:")]
    print("L=%2d r=%2d M=%4d rho=%3d N_lev=%d N_src=%3d src_ctrl=%3d | plain %.3f look %.3f exact %s"
          " | ALG-T(30 look passes): %s %s"
          % (L, r, M, sm["rho"], sm["N_lev"], sm["N_src"], sm["src_ctrl"], res["plain"], res["look"],
             "%.4f" % ex if ex is not None else "-", ("solved" if xx is not None else "UNSOLVED") if not nopad else "-",
             leafkind), flush=True)

"""ALG-Q1: SSS(E) with swaps, plus Lemma A (closed prefix), Lemma T (top circuit at
codimension <= E-1), Lemma R (absorption, cap extra blocks per round) and recursion on the
flats U+ (span of all non-free columns and the free columns inside U_L) and Y.
Records which mechanism solved each bank, and classifies unresolved stalls."""
import random
from q1core import (Field, rank, solve_in_span, check, D, forward, init_state, free_cols,
                    in_span, try_closure, try_top, absorb, rebuild, run_backward, restrict_cols)


def classify(Fd, cols, st):
    p = Fd.p
    r = len(st["B"])
    Ub = st["Ub"]
    u = len(Ub)
    Fr = free_cols(len(cols), st["rounds"])
    Rcols = [i for R in st["rounds"] for i in R.S]
    Rout = [i for i in Rcols if not in_span(Ub, cols[i], p)]
    Fin = [i for i in Fr if in_span(Ub, cols[i], p)]
    X = [i for i in Fr if not in_span(Ub, cols[i], p)]
    b = rank([cols[i] for i in st["B"] if in_span(Ub, cols[i], p)], p)[0]
    y = rank([cols[i] for i in Fin], p)[0]
    Uplus_gen = [cols[i] for i in Rcols] + [cols[i] for i in Fin]
    uplus = rank(Uplus_gen, p)[0]
    return dict(r=r, q=r - u, qplus=r - uplus, eps=u - y, b=b, X=len(X), pi=len(st["pool"]),
                Rout_rank=rank(Ub + [cols[i] for i in Rout], p)[0] - u, M=len(cols))


def solve(Fd, cols, E, rng, passes=12, cap=1, depth=0, log=None, use_top=True,
          use_absorb=True, use_rec=True, order=None):
    p = Fd.p
    n = len(cols)
    log = log if log is not None else []
    for i, c in enumerate(cols):
        if not any(c):
            x = [0] * n
            x[i] = 1
            return x, "zero"
    r = rank(cols, p)[0]
    st = init_state(Fd, cols, order)

    def snap(s):
        Ub = s["Ub"]
        x = try_closure(Fd, cols, s["rounds"], Ub, rng, passes)
        if x is not None:
            s["how"] = "closure@t"
            return x
        if use_top and 1 <= r - len(Ub) <= E - 1:
            x = try_top(Fd, cols, s["rounds"], Ub, E, rng, passes)
            if x is not None:
                s["how"] = "top@t"
                return x
        return None

    while True:
        status = forward(Fd, cols, E, rng, st, snap=snap)
        if status == "direct":
            assert check(Fd, cols, st["x"])
            return st["x"], "direct"
        if status == "snap":
            return st["x"], st["how"]
        if status == "ok":
            x = run_backward(Fd, cols, st["rounds"], st["Ub"], st["B"], rng, passes)
            if x is not None:
                return x, "thm2" + ("+absorb" if any(getattr(R, "extra", 0) for R in st["rounds"]) else "")
            return None, "emptyGood"
        # stall
        Ub = st["Ub"]
        x = try_closure(Fd, cols, st["rounds"], Ub, rng, passes)
        if x is not None:
            return x, "closure@stall"
        if use_top:
            x = try_top(Fd, cols, st["rounds"], Ub, E, rng, passes)
            if x is not None:
                return x, "top@stall"
        if use_absorb:
            g = absorb(Fd, cols, st["rounds"], cap)
            if g:
                st["Ub"] = rebuild(Fd, st["rounds"])
                # unused columns that now lie in U go back through the scan (swap/pool)
                continue
        break
    cl = classify(Fd, cols, st)
    log.append((depth, cl))
    if use_rec:
        Ub = st["Ub"]
        Rcols = [i for R in st["rounds"] for i in R.S]
        Fin = [i for i in free_cols(n, st["rounds"]) if in_span(Ub, cols[i], p)]
        gens = rank([cols[i] for i in Rcols + Fin], p)[1]
        cand = []
        if len(gens) < r:
            cand.append(("U+", [i for i in range(n) if in_span(gens, cols[i], p)]))
        Yg = rank([cols[i] for i in Fin], p)[1]
        if Yg:
            cand.append(("Y", [i for i in range(n) if in_span(Yg, cols[i], p)]))
        for name, idx in cand:
            sc = restrict_cols(idx, cols, p)
            rk = len(sc[0]) if sc else 0
            if rk >= r or len(idx) < D(rk, E) + rk:
                continue
            y, how = solve(Fd, sc, E, rng, passes, cap, depth + 1, log, use_top, use_absorb, use_rec)
            if y is not None:
                x = [0] * n
                for j, i in enumerate(idx):
                    x[i] = y[j]
                assert check(Fd, cols, x)
                return x, "rec-%s(%s)" % (name, how)
    return None, "stall(q=%d,q+=%d,eps=%d,X=%d)" % (cl["q"], cl["qplus"], cl["eps"], cl["X"])

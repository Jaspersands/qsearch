"""ALG-Q1 exactly as in the proof of Theorem Q1 (E = 3, f(r) = D_3(r) + C r, C = 3).
No snapshot shortcuts: one Theorem-2 forward pass, then the case analysis at the stall.
Every inequality used by the proof is asserted, every witness verified.  Returns
(x, trace) where trace lists (depth, case, data) and the absorption load."""
import random
from itertools import combinations
from q1core import (Field, rank, solve_in_span, check, D, forward, init_state, free_cols,
                    in_span, rebuild, run_backward, restrict_cols, mk_round, steer_bad)

E = 3
C = 3


def f(r):
    return D(r, E) + C * r if r > 0 else 0


def absorb_balanced(Fd, cols, rounds, need):
    """Absorb `need` directions (Lemma R), always into the least-loaded round available."""
    p = Fd.p
    for _ in range(need):
        Ub = rebuild(Fd, rounds)
        best = None
        for l, R in enumerate(rounds):
            for b, G in enumerate(R.blocks):
                if len(G) < 2:
                    continue
                for i in G:
                    if not in_span(Ub, cols[i], p):
                        key = getattr(R, "extra", 0)
                        if best is None or key < best[0]:
                            best = (key, l, b, i)
        if best is None:
            return False
        _, l, b, i = best
        R = rounds[l]
        G = R.blocks[b]
        blocks = R.blocks[:b] + [[j for j in G if j != i]] + R.blocks[b + 1:] + [[i]]
        R2 = mk_round(Fd, cols, R.S, R.delta, blocks)
        R2.extra = getattr(R, "extra", 0) + 1
        rounds[l] = R2
        assert rebuild(Fd, rounds) is not None, "Lemma R violated"
    return True


def top_pair(Fd, cols, rounds, Ub, rng, passes, trace, depth):
    """Lemma T at codimension 1: beta = one column of X; pairs inside X minus beta."""
    p = Fd.p
    Fr = free_cols(len(cols), rounds)
    X = [i for i in Fr if not in_span(Ub, cols[i], p)]
    beta, rest = X[0], X[1:]
    rho = sum(1 for R in rounds for b in range(len(R.blocks)) for b2 in range(b + 1, len(R.blocks))
              if R.bclass[b] != R.bclass[b2])
    nbad, good = 0, None
    pairs = list(combinations(rest, 2))
    for (a1, a2) in pairs:
        co = solve_in_span(Ub + [cols[a2]], cols[a1], p)
        assert co is not None and co[-1] != 0
        delta = {a1: 1, a2: (-co[-1]) % p}
        top = mk_round(Fd, cols, [a1, a2], delta, [[a1], [a2]])
        rr = rounds + [top]
        Ub2 = rebuild(Fd, rr)
        assert Ub2 is not None and len(Ub2) == len(Ub) + 1
        src = [i for i in Fr if i not in (a1, a2)]
        if steer_bad(Fd, cols, rr, Ub2, src):
            nbad += 1
            continue
        if good is None:
            good = (rr, Ub2, src)
    # Lemma T': with |X| >= 3 no pair is bad
    assert nbad == 0, ("Lemma T' violated", nbad, rho)
    trace.append((depth, "top-pair", dict(n=len(X), pairs=len(pairs), bad=nbad, rho=rho)))
    if good is None:
        return None
    rr, Ub2, src = good
    return run_backward(Fd, cols, rr, Ub2, src, rng, passes)


def codim1(Fd, cols, rounds, Ub, r, M, rng, passes, trace, depth):
    """Lower flag realizes a hyperplane U containing every round column (Lemma T')."""
    p = Fd.p
    Fr = free_cols(len(cols), rounds)
    Fin = [i for i in Fr if in_span(Ub, cols[i], p)]
    X = [i for i in Fr if not in_span(Ub, cols[i], p)]
    assert all(in_span(Ub, cols[i], p) for R in rounds for i in R.S)
    if rank([cols[i] for i in Fin], p)[0] == len(Ub):
        trace.append((depth, "closure", {}))
        return run_backward(Fd, cols, rounds, Ub, Fin, rng, passes)
    if len(X) >= 3:
        return top_pair(Fd, cols, rounds, Ub, rng, passes, trace, depth)
    idx = [i for i in range(M) if in_span(Ub, cols[i], p)]
    assert len(idx) == M - len(X) and len(idx) >= f(r - 1)
    trace.append((depth, "rec-U", dict(dim=r - 1, cols=len(idx))))
    return recurse(Fd, cols, idx, rng, passes, trace, depth)


def recurse(Fd, cols, idx, rng, passes, trace, depth):
    sc = restrict_cols(idx, cols, Fd.p)
    y = solve_thm(Fd, sc, rng, passes, trace, depth + 1)
    if y is None:
        return None
    x = [0] * len(cols)
    for j, i in enumerate(idx):
        x[i] = y[j]
    assert check(Fd, cols, x)
    return x


def solve_thm(Fd, cols, rng, passes=12, trace=None, depth=0):
    p = Fd.p
    M = len(cols)
    trace = [] if trace is None else trace
    for i, c in enumerate(cols):
        if not any(c):
            x = [0] * M
            x[i] = 1
            trace.append((depth, "zero", {}))
            return x
    r = rank(cols, p)[0]
    assert M >= f(r), "budget"
    st = init_state(Fd, cols)
    status = forward(Fd, cols, E, rng, st)
    if status == "direct":
        trace.append((depth, "direct", {}))
        return st["x"]
    rounds, Ub, B = st["rounds"], st["Ub"], st["B"]
    if status == "ok":
        trace.append((depth, "thm2", {}))
        return run_backward(Fd, cols, rounds, Ub, B, rng, passes)
    # ---- stall ----
    q = r - len(Ub)
    T = st["T"]
    pool = st["pool"]
    Rcols = [i for R in rounds for i in R.S]
    # Theorem 2(b) decomposition
    assert len(Rcols) <= D(r, E) - D(q, E), "round count"
    assert M == r + len(Rcols) + len(pool) + len(T)
    Fr = free_cols(M, rounds)
    Fin = [i for i in Fr if in_span(Ub, cols[i], p)]
    BinU = [i for i in B if in_span(Ub, cols[i], p)]
    b = len(BinU)
    assert rank([cols[i] for i in Fin], p)[0] == b      # pool lies in span(B cap U)
    eps = len(Ub) - b
    X = [i for i in Fr if not in_span(Ub, cols[i], p)]
    Rout = [i for i in Rcols if not in_span(Ub, cols[i], p)]
    gens = rank([cols[i] for i in Rcols + Fin], p)[1]
    qplus = r - len(gens)
    info = dict(r=r, q=q, qplus=qplus, eps=eps, b=b, X=len(X), pi=len(pool), T=len(T))
    trace.append((depth, "stall", info))
    if eps == 0:
        trace.append((depth, "closure", {}))
        return run_backward(Fd, cols, rounds, Ub, Fin, rng, passes)
    if q >= 3 and b <= q - 2:
        Yb = rank([cols[i] for i in BinU], p)[1]
        idx = [i for i in range(M) if in_span(Yb, cols[i], p)]
        assert len(idx) >= f(b), ("Y-recursion count", len(idx), f(b))
        trace.append((depth, "rec-Y", dict(dim=b, cols=len(idx))))
        return recurse(Fd, cols, idx, rng, passes, trace, depth)
    if qplus >= 2:
        Xp = [i for i in Fr if not in_span(gens, cols[i], p)]
        assert len(X) <= r - b + q <= r + 1 <= f(r) - f(r - 2)
        assert len(Xp) <= f(r) - f(r - qplus), ("U+ count", len(Xp), f(r) - f(r - qplus), info)
        idx = [i for i in range(M) if in_span(gens, cols[i], p)]
        trace.append((depth, "rec-U+", dict(dim=r - qplus, cols=len(idx))))
        return recurse(Fd, cols, idx, rng, passes, trace, depth)
    # q+ <= 1: absorb q - q+ directions, reaching U+ (Lemma R)
    trial = list(rounds)
    assert absorb_balanced(Fd, cols, trial, q - qplus)
    load = max(getattr(R, "extra", 0) for R in trial)
    if load >= 3:
        # heavy stall: first try the two recursions whose counts are checkable
        Yb = rank([cols[i] for i in BinU], p)[1]
        idxY = [i for i in range(M) if in_span(Yb, cols[i], p)]
        idxU = [i for i in range(M) if in_span(Ub, cols[i], p)]
        hinfo = dict(info, load=load, colsY=len(idxY), fY=f(b), colsU=len(idxU), fU=f(r - q),
                     Rout=len(Rout), rounds=[(len(R.S), len(R.blocks),
                     sum(1 for i in R.S if not in_span(Ub, cols[i], p))) for R in rounds])
        trace.append((depth, "heavy", hinfo))
        if len(idxY) >= f(b):
            trace.append((depth, "rec-Y", dict(dim=b, cols=len(idxY))))
            return recurse(Fd, cols, idxY, rng, passes, trace, depth)
        if len(idxU) >= f(r - q):
            trace.append((depth, "rec-U", dict(dim=r - q, cols=len(idxU))))
            return recurse(Fd, cols, idxU, rng, passes, trace, depth)
    rounds = trial
    Ub = rebuild(Fd, rounds)
    trace.append((depth, "absorb", dict(dirs=q - qplus, load=load)))
    if qplus == 0:
        assert len(Ub) == r
        return run_backward(Fd, cols, rounds, Ub, B, rng, passes)
    return codim1(Fd, cols, rounds, Ub, r, M, rng, passes, trace, depth)

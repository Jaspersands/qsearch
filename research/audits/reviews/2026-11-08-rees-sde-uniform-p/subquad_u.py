"""[COPY of ../2026-11-07-rees-sde-subquad-A/subquad.py; only leaf() changed: it records the
control fan-in of the leaf and runs the back substitution in mode LEAF_MODE (lookahead.py).]

ALG-T: the general-J reduction of Theorem A in ../2026-11-07-rees-sde-subquad-A.md.

Forward pass SSS(J) with reserved basis, swaps and true pool (q1core.forward, fixed
splitting rule "first"), then at a stall, in this order:
  case 1  eps = 0                      -> closure leaf (Lemma A)
  case 2  b <= q                       -> recursion on Y = span(B cap U)
  case 3  (b >= q+1, so r >= 2q+2)
     3.0  q+ >= 2(J-1)                 -> recursion on U+
     3.1  max absorption with capacity c per round (matroid intersection, Lemma R);
          incomplete                   -> recursion on the Rado flat W = U + span(Z)
     3.2  complete: absorb, reach U+ (codim m = q+ <= 2J-3)
          m = 0                        -> leaf (flag, B)
          closure on U+                -> leaf
          |X'| <= F(r) - F(r-m)        -> recursion on U+
          else top phase: reserve a basis Z of V/U+ inside X', singleton-block greedy
          circuits from X' minus Z; reach V -> leaf (Lemma S + Lemma T_m); stall ->
          recursion on the top realised space H_cur.
Every count inequality used by the proof is asserted (strict mode).  Every leaf is checked
for (F1)/(F2) (rebuild) and for (S) (steer_bad == 0).  Every witness is verified.

strict=False is a stress mode: the capacity c may be set below the theorem's value; then
the W-recursion is used only when its count actually holds, otherwise the absorption is
completed with unbounded capacity and the excess load is recorded.
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-05-rees-sde-q1"))
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-07-rees-sde-subquad-A"))
sys.path.insert(0, HERE)
from q1core import (Field, rank, solve_in_span, check, forward, init_state, free_cols,  # noqa
                    in_span, rebuild, run_backward, restrict_cols, mk_round, steer_bad)
import sss  # noqa  (imported by q1core)
from sss import split_blocks  # noqa
from fastla import Ech, rank_vecs  # noqa
from lookahead import Ctl  # noqa

LEAF_MODE = ["look"]   # mutable: set LEAF_MODE[0] = 'plain' or 'look'
LEAVES = []
EVAL_PASSES = [0]       # if > 0, each leaf also records success rates of both modes


# ---------------------------------------------------------------------------
# counts
# ---------------------------------------------------------------------------

_DT = {}


def DJ(q, J):
    """D_J(q): worst greedy round cost from quotient q to 0 (report section 3.1)."""
    tab = _DT.setdefault(J, [0])
    while len(tab) <= q:
        x = len(tab)
        best = x + 1 + tab[x - J + 1] if x >= J - 1 else 0
        for k in range(1, min(x, J - 2) + 1):
            best = max(best, k + 1 + tab[x - k])
        tab.append(best)
    return tab[q]


class Params:
    def __init__(self, J, kappa, c=None, C=None, strict=True, passes=30):
        assert J >= max(kappa, 2)
        self.J = J
        self.c = 2 * (J - 1) if c is None else c
        self.C = max(2, 2 * J - 4) if C is None else C
        self.strict = strict
        self.passes = passes

    def F(self, r):
        return DJ(r, self.J) + self.C * r if r > 0 else 0


# ---------------------------------------------------------------------------
# fast forward pass: same semantics as q1core.forward (cross-checked in check_fast.py)
# ---------------------------------------------------------------------------

def forward_fast(Fd, cols, E, rng, st, rule="first"):
    p, a = Fd.p, len(cols[0])
    B = st["B"]
    r = len(B)
    EU = Ech(p, a)
    for R in st["rounds"]:
        for w in R.W[1:]:
            EU.add(w, {})

    def mkEB():
        eb = Ech(p, a)
        for s_ in B:
            eb.add(cols[s_], {s_: 1})
        return eb
    EB = mkEB()
    while True:
        if len(EU) == r:
            st["Ub"] = rebuild(Fd, st["rounds"])
            return "ok"
        E2 = EU.copy()
        T, found = [], None
        for cidx in st["unused"]:
            res, co = E2.reduce(cols[cidx], track=True)
            if any(res):
                E2.add(cols[cidx], {cidx: 1})
                T.append(cidx)
                continue
            delta = {cidx: 1}
            for i in T:
                t = co.get(i, 0) % p
                if t:
                    delta[i] = (-t) % p
            found = (cidx, delta)
            break
        if found is None:
            st["T"] = T
            st["Ub"] = rebuild(Fd, st["rounds"])
            return "stall"
        cidx, delta = found
        S = sorted(delta)
        if len(S) == 1:
            st["unused"].remove(cidx)
            res, cb = EB.reduce(cols[cidx], track=True)
            assert not any(res)
            out = [B[j] for j in range(r) if cb.get(B[j], 0) % p and not EU.contains(cols[B[j]])]
            if out:
                sig = out[0]
                B[B.index(sig)] = cidx
                st["unused"].append(sig)
                st["swaps"] = st.get("swaps", 0) + 1
                EB = mkEB()
            else:
                st["pool"].append(cidx)
            continue
        for i in S:
            st["unused"].remove(i)
        e = [sum(delta[i] * cols[i][t] for i in S) % p for t in range(a)]
        if len({Fd.cls(delta[i]) for i in S}) == 1 and not any(e):
            cc = Fd.cls(delta[S[0]])
            zeta = pow(Fd.g, (-cc) % Fd.k, p)
            x = [0] * len(cols)
            for i in S:
                x[i] = zeta * delta[i] % p
            st["x"] = x
            return "direct"
        blocks = split_blocks(Fd, S, delta, E, rng, rule)
        R = mk_round(Fd, cols, S, delta, blocks)
        st["rounds"].append(R)
        for w in R.W[1:]:
            assert EU.add(w, {}), "(F1) in forward_fast"


# ---------------------------------------------------------------------------
# matroid intersection: linear matroid (mod U) x partition matroid (rounds, cap c)
# ---------------------------------------------------------------------------

def indep_mod(Ub, vecs, p):
    return rank(Ub + vecs, p)[0] == len(Ub) + len(vecs)


def rank_mod(Ub, vecs, p):
    return rank(Ub + vecs, p)[0] - len(Ub)


def matroid_intersection(Fd, cols, Ub, elems, part, cap):
    """Max common independent set I of M1 = {S : cols[S] independent mod span(Ub)} and
    M2 = {S : |S cap part^{-1}(l)| <= cap}.  Returns (I, Z) with
    |I| = r1(Z) + r2(elems minus Z) (Edmonds min-max certificate, asserted).
    Exchange graph as in Schrijver, Combinatorial Optimization, Thm 41.2."""
    p = Fd.p
    a = len(cols[0])
    I = []
    EU = Ech(p, a)
    for w in Ub:
        EU.add(w)
    resid = {i: EU.reduce(cols[i])[0] for i in elems}

    def in1(S):
        return rank_vecs([resid[i] for i in S], p, a) == len(S)

    def in2(S):
        cnt = Counter(part[i] for i in S)
        return all(v <= cap for v in cnt.values())

    while True:
        out = [x for x in elems if x not in I]
        X1 = set(x for x in out if in1(I + [x]))
        X2 = set(x for x in out if in2(I + [x]))
        adj = {v: [] for v in elems}
        for y in I:
            rest = [z for z in I if z != y]
            for x in out:
                if in1(rest + [x]):
                    adj[y].append(x)          # y -> x
                if in2(rest + [x]):
                    adj[x].append(y)          # x -> y
        # BFS shortest path X1 -> X2
        prev = {x: None for x in X1}
        frontier = list(X1)
        end = next((x for x in X1 if x in X2), None)
        while end is None and frontier:
            nf = []
            for u in frontier:
                for v in adj[u]:
                    if v not in prev:
                        prev[v] = u
                        if v in X2 and v not in I:
                            end = v
                            break
                        nf.append(v)
                if end is not None:
                    break
            frontier = nf
        if end is None:
            # R = elements reachable from X1 (no X1-X2 path, so R misses X2);
            # then r1(elems minus R) = |I minus R| and r2(R) = |I cap R|
            R = set(X1)
            st = list(X1)
            while st:
                v = st.pop()
                for u in adj[v]:
                    if u not in R:
                        R.add(u)
                        st.append(u)
            assert not (R & X2)
            Z = [x for x in elems if x not in R]
            r1 = rank_vecs([resid[i] for i in Z], p, a)
            cnt = Counter(part[i] for i in R)
            r2 = sum(min(cap, v) for v in cnt.values())
            assert r1 + r2 == len(I), ("min-max certificate", r1, r2, len(I))
            assert in1(I) and in2(I)
            return I, Z
        path = []
        v = end
        while v is not None:
            path.append(v)
            v = prev[v]
        Iset = set(I)
        for v in path:
            if v in Iset:
                Iset.remove(v)
            else:
                Iset.add(v)
        I = [x for x in elems if x in Iset]
        assert in1(I) and in2(I)


def absorb_set(Fd, cols, rounds, I):
    """Lemma R, applied to the columns of I (independent mod U) in the given order."""
    p = Fd.p
    where = {i: l for l, R in enumerate(rounds) for i in R.S}
    for i in I:
        l = where[i]
        R = rounds[l]
        Ub = rebuild(Fd, rounds)
        assert not in_span(Ub, cols[i], p)
        b = next(b for b, G in enumerate(R.blocks) if i in G)
        G = R.blocks[b]
        assert len(G) >= 2, "Lemma R: absorbed column must lie in a block of size >= 2"
        blocks = R.blocks[:b] + [[j for j in G if j != i]] + R.blocks[b + 1:] + [[i]]
        R2 = mk_round(Fd, cols, R.S, R.delta, blocks)
        R2.extra = getattr(R, "extra", 0) + 1
        rounds[l] = R2
        assert rebuild(Fd, rounds) is not None, "Lemma R violated"
    return rebuild(Fd, rounds)


# ---------------------------------------------------------------------------
# leaves and recursion
# ---------------------------------------------------------------------------

def leaf(Fd, cols, rounds, Ub, src, P, rng, stats, kind):
    p = Fd.p
    assert src, "empty source set"
    assert rebuild(Fd, rounds) is not None, "(F1)/(F2)"
    assert all(in_span(Ub, cols[s], p) for s in src)
    used = set(i for R in rounds for i in R.S)
    assert not (used & set(src))
    nbad = steer_bad(Fd, cols, rounds, Ub, src)
    assert nbad == 0, ("(S) fails at leaf", kind, nbad)
    nb = max([len(R.blocks) for R in rounds] + [0])
    rho = sum(1 for R in rounds for b in range(len(R.blocks)) for b2 in range(b + 1, len(R.blocks))
              if R.bclass[b] != R.bclass[b2])
    stats["leaf:" + kind] += 1
    stats["maxblocks"] = max(stats["maxblocks"], nb)
    stats["maxload"] = max(stats["maxload"], max([getattr(R, "extra", 0) for R in rounds] + [0]))
    stats["maxrho"] = max(stats["maxrho"], rho)
    ctl = Ctl(Fd, cols, rounds, Ub, src)
    sm = ctl.summary()
    LEAVES.append(dict(kind=kind, **sm))
    if EVAL_PASSES[0]:
        for mode in ("plain", "look"):
            ok_ = 0
            evs = Counter()
            for _ in range(EVAL_PASSES[0]):
                x_, ev_ = ctl.backward(rng, mode)
                evs.update(ev_)
                if x_ is not None:
                    assert check(Fd, cols, x_), "invalid witness"
                    ok_ += 1
            LEAVES[-1][mode] = ok_ / EVAL_PASSES[0]
            LEAVES[-1]["ev_" + mode] = {k_.split("_level")[0]: v_ for k_, v_ in evs.items()}
    stats["maxN_lev"] = max(stats["maxN_lev"], sm["N_lev"])
    stats["maxN_src"] = max(stats["maxN_src"], sm["N_src"])
    for k in range(P.passes):
        x, ev = ctl.backward(rng, LEAF_MODE[0])
        for key, v in ev.items():
            stats["ev:" + key.split("_level")[0]] += v
        if x is not None:
            assert check(Fd, cols, x), "invalid witness"
            stats["single_pass_fail"] += k
            stats["passes"] += k + 1
            return x
    stats["passes"] += P.passes
    stats["single_pass_fail"] += P.passes
    stats["leaf_fail"] += 1
    return None


def recurse(Fd, cols, Yb, P, rng, stats, depth, kind):
    p = Fd.p
    idx = [i for i in range(len(cols)) if in_span(Yb, cols[i], p)]
    dimY = len(Yb)
    assert 0 < dimY < rank(cols, p)[0]
    if P.strict:
        assert len(idx) >= P.F(dimY), ("recursion count", kind, len(idx), P.F(dimY))
    stats["rec:" + kind] += 1
    sc = restrict_cols(idx, cols, p)
    y = solve_T(Fd, sc, P, rng, stats, depth + 1)
    if y is None:
        return None
    x = [0] * len(cols)
    for j, i in enumerate(idx):
        x[i] = y[j]
    assert check(Fd, cols, x)
    return x


def span_basis(Fd, vecs):
    return rank(vecs, Fd.p)[1]


# ---------------------------------------------------------------------------
# top phase (Lemma T_m)
# ---------------------------------------------------------------------------

def top_phase(Fd, cols, rounds, Ub, r, P, rng, stats, depth):
    """Flag realises H (codim m >= 1), all round columns in H, |X'| > F(r)-F(r-m)."""
    p = Fd.p
    M = len(cols)
    m = r - len(Ub)
    Fr = free_cols(M, rounds)
    Xp = [i for i in Fr if not in_span(Ub, cols[i], p)]
    # reserve Z: a basis of V/H inside X'
    Z, cur = [], list(Ub)
    for i in Xp:
        if not in_span(cur, cols[i], p):
            Z.append(i)
            cur.append(cols[i])
    assert len(Z) == m
    unused = [i for i in Xp if i not in set(Z)]
    tops = []
    while True:
        Ucur = rebuild(Fd, rounds + tops)
        if len(Ucur) == r:
            break
        T, found = [], None
        for cidx in unused:
            co = solve_in_span(Ucur + [cols[i] for i in T], cols[cidx], p)
            if co is None:
                T.append(cidx)
                continue
            delta = {cidx: 1}
            for j, i in enumerate(T):
                t = co[len(Ucur) + j]
                if t:
                    delta[i] = (-t) % p
            found = (cidx, delta)
            break
        if found is None:
            break
        cidx, delta = found
        S = sorted(delta)
        if len(S) == 1:
            unused.remove(cidx)        # top pool (lies in H_cur)
            continue
        for i in S:
            unused.remove(i)
        e = [sum(delta[i] * cols[i][t] for i in S) % p for t in range(len(cols[0]))]
        if len({Fd.cls(delta[i]) for i in S}) == 1 and not any(e):
            cc = Fd.cls(delta[S[0]])
            zeta = pow(Fd.g, (-cc) % Fd.k, p)
            x = [0] * M
            for i in S:
                x[i] = zeta * delta[i] % p
            assert check(Fd, cols, x)
            stats["top-direct"] += 1
            return x
        tops.append(mk_round(Fd, cols, S, delta, [[i] for i in S]))
        assert rebuild(Fd, rounds + tops) is not None
    Ucur = rebuild(Fd, rounds + tops)
    stats["top-rounds"] += len(tops)
    if len(Ucur) == r:
        used = set(i for R in tops for i in R.S)
        src = [i for i in Fr if i not in used]
        assert set(Z) <= set(src)
        return leaf(Fd, cols, rounds + tops, Ucur, src, P, rng, stats, "top")
    mp = r - len(Ucur)
    outside = [i for i in range(M) if not in_span(Ucur, cols[i], p)]
    assert len(outside) <= m + mp, ("top stall outside count", len(outside), m, mp)
    if P.strict:
        assert m + mp <= P.F(r) - P.F(r - mp)
    return recurse(Fd, cols, Ucur, P, rng, stats, depth, "top-stall")


# ---------------------------------------------------------------------------
# main reduction
# ---------------------------------------------------------------------------

def new_stats():
    s = Counter()
    s["maxblocks"] = s["maxload"] = s["maxrho"] = 0
    s["maxq"] = s["max_needed_load"] = 0
    s["maxN_lev"] = s["maxN_src"] = 0
    return s


def solve_T(Fd, cols, P, rng, stats=None, depth=0):
    p = Fd.p
    J, c = P.J, P.c
    stats = new_stats() if stats is None else stats
    M = len(cols)
    for i, v in enumerate(cols):
        if not any(v):
            x = [0] * M
            x[i] = 1
            stats["zero"] += 1
            return x
    r = rank(cols, p)[0]
    assert M >= P.F(r), ("budget", M, P.F(r))
    st = init_state(Fd, cols)
    status = forward_fast(Fd, cols, J, rng, st, rule="first")
    if status == "direct":
        stats["direct"] += 1
        assert check(Fd, cols, st["x"])
        return st["x"]
    rounds, Ub, B = st["rounds"], st["Ub"], st["B"]
    if status == "ok":
        return leaf(Fd, cols, rounds, Ub, B, P, rng, stats, "thm2")
    # ---- stall ----
    q = r - len(Ub)
    T, pool = st["T"], st["pool"]
    Rcols = [i for R in rounds for i in R.S]
    assert len(Rcols) <= DJ(r, J) - DJ(q, J), "Theorem 2(b) round count"
    assert M == r + len(Rcols) + len(pool) + len(T)
    assert len(T) <= q
    Fr = free_cols(M, rounds)
    Fin = [i for i in Fr if in_span(Ub, cols[i], p)]
    BinU = [i for i in B if in_span(Ub, cols[i], p)]
    b = len(BinU)
    assert rank([cols[i] for i in Fin], p)[0] == b
    eps = len(Ub) - b
    X = [i for i in Fr if not in_span(Ub, cols[i], p)]
    assert len(X) == len(B) - b + len(T) and len(B) - b == q + eps
    Rout = [i for i in Rcols if not in_span(Ub, cols[i], p)]
    stats["stall"] += 1
    stats["maxq"] = max(stats["maxq"], q)
    stats["trace"] = stats.get("trace", []) + [dict(depth=depth, r=r, q=q, b=b, eps=eps, pi=len(pool),
                                                    T=len(T), X=len(X), Rout=len(Rout))]
    # case 1
    if eps == 0:
        assert Ub, "U_L = 0 at a stall"
        return leaf(Fd, cols, rounds, Ub, Fin, P, rng, stats, "closure")
    # case 2
    if b <= q:
        return recurse(Fd, cols, span_basis(Fd, [cols[i] for i in BinU]), P, rng, stats, depth, "Y")
    # case 3
    assert r >= 2 * q + 2 and len(X) <= r - 1
    gens = span_basis(Fd, [cols[i] for i in Rcols + Fin])
    qplus = r - len(gens)
    assert rank_mod(Ub, [cols[i] for i in Rout], p) == q - qplus
    if qplus >= 2 * (J - 1):
        outside = [i for i in range(M) if not in_span(gens, cols[i], p)]
        assert set(outside) <= set(X)
        if P.strict:
            assert r - 1 <= P.F(r) - P.F(r - qplus)
        return recurse(Fd, cols, gens, P, rng, stats, depth, "U+")
    part = {i: l for l, R in enumerate(rounds) for i in R.S}
    # the least achievable load (for the record): smallest cap with a complete absorption
    need = 0
    while True:
        I0, _ = matroid_intersection(Fd, cols, Ub, Rout, part, need)
        if len(I0) == q - qplus:
            break
        need += 1
    stats["max_needed_load"] = max(stats["max_needed_load"], need)
    I, Z = matroid_intersection(Fd, cols, Ub, Rout, part, c)
    if len(I) < q - qplus:
        Wb = span_basis(Fd, Ub + [cols[i] for i in Z])
        qW = r - len(Wb)
        outside = [i for i in range(M) if not in_span(Wb, cols[i], p)]
        RZ = [i for i in Rout if i not in set(Z)]
        assert set(outside) <= set(RZ) | set(X)
        cnt = Counter(part[i] for i in RZ)
        r2 = sum(min(c, v) for v in cnt.values())
        nbig = sum(1 for v in cnt.values() if v > c)
        assert r2 <= qW - 1 and nbig >= 1 and c * nbig <= r2
        bound = (qW - 1) + ((qW - 1) // c) * (r + 1 - c) + (r - 1)
        assert len(outside) <= bound and c + 1 <= qW <= q
        stats["W_events"] += 1
        stats["W_eq_U"] += (qW == q)
        colsU = sum(1 for i in range(M) if in_span(Ub, cols[i], p))
        stats["W_but_U_count_fails"] += (colsU < P.F(r - q))
        Yb0 = span_basis(Fd, [cols[i] for i in BinU])
        colsY = sum(1 for i in range(M) if in_span(Yb0, cols[i], p))
        stats["W_and_Y_count_fails"] += (colsY < P.F(b))
        if P.strict:
            assert bound <= P.F(r) - P.F(r - qW), ("(I1)", r, qW, c)
            return recurse(Fd, cols, Wb, P, rng, stats, depth, "W")
        idx = [i for i in range(M) if in_span(Wb, cols[i], p)]
        if len(idx) >= P.F(r - qW):
            return recurse(Fd, cols, Wb, P, rng, stats, depth, "W")
        stats["W_count_fails(stress)"] += 1
        I = I0                                     # complete absorption, load = need > c
    rounds = list(rounds)
    Ub = absorb_set(Fd, cols, rounds, I)
    assert len(Ub) == r - qplus
    load = max([getattr(R, "extra", 0) for R in rounds] + [0])
    if P.strict:
        assert load <= c
    stats["absorb"] += 1
    if qplus == 0:
        return leaf(Fd, cols, rounds, Ub, B, P, rng, stats, "absorbed")
    m = qplus
    assert all(in_span(Ub, cols[i], p) for R in rounds for i in R.S)
    Fr = free_cols(M, rounds)
    Fin2 = [i for i in Fr if in_span(Ub, cols[i], p)]
    if rank([cols[i] for i in Fin2], p)[0] == len(Ub):
        return leaf(Fd, cols, rounds, Ub, Fin2, P, rng, stats, "closure-H")
    Xp = [i for i in Fr if not in_span(Ub, cols[i], p)]
    if len(Xp) <= P.F(r) - P.F(r - m):
        return recurse(Fd, cols, Ub, P, rng, stats, depth, "H")
    return top_phase(Fd, cols, rounds, Ub, r, P, rng, stats, depth)

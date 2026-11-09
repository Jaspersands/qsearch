"""Q1 pass: closed sub-flags (Lemma A), the top-pair/top-triple step (Lemma T), absorption
by re-splitting (Lemma R) and recursion on flats, on top of the SSS(E) code of
../2026-11-05-rees-sde-worst-case/sss.py (imported, unchanged).

All arithmetic is exact.  Every returned witness is verified with sss.check.
"""
import os
import sys
import random
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-05-rees-sde-worst-case"))
import sss  # noqa: E402
from sss import Field, solve_in_span, rank, split_blocks, Round, check, worst_forward_cost  # noqa


def D(q, E):
    return worst_forward_cost(q, E) if q > 0 else 0


# ---------------------------------------------------------------------------
# flags
# ---------------------------------------------------------------------------

def mk_round(Fd, cols, S, delta, blocks):
    p, a = Fd.p, len(cols[0])
    R = Round()
    R.S, R.delta, R.blocks = sorted(S), dict(delta), [list(G) for G in blocks]
    R.e = [sum(delta[i] * cols[i][t] for i in S) % p for t in range(a)]
    R.bclass = [Fd.cls(delta[G[0]]) for G in R.blocks]
    R.W = [[sum(delta[i] * cols[i][t] for i in G) % p for t in range(a)] for G in R.blocks]
    return R


def rebuild(Fd, rounds):
    """Recompute flag coordinates; check (F1) directness and (F2) e_l in U_{l-1}."""
    p = Fd.p
    Ub = []
    for R in rounds:
        if Ub and solve_in_span(Ub, R.e, p) is None:
            return None
        if not Ub and any(R.e):
            return None
        R.start = len(Ub)
        for w in R.W[1:]:
            if solve_in_span(Ub, w, p) is not None:
                return None
            Ub.append(w)
        R.end = len(Ub)
    return Ub


def steer_bad(Fd, cols, rounds, Ub, sources, extra_vecs=()):
    """Number of cross-class pairs (j,b,b') whose steering functional vanishes on every
    source and on every e_l, l>j (the hypothesis of Lemma 2 fails exactly there)."""
    p = Fd.p
    cs = [solve_in_span(Ub, cols[s], p) for s in sources]
    cs += [solve_in_span(Ub, v, p) for v in extra_vecs]
    assert all(c is not None for c in cs), "source outside realized space"
    ce = [solve_in_span(Ub, R.e, p) if any(R.e) else [0] * len(Ub) for R in rounds]
    bad = 0
    for j, R in enumerate(rounds):
        nb = len(R.blocks)
        for b in range(nb):
            for b2 in range(b + 1, nb):
                if R.bclass[b] == R.bclass[b2]:
                    continue
                def phi(c):
                    x = c[R.start + b - 1] if b else 0
                    y = c[R.start + b2 - 1] if b2 else 0
                    return (x - y) % p
                if any(phi(c) for c in cs):
                    continue
                if any(phi(ce[l]) for l in range(j + 1, len(rounds))):
                    continue
                bad += 1
    return bad


def run_backward(Fd, cols, rounds, Ub, sources, rng, passes):
    for _ in range(passes):
        x, st = sss.backward(Fd, cols, rounds, Ub, sources, rng)
        if x is not None:
            assert check(Fd, cols, x), "invalid witness"
            return x
    return None


# ---------------------------------------------------------------------------
# forward pass with swaps, resumable, with snapshots
# ---------------------------------------------------------------------------

def forward(Fd, cols, E, rng, st, rule="random", snap=None):
    """st: dict(rounds, B, pool, unused).  Continues the forward pass of SSS(E) with swaps.
    snap(st) is called after every round.  Returns status: ok/stall/direct."""
    p, a = Fd.p, len(cols[0])
    r = len(st["B"])
    while True:
        Ub = rebuild(Fd, st["rounds"])
        assert Ub is not None
        st["Ub"] = Ub
        if len(Ub) == r:
            return "ok"
        T, found = [], None
        for c in st["unused"]:
            co = solve_in_span(Ub + [cols[i] for i in T], cols[c], p)
            if co is None:
                T.append(c)
                continue
            delta = {c: 1}
            for j, i in enumerate(T):
                t = co[len(Ub) + j]
                if t:
                    delta[i] = (-t) % p
            found = (c, delta)
            break
        if found is None:
            st["T"] = T
            return "stall"
        c, delta = found
        S = sorted(delta)
        if len(S) == 1:
            st["unused"].remove(c)
            B = st["B"]
            cb = solve_in_span([cols[i] for i in B], cols[c], p)
            out = [B[j] for j in range(r) if cb[j] and solve_in_span(Ub, cols[B[j]], p) is None]
            if out:
                sig = out[0]
                B[B.index(sig)] = c
                st["unused"].append(sig)
                st["swaps"] = st.get("swaps", 0) + 1
            else:
                st["pool"].append(c)
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
        st["rounds"].append(mk_round(Fd, cols, S, delta, blocks))
        if snap is not None:
            Ub2 = rebuild(Fd, st["rounds"])
            st["Ub"] = Ub2
            res = snap(st)
            if res is not None:
                st["x"] = res
                return "snap"


def init_state(Fd, cols, order=None):
    p = Fd.p
    order = list(range(len(cols))) if order is None else order
    B, bas = [], []
    for i in order:
        if solve_in_span(bas, cols[i], p) is None:
            bas.append(cols[i])
            B.append(i)
    return dict(rounds=[], B=B, pool=[], unused=[i for i in order if i not in set(B)], swaps=0)


def free_cols(n, rounds):
    used = set(i for R in rounds for i in R.S)
    return [i for i in range(n) if i not in used]


def in_span(Ub, v, p):
    return (not any(v)) if not Ub else solve_in_span(Ub, v, p) is not None


# ---------------------------------------------------------------------------
# Lemma A (closure) and Lemma T (top round)
# ---------------------------------------------------------------------------

def try_closure(Fd, cols, rounds, Ub, rng, passes):
    p = Fd.p
    if not Ub:
        return None
    Fin = [i for i in free_cols(len(cols), rounds) if in_span(Ub, cols[i], p)]
    rk, _ = rank([cols[i] for i in Fin], p)
    if rk < len(Ub):
        return None
    assert steer_bad(Fd, cols, rounds, Ub, Fin) == 0   # Lemma A: no vanishing functional
    return run_backward(Fd, cols, rounds, Ub, Fin, rng, passes)


def top_candidates(Fd, cols, Ub, X, q, E):
    """Circuits modulo U inside X that realize the whole quotient (q <= E-1):
    a set C of q+1 columns of X with a relation mod U of full support."""
    p = Fd.p
    out = []
    for C in combinations(X, q + 1):
        co = solve_in_span(Ub + [cols[i] for i in C[1:]], cols[C[0]], p)
        if co is None:
            continue
        tail = co[len(Ub):]
        if not all(tail):
            continue
        # C[1:] must be independent mod U (then C is a circuit mod U and realizes V/U)
        if rank(Ub + [cols[i] for i in C[1:]], p)[0] != len(Ub) + q:
            continue
        delta = {C[0]: 1}
        for j, i in enumerate(C[1:]):
            delta[i] = (-tail[j]) % p
        out.append((C, delta))
    return out


def try_top(Fd, cols, rounds, Ub, E, rng, passes, maxcand=400, stats=None):
    """Lemma T: lower flag realizes U of codim q <= E-1; top round = a circuit C mod U of
    q+1 free columns outside U (all singleton blocks); sources = all other free columns."""
    p = Fd.p
    r = rank(cols, p)[0]
    q = r - len(Ub)
    if q < 1 or q > E - 1:
        return None
    Fr = free_cols(len(cols), rounds)
    X = [i for i in Fr if not in_span(Ub, cols[i], p)]
    if len(X) < q + 2:
        return None
    cands = top_candidates(Fd, cols, Ub, X, q, E)
    rng.shuffle(cands)
    tried = 0
    for C, delta in cands[:maxcand]:
        top = mk_round(Fd, cols, list(C), delta, [[i] for i in C])
        rr = rounds + [top]
        Ub2 = rebuild(Fd, rr)
        if Ub2 is None:
            continue
        src = [i for i in Fr if i not in set(C)]
        tried += 1
        if steer_bad(Fd, cols, rr, Ub2, src):
            if stats is not None:
                stats["top_bad"] = stats.get("top_bad", 0) + 1
            continue
        x = run_backward(Fd, cols, rr, Ub2, src, rng, passes)
        if x is not None:
            return x
    return None


# ---------------------------------------------------------------------------
# Lemma R (absorption by re-splitting)
# ---------------------------------------------------------------------------

def absorb(Fd, cols, rounds, cap):
    """Lemma R: add singleton blocks {i} for round columns i outside U_L, at most cap extra
    blocks per round (R.extra counts them).  Greedy.  Returns absorbed directions."""
    p = Fd.p
    gained = 0
    for l in range(len(rounds)):
        while getattr(rounds[l], "extra", 0) < cap:
            R = rounds[l]
            Ub = rebuild(Fd, rounds)
            hit = None
            for b, G in enumerate(R.blocks):
                if len(G) >= 2:
                    for i in G:
                        if not in_span(Ub, cols[i], p):
                            hit = (b, i)
                            break
                if hit:
                    break
            if hit is None:
                break
            b, i = hit
            G = R.blocks[b]
            blocks = R.blocks[:b] + [[j for j in G if j != i]] + R.blocks[b + 1:] + [[i]]
            R2 = mk_round(Fd, cols, R.S, R.delta, blocks)
            R2.extra = getattr(R, "extra", 0) + 1
            rounds[l] = R2
            assert rebuild(Fd, rounds) is not None, "Lemma R violated"
            gained += 1
    rebuild(Fd, rounds)
    return gained


def restrict_cols(idx, cols, p):
    sub = rank([cols[i] for i in idx], p)[1]
    return [solve_in_span(sub, cols[i], p) for i in idx]

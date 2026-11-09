"""Shared helpers for the Q1 adversarial search.  The algorithm under test is imported
unchanged from ../2026-11-05-rees-sde-worst-case/sss.py (sss_theorem, sss_full and the
pieces sss_full is made of).  `one_order` replays exactly one iteration of the sss_full
loop (sss_rec, then finish_stall on a stall) on a given column order and also returns the
stall certificate."""
import os
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-05-rees-sde-worst-case"))
import sss  # noqa: E402
from sss import (Field, sss_full, sss_theorem, sss_rec, finish_stall, forward_swap,  # noqa
                 budget, rank, solve_in_span, check)

E = 3


def D3(q):
    return 0 if q == 0 else (q + 2) ** 2 // 4


def theorem_forward(Fd, cols, rule="random", rng=None):
    """Theorem-2 forward pass on the given order: returns dict with pi, status, q, etc."""
    rng = rng or random.Random(0)
    p = Fd.p
    if any(not any(c) for c in cols):
        return dict(status="zero", pi=0)
    reserve, bas = [], []
    for i in range(len(cols)):
        if solve_in_span(bas, cols[i], p) is None:
            bas.append(cols[i])
            reserve.append(i)
    r = len(reserve)
    res = forward_swap(Fd, cols, E, rng, reserve, rule)
    if res["status"] == "direct":
        return dict(status="direct", pi=0, r=r)
    out = dict(status=res["status"], pi=len(res["pool"]), r=r, swaps=res["swaps"])
    if res["status"] == "stall":
        U = res["U"]
        used = set(i for R in res["rounds"] for i in R.S) | set(res["B"]) | set(res["pool"])
        out["q"] = r - len(U)
        out["BoutU"] = sum(1 for i in res["B"] if solve_in_span(U, cols[i], p) is None) if U else r
        out["unused"] = len([i for i in range(len(cols)) if i not in used])
    return out


def cert_of(Fd, cols, res):
    p = Fd.p
    U = res["U"]
    used = set(i for R in res["rounds"] for i in R.S) | set(res["B"]) | set(res["pool"])
    r = len(res["B"])
    return dict(
        U_L=U, dimU=len(U), q=r - len(U), B=list(res["B"]),
        B_out_U=[i for i in res["B"] if not U or solve_in_span(U, cols[i], p) is None],
        pool=list(res["pool"]), pi=len(res["pool"]),
        unused=[i for i in range(len(cols)) if i not in used],
        rounds=[list(R.S) for R in res["rounds"]], swaps=res.get("swaps", 0))


def one_order(Fd, cols, perm, rng, passes=20, rule="random"):
    """One iteration of the sss_full loop on the order `perm`.  Returns (x or None,
    status, cert-or-None), with x in the ORIGINAL column indexing, cert in perm indexing."""
    pc = [cols[i] for i in perm]
    stats = {}
    x, st = sss_rec(Fd, pc, E, rng, passes, rule, stats=stats)
    cert = None
    if x is None and st.startswith("stall"):
        cert = cert_of(Fd, pc, stats["last_res"])
        x, st2 = finish_stall(Fd, pc, E, rng, stats["last_res"], passes, rule)
        st = st2 if x is not None else st + "/" + st2
    if x is not None:
        y = [0] * len(cols)
        for j, i in enumerate(perm):
            y[i] = x[j]
        assert check(Fd, cols, y)
        return y, st, cert
    return None, st, cert


def order_fail_rate(Fd, cols, rng, K, passes=10):
    """Fraction of K orders (first = identity, rest random) on which one sss_full
    iteration fails; plus the first failure certificate."""
    fails, first = 0, None
    for t in range(K):
        perm = list(range(len(cols)))
        if t:
            rng.shuffle(perm)
        x, st, cert = one_order(Fd, cols, perm, rng, passes)
        if x is None:
            fails += 1
            if first is None:
                first = dict(perm=perm, status=st, cert=cert)
    return fails / K, first


# ---------------------------------------------------------------------------
# bank generators
# ---------------------------------------------------------------------------

def rvec(rng, p, a):
    return [rng.randrange(p) for _ in range(a)]


def comb(rng, p, basis, a, nonzero=True):
    while True:
        co = [rng.randrange(p) for _ in basis]
        v = [sum(c * b[t] for c, b in zip(co, basis)) % p for t in range(a)]
        if any(v) or not nonzero:
            return v


def fam_lines(rng, p, a, M, m):
    vs = [rvec(rng, p, a) for _ in range(m)]
    return [[rng.randrange(1, p) * t % p for t in vs[i % m]] for i in range(M)]


def fam_planes(rng, p, a, M, m, dim=2):
    flats = [[rvec(rng, p, a) for _ in range(dim)] for _ in range(m)]
    return [comb(rng, p, flats[i % m], a) for i in range(M)]


def fam_flag_subthreshold(rng, p, a, M):
    """Nested flag Y_1 < Y_2 < ... < Y_a = F^a; Y_k holds D3(k)+k-1 columns (one below the
    recursion threshold) when possible; the rest generic."""
    base = [rvec(rng, p, a) for _ in range(a)]
    cols, cnt = [], 0
    for k in range(1, a + 1):
        want = min(M, D3(k) + k - 1) if k < a else M
        while cnt < want:
            cols.append(comb(rng, p, base[:k], a))
            cnt += 1
    return cols[:M]


def fam_codim1(rng, p, a, M, t):
    """M - t columns in a hyperplane H (generic inside H), t columns outside."""
    H = [rvec(rng, p, a) for _ in range(a - 1)]
    cols = [comb(rng, p, H, a) for _ in range(M - t)] + [rvec(rng, p, a) for _ in range(t)]
    return cols


def fam_codim1_front(rng, p, a, M, t):
    """As fam_codim1 but one outside column FIRST, so that B has exactly one column off H."""
    c = fam_codim1(rng, p, a, M, t)
    return [c[-1]] + c[:-1]


def fam_lines_planes(rng, p, a, M, nl, npl):
    ls = [rvec(rng, p, a) for _ in range(nl)]
    ps = [[rvec(rng, p, a) for _ in range(2)] for _ in range(npl)]
    cols = []
    for i in range(M):
        j = i % (nl + npl)
        if j < nl:
            cols.append([rng.randrange(1, p) * t % p for t in ls[j]])
        else:
            cols.append(comb(rng, p, ps[j - nl], a))
    return cols


def fam_random(rng, p, a, M):
    return [rvec(rng, p, a) for _ in range(M)]


def fam_basis_dense(rng, p, a, M, k):
    """Basis e_1..e_a first, then columns concentrated in span(e_1..e_k) (subthreshold),
    then generic: tries to push columns into span(B cap U)."""
    base = [rvec(rng, p, a) for _ in range(a)]
    cols = list(base)
    n_in = max(0, D3(k) - 1)
    cols += [comb(rng, p, base[:k], a) for _ in range(n_in)]
    while len(cols) < M:
        cols.append(rvec(rng, p, a))
    return cols[:M]


def fam_pairs(rng, p, a, M):
    """Columns come in proportional pairs (lines with exactly 2 points; R1 never fires)."""
    cols = []
    while len(cols) < M:
        v = rvec(rng, p, a)
        cols.append(v)
        cols.append([rng.randrange(1, p) * t % p for t in v])
    return cols[:M]


# ---------------------------------------------------------------------------
# mutations for hill climbing
# ---------------------------------------------------------------------------

def nonresidue(Fd, rng):
    while True:
        y = rng.randrange(2, Fd.p)
        if Fd.cls(y) != 0:
            return y


def mutate(Fd, cols, rng):
    p = Fd.p
    a = len(cols[0])
    c = [list(v) for v in cols]
    M = len(c)
    op = rng.choice(["replace", "scale", "project", "line", "project", "line", "swap", "flat_small"])
    i = rng.randrange(M)
    if op == "replace":
        c[i] = rvec(rng, p, a)
    elif op == "scale":
        u = nonresidue(Fd, rng)
        c[i] = [u * t % p for t in c[i]]
    elif op == "project":
        k = rng.randint(1, max(1, a - 1))
        js = rng.sample([j for j in range(M) if j != i], k)
        c[i] = comb(rng, p, [cols[j] for j in js], a)
    elif op == "line":
        j = rng.choice([j for j in range(M) if j != i])
        c[i] = [rng.randrange(1, p) * t % p for t in cols[j]]
    elif op == "swap":
        j = rng.randrange(M)
        c[i], c[j] = c[j], c[i]
    elif op == "flat_small":
        # move column into the span of two others (a plane)
        js = rng.sample([j for j in range(M) if j != i], 2)
        c[i] = comb(rng, p, [cols[j] for j in js], a)
    if not any(c[i]):
        c[i][0] = 1
    return c, op


def has_collinear_triple(Fd, cols):
    p = Fd.p
    lines = {}
    for c in cols:
        j = next((t for t in range(len(c)) if c[t]), None)
        if j is None:
            return True
        iv = pow(c[j], p - 2, p)
        key = tuple(x * iv % p for x in c)
        lines[key] = lines.get(key, 0) + 1
        if lines[key] >= 3:
            return True
    return False


def dense_flats(Fd, cols, maxk=3):
    """Flats spanned by <= maxk columns that hold >= D3(dim)+dim columns, dim < rank."""
    import itertools
    p = Fd.p
    r = rank(cols, p)[0]
    seen, out = set(), []
    for k in range(1, min(maxk, r - 1) + 1):
        for S in itertools.combinations(range(len(cols)), k):
            rk, bas = rank([cols[i] for i in S], p)
            if rk != k:
                continue
            inside = tuple(i for i in range(len(cols)) if solve_in_span(bas, cols[i], p) is not None)
            if inside in seen:
                continue
            seen.add(inside)
            if len(inside) >= D3(k) + k:
                out.append((k, len(inside)))
    return out

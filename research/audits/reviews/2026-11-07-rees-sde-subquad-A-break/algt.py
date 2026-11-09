"""Independent implementation of ALG-T (report 2026-11-07-rees-sde-subquad-A.md, section 6).

Written from the reports (subquad-A sections 2-6, Q1 sections 1-3, worst-case section 3,
two-relation sections 3-4), not from subquad.py.  Conventions where the reports leave a choice
(recorded in the break report, section 2):
  * reserved basis B = first r independent columns in the given order;
  * scan the unused list in order; the first column dependent mod U + span(T) gives the circuit;
  * swap: sigma = first entry of B (in B's order) outside U with nonzero coefficient; c takes
    sigma's slot in B and sigma is appended to the end of the unused list;
  * split rule ("first"): blocks = classes in increasing class index, each in increasing
    column index; while fewer than min(J,|S|) blocks, take the first largest block G, keep G[0]
    and append G[1:] as a new block (same partition as "peel the first element");
  * matroid intersection: shortest augmenting paths, Rout in increasing index; Z = the set
    of elements from which X2 is reachable (Schrijver Thm 41.2 proof); absorption in the order
    of I as returned;
  * top phase: Z = greedy basis of V/H from X' in index order; singleton-block greedy circuits
    on X' \\ Z modulo H_cur, columns in H_cur set aside;
  * recursion: the sub-bank is the set of columns lying in the flat, kept in original order.
Options (for attacks) change these conventions; the theorem must hold for every choice.
"""
import random
from collections import Counter

import numpy as np

from la import Ech, Fq, CoordSolver, I64

# ---------------------------------------------------------------------------
# counts


_D = {}


def DJ(q, J):
    """D_J(q) = max_{1<=k<=q} (k+1+D_J(q-min(J-1,k))), D_J(0)=0 (brute force from the definition)."""
    t = _D.setdefault(J, [0])
    while len(t) <= q:
        x = len(t)
        t.append(max(k + 1 + t[x - min(J - 1, k)] for k in range(1, x + 1)))
    return t[q]


class Par:
    def __init__(self, J, k, c=None, C=None, sigma_rule="first", split_rule="first",
                 sigma_place="end", abs_order="asis", z_rule="first", zcert="toX2", rng=None):
        assert J >= max(k, 2)
        self.J, self.k = J, k
        self.c = 2 * (J - 1) if c is None else c
        self.C = max(2, 2 * J - 4) if C is None else C
        self.E = 3 * J - 2
        self.sigma_rule = sigma_rule
        self.split_rule = split_rule
        self.sigma_place = sigma_place
        self.abs_order = abs_order
        self.z_rule = z_rule
        self.zcert = zcert
        self.rng = rng or random.Random(0)

    def F(self, r):
        return DJ(r, self.J) + self.C * r if r > 0 else 0


class Fail(Exception):
    """A claim of the theorem (case analysis or count) is violated."""


# ---------------------------------------------------------------------------
# run record


class Rec:
    def __init__(self):
        self.branch = Counter()
        self.slack = {}          # name -> min slack observed
        self.viol = []           # list of (name, value, context)
        self.loads = []
        self.least_loads = []
        self.events = []

    def sl(self, name, val, ctx=None):
        val = int(val)
        if name not in self.slack or val < self.slack[name]:
            self.slack[name] = val
        if val < 0:
            self.viol.append((name, val, ctx))


# ---------------------------------------------------------------------------
# forward pass SSS(J)


def split_blocks(Fd, S, delta, J, par):
    cl = {}
    for i in S:
        cl.setdefault(Fd.cls(delta[i]), []).append(i)
    blocks = [list(v) for _, v in sorted(cl.items())]
    target = min(J, len(S))
    assert len(blocks) <= target
    while len(blocks) < target:
        if par.split_rule == "first":
            big = max(range(len(blocks)), key=lambda b: len(blocks[b]))
            G = blocks[big]
            blocks[big] = G[:1]
            blocks.append(G[1:])
        else:  # random refinement
            cand = [b for b in range(len(blocks)) if len(blocks[b]) >= 2]
            big = par.rng.choice(cand)
            G = blocks[big][:]
            par.rng.shuffle(G)
            cut = par.rng.randrange(1, len(G))
            blocks[big] = sorted(G[:cut])
            blocks.append(sorted(G[cut:]))
    return blocks


def round_vectors(Fd, cols, rnd):
    p = Fd.p
    Ws = []
    for G in rnd["blocks"]:
        w = np.zeros(cols.shape[1], dtype=I64)
        for i in G:
            w = (w + rnd["delta"][i] * cols[i]) % p
        Ws.append(w)
    e = np.zeros(cols.shape[1], dtype=I64)
    for w in Ws:
        e = (e + w) % p
    return Ws, e


def flag_space(Fd, cols, rounds):
    """Rebuild U_L from the rounds, asserting (F1)/(F2) internally."""
    U = Ech(Fd.p, cols.shape[1])
    for rnd in rounds:
        Ws, e = round_vectors(Fd, cols, rnd)
        if not U.contains(e):
            raise Fail("internal F2")
        for w in Ws[1:]:
            if not U.add(w):
                raise Fail("internal F1")
    return U


def scan(Fd, cols, Uech, order, qmax):
    """One greedy scan of `order` modulo U.  Returns (pos, delta) for the first dependent
    column (delta on T+{c}, delta_c = 1), or (None, T) on a stall.  Coefficients tracked."""
    p = Fd.p
    n = len(order)
    if n == 0:
        return None, []
    R0 = Uech.reduce(cols[order])
    R = R0.copy()
    Coef = np.zeros((n, max(qmax, 1) + 1), dtype=I64)
    Tpos, TC, Tpiv = [], [], []
    for i in range(n):
        row = R[i]
        nz = np.nonzero(row)[0]
        if len(nz) == 0:
            if not R0[i].any():
                return i, {order[i]: 1}
            delta = {order[i]: 1}
            for s, t in enumerate(Tpos):
                v = int(Coef[i, s]) % p
                if v:
                    delta[order[t]] = v
            return i, delta
        j = int(nz[0])
        inv = pow(int(row[j]), p - 2, p)
        s = len(Tpos)
        if s >= Coef.shape[1]:
            raise Fail("internal: T larger than q")
        cf = Coef[i].copy()
        cf[s] = (cf[s] + 1) % p
        nrow = row * inv % p
        ncf = cf * inv % p
        R[i] = nrow
        Tpos.append(i)
        TC.append(ncf)
        Tpiv.append(j)
        if i + 1 < n:
            f = R[i + 1:, j].copy()
            nzf = np.nonzero(f)[0]
            if len(nzf):
                idx = nzf + i + 1
                R[idx] = (R[idx] - f[nzf, None] * nrow[None, :]) % p
                Coef[idx] = (Coef[idx] - f[nzf, None] * ncf[None, :]) % p
    return None, [order[t] for t in Tpos]


def init_state(Fd, cols, sub):
    p, a = Fd.p, cols.shape[1]
    B, basis = [], Ech(p, a)
    for i in sub:
        if basis.add(cols[i]):
            B.append(i)
    Bset = set(B)
    return dict(B=B, r=len(B), pool=[], unused=[i for i in sub if i not in Bset], rounds=[],
                U=Ech(p, a), swaps=0)


def forward(Fd, cols, sub, par, rec, st=None):
    """SSS(J) forward pass on the sub-bank `sub` (list of global indices, in order).
    If st is given, the pass is continued from that state (used by the adaptive adversary)."""
    p, a = Fd.p, cols.shape[1]
    J = par.J
    if st is None:
        st = init_state(Fd, cols, sub)
    r = st["r"]
    U = st["U"]
    while U.dim < r:
        pos, res = scan(Fd, cols, U, st["unused"], r - U.dim)
        if pos is None:
            st["T"] = res
            return "stall", st
        delta = res
        c = st["unused"][pos]
        if len(delta) == 1:
            # c in U
            st["unused"].pop(pos)
            BinU = [s for s in st["B"] if U.contains(cols[s])]
            BU = Ech(p, a)
            BU.add_many(cols[BinU])
            if BU.contains(cols[c]):
                st["pool"].append(c)
            else:
                cs = CoordSolver(p, [cols[s] for s in st["B"]])
                gam = cs.coords(cols[c])
                assert gam is not None
                cand = [j for j, s in enumerate(st["B"]) if gam[j] and not U.contains(cols[s])]
                assert cand
                if par.sigma_rule == "first":
                    j = cand[0]
                else:
                    j = par.rng.choice(cand)
                sig = st["B"][j]
                st["B"][j] = c
                if par.sigma_place == "end":
                    st["unused"].append(sig)
                else:  # back at its original index position
                    u = st["unused"]
                    k = 0
                    while k < len(u) and u[k] < sig:
                        k += 1
                    u.insert(k, sig)
                st["swaps"] += 1
            continue
        S = sorted(delta)
        for i in S:
            st["unused"].remove(i)
        e = np.zeros(a, dtype=I64)
        for i in S:
            e = (e + delta[i] * cols[i]) % p
        if not U.contains(e):
            raise Fail("e not in U")
        cls = {Fd.cls(delta[i]) for i in S}
        if len(cls) == 1 and not e.any():
            z = Fd.elem_of_class(-cls.pop())
            x = {i: z * delta[i] % p for i in S}
            st["x"] = x
            return "direct", st
        blocks = split_blocks(Fd, S, delta, J, par)
        rnd = dict(S=S, delta=delta, blocks=blocks, kind="lower", load=0,
                   q_at=r - U.dim)
        Ws, e2 = round_vectors(Fd, cols, rnd)
        for w in Ws[1:]:
            if not U.add(w):
                raise Fail("F1 in forward pass")
        st["rounds"].append(rnd)
    return "full", st


# ---------------------------------------------------------------------------
# matroid intersection: linear matroid (mod U) x partition matroid (rounds, capacity cap)


def matroid_intersection(Fd, cols, U, Rout, part, cap, zcert="toX2"):
    p = Fd.p
    n = len(Rout)
    if n == 0:
        return [], [], dict(r1Z=0, r2=0)
    R = U.reduce(cols[Rout])          # n x a
    I = []
    while True:
        Iset = set(I)
        # coefficients of every element in the basis I (mod U)
        cs = CoordSolver(p, [R[t] for t in I]) if I else None
        coef = {}
        X1 = set()
        for z in range(n):
            if z in Iset:
                continue
            if cs is None:
                if R[z].any():
                    X1.add(z)
                coef[z] = None
                continue
            co = cs.coords(R[z])
            if co is None:
                X1.add(z)
            coef[z] = co
        cnt = Counter(part[t] for t in I)
        X2 = {z for z in range(n) if z not in Iset and cnt[part[z]] < cap}
        # arcs
        out = {v: [] for v in range(n)}
        Ipos = {t: s for s, t in enumerate(I)}
        for z in range(n):
            if z in Iset:
                continue
            for y in I:
                # y -> z  if I - y + z independent in M1
                if z in X1 or (coef[z] is not None and coef[z][Ipos[y]]):
                    out[y].append(z)
                # z -> y  if I - y + z independent in M2
                if part[z] == part[y] or cnt[part[z]] < cap:
                    out[z].append(y)
        # BFS shortest path X1 -> X2
        prev = {}
        from collections import deque
        dq = deque()
        for z in sorted(X1):
            prev[z] = None
            dq.append(z)
        end = None
        while dq:
            v = dq.popleft()
            if v in X2:
                end = v
                break
            for w in out[v]:
                if w not in prev:
                    prev[w] = v
                    dq.append(w)
        if end is None:
            break
        path = []
        v = end
        while v is not None:
            path.append(v)
            v = prev[v]
        newI = set(I) ^ set(path)
        I = sorted(newI)
    # certificate: Zc = elements from which X2 is reachable (zcert="toX2"), or the
    # complement of the set reachable from X1 (zcert="fromX1"); both attain the min-max
    if zcert == "toX2":
        rev = {v: [] for v in range(n)}
        for v in range(n):
            for w in out[v]:
                rev[w].append(v)
        reach = set(X2)
        st = list(X2)
        while st:
            v = st.pop()
            for w in rev[v]:
                if w not in reach:
                    reach.add(w)
                    st.append(w)
    else:
        fr = set(X1)
        st = list(X1)
        while st:
            v = st.pop()
            for w in out[v]:
                if w not in fr:
                    fr.add(w)
                    st.append(w)
        reach = set(range(n)) - fr
    Z = sorted(reach)
    E1 = Ech(p, cols.shape[1])
    r1Z = E1.add_many(R[Z]) if Z else 0
    cz = Counter(part[t] for t in range(n) if t not in reach)
    r2 = sum(min(cap, v) for v in cz.values())
    return [Rout[t] for t in I], [Rout[t] for t in Z], dict(r1Z=r1Z, r2=r2)


# ---------------------------------------------------------------------------
# ALG-T


def cols_in(Fd, cols, sub, flat):
    m = flat.contains_many(cols[sub])
    return [i for i, b in zip(sub, m) if b]


def recurse_target(Fd, cols, sub, flat, par, rec, name, r):
    tgt = cols_in(Fd, cols, sub, flat)
    rr = Ech(Fd.p, cols.shape[1])
    rr.add_many(cols[tgt])
    r2 = rr.dim
    rec.sl("rec_rank_drop", r - 1 - r2, name)
    rec.sl("rec_count", len(tgt) - par.F(r2), name)
    rec.sl("rec_count_" + name, len(tgt) - par.F(r2), name)
    return tgt


def solve(Fd, cols, sub, par, rec, depth=0):
    """Returns ('solution', x) or ('leaf', leaf).  Raises Fail on a broken claim."""
    p, a = Fd.p, cols.shape[1]
    J, c, E = par.J, par.c, par.E
    rec.branch["call"] += 1
    for i in sub:
        if not cols[i].any():
            rec.branch["zero_col"] += 1
            return "solution", {i: 1}
    rk = Ech(p, a)
    rk.add_many(cols[sub])
    r = rk.dim
    M = len(sub)
    rec.sl("hyp_M_ge_F", M - par.F(r), depth)
    status, st = forward(Fd, cols, sub, par, rec)
    if status == "direct":
        rec.branch["direct_fwd"] += 1
        return "solution", st["x"]
    if status == "full":
        rec.branch["reach_V"] += 1
        return "leaf", dict(rounds=st["rounds"], src=list(st["B"]), sub=sub, kind="reach_V")
    # ---- stall
    U = st["U"]
    q = r - U.dim
    B, pool, T = st["B"], st["pool"], st["T"]
    rounds = st["rounds"]
    Rcols = [i for rnd in rounds for i in rnd["S"]]
    Rset = set(Rcols)
    Fr = [i for i in sub if i not in Rset]
    assert sorted(Fr) == sorted(B + pool + T)
    inU = dict(zip(sub, U.contains_many(cols[sub])))
    Fin = [i for i in Fr if inU[i]]
    BinU = [i for i in B if inU[i]]
    b = len(BinU)
    eps = U.dim - b
    X = [i for i in Fr if not inU[i]]
    Rout = [i for i in Rcols if not inU[i]]
    Up = U.copy()
    Up.add_many(cols[Rout])
    qp = r - Up.dim
    pi = len(pool)
    rec.branch["stall"] += 1
    ctx = dict(depth=depth, r=r, q=q, b=b, eps=eps, qp=qp, pi=pi, M=M)
    rec.events.append(ctx)
    # Theorem 2(b) decomposition and its consequences
    rec.sl("T2b_decomp", 0 if M == r + len(Rcols) + pi + len(T) else -1, ctx)
    rec.sl("T2b_rounds", DJ(r, J) - DJ(q, J) - len(Rcols), ctx)
    rec.sl("T2b_unused", q - len(T), ctx)
    rec.sl("pi_ge_2", pi - 2, ctx)
    rec.sl("pi_lower", pi - ((par.C - 1) * r + DJ(q, J) - q), ctx)
    # Corollary A
    BU = Ech(p, a)
    BU.add_many(cols[BinU])
    rec.sl("CorA_pool_in_span", 0 if all(BU.contains(cols[i]) for i in pool) else -1, ctx)
    rec.sl("CorA_b_ge_1", b - 1, ctx)
    rec.sl("CorA_BminusU", 0 if len(B) - b == q + eps else -1, ctx)
    rec.sl("U_vs_Uplus", 0 if all(Up.contains(cols[i]) for i in Rcols + Fin) else -1, ctx)
    if eps == 0:
        rec.branch["case1_closure"] += 1
        sp = Ech(p, a)
        sp.add_many(cols[Fin])
        rec.sl("case1_Fin_spans_U", 0 if sp.dim == U.dim else -1, ctx)
        return "leaf", dict(rounds=rounds, src=Fin, sub=sub, kind="case1")
    if b <= q:
        rec.branch["case2_Y"] += 1
        tgt = recurse_target(Fd, cols, sub, BU, par, rec, "Y", r)
        rec.sl("Y_ineq", b + pi - par.F(b), ctx)
        rec.sl("Y_cols_ge_b_pi", len(tgt) - (b + pi), ctx)
        return solve(Fd, cols, tgt, par, rec, depth + 1)
    # case 3
    rec.sl("case3_r_ge_2q2", r - (2 * q + 2), ctx)
    rec.sl("case3_X_le_r_1", (r - 1) - len(X), ctx)
    outsideUp = [i for i in sub if not Up.contains(cols[i])]
    rec.sl("case3_outUp_in_X", 0 if set(outsideUp) <= set(X) else -1, ctx)
    if qp >= 2 * (J - 1):
        rec.branch["case30_Uplus"] += 1
        rec.sl("I2", (par.F(r) - par.F(r - qp)) - (r - 1), ctx)
        rec.sl("c30_outside", (par.F(r) - par.F(r - qp)) - len(outsideUp), ctx)
        tgt = recurse_target(Fd, cols, sub, Up, par, rec, "U+30", r)
        return solve(Fd, cols, tgt, par, rec, depth + 1)
    part = {}
    for li, rnd in enumerate(rounds):
        for i in rnd["S"]:
            part[i] = li
    I, Zc, cert = matroid_intersection(Fd, cols, U, Rout, [part[i] for i in Rout], c,
                                       zcert=getattr(par, "zcert", "toX2"))
    if getattr(par, "least_load", False):
        need = 0
        while True:
            I0, _, _ = matroid_intersection(Fd, cols, U, Rout, [part[i] for i in Rout], need)
            if len(I0) == q - qp:
                break
            need += 1
        rec.least_loads.append(need)
    rec.sl("MI_cert", 0 if cert["r1Z"] + cert["r2"] == len(I) else -1, ctx)
    # least load (for reporting): smallest capacity giving a complete absorption
    if len(I) < q - qp:
        rec.branch["case31_W"] += 1
        rec.sl("c31_q_gt_c", q - (c + 1), ctx)
        W = U.copy()
        W.add_many(cols[Zc])
        qW = r - W.dim
        outW = [i for i in sub if not W.contains(cols[i])]
        bound = (qW - 1) + ((qW - 1) // c) * (r + 1 - c) + (r - 1)
        ctx2 = dict(ctx, qW=qW, I=len(I), outW=len(outW))
        rec.sl("M_qW_ge_c1", qW - (c + 1), ctx2)
        rec.sl("M_qW_le_q", q - qW, ctx2)
        rec.sl("M_outside_bound", bound - len(outW), ctx2)
        rec.sl("M_r2_le_qW_1", (qW - 1) - cert["r2"], ctx2)
        rec.sl("I1", (par.F(r) - par.F(r - qW)) - bound, ctx2)
        rec.sl("M_outside_in_RoutZ_X", 0 if set(outW) <= (set(Rout) - set(Zc)) | set(X) else -1,
               ctx2)
        tgt = recurse_target(Fd, cols, sub, W, par, rec, "W", r)
        return solve(Fd, cols, tgt, par, rec, depth + 1)
    # complete absorption with load <= c
    if par.abs_order == "reverse":
        I = I[::-1]
    elif par.abs_order == "random":
        I = I[:]
        par.rng.shuffle(I)
    rounds = absorb(Fd, cols, rounds, I, part, rec, ctx)
    loads = Counter(part[i] for i in I)
    ml = max(loads.values()) if loads else 0
    rec.loads.append(ml)
    rec.sl("load_le_c", c - ml, ctx)
    Uab = flag_space(Fd, cols, rounds)
    rec.sl("absorbed_realizes_Uplus", 0 if Uab.dim == Up.dim else -1, ctx)
    if qp == 0:
        rec.branch["case32_leafB"] += 1
        return "leaf", dict(rounds=rounds, src=list(B), sub=sub, kind="case32")
    m = qp
    rec.sl("c33_m_le_2J3", (2 * J - 3) - m, ctx)
    FrH = [i for i in Fr if Up.contains(cols[i])]
    sp = Ech(p, a)
    sp.add_many(cols[FrH])
    if sp.dim == Up.dim:
        rec.branch["case33_closure"] += 1
        return "leaf", dict(rounds=rounds, src=FrH, sub=sub, kind="case33_closure")
    Xp = [i for i in Fr if not Up.contains(cols[i])]
    rec.sl("c33_Xp_eq_outside", 0 if sorted(Xp) == sorted(outsideUp) else -1, ctx)
    if len(Xp) <= par.F(r) - par.F(r - m):
        rec.branch["case33_Uplus"] += 1
        tgt = recurse_target(Fd, cols, sub, Up, par, rec, "U+33", r)
        return solve(Fd, cols, tgt, par, rec, depth + 1)
    rec.branch["case33_top"] += 1
    rec.sl("Tmc_m_le_J2", (J - 2) - m, ctx)
    return top_phase(Fd, cols, sub, par, rec, depth, rounds, Up, Fr, Xp, m, r, ctx)


def absorb(Fd, cols, rounds, I, part, rec, ctx):
    rounds = [dict(rnd, blocks=[list(G) for G in rnd["blocks"]]) for rnd in rounds]
    for i in I:
        rnd = rounds[part[i]]
        bi = next(k for k, G in enumerate(rnd["blocks"]) if i in G)
        if len(rnd["blocks"][bi]) < 2:
            rec.sl("LemmaR_block_ge_2", -1, ctx)
            raise Fail("absorption from a singleton block")
        rnd["blocks"][bi].remove(i)
        rnd["blocks"].append([i])
        rnd["load"] = rnd.get("load", 0) + 1
    return rounds


def top_phase(Fd, cols, sub, par, rec, depth, rounds, H, Fr, Xp, m, r, ctx):
    p, a = Fd.p, cols.shape[1]
    # reserve Z: a basis of V/H inside X'
    Hz = H.copy()
    Z = []
    order = list(Xp)
    if par.z_rule == "random":
        order = order[:]
        par.rng.shuffle(order)
    for i in order:
        if Hz.add(cols[i]):
            Z.append(i)
        if Hz.dim == r:
            break
    rec.sl("Tm_Z_size", 0 if len(Z) == m else -1, ctx)
    Zs = set(Z)
    L = [i for i in Xp if i not in Zs]
    Hc = H.copy()
    top = []
    while Hc.dim < r:
        pos, res = scan(Fd, cols, Hc, L, r - Hc.dim)
        if pos is None:
            mp = r - Hc.dim
            outH = [i for i in sub if not Hc.contains(cols[i])]
            ctx2 = dict(ctx, mp=mp, outH=len(outH))
            rec.branch["top_stall_rec"] += 1
            rec.sl("Tmb_outside", (m + mp) - len(outH), ctx2)
            rec.sl("TS", (par.F(r) - par.F(r - mp)) - (m + mp), ctx2)
            rec.sl("Tmb_mp_le_m", m - mp, ctx2)
            tgt = recurse_target(Fd, cols, sub, Hc, par, rec, "Hcur", r)
            return solve(Fd, cols, tgt, par, rec, depth + 1)
        delta = res
        cc = L[pos]
        if len(delta) == 1:
            L.pop(pos)       # in H_cur: set aside (stays free, becomes a source)
            continue
        S = sorted(delta)
        for i in S:
            L.remove(i)
        e = np.zeros(a, dtype=I64)
        for i in S:
            e = (e + delta[i] * cols[i]) % p
        if not Hc.contains(e):
            raise Fail("top e not in H_cur")
        cls = {Fd.cls(delta[i]) for i in S}
        if len(cls) == 1 and not e.any():
            z = Fd.elem_of_class(-cls.pop())
            rec.branch["direct_top"] += 1
            return "solution", {i: z * delta[i] % p for i in S}
        rnd = dict(S=S, delta=delta, blocks=[[i] for i in S], kind="top", load=0,
                   q_at=r - Hc.dim)
        rec.sl("Tma_top_blocks_le_m1", (m + 1) - len(S), ctx)
        for i in S[1:]:
            if not Hc.add(delta[i] * cols[i] % p):
                raise Fail("top F1")
        top.append(rnd)
    rec.branch["top_leaf"] += 1
    used = {i for rnd in top for i in rnd["S"]}
    src = [i for i in Fr if i not in used]
    return "leaf", dict(rounds=rounds + top, src=src, sub=sub, kind="top_leaf")


def run_algt(Fd, cols, par, rec=None):
    rec = rec or Rec()
    cols = np.array(cols, dtype=I64) % Fd.p
    sub = list(range(len(cols)))
    out = solve(Fd, cols, sub, par, rec)
    return out, rec


# ---------------------------------------------------------------------------
# back substitution (Lemma 2 of Q1), with steering


def good_exact(Fd, betas, classes):
    """All s with beta_b + s in Q_{-c_b} u {0} for all b (needs the class table)."""
    p = Fd.p
    t = Fd.table
    # The class table exists only for p <= 3e6 (la.Fq), so int64 indices are exact here. With
    # QS_BIGP=1, dtype=I64 (object) made t[y] raise IndexError; found 9 Nov when the interesting/
    # case-3.3 banks were added to bigp_equiv.py (audit P6). Unreachable at p > 3e6 (table None).
    s = np.arange(p, dtype=np.int64)
    ok = np.ones(p, dtype=bool)
    for bt, cb in zip(betas, classes):
        y = (s + int(bt)) % p
        cy = t[y]
        ok &= (cy == -1) | (cy == (-cb) % Fd.k)
    return np.nonzero(ok)[0]


class BackSub:
    def __init__(self, Fd, cols, leaf):
        self.Fd = Fd
        p = Fd.p
        self.cols = np.array(cols, dtype=I64) % p
        self.rounds = leaf["rounds"]
        self.src = leaf["src"]
        basis, self.slots = [], []
        for rnd in self.rounds:
            Ws, e = round_vectors(Fd, self.cols, rnd)
            sl = []
            for w in Ws[1:]:
                sl.append(len(basis))
                basis.append([int(x) for x in w])
            self.slots.append(sl)
            rnd["_e"] = e
        self.dim = len(basis)
        self.cs = CoordSolver(p, basis)
        self.ecoord = [self.cs.coords(rnd["_e"]) for rnd in self.rounds]
        self.scoord = [self.cs.coords(self.cols[s]) for s in self.src]
        assert all(v is not None for v in self.ecoord + self.scoord)
        self.bcls = [[Fd.cls(rnd["delta"][G[0]]) for G in rnd["blocks"]] for rnd in self.rounds]
        rho = 0
        for cl in self.bcls:
            for x in range(len(cl)):
                for y in range(x + 1, len(cl)):
                    rho += cl[x] != cl[y]
        self.rho = rho

    def one_pass(self, rng, maxdraw=None):
        Fd, p = self.Fd, self.Fd.p
        x = {}
        co = [0] * self.dim
        for s, sc in zip(self.src, self.scoord):
            t = Fd.rand_P(rng)
            x[s] = t
            for j in range(self.dim):
                co[j] = (co[j] - t * sc[j]) % p
        coinc = 0
        for l in range(len(self.rounds) - 1, -1, -1):
            rnd = self.rounds[l]
            sl = self.slots[l]
            betas = [0] + [co[j] for j in sl]
            cl = self.bcls[l]
            forced = None
            for u in range(len(betas)):
                for v in range(u + 1, len(betas)):
                    if cl[u] != cl[v] and betas[u] == betas[v]:
                        forced = (-betas[u]) % p
            if forced is not None:
                coinc += 1
                if all(Fd.in_Q0(bt + forced, -cb) for bt, cb in zip(betas, cl)):
                    s = forced
                else:
                    return None, dict(fail="coincidence", level=l, coinc=coinc)
            else:
                s = None
                cap = maxdraw or (200 * Fd.k ** len(betas) + 1000)
                for _ in range(cap):
                    y = rng.randrange(p)
                    if all(Fd.in_Q0(bt + y, -cb) for bt, cb in zip(betas, cl)):
                        s = y
                        break
                if s is None:
                    if Fd.table is not None:
                        g = good_exact(Fd, betas, cl)
                        if len(g) == 0:
                            return None, dict(fail="empty_good", level=l, coinc=coinc)
                        s = int(g[rng.randrange(len(g))])
                    else:
                        return None, dict(fail="draw_cap", level=l, coinc=coinc)
            for b, G in enumerate(rnd["blocks"]):
                for i in G:
                    x[i] = rnd["delta"][i] * (betas[b] + s) % p
            for j in sl:
                co[j] = 0
            ec = self.ecoord[l]
            for j in range(self.dim):
                co[j] = (co[j] - s * ec[j]) % p
        if any(co):
            return None, dict(fail="residual", coinc=coinc)
        return x, dict(coinc=coinc)

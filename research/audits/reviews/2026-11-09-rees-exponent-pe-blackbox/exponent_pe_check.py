"""Finite control for the exponent-p^e black-box route (9 Nov 2026, AI only).

Run from the repo root:
    nice -n 19 /opt/anaconda3/bin/python -m research.audits.reviews.\
2026-11-09-rees-exponent-pe-blackbox.exponent_pe_check
(or with PYTHONPATH=. and the file path).

What it checks, on black-box p-groups of class c < p and exponent p^e > p exported from
GAP (groups.txt, written by export_groups.g):

  1. Chart acquisition over Z/M, M = exponent found from generator orders through the
     multiplication oracle (regularity): the free Lazard pullback Phi on F_{s,c}(Z/M) in its
     Lyndon basis, images by the certified inverse-BCH words (theorems/universal_lazard_words),
     ker Phi as a lattice, the chart L_G = Z^d / ker Phi by Smith normal form, structure
     constants projected from the integer bracket table of the free Lie ring, and the map
     E(t) = Phi(sum t_i u_i). Graded: E is a bijection onto G and a homomorphism
     (L_G, BCH) -> G on sampled pairs.
  2. Kernel readout as in Lemma tb-kernel: t uniform samples of (ker Phi)^perp (the exact-QFT
     law), congruence solve, comparison with ker Phi.
  3. Algorithm RtF (Proposition tb-recursion) on the acquired chart, for every exported
     subgroup H. Each field call is validated against Definition def:input-contract: an
     explicit F_p tensor (antisymmetry, Jacobi, class <= c), the lift a -> sum a_i b_i being a
     group map into (S/K, *), and f o E o lift hiding the true (h/K) cap M[p]. The field
     solver is an ORACLE-ONLY brute force (U = {a : f(a) = f(0)}), a stand-in for Theorem
     thm:main; it is not Theorem thm:main. The Schedule-1 query bound of thm:main is tallied
     per call from (dim, g_d).
  4. Negative controls: the cover-socle push-forward (Prop black-box(iii)) and the frozen
     normalizer (no idealizer step).

The ground truth (closures, coset labels) is computed with the hidden permutations and is
used only to build f and to grade. Finite check: it proves nothing for other groups.
"""
from __future__ import annotations

import ast
import json
import math
import random
import sys
import time
from itertools import product
from pathlib import Path

from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_decomp

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from theorems.universal_lazard_words import UniversalLazardWords  # noqa: E402

HERE = Path(__file__).resolve().parent


# ------------------------------------------------------------------ black box
class BlackBox:
    def __init__(self, gens, seed):
        self._rng = random.Random(seed)
        self._h, self._k = {}, {}
        deg = len(gens[0])
        self.identity = self._handle(tuple(range(deg)))
        self.generators = [self._handle(tuple(g)) for g in gens]
        self.calls = 0

    def _handle(self, key):
        h = self._h.get(key)
        if h is None:
            while True:
                h = self._rng.getrandbits(40)
                if h not in self._k:
                    break
            self._h[key], self._k[h] = h, key
        return h

    def mul(self, x, y):
        self.calls += 1
        return self.truth_mul(x, y)

    # grading / oracle construction only
    def truth_mul(self, x, y):
        a, b = self._k[x], self._k[y]
        return self._handle(tuple(b[i] for i in a))

    def handle_of_perm(self, perm):
        return self._handle(tuple(perm))

    def closure(self, gens):
        seen, frontier = {self.identity}, [self.identity]
        while frontier:
            new = []
            for g in frontier:
                for s in gens:
                    h = self.truth_mul(g, s)
                    if h not in seen:
                        seen.add(h)
                        new.append(h)
            frontier = new
        return seen


# ------------------------------------------------------------------ free Lie ring over Z
def lyndon_words(s, c):
    out = []
    for k in range(1, c + 1):
        for w in product(range(s), repeat=k):
            if all(w < w[i:] + w[:i] for i in range(1, k)):
                out.append(w)
    return out


def std_factor(w):
    for i in range(1, len(w)):
        v = w[i:]
        if all(v < v[j:] + v[:j] for j in range(1, len(v))):
            return w[:i], v  # longest proper Lyndon suffix = first i giving Lyndon suffix
    raise ValueError


def amul(a, b, c):
    out = {}
    for u, x in a.items():
        for v, y in b.items():
            if len(u) + len(v) <= c:
                out[u + v] = out.get(u + v, 0) + x * y
    return {w: x for w, x in out.items() if x}


def abr(a, b, c):
    out = amul(a, b, c)
    for w, x in amul(b, a, c).items():
        out[w] = out.get(w, 0) - x
    return {w: x for w, x in out.items() if x}


class FreeLieZ:
    """Free nilpotent Lie ring of class c over Z, Lyndon basis with standard bracketing."""

    def __init__(self, s, c):
        self.s, self.c = s, c
        self.words = lyndon_words(s, c)
        self.index = {w: i for i, w in enumerate(self.words)}
        self.d = len(self.words)
        self.poly = {}
        for w in sorted(self.words, key=len):
            if len(w) == 1:
                self.poly[w] = {w: 1}
            else:
                u, v = std_factor(w)
                self.poly[w] = abr(self.poly[u], self.poly[v], c)
            assert min(self.poly[w]) == w and self.poly[w][w] == 1  # triangularity
        self.table = [[self.coords(abr(self.poly[a], self.poly[b], c)) for b in self.words]
                      for a in self.words]

    def coords(self, q):
        q, out = dict(q), [0] * self.d
        while q:
            u = min(q)
            x = q[u]
            j = self.index[u]  # raises if u is not Lyndon: q was not a Lie element
            out[j] += x
            for w, y in self.poly[u].items():
                q[w] = q.get(w, 0) - x * y
                if q[w] == 0:
                    del q[w]
        return out

    def bracket(self, x, y):
        out = [0] * self.d
        for i, a in enumerate(x):
            if a:
                for j, b in enumerate(y):
                    if b:
                        row = self.table[i][j]
                        for k, z in enumerate(row):
                            if z:
                                out[k] += a * b * z
        return out


# ------------------------------------------------------------------ chart ring
class ChartRing:
    """L = (+)_i Z/mods_i with integer tensor T[i][j] (list over k)."""

    def __init__(self, p, mods, T, c):
        self.p, self.mods, self.T, self.c = p, mods, T, c
        self.n = len(mods)
        self.M = max(mods) if mods else 1
        self.zero = (0,) * self.n

    def red(self, v):
        return tuple(int(x) % m for x, m in zip(v, self.mods))

    def add(self, x, y):
        return tuple((a + b) % m for a, b, m in zip(x, y, self.mods))

    def neg(self, x):
        return tuple((-a) % m for a, m in zip(x, self.mods))

    def smul(self, r, x):
        return tuple((r * a) % m for a, m in zip(x, self.mods))

    def br(self, x, y):
        out = [0] * self.n
        for i, a in enumerate(x):
            if a:
                for j, b in enumerate(y):
                    if b:
                        row = self.T[i][j]
                        for k in range(self.n):
                            if row[k]:
                                out[k] += a * b * row[k]
        return self.red(out)

    def bch(self, x, y):
        inv = lambda q: pow(q, -1, self.M)
        xy = self.br(x, y)
        z = self.add(x, y)
        if self.c >= 2:
            z = self.add(z, self.smul(inv(2), xy))
        if self.c >= 3:
            z = self.add(z, self.smul(inv(12), self.br(x, xy)))
            z = self.add(z, self.smul((-inv(12)) % self.M, self.br(y, xy)))
        if self.c >= 4:
            z = self.add(z, self.smul((-inv(24)) % self.M, self.br(y, self.br(x, xy))))
        if self.c >= 5:
            raise NotImplementedError("BCH implemented to degree 4")
        return z

    def elements(self):
        return list(product(*[range(m) for m in self.mods]))


class HNF:
    """Upper-triangular Hermite basis of a lattice L with M Z^d <= L <= Z^d."""

    def __init__(self, d, M):
        self.d, self.rows = d, [[M if i == j else 0 for j in range(d)] for i in range(d)]

    def insert(self, v):
        v, B = list(v), self.rows
        for i in range(self.d):
            if v[i] == 0:
                continue
            a, b = B[i][i], v[i]
            g, x, y = _egcd(a, b)
            new = [x * s + y * t for s, t in zip(B[i], v)]
            v = [(a // g) * t - (b // g) * s for s, t in zip(B[i], v)]
            B[i] = new
            assert v[i] == 0
        assert not any(v)
        for i in range(self.d - 1, -1, -1):
            if B[i][i] < 0:
                B[i] = [-x for x in B[i]]
            for j in range(i + 1, self.d):
                q = B[i][j] // B[j][j]
                if q:
                    B[i] = [s - q * t for s, t in zip(B[i], B[j])]


def _egcd(a, b):
    if b == 0:
        return (a, 1, 0) if a >= 0 else (-a, -1, 0)
    g, x, y = _egcd(b, a % b)
    return g, y, x - (a // b) * y


def smith(rows, d):
    """rows: list of integer d-vectors spanning K (row space). Returns (deltas, Vinv, V)
    with K = (+)_i delta_i * Vinv[i], Z^d basis Vinv rows, coordinate map y -> y V."""
    A = Matrix(rows)
    S, U, V = smith_normal_decomp(A)  # S = U*A*V
    assert S == U * A * V
    deltas = [abs(int(S[i, i])) if i < min(S.shape) else 0 for i in range(d)]
    Vinv = V.inv()
    return deltas, [[int(x) for x in Vinv.row(i)] for i in range(d)], V


# ------------------------------------------------------------------ helpers
def parse_groups(path):
    groups, cur = [], None
    for line in path.read_text().splitlines():
        if line.startswith("GROUP "):
            tag, p, order, cl, ex, deg = line.split()[1:]
            cur = dict(tag=tag, p=int(p), order=int(order), cls=int(cl), exp=int(ex),
                       deg=int(deg), subs=[])
            groups.append(cur)
        elif line.startswith("GENS "):
            cur["gens"] = [[x - 1 for x in g] for g in ast.literal_eval(line[5:])]
        elif line.startswith("SUB "):
            cur["subs"].append([[x - 1 for x in g] for g in ast.literal_eval(line[4:])])
    return groups


def pad(perm, deg):
    return list(perm) + list(range(len(perm), deg))


def B_d(d, a):
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** math.ceil(math.log2(d + 1))


def schedule1_queries(c, m, gds, eps, p):
    tau = math.ceil(math.log(3 / eps, p))
    q = c * (m + tau)
    for d, g in zip(range(2, c + 1), gds):
        q *= B_d(d, g)
    return q


def lcs_dims_fp(T, k, p, c):
    """dims of gamma_d (d=2..c) of the F_p algebra with tensor T; checks class <= c."""
    def rank(vecs):
        rows = [list(v) for v in vecs if any(v)]
        r, col = 0, 0
        rows = [[x % p for x in v] for v in rows]
        ncol = k
        while rows and col < ncol:
            piv = next((i for i in range(r, len(rows)) if rows[i][col]), None)
            if piv is None:
                col += 1
                continue
            rows[r], rows[piv] = rows[piv], rows[r]
            iv = pow(rows[r][col], -1, p)
            rows[r] = [x * iv % p for x in rows[r]]
            for i in range(len(rows)):
                if i != r and rows[i][col]:
                    f = rows[i][col]
                    rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
            r += 1
            col += 1
        return r, rows[:r]

    def brv(x, y):
        out = [0] * k
        for i in range(k):
            if x[i]:
                for j in range(k):
                    if y[j]:
                        for t in range(k):
                            out[t] += x[i] * y[j] * T[i][j][t]
        return [v % p for v in out]

    basis = [[int(i == j) for j in range(k)] for i in range(k)]
    cur, dims = basis, []
    for d in range(2, c + 2):
        nxt = [brv(x, e) for x in cur for e in basis]
        r, cur = rank(nxt)
        if d <= c:
            dims.append(r)
        else:
            assert r == 0, "class exceeds c"
    return dims


# ------------------------------------------------------------------ one group
def run_group(g, rng, eps=0.1, max_subs=None, log=print):
    t0 = time.time()
    p, c = g["p"], g["cls"]
    deg = g["deg"]
    box = BlackBox([pad(x, deg) for x in g["gens"]], seed=rng.getrandbits(32))
    s = len(box.generators)
    # exponent from generator orders through the oracle (regular: class < p)
    def ppow(x):
        y = box.identity
        for _ in range(p):
            y = box.mul(y, x)
        return y
    e = 0
    for x in box.generators:
        j, y = 0, x
        while y != box.identity:
            y, j = ppow(y), j + 1
        e = max(e, j)
    M = p ** e
    assert M == g["exp"], (M, g["exp"])
    W = UniversalLazardWords(p, c, box.identity, box.mul, modulus=M)
    F = FreeLieZ(s, c)
    d = F.d
    # images of the Lyndon basis by bracket programs
    img = {}
    for w in sorted(F.words, key=len):
        if len(w) == 1:
            img[w] = box.generators[w[0]]
        else:
            u, v = std_factor(w)
            img[w] = W.lie_bracket(img[u], img[v])
    h = [img[w] for w in F.words]
    # ker Phi by Schreier relations of the additive BFS (finite-check device; the
    # algorithm uses Fourier sampling, simulated below from the exact law)
    pre = {box.identity: [0] * d}
    order, lat = [box.identity], HNF(d, M)
    qi = 0
    while qi < len(order):
        a = order[qi]
        qi += 1
        for j in range(d):
            b = W.lie_add(a, h[j])
            v = pre[a][:]
            v[j] += 1
            if b in pre:
                r = [x - y for x, y in zip(v, pre[b])]
                if any(r):
                    lat.insert(r)
            else:
                pre[b] = v
                order.append(b)
    assert len(pre) == g["order"], "image is not all of G"
    deltas, Vinv, V = smith(lat.rows, d)
    keep = [i for i in range(d) if deltas[i] != 1]
    assert all(deltas[i] != 0 and M % deltas[i] == 0 for i in keep)
    mods = [deltas[i] for i in keep]
    lifts = [Vinv[i] for i in keep]
    Vcols = [[int(V[r, i]) for r in range(d)] for i in keep]

    def chart_coord(y):  # Z^d -> L_G
        return tuple(sum(a * b for a, b in zip(y, col)) % m for col, m in zip(Vcols, mods))

    T = [[list(chart_coord(F.bracket(lifts[i], lifts[j]))) for j in range(len(mods))]
         for i in range(len(mods))]
    L = ChartRing(p, mods, T, c)
    n, b = len(mods), sum(round(math.log(m, p)) for m in mods)
    assert p ** b == g["order"]
    # kernel readout from the exact Fourier law (uniform on K^perp), Lemma tb-kernel
    ell = 40
    delta = eps / 4
    tsamp = min(d, math.floor(ell / math.log2(p))) + math.ceil(math.log(2 / delta, p))
    dual = [[int(V[r, i]) for i in range(d)] for r in range(d)]  # rows: V^T columns
    readout_ok = 0
    trials = 20
    allmods = [deltas[i] if deltas[i] else M for i in range(d)]
    for _ in range(trials):
        A = []
        for _ in range(tsamp):
            cvec = [(M // allmods[i]) * rng.randrange(allmods[i]) for i in range(d)]
            A.append([sum(cvec[i] * int(V[r, i]) for i in range(d)) % M for r in range(d)])
        # K' = {u : A u = 0 mod M}; K' == K iff same index and K subset K'
        S2, U2, V2 = smith_normal_decomp(Matrix(A))
        sd = [int(S2[i, i]) if i < min(S2.shape) else 0 for i in range(d)]
        idx = 1
        for x in sd:
            idx *= M // math.gcd(x, M)
        contains = all(sum(a * r for a, r in zip(row, kv)) % M == 0 for row in A
                       for kv in [[deltas[i] * Vinv[i][j] for j in range(d)] for i in range(d)])
        readout_ok += int(contains and idx == g["order"])
    # E(t) = Phi(sum t_i lift_i) via Lazard combinations
    a_img = [W.linear_combination(h, [x % M for x in lift]) for lift in lifts]
    elems = L.elements()
    E = {t: W.linear_combination(a_img, list(t)) for t in elems}
    assert len(set(E.values())) == g["order"]
    for _ in range(400):
        x, y = rng.choice(elems), rng.choice(elems)
        assert E[L.bch(x, y)] == box.truth_mul(E[x], E[y]), "E is not a homomorphism"
    Einv = {v: k for k, v in E.items()}
    Gset = set(E.values())
    chart_s = time.time() - t0

    # ------------------------------------------------ RtF on the chart, every subgroup
    subs = g["subs"] if max_subs is None else g["subs"][:max_subs]
    stats = dict(subs=0, ok=0, calls_max=0, cap=b, instances=0, nonabelian_instances=0,
                 cover_socle_misses=0, frozen_normalizer_nonideal=0, q_bound_max=0)
    pE = {t: L.smul(p, t) for t in elems}
    for sg in subs:
        Hh = [box.handle_of_perm(pad(x, deg)) for x in sg] or [box.identity]
        Hset = box.closure(Hh)
        hset = {Einv[x] for x in Hset}
        # coset labels for f(x)=f(y) iff x^{-1}y in H: left cosets xH
        label, nxt = {}, 0
        for x in Gset:
            if x not in label:
                for y in Hset:
                    label[box.truth_mul(x, y)] = nxt
                nxt += 1
        f = lambda t: label[E[t]]
        # negative control N1: cover socle image (M/p)F -> p^{e-1} L_G versus L_G[p]
        cover_soc = {L.smul(M // p, t) for t in elems}
        socle = {t for t in elems if pE[t] == L.zero}
        if (hset & socle) - cover_soc:
            stats["cover_socle_misses"] += 1
        # RtF
        K, gensK, S = {L.zero}, [], set(elems)
        calls, qtot, frozen_flag = 0, 0, False
        while True:
            if S == K:
                break
            P = [x for x in S if pE[x] in K]
            span, coord, basis = set(K), {k: () for k in K}, []
            for x in P:
                if x in span:
                    continue
                basis.append(x)
                newspan, newcoord = set(), {}
                for y in span:
                    for a in range(p):
                        z = L.add(y, L.smul(a, x))
                        newspan.add(z)
                        newcoord[z] = coord[y] + (a,)
                coord = {z: v + (0,) * (len(basis) - len(v)) for z, v in newcoord.items()}
                span = newspan
            k = len(basis)
            assert set(P) == span and len(P) == len(K) * p ** k
            co = lambda z: coord[z]

            def lift(a):
                z = L.zero
                for ai, bi in zip(a, basis):
                    z = L.add(z, L.smul(ai, bi))
                return z
            Tw = [[list(co(L.br(basis[i], basis[j]))) for j in range(k)] for i in range(k)]
            # instance validation (Definition def:input-contract)
            for i in range(k):
                for j in range(k):
                    assert all((Tw[i][j][t] + Tw[j][i][t]) % p == 0 for t in range(k))
            gds = lcs_dims_fp(Tw, k, p, c)
            Om = ChartRing(p, [p] * k, Tw, c)
            vecs = Om.elements()
            for _ in range(60):
                x, y, z = rng.choice(vecs), rng.choice(vecs), rng.choice(vecs)
                jac = Om.add(Om.add(Om.br(x, Om.br(y, z)), Om.br(y, Om.br(z, x))), Om.br(z, Om.br(x, y)))
                assert jac == Om.zero
                assert co(L.bch(lift(x), lift(y))) == Om.bch(x, y), "lift is not a group map"
            Utrue = {co(z) for z in hset & set(P)} if K <= hset <= S else None
            fo = {a: f(lift(a)) for a in vecs}
            if Utrue is not None:
                for _ in range(120):
                    x, y = rng.choice(vecs), rng.choice(vecs)
                    assert (fo[x] == fo[y]) == (Om.bch(Om.neg(x), y) in Utrue), "not hiding"
            stats["instances"] += 1
            stats["nonabelian_instances"] += int(any(gds))
            qtot += schedule1_queries(c, k, gds, eps / (2 * b), p)
            # oracle-only brute-force field solver (stand-in for Theorem thm:main)
            U = {a for a in vecs if fo[a] == fo[Om.zero]}
            calls += 1
            if Utrue is not None:
                assert U == Utrue
            if U == {Om.zero} or any(Om.br(x, y) not in U for x in U for y in U):
                break
            Kn = {z for z in P if co(z) in U}
            ubasis, uspan = [], {Om.zero}
            for u in sorted(U):
                if u not in uspan:
                    ubasis.append(u)
                    uspan = {Om.add(y, Om.smul(a, u)) for y in uspan for a in range(p)}
            assert uspan == U
            gensK = gensK + [lift(u) for u in ubasis]
            # N2: frozen normalizer -- is K' an ideal of the whole chart?
            if any(L.br(x, gk) not in Kn for x in mods_basis(L) for gk in gensK):
                frozen_flag = True
            Sn = {x for x in S if all(L.br(x, gk) in Kn for gk in gensK)}
            assert Kn <= hset <= Sn, "invariant K <= h <= S broken"
            K, S = Kn, Sn
        assert calls <= b, (calls, b)
        out = box.closure([E[x] for x in gensK]) if gensK else {box.identity}
        stats["subs"] += 1
        stats["ok"] += int(out == Hset)
        stats["calls_max"] = max(stats["calls_max"], calls)
        stats["q_bound_max"] = max(stats["q_bound_max"], qtot)
        stats["frozen_normalizer_nonideal"] += int(frozen_flag)
    bound_all = b * schedule1_queries(c, n, [n] * (c - 1), eps / (2 * b), p)
    res = dict(tag=g["tag"], p=p, order=g["order"], cls=c, exponent=M, s=s, d=d,
               chart_mods=mods, n=n, b=b, readout_ok=f"{readout_ok}/{trials}", t_samples=tsamp,
               mults_chart=box.calls, chart_seconds=round(chart_s, 1),
               seconds=round(time.time() - t0, 1), q_bound_worst=bound_all, **stats)
    log(json.dumps(res))
    return res


def mods_basis(L):
    return [tuple(int(i == j) for j in range(L.n)) for i in range(L.n)]


def main():
    rng = random.Random(20261109)
    groups = parse_groups(HERE / "groups.txt")
    only = sys.argv[1:]
    results = []
    with open(HERE / "results.jsonl", "w") as fh:
        for g in groups:
            if only and g["tag"] not in only:
                continue
            r = run_group(g, rng, log=lambda s: (print(s, flush=True), fh.write(s + "\n"), fh.flush()))
            results.append(r)
    tot = sum(r["subs"] for r in results)
    ok = sum(r["ok"] for r in results)
    print(f"SUMMARY groups={len(results)} subgroups={tot} recovered={ok} "
          f"instances={sum(r['instances'] for r in results)} "
          f"nonabelian_instances={sum(r['nonabelian_instances'] for r in results)} "
          f"cover_socle_misses={sum(r['cover_socle_misses'] for r in results)} "
          f"frozen_nonideal={sum(r['frozen_normalizer_nonideal'] for r in results)}")


if __name__ == "__main__":
    main()

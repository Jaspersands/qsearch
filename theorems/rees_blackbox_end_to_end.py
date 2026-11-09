"""End-to-end black-box control for the Rees HSP at exponent p (finite, exact).

The group is a black box: elements are opaque random 40-bit handles, and the
only group operation is a multiplication oracle on handles (unique encoding).
Behind the box sits a matrix group (unitriangular, so class c < p); the
algorithm never sees a matrix. It runs, using public data (p, c, the
generator handles) and the oracle only:

1. Free pullback (main.tex, Proposition black-box (i)). A basis of the free
   nilpotent Lie algebra F = F_{s,c} over F_p by left-normed brackets of the
   generators (chosen greedily; the paper uses the Lyndon basis, and any basis
   of brackets serves); Phi(sum_b a_b b) is the Lazard linear combination of the
   images Phi(b), computed by the certified inverse-BCH words of
   theorems/universal_lazard_words.py (imported read-only). Phi is a Lie ring
   homomorphism F -> log G, so Phi(x) = Phi(y) iff x - y lies in K = ker Phi.
2. Kernel (Proposition black-box (iv), Lemma tb-kernel). Abelian Fourier
   sampling on (F, +) with hiding function Phi. The measurement law is
   computed from the fibres of Phi (every fibre's indicator is Fourier
   transformed, in floating point), never from K. t = min(d, floor(l/log2 p))
   + ceil(log_p(8/eps)) samples are drawn (Lemma tb-kernel at delta = eps/4);
   their common nullspace is the candidate kernel K'. Public check: each basis
   vector of K' must map to the identity, which catches K' not inside K; it
   cannot catch K' strictly inside K, which an exact sampler never produces
   but an approximate transform could. A rejected K' is resampled.
3. Chart. The quotient F/K with complement coordinates (non-pivot
   coordinates of the RREF kernel basis), structure constants by projection.
   Public checks: K is an ideal, the chart satisfies Jacobi, and the chart
   map y -> Phi(y) is a homomorphism from the BCH product on sampled pairs.
4. Core. The chart and the oracle f o exp_chart go to the scaled exact
   simulator theorems/rees_end_to_end_ext.py (imported read-only): Rees
   cover, Rule W arities, the deterministic Ivanyos-Santha solver, sparse
   exact states, level-set source preparation.
5. Output. The recovered basis of log H is mapped back through the chart to
   black-box handles; the subgroup they generate is compared with the true H
   (enumerated by closure, used only for grading).

Negative controls: (a) a naive pullback Phi'(x) = prod_b Phi(b)^{x_b}
(products of powers, not a homomorphism); (b) too few kernel samples (K' then
not inside K; caught); (c) a forced K' strictly inside K (K cap gamma_2(F)): NOT caught by
any public check, only by the grading-side bijectivity test.

What this does NOT show: it is an exponential-size classical simulation on
fixed tiny groups; it implements no quantum circuit for the pullback or the
kernel step, tests no asymptotic cost, and covers exponent p only (no
ring-to-field recursion, no Sylow split, no primes p <= c). A finite run can
only falsify. AI-written, AI-checked only; pending human review.
"""
from __future__ import annotations

import argparse
from itertools import product
import json
from math import ceil, floor, log, log2
from pathlib import Path
import random
import time

import numpy as np

from theorems import rees_end_to_end_sim as base
from theorems import rees_end_to_end_ext as ext
from theorems.universal_lazard_words import UniversalLazardWords


# ---------------------------------------------------------------- the black box

def _matmul(a, b, n, p):
    return tuple(sum(a[i*n+k]*b[k*n+j] for k in range(n)) % p for i in range(n) for j in range(n))


class BlackBox:
    """Opaque 40-bit handles for a finite group; multiplication oracle only.

    The group behind the box is given by hidden keys and a hidden product:
    n x n matrices over F_p (kind "matrix"), or coordinate vectors of a Lazard
    group with a BCH product (kind "bch", theorems/rees_end_to_end_sim.NilGroup).
    The algorithm sees handles, `identity`, `generators` and `mul` only."""

    def __init__(self, p, spec, generator_keys, seed):
        self.p, self.spec = p, spec
        self._rng = random.Random(seed)
        self._to_handle, self._to_key = {}, {}
        if spec[0] == "matrix":
            n = spec[1]
            ident = tuple(int(i == j) for i in range(n) for j in range(n))
            self._prod = lambda a, b: _matmul(a, b, n, p)
            self._prod_batch = lambda A, B: (A.reshape(-1, n, n) @ B.reshape(-1, n, n) % p).reshape(-1, n*n)
        else:
            G = spec[1]
            ident = (0,)*G.n
            self._prod = lambda a, b: tuple(int(v) for v in G.mul(np.array(a), np.array(b)))
            self._prod_batch = lambda A, B: G.mul(A, B)
        self.identity = self._handle(ident)
        self.generators = [self._handle(tuple(k)) for k in generator_keys]
        self.calls = 0
        self.encoding_bits = 40

    def _handle(self, key):
        if key not in self._to_handle:
            while True:
                h = self._rng.getrandbits(40)
                if h not in self._to_key:
                    break
            self._to_handle[key], self._to_key[h] = h, key
        return self._to_handle[key]

    def mul(self, x, y):
        self.calls += 1
        return self._handle(self._prod(self._to_key[x], self._to_key[y]))

    def mul_batch(self, xs, ys, chunk=1 << 20):
        """len(xs) oracle calls mul(xs[i], ys[i]), evaluated together (numpy). Same access
        model and count as the loop; only the simulation of the box is vectorised."""
        xs, ys = np.asarray(xs, dtype=np.int64), np.asarray(ys, dtype=np.int64)
        self.calls += len(xs)
        out = np.empty(len(xs), dtype=np.int64)
        for s in range(0, len(xs), chunk):
            A, B = self._keys(xs[s:s+chunk]), self._keys(ys[s:s+chunk])
            u, inv = np.unique(self._prod_batch(A, B), axis=0, return_inverse=True)
            hs = np.array([self._handle(tuple(int(v) for v in row)) for row in u], dtype=np.int64)
            out[s:s+chunk] = hs[inv.reshape(-1)]
        return out

    def _keys(self, hs):
        u, inv = np.unique(hs, return_inverse=True)
        keys = np.array([self._to_key[int(h)] for h in u], dtype=np.int64)
        return keys[inv.reshape(-1)]

    # -- grading only (never called by the algorithm)
    def truth_mul(self, x, y):
        return self._handle(self._prod(self._to_key[x], self._to_key[y]))

    def closure(self, generators):
        seen = {self.identity}
        frontier = [self.identity]
        while frontier:
            new = []
            for g in frontier:
                for s in generators:
                    h = self.truth_mul(g, s)
                    if h not in seen:
                        seen.add(h)
                        new.append(h)
            frontier = new
        return seen


# ---------------------------------------------------------------- free nilpotent Lie algebra

def _assoc_mul(a, b, c, p):
    out = {}
    for u, x in a.items():
        for v, y in b.items():
            if len(u)+len(v) <= c:
                w = u+v
                out[w] = (out.get(w, 0)+x*y) % p
    return {w: x for w, x in out.items() if x}


def _assoc_bracket(a, b, c, p):
    ab, ba = _assoc_mul(a, b, c, p), _assoc_mul(b, a, c, p)
    out = dict(ab)
    for w, x in ba.items():
        out[w] = (out.get(w, 0)-x) % p
    return {w: x for w, x in out.items() if x}


class FreeNilpotent:
    """F_{s,c} over F_p inside the truncated free associative algebra (valid for p > c:
    the free Lie algebra embeds in the tensor algebra over any field)."""

    def __init__(self, s, c, p):
        self.s, self.c, self.p = s, c, p
        self.monomials = [w for k in range(1, c+1) for w in product(range(s), repeat=k)]
        self._mindex = {w: i for i, w in enumerate(self.monomials)}
        words, vecs = [], []
        for k in range(1, c+1):
            for w in product(range(s), repeat=k):
                v = self._left_normed(w)
                if base.rref(vecs+[self._vec(v)], p).__len__() > len(vecs):
                    words.append(w)
                    vecs.append(self._vec(v))
        self.words, self._vecs = words, vecs
        self.dim = len(words)
        self.tensor = np.zeros((self.dim, self.dim, self.dim), dtype=np.int64)
        for a in range(self.dim):
            for b in range(self.dim):
                br = _assoc_bracket(self._left_normed(words[a]), self._left_normed(words[b]), c, p)
                co = base.coordinates(vecs, self._vec(br), p)
                if co is None:
                    raise ArithmeticError("bracket left the free Lie algebra")
                self.tensor[a, b] = co
        base.LieAlgebra("F", p, self.tensor).validate()

    def _left_normed(self, w):
        v = {(w[0],): 1}
        for i in w[1:]:
            v = _assoc_bracket(v, {(i,): 1}, self.c, self.p)
        return v

    def _vec(self, poly):
        out = [0]*len(self.monomials)
        for w, x in poly.items():
            out[self._mindex[w]] = x % self.p
        return tuple(out)


def free_rank(s, c):
    from sympy import mobius, divisors
    return sum(sum(mobius(d)*s**(k//d) for d in divisors(k))//k for k in range(1, c+1))


# ---------------------------------------------------------------- pullback and kernel step

def pullback_table(box, free, words_engine, naive=False):
    """Phi(x) for every x in F (C-order over coordinates). Returns array of handles."""
    p, d = free.p, free.dim
    images = []
    for w in free.words:
        v = box.generators[w[0]]
        for i in w[1:]:
            v = words_engine.lie_bracket(v, box.generators[i])
        images.append(v)
    table = {(0,)*d: box.identity}
    for x in product(range(p), repeat=d):
        if not any(x):
            continue
        j = max(i for i in range(d) if x[i])
        prev = x[:j]+(0,)+x[j+1:]
        step = words_engine.power(images[j], x[j])
        if naive:
            table[x] = box.mul(table[prev], step)          # product of powers: NOT a homomorphism
        else:
            table[x] = words_engine.lie_add(table[prev], step)
    order = list(product(range(p), repeat=d))
    return np.array([table[x] for x in order], dtype=np.int64), images


def fourier_law(labels, p, d):
    """Exact measurement law of abelian Fourier sampling with hiding function `labels`
    on (Z/p)^d: sum over fibres of |FFT(indicator)|^2 / |F|^2 (computed in floating point)."""
    N = p**d
    law = np.zeros((p,)*d)
    for val in np.unique(labels):
        ind = (labels == val).astype(float).reshape((p,)*d)
        law += np.abs(np.fft.fftn(ind))**2
    law = law.reshape(-1)/N**2
    return law


def las_vegas_rejects(box, labels, kernel, p, d):
    """Public Las Vegas check: the candidate kernel vectors that do NOT map to the identity.
    Phi(v) is read from the pullback table (the algorithm's own evaluator). It catches
    K' not inside K; it cannot see K' strictly inside K."""
    w = p**np.arange(d-1, -1, -1)
    return [v for v in kernel if labels[int(np.dot(v, w))] != box.identity]


def kernel_step(box, free, words_engine, labels, images, *, eps, rng, samples=None, naive=False):
    p, d = free.p, free.dim
    law = fourier_law(labels, p, d)
    l = box.encoding_bits
    k = samples if samples is not None else min(d, floor(l/log2(p)))+ceil(log(8/eps, p))
    coords = list(product(range(p), repeat=d))
    tries, record = 0, {}
    while True:
        tries += 1
        idx = rng.choice(len(law), size=k, p=law/law.sum())
        chars = [coords[i] for i in idx]
        kernel = base.rref(base.nullspace(chars, d, p), p)
        bad = las_vegas_rejects(box, labels, kernel, p, d)
        record = {"samples": int(k), "tries": tries, "kernel_dim": len(kernel),
                  "las_vegas_rejected_vectors": len(bad)}
        if not bad or samples is not None:
            return kernel, law, record
        if tries >= 20:
            raise RuntimeError("kernel step rejected 20 times")


# ---------------------------------------------------------------- chart

class Chart:
    def __init__(self, free, kernel, labels):
        p, d = free.p, free.dim
        self.p, self.free, self.kernel = p, free, kernel
        pivots = [next(j for j, x in enumerate(row) if x) for row in kernel]
        self.pivots = pivots
        self.free_coords = [j for j in range(d) if j not in pivots]
        self.n = len(self.free_coords)
        T = np.zeros((self.n, self.n, self.n), dtype=np.int64)
        for a, ja in enumerate(self.free_coords):
            for b, jb in enumerate(self.free_coords):
                T[a, b] = self.project(free.tensor[ja, jb])
        self.tensor = T
        self.labels = labels
        self._w = p**np.arange(d-1, -1, -1, dtype=np.int64)

    def project(self, x):
        x = [int(v) % self.p for v in x]
        for row, pc in zip(self.kernel, self.pivots):
            if x[pc]:
                coef = x[pc]
                x = [(a-coef*r) % self.p for a, r in zip(x, row)]
        return [x[j] for j in self.free_coords]

    def lift(self, y):
        x = np.zeros(self.free.dim, dtype=np.int64)
        x[self.free_coords] = np.asarray(y, dtype=np.int64)
        return x

    def exp(self, y):
        """Chart coordinates -> black-box handle, via the pullback table (vectorized)."""
        y = np.asarray(y, dtype=np.int64).reshape(-1, self.n)
        x = np.zeros((len(y), self.free.dim), dtype=np.int64)
        x[:, self.free_coords] = y
        return self.labels[x @ self._w]

    def public_checks(self, box, rng, pairs=20000, exhaustive_limit=10**7, chunk=1 << 20):
        p, free = self.p, self.free
        # K is an ideal
        ideal = all(not any(self.project(np.einsum("i,j,ijk->k", np.array(k_), e, free.tensor) % p))
                    for k_ in self.kernel for e in np.eye(free.dim, dtype=np.int64))
        alg = base.LieAlgebra("chart", p, self.tensor)
        try:
            alg.validate()
            jacobi = True
        except ValueError:
            jacobi = False
        c = len(alg.lower_central_series()) if jacobi else None
        G = base.NilGroup(p, self.tensor, c) if jacobi and c < p else None
        hom = None
        mode = None
        if G is not None:
            if G.order**2 <= exhaustive_limit:
                # every ordered pair (i, j), i-major, in chunks of rows i
                idx = np.arange(G.order)
                step = max(1, chunk//G.order)
                batches = ((G.decode(np.repeat(idx[s:s+step], G.order)),
                            G.decode(np.tile(idx, len(idx[s:s+step])))) for s in range(0, G.order, step))
                mode = "exhaustive_%d_pairs" % G.order**2
            else:
                a = rng.integers(p, size=(pairs, self.n))
                b = rng.integers(p, size=(pairs, self.n))
                batches = [(a, b)]
                mode = "sampled_%d_pairs" % pairs
            hom = True
            for a, b in batches:
                lhs = self.exp(G.mul(a, b))
                rhs = box.mul_batch(self.exp(a), self.exp(b))
                if not (lhs == rhs).all():
                    hom = False       # stop at the first failing chunk
                    break
        return {"kernel_is_ideal": bool(ideal), "chart_jacobi": jacobi, "chart_class": c,
                "chart_exp_homomorphism": hom, "homomorphism_check": mode}


class ChartOracle:
    """f o exp_chart as a table over chart coordinates (big-endian, NilGroup encoding)."""

    def __init__(self, chart, box, H_handles):
        self.n, self.p = chart.n, chart.p
        pts = np.array(list(product(range(chart.p), repeat=chart.n)), dtype=np.int64)
        hs = list(H_handles)
        handles = chart.exp(pts)
        # f(g) = min handle of the left coset gH (black-box multiplications; charged to T_f)
        self.table = np.array([min(box.truth_mul(int(g), h) for h in hs) for g in handles], dtype=np.int64)
        self._w = chart.p**np.arange(chart.n-1, -1, -1, dtype=np.int64)

    def oracle(self, x_coords):
        x = np.asarray(x_coords, dtype=np.int64)
        return self.table[(x % self.p) @ self._w]


# ---------------------------------------------------------------- instances

def ut(n, entries, p):
    m = [[int(i == j) for j in range(n)] for i in range(n)]
    for (i, j), v in entries.items():
        m[i][j] = v % p
    return tuple(x for row in m for x in row)


def catalogue():
    """name -> (p, black-box spec, generator keys, class bound c)."""
    out = {}
    p = 5
    # Heisenberg UT_3(F_5) with a redundant third generator: kernel of dimension 3.
    x, y = ut(3, {(0, 1): 1}, p), ut(3, {(1, 2): 1}, p)
    out["heis5_s3"] = (p, ("matrix", 3), [x, y, _matmul(x, y, 3, p)], 2)
    # Bacon-Childs-van Dam type F_p x| F_p^3 as 4x4 unitriangular matrices: filiform, class 3.
    for q in (5, 7):
        out[f"affine{q}"] = (q, ("matrix", 4), [ut(4, {(0, 1): 1, (1, 2): 1}, q), ut(4, {(2, 3): 1}, q)], 3)
    # The free 2-generator class-3 group of exponent 5 (order 5^5), as a BCH group on
    # hidden coordinates x, y, z=[x,y], u=[x,z], v=[y,z]; generators are two random
    # elements with independent images mod [G,G]. Not a subgroup of UT_4.
    alg = base.lie_from_brackets("free(2,3)", p, 5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}})
    G = base.NilGroup(p, alg.tensor, 3)
    r = random.Random(20261108)
    while True:
        a, b = [tuple(r.randrange(p) for _ in range(5)) for _ in range(2)]
        if (a[0]*b[1]-a[1]*b[0]) % p:
            break
    out["free23_5"] = (p, ("bch", G), [a, b], 3)
    # A class-3 subgroup of UT_5(F_5) given as matrices: g0 = I+E01+E23, g1 = I+E12+E24.
    # Order 5^5, class exactly 3, exponent 5 (checked in GAP: SmallGroup(3125, 3); see
    # the e2e folder). log g0, log g1 generate a copy of F_(2,3) inside n_5 (no grade-4
    # brackets), so this group is abstractly the free 2-generator class-3 exponent-5
    # group again (a 2-generator Lazard algebra of class 3 and dimension 5 is F_(2,3));
    # the black box, the generators and every matrix differ from free23_5 and from UT_4.
    out["ut5_5"] = (p, ("matrix", 5), [ut(5, {(0, 1): 1, (2, 3): 1}, p), ut(5, {(1, 2): 1, (2, 4): 1}, p)], 3)
    return out


def subgroup_words(name):
    """Hidden subgroups as lists of generator words (tuples of generator indices)."""
    common = [("trivial", []), ("<g0>", [(0,)]), ("<g1>", [(1,)]), ("<g0 g1>", [(0, 1)]),
              ("<[g0,g1]>", ["comm01"]), ("<g1, [g0,g1]>", [(1,), "comm01"])]
    if name == "heis5_s3":
        return common+[("<g2> (redundant gen)", [(2,)]), ("G", [(0,), (1,)])]
    if name == "affine5":
        return common+[("<g0 g0 g1>", [(0, 0, 1)]), ("<g1, g0 g1 g0>", [(1,), (0, 1, 0)])]
    if name in ("free23_5", "ut5_5"):
        return common+[("<g0, [g0,g1]>", [(0,), "comm01"]), ("<g0 g1 g1>", [(0, 1, 1)])]
    return common


def word_handle(box, w):
    if w == "comm01":
        a, b = box.generators[0], box.generators[1]
        ai = _inverse_handle(box, a)
        bi = _inverse_handle(box, b)
        return box.truth_mul(box.truth_mul(box.truth_mul(a, b), ai), bi)
    h = box.identity
    for i in w:
        h = box.truth_mul(h, box.generators[i])
    return h


def _inverse_handle(box, g):
    # grading-side helper: g^(exponent-1) by repeated multiplication (exponent p here)
    h = box.identity
    for _ in range(box.p-1):
        h = box.truth_mul(h, g)
    return h


# ---------------------------------------------------------------- driver

def run_group(name, *, eps=0.1, seed=20261108, count="rule_w", h_filter=None, log=None,
              negative_controls=True):
    p, spec, mats, c = catalogue()[name]
    box = BlackBox(p, spec, mats, seed)
    rng = np.random.default_rng(seed)
    t0 = time.time()
    free = FreeNilpotent(len(mats), c, p)
    if free.dim != free_rank(len(mats), c):
        raise ArithmeticError("free nilpotent rank mismatch")
    engine = UniversalLazardWords(p, c, box.identity, box.mul)
    calls0 = box.calls
    labels, images = pullback_table(box, free, engine)
    pullback_calls = box.calls-calls0
    kernel, law, krec = kernel_step(box, free, engine, labels, images, eps=eps, rng=rng)
    chart = Chart(free, kernel, labels)
    checks = chart.public_checks(box, rng)
    # grading of the chart step (truth from the box)
    Gtrue = box.closure(box.generators)
    true_K = [x for x, h in zip(product(range(p), repeat=free.dim), labels) if h == box.identity]
    chart_bijective = len(set(chart.exp(np.array(list(product(range(p), repeat=chart.n)))).tolist())) == len(Gtrue) == p**chart.n
    header = {"group": name, "p": p, "black_box_kind": spec[0], "s": len(mats), "class_bound": c,
              "free_rank": free.dim, "order_G": len(Gtrue), "chart_dim": chart.n,
              "kernel": krec, "kernel_equals_true_fibre": len(true_K) == p**len(kernel)
              and all(base.coordinates(kernel, x, p) is not None for x in true_K) if kernel else len(true_K) == 1,
              "law_mass_outside_true_K_perp": _mass_outside(law, base.rref(true_K, p) if len(true_K) > 1 else [], p, free.dim),
              "pullback_multiplications": pullback_calls, "pullback_points": int(p**free.dim),
              "hiding_function_built_only_after_chart": True, "chart_public_checks": checks,
              "chart_exp_bijective_onto_G": chart_bijective,
              "chart_seconds": round(time.time()-t0, 2)}
    if log:
        print(json.dumps(header), file=log, flush=True)
    alg = base.LieAlgebra(f"chart({name})", p, chart.tensor)
    cover = base.make_cover(alg)
    schedules = ext.tree_schedules(cover, count)
    rows = []
    for hname, words in subgroup_words(name):
        if h_filter and hname not in h_filter:
            continue
        gens = [word_handle(box, w) for w in words]
        H = box.closure(gens) if gens else {box.identity}
        oracle = ChartOracle(chart, box, H)
        # truth in chart coordinates, for grading only
        inv = {int(h): i for i, h in enumerate(chart.exp(np.array(list(product(range(p), repeat=chart.n)))))}
        pts = list(product(range(p), repeat=chart.n))
        gens_chart = tuple(pts[inv[g]] for g in gens)
        truth = base.HiddenInstance(f"{name} H={hname}", alg, gens_chart)
        same_partition = _same_partition(truth.oracle_table, oracle.table)
        t1 = time.time()
        backend = ext.SparseExactBackend(cover)
        source, info = ext.prepare_source(cover, oracle, backend, "level_set", seed)
        recovered, rec = ext.run_rees_ext(cover, source, backend, schedules, seed=seed)
        row = ext.grade_ext(cover, truth, recovered, rec, backend)
        out_gens = [int(chart.exp(np.array(v))[0]) for v in recovered]
        H_out = box.closure(out_gens) if out_gens else {box.identity}
        row.update(group=name, hidden=hname, order_H=len(H), source=info,
                   oracle_partition_matches_truth=same_partition,
                   blackbox_subgroup_recovered=(H_out == H), seconds=round(time.time()-t1, 2))
        row.pop("recovered_basis", None)
        row.pop("truth_basis", None)
        rows.append(row)
        if log:
            print(json.dumps({k: row[k] for k in ("instance", "order_H", "normal", "recovered_equals_log_H",
                                                   "blackbox_subgroup_recovered", "oracle_queries",
                                                   "every_stage_output_equals_rho_H_d", "seconds")}),
                  file=log, flush=True)
    neg = negative(name, eps=eps, seed=seed) if negative_controls else None
    return {"header": header, "runs": rows, "negative_controls": neg}


def _mass_outside(law, K, p, d):
    if not K:
        return 0.0
    chars = np.array(list(product(range(p), repeat=d)), dtype=np.int64)
    outside = ((chars @ np.array(K, dtype=np.int64).T) % p).any(axis=1)
    return float(law[outside].sum())


def _same_partition(a, b):
    pairs = set(zip(a.tolist(), b.tolist()))
    return len(pairs) == len(set(a.tolist())) == len(set(b.tolist()))


def negative(name, *, eps, seed):
    p, spec, mats, c = catalogue()[name]
    out = {}
    # (a) naive pullback by products of powers
    box = BlackBox(p, spec, mats, seed)
    rng = np.random.default_rng(seed)
    free = FreeNilpotent(len(mats), c, p)
    engine = UniversalLazardWords(p, c, box.identity, box.mul)
    labels, images = pullback_table(box, free, engine, naive=True)
    fibres = np.unique(labels, return_counts=True)[1]
    kernel, law, krec = kernel_step(box, free, engine, labels, images, eps=eps, rng=rng, naive=True)
    chart = Chart(free, kernel, labels)
    out["naive_pullback"] = {"fibre_sizes": sorted(set(int(x) for x in fibres)), "kernel": krec,
                             "checks": chart.public_checks(box, rng)}
    # (b) one kernel sample
    box = BlackBox(p, spec, mats, seed)
    rng = np.random.default_rng(seed)
    engine = UniversalLazardWords(p, c, box.identity, box.mul)
    labels, images = pullback_table(box, free, engine)
    kernel, law, krec = kernel_step(box, free, engine, labels, images, eps=eps, rng=rng, samples=1)
    out["one_sample"] = {"kernel": krec,
                         "caught_by_las_vegas_check": krec["las_vegas_rejected_vectors"] > 0}
    # (c) a forced K' strictly inside K (what an approximate Fourier transform could return)
    out["strict_subkernel"] = strict_subkernel_control(name, seed=seed)
    return out


def strict_subkernel_control(name, *, seed=20261108):
    """Force K' = K cap gamma_2(F), when it is a proper nonzero subspace of the true K
    (an ideal, being an intersection of ideals), and run every public check on it.

    Phi factors through F/K' as a Lie homomorphism, so the chart exp map is a group
    homomorphism and every public check passes; only injectivity fails (grading:
    the chart has dimension dim F - dim K' > dim log G). This documents the limitation
    of the public checks; it uses the true kernel and is not part of the algorithm."""
    p, spec, mats, c = catalogue()[name]
    box = BlackBox(p, spec, mats, seed)
    rng = np.random.default_rng(seed)
    free = FreeNilpotent(len(mats), c, p)
    engine = UniversalLazardWords(p, c, box.identity, box.mul)
    labels, images = pullback_table(box, free, engine)
    true_K = [x for x, h in zip(product(range(p), repeat=free.dim), labels) if h == box.identity]
    K = base.rref(true_K, p) if len(true_K) > 1 else []
    s = len(mats)
    # RREF rows with pivot in a grade >= 2 coordinate span exactly K cap gamma_2(F)
    sub = [row for row in K if next(j for j, x in enumerate(row) if x) >= s]
    if not 0 < len(sub) < len(K):
        return {"applicable": False, "true_kernel_dim": len(K), "subkernel_dim": len(sub)}
    chart = Chart(free, sub, labels)
    checks = chart.public_checks(box, rng)
    rejected = len(las_vegas_rejects(box, labels, sub, p, free.dim))
    image = len(set(chart.exp(np.array(list(product(range(p), repeat=chart.n)))).tolist()))
    order_G = len(box.closure(box.generators))
    passed = rejected == 0 and all(v is True for v in checks.values() if isinstance(v, bool))
    return {"applicable": True, "true_kernel_dim": len(K), "subkernel_dim": len(sub),
            "las_vegas_rejected_vectors": rejected, "checks": checks, "chart_dim": chart.n,
            "order_G": order_G, "chart_points": int(p**chart.n), "chart_exp_image_size": image,
            "chart_exp_bijective_onto_G": image == order_G == p**chart.n,
            "caught_by_public_checks": not passed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("groups", nargs="+", choices=sorted(catalogue()))
    parser.add_argument("--count", default="rule_w", choices=("rule_w", "deterministic"))
    parser.add_argument("--h", action="append")
    parser.add_argument("--no-negative", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    import sys
    results = [run_group(g, count=args.count, h_filter=args.h, log=sys.stderr,
                         negative_controls=not args.no_negative) for g in args.groups]
    text = json.dumps(results, indent=1, default=str)
    if args.out:
        Path(args.out).write_text(text+"\n")
    else:
        print(text)


if __name__ == "__main__":
    main()

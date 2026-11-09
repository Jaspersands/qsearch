"""Exact end-to-end simulation of the whole Rees HSP algorithm on small groups.

Input: explicit structure constants of a nilpotent Lie algebra L over F_p
(class c < p) and a hiding function f on G = (L, *) given only as a table
that the algorithm queries. The driver never sees H or log H. It

1. builds the positive Rees cover A = sum_k t^k gamma_k(L) and G~ = (A, *);
2. prepares lifted sources by querying f at the c evaluation points
   E_1, ..., E_c in superposition and tracing out the labels;
3. at each grade d = c, ..., 2 measures the central character of
   Z_d = t^d gamma_d on every source, solves the diagonal equation
   sum_i s_i^d lambda_i = 0 by BRUTE FORCE over F_p^M (fine at these sizes,
   not the paper's Ivanyos-Santha solver), and applies the controlled
   right-action channel to obtain one source on G_(d-1) per block;
4. on grade one, samples the abelian Fourier transform and returns the
   F_p-nullspace of the samples as log H.

Two backends simulate the quantum part.

* ExactBackend: a state that commutes with left translations is stored as
  its regular-representation coefficients, rho = |G|^-1 sum_g c(g) R_g,
  with c(g) in Z[zeta_p] (integer vectors) times one exact rational scale.
  All arithmetic is exact. The representation is faithful only for
  left-invariant states, so this is CHECKED, never assumed: the oracle
  source by an exhaustive coset-partition check, the instrument because
  its Kraus operators are combinations of central R_z, and every channel
  output by checking that the trace function is constant on every central
  fibre (which makes the output entry depend only on q^-1 r for EVERY
  address pair q, r).
* DenseBackend: explicit density matrices in complex floating point. The
  instrument is run as its circuit (Fourier ancilla, controlled central
  translation, inverse Fourier, measure), the channel as explicit
  controlled permutation matrices followed by a partial trace, and the
  readout as an explicit QFT matrix. No left-invariance is used. Feasible
  for the Heisenberg covers only.

What this does NOT show: it is an exponential-size classical simulation of
a polynomial-size quantum algorithm on fixed tiny groups. It implements no
coherent receiver or gate-level circuit, does not test the Ivanyos-Santha
arity B_d(g_d) or its solver (the arity here is the Chevalley-Warning
existence arity kappa_d g_d + 1), tests no asymptotic cost, and a finite
run can only falsify the paper's claims, never prove them for all (G, H).
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import product
import json
from math import gcd
import random
import time

import numpy as np


# ---------------------------------------------------------------- F_p linear algebra

def rref(rows, p):
    """Row-reduced basis (list of tuples) of the span of rows over F_p."""
    m = np.array(rows, dtype=np.int64).reshape(len(rows), -1) % p if len(rows) else None
    if m is None or m.size == 0:
        return []
    m = m.copy()
    r = 0
    for col in range(m.shape[1]):
        pivot = next((i for i in range(r, m.shape[0]) if m[i, col]), None)
        if pivot is None:
            continue
        m[[r, pivot]] = m[[pivot, r]]
        m[r] = m[r]*pow(int(m[r, col]), -1, p) % p
        for i in range(m.shape[0]):
            if i != r and m[i, col]:
                m[i] = (m[i]-m[i, col]*m[r]) % p
        r += 1
        if r == m.shape[0]:
            break
    return [tuple(int(x) for x in row) for row in m[:r]]


def nullspace(rows, width, p):
    """Basis of {x in F_p^width : row . x = 0 for every row}."""
    basis = rref(rows, p)
    pivots = [next(j for j, x in enumerate(row) if x) for row in basis]
    out = []
    for free in (j for j in range(width) if j not in pivots):
        x = [0]*width
        x[free] = 1
        for row, pc in zip(basis, pivots):
            x[pc] = -row[free] % p
        out.append(tuple(x))
    return out


def coordinates(basis, vector, p):
    """Coordinates of vector in the given (independent) basis, or None."""
    if not basis:
        return () if not any(vector) else None
    k, n = len(basis), len(vector)
    sol = nullspace([[basis[i][j] for i in range(k)]+[-vector[j] % p] for j in range(n)], k+1, p)
    for x in sol:
        if x[-1]:
            inv = pow(x[-1], -1, p)
            return tuple(a*inv % p for a in x[:-1])
    return None


def intersect(a, b, p, width):
    """Basis of span(a) cap span(b)."""
    if not a or not b:
        return []
    k = len(a)
    rows = [[a[i][j] for i in range(k)]+[-b[i][j] % p for i in range(len(b))] for j in range(width)]
    sols = nullspace(rows, k+len(b), p)
    return rref([[sum(x[i]*a[i][j] for i in range(k)) % p for j in range(width)] for x in sols], p)


def span_elements(basis, width, p):
    """All elements of span(basis) as an (p^k, width) array."""
    if not basis:
        return np.zeros((1, width), dtype=np.int64)
    coeff = np.array(list(product(range(p), repeat=len(basis))), dtype=np.int64)
    return coeff @ np.array(basis, dtype=np.int64) % p


# ---------------------------------------------------------------- Lie algebras

@dataclass(frozen=True)
class LieAlgebra:
    """Structure constants T[i, j] = [e_i, e_j] over F_p (dense int array)."""
    name: str
    p: int
    tensor: np.ndarray

    @property
    def dim(self):
        return self.tensor.shape[0]

    def bracket(self, x, y):
        x, y = np.asarray(x, dtype=np.int64), np.asarray(y, dtype=np.int64)
        return tuple(int(v) for v in np.einsum("i,j,ijk->k", x, y, self.tensor) % self.p)

    def validate(self):
        p, n, T = self.p, self.dim, self.tensor % self.p
        if any(T[i, i].any() for i in range(n)) or ((T+T.transpose(1, 0, 2)) % p).any():
            raise ValueError("structure constants are not alternating")
        e = np.eye(n, dtype=np.int64)
        for i, j, k in product(range(n), repeat=3):
            terms = [self.bracket(e[a], self.bracket(e[b], e[c]))
                     for a, b, c in ((i, j, k), (j, k, i), (k, i, j))]
            if any(sum(t[q] for t in terms) % p for q in range(n)):
                raise ValueError("Jacobi identity fails")

    def lower_central_series(self):
        """[gamma_1, gamma_2, ...] (nonzero terms only), RREF bases in L coordinates."""
        e = [tuple(int(i == j) for j in range(self.dim)) for i in range(self.dim)]
        series, current = [], rref(e, self.p)
        while current:
            series.append(current)
            current = rref([self.bracket(a, b) for a in e for b in current], self.p)
            if len(current) == len(series[-1]):
                raise ValueError("algebra is not nilpotent")
        return series

    def lie_closure(self, generators):
        basis = rref(list(generators), self.p)
        while True:
            new = rref(basis+[self.bracket(a, b) for a in basis for b in basis], self.p)
            if len(new) == len(basis):
                return new
            basis = new

    def center(self):
        # x -> ([x, e_i])_i is linear; rows are its coordinate functionals
        rows = [[int(self.tensor[a, i, k]) for a in range(self.dim)]
                for i in range(self.dim) for k in range(self.dim)]
        return nullspace(rows, self.dim, self.p)

    def is_ideal(self, basis):
        e = [tuple(int(i == j) for j in range(self.dim)) for i in range(self.dim)]
        return all(coordinates(basis, self.bracket(x, y), self.p) is not None
                   for x in e for y in basis) if basis else True


def lie_from_brackets(name, p, dim, brackets):
    """brackets: {(i, j): {k: coefficient}} for i < j (0-based)."""
    T = np.zeros((dim, dim, dim), dtype=np.int64)
    for (i, j), out in brackets.items():
        for k, v in out.items():
            T[i, j, k] = v % p
            T[j, i, k] = -v % p
    alg = LieAlgebra(name, p, T)
    alg.validate()
    return alg


def heisenberg(p):
    """[x, y] = z on basis (x, y, z)."""
    return lie_from_brackets(f"Heis(F_{p})", p, 3, {(0, 1): {2: 1}})


def filiform4(p):
    """Standard filiform n4: [e1, e2] = e3, [e1, e3] = e4; class three."""
    return lie_from_brackets(f"n4(F_{p})", p, 4, {(0, 1): {2: 1}, (0, 2): {3: 1}})


def filiform5(p):
    """[e1, e_i] = e_(i+1), i = 2, 3, 4; class four (used only for BCH checks)."""
    return lie_from_brackets(f"n5(F_{p})", p, 5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}})


# ---------------------------------------------------------------- groups via truncated BCH

def _inverse(x, p):
    return pow(x, -1, p)


@dataclass
class NilGroup:
    """(F_p^n, BCH product) for a nilpotent Lie tensor of class <= 4 < p.

    Coordinates are encoded big-endian: index = sum_j x_j p^(n-1-j), so the
    LAST coordinates are the least significant digits.
    """
    p: int
    tensor: np.ndarray
    nil_class: int

    def __post_init__(self):
        if not 1 <= self.nil_class < self.p or self.nil_class > 4:
            raise ValueError("this BCH implementation needs class <= 4 and class < p")
        T = self.tensor % self.p
        self._terms = [(int(i), int(j), int(k), int(T[i, j, k])) for i, j, k in zip(*np.nonzero(T))]
        self.n = self.tensor.shape[0]
        self.order = self.p**self.n
        self._weights = self.p**np.arange(self.n-1, -1, -1, dtype=np.int64)

    def bracket(self, X, Y):
        out = np.zeros(np.broadcast_shapes(X.shape, Y.shape), dtype=np.int64)
        for i, j, k, v in self._terms:
            out[..., k] += v*X[..., i]*Y[..., j]
        return out % self.p

    def mul(self, X, Y):
        p = self.p
        X, Y = np.asarray(X, dtype=np.int64), np.asarray(Y, dtype=np.int64)
        out = X+Y
        if self.nil_class >= 2:
            xy = self.bracket(X, Y)
            out = out+_inverse(2, p)*xy
            if self.nil_class >= 3:
                xxy, yxy = self.bracket(X, xy), self.bracket(Y, xy)
                out = out+_inverse(12, p)*(xxy-yxy)
                if self.nil_class >= 4:
                    out = out-_inverse(24, p)*self.bracket(Y, xxy)
        return out % p

    def inv(self, X):
        return (-np.asarray(X, dtype=np.int64)) % self.p

    def encode(self, X):
        return (np.asarray(X, dtype=np.int64) % self.p) @ self._weights

    def decode(self, idx):
        idx = np.asarray(idx, dtype=np.int64)
        return (idx[..., None]//self._weights) % self.p

    def elements(self):
        return self.decode(np.arange(self.order, dtype=np.int64))

    def closure(self, generators):
        """Indices of the subgroup generated by the given coordinate rows."""
        gens = np.asarray(generators, dtype=np.int64).reshape(-1, self.n)
        seen = np.zeros(self.order, dtype=bool)
        seen[0] = True
        frontier = np.zeros((1, self.n), dtype=np.int64)
        while len(frontier):
            new = []
            for g in gens:
                idx = self.encode(self.mul(frontier, g[None, :]))
                idx = np.unique(idx[~seen[idx]])
                seen[idx] = True
                new.append(idx)
            frontier = self.decode(np.unique(np.concatenate(new))) if new else frontier[:0]
        return np.nonzero(seen)[0]


# ---------------------------------------------------------------- Rees cover

@dataclass
class ReesCover:
    """A = sum_(k=1..c) t^k gamma_k(L) with grade-ordered coordinates."""
    algebra: LieAlgebra
    series: list            # RREF bases of gamma_k(L), k = 1..c
    grades: np.ndarray      # grade of each cover coordinate
    tensor: np.ndarray      # cover structure constants
    points: tuple           # evaluation points s_1..s_c

    @property
    def p(self):
        return self.algebra.p

    @property
    def c(self):
        return len(self.series)

    @property
    def dims(self):
        return tuple(len(b) for b in self.series)

    def width(self, d):
        """Number of coordinates of G_d = A / I_d."""
        return sum(self.dims[:d])

    def stage_group(self, d):
        n = self.width(d)
        return NilGroup(self.p, self.tensor[:n, :n, :n], d)

    def evaluation_matrix(self, s):
        """n_A x m matrix: row of t^k b is s^k b."""
        rows = [tuple(pow(s, k, self.p)*x % self.p for x in b)
                for k, basis in enumerate(self.series, 1) for b in basis]
        return np.array(rows, dtype=np.int64)

    def dilation_scales(self, d, s):
        return np.array([pow(s, int(k), self.p) for k in self.grades[:self.width(d)]], dtype=np.int64)


def make_cover(algebra):
    p = algebra.p
    series = algebra.lower_central_series()
    c = len(series)
    if c >= p:
        raise ValueError("Lazard input requires class < p")
    index = [(k, j) for k, basis in enumerate(series, 1) for j in range(len(basis))]
    pos = {key: i for i, key in enumerate(index)}
    n = len(index)
    T = np.zeros((n, n, n), dtype=np.int64)
    for a, (i, x) in enumerate(index):
        for b, (j, y) in enumerate(index):
            value = algebra.bracket(series[i-1][x], series[j-1][y])
            if i+j > c:
                if any(value):
                    raise ArithmeticError("discarded bracket is nonzero")
                continue
            coords = coordinates(series[i+j-1], value, p)
            if coords is None:
                raise ArithmeticError("[gamma_i, gamma_j] not in gamma_(i+j)")
            for k, v in enumerate(coords):
                T[a, b, pos[i+j, k]] = v
    cover = ReesCover(algebra, series, np.array([k for k, _ in index]), T, tuple(range(1, c+1)))
    LieAlgebra("cover", p, T).validate()
    for s in cover.points:   # E_s is a Lie homomorphism on basis pairs
        E = cover.evaluation_matrix(s)
        for a in range(n):
            for b in range(n):
                lhs = (T[a, b] @ E) % p
                rhs = np.array(algebra.bracket(E[a], E[b]))
                if (lhs != rhs).any():
                    raise ArithmeticError("evaluation is not a Lie homomorphism")
    return cover


# ---------------------------------------------------------------- hidden subgroups (test truth)

@dataclass
class HiddenInstance:
    """The hiding function and, separately, the truth used only to grade runs."""
    name: str
    algebra: LieAlgebra
    generators: tuple
    group: NilGroup = field(init=False)
    subgroup: np.ndarray = field(init=False)
    log_h: list = field(init=False)
    oracle_table: np.ndarray = field(init=False)

    def __post_init__(self):
        alg = self.algebra
        self.group = NilGroup(alg.p, alg.tensor, len(alg.lower_central_series()))
        self.subgroup = self.group.closure(self.generators) if self.generators else np.array([0])
        self.log_h = alg.lie_closure(self.generators) if self.generators else []
        lazard = set(self.group.encode(span_elements(self.log_h, alg.dim, alg.p)).tolist())
        if lazard != set(self.subgroup.tolist()):
            raise ArithmeticError("log of the generated subgroup is not its Lie closure")
        G, Hc = self.group, self.group.decode(self.subgroup)
        everything = G.elements()
        table = np.full(G.order, G.order, dtype=np.int64)
        for h in Hc:      # f(x) = min index of the left coset xH
            table = np.minimum(table, G.encode(G.mul(everything, h[None, :])))
        self.oracle_table = table

    def oracle(self, x_coords):
        """Vectorized hiding function on original L coordinates."""
        return self.oracle_table[self.group.encode(x_coords)]

    def flags(self):
        alg, h = self.algebra, self.log_h
        center = alg.center()
        return {"dim_h": len(h), "normal": alg.is_ideal(h),
                "meets_center_trivially": not intersect(h, center, alg.p, alg.dim),
                "contains_center": all(coordinates(h, z, alg.p) is not None for z in center) if h else not center,
                "order_H": int(len(self.subgroup))}


def graded_hidden(cover, log_h):
    """Per grade k: basis of h cap gamma_k in gamma_k coordinates."""
    p, m = cover.p, cover.algebra.dim
    out = []
    for basis in cover.series:
        inter = intersect(log_h, basis, p, m)
        out.append(rref([coordinates(basis, v, p) for v in inter], p))
    return out


def expected_stage_indices(cover, log_h, d):
    """Indices in G_d of H_d = exp(sum_(k<=d) t^k (h cap gamma_k))."""
    grade_bases = graded_hidden(cover, log_h)[:d]
    rows, offset, n = [], 0, cover.width(d)
    for k, basis in enumerate(grade_bases):
        for v in basis:
            row = [0]*n
            row[offset:offset+len(v)] = v
            rows.append(row)
        offset += cover.dims[k]
    return np.sort(cover.stage_group(d).encode(span_elements(rows, n, cover.p)))


def expected_label_support(cover, log_h, d):
    """K_d^perp: annihilator of h cap gamma_d inside F_p^(g_d)."""
    K = graded_hidden(cover, log_h)[d-1]
    return nullspace(K, cover.dims[d-1], cover.p)


# ---------------------------------------------------------------- exact cyclotomic arithmetic

def cyc_canon(v):
    """Canonical form in Z[zeta_p]: subtract the zeta^(p-1) coordinate."""
    return v-v[..., -1:]


def cyc_mul(a, b, p):
    if a.size and b.size:
        bound = int(np.abs(a).max())*int(np.abs(b).max())*p
        if bound >= 2**62:
            raise OverflowError("cyclotomic product could overflow int64")
    out = np.zeros(np.broadcast_shapes(a.shape, b.shape), dtype=np.int64)
    for j in range(p):
        out += a[..., j:j+1]*b[..., (np.arange(p)-j) % p]     # zeta^j * b
    return cyc_canon(out)


def cyc_rational(v):
    """Return the integer if v (canonical) is rational, else None."""
    return int(v[0]) if not v[1:].any() else None


@dataclass
class ExactState:
    """rho = scale/|G_d| * sum_g v[g] R_g, v[g] in Z[zeta_p] canonical."""
    d: int
    scale: Fraction
    v: np.ndarray

    def normalized(self):
        g = int(np.gcd.reduce(np.abs(self.v).ravel())) if self.v.any() else 1
        if g > 1:
            return ExactState(self.d, self.scale*g, self.v//g)
        return self


class ExactBackend:
    """Exact simulation in the regular group algebra (left-invariant states)."""

    exact = True

    def __init__(self, cover):
        self.cover, self.p = cover, cover.p
        self.groups = {d: cover.stage_group(d) for d in range(1, cover.c+1)}
        self._center, self._negdil, self._labels = {}, {}, {}
        for d in range(2, cover.c+1):
            G, g = self.groups[d], cover.dims[d-1]
            zs = np.array(list(product(range(self.p), repeat=g)), dtype=np.int64)
            # central elements have zero in all lower coordinates: top digits only
            top = zs @ (self.p**np.arange(g-1, -1, -1, dtype=np.int64))
            self._center[d] = (zs, top)
            self._labels[d] = zs
            # translation by a central z is addition: verify the top grade is central in G_d
            n = G.n
            if G.tensor[n-g:, :, :].any() or G.tensor[:, n-g:, :].any():
                raise ArithmeticError("top grade of G_d is not central")
        for d in range(1, cover.c+1):
            G = self.groups[d]
            elems = G.elements()
            self._negdil[d] = {s: G.encode(-elems*cover.dilation_scales(d, s)[None, :])
                               for s in range(1, self.p)}

    # -- source preparation: c oracle queries per source
    def prepare_source(self, oracle):
        cover, p = self.cover, self.p
        G = self.groups[cover.c]
        elems = G.elements()
        labels = np.stack([oracle(elems @ cover.evaluation_matrix(s) % p) for s in cover.points], axis=1)
        _, fibre = np.unique(labels, axis=0, return_inverse=True)
        fibre = fibre.ravel()
        identity_fibre = np.nonzero(fibre == fibre[0])[0]
        sizes = np.bincount(fibre)
        if (sizes != len(identity_fibre)).any():
            raise ArithmeticError("tuple-oracle fibres have unequal sizes")
        # generators of the identity fibre S, then: S is a subgroup and every fibre is a left coset
        S = set(identity_fibre.tolist())
        gens, generated = [], {0}
        for x in identity_fibre:
            if int(x) not in generated:
                gens.append(int(x))
                generated = set(G.closure(G.decode(np.array(gens))).tolist())
        if generated != S:
            raise ArithmeticError("identity fibre of the tuple oracle is not a subgroup")
        for g in gens:
            moved = G.encode(G.mul(elems, G.decode(g)[None, :]))
            if (fibre[moved] != fibre).any():
                raise ArithmeticError("tuple oracle is not constant on left cosets")
        v = np.zeros((G.order, p), dtype=np.int64)
        v[identity_fibre, 0] = 1
        return ExactState(cover.c, Fraction(1), v), {"fibres": int(len(sizes)),
                                                     "lifted_order": int(len(identity_fibre))}

    # -- complete central instrument
    def _pi(self, d, lam):
        """Pi_lambda = |Z|^-1 sum_z zeta^(-lambda.z) R_z as (exponent per z)."""
        zs, _ = self._center[d]
        return (-(zs @ np.asarray(lam, dtype=np.int64))) % self.p

    def label_probabilities(self, state):
        """Exact Tr(Pi rho Pi) for every label, from the identity coefficient."""
        d, p = state.d, self.p
        zs, _ = self._center[d]
        Z = len(zs)
        w = p**np.arange(zs.shape[1]-1, -1, -1)
        # coefficient of (Pi rho Pi) at 1 = |Z|^-2 sum_(z,z') zeta^(-lam.(z+z')) c(-(z+z'));
        # a central element has zero lower coordinates, so its index is its top digits
        vals = state.v[((-(zs[:, None, :]+zs[None, :, :])) % p) @ w]     # (Z, Z, p)
        probs = {}
        for lam in self._labels[d]:
            phase = self._pi(d, lam)
            e = (phase[:, None]+phase[None, :]) % p
            acc = np.zeros(p, dtype=np.int64)
            for r in range(p):
                mask = e == r
                if mask.any():
                    acc += np.roll(vals[mask].sum(axis=0), r)
            q = cyc_rational(cyc_canon(acc))
            if q is None:
                raise ArithmeticError("branch probability is not rational")
            pr = state.scale*q/Z**2
            if pr < 0:
                raise ArithmeticError("negative branch probability")
            probs[tuple(int(x) for x in lam)] = pr
        if sum(probs.values()) != 1:
            raise ArithmeticError("instrument probabilities do not sum to one")
        return probs

    def _decode_top(self, d, idx):
        g = self.cover.dims[d-1]
        return (np.asarray(idx)[..., None]//(self.p**np.arange(g-1, -1, -1))) % self.p

    def _central_convolution(self, d, v, lam):
        """(Pi_lambda * c) in the group algebra; translation by central z is addition.
        Returns |Z| (Pi c), i.e. sum_z zeta^(-lam.z) c(x - z); only supp(c) is touched."""
        zs, _ = self._center[d]
        phase = self._pi(d, lam)
        g = zs.shape[1]
        out = np.zeros_like(v)
        support = np.nonzero(v.any(axis=1))[0]
        low, high = support//(self.p**g), support % (self.p**g)
        hdig = self._decode_top(d, high)
        w = self.p**np.arange(g-1, -1, -1)
        rows = v[support]
        perms = [(np.arange(self.p)-k) % self.p for k in range(self.p)]
        for z, ph in zip(zs, phase):
            # the term c(y) R_y R_z lands on x = y + z
            dst = low*(self.p**g)+((hdig+z) % self.p) @ w
            np.add.at(out, dst, rows[:, perms[int(ph)]])
        return cyc_canon(out)

    def condition(self, state, lam, probability):
        """Normalized Pi rho Pi / Tr, both multiplications done explicitly."""
        Z = self.p**self.cover.dims[state.d-1]
        v = self._central_convolution(state.d, state.v, lam)          # Pi rho
        v = self._central_convolution(state.d, v, lam)                # (Pi rho) Pi; Pi is central
        out = ExactState(state.d, state.scale/(Z*Z)/probability, v).normalized()
        if out.scale*cyc_rational(out.v[0]) != 1:
            raise ArithmeticError("conditioned state is not normalized")
        return out

    # -- controlled right-action channel
    def channel(self, states, witness):
        """Q register in uniform superposition, controlled R_(delta_s(sigma(q))) on each
        active target, all targets traced out. Output entry (q, r) equals
        |Q|^-1 prod_i Tr(rho_i R_(delta_si(sigma(r)^-1 sigma(q)))). F below is that
        product as a function on G_d; it is checked constant on every central fibre."""
        d, p = states[0].d, self.p
        active = [(st, s) for st, s in zip(states, witness) if s]
        if not active:
            raise ValueError("zero witness")
        # Tr(rho_i R_x) = c_i(x^-1) with x = delta_si(g); F vanishes off the common support
        idx = [self._negdil[d][s] for _, s in active]
        alive = np.ones(len(idx[0]), dtype=bool)
        for (st, _), ix in zip(active, idx):
            alive &= st.v.any(axis=1)[ix]
        where = np.nonzero(alive)[0]
        Fs, scale = None, Fraction(1)
        for (st, _), ix in zip(active, idx):
            factor = st.v[ix[where]]
            scale *= st.scale
            Fs = factor if Fs is None else cyc_mul(Fs, factor, p)
            g = int(np.gcd.reduce(np.abs(Fs).ravel())) if Fs.any() else 1
            if g > 1:
                Fs, scale = Fs//g, scale*g
        F = np.zeros((len(alive), p), dtype=np.int64)
        F[where] = Fs
        Zsize = p**self.cover.dims[d-1]
        fib = F.reshape(-1, Zsize, p)
        if (fib != fib[:, :1, :]).any():
            raise ArithmeticError("channel output does not descend: F not constant on central fibres")
        Fq = fib[:, 0, :]                          # F on any lift of x in G_(d-1)
        Q = self.groups[d-1]
        neg = Q.encode(Q.inv(Q.elements()))
        out = ExactState(d-1, scale, Fq[neg]).normalized()    # c_out(y) = F(lift of y^-1)
        if out.scale*cyc_rational(out.v[0]) != 1:
            raise ArithmeticError("channel output lost normalization")
        return out

    # -- terminal abelian Fourier sampling
    def readout_probabilities(self, state):
        if state.d != 1:
            raise ValueError("readout only on grade one")
        p, G = self.p, self.groups[1]
        W = G.elements()
        E = (W @ W.T) % p                     # exponent k.w
        acc = np.zeros((G.order, p), dtype=np.int64)
        for r in range(p):
            acc += np.roll((E == r).astype(np.int64) @ state.v, r, axis=-1)
        acc = cyc_canon(acc)
        if acc[:, 1:].any():
            raise ArithmeticError("Fourier probability is not rational")
        probs = {tuple(int(x) for x in k): state.scale*int(a)/G.order
                 for k, a in zip(W, acc[:, 0]) if a}
        if sum(probs.values()) != 1 or min(probs.values()) < 0:
            raise ArithmeticError("Fourier distribution invalid")
        return probs

    # -- grading helpers (truth comparison, cross-checks)
    def equals_coset_state(self, state, indices):
        """Exact test: state == rho_H for the subgroup with these indices."""
        target = np.zeros(len(state.v), dtype=bool)
        target[indices] = True
        rational = ~state.v[:, 1:].any(axis=1)
        if not rational.all():
            return False
        vals = [state.scale*int(x) for x in state.v[:, 0]]
        return all(v == (1 if t else 0) for v, t in zip(vals, target))

    def to_dense(self, state):
        G = self.groups[state.d]
        elems = G.elements()
        zeta = np.exp(2j*np.pi*np.arange(self.p)/self.p)
        cvals = (state.v @ zeta)*float(state.scale)
        diff = np.stack([G.encode(G.mul(G.inv(elems[u])[None, :], elems)) for u in range(G.order)])
        return cvals[diff]/G.order


class DenseBackend:
    """Explicit density matrices; instrument as a circuit; no invariance assumed."""

    exact = False
    TOL = 1e-9

    def __init__(self, cover, max_order=625):
        self.cover, self.p = cover, cover.p
        if cover.stage_group(cover.c).order > max_order:
            raise ValueError("dense backend only for tiny covers")
        self.groups = {d: cover.stage_group(d) for d in range(1, cover.c+1)}
        self.omega = np.exp(2j*np.pi/self.p)
        self.right = {}
        for d, G in self.groups.items():
            E = G.elements()
            # right[d][u, g] = index of u * g
            self.right[d] = np.stack([G.encode(G.mul(E, E[g][None, :])) for g in range(G.order)], axis=1)

    def prepare_source(self, oracle):
        cover, p = self.cover, self.p
        G = self.groups[cover.c]
        elems = G.elements()
        labels = np.stack([oracle(elems @ cover.evaluation_matrix(s) % p) for s in cover.points], axis=1)
        _, lab = np.unique(labels, axis=0, return_inverse=True)
        lab = lab.ravel()
        # purification sum_a |a>|f^(a)> / sqrt N; trace out the label register
        onehot = np.zeros((G.order, lab.max()+1))
        onehot[np.arange(G.order), lab] = 1
        rho = onehot @ onehot.T/G.order
        return (cover.c, rho.astype(complex)), {"fibres": int(lab.max()+1)}

    def _center(self, d):
        g = self.cover.dims[d-1]
        zs = np.array(list(product(range(self.p), repeat=g)), dtype=np.int64)
        n = self.groups[d].n
        full = np.zeros((len(zs), n), dtype=np.int64)
        full[:, n-g:] = zs
        return zs, self.groups[d].encode(full)

    def _blocks(self, state):
        """Return (zs, amplitudes a[lam, z], traces T[z, z']) of the instrument circuit."""
        d, rho = state
        zs, zidx = self._center(d)
        Z = len(zs)
        # ancilla |0> -F-> sum_z |z>/sqrt Z ; controlled R_z ; F^dagger ; <lam|
        fourier = self.omega**((zs @ zs.T) % self.p)/np.sqrt(Z)        # F[lam, z]
        a = fourier.conj()*fourier[:, :1].T                              # <lam|F^+|z><z|F|0>
        R = self.right[d]
        T = np.array([[np.trace(rho[np.ix_(R[:, zi], R[:, zj])]) for zj in zidx] for zi in zidx])
        return zs, zidx, a, T

    def label_probabilities(self, state):
        zs, _, a, T = self._blocks(state)
        probs = {}
        for lam, row in zip(zs, a):
            pr = np.einsum("i,ij,j->", row, T, row.conj())
            if abs(pr.imag) > self.TOL or pr.real < -self.TOL:
                raise ArithmeticError("invalid branch probability")
            probs[tuple(int(x) for x in lam)] = max(pr.real, 0.0)
        if abs(sum(probs.values())-1) > self.TOL:
            raise ArithmeticError("instrument incomplete")
        return probs

    def condition(self, state, lam, probability):
        d, rho = state
        zs, zidx, a, _ = self._blocks(state)
        row = a[[tuple(z) for z in zs.tolist()].index(tuple(lam))]
        R = self.right[d]
        out = np.zeros_like(rho)
        for ai, zi in zip(row, zidx):
            for aj, zj in zip(row, zidx):
                # (R_z rho R_z'^dagger)[u, v] = rho[u z, v z']
                out += ai*np.conj(aj)*rho[np.ix_(R[:, zi], R[:, zj])]
        return (d, out/probability)

    def channel(self, states, witness):
        d = states[0][0]
        G, Q = self.groups[d], self.groups[d-1]
        qe = Q.elements()
        lift = np.zeros((Q.order, G.n), dtype=np.int64)
        lift[:, :Q.n] = qe                                  # section: zero top coordinates
        sigma = np.full((Q.order, Q.order), 1/Q.order, dtype=complex)   # |+><+| on Q
        R = self.right[d]
        for (dd, rho), s in zip(states, witness):
            if not s:
                continue                                    # discarded untouched
            gq = G.encode(lift*self.cover.dilation_scales(d, s)[None, :])
            # T[q, r] = Tr(U_q rho U_r^dagger), (U_q rho U_r^dagger)[u, u] = rho[u g_q, u g_r]
            T = np.empty((Q.order, Q.order), dtype=complex)
            for q in range(Q.order):
                T[q] = rho[R[:, gq[q]][:, None], R[:, gq]].sum(axis=0)
            sigma = sigma*T
        if abs(np.trace(sigma)-1) > self.TOL:
            raise ArithmeticError("channel output lost trace")
        return (d-1, sigma)

    def readout_probabilities(self, state):
        d, sigma = state
        G = self.groups[1]
        W = G.elements()
        F = self.omega**((W @ W.T) % self.p)/np.sqrt(G.order)
        diag = np.einsum("ku,uv,kv->k", F, sigma, F.conj())
        if np.abs(diag.imag).max() > self.TOL or diag.real.min() < -self.TOL:
            raise ArithmeticError("invalid Fourier distribution")
        return {tuple(int(x) for x in k): float(v.real) for k, v in zip(W, diag) if v.real > self.TOL}


# ---------------------------------------------------------------- the algorithm (oracle only)

def sde_arity(cover, d):
    """Chevalley-Warning existence arity kappa_d * g_d + 1 (not Schedule 1's B_d)."""
    return gcd(d, cover.p-1)*cover.dims[d-1]+1


def _ceil_log2(x):
    return (x-1).bit_length()


def schedule_one_B(d, a):
    """B_d(a) of main.tex eq. (is-arity), reported for comparison only."""
    return (d**(d*(d-1)//2)*(a+1)**d)**_ceil_log2(d+1)


def brute_force_sde(labels, d, p, rng):
    """All nonzero s in F_p^M with sum_i s_i^d lambda_i = 0; return a random one.
    BRUTE FORCE over p^M assignments: a test-size solver only."""
    lab = np.array(labels, dtype=np.int64)
    M = len(lab)
    S = np.array(list(product(range(p), repeat=M))[1:], dtype=np.int64)
    sums = (pow_mod(S, d, p) @ lab) % p
    ok = np.nonzero(~sums.any(axis=1))[0]
    if not len(ok):
        return None, 0
    return tuple(int(x) for x in S[ok[rng.randrange(len(ok))]]), int(len(ok))


def pow_mod(a, e, p):
    out = np.ones_like(a)
    for _ in range(e):
        out = out*a % p
    return out


def _sample(probs, rng):
    keys = list(probs)
    weights = [float(probs[k]) for k in keys]
    return rng.choices(keys, weights=weights, k=1)[0]


@dataclass
class RunRecord:
    labels: dict = field(default_factory=dict)          # d -> list of observed labels
    label_laws: dict = field(default_factory=dict)      # d -> list of per-source exact laws
    witnesses: dict = field(default_factory=dict)       # d -> list of (witness, #solutions)
    stage_states: dict = field(default_factory=dict)    # d -> list of produced states
    readout: list = field(default_factory=list)
    top_sources: int = 0
    oracle_queries: int = 0
    source_info: dict = field(default_factory=dict)


def run_rees(cover, oracle, backend, *, seed=0, extra_samples=4, keep_states=False,
             solver=None):
    """The whole Rees algorithm. Uses ONLY the cover (public) and oracle queries.

    S = m + extra_samples grade-one samples, each from its own descent tree.
    `solver` replaces the brute-force SDE solver (negative controls only).
    Returns (basis of recovered log H in L coordinates, RunRecord)."""
    solver = solver or brute_force_sde
    rng = random.Random(seed)
    rec = RunRecord()
    source, rec.source_info = backend.prepare_source(oracle)   # identical density each time
    top_cache = {}

    def fresh_top():
        rec.top_sources += 1
        rec.oracle_queries += len(cover.points)
        return source

    def make(d):
        """One source on G_d."""
        if d == cover.c:
            return fresh_top()
        M = sde_arity(cover, d+1)
        while True:
            block, labels = [], []
            for _ in range(M):
                st = make(d+1)
                if d+1 < cover.c:
                    law = backend.label_probabilities(st)
                else:                       # every top source is the same density
                    if "law" not in top_cache:
                        top_cache["law"] = backend.label_probabilities(st)
                    law = top_cache["law"]
                lam = _sample(law, rng)
                rec.labels.setdefault(d+1, []).append(lam)
                rec.label_laws.setdefault(d+1, []).append(law)
                key = ("post", lam)
                if d+1 == cover.c and key in top_cache:
                    post = top_cache[key]                    # same input, same outcome
                else:
                    post = backend.condition(st, lam, law[lam])
                    if d+1 == cover.c:
                        top_cache[key] = post
                block.append(post)
                labels.append(lam)
            witness, count = solver(labels, d+1, cover.p, rng)
            rec.witnesses.setdefault(d+1, []).append((witness, count))
            if witness is not None:
                out = backend.channel(block, witness)
                if keep_states:
                    rec.stage_states.setdefault(d, []).append(out)
                return out
            # block lost; never happens at the Chevalley-Warning arity

    samples = []
    for _ in range(cover.algebra.dim+extra_samples):
        st = make(1) if cover.c > 1 else fresh_top()
        law = backend.readout_probabilities(st)
        k = _sample(law, rng)
        rec.readout.append((k, law))
        samples.append(k)
    recovered = nullspace(samples, cover.algebra.dim, cover.p)   # grade-1 coords = L coords
    return rref(recovered, cover.p), rec


# ---------------------------------------------------------------- instances and grading

def instances():
    """(cover, list of HiddenInstance) for the tested groups."""
    out = []
    for p in (3, 5):
        alg = heisenberg(p)
        cover = make_cover(alg)
        hs = [("trivial", ()), ("<x> non-normal", ((1, 0, 0),)),
              ("<y+z> non-normal", ((0, 1, 1),)), ("<x+2y+z>", ((1, 2, 1),)),
              ("Z(G)", ((0, 0, 1),)), ("<x,z> normal", ((1, 0, 0), (0, 0, 1))),
              ("<x,y> = G", ((1, 0, 0), (0, 1, 0)))]
        out.append((cover, [HiddenInstance(f"{alg.name} H={n}", alg, g) for n, g in hs]))
    return out


def class_three_instances(p=5):
    alg = filiform4(p)
    cover = make_cover(alg)
    hs = [("<e2> non-normal", ((0, 1, 0, 0),)),
          ("<e1> non-normal", ((1, 0, 0, 0),)),
          ("<e1+e3> non-normal", ((1, 0, 1, 0),)),
          ("<e2,e4> non-normal", ((0, 1, 0, 0), (0, 0, 0, 1))),
          ("<e1+e2,e3> (closure)", ((1, 1, 0, 0), (0, 0, 1, 0))),
          ("<e3,e4> = gamma_2", ((0, 0, 1, 0), (0, 0, 0, 1))),
          ("<e2,e3> non-normal", ((0, 1, 0, 0), (0, 0, 1, 0))),
          ("Z(G)", ((0, 0, 0, 1),)),
          ("trivial", ())]
    return cover, [HiddenInstance(f"{alg.name} H={n}", alg, g) for n, g in hs]


def grade_run(cover, inst, recovered, rec, backend):
    """Compare a run with the truth. Exact comparisons for the exact backend."""
    p = cover.p
    truth = inst.log_h
    ok = rref(recovered, p) == rref(truth, p) if truth else not recovered
    stages = {}
    for d in range(cover.c, 1, -1):
        support = expected_label_support(cover, truth, d)
        allowed = {tuple(int(x) for x in row) for row in span_elements(support, cover.dims[d-1], p)}
        laws = rec.label_laws.get(d, [])
        if backend.exact:
            target = Fraction(1, len(allowed))
            laws_exact = all(all(pr == (target if lam in allowed else 0) for lam, pr in law.items())
                             for law in laws)
        else:
            laws_exact = all(all(abs(pr-((1/len(allowed)) if lam in allowed else 0)) < 1e-9
                                 for lam, pr in law.items()) for law in laws)
        observed = rec.labels.get(d, [])
        stages[d] = {"label_support_size": len(allowed), "labels_observed": len(observed),
                     "observed_labels_in_support": all(l in allowed for l in observed),
                     "every_source_law_uniform_on_K_perp": laws_exact,
                     "sources_measured": len(laws),
                     "blocks": len(rec.witnesses.get(d, [])),
                     "arity": sde_arity(cover, d),
                     "schedule_one_arity_B_d(g_d)": schedule_one_B(d, cover.dims[d-1]),
                     "min_witness_count": min((c for _, c in rec.witnesses.get(d, [])), default=None),
                     "chi_square": chi_square(observed, allowed)}
    return {"instance": inst.name, **inst.flags(), "recovered_equals_log_H": ok,
            "recovered_basis": [list(v) for v in recovered], "truth_basis": [list(v) for v in truth],
            "top_sources": rec.top_sources, "oracle_queries": rec.oracle_queries,
            "readout_samples": len(rec.readout), "lifted_order": rec.source_info.get("lifted_order"),
            "stages": stages}


def chi_square(observed, allowed):
    """Pearson chi-square of observed labels against uniform on the allowed set;
    reported only when every expected count is at least 5."""
    if not observed:
        return None
    k = len(allowed)
    expected = len(observed)/k
    if expected < 5 or k < 2:
        return {"skipped": "expected count < 5 or one category", "n": len(observed), "k": k}
    counts = {a: 0 for a in allowed}
    for l in observed:
        counts[l] = counts.get(l, 0)+1
    stat = sum((c-expected)**2/expected for c in counts.values())
    from scipy.stats import chi2
    return {"n": len(observed), "k": k, "statistic": stat, "p_value": float(chi2.sf(stat, k-1))}


def _non_witness(labels, d, p, rng):
    """Negative control: a nonzero s that is NOT a witness whenever one exists
    (returned count -1); otherwise falls back to a true witness."""
    lab = np.array(labels, dtype=np.int64)
    for s in product(range(p), repeat=len(lab)):
        if any(s) and ((pow_mod(np.array(s), d, p) @ lab) % p).any():
            return tuple(s), -1
    return brute_force_sde(labels, d, p, rng)


def stage_outputs_correct(cover, inst, rec):
    """Exact: every produced source on G_d equals rho of H_d (needs keep_states)."""
    backend = ExactBackend.__new__(ExactBackend)
    return all(backend.equals_coset_state(st, expected_stage_indices(cover, inst.log_h, d))
               for d, states in rec.stage_states.items() for st in states)


def negative_controls(seed=7):
    """Runs that the paper says must fail, to show the simulator can fail.

    (a) One evaluation point instead of c (Proposition single-evaluation): the
        lifted source is rho of E_1^-1(h), which dilations preserve only when
        [G, G] <= H. (b) A nonzero non-witness s in place of the SDE solution,
        used in every block where one exists. Each row records whether a
        descent check raised, whether every intermediate source equals the
        correct rho_(H_d), and whether the final subspace happened to be right
        (a wrong source can still give the right readout by luck)."""
    rows = []
    for cover, insts in (instances()[1], class_three_instances(5)):
        one_point = ReesCover(cover.algebra, cover.series, cover.grades, cover.tensor, (1,))
        for inst in insts:
            derived_in_h = all(coordinates(inst.log_h, v, cover.p) is not None
                               for v in cover.series[1]) if inst.log_h else False
            for kind, cov, solver in (("single_evaluation_point", one_point, None),
                                      ("non_witness_scales", cover, _non_witness)):
                row = {"instance": inst.name, "control": kind, "derived_subgroup_in_H": derived_in_h,
                       "check_raised": None, "stage_outputs_correct": None, "recovered": None}
                try:
                    h, rec = run_rees(cov, inst.oracle, ExactBackend(cov), seed=seed,
                                      solver=solver, keep_states=True)
                    row["stage_outputs_correct"] = stage_outputs_correct(cover, inst, rec)
                    row["recovered"] = rref(h, cover.p) == rref(inst.log_h, cover.p)
                    row["non_witness_blocks"] = sum(c == -1 for ws in rec.witnesses.values() for _, c in ws)
                except ArithmeticError as exc:
                    row["check_raised"] = str(exc)
                    row["non_witness_blocks"] = None
                row["failure_detected"] = bool(row["check_raised"]) or row["stage_outputs_correct"] is False
                rows.append(row)
    return rows


def report(include_f7=False, seeds=(20261102,), dense=True):
    results, t0 = [], time.time()
    groups = instances()+[class_three_instances(5)]
    if include_f7:
        groups.append(class_three_instances(7))
    for cover, insts in groups:
        backends = [("exact", ExactBackend(cover))]
        if dense and cover.stage_group(cover.c).order <= 625:
            backends.append(("dense_float", DenseBackend(cover)))
        for inst in insts:
            for bname, backend in backends:
                for seed in seeds:
                    start = time.time()
                    recovered, rec = run_rees(cover, inst.oracle, backend, seed=seed,
                                              keep_states=backend.exact)
                    row = grade_run(cover, inst, recovered, rec, backend)
                    row.update(backend=bname, seed=seed, cover_dims=list(cover.dims), p=cover.p,
                               c=cover.c, cover_order=cover.stage_group(cover.c).order,
                               stage_outputs_equal_rho_H_d=(stage_outputs_correct(cover, inst, rec)
                                                            if backend.exact else None),
                               seconds=round(time.time()-start, 2))
                    results.append(row)
    controls = negative_controls()
    exact_rows = [r for r in results if r["backend"] == "exact"]
    return {"status": "exact_small_instance_simulation_not_a_coherent_receiver",
            "coherent_receiver_implemented": False,
            "sde_solver": "brute_force_over_F_p^M_at_Chevalley_Warning_arity_kappa_d*g_d+1",
            "schedule_one_solver_tested": False, "asymptotic_cost_tested": False,
            "runs_total": len(results),
            "all_recovered": all(r["recovered_equals_log_H"] for r in results),
            "all_laws_uniform": all(s["every_source_law_uniform_on_K_perp"]
                                    for r in results for s in r["stages"].values()),
            "all_exact_stage_outputs_equal_rho_H_d": all(r["stage_outputs_equal_rho_H_d"] for r in exact_rows),
            "negative_controls_match_prediction": all(
                c["failure_detected"] == (not c["derived_subgroup_in_H"]) for c in controls),
            "negative_controls": controls, "runs": results,
            "seconds": round(time.time()-t0, 1)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--f7", action="store_true", help="also run class three over F_7")
    parser.add_argument("--seeds", type=int, default=1, help="number of seeds per (G, H)")
    parser.add_argument("--out", help="write JSON here")
    args = parser.parse_args()
    result = report(include_f7=args.f7, seeds=tuple(20261102+i for i in range(args.seeds)))
    text = json.dumps(result, indent=1, default=str)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text+"\n")
    for r in result["runs"]:
        print(r["backend"], r["seed"], r["instance"],
              "recovered" if r["recovered_equals_log_H"] else "FAILED",
              "laws", all(s["every_source_law_uniform_on_K_perp"] for s in r["stages"].values()),
              "states", r["stage_outputs_equal_rho_H_d"], "queries", r["oracle_queries"],
              f"{r['seconds']}s")
    for key in ("runs_total", "all_recovered", "all_laws_uniform", "all_exact_stage_outputs_equal_rho_H_d",
                "negative_controls_match_prediction", "seconds"):
        print(key, result[key])


if __name__ == "__main__":
    main()

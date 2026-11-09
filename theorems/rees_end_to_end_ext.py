"""Scaled exact end-to-end Rees simulation: real SDE solvers, Rule W, class four.

Extends theorems/rees_end_to_end_sim.py (round 1, imported read-only) with

(a) the deterministic Ivanyos-Santha solver of theorems/rees_is_sde_solver.py
    (imported read-only) in place of brute force, at the arity the paper
    charges: B_kappa(g_d) of Rule W (main.tex Remark combined-schedule), or
    on request the smaller count G(kappa, g_d)^ceil(log2 t) that the
    deterministic run consumes (main.tex, Schedule 1 paragraph);
(b) the combined per-grade rule (2026-11-02-rees-combined-schedule.md
    section 1): linear if kappa_d = 1, Schedule 2 (the two-level symmetric
    contraction of theorems/power_sde.py, imported read-only, then the
    Bezout lift) if kappa_d >= 2 and p >= 16 kappa_d^(2 kappa_d + 2),
    else Schedule 1 at degree kappa_d. The choice uses (p, d, g_d) only;
(c) class-four covers (n5 and a second filiform family) through a new exact
    backend, SparseExactBackend, that stores a left-invariant state only on
    its support, so covers of order 7^11 and 11^11 fit;
(d) more hidden subgroups (non-normal, meeting the centre trivially,
    containing it, nonhomogeneous).

SparseExactBackend uses the same representation as round 1,
rho = scale/|G_d| sum_g c(g) R_g, with c(g) in Z[zeta_p], but keeps only the
rows with c(g) != 0. It is cross-checked state by state against round 1's
ExactBackend on the small covers (tests). Two exact simplifications, both
stated: (1) Pi rho Pi = Pi rho, since Pi_lambda is a central idempotent of
the group algebra (round 1 forms both products); (2) a pure function is
memoised on its exact inputs: the label law and post-measurement state of a
state object, and the channel output on a sorted tuple of (post state,
scale). The multiset is enough because the channel's trace function is a
product. Post-measurement states are formed only for sources with s_i != 0;
the others are traced out unread. Labels are sampled for every source, and
every source is charged c queries.

Source preparation has three modes. "exhaustive" is round 1's own checked
routine (whole cover enumerated, coset structure verified). "level_set"
evaluates f on all of L (|L| = p^m points, the same information) and
inverts the linear evaluation maps E_s to get the identity fibre S of the
tuple oracle exactly; S is checked to be a subgroup, and the coset property
is spot-checked on random pairs. "substitute" (only for p = 1031, where
|L| = 1.1e9) builds S = exp(sum_k t^k (h cap gamma_k)) from H and
spot-checks it against the oracle; it is labelled in every output. All
later steps see only the state, the labels and the public cover.

What this does NOT show: no coherent receiver or gate-level circuit; no
asymptotic query, time or error bound; nothing for groups, primes or
subgroups not run. A finite run can only falsify. At the charged arities
almost every block on small fields contains a zero label column, and the
deterministic solver then returns a unit vector; the statistics say how
often the full solver path ran.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import product
import json
from math import gcd
import random
import sys
import time

import numpy as np

from theorems import rees_end_to_end_sim as base
from theorems.power_sde import power_arity, power_weights
from theorems.rees_is_sde_solver import (columns_required, is_arity, is_sde_solve,
                                        reduced_degree, verify as sde_verify)


# ---------------------------------------------------------------- Rule W (public data only)

def schedule2_threshold(kappa):
    return 16*kappa**(2*kappa+2)


@dataclass(frozen=True)
class GradeSchedule:
    d: int
    kappa: int
    g: int
    schedule: str          # "linear", "schedule1" or "schedule2"
    arity: int             # M_d, the columns charged at this grade
    paper_B_d: int         # Schedule 1 as written in main.tex, for comparison


def rule_w(p, d, g, *, count="rule_w"):
    """Schedule and arity at grade d from (p, d, g_d) only.

    count="rule_w": Schedule 1 at B_kappa(g_d) (main.tex Remark combined-schedule).
    count="deterministic": Schedule 1 at G(kappa, g_d)^ceil(log2 t), the columns
    the deterministic run consumes (main.tex, Schedule 1 paragraph)."""
    kappa = gcd(d, p-1)
    if kappa == 1:
        name, M = "linear", g+1
    elif p >= schedule2_threshold(kappa):
        name, M = "schedule2", power_arity(g, kappa)
    elif count == "rule_w":
        name, M = "schedule1", is_arity(kappa, g)
    elif count == "deterministic":
        name, M = "schedule1", columns_required(p, d, g)
    else:
        raise ValueError("count must be 'rule_w' or 'deterministic'")
    return GradeSchedule(d, kappa, g, name, M, is_arity(d, g))


def tree_schedules(cover, count="rule_w"):
    return {d: rule_w(cover.p, d, cover.dims[d-1], count=count) for d in range(2, cover.c+1)}


def charged_queries(cover, schedules, samples):
    """c * S * prod_d M_d: the paper's query count for S terminal samples."""
    total = samples*len(cover.points)
    for d in range(2, cover.c+1):
        total *= schedules[d].arity
    return total


@dataclass
class SolverStats:
    blocks: int = 0
    zero_column_exits: int = 0
    full_solver_runs: int = 0
    theorem11_calls: int = 0
    kernel_calls: int = 0
    early_zero: int = 0
    restarts: int = 0
    schedule2_calls: int = 0
    schedule2_scalar_draws: int = 0
    consumed_max: int = 0
    diagnostic_nonzero_solves: int = 0
    support_sizes: Counter = field(default_factory=Counter)


def solve_block(p, sched, labels, rng, stats, *, avoid_zero_columns=False):
    """Nonzero s with sum_i s_i^d lambda_i = 0, from the schedule Rule W chose.

    avoid_zero_columns (diagnostic witness policy): if some label is zero and the
    nonzero labels alone meet the solver's column count, solve on those, so the
    full solver path runs on real label data. Any nonzero witness is valid for
    the channel, so this is a legitimate policy, but it is not the default."""
    d = sched.d
    cols = labels if isinstance(labels[0], tuple) else [tuple(int(x) for x in lam) for lam in labels]
    if len(cols) != sched.arity:
        raise AssertionError("block size differs from the charged arity")
    stats.blocks += 1
    if avoid_zero_columns and sched.schedule in ("linear", "schedule1"):
        nz = [i for i, col in enumerate(cols) if any(col)]
        if nz and len(nz) < len(cols):
            rank = base.rref([cols[i] for i in nz], p)
            if len(nz) >= columns_required(p, d, len(rank)):
                w = is_sde_solve(p, d, [cols[i] for i in nz])
                s = [0]*len(cols)
                for i, x in zip(nz, w.s):
                    s[i] = x
                s = tuple(s)
                stats.full_solver_runs += 1
                stats.diagnostic_nonzero_solves += 1
                stats.theorem11_calls += w.theorem11_calls
                stats.kernel_calls += w.kernel_calls
                stats.early_zero += bool(w.early_zero)
                stats.restarts += w.restarts
                stats.consumed_max = max(stats.consumed_max, w.columns_required)
                if not sde_verify(p, d, cols, s):
                    raise ArithmeticError("solver returned a non-witness")
                stats.support_sizes[sum(1 for x in s if x)] += 1
                return s
    if sched.schedule in ("linear", "schedule1"):
        w = is_sde_solve(p, d, cols)
        s = w.s
        if w.levels == 0 and w.columns_required == 1 and w.early_zero:
            stats.zero_column_exits += 1
        else:
            stats.full_solver_runs += 1
        stats.theorem11_calls += w.theorem11_calls
        stats.kernel_calls += w.kernel_calls
        stats.early_zero += bool(w.early_zero)
        stats.restarts += w.restarts
        stats.consumed_max = max(stats.consumed_max, w.columns_required)
    else:
        kappa, t = reduced_degree(p, d)
        w = power_weights(p, kappa, cols, rng=rng)
        s = tuple(pow(x, t, p) if x else 0 for x in w.weights)
        stats.schedule2_calls += 1
        stats.full_solver_runs += 1
        stats.schedule2_scalar_draws += sum(w.closure.stage_draws) if w.closure else 0
        stats.consumed_max = max(stats.consumed_max, w.required_columns)
    if not sde_verify(p, d, cols, s):
        raise ArithmeticError("solver returned a non-witness")
    stats.support_sizes[sum(1 for x in s if x)] += 1
    return s


# ---------------------------------------------------------------- sparse exact states

POLY_MAX_PRIME = 64      # above this, coefficients are kept as monomials a*zeta^e


class NotMonomial(ArithmeticError):
    pass


@dataclass(eq=False)
class SparseState:
    """rho = scale/|G_d| sum_g c(g) R_g, rows only where c(g) != 0.

    poly mode (p <= 64): V[i] is a canonical Z[zeta_p] vector of c(idx[i]).
    mono mode: c(idx[i]) = a[i] * zeta^e[i] (a unique representation)."""
    d: int
    scale: Fraction
    idx: np.ndarray
    V: np.ndarray = None
    a: np.ndarray = None
    e: np.ndarray = None
    cache: dict = field(default_factory=dict, repr=False)

    @property
    def mono(self):
        return self.V is None

    def __len__(self):
        return len(self.idx)


def _canon(V):
    return V-V[..., -1:]


def _poly_to_mono(V, p):
    """Canonical vectors -> (a, e), raising NotMonomial otherwise. Zero rows give a = 0."""
    nz = np.count_nonzero(V, axis=1)
    a = np.zeros(len(V), dtype=np.int64)
    e = np.zeros(len(V), dtype=np.int64)
    one = nz == 1
    j = np.argmax(V != 0, axis=1)
    a[one], e[one] = V[one, j[one]], j[one]
    # a*zeta^(p-1) is canonically (-a, ..., -a, 0)
    full = nz == p-1
    if full.any():
        rows = V[full]
        okfull = (rows[:, :-1] == rows[:, :1]).all(axis=1) & (rows[:, -1] == 0)
        if not okfull.all():
            raise NotMonomial("coefficient is not a monomial")
        a[full], e[full] = -rows[:, 0], p-1
    if ((nz > 1) & (nz != p-1)).any():
        raise NotMonomial("coefficient is not a monomial")
    return a, e


def _cyc_conv(A, B, p):
    """Cyclic convolution of rows (product in Z[C_p]), then canonical."""
    if A.size and int(np.abs(A).max())*int(np.abs(B).max())*p >= 2**62:
        raise OverflowError("cyclotomic product could overflow int64")
    out = np.zeros_like(B)
    for j in range(p):
        if A[:, j].any():
            out += A[:, j:j+1]*np.roll(B, j, axis=1)
    return _canon(out)


def _group_sum(keys, rows=None, a=None, e=None, p=None):
    """Sum contributions with equal keys. Returns (ukeys, V) or (ukeys, a, e), zero rows dropped."""
    order = np.argsort(keys, kind="stable")
    keys = keys[order]
    starts = np.r_[0, np.nonzero(np.diff(keys))[0]+1]
    ukeys = keys[starts]
    if rows is not None:
        V = _canon(np.add.reduceat(rows[order], starts, axis=0))
        keep = V.any(axis=1)
        return ukeys[keep], V[keep]
    a, e = a[order], e[order]
    sizes = np.diff(np.r_[starts, len(keys)])
    out_a, out_e = a[starts].copy(), e[starts].copy()
    multi = np.nonzero(sizes > 1)[0]
    if len(multi):
        if len(multi)*p > 5*10**7:
            raise MemoryError("too many colliding monomial groups")
        gid = np.repeat(np.arange(len(starts)), sizes)
        sel = np.isin(gid, multi)
        local = np.searchsorted(multi, gid[sel])
        H = np.zeros((len(multi), p), dtype=np.int64)
        np.add.at(H, (local, e[sel]), a[sel])
        ma, me = _poly_to_mono(_canon(H), p)
        out_a[multi], out_e[multi] = ma, me
    keep = out_a != 0
    return ukeys[keep], out_a[keep], out_e[keep]


class Law:
    """Exact label law prob(lambda) = scale * q[lambda] / P, lambda in F_p^g in product order."""

    def __init__(self, scale, P, q, p, g):
        self.scale, self.P, self.q, self.p, self.g = scale, P, q, p, g
        if (q < 0).any():
            raise ArithmeticError("negative branch probability")
        if scale*int(q.sum()) != P:
            raise ArithmeticError("instrument probabilities do not sum to one")
        self.nonzero = np.nonzero(q)[0]
        w = q[self.nonzero].astype(float)
        self.weights = w/w.sum()
        self._weights_pow = p**np.arange(g-1, -1, -1, dtype=np.int64)
        self.keys = [tuple(int(x) for x in row) for row in product(range(p), repeat=g)]

    def key(self, i):
        return self.keys[i]

    def index(self, lam):
        return int(np.asarray(lam, dtype=np.int64) @ self._weights_pow)

    def prob(self, lam):
        return self.scale*int(self.q[self.index(lam)])/self.P

    def as_dict(self):
        return {self.key(i): self.scale*int(x)/self.P for i, x in enumerate(self.q)}

    def uniform_on(self, allowed):
        """Exact: prob = 1/|allowed| on allowed labels and 0 elsewhere."""
        mask = np.zeros(len(self.q), dtype=bool)
        mask[[self.index(l) for l in allowed]] = True
        n, sc = len(allowed), self.scale
        on = self.q[mask]
        # scale*q/P == 1/n  <=>  q * num * n == P * den
        return bool((self.q[~mask] == 0).all()
                    and all(int(x)*sc.numerator*n == self.P*sc.denominator for x in np.unique(on)))


class SparseExactBackend:
    """Exact simulation of left-invariant states stored on their support."""

    exact = True

    def __init__(self, cover):
        self.cover, self.p = cover, cover.p
        self.mono = cover.p > POLY_MAX_PRIME
        self.groups = {d: cover.stage_group(d) for d in range(1, cover.c+1)}
        for d in range(2, cover.c+1):
            G, g = self.groups[d], cover.dims[d-1]
            n = G.n
            if G.tensor[n-g:, :, :].any() or G.tensor[:, n-g:, :].any():
                raise ArithmeticError("top grade of G_d is not central")
        self._channel_memo = {}
        self._intern = {}
        self.channel_calls = 0
        self.channel_computed = 0

    # -- helpers
    def _P(self, d):
        return self.p**self.cover.dims[d-1]

    def _top_digits(self, d, idx):
        g = self.cover.dims[d-1]
        return (np.asarray(idx)[..., None]//(self.p**np.arange(g-1, -1, -1, dtype=np.int64))) % self.p

    def _top_encode(self, d, digits):
        g = self.cover.dims[d-1]
        return (np.asarray(digits) % self.p) @ (self.p**np.arange(g-1, -1, -1, dtype=np.int64))

    def make_state(self, d, scale, idx, *, ones=False, V=None, a=None, e=None):
        idx = np.asarray(idx, dtype=np.int64)
        if ones:
            if self.mono:
                a, e = np.ones(len(idx), dtype=np.int64), np.zeros(len(idx), dtype=np.int64)
            else:
                V = np.zeros((len(idx), self.p), dtype=np.int64)
                V[:, 0] = 1
        order = np.argsort(idx)
        idx = idx[order]
        if len(idx) > 1 and (np.diff(idx) == 0).any():
            raise ArithmeticError("duplicate support index")
        if V is not None:
            st = SparseState(d, Fraction(scale), idx, V=V[order])
        else:
            st = SparseState(d, Fraction(scale), idx, a=a[order], e=e[order])
        return self._normalized(st)

    def _normalized(self, st):
        """Divide out the content, then intern: a state whose exact representation was
        seen before is replaced by that object (so memoised results are shared)."""
        vals = st.V if st.V is not None else st.a
        g = int(np.gcd.reduce(np.abs(vals).ravel())) if vals.size and vals.any() else 1
        if g > 1:
            if st.V is not None:
                st.V = st.V//g
            else:
                st.a = st.a//g
            st.scale *= g
        key = (st.d, st.scale, st.idx.tobytes(),
               st.V.tobytes() if st.V is not None else st.a.tobytes()+st.e.tobytes())
        return self._intern.setdefault(key, st)

    def coefficient_at_identity(self, st):
        """c(1) as an int, if rational; else None."""
        if not len(st.idx) or st.idx[0] != 0:
            return 0
        if st.mono:
            return int(st.a[0]) if st.e[0] == 0 else None
        row = st.V[0]
        return int(row[0]) if not row[1:].any() else None

    def _check_normalized(self, st, what):
        c1 = self.coefficient_at_identity(st)
        if c1 is None or st.scale*c1 != 1:
            raise ArithmeticError(f"{what}: state is not normalized")

    # -- sources
    def source_from_dense(self, dense_state):
        """Convert a round-1 ExactState (dense rows) to a sparse state."""
        v = base.cyc_canon(dense_state.v)
        rows = np.nonzero(v.any(axis=1))[0]
        if self.mono:
            a, e = _poly_to_mono(v[rows], self.p)
            st = self.make_state(dense_state.d, dense_state.scale, rows, a=a, e=e)
        else:
            st = self.make_state(dense_state.d, dense_state.scale, rows, V=v[rows])
        return st

    def source_from_fibre(self, S_indices):
        st = self.make_state(self.cover.c, Fraction(1), S_indices, ones=True)
        self._check_normalized(st, "source")
        return st

    # -- complete central instrument
    def label_law(self, st):
        """Exact Tr(Pi_lambda rho) = scale/|Z| sum_(w central in supp) c(w) zeta^(lambda.w)."""
        if "law" in st.cache:
            return st.cache["law"]
        d, p = st.d, self.p
        g, P = self.cover.dims[d-1], self._P(d)
        lams = np.array(list(product(range(p), repeat=g)), dtype=np.int64)
        central = np.nonzero(st.idx < P)[0]       # low part zero <=> index < p^g
        W = self._top_digits(d, st.idx[central])
        E = (lams @ W.T) % p                       # (Lambda, k)
        acc = np.zeros((len(lams), p), dtype=np.int64)
        L = np.repeat(np.arange(len(lams)), len(central))
        if st.mono:
            np.add.at(acc, (L, ((st.e[central][None, :]+E) % p).ravel()), np.tile(st.a[central], len(lams)))
        else:
            for w_i, row in zip(range(len(central)), st.V[central]):
                cols = (np.arange(p)[None, :]+E[:, w_i:w_i+1]) % p
                np.add.at(acc, (np.repeat(np.arange(len(lams)), p), cols.ravel()), np.tile(row, len(lams)))
        acc = _canon(acc)
        if acc[:, 1:].any():
            raise ArithmeticError("branch probability is not rational")
        law = Law(st.scale, P, acc[:, 0].copy(), p, g)
        st.cache["law"] = law
        return law

    def condition(self, st, lam):
        """Normalized Pi_lambda rho (= Pi rho Pi). Cached per (state, lambda)."""
        key = ("post", lam)
        if key in st.cache:
            return st.cache[key]
        pr = self.label_law(st).prob(lam)
        if pr == 0:
            raise ArithmeticError("conditioning on a zero-probability label")
        d, p = st.d, self.p
        g, P = self.cover.dims[d-1], self._P(d)
        Z = np.array(list(product(range(p), repeat=g)), dtype=np.int64)
        ph = (-(Z @ np.asarray(lam, dtype=np.int64))) % p        # zeta^(-lambda.z)
        low, top = st.idx//P, st.idx % P
        tdig = self._top_digits(d, top)
        new_top = self._top_encode(d, tdig[:, None, :]+Z[None, :, :])     # (N, |Z|)
        x = (low[:, None]*P+new_top).ravel()
        N = len(st.idx)
        if st.mono:
            a = np.repeat(st.a, len(Z))
            e = ((st.e[:, None]+ph[None, :]) % p).ravel()
            ux, ua, ue = _group_sum(x, a=a, e=e, p=p)
            out = SparseState(d, st.scale/(P*pr), ux, a=ua, e=ue)
        else:
            shift = np.tile(ph, N)
            src = np.repeat(np.arange(N), len(Z))
            rows = st.V[src[:, None], (np.arange(p)[None, :]-shift[:, None]) % p]
            ux, V = _group_sum(x, rows=rows)
            out = SparseState(d, st.scale/(P*pr), ux, V=V)
        out = self._normalized(out)
        self._check_normalized(out, "conditioned state")
        st.cache[key] = out
        return out

    # -- controlled right-action channel
    def channel(self, posts, witness):
        """Output on G_(d-1): c_out(y) = F(lift of y^-1), F(g) = prod_i c_i(-delta_si(g)).
        F is checked constant on every central fibre gZ_d (else: does not descend)."""
        active = [(st, int(s)) for st, s in zip(posts, witness) if s % self.p]
        if not active:
            raise ValueError("zero witness")
        self.channel_calls += 1
        key = tuple(sorted((id(st), s) for st, s in active))
        if key in self._channel_memo:
            return self._channel_memo[key][0]
        self.channel_computed += 1
        d, p = active[0][0].d, self.p
        G = self.groups[d]
        P = self._P(d)
        active.sort(key=lambda t: len(t[0]))
        first, s1 = active[0]
        inv_scales = self.cover.dilation_scales(d, pow(s1, -1, p))
        gcoords = (-G.decode(first.idx)*inv_scales[None, :]) % p       # g with -delta_s1(g) = x
        gidx = G.encode(gcoords)
        if first.mono:
            fa, fe = first.a.copy(), first.e.copy()
        else:
            FV = first.V.copy()
        scale = first.scale
        for st, s in active[1:]:
            y = G.encode((-gcoords*self.cover.dilation_scales(d, s)[None, :]) % p)
            pos = np.searchsorted(st.idx, y)
            pos = np.minimum(pos, len(st.idx)-1)
            found = st.idx[pos] == y
            gcoords, gidx, pos = gcoords[found], gidx[found], pos[found]
            if first.mono:
                fa, fe = fa[found], fe[found]
                if fa.size and int(np.abs(fa).max())*int(np.abs(st.a[pos]).max()) >= 2**62:
                    raise OverflowError("monomial product could overflow int64")
                fa, fe = fa*st.a[pos], (fe+st.e[pos]) % p
                gg = int(np.gcd.reduce(np.abs(fa))) if fa.size else 1
                if gg > 1:
                    fa, scale = fa//gg, scale*gg
            else:
                FV = _cyc_conv(FV[found], st.V[pos], p)
                keep = FV.any(axis=1)
                gcoords, gidx, FV = gcoords[keep], gidx[keep], FV[keep]
                gg = int(np.gcd.reduce(np.abs(FV).ravel())) if FV.size and FV.any() else 1
                if gg > 1:
                    FV, scale = FV//gg, scale*gg
            scale *= st.scale
        order = np.argsort(gidx)
        gidx = gidx[order]
        low = gidx//P
        starts = np.r_[0, np.nonzero(np.diff(low))[0]+1] if len(low) else np.array([], dtype=np.int64)
        sizes = np.diff(np.r_[starts, len(low)])
        if (sizes != P).any():
            raise ArithmeticError("channel output does not descend: F not constant on central fibres")
        if first.mono:
            fa, fe = fa[order], fe[order]
            if ((fa != np.repeat(fa[starts], P)).any() or (fe != np.repeat(fe[starts], P)).any()):
                raise ArithmeticError("channel output does not descend: F not constant on central fibres")
        else:
            FV = FV[order]
            if (FV != np.repeat(FV[starts], P, axis=0)).any():
                raise ArithmeticError("channel output does not descend: F not constant on central fibres")
        Q = self.groups[d-1]
        lows = low[starts]
        out_idx = Q.encode(Q.inv(Q.decode(lows)))
        if first.mono:
            out = self.make_state(d-1, scale, out_idx, a=fa[starts], e=fe[starts])
        else:
            out = self.make_state(d-1, scale, out_idx, V=FV[starts])
        self._check_normalized(out, "channel output")
        self._channel_memo[key] = (out, tuple(st for st, _ in active))
        return out

    # -- terminal abelian Fourier sampling
    def readout_law(self, st):
        """Law of k in F_p^m: prob(k) = scale/|G| sum_w c(w) zeta^(k.w).

        With V = span(supp c), prob is constant on cosets of V^perp (k.w is), so the
        law is a law on classes u = (k.b_i) in F_p^r times uniform on V^perp."""
        if "readout" in st.cache:
            return st.cache["readout"]
        if st.d != 1:
            raise ValueError("readout only on grade one")
        p, G = self.p, self.groups[1]
        m = G.n
        W = G.decode(st.idx)
        basis = _span_basis(W, p)
        r = len(basis)
        pivots = [next(j for j, x in enumerate(row) if x) for row in basis]
        Wp = W[:, pivots] if r else np.zeros((len(W), 0), dtype=np.int64)    # coordinates in the basis
        U = np.array(list(product(range(p), repeat=r)), dtype=np.int64)
        E = (U @ Wp.T) % p
        acc = np.zeros((len(U), p), dtype=np.int64)
        L = np.repeat(np.arange(len(U)), len(W))
        if st.mono:
            np.add.at(acc, (L, ((st.e[None, :]+E) % p).ravel()), np.tile(st.a, len(U)))
        else:
            for w_i in range(len(W)):
                cols = (np.arange(p)[None, :]+E[:, w_i:w_i+1]) % p
                np.add.at(acc, (np.repeat(np.arange(len(U)), p), cols.ravel()), np.tile(st.V[w_i], len(U)))
        acc = _canon(acc)
        if acc[:, 1:].any():
            raise ArithmeticError("Fourier probability is not rational")
        mass = {tuple(int(x) for x in u): st.scale*int(q)*p**(m-r)/G.order for u, q in zip(U, acc[:, 0])}
        if sum(mass.values()) != 1 or min(mass.values()) < 0:
            raise ArithmeticError("Fourier distribution invalid")
        perp = base.nullspace(basis, m, p)
        out = {"basis": basis, "pivots": pivots, "class_mass": mass, "perp": perp}
        st.cache["readout"] = out
        return out

    def sample_readout(self, st, nprng):
        law = self.readout_law(st)
        keys = [k for k, v in law["class_mass"].items() if v]
        w = np.array([float(law["class_mass"][k]) for k in keys])
        u = keys[nprng.choice(len(keys), p=w/w.sum())]
        k = np.zeros(self.groups[1].n, dtype=np.int64)
        for ui, pc in zip(u, law["pivots"]):
            k[pc] = ui
        for v in law["perp"]:
            k = (k+int(nprng.integers(self.p))*np.array(v)) % self.p
        return tuple(int(x) for x in k)

    # -- grading
    def equals_coset_state(self, st, indices):
        idx = np.sort(np.asarray(indices, dtype=np.int64))
        if len(idx) != len(st.idx) or (idx != st.idx).any():
            return False
        if st.mono:
            return bool((st.e == 0).all() and all(st.scale*int(x) == 1 for x in np.unique(st.a)))
        if st.V[:, 1:].any():
            return False
        return all(st.scale*int(x) == 1 for x in np.unique(st.V[:, 0]))

    def equals_dense(self, st, dense):
        """Exact equality with a round-1 ExactState (same group algebra element)."""
        v = base.cyc_canon(dense.v)
        rows = np.nonzero(v.any(axis=1))[0]
        if st.d != dense.d or len(rows) != len(st.idx) or (rows != st.idx).any():
            return False
        if st.mono:
            mine = np.zeros((len(st.idx), self.p), dtype=np.int64)
            mine[np.arange(len(st.idx)), st.e] = st.a
            mine = _canon(mine)
        else:
            mine = st.V
        lhs = mine*(st.scale.numerator*dense.scale.denominator)
        rhs = v[rows]*(dense.scale.numerator*st.scale.denominator)
        return bool((lhs == rhs).all())


def _span_basis(rows, p):
    """RREF basis of the span of many rows (subset, then verified for all)."""
    rows = np.asarray(rows, dtype=np.int64)
    if not len(rows) or not rows.any():
        return []
    pick = rows[np.linspace(0, len(rows)-1, min(len(rows), 64)).astype(int)]
    basis = base.rref(pick.tolist(), p)
    while True:
        perp = base.nullspace(basis, rows.shape[1], p)
        if not perp:
            return basis
        bad = np.nonzero(((rows @ np.array(perp, dtype=np.int64).T) % p).any(axis=1))[0]
        if not len(bad):
            return basis
        basis = base.rref(basis+[tuple(int(x) for x in rows[bad[0]])], p)


# ---------------------------------------------------------------- algebras and hidden subgroups

def filiform5_q(p):
    """Second class-four filiform family: [e1, e_i] = e_(i+1) (i = 2, 3, 4), [e2, e3] = e5."""
    return base.lie_from_brackets(f"Q5(F_{p})", p, 5,
                                  {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (1, 2): {4: 1}})


class LazyHidden:
    """Hiding function f(x) = min index of the left coset xH, computed on demand.

    For groups too large for a full table (Heis(F_1031)); H is enumerated (|H| small)."""

    def __init__(self, name, algebra, generators):
        self.name, self.algebra, self.generators = name, algebra, generators
        self.group = base.NilGroup(algebra.p, algebra.tensor, len(algebra.lower_central_series()))
        self.log_h = algebra.lie_closure(generators) if generators else []
        G = self.group
        H = base.span_elements(self.log_h, algebra.dim, algebra.p)
        Hidx = set(G.encode(H).tolist())
        for h in H:          # Lazard: log of the closure is the Lie closure, so H is a group
            if not set(G.encode(G.mul(H, h[None, :])).tolist()) <= Hidx:
                raise ArithmeticError("Lie closure is not closed under the group law")
        self.subgroup = np.sort(np.array(sorted(Hidx), dtype=np.int64))
        self._H = H

    def oracle(self, x_coords):
        G = self.group
        x = np.asarray(x_coords, dtype=np.int64)
        flat = x.reshape(-1, G.n)
        out = np.full(len(flat), np.iinfo(np.int64).max, dtype=np.int64)
        for h in self._H:
            out = np.minimum(out, G.encode(G.mul(flat, h[None, :])))
        return out.reshape(x.shape[:-1])

    def flags(self):
        return base.HiddenInstance.flags(self)


def hidden(name, algebra, generators, *, lazy=False):
    cls = LazyHidden if lazy else base.HiddenInstance
    return cls(f"{algebra.name} H={name}", algebra, tuple(generators))


def _unit(n, *ones):
    v = [0]*n
    for i in ones:
        v[i] += 1
    return tuple(v)


def heisenberg_subgroups():
    return [("trivial", ()), ("<x> non-normal", ((1, 0, 0),)),
            ("<y+z> non-normal", ((0, 1, 1),)), ("<x+2y+z>", ((1, 2, 1),)),
            ("Z(G)", ((0, 0, 1),)), ("<x,z> normal", ((1, 0, 0), (0, 0, 1))),
            ("<x,y> = G", ((1, 0, 0), (0, 1, 0)))]


def filiform4_subgroups():
    u = lambda *i: _unit(4, *i)
    return [("<e2> non-normal", (u(1),)), ("<e1> non-normal", (u(0),)),
            ("<e1+e3> non-normal", (u(0, 2),)), ("<e2,e4> non-normal", (u(1), u(3))),
            ("<e1+e2,e3> (closure)", (u(0, 1), u(2))), ("<e3,e4> = gamma_2", (u(2), u(3))),
            ("<e2,e3> non-normal", (u(1), u(2))), ("Z(G)", (u(3),)), ("trivial", ()),
            # new in this extension
            ("<e2+e4> non-normal", (u(1, 3),)),
            ("<e2+e3> non-normal", (u(1, 2),)), ("<e1,e4> non-normal", (u(0), u(3))),
            ("<e1+e2> non-normal", (u(0, 1),)), ("<e1+2e2+e4>", ((1, 2, 0, 1),))]


def filiform5_subgroups(kind="n5"):
    u = lambda *i: _unit(5, *i)
    hs = [("trivial", ()), ("<e2> non-normal", (u(1),)), ("<e1> non-normal", (u(0),)),
          ("<e1+e3> non-normal", (u(0, 2),)), ("<e2+e4> non-normal", (u(1, 3),)),
          ("<e3> non-normal", (u(2),)), ("Z(G) = <e5>", (u(4),)),
          ("<e2,e5> non-normal", (u(1), u(4))), ("<e1+e2+e5>", (u(0, 1, 4),))]
    if kind == "q5":
        hs = [h for h in hs if h[0] != "<e3> non-normal"]+[("<e3+e4> non-normal", (u(2, 3),))]
    return hs


# ---------------------------------------------------------------- lifted source (three modes)

def _membership(cover, oracle, a_coords, f0):
    """a in S <=> f(E_s(a)) = f(0) for every evaluation point (oracle calls only)."""
    ok = np.ones(len(a_coords), dtype=bool)
    for s in cover.points:
        ok &= oracle(a_coords @ cover.evaluation_matrix(s) % cover.p) == f0
        if not ok.any():
            break
    return ok


def _check_subgroup(G, S, rng, max_full=4*10**6, samples=20000):
    """S (sorted indices) contains 1 and is closed under products: in full if |S|^2 is
    small, else on random pairs (labelled in the returned info)."""
    if S[0] != 0:
        raise ArithmeticError("identity fibre does not contain the identity")
    n = len(S)
    k = round(np.log(n)/np.log(G.p))
    if G.p**k != n:
        raise ArithmeticError("identity fibre has order not a power of p")
    coords = G.decode(S)
    if n*n <= max_full:
        for i in range(0, n, max(1, max_full//(4*n))):
            block = coords[i:i+max(1, max_full//(4*n))]
            prod_ = G.encode(G.mul(block[:, None, :], coords[None, :, :]).reshape(-1, G.n))
            pos = np.minimum(np.searchsorted(S, prod_), n-1)
            if (S[pos] != prod_).any():
                raise ArithmeticError("identity fibre is not closed under products")
        return "full"
    i, j = rng.integers(n, size=samples), rng.integers(n, size=samples)
    prod_ = G.encode(G.mul(coords[i], coords[j]))
    pos = np.minimum(np.searchsorted(S, prod_), n-1)
    if (S[pos] != prod_).any():
        raise ArithmeticError("identity fibre is not closed under products")
    return f"sampled_{samples}_pairs"


def _coset_spot_check(cover, oracle, G, S, rng, samples=2000):
    """Random a in G~, b in S: the tuple at a*b equals the tuple at a; random
    pairs with a^-1 a' outside S get different tuples."""
    p = cover.p
    a = rng.integers(p, size=(samples, G.n))
    b = G.decode(S[rng.integers(len(S), size=samples)])
    Es = [cover.evaluation_matrix(s) for s in cover.points]
    tup = lambda X: np.stack([oracle(X @ E % p) for E in Es], axis=1)
    if (tup(a) != tup(G.mul(a, b))).any():
        raise ArithmeticError("tuple oracle not constant on sampled left cosets")
    a2 = rng.integers(p, size=(samples, G.n))
    rel = G.encode(G.mul(G.inv(a), a2))
    pos = np.minimum(np.searchsorted(S, rel), len(S)-1)
    outside = S[pos] != rel
    same = (tup(a) == tup(a2)).all(axis=1)
    if (same & outside).any():
        raise ArithmeticError("tuple oracle identifies points in different left cosets")
    return samples


def prepare_source(cover, inst, backend, mode, seed=0):
    """Lifted source rho_S on G~ = G_c and an info dict. Only inst.oracle is used,
    except in mode 'substitute' (labelled)."""
    p, G = cover.p, backend.groups[cover.c]
    rng = np.random.default_rng(seed)
    info = {"mode": mode}
    if mode == "exhaustive":
        shim = type("Shim", (), {})()
        shim.cover, shim.p, shim.groups = cover, p, {cover.c: G}
        dense, extra = base.ExactBackend.prepare_source(shim, inst.oracle)
        info.update(extra, coset_check="exhaustive (round-1 routine)")
        S = np.nonzero(dense.v.any(axis=1))[0]
    elif mode == "level_set":
        m = cover.algebra.dim
        L = base.NilGroup(p, cover.algebra.tensor, cover.c)
        f_all = np.concatenate([inst.oracle(L.decode(np.arange(i, min(i+10**6, L.order))))
                                for i in range(0, L.order, 10**6)])
        f0 = f_all[0]
        Hset = L.decode(np.nonzero(f_all == f0)[0])
        E1 = cover.evaluation_matrix(1)
        hi = E1[m:]                                   # grade >= 2 rows of E_1
        nh = G.n-m
        S_parts = []
        tails = None
        for start in range(0, p**nh, 2*10**6):
            chunk = np.arange(start, min(start+2*10**6, p**nh), dtype=np.int64)
            tails = (chunk[:, None]//(p**np.arange(nh-1, -1, -1, dtype=np.int64))) % p
            img = tails @ hi % p
            for x in Hset:
                a = np.concatenate([(x[None, :]-img) % p, tails], axis=1)
                ok = _membership(cover, inst.oracle, a, f0)
                if ok.any():
                    S_parts.append(G.encode(a[ok]))
        S = np.unique(np.concatenate(S_parts))
        info.update(oracle_points_evaluated=int(L.order), level_set_size=int(len(Hset)),
                    lifted_order=int(len(S)))
        info["subgroup_check"] = _check_subgroup(G, S, rng)
        info["coset_check"] = f"sampled_{_coset_spot_check(cover, inst.oracle, G, S, rng)}_pairs"
    elif mode == "substitute":
        rows, offset, n = [], 0, G.n
        for k, basis in enumerate(base.graded_hidden(cover, inst.log_h)):
            for v in basis:
                row = [0]*n
                row[offset:offset+len(v)] = v
                rows.append(row)
            offset += cover.dims[k]
        S = np.unique(G.encode(base.span_elements(rows, n, p)))
        f0 = inst.oracle(np.zeros((1, cover.algebra.dim), dtype=np.int64))[0]
        sample = G.decode(S[rng.integers(len(S), size=min(len(S), 3000))])
        if not _membership(cover, inst.oracle, sample, f0).all():
            raise ArithmeticError("substitute source: a point of S is outside the identity fibre")
        info.update(lifted_order=int(len(S)),
                    substitute="S = exp(sum_k t^k (h cap gamma_k)) built from H; NOT from the oracle",
                    subgroup_check=_check_subgroup(G, S, rng))
        info["coset_check"] = f"sampled_{_coset_spot_check(cover, inst.oracle, G, S, rng)}_pairs"
    else:
        raise ValueError(mode)
    return backend.source_from_fibre(S), info


# ---------------------------------------------------------------- the algorithm

@dataclass
class ExtRecord:
    schedules: dict
    label_counts: dict = field(default_factory=dict)      # d -> counts per label index
    measured: dict = field(default_factory=dict)          # d -> {id: state} measured
    produced: dict = field(default_factory=dict)          # d -> {id: state} channel outputs
    sources_measured: dict = field(default_factory=dict)  # d -> count
    solver: dict = field(default_factory=dict)            # d -> SolverStats
    block_sizes: dict = field(default_factory=dict)       # d -> set of block sizes
    readout: list = field(default_factory=list)
    readout_states: dict = field(default_factory=dict)
    top_sources: int = 0
    oracle_queries: int = 0
    aborted: str = None


def run_rees_ext(cover, source, backend, schedules, *, seed=0, extra_samples=4,
                 solver=None, avoid_zero_columns=False, trees=None):
    """The Rees algorithm with Rule W arities and the real solvers.

    `source` is the prepared top source (each use charges c queries); the
    driver sees only it, the labels and the public cover. `solver` replaces
    solve_block (negative controls only)."""
    if solver is None:
        solver = lambda *a: solve_block(*a, avoid_zero_columns=avoid_zero_columns)
    rng = random.Random(seed)
    nprng = np.random.default_rng(seed)
    rec = ExtRecord(schedules)
    c = cover.c
    for d in range(2, c+1):
        rec.label_counts[d] = np.zeros(cover.p**cover.dims[d-1], dtype=np.int64)
        rec.measured[d], rec.produced[d-1] = {}, {}
        rec.sources_measured[d] = 0
        rec.solver[d] = SolverStats()
        rec.block_sizes[d] = set()

    p = cover.p
    top_buffer = {"idx": np.zeros(0, dtype=np.int64), "pos": 0}

    def sample_labels(st, n):
        """n i.i.d. labels from the exact law of st (top source: drawn in large
        i.i.d. batches and consumed in order, which is the same joint law)."""
        law = backend.label_law(st)
        rec.measured[st.d].setdefault(id(st), st)
        rec.sources_measured[st.d] += n
        if st is source:
            buf = top_buffer
            if buf["pos"]+n > len(buf["idx"]):
                fresh = law.nonzero[nprng.choice(len(law.nonzero), size=max(n, 1 << 16), p=law.weights)]
                buf["idx"] = np.concatenate([buf["idx"][buf["pos"]:], fresh])
                buf["pos"] = 0
            draws = buf["idx"][buf["pos"]:buf["pos"]+n]
            buf["pos"] += n
        else:
            draws = law.nonzero[nprng.choice(len(law.nonzero), size=n, p=law.weights)]
        rec.label_counts[st.d] += np.bincount(draws, minlength=len(law.q))
        keys = law.keys
        return [keys[i] for i in draws.tolist()]

    def make(d):
        if d == c:
            rec.top_sources += 1
            rec.oracle_queries += len(cover.points)
            return source
        sched = schedules[d+1]
        M = sched.arity
        if d+1 == c:
            rec.top_sources += M
            rec.oracle_queries += M*len(cover.points)
            children = None
            labels = sample_labels(source, M)
        else:
            children = [make(d+1) for _ in range(M)]
            labels = [None]*M
            i = 0
            while i < M:                         # runs of one state object: batch sampling
                j = i
                while j < M and children[j] is children[i]:
                    j += 1
                labels[i:j] = sample_labels(children[i], j-i)
                i = j
        rec.block_sizes[d+1].add(len(labels))
        s = solver(p, sched, labels, rng, rec.solver[d+1])
        posts = [backend.condition(source if children is None else children[i], labels[i])
                 if s[i] % p else None for i in range(M)]
        out = backend.channel(posts, s)
        rec.produced[d].setdefault(id(out), out)
        return out

    samples = []
    for _ in range(cover.algebra.dim+extra_samples if trees is None else trees):
        st = make(1)
        rec.readout_states.setdefault(id(st), st)
        k = backend.sample_readout(st, nprng)
        rec.readout.append(k)
        samples.append(k)
    recovered = base.nullspace(samples, cover.algebra.dim, cover.p)
    return base.rref(recovered, cover.p), rec


def grade_ext(cover, inst, recovered, rec, backend):
    """Exact comparisons with the truth (used only after the run)."""
    p = cover.p
    truth = inst.log_h
    ok = base.rref(recovered, p) == base.rref(truth, p) if truth else not recovered
    stages = {}
    for d in range(cover.c, 1, -1):
        support = base.expected_label_support(cover, truth, d)
        allowed = {tuple(int(x) for x in row) for row in base.span_elements(support, cover.dims[d-1], p)}
        laws_exact = all(backend.label_law(st).uniform_on(allowed) for st in rec.measured[d].values())
        counts = rec.label_counts[d]
        keys = list(product(range(p), repeat=cover.dims[d-1]))
        observed = Counter({k: int(n) for k, n in zip(keys, counts) if n})
        sched = rec.schedules[d]
        stats = rec.solver[d]
        stages[d] = {"schedule": sched.schedule, "kappa": sched.kappa, "g": sched.g,
                     "charged_arity": sched.arity, "paper_B_d": sched.paper_B_d,
                     "block_sizes": sorted(rec.block_sizes[d]),
                     "label_support_size": len(allowed),
                     "sources_measured": rec.sources_measured[d],
                     "distinct_states_measured": len(rec.measured[d]),
                     "every_measured_law_uniform_on_K_perp": laws_exact,
                     "observed_labels_in_support": all(l in allowed for l in observed),
                     "labels_observed": int(counts.sum()),
                     "chi_square": _chi_counts(observed, allowed),
                     "blocks": stats.blocks, "zero_column_exits": stats.zero_column_exits,
                     "full_solver_runs": stats.full_solver_runs,
                     "diagnostic_nonzero_solves": stats.diagnostic_nonzero_solves,
                     "theorem11_calls": stats.theorem11_calls, "restarts": stats.restarts,
                     "schedule2_calls": stats.schedule2_calls,
                     "max_columns_consumed": stats.consumed_max,
                     "witness_support_sizes": dict(sorted(stats.support_sizes.items()))}
    stage_ok = all(backend.equals_coset_state(st, base.expected_stage_indices(cover, truth, d))
                   for d, states in rec.produced.items() for st in states.values())
    top_ok = all(backend.equals_coset_state(st, base.expected_stage_indices(cover, truth, cover.c))
                 for st in rec.measured[cover.c].values())
    g1 = rec.readout_states.values()
    readout_uniform = all(
        base.rref(backend.readout_law(st)["basis"], p) == base.rref(truth, p)
        and backend.readout_law(st)["class_mass"].get(tuple([0]*len(backend.readout_law(st)["basis"]))) == 1
        for st in g1)
    expected_q = charged_queries(cover, rec.schedules, len(rec.readout))
    return {"instance": inst.name, **inst.flags(), "recovered_equals_log_H": ok,
            "recovered_basis": [list(v) for v in recovered], "truth_basis": [list(v) for v in truth],
            "top_sources": rec.top_sources, "oracle_queries": rec.oracle_queries,
            # by construction: queries are charged from the same arities (Rule W is pinned by tests)
            "charged_queries": expected_q, "queries_equal_charged": rec.oracle_queries == expected_q,
            "readout_samples": len(rec.readout),
            "every_stage_output_equals_rho_H_d": stage_ok,
            "top_source_equals_rho_H_c": top_ok,
            "distinct_stage_outputs": {d: len(s) for d, s in rec.produced.items()},
            "readout_law_uniform_on_h_perp": readout_uniform,
            "channel_calls": backend.channel_calls, "channel_outputs_computed": backend.channel_computed,
            "stages": stages}


def _chi_counts(counter, allowed):
    k = len(allowed)
    n = sum(counter.values())
    if k < 2 or n/k < 5:
        return {"skipped": "expected count < 5 or one category", "n": n, "k": k}
    expected = n/k
    stat = sum((counter.get(a, 0)-expected)**2/expected for a in allowed)
    from scipy.stats import chi2
    return {"n": n, "k": k, "statistic": stat, "p_value": float(chi2.sf(stat, k-1))}


def non_witness_solver(p, sched, labels, rng, stats):
    """Negative control: s = e_i for a nonzero label column (a non-witness), when one exists."""
    stats.blocks += 1
    for i, lam in enumerate(labels):
        if any(lam):
            return tuple(int(j == i) for j in range(len(labels)))
    return tuple(int(j == 0) for j in range(len(labels)))


# ---------------------------------------------------------------- catalogue and driver

def catalogue():
    """name -> (algebra builder, subgroup list, source mode, lazy oracle?)."""
    return {
        "heis3": (lambda: base.heisenberg(3), heisenberg_subgroups(), "exhaustive", False),
        "heis5": (lambda: base.heisenberg(5), heisenberg_subgroups(), "exhaustive", False),
        "n4_5": (lambda: base.filiform4(5), filiform4_subgroups(), "exhaustive", False),
        "n4_7": (lambda: base.filiform4(7), filiform4_subgroups(), "exhaustive", False),
        "n5_11": (lambda: base.filiform5(11), filiform5_subgroups(), "level_set", False),
        "n5_7": (lambda: base.filiform5(7), filiform5_subgroups(), "level_set", False),
        "q5_7": (lambda: filiform5_q(7), filiform5_subgroups("q5"), "level_set", False),
        "heis1031": (lambda: base.heisenberg(1031), heisenberg_subgroups()[:4], "substitute", True),
    }


def run_instance(key, h_names=None, *, count="rule_w", seeds=(20261102,), extra_samples=4,
                 log=None, avoid_zero_columns=False):
    build, hs, mode, lazy = catalogue()[key]
    alg = build()
    cover = base.make_cover(alg)
    schedules = tree_schedules(cover, count)
    rows = []
    for name, gens in hs:
        if h_names is not None and name not in h_names:
            continue
        inst = hidden(name, alg, gens, lazy=lazy)
        for seed in seeds:
            t0 = time.time()
            backend = SparseExactBackend(cover)
            source, info = prepare_source(cover, inst, backend, mode, seed)
            t1 = time.time()
            try:
                recovered, rec = run_rees_ext(cover, source, backend, schedules, seed=seed,
                                              extra_samples=extra_samples,
                                              avoid_zero_columns=avoid_zero_columns)
            except RuntimeError as exc:          # Schedule 2 Las Vegas cap only
                if "sampler exhausted" not in str(exc):
                    raise
                rows.append({"instance": inst.name, "seed": seed, "aborted": str(exc)})
                continue
            row = grade_ext(cover, inst, recovered, rec, backend)
            row.update(group=key, p=cover.p, c=cover.c, cover_dims=list(cover.dims), count=count,
                       witness_policy="avoid_zero_columns (diagnostic)" if avoid_zero_columns
                       else "solver on the whole block",
                       seed=seed, source=info, source_seconds=round(t1-t0, 2),
                       seconds=round(time.time()-t0, 2))
            rows.append(row)
            if log:
                print(_summary(row), file=log, flush=True)
    return rows


def _summary(r):
    if "aborted" in r:
        return f"{r['instance']} seed {r['seed']} ABORTED {r['aborted']}"
    st = r["stages"]
    return (f"{r['instance']} [{r['count']}] seed {r['seed']}: "
            f"{'recovered' if r['recovered_equals_log_H'] else 'FAILED'}, "
            f"laws {all(s['every_measured_law_uniform_on_K_perp'] for s in st.values())}, "
            f"states {r['every_stage_output_equals_rho_H_d']}, readout {r['readout_law_uniform_on_h_perp']}, "
            f"queries {r['oracle_queries']} (charged {r['charged_queries']}), "
            f"arities {[st[d]['charged_arity'] for d in sorted(st)]}, "
            f"full solver runs {[st[d]['full_solver_runs'] for d in sorted(st)]}/"
            f"{[st[d]['blocks'] for d in sorted(st)]}, {r['seconds']}s")


def summarize(rows):
    done = [r for r in rows if "aborted" not in r]
    return {"runs": len(rows), "aborted": len(rows)-len(done),
            "all_recovered": all(r["recovered_equals_log_H"] for r in done),
            "all_laws_uniform": all(s["every_measured_law_uniform_on_K_perp"] for r in done for s in r["stages"].values()),
            "all_stage_outputs_equal_rho_H_d": all(r["every_stage_output_equals_rho_H_d"] for r in done),
            "all_top_sources_equal_rho_H_c": all(r.get("top_source_equals_rho_H_c", True) for r in done),
            "all_readout_laws_uniform_on_h_perp": all(r["readout_law_uniform_on_h_perp"] for r in done),
            "all_queries_equal_charged": all(r["queries_equal_charged"] for r in done),
            "all_block_sizes_equal_charged_arity": all(s["block_sizes"] == [s["charged_arity"]]
                                                       for r in done for s in r["stages"].values())}


def _tree_worker(args):
    """One process: `trees` independent descent trees of one (G, H), graded locally."""
    key, name, count, seed, trees = args
    build, hs, mode, lazy = catalogue()[key]
    alg = build()
    cover = base.make_cover(alg)
    inst = hidden(name, alg, dict(hs)[name], lazy=lazy)
    backend = SparseExactBackend(cover)
    source, info = prepare_source(cover, inst, backend, mode, seed)
    schedules = tree_schedules(cover, count)
    _, rec = run_rees_ext(cover, source, backend, schedules, seed=seed, trees=trees)
    row = grade_ext(cover, inst, [], rec, backend)
    row["samples"] = rec.readout
    row["source"] = info
    return row


def run_instance_parallel(key, name, *, count="rule_w", seed=20261102, extra_samples=4, workers=4,
                          log=None):
    """The S = m + extra_samples trees are independent; run them in `workers` processes with
    independent seeds (seed*1000 + worker) and pool the grade-one samples. Every worker grades
    its own trees exactly; the pooled row ANDs the flags and sums the counts."""
    import multiprocessing as mp
    build, hs, mode, lazy = catalogue()[key]
    alg = build()
    S = alg.dim+extra_samples
    split = [S//workers+(i < S % workers) for i in range(workers)]
    jobs = [(key, name, count, seed*1000+i, t) for i, t in enumerate(split) if t]
    t0 = time.time()
    with mp.get_context("spawn").Pool(len(jobs)) as pool:
        parts = pool.map(_tree_worker, jobs)
    cover = base.make_cover(alg)
    inst = hidden(name, alg, dict(hs)[name], lazy=lazy)
    samples = [k for part in parts for k in part["samples"]]
    recovered = base.rref(base.nullspace(samples, alg.dim, cover.p), cover.p)
    truth = inst.log_h
    row = {"instance": inst.name, **inst.flags(), "group": key, "p": cover.p, "c": cover.c,
           "cover_dims": list(cover.dims), "count": count, "seed": seed, "workers": len(jobs),
           "witness_policy": "solver on the whole block",
           "recovered_equals_log_H": recovered == base.rref(truth, cover.p) if truth else not recovered,
           "recovered_basis": [list(v) for v in recovered], "truth_basis": [list(v) for v in truth],
           "readout_samples": len(samples), "source": parts[0]["source"]}
    for flag in ("every_stage_output_equals_rho_H_d", "top_source_equals_rho_H_c",
                 "readout_law_uniform_on_h_perp"):
        row[flag] = all(part[flag] for part in parts)
    for num in ("top_sources", "oracle_queries", "channel_calls", "channel_outputs_computed"):
        row[num] = sum(part[num] for part in parts)
    row["charged_queries"] = charged_queries(cover, tree_schedules(cover, count), len(samples))
    row["queries_equal_charged"] = row["oracle_queries"] == row["charged_queries"]
    stages = {}
    for d in parts[0]["stages"]:
        st = dict(parts[0]["stages"][d])
        for part in parts[1:]:
            o = part["stages"][d]
            for k in ("sources_measured", "blocks", "zero_column_exits", "full_solver_runs",
                      "diagnostic_nonzero_solves", "theorem11_calls", "restarts", "schedule2_calls",
                      "labels_observed"):
                st[k] += o[k]
            st["distinct_states_measured"] = max(st["distinct_states_measured"], o["distinct_states_measured"])
            st["max_columns_consumed"] = max(st["max_columns_consumed"], o["max_columns_consumed"])
            st["block_sizes"] = sorted(set(st["block_sizes"]) | set(o["block_sizes"]))
            for flag in ("every_measured_law_uniform_on_K_perp", "observed_labels_in_support"):
                st[flag] = st[flag] and o[flag]
            ws = Counter({int(a): b for a, b in st["witness_support_sizes"].items()})
            ws.update({int(a): b for a, b in o["witness_support_sizes"].items()})
            st["witness_support_sizes"] = dict(sorted(ws.items()))
        st["chi_square"] = "per worker only"
        stages[d] = st
    row["stages"] = stages
    row["seconds"] = round(time.time()-t0, 2)
    if log:
        print(_summary(row), file=log, flush=True)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("groups", nargs="+", choices=sorted(catalogue()))
    parser.add_argument("--count", default="rule_w", choices=("rule_w", "deterministic"))
    parser.add_argument("--seeds", type=int, default=1)
    parser.add_argument("--extra-samples", type=int, default=4,
                        help="S = m + this many terminal samples (round 1 used 4; t = 1 at eps = 1/3)")
    parser.add_argument("--h", action="append", help="restrict to these subgroup names")
    parser.add_argument("--avoid-zero-columns", action="store_true",
                        help="diagnostic witness policy: solve on the nonzero labels when possible")
    parser.add_argument("--workers", type=int, default=0,
                        help="run the trees of each (G, H) in this many processes (needs one --h per run)")
    parser.add_argument("--out", help="write JSON here")
    args = parser.parse_args()
    seeds = tuple(20261102+i for i in range(args.seeds))
    rows = []
    t0 = time.time()
    for key in args.groups:
        if args.workers:
            for name in args.h:
                rows.append(run_instance_parallel(key, name, count=args.count, seed=seeds[0],
                                                  extra_samples=args.extra_samples,
                                                  workers=args.workers, log=sys.stdout))
            continue
        rows += run_instance(key, args.h, count=args.count, seeds=seeds, log=sys.stdout,
                             extra_samples=args.extra_samples,
                             avoid_zero_columns=args.avoid_zero_columns)
    result = {"status": "exact_small_instance_simulation_not_a_coherent_receiver",
              "coherent_receiver_implemented": False, "asymptotic_cost_tested": False,
              "count": args.count, "groups": args.groups, **summarize(rows),
              "seconds": round(time.time()-t0, 1), "rows": rows}
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(json.dumps(result, indent=1, default=str)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, default=str))


if __name__ == "__main__":
    main()

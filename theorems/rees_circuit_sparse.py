"""Sparse coset-support simulation mode for the gate-level Rees circuit generator.

Adds to theorems/rees_circuit_general.py (imported read-only, not edited) a
simulation mode whose states are stored only on their support, so class
four (n5 over F_5, |G_4| = 5^11 ~ 4.9e7) fits in memory. AI-checked, pending
human review.

Same circuits, same conventions as the dense Engine of rees_circuit_general:
rho[x, y] = phi(x^-1 y)/|G_d|, phi(g) = scale * sum_j V[g, j] zeta^j with
canonical Z[zeta_p] rows (last coordinate zero), but only rows with
phi(g) != 0 are kept (SState: sorted indices idx and rows V). Nothing here
is a new formula: every step is the dense Engine's step restricted to the
support, and on Heis(F_3) and n4(F_5) the two are compared state by state.

* source: the source gate list (QFT_p head checked, then X/CX/MCX/SWAP/U_f)
  is evaluated bit-sliced on ALL canonical addresses of G_c, in address
  chunks, so no |G_c|-sized coordinate array is ever formed; only one int64
  key per address is kept (the label bits of the c oracle registers). The
  checks are the dense ones: address unchanged, workspace clean, all fibres
  of equal size, the identity fibre S a subgroup, every fibre a left coset
  of S (key(x g) = key(x) for all x and each generator g of S, chunked);
  then rho = 1_S/|G_c| on its support S;
* instrument: the exponents e_j[lambda][u] are those that
  rees_circuit_general.instrument_semantics derives from the instrument's
  own gate list (by default exactly in Z[zeta_p], no floating point; the old
  float-and-round path with --instrument float); conditioning is
  phi'(g) = p^-g_d sum_u zeta^e(u) phi(g+u) on the support rows (the support grows to the central saturation S Z_d);
* merge: F(g) = prod_i phi_i(delta_si(g)) on the intersection of the
  supports, checked to be constant on full central fibres (descent), and the
  output is psi = F o sigma on G_(d-1). The gate-level fact that the merge
  gate list is the BCH right translation is the generator's own prove_merge
  (macro exhaustion + symbolic replay), run here for every d and s;
* readout: P(k) = |G_1|^-1 sum_(w in supp) zeta^(-k.w) psi(w), exact.

What this does NOT show: anything asymptotic; a coherent receiver
(coherent_receiver_implemented stays false); a monolithic simulation (the
modules are composed by the tensor / Schur identities, as in the dense
mode); finite-gate QFT or poly(log p) arithmetic; noise; the oracle cost.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import product
import json
import os
import random
import time

import numpy as np

from theorems.rees_circuit_general import (
    STATUS, BitSim, Config, Engine, Hidden, XState, _qft_ok, all_witnesses, allowed_labels, check_instance,
    compile_ops, heis3_instances, instrument_semantics, merge_bitlevel, n4_instances, prove_merge, run_algorithm, solve_sde,
    source_circuit, stage_indices, wires_of,
)
from theorems.rees_end_to_end_sim import (
    cyc_canon, cyc_mul, cyc_rational, filiform4, filiform5, heisenberg, nullspace, rref, span_elements,
)

SPARSE_STATUS = {**STATUS, "status": "sparse_coset_support_simulation_of_generated_circuits_finite_instances",
                 "coherent_receiver_implemented": False}


# ====================================================================== sparse exact states

@dataclass(eq=False)
class SState:
    """rho[x, y] = phi(x^-1 y)/|G_d|, phi(idx[i]) = scale * sum_j V[i, j] zeta^j; phi = 0 off idx."""
    d: int
    scale: Fraction
    idx: np.ndarray
    V: np.ndarray
    cache: dict = field(default_factory=dict, repr=False)

    def __len__(self):
        return len(self.idx)

    def normalized(self):
        g = int(np.gcd.reduce(np.abs(self.V).ravel())) if self.V.size and self.V.any() else 1
        return SState(self.d, self.scale*g, self.idx, self.V//g) if g > 1 else self

    def value_at_identity(self):
        if not len(self.idx) or self.idx[0] != 0:
            return Fraction(0)
        q = cyc_rational(self.V[0])
        if q is None:
            raise ArithmeticError("trace is not rational")
        return self.scale*q

    def equals_indicator(self, indices):
        """phi = 1_indices exactly."""
        ind = np.sort(np.asarray(indices, dtype=np.int64))
        if len(ind) != len(self.idx) or (ind != self.idx).any() or self.V[:, 1:].any():
            return False
        return bool((self.V[:, 0]*self.scale.numerator == self.scale.denominator).all())

    def key(self):
        return (self.d, self.scale, self.idx.tobytes(), self.V.tobytes())

    @classmethod
    def from_dense(cls, st):
        v = cyc_canon(st.v)
        rows = np.nonzero(v.any(axis=1))[0]
        return cls(st.d, st.scale, rows.astype(np.int64), v[rows]).normalized()

    def equals_dense(self, st):
        """Exact equality of the group-algebra element with a dense XState."""
        v = cyc_canon(st.v)
        rows = np.nonzero(v.any(axis=1))[0]
        if self.d != st.d or len(rows) != len(self.idx) or (rows != self.idx).any():
            return False
        lhs = self.V*(self.scale.numerator*st.scale.denominator)
        rhs = v[rows]*(st.scale.numerator*self.scale.denominator)
        return bool((lhs == rhs).all())


def _group_sum(keys, rows):
    """Sum rows with equal keys; canonical; zero rows dropped. Returns (sorted keys, rows)."""
    if not len(keys):
        return keys.astype(np.int64), rows
    order = np.argsort(keys, kind="stable")
    keys = keys[order]
    starts = np.r_[0, np.nonzero(np.diff(keys))[0]+1]
    V = cyc_canon(np.add.reduceat(rows[order], starts, axis=0))
    keep = V.any(axis=1)
    return keys[starts][keep], V[keep]


# ====================================================================== engine

class SparseEngine:
    """Exact composition of the simulated modules, states on their support only."""

    def __init__(self, cfg, chunk=1 << 20):
        self.cfg, self.p, self.chunk = cfg, cfg.p, int(chunk)
        self.kernels = {d: instrument_semantics(cfg, d) for d in range(2, cfg.c+1)}
        self._tables = {}

    # -- per-grade tables: central shifts and instrument exponents
    def tables(self, d):
        if d not in self._tables:
            p, g = self.p, self.cfg.dims[d-1]
            P = p**g
            Z = np.array(list(product(range(p), repeat=g)), dtype=np.int64).reshape(-1, g)
            w = p**np.arange(g-1, -1, -1, dtype=np.int64)
            sub = np.stack([((Z-u) % p) @ w for u in Z], axis=1)       # sub[t, u] = t - u
            expo, _ = self.kernels[d]
            E = np.zeros((P, P), dtype=np.int64)                         # E[lam, u] = e(lam, u)
            for li, lam in enumerate(Z):
                for ui, u in enumerate(Z):
                    E[li, ui] = sum(int(expo[j][lam[j], u[j]]) for j in range(g)) % p
            self._tables[d] = (P, Z, sub, E)
        return self._tables[d]

    # -- source from the source gate list, chunked over all canonical addresses
    def source(self, inst, points=None, uncompute=True, expand_oracle=False):
        cfg, p = self.cfg, self.p
        qc, B, (a_reg, a, w_reg, w, labels) = source_circuit(cfg, inst, points, uncompute)
        head = qc.data[:len(a)]
        if [i.operation.name for i in head] != [f"qft{p}"]*len(a) or \
                [tuple(i.qubits) for i in head] != list(a) or not _qft_ok(p):
            raise AssertionError("source must start with exact QFT_p on each address coordinate")
        pos = {q: i for i, q in enumerate(qc.qubits)}
        ops = compile_ops(qc.data[len(a):], pos)
        law = cfg.laws[cfg.c]
        N = law.order
        lb = cfg.label_bits
        if lb*len(labels) > 62:
            raise ValueError("label tuple does not fit one int64 key")
        key = np.empty(N, dtype=np.int64)
        wkey = None
        addr_ok = work_clean = True
        a_w, w_w = wires_of(a, pos), wires_of(w, pos)
        y_w = [[pos[q] for q in y] for y in labels]
        for start in range(0, N, self.chunk):
            stop = min(N, start+self.chunk)
            X = law.decode(np.arange(start, stop, dtype=np.int64))
            sim = BitSim(qc.num_qubits, stop-start)
            sim.load(a_w, X)
            sim.run(ops, expand_oracle=expand_oracle)
            addr_ok &= bool((sim.read(a_w) == X).all())
            Wv = sim.read(w_w)
            clean = bool((Wv == 0).all())
            if not clean and wkey is None:
                wkey = np.zeros(N, dtype=np.int64)
            if wkey is not None:
                wkey[start:stop] = Wv @ (p**np.arange(Wv.shape[1]-1, -1, -1, dtype=np.int64))
            work_clean &= clean
            k = np.zeros(stop-start, dtype=np.int64)
            for i, wires in enumerate(y_w):
                k |= sim.read_bits(wires) << (lb*i)
            key[start:stop] = k
            del sim, X
        if wkey is not None:                       # dirty workspace: it is part of the fibre key
            _, key = np.unique(np.stack([key, wkey], axis=1), axis=0, return_inverse=True)
            key = key.ravel().astype(np.int64)
            del wkey
        S = np.nonzero(key == key[0])[0]
        _, sizes = np.unique(key, return_counts=True)
        info = {"address_unchanged": addr_ok, "workspace_clean": work_clean,
                "fibres": int(len(sizes)), "lifted_order": int(len(S)),
                "equal_fibres": bool((sizes == len(S)).all())}
        del sizes
        Sset = set(S.tolist())
        gens, gen_set = [], {0}
        for x in S:
            if int(x) not in gen_set:
                gens.append(int(x))
                gen_set = set(law.closure(law.decode(np.array(gens))).tolist())
        info["identity_fibre_is_subgroup"] = gen_set == Sset
        cosets = info["equal_fibres"]
        for g in gens:
            if not cosets:
                break
            gv = law.decode(np.array([g]))
            for start in range(0, N, self.chunk):
                stop = min(N, start+self.chunk)
                X = law.decode(np.arange(start, stop, dtype=np.int64))
                if (key[law.encode(law.mul(X, gv))] != key[start:stop]).any():
                    cosets = False
                    break
        info["fibres_are_left_cosets"] = bool(cosets)
        info["coset_generators"] = len(gens)
        info["coset_state"] = info["identity_fibre_is_subgroup"] and info["fibres_are_left_cosets"] and addr_ok
        info["chunks"] = -(-N//self.chunk)
        del key
        if info["coset_state"]:
            V = np.zeros((len(S), p), dtype=np.int64)
            V[:, 0] = 1
            st = SState(cfg.c, Fraction(1), S.astype(np.int64), V)
        else:
            st = SState(cfg.c, Fraction(1), np.zeros(0, dtype=np.int64), np.zeros((0, p), dtype=np.int64))
        return st, S, info

    # -- complete central instrument
    def condition_unnormalized(self, st, lam):
        d, p = st.d, self.p
        P, Z, sub, E = self.tables(d)
        li = int(np.asarray(lam, dtype=np.int64) @ (p**np.arange(len(lam)-1, -1, -1, dtype=np.int64)))
        e = E[li]                                           # e[u]
        low, top = st.idx//P, st.idx % P
        keys = (low[:, None]*P+sub[top]).ravel()            # g = (low, t - u) gets zeta^e(u) phi(low, t)
        cols = (np.arange(p)[None, :]-e[:, None]) % p       # zeta^e(u) * v = roll(v, e(u))
        rows = st.V[:, cols].reshape(-1, p)                  # rows[i, u] = roll(V[i], e[u])
        idx, V = _group_sum(keys, rows)
        return SState(d, st.scale/P, idx, V)

    def label_probs(self, st):
        """prob(lambda) for every lambda in product order (dense label_law's first output)."""
        if "probs" in st.cache:
            return st.cache["probs"]
        d, p = st.d, self.p
        P, Z, sub, E = self.tables(d)
        central = np.nonzero(st.idx < P)[0]                 # low part zero
        acc = np.zeros((P, p), dtype=np.int64)
        for r in central:
            u = int(st.idx[r])
            for sh in range(p):
                sel = E[:, u] == sh
                if sel.any():
                    acc[sel] += np.roll(st.V[r], sh)
        acc = cyc_canon(acc)
        if acc[:, 1:].any():
            raise ArithmeticError("branch probability is not rational")
        probs = {}
        for li, lam in enumerate(Z):
            pr = st.scale*int(acc[li, 0])/P
            if pr < 0:
                raise ArithmeticError("negative branch probability")
            probs[tuple(int(x) for x in lam)] = pr
        if sum(probs.values()) != 1:
            raise ArithmeticError("instrument probabilities do not sum to one")
        st.cache["probs"] = probs
        return probs

    def conditioned(self, st, lam):
        lam = tuple(int(x) for x in lam)
        key = ("post", lam)
        if key not in st.cache:
            pr = self.label_probs(st)[lam]
            if not pr:
                raise ArithmeticError("conditioning on a zero-probability label")
            un = self.condition_unnormalized(st, lam)
            out = SState(st.d, un.scale/pr, un.idx, un.V).normalized()
            if out.value_at_identity() != 1:
                raise ArithmeticError("conditioned state is not normalized")
            if pr != un.value_at_identity():
                raise ArithmeticError("label probability is not the trace of the conditioned branch")
            st.cache[key] = out
        return st.cache[key]

    def label_law(self, st):
        """Same output as Engine.label_law: (probs, states for pr > 0)."""
        probs = self.label_probs(st)
        return probs, {lam: self.conditioned(st, lam) for lam, pr in probs.items() if pr}

    # -- controlled right-action channel and descent
    def merge(self, states, witness):
        """psi = F o sigma, F(g) = prod_i phi_i(delta_si(g)), F checked constant on central fibres."""
        cfg, p = self.cfg, self.p
        active = [(st, int(s) % p) for st, s in zip(states, witness) if int(s) % p]
        if not active:
            raise ValueError("zero witness")
        d = active[0][0].d
        law = cfg.laws[d]
        P = p**cfg.dims[d-1]
        order = sorted(range(len(active)), key=lambda i: len(active[i][0]))
        st1, s1 = active[order[0]]
        inv = np.array(cfg.scales(d, pow(s1, -1, p)), dtype=np.int64)
        g = (law.decode(st1.idx)*inv[None, :]) % p            # delta_s1(g) = x  for x in supp phi_1
        F, scale = st1.V.copy(), st1.scale
        for k in order[1:]:
            st, s = active[k]
            y = law.encode(g*np.array(cfg.scales(d, s), dtype=np.int64)[None, :])
            pos = np.minimum(np.searchsorted(st.idx, y), max(len(st.idx)-1, 0))
            found = (st.idx[pos] == y) if len(st.idx) else np.zeros(len(y), dtype=bool)
            g, F = g[found], cyc_mul(F[found], st.V[pos[found]], p)
            keep = F.any(axis=1)
            g, F = g[keep], F[keep]
            gg = int(np.gcd.reduce(np.abs(F).ravel())) if F.size and F.any() else 1
            if gg > 1:
                F, scale = F//gg, scale*gg
            scale *= st.scale
        gidx = law.encode(g) if len(g) else np.zeros(0, dtype=np.int64)
        o = np.argsort(gidx)
        gidx, F = gidx[o], F[o]
        low = gidx//P
        starts = np.r_[0, np.nonzero(np.diff(low))[0]+1] if len(low) else np.zeros(0, dtype=np.int64)
        sizes = np.diff(np.r_[starts, len(low)])
        if (sizes != P).any() or (F != np.repeat(F[starts], P, axis=0)).any() or \
                (gidx % P != np.tile(np.arange(P), len(starts))).any():
            raise ArithmeticError("merge output does not descend (not constant on central fibres)")
        out = SState(d-1, scale, low[starts].astype(np.int64), F[starts].copy()).normalized()
        if out.value_at_identity() != 1:
            raise ArithmeticError("merge output lost normalization")
        return out

    # -- terminal Fourier sampling
    def readout(self, st):
        """Same output as Engine.readout (dict over k in product order, zero entries omitted)."""
        if st.d != 1:
            raise ValueError("readout on grade one only")
        if "readout" in st.cache:
            return st.cache["readout"]
        p, law = self.p, self.cfg.laws[1]
        K = law.elements()
        Wsupp = law.decode(st.idx)
        E = (-(K @ Wsupp.T)) % p                               # (|G_1|, |supp|)
        acc = np.zeros((law.order, p), dtype=np.int64)
        for r in range(p):
            acc += np.roll((E == r).astype(np.int64) @ st.V, r, axis=-1)
        acc = cyc_canon(acc)
        if acc[:, 1:].any():
            raise ArithmeticError("Fourier probability is not rational")
        probs = {tuple(int(x) for x in k): st.scale*int(a)/law.order for k, a in zip(K, acc[:, 0]) if a}
        if sum(probs.values()) != 1 or min(probs.values()) < 0:
            raise ArithmeticError("Fourier distribution invalid")
        st.cache["readout"] = probs
        return probs


# ====================================================================== checks and runs (sparse mode)

def check_instance_sparse(cfg, inst, engine=None, *, max_cases=4000, sample_tuples=6, max_witnesses=None,
                          seed=0, log=None, source=None):
    """rees_circuit_general.check_instance in the sparse mode: same rng use, same
    tuple / witness selection, same grading; plus the support sizes. `source` may be
    a precomputed eng.source(inst) result (it is then not recomputed)."""
    eng = engine or SparseEngine(cfg)
    rng = random.Random(seed)
    p, c = cfg.p, cfg.c
    t0 = time.time()
    st, S, sinfo = source if source is not None else eng.source(inst)
    row = {"instance": inst.name, "normal": inst.normal, "dim_h": len(inst.log_h), "source": sinfo,
           "source_equals_rho_lift": bool(sinfo["coset_state"] and
                                          np.array_equal(np.sort(S), stage_indices(cfg, inst.log_h, c))),
           "source_workspace_clean": sinfo["workspace_clean"], "grades": {},
           "group_order_top": int(cfg.laws[c].order), "source_seconds": round(time.time()-t0, 1)}
    if log:
        log(inst.name, "source", row["source_equals_rho_lift"], row["source_seconds"], "s")
    ok = row["source_equals_rho_lift"] and row["source_workspace_clean"]
    for d in range(c, 1, -1):
        probs, states = eng.label_law(st)
        allowed = allowed_labels(cfg, inst.log_h, d)
        law_ok = all(pr == (Fraction(1, len(allowed)) if lam in allowed else 0) for lam, pr in probs.items())
        M = cfg.arity[d]
        total = len(allowed)**M
        expected_cases = total*p**M//len(allowed)
        if expected_cases <= max_cases:
            tuples, mode = list(product(allowed, repeat=M)), "all"
        else:
            zero = tuple([0]*cfg.dims[d-1])
            tuples = [tuple([zero]*M), tuple([allowed[-1]]*M)]
            tuples += [tuple(rng.choice(allowed) for _ in range(M)) for _ in range(max(0, sample_tuples-2))]
            mode = f"sampled {len(tuples)} of {total}"
        target = stage_indices(cfg, inst.log_h, d-1)
        cases = good = capped = 0
        for labels in tuples:
            wits = all_witnesses(labels, d, p)
            if mode != "all" and max_witnesses is not None and len(wits) > max_witnesses:
                wits = wits[sorted(rng.sample(range(len(wits)), max_witnesses))]
                capped += 1
            for s in wits:
                act = [states[lam] for lam, si in zip(labels, s) if si]
                out = eng.merge(act, [int(x) for x in s if x])
                cases += 1
                good += out.equals_indicator(target)
        row["grades"][d] = {"label_support": len(allowed), "label_law_uniform_on_K_perp": bool(law_ok),
                            "arity": M, "tuples": mode, "tuples_with_witnesses_capped": capped,
                            "cases": cases, "merge_outputs_equal_rho_H": good == cases,
                            "state_support": len(st), "branch_support_max": max(len(v) for v in states.values()),
                            "group_order": int(cfg.laws[d].order), "target_support": int(len(target))}
        if log:
            log(inst.name, f"grade {d}", law_ok, mode, cases, good == cases, round(time.time()-t0, 1), "s")
        ok = ok and law_ok and good == cases and cases > 0
        V = np.zeros((len(target), p), dtype=np.int64)
        V[:, 0] = 1
        st = SState(d-1, Fraction(1), np.sort(target).astype(np.int64), V)
    probs = eng.readout(st)
    h_perp = {tuple(int(x) for x in r) for r in span_elements(nullspace(inst.log_h, cfg.m, p), cfg.m, p)}
    row["readout_uniform_on_h_perp"] = set(probs) == h_perp and \
        all(v == Fraction(1, len(h_perp)) for v in probs.values())
    row["nullspace_of_readout_support_equals_log_H"] = \
        rref(nullspace(sorted(h_perp), cfg.m, p), p) == rref(inst.log_h, p)
    row["passed"] = bool(ok and row["readout_uniform_on_h_perp"] and row["nullspace_of_readout_support_equals_log_H"])
    row["seconds"] = round(time.time()-t0, 2)
    return row


def run_algorithm_sparse(cfg, inst, engine=None, seed=0, extra_samples=4, solver="auto", top=None):
    """rees_circuit_general.run_algorithm in the sparse mode (same rng use)."""
    eng = engine or SparseEngine(cfg)
    rng = random.Random(seed)
    p, c = cfg.p, cfg.c
    if top is None:
        top, _, _ = eng.source(inst)
    law_cache = {}
    stats = Counter()

    def law_of(st, key):
        if key not in law_cache:
            law_cache[key] = eng.label_law(st)
        return law_cache[key]

    def sample(probs):
        keys = [k for k in probs if probs[k]]
        return rng.choices(keys, weights=[float(probs[k]) for k in keys], k=1)[0]

    def make(d):
        if d == c:
            stats["top_sources"] += 1
            probs, states = law_of(top, ("top",))
            lam = sample(probs)
            return lam, states[lam]
        kids = [make(d+1) for _ in range(cfg.arity[d+1])]
        labels = [k[0] for k in kids]
        s, used = solve_sde(labels, d+1, p, rng, solver)
        stats[f"solver_{used}_d{d+1}"] += 1
        out = eng.merge([k[1] for k in kids], s)
        if d == 1:
            return None, out
        probs, states = law_of(out, out.key())
        lam = sample(probs)
        return lam, states[lam]

    samples = []
    for _ in range(cfg.m+extra_samples):
        if c == 1:
            stats["top_sources"] += 1
            st = top
        else:
            _, st = make(1)
        probs = eng.readout(st)
        samples.append(sample(probs))
    got = rref(nullspace(samples, cfg.m, p), p)
    return got, {"oracle_queries": len(cfg.points)*stats["top_sources"], **dict(stats),
                 "recovered": got == rref(inst.log_h, p)}


# ====================================================================== agreement with the dense mode

def compare_with_dense(cfg, inst, dense=None, sparse=None, *, merge_cases=200, seed=0, chunk=None):
    """State-by-state exact comparison of the sparse and dense modes on one subgroup:
    source (state and every info flag), every label law and every conditioned branch
    at every grade, merge outputs on up to merge_cases (tuple, witness) cases per grade
    (rho_(H_d) branches, structured and random tuples, all their witnesses up to the
    cap), and the readout. Returns a dict of booleans and counts."""
    eng_d = dense or Engine(cfg)
    eng_s = sparse or SparseEngine(cfg, **({} if chunk is None else {"chunk": chunk}))
    rng = random.Random(seed)
    p, c = cfg.p, cfg.c
    std, Sd, infod = eng_d.source(inst)
    sts, Ss, infos = eng_s.source(inst)
    infos_cmp = {k: v for k, v in infos.items() if k in infod}
    out = {"instance": inst.name, "source_state_equal": sts.equals_dense(std),
           "source_info_equal": infos_cmp == infod, "source_S_equal": bool(np.array_equal(np.sort(Sd), Ss)),
           "grades": {}}
    for d in range(c, 1, -1):
        pd, bd = eng_d.label_law(std)
        ps, bs = eng_s.label_law(sts)
        g = {"label_laws_equal": pd == ps and list(pd) == list(ps),
             "branches_equal": set(bd) == set(bs) and all(bs[k].equals_dense(bd[k]) for k in bd),
             "branches": len(bd)}
        allowed = allowed_labels(cfg, inst.log_h, d)
        M = cfg.arity[d]
        zero = tuple([0]*cfg.dims[d-1])
        tuples = [tuple([zero]*M), tuple([allowed[-1]]*M)]+[tuple(rng.choice(allowed) for _ in range(M))
                                                              for _ in range(4)]
        cases = equal = 0
        last = None
        per = max(1, merge_cases//len(tuples))
        for labels in tuples:
            wits = all_witnesses(labels, d, p)
            if len(wits) > per:
                wits = wits[sorted(rng.sample(range(len(wits)), per))]
            for s in wits:
                act_d = [bd[lam] for lam, si in zip(labels, s) if si]
                act_s = [bs[lam] for lam, si in zip(labels, s) if si]
                wit = [int(x) for x in s if x]
                od, os_ = eng_d.merge(act_d, wit), eng_s.merge(act_s, wit)
                cases += 1
                equal += os_.equals_dense(od)
                last = (od, os_)
        g.update(merge_cases=cases, merge_outputs_equal=equal == cases and cases > 0)
        out["grades"][d] = g
        std, sts = last
    rd, rs = eng_d.readout(std), eng_s.readout(sts)
    out["readout_equal"] = rd == rs and list(rd) == list(rs)
    out["all_equal"] = bool(out["source_state_equal"] and out["source_info_equal"] and out["source_S_equal"]
                            and out["readout_equal"] and all(v["label_laws_equal"] and v["branches_equal"]
                                                             and v["merge_outputs_equal"]
                                                             for v in out["grades"].values()))
    return out


# ====================================================================== class-four instances

def _u(n, *ones):
    v = [0]*n
    for i in ones:
        v[i] += 1
    return tuple(v)


N5_SUBGROUPS = [("trivial", ()), ("<e1> non-normal", (_u(5, 0),)), ("<e2> non-normal", (_u(5, 1),)),
                ("<e3> non-normal", (_u(5, 2),)), ("Z(G) = <e5>", (_u(5, 4),)),
                ("<e2,e5> non-normal", (_u(5, 1), _u(5, 4))), ("<e1+e2+e5> non-normal", (_u(5, 0, 1, 4),)),
                ("<e4,e5> = gamma_3", (_u(5, 3), _u(5, 4))), ("<e3,e4,e5> = gamma_2", (_u(5, 2), _u(5, 3), _u(5, 4)))]


def n5_instances(p=5, names=None):
    alg = filiform5(p)
    return [Hidden(f"{alg.name} H={n}", alg, g) for n, g in N5_SUBGROUPS if names is None or n in names]


def merge_gate_checks(cfg, rows=8, xs=1 << 14, seed=0):
    """prove_merge for every d and s, plus a bit-level run of the whole merge gate list
    on `rows` q values x `xs` random x values (sampled; a full x sweep at class four
    would be |G_4| inputs per q row)."""
    out = {}
    rs = np.random.default_rng(seed)
    for d in range(2, cfg.c+1):
        nQ, nX = cfg.p**cfg.width[d-1], cfg.laws[d].order
        for s in range(1, cfg.p):
            flags = prove_merge(cfg, d, s)
            qi = np.unique(rs.integers(nQ, size=rows))
            xi = np.unique(rs.integers(nX, size=min(xs, nX)))
            _, bit = merge_bitlevel(cfg, d, s, q_indices=qi, x_indices=xi)
            out[f"d{d}_s{s}"] = {"proof": flags, "bitlevel_sampled": bit}
    return out


# ====================================================================== report

def comparable_row(row):
    """A check_instance row without timings and sparse-only fields (for dense/sparse equality)."""
    r = {k: v for k, v in row.items() if k not in ("seconds", "source_seconds", "group_order_top")}
    r["source"] = {k: v for k, v in r["source"].items() if k not in ("coset_generators", "chunks")}
    r["grades"] = {d: {k: v for k, v in g.items()
                       if k not in ("state_support", "branch_support_max", "group_order", "target_support")}
                   for d, g in r["grades"].items()}
    return r


def report_class_four(names=None, *, out_path=None, seeds=(20261103,), check_kw=None, log=print, chunk=1 << 20,
                      gate_checks=True):
    """n5(F_5), class four: merge proofs, instrument, then per subgroup the sparse check
    and seeded runs. Writes the JSON after every subgroup (incremental)."""
    t0 = time.time()
    cfg = Config(filiform5(5))
    res = {**SPARSE_STATUS, "config": cfg.name(), "group_orders": {d: int(cfg.laws[d].order) for d in cfg.laws},
           "checks": [], "seeded_runs": []}

    def dump():
        res["seconds"] = round(time.time()-t0, 1)
        if out_path:
            with open(out_path, "w") as fh:
                fh.write(json.dumps(res, indent=1, default=str)+"\n")

    res["merge_gate_checks"] = merge_gate_checks(cfg) if gate_checks else {}
    res["all_merges_proved"] = all(v["proof"]["proved"] for v in res["merge_gate_checks"].values())
    res["all_bitlevel_ok"] = all(all(x for k, x in v["bitlevel_sampled"].items() if k != "inputs")
                                 for v in res["merge_gate_checks"].values())
    log("merges proved", res["all_merges_proved"], "bitlevel", res["all_bitlevel_ok"], round(time.time()-t0, 1), "s")
    eng = SparseEngine(cfg, chunk=chunk)
    res["instrument"] = {d: eng.kernels[d][1] for d in eng.kernels}
    dump()
    kw = dict(max_cases=3000, sample_tuples=6, max_witnesses=60) if check_kw is None else check_kw
    for inst in n5_instances(5, names):
        ts = time.time()
        src = eng.source(inst)                    # from the source gate list, once per subgroup
        ts = round(time.time()-ts, 1)
        row = check_instance_sparse(cfg, inst, eng, log=log, source=src, **kw)
        row["source_seconds"] = ts
        res["checks"].append(row)
        log(inst.name, "OK" if row["passed"] else "FAIL", row["seconds"], "s")
        dump()
        for seed in seeds:
            got, info = run_algorithm_sparse(cfg, inst, eng, seed=seed, extra_samples=2, top=src[0])
            res["seeded_runs"].append({"instance": inst.name, "normal": inst.normal, "seed": seed, **info})
            log(inst.name, "seed", seed, info, round(time.time()-t0, 1), "s")
        dump()
    res["all_checks_pass"] = all(r["passed"] for r in res["checks"])
    res["all_runs_recover"] = all(r["recovered"] for r in res["seeded_runs"])
    dump()
    return res


def report_agreement(jobs=("heis_f3", "n4_f5"), *, merge_cases=200, log=print, chunk=None):
    out = {}
    for key in jobs:
        if key == "heis_f3":
            cfg, insts = Config(heisenberg(3)), heis3_instances()
        elif key == "n4_f5":
            cfg, insts = Config(filiform4(5)), n4_instances(5)
        else:
            raise ValueError(key)
        dense, sparse = Engine(cfg), SparseEngine(cfg, **({} if chunk is None else {"chunk": chunk}))
        kw = {} if key == "heis_f3" else dict(max_cases=4000, sample_tuples=6)
        rows = []
        for inst in insts:
            r = compare_with_dense(cfg, inst, dense, sparse, merge_cases=merge_cases)
            rs = check_instance_sparse(cfg, inst, sparse, **kw)
            r["check_rows_identical"] = comparable_row(check_instance(cfg, inst, dense, **kw)) == comparable_row(rs)
            r["sparse_check_passed"] = rs["passed"]
            r["sparse_cases"] = {d: g["cases"] for d, g in rs["grades"].items()}
            r["seeded_runs_identical"] = all(run_algorithm(cfg, inst, dense, seed=sd) ==
                                             run_algorithm_sparse(cfg, inst, sparse, seed=sd)
                                             for sd in (20261103, 20261104))
            r["all_equal"] = bool(r["all_equal"] and r["check_rows_identical"] and r["sparse_check_passed"]
                                  and r["seeded_runs_identical"])
            rows.append(r)
            log(key, inst.name, r["all_equal"], r["sparse_cases"])
        out[key] = {"rows": rows, "all_equal": all(r["all_equal"] for r in rows)}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--job", choices=["agree", "n5"], required=True)
    ap.add_argument("--names", help="semicolon list of N5_SUBGROUPS names (default all)")
    ap.add_argument("--out", help="write JSON here")
    ap.add_argument("--chunk", type=int, default=1 << 20)
    ap.add_argument("--max-cases", type=int, default=3000)
    ap.add_argument("--max-witnesses", type=int, default=60)
    ap.add_argument("--no-runs", action="store_true", help="skip seeded runs")
    ap.add_argument("--no-gate-checks", action="store_true", help="skip merge proofs / bit-level runs")
    ap.add_argument("--instrument", choices=["exact", "float"], default="exact",
                    help="instrument exponent derivation (rees_circuit_general.INSTRUMENT_EXPONENTS)")
    args = ap.parse_args()
    import theorems.rees_circuit_general as _G
    _G.INSTRUMENT_EXPONENTS = args.instrument
    lg = lambda *a: print(*a, flush=True)
    if args.job == "agree":
        res = report_agreement(log=lg, chunk=args.chunk if args.chunk != 1 << 20 else None)
        if args.out:
            with open(args.out, "w") as fh:
                fh.write(json.dumps(res, indent=1, default=str)+"\n")
        print({k: v["all_equal"] for k, v in res.items()})
    else:
        names = args.names.split(";") if args.names else None
        res = report_class_four(names, out_path=args.out, log=lg, chunk=args.chunk,
                                check_kw=dict(max_cases=args.max_cases, sample_tuples=6,
                                              max_witnesses=args.max_witnesses),
                                seeds=() if args.no_runs else (20261103,), gate_checks=not args.no_gate_checks)
        print({k: res[k] for k in ("all_merges_proved", "all_bitlevel_ok", "all_checks_pass", "all_runs_recover")})


if __name__ == "__main__":
    main()

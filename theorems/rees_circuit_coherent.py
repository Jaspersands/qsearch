"""Coherent-label receiver backend for the gate-level Rees circuit generator.

AI-checked, pending human review. Report:
research/audits/reviews/2026-11-04-rees-circuit-coherent.md.

Scope: instances whose SDE grades all have kappa_d = gcd(d, p-1) in {1, 2}:
Heis(F_3) (class 2) and n4(F_5) (class 3, p = 5 = 2 mod 3). No existing file
is edited; rees_circuit_general, rees_circuit_arith, rees_coherent_sde and
rees_coherent_sde_k2 are imported read-only.

Against the measured-label generator (rees_circuit_general.terminal_sample_
circuit) nothing is measured before the final Fourier readout:
* the central instrument's label register z is kept coherent and becomes a
  label column of the parent's merge block;
* MergeBlock(cfg, d) is one permutation gate list on (labels, children, Q,
  workspace): U_SDE (the kappa = 1 circuit of rees_coherent_sde or the
  kappa = 2 circuit of rees_coherent_sde_k2, inputs mapped onto the label
  registers) writes the canonical witness s(lambda) into S; for every child
  i the register G = -delta_(s_i)(sigma(q)) is computed (powers of s_i, one
  product per coordinate), the four-pass BCH right translation x_i <- x_i * G
  of rees_circuit_general.merge_ops is run with G as a REGISTER (the merge
  controlled on the witness register), and G is uncomputed; then U_SDE^-1
  clears S and the SDE workspace (the merge only reads S and the labels);
* the merge workspace (G, powers, W, bracket registers) lives on SDE
  workspace wires, which are 0 between U_SDE and U_SDE^-1;
* garbage, never touched again: label registers, merged children, oracle
  outputs (as in the measured generator).

Arity: (g_2+1)(g_2+2)/2 at kappa = 2: Heis(F_3) 3 (unchanged), n4(F_5) 6
instead of the generator's Chevalley-Warning 5; kappa = 1 grades g_d+1.

Checks (all exact): block_check (bit-sliced, all wires of a merge block, on
any set of basis inputs: output x_i * G_i, labels/Q unchanged, S and every
workspace wire 0), prove_controlled_merge (symbolic replay over F_p[s, q, x]
of the controlled merge, against the classical BCH polynomial),
heis_end_to_end (every module of the Heis(F_3) coherent terminal sample --
the generator's source gate list, the instrument macro, the merge block gate
list -- simulated exactly and composed in a factorised Z[zeta_3] form: sum
over label tuples of tensor products; reduced state on Q and readout law
compared with the measured generator), assembled_basis_paths (the assembled
program of one terminal sample run bit-level on random basis paths, against
an independent classical recursion: checks its wiring), n4_state_checks (the generator's exact Engine with
witnesses produced by the coherent SDE gate lists, per merge).

What this does NOT do: kappa_d >= 3 grades (they stay classical), general
instances, QFT_p synthesis (QFT_p calls are counted, not expanded), the
oracle cost, noise, layout, a monolithic 2^n statevector. It flips no claim
gate: coherent_receiver_implemented stays False in
research/reductions/rees_hsp_reduction.json.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import nullcontext
from fractions import Fraction
from itertools import product
import json
from math import gcd, prod
import random
import time

import numpy as np

import theorems.rees_circuit_general as G
from theorems.rees_circuit_arith import (Anc, CountingArithBuilder, add_product_ops, add_scaled_ops, anc_size,
                                         arith_backend, arith_gate_counts)
from theorems.rees_coherent_sde import BitSim, CoherentSDE, Macro, Prog, canonical_witness_batch, macro_gate_types
from theorems.rees_coherent_sde_k2 import CoherentSDEK2, canonical_witness_k2_batch, columns
from theorems.rees_end_to_end_sim import filiform4, heisenberg, nullspace, rref, span_elements

STATUS = {"status": "coherent_label_receiver_backend_small_instances_finite_checks",
          "scope": "Heis(F_3) and n4(F_5) only: every SDE grade has kappa_d in {1, 2}",
          "coherent_receiver_implemented": False,
          "coherent_label_backend_kappa_le2_instances": True,
          "kappa_ge3_grades_coherent": False, "general_instances": False,
          "qft_synthesised": False, "independent_review": False, "speedup_claim_allowed": False,
          "review": "AI-checked, pending human review"}


# ====================================================================== configs

def kappa(p, d):
    return gcd(d, p-1)


def coherent_arity(p, g, d):
    """Columns of the coherent SDE circuit at grade d (label dimension g)."""
    k = kappa(p, d)
    if k == 1:
        return g+1
    if k == 2:
        return columns(g)
    raise ValueError(f"kappa_{d} = {k} >= 3: no coherent SDE circuit (grade stays classical)")


def coherent_config(alg):
    """Config with the coherent arities at every grade (refuses kappa >= 3)."""
    cfg0 = G.Config(alg)
    ar = {d: coherent_arity(cfg0.p, cfg0.dims[d-1], d) for d in range(2, cfg0.c+1)}
    return G.Config(alg, arities=ar)


def job_config(job):
    if job == "heis_f3":
        return coherent_config(heisenberg(3))
    if job == "n4_f5":
        return coherent_config(filiform4(5))
    raise ValueError(job)


def sde_circuit(p, g, d):
    k = kappa(p, d)
    if k == 1:
        return CoherentSDE(p, g, d)
    if k == 2:
        return CoherentSDEK2(p, g, d)
    raise ValueError(f"kappa_{d} = {k} >= 3")


def sde_reference(p, d, A):
    """Canonical witness of the coherent SDE circuit (independent references); A (N, g, M)."""
    if kappa(p, d) == 1:
        return canonical_witness_batch(p, A, d)
    return canonical_witness_k2_batch(p, A, d)[0]


# ====================================================================== program helpers

def remap(prog, wmap):
    """Prog with every wire w replaced by wmap[w] (gate tuples and macro args)."""
    out = Prog()
    for it in prog:
        if isinstance(it, Macro):
            out.append(Macro(it.kind, it.coeff, tuple(tuple(wmap[w] for w in r) for r in it.args), it.inv))
        else:
            name, qs = it
            if name == "swapreg":
                out.append((name, tuple(tuple(wmap[w] for w in r) for r in qs)))
            elif name in ("qft", "qft_dg", "oracle", "measure"):
                out.append((name, tuple(tuple(wmap[w] for w in r) for r in qs)))
            else:
                out.append((name, tuple(wmap[w] for w in qs)))
    return out


def flatten(prog, p, anc):
    """X/CX/CCX/SWAP gate list; macros expanded with the rees_circuit_arith gate
    lists on the ancilla layout anc (inverse macro = reversed list), swapreg as
    qubit SWAPs. Refuses qft/oracle items (not permutations of this simulator)."""
    cache, out = {}, []
    for it in prog:
        if isinstance(it, Macro):
            key = (it.kind, it.coeff, it.args)
            ops = cache.get(key)
            if ops is None:
                fn = add_product_ops if it.kind == "add_product" else add_scaled_ops
                ops = fn(p, *[list(r) for r in it.args], it.coeff, anc)
                cache[key] = ops
            out.extend(reversed(ops) if it.inv else ops)
        elif it[0] == "swapreg":
            for a, b in zip(*it[1]):
                out.append(("swap", (a, b)))
        elif it[0] in ("x", "cx", "ccx", "swap"):
            out.append(it)
        else:
            raise ValueError(f"not a permutation item: {it[0]}")
    return out


def prog_counts(prog, p):
    """Exact gate counts by type: macros by the per-(kind, coeff) counts of one
    emitted rees_circuit_arith instance; swapreg as SWAPs; qft/oracle as calls."""
    tot, mc = Counter(), Counter()
    for it in prog:
        if isinstance(it, Macro):
            mc[(it.kind, it.coeff)] += 1
        elif it[0] == "swapreg":
            tot["swap"] += len(it[1][0])
        elif it[0] in ("qft", "qft_dg"):
            tot["qft_calls"] += 1
        elif it[0] == "oracle":
            tot["oracle_calls"] += 1
        elif it[0] == "measure":
            tot["measured_qudits"] += len(it[1])
        else:
            tot[it[0]] += 1
    for (kind, coeff), n in mc.items():
        for k, v in macro_gate_types(p, kind, coeff).items():
            tot[k] += n*v
        tot[kind] += n
    tot["gates"] = sum(tot[k] for k in ("x", "cx", "ccx", "swap"))
    return dict(tot)


def targets(it):
    """Wires written by a program item."""
    if isinstance(it, Macro):
        return set(it.args[0])
    name, qs = it
    if name == "swapreg":
        return set(qs[0]) | set(qs[1])
    if name in ("qft", "qft_dg"):
        return {w for r in qs for w in r}
    if name == "oracle":
        return set(qs[1])
    if name == "measure":
        return set()
    if name == "swap":
        return set(qs)
    return {qs[-1]}


def touched(it):
    if isinstance(it, Macro):
        return {w for r in it.args for w in r}
    name, qs = it
    if name in ("swapreg", "qft", "qft_dg", "oracle", "measure"):
        return {w for r in qs for w in r}
    return set(qs)


# ====================================================================== the merge block

class MergeBlock:
    """One coherent merge at grade d: a permutation program on
    lam[i][r] (label i, row r), x[i][j] (child i, coordinate j), Q[j], with
    the witness register S and all workspace returned to 0.

    prog = U_SDE + sum_i (ctrl_i + bch_i + ctrl_i^-1) + U_SDE^-1; segments are
    kept separately for counting. mutate: test hook ('g_sign', 'skip_ctrl_inv',
    'skip_sde_inv', 'skip_bennett')."""

    def __init__(self, cfg, d, mutate=None):
        self.cfg, self.d, self.p = cfg, d, cfg.p
        self.mutate = set(mutate or ())
        p, b = cfg.p, cfg.enc.nb
        self.b = b
        self.g = g = cfg.dims[d-1]
        self.sde = sde = sde_circuit(p, g, d)
        self.M = M = len(sde.L)
        if cfg.arity[d] != M:
            raise ValueError(f"config arity M_{d} = {cfg.arity[d]} but the coherent SDE has {M} columns")
        self.nq, self.nx = cfg.width[d-1], cfg.width[d]
        self.nw = 0
        fresh = self._fresh
        self.lam = [[fresh(b) for _ in range(g)] for _ in range(M)]
        self.x = [[fresh(b) for _ in range(self.nx)] for _ in range(M)]
        self.Q = [fresh(b) for _ in range(self.nq)]
        self.S = [fresh(b) for _ in range(M)]
        self.anc = Anc(fresh(anc_size(b)), b)
        # SDE wire map: L -> lam, S -> S, anc -> anc, the rest -> block workspace
        wmap = {}
        for c in range(M):
            for r in range(g):
                wmap.update(zip(sde.L[c][r], self.lam[c][r]))
            wmap.update(zip(sde.S[c], self.S[c]))
        wmap.update(zip(sde.anc.all, self.anc.all))
        rest = [w for w in range(sde.nw) if w not in wmap]
        self.sde_work = fresh(len(rest))
        wmap.update(zip(rest, self.sde_work))
        self.U = remap(sde.prog, wmap)
        # merge workspace on SDE workspace wires (0 between U and U^-1)
        pool = list(self.sde_work)

        def reg():
            nonlocal pool
            if len(pool) >= b:
                r, pool = pool[:b], pool[b:]
                return r
            return fresh(b)
        self.G = [reg() for _ in range(self.nq)]
        self.degs = [cfg.grades[j] for j in range(self.nq)]
        self.pw = {k: reg() for k in range(2, max(self.degs)+1)}
        self.W = [reg() for _ in range(self.nx)]
        self.bws = {w: {k: reg() for k in supp} for w, _, supp in cfg.nodes[d]}
        self.ctrl, self.bch = [], []
        for i in range(M):
            self.ctrl.append(self._ctrl_prog(self.S[i]))
            self.bch.append(self._bch_prog(self.x[i]))
        P = Prog(self.U)
        for i in range(M):
            P += self.ctrl[i]
            P += self.bch[i]
            if "skip_ctrl_inv" not in self.mutate:
                P += self.ctrl[i].inverse()
        if "skip_sde_inv" not in self.mutate:
            P += self.U.inverse()
        self.prog = P
        self.io = {w for r in self.lam for q in r for w in q} | {w for r in self.x for q in r for w in q} | \
            {w for q in self.Q for w in q}

    def _fresh(self, n):
        out = list(range(self.nw, self.nw+n))
        self.nw += n
        return out

    # -- G = -delta_s(sigma(q)): G_j = -s^deg(j) q_j
    def _ctrl_prog(self, s):
        P = Prog()
        prev = s
        for k in sorted(self.pw):
            P.append(Macro("add_product", 1, (tuple(self.pw[k]), tuple(prev), tuple(s))))
            prev = self.pw[k]
        sign = 1 if "g_sign" in self.mutate else -1
        for j in range(self.nq):
            src = s if self.degs[j] == 1 else self.pw[self.degs[j]]
            P.append(Macro("add_product", sign % self.p, (tuple(self.G[j]), tuple(src), tuple(self.Q[j]))))
        return P

    # -- four-pass BCH right translation x <- x * G (merge_ops with G a register)
    def _bch_prog(self, x):
        cfg, d, p = self.cfg, self.d, self.p
        T = cfg.laws[d].tensor
        nodes, nq, nx = cfg.nodes[d], self.nq, self.nx
        Gr, W, bws = self.G, self.W, self.bws
        P = Prog()

        def prod_(t, a, b, c):
            if c % p:
                P.append(Macro("add_product", c % p, (tuple(t), tuple(a), tuple(b))))

        def scal(t, a, c):
            if c % p:
                P.append(Macro("add_scaled", c % p, (tuple(t), tuple(a))))

        def bracket_pass(u, sign_g, sign):
            order = nodes if sign > 0 else list(reversed(nodes))
            for w, _, supp in order:
                out = bws[w]
                for k in supp:
                    if w == "xy":
                        for i in range(nx):
                            for j in range(nq):
                                if T[i, j, k]:
                                    prod_(out[k], u[i], Gr[j], sign*int(T[i, j, k])*sign_g)
                    else:
                        child = bws[w[1:]]
                        for i in range(nx):
                            for j in child:
                                if not T[i, j, k]:
                                    continue
                                if w[0] == "x":
                                    prod_(out[k], u[i], child[j], sign*int(T[i, j, k]))
                                elif i < nq:
                                    prod_(out[k], Gr[i], child[j], sign*int(T[i, j, k])*sign_g)

        def bch_linear(u, sign_g, sign):
            for j in range(nx):
                scal(W[j], u[j], sign)
            for j in range(nq):
                scal(W[j], Gr[j], sign*sign_g)
            for w, alpha, supp in nodes:
                if alpha:
                    for k in supp:
                        scal(W[k], bws[w][k], sign*alpha)

        bracket_pass(x, 1, 1)
        bch_linear(x, 1, 1)
        if "skip_bennett" not in self.mutate:
            bracket_pass(x, 1, -1)
        P.append(("swapreg", (tuple(w for q in x for w in q), tuple(w for q in W for w in q))))
        bracket_pass(x, -1, 1)
        bch_linear(x, -1, -1)
        bracket_pass(x, -1, -1)
        return P

    # -- gate list and counts
    def flatten(self):
        return flatten(self.prog, self.p, self.anc)

    def segment_counts(self):
        p = self.p
        ctrl = Prog(it for c in self.ctrl for it in c)
        ctrl_all = Prog(ctrl+ctrl.inverse())
        bch = Prog(it for c in self.bch for it in c)
        return {"sde_U_and_Uinv": prog_counts(Prog(self.U+self.U.inverse()), p),
                "witness_control_G": prog_counts(ctrl_all, p),
                "bch_merge": prog_counts(bch, p),
                "block_total": prog_counts(self.prog, p)}

    def qubits(self):
        """Wires by role."""
        b = self.b
        merge_work = {w for r in [*self.G, *self.pw.values(), *self.W] for w in r} | \
            {w for bw in self.bws.values() for r in bw.values() for w in r}
        return {"labels": self.M*self.g*b, "children": self.M*self.nx*b, "Q": self.nq*b, "witness_S": self.M*b,
                "arith_ancilla": anc_size(b), "sde_workspace": len(self.sde_work),
                "merge_workspace_on_sde_wires": len(merge_work & set(self.sde_work)),
                "merge_workspace_extra": len(merge_work-set(self.sde_work)),
                "total": self.nw, "workspace_total": self.nw-len(self.io)}


# ====================================================================== block checks (bit level)

def _witness_bound_g(block, s, qv):
    """G_i rows: -s^deg q (padded with zero top grade), (N, nx)."""
    p = block.p
    pw = np.stack([np.array([pow(v, e, p) for v in range(p)], dtype=np.int64)[s] for e in block.degs], axis=1)
    gi = (-pw*qv) % p
    return np.concatenate([gi, np.zeros((len(qv), block.nx-block.nq), dtype=np.int64)], axis=1)


def block_check(block, lam, xs, qv, gates=None, chunk=1 << 18):
    """Run the block gate list on basis inputs lam (N, M, g), xs (N, M, nx),
    qv (N, nq) with all other wires 0. Checks: labels and Q unchanged, x_i =
    x_i * (-delta_(s_i)(sigma(q))) with s the canonical witness (independent
    reference), witness S and every workspace wire 0, outputs canonical."""
    cfg, p, M = block.cfg, block.p, block.M
    gates = block.flatten() if gates is None else gates
    law = cfg.laws[block.d]
    N = len(qv)
    flags = {"inputs": int(N), "gates": len(gates), "qubits": block.nw, "labels_unchanged": True,
             "q_unchanged": True, "x_equals_bch_with_coherent_witness": True, "witness_and_workspace_clean": True,
             "outputs_canonical": True}
    t0 = time.time()
    for a in range(0, N, chunk):
        sl = slice(a, min(N, a+chunk))
        n = sl.stop-sl.start
        sim = BitSim(block.nw, n)
        for i in range(M):
            for r in range(block.g):
                sim.load(block.lam[i][r], lam[sl, i, r])
            for j in range(block.nx):
                sim.load(block.x[i][j], xs[sl, i, j])
        for j in range(block.nq):
            sim.load(block.Q[j], qv[sl, j])
        sim.run(gates)
        A = np.transpose(lam[sl], (0, 2, 1))                   # (n, g, M) columns = labels
        s = sde_reference(p, block.d, A)
        flags["labels_unchanged"] &= all(np.array_equal(sim.read(block.lam[i][r]), lam[sl, i, r])
                                         for i in range(M) for r in range(block.g))
        flags["q_unchanged"] &= all(np.array_equal(sim.read(block.Q[j]), qv[sl, j]) for j in range(block.nq))
        for i in range(M):
            out = np.stack([sim.read(block.x[i][j]) for j in range(block.nx)], axis=1)
            flags["outputs_canonical"] &= bool((out < p).all())
            ref = law.mul(xs[sl, i], _witness_bound_g(block, s[:, i], qv[sl]))
            flags["x_equals_bch_with_coherent_witness"] &= bool(np.array_equal(out, ref))
        flags["witness_and_workspace_clean"] &= not any(sim.wire_nonzero(w) for w in range(block.nw)
                                                        if w not in block.io)
        del sim
    flags["sim_seconds"] = round(time.time()-t0, 2)
    flags["passed"] = all(v for k, v in flags.items() if isinstance(v, bool))
    return flags


def mixed_radix(idx, radices):
    out, r = [], idx
    for m in reversed(radices):
        out.append(r % m)
        r //= m
    return out[::-1]


def block_inputs_from_index(block, idx):
    """Decode a flat input index into (lam, xs, qv): radix p on every coordinate,
    order lam (M g), x (M nx), q (nq)."""
    p, M, g, nx, nq = block.p, block.M, block.g, block.nx, block.nq
    n = M*g+M*nx+nq
    digits = np.zeros((len(idx), n), dtype=np.int64)
    r = np.asarray(idx, dtype=np.int64).copy()
    for t in range(n-1, -1, -1):
        digits[:, t] = r % p
        r //= p
    lam = digits[:, :M*g].reshape(-1, M, g)
    xs = digits[:, M*g:M*g+M*nx].reshape(-1, M, nx)
    qv = digits[:, M*g+M*nx:]
    return lam, xs, qv


def block_input_count(block):
    return block.p**(block.M*block.g+block.M*block.nx+block.nq)


def block_exhaustive(block, chunk=1 << 21, log=None, start=0, stop=None):
    """block_check on ALL canonical inputs (index range [start, stop))."""
    gates = block.flatten()
    total = block_input_count(block)
    stop = total if stop is None else min(stop, total)
    agg = None
    t0 = time.time()
    for a in range(start, stop, chunk):
        lam, xs, qv = block_inputs_from_index(block, np.arange(a, min(stop, a+chunk), dtype=np.int64))
        f = block_check(block, lam, xs, qv, gates=gates, chunk=chunk)
        if agg is None:
            agg = dict(f)
        else:
            for k, v in f.items():
                if isinstance(v, bool):
                    agg[k] = agg[k] and v
            agg["inputs"] += f["inputs"]
        if log:
            log(f"  block d={block.d} inputs {min(stop, a+chunk)}/{stop} ok={agg['passed'] and f['passed']} "
                f"{time.time()-t0:.0f}s")
    agg["passed"] = all(v for k, v in agg.items() if isinstance(v, bool))
    agg["sim_seconds"] = round(time.time()-t0, 1)
    agg["index_range"] = [start, stop]
    return agg


def structured_label_tuples(cfg, d, n, rng, allowed=None):
    """Label tuples biased to rank deficiency (zero, repeated, combinations),
    optionally drawn from an allowed label set."""
    p, g, M = cfg.p, cfg.dims[d-1], cfg.arity[d]
    out = np.zeros((n, M, g), dtype=np.int64)
    for t in range(n):
        for i in range(M):
            mode = rng.randrange(4)
            if allowed is not None:
                out[t, i] = allowed[rng.randrange(len(allowed))] if mode else 0
            elif mode == 0:
                out[t, i] = 0
            elif mode == 1 or i == 0:
                out[t, i] = [rng.randrange(p) for _ in range(g)]
            else:
                c = [rng.randrange(p) for _ in range(i)]
                out[t, i] = (np.array(c) @ out[t, :i]) % p
    return out


def block_sampled(block, n=4096, seed=0, gates=None):
    rng = random.Random(seed)
    cfg, p = block.cfg, block.p
    lam = structured_label_tuples(cfg, block.d, n, rng)
    nrng = np.random.default_rng(seed)
    xs = nrng.integers(0, p, size=(n, block.M, block.nx))
    qv = nrng.integers(0, p, size=(n, block.nq))
    return block_check(block, lam, xs, qv, gates=gates)


# ====================================================================== compositional proof pieces

def sde_exhaustive(block):
    """U_SDE alone (remapped) on ALL canonical label tuples: S = canonical
    witness, labels restored, workspace 0 (the measured-free solve)."""
    p, M, g = block.p, block.M, block.g
    N = p**(M*g)
    idx = np.arange(N, dtype=np.int64)
    lam = np.zeros((N, M, g), dtype=np.int64)
    r = idx.copy()
    for i in range(M):
        for k in range(g):
            lam[:, i, k] = r % p
            r //= p
    gates = flatten(block.U, p, block.anc)
    sim = BitSim(block.nw, N)
    for i in range(M):
        for k in range(g):
            sim.load(block.lam[i][k], lam[:, i, k])
    sim.run(gates)
    s = np.stack([sim.read(block.S[i]) for i in range(M)], axis=1)
    ref = sde_reference(p, block.d, np.transpose(lam, (0, 2, 1)))
    sd = np.array([pow(t, block.d, p) for t in range(p)])[np.minimum(s, p-1)]
    io = {w for r in block.lam for q in r for w in q} | {w for q in block.S for w in q}
    return {"inputs": int(N), "gates": len(gates), "witness_equals_canonical": bool(np.array_equal(s, ref)),
            "witness_nonzero": bool(s.any(axis=1).all()),
            "equation_holds": bool((np.einsum("nig,ni->ng", lam, sd) % p == 0).all()),
            "labels_restored": all(np.array_equal(sim.read(block.lam[i][k]), lam[:, i, k])
                                   for i in range(M) for k in range(g)),
            "workspace_clean": not any(sim.wire_nonzero(w) for w in range(block.nw) if w not in io)}


def prove_controlled_merge(block):
    """Symbolic replay of ctrl_i + bch_i + ctrl_i^-1 for child 0 over
    F_p[s, q, x] (macros as their declared maps; the macro gate lists are the
    rees_circuit_arith ones): x must become the classical BCH polynomial of
    x * (-delta_s(sigma(q))) (rees_circuit_general.sym_bch_reference, written
    independently of the node derivation), G, powers, W and bracket registers
    must be 0, s and q unchanged. Proves the controlled merge on ALL canonical
    (s, q, x)."""
    cfg, p, d = block.cfg, block.p, block.d
    Poly = G.Poly
    nq, nx = block.nq, block.nx
    sv = Poly.var(p, 0)
    qv = [Poly.var(p, 1+j) for j in range(nq)]
    xv = [Poly.var(p, 1+nq+j) for j in range(nx)]
    zero = Poly(p)
    P = {tuple(block.S[0]): sv}
    P.update({tuple(block.Q[j]): qv[j] for j in range(nq)})
    P.update({tuple(block.x[0][j]): xv[j] for j in range(nx)})
    prog = Prog(block.ctrl[0]+block.bch[0]+block.ctrl[0].inverse())
    xreg = [tuple(q) for q in block.x[0]]
    for it in prog:
        if isinstance(it, Macro):
            c = it.coeff if not it.inv else -it.coeff
            if it.kind == "add_product":
                t, a, b = it.args
                P[t] = P.get(t, zero)+(P.get(a, zero)*P.get(b, zero))*c
            else:
                t, a = it.args
                P[t] = P.get(t, zero)+P.get(a, zero)*c
        elif it[0] == "swapreg":
            A, B = it[1]
            b = block.b
            for k in range(0, len(A), b):
                ra, rb = tuple(A[k:k+b]), tuple(B[k:k+b])
                P[ra], P[rb] = P.get(rb, zero), P.get(ra, zero)
        else:
            raise ValueError(it)
    g = [qv[j]*(-1) for j in range(nq)]
    for j in range(nq):
        for _ in range(block.degs[j]):
            g[j] = g[j]*sv
    g += [zero]*(nx-nq)
    ref = G.sym_bch_reference(cfg.laws[d].tensor, d, xv, g, p)
    work = [*block.G, *block.pw.values(), *block.W] + [r for bw in block.bws.values() for r in bw.values()]
    wr = {w for it in prog for w in targets(it)}
    flags = {"macros": sum(isinstance(it, Macro) for it in prog),
             "x_equals_bch_of_minus_delta_s_sigma_q": all(P.get(xreg[j], zero) == ref[j] for j in range(nx)),
             "workspace_zero": all(P.get(tuple(r), zero).is_zero() for r in work),
             "s_and_q_unchanged": P[tuple(block.S[0])] == sv and all(P[tuple(block.Q[j])] == qv[j] for j in range(nq)),
             "never_writes_labels_S_Q": not (wr & ({w for r in block.lam for q in r for w in q} |
                                                   {w for q in block.S for w in q} | {w for q in block.Q for w in q}))}
    flags["proved"] = all(v for k, v in flags.items() if k != "macros")
    return flags


def block_structure(block):
    """Footprints: U_SDE never writes labels; the controlled merge of child i
    writes only x_i and merge workspace, reads S_i, Q; children are disjoint."""
    lamw = {w for r in block.lam for q in r for w in q}
    Sw = {w for q in block.S for w in q}
    Qw = {w for q in block.Q for w in q}
    xw = [{w for q in xi for w in q} for xi in block.x]
    work = {w for r in [*block.G, *block.pw.values(), *block.W] for w in r} | \
        {w for bw in block.bws.values() for r in bw.values() for w in r}
    anc = set(block.anc.all)
    U_w = {w for it in block.U for w in targets(it)}
    ok_child = []
    for i in range(block.M):
        P = Prog(block.ctrl[i]+block.bch[i]+block.ctrl[i].inverse())
        wr = {w for it in P for w in targets(it)}
        rd = {w for it in P for w in touched(it)}
        ok_child.append(wr <= (xw[i] | work) and rd <= (xw[i] | work | set(block.S[i]) | Qw) and
                        not any(rd & xw[j] for j in range(block.M) if j != i))
    return {"sde_never_writes_labels_or_Q_or_children": not (U_w & (lamw | Qw | set().union(*xw))),
            "child_merges_local_footprint": all(ok_child),
            "merge_workspace_wires_outside_sde_workspace": len(work-set(block.sde_work))}


# ====================================================================== the assembled terminal sample

class TerminalSample:
    """The complete coherent terminal sample as one integer-wire program
    (qft/oracle/measure items marked; the oracle is a table call, not
    counted). Depth first, garbage never reused, clean workspace (w, the
    arithmetic ancillas, one block-workspace pool) shared."""

    def __init__(self, cfg):
        self.cfg, self.p = cfg, cfg.p
        p, b, c = cfg.p, cfg.enc.nb, cfg.c
        self.blocks = {d: MergeBlock(cfg, d) for d in range(2, c+1)}
        self.nw = 0
        self.role = {}
        self.anc = Anc(self._fresh(anc_size(b), "arith_ancilla"), b)
        self.w = [self._fresh(b, "evaluation_w") for _ in range(cfg.m)]
        pool_size = max(blk.nw-len(blk.io)-anc_size(b) for blk in self.blocks.values()) if self.blocks else 0
        self.pool = self._fresh(pool_size, "block_workspace_pool")
        self.items = []                       # (component, item)
        self.garbage_after = []               # (item index, wires that must never be touched again)
        self.N = G.sources_per_grade(cfg)
        self.nodes = []
        root = self._emit(1 if c >= 2 else c)
        self.tree = self.nodes[-1]
        for q in root[0]:
            self._add("final_qft", ("qft", (tuple(q),)))
        self._add("final_qft", ("measure", tuple(tuple(q) for q in root[0])))
        self.root = root[0]

    def _fresh(self, n, role):
        out = list(range(self.nw, self.nw+n))
        self.nw += n
        for w in out:
            self.role[w] = role
        return out

    def _add(self, comp, it):
        self.items.append((comp, it))

    def _instrument(self, d, a):
        cfg, b = self.cfg, self.cfg.enc.nb
        z = [self._fresh(b, f"label_z_grade{d}") for _ in range(cfg.dims[d-1])]
        for q in z:
            self._add("instrument_qft", ("qft", (tuple(q),)))
        for j, t in enumerate(cfg.top(d)):
            self._add("instrument", Macro("add_scaled", (-1) % self.p, (tuple(a[t]), tuple(z[j]))))
        for q in z:
            self._add("instrument_qft", ("qft_dg", (tuple(q),)))
        return z

    def _emit(self, d):
        cfg, b, p = self.cfg, self.cfg.enc.nb, self.p
        if d == cfg.c:
            a = [self._fresh(b, "address_top") for _ in range(cfg.width[d])]
            ys = [self._fresh(cfg.label_bits, "oracle_output") for _ in cfg.points]
            for q in a:
                self._add("source_qft", ("qft", (tuple(q),)))
            for s, y in zip(cfg.points, ys):
                E = cfg.cover.evaluation_matrix(s)
                for sign in (1, -1):
                    for i in range(E.shape[0]):
                        for j in range(E.shape[1]):
                            if E[i, j]:
                                self._add("source_evaluation", Macro("add_scaled", sign*int(E[i, j]) % p,
                                                                     (tuple(self.w[j]), tuple(a[i]))))
                    if sign == 1:
                        self._add("oracle", ("oracle", (tuple(w for q in reversed(self.w) for w in q), tuple(y))))
            z = self._instrument(d, a) if d >= 2 else None
            self.nodes.append({"d": d, "reg": a, "z": z, "kids": [], "ys": ys})
            return a, z
        blk = self.blocks[d+1]
        kids = [self._emit(d+1) for _ in range(cfg.arity[d+1])]
        kid_nodes = self.nodes[-cfg.arity[d+1]:]
        del self.nodes[-cfg.arity[d+1]:]
        Q = [self._fresh(b, f"Q_grade{d}") for _ in range(cfg.width[d])]
        for q in Q:
            self._add("q_prep_qft", ("qft", (tuple(q),)))
        wmap = {}
        for i, (a, z) in enumerate(kids):
            for r in range(blk.g):
                wmap.update(zip(blk.lam[i][r], z[r]))
            for j in range(blk.nx):
                wmap.update(zip(blk.x[i][j], a[j]))
        for j in range(blk.nq):
            wmap.update(zip(blk.Q[j], Q[j]))
        wmap.update(zip(blk.anc.all, self.anc.all))
        local_work = [w for w in range(blk.nw) if w not in wmap]
        wmap.update(zip(local_work, self.pool))
        U = remap(blk.U, wmap)
        for it in U:
            self._add(f"sde_grade{d+1}", it)
        for i in range(blk.M):
            ci = remap(blk.ctrl[i], wmap)
            for it in ci:
                self._add(f"witness_control_grade{d+1}", it)
            for it in remap(blk.bch[i], wmap):
                self._add(f"bch_merge_grade{d+1}", it)
            for it in ci.inverse():
                self._add(f"witness_control_grade{d+1}", it)
        for it in U.inverse():
            self._add(f"sde_grade{d+1}", it)
        garbage = {w for a, z in kids for q in [*a, *z] for w in q}
        self.garbage_after.append((len(self.items), garbage))
        z = self._instrument(d, Q) if d >= 2 else None
        self.nodes.append({"d": d, "reg": Q, "z": z, "kids": kid_nodes})
        return Q, z

    # -- counts and structure
    def counts(self):
        by = {}
        comps = sorted({c for c, _ in self.items})
        for comp in comps:
            by[comp] = prog_counts(Prog(it for c, it in self.items if c == comp), self.p)
        tot = prog_counts(Prog(it for _, it in self.items), self.p)
        roles = Counter(self.role.values())
        return {"by_component": by, "total": tot, "qubits": self.nw, "qubits_by_role": dict(roles),
                "sources": self.N, "arities": dict(self.cfg.arity),
                "oracle_calls": tot.get("oracle_calls", 0)}

    def structure(self):
        """(i) garbage (labels, merged children) is never touched after its
        merge block; (ii) only the root is measured, at the end; (iii) no
        item other than qft touches a wire after it is measured."""
        ok_garbage = True
        for pos, wires in self.garbage_after:
            for _, it in self.items[pos:]:
                if touched(it) & wires:
                    ok_garbage = False
                    break
        meas = [i for i, (_, it) in enumerate(self.items) if not isinstance(it, Macro) and it[0] == "measure"]
        last = self.items[-1][1]
        return {"garbage_never_touched_again": ok_garbage,
                "single_measurement_at_end": meas == [len(self.items)-1],
                "measured_register_is_root_Q": last[1] == tuple(tuple(q) for q in self.root)}


def assembled_basis_paths(ts, n=256, seed=0):
    """Wiring check of the ASSEMBLED terminal-sample program: every QFT_p on a
    fresh register is replaced by a random canonical basis load, qft_dg, the
    oracle and the measurement are skipped, and every other item is run
    bit-level on n paths. An independent classical recursion predicts every
    register: a source address a ends at (a z^-1) * g(s_i, q) (instrument,
    then the parent's merge with the canonical witness of the sibling labels
    and the parent's loaded q), a grade-d Q likewise, the root Q is unchanged,
    labels keep their loaded values; w, ancillas, pool and oracle outputs end 0."""
    cfg, p = ts.cfg, ts.p
    rng = np.random.default_rng(seed)
    sim = BitSim(ts.nw, n)
    loaded = {}
    buf = Prog()

    def flush():
        if buf:
            sim.run(flatten(buf, p, ts.anc))
            buf.clear()
    fresh_ok = True
    for comp, it in ts.items:
        if isinstance(it, Macro) or it[0] in ("x", "cx", "ccx", "swap", "swapreg"):
            buf.append(it)
            continue
        flush()
        if it[0] == "qft" and comp != "final_qft":        # the readout QFT is not a preparation
            reg = it[1][0]
            fresh_ok &= not any(sim.wire_nonzero(w) for w in reg)
            v = rng.integers(0, p, size=n)
            sim.load(list(reg), v)
            loaded[reg] = v
    flush()

    def val(reg):
        return np.stack([loaded[tuple(q)] for q in reg], axis=1)

    def read(reg):
        return np.stack([sim.read(list(q)) for q in reg], axis=1)
    ok = {"fresh_registers_zero_before_qft": bool(fresh_ok), "children_and_Q": True, "labels": True}

    def after_instrument(node):
        x = val(node["reg"])
        if node["z"] is None:
            return x
        z = val(node["z"])
        law = cfg.laws[node["d"]]
        zf = np.concatenate([np.zeros((n, cfg.width[node["d"]]-cfg.dims[node["d"]-1]), dtype=np.int64),
                             (-z) % p], axis=1)
        return law.mul(x, zf)

    def visit(node):
        if not node["kids"]:
            return
        d = node["d"]+1
        blk = ts.blocks[d]
        lam = np.stack([val(k["z"]) for k in node["kids"]], axis=2)          # (n, g, M)
        s = sde_reference(p, d, lam)
        qv = val(node["reg"])
        for i, k in enumerate(node["kids"]):
            want = cfg.laws[d].mul(after_instrument(k), _witness_bound_g(blk, s[:, i], qv))
            ok["children_and_Q"] &= bool(np.array_equal(read(k["reg"]), want))
            ok["labels"] &= bool(np.array_equal(read(k["z"]), val(k["z"])))
            visit(k)
    visit(ts.tree)
    ok["root_Q_unchanged"] = bool(np.array_equal(read(ts.tree["reg"]), val(ts.tree["reg"])))
    clean = [w for w in range(ts.nw) if ts.role[w] in ("arith_ancilla", "evaluation_w", "block_workspace_pool",
                                                       "oracle_output")]
    ok["workspace_clean"] = not any(sim.wire_nonzero(w) for w in clean)
    ok["paths"] = n
    ok["passed"] = all(v for k, v in ok.items() if isinstance(v, bool))
    return ok


def measured_counts(alg, arities=None, witness=None):
    """The measured-label generator's terminal sample under the poly(log p)
    arithmetic backend (counting builder): qubits and gate counts, for
    comparison (all merges active: witness all ones by default)."""
    cfg = G.Config(alg, arities=arities)
    with arith_backend(CountingArithBuilder):
        qc, B = G.terminal_sample_circuit(cfg, None, witness)
    c = arith_gate_counts(B)
    return {"qubits": qc.num_qubits, "arith_gates": c.get("arith_total", 0), "swap_macro": c.get("swap_macro", 0),
            "ccx": c.get("ccx", 0), "qft_calls": c.get("qft_unitary", 0) or sum(v for k, v in B.counts.items()
                                                                             if k.startswith("qft")),
            "oracle_calls": B.counts["oracle_calls"], "classical_bits": qc.num_clbits,
            "macros": dict(Counter(m[0] for m in B.macros if m[0] in ("add_product", "add_scaled"))),
            "arities": dict(cfg.arity)}


# ====================================================================== Heis(F_3): exact end-to-end simulation

def _cyc_conj(v):
    """Complex conjugate in Z[zeta_p] (coefficient vector, last axis)."""
    p = v.shape[-1]
    return v[..., (-np.arange(p)) % p]


def _cyc_dot(a, b, p):
    """sum over leading axis of a_k * b_k in Z[zeta_p]; a, b (n, p)."""
    out = np.zeros(p, dtype=np.int64)
    for i in range(p):
        out += np.roll(a[:, i:i+1]*b, i, axis=1).sum(axis=0)
    return out


def source_label_keys(cfg, inst):
    """Bit-level run of the generator's source gate list (poly(log p) backend)
    on ALL canonical addresses: label key per address; address unchanged and
    evaluation workspace clean are checked."""
    with arith_backend():
        qc, B, (a_reg, a, w_reg, w, labels) = G.source_circuit(cfg, inst)
    if [i.operation.name for i in qc.data[:len(a)]] != [f"qft{cfg.p}"]*len(a):
        raise AssertionError("source must start with QFT_p on each address coordinate")
    pos = {q: i for i, q in enumerate(qc.qubits)}
    law = cfg.laws[cfg.c]
    X = law.elements()
    sim = G.BitSim(qc.num_qubits, law.order)
    sim.load(G.wires_of(a, pos), X)
    sim.run(G.compile_ops(qc.data[len(a):], pos))
    ok = bool((sim.read(G.wires_of(a, pos)) == X).all()) and bool((sim.read(G.wires_of(w, pos)) == 0).all())
    anc = [pos[q] for q in qc.qubits if q not in set(a_reg) | set(w_reg) | {qb for y in labels for qb in y}]
    ok = ok and all(not sim.cols[k].any() for k in anc)
    keys = np.zeros(law.order, dtype=np.int64)
    shift = 0
    for y in labels:
        keys |= sim.read_bits([pos[q] for q in y]) << shift
        shift += len(y)
    return keys, ok


def instrument_permutation(cfg, d):
    """Bit-level run of the instrument's permutation part (a_top -= z, the
    add_scaled macro of rees_circuit_arith) on all (x, z): returns the index of
    x' = x z^-1 per (x, z); checks z unchanged and ancillas clean."""
    p, b = cfg.p, cfg.enc.nb
    law = cfg.laws[d]
    n, g = cfg.width[d], cfg.dims[d-1]
    a = [list(range(k*b, (k+1)*b)) for k in range(n)]
    z = [list(range((n+k)*b, (n+k+1)*b)) for k in range(g)]
    anc = Anc(list(range((n+g)*b, (n+g)*b+anc_size(b))), b)
    P = Prog(Macro("add_scaled", (-1) % p, (tuple(a[t]), tuple(z[j]))) for j, t in enumerate(cfg.top(d)))
    gates = flatten(P, p, anc)
    X = law.elements()
    Z = np.array(list(product(range(p), repeat=g)), dtype=np.int64).reshape(-1, g)
    XX, ZZ = np.repeat(X, len(Z), axis=0), np.tile(Z, (len(X), 1))
    sim = BitSim((n+g)*b+anc_size(b), len(XX))
    for k in range(n):
        sim.load(a[k], XX[:, k])
    for k in range(g):
        sim.load(z[k], ZZ[:, k])
    sim.run(gates)
    out = np.stack([sim.read(a[k]) for k in range(n)], axis=1)
    ok = all(np.array_equal(sim.read(z[k]), ZZ[:, k]) for k in range(g)) and \
        not any(sim.wire_nonzero(w) for w in anc.all)
    zfull = np.concatenate([np.zeros((len(ZZ), n-g), dtype=np.int64), (-ZZ) % p], axis=1)
    ok = ok and bool(np.array_equal(out, law.mul(XX, zfull)))      # x z^-1, z central
    return law.encode(out).reshape(len(X), len(Z)), ok


def child_state_after_instrument(cfg, keys, perm):
    """phi[lam] as integer Z[zeta_p] arrays over (x', key) for every label lam
    (the label register kept coherent): phi_lam(x', y) = sum_z zeta^(-lam.z)
    [y = key(x' z)], with overall scale 1/(sqrt|G_c| p^g) (tracked separately).
    QFT_p is the exact unitary of rees_circuit_general.qft_matrix (checked)."""
    p, d = cfg.p, cfg.c
    if not G._qft_ok(p):
        raise AssertionError("QFT_p gate is not the exact Fourier matrix")
    g = cfg.dims[d-1]
    law = cfg.laws[d]
    ukeys, kidx = np.unique(keys, return_inverse=True)
    Z = np.array(list(product(range(p), repeat=g)), dtype=np.int64).reshape(-1, g)
    phi = {}
    for lam in product(range(p), repeat=g):
        arr = np.zeros((law.order, len(ukeys), p), dtype=np.int64)
        for zi, zv in enumerate(Z):
            e = int(-np.dot(lam, zv)) % p
            xprime = perm[:, zi]                        # x -> x' = x z^-1
            np.add.at(arr, (xprime, kidx, e), 1)
        arr = arr-arr[..., -1:]
        if arr.any():
            phi[lam] = arr
    return phi, len(ukeys)


def block_child_tables(block, lam_tuples, gates=None):
    """For every label tuple and every q: the permutation x -> pi(x) applied to
    each child by the block gate list, from a bit-level run with x_1 = .. = x_M
    = u for all u (valid because the block maps children independently:
    block_exhaustive / block_structure). Returns tab[t, i, q, u]."""
    cfg, p, M = block.cfg, block.p, block.M
    law_x, law_q = cfg.laws[block.d], cfg.laws[block.d-1]
    X, Qe = law_x.elements(), law_q.elements()
    T = len(lam_tuples)
    nX, nQ = len(X), len(Qe)
    tt, qq, uu = np.meshgrid(np.arange(T), np.arange(nQ), np.arange(nX), indexing="ij")
    tt, qq, uu = tt.ravel(), qq.ravel(), uu.ravel()
    lam = np.asarray(lam_tuples, dtype=np.int64)[tt]
    xs = np.repeat(X[uu][:, None, :], M, axis=1)
    qv = Qe[qq]
    gates = block.flatten() if gates is None else gates
    sim = BitSim(block.nw, len(tt))
    for i in range(M):
        for r in range(block.g):
            sim.load(block.lam[i][r], lam[:, i, r])
        for j in range(block.nx):
            sim.load(block.x[i][j], xs[:, i, j])
    for j in range(block.nq):
        sim.load(block.Q[j], qv[:, j])
    sim.run(gates)
    clean = not any(sim.wire_nonzero(w) for w in range(block.nw) if w not in block.io)
    tab = np.zeros((T, M, nQ, nX), dtype=np.int64)
    for i in range(M):
        out = np.stack([sim.read(block.x[i][j]) for j in range(block.nx)], axis=1)
        tab[:, i] = law_x.encode(out).reshape(T, nQ, nX)
    return tab, clean


def heis_end_to_end(cfg, inst, block=None, gates=None, tables=None):
    """Exact simulation of the COMPLETE coherent terminal sample of a class-2
    instance (Heis(F_3)) from its gate lists: M sources (generator gate list,
    bit level), M unmeasured instruments (exact QFT_p, bit-level a_top -= z),
    Q prepared by QFT_p, the coherent merge block (bit level), final QFT_p on Q.
    The state is kept in the exact factorised form
        sum_lam |lam> (x) sum_q |q> (x)_i R^(i)_(lam, q) phi^(lam_i)
    (children are disjoint registers until the block, and the block is block
    diagonal in lam with S and workspace returned to 0). Returns the exact
    reduced density of Q (over Z[zeta_p], rational scale), the exact readout
    law, and the per-label-tuple conditional states."""
    p, c = cfg.p, cfg.c
    if c != 2:
        raise ValueError("factorised end-to-end simulation implemented for class 2")
    block = block or MergeBlock(cfg, 2)
    M, g = block.M, block.g
    keys, src_ok = source_label_keys(cfg, inst)
    perm, inst_ok = instrument_permutation(cfg, 2)
    phi, nkeys = child_state_after_instrument(cfg, keys, perm)
    lam_tuples = list(product(product(range(p), repeat=g), repeat=M))
    if tables is None:
        tables, clean = block_child_tables(block, lam_tuples, gates)
    else:
        clean = True
    law1 = cfg.laws[1]
    nQ = law1.order
    gram_cache = {}
    # rho[q, r] = |Q|^-1 sum_lam prod_i <R_r phi_i | R_q phi_i>;  inner products over (x', key)
    rho = np.zeros((nQ, nQ, p), dtype=np.int64)
    cond = {}
    for t, lams in enumerate(lam_tuples):
        if not all(l in phi for l in lams):
            continue                                  # zero amplitude branch
        acc = None
        for i, l in enumerate(lams):
            tab = tables[t, i]                         # (nQ, nX): pi_q(u)
            key = (l, tab.tobytes())
            if key not in gram_cache:
                ph = phi[l]                            # (nX, nkeys, p)
                V = np.zeros((nQ,)+ph.shape, dtype=np.int64)
                for q in range(nQ):
                    V[q, tab[q]] = ph                  # (R_q phi)(pi_q(u)) = phi(u)
                Vf = V.reshape(nQ, -1, p)
                Gm = np.zeros((nQ, nQ, p), dtype=np.int64)
                Vc = _cyc_conj(Vf)
                for q in range(nQ):
                    for r in range(nQ):
                        Gm[q, r] = _cyc_dot(Vc[r], Vf[q], p)
                gram_cache[key] = Gm - Gm[..., -1:]
            Gm = gram_cache[key]
            acc = Gm if acc is None else _cyc_mul_entrywise(acc, Gm, p)
        cond[lams] = acc
        rho += acc
    rho = rho-rho[..., -1:]
    # scales: each child amplitude 1/(sqrt|G_2| p^g) -> inner product 1/(|G_2| p^(2g)); Q prep 1/|G_1|
    scale = Fraction(1, nQ)*Fraction(1, (cfg.laws[2].order*p**(2*g))**M)
    # readout: P(k) = |G_1|^-1 sum_(q,r) zeta^(k.(q-r)) rho[q, r]
    E = law1.elements()
    kq = (E @ E.T) % p                                 # k.q
    probs = {}
    for ki, k in enumerate(E):
        ph = (kq[ki][:, None]-kq[ki][None, :]) % p     # exponent of zeta for (q, r)
        tot = np.zeros(p, dtype=np.int64)
        for e in range(p):
            m = (ph == e)
            tot += np.roll(rho[m].sum(axis=0), e)
        tot = tot-tot[-1]
        if tot[1:].any():
            raise ArithmeticError("readout probability not rational")
        if tot[0]:
            probs[tuple(int(v) for v in k)] = scale*Fraction(int(tot[0]), nQ)
    return {"rho": rho, "scale": scale, "probs": probs, "cond": cond, "source_ok": src_ok,
            "instrument_ok": inst_ok, "block_clean": clean, "nkeys": nkeys,
            "label_tuples_nonzero": len(cond)}


def _cyc_mul_entrywise(a, b, p):
    out = np.zeros(np.broadcast_shapes(a.shape, b.shape), dtype=np.int64)
    for i in range(p):
        out += np.roll(a[..., i:i+1]*b, i, axis=-1)
    return out - out[..., -1:]


def rho_target(cfg, log_h, d):
    """rho_(H_d)[q, r] = [q^-1 r in H_d]/|G_d| as a 0/1 matrix and scale (grade 1: abelian)."""
    law = cfg.laws[d]
    idx = set(G.stage_indices(cfg, log_h, d).tolist())
    E = law.elements()
    inv = (-E) % cfg.p if d == 1 else None
    D = np.array([[law.encode(law.mul(inv[q][None, :], E[r][None, :]))[0] for r in range(law.order)]
                  for q in range(law.order)])
    return np.isin(D, list(idx)).astype(np.int64), Fraction(1, law.order)


def heis_compare(cfg, inst, res):
    """Compare the coherent end-to-end result with the measured generator."""
    p = cfg.p
    tgt, tsc = rho_target(cfg, inst.log_h, 1)
    rho, sc = res["rho"], res["scale"]
    rational = not rho[..., 1:].any()
    rho_equal = rational and all(sc*int(rho[q, r, 0]) == tsc*int(tgt[q, r])
                                 for q in range(len(tgt)) for r in range(len(tgt)))
    # every positive-probability label tuple: conditional state proportional to rho_H1
    cond_ok = True
    for lams, acc in res["cond"].items():
        if acc[..., 1:].any():
            cond_ok = False
            break
        v = acc[..., 0]
        if not v.any():
            continue
        ratio = v[0, 0]
        cond_ok &= bool(np.array_equal(v*1, tgt*ratio)) and ratio > 0
    h_perp = {tuple(int(x) for x in r) for r in span_elements(nullspace(inst.log_h, cfg.m, p), cfg.m, p)}
    probs = res["probs"]
    uniform = set(probs) == h_perp and all(v == Fraction(1, len(h_perp)) for v in probs.values())
    recovered = rref(nullspace(sorted(probs), cfg.m, p), p) == rref(inst.log_h, p)
    return {"rho_Q_equals_rho_H1": bool(rho_equal), "every_label_branch_proportional_to_rho_H1": bool(cond_ok),
            "readout_uniform_on_h_perp": bool(uniform), "support_nullspace_equals_log_H": bool(recovered),
            "trace_one": sum(probs.values()) == 1}


def heis_measured_reference(cfg, inst, eng, witness_rule="canonical"):
    """Measured-label generator (exact Engine): mixture over all label tuples of
    the merged outputs with the witness s(lambda) (canonical rule, i.e. the
    classical feed-forward of the same s) and readout law."""
    p, d = cfg.p, 2
    st, S, info = eng.source(inst)
    probs, states = eng.label_law(st)
    M = cfg.arity[d]
    acc = None
    tot = Fraction(0)
    for lams in product(sorted(probs), repeat=M):
        pr = prod(probs[l] for l in lams)
        if not pr:
            continue
        A = np.array([[list(l) for l in lams]]).transpose(0, 2, 1)
        s = sde_reference(p, d, A)[0]
        out = eng.merge([states[l] for l, si in zip(lams, s) if si], [int(x) for x in s if x])
        dense = out.v[:, 0] if not out.v[:, 1:].any() else None
        if dense is None:
            raise ArithmeticError("non-rational merged output")
        vec = {k: pr*out.scale*int(v) for k, v in enumerate(dense) if v}
        tot += pr
        if acc is None:
            acc = Counter()
        for k, v in vec.items():
            acc[k] += v
    tgt = set(G.stage_indices(cfg, inst.log_h, 1).tolist())
    mixture_ok = tot == 1 and set(acc) == tgt and all(v == 1 for v in acc.values())
    return {"measured_mixture_equals_rho_H1": bool(mixture_ok)}


def sample_recovery(cfg, inst, probs, seed, extra=4):
    rng = random.Random(seed)
    keys = sorted(probs)
    w = [float(probs[k]) for k in keys]
    samples = rng.choices(keys, weights=w, k=cfg.m+extra)
    return rref(nullspace(samples, cfg.m, cfg.p), cfg.p) == rref(inst.log_h, cfg.p)


# ====================================================================== n4(F_5): per-merge state checks

class CircuitWitness:
    """s(lambda) computed by running the coherent SDE gate list (remapped into
    a block) bit-level; cached."""

    def __init__(self, block):
        self.block = block
        self.gates = flatten(block.U, block.p, block.anc)
        self.cache = {}
        self.runs = 0

    def __call__(self, label_tuples):
        todo = [t for t in label_tuples if t not in self.cache]
        if todo:
            blk = self.block
            lam = np.array(todo, dtype=np.int64).reshape(len(todo), blk.M, blk.g)
            sim = BitSim(blk.nw, len(todo))
            for i in range(blk.M):
                for r in range(blk.g):
                    sim.load(blk.lam[i][r], lam[:, i, r])
            sim.run(self.gates)
            s = np.stack([sim.read(blk.S[i]) for i in range(blk.M)], axis=1)
            for t, row in zip(todo, s):
                self.cache[t] = tuple(int(v) for v in row)
            self.runs += 1
        return [self.cache[t] for t in label_tuples]


def n4_state_checks(cfg, inst, eng, witnesses, rng, grade2_tuples=12, max_all=5000):
    """Per merge, exact (Engine, Z[zeta_5]): grade 3 on ALL positive-probability
    label pairs, grade 2 on sampled label 6-tuples; the witness of every merge is
    the output of the coherent SDE gate list; every merged output must equal
    rho_(H_(d-1)) (so the deferred-measurement mixture does too); readout law."""
    p = cfg.p
    row = {"instance": inst.name, "grades": {}}
    st, S, sinfo = eng.source(inst)
    ok = bool(sinfo["coset_state"]) and np.array_equal(np.sort(S), G.stage_indices(cfg, inst.log_h, cfg.c))
    for d in range(cfg.c, 1, -1):
        probs, states = eng.label_law(st)
        allowed = [l for l, v in probs.items() if v]
        M = cfg.arity[d]
        if len(allowed)**M <= max_all:
            tuples, mode = list(product(allowed, repeat=M)), "all"
        else:
            zero = tuple([0]*cfg.dims[d-1])
            tuples = [tuple([zero]*M), tuple([allowed[-1]]*M)]
            tuples += [tuple(rng.choice(allowed) for _ in range(M)) for _ in range(grade2_tuples-2)]
            mode = f"sampled {len(tuples)} of {len(allowed)**M}"
        ws = witnesses[d](tuples)
        target = G.stage_indices(cfg, inst.log_h, d-1)
        good = 0
        valid = 0
        fac = {}
        for lams, s in zip(tuples, ws):
            valid += any(s) and all(sum(pow(si, d, p)*l[r] for si, l in zip(s, lams)) % p == 0
                                    for r in range(cfg.dims[d-1]))
            act = [(l, si) for l, si in zip(lams, s) if si]
            for key in act:
                if key not in fac:
                    fac[key] = states[key[0]].v[eng.dil(d, key[1])]
            out = eng.merge([states[l] for l, _ in act], [si for _, si in act], factors=[fac[k] for k in act])
            good += out.equals_indicator(target)
        row["grades"][d] = {"arity": M, "label_support": len(allowed), "tuples": mode, "cases": len(tuples),
                            "witness_valid": valid == len(tuples), "outputs_equal_rho_H": good == len(tuples)}
        ok = ok and valid == len(tuples) and good == len(tuples)
        v = np.zeros((cfg.laws[d-1].order, p), dtype=np.int64)
        v[target, 0] = 1
        st = G.XState(d-1, Fraction(1), v)
    pr = eng.readout(st)
    h_perp = {tuple(int(x) for x in r) for r in span_elements(nullspace(inst.log_h, cfg.m, p), cfg.m, p)}
    row["readout_uniform_on_h_perp"] = set(pr) == h_perp and all(v == Fraction(1, len(h_perp)) for v in pr.values())
    row["passed"] = bool(ok and row["readout_uniform_on_h_perp"])
    return row


def run_coherent_witness(cfg, inst, eng, witnesses, seed=0, extra=4):
    """Seeded run from oracle access: exact label laws, labels sampled, the
    witness of EVERY merge from the coherent SDE gate list (the classical
    shadow of the coherent receiver: by deferred measurement the coherent
    receiver's readout law is the law of this run's readout), nullspace."""
    rng = random.Random(seed)
    p, c = cfg.p, cfg.c
    top, _, _ = eng.source(inst)
    cache = {}

    def law(st, key):
        if key not in cache:
            cache[key] = eng.label_law(st)
        return cache[key]

    def sample(probs):
        ks = [k for k in probs if probs[k]]
        return rng.choices(ks, weights=[float(probs[k]) for k in ks], k=1)[0]
    stats = Counter()

    def make(d):
        if d == c:
            stats["top_sources"] += 1
            pr, sts = law(top, ("top",))
            lam = sample(pr)
            return lam, sts[lam]
        kids = [make(d+1) for _ in range(cfg.arity[d+1])]
        lams = tuple(k[0] for k in kids)
        s = witnesses[d+1]([lams])[0]
        stats[f"coherent_witness_d{d+1}"] += 1
        out = eng.merge([k[1] for k, si in zip(kids, s) if si], [si for si in s if si])
        if d == 1:
            return None, out
        pr, sts = law(out, (d, out.scale, out.v.tobytes()))
        lam = sample(pr)
        return lam, sts[lam]
    samples = []
    for _ in range(cfg.m+extra):
        _, st = make(1)
        samples.append(sample(eng.readout(st)))
    got = rref(nullspace(samples, cfg.m, p), p)
    return {"recovered": got == rref(inst.log_h, p), "oracle_queries": len(cfg.points)*stats["top_sources"],
            **dict(stats)}


# ====================================================================== report driver

def counts_report(job):
    cfg = job_config(job)
    ts = TerminalSample(cfg)
    out = {"config": cfg.name(), "terminal_sample": ts.counts(), "structure": ts.structure(), "blocks": {}}
    for d, blk in ts.blocks.items():
        out["blocks"][d] = {"kappa": kappa(cfg.p, d), "arity": blk.M, "label_dim": blk.g,
                            "sde_qubits": blk.sde.nw, "qubits": blk.qubits(), "segments": blk.segment_counts(),
                            "structure": block_structure(blk)}
    alg = cfg.algebra
    out["measured_generator_cw_arity"] = measured_counts(alg)
    if job == "n4_f5":
        out["measured_generator_coherent_arity"] = measured_counts(alg, arities=dict(cfg.arity))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    ap.add_argument("--parts", default="counts,proofs,paths,heis,n4,sampled")
    ap.add_argument("--heis-exhaustive", action="store_true", help="block on ALL 3^18 joint inputs (minutes)")
    args = ap.parse_args()
    parts = set(args.parts.split(","))
    log = lambda *a: print(*a, flush=True)
    res = {**STATUS, "parts": sorted(parts)}
    t0 = time.time()

    def dump():
        with open(args.out, "w") as fh:
            json.dump(res, fh, indent=1, default=str)

    if "counts" in parts:
        res["counts"] = {job: counts_report(job) for job in ("heis_f3", "n4_f5")}
        log("counts", round(time.time()-t0, 1))
        dump()
    if "proofs" in parts:
        res["proofs"] = {}
        for job in ("heis_f3", "n4_f5"):
            cfg = job_config(job)
            for d in range(2, cfg.c+1):
                blk = MergeBlock(cfg, d)
                res["proofs"][f"{job}_d{d}"] = {"controlled_merge": prove_controlled_merge(blk),
                                                "structure": block_structure(blk)}
                if blk.p**(blk.M*blk.g) <= 3**12:
                    res["proofs"][f"{job}_d{d}"]["sde_exhaustive"] = sde_exhaustive(blk)
        log("proofs", round(time.time()-t0, 1))
        dump()
    if "paths" in parts:
        res["assembled_basis_paths"] = {}
        for job, n in (("heis_f3", 1 << 14), ("n4_f5", 1024)):
            res["assembled_basis_paths"][job] = assembled_basis_paths(TerminalSample(job_config(job)), n=n,
                                                                      seed=20261104)
            log("paths", job, res["assembled_basis_paths"][job]["passed"], round(time.time()-t0, 1))
        dump()
    if "sampled" in parts:
        res["block_sampled"] = {}
        for job, n in (("heis_f3", 1 << 16), ("n4_f5", 4096)):
            cfg = job_config(job)
            for d in range(2, cfg.c+1):
                blk = MergeBlock(cfg, d)
                res["block_sampled"][f"{job}_d{d}"] = block_sampled(blk, n=n, seed=20261104)
                log("sampled", job, d, res["block_sampled"][f"{job}_d{d}"]["passed"], round(time.time()-t0, 1))
        cfg = job_config("n4_f5")
        blk = MergeBlock(cfg, 3)
        # grade 3: ALL (lam_1, lam_2, q) with one random pair of children per input
        lam = np.array(list(product(range(cfg.p), repeat=2)), dtype=np.int64)
        Qe = cfg.laws[2].elements()
        L = np.repeat(lam, len(Qe), axis=0).reshape(-1, 2, 1)
        qv = np.tile(Qe, (len(lam), 1))
        xs = np.random.default_rng(3).integers(0, cfg.p, size=(len(qv), 2, blk.nx))
        res["block_sampled"]["n4_f5_d3_all_labels_all_q"] = block_check(blk, L, xs, qv)
        log("n4 d3 all (lam, q)", res["block_sampled"]["n4_f5_d3_all_labels_all_q"]["passed"], round(time.time()-t0, 1))
        dump()
    if "heis" in parts:
        cfg = job_config("heis_f3")
        blk = MergeBlock(cfg, 2)
        gates = blk.flatten()
        eng = G.Engine(cfg)
        lam_tuples = list(product(product(range(cfg.p), repeat=blk.g), repeat=blk.M))
        tables, clean = block_child_tables(blk, lam_tuples, gates)
        rows = []
        for inst in G.heis3_instances():
            t1 = time.time()
            r = heis_end_to_end(cfg, inst, blk, tables=tables)
            cmp_ = heis_compare(cfg, inst, r)
            meas = heis_measured_reference(cfg, inst, eng)
            rec = [sample_recovery(cfg, inst, r["probs"], seed) for seed in (20261103, 20261104)]
            rows.append({"instance": inst.name, "source_ok": r["source_ok"], "instrument_ok": r["instrument_ok"],
                         "label_tuples_nonzero": r["label_tuples_nonzero"], **cmp_, **meas,
                         "seeded_recoveries": rec, "seconds": round(time.time()-t1, 2)})
            log("heis", inst.name, all(v for k, v in rows[-1].items() if isinstance(v, bool)), rows[-1]["seconds"])
        res["heis_end_to_end"] = {"block_tables_clean": clean, "rows": rows,
                                  "all_pass": clean and all(all(v for k, v in r.items() if isinstance(v, bool))
                                                            and all(r["seeded_recoveries"]) for r in rows)}
        dump()
    if args.heis_exhaustive:
        cfg = job_config("heis_f3")
        blk = MergeBlock(cfg, 2)
        res["heis_block_exhaustive"] = block_exhaustive(blk, log=log)
        dump()
    if "n4" in parts:
        cfg = job_config("n4_f5")
        eng = G.Engine(cfg)
        wit = {d: CircuitWitness(MergeBlock(cfg, d)) for d in range(2, cfg.c+1)}
        rng = random.Random(20261104)
        rows, runs = [], []
        for inst in G.n4_instances(5):
            t1 = time.time()
            rows.append(n4_state_checks(cfg, inst, eng, wit, rng, grade2_tuples=256, max_all=20000))
            for seed in (20261103, 20261104):
                runs.append({"instance": inst.name, "seed": seed,
                             **run_coherent_witness(cfg, inst, eng, wit, seed=seed)})
            log("n4", inst.name, rows[-1]["passed"], [r["recovered"] for r in runs[-2:]], round(time.time()-t1, 1))
            res["n4_state"] = {"rows": rows, "runs": runs}
            dump()
        res["n4_state"]["all_pass"] = all(r["passed"] for r in rows) and all(r["recovered"] for r in runs)
        dump()
    res["seconds"] = round(time.time()-t0, 1)
    dump()
    log("done", res["seconds"])


if __name__ == "__main__":
    main()

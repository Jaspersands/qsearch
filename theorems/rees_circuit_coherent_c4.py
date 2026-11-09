"""Coherent-label Rees backend on a class-four instance: n5(F_7).

AI-checked, pending human review. Report:
research/audits/reviews/2026-11-04-rees-circuit-coherent-c4.md.

Instance: the class-four filiform algebra n5 = <e1..e5 | [e1, e_i] = e_(i+1),
i = 2, 3, 4> over F_7. Graded cover dims (5, 3, 2, 1), |G_4| = 7^11. Every SDE
grade has p = 7 outside E_2(kappa_d): kappa_4 = gcd(4, 6) = 2 (g_4 = 1),
kappa_3 = 3 (g_3 = 2), kappa_2 = 2 (g_2 = 3). Merge arity (g_d+1)(g_d+2)/2 at
every grade (kappa_d >= 2): M_4 = 3, M_3 = 6, M_2 = 10 (Chevalley-Warning
arities of the measured generator: 3, 7, 7).

No existing file is edited. The circuit is the fifth backend's
(theorems/rees_circuit_coherent_k3.py, imported read-only), which in turn runs
the fourth backend's MergeBlock / TerminalSample under a scoped dispatch:
grade 4 uses CoherentSDEK2(7, 1, 4), grade 3 CoherentSDEKappa(7, 2, 3) (the
triangular solver of lem:coherent-power-sde), grade 2 CoherentSDEK2(7, 3, 2).
This module adds the class-four instance, checks sized for it, and an exact
per-merge state check on reduced supports.

Checks (exact unless marked sampled):
* macro_checks: rees_circuit_arith.exhaustive_macro_check(7), all
  coefficients, all 2^(kb) words: every add_scaled / add_product gate list
  the blocks use is the declared F_7 map with clean ancillas;
* prove_controlled_merge at d = 2, 3, 4 (symbolic replay over F_7[s, q, x]
  against the class-d BCH polynomial) and block_structure (footprints);
* sde_check: U_SDE inside the block; grade 4 on ALL 7^3 label triples,
  grade 3 on ALL rank <= 1 label 6-tuples (941 185) plus random ones,
  grade 2 sampled (structured + random);
* block checks (bit level, every wire of a merge block): sampled (x, q),
  grade 4 for all 343 label triples, grade 3 for all rank <= 1 tuples;
* mutants that block_check / the wiring check must reject;
* assembled_basis_paths: wiring of the whole terminal sample (83 M gates);
* source_exact_check: the evaluation program of a source, replayed
  symbolically (linear forms over the 11 address coordinates) and checked
  to be w = a E_s at each oracle call; the identity fibre of the joint
  oracle key computed by linear algebra (kernel of a -> (a E_s N_h)_s) and
  compared with exp(h~) = stage_indices(c); E_s a homomorphism on samples;
* state_checks: SparseEngine (states on their support only) with the top
  source built as the coset state of that kernel (NOT evaluated from the
  source gate list on all 7^11 addresses) and the witness of every merge from
  a bit-level run of the coherent SDE gate list; every merged output must
  equal rho_(H_(d-1)) and the readout must be uniform on h^perp;
* seeded runs (same engine, breadth first), nullspace of the readout.

NOT done: any amplitude simulation of the whole terminal sample (20 566
qubits), a dense state at grade four, the source from its gate list on all
addresses, QFT_7 synthesis, oracle cost, noise, layout, other instances. No
claim gate is flipped: coherent_receiver_implemented stays False in
research/reductions/rees_hsp_reduction.json.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
import random
import time

import numpy as np

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_coherent_k3 as K
import theorems.rees_circuit_general as G
from theorems.rees_circuit_arith import exhaustive_macro_check
from theorems.rees_circuit_sparse import SparseEngine, SState, n5_instances
from theorems.rees_coherent_sde import BitSim, Macro, Prog
from theorems.rees_coherent_sde_k2 import CoherentSDEK2
from theorems.rees_coherent_sde_kappa import rref_count, rref_iter_chunks
from theorems.rees_end_to_end_sim import filiform5, nullspace, rref, span_elements

STATUS = {"status": "coherent_label_receiver_backend_class_four_instance_finite_checks",
          "scope": "n5(F_7) only: kappa = (2, 3, 2) at grades (4, 3, 2), arities (3, 6, 10)",
          "coherent_receiver_implemented": False,
          "coherent_label_backend_class_four_instance": True,
          "general_instances": False, "qft_synthesised": False,
          "whole_circuit_amplitude_simulation": False,
          "source_from_gate_list_on_all_addresses": False,
          "independent_review": False, "speedup_claim_allowed": False,
          "review": "AI-checked, pending human review"}

P = 7
SEEDS = (20261103, 20261104)
log = lambda *a: print(*a, flush=True)


# ====================================================================== instance

def config():
    """Coherent config of n5(F_7): arities (g_d+1)(g_d+2)/2 at every grade."""
    return K.coherent_config_k(filiform5(P))


def instances():
    """The nine hidden subgroups of rees_circuit_sparse.N5_SUBGROUPS, over F_7."""
    return n5_instances(P)


def blocks(cfg, mutate=None, sde_mutate=None):
    return {d: K.MergeBlockK(cfg, d, mutate=mutate, sde_mutate=sde_mutate) for d in range(2, cfg.c+1)}


# ====================================================================== counts

def counts_report(cfg=None):
    cfg = cfg or config()
    ts = K.TerminalSampleK(cfg)
    out = {"config": cfg.name(), "terminal_sample": ts.counts(), "structure": ts.structure(), "blocks": {}}
    for d, blk in ts.blocks.items():
        out["blocks"][d] = {"kappa": K.kappa(cfg.p, d), "arity": blk.M, "label_dim": blk.g,
                            "sde_class": type(blk.sde).__name__, "sde_qubits": blk.sde.nw, "qubits": blk.qubits(),
                            "segments": blk.segment_counts(), "structure": C.block_structure(blk)}
    out["measured_generator_cw_arity"] = C.measured_counts(cfg.algebra)
    out["measured_generator_coherent_arity"] = C.measured_counts(cfg.algebra, arities=dict(cfg.arity))
    for key in ("measured_generator_cw_arity", "measured_generator_coherent_arity"):
        m = out[key]
        m["gates_incl_bch_swaps"] = m["arith_gates"]+m["swap_macro"]
    return out


# ====================================================================== arithmetic: macros

def used_macros(blks):
    """(kind, coeff) pairs of every macro in the given blocks."""
    return sorted({(it.kind, int(it.coeff)) for blk in blks.values() for it in blk.prog if isinstance(it, Macro)})


def macro_checks(blks=None):
    rows = exhaustive_macro_check(P)
    used = used_macros(blks) if blks else []
    ok = {(r["kind"], r["coeff"]): r["ok"] for r in rows}
    return {"rows": len(rows), "all_ok": all(r["ok"] for r in rows),
            "words_per_row": sorted({r["words"] for r in rows}),
            "used_kind_coeff": used, "used_all_checked": all(ok.get(u, False) for u in used)}


# ====================================================================== U_SDE inside a block

def rank_le1_tuples(p, g, M):
    """All M-tuples of vectors of F_p^g spanning a space of dimension <= 1:
    the zero tuple, then for each projective point v and each nonzero c in F_p^M
    the tuple (c_1 v, .., c_M v). Count 1 + (p^g-1)/(p-1) (p^M-1)."""
    lines = []
    for v in product(range(p), repeat=g):
        nz = [x for x in v if x]
        if nz and nz[0] == 1:
            lines.append(v)
    cs = np.array(list(product(range(p), repeat=M))[1:], dtype=np.int64)        # nonzero c
    out = [np.zeros((1, M, g), dtype=np.int64)]
    for v in lines:
        out.append((cs[:, :, None]*np.array(v, dtype=np.int64)[None, None, :]) % p)
    return np.concatenate(out, axis=0)


def random_rank_le1_tuples(p, g, M, n, seed):
    """n uniform random rank-exactly-1 tuples: random nonzero line v (projective
    representative), random nonzero c in F_p^M, tuple (c_i v)."""
    rng = np.random.default_rng(seed)
    lines = [v for v in product(range(p), repeat=g) if any(v) and [x for x in v if x][0] == 1]
    V = np.array(lines, dtype=np.int64)[rng.integers(0, len(lines), n)]
    c = rng.integers(0, p, size=(n, M))
    bad = ~c.any(axis=1)
    c[bad, 0] = 1
    return (c[:, :, None]*V[:, None, :]) % p


def all_label_tuples(p, g, M):
    lam = np.array(list(product(range(p), repeat=M*g)), dtype=np.int64)
    return lam.reshape(-1, M, g)


def random_label_tuples(p, g, M, n, seed):
    return np.random.default_rng(seed).integers(0, p, size=(n, M, g))


def structured_tuples(cfg, d, n, seed):
    return C.structured_label_tuples(cfg, d, n, random.Random(seed))


def sde_check(block, lam, chunk=1 << 18, gates=None):
    """U_SDE (remapped into the block) alone on the given label tuples (N, M, g):
    S = canonical witness of the independent reference, s != 0,
    sum_i s_i^d lam_i = 0, labels restored, every other wire 0."""
    p, M, g, d = block.p, block.M, block.g, block.d
    gates = C.flatten(block.U, p, block.anc) if gates is None else gates
    io = {w for r in block.lam for q in r for w in q} | {w for q in block.S for w in q}
    f = {"inputs": int(len(lam)), "gates": len(gates), "witness_equals_canonical": True, "witness_nonzero": True,
         "equation_holds": True, "labels_restored": True, "workspace_clean": True}
    pw = np.array([pow(t, d, p) for t in range(p)], dtype=np.int64)
    t0 = time.time()
    for a in range(0, len(lam), chunk):
        L = lam[a:a+chunk]
        sim = BitSim(block.nw, len(L))
        for i in range(M):
            for k in range(g):
                sim.load(block.lam[i][k], L[:, i, k])
        sim.run(gates)
        s = np.stack([sim.read(block.S[i]) for i in range(M)], axis=1)
        with K.kappa_dispatch():
            ref = C.sde_reference(p, d, np.transpose(L, (0, 2, 1)))
        f["witness_equals_canonical"] &= bool(np.array_equal(s, ref))
        f["witness_nonzero"] &= bool(s.any(axis=1).all())
        f["equation_holds"] &= bool((np.einsum("nig,ni->ng", L, pw[np.minimum(s, p-1)]) % p == 0).all())
        f["labels_restored"] &= all(np.array_equal(sim.read(block.lam[i][k]), L[:, i, k])
                                    for i in range(M) for k in range(g))
        f["workspace_clean"] &= not any(sim.wire_nonzero(w) for w in range(block.nw) if w not in io)
        del sim
    f["sim_seconds"] = round(time.time()-t0, 1)
    f["passed"] = all(v for v in f.values() if isinstance(v, bool))
    return f


def rref_label_chunks(p, g, M, chunk=1 << 18):
    """One label tuple per row space of the g x M label matrix (dimension <= g):
    the RREF representatives of rees_coherent_sde_kappa, as (N, M, g) chunks.
    The canonical witness depends only on the row space (Lemma 5 of the
    kappa = 3 report); the circuit is checked on the representatives themselves."""
    for A in rref_iter_chunks(p, g, M, chunk):
        yield np.ascontiguousarray(np.transpose(A, (0, 2, 1)))


def sde_check_rref(block, chunk=1 << 18, log_fn=None):
    """sde_check on every RREF representative (grade 3: 6 884 860 row spaces)."""
    gates = C.flatten(block.U, block.p, block.anc)
    agg, t0 = None, time.time()
    for lam in rref_label_chunks(block.p, block.g, block.M, chunk):
        f = sde_check(block, lam, chunk=chunk, gates=gates)
        agg = _and_flags(agg, f)
        if log_fn:
            log_fn(f"  sde rref d={block.d} {agg['inputs']} ok={agg['passed']} {time.time()-t0:.0f}s")
    agg["row_spaces_expected"] = rref_count(block.p, block.g, block.M)
    agg["sim_seconds"] = round(time.time()-t0, 1)
    return agg


def _and_flags(agg, f):
    if agg is None:
        return dict(f)
    for k, v in f.items():
        if isinstance(v, bool):
            agg[k] = agg[k] and v
    agg["inputs"] += f["inputs"]
    agg["passed"] = all(v for k, v in agg.items() if isinstance(v, bool))
    return agg


# ====================================================================== whole merge blocks

def block_check_labels(block, lam, seed, chunk=1 << 16, gates=None, log_fn=None):
    """K.block_check on the given label tuples, each with one random (x_1..x_M, q)."""
    rng = np.random.default_rng(seed)
    xs = rng.integers(0, block.p, size=(len(lam), block.M, block.nx))
    qv = rng.integers(0, block.p, size=(len(lam), block.nq))
    return K.chunked_block_check(block, lam, xs, qv, chunk=chunk, gates=gates, log=log_fn)


def block_check_rref(block, seed, chunk=1 << 16, log_fn=None):
    """Whole block on every RREF label representative, one random (x, q) each."""
    gates = block.flatten()
    agg, t0 = None, time.time()
    for i, lam in enumerate(rref_label_chunks(block.p, block.g, block.M, 1 << 18)):
        f = block_check_labels(block, lam, [seed, i], chunk=chunk, gates=gates)
        agg = _and_flags(agg, f)
        if log_fn:
            log_fn(f"  block rref d={block.d} {agg['inputs']} ok={agg['passed']} {time.time()-t0:.0f}s")
    agg["row_spaces_expected"] = rref_count(block.p, block.g, block.M)
    agg["sim_seconds"] = round(time.time()-t0, 1)
    return agg


def repeat_labels(lam, k):
    return np.repeat(lam, k, axis=0)


def block_mutants(cfg, n=256, seed=7):
    """Each mutant must be rejected (passed False). Block mutants of the fourth
    backend at grade 4; kappa = 3 witness mutants at grade 3 (constants of
    kappa_constants(7, 3): alpha = (1, 0, 5), beta = (0, 2, 6)); a wrong-degree
    witness at grade 4 (the kappa = 2 circuit for d = 2 in place of d = 4)."""
    out = {}
    for mut in ("g_sign", "skip_ctrl_inv", "skip_sde_inv", "skip_bennett"):
        blk = K.MergeBlockK(cfg, 4, mutate={mut})
        lam = structured_tuples(cfg, 4, n, seed)
        out[f"d4_{mut}"] = not block_check_labels(blk, lam, seed)["passed"]
    for name, m in (("beta", {"beta": (0, 2, 5)}), ("alpha", {"alpha": (1, 0, 4)}), ("omega_min", {"omega_min": True})):
        blk = K.MergeBlockK(cfg, 3, sde_mutate=m)
        lam = np.concatenate([random_label_tuples(cfg.p, 2, 6, n, seed), rank_le1_tuples(cfg.p, 2, 6)[::3677]])
        out[f"d3_sde_{name}"] = not sde_check(blk, lam)["passed"] and not block_check_labels(blk, lam, seed)["passed"]
    # wrong degree: U_SDE solves sum s^2 lam = 0 at grade 4
    orig = K.sde_circuit_k

    def wrong(p, g, d, mutate=None):
        return CoherentSDEK2(p, g, 2) if d == 4 else orig(p, g, d, mutate)
    K.sde_circuit_k = wrong
    try:
        blk = K.MergeBlockK(cfg, 4)
    finally:
        K.sde_circuit_k = orig
    lam = all_label_tuples(cfg.p, 1, 3)
    out["d4_wrong_degree_witness"] = not block_check_labels(blk, lam, seed)["passed"]
    out["all_rejected"] = all(out.values())
    return out


def basis_paths_checked(ts, n=64, seed=0):
    """K.assembled_basis_paths, but a structurally broken program (for example a
    preparation transform that was deleted, so a register is never loaded) is a
    reported failure instead of a KeyError."""
    try:
        return K.assembled_basis_paths(ts, n=n, seed=seed)
    except (KeyError, IndexError, ValueError) as e:
        return {"passed": False, "crashed": f"{type(e).__name__}: {e}", "paths": n}


def assembled_mutants(cfg, n=64, seed=3):
    """Wiring check of a terminal sample with one item removed; must fail."""
    out = {}
    for comp, which in (("instrument", 0), ("witness_control_grade4", -1)):
        ts = K.TerminalSampleK(cfg)
        idx = [i for i, (c, _) in enumerate(ts.items) if c == comp][which]
        del ts.items[idx]
        ts.garbage_after = [(pos-(pos > idx), w) for pos, w in ts.garbage_after]
        out[f"drop_one_{comp}"] = not basis_paths_checked(ts, n=n, seed=seed)["passed"]
    out["all_rejected"] = all(out.values())
    return out


# ====================================================================== exact source check (no enumeration)

def first_source_items(ts):
    """Items of the first top source up to its instrument; and its node."""
    node = ts.tree
    while node["kids"]:
        node = node["kids"][0]
    items = []
    for comp, it in ts.items:
        if comp == "instrument_qft":
            break
        items.append((comp, it))
    return node, items


def source_exact_check(cfg, ts, inst, n_hom=4096, seed=0):
    """(i) Symbolic linear replay of the first source's evaluation macros:
    at the k-th oracle call the evaluation register w holds a E_(s_k) exactly
    (for ALL a), the oracle reads w and writes the k-th output register, and w
    is 0 after the last uncompute; (ii) the identity fibre of the joint key
    a -> (f(a E_s))_s is the subspace {a : a E_s n = 0 for all s and all n in
    h^perp} (f has fibres the left cosets of H by construction, E_s is linear
    in exponential coordinates); it must equal the rows of exp(h~) =
    stage_indices(c); (iii) E_s(x * y) = E_s(x) * E_s(y) on n_hom random pairs
    (so the fibres are the left cosets of that subgroup); (0) the source
    transforms are exactly one QFT_p per address register, in order, before any
    evaluation macro, the oracle output registers are distinct and fresh, and
    the address register ends as it started (form e_i) before the instrument."""
    p, c = cfg.p, cfg.c
    node, items = first_source_items(ts)
    a = node["reg"]
    n = cfg.width[c]
    form = {tuple(q): np.eye(n, dtype=np.int64)[i] for i, q in enumerate(a)}
    zero = np.zeros(n, dtype=np.int64)
    k = 0
    ok_eval = ok_wiring = True
    # (0) preparing transforms: exactly one source QFT_p per address register, in
    # register order, all before the first evaluation macro; no other qft/qft_dg
    # before the instrument; oracle output registers distinct and disjoint from
    # the address and evaluation registers.
    qfts = [(comp, tuple(it[1][0])) for comp, it in items
            if not isinstance(it, Macro) and it[0] in ("qft", "qft_dg")]
    first_use = next((i for i, (_, it) in enumerate(items) if isinstance(it, Macro) or it[0] != "qft"), len(items))
    pos_qft = [i for i, (_, it) in enumerate(items) if not isinstance(it, Macro) and it[0] in ("qft", "qft_dg")]
    ok_prep = qfts == [("source_qft", tuple(q)) for q in a] and \
        all(i < first_use for i in pos_qft)
    ys = [tuple(y) for y in node["ys"]]
    used = {w for q in a for w in q} | {w for q in ts.w for w in q}
    ok_outputs = len(set(ys)) == len(ys) == len(cfg.points) and \
        not any(set(y) & used for y in ys) and len({w for y in ys for w in y}) == sum(len(y) for y in ys)
    for comp, it in items:
        if isinstance(it, Macro):
            if it.kind != "add_scaled":
                ok_eval = False
                continue
            t, src = it.args
            cf = -it.coeff if it.inv else it.coeff
            form[t] = (form.get(t, zero)+cf*form.get(src, zero)) % p
        elif it[0] == "oracle":
            E = cfg.cover.evaluation_matrix(cfg.points[k])
            ok_eval &= all(np.array_equal(form.get(tuple(ts.w[j]), zero), E[:, j] % p) for j in range(cfg.m))
            ok_wiring &= it[1][0] == tuple(w for q in reversed(ts.w) for w in q) and \
                list(it[1][1]) == list(node["ys"][k])
            k += 1
        elif it[0] != "qft":
            ok_eval = False
    ok_eval &= k == len(cfg.points) and all(not form.get(tuple(q), zero).any() for q in ts.w)
    # (i') the address register is restored: form of a_i is the unit vector e_i
    ok_addr = all(np.array_equal(form.get(tuple(q), zero), np.eye(n, dtype=np.int64)[i]) for i, q in enumerate(a))
    hperp = nullspace(inst.log_h, cfg.m, p)
    rows = [tuple(int(x) for x in (cfg.cover.evaluation_matrix(s) @ np.array(v, dtype=np.int64)) % p)
            for s in cfg.points for v in hperp]
    kern = nullspace(rows, n, p) if rows else [tuple(int(i == j) for j in range(n)) for i in range(n)]
    S = np.sort(cfg.laws[c].encode(span_elements(kern, n, p)))
    want = G.stage_indices(cfg, inst.log_h, c)
    rng = np.random.default_rng(seed)
    X = rng.integers(0, p, size=(n_hom, n))
    Y = rng.integers(0, p, size=(n_hom, n))
    law, L = cfg.laws[c], cfg.L_law
    hom = all(np.array_equal(law.mul(X, Y) @ cfg.cover.evaluation_matrix(s) % p,
                             L.mul(X @ cfg.cover.evaluation_matrix(s) % p, Y @ cfg.cover.evaluation_matrix(s) % p))
              for s in cfg.points)
    res = {"evaluation_is_aE_s_for_all_a": bool(ok_eval), "oracle_wiring": bool(ok_wiring),
           "source_transforms_one_qft_per_address": bool(ok_prep), "oracle_outputs_distinct_fresh": bool(ok_outputs),
           "address_register_restored": bool(ok_addr),
           "kernel_dim": len(kern), "kernel_equals_exp_h_lift": bool(np.array_equal(S, want)),
           "evaluation_homomorphism_sampled": bool(hom), "hom_pairs": n_hom}
    res["passed"] = all(v for v in res.values() if isinstance(v, bool))
    return res, S


class SourceFromKernel(SparseEngine):
    """SparseEngine whose top source is the coset state 1_S / |G_c| with S the
    identity fibre computed by source_exact_check (no enumeration of G_c)."""

    def __init__(self, cfg, ts=None, chunk=1 << 20):
        super().__init__(cfg, chunk=chunk)
        self.ts = ts or K.TerminalSampleK(cfg)
        self.source_checks = {}

    def source(self, inst, points=None, uncompute=True, expand_oracle=False):
        info, S = source_exact_check(self.cfg, self.ts, inst)
        self.source_checks[inst.name] = info
        V = np.zeros((len(S), self.p), dtype=np.int64)
        V[:, 0] = 1
        info = {**info, "coset_state": info["passed"]}
        return SState(self.cfg.c, Fraction(1), S.astype(np.int64), V), S, info


# ====================================================================== per-merge exact states

def indicator_state(d, idx, p):
    V = np.zeros((len(idx), p), dtype=np.int64)
    V[:, 0] = 1
    return SState(d, Fraction(1), np.asarray(idx, dtype=np.int64), V)


def state_checks(cfg, inst, eng, witnesses, rng, tuples=64, max_all=400, log_fn=None):
    """Per merge, exact (SparseEngine, Z[zeta_7], states on their support): all
    positive-probability label tuples if there are <= max_all of them, else
    sampled (zero tuple, a constant tuple, uniform random ones); the witness of
    every merge from the coherent SDE gate list (CircuitWitness); every merged
    output must equal rho_(H_(d-1)); the next grade starts from rho_(H_(d-1));
    the readout law must be uniform on h^perp."""
    p = cfg.p
    row = {"instance": inst.name, "normal": bool(inst.normal), "grades": {}}
    st, S, sinfo = eng.source(inst)
    row["source"] = {k: v for k, v in sinfo.items()}
    row["source_support"] = int(len(S))
    ok = bool(sinfo["coset_state"])
    for d in range(cfg.c, 1, -1):
        t0 = time.time()
        probs, states = eng.label_law(st)
        allowed = [l for l, v in probs.items() if v]
        uniform = len(set(probs[l] for l in allowed)) == 1
        M = cfg.arity[d]
        if len(allowed)**M <= max_all:
            tups, mode = list(product(allowed, repeat=M)), "all"
        else:
            zero = tuple([0]*cfg.dims[d-1])
            tups = [tuple([zero]*M), tuple([allowed[-1]]*M)]
            tups += [tuple(rng.choice(allowed) for _ in range(M)) for _ in range(tuples-2)]
            mode = f"sampled {len(tups)} of {len(allowed)}^{M}"
        ws = witnesses[d](tups)
        target = G.stage_indices(cfg, inst.log_h, d-1)
        good = valid = 0
        cache = {}
        for lams, s in zip(tups, ws):
            valid += any(s) and all(sum(pow(si, d, p)*l[r] for si, l in zip(s, lams)) % p == 0
                                    for r in range(cfg.dims[d-1]))
            act = tuple(sorted((l, si) for l, si in zip(lams, s) if si))
            if act not in cache:
                try:
                    out = eng.merge([states[l] for l, _ in act], [si for _, si in act])
                    cache[act] = bool(out.equals_indicator(target))
                except (ArithmeticError, ValueError):
                    cache[act] = False
            good += cache[act]
        row["grades"][d] = {"arity": M, "state_support": int(len(st)), "label_support": len(allowed),
                            "label_law_uniform": bool(uniform), "tuples": mode, "cases": len(tups),
                            "distinct_merges": len(cache), "witness_valid": valid == len(tups),
                            "outputs_equal_rho_H": good == len(tups), "seconds": round(time.time()-t0, 1)}
        ok = ok and valid == len(tups) and good == len(tups) and uniform
        if log_fn:
            log_fn(f"  {inst.name} grade {d}: {row['grades'][d]}")
        st = indicator_state(d-1, target, p)
        del states
    pr = eng.readout(st)
    h_perp = {tuple(int(x) for x in r) for r in span_elements(nullspace(inst.log_h, cfg.m, p), cfg.m, p)}
    row["readout_uniform_on_h_perp"] = set(pr) == h_perp and all(v == Fraction(1, len(h_perp)) for v in pr.values())
    row["passed"] = bool(ok and row["readout_uniform_on_h_perp"])
    return row


def run_seeded(cfg, inst, eng, witnesses, seed=0, extra=4):
    """Seeded run, breadth first over m+extra terminal samples: labels sampled
    from the exact label laws, the witness of EVERY merge from the coherent SDE
    gate list (by deferred measurement the law of the coherent readout), the
    merge by the exact SparseEngine, then the nullspace of the readout samples.
    Same law as the depth-first order (all sources independent)."""
    rng = random.Random(seed)
    p, c = cfg.p, cfg.c
    T = cfg.m+extra
    top, _, sinfo = eng.source(inst)
    if not sinfo.get("coset_state"):
        return {"recovered": False, "source_check_failed": True, "terminal_samples": 0,
                "oracle_queries": 0}
    laws = {}

    def law(st):
        k = st.key()
        if k not in laws:
            laws[k] = eng.label_law(st)
        return laws[k]

    def sample(probs):
        ks = [k for k in probs if probs[k]]
        return rng.choices(ks, weights=[float(probs[k]) for k in ks], k=1)[0]
    stats = Counter()
    n_top = T*G.sources_per_grade(cfg)[c]
    level = []
    for _ in range(n_top):
        pr, sts = law(top)
        lam = sample(pr)
        level.append((lam, sts[lam]))
    stats["top_sources"] = n_top
    for d in range(c, 1, -1):
        M = cfg.arity[d]
        groups = [level[i:i+M] for i in range(0, len(level), M)]
        ws = witnesses[d]([tuple(l for l, _ in g) for g in groups])
        stats[f"coherent_witness_d{d}"] = len(groups)
        nxt, mcache = [], {}
        for g, s in zip(groups, ws):
            key = tuple((id(st), si) for (_, st), si in zip(g, s))
            if key not in mcache:
                mcache[key] = eng.merge([st for (_, st), si in zip(g, s) if si], [si for si in s if si])
            out = mcache[key]
            if d == 2:
                nxt.append((None, out))
            else:
                pr, sts = law(out)
                lam = sample(pr)
                nxt.append((lam, sts[lam]))
        level = nxt
    samples = [sample(eng.readout(st)) for _, st in level]
    got = rref(nullspace(samples, cfg.m, p), p)
    return {"recovered": got == rref(inst.log_h, p), "terminal_samples": len(samples),
            "oracle_queries": len(cfg.points)*n_top, **dict(stats)}


# ====================================================================== CLI

def main():
    ap = argparse.ArgumentParser(description="coherent labels on the class-four filiform algebra over F_7")
    ap.add_argument("--out", required=True)
    ap.add_argument("--parts", default="counts,macros,proofs,sde,blocks,mutants,state,runs")
    ap.add_argument("--per-label", type=int, default=4096, help="grade-4 block: (x, q) samples per label triple")
    ap.add_argument("--random-sde", type=int, default=1 << 22, help="random label tuples for U_SDE at grades 3, 2")
    ap.add_argument("--tuples", type=int, default=64, help="state checks: sampled label tuples per sampled grade")
    ap.add_argument("--max-all", type=int, default=400)
    ap.add_argument("--state-instances", default="")
    ap.add_argument("--run-instances", default="")
    ap.add_argument("--paths", type=int, default=256)
    args = ap.parse_args()
    parts = set(args.parts.split(","))
    res = {**STATUS, "parts": sorted(parts), "args": vars(args)}
    t0 = time.time()
    cfg = config()
    res["config"] = cfg.name()

    def dump():
        with open(args.out, "w") as fh:
            json.dump(res, fh, indent=1, default=str)

    blks = blocks(cfg)
    if "counts" in parts:
        res["counts"] = counts_report(cfg)
        log("counts", res["counts"]["terminal_sample"]["total"]["gates"], res["counts"]["terminal_sample"]["qubits"],
            round(time.time()-t0, 1))
        dump()
    if "macros" in parts:
        res["macros"] = macro_checks(blks)
        log("macros", res["macros"]["all_ok"], res["macros"]["used_all_checked"], round(time.time()-t0, 1))
        dump()
    if "proofs" in parts:
        res["proofs"] = {}
        for d, blk in blks.items():
            res["proofs"][f"d{d}"] = {"controlled_merge": C.prove_controlled_merge(blk),
                                      "structure": C.block_structure(blk)}
            log("proof", d, res["proofs"][f"d{d}"]["controlled_merge"]["proved"], round(time.time()-t0, 1))
            dump()
    if "sde" in parts:
        res["sde"] = {}
        res["sde"]["d4_all_label_triples"] = sde_check(blks[4], all_label_tuples(P, 1, 3))
        log("sde d4", res["sde"]["d4_all_label_triples"], round(time.time()-t0, 1))
        g3 = C.flatten(blks[3].U, P, blks[3].anc)
        res["sde"]["d3_all_rank_le1"] = sde_check(blks[3], rank_le1_tuples(P, 2, 6), gates=g3)
        log("sde d3 rank<=1", res["sde"]["d3_all_rank_le1"], round(time.time()-t0, 1))
        dump()
        res["sde"]["d3_random"] = sde_check(blks[3], random_label_tuples(P, 2, 6, args.random_sde, 31), gates=g3)
        res["sde"]["d3_structured"] = sde_check(blks[3], structured_tuples(cfg, 3, 1 << 14, 32), gates=g3)
        log("sde d3", res["sde"]["d3_random"]["passed"], res["sde"]["d3_structured"]["passed"],
            round(time.time()-t0, 1))
        del g3
        dump()
        g2 = C.flatten(blks[2].U, P, blks[2].anc)
        res["sde"]["d2_random"] = sde_check(blks[2], random_label_tuples(P, 3, 10, args.random_sde//4, 21), gates=g2)
        res["sde"]["d2_structured"] = sde_check(blks[2], structured_tuples(cfg, 2, 1 << 14, 22), gates=g2)
        res["sde"]["d2_rank_le1_sampled"] = sde_check(
            blks[2], random_rank_le1_tuples(P, 3, 10, 1 << 14, 23), gates=g2)
        log("sde d2", res["sde"]["d2_random"]["passed"], res["sde"]["d2_structured"]["passed"],
            res["sde"]["d2_rank_le1_sampled"]["passed"], round(time.time()-t0, 1))
        del g2
        dump()
    if "rref" in parts:
        res["rref"] = {"d3_sde_all_row_spaces": sde_check_rref(blks[3], log_fn=log)}
        log("sde rref", res["rref"]["d3_sde_all_row_spaces"], round(time.time()-t0, 1))
        dump()
        res["rref"]["d3_block_all_row_spaces"] = block_check_rref(blks[3], 47, log_fn=log)
        log("block rref", res["rref"]["d3_block_all_row_spaces"], round(time.time()-t0, 1))
        dump()
    if "blocks" in parts:
        res["blocks"] = {}
        gl = blks[4].flatten()
        res["blocks"]["d4_all_label_triples"] = block_check_labels(
            blks[4], repeat_labels(all_label_tuples(P, 1, 3), args.per_label), 41, gates=gl, log_fn=log)
        del gl
        dump()
        gl = blks[3].flatten()
        res["blocks"]["d3_all_rank_le1"] = block_check_labels(blks[3], rank_le1_tuples(P, 2, 6), 42, gates=gl,
                                                              log_fn=log)
        dump()
        res["blocks"]["d3_random"] = block_check_labels(blks[3], random_label_tuples(P, 2, 6, 1 << 18, 43), 43,
                                                        gates=gl)
        res["blocks"]["d3_structured"] = block_check_labels(blks[3], structured_tuples(cfg, 3, 4096, 44), 44, gates=gl)
        del gl
        dump()
        gl = blks[2].flatten()
        res["blocks"]["d2_structured"] = block_check_labels(blks[2], structured_tuples(cfg, 2, 4096, 45), 45, gates=gl)
        res["blocks"]["d2_random"] = block_check_labels(blks[2], random_label_tuples(P, 3, 10, 1 << 16, 46), 46,
                                                        gates=gl)
        del gl
        log("blocks", {k: v["passed"] for k, v in res["blocks"].items()}, round(time.time()-t0, 1))
        dump()
    if "mutants" in parts:
        res["mutants"] = block_mutants(cfg)
        log("mutants", res["mutants"], round(time.time()-t0, 1))
        dump()
    if "paths" in parts:
        res["assembled_basis_paths"] = basis_paths_checked(K.TerminalSampleK(cfg), n=args.paths, seed=20261104)
        log("paths", res["assembled_basis_paths"], round(time.time()-t0, 1))
        dump()
        res["assembled_mutants"] = assembled_mutants(cfg)
        log("assembled mutants", res["assembled_mutants"], round(time.time()-t0, 1))
        dump()
    if "state" in parts or "runs" in parts:
        eng = SourceFromKernel(cfg)
        wit = {d: C.CircuitWitness(blk) for d, blk in blks.items()}
        insts = instances()
    if "state" in parts:
        rows = []
        res["state"] = {"rows": rows}
        rng = random.Random(20261104)
        sel = [int(x) for x in args.state_instances.split(",") if x] or range(len(insts))
        for i in sel:
            t1 = time.time()
            rows.append(state_checks(cfg, insts[i], eng, wit, rng, tuples=args.tuples, max_all=args.max_all,
                                     log_fn=log))
            rows[-1]["seconds"] = round(time.time()-t1, 1)
            log("state", insts[i].name, rows[-1]["passed"], rows[-1]["seconds"])
            dump()
        res["state"]["all_pass"] = all(r["passed"] for r in rows)
        dump()
    if "runs" in parts:
        runs = []
        res["runs"] = {"rows": runs}
        sel = [int(x) for x in args.run_instances.split(",") if x] or range(len(insts))
        for i in sel:
            for seed in SEEDS:
                t1 = time.time()
                r = run_seeded(cfg, insts[i], eng, wit, seed=seed)
                runs.append({"instance": insts[i].name, "normal": bool(insts[i].normal), "seed": seed, **r,
                             "seconds": round(time.time()-t1, 1)})
                log("run", insts[i].name, seed, r["recovered"], runs[-1]["seconds"])
                dump()
        res["runs"]["all_recovered"] = all(r["recovered"] for r in runs)
        dump()
    res["seconds"] = round(time.time()-t0, 1)
    dump()
    log("done", res["seconds"])


if __name__ == "__main__":
    main()

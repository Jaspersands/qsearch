"""Fifth backend: coherent-label Rees receiver with a kappa_d = 3 grade (n4(F_7)).

AI-checked, pending human review. Report:
research/audits/reviews/2026-11-04-rees-circuit-coherent-k3.md.

Instance: the class-three filiform algebra n4 ([e1,e2] = e3, [e1,e3] = e4) over
F_7. Its graded cover has dims (4, 2, 1); grade 3 has kappa_3 = gcd(3, 6) = 3
and label dimension g_3 = 1, grade 2 has kappa_2 = 2 and g_2 = 2. The fourth
backend (theorems/rees_circuit_coherent.py) refuses kappa >= 3; this module
supplies the kappa = 3 coherent witness circuit
(theorems/rees_coherent_sde_kappa.CoherentSDEKappa, the triangular solver of
lem:coherent-power-sde) at grade 3 and the kappa = 2 circuit
(theorems/rees_coherent_sde_k2.CoherentSDEK2) at grade 2. Merge arities:
(g_d+1)(g_d+2)/2 at kappa_d >= 2, i.e. M_3 = 3 (CW arity 4) and M_2 = 6
(CW arity 5); g_d+1 at kappa_d = 1.

No existing file is edited. The merge block, terminal-sample assembly, block
checks, symbolic merge proof, wiring check and per-merge Engine checks are
the fourth backend's code, imported read-only. That code chooses the SDE
circuit and its reference witness through three module-level functions
(sde_circuit, sde_reference, coherent_arity). kappa_dispatch() is a scoped
override of exactly these three names: kappa <= 2 delegates to the original
functions (so Heis(F_3) and n4(F_5) are unchanged, test_k12_delegation),
kappa >= 3 builds CoherentSDEKappa and uses canonical_witness_kappa_batch
(an independent reference written from the definition). The override is
entered only while a block or terminal sample is constructed or a check that
reads the reference runs, and is always restored (test_dispatch_restored).

Checks (all exact): block_check (bit-sliced, every wire of a merge block:
labels/Q unchanged, x_i = x_i * (-delta_(s_i)(sigma(q))) with s the canonical
witness of the independent reference, S and every workspace wire 0),
sde_exhaustive (U_SDE inside the block on all 7^3 grade-3 label triples),
prove_controlled_merge (symbolic replay over F_7[s, q, x] against the
classical BCH polynomial), assembled_basis_paths (wiring of the assembled
terminal sample), state_checks (Engine, exact Z[zeta_7] states, witnesses
from the coherent SDE gate lists: every merged output equals rho_(H_(d-1))),
run_coherent_witness (seeded runs from oracle access).

NOT done: a monolithic statevector or a module-by-module amplitude simulation
of the whole terminal sample (only the merges, through the Engine, by the
deferred-measurement theorem of the fourth backend's report), QFT_p synthesis,
oracle cost, noise, layout, other instances. No claim gate is flipped:
coherent_receiver_implemented stays False in
research/reductions/rees_hsp_reduction.json.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from fractions import Fraction
from itertools import product
import json
import random
import time

import numpy as np

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_general as G
from theorems.rees_coherent_sde import CoherentSDE, Macro, Prog
from theorems.rees_coherent_sde_k2 import CoherentSDEK2, columns
from theorems.rees_coherent_sde_kappa import CoherentSDEKappa, canonical_witness_kappa_batch, kappa_constants
from theorems.rees_end_to_end_sim import filiform4, nullspace, span_elements

STATUS = {"status": "coherent_label_receiver_backend_kappa3_grade_finite_checks",
          "scope": "n4(F_7) only: grade 3 kappa_3 = 3 (triangular arity 3), grade 2 kappa_2 = 2 (arity 6)",
          "coherent_receiver_implemented": False,
          "coherent_label_backend_kappa3_instance": True,
          "general_instances": False, "qft_synthesised": False,
          "whole_circuit_amplitude_simulation": False,
          "independent_review": False, "speedup_claim_allowed": False,
          "review": "AI-checked, pending human review"}

_ORIG = {"sde_circuit": C.sde_circuit, "sde_reference": C.sde_reference, "coherent_arity": C.coherent_arity}
MACRO_KINDS = {"add_product", "add_scaled"}


# ====================================================================== kappa dispatch

def kappa(p, d):
    return C.kappa(p, d)


def coherent_arity_k(p, g, d):
    """Columns of the coherent SDE circuit at grade d: g+1 (kappa 1), (g+1)(g+2)/2 (kappa >= 2)."""
    return g+1 if kappa(p, d) == 1 else columns(g)


def sde_circuit_k(p, g, d, mutate=None):
    """kappa 1 / 2: the fourth backend's choice (CoherentSDE / CoherentSDEK2);
    kappa >= 3: CoherentSDEKappa (raises if p is in E_2(kappa))."""
    if kappa(p, d) <= 2:
        if mutate:
            raise ValueError("SDE mutations are only wired for kappa >= 3")
        return _ORIG["sde_circuit"](p, g, d)
    return CoherentSDEKappa(p, g, d, mutate=mutate)


def sde_reference_k(p, d, A):
    """Canonical witness of the coherent SDE circuit; A (N, g, M)."""
    if kappa(p, d) <= 2:
        return _ORIG["sde_reference"](p, d, A)
    return canonical_witness_kappa_batch(p, A, d)[0]


@contextmanager
def kappa_dispatch(sde_mutate=None):
    """Scoped override of the fourth backend's three dispatch functions."""
    for name in _ORIG:
        if not callable(getattr(C, name, None)):
            raise RuntimeError(f"rees_circuit_coherent.{name} missing: interface changed")
    saved = {name: getattr(C, name) for name in _ORIG}
    C.sde_circuit = (lambda p, g, d: sde_circuit_k(p, g, d, sde_mutate))
    C.sde_reference = sde_reference_k
    C.coherent_arity = coherent_arity_k
    try:
        yield
    finally:
        for name, fn in saved.items():
            setattr(C, name, fn)


def coherent_config_k(alg):
    cfg0 = G.Config(alg)
    ar = {d: coherent_arity_k(cfg0.p, cfg0.dims[d-1], d) for d in range(2, cfg0.c+1)}
    return G.Config(alg, arities=ar)


def job_config(job):
    if job == "n4_f7":
        return coherent_config_k(filiform4(7))
    return C.job_config(job)


def _check_macro_kinds(prog):
    kinds = {it.kind for it in prog if isinstance(it, Macro)}
    if not kinds <= MACRO_KINDS:
        raise AssertionError(f"unexpected macro kinds {kinds - MACRO_KINDS}")


class MergeBlockK(C.MergeBlock):
    """The fourth backend's MergeBlock with the kappa >= 3 SDE circuit allowed.
    sde_mutate: test hook passed to CoherentSDEKappa (kappa >= 3 grades only)."""

    def __init__(self, cfg, d, mutate=None, sde_mutate=None):
        with kappa_dispatch(sde_mutate):
            super().__init__(cfg, d, mutate)
        _check_macro_kinds(self.prog)


class TerminalSampleK(C.TerminalSample):
    def __init__(self, cfg):
        with kappa_dispatch():
            super().__init__(cfg)
        _check_macro_kinds(Prog(it for _, it in self.items if isinstance(it, Macro)))


def _dispatched(fn):
    def wrapper(*a, **k):
        with kappa_dispatch():
            return fn(*a, **k)
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


block_check = _dispatched(C.block_check)
block_sampled = _dispatched(C.block_sampled)
block_exhaustive = _dispatched(C.block_exhaustive)
sde_exhaustive = _dispatched(C.sde_exhaustive)
assembled_basis_paths = _dispatched(C.assembled_basis_paths)
prove_controlled_merge = C.prove_controlled_merge
block_structure = C.block_structure
prog_counts = C.prog_counts
CircuitWitness = C.CircuitWitness
run_coherent_witness = C.run_coherent_witness
measured_counts = C.measured_counts


# ====================================================================== bit-level block inputs

def all_labels_sampled_rest(block, per_label, seed):
    """Every canonical label tuple (p^(M g)), each with per_label random (x_1..x_M, q)."""
    p, M, g = block.p, block.M, block.g
    lam = np.array(list(product(range(p), repeat=M*g)), dtype=np.int64).reshape(-1, M, g)
    L = np.repeat(lam, per_label, axis=0)
    rng = np.random.default_rng(seed)
    xs = rng.integers(0, p, size=(len(L), M, block.nx))
    qv = rng.integers(0, p, size=(len(L), block.nq))
    return L, xs, qv


def all_q_fixed_labels(block, label_tuples, seed):
    """All p^nq values of q for each given label tuple, random children."""
    cfg = block.cfg
    Qe = cfg.laws[block.d-1].elements()
    lam = np.asarray(label_tuples, dtype=np.int64).reshape(-1, block.M, block.g)
    L = np.repeat(lam, len(Qe), axis=0)
    qv = np.tile(Qe, (len(lam), 1))
    xs = np.random.default_rng(seed).integers(0, block.p, size=(len(L), block.M, block.nx))
    return L, xs, qv


def all_lambda_q_check(block, chunk=1 << 16, seed=0, start=0, stop=None, log=None):
    """block_check on ALL (lambda, q): p^(M g) label tuples times p^nq values of q
    (grade 3 of n4(F_7): 343 * 7^6 = 40 353 607 inputs), one random child tuple per
    input (seeded per chunk); inputs generated chunk by chunk (bounded memory)."""
    p, M, g, nq = block.p, block.M, block.g, block.nq
    nQ = p**nq
    total = p**(M*g)*nQ
    stop = total if stop is None else min(stop, total)
    gates = block.flatten()
    Qe = block.cfg.laws[block.d-1].elements()
    agg = None
    t0 = time.time()
    for a in range(start, stop, chunk):
        idx = np.arange(a, min(stop, a+chunk), dtype=np.int64)
        li, qi = idx // nQ, idx % nQ
        lam = np.zeros((len(idx), M*g), dtype=np.int64)
        r = li.copy()
        for t in range(M*g-1, -1, -1):
            lam[:, t] = r % p
            r //= p
        lam = lam.reshape(-1, M, g)
        xs = np.random.default_rng([seed, a]).integers(0, p, size=(len(idx), M, block.nx))
        f = block_check(block, lam, xs, Qe[qi], gates=gates, chunk=chunk)
        if agg is None:
            agg = dict(f)
        else:
            for k, v in f.items():
                if isinstance(v, bool):
                    agg[k] = agg[k] and v
            agg["inputs"] += f["inputs"]
        if log and (a//chunk) % 32 == 0:
            log(f"  all (lam, q) d={block.d} {min(stop, a+chunk)}/{stop} ok={agg['passed'] and f['passed']} "
                f"{time.time()-t0:.0f}s")
    agg["passed"] = all(v for k, v in agg.items() if isinstance(v, bool))
    agg["sim_seconds"] = round(time.time()-t0, 1)
    agg["index_range"] = [start, stop]
    agg["total_inputs_all_lambda_q"] = total
    return agg


def chunked_block_check(block, lam, xs, qv, chunk=1 << 15, gates=None, log=None):
    """block_check over chunks (bounded memory); flags AND-ed."""
    gates = block.flatten() if gates is None else gates
    agg = None
    t0 = time.time()
    for a in range(0, len(qv), chunk):
        sl = slice(a, a+chunk)
        f = block_check(block, lam[sl], xs[sl], qv[sl], gates=gates, chunk=chunk)
        if agg is None:
            agg = dict(f)
        else:
            for k, v in f.items():
                if isinstance(v, bool):
                    agg[k] = agg[k] and v
            agg["inputs"] += f["inputs"]
        if log:
            log(f"  block d={block.d} {min(len(qv), a+chunk)}/{len(qv)} ok={agg['passed']} {time.time()-t0:.0f}s")
    agg["passed"] = all(v for k, v in agg.items() if isinstance(v, bool))
    agg["sim_seconds"] = round(time.time()-t0, 1)
    return agg


# ====================================================================== per-merge exact state checks

def state_checks(cfg, inst, eng, witnesses, rng, grade2_tuples=12, max_all=400, log=None):
    """C.n4_state_checks with bounded memory (no per-(label, s) factor cache;
    merge outcomes cached by the multiset of active (label, s) pairs, on which
    the Engine's merge depends only). Per merge, exact (Engine, Z[zeta_p]):
    ALL positive-probability label tuples when there are <= max_all of them
    (grade 3 of n4(F_7): at most 7^3 = 343), else sampled (the all-zero tuple,
    a constant tuple and random ones); the witness of every merge is the output
    of the coherent SDE gate list; every merged output must equal
    rho_(H_(d-1)); then the readout law must be uniform on h^perp."""
    p = cfg.p
    row = {"instance": inst.name, "grades": {}}
    st, S, sinfo = eng.source(inst)
    ok = bool(sinfo["coset_state"]) and np.array_equal(np.sort(S), G.stage_indices(cfg, inst.log_h, cfg.c))
    for d in range(cfg.c, 1, -1):
        t0 = time.time()
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
        good = valid = 0
        cache = {}
        for lams, s in zip(tuples, ws):
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
        row["grades"][d] = {"arity": M, "label_support": len(allowed), "tuples": mode, "cases": len(tuples),
                            "distinct_merges": len(cache), "witness_valid": valid == len(tuples),
                            "outputs_equal_rho_H": good == len(tuples), "seconds": round(time.time()-t0, 1)}
        ok = ok and valid == len(tuples) and good == len(tuples)
        if log:
            log(f"  {inst.name} grade {d}: {row['grades'][d]}")
        v = np.zeros((cfg.laws[d-1].order, p), dtype=np.int64)
        v[target, 0] = 1
        st = G.XState(d-1, Fraction(1), v)
        del states
    pr = eng.readout(st)
    h_perp = {tuple(int(x) for x in r) for r in span_elements(nullspace(inst.log_h, cfg.m, p), cfg.m, p)}
    row["readout_uniform_on_h_perp"] = set(pr) == h_perp and all(v == Fraction(1, len(h_perp)) for v in pr.values())
    row["passed"] = bool(ok and row["readout_uniform_on_h_perp"])
    return row


# ====================================================================== counts

def counts_report(job="n4_f7"):
    cfg = job_config(job)
    ts = TerminalSampleK(cfg)
    out = {"config": cfg.name(), "terminal_sample": ts.counts(), "structure": ts.structure(), "blocks": {}}
    for d, blk in ts.blocks.items():
        out["blocks"][d] = {"kappa": kappa(cfg.p, d), "arity": blk.M, "label_dim": blk.g,
                            "sde_class": type(blk.sde).__name__, "sde_qubits": blk.sde.nw, "qubits": blk.qubits(),
                            "segments": blk.segment_counts(), "structure": block_structure(blk)}
    out["measured_generator_cw_arity"] = measured_counts(cfg.algebra)
    out["measured_generator_coherent_arity"] = measured_counts(cfg.algebra, arities=dict(cfg.arity))
    return out


# ====================================================================== CLI

SEEDS = (20261103, 20261104)


def main():
    ap = argparse.ArgumentParser(description="fifth backend: coherent labels with a kappa = 3 grade, n4(F_7)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--parts", default="counts,proofs,blocks,paths,state,runs")
    ap.add_argument("--per-label", type=int, default=256, help="grade-3 block: (x, q) samples per label triple")
    ap.add_argument("--grade2-tuples", type=int, default=64)
    ap.add_argument("--max-all", type=int, default=400, help="state checks: all label tuples up to this many")
    ap.add_argument("--state-instances", default="", help="indices into n4_instances(7) (default all)")
    ap.add_argument("--run-instances", default="0,1,2,3,7,8", help="indices into n4_instances(7) for seeded runs")
    ap.add_argument("--all-lambda-q", action="store_true",
                    help="grade-3 block on ALL 343 * 7^6 (lambda, q), random children (~15 min)")
    args = ap.parse_args()
    parts = set(args.parts.split(","))
    log = lambda *a: print(*a, flush=True)
    res = {**STATUS, "parts": sorted(parts), "args": vars(args)}
    t0 = time.time()
    cfg = job_config("n4_f7")
    res["config"] = cfg.name()
    res["kappa_constants_grade3"] = {k: v for k, v in kappa_constants(7, 3).items()}

    def dump():
        with open(args.out, "w") as fh:
            json.dump(res, fh, indent=1, default=str)

    blocks = {d: MergeBlockK(cfg, d) for d in (2, 3)}
    if "counts" in parts:
        res["counts"] = counts_report("n4_f7")
        log("counts", res["counts"]["terminal_sample"]["total"]["gates"], res["counts"]["terminal_sample"]["qubits"],
            round(time.time()-t0, 1))
        dump()
    if "proofs" in parts:
        res["proofs"] = {}
        for d, blk in blocks.items():
            res["proofs"][f"d{d}"] = {"controlled_merge": prove_controlled_merge(blk),
                                      "structure": block_structure(blk)}
        res["proofs"]["d3"]["sde_exhaustive"] = sde_exhaustive(blocks[3])
        log("proofs", {k: v["controlled_merge"]["proved"] for k, v in res["proofs"].items()},
            res["proofs"]["d3"]["sde_exhaustive"], round(time.time()-t0, 1))
        dump()
    if "blocks" in parts:
        res["blocks"] = {}
        b3 = blocks[3]
        g3 = b3.flatten()
        L, xs, qv = all_labels_sampled_rest(b3, args.per_label, seed=20261104)
        res["blocks"]["d3_all_label_triples"] = chunked_block_check(b3, L, xs, qv, gates=g3, log=log)
        dump()
        L, xs, qv = all_q_fixed_labels(b3, [[[3], [5], [1]], [[0], [2], [4]]], seed=5)
        res["blocks"]["d3_all_q_two_label_triples"] = chunked_block_check(b3, L, xs, qv, gates=g3, log=log)
        dump()
        res["blocks"]["d3_structured"] = block_sampled(b3, n=4096, seed=20261104, gates=g3)
        del g3
        res["blocks"]["d2_structured"] = block_sampled(blocks[2], n=4096, seed=20261104)
        log("blocks", {k: v["passed"] for k, v in res["blocks"].items()}, round(time.time()-t0, 1))
        dump()
    if args.all_lambda_q:
        res["d3_all_lambda_q"] = all_lambda_q_check(blocks[3], seed=20261104, log=log)
        log("all (lam, q)", res["d3_all_lambda_q"]["passed"], round(time.time()-t0, 1))
        dump()
    if "paths" in parts:
        res["assembled_basis_paths"] = assembled_basis_paths(TerminalSampleK(cfg), n=512, seed=20261104)
        log("paths", res["assembled_basis_paths"]["passed"], round(time.time()-t0, 1))
        dump()
    eng = None
    if "state" in parts or "runs" in parts:
        eng = G.Engine(cfg)
        wit = {d: CircuitWitness(blk) for d, blk in blocks.items()}
        insts = G.n4_instances(7)
    if "state" in parts:
        rng = random.Random(20261104)
        rows = []
        res["state"] = {"rows": rows}
        sel = [int(x) for x in args.state_instances.split(",") if x] or range(len(insts))
        for inst in [insts[i] for i in sel]:
            t1 = time.time()
            rows.append(state_checks(cfg, inst, eng, wit, rng, grade2_tuples=args.grade2_tuples,
                                     max_all=args.max_all, log=log))
            rows[-1]["seconds"] = round(time.time()-t1, 1)
            log("state", inst.name, rows[-1]["passed"], rows[-1]["seconds"])
            dump()
        res["state"]["all_pass"] = all(r["passed"] for r in rows)
        dump()
    if "runs" in parts:
        runs = []
        res["runs"] = {"rows": runs}
        for i in [int(x) for x in args.run_instances.split(",") if x]:
            inst = insts[i]
            for seed in SEEDS:
                t1 = time.time()
                r = run_coherent_witness(cfg, inst, eng, wit, seed=seed)
                runs.append({"instance": inst.name, "seed": seed, **r, "seconds": round(time.time()-t1, 1)})
                log("run", inst.name, seed, r["recovered"], runs[-1]["seconds"])
                dump()
        res["runs"]["all_recovered"] = all(r["recovered"] for r in runs)
        dump()
    res["seconds"] = round(time.time()-t0, 1)
    dump()
    log("done", res["seconds"])


if __name__ == "__main__":
    main()

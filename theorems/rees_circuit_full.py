"""One gate-level circuit per terminal sample for Heis(F_3) and n4(F_5):
explicit QFT (lem:qft-mod) + coherent labels. AI-checked, pending human review.

Report: research/audits/reviews/2026-11-04-rees-circuit-full.md.
New file; imports read-only: rees_circuit_coherent (TerminalSample, flatten,
footprints, witness references), rees_circuit_qft_wire (pool size, sparse
float simulator CircuitState), rees_qft_mod (the gate list of lem:qft-mod,
params_for_eta, error_bound), rees_circuit_general (configs, instances,
qft_matrix). No existing file is edited.

The circuit. FullTerminalSample(cfg, (t, r, tp)) takes the assembled coherent
terminal sample (nothing measured before the final readout of the root Q) and
replaces every qft item by rees_qft_mod.qft_mod_ops(p, t, r, tp) and every
qft_dg item by its inverse, relabelled: lemma register X -> the called
b-wire register (LSB first); F, Z, K, M, W, a (4b+2t+1) -> the QFT pool;
the lemma's 3b+5 arithmetic ancillas -> the terminal sample's arith_ancilla
register (same Anc layout). Macros are expanded with the rees_circuit_arith
gate lists. Gates: X, CX, CCX, SWAP, H, R_k^(+-1) = Phase(+-2pi/2^k),
CR_k^(+-1); plus the (uncounted) oracle calls and ONE final measurement.

Ancilla sharing. layout="overlay" (default) puts the QFT pool on the first
4b+2t+1 wires of the coherent block_workspace_pool (witness S, SDE and merge
workspace), fresh wires only for any excess: no qubit is added at the
parameters used here. Soundness (report Section 1): in the exact-transform
circuit those wires are 0 at every transform call (merge blocks return them to
0 on every canonical input; no call lies inside a block; exact transforms do
not touch them), which is all the hybrid argument needs; in the explicit
circuit the residue a transform leaves in the pool is exactly what the bound
charges. layout="separate": the QFT pool on fresh wires (comparison).
layout="mutant_labels" / "mutant_oracle" / "mutant_qudit": test hooks that overlay the pool on
live registers (must be rejected by the checks).

Checks: gate_set_check (every emitted gate, whole list), slice_check (every
transform slice equals the lemma's list under a relabelling rebuilt from the
Layout fields, footprint qudit+pool+ancillas), wire_check (static roles and
footprints), basis_paths (bit-level run of the whole assembled program on
random basis paths: pool and ancillas 0 before EVERY call, every register
against an independent classical recursion), call_error / segment_compare
(float: single emitted transforms on every canonical input; the first source
with its unmeasured instrument; Q preparation + one merge block, explicit vs
exact transforms, all touched wires). Budgets: hybrid_budget, target_params.

What this does NOT do: a monolithic simulation of a whole terminal sample
(explicit or exact); kappa_d >= 3 grades; other instances; a fixed finite
gate set (R_k, k <= max(r, tp), are primitives); the oracle cost; noise. No
claim gate is changed: coherent_receiver_implemented stays False.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import os
import random
import time

import numpy as np

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_general as G
import theorems.rees_circuit_qft_wire as W
import theorems.rees_qft_mod as Q
from theorems.rees_coherent_sde import BitSim, Macro, Prog

STATUS = {"status": "explicit_qft_and_coherent_labels_one_circuit_per_terminal_sample_finite_checks",
          "scope": "Heis(F_3) and n4(F_5) only (every SDE grade has kappa_d <= 2)",
          "full_gate_level_terminal_sample": True,
          "no_mid_circuit_measurement": True,
          "monolithic_simulation": False,
          "fixed_finite_gate_set": False,
          "coherent_receiver_implemented": False, "general_instances": False,
          "kappa_ge3_grades_coherent": False, "independent_review": False,
          "speedup_claim_allowed": False,
          "review": "AI-checked, pending human review"}

GATE_SET = ("x", "cx", "ccx", "swap", "h", "r", "cr")
ARITY = {"x": 1, "cx": 2, "ccx": 3, "swap": 2, "h": 1, "r": 1, "cr": 2}
BLOCK_PREFIXES = ("sde_grade", "witness_control_grade", "bch_merge_grade")
PERM_ITEMS = ("x", "cx", "ccx", "swap", "swapreg")


def is_block(comp):
    return comp.startswith(BLOCK_PREFIXES)


# ====================================================================== parameters and budgets

def n_samples(cfg):
    """Terminal samples per seeded run (m + 4, as in the coherent and qft-wire reports)."""
    return cfg.m+4


def lemma_level_delta(eta, tp, n_zero, n_general):
    """Per-sample bound from the statement of lem:qft-mod as main.tex now words it:
    eta per general call, 3 pi 2^-tau per forward call on input |0>."""
    return n_general*eta+n_zero*3*math.pi*2.0**-tp


def target_params(p, n_zero, n_general, n, cap=0.1):
    """Largest eta with two significant digits for which the lemma-level coupling
    bound n * delta is < cap; parameters from rees_qft_mod.params_for_eta."""
    for e in range(2, 9):
        for k in range(99, 9, -1):
            eta = k/10**(e+1)
            t, r, tp = Q.params_for_eta(p, eta)
            P = n*lemma_level_delta(eta, tp, n_zero, n_general)
            if P < cap:
                return {"eta": eta, "params": (t, min(r, t), tp), "delta_lemma": P/n, "P_lemma": P}
    raise ValueError("no eta found")


def hybrid_budget(calls, p, t, r, tp, eta=None):
    """Proved per-sample bounds for the given call list (dicts with kind, zero):
    'exact_formula': zero-input forward calls cost the exact prep term of
    error_bound, every other call its B; 'lemma': with eta, the statement-level
    bound (eta per general call, 3 pi 2^-tp per zero-input forward call)."""
    bd = Q.error_bound(p, t, r, tp)
    nz = sum(1 for c in calls if c["zero"] and c["kind"] == "qft")
    ng = len(calls)-nz
    out = {"n_calls": len(calls), "zero_input_forward": nz, "general": ng, "B": bd["B"], "prep": bd["prep"],
           "B_simple": bd["B_simple"], "exact_formula": ng*bd["B"]+nz*bd["prep"]}
    if eta is not None:
        out["lemma"] = lemma_level_delta(eta, tp, nz, ng)
    return out


# ====================================================================== the combined circuit

class FullTerminalSample:
    """The coherent terminal sample with every transform expanded into the
    lem:qft-mod gate list (see the module docstring for the layouts)."""

    def __init__(self, cfg, params, layout="overlay", mutate=None):
        self.cfg, self.p = cfg, cfg.p
        self.ts = ts = C.TerminalSample(cfg)
        self.b = b = cfg.enc.nb
        t, r, tp = params
        self.params = (int(t), int(min(r, t)), int(tp))
        t, r, tp = self.params
        self.kmax = max(r, tp)
        self.mutate = set(mutate or ())
        self.npool = W.pool_size(b, t)
        self.nw = ts.nw
        self.role = dict(ts.role)
        self.layout = layout
        if layout == "overlay":
            k = min(self.npool, len(ts.pool))
            pool = list(ts.pool[:k])+self._fresh(self.npool-k)
        elif layout == "separate":
            pool = self._fresh(self.npool)
        elif layout == "mutant_labels":          # test hook: pool on live label registers first
            lab = [w for w in range(ts.nw) if ts.role[w].startswith("label_z")]
            rest = [w for w in ts.pool if w not in lab]
            pool = (lab+rest)[:self.npool]
        elif layout == "mutant_oracle":          # test hook: pool on the (live) oracle output registers first
            ys = [w for w in range(ts.nw) if ts.role[w] == "oracle_output"]
            pool = (ys+list(ts.pool))[:self.npool]
        elif layout == "mutant_qudit":           # test hook: pool contains the first address register
            first = next(it[1][0] for _, it in ts.items if not isinstance(it, Macro) and it[0] == "qft")
            pool = (list(first)+list(ts.pool))[:self.npool]
        else:
            raise ValueError(layout)
        if len(pool) != self.npool:
            raise ValueError("pool too small for this layout")
        self.pool = pool
        self.anc = list(ts.anc.all)
        fwd, L, _ = Q.qft_mod_ops(self.p, t, r, tp, False)
        inv, _, _ = Q.qft_mod_ops(self.p, t, r, tp, True)
        self.L = L
        if L.nq != b+self.npool+len(self.anc):
            raise AssertionError("layout size mismatch")
        self.ref = {"qft": tuple(fwd), "qft_dg": tuple(inv)}
        self.calls, self.call_of_item = [], {}
        seen = set()
        for i, (comp, it) in enumerate(ts.items):
            if not isinstance(it, Macro) and it[0] in ("qft", "qft_dg"):
                reg = tuple(it[1][0])
                self.call_of_item[i] = len(self.calls)
                self.calls.append({"item": i, "component": comp, "kind": it[0], "reg": reg,
                                   "zero": not (set(reg) & seen)})
            seen |= C.touched(it)

    def _fresh(self, n):
        out = list(range(self.nw, self.nw+n))
        self.nw += n
        for w in out:
            self.role[w] = "qft_pool"
        return out

    # -- emission
    def qubit_map(self, reg):
        """lemma layout index -> wire, for a call on register reg (X, then pool F..a, then arith)."""
        return list(reg)+list(self.pool)+list(self.anc)

    def slice(self, ci):
        c = self.calls[ci]
        qm = self.qubit_map(c["reg"])
        out = [(g[0], tuple(qm[i] for i in g[1]), *g[2:]) for g in self.ref[c["kind"]]]
        if "rotation" in self.mutate and ci == 0:      # test hook: one rotation angle changed
            j = next(k for k, g in enumerate(out) if g[0] == "r")
            g = out[j]
            out[j] = (g[0], g[1], g[2]+1, g[3])
        if "footprint" in self.mutate and ci == 0:     # test hook: one gate moved outside the footprint
            j = next(k for k, g in enumerate(out) if g[0] == "x")
            out[j] = ("x", (self.ts.w[0][0],))
        return out

    def segments(self):
        """Circuit order: ('perm', comp, gates) per permutation item (macros
        expanded), ('qft', comp, (call index, gates)), ('oracle', comp, item),
        ('measure', comp, item)."""
        p, anc = self.p, self.ts.anc
        for i, (comp, it) in enumerate(self.ts.items):
            if isinstance(it, Macro) or it[0] in PERM_ITEMS:
                yield "perm", comp, C.flatten(Prog([it]), p, anc)
            elif it[0] in ("qft", "qft_dg"):
                ci = self.call_of_item[i]
                yield "qft", comp, (ci, self.slice(ci))
            elif it[0] == "oracle":
                yield "oracle", comp, it
            elif it[0] == "measure":
                yield "measure", comp, it
            else:
                raise ValueError(it[0])

    def iter_gates(self):
        """Every emitted gate except the oracle calls and the final measurement."""
        for kind, _, pay in self.segments():
            if kind == "perm":
                yield from pay
            elif kind == "qft":
                yield from pay[1]

    def call_summary(self):
        by = Counter((c["component"], c["kind"], "zero" if c["zero"] else "general") for c in self.calls)
        return {"calls": len(self.calls), "zero_input_forward": sum(1 for c in self.calls if c["zero"] and
                                                                    c["kind"] == "qft"),
                "zero_input_inverse": sum(1 for c in self.calls if c["zero"] and c["kind"] == "qft_dg"),
                "general": sum(1 for c in self.calls if not c["zero"]),
                "by_component": {f"{a}/{b}/{z}": v for (a, b, z), v in sorted(by.items())}}


# ====================================================================== exact checks on the emitted list

def gate_set_check(fts):
    """Every emitted gate (whole list, streamed): name in GATE_SET, right arity,
    distinct wires inside the circuit; R/CR with integer 1 <= k <= max(r, tp) and
    sign +-1. Exactly one measurement, last, of the root Q. Counts by component
    and gate type (exact counts of the emitted list)."""
    nw, kmax = fts.nw, fts.kmax
    by = {}
    flags = {"gate_set_ok": True, "arity_ok": True, "wires_ok": True, "rotation_params_ok": True}
    ks = Counter()
    used = set()
    seg_kinds = []
    for kind, comp, pay in fts.segments():
        seg_kinds.append(kind)
        if kind in ("oracle", "measure"):
            if kind == "measure":
                flags["measured_registers"] = [list(r) for r in pay[1]]
            by.setdefault(comp, Counter())[kind+"_items"] += 1
            continue
        gates = pay if kind == "perm" else pay[1]
        cnt = by.setdefault(comp, Counter())
        if kind == "qft":
            cnt["qft_calls"] += 1
        for g in gates:
            nm = g[0]
            if nm not in ARITY:
                flags["gate_set_ok"] = False
                continue
            ws = g[1]
            if len(ws) != ARITY[nm] or len(set(ws)) != len(ws):
                flags["arity_ok"] = False
            if any(not (0 <= w < nw) for w in ws):
                flags["wires_ok"] = False
            if nm in ("r", "cr"):
                if len(g) != 4 or not isinstance(g[2], int) or not (1 <= g[2] <= kmax) or g[3] not in (1, -1):
                    flags["rotation_params_ok"] = False
                ks[(nm, g[2], g[3])] += 1
            elif len(g) != 2:
                flags["arity_ok"] = False
            used.update(ws)
            cnt[nm] += 1
    meas = [i for i, k in enumerate(seg_kinds) if k == "measure"]
    flags["single_measurement_at_end"] = meas == [len(seg_kinds)-1]
    flags["measured_register_is_root_Q"] = flags.get("measured_registers") == [list(q) for q in fts.ts.root]
    tot = Counter()
    for c in by.values():
        tot.update(c)
    for c in list(by.values())+[tot]:
        c["gates"] = sum(c[k] for k in GATE_SET)
    flags["passed"] = all(v for k, v in flags.items() if isinstance(v, bool))
    return {**flags, "by_component": {k: dict(v) for k, v in sorted(by.items())}, "total": dict(tot),
            "qubits": fts.nw, "qubits_used": len(used),
            "rotations_by_k_sign": {f"{a}{k}{'+' if s > 0 else '-'}": v for (a, k, s), v in sorted(ks.items())},
            "max_rotation_index": max([k for (_, k, _) in ks], default=0)}


def slice_check(fts):
    """Every transform slice equals the lem:qft-mod gate list (rebuilt here from
    rees_qft_mod, not from fts.ref) under the relabelling X -> called register,
    (F, Z, K, M, W, a) -> pool, arithmetic ancillas -> arith_ancilla register,
    built from the Layout fields; gate by gate (name, wires, k, sign). Also:
    footprint inside register + pool + ancillas, which are pairwise disjoint.
    A consistency and mutation check (the reference is the same deterministic
    qft_mod_ops), not an independent derivation of the lemma's circuit."""
    p, b = fts.p, fts.b
    t, r, tp = fts.params
    ref = {False: Q.qft_mod_ops(p, t, r, tp, False), True: Q.qft_mod_ops(p, t, r, tp, True)}
    L = ref[False][1]
    lemma_pool = [*L.F, *L.Z, *L.K, *L.M, *L.W, L.a]
    out = {"slices": 0, "gates_compared": 0, "equal_to_lemma": True, "footprint_ok": True, "disjoint_ok": True,
           "first_failure": None}
    pool, anc = list(fts.pool), list(fts.anc)
    for kind, comp, pay in fts.segments():
        if kind != "qft":
            continue
        ci, gates = pay
        call = fts.calls[ci]
        it = fts.ts.items[call["item"]][1]
        reg = list(it[1][0])                                   # from the coherent item itself
        inverse = it[0] == "qft_dg"
        ops = ref[inverse][0]
        m = {}
        for i, x in enumerate(L.X):
            m[x] = reg[i]
        for i, x in enumerate(lemma_pool):
            m[x] = pool[i]
        for i, x in enumerate(L.anc):
            m[x] = anc[i]
        allowed = set(reg) | set(pool) | set(anc)
        if len(allowed) != len(reg)+len(pool)+len(anc):
            out["disjoint_ok"] = False
        out["slices"] += 1
        if len(gates) != len(ops):
            out["equal_to_lemma"] = False
            out["first_failure"] = out["first_failure"] or (ci, "length")
            continue
        for k, (g, h) in enumerate(zip(gates, ops)):
            want = (h[0], tuple(m[i] for i in h[1]), *h[2:])
            if tuple(g) != want:
                out["equal_to_lemma"] = False
                out["first_failure"] = out["first_failure"] or (ci, k)
            if not set(g[1]) <= allowed:
                out["footprint_ok"] = False
        out["gates_compared"] += len(gates)
    out["passed"] = out["equal_to_lemma"] and out["footprint_ok"] and out["disjoint_ok"]
    return out


def block_runs(ts):
    """Maximal runs [start, stop) of merge-block items (U_SDE .. U_SDE^-1)."""
    runs, start = [], None
    for i, (comp, _) in enumerate(ts.items):
        if is_block(comp):
            if start is None:
                start = i
        elif start is not None:
            runs.append((start, i))
            start = None
    if start is not None:
        runs.append((start, len(ts.items)))
    return runs


def wire_check(fts):
    """Static part of the overlay argument: (a) pool, ancillas and every called
    register pairwise disjoint; pool wires only of role block_workspace_pool or
    qft_pool; (b) outside merge blocks no item touches a pool wire; (c) no
    transform, oracle or measurement inside a merge block, and the number of
    blocks equals the number of merge nodes; (d) zero-input classification
    recomputed from the emitted stream equals the item-level one."""
    ts, cfg = fts.ts, fts.cfg
    pool, anc = set(fts.pool), set(fts.anc)
    flags = {}
    flags["pool_and_ancillas_disjoint"] = not (pool & anc) and len(pool) == len(fts.pool)
    flags["called_registers_disjoint_from_pool_and_ancillas"] = all(not (set(c["reg"]) & (pool | anc))
                                                                   for c in fts.calls)
    flags["pool_roles"] = sorted({fts.role[w] for w in pool})
    flags["pool_roles_ok"] = set(flags["pool_roles"]) <= {"block_workspace_pool", "qft_pool"}
    runs = block_runs(ts)
    inside = set()
    for a, b in runs:
        inside.update(range(a, b))
    flags["pool_untouched_outside_blocks"] = all(not (C.touched(it) & pool)
                                                 for i, (_, it) in enumerate(ts.items) if i not in inside)
    flags["no_call_oracle_or_measure_inside_blocks"] = all(
        isinstance(ts.items[i][1], Macro) or ts.items[i][1][0] in PERM_ITEMS for i in inside)
    N = G.sources_per_grade(cfg)
    flags["blocks"] = len(runs)
    flags["blocks_equal_merge_nodes"] = len(runs) == sum(N[d-1] for d in range(2, cfg.c+1))
    # (d) zero-input from the emitted stream (wires touched by earlier emitted gates)
    seen, zero = set(), []
    for kind, comp, pay in fts.segments():
        if kind == "qft":
            ci, gates = pay
            reg = set(fts.calls[ci]["reg"])
            zero.append(not (reg & seen))
            for g in gates:
                seen.update(g[1])
        elif kind == "perm":
            for g in pay:
                seen.update(g[1])
        else:
            seen |= C.touched(pay)
    flags["zero_input_from_stream_equals_items"] = zero == [c["zero"] for c in fts.calls]
    flags["every_zero_input_call_is_forward"] = all(c["kind"] == "qft" for c in fts.calls if c["zero"])
    flags["passed"] = all(v for k, v in flags.items() if isinstance(v, bool))
    return flags


def basis_paths(fts, n=256, seed=0):
    """Bit-level run of the whole assembled program on n random basis paths: the
    classical skeleton of the exact-transform circuit (as in rees_circuit_coherent.
    assembled_basis_paths, except for the oracle): a forward transform on a fresh
    register loads a random canonical value, the other transforms are skipped,
    and an oracle call XORs a random value into its output register (so the
    oracle outputs are live, as f(w) makes them). Asserts before EVERY transform
    call that the pool and the arithmetic ancillas are 0 on every path (premise
    (i) of the overlay argument, on this skeleton) and that a zero-input call
    finds its register 0; at the end checks every register against the
    independent classical recursion of the coherent report and the clean
    registers (w, ancillas, block pool, QFT pool) against 0."""
    ts, cfg, p = fts.ts, fts.cfg, fts.p
    rng = np.random.default_rng(seed)
    sim = BitSim(fts.nw, n)
    loaded, buf = {}, Prog()
    check_w = sorted(set(fts.pool) | set(fts.anc))

    def flush():
        if buf:
            sim.run(C.flatten(buf, p, ts.anc))
            buf.clear()
    pre_ok, zero_ok, checked = True, True, 0
    for i, (comp, it) in enumerate(ts.items):
        if isinstance(it, Macro) or it[0] in PERM_ITEMS:
            buf.append(it)
            continue
        flush()
        if it[0] in ("qft", "qft_dg"):
            call = fts.calls[fts.call_of_item[i]]
            pre_ok &= not any(sim.wire_nonzero(w) for w in check_w)
            checked += 1
            if call["zero"]:
                reg = it[1][0]
                zero_ok &= not any(sim.wire_nonzero(w) for w in reg)
                if comp != "final_qft":
                    v = rng.integers(0, p, size=n)
                    sim.load(list(reg), v)
                    loaded[tuple(reg)] = v
            elif it[0] == "qft" and comp != "final_qft":
                raise AssertionError("a forward preparation on a non-fresh register")
        elif it[0] == "oracle":
            y = list(it[1][1])
            sim.load(y, rng.integers(0, 1 << len(y), size=n))
    flush()

    def val(reg):
        return np.stack([loaded[tuple(q)] for q in reg], axis=1)

    def read(reg):
        return np.stack([sim.read(list(q)) for q in reg], axis=1)
    ok = {"pool_and_ancillas_zero_before_every_call": bool(pre_ok), "calls_checked": checked,
          "zero_input_registers_zero": bool(zero_ok), "children_and_Q": True, "labels": True}

    def after_instrument(node):
        x = val(node["reg"])
        if node["z"] is None:
            return x
        z = val(node["z"])
        d = node["d"]
        zf = np.concatenate([np.zeros((n, cfg.width[d]-cfg.dims[d-1]), dtype=np.int64), (-z) % p], axis=1)
        return cfg.laws[d].mul(x, zf)

    def visit(node):
        if not node["kids"]:
            return
        d = node["d"]+1
        blk = ts.blocks[d]
        lam = np.stack([val(k["z"]) for k in node["kids"]], axis=2)
        s = C.sde_reference(p, d, lam)
        qv = val(node["reg"])
        for i, k in enumerate(node["kids"]):
            want = cfg.laws[d].mul(after_instrument(k), C._witness_bound_g(blk, s[:, i], qv))
            ok["children_and_Q"] &= bool(np.array_equal(read(k["reg"]), want))
            ok["labels"] &= bool(np.array_equal(read(k["z"]), val(k["z"])))
            visit(k)
    visit(ts.tree)
    ok["root_Q_unchanged"] = bool(np.array_equal(read(ts.tree["reg"]), val(ts.tree["reg"])))
    clean = [w for w in range(fts.nw) if fts.role[w] in ("arith_ancilla", "evaluation_w", "block_workspace_pool",
                                                         "qft_pool")]
    ok["workspace_clean"] = not any(sim.wire_nonzero(w) for w in clean)
    ok["paths"] = n
    ok["passed"] = all(v for k, v in ok.items() if isinstance(v, bool))
    return ok


# ====================================================================== float simulation

def _compile_local(ops, idx):
    """Full-format ops -> rees_circuit_qft_wire.CircuitState tuples on local indices."""
    wo = lambda w: (idx[w] // 64, idx[w] % 64)
    out = []
    for g in ops:
        nm = g[0]
        if nm in ("x", "h"):
            out.append((nm, *wo(g[1][0])))
        elif nm in ("cx", "swap"):
            out.append((nm, *wo(g[1][0]), *wo(g[1][1])))
        elif nm == "ccx":
            out.append((nm, *wo(g[1][0]), *wo(g[1][1]), *wo(g[1][2])))
        elif nm == "r":
            out.append(("p", *wo(g[1][0]), np.exp(1j*g[3]*2*math.pi/2**g[2])))
        elif nm == "cr":
            out.append(("cp", *wo(g[1][0]), *wo(g[1][1]), np.exp(1j*g[3]*2*math.pi/2**g[2])))
        elif nm == "u":
            out.append(("u", [wo(w) for w in g[1]], g[2]))
        elif nm == "oracle":
            _, wq, wy, table, p, m = g
            out.append(("oracle", [[wo(w) for w in q] for q in wq], [wo(w) for w in wy], table, p, m))
        else:
            raise ValueError(nm)
    return out


def segment_ops(fts, i0, i1, backend, inst=None):
    """Full-format ops of items [i0, i1): transforms explicit (the emitted slice)
    or exact ('u' = qft_matrix on the register); oracle items as table calls."""
    ts, p, b, m = fts.ts, fts.p, fts.b, fts.cfg.m
    out = []
    for i in range(i0, i1):
        comp, it = ts.items[i]
        if isinstance(it, Macro) or it[0] in PERM_ITEMS:
            out.extend(C.flatten(Prog([it]), p, ts.anc))
        elif it[0] in ("qft", "qft_dg"):
            if backend == "explicit":
                out.extend(fts.slice(fts.call_of_item[i]))
            else:
                out.append(("u", tuple(it[1][0]), G.qft_matrix(p, it[0] == "qft_dg")))
        elif it[0] == "oracle":
            if inst is None:
                raise ValueError("segment has an oracle call: give inst")
            flat, y = it[1]
            wq = [flat[b*(m-1-j):b*(m-j)] for j in range(m)]
            out.append(("oracle", wq, tuple(y), inst.oracle_table, p, m))
        else:
            raise ValueError(f"{it[0]} inside a simulated segment")
    return out


def _wires_of(ops):
    s = set()
    for g in ops:
        if g[0] == "oracle":
            s.update(w for q in g[1] for w in q)
            s.update(g[2])
        else:
            s.update(g[1])
    return s


def _key(assign, idx):
    k = 0
    for reg, v in assign:
        for j, w in enumerate(reg):
            if v >> j & 1:
                k |= 1 << idx[w]
    return k


def _distance(s0, s1):
    """|| s1 - s0 || for two CircuitStates on the same local indexing."""
    keys = [np.concatenate([a, b]) for a, b in zip(s0.keys, s1.keys)]
    amps = np.concatenate([-s0.amps, s1.amps])
    _, a = W._merge(keys, amps, s0.W)
    return float(np.sqrt(np.sum(np.abs(a)**2)))


def _nonzero_on(st, idx, wires):
    """Total probability on basis states with some of the given wires set."""
    m = np.zeros(len(st.amps), dtype=bool)
    for w in wires:
        ww, o = idx[w] // 64, idx[w] % 64
        m |= ((st.keys[ww] >> np.uint64(o)) & np.uint64(1)).astype(bool)
    return float(np.sum(np.abs(st.amps[m])**2))


def call_error(fts, ci, tol=1e-13):
    """Float check of ONE emitted transform slice: for every canonical x the
    output over all its wires (register, pool, ancillas) minus the ideal
    (QFT_p^(+-1)|x>)|0>; sigma_max (operator norm on the canonical subspace),
    column errors, pruning accounting; against error_bound."""
    call = fts.calls[ci]
    p, b = fts.p, fts.b
    gates = fts.slice(ci)
    reg = list(call["reg"])
    others = sorted(_wires_of(gates)-set(reg))
    idx = {w: i for i, w in enumerate(reg+others)}
    nq = len(idx)
    cg = _compile_local(gates, idx)
    sign = -1 if call["kind"] == "qft_dg" else 1
    Wd = (nq+63)//64
    rows_k, rows_v, cols, perr, maxsup = [], [], [], 0.0, 0
    for x in range(p):
        st = W.CircuitState(nq, [x], tol=tol).run(cg)
        perr = max(perr, st.prune_err)
        maxsup = max(maxsup, st.max_support)
        stk = np.stack(st.keys, axis=1)
        ideal = np.zeros((p, Wd), dtype=np.uint64)
        ideal[:, 0] = np.arange(p, dtype=np.uint64)
        iamp = np.exp(sign*2j*math.pi*x*np.arange(p)/p)/math.sqrt(p)
        rows_k.append(np.concatenate([stk, ideal]))
        rows_v.append(np.concatenate([st.amps, -iamp]))
        cols.append(np.full(len(st.amps)+p, x))
    allk = np.ascontiguousarray(np.concatenate(rows_k))
    v = allk.view(np.dtype((np.void, 8*allk.shape[1]))).ravel()
    _, rid = np.unique(v, return_inverse=True)
    rid = rid.ravel()
    from scipy.sparse import coo_matrix
    E = coo_matrix((np.concatenate(rows_v), (rid, np.concatenate(cols))), shape=(rid.max()+1, p)).tocsc()
    Gm = (E.conj().T @ E).toarray()
    ev = np.linalg.eigvalsh((Gm+Gm.conj().T)/2)
    sigma = float(math.sqrt(max(ev[-1], 0.0)))
    bd = Q.error_bound(p, *fts.params)
    return {"call": ci, "component": call["component"], "kind": call["kind"], "zero_input": call["zero"],
            "params": fts.params, "wires": nq, "gates": len(gates), "sigma_max": sigma,
            "sigma_upper": sigma+math.sqrt(p)*perr, "column_errors": [float(math.sqrt(max(Gm[x, x].real, 0.0)))
                                                                    for x in range(p)],
            "prune_err_max": perr, "max_support": maxsup, "B": bd["B"], "prep": bd["prep"]}


def segment_compare(fts, i0, i1, init=(), inst=None, tol=1e-12, extra_wires=()):
    """Items [i0, i1) simulated gate by gate over ALL wires they touch, once with
    the emitted explicit transforms and once with exact ones, from the same
    initial state (init: list of (amplitude, [(register, value), ...]); empty =
    all zero). Returns the full-state distance, pruning accounting, the hybrid
    budget of the calls in the segment, and for the exact run the probability
    found on the pool and ancillas at the end."""
    t0 = time.time()
    ops1 = segment_ops(fts, i0, i1, "explicit", inst)
    ops0 = segment_ops(fts, i0, i1, "exact", inst)
    wires = _wires_of(ops1) | _wires_of(ops0) | set(extra_wires) | \
        {w for _, asg in init for reg, _ in asg for w in reg}
    wires = sorted(wires)
    idx = {w: i for i, w in enumerate(wires)}
    nq = len(wires)
    start = [(a, _key(asg, idx)) for a, asg in init] or [(1.0, 0)]
    s0 = W.CircuitState(nq, [k for _, k in start], amps=np.array([a for a, _ in start], dtype=complex), tol=0.0)
    s0.run(_compile_local(ops0, idx))
    s1 = W.CircuitState(nq, [k for _, k in start], amps=np.array([a for a, _ in start], dtype=complex), tol=tol)
    s1.run(_compile_local(ops1, idx))
    calls = [fts.calls[fts.call_of_item[i]] for i in range(i0, i1) if i in fts.call_of_item]
    clean = [w for w in set(fts.pool) | set(fts.anc) if w in idx]
    return {"items": [i0, i1], "wires": nq, "gates_explicit": len(ops1), "gates_exact": len(ops0),
            "support_exact": len(s0.amps), "support_explicit": len(s1.amps), "max_support_explicit": s1.max_support,
            "prune_err_explicit": s1.prune_err, "prune_err_exact": s0.prune_err,
            "norm_explicit": float(np.sum(np.abs(s1.amps)**2)), "state_distance": _distance(s0, s1),
            "exact_run_mass_on_pool_or_ancillas": _nonzero_on(s0, idx, clean),
            "hybrid": hybrid_budget(calls, fts.p, *fts.params), "seconds": round(time.time()-t0, 1)}


# ---- segments of the terminal sample

def first_source_segment(fts, include_inverse=True):
    """Items of the first top source and its (unmeasured) instrument: from 0 to
    the first instrument qft_dg, inclusive (include_inverse) or exclusive."""
    for i, (comp, it) in enumerate(fts.ts.items):
        if comp == "instrument_qft" and not isinstance(it, Macro) and it[0] == "qft_dg":
            if not include_inverse:
                return 0, i
            last = i
            while fts.ts.items[last+1][0] == "instrument_qft" and fts.ts.items[last+1][1][0] == "qft_dg":
                last += 1
            return 0, last+1
    raise ValueError("no instrument")


def merge_nodes(ts):
    """Merge nodes in emission (post-) order, matching block_runs."""
    out = []

    def visit(node):
        for k in node["kids"]:
            visit(k)
        if node["kids"]:
            out.append(node)
    visit(ts.tree)
    return out


def merge_segment(fts, j):
    """Items of the Q preparation (its forward transforms) and merge block j."""
    a, b = block_runs(fts.ts)[j]
    s = a
    while s > 0 and fts.ts.items[s-1][0] == "q_prep_qft":
        s -= 1
    return s, b


def merge_inputs(fts, j, K, seed=0):
    """K random canonical basis assignments of block j's children and labels
    (uniform superposition); everything else 0."""
    node = merge_nodes(fts.ts)[j]
    rng = random.Random(seed)
    p = fts.p
    out = []
    for _ in range(K):
        asg = []
        for kid in node["kids"]:
            for q in kid["reg"]:
                asg.append((tuple(q), rng.randrange(p)))
            for q in kid["z"]:
                asg.append((tuple(q), rng.randrange(p)))
        out.append((1/math.sqrt(K), asg))
    keys = {tuple(v for _, v in asg) for _, asg in out}
    if len(keys) != K:
        raise ValueError("repeated input; change the seed")
    return out


# ====================================================================== counts and reports

def config(job):
    return C.job_config(job)


def counts_report(job, params, eta=None):
    cfg = config(job)
    fts = FullTerminalSample(cfg, params)
    gs = gate_set_check(fts)
    coh = fts.ts.counts()
    per_call = len(fts.ref["qft"])
    calls = fts.call_summary()
    hb = hybrid_budget(fts.calls, fts.p, *fts.params, eta=eta)
    n = n_samples(cfg)
    qft_types = Counter(g[0] for g in fts.ref["qft"])
    out = {"config": cfg.name(), "params": fts.params, "eta": eta, "pool_size": fts.npool,
           "block_workspace_pool": len(fts.ts.pool), "qubits": fts.nw, "qubits_coherent": fts.ts.nw,
           "qubits_separate_layout": fts.ts.nw+fts.npool, "gates_per_call": per_call,
           "gate_types_per_call": dict(qft_types), "gate_bound_per_call": Q.gate_bound(fts.b, *fts.params),
           "calls": calls, "coherent_gates": coh["total"]["gates"],
           "formula_total": coh["total"]["gates"]+len(fts.calls)*per_call, "emitted": gs,
           "oracle_calls": coh["oracle_calls"], "n_samples": n, "hybrid": hb,
           "P_run_differs_exact_formula": min(1.0, n*hb["exact_formula"])}
    if eta is not None:
        out["P_run_differs_lemma"] = min(1.0, n*hb["lemma"])
    out["formula_equals_emitted"] = out["formula_total"] == gs["total"]["gates"]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, help="output folder")
    ap.add_argument("--parts", default="counts,checks,per_call,source,merge")
    ap.add_argument("--heis-instances", type=int, default=19)
    ap.add_argument("--n4-merge-inputs", type=int, default=2)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    parts = set(args.parts.split(","))
    log = lambda *a: print(*a, flush=True)
    t00 = time.time()

    def dump(name, obj):
        with open(os.path.join(args.out, name+".json"), "w") as fh:
            json.dump({"status": STATUS, **obj}, fh, indent=1, default=str)

    targets = {}
    for job in ("heis_f3", "n4_f5"):
        cfg = config(job)
        fts = FullTerminalSample(cfg, (cfg.enc.nb+5,)*2+(28,))
        cs = fts.call_summary()
        targets[job] = target_params(cfg.p, cs["zero_input_forward"], cs["general"], n_samples(cfg))
    sim_params = {"heis_f3": (7, 7, 28), "n4_f5": (8, 8, 28)}
    if "counts" in parts:
        res = {"targets": targets}
        for job in ("heis_f3", "n4_f5"):
            t0 = time.time()
            res[job] = {"target": counts_report(job, targets[job]["params"], targets[job]["eta"]),
                        "sim_params": counts_report(job, sim_params[job])}
            log("counts", job, res[job]["target"]["emitted"]["total"]["gates"], round(time.time()-t0, 1))
        dump("counts", res)
    if "checks" in parts:
        res = {}
        for job, npaths in (("heis_f3", 1 << 14), ("n4_f5", 1024)):
            cfg = config(job)
            t0 = time.time()
            fts = FullTerminalSample(cfg, targets[job]["params"])
            res[job] = {"slice_check": slice_check(fts), "wire_check": wire_check(fts),
                        "basis_paths": basis_paths(fts, n=npaths, seed=20261104)}
            mut = {}
            for lay in ("mutant_labels", "mutant_oracle", "mutant_qudit"):
                fm = FullTerminalSample(cfg, targets[job]["params"], layout=lay)
                mut[lay] = {"wire_check_passed": wire_check(fm)["passed"],
                            "basis_paths_passed": basis_paths(fm, n=256, seed=1)["passed"]}
            fm = FullTerminalSample(cfg, targets[job]["params"], mutate={"rotation"})
            mut["rotation"] = {"slice_check_passed": slice_check(fm)["passed"]}
            fm = FullTerminalSample(cfg, targets[job]["params"], mutate={"footprint"})
            sc = slice_check(fm)
            mut["footprint"] = {"slice_check_passed": sc["passed"], "footprint_ok": sc["footprint_ok"]}
            res[job]["mutants"] = mut
            res[job]["seconds"] = round(time.time()-t0, 1)
            log("checks", job, res[job]["slice_check"]["passed"], res[job]["wire_check"]["passed"],
                res[job]["basis_paths"]["passed"], mut, res[job]["seconds"])
        dump("checks", res)
    if "per_call" in parts:
        res = {}
        for job, plist in (("heis_f3", [(7, 7, 28), (9, 9, 28), (7, 7, 8)]), ("n4_f5", [(8, 8, 28), (8, 8, 8)])):
            cfg = config(job)
            rows = []
            for prm in plist:
                fts = FullTerminalSample(cfg, prm)
                seen = set()
                for ci, c in enumerate(fts.calls):
                    key = (c["component"], c["kind"])
                    if key in seen:
                        continue
                    seen.add(key)
                    t0 = time.time()
                    r = call_error(fts, ci)
                    r["seconds"] = round(time.time()-t0, 1)
                    rows.append(r)
                    log("per_call", job, prm, key, r["sigma_max"], r["column_errors"][0], r["B"], r["seconds"])
            res[job] = rows
        dump("per_call", res)
    if "source" in parts:
        res = {}
        # Heis: the source with its complete unmeasured instrument (5 zero-input calls + 1 general);
        # n4: the source and the instrument up to (not including) its inverse transform (8 zero-input
        # calls), since the general call multiplies a support of 5^7 addresses by its pool tail.
        for job, prm, insts, inv in (("heis_f3", (7, 7, 28), G.heis3_instances()[:args.heis_instances], True),
                                     ("n4_f5", (4, 4, 28), G.n4_instances(5)[:3], False)):
            cfg = config(job)
            fts = FullTerminalSample(cfg, prm)
            i0, i1 = first_source_segment(fts, include_inverse=inv)
            rows = []
            for inst in insts:
                r = segment_compare(fts, i0, i1, inst=inst, tol=1e-10)
                r["instance"] = inst.name
                rows.append(r)
                log("source", job, inst.name, r["state_distance"], r["prune_err_explicit"],
                    r["hybrid"]["exact_formula"], r["seconds"])
            res[job] = {"params": prm, "includes_inverse_transform": inv, "tol": 1e-10, "rows": rows}
            dump("source_segment", res)
    if "merge" in parts:
        res = {}
        for job, prm, K in (("heis_f3", (7, 7, 28), 64), ("n4_f5", (8, 8, 28), args.n4_merge_inputs)):
            cfg = config(job)
            rows = []
            fts = FullTerminalSample(cfg, prm)
            fm = FullTerminalSample(cfg, prm, layout="mutant_labels")
            nblocks = len(block_runs(fts.ts))
            for j in sorted({0, nblocks-1}):
                i0, i1 = merge_segment(fts, j)
                init = merge_inputs(fts, j, K, seed=20261104+j)
                r = segment_compare(fts, i0, i1, init=init, tol=1e-9)
                r.update({"params": prm, "layout": "overlay", "block": j, "inputs": K, "tol": 1e-9,
                          "grade": merge_nodes(fts.ts)[j]["d"]+1})
                rows.append(r)
                log("merge", job, j, r["state_distance"], r["prune_err_explicit"], r["hybrid"]["exact_formula"],
                    r["exact_run_mass_on_pool_or_ancillas"], r["seconds"])
                # mutant: the pool overlaid on the (live) label registers; first Q-preparation call only
                r = segment_compare(fm, i0, i0+1, init=init, tol=1e-9)
                r.update({"params": prm, "layout": "mutant_labels", "block": j, "inputs": K, "tol": 1e-9,
                          "first_call_only": True})
                rows.append(r)
                log("merge mutant", job, j, r["state_distance"], r["hybrid"]["exact_formula"], r["seconds"])
                res[job] = rows
                dump("merge_segment", res)
    log("done", round(time.time()-t00, 1))


if __name__ == "__main__":
    main()

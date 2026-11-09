"""(B) class-general structural checks of the coherent terminal sample emitted by
TerminalSampleK(coherent_config_k(L)) (theorems/rees_circuit_coherent_k3.py over
the fourth backend), for several (L, p). Report:
../2026-11-05-rees-receiver-general-gh.md, Section 3.

AI-written, pending human review. Imports theorems/ read-only; writes only --out.

Per configuration (all checks read the emitted program; nothing is simulated
except where marked):
  R   refusal: the generator raises exactly when some grade has kappa_d >= 3 and
      p in E_2(kappa_d);
  D1  every label register: prep qft, instrument macro (operand only), qft_dg,
      and afterwards never a target of any item (macro target, gate target,
      swapreg, transform, oracle, measurement); every oracle-output register is
      written by its oracle call only and never touched again;
  S5  garbage never touched after its block; one measurement, at the end, of the
      root Q (TerminalSample.structure);
  D2c every block occurrence is, item by item, remap(block.prog) under an
      INJECTIVE wire map (so it is U, (ctrl_i, bch_i, ctrl_i^-1)_i, U^-1 of the
      block, and U is the block's SDE program), the map sends the block's
      labels / children / Q to the children's label and group registers and the
      parent's Q, and its workspace to the shared pool and arithmetic ancillas;
      inside the block, U = remap(sde.prog) under an injective map;
  D2a-type  which SDE circuit each block uses (class, p, a, d, kappa, stop mode);
  D2b block_structure (footprints) and prove_controlled_merge (symbolic replay
      over F_p[s, q, x] against sym_bch_reference) at every grade; children
      i > 0 equal child 0 under the renaming S_0 -> S_i, x_0 -> x_i;
  SIM (marked) U alone on all label tuples where p^(M g) <= 7*10^4, and the whole
      block on sampled inputs (block_sampled) otherwise;
  CNT counts of one terminal sample (gates excluding the oracle, qubits,
      transforms, oracle calls) against the closed-form bound of Section 3.4.
"""
from __future__ import annotations

import argparse
import gc
import json
import math
import resource
import sys
import time

REPO = "/Users/jaspersands/Developer/qsearch"
sys.path.insert(0, REPO)

import numpy as np  # noqa: E402

import theorems.rees_circuit_coherent as C  # noqa: E402
import theorems.rees_circuit_coherent_k3 as K  # noqa: E402
from theorems.rees_coherent_sde import Macro, Prog  # noqa: E402
from theorems.rees_end_to_end_sim import filiform4, filiform5, heisenberg, lie_from_brackets  # noqa: E402


def free_nil_2_3(p):
    """Free nilpotent Lie algebra of rank 2, class 3: x, y, z = [x,y], u = [x,z], v = [y,z]."""
    return lie_from_brackets(f"f(2,3)(F_{p})", p, 5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}})


def filiform6(p):
    return lie_from_brackets(f"n6(F_{p})", p, 6, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (0, 4): {5: 1}})


FAMILIES = {"heis": heisenberg, "n4": filiform4, "n5": filiform5, "n6": filiform6, "f23": free_nil_2_3}


def make_alg(name):
    """'<family>_f<p>', e.g. n4_f13, f23_f7, heis_f3."""
    fam, pp = name.split("_f")
    return FAMILIES[fam](int(pp))


def rss_mb():
    return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)


# ====================================================================== item matching

def match_items(local, glob, wmap):
    """Item-by-item equality up to a wire map (built here, checked consistent)."""
    if len(local) != len(glob):
        return False

    def bind(lw, gw):
        if len(lw) != len(gw):
            return False
        for a, b in zip(lw, gw):
            if wmap.setdefault(a, b) != b:
                return False
        return True
    for li, gi in zip(local, glob):
        if isinstance(li, Macro) != isinstance(gi, Macro):
            return False
        if isinstance(li, Macro):
            if (li.kind, li.coeff, li.inv, len(li.args)) != (gi.kind, gi.coeff, gi.inv, len(gi.args)):
                return False
            if not all(bind(a, b) for a, b in zip(li.args, gi.args)):
                return False
        else:
            if li[0] != gi[0]:
                return False
            if li[0] in ("swapreg", "qft", "qft_dg", "oracle", "measure"):
                if len(li[1]) != len(gi[1]) or not all(bind(a, b) for a, b in zip(li[1], gi[1])):
                    return False
            elif not bind(li[1], gi[1]):
                return False
    return True


def canon(it):
    return ("M", it.kind, it.coeff, it.args, it.inv) if isinstance(it, Macro) else it


def injective(wmap):
    return len(set(wmap.values())) == len(wmap)


# ====================================================================== per configuration

def check_config(name, sim=True, prove=True):
    t0 = time.time()
    alg = make_alg(name)
    out = {"config": name, "p": alg.p}
    try:
        cfg = K.coherent_config_k(alg)
        out["dims"], out["c"] = list(map(int, cfg.dims)), cfg.c
        out["kappa"] = {d: math.gcd(d, cfg.p-1) for d in range(2, cfg.c+1)}
        out["arity"] = dict(cfg.arity)
        ts = K.TerminalSampleK(cfg)
    except ValueError as e:
        out["refused"] = str(e)
        out["seconds"] = round(time.time()-t0, 1)
        return out
    out["refused"] = None
    items = ts.items
    role = ts.role
    out["items"] = len(items)
    # ---------------- D1
    label_regs, y_regs = {}, {}
    for w, r in role.items():
        if r.startswith("label_z_grade"):
            label_regs.setdefault(r, []).append(w)
        elif r == "oracle_output":
            y_regs.setdefault(r, []).append(w)
    touch_idx = {}
    for i, (_, it) in enumerate(items):
        for w in C.touched(it):
            touch_idx.setdefault(w, []).append(i)
    # group wires into registers: label registers are b-wire runs created together
    b = cfg.enc.nb
    lab_wires = sorted(w for ws in label_regs.values() for w in ws)
    regs = [tuple(lab_wires[i:i+b]) for i in range(0, len(lab_wires), b)]
    ok_d1, n_lab = True, 0
    for reg in regs:
        n_lab += 1
        w0 = set(reg)
        idx = sorted({i for w in reg for i in touch_idx.get(w, [])})
        kinds = []
        seen_dg = False
        for i in idx:
            comp, it = items[i]
            tg = C.targets(it) & w0
            if not isinstance(it, Macro) and it[0] == "qft":
                ok_d1 &= (not seen_dg and set(it[1][0]) == w0 and not kinds)
                kinds.append("qft")
            elif not isinstance(it, Macro) and it[0] == "qft_dg":
                ok_d1 &= (not seen_dg and set(it[1][0]) == w0 and kinds and kinds[0] == "qft")
                seen_dg = True
                kinds.append("qft_dg")
            else:
                if tg:
                    ok_d1 = False
                if not isinstance(it, Macro) and it[0] in ("swapreg", "oracle", "measure"):
                    ok_d1 = False
                if not seen_dg:
                    ok_d1 &= isinstance(it, Macro) and comp == "instrument"
                kinds.append("ctrl")
        ok_d1 &= seen_dg
    y_wires = sorted(y_regs.get("oracle_output", []))
    ok_y = True
    for w in y_wires:
        idx = touch_idx.get(w, [])
        ok_y &= (len(idx) == 1 and items[idx[0]][1][0] == "oracle" and w in C.targets(items[idx[0]][1]))
    out["D1_label_registers"] = n_lab
    out["D1_labels_control_only_after_qft_dg"] = ok_d1
    out["D1_oracle_outputs_written_once_never_touched"] = ok_y
    out["S5_structure"] = ts.structure()
    # ---------------- D2c: block occurrences = remap(block.prog) under injective maps
    blocks = ts.blocks
    comps_of = {d: {f"sde_grade{d}", f"witness_control_grade{d}", f"bch_merge_grade{d}"} for d in blocks}
    occ = {d: [] for d in blocks}
    i = 0
    while i < len(items):
        comp = items[i][0]
        d = next((dd for dd in blocks if comp in comps_of[dd]), None)
        if d is None:
            i += 1
            continue
        L = len(blocks[d].prog)
        occ[d].append((i, i+L))
        i += L
    d2c = {}
    for d, blk in blocks.items():
        oks, roles_ok = [], []
        for (st, en) in occ[d]:
            seg = [it for _, it in items[st:en]]
            wmap = {}
            ok = match_items(list(blk.prog), seg, wmap) and injective(wmap)
            ok &= all(items[j][0] in comps_of[d] for j in range(st, en))
            oks.append(ok)
            # role check of the map
            rl = all(role[wmap[w]].startswith(f"label_z_grade{d}") for r in blk.lam for q in r for w in q if w in wmap)
            rx = all(role[wmap[w]] in ("address_top", f"Q_grade{d}") for r in blk.x for q in r for w in q if w in wmap)
            rq = all(role[wmap[w]] == f"Q_grade{d-1}" for q in blk.Q for w in q if w in wmap)
            io = {w for r in blk.lam for q in r for w in q} | {w for r in blk.x for q in r for w in q} | \
                {w for q in blk.Q for w in q}
            rw = all(role[wmap[w]] in ("block_workspace_pool", "arith_ancilla") for w in wmap if w not in io)
            roles_ok.append(rl and rx and rq and rw)
        smap = {}
        u_ok = match_items(list(blk.sde.prog), list(blk.U), smap) and injective(smap)
        sde = blk.sde
        d2c[d] = {"occurrences": len(occ[d]), "expected": int(np.prod([cfg.arity[e] for e in range(2, d)])) if d > 2 else 1,
                  "all_equal_remap_of_block_prog_injective": all(oks), "roles_ok": all(roles_ok),
                  "U_equals_remap_of_sde_prog_injective": u_ok,
                  "sde": {"class": type(sde).__name__, "p": sde.p, "a": getattr(sde, "a", getattr(sde, "g", None)),
                          "d": sde.d, "kappa": math.gcd(sde.d, sde.p-1), "M": blk.M,
                          "stop": getattr(sde, "stop_mode", None),
                          "contraction": (list(sde.alpha), list(sde.beta)) if hasattr(sde, "alpha") else None}}
    out["D2c_blocks"] = d2c
    # ---------------- D2b and footprints
    d2b = {}
    for d, blk in blocks.items():
        row = {"block_structure": C.block_structure(blk)}
        if prove:
            t1 = time.time()
            row["prove_controlled_merge"] = C.prove_controlled_merge(blk)
            row["prove_seconds"] = round(time.time()-t1, 1)
        base = Prog(blk.ctrl[0]+blk.bch[0]+blk.ctrl[0].inverse())
        ren = []
        for ci in range(1, blk.M):
            wm = {w: w for w in range(blk.nw)}
            wm.update(zip(blk.S[0], blk.S[ci]))
            for j in range(blk.nx):
                wm.update(zip(blk.x[0][j], blk.x[ci][j]))
            other = Prog(blk.ctrl[ci]+blk.bch[ci]+blk.ctrl[ci].inverse())
            ren.append([canon(x) for x in C.remap(base, wm)] == [canon(x) for x in other])
        row["children_equal_child0_under_renaming"] = all(ren)
        d2b[d] = row
    out["D2b_blocks"] = d2b
    # ---------------- simulations (marked)
    if sim:
        simr = {}
        for d, blk in blocks.items():
            n_tuples = blk.p**(blk.M*blk.g)
            t1 = time.time()
            if n_tuples <= 7*10**4:
                r = K.sde_exhaustive(blk)
                simr[d] = {"mode": "U alone, all label tuples", **r}
            else:
                r = K.block_sampled(blk, n=192, seed=d)
                simr[d] = {"mode": "whole block, 192 sampled inputs",
                           **{k: v for k, v in r.items() if not isinstance(v, (list, dict))}}
            simr[d]["seconds"] = round(time.time()-t1, 1)
        out["SIM"] = simr
    # ---------------- counts
    cnt = ts.counts()
    tot = cnt["total"]
    out["CNT"] = {"gates_excl_oracle": tot.get("gates"), "ccx": tot.get("ccx"), "qubits": cnt["qubits"],
                  "qft_calls": tot.get("qft_calls"), "oracle_calls": cnt["oracle_calls"],
                  "add_product": tot.get("add_product"), "add_scaled": tot.get("add_scaled"),
                  "sources": cnt["sources"], "b": b, "n_cover": int(cfg.width[cfg.c]), "m": int(cfg.m)}
    out["CNT"]["by_component_gates"] = {k: v.get("gates") for k, v in cnt["by_component"].items()}
    out["CNT"]["by_component_macros"] = {k: v.get("add_product", 0)+v.get("add_scaled", 0)
                                         for k, v in cnt["by_component"].items()}
    out["rss_mb"] = rss_mb()
    out["seconds"] = round(time.time()-t0, 1)
    del ts, items
    gc.collect()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", default="heis_f3,n4_f5,n4_f7,n4_f13,f23_f7,n5_f7,n5_f41,n5_f13,n5_f5")
    ap.add_argument("--no-sim", action="store_true")
    ap.add_argument("--no-prove", action="store_true")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    res = []
    try:
        old = json.load(open(args.out))["configs"]
    except Exception:
        old = []
    done = {r["config"] for r in old}
    res = list(old)
    for name in args.configs.split(","):
        if name in done:
            continue
        r = check_config(name, sim=not args.no_sim, prove=not args.no_prove)
        res.append(r)
        print(json.dumps({k: r.get(k) for k in ("config", "refused", "items", "D1_labels_control_only_after_qft_dg",
                                                 "seconds", "rss_mb")}), flush=True)
        with open(args.out, "w") as f:
            json.dump({"configs": res}, f, indent=1, default=str)


if __name__ == "__main__":
    main()

"""Independent check of the coherent generator TerminalSampleK(coherent_config_k(L)) on
configurations the report did not list (referee of 2026-11-05-rees-receiver-general-gh.md).

Imports only theorems/ modules. New here: the macro-count formula (arities, N_d, BCH bracket
supports recomputed from the cover tensor), the per-label D1 scan over the emitted items, the
oracle-output scan, the refusal list, and the raw-gate accounting. AI-written, pending human review.
"""
from __future__ import annotations

import argparse
import json
import math
import resource
import sys
import time
from math import gcd, prod

sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
from theorems.rees_circuit_coherent_k3 import TerminalSampleK, coherent_config_k  # noqa: E402
from theorems.rees_circuit_coherent import prog_counts  # noqa: E402
from theorems.rees_circuit_general import bch_nodes, _mod_fraction  # noqa: E402
from theorems.rees_coherent_sde import Macro, Prog  # noqa: E402
from theorems.rees_circuit_arith import formula_counts  # noqa: E402
from theorems.rees_end_to_end_sim import filiform4, filiform5, heisenberg  # noqa: E402
from theorems.rees_end_to_end_ext import filiform5_q  # noqa: E402
from theorems.rees_circuit_exhaustive import filiform6  # noqa: E402


def rss():
    return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)


def own_arity(p, g, d):
    return g+1 if gcd(d, p-1) == 1 else (g+1)*(g+2)//2


def own_nodes(cover_T, p, d, width):
    """Right-nested BCH nodes with supports, recomputed from the tensor (alpha from bch_nodes)."""
    n, nq = width[d], width[d-1]
    T = cover_T[:n, :n, :n] % p
    supp, out = {}, []
    for w, a in bch_nodes(d):
        if w == "xy":
            left, right = range(n), range(nq)
        else:
            if w[1:] not in supp:
                continue
            left = range(n) if w[0] == "x" else range(nq)
            right = supp[w[1:]]
        s = sorted({k for i in left for j in right for k in range(n) if T[i, j, k]})
        if s:
            supp[w] = s
            out.append((w, _mod_fraction(a, p), s))
    keep = {w for w, a, _ in out if a}
    changed = True
    while changed:
        changed = False
        for w, _, _ in out:
            if w not in keep and any(u != w and u.endswith(w) for u in keep):
                keep.add(w)
                changed = True
    return [(w, a, s) for w, a, s in out if w in keep], T


def own_macro_formula(cfg, sde_macros):
    p, c = cfg.p, cfg.c
    dims = cfg.dims
    width = {d: sum(dims[:d]) for d in range(0, c+1)}
    M = {d: own_arity(p, dims[d-1], d) for d in range(2, c+1)}
    N = {d: prod(M[e] for e in range(2, d+1)) for d in range(1, c+1)}
    grades = [k for k in range(1, c+1) for _ in range(dims[k-1])]
    comp = {}
    nnzE = sum(int((cfg.cover.evaluation_matrix(s) % p != 0).sum()) for s in cfg.points)
    comp["source_evaluation"] = N[c]*2*nnzE
    comp["instrument"] = sum(N[d]*dims[d-1] for d in range(2, c+1))
    BR, LIN = {}, {}
    for d in range(2, c+1):
        nodes, T = own_nodes(cfg.cover.tensor, p, d, width)
        nx, nq = width[d], width[d-1]
        br = 0
        sup = {w: s for w, _, s in nodes}
        for w, _, s in nodes:
            for k in s:
                if w == "xy":
                    br += sum(1 for i in range(nx) for j in range(nq) if T[i, j, k])
                else:
                    li = range(nx) if w[0] == "x" else range(nq)
                    br += sum(1 for i in li for j in sup[w[1:]] if T[i, j, k])
        lin = nx+nq+sum(len(s) for w, a, s in nodes if a)
        BR[d], LIN[d] = br, lin
        maxdeg = max(grades[:nq])
        comp[f"sde_grade{d}"] = 2*N[d-1]*sde_macros[d]
        comp[f"witness_control_grade{d}"] = 2*N[d-1]*M[d]*(max(0, maxdeg-1)+nq)
        comp[f"bch_merge_grade{d}"] = N[d-1]*M[d]*(4*br+2*lin)
        # coarse bounds of the report
        nnzT = int((T != 0).sum())
        comp[f"_bound_ok_grade{d}"] = br <= 2**(d-1)*nnzT <= 2**(d-1)*cfg.cover.tensor.shape[0]**3 and \
            lin <= 2*cfg.cover.tensor.shape[0]+2**(d-1)*cfg.cover.tensor.shape[0]
    return comp, M, N, BR, LIN


def d1_scan(ts):
    """Each label register: qft, instrument macro (as operand only), qft_dg, then only non-target
    uses inside SDE segments; oracle outputs written once by their oracle call and never touched."""
    lab = {}
    for w, r in ts.role.items():
        if r.startswith("label_z"):
            lab.setdefault(r, set()).add(w)
    labw = set().union(*lab.values()) if lab else set()
    orw = {w for w, r in ts.role.items() if r == "oracle_output"}
    hist = {}
    bad, bad_or, or_touch = [], [], {}
    for idx, (comp, it) in enumerate(ts.items):
        if isinstance(it, Macro):
            tg = set(it.args[0])
            tc = {w for r in it.args for w in r}
            kind = "macro"
        else:
            name, qs = it
            if name in ("qft", "qft_dg", "oracle", "measure", "swapreg"):
                tc = {w for r in qs for w in r}
                tg = set() if name == "measure" else ({w for w in qs[1]} if name == "oracle" else tc)
            else:
                tc = set(qs)
                tg = set(qs) if name == "swap" else {qs[-1]}
            kind = name
        hit = tc & labw
        if hit:
            for w in hit:
                hist.setdefault(w, []).append((comp, kind, w in tg))
        if tc & orw:
            for w in tc & orw:
                or_touch.setdefault(w, []).append((comp, kind, w in tg))
    for w, h in hist.items():
        # first three: qft (target), instrument macro (not target), qft_dg (target)
        head = h[:3]
        ok = len(h) >= 3 and head[0][:2] == ("instrument_qft", "qft") and head[1][:2] == ("instrument", "macro") \
            and not head[1][2] and head[2][:2] == ("instrument_qft", "qft_dg")
        ok = ok and all(cmp.startswith("sde_grade") and not tgt for cmp, _, tgt in h[3:])
        # the root-level labels? every label must be consumed by exactly one parent block (U and U^-1)
        ok = ok and len(h) > 3
        if not ok:
            bad.append(w)
    for w in orw:
        h = or_touch.get(w, [])
        if not (len(h) == 1 and h[0][1] == "oracle" and h[0][2]):
            bad_or.append(w)
    return {"label_wires": len(labw), "label_wires_bad": len(bad), "oracle_output_wires": len(orw),
            "oracle_wires_bad": len(bad_or), "passed": not bad and not bad_or}


def check(name, alg):
    t0 = time.time()
    try:
        cfg = coherent_config_k(alg)
        ts = TerminalSampleK(cfg)
    except (ValueError, RuntimeError) as e:
        return {"config": name, "refused": f"{type(e).__name__}: {e}", "seconds": round(time.time()-t0, 1)}
    p, c = cfg.p, cfg.c
    b = cfg.enc.nb
    sde_macros = {d: sum(isinstance(it, Macro) for it in blk.sde.prog) for d, blk in ts.blocks.items()}
    comp, M, N, BR, LIN = own_macro_formula(cfg, sde_macros)
    emitted = {}
    for cmp, it in ts.items:
        if isinstance(it, Macro):
            key = cmp if not cmp.startswith("instrument") else "instrument"
            emitted[key] = emitted.get(key, 0)+1
    pred = {k: v for k, v in comp.items() if not k.startswith("_")}
    tot = prog_counts(Prog(it for _, it in ts.items), p)
    n_macros = sum(emitted.values())
    raw = tot["gates"]-sum(tot.get(k, 0) for k in ())  # placeholder, refined below
    macro_gate_sum = 0
    from collections import Counter
    mc = Counter((it.kind, it.coeff) for _, it in ts.items if isinstance(it, Macro))
    for (kind, coeff), cnt in mc.items():
        fc = formula_counts(p, coeff)
        macro_gate_sum += cnt*fc[kind+"_total"]
    raw = tot["gates"]-macro_gate_sum
    bound = 158*b*b+46*b
    m, n = cfg.m, cfg.cover.tensor.shape[0]
    res = {"config": name, "refused": None, "p": p, "b": b, "c": c, "m": m, "n": n, "dims": list(cfg.dims),
           "kappa": {d: gcd(d, p-1) for d in range(2, c+1)}, "own_arity": M, "config_arity": dict(cfg.arity),
           "arity_match": {d: M[d] == cfg.arity[d] for d in M},
           "sde_classes": {d: type(blk.sde).__name__ for d, blk in ts.blocks.items()},
           "N": N, "BR": BR, "LIN": LIN, "predicted": pred, "emitted": emitted,
           "exact_match_by_component": {k: pred.get(k) == emitted.get(k) for k in set(pred) | set(emitted)},
           "coarse_bounds_ok": all(v for k, v in comp.items() if k.startswith("_")),
           "macros": n_macros, "gates": tot["gates"], "macro_gates_by_formula_counts": macro_gate_sum,
           "raw_gates_outside_macros": raw, "raw_fraction": round(raw/tot["gates"], 4),
           "gates_le_bound_times_macros_plus_raw": tot["gates"] <= bound*n_macros+raw,
           "gates_per_macro": round(tot["gates"]/n_macros, 1), "macro_bound_158b2_46b": bound,
           "qft_calls": tot.get("qft_calls"), "oracle_calls": tot.get("oracle_calls"), "qubits": ts.nw,
           "oracle_calls_eq_c_Nc": tot.get("oracle_calls") == c*N[c], "items": len(ts.items),
           "structure": ts.structure()}
    res["d1"] = d1_scan(ts)
    res["seconds"] = round(time.time()-t0, 1)
    res["rss_mb"] = rss()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--configs", default="heis_f7,n4_f73,n5_f29,n5_f37,n5_f53,n5_f17,n6_f11,n6_f31,q5_f13,n5_f61")
    args = ap.parse_args()
    algs = {"heis_f7": lambda: heisenberg(7), "n4_f73": lambda: filiform4(73),
            "n5_f29": lambda: filiform5(29), "n5_f37": lambda: filiform5(37), "n5_f53": lambda: filiform5(53),
            "n5_f17": lambda: filiform5(17), "n6_f11": lambda: filiform6(11), "n6_f31": lambda: filiform6(31),
            "q5_f13": lambda: filiform5_q(13), "n5_f61": lambda: filiform5(61), "q5_f61": lambda: filiform5_q(61)}
    out = []
    for name in args.configs.split(","):
        r = check(name, algs[name]())
        out.append(r)
        print(json.dumps({k: r.get(k) for k in ("config", "refused", "kappa", "macros", "gates", "raw_fraction",
                                                  "exact_match_by_component", "d1", "seconds", "rss_mb")},
                         default=str), flush=True)
        with open(args.out, "w") as fh:
            json.dump(out, fh, indent=1, default=str)


if __name__ == "__main__":
    main()

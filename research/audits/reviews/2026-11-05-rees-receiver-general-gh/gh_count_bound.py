"""(B) gate count of one coherent terminal sample of TerminalSampleK: exact macro count
per component from closed forms (no program needed), compared with the emitted program,
and the polynomial bound of the report (Section 3.4). Report:
../2026-11-05-rees-receiver-general-gh.md. AI-written, pending human review.

Exact per-component macro formulas (N_d = prod_{e=2..d} M_e, N_1 = 1; w_d = width[d]):
  source_evaluation  N_c * 2 * sum_s nnz(E_s)
  instrument         sum_{d=2..c} N_d * g_d
  sde_grade d        N_{d-1} * 2 * SDE_d          (SDE_d = macros of F + C + F^-1, closed form of the
                                                    kappa_d module: rees_coherent_sde / _k2 / _kappa)
  witness_control d  N_{d-1} * M_d * 2 * ((d-2) + w_{d-1})
  bch_merge d        N_{d-1} * M_d * (4 * BR_d + 2 * LIN_d), BR_d = sum over the pruned nodes and
                     their supports of the nonzero structure constants, LIN_d = w_d + w_{d-1} + sum over
                     nodes with alpha != 0 of |supp|
Coarse bound: BR_d <= 2^(d-1) nnz(T_d), LIN_d <= 2 w_d + 2^(d-1) w_d, every macro <= 158 b^2 + 46 b gates.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time

REPO = "/Users/jaspersands/Developer/qsearch"
sys.path.insert(0, REPO)
sys.path.insert(0, __file__.rsplit("/", 1)[0])

import numpy as np  # noqa: E402

import theorems.rees_circuit_coherent_k3 as K  # noqa: E402
import theorems.rees_coherent_sde as S1  # noqa: E402
import theorems.rees_coherent_sde_k2 as S2  # noqa: E402
import theorems.rees_coherent_sde_kappa as SK  # noqa: E402
from gh_structure_check import make_alg  # noqa: E402


def sde_macros(p, g, d):
    k = math.gcd(d, p-1)
    f = S1.closed_form_macros if k == 1 else (S2.closed_form_macros if k == 2 else SK.closed_form_macros)
    r = f(p, g, d)
    return r["add_product"]+r["add_scaled"]


def predicted(cfg):
    p, c = cfg.p, cfg.c
    N = {1: 1}
    for d in range(2, c+1):
        N[d] = N[d-1]*cfg.arity[d]
    out, coarse = {}, {}
    nnzE = sum(int(np.count_nonzero(cfg.cover.evaluation_matrix(s) % p)) for s in cfg.points)
    out["source_evaluation"] = N[c]*2*nnzE
    out["instrument"] = sum(N[d]*cfg.dims[d-1] for d in range(2, c+1))
    for d in range(2, c+1):
        M, w1, w = cfg.arity[d], cfg.width[d-1], cfg.width[d]
        T = cfg.laws[d].tensor % p
        out[f"sde_grade{d}"] = N[d-1]*2*sde_macros(p, cfg.dims[d-1], d)
        out[f"witness_control_grade{d}"] = N[d-1]*M*2*((d-2)+w1)
        br, lin = 0, w+w1
        nodes = cfg.nodes[d]
        supp = {wd: s for wd, _, s in nodes}
        for wd, a, s in nodes:
            right = range(w1) if wd == "xy" else supp[wd[1:]]
            left = range(w) if wd[0] == "x" else range(w1)
            br += sum(1 for k in s for i in left for j in right if T[i, j, k])
            if a:
                lin += len(s)
        out[f"bch_merge_grade{d}"] = N[d-1]*M*(4*br+2*lin)
        nnz = int(np.count_nonzero(T))
        coarse[f"bch_per_child_grade{d}"] = {"exact": 4*br+2*lin,
                                             "coarse_bound": 4*2**(d-1)*nnz+2*(2*w+2**(d-1)*w)}
    return N, out, coarse


def run(name, build=True):
    t0 = time.time()
    alg = make_alg(name)
    cfg = K.coherent_config_k(alg)
    N, pred, coarse = predicted(cfg)
    row = {"config": name, "p": cfg.p, "c": cfg.c, "m": int(cfg.m), "n": int(cfg.width[cfg.c]),
           "b": cfg.enc.nb, "arity": dict(cfg.arity), "N": N, "predicted_macros": pred,
           "bch_bound": coarse, "predicted_total_macros": sum(pred.values())}
    if build:
        try:
            ts = K.TerminalSampleK(cfg)
        except ValueError as e:
            row["refused"] = str(e)
            return row
        cnt = ts.counts()
        meas = {k: v.get("add_product", 0)+v.get("add_scaled", 0) for k, v in cnt["by_component"].items()
                if v.get("add_product", 0)+v.get("add_scaled", 0)}
        row["measured_macros"] = meas
        row["exact_match"] = meas == pred
        tot = cnt["total"]
        row["gates_excl_oracle"] = tot["gates"]
        row["qubits"] = cnt["qubits"]
        row["qft_calls"] = tot.get("qft_calls", 0)
        row["oracle_calls"] = cnt["oracle_calls"]
        b = cfg.enc.nb
        row["gates_le_macros_times_158b2_plus_raw"] = None   # raw (non-macro) gates reported separately
        row["max_gates_per_macro_bound"] = 158*b*b+46*b
        row["gates_over_macros"] = round(tot["gates"]/sum(meas.values()), 1)
        del ts
    row["seconds"] = round(time.time()-t0, 1)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", default="heis_f3,heis_f5,n4_f5,n4_f7,n4_f13,f23_f7,f23_f13,n5_f7,n5_f41,n6_f7")
    ap.add_argument("--scaling", default="n4_f7,n4_f13,n4_f19,n4_f31,n4_f37,n4_f43,n4_f61,n4_f67")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    res = {"configs": [], "scaling": []}
    for name in args.configs.split(","):
        r = run(name)
        res["configs"].append(r)
        print(json.dumps({k: r.get(k) for k in ("config", "exact_match", "predicted_total_macros",
                                                 "gates_excl_oracle", "seconds")}), flush=True)
        json.dump(res, open(args.out, "w"), indent=1, default=str)
    for name in args.scaling.split(","):
        r = run(name)
        res["scaling"].append({k: r.get(k) for k in ("config", "p", "b", "arity", "exact_match",
                                                     "predicted_total_macros", "gates_excl_oracle", "qubits",
                                                     "qft_calls", "oracle_calls", "gates_over_macros",
                                                     "seconds")})
        print(json.dumps(res["scaling"][-1]), flush=True)
        json.dump(res, open(args.out, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()

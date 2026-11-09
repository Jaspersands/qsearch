"""Driver for the qft-wire report. Usage (repo root):
  /opt/anaconda3/bin/python research/audits/reviews/2026-11-04-rees-qft-wire/run_all.py JOB
JOB in counts, per_call, heis_composite, n4_composite, recoveries. Writes JOB.json next to this file.
AI-checked, pending human review."""
import json
import math
import os
import sys
import time

sys.path.insert(0, os.getcwd())
import theorems.rees_circuit_general as G
import theorems.rees_circuit_qft_wire as W
import theorems.rees_qft_mod as Q
from theorems.rees_end_to_end_sim import filiform4, heisenberg

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = {3: (7, 7, 28), 5: (8, 8, 28)}          # t = b + 5, r = t, tp = 28
N_SAMPLES = {"heis_f3": 3+4, "n4_f5": 4+4}     # cfg.m + extra_samples of run_algorithm
TARGET = 0.1                                   # per-run coupling failure we aim for


def cfgs():
    return {"heis_f3": G.Config(heisenberg(3)), "n4_f5": G.Config(filiform4(5))}


def dump(job, obj):
    with open(os.path.join(HERE, f"{job}.json"), "w") as f:
        json.dump({"status": W.WIRE_STATUS, job: obj}, f, indent=1, default=float)


def log(*a):
    print(*a, flush=True)


def eta_for_target(cfg, name):
    """Largest eta = 2^-k/... on a fine grid with n_samples * proved budget <= TARGET (Cor. 8 params)."""
    calls = W.qft_call_inputs(*W.terminal_sample_circuit(cfg))
    best = None
    for j in range(0, 400):
        eta = 0.5*2**(-j/8)
        t, r, tp = Q.params_for_eta(cfg.p, eta)
        r = min(r, t)
        bud = W.hybrid_budget(calls, cfg.p, t, r, tp)["proved_total"]
        if N_SAMPLES[name]*bud <= TARGET:
            best = (eta, (t, r, tp), bud)
            break
    return best


def job_counts():
    out = {}
    for name, cfg in cfgs().items():
        b = cfg.enc.nb
        qc, B = G.terminal_sample_circuit(cfg)
        row = {"original": {"qubits": qc.num_qubits, "gates_incl_qft_unitaries": len(qc.data)},
               "exact_arith": W.terminal_counts(cfg),
               "explicit_sim_shared": W.terminal_counts(cfg, "explicit", params=SIM[cfg.p]),
               "explicit_sim_fresh": W.terminal_counts(cfg, "explicit", params=SIM[cfg.p], pool="fresh")}
        eta, prm, bud = eta_for_target(cfg, name)
        row["target"] = {"per_run_coupling_target": TARGET, "n_samples": N_SAMPLES[name], "eta": eta,
                         "params": prm, "proved_budget_per_sample": bud}
        row["explicit_target_shared"] = W.terminal_counts(cfg, "explicit", params=prm)
        # one call at the target params, gate count vs the closed form
        ops, L = W.reference_ops(cfg.p, *prm)
        row["target"]["gates_per_call"] = len(ops)
        row["target"]["gate_bound_per_call"] = Q.gate_bound(L.b, *prm)
        row["target"]["qubits_per_call_lemma"] = L.nq
        out[name] = row
        log(name, json.dumps(row, default=float))
    return out


def job_per_call():
    out = []
    plans = {3: [(7, 7, 28), (9, 9, 28), (11, 11, 28), Q.params_for_eta(3, 0.25)],
             5: [(8, 8, 28), (10, 10, 28), Q.params_for_eta(5, 0.25)]}
    for name, cfg in cfgs().items():
        for prm in plans[cfg.p]:
            t, r, tp = prm
            prm = (t, min(r, t), tp)
            qc, B, _ = W.build(G.instrument_circuit, cfg, cfg.c, qft="explicit", params=prm)
            W.check_macros_qft(qc, B)
            for m in B.macros:
                if m[0] in ("qft", "qft_dg"):
                    r_ = W.call_operator_error(qc, B, m)
                    r_["config"] = cfg.name()
                    out.append(r_)
                    log(cfg.p, prm, m[0], r_["sigma_max"], r_["column_errors"][0], r_["bound"]["B"],
                        r_["bound"]["prep"], r_["max_support"])
            dump("per_call", out)
    return out


def job_heis_composite():
    cfg = cfgs()["heis_f3"]
    out = {"source": [], "segment": [], "instrument": None}
    out["instrument"] = W.instrument_block_error(cfg, 2, SIM[3])
    log("instrument", out["instrument"])
    for inst in G.heis3_instances():
        r = W.compare_prefix(cfg, inst, SIM[3], end_fn=W.source_prefix_end)
        out["source"].append(r)
        r2 = W.compare_prefix(cfg, inst, SIM[3])
        out["segment"].append(r2)
        log(inst.name, r["state_distance"], r["prune_err_explicit"], r2["state_distance"], r2.get("label_tv"),
            r2["hybrid"]["proved_total"], r2["seconds"])
        dump("heis_composite", out)
    return out


def job_n4_composite():
    cfg = cfgs()["n4_f5"]
    out = {"instrument": [], "source": []}
    for d, prm in ((3, SIM[5]), (3, (5, 5, 28))):   # d = 2 (two general calls in sequence) did not finish in 300 s at t = 3
        r = W.instrument_block_error(cfg, d, prm)
        out["instrument"].append(r)
        log("instrument", r)
        dump("n4_composite", out)
    for inst in G.n4_instances(5)[:3]:
        r = W.compare_prefix(cfg, inst, (4, 4, 28), end_fn=W.source_prefix_end)
        out["source"].append(r)
        log(inst.name, r)
        dump("n4_composite", out)
    return out


def job_recoveries():
    import theorems.rees_circuit_arith as A
    import theorems.rees_circuit_sparse as S
    out = {}
    per_call = json.load(open(os.path.join(HERE, "per_call.json")))["per_call"]
    for name, cfg in cfgs().items():
        insts = G.heis3_instances() if name == "heis_f3" else G.n4_instances(5)
        seeds = (20261103, 20261104) if name == "heis_f3" else (20261103,)
        with A.arith_backend():
            eng = S.SparseEngine(cfg)
            runs = []
            for inst in insts:
                for sd in seeds:
                    got, info = S.run_algorithm_sparse(cfg, inst, eng, seed=sd)
                    runs.append({"instance": inst.name, "seed": sd, "recovered": info["recovered"],
                                 "oracle_queries": info["oracle_queries"]})
                    log(name, inst.name, sd, info["recovered"])
        calls = W.qft_call_inputs(*W.terminal_sample_circuit(cfg))
        sim = {}
        for k in ("qft", "qft_dg"):
            sim[k] = next(r for r in per_call if r["p"] == cfg.p and r["kind"] == k and
                          (r["t"], r["r"], r["tp"]) == SIM[cfg.p])
        bud_sim = W.hybrid_budget(calls, cfg.p, *SIM[cfg.p], sim=sim)
        eta, prm, bud = eta_for_target(cfg, name)
        n = N_SAMPLES[name]
        out[name] = {"runs": runs, "all_recovered_exact_backend": all(r["recovered"] for r in runs),
                     "n_samples_per_run": n,
                     "sim_params": SIM[cfg.p], "budget_sim_params": bud_sim,
                     "coupling_failure_sim_params_proved": W.coupling_bound(bud_sim["proved_total"], n),
                     "coupling_failure_sim_params_float": W.coupling_bound(bud_sim["float_total"], n),
                     "target_eta": eta, "target_params": prm, "target_budget_proved": bud,
                     "coupling_failure_target_proved": W.coupling_bound(bud, n)}
        log(name, {k: v for k, v in out[name].items() if k != "runs"})
    return out


if __name__ == "__main__":
    job = sys.argv[1]
    t0 = time.time()
    res = globals()[f"job_{job}"]()
    dump(job, res)
    log("done", job, round(time.time()-t0, 1), "s")

"""Summarize the saved long-run JSON files of theorems/rees_end_to_end_ext.py (one line per group)."""
import glob
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
for path in sorted(glob.glob(os.path.join(here, "*.json"))):
    r = json.load(open(path))
    flags = {k: r[k] for k in ("runs", "aborted", "all_recovered", "all_laws_uniform",
                               "all_stage_outputs_equal_rho_H_d", "all_readout_laws_uniform_on_h_perp",
                               "all_queries_equal_charged", "all_block_sizes_equal_charged_arity", "seconds")}
    print(os.path.basename(path), r["count"], flags)
    groups = {}
    for row in r["rows"]:
        if "aborted" in row:
            continue
        a = groups.setdefault(row["group"], {"runs": 0, "H": set(), "queries_per_run": row["oracle_queries"],
                                             "cover_dims": row["cover_dims"], "stages": {}})
        a["runs"] += 1
        a["H"].add(row["instance"])
        for d, s in row["stages"].items():
            t = a["stages"].setdefault(d, {"schedule": s["schedule"], "kappa": s["kappa"], "M": s["charged_arity"],
                                           "blocks": 0, "full_solver": 0, "zero_col": 0, "diag": 0, "thm11": 0,
                                           "s2": 0, "sources": 0, "max_distinct": 0})
            t["blocks"] += s["blocks"]
            t["full_solver"] += s["full_solver_runs"]
            t["zero_col"] += s["zero_column_exits"]
            t["diag"] += s["diagnostic_nonzero_solves"]
            t["thm11"] += s["theorem11_calls"]
            t["s2"] += s["schedule2_calls"]
            t["sources"] += s["sources_measured"]
            t["max_distinct"] = max(t["max_distinct"], s["distinct_states_measured"])
    for g, a in groups.items():
        print(f"  {g} dims {a['cover_dims']}: {a['runs']} runs, {len(a['H'])} subgroups, "
              f"{a['queries_per_run']} queries per run")
        for d in sorted(a["stages"], key=int):
            print(f"    grade {d}: {a['stages'][d]}")

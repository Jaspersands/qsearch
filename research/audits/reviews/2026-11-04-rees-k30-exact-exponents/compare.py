"""K30: compare the exact-exponent reruns with the 2026-11-03 float-path artifacts.
Every check row and every seeded-run record is compared after dropping timing fields."""
import json
import os

A = "research/audits/reviews/2026-11-04-rees-k30-exact-exponents"
OLD2 = "research/audits/reviews/2026-11-03-rees-circuit-2"
OLD3 = "research/audits/reviews/2026-11-03-rees-circuit-3"


def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if "seconds" not in k}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x


def load(path):
    with open(path) as fh:
        return json.load(fh)


def by_key(rows, key=lambda r: r["instance"]):
    out = {}
    for r in rows:
        out.setdefault(key(r), []).append(strip(r))
    return out


def compare(label, old_rows, new_rows, key=lambda r: r["instance"]):
    old, new = by_key(old_rows, key), by_key(new_rows, key)
    common = sorted(set(old) & set(new), key=str)
    diff = [k for k in common if any(o != new[k][0] for o in old[k])]
    print(f"{label}: old {len(old_rows)} rows, new {len(new_rows)} rows, compared {len(common)} keys, "
          f"identical {len(common)-len(diff)}, differing {len(diff)}, only-old {sorted(set(old)-set(new), key=str)}, "
          f"only-new {sorted(set(new)-set(old), key=str)}")
    return len(common), len(diff)


summary = {}
new = load(f"{A}/report_exact.json")["runs"]
old = load(f"{OLD2}/report_main.json")["runs"]
for job in ("heis_f3", "n4_f5"):
    summary[job] = {
        "checks": compare(f"{job} checks", old[job]["checks"], new[job]["checks"]),
        "runs": compare(f"{job} seeded runs", old[job]["seeded_runs"], new[job]["seeded_runs"],
                        key=lambda r: (r["instance"], r["seed"])),
        "merge_proofs_identical": strip(old[job]["merge_proofs"]) == strip(new[job]["merge_proofs"]),
        "merge_bitlevel_identical": strip(old[job]["merge_bitlevel"]) == strip(new[job]["merge_bitlevel"]),
        "new_recovered": sum(r["recovered"] for r in new[job]["seeded_runs"]), "new_runs": len(new[job]["seeded_runs"]),
        "new_all_checks_pass": new[job]["all_checks_pass"], "new_instrument_modes": {d: v["mode"] for d, v in new[job]["instrument"].items()},
    }
    print(job, {k: v for k, v in summary[job].items() if k not in ("checks", "runs")})
if os.path.exists(f"{A}/n5_f5_exact.json"):
    o1, o2, n5 = load(f"{OLD3}/n5_f5.json"), load(f"{OLD3}/n5_f5_b.json"), load(f"{A}/n5_f5_exact.json")
    summary["n5_f5"] = {
        "checks": compare("n5_f5 checks", o1["checks"]+o2["checks"], n5["checks"]),
        "runs": compare("n5_f5 seeded runs", o1["seeded_runs"]+o2["seeded_runs"], n5["seeded_runs"],
                        key=lambda r: (r["instance"], r["seed"])),
        "new_recovered": sum(r["recovered"] for r in n5["seeded_runs"]), "new_runs": len(n5["seeded_runs"]),
        "new_all_checks_pass": n5.get("all_checks_pass"), "new_instrument_modes": {d: v["mode"] for d, v in n5["instrument"].items()},
    }
    print("n5_f5", {k: v for k, v in summary["n5_f5"].items() if k not in ("checks", "runs")})
if os.path.exists(f"{A}/n5_f5_exhaustive_exact.json"):
    o, n = load(f"{OLD3}/n5_f5_exhaustive.json"), load(f"{A}/n5_f5_exhaustive_exact.json")
    summary["n5_f5_exhaustive"] = {"checks": compare("n5_f5 exhaustive checks", o["checks"], n["checks"]),
                                   "new_all_checks_pass": n.get("all_checks_pass")}
    print("n5_f5_exhaustive", summary["n5_f5_exhaustive"])
with open(f"{A}/compare.json", "w") as fh:
    fh.write(json.dumps(summary, indent=1)+"\n")

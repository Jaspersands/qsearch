import json, glob, math
rows = []
for f in ("sweep_t_r.json", "sweep_27.json", "eta_runs.json", "large_runs.json"):
    try:
        data = json.load(open(f))
    except FileNotFoundError:
        continue
    data = data["results"] if isinstance(data, dict) else data
    for d in data:
        rows.append((f.split("_")[0], d["N"], d["t"], d["r"], d["tp"], d.get("eta", ""), d["sigma_max"], d.get("sigma_upper", d["sigma_max"]),
                     d["bound"]["B"], d["gates"]["total"], d["gate_bound"], d["qubits"]))
seen = set()
print("| set | N | t | r | tp | eta | sigma_max (float) | B (proved) | ok | gates | gate bound | qubits |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    if r[:6] in seen:
        continue
    seen.add(r[:6])
    print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]:.4f} | {r[8]:.4f} | {'yes' if r[7] <= r[8] else 'NO'} | {r[9]} | {r[10]} | {r[11]} |")

"""Collect every dfs2/dfs2b verdict line for kappa = 8, 9 and summarise E_2(8), E_2(9).

AI-written (10 Nov 2026), pending human review. Reads only; runs no search.
Usage: python -I collect.py REPO_ROOT > collect.out
"""
import re, sys, json
from pathlib import Path
from collections import defaultdict

root = Path(sys.argv[1])
R = root / "research/audits/reviews"
SRC = {
    "small-prime": sorted((R / "2026-11-02-rees-schedules/small-prime").glob("*.out")),
    "k9-sweep-out": sorted((R / "2026-11-04-rees-k9-sweep/out").glob("dfs*.out")),
    "local-queue": sorted((R / "2026-11-07-rees-dfs2b-local-queue/out").glob("*.out")),
    "cloud-late": [R / "2026-11-07-rees-cloud-late-results.txt"],
}
LINE = re.compile(r"^(?:[A-F] )?(FEASIBLE|INFEASIBLE|LIMIT) k=(\d+) p=(\d+)(.*)$")


def isprime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def program(src, f):
    name = f.name
    if src == "cloud-late":
        return "cloud"
    if src == "local-queue":
        return "dfs2b-plain" if name.endswith("_plain.out") else "dfs2b"
    if name.startswith("dfs2_"):
        return "dfs2"  # older unpruned search
    if "plain" in name:
        return "dfs2b-plain"
    if "nosym" in name:
        return "dfs2b-nosym"
    return "dfs2b"


ver = defaultdict(list)  # (k,p) -> [(verdict, program, file)]
wit = []
for src, files in SRC.items():
    for f in files:
        for line in f.read_text(errors="replace").splitlines():
            m = LINE.match(line.strip())
            if not m:
                continue
            v, k, p, rest = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
            if k not in (8, 9):
                continue
            prog = program(src, f)
            if src == "cloud-late":
                prog = "cloud-" + line.split()[0]
            ver[(k, p)].append((v, prog, str(f.relative_to(root))))
            if v == "FEASIBLE":
                g = re.search(r"g=(\d+)", rest)
                b = re.search(r"beta=([\d,]+)", rest)
                a = re.search(r"alpha=([\d,]+)", rest)
                if g and b and a:
                    wit.append({"k": k, "p": p, "g": int(g.group(1)),
                                "beta": [int(x) for x in b.group(1).split(",")],
                                "alpha": [int(x) for x in a.group(1).split(",")],
                                "file": str(f.relative_to(root))})

conflicts = []
final = {}
for key, lst in ver.items():
    vs = {v for v, _, _ in lst if v != "LIMIT"}
    if len(vs) > 1:
        conflicts.append((key, lst))
    final[key] = vs.pop() if len(vs) == 1 else ("LIMIT-only" if not vs else "CONFLICT")

print("conflicting verdicts:", len(conflicts))
for c in conflicts:
    print("  CONFLICT", c)

for k in (8, 9):
    ps = [p for p in range(k + 1, 20001, k) if isprime(p)]
    dec = [p for p in ps if final.get((k, p)) in ("FEASIBLE", "INFEASIBLE")]
    und = [p for p in ps if p not in dec]
    mem = [p for p in dec if final[(k, p)] == "INFEASIBLE"]
    print(f"kappa={k}: primes p=1 mod {k} up to 20000: {len(ps)}; decided {len(dec)}; undecided {len(und)} {und[:20]}")
    print(f"  members (INFEASIBLE) {len(mem)}; largest {max(mem)}; ratio largest/k^((k+1)/2) = {max(mem)/k**((k+1)/2):.4f}")
    print(f"  non-members (FEASIBLE) {len(dec)-len(mem)}")
    # which programs decided the primes above 16000
    progs = defaultdict(int)
    for p in dec:
        progs[tuple(sorted({pr for v, pr, _ in ver[(k, p)] if v != 'LIMIT'}))] += 1
    print("  program combinations over decided primes:")
    for pr, n in sorted(progs.items(), key=lambda t: -t[1]):
        print(f"    {n:4d}  {'+'.join(pr)}")
    json.dump({"members": mem, "nonmembers": [p for p in dec if p not in mem], "undecided": und},
              open(Path(__file__).with_name(f"E2_k{k}_le20000.json"), "w"))

# kappa = 9 exceptions above 20000
exc = [int(x) for x in (R / "2026-11-04-rees-k9-sweep/exceptions_20000_193710244.txt").read_text().split() if x.isdigit()]
print(f"kappa=9 sweep exceptions above 20000: {len(exc)} (largest {max(exc)})")
dec = [p for p in exc if final.get((9, p)) in ("FEASIBLE", "INFEASIBLE")]
mem = [p for p in dec if final[(9, p)] == "INFEASIBLE"]
print(f"  decided {len(dec)}: members {len(mem)} {mem}; non-members {[p for p in dec if p not in mem]}")
print(f"  undecided {len(exc)-len(dec)}; smallest undecided {min(p for p in exc if p not in dec)}")
print(f"  largest decided member {max(mem)}; ratio to 9^5 = {max(mem)/9**5:.4f}")
for p in dec:
    print(f"    {p} {final[(9,p)]} via {sorted({pr for v, pr, _ in ver[(9,p)] if v!='LIMIT'})}")
json.dump(wit, open(Path(__file__).with_name("witnesses.json"), "w"))
print("feasible witness lines collected:", len(wit), "distinct (k,p):", len({(w['k'], w['p']) for w in wit}))

# ---- unpruned cross-check coverage (dfs2 = older unpruned program, dfs2b plain mode, cloud D/E plain)
UNPRUNED = {"dfs2", "dfs2b-plain", "cloud-D", "cloud-E"}
for k in (8, 9):
    ps = [p for p in range(k + 1, 20001, k) if isprime(p)]
    unp = {p for p in ps if any(pr in UNPRUNED and v != "LIMIT" for v, pr, _ in ver[(k, p)])}
    agree = all({v for v, pr, _ in ver[(k, p)] if v != "LIMIT"} == {final[(k, p)]} for p in unp)
    pref = 0
    for p in ps:
        if p in unp:
            pref = p
        else:
            break
    mem = [p for p in ps if final[(k, p)] == "INFEASIBLE"]
    memu = [p for p in mem if p in unp]
    first_gap = next((p for p in mem if p not in unp), None)
    print(f"kappa={k}: unpruned verdict for {len(unp)} of {len(ps)} primes (all agree with pruned: {agree});"
          f" every prime up to {pref} has one; members with one: {len(memu)} of {len(mem)};"
          f" first member without one: {first_gap}; members without one: {len(mem)-len(memu)}")
    wp = {w['p'] for w in wit if w['k'] == k}
    nm = [p for p in ps if final[(k, p)] == "FEASIBLE"]
    print(f"  non-members with a stored witness: {len([p for p in nm if p in wp])} of {len(nm)};"
          f" without: {[p for p in nm if p not in wp]}")

for k, lo in ((8, 4202), (9, 5690)):
    ps = [p for p in range(k + 1, 20001, k) if isprime(p)]
    unp = {p for p in ps if any(pr in UNPRUNED and v != "LIMIT" for v, pr, _ in ver[(k, p)])}
    low = [p for p in ps if p < lo]
    print(f"kappa={k}: primes below {lo}: {len(low)}, with unpruned verdict here: {len([p for p in low if p in unp])}"
          f" (smallest with one {min(unp)})")
    mem_hi = [p for p in ps if p >= lo and final[(k, p)] == "INFEASIBLE"]
    X = lo
    for p in mem_hi:
        if p in unp:
            X = p
        else:
            break
    cov = [p for p in mem_hi if p in unp]
    print(f"  members >= {lo}: {len(mem_hi)}; every member in [{lo},{X}] has an unpruned verdict"
          f" ({len([p for p in mem_hi if p <= X])} members); first member without: "
          f"{next((p for p in mem_hi if p not in unp), None)}; members with one above {lo}: {len(cov)};"
          f" non-members >= {lo} with an unpruned verdict: {len([p for p in ps if p>=lo and p in unp and final[(k,p)]=='FEASIBLE'])}")

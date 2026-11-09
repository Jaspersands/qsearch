"""Aggregate out/*.json (attack groups) and out/climb_*.json into summary.json and print tables."""
import glob
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
fam_n = Counter()
group_n = Counter()
branch = Counter()
outcomes = Counter()
slack = {}
fails = []
bs = defaultdict(lambda: [0, 0, 0])   # key -> passes, failures, coincidences
maxload = 0
maxblocks = 0
for fn in sorted(glob.glob(os.path.join(HERE, "out", "*.json"))):
    base = os.path.basename(fn)
    if base.startswith("climb_") or "crashed" in base:
        continue
    d = json.load(open(fn))
    g = base.rsplit("_", 1)[0]
    for key, s in d["summary"].items():
        fam = key.split("|")[0]
        fam_n[fam] += s["n"]
        group_n[g] += s["n"]
        branch.update(s["branch"])
        outcomes.update(s["outcomes"])
        maxload = max(maxload, s["maxload"])
        maxblocks = max(maxblocks, s["maxblocks"])
        for k2, v in s["slack"].items():
            if k2 not in slack or v < slack[k2]:
                slack[k2] = v
        if s["passes"]:
            kk = g + ":" + "|".join(key.split("|")[1:3]) if g != "thmprime" else key.split("|")[0] + "|" + "|".join(key.split("|")[1:3])
            bs[kk][0] += s["passes"]
            bs[kk][1] += s["pass_fail"]
            bs[kk][2] += s["pass_coinc"]
    for key, fl in d.get("fails", {}).items():
        fails += fl
climb = {}
for fn in sorted(glob.glob(os.path.join(HERE, "out", "climb_*.json"))):
    d = json.load(open(fn))
    climb[os.path.basename(fn)] = d
    for k2, v in d["minslack"].items():
        if k2 not in slack or v < slack[k2]:
            slack[k2] = v
    branch.update({"climb:" + k: v for k, v in d["stats"].items()})
    fails += d["fails"]
res = dict(groups=dict(group_n), families=dict(fam_n), branch=dict(branch), outcomes=dict(outcomes),
           minslack=dict(sorted(slack.items())), nfails=len(fails), fails=fails[:50],
           backsub={k: dict(passes=v[0], fail=v[1], coinc=v[2]) for k, v in sorted(bs.items())},
           maxload=maxload, maxblocks=maxblocks)
json.dump(res, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
print(json.dumps(res, indent=1)[:12000])

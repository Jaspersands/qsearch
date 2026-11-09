"""Cross-check on the saved banks that reached rare branches (interesting/*.json).
Only banks run with the standard conventions (par_kw == {}) are compared (subquad.py has
no sigma/split options).  Usage: cross_interesting.py MAXRANK"""
import glob
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MAXR = int(sys.argv[1]) if len(sys.argv) > 1 else 40
sys.argv = [sys.argv[0], "0", "0"]
import cross  # noqa  (loads subquad and the comparison helpers)

out = open(os.path.join(HERE, "cross_interesting.jsonl"), "w")
tot = Counter()
seen = Counter()
for fn in sorted(glob.glob(os.path.join(HERE, "interesting", "*.json"))):
    d = json.load(open(fn))
    if d["par_kw"]:
        continue
    r = len(d["bank"][0])
    if r > MAXR:
        continue
    key = tuple(sorted(d["branch"]))
    if seen[key] >= 6:
        continue
    seen[key] += 1
    ag = cross.compare(os.path.basename(fn)[:-5], d["p"], d["k"], d["J"], d["bank"], out, 7)
    tot["banks"] += 1
    tot["agree"] += ag
    for b in d["branch"]:
        tot["br_" + b] += 1
    print(os.path.basename(fn), "agree" if ag else "DISAGREE", flush=True)
print("TOTAL", dict(tot))
out.write(json.dumps(dict(total=dict(tot))) + "\n")

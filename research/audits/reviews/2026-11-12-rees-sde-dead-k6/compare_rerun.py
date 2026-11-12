"""Compare deadcone.c (w2 mode: w2_validation.out), indep_cone.py (indep_cone.out) and
deadcone.c (tri mode: tri_crosscheck.out) with the 20 final rows of dead_w2_rerun.out.
Fields compared: m1, m2, #max_ext, #cand_3 (tri: m1, m2 only).
Run: /opt/anaconda3/bin/python -I compare_rerun.py
"""
import re

OLD = ("/Users/jaspersands/Developer/qsearch/research/audits/reviews/"
       "2026-11-11-rees-sde-near-linear-total/dead_w2_rerun.out")
HERE = "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-sde-dead-k6/"


def parse(fn):
    rows = {}
    for ln in open(HERE + fn):
        d = dict(re.findall(r"(\w+)=([0-9]+)", ln))
        if "kappa" in d and "m2" in d:
            rows[(int(d["kappa"]), int(d["p"]))] = d
    return rows


ref = {}
for ln in open(OLD):
    f = ln.split()
    if f and f[0].isdigit():
        ref[(int(f[0]), int(f[1]))] = dict(m1=f[3], m2=f[4], nmax_ext=f[5], ncand3=f[6])
w2, ind, tri = parse("w2_validation.out"), parse("indep_cone.out"), parse("tri_crosscheck.out")
bad = 0
for key, r in sorted(ref.items()):
    for name, src, fields in [("w2", w2, ["m1", "m2", "nmax_ext", "ncand3"]),
                              ("indep", ind, ["m1", "m2", "nmax_ext", "ncand3"]),
                              ("tri", tri, ["m1", "m2"])]:
        if key not in src:
            continue
        diff = [f for f in fields if src[key][f] != r[f]]
        bad += bool(diff)
        print(key, name, "MATCH" if not diff else f"DIFF {diff}")
print("reference rows:", len(ref), "mismatches:", bad)
new = sorted(k for k in w2 if k not in ref)
for k in new:
    a, b, c = w2[k], ind.get(k), tri.get(k)
    print("NEW", k, "w2", a["m1"], a["m2"], a["nmax_ext"], "| indep", b and (b["m1"], b["m2"], b["nmax_ext"]),
          "| tri", c and (c["m1"], c["m2"]))

"""Cross-check subquad.solve_T against my ALG-T on the saved banks that reached the top-phase
stall recursion T_m(b) (standard conventions only; ranks 44-50, above cross_interesting's cap)."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], "0", "0"]
import cross  # noqa
out = open(os.path.join(HERE, "cross_topstall.jsonl"), "w")
n = ag = 0
for fn in sorted(glob.glob(os.path.join(HERE, "interesting", "*top_stall_rec*.json"))):
    d = json.load(open(fn))
    if d["par_kw"]:
        print(os.path.basename(fn), "skipped (non-standard C)", flush=True)
        continue
    a = cross.compare(os.path.basename(fn)[:-5], d["p"], d["k"], d["J"], d["bank"], out, 7)
    n += 1; ag += a
    print(os.path.basename(fn), "r=%d" % len(d["bank"][0]), "agree" if a else "DISAGREE", flush=True)
print("TOTAL banks", n, "agree", ag)

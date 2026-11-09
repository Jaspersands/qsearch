"""Coverage check for the case-split SAT outputs (`*_split.out`).

For each split output, rebuild the set of --fix strings that run_split.sh / run_split_k.sh generate
from its case file (every Lemma U case, split over ALL p^k values of gamma_{(1,1),0}, an exact
cover) and require exactly one LRAT-VERIFIED UNSAT line per string; any SAT line, unverified line,
missing, duplicated or unexpected fix string is reported.  Replaces the hand check done for
cases11/cases13 and k3_7.

Usage (from this folder):  python check_split_cover.py [FILE ...]
With no argument the three completed outputs are checked.  Empty files (e.g. int13_split.out) are
reported as EMPTY: no coverage is claimed for them.
"""
import itertools, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASEFILE = {"cases11_split.out": "cases11.txt", "cases13_split.out": "cases13.txt",
            "k3_7_split.out": "cases7k3.txt"}
DEFAULT = ["cases11_split.out", "cases13_split.out", "k3_7_split.out"]
HEAD = re.compile(r"^p=(\d+) S=\[[^\]]*\] k=(\d+) d=(\d+) L=(\S+) .*?fix=(\S+): (UNSAT|SAT) \[[^\]]*\] (.*)$")


def expected(casefile, p, k):
    cases = [ln.strip() for ln in open(casefile) if ln.strip()]
    out = []
    for c in cases:
        for g in itertools.product(range(p), repeat=k):
            out.append((c + ";" if c else "") + "1,1,0:" + ",".join(map(str, g)))
    return out


def check(path):
    name = os.path.basename(path)
    lines = [ln for ln in open(path).read().splitlines() if ln.startswith("p=")]
    if not lines:
        return "EMPTY", f"{name}: no result lines; no coverage claimed"
    if name not in CASEFILE:
        return "UNKNOWN", f"{name}: no case file registered"
    p = k = None
    got, bad = {}, []
    for ln in lines:
        m = HEAD.match(ln)
        if not m:
            bad.append("unparsed: " + ln[:100]); continue
        p, k = int(m.group(1)), int(m.group(2))
        fix, res, info = m.group(5), m.group(6), m.group(7)
        if res != "UNSAT" or "'proof': 'LRAT VERIFIED'" not in info:
            bad.append(f"not a verified UNSAT: {fix} {res}")
        got[fix] = got.get(fix, 0) + 1
    exp = expected(os.path.join(HERE, CASEFILE[name]), p, k)
    es = set(exp)
    missing = [f for f in exp if f not in got]
    dup = [f for f, n in got.items() if n > 1]
    extra = [f for f in got if f not in es]
    ok = not (missing or dup or extra or bad) and len(exp) == len(es)
    ncases = len([l for l in open(os.path.join(HERE, CASEFILE[name])) if l.strip()])
    msg = (f"{name}: {len(exp) - len(missing)}/{len(exp)} expected sub-cases LRAT-verified UNSAT "
           f"(p={p}, k={k}, {ncases} cases); "
           f"missing {len(missing)}, duplicated {len(dup)}, unexpected {len(extra)}, bad lines {len(bad)}")
    return ("OK" if ok else "FAIL"), msg + ("" if ok else "\n  e.g. " + str((missing[:2], dup[:2], extra[:2], bad[:2])))


if __name__ == "__main__":
    files = sys.argv[1:] or DEFAULT
    status = 0
    for f in files:
        f = f if os.path.exists(f) else os.path.join(HERE, f)
        st, msg = check(f)
        print(st, msg)
        status |= st == "FAIL"
    sys.exit(status)

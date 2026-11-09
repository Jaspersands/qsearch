"""Equivalence check for the QS_BIGP=1 (object-dtype) arithmetic: run the SAME banks at primes
< 2^31 and compare branch counters, slacks and outcomes between the int64 build and the object
build.  Usage: bigp_equiv.py dump FILE   (any build)  ;  bigp_equiv.py compare A B
"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from la import Fq, BIGP
from harness import Tally, run_bank
import families

def dump(fn):
    out = []
    for (p, k, J, r, fam, seed) in [(100003, 3, 4, 12, f, s) for f in ("uniform", "planted", "nested", "adapt_rado", "adapt_top", "twist") for s in (1, 2)] + \
                                     [(10007, 2, 4, 14, f, s) for f in ("planted2", "repeat", "lines") for s in (1, 2)] + \
                                     [(100003, 3, 3, 16, f, s) for f in ("planted", "adapt_mix") for s in (1, 2)]:
        try:
            bank = families.make(fam, random.Random(seed), p, k, J, r)
        except Exception as e:
            out.append(dict(key=[p, k, J, r, fam, seed], gen_error=str(e)[:80])); continue
        T = Tally()
        o, rec, ex = run_bank(bank, p, k, J, T, passes=3, seed=seed, fd=Fq(p, k), save=False, tag="equiv")
        out.append(dict(key=[p, k, J, r, fam, seed], outcome=o, branch=dict(rec.branch), slack=rec.slack,
                        nf=ex.get("nf"), rho=ex.get("rho"), fails=T.fail))
    json.dump(dict(bigp=BIGP, runs=out), open(fn, "w"), indent=0, sort_keys=True, default=str)
    print("dumped", len(out), "bigp", BIGP)

def compare(a, b):
    A, B = json.load(open(a)), json.load(open(b))
    bad = 0
    for x, y in zip(A["runs"], B["runs"]):
        xx = {k: v for k, v in x.items()}; yy = {k: v for k, v in y.items()}
        if xx != yy:
            bad += 1; print("DIFF", x["key"])
    print("compared", len(A["runs"]), "runs; bigp flags", A["bigp"], B["bigp"], "; differences:", bad)

if __name__ == "__main__":
    if sys.argv[1] == "dump": dump(sys.argv[2])
    else: compare(sys.argv[2], sys.argv[3])

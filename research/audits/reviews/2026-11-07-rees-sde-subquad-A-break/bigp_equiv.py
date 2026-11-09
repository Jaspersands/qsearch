"""Equivalence check for the QS_BIGP=1 (object-dtype) arithmetic: run the SAME banks at primes
< 2^31 and compare branch counters, slacks and outcomes between the int64 build and the object
build.  Usage: bigp_equiv.py dump FILE   (any build)  ;  bigp_equiv.py compare A B
The bank set is the original 22 family banks plus (added 9 Nov, mechanical-queue audit P6) every
saved interesting/*case33_Uplus*.json bank (all have p < 2^31), replayed with its saved par_kw and
the seed in its file name, so the case-3.x branches used at the theorem prime are exercised too.
Saved results: out/bigp_equiv_int64.json, out/bigp_equiv_bigp.json, out/bigp_equiv_compare.out.
"""
import glob, json, os, random, re, sys
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
    for path in sorted(glob.glob(os.path.join(HERE, "interesting", "*case33_Uplus*.json"))):
        d = json.load(open(path))
        p, k, J = d["p"], d["k"], d["J"]
        assert p < 2 ** 31
        m = re.search(r"_(\d+)\.json$", path)
        seed = int(m.group(1)) if m else 0
        name = os.path.basename(path)
        bank = [list(map(int, v)) for v in d["bank"]]
        T = Tally()
        o, rec, ex = run_bank(bank, p, k, J, T, passes=3, seed=seed, fd=Fq(p, k), save=False, tag="equiv",
                              par_kw=d.get("par_kw") or None)
        out.append(dict(key=[p, k, J, len(bank), "interesting/" + name, seed], outcome=o, branch=dict(rec.branch),
                        slack=rec.slack, nf=ex.get("nf"), rho=ex.get("rho"), fails=T.fail))
    json.dump(dict(bigp=BIGP, runs=out), open(fn, "w"), indent=0, sort_keys=True, default=str)
    print("dumped", len(out), "bigp", BIGP)

def compare(a, b):
    A, B = json.load(open(a)), json.load(open(b))
    bad = 0
    if len(A["runs"]) != len(B["runs"]):
        bad += 1; print("DIFF run counts", len(A["runs"]), len(B["runs"]))
    for x, y in zip(A["runs"], B["runs"]):
        xx = {k: v for k, v in x.items()}; yy = {k: v for k, v in y.items()}
        if xx != yy:
            bad += 1; print("DIFF", x["key"])
    print("compared", len(A["runs"]), "runs; bigp flags", A["bigp"], B["bigp"], "; differences:", bad)
    rare = ("case30_Uplus", "case31_W", "top_stall_rec", "case33_top", "direct_top", "case33_Uplus",
            "case33_closure")
    for nm in rare:
        n = sum(1 for x in A["runs"] if (x.get("branch") or {}).get(nm))
        print("  runs reaching %s: %d" % (nm, n))
    print("  outcomes:", dict(sorted({o: sum(1 for x in A["runs"] if x.get("outcome") == o)
                                       for o in set(x.get("outcome") for x in A["runs"])}.items(),
                                      key=lambda t: str(t[0]))))

if __name__ == "__main__":
    if sys.argv[1] == "dump": dump(sys.argv[2])
    else: compare(sys.argv[2], sys.argv[3])

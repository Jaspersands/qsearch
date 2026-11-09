"""Cross-check my ALG-T (algt.py) against the agent's subquad.solve_T on shared banks.

Banks come from the agent's own generators (run_tests.py: planted, vtwist, topbank, degenerate,
the 12 Q1 families) and from my generators (families.py).  For each bank we compare the
sequence of stalls (depth, r, q, b, eps, pool size), the branch multiset and the leaf kind.
Usage: cross.py SEED NBANKS_PER_GROUP
"""
import os
import sys
import json
import random
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
AG = os.path.join(HERE, "..", "2026-11-07-rees-sde-subquad-A")
Q1 = os.path.join(HERE, "..", "2026-11-05-rees-sde-q1")
sys.path.insert(0, HERE)

from la import Fq  # noqa
from algt import Par, Rec, run_algt, Fail  # noqa
import checker  # noqa
import families  # noqa

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NB = int(sys.argv[2]) if len(sys.argv) > 2 else 2

# load the agent's code
sys.path.insert(0, AG)
sys.path.insert(0, Q1)
_argv = sys.argv
sys.argv = ["run_tests.py", "none", "0"]
src = open(os.path.join(AG, "run_tests.py")).read()
cut = src.rfind('{"heavy"')
ns = {"__file__": os.path.join(AG, "run_tests.py"), "__name__": "author_gens"}
exec(compile(src[:cut], "run_tests.py", "exec"), ns)
sys.argv = _argv
import subquad  # noqa

MAPK = {"leaf:thm2": "reach_V", "leaf:closure": "case1_closure", "leaf:absorbed": "case32_leafB",
        "leaf:closure-H": "case33_closure", "leaf:top": "top_leaf", "rec:Y": "case2_Y",
        "rec:U+": "case30_Uplus", "rec:W": "case31_W", "rec:H": "case33_Uplus",
        "rec:top-stall": "top_stall_rec", "direct": "direct_fwd", "top-direct": "direct_top",
        "zero": "zero_col"}
MINE = {"reach_V": "reach_V", "case1_closure": "case1_closure", "case32_leafB": "case32_leafB",
        "case33_closure": "case33_closure", "top_leaf": "top_leaf", "case2_Y": "case2_Y",
        "case30_Uplus": "case30_Uplus", "case31_W": "case31_W", "case33_Uplus": "case33_Uplus",
        "top_stall_rec": "top_stall_rec", "direct_fwd": "direct_fwd", "direct_top": "direct_top",
        "zero_col": "zero_col"}


def theirs(p, k, J, cols, seed):
    Fd = subquad.Field(p, k) if p < 200000 else ns["LightField"](p, k)
    P = subquad.Params(J, k, passes=5)
    st = subquad.new_stats()
    rng = random.Random(seed)
    try:
        x = subquad.solve_T(Fd, [list(v) for v in cols], P, rng, st)
        err = None
    except AssertionError as ex:
        x, err = None, "AssertionError " + repr(ex)[:200]
    br = Counter()
    for key, v in st.items():
        if key in MAPK and v:
            br[MAPK[key]] += v
    trace = [(t["depth"], t["r"], t["q"], t["b"], t["eps"], t["pi"]) for t in st.get("trace", [])]
    return dict(branch=br, trace=trace, x=x, err=err, leaf_fail=st["leaf_fail"],
                spf=st["single_pass_fail"], passes=st["passes"])


def mine(p, k, J, cols):
    Fd = Fq(p, k)
    par = Par(J, k)
    try:
        out, rec = run_algt(Fd, cols, par)
    except Fail as ex:
        return dict(err="Fail " + str(ex))
    br = Counter({MINE[k2]: v for k2, v in rec.branch.items() if k2 in MINE})
    trace = [(e["depth"], e["r"], e["q"], e["b"], e["eps"], e["pi"]) for e in rec.events]
    kind, obj = out
    probs = []
    if kind == "leaf":
        probs, info = checker.check_leaf([list(map(int, v)) for v in cols], p, k, J, obj, c=par.c)
    else:
        probs = checker.check_witness([list(map(int, v)) for v in cols], p, k, obj)
    return dict(branch=br, trace=trace, kind=kind, probs=probs, viol=rec.viol, err=None)


def compare(label, p, k, J, cols, out, seed):
    t0 = time.time()
    a = theirs(p, k, J, cols, seed)
    t1 = time.time()
    b = mine(p, k, J, cols)
    t2 = time.time()
    agree = (a["err"] is None and b["err"] is None and a["branch"] == b["branch"]
             and a["trace"] == b["trace"])
    rec = dict(label=label, p=p, k=k, J=J, M=len(cols), agree=agree,
               theirs=dict(branch=dict(a["branch"]), trace=a["trace"], err=a["err"],
                           solved=a["x"] is not None, leaf_fail=a["leaf_fail"]),
               mine=dict(branch=dict(b.get("branch", {})), trace=b.get("trace"), err=b["err"],
                         probs=b.get("probs"), viol=str(b.get("viol"))[:300]),
               t_theirs=round(t1 - t0, 2), t_mine=round(t2 - t1, 2))
    out.write(json.dumps(rec) + "\n")
    out.flush()
    if not agree:
        os.makedirs(os.path.join(HERE, "cross_disagree"), exist_ok=True)
        with open(os.path.join(HERE, "cross_disagree", "%s_%d.json" % (label.replace(" ", "_"), seed)), "w") as f:
            json.dump(dict(rec, bank=[list(map(int, v)) for v in cols]), f)
    return agree


def main():
    rng = random.Random(SEED)
    ns["rng"] = rng
    out = open(os.path.join(HERE, "cross_%d.jsonl" % SEED), "w")
    tot = Counter()
    jobs = []
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd = ns["Field"](p, k)
        for J in (3, 4):
            if J < k:
                continue
            P = subquad.Params(J, k)
            for a in (8, 12):
                M = P.F(a)
                nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
                fams = dict(ns["family_list"](rng, p, a, M, nr))
                for name, cols in ns["degenerate"](Fd, a, M).items():
                    fams[name] = (lambda c=cols: c)
                for name in sorted(fams)[:NB * 4]:
                    jobs.append(("fam_" + name, p, k, J, fams[name]))
        for J in (3,):
            P = subquad.Params(J, k)
            for r in (14, 18):
                for Qs in ([8], [6, 5]):
                    jobs.append(("planted_%d_%s" % (r, Qs), p, k, J,
                                 (lambda r=r, Qs=Qs, Fd=Fd, P=P: ns["planted"](Fd, r, Qs, J, P.F(r)))))
            for r in (24,):
                jobs.append(("vtwist_%d" % r, p, k, J,
                             (lambda r=r, Fd=Fd, P=P: ns["vtwist"](Fd, r, 8, J, P.F(r)))))
            for (r, b, kk, nrest, m, dg) in [(18, 5, 5, 7, 1, False), (20, 6, 5, 7, 2, False),
                                             (20, 6, 6, 6, 2, True), (16, 6, 4, 5, 1, False)]:
                jobs.append(("topbank_%d_%d" % (r, m), p, k, J,
                             (lambda a_=(r, b, kk, nrest, m, dg), Fd=Fd, P=P:
                              ns["topbank"](Fd, a_[0], a_[1], a_[2], a_[3], a_[4], J, P.F(a_[0]), a_[5]))))
    # my own families (shared with the attack runs)
    for (p, k) in [(10007, 2), (100003, 3)]:
        for J in (2, 3, 4):
            if J < k:
                continue
            for r in (10, 16):
                for fam in families.NAMES:
                    jobs.append(("my_" + fam + "_%d" % r, p, k, J,
                                 (lambda fam=fam, r=r, p=p, k=k, J=J:
                                  families.make(fam, random.Random(rng.random()), p, k, J, r))))
    for idx, (label, p, k, J, gen) in enumerate(jobs):
        try:
            cols = gen()
        except Exception:
            tot["gen_fail"] += 1
            continue
        if cols is None:
            continue
        ag = compare(label, p, k, J, cols, out, SEED * 1000 + idx)
        tot["banks"] += 1
        tot["agree"] += ag
        print(idx, label, "agree" if ag else "DISAGREE", flush=True)
    print("TOTAL", dict(tot))
    out.write(json.dumps(dict(total=dict(tot))) + "\n")


if __name__ == "__main__":
    main()

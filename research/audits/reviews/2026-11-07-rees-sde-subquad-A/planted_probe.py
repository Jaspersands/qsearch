"""Probe for the run_tests.py planted() fix (mechanical-queue audit 9 Nov, P7).

The audit's probe (same parameter grid: 2 fields x J in {3,4} x 11 shapes x mix x 4 repeats = 352
calls) counted the forward_fast 'direct' exits that happen after rounds were realised; there the
8 Nov fix used Omega = [] and dropped the Omega component of the later columns. planted() now uses
Omega = rebuild(Fd, st["rounds"]). This probe builds the banks only (no ALG-T solve) and counts
(a) generator errors, (b) direct exits, (c) direct exits with realised rounds, (d) how often the
rebuilt Omega is None (an (F1)/(F2) failure) or empty, and (e) the rank of Omega when non-empty.
usage: python -I planted_probe.py > planted_probe.out
"""
import os
import sys
import types
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["run_tests.py", "none", "1"]
sys.path.insert(0, HERE)
src = open(os.path.join(HERE, "run_tests.py")).read().split('\n{"heavy": group_heavy')[0]
ns = {"__name__": "run_tests_defs", "__file__": os.path.join(HERE, "run_tests.py")}
exec(compile(src, os.path.join(HERE, "run_tests.py"), "exec"), ns)
rt = types.SimpleNamespace(**ns)
Field = ns["Field"]

stats = Counter(errors=0, direct_rebuild_None=0)
last = {}
orig_forward = rt.forward
orig_rebuild = rt.rebuild


def spy_forward(Fd, cols, J, rng, st, rule="first"):
    res = orig_forward(Fd, cols, J, rng, st, rule=rule)
    last["res"], last["rounds"] = res, len(st["rounds"])
    if res == "direct":
        stats["direct"] += 1
        if st["rounds"]:
            stats["direct_with_rounds"] += 1
    return res


def spy_rebuild(Fd, rounds):
    Ub = orig_rebuild(Fd, rounds)
    if last.get("res") == "direct":
        if Ub is None:
            stats["direct_rebuild_None"] += 1
        elif not Ub:
            stats["direct_Omega_empty"] += 1
        else:
            stats["direct_Omega_rank_%d" % len(Ub)] += 1
    return Ub


ns["forward"] = spy_forward
ns["rebuild"] = spy_rebuild
for (p, k) in [(10007, 2), (100003, 3)]:
    Fd = Field(p, k)
    for J in (3, 4):
        for r, Qs in [(8, [1]), (8, [2]), (10, [1, 1]), (12, [3, 1]), (14, [5, 1]), (16, [6, 1]), (16, [4, 2, 1]),
                      (20, [6, 6]), (24, [8, 4]), (14, [7]), (18, [2, 2, 2])]:
            for mix in (False, True):
                for rep in range(4):
                    stats["calls"] += 1
                    last.clear()
                    try:
                        ns["planted"](Fd, r, Qs, J, 3 * r * r, mix)
                    except Exception as e:
                        stats["errors"] += 1
                        print("ERROR", p, k, J, r, Qs, mix, repr(e)[:80])
print(dict(sorted(stats.items())))
print("note: the fixed planted() draws extra random numbers for the Omega component, so the shared\n"
      "rng stream (and the bank sequence) diverges from the audit's probe after the first direct exit\n"
      "with realised rounds; the counts are therefore not those of the audit (127 / 87).")

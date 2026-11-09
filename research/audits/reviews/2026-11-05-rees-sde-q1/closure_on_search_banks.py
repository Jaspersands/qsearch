"""Lemma A on the search agent's critical-stall banks (read-only from ../2026-11-05-rees-sde-q1-search/banks).
Identity column order, Theorem-2 forward pass with swaps; at the stall, if eps = 0 (B cap U_L spans U_L),
back-substitute with the free columns lying in U_L (Lemma A).  Usage: closure_on_search_banks.py seed"""
import sys, os, json, glob, random
from q1core import Field, forward, init_state, free_cols, in_span, rank, steer_bad, run_backward, check

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "2026-11-05-rees-sde-q1-search", "banks")
tot = solved = 0
for fn in sorted(glob.glob(os.path.join(d, "*.json"))):
    bk = json.load(open(fn))
    Fd, cols = Field(bk["p"], bk["kappa"]), bk["cols"]
    p = Fd.p
    st = init_state(Fd, cols)
    status = forward(Fd, cols, 3, rng, st, rule="first")
    rounds, Ub, B = st["rounds"], st["Ub"], st["B"]
    r = len(B)
    line = [os.path.basename(fn), "M=%d" % len(cols), status]
    tot += 1
    if status == "stall":
        q = r - len(Ub)
        b = rank([cols[i] for i in B if in_span(Ub, cols[i], p)], p)[0]
        Fin = [i for i in free_cols(len(cols), rounds) if in_span(Ub, cols[i], p)]
        eps = len(Ub) - b
        line += ["q=%d" % q, "|B-U|=%d" % sum(1 for i in B if not in_span(Ub, cols[i], p)),
                 "unused=%d" % len(st["T"]), "pi=%d" % len(st["pool"]), "eps=%d" % eps]
        if eps == 0:
            nbad = steer_bad(Fd, cols, rounds, Ub, Fin)
            fails = 0
            x = None
            for _ in range(20):          # 20 single passes, count failures
                y = run_backward(Fd, cols, rounds, Ub, Fin, rng, 1)
                if y is None:
                    fails += 1
                else:
                    assert check(Fd, cols, y) and any(y)
                    x = y
            line += ["closure: bad functionals=%d" % nbad, "single-pass fails %d/20" % fails,
                     "SOLVED" if x is not None else "unsolved"]
            solved += x is not None
    elif status == "ok":
        x = run_backward(Fd, cols, rounds, Ub, B, rng, 12)
        line.append("thm2 " + ("SOLVED" if x is not None and check(Fd, cols, x) else "unsolved"))
        solved += x is not None
    print(*line, flush=True)
print("banks", tot, "solved by identity-order forward pass + Lemma A closure / Theorem 2:", solved)

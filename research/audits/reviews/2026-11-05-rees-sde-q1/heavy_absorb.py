"""On the saved heavy-stall banks (heavy_found_3.jsonl), redo forward passes until a stall whose
balanced absorption has load >= 3 appears, then absorb fully (Lemma R, 3+load blocks in one
round) and back-substitute with B (no recursion fallback).  Reports single-pass failure counts."""
import json, random
from q1core import Field, forward, init_state, rebuild, in_span, rank, run_backward, check, steer_bad
from alg_thm import absorb_balanced

rng = random.Random(5)
for ln, l in enumerate(open("heavy_found_3.jsonl")):
    d = json.loads(l)
    Fd, cols = Field(d["p"], d["k"]), d["cols"]
    p = Fd.p
    done = False
    for attempt in range(200):
        st = init_state(Fd, cols)
        if forward(Fd, cols, 3, rng, st) != "stall":
            continue
        rounds, Ub, B = st["rounds"], st["Ub"], st["B"]
        r = len(B)
        q = r - len(Ub)
        Rcols = [i for R in rounds for i in R.S]
        Fin = [i for i in range(len(cols)) if i not in Rcols and in_span(Ub, cols[i], p)]
        qplus = r - rank([cols[i] for i in Rcols + Fin], p)[0]
        if qplus != 0:
            continue
        trial = list(rounds)
        assert absorb_balanced(Fd, cols, trial, q)
        load = max(getattr(R, "extra", 0) for R in trial)
        if load < 3:
            continue
        Ub2 = rebuild(Fd, trial)
        assert len(Ub2) == r and steer_bad(Fd, cols, trial, Ub2, B) == 0
        fails = 0
        for _ in range(20):
            x = run_backward(Fd, cols, trial, Ub2, B, rng, 1)
            if x is None:
                fails += 1
            else:
                assert check(Fd, cols, x)
        print("bank", ln, "p", p, "k", d["k"], "a", d["a"], "q", q, "load", load,
              "max blocks", max(len(R.blocks) for R in trial), "single-pass fails %d/20" % fails, flush=True)
        done = True
        break
    if not done:
        print("bank", ln, "no heavy stall reproduced in 200 forward passes")

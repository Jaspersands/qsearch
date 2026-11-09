"""Diagnose the slow budgetC bank (k=3, J=5, r=24, C=2): regenerate the same seeds as
attack.py budgetC 1 and time ALG-T and each back-substitution pass separately."""
import random, sys, time, os, signal
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from la import Fq
from algt import Par, Rec, run_algt, BackSub
import families, checker
rng = random.Random(1)
target = (100003, 3, 5, int(sys.argv[1]) if len(sys.argv) > 1 else 24)
Fd = Fq(100003, 3)
class TO(Exception): pass
def h(*a): raise TO()
signal.signal(signal.SIGALRM, h)
for (p, k) in [(10007, 2), (100003, 3)]:
    for J in (4, 5):
        C = max(2, J - 3)
        for r in (12, 16, 20, 24, 30, 40):
            for fam in families.NAMES:
                for rep in range(2):
                    s = rng.randrange(10 ** 9)
                    if (p, k, J, r) != target:
                        continue
                    par = Par(J, k, C=C, rng=random.Random(s + 1))
                    bank = families.make(fam, random.Random(s), p, k, J, r, M=par.F(r))
                    t0 = time.time()
                    signal.alarm(120)
                    try:
                        out, rec = run_algt(Fd, bank, par, Rec())
                        ta = time.time() - t0
                        msg = "algt %.1fs %s %s" % (ta, out[0], dict(rec.branch))
                        if out[0] == "leaf":
                            leaf = out[1]
                            probs, info = checker.check_leaf([list(map(int, v)) for v in bank], p, k, J, leaf, c=par.c)
                            bs = BackSub(Fd, bank, leaf)
                            nb = [len(rr["blocks"]) for rr in leaf["rounds"]]
                            t1 = time.time()
                            x, inf = bs.one_pass(random.Random(s))
                            msg += " leafprobs=%s blocks=%s pass %.1fs ok=%s %s" % (probs, nb, time.time() - t1, x is not None, inf)
                    except TO:
                        msg = "TIMEOUT after %.0fs" % (time.time() - t0)
                    signal.alarm(0)
                    print(fam, rep, s, msg, flush=True)

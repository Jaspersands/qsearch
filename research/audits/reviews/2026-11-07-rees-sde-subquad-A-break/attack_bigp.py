"""J = 4, kappa = 3 INSIDE the theorem prime range (p >= max(8 kappa^{2E} E^2, 2 E r kappa^E),
E = 3J-2 = 10, i.e. p >= ~2.79e12), which needs arithmetic beyond p < 2^31: run with QS_BIGP=1
(la.py then uses dtype=object / Python ints; equivalence with the int64 build on 22 banks is
bigp_equiv.py).  Usage: QS_BIGP=1 attack_bigp.py SEED [seconds]
  fams      every family in families.NAMES, r in (8, 12, 16, 24), 2 repetitions, 30 back-substitution passes
  topstall  the topstall designs of attack.py (aimed at the top-phase stall, rank up to 56), 20 passes
Every leaf is checked by checker.py, every witness verified, every count and slack recorded
(harness.run_bank).  Artifacts: out/bigp_J4k3_<seed>.{out,json}.  Finite control only.
"""
import json, os, random, sys, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from la import Fq, is_prime, BIGP
from algt import Par
from harness import Tally, run_bank
import families

assert BIGP, "run with QS_BIGP=1"
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1
BUDGET = float(sys.argv[2]) if len(sys.argv) > 2 else 5400.0
J, K = 4, 3
E = 3 * J - 2
rng = random.Random(SEED)
LOG = open(os.path.join(HERE, "out", "bigp_J4k3_%d.out" % SEED), "w")

def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.write(s + "\n"); LOG.flush()

def next_prime(n, k):
    while not (is_prime(n) and (n - 1) % k == 0):
        n += 1
    return n

P = next_prime(8 * K ** (2 * E) * E * E, K)
RMAX = 56
assert P >= max(8 * K ** (2 * E) * E * E, 2 * E * RMAX * K ** E)
TALLY = {}
GENFAIL = Counter()
T0 = time.time()

def tally(key):
    if key not in TALLY:
        TALLY[key] = Tally()
    return TALLY[key]

def dump():
    out = {k: v.summary() for k, v in TALLY.items()}
    fails = {k: v.fail for k, v in TALLY.items() if v.fail}
    with open(os.path.join(HERE, "out", "bigp_J4k3_%d.json" % SEED), "w") as f:
        json.dump(dict(p=P, kappa=K, J=J, E=E, in_theorem_range=True, seed=SEED, summary=out, fails=fails,
                       generator_failures=dict(GENFAIL), elapsed_s=round(time.time() - T0)), f, indent=1, default=str)

def over():
    return time.time() - T0 > BUDGET

def main():
    log("p =", P, "kappa =", K, "J =", J, "E =", E, "bound 8 k^{2E} E^2 =", 8 * K ** (2 * E) * E * E)
    Fd = Fq(P, K)
    # topstall designs first (the structurally interesting banks), then families
    for rep in range(12):
        if over(): break
        s = rng.randrange(10 ** 9)
        r2 = random.Random(s)
        c = 2 * (J - 1)
        t = r2.choice([2, 3])
        PL = [r2.randrange(J - 1, c + 1) for _ in range(t)]
        m = r2.choice([2, 2, J - 2])
        bank = families.fam_design(r2, P, K, J, P_list=PL, m=m, b=sum(PL) + m + 1 + r2.choice([0, 1]),
                                   degenerate=True, tcount=sum(PL) + 1, rmax=RMAX)
        if bank is None:
            GENFAIL["topstall"] += 1; continue
        t0 = time.time()
        out, rec, ex = run_bank(bank, P, K, J, tally("topstall"), passes=20, fd=Fd, seed=s, save=True,
                                tag="bigp_topstall_r%d" % len(bank[0]))
        log("topstall r=%d %s %.0fs" % (len(bank[0]), out, time.time() - t0), dict(rec.branch),
            {x: ex.get(x) for x in ("rho", "nf", "nc", "bound")})
        dump()
    for r in (8, 12, 16, 24):
        for fam in families.NAMES:
            for rep in range(2):
                if over(): break
                s = rng.randrange(10 ** 9)
                try:
                    bank = families.make(fam, random.Random(s), P, K, J, r)
                except Exception as e:
                    GENFAIL[fam] += 1; log("generator failure", fam, r, str(e)[:60]); continue
                t0 = time.time()
                out, rec, ex = run_bank(bank, P, K, J, tally("fams|" + fam), passes=30, fd=Fd, seed=s, save=True,
                                        tag="bigp_%s_r%d" % (fam, r))
                log("fam", fam, "r=%d %s %.0fs" % (r, out, time.time() - t0), dict(rec.branch),
                    {x: ex.get(x) for x in ("rho", "nf", "nc", "bound")})
        dump()
    dump()
    tot, br, nf, passes, pf = Counter(), Counter(), 0, 0, 0
    for v in TALLY.values():
        tot.update(v.outcomes); br.update(v.branch); nf += len(v.fail); passes += v.passes; pf += v.pass_fail
    log("TOTAL banks", sum(v.n for v in TALLY.values()), dict(tot), "assertion/check failures", nf,
        "backsub passes", passes, "backsub failures", pf, "generator failures", dict(GENFAIL),
        "time %.0fs" % (time.time() - T0))
    log("BRANCHES", dict(br))

if __name__ == "__main__":
    main()

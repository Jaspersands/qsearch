"""Attack driver.  Usage: attack.py GROUP SEED [extra]

GROUP:
  fams      all my families, kappa in {2,3}, J in {2,3,4} (J >= kappa), r in {8..40}, p = 10007/100003
  conv      same banks, alternative conventions (sigma index/random, random split, random
            absorption order, random Z) -- the theorem must hold for every convention
  agent     the agent's generators (planted, vtwist, topbank, degenerate, Q1 families),
            run by MY implementation
  thmprime  primes inside the theorem range (J = 2, 3; kappa = 2, 3; J = 4 kappa = 2), many
            back-substitution passes, failure rate vs the Lemma 2 bound
  smallp    small primes p in {3,5,7,11,13,17,31} (kappa=2) and {7,13,19,31,37} (kappa=3),
            deterministic part + back-substitution rates (no bound claimed there)
  budgetC   the side claim C = max(2, J-3) (section 5, T_m(c)) at J = 4, 5
Every leaf is checked by checker.py, every witness verified, every count recorded.
"""
import json
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from la import Fq, is_prime  # noqa
from algt import Par  # noqa
from harness import Tally, run_bank  # noqa
import families  # noqa

GROUP = sys.argv[1]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
EXTRA = sys.argv[3] if len(sys.argv) > 3 else ""
rng = random.Random(SEED)
TAGX = (GROUP + EXTRA) if EXTRA == "rest" else GROUP
LOG = open(os.path.join(HERE, "out", "%s_%d.out" % (TAGX, SEED)), "w")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def next_prime(n, k):
    n = max(n, 3)
    while not (is_prime(n) and (n - 1) % k == 0):
        n += 1
    return n


TALLY = {}


def tally(key):
    if key not in TALLY:
        TALLY[key] = Tally()
    return TALLY[key]


def dump():
    out = {k: v.summary() for k, v in TALLY.items()}
    fails = {k: v.fail for k, v in TALLY.items() if v.fail}
    with open(os.path.join(HERE, "out", "%s_%d.json" % (TAGX, SEED)), "w") as f:
        json.dump(dict(summary=out, fails=fails), f, indent=1, default=str)


def fams_group(conv=False, rs=(8, 12, 16, 20, 24, 30, 40), reps=None, passes=10):
    Fds = {}
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fds[p] = Fq(p, k)
        for J in (2, 3, 4):
            if J < k:
                continue
            for r in rs:
                nrep = reps or (3 if r <= 16 else (2 if r <= 24 else 1))
                for fam in families.NAMES:
                    for rep in range(nrep):
                        s = rng.randrange(10 ** 9)
                        t0 = time.time()
                        try:
                            bank = families.make(fam, random.Random(s), p, k, J, r)
                        except Exception as ex:
                            log("GENFAIL", fam, k, J, r, repr(ex))
                            continue
                        variants = [("std", {})]
                        if fam.startswith("adapt"):
                            variants.append(("sigidx", dict(sigma_place="index")))
                        if conv:
                            variants = [("sigidx", dict(sigma_place="index")),
                                        ("sigrand", dict(sigma_rule="random")),
                                        ("split_rand", dict(split_rule="random")),
                                        ("abs_rand", dict(abs_order="random", z_rule="random")),
                                        ("zcert_fromX1", dict(zcert="fromX1"))]
                        for vn, kw in variants:
                            T = tally("%s|k%d|J%d|%s" % (fam, k, J, vn))
                            out, rec, ex = run_bank(bank, p, k, J, T, passes=passes,
                                                    tag="%s_k%d_J%d_r%d_%s" % (fam, k, J, r, vn),
                                                    par_kw=kw, seed=s, fd=Fds[p])
                            if T.fail and len(T.fail) and ex.get("saved"):
                                log("FAILURE", fam, k, J, r, vn, T.fail[-1], ex.get("saved"))
                        log("done", fam, "k=%d J=%d r=%d rep=%d %.1fs" % (k, J, r, rep, time.time() - t0),
                            dict(rec.branch))
                dump()


def agent_group():
    """The agent's generators, run by my implementation."""
    AG = os.path.join(HERE, "..", "2026-11-07-rees-sde-subquad-A")
    Q1 = os.path.join(HERE, "..", "2026-11-05-rees-sde-q1")
    sys.path.insert(0, AG)
    sys.path.insert(0, Q1)
    argv = sys.argv
    sys.argv = ["run_tests.py", "none", "0"]
    src = open(os.path.join(AG, "run_tests.py")).read()
    ns = {"__file__": os.path.join(AG, "run_tests.py"), "__name__": "author_gens"}
    exec(compile(src[:src.rfind('{"heavy"')], "run_tests.py", "exec"), ns)
    sys.argv = argv
    ns["rng"] = rng
    import subquad
    for (p, k) in [(10007, 2), (100003, 3)]:
        Fd = ns["Field"](p, k)
        myFd = Fq(p, k)
        for J in (3, 4):
            if J < k:
                continue
            P = subquad.Params(J, k)
            jobs = []
            for r in (16, 20, 24, 28, 32, 36, 40):
                for Qs in ([r // 2], [r // 2 - 2], [r // 3, r // 4]):
                    jobs.append(("planted", lambda r=r, Qs=Qs: ns["planted"](Fd, r, Qs, J, P.F(r))))
            for r in (24, 28, 32, 36, 40):
                for Q in (8, 10):
                    jobs.append(("vtwist", lambda r=r, Q=Q: ns["vtwist"](Fd, r, Q, J, P.F(r))))
            shapes = [(18, 5, 5, 7, 1, False), (20, 6, 5, 7, 2, False), (22, 7, 5, 7, 3, False),
                      (20, 6, 6, 6, 2, True), (22, 7, 5, 8, 2, True), (16, 6, 4, 5, 1, False),
                      (26, 8, 5, 9, 4, False), (40, 4, 4, 30, 2, True), (40, 4, 4, 30, 2, False)]
            for sh in shapes:
                jobs.append(("topbank", lambda sh=sh: ns["topbank"](Fd, sh[0], sh[1], sh[2], sh[3], sh[4], J,
                                                                    P.F(sh[0]), sh[5])))
            for a in (8, 12, 16):
                M = P.F(a)
                nr = next(z for z in range(2, p) if Fd.cls(z) != 0)
                fl = dict(ns["family_list"](rng, p, a, M, nr))
                for name, cols in ns["degenerate"](Fd, a, M).items():
                    fl[name] = (lambda c=cols: c)
                for name, g in fl.items():
                    jobs.append(("q1fam_" + name, g))
            for name, g in jobs:
                try:
                    bank = g()
                except Exception:
                    tally("gen_fail").n += 1
                    continue
                r = len(bank[0])
                T = tally("agent_%s|k%d|J%d" % (name, k, J))
                t0 = time.time()
                out, rec, ex = run_bank(bank, p, k, J, T, passes=10, tag="agent_" + name, fd=myFd,
                                        seed=rng.randrange(10 ** 9))
                log("done", name, "k=%d J=%d a=%d M=%d %.1fs" % (k, J, r, len(bank), time.time() - t0),
                    dict(rec.branch), "FAIL" if ex.get("saved") else "")
            dump()


def thmprime_group(passes=200):
    cases = []
    jk = [(2, 2), (3, 2), (3, 3), (4, 2)]
    rs = (8, 12, 16, 24, 32, 40)
    below = True
    if EXTRA == "reduced":
        jk, rs, below, passes = [(3, 2), (3, 3), (4, 2)], (8, 16, 24, 40), True, 100
    for (J, k) in jk:
        E = 3 * J - 2
        for r in rs:
            thr = max(8 * k ** (2 * E) * E * E, 2 * E * r * k ** E)
            if thr >= 2 ** 31:
                continue
            cases.append((J, k, r, next_prime(thr, k), "in"))
    # J = 2: also primes just below the range and far below
    for r in ((8, 16, 24, 40) if below else ()):
        for p in (next_prime(4000, 2), next_prime(30000, 2), next_prime(1009, 2)):
            cases.append((2, 2, r, p, "below"))
    if EXTRA == "reduced":
        cases += [(3, 3, r, next_prime(100000, 3), "below") for r in (8, 16, 24)]
        cases += [(3, 2, r, next_prime(100000, 2), "below") for r in (8, 16, 24)]
    Fds = {}
    if EXTRA == "below3":
        cases = [(3, 2, r, next_prime(100000, 2), "below") for r in (8, 16, 24)]
    for (J, k, r, p, where) in cases:
        if (p, k) not in Fds:
            Fds[(p, k)] = Fq(p, k)
        for fam in families.NAMES:
            nrep = (2 if r <= 16 else 1) if EXTRA not in ("reduced", "below3") else 1
            for rep in range(nrep):
                s = rng.randrange(10 ** 9)
                bank = families.make(fam, random.Random(s), p, k, J, r)
                T = tally("thm_%s|J%d|k%d|%s" % (where, J, k, fam))
                t0 = time.time()
                out, rec, ex = run_bank(bank, p, k, J, T, passes=passes if r <= 24 else passes // 2,
                                        tag="thm_%s_J%d_k%d_r%d_%s" % (where, J, k, r, fam), fd=Fds[(p, k)], seed=s)
                log("done", where, fam, "J=%d k=%d r=%d p=%d %.1fs" % (J, k, r, p, time.time() - t0),
                    dict(rec.branch), {x: ex.get(x) for x in ("rho", "nf", "nc", "bound")})
        dump()


def smallp_group(passes=30):
    Fds = {}
    for (k, ps) in [(2, (3, 5, 7, 11, 13, 17, 31)), (3, (7, 13, 19, 31, 37))]:
        for p in ps:
            Fds[(p, k)] = Fq(p, k)
            for J in (2, 3, 4):
                if J < k:
                    continue
                for r in (4, 6, 8, 12, 16):
                    for fam in families.NAMES:
                        for rep in range(3):
                            s = rng.randrange(10 ** 9)
                            try:
                                bank = families.make(fam, random.Random(s), p, k, J, r)
                            except Exception as ex:
                                log("GENFAIL", fam, p, k, J, r, repr(ex))
                                continue
                            T = tally("small|k%d|J%d|p%d" % (k, J, p))
                            out, rec, ex = run_bank(bank, p, k, J, T, passes=passes, fd=Fds[(p, k)],
                                                    tag="small_p%d_J%d_r%d_%s" % (p, J, r, fam), seed=s)
                    log("done p=%d k=%d J=%d r=%d" % (p, k, J, r), T.summary()["outcomes"],
                        T.summary()["branch"])
                dump()


def budgetC_group():
    """C = max(2, J-3) instead of max(2, 2J-4) (the report's sharper side claim, sec 5(c))."""
    Fds = {10007: Fq(10007, 2), 100003: Fq(100003, 3)}
    for (p, k) in [(10007, 2), (100003, 3)]:
        for J in (4, 5):
            C = max(2, J - 3)
            for r in (12, 16, 20, 24, 30, 40):
                for fam in families.NAMES:
                    for rep in range(2):
                        s = rng.randrange(10 ** 9)
                        if EXTRA == "rest" and not (k == 3 and J == 5 and r >= 24):
                            continue   # resume after the run killed at k=3, J=5, r=24 (sampler cap)
                        par = Par(J, k, C=C)
                        bank = families.make(fam, random.Random(s), p, k, J, r, M=par.F(r))
                        T = tally("budgetC|k%d|J%d|%s" % (k, J, fam))
                        out, rec, ex = run_bank(bank, p, k, J, T, passes=0 if EXTRA == "rest" else 5,
                                                par_kw=dict(C=C), fd=Fds[p],
                                                tag="budgetC_J%d_r%d_%s" % (J, r, fam), seed=s)
                if EXTRA == "rest" and not (k == 3 and J == 5 and r >= 24):
                    continue
                log("done budgetC k=%d J=%d r=%d" % (k, J, r))
                dump()


def topstall_group():
    """Designs aimed at Lemma T_m(b) (top-phase stall, m = 2, J in {4, 5}), ranks 36-56,
    at p = 10007/100003 and, for J = 4, kappa = 2, at the theorem prime."""
    Fds = {}
    for (p, k, J) in [(10007, 2, 4), (100003, 3, 4), (10007, 2, 5), (100003, 3, 5),
                      (next_prime(8 * 2 ** 20 * 100, 2), 2, 4)]:
        if (p, k) not in Fds:
            Fds[(p, k)] = Fq(p, k)
        c = 2 * (J - 1)
        for rep in range(12):
            s = rng.randrange(10 ** 9)
            if EXTRA == "rest" and (p, k, J) in [(10007, 2, 4), (100003, 3, 4), (10007, 2, 5)]:
                continue   # resume after the run killed in (100003, 3, 5) (sampler cap, below range)
            r2 = random.Random(s)
            t = r2.choice([2, 3])
            PL = [r2.randrange(J - 1, c + 1) for _ in range(t)]
            m = r2.choice([2, 2, J - 2]) if J >= 4 else 1
            bank = families.fam_design(r2, p, k, J, P_list=PL, m=m, b=sum(PL) + m + 1 + r2.choice([0, 1]),
                                       degenerate=True, tcount=sum(PL) + 1, rmax=56)
            if bank is None:
                continue
            T = tally("topstall|k%d|J%d|p%d" % (k, J, p))
            t0 = time.time()
            npass = 0 if (EXTRA == "rest" and (p, k, J) == (100003, 3, 5)) else 20
            out, rec, ex = run_bank(bank, p, k, J, T, passes=npass, fd=Fds[(p, k)], seed=s,
                                    tag="topstall_J%d_k%d_r%d" % (J, k, len(bank[0])))
            log("done topstall p=%d k=%d J=%d r=%d %.0fs" % (p, k, J, len(bank[0]), time.time() - t0),
                dict(rec.branch), {x: ex.get(x) for x in ("rho", "nf", "bound")})
        dump()


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    t0 = time.time()
    if GROUP == "fams":
        fams_group()
    elif GROUP == "conv":
        fams_group(conv=True, rs=(8, 12, 16, 24, 32), reps=1, passes=5)
    elif GROUP == "agent":
        agent_group()
    elif GROUP == "thmprime":
        thmprime_group()
    elif GROUP == "smallp":
        smallp_group()
    elif GROUP == "topstall":
        topstall_group()
    elif GROUP == "budgetC":
        budgetC_group()
    dump()
    tot = Counter()
    br = Counter()
    nf = 0
    for v in TALLY.values():
        tot.update(v.outcomes)
        br.update(v.branch)
        nf += len(v.fail)
    log("TOTAL", GROUP, SEED, "banks", sum(v.n for v in TALLY.values()), dict(tot), "fails", nf,
        "time %.0fs" % (time.time() - t0))
    log("BRANCHES", dict(br))

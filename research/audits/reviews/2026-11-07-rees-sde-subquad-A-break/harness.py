"""Run my ALG-T on a bank, check everything independently, run back substitution."""
import json
import os
import random
import time
from collections import Counter

import numpy as np

from la import Fq
from algt import Par, Rec, Fail, run_algt, BackSub, DJ
import checker

HERE = os.path.dirname(os.path.abspath(__file__))
FAILDIR = os.path.join(HERE, "failures")


def save_failure(tag, bank, p, k, J, info):
    os.makedirs(FAILDIR, exist_ok=True)
    fn = os.path.join(FAILDIR, "%s_%d.json" % (tag, int(time.time() * 1000) % 10 ** 9))
    with open(fn, "w") as f:
        json.dump(dict(p=p, k=k, J=J, bank=[list(map(int, v)) for v in bank], info=str(info)), f)
    return fn


class Tally:
    def __init__(self):
        self.n = 0
        self.branch = Counter()
        self.slack = {}
        self.slack_ctx = {}
        self.fail = []
        self.passes = 0
        self.pass_fail = 0
        self.pass_coinc = 0
        self.bound_sum = 0.0
        self.max_rate_ratio = 0.0
        self.leafkinds = Counter()
        self.maxload = 0
        self.maxblocks = 0
        self.time = 0.0
        self.outcomes = Counter()

    def merge_rec(self, rec):
        self.branch.update(rec.branch)
        for k, v in rec.slack.items():
            if k not in self.slack or v < self.slack[k]:
                self.slack[k] = v
        if rec.loads:
            self.maxload = max(self.maxload, max(rec.loads))

    def summary(self):
        return dict(n=self.n, outcomes=dict(self.outcomes), branch=dict(self.branch),
                    leafkinds=dict(self.leafkinds), slack=dict(sorted(self.slack.items())),
                    fails=len(self.fail), passes=self.passes, pass_fail=self.pass_fail,
                    pass_coinc=self.pass_coinc, maxload=self.maxload, maxblocks=self.maxblocks,
                    time=round(self.time, 1))


def G_lower(p, k, E):
    """Lemma W lower bound on G*_E(p) (min over e <= E); may be <= 0."""
    best = None
    for e in range(1, E + 1):
        v = (p - e - (k ** e - 1) * (e - 1) * p ** 0.5) / k ** e
        best = v if best is None else min(best, v)
    return best


def run_bank(bank, p, k, J, tally, passes=0, tag="bank", par_kw=None, seed=0, fd=None,
             save=True):
    """Returns (outcome, rec, extra)."""
    t0 = time.time()
    Fd = fd or Fq(p, k)
    assert (Fd.p, Fd.k) == (p, k), "field cache mismatch"
    rng = random.Random(seed)
    par = Par(J, k, rng=random.Random(seed + 1), **(par_kw or {}))
    tally.n += 1
    rec = Rec()
    extra = {}
    try:
        out, rec = run_algt(Fd, bank, par, rec)
    except Fail as ex:
        tally.fail.append((tag, "Fail:" + str(ex)))
        tally.outcomes["FAIL"] += 1
        if save:
            extra["saved"] = save_failure(tag + "_fail", bank, p, k, J, str(ex))
        tally.merge_rec(rec)
        tally.time += time.time() - t0
        return "FAIL", rec, extra
    tally.merge_rec(rec)
    rare = [b for b in ("case30_Uplus", "case31_W", "top_stall_rec", "case33_top", "direct_top",
                        "case33_Uplus", "case33_closure") if rec.branch.get(b)]
    if rare and save:
        d = os.path.join(HERE, "interesting")
        os.makedirs(d, exist_ok=True)
        key = "_".join(sorted(rare))
        cnt = len([f for f in os.listdir(d) if f.startswith(key)])
        if cnt < 25:
            with open(os.path.join(d, "%s_%s_%d.json" % (key, tag, seed)), "w") as f:
                json.dump(dict(p=p, k=k, J=J, par_kw=par_kw or {}, branch=dict(rec.branch),
                               bank=[list(map(int, v)) for v in bank]), f)
    if rec.viol:
        tally.fail.append((tag, "viol:" + str(rec.viol[:3])))
        tally.outcomes["VIOL"] += 1
        if save:
            extra["saved"] = save_failure(tag + "_viol", bank, p, k, J, rec.viol[:5])
    kind, obj = out
    blist = [list(map(int, v)) for v in bank]
    if kind == "solution":
        pr = checker.check_witness(blist, p, k, obj)
        if pr:
            tally.fail.append((tag, "bad direct witness " + str(pr)))
            tally.outcomes["BADWIT"] += 1
            if save:
                extra["saved"] = save_failure(tag + "_badwit", bank, p, k, J, pr)
        else:
            tally.outcomes["solution"] += 1
        tally.time += time.time() - t0
        return "solution", rec, extra
    leaf = obj
    tally.leafkinds[leaf["kind"]] += 1
    probs, info = checker.check_leaf(blist, p, k, J, leaf, c=par.c)
    extra["leafinfo"] = info
    tally.maxblocks = max(tally.maxblocks, info.get("maxblocks", 0))
    if probs:
        tally.fail.append((tag, "leaf " + str(probs)))
        tally.outcomes["BADLEAF"] += 1
        if save:
            extra["saved"] = save_failure(tag + "_badleaf", bank, p, k, J, probs)
        tally.time += time.time() - t0
        return "BADLEAF", rec, extra
    tally.outcomes["leaf"] += 1
    if passes:
        bs = BackSub(Fd, bank, leaf)
        nf = nc = 0
        for _ in range(passes):
            x, inf = bs.one_pass(rng)
            nc += inf["coinc"] > 0
            if x is None:
                nf += 1
                continue
            pr = checker.check_witness(blist, p, k, x)
            if pr:
                tally.fail.append((tag, "bad backsub witness " + str(pr)))
                if save:
                    extra["saved"] = save_failure(tag + "_badbs", bank, p, k, J, pr)
                break
        tally.passes += passes
        tally.pass_fail += nf
        tally.pass_coinc += nc
        E = 3 * J - 2
        gl = G_lower(p, k, E)
        bound = bs.rho * max(1.0 / gl, k / (p - 1)) if gl and gl > 0 else float("inf")
        extra.update(rho=bs.rho, nf=nf, nc=nc, bound=bound, dim=bs.dim)
        # rate check: flag only clear excess (> bound + 4 sigma) when the bound is < 1
        if bound < 1:
            rate = nf / passes
            sd = (bound * (1 - bound) / passes) ** 0.5
            if rate > bound + 4 * sd + 2.0 / passes:
                tally.fail.append((tag, "backsub rate %.3f > bound %.3f" % (rate, bound)))
                if save:
                    extra["saved"] = save_failure(tag + "_rate", bank, p, k, J,
                                                  dict(rate=rate, bound=bound))
    tally.time += time.time() - t0
    return "leaf", rec, extra

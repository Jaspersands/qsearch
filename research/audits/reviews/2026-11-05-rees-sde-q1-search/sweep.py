"""Structured-family sweep against Conjecture 5.
usage: sweep.py <tag> <seed> <kappa:p:a1,a2,..>... [--M=budget|cw|all] [--n=6] [--K=4]
For every bank: Theorem-2 forward pass on the identity order (pi, status), K single
sss_full iterations on orders identity + random (per-order failure rate), and sss_full
(forwards=3) when the identity order fails.  Failures of sss_full are re-checked with
the independent solver (indep.py) and saved with their stall certificates."""
import json
import random
import sys
import time
from q1lib import (Field, budget, theorem_forward, one_order, sss_full, check, D3,
                   fam_lines, fam_planes, fam_flag_subthreshold, fam_codim1, fam_codim1_front,
                   fam_lines_planes, fam_random, fam_basis_dense, fam_pairs)
from critical import chain4, chainfull
import indep

args = [s for s in sys.argv[1:] if not s.startswith("--")]
opts = dict(s[2:].split("=") for s in sys.argv[1:] if s.startswith("--"))
tag, seed = args[0], int(args[1])
confs = []
for s in args[2:]:
    k, p, As = s.split(":")
    confs.append((int(k), int(p), [int(x) for x in As.split(",")]))
NB, K, Mmode = int(opts.get("n", 6)), int(opts.get("K", 4)), opts.get("M", "budget")
rng = random.Random(seed)
out_fail = open("out/%s_failures.jsonl" % tag, "a")
out_rows = open("out/%s_rows.jsonl" % tag, "a")


def families(Fd, a, M):
    p = Fd.p
    only = opts.get("fams")
    fams = {
        "random": lambda: fam_random(rng, p, a, M),
        "lines_a+1": lambda: fam_lines(rng, p, a, M, a + 1),
        "lines_a": lambda: fam_lines(rng, p, a, M, a),
        "pairs": lambda: fam_pairs(rng, p, a, M),
        "planes5": lambda: fam_planes(rng, p, a, M, max(2, -(-M // 5))),
        "flats3_8": lambda: fam_planes(rng, p, a, M, max(2, -(-M // 8)), dim=min(3, a - 1)),
        "lines+planes": lambda: fam_lines_planes(rng, p, a, M, a // 2 + 1, a // 2 + 1),
        "flag_sub": lambda: fam_flag_subthreshold(rng, p, a, M),
        "codim1_2": lambda: fam_codim1(rng, p, a, M, 2),
        "codim1_3": lambda: fam_codim1(rng, p, a, M, 3),
        "codim1_front_2": lambda: fam_codim1_front(rng, p, a, M, 2),
        "basis_dense": lambda: fam_basis_dense(rng, p, a, M, max(1, a // 2)),
        "chain4": lambda: chain4(Fd, rng, a, M),
    }
    if Fd.k == 3:
        fams["chainfull"] = lambda: chainfull(Fd, rng, a, M)
    if only:
        fams = {n: g for n, g in fams.items() if n in only.split(",")}
    return fams


t0 = time.time()
for (k, p, As) in confs:
    Fd = Field(p, k)
    for a in As:
        Mb = budget(a, 3)
        if Mmode == "budget":
            Ms = [Mb]
        else:
            lo = {"cw": k * a + 1, "2a": 2 * a + 1}.get(Mmode, a + 2)
            Ms = list(range(lo, Mb + 1))
        for M in Ms:
            for name, gen in families(Fd, a, M).items():
                row = dict(family=name, kappa=k, p=p, a=a, M=M, banks=0, solved=0,
                           id_stalls=0, id_fail=0, order_fail=0, orders=0, max_pi=0, pi_sum=0,
                           crit=0)
                for t in range(NB):
                    cols = gen()
                    row["banks"] += 1
                    tf = theorem_forward(Fd, cols, rng=rng)
                    pi = tf.get("pi", 0)
                    row["max_pi"] = max(row["max_pi"], pi)
                    row["pi_sum"] += pi
                    if tf["status"] == "stall":
                        row["id_stalls"] += 1
                        if tf["unused"] == 0 and tf["BoutU"] == tf["q"]:
                            row["crit"] += 1
                    idfail, cert0 = False, None
                    for o in range(K):
                        perm = list(range(M))
                        if o:
                            rng.shuffle(perm)
                        x, st, cert = one_order(Fd, cols, perm, rng, passes=10)
                        row["orders"] += 1
                        if x is None:
                            row["order_fail"] += 1
                            if o == 0:
                                idfail, cert0 = True, (st, cert)
                    row["id_fail"] += idfail
                    ok = True
                    if idfail:
                        x, st = sss_full(Fd, cols, 3, rng, passes=10, forwards=3)
                        ok = x is not None
                        if not ok:
                            row.setdefault("fail_how", [])
                            w, how = indep.find_solution(indep.F(p, k), cols, random.Random(1))
                            rec = dict(family=name, kappa=k, p=p, a=a, M=M, cols=cols,
                                       sss_full_status=st, id_status=cert0[0], cert=cert0[1],
                                       pi_theorem=pi, indep_witness=w, indep_how=how,
                                       solvable_by_CW=M >= k * a + 1)
                            out_fail.write(json.dumps(rec) + "\n")
                            out_fail.flush()
                            row["fail_how"].append(how)
                            print("SSS_FULL FAIL", name, k, p, a, M, st, "indep:", how, flush=True)
                    row["solved"] += ok
                out_rows.write(json.dumps(row) + "\n")
                out_rows.flush()
                print("%-15s k=%d p=%d a=%d M=%d solved %d/%d idstall %d crit %d idfail %d orderfail %d/%d maxpi %d  [%.0fs]" % (
                    name, k, p, a, M, row["solved"], row["banks"], row["id_stalls"], row["crit"],
                    row["id_fail"], row["order_fail"], row["orders"], row["max_pi"], time.time() - t0), flush=True)
print("DONE %.0fs" % (time.time() - t0))

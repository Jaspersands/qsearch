"""Critical-stall banks (chain4, chainfull) per (kappa, p, a): identity-order run of one
sss_full iteration (R1-R4), stall certificate, independent witness, dense-flat check,
per-order failure rate over N random orders, and sss_full (forwards=3).
usage: chain_certs.py seed N kappa:p:a1,a2,...  ...
Writes banks/<fam>_k<k>_p<p>_a<a>.json and prints a table row per bank."""
import itertools
import json
import random
import sys
import time
from q1lib import Field, budget, one_order, theorem_forward, sss_full, rank, solve_in_span, D3, has_collinear_triple
from critical import chain4, chainfull
import indep

seed, N = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)


def dense_flats_exhaustive(Fd, cols, maxsub):
    """All flats spanned by independent subsets of size <= maxsub; return those with
    >= D3(dim)+dim columns and dim < rank (proper)."""
    p = Fd.p
    r = rank(cols, p)[0]
    seen, dense, nflats = set(), [], 0
    for kk in range(1, min(maxsub, r - 1) + 1):
        for S in itertools.combinations(range(len(cols)), kk):
            rk, bas = rank([cols[i] for i in S], p)
            if rk != kk:
                continue
            inside = frozenset(i for i in range(len(cols)) if solve_in_span(bas, cols[i], p) is not None)
            if min(inside) < S[0] or (kk, inside) in seen:
                continue
            seen.add((kk, inside))
            nflats += 1
            if len(inside) >= D3(kk) + kk:
                dense.append((kk, len(inside)))
    return dense, nflats


for s in sys.argv[3:]:
    k, p, As = s.split(":")
    k, p = int(k), int(p)
    Fd = Field(p, k)
    for a in (int(x) for x in As.split(",")):
        M = budget(a, 3)
        fams = [("chain4", chain4)] + ([("chainfull", chainfull)] if k == 3 else [])
        for fname, fam in fams:
            t0 = time.time()
            cols = fam(Fd, rng, a, M)
            tf = theorem_forward(Fd, cols, rng=rng)
            x, st, cert = one_order(Fd, cols, list(range(M)), rng, passes=20)
            fails = 0
            for t in range(N):
                perm = list(range(M))
                rng.shuffle(perm)
                y, st2, _ = one_order(Fd, cols, perm, rng, passes=10)
                fails += y is None
            xf, stf = sss_full(Fd, cols, 3, rng, passes=10, forwards=3)
            w, how = indep.find_solution(indep.F(p, k), cols, random.Random(1))
            exhaustive = a <= 6
            dense, nfl = dense_flats_exhaustive(Fd, cols, a - 1 if exhaustive else 3)
            cnt_UL = None
            if cert:
                cnt_UL = sum(1 for c in cols if solve_in_span(cert["U_L"], c, p) is not None)
            rec = dict(family=fname, kappa=k, p=p, a=a, M=M, cols=cols, theorem_forward=tf,
                       identity_status=st, identity_cert=cert, cols_in_UL=cnt_UL,
                       R3_threshold=D3(a - 1) + a - 1, collinear_triple=has_collinear_triple(Fd, cols),
                       dense_proper_flats=dense, flats_checked=nfl,
                       dense_check="exhaustive (all proper flats)" if exhaustive else "flats spanned by <=3 columns only",
                       random_order_fails=fails, random_orders=N,
                       sss_full_forwards3=("ok: " + stf) if xf is not None else ("FAIL: " + stf),
                       indep_witness=w, indep_how=how, indep_verified=indep.verify(indep.F(p, k), cols, w))
            json.dump(rec, open("banks/%s_k%d_p%d_a%d.json" % (fname, k, p, a), "w"))
            print("%-9s k=%d p=%5d a=%2d M=%2d pi=%2d id=%-36s inUL=%s/thr%d dense=%s rnd_fail=%d/%d full=%s indep=%s [%.0fs]" % (
                fname, k, p, a, M, tf.get("pi", 0), st, cnt_UL, D3(a - 1) + a - 1, dense or "none",
                fails, N, "ok" if xf is not None else "FAIL", how, time.time() - t0), flush=True)

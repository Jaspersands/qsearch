"""Simulations of the zero-sum node (float checks, plus exact end-to-end runs).

[1] Monte Carlo of the node alone: a random subspace V <= F_p^g of dimension a (random full-rank
    basis matrix E), M i.i.d. uniform labels lambda_i = E x_i, both searches of
    theorems/rees_zero_sum_node.py, the exact witness check of (F5) at d = p-1, and the
    empirical abort frequency against the exact probability and the second-moment bound.
[2] Exact end-to-end runs of the whole Rees recursion at p = c+1 with the zero-sum node at the
    top grade, using the exact simulator theorems/rees_end_to_end_ext.py (imported read-only,
    SparseExactBackend; every stage output is compared exactly with rho_{H_{d-1}}):
      heis3 (c=2, p=3) and n5 at p=5 (c=4, the filiform profile r=3 of Part C).
    Grades with kappa_d < p-1 use the Chevalley-Warning arity kappa_d g_d + 1 and the round-1
    brute-force solver (a test solver, not FCS); the zero-sum grade uses
      det : M = g(p-1)+1, exhaustive search (never aborts), and
      rand: M = explicit second-moment arity at tau = 1/8, exhaustive search, ABORT if no subset;
      tiny: M = 2 at heis3 only (bank event 2/9 per node when a = 1), to exercise the abort path.
    An aborted run outputs ABORT and is counted; it is not retried inside the run.
Run (niced, one job): /opt/anaconda3/bin/python research/audits/reviews/2026-11-04-rees-zero-sum-node/simulate_node.py [part]
"""
import json
import random
import sys
import time
from fractions import Fraction as F
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from theorems import rees_zero_sum_node as z  # noqa: E402

HERE = Path(__file__).resolve().parent


def rand_subspace_basis(p, g, a, rng):
    while True:
        E = [[rng.randrange(p) for _ in range(a)] for _ in range(g)]
        # rank check by elimination on the columns
        cols = [[E[i][j] for i in range(g)] for j in range(a)]
        rows = [c[:] for c in cols]
        r = 0
        for col in range(g):
            piv = next((i for i in range(r, a) if rows[i][col] % p), None)
            if piv is None:
                continue
            rows[r], rows[piv] = rows[piv], rows[r]
            inv = pow(rows[r][col], p - 2, p)
            rows[r] = [x * inv % p for x in rows[r]]
            for i in range(a):
                if i != r and rows[i][col]:
                    f = rows[i][col]
                    rows[i] = [(x - f * y) % p for x, y in zip(rows[i], rows[r])]
            r += 1
        if r == a:
            return E


def part1(trials=20000, seed=20261104):
    rng = random.Random(seed)
    rows = []
    for p, g, a, M in ((3, 3, 2, 4), (3, 3, 3, 6), (5, 2, 2, 5), (5, 3, 3, 6), (7, 2, 1, 3),
                       (7, 2, 2, 6), (11, 1, 1, 5), (5, 1, 1, 7), (3, 2, 2, 9)):
        aborts = 0
        mismatch = 0
        bad = 0
        for _ in range(trials):
            E = rand_subspace_basis(p, g, a, rng)
            xs = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
            lab = [tuple(sum(E[i][j] * x[j] for j in range(a)) % p for i in range(g)) for x in xs]
            s1, _ = z.exhaustive_zero_sum(lab, p)
            s2, _ = z.dp_zero_sum(lab, p)
            if (s1 is None) != (s2 is None):
                mismatch += 1
            if s1 is None:
                aborts += 1
                continue
            if not (z.is_witness(lab, s1, p, p - 1) and z.is_witness(lab, s2, p, p - 1)):
                bad += 1
        exact = z.exact_zero_sum_free_probability(p, a, M) if (p ** a <= 49 or (p ** a <= 125 and M <= 4)) else None
        bound = z.second_moment_bound(p, a, M)
        freq = aborts / trials
        se = (max(freq * (1 - freq), 1 / trials) / trials) ** 0.5
        row = dict(p=p, g=g, a=a, M=M, trials=trials, abort_freq=freq,
                   exact=float(exact) if exact is not None else None, bound=float(bound),
                   searches_agree=mismatch == 0, all_witnesses_valid=bad == 0,
                   within_4se_of_exact=(exact is None or abs(freq - float(exact)) <= 4 * se + 1e-12),
                   davenport_regime=M >= a * (p - 1) + 1)
        rows.append(row)
        print(row, flush=True)
    return rows


def part2(seeds=(20261104, 7)):
    from theorems import rees_end_to_end_ext as ext
    from theorems import rees_end_to_end_sim as base

    class ZeroSumAbort(Exception):
        pass

    def make_schedules(cover, mode):
        p = cover.p
        out = {}
        for d in range(2, cover.c + 1):
            g = cover.dims[d - 1]
            k = gcd(d, p - 1)
            if k == p - 1:
                if mode == "det":
                    M = z.davenport_arity(p, g)
                elif mode == "rand":
                    M = z.zero_sum_arity_explicit(p, g, F(1, 8))
                else:
                    M = 2
                out[d] = ext.GradeSchedule(d, k, g, "zero_sum", M, 0)
            else:
                out[d] = ext.GradeSchedule(d, k, g, "cw_bruteforce", k * g + 1, 0)
        return out

    def solver(p, sched, labels, rng, stats):
        stats.blocks += 1
        cols = [tuple(int(x) for x in lam) for lam in labels]
        assert len(cols) == sched.arity
        if sched.schedule == "zero_sum":
            s, _ = z.exhaustive_zero_sum(cols, p)
            s_dp, _ = z.dp_zero_sum(cols, p)
            assert (s is None) == (s_dp is None)
            if s is None:
                raise ZeroSumAbort
            assert z.is_witness(cols, s, p, sched.d) and z.is_witness(cols, s_dp, p, sched.d)
        else:
            s, cnt = base.brute_force_sde(cols, sched.d, p, rng)
            assert s is not None and z.is_witness(cols, s, p, sched.d)
        stats.support_sizes[sum(1 for x in s if x)] += 1
        return tuple(s)

    jobs = [("heis3", "det"), ("heis3", "rand"), ("heis3", "tiny"), ("n5_5", "det"), ("n5_5", "rand")]
    cat = ext.catalogue()
    cat["n5_5"] = (lambda: base.filiform5(5), ext.filiform5_subgroups(), "level_set", False)
    rows = []
    for key, mode in jobs:
        build, hs, smode, lazy = cat[key]
        alg = build()
        cover = base.make_cover(alg)
        schedules = make_schedules(cover, mode)
        for name, gens in hs:
            inst = ext.hidden(name, alg, gens, lazy=lazy)
            for seed in seeds:
                t0 = time.time()
                backend = ext.SparseExactBackend(cover)
                source, info = ext.prepare_source(cover, inst, backend, smode, seed)
                try:
                    recovered, rec = ext.run_rees_ext(cover, source, backend, schedules, seed=seed,
                                                      solver=solver)
                except ZeroSumAbort:
                    rows.append(dict(group=key, mode=mode, instance=name, seed=seed, aborted=True))
                    print(key, mode, name, seed, "ABORT", flush=True)
                    continue
                r = ext.grade_ext(cover, inst, recovered, rec, backend)
                keep = dict(group=key, mode=mode, instance=name, seed=seed, aborted=False,
                            p=cover.p, c=cover.c, arities={d: s.arity for d, s in schedules.items()},
                            recovered_equals_log_H=r["recovered_equals_log_H"],
                            every_stage_output_equals_rho_H_d=r["every_stage_output_equals_rho_H_d"],
                            top_source_equals_rho_H_c=r["top_source_equals_rho_H_c"],
                            readout_law_uniform_on_h_perp=r["readout_law_uniform_on_h_perp"],
                            laws_uniform={d: st["every_measured_law_uniform_on_K_perp"] for d, st in r["stages"].items()},
                            label_support={d: st["label_support_size"] for d, st in r["stages"].items()},
                            zs_support_sizes=r["stages"][cover.c]["witness_support_sizes"],
                            oracle_queries=r["oracle_queries"], seconds=round(time.time() - t0, 1))
                rows.append(keep)
                print(keep, flush=True)
    return rows


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = {}
    if which in ("1", "all"):
        res["node_monte_carlo"] = part1()
        (HERE / "simulate_node_part1.json").write_text(json.dumps(res["node_monte_carlo"], indent=1) + "\n")
    if which in ("2", "all"):
        res["end_to_end"] = part2()
        (HERE / "simulate_node_part2.json").write_text(json.dumps(res["end_to_end"], indent=1, default=str) + "\n")
    print("done")

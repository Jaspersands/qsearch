"""Proposition C checks [sampled]: steering failures are target-specific.

(a) Planted non-steerable banks of the two-relation pass (brt_tests.planted_top, fixed
    'first' split, so (ND') fails): back substitution for the planted top target versus
    for uniformly random targets in F_p^a, with the same flag.
(b) Two disjoint flags and a random split: the planted top target t is written as
    u + (t - u), u uniform; flag A realises u, flag B realises t - u.
(c) Degenerate banks (repeated columns, columns in a codim-2 subspace, nested subspaces,
    proportional pairs): forward pass status after rank reduction, and uniform-target
    success when the flag reaches the span.
backward_target(tau) returns weights whose value is exactly tau; every witness is checked.
"""
import random

from subB import F, brt, brt_tests, backward_target, forward_flag, value, check_witness


def attempt_rate(Fd, cols, rounds, basis, tau_fn, n, rng, tries=3):
    ok = 0
    for _ in range(n):
        tau = tau_fn()
        for _ in range(tries):
            x, st = backward_target(Fd, cols, rounds, basis, tau, rng)
            if x is not None:
                assert value(cols, x, Fd.p) == [t % Fd.p for t in tau]
                assert all(Fd.in_sq(v) for v in x)
                ok += 1
                break
    return ok


def part_a_b(rng):
    for (p, k, a, E) in [(1009, 2, 6, 3), (1009, 2, 8, 3), (1009, 3, 6, 3), (10007, 2, 10, 4)]:
        Fd = F(p, k)
        res = dict(inst=0, spec=0, unif=0, split=0, n=0, nsplit=0)
        for _ in range(6):
            cols = brt_tests.planted_top(Fd, a, E, rng)
            if cols is None:
                continue
            top = cols[-1]
            body = cols[:-1]
            r2 = random.Random(1)
            rounds, basis, st = forward_flag(Fd, body, E, r2, split="first")
            if st != "ok":
                continue
            res["inst"] += 1
            n = 10
            res["n"] += n
            # specific target: -y * top, y in P  (with weight y on the top column it is a solution)
            def spec():
                y = rng.choice(Fd.P)
                return [(-y * v) % p for v in top]
            res["spec"] += attempt_rate(Fd, body, rounds, basis, spec, n, rng)
            res["unif"] += attempt_rate(Fd, body, rounds, basis,
                                        lambda: [rng.randrange(p) for _ in range(a)], n, rng)
            # (b) second, independent flag on fresh random columns
            other = [[rng.randrange(p) for _ in range(a)] for _ in range(brt.arity(a, E) + 2)]
            rB, bB, stB = forward_flag(Fd, other, E, random.Random(2), split="first")
            if stB != "ok":
                continue
            res["nsplit"] += n
            allc = body + other + [top]
            for _ in range(n):
                y = rng.choice(Fd.P)
                t = [(-y * v) % p for v in top]
                done = False
                for _ in range(3):
                    u = [rng.randrange(p) for _ in range(a)]
                    xA, sA = backward_target(Fd, body, rounds, basis, u, rng)
                    if xA is None:
                        continue
                    xB, sB = backward_target(Fd, other, rB, bB, [(ti - ui) % p for ti, ui in zip(t, u)], rng)
                    if xB is None:
                        continue
                    x = xA + xB + [y]
                    assert check_witness(Fd, allc, x)
                    done = True
                    break
                res["split"] += done
        print(f"(a,b) planted p={p} kappa={k} a={a} E={E}: instances={res['inst']}, "
              f"specific-target successes {res['spec']}/{res['n']}, uniform-target {res['unif']}/{res['n']}, "
              f"two-flag split for the specific target {res['split']}/{res['nsplit']} (instances whose second random flag reached F_p^a)", flush=True)


def degenerate_banks(rng, p, a, M):
    fams = {}
    base = [[rng.randrange(p) for _ in range(a)] for _ in range(a)]
    # repeated columns from 3 vectors
    b3 = base[:3]
    fams["repeated3"] = [list(b3[rng.randrange(3)]) for _ in range(M)]
    # codim-2 subspace
    def comb(V):
        c = [rng.randrange(p) for _ in V]
        return [sum(ci * v[t] for ci, v in zip(c, V)) % p for t in range(a)]
    fams["codim2"] = [comb(base[:a - 2]) for _ in range(M)]
    # nested subspaces: half the columns in a 2-dim space, a quarter in a 4-dim space, rest generic
    fams["nested"] = [comb(base[:2]) for _ in range(M // 2)] + [comb(base[:4]) for _ in range(M // 4)]
    fams["nested"] += [[rng.randrange(p) for _ in range(a)] for _ in range(M - len(fams["nested"]))]
    rng.shuffle(fams["nested"])
    # proportional pairs: each column appears with a random multiple
    half = [[rng.randrange(p) for _ in range(a)] for _ in range(M // 2)]
    fams["proportional"] = []
    for v in half:
        c = rng.randrange(1, p)
        fams["proportional"] += [v, [(c * t) % p for t in v]]
    rng.shuffle(fams["proportional"])
    return fams


def part_c(rng):
    for (p, k, a, E) in [(1009, 2, 6, 3), (10007, 2, 8, 3), (1009, 3, 6, 3)]:
        Fd = F(p, k)
        M = brt.arity(a, E) + a
        for name, cols in degenerate_banks(rng, p, a, M).items():
            cols2, r = brt.reduce_rank(cols, p)
            rounds, basis, st = forward_flag(Fd, cols2, E, random.Random(3))
            if st != "ok":
                note = "monochromatic round found: solved directly" if st == "stop" else "flag stalls (pool columns wasted)"
                print(f"(c) p={p} kappa={k} a={a} {name}: rank {r}, forward status {st} ({note})")
                continue
            n = 20
            ok = attempt_rate(Fd, cols2, rounds, basis, lambda: [rng.randrange(p) for _ in range(r)], n, rng)
            print(f"(c) p={p} kappa={k} a={a} {name}: rank {r}, flag reaches the span; uniform-target "
                  f"successes {ok}/{n}", flush=True)


if __name__ == "__main__":
    rng = random.Random(77)
    part_a_b(rng)
    part_c(rng)

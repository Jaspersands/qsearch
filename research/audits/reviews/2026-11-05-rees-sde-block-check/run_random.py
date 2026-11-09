"""Uniform random columns through mybrt: witnesses, column counts, (H1)/(ND') rates.
Also the 'Rees label' mode: columns i.i.d. uniform on a random a-dim subspace of F_p^g, with the
public budget M_E(g) columns and the solver working on the observed span."""
import itertools
import math
import random
import sys
import time

import mybrt as mb


def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for b in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(b, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_at_least(n, k):
    p = n
    while not (is_prime(p) and (p - 1) % k == 0):
        p += 1
    return p


def run(cases, seed, reps, label_mode=False):
    rng = random.Random(seed)
    tot = dict(runs=0, ok=0, fail=0, budget=0, ndf=0, h1f=0, over=0)
    for (k, p, a, E, g) in cases:
        Fd = mb.Field(p, k)
        Mpub = mb.arity(g if label_mode else a, E)
        Ma = mb.arity(a, E)
        assert Ma == mb.closed_arity(a, E)
        st = dict(ok=0, fail=0, budget=0, ndf=0, h1f=0, used=[], passes=[])
        t0 = time.time()
        for _ in range(reps):
            if label_mode:
                B = [[rng.randrange(p) for _ in range(g)] for _ in range(a)]   # basis of V (rank a whp)
                cols = []
                for _ in range(Mpub):
                    c = [rng.randrange(p) for _ in range(a)]
                    cols.append([sum(c[i] * B[i][j] for i in range(a)) % p for j in range(g)])
            else:
                cols = [[rng.randrange(p) for _ in range(a)] for _ in range(Ma)]
            x, info = mb.solve(Fd, cols, E, rng)
            st[info["status"]] = st.get(info["status"], 0) + 1
            if info.get("nd_fails"):
                st["ndf"] += 1
            if not info.get("h1", True):
                st["h1f"] += 1
            st["used"].append(info["used"])
            if x is not None:
                assert mb.verify(Fd, cols, x)
                st["passes"].append(info["passes"])
                if info["used"] > Ma:
                    tot["over"] += 1
        tot["runs"] += reps
        for key in ("ok", "fail", "budget", "ndf", "h1f"):
            tot[key] += st[key]
        mp = max(st["passes"]) if st["passes"] else None
        print(f"kappa={k} p={p} a={a} E={E}" + (f" g={g} M_pub={Mpub}" if label_mode else "")
              + f" M_E(a)={Ma}: ok={st['ok']} fail={st['fail']} budget={st['budget']} "
              f"ND'fail={st['ndf']} H1fail={st['h1f']} used(max)={max(st['used'])} "
              f"passes(max)={mp} t={time.time() - t0:.1f}s", flush=True)
    print("# totals:", tot, flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "uniform":
        cases = []
        for a in (2, 3, 4, 5, 6, 8, 10, 12):
            cases.append((2, prime_at_least(64 * a * a, 2), a, 3, a))          # kappa=2 at the stated bound
            cases.append((3, prime_at_least(max(2750, 1000 * a * a), 3), a, 3, a))
        for (k, p, a, E) in [(2, 10007, 12, 4), (2, 10 ** 9 + 7, 20, 3), (3, 10 ** 9 + 9 if (10 ** 9 + 8) % 3 == 0 else prime_at_least(10 ** 9, 3), 20, 3),
                             (2, 10 ** 6 + 3, 16, 5), (4, prime_at_least(10 ** 7, 4), 8, 4),
                             (5, prime_at_least(10 ** 9, 5), 8, 5), (2, prime_at_least(10 ** 6, 2), 30, 5),
                             (3, prime_at_least(10 ** 7, 3), 12, 4)]:
            cases.append((k, p, a, E, a))
        run(cases, seed=int(sys.argv[2]), reps=int(sys.argv[3]))
    elif mode == "label":
        cases = []
        for (k, a, g, E) in [(2, 3, 6, 3), (2, 5, 8, 3), (3, 4, 8, 3), (2, 8, 12, 3), (3, 6, 10, 3)]:
            p = prime_at_least(64 * g * g if k == 2 else max(2750, 1000 * g * g), k)
            cases.append((k, p, a, E, g))
        run(cases, seed=int(sys.argv[2]), reps=int(sys.argv[3]), label_mode=True)

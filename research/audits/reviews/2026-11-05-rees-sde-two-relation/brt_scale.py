"""Larger random runs of brt.py (sampling branch of good_set, p > 20000) with timing,
plus the steering diagnostics (ND') and the forward-pass hypothesis (H1)."""
import random
import time

from common import F, check_witness
import brt


def main():
    rng = random.Random(4242)
    for (p, k, a, E, n) in [(1000000007, 2, 20, 3, 4), (1000000007, 2, 40, 3, 2), (1000000007, 2, 40, 6, 2),
                            (1000000009, 3, 20, 3, 4), (1000000009, 3, 40, 4, 2), (1000003, 2, 30, 8, 2)]:
        Fd = F(p, k) if p < 10 ** 7 else None
        if Fd is None:
            Fd = F.__new__(F)
            Fd.p, Fd.k, Fd.h = p, k, (p - 1) // k
            # primitive root search is slow for big p; any generator of F_p^*/P suffices
            g = 2
            while pow(g, (p - 1) // k * 1, p) == 1 or any(pow(g, (p - 1) // r, p) == 1
                                                         for r in [r for r in range(2, k + 1) if k % r == 0]):
                g += 1
            Fd.g = g
            Fd.zeta = pow(g, Fd.h, p)
            Fd.zlog = {pow(Fd.zeta, j, p): j for j in range(k)}
            Fd.Sq = None
            # sample of P (kappa-th powers) for weights
            Fd.P = [pow(rng.randrange(1, p), k, p) for _ in range(64)]
        M = brt.arity(a, E)
        for _ in range(n):
            cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
            t0 = time.time()
            rounds, basis, top, used, status = brt.forward(Fd, cols, E, rng)
            nd = brt.nd_report(Fd, cols, rounds, basis, top) if status != "budget" else None
            x, info = brt.solve(Fd, cols, E, rng)
            ok = x is not None and all(v % p == 0 or pow(v, Fd.h, p) == 1 for v in x) and any(x) and \
                all(sum(x[i] * cols[i][j] for i in range(M)) % p == 0 for j in range(a))
            print(f"p={p} kappa={k} a={a} E={E} M={M} (tri {(a+1)*(a+2)//2}): status={info['status']} "
                  f"witness_ok={ok} ND'-fails={len(nd) if nd is not None else 'n/a'} rounds={info.get('rounds')} "
                  f"time={time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()

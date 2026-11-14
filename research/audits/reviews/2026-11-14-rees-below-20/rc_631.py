#!/usr/bin/env python3
"""Second, non-SAT decision of TL6, TL7, TL9 = RC(k; Z_k -> {0}) at p = 631, xi = 3 (least primitive
root), with the complete DFS of rc_exhaust.py (beta_0 = 0 normalisation), plus a scaling
normalisation: (alpha, beta) -> (s alpha, s beta) with s in P_k preserves Def. plus-rc, so the first
nonzero beta_i may be taken in a set of representatives of F_p^* / P_k (k values).
Positive control: TL6 at 229 and TL7 at a prime where it exists (found by the same DFS)."""
import sys, time
sys.path.insert(0, __import__('os').path.dirname(__file__))
from rc_exhaust import least_prim_root, cl_table, verify


def available_scaled(p, D, xi):
    cl = cl_table(p, D, xi)
    reps = [pow(xi, i, p) for i in range(D)]  # representatives of F_p^*/P_D

    def ok(x, b, i, j):
        s = (x + b) % p
        return s == 0 or (cl[s] + i + j) % D == 0
    X0 = [[x for x in range(1, p) if cl[x] == 0]] + [[x for x in range(p) if ok(x, 0, 0, j)] for j in range(1, D)]
    nodes = [0]

    def dfs(i, X, beta, scaled):
        nodes[0] += 1
        if i == D:
            return dict(beta), [Xj[0] for Xj in X]
        cand = range(p) if scaled else ([0] + reps)
        for b in cand:
            Y = []
            for j in range(D):
                Yj = [x for x in X[j] if ok(x, b, i, j)]
                if not Yj:
                    break
                Y.append(Yj)
            else:
                beta[i] = b
                r = dfs(i + 1, Y, beta, scaled or b != 0)
                if r:
                    return r
                del beta[i]
        return None
    return dfs(1, X0, {0: 0}, False), nodes[0]


if __name__ == '__main__':
    for p, D in [(229, 6), (631, 6), (631, 7), (631, 9)] + [(q, 7) for q in (491, 547, 617, 659, 673, 701)]:
        xi = least_prim_root(p)
        t = time.time()
        r, n = available_scaled(p, D, xi)
        s = f"TL{D} at p={p} xi={xi}: " + ("AVAILABLE" if r else "NONE") + f" (DFS nodes {n}, {time.time()-t:.1f} s)"
        if r:
            verify(p, D, list(range(D)), [0], r[0], r[1], xi)
            s += f" witness verified beta={r[0]}"
        print(s, flush=True)

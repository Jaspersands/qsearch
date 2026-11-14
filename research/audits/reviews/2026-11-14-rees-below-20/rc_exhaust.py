#!/usr/bin/env python3
"""Exhaustive decision of RC(D; Delta -> Omega) availability (core Def. plus-rc), written from the
definition. Translation normalisation beta_0 = 0 (stated after Def. plus-rc). DFS over beta_i,
i in Delta \\ {0}, keeping for every column j the set of admissible alpha_j; complete.
Also: the plan counting bound |T_1 \\ 0| for the two-class type (1, eps), eps = -xi^{-m}.
usage: rc_exhaust.py   (runs the fixed list of instances below)
"""
import sys


def least_prim_root(p):
    n = p - 1
    fs = [q for q in range(2, n + 1) if n % q == 0 and all(q % r for r in range(2, int(q ** .5) + 1))]
    for g in range(2, p):
        if all(pow(g, n // q, p) != 1 for q in fs):
            return g


def cl_table(p, D, xi):
    # discrete log mod (p-1), reduced mod D
    dl = {}
    x = 1
    for e in range(p - 1):
        dl[x] = e % D
        x = x * xi % p
    return dl


def available(p, D, Delta, Omega, xi=None):
    xi = xi or least_prim_root(p)
    cl = cl_table(p, D, xi)
    Delta = sorted(Delta)
    assert Delta[0] == 0
    Om = set(Omega)
    # column constraints from i = 0 (beta_0 = 0)
    def ok(x, b, i, j):
        s = (x + b) % p
        return s == 0 or (cl[s] + i + j) % D in Om
    X0 = []
    for j in range(D):
        if j == 0:
            X0.append([x for x in range(1, p) if cl[x] == 0])  # alpha_0 + beta_0 in P_D
        else:
            X0.append([x for x in range(p) if ok(x, 0, 0, j)])
    rest = [i for i in Delta if i != 0]
    nodes = [0]
    sol = []

    def dfs(k, X, beta):
        nodes[0] += 1
        if k == len(rest):
            sol.append((dict(beta), [Xj[0] for Xj in X]))
            return True
        i = rest[k]
        for b in range(p):
            Y = []
            for j in range(D):
                Yj = [x for x in X[j] if ok(x, b, i, j)]
                if not Yj:
                    break
                Y.append(Yj)
            else:
                beta[i] = b
                if dfs(k + 1, Y, beta):
                    return True
                del beta[i]
        return False

    found = dfs(0, X0, {0: 0})
    return found, nodes[0], (sol[0] if sol else None)


def verify(p, D, Delta, Omega, beta, alpha, xi):
    cl = cl_table(p, D, xi)
    assert (alpha[0] + beta[0]) % p and cl[(alpha[0] + beta[0]) % p] == 0
    for i in Delta:
        for j in range(D):
            s = (alpha[j] + beta[i]) % p
            assert s == 0 or (cl[s] + i + j) % D in set(Omega), (i, j)
    return True


def T1_size(p, kappa, m, xi):
    h = (p - 1) // kappa
    P = {pow(x, kappa, p) for x in range(1, p)}
    eps = (-pow(pow(xi, m, p), p - 2, p)) % p
    T = set()
    for y1 in P | {0}:
        for y2 in P | {0}:
            if y1 or y2:
                T.add((y1 + eps * y2) % p)
    return len(T - {0}), len(P), 0 in T


def main():
    insts = [
        (37, 4, [0, 1, 2, 3], [0], 'TL4 at 37'),
        (37, 6, list(range(6)), [0], 'TL6 at 37'),
        (37, 9, [0, 3, 6], [0], 'TW at 37'),
        (37, 9, list(range(9)), [0], 'TL9 at 37'),
        (41, 4, [0, 1, 2, 3], [0], 'control TL4 at 41 (expect available)'),
        (229, 6, list(range(6)), [0], 'control TL6 at 229 (expect available)'),
        (43, 6, list(range(6)), [0], 'control TL6 at 43 (expect none)'),
        (397, 9, [0, 3, 6], [0], 'control TW at 397 (not in the paper list; expect available)'), (73, 9, [0, 3, 6], [0], 'control TW at 73 (listed; expect none)'),
    ]
    for p, D, Delta, Om, name in insts:
        xi = least_prim_root(p)
        found, nodes, s = available(p, D, Delta, Om, xi)
        line = f"{name}: p={p} xi={xi} step=({D},{Delta},{Om}) -> {'AVAILABLE' if found else 'NONE'} (DFS nodes {nodes})"
        if found:
            beta, alpha = s
            verify(p, D, Delta, Om, beta, alpha, xi)
            line += f" witness beta={beta} alpha={alpha} verified"
        print(line, flush=True)
    print("two-class F1 counting at (37,9): need |T_1 \\ 0| >= 36 = p-1")
    for m in range(1, 9):
        n, h, z = T1_size(37, 9, m, 2)
        print(f"  m={m}: |T_1\\0|={n} (|P|={h}, bound 2h+h^2={2*h+h*h}), 0 in T_1: {z}")


if __name__ == '__main__':
    main()

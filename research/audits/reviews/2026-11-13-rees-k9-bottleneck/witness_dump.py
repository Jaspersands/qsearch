#!/opt/anaconda3/bin/python
"""Print and independently re-check the RC(D; R -> K) witnesses used by the R8 plans (finite exact check).
Class test: cl_D(y) = c iff y^((p-1)/D) = zeta^c, zeta = g^((p-1)/D) (no discrete-log table).
Witnesses come from chain_exec.rc_witness (pure-Python DFS); conditions re-checked here cell by cell."""
import chain_exec as CE

def cls(y, p, g, D):
    z, t, w = pow(g, (p - 1) // D, p), pow(y, (p - 1) // D, p), 1
    for c in range(D):
        if w == t: return c
        w = w * z % p
    raise ValueError

STEPS = {  # p: list of (D, R, K) used
    37: [(3, (0, 1, 2), (0,)), (9, (0, 3, 6), (0, 4)), (9, tuple(range(9)), (0, 2, 5))],
    73: [(3, (0, 1, 2), (0,)), (9, (0, 3, 6), (0, 1))],
    19: [(3, (0, 1, 2), (0,)), (9, (0, 3, 6), (0, 1)), (9, tuple(range(9)), (0, 1, 4, 7)), (9, (0, 1, 4, 7), (0, 3, 8))],
    127: [(3, (0, 1, 2), (0,)), (9, (0, 3, 6), (0, 3)), (9, (0, 3), (0,))],
    181: [(3, (0, 1, 2), (0,)), (9, (0, 3, 6), (0, 1)), (9, (0, 1), (0,))],
    433: [(3, (0, 1, 2), (0,)), (9, (0, 3, 6), (0, 1)), (9, (0, 1), (0,))],
}
allok = True
for p, steps in STEPS.items():
    g = CE.prim_root(p)
    for (D, R, K) in steps:
        al, be = CE.rc_witness(p, D, R, K)
        be = dict(be)
        ok = (al[0] + be[0]) % p != 0 and cls((al[0] + be[0]) % p, p, g, D) == 0
        for i in R:
            for j in range(D):
                v = (al[j] + be[i]) % p
                if v and (cls(v, p, g, D) + i + j) % D not in K:
                    ok = False
        allok &= ok
        print(f'p={p} g={g} RC({D}; R={R} -> K={K}): alpha={list(al)} beta={be}  check={ok}')
print('ALL OK' if allok else 'FAILURE')

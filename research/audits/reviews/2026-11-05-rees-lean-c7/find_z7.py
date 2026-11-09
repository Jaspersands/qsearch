"""Find a sparse right-normed form of the degree-7 BCH part of log(exp x exp y)
in the exact model (model7.py). Design aid only."""
from fractions import Fraction as Q
from itertools import product, combinations
import numpy as np
import sympy as sp
import model7 as m

target = m.deg(m.logo(m.mul(m.expo(m.gen('x')), m.expo(m.gen('y')))), 7)
words = [tuple(w) + ('x', 'y') for w in product('xy', repeat=5)]
vecs = {w: m.deg(m.rn(w), 7) for w in words}
keys = sorted(set().union(*[set(v) for v in vecs.values()]) | set(target))

def solve(ws):
    A = sp.Matrix([[vecs[w].get(k, 0) for w in ws] for k in keys])
    b = sp.Matrix([target.get(k, 0) for k in keys])
    try:
        sol, params = A.gauss_jordan_solve(b)
    except ValueError:
        return None
    if params.shape[0]:
        return None
    return [Q(int(sp.fraction(s)[0]), int(sp.fraction(s)[1])) for s in sol]

# Batched floating-point feasibility over all supports of size k, then exact check.
Afl = np.array([[float(vecs[w].get(k, 0)) for w in words] for k in keys])
bfl = np.array([float(target.get(k, 0)) for k in keys])
rows, r = [], 0
for i in range(len(keys)):  # 18 independent coordinate rows of the Lie space
    if np.linalg.matrix_rank(Afl[rows + [i]]) > r:
        rows.append(i); r += 1
Ar, br_ = Afl[rows], bfl[rows] * 30240.0

def feasible_batch(combs):
    C = np.array(combs)
    A = Ar[:, C].transpose(1, 0, 2)                 # (N, 18, k)
    Ab = np.concatenate([A, np.broadcast_to(br_[None, :, None], (len(C), len(rows), 1))], axis=2)
    ra = np.linalg.matrix_rank(A)
    rb = np.linalg.matrix_rank(Ab)
    return [c for c, a, b in zip(combs, ra, rb) if a == C.shape[1] and b == a]

if __name__ == '__main__':
    import sys
    from itertools import islice
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    for k in range(1, kmax + 1):
        found = []
        it = combinations(range(len(words)), k)
        while True:
            chunk = list(islice(it, 200000))
            if not chunk:
                break
            for idx in feasible_batch(chunk):
                ws = [words[i] for i in idx]
                s = solve(ws)
                if s is not None and all(c != 0 for c in s):
                    found.append((max(c.denominator for c in s), ws, s))
        print('k', k, 'solutions', len(found), flush=True)
        if found:
            found.sort(key=lambda f: (f[0], [''.join(w) for w in f[1]]))
            for f in found[:12]:
                print(k, f[0], [(''.join(w), str(c)) for w, c in zip(f[1], f[2])])
            break

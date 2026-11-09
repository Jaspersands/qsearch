from fractions import Fraction as Q
from itertools import product, combinations
import sympy as sp
import model6 as m
target = m.deg(m.logo(m.mul(m.expo(m.gen('x')), m.expo(m.gen('y')))), 6)
words = [tuple(w) for w in product('xy', repeat=4)]
words = [w + ('x', 'y') for w in words]
vecs = {w: m.deg(m.rn(w), 6) for w in words}
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
for k in range(1, 6):
    found = []
    for ws in combinations(words, k):
        s = solve(ws)
        if s is not None and all(c != 0 for c in s):
            found.append((max(c.denominator for c in s), ws, s))
    if found:
        found.sort()
        for f in found[:8]:
            print(k, f[0], [(''.join(w), str(c)) for w, c in zip(f[1], f[2])])
        break

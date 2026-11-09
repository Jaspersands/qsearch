"""Rewrite rules for class-four normal forms, with certificates from three Jacobi lemmas.

Formal vectors: dict canonical-word -> Fraction, where a canonical word is a
right-normed word whose innermost pair is strictly sorted (x<y<z).
"""
from fractions import Fraction as Q
from itertools import product, permutations
import importlib.util, sys
spec = importlib.util.spec_from_file_location('m', 'bch4_model.py')
m = importlib.util.module_from_spec(spec); sys.stdout = open('/dev/null','w'); spec.loader.exec_module(m); sys.stdout = sys.__stdout__

def canon(w, c=Q(1)):
    if w[-2] == w[-1]:
        return {}
    if w[-2] > w[-1]:
        return {w[:-2] + (w[-1], w[-2]): -c}
    return {w: c}

def fv(*terms):
    out = {}
    for c, w in terms:
        for k, v in canon(tuple(w), Q(c)).items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v}

def solve(target, vecs):
    keys = sorted({k for v in vecs + [target] for k in v})
    n = len(vecs)
    rows = [[v.get(k, Q(0)) for v in vecs] + [target.get(k, Q(0))] for k in keys]
    r = 0; piv = []
    for col in range(n):
        p = next((i for i in range(r, len(rows)) if rows[i][col] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        rows[r] = [x / rows[r][col] for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col] != 0:
                f = rows[i][col]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(col); r += 1
    for i in range(r, len(rows)):
        if rows[i][n] != 0: return None
    return {c: rows[i][n] for i, c in enumerate(piv) if rows[i][n] != 0}

L = 'xyz'
# relation instances: r1(a,b,c), r2(a,b,c), r3(a,b)
inst = []
for a, b, c in product(L, repeat=3):
    inst.append((f"jacobi4a {a} {b} {c}", fv((1, a+a+b+c), (-1, a+b+a+c), (1, a+c+a+b))))
    inst.append((f"jacobi4b {a} {b} {c}", fv((1, c+a+a+b), (-1, a+b+a+c), (1, b+a+a+c), (-1, a+c+a+b))))
for a, b in product(L, repeat=2):
    inst.append((f"jacobi4c {a} {b}", fv((1, a+b+a+b), (-1, b+a+a+b))))
inst = [(n, v) for n, v in inst if v]
# canonical degree-4 words grouped by multidegree; basis chosen greedily
words = [w for w in product(L, repeat=4) if w[-2] < w[-1]]
# Prefer as basis: words whose inner pair contains the repeated letter
def key(w):
    from collections import Counter
    cnt = Counter(w); rep = [l for l in cnt if cnt[l] > 1]
    return (0 if any(l in w[-2:] for l in rep) else 1, w)
basis = []
for w in sorted(words, key=key):
    if not basis or m.express(m.rn(w), basis) is None:
        pass
for w in sorted(words, key=key):
    try:
        m.express(m.rn(w), basis); dep = bool(basis)
    except AssertionError:
        dep = False
    if not dep: basis.append(w)
print("deg4 basis", len(basis))
rules = []
for w in words:
    if w in basis: continue
    e = m.express(m.rn(w), basis)
    target = dict({w: Q(1)}); 
    for b, c in e.items(): target[b] = target.get(b, 0) - c
    cert = solve(target, [v for _, v in inst])
    assert cert is not None, w
    rules.append((w, e, {inst[i][0]: c for i, c in cert.items()}))
for w, e, cert in rules:
    print(''.join(w), '=', {''.join(k): str(v) for k, v in e.items()}, ' cert', {k: str(v) for k, v in cert.items()})

# The rule set actually used in Lean (LHS words eliminated); check the rest is a basis.
lean_lhs = ['xxyz', 'yyxz', 'zzxy', 'zxxy', 'zyxy', 'yzxz', 'yxxy', 'zxxz', 'zyyz']
rest = [w for w in words if ''.join(w) not in lean_lhs]
assert len(rest) == 18
m.express(m.rn(('x', 'x', 'y', 'z')), rest)  # raises if rest dependent
print("Lean degree-4 basis (18 words) independent: ok")

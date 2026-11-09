"""Degree-four rewrite rules compatible with the degree-three rule `jacobi3 x y z`.

Lean normal form: right-normed words, innermost pair sorted, and the suffix
[z,[x,y]] replaced by [y,[x,z]] - [x,[y,z]]. In degree four this leaves 24
words a + w (w one of the 8 reduced degree-three words). We choose 6 rules
LHS -> combination of the other 18 and a certificate from Jacobi instances.
Prints Lean source for the rules.
"""
from fractions import Fraction as Q
from itertools import product
import importlib.util, sys, io
spec = importlib.util.spec_from_file_location('m', 'bch4_model.py')
m = importlib.util.module_from_spec(spec); _o = sys.stdout; sys.stdout = io.StringIO(); spec.loader.exec_module(m); sys.stdout = _o
L = 'xyz'

def red(w, c):
    w = tuple(w)
    if w[-2] == w[-1]:
        return {}
    if w[-2] > w[-1]:
        w = w[:-2] + (w[-1], w[-2]); c = -c
    if w[-3:] == ('z', 'x', 'y'):
        out = {}
        for ww, cc in [(w[:-3] + ('y', 'x', 'z'), c), (w[:-3] + ('x', 'y', 'z'), -c)]:
            out[ww] = out.get(ww, 0) + cc
        return out
    return {w: c}

def fv(*terms):
    out = {}
    for c, w in terms:
        for k, v in red(w, Q(c)).items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v}

D3 = [w for w in product(L, repeat=3) if w[-2] < w[-1] and w != ('z', 'x', 'y')]
W4 = [(a,) + w for a in L for w in D3]
assert len(W4) == 24
inst = []
for a, b, c in product(L, repeat=3):
    inst.append((f"jacobi4a {a} {b} {c}", fv((1, a+a+b+c), (-1, a+b+a+c), (1, a+c+a+b))))
    inst.append((f"jacobi4b {a} {b} {c}", fv((1, c+a+a+b), (-1, a+b+a+c), (1, b+a+a+c), (-1, a+c+a+b))))
for a, b in product(L, repeat=2):
    inst.append((f"jacobi4c {a} {b}", fv((1, a+b+a+b), (-1, b+a+a+b))))
inst = [(n, v) for n, v in inst if v]
# sanity: every instance holds in the free algebra
for n, v in inst:
    tot = {}
    for w, c in v.items():
        tot = m.add(tot, m.sc(c, m.rn(w)))
    assert tot == {}, n

# Preferred LHS order: words whose inner pair avoids the repeated letter first.
from collections import Counter
def pref(w):
    cnt = Counter(w); rep = [l for l in cnt if cnt[l] > 1]
    return (0 if all(l not in w[-2:] for l in rep) else 1, w)
order = sorted(W4, key=pref)
# Gaussian elimination over the instance vectors, pivoting in `order`.
rows = [(dict(v), {i: Q(1)}) for i, (n, v) in enumerate(inst)]
pivots = []
for col in order:
    idx = next((k for k, (v, _) in enumerate(rows) if v.get(col, 0) != 0), None)
    if idx is None:
        continue
    v, cert = rows.pop(idx)
    f = v[col]
    v = {k: x / f for k, x in v.items()}; cert = {k: x / f for k, x in cert.items()}
    newrows = []
    for (u, cu) in rows:
        g = u.get(col, 0)
        if g:
            u = {k: u.get(k, 0) - g * v.get(k, 0) for k in set(u) | set(v)}
            u = {k: x for k, x in u.items() if x}
            cu = {k: cu.get(k, 0) - g * cert.get(k, 0) for k in set(cu) | set(cert)}
            cu = {k: x for k, x in cu.items() if x}
        newrows.append((u, cu))
    rows = newrows
    pivots.append((col, v, cert))
assert all(not v for v, _ in rows)
# back-substitute so each rule's RHS has no pivot words
for i in range(len(pivots) - 1, -1, -1):
    col, v, cert = pivots[i]
    for j in range(i):
        cj, vj, certj = pivots[j]
        g = vj.get(col, 0)
        if g:
            vj = {k: vj.get(k, 0) - g * v.get(k, 0) for k in set(vj) | set(v)}
            vj = {k: x for k, x in vj.items() if x}
            certj = {k: certj.get(k, 0) - g * cert.get(k, 0) for k in set(certj) | set(cert)}
            certj = {k: x for k, x in certj.items() if x}
            pivots[j] = (cj, vj, certj)
lhs = [p[0] for p in pivots]
basis4 = [w for w in W4 if w not in lhs]
print("rank", len(pivots), "basis4", len(basis4))
m.express(m.rn(('x','x','x','y')), basis4)  # independence check (raises if dependent)

def word(w):
    s = w[-1]
    for ch in reversed(w[:-1]):
        s = f"⁅{ch}, {s}⁆"
    return s
def num(q):
    return f"({q.numerator} : ℤ)" if q.denominator == 1 else f"(({q.numerator} : ℤ) / {q.denominator})"
for k, (col, v, cert) in enumerate(pivots):
    rhs = []
    for w in sorted(v):
        if w == col: continue
        c = -v[w]
        rhs.append((c, w))
    rhs_s = " + ".join(f"{num(c)} • {word(w)}" for c, w in rhs) or "0"
    names = [(inst[i][0], c) for i, c in sorted(cert.items())]
    print(f"-- rule {k+1}: {''.join(col)}")
    print(f"  have r{k+1} : {word(col)} = {rhs_s} := by")
    for j, (n, c) in enumerate(names):
        print(f"    have e{j} := {n.split()[0]} {' '.join(n.split()[1:])}")
    print("    simp only [N3] at " + " ".join(f"e{j}" for j in range(len(names))))
    print("    linear_combination (norm := module) " + " + ".join(f"{num(c)} • e{j}" for j, (n, c) in enumerate(names)))
print("BASIS4", [''.join(w) for w in basis4])

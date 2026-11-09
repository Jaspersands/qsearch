"""Normal form for right-normed words in x<y<z up to degree 6, mirroring the
Lean simp set of BCHClassSix.lean, and the degree-4/5 rewrite rules with
lie_skew certificates. Design aid only: Lean rechecks every rule.
"""
from fractions import Fraction as Q
from itertools import product
import model6 as m

L = 'xyz'
TOP = 6
RULES = {3: {('z', 'x', 'y'): {('y', 'x', 'z'): Q(1), ('x', 'y', 'z'): Q(-1)}}}
BASIS = {1: [(a,) for a in L], 2: [(a, b) for a in L for b in L if a < b]}

def addd(*ds):
    out = {}
    for d in ds:
        for k, v in d.items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v}

def scd(c, d):
    return {k: c * v for k, v in d.items() if c * v}

def prepend(a, w, raw_top=None):
    """[a, w] for a normal word w, reduced (top degree raw if raw_top == len)."""
    n = len(w) + 1
    if n > TOP:
        return {}
    if n == 2:
        b = w[0]
        if a == b:
            return {}
        return {(a, b): Q(1)} if a < b else {(b, a): Q(-1)}
    word = (a,) + w
    if raw_top == n:
        return {word: Q(1)}
    r = RULES.get(n, {})
    if word in r:
        return dict(r[word])
    return {word: Q(1)}

def bw(u, v, raw_top=None):
    if len(u) + len(v) > TOP:
        return {}
    if u == v:  # Lean's simp closes a syntactic [W, W] by lie_self before lie_lie
        return {}
    if len(u) == 1:
        return prepend(u[0], v, raw_top)
    a, rest = u[0], u[1:]
    # [[a, rest], v] = [a, [rest, v]] - [rest, [a, v]]
    t1 = {}
    for w, c in bw(rest, v, raw_top).items():
        t1 = addd(t1, scd(c, bw((a,), w, raw_top)))
    t2 = {}
    for w, c in bw((a,), v, raw_top).items():
        t2 = addd(t2, scd(c, bw(rest, w, raw_top)))
    return addd(t1, scd(-1, t2))

def br(U, V, raw_top=None):
    out = {}
    for u, cu in U.items():
        for v, cv in V.items():
            out = addd(out, scd(cu * cv, bw(u, v, raw_top)))
    return out

def to_assoc(d):
    return m.add(*[m.sc(c, m.rn(w)) for w, c in d.items()]) if d else {}

def rank_assoc(words):
    vecs = [to_assoc({w: Q(1)}) for w in words]
    rows = [dict(v) for v in vecs]; r = 0; piv = []
    rows2 = []
    for v in rows:
        for (k, pv) in piv:
            if v.get(k, 0):
                f = v[k] / pv[k]
                v = {kk: v.get(kk, 0) - f * pv.get(kk, 0) for kk in set(v) | set(pv)}
                v = {kk: x for kk, x in v.items() if x}
        if v:
            k = min(v); piv.append((k, v))
    return len(piv)

def word_str(w):
    s = w[-1]
    for ch in reversed(w[:-1]):
        s = f"⁅{ch}, {s}⁆"
    return s

def build_degree(n, prefer):
    """Find the degree-n rules from lie_skew instances [U,V] + [V,U] = 0."""
    Wn = [(a,) + w for a in L for w in BASIS[n - 1]]
    inst = []
    for k in range(1, n // 2 + 1):
        for U in BASIS[k]:
            for V in BASIS[n - k]:
                if k == n - k and U > V:
                    continue
                if U == V:  # lie_self U: [U, U] = 0 (integral, not half of lie_skew)
                    v = br({U: Q(1)}, {U: Q(1)}, raw_top=n)
                else:
                    v = addd(br({U: Q(1)}, {V: Q(1)}, raw_top=n), br({V: Q(1)}, {U: Q(1)}, raw_top=n))
                if v:
                    inst.append(((U, V), v))
    for nm, v in inst:
        assert to_assoc(v) == {}, nm
    order = sorted(Wn, key=prefer)
    rows = [(dict(v), {i: Q(1)}) for i, (nm, v) in enumerate(inst)]
    pivots = []
    for col in order:
        cand = [k for k, (v, _) in enumerate(rows) if v.get(col, 0) != 0]
        if not cand:
            continue
        idx = min(cand, key=lambda k: (any(c.denominator != 1 for c in scd(1 / rows[k][0][col], rows[k][1]).values()),
                                       abs(rows[k][0][col]) != 1, len(rows[k][1])))
        v, cert = rows.pop(idx)
        f = v[col]
        v = scd(1 / f, v); cert = scd(1 / f, cert)
        newrows = []
        for (u, cu) in rows:
            g = u.get(col, 0)
            if g:
                u = addd(u, scd(-g, v)); cu = addd(cu, scd(-g, cert))
            newrows.append((u, cu))
        rows = newrows
        pivots.append([col, v, cert])
    assert all(not v for v, _ in rows)
    for i in range(len(pivots) - 1, -1, -1):
        col, v, cert = pivots[i]
        for j in range(len(pivots)):
            if j == i:
                continue
            g = pivots[j][1].get(col, 0)
            if g:
                pivots[j][1] = addd(pivots[j][1], scd(-g, v))
                pivots[j][2] = addd(pivots[j][2], scd(-g, cert))
    lhs = [p[0] for p in pivots]
    basis = [w for w in Wn if w not in lhs]
    rules = {}
    for col, v, cert in pivots:
        rules[col] = {w: -c for w, c in v.items() if w != col}
        assert to_assoc(addd({col: Q(1)}, scd(-1, rules[col]))) == {}
    RULES[n] = rules
    BASIS[n] = basis
    return inst, pivots

def check_basis():
    for n in range(1, TOP + 1):
        assert rank_assoc(BASIS[n]) == len(BASIS[n]), n
    return {n: len(BASIS[n]) for n in BASIS}

def pref(w):
    from collections import Counter
    cnt = Counter(w); rep = [l for l in cnt if cnt[l] > 1]
    return (0 if all(l not in w[-2:] for l in rep) else 1, w)

BASIS[3] = [(a,) + w for a in L for w in BASIS[2] if (a,) + w != ('z', 'x', 'y')]
INST4, PIV4 = build_degree(4, pref)
INST5, PIV5 = build_degree(5, pref)
INST6, PIV6 = build_degree(6, pref)

if __name__ == '__main__':
    print(check_basis())
    INST = {4: INST4, 5: INST5, 6: INST6}
    for n, piv in ((4, PIV4), (5, PIV5), (6, PIV6)):
        for col, v, cert in piv:
            print(n, ''.join(col), len(RULES[n][col]), 'cert',
                  {(''.join(INST[n][i][0][0]), ''.join(INST[n][i][0][1])): str(c) for i, c in cert.items()})

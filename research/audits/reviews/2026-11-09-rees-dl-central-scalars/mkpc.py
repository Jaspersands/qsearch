"""Pc presentation of the Lazard group exp(L_DL) over F_p (class 3 < p), as GAP code.
Usage: mkpc.py p  -> prints GAP code defining G."""
import sys
from fractions import Fraction
p = int(sys.argv[1]); n = 8
br = [(1,2,5,1),(1,3,6,1),(1,4,7,1),(1,5,8,-1),(2,3,8,1),(2,4,6,1),(2,6,7,-1),(3,4,5,-1),(3,5,7,-1),(4,6,8,-1)]
C = {}
for i,j,k,c in br:
    C[(i-1,j-1)] = [(k-1, c % p)]; C[(j-1,i-1)] = [(k-1, (-c) % p)]
def lie(x, y):
    z = [0]*n
    for i in range(n):
        if x[i] == 0: continue
        for j in range(n):
            if y[j] == 0: continue
            for k, c in C.get((i,j), []):
                z[k] = (z[k] + x[i]*y[j]*c) % p
    return z
inv = lambda a: pow(a % p, p-2, p)
h, t = inv(2), inv(12)
def add(*vs): return [sum(v[i] for v in vs) % p for i in range(n)]
def sc(a, v): return [(a*x) % p for x in v]
def bch(x, y):
    xy = lie(x, y)
    return add(x, y, sc(h, xy), sc(t, lie(x, xy)), sc((-t) % p, lie(y, xy)))
def e(i, a=1):
    v = [0]*n; v[i] = a % p; return v
def normal_word(x):
    a = []
    y = list(x)
    for i in range(n):
        ai = y[i] % p; a.append(ai)
        y = bch(e(i, -ai), y)
        assert all(y[j] == 0 for j in range(i+1))
    return a
# Jacobi check
import itertools
for i,j,k in itertools.combinations(range(n),3):
    a,b,c = e(i),e(j),e(k)
    s = add(lie(a,lie(b,c)), lie(b,lie(c,a)), lie(c,lie(a,b)))
    assert all(v == 0 for v in s), (i,j,k)
out = [f"F := FreeGroup({n});; rws := SingleCollector(F, List([1..{n}], i -> {p}));;"]
for i in range(n):
    for j in range(i+1, n):
        # g_j^{g_i} = g_i^{-1} g_j g_i
        w = normal_word(bch(bch(e(i,-1), e(j)), e(i)))
        word = "*".join(f"F.{k+1}^{w[k]}" for k in range(n) if w[k]) or "One(F)"
        if w != [1 if k == j else 0 for k in range(n)]:
            out.append(f"SetConjugate(rws, {j+1}, {i+1}, {word});;")
out.append("G := GroupByRwsNC(rws);;")
print("\n".join(out))

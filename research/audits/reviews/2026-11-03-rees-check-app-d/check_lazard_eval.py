"""Lemma tb-evaluation / Lemma tb-words, checked on UT_{c+1}(Z/p^e) (class c).

Uses theorems/universal_lazard_words.py read-only. For each (p,c,e) with c<p,
random x,y: Pi_+ and Pi_[] evaluated with modulus M=p^e must equal
exp(log x + log y) and exp([log x, log y]) computed by matrix series mod p^e.
Negative control: modulus p (too small) when e>=2 must fail somewhere.
Edge: c = p-1 (largest allowed class) and c >= p rejected by the evaluator.
"""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from theorems.universal_lazard_words import UniversalLazardWords

random.seed(7)

def mat_mul(A, B, M):
    n = len(A)
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(n)) % M for j in range(n)) for i in range(n))

def ident(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))

def mat_add(A, B, M, s=1):
    return tuple(tuple((a + s*b) % M for a, b in zip(r1, r2)) for r1, r2 in zip(A, B))

def mat_scale(A, r, M):
    return tuple(tuple(r*a % M for a in row) for row in A)

def log_ut(X, c, M):
    n = len(X); N = mat_add(X, ident(n), M, -1)
    out = tuple(tuple(0 for _ in range(n)) for _ in range(n)); P = ident(n)
    for k in range(1, c+1):
        P = mat_mul(P, N, M)
        out = mat_add(out, mat_scale(P, (-1)**(k+1) * pow(k, -1, M), M), M)
    return out

def exp_ut(A, c, M):
    n = len(A); out = ident(n); P = ident(n); f = 1
    for k in range(1, c+1):
        P = mat_mul(P, A, M); f *= k
        out = mat_add(out, mat_scale(P, pow(f, -1, M), M), M)
    return out

def rand_ut(n, M):
    return tuple(tuple(1 if i == j else (random.randrange(M) if j > i else 0) for j in range(n)) for i in range(n))

def run(p, c, e, trials=4, modulus=None):
    M = p**e; n = c + 1
    W = UniversalLazardWords(p, c, ident(n), lambda a, b: mat_mul(a, b, M), modulus=modulus or M)
    ok = True
    for _ in range(trials):
        x, y = rand_ut(n, M), rand_ut(n, M)
        lx, ly = log_ut(x, c, M), log_ut(y, c, M)
        assert exp_ut(lx, c, M) == x
        want_add = exp_ut(mat_add(lx, ly, M), c, M)
        br = mat_add(mat_mul(lx, ly, M), mat_mul(ly, lx, M), M, -1)
        want_br = exp_ut(br, c, M)
        ok &= W.lie_add(x, y) == want_add and W.lie_bracket(x, y) == want_br
    return ok, W.operation_caps()

cases = [(3, 2, 2), (3, 2, 3), (5, 3, 2), (5, 4, 2), (5, 4, 3), (7, 3, 3), (7, 5, 2), (7, 6, 2)]
for p, c, e in cases:
    ok, caps = run(p, c, e)
    print(f"p={p} c={c} e={e}: modulus p^e correct={ok}  caps={caps}")
    assert ok
for p, c, e in [(5, 3, 2), (7, 5, 2), (5, 4, 2)]:
    bad, _ = run(p, c, e, trials=6, modulus=p)
    print(f"negative control p={p} c={c} e={e} with modulus p: all correct={bad} (expect False)")
for p, c in [(3, 3), (5, 5), (2, 2)]:
    try:
        UniversalLazardWords(p, c, ident(c+1), lambda a, b: a)
        print("p<=c accepted?!", p, c)
    except ValueError as err:
        print(f"p={p} c={c} rejected: {err}")

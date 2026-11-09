# F_p semidirect F_p^m with p <= m but class < p: does the matrix log in UT_{m+1} still give the Lazard ring?
import itertools, numpy as np
p, m = 3, 4
n = m + 1
A = np.eye(m, dtype=int); A[0,1] = 1; A[2,3] = 1   # N^2 = 0, class 2 < p = 3, but m = 4 > p
def emb(a, v):
    M = np.eye(n, dtype=int)
    M[:m,:m] = np.linalg.matrix_power(A, a) % p
    M[:m, m] = v
    return M % p
inv = lambda k: pow(k, -1, p)
G = [emb(a, np.array(v)) for a in range(p) for v in itertools.product(range(p), repeat=m)]
I = np.eye(n, dtype=int)
def log(g):
    M = (g - I) % p
    return (M - inv(2) * (M @ M)) % p           # truncated at degree 2 (< p)
def exp(X):
    return (I + X + inv(2) * (X @ X)) % p
def br(X, Y): return (X @ Y - Y @ X) % p
# check: every product of 3 elements (g-I) vanishes on generators' associative algebra
gens = [emb(1, np.zeros(m, dtype=int)), emb(0, np.array([0,1,0,1]))]
Ms = [(g - I) % p for g in G]
nil3 = all(not ((x @ y @ z) % p).any() for x in Ms[:40] for y in Ms[:40] for z in Ms[:40])
ok_inv = all((exp(log(g)) == g).all() for g in G)
ok_bch = True
for g in G[::7]:
    for h in G[::5]:
        X, Y = log(g), log(h)
        Z = (X + Y + inv(2) * br(X, Y)) % p
        if not ((exp(Z) - (g @ h) % p) % p == 0).all(): ok_bch = False
expo = all((np.linalg.matrix_power(g, p) % p == I).all() for g in G)
print("order", len(G), "exp p:", expo, "deg-3 products vanish (sample):", nil3, "exp.log=id:", ok_inv, "BCH_2 ok:", ok_bch)

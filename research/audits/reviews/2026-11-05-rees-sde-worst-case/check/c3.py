import itertools, numpy as np
p, k = 7, 3
P = sorted({pow(y, k, p) for y in range(1, p)})
W = [0] + P
reps, seen = [], set()
for x in range(p):
    for y in range(p):
        if (x, y) == (0, 0) or (x, y) in seen: continue
        reps.append((x, y)); seen |= {((w*x) % p, (w*y) % p) for w in P}
def unsolvable_count(n_extra):
    X = np.array([v for v in itertools.product(W, repeat=2 + n_extra) if any(v)])  # weights
    cnt = 0; ex = None
    for extra in itertools.combinations_with_replacement(reps, n_extra):
        cols = np.array([(1, 0), (0, 1)] + list(extra))
        s = (X @ cols) % p
        if not np.any((s == 0).all(axis=1)):
            cnt += 1; ex = extra
    return cnt, ex
for n in (3, 4):
    print("a=2, M=%d: unsolvable banks (with e1,e2):" % (n + 2), unsolvable_count(n))

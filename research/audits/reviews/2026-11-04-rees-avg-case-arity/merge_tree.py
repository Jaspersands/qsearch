"""Merge trees ("merge columns by isotropic vectors") for i.i.d. uniform columns.

Level j kills coordinate j: a node takes m children z_1..z_m (first j-1 coordinates
already 0), finds y in D^m \\ 0 with sum y_l z_l[j] = 0, and outputs sum y_l z_l.
Raw column weight = product of the y's on its root path (in D since D is closed
under products).  The root is the zero vector with a nonzero weight vector.

  triple : fan-in 3, deterministic success.  For kappa = 2 the ternary diagonal form
           c1 x1 + c2 x2 + c3 x3 (x_i squares) is isotropic; for kappa = 3 the
           diagonal cubic curve has a point (Hasse).  Found by sampling x1, x2 in
           P_kappa and testing x3 = -(c1 x1 + c2 x2)/c3 in D (expected O(kappa) tries).
           Raw columns: 3^a exactly.
  pair   : adaptive fan-in 2 from a pool.  z with z[j] = 0 passes up alone (y = 1);
           z, w pair when -z[j]/w[j] in P_kappa (coset condition).  Greedy matching.
           Reports the smallest pool N (doubling then bisection) with success >= 1/2.

Usage: python merge_tree.py triple p kappa a reps
       python merge_tree.py pair   p kappa a reps
"""
import random
import sys
from common import Field, check_witness, rand_cols


def triple_tree(Fd, cols, rng):
    p, a = Fd.p, len(cols[0])
    # nodes: (vector, list of (raw index, weight))
    level = [(c, [(i, 1)]) for i, c in enumerate(cols)]
    tries = 0
    for j in range(a):
        nxt = []
        for t in range(0, len(level) - 2, 3):
            trio = level[t:t + 3]
            c = [z[0][j] % p for z in trio]
            y = None
            for i in range(3):
                if c[i] == 0:
                    y = [1 if l == i else 0 for l in range(3)]
                    break
            while y is None:
                tries += 1
                x1, x2 = Fd.rand_P(rng), Fd.rand_P(rng)
                x3 = (-(c[0] * x1 + c[1] * x2) * pow(c[2], -1, p)) % p
                if Fd.inD(x3):
                    y = [x1, x2, x3]
            vec = [sum(y[l] * trio[l][0][i] for l in range(3)) % p for i in range(a)]
            assert vec[j] == 0
            wts = [(idx, w * y[l] % p) for l in range(3) for (idx, w) in trio[l][1] if y[l]]
            nxt.append((vec, wts))
        level = nxt
    root = level[0]
    assert all(v == 0 for v in root[0])
    x = [0] * len(cols)
    for idx, w in root[1]:
        x[idx] = w
    return x, tries


def pair_tree(Fd, cols, rng):
    """Returns a witness or None."""
    p, a, k = Fd.p, len(cols[0]), Fd.k
    cm1 = Fd.coset(p - 1)
    level = [(c, [(i, 1)]) for i, c in enumerate(cols)]
    for j in range(a):
        nxt, classes = [], {}
        for z in level:
            if z[0][j] % p == 0:
                nxt.append(z)
            else:
                classes.setdefault(Fd.coset(z[0][j]), []).append(z)
        # z, w pair iff coset(z_j) - coset(w_j) = coset(-1)  (then y = (1, -z_j/w_j))
        used = set()
        for m in range(k):
            m2 = (m - cm1) % k
            A, B = classes.get(m, []), classes.get(m2, [])
            if m == m2:
                for t in range(0, len(A) - 1, 2):
                    nxt.append(merge2(Fd, A[t], A[t + 1], j))
                used.add(m)
            elif m not in used and m2 not in used:
                for t in range(min(len(A), len(B))):
                    nxt.append(merge2(Fd, A[t], B[t], j))
                used.update((m, m2))
        level = nxt
        if not level:
            return None
    # every survivor is the zero vector; take the first
    x = [0] * len(cols)
    for idx, w in level[0][1]:
        x[idx] = w
    return x


def merge2(Fd, z, w, j):
    p = Fd.p
    y2 = (-z[0][j] * pow(w[0][j], -1, p)) % p
    assert Fd.inD(y2)
    vec = [(z[0][i] + y2 * w[0][i]) % p for i in range(len(z[0]))]
    wts = list(z[1]) + [(idx, ww * y2 % p) for idx, ww in w[1]]
    return vec, wts


def main():
    mode, p, k, a, reps = sys.argv[1], *map(int, sys.argv[2:6])
    Fd = Field(p, k)
    rng = random.Random(20261104 + a)
    if mode == "triple":
        tot = 0
        for r in range(reps):
            cols = rand_cols(rng, p, a, 3 ** a)
            x, tries = triple_tree(Fd, cols, rng)
            assert check_witness(Fd, cols, x)
            tot += tries
        nodes = (3 ** a - 1) // 2
        print(f"triple p={p} kappa={k} a={a}: columns 3^a={3**a}, {reps}/{reps} exact witnesses, "
              f"mean isotropic tries per node {tot/reps/nodes:.3f}")
    else:
        def rate(N):
            ok = 0
            for r in range(reps):
                cols = rand_cols(rng, p, a, N)
                x = pair_tree(Fd, cols, rng)
                if x is not None:
                    assert check_witness(Fd, cols, x)
                    ok += 1
            return ok / reps
        N = 2
        while rate(N) < 0.5:
            N *= 2
        lo, hi = N // 2, N
        while hi - lo > max(1, hi // 64):
            mid = (lo + hi) // 2
            if rate(mid) >= 0.5:
                hi = mid
            else:
                lo = mid
        print(f"pair p={p} kappa={k} a={a}: smallest pool with success>=1/2 ~ {hi} "
              f"(2^a = {2**a}, ratio {hi/2**a:.3f}); witnesses checked exactly")


if __name__ == "__main__":
    main()

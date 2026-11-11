"""Largest dead banks (no nonzero P0-solution) in F_p^1 and F_p^2, exhaustive.

Columns are taken up to P-scaling (which bijects solution sets), i.e. as pairs
(projective point, coset class). In F_p^2 every dead bank spanning the plane is
mapped by GL_2 to one containing e1 and e2, so we search over dead extensions of
{e1, e2} by depth-first search over increasing class index (every subset of a dead
bank is dead, so pruning is exact). A bank lying on one line is a 1-dim bank.
Output: max dead size m1 (in F_p^1) and m2 (in F_p^2, spanning), and the number of
maximum dead extensions found. N(kappa, d, p) = (max dead size) + 1.
Run: nice -n 19 /opt/anaconda3/bin/python -I dead_w2.py
"""
import sys
import time

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from sdecore import coset_table, is_dead  # noqa: E402


def classes2(p, g, kap):
    reps = [(1, t) for t in range(p)] + [(0, 1)]
    out = []
    for (u, v) in reps:
        for e in range(kap):
            s = pow(g, e, p)
            out.append([u * s % p, v * s % p])
    return out


def max_dead_1(p, g, kap, cos):
    cl = [[pow(g, e, p)] for e in range(kap)]
    best = 0
    # multiset of classes: columns g^e (repetition allowed); search multisets by size
    def rec(start, cur):
        nonlocal best
        best = max(best, len(cur))
        if len(cur) >= 3 * kap:
            return
        for i in range(start, kap):
            nxt = cur + [cl[i]]
            if is_dead(nxt, p, cos):
                rec(i, nxt)
    rec(0, [])
    return best


def max_dead_2(p, g, kap, cos, cap=None):
    cl = classes2(p, g, kap)
    base = [[1, 0], [0, 1]]
    cand = [i for i, c in enumerate(cl) if is_dead(base + [c], p, cos)]
    best, nbest = 2, 0
    stack = [([], 0)]

    def rec(chosen, start):
        nonlocal best, nbest
        size = 2 + len(chosen)
        if size > best:
            best, nbest = size, 1
        elif size == best:
            nbest += 1
        if cap is not None and size >= cap:
            return
        for j in range(start, len(cand)):
            i = cand[j]
            cols = base + [cl[k] for k in chosen] + [cl[i]]
            if is_dead(cols, p, cos):
                rec(chosen + [i], j)  # repetition allowed (same class twice)
    rec([], 0)
    return best, nbest, len(cand)


def main():
    print("kappa p (-1 in P) m1 m2 #max_ext #cand_3 seconds")
    for kap, plist in [(3, [7, 13, 19, 31, 37, 43, 61, 67]), (4, [13, 17, 29, 37, 41, 53]),
                       (5, [11, 31, 41, 61]), (6, [13, 19, 31, 37, 43])]:
        for p in plist:
            t0 = time.time()
            g, cos = coset_table(p, kap)
            minus1 = cos[p - 1] == 0
            m1 = max_dead_1(p, g, kap, cos)
            m2, nb, nc = max_dead_2(p, g, kap, cos)
            print(kap, p, bool(minus1), m1, m2, nb, nc, f"{time.time() - t0:.1f}", flush=True)


if __name__ == "__main__":
    main()

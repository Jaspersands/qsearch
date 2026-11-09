"""Cross-check wnest.py (the note's implementation, mode 'wnest') against strict_wnest.py
(variant 'proof': WNEST at q >= 4, KOW pool q+1; after the 9 Nov fix wnest.py matches it).  Same instances; compare the
columns pulled and the per-piece (q, |X|) sequence.  Any divergence is a code/proof discrepancy
to report.  Also runs wnest.py's own asserts on the climbed worst pools saved by attack_climb.py
(as one-stage instances: the pool followed by random filler).
"""
import sys, glob, math
import numpy as np
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-08-rees-sde-p3-nest")
import wnest
from strict_wnest import StrictRun, Fail, closed_form, guarantee

def both(n, vecs):
    R1 = wnest.Run(n, wnest.stream_from_list(vecs), "wnest")
    sol1 = R1.run()
    R2 = StrictRun(n, vecs, "proof", brute_var=False)
    try:
        sol2 = R2.run()
    except Fail as e:
        sol2 = None
    seq1 = [(c[0], c[2]) for c in R1.costs]
    seq2 = [(c[0], c[2]) for c in R2.costs]
    return (len(R1.stream) if sol1 is not None else None, seq1, R2.m_needed if sol2 is not None else None, seq2,
            sorted(sol1) if sol1 is not None else None, sorted(sol2) if sol2 is not None else None)

if __name__ == "__main__":
    rng = np.random.default_rng(99)
    diverge = 0; cnt = 0
    for n in (4, 5, 6, 7, 8, 9, 11, 13, 15, 17, 21, 25, 31, 41, 61):
        for rep in range(4):
            m = math.ceil(closed_form(n))
            kind = rep % 4
            if kind == 0: vecs = [rng.integers(0, 3, n) for _ in range(m)]
            elif kind == 1:
                vecs = []
                while len(vecs) < m:
                    v = rng.integers(0, 3, n); vecs += [v, v.copy()]
                vecs = vecs[:m]
            elif kind == 2:
                vecs = []
                while len(vecs) < m:
                    v = np.zeros(n, dtype=np.int64); v[rng.choice(n, min(2, n), replace=False)] = rng.integers(1, 3, min(2, n)); vecs.append(v)
            else:
                vecs = []
                while len(vecs) < m:
                    a = rng.integers(0, 3, n); b = rng.integers(0, 3, n); vecs += [a, b, (-(a + b)) % 3]
                vecs = vecs[:m]
            m1, s1, m2, s2, w1, w2 = both(n, vecs)
            cnt += 1
            same = (m1 == m2 and s1 == s2 and w1 == w2)
            if not same:
                diverge += 1
                print("DIVERGENCE n=%d kind=%d: wnest m_used=%s strict m_needed=%s\n  wnest %s\n  strict %s\n  witnesses equal: %s" % (n, kind, m1, m2, s1, s2, w1 == w2))
            else:
                print(f"n={n:3d} kind={kind}: identical (m={m1}, {len(s1)} pieces, |witness|={len(w1)}); wnest.guarantee={wnest.guarantee(n)} strict guarantee(proof)={guarantee(n,'proof')}")
    print(f"\n{cnt} instances compared, {diverge} divergences")
    # climbed pools through wnest.py's asserts
    files = sorted(glob.glob("best_pool_q*_wt_*.npy"))
    bad = 0
    for f in files:
        M = np.load(f)                       # q x N
        q, N = M.shape
        vecs = [M[:, j] for j in range(N)] + [rng.integers(0, 3, q) for _ in range(math.ceil(closed_form(q)))]
        R = wnest.Run(q, wnest.stream_from_list(vecs), "wnest")
        try:
            sol = R.run()
            first = R.costs[0]
        except AssertionError as e:
            bad += 1; print("wnest.py ASSERT on", f, e); continue
        print(f"{f}: wnest.py first piece (q, d, |X|, N, N*, r*, wt, mu, sigma) = {first}")
    print(f"{len(files)} climbed pools run through wnest.py, {bad} asserts")

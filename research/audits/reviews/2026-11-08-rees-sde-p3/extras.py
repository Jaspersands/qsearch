import itertools, numpy as np
from kow_p3 import solve, verify, nullspace3
vecs2 = [np.array(v) for v in itertools.product(range(3), repeat=2)]
shown = 0
for combo in itertools.combinations_with_replacement(range(9), 5):
    inst = [vecs2[i] for i in combo]
    if solve(inst) is None:
        # existence check by brute force
        sols = [S for r in range(1, 6) for S in itertools.combinations(range(5), r) if not (sum(inst[i] for i in S) % 3).any()]
        print("n=2, m=5 failure instance:", [tuple(int(x) for x in v) for v in inst], "| zero-sum subsets exist:", len(sols) > 0, "e.g.", sols[:2])
        shown += 1
        if shown == 2: break
# pattern counts of q+2 random columns
rng = np.random.default_rng(11)
for q in (10, 30, 60):
    cnts = []
    for _ in range(20):
        while True:
            cols = [rng.integers(0, 3, q) for _ in range(q + 2)]
            B = nullspace3(np.array(cols).T % 3)
            if len(B) == 2: break
        pats = set(zip(B[0].tolist(), B[1].tolist())) - {(0, 0)}
        cnts.append(len(pats))
    print(f"q={q}: distinct nonzero joint patterns of a 2-dim dependency space on q+2 random columns: min {min(cnts)}, max {max(cnts)} (of 8) over 20 instances")

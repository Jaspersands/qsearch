"""Independent small-case check of the KOW sparse-dependency algorithm at p = 3.
Intrinsic formulation (no coordinates for the quotient): state = realized subgroup U of F_3^n and
the ordered list of unused vectors.  Round at codimension l: if some unused v lies in U, or l = 0,
success.  Else take the first min(m, l + r) unused vectors (r = ceil(log_3(l+1))), find ALL sparsest
nonzero delta with sum delta_i v_i in U ('dependency mod U'); for each such choice (nondeterministic
branch) A = {delta=1}, B = {delta=2}, u = sum_A v; if A or B is empty or u in U: success; else
U <- U + <u>, remove A u B (the rest keeps its order) and recurse.
We report, for n = 2 and every ordered sequence / every multiset, whether SOME branch fails and
whether ALL branches fail.  'sorted' = the multiset in the order of itertools.product(range(3),
repeat=2) indices, which is the order used by the author's calib.py."""
import itertools, math
from functools import lru_cache

def run_n(n):
    V = list(itertools.product(range(3), repeat=n))
    addv = lambda a, b, c=1: tuple((x + c * y) % 3 for x, y in zip(a, b))
    zero = (0,) * n
    def span_add(U, u):
        return frozenset(addv(x, u, c) for x in U for c in range(3))
    def r_of(l): return max(1, math.ceil(math.log(l + 1, 3) - 1e-12))
    @lru_cache(maxsize=None)
    def outcome(U, seq):
        """returns (some_branch_succeeds, some_branch_fails)."""
        dimU = round(math.log(len(U), 3)); l = n - dimU
        if l == 0 and seq: return (True, False)
        if any(V[i] in U for i in seq): return (True, False)
        if not seq: return (False, True)
        take = min(len(seq), l + r_of(l)); F = seq[:take]
        deps = []
        for d in itertools.product(range(3), repeat=take):
            if not any(d): continue
            s = zero
            for c, i in zip(d, F):
                if c: s = addv(s, V[i], c)
            if s in U: deps.append(d)
        if not deps: return (False, True)
        w = min(sum(1 for c in d if c) for d in deps)
        succ = False; fail = False
        for d in deps:
            if sum(1 for c in d if c) != w: continue
            A = [j for j, c in enumerate(d) if c == 1]; B = [j for j, c in enumerate(d) if c == 2]
            u = zero
            for j in A: u = addv(u, V[F[j]])
            if not A or not B or u in U: succ = True; continue
            rest = tuple(F[j] for j in range(take) if d[j] == 0) + seq[take:]
            s2, f2 = outcome(span_add(U, u), rest)
            succ |= s2; fail |= f2
        return (succ, fail)
    return V, outcome, frozenset([zero])

def has_zero_sum(vecs):
    n = len(vecs[0])
    for r in range(1, len(vecs) + 1):
        for S in itertools.combinations(range(len(vecs)), r):
            if all(sum(vecs[i][k] for i in S) % 3 == 0 for k in range(n)): return True
    return False

V, outcome, U0 = run_n(2)
for m in (5, 6):
    seq_some = seq_all = 0
    for seq in itertools.product(range(9), repeat=m):
        s, f = outcome(U0, seq)
        seq_some += f; seq_all += (f and not s)
    ms_sorted_some = ms_sorted_all = ms_every_order_all = ms_some_order_some = 0; nms = 0; zs = 0
    for ms in itertools.combinations_with_replacement(range(9), m):
        nms += 1; zs += has_zero_sum([V[i] for i in ms])
        s, f = outcome(U0, ms)
        ms_sorted_some += f; ms_sorted_all += (f and not s)
        perms = set(itertools.permutations(ms))
        res = [outcome(U0, p) for p in perms]
        ms_every_order_all += all(f and not s for s, f in res)
        ms_some_order_some += any(f for s, f in res)
    print(f"n=2 m={m}: ordered sequences {9**m}: some-branch-fails {seq_some}, all-branches-fail {seq_all}")
    print(f"   multisets {nms} (with a zero-sum subset: {zs}); sorted order: some-branch-fails {ms_sorted_some}, "
          f"all-branches-fail {ms_sorted_all}; fail for every order and branch {ms_every_order_all}; "
          f"fail for some order/branch {ms_some_order_some}")
ex = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 2)]
print("author's example", ex, "sorted-order outcome (some succ, some fail):", outcome(U0, tuple(V.index(v) for v in ex)))

# author's reported failure instances at n = 3 (m = 8) and n = 4 (m = 12)
for inst in ([(2, 0, 2), (2, 1, 0), (0, 2, 1), (2, 2, 2), (1, 2, 1), (2, 0, 0), (0, 1, 2), (2, 1, 2)],
             [(1, 2, 2, 1), (2, 1, 0, 1), (1, 1, 1, 1), (1, 2, 0, 0), (1, 0, 1, 2), (0, 2, 0, 0), (2, 2, 0, 1),
              (1, 2, 1, 1), (1, 0, 1, 1), (1, 0, 0, 2), (2, 2, 1, 1), (0, 1, 2, 2)]):
    n = len(inst[0]); Vn, outn, U0n = run_n(n)
    s, f = outn(U0n, tuple(Vn.index(v) for v in inst))
    print(f"n={n} m={len(inst)} author's failure instance: some branch succeeds {s}, some branch fails {f}; "
          f"zero-sum subset exists {has_zero_sum(inst)}")

# recursion m_l = max(l + r, m_{l-1} + floor((l+r) 2 3^{r-1} / (3^r - 1))), m_0 = 1
m = {0: 1}
for l in range(1, 9):
    r = max(1, math.ceil(math.log(l + 1, 3) - 1e-12))
    m[l] = max(l + r, m[l - 1] + (l + r) * 2 * 3 ** (r - 1) // (3 ** r - 1))
print("recursion m_1..m_8:", [m[l] for l in range(1, 9)])

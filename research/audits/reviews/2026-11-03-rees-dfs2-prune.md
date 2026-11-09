# dfs2b: pruned exact DFS for the Schedule 2 two-level contraction (kappa 8, 9 LIMIT primes)

2026-11-04 (started 11-03). AI-only session, not human review. Labels: **[exact]** =
complete finite computation with the named program and output file;
**[proved]** = written argument here or in the program header; **[argued]** =
heuristic. Directory of programs and outputs:
`research/audits/reviews/2026-11-02-rees-schedules/small-prime/` (below "SP").
Interpreter for the Python check: `/opt/anaconda3/bin/python`.

## 0. Problem (unchanged from dfs2)

`dfs2b.c` (SP) decides exactly the problem of `dfs2.c`: for a prime p = 1 (mod
kappa), with A_m = Q_m U {0} the coset of kappa-th powers shifted by g^m plus
zero, do alpha, beta in F_p^kappa exist with alpha_0 = 1, beta_0 = 0 and
alpha_j + beta_i in A_{-(i+j)} for all i, j in Z_kappa? The general form of the
notes (alpha_0 + beta_0 != 0, `2026-11-02-rees-threshold-2.md` §0) normalises
to this by translating beta_0 to 0 and scaling by (alpha_0 + beta_0)^{-1} in
Q_0. E_2(kappa) is the set of primes where no such pair exists. dfs2 answers
FEASIBLE (witness re-checked), INFEASIBLE (complete search) or LIMIT (node
budget). dfs2b has the same three answers and the same output lines (plus
`secs=`), re-checks every FEASIBLE witness on all kappa^2 cells against the
original definition, and has a `plain` flag that reproduces dfs2's search tree
node for node (used as the independent cross-check mode).

## 1. The prunes and why they are sound [proved]

Write M_{ij} = alpha_j + beta_i (the "sum matrix", indices in Z_kappa) and
c_i = M_{i0} = 1 + beta_i (column 0, c_0 = 1). The DFS assigns rows beta_i and
keeps, per column j >= 1, the set S_j of alpha_j values consistent with all
assigned rows. A leaf (all rows assigned, all S_j nonempty) is a solution.

**Prune 1: row viability, forward checking, most-constrained row first.**
A value b for an unassigned row r is viable iff 1 + b in A_{-r} and, for every
column j, S_j meets A_{-(r+j)} - b. These are exactly the tests dfs2 makes
before descending, and every completion of the current partial assignment
satisfies them; so a row with no viable value proves the node dead, and
restricting a branch to viable values loses nothing. The constraints are
symmetric across rows, so rows may be assigned in any order and the search
stays exhaustive; dfs2b branches on the row with the fewest viable values
(row 1 is forced first, see Prune 2). The viable set is computed either as the
bitset intersection of the difference sets A_m - S_j = U_{x in S_j}(A_m - x)
(cost |S_j| x W words, W = ceil(p/64)) or, once the running intersection is
small, by direct coset-table look-ups; both compute the same set. This is the
source of the speed: deep in the tree |S_j| is 1-12, where dfs2 paid
(p/kappa) x kappa x W word operations per node.

**Prune 2: a canonical corner (symmetry breaking).** Let M be a normalised
solution. (i) For every cell (s,t) with M_{st} != 0, the recentred matrix
M'_{ij} = M_{i+s,j+t} / M_{st} is a normalised solution: it is a sum matrix
(alpha'_j = (alpha_{j+t} + beta_s)/M_{st}, beta'_i = (beta_{i+s} - beta_s)/M_{st}),
M'_{00} = 1, and M'_{ij} in M_{st}^{-1} A_{-(i+s+j+t)} = A_{-(i+j)} because
M_{st} in Q_{-(s+t)} and Q_a Q_b = Q_{a+b}. (ii) The transpose M^T is a
normalised solution (alpha' = 1 + beta, beta' = alpha - 1). (iii) Let R(M) be
the set of all vertical ratios M_{s+1,t}/M_{st} and horizontal ratios
M_{s,t+1}/M_{st} over cells with M_{st} != 0, read as integers in [0,p).
Recentring and transposing permute the cells and preserve ratios of
neighbouring cells, so R is invariant. (iv) Take the cell (after transposing
if the minimum is a horizontal ratio) at which min R(M) is attained and
recentre there: the result M* has c*_1 = M*_{10}/M*_{00} = min R(M*). Hence
*the instance is feasible iff a normalised solution with c_1 = min R exists*
("canonical"). The search is restricted to canonical solutions: with v = c_1,
every ratio in R must be >= v. dfs2b enforces only the subset of these
necessary conditions decidable from the current partial assignment (enforcing
fewer is still sound):
- (2a) consecutive assigned rows s, s+1 (mod kappa): c_{s+1}/c_s >= v;
- (2b) consecutive assigned rows s, s+1 and x in S_t: keep x only if
  x + beta_s = 0 or (x + beta_{s+1})/(x + beta_s) >= v;
- (2c) column pair (0,1) in an assigned row s: keep x in S_1 only if
  (x + beta_s)/c_s >= v;
- (2d) zeros: if v != 0 then M has no zero cell. Proof: in a normalised
  solution all beta_i are distinct (two equal rows i != i' lie in
  A_{-(i+j)} cap A_{-(i'+j)} = {0}, so they are zero rows, so every alpha_j
  equals -beta_i, so all alpha_j = alpha_0 = 1, but 1 is not in A_{-1} for
  kappa >= 2); likewise all alpha_j are distinct. So each column has at most
  one zero; if M_{ut} = 0 then M_{u-1,t} != 0 and 0 = M_{ut}/M_{u-1,t} is in
  R, forcing v = 0. Therefore for v != 0 dfs2b deletes -beta_s from every S_t
  for every assigned row s (s = 0 gives x = 0), rejects b with 1 + b = 0, and
  every inverse in (2a)-(2c) exists. For v = 0 (beta_1 = -1) nothing binds.
Soundness as a whole: if the restricted search finds no leaf, no canonical
normalised solution exists, hence (by the displayed equivalence) no normalised
solution exists, which is dfs2's INFEASIBLE. If it finds a leaf, the leaf
satisfies the original constraints (filters only delete elements) and is
re-checked on all kappa^2 cells. Row 1 is always assigned first so v is known
from level 1 on; at level 0 all rows have equal domain size anyway.

The symmetry group here is the Z_kappa^2 x Z_2 of double cyclic shifts with
renormalisation plus transpose (order 2 kappa^2 = 128 for kappa 8, 162 for
kappa 9), acting on sum matrices with no zero cell; the canonical-corner rule
is the standard "lexicographic leader" argument for it. For v small the
ratio conditions bind weakly, for v near p strongly, so the realised gain is
well below 2 kappa^2 (measured: 348,029 nodes against dfs2's 6,620,653 at
kappa 8, p = 4201, i.e. 19x fewer nodes with Prunes 1+2 together, on top of
the per-node speed-up; the node counts of the two programs count the same
thing, internal nodes of the search tree).

**Independent check of the lemma [exact].** `symcheck.py` (scratchpad, listing
in §5) enumerates by brute force *every* normalised solution for 20 small
instances (kappa 3-6, p up to 73; 8 feasible, 12 infeasible; 2-191 solutions
each) and verifies, for every solution: every recentring and the transpose are
normalised solutions; R is invariant; some sibling is canonical; alpha and
beta are injective; every canonical sibling with v != 0 is zero-free; and
every canonical sibling passes dfs2b's full filter set (2a)-(2d). All checks
passed (`ALL CHECKS PASSED`).

## 2. Validation [exact]

All runs: `dfs2b K P0 P1 2000000000` (full mode: Prunes 1 and 2), ground truth
as named. No LIMIT line anywhere; no `UNEXPECTED_EMPTY` flag (which would mark
a candidate that dfs2b's viability test accepted but whose child sets came
out empty, i.e. an internal inconsistency).

| kappa | range run | INFEASIBLE found | ground truth | agree | time, all INFEASIBLE primes |
|---|---|---|---|---|---|
| 4 | [5, 3000] | 6 | E_2(4) = {5,13,17,29,37,53} (`xval_k4.out`, SPA) | yes | < 0.01 s |
| 5 | [6, 20000] | 9 | E_2(5), 9 primes (`xval_k5.out`, SPA) | yes | < 0.01 s |
| 6 | [7, 20000] | 53 | E_2(6), 53 primes, largest 859 (`xval_k6.out`) | yes | 0.03 s total |
| 7 | [3, 20000] | 56 | E_2(7), Theorem 6 (`E2_k7.txt`) | yes, identical list | 8.9 s total, max 1.7 s (p = 3221, 977,481 nodes) |
| 8 | [9, 4201] | 132 | dfs2's 50 decided primes in [2442, 4201] (`dfs2_k8.out` + 6 reruns) | yes: the 50 agree and every prime dfs2 decided FEASIBLE is FEASIBLE here | 23 s total, max 1.4 s (p = 4201, 348,029 nodes) |

Note on kappa 8: dfs2's range started at 2442; dfs2b also ran [9, 2441] and
found 82 further INFEASIBLE primes there, so only 5 primes p = 1 (mod 8) up to
4201 are NOT in E_2(8) (consistent with SPA's small-kappa picture; not needed
for this task). Scratch outputs: `k5_full.out` ... `k8_full.out` in the
scratchpad; only the `dfs2b_*.out` files for the LIMIT primes are kept in SP.

**Node-for-node agreement in `plain` mode [exact].** `dfs2b 7 1597 1597 ... plain`
gives `nodes=205272`, exactly dfs2's count for p = 1597 (`dfs2_k7.out`), in
0.13 s. Further plain-mode counts are in §3 (cross-checks).

## 3. LIMIT primes resolved

Command per prime:
`nice -n 10 timeout 14400 ./dfs2b K p p 4000000000 print > dfs2b_kK_p.out`
(SP), two jobs at a time on a 10-core machine with load average 3-7 from
other work. Every answer below is a complete search (no LIMIT), **[exact]**.

### kappa = 8 (dfs2 LIMIT at 5e7 nodes, killed at 5400 s)

| p | dfs2b answer | nodes | wall time | file |
|---|---|---|---|---|
| 6073 | INFEASIBLE | 4,560,676 | 14.9 s | `dfs2b_k8_6073.out` |
| 6089 | INFEASIBLE | 4,763,467 | 16.5 s | `dfs2b_k8_6089.out` |
| 8009 | INFEASIBLE | 25,558,461 | 103.8 s | `dfs2b_k8_8009.out` |

### kappa = 9 (dfs2 LIMIT at 5e6 nodes, never rerun)

| p | dfs2b answer | nodes | wall time | file |
|---|---|---|---|---|
| 6067 | INFEASIBLE | 318,496 | 2.6 s | `dfs2b_k9_6067.out` |
| 7507 | INFEASIBLE | 1,229,392 | 9.1 s | `dfs2b_k9_7507.out` |
| 7669 | INFEASIBLE | 1,685,675 | 11.7 s | `dfs2b_k9_7669.out` |
| 7561 | INFEASIBLE | 1,578,487 | 11.9 s | `dfs2b_k9_7561.out` |
| 9613 | INFEASIBLE | 8,744,521 | 56.0 s | `dfs2b_k9_9613.out` |
| 9631 | INFEASIBLE | 8,632,346 | 56.2 s | `dfs2b_k9_9631.out` |
| 11503 | INFEASIBLE | 29,409,125 | 194.8 s | `dfs2b_k9_11503.out` |
| 13537 | INFEASIBLE | 83,320,096 | 622.8 s | `dfs2b_k9_13537.out` |
| 15607 | INFEASIBLE | 191,893,527 | 1686.7 s | `dfs2b_k9_15607.out` |
| 15643 | INFEASIBLE | 195,027,696 | 1713.6 s | `dfs2b_k9_15643.out` |
| 17551 | INFEASIBLE | 358,113,721 | 3339.3 s | `dfs2b_k9_17551.out` |

All 14 LIMIT primes are INFEASIBLE, i.e. in E_2(kappa). Largest INFEASIBLE
prime now known: kappa 8: **8009** (was 4201); kappa 9: **17551** (was 5923).
Node counts grow like p^6 along the kappa 9 list (8.7M at 9613, 358M at
17551), so each further prime near 20000 costs about one to two hours.

### Independent cross-checks of newly INFEASIBLE primes [exact]

Three different searches of the same instance, one newly resolved prime per
kappa (files in SP):

| kappa, p | mode | what it is | answer | nodes | time |
|---|---|---|---|---|---|
| 8, 6073 | `plain` | dfs2's own tree: static row order, no forward checking, no symmetry prune; only the per-node set arithmetic differs | INFEASIBLE | 73,092,055 | 139.3 s |
| 8, 6073 | `nosym` | Prune 1 only (forward checking, most-constrained row first), no symmetry prune | INFEASIBLE | 65,229,218 | 139.9 s |
| 8, 6073 | full | Prunes 1 + 2 | INFEASIBLE | 4,560,676 | 14.9 s |
| 9, 6067 | `plain` | as above | INFEASIBLE | 6,407,153 | 15.2 s |
| 9, 6067 | `nosym` | as above | INFEASIBLE | 4,253,098 | 24.1 s |
| 9, 6067 | full | Prunes 1 + 2 | INFEASIBLE | 318,496 | 2.6 s |

The plain-mode node counts explain dfs2's LIMITs exactly: 73.1M > dfs2's 5e7
budget at kappa 8, and 6.4M > its 5e6 budget at kappa 9 (dfs2 never reran
kappa 9). The plain-mode tree is dfs2's tree: `dfs2b ... plain` reproduces
dfs2's node counts to the last digit on kappa 7 p = 1597 (205,272) and
p = 2731 (6,239,108, `dfs2b_k7_2731_plain.out` vs `dfs2_k7_rerun_2731.out`).
So the INFEASIBLE verdicts on 6073 and 6067 do not rest on the symmetry prune
or on the row ordering; the symmetry prune's correctness is in addition
checked by the brute-force lemma test of §1 and by the exact agreement of the
full mode with the known sets E_2(4..7) and dfs2's kappa-8 verdicts (§2).
The remaining kappa 9 primes above 6067 were run in full mode only (plain
mode would take hours each); their verdicts rest on the proved prunes of §1
and the validations above.

## 4. Statement that now holds, what is missing, proposed paper text

**Holds [exact, with the prunes proved in §1 and checked in §1-§3].**
- Every prime previously left at LIMIT by dfs2 is in E_2(kappa):
  kappa 8: 6073, 6089, 8009; kappa 9: 6067, 7507, 7561, 7669, 9613, 9631,
  11503, 13537, 15607, 15643, 17551.
- kappa = 8: every prime p = 1 (mod 8) with p <= 4201 is decided
  (`k8_full.out`, this pass; 132 of the 137 such primes are in E_2(8); the
  five that are not are 1553, 3089, 3121, 3361, 4177; the verdicts agree with
  dfs2 on [2442, 4201]). Above 4201 the decided primes are
  exactly those dfs2's killed chunks printed plus the three above; the
  largest known element of E_2(8) is 8009.
- kappa = 9: every prime p = 1 (mod 9) in [3584, 5689] is decided (dfs2 round
  1), plus dfs2's five INFEASIBLE primes 5743-5923 and the eleven above; the
  largest known element of E_2(9) is 17551.
- dfs2b reproduces E_2(4), E_2(5), E_2(6), E_2(7) exactly and agrees with
  every kappa 8 verdict of dfs2, and in `plain` mode it reproduces dfs2's
  search tree node for node.

**Missing.**
- E_2(8) is NOT established on (4201, 20000] and E_2(9) is NOT established
  on (5689, 20000] except at the primes listed: dfs2's chunk runs were killed
  with unknown reach and FEASIBLE primes print nothing. A complete rescan
  with dfs2b is now affordable for kappa 8 (all 132 primes <= 4201 took 23 s;
  8009 took 104 s): `./dfs2b 8 4202 20000 4000000000 print`, estimated a few
  hours, output `dfs2b_k8_4202_20000.out`, acceptance test: a DONE line with
  limit=0. For kappa 9 the same scan on (5689, 20000] costs roughly an hour
  per infeasible prime above 15000 (about 2-4 CPU-days if most are
  infeasible, which the node growth suggests); chunk it and run on an idle
  machine. Neither was run here (out of the brief's scope).
- Since the known exceptional primes for kappa <= 7 reach 1.3-1.7 times
  kappa^{(kappa+1)/2} (= 11,585 for kappa 8 and 59,049 for kappa 9), E_2(8)
  may well extend beyond 20000 and E_2(9) certainly may; "largest known" is
  not "largest". [argued]
- dfs2b is AI-written and AI-checked; the soundness arguments in §1 and the
  header of `dfs2b.c` await human review. The brute-force lemma check covers
  kappa <= 6 and p <= 73 only.
- Above T_A(kappa) the Weil-threshold theorem of `2026-11-02-rees-weil-threshold.md`
  decides everything; the gap (20000, T_A(8) = 1.17e8] is unchanged.

**Proposed paper text** (for the E_2 discussion, replacing "for kappa >= 8
only bounds on E_2(kappa) are known"):
"For $\kappa = 8$ and $9$ the exceptional sets are not known exactly, but an
exhaustive search with symmetry breaking (\file{research/audits/reviews/2026-11-03-rees-dfs2-prune.md})
shows that $8009 \in E_2(8)$ and $17551 \in E_2(9)$, so the largest exceptional
prime is at least $0.69\,\kappa^{(\kappa+1)/2}$ for $\kappa = 8$ and at least
$0.30\,\kappa^{(\kappa+1)/2}$ for $\kappa = 9$; every prime $p \equiv 1 \pmod 8$
up to $4201$ and every prime $p \equiv 1 \pmod 9$ up to $5689$ is decided."

## 5. Listing of `symcheck.py` (scratchpad; run with `/opt/anaconda3/bin/python -I symcheck.py`, output `ALL CHECKS PASSED`)

```python
"""Brute-force check of the symmetry lemma used by dfs2b.c (PRUNE 2).

For small kappa and p: enumerate EVERY normalised solution (alpha_0 = 1, beta_0 = 0,
alpha_j + beta_i in A_{-(i+j)}), and verify:
  (1) recentring at any nonzero cell, and transposing, give normalised solutions;
  (2) the ratio set R(M) is invariant under these maps;
  (3) every solution has a sibling with c_1 = min R   (so restricting to canonical
      solutions is sound: feasible <=> a canonical solution exists);
  (4) all beta_i distinct, all alpha_j distinct;
  (5) if c_1 != 0 and c_1 = min R then M has no zero cell;
  (6) a direct count: number of canonical solutions >= 1 iff number of solutions >= 1.
Also checks that the FULL filter set of dfs2b (2a-2d) accepts every canonical solution
(no canonical solution is wrongly pruned when all rows are assigned).
Interpreter: /opt/anaconda3/bin/python
"""
import itertools, sys

def primroot(p):
    n = p - 1; f = []; m = n; q = 2
    while q * q <= m:
        if m % q == 0:
            f.append(q)
            while m % q == 0: m //= q
        q += 1
    if m > 1: f.append(m)
    g = 2
    while True:
        if all(pow(g, (p - 1) // r, p) != 1 for r in f): return g
        g += 1

def setup(p, k):
    g = primroot(p); idx = [None] * p; x = 1
    for e in range(p - 1):
        idx[x] = e % k; x = x * g % p
    A = [set([0]) | {y for y in range(1, p) if idx[y] == m} for m in range(k)]
    return idx, A

def inA(y, m, idx, k):
    return y == 0 or idx[y] == m % k

def solutions(p, k, idx, A, cap=200000):
    sols = []
    for beta in itertools.product(range(p), repeat=k - 1):
        beta = (0,) + beta
        if not all((1 + beta[i]) % p in A[(-i) % k] for i in range(1, k)):   # column 0: alpha_0 = 1
            continue
        S = []
        ok = True
        for j in range(1, k):
            Sj = [x for x in A[(-j) % k] if all((x + beta[i]) % p in A[(-(i + j)) % k] for i in range(1, k))]
            if not Sj: ok = False; break
            S.append(Sj)
        if not ok: continue
        for al in itertools.product(*S):
            sols.append(((1,) + al, beta))
            if len(sols) > cap: return sols, False
    return sols, True

def M_of(alpha, beta, p, k):
    return [[(alpha[j] + beta[i]) % p for j in range(k)] for i in range(k)]

def is_norm_sol(M, p, k, idx):
    if M[0][0] != 1: return False
    for i in range(k):
        for j in range(k):
            if (M[i][j] - M[i][0] - M[0][j] + M[0][0]) % p: return False   # sum matrix
            if not inA(M[i][j], -(i + j), idx, k): return False
    return True

def ratios(M, p, k):
    R = set()
    for s in range(k):
        for t in range(k):
            if M[s][t]:
                iv = pow(M[s][t], p - 2, p)
                R.add(M[(s + 1) % k][t] * iv % p)
                R.add(M[s][(t + 1) % k] * iv % p)
    return R

def recenter(M, s, t, p, k):
    iv = pow(M[s][t], p - 2, p)
    return [[M[(i + s) % k][(j + t) % k] * iv % p for j in range(k)] for i in range(k)]

def transpose(M, k):
    return [[M[j][i] for j in range(k)] for i in range(k)]

def filters_accept(M, p, k):
    """dfs2b's enforced conditions 2a-2d on a complete solution with v = c_1."""
    v = M[1][0]
    if v == 0: return True
    for i in range(k):
        for j in range(k):
            if M[i][j] == 0: return False                       # 2d
    for s in range(k):
        s1 = (s + 1) % k
        for t in range(k):                                      # 2a (t=0) and 2b (t>=1)
            if M[s1][t] * pow(M[s][t], p - 2, p) % p < v: return False
        if M[s][1] * pow(M[s][0], p - 2, p) % p < v: return False   # 2c
    return True

def check(p, k):
    idx, A = setup(p, k)
    sols, complete = solutions(p, k, idx, A)
    ncanon = 0
    for alpha, beta in sols:
        M = M_of(alpha, beta, p, k)
        assert is_norm_sol(M, p, k, idx)
        assert len(set(beta)) == k and len(set(alpha)) == k, "distinctness"
        R = ratios(M, p, k)
        found = False
        for Mx in (M, transpose(M, k)):
            assert is_norm_sol(Mx, p, k, idx), "transpose"
            for s in range(k):
                for t in range(k):
                    if Mx[s][t]:
                        Mr = recenter(Mx, s, t, p, k)
                        assert is_norm_sol(Mr, p, k, idx), "recentre"
                        assert ratios(Mr, p, k) == R, "ratio set not invariant"
                        if Mr[1][0] == min(R):
                            found = True
                            assert filters_accept(Mr, p, k), "canonical solution rejected by filters"
                            if Mr[1][0] != 0:
                                assert all(Mr[i][j] for i in range(k) for j in range(k)), "zero cell with v != 0"
        assert found, "no canonical sibling"
        if M[1][0] == min(R): ncanon += 1
    return len(sols), ncanon, complete

if __name__ == "__main__":
    cases = [(3, 7), (3, 13), (3, 19), (3, 31), (4, 13), (4, 17), (4, 29), (4, 37), (4, 41), (4, 53), (4, 61), (4, 73),
             (5, 11), (5, 31), (5, 41), (5, 61), (6, 13), (6, 19), (6, 31), (6, 37)]
    for k, p in cases:
        n, nc, complete = check(p, k)
        print(f"k={k} p={p} solutions={n}{'' if complete else '+ (capped)'} canonical={nc} "
              f"{'INFEASIBLE' if n == 0 else 'FEASIBLE'} lemma_ok")
    print("ALL CHECKS PASSED")
```

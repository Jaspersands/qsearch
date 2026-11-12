# Diagonal SDE, largest dead banks at κ = 6, p = 31, 37, 43: all three cells computed exactly

AI-only pass, 12 November 2026, one Claude Code helper session. Not human-reviewed. No git, no
network. Only this file and the folder `2026-11-12-rees-sde-dead-k6/` were written. The 11 Nov
note and its folder were read and not edited. Interpreter: `/opt/anaconda3/bin/python -I`.
C: Apple clang 21, `cc -O2`. Every run used `nice -n 19`. Peak RSS was under 6 MB (C) and 226 MB
(Python). The longest single run took 18 s, and the whole pass used minutes of CPU.

Definitions as in `2026-11-11-rees-sde-near-linear-total.md` (lines 13–19 and the dead_w2 bullet,
lines 335–351). P = (F_p^×)^κ, P₀ = P ∪ {0}. A bank is a multiset of nonzero columns, with
repetition allowed. It is dead if Σ x_i λ_i = 0 has no solution x ∈ P₀^n ∖ {0}. m1 is the largest
dead bank in F_p¹. m2 is the largest dead bank in F_p² that spans F_p². N(κ, 2, p) = m2 + 1.

## 1. Results

| κ | p | −1 ∈ P | m1 | m2 | N(κ,2,p) | #max_ext (dead_w2 count) | status |
|---|---|---|---|---|---|---|---|
| 6 | 31 | no | **4** | **8** | 9 | 25791 | exact |
| 6 | 37 | yes | 3 | **6** | 7 | 3625 | exact |
| 6 | 43 | no | 3 | **6** | 7 | 66558 | exact |

Status labels:
- Lower bounds: **PROVED**. Each cell has an explicit dead bank of size m2, and brute force over
  all of P₀^n confirms it (`brute_verify.out`).
- Upper bounds: **exact by exhaustive computation**. Two implementations agree, and both are
  validated against all 20 reference rows (§3). This is computer-assisted, AI-checked and pending
  human review.
- Every value lies within Chevalley–Warning (m1 ≤ κ = 6, m2 ≤ κa = 12).

The new facts are:
- At p = 31, m2 = 8 exceeds the value 7 found at p = 13 and 19. The sequence in p is not monotone.
- The p = 31 anomaly has an explanation. 31 = 2⁵ − 1, so P = ⟨2⟩ = {1, 2, 4, 8, 16}.
  - **Hand proof that m1 ≥ 4 and m2 ≥ 8 at p = 31 [PROVED].** Take the bank (1,0)⁴, (0,1), (1,1)³.
  - A sum of j ≤ 4 elements of P is an integer in [0, 64]. To vanish mod 31 it must equal 0, 31
    or 62. The binary weights of 31 and 62 are 5, and a sum of j powers of two has binary weight
    at most j. So the sum is 0, which forces every term to be 0.
  - The second coordinate y + z₁ + z₂ + z₃ has at most 4 terms, so y = z = 0. Then the first
    coordinate x₁ + … + x₄ = 0 forces x = 0.
  - The same argument shows that four copies of 1 form a dead bank in F_31¹.
  - The exhaustive search shows these values are maximal: m1 = 4, so N(6, 1, 31) = 5, and m2 = 8.
- In all three cells, m2 = 2·m1. This is attained by the two-line banks (m1 columns on each of two
  independent lines). Banks with at least 3 projective points also reach m2
  (`threepoint_max.out`).

**Supplementary cells [exact, same method]** (`k6_extension.out`, 8-word bitsets): for κ = 6,

| p | 61 | 67 | 73 | 79 |
|---|---|---|---|---|
| (m1, m2) | (2, 5) | (3, 6) | (3, 6) | (3, 6) |

So N(6, 2, p) > 2a + 1 = 5 for every tested p ≤ 79. Reaching 5 needs m1 = 2, since m2 ≥ 2·m1 and
5 = 2·2 + 1. For comparison, (E4) guarantees N(6, 1, p) = 3 only for p ≥ 6⁴ = 1296.

## 2. Method (`deadcone.c`)

**Lemma (cone rule) [PROVED].**
- Let C(B) = {Σ x_i λ_i : x ∈ P₀^n}, the cone. It is P-stable: s·Σ x_iλ_i = Σ (s x_i)λ_i. So it is
  a union of P-orbits ("classes") of F_p² ∖ {0}, plus 0. There are (p+1)κ classes: 192, 228 and
  264 at p = 31, 37, 43.
- Let B be dead and λ ≠ 0. Then B + λ is dead iff class(−λ) ∉ C(B).
  - Proof: a solution of B + λ must have x_λ ≠ 0, because B is dead. Then −x_λ λ = Σ_B x_i λ_i ∈ C(B).
    By P-stability this happens iff class(−λ) ∈ C(B).
- Recursion: C(B + λ) = C(B) ∪ Pλ ∪ (C(B) + Pλ).
- For orbits A = Pa and B = Pb, A + B = P·{a + ub : u ∈ P}. This is precomputed as a class bitset
  T[A][B].

The code stores D = −C(B) as a bitset of at most 320 bits. "B + L dead" is a single bit test, and
the update ORs at most |D| table rows. Every subset of a dead bank is dead, and every prefix of a
dead multiset in sorted order is dead. So a depth-first search over multisets in nondecreasing
class index with this exact test enumerates every dead multiset exactly once. Nothing is stored
except the recursion stack (depth ≤ 13).

**Two independent search frames:**
- `w2` mode is the frame of dead_w2.py. The base is e1, e2. The candidates are the classes dead
  with the base, in the same class order: point t < p is (1, t), point p is (0, 1), and
  class = pt·κ + e with representative g^e·point. The mode reproduces dead_w2's m1, m2, #max_ext
  and #cand_3 counts digit for digit.
- `tri` mode uses 3-transitivity of PGL₂.
  - A spanning dead bank with at least 3 projective points maps under GL₂ to one containing
    g^{c1}e1, g^{c2}e2 and (1,1), for some c1, c2 ∈ Z/κ (36 bases).
  - A bank on exactly 2 points has independent line components. It is dead iff both components
    are dead, so its maximum is 2·m1.
  - So m2 = max(2·m1, tri maximum).

m1 uses the same rule on Z/κ (1-dimensional classes g^e).

## 3. Validation

1. **`w2_validation.out` vs `dead_w2_rerun.out`.** The C cone code in `w2` mode reproduces all 20
   final rows exactly: m1, m2, #max_ext and #cand_3, for κ = 3 (8 primes), κ = 4 (6), κ = 5 (4)
   and κ = 6 (p = 13, 19). The reference rows come from a different algorithm, the kernel
   enumeration in sdecore.py. κ = 6, p = 19 took 61664 s there and 0.04 s here.
2. **`indep_cone.py`.** This is an independent Python implementation with no class tables:
   - the cone is a p×p boolean array of vectors, updated by `np.roll`;
   - the deadness test checks all |P| vectors of −Pλ, so P-stability is not assumed;
   - m1 is computed by brute force over P₀^n;
   - it imports only `primroot` and the reference class list `classes2` from the 11 Nov folder.
   It matches 12 reference rows and gives the same three new rows, including #max_ext
   (`indep_cone.out`).
3. **`tri` mode.** This different symmetry reduction gives the same m1 and m2 on all 23 cells
   (`tri_crosscheck.out`).
4. **`brute_verify.py` (brute force over P₀^n, no cone code):**
   - every example maximum bank (w2 and tri modes, κ = 6, p = 13…43) has rank 2 and 0 nonzero
     solutions;
   - its brute-force cone is all of F_p², so it is locally maximal;
   - on 2000 random banks (400 per prime, n = 3…7, about 29% dead), the deadness flag from
     `deadcone check` agrees with brute force 2000/2000 times.
5. **`compare_rerun.py` → `compare_rerun.out`.** Automated diff of items 1–3: 52 comparisons,
   0 mismatches.

## 4. Comparison with dead_w2.py

dead_w2.py uses the same search tree, but its `is_dead` enumerates every projective point of the
(n−2)-dimensional kernel: p^{n−3} points, materialized as `proj_points` and `T @ Phi`. At n = 8
and p = 31 that is about 2.9·10⁷ rows × n int64 per test. This explains the memory kill. The cone
rule replaces each test with one bit lookup and an O(|D|·W) update. The search tree and its counts
are unchanged. Nodes visited: 3.4·10⁵ at p = 19, 5.6·10⁵ at p = 31.

## 5. Proposed text for the dead_w2 bullet (do not apply without the integrator)

Replace the two sub-bullets "κ = 6: m2 = 7 at p = 13 and at p = 19 …" and "κ = 6 at p = 31, 37,
43: NOT computed …" with:

> - κ = 6: m2 = 7 at p = 13 and at p = 19 (m1 = 3 both); m2 = 8 at p = 31 (m1 = 4); m2 = 6 at
>   p = 37, 43 (m1 = 3). The p ≥ 31 cells come from `2026-11-12-rees-sde-dead-k6/deadcone.c` [exact]:
>   - it is the same search tree with a P-stable cone bitset instead of kernel enumeration;
>   - it reproduces all 20 rows above, including #max_ext;
>   - it is cross-checked by an independent numpy implementation and by brute force.
>
>   At p = 31, P = ⟨2⟩, and binary weight shows that (1,0)⁴, (0,1), (1,1)³ is dead (hand proof in
>   the 12 Nov report). Supplementary [exact]: (m1, m2) = (2, 5), (3, 6), (3, 6), (3, 6) at
>   p = 61, 67, 73, 79.

and change the closing sentence to:

> So, at a = 2, N(κ, 2, p) reaches 2a + 1 = 5 already at p = 37 (κ = 4) and p = 61 (κ = 5), but
> not for κ = 6 at any p ≤ 79. There N(6, 2, p) ∈ {6, 7, 9}, with m2 = 2·m1 except at p = 13, 19, 61.
> The values are not monotone in p (N(6, 2, 31) = 9). All rows are within Chevalley–Warning.
> This is still falsification-level evidence at a = 2 only.

## 6. Adversarial self-check

- **Is the symmetry reduction sound?**
  - GL₂: Σ x_i Mλ_i = M Σ x_i λ_i, so solution sets are preserved.
  - P-scaling of one column: x_i ↦ x_i s⁻¹ bijects P₀.
  - A spanning bank has two independent columns, and some M sends them to e1, e2 (both class 0).
    So w2 mode loses nothing.
  - tri mode: PGL₂ is sharply 3-transitive on P¹(F_p). After mapping three points to
    [1:0], [0:1], [1:1], rescale M by the inverse of the third coefficient (still in GL₂). This
    fixes the third class to 0 and leaves (c1, c2) free. All 36 are searched.
  - The 2-point case is exactly 2·m1: the coordinates in the basis of the two lines decouple.
  - Repetitions of a class are allowed in both modes (the DFS restarts at index L, not L + 1), as
    in dead_w2.py.
  - The sign issue is handled: neg(L) is computed from the vector −rep(L), not assumed to be L.
- **Shared-assumption risk.** The C code and indep_cone.py both rest on the cone lemma. A flaw
  there would be shared. But the lemma is proved above, the 20 reference rows come from kernel
  enumeration, and brute force checks deadness with no lemma at all.
- **Residual risk.** Global maximality at the new cells (no dead 9-bank at p = 31, no dead 7-bank
  at p = 37, 43) is certified only by the two exhaustive searches. No different-kind check was
  run, such as a SAT/ILP certificate or a Weil/CW argument proving m2 ≤ 8 or ≤ 6. The
  local-maximality brute force does not prove global maximality.
- **Other code risks, checked:**
  - a class-count overflow aborts the program (NC ≤ 64W);
  - κ | p − 1 is enforced;
  - products stay below p² in `long`;
  - the 8-word build reproduces the 5-word p = 31 row.
- **Not claimed.** Nothing here proves any statement for general p, and nothing bears on the
  a-independent-threshold conjecture beyond a = 2 and p ≤ 79. It is evidence only, per trap 7.
  No claim gate is touched.

Files (all in `research/audits/reviews/2026-11-12-rees-sde-dead-k6/`):
- code: `deadcone.c` (binaries `deadcone`, `deadcone8`), `indep_cone.py`, `brute_verify.py`,
  `compare_rerun.py`;
- outputs: `w2_validation.out`, `indep_cone.out`, `tri_crosscheck.out`,
  `tri_full_k6_p{31,37,43}.out`, `threepoint_max.out`, `k6_extension.out`, `brute_verify.out`,
  `compare_rerun.out`;
- `SHA256SUMS`.

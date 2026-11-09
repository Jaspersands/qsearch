# Worst-case F_3^n subset sum below n²/3: NEST made worst-case by series-class peeling and the second Pless moment, m = n²/4 + O(n^{3/2}) deterministic

AI-only pass, 8 November 2026, one Claude Code session; not human-reviewed; no novelty or
priority claim (the only literature consulted is `2026-11-07-rees-sde-subquad-lit.md`, KOW =
arXiv 2510.07515, KOMSW = arXiv 2609.40321). Inputs: the pass `2026-11-08-rees-sde-p3.md` and
its referee `2026-11-08-rees-sde-p3-referee.md`. Scripts and outputs are in
`2026-11-08-rees-sde-p3-nest/`, interpreter `/opt/anaconda3/bin/python -B`. Only this file and
that folder were written; no git, no network, `make_numbers.py` not run.

Labels: **[proved]** complete proof here; **[exact]** finite computation, script named;
**[sampled]** exact arithmetic on random or constructed instances; **[argued]**; **[conjecture]**;
**[literature]**. Every statement says whether it is worst-case or average-case.

**Corrections of 9 Nov 2026 (mechanical pass; no new claim, no change of any conclusion).** After the
referee and break reports: (i) `wnest.py` now runs WNEST at q ≥ 4 and a KOW round with pool q + 1 at q ≤ 3
(it ran WNEST at q = 3 and used KOW's pool q + ⌈log₃(q+1)⌉, so its own worst case was guarantee(n) + 2 for
odd n); `tables.py` is rerun with identical numbers; (ii) the "guaranteed 63, 84, 109, 135" in §3 are bound(n),
the exact guarantee(n) is 46, 64, 85, 108; (iii) the dual-distance and KOW-comparison statements are corrected
in §0 and Lemma M; Remark (b) is marked unproved. See `2026-11-09-mechanical-queue-run.md`.

Problem. v_1..v_m ∈ F_3^n arbitrary (worst case); find nonempty S with Σ_{i∈S} v_i = 0 in
poly(n, m) time. Best proved worst-case threshold before this note: KOW Theorem 1.2,
m ≥ n²/3 + O(n log n), deterministic [literature].

## 0. Verdict

1. **Theorem A (worst case) [proved; §2].** For every n ≥ 4 and every instance with
   m ≥ n²/4 + (8/9)(n+2)^{3/2} + 4n + 2√n + 15 columns, the deterministic algorithm WNEST
   (§2) outputs a nonempty zero-sum subset in poly(n, m) time. So the worst-case constant drops
   from 1/3 (KOW) to 1/4. The exact recursion behind the bound (`tables.out`) is below this note's
   sharpened KOW-type recursion (`kow_recursion()` in `tables.py`, which is NOT KOW's recursion
   (8)) for every n ≥ 35 (n = 64: 1433 vs 1536; n = 1000: 269 044 vs 337 479). Against KOW's own
   recursion (8), m_l = max{l, m_{l−1} + 2(l+1)/3 + ⌈log₃(l+1)⌉}, it is below for 9 ≤ n < 3000
   (15 ≤ n < 3000 with integer pieces; n = 64: 1433 vs 1651) [referee `recursion_ref.out`]. The
   explicit closed form of Theorem A is below KOW's explicit closed form only for n > 80 (below
   (8) only for n > 105), so it is not an explicit improvement for small n.
   The three ingredients: the referee's NEST piece (a dependency δ with |supp δ| ≥ rank(supp δ)+2
   carries a second dependency, and the pass's Theorem 4 gadget realizes 2 dimensions for
   |supp δ| columns); **series-class peeling** (Lemma P: deleting a series class of size a drops
   the rank by ≥ a−1, so N − 1.5·rank never decreases and the pool's dependency code ends with no
   coloop and every proportionality class of size ≤ 2, i.e. dual distance ≥ 2 [corrected after
   the referee: series PAIRS survive peeling, so dual distance ≥ 3 is not reached]); and the
   **second Pless moment** (Lemma M: with no coloop and all classes of size ≤ 2 the
   weight of a uniform codeword has mean 2N*/3 and variance ≤ 4N*/9 (tight, attained when all
   classes are pairs; true dual distance ≥ 3 would give 2N*/9), and conditional
   expectations give a codeword within one standard deviation deterministically). The referee
   asked for a dependency of weight in [q+2, (4/3−ε)q] with nested structure in every pool; after
   peeling one of weight in [q+2, q + (8/3)√q + 4] always exists and is found.
2. **NEST re-derived, constant and recursion (average case) [proved for the cost recursion,
   sampled for the per-piece input].** A NEST piece at codimension q costs |X| = q + 2 + O(1)
   on uniformly random instances; the recursion m(q) = m(q−2) + q + O(1) gives n²/4 + O(n).
   The constant is exactly 1/4, not below. My implementation (`wnest.py`, every witness checked
   by summation over the original vectors) gives 0.2596–0.2601 n² at n = 150 for the Las Vegas
   refinement WNEST+ (cost exactly q + 2 per piece; Σ(q+2) = n²/4 + 3n/2) and 0.285 n² for the
   purely deterministic WNEST at n = 150 (its n^{3/2} term is real: it needs n ≥ 35 to beat
   the note's sharpened KOW-type recursion (n ≥ 9 for KOW's recursion (8)) and n between 120 and 150 to beat KOW's observed random-instance cost 0.289 n²).
3. **Tightness and the frontier [proved + exact; §4].** Any piece gaining d ≥ 2 dimensions has
   dim D(X) ≥ 2, so |X| ≥ rank(X) + 2 (Lemma 3 of the pass); a scheme whose pieces are in
   general position (rank(X) = min(|X|, q)) and gain ≤ 2 therefore spends ≥ Σ(q_j + 2) ≥ n²/4.
   Three dimensions from one piece: pattern-complete bundles never gain 3 for k ≤ 4 (SAT, exact:
   all 26 patterns of F_3^3 and all 80 of F_3^4 are UNSAT for d = 3), and the configurations
   that worst-case-findable mechanisms produce (δ_1 of full support: 9 points of PG(2,3) off a
   line; the nested chain supp δ_3 ⊆ supp δ_2 ⊆ supp δ_1 = X, 7 points; two disjoint
   dependencies inside a full-support one, 5 points) are all UNSAT for d = 3. §4 lists the
   feasible point sets of PG(2,3) for d = 3 (`pattern_sat.out`): among the 29 PGL(3,3)-orbits of
   negation-closed configurations exactly two are feasible, and both are disjoint unions of a
   KOW piece with another KOW or NEST piece, so no connected 3-dependency bundle gains 3. Going
   below 1/4 needs a piece with k ≥ 4 dependencies
   whose pattern configuration misses a prescribed part of PG(2,3), which on general-position
   instances is a search over column sets, not linear algebra on a pool.
4. **What was wrong in the pass and right in the referee.** The pass's barrier (Theorem 6) is
   dead for the reason the referee gave, and more: the referee's "weight gap around q in every
   shortened code" adversary is impossible once series classes are peeled, because the second
   moment of the weight is then fixed. The referee's 82 non-trivial feasible pattern sets and
   its Theorem 4 correction (empty unions) are re-derived and confirmed (`pattern_sat.out`).
5. **Weakest step.** Theorem A has no probabilistic step; its weakest point is the lower-order
   term, O(n^{3/2}) against KOW's O(n log n) (the window [r*+2, μ+σ] has width Θ(√N), and an
   adversary whose code keeps series pairs (dual distance exactly 2 after peeling, variance
   4N*/9) controls all higher moments). Everything else is
   finite linear algebra; the parts a referee should attack are Lemma P (rank drop of a series
   class), Lemma M (the variance formula), and the accounting of returned columns (§2, 'Accounting').

## 1. Setup and lemmas

Columns live in V = F_3^q after passing to the quotient by the realized subgroup (q = current
codimension). For X ⊆ [m], φ_X(x) = Σ x_i v_i, D(X) = ker φ_X ⊆ F_3^X (dependencies),
R(X) = φ_X({0,1}^X). A piece X **realizes** a subgroup H ⊆ R(X) and **gains** dim H at **cost** |X|.

**Lemma 1 (recursion) [proved; the pass's Lemma 1, re-checked].** If X realizes H and
T ⊆ [m]∖X is nonempty with Σ_T v_i ∈ H, then with S ⊆ X realizing −Σ_T v_i ∈ H, T ∪ S is a
nonempty zero-sum set. Iterating over a chain of realized subgroups H_1 ⊆ V, H̄_2 ⊆ V/H_1, …
until codimension 0 and taking any remaining column solves the instance. ∎

**Lemma G (nested-support gadget; the pass's Theorem 4 with the referee's correction) [proved;
`wnest.py: gadget_symbolic_check`, and checked numerically in the quotient on every piece of
every run].** Let δ, δ′ ∈ D(X) be independent with supp δ = X. For a ∈ {1,2}, b ∈ F_3 let
P_ab = {i : δ_i = a, δ′_i = b}, w_ab = Σ_{P_ab} v_i, h_1 = w_10 + w_11 + w_20,
h_2 = w_11 + w_12 + w_22. Then for every α ∈ F_3²∖0, α_1 h_1 + α_2 h_2 is the sum over the class
union U_α listed in `UNIONS` (e.g. U_(1,2) = X), modulo the two relations w_1• = w_2• and
w_11 + w_21 = w_12 + w_22. Hence either h_1, h_2 are independent and R(X) ⊇ ⟨h_1, h_2⟩ (gain 2),
or some α ≠ 0 has α·h = 0 and a *nonempty* U_α is a zero-sum set.
*Proof.* The eight identities are rank checks in the six symbols w_ab modulo the two relations
(`gadget_symbolic_check` returns True; h_1, h_2 are independent modulo the relations). If
α·h = 0 for α ≠ 0 then also (2α)·h = 0; the two unions U_α, U_{2α} are both empty only if
δ′ = 0, δ′ = 2δ or δ′ = δ on X (cases h_2 = 0, h_1 = 0, h_1 + h_2 = 0 respectively; for
h_1 + 2h_2 = 0 the union is X ≠ ∅), contradicting independence. ∎

**Lemma P (series classes) [proved].** Let F be a set of N nonzero columns spanning a space of
dimension r, with dependency code D = D(F) ⊆ F_3^F, and suppose no coordinate functional
f_i : D → F_3 is zero (no coloop). Call i ~ j if f_i and f_j are proportional (equivalently:
every dependency vanishing at one vanishes at the other; every circuit through one passes
through the other). Let A be a ~-class, a = |A|. Then rank(F∖A) ≤ r − a + 1.
*Proof.* Put U′ = span(F∖A). (i) Pick δ ∈ D with δ_i ≠ 0 for some i ∈ A (i is not a coloop);
by proportionality δ_j ≠ 0 for all j ∈ A, and Σ_{j∈A} δ_j v_j = −Σ_{l∉A} δ_l v_l ∈ U′: the images
of A in span(F)/U′ are dependent with all coefficients nonzero. (ii) If ∅ ≠ B ⊊ A and
Σ_{j∈B} μ_j v_j ∈ U′ with μ ≠ 0, extend to δ′ ∈ D with δ′|_A = μ on B, 0 on A∖B; for i ∈ B with
μ_i ≠ 0 and j ∈ A∖B we get δ′_i ≠ 0 = δ′_j, contradicting f_i ∝ f_j. So every proper subset of
the images is independent, the images span exactly a − 1 dimensions of span(F)/U′, and
r − rank(F∖A) ≥ a − 1. ∎

**Lemma M (second moment) [proved].** Let D ⊆ F_3^N be a linear code with all coordinate
functionals nonzero and proportionality classes of sizes a_1, …, a_c (Σ a_j = N). For δ uniform
in D, E[wt δ] = 2N/3 and Var[wt δ] = (2/9) Σ_j a_j². In particular all a_j ≤ 2 gives
Var ≤ 4N/9. *Proof.* A nonzero functional on D is uniform on F_3, so P(δ_i ≠ 0) = 2/3. For
f_i = λ f_j, P(δ_i ≠ 0 ≠ δ_j) = 2/3, covariance 2/3 − 4/9 = 2/9; for non-proportional f_i, f_j
the pair (δ_i, δ_j) is uniform on F_3² (the map D → F_3² is onto), covariance 0. Sum. ∎
(This is the second Pless power moment: D has dual distance ≥ 3 iff no coloop and no
proportional pair. After peeling, proportional pairs may remain, so D(F*) has only dual distance
≥ 2; the proof uses the statement of Lemma M as written, with a_j ≤ 2, not dual distance ≥ 3.)

**Lemma D (deterministic selection) [proved; `wnest.py: pick_codeword`, asserted on every
piece].** Given a basis B (k × N) of D, a codeword δ with (wt δ − 2N/3)² ≤ Var[wt] can be
computed in poly(N, k) time. *Proof.* Write δ = xB and fix x_1, …, x_j in turn, choosing each
value to minimize Φ(x_1..x_j) = E[(wt − 2N/3)² | x_1..x_j]; since Φ(prefix) is the average of
Φ(prefix, v) over v ∈ F_3, the minimum never exceeds the previous value, and Φ(∅) = Var. Φ is
computable exactly: given the prefix, f_i(x) = c_i + g_i(x_rest) with g_i linear; group the
coordinates by the projective class of g_i; coordinates with g_i = 0 are constants; within a class
all f_i are affine in one uniform scalar t; distinct classes are pairwise independent and
centred (E[1(f_i ≠ 0) − 2/3] = 0), so Φ = (Σ_{g_i=0}(1(c_i≠0) − 2/3))² +
Σ_classes (1/3) Σ_t (Σ_{i∈class}(1(c_i + s_i t ≠ 0) − 2/3))². ∎ The final δ is nonzero since
(0 − 2N/3)² > Var.

## 2. Algorithm WNEST and Theorem A

**Pool size.** For q ≥ 4 let N(q) = min{N ∈ ℕ : N − 1.5q ≥ 3 + √N}. Then
N(q) ≤ 1.5q + 2√q + 6 [proved: N = ⌈1.5q + 2√q + 5⌉ satisfies the inequality because
1.5q + 2√q + 6 ≤ 4q for q ≥ 4 gives √N ≤ 2√q; checked exactly for 4 ≤ q < 3000 in `tables.out`].

**WNEST at codimension q ≥ 4** (ambient V = F_3^q = original space modulo the realized subgroup;
"pool" = the first N(q) not-yet-consumed columns, in input order, mapped to V):
0. If some pool column is 0 in V, it lies in the realized subgroup: finish by Lemma 1.
1. **Peel.** F ← pool. Repeat: compute a basis of D(F); delete every coloop (zero column of the
   basis matrix); if none, compute the proportionality classes of the columns of the basis
   matrix and delete the largest class if its size is ≥ 3; stop when there is no coloop and
   every class has size ≤ 2. Call the result F*, N* = |F*|, r* = rank(F*).
2. **Select.** δ ← the codeword of D(F*) from Lemma D. X ← supp δ.
3. **Gadget.** δ′ ← any basis vector of D(X) independent of δ (exists: dim D(X) ≥ 2, below).
   Apply Lemma G: either realize ⟨h_1, h_2⟩ (dim 2) on X and continue in V/⟨h_1,h_2⟩ with all
   columns except X (the peeled columns and F∖X return to the front of the pool), or output the
   zero-sum union and finish by Lemma 1.
For q ≤ 3 run a KOW round (pool q + 1, any dependency, realize ⟨u⟩ at cost ≤ q + 1).

**Theorem A [proved].** Let n ≥ 4 and m ≥ n²/4 + (8/9)(n+2)^{3/2} + 4n + 2√n + 15. On every
instance v_1..v_m ∈ F_3^n WNEST outputs a nonempty zero-sum subset in deterministic poly(n, m)
time. More precisely, at codimension q ≥ 4 each piece gains 2 dimensions at cost
|X| ≤ 2N(q)/3 + (2/3)√N(q) ≤ q + (8/3)√q + 4, and the exact value `guarantee(n)` of the
recursion (max over stages of consumed + pool) is ≤ the closed form (verified for
4 ≤ n < 3000, and ≤ the analytic sum below for all n).

*Proof.* **Invariant.** Let Δ(F) = |F| − 1.5·rank(F). Deleting a coloop changes Δ by −1 + 1.5 > 0.
Deleting a series class of size a ≥ 3 changes it by −a + 1.5·(rank drop) ≥ −a + 1.5(a−1) ≥ 0 by
Lemma P. Hence Δ(F*) ≥ Δ(pool) ≥ N(q) − 1.5q ≥ 3 + √N(q) ≥ 3 + √N*, i.e.
N* ≥ 1.5 r* + 3 + √N*, so 2N*/3 ≥ r* + 2 + (2/3)√N*. (In particular F* ≠ ∅.)
**Weight window.** By Lemma M with all classes ≤ 2, σ² = Var ≤ 4N*/9, and by Lemma D,
|wt δ − 2N*/3| ≤ σ ≤ (2/3)√N*. So wt δ ≥ 2N*/3 − (2/3)√N* ≥ r* + 2, and
wt δ ≤ 2N*/3 + (2/3)√N* ≤ 2N/3 + (2/3)√N with N = N(q) ≥ N*.
**Gain.** rank(X) ≤ rank(F*) = r*, so dim D(X) = |X| − rank(X) ≥ r* + 2 − r* = 2, and Lemma G
applies: either 2 dimensions are realized at cost |X|, or a zero-sum set is output.
**Cost bound.** With N ≤ 1.5q + 2√q + 6 and q ≥ 4: 2N/3 ≤ q + (4/3)√q + 4 and
(2/3)√N ≤ (2/3)·2√q, so |X| ≤ q + (8/3)√q + 4.
**Accounting.** Columns are consumed only as pieces X_j; everything else returns to the pool, so
the run needs m ≥ Σ_{i<j}|X_i| + N(q_j) at stage j, and m ≥ Σ_j |X_j| + N(n) suffices. Stages
are q = n, n−2, …, down to q ≥ 4, then at most three KOW rounds (cost ≤ 4 + 3 + 2). Using
Σ_{q ≡ n (2), 4 ≤ q ≤ n} q ≤ n²/4 + n/2, Σ √q ≤ (1/2)∫_0^{n+2} √x dx = (n+2)^{3/2}/3 and at
most n/2 stages: Σ_j |X_j| ≤ n²/4 + n/2 + (8/9)(n+2)^{3/2} + 2n + 9, and N(n) ≤ 1.5n + 2√n + 6.
Total ≤ n²/4 + (8/9)(n+2)^{3/2} + 4n + 2√n + 15. **Time.** Each stage is O(1) rank
computations on q × N matrices, O(N²) proportionality checks, 3k evaluations of Φ (each
O(N·k)), and one gadget; at most n/2 + 3 stages; Lemma 1's unwinding is one linear solve per
stage. **Correctness of the witness.** Lemma 1 and Lemma G; `Run.finish` re-sums the output over
the original vectors and asserts zero. ∎

Remarks. (a) **Las Vegas refinement WNEST+** (same guarantee): among the Lemma D codeword and
polynomially many uniform samples of D(F*), take the lightest with weight ≥ r* + 2. On random
instances this is q + 2 exactly (`tables.out`). (b) **Mixing with KOW**: at each stage one may also
compute KOW's sparse dependency (cost w_K for 1 dimension) and take the cheaper per dimension;
on random instances w_K ≈ 2q/3 > q/2, so WNEST wins. [UNPROVED: that the worst-case bound is
the minimum of both. A per-stage greedy mix of two recursions is not shown to be at most the
minimum of the two global bounds (referee, "Remark (b): GAP"); Theorem A does not use it.] (c) The pass's Model A excluded nothing that WNEST does: F is the first N(q) columns (an
oblivious choice), peeling is linear algebra on D(F), and the codeword is chosen by conditional
expectations exactly as KOW derandomize; so the pass's Theorem 6 was false in every reading, as
the referee said, and the referee's NEST needed only Lemmas P, M, D to become worst-case.

## 3. NEST: constant and recursion (average case) and the measured numbers

**Re-derivation.** NEST (referee §3a) at codimension q takes F = the first ≈ 1.5(q+2) + 3
columns, samples D(F), keeps a sample δ with |supp δ| ≥ q + 2 (so dim D(supp δ) ≥ 2), and runs
Lemma G. On uniformly random columns, D(F) has dual distance ≥ 3 with probability 1 − 3^{−Ω(q)}
(a series pair needs F minus two columns to lie in a hyperplane), so by Lemma M the weight of a
uniform codeword is q + 4 ± (2/3)√|F|, and among poly(q) samples the lightest with weight ≥ q+2
has weight q + 2 + O(1) with probability 1 − o(1) [argued from Lemma M; the weight distribution
of a random code is not needed beyond its mean and variance plus the observation that the
window [q+2, q+4] has constant probability by Cantelli's inequality on both sides]. The cost
recursion m(q) = m(q−2) + q + c gives
  **m(n) = n²/4 + O(n)** on random instances, constant exactly 1/4 [proved given the per-piece
cost q + O(1); the per-piece cost itself is sampled: 0 exceptions in all runs].
The referee's 0.2506 n² at n = 120 is 1/4 + 3/(2n) + O(1/n²) with pieces of cost q ± 2.

**Measured [sampled; `wnest.out`, `tables.out`, `adversarial.out`; every witness verified].**

| n | KOW (0.289 n² at n ≥ 90) | WNEST (deterministic) | WNEST+ (Las Vegas, same guarantee) | guarantee(n)/n² |
|---|---|---|---|---|
| 60 | 1037–1045 | 1113–1140 (0.309–0.317) | 935–993 (0.260–0.276) | 0.354 (1275; sharpened KOW-type recursion 1359; KOW (8) 1465) |
| 90 | 2333–2340 | 2425–2430 (0.299–0.300) | 2163 (0.267) | 0.329 (2668; sharpened 2954; KOW (8) 3125) |
| 120 | 4154–4173 | 4185–4187 (0.2906) | 3783 (0.2627) | 0.316 (4552; sharpened 5156; KOW (8) 5405) |
| 150 | 6516–6520 | 6405–6416 (0.285) | 5842–5853 (0.260) | 0.307 (6916; sharpened 7966; KOW (8) 8285) |

Deterministic WNEST pieces cost q + 8..15 at these n (the (2/3)√N slack is paid twice: once
in the pool size, once in the selected weight); WNEST+ pieces cost exactly q + 2.

**Structured families, n = 60 (`adversarial.out`) [sampled].** Chains of length 20, 10, 5
(series classes of those sizes; the invariant held with equality cases), low rank, two
subspaces, duplicated columns, sparse columns, projective columns, signed blocks, block-diagonal
"weight-gap" pools: WNEST used 104–1144 columns, never more than the random instances, and no
per-piece assert fired (wt ≥ r* + 2, wt ≤ 2N/3 + (2/3)√N, Δ(F*) ≥ Δ(F), classes ≤ 2 after
peeling). The largest series class peeled was 20. **Hill climb (n = 8..14, 400 steps from
random and chain starts)** could not push m_used above 40, 55, 75, 95 against bound(n) = 63, 84, 109, 135
(the crude reporting formula `bound()`, labelled "formula" in `adversarial.out`; the exact
`guarantee(n)` is 46, 64, 85, 108, still above 40, 55, 75, 95) and never made the per-piece cost exceed the cap (`adversarial.out`, part B).
**Single-pool hill climb (`pool_climb.out`, q = 8..14, 600 steps from random and duplicated-column
pools)**: the Lemma D weight never exceeded r* + 2 + 5 against the cap r* + 2 + (4/3)√N* ≈ 6–7.3,
and σ stayed ≤ 2.75 ≤ (2/3)√N*. Finite checks falsify only; Theorem A does not rest on them.

## 4. Tightness and the d ≥ 3 frontier

**Two-dimensional pieces [proved].** By Lemma 3 of the pass, a piece gaining d = 2 has
dim K ≥ 2 with K ⊆ D(X), so |X| ≥ rank(X) + 2. On any instance where the pieces used are in
general position (rank(X) = min(|X|, q)), a scheme whose pieces gain ≤ 2 spends
≥ Σ_j (q_j + 2) ≥ n²/4 columns. So 1/4 is the constant of the NEST family; WNEST attains it in
the worst case up to O(n^{3/2}) and WNEST+ up to O(n) on random instances. (Instances with
m = Θ(n²) random columns do contain sets X with |X| < q and dim D(X) ≥ 2 — by counting, of size
≈ q(1 − 2 log 3 / log q) — but finding them is a decoding problem; nothing here finds them.)

**Three dimensions from one piece [exact; `pattern_sat.py`, `pattern_sat_k4.py`, own SAT
encoding, validated against the referee's numbers: 218 feasible / 82 non-trivial sets for
d = k = 2, Theorems 2–4 reproduced].** A d-dimensional realization from a k-dimensional bundle
with pattern set T ⊆ F_3^k∖0 is a map C and local assignments as in the pass's §2; "feasible"
means it exists for every column set with these patterns. Results for d = 3:
- k = 3, all 26 patterns: UNSAT. k = 4, all 80 patterns: UNSAT. With Theorem 3 (rank C ≤ 2
  impossible) this says: **a pattern-complete bundle of dimension k ≤ 4 never gains 3** — the
  generic (r* + k)-set in general position gains at most 2 whatever k ≤ 4 is. (k = 4 with δ_1 of
  full support, 54 patterns: UNSAT, rerun 9 Nov with CaDiCaL and an LRAT proof checked by lrat-check, 839 s
  [the build used then was unsound; all four proofs below were re-verified with the fixed checker, 9 Nov,
  `2026-11-09-lrat-checker-fix/recheck/pattern_proofs.out`];
  k = 4 with δ_1 and δ_2 both of full support, 36 patterns: UNSAT, 1486 s; k = 3 with δ_1 and δ_2 both of
  full support, 12 patterns: UNSAT, 60 s — all in `pattern_sat_k4.out`; the earlier pycosat run of the 54-pattern
  case, stopped after ~30 min with no answer, is kept as `pattern_sat_k4.pycosat_stopped.out`.)
- δ_1 of full support (the NEST precondition; 9 points of PG(2,3) off a line, 18 patterns):
  UNSAT. The nested chain supp δ_3 ⊆ supp δ_2 ⊆ supp δ_1 = X (7 points): UNSAT. Two disjoint
  dependencies inside a full-support one (5 points): UNSAT. Nested pair plus a disjoint third
  (two separate pieces): SAT, as it must be.
- **All negation-closed pattern sets, k = 3 [exact].** PGL(3,3) (5616 collineations) has 29
  orbits on nonempty point sets of PG(2,3); feasibility for d = 3 was decided for each orbit
  representative (patterns = the points and their negatives). Exactly two orbits are feasible
  and non-trivial: the three coordinate points {e_1, e_2, e_3} (three dependencies with
  pairwise disjoint supports: three KOW pieces) and {e_1, e_2, e_3, e_2+e_3} (δ_1 disjoint from
  supp δ_2 ⊇ supp δ_3: a NEST piece plus a KOW piece). Every other point set — in particular
  every connected one, where the three supports cannot be split into blocks with no dependency
  across them — is UNSAT. So **no single connected bundle of three dependencies with
  negation-closed patterns ever gains three dimensions**, whatever the supports do. Caveat:
  pattern sets containing π but not 2π were not enumerated (2^26 sets); such sets are what an
  adversary avoids, not what a selection rule can force, and on general-position instances both
  signs occur.
Interpretation [argued]: the mechanisms available in the worst case (weight selection in a
pool, support nesting) remove *lines* of PG(2,3) from the pattern configuration — one line per
full-support dependency — and the configurations they produce are infeasible for d = 3. Any
piece gaining 3 must have a pattern configuration missing points that no linear-algebraic
selection controls, i.e. must be found by a search over column sets. This is the frontier of the
method, not a barrier for all algorithms; KOW's o(n²) question stays open.

## 5. Computations

All exact over F_3 (numpy int64), interpreter `/opt/anaconda3/bin/python -B`.

| artifact | what | result |
|---|---|---|
| `wnest.py` → `wnest.out` (fixed 9 Nov: WNEST for q ≥ 4, KOW pool q + 1 for q ≤ 3; output unchanged) | WNEST/WNEST+/KOW solver; Lemma G symbolic check; peeling, Lemma D selection with asserts for every per-piece bound; random instances n ≤ 150 | gadget identities True; all asserts hold; table in §3 |
| `tables.py` → `tables.out` | exact `guarantee(n)` recursion vs closed form and KOW's recursion; N(q) bound; WNEST+ on random instances | closed form holds 4 ≤ n < 3000; WNEST < the note's sharpened KOW-type recursion for all n ≥ 35 (KOW's recursion (8): all n ≥ 9, referee); WNEST+ 0.26 n² at n = 150 |
| `adversarial.py` → `adversarial.out` | 11 structured families at n = 60 (chains with series classes 5–20, low rank, subspaces, duplicates, sparse, projective, signed blocks, block-diagonal); hill climb n = 8..14 | no assert fired; m_used ≤ random case; hill climb far below the guarantee |
| `pattern_sat.py` → `pattern_sat.out` | own SAT encoding; d = 2 validation; d = 3 for k = 3 natural sets; PGL(3,3) orbits of point sets | 218/82 reproduced; all d = 3 natural sets UNSAT; orbit table |
| `pattern_sat_k4.py` → `pattern_sat_k4.out` | d = 3 from k = 4 bundles (CaDiCaL + LRAT proof checked since 9 Nov; `pattern_sat.py` gained a `solver='cadical'` option) | all 80 patterns UNSAT (150 s); 54 patterns (δ_1 full support) UNSAT (839 s); 36 patterns (δ_1, δ_2 full support) UNSAT (1486 s); k = 3, 12 patterns UNSAT (60 s); every UNSAT LRAT-verified (re-verified with the fixed checker, 9 Nov: `2026-11-09-lrat-checker-fix/recheck/pattern_proofs.out`) |
| `pool_climb.py` → `pool_climb.out` | hill climb over single pools maximizing the selected weight after peeling | max wt − (r*+2) = 4, 4, 5, 5 at q = 8, 10, 12, 14; no assert fired |

## 6. Claim gates, next question, next command

Gates that must stay false:
- "Theorem A is new / has priority." Not checked beyond the local literature summary (KOW
  Theorem 1.2 at 1/3 and KOW Theorem 1.11 at 3^9(n+1)² are the worst-case results it lists;
  KOMSW's 0.1022 n² is average-case and unverified). Human review and a literature search are
  required before any external statement.
- "o(n²) or any c < 1/4 is obtained in the worst case." No. §4 says why the NEST family stops
  at 1/4 and what a 3-dimensional piece would need.
- "The O(n^{3/2}) term is O(n log n)." Not shown; the window argument is Θ(√N) wide.
- "Average-case 1/4 is optimal." KOMSW claim 0.1022 on average; irrelevant to Theorem A.
- Finite computations (n ≤ 150, SAT for k ≤ 4) are not scaling evidence for anything beyond
  what they state.

Next hard question. Is there a polynomial-time rule that, in every pool of poly(q) columns in
F_3^q, finds a set X with dim D(X) ≥ 3 whose pattern configuration in PG(2,3) is one of the
feasible d = 3 sets of `pattern_sat.out`, at cost |X| ≤ (3/2 − ε)q? A positive answer gives
c < 1/4 in the worst case by Lemma 1; the SAT table says which configurations qualify, and all
of them miss points that support nesting does not remove. Secondary: reduce Theorem A's
lower-order term to O(n log n) by replacing the one-sided window with KOW-style enumeration of
the heaviest codewords in a small quotient.

Next command. `cd research/audits/reviews/2026-11-08-rees-sde-p3-nest && /opt/anaconda3/bin/python -B adversarial.py`
extended with a hill climb over *single pools* at q ∈ {8..14} that maximizes the Lemma D weight
minus (r* + 2) after peeling; expected artifact `pool_climb.out`; acceptance: the maximum stays
≤ (4/3)√N* (it must, by Lemmas M and D) and the realized per-piece cost stays ≤ q + (8/3)√q + 4;
any violation refutes Theorem A and must be recorded first.

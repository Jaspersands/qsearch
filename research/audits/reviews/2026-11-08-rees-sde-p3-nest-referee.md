# Referee: proof of Theorem A in `2026-11-08-rees-sde-p3-nest.md` (worst-case F_3^n subset sum at n²/4 + O(n^{3/2}))

This is an AI-only adversarial referee pass from 8 November 2026. No human has reviewed it.
Novelty and priority were not assessed. I re-derived every step by hand. The computations use my
own code in `2026-11-08-rees-sde-p3-nest-referee/`, independent of the note's `wnest.py`; the
only exception is that the union table from Theorem 4 was imported so that it could be
re-derived and checked. Interpreter: `/opt/anaconda3/bin/python -B`. Only this file and that
folder were written. No git, no network, and `make_numbers.py` was not run.

## Verdict

**Theorem A's proof: CONFIRMED.** I found no gap in the chain from the gadget through Lemmas P,
M and D, the window, the accounting and the closed form. Corrections are needed only in three
places: the descriptive claims about dual distance, the KOW comparison, and one remark that the
theorem does not use.

| step | verdict |
|---|---|
| Lemma G (Theorem 4 gadget, nested supports) | CONFIRMED |
| Lemma P (series-class rank drop; Δ = \|F\| − 1.5 rank is monotone) | CONFIRMED (the drop is in fact exactly a − 1) |
| "peeling reaches dual distance ≥ 3" (§0 items 1 and 4, the Lemma M parenthetical) | CONFIRMED WITH CORRECTION |
| Lemma M (mean 2N*/3, Var = (2/9) Σ a_j²) | CONFIRMED (the §1 statement is right; the dual-distance gloss is wrong, see above) |
| Lemma D (conditional expectations) | CONFIRMED |
| Window [r*+2, 2N/3 + (2/3)√N]: achievable and sufficient | CONFIRMED |
| Accounting, back substitution at P = {1}, recursion, closed form | CONFIRMED |
| "Exact recursion beats KOW's for 35 ≤ n < 3000" | CONFIRMED WITH CORRECTION |
| Remark (b) ("worst-case bound is the minimum of both") | GAP (not used by Theorem A) |

## Step-by-step

**Lemma G: CONFIRMED.**
- *The two relations.* The dependency δ gives w_1• − w_2• = 0. The dependency δ′ gives
  (w_11 + w_21) − (w_12 + w_22) = 0. Both are exactly the span of the class-indicator rows of δ
  and δ′.
- *Union identities.* Over all 2^6 class unions I searched for every union U with
  1_U ≡ α_1 h_1 + α_2 h_2 modulo these relations. The note's union for each of the eight α is
  among the solutions. Each solution is unique, except α = (2,1), which also admits
  P_10 ∪ P_11 ∪ P_12.
- *Independence.* h_1 and h_2 are independent modulo the relations.
- *Emptiness cases.* I enumerated all 54 nonempty-class patterns with δ′ ∉ ⟨δ⟩. For every α ≠ 0,
  at least one of U_α and U_{2α} is nonempty, with 0 exceptions. The referee's count of 16
  patterns that empty some listed union is reproduced.
- *Consequence.* So α·h = 0 always yields a nonempty set whose sum is zero in V, that is, a sum
  lying in the realized subgroup W. Lemma 1 then applies.
- *Numeric check.* The identities also hold numerically on 300 random nested pairs
  (`lemmas.out`).

**Lemma P: CONFIRMED.**
- *Terminology.* "Series class" is used correctly. With no coloops, i ~ j means f_i ∝ f_j on D,
  which means ker f_i = ker f_j, which means every circuit through i passes through j. These are
  the parallel classes of the dual matroid.
- *Proof.* Step (i) shows the images of A in span(F)/span(F∖A) are dependent with full support.
  Step (ii) shows that every proper subset of them is independent. So the images form a circuit,
  and the rank drop is **exactly** a − 1.
- *Exhaustive check.* On 20 562 classes (random, low-rank and planted-chain matrices, class
  sizes up to 7), every drop equals a − 1.
- *Δ is monotone.* Deleting a coloop changes Δ by −1 + 1.5 > 0. Deleting a class of size a ≥ 3
  changes it by −a + 1.5(a − 1) ≥ 0. Classes of size 2 are kept, correctly, since deleting one
  would cost 0.5.
- *Termination and nonemptiness.* Peeling terminates, and F* ≠ ∅ because Δ(∅) = 0 < 3 + √N.

**Correction: dual distance.** Peeling stops when there is no coloop and every class has size
≤ 2. Proportional pairs survive, so D(F*)^⊥ can contain words of weight 2: the dual distance is
≥ 2, not ≥ 3.
- My runs hit this case. On the `dup_blocks` family, all classes have size 2 and
  9 Var/(2N*) = 2.000, so Var = 4N*/9 is attained (`dualdist_ref.out`).
- Under true dual distance ≥ 3, the variance would be exactly 2N*/9.
- Corrected statement: "after peeling, D(F*) has no coloop and its proportionality classes have
  size ≤ 2; hence Var ≤ 4N*/9 (tight)."
- The proof of Theorem A uses only this corrected statement, so the theorem is unaffected.

**Lemma M: CONFIRMED.**
- *Derivation.* E[wt] = 2N/3 because each nonzero functional is uniform on F_3. Each diagonal
  covariance term is 2/9. Proportional pairs have identical indicators, so their covariance is
  2/9. Non-proportional pairs are jointly uniform on F_3², so their covariance is 0. Summing,
  Var = (2/9) Σ a_j², and a_j ≤ 2 gives Var ≤ 4N/9.
- *Exact check.* Enumerating every codeword of 432 coloop-free codes, including some with planted
  proportional columns, matches both the mean and the variance formula.

**Lemma D: CONFIRMED.**
- *Exactness of Φ.* The class decomposition of Φ is exact. Constants contribute a squared sum.
  Nonzero g_i in distinct projective classes are pairwise independent and centred, so their cross
  terms vanish. Within a class every f_i is affine in one uniform scalar.
- *Exact check.* My integer form of 27Φ equals the brute-force conditional expectation at every
  prefix of 208 codes. The greedy codeword satisfies (3 wt − 2N)² ≤ 9 Var and is nonzero.

**Window: CONFIRMED (achievable and sufficient).**
- *Achievable.* Δ(F*) ≥ Δ(pool) ≥ N(q) − 1.5q ≥ 3 + √N(q) ≥ 3 + √N*. This gives
  2N*/3 − (2/3)√N* ≥ r* + 2, and Lemma D gives |wt − 2N*/3| ≤ σ ≤ (2/3)√N*. So
  wt ≥ r* + 2 holds deterministically.
- *Sufficient.* X = supp δ has rank(X) ≤ r*, so dim D(X) ≥ 2. Every δ′ ∈ D(X)∖⟨δ⟩ satisfies
  supp δ′ ⊆ X = supp δ, so the pair is nested and δ has full support on X. That is exactly
  Lemma G's hypothesis.
- *Upper bound.* The upper end follows from N* ≤ N(q) and monotonicity.
- *Pool size.* For N(q): ⌈1.5q + 2√q + 5⌉ satisfies the defining inequality, using √N ≤ 2√q for
  q ≥ 4 (equality case 2.5q = 2√q + 6 at q = 4). N(q) ≤ 1.5q + 2√q + 6 and N(q) is nondecreasing;
  both were checked for q < 20 000.

**Accounting and back substitution: CONFIRMED.**
- *Disjoint pieces.* Columns leave the pool only as X (or as a KOW support), so the pieces are
  disjoint.
- *Pool requirement.* Stage j needs Σ_{i<j}|X_i| + N(q_j) columns. Since N(q) is monotone, the
  maximum over stages plus the one final column is ≤ Σ|X_j| + N(n).
- *Back substitution.* At p = 3 there is no scaling freedom, and none is needed. Each stage
  stores an explicit 0/1 subset for **each of the 9** (or 3, for KOW) elements of its realized
  subgroup in V_j = F_3^n / W_{j−1}.
  - Given t ∈ W_k, at stage j look up the subset for −t̄ ∈ G_j and add its original sum.
  - Then t ∈ W_{j−1}, and the process ends at 0.
  - Degenerate exits (a zero column, a zero gadget union, or KOW with u = 0) produce a nonempty
    T with Σ_T ∈ W, and the same unwinding applies.
- *Sums.* Σ q ≤ n²/4 + n/2, Σ √q ≤ (n+2)^{3/2}/3, there are ≤ n/2 stages, and the KOW tail
  costs ≤ 9. Each was checked for n < 5000. These give exactly
  n²/4 + (8/9)(n+2)^{3/2} + 4n + 2√n + 15.
- *Closed form.* My exact `guarantee(n)` never exceeds the bound for 4 ≤ n < 3000. It even stays
  ≥ 28 below the stronger form with "4n + 12" that the note's `tables.py` actually checks. That
  is a harmless mismatch between the script and the statement.

**KOW comparison: CONFIRMED WITH CORRECTION.**
- *Which recursion.* The note's `kow_recursion` is **not** KOW's recursion (8). It is the note's
  own sharpened version, with weight ≈ 2(l+r)/3 · 3^r/(3^r − 1). KOW's (8), read from the local
  text `2026-11-02-rees-linear-arity/lit/arxiv_2510.07515.txt` around line 473, is
  m_l = max{l, m_{l−1} + 2(l+1)/3 + ⌈log₃(l+1)⌉}.
- *Exact recursion versus each KOW recursion* (`recursion_ref.out`):

| compared against | WNEST guarantee(n) is smaller for |
|---|---|
| the note's version | all 35 ≤ n < 3000 (claim reproduced) |
| KOW (8) literally | all 9 ≤ n < 3000 |
| KOW (8) with integer pieces | all 15 ≤ n < 3000 |

- *Closed forms.* Theorem A's stated closed form is below KOW's closed form
  ((n+1)(n+2)+1)/3 + n⌈log₃(n+1)⌉ only for n > 80, and below (8) only for n > 105.
- *Corrected statement.* The exact WNEST recursion is below KOW's recursion (8) for 9 ≤ n < 3000
  (and below the note's sharpened version for 35 ≤ n < 3000). The explicit bound of Theorem A
  improves on KOW's explicit bound only for n > 80.

**Remark (b): GAP.** Choosing the cheaper option per stage is a greedy mix of two recursions. It
is not shown to be at most the minimum of the two global bounds. Theorem A does not use this
remark.

## Implementation and adversarial runs [sampled; finite checks falsify only]

`wnest_ref.py` is a minimal WNEST written from §2. It covers:
- the pool as the first N(q) unconsumed columns;
- peeling, with Lemma P and Δ-monotonicity asserted;
- the Lemma D greedy selection, with the exact window asserted;
- the gadget, with all eight identities asserted in the quotient;
- KOW tail rounds;
- explicit back substitution, with the witness re-summed over the original vectors.

`adversarial_ref.py` makes **532 runs at m = ⌈Theorem A bound⌉ exactly**, for
n ∈ {4, 5, 8, 12, 20, 30, 40}, over 19 families:
- random;
- 5 distinct vectors repeated;
- consecutive duplicates;
- ± pairs;
- circuits of length 3, 5 and 9 in coordinate blocks;
- 90% in an n/3-dimensional subspace;
- a flag of subspaces;
- coloop-heavy (basis vectors plus a low-rank bank);
- weight-1 and weight-2 vectors;
- block-diagonal blocks of size 2 and 4, where every dependency is block-local;
- PG(2,3) points;
- simplex-code columns;
- planted series classes of size 3, 4 and 7, peeled as designed.

Results:
- No assertion fired, and there was no pool shortfall.
- Every witness is nonempty, has distinct indices and sums to 0.
- Columns pulled never exceeded guarantee(n) (at most 552 against 621 at n = 40).
- The largest per-piece wt − q was 8, against the cap (8/3)√q + 4.
- Hill climbs over whole instances (`hillclimb_ref.out`, n = 6–10, 1500 steps each) reached at
  most 26, 33, 40 and 56 columns pulled, against guarantees of 30, 36, 46 and 64.

## Gates that stay false

- Novelty or priority of Theorem A.
- Any worst-case constant c < 1/4.
- A lower-order term of O(n log n).
- "Theorem A's explicit bound beats KOW's explicit bound for all n ≥ 35". That holds only for
  n > 80.

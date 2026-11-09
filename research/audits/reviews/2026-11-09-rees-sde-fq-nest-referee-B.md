# Referee B: Theorem B of `2026-11-08-rees-sde-fq-nest.md` (p = 5, κ = 2, worst case n²/4 + O(n^{3/2}))

AI-only adversarial referee pass, 9 November 2026, one Claude Code session; not human-reviewed; no
novelty or priority assessment. Scope: §0, §1 (setup, Lemmas 1, 2, R, Q, U) and §3 (Fact F5,
Lemma J, Lemmas P/M/D, WNEST₅, Theorem B, guarantee(n)) of the target note. Context read:
`2026-11-08-rees-sde-p3-nest.md` (template), its referee and break notes, `research/STATE.md`
("Now"). All computations are my own scripts in `2026-11-09-rees-sde-fq-nest-referee-B/`
(interpreter `/opt/anaconda3/bin/python -B`, pycosat 0.6.6); the note's code was only *run* (its
WNEST₅ and its `solve4`, as attack targets), never edited. Only this file and that folder were
written. No git, no network.

## Verdict

**ACCEPT WITH FIXES.** Theorem B is proved as stated, given Fact F5, and I re-verified Fact F5
independently (orbit enumeration, Burnside count, and a different CNF whose every model was
re-checked by plain arithmetic, plus an end-to-end run on real column sets for every orbit).
No fatal finding. Two material findings:

- **M1 (strengthening; changes the headline).** Fact F5 covers *every* spanning label set, so the
  peeling, Lemma D window and Lemma J are unnecessary at p = 5. Taking the first q + 2 pool columns
  and *any* two independent dependencies already gains two dimensions or yields a witness. That
  gives a deterministic worst-case bound of **n²/4 + 3n/2 + 2** columns (exact recursion
  ≤ n²/4 + 3n/2 + 1.25), not n²/4 + O(n^{3/2}). The gate "Theorem B's O(n^{3/2}) is O(n log n) (not
  shown)" is too cautious: O(n) follows from the note's own Fact F5.
- **M2 (outside Theorem B, inside §1).** Lemma Q's reduction to one label per P-class is proved only
  in the SAT direction. The direction every UNSAT verdict needs (a weakly nondegenerate solution on
  L gives a P-consistent one) is not proved. That direction is used by all `gadget_cnf4/5` UNSAT
  results (p = 7, 11, 13, the §2 table, and Lemma U case splits). See finding 2 for what my test
  found.

## Findings

1. **[material, §0 item 1 / §3 / §7 gate] Theorem B's error term is O(n), by the note's own
   inputs.**
   - *Construction (SIMPLE5).* At codimension q ≥ 2, take the first q + 2 unused columns. Their
     images in V = F_5^q have rank ≤ q, so dim D ≥ 2. Take any independent δ, δ′ and labels
     ℓ_i = (δ_i, δ′_i). Columns with ℓ_i = 0 get weight 0 and go back to the pool. The nonzero
     labels span F_5² (since δ, δ′ are independent), so Fact F5 supplies (Φ, γ).
   - *Gain or witness.* Lemma 2(A)'s proof applies verbatim: Σ⟨γ_α, ℓ_i⟩v_i = 0 because
     γ_α·(δ, δ′) is a dependency. So the piece gains ⟨h₁, h₂⟩ at cost ≤ q + 2, or yields a witness.
   - *Tail.* q = 1 costs 2 columns: any two nonzero u, v = cu realize the whole line, since
     {a + bc : a, b ∈ {0, ±1}} = F_5 for every c ≠ 0. Then one closing column.
   - *Bound.* guarantee_simple(n) = Σ_{q = n, n−2, …, ≥ 2}(q + 2) [+ 2 if n is odd] + 1 ≤
     n²/4 + 3n/2 + 5/4.
   - *No extra machinery.* Lemma D, the peeling, Lemma J and the "+3" are not needed. The note half
     says this ("any δ′ ∈ D(X) independent of δ serves, and dim D(X) ≥ 2 suffices") but does not
     draw the consequence. Its full-support X and N(q) ≈ 5q/4 + √(2q) are what produce the n^{3/2}.
   - *Implemented and tested.* `simple5.py`, `attack_ref.out`: 8 families, n ≤ 40, at m =
     guarantee_simple(n) exactly, plus hill climbs that reach m − 1 or m − 2 consumed. Every witness
     re-summed, no failure.
   - *Against KOW.* KOW Thm 3.7 at q = 5 (best r) is 405 046 at n = 1000; SIMPLE5 needs 251 501 and
     Theorem B's guarantee 271 321. SIMPLE5 is below KOW Thm 3.7 for every 3 ≤ n ≤ 5000
     (`accounting_ref.out`).
   - *Fixes.* Restate Theorem B as m ≥ n²/4 + 3n/2 + 2. Rewrite the §7 gate. Optionally keep WNEST₅
     as the template that generalizes where only nested label sets are feasible (as at p = 3).

2. **[material, §1 Lemma Q; affects §2/§4 UNSAT verdicts, not Theorem B] Lemma Q's reduction is
   proved only in the SAT direction.**
   - *What is proved.* A P-consistent solution (Φ(λℓ) = λΦ(ℓ)) is a solution on L. This is the SAT
     direction, and it is all that WNEST₅ uses (`solve4` models are re-verified on L).
   - *What is not.* The converse: a feasible, weakly nondegenerate (Φ, γ) on a P-closed L yields a
     P-consistent one. Re-basing each label class at one chosen element keeps feasibility. But weak
     nondegeneracy is per direction, and one global choice of base element per class must serve all
     p + 1 directions. If direction D is nonzero only at λℓ and direction D′ only at ℓ (same class,
     no other class nonzero), no choice works.
   - *The note's argument.* "Weak nondegeneracy is unchanged" holds only for the extension of a
     solution from representatives, not for the restriction.
   - *Where it is used.* `solve4`/`solve5` impose P-consistency (the comment says "feasibility of L
     equals that of its P-closure (Lemma Q)"), so every UNSAT verdict from them rests on the
     unproved direction.
   - *Computational test (`q_check.out`, `q_check2.out`).* I found no counterexample, and the test is weak on the side that matters.
     - At p = 5 the note's `solve4` is SAT on all 36 090 spanning orbits, so the WNEST₅ code path never hits "no gadget".
     - At p = 7 (κ = 2 and 3), on 396 random label sets with a propagation limit: 289 were SAT for both solvers and 5 UNSAT for both; there were 0 disagreements where both decided.
     - But 86 sets that the reduced CNF called UNSAT were left undecided by the unreduced CNF. So the UNSAT direction is essentially untested at the sizes where it matters.
     - The unbounded run (`q_check.py` part 2) stalled on hard unreduced UNSAT instances and was stopped after about 25 minutes. `q_check.out` therefore contains only part 1.
   - *Fixes.* Either prove the converse, or re-decide the p ≥ 7 cells without the label reduction
     (Lemma R alone is fine; see finding 3). Until then, the p = 7, 11, 13 "no two-dimensional
     gadget" verdicts are conditional on Lemma Q completeness.

3. **[minor, §1 Lemma R] The proof checks nonzero-ness per α, but weak nondegeneracy is per
   direction.**
   - *Gap.* If the only nonzero realizer of a direction sits at a non-representative multiple μα,
     then γ′_{λα} := λγ_α (λ ∈ P) can make that direction degenerate.
   - *Repair.* Re-base each (direction, coset) slot at a nonzero member μα: set
     y′_{νμα} := ν y_{μα}. This is a valid family, since y_{μα} ≡ ⟨μα, y_e⟩ modulo the row space.
     The CNF's free γ-slot for that coset can represent it, and for coset 0 of a unit direction
     one re-normalizes Φ_j := μ^{-1}y_{μe_j}.
   - *Conclusion.* Unlike Q, the choice is per slot, so it never conflicts. Lemma R stands with
     this proof.

4. **[minor, §1 Lemma 2(B)] The witness construction breaks the normalization used by the CNFs.**
   - *Issue.* With Φ₁ = y, Φ₂ = 0, γ_α = (1−α₁)μ, one gets γ_{e₂} = μ ≠ 0. That contradicts the
     normalization "γ = 0 at unit directions, Φ_j := y_{e_j}" used by the CNFs.
   - *Fix.* Use Φ₁ = Φ₂ = y and γ_α = (1−α₁−α₂)μ. Then y_α = y for every α.

5. **[minor, §1 Lemma U] Proof checked by hand; correct.**
   - *Argument.* With Φ₁ = y_{e₁} ∈ S and r ∉ P, rS ∩ S = {0} forces Φ₁ ≡ 0. A nonzero functional
     on F_p^*×F_p takes a non-S value (|S| < p). So all realizers of [(1,0)] vanish,
     contradicting weak nondegeneracy.
   - *Not checked.* The 3p − 2 case cover (`cases_cover.out`) is computational, concerns p ≥ 7
     only, and was not re-run.

6. **[minor, §3 N(q) bound] The note's argument proves a weaker constant than it states.**
   - *Issue.* The text proves N(q) ≤ 5q/4 + √(2q) + 7 "with N = ⌈5q/4 + √(2q) + 7⌉", which only
     gives + 8.
   - *Fix.* N₀ = ⌈5q/4 + √(2q) + 6⌉ is feasible for all q ≥ 1, because
     (√(2q) + 9/4)² ≥ 5q/4 + √(2q) + 7 ⟸ 3q/4 + 3.5√(2q) ≥ 31/16. Checked for q < 10⁵.
   - *Consequence.* The cost cap q + (8/5)√(2q) + 8 then follows, also checked for q < 10⁵.

7. **[minor, §3 Theorem B "deterministic"] `choose_second` falls back to random combinations.**
   - *Issue.* The proof only shows that δ′ exists.
   - *Fix.* At p = 5 take any independent δ′ (Fact F5). In general, derandomize the avoidance of
     ≤ 3 hyperplanes (for example scan b + c·b′ over basis pairs).

8. **[minor, §3 Lemma J] The proof is correct and holds for every p ≥ 3, not only p ≥ 5.**
   - *Why.* t proper hyperplanes cannot cover F_p^k unless t ≥ p + 1. Here t ≤ 3, so the
     condition t < p is sufficient but not needed.
   - *Check.* Exhaustive at p = 3 (k = 2 all sets; k = 3 up to 6 labels) and over all p = 5, k = 2
     orbits, plus samples at (5, 3), (7, 2), (7, 3): 0 failures in 1.17 M (L, δ) pairs
     (`lemma_j_ref.out`).
   - *Relevance.* Lemma J is not needed at p = 5 (finding 1).

9. **[minor, §3 "Measured" / §0 item 1] The adversarial evidence is weaker than described.**
   - *chain3/chain4.* Described as "series classes of size 3 and 4, which are not peeled". In
     `adversarial_p5.py` they are proportional columns (v, 2v, 3v, …): parallel classes of the
     column matroid. Those runs end with an immediate witness (38 columns).
   - *Trivial runs.* `dup`, `sparse` and `signed_blocks` consumed 0 columns.
   - *My series families.* True series classes (circuits in private coordinates, hidden by a random
     GL_n), of sizes 4, 6 and 7, ran in `attack_ref.out` with no failure.

10. **[minor, §0/§3 provenance] Two output files have no generating script.**
    - *Missing.* `closed_form_p5.out` and `guarantee_p5.out` (the 0.754 closed form, "q < 5000")
      are not produced by any script in the folder.
    - *Mismatch.* `tables_p5.py` prints a different, weaker closed form (n²/4 + 2n^{3/2} + 12n + 40,
      q < 3000), which is what `tables_p5.out` shows.
    - *Status.* I reproduced the stated closed form independently (finding 11).

11. **[minor, §0/§5 KOW comparison] "Halves KOW's 0.4 to 0.25" is a leading-constant statement.**
    - *Explicit bounds.* Theorem B's closed form is below KOW Thm 3.7's explicit bound (q = 5, best
      r) only for n ≥ 59. Its exact recursion guarantee(n) is below it only for n ≥ 18 (same
      against Remark 3.8: n ≥ 60 and n ≥ 19).
    - *Comparison table.* n = 60: 1340 (guarantee) / 1637 (closed form) / 1647 (KOW 3.7) /
      991 (SIMPLE5).
    - *Citation check (local text
      `2026-11-02-rees-linear-arity/lit/arxiv_2510.07515.txt`, l. 625–671).* KOW Thm 3.7: q > 3
      prime, deterministic, worst case, m ≥ ((1−q^{−1})/(1−q^{−r}))·n(n+1)/2 + r(n+1) gives a
      nontrivial (±⌊q/4⌋)-zero-sum. At q = 5, ⌊q/4⌋ = 1 and the coefficient set is {0, ±1} = S, so
      the leading constant (1−1/5)/2 = 0.4 is cited correctly. Remark 3.8 gives the
      O(n log n) form the note quotes.
    - *Terminology.* This is KOW's (±1)-zero-sum (SIS∞-type) problem, not "subset sum" in the 0/1
      sense.

12. **[confirmed] Every other step of Theorem B.**
    - *Lemma P over F_p.* Exact rank drop a − 1. The coordinate functionals of a class share one
      kernel hyperplane, so dim D drops by exactly 1.
    - *Δ invariant.* Δ = |F| − (5/4)rank: a coloop changes it by +1/4; a class a ≥ 5 by (a − 5)/4 ≥ 0.
    - *Lemma M.* Mean (4/5)N. Variance (4/25)Σa_j² ≤ (16/25)N with classes ≤ 4. Non-proportional
      pairs are jointly uniform; proportional pairs are nonzero together.
    - *Lemma D.* The class decomposition of Φ is exact, since each class sum is centred and
      different classes are pairwise independent. δ ≠ 0 since μ > σ.
    - *Window.* wt ≥ r* + 3, so dim D(X) ≥ 3.
    - *Step 3 exits.* Constant δ means X sums to zero. c = k means each class sums to zero.
    - *Lemma 1 unwinding.* Disjoint pieces; every element of each H_j is realized modulo W_{j−1}.
    - *Accounting.* Σq ≤ n²/4 + n/2, Σ√q ≤ (n+2)^{3/2}/3, ≤ n/2 stages, tail 6, first pool N(n).
      Total n²/4 + (8√2/15)(n+2)^{3/2} + 5.75n + √(2n) + 13, with 8√2/15 = 0.75425 ≤ 0.754 +
      rounding slack. My exact recursion equals the code's `guarantee` (n < 400 and
      n = 600, 1000, 3000) and stays ≥ 29.4 below the closed form for 3 ≤ n ≤ 5000.
    - *Worst case.* No general-position assumption enters. Fact F5 covers degenerate label sets
      (|L′| = 2, 3; labels with a zero coordinate), multiplicities are irrelevant to Lemma 2(A),
      zero columns exit at step 0, and the 1-d tail is exact.

## Re-verified computationally (`2026-11-09-rees-sde-fq-nest-referee-B/`)

| script → output | what | result |
|---|---|---|
| `orbits_f5.py` → `orbits_f5.out` | all 480 matrices of GL_2(F_5) enumerated directly; canonical form of every one of the 2^24 subsets; Burnside/cycle-index count; Σ 480/\|Stab\| = 2^24 | 36 096 orbits, per-size counts equal Burnside's and the note's; 36 090 spanning (non-spanning: sizes 0,1,2,2,3,4) |
| `f5_feas.py` → `f5_feas.out` | Fact F5 by a new CNF from Lemma 2(A) only (all 24 α, no Lemma R/Q, no normalization, Φ ∈ F_5² unrestricted, a sound relaxation); every model re-checked arithmetically | 36 090 / 36 090 spanning orbits feasible with weak nondegeneracy; 0 unverified (546 s) |
| `e2e_orbits.py` → `e2e_orbits.out` | for each orbit (\|L\| ≥ 3), real columns in F_5^{c−2} with that dependency space (with and without duplicated labels, random GL change of coordinates, random order), solver picks its own basis; all 24 realizers summed; gain-2 independence or witness checked | 36 089 orbits × 2 column sets (the size-2 orbit is the trivial zero-column case): every run gain-2 (h independent) or a re-summed witness; 0 failures (1328 s). E.g. \|L\| = 12: 11 524 gain-2, 12 witness |
| `lemma_j_ref.py` → `lemma_j_ref.out` | Lemma J exhaustive p = 5, k = 2 (orbits) and p = 3; sampled (5,3), (7,2), (7,3) | 0 failures |
| `accounting_ref.py` → `accounting_ref.out` | N(q), cost cap, guarantee(n) in integer arithmetic; closed form; KOW 3.7 / 3.8; SIMPLE5 | as in findings 6, 11, 12 |
| `simple5.py` | SIMPLE5 (finding 1), own quotient/back-substitution, own gadget CNF | used below |
| `attack_ref.py` → `attack_ref.out` | note's WNEST₅ at m = guarantee(n) and SIMPLE5 at its guarantee: 8 families (true series classes 4/6/7, PG(2,5) blocks, dependency triples, mixed, weight-2, random), n = 6..40, 3 each; hill climbs | no failure, every witness re-summed; WNEST₅ first-piece excess climbed to cap − 2/−2/−3 (q = 5, 8, 12); SIMPLE5 climbs reach m − 1 or m − 2 consumed (n = 6..12; its recursion is essentially tight) |
| `q_check.py` → `q_check.out` | Lemma Q completeness: note's `solve4` over all p = 5 orbits; reduced vs unreduced at p = 7 (κ = 2, 3) on random sets | p = 5: `solve4` SAT on 36 090 / 36 090 orbits. p = 7 (bounded, `q_check2.py`): 0 disagreements among 294 decided pairs; 86 reduced-UNSAT / unreduced-unknown (inconclusive) |

Attack (obligation 5): no column set on which WNEST₅ fails at guarantee(n) was found. Since
Fact F5 is now independently certified, a failure would need a bug in the note's code, not in
the proof.

## Exact claim I consider proved

For p = 5, S = {0, ±1} (κ = 2; equivalently KOW's (±1)-zero-sum over F_5), and every n ≥ 1 and
every (adversarial) λ_1, …, λ_m ∈ F_5^n with **m ≥ n²/4 + 3n/2 + 2**, a nonzero x ∈ S^m with
Σ x_iλ_i = 0 is found in deterministic poly(n, m) time. The only finite input is Fact F5, a table
of 36 090 certified gadgets up to GL_2(F_5), each checkable by arithmetic. Theorem B as stated
(m ≥ n²/4 + 0.754(n+2)^{3/2} + 5.75n + √(2n) + 13, via WNEST₅) is also proved, with fixes 3, 4, 6
and 7.

Gates that stay false:
- novelty or priority;
- a constant below 1/4 at p = 5 (the framework's floor q + 2 per two dimensions);
- any statement that the p ≥ 7 obstruction holds without Lemma Q completeness (finding 2);
- "Theorem B's explicit bound beats KOW's explicit bound for all n" (only for n ≥ 59; SIMPLE5 for
  all tested n ≥ 3).

Next question: do the k = 3, d = 3 label sets at p = 5 admit the same "every spanning set" property?
That would give n²/6 + O(n) by the same argument; `big_5_d3_*` in the note's folder is the place to
start, decided without the Lemma Q reduction.

# Referee: free23 aligned-triples merge (§9 of the 11-13 pair-measurement report) (2026-11-13)

**Status: AI-checked, pending human review.** One hostile AI referee (Claude). Target:
`2026-11-13-rees-free23-pair-measurement.md`, mainly §9, and its scripts `aligned_triples.py` and `end_to_end.py`.
Checked against `2026-11-12-rees-entangled-twist-impossibility.md`. The referee's own code and outputs are in
`2026-11-13-rees-free23-triples-referee/`. That code was written from the definitions and does not import the audited
scripts. No other file was edited. Finite checks can only falsify (TRAPS 7).

## Verdict: SOUND CANDIDATE

No flaw was found. The procedure works when the quantum states are simulated from the group itself, not only from
the closed form. It is consistent with the impossibility note, because it lies outside SOT(Aut). Nothing in it leaks
H. Item (c) of the target reduces to item (b), and (b) is now PROVED for every configuration sampled at p = 30011.

The remaining gaps are these:

* **G1 (b) in general: CONDITIONAL.**
  * The level-2 weight variety C is a complete intersection of type (3,3,2,2) in P⁵. It has degree 36 and arithmetic
    genus 73.
  * It is smooth in 6/6 random configurations at p = 10007 and at p = 30011. At p = 101, 2/6 are smooth and the
    others have finitely many singular points.
  * Smooth implies geometrically irreducible. By the Weil bound, a torus point exists once p ≥ 21,751.
  * Missing: a written proof that the family is smooth for generic labels over Z, with an effective bound on the
    bad-label probability (§4.2).
* **G2 (c): reduces to (b).** For a smooth C, a random fibre solve succeeds with probability ≥ 1/36 − O(p^{−1/2}). Its
  cost is poly(log p) (PROVED given smoothness; §4.2). Exhaustive search is not needed.
* **G3.** The §9.1 along-line formulas, the claim that W+S has rank 2 after Q₃ is eliminated, and the linearity of μ
  are proof sketches in the target ("PROVED given §2"). The referee re-derived none of them in writing. They were
  confirmed independently with 0 failures (§3).
* **G4.** A copy whose special line is the true line spoils the run. The chance of this is ≤ 54/(p+1) per run, so the
  algorithm needs p ≫ 54. Both simulations conditioned this event away. Without the conditioning, a run at p = 11
  succeeds with probability ≈ (10/11)^54 ≈ 0.6%.
* **G5.** Human review is pending, novelty is unchecked, and the error analysis of the approximate QFT and phase
  oracles is not written.

Claim gates stay false until a human has reviewed G1–G3: "exit (ii) closed", "a poly-time non-binary merge exists",
and any lower bound.

## 1. Consistency with the 11-12 impossibility note

**No contradiction (PROVED from the definitions).** The procedure lies outside SOT(Aut), for this precise reason:

* The per-copy IS front end starts with two legal SOT(Aut) operations:
  * O2, the γ₃ label;
  * O4, promotion to fil4_λ = G/ker λ.
* The frame is then the non-abelian fil4_λ. The next operation is a QFT over N_λ = exp(F_p g₀ + γ₂)/ker λ. That
  subgroup is abelian and normal but **not central**, and the QFT keeps the transversal coordinate x coherent. None of
  O1–O6 does this:
  * O6 needs an abelian frame;
  * O5 (restriction to N_λ ⊇ γ₃) would measure x and erase all the information.
* The note excludes this operation explicitly: §1 table, "IS Cor 8 / HPGP … no"; §10, "Fourier over a non-central N".
  It is exit (ii) of §8.
* The S, coset and phase steps then act on transversal phase states, which are not group-frame registers, so they are
  not O3 merges either.

**Where Theorem R's mechanism is bypassed.**
* Proof step 2 of Theorem R says that O6 forces promotion of all of γ₃, and that promoting the last part requires
  ẑ = 0, which is a binary zero-sum.
* The front end never promotes the label away. It absorbs it into the N_λ-character sector l = −1. Exactly: all
  outcome probability lies on l = −1, uniformly over (j, k) (`check_copy.out`, 174 non-special copies at p = 7, 11, 13,
  0 exceptions).
* The F_p-weighted relations s_j are then usable. Lemma Q of the target shows that they are non-binary.

**Single-copy and two-copy refutations.** Both still hold and are consistent with the procedure:
* η_c enters copy i only through a₁, as λ_i(η_c)/f_i(e). It cancels only along φ_j(e), through Σ_i s_i λ_i = 0. That is
  a three-copy relation.
* The single-copy average over η_c is I/p³, and independent pairs carry nothing (Lemma J). The procedure never relies
  on either.
* Theorem R's "transcript H-independent until the crossing" also has an analogue here: every outcome before the final
  z is exactly uniform (§3).

**What changes.** If G1 is settled, exit (ii) of §8 is open in the positive direction. The note's §8 "UNKNOWN" would
then be resolved, but the note remains correct as stated.

## 2. Information leakage (both scripts read line by line)

**Public choices use only labels, outcomes and trial H.** No H-dependence found:
* `aligned_triples.build/search` and `end_to_end.find_u` use labels, charts, κ, s, f and h only.
* `Level2.__init__` (`end_to_end.py:35`) computes Q₃ from the labels.
* The level-3 data (`end_to_end.py:123–145`) use trial H (e₃ = η_c = 0) and the base points x0.
* μ's coefficients (`end_to_end.py:200–206`) come from trial H.
* The true η enters only through the `table(eta)` calls of the checks and of the final state.

**Sampling.**
* y and x0 are drawn uniformly (`end_to_end.py:37–38`), and so are the level-3 bases (`:146`). That is the true
  distribution, because every state in the pipeline has flat modulus. The referee verified this exactly rather than
  assuming it: the deviation is ≤ 1e−16 for the S outcomes, level 2 and level 3.
* Taking a uniform point of the coset as the origin is equivalent to taking a canonical representative. The
  referee's code uses the canonical representative.
* z is drawn from the exact |FFT|² of the closed-form final state (`:208–211`). The closed form agrees with the
  group-level state (§3).

**So the simulation does not assume its conclusion.** It has four weaknesses, none of which is a leak:
1. **Label conditioning on test lines** (`end_to_end.py:73–75`). Labels avoid the special lines of the 5 test lines,
   and the true line is one of 4 of them (`:191`). This conditions on H. It is benign asymptotically, but see G4.
2. **Fits and phase checks on the test lines only** (`:96`, `:125–129`, `:159`, `:200–206`). Linearity of μ off the
   test lines was not checked there. The referee's code checks every generic line of every triple: 0 failures.
3. **The same pipelines are reused across trials.** `recover()` rebuilds `main(p, 6, 3, 8, sd)` from the same seeds
   for each hidden H. All five p = 11 trials used seeds [1, 2, 4] (`end_to_end_recover11.out`), and both p = 17 trials
   used [1, 2, 3]. So "12/12" means about 3 pipeline instances per prime, each tested against several H. It is not 36
   independent runs.
4. **"Unique solution from 3 equations" is a chance event.** Two runs' equations are proportional with probability
   about 1/(p+1) (§3).

## 3. Independent reproduction (exact, from the definitions)

**Code.**
* `f23.py`: free23 with its own bracket and class-3 BCH (associativity: 0 failures). It builds the true copy:
  * a uniformly random base point g and the pure coset state |gH⟩ on ℂ[G];
  * the projector onto label λ;
  * the promotion to G/ker λ, with ker λ-invariance checked;
  * the chart g = n·exp(x x');
  * the QFT over N_λ by FFT;
  * y sampled from its exact probabilities.
* `pipeline.py`: the three levels. Each coset measurement is sampled from |amplitude|² of the true product state. The
  post-measurement state is its restriction, and no flatness is assumed. The final QFT uses the true amplitudes.
* Public identities "for all e" are interpolated per triple and verified on every other generic line of that triple.

| check | result |
|---|---|
| true state vs trial-H routine vs re-derived closed form, `check_copy.out` | 0 / 0 mismatches over 174 non-special copies (p = 7, 11, 13). The phase table is base-point-independent up to a global phase |
| polynomial-identity fits (W, S, E3, level-3 N, μ), a₃ independent of y/e₃/η_c, η_c cancels along φ | 0 failures in 240 level-2 searches and 45 completed runs |
| W ⇔ S | same solution sets in 240/240. **S ⇒ W PROVED** by polarization: T(w,w,d) ≡ 0 gives T(d,d,·) = 0. So equality means only that the ranks are equal |
| final z on the predicted line z·M_ref e = μ(e, e₃) | 0 violations, mass 1.000, in 45/45 runs (p = 7: 9, p = 11: 24, p = 13: 12). Support 7–13 points of the line (once 1 point) |
| recovery of (line, e₃) from 3 fresh runs, true line uniform over all p+1 lines | p = 7: 3/3; p = 11: 7/8; p = 13: 4/4. The one failure had two proportional equations, so the true value was among 12 candidates |
| negative control: drop Q₃, keep everything else (`negctl.out`) | mass on the predicted line 0.08–0.17 ≈ 1/p. The check is not vacuous, and Q₃ is essential |

**Costs observed.**
* Copies per completed run at p = 11, 13: mean 64. This includes dependent-label discards and level-2 redraws
  (9/129 groups, about 7%). At p = 7 the redraw rate is 72/111, because cubes are ±1 when 3 | p − 1.
* Level-3 failures: 4/40. They happen when a conic coefficient is 0, at a rate of about 1/p per coefficient
  (`k3stats.out`). That is a small-p effect.

**Chart artefact seen at p = 7 (not a leak).** When every copy has λ₀ ≠ 0, the chart has x' = (1,0). The trial phase
at e = (1,0) with e₃ = η_c = 0 is then identically 0, so N_l·(1,0) = 0. This is public and does not depend on H.

## 4. Resources

### 4.1 Per run

* **Copies:** 54 = 3 × 6 × 3, plus O(1/p) discards. Two runs suffice with probability 1 − O(1/p); the target used 3.
  Then restrict raw copies to K = exp(F_p(e + e₃z) + γ₃) ≅ F_p³ and Fourier-sample to get η_c (standard).
* **Quantum gates:** poly(log p). The work is:
  * 54 front ends: a γ₃-QFT, chart arithmetic (BCH, O(log² p) gates) and a QFT over F_p³;
  * 18 S-measurements;
  * three 12-dimensional and one 6-dimensional F_p-linear coset measurements;
  * cubic and quadratic phase oracles;
  * one QFT over F_p².

  PLAUSIBLE; the approximate-QFT error analysis is not written.
* **Classical, as implemented in the target:** exhaustive search over (p−1)⁵ projective u per level-2 state, and
  (p−1)² for level 3. That is p^{5+o(1)}, not polynomial. Its public tables use p × p grids; the closed form gives the
  same coefficients in poly(log p).

### 4.2 Items (b) and (c)

**The weight variety.** After Q₃ is eliminated, W+S always has rank exactly 2 on u³. This was observed in 240/240 runs
and in 30 configurations at p = 101 to 30011 (`curve_*.json`). E3 is 2 diagonal quadrics. So the variety is

C = {K u³ = 0, E u² = 0} ⊂ P⁵,

of type (3,3,2,2).

**Exact facts (Sage/Singular, `curve_geom_*.out`).**
* The cone has dimension 2.
* The Hilbert polynomial is 36t − 72, so the degree is 36 and the arithmetic genus is 73.
* The singular locus is empty (projectively) in 6/6 configurations at p = 10007 and 6/6 at p = 30011.

**Torus point counts.** Exhaustive at p = 101, 227 and 503, with p ≡ 2 mod 3 (`count_points_*.out`):

| p | #C(F_p) on the torus / p, 6 configurations |
|---|---|
| 101 | 0.88–1.05 |
| 227 | 0.89–1.00 |
| 503 | 0.94–1.04 |

A count of about p is the signature of one geometrically irreducible F_p-component.

**For these instances (PROVED, computer-assisted).**
* A smooth complete intersection of positive dimension is connected (Hartshorne III Ex. 5.5, cited from memory). Being
  smooth, it is therefore geometrically irreducible.
* The Weil bound gives #C(F_p) ≥ p + 1 − 146√p.
* At most 6 · 36 points lie off the torus.
* So torus solutions exist whenever p ≥ 21,751. In particular they exist for all 6 sampled configurations at
  p = 30011.

**Solver (c), given smoothness (PROVED).**
* Set u₁ = 1 and u₆ = t, with t random, and solve the zero-dimensional system in u₂, …, u₅. Its Bezout number is 36.
* Each torus point lies in exactly one fibre, and each fibre holds ≤ 36 points. So
  P[the fibre has a torus point] ≥ (p − 146√p − 216)/(36p).
* Each solve costs O(1) field operations for the elimination plus root finding of degree ≤ 36 (Cantor–Zassenhaus).
  That is poly(log p).
* Observed: 76/120 fibres at p = 10007 and 77/120 at p = 30011 had a torus point.
* Level 3 is one diagonal conic: poly(log p) whenever its coefficients are nonzero (probability 1 − O(1/p)).

**What is missing for a poly(log p) total.** Exactly G1. One smooth fibre of the family over Spec Z[labels][1/Δ]
makes the generic fibre smooth, because the smooth locus is open. Then, for all but finitely many p, the bad labels
have probability ≤ deg/p.

This needs three things written out:
1. a uniform algebraic description of K and E over Z[labels], on the open set where the charts and pivots are fixed;
2. an effective degree;
3. the exceptional primes.

Until then, (b) is **CONDITIONAL**. It is strongly supported.

## 5. Classical baseline

* **Classical post-processing cannot replace the quantum step.** Every outcome before z (labels, y, S, cosets) is
  exactly uniform and independent of H (§3), so it carries no information. All the information comes from
  interference in the final Fourier sample.
* **Plain Fourier sampling falls short.** The target's own measurements show single-shot Fourier MI decaying with p:
  for a triple, F3 drops from 0.0031 to 0.0014 bits between p = 5 and 7 (§6, §9.5). The referee did not evaluate
  strong Fourier sampling of raw coset states.
* **The known binary merge needs a zero-sum solver.** It needs ZS(p, 2, n) (Theorem R / Prop R′). Brute force costs
  about p² per merge; generalized birthday is conjecturally 2^{O(√log p)}. Neither is poly(log p).
* **Classical query access** is not polynomial: Ω(√p)-type collision bounds (standard; not re-derived).
* **Comparison with known algorithms.** The candidate adds F_p-weighted, non-binary relations, made usable by the IS
  front end. The Rees cover already solves free23 in polynomial time. The candidate's interest is that it is
  cover-free and uses a constant number of copies per equation.

## 6. Requested corrections to the target (not applied; the referee edits no other file)

1. **§9.3 table.** Say that the pipelines were reused across trials, and that the true lines were restricted to 4
   test lines.
2. **(e).** Say that 54/(p+1) ≥ 1 for p ≤ 53, so the simulation is a large-p proxy (G4).
3. **(c).** Replace "exhaustive" by the fibre solver, and make (c) conditional on (b) only.
4. **(f).** Mark it settled by this referee (§1).
5. **W ⇔ S.** S ⇒ W is PROVED; equality is equality of ranks.
6. **Runs.** Two runs are generic, and a dependent pair has probability about 1/p, so a further run must be allowed.

## 7. Adversarial self-check

* **Did the referee's simulation share the target's closed form?** Only for trial-H public data. The true states come
  from ℂ[G] with random base points, and they match the closed form exactly. A wrong closed form would have broken
  the support check, as the negative control shows.
* **Is the conditioning on special labels a leak?** It uses H. But the support identity holds for every non-special
  label set, so the conditioning cannot fake success. It only hides a failure mode of probability ≤ 54/(p+1) (G4).
* **Does "smooth at p = 10007 and 30011" prove (b)?** No. It proves (b) for 12 sampled instances. The
  generic-smoothness step is a sketch.
* **Citations from memory.** Hartshorne's connectedness exercise and the Weil bound for smooth curves are cited from
  memory (TRAPS 10).
* **The Sage singular-locus test.** It uses the 4×4 minors of the Jacobian of the 4 generators. That test is valid for
  a complete intersection, and codimension 4 with 4 equations was checked.
* **Small primes.** p ≤ 13 for the full quantum simulation, so this is falsification only. The genericity counts are
  on the torus.
* **Not checked:**
  * the target's claim that "only aligned merges qualify";
  * the dense-σ validation in `isbasis.py`, which was superseded by the group-level check;
  * the approximate-QFT error;
  * novelty and priority.
* Every claim here is AI-checked and pending human review.

## Reproduce (from the folder; python = /opt/anaconda3/bin/python, sage = /opt/anaconda3/envs/qsearch-cas/bin/sage, all under nice -n 19)

```
python check_copy.py 11 60 5 > check_copy.out; python check_copy.py 7 100 6 >> check_copy.out; python check_copy.py 13 40 7 >> check_copy.out
python pipeline.py 7 1,2,3 > pipeline_7.out; python pipeline.py 11 1,2,3,4,5,6,7,8 > pipeline_11.out; python pipeline.py 13 1,2,3,4 > pipeline_13.out
python negctl.py 11 > negctl.out; python k3stats.py 11 25 > k3stats.out; python k3stats.py 13 15 >> k3stats.out
for p in 101 227 503 10007 30011; do python curve_data.py $p 6 $p; done   # curve_<p>.json (~90 s at 30011)
for p in 101 227 503; do python count_points.py $p > count_points_$p.out; done
sage curve_geom.sage 101 5 > curve_geom_101.out; sage curve_geom.sage 10007 20 > curve_geom_10007.out; sage curve_geom.sage 30011 20 > curve_geom_30011.out
```

Every run takes under 2 minutes and under 0.5 GB.

Acceptance:
* 0 mismatches, fit failures and support violations;
* Hilbert polynomial 36t − 72;
* singular-locus cone of dimension 0 (smooth) at p ≥ 10007.

# Can an entangled, adaptive ISS twist solve free class 3 without the cover? (2026-11-12)

**Status: AI-checked, pending human review.** One AI session did the derivations. The
finite checks are exact (they compute states and probabilities, they do not sample
measurement outcomes), but they can only falsify (TRAPS 7). Scripts and outputs are in
`research/audits/reviews/2026-11-12-rees-entangled-twist-construction/`. No paper, STATE,
handoff or reductions file was edited. Context read: STATE.md "Now" (iii) and (v),
`main-core.tex` (obstacle (2), Section `sec:example-class3`), `2026-11-12-rees-adaptive-twist.md`
and `2026-11-12-rees-direct-twist-class3.md`. No network was used, so the literature
claims below come from those notes, not from fresh reading.

## Verdict

**I did not find a polynomial-time direct algorithm. The precise obstruction is the alignment
of label lines.** All results are for G = exp(L), with L the free 2-generator class-3 Lie algebra
over F_p, p > 3, and H = ⟨exp v⟩ with v_1 ≠ 0. This is the hard case. If v_1 = 0, H lies in the
abelian group γ_2 and direct methods work.

1. **A reduction (PROVED, checked exactly).** After strong Fourier sampling, each copy is a
   cubic-phase state. It is the H-fixed vector in a p-dimensional irrep σ_{λ,κ}, which factors
   through G_λ = G/ker λ ≅ (filiform group, Z_p ⋉ F_p^3). The hidden parameters enter the phase
   as (linear form in v)/D_λ, where D_λ = λ([v_1, z]).
2. **Aligned copies suffice (PROVED, standard BCvD, checked exactly).** Suppose three copies
   have labels on one line of γ_3^*. Then a 3-copy measurement (polynomial map, then a QFT over
   F_p^3) gives the line of v_1 with probability ≥ 1/n_max ≥ 1/6. The measured minimum is 0.31
   at p = 5, 7, 11, 13. ISS in the class-2 subgroup M = exp(F_p v_1 + γ_2) then gives H.
3. **Alignment is the whole problem.** Each fresh copy's label line is uniform among p+1 lines.
   * *Label additivity (PROVED):* any H-independent combining map that commutes with the
     right G-action adds labels. Central characters carry no information about H.
   * *Pole invariance (PROVED):* no automorphism of G changes the line that sits in a copy's
     denominator.
   * *Phase rank (PROVED):* every polynomial-map/QFT measurement on k copies whose labels
     span L distinct lines succeeds with probability ≤ p^{k−3L}.

   So the ISS correction step is never the problem; the label lines are. To align them, you
   need either automorphisms that depend on H (Prop C) or subsets of labels that sum to zero
   with weights 0 and 1 (Imran–Ivanyos).
4. **What does work directly is not polynomial.**
   * Grover over the p+1 candidate lines, with ISS-in-M as the checker: O(√p · poly log p).
     This is a standard composition.
   * A Kuperberg/Wagner-type sieve on the labels: 2^{O(√log p)}. This is CONDITIONAL on the
     heuristic analysis of the k-tree algorithm.

   Neither approach is new as a technique. The Rees cover remains the only polynomial-time
   method known to us for this group.
5. **General entangled measurements outside this template: UNKNOWN.** Ettinger–Høyer–Knill (EHK)
   gives O(log|G|) copies information-theoretically. Nothing here is a lower bound (TRAPS 8).

## 1. The reduction (Prop 1, PROVED)

Notation: z = [x,y], u = [x,z], w = [y,z]. The map ι: L/γ_2 → γ_3, q ↦ [q, z] is an isomorphism
(ι x = u, ι y = w). For a central label λ ∈ γ_3^* ∖ 0, fix:

* x' with λ(ι x') = 1;
* y' = (−λ_w, λ_u), so λ(ι y') = 0 and det(x', y') = 1;
* the polarization 𝔭_λ = span(y', z, u, w). It is an ideal of index p, and the only polarization
  containing z;
* f ∈ L^* with f|γ_3 = λ, f(z) = 0, f(x') = 0 and f(y') = κ.

Then σ_{λ,κ} = Ind_{exp 𝔭_λ}^G χ_f, with κ ∈ F_p, runs over the p irreps with central label λ.
They act on C^p with s = λ(ι q) ∈ G/exp 𝔭_λ.

**Prop 1.** Let D = λ(ι v_1) and δ = det(v_1, x'). If D ≠ 0, the H-fixed space of σ_{λ,κ} is
spanned by ψ(s) = p^{-1/2} ω^{Φ(s)}, where

  Φ(s) = [ s·f(v) − (s²/2)·v_z − (s³/6)·δ ] / D.

Strong Fourier sampling of a coset state |aH⟩ gives:

* label λ: uniform on γ_3^*, for every H with H ∩ γ_3 = 1;
* each regular (λ, κ): probability exactly p^{-3}. The Fourier coefficient equals
  √p·σ(a)|ψ⟩⟨ψ|, so the residual state is ψ (or its conjugate), independent of a.

*Proof.* Since D ≠ 0, H acts simply transitively on G/exp 𝔭. So the fixed vector is unique and
equals ψ(s_t) = χ_f(m_t) with exp(tv) = c(s_t)m_t and s_t = tD. Expand
m_t = BCH(−s x', (s/D)v) at class 3. This uses f([x',v]) = c − δ f_z,
f([x',[x',v]]) = −δ and f([v,[v,x']]) = δD. The rest is Frobenius reciprocity. ∎

Check (`check_formula.py`, all exact):

| check | p = 5 | p = 7 |
|---|---|---|
| homomorphism failures | 0/200 | 0/200 |
| ⟨χ,χ⟩ = 1 and inequivalence | all 24 labels × 5 κ | 6 labels × 7 κ |
| closed form not fixed, or ≠ orbit vector | 0/339 | 0/347 |
| SFS coefficient ≠ √p σ(a)\|ψ⟩⟨ψ\| | 0/300 | 0/49 |
| regular irreps with probability p^-3 | all | all |

Copies with D = 0 have probability (p−1)/p² in total. They are the "eigen" events of the
earlier note, and they cannot be recognized.

## 2. Aligned copies (Prop 2, PROVED: BCvD for m = 3 inside G_{λ_0})

Take labels λ_i = m_i λ_0. Then frame i is (x'_0/m_i, m_i y'_0) and D_i = m_i D_0. With
θ = (δ_0, v_z, λ_0(v_3))/D_0, the phases are

  Φ_i(s) = θ · C_i(s),  C_i(s) = ((−κ_i s − s³/6)/m_i², −s²/(2m_i), s).

Measure as follows: compute Γ = Σ_i C_i(s_i) ∈ F_p^3, measure the fiber index, and apply the QFT
over F_p^3. The probability of getting θ is Σ_j N_j²/p^6 ≥ 1/n_max, by Cauchy–Schwarz, where
n_max is the largest fiber. The system has degrees 1, 2, 3, so n_max ≤ 6 when the fibers are
finite. That holds for generic labels; I did not prove it for all labels. Then
v_1 ∝ x'_0 − θ_1 y'_0. Given the line of v_1, M = exp(F_p v_1 + γ_2) has class 2 (M ≅ Heis × Z_p)
and ISS finishes.

Check (`check_aligned.py`, 40 random instances per prime):

* linearity holds, decoding is right, and the simulated quantum measurement equals the formula:
  0 failures;
* P(θ): min 0.328, 0.313, 0.322, 0.423 and mean 0.52, 0.50, 0.48, 0.49, at p = 5, 7, 11, 13.

## 3. Why alignment cannot be had for free

**Lemma L (label additivity, PROVED).** Let T: ℓ²(G)^{⊗m} → ℓ²(G) be linear and commute with
the diagonal right action of G. Then T sends inputs with central labels λ_1, …, λ_m to an output
with label Σλ_i. γ_3 is central, so n acts on the input by ∏λ_i(n), and T intertwines.

The merge "measure k = g_1 g_2^{-1}, keep Ψ(g) ∝ ψ_1(kg)ψ_2(g)" is such a map, branch by branch.
It is also deterministic: Ψ is supported on one full coset of K = Hγ_3.

`check_merge.py` checks this exactly on all of G (100 merges at p = 5, 39 at p = 7, 0 failures):

* Ψ is right-H-invariant;
* its label is λ_1 + λ_2;
* its support has size p³;
* its κ-law is exactly uniform (1/p);
* its output is the closed-form fixed vector.

So a merged copy is distributed like a fresh copy with label λ_1 + λ_2. By Prop 1 the label law
does not depend on H. **Hence idea (c), learning H from the central characters of multi-copy
states, is REFUTED in its literal form:** those characters are sums of H-independent uniform
labels.

**Lemma P (pole invariance, PROVED).** Let α ∈ Aut(G) induce A on L/γ_2. Then
ι(Aq) = α(ιq)/det A, so

  D_{λ∘α}(α^{-1}v) = det(A)·D_λ(v).

The twisted copy is the fixed vector of α^{-1}(H) in σ∘α. Its denominator, as a function of the
unknown v, therefore vanishes on the same line as before. Twisting changes the label but not the
pole.

`check_rank.py`: 0/300 failures at p = 7 and at p = 11.

**Prop R (phase rank, PROVED for L < p/2).** Take k copies, possibly twisted by public
automorphisms, whose original labels span L distinct lines. In the chart v = (1, r, c, d, e),
the F_p-span of {1} ∪ {the s, s², s³ phase coefficients, as functions of the hypothesis} equals

  span{1} ⊕ ⨁_ℓ span{ 1/(r−r_ℓ), c/(r−r_ℓ), ℓ_ℓ(d,e)/(r−r_ℓ) },

so it has dimension R = 1 + 3L. *Proof.* Each copy contributes exactly these functions:
δ/D has a nonzero pole part, because x' and y' are independent. Copies on one line contribute
nothing new. For independence, the c-, d- and e-coefficients separate. Then clear
denominators: a polynomial of degree ≤ L that vanishes on more than L points is zero. ∎

Exact check (p = 7, 11):

* rank = 1 + 3L for L = 1, …, 4 distinct lines;
* rank = 4 for 3 or 4 copies on one line;
* rank = 10, not 4, when public automorphisms put the labels of three copies on one line;
* p = 7, L = 4 saturates at 12 (L ≥ p/2, as the proof requires).

**Lemma Q (template bound, PROVED).** Call a measurement *linear-QFT* if it does three things:

1. writes the joint phase as Θ(v)·Γ(s) + known, with Θ ∈ F_p^d;
2. maps s ↦ (Γ(s), fiber index);
3. applies the QFT over F_p^d and outputs Θ.

This class covers BCvD, the HPGP algorithms and the merge-then-Fourier sieves. Its success
probability is Σ_j N_j²/p^{k+d} ≤ p^{k−d}. Prop R forces d ≥ 3L, so the success probability is
at most **p^{k−3L}**. Success therefore needs L ≤ k/3, i.e. many coincidences of label lines.
With fresh copies, a given pair coincides with probability 1/(p+1). Variants that measure some
of the registers in the computational basis reduce to this template on the remaining copies.
That reduction is argued, not proved in general.

## 4. Where each proposed route breaks

* **(a) Twist preserving H only modulo a smaller subgroup, then correct.**
  * The correction is never the obstruction. A public twist only relabels the unknowns: the
    twisted copy's coefficients are still (linear in v)/D_i (Lemma P). So any central or
    BCH correction is absorbed by the QFT. This is PROVED inside the template.
  * Its denominator line does not move, so it buys no alignment.
  * Learning Hγ_3/γ_3 by ISS on Q = G/γ_3 needs Q-coset states. These are copies with λ = 0,
    which occur with probability exactly 1/p². Making them by merging requires a subset of labels
    with zero sum, using weights 0 and 1 (Lemma L).
  * Weighted cancellation, as in ISS's class-2 system Σ j_i² u_i = 0, needs twists that
    preserve K = Hγ_3 (merged inputs must agree modulo the kernel of the output label). That is
    Prop C.
* **(b) Coherent superposition over candidate twists.** Superpose over the p+1 candidate lines r'.
  In branch r', align with the K-stabilizing twists for slope r' and output r'.
  * Without later joint processing, the output register is the branch mixture. So
    P(success) ≤ 1/(p+1) + max_{r'≠r} P_{r'}.
  * A wrong branch outputs r' ≠ r. For variants that decode the slope from data, the wrong
    branches still carry distinct poles (Lemma P), and a Weil-bound argument makes their
    outputs nearly uniform. That part is argued, not computed.
  * With verification and amplitude amplification, (b) is exactly the O(√p) Grover baseline.
* **(c) PGM / Kuperberg combining in poly(log p) copies.**
  * Combining is label addition (Lemma L).
  * The PGM is information-theoretically enough with O(1) copies: each unaligned copy has
    single-copy overlaps of order p^{-1/2} (Weil), and EHK applies. I did not compute it.
  * Implementing it efficiently is the open problem. The algebraic implementation is ruled out
    by Lemma Q unless the label lines align.
* **(d) Other routes tried.**
  * Partial central measurement (λ_w = 0 only) gives genuine coset states of the filiform
    quotient, with probability 1/p each: an O(p) algorithm.
  * Guessing a Carnot grading W ∋ v mod γ_3 works with probability 1/p; this is the plane case
    of the partial_info table.
  * Collecting three copies on a common line by the birthday bound costs about p^{2/3} copies.
  * The sieve: run Wagner's k-tree on the label coordinate λ_w, with 2^{√log p} lists of size
    2^{√log p}, three times. Merge each solution, then apply Prop 2. Cost 2^{O(√log p)}.
    CONDITIONAL on the heuristic k-tree analysis; a degenerate D = 0 occurs with probability
    1/p per merge.

## 5. Honest comparison

**Rees cover.**
* Polynomial in log p. Its sufficient count for this instance is about 2^{33.19} queries.
* It aligns nothing, because the dilations of the cover preserve the lifted subgroup for every H.

**Direct methods.**
* The Grover baseline O(√p polylog p) is simpler, but exponential in log p. Comparing
  sufficient counts is not a lower bound (TRAPS 9).
* The sieve is subexponential and uses only standard parts: Kuperberg-type merging plus
  BCvD in a quotient. I did not search the literature for it; it should not be called new.

**What is new here** (repo-level, AI-checked):
* the closed form of Prop 1;
* the pole-invariance lemma;
* the rank bound p^{k−3L}.

Together they locate the class-3 analogue of ISS's label cancellation exactly. The cancellation
target is a common label line, not zero, and only H-dependent twists can reach it. Claim gates
are unchanged: the cover is not claimed necessary, and no hardness is claimed.

## 6. Adversarial self-check

* **The template is narrow.** Lemma Q excludes non-QFT measurements, measurements on
  multiplicity spaces of 3-fold Clebsch–Gordan products (those spaces are p-dimensional and
  carry conjugation-invariant information), and maps that preserve every ℓ²(G)^H without
  commuting with G. None of these is ruled out.
* **The rank can drop with side information.** If c and v_3 were known, R = 1 + L. That still
  exceeds k when L ≈ k, but it is a different bound.
* **Small primes.** p ≤ 13 checks are exact but say nothing for large p beyond falsification.
  At p = 7 the rank saturates at L = 4, as the proof requires.
* **Prop 2 rests on n_max.** Its bound needs finite fibers. Degenerate labels (for example
  κ_i making the cubic equation linear) were not classified. The measured minimum of 0.31 is
  over 160 random instances.
* **The sieve cost is heuristic.** The k-tree analysis over F_p (interval merging) is heuristic.
  A rigorous version (Minder–Sinclair style) is expected but was not checked.
* **Grover needs coherent ISS.** It requires a coherent, error-reduced ISS run in M_{r'}. This
  is standard, but I did not write it out.

## Next hard question

Is there a polynomial-time measurement on poly(log p) copies whose label lines are pairwise
distinct? In normalized form the problem is this. Learn r ∈ P^1(F_p) from the states
Σ_s ω^{(g_i·r)s³/6 + β_i s² + α_i s}|s⟩, where the g_i ∈ SL_2(F_p) are known and random, and
β_i = −c/(2 j(g_i, r)) and α_i = (linear in r, v_3)/j(g_i, r). Here j(g, r) is the
automorphy factor and (c, v_3) are shared nuisances.

A yes would give a direct polynomial algorithm. A no needs a lower-bound technique beyond
templates.

**Next command.** Compute the exact PGM success for k = 2, 3, 4 unaligned copies at p = 5, 7, as
a sanity check of the information content:

`nice -n 19 /opt/anaconda3/bin/python pgm_unaligned.py 5` → `pgm_unaligned.out`

Acceptance: the success for r increases toward 1 with k. Then do a literature check on hidden
rational-function and Möbius phase problems.

**Mechanical items** (for Gemini; not added to the plan file): add the four checks below to the
artifact index.

## Reproduce (from the folder; each takes under 10 s)

```
py() { nice -n 19 /opt/anaconda3/bin/python "$@"; }
(py check_formula.py 5; py check_formula.py 7) > check_formula.out
for p in 5 7 11 13; do py check_aligned.py $p 40; done > check_aligned.out
(py check_merge.py 5 200; py check_merge.py 7 60) > check_merge.out
(py check_rank.py 7; py check_rank.py 11) > check_rank.out
```

Acceptance:
* every failure counter is 0;
* `rank == predicted`, except the documented p = 7, L = 4 saturation;
* min P(θ) ≥ 1/6.

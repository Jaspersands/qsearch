# Rees full campaign 2, item 8: notes the paper cites without re-auditing them

2 November 2026. AI session only; nothing here is a human review, and no claim gate
changes. The target is `docs/papers/rees-hsp/main-full-draft.tex`; line numbers below
refer to that file as of this pass. Scripts and outputs are in
`research/audits/reviews/2026-11-02-rees-cited-notes/`, one subfolder per note.

Labels: **proved** (written proof here), **exact** (exact integer or rational
computation), **float** (numpy, tolerance about 1e-9), **argued** (written argument
that relies on an imported theorem or on steps not checked line by line), **import**
(a published theorem whose statement was read from the full text).

## Verdict

Of the notes round 1 left unchecked, two sentences in the paper fail. Both are paper-side restatements of classical-filter notes, (ii) and (iii) below, and each needs a one-sentence fix. No note's own claim fails. The rest hold, sometimes with wording fixes:

- `REES_FULL_GRADE_PARAMETER_BOUND.md`: everything the paper uses holds (exact). The
  paper's pointer names the wrong note, though. The proof of Theorem power-sde(ii) is in
  `POWER_SDE_SYMMETRIC_CONTRACTION.md` and `POWER_SDE_RANDOMNESS_BUDGET.md`. This note is
  the whole-grade composition and resource count, and it should be cited for those.
- `REES_MIXED_SPECTRAL_SOURCE.md`: the reduction survives. Its stabilizer, gap and
  register-count lemmas are proved here and checked exactly or in floating point, with no
  counterexample. Its four imported results match their sources up to three citation
  fixes. Its growth-clock bound also has a self-contained proof here. The paper can state it
  as a conditional remark instead of a bare pointer. Proposed text is below.
- `DERIVED_RANK_REES_EXTENSION.md`, scalar-flag bound: holds as stated (exact).
- `REES_PREMATURE_GRADE_MEASUREMENT.md`: accurate, but too vague. Its obstruction holds and
  was checked exactly at c = 3, 4. Its exponent at c = 12 is also 55, so the remark should
  name the interface and the family (P0).
- Classical filters, Remark rem:filters:
  - (ii) "every anchored 2-jet is inconclusive at T = p" is **false** for the tangent
    family. The smallest instance is the note's own p = 7 control, which a fixed anchor
    resolves. It is true for the note's orbit-sum family.
  - (iii) "canonical gauge fixing is not available over F_p" is **not in the note and
    false**. The note says Gram-based support recovery fails.
  - (i) needs an explicit large-kernel example.
  - The Moore-form recognizer cites the wrong note.
  Fixes are P4–P7.

## 1. Table of every note the draft cites as a source

"R1" means a round-1 report already checked the claim. "App." means the note's content is
being turned into an appendix by items 14–18 of `REES_FULL_CAMPAIGN_2.md`, so it is skipped
here. "Here" means it is checked in this report.

| Line | Note | Claim the paper takes from it | Checked by | Status here |
|---|---|---|---|---|
| 72 | `REES_HSP_REDUCTION.md` | tuple oracle, controlled right-action channel (core) | R1 `2026-11-01-rees-core-proof-check.md` §§1–7 | not redone |
| 363 | `REES_PREMATURE_GRADE_MEASUREMENT.md` | obstruction for one measure-first interface; Ω(p^55) withdrawn | none | **here, §5** |
| 440 | `POWER_SDE_SYMMETRIC_CONTRACTION.md` | Thm power-sde(ii), two-level construction | R1 core §5.4; `-small-prime-arity.md` | App. (item 14) |
| 450 | `REES_FULL_GRADE_PARAMETER_BOUND.md` | "part (ii) is a proposed corollary"; Table full-grade-budget | R1 core §5.4 checked the contraction only, not this note | **here, §2** |
| 476, 572, 587 | `RANDOM_COLUMN_REES_PARAMETER_BOUND.md` (§§5, 6) | Thm random-column; Cor fpt-r; Cor codim(ii) | R1 core §5.5; `-fpt-torsion-check.md`; `-codimension.md`; 10-30 review | App. (item 15) |
| 485 | `REES_UNIFORM_INSTRUMENT_COMPILATION.md` | Thm uniform-compilation | R1 `-compilation-filters.md` part (a) | not redone |
| 491 | `DERIVED_RANK_REES_EXTENSION.md` §3 | BCH by ODE, bracket count | R1 `-compilation-filters.md` (a)(i) | not redone |
| 572 | `DERIVED_RANK_REES_EXTENSION.md` §2 | scalar-flag bound 2^{O(r² log(r+2))}, "needs no random-column argument" | none | **here, §4** |
| 587 | `BOUNDED_CODIMENSION_HSP_REDUCTION.md` | Cor codim | R1 `-codimension.md` | App. (item 18) |
| 597 | `UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md` | Thm ring-to-field, quotient oracle | R1 `-fpt-torsion-check.md`, `-black-box-check.md` | App. (item 17) |
| 624, 629 | `FREE_LAZARD_PULLBACK.md` | black-box pullback; "chart from notes still under review" | R1 `-black-box-check.md` | App. (item 17) |
| 635 | `UNIVERSAL_LAZARD_WORD_COMPILER.md`, `CLASS_FOUR_PRIME_POWER_INPUT.md` | words valid mod p^e; implemented coverage c ≤ 4 | R1 `-prime-power-compiler.md` §1 | not redone |
| 644, 648 | `REES_SUBSPACE_SYMMETRY_SOURCE.md` | Thm subspace-source | R1 `-subspace-source.md` | App. (item 16) |
| 665 | `REES_PROJECTIVE_STATE_SOURCE.md` §3 | zero-moment design, four steps | R1 `-subspace-source.md` | App. (item 16) |
| 684 | `REES_MIXED_SPECTRAL_SOURCE.md` | "proposes a separate spectral-flag reduction" | none (`-subspace-source.md` line 7 put it out of scope) | **here, §3** |
| 717, 723 | `POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md` | filter (i); Moore-form gradient recognizer | R1 `-compilation-filters.md`: "not reproved" | **here, §6** |
| 718 | `ITERATED_QUADRATIC_JET_FILTER.md` | filter (ii): anchor and index statements; T = p family | R1 checked anchor and index only | **here, §6** (T = p family) |
| 718, 723 | `SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md` §3 | linearization under p > max(D,(D−1)Δ); Δ < p not enough | R1 `-compilation-filters.md` (exact) | not redone |
| 719 | `TENSOR_TRAIN_CLASSICAL_FILTER.md` | filter (iii) | R1: "not reproved" | **here, §6** |

Lines 99 and 191 ("conditional corollaries recorded in the project notes") refer to
Schedules 2 and 3 and Cor fpt-r, all covered by items 14 and 15. Line 357's cubic-control
counts are artifact numbers (`rees_complete_instrument.json`), not a note, and are out of
scope.

## 2. `REES_FULL_GRADE_PARAMETER_BOUND.md`

**What the paper says (line 450).** "Part (ii) is a proposed corollary
(REES_FULL_GRADE_PARAMETER_BOUND.md); its proof is not reproduced here." Table
full-grade-budget and its caption ("Whole-grade contraction reduces the leaves per terminal
sample at c = 12 from … to …") take their numbers from the note's artifact
`research/reductions/rees_full_grade_budget.json`.

**What the note claims.** For an explicit n-dimensional Lie algebra of class c < p, with
r = dim[L,L], r_d = dim γ_d L and g_d = gcd(d, p−1):
1. (§1) A whole central grade is removed by one vector SDE at reduced degree g_d. The
   lift is s_i = x_i^u, with d·u ≡ g_d (mod p−1), and s_i = 0 when x_i = 0.
2. (§2) M_d ≤ (d−1)(r_d+1)², and P = ∏ M_d ≤ (c−1)!·[(r+1)!/(r−c+2)!]² ≤ r!((r+1)!)² ≤ (r+1)^{3r}.
3. (§3) One invocation costs at most (1+g^g)·poly(a, g, log p, k) for abort 2^{−k}. The
   uniform-draw cap is Q = J + Σ_{j<g} 2g^{j+1}B + Rg(g−1)K, and classical work adds over
   nodes.
4. (§4) The forest has mP leaves, T ≤ mP − m merges and I ≤ 2mP instruments, with rank
   failure at most 1/((p−1)p^{m−n}).
5. (§6) Artifact numbers for three profiles.

**Checks** (`full_grade/check_full_grade.py`, output `check_full_grade.out`, 0 failures):
- Bezout lift: s^d = x^{g_d}, and s = 0 exactly when x = 0, for every p ≤ 101 in the list,
  every 2 ≤ d < p and every x (35,691 triples, including d = p−1, where u = 0 on nonzero
  entries). **Exact.** The proof is one line: x^{du} = x^{g + t(p−1)} = x^g for x ≠ 0.
- Arity and product chain (item 2) over all 16,383 strictly decreasing profiles with
  r ≤ 14, at the worst case g_d = d (M is increasing in g). **Exact.** The middle bound is
  the one the artifact records as `derived_parameter_leaf_bound` (288 at (6,3,1)).
  r!((r+1)!)² is the class-free relaxation. The ratio between the bound and the true
  worst-case P grows slowly, from 1 at r = 1 to 9.8 at r = 14.
- Rank failure: the exact non-spanning probability 1 − ∏_{i<t}(1 − p^{i−m}) is at most
  1/((p−1)p^{m−t}) for p ≤ 7, t ≤ 4, m ≤ t+4. **Exact.** The general proof is a union over
  the (p^t−1)/(p−1) hyperplanes.
- Artifact: for all three cases, the cover dimension, the final samples m = n + 4, the leaves
  P, the scalar-flag leaves ∏(g_d+1)^{r_d}, the middle leaf bound, the source preparations
  mP and the original inputs c·mP all recompute exactly. So do the SDE calls
  Σ_d m∏_{e<d}M_e, the nonlinear SDE calls, k = ⌈log₂(9T_rand)⌉, the uniform-draw cap
  Σ calls·Q and the fair-bit cap Σ calls·Q·L·⌈log₂ p⌉, all recomputed from the §3 formulas.
  The bounds I ≤ 2mP and T ≤ mP − m hold. **Exact.** Class-12 profile: P = 7,640,436,342,325,248,000
  against 371,209,638,446,513,340,737,559,399,141,212,160,000 scalar-flag leaves, at
  g = (2,3,2,1,6,7,2,9,2,1,6) for d = 2..12 at p = 2^127 − 1. The guard p ≥ 16g^{2g+2}
  holds at every grade.
- Σ_{j=1}^{g−1} 2g^{j+1} ≤ 4g^g for g ≤ 39, so Q ≤ g^g·poly. **Exact**; for general g
  the proof is a geometric sum.
- The class-12 profile (13, 11, 10, …, 1) is realized by the model filiform algebra
  [e₁, e_i] = e_{i+1} of dimension 13 over any F_p with p > 12. **Proved.** The artifact
  itself does not certify realizability.

**Gap or misattribution.** The note does not prove Theorem power-sde(ii). It cites the
two-level construction (`POWER_SDE_SYMMETRIC_CONTRACTION.md`, checked in round 1, core §5.4)
and the randomness budget (`POWER_SDE_RANDOMNESS_BUDGET.md`) for that. What the note adds
is (1)–(5) above. The paper's sentence therefore points a reader at the wrong file for the
proof of (ii). The Weil-count step remains the human-review item (core §5.4), and item 14
writes it out as an appendix.

**Verdict.** Accurate with a fix. Re-point the sentence (proposed text P1).

## 3. `REES_MIXED_SPECTRAL_SOURCE.md`

**What the paper says (line 684).** The earlier weak-Schur-sampling claim is withdrawn,
and "the project note … proposes a separate spectral-flag reduction, which is not
reproduced or re-audited here."

**Exact claim of the note (§1).** The input is fresh i.i.d. copies of an arbitrary density
ρ on q qubits, together with:
- a correct upper bound rank ρ ≤ R;
- a controlled linear unitary representation U of a finite group G;
- the hidden subgroup H = {g : U_gρU_g† = ρ};
- a promised global gap TD(ρ, U_gρU_g†) ≥ δ for all g ∉ H.

From these one can prepare approximate copies of a pure state Ψ such that:
- the ray stabilizer of Ψ is exactly H;
- the overlap satisfies |⟨Ψ|U_g^{⊗}Ψ⟩| ≤ 1 − δ²/8 for g ∉ H;
- Ψ uses at most min(R(R+1)/2, 16R/δ) registers;
- the cost is polynomial in R, q, 1/δ, the number of copies and the inverse error.

No eigenvalue gap, flatness, eigenbasis or inverse is assumed.

**Construction and proof status.**

(a) *Grid and compression (§2). Proved, and exact.* Put w = δ/(16R), J = ⌈1/w⌉, a random
a ∈ [0, M), t_j = w(1 + a/M + j), P_j = 1[ρ ≥ t_j] and B = wΣP_j. Each eigenvalue maps to
b(λ) = w·max(0, ⌊λ/w − a/M⌋). No cap at J is needed, because λ ≤ 1 ≤ Jw.
- Bounds: 0 ≤ λ − b(λ) < w(1 + a/M) < 2w.
- Hence 0 ≤ B ≤ ρ and e = Tr(ρ − B) < 2Rw = δ/8.
- Stabilizer: if g fixes every P_j, then TD(ρ, gρg†) ≤ ½‖ρ−B‖₁ + ½‖gBg† − gρg†‖₁ = e < δ,
  so g ∈ H. Conversely, H commutes with ρ, so it fixes every spectral projector.

Checked exactly on 11,664 (eigenvalue, offset) pairs, including 2^{−40} internal gaps
and tails.

(b) *Product flag and gap (§3). Proved, with a float check.*
- Distinct positive-rank P_j are nested with distinct ranks, so there are K ≤ R of them, Q_l
  of rank r_l. Σr_l ≤ R(R+1)/2, and Σr_l ≤ Σ_j rank P_j = Tr B/w ≤ 1/w.
- The ray stabilizer of Ψ = ⊗Ω_{ran Q_l} is the intersection of the stabilizers of the Q_l,
  which is H by (a). On H the phase is χ = ∏_l det(U|_{ran Q_l}), a linear character.
- For g ∉ H: TD(B, gBg†) ≥ δ − e > 7δ/8. Writing B = Σc_l r_l σ_l with Σc_l r_l ≤ 1 gives a
  component with TD(σ_l, gσ_lg†) ≥ 7δ/8.
- With principal angles θ_i, TD = (1/r)Σ sin θ_i and |⟨Ω|Ω'⟩|² = ∏cos²θ_i ≤ 1 − max sin²θ_i
  ≤ 1 − TD². So |⟨Ψ|U_gΨ⟩| ≤ √(1 − 49δ²/64) ≤ 1 − 49δ²/128 < 1 − δ²/8.

Float checks:
- The lemma |⟨Ω_A|Ω_B⟩|² ≤ 1 − TD(A/r, B/r)² held on 4,000 random subspace pairs,
  including near-coincident ones.
- On 1,768 (state, offset) instances under permutation actions of S₄, D₄, C₅ and S₃×C₂ on
  C⁴–C⁶ (dense random low-rank ρ, partly symmetrized), the stabilizer of the flag product
  equaled H every time. Every g ∉ H met 1 − overlap ≥ 4.0·δ²/8.
- False-gap control: a supplied δ larger than the true gap lets a non-symmetry fix every
  flag. The promise is necessary, as the note says.

(c) *Random margin (§4). Proved, and exact.* Candidate thresholds over all offsets form
the lattice w(1 + k/M), with spacing w/M = 4Δ. So an eigenvalue lies within distance less
than Δ of a threshold for at most one offset, and Pr[bad grid] ≤ R/M ≤ β/8. Checked exactly
on 300 spectra (each eigenvalue spoils at most one offset).

(d) *Threshold instruments (§5). Argued, composition of imports.* The density-matrix
exponentiation copy count O(t²/η) matches Kimmel et al., arXiv:1608.00281, Appendix C,
Theorem 20 (controlled version, program |1⟩⟨1|⊗ρ) and Theorem 1 (either sign of t). Go,
Kwon, Park, Patel and Wilde, arXiv:2412.02134v3, Section IV, Theorem 2 gives half-diamond
error 4t²/n for all program states, hence with references. It assumes t ≥ 0 and n > t; the
negative-time evolutions should be cited to Kimmel's Theorem 1. The phase-estimation
composition is not checked line by line.

(e) *Rank learning (§6). Proved, and exact.*
- Rank identity: E_{i∼λ}[1(λ_i ≥ t)/λ_i] = rank P_t (exact).
- Bias: 2h/w² + (κ+ζ)/w = 1/32 with h = w²/128 and κ = ζ = w/128 (exact).
- Hoeffding at range 1/w and deviation 1/8, with m = ⌈128w^{−2}⌈log₂(2J/β)⌉⌉ and a union
  over J thresholds, gives total failure ≤ β (checked numerically for several w and β).
- Rounding error stays below 1/2.

(f) *Component preparation (§7). Proved here, independently of the import.*
- Acceptance: for any pure ψ ∈ ∧^kV with one-body density γ_ψ (trace 1), one growth step
  accepts with probability (1 − k·Tr(ργ_ψ))/(k+1). Since kγ_ψ ≤ I on V with trace k,
  this is at least w(r−k)/(k+1) whenever ρ ≥ wΠ_V. Checked in floating point against the
  explicit antisymmetrizer for (n, k) up to (4, 3).
- Uniqueness: ∧^rV is one-dimensional, so the output at k = r is exactly Ω_V even for
  nonflat ρ.
- Timeout: stochastic domination by collecting r coupons of probability w/r gives timeout
  ≤ r(1 − w/r)^N ≤ re^{−Nw/r}. Checked against the exact tail of the worst admissible
  geometric sums for r ≤ 6.

This also matches Bene Watts et al., arXiv:2610.06737v1, Section 3, Theorem 5: success
probability at least 1 − r(1 − λ_min/r)^n, with output the antisymmetric state on the
support. Two fixes:
- the known-rank stopping rule is Remark 6, not Theorem 5;
- "nonflat" is the note's word, not the paper's.

Ideal filtering gives ρ_l = Q_lρQ_l/p_l with rank r_l and minimum eigenvalue at least
t_j ≥ w (proved).

(g) *Feeding the Rees core.*
- The paper's four steps (line 665 onward) use only three properties of Ω_V:
  - ray stabilizer H;
  - a linear character on H, which the zero-moment design cancels;
  - a uniform overlap bound 1 − γ off H.
- Ψ has all three, with γ = δ²/8 in place of δ²/2 and Σr_l registers in place of r.
- The phase cancellation needs the same Ψ, hence the same offset a, for every copy in a
  run. The note's "grid chosen once per run" is therefore essential: a fresh offset per
  copy changes χ between the points s ∈ S of one block.

This substitution is **argued**, not checked by simulation.

(h) *Holt–Subramanian citation.* arXiv:2609.38085v2, Section 10.4 (Problem 10.14) is the
mixed-state conjugation-symmetry problem. The "normalized Frobenius separation" that the
note attributes to their Hamiltonian route is in Section 10.2, Theorem 10.8, not 10.4. This
is a fix to the note, not to the paper.

Literature details are in `literature/CITATION_CHECK.md`.

**Smallest counterexample found.** None to the stated claim. The only failure is the
note's own false-gap control (an overstated δ), which shows the global-gap promise cannot
be dropped.

**Verdict.** The reduction survives. Its stabilizer, gap, margin and rank lemmas are
**proved** with **exact** or **float** checks. The physical threshold instrument is
**argued** from imports that match their sources. Its use in the Rees core is **argued**.
The paper may replace the pointer with a precise conditional remark (proposed text P2),
or keep the pointer and add the status; P2 is preferred because the paper aims to be
complete.

## 4. `DERIVED_RANK_REES_EXTENSION.md`, scalar-flag bound

**What the paper says (line 572).** "The earlier scalar-flag bound 2^{O(r² log(r+2))}·poly
… needs no random-column argument."

**Claim.** Descend each central grade one public line at a time, with d+1 sources per line,
or g_d + 1 after the Bezout reduction. Each line needs one scalar diagonal equation
Σλ_is_i^d = 0. It has a nonzero solution by Chevalley–Warning, or trivially if some λ_i = 0,
and van de Woestijne's deterministic solver (Ivanyos–Santha Fact 2, already checked in
round 1, core §5.3) finds it in time poly(d, log p). So P_p = ∏(g_d+1)^{r_d} ≤
P_scalar = ∏(d+1)^{r_d} ≤ (r+2)^{r(r+1)/2}.

**Checks** (`derived_rank/check_scalar_flag.py`, 0 failures):
- The chain holds for all 16,383 profiles with r ≤ 14 and 17 primes. **Exact.** The proof
  uses d+1 ≤ c+1 ≤ r+2 and Σr_d ≤ r(r+1)/2.
- The node identities T ≤ L − M, character measurements = L + T − M and I = L + T + M ≤ 2L
  reproduce in the full-grade artifact. **Exact.**
- The line-by-line descent uses only arbitrary scalar labels and any nonzero witness. This
  is the pointwise central conversion the core check verified for vector labels, applied
  with a = 1. **Argued.**

**Verdict.** Accurate as is, including "needs no random-column argument": it uses no label
law. The bound inherits the core composition's status.

## 5. `REES_PREMATURE_GRADE_MEASUREMENT.md` (Remark rem:premature, line 363)

**Note's exact claim.**
- *Setting.* Filiform L = ⟨X, Y₁..Y_c⟩ with [X, Y_j] = Y_{j+1}, any prime p > c ≥ 3, and its
  actual Rees cover A = ⊕ t^d γ_d(L).
- *Measured subgroup.* N = exp(⊕_{d≥2} A_d) is abelian and normal, but not central, of order
  p^R. The instances are K = exp(F_p tX) against the trivial subgroup.
- *Access model.* On each of M independent lifted coset sources, measure the N-character
  label λ. Keep the label and the post-measurement state. Then apply any CPTP processing,
  abort included, with no further oracle access, no purification and no unmeasured source.
- *Mechanism.* With κ = rank ad(tX)|_N = (c−1)(c−2)/2, only a p^{−κ} fraction of labels
  separates the instances. Every label has mass p^{−R} in both instances, and on the other
  labels the two branches are identical.
- *Bound.* The bank distance is exactly 1 − (1−δ)^M with δ = p^{−κ}(1 − 1/p). Total error e
  therefore forces M ≥ p^κ[1 − e/(1 − 1/p)], hence Ω(c·p^κ) original queries in this
  interface only. The c comes from the interface's c queries per source.

**Proof.** A helper agent re-derived every step and found no gap; I read the derivation
against the note. **Proved**, pending human review. The steps are:
- the projectors;
- the branch formula;
- each stabilizer is either all of K or trivial, because image(exp(aT) − I) = image T;
- equal label masses;
- distance 1 − 1/p on separating labels;
- the binomial tensor formula.

**Exact checks** (`premature/premature_exact_check.py`, `.out`: ALL PASS).
- *Group law (symbolic).* The c = 3 law is associative, of class exactly 3, and N is abelian.
- *Branches (exact, in Z[ω_p]).* Filiform c = 3 at p = 5 with all 125 labels, and at p = 7 on
  8 labels. Every label has mass exactly 1/|N|. All 100 non-separating labels at p = 5 give
  K-branch = trivial branch exactly, and the separating fraction is exactly 1/5.
- *Heisenberg control (c = 2, p = 3, 5).* N is central and κ = 0, so there is no
  obstruction, as central descent predicts.
- *Rank.* κ = (c−1)(c−2)/2 for c = 3..20 over F_p.
- *Stabilizer census.* At (c, p) ∈ {(3,5), (3,7), (4,5), (4,7)} every stabilizer is all of K
  or trivial, with exactly p^{R−κ} fixed labels.
- *Distance and bound formulas.* Checked with Fractions.

**The Ω(p^55) withdrawal (exact).**
- The archived pre-correction statement
  (`docs/papers/rees-hsp/archive/main-2026-10-31-before-correction.tex`, line 296) used a
  computational-basis measurement and a collision count on a profile with g₁ = 2 and
  Σ_{k=2}^{11} g_k = 55.
- The cited artifact case (`rees_full_grade_budget.json`, class 12) has g₁ = 13 and
  Σ_{k=2}^{11} g_k = 65. The withdrawal is justified.
- That artifact profile, (13, 11, …, 1), is exactly the filiform profile of class 12. For
  it, the note's own κ is 55, with R = 66 and |S| = p^{11}. So Ω(p^55) does hold at c = 12,
  but only for the note's measure-and-keep interface and that one algebra.
- The profile alone does not determine κ.

**Verdict.** The paper sentence is accurate, with a clarity fix. "Every grade above one …
is measured first" under-describes the measurement: it is the joint character of a
noncentral abelian normal subgroup, with the post-measurement states kept. The sentence
also does not say that the obstruction is for one family. And since the note's exponent
at c = 12 is also 55, the withdrawal sentence invites confusion. Proposed text P0.

## 6. Classical-filter notes (Remark rem:filters, lines 712–723)

Round 1 checked item (ii)'s anchor and index statements and the linearization sentence.
This pass checks the rest. Scripts are in `filters/`: the shared helpers `fp.py` and four
`check_*.py` files, each with its `.out`. All ended ALL_PASS or matched the note. The
repo's tensor-train solver was imported read-only.

**(i) Orbit-module rank. Accurate with a fix.**
- *Faithful reduction (proved).* diag(g, ρ_W(g)) fixes (0, e_F) exactly when ρ_W(g)e_F = e_F,
  that is when g fixes F. The first block makes it faithful.
- *Exact checks.* Nine exhaustive instances over UT₃(F₃), UT₃(F₅) and UT₄(F₃), including
  the note's Moore-minor control, give Stab F = vector stabilizer every time.
- *"ρ_W alone can have a large kernel".* The note never exhibits this. Its only example,
  an invariant coordinate, has kernel equal to the whole group. Explicit case (exact):
  F = x₂ under UT₄(F₃) has dim W = 2 and |ker ρ_W| = 243, index 3. In general F = x_{D−2}
  under UT_D(F_p) gives dim W = 2 and a kernel of index p (proved).
- *Identity-testing discovery step.* Argued in the note; read and found consistent.

**(ii-b) "In the note's iterated-map family with T = p iterations, every anchored 2-jet is
inconclusive." Fails as worded.** The note has two T = p families.
- *Tangent family P = x + Q.* All degrees 2..p of ℓ∘P^p − ℓ vanish, so the origin jet
  degenerates. But the note itself shows that the fixed anchor e₀ resolves its p = 7
  control: K_* = diag(I₂, UT₃) = H. This pass re-confirmed it exactly (Lie kernel dimension
  6 → 3). On three random dense tangent maps at p = 7, T = 7, the fixed anchors give H = 1
  exactly. So "every anchored 2-jet is inconclusive" is **false** for this family; the
  smallest instance is the note's own p = 7 control.
- *Orbit-sum family P(u,w) = (u + q(w), w + Q(w)), ℓ = Σu_i.* Here the claim is true.
  Every fixed-anchor 2-jet, extension anchors included, is ℓ plus a constant. The note
  proves this from (X^p − 1)/(X − 1) = (X − 1)^{p−1} in F_p[X]. In the p = 7 control, K ⊋ H.
- *Checks for the orbit-sum family (exact):* ℓ∘P^p = u + (terms of degree ≥ p+1) for the
  note's control at p = 7 and 11 and for two random dense instances at p = 7. The degree-8
  term matches the note. The random checks cover m = 1 only.

**(iii) Tensor trains. Accurate with two fixes.**
- *The reduction holds (exact).* On six exhaustive cases the stage-N subgroup equals the
  exact stabilizer, and the repo solver agrees on UT₃(F₅)², where |H| = 25. Gauge-modified
  and dead-bond cores give identical contraction spaces U_i.
- *The p-group premise is needed (exact).* The scalar 2 over F₅ preserves every U_i but
  moves the tensor.
- *"Canonical gauge fixing is not available over F_p" is not in the note, and it is false.*
  A local echelon-basis sweep gives identical canonical cores for gauge-equivalent and
  dead-bond trains, and they rebuild A (exact, p = 3, 5, 7). The note says something
  different: Gram-based support recovery is invalid over F_p because of isotropic vectors.
  For example (1,2) over F₅, or M = [[1,2],[2,4]], which has rank 1 but MMᵀ = 0.
- *Implementation scope.* The index guard applies at every augmented stage, not per site,
  and the implementation covers only odd p. On the note's p = 3 Jordan control, the per-site
  index is 3 ≤ p, but stage 2 has index 5, and the solver returns UNSUPPORTED_COMMON_INDEX.

**(M) "the gradient recognizer for the Moore-form family that defeats the orbit-rank cap
(POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md)". Accurate with a citation fix.**
- The recognizer is in `research/MOORE_GRADIENT_CLASSICAL_FILTER.md`. The orbit-module
  note's 2026-10-22 follow-up line only points there. That note calls the recognizer Monte
  Carlo and "under review". It assumes a promised p-group and imports Luks's subspace
  stabilizer, which is not implemented.
- *Exact, b = 3, m = 2, p = 5, exhaustive over 15,625 elements.* The orbit rank is 9, above
  the cap of 4. The gradient row space is span(e₀, e₃), and Stab F = Stab W = UT₂(F₅)²
  (25 elements). At m = 3 the orbit rank is 27.
- *The note's own caveat (exact).* x₀ + x₁⁵ and x₀ have the same gradient row space but
  different stabilizers.

## Exact statement that now holds

AI-checked only; human review is pending for all of it.

1. **Full-grade bound** (`REES_FULL_GRADE_PARAMETER_BOUND.md` §§1, 2, 4, 6).
   - For every prime p, every 2 ≤ d < p and u with du ≡ gcd(d, p−1) (mod p−1), the lift
     x ↦ x^u (0 ↦ 0) turns a reduced-degree witness into a degree-d witness. **Proved; exact
     for p ≤ 101.**
   - For every strictly decreasing lower-central profile and every prime,
     ∏_d M_d^sym ≤ (c−1)!·[(r+1)!/(r−c+2)!]² ≤ r!((r+1)!)² ≤ (r+1)^{3r}. **Proved; exact for r ≤ 14.**
   - Every count of `rees_full_grade_budget.json` follows from the note's formulas. **Exact.**
   - The proof of Theorem power-sde(ii) is not in this note.
2. **Scalar-flag bound** (`DERIVED_RANK_REES_EXTENSION.md` §2).
   - P_p ≤ P_scalar ≤ (r+2)^{r(r+1)/2}. **Proved; exact for r ≤ 14.**
   - The bound uses no label law. It is conditional only through the core composition.
3. **Mixed spectral flags** (`REES_MIXED_SPECTRAL_SOURCE.md`).
   - Remark P2(i) holds for every offset. **Proved**, with exact and float checks.
   - Each eigenvalue spoils at most one offset. **Proved; exact.**
   - Rank learning by reciprocal eigenvalue sampling. **Proved; exact constants.**
   - The growth step accepts with probability at least w(r−k)/(k+1), times out with
     probability at most re^{−Nw/r}, and outputs exactly Ω_V. **Proved; float and exact
     checks.**
   - The four imports match their sources, up to the citation fixes in §3.
   - The physical threshold instrument and the substitution into the Rees core are
     **argued** only.
4. **Premature measurement** (`REES_PREMATURE_GRADE_MEASUREMENT.md`).
   - In the measure-N-character-and-keep interface on the class-c filiform algebra
     (3 ≤ c < p), bounded error needs M ≥ p^κ[1 − e/(1 − 1/p)] sources, with
     κ = (c−1)(c−2)/2. **Proved; exact controls at c = 3, 4 and p = 5, 7.**
   - This is no bound on coherent receivers.
5. **Classical filters.**
   - (i) holds as stated, and its large-kernel example is now explicit.
   - (ii-b) is false for the tangent family. The smallest instance is the note's p = 7
     control, which a fixed anchor resolves. The claim is true for the orbit-sum family.
   - (iii)'s "canonical gauge fixing is not available" is false and is not in the note. The
     note's statement is about Gram-based support recovery.
   - (M) is correct, but it cites the wrong note.

## Still missing

- Human review of all of the above. A human must also check the Weil-count step of
  Schedule 2 (item 14 / Appendix schedule2) and the DME threshold-instrument composition
  of the mixed source, §5 of that note.
- An end-to-end simulation of the mixed-source substitution into the Rees core. The
  existing artifacts supply spectra as reference access and run no receiver.
- An explicit family with a proved global gap δ, polynomial rank and a nonnormal H, for
  either the flat or the mixed source. As before, none is known.
- Filter (ii-b): the random orbit-sum checks cover m = 1 only. Filters (i) and (iii) import
  Luks's theorem as published; it was not reproved.

## Claim gates that must stay false

`speedup_claim_allowed`, `novelty_established`, `native_application_established`,
`quantum_receiver_implemented`, `circuit_generator_implemented`,
`whole_rees_correctness_certified`, `formal_total_policy_instantiated`, and every Rees
candidate or proof promotion. `mixed_spectral_source.json` stays as it is. Human review is
still required for everything above.

## Proposed paper text

Every item keeps "AI-checked, pending human review". No status rises. Targets are in
`main-full-draft.tex`. The integrator should map them to `main.tex` by the quoted
old text, not by line number.

**P0. Remark premature, lines 361–364** (`rem:premature`). Replace the body with

```latex
Descent proceeds from grade $c$ downward with all lower grades kept coherent. The note \file{research/REES_PREMATURE_GRADE_MEASUREMENT.md} derives an obstruction for one specific alternative interface. In it, the character of the abelian normal, noncentral subgroup $\exp(\bigoplus_{d \ge 2} t^d\gamma_d(\mathcal{L}))$ of the cover is measured on every lifted source, each label is kept with its post-measurement state, and this bank is then processed without further oracle access. For the filiform algebra of class $c$ with $3 \le c < p$, and the hidden subgroup $\exp(\Fp\, tx)$ against the trivial one, only a $p^{-(c-1)(c-2)/2}$ fraction of labels separates the two instances, so bounded error needs $\Omega(p^{(c-1)(c-2)/2})$ sources in that interface. This derivation was checked by an AI session with exact controls at $c = 3, 4$ and $p = 5, 7$ (\file{research/audits/reviews/2026-11-02-rees-cited-notes.md}, Section~5), not by a human. It is not a lower bound for coherent collective receivers or for the procedure here. At $c = 12$ its exponent is $55$. The previous version's $\Omega(p^{55})$ statement was a different, computational-basis collision argument that quoted profile data not matching its cited artifact, and it is withdrawn.
```

Status: argued and AI-checked, for one interface and one family.

**P1. Theorem power-sde, line 450** (`thm:power-sde`). Replace the first sentence

> Part~(ii) is a proposed corollary (\file{research/REES_FULL_GRADE_PARAMETER_BOUND.md}); its proof is not reproduced here.

with

```latex
Part~(ii) is proved in Appendix~\ref{app:schedule2} from the two-level construction of \file{research/POWER_SDE_SYMMETRIC_CONTRACTION.md} and the randomness budget of \file{research/POWER_SDE_RANDOMNESS_BUDGET.md}; that proof is checked by AI sessions only. The whole-grade composition and the counts of Table~\ref{tab:full-grade-budget} come from \file{research/REES_FULL_GRADE_PARAMETER_BOUND.md}. An AI-only check (\file{research/audits/reviews/2026-11-02-rees-cited-notes.md}, Section~2) recomputed every count of that table's artifact from the note's formulas and verified exactly, for every strictly decreasing profile with $r = \dim[\mathcal{L},\mathcal{L}] \le 14$, that $\prod_{d=2}^c M_d^{\mathrm{sym}} \le (c-1)!\,[(r+1)!/(r-c+2)!]^2 \le r!\,((r+1)!)^2$.
```

If the integrator does not adopt Appendix schedule2, use "its proof is in
\file{research/POWER_SDE_SYMMETRIC_CONTRACTION.md} and is not reproduced here" in place
of the first clause, and keep the rest. Status: unchanged (conditional, AI-checked).

**P2. Section subspace, line 684.** Replace the last sentence of the paragraph

> The project note \file{research/REES_MIXED_SPECTRAL_SOURCE.md} proposes a separate spectral-flag reduction, which is not reproduced or re-audited here.

with the sentence and remark below. It should come after Corollary subspace-hsp and its
status paragraph, which is where it sits now.

```latex
A separate reduction replaces the single support by a flag of spectral projectors (\file{research/REES_MIXED_SPECTRAL_SOURCE.md}); we record it as a conditional remark.

\begin{remark}[Nonflat sources by spectral flags; argued, AI-checked only]
\label{rem:mixed-source}
Let fresh i.i.d.\ copies of an arbitrary density $\rho$ on $q$ qubits be given, with a supplied bound $\rank\rho \le \bar r$, an efficiently controlled linear unitary representation $R(\cdot)$ of $G$, $H = \{g : R(g)\rho R(g)^\dagger = \rho\}$, and the promise $\mathrm{TD}(\rho, R(g)\rho R(g)^\dagger) \ge \delta$ for every $g \notin H$. Put $w = \delta/(16\bar r)$, $J = \lceil 1/w\rceil$, draw one offset $a$ uniformly from $\{0,\dots,M_0-1\}$ with $M_0 \ge 8\bar r/\beta$ a power of two, once per run, and let $Q_1,\dots,Q_K$ be the distinct nonzero spectral projectors $\mathbf{1}[\rho \ge w(1 + a/M_0 + j)]$, $0 \le j < J$, of ranks $r_1 > \cdots > r_K$. Let $\Psi = \bigotimes_l \Omega_{\operatorname{ran} Q_l}$.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item For every offset, $K \le \bar r$, $\sum_l r_l \le \min(\bar r(\bar r+1)/2,\,16\bar r/\delta)$, the ray stabilizer of $\Psi$ is exactly $H$, the phase on $H$ is the linear character $\prod_l \det(R(\cdot)|_{\operatorname{ran}Q_l})$, and $|\langle\Psi|R(g)^{\otimes\sum_l r_l}|\Psi\rangle| \le 1 - \delta^2/8$ for $g \notin H$.
  \item Except with probability $\bar r/M_0 \le \beta/8$ over $a$, every threshold lies at distance at least $w/(4M_0)$ from the spectrum. Then the ranks $r_l$ can be learned from eigenvalue samples, each $Q_l$ can be applied as a coherent threshold instrument built from density-matrix exponentiation (\arxivid{1608.00281}, Appendix~C, Theorems~1 and~20; \arxivid{2412.02134}, Theorem~2), and $\Omega_{\operatorname{ran}Q_l}$ can be grown from the filtered states $Q_l\rho Q_l/\tr(Q_l\rho)$ by the antisymmetrization instrument of~\cite[Theorem~5 and Remark~6]{BeneWatts2026}, at cost polynomial in $\bar r$, $q$, $1/\delta$, the number of copies and $1/\eps$.
\end{enumerate}
\end{remark}

For~(i), each eigenvalue $\lambda$ moves to $w\max(0,\lfloor\lambda/w - a/M_0\rfloor) \in (\lambda - 2w, \lambda]$, where $t_j = w(1 + a/M_0 + j)$, so $\tilde\rho = w\sum_j \mathbf{1}[\rho \ge t_j]$ satisfies $0 \le \tilde\rho \le \rho$ and $\tr(\rho - \tilde\rho) < \delta/8$. An element fixing every $Q_l$ fixes $\tilde\rho$, so it moves $\rho$ by less than $\delta$ and lies in $H$. For $g \notin H$, $\mathrm{TD}(\tilde\rho, R(g)\tilde\rho R(g)^\dagger) > 7\delta/8$, so some $Q_l/r_l$ moves by more than $7\delta/8$, and the principal-angle bound of Theorem~\ref{thm:subspace-source}(i) applies to that factor. For the growth step, a retained pure state $\psi \in \wedge^k V$ with one-body density $\gamma_\psi$ is accepted with probability $(1 - k\tr(\rho\gamma_\psi))/(k+1) \ge w(r-k)/(k+1)$ when $\rho \ge w\Pi_V$; since $\wedge^r V$ is a line, the output is exactly $\Omega_V$, and comparison with $r$ coupons of probability $w/r$ bounds the timeout by $re^{-Nw/r}$. Feeding $\Psi$ to the four steps above in place of $\Omega_V$, with $\gamma = \delta^2/8$ and $\sum_l r_l$ registers in place of $r$, would extend Corollary~\ref{cor:subspace-hsp} to nonflat $\rho$; the same offset must be used for every copy, or the character changes between the points of one design block. This extension is argued, not simulated. Part~(i) was checked exactly on the grid and margin identities and in floating point on permutation actions of $S_4$, $D_4$, $C_5$ and $S_3 \times C_2$ (\file{research/audits/reviews/2026-11-02-rees-cited-notes.md}, Section~3); the threshold instrument in~(ii) is a composition of the cited results that has not been checked line by line, and nothing here has had human review. An overstated $\delta$ can make a non-symmetry fix every flag, so the global gap cannot be dropped.
```

Status: argued (i proved), AI-checked only. The integrator may shorten the proof
paragraph. If space is tight, keep only the first sentence and give the status
"checked by an AI session (… Section 3), not by a human".

**P3. Corollary fpt-r source paragraph, line 572.** Optional. After "needs no
random-column argument." add

```latex
Its source factor is $\prod_{d=2}^c(\gcd(d,p-1)+1)^{g_d} \le \prod_{d=2}^c(d+1)^{g_d} \le (r+2)^{r(r+1)/2}$, one scalar diagonal equation per public central line, solved by van de Woestijne's deterministic algorithm as in Schedule~1; it uses no label law.
```

Status: unchanged (conditional on the core composition).

**P4. Remark filters (i), line 717.** Replace

> The symmetry problem becomes a vector stabilizer for the faithful representation $g \mapsto \diag(g, \rho_W(g))$; $\rho_W$ alone can have a large kernel.

with

```latex
The symmetry problem becomes a vector stabilizer for the faithful representation $g \mapsto \diag(g, \rho_W(g))$, which fixes $(0, e_F)$ exactly when $g$ fixes $F$; $\rho_W$ alone can have a large kernel (for $F = x_{D-2}$ under $\UT_D(\Fp)$, $\dim W = 2$ and $\ker\rho_W$ has index $p$).
```

**P5. Remark filters (ii), line 718.** Replace

> Also $K \ne H$ is possible: in the note's iterated-map family with $T = p$ iterations, every anchored $2$-jet is inconclusive.

with

```latex
Also $K \ne H$ is possible: in the note's orbit-sum family $P(u,w) = (u + q(w),\, w + Q(w))$ with $\ell = \sum_i u_i$ and $T = p$ iterations, every fixed-anchor $2$-jet, extension anchors included, is $\ell$ plus a constant, and $K \supsetneq H$ in the note's $p = 7$ control. For the tangent family $P = x + Q$ at $T = p$ only the jet at the origin degenerates, and a fixed anchor resolves the note's $p = 7$ control.
```

**P6. Remark filters (iii), line 719.** Replace the last two sentences

> Canonical gauge fixing is not available over $\Fp$. The implementation covers only actions whose common nilpotent algebra has index at most $p$.

with

```latex
Gram-matrix support recovery is not available over $\Fp$, which has isotropic vectors, so the note uses exact flattening ranks. The implementation covers only odd $p$, and it requires every augmented stage action, not only each site action, to have common nilpotent algebra of index at most $p$.
```

**P7. Closing paragraph, line 723.** Replace

> and the gradient recognizer for the Moore-form family that defeats the orbit-rank cap (\file{research/POLYNOMIAL_ORBIT_MODULE_CLASSICAL_FILTER.md})

with

```latex
and the Monte Carlo gradient recognizer for scalar Moore forms, a family whose orbit rank $b^m$ defeats the orbit-rank cap (\file{research/MOORE_GRADIENT_CLASSICAL_FILTER.md}; it assumes a promised $p$-group and imports a subspace stabilizer)
```

P4–P7 keep the remark's heading "conditional on the cited notes" and its sentence "None
of the following is reproved here". Change that sentence to

```latex
None of the following is reproved here; an AI-only check (\file{research/audits/reviews/2026-11-02-rees-cited-notes.md}, Section~6) tested items~(i)--(iii) on small exact instances.
```

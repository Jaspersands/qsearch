# Referee: Theorem HSP23 (free23, every subgroup, no cover) and Theorem F23′ (2026-11-13)

**Status: AI-checked, pending human review.** One hostile AI referee (Claude). Target:
`2026-11-13-rees-free23-all-subgroups.md` and its folder. Context read: the F23 note and its referee (verdicts, §§0–5),
the IS text (`2026-11-05-rees-sde-subquadratic/lit/ivanyos_santha_1503.09016.txt`; the 11-02 copy the target cites
has the same Cor 8 and Prop 7 in a different layout), core `main-core.tex` ll. 95–110, 222, 230, and
`CLASS_THREE_HSP_THEOREM_DRAFT.md` ll. 95–130 and 268–292. My scripts and outputs are in
`2026-11-13-rees-free23-all-subgroups-referee/`. They import nothing from the audited folder, except for the
labelled reproduction in §6. No existing file was edited. Finite checks can only falsify (TRAPS 7).

## Verdict: PROVED WITH FIXES (given cited theorems)

I found no mathematical gap. Every lemma holds as stated. The fixes are about precision and scope, and none changes a
constant or a branch.

| item | verdict |
|---|---|
| Lemma 0′ | **PROVED.** Re-derived; my own exact check, with an independent front end, found 0 failures. |
| Lemma S | **PROVED, given Lemmas L, W, E of F23 read as formal identities** (fix 1). I did not re-derive Lemma E. |
| Lemma C′ | **PROVED.** Re-derived, including the i* = 1 case; my own exact triple-level check found 0 failures. |
| Theorem F23′ | **PROVED given cited theorems.** s(p) ≥ (1−3/p)²(1−1/p) re-derived; the arithmetic is correct. |
| Lemma T (13 types) | **PROVED.** Re-derived by hand. GAP counts at group level match all 13 formulas at p = 5 and 7. |
| P1–P7 and the branch logic | **PROVED.** An exhaustive run over all 1901 and 6453 subgroups found 0 certified-wrong outputs. |
| IS Cor 8 usage (types 8, 10) | **Hypotheses hold** (§1). The IS state form was verified exactly in 1.24·10⁶ states. Caveats: fixes 2 and 3. |
| Theorem HSP23 | **PROVED WITH FIXES, given cited theorems** (fixes 1–5). |
| §E (free33) | **PROVED** for the structural claim. The "Route A breaks" consequence is about this method only. |

**Fixes.**
1. **Lemma S, step 6.** State that Δ_tot(w_0, τ; θ) ≡ μ(θ)τ is an identity in the polynomial ring over F_p in
   w_0, τ, θ and the outcome variables (j, k, X), obtained from the written derivation of Lemma E. It cannot come
   from a density argument. At p = 5, 288 of 300 runs contain a spoiled copy, and for small p every direction e is
   spoiled for some used copy. The target relies on the derivation, but says so only in its self-check.
2. **Exact QFT is needed for "every certified output is correct".** The certification step proves ŝ ⊆ s. The
   inclusion ŝ ⊇ s holds only because exact Fourier samples lie in s^⊥.
   * With an approximate QFT_p, one bad sample gives ŝ ⊊ s. Certification still passes, and the branch can then be
     wrong. Example: a type-10 H with ŝ = F_pq goes to step 3. If e ∦ g_0, IS then runs outside its promise (|H/⟨q⟩| = p²), and a certified ĥ ∈ H gives the output span(log ĥ, q) ⊊ h.
   * So the "never wrong otherwise" and one-sided claims are exact only under the stated exact-QFT hypothesis.
     Under an approximate QFT, a completeness error of O(N_samples·ε) must be charged. The CLASS_THREE draft makes
     the same point (ll. 127–129).
3. **IS wording.**
   * IS Theorem 5's proof is a sketch in the source (l. 1023: "Proof of Theorem 5 (sketch)"). Cite it as such in the
     theorem's dependency list, not only in the self-check.
   * IS state polynomial *time*. They state no O(1) query count. HSP23's "O(1) otherwise" should read "poly(log p)
     (IS); constant in p plausible, not extracted".
   * IS Definition 4 uses right cosets (l. 184), while Prop 7's proof (l. 955) and HSP23 use left cosets. This is
     harmless (invert g), but say so.
4. **Candidate form in the IS steps.** Certification must be applied to ĥ = n_v·b, which has chart coordinate
   x = 1, as IS's output v = v(1) gives. A candidate in ⟨q⟩ (or γ_3) passes f(ĥ) = f(1) trivially, and would then
   make step 3 output s for a type-8 H. Implicit in the target; make it explicit.
5. **Cap the IS run when its promise fails.** For types 2 and 4, H̄ is trivial, which is outside IS's family
   (order-p subgroups not in N̄, l. 249). IS's running-time bound then does not apply. Run IS with the cutoff of its
   promised bound, then certify. The same holds for Route A on trivial H, which already has bounded time.

**Consequence for the core paper.** No sentence of `main-core.tex` becomes false.
* Item (2) at l. 104 is about H-preserving automorphisms. HSP23 uses none, and does not contradict it.
* L. 222 ("we know of no earlier method") still holds literally.
* The DRAFT remark at l. 230 would become outdated after human review: "It covers only this promise", "p ≥ 5000",
  and the brute force. Free23 would then no longer be an example that *needs* the cover. It would only show that
  automorphism alignment fails.
* I have not edited the paper. The gates stay false (§8).

## 1. IS Cor 8: what it says and whether it applies

**What IS state** (local text, line numbers of the 11-05 file).
* Cor 8 (l. 262) concerns HSP(G, 𝓗) for G = F_p ⋉ F_p^m of constant class.
* 𝓗 is the family of order-p subgroups not contained in the normal subgroup 0 × F_p^m (l. 249; l. 847 in Prop 7's
  proof).
* The oracle is the standard one (Definition 4, l. 179).
* Prop 7 (l. 257) reduces it to HPGP′(F_p, 1, m, d) through the chart M_B(x, v) = n_v k^x. The left cosets of H_v are
  {M_B(x, u + v(x))} with v(x) = Σ_{k<x} B^k v.
* Thm 5 then solves HPGP′. Its proof, a sketch, assumes p > d, with p ≤ d handled through [10].
* No normality of H is needed. The promise is "order p, not in N".

**Type 8 in G/⟨q⟩.**
* L/F_pq has dimension 4 and class 3 for every q ∈ γ_3 \ 0. It is filiform.
* N̄ = (F_pg_0 + γ_2)/F_pq is an abelian ideal of codimension 1, because [g_0, Z] = q. And b = exp(x′) with
  x′ ∉ F_pg_0 + γ_2 is a complement.
* So G/⟨q⟩ ≅ F_p ⋉_B F_p³ with (B − I)³ = 0, B^p = I and class d = 3 < p.
* H/⟨q⟩ has order p, and η̄ ∉ N̄ because e ∦ g_0, which is equivalent to q ∦ [e,Z]. Hypotheses hold.
* The oracle f̄(g⟨q⟩) = f(g) is well defined and hides H/⟨q⟩ exactly, because ⟨q⟩ ≤ H and ⟨q⟩ is central.
* Mapping a coset state of H to the chart gives a uniform state on ḡH̄ times a uniform fibre over ⟨q⟩, which is
  discarded.

**Type 10 in G/γ_3 ≅ heis.**
* Here N̄ = M_{g_0}/γ_3 with a public random g_0, of class 2, and H/γ_3 is order p and not in N̄ when g_0 ∦ e.
  Hypotheses hold.
* When g_0 ∥ e, the AbHSP on M_{g_0}/γ_3 catches it first.

**The H ∩ γ_3 quotient step (brief item 2).**
* ⟨q⟩ = H ∩ γ_3 is obtained from the step-1 AbHSP and certified ⊆ H by queries before it is used. It is central,
  hence normal.
* The quotient oracle is a valid hiding function. No Hγ_3 or other non-normal subgroup is quotiented. K̂ is used
  only through left cosets, as in F23 fix 2.
* M_{g_0} depends on H through q, but it is only *restricted* to, which is legitimate for any subgroup.
* No normalizer appears. This is not the frozen-normalizer error.

**Exact check** (`hsp23_indep.py`; quotient coset states built from f alone).
* Each state was mapped to the chart and asserted to be Σ_x|x⟩|u + v(x)⟩ with v(x) = Σ_{i<x}B^iv(1), B computed
  publicly.
* 121,475 states at p = 5 and 1,115,602 at p = 7 (type 8), plus 1,008 and 2,885 (type 10): **0 form failures.**
* IS was entered only when the promise held or H̄ was trivial (types 2 and 4). It was never entered on a
  non-trivial H̄ ≤ N̄.

## 2. Spoiled copies: Lemma 0′, Lemma S, Lemma C′, F23′ (rechecked)

**Lemma 0′.**
* λ·e = 0 forces e ∥ g_0. Then H̄ ≤ N_λ, so each coset lies at one chart coordinate x_0.
* The Fourier support is the annihilator of Ad_{x_0}η inside the occupied sector. Expanding Ad to second order gives
  −q′_y(x_0).
* q′_y is linear in j with coefficient h(e) ≠ 0, so there are exactly p outcomes per x_0, and Pr[y] = |R_y|/p².
* The leading coefficient 3A_3 = −(n²/2)h ≠ 0, so |R_y| ≤ 2. Correct.

**Lemma S.**
* The support-line steps (2)–(4) are correct: at most one spoiled copy per triple, parallel lines, consistent
  intersection.
* Step 7 is correct. The spoiled copy does not move along e′, since f(e′) = 0. Its formal increment τcs·q′(x_0) is
  0 at the true θ. The higher terms carry f(e) = 0.
* Step 6 is the formal-identity claim; see fix 1.
* The mixture over the two roots of R_y is harmless. Both branches have support parallel to e′ and the same public
  slope μ(θ_true).

**Lemma C′.**
* D_l is a function of the level-2 coset, because Σu_j²P_2 = 0 makes it invariant under a_j ↦ a_j + u_jw.
* The coupling with independent a_j ~ |χ_j|² is the correct coset law.
* The three cases are correct. In the case i* = 1, P_2 ∥ λ_1 ⇔ s_2 = s_3, and then κ = s_1(s_1 − s_2), so the
  coefficient of r is s_1 − κ/s_1 = s_2 ≠ 0. This sharpens the target's "κ ≠ s_1²".
* **The relative sign of the r and P_2·a terms is intrinsic.** It comes from Σ_is_in_iX_i. It is also essential:
  with the opposite sign, uniformity fails when 2s_1 = s_2.
* The target's displayed form −Σu_j[s_{j1}r_j + P_2·a_j + Σs k] flips the k-sign relative to F23's
  D = Σu Σs(nX − k). That is CONV (j,k) → −(j,k), and it does not affect uniformity.

**F23′.**
* Runs are independent given H, so Pr[both C ≠ 0] ≥ (1−3/p)².
* Lemma R(b) is unaffected, because α is uniform given σ(H) and the run's randomness. So Pr[proportional | both
  C ≠ 0] = 1/p.
* The η_c step and the oracle verification do not depend on λ·e.
* s(5) = 0.128, s(7) = 0.280, s(11) = 0.481, s(13) = 0.546, s(5000) ≥ 0.9986.
* The p ≡ 2 mod 3 Lemma-B case at p = 5 works (cubing is bijective, conics have ≥ 4 points).

**My exact checks** (`frontend_check.py`; my own front end, written from the definitions).

| p | sign convention fitted on non-spoiled copies | spoiled instances (all base points) / y-blocks | diag / support = R_y / weights / Pr[y] / Ad-form fails | triples with a spoiled copy | g = s_1r + P_2·a non-uniform | sign-flipped control non-uniform |
|---|---|---|---|---|---|---|
| 5 | (−1, −1, 1), unique of 8 | 40 / 600 | 0 / 0 / 0 / 0 / 0 | 300 (i* = 1: 169; s_2 = s_3 at i* = 1: 121) | **0** | 31 |
| 7 | (−1, −1, 1), unique of 8 | 8 / 224 | 0 / 0 / 0 / 0 / 0 | 200 (122; 92) | **0** | 12 |

* The independently fitted convention equals the target's CONV.
* The control shows that the test can fail.

## 3. Classification (brief item 4)

**By hand.** Lemma T (d_1 = 0, 1, 2; ad_η-invariance of s) is correct. The 13 counts sum to 1901 at p = 5.

**GAP** (`gap_count.g`, `.out`; 1.7 s, 0.15 GB).
* G = ⟨a,b | a^p, b^p⟩ modulo lower exponent-p class 3. This group is regular, hence of exponent p, and has order
  p⁵, class 3 and exponent p, as checked.
* Invariants of each subgroup: (|H|, |H∩γ_2|, |H∩γ_3|, [H,γ_2] ≤ H).
  * p = 5: 1901 subgroups, 13 classes.
  * p = 7: 6453 subgroups, 13 classes.
* Every class count equals the formula of its type: 1, p+1, p², 1, p(p+1), 1, p³(p+1), p³(p+1), p²(p+1), p(p+1),
  p²(p+1), p+1, 1. The last invariant separates types 8 and 9.
* My own subalgebra enumeration (`hsp23_indep.py`) also gives 1901, and every exp(h) passes a subgroup check.

## 4. Type identification (brief item 5)

The algorithm never needs to know the type in advance.
* The branch is a function of s and T only. Both come from Las Vegas AbHSP, which is exact, with fix 2.
* Inside a branch, the only ambiguities are trivial versus hard cyclic (step 2), type 2 versus type 8 (step 3), and
  type 4 versus type 10 (step 4).
* Each is resolved by running the sub-algorithm and certifying it, with the smaller subgroup as the default. A
  failed sub-algorithm can therefore only return a proper subgroup of H.
* A wrong branch is impossible under exact QFT, and is not merely caught by certification.

## 5. Independent end-to-end check over every subgroup (falsification only)

**Set-up** (`hsp23_indep.py`; `hsp23_indep_{5,7}.out`; 23 s and 556 s, ≤ 0.13 GB).
* f is an explicit left-coset table.
* AbHSP uses exact one-coset-state Fourier sampling and Las Vegas certification.
* The IS branch uses the quotient states of §1. The HPGP′ solver is replaced by a brute-force candidate elimination
  that uses only exact measurement statistics. It is a correct small-p solver; IS Theorem 5 is not tested.
* Route A is replaced by a stand-in: the true generator with probability ½ per attempt if H is hard cyclic,
  otherwise an adversarial random candidate, 6 attempts. Then classical certification.

**Results.**
* **Every** subgroup was run: 1901 at p = 5 and 6453 at p = 7.
* **0 certified-wrong outputs.**
* The only wrong outputs are the type-7 one-sided defaults (output 1 ⊊ H): 10/750 at p = 5 and 31/2744 at p = 7.
  These are expected from the stand-in, at rate 2^{−6}.
* Branch usage matched the table for every type. For type 10, the M_{g_0}/γ_3 branch was hit 1/30 times at p = 5
  and 9/56 at p = 7.

**What this does not test.** Route A itself, IS Theorem 5, large p, and approximate gates.

## 6. Route A with unconditioned labels: labelled reproduction (not independent)

I re-ran the target's `e2e_spoiled.py`, which drives the F23 referee's simulator, with fresh seeds.

| p | attempts | success | wrong output | equations held | spoiled runs checked (line / phase fails) | D_l = 0 (clean / spoiled) | C forced 0 |
|---|---|---|---|---|---|---|---|
| 5 | 60 | 22 (0.37; bound 0.128) | 0 | 93/93 | 85 (0 / 0) | 36/135, 32/225 (1/p = 0.2) | 27/120 runs |
| 7 | 12 | 8 | 0 | 21/21 | 16 (0 / 0) | 4/36, 7/36 | 3/24 |

* The p = 5 success rate (0.37) is lower than the target's 0.55, within about 2σ.
* The D_l = 0 rate summed over clean and spoiled states is 68/360, against 72 expected.

## 7. Other items

* **§E (free33).** A codimension-1 ideal contains [L̄,L̄], so it equals W + γ̄_2. Then [w_1,w_2] ∉ γ_3 ⊇ ker λ, so
  the ideal is not abelian. Correct. "Largest abelian normal subgroup that works for all λ" is unchecked: for
  special λ an index-p² abelian ideal may exist. Immaterial.
* **H-dependence audit (§B3).** Correct. See §1.
* **Theorem R consistency (§B2).** Not re-audited. Nothing in HSP23's proof uses it.
* **The target's own outputs.** `e2e_spoiled_{5,7}.out`, `spoiled.out`, `classify_7.out` and `hsp_all_*.out` match
  the numbers in its §§A, B and D.

## 8. Claim gates and next question

* **Gates stay false.** "Cover unnecessary for free23", novelty, priority and speedup all wait for human review.
  The core paper is not to be edited on the strength of AI review.
* **Strongest counterexample or baseline.** None found. HSP23 reduces to F23′ plus standard or cited pieces, as the
  target says.
* **Next hard question** (unchanged). Is there a multivariate aligned merge for free33, whose N_λ is non-abelian?
* **For the integrator.**
  * Apply fixes 1–5 to the target note.
  * A human should check Lemma E's derivation as a formal identity. Lemma S, and therefore F23′ at small p, rests
    on it.

## 9. Adversarial self-check

* **I did not re-derive Lemma E or Lemma W.** Lemma S inherits them. The exact line and phase checks (227 + 85
  spoiled runs at p = 5) use the F23 referee's simulator, not mine.
* **My Route-A and IS stand-ins cannot fail in the way the real algorithms might.** My end-to-end run tests the
  decision logic, the oracle constructions, the IS state form, the promise bookkeeping and the certification. It
  does not test the two cited sub-algorithms.
* **Lemma C′ check scope.** My check covers the per-triple statistic g_j for fixed realisations. It does not test the
  D_l closed form itself, which is Lemma C0, checked by the authors (C0_closed_form_fail = 0).
* **The GAP construction.** It relies on regularity: class < p and generated by elements of order p implies
  exponent p. The printed order p⁵, class 3 and exponent p confirm it.
* **IS was read from the arXiv v2 text only**, not the journal version. Thm 5 is a sketch there.
* **Fix 2 might be called pedantic,** since the theorem assumes an exact QFT. I list it because the target's
  one-sided claim is the kind of statement a later summary might repeat without the exact-QFT hypothesis.
* **Small p only** (5, 7). Nothing here is evidence for large p beyond the proofs.

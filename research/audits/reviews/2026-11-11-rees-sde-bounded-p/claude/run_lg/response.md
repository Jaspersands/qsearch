# Referee report: Lemmas K, V, 1, Theorems LG, LG_R, Corollaries 1–2

**Summary.** I found no counterexample to any claim. Lemmas K, V and 1 and Corollary 2 hold as stated. Theorem LG has one wording defect, and its proof is correct. Corollary 1 needs one missing argument to use the p = 7, 11 inputs for the full set. Theorem LG_R has a real logical gap: "W has dim R" is not proved. The gap is repairable, and the stated conclusion survives. Throughout, "family" means feasible family. Every argument below uses feasibility (y_α ∈ S); the claims should say so.

The cheapest attack was a consistency check, not a counterexample. At p = 5, F_5^2∖0 has a weakly nondegenerate 2-family. This is consistent with everything:
- Lemma 1 holds (each K_u has codim ≤ 1).
- The K_u cannot all coincide.
- LG's hypothesis fails for that very section.

At p = 3, k = 1, the quotient F(L)/Lin(L) is 1-dimensional, so Lemma 1 is immediate there. I found no tiny counterexample to any claim.

## Lemma K — ACCEPT
- **Linearity.** For α ≠ 0, y_α − Σ α_j y_{e_j} = ⟨γ_α − Σ α_j γ_{e_j}, l⟩. With y_0 = 0, the map α ↦ [y_α] is linear.
- **Kernel.** α ∈ K iff y_α|L is linear and S-valued, hence 0. Read "no nonzero S-valued functional" as: f(L) ⊂ S ⇒ f|L = 0.
- **Nondegeneracy.** λα ∈ K ⇔ α ∈ K, so [α] is degenerate iff α ∈ K.

## Lemma V — ACCEPT
- y_{rα} − r y_α = ⟨Δ_α, ·⟩ holds for any family. The Lemma R normalization is not used.
- S ∩ r^{-1}S = {0} because r^{-1} ∉ P.
- For the line statement, adjoin α = 0 to the set.
- The converse direction correctly uses that the line has no S-valued functional (κ ≥ 2) and that K is a subspace.

## Lemma 1 — ACCEPT (point (a), point (b))
**(a) Reparametrization.** Set Φ'(l) = (y_{Be_1}(l), y_{Be_2}(l)) ∈ S² by feasibility, and γ'_β = γ_{Bβ} − Σ β_j γ_{Be_j}. Then:
- y_{Bβ} = ⟨β, Φ'⟩ + ⟨γ'_β, l⟩ exactly, because ⟨Bβ, Φ⟩ − Σ β_j ⟨Be_j, Φ⟩ = 0.
- The family is feasible.
- β ∈ K' ⇔ y_{Bβ} ∈ Lin ⇔ Bβ ∈ K, so K' = B^{-1}(K).
- An injective B whose image meets K trivially exists iff codim K ≥ 2.

Note that BᵀΦ need not lie in S², so defining Φ' from the y-values (as the proof does) is necessary.

**(b) Equivariance and dimension count.**
- F_p^* (k = 1) spans and has no S-valued functional, so Q/N applies. Q/N preserves nondegeneracy (it depends on γ only) and makes Φ' P-equivariant.
- Then y'_β(λl) = λ y'_β(l) for λ ∈ P.
- The P-equivariant functions on F_p^* have dimension equal to the number of P-cosets, which is 2.
- Lin is 1-dimensional, so β ↦ [y'_β] maps F_p² into a 1-dimensional space. Its kernel is nonzero, a contradiction.

## Theorem LG — ACCEPT WITH FIX (wording only) (point (c), point (d))
**Fix.** Read "two distinct u, w ∈ FL" as "u, w spanning distinct full lines." For u, w on the same line, span(u, w) is not a plane and the hypothesis is meaningless; K_u = K_w trivially in that case.

**Proof check.**
1. **No S-valued functional on L.** Such a functional is S-valued on each full line, hence 0 there (κ ≥ 2). Since FL spans, it is 0.
2. **Restriction.** If y_α|_{L∩W} is linear, so is its restriction to l_u. Hence K(L∩W) ⊆ K_u ∩ K_w.
3. **Lemma K on L∩W.** L∩W contains two independent full lines, so it spans W and has no S-valued functional. Lemma K applies (in coordinates on W; ⟨γ, l⟩|_W is a functional on W).
4. **Reparametrization on L∩W.** If codim K(L∩W) ≥ 2, the reparametrization gives a weakly nondegenerate 2-family on L∩W, excluded by hypothesis. So codim(K_u ∩ K_w) ≤ 1.
5. **(d)** The hypothesis is invoked only for such two-line sections.
6. **(c) Common hyperplane.** Two distinct hyperplanes would intersect in codimension 2. So all hyperplane K_u are equal, say to H. The other K_u equal F_p^d ⊇ H. If no K_u is a hyperplane, any H works. If d = 1, then H = 0 and the claim is trivial.
7. **H ⊆ K(L).** Take α ∈ H.
   - α and rα lie in every K_u, so y_α and y_{rα} vanish on full lines (Lemma K on lines).
   - g = y_{rα} − r y_α = ⟨γ_{rα} − rγ_α, ·⟩ is a global functional vanishing on spanning lines, so g = 0.
   - Then y_α(l) ∈ S ∩ r^{-1}S = {0}.
   - So H ⊆ K(L), and codim K(L) ≤ 1.
8. **Last clause, S-witness.** x ∈ D(X) means x_i = ⟨c, l_i⟩, an S-valued functional on L, so x = 0. Zero-label columns give x_i = 0 automatically.
9. **Last clause, 2-dim subgroup.** Lemma 2(B) applies. See (f) below for the per-label step.

## Corollary 1 — ACCEPT WITH FIX
**Planar sections.** For the full set, every planar section is W∖0. For the nested set, every plane through two lines off {l_1 = 0} meets it in {l ∈ W : l_1 ≠ 0}. A GL_2 change of coordinates sending l_1|_W to the first coordinate makes this the nested planar set. Families transfer under coordinate change (γ ↦ transpose action).

**Gap.** The p = 7, 11 certificates concern the nested planar set only. "Subset has none ⇒ full set has none" is not automatic: restricting a family to a subset can destroy weak nondegeneracy. The fix holds:
- The nested planar set's full lines span F_p².
- So if α ∈ K(nested), then y_α and y_{rα} vanish on those lines.
- The step-7 argument above then gives y_α = 0 on all of F_p²∖0.
- Hence K(nested) ⊆ K(full), and a weakly nondegenerate family on the full set restricts to one on the nested set.

This argument must be added.

**Other points.**
- "Every d ≥ 2" is consistent: realizing a d-dimensional subgroup includes realizing ⟨h_1, h_2⟩.
- p = 13 remains conditional on proof checking, as stated.

## Theorem LG_R — ACCEPT WITH FIX (real gap)
**Equality K(L) = ∩ K_u is fine.** It holds whenever the full lines span, by the step-7 argument. The bracketed "union of full lines" caveat is unnecessary. Lemma 1 gives dim K_u^⊥ ≤ 1.

**Gap.** "Choose R full lines with independent n_u; their span W has dim R" is unjustified. Independence of the n_u ∈ (F_p^d)* does not imply independence of the u ∈ F_p^k. For example, u_3 ∈ span(u_1, u_2) with n_{u_1}, n_{u_2}, n_{u_3} independent would mean rank 3 on a planar F_p²∖0. Nothing given excludes that.

**Fix.** All that is needed is K(L∩W) ⊆ ∩ K_{u_i}, which holds by restriction, so the rank on L∩W is ≥ R.
- **k ≥ R:** take any R-dimensional W' ⊇ span(u_i). Then L∩W' = W'∖0, and rank ≥ R there. Reparametrize with B as in Lemma 1 to get a weakly nondegenerate R-family on F_p^R∖0.
- **k < R** (the claim says "for every k"): lift.
  - Let π: F_p^R → F_p^k be a coordinate projection.
  - Set Φ'(l) = Φ(πl) and γ'_α = πᵀγ_α when πl ≠ 0, and Φ'(l) = 0 on ker π ∖ 0.
  - The lift is feasible, since y'_α = 0 on ker π.
  - α ∈ K' gives y'_α = 0, hence y_α = 0, so K' ⊆ K and the rank is ≥ R on F_p^R∖0.

With this fix, the p = 5, R = 3 conclusion holds, conditional on the F_5^3 certificate.

## Corollary 2 — ACCEPT (point (e))
- With c_i = ⟨t, l_i⟩, c is supported in X iff t ∈ U^⊥, U = span(labels outside X). So D(X) ≅ U^⊥ and k = r − dim U.
- The labels of X are the images of l_i in (U^⊥)* ≅ F_p^r/U.
- Every point of F_p^r ∖ U is some pool label, and it is not outside X, so the images cover (F_p^r/U)∖0.
- X-labels lying in U become zero labels, which is consistent.
- Multiplicities and zero-label pool columns are harmless.

## (f) Multiplicities
Lemma 2(B) produces per-column Φ_i, while LG and the Corollaries are stated for per-label Φ. The reduction is valid whenever L spans and has no S-valued functional; this holds in LG and in both Corollaries.
- At column level, Lemma K still gives: degenerate ⇔ y_α ≡ 0 on columns.
- Lemma V's argument gives: degenerate ⇔ Δ_α = 0, using that L spans.
- So keeping γ and taking Φ from one representative column per label preserves feasibility and exactly the degenerate directions.

No claim silently needs one column per label. Corollary 2 is multiplicity-agnostic.

## Weakest step
LG_R's "span W has dim R," which is false as an inference but repaired above. Next weakest is Corollary 1's nested→full transfer, which is missing but true by the argument given. Finally, the p = 13 and F_5^3 inputs rest on certificates; p = 13 is flagged as unchecked.
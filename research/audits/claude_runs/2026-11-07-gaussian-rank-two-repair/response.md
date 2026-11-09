**Verdict on the lemma: TRUE, with C = 1.52 (any δ<1/100); the √δ exponent is tight (C ≥ 0.99 is forced). Proof below is complete; the corollary follows conditionally with obligations listed.**

## 1. Lemma — proof

Notation: a∧b := ab^T − ba^T.

**Fact A (operator norm of a wedge).** For a,b ∈ R^N, ‖a∧b‖ = |a|·|b_⊥| ≤ |a||b|, where b_⊥ = b − ⟨a,b⟩a/|a|². Proof: a∧b = a∧b_⊥; on span{a,b_⊥} it equals |a||b_⊥|·J with J a rotation generator (J² = −I, ‖J‖=1), and it vanishes on the orthogonal complement. Equality ‖a∧b‖ = |a||b| when a ⊥ b.

**Fact B (normal form).** A real skew matrix of rank ≤ 2 is 0 or s·u∧v with u,v orthonormal, s>0 (rank 1 is impossible for skew). For any rotation u' = cu+σv, v' = −σu+cv (c²+σ²=1), u'∧v' = u∧v, so the representation is invariant under orientation-preserving rotation of the plane P = span{u,v}.

**Step 0 (s = 0).** B = 0 ⇒ ‖D‖ ≤ δ; take B0 = 0: ‖D−B0‖ ≤ δ ≤ √δ. Done.

**Step 1 (size).** s = ‖B‖ ≤ ‖D‖ + δ ≤ 2+δ.

**Step 2 (reference wedge).** R B R = s·(Ru)∧(Rv) (using R = R^T), and ‖RBR‖ ≤ ‖R‖‖B−D‖‖R‖ + ‖RDR‖ ≤ δ.

**Step 3 (rotation).** The symmetric bilinear form (x,y) ↦ ⟨Rx,Ry⟩ = ⟨x,Ry⟩ restricted to the 2-plane P is diagonalized by an orthonormal basis of P (spectral theorem for the 2×2 symmetric compression of R to P). Choosing its orientation, by Fact B we may assume Ru ⊥ Rv. The rotation is needed: without it ‖(Ru)∧(Rv)‖ = |Ru||(Rv)_⊥| can be small while both |Ru|,|Rv| are large (nearly parallel reference parts).

**Step 4 (product bound).** By Fact A with Ru ⊥ Rv: s|Ru||Rv| = ‖RBR‖ ≤ δ. WLOG |Ru| ≤ |Rv|, so s|Ru|² ≤ δ, i.e. |Ru| ≤ √(δ/s).

**Step 5 (deletion).** Put u0 := (I−R)u (not normalized), B0 := s·u0∧v. Then B0 is skew, rank ≤ 2 (decomposable), and R B0 R = s·(Ru0)∧(Rv) = 0 since Ru0 = 0. Change: B − B0 = s·(Ru)∧v, so by Fact A ‖B−B0‖ ≤ s|Ru||v| ≤ s√(δ/s) = √(sδ).

**Step 6 (constant).** ‖D−B0‖ ≤ δ + √((2+δ)δ) = √δ(√δ + √(2+δ)) ≤ √δ(0.1 + 1.418) ≤ 1.52√δ for δ<1/100. C is independent of N, R, and no small singular value is inverted. (Degenerate sub-case u0 = 0: then u ∈ ran R, |Ru| = 1 ≤ √(δ/s) ⇒ s ≤ δ, B0 = 0, and the bound still holds.)

## 2. Tightness (exponent ½ is necessary)

N=4, R = projection onto span{e1,e2}. Let u = √δ e1 + √(1−δ) e3, v = √δ e2 + √(1−δ) e4 (orthonormal), B = u∧v, D := B − RBR = (1−δ)e3∧e4 + √(δ(1−δ))(e1∧e4 − e2∧e3). Then RDR = 0, ‖D‖ ≤ 1+δ ≤ 2, ‖D−B‖ = ‖δ e1∧e2‖ = δ. For any admissible B0 = s·w1∧w2 (rotated so Rw1 ⊥ Rw2), RB0R = 0 forces s=0 or Rw1=0 or Rw2=0, hence the off-diagonal block R B0 (I−R) = −s·Rw2·((I−R)w1)^T has rank ≤ 1. But R D (I−R) = √(δ(1−δ))(e1e4^T − e2e3^T) has both singular values √(δ(1−δ)). By Eckart–Young, ‖D−B0‖ ≥ ‖R(D−B0)(I−R)‖ ≥ σ2(RD(I−R)) = √(δ(1−δ)) ≥ 0.99√δ. So 0.99 ≤ C_opt ≤ 1.52.

## 3. Corollary (conditional verification)

**Key exact fact (proved, no approximation).** If Γ2′ = Γ1 − B0 with B0 skew of rank ≤ 2, then for every principal index set S, Pf((Γ1 − tB0)_S) is affine in t: writing Pfaffians as top components of exp(ω_A + tω_W) in the exterior algebra, ω_W∧ω_W = 0 for decomposable ω_W (restriction of a rank-2 wedge to S is still a wedge), so exp(ω_A + tω_W) = exp(ω_A)(1 + tω_W). Since all 2m-point correlators of a Gaussian state are such Pfaffians (odd ones vanish for both states and the mixture), **p ρ_{Γ1} + q ρ_{Γ1−B0} = ρ_{Γ1−qB0} exactly**, a Gaussian state; it is physical because it is a convex combination. Side remark: for general Δ the 4-point defect of the mixture is p Pf(Γ1)+q Pf(Γ2) − Pf(Γ̄) = pq Pf(Δ_S) = (pq Δ∧Δ)_S, i.e. H is exactly the 4-point non-Gaussianity — consistent with the hypothesis.

**Case min(p,q) ≤ k⁸** (say q): ‖pΦ1+qΦ2 − Φ1‖⋄ ≤ 2q ≤ 2k⁸, and ‖Γ̄−Γ1‖ = q‖Δ‖ ≤ 2k⁸, so the single-Gaussian bound gives ‖Φ1 − Φ_Γ̄‖⋄ ≤ 200n√(2k⁸) ≤ 283 n k⁴. Total ≤ 2k⁸ + 283nk⁴ = O(nk).

**Case min(p,q) ≥ k⁸:** pq ≥ k⁸/2, so ‖Δ∧Δ‖ ≤ 6k⁸. With singular pairs σ1 ≥ σ2 ≥ … of Δ, σ1σ2 ≤ ‖Δ∧Δ‖ (see normalization below), so the top-pair truncation B (rank 2) satisfies ‖Δ−B‖ = σ2 ≤ min(σ1, 6k⁸/σ1) ≤ √6 k⁴ =: δ. If k ≥ 1/4 the O(nk) bound is trivial (diamond ≤ 2 ≤ 8nk); otherwise δ < 1/100, and D := Δ satisfies RΔR = 0, ‖Δ‖ ≤ 2. The lemma gives B0 with RB0R=0, ‖Δ−B0‖ ≤ 1.52√δ ≤ 2.4k². Set Γ2′ := Γ1 − B0: RR-block zero (reference marginal maximally mixed ⇒ trace-preserving Choi), ‖Γ2′−Γ2‖ ≤ 2.4k², and I ± iΓ2′ ≥ (k − 2.4k²)I ≥ 0 for k<1/4. Then
‖pΦ1+qΦ2 − Φ_Γ̄‖⋄ ≤ q‖Φ2−Φ2′‖⋄ + ‖Φ_{Γ1−qB0} − Φ_Γ̄‖⋄ ≤ 2·200n√(2.4k²) ≤ 620 n k,
using the exact fact for the middle equality pΦ1+qΦ2′ = Φ_{Γ1−qB0}. No supplied p and no gap are used; p enters only through the analysis split.

**Proof obligations / missing normalization (not supplied, must be checked):**
1. Normalization of ‖Δ∧Δ‖: the argument needs ‖Δ∧Δ‖ ≥ σ1(Δ)σ2(Δ). In the normal basis the e1∧e2∧e3∧e4 coefficient of Δ∧Δ equals σ1σ2 (Pfaffian convention) or 2σ1σ2 (ω=Σ_{i<j}Δ_ij e_i∧e_j convention); any norm dominating the max coefficient (operator norm on Λ², Frobenius) works. If "‖H‖" is a smaller norm, the constant 6 changes but not the k-exponent.
2. The single-Gaussian bound 200n√(‖Γ−Γ′‖) must apply to Choi covariances with margin as small as k − 2.4k² and must not need a gap.
3. "Gaussian Choi state with zero RR-block ⇔ Gaussian TP channel" (Choi–Jamiołkowski in the fermionic/parity-superselected setting) is assumed for identifying Φ_{Γ1−qB0} with the mixture channel.

**Falsifiers:** an admissible pair with ‖Δ∧Δ‖ small but σ1σ2 large (would contradict obligation 1 for the chosen norm); a Gaussian pair whose rank-2-difference mixture has a non-Gaussian 6-point correlator (would contradict the exact Pfaffian affineness — I claim impossible); the N=4 example above shows no proof can improve √δ to δ.
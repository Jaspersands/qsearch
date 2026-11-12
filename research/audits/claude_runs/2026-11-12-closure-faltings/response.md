# Conditional arithmetic extension of the Merkl atlas: verdict, proof, ledger

## 0. Verdict in one paragraph

**PROVED, conditionally.** Under the stated analytic hypothesis (H1) (Merkl numbers r₁ = 3/4, n_σ ≤ c_r d(d+L_σ), c₁ ≤ c d², log M ≤ c d for the canonical probability Arakelov measure of every complex fibre Y_σ) together with a structural clause (H2) that I isolate below and verify from the candidate's two chart types by a unitary-Möbius derivative computation, and under the source-inherited results (Theorem 2.4.1, Lemma 2.3.1, Proposition 4.2.4, Theorem 4.3.2, well-definedness of h(b) and ‖Wr‖_Ar), the following holds: for every finite π: Y → P¹ over Q̄ of degree d ≥ 2 with g(Y) ≥ 1, étale outside a Galois-stable set B ⊂ P¹(Q̄) with |B| ≤ r and h_B := max_{β∈B} h(β),

  h_Fal(Y) ≤ C_r d⁵ (d + 1 + h_B),

with C_r explicit in c_r, c, c₀, r (Section 7). No uniform archimedean distance promise, no supplied torsion, no hidden model height, no fixed-X constant is used. The exponential dependence on h_B of the Belyi route is replaced by linear dependence, exactly through two uses of one exact product-formula identity on P¹_{O_K} (Lemma A). What is **not** obtained: any bound on the height of a plane model or of coordinates of Y (the twist family y² = a·x(x−1)(x−2) has constant stable Faltings height but unbounded model height, so stable h_Fal cannot control model data), any torsion module, any Frobenius, any point-counting cost. The remaining risk is entirely in (H1)/(H2) and in the cited source theorems, each listed as an obligation with a falsifier in Section 8.

Everything below is a deduction unless marked **[ASSUMPTION]** or **[NORMALIZATION]**.

## 1. Setting, normalizations, quantifiers

Fix r ≥ 3 (for r ≤ 2 a cover of P¹ branched in ≤ 2 points has genus 0, so the statement is vacuous). Let Y/Q̄ be smooth projective connected of genus g ≥ 1, π: Y → P¹_{Q̄} finite of degree d, étale over P¹ − B, where B is the full Galois orbit closure of the branch locus, |B| ≤ r. Since h is Galois-invariant, h_B equals the maximum over the original branch points. Riemann–Hurwitz gives 2g − 2 = −2d + Σ_x (e_x − 1) ≤ −2d + r(d − 1), hence

  (1.1) g ≤ (r − 2)(d − 1)/2 ≤ r d.

**[NORMALIZATION]** For a number field K: for finite v, |x|_v = #k(v)^{−ord_v x}; for archimedean v, |x|_v = |σ_v x|^{[K_v:R]}, so Σ_{v arch} log|x|_v = Σ_{σ:K→C} log|σx|, and Σ_{all v} log|x|_v = 0 for x ∈ K^×. For P = (x₀:x₁) ∈ P¹(K), h(P) = [K:Q]^{−1} Σ_v log max(|x₀|_v, |x₁|_v); for α ∈ K, h(α) := h((α:1)) = log H(α) with the source's H (lines 108–111). h(∞) = 0. Chordal distance on P¹(C): d_ch(x,y) = |x₀y₁ − x₁y₀| / (‖x‖‖y‖), Euclidean norms; d_ch ≤ 1. For σ: K → C write B_σ = σ(B), δ_σ = min_{β≠β'∈B} d_ch(σβ, σβ'), L_σ = 1 + log(1/δ_σ). t denotes the affine coordinate on P¹; dt is the tautological section of ω_{P¹} with divisor −2[∞]; dπ := π^*dt.

**[NORMALIZATION N1]** (source Section 2.1, not supplied verbatim; standard Arakelov convention) For a local coordinate z at x ∈ Y_σ, log‖dz‖_Ar(x) = lim_{y→x} ( log|z(y) − z(x)| − gr(x,y) ), and for a global orthonormal basis ω = (ω_k = f_k dz) one has log‖Wr‖_Ar(x) = log|W_z(ω)(x)| + (g(g+1)/2) log‖dz‖_Ar(x), with W_z the g×g Wronskian determinant (as used in the supplied proof of Proposition 3.5.1). The canonical form is μ = (i/2g) Σ_k ω_k ∧ ω̄_k, so if μ = i F_j dz_j ∧ dz̄_j then Σ_k |f_k|² = 2g F_j on U_j (supplied, lines 1040–1050).

h(b) for b ∈ Y(Q̄) and ‖Wr‖_Ar(b) are the [K:Q]-normalized quantities of source Section 2.3 **[ASSUMPTION A0: well-defined and field-independent, source cites [36, §5.4]]**.

## 2. Lemma A: exact Arakelov intersection identity on P¹_{O_K}

**Lemma A.** Let K be a number field, P = (x₀:x₁) ≠ Q = (y₀:y₁) in P¹(K), P̄, Q̄ their Zariski closures in P¹_{O_K}, Δ := x₀y₁ − x₁y₀ ≠ 0. For σ: K → C put ϑ_σ(P,Q) := |σΔ| / ( max(|σx₀|,|σx₁|) · max(|σy₀|,|σy₁|) ) ∈ (0, 2]. Then

  (A) (P̄, Q̄)_fin + Σ_{σ:K→C} log(1/ϑ_σ(P,Q)) = [K:Q] ( h(P) + h(Q) ).

Consequently
 (A.a) (P̄, Q̄)_fin ≤ [K:Q] ( h(P) + h(Q) + log 2 );
 (A.b) Σ_σ log(1/d_ch(σP, σQ)) ≤ [K:Q] ( h(P) + h(Q) + log 2 ).

*Proof.* P¹_{O_K} is regular; P̄ ≅ Spec O_K is a section, hence an effective Cartier divisor, and the local intersection number at a closed point over v is (P̄,Q̄)_v = ord_v(ℓ_P|_{Q̄}) where ℓ_P is a local equation of P̄. Choose λ_x ∈ K_v^× with ord_v λ_x = min(ord_v x₀, ord_v x₁) and set x^{(v)} = x/λ_x (v-primitive); then ℓ_P = x₁^{(v)}X₀ − x₀^{(v)}X₁ is a local equation of P̄ at every point of the fibre over v (it is primitive, so its zero locus is exactly the closure). Restricting to Q̄ via (X₀:X₁) = (y₀^{(v)}:y₁^{(v)}) gives ℓ_P|_{Q̄} = −Δ/(λ_x λ_y) up to a unit. Hence

 (P̄,Q̄)_v · log #k(v) = −log|Δ|_v + log max(|x₀|_v,|x₁|_v) + log max(|y₀|_v,|y₁|_v).

Summing over finite v and using the product formula Σ_{v fin} log|Δ|_v = −Σ_σ log|σΔ|, and [K:Q]h(P) = Σ_{v fin} log max|x_i|_v + Σ_σ log max|σx_i|:

 (P̄,Q̄)_fin = Σ_σ log|σΔ| + [K:Q]h(P) − Σ_σ log max|σx_i| + [K:Q]h(Q) − Σ_σ log max|σy_i|
     = [K:Q](h(P)+h(Q)) − Σ_σ log(1/ϑ_σ).

This is (A). ϑ_σ ≤ 2 by the triangle inequality, so Σ_σ log(1/ϑ_σ) ≥ −[K:Q] log 2, giving (A.a). Since ‖x‖ ≤ √2 max|x_i|, d_ch ≥ ϑ_σ/2, so log(1/d_ch) ≤ log 2 + log(1/ϑ_σ); summing and using (P̄,Q̄)_fin ≥ 0 gives (A.b). ∎

*Finite control.* β = 0 = (0:1), a = p/q = (p:q) coprime: Δ = −p, max|y_i|_v = 1 at finite v, so (A) gives (0̄, ā)_fin = [K:Q] log p, which is exactly the source's computation (0+1+∞, Q)_fin = [K:Q] log(pq(q−p)) (lines 1570–1575) restricted to the component 0. The bound (A.a) gives ≤ [K:Q](log q + log 2), consistent with the source's 3 log q after summing three components.

Lemma A is the whole "product formula, not a uniform archimedean distance promise" mechanism: (A.a) controls horizontal finite intersections, (A.b) controls the archimedean collision terms, and both are linear in heights.

## 3. Lemma B: local Merkl comparison ⇒ norm of chart differentials

**Lemma B.** Let ({(U_j,z_j)}_{j=1}^n, r₁, M, c₁) be a Merkl atlas of a compact Riemann surface X of genus ≥ 1 (Definition 3.1.1), and set

  Λ := 330 n (1−r₁)^{−3/2} log(1/(1−r₁)) + 13.2 n c₁ + (n−1) log M.

Then for every j and every x ∈ U_j^{r₁}: |log‖dz_j‖_Ar(x)| ≤ Λ.

*Proof.* Theorem 3.1.2 (supplied, lines 731–737) gives |gr(x,y) − log|z_j(x) − z_j(y)|| ≤ Λ for all x ≠ y in U_j^{r₁}. The function gr(x,y) − log|z_j(x)−z_j(y)| extends continuously (indeed smoothly) across the diagonal of U_j × U_j because gr(x,·) − log|z(·)−z(x)| is smooth near x for any coordinate z. Let y → x inside the open set U_j^{r₁}; by N1 the limit is −log‖dz_j‖_Ar(x). ∎

This is the only analytic input beyond (H); it uses the local statement, not merely sup gr.

## 4. The hypothesis (H) and its structural clause

**(H1) [ASSUMPTION — the Merkl atlas lemma]** There exist constants c_r, c (depending only on r) such that for every σ: K → C there is a Merkl atlas A_σ of Y_σ for the canonical probability Arakelov measure with r₁ = 3/4, n_σ ≤ c_r d(d + L_σ), c₁ ≤ c d², log M ≤ c d.

**(H2) [structural clause]** There is an absolute c₀ ∈ (0,1] such that every x ∈ Y_σ with π(x) ≠ ∞ lies in U_j^{r₁} for a chart (U_j,z_j) of A_σ with

  |d(t∘π)/dz_j (x)| ≥ c₀ · min(1, d_ch(π(x), B_σ)).

**Verification of (H2) from the candidate's chart types.** The candidate atlas (MERKL_LOG_COLLISION_ATLAS.md) uses exactly two chart types, and property (2) of Definition 3.1.1 says their inner discs cover Y_σ. Let u be a unitary Möbius map, u(t) = (αt+β)/(−β̄t+ᾱ), |α|²+|β|² = 1. A direct computation gives |αt+β|² + |−β̄t+ᾱ|² = 1+|t|², hence

  (4.1) |du/dt| = (1+|u|²)/(1+|t|²), so |dt/du| = (1+|t|²)/(1+|u|²) ≥ 1/2 whenever |u| ≤ 1.

(i) Unramified Whitney chart: z_j = u_j(t∘π)/ρ_j with 0 < ρ_j ≤ 1, u_j(center) = 0, ρ_j = κ·d_ch(center, B_σ) capped at ρ_cap. For x ∈ U_j^{r₁}, d_ch(π(x), center) ≤ |u_j| ≤ ρ_j, so d_ch(π(x),B_σ) ≤ (1+1/κ)ρ_j in the uncapped case, and ρ_j = ρ_cap ≥ ρ_cap min(1, d_ch) in the capped case. Thus ρ_j ≥ c₁' min(1, d_ch(π(x),B_σ)) with c₁' = min(κ/(1+κ), ρ_cap), and by (4.1) |dt/dz_j| = ρ_j |dt/du_j| ≥ ρ_j/2.

(ii) Branch (root) chart over b ∈ B_σ: φ_b = u_b(t), φ_b(π(w)) = h w^e, |w| < 1, 1 ≤ e ≤ d. Then |dt/dw| = |dt/dφ_b| · h e |w|^{e−1} = |dt/dφ_b| · e|φ_b(π(w))|/|w| ≥ (1/2)·|φ_b(π(w))| ≥ (1/2) d_ch(π(w), b) ≥ (1/2) d_ch(π(w), B_σ), using |w| < 1, e ≥ 1, (4.1), and d_ch(0,φ) = |φ|/√(1+|φ|²) ≤ |φ| together with unitary invariance of d_ch. Note that no factor |w|^{−(e−1)} survives: the ramified chart loses nothing.

Hence (H2) holds with c₀ = c₁'/2 whenever A_σ consists of these two chart types and covers Y_σ. The *only* unverified content of (H2) is therefore the coverage/count assertion that is already the content of (H1); I list it separately because (H1) as a bare set of four numbers does not imply (H2).

Under (H1), for d ≥ 2 (so 1 ≤ d ≤ d²):

  (4.2) Λ_σ ≤ c_r d(d+L_σ)[330·8·log 4 + 13.2 c d² + c d] ≤ κ_r d³ (d + L_σ), κ_r := c_r (3661 + 14.2c).

Linearity of Λ_σ in L_σ is essential and is what makes averaging over σ possible.

## 5. Lemmas C and D: per-embedding archimedean bounds

**Lemma C (differential).** Assume (H1),(H2). For x ∈ Y_σ with a := π(x) ∈ C,

  −log‖dπ‖_Ar(x) ≤ Λ_σ + log(1/c₀) + log( 1/min(1, d_ch(a, B_σ)) ).

*Proof.* Take the chart of (H2). dπ = π^*dt = (d(t∘π)/dz_j) dz_j, so −log‖dπ‖_Ar(x) = −log‖dz_j‖_Ar(x) − log|d(t∘π)/dz_j(x)| ≤ Λ_σ + log(1/c₀) + log(1/min(1,d_ch(a,B_σ))) by Lemma B and (H2). ∎

**Lemma D (Wronskian).** Assume (H1). For every x ∈ Y_σ,

  log‖Wr‖_Ar(x) ≤ (g(g+1)/2) Λ_σ + W₀, W₀ := g² log(4g) + (g/2) log(2 c g² d²).

*Proof.* Pick j with x ∈ U_j^{r₁}, r₁ = 3/4. On U_j write ω_k = f_k dz_j with (ω_k) orthonormal; Σ_k |f_k|² = 2g F_j ≤ 2g c₁ on the whole unit disc (property (4)). The closed disc of radius 1/4 around z_j(x) lies in the unit disc, so Cauchy's estimate gives |f_k^{(l)}(x)| ≤ l! 4^l sup|f_k| ≤ l! 4^l (2g c₁)^{1/2}. Hadamard: |W_{z_j}(ω)(x)| ≤ Π_{l=0}^{g−1} (Σ_k |f_k^{(l)}(x)|²)^{1/2} ≤ Π_l l! 4^l (2 g² c₁)^{1/2}. Taking logs, log|W| ≤ Σ_l (log l! + l log 4) + (g/2) log(2g²c₁) ≤ g² log(4g) + (g/2) log(2cg²d²). Combine with N1 and log‖dz_j‖_Ar(x) ≤ Λ_σ (Lemma B, upper side). ∎

Both lemmas hold for every x, so no choice of point is needed before averaging; the averaging cost is only in Λ_σ and in the collision term of Lemma C.

## 6. Proposition E: reworked Theorem 4.5.1 with general B

**Proposition E.** Assume (H1),(H2). Let a ∈ Q with a ∉ B ∪ {∞}, and let b ∈ Y(Q̄) with π(b) = a. Then

 (E) h(b) ≤ d · Σ_{β∈B} (h(β) + h(a) + log 2) + 2d² log d
      + [K:Q]^{−1} Σ_σ Λ_σ + log(1/c₀) + Σ_{β∈B} (h(β) + h(a) + log 2),

for any number field K as in the proof, and the Λ-average satisfies

 (E′) [K:Q]^{−1} Σ_σ Λ_σ ≤ κ_r d³ ( d + 1 + r(r−1)(2h_B + log 2) ).

*Proof.* Step 0 (field). Let K₀ be a number field over which Y, π, every β ∈ B and every point of π^{−1}(a) are defined. Apply Theorem 4.3.2 (supplied) to π_{K₀}: obtain K ⊃ K₀ and the finite flat normalization π: 𝒴 → P¹_{O_K} with minimal resolution ψ: 𝒴′ → 𝒴 semistable over O_K and all vertical branch components of residue characteristic ≤ d. Everything below is normalized by [K:Q]; by A0 the result is field-independent.

Step 1 (minimality). Let P′ be the closure of b in 𝒴′. By Lemma 2.3.1 (supplied), h(b)[K:Q] ≤ (P′, ω_{𝒴′/O_K}).

Step 2 (rational section). K_{𝒴′} := div(dπ) as rational section of ω_{𝒴′/O_K}. Its support in the generic fibre is π^{−1}(B ∪ {∞}) (zeros of π^*dt at ramification points of π over B, poles over ∞). Since a ∉ B ∪ {∞}, P′ ⊄ Supp K_{𝒴′} (a horizontal prime divisor is never contained in a vertical one). Hence

 (P′, ω_{𝒴′/O_K}) = (P′, K_{𝒴′})_fin + Σ_σ (−log‖dπ‖_σ)(σ(b)).

Step 3 (finite part). Let D be the reduced branch divisor of π: 𝒴 → P¹_{O_K}. Its horizontal part is Σ_{β∈B} β̄ (a horizontal prime divisor has as generic point a point of P¹_K, where π is non-étale iff that point lies in B). By Theorem 4.3.2 every vertical component has p_i ≤ d, so in the notation of Section 4.2, D₁ = Σ_{β∈B} β̄. Proposition 4.2.4 (supplied) with Q = ā:

 (P′, K_{𝒴′})_fin ≤ d (D₁, ā)_fin + 2d² log d [K:Q] = d Σ_β (β̄, ā)_fin + 2d² log d [K:Q].

The wild term 2d² log d[K:Q] comes from Lemma 4.2.3/Proposition 4.1.3 and the sum over primes p ≤ d; it is independent of B and of a. By Lemma A(a), (β̄, ā)_fin ≤ [K:Q](h(β)+h(a)+log 2).

Step 4 (archimedean part). For each σ, Lemma C at x = σ(b), π(x) = σ(a) = a: −log‖dπ‖_σ(σ b) ≤ Λ_σ + log(1/c₀) + log(1/min(1, d_ch(a,B_σ))). Now min(1, d_ch(a,B_σ)) = min_β d_ch(a, σβ) and all log(1/d_ch) ≥ 0, so log(1/min_β d_ch(a,σβ)) ≤ Σ_β log(1/d_ch(σa, σβ)). Summing over σ and applying Lemma A(b) to the pair (β, a):

 Σ_σ log(1/min(1,d_ch(a,B_σ))) ≤ [K:Q] Σ_β (h(β) + h(a) + log 2).

Adding Steps 3 and 4 and dividing by [K:Q] gives (E).

Step 5 (average of L_σ). δ_σ ≤ 1, so log(1/δ_σ) ≤ Σ_{β≠β'} log(1/d_ch(σβ,σβ')) (ordered pairs, each term ≥ 0). By Lemma A(b) applied to (β, β′), Σ_σ log(1/d_ch(σβ,σβ′)) ≤ [K:Q](h(β)+h(β′)+log 2) ≤ [K:Q](2h_B + log 2). Hence [K:Q]^{−1}Σ_σ L_σ ≤ 1 + r(r−1)(2h_B + log 2), and (E′) follows from (4.2) by linearity in L_σ. ∎

Remark on quantifiers. The per-σ collision term log(1/d_ch(a,B_σ)) is *not* uniformly bounded: a may be archimedeanly close to a conjugate of some β. Lemma A(b) bounds its *sum* over all embeddings by heights, which is the exact replacement for the source's "ℑ(λ^{−1}(a)) ≥ 0.85" distance promise (lines 1590–1597). No distance promise is used anywhere.

## 7. Choice of a and assembly

**Choice of a.** Y has at most g³ − g Weierstrass points (zero for g = 1), hence π(Weierstrass) ∪ B ∪ {∞} has at most g³ + r points. Among the integers 1, 2, …, g³ + r + 1 at least one, call it a, avoids this set; then every point of π^{−1}(a) is non-Weierstrass and a ∉ B ∪ {∞}. By (1.1), h(a) = log a ≤ log(r³d³ + r + 1) ≤ log(2r³d³) ≤ 3 log(2rd). This is an explicit finite search over ≤ g³+r+1 candidates given the finite sets π(W) and B; no claim is made about the bit cost of *computing* those sets, since the theorem is a geometric inequality, not an algorithm.

**Assembly.** Let b ∈ π^{−1}(a). Theorem 2.4.1 **[ASSUMPTION A1, proof not supplied: cites [11, Thm 5.9], Faltings, Bost]** gives

  h_Fal(Y) ≤ (g(g+1)/2) h(b) + log‖Wr‖_Ar(b),

where log‖Wr‖_Ar(b) = [K:Q]^{−1} Σ_σ log‖Wr‖_Ar(σb) ≤ (g(g+1)/2)[K:Q]^{−1}Σ_σ Λ_σ + W₀ by Lemma D.

From (E), (E′), h(a) ≤ 3 log(2rd), |B| ≤ r, and r(r−1)(2h_B+log 2) ≤ 2r²(h_B+1):

 h(b) ≤ κ_r d³( d + 1 + 2r²(h_B+1) ) + (d+1) r ( h_B + 3 log(2rd) + log 2 ) + 2d² log d + log(1/c₀)
   ≤ C_r^{(1)} d³ (d + 1 + h_B),

with, e.g., C_r^{(1)} = 3r²κ_r + 2r(3 log(2r) + 4) + 2 + log(1/c₀) (using log d ≤ d, d ≥ 2). Likewise [K:Q]^{−1}Σ_σ Λ_σ ≤ 3r²κ_r d³(d+1+h_B), and W₀ ≤ C_r^{(2)} d² log(4rd) by (1.1). Since g(g+1)/2 ≤ r²d² by (1.1),

 h_Fal(Y) ≤ r²d² · (C_r^{(1)} + 3r²κ_r) d³(d+1+h_B) + C_r^{(2)} d² log(4rd) ≤ C_r d⁵ (d + 1 + h_B),

with C_r := r²(C_r^{(1)} + 3r²κ_r) + C_r^{(2)}. This is the claimed statement. ∎

*Consistency control (not evidence).* For r = 3, h_B = 0 the bound reads C₃ d⁶, matching the shape of the supplied Belyi assembly (h(b) ≲ d⁵/g, log‖Wr‖ ≲ g d⁵, so h_Fal ≲ g d⁵ ≤ C d⁶ after (1.1)). The h_B-dependence is linear in the logarithmic height, i.e. logarithmic in the exponential height H_B, as opposed to the exponential dependence of the Belyi conversion; this matches the shape attributed in the repository note to Remark 6.0.5 but I have no access to that remark and do not use it.

## 8. Hypothesis ledger, proof obligations, falsifiers

Exact list of what is assumed versus proved.

**Proved here (unconditional):** Lemma A (identity (A) and (A.a),(A.b)); the unitary-Möbius derivative identity (4.1); the derivation of (H2) from the candidate's two chart types with c₀ = min(κ/(1+κ), ρ_cap)/2; Lemma B given N1 and Theorem 3.1.2; Lemmas C, D given (H); Proposition E and the assembly given the ledger below; the non-Weierstrass base-value choice.

**Assumptions (each one is a separate obligation):**
- **O1 (H1).** The analytic Merkl-atlas lemma, including its coverage of Y_σ by inner discs and its counts. Status in repository: under independent attack, provisional. Falsifier: a single cover Y_σ (fixed d, B_σ) for which any maximal-net construction needs more than c_r d(d+L_σ) charts, or a chart on which F_j exceeds c d², or a transition with |dz_j/dz_{j'}| > e^{cd}. A finite numerical scan cannot establish (H1); it can only refute it.
- **O2 (H2).** Reduces to: every chart of A_σ is of Whitney or root type with the stated radius rule. If the construction is modified (e.g., extra charts near cluster boundaries), (H2) must be re-verified; falsifier: a point whose only covering inner disc has |d(t∘π)/dz_j| < c₀ min(1,d_ch(π x,B_σ)).
- **O3 (N1).** Normalization of ‖·‖_Ar via gr and the Wronskian decomposition. Standard, taken from the source's Section 2.1 which is not supplied; the supplied Proposition 3.5.1 proof uses exactly this decomposition. A sign/normalization error here would rescale Λ-terms by a constant, not change the polynomial shape; falsifier: a genus-1 example with explicitly known gr where lim_{y→x}(log|z(y)−z(x)| − gr) ≠ log‖dz‖_Ar.
- **O4 (A1).** Theorem 2.4.1: h_Fal ≤ ½g(g+1)h(b) + log‖Wr‖_Ar(b) for non-Weierstrass b. The supplied text attributes it to [11, Theorem 5.9] and (4) of Section 2.1; the proof is not supplied, so it is an assumption, not a proof.
- **O5.** Theorem 4.3.2, Proposition 4.2.4, Lemma 4.2.3/Proposition 4.1.3, Lemma 2.3.1: proofs supplied, relying on [29],[30] (Liu) and Lenstra's bound; accepted as source-proved. Note the wild term 2d²log d is independent of B only because Theorem 4.3.2 forces vertical branch components into characteristic ≤ d; that step depends on semistability over O_L from [30, Cor. 2.8].
- **O6 (A0).** Field-independence of h(b) and ‖Wr‖_Ar ([36, §5.4]).

**Added arithmetic model hypothesis:** none beyond O5/O6, which the source itself uses. In particular no hypothesis on the heights of equations of Y, no Galois-orbit splitting beyond Galois-stability of B (which is forced by the definition of "total orbit"), no uniform archimedean separation of a from B_σ, no uniform lower bound on δ_σ.

**Falsifiers of the conditional statement as a whole.** Any family (fixed r) with h_Fal(Y)/(d⁵(d+1+h_B)) → ∞ would refute the theorem and therefore refute at least one of O1–O6. The twist family y² = a·x(x−1)(x−2) is *not* a falsifier: its stable Faltings height is constant in a, in agreement with the bound; it does refute any attempt to read the bound as a bound on model/coordinate heights.

## 9. What is charged, and what does not follow

- Inputs charged: the cover (Y, π, B) over Q̄ as a geometric object and h_B. Nothing else enters.
- Precision/outputs: the bound is a real inequality with constants explicit in (c_r, c, c₀, r). No numerical Faltings height is computed; no bit cost is claimed.
- The obstruction attacked first was the cheapest one: whether averaged archimedean collision and horizontal finite intersections are polynomial in h_B. Both are settled exactly by Lemma A; the entire residual risk is the analytic lemma O1/O2 plus the cited O3–O6.
- Nothing here produces a torsion module, a Frobenius, a coordinate height, a CRT reconstruction, a surface point count, a hardness statement, or a quantum speedup. The stable Faltings height controls the Q̄-isomorphism class only; passing to any presented model, or to degree-five surfaces over F_p, is a separate obligation not addressed and not implied.
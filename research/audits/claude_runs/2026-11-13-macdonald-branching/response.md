# Review: regular specialization at q = t³ and positive branching for the Macdonald Lax transform

## Verdict

**I did not falsify the algebraic obligation.** With t = D/(D+1), q = t³ and N = D+1 held fixed for every stage n ≤ D, the following all hold at the specialized point:

- every source identity the construction needs is regular there;
- the creation scalar is q^(−j−1/2) > 0;
- χ_μ = (1−t)(q⁻¹−1) Σ_{b∈μ}[b] = Θ(n/N²);
- every removal weight satisfies p_(μ,r) > 0 and p_(μ,r) = Ω(1/n);
- every τ satisfies Ω(1/n²) ≤ τ ≤ 1.

The parent's notation "Jhat" collides with the source. In the source, Ĵ_λ = J_λ/ϖ_λ, which is singular. Below, Ĵ_λ means J_λ/‖J_λ‖ only.

**Status of the evidence.** Generic-(q,t) source theorems are used as cited facts and were not re-proved:

- Props 3.11–3.13, Lemma 3.10;
- Lemma 4.7, Prop 4.8 (whose proof leans on reference [6]);
- Macdonald integrality of J_λ, which needs a citation check.

Everything else below is deduction. The native block encoding, polar compilation and QPE costs are not established here.

## 1. Regularity ledger at q = t³, 0 < t < 1

All exponent arithmetic uses e(i,j) = i − 3j, so [b] = t^{e(b)}, with zero-indexed (row, column). The main tool is that 1 − t^x = 0 iff x = 0.

- **Hook factors.** 1 − q^a t^{ℓ+1} = 1 − t^{3a+ℓ+1} and 1 − q^{a+1} t^ℓ = 1 − t^{3a+3+ℓ}. Both exponents are positive, so H_λ = Π h h′ > 0.
- **Hall form.** r_k = 1 + t^k + t^{2k} ∈ [1, 3].
- **Full inner product.** ⟨z^{−m}p_μ, z^{−n}p_ν⟩_∞ = q^m δ_{mn} δ_{μν} z_μ Π_k r_k^{m_k} is real positive definite.
- **Entries of L.** L = Q†D_{t/q}Q has p-basis entries that are Laurent polynomials in (q, t). They are regular at the point, and L stays self-adjoint by continuity.
- **J_λ.** I rely on the integrality theorem J_λ ∈ Z[q,t]-span{m_μ} (Knop; Sahi; Kirillov–Noumi; Garsia–Tesler; citation check required).
  - **Required pole check.** Do not build J_λ from Macdonald-operator eigenvalue denominators. Σ q^{λ_i} t^{−i} coincides across λ at q = t³, so those denominators genuinely have poles there.
  - **Consequences.** Orthogonality and ‖J_λ‖² = Π h h′ then specialize by continuity.
- **Corner interlacing.** For a nonempty λ, the addable corners are a_k = (I_k, L_{k+1}) and the outer corners are r_k⁺ = (I_k, L_k). Write f_k = e(a_k) and e_k = e(r_k⁺). Then:
  - e_k − f_{k−1} = I_k − I_{k−1} ≥ 1;
  - f_k − e_k = 3(L_k − L_{k+1}) ≥ 3;
  - hence f_0 < e_1 < f_1 < … < e_m < f_m, strictly, in integers.

  The range is R = f_m − f_0 = ℓ(λ) + 3λ_1 ≤ 3(n+1). Within one partition, therefore, no content coincidences and no zeros of τ or τ̃ occur.
- **Un-hatted cyclic definition.** Use Ψ^s_λ = (1/τ^s_λ) Π_{r∈A_λ, r≠s} (L − [r])/([s] − [r]) · J_λ.
  - The generic identity Π_{s∈A_λ}(L − [s])J_λ = 0 (Prop 3.12) is a Laurent-polynomial identity, so it holds at the point.
  - All denominators are nonzero by interlacing.
  - LΨ = [s]Ψ, π0Ψ = J_λ, mutual orthogonality and ‖Ψ^s_λ‖² = H_λ/τ^s_λ all follow by continuity.
  - Ψ ≠ 0 because π0Ψ = J_λ. Orthogonal nonzero vectors under a positive-definite form, together with the source count Σ|A_λ| = dim, give a basis.
- **φ and creation.** φ^r_γ = Σ_a τ^a_γ [a]/([a] − [r⁺]) Ψ^a_γ is regular, since [a] ≠ [r⁺] by interlacing. Lemma 4.7, Prop 4.8 and Cor 4.9 are identities between vectors that are regular at the point, so they specialize. Their generic proofs used ϖ; the specialized statements do not.
- **Global coincidences** ([s] for s ∈ A_λ equal to [s′] for s′ ∈ A_{λ′}, λ ≠ λ′) are harmless. Eigenspaces of L become degenerate, but none of the constructions above divides by a cross-λ content difference.
- **Genuine singularities to avoid.** ϖ_λ = 0 whenever λ contains a box with i = 3j ≠ 0, for example (3,1) ∈ (2,2,2,2) and every λ containing it. Also [s] − 1 = 0 for such an s. Hence the hatted Ψ̂ and the source equations (19), (21) and (24) are 0/0 there. Never use them.

## 2. Creation scalar

Prop 4.8 and Lemma 4.7(ii) give Q z⁻¹ Ψ^s_λ = q^{−a′(s)} Q φ^s_{λ+s} = q^{−j} J_{λ+s}, where j is the column index of s.

The norm satisfies ‖z⁻¹f‖² = q‖f‖². So I(f) = z⁻¹f/√q is unitary from Λ[z⁻¹]_{n−1} onto Λ^∞_n, and:

A Ψ^s_λ = q^{−j−1/2} J_{λ+s}, with q^{−j−1/2} > 0.

## 3. Formula and bounds for χ

The block form of L makes the adjoint of Q equal to D_{q⁻¹}Q*. Therefore AA† = QQ† = π0 L² π0 − 1 = T₂ − 1.

From (9), T_λ(u) = 1 + u⁻¹(1 + u⁻¹(Σ_A[a] − Σ_{R⁺}[b]) + …). So the eigenvalue is χ_λ = Σ_A[a] − Σ_{R⁺}[b] − 1.

Lemma 2.3 gives N(u/[b]) = 1 − [b](1−t)(1−q⁻¹)/u + O(u⁻²). Comparing the u⁻¹ coefficients of S_λ yields:

χ_λ = (1−t)(q⁻¹ − 1) Σ_{b∈λ} [b].

Numerical bounds:

- 1 − t = 1/N.
- q⁻¹ − 1 = (3D² + 3D + 1)/D³ ∈ [3/D, 7/D].
- Boxes have i, j ≤ n−1, so [b] ∈ [t^{n−1}, t^{−3(n−1)}] ⊂ [e⁻¹, e³].

Hence χ_μ ∈ [3n/(eND), 7e³n/(ND)] = Θ(n/N²), uniformly for n ≤ D. The singular-value spread of A at a fixed stage is bounded: the ratio is at most √(7e⁴/3) ≈ 11.3. Absolute conditioning relative to the native normalization of A is the polar task's obligation.

## 4. The isometry V and the branching weights

The Ψ^r_{μ−r} are orthogonal with ‖Ψ^r_{μ−r}‖² = H_{μ−r}/τ. Using ⟨AΨ^s_λ, J_μ⟩ = q^{−j−1/2} δ_{λ+s,μ} H_μ:

A†J_μ = Σ_{r∈R_μ} q^{−j(r)−1/2} τ^r_{μ−r} (H_μ/H_{μ−r}) Ψ^r_{μ−r}.

Define V = A†(AA†)^{−1/2}. Then V†V = I on Λ_n, and

V Ĵ_μ = Σ_r √p_(μ,r) · Ψ̃^r_{μ−r}, where Ψ̃ = Ψ/‖Ψ‖ and

p_(μ,r) = q^{−2j−1} τ^r_{μ−r} H_μ / (χ_μ H_{μ−r}).

Two consequences:

- **Normalization.** Σ_r p_(μ,r) = ‖A†J_μ‖²/(χ_μ H_μ) = 1.
- **Sign.** Each p is a product of positive factors, so p > 0. Also ⟨Ψ̃^r_γ, Ĵ_γ⟩ = √τ^r_γ > 0, which is the positive-phase convention.

**Second form of p.** Lemma 4.7(iii) gives Q†J_μ = −Σ[r⁺]τ̃^{r⁺}_μ φ^r_μ, and φ^r_μ = q^j z⁻¹Ψ^r_{μ−r}. Comparing coefficients gives:

p_(μ,r) = −[r⁺] τ̃^{r⁺}_μ / χ_μ.

Its sum over r equals 1 independently, by Lemma 3.10's fourth identity (Σ_b [b]τ̃^b = −χ). This is a consistency check; the termwise equality is a cheap exact-rational falsifier test, and passing it is not a proof.

## 5. Uniform bounds on τ and p via the Jack comparison

Set h = −ln t = ln(1 + 1/D) ∈ [1/N, 1/D]. Write 1 − t^x = h·x·G(x), where G(x) = (1 − e^{−hx})/(hx) > 0. Then:

- d/dx log G(x) = h·φ(hx), with φ(y) = 1/(e^y − 1) − 1/y ∈ [−1, 0]. Hence |Δ log G| ≤ h|Δx|.
- All exponent differences satisfy |x| ≤ R ≤ 3(n+1), so h|x| ≤ 6. Thus G ∈ [g₋, g₊] with g₋ = (1 − e⁻⁶)/6 and g₊ = (e⁶ − 1)/6.

**Bound on τ.** For s = a_p:

τ^s_λ = t^{−e_s} · τ^lat · e^E, where τ^lat = Π_k (e_k − f_p) / Π_{k≠p} (f_k − f_p).

The m factors of h cancel. Pair e_k with f_{k−1} for k ≤ p, and e_k with f_k for k > p. These pairings cover disjoint intervals, so |E| ≤ hR ≤ 6. This is the accumulated defect O(hD) = O(1).

For the lattice part, write e_k ≥ f_{k−1} + 1 and telescope. The right product is at least 1/(f_m − f_p), and the left product is at least 1/(f_p − f_0). With t^{−e_s} ≥ e⁻³:

τ ≥ 4e⁻⁹ / (9(n+1)²).

Also τ ≤ 1, because the τ are positive and sum to 1. A direct sign count confirms positivity: p negative factors in the numerator and p in the denominator.

**Bound on p.** −[b]τ̃^b = [b]·h²·ν^lat_b·(G ratio). The G ratio is at least e⁻⁶g₋², using m−1 pairs plus two leftover factors.

For the lattice co-transition weight ν^lat_b, pair e_{k′} with f_{k′−1} for k′ < k and with f_{k′} for k′ > k. Each ratio is at least 1, and the leftover factor is (e_b − f_{k−1})(f_k − e_b) ≥ 1. So ν^lat_b ≥ 1.

With [b] ≥ e⁻¹ and h² ≥ N⁻², this gives p_(μ,r) ≥ c/n, with c = e⁻¹⁰g₋²/14 (small but absolute).

## 6. Down-stage map, labels, phase and bit cost

**Content resolution.** Let P_c be the eigenprojector of L onto content c in degree n−1.

- P_c Ĵ_γ = √τ · Ψ̃^s_γ if some s ∈ A_γ has [s] = c, and 0 otherwise.
- So π0 P_c π0 is diagonal on {Ĵ_γ}. The two-dimensional planes span{Ĵ_γ, Ψ̃^s_γ} ⊂ Z_γ are mutually orthogonal across γ. Coincident contents across different γ therefore cause no mixing.

**Rotation with positive phase.** Let R₀ be the reflection 2π0 − 1 and R_c the reflection 2P_c − 1.

- In each plane, R₀R_c is a rotation by −2θ, where cos θ = √τ.
- Its principal square root sends Ψ̃ to +Ĵ_γ.
- The eigenphase satisfies 2θ ≤ π − Ω(1/n), because τ ≥ Ω(1/n²). An equivalent route is QSVT singular-vector transformation at singular value √τ.

**Labels and erasure.**

- Removable corners of μ have distinct contents. Addable corners of each intermediate shape have distinct contents. Hence the content sequence determines the whole path and μ, so shape labels can be erased.
- Each label k = i − 3j ∈ [−3(n−1), n−1] costs ⌈log₂(4D+1)⌉ bits.
- Eigenvalue gaps are t^k/N ≥ 1/(eN).

Stage n then maps Ĵ_μ to Σ_r √p_(μ,r) |k_r⟩Ĵ_{μ−r}, with all path amplitudes positive. This fixes the output phase to +J_μ/‖J_μ‖.

**Bit cost of the weights.**

- τ and τ̃ each have O(√D) factors of the form 1 − t^x, with |x| ≤ 3D+3.
- Each factor equals ((D+1)^x − D^x)/(D+1)^x, which takes O(D log D) bits.
- Exact rationals therefore need O(D^{1.5} log D) bits; χ needs O(D log D) bits.
- All quantities are well-conditioned, so O(b + log D) working bits suffice for 2^{−b} accuracy in the angles.

## 7. Not established here: obligations and falsifiers

1. **Integrality citation.** Check that the cited integrality of J_λ applies. The fallback is any construction of J_λ that is regular at q = t³.
2. **Native block encoding of L and A.** Prove the constant-normalization claim for C† (I checked only w_k ≤ 16√k/N, which holds since w_k² ≤ 3e³k/N²). Bound the exp(C) LCU and the reversibility of the truncation.
3. **Polar compilation.** Compile (AA†)^{−1/2} at the actual ratio σ_min/α, using the failure-projector form of I − B†B rather than a two-term LCU.
4. **Clean QPE.** Show that QPE at gap 1/(eN) gives errors that compose to at most 2^{−b} over D stages, with uncomputation paid.
5. **Shape-side state C.** Prove that C prepares Π√p over paths reversibly in poly(D, b) and that the B†C erasure is exact up to stated error.
6. **Falsifiers.**
   - Any pair of addable/outer contents within one partition coinciding: excluded by the integer interlacing proof above.
   - Exact-rational disagreement between the two forms of p.
   - Native block normalization growing with D.
   - A polynomial classical sampler for this output law, which would remove any claimed advantage. The current status remains "no established advantage".
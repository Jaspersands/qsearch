# Adversarial review: two-branching-circuit full Jack transform at α = 3

## Verdict

**The full-transform mechanism survives review, conditionally.** I found no fatal gap. The three conditions are:

- **(H1)** The supplied identity (6)/(7), A_D† J_μ = Σ_r τ N_μ/N_{μ−r} ψ_{μ−r,r}, holds. I re-traced its logic (see A0 below). It rests on the Mickler–Moll cyclic and compression facts and on the one-box Pieri rule.
- **(H2)** The uniform bound τ_{λ,s} ≥ 3/[16(n−1)] holds. It is taken as given, as instructed.
- **(H3)** The "native α3 Hall coefficient-state model" stores amplitudes in the orthonormal basis e_μ w^l = V_μ w^l/‖V_μ‖₃, using an occupation-number register. I could not see JACK_LAX_PREPARATION_CANDIDATE, so this is an assumption. If the native basis differs, a basis-change step must be added and charged.

Two components remain open or are replaced:

- **QSVT route: OPEN as written.** The supplied excerpt of Gilyén–Su–Low–Wiebe (arXiv 1806.01838v1) proves the existence of Φ, citing Lemma 25, Corollary 10, Theorem 17 and Lemma 19. It does not show a polynomial-bit classical algorithm for computing Φ. Lemma 25 states only that P_< is "efficiently computable", not that the phases are.
- **QSVT replacement.** The rotation synthesis you suggest, controlled by a computable rational τ, is unavailable inside B_n†. At that point λ exists only in the Fock register, and extracting it is exactly the decoding problem. The repair below is λ-oblivious: phase estimation on the walk operator, followed by a half-angle phase. It uses only phase estimation, comparisons and dyadic phase gates. It is fully explicit and polynomial.

The construction below is a complete polynomial gate/bit circuit, modulo (H1)–(H3). It is not a proof of hardness, novelty, separation, or anything physical about Calogero–Sutherland systems.

---

## Attacks, cheapest first

### A0. Algebra logic check (not a re-proof of the source inputs)

The step chain is as follows.

1. u = A†J_μ has spectral support in {c(r) : r ∈ R_μ}.
2. A_λ ∩ R_μ contents = {c(s)}. So ⟨J_λ, u⟩ = ⟨P_{c(r)} J_λ, u⟩.
3. ⟨J_λ, A†J_μ⟩ = ⟨V₁J_λ, J_μ⟩ = τ N_μ.
4. The orthogonal projections onto e_r = τ ψ_{λ,r} have squared norms summing to N_μ Σ τ N_μ/N_λ = 3(D+1)N_μ = ‖u‖². Pythagoras then leaves zero remainder.

Each step is valid given the sources.

I also did a hand sign check at degree 2 (consistency only, not evidence). With J₂ = V₁²+3V₂ and N = 72, and J₁₁ = V₁²−V₂ and N = 24, I get τ_{(1),(1,0)} = 1/4 and τ_{(1),(0,1)} = 3/4. This gives A†J₂ = 6V₁+18w = 6ψ_{(1),(1,0)} and A†J₁₁ = 6V₁−6w = 6ψ_{(1),(0,1)}, both with positive coefficients.

**Falsifier for H1:** any exact (μ, D) at α = 3 where A_D† J_μ has a component orthogonal to span{ψ_{μ−r,r}}.

### A1. Path-space consistency — survives (proved)

Let Φ_μ = Σ_paths √(∏q) |∅⟩|c_D…c_1⟩.

- **Orthonormality across μ.** Read a path from ∅ upward. Each content selects a unique addable corner, because addable corners (x_i, y_i) have x increasing and y decreasing, so 3x−y is strictly monotone. The path therefore determines μ, and different μ have disjoint path supports.
- **The B-chain gives this exact state.** Consider B_n j_μ and B_n j_ν. Any overlap requires μ−r = ν−r' = λ with c(r) = c(r'). Then r and r' are addable corners of λ with equal content, so r = r'. Hence B_n is an isometry on F_n, and the composite B-chain sends j_μ to |vac⟩⊗Φ_μ with the same amplitudes ∏q as the C-chain.

Therefore T := (B-chain)⁻¹ ∘ (C-chain) maps |μ⟩ ↦ j_μ exactly, and linearly on superpositions.

### A2. Global singular pairs despite content degeneracy — survives (proved)

Let Π̃ = P₀ (marker l = 0) and Π = Σ_c P_c ⊗ |c⟩⟨c|, where P_c is the global spectral projector of L_{n−1}.

- By Mickler–Moll Theorem 1.4 and Lemma 3.5, ran P_c has the orthonormal basis {v_{λ,s(λ,c)}}. This runs over the λ that have an addable corner of content c, and there is at most one such corner per λ. The spaces Z_λ are mutually orthogonal.
- P₀ v_{λ,s} = π₀ψ/‖ψ‖ = √τ_{λ,s} j_λ, using ‖ψ‖² = N_λ/τ.
- Π j_λ|c⟩ = √τ v_{λ,s}|c⟩, because j_λ ∈ Z_λ is orthogonal to every Z_{λ'}.

So the planes S_{λ,c} = span{v_{λ,s}|c⟩, j_λ|c⟩} are invariant under both projectors. On each plane, P₀P_c has singular pair (v, j) with value √τ > 0.

The remaining invariant pieces are:
- unpaired j_λ|c⟩ vectors, on which W = −1;
- the common complement, on which W = +1;
- τ = 1 lines, where v = j.

### A3. Phases between B and C — survives (proved)

Write q = τ N_μ/(3n N_{μ−r}). Then V j_μ = Σ √q v_{μ−r,r} with positive coefficients.

The remaining phase sources are all trivial:

- **Phase estimation on an exact integer eigenvalue** produces no phase on the eigenvector.
- **The polar map** sends v ↦ +j: the rotation is by +θ toward j, and cos θ = √τ > 0.
- **The C-chain** uses the same positive √q.

The overall convention is that [V₁^D] J_μ = 1 is positive. That is the target's convention; any other convention is a classically computable diagonal ±1 applied to |μ⟩ beforehand.

### A4. QSVT step

**If Φ can be computed, the conversion is fine.** Set U = I, with right projector Π and left projector Π̃. All input vectors lie in Π_{≥δ}, with δ² = min τ ≥ 3/[16(n−1)].

Theorem 26 gives ‖Π̃_{≥δ} U_Φ x − WV†x‖ ≤ ε for a unit vector x in that range. Since WV†x ∈ ran Π̃_{≥δ} and ‖U_Φ x‖ = 1:

‖U_Φ x − WV†x‖² ≤ ε² + 1 − (1−ε)² ≤ 3ε.

This bound is linear, so it holds in operator norm on the subspace.

**The gap is phase compilation**, as stated in the Verdict, so this gate stays OPEN. The construction below does not use it.

---

## Explicit circuit

### Registers (all polynomial)

| Register | Contents | Size |
|---|---|---|
| Label | partition μ ⊢ ≤ D | O(D log D) |
| Fock | power-sum occupations m_k plus marker l, with Σ k m_k + l = current degree | O(D log D) |
| Content records R_D…R_1 | c mod M, with M = 2^⌈log₂(8D)⌉ > spectral width 4D | log M each |
| Phase estimation for L | t = log M qubits | — |
| Phase estimation for the walk | t' qubits | — |
| Arithmetic workspace | fixed-point values at b = O(log(D/ε)) bits | poly |

Both sides encode contents as c mod M, so no signed decoding is needed.

### C_n (label side)

1. Reversibly compute the removable corners r_i of μ, the contents c(r_i), and the rationals q_i. These are ratios of O(D) hook factors of size O(D), so O(D log D)-bit integers. Σ q_i = 1 exactly, by the sum rule (4).
2. Compute Grover–Rudolph-style tree angles arccos√(partial-sum ratios) to b bits.
3. Prepare Σ_i √q_i |i⟩ using rotations by fixed dyadic angles, one controlled per angle bit.
4. Uncompute the angles and q_i, which are functions of μ.
5. Compute c(r_i) into R_n.
6. Uncompute i from (μ, c), which is unique because removable contents are distinct.
7. **Update with a unitary extension:**
   - compute λ = μ − r(μ, c) into a fresh register;
   - XOR g(λ, c) = λ + a(λ, c) into the μ register, where a is the unique addable corner with content c;
   - swap.

   On valid pairs this sends |μ, c, 0⟩ ↦ |0, c, λ⟩ ↦ |λ, c, 0⟩. On invalid encodings the circuit is still a composition of reversible gates, so it is unitary. No rectangular inverse is claimed.

**Error.** C̃_n = Update ∘ S̃ with S̃ = ⊕_μ S̃_μ. So ‖C̃_n − C_n‖ ≤ max_μ ‖S̃_μ − S_μ‖ = O(2^{−b}·#corners), with no factor from the partition count.

### V (Fock side, degree n → n−1)

On basis states, e_μ ↦ Σ_k √(k m_k/n) e_{μ−k} w^{k−1}.

- Prepare the index k with these amplitudes (rational squares, same method as C_n).
- Decrement m_k and set l = k−1.
- Uncompute k from l.

This is block-diagonal in μ, with an injective update and a unitary extension by the same compute–XOR–swap pattern.

### Explicit simulation of L_{n−1} (no black-box sparse simulation)

Decompose L = 2N_w + Σ_{k=1}^{n−1} (H_k^{even} + H_k^{odd}).

- 2N_w is diagonal.
- H_k^{par} = Y_k^{par} + h.c., where Y_k maps (μ, l) → (μ−k, l+k) with weight √(3k m_k), restricted by the parity of m_k.

Each H_k^{par} is 1-sparse Hermitian with explicitly computable real entries of size at most √(3n). Its exponential is a two-level rotation: compute the partner and the angle t√(3k m_k) mod 2π to b bits, apply a controlled R_x, then uncompute. Invalid encodings have no partner and are acted on by the identity.

First-order Trotter gives error ≤ (t²/2r) Σ‖[H_i, H_j]‖ = O(n³/r) for t ≤ 2π. Hence r = O(n³/η) steps, each costing Õ(n) gates.

### PE_L

Apply controlled e^{2πiL·2^j/M} for j < t, followed by the inverse QFT. The spectrum on H_{n−1} consists of integers in [−(n−1), 3(n−1)], so exact evolutions give exactly |c mod M⟩ on eigenvectors. No other workspace exists, and the only error is O(t·η) from simulation.

### R_Π, R_Π̃, W

- **R_Π:** run PE_L into scratch, compare with c, apply a phase −1 on mismatch, then uncompute.
- **R_Π̃:** apply a phase on l ≠ 0. This is exact.
- **W = R_Π̃ R_Π.**
- **Controlled-W:** only the phase kick needs to be controlled.

### G: polar map without QSVT

**Lemma (proved).** On S_{λ,c} with cos θ = √τ ∈ (0, 1), W is rotation by +2θ from v toward j. The principal square root G = W^{1/2}, with eigenphase φ ↦ φ/2 for φ ∈ (−π, π), therefore maps v ↦ +j. On τ = 1 lines, W = 1 = G.

**Gap from the branch cut.** For φ = ±2θ, 2θ = 2 arccos√τ ≤ π − 2√τ_min. So the margin is γ ≥ 2√(3/(16(n−1))) = Ω(n^{−1/2}).

**Implementation.**

1. Run phase estimation of W with t' qubits.
2. Apply the phase e^{iφ̂/2} using t' fixed dyadic phase gates. Assign the outcome φ̂ = ±π arbitrarily.
3. Run the inverse phase estimation.

**Error (operator norm, proved sketch).** The phase-estimation amplitudes satisfy |α_k| ≤ min(1, π/(2^{t'}|Δ_k|)), where Δ_k = φ̂_k − φ.

On an eigencomponent, the error vector before the inverse phase estimation is e_φ ⊗ d_φ, with

‖d_φ‖² ≤ Σ_{|Δ|<γ} (π/(2^{t'}Δ))²(Δ/2)² + Σ_{|Δ|≥γ} 4(π/(2^{t'}Δ))² = O(2^{−t'}) + O(1/(2^{t'}γ)).

Distinct eigenvectors give orthogonal error vectors. So the operator-norm error is at most max_φ ‖d_φ‖ = O((2^{t'}γ)^{−1/2}). Choose 2^{t'} = Θ(√n/ε_G²).

Inputs to G in the forward direction, and to G† in the inverse direction, lie exactly in the paired planes. The W = −1 subspace is reached only through leakage, which the hybrid bound below absorbs.

### B_n and the full transform

- **B_n** = G ∘ PE_L ∘ V. G returns the marker to l = 0, so the marker workspace is cleaned.
- **T** = B̃_D⁻¹ ⋯ B̃_1⁻¹ ∘ C̃_1 ⋯ C̃_D, where each B̃_n⁻¹ is the inverse circuit and B̃_1⁻¹ is applied first. The forward B-chain is never executed.
- At the end of the C-chain the label register is exactly ∅ = 0, and the Fock register is vacuum. The B-chain inverses consume every record. All workspace returns to 0 up to the error budget below.

---

## Uniform error (no p(D) factor)

**Hybrid lemma (proved).** Suppose each stage i satisfies ‖Ũ_i(x⊗0) − B_i x‖ ≤ η_i for every unit x in its domain, and each B_i maps its domain into the next stage's domain. Then the composite error is at most Σ η_i.

For an inverse stage, ‖Ũ⁻¹ B x − x⊗0‖ = ‖B x − Ũ(x⊗0)‖ by unitary invariance.

All per-stage bounds are operator norms, either block-diagonal in a classical basis or established through orthogonal eigen-decomposition. So ‖T̃ − T‖ ≤ 2D·max η holds uniformly over arbitrary superpositions of μ. Choosing η = ε/(4D) per stage gives total error ε.

## Crude cost (unoptimized, polylog factors dropped)

- **Error budget:** ε_G = ε/(4D) per stage. Per-call PE_L error η_L ≈ ε_G/2^{t'+2} = Θ(ε_G³/√n).
- **One PE_L:** O(n³/η_L) Trotter steps of Õ(n) gates each, giving Õ(n^{4.5} ε_G^{−3}).
- **One G:** Õ(√n ε_G^{−2}) calls to PE_L, giving Õ(n⁵ ε_G^{−5}).
- **Total:** Õ(D¹¹ ε^{−5}).
- **Single-qubit dyadic rotations:** Solovay–Kitaev overhead is polylog(D/ε) per gate.

This is polynomial but crude. A verified QSVT phase compiler would reduce the ε-dependence.

## Remaining obligations and falsifiers

1. **H2 enters only through γ.** A single λ ⊢ n−1 with τ superpolynomially small would make this G superpolynomial, though not incorrect.
2. **H3: encoding match.** The native-model note must confirm the e_μ w^l orthonormal occupation encoding at ħ = 3.
3. **H1.** See the falsifier under A0. Any failure of the Z_λ orthogonality or simple-spectrum facts at α = 3 would break A2.
4. **QSVT phases.** These remain OPEN unless a polynomial-bit phase-factor algorithm is supplied from an actual source. The construction above does not need them.
5. **Independent check of this review.** A reviewer should confirm the 1-sparse parity split of Y_k and the Fejér-kernel tail bound. Both are standard, but I wrote them here without tools.

## Scope

If H1–H3 hold, this is a polynomial-size unitary change of basis at fixed α = 3, mapping |μ⟩ ↦ j_μ. There is no postselection, coupon collector, retained label garbage or rectangular inverse. Nothing here establishes classical hardness, novelty, a speedup or a physical position-space transform.
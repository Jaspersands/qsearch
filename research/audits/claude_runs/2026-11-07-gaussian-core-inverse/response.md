# Verdict: the lemma is true, with exponent k^(−d/2) ≤ k^(−4)

I found no counterexample. The bound is tight in its k‑dependence. The constant depends only on d, never on N. Sign, phase and normalization conventions do not affect any absolute value used below.

The cheapest decisive attack was to look for a hidden k^(−1) coming from the noise term after substitution. It fails. The exact inverse undoes the noise in output variables *before* rescaling, so the noise contributes only constants of the form Pf(A0_U).

## Setting (assumptions, not derived)

- **Known channel.** Ψ is known. On the chosen d output Majoranas γ′₁..γ′_d (an orthonormal recombination of the 2N output Majoranas), the restricted channel is Gaussian with:
  - X = O·√R, where O is orthogonal (or O = I after an input-frame rotation),
  - kI ≤ R ≤ I with k > 0,
  - Y = A0 antisymmetric with ‖A0‖ ≤ 1.
- **Physical core.** σ is a physical, even state on k0 ≤ 4 modes. D = 2^{k0} ≤ 16.
- **Moments.** m_S(ρ) = tr(ρ γ_S) for even S ⊆ [d], where γ_S is the Hermitian (phase-fixed) ordered product. m_∅ = 1.
- **Data error.** The data m̂ satisfies ‖m̂ − m(Ψ(σ))‖_∞ ≤ δ, with m̂_∅ = 1.
- **Positive margin.** R ≥ kI with k > 0 *is* a quantitative injectivity hypothesis. Without it (k = 0) there is no inverse and the lemma is vacuous.

## Lemma

Let T be the linear map m(ρ_in) ↦ m(Ψ(ρ_in)) restricted to the d modes. Then T is invertible and

‖T^{-1}‖_{∞→∞} ≤ 9·2^{d−1}·k^{−d/2}.

Let τ be produced as follows:
1. M = Σ_S (T^{-1}m̂)_S γ_S / D. M is Hermitian, even, and has trace 1.
2. τ = M₊ / tr M₊, where M₊ is the positive part of M.

Then

‖τ − σ‖₁ ≤ 3·2^{d−1}·‖T^{-1}‖_{∞→∞}·δ ≤ 27·2^{2d−2}·k^{−d/2}·δ ≤ C·k^{−4}·δ,

with C ≤ 4.5×10⁵ for d = 8. This holds for all δ, with no smallness condition and no fallback branch.

## Proof (proved)

**1. Characteristic-function form.** For any input, χ_out(θ) = χ_in(Xᵀθ)·e^{c·θᵀA0θ}, where c ∈ {±½, ±i/2} depending on convention. Therefore

χ_in(η) = [χ_out · e^{−c·θᵀA0θ}](θ = X^{−T}η).

This is exact. Grassmann ordering and phase signs only produce diagonal unit-modulus rescalings of the coordinates.

**2. Noise removal (step N).** The θ_S coefficient after multiplying by e^{−q} is Σ_{U⊆S, |U| even} ±Pf(A0_U)·χ_{S∖U}. Since Pf² = det, |Pf(A0_U)| ≤ ‖A0‖^{|U|/2} ≤ 1. This gives ‖N‖_{∞→∞} ≤ 2^{d−1}, independent of k.

**3. Substitution (step Λ).** On the degree‑2m block, the substitution acts by Λ^{2m}(X^{−1}). Its operator norm is at most the product of the 2m largest singular values of X^{−1}, which is ≤ k^{−m}. The orthogonal factor O is an isometry on each block. Converting ∞→∞ norms costs at most √binom(d,2m) ≤ √70 < 9. So ‖Λ‖_{∞→∞} ≤ 9k^{−d/2}.

**4. Linear-inverse error.** Write E = M − σ = Σ_S e_S γ_S / D with ‖e‖_∞ ≤ ‖T^{-1}‖δ. Since each γ_S is Hermitian and unitary, ‖γ_S‖₁ = D. Hence ‖E‖₁ ≤ Σ_S|e_S| ≤ 2^{d−1}‖e‖_∞.

**5. Post-processing.** Let ε = ‖E‖₁.
- **Evenness.** M commutes with parity, so M₊ is even.
- **Negative part is small.** Let P₋ be the projector onto M's negative eigenspace. Then tr M₋ = −tr(P₋M) ≤ −tr(P₋E) ≤ ε, because tr(P₋σ) ≥ 0.
- **Clipping costs 2ε.** ‖M₊ − σ‖₁ ≤ ε + ε = 2ε.
- **Normalization costs ε.** t = tr M₊ = 1 + tr M₋ ∈ [1, 1+ε]. Then ‖τ − σ‖₁ ≤ ‖M₊ − σ‖₁/t + (1 − 1/t) ≤ 3ε.
- An explicit parity pinching is a trace-norm contraction, so it is harmless if used.

## Tightness (finite control, exact)

Take R = kI, A0 = 0, d = 8. Compare σ_± = (I ± c·γ_{1..8})/16. Their outputs differ only in the degree‑8 moment, by 2c·k⁴. So k^{−4} cannot be improved. Lower-degree moments are amplified only by k^{−m}.

## Branch comparison corollary (proved; this is a forward bound with no k)

**Gaussian branches.** Suppose ‖Γ‖, ‖Γ′‖ ≤ 1. Let m = |S|/2. Then

|Pf(Γ_S) − Pf(Γ′_S)| ≤ m·‖Γ − Γ′‖_op ≤ 4ε.

Reason: dPf = ½·tr((Pf·A^{−1}) dA), and Pf·A^{−1} has singular values given by products of the other singular values, each ≤ 1. So its trace norm is ≤ 2m. This holds along the segment between Γ and Γ′, extended by density to singular matrices. A restricted block has op norm no larger than the full matrix.

**Mixing.** Mixing is linear in the moments. Matched-weight mixtures therefore differ by ≤ 4·Σ_b p_b ε_b. Mismatched weights add ‖p − p′‖₁.

**Non-Gaussian core through two channels.** Telescoping the Λ^{2m} and Pfaffian factors gives |Δm| ≤ C(d)(‖X − X′‖ + ‖Y − Y′‖).

**Pulled back to the input.** The error becomes ≤ 3·2^{d−1}·‖T^{-1}‖·(δ + 4ε_branch) = O(k^{−4}(δ + ε)). The forward Lipschitz step adds no k. The k^{−4} appears exactly once, at inversion, and it is unavoidable by the tightness example.

**Using an estimate of the channel.** If (X̂, Ŷ) are known only to precision η ≤ √k/2, then the error is ≤ ‖T̂^{-1}‖(δ + C(d)η), with k̂ ≥ k/4.

## Costs and polynomiality (charged)

- **Accuracy target.** Error ε needs δ = ε·k^{d/2}/C. Choosing δ = k^{20} gives error ≤ C·k^{16}.
- **Samples.** The sample cost is Õ(81·log(2^d/fail)/δ²) = Õ(k^{−40}).
  - First rotate the d target Majoranas onto the first k0 modes with a Gaussian unitary of O(N²) Givens rotations.
  - Then measure in at most 3⁴ local Pauli bases.
- **Alternative to rotating.** Rotated moments can be computed from original-frame moments. Each degree-2m monomial expands with ℓ₁ weight ≤ (2N)^m ≤ (2N)⁴. That multiplies the required precision by a polynomial factor.
- **When it is polynomial.** Everything is polynomial if and only if 1/k ≤ poly(n). The lemma does not rescue an exponentially small k. With k = 0 the method fails outright.

## Falsifiers and what the lemma does not cover

**Hypotheses the lemma needs:**
- **Wrong d modes.** If the d modes are fixed in advance rather than taken from the singular-vector frame of X, the restricted X can be singular or have tiny singular values even when the full channel is injective. The R ≥ kI hypothesis must hold for the modes actually measured.
- **Physical core.** Step 5 requires σ to be PSD and even.
- **Model error.** If the data are not of the form Ψ(σ) up to δ, the extra deviation must be added to δ.

**Scope:**
- The lemma says nothing about learnability of the full learner.
- It says nothing about hardness.
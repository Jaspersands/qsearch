# Review: ENERGY endpoint, native periodic conductivity

Status of this report: independent desk attack with no code execution. Everything below is either (P) proved here in text, (A) assumed from standard quantum-algorithm results I am confident of, (C) a finite control to be run by the parent, or (S) speculation. No novelty, advantage, or practical speedup is claimed.

## 1. Verdict

1. ENERGY is correct (P), including the unnormalized q, the zero-q case, and the direct-sum treatment of constants. Its rational Schur-complement form is the right Sage control.
2. The sketch in the admission file assembles into a complete algorithm. I give it below with registers, unitary blocks, fresh ancillas, precision, QSVT normalization, and an explicit error budget. Gate count: O(log(1/δ)·(ρ³/ε)·log(ρ/ε)·(B + n² + (n + log(ρ/ε))²)), i.e. poly(B, n, 1/ε, log 1/δ) at fixed ρ ≤ ρ₀, and in fact poly(ρ) too (P modulo the standard results listed as A).
3. The cheapest things that could have broken it do not: zero-mode routing, Ω(1/L) denominator, no postselection on q, no field extraction. The step that *would* fail, preparing q/‖q‖, fails on an explicit instance (§7).
4. Prior art: the supplied source (Sections 3.2–3.8) already does the hard part, a unit-subnormalization encoding of the preconditioned operator, for Q1 finite elements, and explicitly defers conductivity readout to a companion paper that is not supplied. The readout used here (Hadamard test + amplitude estimation on a block-encoding matrix element) is textbook. The endpoint is therefore "closed" in the sense of being a routine assembly; it is not a research contribution and may well coincide with the unsupplied companion paper. I cannot verify that.
5. Classical side: unchanged. No poly(B, n, 1/ε) classical algorithm for all circuits is known to me, and none is excluded. The Neumann-series route stays quasi-polynomial at best and still owes a torus kernel evaluator.

## 2. Model, and how it differs from the source's finite elements

Torus X = (Z/LZ)², L = 2ⁿ, N = L². Edge set E = X × {0,1}, edge (x,j) from x to x+e_j, |E| = 2N. Conductivity a_e ∈ {1,ρ} given by a size-B Boolean circuit χ(x,j) (χ=1 ⇔ a=ρ). D: ℂ^X → ℂ^E, (Dφ)_{(x,j)} = φ(x+e_j) − φ(x). η_j = N^{−1/2}·1_{dir=j}.

K_j = (1/N) min_φ Σ_e a_e (1_{dir(e)=j} + (Dφ)_e)² = min_ψ ⟨η_j + Dψ, a(η_j + Dψ)⟩ (substitute φ = √N ψ).

Differences from the source paper (Q1 elements, 2×2 Gauss):
- Local register: 2 gradient values per node here (one per edge direction) vs 8 per element there. No hourglass vectors t₂, t₃, no element weights W; the fixed unitary T of their Eq. (40) is not needed.
- Homogeneous symbol: Ŝ(k) = 4(sin²φ₁ + sin²φ₂), φ_j = πk_j/L, versus their Eq. (30) with the 2/3 cross term.
- S acts per edge, not per quadrature point; the material reflection is on (x,j).
- The output here is the discrete cell energy itself (a resistor-network effective conductance); their K_χ-energy norm bound (37) concerns a field, not this scalar.
- The source's "measured, not theorem" precision bound (41) with a constant 2.7×10³ is not imported; I derive the bit count for the two-component rotation directly.

## 3. ENERGY: proof, gauge, and controls (P)

Let S = diag(a)/ρ (entries in {1/ρ, 1}), K₀ = D*D, P₀ the projector onto constants, V = D K₀^{+1/2} (pseudo-inverse square root).

Facts: V*V = K₀^{+1/2}K₀K₀^{+1/2} = I − P₀; VV* = D K₀⁺D* = Π, the orthogonal projector onto range(D); ‖V‖ = 1. Also D*η_j = 0 (η_j is constant along each direction), so η_j ⊥ range(D).

Write Dψ = Vψ' with ψ' ⊥ constants (range of V on the complement is all of range(D)). Then
f(ψ') = ⟨η,Sη⟩ + 2Re⟨ψ', V*Sη⟩ + ⟨ψ', V*SVψ'⟩.
On the complement of constants, A := V*SV satisfies ⟨ψ',Aψ'⟩ = ⟨Vψ', S Vψ'⟩ ∈ [‖Vψ'‖²/ρ, ‖Vψ'‖²] = [1/ρ, 1]‖ψ'‖², so A is invertible there with inverse norm ≤ ρ. M := A + P₀ is invertible on all of ℂ^X with spectrum in [1/ρ,1]. q := V*Sη = K₀^{+1/2}D*Sη lies in range(K₀^{+1/2}) ⊥ constants. Minimizing: ψ' = −A⁺q = −M⁻¹q, and
min f = ⟨η,Sη⟩ − ⟨q, M⁻¹q⟩, hence K_j = ρ⟨η,Sη⟩ − ρ⟨q,M⁻¹q⟩. (ENERGY) ∎

Remarks proved along the way:
- The constant mode of M is analysis only; M⁻¹q = A⁺q because q ⊥ constants. Replacing P₀ by σ̄P₀ for any σ̄ ∈ [1/ρ,1] (what the circuit naturally produces, §4) changes nothing.
- q = 0 iff D*Sη = 0 iff a_{(x,j)} = a_{(x−e_j,j)} for all x, i.e. the direction-j conductivity is constant along direction j (constant media, layers parallel to the current). Then K_j = ρ⟨η,Sη⟩ = arithmetic mean, correct.
- Rational Schur form (what Sage should compute, no square roots): since (K₀^{+1/2}AK₀^{+1/2})⁻¹ = K₀^{1/2}A⁻¹K₀^{1/2} on the complement,
  ⟨q,M⁻¹q⟩ = ⟨D*Sη, (D*SD)⁺ D*Sη⟩, so K_j = (1/N)[⟨1_j, a1_j⟩ − ⟨D*a1_j, (D*aD)⁺D*a1_j⟩].
  This is exactly "direct rational minimization"; ENERGY is its K₀^{1/2}-conjugated form. The L=4 Sage control should (i) compute this rationally, (ii) compute ENERGY numerically with K₀^{+1/2} from the Fourier symbol, (iii) compare the circuit-form Π_e U_V Π_n against V (§4). Agreement of (i) and (ii) is forced by the algebra above; disagreement means a transcription bug.
- Analytic control, L=2 ring in 1D (two edges a₀,a₁ between the same two nodes): u = (1,−1)/√2, K₀^{+1/2} = ½uu*, Vu = (−1,1)/√2 =: v, q = u(a₁−a₀)/(2ρ), M = ((a₀+a₁)/2ρ)uu* + P₀. Then ⟨q,M⁻¹q⟩ = (a₁−a₀)²/(2ρ(a₀+a₁)), ⟨η,Sη⟩ = (a₀+a₁)/(2ρ), and ENERGY gives K = 2a₀a₁/(a₀+a₁), the harmonic mean, which is the series-resistor answer. Sign and constant-mode bookkeeping check out.

## 4. Unitary blocks

### 4.1 Registers
- pos: 2n qubits = two n-qubit coordinate registers (x₁, x₂), or (k₁,k₂) between the transforms.
- loc: 2 qubits = dir (edge direction j ∈ {0,1}) and flag. Edge space = {flag=0}; node space = {dir=0, flag=0}. Node vectors enter in |00⟩_loc; edge fields live in flag=0. The flag=1 subspace is the orthogonal workspace for the zero mode (the analogue of the source's states |8⟩–|15⟩).
- anc_S (one fresh qubit per application of U_S; two applications in the readout, one per QSVT query), anc_QSVT (1), anc_HT (1 Hadamard-test qubit), anc_AE (O(log(ρ²/ε))), work (arithmetic, returned to |0⟩).

Projectors: Π_n = I_pos ⊗ |00⟩⟨00|_loc ⊗ |0⟩⟨0|_anc, Π_e = I_pos ⊗ I_dir ⊗ |0⟩⟨0|_flag ⊗ |0⟩⟨0|_anc.

### 4.2 Material block U_S (P)
S = β₀I + β₁(−R_χ), R_χ = I − 2diag(χ) on (x,j), β₀ = (1+1/ρ)/2, β₁ = (1−1/ρ)/2; check χ=1:
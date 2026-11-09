# Audit: uniform stability/completion for the two-Fock spectral learner

**Verdict (deduction-level, conditional on items in §5):** I could not break the completion. The sequential rounding is exact by construction, the common frame requires no gap, and the cat phase / p↔1−p ambiguity (invisible to all moments of order ≤4) is closed by the final two-dimensional block tomography. A concrete polynomial allocation is given in §4; the contract's δ is far more than sufficient. Two source-level items remain open (§5).

## 1. Mechanism checks (proved here, modulo one convention)

- Cross elements: G even ⇒ G†(quartic)G is a sum of physical quartic monomials, each changing ≤4 occupations; k even ≥6 ⇒ zero. So C = pJ0+(1−p)J1 = B+(2p−1)J and T = pW(J0)+(1−p)W(J1).
- W is a quadratic form, so with J0,1 = B±J: T = W(B)+W(J)+(2p−1)·cross, W(C) = W(B)+(2p−1)²W(J)+(2p−1)·cross, hence K = 4p(1−p)W(J). ✓
- Flattening: Σ_{c<d}W_abcd X_cd = ⟨J,X⟩J_ab + (JXJ)_ab (both Wick terms contribute +½JXJ). ✓ Entries with overlapping index pairs vanish identically (J_aa=0), so set them to 0 in K̂ without estimation.
- Spectrum on the active 2k-space: L_J(J)=(k−1)J; X↦JXJ is an involution, eigenvalue +1 on anticommuting X (mult. k²−k), −1 on commuting X (mult. k²−1 after removing J). Top |λ| = a(k−1), next a, gap a(k−2) ≥ 4a. ✓
- Convention risk: if the sign of T is flipped the top eigenvalue becomes the most negative one. Use the eigenvector of **largest |λ|**; this is convention-agnostic since a(k−1) > a for k ≥ 3.
- Excitation identity: for pure Γ,Γ', ‖Γ−Γ'‖_F²/8 = Σ_j(1−Γ_{2j−1,2j})/2 in Γ'’s Fock frame = expected disagreement count ≥ infidelity. ✓ (Uses Tr Γ^TΓ = 2n.)
- Parity toggle: γ1G = (γ1Gγ1)γ1 with γ1Gγ1 even Gaussian, so X1ψ = G̃(α'|x⊕e1⟩+β'|y⊕e1⟩), same class, same k. ✓

## 2. Attacks on simultaneous rounding / common frame

- "Simultaneous" rounding never occurs: Ĵ = polar of the top-k-pair Schur truncation of √k·v̂ (antisymmetric ⇒ polar factor is an exact complex structure on its range P̂); then B̂ = polar of P̂⊥ĈP̂⊥ on P̂⊥ (even dimension, nonsingular once ‖M−B‖_op<1). B̂Ĵ = ĴB̂ = 0 exactly, so Ĵ0,1 = B̂±Ĵ square to −I exactly. No joint-approximation step to break.
- Common frame: Ĵ0 is an exact orthogonal antisymmetric matrix; P̂ is Ĵ0-invariant, so a block-compatible normal form exists with Ĵ1 flipping exactly k blocks. No covariance-gap input anywhere; frame non-uniqueness is a Fock-string-preserving Gaussian, harmless.
- Rounding stability without gap: Mirsky gives ‖polar(X_2k)−X_2k‖_F ≤ ‖X−J‖_F, hence ‖Ĵ−J‖_F ≤ 3‖X−J‖_F and ‖B̂−B‖_F ≤ 2‖M−B‖_F, ‖M−B‖_F ≤ 2nδ+4‖Ĵ−J‖_F.

## 3. Attacks on amplitude-uniformity and cat phase

- Small-amplitude regime (min(p,1−p) ≤ s): generic rounding bounds would suggest infidelity ∼ k s², i.e. a threshold not uniform in n. This does not materialize: C = J0(P⊥+|2p−1|P) with commuting positive factor, so polar(C) = J0 **exactly**; noisy polar is Lipschitz with constant ≤ 2/(1−2s−2nδ), giving branch infidelity ≤ 2n²δ². Candidate infidelity ≤ (1+√2)(s+2n²δ²). Contract's s = ε²/10⁴ is fine for all n. (Recommend recording the polar identity in the contract; the generic bound is misleading.)
- Cat phase: C depends only on p, K only on a = 4p(1−p), and v̂ is defined up to sign (branch relabeling). Hence moments ≤4 are blind to the relative phase and to p↔1−p; this is not a defect since the completion is pure tomography in span{Ĝ|x̂⟩,Ĝ|ŷ⟩}. Projection of ψ onto that span has norm² ≥ 1−η0−η1 (|α|√η0+|β|√η1 ≤ √(η0+η1)), and the projected block is exactly rank one (vv†), so its top eigenvector is the full answer including phase. Off-diagonals are bounded observables (CNOT ladder + Hadamard on the k differing qubits, Z-projectors elsewhere), values in {−1,0,1}; no postselection.
- Algorithm never needs to know the regime: all candidates are produced; selection by all-zeros probability after inverse preparation is unbiased.

## 4. Concrete allocation (targets: good-candidate infidelity ≤ ε²/4, selection error ε²/8, output trace distance ≤ √(3/8)ε)

- s = ε²/10⁴; in the main regime a ≥ 2ε²/10⁴.
- Entrywise δ for all ≤ n⁴ two/four-point Paulis. Error propagation: |K̂−K| entries ≤ 8δ; ‖E‖_op ≤ 16n²δ; Davis–Kahan ‖v̂−J/√k‖ ≤ 12n²δ/a; ‖Ĵ−J‖_F ≤ 51n^{2.5}δ/a; ‖Ĵ_i−J_i‖_F ≤ 463n^{2.5}δ/a. Requiring ≤ ε/2 (branch infidelity ≤ ε²/32): **δ = ε³/(5·10⁶ n^{2.5})** suffices; it also gives ‖E‖_op < gap/2 and n²δ² negligible in the small regime. The contract's δ = ε¹⁰/(10²⁰(n+1)¹⁰) is therefore sufficient (proved, not just plausible), at a sampling cost ∼ n²⁴ε⁻²⁰ versus ∼ n¹¹ε⁻⁶ for the tighter choice.
- Copies: n⁴·2δ⁻²ln(2n⁴/η) for moments; 4 observables at τ = ε/40, O(ε⁻²log(1/η)) for the block (sin θ ≤ ε/4.5); O(n) candidates × O(ε⁻⁴log(n/η)) for selection. All polynomial.
- Classical: O(n²)-square eigenproblem, polar decompositions, normal form, Givens compilation of Ĝ — polynomial time; floating-point error budget not worked out here (routine but unproved).

## 5. Open obligations (not resolvable from the packet)

1. Sign convention of T relative to W must be confirmed once numerically; the |λ| rule removes dependence on it, but the identity K = aW(J) presumes the same Wick sign in T and W(C).
2. k ∈ {2,4}: absorbing the common Fock string into the Gaussian uses a product of |z| Majoranas, odd if |z| is odd. Either verify the cited compressible learner (Mele–Herasymenko) admits odd Gaussian unitaries, or absorb one occupied mode into the compressed block (t ≤ 5). Also verify the source's guarantee is uniform in the branch amplitudes (its subspace identification faces the same near-Gaussian degeneracy); treated as source assumption.
3. Amidi 2610.08723 overlap check (per contract) remains unperformed here.

## 6. Falsifiers

- n=8, k=6, random G, p ∈ {0.5, 0.3, 10⁻³}: largest-|λ| eigenvector of exact K must equal ±J/√6 with |λ| = 5a; failure ⇒ convention/flattening error.
- Add i.i.d. noise δ = ε³/(5·10⁶n^{2.5}) to all moments and run the pipeline; any instance with output trace distance > ε at min(p,1−p) > ε²/10⁴ falsifies §4.
- p = 1−ε²/10⁴, k = n: polar(Ĉ) candidate must achieve infidelity ≤ 2.5ε²/10⁴ + O(n²δ²) for all n; growth with n falsifies the polar-identity argument.

No speedup or hardness is inferred; the claim is only a polynomial copy/time count for this restricted class.
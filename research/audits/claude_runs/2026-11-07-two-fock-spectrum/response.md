# Audit of the exact fourth-cumulant spectral mechanism in the two-Fock-string contract

**Scope.** This audit covers only the exact (noiseless) mechanism. I could not access the repository or check the SHA256 hash, so I audited the pasted contract text.

## Verdict

The exact mechanism is **correct as stated**, for every even k ≥ 6 and every 0 < p < 1.

- I found no counterexample inside the declared regime.
- There are no exceptional k among even k ≥ 6.
- The cheapest decisive attack is at k = 4, which the contract already excludes. There the hypothesis fails in a direct, constructive way (see below).
- The extracted direction, combined with the two-point covariance C, determines the unordered pair {J0, J1} exactly.

Two side observations, both about the exact case:

- **The k-loop is unnecessary.** k equals half the rank of the extracted eigenvector.
- **The quartic data is only needed near p = 1/2.** For p ≠ 1/2, the active space is already visible in the spectrum of C.

## Counterexample attempts (cheapest first)

**1. k = 4 cross term (boundary of the claim).** Take n = 4, x = 0000, y = 1111, and the operator γ1γ3γ5γ7.

- This monomial flips all four modes, so |⟨x|γ1γ3γ5γ7|y⟩| = 1.
- The moment T therefore picks up a term 2Re(ᾱβ·…), and the identity K = aW(J) fails.
- This is consistent with the contract's restriction to k ≥ 6. The general bound: a Majorana monomial of degree ≤ 4 flips at most 4 Jordan–Wigner occupations. Conjugating by G maps γ to Rγ, which preserves degree. So cross terms vanish exactly when k ≥ 5. Under the same-parity condition k is even, so the threshold is k ≥ 6.
- At k = 2, quadratic cross terms also survive, and in addition the spectral gap is zero (see the spectrum below).

**2. Explicit k = 6 numerical check.** Take x = 0^6, y = 1^6, G = I. Then J = J0, B = 0, and C = (2p−1)J.

- Entry (1,2,3,4): with ⟨γ1γ2⟩ = −iΓ12 = −i, the raw moment is (−i)(−i) = −1 on both branches. So T = +1. Also W(C) = (2p−1)², so K = 1 − (2p−1)² = 4p(1−p) = a·W(J)₁₂₃₄. ✓
- Entry (1,3,2,4): raw = +1, T = −1, and W(J) = −1. ✓

**3. Trace checks of the claimed spectrum.** Both pass (computed in the proof below).

## Self-contained proof

**Conventions.**
- Majoranas satisfy {γa, γb} = 2δab.
- Covariance: Γab = (i/2)⟨[γa, γb]⟩. For a ≠ b this gives ⟨γaγb⟩ = −iΓab.
- Pure Gaussian states have real antisymmetric Γ with Γ² = −I.

**(i) Signs.**
- For distinct a, b, c, d, the operator γaγbγcγd is Hermitian: reversing four factors gives sign (−1)^6 = +1. It is therefore a signed Pauli string under Jordan–Wigner.
- Wick's theorem gives ⟨γaγbγcγd⟩ = (−i)²[ΓabΓcd − ΓacΓbd + ΓadΓbc] = −W(Γ)abcd.
- Since W is quadratic in Γ, this holds under either sign convention for Γ. So T := −(raw moment) equals W(Γ) on Gaussian states, as the contract claims.

**(ii) The mixture identity.**
- Because cross terms vanish for k ≥ 6, T = pW(J0) + (1−p)W(J1).
- J0 and J1 are J_x and J_y rotated by the same orthogonal R. In a common frame they are block-diagonal with sign flips on the k active blocks. Hence:
  - they commute;
  - J is supported on the active space;
  - P = −J² is the active projector, of rank 2k;
  - B = Q J0 Q, with Q = I − P, and B is a complex structure on P⊥.
- Algebraically, C = pJ0 + (1−p)J1 = B + (2p−1)J.
- Let W(X,Y) be the symmetric bilinear form with W(X,X) = W(X). Then T = W(B) + W(J) + 2(2p−1)W(B,J).
- Also W(C) = W(B) + (2p−1)²W(J) + 2(2p−1)W(B,J).
- Subtracting gives K = T − W(C) = [1 − (2p−1)²]W(J) = 4p(1−p)·W(J). ✓

**(iii) Repeated indices.** W(J) vanishes whenever two indices coincide. For example, W_abad = J_ab J_ad + J_ad J_ba = 0. In fact W is totally antisymmetric, proportional to J∧J. So only distinct-index four-point means are needed, and the diagonal blocks of the flattening are zero.

**(iv) Flattening.** Index pairs by a < b, which makes them orthonormal under ⟨X,Y⟩ = Tr(XᵀY)/2. Then

(MX)ab = ½Σcd W_abcd X_cd = J_ab⟨J,X⟩ + ½(JXJ)ab + ½(JXJ)ab.

Here I used Jᵀ = −J and Xᵀ = −X. So M = L_J with L_J(X) = ⟨J,X⟩J + JXJ. ✓

**(v) Full spectrum.** Split X into its PP, mixed (PQ + QP), and QQ blocks.

- Both terms of L_J annihilate the mixed and QQ blocks, so L_J is zero there. This covers n(2n−1) − k(2k−1) dimensions.
- On active antisymmetric X, which has k(2k−1) dimensions:
  - L(J) = kJ + J³ = (k−1)J, using ⟨J,J⟩ = Tr P / 2 = k.
  - The map S(X) = JXJ satisfies S² = id on the active space. It also preserves J⊥, since ⟨J, JXJ⟩ = −⟨J,X⟩.
  - S = −1 on matrices commuting with J. This is a copy of u(k), of dimension k², and it contains J.
  - S = +1 on matrices anticommuting with J, of dimension k(k−1).

The resulting spectrum of L_J is:

| Eigenvalue | Multiplicity | Eigenspace |
|---|---|---|
| k − 1 | 1 | J |
| +1 | k(k−1) | anticommuting with J |
| −1 | k² − 1 | u(k) ⊖ J |
| 0 | the rest | mixed and inactive blocks |

**Checks.**
- Trace: (k−1) + k(k−1) − (k²−1) = 0, which equals Σ W_abab = 0. ✓
- Trace of L²: (k−1)² + k(k−1) + (k²−1) = 3k(k−1). This equals 6·C(k,2), the direct count of ±1 entries of W. ✓

**Consequence for K = aL_J.**
- The top eigenvalue is a(k−1).
- The eigenvalue gap to the next eigenvalue (+a) is a(k−2), and it is also a(k−2) in absolute value.
- The unit top eigenvector is ±J/√k. ✓
- This requires a > 0 (i.e. 0 < p < 1) and k ≥ 3. Within the regime, k ≥ 6, so the gap is at least 4a.

**(vi) Determination of the branches.**
- The unit eigenvector u = ±J/√k has rank 2k and all nonzero singular values equal to 1/√k. So k and P are read off from u, and J = √k·u up to sign.
- Since B = QBQ, J = PJP, and the mixed blocks of C vanish, we get B = QCQ exactly.
- Hence {J0, J1} = {B + J, B − J}.
- The sign ambiguity J → −J swaps the two branches (equivalently p ↔ 1−p), so the unordered pair is determined.
- As a byproduct, ⟨J,C⟩ = (2p−1)k recovers p up to the same swap.
- Remark: C has singular value |2p−1| on P and 1 on Q. So K is essential only when p ≈ 1/2.

## Exceptional k

| k | Status |
|---|---|
| Even k ≥ 6 | No exceptions. |
| k = 4 | Quartic cross terms are present (explicit witness above). |
| k = 2 | Quadratic and quartic cross terms are present, and the gap is zero. |
| Odd k | Excluded by the parity condition. Without that condition, k = 5 would also work. |
| p ∈ {0, 1} | K = 0. The state is Gaussian, which the contract handles separately. |

## Not audited — remaining obligations

1. **Robustness.** Required precision δ versus the gaps a(k−2) and 1/√k for singular-value rounding, the behaviour of polar rounding of QCQ, and whether the stated δ suffices. All unproved.
2. **Frame realisation.** If the normal-form O has det O = −1, it must be fixed by reorienting one mode. This flips one bit in both strings and is harmless, but should be stated.
3. **Downstream steps.** The relative phase, the 2×2 block tomography without postselection, model selection by fidelity, and the stability bound ‖Γ−Γ′‖²_F/8. Plausible but unchecked here.
4. **k ≤ 4 learner and sources.** The fixed-4 learner and the cited sources (Mele/Herasymenko, Sen, Amidi) were not checked. No novelty or overlap judgment is made.
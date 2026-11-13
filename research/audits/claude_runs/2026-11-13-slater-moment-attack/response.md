# Verdict: the bound survives within the stated architecture

I found no loophole. **Every output law of this architecture has TV ≥ 1008/8425 ≈ 0.1196 from the target.** The argument is a proved deduction, not a finite control. It is not tight in any claimed sense: it is a lower bound from one event.

## Arithmetic, re-derived independently

- **Slater expansion.** (3a†+4c†)(4b†+3d†)/25 = (12 a†b† + 9 a†d† − 16 b†c† + 12 c†d†)/25. The sign comes from c†b† = −b†c†. The norm is 144+81+256+144 = 625.
- **Records.** Pair parities are (p₁,p₂):
  - |ab⟩ gives (2,0), even/even.
  - |cd⟩ gives (0,2), even/even.
  - |ad⟩ and |bc⟩ give odd/odd.
  
  So there are exactly two records, with probabilities 337/625 and 288/625. The branch states O and E are as stated.
- **Target.** The valid support is {ac, ad, bc, bd}. Q Φ ∝ 9|ad⟩ − 16|bc⟩, so P_target(a occupied) = P(ad) = 81/337.

## Covariance facts

- **Convention.** With c₁ = a + a† and c₂ = −i(a − a†), we have c₁c₂ = −i(2n−1). So M₁₂ = i⟨c₁c₂⟩ = 2⟨n⟩ − 1, and in general ⟨n_j⟩ = (1 + M_{2j−1,2j})/2.
- **Branch E.** |ab⟩ and |cd⟩ differ in all four modes. No quadratic monomial connects them, and a quadratic monomial acting on either one gives zero overlap with E. Every ⟨n_j⟩ = 1/2, so M_E = 0.
- **Branch O.** |ad⟩ and |bc⟩ also differ in four modes. Hopping or pairing terms map them outside the support of O. Therefore M_O is block-diagonal with entries 2n_j − 1 = ∓175/337, and its operator norm is 175/337.

## Step-by-step check of the architecture

1. **Gaussian unitaries act orthogonally on any state.** U†c_kU = Σ_l R_{kl}c_l is an operator identity (Eq. 5 of the excerpt, with R ∈ SO(2n)). Taking its expectation in any ρ gives M(UρU†) = R M Rᵀ, regardless of whether ρ is Gaussian. The direction convention (V c V† versus V† c V) only replaces R by Rᵀ. Including parity-odd reflections, such as conjugation by a single Majorana operator, only extends this to O(2n). The bound survives even that extension.
2. **Pairing terms are included.** Pairing is already inside SO(2n), so number-nonconserving unitaries are covered.
3. **Single-mode bound.** |M_{2j−1,2j}| ≤ ‖M‖_op. Therefore ⟨n_j⟩ ∈ [(1−σ)/2, (1+σ)/2], where σ is the largest singular value of M. This interval is invariant under every Gaussian unitary.
4. **Randomness and feedforward.** Occupation expectations are linear in the state. The bound therefore holds term by term over:
   - classical randomness,
   - record-conditioned choices, including altering the "successful" O branch,
   - products of Gaussian unitaries.
5. **Combining the branches.**
   - P_out(a) ≥ (337/625)(81/337) + (288/625)(1/2) = 225/625 = 9/25.
   - This bound is attained by applying the identity on both branches.
   - Since "a occupied" is an event in the full occupation alphabet, TV ≥ 9/25 − 81/337 = (3033 − 2025)/8425 = 1008/8425.

Loopholes I checked and rejected:
- Two records only: p₁ = p₂ is forced because total parity is even.
- Pure post-measurement branches.
- Global phases.
- Time-dependent quadratic Hamiltonians, which compose to Gaussian unitaries.

## Reusable mathematical fact

For an n-mode state ρ, the singular values of its Majorana covariance M(ρ) are invariant under all ancilla-free Gaussian unitaries. Consequently, for any architecture of the form "measured record r → random Gaussian unitary on the same modes → occupation measurement":

> Σ_r p_r (1 − σ_max(M_r))/2 ≤ P(n_j = 1) ≤ Σ_r p_r (1 + σ_max(M_r))/2.

Any target whose single-mode marginal lies outside this interval is excluded, with a TV gap at least the distance to the interval. In particular, a branch with M = 0 is pinned to marginal 1/2. This is exactly what separates the present example from the earlier singlet case, whose target marginal was 1/2 and was therefore compatible with the pinned branch.

## Exact scope

The result covers:
- this two-site, four-mode instance;
- a projective per-pair parity measurement on Φ, with no prior operation;
- arbitrary randomized, record-conditioned unitaries in SO(2n), or even O(2n);
- a fixed-basis occupation readout on the same modes.

It does not cover, and the bound can fail for:
- **Gaussian ancillas or non-unitary Gaussian channels such as loss or reset.** These contract M, for example swapping in a vacuum ancilla to empty mode a in branch E.
- **Additional measurements, postselection, or rejection.**
- **Non-Gaussian corrections.**
- **Gaussian operations before the parity measurement.**
- **Final readout in rotated modes, or arbitrary classical relabeling.** Relabeling is the mechanism behind the earlier singlet repair.
- **General classical sampling.**

No novelty, all-algorithm no-go, hardness, or speedup claim follows.

## Falsifiers and proof obligations for the parent

- **Re-verify Eq. 5 against the primary PDF.** I only saw the excerpt, and I did not verify the SHA256 hashes. Specifically confirm that the Heisenberg action is a real orthogonal map on Majorana operators.
- **Confirm the measurement model.** "Coarse parity measurement" must mean the projectors onto pair-parity subspaces. A weak or non-projective implementation is outside this proof.
- **Confirm the alphabet.** "Physical occupations" must mean the a, b, c, d number basis.
- **Any counterexample must leave the architecture.** It would require an allowed operation whose covariance action is not R·Rᵀ. Any such operation is by construction outside the stated architecture.
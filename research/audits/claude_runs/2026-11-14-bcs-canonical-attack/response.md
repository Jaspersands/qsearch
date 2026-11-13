# Review: classical BCS canonical Born sampler

## Verdict

I found **no decisive mathematical or source-hypothesis error** in the supplied composition. The sampler checks under the stated hypotheses, subject to two **source obligations** that the excerpts cannot discharge (O1, O2 below). One clause should be **replaced, not merely charged**: the small-coupling branch (R1). With that repair, 1/g disappears as a resource.

Neither the finite Sage controls nor the absence of a counterexample is evidence for an all-input theorem. What follows is a deduction check only.

## Checked composition (only the steps that could fail)

**1. Sector convexity.** In sector m, T_m = gA_J − g·m(N−m) − D = −H_m − g·m(N−m), so r_m = −E_m − g·m(N−m).

- T_m is symmetric, and the all-ones vector has positive overlap with a nonnegative top eigenvector. Hence dim⁻¹·c_m ≤ e^{t r_m} up to constants, and lim (1/t) log c_m(t) = r_m. Irreducibility is not even needed.
- I recomputed the identity (m+1)(N−m−1) + (m−1)(N−m+1) − 2m(N−m) = −2. Combined with 2r_M ≥ r_{M−1} + r_{M+1}, this gives E_{M+1} + E_{M−1} − 2E_M ≥ 2g. **Correct.**
- Stability preservation follows from BBL Prop 5.1 for gL and from the positive rescaling z_i → e^{−t·eps_i}z_i, with Trotter limits that stay stable and nonzero since coefficients are positive. Wei Thm 7.1 independently covers this case.

**2. Grid.** The admissible μ-interval has width ≥ 2g, so a point at distance ≥ g/2 from both endpoints lies on a g/4-spacing grid.

- Convexity of m ↦ E_m − μm makes sector M the unique global minimiser, with margin ≥ g/2.
- This step is needed only for **existence** of an acceptable grid point. Correctness never uses it.

**3. Conditioning invariance.** H conserves N̂. Hence Π_M e^{−β(H−μN̂)} Π_M ∝ e^{−βH_M}, which is independent of μ.

- The canonical-to-ground distance is ≤ C(N,M)·e^{−βκ}.
- With β ≥ C(N + log 1/τ)/min(κ, g), both this canonical error and the off-sector mass at the good μ are ≤ τ.
- The mixture over accepted points is harmless. **Correct.**

**4. Anisotropy repair.** Take a = g/2 + λ and b = −g/2. Then |b| ≤ a, a − b = g + λ, a + b = λ, so c_min = λ exactly, and the model stays stoquastic.

- Gibbs relative entropy obeys S ≤ β·Tr ρ(H′−H) + log(Z′/Z) ≤ 2β‖ΔH‖.
- With ‖ΔH‖ ≤ λN²/2 and λ ≤ cτ²/(βN²), Pinsker gives TV ≤ O(τ). **Correct.**

**5. Trotter state bound.** If δB ≤ 1/10, then ‖C − I‖ ≤ e^{δB} − 1 and CC† = I − 2δH_pert + R with ‖R‖ = O(δ²B²).

- In particular ‖CC† − I‖ < 0.25, so the principal logarithm exists.
- (CC†)^L = exp(−2δL·H_eff) = exp(−βH_eff) **exactly**, with ‖H_eff − H_pert‖ = O(δB²).
- Relative entropy ≤ 2β·O(δB²) = O(β²B²/L). Choosing L ≍ β²B²/τ² suffices. **Correct.** This replaces source Theorem 1, which is only a partition-function bound, as the note requires.
- The first-slice marginal of π₀ on C₀ is ⟨σ|(CC†)^L|σ⟩/Z̃, which is nonnegative.

**6. Zero-defect mass (source Lemma 2).** The step (C7)→(C8), Σ s_k^{K_a+K_b} ≤ O(1)·Σ s_k^L, is **not** generally valid when s_k < 1.

- It holds here only because s_k(CC†) ≥ 1 − 2δB − O(δ²B²) ≥ 1/2. Then s_k^{−2} ≤ 4 and K_a + K_b ≥ L − 2 give the O(1) factor.
- **Record this dependence on δB ≤ 1/10 explicitly.** It is satisfied in the note's regime.
- Result: mass(C₂)/mass(C₀) ≤ O(M_ops²), so p₀ := π(C₀) ≥ 1/poly.

**7. Conditioning amplification.** Two conditionings occur:

- on C₀, with factor 1/p₀;
- on Hamming weight M, with factor ≤ 4 at accepted points, since accepted means ideal mass ≥ 1/2 − 1/16 − O(τ) ≥ 1/4.

The required chain accuracy is therefore δ_mix ≤ c·τ·p₀/4, and the cost enters only through ln(1/δ_mix). This is polynomial. The note "charges" this, but should write the 1/p₀ factor into the clock explicitly.

**8. Finite bits.** All local weights are rationals built from δ, λ, (eps_i − μ) and g, so Metropolis ratios are exact rationals.

- Dyadic rounding of each coin to accuracy τ/(4T_chain), with a telescoping coupling over T_chain steps, costs O(log(T_chain/τ)) bits per step.
- The initial all-zero path gives ln π(x)⁻¹ ≤ n + O(β′Σ|d_i| + β′n²a), which is polynomial.

## Source obligations (not errors, but unverified)

**O1. L-dependence of the mixing proof.** The source states congestion as O(n¹⁰β⁵ε⁻³)·c_min⁻¹ under its own choice L = Θ(n²β²/ε). The note uses a **different, larger** L.

- *Obligation:* restate the mixing bound as poly(n, β′, L)·c_min⁻¹. This could be done via ε_eff := n²β′²/L, checking that every use of ε in eqs 28, 36 and 44–45 enters only through δ = β′/2L and M_ops = Θ(n²L).
- *Falsifier:* any step needing L ≤ poly(n, β)/ε with ε tied to the partition-function guarantee rather than to δ.

**O2. Where c_min enters.** The excerpt shows c_min⁻¹ only in the C₂–C₂ rerouting term (42)–(43). Eqs 28/36 and the claim "P(z,z′) ≥ 1/poly(n, β, ε⁻¹)" are not in the excerpt.

- With a + b = λ, any move creating a 00↔11 vertex has acceptance ∝ δλ. So the P(z,z′) lower bound **must** degrade with λ.
- *Obligation:* verify the total exponent of c_min⁻¹ across eqs 28, 36 and 44–45, and that no step uses c_min ≥ const (e.g., a ratio bound like eq 46 dividing by δ(a+b)).
- Any **finite** exponent keeps the bound polynomial, since 1/λ = poly(β, N, 1/τ).
- *Decisive falsifier:* a step where c_min appears inside an exponential, or as c_min^{−M_ops}.

Neither obligation is refuted by anything supplied. Until both are checked line-by-line in the full source (LF 600–780 and eqs 44–45), the mixing claim is **source-conditional**.

## Exact repair R1: remove 1/g entirely (replaces the Δ-clause)

As written, "polynomial native inverse spacing" is **not** implied by the input bits. With eps_M = 0 and eps_{M+1} = 2^{−n}, the bit length is O(n) but 1/Δ = 2^n. Use the promised κ instead.

Let γ be the true sector-M gap, with κ ≤ γ. Weyl's inequality gives |γ − Δ| ≤ 2‖gA_J|_M‖ ≤ gN²/2.

- **Branch A: gN² ≤ cτκ (c ≤ 1/8).**
  - Then Δ ≥ κ − gN²/2 ≥ 3κ/4 and ‖gA_J‖ ≤ κ/8.
  - Davis–Kahan gives sin θ ≤ ‖gA_J‖/(Δ − ‖gA_J‖) ≤ (cτκ/4)/(κ/2) ≤ cτ/2.
  - Born TV ≤ sin θ ≤ τ. **Output the M-lowest monomial.**
- **Branch B: otherwise.**
  - Then 1/g < N²/(cτκ), so β ≤ poly(N, log 1/τ, 1/τ, 1/κ).

The branch test uses only input data (g, N, τ, κ). If g = 0 exactly, branch A applies, with the distinct-eps promise giving Δ > 0 consistently with κ.

**Resulting clock:** poly(N, bits, 1/τ, K/κ), where K ≥ ‖H‖. This should be stated in the scale-invariant ratio K/κ: rescaling to the source range |d_i| ≤ 1 and a ≤ 1/2 multiplies β by s ≈ K. "Polynomial in 1/κ" alone is not scale-correct, because eps magnitudes can be 2^{bits}.

## Checked-gap status

| Item | Status |
|---|---|
| Zero-defect mass | Holds; needs δB ≤ 1/10 for (C7)→(C8); 1/p₀ charged in δ_mix |
| Vanishing/small g | Repaired (R1); no 1/g or 1/Δ resource remains |
| Finite-bit weights | Holds; rational exact ratios plus dyadic coin coupling |
| Source mixing dependence | **Conditional on O1, O2** |
| Conditioning amplification | Holds; factor ≤ 4·(1/p₀), logarithmic in the clock |
| Promise failure | **Not certified.** If κ is false, the output is ungaranteed; the same holds for the quantum route |

## Consequence for the next scientific action

Conditional on O1 and O2, the comparison stands as follows.

- **Matched:** Born readout of the fixed-M BCS ground state, under the same final-gap promise. It is classically sampleable in poly(N, bits, 1/τ, K/κ).
- **What remains is not a speedup:** a gapped quantum preparation could achieve poly log(1/τ) precision dependence, against the classical poly(1/τ). That difference is polynomial and gives no separation.
- **Not matched:**
  - coherent state preparation;
  - non-diagonal observables beyond what the loop sampler estimates;
  - arbitrary interacting excited branches.
- **Not shown:** an internal fixed-M gap from convexity or from the three finite controls.

**Recommended next action:** discharge O1 and O2 against the full source text, specifically the exponent of c_min⁻¹ and the L-only dependence. Do this before any quantum coding for Born-readout targets. If either fails with super-polynomial c_min dependence, the decisive falsifier is an XY instance family where the λ → 0 chain provably freezes, e.g. a conductance bound through 00↔11 vertex moves ∝ δλ that is exponential in N. That outcome would reopen the comparison.
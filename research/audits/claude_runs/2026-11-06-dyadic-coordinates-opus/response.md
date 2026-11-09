# Verdict on the dyadic squareclass algorithm in coordinate_lemma.md

**Verdict: no counterexample found.** Under the paid order/uniformizer/residue contract and the stated valuation bound, the proposal is a complete, exact algorithm that runs in polynomial bit time. Its output map

a ↦ (m mod 2, w mod R̄) ∈ F₂ × F₂^k/R̄, where R̄ = (R + 2Zᵏ)/2Zᵏ,

is a group isomorphism E*/E*² → F₂^{n+2}. The one inaccuracy found is a conservative precision constant, which is harmless. Below, ✔ marks a deduction proved here, and **[A]** marks an assumption carried from the contract.

## 1. Structural reduction (✔ proved)

1. **Decomposition.** E* = π^ℤ × μ_{2^f−1} × U₁.
2. **Teichmüller units are squares.** μ_{2^f−1} has odd order, so squaring is a bijection on it. Hence μ_{2^f−1} ⊂ E*².
3. **Unit squares inside U₁.** Suppose x = y² ∈ U₁ with y = π^k ζ w. Then k = 0, and ζ² ∈ U₁ ∩ μ_odd = {1}. So x = w², which gives U₁ ∩ E*² = U₁². It follows that E*/E*² ≅ ℤ/2 × U₁/U₁².
4. **Odd powering preserves the squareclass.** u^{2^f−1} = u · (u^{(2^f−2)/2})². The power lies in U₁ because the residue of u has order dividing 2^f−1. So the "odd residue Teichmüller units" concern is fully dissolved.
5. **Truncation is valid.** Hensel's lemma on y² − (1+t) at y = 1 needs v(t) > 2v(2) = 2e. Since N = 3e ≥ 2e+1, we get U_N ⊂ U₁².
   - Therefore U₁/U₁² = (U₁/U_N)/(U₁/U_N)². The image of U₁² in U₁/U_N is exactly (U₁/U_N)².
   - N = 2e+1 would also suffice.
6. **Quotient identification.** With φ: ℤᵏ ↠ U₁/U_N and R = ker φ, we have (U₁/U_N)/(·)² ≅ ℤᵏ/(R + 2ℤᵏ). This is correct, and only R mod 2 is ever needed.
7. **Homomorphism check.** u(ab) = u(a)u(b) and m is additive, so the coordinates are a well-defined homomorphism with kernel E*². The coordinate frame depends on (π, residue basis, lifts). No cross-run canonicity is claimed, consistent with the proposal.

## 2. Full kernel, not saturation (✔ proved by induction)

**Claim.** M_j = φ⁻¹(U_j/U_N) for every j.

**Proof.**
- Each U_j/U_{j+1} ≅ (F_{2^f}, +) via 1 + π^j x ↦ x̄. This holds because (1+π^j x)(1+π^j y) = 1 + π^j(x+y) + π^{2j}xy, and the cross term lies in π^{j+1}O.
- Hence ψ_j: M_j → F₂^f, defined by c ↦ leading digit of φ(c), is a group homomorphism. Its kernel contains 2M_j.
- Therefore ker ψ_j = C · {a : a mod 2 ∈ ker(ψ_j mod 2)} = C · (lift(ker) + 2ℤᵏ), where C is the current basis matrix.
- Then M_{j+1} = ker ψ_j exactly, and M_N = R. No saturation or rational closure is taken anywhere.

**Carries.** Mixed-characteristic carries do not break this. ψ_j is evaluated on the actual product φ(c_i) computed in O/8O, never on a digit-wise linearization of the g-exponents. The only property used is that the U_j/U_{j+1} are groups.

**Required implementation detail.** Each φ(c_i) for c_i ∈ M_j must be checked to lie in U_j. Failure of this check falsifies the implementation.

**Surjectivity.** Digit peeling from j = 1 to N−1 leaves a residual in U_N, so the g_{j,l} generate U₁/U_N. Each step solves π^j z ≡ u−1 (mod π^N) as a linear system over ℤ/8. The solution z is defined modulo π^{N−j}, so z̄ is well-defined because j < N.

## 3. Finite-ring precision (✔, with one constant corrected)

**Normalization.** Let a′ = a + δ with δ ∈ 2^P O.
- Since eP > V > m, we have v_E(a′) = m. Since fm < nV < P, v₂(det L_{a′}) = fm is readable modulo 2^P.
- Since δ ∈ π^m O, a′ ∈ π^m O, and the solution u′ satisfies u′ ≡ u mod 2^{P−⌈m/e⌉}O.

**Correction.** The true loss is ⌈m/e⌉ digits, not fm. The fm figure is a valid bound only for the generic Cramer-solve error analysis. Either way, P > nV+4 leaves at least 3 digits, so u mod 8O is exact.

**Ring identification.** O/8O = O/π^{3e} because π^e = 2·unit. All later steps (inversion, powering by 2^f−1, digit extraction, φ evaluation) are exact ring or linear operations over (ℤ/8)ⁿ.

**[A] Table precision.** The multiplication table and π must be supplied to at least P + fm bits. If they are exact integers, this holds trivially. I treat it as part of the paid contract.

## 4. Polynomial cost (✔)

| Step | Size / count | Cost |
|---|---|---|
| Generators | k = (3e−1)f < 3n | — |
| HNF entries of M_j | ≤ [ℤᵏ : M_j] ≤ 2^{(N−1)f} ≤ 2^{3n}, so O(n) bits | — |
| Lifted kernel C·L (before HNF) | entries ≤ 2k·max\|C\| | HNF stays polynomial |
| Ring multiplications | O(N·k²·n) = O(n⁴) | each poly(n) bit ops in (ℤ/8)ⁿ |
| Odd powering u^{2^f−1} | f squarings | poly(n) ring ops |
| Normalization | determinant / adjugate on n×n integer matrices with entries of O(nP) bits | poly(n, P), plus O(log V) multiplications for π^m |
| Final step | F₂ echelon form | poly(n) |

There is no enumeration of U₁/U_N and no discrete logarithm. Total cost is poly(n, P, log V) ⊂ poly(n, V, P).

## 5. Controls and falsifiers (finite checks, not part of the proof)

- **Dimension identity (theorem-level check).** U₁ ≅ μ_{2^∞}(E) × ℤ₂ⁿ, so dim F₂^k/R̄ must equal n+1, and the total dimension must be n+2. Any run with rank ≠ n+1 falsifies the implementation.
- **Q₂ control.** Generators are g₁ = 3 and g₂ = 5.
  - Level 1: ψ₁ = (1, 0), so M₂ = ⟨2e₁, e₂⟩.
  - Level 2: 9 ≡ 1 (mod 8) gives digit 0, and 5 gives digit 1, so M₃ = 2ℤ².
  - Result: R = 2ℤ², the classes of 1, 3, 5, 7 are distinguished, and the total dimension is 3. ✔
- **Further cheap checks.**
  - Q₂(i) (e = 2) and Q₄ (f = 2) should both give total dimension 4.
  - φ(R-basis) should equal 1 in O/8O.
  - Applying the map to a² should give 0 for random a.

## 6. Residual obligations

- **[A]** Correctness of the paid order, uniformizer and residue contract, including table precision of at least P + fm bits.
- **[A]** The guarantee m < V.

No gap remains in the full-kernel construction, the precision argument, the unit-square quotient, or the cost bound.
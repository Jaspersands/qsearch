# Audit: exact Bell law for ν and the degree‑D support gap

## Verdict

I found no counterexample. The cheapest attacks fail: interference cancellation, the transpose or U†PU error, an inconsistency with q, a non‑injective transfer map, and degree inflation beyond D+1. Both the Bell law and the gap argument hold as stated.

- **Bell law:** proved below, independent of Pauli phase convention.
- **Gap:** γ_D ≥ 2^{-2D-3} for every n, so γ_3 ≥ 2^{-9}.
  - This uses only the product anti‑concentration lemma applied to μ.
  - I re‑prove that lemma here rather than rely on citation.
  - Proposition S9 itself does not apply to ψ.
- **Sample bound:** O((n³ + log 1/δ)/γ_3) samples suffice for exact recovery of K3. This follows by a standard union bound, with costs charged in §5.

All of this is proved deduction for the exact state. Nothing here addresses extracting p, or the case where the rotation angle or state is only approximate (see §6).

---

## 1. Bell law

**Setup.** Write P_v = X^x Z^z, which is a real matrix. Write Z⊗ⁿ = P_p, with c = cos π/8, s = sin π/8, and U = c·I − i s·P_p.

- The Bell amplitude for two copies is 2^{-n/2}·ψᵀ P_v ψ, which involves the transpose, not ψ†.
- |H⟩ⁿ is real and Uᵀ = U (P_p is diagonal and real). Hence ψᵀ P_v ψ = ⟨Hⁿ| U P_v U |Hⁿ⟩.

**Transpose check (attack 1).** The product is U P U, not U†PU. Using U†PU would swap the roles of ℓ=0 and ℓ=1 and give the wrong support. The contract's assignment is the correct one.

**Case ℓ(v)=1** (P_v anticommutes with P_p):
- P_v U = U† P_v, so U P_v U = P_v.
- The amplitude is a(v) = ⟨Hⁿ|P_v|Hⁿ⟩, giving ν(v) = μ(v).

**Case ℓ(v)=0** (P_v commutes with P_p):
- U P_v U = P_v U² = (P_v − i P_v P_p)/√2.
- In this convention P_v P_p = X^x Z^{z+1} = P_{v+p} exactly, with no phase.
- The amplitude is (a(v) − i·a(v+p))/√2.

**Reality and no interference (attack 2).** a(·) is real, because |H⟩ is real and X^x Z^z is real. So the two terms are in quadrature and no cross term appears:

ν(v) = (μ(v) + μ(v+p))/2.

**Convention independence.** With the Hermitian convention P_v = i^{q(v)} X^x Z^z, one gets P_v P_p = i^{q(v)−q(v+p)} P_{v+p}. Since q(v+p) = q(v) + ℓ(v), the phase is 1 on ℓ=0.

**Local law.**
- The per‑qubit values ⟨H|M|H⟩ are 1, 1/√2, 1/√2 for M = I, X, Z.
- For XZ the value is 0, because XZ is real antisymmetric.
- With the 2^{-1} factor per qubit, this gives I = 1/2, X = Z = 1/4, Y = 0. This is μ.

**q and transpose.** (X^x Z^z)ᵀ = (−1)^{q(v)} X^x Z^z. For real ψ, an antisymmetric P gives ψᵀPψ = 0, so supp ν ⊆ {q=0}. This is consistent with the formula:
- On B, q = 0.
- On B+p, q(b+p) = ℓ(b).

So S = B ∪ ((B+p) ∩ {ℓ=0}) = (B ∪ (B+p)) ∩ {q=0}. S is not p‑periodic: for example, X on qubit 1 and I elsewhere lies in S, but adding p gives a point with q = 1.

**Normalization.** ℓ(v+p) = ℓ(v) + [p,p] = ℓ(v). So v ↦ v+p is an involution on {ℓ=0}, and Σ_{ℓ=0} μ(v+p) = Σ_{ℓ=0} μ(v). Therefore Σν = Σμ = 1.

**Side check.** The E_ij together with q cut S exactly, as claimed:
- If all active x positions have z = 0, the point is in B.
- If all active positions have z = 1, q forces their count k to be even, and the point equals b+p with ℓ(b) = k = 0.

## 2. Product anti‑concentration (self‑contained)

**Lemma.** Let the coordinates y_1,…,y_n be independent. Each y_i takes values in {I, X, Z}, and every value has probability at least η. Let f: B → F2 be nonzero, written in the product basis {1, x_i, z_i}, with at most ℓ qubits carrying a nonconstant factor in any monomial. Then Pr_μ[f ≠ 0] ≥ η^ℓ.

*Proof.*
1. On {I, X, Z}, the functions 1, x, z take the values (1,1,1), (0,1,0), (0,0,1). They are linearly independent over F2, so the product basis is a basis of functions on B.
2. Pick a monomial and a qubit j in it with nonconstant factor e. Expand f = Σ_b b(y_j)·g_b(y_{-j}). The coefficient g_e is nonzero and has degree at most ℓ−1.
3. By induction, Pr[g_e ≠ 0] ≥ η^{ℓ−1}.
4. On that event, f(·, y_{-j}) is a nonzero combination of the independent local basis functions. So f ≠ 0 for at least one value of y_j, which has probability at least η.
5. Independence multiplies the two bounds. ∎

**Applying it to ANF degree.** On B we have x_i z_i = 0. So any ANF monomial containing x_i z_i vanishes, and every other monomial has at most deg(f) nonconstant qubit factors. Restriction to B therefore does not increase degree. Here η = 1/4.

## 3. Gap proof

Let deg f ≤ D and f|_S ≠ 0.

**Case (a): f ≠ 0 somewhere on B.**
- On B, ν ≥ μ/2: equality-or-better holds on ℓ=1, and on ℓ=0 we have ν ≥ μ(v)/2.
- So ν(f≠0) ≥ μ(f≠0)/2 ≥ 4^{-D}/2.

**Case (b): f(v) = 1 for some v ∈ S∖B.**
- Then v = b+p with b ∈ B and ℓ(b) = 0.
- Define g(u) = (1+ℓ(u))·f(u+p). Then deg g ≤ D+1, because shifting by p preserves degree and ℓ is affine. Also g(b) = 1, so g is nonzero on B.
- For each u ∈ B with g(u) = 1:
  - ℓ(u) = 0, so u+p ∈ S;
  - f(u+p) = 1;
  - ν(u+p) = (μ(u+p) + μ(u))/2 ≥ μ(u)/2.
- The map u ↦ u+p is injective (attack 3 fails). Hence ν(f≠0) ≥ μ(g≠0)/2 ≥ 4^{-(D+1)}/2.

**Conclusion.** γ_D ≥ 2^{-2D-3} for every n. The case n < D+1 only enlarges the product bound.

**Hand control (n=4, D=2).** Take f = x_1 z_1, which vanishes on B. Its true mass is (1/8)·Pr[odd number of X among 3 qubits] = (1/8)(7/16) = 7/128, which is at least the bound 1/128. This is a consistency check only. Tightness of 2^{-9} for D=3 is not claimed.

## 4. Clifford invariance

Let M = C̄. Then Cᵀ = M†, and

Cᵀ P_v C = (M† P_v M)(C̄† C).

- Complex conjugation flips only the sign of Y, so C̄ and C induce the same symplectic map. Hence C̄†C is a Pauli up to phase.
- So labels move by an affine map v ↦ Av + w, with unit‑modulus phases that do not affect probabilities.
- Transposing gives q(Av+w) = q(v). The shift p maps to Ap.
- Invertible affine maps preserve ANF degree and mass, so γ_D is Clifford‑invariant.

## 5. Learner cost (charged)

**Unknowns.** m = 1 + 2n + C(2n,2) + C(2n,3) ≈ (4/3)n³.

**Estimator.** K̂ is the set of degree‑≤3 f vanishing on all N samples. Then K̂ ⊇ K3 always.

**Failure probability.** Failure means some class in the quotient by K3 survives. There are at most 2^m such classes, each surviving with probability at most (1−γ_3)^N. So

N = ⌈512·(m ln 2 + ln(1/δ))⌉

suffices. This is explicit but has a large constant, about 475n³.

**Resource costs.**

| Resource | Cost |
|---|---|
| Copies | 2N |
| Each Bell measurement | O(n) gates (n CNOT + n H) and 2n measured bits |
| Classical post‑processing | F2 elimination on an N×m system: O(N m²) ≈ O(n⁹) bit operations, memory O(m²) |

Input access is copies only. There is no state‑preparation oracle and no precision parameter, because the setting is exact.

## 6. Scope of the Haug source text

**What is used.** The excerpt states and proves the degree‑ℓ anti‑concentration property inside the proof of Proposition S9. Only that property, applied to the product law μ of |H⟩ⁿ, is used here. |H⟩ has Bell law (1/2, 1/4, 1/4), and the excerpt gives the same law for |T⟩.

**What is not used.** Proposition S9 itself (γ₂ = η₍₁₎η₍₂₎ for Clifford‑scrambled products) does not apply to ψ. ψ is not a Clifford‑scrambled product, and ν is not a product law. That non‑product structure is exactly why case (b) needs the shift‑and‑multiply step.

## 7. Dependencies and falsifiers

The proof needs four things to hold:

1. |H⟩ is real.
2. The rotation axis Z⊗ⁿ is real, diagonal and symmetric, so the amplitude is U P U.
3. a(v) and a(v+p) combine with a purely imaginary relative phase, so there is no interference.
4. The input is exact copies.

What would falsify it:
- A complex local state, which makes a(v) complex and introduces cross terms.
- A real relative phase between the two terms.
- Any approximate angle or noise.

Under approximate inputs, exact‑vanishing K3 learning has no gap. A robust version would be a separate obligation.

**Remaining open (out of scope).** Whether K3, modulo the universal span of q and q·affine forms, determines Ap, and the sign handling. Nothing above bears on that.
# Audit report: in-span stabilizer frame obstruction

## Verdict

The central falsifier holds. All four claims check out, with three corrections:

1. **The condition-number bound is vacuous for small n.** 1/(Kr) exceeds 1 only for n ≥ 9.
2. **The "for any frame" statement needs one clarification.** It must cover frames that do not span V, or condition numbers taken on the range of F.
3. **The in-span upper bound on extent is loose.** For n = 2 the exact value is ξ_V = 1/r, not the (4+2√2)²/r bound.

No in-span stabilizer state evades the support argument. The outside-span construction refutes only overbroad claims, not your precise in-span statement.

## Cheapest attack first: Claim 2 (the support argument)

This is the load-bearing step, so I attacked it first.

- Every s ∈ V is constant, as a complex value, on E and on each cell C_ij. This is because V is exactly the block-constant functions (verified below).
- Suppose ⟨u,s⟩ ≠ 0. Since s is constant on E, it is nonzero at every point of E.
- So E ⊆ supp(s) = A, where A is an affine subspace.
- E = {0, e₁,…,eₙ} affinely spans F₂ⁿ, so A = F₂ⁿ.
- A flat-modulus stabilizer state on the full cube has |s(x)| = 2^{-n/2}. Constancy on E then gives s|_E = 2^{-n/2}ω with |ω| = 1.
- Hence |⟨u,s⟩|² = (m^{-1/2}·m·2^{-n/2})² = m/2ⁿ = r.

On complex phases: constancy is a property of the complex values, so allowing i^{ℓ·x}(−1)^{q(x)} phases changes nothing. Only the modulus and the support enter the argument.

**Do alternative in-span stabilizers evade it? No.** Every stabilizer state in V either vanishes on E or has full support. Additional full-support states in V do exist.

- Example at n = 2: CZ|++⟩ = (|00⟩+|01⟩+|10⟩−|11⟩)/2 lies in V = span(|++⟩, |11⟩).
- Its overlap with u is ⟨u, CZ++⟩ = √3/2, so |⟨u, CZ++⟩|² = 3/4 = r. It obeys the bound exactly.

**Status:** Claim 2 is proved, for all n ≥ 2.

## Claim 1: structure of V and the Gram matrix

**Cells.** Every x of weight ≥ 2 has a unique pair of first two 1s (i, j). So the cells C_ij partition F₂ⁿ \ E. Each cell C_ij fixes coordinates 1..j and leaves n−j coordinates free, so it is affine of dimension n−j and disjoint from E.

**V is the block-constant space.** Since p = 2^{-n/2}(1_E + Σ 1_{C_ij}), the indicator 1_E lies in V. Therefore V equals the space of functions constant on E and on each cell, of dimension binom(n,2)+1 = K. Independence of the K vectors follows from the smallest Gram eigenvalue below being positive (r > 0).

**The identity for u.** We have 2^{-j/2}c_ij = 2^{-n/2}1_{C_ij}. Hence p − Σ 2^{-j/2}c_ij = 2^{-n/2}1_E = √(m/2ⁿ)·u = √r·u. Verified.

**Gram matrix.** The Gram matrix is [[1, bᵀ],[b, I]] with b_ij = ⟨p, c_ij⟩ = 2^{-j/2}. Then ‖b‖² equals the weight of p off E, namely 1 − r. The eigenvalues are 1 ± √(1−r), plus 1 with multiplicity K−2.

For n = 2 (K = 2), the eigenvalue-1 part is empty. Then b = 1/2 and the eigenvalues are 3/2 and 1/2, so the condition number is 3. Consistent.

**Status:** proved.

## Claim 3: conditioning of in-V frames

Take atoms s_k ∈ V, unit norm, with weights w_k ≥ 0, and F = Σ w_k |s_k⟩⟨s_k|. Then:

- Tr F = Σ w_k.
- By Claim 2, ⟨u,Fu⟩ = Σ w_k |⟨u,s_k⟩|² ≤ r·Tr F.
- λ_max ≥ Tr F / dim(range F) ≥ Tr F / K.
- So κ_V(F) ≥ 1/(Kr), or F is singular on V.

**Correction (a): range-only condition numbers.** A method might report κ only on range(F) when the atoms fail to span V. The bound survives:

- If u ∈ W := range F, the same two inequalities hold with dim W ≤ K.
- If u ∉ range F, the frame cannot synthesize u at all.

Infinitely many atoms add nothing. V contains finitely many stabilizer states up to phase, and phase-equivalent atoms merge their weights. A frame always exists, since {p, c_ij} are themselves stabilizer states in V (each c_ij is uniform on an affine set).

**Correction (b): the quantifier "for all n" overstates the nontrivial range.** κ ≥ 1 always holds, and 1/(Kr) > 1 iff 2ⁿ > (n+1)(binom(n,2)+1). The values of Kr are:

| n | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| Kr | 1.5 | 2 | 2.19 | 2.06 | 1.75 | 1.375 | ≈1.02 | ≈0.72 |

So the bound has content only for n ≥ 9.

Asymptotically, 1/(Kr) = 2ⁿ/((n+1)K) = 2^{Θ(√K)}. That is superpolynomial in K, which is the stated conclusion.

The explicit original frame has κ = (1+√(1−r))/(1−√(1−r)) ≈ 4/r. This is consistent with the bound and shows the obstruction is real for small n too, just not certified by 1/(Kr).

**Optional strengthening (proved under the stated model).** Suppose a method uses operator frames built from rank-one products |s_a⟩⟨s_b| with s_a, s_b ∈ V. Then:

- ⟨⟨uu|F|uu⟩⟩ = Σ w |⟨u,s_a⟩|²|⟨u,s_b⟩|² ≤ r²·Tr F.
- The relevant space has dimension K², so κ ≥ 1/(K²r²).

Hermitian symmetrizations need separate handling. Do not assert this without fixing the model.

**Status:** proved, with corrections (a) and (b).

## Claim 4: restricted versus global extent

**Restricted lower bound.** Write u = Σ c_k s_k with s_k ∈ V. Then 1 = Σ c_k ⟨u,s_k⟩ ≤ √r·Σ|c_k|, so ξ_V(u) ≥ 1/r = 2ⁿ/(n+1). This holds for complex coefficients. Proved.

**Restricted upper bound.** Take the ℓ₁ norm of the Claim 1 identity:

- Σ_{i<j} 2^{-j/2} = Σ_{j≥2} (j−1)2^{-j/2} = x²/(1−x)² with x = 2^{-1/2}, which equals 3+2√2.
- So ξ_V ≤ (4+2√2)²/r ≈ 46.6/r. Proved.

**Correction (c): the upper bound is loose.** At n = 2, u = (|++⟩ + CZ|++⟩)/√3. This gives ξ_V = 4/3 = 1/r exactly. Tightness for general n is not established and is not needed.

**Global upper bounds.** Using the n+1 computational-basis atoms gives χ(u) ≤ n+1 and ξ(u) ≤ (√m)² = n+1. Proved.

**Global fidelity.** E consists of n+1 affinely independent points. An affine set of dimension d therefore contains at most d+1 of them. Hence |⟨u,s⟩|² ≤ (d+1)²/(m·2ᵈ).

- The values of (d+1)²/2ᵈ are 1, 2, 9/4, 2, 25/16, … for d = 0, 1, 2, 3, 4, so the maximum is 9/4 at d = 2.
- This needs m ≥ 3, i.e. n ≥ 2.
- It is attained by the uniform positive state on span{e₁,e₂}, which contains 0, e₁, e₂.
- So F_stab(u) = 9/(4(n+1)) exactly, and ξ(u) ≥ 1/F_stab = 4(n+1)/9.

At n = 2 we get F_stab = 3/4 = r, so global and restricted fidelities coincide there. The separation begins at n = 3. Proved.

**Net separation, all proved:**

- ξ_V(u) = Θ(2ⁿ/n) = 2^{Θ(√K)}.
- ξ(u) ∈ [4(n+1)/9, n+1].

## What exactly is falsified

**Falsified (proved).** Your precise statement is refuted by an explicit, efficiently describable family. The statement:

> For all K stabilizer states with span V and all unit u ∈ V, there is a stabilizer dictionary inside V with a weighted frame of condition poly(K), or ξ_V(u) ≤ poly(K).

The family uses K = binom(n,2)+1 independent inputs (p, c_ij) and target u. The condition-number certificate applies for n ≥ 9; the ξ_V version gives super-polynomial growth asymptotically. This is an existence/geometry obstruction, so no access model, state-preparation cost, or sample budget can rescue an in-span method.

**Not falsified:**

- Global polynomial extent: u has ξ ≤ n+1.
- Methods allowed to leave V, including your existing projection proof.
- Arbitrary measurements.
- Learner existence.

**Representation dependence.** The obstruction attaches to the representation (p, c_ij), not to the state. A different representation of u, on n+1 basis states, has an orthonormal in-span frame. So "polynomial-rank state ⇒ hard for in-span methods" would be wrong. The correct statement is "some rank-K input representation defeats in-span methods". A method that first re-represents u, or augments V by poly(n) outside atoms such as the |eᵢ⟩, evades the result.

**Outside-span construction.** It invalidates only overbroad claims, namely "u is stabilizer-hard" or "conditioning forces exponential cost for every learner". It does not touch your precise in-span claim. It also shows that any proof of polynomial conditioning must leave V.

**Consistency with the quoted published bound.** I cannot verify its source, scope, or whether it concerns ξ or ξ_V. If it is an in-span upper bound of the form 2^{O(√(k log(k+1)))}, this family gives 2^{Ω(√k)} and is consistent with it. The family would then show the √k-type exponent is near-tight up to the log factor. If the bound is global, there is no interaction, since ξ(u) = O(n).

## Proof obligations and falsifiers for whoever invokes this

1. **Pin down the method's atom class.** State "unit stabilizer vectors in V, nonnegative weights, κ on V or on range F". Operator-valued or symmetrized frames need their own analogue of Claim 2.
2. **State the quantifier with its threshold.** The κ certificate applies for n ≥ 9; the ξ_V version applies for all n ≥ 3, with super-polynomial growth asymptotically. Do not claim n = 2 as a counterexample: there ξ_V = ξ = 4/3.
3. **Conditioning to cost.** "Large κ ⇒ large sample/precision cost" holds only within the method's own error analysis. It is not a lower bound on tomography.
4. **What would falsify this report.** Any of the following would:
   - a stabilizer state in V with 0 < |⟨u,s⟩|² ≠ r (impossible by the support argument);
   - a stabilizer state with affine support of dimension d meeting E in more than d+1 points (impossible by affine independence);
   - an error in ‖b‖² = 1−r.
   I found none.

## Novelty

That the in-span stabilizer extent can be exponentially larger than the global extent, with this explicit family, is correct as mathematics. I know of no specific source for it, but I cannot rule out prior or folklore appearance. Treat novelty as unknown.
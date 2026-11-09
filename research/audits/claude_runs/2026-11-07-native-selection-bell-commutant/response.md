# Audit: six-copy anti-identity unitary followed by two Bell measurements

## Verdict

The proposed simplification is **correct** after two small clarifications: a hidden register swap and the exact global phase. The operation produces exactly two ordinary Bell samples of ψ⊗ψ and two copies of ψ hit by a known Pauli. The hypothesis is **falsified for this exact operation, for every input ψ**. This is proved below. It does not rest on failed attacks or finite examples.

## 1. Cheapest decisive check: U_A commutes with the Bell projectors

Write U_A|x⟩ = |Ax⟩, where A acts on the copy index, with A = I₆ + J₆.

**A is an involution.** A² = I + 2J + J² = I + 6J = I (mod 2).

**Action on a pair Bell basis.** |B_{a,c}⟩ on copies (i,j) is the unique joint eigenvector of:
- X^u⊗X^u, with eigenvalue (−1)^{c·u}, for all u;
- Z^v⊗Z^v, with eigenvalue (−1)^{a·v}, for all v.

This is checked directly from 2^{−n/2}Σ_z(−1)^{c·z}|z+a,z⟩. So Π_{a,c} is a polynomial in these Paulis.

**Conjugating those Paulis by U_A.**
- X^u on copies i and j shifts x by u⊗(e_i+e_j). This commutes with U_A iff A(e_i+e_j) = e_i+e_j. That holds because every even-weight vector is fixed by A (Av = v + wt(v)·**1**).
- Z^v⊗Z^v contributes the phase (−1)^{v·(y_i+y_j)}. Since y_i + y_j = x_i + x_j (the sum T cancels), it commutes with U_A. This is the condition A^T(e_i+e_j) = e_i+e_j, and A is symmetric.

**Conclusion.** Π_{(a,c)}^{(2,3)} ⊗ Π_{(b,d)}^{(4,5)} commutes with U_A. This holds for any pairing of the six registers. Therefore:
- Pr(a,c,b,d) = ⟨ψ^{⊗6}|U_A^†ΠU_A|ψ^{⊗6}⟩ = ⟨ψ^{⊗6}|Π|ψ^{⊗6}⟩ = |β_{a,c}|²|β_{b,d}|².
- That is exactly two independent ordinary Bell measurements.
- The post-measurement state is U_A applied to β_{a,c}β_{b,d} ψ⊗B_{ac}⊗B_{bd}⊗ψ, which is a known, ψ-independent unitary acting on a product state.

## 2. Independent direct computation (orientation, phases, normalization)

Start from the projected state ψ₁⊗B_{ac}⊗B_{bd}⊗ψ₆ with x₂=z+a, x₃=z, x₄=w+b, x₅=w.

- **The sum.** S = Σx_i = x₁+x₆+a+b.
- **Retained registers.** y₁ = x₆+a+b and y₆ = x₁+a+b. This is a **swap** plus X^{a+b}: the residual map on the two retained copies is I₂+J₂ = SWAP.
- **Bell registers.** Σ_z(−1)^{c·z}|z+a+S, z+S⟩ = (−1)^{c·S}|B_{ac}⟩.
- **Coefficient of |y₁,y₆⟩.** α_{y₆+a+b} α_{y₁+a+b} (−1)^{(c+d)·(y₁+y₆+a+b)}.

This matches your expression. Since the α's are scalars, the swap is harmless: the coefficient equals (Pψ)⊗(Pψ) with P = Z^{c+d}X^{a+b}, up to the global phase (−1)^{(c+d)·(a+b)}. With the opposite ordering X^{a+b}Z^{c+d}, the per-copy sign (−1)^{u·s} appears twice and cancels, so the global phase is the same.

**Bell amplitude.** β_{a,c} = 2^{−n/2}Σ_z(−1)^{c·z}α_{z+a}α_z = 2^{−n/2}⟨ψ̄|X^aZ^c|ψ⟩.
- It is bilinear in ψ, with no conjugates. That is correct for ψ⊗ψ because the Bell bra has real coefficients.
- Complex α causes no issue anywhere. No real or uniform-amplitude premise is used.

**Normalization.** Σ_{a,c}|β_{a,c}|² = 1 by completeness of the Bell basis. The branch norms then sum to (Σ|β|²)² = 1. This is consistent with U_A being unitary, so no terms are missing.

## 3. Clifford covariance

I proved this directly on generators rather than relying on the "rows have weight 5" argument, which alone is insufficient.

| Generator | Reason it commutes with U_A |
|---|---|
| Paulis X^s | Uses A**1** = **1** |
| Paulis Z^u | Uses Σ_i(Ax)_i = Σ_i x_i |
| CNOT / linear maps within a copy | Act on the other tensor index |
| Phase gate S on qubit j | The column-bit vector v ∈ F₂⁶ maps to Av = v (even weight) or to its complement (odd weight). Weights 1↔5 and 3↔3 agree mod 4. |
| H | Needs (Au)·(Av) = u·v, i.e. A^TA = I, which holds |
| CZ | Phase (−1)^{v_i·v_j} is preserved by orthogonality |

So U_A commutes with C^{⊗6} for all n-qubit Cliffords C (global phases cancel).

**Consequence for ψ = Cφ.** The identity is state-independent, so it applies unchanged. The retained copies are PCφ = C(C^†PC)φ, with P known.

**Inherited caveat about the old primitive.** β depends on C^TC: ⟨φ̄|C^T W C|φ⟩ = ⟨φ̄|(C^TC)(C^†WC)|φ⟩, and C^TC is generally not a Pauli. This is inherited unchanged from ordinary Bell sampling, neither improved nor worsened.

## 4. Information conclusion (proved)

The instrument {Π_k U_A} equals {W_k Π_k}. Here W_k is a known, outcome-dependent unitary consisting of a swap, P⊗P, and phases.

By data processing, any downstream protocol using it is exactly simulated by ordinary Bell measurements followed by a known unitary. So it yields:
- zero additional statistical information;
- no derivative state;
- no new stabilizer data.

The same argument covers measuring 1, 2 or 3 Bell pairs in any pairing. With only one pair measured, the four retained copies undergo I₄+J₄. That map is not Clifford-commuting (row weight 3) but is still known and ψ-independent, so it is invertible at no information cost.

## 5. Optional question: classification (proved)

**Claim.** Let A ∈ GL₆(F₂) with A^TA = I and wt(Av) ≡ wt(v) mod 4 for all v. Then A = P or A = (I+J)P = J+P for some permutation P. These form the group S₆×⟨I+J⟩, of order 1440.

**Weight criterion.** Weight preservation mod 4 is equivalent, given orthogonality, to every column having weight ≡ 1 mod 4. This follows from wt(u+v) = wt u + wt v − 2|u∧v| together with the fact that |Au∧Av| ≡ u·v mod 2. In F₂⁶, column weights are therefore 1 or 5, and columns must be distinct with pairwise even overlap.

**Overlaps between candidate columns.**
- Two weight-1 columns: overlap 0 iff they are distinct. Allowed.
- Two weight-5 columns **1**+e_p and **1**+e_q with p≠q: overlap 4, even. Allowed.
- A weight-1 column e_i and a weight-5 column **1**+e_k: overlap 1 (odd, forbidden) unless i = k.

**A mix is impossible.**
- If there are ≥ 2 weight-5 columns with distinct p and q, any weight-1 column would need i = p and i = q. Contradiction.
- If there is exactly one weight-5 column, all five weight-1 columns must equal e_k, contradicting distinctness.

**The two pure cases.**
- All columns weight 1: A is a permutation.
- All columns weight 5: column j is **1**+e_{π(j)}, so A = J+P_π = (I+J)P_π. This is orthogonal: J^TJ = 0, JP = PJ = J, so the product is I.

Because P permutes identical copies and commutes with I+J, every member of this group, combined with any choice of two Bell pairs, reduces to §1–4.

**Exact boundary.** This excludes only the following pattern: a copy-linear unitary r(A)^{⊗n} with A orthogonal and Z₄-weight-preserving on exactly six copies, followed by pairwise Bell measurements with copy-uniform Pauli structure.

It does **not** exclude:
- Non-invertible Clifford-commutant elements. For example, N = ⟨111100⟩ is self-orthogonal, doubly even, and has **1** ∈ N^⊥. I believe codes like this give projector-type commutant operators, but I did not derive that here; treat it as an unchecked pointer.
- Linear combinations of commutant elements.
- t ≠ 6 copies.
- Non-copy-linear maps, or maps that are not Clifford-commuting.
- Adaptive or general coherent measurements, ancillas, or non-Bell POVMs.

Nothing here implies hidden-frame hardness, removal of the factor-search blocker, or any speedup or slowdown.

## 6. Proof obligations and falsifiers for follow-ups

- **Finite control (not a proof).** Brute-force n = 1, 2 with random complex ψ. Check that Pr(a,c,b,d) equals the product |β_{a,c}|²|β_{b,d}|² and that the corrected post-state equals ψ⊗ψ up to the phase (−1)^{(c+d)·(a+b)}. Any mismatch would falsify §2.
- **Screen for any new map M.** First test whether the measured observables are U_M-invariant, as in §1. If they are and the residual map is ψ-independent, M yields nothing new, and you can stop there.
- **Burden for a positive claim.** A positive claim needs a map whose post-measurement residual depends on ψ, or whose outcome statistics differ from products of ordinary Bell samples. It must also come with a full cost accounting: copies, gates, precision, and classical post-processing.
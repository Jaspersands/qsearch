# Audit of Proposition `prop:general-count`

## Blocker

**No blocker in the algebraic-operation statement.** I found no counterexample. The proposition follows from the excerpt's own lemmas under two interpretive hypotheses, H1 and H2 below.

The proposition does **not** give a bit-time bound, and it says so. The final paragraph of its proof defers bit cost to Section `subsec:one-query-cost`. That section is not in the excerpt, so its contents are unknown.

All conclusions below assume the design in Definition `def:layout` is supplied and valid, as the task specifies.

## Interpretive hypotheses

- **H1.** In (`eq:general-product-degree`), deg means **total degree** in the Y_{f,v}.
  - If it meant maximum degree per variable, deg_T H ≤ dR would fail.
  - Counterexample under that reading: Φ = Y₁Y₂ has per-variable degree 1 but T-degree 2R.
- **H2.** ker C_h means the **rational** kernel. This matches item 4 of the definition (ξ ∈ ℚ^{S}) and the lemma's domain ℚⁿ.

## Exact derivation, with the four checks

**1. Degree and value at zero.** Substitution Y_{f,v} ↦ ⟨P_{f,v}(T), x⟩ is a ring homomorphism, so it commutes with the product over A, even if A has nilpotents.
- Each image has T-degree ≤ R, so under H1, deg_T H ≤ dR = d_H.
- P_{f,v}(0) = δ_v gives H(0) = Z.
- QJ = Q(⌊d_H/Q⌋ + 1) > d_H, so the Hermite map ℚ^{QJ} → ℚ^{QJ} at the distinct nodes 1..Q is invertible.
- Its rational inverse acts coordinatewise on A^{QJ}, because A is a ℚ-algebra. So Z = H(0) is recovered.

**2. Check (1): p_x depends on x in Lemma `lem:boolean-differences`. The lemma is valid.**
- For each x separately, multilinearize p_x. Multilinear representations of functions {0,1}ⁿ → A are unique over any commutative ring, because Möbius inversion has integer coefficients.
- Hence c_{x,E} = Σ_{U⊆E} (−1)^{|E|−|U|} p_x(1_U), and c_{x,E} = 0 for |E| > q.
- Then Σ_x p_x(x) = Σ_x Σ_{|E|≤q} c_{x,E}·[x_E = 1].
- Swapping these finite sums gives the identity. The x-dependence stays inside the inner sum over x, so nothing is lost.

**3. Applying the lemma to the Taylor coefficients.**
- Every X-occurrence in (`eq:jet-substitution`) carries a factor of z, because ΔP(z) ∈ zℚ[z]^{1×n}. So deg_X [z^j] G_x ≤ j ≤ J − 1 = q, uniformly for all j < J.
- G_x(x, z) equals the product of Φ_f(⟨P(t+z), x⟩), so Σ_x G_x(x, z) = H(t+z).
- Therefore (`eq:full-taylor-sum`) holds exactly mod z^J.

**4. Check (3): corrections are independent of x once X = 1_U. This holds.**
- The input to factor f is ⟨P_{f,v}(t), x⟩ + ⟨ΔP_{f,v}(z), 1_U⟩.
- The second term is a constant in ℚ[z]/(z^J), even though U may span several groups.
- The x-dependence is confined to ⟨P_{f,v}(t), x⟩ at an integer t ∈ [Q]. Item 4 of the definition kills ker C_{t,h} for every h ≠ σ_f(t).
- So A_{g,U} : ℚⁿ → R = A[z]/(z^J) satisfies the invariance hypothesis for all rational x. R is commutative with identity.
- Caution: an implementation that uses ⟨ΔP(z), x⟩ instead would give the same total sum but **violate** this invariance.

**5. Check (2): fixed bits and arbitrary representatives in Lemma `lem:measurement-separation`. The lemma is valid.**
- Invariance holds on all of ℚⁿ. So each successive replacement x_h → x̄_h (difference in ker C_h) is legal, whatever bits x̄_h has.
- E is imposed only on the summation variable x_g in Σ_g.
- Each case is handled correctly:
  - If X_g(y_g) = ∅, the tuple is skipped.
  - If X_g(y_g) ≠ ∅ but X_{g,E}(y_g) = ∅, then Σ_g = 0.
- Every Boolean x has a unique measurement tuple, and row ℓ₁-norms ≤ D place it in [−D, D]^c. So the decomposition is a partition.
- Choosing E-respecting representatives would also be correct, though unnecessary.

**6. Count of examined vectors.**
- c ≤ 2τn and |S_{t,g}| ≤ 2n/r give Σ_g 2^{|S_g|} ≤ r·2^{2n/r}.
- Two scans per tuple give 2r(2D+1)^{2τn}·2^{2n/r} per pair (E, U).
- Multiplying by C_q pairs and Q points gives the stated bound exactly.

## Check (4): hidden costs

- **Enumeration.** None is hidden in the vector count. The representative scans are counted, and pairs (E, U) are enumerated by index.
- **Per-vector work.**
  - Measurement checks: poly(n, c, log D) bits.
  - Inputs: inner products with precomputed P_{f,v}(t) and ⟨ΔP, 1_U⟩.
  - Group product: ≤ |F| factor calls plus O(|F|J²) operations in A.
  - Factor-evaluation cost is excluded, as the proposition explicitly states.
- **Interpolation.** O((QJ)^{O(1)}) operations, and QJ ≤ d_H + Q.
- **Algebra-element size is the real gap.**
  - "Polynomially many algebra elements" bounds the *count* of stored elements, not their size.
  - For general A, bit size is unknown and is not claimed.
  - So the storage and operation claims hold only in the algebraic model.

## Hypotheses still needed for a bit-time algorithm

The excerpt does not establish these; they are unknown here.

1. **A concrete representation of A.**
   - For A = ℚ: all Φ_f coefficients have poly(n) bits, and the total factor degree Σ_f deg Φ_f is poly(n).
   - Over a domain this equals the degree of the product, so d ≤ poly.
   - For other A: an explicit size bound on elements and the cost of the ring operations.
2. **Factor evaluators.** Each evaluates Φ_f at inputs in ℚ[z]/(z^J) with poly-bit coefficients, in poly time and space.
3. **A size bound for every accumulator** (s, p, Σ_g, Z_E, and the coefficients of 𝓗_t). For A = ℚ:
   - Denominators divide d_den^{Σdeg} times the coefficient denominators, where d_den = (R−1)!Q! (item 5).
   - Additional factors come from the Taylor shift and the Hermite inverse.
   - Numerators gain only O(n + log C_q + log Q) bits from summation.
   - This gives poly bits **if** Q, R, J, d, and log D are poly(n).
4. **Polynomial parameters.** Q, R, J, r, |F|, total scope length, and log D must be poly(n), and the design must be given with poly-bit entries (item 5 plus the C matrices).
5. **Exact Hermite inverse.** Its entries must have poly(QJ·log Q) bits.

## Small exact test

**Design.** n = 2, a single factor Φ(y) = y² with I = {1}, so Z = 2.
- Parameters: d = 2, R = 1, Q = 2, so d_H = 2, q = 1, J = 2.
- Replacement row: P(T) = (1 − T, T). Then d_den = 2 and 2P is integral.
- Partitions: S_{t,1} = {1}, S_{t,2} = {2}, with σ(t) = 1.
- Measurements: C_{t,g} = [1], so D = 1 and τ = 1/2.
- This satisfies every item of `def:layout`.

**Expected values.** H(T) = 2 − 2T + 2T².

| t | E = ∅ | E = {1} | E = {2} | Total |
|---|---|---|---|---|
| 1 | 2 | −2z | +4z | 2 + 2z |
| 2 | 6 | 0 | +6z | 6 + 6z |

Hermite interpolation on (1; 2, 2) and (2; 6, 6) gives H(0) = **2**.

**Errors this test catches.**

| Implementation error | Result |
|---|---|
| Off-by-one J = q (values only) | Line through (1, 2), (2, 6) gives H(0) = −2 |
| Dropping the x_E = 1 restriction | t = 1 coefficient becomes 2 instead of 2 + 2z |
| Sign flip (−1)^{\|U\|} | t = 1 coefficient becomes 2 − 2z |

**Limitation.** This test uses identity measurements, so it does not exercise the kernel or representative logic. A second test with a nontrivial ker C, for example a group {1, 2} with C = (1 1), would be needed to catch the plausible error of using ⟨ΔP(z), x⟩ instead of ⟨ΔP(z), 1_U⟩.

Passing either test does not establish the proposition. The derivation above is what supports it.
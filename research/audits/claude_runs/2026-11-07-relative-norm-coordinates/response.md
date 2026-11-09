# Audit of the compact endpoint (conditional on (1) and a complete compact S-unit primitive)

## Verdict

- **No hidden exponential bit cost found.** Each step after the S-unit call has a polynomial bit-cost bound, provided the obligations O1–O8 below are discharged in the write-up.
- **Torsion handling is correct.** It needs only minor tightening.
- **The relative basis is not circular.**
- **The ideal-norm image is not used.** The endpoint is purely element-level. One completeness condition on S must be stated explicitly; it is inherited from (1).
- **The endpoint contains no quantum content.** It is entirely classical and deterministic. The only quantum dependencies are upstream: S-unit completeness and integer factoring for the support set. The endpoint therefore adds nothing to any separation claim.

## Step-by-step audit

**Step 0: Embedding contract.** The Q-linear map φ: K→L is a promise. Make it a check rather than an assumption:
- φ(1) = 1;
- φ(ε_a ε_b) = φ(ε_a)φ(ε_b) for all basis pairs (m² products in L);
- m divides N.

This costs polynomial time. Without it, every relative determinant is meaningless.

**Step 1: Full torsion µ(L).** The bound w ≤ 2N² is correct, because φ(n) ≥ √(n/2) for all n and φ(w) ≤ N.

Tightenings:
- Only t with φ(t) | N can succeed. Restricting to these keeps dim_Q L[T]/Φ_t ≤ N². The unrestricted bound is about 2N³; that is still polynomial, but the restriction is cheaper.
- Coefficients of Φ_t satisfy |c_k| ≤ C(φ(t), k) ≤ 2^{φ(t)}, so each is at most N bits.

Applying LS Theorem 1.10 to E = L[T]/Φ_t gives Spec(E) and each quotient E/m:
- A factor with dim_Q(E/m) = N receives the composite L → E → E/m. This map is an injective field map of equal dimension, so it is an isomorphism. Its inverse comes from rational linear algebra.
- ζ_t is the image of T pulled back to L.
- Check Φ_t(ζ_t) = 0 directly.

The maximum successful t is exactly w, since t succeeds if and only if t | w. One gap: the packet's "maximum successful order" step needs the sentence "t succeeds iff t | w" to be proved, not just asserted.

The excerpt also mentions LS's separate µ(E) result [14]. It is not needed, because the Theorem 1.10 route is self-contained.

**Step 2: K-basis of L and relative norms.**

*Greedy construction.* The K-span of the chosen vectors is the Q-span of {φ(ε_k)v_i}. Q-rank tests are rational Gaussian elimination. The process terminates with exactly d vectors, because the supplied Q-basis of L spans L. It needs no relative integral basis or pseudo-basis, so there is no circularity and no reliance on O_L being O_K-free.

*Matrix of β.* Expand β·v_i in the Q-basis {φ(ε_k)v_j}. The coefficients c_{ijk} give c_ij = Σ_k c_{ijk} ε_k ∈ K. This is correct because L is commutative and K acts through φ.

*Determinant over K.* This is where a bit bound is required (obligation O3). Use fraction-free (Bareiss) elimination over K, or ordinary elimination where every intermediate is a ratio of minors. Every intermediate is then a minor of the d×d matrix.

- Bound for a minor: at most d! terms, each a product of at most d K-elements.
- Each K-multiplication multiplies the coordinate bound by at most m·max|structure constant|.
- With a maximal-order integral basis, structure constants are integers of input size. Denominators come only from β and the basis-change inverse, and those are polynomial by Cramer/Hadamard bounds.
- Exact division in K is a size-m rational linear solve.

Every γ_l = N_{L/K}(β_l) therefore has polynomial bit size. The packet asserts this but does not prove it; the proof needs the ratio-of-minors argument above.

**Step 3: LS relation lattice.**

- K is a Q-algebra given by structure constants, so Theorem 1.11(i) applies as stated. It decides whether every γ_l is nonzero and returns generators of the kernel of Z^{J+1} → K*.
- Λ is the full kernel, including torsion relations such as 2·e for γ = −1. Do not saturate Λ. The packet is right about this.
- **Citation hygiene.** "Proposition 8.2" is listed in the source metadata, but its text does not appear in the excerpt. Rely on Theorem 1.11(i) as quoted. It suffices because K is a Q-algebra; the field case needs no separate claim.
- **Repeated labels.** Theorem 1.11 speaks of a "finite system S". Do not depend on how "system" handles repeats. Deduplicate by exact equality (a coordinate comparison), compute Λ for the distinct elements, then add e_l − e_k for each identified pair. This is a cheap, rigorous fix.
- **Generator count.** The kernel generators number polynomially many, because the output size is polynomial. Then compute an HNF basis R.

**Step 4: Integer system.**

- Let P be the J×n exponent matrix: its columns are the p_j, including the torsion column. Solve [P;0]z − Rh = e_{J+1}.
- This is a linear Diophantine system with polynomial-bit entries. Polynomial-time HNF or SNF decides it and returns a particular solution of polynomial bit size.
- The torsion coefficient can be reduced mod w.
- Correctness uses only multiplicativity: ∏γ_l^{(Pz)_l} = N(∏β_l^{(Pz)_l}).

**Step 5: Flatten and verify.**

- The exponents (Pz)_l have bit size at most bits(z) + bits(P) + log n. x is never expanded.
- Verification recomputes each γ_l and tests whether ((Pz), −1) ∈ Λ, or applies Theorem 1.11(ii).

**Scale check.** |S| ≈ π(B0) with B0 polynomial. The L-prime count is at most N·|S|, so the unit rank, J, and the HNF dimensions are all polynomial. They are large-degree polynomials, but not exponential.

## Requested failure categories

1. **Hidden exponential bit cost.** None found, subject to O3 (determinant bit bound) and O6 (the HNF solution size is taken from the standard result, not re-derived here). The only potentially large values are the exponents. They stay binary throughout and are never evaluated.

2. **Wrong torsion assumption.** The packet correctly includes the full µ(L) rather than just ±1. Remaining requirements:
   - The S-unit output must be lifts of a basis of O_{L,S}^*/µ(L), not a basis of a finite-index sublattice of the log-image.
   - The torsion generator must be primitive of order exactly w.

   µ(K) is not needed. Theorem 1.11(i) already captures every torsion relation among the γ's and a inside K*.

3. **Incomplete ideal-norm image.** The endpoint never uses ideal norms. It decides membership a ∈ ⟨N(ζ), N(u_j)⟩ = N(O_{L,S}^*), and (1) identifies this with N(L*) ∩ O_{K,S}^*. Two silent requirements must be stated:
   - S_L must consist of all L-primes above every rational prime in S. Omitting even one makes N(O_{L,S'}^*) a proper subgroup and invalidates the NO answer.
   - a ∈ O_{K,S}^* must hold. Upstream, this follows from including the primes dividing c and |N_{K/Q}(ca)|.

4. **Circular relative basis.** None. A K-vector-space basis suffices for N_{L/K}, and it is built from supplied data alone.

## Proof obligations

| # | Obligation |
|---|---|
| O1 | Verify the embedding is a ring homomorphism with m \| N (polynomial check, see Step 0). |
| O2 | Prove that t succeeds iff t \| w, and that dim_Q(E/m) = N identifies the L-rational factors. |
| O3 | Give an explicit polynomial bit bound for N_{L/K}(β) via the ratio-of-minors argument over K. |
| O4 | Replace the "repeated labels" reliance with deduplication plus equality relations. |
| O5 | Cite only Theorem 1.11(i)/(ii) as quoted. Do not cite the Proposition 8.2 text unless it is excerpted. |
| O6 | Give an explicit HNF/SNF solvability statement with a polynomial bound on the particular solution. |
| O7 | State that S_L is the full set of L-primes above S, and that the source's completeness means a basis of O_{L,S}^*/µ(L). |
| O8 | State the asymmetry. YES answers are certified unconditionally and classically. NO answers depend on GRH, (1), and an S-unit completeness event that the endpoint cannot verify. The probability η therefore governs undetected wrong NO answers only. |

## Falsifiers for this endpoint

Any one of the following would block the endpoint:

- a nonzero atom whose computed relative norm disagrees with an independent computation (for example, the product of conjugates in a small control);
- an L with µ(L) ≠ ⟨ζ⟩ under the enumeration;
- a solvable instance answered NO even though the S-unit basis passes an independent index check;
- a case where Λ from Theorem 1.11(i) differs from relations found by direct evaluation;
- any intermediate whose coordinate size grows super-polynomially in d.

A finite control, such as the planned PARI rnfisnorm comparison, can only falsify. It cannot confirm the endpoint.

## Strongest classical counterpart

**Already wholly classical and deterministic:** every step after the S-unit call. This covers torsion, relative norms, Theorem 1.11 relation lattices, integer linear algebra, flattening, and verification.

**Quantum dependencies are upstream only:**
- factoring D_L, c, and N_{K/Q}(ca) for the support set (outside this audit);
- the complete compact S-unit basis of L.

Prime decomposition is randomized classical finite-field factoring, also outside this audit.

**The matched classical baseline** keeps the same support reduction and this identical endpoint, and substitutes a classical GRH-conditional S-unit computation. Its cost is whatever that classical S-unit method costs at growing degree. I make no claim about that cost here.

**Consequences for any claimed advantage:**
- Any advantage lies entirely in the S-unit primitive and in factoring.
- The endpoint is plausibly the standard S-unit-to-norm-image step used by prior relative norm solvers. Simon 2002, Fieker–Jurk–Pohst 1997 and PARI rnfisnorm are named in the packet, but their content is not supplied, so overlap and priority remain unsettled.
- Nothing here supports a separation or hardness claim.
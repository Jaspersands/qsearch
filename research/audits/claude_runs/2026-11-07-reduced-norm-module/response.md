# Review: reconstructing x with Nrd(x) = a from a compact splitting, and the certificate interface

## 0. Verdict

- **The algebra is correct.** Given a correct F-linear homomorphism ρ: A⊗F → M_n(F), x = B_w⁻¹(θw) satisfies Prd_x = P_θ, so Nrd(x) = N_{F/K}(θ) = a. This holds for nondivision A, under either orientation, and needs no minimal ideal of A. It is the constructive form of "a degree-n splitting field embeds in A."
- **The certificate interface does not avoid general circuit identity testing.** It certifies two kinds of facts exactly:
  - nonzero facts, by a modular witness;
  - purely multiplicative equalities, by exponent-lattice/LS-type verification.
- **The hidden unverified step is that ρ is a homomorphism on the given presentation of A** (source map M4 below). This is an additive identity among circuits whose values have log-height up to 2^poly. An exact certificate for c = δ(α) in F^{⊗3} does not imply it.
- **The step can be removed from soundness, but not made deterministic.** A verifier that never trusts ρ or α (Section 4) reduces everything to one equality instance of EquSLP type. That instance is checkable with one-sided randomized error. To my knowledge it is not checkable by a deterministic polynomial certificate unless arithmetic-circuit identity testing (ACIT) is derandomized; I recall a published polynomial-time equivalence between EquSLP and ACIT but cannot verify the citation here.
- I make no novelty or speedup claim.

## 1. Algebra check (proved, conditional on H_ρ)

**Hypothesis H_ρ.** ρ|_{A⊗1}: A → M_n(F) is a unital K-algebra homomorphism (or anti-homomorphism), extended F-linearly. A is simple, so ρ is injective, and by dimension the F-linear extension is an isomorphism.

**(a) V = Fⁿ is the regular module.**
- dim_K V = n². Write A = M_m(D) with deg D = d and n = md.
- The simple A-module S has dim_K S = nd.
- By semisimplicity, V ≅ S^{n/d} = S^m ≅ _A A.
- Hence cyclic vectors exist, and φ_w: b ↦ ρ(b)w is an A-module isomorphism exactly when det B_w ≠ 0.

**(b) Sampling w.**
- Fix the power K-basis of F = K[t]/(f). Then B_w is n²×n² over K, each column is K-linear in the n² K-coordinates of w, and det B_w is homogeneous of degree n².
- It is not identically zero, by (a).
- Schwartz–Zippel on an integer grid of size S = 4n² gives P[det B_w = 0] ≤ 1/4.

**(c) Orientation.** θ acts by F-scalars and ρ is F-linear, so θ commutes with ρ(A). Define x by θw = ρ(x)w. Then

  φ(bx) = ρ(b)ρ(x)w = ρ(b)θw = θρ(b)w.

So multiplication by θ on V is conjugate, via φ, to right multiplication R_x on A.
- If ρ is an anti-homomorphism, the same computation gives L_x instead.
- Both L_x and R_x have characteristic polynomial Prd_xⁿ, and Nrd_{A^op} = Nrd_A, so orientation does not matter.

**(d) Norm.**
- The characteristic polynomial of θ on V ≅ Fⁿ over K is P_θⁿ.
- So Prd_xⁿ = P_θⁿ. These are monic polynomials over a field, so by unique factorization Prd_x = P_θ, and Nrd(x) = N(θ) = a.
- Bonus: f ↦ x_f is a homomorphism F → A, since x_{fg} = x_g x_f and F is commutative. So if θ is primitive, K[x] ≅ F is a maximal subfield.

**(e) Nondivision A.** Nothing above used division. Requiring a ≠ 0 excludes the trivial case θ = 0.

What this avoids is a global minimal ideal of A. It does not avoid splitting work: ρ is equivalent to a minimal left ideal of A⊗F, namely ρ⁻¹(M_n(F)e₁₁). That work sits in the primitive.

## 2. Required source maps (each needs a stated type and a correctness proof)

| Map | Content | Kind of identity |
|---|---|---|
| M0 | Input encodings: K = Q[ω]; A by basis b_i and structure constants γ_ijk ∈ K; F = K[t]/(f); θ; a | Exact data |
| M1 | Coface maps d⁰, d¹, d²: F^{⊗2} → F^{⊗3} applied to the atoms ("mapped atoms") | Syntactic |
| M2 | Map from α-atoms to ρ entries, e.g. codiagonal F⊗F → F, or a projection to one factor of F⊗F ≅ F × E | Must be specified |
| M3 | Coordinate map Fⁿ → K^{n²} | Exact, linear |
| **M4** | **ρ(b_i)ρ(b_j) = Σ_k γ_ijk ρ(b_k) and ρ(1) = I, for the input γ** | **Additive identity among exponential-height circuits** |
| M5 | Reduction maps from Z_(N)-orders to Z/N | Ring homomorphism if every inverted node is a unit mod N |

**Type problem to resolve.** Suppose α is a scalar 1-cochain in (F⊗F)^× and c is the Amitsur 2-cocycle of [A]. Then c = δ(α) says [A] = 0, i.e. A is split, so the certificate cannot exist for nonsplit A. Coherent readings are:
- the matrix cochain g ∈ GL_n(F⊗F), with scalar defect δg = c, so that A ≅ {m : g(m⊗1)g⁻¹ = 1⊗m}; or
- a cocycle of some other presentation.

In either reading, the identification of that descended algebra with the input (b_i, γ) is M4.

## 3. What is certifiable, and where the gap is

### Nonzero facts: certifiable deterministically
A witness modulus N with (det B_w mod N) a unit proves det B_w ≠ 0. The verifier recomputes this in polynomial time. Requirements and cost:
- Primality of N is not needed: any ring homomorphism Z_(N) → Z/N works.
- O_K is not needed. Computing a maximal order needs the squarefree factorization of the discriminant, which is not known to be polynomial time. Use Z[ω][t]/(f) localized at N.
- Every inverted atom must be a unit mod N; the verifier checks this by computing the inverses.
- Binary exponents are evaluated by repeated squaring, costing O(e) multiplications.
- If det ≠ 0 has log-height ≤ H, a random b-bit prime divides its norm with probability ≲ (H·d·n²/b)/π(2^b). Taking b = log₂H + O(log(dn)) + λ makes witnesses easy to find.

### Multiplicative equalities: certifiable exactly
An equality ∏β_j^{e_j} = ∏β_j^{e'_j} with binary exponents can be tested in deterministic polynomial time in a number field. I recall Ge (FOCS 1993) for this but cannot confirm the citation here.

Costs to charge:
- splitting the étale algebra F^{⊗3} into number-field components, by polynomial factoring over number fields, in degree up to n³·[K:Q];
- the relation-lattice computation.

So "c = δ(α) exactly" is legitimate, given those costs.

### Additive equalities: not certifiable deterministically
The following are all EquSLP/ACIT-type statements about circuits containing + and exponentiation:
- M4, the homomorphism property of ρ;
- any check that Nrd(x) = a, because x is a Cramer quotient and so additive;
- N(θ) = a, if θ is a compact element containing additions.

Exact evaluation needs about 2^poly bits, or a CRT over about 2^poly/poly primes. Either is an exponential clock.

### c = δ(α) does not imply M4 (falsifier)
Keep α, c and the LS certificate unchanged, and replace ρ by ρ' = ρ∘τ, where τ is K-linear, fixes 1, but is not multiplicative (for example, add a generic matrix to ρ(b_k) for one k).
- The cochain certificate still passes.
- x' = B'_w⁻¹(θw) is a well-defined element of A.
- Generically Nrd(x') ≠ a.

The certificate is sound only with a theorem that ρ is a fixed syntactic function of α (and of γ). That theorem would have to show that the M4 identities lie in the ideal generated by the multiplicative relations. For arbitrary input γ, the change of basis to a cochain-adapted basis is additive data, so the theorem has to cover it as well.

### A second hidden location: inside the primitive
Any primitive step that concludes a value is zero needs a vanishing claim, and vanishing has no modular witness. Examples:
- a rank deficiency;
- a kernel vector;
- "all (r+1)-minors vanish."

Only full-rank operations with witnessed nonzero pivots are certificate-safe. Proof obligation: audit the ρ-primitive and confirm every branch decision is a nonzero decision.

## 4. Concrete repair: a ρ-free verifier

The output check should not depend on ρ, α, c, or the LS data. Those serve only the prover.

**Prover.**
1. Run the primitive to get ρ.
2. Sample w on the grid until a modulus witness shows det B_w is a unit mod N. Expected ≤ 4/3 draws; failure (1/4)^t after t draws.
3. Output:
   - x as a polynomial-size K-coordinate circuit, using Cramer's rule or Gaussian elimination mod the evaluation modulus;
   - w;
   - N;
   - the data needed to evaluate x.

**Verifier, given only M0 inputs and x.**
1. **Norm of θ.** Check N_{F/K}(θ) = a. This is exact if θ and a are explicit. If they are multiplicative products, use the exact multiplicative test above. If they contain additions, this check is randomized as well.
2. **x is defined.** Check that det B_w is a unit mod N.
3. **One identity.** Choose one form:
   - **3a (primitive θ).** First certify disc(P_θ) ≠ 0 with a modular witness; this is a nonzero fact and certifies that θ is primitive. Then check P_θ(x) = 0 in A, computed with γ. Since P_θ is irreducible of degree n and the irreducible factors of Prd_x are those of the minimal polynomial of x, this gives Prd_x = P_θ and so Nrd(x) = a.
   - **3b (general θ).** Check char(L_x) = P_θⁿ coefficientwise. Then Prd_xⁿ = P_θⁿ, so Prd_x = P_θ. This also covers non-primitive θ.
   
   Batch the n² coordinate identities (3a) or n² coefficients (3b) with random small K-coefficients. Evaluate modulo s independent random b-bit primes q, resampling any q at which det B_w or an atom is not a unit.

**Guarantees.**
- **Completeness.** If H_ρ holds, the identity holds exactly, so the verifier always accepts.
- **Soundness.** A false identity is accepted with probability ≤ 2^{-s} for suitable b. This holds whatever ρ was used, including a wrong one.
- **What remains.** Exactly one EquSLP instance, of size poly(n, s_ρ, e, [K:Q]). The verifier is randomized with one-sided error, not an NP-style certificate.

**Deterministic alternatives, all charged:**
1. If the primitive is a proven-correct deterministic algorithm whose branches are all nonzero-witnessed, then Nrd(x) = a is a theorem and verification means recomputing ρ plus the det witness.
2. Exact exponential-size evaluation.
3. Derandomizing ACIT.

## 5. Finite clocks

Parameters: d = [K:Q], n, ρ circuit size s_ρ, m atoms, exponent bit-length e, atom height h, and

  log-height H ≤ 2^{O(s_ρ + e)}·h·poly(n), including the Cramer factor N = n².

| Clock | Cost |
|---|---|
| Reading input | n⁶ structure constants; the ρ circuit, shared across n⁴ entries; m atoms of size e + h |
| w-sampling | ≤ t draws; failure (1/4)^t |
| Modular evaluation | O(n⁴·s_ρ·e) ring operations to evaluate ρ(b_i)w; O(n⁶) for elimination on n²×n²; each operation Õ(d·n·b) bit cost |
| Bad-modulus resampling | Number of bad primes ≤ (log-norms of atoms + H)/b |
| Modulus bit-length | b = log₂H + O(log dn) + λ; prime sampling with randomized or AKS primality testing, needed only for the soundness count |
| Multiplicative test, if used | Polynomial in (m, e, h, d·n³), plus the étale decomposition |
| Soundness repetitions | s |
| Output size | x is a circuit. Its standard-form coordinates may have about 2^poly bits; this is not shown either way. Every downstream consumer inherits the EquSLP issue. |

## 6. Open proof obligations and falsifiers

1. **Fix the type of α** (scalar vs. GL_n-valued) and state M2 and M4 explicitly. Falsifier: with a scalar α and nonsplit A, no certificate can exist.
2. **Either prove M4 is syntactic** from the cochain identity for arbitrary input γ, **or drop it from soundness** via Section 4. Falsifier: the ρ∘τ perturbation in Section 3.
3. **Audit the primitive** for zero-concluding branches. Each one is an unverified EquSLP decision.
4. **Specify the form of θ and a.** If either contains additions, check 1 of the verifier becomes randomized too.
5. **Claim boundary.** The resulting statement is "polynomial-size circuit for x plus a one-sided randomized verifier." It is not a deterministic certificate, and it implies nothing about hardness or speedup.
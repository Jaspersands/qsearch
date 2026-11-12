# Report: charpoly of Frobenius on a finite étale ℓ-group via Hopf-algebra operations

## Verdict

**The lemma is true.** There is a deterministic algorithm that computes χ_F ∈ F_ℓ[X], the characteristic polynomial of arithmetic Frobenius σ on U = G(F̄_p).

- It uses only F_p-linear algebra inside C. It builds no splitting field and no point labels.
- Write N = rank C = ℓ^m. The cost is O(m·N^5 + N^4·log p) operations in F_p.
- The bit cost is O((m·N^5 + N^4·log p)·M(log p)), where M(·) is the cost of integer multiplication.
- Integer-side work and polynomial enumeration over F_ℓ add only lower-order terms.

So the cost is poly(N, log p). Since ℓ ≤ N, it is also poly(rank C, log p, ℓ).

**Corrections to the sketch as stated:**

1. The method returns the charpoly of **arithmetic** σ. Geometric Frobenius gives the reciprocal polynomial.
2. The rank of multiplication by an idempotent must be computed by elimination, not by trace. Trace only gives rank mod p, and p ≤ N is allowed.
3. f(F) must be evaluated by Horner's rule with contraction after every addition. The naive tensor expansion has tensor degree up to about (ℓ−1)(deg+1) and blows up to dimension N^{Θ(mℓ)}.

**Scope blocker (not a refutation).** The bound is polynomial in N = ℓ^m, so it is exponential in m. If the m in this lemma is the header's m = 13516, then N ≥ 2^13516. Even the input size, Θ(N^3 log p), is far outside any degree-53 poly(log p) budget. For ℓ = Θ(log p), staying under degree 53 needs roughly 5m ≤ 53, i.e. m ≤ 10, and even 3m ≤ 53 just to read the input. This must be resolved upstream.

The rest is the proof.

---

## 1. Conventions and the Frobenius map

**Input.**
- C is a finite étale commutative F_p-algebra of dimension N, given by structure constants c_{ij}^k in a basis b_1..b_N, and a unit vector for 1.
- Δ: C → C⊗C is given by coefficients δ^{s}_{ik} with Δ(b_s) = Σ δ^s_{ik} b_i⊗b_k.
- The counit ε: C → F_p and the antipode S are also given.
- C is a commutative, cocommutative Hopf algebra. G = Spec C has G(F̄_p) ≅ U ≅ (Z/ℓ)^m.

**Points.** A geometric point is an F_p-algebra homomorphism x: C → F̄_p. The group law is y·z := (y⊗z)∘Δ. The identity is ε.

**Endomorphisms.** An F_p-algebra map A: C → C defines a point map α(x) := x∘A. When A is compatible with Δ, ε, S, α is a group endomorphism. We write A = α*.

**Proposition 1 (variance and sign of Frobenius).** Let Φ(a) = a^p.

(a) Φ is F_p-linear. Indeed (a+b)^p = a^p + b^p, and λ^p = λ for λ ∈ F_p.

(b) Φ is a Hopf endomorphism. In the commutative F_p-algebra C⊗C we have (Σ u_i⊗v_i)^p = Σ u_i^p⊗v_i^p. Since Δ is an algebra map, Δ(a^p) = Δ(a)^p = (Φ⊗Φ)Δ(a). Similarly ε(a^p) = ε(a)^p = ε(a).

(c) The induced point map is F(x) = x∘Φ, and (x∘Φ)(a) = x(a)^p = σ(x(a)). So F = σ, **arithmetic** Frobenius, acting by x ↦ σ∘x. It is a group automorphism of U, because σ is bijective on G(F̄_p).

Geometric Frobenius σ^{-1} has charpoly χ_{σ^{-1}}(X) = X^m·χ_σ(1/X)/χ_σ(0). This is well defined because χ_σ(0) ≠ 0.

(d) For an abelian variety A over F_p, the relative Frobenius π_A acts on A(F̄_p) exactly as σ. So the charpoly of σ on A[ℓ] equals the Weil polynomial mod ℓ.

For any other Galois module (for example H² with μ_ℓ-twists, or a dual), the twist and duality conversion is a **separate proof obligation**. It is not part of this lemma.

## 2. Hopf calculus: no representation growth

**Lemma 2.** Let A, B be algebra maps with point maps α, β.

(i) The algebra map Σ(A,B) := μ∘(A⊗B)∘Δ has point map x ↦ α(x)·β(x) = (α+β)(x).

*Proof.* Since x is an algebra map, x∘μ = μ_{F̄}∘(x⊗x). Hence
x∘μ∘(A⊗B)∘Δ = ((x∘A)⊗(x∘B))∘Δ = α(x)·β(x). ∎

(ii) The composite A∘B has point map x ↦ (x∘A)∘B = β(α(x)). Pullback is contravariant. In particular, the algebra map of ψ∘F is Φ∘Ψ.

(iii) The map a ↦ ε(a)·1 is the zero endomorphism. The identity map of C is id_U. For integers c ≥ 0, c·id is obtained by iterating (i); S gives −id but is never needed.

**Evaluating g(F).** Let g(X) = X^D + g_{D−1}X^{D−1} + … + g_0 ∈ F_ℓ[X]. Choose integer representatives ĝ_i ∈ [0, ℓ).

- Precompute the matrices E_c := (c·id)* for c = 0..ℓ−1. This takes ℓ−2 applications of Σ.
- Horner: set Ψ ← I. For i = D−1 down to 0, set Ψ ← Σ(Φ·Ψ, E_{ĝ_i}).

By induction using Lemma 2, Ψ is the pullback of ĝ(σ). On U, multiplication by ℓ is zero, so ĝ(σ) = g(σ). This needs only that U is elementary abelian; no scheme-level [ℓ] = 0 is used.

**Growth control.**
- Every intermediate object is an N×N matrix over F_p, about N² log p bits, whatever D or the coefficients are.
- The tensor square C⊗C appears only transiently, inside one application of Σ, and is contracted immediately.
- No C^{⊗k} with k > 2 is ever formed.

**Cost of one Σ.** Fix a basis element b_s.
- Form the N×N coefficient matrix D_s of Δ(b_s).
- Compute A·D_s·B^T in O(N³). This gives (A⊗B)Δ(b_s) in the basis b_u⊗b_v.
- Contract with the structure constants in O(N³).

Over all s this is O(N^4) F_p-operations.

Composition with Φ is one matrix product, O(N³). Powers ψ^j = ψ^{j−1}∘ψ are matrix products, O(N³) each.

## 3. The identity idempotent

**Lemma 3.** Let 𝔪 = ker ε. Then Ann(𝔪) = F_p·e0, where e0 is the unique primitive idempotent with ε(e0) = 1. Moreover, a geometric point y satisfies y(e0) = 1 iff y = ε, and y(e0) = 0 otherwise.

*Proof.*
- C is étale, so C ≅ ∏ K_i with K_i finite fields.
- ε: C → F_p is a surjective algebra map. So 𝔪 is maximal with residue field F_p, and equals the kernel of the projection to one factor K_0 = F_p.
- Hence 𝔪 = 0×∏_{i≠0}K_i, and Ann(𝔪) = K_0×0 = F_p·e0.
- For a point y, y(e0) is an idempotent in F̄_p, so it is 0 or 1.
- y(e0) = 1 iff y kills 1−e0, iff y factors through C·e0 ≅ F_p (via ε), iff y = ε. ∎

**Construction.**
- 𝔪 is spanned by b_i − ε(b_i)·1.
- Solve the homogeneous system (L_{b_i} − ε(b_i)I)·a = 0 for all i. Here L_b is multiplication by b, read off the structure constants.
- This is an N²×N system, solved by deterministic Gaussian elimination in O(N^4) F_p-operations.
- The solution space is one-dimensional. Normalize the solution so that ε(a) = 1.
- If the solution space is not one-dimensional, the input is invalid; reject.

## 4. Kernel order from rank

**Lemma 4.** Let ψ be a group endomorphism with algebra map Ψ, and set e := Ψ(e0). Then e is idempotent, and dim_{F_p}(C·e) = |ker ψ on U|.

*Proof.*
- Ψ is an algebra map, so e² = e.
- C·e is a direct factor of C, hence étale. So dim_{F_p} C·e = #Hom(C·e, F̄_p), the number of points x of G with x(e) = 1.
- x(e) = x(Ψ(e0)) = (x∘Ψ)(e0) = ψ(x)(e0). By Lemma 3 this is 1 iff ψ(x) = ε.
- So the points of C·e are exactly ker ψ. ∎

**Computation.**
- Form L_e = Σ_s e_s L_{b_s} in O(N³).
- Compute rank L_e = dim C·e by elimination in O(N³).
- **Do not use Tr(L_e).** It equals the rank only mod p, and that fails whenever p ≤ N. Example: N = 4, p = 3, rank 4 ≡ 1.

**Exact logarithm.** The rank r is an integer with 1 ≤ r ≤ N. Compute k = log_ℓ r by at most m exact divisions by ℓ. If r is not a power of ℓ, reject the input. If ℓ is not supplied, recover it as the exact integer m-th root of N.

## 5. From kernel exponents to χ_F

Regard U as an F_ℓ[X]-module, with X acting as F. By primary decomposition, U = ⊕_f V_f, where V_f = ker f(F)^J for J ≥ dim V_f / deg f.

**Choice of J.**
- Since dim V_f ≤ m, J_f := ⌊m/d⌋ suffices, with d = deg f.
- Write t_f = dim V_f / d. The minimal polynomial of F on V_f is f^s with s ≤ t_f ≤ J_f. So f(F)^{J_f} kills V_f.

**Charpoly of each block.**
- Every irreducible factor of χ_{F|V_f} divides the minimal polynomial f^s.
- So χ_{F|V_f} = f^{dim V_f / d}, and χ_F = ∏_f f^{k_{f,J_f}/d}.

**Elementary divisors (bonus).** Write k_{f,j} = log_ℓ |ker f(F)^j|. Then k_{f,j} = d·Σ_i min(λ_{f,i}, j). The increments (k_{f,j} − k_{f,j−1})/d count the elementary divisors f^λ with λ ≥ j. So the full Segre data is also recovered.

**Built-in checks.**
- Σ_f k_{f,J_f} = m.
- k_{X,1} = 0, because F is invertible.
- Every increment is divisible by d and non-increasing in j.

Any violation means the input is invalid.

**Irreducible enumeration (deterministic).** For each d ≤ m, enumerate all ℓ^d monic polynomials of degree d. Test irreducibility with Rabin's criterion:
- f | X^{ℓ^d} − X, and
- gcd(X^{ℓ^{d/q}} − X, f) = 1 for each prime q | d.

Compute X^{ℓ^i} mod f by repeated ℓ-th powering. This costs poly(d, log ℓ) per candidate, so ℓ^m·poly(m, log ℓ) in total. That is dominated by the rest and needs no randomness.

## 6. Full algorithm and bit cost

| Step | Work | F_p-operations |
|---|---|---|
| Φ matrix | b_s^p by square-and-multiply, N·2log p products at O(N³) each | O(N^4 log p) |
| e0 | Lemma 3 | O(N^4) |
| E_c, c < ℓ | ℓ−2 applications of Σ | O(ℓN^4) ⊆ O(N^5) |
| Each monic irreducible f, deg d | Horner for f(F): d steps, each O(N^4) | O(dN^4) |
| | powers ψ^j for j ≤ ⌊m/d⌋ | O((m/d)N³) |
| | ranks | O((m/d)N³) |

**Pruning.** If k_{f,1} = 0, skip j > 1.

**Totals.**
- Summing over all f: Σ_{d≤m} ℓ^d·(dN^4 + (m/d)N³) ≤ 2mℓ^m N^4 + O(mℓ^m N³) = O(mN^5).
- Overall: O(mN^5 + N^4 log p) F_p-operations, each of bit cost O(M(log p)).
- Inversions occur only in elimination: O(N³) per elimination, each O(M(log p)·log log p) bits.
- Integer and F_ℓ work: ℓ^m·poly(m, log ℓ) bit-operations.
- Input size: Θ(N³ log p) bits.
- Total bit complexity: O((mN^5 + N^4 log p)·M(log p)), polynomial in (N, log p) as claimed.

Asymptotically faster matrix multiplication lowers the exponent of N but does not change the qualitative picture.

The lemma only needs U elementary abelian and C étale. The condition ℓ ≠ p enters solely through étaleness: an étale Z/p would also work, while μ_p would fail.

## 7. Optional certification of the promise (all poly(N))

None of these checks is needed if the input is promised valid, but each is cheap:

- **Étaleness.** C is étale iff Φ is bijective.
  - A nonzero nilpotent a has a^{p^k} = 0 for some k, so Φ is not injective. Conversely, a ≠ 0 with a^p = 0 is nilpotent.
  - Reduced over the perfect field F_p is equivalent to étale.
  - Check rank Φ = N: O(N³).
- **Hopf axioms.** Coassociativity, counit, antipode, and multiplicativity of Δ: O(N^5) by direct contraction.
- **Commutativity of U.** Cocommutativity Δ = τΔ: O(N³).
- **Exponent ℓ.** Check (ℓ·id)* = the zero map a ↦ ε(a)·1: O(ℓN^4).

With rank N = ℓ^m and ℓ prime, an abelian group of exponent ℓ is (Z/ℓ)^m. These checks plus the consistency checks of §5 turn the promise into a certificate.

## 8. Status of obligations

- **Proved:** Proposition 1, Lemmas 2–4, the primary-decomposition step, deterministic enumeration, the exact logarithm, and the bit-cost bound.
- **Assumed (input promise):** C, Δ, ε, S are given explicitly as structure-constant tensors over F_p of size O(N³), and the constants are correct. Correctness is verifiable as in §7.
- **Not covered and open:**
  - **(a)** Producing C from the surface data within budget. Its size is already ℓ^{3m}·log p.
  - **(b)** Identifying U, and its twist and duality, with the module whose P2 factor is targeted. The sign or variance conversion in Proposition 1(c) must be fixed there.
  - **(c)** Reconciling N = ℓ^m with the degree-53 target. If m = 13516 or anything near it, the lemma is correct but unusable. **This is the concrete blocker.**

## 9. Falsifiers and finite controls (run by the requester; nothing was executed here)

1. **Twisted plane.** Take ℓ = 2, p = 3, U = F_4 with σ acting as multiplication by ω, which has order 3.
   - The orbits are {0} and {1, ω, ω²}, so C ≅ F_3 × F_27.
   - Expected: k_{X²+X+1,1} = 2, k_{X−1,j} = 0, χ = X²+X+1.
   - Rank check: |ker(F−1)| = 1, so the rank is 1, while the trace mod 3 of a rank-4 idempotent would be 1. This exercises §4's warning.
2. **Unipotent versus identity.** Take U = (Z/ℓ)² with σ = [[1,1],[0,1]], against σ = I.
   - Expected k_{X−1,1} = 1 versus 2, and k_{X−1,2} = 2 in both cases.
   - The algorithm must separate the Jordan structures even though both charpolys are (X−1)².
3. **Sign test.** In any example where σ ≠ σ^{-1} on U, check that the output equals χ_σ and not its reciprocal. Control 1 does not do this, since X²+X+1 is self-reciprocal.
4. **Bad-input rejection.**
   - Replacing Δ by a non-coassociative tensor must trigger §7.
   - Using a non-reduced C, for example F_p[x]/(x^p) as the coordinate ring of μ_p, must fail the Φ-bijectivity check. Without that check, the rank formula would wrongly report kernel orders.

Any control giving χ inconsistent with an independently known Galois action would falsify this report. Until such controls are run, the result rests on the proofs above only.
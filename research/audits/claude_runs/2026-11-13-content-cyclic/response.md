# Cyclic-projection content cover for native sparse norms with growing δ: verdict and proof ledger

## 0. Verdict

**No general guarantee is proved.** I found no native counterexample. The full primitive, complete finite-prime support for growing δ, **remains OPEN**.

What is established below:

- **(P1) Certified multiple, zero-error.** Any nonzero projection gives a nonzero integer C with content(P) | C and |C| ≤ ‖P‖₁. Computing it is polynomial-time without expanding the norm. Failure is detected, never silent.
- **(P2) Exact failure criterion.** For q prime, the projection vanishes iff Φ_q·(T−1) divides the Kronecker image P_w. A pure support/degree argument cannot rule this out once δ grows.
- **(P3) Bounded-expansion theorem.** This gives polynomial q when the expanded support is polynomial. It covers fixed δ, which is already matched by known algorithms.
- **(P4) New growing-δ positive family.** For every promised-irreducible radical (Kummer) field f = Y^δ − T^α, with u arbitrary sparse, polynomial q suffices. This holds although the norm's expansion is exponential in δ. So exponential expansion alone is **not** a falsifier.
- **(N) Falsifier ledger.** T^M−1 with M = lcm(1..Q₀), binomial products, and cyclotomic multiplicity all fail to defeat a polynomial window Q = poly(n)/ε.

The open gap is reduced to one explicit statement (CSB, §6).

## 1. (P1) The certified multiple and its cost

**Computational object.** Clear rational coefficients to get integer f̃, ũ ∈ Z[T][Y]. Let S be their Sylvester matrix, of size ≤ 2δ−1. Its entries are the original explicit sparse coefficients, so S is genuinely sparse. Since f is monic, Res(f̃, ũ) equals ±Norm(u) times explicit powers of the clearing denominators. Those denominators are explicit sparse polynomials whose contents are read off directly. Hence covering content(det S) also covers content(det A_i) modulo explicitly computable factors.

**Coefficient bound.** Write P = det S.
- By the determinant expansion, ‖P‖₁ ≤ ∏_rows Σ_j ‖S_ij‖₁ =: V_S. The exponent log V_S is polynomial in the input bits.
- **Deterministic Kronecker step.** Let B = 1 + (a binary bound on every per-variable degree of P). Set P_w(T) = P(T, T^B, …, T^{B^{s−1}}). This map is injective on monomials, so P_w ≠ 0. Its exponent bit length is n' ≤ s·log B, which is polynomial.
- Every coefficient of P_w mod (T^q − 1) is a sum of coefficients of P. So the projection's coefficients are integers in [−V_S, V_S], and content(P) divides each of them.

Therefore any nonzero projection coefficient C satisfies 0 < |C| ≤ V_S and content(P) | C.

**Computation, with no expansion.** Reduce every exponent ⟨w, α⟩ modulo q, using binary arithmetic on exponents. Then compute det over R_ℓ = F_ℓ[T]/(T^q − 1) for O(log V_S) word-size primes ℓ:
- Use a division-free determinant algorithm (Berkowitz-type), which is valid over non-domains. It needs O(δ⁴) ring operations, each costing O(q²) field operations.
- Alternatively, split T^q − 1 over F_ℓ for ℓ ∤ q and run Gaussian elimination in each factor field.
- Recover the integer coefficients by CRT, using the a-priori bound |coeff| ≤ V_S.

No intermediate-growth analysis is needed. The native multiplication matrix A_i can also be formed inside R_ℓ, via companion powers, without expanding its entries. Those entries can have exponentially many terms when δ grows.

**Zero-error behaviour.** The output is either a certified nonzero multiple or "all projections zero". Repeating with fresh q costs log(1/η) only under a per-trial success bound, and such a bound is exactly what is missing in general.

**Post-processing (charged separately).**
- Factor C, which has at most log V_S bits; integer factoring is allowed but charged.
- For each prime factor p, test whether p actually divides the content. This means deciding whether det(S mod p) ≡ 0 in F_p[T]. Evaluate at a random point of F_{p^r}^s with p^r ≥ 2·deg/ε, so r = O((log D + log 1/ε)/log p). The test has one-sided error.
- The result is the exact set of content primes from any single nonzero C. Without factoring, C still serves as a coprime-base multiple.

## 2. (P2) Exact failure criterion and two cheap augmentations

- **When projection fails.** P_w mod (T^q − 1) = 0 iff P_w vanishes at every q-th root of unity. For q prime this means P_w(1) = 0 and Φ_q | P_w. By Galois conjugation, vanishing at one primitive ζ_q implies vanishing at all of them.
- **q = 1 test.** C₁ = P(1,…,1) has |C₁| ≤ V_S. If it is nonzero, we are done. An adversary must therefore have P(1,…,1) = 0.
- **Multivariate, random weights.** For random w the bad event is "P vanishes at the torsion point ζ^w". A cyclic subgroup always contains the identity, so the analysis is the same.
- **Taylor augmentation.** Let ρ be a root of unity of small order r. Compute P_w(ρ(1+x)) mod x^{K+1} over Z[ζ_r][x]/(x^{K+1}). Here T^e maps to ρ^e Σ_{i≤K} C(e,i) x^i, with coefficient bits ≤ K·n'.
  - The first nonzero x-coefficient is a nonzero element of Z[ζ_r] divisible by content(P).
  - Its norm to Q has polynomial bits: at most r·(log V_S + K·n').
  - This succeeds whenever ord_ρ P_w ≤ K. An adversary must then also have high multiplicity at every small-order root of unity.
  - This is a strengthening only, not a proof.

## 3. (N) Cheapest falsifiers (none survives a polynomial window)

Throughout, the window is: q is a random prime in [Q, 2Q]. I use the retained Rosser–Schoenfeld count of more than 3Q/(5 ln Q) primes in the window, and the fact that a nonzero integer d has at most log|d|/log Q prime factors that are ≥ Q.

1. **P = T^M − 1, M = lcm(1..Q₀).** This is native, e.g. δ = 1 with u = T^M − 1. The projection vanishes iff q | M. Bad primes in the window number at most log₂M / log₂Q ≤ n / log₂Q. Since Q₀ ≲ n, this defeats only Q ≲ n. Survives? **No.**
2. **Products of binomials ∏(T^{a_i} − T^{b_i}).** Vanishing at ζ_q needs q | (a_i − b_i) for some i. The bad primes divide ∏(a_i − b_i), whose bit length is ≤ the input bits. Survives? **No.**
3. **Cyclotomic high multiplicity.** This is irrelevant to the projection test, because the zero criterion is set-theoretic. It matters only to the §2 Taylor variant.
4. **Exponential expansion from native companion/Sylvester cancellation.** The Kummer case (§5) is not a counterexample despite exponential expansion. The general case is open.

## 4. (P3) Bounded-expansion theorem

**Theorem A.** Suppose |supp P_w| ≤ N and the exponents are ≤ 2^{n'}. Then for q prime with N < q, the projection is zero only if q divides some nonzero difference of two support exponents.

*Proof.*
1. Group coefficients by exponent mod q. P_w(ζ) = 0 forces all class sums to be equal, since the only Q-relation on ζ^0, …, ζ^{q−1} is that their sum is zero.
2. Because N < q, some class is empty, so every class sum is zero.
3. Any nonzero coefficient must therefore share its class with another support element, so q divides their exponent difference. ∎

**Window bound.** There are at most N² differences, each with at most n'+1 bits. The bad fraction is at most 1.2·N²(n'+1)/Q. So Q ≥ 2.4·N²(n'+1)/ε suffices.

**Sylvester instance.** N ≤ t_f^{deg u}·t_u^{δ}, where t_f and t_u count the terms of f̃ and ũ. This is polynomial for fixed δ and exponential for growing δ. The method may still work there; only this proof stops.

## 5. (P4) Growing-δ radical family

**Theorem B.** Assume:
- f = Y^δ − T^α, promised irreducible;
- ũ = Σ_{j<δ} Σ_l c_{jl} T^{α_{jl}} Y^j is a nonzero integer sparse polynomial with t' ≤ δt terms;
- P_w = Res(f, ũ)_w after the Kronecker step, with a = ⟨w, α⟩.

Let q be prime with q ∤ δ and q > δt. Suppose q divides none of the at most (δt)² nonzero integers δ·(a_{jl} − a_{j'l'}) + a·(j − j'). Then Φ_q ∤ P_w, so the projection is nonzero.

*Proof.*
1. **Norm factorisation.** P_w = ∏_{ω ∈ μ_δ} ũ(ωβ), where β^δ = T^a.
2. **Specialise.** At T = ζ (primitive q-th root), take k with kδ ≡ 1 mod q. The roots of Y^δ = ζ^a are then ωζ^{ak}.
3. **Write the factor.** Each factor equals Σ c_{jl} ω^j ζ^{a_{jl} + ajk}. Every term is ζ^{(exponent)} times an element of Q(ζ_δ).
4. **Linear disjointness.** Since q ∤ δ, [Q(ζ_{qδ}) : Q(ζ_δ)] = q − 1, using the standard irreducibility of Φ_q. So 1, ζ, …, ζ^{q−2} is a basis over Q(ζ_δ), and the only relation is Σ ζ^r = 0.
5. **Formal classes.** Group the terms by formal exponent E = a_{jl} + ja/δ ∈ (1/δ)Z. Some formal class sum S_E ∈ Q(ζ_δ) is nonzero; otherwise ũ(ωT^{a/δ}) ≡ 0 and P_w = 0. This remains valid even if Kronecker identifies formal classes.
6. **Residues.** The residue mod q of E's class is k·(δE). If a factor vanishes, all residue-class sums are equal. Since δt < q, some residue class is empty, so all residue-class sums are zero.
7. **Conclusion.** The residue class of a nonzero S_E must contain another formal class E', so q | δ(E − E'). This is exactly one of the displayed nonzero integers, each of size ≤ δ·2^{n'} + aδ. ∎

**Window bound.** The bad fraction is at most 1.2·(δt)²(n' + log₂(aδ) + 2)/Q + log δ/log Q. So Q = O((δt)²(n' + log δ)/ε) suffices, uniformly in growing δ, s and k. The bit costs are those of §1.

**Scope caveat.** Coefficients c·T^α with c ≠ ±1 are deliberately excluded. Q(c^{1/δ}) can meet Q(ζ_q), e.g. √q ∈ Q(ζ_{4q}). That case needs its own disjointness argument.

## 6. Exact open obligation and what a negative must show

The argument in §5 used that, at torsion T, every branch is a root of unity, i.e. that linear disjointness holds. For general f, the roots of f(ζ_q, ·) are arbitrary algebraic numbers of degree ≤ δ over Q(ζ_q). Degree counting only gives #bad ≤ D/Q, which is useless.

**CSB (needed for a positive).** For every native pair (f, u) with t terms, δ, and n'-bit exponents, the number of primes q ∈ [Q, 2Q] with Res_Y(f, u)_w(ζ_q) = 0 is at most poly(t, δ, n', log Q). It is enough that this is < ½ of the primes in the window for some Q = poly. Equivalently: the T-coordinates of the 0-dimensional intersection {f = u = 0} on the sparse plane curve contain few full primitive-root orbits of prime order.

**Counterexample requirements.** A counterexample must be an explicit native univariate family (weights are then irrelevant) such that, for every polynomial Q(n):
- (T−1)·∏_{q ∈ window} Φ_q divides P;
- to beat §2 as well, it has high multiplicity at small-order roots of unity.

The required degree, about Q²/(2 ln Q), is affordable. So only an explicit construction, or a CSB proof, decides the question.

**Necessary features of a counterexample:**
- f cannot be radical (Theorem B).
- No fixed algebraic root β₀ can be shared by f and u: then f(T, β₀) would be an explicit sparse polynomial, and Theorem A applies to it.
- Every branch must vary with T in a non-cyclotomic way.

**Speculation, unproved.** For arbitrary sparse-entry determinants, as opposed to native resultants, CSB would amount to an explicit lower bound for representing multiples of ∏Φ_q. I do not know such a bound to be available, and I import none. Native resultants are a strict-looking subclass: f and u must themselves be explicitly sparse, and characteristic polynomials of sparse matrices are not. No hardness is inferred from the absence of a proof.

## 7. Residual obligations outside this gate

1. Prove that covering content(Res(f̃, ũ)) together with the explicit denominator contents covers all relevant vertical primes. This includes non-integral Y-basis coefficients and order-index or discriminant primes, as flagged in the torus-vertical proposal; that claim is unchecked here.
2. Once some nonzero C is found, the remaining steps (factoring, mod-p PIT filtering, valuations) are polynomial except for the charged factoring.

## 8. Next falsifiers, cheapest first

1. Trinomial fields f = Y^δ + T^a·Y + T^b with u = Y − T^c, where P = f(T^c) (with explicit c^j powers). Search for primes q ≤ 10³ with Φ_q | P_w using exact modular checks, at growing δ.
2. Fields with f(T, Y) = g(Y) − h(T), where g is non-radical, e.g. g = Y^δ − Y. Is h(ζ) ∈ g(Q̄) ∩ {u = 0} forced for many q?
3. A Kummer twist with c = q-dependent constants, to test the scope caveat in §5.

Any such exact control would be a finite falsifier only, not an asymptotic statement.
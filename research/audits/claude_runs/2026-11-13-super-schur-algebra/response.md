# Review of contract.md: fixed-Durfee Kronecker computation via hook Schur specialization

## Verdict

I attacked the interface through tensor parity, sign conventions, conjugation, hook vanishing, independence, and the lex-leading claim. **I found no coefficient alias, sign error, conjugation error, or hidden exponential output** under the convention the contract declares authoritative. The interface is correct for:

- all λ ⊢ n with Durfee(λ) ≤ d,
- all μ ⊢ n with Durfee(μ) ≤ e,
- every ν ⊢ n.

A proof follows. The bit complexity is polynomial in n for fixed d and e, with an exponent that grows like O(d+e). However, the contract leaves four operations uncharged or unspecified (§4). There is also one real failure mode: if two sign conventions are mixed, the triangular extraction returns wrong numbers silently (§3).

The contract's stated motivation is **not supported by the supplied excerpts** (§5). It also does not cover the "one-hook" case it cites.

## 1. Convention reconciliation (proved)

**Moens convention (excerpt lines 284–315).** The definition is h_r(x/y) = Σ_j h_{r−j}(x) e_j(y). Its generating function is H(t) = ∏(1+y_j t)/∏(1−x_i t). Taking the logarithm:

- log H(t) = Σ_r [p_r(x) + (−1)^{r−1} p_r(y)] t^r / r.

This matches the contract's p_r(X) exactly.

**Pragacz (excerpt lines 260–296).** Pragacz writes S_I(A−B). The supplied excerpt does not state his generating function. In the standard λ-ring reading, S_I(A−B) = s_I(x/y) evaluated at y = −b. That reading is a lead, not verified from the excerpt. The reconciliation does not depend on it, because:

- **Vanishing is invariant.** y ↦ −y is a ring automorphism of Z[x,y], and it preserves which polynomials are zero.
- **Independence is invariant.** The same automorphism preserves Z-linear independence.
- **Hook orientation is fixed by Pragacz's own example.** I = (2,5,6,8), sorted decreasingly as (8,6,5,2), is "not contained" in the (2,4)-hook. This forces the rule "contained ⇔ I_{m+1} ≤ n" with m = |A|. The conjugate reading would be λ'_3 = 3 ≤ 4, which would make I contained, contradicting the example.
- **Moens agrees.** Moens states vanishing "when λ_{m+1} > n".
- **Square hooks make orientation irrelevant.** For m = n = d, the condition a_{d+1} ≤ d is equivalent to Durfee(a) ≤ d.

**Tensor parity (proved).** Expanding the product of power sums:

- p_r(X) p_r(Z) = p_r(xu) + p_r(yv) + (−1)^{r−1}[p_r(xv) + p_r(yu)], using ((−1)^{r−1})² = 1.

So the even entries are xu and yv, and the odd entries are xv and yu. This is exactly what the contract states.

## 2. Proof of the interface

Work in Λ_Q = Q[p_1, p_2, …], which is free on the power sums.

**P1 (specialization is a ring homomorphism).** Define φ_X : Λ_Q → Q[x,y] on generators by p_r ↦ p_r(x) + (−1)^{r−1} p_r(y). Since Λ_Q is free on the p_r, this determines a ring homomorphism.

- By §1, φ_X(H(t)) = exp(Σ φ_X(p_r) t^r/r) = ∏(1+yt)/∏(1−xt). Hence φ_X(h_r) = h_r(x/y).
- Jacobi–Trudi is a polynomial identity in the h_r. Therefore φ_X(s_a) = det(h_{a_i−i+j}(x/y)) = hs_a(X), which is Moens (16).
- No conjugation enters: hs_a(x/0) = s_a(x).

**P2 (universal Kronecker identity).** Use the character expansions:

- s_ν = Σ_ρ χ^ν(ρ) p_ρ / z_ρ,
- p_ρ = Σ_a χ^a(ρ) s_a.

Define Δ : Λ_Q → Λ_Q ⊗ Λ_Q as the ring homomorphism with p_r ↦ p_r ⊗ p_r. Then

- Δ s_ν = Σ_{a,b} [Σ_ρ χ^a(ρ) χ^b(ρ) χ^ν(ρ) / z_ρ] s_a ⊗ s_b = Σ_{a,b ⊢ n} g(a,b,ν) s_a ⊗ s_b,

because S_n characters are real.

Now compare two ring homomorphisms Λ_Q → Q[x,y,u,v]:

- (φ_X ⊗ φ_Z) ∘ Δ, and
- φ_{X⊗Z}, defined by p_r ↦ p_r(X⊗Z).

Both send p_r to p_r(X) p_r(Z), so they are equal. Applying both to s_ν, and using P1 for the super alphabet X⊗Z (2de even and 2de odd entries), gives the contract's identity:

- hs_ν(X⊗Z) = Σ g(a,b,ν) hs_a(X) hs_b(Z).

Signs: there is no ω-twist and no conjugation.

**P3 (hook vanishing).** By Moens/Pragacz, hs_a(X) = 0 iff a_{d+1} > d, i.e. iff Durfee(a) > d. My own route: hs_a = Σ_{κ ⊂ a} s_κ(x) s_{a'/κ'}(y). The s_κ(x) factor needs ℓ(κ) ≤ d. Then rows d+1, d+2, … of a lie in a/κ. Those rows must have length ≤ d for s_{a'/κ'}(y) in d variables to be nonzero. So only hook partitions survive on the right-hand side.

**P4 (lex-leading claim; independent proof of independence).** Fix the lex order x_1 > … > x_d > y_1 > … > y_d. Let a be a hook partition and ρ = (a_{d+1}, a_{d+2}, …).

- **Expansion.** hs_a = Σ_κ s_κ(x) s_{a'/κ'}(y).
- **Which κ can reach the top x-monomial.** The monomial x^α appears in s_κ(x) only if κ ⊵ α. The constraints κ ⊂ a and ℓ(κ) ≤ d give κ_i ≤ a_i.
  - So the lex-maximal x-exponent is α = (a_1, …, a_d).
  - It occurs only for κ = α, with Kostka number K_{α,α} = 1.
- **The remaining y-factor.** The cofactor is s_{ρ'}(y), where ρ'_j = max(a'_j − d, 0).
  - ℓ(ρ') = ρ_1 = a_{d+1} ≤ d.
  - So its lex-leading monomial is y^{ρ'}, with coefficient 1.

Hence LM(hs_a) = x^{(a_1,…,a_d)} y^{ρ'}, with coefficient 1. **The contract's claim holds.**

Two checks on the formula:

- d = 1, a = (1⁴): hs = x y³ + y⁴, so LM = x y³. ✓
- d = 2, a = (3): LM = x_1³. ✓

The exponent vector returns (a_1, …, a_d) and ρ' directly, hence a. So the map a ↦ LM is injective. Distinct leading monomials with unit leading coefficients give Z- and Q-linear independence. This does not rely on Pragacz Theorem 3.

Note that the claim depends on the variable order. If y precedes x, the leading monomial changes to the conjugate-type monomial.

**P5 (product basis).** The X and Z variables are disjoint, and lex order is a monomial order. So LM(hs_a(X) hs_b(Z)) = LM(hs_a(X)) · LM(hs_b(Z)), with leading coefficient 1. Distinct pairs (a,b) therefore have distinct leading monomials.

**Conclusion.** The coefficients in the identity are uniquely determined. The coefficient of hs_λ(X) hs_μ(Z) is exactly g(λ,μ,ν). There is no folding or aliasing.

**Free corollary (proved here).** X⊗Z has 2de even and 2de odd entries. So the left-hand side vanishes when Durfee(ν) > 2de, and by independence g(a,b,ν) = 0 for all hook pairs (a,b). The algorithm should return 0 immediately in that case. Prior statements of this bound (Berele–Remmel, Dvir) are unverified leads only.

**Finite control (sign check only, not evidence of anything general).** Take n = 2, d = e = 1, ν = (1,1).

- Left-hand side: e_2(xu, yv / xv, yu).
- Right-hand side: (x² + xy)(uv + v²) + (xy + y²)(u² + uv).
- Both expand to the same eight monomials, including 2xyuv.

## 3. Attempted falsifications

**(a) Conjugation or ω error.** Excluded by P1: the x-letters are even, and no ω is applied anywhere.

**(b) Treating odd tensor entries as even.** This means plain s_ν in 4de commuting variables. That changes p_r and is wrong. The contract avoids this mistake.

**(c) Convention mixing — a real failure mode.** Suppose the left-hand side is computed with Moens signs but the basis uses Pragacz-literal ∏(1−bt) with b = y. That basis is hs_a(x/−y). Then:

- The left-hand side is generally not in the span of that basis.
- The unitriangular extraction never tests membership in the span.
- So it outputs integers that are wrong, with no error raised.

**Remedy (mandatory):** compute the full residual C − A_X^T G A_Z and require it to be exactly zero (§4d).

**(d) Hidden exponential output.**

- Sizes: g ≤ min(f^λ, f^μ, f^ν) ≤ √(n!), which is O(n log n) bits. There are at most (n+1)^{2d+2e} basis pairs.
- Dense polynomial sizes: the left-hand side is bihomogeneous of bidegree (n,n). It has M_X · M_Z monomials, where M_X = C(n+2d−1, 2d−1) = O(n^{2d−1}), and M_Z is the same with e in place of d.
- Coefficient magnitudes (Moens signs make every coefficient nonnegative):
  - hs_ν(X⊗Z) evaluated at all ones is at most (4de)^n;
  - basis coefficients are at most (2d)^n.
  - So all coefficients have O(n log(de)) bits.

All of this is polynomial for fixed d and e. The scaling is XP in (d,e), not FPT.

## 4. Bit-complexity audit: uncharged or unspecified operations

**(a) Entries of the left-hand side — uncharged.** The contract specifies h_r(X) only for the alphabet X. The ν-determinant needs h_r(X⊗Z) for r ≤ ν_1 + ℓ(ν) − 1 ≤ n. These must be built as the truncated power series

- ∏_{odd w}(1 + wt) / ∏_{even w}(1 − wt), with the 4de products w expanded in Z[x,y,u,v].

This takes O(de) series operations of length n with dense coefficient arithmetic. It is polynomial, but it must be stated and costed.

**(b) The ℓ(ν) × ℓ(ν) determinant, with ℓ(ν) up to n — method unspecified.** Three options:

- **Gaussian elimination over Q(x,y,u,v):** this is the excluded "free rational-function determinant". It risks uncontrolled blow-up and must not be used.
- **Plain division-free Berkowitz:** degrees can blow up. Walk products have index sum up to about k·ν_1 + ℓ, i.e. O(n²) degrees.
  - Fix: run Berkowitz in the truncated ring Z[vars]/𝔪^{2n+1}. Truncation is a ring homomorphism, Berkowitz uses no division, and det is homogeneous of degree 2n. So the result is exact.
- **Evaluation and interpolation:** each variable has degree ≤ n, so a grid of (n+1)^{2d+2e} integer points suffices.
  - At each point, run Bareiss with O(n³) operations on integers of Õ(n²) bits.
  - Then do grid interpolation.
  - Crude total: Õ(n^{5+2d+2e}) bit operations. This is my estimate, not an optimized bound.

**(c) Basis construction.** There are up to (n+1)^{2d} hook partitions a. Each Jacobi–Trudi matrix has size ℓ(a) ≤ n, which is not a constant. So each basis element needs the same determinant care as in (b), and the cost multiplies by the basis count.

**(d) Extraction — make it separable and division-free.**

- Write the coefficient array of the left-hand side as an M_X × M_Z matrix C. Then C = A_X^T G A_Z, where A_X has rows hs_a(X).
- Restricting to leading-monomial columns gives unitriangular integer matrices T_X and T_Z.
- Solve G = T_X^{−T} C_LM T_Z^{−1} by back-substitution. This uses integer arithmetic only, and intermediate bits are bounded by polynomial sums.
- Do not form the products hs_a hs_b as polynomials.
- Then **verify the full residual** (§3c). This costs O(M_X M_Z (n+1)^{2d}) arithmetic operations.

**(e) Encoding.** Hook partitions have O(d log n)-size compact encodings. The contract charges n in unary, so the result is polynomial in n only, not in log n. Keep this restriction explicit.

## 5. Scope and source issues

1. **Unsupported motivation.** The claim "Panova §7.5 leaves fixed-Durfee/one-hook open" is not in the supplied excerpts. The supplied Panova lines 1043–1063 cover §§7.2–7.4. Treat the claim as unverified.
2. **The "one-hook" case is not covered.** The algorithm needs two of the three partitions to have bounded Durfee size. Since g is symmetric in its three arguments, the case with one hook and two arbitrary partitions is **not** handled. If Panova's open case is that one, this algorithm does not address it.
3. **Relation to Panova Theorem 1.1.** That theorem (excerpt lines 77–150) assumes f^ν ≤ n^k. Fixed-Durfee λ and μ can have exponential dimension, e.g. λ = (n/2, 1^{n/2}). So the regime here is not obviously covered by it.
   - Classical results on Kronecker products of hooks and on super-Schur methods (Remmel, Rosas, Berele–Remmel, Campbell 2604.23286) are leads for prior art and are unverified.
   - **Do not claim novelty.**
4. **Relation to Larocca–Havlicek.** Their O(n⁴(d_λ d_μ / d_ν)²) bound (excerpt lines 247–326) matches the contract's R² statement.
   - If the algorithm here is implemented as corrected, the fixed-(d,e) regime admits no superpolynomial quantum advantage from that algorithm.
   - This says nothing about the unrestricted ratio promise, growing d or e, or hardness.

## 6. Remaining proof obligations and falsifiers

**Obligations:**

- (O1) State the determinant method from §4b, with explicit degree and bit bounds.
- (O2) Charge the construction of h_r(X⊗Z) (§4a).
- (O3) Fix the lex variable order and use separable unitriangular extraction (§4d).
- (O4) Make the full residual check mandatory.
- (O5) Add the Durfee(ν) > 2de early exit.
- (O6) State the complexity exponent as a function of (d,e).

**Falsifiers, any one of which refutes an implementation:**

- a nonzero residual;
- a negative g;
- g(λ,μ,ν) ≠ g(μ,λ,ν);
- g(λ,μ,ν) ≠ g(λ',μ',ν) (λ' keeps Durfee size d);
- a nonzero output when Durfee(ν) > 2de;
- disagreement with the character formula at small n.

Passing these finite checks is a control on the implementation, not acceptance of the claim.
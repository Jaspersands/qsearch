# Audit of the single Laurent-coefficient formula in `contract.md`

## 1. Verdict

I found no counterexample. The single-coefficient formula is **correct**, provided one clause is added: the expansion must be fixed to one formal ring, stated below. With that ring, the formula follows by a short argument from two inputs:

- **Proved here:** the plethystic expansion of F, the coproduct decomposition, the Giambelli identity and the hook generating function.
- **Taken from a source:** the Berele–Regev/Pragacz factorization. I translated its sign convention explicitly and checked it in small cases.

Points of scope:

- Correctness of the formula does **not** depend on the linear-independence theorem (Pragacz Thm 3).
- The formula is a statement about a coefficient. It says nothing about running time.
- Every bit-cost claim lives in the compiler, which I flag in §5 but do not certify.
- I answer the contract's "CHECK THIS" item there: **no**. Off-diagonal Giambelli hooks have size at most n.

## 2. Precise statement, with the expansion direction made explicit

Let a = Durfee(λ) ≥ 1 and b = Durfee(μ) ≥ 1. Both are read off as the number of Frobenius coordinates; the input check must enforce α₁>…>α_a≥0 and β₁>…>β_a≥0, and likewise for γ, δ. Let n ≥ 1, and |λ| = |μ| = |ν| = n, checked by exact binary sums.

Work in the ring

  **R = ℤ[x^{±1}, u^{±1}][[y, v]]**,

that is, power series in y₁..y_a and v₁..v_b whose coefficients are Laurent polynomials in x and u.

**Q_X is a unit in R.** Write Q_X = (∏_i x_i^a) · ∏_{i,j}(1 + y_j/x_i).

- The first factor is a unit of ℤ[x^{±1}].
- Each factor 1 + y_j/x_i has constant term 1 in y, so it is a unit of R.
- Its inverse is uniquely Σ_{k≥0} (−y_j/x_i)^k.

So Q_X^{-1} ∈ R is unique and equals the contract's expansion ∏_i x_i^{-a} ∏_{i,j} Σ_k (−y_j/x_i)^k. The same holds for Q_Z with (u, v).

Every monomial coefficient of an element of R is well defined. The coefficient of y^β v^δ is a Laurent polynomial in x and u; take its x^α u^γ coefficient.

**Claim.** For F = hs_ν(T) ∈ ℤ[x, y, u, v],

  g(λ, μ, ν) = [x^α y^β u^γ v^δ] F · Δ(x)Δ(y)Δ(u)Δ(v) · Q_X^{-1} Q_Z^{-1}, computed in R.

Without the ring R, the "rational-function equality" is meaningless, as the brief notes. The proof covers:

- the uniform x-dominant chamber, which the contract specifies, and
- by the mirror argument in §3e, the uniform y-dominant chamber.

**Mixed chambers are not covered and must not be used.** A mixed chamber means expanding some factors (x_i + y_j)^{-1} in y/x and others in x/y. The annihilation step in §3d uses the fact that *every* factor lowers *every* x exponent.

## 3. Independent proof

### (a) Kronecker expansion

Specializing Λ to the super alphabet X is the ring homomorphism

  ev_X : p_r ↦ p_r(x) + (−1)^{r−1} p_r(y).

The internal coproduct sends p_r ↦ p_r ⊗ p_r and s_ν ↦ Σ g(ρ,σ,ν) s_ρ ⊗ s_σ.

Composing with ev_X ⊗ ev_Z sends p_r to p_r(X)p_r(Z). Expanding this product:

- (xu)^r and (yv)^r appear with sign +1, since (−1)^{2(r−1)} = 1;
- (xv)^r and (yu)^r appear with sign (−1)^{r−1}.

This is exactly p_r(T) with xu, yv even and xv, yu odd. Hence F = Σ_{ρ,σ⊢n} g(ρ,σ,ν) hs_ρ(X) hs_σ(Z), a finite sum.

Terms with ρ outside the (a,a)-hook, i.e. ρ_{a+1} > a, vanish. Sources: Pragacz eq. (6); Moens–Van der Jeugt "zero when λ_{m+1} > n". So every surviving ρ has Durfee(ρ) ≤ a.

The same vanishing for T (2ab even and 2ab odd letters) gives F = 0 when Durfee(ν) > 2ab. In that case the coefficient formula also returns 0, which is consistent.

### (b) Factorization and sign translation (sourced)

Pragacz eq. (9) uses λ-ring notation S_I(A − B). Choose:

- A = {x_i};
- B = {−y_j} (numerical negation), so that p_r(A) − p_r(B) = p_r(x) − (−1)^r p_r(y) = p_r(X).

Then:

- R(A, B) = ∏(x_i − (−y_j)) = Q_X.
- S_J(−B) has power sums (−1)^{r−1} p_r(y), which is ev_y∘ω. Hence S_J(−B) = s_{J′}(y).

Pragacz's indexing (J, I+n) with n = |B| = a puts the a largest rows, of length I_k + a, on top of J. Pragacz's numeric example mislabels m and n; this does not affect the general formula.

So for ρ ⊇ a×a inside the (a,a)-hook:

  hs_ρ(X) = Q_X · s_{(ρ_i − a)_{i≤a}}(x) · s_{(ρ′_j − a)_{j≤a}}(y).

- **Sign:** +1, no (−1)^{|J|}.
- **Length:** J′ has at most a parts because ρ_{a+1} ≤ a.

Independent spot checks with a = 1:

- hs_(1) = x + y = Q_X.
- hs_(2) = h₂ = x² + xy = Q_X · x.
- hs_(11) = e₂ = xy + y² = Q_X · y, using E(w) = (1 + xw)/(1 − yw).

These are finite controls only. The general case rests on the source, which the brief says was already checked.

### (c) Durfee exactly a: uniqueness and coefficient +1

In R, Q_X · Q_X^{-1} = 1 exactly, so hs_ρ(X) Q_X^{-1} is the polynomial s_κ(x) s_η(y), with κ = (ρ_i − a) and η = (ρ′_j − a).

With Δ(x) = ∏_{i<j}(x_i − x_j) = det(x_i^{a−j}):

  Δ(x) s_κ(x) = det(x_i^{κ_j + a − j}) = Σ_w sgn(w) x^{w(κ+δ)}.

The exponent vector κ + δ is (ρ_i − i)_i, which is strictly decreasing. A permutation of a strictly decreasing vector is strictly decreasing only when it is the identity. So

  [x^α] = 1 if ρ_i − i = α_i for all i, and 0 otherwise.

The same holds for y with exponents ρ′_j − j and target β.

The Frobenius coordinates (ρ_i − i, ρ′_j − j)_{i,j≤a} of a Durfee-a partition determine it. So exactly one ρ contributes, namely ρ = λ, with coefficient +1.

### (d) Lower-Durfee annihilation in R

Let Durfee(ρ) < a. Then ρ_a ≤ a − 1.

By the coproduct, Δs_ρ = Σ_{κ⊆ρ} s_κ ⊗ s_{ρ/κ}, and the y-evaluation is ev_y∘ω. Hence

  hs_ρ(X) = Σ_{κ⊆ρ, ℓ(κ)≤a} s_κ(x) s_{ρ′/κ′}(y).

Fix any such κ. Then κ_a ≤ ρ_a ≤ a − 1.

- Every monomial of Δ(x) s_κ(x) is x^{w(κ+δ)}. Some coordinate i has exponent κ_a + 0 ≤ a − 1.
- Every monomial of Q_X^{-1} has x_i exponent equal to −a − Σ_j k_{ij} ≤ −a, for every i.
- Δ(y) and s_{ρ′/κ′}(y) carry no x.

So every monomial of hs_ρ Δ(x)Δ(y) Q_X^{-1} has some x exponent ≤ −1. The target has α_a = λ_a − a ≥ 0, because Durfee(λ) is exactly a. Hence the coefficient is zero, term by term and with no cancellation needed.

This is where both conditions matter:

- **Exact Durfee for λ.** If the alphabet were padded so that a > Durfee(λ), the target would have α_a < 0 and the statement would collapse. The input checks must enforce exact Durfee.
- **Uniform chamber.** If one factor were expanded the other way, it would raise x_i exponents and the bound would fail.

### (e) Two-sided product and the mirror chamber

Each term g · [hs_ρ(X) Δ_xΔ_y Q_X^{-1}] · [hs_σ(Z) Δ_uΔ_v Q_Z^{-1}] is a product of factors in disjoint variables inside R. Its target coefficient is therefore the product of the two separate coefficients. Combining (c) and (d) on each side, only (ρ, σ) = (λ, μ) survives, with weight g(λ, μ, ν). ∎

**Mirror chamber.** In the uniform y-dominant chamber, use instead hs_ρ = Σ_η s_{ρ/η}(x) s_{η′}(y) with η′ ⊆ ρ′. Since Durfee(ρ′) = Durfee(ρ) < a, we get η′_a < a and the same argument applies. This is not needed for the contract.

### Degenerate cases

- n = 0: output 1.
- Inconsistent input sizes: output 0 or reject. If the sizes were not checked, no ρ ⊢ n has λ's Frobenius coordinates, so the formula still returns 0, which is correct for g.

## 4. Consistency with Giambelli and the hook generating function (proved)

**Giambelli.** The identity s_ν = det(s_{(r_i+1, 1^{s_j})}) holds in Λ (Giambelli source, eq. (8)). ev_T is a ring homomorphism, so the identity holds for hs over T, with the Leibniz signs sgn(σ).

**Hook identity.** In Λ[[t, w]]: H(t)E(w) = 1 + (t + w) Σ_{r,s≥0} s_{(r+1, 1^s)} t^r w^s.

Checks in low degree:
- Degree 1: p₁(t + w) on both sides.
- Degree 2: h₂t² + h₁e₁tw + e₂w² = (t + w)(s₂t + s₁₁w), using h₁e₁ = s₂ + s₁₁.

In general, the coefficient of t^r w^s on the right is s_(r+1,1^{s−1}) + s_(r,1^s) = h_r e_s, the Pieri rule (with the convention s_(0,…) = 0).

**Specialization.** Since H(t) = exp(Σ p_r t^r / r):
- an even letter z contributes 1/(1 − zt);
- an odd letter z contributes exp(Σ (−1)^{r−1} z^r t^r / r) = 1 + zt.

So the contract's H_T and E_T = 1/H_T(−w) are correct.

**Expansion direction for 1/(t + w).** Work in R((t))((w)). Here t is a unit, and 1/(t + w) = t^{-1} Σ_{j≥0} (−w/t)^j. The power series HE − 1 lies in this ring, so the true quotient equals (HE − 1) times this expansion.

The term "−1" contributes only monomials t^{−1−j} w^j. Dropping it is therefore valid for coefficients with r ≥ 0.

Hooks with independent auxiliary variables t_j, w_j cannot leak into each other.

## 5. Finite controls (not proof)

**n = 1, a = b = 1.**
- hs_(1)(T) = (x + y)(u + v).
- The quotient by Q_X Q_Z is 1.
- [x⁰y⁰u⁰v⁰] = 1 = g((1),(1),(1)). ✓

**n = 2, ν = (1,1), a = b = 1.**
- e₂(T) = 2xyuv + x²uv + xyu² + xyv² + y²uv + x²v² + y²u².
- This equals hs₂(X) hs₁₁(Z) + hs₁₁(X) hs₂(Z) = xv(x + y)(u + v) + yu(x + y)(u + v).
- The quotient is exactly xv + yu.
- λ = (2) = (1|0) and μ = (11) = (0|1): [x¹y⁰u⁰v¹] = 1 = g. ✓
- λ = μ = (2): [x¹u¹] = 0 = g((2),(2),(11)). ✓

**Not yet exercised.** None of these controls tests the lower-Durfee annihilation, which needs a ≥ 2. One check of the mechanism: a = 2, ρ = (1). Here (x₁ + x₂)(x₁ − x₂) = x₁² − x₂², and the y-terms carry the factor (x₁ − x₂). Every monomial has an x exponent of 0 before the x^{−2} shift, so the coefficient is zero. ✓

A recommended falsification test is brute-force comparison against tabulated Kronecker coefficients for n ≤ 8 with a or b equal to 2.

## 6. Downstream requirements for the compiler (flagged, not certified)

The formula does not by itself give polynomial bit time. The compiler, audited separately, must discharge the following.

1. **One common ring.** All expansions must be the specific expansions inside R((t_·))((w_·)):
   - Q_X^{-1} and Q_Z^{-1} x- and u-dominant, exactly as in §2;
   - 1/(1 − zt) as power series in t;
   - 1/(t + w) t-dominant.

   Signed counting of index tuples is then the coefficient, *provided* every contributing tuple is shown to lie in the box (item 3). Finiteness must be proved per tuple, never through cancellation.

2. **"CHECK THIS": answered, no.** For ν = (r₁…r_c | s₁…s_c), each off-diagonal hook has size r_i + s_j + 1 ≤ r₁ + s₁ + 1 ≤ n. The fallback box 2n is unnecessary, though harmless.

   The contract's sentence "Hook j consumes auxiliary w-degree, so j ≤ s_j" overloads j, which is both the hook index and the 1/(t+w) index. Correct derivation:
   - The w-degree equation is (E odd-denominator occupations) + (E numerator choices) + j′ = s. Every term is nonnegative, so j′ ≤ s.
   - The t-degree equation is Σ(H even occupations) + (H numerator) − 1 − j′ = r. Hence the H occupations total at most r + 1 + j′ ≤ r + s + 1 ≤ n.

3. **Q-index bounds.** For each j, Σ_i k_{ij} ≤ β_j, because every other y source (Δ(y), letters yv and yu, numerators) has nonnegative degree. The same holds for v and δ.

   The x and u equations then have bounded right-hand sides, since all their other variables are already boxed. Each tuple in the box is a bounded integer point, so the count is finite.

4. **Signs.** Signs come from (−1)^{j′}, (−1)^{k_{ij}}, numerator choices, sgn(σ) and Vandermonde permutations.
   - Parity branching over a fixed number of indices is valid.
   - The substitution k = 2z + ε must keep the bound 0 ≤ k ≤ B as 0 ≤ 2z + ε ≤ B.

5. **Fixed-dimensional counting.** Barvinok–Pommersheim Thm 4.4 and Algorithm 5.2 count points of a rational polytope given by inequalities, in polynomial time for fixed dimension. Obligations:
   - The polytopes are lower-dimensional because of the equality constraints. Either justify the algorithm on such inputs, or first parametrize ℤ-solutions of Ak = b by Hermite or Smith normal form (polynomial time) and count a full-dimensional polytope in the lattice coordinates.
   - Handle the empty case.
   - Charge the cost of choosing l in Algorithm 5.2 and of the rational arithmetic in (5.2.1).

6. **Constants.** Let D be the number of geometric variables per term:

   D ≤ c(4ab + 1) + 2a² + 2b², with c ≤ 2ab.

   The number of terms is c! · 2^{4abc} · (a! b!)² times the parity branches. These are constants in (d, e), but astronomically large ones. The exponent of the polynomial in L depends on D, so the target running time is poly_{d,e}(L) with an unspecified, possibly huge, degree.

7. **Output and intermediate sizes.**
   - Counts are at most (Cn + C)^D.
   - The signed sum has O_{d,e}(log n) bits.
   - Right-hand sides are O(L) bits.
   - Matrices must be generated uniformly from (d, e); no advice.

## 7. Remaining proof obligations and falsifiers

**Obligations:**
- (O1) Rely on the factorization (Pragacz eq. 9 / Berele–Regev) in the translated sign convention of §3b. Only a = 1 was checked independently.
- (O2) Input validation must enforce exact Durfee a and b, with strictly decreasing nonnegative coordinates.
- (O3) Use the uniform chamber of §2 throughout the compiler.
- (O4) Items 1–5 of §6.

**Falsifiers that would refute the formula:**
- Any small (λ, μ, ν) with a or b ≥ 2 where the extracted coefficient differs from a tabulated g.
- Any instance where a mixed or inconsistent chamber in the implementation produces a nonzero contribution from Durfee < a. That would indicate the implementation, not the formula, is wrong.

**Not claimed:**
- No novelty or priority. Panova's §7.5 open question is not evidence of novelty.
- No quantum claim.
- No statement about growing Durfee size.
- No polynomial-time claim from the formula alone.
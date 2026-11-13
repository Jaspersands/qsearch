# Rosas Theorem 11 after tensor substitution: a direct binary-input compiler for g(λ,μ,ν)

## 0. Verdict and status labels

**Verdict.** I found no substitution, chamber, or asymptotic flaw. The proposed route works, with three corrections:

1. **Fewer cross factors.** The cross factors are only the boxes of ν inside [m]×[m], not all m² pairs.
2. **The signs simplify.** With V = −O, every letter in the numerator becomes a positive monomial. The only sign-carrying geometric indices come from Q_X and Q_Z.
3. **Finiteness needs the weight argument.** The contract's per-variable monotonicity argument (Q_X is the only thing that increases y) is false in this chamber, because Δ(O) ratios such as xv/(yu) lower y. Finiteness must come from a single weight bound. Section 5 gives that bound, and it gives an explicit O_ab(n) box.

Result: a deterministic algorithm with poly_{d,e}(L) bit cost, no auxiliary hook variables, and counting dimension at most D = m(m−1)+a²+b² with m = 2ab. Its constants are galactic for d,e ≥ 2.

**Labels used below.**
- [IMPORT]: standard identities taken from sources.
- [CONTRACT]: facts the contract marks as already checked.
- [PROVED]: deductions made in this report.
- [CHECK]: finite hand checks done here.
- [ASSUME]: source assumptions I cannot verify from the excerpts.
- [PRIORITY-UNVERIFIED]: claims about prior work I cannot settle.

## 1. Substitution and sign conventions

**Plethystic convention [IMPORT/CHECK].** Rosas writes s_λ[X−Y] with p_r[X−Y] = p_r(X) − p_r(Y). I checked this against Theorem 11 with one letter on each side:
- s_(2)[x−y] = h₂ − h₁e₁ = x(x−y). Theorem 11 gives (x−y)·x, since y₂ = 0.
- s_(1,1)[x−y] = −xy + y² = −y(x−y). Theorem 11 gives (x−y)(0−y).
- Rosas eq. (17), the hook (m₂,1^{e₁}), comes out as (x₁−x₂)·x₁^{m₂−1}·(−x₂)^{e₁}. This matches.

So box (i,j) means row i, column j. U_i sits on rows and V_j on columns.

**The tensor alphabet [PROVED].** The contract's hs convention is p_r(T) = p_r(E) + (−1)^{r−1} p_r(O). Expanding p_r(X)p_r(Z), the factor ((−1)^{r−1})² = 1 lands on the yv term. Take:
- U = E = {x_i u_k, y_j v_l},
- V = −O = {−x_i v_l, −y_j u_k}.

Then p_r(V) = (−1)^r p_r(O), so p_r[U−V] = p_r(T). Since s_ν ∈ Q[p₁,p₂,…], we get hs_ν(T) = s_ν[E − (−O)]. This agrees with Rosas's own use: (1−x)(1−y) gives U = {1,xy}, V = {x,y}.

**Sergeev after substitution [PROVED from IMPORT].** Theorem 11 is a polynomial identity in independent letters:

Δ(U)Δ(V)·s_ν[U−V] = Alt_U Alt_V(…).

It survives the ring map U ↦ E, V ↦ −O. Two sign facts:
- V^{δ_m} = (−1)^{m(m−1)/2} O^{δ_m},
- Δ(V) = ∏_{i<j}(O_j − O_i) = (−1)^{m(m−1)/2} Δ(O).

These cancel. Also U_i − V_j = E_i + O_j, and (−V_j) = O_j.

**Box grouping.** Let r_i = max(ν_i − m, 0) and c_j = max(ν'_j − m, 0). Let C = {(i,j) ∈ ν : i,j ≤ m}, so |C| ≤ m². Boxes split as follows:
- i ≤ m, j > m: factor E_i.
- i > m, j ≤ m: factor O_j.
- i > m, j > m: factor 0. Such a box exists iff Durfee(ν) > m. This is consistent with the contract's return-0 rule.

So, for Durfee(ν) = c ≤ m:

  F = hs_ν(T) = [Δ(E)Δ(O)]^{-1} Σ_{π,σ∈S_m} sgnπ·sgnσ · ∏_{i≤m} E_{π(i)}^{m−i+r_i} · ∏_{j≤m} O_{σ(j)}^{m−j+c_j} · ∏_{(i,j)∈C} (E_{π(i)} + O_{σ(j)}).   (★)

**Recovering the shape data from compact coordinates.** Write ν = (α^ν | β^ν).
- For i ≤ c: ν_i = α^ν_i + i.
- For c < i ≤ m: ν_i = #{j ≤ c : β^ν_j + j ≥ i}. This is at most c ≤ m, so r_i = 0 there.
- Columns are symmetric.

This takes O(m²) comparisons of O(log n)-bit integers. All exponents in (★) are binary integers of size at most n + m.

**Check: ν = (1) [CHECK].** The numerator is (E₁²−E₂²)(O₁−O₂) + (E₁−E₂)(O₁²−O₂²) = Δ(E)Δ(O)(E₁+E₂+O₁+O₂). So F = xu + yv + xv + yu = (x+y)(u+v) = hs₁(X)hs₁(Z). Correct.

**Check: ν = (2), letters generic [CHECK].** Alt_V gives (U₁−V₁)(U₁−V₂). The divided difference in U of t(t−V₁)(t−V₂) is h₂(U) − h₁(U)e₁(V) + e₂(V) = h₂[U−V]. Correct.

## 2. Nonvanishing of Δ(E)Δ(O), including a = b = 1 [PROVED]

**Distinctness.**
- E letters: x_i u_k and y_j v_l are squarefree degree-2 monomials. They are distinct for distinct index pairs, and x-u monomials never equal y-v monomials.
- O letters: x_i v_l and y_j u_k are likewise distinct.

So every factor E_p − E_q or O_p − O_q is a nonzero binomial. The product is nonzero in the domain Z[x,y,u,v], and division happens in its fraction field.

The relation E-letter·E-letter = O-letter·O-letter (for example (xu)(yv) = (xv)(yu)) is irrelevant. It only makes some hs_ν(T) vanish inside the hook, which (★) reproduces exactly.

**a = b = 1 explicitly.** m = 2.
- E = {xu, yv}, Δ(E) = xu − yv.
- O = {xv, yu}, Δ(O) = xv − yu.
- Both are nonzero.

## 3. Status of the single-coefficient extractor [CONTRACT, re-derived]

The extractor is

  g = [x^α y^β u^γ v^δ] F·Δ(x)Δ(y)Δ(u)Δ(v) / (Q_X Q_Z),

with 1/(x_i+y_j) expanded in y/x and 1/(u_k+v_l) in v/u. I re-derived the contract's argument and it holds, given two imports:

- **The coproduct expansion [CONTRACT].** F = Σ g·hs_ρ(X)hs_σ(Z), with hook vanishing.
- **The factorization [IMPORT].** For Durfee(ρ) = a, hs_ρ = Q_X s(x) s(y). This is Pragacz eq. (9) in plethystic form with B = −y, so R = ∏(x_i + y_j).

The coefficient factorizes over the (x,y) and (u,v) blocks.
- **Durfee(ρ) = a.** Q_X cancels exactly. The alternants a_{ρ_i−i}(x)·a_{ρ'_j−j}(y) meet the strictly decreasing target only at ρ = λ, with coefficient +1.
- **Durfee(ρ) < a.** Every κ ⊆ ρ with ℓ(κ) ≤ a has κ_a < a, so some x-exponent in Δ(x)s_κ is less than a. The factor Q_X^{-1} shifts every x-exponent by −a and otherwise only lowers x-exponents. So the target, which has nonnegative x-exponents, is never hit. Δ(y) does not involve x.

The rest of this report treats the extractor as given, as the task allows.

## 4. One pointed chamber containing both the extractor and (★) [PROVED]

**Weight.** Order the 2a+2b variables as x₁…x_a, u₁…u_b, y₁…y_a, v₁…v_b. Give them weights w = 2⁰, 2¹, …, 2^{2a+2b−1}, and let W = 2^{2a+2b−1}.
- Squarefree degree-2 monomials in two distinct variables have distinct binary weights. So w is injective on E ∪ O.
- w(y_j) > w(x_i) and w(v_l) > w(u_k) for all indices.

**The field.** Order Z^{2a+2b} by (w, then lex). This is a group order. Let H be the Malcev–Neumann field of series with well-ordered support. The map Q(x,y,u,v) → H is an injective field homomorphism.

**Expansion rules in H.**
- **Q factors:** 1/(x_i+y_j) = x_i^{-1} Σ_k (−1)^k (y_j/x_i)^k, with w(y_j/x_i) ≥ 1. This is exactly the contract's chamber.
- **Δ factors:** for each factor 1/(P−Q) of Δ(E) or Δ(O), let L be the lower-weight monomial and H′ the higher one. Then 1/(P−Q) = s·L^{-1} Σ_k (H′/L)^k, where s = +1 if L = P and s = −1 if L = Q. The ratio satisfies w(H′/L) ≥ 1. Every one of these coefficients is +1, so these indices are unsigned.

**Lemma (consistency).** Each series above is the unique inverse in H of its binomial. The extractor's series equals the H-image of the rational function F·Δ⁴/(Q_X Q_Z), since F·Δ⁴ is a polynomial and the image is a finite product. Expanding (★) term by term gives a finite sum of H-images of the same rational function. Two images of the same element agree coefficientwise. Hence the target coefficient of the compiled sum equals g.

No cancellation between infinite expansions is used. Each term's coefficient is a finite sum by the bound in Section 5, and there are finitely many terms.

**Chamber caveat.** In this chamber some Δ(O) ratios lower y (for a = b = 1, xv/(yu) has weight 9 − 6 = 3 > 0). The contract's "only Q_X raises y" finiteness argument therefore does not apply. Use the weight bound instead.

## 5. The explicit compiled term list and box [PROVED]

**Term data.** A term is specified by a fixed-size tuple:
- (π, σ) ∈ S_m²,
- a choice function S: C → {E, O},
- (τ₁, τ₂, τ₃, τ₄) ∈ S_a × S_a × S_b × S_b, from Δ(x) = det(x_i^{a−j}) and the analogous Vandermondes.

**Term sign.** sgnπ·sgnσ·∏sgnτ_r·∏_{Δ factors} s.

**Monomial.** M = N·V_τ·Pre, where:
- N = ∏_i E_{π(i)}^{m−i+r_i+e_i} · ∏_j O_{σ(j)}^{m−j+c_j+o_j}, with e_i = #{(i,j) ∈ C : S = E} and o_j = #{(i,j) ∈ C : S = O}.
- V_τ is the Vandermonde monomial.
- Pre = ∏_{Δ factors} L^{-1} · ∏_i x_i^{-a} · ∏_k u_k^{-b}.

The exponent vector of M lies in Z^{2a+2b} with entries of O(log n) bits.

**Generators.** The integer vectors g_t ∈ {−1,0,1}^{2a+2b}, for t = 1…D:
- m(m−1) Δ-ratios,
- a² ratios y_j/x_i,
- b² ratios v_l/u_k.

Let Q be the set of the a²+b² signed indices.

**Term coefficient.**

  c_term = Σ_{k ∈ N^D : M + Σ_t k_t g_t = τ} (−1)^{Σ_{t∈Q} k_t},

where τ = (α, β, γ, δ). The output is g = Σ_terms sign·c_term.

**Pointedness and box.** Every g_t satisfies w(g_t) ≥ 1, so the cone they generate is pointed. Bounds:
- Upper: w(τ) ≤ W(|α|+|β|+|γ|+|δ|) ≤ 2Wn.
- Lower: N and V_τ have nonnegative exponents, so w(M) ≥ w(Pre) ≥ −W(2m(m−1)+a²+b²).

Applying w to the defining equation gives

  Σ_t k_t ≤ w(τ) − w(M) ≤ W(2n + 2m(m−1) + a² + b²) ≤ C_ab(n+1).

If w(τ) − w(M) < 0, then c_term = 0. This is the explicit O_ab(n) box the contract asked for. Adding the box inequalities is harmless, since the equations already imply them.

**Numerator degrees.** Every numerator exponent is at most n + m + |C| + O(a+b), so O_ab(n). Prefactor exponents are O_ab(1).

## 6. Counting procedure and cost [PROVED, modulo ASSUME on Barvinok scope]

**Steps for each term.**

1. **Parity split.** For t ∈ Q, write k_t = 2z_t + ε_t with ε ∈ {0,1}^{a²+b²}. Each branch carries sign (−1)^{Σε}, giving 2^{a²+b²} branches.
2. **Integer solution space.** Solve the affine system A k = b′ over Z. A has 2a+2b rows and D columns with entries 0 or ±1 (doubled on the Q columns after the split). b′ has O(log n) bits. Use Hermite or Smith normal form of the fixed matrix A; this is constant work plus O(log n)-bit arithmetic on b′.
   - If there is no integer solution, the branch contributes 0.
   - Otherwise k = k₀ + N y, with y ∈ Z^{D′} and D′ ≤ D.
3. **Count.** P = {y : k₀ + N y ≥ 0, Σ k ≤ C_ab(n+1)}. This is a rational polytope in fixed dimension D′ with O(D) inequalities and O(log n)-bit right-hand sides. It may be empty. Count |P ∩ Z^{D′}| with Barvinok–Pommersheim Theorem 4.4 followed by Algorithm 5.2. Formula (5.2.1) is evaluated in exact rational arithmetic.

**Lower-dimensional P [ASSUME].** The excerpted Theorem 4.4 is stated for any rational polyhedron given by inequalities, with no full-dimensionality hypothesis. If one prefers full-dimensional input, detect implicit equalities by a fixed number of linear programs and re-parametrize. This is standard and polynomial in fixed dimension, but it is not shown in the excerpt.

**Term count.** The total number of counting calls is

  T_ab = m!² · 2^{|C|} · a!² · b!² · 2^{a²+b²}.

This depends only on a ≤ d and b ≤ e. All matrices are generated uniformly from (a, b, ν ∩ [m]²), with no advice.

**Cost.**
- Each call takes poly_D(log n) time.
- log n ≤ L + O(log a), since some Frobenius coordinate is at least (n−a)/(2a).
- Each count is at most (C_ab(n+1)+1)^D, so O_ab(log n) bits. The signed sum has the same bit size.
- Total cost: poly_{d,e}(L), plus O(L) for input validation:
  - sizes: 2n = Σ(2α_i + 1)-style sums must agree across λ, μ, ν;
  - Frobenius coordinates must be strictly decreasing;
  - output 1 if n = 0, output 0 if Durfee(ν) > 2ab.

**Honest scale.**
- a = b = 1: D = 4 and T = 4·2^{|C|}·4 ≤ 2^{8}. Practical.
- a = b = 2: D = 64 and T ≈ (8!)²·2^{64}·2^{8}·(2!)⁴. Polynomial, but useless in practice.

Barvinok's degree in L grows with D. That growth is the true dependence on d and e.

**Comparison with the Giambelli compiler.** That route needed c! hook determinants plus auxiliary t and w variables. This route needs neither, and it has no off-diagonal auxiliary-cell issue.

## 7. Source scope and priority

**Standard imports.**
- **Coproduct method.** The comultiplication expansion (Rosas eq. 2) and Rosas's use of Theorem 11 to compute Kronecker coefficients for hooks and two-row shapes. Rosas specializes U = {1, xy}, V = {x, y}. The mechanism (Kronecker via the super-Schur of a product alphabet plus Sergeev) is not new.
- **Rosas's a = b = 1 case.** This compiler at a = b = 1 is exactly the hook × hook setting, for which Rosas gives closed formulas, including Case 1, "(3,3) ∈ λ ⇒ 0". It is not a new case.
- **Hook vanishing and independence.** Pragacz (6), Theorem 3, and (9). Sergeev's formula itself is cited by Rosas to [1] and to Macdonald I.3. No proof is in the excerpt.

**New composition (this report).**
- General (a|a) ⊗ (b|b) substitution with V = −O.
- The explicit form (★).
- The single weight-pointed Hahn chamber shared with the extractor, and the uniform O_ab(n) box.
- The parity-split fixed-dimensional counting.

**[PRIORITY-UNVERIFIED].**
- Panova (arXiv 2502.20253v2, §7.5) writes that even for ν a hook with fixed Durfee sizes "it is not clear how to efficiently compute" g. That reflects the author's statement, not proof that no algorithm exists. It does not establish that no one has published this composition.
- CDW12 and PP17 (fixed lengths, binary input) are cited only through Panova's sentence. Their methods are not characterized here.
- No claim of novelty or priority. Because §7.5 frames even the unary hook case as open, independent finite controls (Section 8) should precede any public claim.

## 8. Proof obligations and falsifiers

**Obligations.**

| # | Obligation | Status |
|---|---|---|
| O1 | Sergeev's formula exactly as in Rosas Thm 11 for every λ in the (m,m)-hook, with the convention U_i = 0 for i > m and V_j = 0 for j > m. | Checked here on (1), (2), (1,1) and Rosas (17). General proof imported. |
| O2 | hs_ν(T) = s_ν[E − (−O)]. | Proved above via power sums. |
| O3 | Extractor (Section 3). | Contract fact; argument re-derived here. Relies on the Berele–Regev/Pragacz factorization in hs sign convention. |
| O4 | Field-embedding consistency (Section 4) and injectivity of the weight on E ∪ O. | Proved. |
| O5 | Box bound (Section 5). | Proved via w(g_t) ≥ 1. |
| O6 | Barvinok applicability to possibly empty or lower-dimensional P; exact arithmetic in (5.2.1). | ASSUME, plus standard fix. |
| O7 | Sign bookkeeping: s per Δ factor, (−1)^k only on Q indices, alternant and Vandermonde signs. | Must be implemented exactly as listed. |

**Falsifiers to run (I ran none of these).**

- **F1. Rational identity.** For n ≤ 12 and a, b ≤ 2, evaluate (★) at random integer points with Δ(E)Δ(O) ≠ 0 and compare with hs_ν(T), computed independently. Include a case with Durfee(ν) > 2ab, which must give 0. This tests O1 and O2 independently of any chamber.
- **F2. End-to-end small cases.** For all (λ, μ, ν) with n ≤ 10 and Durfee ≤ 2, compare the compiled Σ sign·c_term with character-table Kronecker coefficients. Any single mismatch refutes the compiler.
- **F3. Binary regime, a = b = 1.** For n ~ 2^{40}, compare with Rosas's hook × hook closed form (its full statement is beyond the excerpt; obtain it from the source). This tests signs and parity at huge exponents.
- **F4. Chamber test.** Recompute F2 with a different valid weight, for example a permuted variable order that still keeps y and v above x and u. The results must be identical.
- **F5. Pointedness sanity.** Assert w(g_t) ≥ 1 for every generated g_t, and that no term reports an unbounded polytope.

No hardness or speedup conclusion follows from any of the above. This is a classical deterministic algorithm whose correctness reduces to O1–O7.
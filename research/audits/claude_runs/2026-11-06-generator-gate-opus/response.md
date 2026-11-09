# Verdict: **ACCEPT** for the exact conditional lemma

The lemma holds as stated, with non-blocking repairs. It assumes a supplied polynomial-length compact generator `a` of a principal `J`, a polynomial-bit HNF presentation, and the effective nonreal L(1,χ) bound.

I found no step whose runtime depends on a compact exponent's numerical size rather than its bit length. The repairs below are missing explicit inequalities, not gaps in the argument.

## Cheapest falsification attempts (all fail)

**1. The excerpt's own counterexample, a = η^(2^B) in Z[ζ₅].**
- Here m = 2 and B is the single column Log(u₂) for u₂ = 1+ζ.
- |1+ζ| = 2cos(π/5) = φ and |1+ζ²| = 2cos(2π/5) = 1/φ, so the column is (log φ, −log φ).
- Its σ_min is √2·log φ, which is at least c₀ = log φ, consistent with the class-number bound hR ≥ log φ.
- If η = u₂, then y = 2^B exactly. The rounded z = 2^B is stored with B bits, and a' = 1.
- For general η, y = 2^B·y_η has O(B) bits. The rounding never manipulates 2^B numerically.

**2. Identity (10) checked directly.**
- Write b = Σ_{k=0}^{ℓ−1} c_k ζ^k with c_{ℓ−1} = 0.
- Then Σ_{a=1}^{ℓ−1} ζ^{−aj}σ_a(b) = ℓc_j − Σc_k.
- The j = ℓ−1 instance gives Σ_a ζ^{a}σ_a(b) = −Σc_k.
- Subtracting yields ℓc_j. So (10) is exact.
- Its bound is |b_j| ≤ (ℓ−1)·2M/ℓ < 2M.
- Editorial: "a" is used both as the generator and as the summation index. Rename one.

**3. Conditioning.**
- Index the m complex places by G = (Z/ℓ)^×/{±1}. Put f(t) = log|1−ζ^t| and M_{a,i} = f(ai).
- Then B = MΔ, where Δ has columns e_i − e₁.
- M is real symmetric and leaves the zero-sum subspace invariant, since Σ_a f(ai) does not depend on i.
- M = K·P, with K the group convolution and P the inversion permutation. So its singular values on that subspace are the nonprincipal |f̂(ψ)|.
- For even ψ ≠ 1, |Σ_{t∈(Z/ℓ)^×} ψ̄(t)log|1−ζ^t|| = √ℓ·|L(1,ψ)|. Halving over G gives √ℓ|L(1,ψ)|/2, as stated.
- **Nonreal ψ:** L(1,ψ) ≫ 1/log ℓ effectively, so √ℓ/(2·log ℓ)·const is bounded below by an absolute constant.
- **Real even quadratic character** (exists iff ℓ ≡ 1 mod 4): √ℓ·L/2 = hR ≥ log((1+√5)/2) ≈ 0.481. This is correct and uses no Siegel-type input.
- Δ^TΔ = I + J has eigenvalues 1 and m, so σ_min(Δ) ≥ 1.
- Therefore σ_min(B) ≥ c₀. The claim is correct.
- Entry bound: 2sin(π/ℓ) ≥ 4/ℓ, so |log|u_i(σ_a)|| ≤ log(ℓ/2) ≤ log ℓ.

**4. Normalisation.**
- With per-complex-place coordinates, Σ_{a=1}^m log|σ_a(a)| = ½·log N(J) = m·μ.
- So Log(a) − μ·1 is zero-sum and lies in span(B).
- For ℓ = 3 the balancing step is vacuous: log|σ₁(a)| = μ.

**5. Inequality (9).**
- Write Log(a) − μ1 = By, round to z with |y − z|_∞ ≤ 3/4, and set a' = a/Πu_i^{z_i}.
- Then |log|σ(a')| − μ| ≤ (3/4)(m−1)·log ℓ.
- Notably, (9) itself does **not** use σ_min(B). Conditioning is needed only to make the linear solve's precision and the bit length of y polynomial.

## Bit-cost accounting, step by step

### (a) Effective exponents
If the compact representation is a nested product/power DAG, each leaf λ_k has an effective multiplicity E_k = Σ over paths of products of edge exponents.
- **Missing inequality:** log₂|E_k| ≤ total exponent bits + log₂(number of paths).
- This is polynomial for a polynomial-size DAG.
- The excerpt's phrase "log(Σ|exponents|)" should read "log Σ_k |E_k|". Otherwise it is false for nested representations.

### (b) Leaf conjugates bounded away from 0
- **Missing explicit inequality:** suppose λ = x/d with x ∈ R∖{0} and |σ(x)| ≤ H for all σ.
- Then |σ_a(x)| ≥ |N(x)|/H^{ℓ−2} ≥ H^{−(ℓ−2)}.
- So log|σ_a(λ)| and arg σ_a(λ) are computable to absolute error ε in poly(ℓ, log H, log d, log 1/ε) bits.

### (c) Log(a) to absolute error ε
- Compute each leaf log to ε/(ℓ·Σ_k|E_k|).
- Cost: O(log Σ|E_k| + log 1/ε) extra bits. Polynomial.

### (d) Solve for y — **missing inequality**
- ‖y‖₂ ≤ ‖Log(a) − μ1‖₂/c₀ ≤ √m·(Σ_k|E_k|·h_k + |μ|)/c₀, where h_k bounds the leaf log heights.
- So log‖y‖ is polynomial.
- Use B̃ (entries to error δ_B) and right-hand side to error ε. The solution error is at most (√m/c₀)·(ε + δ_B·√m·‖y‖₂), up to a factor of 2 once √m·δ_B ≤ c₀/2.
- Choosing ε, δ_B ≤ c₀/(16·m·(1+‖y‖₂)) gives coordinate error ≤ 1/4.
- This needs O(log‖y‖ + log ℓ) bits. Polynomial.
- The excerpt asserts the precision is fine but never states this bound. Add it.

### (e) The new compact generator
- a' has the original compact length plus (m−1) leaves u_i, with exponents z_i of polynomial bit length.
- No circular-unit/full-unit index or h⁺ enters, because any generator suffices. This is correctly separated from CDPR's prescribed-short-generator goal.

### (f) The bound M
- log M = log D₀ + |μ| + (3/4)(m−1)·log ℓ.
- |μ| = log N(J)/(ℓ−1), and N(J) (or N(D₀J)/D₀^{ℓ−1}) has polynomial bit size from the HNF.
- D₀ is the HNF denominator, with polynomial bits.
- So log M is polynomial, and each |b_j| < 2M has polynomial bits.
- M itself is exponential, which is harmless. This is the correct height-versus-bit-length distinction.

### (g) Evaluating σ_a(b) without cancellation blow-up
- Compute L_a = log D₀ + Σ_k E_k·log|σ_a(λ_k)| − Σ_i z_i·log|σ_a(u_i)|.
- Compute θ_a = Σ_k E_k·arg σ_a(λ_k) − Σ_i z_i·arg σ_a(u_i) mod 2π.
- Each arg needs precision δ/(Σ|E_k| + Σ|z_i|), i.e. O(log of exponent sizes) extra bits.
- Only exp(L_a) is ever formed, and L_a ≤ log M + o(1). No huge intermediate product is expanded.
- Error budget: |σ_a(b) − σ̃_a| ≤ M·(e^{δ}−1 + δ) ≤ 3Mδ.
- Summed in (10) with weights ≤ 2/ℓ over ℓ−1 terms, the error is at most 6Mδ.
- Taking δ ≤ 1/(64M) gives error < 1/8, which needs log M + O(1) bits.

### (h) Rounding the coefficients
- b ∈ D₀J ⊆ R, so the b_j are integers. Error < 1/8 means rounding is exact.
- Output: a' = Σ(b_j/D₀)ζ^j. This is rational with polynomial bits and exactly a generator of J.

### (i) Final certificate
- Form the multiplication matrix of b (polynomial bits), take its HNF, and compare with D₀J.
- The analysis above already guarantees success. The check is a sound certificate rather than a probabilistic patch.
- The excerpt's "capped retries" belong to the upstream S-unit stage, which is out of scope.

## Specific repairs (non-blocking)

1. State the leaf lower bound in (b).
2. State the ‖y‖ bound and solve precision in (d).
3. Replace "log(Σ|exponents|)" by the effective-multiplicity bound in (a).
4. Rename the clashing symbols: the constant c₀ versus the "compact c₀" output, and the generator a versus the index a in (10).
5. Note that "circulant" should read "group-Hankel/symmetric with singular values |f̂(ψ)|". The conclusion is unchanged.
6. Optional robustness note: the L(1,χ) assumption is avoidable.
   - Delete one row of B to get a square B'. Then |det B'| = h⁺R⁺, and σ_min(B) ≥ |det B'| / ((m−1)·log ℓ)^{m−2}.
   - h⁺R⁺ ≥ R⁺ is bounded below by an absolute constant. I recall Friedman's regulator lower bound but cannot verify the exact constant here.
   - This gives log(1/σ_min) = O(ℓ·log log ℓ), which is still polynomial. The polynomial-bit claim needs only that log(1/σ_min) is polynomial, not that σ_min ≥ c₀.

## Scope caveats (not evaluated)

- How the compact generator a is found: the support factorisation via D₀ and N(D₀J), and the S-unit theorem.
- The map back to U.
- Any factorial-level conclusion. Nothing here establishes a full algorithm, a speedup, or a hardness statement.
- The lemma's status is conditional on a valid compact a and on exact polynomial-bit ideal arithmetic, as granted.
# Review: classical sampler for the Jack3 → Schur work law on unrestricted λ

## Bottom line

- **No polynomial classical sampler for unrestricted λ is obtained.** I do not claim hardness, a speedup, or novelty.
- **Positive but scoped result (proved modulo standard Jack facts).** The work law can be computed exactly in Q(√3) in time D^{O(m)}, where m = min(ℓ(λ), λ₁). This covers rows and columns (m = 1) and, for example, λ = (2,1). It does **not** cover growing Durfee rank d, since m ≥ d.
- **Falsifier F1 (rigorous, single instance).** For λ = (2,1), the work law cannot be any positive mixture of z-measures. It also cannot be any positive mixture of Schur-positive symmetric Schur-measure slices. Any construction of that kind claimed for all λ is dead.
- **Falsifier F2 (rigorous on the growing-Durfee family λ = (dᵈ)).** Consider any *exact* representation of f_λ as a sum of K vertex-coherent states. This class includes Cauchy-type projections, super-Cauchy, and exact quadrature of any integral in which p enters only through exp(Σ aₖ pₖ/k). Such a representation needs K ≥ binom(2d,d)/(d²+1) = exp(Ω(√D)).
- **What remains open** is stated precisely in section 5.

## 1. Baseline reproduced (not new)

**Row case.** The Jack Cauchy identity is
Σ_λ J_λ(x)J_λ(y)/j_λ = exp(Σ_k p_k(x)p_k(y)/(αk)),
with j_λ = ∏_s (α a + l + 1)(α a + l + α).

After the substitution p → √3 p, this becomes:

**(★)** Σ_μ f_μ(p) J_μ(y)/√j_μ = exp(z Σ_k p_k p_k(y)/k), with z = 1/√3.

With one variable y, only rows survive, so f_(n) ∝ Σ_ν s_ν(ρ_z) s_ν. Here s_ν(ρ_z) = ∏_b (z+c(b))/h(b). The normalization is Σ s_ν(ρ_z)² = (z²)_n/n!. This gives exactly M_{z,z}(ν) from BO Eq. 1.1 with t = 1/3.

**Column case.** Use ω_α J^{(α)}_λ = α^{|λ|} J^{(1/α)}_{λ'}, and J_(1ⁿ) = n! e_n. This gives the transpose of z = √3, with the energy flipped.

**Sampler.** Grow the shape with up-transition (z+c)²/(z²+n) · dim(ν+□)/((n+1)dim ν).
- These probabilities normalize because the Plancherel transition moments are 1, 0, n.
- Rounding each step to b = O(log(D/η)) bits gives TV ≤ η.
- The cost is poly(D, log 1/η).

**Sanity checks.**
- D = 2, row: the law is ((2+√3)/4, (2−√3)/4), which matches M_{1/√3, 1/√3}.

## 2. Exact algorithm for bounded m = min(ℓ(λ), λ₁)

**Proposition A.** Take ℓ(λ) ≤ m and m variables y. Restricted to m variables, the Jacks J_μ with ℓ(μ) ≤ m are linearly independent, and those with ℓ(μ) > m vanish.

Write J_μ(y) = Σ_κ A_{μκ} m_κ(y). The matrix A is triangular in dominance order and square on Par_m(D).

Define R_κ := ∏_i r_{κ_i}, where r_n = [uⁿ] exp(z Σ p_k u^k/k) is the row state. Matching the coefficient of the monomial y^κ in (★) gives

f_λ = √j_λ Σ_{κ ≥ λ} b_κ R_κ, where A b = e_λ.

The vector b is supported on κ ≥ λ with ℓ(κ) ≤ m.

**Contraction step.**

P_λ(e) = j_λ Σ_{κ,κ'} b_κ b_κ' [q^e][x^{κ'} y^κ] W, where

W = Σ_{|ν|=D} s_ν(z·x) s_ν(z·y) q^{2C1
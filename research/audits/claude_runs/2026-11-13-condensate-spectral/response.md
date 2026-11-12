# qRSt classical spectral sampler for the condensate input μ = (1^D) at q = t³, t = D/(D+1)

## 0. Verdict

**What is established, modulo the source obligations in §8:**

- **Shape law.** The parent's identification is correct, including every D!, r₁ and h_λ factor.
- **Sampler.** The qRSt growth driven by a uniform permutation samples the exact spectral measure π_D(λ) = |⟨Ĵ_λ, ψ_D⟩|². It does so at the native dependent point with a deterministic BIT clock of O(D³(b + log D)²) to TV 2^{-b}. No enumeration of tableaux or permutations is needed.
- **Return estimators.** Additive-ε estimators of the return amplitude A(τ) and the return probability |A(τ)|² = P_{(1^D),τ}((1^D)) follow, with failure probability δ. The time τ enters only through exact integer reduction.
- **Stronger observable.** The same construction yields more than the parent claimed. It produces a sample path of the (q,t)-Plancherel growth chain. That gives additive estimators for every "monotone" correlator ⟨1^{D−k}| e^{−iT_kH} a₁ ⋯ a₁ e^{−iT₀H} |1^D⟩ (§6).

**What does not follow:**

- The full occupation sampler.
- The mode-1 count ⟨n₁⟩(T).

I reduce ⟨n₁⟩(T) exactly to a conditional-pair (bridge) primitive that the source does not supply (§7). No hardness is claimed.

---

## 1. Conventions and exact shape law

**Basis and inner product.**
- Hall form: ⟨p_ρ, p_σ⟩ = δ_{ρσ} z_ρ R_ρ.
- Q_λ = b_λ P_λ and ⟨P_λ, Q_μ⟩ = δ_{λμ}, so ⟨P_λ, P_λ⟩ = 1/b_λ = h_λ. This matches the contract's notation and Macdonald VI (4.11).
- Ĵ_λ = √(b_λ) P_λ. The normalized J_λ is ±Ĵ_λ.
- The input vector is ψ_D = p₁^D / √(D! r₁^D), since R_{(1^D)} = z_{(1^D)} r₁^D = D! r₁^D.
- At q = t³, r₁ = 1 + t + t².

**Squarefree coefficients (deduction).** Only p₁^D contains the monomial x₁⋯x_D, with coefficient D!. Theorem 3.3 restricted to standard fillings then gives:
- Σ_{T∈SYT(λ)} ψ_T = [x₁⋯x_D] P_λ = D! κ_λ, where κ_λ := [p₁^D] P_λ.
- Σ_T φ_T = [x₁⋯x_D] Q_λ = b_λ D! κ_λ, using (3.3).

**qRSt marginal (deduction from Theorem 4.25).** Start from the compatibility relation and sum over σ, using Σ_σ P̄(σ←P,Q) = 1:
- r₁^{−D} Σ_σ P(σ→P,Q) = ψ_P φ_Q.
- For uniform σ: Pr(P,Q) = r₁^D ψ_P φ_Q / D!.

Summing over P and Q of shape λ:

  Pr(λ) = (r₁^D / D!)(D! κ_λ)(b_λ D! κ_λ) = D! r₁^D b_λ κ_λ².

**Overlap check.**
- ⟨Ĵ_λ, p₁^D⟩ = √(b_λ) · κ_λ D! r₁^D, since ⟨P_λ, p₁^D⟩ = κ_λ · z_{(1^D)} R_{(1^D)}.
- Hence |⟨Ĵ_λ, ψ_D⟩|² = b_λ κ_λ² (D! r₁^D)² / (D! r₁^D) = D! r₁^D κ_λ² / h_λ.
- This is exactly the parent's expression.
- Σ_λ = 1 follows from orthonormality and completeness, which specialize because there are no poles (§2).

**Finite controls (falsification only).**
- D = 1: π((1)) = 1 · r₁ · r₁^{−1} = 1.
- D = 2, from the formula: κ₍₂₎ = (1+q)(1−t)/(2(1−qt)) and κ₍₁₁₎ = 1/2. This gives π₍₂₎ = (1+q)(1−t)/(2(1−qt)) and π₍₁₁₎ = (1−q)(1+t)/(2(1−qt)). They sum to 1.
- D = 2, from qRSt directly using Example 4.19 with h = v = 1:
  - σ = id: the last cell has r = 0, so Pr(2) = (1−t)/(1−qt).
  - σ = 21: the last cell has r = 1, so Pr(2) = q(1−t)/(1−qt).
  - The average is (1+q)(1−t)/(2(1−qt)), which matches.

## 2. Positivity and absence of poles on the curve q = t³

The analysis splits into three parts.

**Tableau weights.**
- b_λ(c) = (1 − t^{3a+ℓ+1}) / (1 − t^{3a+ℓ+3}) lies in (0,1).
- So ψ_T, φ_T, κ_λ and b_λ are all strictly positive.
- Consequently π_D has full support on all p(D) shapes. This contrasts with μ = (D).

**Local probabilities.**
- Every factor of the form 1 − q^i t^j in Proposition 4.17 / (4.11) has i, j ≥ 0 and i + j > 0 (Remark 4.18(1)).
- On the curve such a factor becomes 1 − t^{3i+j}, which lies in [1/(D+1), 1).
- The τ-monomial exponents are nonnegative.
- Therefore p_{r,s} > 0 strictly, for all d + 1 outcomes.

**Direct check in the compact form (4.14).** Write a_i = t^{3x_i+y_i} and b_i = t^{3x_{i−1}+y_i}. Since x and y are strictly increasing, the paired exponent differences always have the same sign:
- a_s − a_i: the pair is (x_s − x_i, y_s − y_i), same sign.
- a_s − b_i: for i ≤ s the pair is (≥1, ≥0); for i > s it is (≤0, ≤−1).
- b_r = q^{x_{r−1}+1} t^{y_r−1} against a_i:
  - for i < r: (≥1, ≥ v_r − 1 ≥ 0);
  - for i ≥ r: (≤ 1 − h_r ≤ 0, ≤ −1).

Consequences:
- No "coincident content" difference t^A − t^A ever occurs.
- The Lagrange nodes stay distinct on the curve.
  - 3x_i + y_i is strictly increasing.
  - b_r − b_i has exponent difference 3(x_{r−1} − x_{i−1}) + 2 + (y_r − y_i) > 0 for i < r.
  - For i > r it is ≥ 3h_r − 2 + 1 > 0.
  - The modified a_s = q^{x_s−1} t^{y_s+1} similarly differs from every other a_i.
- Hence Theorems 4.11, 4.14 and 4.25 specialize from Q(q,t) to the curve with no division by zero.
- The raw γ in Definition 4.13 could in principle contain 1 − t^{3A−B}. It is only safe through Proposition 4.17's rewriting γ = γ′ · monomial, and that proof is truncated in the extract. This is obligation O2.

## 3. Sampler and deterministic BIT clock to TV 2^{-b}

**Algorithm S(D, b).**

1. **Precompute powers.**
   - Fixed-point table of t^m for 0 ≤ m ≤ M = 6D + 8, at W working bits.
   - Exact source t = D/(D+1).
2. **Draw the permutation.**
   - Use Fisher–Yates. Draw j ∈ {1..i} as 1 + ⌊U·i/2^{B′}⌋ with U a uniform B′-bit integer.
   - Per-draw TV ≤ i/2^{B′}; total ≤ D²/2^{B′}.
3. **Run the growth.**
   - Process the D × D grid row by row (D² local cells), holding one row of D + 1 shapes.
   - For a cell with NW µ, NE ρ, SW λ:
     - λ ≠ ρ: set ν = λ ∪ ρ (type II).
     - µ = λ = ρ with no entry: set ν = µ (type I).
     - µ = λ = ρ with entry: type III with r = 0.
     - λ = ρ ⋗ µ: type III with r equal to the index of the corner λ/µ.
   - For type III:
     - Compute the parameters (h, v) of λ in O(D) word operations.
     - Compute p_{r,s} for s = 0..d, with d ≤ √(2D), as t^{E₀} ∏_{k≤4d+2} (1 − t^{m_k})^{±1}, with E₀ ≥ 0 and m_k ≤ M.
     - Sample by inversion with B random bits. Cumulative sums are rounded down and made monotone; the last outcome takes the remainder.
4. **Output.** Return the shape at (D, D). Optionally return the entire south-boundary chain λ⁰ ⊂ ⋯ ⊂ λ^D.

**Local error.**
- Relative error of each 1 − t^m: at most (D+1) · 2 log₂M · 2^{−W}, using 1 − t^m ≥ 1/(D+1).
- Each p has at most 4d + 3 factors, so its absolute error is ε_a ≤ 8(d+1)(D+1) log₂M · 2^{−W}.
- Inversion with monotone cumulatives gives local TV ≤ 2(d+1)²(ε_a + 2^{−B}).
- This bound is uniform over input states.

**Global error.**
- Couple the exact and approximate processes cell by cell.
- TV_out ≤ D²/2^{B′} + D² · 2(d+1)² (ε_a + 2^{−B}).

**Parameter choice.**
- B′ = b + 2⌈log₂D⌉ + 2.
- B = b + 2⌈log₂D⌉ + 2⌈log₂(d+2)⌉ + 5.
- W = B + ⌈log₂(16(d+1)(D+1) log₂M)⌉.
- Then TV ≤ 2^{−b}, and W = b + O(log D).

**Deterministic cost.**
- D² cells, each costing O(D) word operations plus at most (d+1)(4d+3) ≤ 9D + O(√D) fixed-point multiplications on W-bit numbers.
- Total ≤ c₀ D³ W² bit operations, i.e. O(D³(b + log D)²).
- Random bits: O(D² (b + log D)).
- Memory: O(D² log D).
- An exact-rational Las Vegas variant also runs in polynomial expected time, using numbers of O(D^{3/2} log D) bits. It is not needed.

## 4. Exact phase reduction

E_λ = Σ_i (q^{−λ_i} − 1) t^{i−1}.

**Exact integer numerator.**
- Put Δ = D^{3D}(D+1)^D. Then N_λ = Δ·E_λ is an integer:

  N_λ = Σ_i [(D+1)^{3λ_i} − D^{3λ_i}] · D^{i−1} · D^{3D−3λ_i} · (D+1)^{D−i+1}

- N_λ has O(D log D) bits.

**Reduction and evaluation.**
- φ_λ = (a·N_λ mod cΔ)/(cΔ) ∈ [0, 1) is computed exactly. Its cost is O(D · M(D log D) + M(L + D log D)).
- Only then is e^{−2πiφ} evaluated to W₂ bits.
- |τ| enters only through L. Degeneracies of E are irrelevant, because A depends only on the spectral measure.

## 5. Estimators

**Return amplitude A(τ) = Σ_λ π(λ) e^{−2πiτE_λ}.**

This equals ⟨ψ_D| e^{−iTH} |ψ_D⟩, given the contract's admitted eigen-relation.

- **Bias budget.**
  - Run S with b_s = ⌈log₂(16/ε)⌉, so the sampling bias is ≤ 2·TV ≤ ε/8.
  - Evaluate phases with W₂ = ⌈log₂(8/ε)⌉ + 4 bits, so the rounding bias is ≤ ε/8 and |ζ̃| ≤ 1 + ε/8.
- **Sample count.** Average n = ⌈9 ε^{−2} ln(4/δ)⌉ independent ζ̃. Apply Hoeffding separately to the real and imaginary parts, each with range ≤ 2.25 and deviation ≤ (3/4)ε/√2.
- **Guarantee.** |Â − A| ≤ ε with probability ≥ 1 − δ. The variance is bounded by 1 + o(1).

**Return probability |A|² = P_{(1^D),τ}((1^D)).**
- Run the amplitude estimator at ε/3 and output clip(|Â|², 0, 1).
- The error is ≤ (ε/3)(2 + ε/3) < ε, with n = ⌈81 ε^{−2} ln(4/δ)⌉.
- An unbiased alternative is the pair estimator Re ζ₁ζ̄₂. Its bias is ≤ 4·TV.

**Total cost.** O(ε^{−2} log(1/δ) · [D³ log²(D/ε) + D · M(D log D) + M(L + D log D)]).

The guarantee is additive only. Nothing is claimed about relative accuracy when |A|² ≪ ε.

## 6. What the construction gives beyond the parent claim

**Empty rows and columns copy.** In an empty row the SW vertex equals the NW vertex. No type-III cell with r > 0 can arise, so every shape is copied from the row above. Consequences:
- The south-boundary shape at (D, k) is distributed as π_k.
- The chain is Markov, because P(Q) = r₁^D κ_ν φ_Q telescopes into

  ∏_k T(λ^{k−1} → λ^k), with T(λ→ν) = r₁ φ_{ν/λ} κ_ν / κ_λ.

**Pieri check.** I use P_μ g₁ = Σ φ_{ν/μ} P_ν, i.e. Macdonald VI (6.24). I checked it at μ = (1) against the source φ definition: the coefficients are (1−t)/(1−q) and (1−t²)/(1−qt). This identity is obligation O4.

**Monotone correlators (deduction).** Let a₁ = p₁^⊥/√r₁ be the normalized annihilator, with p₁^⊥ = r₁ ∂_{p₁}. Then:

  G(T₀, …, T_k) := ⟨1^{D−k}| e^{−iT_kH} a₁ ⋯ a₁ e^{−iT₀H} |1^D⟩ = √((D)_k) · E_path[ ∏_{j=0}^{k} e^{−iT_j E_{λ^{D−j}}} ].

Proof by induction:
- a₁ Ĵ_ν = √r₁ Σ_λ ψ_{ν/λ} √(b_ν/b_λ) Ĵ_λ.
- Use b_ν ψ_{ν/λ} = b_λ φ_{ν/λ}.
- Use c^{(m)}_λ = √(b_λ m! r₁^m) κ_λ.
- Apply the Markov property of the up-chain.

Checks:
- D = 2, k = 1 reproduces √2 · A-type sums correctly.
- At T = 0 the formula gives √((D)_k).

These are k-boson-removal amplitudes from the condensate. Each has additive estimators at the cost of §5, with k + 1 phases per path.

## 7. Full occupation output: not obtained

**(a) Signed coefficients.** The output amplitude is

  a_ρ(T) = √(R_ρ/R_{(1^D)}) · E_π[ (X_{λρ}/κ_λ) e^{−iTE_λ} ], with X_{λρ} = [p_ρ] P_λ.

- For ρ ≠ (1^D), X_{λρ} = Σ_α [m_α]P_λ · [p_ρ]m_α.
- The factors [p_ρ]m_α are signed, so no positive path representation is supplied.
- The qRSt construction encodes only the p₁ (squarefree) part of Cauchy; see (1.3) and (1.5).

**(b) Mode-1 count.** Using n₁ = p₁ p₁^⊥ / r₁ and the §6 calculus:

  ⟨n₁⟩(T) = D · E_{λ∼π_{D−1}} | E[e^{−iTE_ν} | λ] |², with ν ∼ T(λ, ·).

- Checks: D = 1 gives 1; D = 2 gives 2|A|²; the expression is ≥ D|A|² by Jensen.
- This is a down–up, non-monotone quantity. qRSt supplies one ν per λ, not a conditionally independent pair.
- Re-running only the last column, given its hidden data G, gives the estimable bound

  D|A|² ≤ ⟨n₁⟩ ≤ D · E|E[e^{−iTE_ν} | G]|².

- The bound is not exact.
- Rejection to match λ succeeds with probability π_{D−1}(λ), which is typically tiny.
- Factorial moments E[(n₁)_k] reduce in the same way. Recovering marginals from them requires alternating binomial sums, so even this primitive would not give the m₁ law efficiently.

**Exact missing interfaces, with no no-go claimed:**

- **(M1) Bridge sampler.** Given λ ⊢ k, sample P ∈ SYT(λ) with probability ∝ ψ_P in poly time. Equivalently, provide the ratios κ_μ/κ_λ to 1/poly relative precision, which yields T_down(ν→λ) = ψ_{ν/λ} κ_λ / (|ν| κ_ν). MCMC on ψ-weighted SYT is a candidate, but its mixing time is unproven. This gives ⟨n₁⟩(T).
- **(M2) Full sampler.** A classical oracle for the prefix marginals P_T(m₁, …, m_j), accurate to relative error 2^{−b}/D in poly(D, L, b). Alternatively, a positive or poly-variance path representation of ⟨p_ρ/√R_ρ | Ĵ_λ⟩ / ⟨ψ_D | Ĵ_λ⟩ with exact conditionals. Either is required to reach modes k ≥ 2, whose p_k-Pieri coefficients are signed.

## 8. Proof obligations and falsifiers

**Obligations:**
- **O1.** The full proof of Lemma 4.26 / Theorem 4.25. The extract is truncated at Case 2.
- **O2.** Equality of Definition 4.13 with Propositions 4.17 and 4.21. The β and γ details are omitted in the source, and the γ proof is cut off.
- **O3.** The §2.3 growth conventions: type dispatch by entry, and that P lies on the east boundary and Q on the south.
- **O4.** Macdonald VI (6.24). It is used only in §6 and §7.
- **O5.** The contract's eigen-relation H Ĵ_λ = E_λ Ĵ_λ. This is admitted, not re-verified.

**Falsifiers:**
- An exact D = 3 or D = 4 symbolic enumeration of qRSt shape frequencies over all σ that differs from D! r₁^D b_λ κ_λ².
- A local p_{r,s} ≤ 0 on the curve.
- A cell configuration not covered by the dispatch in §3.
- A D = 3 mismatch in the ⟨n₁⟩ or G identities.

## 9. Observables the candidate already loses to classical methods

All of the following are classically estimable to additive ε in poly(D, L, ε^{−1}, log δ^{−1}) on this input, modulo O1–O5:
- the return amplitude A(τ);
- the return probability, which is one output probability of the target law;
- energy statistics E_π[g(E)] and the collision quantity Σ_E π(E)², which equals the time-averaged return probability;
- all monotone a₁-correlators G.

Still unmatched:
- full occupation sampling at TV 2^{−b};
- mode counts, including n₁;
- relative-precision small probabilities.
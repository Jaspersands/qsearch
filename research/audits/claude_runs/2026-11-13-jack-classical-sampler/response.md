# Advisory report: strongest classical attack on fixed-λ Jack power-sum Born sampling at α = 3

## 0. Bottom line (changes the scientific action)

- **What is proved here.** An exact sequential sampler is proved for the same output. Sampling the Born distribution π_λ reduces exactly to computing Hall norms of iterated derivatives V_{-k_j}…V_{-k_1} J_λ. The reduction uses only adjointness and the Euler identity, both from the supplied material.

- **What is conditional.** The reduction becomes an algorithm through one hypothesis, H_P (Section 3): the p₁-Pieri rule with the Mickler–Moll transition weights τ. H_P is not in the supplied material and is not proved here. It is checked here only for ν = ∅, (1), (2).
  - H_P is a consequence of the candidate's own "crucial identity" A_d ψ_{λ,s} = J_{λ+s}.
  - So if the candidate's key lemma is proved, the classical attack below becomes unconditional.

- **Conditional on H_P,** there is an exact classical sampler of π_λ.
  - Its cost is poly(D) · N(λ)² arithmetic operations on poly(D)-bit rationals.
  - Here N(λ) = #{ν ⊆ λ} is the number of partitions contained in λ.
  - N(λ) ≤ (D+1)^{2h(λ)}, where h(λ) is the Durfee-square size of λ.

- **Strongest counterexample to any sampling-advantage claim (conditional on H_P).** Every family with h(λ) = O(1) has an exact polynomial classical sampler. This includes two-row, two-column, hook, and bounded-row/column λ. Families with h(λ) = polylog D have a quasi-polynomial sampler.
  - Any advantage claim must therefore be restricted to h(λ) = (log D)^{ω(1)}.
  - Even there, the worst case is exp(O(√D)).

- **Not achieved.** No polynomial sampler for unbounded Durfee size. No hardness is inferred from this.

## 1. Conventions

- Parameters: α = 3, ε1 = 3, ε2 = −1, ħ = −ε1ε2 = 3, ε = ε1 + ε2 = 2.
- Variables and norms: V_k = p_k, and j_λ (lowercase) = J_λ by (1.7).
- Contents: [(x,y)] = 3x − y, where x is the column index and y the row index, both 0-based.
- Operators: V_{-k} = 3k ∂/∂p_k.
- Notation: ‖·‖ is the Hall norm. I write N_λ := ‖J_λ‖² to keep the norm distinct from the polynomial j_λ.
- Target: π_λ(μ) = θ_μ² z_μ 3^{ℓ(μ)} / N_λ, where J_λ = Σ_μ θ_μ p_μ.

## 2. Unconditional derived facts

**F1 (adjointness and Euler; PROVED from supplied Lemma 3.4).**
- V_k^† = V_{-k}.
- Σ_k V_k V_{-k} = ħ · (degree operator), because V_k V_{-k} p_μ = ħ k m_k p_μ.
- Hence Σ_k ‖V_{-k} f‖² = 3 d ‖f‖² for homogeneous f of degree d.

**F2 (exact sequential sampler; PROVED).** Set f₀ = J_λ and d₀ = D.

1. At step j, pick k with probability q_j(k) = ‖V_{-k} f_j‖² / (3 d_j ‖f_j‖²). These sum to 1 by F1.
2. Set f_{j+1} = V_{-k} f_j and d_{j+1} = d_j − k.
3. Stop when d = 0. Output the multiset μ of chosen k.

Proof:
- The probability of an ordered sequence telescopes to ‖f_ℓ‖² / (3^ℓ Π_j d_j · N_λ).
- Only p_μ with μ equal to the chosen multiset survives the derivatives, and V_{-k}^m V_k^m = (3k)^m m!. So f_ℓ = θ_μ 3^ℓ z_μ.
- Sum over distinct orderings. The identity Σ_σ Π_j 1/(tail sum of x_σ) = Π_i 1/x_i holds; it follows by induction, choosing the first element. Dividing by Π_k m_k! gives Σ 1/Π d_j = 1/z_μ.
- Therefore P(μ) = θ_μ² 3^ℓ z_μ² / (z_μ N_λ) = π_λ(μ). ∎

Finite control, λ = (2): J_2 = p₁² + 3p₂ and N = 18 + 54 = 72.
- V_{-1}J_2 = 6p₁ has norm² 108.
- V_{-2}J_2 = 18 has norm² 324.
- So q(1) = 1/4 and q(2) = 3/4, which equals π((1,1)) = 1/4 and π((2)) = 3/4. ✓

**F3 (T₃ eigenvalue; derived from supplied (2.4)).** Expand log(u·T_ν(u)) per box. The u⁻² term is ħ, and the u⁻³ term is ħ(2[s] + ε). Hence:
- T₂ = ħ|ν|.
- e_ν := eigenvalue of T₃ = π₀L³ on J_ν = ħ(2 Σ_{t∈ν} [t] + ε|ν|).
- Checked directly against (2.1) on j_2.

**F4 (operator identities; PROVED from (2.1)).**
- [T₃, V₁] = 2ħ E₁ + εħ V₁, where E₁ := Σ_{b≥1} V_{b+1} V_{-b}.
- [E₁, V_k] = ħ k V_{k+1}.
- Hence V_k = ad_{E₁}^{k−1}(V₁) / (ħ^{k−1} (k−1)!).

**F5 (single-part coefficient; from supplied (4.8)).** The coefficient of z in Π_{t∈λ} (z + [t]) gives θ_{(D)} = Π_{t∈λ, t≠(0,0)} [t]. Therefore:
- π_λ((D)) = 3D (Π_{t≠0} [t])² / N_λ.
- This vanishes iff (1,3) ∈ λ, i.e. iff λ₄ ≥ 2. That is an exact zero of the target.

**F6 (doubly stochastic; PROVED).** Degree-D Jacks are p(D) orthogonal nonzero vectors in F_D, so they form a basis. Hence Σ_λ π_λ(μ) = 1 as well as Σ_μ π_λ(μ) = 1.

## 3. The single imported hypothesis

**H_P.** V₁ J_ν = Σ_{s∈A_ν} τ_ν^s J_{ν∪s}, with τ as in supplied (1.18).

Status:
- Classical in the literature, but not in the supplied material, so not promoted here. It is OPEN as a proof here.
- Verified at generic ε for ν = ∅, (1), (2); ν = (1,1) follows by the supplied ε1↔ε2 symmetry.
- Implied by the candidate identity: apply A_d to (1.17).

Positivity τ > 0 and Σ_s τ = 1 are derived from the supplied material via Prop. A.6 and π₀ of (1.17).

**Consequences under H_P (each derived here):**

- **(a) Content-weighted Pieri.** From F3 and F4, e_{ν+s} − e_ν = ħ(2[s] + ε). Hence E₁ J_ν = Σ_s [s] τ_ν^s J_{ν+s}.
  - Check: E₁ p₁ = 3p₂. ✓

- **(b) Jack Murnaghan–Nakayama analogue.** The coefficient of J_κ in V_k J_ρ is
  (ħ^{k−1}(k−1)!)⁻¹ Σ_{paths s₁…s_k from ρ to κ} (Π_j τ_j) · Σ_{m=1}^{k} (−1)^{m−1} C(k−1, m−1) Π_{j≠m} [s_j].
  - Check: this gives V₂·1 = p₂.
  - At α = 1 it reproduces rim-hook cancellation.
  - At α = 3 it does not: in p₁p₂ the J_{21} coefficient is 16/5 times the J_3 coefficient. So there is no rim-hook sparsity.

- **(c) Norms and Plancherel.** p₁^D = Σ_λ T_λ J_λ, where T_λ = Σ_{paths} Π τ is computable by a DP over the down-set of λ. The coefficient of p₁^D in J_λ is 1 (normalization). Hence:
  - N_λ = D! 3^D / T_λ.
  - Check: N_2 = 72. ✓
  - Pl₃(λ) = T_λ = π_λ(1^D).

## 4. Algorithm and cost (conditional on H_P)

Work in the span of {J_ν : ν ⊆ λ}. This down-set is closed under the paths needed, since raising paths into λ pass only through ν ⊆ λ.

1. Build the V₁ and E₁ matrices restricted to the down-set. Each column has at most √(2D) + 1 entries.
2. Build V_k via V_{k+1} = (E₁V_k − V_k E₁)/(3k). This costs O(√D N²) operations in total.
3. Run F2 with V_{-k} expressed through V_k and the norms N_ν (unnormalized basis):
   - ⟨J_ρ, V_{-k} J_κ⟩ = [V_k]_{κρ} N_κ.
   - ‖Σ_ν c_ν J_ν‖² = Σ_ν c_ν² N_ν.
   - There are at most D steps, each costing O(N²). Total O(D N²).
4. All quantities are rationals with poly(D) bits. A crude bound is O(D^{2.5}) bits from lcm of content differences of size ≤ 4D; the constant is OPEN. Sampling is exact, or ε-close in total variation with O(D log(D/ε)) random bits.

**Size of N(λ).**
- Every ν ⊆ λ is determined by its first h rows and first h columns, so N(λ) ≤ (D+1)^{2h(λ)}.
- Also N(λ) ≤ C(λ₁ + ℓ(λ), ℓ(λ)) and N(λ) ≤ (D+1)p(D).
- If λ contains an h×h square, then N(λ) ≥ C(2h, h).
- For the staircase, N is a Catalan number, about e^{1.96√D}. Compare p(D) ≈ e^{2.565√D}.
- So the worst case is e^{c√D} with 1.96 ≤ c ≤ 2.565 + o(1). The maximizing constant is OPEN.

**Exact remaining bottleneck.** Representing f_j generically fills a whole level of the down-set. Equivalently, the algorithm needs poly(D) factorial-moment norms ‖Π_{k∈S} V_{-k} J_λ‖² along one sampled path, for |S| up to D.

## 5. Shape sampling versus fixed-λ sampling

- **One-box chain.** The chain with transition probabilities τ_ν^s is a valid Markov chain (derived) and samples a shape λ from Jack–Plancherel in poly(D).
- **Overlap with the target.** By F6 and H_P(c), its only overlap with the target is the single atom Pl₃(λ) = π_λ(1^D).
- **Fixed λ is a different object.** For fixed λ, the target varies over μ, and the needed amplitudes interfere along paths (formula (b)). No Markov growth chain for μ was found.

## 6. Attacks tried; none beat Section 4 in general (no hardness inferred)

- **Signed p-basis recurrence from T₃J = eJ.**
  - The diagonal term is εħ Σ μ_i². The join term comes from partitions with one more part, the cut term from partitions with one fewer.
  - The recurrence is not triangular, so it costs poly(p(D)).
- **Group or random-permutation formulas.** None is available at α = 3. The α = 1 (and α = 2, ½) formulas are not transferred.
- **Rejection from the Ewens(1/3) proposal** q ∝ 1/(z_μ 3^ℓ).
  - No polynomial bound on π/q was found. At μ = 1^D the ratio contains a D! 3^D / N_λ-type factor.
- **MCMC.** Each θ_μ costs a DP over the down-set, so there is no gain.
- **Tensor networks (MPS over occupations).** No bond-dimension bound was derived. OPEN.
- **Speculative, not used.** A skew vanishing rule at offset (1,3) pairs, generalizing F5.

## 7. Proof obligations and falsifiers

- **O1. Prove H_P, or source it with its content checked.**
  - Exact controls for all ν with |ν| ≤ 12: formula (b) and N_λ = D! 3^D / T_λ.
  - A single wrong coefficient falsifies Section 4 as stated.
- **O2. Exact π_λ comparison.** Compare F2 + DP against brute-force J_λ for all λ ⊢ D, D ≤ 14.
- **O3. Worst-case constant.** Determine max_{λ⊢D} N(λ).
- **Falsifier of the bottleneck.** A poly(D) algorithm for ‖Π_{k∈S} V_{-k} J_λ‖² at large h would give a complete polynomial sampler and remove any sampling advantage.

## 8. Recommended action

1. Prioritize proving H_P. It is weaker than the candidate's identity and is a prerequisite for both routes.
2. Then restrict any quantum claim to h(λ) = (log D)^{ω(1)}.
3. Require that the quantum route's total cost (overlaps, failure resets, precision) beat D^{O(1)} · N(λ)² on that specific family. Beating exp(Θ(√D)) on generic λ is not enough.
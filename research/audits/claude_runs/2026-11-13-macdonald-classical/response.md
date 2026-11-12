# Review: exact classical sampler for the fixed‑label Macdonald occupation law at q = t³, t = D/(D+1)

## Verdict

The status remains **OPEN**. I did not find a complete poly(D, b) classical sampler for unrestricted λ ⊢ D. Nothing below implies hardness.

The review does produce three useful results:

- **A new exact classical sampler.** Every shape with λ₁ ≥ D − s, or with ℓ(λ) ≥ D − s, can be sampled exactly in D^{O(s)}·poly time. This covers rows and columns and their bounded‑depth neighbours.
- **A falsification of the Jack‑approximation route.** The α = 3 Jack law does not approximate this law at inverse‑poly total variation (TV). Already for λ = (D), the TV stays bounded below by a constant.
- **A localized gap.** The derivative‑norm route reduces exactly to one family of numbers, the squared‑sum of power‑sum Pieri coefficients. These numbers are computable for small part sizes k and for k = D. They are not computable by any method I know for mid‑range k on balanced shapes.

Notation used throughout:

- R_μ = ∏ r_{μᵢ}, and H_λ = ⟨J_λ, J_λ⟩_{q,t}.
- The target law is P_λ(μ) = θ_{λμ}² z_μ R_μ / H_λ, where J_λ = Σ_μ θ_{λμ} p_μ.

---

## 1. Audit of the supplied baseline and sources

**Rows and columns. [Proved; baseline is correct]**

- *Row.* By the Cauchy identity, g_n and m_ν are dual bases. Hence g_n is orthogonal to span{m_ν : ν < (n)}, so J_(n) ∝ g_n = Σ p_μ/(z_μ R_μ). The occupation law is the weighted cycle measure with w_k = 1/r_k.
- *Column.* By triangularity, J_(1^n) ∝ e_n, which gives w_k = r_k.
- *Dynamic program.* The DP recursion n Z_n = Σ_k w_k Z_{n−k}, followed by size‑biased cycle selection, samples both laws exactly.
- *Closed forms (new, useful for checking).* Since 1/r_k = (1 − u)/(1 − u³) evaluated at u = t^k:
  - Z_n^row = [xⁿ] (tx; q)_∞ / (x; q)_∞ = (t; q)_n / (q; q)_n.
  - Z_n^col = (q; t)_n / (t; t)_n.
- *Bit lengths.* All rationals have O(D² log D) bits. Sampling to TV ≤ 2^{−b} costs poly(D, b).

**Diaconis–Ram (1007.4779), Eqs. 1.1–1.4.** π_{q,t} = Z / z_λ(q,t), which is the row law. The reciprocal‑parameter map works as described: each Hall weight picks up a common factor (t/q)^D and P_λ is unchanged. The source does **not** give squared‑eigenfunction laws for other λ. **Confirmed.**

**O'Connell–Pei (1212.6716), Theorem 2 and Eqs. 11–13.** These are t = 0 (q‑Whittaker) tableau and shape laws. They are irrelevant to the fixed‑λ occupation law at q = t³. **Confirmed.**

**Two caveats on the baseline.**

1. *Brute force is subexponential.* Expanding over p(D) = exp(O(√D)) partitions is subexponential. Any separation the candidate could claim is therefore at most subexponential in D.
2. *Superposition inputs need amplitudes.* The contract also allows superposition inputs Σ c_λ |λ⟩. That output law has cross terms Σ_λ c_λ Ĵ_λ(μ). A classical sampler for it needs signed amplitudes, not just the fixed‑label Born laws. The fixed‑label task is strictly weaker.

---

## 2. New exact deductions

### 2.1 ω‑duality maps the problem to t′ = q′³ [Proved]

- ω_{q,t} p_k = (−1)^{k−1} r_k p_k.
- ω_{q,t} J_λ(q,t) = J_{λ′}(t,q) (Macdonald, *Symmetric Functions and Hall Polynomials*, Ch. VI).
- ⟨ωf, ωg⟩_{t,q} = ⟨f, g⟩_{q,t}.

Hence P^{(q,t)}_λ(μ) = P^{(t,q)}_{λ′}(μ) exactly. The dual parameters (q′, t′) = (t, t³) satisfy t′ = q′³, with r′_k = 1/r_k. Rows and columns swap, and every result below transfers to conjugate shapes.

### 2.2 Finite‑colour (three‑alphabet) Schur representation [Proved; not a sampler]

Define ι(f) = f(X₁, t^{1/2}X₂, t X₃). Then

- ι(p_k) = p_k(X₁) + t^{k/2} p_k(X₂) + t^k p_k(X₃), and
- ⟨ι p_μ, ι p_ν⟩_{Hall⊗3} = δ_{μν} z_μ R_μ.

So ι is an isometry from the q,t‑inner product into the triple Hall space.

**Exact consequence.** Measure ι(Ĵ_λ) in the tensor power‑sum basis and take the union of the three sampled partitions. The result has exactly law P_λ. Conditionally on μ, the colours of the parts are independent, with probabilities (1, t^k, t^{2k}) / r_k.

**Why it is not a sampler.** The lift is lossless: the tensor law equals the target times an independent colouring. Expanding ι(J_λ) = Σ_{ν⊂κ⊂λ} P_{λ/κ}(X₁) P_{κ/ν}(t^{1/2}X₂) P_ν(tX₃) yields skew pieces that overlap in power‑sum support, so they interfere.

A sampler would need a decomposition into pieces that are both:

- separately samplable, and
- disjointly supported in the tensor power‑sum basis.

No such decomposition is known. Even a single Schur factor's Born law is the S_n character law χ²|C|/n!, whose classical complexity I do not assume.

The finite‑colour representation is therefore fully paid but buys nothing on its own. It does not kill the candidate.

### 2.3 Near‑row and near‑column shapes: exact sampler [Proof sketch with explicit obligations]

**Lemma (span).** Assume D ≥ 2s and 0 < q, t < 1. Then

span{P_κ : κ₁ ≥ D − s} = span{g_{D−j} P_ρ : ρ ⊢ j ≤ s}.

*Proof sketch.*

- By the Macdonald Pieri rule for g_m (horizontal strips), g_m P_ρ is a combination of P_κ with κ/ρ a horizontal strip of size m.
- At most ρ₁ boxes can land outside row 1, so κ₁ ≥ m.
- Equality κ₁ = m forces κ = (m, ρ), and its coefficient is a product of factors (1 − q^a t^b)^{±1}. These factors are nonzero, including at q = t³.
- Downward induction on m therefore gives a triangular, invertible system.

*Obligation:* check the ψ‑coefficient formula for absence of zeros or poles at q = t³.

**Amplitude structure.** Write J_λ = Σ_{j≤s} g_{D−j} h_j with h_j ∈ Λ_j. Since [p_α] g_m = 1/(z_α R_α),

θ_{λμ} z_μ R_μ = Φ_λ(m₁, …, m_s)
  = Σ_{β ⊆ μ, |β| ≤ s} c(β) R_β ∏_k k^{b_k} (m_k)_{b_k}.

Here (m)_b denotes the falling factorial, and c(β) collects the power‑sum coefficients of the h_j. So

**P_λ(μ) = Φ_λ(m_{≤s})² · π_row(μ) / E_row[Φ_λ²].**

In words: the law is the row weighted‑cycle law, tilted by a squared polynomial in the counts of parts of size at most s.

**Algorithm.**

1. Solve the triangular system of size Σ_{j≤s} p(j). This needs P_ρ power‑sum tables for |ρ| ≤ s, at cost exp(O(√s)).
2. Enumerate the ≤ (D+1)^s vectors (m₁, …, m_s). Weight each by Φ² · ∏_{k≤s} (w_k/k)^{m_k}/m_k! · Z^{(>s)}_{D−Σ k m_k}. Here Z^{(>s)} is a DP restricted to parts larger than s.
3. Sample a vector exactly, then complete the parts larger than s by restricted size‑biased DP.

**Cost.** D^{O(s)} · poly(D, b). All quantities are exact rationals with poly(D) bits, and no advice is required. By §2.1 the same holds for ℓ(λ) ≥ D − s. Signed amplitudes are available, so poly‑sparse superpositions over such labels are also covered.

**Consistency check (λ = (2,1), D = 3) [finite control].**

- Orthogonality to e₃ gives the coefficient of m₁₁₁ in P₂₁ as c = 6(r₁r₂ + r₃) / (r₁³ + 3r₁r₂ + 2r₃).
  - This gives c = 2 at q = t (Schur) and c = 6/5 at r ≡ 3 (Jack α = 3).
  - At t = 3/4: r₁ = 37/16, r₂ = 481/256, r₃ = 6553/4096, so c = 974/781.
- The linear‑in‑m₁ form Φ = c₀ + c₁ r₁ m₁ holds if and only if c satisfies exactly this orthogonality equation. The structure is confirmed.
- Exact Born law: P(111, 21, 3) = (72079928142, 27689426856, 36844131099) / 136613486097 ≈ (0.5276, 0.2027, 0.2697).
- The amplitudes have mixed signs: θ ∝ (487, 882, −1369) / 2343.

**Consequence for the candidate.** Any advantage must come from shapes with both λ₁ and ℓ(λ) well below D. Compared with brute force exp(O(√D)), this sampler is already better whenever s ≲ √D / log D.

### 2.4 Derivative‑norm recursion: an exact reduction [Proved]

Let ∂_k = ∂/∂p_k. In the q,t‑product, ∂_k† = p_k / (k r_k). For any ψ,

Σ_k k² r_k ‖∂_k ψ‖² = D ‖ψ‖².

A size‑biased part removal then satisfies:

- P(k) = k² r_k ‖∂_k ψ‖² / (D ‖ψ‖²) = k E_ψ[m_k] / D, and
- the remainder is distributed exactly as the Born law of ∂_k ψ.

Iterating, the exact sampler needs only the factorial moments

M_λ(a) = E_λ[∏_k (m_k)_{a_k}] = ⟨J_λ, p_κ ∂_κ J_λ⟩ / H_λ.

Precision requirement: relative error 2^{−(b + O(log D))} per step gives TV ≤ 2^{−b}. The reduction is circular in general, because the moments encode the law. It is useful only if the moments are computable.

**What is computable.** Write ∂_κ J_λ = Σ_ν ⟨J_λ, p_κ J_ν⟩ J_ν / (∏ k r_k · H_ν), with |λ/ν| = |κ| = K.

- *Small K.* Newton's identities express p_κ in the e‑basis with ≤ p(K) terms. Each e_j Pieri step has product coefficients, and there are at most D^{O(K)} intermediate shapes ν. So low‑order moments cost D^{O(K)} for every λ.
- *K = D, β = ∅.* The standard identity [p_D] J_λ = ((1 − t^D)/D) ∏_{(i,j)≠(1,1)} (t^{i−1} − q^{j−1}) applies. I checked it against λ = (2,1) above. Together with the product formula for H_λ, it gives P_λ((D)) in closed form.
  - **Exact q = t³ feature:** P_λ((D)) = 0 if and only if (4,2) ∈ λ, i.e. λ₄ ≥ 2. This reflects the coincident contents i − 1 = 3(j − 1).
- *Mid‑range K on balanced λ.* Both the number of intermediate ν and the dimension p(D − K) are exponential. **The route stalls here.**

### 2.5 Positive‑process and Diaconis–Ram spectral route [Deduction; no polynomial route]

P_λ(μ) = π_row(μ) f_λ(μ)², where f_λ is the L²(π)‑normalized eigenfunction of the Diaconis–Ram chain. Equivalently, it is the diagonal of the spectral projector E_λ(μ, μ).

Return probabilities satisfy M^s(μ, μ) = Σ_λ β_λ^s P_λ(μ). Inverting this would require:

- p(D) eigenvalue moments,
- a Vandermonde inversion with gaps that can be exponentially small, and
- a fixed μ, so it does not even give sampling.

As a separate fact, the Born matrix is unistochastic: Σ_λ P_λ(μ) = 1. I know of no positive Macdonald process whose marginal is the fixed‑λ law.

---

## 3. Jack α = 3 approximation versus the D‑dependent deformation

**Claim: the Jack α = 3 law does not approximate the deformed law, even for the row shape.** [Proof sketch; standard inputs]

For λ = (D), the Jack row law is Ewens(θ = 1/3). The density ratio is

P_def / P_Jack ∝ ∏_k (3 / r_k)^{m_k}.

With t^k = e^{−k/N + O(k/N²)}, write log(3/r_k) = f(k/N) where f(x) = log(3 / (1 + e^{−x} + e^{−2x})) = x + h(x), and h(x) = −x²/3 + O(x³).

- The linear part contributes e^{D/N}, a constant that cancels in normalization.
- The remaining factor exp(Σᵢ h(ℓᵢ/N)) is bounded, since |h(x)| ≤ C x² and Σ xᵢ² ≤ 1. It is continuous in the ranked normalized parts.

Ewens(1/3) ranked parts converge to Poisson–Dirichlet PD(1/3). Hence:

- P_def converges to PD(1/3) tilted by e^{H} / E[e^{H}], with H = Σ h(xᵢ), which is non‑constant.
- By lower semicontinuity of TV, liminf_D TV(P_def, P_Jack) ≥ ½ E_PD |e^{H}/E[e^{H}] − 1| > 0.

The deformation lives on parts of size Θ(N), where r_k ranges over roughly [1.50, 3].

**Finite certification is available.** The probabilities P(largest part > D/2) = Σ_{k>D/2} (w_k/k) Z_{D−k} / Z_D are exact under both laws:

- deformed: Z_m = (t; q)_m / (q; q)_m;
- Jack: Z_m = (1/3)_m / m!.

These give exact TV lower bounds for any D in poly time. Running this is a finite check, not the proof.

**Consequences.**

- No uniform inverse‑poly TV approximation by the Jack law exists.
- Convergence for fixed λ and agreement at small D are irrelevant to this question. For example, at λ = (2,1), D = 3, the TV is only about 0.026.
- The deformation itself is not the obstruction. The §2.3 sampler handles it exactly for near‑row shapes.

---

## 4. Decisive next equation

**(E\*)** For balanced λ ⊢ D (test family: squares (aᵃ) and staircases) and k ≍ D/2, decide whether

S_k(λ) = Σ_{ν ⊢ D−k} ⟨J_λ, p_k J_ν⟩²_{q,t} / H_ν = k r_k H_λ E_λ[m_k]

admits a poly(D)‑term expression, uniformly in λ. The two anchors are:

- small k, which is a Pieri product sum (§2.4);
- k = D, which is the hook‑vanishing product (§2.4).

**If (E\*) succeeds**, the next obligation is the iterated version with p_κ, |κ| = K, which feeds §2.4 at every stage.

**If (E\*) fails**, the derivative route is closed. That is still **not** evidence of hardness.

A finite exploratory check would compute S₂ and S_{⌊D/2⌋} exactly for D ≤ 30 by full expansion and test for low‑degree rational or product structure. This is a control, not a proof.

## 5. Falsifiers and obligations

- **§2.3:** confirm that the g‑Pieri coefficients have no zeros or poles at q = t³, and confirm the dimension count for D < 2s.
- **§2.4:** verify the power‑sum coefficient identity against Macdonald's book. It is checked here only at λ = (2,1).
- **§3:** make the convergence of ranked parts under the tilt rigorous, using standard logarithmic‑structure arguments.
- **What would kill the candidate:** (E\*) together with its iterates, or any representation, computable in poly(D, b), of Φ‑type amplitudes for balanced shapes.
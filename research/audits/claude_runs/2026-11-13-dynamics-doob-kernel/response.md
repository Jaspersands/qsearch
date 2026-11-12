# Doob transform of the Nazarov–Sklyanin Hamiltonian on power-sum occupations, and whether it yields a real-time sampler

## 0. Verdict

**Proved, for all 0<q,t<1, and in particular at q=t³:**

1. **Strictly positive matrix.** In the normalized occupation basis e_μ = p_μ/√R_μ, the Hamiltonian H is a strictly positive symmetric matrix. Section 1 gives its closed vertex expression.
2. **Perron vector.** The Perron vector is the row function. In power sums, g_D = Σ_μ p_μ/R_μ, so φ(μ) = (Z R_μ)^(-1/2). The Perron eigenvalue is λ0 = q^(-D) − 1, and Z = Σ_μ 1/R_μ ≤ 1. I prove H g_D = λ0 g_D directly from the vertex series, with no Macdonald input.
3. **The Doob kernel.** It is exactly
   K(μ→ν) = [p_ν](H p_μ)/(q^(-D) − 1).
   It is the transpose of H's matrix in the unnormalized p-basis. Combinatorially:
   - delete each part of size k independently with probability 1 − q^k, conditioned on deleting at least one part;
   - redistribute the deleted mass n as a random partition with cycle weights (1 − t^k).
4. **Cost of one update.** One update costs expected Õ(D²) bit operations exactly, or Õ(D(D log D + b)) worst case at TV ≤ 2^-b. Every single entry K(μ,ν) is exactly computable in poly(D) bit time.
5. **Real-time Born law in Doob form.** With θ = 2πτλ0 and M = e^(−iθK), the target satisfies
   P_{μ,τ}(ν) = M_{μν} · conj(M)_{νμ}.
   All stationary ratios cancel identically.

**Decision (scoped to this route).** The Doob chain does not give a real-time Born sampler, nor a bounded-variance estimator uniform in binary time.

- The natural complex-weight trajectory estimator is unbiased. On the explicit family μ = (D) with observable n_D, its variance is at least e^(2θ(1+κ_D)) − 1 ≥ e^(42π|τ|) − 1.
- At τ = P (the exact period), the evolution is the identity, yet the variance is still at least e^(42πP) − 1. The estimator is blind to the exact rational spectral structure.
- Constructively, it does give D^O(1)·ε^-2 additive estimation of any bounded occupation observable (e.g. k·n_k/D) when |τ| = O(log D). That is not the full TV-2^-b sampler.

None of this is evidence of hardness.

---

## 1. The vertex expression in occupations

**Conventions.** The Hall(q,t) form is source Eq. 1.15: ⟨p_λ,p_μ⟩ = δ z_λ ∏ r_{λ_i}, with r_k = (1−q^k)/(1−t^k). The source gives p_k^* = r_k p_k^⊥ = r_k·k∂/∂p_k.

**The two vertex series.**
- V(z) = Q(z) = exp(Σ (1−t^k)p_k z^k/k).
- V^*(w) = exp(Σ (1−q^k) w^k ∂/∂p_k) (source 1.16). This is the translation p_k ↦ p_k + (1−q^k)w^k.

**Action on power sums.** Write μ = 1^{m_1}2^{m_2}⋯.
- Removal: V_n^* p_μ = Σ_{β≤m, Σkβ_k=n} ∏_k C(m_k,β_k)(1−q^k)^{β_k} p_{μ−β}.
- Addition: V_n p_ρ = Σ_{Σkα_k=n} ∏_k ((1−t^k)/k)^{α_k}/α_k! · p_{ρ+α}.

**Matrix in the p-basis.** A pair (μ,ν) determines the common kept multiset ρ = μ−β = ν−α, with ρ ≤ m∧n′ componentwise (n′_k are ν's multiplicities) and ρ ≠ μ. Hence

a_{νμ} := [p_ν] H p_μ = (1−t)^(-1) Σ_{ρ ≤ m∧n′, ρ≠μ} ∏_k q^{−k(m_k−ρ_k)} C(m_k,ρ_k)(1−q^k)^{m_k−ρ_k} ((1−t^k)/k)^{n′_k−ρ_k}/(n′_k−ρ_k)!.

**Matrix in the normalized basis.** Use H_{νμ} = a_{νμ}√(R_ν/R_μ), with R = ∏ k^{m_k} m_k! r_k^{m_k}. Write b_k = m_k−ρ_k and c_k = n′_k−ρ_k. The powers of r_k combine to give

H_{νμ} = (1−t)^(-1) Σ_ρ q^{−(D−|ρ|)} ∏_k [√(m_k! n′_k!)/(ρ_k! b_k! c_k!)] · s_k^{(b_k+c_k)/2},  where s_k = (1−q^k)(1−t^k)/k.

**Properties.**
- This is manifestly symmetric in μ↔ν, confirming self-adjointness.
- Every term is positive.
- The term ρ = ∅ (n = D ≥ 1) is always present, so H_{νμ} > 0 for all μ,ν. The matrix is strictly positive, not merely nonnegative.

**Entry oracle.** The summand factorizes over k. The constraint Σk·b_k = Σk·c_k holds automatically, because |μ| = |ν| = D. Therefore

a_{νμ} = (1−t)^(-1) [∏_k Σ_{ρ_k=0}^{min(m_k,n′_k)} (k-factor)] − δ_{μν}/(1−t).

This is exact rational arithmetic with O(D²) terms of O(D log D) bits. It is a poly(D) exact entry oracle, but it is not a sampler.

## 2. The Perron vector, derived directly

Let G(y) = Σ_D g_D y^D = exp(Σ (1−t^k)p_k y^k/(k(1−q^k))). Its coefficients are g_D = Σ_μ p_μ/R_μ (matching Borodin–Corwin's g_r = Q_(r)).

1. **Removal.** The translation property gives V^*(w)G(y) = G(y)·exp(Σ(1−t^k)(wy)^k/k) = G(y)(1−twy)/(1−wy). Hence V_n^* g_D = (1−t) g_{D−n} for 1 ≤ n ≤ D.
2. **Addition.** Since q^{−k} + 1/(1−q^k) = 1/(q^k(1−q^k)), we get V(y/q)G(y) = G(y/q). Taking [y^D]: Σ_{n=0}^D q^{−n} V_n g_{D−n} = q^{−D} g_D.
3. **Conclusion.** H g_D = Σ_{n=1}^D q^{−n} V_n g_{D−n} = (q^{−D}−1) g_D.

**Normalized Perron vector.** φ(μ) = R_μ^(-1/2)/√Z, with Z = ⟨g_D,g_D⟩ = Σ_μ 1/R_μ. Since r_k ≥ 1, Z ≤ Σ 1/z_μ = 1. The repository baseline gives Z = (t;q)_D/(q;q)_D. The stationary law π = φ² is exactly the reviewed row law.

**Simplicity and an explicit gap (no division by spectral gaps between other eigenvalues).** Let f(x) = q^{−x} − 1, which is convex with f(0) = 0.
- For λ ≠ (D): E_λ ≤ Σ f(λ_i) ≤ f(D−1) + f(1), by Karamata, since (D−1,1) majorizes λ.
- Hence 1 − E_λ/λ0 ≥ (q^{-1}−1)(q^{−(D−1)}−1)/(q^{−D}−1).
- At q = t³ with D ≥ 2: q^{-1}−1 ≥ 3/D, q^{−(D−1)}−1 ≥ 3/2, and λ0 = (1+1/D)^{3D} − 1 ∈ [7, e³−1).
- So the gap is at least 1/(5D).
- All E_λ > 0, so K has spectrum in (0,1].

## 3. The Doob chain and exact similarity constants

**Definition.** Set K_{μν} = H_{μν}φ(ν)/(λ0 φ(μ)), i.e. K = λ0^(-1) D_φ^(-1) H D_φ.

**Exact constants.**
- Inverse similarity: H = λ0 D_φ K D_φ^(-1).
- Perron data: λ0 = q^{−D} − 1, φ(μ)² = π(μ) = 1/(Z R_μ).
- Relation to the p-basis: write S = diag(√R) and A_{νμ} = a_{νμ}. Then H = S A S^(-1). Self-adjointness gives R_ν a_{νμ} = R_μ a_{μν}, hence S² A S^(-2) = Aᵀ and K_{μν} = a_{νμ}/λ0.
- Reversibility: π(μ)K_{μν} = π(ν)K_{νμ}.
- Eigenvectors: right eigenvectors are f_λ(μ) = √Z R_μ [p_μ]J_λ/‖J_λ‖, with eigenvalue E_λ/λ0. Left eigenvectors are the p-coefficients of J_λ.

**Normalization, proved combinatorially.**
- Removal factor: Σ_{β≤m} q^{−|β|} ∏ C(m_k,β_k)(1−q^k)^{β_k} = ∏_k(q^k + 1 − q^k)^{m_k} q^{−k m_k} = q^{−D}. Excluding β = 0 leaves λ0.
- Addition factor: for n ≥ 1, Σ_{Σkα_k=n} ∏((1−t^k)/k)^{α_k}/α_k! = [z^n](1−tz)/(1−z) = 1−t, which cancels the prefactor (1−t)^(-1).
- Hence Σ_ν K_{μν} = 1. Moreover q^{−n} ∏ C(1−q^k)^{β_k} = q^{−D} Pr[β], where Pr is the law of independent deletions (part of size k deleted with probability 1−q^k).
- Therefore K(μ→ν) = Pr[β | β≠0] · A_n(α), with A_n(α) = (1−t)^(-1) ∏((1−t^k)/k)^{α_k}/α_k!.

**Exact D = 2 check.** Here t = 2/3 and q = t³, but the identities hold for general q,t.
- K((2)→(11)) = (1−t)/2.
- K((11)→(2)) = (1−q)(1+t)/(2(1+q)).
- Detailed balance with R_{(2)} = 2r_2 and R_{(11)} = 2r_1² holds identically.
- The nontrivial eigenvalue is 1 − (1−t)/2 − (1−q)(1+t)/(2(1+q)) = q(1+t)/(1+q) = E_{(11)}/λ0, as Eq. 1.18 requires.

**Comparison with Diaconis–Ram.** This is unchecked recollection, not from the supplied sources. Diaconis–Ram (Ann. Probab. 2012) give a remove-parts/add-a-partition auxiliary-variables chain on partitions of n, with stationary law ∝ 1/(z_λ ∏ r_{λ_i}) and Macdonald coefficients as eigenfunctions.
- The derived chain has exactly this stationary law and this two-step structure.
- I cannot certify from the extracts that the kernels coincide. They could differ, for example, by q↔q^(-1) conventions, laziness, or deletion rule.
- **Decisive test:** compare their n = 2 kernel and nontrivial eigenvalue with the two transition entries and q(1+t)/(1+q) above.

## 4. Sampling one update: algorithm and BIT cost

**Input.** Multiplicities (m_k), with at most D parts.

1. **Deletion.** For each part of size k, draw Bernoulli(1−q^k), where q^k = D^{3k}/(D+1)^{3k} has at most 3D log(D+1) + 1 bits. Repeat if nothing is deleted. The acceptance probability is 1−q^D ≥ 7/8, since q^D = (1+1/D)^{−3D} ≤ 1/8. Let n be the deleted mass.
2. **Redistribution.** Sample α ~ A_n by the size-biased recursion with Z_0 = 1 and Z_r = 1−t for r ≥ 1. From remaining mass r:
   - choose k < r with probability (1−t^k)/r;
   - choose k = r with probability (1−t^r)/(r(1−t)) = (D+1)(1−t^r)/r.
   The CDF has closed form F(k) = (k − D(1−t^k))/r for k < r, so inversion uses binary search.
   - *Correctness proof:* write P_n(α) = ∏(w_k/k)^{α_k}/α_k!/Z_n with w_k = 1−t^k. Then Σ_k [w_k Z_{n−k}/(nZ_n)] P_{n−k}(α−e_k) = Σ_k (kα_k/n) P_n(α) = P_n(α). Induct on n.
3. **Output.** ν = μ − β + α.

**Exact Las Vegas cost.**
- Precompute powers D^j and (D+1)^j for j ≤ 3D.
- Steps 1–2 use at most 2D draws, each comparing lazy random bits with a rational of O(D log D) bits. Expected cost is O(D log D) per Bernoulli and O(log D·M(D log D)) per binary search.
- Total expected cost is Õ(D²) bit operations, with expected at most 8/7 rejection rounds.

**Finite worst-case version.**
- Cap rejection at ⌈b/3⌉ + 1 rounds, giving failure probability ≤ 2^{−b−3}.
- Truncate every comparison at b + ⌈log₂(8D)⌉ bits.
- The union bound gives TV ≤ 2^-b at cost Õ(D(D log D + b)).
- No normalization constant, coefficient table or eigenvector is needed.

## 5. Real time through the Doob conjugation

**Ratio-free form.** e^{−iTH} = D_φ e^{−iθK} D_φ^(-1), with θ = Tλ0 = 2πτλ0. The amplitude can be written in two equivalent ways:
(e^{−iTH})_{νμ} = φ(ν)M_{νμ}/φ(μ) = φ(μ)M_{μν}/φ(ν).
Multiplying one form by the conjugate of the other gives the exact ratio-free formula

**P_{μ,τ}(ν) = M_{μν} · conj(M)_{νμ},  with M = e^{−iθK}.**

**Ratio charge for the one-sided form.** The one-sided amplitude estimator carries the factor √(π(μ)/π(ν)). For μ = (D), ν = (1^D) this is √(R_{1^D}/R_{(D)}) ≥ √((D−1)!(7/4)^D/3), using r_1 ≥ 7/4 and r_D ≤ 3. The two-sided form avoids it entirely.

**Periodicity.** Each term satisfies q^{−λ_i}t^{i−1} = ((D+1)/D)^{3λ_i−i+1}, with exponents in [4−D, 3D].
- So P := D^{3D}(D+1)^{D−1} has P·E_λ ∈ ℤ for all λ.
- For τ = a/c, reducing a mod cP is exact.
- Effective times are therefore still as large as about P, which has O(D log D) bits.

**Natural estimator.**
- Draw N1, N2 ~ Poisson(θ). Run the chain N1 steps from μ to get ν, then N2 steps from ν to get Y.
- Output v = e^{2θ} i^{N2−N1} O(ν) 1[Y=μ].
- Since e^{−θ}Σ θ^n(−i)^n K^n/n! = e^{−θ}M, we get E v = Σ_ν M_{μν}O(ν)conj(M)_{νμ} = E_{P_τ}[O].
- Taking O = 1[ν=ν0] estimates P(ν0) without bias.

**Variance lower bound on an explicit family.** Take μ = (D) and O = n_D (the specified mode count k·n_k/D with k = D).
- Staying probability: K((D)→(D)) = A_D((D)) = (D+1)(1−t^D)/D =: κ_D. Since t^D ∈ [e^-1, 1/2], κ_D ∈ [1/2, 1].
- Paths staying at (D) throughout give E|v|² ≥ e^{4θ}(E κ^{N1})² = e^{2θ(1+κ_D)} ≥ e^{3θ}.
- Meanwhile |E v| ≤ 1.
- So Var ≥ e^{3θ} − 1 ≥ e^{42π|τ|} − 1. Asymptotically κ_D → 1 − 1/e, giving an exponent ≈ 3.26θ.
- Exact D = 1 control: E v = 1 and E|v|² = e^{4θ}.
- At τ = P the dynamics is exactly the identity, yet the variance is at least e^{42πP} − 1.

**Removable versus essential costs.**
- *Time cost* (Θ(θ) chain steps) is removable. Use the gap bound 1/(5D), the bound log(1/π(μ)) ≤ log(D!·3^D), and exact π sampling by the row DP. Steps beyond N0 = O(D(D log D + b + θ)) can be replaced by an exact π draw, at bias ≤ e^{2θ}·2^{-b}.
- *Weights* are not removable this way. Projecting out the Perron component exactly still leaves Poisson coefficients of total mass about e^{θ(1−gap)}.
- *Accuracy:* even at θ = O(1), converting additive estimates into a TV-2^-b sampler by conditionals costs 2^{O(b)}. The recollected "estimation→sampling" lemmas are not relied on.

**Constructive small-time result.** For |τ| ≤ κ0 ln D/(8πλ0), and any O with |O| ≤ 1, the mean of O(e^{4θ}ε^-2 log(1/δ)) samples estimates E_{P_τ}[O] to ±ε. The total cost is D^{O(κ0)}·Õ(D²)·ε^-2 log(1/δ).

## 6. Imaginary time (aside, scoped)

- e^{sH} = e^{sλ0} D_φ e^{sλ0(K−I)} D_φ^(-1), which is a true Markov semigroup and is samplable by uniformization.
- The Born law of e^{sH}e_μ is ∝ S_{μν}S_{νμ}, with S = e^{sλ0(K−I)}.
- Return-conditioning accepts with probability → π(μ) ≤ 3D/(D!(7/4)^D) for μ = (1^D). However, the limiting law π itself is directly samplable.
- The general case is not settled here.

## 7. Proof obligations, falsifiers and the next question

**Discharged here.**
- Row-sum identity.
- Positivity.
- Reversibility.
- Similarity constants.
- Update sampler and its BIT costs.
- Ratio-free formula.
- Estimator unbiasedness and its variance bound.

**Exact falsifiers.**
- For the Doob claims: any μ with Σ_ν [p_ν]Hp_μ ≠ q^{−D} − 1, or any mismatch with the D = 2 kernel above.
- For the scoped negative result: a flaw in E v = E_P[O]. The variance bound itself is a one-line deduction.
- Global falsifier: an exact poly(D,L,b) classical sampler for all D.

**Not claimed.** No hardness, and no claim that other estimators fail.

**Next decisive question.** For the one-boson input μ = (D), the spectral support is O(D³) shapes (a,b,c,1^r), by Mickler's Theorem 4.1. The question is whether [p_ν]J_λ on these shapes admits a D^{O(1)}-term tilt Φ over a row or column cycle law, analogous to the near-row representation.
- If yes, combining it with the exact rational phases gives a poly classical sampler for that input.
- If no, this Doob route gives no further leverage there.
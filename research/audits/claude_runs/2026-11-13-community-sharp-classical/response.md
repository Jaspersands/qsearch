# Log-free classical detector for the native 4-uniform, 3-community Bernoulli hypergraph

## 0. Verdict

**The adaptation succeeds.** I could not find a failing identity. On the exact native input (p=4, k=3, q=1/4, one bit for every 4-set, ε known), there is a classical detector with:

- **Detection range:** β ≥ C₄,₃ · n⁻¹ · ℓ^(−1/2), with no log factor.
- **Cost:** n^(ℓ+2) · poly(ℓ, log n) bit operations.

The proof needs less of the paper's machinery than the candidate assumed:

- **Fresh mass:** no probabilistic fresh-mass extension is needed, neither Mecke nor sampling without replacement. On the complete deterministic support, the fresh-mass hypothesis (5.6) becomes a deterministic count.
- **Normalizer and transfer:** no degree normalizer and no Lemma 4.5 transfer are needed. A deterministic normalizer lets plain Jensen on Schatten norms carry the analysis-only symmetrization.
- **Where log-freeness comes from:** it comes entirely from the closing count (Lemma 5.1) and excess accounting at moment t ≍ ℓ log n. The degree-normalization identity in Remark 5.4 plays no role, because native Kikuchi degrees are deterministic.

**What this proof rests on:**

- Primary Lemmas 5.1 and 5.2(1), read from the supplied source. I re-checked the proof of Lemma 5.1.
- The user-supplied certificate facts, which I re-derived below with explicit constants for typical labels.

**What is not claimed:** nothing about hardness, novelty, or optimality, and nothing about quantum algorithms that might use a log-free analysis.

## 1. Algorithm, constants, ranges, bit model

**Rows.** Rows are injective ordered tuples I ∈ [n]^ℓ. There are N_ord = (n)_ℓ ≤ n^ℓ of them. Require 4 | ℓ, write ℓ = 4λ, and take 8 ≤ ℓ ≤ c₀√n.

**Matrix.**
- K = Σ_E (Y_E − q) Ã_E.
- (Ã_E)_{I,I′} = 1 exactly when:
  - I and I′ differ in exactly two positions J₀, and
  - {i_a, i′_a : a ∈ J₀} = E consists of 4 distinct vertices.
- Each row has b_ord = C(ℓ,2)(n−ℓ)(n−ℓ−1) = 2·b_{2,ℓ} ≤ ℓ²n²/2 nonzeros.
- The integer matrix M = 4K has entries in {−1, 3}.

**Statistic.**
- Set s = ⌈ℓ log₄ n⌉ + 2 and R = ⌈log² n⌉.
- Draw independent Rademacher vectors v₁,…,v_R ∈ {±1}^{N_ord}.
- Compute ‖M^s v_r‖² exactly in integers. Equivalently, v_r^T K^{2s} v_r = 4^(−2s)‖M^s v_r‖².
- Set τ_alg = ε̃ ℓ² n² / 450, where ε̃ is a known rational with ε/2 ≤ ε̃ ≤ ε. With ε given exactly, take ε̃ = ε.
- Output **planted** iff some r has v_r^T K^{2s} v_r > N_ord · τ_alg^{2s}.

**Bit cost.**
- Each entry of M^j v is bounded by (3ℓ²n²)^j, so it fits in O(ℓ log² n) bits.
- One matvec costs N_ord · b_ord multiply-adds of those integers.
- The total is R · s · n^(ℓ+2) · ℓ² · O(ℓ log² n) = n^(ℓ+2) · poly(ℓ, log n).
- Reading the input costs n⁴/24 bits.
- Memory is n^ℓ · O(ℓ log² n) bits plus the input.
- Neighbour enumeration costs poly(ℓ, log n) per entry.
- **Randomness-free variant:** computing Tr(M^{2s}) exactly costs n^(2ℓ+2) poly. That is still n^(O(ℓ)).

**Input use.** No extra samples, labels, repeats, or oracles are used. The copy Y′ below exists only inside an expectation.

## 2. Theorem (native model)

**Statement.** There are absolute constants C_* and c₀ such that the following holds. Let 8 ≤ ℓ ≤ c₀√n with 4 | ℓ, and let ε ≥ 900 C_* / (n√ℓ), i.e. β ≥ C₄,₃ n⁻¹ ℓ^(−1/2) with C₄,₃ = 3600 C_*/√3. Then the detector above has total error at most

n^(−Bℓ) + 6e^(−2n^(1/3)) + (13/16)^R = o(1).

### Proof

**(A) Exact symmetrization.**

1. Let Y′ be an analysis-only independent copy of Y with the same law: conditional on x in the planted case, unconditional in the null case.
2. Write K̄ := K − E[K | x], with E[K | x] = 0 in the null case. Then K̄ = E′[K − K′].
3. Tr(H^{2t}) = ‖H‖_{S_{2t}}^{2t} is convex in symmetric H. Jensen therefore gives E Tr(K̄^{2t}) ≤ E Tr((K − K′)^{2t}).
4. Expand the difference: K − K′ = Σ_E (Y_E − Y′_E) Ã_E.
5. Because (Y_E, Y′_E) is exchangeable and independent across E, we can write Y_E − Y′_E = σ_E u_E, where:
   - u_E = |Y_E − Y′_E| ∈ {0, 1}, and
   - the σ_E are i.i.d. Rademacher, independent of u.

   This holds for **any** Bernoulli parameters, so it covers the biased native values, which are not symmetric themselves.

**(B) Deterministic-support trace bound, adapted from Theorem 5.3.**

Fix u ∈ [−1,1]^{(n choose 4)} and average over σ. Only words in which every label has even multiplicity survive, with weight at most 1. Words are counted first on the slice, using b := b_{2,ℓ}:

1. **Chronologies.** By Lemma 5.2(1) there are at most C^t 2^χ of them.
2. **Opening an old label.** At most b choices, since all candidates are legal at S.
3. **Opening a first-use label with h recycled exterior vertices.** At most C(ℓ,2)·(ℓ + 8t)^h · n^(2−h) ≤ 4b(9t/n)^h choices. This is the deterministic replacement for (5.6), so no Mecke or (4.7) step is needed.
4. **Closing.** By Lemma 5.1 with r = 2, at most (ℓ + 2χ)/2 choices. I checked its proof: it is purely combinatorial and valid for distinct physical labels.
5. **Lift to ordered rows.** Multiply by ℓ! for the starting ordering and by 2 per step for placing the two new vertices in the vacated positions.

Combining these:

E_σ Tr((Σ σ_E u_E Ã_E)^{2t}) ≤ N_ord (C₃ ℓ b)^t Σ_χ (18t/n)^χ (1 + 2χ/ℓ)^t.

**Fixing t and summing.**

1. Take t = ⌊cℓ log n⌋ with c = 1/16. Then (1 + 2χ/ℓ)^t ≤ n^(2cχ).
2. Since ℓ ≤ c₀√n, we have ℓ log n ≤ n^(3/4), so 18t/n ≤ n^(−1/4+o(1)). The χ-sum is at most 2.
3. Markov's inequality then gives P(‖K̄‖ > C_* ℓ^(3/2) n) ≤ n^(−Bℓ), with C_* = e^((B+2)/c) · O(1).
4. The prefactor N_ord^(1/2t) = O(1), because t ≍ ℓ log n. This is exactly where the log disappears.

**(C) Mean identity: E[K | x] = ε(ΠBΠ − ℰ).**

For injective I, I′, the entries of B behave as follows:

| Relation between I and I′ | Entry of ΠBΠ | Assigned to |
|---|---|---|
| Differ in exactly J₀, 4 distinct vertices | Σ_c Π_{v∈E} w_c(v) = f(E) | Σ_E f(E) Ã_E |
| Equal (diagonal) | ≤ ℓ²/3 | ℰ |
| Differ in exactly one position | Row sum ≤ ℓn | ℰ |
| Differ in two positions, 3 or 2 distinct vertices | Row count ≤ ℓ²n + ℓ², entries < 1 | ℰ |
| Differ in ≥ 3 positions | 0 | — |

By the Schur test, ‖ℰ‖ ≤ 3ℓ²n.

**(D) Rayleigh certificate. The vector is never computed.**

1. **Typical labels.** Assume |n_c − n/3| ≤ n^(2/3); this fails with probability at most 6e^(−2n^(1/3)) by Hoeffding.
2. **Gram matrix.** G_{cc′} = ⟨w_c, w_{c′}⟩ = (n/3)P + O(n^(2/3)), where P = I − 11ᵀ/3.
3. **Block test vector.** Take φ = (F/‖F‖)^{⊗λ} and set a_c = ⟨F̂, (w_c w_cᵀ)_s F̂⟩ for a position s in a block. Then
   - a_c = Σ_{c′,c″} G_{cc′} G_{cc″} G³_{c′c″} / Σ G⁴_{c′c″} = n/9 + O(n^(2/3)).
4. **Lower bound on φᵀBφ.**
   - B is PSD, so we may keep only the ℓ(ℓ−4)/2 cross-block pairs J.
   - Each such J contributes Σ_c a_c² ≥ n²/28.
   - Hence φᵀBφ ≥ ℓ²n²/112 for ℓ ≥ 8.
5. **Projection to injective tuples.**
   - ‖F‖² ≥ 3(n/9)⁴ and ‖F‖_∞ ≤ 16/27, so every one-coordinate marginal and every within-block collision probability is at most 768/n. This bound is uniform over labels.
   - Hence η := ‖(1−Π)φ‖ ≤ 20ℓ/√n.
   - Also ‖B‖ ≤ C(ℓ,2) Σ_c G²_{cc} ≤ (8/27)ℓ²n².
6. **Combine.** With ψ = Πφ/‖Πφ‖:

   ψᵀ E[K|x] ψ / ε ≥ ℓ²n²/112 − 2‖B‖η − ‖ℰ‖ ≥ ℓ²n²/150,

   for ℓ ≤ √n/12000 and n ≥ 3000.

**(E) Decision.**

- **Null.** On ‖K‖ ≤ C_* ℓ^(3/2) n ≤ τ_alg, we have v^T K^{2s} v ≤ N_ord ‖K‖^{2s} ≤ N_ord τ_alg^{2s}. So the detector outputs null, deterministically on that event.
- **Planted (typical x, noise event).**
  1. λ_max(K) ≥ εℓ²n²/150 − τ_alg ≥ 2τ_alg.
  2. Let u be the top eigenvector. Then v^T K^{2s} v ≥ (2τ_alg)^{2s} (v·u)².
  3. Paley–Zygmund gives (v·u)² ≥ 1/4 with probability at least 3/16.
  4. Since 4^s/4 > N_ord, the statistic exceeds the threshold.

**Range check.** The inequality C_* ℓ^(3/2) n ≤ τ_alg is exactly the stated ε-condition, with the factor 2 absorbing ε̃ versus ε. ∎

## 3. Audit of the four mismatches

| Issue | Literal status | Exact disposition |
|---|---|---|
| Deterministic distinct supports vs Poisson/i.i.d. clauses | Theorem 5.3, Proposition 6.1, Lemma 4.2 and Remark 4.4 hypotheses are **not met** | Not needed. (5.6) becomes a deterministic count, no exposure or filtration is required, and labels never repeat. |
| Biased centered Bernoulli vs Rademacher | Theorem 5.3 requires independent signs | Y−Y′ = σu exactly, with u ⊥ σ. |
| Multicommunity vs Boolean gauge | **Fails.** The identity Z_SS Z_TT = x_{S△T} needs x_i² = 1, but w_c(i)² ∈ {4/9, 1/9}. Lemma 6.2 and Proposition 6.4 therefore do not transfer. | Replaced by the PSD certificate ΠBΠ − ℰ of step (C). |
| Slice vs ordered tuples | — | See below. |

**Symmetrization: where the paper's route would actually fail.** If the paper's random normalizer Γ = G + dI with G = Σ u_E P_E were kept, the Jensen step would fail: Γ depends on (Y, Y′), so Γ^(−1/2) K Γ^(−1/2) is not E′ of the symmetrized normalized matrix. Lemma 4.5 would then be needed. A deterministic normalizer removes this obstruction, at a constant-factor cost since G ⪯ bI.

**Slice vs ordered tuples.**
- K_ord commutes with permutations of positions.
- On the symmetric sector it equals 2× the slice matrix.
- φ is not symmetric across blocks: the cross terms w_{c₁}^{⊗4} ⊗ w_{c₂}^{⊗4} with c₁ ≠ c₂ are not symmetrized.
- The top eigenvector may therefore lie in a non-trivial isotypic sector.
- Consequently a **slice** detector is not proved here. The ordered detector is proved and costs n^(ℓ+O(1)).

## 4. Primary theorem dispositions

- **Theorems 2.2, 2.5, 5.3 and Proposition 6.1:** not applicable verbatim (kXOR, random supports, signs). The proof of Theorem 5.3 transfers in simplified form, as step (B).
- **Lemmas 5.1 and 5.2(1):** used as-is.
- **Lemmas 4.1–4.3 and 4.5:** unused.
- **Lemma 4.6 (Krylov):** replaced by the exact-integer power statistic, which avoids any floating-point analysis.
- **Theorem 2.6 and Corollary 2.8:** concern noisy kXOR. Nothing here is inferred from them.

## 5. Same original-input comparison at β = C/(n√log n)

All three detectors below use the same input: all C(n,4) bits, paid once.

| Detector | Required level ℓ | Cost |
|---|---|---|
| This classical detector | ℓ_cl = max(8, 4⌈(C₄,₃/C)² log n / 4⌉) | n^(ℓ_cl+2) poly = exp((C₄,₃/C)² log² n · (1+o(1))) |
| Repaired quantum bound (as supplied; I did not verify it) | ℓ_q ≥ (B_pk/C)² log² n | n^(ℓ_q/4) e^(O(ℓ_q log ℓ_q)) = exp(Ω(log³ n)) |
| Unnormalized classical at ℓ_q | ℓ_q | n^(ℓ_q) = exp(Θ(log³ n)) |

Consequences:
- For every fixed C and B, the classical log-free detector is asymptotically cheaper than the stated quantum bound at this window. Any advantage claim for that bound, as stated, is falsified.
- The repair's sqrt(log n) loss is an analysis artifact for this input: the same dense Kikuchi matrix is log-free by (B).
- None of this says anything about a quantum algorithm with a log-free analysis.

## 6. Residual proof obligations and falsifiers

1. **Lemma 5.1 legality notion.** The bound must hold for ordered walks through their set projection. This holds because legality is set-based. A falsifier would be a closed ordered word whose closing choices are not bounded by (ℓ+2χ)/2 times 2.
2. **Typical-label Rayleigh constant n²/28.** This is a perturbation of the exact balanced value n²/27. Uniformity over all labels is not needed and was not re-derived.
3. **Unspecified absolute constants.** C_* inherits the C from Lemma 5.2(1). The algorithm's threshold uses only ε, ℓ and n, so no unknown constant enters the decision. Only the range constant C₄,₃ is non-numeric.
4. **Concrete falsifier for the theorem.** A null instance family with ‖K‖ ≫ ℓ^(3/2) n with probability that is not o(1) at ℓ ≍ log n. The trace bound E Tr(K^{2t}) ≤ 2N_ord(C₃ℓb)^t excludes this unless the word count in (B) is wrong.
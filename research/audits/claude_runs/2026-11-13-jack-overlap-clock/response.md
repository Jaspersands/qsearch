# Report: Jack–Lax two-stage growth, overlap bounds at α = 3

## 0. Verdict

The cheapest attack on this obligation is to look for a family that makes either stage overlap superpolynomially small. That attack fails. I prove the following, with all objects at ε₁ = 3, ε₂ = −1, ℏ = 3, ε = 2.

| Quantity, for d = \|λ\| and μ = λ+s | Proved lower bound | Strongest small family (exact) | Status |
|---|---|---|---|
| Stage 1: τ_λ^s = \|⟨Ĵ_λ, ψ̂_λ^s⟩\|² | 3/(16d) for d ≥ 1; equals 1 for d = 0 | λ = (d), s = (d,0): τ = 1/(3d+1) | Proved from MM Thm 1.4 and (A.31). Does not use the unproved identity. |
| Stage 2: ‖P_A ψ̂_λ^s‖² | 1/(d+1) for all d ≥ 0 | λ = (nⁿ), s = (n,0): (4n+2)/((n+2)(n²+1)) ≈ 4/d | Conditional on A_dψ_λ^s = J_{λ+s}, for that single pair only. |

Both overlaps are therefore Θ(1/d) in the worst case, with explicit constants. Overlap size is not the falsifier for this candidate.

Exact alternating measurement then uses O(d·log(1/δ)) measurements per stage, with no reset. One caveat: plain alternation has only Θ(1/δ) worst-case cost when the overlap is close to 1. A one-qubit dilution with a classically known angle fixes this (§4).

The scientific action moves to three places:
- the identity itself (§5 gives a sharp equivalent form and cheap necessary tests);
- the error and leakage analysis for the approximate content projector;
- the classical sampler check.

A note on the doc's wording: τ is a squared overlap (a probability). The amplitude is √τ. This follows from (A.31): τ = |⟨J,ψ⟩|²/(‖J‖²‖ψ‖²).

## 1. Corner geometry at α = 3 (PROVED, elementary)

Coordinates are s = (x, y), with x the column and y the row, and content [s] = 3x − y.

For λ ≠ ∅ with m removable corners, write:
- 0 = X₀ < X₁ < … < X_m and Y₁ > … > Y_m > Y_{m+1} = 0;
- outer corners R_k⁺ = (X_k, Y_k), for k = 1..m;
- addable corners A_k = (X_k, Y_{k+1}), for k = 0..m.

As a check, λ = (6,2,1) reproduces MM Fig. 1.

Let a_k = [A_k] and b_k = [R_k⁺]. Then:
- g_k := b_k − a_{k−1} = 3(X_k − X_{k−1}) ≥ 3;
- h_k := a_k − b_k = Y_k − Y_{k+1} ≥ 1.

So the integer interlacing a₀ < b₁ < a₁ < … < b_m < a_m is strict. The gaps alternate as multiples of 3 and positive integers.

Size constraints:
- X_m ≤ d and Y₁ ≤ d.
- For 1 ≤ i ≤ m−1, the box (X_i − 1, Y_{i+1}) lies in λ. Hence d ≥ X_i(Y_{i+1}+1) > X_i·Y_{i+1}.

## 2. Stage 1: τ_λ^s ≥ 3/(16d)

Here τ_i = ∏_j (a_i − b_j) / ∏_{k≠i}(a_i − a_k), and the signs cancel. Split τ_i into a left factor 𝓛 and a right factor 𝓡.

**Left factor (pairs a_k with b_{k+1}, for k < i).**
- Write P_k = 3(X_i − X_k) and Q_k = Y_{k+1} − Y_{i+1}.
- Then 𝓛 = ∏_{k=0}^{i−1} (P_{k+1}+Q_k)/(P_k+Q_k).
- For k ≤ i−2, we have 0 < P_{k+1} < P_k. The inequality (P′+Q)/(P+Q) ≥ P′/P holds because P·Q ≥ P′·Q.
- The product telescopes to P_{i−1}/P₀ = (X_i − X_{i−1})/X_i.
- The last factor (k = i−1) is h_i/(g_i + h_i).
- Hence 𝓛 ≥ (g_i h_i)/(3X_i(g_i + h_i)).

**Right factor (pairs a_k with b_k, for k > i).**
- Write P′_k = 3(X_k − X_i) and Q′_k = Y_{i+1} − Y_k.
- Then 𝓡 = ∏_{k=i+1}^{m} (P′_k+Q′_k)/(P′_k+Q′_{k+1}).
- The first factor is g_{i+1}/(g_{i+1}+h_{i+1}).
- For k ≥ i+2, we have 0 < Q′_k < Q′_{k+1}. The inequality (P+Q)/(P+Q′) ≥ Q/Q′ applies.
- The product telescopes to Q′_{i+2}/Q′_{m+1} = h_{i+1}/Y_{i+1}.
- Hence 𝓡 ≥ (g_{i+1} h_{i+1})/(Y_{i+1}(g_{i+1}+h_{i+1})).

**Combining.** The function gh/(g+h) is increasing in both arguments, so its minimum over g ≥ 3, h ≥ 1 is 3/4. Therefore, for all λ and every addable corner s = (x, y):
- interior corner (x, y ≥ 1): τ ≥ 3/(16xy) > 3/(16d);
- top of first column, s = (0, Y₁): τ ≥ 3/(4Y₁) ≥ 3/(4d);
- end of first row, s = (X_m, 0): τ ≥ 1/(4X_m) ≥ 1/(4d);
- d = 0: A_∅ = {(0,0)} and R⁺ = ∅, so τ = 1.

**Tightness.**
- λ = (2,1), s = (1,1): τ = 3/16, which equals the interior bound.
- λ = (1), s = (1,0): τ = 1/4, which equals the end-of-row bound.
- Smallest known values: λ = (d), s = (d,0) gives τ = 1/(3d+1). λ = (1^d), s = (0,d) gives τ = 3/(d+3).
- So min over (λ,s) of τ lies in [3/(16d), 1/(3d+1)].

**No leakage in stage 1 (PROVED).**
- Z_λ is invariant under Π_F, since π₀Z_λ = ℂj_λ ⊂ Z_λ and Π_F is self-adjoint.
- Z_λ is invariant under Π_{[s]}.
- On Z_λ, Π_F = |Ĵ_λ⟩⟨Ĵ_λ| and Π_{[s]} = |ψ̂⟩⟨ψ̂|, by simple spectrum.
- The dynamics therefore stay in span{Ĵ_λ, ψ̂_λ^s}, even though the global content eigenspace is degenerate.

## 3. Stage 2 (CONDITIONAL on Aψ_λ^s = j_μ for this single pair)

**Step 1 (PROVED, by inspection).** On F_{d+1} ⊕ wF[w]_d, with wF[w]_d ≅ F[w]_d isometrically,

  L_{d+1} = [[0, A], [A†, L_d + 2]].

As a consequence, a_μ = ⟨j_μ, L j_μ⟩ = 0. Also J̃ := L j_μ = A†j_μ.

Using AA† = 3(d+1)I (Euler identity, checked) and (A.11):

  Σ_r τ̃_μ^r = ‖J̃‖²/‖j_μ‖² = 3(d+1).

**Step 2 (PROVED given the hypothesis).**
- Let Ψ be ψ_λ^s embedded in the w-block, and set σ = [s] + 2 = [s + (1,1)] ∈ [R_μ⁺].
- Then (L_{d+1} − σ)Ψ = j_μ.
- Split Ψ = Ψ_Z + Ψ_⊥ along Z_μ ⊕ Z_μ^⊥. Both pieces are L-invariant, since L is self-adjoint.
- Because σ ∉ spec L|_{Z_μ} (strict interlacing), Ψ_Z = (L − σ)⁻¹j_μ = ψ̃_μ^{(s)} by (A.37).
- Ψ_⊥ is a σ-eigenvector with π₀Ψ_⊥ = 0. This holds because π₀Ψ = 0, and π₀Ψ_Z = (⟨j_μ,Ψ⟩/‖j_μ‖²)j_μ = 0.
- Each Z_ν-component of Ψ_⊥ equals c_ν ψ_ν^t with π₀ = c_ν j_ν. Since Jacks are linearly independent, every c_ν = 0.
- Therefore Ψ = ψ̃_μ^{(s)}, and by (A.26), ‖ψ_λ^s‖² = ‖j_μ‖²/τ̃_μ^{(s)}.

**Result.**

  p₂ = ‖j_μ‖²/(3(d+1)‖ψ‖²) = τ̃_μ^{(s)}/(3(d+1)),

where

  τ̃_μ^{(s)} = ∏_{t∈A_μ}|σ − [t]| / ∏_{r′∈R_μ⁺∖{s+(1,1)}}|σ − [r′]|.

So p₂ is the normalized cotransition weight of μ.

**Lower bound.** Label the outer corners of μ as b_j, with neighbours a_{j−1} < b_j < a_j. Then

  τ̃_j = (b_j − a_{j−1})(a_j − b_j) · ∏_{k<j} (b_j − a_{k−1})/(b_j − b_k) · ∏_{k>j} (a_k − b_j)/(b_k − b_j).

Each factor in the two products is greater than 1. So τ̃_j ≥ g_j h_j ≥ 3, and p₂ ≥ 1/(d+1) = 1/|μ|.

This holds at both endpoints, since a_{j−1} and a_j always exist. For d = 0: Aψ_∅ = V₁ = j₁ and p₂ = 3/3 = 1. When μ is a rectangle (a single outer corner), p₂ = 1.

**Strongest small family.** Take λ = (nⁿ) and s = (n,0), with n ≥ 2:
- addable contents of μ: −n, 3n−1, 3n+3;
- outer contents of μ: 2n, 3n+2;
- p₂ = 3(4n+2)/((n+2)·3(n²+1)) ≈ 4/d.

Stage 1 for the same pair has τ = 1/4.

**Unconditional by-product.** |⟨V Ĵ_μ, ψ̂̃_μ^{(s)}⟩|² = τ̃/(3(d+1)) always holds, using (A.34). The hypothesis is used only to identify ψ̃_μ^{(s)} with ψ_λ^s.

**2D invariance (CONDITIONAL).** Q A†j_μ = τ̃ψ̃^{(s)}. This holds unconditionally because W̃_μ lies in the w-block and L̃ = (L_d + 2)|_{W̃}, so it uses only distinct removable contents. Under the hypothesis this equals τ̃ψ_λ^s. Hence span{ψ̂, P_A ψ̂} is invariant under both P_A and Π_{[s]}, and both act on it as rank-one projectors.

## 4. Alternating measurements, exact rank-one case, no reset

**Setting.** Two projectors P and Q act on an invariant 2D space with lines a (from P) and b (from Q), and p = |⟨a|b⟩|², q = 1 − p. The process starts in a.

**Transitions.**
- Q-measurement from a: reaches b with probability p, otherwise b^⊥.
- P-measurement from b^⊥: reaches a with probability q, otherwise a^⊥ (probability p).
- Q-measurement from a^⊥: reaches b with probability q.
- The process never leaves the 2D space, and no reset is needed.

**Success law.**
- Each (P, Q) round after the first failure succeeds with probability 2pq.
- Failure after 1 + k Q-measurements is exactly q(1 − 2pq)^k.
- Expected number of Q-measurements is 1 + 1/(2p).
- Expected total number of measurements is 1 + 1/p.

**Small overlap, p ≤ 1/2.** The failure probability is at most (1−p)^{k+1}. Choosing k = ⌈ln(1/δ)/p_min⌉ gives failure at most δ.
- Stage 1: k = ⌈(16d/3) ln(1/δ)⌉.
- Stage 2: k = ⌈(d+1) ln(1/δ)⌉.

**Pitfall at overlap near 1, p > 1/2.** The failure probability is at most q·e^{−qk}. Its supremum over q is 1/(ek), so blind alternation costs Θ(1/δ) in the worst case.

**Fix (PROVED).** p is classically computable from (1.18) or from τ̃ in O(d) operations. Stage 2 needs the hypothesis for this.
1. Add one ancilla qubit and set c = √θ|0⟩ + √(1−θ)|1⟩, with θ = 1/(2p).
2. Use the projectors P′ = P ⊗ |0⟩⟨0| and Q′ = Q ⊗ |c⟩⟨c|.
3. The space span{a⊗0, b⊗c} is invariant, and both projectors are rank one on it, with p′ = 1/2.
4. Failure after 1 + k Q-measurements is 2^{−(k+1)}.
5. On success the state is the product b⊗c, so discarding the ancilla leaves b exactly.
6. Knowing p to relative error 0.1 still gives a per-round success probability of at least 0.49.

**Full path cost.**
- Use δ = ε/(2D) per stage and a fixed maximum number of rounds.
- Exact total failure is at most ε, with O(D² log(D/ε)) measurements.
- On failure, restarting from j_∅ = 1 costs only poly(D). No recursively prepared state inverse is used.

**OPEN: approximate measurements.**
- If each implemented instrument is η-close in diamond norm to the ideal one, the hybrid argument with a fixed maximum length gives total error at most (number of measurements)·η.
- Achieving such η for Π_{[s]} via phase estimation of L_d is not proved here. The available facts are integer spectrum, gap 1, contents in [−d, 3d], and sparse rows.

## 5. Sharpened identity obligation and cheap falsifiers

**Equivalence (PROVED).** Aψ_λ^s = j_μ holds if and only if ψ_λ^s = ψ̃_μ^{(s)} (shifted). Equivalently, the w¹-coefficient of (L_{d+1} − [s] − 2)⁻¹ j_μ, restricted to Z_μ, equals j_λ.
- One direction is §3, Step 2.
- For the other: π₀Lψ̃ = j_μ by (A.16). Also, π₀ of an [s]-eigenvector of L_d equals j_λ only if that eigenvector is ψ_λ^s.

**Necessary consequences (cheap tests).**
- Norm ratio: ‖J_{λ+s}‖²/‖J_λ‖² = τ̃_{λ+s}^{(s)}/τ_λ^s.
- Path independence: the product of these ratios along every growth path to a given ν must be the same.
- Any single violation refutes the identity. Passing these tests proves nothing beyond the cases tested.

**FINITE CONTROL (hand computation, from MM's listed ψ at ε₁ = 3, ε₂ = −1).**
- Aψ = j_μ holds for all 7 pairs with d ≤ 2.
- p₂ values: (1)→(2) and (1)→(1,1) give 1; (2)→(2,1) gives 5/12; (1,1)→(2,1) gives 7/12. These sum to 1 over the corners of (2,1). In the last two cases p₂ equals ‖j_μ‖²/(3(d+1)‖ψ‖²) computed directly, e.g. ‖j_{21}‖² = 315 and ‖ψ_2^{(0,1)}‖² = 84.
- Norm ratios: ‖j_{1}‖², ‖j_{2}‖², ‖j_{11}‖², ‖j_{21}‖² = 3, 72, 24, 315. The two paths to (2,1) agree: 72·35/8 = 24·105/8 = 315.

These are finite controls only.

## 6. Action

Stop treating overlap size as a risk. It is Θ(1/d) with explicit constants (§2, §3), and only stage 2 depends on the identity. Next priorities, cheapest first:

1. Test the norm-ratio and path-independence consequences at degree around 10 to 15, using exact Gram–Schmidt Jack norms. Then attack the reformulated identity in §5.
2. Prove diamond-norm bounds for the content-projector instrument, including leakage outside the 2D blocks.
3. Run the classical sampler search on the same Born distribution. All overlaps here are explicit and classically computable, so they offer no hardness evidence.
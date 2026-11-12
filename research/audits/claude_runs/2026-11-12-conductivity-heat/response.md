# Review: parent marked-heat-kernel sampler (heat-context.md, final section)

**Verdict in one line.** I tried to break the construction at each of the listed joints and failed; after tightening constants and fixing one ordering of the error composition, the idealized and finite-bit arguments both close. I give the resulting theorem with explicit parameters. This is agreement with the parent's upper bound, not a hardness, separation, or optimality statement; the full-polynomial match in (n, 1/ε) remains OPEN, and I add a remark on why the n² per-step factor is intrinsic to this *class* of one-step samplers (heuristic, not proved).

Evidence used: heat-context.md (SHA256 6a7a9a7d…c326) and binomial-lemma.md (SHA256 831f42d7…14c) via its stated contract only: a Bin(N,p) sampler with TV ≤ δ_s, running time polynomial in log(N+2), bitlength(p), log(1/δ_s). No tools were run; every identity below was checked by hand.

---

## 1. Checked deductions (proved, idealized arithmetic)

Conventions: (Dφ)_(x,i) = φ(x+e_i) − φ(x); S_v f(x) = f(x+v); K0 = D*D with eigenvalues Σ_l 4 sin²(πk_l/L) ∈ [0, 8]; d = 2.

**(P1) Energy series.** Write a = c(I + zΣ), g = √N η_j. The minimizer field e = g + u with u ∈ ran D = ran Π and Π a e = 0. Using Πg = 0 (D_j* applied to the constant direction-j field is (S_{−e_j} − I)·const = 0), one gets (I + zΠΣ)e = g, hence e = Σ_r (−z)^r (ΠΣ)^r g, and K_j = (1/N)⟨g, a e⟩ = c[1 + z⟨η,Ση⟩ + zΣ_{r≥1}(−z)^r⟨η,Σ(ΠΣ)^r η⟩], which is exactly SERIES with T_r = ⟨η,ΣΠ(ΣΠ)^rΣη⟩. |T_r| ≤ 1 since Π, Σ are contractions. Tail of the truncation at k terms: ≤ c z^{k+2}/(1−z). Controls: Σ ≡ ±1 give ρ and 1; layers parallel to j give divergence-free Ση_j, so all T_r = 0 and K_j is the arithmetic mean. **Correct.**

**(P2) Heat-kernel representation.** e^{−tK0} = Π_l e^{−2t} e^{tS_{e_l}} e^{tS_{−e_l}}; expanding gives E f(x+Y), Y = Σ_l (N_l^+ − N_l^−) e_l mod L, all four counts independent Poisson(t). Wrap-around is automatic since S^L = I. **Correct.**

**(P3) Poisson integration by parts, including i = j.** For N ~ Poi(t): Σ_m e^{−t}t^{m−1}/(m−1)! f(x+m e) = E[(N/t) f(x+Ne)], so (S_{e_i} − I)E f(x+N_i^+ e_i) = E[(N_i^+/t − 1) f(x+N_i^+ e_i)]. Also D_j* = S_{−e_j} − I, so the second mark pairs with N_j^−. All shifts commute, so

(D_i e^{−tK0} D_j* f)(x) = E[(N_i^+/t − 1)(N_j^−/t − 1) f(x+Y)]   (MARKS)

holds for every i, j. For i = j the two marks use N_i^+ and N_i^−, which are independent, and the identity gives (S_{e_i}−I)(S_{−e_i}−I)e^{−tK0} = (2I − S_{e_i} − S_{−e_i})e^{−tK0}, the correct diagonal block. **Correct; the i = j case is not special.** Second moment of the product of marks: Var(N)/t² each, so exactly 1/t² for Poisson. **Correct.**

**(P4) Kernel orientation.** The path estimator needs *rows* of Π: from current edge (x,i) the next edge is (x+Y, j) with weight (N_i^+/t − 1)(N_j^−/t − 1), i.e. the "+" count belongs to the direction being left, the "−" count to the direction being entered. The small-time four-term form, with i the current direction, is shifts (e_i − e_j, +e_i, −e_j, 0) with signs (+, −, −, +). The parent's formula is written in this convention and is correct. **Warning for implementation:** using (N_i^+, N_j^+) would produce D_i D_j e^{−tK0} = (S_{e_i+e_j} − S_{e_i} − S_{e_j} + I)e^{−tK0}, a different operator for i ≠ j; this is the single most likely transcription bug and the L = 4 fixture must test an off-diagonal row. Because Π and all exact intermediate operators are symmetric, nothing else depends on row/column choice; the approximate operator Π̃ need not be symmetric, since only ‖Π̃ − Π‖ and the ordered path expectation are used.

**(P5) Time truncation.** Π − Π_T = V e^{−TK0} V* with V P0 = 0 and ‖V‖ = 1, so ‖Π − Π_T‖ ≤ e^{−λ_min^+ T}; λ_min^+ = 4 sin²(π/L) ≥ 16/L² (sin x ≥ 2x/π on [0, π/2], L ≥ 2). Π_T is a contraction. Replacing r+1 factors Π by Π_T in T_r costs ≤ (r+1)e^{−λ_min^+ T} by telescoping. **Correct** (the log in T must be natural or larger).

**(P6) Variance of one transition.** Interval chosen uniformly among J+1, then t uniformly (continuous or on the grid). Small interval: weight ±4·(J+1)·1, second moment 16(J+1)². Interval [2^ℓ, 2^{ℓ+1}]: weight (J+1)2^ℓ·marks, second moment (J+1)²2^{2ℓ}/t² ≤ (J+1)². Averaging over the uniform interval choice: ≤ (J+1)(16 + J). Uniform next direction with weight d = 2: conditional second moment

H² := 4(J+1)(J+16) ≤ 64(J+1)²,

matching the parent's 16d²(J+1)² as an upper bound. **Correct.**

**(P7) Variance of path products.** Each transition has conditional second moment ≤ H² given the past; Σ-values and the final direction indicator are bounded by 1 in modulus. By the tower property the (r+1)-step signed product has second moment ≤ H^{2(r+1)}. **Correct**; no hidden L- or Σ-dependence.

**(P8) Dyadic grid.** d/dt D_i e^{−tK0}D_j* = −D_i K0 e^{−tK0} D_j*, norm ≤ 2·8·2 = 32 = 16d; the four-term small-time integrand has the same bound. Midpoint rule with spacing h on [0,T] has operator error ≤ 16d·T·h/4 = 4dTh; so h ≤ τ/(4dT) = τ/(8T) gives error ≤ τ. The parent's O(τ/(d²T)) is sufficient. The index has O(log T + log 1/τ) bits and t is a dyadic rational, so N/t − 1 is exact rational arithmetic. **Correct.**

**(P9) Translation invariance makes ℓ¹ control sufficient.** Every approximate transition operator built below is a convolution with a signed kernel (its law does not depend on x; Σ is applied exactly afterwards). For such operators ‖·‖_{2→2} ≤ ‖kernel‖_{ℓ¹} = sup_{|f|≤1}|E[W f(x+Y)]|, which is exactly what coupling/TV arguments bound. This is the step the parent uses implicitly; it is valid.

---

## 2. Finite-bit composition, repaired with explicit tolerances

Fix τ > 0 (chosen in §3). Per transition, compose the following, in this order (ordering matters: clip before the TV comparisons so that the observable is bounded):

1. **Truncation** Π → Π_T: ℓ¹/operator error ≤ τ once T ≥ (L²/16) ln(1/τ).
2. **Grid**: error ≤ τ with h ≤ τ/(8T).
3. **Clipping at C := H²/τ** of the final signed transition weight W (including the (J+1)·d·width factors): the lost kernel mass is ≤ E[|W|1_{|W|>C}] ≤ E[W²]/C ≤ τ (Markov). Clipping cannot increase the second moment. The parent's statement is correct.
4. **Poisson → exact Binomial(Q, t/Q)** for all four counts: TV of the joint ≤ 4t²/Q ≤ 4T²/Q (Le Cam, product measures). With the clipped weight the observable is bounded by C, so the kernel error is ≤ 2C·4T²/Q ≤ τ/2 provided Q ≥ 16CT²/τ. Q = 2^q, q = O(n + log 1/τ) bits; p = t/Q is a dyadic rational of the same bit length, p ≤ 1 since Q ≥ T. Under exact binomial law the marks still have mean 0 exactly and second moment (1 − t/Q)/t ≤ 1/t each. (The parent's alternative Cauchy–Schwarz route, error ≤ (2/t)·√TV·width ≤ 4T/√Q, also gives polynomial Q; either suffices, one allocation is enough.)
5. **Binomial lemma** with per-call TV δ_s := τ/(16C): four calls per transition, joint TV ≤ 4δ_s, kernel error ≤ 2C·4δ_s = τ/2.

Resulting approximate transition operator Π̃: ‖Π̃ − Π‖ ≤ 4τ. Conditional second moment under the implemented law: the clipped weight squared is bounded by C², so its mean differs from the exact-Poisson one by ≤ 2C²·(4T²/Q + 4δ_s) ≤ 2C²·τ/(2C) = Cτ = H²; hence ≤ 2H². This makes the parent's "changes by at most a constant" explicit: the constant is 2, and it requires exactly the choices of Q and δ_s above.

**Bit lengths.** Node coordinates: n bits each; counts: q bits; t and weights: O(q + log(J+1)) bits; a path product of ≤ k clipped weights has magnitude ≤ C^k and O(k·log C) bits. All arithmetic is exact rational; no rounding is needed except inside the binomial lemma (already paid in its contract).

---

## 3. Theorem (explicit parameters)

**Theorem.** Let ρ ∈ (1, ρ0] rational, c = (ρ+1)/2, z = (ρ−1)/(ρ+1), ε ∈ (0,1], δ ∈ (0,1/2), L = 2^n, and let Σ be given by a size-B circuit. Set

- k = ⌈ ln(8c/((1−z)ε)) / ln(1/z) ⌉;
- δ_op = ε(1−z)²/(16c), τ = δ_op/4;
- J = ⌈log₂ max(2, (L²/16) ln(1/τ))⌉ ≤ 2n + log₂ln(1/τ), T = 2^J;
- h = 2^{−m} ≤ τ/(8T); H² = 4(J+1)(J+16); C = H²/τ; Q = 2^q ≥ 16CT²/τ; δ_s = τ/(16C);
- ε_T = ε(1−z)/(4c); group size s_r = ⌈8(2H²)^{r+1}/ε_T²⌉ for r = 0,…,k−1; number of groups g = ⌈4 ln(4k/δ)⌉;
- s_0' = ⌈2(8cz/ε)² ln(4/δ)⌉ samples for ⟨η,Ση⟩.

Then the estimator

K̂ = c[1 + z·mean(Σ over s_0' uniform direction-j edges) − z² Σ_{r<k} (−z)^r MoM_r],

with MoM_r the median of g means of s_r independent (r+1)-step clipped signed path products, satisfies |K̂ − K_j| ≤ ε with probability ≥ 1 − δ, for every circuit Σ, with total running time

Time ≤ poly(B, n, log(1/ε), log(1/δ), log(1/(1−z))) · (2H²)^k · c²(1−z)^{−2} ε^{−2},   (2H²)^k ≤ (128(J+1)²)^k.

The poly factor is: ≤ k transitions per sample, each costing 4 binomial-lemma calls with parameters (log Q, bitlength(t/Q), log 1/δ_s) = O(n + log(1/ε) + log(1/(1−z))) bits, one circuit evaluation (B), and O(n + q + k log C)-bit arithmetic; plus Σ_r s_r g ≤ 16 g (2H²)^k/ε_T² samples.

**Corollaries.**
(a) Fixed ρ, ε: k is a constant and J ≤ 2n + O(1), so Time ≤ poly(B)·n^{2k + O(1)}: polynomial in (B, n) with degree 2⌈ln(8c/((1−z)ε))/ln(1/z)⌉ + O(1). Note ln(1/z) = ln((ρ+1)/(ρ−1)) ≥ 2/ρ, so the degree is ≤ ρ ln(8c/((1−z)ε)) + O(1): exponential in ρ·log(1/ε), harmless at fixed contrast and precision.
(b) ε = n^{−a}: k ≤ a ln n/ln(1/z) + O_ρ(1), and (128(J+1)²)^k ≤ exp((2a/ln(1/z) + o(1)) ln² n) ≤ exp((aρ + o(1)) ln² n). Quasi-polynomial, times poly(B, n). Full polynomial in both n and 1/ε: not established.

**Proof outline (error budget).** Tail: c z^{k+2}/(1−z) ≤ ε/8 by choice of k. Operator errors: ‖Π̃ − Π‖ ≤ 4τ = δ_op and ‖Π̃‖ ≤ 1 + δ_op, so |T̃_r − T_r| ≤ (r+1)δ_op(1+δ_op)^r; since δ_op ≤ (1−z)/2, c z² Σ_r z^r (r+1)δ_op(1+δ_op)^r ≤ 4cz²δ_op/(1−z)² ≤ ε/4. Statistics: each T̃_r has second moment ≤ (2H²)^{r+1} (P7 with the §2 constant); Chebyshev gives each group mean within ε_T with probability ≥ 7/8, and Hoeffding on the median gives failure ≤ exp(−9g/32) ≤ δ/(4k); summing c z² Σ z^r ε_T ≤ ε/4. First mean: Hoeffding, error ≤ ε/(8cz)·cz = ε/8, failure ≤ δ/4. Total error ≤ ε, failure ≤ δ/4 + k·δ/(4k) ≤ δ/2. ∎

The per-step tolerance δ_op does not need a 1/k factor because the series weights are geometric; the parent's O(ε/poly(k,ρ)) is sufficient but wasteful.

---

## 4. What is assumed, what is control, what is speculation

**Assumed (imported):** the binomial-lemma TV contract and its polylog(Q) runtime. Nothing else is imported; no Green kernel, no O(t) loop, no IID, no field or normalization oracle is used. The score circuit is called once per visited edge.

**Finite controls that must be run (not yet run):** L = 4, ρ = 2, exact rational enumeration (Poisson truncated at a provable tail) of the sampled row kernel of D_i e^{−tK0}D_j* for an off-diagonal pair (i ≠ j) and for i = j, compared against the exact matrix; exact Π_T vs. Π at T = 2^J; the four-term small-time block at t = 0 (must equal D_i D_j*). These check transcription, not scaling.

**Speculative remark (not proved):** for any one-step estimator that samples a proposal y ~ p and returns K(y)/p(y), the second moment is Σ_y K(y)²/p(y) ≥ (Σ_y |K(y)|)² by Cauchy–Schwarz. If the rows of Π on the torus have ℓ¹ norm Θ(log L) (expected from |x|^{−2} decay of the discrete Riesz kernel in 2D; I have not proved this bound here), then H² = Ω(log² L) is unavoidable for this class, and the quasi-polynomial (log L)^{O(k)} factor cannot be removed by better importance weights within per-step unbiased sampling. This says nothing about other classical methods (control variates, deterministic multigrid, Fourier-side algorithms) and is not a lower bound.

---

## 5. Corrections and nits to the parent text

1. "second moment at most 16(J+1)²" for the Π_T sampler: correct; the sharper value is (J+1)(J+16).
2. "TV ≤ t²/Q": correct per count; the joint of four counts has TV ≤ 4t²/Q, and the comparison must be made *after* clipping (or via Cauchy–Schwarz before clipping). The parent lists both routes; one consistent allocation (above) is enough.
3. "Choose each sampler tolerance accordingly" must be δ_s ≤ τ/(16C) = τ²/(16H²); only then is the "constant factor" on the second moment the stated 2.
4. "T ≥ (L²/16) log(1/τ)": natural logar
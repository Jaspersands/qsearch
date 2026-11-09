# Proof audit of LEGENDRE_FOURIER_FEATURE_CLASSICAL_MATCH.md

I checked the note by hand, without tools. Its three central mathematical claims hold as scoped. I found no counterexample. The repairs below are minor. One scope remark broadens Section 2.

I did not check the following:
- the SHA256 hash;
- the cited artifacts (JSON and success-boundary note);
- the bound of 1.5·d^-d on success probability;
- the Russell–Shparlinski and Kopparty characterizations.

Treat all of these as unaudited.

## 1. Exact classical Fourier-mean estimator (claim (1))

**Derivation is correct.** Use QFT amplitudes D^{-1/2}ω^{⟨R,y⟩}, with ω = e^{2πi/p}. Then P_F(y) = (ND)^{-1}|Σ_R s(R)ω^{⟨R,y⟩}|². Summing ω^{⟨h,y⟩}P_F(y) over y forces R′ = R+h. This gives N^{-1}Σ_{R, R+h∈S} s(R)s(R+h).

- The opposite Fourier sign gives the sum over R′ = R−h. This equals the same sum after substitution, so the right-hand side is symmetric in h ↔ −h.
- The amplitudes are real, so P_F is even and the mean is real.
- Normalization is correct because |s| = 1 when F takes values ±1.

**Estimator is unbiased and bounded.**
- (c, m-subset) ↦ R is a bijection onto S, so the sampler is uniform. N = (p−1)·binom(p,m) is correct.
- The estimator is X = 1[R+h∈S]·s(R)s(R+h), which lies in [−1,1].
- It uses at most 2m classical sign queries.
- The factor χ(lead)^d is computed publicly.

**Small repairs:**
1. **Truncation must abort, not return 0.** A truncated root-finder run that returns 0 biases the estimate. The note's "failure allocated within δ" is correct only if such an event aborts the whole run.
2. **Only root extraction is randomized.** Whether R+h is split and squarefree can be tested deterministically: check (R+h) | X^p − X, via X^p mod (R+h). Extracting the roots (Cantor–Zassenhaus) is Las Vegas.
3. **Use Floyd's algorithm for the subset.** It gives a uniform m-subset with m bounded draws and avoids coupon-collector cost when m ≈ p. Exact uniform draws from F_p still need rejection sampling with a bounded clock.
4. **K must be a fixed upper bound** chosen in advance for the union bound. Conditional Hoeffding under adaptivity is valid because each query's samples are fresh given the transcript.

**SQ transfer: correct, and slightly extendable.**
- Any bounded φ(y) with Fourier ℓ1-mass B and an efficiently samplable spectrum can be estimated with O(B²ε^-2 log(K/δ)) observations. Sample h ∝ |φ̂(h)|, then run the estimator.
- Example: the coset indicator 1[y ∈ z+W′^⊥] for any public subspace W′ has B = 1.
- Hence a candidate Q′'s complete-syndrome probabilities are also classically estimable.

**What the transfer does not cover.** The note mostly states these points; I list them because they are where quantum Fourier sampling differs from SQ.
- It does not output labels.
- It does not find heavy hitters. Outputting a y from an exponentially large support is not an SQ task.
- It does not give exponentially many simultaneous means from one sample set.
- It does not give non-ℓ1-bounded functionals.
- It does not apply in the copy-only model. The match uses chosen-BIT access, so "not an oracle separation" holds only inside chosen-BIT.

## 2. Mask-only syndrome marginal (claim (2))

**Phase is constant on fibers.** For monic Q and R = c∏(X−r_i):

- Res(R,Q) = c^d ∏Q(r_i).
- Res(R,Q) = (−1)^{md}·det(multiplication by R on F_p[X]/Q) = (−1)^{md}·N_{A/F_p}(v).

Therefore s(R) = λ(−1)^{md}·χ_A(v). The global sign is explicit, and v ≠ 0 holds as claimed.

**Coset formula is correct.** Write y = z+η with η ∈ H. Then ω^{⟨R,η⟩} depends only on v. Parseval over V/W gives a factor |H| = p^d, and D/|H| = K0. This yields (2). The unit-modulus fiber phase drops out of each |a_v|.

**Scope remark (repair, not refutation).** The proof needs only one fact: the phase is a unit-modulus function of v = R mod Q.
- That holds for every monic Q with no roots in F_p, including reducible and even non-squarefree Q. In that case no Q(r_i) vanishes, and det(·R) depends only on v.
- It also holds for arbitrary R-dependent magnitudes b_R, provided the phase depends only on v.
- It genuinely fails when Q has an F_p-root a. The factor ∏_{r≠a}(a−r) ∝ R′(a) is not determined by v, and the λ(0) = +1 convention breaks the norm identity.

So "requires new analysis for reducible Q" is too cautious: only F_p-roots matter. The restriction to irreducible Q is sufficient but not necessary.

**Counterexample independently recomputed.**
- X²+2 is irreducible over F_5, since 3 is a nonsquare mod 5.
- F_25^*/F_5^* ≅ C6. This is P¹(F_5).
- The classes of α−r, r ∈ F_5, are exactly the five non-identity classes.
- χ_A is trivial on F_5^* and is the unique order-2 character of C6.
- The 3-subset sums of {1,…,5} mod 6 have counts (0:2, 1:1, 2:2, 3:2, 4:2, 5:1).
- Each class contains 4 values of v.

From these:

| Quantity | Value |
|---|---|
| Energy | 4·(4+1+4+4+4+1) = **72** |
| Signed sum | 4·(6−4) = **8** (λ(−1)^6 = +1) |
| P_F(0) | 64/(40·625) = **8/3125** |
| P_M(0) | N/D = **8/125** |
| P_M(H) | 72/(40·25) = **9/125** |
| Pr[T+Z = 0] | (1/125)/24 = **1/3000** |

All values agree with the note. Both models share the syndrome law: y mod H = Z mod H. The independent-noise full-label model is refuted, while syndrome equality stands. The note's distinction between syndrome law and full law is correctly drawn.

## 3. One-row occupancy

**The projector identity is correct.** P(s_i = 0) = p^{-1}Σ_C ‖Σ_{R∈C} ψ_R φ_R‖², summed over cosets C of span(X^iQ). By Cauchy–Schwarz, this is at most (max |C∩S|)/p. This holds for arbitrary weights and ancillas.

**Occupancy bounds hold.**
- For i = 0: a shared root x would force Q(x) = 0. Two labels with an identical root set would force Q ∝ R. So the root sets are disjoint, giving occupancy ≤ ⌊p/m⌋.
- For i > 0: labels can share only the root 0, so occupancy ≤ ⌊(p−1)/(m−1)⌋. This needs m ≥ 2, which holds.

**The final inequality checks.** 1/m + (m−d)/(m−1) ≤ 1 is equivalent to m(d−2) ≥ −1, which is true. The value at m = 2d−1 is correct.

**Scope.** The argument needs only that Q has no F_p-root. It concerns expected per-row correctness, which suffices against a "mostly correct" premise (Markov). It says nothing about low-inlier robust regression, collective statistics or attainability, as the note itself states.

## Falsifiers and proof obligations for the next step

- **(1) would fail** if the actual paid source differs from |S_F⟩. Examples: nonuniform weights from preparation or postselection, or a different pairing ⟨·,·⟩. The obligation is to confirm that the Hankel note's state and pairing match exactly.
- **(2) would fail** for Q with an F_p-root, or for a corrupted F that is non-constant on fibers. A cheap exact control is a reducible Q with a linear factor at p = 5 or 7.
- **Any claimed advantage** must use label-level information, such as within-coset coherent structure or heavy-hitter outputs. It cannot rest on ℓ1-bounded means, which are classically matched. Its cost must be charged against copy-only access if it is claimed beyond chosen-BIT.

None of these results gives hardness, a decoder, or a speedup. The note's disposition is accurate.
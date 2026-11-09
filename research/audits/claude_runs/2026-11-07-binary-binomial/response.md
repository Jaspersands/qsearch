# Audit: Bin(N,p) sampling lemma, bit-complexity version

## Verdict

**Fixable, and no counterexample found.** The core mathematics is sound: the Bernstein interval, the characteristic-function bound on the maximum pmf, the O(t) rejection rate, and absolute-precision acceptance all check out.

Six bookkeeping gaps must be closed before the lemma is fully proved:

1. **M must be a certified upper bound on max pmf.** "Within a constant factor" is not enough. Clipping acceptance probabilities greater than 1 would silently bias the output.
2. **The irrational quantities t, √(2vt) and 1/√v need rational outer approximations.** These must be rounded in the safe direction.
3. **The error amplification from normalization must be made explicit.** The relevant factor is LM/P(I), not just "R bounded."
4. **The nested rejection caps should be merged into one clock.**
5. **The Stirling remainder bound and the shift threshold need explicit constants.**
6. **Underflow, rounding and failure output need explicit TV accounting.**

All six are closed below. The result is a worst-case bit cost of poly(log N, B, log 1/δ), where B is the bit-length of p.

## Component checks

### Interval (correct)

- X − μ is a sum of independent centred terms with |X_i − p| ≤ 1 and variance sum v.
- Bernstein's inequality gives P(|X−μ| ≥ s) ≤ 2exp(−s²/(2(v+s/3))).
- The exponent is at least t exactly when s ≥ t/3 + √(t²/9 + 2vt).
- Since √(a+b) ≤ √a + √b, the choice s = √(2vt) + 2t/3 is at least this root.
- So the tail is at most 2e^{−t} = δ/4 when t = ln(8/δ).

**Rational fix:**
- Use t̄ = ⌈log₂(8/δ)⌉. This is at least ln(8/δ), and t̄ ≥ 3 for δ ≤ 1.
- Write p = a/b, so v = Na(b−a)/b² exactly.
- Set w = isqrt(⌈2vt̄⌉) + 1 and s̄ = w + ⌈2t̄/3⌉. Then s̄ ≥ s.
- Set I = [max(0, ⌈μ−s̄⌉), min(N, ⌊μ+s̄⌋)], with μ = Na/b computed exactly.
- Enlarging I only shrinks the tail.
- Let L = |I|. Then L ≤ 2s̄+1 ≤ 2√(2vt̄) + 4t̄/3 + 7.

### Envelope (correct)

- |1−p+pe^{iθ}|² = 1 − 4p(1−p)sin²(θ/2).
- For |θ| ≤ π, sin²(θ/2) ≥ θ²/π². Combined with 1−x ≤ e^{−x}, this gives |φ(θ)| ≤ exp(−2vθ²/π²).
- Hence pmf(k) ≤ (1/2π)∫exp(−2vθ²/π²)dθ ≤ √π/(2√(2v)) ≈ 0.627/√v.

**Rational fix:**
- Let r = isqrt(Na(b−a)). Then r ≥ 1 whenever 0 < p < 1.
- √v ≥ r/b, so b/r ≥ 1/√v, which is a certified upper bound.
- Since √(Na(b−a)) < r+1 ≤ 2r, we also have b/r ≤ 2/√v.
- Set M = min(1, b/r). Then M ≥ max pmf and M ≤ min(1, 2/√v).

**Product bound:**
- If v ≥ 1: LM ≤ 4√(2t̄) + 8t̄/3 + 14 ≤ 16t̄ for t̄ ≥ 3.
- If v < 1: L ≤ 2√(2t̄) + 4t̄/3 + 7 ≤ 16t̄ and M ≤ 1.
- So **LM ≤ 16t̄**, independent of N.
- p ∈ {0,1}: output 0 or N directly.

### Single clock (replaces nested caps)

Each round does the following:

1. Draw m = ⌈log₂L⌉ fair bits to get j ∈ [0, 2^m).
2. If j ≥ L, the round fails.
3. Otherwise set k = I_min + j and accept with probability q̃(k), using a dyadic q̃ with exact coin comparison.

**Acceptance rate:**
- Let q(k) = pmf(k)/M ≤ 1.
- Then Σ_{k∈I} q(k) = P(I)/M ≥ 3/(4M).
- Since 2^m < 2L, the exact per-round acceptance is at least 3/(8LM) ≥ 3/(128t̄).
- If |q̃−q| ≤ ε ≤ 1/(128t̄), the acceptance is A ≥ 1/(64t̄).

**Cap:**
- Run R = ⌈64t̄·ln(4/δ)⌉ = O(t̄²) rounds.
- If all fail, output ⌊μ⌋.
- P(fail) ≤ e^{−AR} ≤ δ/4.

### Normalization and TV (the step "since R bounded" needs this)

- Given success, the output is q̃/Σq̃ on I.
- ½‖q̃/Q̃ − q/Q‖₁ ≤ ‖q̃−q‖₁/Q ≤ Lε·M/(3/4) ≤ (64/3)t̄ε.
- Choose **ε = δ/(64t̄)**. This term is then at most δ/3.

Total TV:
- Failure output: δ/4.
- Acceptance error: δ/3.
- Truncation to I: δ/4.
- Sum: δ/4 + δ/3 + δ/4 < δ.

### Acceptance value from logs

- Let ℓ = ln pmf(k) − ln M. Then ℓ ≤ 0 because M is a certified envelope.
- Suppose |ℓ̃ − ℓ| ≤ η.
- Then |min(1, e^{ℓ̃}) − e^ℓ| ≤ e^η·η ≤ 2η.
- If ℓ̃ < −ln(16/ε), set q̃ = 0. This is underflow, and costs at most ε/8 extra error.
- Otherwise compute exp to absolute error ε/8, then round to r = ⌈log₂(8/ε)⌉ bits.
- With η = ε/8, the total is |q̃−q| ≤ ε.
- This confirms that absolute precision suffices and relative precision on tiny pmf values is not needed.

### Log-factorial: explicit and safe

Required bound: ℓ̃ needs total absolute error η = δ/(512t̄) across six terms. These are ln N!, ln k!, ln(N−k)!, k·ln p, (N−k)·ln(1−p), and ln M.

**Base logarithms:**
- Compute ln of integers up to max(N+1, b) to absolute error 2^{−P}.
- Use argument reduction z = 2^e·y with y ∈ [1, 2).
- Then ln z = e·ln2 + 2·atanh((y−1)/(y+1)).
- The atanh series converges with ratio at most 1/9, so O(P) terms suffice. ln2 is computed the same way.
- ln p = ln a − ln b and ln(1−p) = ln(b−a) − ln b.

**Stirling series:**
- For real x > 0, lnΓ(x) = (x−½)ln x − x + ½ln2π + Σ_{j=1}^{m} B_{2j}/(2j(2j−1)x^{2j−1}) + R_m.
- The classical remainder bound is |R_m| ≤ |B_{2m+2}|/((2m+2)(2m+1)x^{2m+1}).
- Using |B_{2j}| ≤ 4(2j)!/(2π)^{2j}, this gives |R_m| ≤ (2m/(2πx))^{2m} ≤ (2π)^{−2m} ≤ 2^{−5m} for x ≥ 2m.
- Take **m = ⌈P/5⌉ + 1** and threshold **T = 2m**.
- Compute B₂, …, B_{2m} exactly by the standard recurrence. This costs poly(m).

**Shift for small arguments:**
- For n+1 < T, use ln n! = ln((n+T)!) − ln Π_{j=1}^{T}(n+j).
- The product is an exact integer of at most T·log₂(2T) bits.

**Precision:**
- Errors in ln z are multiplied by integers up to N+1, which is where the O(log N) guard bits come from.
- Take **P = ⌈log₂(N+1)⌉ + ⌈log₂(1/δ)⌉ + ⌈log₂t̄⌉ + 14**.
- Add ⌈log₂(m+T+1)⌉ + 4 guard bits to cover accumulation of O(m+T) rounded terms.
- Then the total error is at most 12(N+1)·2^{−P} + 3·2^{−5m} ≤ η.
- All intermediate quantities have O(log N + log log N + P + B) bits.

### Cost

- Per round: O(log N) random bits plus poly(log N, B, P) bit operations.
- Number of rounds: O(t̄²).
- Precomputation (Bernoulli numbers, ln2, ln a, ln b, ln(b−a), M, I): poly(log N, B, log 1/δ).
- **Worst-case total: poly(log N, B, log(1/δ)).** There are no loops numerical in N.
- The bound is worst-case because of the hard cap, assuming a fair-coin bit model.

## Proof obligations for the independent checker

1. The Stirling remainder bound for real positive x: remainder bounded by the first omitted term. This is classical; verify the statement and the ζ(2j) ≤ 2 step.
2. The inequality sin(x) ≥ 2x/π on [0, π/2].
3. The algebra giving LM ≤ 16t̄ in both regimes v ≥ 1 and v < 1.
4. The normalized-ratio TV inequality ½‖x/|x| − y/|y|‖₁ ≤ ‖x−y‖₁/|y|.
5. Bernstein's inequality's applicability to the variables X_i − p, which are bounded by 1 in absolute value.

## Falsifiers to test

- **Envelope:** any (N, p, k) with pmf(k) > b/r would break it. Check small N exhaustively, including p near 0 and 1.
- **Interval:** any (N, p) with P(X ∉ I) > δ/4. Brute-force at small N.
- **Small-argument shift:** run k ∈ {0, 1, T−1, T} through the shifted path. Compare against exact ln k! computed from integer factorials.
- **Rounding:** at N = 2^{60}, p = 1 − 2^{−60}, check that ln(1−p) carries P + 60 effective bits. This tests the guard bits.

No quantum or hardness claim is implied.
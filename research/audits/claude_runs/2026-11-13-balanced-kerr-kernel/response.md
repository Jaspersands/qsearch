# Review: balanced central-window Krawtchouk kernel bound (2) and bulk ℓ² consequence (14)

## Disposition

**The kernel bound survives the attack.** I re-derived every step of §§1–5 by hand. No invalid step was found, and no counterfamily exists within the stated quantifiers. The constants close as written, with slack: the proof actually yields 2^15+4 where it claims 2^16.

**The bulk ℓ² consequence (14) survives as an absolute bound.**

**One statement-level repair is needed.** The native-sign sentence ("for ANY diagonal Kerr phase … single output-row sign (−1)^{K+r}") is true only for one input convention. It holds for input |K,0⟩, with all photons in mode a. For |0,K⟩ there is a residual (−1)^n inside the sum over n. That residual is harmless for pure self-Kerr χn², because it is equivalent to the relabelling χ→χ+π, but it is not a single output-row sign.

The endpoint evaluator, phase-to-count cells, normalization and sampler were not assessed. Nothing here supports a claim of speedup, hardness or a full sampler.

Every check below was done by hand. The only finite controls I evaluated are noted, and they are sanity checks, not evidence of the asymptotic regime.

## 1. Attacks attempted, cheapest first

### A1. Sign and phase convention (cheapest falsifier)

- **Case K=2, r=1** (outside the hypotheses; this checks the convention only).
  - Here φ=π/2 and A=√(2/π).
  - Exact values: V[1,0]=−1/√2, V[1,1]=0, V[1,2]=+1/√2.
  - The cosine predicts the signs −, 0, + (cos(−π), cos(−π/2), cos 0).
  - Signs and the zero match, so the convention ψ = mφ_r − πr/2 is not off by a sign or a parity.
- **Case m=0, K even.** The identity V[r,K/2] = 2^{−K/2}·√(r!s!)/(K/2)!·(−1)^{r/2}·binom(K/2,r/2) holds.
  - Its square equals 2^{−K}·binom(r,r/2)·binom(s,s/2), as stated.
  - The sign (−1)^{r/2} = cos(−πr/2). Correct.

### A2. Contour normalization (3)

- Start from [z^r]f = (1/2π)∫f(ρe^{iθ})ρ^{−r}e^{−irθ}dθ.
- The coefficients are real, so the lower half is the conjugate of the upper half. This gives (1/π)Re∫ over the upper half.
- Substitute θ = π/2 + x. Then f = (1−z²)^{K/2}((1+z)/(1−z))^m, and at x=0:
  - |1−z²| = 1+ρ²;
  - arg((1+iρ)/(1−iρ)) = 2 atan ρ = φ_r (principal value, since φ_r < π).
- Together with e^{−iπr/2}, this gives exactly e^{iψ}.

(3) is correct.

### A3. Linear term in H (does the saddle sit at x=0?)

Write Q(x) = (K/2)log((1+ζ)/(1+ρ²)) − irx, with ζ = ρ²e^{2ix}.

- Q′(0) = iKρ²/(1+ρ²) − ir = 0, using ρ²/(1+ρ²) = r/K.
- For L = log((1+w)/(1−w)) with w = iρe^{ix}: L′ = 2iw/(1−w²), so L′(0) = −2ρ/(1+ρ²) = −h. This is real.

So H′(0) = −mh is real. The real tilt is handled exactly by the shifted Gaussian G.

### A4. Strongest candidate gap: the imaginary quadratic term

- G keeps −Dx² but drops the term m·L″(0)x²/2.
- Here L″(0) = −2iρ(1−ρ²)/(1+ρ²)², which is purely imaginary with modulus ≤ h.
- Its contribution is a genuine phase/frequency correction. It has two parts:
  - roughly (1+ic/D)^{−1/2} with c/D ~ δ, i.e. a phase of order δ;
  - a phase of order (m²/K)·δ, i.e. about T^{3/2}/√D.
- These are exactly the expected semiclassical corrections: a frequency shift r→r+O(1) of size m·dφ/dr = m/√(rs) = δ, and a cubic phase.
- The proof does not ignore this term. It is charged in (8) as 2|m|hx², which produces 200|δ| + 200D|δ|³ in (11).
- With δ ≤ √(T/D) and Dδ² = m²/K ≤ T, both pieces are ≤ (1+T)²/√D.

No gap. The (1+T)² prefactor dominates the T^{3/2} cubic phase. That cubic phase is genuinely present at leading order, so the T-dependence cannot be improved for free. This is an observation, not a proved lower bound.

### A5. Exponential tilt e^{m²/K} versus prefactor

This is the place an exp(cT) loss would hide. It does not.

- **Global modulus.** I checked |1+ζ|²/(1+ρ²)² = 1 − h²sin²x and |(1+w)/(1−w)|² = (1−h sin x)/(1+h sin x). So Re H = F(−h sin x), with F(v) = (n/2)log(1+v) + ((K−n)/2)log(1−v). (4) is correct.
- **Derivative and quadratic bound.**
  - F′(v) = −(K/2)(v−u)/(1−v²), with u = 2m/K = hδ.
  - For either sign of v−u, ∫_u^v |t−u|/(1−t²)dt ≥ (v−u)²/2. Hence (5).
  - Since (K/4)h² = D, (6) follows.
- **Entropy identity (7).**
  - F(u) = (K/4)Σ_{k≥1} u^{2k}/(k(2k−1)).
  - The k=1 term equals m²/K.
  - The tail is ≤ (K/4)·u⁴/(6(1−u²)) ≤ m⁴/K³ when u² ≤ 1/3.
  - This is ≤ T²/K ≤ 1.
- **Stirling cancellation (13).** I recomputed it from scratch:
  - ρ^{−r}(1+ρ²)^{K/2} = K^{K/2}r^{−r/2}s^{−s/2};
  - (n+½)log n + (n′+½)log n′ = (K+1)log(K/2) + 2F(u) + ½log(1−u²);
  - the K-dependent logs collapse to −½log(K/2) + ½log K − ½log(rs) + ¼log(rs).
  - Result: log(P/A_r) = m²/K − F(u) − ¼log(1−u²) + E, exactly as stated.
  - All factorial arguments are integers (r, s, n, K−n), including odd K. |E| ≤ 1/(4r) is safe.

### A6. Odd K, half-integer m, and zeros

- **Reflection.** z^K f(1/z) = (−1)^{K−n}f(z), which gives V[K−r,n] = (−1)^{K−n}V[r,n].
- **Cosine side.** cos(m(π−φ) − π(K−r)/2) = cos(−ψ + π(n−K)) = (−1)^{K−n}cos ψ.
  - This is correct for half-integer m, because m − K/2 = n − K is an integer.
- **Zeros on the contour.** These occur only when ρ=1 (r=s), at x = ±π/2. There n, K−n ≥ K/4 > 0, so the integrand vanishes and F → −∞. The modulus bound holds by continuity.
- **Cosine zeros.** (12) bounds the complex J−J0 relative to J0. So the bound is absolute at cosine zeros, and no division by cos ψ occurs.

### A7. Hypothesis consequences

Assume k ≥ 2^10(1+T)² and use T/(1+T)² ≤ 1/4.

- D = rs/K ≥ r/2.
- δ² ≤ T/D ≤ 2T/r ≤ 2^{−11}, so |δ| ≤ 0.023 ≤ 1/16.
- K ≥ 2r gives T/K ≤ 2^{−13}, so |u| ≤ 2√(T/K) ≤ 0.023.
- T²/K ≤ 2^{−11}.
- n, K−n ≥ K/2 − K·2^{−6.5} ≥ K/4.

All claims hold.

## 2. Essential checked estimates (all verified)

| # | Estimate | Check |
|---|---|---|
| E1 | Q‴ = −4iKζ(1−ζ)/(1+ζ)³ | Differentiated: Q″ = −2Kζ/(1+ζ)², Q″(0) = −2D |
| E2 | \|1+ζ\| ≥ (1+ρ²)/2 on \|x\| ≤ 1/4 | Actually ≥ 0.968(1+ρ²), from 1 − h²sin²(1/4) ≥ 0.938 |
| E3 | \|Q‴\| ≤ 32D | 4Kρ²(1+ρ²)·8/(1+ρ²)³ = 32Kρ²/(1+ρ²)² = 32rs/K |
| E4 | L″ = −2iρe^{ix}(1−ρ²e^{2ix})/(1+ρ²e^{2ix})², \|L″\| ≤ 4h | Verified via L″ = −2w(1+w²)/(1−w²)² |
| E5 | (8): \|H−G\| ≤ 6D\|x\|³ + 2\|m\|h x² | 32/6 ≤ 6; 4h/2 = 2h |
| E6 | Analytic logs on the short arc | Re(1+ζ) > 0; Re(1±w) ≥ 1 − sin(1/4) > 0 |
| E7 | (9): \|e^H − e^G\| ≤ \|H−G\|(e^{Re H} + e^G) | Segment argument; G is real |
| E8 | (10): \|sin x + δ\| ≥ \|x − x_*\|/2 and the e^1 ≤ 3 factor | cos(1/4) ≈ 0.97 ≥ 1/2 |
| E9 | Moment constants 196 and 50 | e^{Re H} part: 6·4·(8D^{−3/2}·E\|z\|³ + 8\|δ\|³) ≤ 192(·); G part ≤ 4(·). Second moment: 48 + 2. E\|z\|³ = π^{−1/2}, Ez² = ½ |
| E10 | (11): 1376D\|δ\|³ + 200\|δ\| + 1176/√D | Uses \|m\|h = 2D\|δ\|; Dδ² = m²/K ≤ T; sum 2752 ≤ 2^12 |
| E11 | Long arc ≤ 3√π·√D·e^{−D/64} | sin(1/4) − 1/16 ≈ 0.185 ≥ 1/8; arc length ≤ π |
| E12 | Gaussian tails ≤ erfc(3√D/16) ≤ e^{−9D/256} ≤ 2e^{−D/64} | — |
| E13 | Sum of E11–E12 ≤ 512/√D | D e^{−D/64} ≤ 64/e; D ≥ 1 |
| E14 | (12) and the 2^14 conversion | √2·2^13 ≤ 2^14 |
| E15 | \|log(P/A)\| ≤ T²/K + 4T/(3K) + 1/(4r) ≤ 2(1+T)²/r | K ≥ 2r; then P/A ≤ 2 and \|P/A − 1\| ≤ 4(1+T)²/r |
| E16 | Final: \|V − A cos ψ\| ≤ A\|P/A − 1\| + (P/A)·A·\|J−J0\|/J0 ≤ A(1+T)²r^{−1/2}(4 + 2^15) | Within 2^16 |

## 3. Bulk ℓ² consequence (14)

The orientation is correct. Output amplitude = Σ_n V[r,n]·c_n, where n is the intermediate (column) index, m = n − K/2, and c_n = b_n e^{iθ_n}.

- **ℓ¹ norm.** Weighted Cauchy gives (Σb_n)² ≤ E[e^{X²/K}]·Σ_m e^{−m²/K}.
  - E[e^{X²/K}] ≤ 1 + ∫_0^∞ 2e^{−2t}e^t dt = 3, using Hoeffding.
  - The lattice sum of a unimodal function is ≤ max + integral = 1 + √(πK). This holds on Z − K/2 as well.
  - So the total is ≤ 3 + 5.32√K ≤ 9√K for K ≥ 1. ✓
- **Truncation tail.** Pr(|X| ≥ √(KT)) ≤ 2e^{−2T}. Its image under the orthogonal V has the same norm. ✓
- **Kernel replacement.** Σ_r |Σ_n (V−Ṽ)c_n|² ≤ ‖c‖₁²·Σ_r max_n|V−Ṽ|².
  - (2) applies to every bulk row, since Y ≥ 2^10(1+T)².
  - A_r²/r ≤ (2√2/π)K^{−1/2}r^{−3/2} for r ≤ K/2.
  - Σ_{r≥Y} r^{−3/2} ≤ Y^{−3/2} + 2Y^{−1/2} ≤ 3/√Y.
  - Reflection doubles this, giving 9·6 = 54 ≤ 64. ✓
- **Combined.** (a+b)² ≤ 2a² + 2b² gives 128C²(1+T)⁴/√Y + 4e^{−2T}. ✓ This is valid for any unit phases, so it does not depend on the Kerr phase.

**Quantitative caveats.** These are not errors.

- The bound is absolute, not relative to the bulk mass. The document correctly asserts no endpoint-mass bound.
- Achieving total error ε requires Y ≳ (128·2^32(1+T)⁴/ε²)² = 2^78(1+T)⁸ε^{−4}.
  - This is polynomial in 1/ε, but the bulk is empty unless K ≥ 2Y ≈ 2^79ε^{−4}(1+T)⁸.
  - For all smaller K, everything falls to the separately required endpoint machinery.

## 4. Native sign (repair needed)

**Rotation and single-gate sign: verified.**

- With G = a†b − b†a: d/dθ(Ua†U†) = −Ub†U† and d/dθ(Ub†U†) = Ua†U†.
- At θ = π/4: a† → (a†−b†)/√2 and b† → (a†+b†)/√2. ✓
- The output amplitude involves [z^s](1−z)^n(1+z)^{K−n} = (−1)^s c_{K−r}(n) = (−1)^{r+n}c_r(n).
- Hence B(π/4)[r,n] = (−1)^{r+n}V[r,n]. ✓

**Two-gate sign: input-dependent.**

- **Input |K,0⟩** (n=K, all photons in mode a):
  - V[n,K] = 2^{−K/2}√binom(K,n) > 0, so B[n,K] = (−1)^{n+K}b_n.
  - Total amplitude = (−1)^{r+K}·Σ_n V[r,n]e^{iθ_n}b_n.
  - The claimed single row sign holds for every diagonal phase. ✓
- **Input |0,K⟩:**
  - V[n,0] = (−1)^n b_n, so B[n,0] = +b_n.
  - Total amplitude = (−1)^r·Σ_n V[r,n]e^{i(θ_n+πn)}b_n.
  - The residual (−1)^n changes count probabilities in general.
  - For pure self-Kerr θ_n = χn² (mode a) it is absorbed exactly by χ → χ+π, since n² ≡ n (mod 2). This preserves rational phase bits.
  - For a general "ANY diagonal" phase, it is a relabelling θ_n → θ_n + πn, not a row sign.

**Required repair.** Fix the input as |K,0⟩, with K photons in the mode counted by r. Alternatively, state the relabelling θ_n → θ_n + πn for the other input. The kernel bound (2) and the ℓ² bound (14) are unaffected either way, because (14) allows arbitrary phases.

## 5. Status of claims

- **Proved (verified):** bound (2) for all integer K ≥ 1 and r, n ∈ [0,K] with k ≥ 2^10(1+T)², |m| ≤ √(KT), real T ≥ 1, all parities, with C = 2^16. Also the bulk ℓ² bound 128C²(1+T)⁴/√Y + 4e^{−2T} for any unit input phases, and the single-gate sign B(π/4) = (−1)^{r+n}V.
- **Conditional:** the two-gate row sign (−1)^{K+r} holds for input |K,0⟩ only.
- **Finite controls only:** the K=2 sign check and the m=0 binomial identity. These test conventions, not asymptotics.
- **Not addressed, and remaining proof obligations:**
  - endpoint rows r < Y or r > K−Y, which may carry essentially all the probability;
  - phase-to-count cell error;
  - normalization of the full sampler;
  - the cost of the Y ~ 2^78ε^{−4} threshold in any compiler.

**Falsifiers that would overturn this disposition:** a numerically exact evaluation of V (integer arithmetic) at some admissible (K, r, m) that violates (2) by more than 2^16·A_r(1+T)²/√k. Given the hand-verified chain, such a violation would point to an algebra slip I missed. The natural places to look are E3/E4 (where |1+ζ| ≥ 0.968(1+ρ²) leaves margin) or the Stirling cancellation (13).
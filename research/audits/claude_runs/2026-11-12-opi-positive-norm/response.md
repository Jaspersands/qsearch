# Verdict (one line)

Within its stated hypotheses, Section 4 is correct and I could not break it; Section 5 is correct under one model reading that must be confirmed. All attempted counterexamples land on the boundary of the hypotheses, and each boundary case shows which assumption is load‑bearing. The result is weaker and more trivial than the surrounding prose suggests: the uniform‑weight averaged filter with its identity term is **provably within a factor (M+1)²·e^{2sM} of π (two‑sided, pointwise)**, so an exact classical sampler is unsurprising. The implication is a sharp limit on *this* filter at bounded sM, not on tilted‑walk algorithms generally.

---

## 1. Counterexample attempts (cheapest first)

**C1. Drop the identity term (w₀ = 0).** Take P₀ = I (so s is irrelevant; set s = 0), ḡ = 1 attained on a set of π‑mass δ, G = 0 elsewhere, ν = E = 1+b, b large, weights w_M = 1 only. Then p(x) = ((1+bG(x))/(1+b))^M ≈ 1_{G(x)=1}; acceptance ≈ δ, cost 1/δ, while "poly(M)·e^{2sM}" = poly(M). **Not** a counterexample to the document (it fixes w_j = 1/(M+1)), but it proves the j=0 term is the entire mechanism. The acceptance bound is really (w₀/A)²; any source filter with w₀ = 0 or w₀ exponentially small is outside the theorem. **Obligation:** confirm the source's actual weight profile has w₀ ≥ 1/poly.

**C2. Unattained maximum with a tight normalizer.** P₀ = I, true max g* = ḡ/2, ν = E = 1+bg* (valid, paid), killed walk built with ḡ. Then ρ = (1+bḡ)/ν → 2 as b → ∞, A ≈ 2^M/(M+1), acceptance ≈ (M+1)²/4^M, cost exponential in M with s = 0. Again inside the document's exclusions, but it shows: (i) b‑independence needs attainment (or ν ≤ (1+s)(1+bḡ')/... controlled slack); (ii) the inefficiency here is an *implementation* artifact — with ḡ' = g* the same sampler is cheap — so the advice actually needed is the ratio ρ = (1+bḡ')/ν, not x* or E.

**C3. Section 5 with z ∈ F_q\{0}.** If the increment multiplier z is uniform on the nonzero elements, λ_t = (q·p_{k−1} − 1)/(q−1); eigenvalues can be negative (t in no (k−1)‑row span gives λ_t = −1/(q−1)) and the gap becomes rq/(q−1). The document's formulas require z uniform on all of F_q (including the self‑loop z = 0). **Obligation:** confirm the native update draws z from F_q.

**C4. "Does NOT sample outside T."** Overstated. Starting x ~ π (not π_T) and demanding both killed walks end in T samples the **full** normalized law of C|T⟩ (output ∝ π(x)f(x)², all x), at extra cost ~1/π(T) because the j=0 lower bound only holds on T. Not an error in the bounds, just an inaccurate scoping sentence.

**C5. Iterated use.** C^k is again a nonnegative‑weight polynomial of degree kM with w'₀ = (M+1)^{−k}; the bounds become e^{skM} and (M+1)^{2k}. The "no superpolynomial gain at bounded sM" statement holds for one application only; it says nothing about poly(k) heralded compositions, amplitude amplification, or filters embedded in phase estimation. The document mostly says this; it must not be read more broadly.

No counterexample to the claims as literally stated.

---

## 2. Independent proof of Section 4 (sampler, cost, bits, clock)

Notation: Π = diag(π), D(P) := Π^{1/2}PΠ^{−1/2} (symmetric iff P reversible). G diagonal, 0 ≤ G ≤ ḡ, X := (D(P_s)+bG)/ν, C := (M+1)^{−1}Σ_{j=0}^M X^j.

**Identity (no detailed balance needed beyond the definition of D):** D(P_s)+bG = Π^{1/2}(P_s+bG)Π^{−1/2}, hence (D+bG)^j√π = Π^{1/2}(P_s+bG)^j 1, i.e.
 C√π(x) = √π(x) · Σ_j w_j ν^{−j}((P_s+bG)^j 1)(x) =: √π(x)·A·p(x).
All quantities are nonnegative, so the computational‑basis law is q(x) ∝ π(x)p(x)². This is exactly what the paired sampler produces: P(accept | x) = p(x)² **provided the two trials draw independent degrees j, j'** (same j for both would give Σ_j (d_j/A)(R^j1)(x)² ≠ p(x)²).

**Killed kernel:** R = [P_s + bḡ·(G/ḡ)]/(1+bḡ) = (P_s+bG)/(1+bḡ); survival probability of j steps is (R^j 1)(x), and sampling j ∝ d_j = w_jρ^j, ρ := (1+bḡ)/ν, gives survival Σ_j (d_j/A)(R^j1)(x) = p(x). ✔

**Diagonal bound:** ⟨√π|D(P_s)|√π⟩ = Σπ_xP_s(x,y) = 1 ⇒ E ≥ 1+bE_πG ≥ 1. At x* with G(x*) = ḡ: E ≥ (D+bG)_{x*x*} = P_s(x*,x*)+bḡ ≥ 1−s+bḡ. So ρ ≤ (E+s)/ν ≤ 1+s/E ≤ 1+s and A ≤ ρ^M ≤ e^{sM}. Sharper and uniform in b: ρ ≤ 1 + s/max(1, 1−s+bḡ), maximized at bḡ = s. (Also note ν = 1+bḡ is always a valid normalizer since ‖D(P_s)‖ ≤ 1, giving ρ = 1, A = 1, cost (M+1)² with no promise at all — the e^{sM} is purely the price of using a ν between E and 1+bḡ.) ✔

**Zero‑degree lower bound:** p(x) ≥ (d₀/A)(R⁰1)(x) = 1/((M+1)A) ≥ e^{−sM}/(M+1); acceptance Σ_xπ(x)p(x)² ≥ e^{−2sM}/(M+1)². ✔

**Two‑sided law bound (stronger than anything stated):** q(x)/π(x) = p(x)²/Σ_yπ(y)p(y)² ∈ [(M+1)^{−2}A^{−2}, (M+1)²A²]. So for any event S, q(S) ≤ (M+1)²e^{2sM}π(S). This is the real content: the filter is a bounded reweighting of π.

**Finite bits/clock (exact law with abort, not an approximate law):** Let L bound the bitlength of s, b, ḡ, ν and of each G(x) returned by the paid oracle. With ρ = N/D, set c_j = N^jD^{M−j}, S = Σc_j (bitlength O(ML)); sample j by a uniform integer in [0,S) (rejection on ⌈log₂S⌉ bits, expected ≤ 2 draws). Each Bernoulli (1/(1+bḡ), G(x)/ḡ) is a rational a/c with O(L) bits, sampled the same way. Per outer trial: 2 degree draws, ≤ 2M P_s steps, ≤ 2M G‑evaluations and Bernoullis; expected bits O(M(ML+L)) plus the paid π/P_s samplers. Cap outer trials at N_max = ⌈(M+1)²e^{2sM} ln(1/ε)⌉ and cap each internal rejection loop at K = ⌈log₂(2M·N_max/ε)⌉ attempts; abort (report failure) on any cap. Because trials are i.i.d. and abort is "report, not restart", the output conditioned on no abort is **exactly** q; total abort probability ≤ 2ε. This needs the native samplers to be exact with bounded or geometric‑tail cost; for expected‑cost‑only samplers the document's global‑cutoff caveat stands. Expected work O(M³e^{2sM}) elementary steps plus charged oracle calls. ✔

## 3. Projected law and marked amplitude

For |T⟩ = Σ_{x∈T}√(π(x)/π(T))|x⟩: Π^{−1/2}|T⟩ = π(T)^{−1/2}1_T, so C|T⟩(x) = √(π(x)/π(T))·f(x) with f(x) = Σ_jw_jν^{−j}((P_s+bG)^j1_T)(x), 0 ≤ f ≤ A (row sums ≤ (1+bḡ)^j). Hence ‖Π_SC|T⟩‖ ≤ A√(π(S)/π(T)) ≤ e^{sM}√(π(S)/π(T)) for any S ⊆ T (indeed for any S). ✔ Sampling: x ~ π_T, two independent killed walks, test only the **final** state of each for T‑membership (intermediate excursions out of T are allowed, matching (P_s+bG)^j1_T); acceptance f(x)²/A², output ∝ π_T(x)f(x)² ∝ |Π_TC|T⟩(x)|². The j=0 term gives f ≥ 1/(M+1) on T, so the same acceptance bound holds. ✔ Two‑sided: q_T(x)/π_T(x) ∈ [(M+1)^{−2}A^{−2},(M+1)²A²].

Contraction: D(P_s)+bG ⪰ (1−2s)I ⪰ −I and ≤ E ≤ ν ⇒ ‖X‖ ≤ 1, ‖C‖ ≤ 1 when ν ≥ E. Note ν ≥ E is needed only for this contraction/heralding statement, not for exactness of the sampler.

Remark (observation, not a theorem about the source): an LCU block‑encoding of X built from a unit‑norm encoding of D and a G/ḡ'‑encoding has subnormalization exactly ρ, so its naive heralded success probability for C is ‖C√π‖²/A² — identical to the classical acceptance. Any quantum gain for a single application must come from amplitude amplification (quadratic) or from a better‑normalized block encoding, which requires its own paid spectral knowledge.

## 4. Charging

- Sampler execution needs: π sampler, P_s updates, G‑oracle, membership in T / π_T sampler, and the numbers (ν, b, ḡ', M, s). It never needs x*, E, or the attainment fact.
- The cost A(ν,b,ḡ',M) is **computable from the paid description**; attainment of ḡ' is merely a sufficient condition for A ≤ e^{sM}. The quantum filter needs the same ν and some G‑normalizer ḡ' ≥ max G, so this advice is symmetric and correctly charged. An unverified "attained" promise is an instance promise (e.g., existence of a perfect‑score solution); the document correctly excludes the unattained/under‑normalized case rather than claiming it.
- The REG inequality sM ≤ log(1/(1−η))/(rγ)+s and "Theorem 4.6 has S ⊆ T_η ⊆ T" cannot be verified from the supplied evidence; they are the bridge to the source and remain open obligations.

## 5. Section 5 (anchor‑mixer spectrum): independent check

Model reading required: state ∈ F_q^k (coefficients), m ≥ k distinct evaluation points, A a uniform (k−1)‑subset, D_A the degree‑<k polynomial vanishing on A (1‑dimensional space), update coeff ← coeff + z·coeff(D_A) with z uniform on F_q. Then:
- Characters χ_t(c) = ω^{tr(t·c)}; averaging z gives λ_t = Pr_A[t·coeff(D_A) = 0]. Since {c : c·v(a)=0 ∀a∈A} = span(coeff D_A) (dimension k−(k−1) = 1), double annihilation gives t ⊥ coeff(D_A) ⇔ t ∈ span{v(a): a∈A}. ✔ Eigenvalues are probabilities, so ≥ 0; P₀ is symmetric (z ↦ −z), uniform π. ✔
- "At most one new point": if t ∉ span v(B) and both a, a' ∉ B made it enter, then c·v(a) − c'·v(a') ∈ span v(B) with c,c' ≠ 0, a nontrivial dependence among j+2 ≤ k distinct Vandermonde rows — impossible. ✔
- Coupling uniform (j+1)‑subset = uniform j‑subset + uniform point from the m−j remaining gives p_{j+1} ≤ p_j + (1−p_j)/(m−j); the right side is increasing in p_j, and substituting p_j ≤ j/m yields exactly (j+1)/m. ✔ (Tight for t = v(a_i): membership ⇔ a_i ∈ A, probability (k−1)/m.)
- Gap of P₀: 1 − (k−1)/m = (m−k+1)/m; of P_s: s(m−k+1)/m; P_s ⪰ (1−s)I. ✔ No bits/clock issues; it is exact algebra. Falsifier: any instance where the update draws z ≠ 0 only, uses |A| ≠ k−1, or non‑distinct/fewer than k points — then the formula changes (C3).

## 6. Limited implications (what is and is not shown)

Shown: for the uniform‑weight degree‑M averaged filter with identity term, any ν ≥ E and any valid G‑normalizer ḡ' with ρ = (1+bḡ')/ν, the measurement law of C√π (resp. Π_TC|T⟩) is within (M+1)²A² of π (resp. π_T) pointwise, is exactly classically samplable at expected cost O(M³A²) + charged oracle calls, and A ≤ e^{sM} when ḡ' is attained. So at sM = O(log input) this one filter cannot concentrate on any set beyond a polynomial factor over the paid starting measure; the single‑application heralded marked amplitude is ≤ e^{sM}√(π(S)/π(T)).

Not shown and not to be claimed: anything about w₀ → 0 or sM growing filters, iterated/amplified use (C5), non‑nonnegative or phase‑bearing inputs, use of X inside phase estimation of E, or generic OPI/tilted‑walk advantage. Section 5 gives a mixing baseline only; it is not a hitting‑time or log‑Sobolev statement.

**Decisive falsifier for the bridge to the source:** exhibit the source's actual C (weights, ν, degree, input state) and a finite instance where q(S)/π_T(S) > (M+1)²e^{2sM}; by the two‑sided bound this is impossible for the analyzed C, so such an instance would prove the source's filter is not the one analyzed (most likely w₀ ≈ 0, total degree ≫ M, or a different D(P) convention).
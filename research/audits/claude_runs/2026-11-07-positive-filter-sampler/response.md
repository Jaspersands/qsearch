# Verdict on the TWO-KILLED-WALK sampler: the exactness and polynomial-cost claim holds, with corrections

**No counterexample exists within the stated hypotheses.** The claim holds under these conditions:

- P is reversible.
- G is a diagonal multiplier in the same basis as the chain's state space.
- w_j ≥ 0 with not all zero, b ≥ 0 and ν > 0.
- The two trials are fully independent, including independent draws of the degree j.
- The samplers for π and for P-updates are exact.

Under those conditions the accepted law is exactly the computational-basis law of C|√π⟩/‖C|√π⟩‖. The expected bit cost is polynomial when M = poly and bM = O(log n). The constants below are corrected or tightened; none of the original bounds is false.

**Failure modes** (each is a falsifier if the implementation or the definitions deviate):

1. **Shared degree j between the two trials.** The acceptance probability becomes Σ_j (d_j/A)(R^j𝟙)(x)², which is not p(x)². The output law is then wrong.
2. **Shared path randomness.** Acceptance becomes p(x), not p(x)². The output is then ∝ π·p, the wrong power.
3. **Non-reversible P with D defined as √(P(x,y)P(y,x)).** Take the directed 3-cycle with π uniform. Then D = 0, but the sampler simulates Π^{1/2}PΠ^{-1/2} = P. With nonconstant G the two laws differ. This is excluded by the reversibility hypothesis.
4. **Approximate π-sampler (for example, MCMC to mixing).** Exactness is lost. With TV error δ, the output TV error is at most 3δ / (2(t₀^{2M} − δ)). So δ must be much smaller than t₀^{2M}.
5. **A different native input.** If the native "coherent stationary state" is a Szegedy edge state Σ√π(x)|x⟩|p_x⟩, or uses another basis or encoding, the identity below must be re-derived. It is proved only for |√π⟩ = Σ_x √π(x)|x⟩.

# Proof

## Access assumptions

- **(A1)** Exact samplers for π and for y ↦ P(y,·), with expected bit cost c_π and c_P(y).
- **(A2)** Exact rational G(y) ∈ [g₀, 1], with evaluation cost c_G(y).
- **(A3)** The rationals b = β₁/β₂, ν = n₁/n₂ and w_j = a_j/c_j have bitlength at most L.
- If π(x) = 0 for some states, restrict to supp π. This is closed under P, because π(y) = Σ_x π(x)P(x,y).

## 1. Identity

Let Π = diag(π). Use D = Π^{1/2} P Π^{-1/2}.

- Under detailed balance this matrix is symmetric and equals √(P(x,y)P(y,x)).
- It also equals Π^{-1/2} Pᵀ Π^{1/2}, so the row/column convention is immaterial.

G is diagonal, so it commutes with Π^{±1/2}. Therefore (D + bG)^j = Π^{1/2} (P + bG)^j Π^{-1/2}. Since Π^{-1/2}|√π⟩ = 𝟙,

C|√π⟩ = Σ_x √π(x) · [Σ_j w_j ν^{-j} ((P + bG)^j 𝟙)(x)] |x⟩.

## 2. The survival trial computes p

Define R(x,y) = [P(x,y) + b·G(x)·δ_{xy}] / (1 + b).

The described step does the following from the current state y:

- With probability 1/(1+b) it moves according to P(y,·), with no kill.
- Otherwise it stays and survives with probability G(y).

Summing the product of R entries over paths gives P_x(survive j steps) = (R^j 𝟙)(x). Self-loops in P are handled correctly because both contributions add in R(y,y).

Let j be drawn with probability d_j/A, where d_j = w_j((1+b)/ν)^j and A = Σ d_j > 0. The survival probability is then

p(x) = Σ_j (d_j/A)(1+b)^{-j} ((P + bG)^j 𝟙)(x) = A^{-1} Σ_j w_j ν^{-j} ((P + bG)^j 𝟙)(x).

Combining with Section 1, C|√π⟩ = A Σ_x √π(x) p(x) |x⟩.

## 3. Exact output law

Two fully independent trials from the same x both survive with probability p(x)². Hence:

- P(accept, x) = π(x) p(x)².
- The acceptance probability is Z = E_π[p²].
- Conditioned on acceptance, q(x) = π(x)p(x)²/Z.

This is exactly A²π(x)p(x)² / ‖C√π‖², the Born law of the normalized state. ∎

Check: for b = 0, p ≡ 1 and q = π. This is correct, since P𝟙 = 𝟙.

## 4. Survival and likelihood-ratio bounds (corrected constants)

From any state, one R-step survives with probability (1 + bG(y))/(1 + b) ≥ t₀ = (1 + bg₀)/(1 + b). Hence t₀^M ≤ p ≤ 1, and Z ≥ t₀^{2M}.

The inverse of t₀ satisfies

1/t₀ = 1 + b(1 − g₀)/(1 + bg₀) ≤ 1 + b(1 − g₀) ≤ e^{b(1−g₀)}.

So t₀^{-2M} ≤ exp(2(1 − g₀)bM).

The likelihood ratio is q/π = p²/Z, which lies in [t₀^{2M}, t₀^{-2M}]. The lower end gives t₀^{2M} ≥ 1 − 2M(1 − t₀) ≥ 1 − 2(1 − g₀)bM/(1 + b).

Total variation:

- TV(q, π) = Σ_x π(1 − q/π)₊ ≤ 1 − t₀^{2M} ≤ 2(1 − g₀)bM/(1 + b).
- This is sharper than the stated e^{2(1−g₀)bM} − 1, which is also valid.

g₀ > 0 is not needed for polynomiality. Since t₀ ≥ 1/(1+b) always, the cost is at most e^{2bM} even with g₀ = 0.

**Corollaries:**

- q(S) ≤ e^{2(1−g₀)bM} π(S). For g₀ = 1/2 this is e^{bM}π(S), as stated.
- Let C/α be a block encoding with α ≥ ‖C‖. The marked heralded amplitude is ‖Π_S C√π‖/α = √q(S) · ‖C√π‖/α ≤ √q(S). This bounds only this use of the filter.
- The claim "q/π = 1 + O(Λ⁻²)" for PRODUCT holds if and only if PRODUCT gives bM = O(Λ⁻²). PRODUCT is not stated in the context, so this remains a proof obligation for the parent.

## 5. Expected bit cost

Rounds are i.i.d. and the stopping round N satisfies E[N] = 1/Z ≤ t₀^{-2M}. By Wald's identity, E[total cost] = E[N] · E[cost of one round].

To bound per-step costs, couple the killed walk with the unkilled lazy chain (P + bI)/(1 + b). That chain preserves π, and each trial marginally starts from π. So the expected state-dependent cost per step is at most E_π[c_P]/(1+b) + bE_π[c_G]/(1+b). Average-case cost under π therefore suffices; no worst case over states is needed.

**Exact coins.** Clear denominators to get integers

D_j = a_j (β₁ + β₂)^j n₂^j β₂^{M−j} n₁^{M−j} · lcm(c)/c_j,

each of bitlength O(ML). Then:

- **Sampling j:** draw U uniform on [0, 2^k), where k is the bitlength of ΣD_j. Reject if U ≥ ΣD_j (probability < 1/2), then locate j by prefix sums. This is exact.
- **Bernoulli coins:** Bernoulli(β₂/(β₁ + β₂)) and Bernoulli(G(y)) are sampled the same way.

Each round costs O(M) coins of poly(ML) bits, plus c_π, plus O(M) expected update and G costs. Hence

E[total] ≤ e^{2(1−g₀)bM} · poly(M, L) · (c_π + E_π c_P + E_π c_G).

This is polynomial under the stated scaling.

## 6. Bounded cost (approximate law)

- **Outer cap.** Cap the outer rounds at T = ⌈K ln(1/ε)⌉, with the rational K = ⌈(1 + b(1 − g₀))^{2M}⌉ ≥ t₀^{-2M}. Overall failure has probability at most (1 − Z)^T ≤ ε; on failure, output anything.
- **Internal rejection coins.** Each internal rejection coin is capped at ⌈log₂(N_c/ε)⌉ attempts, where N_c is the total number of coins. A union bound then gives an additional TV error of at most ε.
- **External samplers.** Restarting a timed-out Las Vegas sampler for π or P biases its output, so this must not be done. If only expected-cost bounds hold, Markov truncation gives cost poly(1/ε). A log(1/ε) dependence needs worst-case or geometric-tail bounds on those samplers.

## Remaining obligations for the parent

1. Confirm that the native state is Σ√π(x)|x⟩ in the chain basis, and that G is diagonal in that basis.
2. Confirm that the π-sampler is exact, or bound its error δ against t₀^{2M}.
3. Verify bM = O(log n), and bM = O(Λ⁻²) for the 1 + O(Λ⁻²) claim, from PRODUCT.
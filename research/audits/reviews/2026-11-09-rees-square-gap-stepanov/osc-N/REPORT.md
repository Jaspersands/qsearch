# OSC part (N): the C1 count — identity, barriers, Theorem C

AI-only (2026-11-09). A subagent wrote this report and the parent saved it. Pending human review.

**Referee (independent AI agent, scripts in `referee/`):**
- Theorem C: CORRECT WITH FIXES. The fixes are to the write-up and are applied below. All
  thresholds and B ≤ 2.05 at (4,641) were recomputed independently and match.
- Barrier 2.1: CORRECT. It covers only certificates that bound every e ≠ 0 by its modulus;
  signed certificates such as PW_pair escape it.
- Barrier 2.3: the narrow moment-only statement is CORRECT. The broad claim "≤κ−1 rows of
  information = Λ₁..Λ_{κ−1}" is ARGUED ONLY and false in its natural readings, so it is
  restated below as a conjecture. Scripts and outputs are in this folder. Every run used
`nice -n 19 /opt/anaconda3/bin/python -I` with κ ≤ 6, except formula-only evaluations.

Convention: χ⁰(0) = 1 and χ^s(0) = 0. ker is the set of e ∈ Z_κ^{κ×κ} with all row and column sums
≡ 0, so |ker| = κ^{(κ−1)²}.

## 1. Kernel identity [proved; computed]

- (I1) κ^{−(κ−1)²} Σ_{e∈ker} S_e = Σ_{(α,β)} κ^{c(G)−1−z}[P separable on G]. Here G is K_{κ,κ}
  minus the z zero cells, and c(G) counts its components.
  - Pointwise the kernel sum is |ker_G|·[P ∈ (ker_G)^⊥]. The annihilator is the image of
    (U,V) ↦ U_i+V_j (double annihilator over Z_κ).
- (I2) The same quantity equals Σ_α Σ_{c ∈ Z_κ^κ/diag} b_c(α)^κ. Buckets are profiles
  (ind(α_j−t))_j; a coordinate with α_j = t is uniformised.
  - Corollary: Σ_{e∈ker∖0} S_e ≥ 0, by the power mean.
- (I3) N₁^{lab} = p(p−1)N₁ = Σ_{S distinct} Σ_c (b_c(S))_κ, counting t ∉ S.
- [computed] (I1) = (I2) = kernel sum at (3,7), (3,13), (4,5). (I3) gives 168 and 3276 at p = 19
  and 31, matching types/bf_c1.py. Files: kernel_identity.py and .out.

## 2. Barriers

**2.1 O1-N [proved].** Any certificate built from bounds |S_e| ≤ B_e on the full space, plus an
upper bound D⁺ on the degenerate mass, has value at most 2(μ' − W_deg) − N₁^{lab}. So it fails
whenever W_deg ≥ μ' = p^{2κ}κ^{−(κ−1)²}.
- A rigorous lower bound on W_deg comes from the strata "all α equal", "all β equal" and "exactly
  one coincident pair" (the last via Jensen).
- This gives a crossing P_N ≈ (κ−1)κ^κ, which is above pigeonhole:

  | κ | pigeonhole | P_N |
  |---|---|---|
  | 3 | 20 | 37 |
  | 4 | 195 | 641 |
  | 5 | 2504 | 11121 |
  | 6 | 38885 | 212641 |
  | 12 | 8.2·10¹² | 9.4·10¹³ |

  Source: barriers.py, barriers_o1n.out.
- This corrects the parent's hope. The degenerate strata do add positive mass, but N₁ = W_full −
  W_deg, and the triangle inequality counts W_deg twice.

**2.2 Open stratum [argued; computed at κ = 3].**
- No O1 witness was found. The (C1) class is always the smallest twisted class: 0.24, 0.47, 0.72
  of the mean at p = 19, 31, 61.
- The κ = 3 data are in twisted_classes_k3.py and .out.
- Mechanism [argued]: the n₄ = (κ−1)C(κ,2)² kernel 4-cycle frequencies each equal
  −S'_0/p·(1+O(κ/p)), by the cross-ratio bijection.
- Fit [computed, heuristic law]: N₁/μ₁ ≈ exp(−n₄/(p−2)). It holds within 0.5% at κ = 3 for p ≥ 97,
  and within ±5% at κ = 4 for p ≥ 197. Below n₄ it plateaus near 0.2–0.3 at κ = 4.
  File: c1_bias_vs_4cycles.out.

**2.3 Moment-only barrier (restated after referee).**
- [proved] Let Λ_m = E_S Σ_c (b_c)_m. If Λ_m/D are the factorial moments of a nonnegative law on
  {0..κ−1}, then no certificate built from Λ₁..Λ_{κ−1} alone can decide. Theorem C is such a
  certificate.
- [conjecture; was mislabelled "argued"] Every certificate built from kernel frequencies
  supported on ≤κ−1 rows fails in the same range.
  - Why it is not a theorem: S-dependent weights already determine b_c(S). A real barrier would
    need an exchangeable κ-row extension of the (κ−1)-row marginals with zero separable mass,
    which has not been constructed.
- [computed] This is realizable at κ = 4 for every prime 37–97, although (C1) configurations exist
  from 41. At κ = 3 it is realizable at 13. File: barriers_lp.out.
- [argued] In general the barrier sits at λ = (p−κ)/κ^{κ−1} ≈ 1.
- Consequence [conjectural, given the restatement above]: in the OSC regime λ ≪ 1, (N) would need
  full-support kernel information, of the same kind as (H). What is proved is narrower: moment-only
  certificates like Theorem C cannot reach that regime.

**2.4 Jensen cap [proved].** Positivity-only certificates cannot go beyond λ > ((κ−2)!)^{1/(κ−2)}
≈ κ/e.

## 3. Theorem C: (C1) existence below pigeonhole [proved; referee: CORRECT WITH FIXES]

**Definition.** Λ_M = E_S Σ_c (b_c(S))_M.
- S runs over the (p)_κ ordered distinct κ-tuples in F_p.
- Buckets are profiles (ind(s_j−t))_j in Z_κ^κ modulo the diagonal, for t ∈ F_p∖S.
- ∞ is excluded on both sides. That is harmless, since PGL₂ moves any (C1) configuration to
  an all-finite one.

**Double counting.** "All u ∈ U have the same S-profile" and "all s ∈ S have the same class
relative to U" both mean that the M×κ index matrix is separable. Hence
Λ_M = (p)_M/(p)_κ · avg_U Σ_d (n_d(U))_κ. The κ^{M−1} classes n_d(U) partition F_p∖U.

Λ_M ≥ L_M = (p)_M G(p−M, κ^{M−1})/(p)_κ, where G is the balanced-split minimum of Σ(n_d)_κ. This
needs no Weil.
- Λ_2 is exact, via the two-point bijection.
- U_m, for m ≥ 3, is an upper bound from Weil.
- If no bucket has κ points, then (b)_M ≤ (κ−1−m)_{M−m}(b)_m bucket by bucket.
- So L_M > (κ−1−m)_{M−m}U_m certifies a (C1) configuration.
- Quantitative form: E_S Σ(b)_κ ≥ (κ−M)![L_M − (κ−1−m)_{M−m}U_m].

First prime certified (certified at every larger prime tested), from bucket_cert.py:

| κ | certified | pigeonhole | true first (C1) prime |
|---|---|---|---|
| 3 | 19 (tight) | 31 | 19 |
| 4 | 137 | 197 | 41 |
| 5 | 1451 | 2521 | — |
| 6 | 20233 | 38891 | — |

- The κ ≤ 6 rows use no Weil: every best (m,M) has m ≤ 2, and with Weil disabled the first
  primes are unchanged (referee, `referee/noweil.py`).
- "Pigeonhole" in the κ = 3 row is the first prime above the bound 20.
- Asymptotics [argued at leading order; bookkeeping not written out]: λ* ≈ κ/e without Weil,
  and κ/(2e) with Weil at m ≈ κ/2. So for all large κ, (C1)
  exists for p ≥ (1+ε)κ^κ/(2e). The factor 2e is approached slowly: pigeonhole/certified is 4.06
  at κ = 40.
- Quantitative (N), proved: B ≤ 2.05 at (4, 641); B ≤ 8.6 at (5, 3461); B ≤ 9.9 at (6, 50023).
  Nothing is proved at κ = 7, where λ = 0.31.

## 4. Corrections

- The "ideal term-by-term" bound for (N) is about κ times below pigeonhole, not "at pigeonhole
  scale".
- κ = 5 near p ≈ 3·10³ has λ ≈ 4.8, so it is not the λ ≪ 1 regime. The first real test is κ = 7
  (T_strong(1) ≈ 3.6·10⁴, λ ≈ 0.31).

## 5. Claim gates (stay false)

- OSC proved.
- (N) proved for any p with λ < 2.
- Any change to T_A or the E_2 tables.
- Theorem C gives contractions. It does not: it gives (C1) existence only.

## 6. Next step

Monte Carlo test of (N) at κ = 7: `mc_N1.py 7 36037 10000` and `mc_N1.py 7 12041 20000`. The parent
launched these; output goes to mc_N1_k7.out. Pass: R = N₁/μ₁ stays within a constant of
exp(−2646/p).

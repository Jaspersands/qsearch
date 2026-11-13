# Square gap, constructive route: structured families for prime κ

AI-only report (2026-11-13), pending human review. No existing file was edited. Scripts and
outputs are in `2026-11-13-rees-square-gap-families/`. Every run used `nice -n 19`, a single
thread and under 5 MB of memory.

Read first: `appendix-schedule2.tex` lines 79–480 and 482–720; the square-gap attack review
(2026-11-05) §§0–6, including the §4 square-root heuristic; the Stepanov review (2026-11-09)
§0, §3 and §9 with `osc-N/REPORT.md` §3 (Theorem C); and TH5 (2026-11-04) §§0–2, which
classifies every cell-permuting linear ansatz.

Notation as in the appendix. κ is an odd prime and p ≡ 1 (mod κ). ξ = g is the least primitive
root, I(x) = ind(x) mod κ and ζ = g^{(p−1)/κ}, so c := I(ζ) ≡ h (mod κ); c = 0 exactly when
p ≡ 1 (mod κ²). In the PGL₂ language of Stepanov Theorem A, a contraction is a configuration
(S, T, z) on P¹(F_p) with S = {α_j}, T = {−β_i} and chart point z. It must satisfy (C1): in
some (equivalently every) chart, I(s − t) = u(s) + v(t) on the nonzero cells. It must also
satisfy (C2): in the chart z, the twisted labels u(s) − I(s − z) and v(t) − I(t − z) are
bijections onto Z_κ, and some nonzero cell gets label (0,0).

## 0. Verdict

- **Negative for the brief's goal.** Every structured family below that collapses coset
  conditions does so by Kummer-rank collapse along 1-parameter-group orbits. None gives a
  Weil-provable threshold below T_A, let alone below κ^κ. The best one-variable Weil
  thresholds they give are ≈ (κ−1)²κ^{2κ}, about T_A². Their square-root thresholds κ^{2c/v}
  are also all above κ^{κ+1} (§5).
- **Empirically they help only a little.** Up to the limits searched:
  - At κ = 5, F3 (open geometric progressions, 2 parameters) succeeds at every prime from 761 to
    12941. The orbit family F2 (2 parameters, all charts) fails as late as 5231. The true last
    exceptional prime is 181, and T_A(5) ≈ 1.27·10⁴.
  - At κ = 7, F2 still fails at sampled primes up to 1.01·10⁶. F3 fails at 5 of 8 sampled primes
    near 6·10⁴. The true last exceptional prime is
    3221, and T_A(7) ≈ 4.94·10⁶.
  - The heuristic thresholds of all these families are κ^{κ−1+o(1)} [heuristic, §4]. That is
    below κ^κ by a factor of about κ and above the observed κ^{(κ+1)/2} by about κ^{(κ−3)/2}.
  - So they meet the brief's lead criterion ("slower than κ^κ") only technically, and they are
    not provable.
- **Proved (new in this form, elementary):**
  - Lemma 1: for prime κ, every configuration with an order-κ Möbius symmetry is PGL₂-equivalent
    to the orbit family S = μ_κ, T = tμ_κ.
  - Lemma 2: in a fixed-point chart this is TH5's shift family with o = κ; in every other chart
    it lies outside TH5's scope.
  - Lemma 3: the constant-cell loophole of the attack review §4 yields nothing under Weil. A cell
    pre-tuned by the Kummer substitution t = r + c u^κ reproduces the bound of
    `lem:app-s2-weil-count` to within κ^{−ℓ−1}√p.
  - Proposition 4: explicit Weil thresholds for F1 and F3, ≥ (κ−1)²κ^{2κ}.
- **Accounting identity [heuristic, §6].** Consider the family whose S and T are each a union
  of m progressions with a common ratio. It has c/v = κ − m/2 + O(1). Every Kummer-rank collapse
  raises c/v. The unstructured problem (m = κ, c/v = (κ+1)/2) minimises it. Collapsing cells
  saves conditions only in proportion to parameters lost, times 2. This is why the structured
  route cannot beat the square-root limit.
- **Two computed side observations.**
  - Solutions in the orbit family come in correlated clumps: 2κ parameters t per (C1) orbit
    configuration, and κ charts z per orbit. A naive first moment that ignores the clumping puts
    F2's threshold at κ^{κ/2+κ/ln κ}. The correct heuristic is κ^{κ−1+o(1)}, because a solution
    needs a (C1) orbit configuration first.
  - The generic-chart contribution is erratic. At κ = 5, (c, θ) = (0, 0) and (3, 0), (3, 3)
    gave no generic-chart solution, against 22 and 140 predicted (§4.2; unexplained).
- Nothing changes in the paper, E₂, T_A or any table; the claim gates stay false (§8).

## 1. The accounting used throughout

A family with v free parameters over F_p and c coset conditions (in κ-units: the log_κ of the
inverse probability that a random point satisfies them) has
- first moment p^v κ^{−c}, divided by the size of the symmetry clump of each solution;
- square-root certificate threshold κ^{2c/v} times Betti factors (attack review §4,
  [heuristic]).

Conditions that hold automatically on the family are not counted. But Lemma 3 shows that
automatic conditions made by Kummer substitution are paid back in the Weil error. The
bijectivity part (C2) costs 2 log_κ(κ^κ/κ!) ≈ 2κ/ln κ κ-units when it is not automatic.

## 2. The families

| family | definition (chart ∞ unless stated) | v | c (κ-units) | (C2) |
|---|---|---|---|---|
| F0 full problem | α, β free | 2κ−2 | κ²−1 | built in |
| F1 orbit, fixed chart (= TH5 shift, o = κ) | α_j = ζ^j, β_i = −tζ^i, relabelled affinely | 1 | κ − 2 + log_κ(κ/(κ−2)) | automatic iff θ ∉ {0, c} |
| F2 orbit, all charts | S = μ_κ, T = tμ_κ, z ∈ P¹ ∖ (S∪T); α_j = 1/(ζ^j − z), β_i = −1/(tζ^i − z) | 2 | (κ−2) + 2 log_κ(κ^κ/κ!) | rainbow in z |
| F2P | the case t ∈ μ_κ of F2: T = S, κ zero cells, fixed cyclotomic (C1) data | 1 | (C1) is Chebotarev data | rainbow in z |
| F3 open progressions | α_j = ρ^j, β_i = −tρ^i (j, i < κ), ρ of order ≥ κ | 2 | 2κ − 3 + log_κ(κ/(κ−2)) | automatic iff θ ∉ {0, I(ρ)} |
| F3′ non-split torus | the same with ρ in the norm-one group of F_{p²}, via the Cayley chart (§6.3) | 2 | as F3 | as F3 |

Conditions:
- In F1 and F2, (C1) is "F_t(d) := I(ζ^d − t) is affine in d ∈ Z_κ" with slope θ. Then
  I(ζ^j − tζ^i) = ic + F_t(j−i) is separable.
- In F3, (C1) is "H(d) := I(ρ^d − t) is affine for d ∈ [−(κ−1), κ−1]" (2κ − 1 values).

## 3. Proved statements

**Lemma 1 (order-κ symmetry forces the orbit family) [proved].** Let κ ≥ 3 be prime, p ≡ 1 (mod κ),
and let g ∈ PGL₂(F_p) have order κ with g(S) = S and g(T) = T for κ-sets S, T ⊂ P¹(F_p). Then for
some h ∈ PGL₂(F_p) and t ∈ F_p^×, h g h^{−1} is x ↦ ζx for a primitive ζ ∈ μ_κ, h(S) = μ_κ and
h(T) = tμ_κ.

*Proof.* Take a lift G ∈ GL₂(F_p). If G has a repeated eigenvalue and g ≠ 1, then g is unipotent,
of order p ≠ κ. If its eigenvalues a, a^p lie in F_{p²} ∖ F_p, the order of g divides p + 1; then κ
divides both p − 1 and p + 1, hence 2, which is impossible. So G is F_p-diagonalisable,
g ~ (x ↦ (a/b)x), and a/b has order κ. The orbits of x ↦ ζx on P¹(F_p) are {0}, {∞} and the cosets
xμ_κ. A κ-set that is a union of orbits has size e + κm with e ∈ {0,1,2}. Since κ ≥ 3 is odd,
κ ∤ κ−1 and κ ∤ κ−2, so S = sμ_κ and likewise T = t′μ_κ. Scaling by s^{−1} commutes with g. ∎

Since (C1) is PGL₂-invariant and a chart change only twists the labels (Stepanov Theorem A), and
affine maps preserve contraction-ness up to relabelling (scaling shifts every index by I(a),
absorbed by j ↦ j + I(a)), every contraction with such a symmetry is an F2 point (t, z).

**Lemma 2 (where F2 sits) [proved].**
1. For t ∉ μ_κ, (C1) for (μ_κ, tμ_κ) holds iff F_t is affine on Z_κ. Indeed
   I(ζ^j − tζ^i) = ic + F_t(j − i), and a function of j − i is separable iff
   F_t(d + e) − F_t(d) is independent of d, that is, iff F_t is affine.
2. In the charts z ∈ {0, ∞} (the fixed points), the labels are u_j = F_t(j) and
   v_i = i(c − θ) + const. So (C2) holds iff θ ∉ {0, c}. This is exactly TH5 Theorem 2.2 with
   o = κ and λ a primitive element of μ_κ (a power of ζ fixed by θ), after translation.
3. For z ∉ {0, ∞}, the symmetry g_z (the conjugate of x ↦ ζx) maps cells to cells times the
   non-constant separable factors det/((γa + δ)(γb + δ)). Equivalently M ↦ (M ∘ π)·(u ⊗ v)
   with u, v non-constant. TH5 §2 considers only M ↦ λ·(M ∘ π) with λ constant, so these points
   are outside its classification.
4. Moreover T-side bijectivity at z ⇔ S-side bijectivity at t/z: the involution x ↦ t/x
   exchanges S and T. The S-side condition reads
   j ↦ j(θ − c) − I(1 − zζ^{−j}) bijective. This is a direct computation with −1 ∈ Q_0 (κ odd).

**Lemma 3 (Kummer substitution gains nothing under Weil) [proved].** Pre-tune the condition
t − r₀ ∈ c₀Q₀ by putting t = r₀ + c₀u^κ, and keep ℓ further conditions c_k(t − r_k) ∈ Q_{m_k}
(r_k ≠ r₀ distinct). Then N_u = κ·N_t exactly, where N_t counts t with all ℓ + 1 conditions.

In u, condition k is a character of c₀u^κ + (r₀ − r_k). This has κ distinct roots, because μ_κ ⊂ F_p
and r_k ≠ r₀. A frequency of support size s therefore has κs distinct roots, and Weil gives
≤ (κs − 1)√p. The resulting bound is
|N_u − pκ^{−ℓ}| ≤ κ^{−ℓ}Σ_s C(ℓ,s)(κ−1)^s(κs − 1)√p + O(ℓ) = (ℓ(κ−1) − 1 + κ^{−ℓ})√p + O(ℓ).
Divided by κ, the error for N_t is (ℓ(1 − 1/κ) − 1/κ + κ^{−ℓ−1})√p. The direct bound of
`lem:app-s2-weil-count` with ℓ + 1 conditions is (ℓ(1 − 1/κ) − 1/κ + κ^{−ℓ−1})√p. They agree up to
the bounded O(ℓ) terms. ∎

[argued] The same holds on any base. A κ-cyclic Kummer cover multiplies the Euler
characteristic of the complement by κ (Riemann–Hurwitz, tame ramification). That pays back
exactly the factor κ^{−1} in the density, so "constant cells" made by covers never improve a
square-root certificate. Only multiplicative dependence that already exists on the base helps.
That is the Kummer-rank collapse of §6.

**Proposition 4 (Weil thresholds of the structured families) [proved given the Weil bound as
cited in the appendix].**
- (F1) If (p − κ)κ^{−κ} > E_κ(κ, p), in particular if √p ≥ (κ − 1)κ^κ + 1 (by E_κ(κ,p) ≤ (κ−1)√p + 1), then
  p ∉ E₂(κ), via an F1 contraction. By `lem:app-s2-weil-count` with ℓ = κ, r_d = ζ^d and
  c_d = −1, each of the κ(κ − 2) patterns (F₀, θ ∉ {0, c}) is hit by some t ∉ μ_κ.
- (F3) Likewise for each fixed ρ of order ≥ 2κ − 1 if (p − 2κ + 1)κ^{−(2κ−1)} > E_κ(2κ − 1, p),
  that is, roughly √p > (2κ − 2)κ^{2κ−1}.
- The subgroup-indicator form (expanding [F ∈ affine subgroup] over its annihilator) improves
  both by a factor of about κ²/9 in p and no more (`predictions.py`).
- Numerically, F1 is certified from p ≈ 1.6·10⁸ (κ = 5) and ≈ 2.4·10¹³ (κ = 7). These are far
  above T_A(5) = 1.27·10⁴ and T_A(7) = 4.94·10⁶.

## 4. Computations [finite computations; witnesses re-checked by an independent program]

`mobius_orbit.c` decides F2 completely at each prime. It scans t ∈ F_p^× for (C1) (in chart ∞)
and, for every (C1) parameter, every chart z ∈ P¹ ∖ (S ∪ T). It uses the generic zero-cell-aware
labelling test for t ∈ μ_κ and the bijection test otherwise. `two_prog.c` decides F3 in the fixed
chart; zero cells are skipped, so F3 is slightly undercounted. `verify.py` is written separately.
It rebuilds α, β from (p, t, z) or (p, ρ, t), searches the labels by propagation from a chosen
(0,0) cell, and checks all κ² cells from the definition, using x ∈ Q_m ⇔ (x g^{−m})^h = 1. It
accepted 141/141 F2 witnesses (κ = 5, p ≤ 6000), all 78 + 278 F3 witnesses at κ = 5 (p ≤ 13000)
and the κ = 7 witnesses listed in §4.3.

### 4.1 κ = 5 (E₂(5) = {11,…,181}, T_A ≈ 1.27·10⁴)

F2 (`mob_k5.out`, every prime p ≡ 1 (mod 5) up to 6000):
- It succeeds at 141 of 194 primes; the fixed chart alone (= F1) succeeds at 136.
- Generic charts add only 1601, 2371, 3391, 3541 and 5171.
- Failures at primes ∉ E₂ go as far as 4231, 4241 and 5231.
- No class of p mod 25 stands out: successes 33/42, 26/37, 24/35, 29/39 and 29/41 for the
  classes 1, 11, 16, 21 and 6.

F3 (`tp_k5.out`, `tp_k5_b.out`, every prime p ≡ 1 (mod 5) up to 13000):
- It fails at 11 31 41 61 71 101 131 151 181 191 211 241 251 271 281 311 331 401 421 521 571
  631 641 691 751, and succeeds at every prime from 761 to 12941.
- So F3's empirical threshold at κ = 5 is 761, about 4.2 × max E₂(5) and 0.06 T_A(5).

### 4.2 Clumping and the chart anomaly (`diag_charts.py`, `diag2.py`, `diag3.py`)

- The (C1) parameters t come in clumps of 2κ (t ↦ tζ, t ↦ 1/t), and their mean count matches
  pκ²/κ^κ. At κ = 7, in 50k-wide bins up to 3·10⁵, the observed mean nC1 is 1.69, 4.58, 6.99,
  10.52, 12.84, 16.79 against 1.41, 4.45, 7.42, 10.40, 13.39, 16.07.
- Good charts come in μ_κ-orbits. So the per-prime success probability is that of
  Poisson(pκ²/(2κ^{κ+1})) clumps, not the naive p²κ^{2−κ}(κ!/κ^κ)². The naive version would
  put F2 at κ^{κ/2+κ/ln κ}, which is wrong. The corrected heuristic is in `predictions.out`
  (row F2all).
- Aggregated over κ = 5, p ≤ 3000, generic-chart solutions roughly follow independence. The
  exceptions are (c, θ) = (0,0): 0 against 22, and (3,0), (3,3): 0 against 140 each. At
  p = 2851 (c = θ = 0) the S-bijective and T-bijective chart sets have size 80 each and are
  disjoint. [computed; unexplained; the clump sizes of 50 make these counts noisy]

### 4.3 κ = 7 (|E₂(7)| = 56, max 3221; T_A ≈ 4.94·10⁶)

F2, complete for every prime p ≡ 1 (mod 7) up to 294337 (`mob_k7.out`, 4137 primes, stopped
there), then every 25th prime up to the limit reached (`mob_k7_sampled.out`):

| range | primes | F2 succeeds | fixed chart (F1) |
|---|---|---|---|
| < 5·10⁴ | 848 | 0.09 | 0.09 |
| 5–10·10⁴ | 745 | 0.24 | 0.22 |
| 1–1.5·10⁵ | 711 | 0.33 | 0.31 |
| 1.5–2·10⁵ | 678 | 0.48 | 0.43 |
| 2–2.5·10⁵ | 695 | 0.54 | 0.49 |
| 2.5–3·10⁵ | 514 | 0.66 | 0.59 |
| 2.5–5·10⁵ (sampled) | 106 | 0.76 | 0.69 |
| 5–10·10⁵ (sampled) | 247 | 0.955 | 0.90 |
| 1–1.62·10⁶ (sampled; run stopped at 1621537) | 295 | 0.997 | 0.976 |

- The last sampled failure is 1013503. So F2's empirical threshold at κ = 7 is above 10⁶,
  within a factor of about 5 of T_A(7). Only every 25th prime above 2.94·10⁵ was tested.
- The predicted crossing (mean 5 clumps) is 1.2·10⁶ (`predictions.out`).

F3 at κ = 7, sampled bands (`tp_k7_sampled.out`; the run was stopped for time after three primes
of the third band):
- near 3·10⁴: 3 of 10 primes succeed;
- near 6·10⁴: 3 of 8;
- near 1.2·10⁵: 3 of 3.

So F3's κ = 7 threshold is above 6·10⁴ and is NOT determined. Its heuristic crossing (mean 5)
is 2.35·10⁵.

The witnesses verified by `verify.py` are all 1579 of `mob_k7.out`, all 611 of
`mob_k7_sampled.out` and all 9 F3 witnesses at κ = 7.

### 4.4 Summary against the truth

| κ | max E₂(κ) | F3 empirical | F2 empirical | κ^{κ−1} | T_A |
|---|---|---|---|---|---|
| 5 | 181 | 761 (complete to 12941) | > 5231 (complete to 6000) | 625 | 1.27·10⁴ |
| 7 | 3221 | > 6·10⁴ (undetermined) | > 10⁶ (sampled) | 1.18·10⁵ | 4.94·10⁶ |

## 5. Why no Weil proof comes out of these families

1. **v is small.** In every family found, Kummer-rank collapse comes from orbits of 1-parameter
   subgroups of PGL₂ [argued; no classification of collapsing families is proved]. These are
   split tori (F1, F2, F3), the non-split torus (F3′) and the translation group (APs: 2κ − 2
   conditions on one variable, even worse). These families have v ≤ 3. With v ≤ 3,
   square-root cancellation buys at most p^{3/2}, against main terms κ^{−c} with c ≥ κ − 2.
2. **The square-root thresholds are worse than T_A** (`predictions.out`):
   - κ = 5: F1 1.6·10⁴, F2 8.5·10⁴, F3 3.9·10⁵;
   - κ = 7: F1 2.8·10⁸, F2 4.5·10⁸, F3 1.4·10¹⁰;
   - against κ^{κ+1} = 1.6·10⁴ and 5.8·10⁶.
   Asymptotically 2c/v is 2κ − 4 (F1), κ − 2 + 2 log_κ(κ^κ/κ!) ≈ κ − 2 + 2κ/ln κ (F2) and
   2κ − 3 (F3). F2 and F3 exceed κ + 1 for every κ ≥ 5; F1 ties it at κ = 5 and exceeds it for
   κ ≥ 7.
3. **Even the one-variable steps cost κ^{2κ−O(1)}** (Proposition 4). The rainbow step in z
   costs ((2κ−2)L)² with L ≈ (eκ)^κ (Stepanov `types/pointwise_rainbow.out`), already
   9.4·10⁹ at κ = 5.
4. **Symmetric families are ratio-neutral.** These are TH5's families and Möbius-symmetric
   ones that do not fix the chart (Lemma 1 caps the order-κ ones at v = 2). Orbit-averaging
   divides c and v by the same group order. Only boundary effects remain, at most
   1/(2(κ−1)) in c/v (TH5 Proposition 2.5).
5. **Fixed algebraic data is excluded by Chebotarev** (`prop:app-s2-chebotarev`). Per-prime
   Möbius charts escape that proposition: its conclusion concerns rescaling and permuting only.
   But they need the rainbow step of item 3.

## 6. The accounting identity, and what a working family would need

### 6.1 Block families [heuristic]

Let S be a union of m_S progressions s_k{ρ^j : j < a_k} and T a union of m_T progressions
t_l{ρ^i : i < b_l}, all with the same ratio ρ, Σa_k = Σb_l = κ. Each block pair (k, l) has
a_k + b_l − 1 distinct cell values up to known separable factors (open progressions).
Separability forces one common slope θ and one offset per block. So, to leading order,
c ≈ Σ_{k,l}(a_k + b_l − 1) − (m_S + m_T) = κ(m_S + m_T) − m_S m_T − (m_S + m_T), with v = m_S + m_T.

With m_S = m_T = m this gives c/v = κ − m/2 − 1 + O(1/m). The bijectivity correction is
O(log_κ m!) = O(m/ln κ)·κ-units. The endpoints are F3 (m = 1, exactly (2κ − 3)/2) and F0 (m = κ,
exactly (κ+1)/2).

So c/v decreases monotonically in m: each collapse saves a factor of about 2/a in conditions
but a factor of a in parameters. The unstructured problem is the minimiser.

### 6.2 What a working family would need [conditional target]

A Weil-provable threshold below κ^κ needs a family with v ≥ 2 and c/v < κ/2 after Lemma 3's
payback. Equivalently, the κ² cells, restricted to the family, must generate a group of rank
< κv/2 modulo κ-th powers, compatibly with the separable target. Lemma 1 and §6.1 show that
orbit structure gives rank ≈ (κ − m/2)v. A family with rank o(κv) would need cells sharing
zeros across many independent parameters: a positive-dimensional family of near-S-unit
configurations. By function-field abc (Mason–Stothers, Brownawell–Masser; Stepanov review §3,
angle (b)), the non-constant ones have bounded degree. No candidate was found.

### 6.3 F3′ (not computed)

With the Cayley chart P¹(F_p) → U₁ = ker N_{F_{p²}/F_p}, s − t = (y_s − y_t)·A_s A_t. Then
(s − t)² = N(y_s − y_t)·N(A_s)N(A_t), and since κ is odd, χ ↔ χ² gives:
(C1) for χ ⇔ separability of χ∘N(y_s − y_t).

So progressions η^j y in U₁ give the same collapse as F3, with the coset conditions now norm
conditions in F_{p²}. Same (c, v); no gain; not run.

## 7. Adversarial self-check

- **Is Lemma 1's "order κ" too narrow?** Yes, deliberately. Involutions and other small-order
  Möbius symmetries are allowed by TH5's count only in fixed charts (H needs κ even). In generic
  charts they are ratio-neutral by orbit counting (§5.4), which is [argued], not proved. No
  claim is made about all Möbius symmetries.
- **Is F2 really outside TH5?** Only its generic-chart part. That part added just 5 primes at
  κ = 5 ≤ 6000. It is not a new mechanism of any strength.
- **Is the "κ^{κ−1+o(1)}" empirical threshold real?**
  - It is a heuristic extrapolation from κ = 5, 7 plus first moments with clumping. The κ = 7
    F2 data are sampled above 2.94·10⁵.
  - F3 at κ = 7 is a handful of sampled primes. Its threshold there is NOT established.
  - The F3 heuristic undercounted the κ = 7 band near 3·10⁴ (3 of 10 primes succeed, against
    a predicted ~8%). So the constants in `predictions.out` are unreliable at small p.
- **Could F3's 761 at κ = 5 be a coincidence of small p?** It is a complete computation up to
  12941; F3 succeeds everywhere there from 761 on.
  - It says nothing about larger p or other κ.
  - At κ = 5 the full problem is decided exactly anyway (E₂(5) known), so this changes nothing.
- **Verification gaps.**
  - Every witness in every output file was accepted by `verify.py`: F2 141 (κ = 5), 1579 + 611
    (κ = 7); F3 78 + 278 (κ = 5), 9 (κ = 7).
  - Failures ("no solution in the family") are not independently re-checked. They concern the
    family only, never E₂.
  - F3 skips zero-cell configurations, so a reported F3 failure could hide a zero-cell solution.
  - Within F2, t ∈ μ_κ (T = S) is handled by the general zero-aware test.
- **Lemma 3's scope.** It is proved for one-variable substitutions. The multi-variable
  Riemann–Hurwitz version is [argued].
- **Does the accounting identity overreach?** It is a leading-order condition count for block
  families with a common ratio. It is not a theorem about all algebraic families. It does not
  exclude exotic families with more collapse (§6.2), which this pass did not find. It only shows
  that the natural ones lose.

## 8. Claim gates that stay false

No threshold below T_A is proved. E₂(κ), T_A, Table `tab:app-s2-thresholds` and every schedule
are unchanged. F1–F3 are not proposed for the paper. A one-line remark could cite Lemma 1 and
the §6.1 identity under the barrier remarks; the integrator decides.

## 9. Files (`2026-11-13-rees-square-gap-families/`)

- `mobius_orbit.c`: F2 decider. Usage: `kappa pmin pmax [w [stride]]`; columns p, p mod κ², nC1,
  nsol, fixed_ok, n_generic (t ∉ μ_κ), n_P (t ∈ μ_κ, z generic), witness t z.
  Outputs: `mob_k5.out`, `mob_k7.out`, `mob_k7_sampled.out`.
- `two_prog.c`: F3 decider. Outputs: `tp_k5.out`, `tp_k5_b.out`, `tp_k7_sampled.out`
  (driver `run_tp_k7.sh`).
- `verify.py`: independent witness checker (`verify.py κ file` for F2,
  `verify.py κ file twoprog` for F3).
- `diag_charts.py`, `diag2.py`, `diag3.py`: chart-bijectivity diagnostics (§4.2).
- `predictions.py`, `predictions.out`: first moments with clumping, square-root and Weil
  thresholds.

# Report: complete-output consequence of the exact two-step identities

## 1. Verdict

**Proved (finite-dimensional, all n ≥ 2):** the parent identities M v_A = q and M q = (v_A − e)/2 are exact; every full moment obeys |T_{2k} − 2^{−k−1}| ≤ √(2/L) and |T_{2k+1}| ≤ √(2/L) uniformly in k; the native output converges to K_∞ = 2c(1−z²)/(2−z²) with |K_L − K_∞| ≤ c z²√2 /((1−z)√L).

**Proved:** every width-restricted moment T_r^{(w)}, r ≥ 1, satisfies an explicit bound, uniform in r, that tends to 0 for every w ≤ n − log₂(n log₂ n) − ω(1) (in particular fixed w and w = o(n)); T_0^{(w)} = T_0 → 1/2. Hence the truncated shortcut output converges to c(1 − z²/2), exceeding K_∞ by exactly c z⁴/[2(2−z²)] > 0 for every fixed ρ > 1. With R = O_ρ(log 1/ε) and fixed ε below one third of this gap, the scalar shortcut is falsified, not merely one moment.

**Not claimed:** any hardness, separation, generic correlated-estimator no-go, or classical polynomial match. Assumptions inherited from the attached proof are listed in §6.

## 2. Exact identities and the full output

Notation: M = Π S Π, Π v = v_A + e with e = Π v_B, ‖e‖ ≤ (2L)^{−1/2}; q = Π S v_A = (h − ½)e₁/L. Series convention T_r = ⟨Π v, M^r Π v⟩ (M^0 := Π), which matches the stated T_2 = ‖Π S Π v‖².

(i) M v_A = Π S v_A = Π(h e₁/L) = q. 
(ii) S q = (h−½)σ e₁/L: on h = 1, σ = (−1)^x gives ½(−1)^x; on h = 0, σ = (−1)^y gives −½(−1)^y. So S q = (v_A − v_B)/2 and M q = Π S q = (v_A − e)/2. Exact.

Orthogonality facts (exact): ⟨v_A, e⟩ = ⟨v_A, v_B⟩ = 0 (disjoint supports); ⟨v_A, q⟩ = (1/L²)·L·Σ_{x<L/2}½(−1)^x = 0 (L/2 even); ⟨e, q⟩ = ⟨v_B, q⟩ = −(1/2L²)Σ_{h=0}(−1)^y = 0.

Induction with ‖M‖ ≤ 1: M^{2k}v_A = 2^{−k}v_A + ε_{2k}, M^{2k+1}v_A = 2^{−k}q + ε_{2k+1}, with ‖ε_r‖ ≤ Σ_{m≤k}2^{−m}‖e‖ < ‖e‖. Then, using ‖Π v‖ ≤ 1 and the orthogonalities,

 T_r = ⟨v_A + e, M^r v_A + M^r e⟩ = τ_r + ⟨Π v, ε_r⟩ + ⟨Π v, M^r e⟩, |T_r − τ_r| ≤ 2‖e‖ ≤ √(2/L),

with τ_{2k} = 2^{−k−1}, τ_{2k+1} = 0, uniformly in r. (T_0 = ½ + ‖e‖² exactly, consistent with the L = 8 control ½ + 3/68.)

Series: Σ_r(−z)^r τ_r = Σ_k z^{2k}2^{−k−1} = 1/(2−z²), so K_∞ = c[1 − z²/(2−z²)] = 2c(1−z²)/(2−z²), and |K_L − K_∞| ≤ c z²Σ_r z^r·√(2/L) = c z²√2/((1−z)√L). The parent's O_ρ(L^{−1/2}) claim holds with this explicit constant.

Consistency check (not a proof of the series convention, which I take from the existing proof): with c(1+z) = ρ, c(1−z) = 1, K_∞ = 4ρ(ρ+1)/(ρ²+6ρ+1), which equals the series combination (harmonic mean) of the left half's series laminate 2ρ/(ρ+1) and the right half's parallel laminate (ρ+1)/2. This is exactly what the two-phase geometry should give up to interface corrections O(1/L).

## 3. Restricted moments: definition and window decomposition

A_j = Π a_j(K_e), j ≥ −1, positive, commuting, Σ_j A_j = Π; c_j = a_j(4) ≥ 0, Σ c_j = 1. Define

 T_r^{(w)} = Σ_{(i_0,…,i_r): max−min ≤ w} ⟨A_{i_0}v, S A_{i_1} S ⋯ S A_{i_r} v⟩ (r+1 band indices).

For r ≥ 3 the admissible set is **not** a product set once the outer pair is fixed (e.g. i_0 = i_r = 5, w = 3 admits middle 2 and middle 8 separately but not jointly), so no "sum the middle bands into one contraction" step is available. Instead use the exact inclusion–exclusion

 1{max−min ≤ w} = Σ_{s≥−1} (1{all ∈ [s,s+w]} − 1{all ∈ [s+1,s+w]}),

(each tuple counted once, at s = its minimum). With P_s = Σ_{j=s}^{s+w}A_j and P′_s = Σ_{j=s+1}^{s+w}A_j (both 0 ≤ P ≤ Π, commuting with Π, K_e),

 T_r^{(w)} = Σ_s [G_r(P_s) − G_r(P′_s)], G_r(P) := ⟨v, P(SP)^r v⟩ = ⟨Pv, (SP)^{r−1}S (Pv)⟩.

All sums converge absolutely at each finite L (band norms decay like e^{−λ_*2^s}). No positivity of the restricted quadratic form is assumed anywhere; only absolute values are bounded.

**Lemma A (contraction trick).** For 0 ≤ P ≤ I and any vector u, |⟨u, P(SP)^m u⟩| ≤ ⟨u, Pu⟩ for all m ≥ 0. Proof: P(SP)^m = P^{1/2}(P^{1/2}SP^{1/2})^m P^{1/2} and ‖P^{1/2}SP^{1/2}‖ ≤ 1.

**Lemma B (outer replacement inside one window).** P_s v = C_s v_A + e^{(s)}, C_s = Σ_{i∈[s,s+w]}c_i ≤ 1, e^{(s)} = Σ_{i∈[s,s+w]}e_i, e_i := A_i v − c_i v_A. Since ‖(SP_s)^{r−1}S‖ ≤ 1,

 |G_r(P_s) − C_s²⟨v_A,(SP_s)^{r−1}S v_A⟩| ≤ √2‖e^{(s)}‖ + ‖e^{(s)}‖².

For r ≥ 2 the main term equals C_s²⟨q, P_s(SP_s)^{r−2}q⟩ (q = S v_A); for r = 1 it equals C_s²⟨v_A, q⟩ = 0.

**Lemma C (no infinite count).** Σ_s‖e^{(s)}‖ ≤ (w+1)E and Σ_s‖e^{(s)}‖² ≤ Σ_s(Σ_{i∈[s,s+w]}‖e_i‖)·E ≤ (w+1)E², where E = Σ_i‖e_i‖ ≤ E_n = 4(3n+2)/√L + 3e^{−32L} (attached eq. (4), including the J = 3n tail). The only multiplicity is the finite window overlap w+1 — each band index lies in exactly w+1 windows — never a count of tuples or of bands.

**Lemma D (scalar main term).** With a = ⌈log₂n⌉, T = 2^{a+w+1}, τ = Σ_{i>a}c_i = e^{−4·2^{a+1}} ≤ e^{−8n}: for s ≤ a, P_s ≤ Σ_{j≤a+w}A_j = Π(1−e^{−TK_e}) ≤ 1−e^{−TK_e}, so ⟨q,P_s q⟩ ≤ T⟨q,K_e q⟩ = 2T/L (two interfaces, L edges each, amplitude 1/L). For s > a, C_s ≤ τ, so C_s² ≤ τC_s, and Σ_s C_s = w+1.

## 4. Theorem (restricted moments vanish, uniformly in r)

For all n ≥ 2, w ≥ 0, r ≥ 1,

 |T_r^{(w)}| ≤ 2Σ_{s≤a}C_s²⟨q,P_s q⟩ + 2Σ_{s>a}C_s²⟨q,P_s q⟩ + 2(w+1)(√2E_n + E_n²)
  ≤ (a+2)2^{a+w+3}/L + (w+1)e^{−8n} + 2(w+1)(√2E_n + E_n²)
  ≤ 16(⌈log₂n⌉+2)·n·2^w/2^n + (w+1)e^{−8n} + O(w n/2^{n/2}).

(The factor 2 collects the primed windows, whose C′_s ≤ C_s, P′_s ≤ P_s; the first term counts the a+2 windows s ∈ {−1,…,a}; Lemma A removes all r-dependence.) The bound → 0 whenever 2^w = o(2^n/(n log n)) and w = o(2^{n/2}/n), i.e. for every fixed w, every w = o(n), and indeed every w ≤ n − log₂(n log₂n) − ω(1). Thus the shortcut cannot save more than roughly half of the ≈2n relevant band range on this family, and no width depending only on (ε, r) suffices.

Meanwhile T_0^{(w)} = T_0 (one index, no restriction) = ½ + ‖e‖² → ½, and the unrestricted T_r → τ_r with τ_2 = ¼, confirming the attached r = 2 result as the special case and extending it to all r.

## 5. Complete scalar-output consequence

Shortcut output K^{(w,R)} = c[1 − z²Σ_{r<R}(−z)^r T_r^{(w)}]. Let B_n(w) denote the bound of §4. Then

 |K^{(w,R)} − c(1 − z²T_0)| ≤ c z²Σ_{1≤r<R}z^r|T_r^{(w)}| ≤ c z³B_n(w)/(1−z) → 0,

so K^{(w,R)} → c(1 − z²/2) for every R ≥ 2 (R ≥ 3 as requested) and every admissible w, including R = O_ρ(log 1/ε). The true output: |K_L − K_∞| ≤ c z²√2/((1−z)√L), and the honest R-cutoff of the true series costs at most c z^{R+2}/(1−z)·sup_r|T_r| ≤ c z^{R+2}/(1−z). Algebra: c(1−z²/2) − 2c(1−z²)/(2−z²) = c z⁴/[2(2−z²)] =: Δ_ρ > 0.

Falsification statement: fix ρ > 1, fix ε < Δ_ρ/3, choose R with c z^{R+2}/(1−z) ≤ ε. Then for all sufficiently large n and any w ≤ n − log₂(n log₂n) − ω(1), |K^{(w,R)} − K_L| ≥ Δ_ρ − 2ε − o(1) > ε. Cancellations between moments cannot rescue the shortcut: the restricted odd and even moments all vanish individually, the true even moments carry the geometric mass 2^{−k−1}, and the series tail is a geometric sum of uniformly bounded terms. Large individual terms play no role; every estimate is on the total.

Paid-resource meaning: the hoped-for cost reduction (band enumeration O(w) with w = O(r + log 1/ε) instead of Θ(n)) is not available for this O(n)-size, three-bit-decision input; a correct band-expansion estimator must represent index separations of order n (heat times from O(1) up to ≈L²) within a single triple/tuple. This is an obligation on cost accounting, not a lower bound on all classical algorithms.

## 6. Assumptions, obligations, falsifiers

Inherited (used, not re-derived here): the series formula K = c[1 − z²Σ(−z)^r T_r] with T_r = ⟨Πv, M^rΠv⟩ (checked only via the laminate consistency of §2, which is strong but is a corroboration, not a derivation); the band facts ‖A_i v − c_i v_A‖ ≤ 3/√L, ‖A_i v_B‖ ≤ (2L)^{−1/2}, and the tail bound Σ_{i>3n}‖A_i v‖ ≤ 2e^{−32L} (attached eqs. (2)–(4); I re-verified the four-boundary-site identity, the Lipschitz constants, and ‖Πv_B‖² ≤ 1/(2L) via the k_y = L/2 symbol λ_x/(λ_x+4)).

Independent of these, the identities of §2 and Lemmas A–D are self-contained finite-dimensional statements.

Cheapest falsifiers of this report: (1) exact linear algebra at L = 8 or 16 checking M q = (v_A − e)/2 and |T_r − τ_r| ≤ √(2/L) for r ≤ 6 (transcription check only; the all-n claim is the proof); (2) compute T_3^{(0)}, T_4^{(1)} at L = 16, 32 and compare with the §4 bound and with T_3 ≈ 0, T_4 ≈ 1/8; (3) if the series convention differs from the one assumed (e.g. T_r defined with S on the outside), the laminate identity K_∞ = 4ρ(ρ+1)/(ρ²+6ρ+1) would fail — that would invalidate §5's numerical gap but not §4.

Unresolved/open (unchanged): any coupled or variational estimator retaining distant-scale tuples; full polynomial classical match; hardness of any kind. This family has simple microstructure and is an attack on one estimator only.
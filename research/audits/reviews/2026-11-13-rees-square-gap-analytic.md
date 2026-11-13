# Square gap, analytic attack on the upper side for prime κ (13 Nov)

AI-only report (2026-11-13), pending human review. No existing file was edited. Scripts and
outputs are in `2026-11-13-rees-square-gap-analytic/` (every run `nice -n 19
/opt/anaconda3/bin/python -I`, one process at a time, largest observed resident size about 0.7 GB, longest run about 7 min).
Notation as in `appendix-schedule2.tex` and `2026-11-05-rees-square-gap-attack.md` §1: κ ≥ 3,
p ≡ 1 (mod κ), h = (p−1)/κ, y = (0, y_1, …, y_{κ−1}) uniform, X_j(y) ⊆ Q_{−j}, n_j = |X_j(y)|,
λ = Λ = (p−1)/κ^κ, E_κ(m,p) the error of `lem:app-s2-weil-count`, ρ_m = (p−m)/(pκ^m),
η_m = κ^m E_κ(m,p)/(p−m). TH2 and TH9 are `2026-11-02-rees-threshold-2.md` and
`2026-11-05-rees-threshold-9.md`.

Read: appendix lines 79–480; the 11-05 report §§0–6; the 11-09 report §§0–3, 9, 11.8,
12.12–12.14; TH2 §§0, 2, 3; TH9 §§0, 2.1–2.3; `main.tex` `rem:two-level-threshold-size`; the
provenance items `prov:sde-threshold` and `prov:s2-joint-moments`.

## 0. Verdict

- **(T1) not reached.** No exponent below κ is proved, conditionally or not, and no route found
  here gives one. Every route in the brief was traced to the same missing input (§6).
- **(T2) holds already, by a proof that the paper labels "argued".** TH2 Theorem 5 (central
  moments of order 2m) is a complete proof. I re-derived it line by line (§2) and reimplemented
  it from its statement. For prime κ it beats T_A from κ = 17 on: T_A/T_C = 2.17 at κ = 17,
  3.64 at κ = 31 and 6.85 at κ = 71 (`tc_vs_ta_prime.out`). Asymptotically the gain is a factor
  (κ−1)/(4e⌈ln 4κ⌉²) for κ ≥ 32, and (κ−1)/6 for κ ≥ 729 with TH9 Corollary 3. The paper calls
  that corollary conditional, and its only conditional input is TH2 Theorem 5 with m = 2.
  - PROVED (AI-checked twice, pending human review).
  - This is a status correction, not new mathematics.
  - For prime κ ≤ 13 nothing beats T_A, so the paper's small κ are unchanged.
- **(T3) two new rigorous barriers.**
  - *Theorem D (Deligne–Betti barrier on the open stratum; route (a))* [PROVED given cited
    theorems].
    - Normalise the stratum with no zero cell to M ⊂ A^{2κ−2}.
    - Every frequency sum bound that Deligne's theorem gives from Betti numbers is at least
      β_κ p^{κ−1}. Here β_κ = |χ_c(M)| = 1, 5, 73, 2069, 95401, 6487445 for κ = 2, …, 7: the
      Euler characteristic of the complement of the K_{κ,κ} graphic arrangement, computed exactly.
    - Grouping frequencies into one complete sum over an intermediate Kummer cover changes
      nothing (Lemma G).
    - So any such certificate fails for p ≤ T_Del(κ) = ((κ^{κ²−1} − 1)β_κ)^{1/(κ−1)}, which is
      about 0.28·κ^{κ+3} (measured for 5 ≤ κ ≤ 16) and lies above T_A for every κ ≥ 3.
    - This is the stratum where O1 does not apply. Theorem D turns the 11-09 "[argued]"
      angle (a) into a theorem, in the (α, β) chart.
  - *Theorem B (point-set Weil barrier; routes (b) and (d))* [PROVED].
    - Take κ ≥ 3 and p ≤ κ^κ/2. There is a law of a random set 𝒳 = ⊔_j 𝒳_j with these
      properties:
      - its single columns are exact;
      - it is independent on any κ−1 columns;
      - it has the Q_0-scaling and ξ-rotation symmetries;
      - every point set P satisfies the Weil bracket for Pr[P ⊆ X(y)]: the upper bracket at
        every size, the lower one wherever it is nontrivial;
      - no realisation of 𝒳 has all κ columns nonempty.
    - This strengthens `prop:app-s2-barrier`, which constrains only E C(M_S, m) with η_m < 1. It
      also closes the gap that `rem:app-s2-barrier-scope` names: one-sided brackets with
      η_m ≥ 1 and all κ columns.
    - Corollary: no lower bound on E Π_j n_j, that is on the count of contractions with no zero
      cell, follows from point-set Weil brackets at p ≤ κ^κ/2. So the second-moment and
      conditioning versions of route (b) need an input that is not of this kind.
- **Routes (c) and (d):** no rigorous progress (§5).
- **Data.** No threshold below T_A is claimed for any κ ≤ 13. So nothing conflicts with
  E_2(5) ∋ 181, 3221 = max E_2(7) (`E2_k7.txt`) or E_2(3) = ∅. All barrier values lie above
  every known member of E_2.

## 1. A reformulation used below

A contraction with no zero cell is a transversal P = (x_0, …, x_{κ−1}), x_j ∈ Q_{−j}, together
with y_1, …, y_{κ−1} such that x_j + y_i ∈ Q_{−(i+j)} for all i ≥ 1 and all j. Given P the rows
decouple, so

  N*(p) = Σ_{P transversal} Π_{i=1}^{κ−1} N_i(P),  N_i(P) = #{y : x_j + y ∈ Q_{−(i+j)} ∀ j},  (1.1)

and E_y Π_j n_j = N*(p)/p^{κ−1} = Σ_P Pr_y[P ⊆ X(y)]. Each N_i(P) is a one-variable count with κ
shifts. Its main term p/κ^κ is of order λ, and its Weil error is of order κ√p. Everything below
comes back to (1.1).

## 2. (T2): the central-moment threshold is a proof

**What was checked [PROVED, re-derived here].** TH2 Lemma D and Theorem 5, steps 1–6:
- the test polynomial (1 − n/λ)^{2m};
- the factorial-moment comparison with Bin(h, κ^{−(κ−1)}), with F_k/B_k ∈ [1−δ_k, 1+δ_k] from
  Lemma D row by row;
- the central-moment bound E(B−λ)^{2m} ≤ A_{2m}(λ) by grouping into partitions with no singleton
  block;
- the coefficient bound Σ|a_k|B_k ≤ W_m(λ);
- the union bound over the κ columns, using that the n_j have the same law since
  X_j(y) = ξ^{−j}X_0(ξ^j y).

In Corollary 5′ I checked:
- Bell(2m) ≤ (2m)^{2m};
- S(j,k) ≤ C(j,k)k^{j−k}, via block minima;
- T_j(λ) ≤ (λ+j)^j and W_m ≤ 4^m e^{1/(2e)};
- E_k ≤ k√p and ε_k ≤ 2kκ^k/√p for p ≥ 4m;
- δ_k ≤ 10mκ^{2m+1}/√p;
- the constant 12.1 (corrected by TH2's own referee);
- condition (C) at κ = 31 (fails, 12.02 < 12.43) and κ = 32 (holds, 13.86 ≥ 12.43).

I found no error.

**Independent recomputation [computed].** `tc_vs_ta_prime.py` was written from the statements, not
from TH2's code. It computes T_A by bisection on U_κ of `prop:app-s2-TA` and T_C = min_m inf{p :
G_m(p) < 1}. It reproduces T_A(3) = 79.04, T_A(5) = 1.266·10⁴, T_A(7) = 4.94·10⁶, and TH2's T_C
to six digits.

| prime κ | 7 | 11 | 13 | 17 | 19 | 23 | 29 | 31 | 37 | 43 | 53 | 71 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T_A/κ^κ | 6.00 | 10.0 | 12.0 | 16.0 | 18.0 | 22.0 | 28.0 | 30.0 | 36.0 | 42.0 | 52.0 | 70.0 |
| T_C/κ^κ | 59.1 | 11.3 | 13.0 | 7.36 | 7.71 | 7.51 | 8.07 | 8.24 | 8.71 | 9.11 | 9.56 | 10.2 |
| T_A/T_C | 0.10 | 0.89 | 0.92 | **2.17** | 2.33 | 2.93 | 3.47 | 3.64 | 4.13 | 4.61 | 5.44 | 6.85 |

**Consequence.**
- *Status.* `main.tex` `rem:two-level-threshold-size` says the 4e⌈ln 4κ⌉²κ^κ + 1 bound is
  "argued, not proved here", and `prov:s2-joint-moments` calls TH9 Corollary 3 "conditional on
  … Theorem 5, not proved". On the evidence above, both are proofs in the reports, refereed by
  AI only: TH2's own check, TH9's check, and this re-derivation.
- *Prime κ.* T_A is improved by a factor that grows with κ:
  - ≥ 2.17 for every prime κ ≥ 17, from the computable G_m. That is a finite list of bisections
    at κ ≤ 71; for κ > 71 the asymptotic statements apply.
  - (κ−1)/(4e⌈ln 4κ⌉²) for κ ≥ 32 (Corollary 5′).
  - (κ−1)/6 for κ ≥ 729 (TH9 Corollary 3).
- *Small κ.* Neither helps at κ ≤ 13. The paper's tables are unaffected.
- *Recommendation.* After a human check, the paper could state the T_C bound as proved. That
  is the integrator's call, and nothing is applied here.

## 3. Route (a): Theorem D and Lemma G

**Setting.** Let M = {(α_1..α_{κ−1}, β_1..β_{κ−1}) ∈ A^{2κ−2} : α_j + β_i ≠ 0 ∀ i, j}, with
α_0 = 1 and β_0 = 0. It is the open stratum modulo translation and scaling: d = 2κ−2, smooth,
affine, geometrically connected.

For e′ ∈ Z_κ^{κ²−1} (the cells other than (0,0)), put f_{e′} = Π (α_j+β_i)^{e′_ij} and
S_{e′}(M) = Σ_{m∈M(F_p)} χ(f_{e′}(m)).

A point of M with cell indices −(i+j) is a contraction with no zero cell, and there is one in
each scaling class. So N′(p) = κ^{1−κ²} Σ_{e′} ω^{⟨e′,i+j⟩} S_{e′}(M), and N′(p) > 0 implies
p ∉ E_2(κ). The term-by-term certificate is #M(F_p) > Σ_{e′≠0} B_{e′}, where B_{e′} is any upper
bound for |S_{e′}|.

**Theorem D [PROVED given cited theorems].** Let L_{e′} be the rank-one Kummer sheaf of χ∘f_{e′},
and let B^{Del}_{e′} = Σ_i dim H^i_c(M_{F̄_p}, L_{e′}) p^{i/2}. This is the bound that the
Grothendieck trace formula and Deligne's Weil II give from Betti numbers.

(i) B^{Del}_{e′} ≥ β_κ p^{κ−1} for every e′ ≠ 0. Here β_κ = |χ_c(M)| = |Q_κ(1)|, and
Q_κ(t) = P_{K_{κ,κ}}(t)/(t(t−1)) with P the chromatic polynomial of K_{κ,κ}.

(ii) Hence the Deligne–Betti certificate fails whenever
#M(F_p) ≤ (κ^{κ²−1} − 1)β_κ p^{κ−1}, in particular for every
p ≤ T_Del(κ) := ((κ^{κ²−1}−1)β_κ)^{1/(κ−1)}.

*Proof.*
1. *Lisse, tame, nontrivial.* L_{e′} is lisse of rank one on M and tame, since its order divides
   κ and p ∤ κ. It is geometrically nontrivial for e′ ≠ 0. On the slice, the cells other than
   (0,0) are κ²−1 distinct nonconstant affine-linear functions (α_j, 1+β_i, α_j+β_i), so f_{e′}
   is not a constant times a κ-th power in F̄_p(M).
2. *Vanishing outside [d, 2d−1].* M is smooth affine of dimension d. Artin vanishing and
   Poincaré duality give H^i_c(M, L) = 0 for i < d. H^{2d}_c(M, L) is the coinvariants of a
   nontrivial character of π_1^{geom}, hence 0.
3. *Euler characteristic.* χ_c(M, L_{e′}) = χ_c(M), by Deligne's Euler-characteristic formula for
   tamely ramified lisse sheaves (rank × χ_c; as in Illusie, Astérisque 82–83, 1981). NEEDS
   HUMAN VERIFICATION of the exact form cited. The Kummer sheaf is pulled back from the tame
   sheaf on G_m, so it is tame in the curve sense.
4. *χ_c(M).* #M(F_q) = Q_κ(q) for every finite field F_q: the vertices α_j and −β_i form a
   proper colouring of K_{κ,κ}, divided by translation (q) and scaling (q−1). Apply the trace
   formula over F_{p^n} for all n. Linear independence of n ↦ λ^n then gives
   Σ(−1)^i dim H^i_c = Q_κ(1).
5. *Bound.* B^{Del} = Σ_{i=d}^{2d−1} h^i p^{i/2} ≥ p^{d/2} Σ h^i ≥ p^{d/2}|χ_c| = β_κ p^{κ−1}.
   There are κ^{κ²−1} − 1 frequencies e′ ≠ 0. ∎

**Lemma G (grouping) [PROVED given standard facts].**
- Let V → M be the Kummer cover w_{ij}^κ = α_j + β_i, (i,j) ≠ (0,0), with group
  G = μ_κ^{κ²−1}. Then π_*Q̄_ℓ = ⊕_{e′} L_{e′}.
- For a subgroup H ≤ G, the intermediate cover V/H → M has
  H^i_c(V/H) = ⊕_{e′ ∈ H^⊥} H^i_c(M, L_{e′}). A pattern twist changes only Frobenius, not the
  geometric cohomology.
- So for any family of frequencies grouped into one complete sum over V/H, which has dimension
  2κ−2, the Deligne–Betti error bound is exactly Σ_{e′∈H^⊥∖0} B^{Del}_{e′}.
- Grouping is therefore never better than term by term for any bound made from Betti numbers and
  the Weil II weight bound. This covers route (a) in the form posed. Katz's Betti-sum bounds are
  upper bounds for the same h^i, so they are covered too. ∎

**Numbers [computed exactly; `beta_arrangement.py`, `beta_table.out`, `beta_brute.out`].**
- The point-count polynomial was checked by enumeration at κ = 2 (p ≤ 13) and κ = 3 (p ≤ 11).
- β_κ for κ = 2..16 is 1, 5, 73, 2069, 95401, 6487445, 610093513, …
- β_κ^{1/(κ−1)} = 2.24, 4.18, 6.74, 9.91, 13.7 for κ = 3–7, and ≈ 0.287κ² at κ = 16.
- So T_Del(κ)/κ^{κ+1} = β_κ^{1/(κ−1)} × (1 − o(1)):
  - log_κ T_Del = 4.73, 6.03, 7.19, 8.28, 9.34 for κ = 3–7, and 18.55 at κ = 16;
  - T_Del/T_A = 181/79 = 2.3 at κ = 3 and 1.05·10⁵/1.27·10⁴ = 8.3 at κ = 5.

**κ = 3 check of the scale [computed exactly; `k3_open_stratum*.py`, `k3_support_types.py`].**
All 3⁸ sums S_{e′}(M) were computed exactly for p ≤ 181.
- The exact-modulus certificate L1/S_0 is 4.12 at 43, 1.004 at 127 and 0.893 at 139, so with
  exact moduli it first holds at p = 139.
- The Deligne–Betti lower bound for L1/S_0 is 21.4 at 43 and 1.05 at 181. So the crude Betti
  certificate cannot fire below 181, as Theorem D says.
- By support:
  - full-support frequencies have median |S| ≈ 0.4–1.1 p² (square-root size) and maximum
    ≈ 7–11 p²;
  - frequencies with every row and column of degree ≥ 2 but not full have median 0.13–0.29 p²;
  - frequencies with a row or column of degree ≤ 1 have median ≈ 0.19 p^{3/2}, and the maximum
    (p−3)p ≈ p³ comes from 4-cycle-type supports.

**Scope (what Theorem D does not cover).** Theorem D bars Betti-number bounds with Weil II's
weight bound i on H^i_c. The κ = 3 data show these bounds are loose for most frequencies, whose
weights are evidently below d. A weight-refined or exact-modulus term-by-term certificate on M is
not covered.
- At κ = 3, exact moduli first certify at 139, between T_A(3) = 79 and T_Del(3) = 181.
- `app:sde-side-barrier` argues that such hybrid certificates improve T_A by at most a factor
  tending to 1. That is not re-proved here.

Theorem D is the rigorous form of the 11-09 §3 angle (a) [argued]. That argument used M_{0,2κ+1}
and (2κ−2)!. Here the chart is (α, β), with the exact β_κ and both proofs written out.

## 4. Route (b): Theorem B

For finite P ⊆ F_p^× put a = |P|, P_j = P ∩ Q_{−j} and π(P) = Pr_y[P ⊆ X(y)]. Define

  u_a = ρ_a(1+η_a) = κ^{−a}(1 − a/p) + E_κ(a,p)/p,  ū_a = min(1,u_a)^{κ−1},
  ℓ_a = (ρ_a(1−η_a))^{κ−1} if η_a < 1, else 0.

Applying `lem:app-s2-weil-count` row by row (TH9 Lemma 2, steps 3–4) gives
ℓ_a ≤ π(P) ≤ ū_a for all P. These are the **point-set Weil brackets**.

**Lemma U [PROVED].** Let κ ≥ 3 and p ≥ 7. If a_1, …, a_r ≥ 1 with r ≥ 2 and a = Σ a_t, then
Π_t min(1, u_{a_t}) ≤ min(1, u_a).

*Proof.*
1. *Two parts.* Let a, b ≥ 1, m = a+b and u_m < 1. Expanding,
   p²(u_m − u_au_b) = p[E_m − κ^{−a}(1−a/p)E_b − κ^{−b}(1−b/p)E_a] − E_aE_b − abκ^{−m}
   ≥ (1−1/κ)pE_m − E_aE_b − abκ^{−m}.
   This uses E_a + E_b ≤ E_m (superadditivity of c and d, shown in `prop:app-s2-barrier`(iii))
   and κ^{−a} ≤ 1/κ.
   - If min(a,b) = 1, then E_1 = 0. The bound is ≥ (2/3)³p^{3/2} − 1/9 > 0.
   - If a, b ≥ 2, then E_k ≤ (k−1)√p + k/κ and E_m ≥ c_m√p. Also u_m < 1 forces √p > c_m,
     where c_m = m(1−1/κ) − 1 + κ^{−m}.
   - It then suffices that F(m) := (2/3)c_m s − (m−2)²/4 − (m²/2−m)/(3s) − m²/(18s²) ≥ 0 at
     s = max(c_m, √7). Here κ = 3 is the worst case, because the left side increases in κ and
     in s and the right side decreases.
   - F(m) ≥ 0.45 for 4 ≤ m ≤ 10⁶ (`lemmaU_Fm.out`; minimum at m = 6).
   - For m ≥ 100, F(m) ≥ 0.0463m² + 0.11m − 1 − 0.26m − 0.14 > 0.
2. *Chaining.*
   - If u_a ≥ 1 the claim is trivial.
   - If 1 − 1/κ ≤ u_a < 1, take any two parts. If one has size 1, its factor is below 1/κ.
     Otherwise both factors are ≤ κ^{−2} + x_t, with x_1 + x_2 ≤ E_a/p < 1, so their product is
     < (1/9 + 1/2)² < 0.38 < 2/3.
   - If u_a < 1 − 1/κ, then every partial sum s has u_s < 1: otherwise
     E_a ≥ E_s ≥ p(1−1/κ) and u_a ≥ 1 − 1/κ. So merge one part at a time with step 1. ∎

The grid check `setlevel_check.py merge` covers 3.6·10⁷ cases (κ = 3..40, 60 values of p up to
min(κ^κ/2, 10¹²), a+b ≤ 300). It finds both merging inequalities with minimum relative margin
1.2·10⁻⁴ > 0.

**Theorem B (point-set Weil barrier) [PROVED].** Let κ ≥ 3 and p ≤ κ^κ/2. There is a law 𝓛 of
a random set 𝒳 = ⊔_j 𝒳_j, 𝒳_j ⊆ Q_{−j}, such that:
- (i) for |S| ≤ κ−1, the law of (𝒳_j)_{j∈S} is the product of the true laws of the X_j(y);
- (ii) 𝓛 is invariant under x ↦ qx for q ∈ Q_0, and the law of (ξ𝒳_{j+1})_j equals that of
  (𝒳_j)_j, as for the true X;
- (iii) ℓ_{|P|} ≤ π_𝓛(P) ≤ ū_{|P|} for every finite P;
- (iv) 𝓛(all 𝒳_j ≠ ∅) = 0.

*Proof.*
1. *Construction.* Put θ = Pr[X_0 ≠ ∅] ≤ E n_0 < p/κ^κ ≤ 1/2. Draw B from P_θ
   (`lem:app-s2-kwise`), and independently Z_j ~ Law(X_j(y) | X_j(y) ≠ ∅). Set 𝒳_j = Z_j if
   B_j = 1, and ∅ otherwise. (If θ = 0, take 𝒳 = ∅.)
2. *(i) and (iv)* hold as in `prop:app-s2-barrier`.
3. *(ii).* P_θ is exchangeable. The conditional laws are Q_0-invariant, since X(qy) = qX(y)
   with qy uniform. They are ξ-covariant, since X_j(ξy) = ξX_{j+1}(y).
4. *(iii), P meeting all κ columns.* Then π_𝓛(P) = 0. Also a ≥ κ and
   η_a ≥ η_{κ−1} > 1 when p ≤ κ^κ/2 (`prop:app-s2-barrier`(iii)), so ℓ_a = 0.
5. *(iii), P meeting a set J of at most κ−1 columns.* The B_j, j ∈ J, are independent, so
   π_𝓛(P) = Π_{j∈J} θ·Pr[P_j ⊆ Z_j] = Π_{j∈J} π(P_j), with each
   π(P_j) ∈ [ℓ_{a_j}, ū_{a_j}].
   - *Lower bracket, when η_a < 1.* η is nondecreasing, and
     Π ρ_{a_j}(1−η_{a_j}) ≥ ρ_a(1−η_a) (the merging step of `prop:app-s2-barrier`(iii), which
     needs only η_a < 1 and κ ≥ 3).
   - *Upper bracket.* This is Lemma U, raised to the power κ−1. ∎

**What Theorem B excludes.** At p ≤ κ^κ/2 the following cannot prove p ∉ E_2(κ): any
certificate that combines, by linear-programming duality,
- the exact law of one column,
- facts about at most κ−1 columns that are true under independence,
- the symmetries (ii),
- and any family of point-set brackets of any size, including one-sided brackets with η ≥ 1 on
  sets meeting all κ columns.

That class includes:
- every factorial or mixed moment E Π_j (n_j)_{m_j} of any orders (each is a sum of π(P));
- Bonferroni and inclusion–exclusion of any depth over columns and points;
- Chebyshev or Paley–Zygmund applied to any polynomial in the n_j;
- in particular, a second moment of Z = Π_j n_j. Under 𝓛, E Z = Σ_{P transversal} π_𝓛(P) = 0,
  while every bracket holds.

So the "joint law of all κ columns", at the level of Weil-controlled point statistics, carries
nothing beyond what O2 already excludes.

**Not covered.**
- Facts that are not inequalities on point-inclusion probabilities. Examples: deterministic
  statements holding for every y (an energy bound on each X(y)), the row-product structure
  π(P) = Π_i N_i(P)/p with N_i an integer count, and Janson-type inequalities, which need the
  product structure of the y_i.
- Any true two-column fact that is false under independence.

**Exact check [computed; `setlevel_check.out`].** The exact laws of X(y) over all y were
computed at (κ, p) = (3, 7), (3, 13), (5, 11) and (5, 31), and 𝓛 was built from them.
- θ = 0.163, 0.379, 0.0022, 0.0084 (all ≤ 1/2).
- Point sets up to size 6 or 8 were checked by column-size profile: 18, 60, 185 and 455
  profiles, with no bracket violated.
- At every all-column profile the lower bracket is vacuous: 8, 44, 6 and 6 profiles.
- At κ = 3 both primes have contractions (E_2(3) = ∅), which illustrates that Theorem B bars a
  method and says nothing about E_2.

## 5. Routes (c) and (d)

- **(c) ρ_rest and G near the thresholds.** No rigorous progress.
  - G and ρ_rest are statistics of the (C1)-configuration measure at λ ≈ κ^{−κ/2+o(κ)}.
  - The only rigorous handle (11-09 §12.13) is Weil at fixed κ, which starts at
    p ≈ κ^{(4+o(1))κ}.
  - These are exact frequency sums on the open stratum, so Theorem B does not apply to them.
    Theorem D says only that Betti-type bounds on them are useless below T_Del.
  - I found no input that controls the joint factorial moments of (b_K, m_K) at λ ≈ 1. The
    question of whether sparse patterns cluster in buckets by more than κ^{o(κ)} stays open.
  - Not attempted further.
- **(d) Sum-product and energy** [assessment].
  - The decisive sets are small. The columns have size about λ = O(1), and the partial last-row
    sets have size about κλ. Sum-product estimates say nothing about sets of bounded size.
  - Where the sets are large (index-κ coset intersections), the two- and four-fold additive
    statistics are cyclotomic numbers and Jacobi sums (11-05 Prop. 3). These are known to
    O(√p), and that error is genuine.
  - Any such input that becomes an inequality on point-inclusion probabilities falls under
    Theorem B. Deterministic per-y structure is the one form not excluded, and no usable
    statement of that kind was found.

## 6. Why (T1) is not reached: the missing input

By (1.1) and Theorem B, any proof below κ^κ/2 must give a lower bound for the averaged
transversal product

  Σ_{P transversal} Π_{i=1}^{κ−1} N_i(P) > 0,

and that bound must not come from per-row Weil brackets. Each factor is a one-variable count with
κ shifts. Its mean is O(λ), and at the relevant p it vanishes for most P.

So the input needed is cancellation among the κ^κ frequencies of a single row's κ-point sum,
averaged over P: Poisson-level accuracy instead of Weil's κ√p. This is the averaged form of the
Paley n-e.c. question (Weil: q > n²4^n; truth ≈ 2^n). Theorem D shows that cohomology with only
Betti and weight data cannot supply it either. A proof would need actual Frobenius-phase
information: equidistribution with constants κ^{o(κ²)}, or the OSC′ input of 11-09. No such
statement is known.

## 7. Data consistency (κ = 3, 5, 7)

No threshold below T_A is claimed for κ ≤ 13 (T_C > T_A there). Proved thresholds used:
- T_A(5) = 12658 > 181 = max E_2(5);
- T_A(7) = 4.94·10⁶ > 3221 = max E_2(7);
- E_2(3) = ∅.

Barriers restrict methods only. Each one is consistent with the data, because no method of its
class certifies below it:
- Theorem B at κ^κ/2 = 13.5, 1562 and 4.1·10⁵ for κ = 3, 5, 7: T_A, T_C and TH9 all fire
  above;
- Theorem D at T_Del = 181, 1.05·10⁵ and 7.9·10⁷: the κ = 3 Betti certificate first could fire
  at 181, and the exact-modulus certificate, which Theorem D does not cover, fires at 139.

## 8. Claim gates that stay false

- An exponent below κ, conditionally or not.
- Any threshold below T_A for prime κ ≤ 13.
- "Theorem D excludes weight-refined or exact-modulus certificates on the open stratum."
- "Theorem B excludes per-y deterministic structure, Janson-type product-structure inequalities,
  or two-column facts that fail under independence."
- The T_C bound and TH9 Corollary 3 as human-verified. They are AI-checked three times, not
  human-checked.
- Any statement about E_2(κ) itself.

## 9. Next

- **Next hard question.** Does the averaged transversal product (§6) admit a bound from an
  arithmetic input other than per-row Weil? The candidate is a Katz-type equidistribution of
  (N_1(P), …, N_{κ−1}(P)) as P varies, with constants κ^{o(κ²)}.
- **Cheapest test.** At κ = 5, p ≈ 1500–2500 (λ ≈ 0.5–0.8), compute the empirical joint law of
  (N_i(P))_i over random transversals P and compare it with i.i.d. Poisson(p/κ^κ).
- **Command.** None was run. A sketch: a new `transversal_law.py 5 p 10^6` in this folder,
  about 1 core-min per prime. Expected artifact: the histogram and the pairwise and higher
  correlations. Acceptance: the total-variation distance to i.i.d. Poisson is below 0.05 at
  every tested p. That would be evidence, not proof, that the missing input is true at κ = 5.
- **Paper.** Integrator's call:
  - relabel the T_C and 6κ^κ statements from "argued/conditional" to "proved, AI-checked";
  - optionally add Theorems B and D next to `prop:app-s2-barrier`. Nothing is applied here.

## 10. Adversarial self-check

1. *Is T2 really new?* No. It is TH2's and TH9's mathematics. My contribution is the
   re-derivation, the independent code, and pointing out that the paper's labels are more
   conservative than the reports. If TH2 Lemma D or the Weil citation (L–N 5.41, flagged in the
   appendix) is wrong, all of §2 falls with it.
2. *Theorem D citations.* Step 3 (tame Euler characteristic) is cited, not proved. If it failed
   for some e′, then (i) could fail for that e′. Step 4 is elementary. Step 2 is standard (SGA 4).
   The theorem bars only Betti and Weil-II bounds. The κ = 3 data show that bound is loose by
   one to two orders, so the barrier is real but narrow, and a weight computation could escape
   it. I state this in §3 rather than claiming more.
3. *Theorem D's counting.* I used #M ≤ p^{2κ−2} and the count κ^{κ²−1} − 1 of e′ ≠ 0. The
   certificate could drop frequencies whose sums are exactly 0. On the open stratum none is
   identically 0 for e′ ≠ 0 (H^{≥d}_c ≠ 0, since |χ_c| ≥ 1), but S_{e′}(M) could be 0 at a given
   p. A certificate that knows exact zeros is no longer a Betti certificate. So (ii) is stated
   for Betti bounds only.
4. *Theorem B, the merging lemma.* The two-part case was reduced to F(m) ≥ 0. It was checked
   numerically for m ≤ 10⁶ and analytically beyond, with monotonicity in κ and s argued from
   signs. The grid check covered a + b ≤ 300, not all sizes. The analytic proof covers all
   sizes. If the κ-monotonicity step were wrong for some small κ, the grid (κ ≤ 40) would
   probably have caught it.
5. *Theorem B's scope.* "Linear-programming duality over point probabilities" is precise.
   "Conditioning arguments" in general is not. Conditioning on a y-event that is not a function
   of X(y) is not modelled by 𝓛. So I claim exclusion only for certificates expressible through
   π(P), the single-column law and the symmetries.
6. *Hidden reliance on p ≤ κ^κ/2.* It is used twice: for θ ≤ 1/2 and for η_{κ−1} > 1. Both are
   cited from `prop:app-s2-barrier`. Above κ^κ/2 Theorem B says nothing, consistent with TH9
   certifying from 6κ^κ.
7. *Data.* The κ = 3 support split shows full-support maxima of 7–11 p², above 5p². That does
   not contradict Theorem D, which is a lower bound on the Betti bound. It does show that for some e′ the cohomology is not concentrated in degree 4 with dimension β_3.

## 11. Artifacts (`2026-11-13-rees-square-gap-analytic/`)

| file | content |
|---|---|
| `tc_vs_ta_prime.py`, `.out` | independent T_A and T_C for prime κ ≤ 71 (§2) |
| `beta_arrangement.py`, `beta_table.out`, `beta_brute.out` | β_κ = \|χ_c(M)\|, T_Del, and the point-count check (§3) |
| `k3_open_stratum.py`, `.out`; `k3_open_stratum_chunked.py`, `.out` | κ = 3 exact S_{e′}(M), p ≤ 181 (§3) |
| `k3_support_types.py`, `.out` | κ = 3 sizes by support class (§3) |
| `setlevel_check.py`, `setlevel_check.out`, `merge_check.out` | Theorem B: merging grid and exact pseudo-law checks (§4) |
| `lemmaU_Fm.py`, `.out` | Lemma U, F(m) ≥ 0.45 for m ≤ 10⁶ (§4) |

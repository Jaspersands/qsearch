# Two-level SDE threshold, round 4: the refined (stratified) character-sum bound

3 November 2026 (written on the night of 2 November). AI-only research pass. It is not
a human review, a Lean proof or a priority claim. **"AI-checked, pending human review"
applies to every claim below.** Written incrementally; sections are appended as they are
finished.

Labels: **[proved]** written proof here; **[exact]** complete finite computation (script
named); **[float]** exact sums evaluated in floating point; **[argued]** heuristic.

Notation as in `2026-11-03-rees-threshold-3.md` (below "TH3") §2:
N_c = #{(α,β) ∈ F_p^{2κ} : α_j + β_i ∈ Q_{c_ij} ∀ i,j} (all cells nonzero),
S_e = Σ_{α,β} Π_ij χ^{e_ij}(α_j+β_i) with χ^s(0) = 0, so N_c = κ^{−κ²} Σ_e ω^{−⟨e,c⟩} S_e;
c_0 = (−(i+j)) is the Rees pattern; h = (p−1)/κ.
Scripts: `2026-11-03-rees-threshold-4/`, run with `/opt/anaconda3/bin/python`.

**Question (TH3 §2 "Scope", §7(ii)).** TH3's Theorem O1 is witnessed by degenerate
configurations (all α_j equal). Does a refined certificate, which treats the degenerate
strata exactly and bounds only the rest term by term, certify a threshold T_R(κ) < T_A(κ)
for κ ≤ 12? Heuristic target: (κ−1)^{κ+1}.

## 0. Verdict

See §0′ below (written after the computations). In one line: the refined bound fails;
nothing below T_A is proved; even ideal refined bounds beat T_A only at κ = 3.

## 1. The refined expansion [proved]

**Strata.** For a configuration (α,β) let π(α), ρ(β) be the set partitions of the column and
row indices by equality. The discrete stratum is D = {all α_j distinct, all β_i distinct}.

**Lemma R0 [proved].** Every configuration counted by N_{c_0} lies in D. *Proof.* Row 0 has
α_j + β_0 ∈ Q_{−j}, distinct cosets for distinct j, so the α_j are distinct; column 0 gives
the same for the β_i. ∎

Hence N_{c_0} = N^D_{c_0} := #(D ∩ {pattern c_0}), and for any union U of strata with D ⊆ U,
N_{c_0} = N^U_{c_0}. Every degenerate stratum contributes exactly 0 to c_0: this is the
"exact handling" of the degenerate configurations. The refined expansion is

    N^D_c = κ^{−κ²} Σ_e ω^{−⟨e,c⟩} S^D_e,   S^D_e = Σ_{(α,β)∈D} Π_ij χ^{e_ij}(α_j+β_i),

and the refined term-by-term certificate is (R): L1^D := Σ_{e≠0} |S^D_e| < S^D_0.
Two other unions are tested: U_full (TH3's expansion) and U_min = U_full minus
{all α_j equal} minus {all β_i equal} (the O1 witnesses only).

**Lemma R1 (scaling) [proved].** S^D_e = 0 unless Σ_ij e_ij ≡ 0 (mod κ). *Proof.* D is
invariant under (α,β) ↦ λ(α,β), λ ∈ F_p^×, and the product picks up χ(λ)^{Σe}. ∎
At κ = 3 every balanced e ≠ 0 has S^D_e ≠ 0 (6560 = 3^8 − 1 nonzero sums, §2), so the
13122 + 2670 zeros of TH3's full expansion split as: 13122 from scaling, and the rest are
artefacts of the degenerate strata (they are nonzero once the strata are separated).

## 2. κ = 3, exact: the refinement does not beat T_A [exact]

`strata_k3.py` computes the exact integer pattern counts N^U_c for U ∈ {full, U_min, D}
(via column-code histograms over β, with injectivity corrections for D), and all 3^9 sums
S^U_e by FFT; `strata_k3.out`. It reproduces TH3/TH2 for U_full (L1/S0 = 2.514 at p = 61,
0.8932 at p = 139) and N_{c_0} = 0 at p = 7, 13 (strict contractions need zero cells
there, TH3 §3).

| p | 61 | 73 | 79 | **97** | 103 | 139 | 199 | 337 |
|---|---|---|---|---|---|---|---|---|
| L1/S0, U_full | 2.51 | | | | | 0.893 | | |
| L1/S0, U_min | 2.58 | | | | | 0.909 | | |
| L1/S0, D | 1.815 | 1.342 | 1.206 | **0.903** | 0.850 | 0.561 | 0.361 | 0.192 |
| max_c N^D_c/μ^D | 1.29 | 1.23 | 1.23 | 1.16 | 1.16 | 1.12 | 1.08 | 1.05 |
| min_c N^D_c/μ^D | 0.30 | 0.37 | 0.47 | 0.49 | 0.51 | 0.68 | 0.76 | 0.85 |

- (R) fails at every prime p ≡ 1 (mod 3) with p ≤ 79 and holds at every tested prime
  97 ≤ p ≤ 337. **So the best possible refined term-by-term certificate at κ = 3 (it uses
  the exact value of every |S^D_e|) certifies exactly from p = 97, which is above
  T_A(3) = 79.04.** Any refined bound B_e ≥ |S^D_e| is at least as weak.
- Removing only the O1 witnesses (U_min) makes things slightly worse than U_full.
- Pattern-blind check: max_c|N^D_c − μ^D| < μ^D already at p = 37 (min/μ = 0.19, max/μ =
  1.57). So the pattern-blind obstruction of TH3 O1 no longer binds in D; the loss is the
  triangle inequality over e (≈ factor 2 at p = 97).

**Where the mass goes [exact].** `classes_k3.py` (`classes_k3.out`) splits L1^D by
v = number of rows + columns touched by supp(e) and z = number of zero cells.

| class (v, z) | # e | L1/S0 at p = 97 | 199 | 337 | rms |S_e| / p^{κ+1} at 97 / 199 / 337 |
|---|---|---|---|---|---|
| v=3 (one row or column, e = (s,−s)) | 36 | 0.379 | 0.183 | 0.108 | 84.6 / 186 / 324 (≈ p) |
| v=4, z=5 (2×2 blocks) | 54 | 0.198 | 0.093 | 0.054 | 48.9 / 108 / 187 (≈ 0.55 p) |
| v=4, z=6 / z=7 | 84 / 36 | 0.074 / 0.008 | 0.028 / 0.002 | 0.012 / 0.0006 | 7.4–16.7 / 1.8–1.9 |
| v=5 (all z) | 996 | 0.098 | 0.023 | 0.008 | 0.11–5.5 |
| v=6 (all z) | 5354 | 0.147 | 0.035 | 0.0094 | 0.003–2.8 |
| total | 6560 | 0.903 | 0.361 | 0.192 | |

- The degenerate mass is **not** removed by passing to D: inclusion–exclusion moves it
  into the 36 one-line sums (v = 3) and the 54 full 2×2-block sums (v = 4), each of size
  ≈ S^D_0/p = p^{2κ−1}(1+o(1)). At p = 97 these 90 sums carry 0.58 of the 0.90.
- The sums touching every row and column (v = 2κ = 6) are of square-root size on the
  (2κ−2)-dimensional orbit space: mean |S^D_e|/p^{κ+1} ≈ 0.22 (p = 97), 0.19 (p = 337).
  That is about 4.5 times *smaller* than the random-phase value 0.886·√(S_0 p(p−1))/p^{κ+1}
  ≈ 0.87.

## 3. κ = 3, exact: a hybrid refinement does beat T_A [exact]

The one-line and 2×2 sums of §2 are low-dimensional: Σ_{supp e ⊆ A} ω^{−⟨e,c⟩}S^D_e =
κ^{|A|}·#{(α,β) ∈ D : the cells in A have the pattern c|_A}, a marginal count on a set A of
cells meeting at most 4 rows + columns, which is a two-variable count after translation and
scaling. So they can be **kept with their phases** instead of being bounded in absolute
value. Hybrid certificate (H_V): with v(e) as in §2,

    M_V := S^D_0 + Re Σ_{0<v(e)≤V} ω^{−⟨e,c_0⟩} S^D_e   >   L1_{>V} := Σ_{v(e)>V} |S^D_e|.

`hybrid_k3.py` (`hybrid_k3.out`; it checks Σ_e ω^{−⟨e,c_0⟩}S^D_e = κ^{κ²}N_{c_0} exactly at
every p):

| p | 37 | 43 | 61 | 73 | 79 | 97 |
|---|---|---|---|---|---|---|
| V = 3: M/S0, L1_{>3}/S0 | 1.51, 3.19 | 1.44, 2.39 | **1.31, 1.21** | 1.25, 0.83 | 1.23, 0.74 | 1.19, 0.52 |
| V = 4: M/S0, L1_{>4}/S0 | 1.10, 2.11 | 1.06, 1.53 | **1.00, 0.69** | 0.99, 0.43 | 1.03, 0.36 | 0.98, 0.24 |
| V = 5: M/S0, L1_{>5}/S0 | 1.07, 1.33 | **1.07, 1.00** | 0.97, 0.43 | 0.95, 0.25 | 1.01, 0.20 | 0.99, 0.15 |

So with exact values, (H_3) and (H_4) hold at every prime p ≡ 1 (mod 3) from 61 to 199,
and (H_5) from 43 to 199; all fail at p ≤ 37 (H_5) and p ≤ 43 (H_3, H_4).
**The hybrid refinement certifies at κ = 3 from p = 61 (V = 3, 4) or p = 43 (V = 5), below
T_A(3) = 79.04 but above (κ−1)^{κ+1} = 16.** This is "exact" only as a statement about the
best bound of this shape: it uses the exact |S^D_e| for v > V, which no theorem supplies (§5).

## 4. Why the degenerate mass survives, and the (κ−1)^{κ+1} heuristic

**Lemma R2 (one-line sums) [proved].** Let e = s(δ_{(i,j)} − δ_{(i,j′)}) with s ≢ 0, j ≠ j′
(v = 3). Then

    −(2κ−2)·S^D_0/(p−2κ+1) ≤ Re S^D_e,  |S^D_e| ≤ (2κ−2)·S^D_0/(p−2κ+1),

and S^D_e = −Σ_Ω 1 + R_e with |R_e| ≤ (2κ−3)·#Ω, where Ω is the set of configurations
of the other 2κ−1 coordinates.
*Proof.* Fix every coordinate except β_i, satisfying the D and nonzero-cell conditions off
row i. β_i must avoid B = {β_{i′} : i′ ≠ i} ∪ {−α_k : k}, which has exactly 2κ−1 elements
(β_{i′} = −α_k would zero cell (i′,k)). So S^D_0 = #Ω·(p−2κ+1). The Möbius map
r(b) = (α_j+b)/(α_{j′}+b) is a bijection F_p∖{−α_{j′}} → F_p∖{1}, so
Σ_{b ≠ −α_{j′}} χ^s(r(b)) = −1. Removing the other 2κ−3 points of B (the point −α_j gives
χ^s(0) = 0) changes this by at most 2κ−3. ∎

So for every e of this type the refined expansion contains a sum of size ≍ S^D_0/p, and
there are κ²(κ−1)² of them: κ·C(κ,2)·(κ−1) in rows (a row, an unordered column pair, and
s ∈ {1,…,κ−1}), and as many in columns (the same lemma with α and β exchanged). At κ = 3 they are ≈ −S^D_0/p each
(rms/p^{κ+1} ≈ 0.87p–0.96p, §2). Their total, ≈ κ²(κ−1)²/p, is polynomial in κ, so for large
κ they matter only below p ≈ κ⁴; at κ = 3 they are 36/p, the largest single class.

**The heuristic (κ−1)^{κ+1} undercounts [exact at κ = 3; argued in general].** It assumes
that only the (κ−1)^{κ²} full-support e matter and that each is of square-root size p^{κ+1}
on the (2κ−2)-dimensional orbit space. At κ = 3, p = 97, the 170 full-support e carry
L1/S0 = 0.025 of the total 0.903; the 5184 e that touch every row and column but have
zero cells carry 0.122; and the 1170 e touching ≤ 5 rows + columns carry 0.76.
- Zero cells do not make a sum smaller: the z = 1 class has larger rms than z = 0.
- Sums touching v < 2κ vertices are larger, ≍ p^{2κ+1−v/2} on the square-root heuristic
  (their orbit space has dimension v−2 and the other 2κ−v coordinates are free); the
  observed growth matches for v = 5, z = 3 (rms/p^4 ∝ p^{0.53}).
- So the correct count of square-root-size terms is ≈ κ^{κ²−1} (all balanced e touching every
  row and column), not (κ−1)^{κ²}, and the ideal threshold of any term-by-term bound on
  these terms is about (m_κ κ^{κ²−1})^{1/(κ−1)} ≈ m_κ^{1/(κ−1)}·κ^{κ+1}, where
  m_κ = mean |S^D_e|/p^{κ+1} over that class (+ the classes v = 2κ−1, 2κ−2, which are of
  comparable total size near p ≈ κ^{κ+1}). Compare T_A(κ) ≈ (κ−1)κ^κ: the ideal beats T_A
  only if m_κ < ((κ−1)/κ)^{κ−1}(1 + o(1)) ≈ 1/e, minus what the v < 2κ classes use up.

## 5. Where a proof of T_R fails [proved / argued]

A proof of an explicit T_R by the refined route needs, for every p ≥ T_R, (a) a lower bound
for the exact low-order term M_V, and (b) explicit bounds B_e ≥ |S^D_e| for every balanced
e with v(e) > V, with Σ B_e < M_V.

- (a) is available in principle [argued]: for v ≤ 4 the sums are marginal counts of at
  most 2×2 or 1×3 sub-patterns, i.e. two-variable counts after translation and scaling,
  expressible through cyclotomic numbers of order κ and Jacobi sums (Lemma R2 is the
  one-line case). This pass did not write these out; it evaluated them exactly per prime.
- (b) is where it fails. The only unconditional bound for S^D_e with v(e) = 2κ is iterated
  one-variable Weil plus Möbius inversion over the α-partitions (Lemma
  `lem:app-s2-weil-count` per column): |S^D_e| ≤ p(p−1)·Σ_β Σ_π |μ(π)| Π_B |T_{f_B}(β)|,
  dominated by the discrete partition with Π_j ((s_j−1)√p + κ) ≈ (κ−1)^κ p^{κ/2} per β.
  Summed over the ≈ κ^{κ²} tuples this certifies only for p ≳ (κ−1)²κ^{2κ}, i.e. T_W again
  [argued; it is TH3 O3 restated on D]. A square-root bound |S^D_e| ≤ C p^{κ+1} for
  v(e) = 2κ would be a Deligne–Katz statement for the graphic arrangement of K_{κ,κ},
  whose hypothesis (b) fails (TH3 §2, still true on D: the strata removal deletes
  configurations, it does not change the arrangement). No such estimate is known.
- So **no explicit T_R < T_A is proved for any κ**. The κ = 3 statements of §2–§3 are exact
  evaluations, per prime, of the best possible bound of each shape; they are not proofs
  for all p (and κ = 3 needs none: E_2(3) = ∅ is already proved).

## 6. κ = 4: the ideal refined bounds do not beat T_A(4) = 869 [exact low part + sampled]

`dsum.py` computes S^D_e exactly for any list of e (translation and scaling fix
β_0 = 0, β_1 = 1; Möbius inversion over the set partitions of the α's; the last β by an FFT
correlation). `test_dsum.py` checks it against the κ = 3 FFT values (relative error
< 3·10⁻¹⁷ at p = 31, 61) and against brute force at κ = 4, p = 5 and p = 13 (relative
error < 10⁻¹⁷). `kappa4.py p nsamp seed` then:
- computes every balanced e with v(e) ≤ 5 exactly (106 orbit representatives under row and
  column permutations and transposition; all placements) and the exact hybrid main term
  M_5 with the Rees phases;
- estimates L1 over the four classes with v ≥ 6 as (exact class size) × (sample mean of
  |S^D_e| over nsamp uniform members) **[float, sampled; heavy-tailed, standard errors
  shown]**. The class sizes sum with the low classes to 4^15 balanced tuples (checked).

| p | 401 | 857 | 1601 |
|---|---|---|---|
| samples per class | 100 | 800 | 400 |
| M_5/S0 (exact) | 0.936 | 0.975 | 0.985 |
| L1(v ≤ 5)/S0 (exact) | 1.147 | 0.432 | 0.197 |
| class (2,4)+(4,2) L1/S0 | 0.083 | 0.016 | 0.004 |
| class (3,3) | 1.87 | 0.49 (se 0.09) | 0.25 (se 0.08) |
| class (3,4)+(4,3) | 4.91 | 0.41 (se 0.03) | 0.064 |
| class (4,4) | 7.41 | 0.71 (se 0.03) | 0.147 (se 0.04) |
| L1(v ≥ 6)/S0 | 14.3 ± 2.3 | **1.62 ± 0.10** | 0.46 ± 0.08 |
| pure refined (R): L1/S0 | 15.4 | **2.05** | 0.66 |
| hybrid (H_5): M_5 vs L1(v≥6) | fails | **fails** | holds |

Two more primes (400 samples per class): p = 1009: L1(v≥6)/S0 = 1.16 ± 0.17 against
M_5/S0 = 0.968, so (H_5) fails (by about 1.1 standard errors) and (R) gives 1.51;
p = 1201: L1(v≥6)/S0 = 0.77 ± 0.11 against 0.985, so (H_5) holds and (R) gives 1.05 ± 0.11
(fails, marginally). Outputs: `kappa4_p{401,857,1009,1201,1601}.out`.
**So the ideal hybrid threshold at κ = 4 lies between about 1009 and 1201, and the ideal pure
refined threshold between about 1201 and 1601; both are above T_A(4) = 869** [sampled].

- At p = 857, the largest prime p ≡ 1 (mod 4) below T_A(4) = 869, both certificates fail by a
  margin far outside the sampling error: even with the exact |S^D_e| of every tuple, the
  refined route cannot certify p = 857. Dropping the heavy-tailed (3,3) class entirely
  still leaves 1.13 > 0.98.
- Mean |S^D_e|/p^{κ+1} over the 1.04·10⁹ tuples touching every row and column is
  m_4 ≈ 0.43, 0.42, 0.57 at p = 401, 857, 1601 (compare m_3 ≈ 0.2). The (3,3) class contains
  sums of size up to ≈ 30 p^{2κ−2}: structured tuples carrying transferred degenerate mass,
  as in Lemma R2.

## 7. κ = 5..12: how far an ideal refined bound could go [exact counts; argued sizes]

`extrapolate.py` (`extrapolate.out`) computes, exactly, the number N_full(κ) of balanced e
touching every row and column (N_full/κ^{κ²−1} = 0.816, 0.970, 0.997, then 1.0000 to 4 digits
for κ ≥ 7), and T_A(κ) by bisection on U_κ (it reproduces the appendix table). Suppose the
v = 2κ class has mean |S^D_e| = m·p^{κ+1}, and give every other class, and the exact
low-order term, for free (M = S0, all v < 2κ sums zero). Then the ideal threshold is at
least (m·N_full)^{1/(κ−1)}, and it is below T_A only if m < m*(κ) := T_A^{κ−1}/N_full:

| κ | 3 | 4 | 5 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|---|
| m* | 1.17 | 0.63 | 0.43 | 0.405 | 0.393 | 0.387 | 0.384 |
| ideal/T_A at m = 0.2 | 0.41 | 0.68 | 0.83 | 0.87 | 0.91 | 0.93 | 0.94 |
| ideal/T_A at m = 0.42 | 0.60 | 0.87 | 0.99 | 1.008 | 1.010 | 1.009 | 1.008 |
| (κ−1)^{κ+1}/T_A | 0.20 | 0.28 | 0.32 | 0.33 | 0.34 | 0.35 | 0.35 |

Observed: m_3 ≈ 0.19–0.22, m_4 ≈ 0.39–0.57 (§2, §6). The random-phase value is ≈ 0.87.
- **(κ−1)^{κ+1} is out of reach of every term-by-term bound, refined or not [argued].**
  Reaching it needs m ≤ m*·((κ−1)^{κ+1}/T_A)^{κ−1}, e.g. ≈ 4·10⁻⁶ at κ = 12, i.e. the typical
  square-root-size sum would have to be exponentially smaller than its square-root scale.
  Nothing in the κ = 3, 4 data points that way (m grows from κ = 3 to κ = 4).
- Even in the most favourable reading (m ≈ 0.2, all other classes free), the ideal gain
  over T_A for κ ≥ 5 is a factor 0.83–0.94, i.e. T_A·(1 − O(log(1/m)/κ)); with m ≈ 0.42 there
  is no gain at all for κ ≥ 6. The classes v = 2κ−1, 2κ−2 (which at κ = 4 carry as much as
  v = 2κ near p ≈ T_A) only make this worse [argued: they scale as κ^{(3−κ)/2} relative to
  v = 2κ at p ≈ κ^{κ+1}].

## 0′. Verdict

**The target is not reached, and it fails at a precise place.**

1. *Exact handling of the degenerate strata* (Lemma R0: the Rees count lives on the
   discrete stratum D) removes TH3's O1 witness — on D no coset pattern is over- or
   under-full beyond (0, 2μ) already from p = 37 at κ = 3 — but it does **not** remove the
   degenerate mass. Inclusion–exclusion moves it into κ²(κ−1)² one-line sums and the
   2×2-block sums, each ≍ S^D_0/p (Lemma R2 **[proved]**; sizes **[exact]** at κ = 3).
2. *Pure refined certificate* (every e ≠ 0 bounded in absolute value, even by its exact
   value): at κ = 3 it first holds at p = 97 > T_A(3) = 79.04 **[exact]**; at κ = 4 it fails at
   p = 1201 and holds at 1601, against T_A(4) = 869 **[sampled]**. It does not beat T_A.
3. *Hybrid certificate* (sums touching ≤ 5 rows+columns kept exactly with the Rees phases,
   the rest bounded by their exact values): at κ = 3 it holds from p = 61 (V = 3, 4) or 43
   (V = 5), below T_A(3) **[exact]**; at κ = 4 it fails at p = 857 and 1009 and holds at 1201,
   so its threshold lies between 1.16·T_A(4) and 1.38·T_A(4) **[sampled]**. The κ = 3 gain does not persist.
4. For κ = 5..12 even the ideal hybrid can gain at most a factor ≈ 0.83–0.94 over T_A, and
   only if the typical full-support sum is ≤ 0.2 p^{κ+1}; the heuristic (κ−1)^{κ+1} would need
   it exponentially smaller **[argued, exact counts]**. The heuristic was wrong because it
   counted only the (κ−1)^{κ²} full-support tuples; the ≈ κ^{κ²−1} tuples touching every row
   and column, zero cells allowed, are all of the same size (§4).
5. Independently of 2–4, no unconditional bound for the v = 2κ sums on D beats iterated
   Weil, which gives back T_W ≈ κ^{2κ} (§5). **No explicit T_R < T_A is proved for any κ.**

## 8. Statement that now holds

AI-checked, pending human review. Access model unchanged (arbitrary columns; scalars are
public precomputation depending only on (p, κ, ξ)).
- (a) Unchanged: p ∉ E_2(κ) for p > min(T_A(κ), T_C(κ)); E_2(κ) known exactly for κ ≤ 7.
- (b) **[proved]** N_{c_0} = N^D_{c_0} (Lemma R0); S^D_e = 0 unless Σe ≡ 0 (Lemma R1); each
  one-line sum satisfies |S^D_e| ≤ (2κ−2)S^D_0/(p−2κ+1) and Re S^D_e = −#Ω + O((2κ−3)#Ω)
  (Lemma R2).
- (c) **[exact, κ = 3]** With exact values of all 3^9 sums S^D_e: the pure refined certificate
  holds at the primes p ≡ 1 (mod 3) with 97 ≤ p ≤ 337 and fails at every p ≤ 79; the hybrid
  certificates hold for 61 ≤ p ≤ 199 (V = 3, 4) and 43 ≤ p ≤ 199 (V = 5) and fail below.
- (d) **[sampled, κ = 4]** With the exact low part and sampled high classes: the hybrid
  certificate fails at p = 857, 1009 and holds at 1201, 1601; the pure one fails at 857,
  1009, 1201 and holds at 1601. T_A(4) = 869.
- (e) **[argued]** For κ ≥ 5 no refined term-by-term bound can reach (κ−1)^{κ+1}; it can gain at
  most a factor (m*/m)^{1/(κ−1)} over T_A, where m is the true mean size of the
  full-support-class sums in units of p^{κ+1}.

## 9. Still missing

- A proof of any square-root bound |S^D_e| ≪ p^{κ+1} on D for tuples touching every row and
  column — the single estimate a refined proof needs. Without it the route gives T_W.
- Closed forms (cyclotomic/Jacobi) for the v ≤ 5 main term M_V, valid for all p.
- κ = 4 to more samples (the (3,3) class is heavy-tailed: max ≈ 30p^{2κ−2}); identifying the
  structured heavy tuples there and treating them exactly as well (they move the κ = 4
  hybrid threshold only within the 1009–1201 bracket unless they dominate, which the data
  at 857 rule out: removing the class leaves 1.13 > 0.98).
- Any κ ≥ 5 computation (4^16-scale tuple counts become 5^25; only sampling is possible).
- A human check of Lemmas R0–R2 and of `dsum.py`.

## 10. Claim gates that must stay false

- "T_R(κ) < T_A(κ) proved" for any κ; "threshold ≈ (κ−1)^{κ+1}" or "exponent below κ" proved.
- "The refined bound beats T_A for κ ≥ 4" (it does not at κ = 4, even ideally, per §6).
- "Exact handling of degenerate strata removes the O1 obstruction" as a positive result:
  it removes the pattern-blind witness but not the mass (Lemma R2).
- "No method can beat T_A": §7 covers only term-by-term bounds on the D expansion and its
  hybrids, and §7 is argued.
- The κ = 4 numbers as exact: they are sampled estimates with the standard errors shown.
- All gates of TH2 and TH3 unchanged; no priority or novelty claim.

## 11. Proposed paper text

**Target:** `main.tex`, Remark `rem:two-level-threshold-size`. Insert after the sentence
ending "…so nonsingular Deligne--Katz estimates do not apply (\file{…threshold-3.md},
Sections~2--3)." and before "A sub-family of the problem…". **Status label:** AI-checked,
pending human review.

```latex
Treating the degenerate configurations exactly does not change this picture. Every contraction counted lies in the stratum where the $\alpha_j$ are distinct and the $\beta_i$ are distinct, and on that stratum no coset pattern is overfull; but inclusion--exclusion moves the degenerate mass into $\kappa^2(\kappa-1)^2$ one-line character sums and the $2\times2$-block sums, each of size about $p^{2\kappa-1}$, while the roughly $\kappa^{\kappa^2-1}$ sums that involve every row and column are at best of square-root size $p^{\kappa+1}$, a bound no known estimate supplies. With the exact value of every sum, the refined term-by-term certificate first holds at $p = 97 > T_A(3)$ for $\kappa = 3$; keeping the low-order sums with their phases lowers this to $p = 43$, but at $\kappa = 4$ the same hybrid certificate still fails at $p = 1009 > T_A(4)$ in a sampled evaluation, and for larger $\kappa$ such certificates can improve on $T_A(\kappa)$ by at most a factor tending to $1$, far from $(\kappa-1)^{\kappa+1}$ (\file{research/audits/reviews/2026-11-03-rees-threshold-4.md}).
```

No change to theorem statements, Table `tab:main-regimes` or `appendix-schedule2.tex`.

## 12. Artifacts (`2026-11-03-rees-threshold-4/`)

| file | role |
|---|---|
| `strata_k3.py`, `strata_k3.out` | κ = 3: exact N^U_c for U = full, U_min, D; L1/S0, pattern max/min, split by v |
| `classes_k3.py`, `classes_k3.out` | κ = 3, D: per-class counts, L1, rms, Parseval check |
| `hybrid_k3.py`, `hybrid_k3.out` | κ = 3, D: hybrid certificates H_V, V = 2..5, with N_{c_0} check |
| `dsum.py`, `test_dsum.py` | exact S^D_e for any κ, list of e; checks vs κ = 3 FFT and κ = 4 brute force |
| `kappa4.py`, `kappa4_p{401,857,1009,1201,1601}.out` | κ = 4: exact v ≤ 5 part + sampled v ≥ 6 classes |
| `extrapolate.py`, `extrapolate.out` | N_full(κ), T_A(κ), m*(κ), ideal/T_A, κ ≤ 12 |

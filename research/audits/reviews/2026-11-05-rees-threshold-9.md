# Two-level SDE threshold, round 9: joint column moments reach the β-averaging barrier; the exponent is unchanged

5 November 2026 (overnight pass). AI-only research pass, not a human review, not a Lean proof,
not a priority claim. **"AI-checked, pending human review" applies to every claim below.**

Labels: **[proved]** full proof written here; **[computed]** complete finite computation (script
named); **[cited]** proved in an earlier report or in the appendix; **[conjecture]** heuristic;
**[argued]** an argument that is not a complete proof.

Scripts and outputs: `2026-11-05-rees-threshold-9/` (interpreter `/opt/anaconda3/bin/python`,
mpmath 1.3; every run under `nice -n 10`, at most two processes, each well under 1 GB).
Notation as in `docs/papers/rees-hsp/appendix-schedule2.tex`: p prime, κ | p − 1, h = (p−1)/κ,
Q_m the m-th coset of the κ-th powers, Q°_m = Q_m ∪ {0}, ind(x) the coset index, and a
two-level contraction is (α, β) with α_0 + β_0 ≠ 0 and α_j + β_i ∈ Q°_{−(i+j)} for all
i, j ∈ Z_κ. Throughout

    Λ := (p − 1)/κ^κ = h/κ^{κ−1},   μ := κ e^{−Λ}.

(Λ is the λ of TH2 §2 and, up to a factor 1 + O(κ/p), the mean E n_j = h^κ/p^{κ−1}.)
TH2, …, TH8 are the earlier threshold reports (`2026-11-02-rees-threshold-2.md`, …,
`2026-11-05-rees-threshold-8.md`); TH3's barriers O1–O3 and TH5 §2–3 are used as stated there.

## 0. Verdict

- **Goal (a threshold κ^{(1−ε)κ}, or even κ^{κ−ω(1)}, for the two-level construction): not
  reached.** No exponent below κ is proved. The square gap between κ^κ and κ^{(κ+1)/2} stays
  open.
- **What is proved instead: the β-averaging route of T_A is pushed to its barrier.**
  1. *Lemma 2 and Theorem 1 [proved].* For uniform β, the joint factorial moments of the column
     counts n_j = |X_j(β)| are controlled by the Weil bound for up to about κ/2 points at once
     (Lemma 2). A double Bonferroni inequality, over columns and over points, turns them into an
     explicit certificate F_κ(p) > 0 for p ∉ E_2(κ) (Theorem 1). Every term of F_κ is a closed
     form.
  2. *Corollary 3 [proved; one input cited].* **For every κ ≥ 729 and every prime p ≡ 1 (mod κ)
     with p ≥ 6κ^κ + 1, p ∉ E_2(κ).** The large-Λ range uses TH2 Theorem 5 with m = 2 [cited].
     This replaces the best earlier asymptotic bounds, T_A ≈ (κ−1)κ^κ = κ^{κ+1−o(1)} (appendix)
     and 4e⌈ln 4κ⌉²κ^κ + 1 (TH2 Cor. 5′), by O(κ^κ).
  3. *Remark 5 [proved].* Theorem 1 cannot certify any p ≤ κ^κ/2: the
     Benjamini–Gurel-Gurevich–Peled law behind TH3's O2 satisfies every bracket that Theorem 1
     uses. So every certificate built from Weil-controlled joint moments of at most κ − 1
     columns (that is, every certificate of Theorem 1's kind) is pinned down within a factor 12
     for κ ≥ 729. Below κ^κ/2 it is not a matter of better constants. This does not rule out
     uniform-β arguments that use the full joint law of all κ columns.
- **Computed.**
  - Pointwise certificate starts Λ*(κ). The certificate fires from Λ ≈ ln κ for 28 ≤ κ ≤ 100,
    and from Λ*(κ) = 4.52–4.75 for 150 ≤ κ ≤ 1000. On a fine grid it gives no positive F for
    any κ ≤ 27; the first κ is 28 (window Λ ∈ [3.397, 4.034]).
  - Interval covers (§3.2) did not complete: the naive interval scheme needs relative widths
    10^{−6} (R = 1) to below 10^{−10} (R = 3). Only κ = 80, Λ ∈ [4.43, 4.92], was covered.
    So the pointwise windows are not thresholds for κ < 729.
  - Exhaustive checks of Lemma 2 and of every Bonferroni step at κ = 3, 4. These are 3138
    checks with 0 failures.
  - A synthetic test of the algebra.
  - Theorem 1 never certifies any of the 2214 known members of E_2(κ), 4 ≤ κ ≤ 16.
- **Unchanged for the paper.** For the small κ of the paper (κ ≤ 16), and indeed for all
  κ ≤ 27, Theorem 1 certifies nothing new. T_A, the explicit κ = 8 witnesses and the exact E_2 data are unaffected.
- **Why the exponent was not reached.** §4 takes the brief's four methods in turn. In every one
  the decoupled last unknown still faces κ coset conditions (Lemma 4), so its expected
  number of solutions is below p/κ^κ. Getting below κ^κ needs the κ-column statistic itself
  (TH3 O3), or an algebraic family whose provable threshold is not twice its first-moment
  exponent (TH6 §6.2). Neither was found.

## 1. How T_A works, and the two places where it loses

Proposition `prop:app-s2-TA`:
- Draw y_1, …, y_{κ−1} uniformly and put y_0 = 0. Let X_j(y) be the set of x with
  x + y_i ∈ Q_{−(i+j)} for all i, and n_j = |X_j(y)|. If every n_j ≥ 1, then β = y with any
  α_j ∈ X_j(y) is a contraction with no zero entry.
- The rows are independent given x, so E n_j = h^κ/p^{κ−1} ≈ Λ.
- E n_j² needs only 2-point counts per row, that is the cyclotomic numbers. Their first-order
  deviations cancel because Σ_b δ_b = 0, so R = E n_j²/(E n_j)² ≤ 1 + 1/Λ + O(κ^5/p).
- Paley–Zygmund gives P(n_j = 0) ≤ 1 − 1/R ≈ 1/(1 + Λ). The union bound over κ columns then
  needs Λ > κ − 1, which is T_A ≈ (κ−1)κ^κ.

There are three separate losses. The third is the real one.
1. *Paley–Zygmund instead of the Poisson tail.* The true P(n_j = 0) is ≈ e^{−Λ}. TH2's central
   moments reach Λ ≈ (ln κ)².
2. *The union bound over columns.* With i.i.d. Poisson columns, P(all n_j ≥ 1) = (1 − e^{−Λ})^κ
   > 0 for every Λ > 0. The union bound throws this away and needs μ = κe^{−Λ} < 1.
   Theorem 1 removes this loss down to Λ = O(1).
3. *E n_j = Λ < 1 for p < κ^κ.* No argument that averages over uniform β and reads only the
   joint laws of at most κ − 1 of the n_j can go below κ^κ/2 (TH3 O2; Remark 5 below). This
   is where the square gap begins.

So "pushing T_A's idea further", as the brief asks, ends at Θ(κ^κ) for every certificate that
reads at most κ − 1 columns at a time. Rounds 2 and 9 together do that. Anything below κ^κ/2
has to use the joint law of all κ columns (TH3 O3), or leave the β-averaging frame.

## 2. Proved results

Fix κ ≥ 3 and a prime p ≡ 1 (mod κ), and let y and n_j be as in §1. For S ⊆ Z_κ put
M_S = Σ_{j∈S} n_j. For m ≥ 0 put

    E_κ(m,p) = (m − 1 − m/κ + κ^{−m})√p + m/κ − mκ^{−m}  (m ≥ 1),  E_κ(0,p) = 0,
    η_m = κ^m E_κ(m,p)/(p − m),   ρ_m = (p − m)/(p κ^m),
    l_m(r) = C(rh, m) ρ_m^{κ−1} (1 − η_m)^{κ−1},   u_m(r) = C(rh, m) ρ_m^{κ−1} (1 + η_m)^{κ−1},

with C(N, m) = N(N−1)⋯(N−m+1)/m!. E_κ(m,p) is the error term of `lem:app-s2-weil-count`, in
its closed form. Note E_κ(1,p) = 0, so l_1 = u_1.

### 2.1 Joint factorial moments

**Lemma 2 [proved].** Let S ⊆ Z_κ with |S| = r ≥ 1, and let 1 ≤ m ≤ rh. Then
E C(M_S, m) ≤ u_m(r). If moreover η_m < 1, then E C(M_S, m) ≥ l_m(r).

*Proof.*
1. *The column sets are disjoint.* Row i = 0 has y_0 = 0, so X_j(y) ⊆ Q_{−j}. The X_j are
   therefore disjoint, and M_S = |⋃_{j∈S} X_j(y)|.
2. *Counting m-subsets.* Put D_S = ⋃_{j∈S} Q_{−j}, of size rh. For x ∈ D_S let j(x) ∈ S be
   the index with x ∈ Q_{−j(x)}. Then C(M_S, m) is the number of m-subsets T ⊆ D_S with
   x ∈ X_{j(x)}(y) for every x ∈ T. Row 0 holds automatically, so this says
   x + y_i ∈ Q_{−(i+j(x))} for all x ∈ T and all i = 1, …, κ−1.
3. *Rows are independent.* The y_i are independent, so
   P(T ⊆ ⋃_{j∈S} X_j) = Π_{i=1}^{κ−1} N_i(T)/p, where
   N_i(T) = #{y ∈ F_p : y − (−x) ∈ Q_{−(i+j(x))} for all x ∈ T}.
4. *Weil.* The m roots −x, x ∈ T, are distinct. `lem:app-s2-weil-count` with ℓ = m, c_k = 1
   gives |N_i(T) − (p − m)/κ^m| ≤ E_κ(m, p), that is N_i(T)/p ∈ ρ_m[1 − η_m, 1 + η_m].
5. *Sum.* Take the product over the κ − 1 rows and sum over the C(rh, m) sets T. ∎

*Remark.* The two-sided bound means the joint law of the n_j matches i.i.d. Poisson(Λ) in all
factorial moments of total order m, up to the relative error ≈ (κ−1)(m−1)κ^m/√p. This is
useful while κ^m ≪ √p/κ², that is for m ≲ κ/2 − 2 when p ≍ κ^κ. TH2's Lemma D is the case
|S| = 1. The new point is that one Weil count per row handles points from different columns at
once, because points of different columns lie in different cosets and so are automatically
distinct.

### 2.2 The certificate

**Theorem 1 [proved].** Let R ≤ κ be odd. For each r = 1, …, R choose an integer K_r ≥ 0, odd if
r is even and even if r is odd, with K_r ≤ rh, and with η_m < 1 for all m ≤ K_r (for every r:
both L_r and U_r use lower bounds l_m, for even m and odd m respectively).
Put

    L_r = Σ_{m=0}^{K_r} (−1)^m · (l_m(r) if m even, u_m(r) if m odd)     (r even),
    U_r = Σ_{m=0}^{K_r} (−1)^m · (u_m(r) if m even, l_m(r) if m odd)     (r odd),
    F   = 1 + Σ_{r even, r<R} C(κ,r) max(L_r, 0) − Σ_{r odd, r≤R} C(κ,r) min(U_r, 1),

where l_0 = u_0 = 1. If F > 0, then a fraction at least F of all y ∈ {0} × F_p^{κ−1} have every
X_j(y) nonempty, and so p ∉ E_2(κ).

*Proof.*
1. *Bonferroni for one integer.* For integers N, K ≥ 0,
   Σ_{m=0}^{K} (−1)^m C(N, m) = (−1)^K C(N−1, K) if N ≥ 1, and = 1 if N = 0.
   This follows by induction on K from C(N,K) = C(N−1,K) + C(N−1,K−1). Hence
   1[N = 0] − Σ_{m≤K} (−1)^m C(N,m) equals 0 for N = 0 and (−1)^{K+1}C(N−1,K) for N ≥ 1. So
   1[N=0] ≥ Σ_{m≤K}(−1)^m C(N,m) when K is odd, and ≤ when K is even.
2. *Inner step.* Apply step 1 to N = M_S. Since n_j ≥ 0, {M_S = 0} = ⋂_{j∈S}{n_j = 0}.
   - For |S| = r even and K_r odd, take expectations and use Lemma 2: E C(M_S, m) ≥ l_m(r) for
     even m and −E C(M_S, m) ≥ −u_m(r) for odd m. This gives P(M_S = 0) ≥ L_r, and also
     P ≥ 0.
   - For r odd and K_r even, symmetrically P(M_S = 0) ≤ U_r, and also P ≤ 1.
3. *Outer step.* Let W = #{j : n_j = 0}. By step 1 with K = R odd,
   1[W = 0] ≥ Σ_{r≤R} (−1)^r C(W, r). Also
   E C(W, r) = Σ_{|S|=r} P(⋂_{j∈S}{n_j = 0}) = Σ_{|S|=r} P(M_S = 0).
   The bounds of step 2 depend on S only through r, which gives P(W = 0) ≥ F. ∎

*Remarks.*
- F uses only the brackets of Lemma 2, and nothing else about the n_j. So P(W = 0) ≥ F holds
  for **every** random vector in ℕ^κ whose factorial moments E C(M_S, m), |S| ≤ R, m ≤ K_r, lie
  in [l_m(r), u_m(r)]. Remark 5 uses this.
- R = 1 is the union bound, with a Bonferroni bound for one column. TH2 §3.6 tried that
  single-column Bonferroni on a grid with κ ≤ 30 and found no certificate. That agrees with the
  computations here [computed, grid; independent check `scan_small.out`]: no positive F for
  κ ≤ 27; the first κ is 28, on Λ ∈ [3.397, 4.034]; κ = 29 fires on [3.41, 4.23] and κ = 30 on
  [3.45, 4.25]. These narrow windows lie between that grid's points.

### 2.3 Explicit consequence

**Corollary 3 [proved; range (C) cites TH2 Theorem 5].** Let κ ≥ 729 and let p ≡ 1 (mod κ) be a
prime with p ≥ 6κ^κ + 1. Then p ∉ E_2(κ).

*Proof.* Here Λ ≥ 6. Write u = e^{−Λ} and μ = κu. The proof splits the range of Λ into three
pieces.

*Range (C): Λ ≥ √(8κ). [cited]*
1. TH2 Theorem 5 states: if G_m(p) < 1 for some m ≥ 1, then p ∉ E_2(κ). Here
   G_m(p) = κ[λ^{−2m}A_{2m}(λ) + W_m(λ) max_{k≤2m} δ_k] with λ = Λ.
2. For m = 2, A_4(λ) = λ + 3λ² and W_2(λ) = 16 + 24/λ + 11/λ² + 1/λ³. TH2's moment-error
   step gives δ_k ≤ 2(κ−1)(ε* + 4/p) for k ≤ 4, with ε* = 8κ^4/√p, provided p ≥ 8 and
   (κ−1)ε* ≤ 1. At p ≥ √(8κ)κ^κ and κ ≥ 729 this side condition holds with enormous room
   (`verify_corollary.py` checks it).
3. At λ ≥ √(8κ): κλ^{−4}A_4(λ) = 3κ/λ² + κ/λ³ ≤ 3/8 + κ(8κ)^{−3/2}. W_2 is decreasing in λ
   and δ_k is decreasing in p, so κW_2(λ)·max_k δ_k is at most its value at λ = √(8κ), which
   is below 10^{−900} for κ ≥ 729.
4. So G_2(p) < 0.9 (`verify_corollary.py`, condition (C)).

*Two bounds used in (A) and (B).* Fix an integer K with RΛ ≤ K ≤ κ, and put x_r = rΛ.

(S1) *A uniform relative error.* For 1 ≤ m ≤ K and r ≥ 1,
x_r^m/m!·(1 − δ) ≤ l_m(r) and u_m(r) ≤ x_r^m/m!·(1 + δ), with δ := 3.1κKκ^K/√p, provided
(κ−1)η_K ≤ 1.
1. *η_m is nondecreasing in m.* In E_κ(m,p), the coefficient of √p has m-derivative
   1 − 1/κ − κ^{−m}ln κ > 0. The constant part m/κ − mκ^{−m} is nondecreasing for m ≥ 1. The
   factors κ^m and 1/(p−m) increase with m.
2. *Upper side.* C(rh,m) ≤ (rh)^m/m! and ρ_m ≤ κ^{−m}. Since (rh)^m κ^{−m(κ−1)} = x_r^m, this
   gives u_m ≤ (x_r^m/m!)(1 + η_K)^{κ−1}.
3. *Lower side.* C(rh,m) ≥ ((rh)^m/m!)(1 − m²/(rh)), ρ_m^{κ−1} ≥ κ^{−m(κ−1)}(1 − κm/p), and
   (1 − η)^{κ−1} ≥ 1 − (κ−1)η. This gives l_m ≥ (x_r^m/m!)(1 − K²/h − κK/p − (κ−1)η_K).
4. *Collecting.* (1 + η_K)^{κ−1} − 1 ≤ 2(κ−1)η_K because e^t − 1 ≤ 2t for t ≤ 1. Also
   η_K ≤ κ^K(K√p)/(p−K) ≤ 1.001Kκ^K/√p, and K²/h + κK/p ≤ 0.001κKκ^K/√p. Together these give
   δ ≤ 2.1κKκ^K/√p.

(S2) *Truncated sums.* For r even (K_r odd), L_r ≥ e^{−x_r} − x_r^{K_r+1}/(K_r+1)! − δe^{x_r}.
For r odd (K_r even), U_r ≤ e^{−x_r} + x_r^{K_r+1}/(K_r+1)! + δe^{x_r}. This combines (S1),
Σ_{m≤K} x^m/m! ≤ e^x, and Taylor's theorem with Lagrange remainder for e^{−x}.

Take K_r ∈ {K−1, K} of the required parity. Then K_r + 1 ≥ K ≥ x_r. Since n ↦ x^n/n! is
nonincreasing for n ≥ x, and K! ≥ (K/e)^K, the remainder is at most (e x_r/K)^K.

The binomial identity Σ_{r≤R} (−1)^r C(κ,r)u^r ≥ (1−u)^κ − C(κ,R+1)u^{R+1} (R odd) is step 1
of Theorem 1 applied to N ~ Bin(κ, u). With it,

    (★)  F ≥ (1−u)^κ − C(κ,R+1)u^{R+1} − Σ_{r=1}^{R} C(κ,r)(erΛ/K)^K − δ Σ_{r=1}^{R} C(κ,r) e^{rΛ}.

*Range (B): ln κ + 1.5 ≤ Λ ≤ √(8κ).* Take R = 1 and K = ⌈3.6Λ⌉. Then
F ≥ 1 − κ[e^{−Λ} + (eΛ/K)^K + δe^Λ], and the three terms are small:
1. κe^{−Λ} = μ ≤ e^{−1.5} < 0.2232.
2. (eΛ/K)^K is nonincreasing in K ≥ Λ, so κ(eΛ/K)^K ≤ κ(e/3.6)^{3.6Λ} ≤ κe^{−1.0112Λ} ≤ μ < 0.2232.
3. κδe^Λ ≤ 3.1κ²K̄κ^{K̄−κ/2}e^{√(8κ)}, with K̄ = 3.6√(8κ) + 1. Condition (B) of
   `verify_corollary.py` makes this ≤ 0.5/e < 0.19.

So F > 0.36. The side conditions hold: K ≤ κ, Λ ≤ K, and (κ−1)η_K ≤ δ ≤ 1.

*Range (A): 6 ≤ Λ < ln κ + 1.5.* This range is nonempty only for κ > e^{4.5}, and there
μ > e^{−1.5}. Take R = 2⌈2μ + 2⌉ − 1, so R is odd and 4μ + 3 ≤ R ≤ 4μ + 5. Take K = ⌈4RΛ⌉.
- *Main term.* (1−u)^κ ≥ exp(−κu/(1−u)) ≥ e^{−1.0025μ}, since u ≤ e^{−6}.
- *First error.* C(κ,R+1)u^{R+1} ≤ (eμ/(R+1))^{R+1} ≤ (e/4)^{R+1} ≤ e^{−1.5448(μ+1)}, which is
  < e^{−1.0025μ}/3.
- *Second error.* Σ_{r≤R} C(κ,r) ≤ (eκ/R)^R, and ln κ = Λ + ln μ with ln(μ/R) ≤ −ln 4. So
  Σ_{r≤R} C(κ,r)(erΛ/K)^K ≤ (e/4)^{4RΛ}(eκ/R)^R ≤ exp(R(−0.5448Λ − 0.3862)) ≤ e^{−3.655R}.
  Since R ≥ 4μ + 3, this is < e^{−1.0025μ}/3.
- *Third error.* δΣ_{r≤R} C(κ,r)e^{rΛ} ≤ δ exp(R(2Λ − 0.3862)). Put c_0 = 6e^{−6}; since
  Λe^{−Λ} decreases for Λ ≥ 1, μΛ ≤ c_0κ. Then:
  - RΛ ≤ 4c_0κ + 5(ln κ + 1.5);
  - K ≤ K̄_A := 16c_0κ + 20(ln κ + 1.5) + 1;
  - 2RΛ ≤ 8c_0κ + 10(ln κ + 1.5).

  Condition (A) of `verify_corollary.py`,
  (κ/2 − K̄_A) ln κ ≥ ln(3.1κK̄_A) + 8c_0κ + 10(ln κ + 1.5) + 1.0025κe^{−6} + ln 3 + 1, makes this
  error < e^{−1.0025μ}/3.

So F > 0 by (★). The side conditions hold: R ≤ κ, x_r ≤ RΛ ≤ K ≤ κ/2, and (κ−1)η_K ≤ 1.

*Where (A)–(C) hold.* `verify_corollary.py 6 100 1000000` evaluates (A), (B) and (C) for every
κ ≤ 10^6, with a margin of 1 in the logarithm. All three hold for every 729 ≤ κ ≤ 10^6. The last
failure is at κ = 728, from (A).

For κ > 10^6:
- (A): 16c_0 = 0.23796…, so K̄_A ≤ 0.2383κ, and the left side is ≥ 0.2617κ ln κ ≥ 3.61κ.
  The right side is ≤ 0.13κ + O(ln κ).
- (B): K̄_B − κ/2 ≤ −0.48κ, so the left side is −Θ(κ ln κ) against +O(√κ).
- (C): its last term is smaller still.

The same proof with L_0 = 5.5 in place of 6 gives the threshold 5.5κ^κ + 1 for κ ≥ 1677. Its
constants change: the main term becomes e^{−1.0041μ} (since u ≤ e^{−5.5}), the second error
becomes e^{−3.385R}, and c_0 = 5.5e^{−5.5}; both error comparisons still hold, and the script
(which now uses c_main = 1/(1 − e^{−L_0})) finds the last failure at κ = 1676. With L_0 = 5 the
proof fails, because 16c_0 > 1/2. ∎

### 2.4 The barrier for this method, and two structural facts

**Remark 5 (Theorem 1 cannot reach κ^κ/2) [proved].** Let p ≤ κ^κ/2. Then every F of
Theorem 1 (any odd R ≤ κ, any admissible K_r) is ≤ 0.

*Proof.*
1. *Only m ≤ κ − 2 occurs.* Write E_κ(m,p) = c(m)√p + d(m) with c(m) = m(1 − 1/κ) − 1 + κ^{−m}
   and d(m) = m/κ − mκ^{−m} ≥ 0. For m ≥ 2, c(m) ≥ c(2) = (1 − 1/κ)² ≥ 4/9. Hence
   η_{κ−1} ≥ κ^{κ−1}c(κ−1)/√p ≥ √2·κ^{κ/2−1}c(κ−1), using √p ≤ κ^{κ/2}/√2. This is
   √2·√3·4/9 = 1.09 at κ = 3, and it increases with κ, so η_{κ−1} ≥ 1. Since η_m is
   nondecreasing in m (Corollary 3, (S1) step 1), Theorem 1's condition η_m < 1 forces every
   K_r ≤ κ − 2.
2. *Setup.* Let ν be the true law of n_0. Then ν(n > 0) ≤ E n_0 = h^κ/p^{κ−1} < p/κ^κ ≤ 1/2.
   TH3's Lemma (BGP Prop. 26) gives a law Λ_BGP on ℕ^κ that is exactly ν^{⊗S} on every S with
   |S| ≤ κ − 1, and has Λ_BGP(all n_j > 0) = 0.
3. *Reduction to products.* By Vandermonde, C(M_S, m) = Σ_{m_1+…+m_r=m} Π_{j∈S} C(n_j, m_j).
   Each term involves at most m ≤ κ − 2 coordinates with m_j > 0, so E C(M_S, m) is the same
   under Λ_BGP and under ν^{⊗κ}, for every S including |S| = κ. Under ν^{⊗κ} it equals
   Σ Π_j E_ν C(n, m_j). Each factor lies in [l_{m_j}(1), u_{m_j}(1)], because ν is the true law
   and Lemma 2 applies with r = 1. Also Σ_{m_1+…+m_r=m} Π_j C(h, m_j) = C(rh, m).
4. *The product brackets lie inside [l_m(r), u_m(r)].* It suffices to show, for a, b ≥ 1 with
   m = a + b and η_m < 1,
   (i) ρ_aρ_b(1 − η_a)(1 − η_b) ≥ ρ_m(1 − η_m) and (ii) ρ_aρ_b(1 + η_a)(1 + η_b) ≤ ρ_m(1 + η_m).
   Merging two parts at a time then gives Π_j ρ_{m_j}(1 ± η_{m_j}) within ρ_m(1 ± η_m) for any
   composition; raise to the power κ − 1 and sum over compositions. (Parts equal to 0 are
   harmless, since ρ_0 = 1 and η_0 = 0.)
   - *Superadditivity.* c(m) − c(a) − c(b) = (1 − κ^{−a})(1 − κ^{−b}) ≥ 0 and
     d(m) − d(a) − d(b) = aκ^{−a} + bκ^{−b} − mκ^{−m} ≥ 0. So E_κ(a,p) + E_κ(b,p) ≤ E_κ(m,p).
   - *Hence η_a + η_b ≤ η_m/κ.* Indeed κ^a, κ^b ≤ κ^{m−1} and p − a, p − b ≥ p − m.
   - *The ρ factor.* ρ_aρ_b/ρ_m = (p − a)(p − b)/(p(p − m)) = 1 + ab/(p(p − m)) ≥ 1.
   - *(i).* (1 − η_a)(1 − η_b) ≥ 1 − η_a − η_b ≥ 1 − η_m, all factors are nonnegative, and
     ρ_aρ_b ≥ ρ_m.
   - *(ii).* (1 + η_a)(1 + η_b) ≤ 1 + η_m/κ + (η_m/(2κ))² ≤ 1 + (13/36)η_m, using κ ≥ 3 and
     η_m < 1. For the ρ factor, ab/(p(p − m)) divided by η_m equals ab/(pκ^m E_κ(m,p)), which is
     ≤ (m²/4)/(pκ^m·(4/9)√p) = (9/16)(m²κ^{−m})p^{−3/2} ≤ (1/4)p^{−3/2} < 0.023, because
     m²κ^{−m} ≤ 4/9 for κ ≥ 3 and p ≥ 5. So the left side of (ii) is at most
     ρ_m(1 + (13/36)η_m)(1 + 0.023η_m) ≤ ρ_m(1 + 0.4η_m).
5. *Conclusion.* Λ_BGP satisfies every bracket Theorem 1 uses, so the first remark after
   Theorem 1 gives 0 = Λ_BGP(W = 0) ≥ F. ∎

Numerical cross-checks of step 4: `o2_compat.py` (`o2_compat.out`), 7,801,598 pairs (m_1, m_2)
for 7 ≤ κ ≤ 400 at Λ ∈ {1/16, 1/4, 1/2}, 0 failures (it skips p < 1000(4κ+2), so it misses
κ ≤ 6); the independent check's `o2small.out` covers κ = 3, …, 7 at all small primes, 10117
pairs, 0 failures.

So every certificate of Theorem 1's kind (uniform β, Weil-controlled joint moments of at most
κ − 1 columns, together with TH2 Theorem 5 above √(8κ)κ^κ) has its threshold between κ^κ/2
and 6κ^κ for κ ≥ 729. Remark 5 says nothing
about arguments that use the joint law of all κ columns.

**Lemma 4 (decoupling forces κ conditions) [proved].** Fix some of the 2κ coordinates. Suppose
the remaining coordinates are split into blocks with no cell condition joining two different
blocks. Then either there is a single block, or every block lies entirely on the α side or
entirely on the β side. In the second case each α_j in a block faces all κ conditions of its
column, with all κ partners fixed.

*Proof.* Every pair (α_j, β_i) is joined by the cell (i, j). If one block contains α_j and
another contains β_i, that cell joins them. So when there are two or more blocks, either no
block meets the β side, or no block meets the α side. ∎

So the "decouple, then count one coordinate" step of T_A, T_W and every sequential scheme puts κ
fixed-root conditions on one variable. Over uniform fixed coordinates its mean count is
h^κ/p^{κ−1} < p/κ^κ (TH5 §3.4 states the sequential version).

**Lemma 6 (coset restrictions make no cell automatic) [proved].** Suppose Δ(p) < 1, as in
`lem:app-s2-cyclo`; this holds for p ≳ κ^4. Then for all s, t, m ∈ Z_κ there are a ∈ Q_s and
b ∈ Q_t with a + b ∈ Q_m.

*Proof.* Scale by a^{−1}. The claim becomes: some v ∈ Q_{t−s} has 1 + v ∈ Q_{m−s}. The number of
such v is a cyclotomic number. By the expansion in the proof of `lem:app-s2-cyclo`, applied with
two arbitrary cosets (the same character-sum computation), it is
(p − κ − 1)/κ² · (1 + O(Δ)) > 0. ∎

So restricting α_j or β_i to cosets, or to Gauss-period-type sets that are unions of cosets, adds
conditions and never removes one. This is the content of the brief's method (3) in its simplest
form.

## 3. Computations [computed]

### 3.1 Where the certificate fires (pointwise; `cert.py table`, `lamstar_big.py`)

Λ*(κ) is the first Λ on a 1% grid (0.2% in `cover.py`) where Theorem 1, with R and every K_r
optimised, gives F > 0 at p = Λκ^κ + 1, taking p as a real number. "Window end" is where it stops
again: the Bonferroni sums need K ≳ eΛ, and K is capped near κ/2 by Lemma 2.

| κ | Λ*(κ) | window end | best R | K_max | μ at Λ* | ln κ | TH2 T_C/κ^κ |
|---|---|---|---|---|---|---|---|
| ≤ 27 | none | – | – | ≤ 12 | – | – | 7.4–8.0 (κ ≥ 15) |
| 28 | 3.40 | 4.03 | 1 | 13 | 0.94 | 3.33 | – |
| 29 | 3.41 | 4.23 | 1 | 13 | 0.96 | 3.37 | – |
| 30 | 3.45 | 4.25 | 1 | 14 | 0.96 | 3.40 | 8.16 |
| 40 | 3.69 | 6.39 | 1 | 19 | 0.99 | 3.69 | 8.93 |
| 50 | 3.92 | 8.03 | 1 | 24 | 0.99 | 3.91 | ≈ 9.4 |
| 60 | 4.12 | 9.99 | 1 | 29 | 0.97 | 4.09 | 9.84 |
| 80 | 4.42 | 13.6 | 1 | 39 | 0.96 | 4.38 | ≈ 10.5 |
| 100 | 4.16 | 17.3 | 3 | 49 | 1.56 | 4.61 | 11.07 |
| 150 | 4.57 | – | 3 | 74 | 1.56 | 5.01 | – |
| 200 | 4.52 | – | 5 | 99 | 2.17 | 5.30 | 12.81 |
| 300 | 4.52 | – | 9 | 149 | 3.26 | 5.70 | – |
| 500 | 4.61 | – | 15 | 249 | 4.96 | 6.21 | – |
| 700 | 4.75 | – | 19 | 349 | 6.04 | 6.55 | – |
| 1000 | 4.71 | – | 29 | 499 | 9.04 | 6.91 | – |

*Reading the table.*
- For κ ≤ 80 the certificate fires at Λ ≈ ln κ, that is μ ≈ 1. This is the union-bound limit,
  reached with R = 1.
- From κ = 100 on, R ≥ 3 lets it go below ln κ, and Λ* levels off at 4.5–4.75.
- The rough asymptotic analysis behind Corollary 3 gives a limit near 4.85 (it needs
  12.9Λe^{−Λ} < 1/2). The optimised per-r choices do slightly better.
- For κ ≤ 27 there is no certificate, so T_A (κ ≤ 14) and T_C (κ ≥ 15) remain the best explicit
  thresholds there. The rows κ ≤ 29 come from the independent check's 0.1% grid
  (`2026-11-05-rees-threshold-9-check/scan_small.out`); κ = 26, 27 have max F ≈ −0.2.
- The T_C column is from TH2's `cm_table.out` and `cm_table_large.out`; "≈" marks values read
  between the tabulated κ.

### 3.2 Interval covers, attempted (`cover.py` → `cover.out`)

Pointwise positivity is not a threshold. `cover.py` covers [Λ_s κ^κ + 1, T_C(κ)] by a chain of
p-intervals [p_lo, p_hi]. On each one it evaluates Theorem 1 with p_lo in every η and every lower
bound, and p_hi in the upper binomial and ρ factors; all of these are monotone, so the interval
value bounds F at every p in the interval. T_C(κ) is computed with TH2's own
`central_moment.py` (m ≤ 10), whose G_m is non-increasing in p, so primes above T_C are covered
by TH2 Theorem 5. A completed cover would give the threshold T_9(κ) := Λ_s κ^κ + 1, where
Λ_s = 1.01·Λ* (Λ* from the 0.2% grid).

**Result: no cover completed; the naive interval scheme is too weak.** `cover.out` (run under
`nice -n 10`, stopped by this pass at the 30-minute budget):
- κ = 80: intervals verified with F > 0 cover Λ ∈ [4.4296, 4.9236] (14904 intervals, then the
  time cap), against T_C/κ^κ = 10.513. Rigorous up to floating-point rounding on that range.
- κ = 100: STUCK at the start Λ_s = 4.1803 with 0 intervals: even relative width 10^{−7}
  fails.
- κ = 150, 200, 60: not reached.

*Why.* The interval bound pairs p_hi in the upper terms with p_lo in the lower terms. Each
alternating sum has terms of size about e^{x_r} that cancel down to about e^{−x_r}, so a relative
width s costs about C(κ,r)·x_r e^{x_r}·s in F. At R = 1 this forces s ≈ 10^{−6} (about 10^5
intervals per κ); at R = 3 it forces s below 10^{−10}. A usable cover must bound the main
polynomial part Σ_m (−1)^m C(rh,m)ρ_m^{κ−1} over an interval as one function (for example by a
derivative bound on the alternating sum) and treat only the Weil part (1 ± η_m)^{κ−1} − 1 term by
term. That was not written in this pass.

*Consequence.* §3.1 is pointwise only. No explicit threshold below 6κ^κ + 1 is claimed for any
κ < 729; for those κ the best proved thresholds remain T_A and TH2's T_C. Corollary 3 does not
use §3.2.

### 3.3 Checks

- **Exhaustive, κ = 3 and 4** (`exact_check.py` → `exact_check_k3.out`, `exact_check_k4.out`).
  - Coverage: every y ∈ {0} × F_p^{κ−1}, for all primes p ≡ 1 (mod 3) up to 400 and
    p ≡ 1 (mod 4) up to 160.
  - Lemma 2: every S ⊆ Z_κ and m ≤ 4, the exact E C(M_S, m) against [l_m(r), u_m(r)].
  - Theorem 1, step 2: every S, P(M_S = 0) against the bound L_r or U_r that `cert.py` uses.
  - Theorem 1 itself: F ≤ P(all n_j > 0).
  - Result: 1591 + 1547 checks, 0 failures.
  - At these small primes K_max ≤ 2 and F < 0, as expected. The test exercises the brackets
    and the signs, not a firing certificate.
  - Side observation: P(all n_j > 0) stays about 3/p below (1 − e^{−Λ})^κ at large Λ, because
    y with a repeated coordinate empties every column. This is inside the Weil error, not a
    contradiction.
- **Synthetic algebra test** (`synthetic_check.py` → `synthetic_check.out`). For i.i.d.
  Binomial(H, Λ/H) columns, E C(M_S, m) = C(rH, m)(Λ/H)^m is exact. The assembly of Theorem 1 was
  run with brackets widened by d ∈ {0, 10^{−12}, 10^{−4}}, and also on a correlated law
  (n_j = Z·B_j with a shared Bernoulli Z). It never exceeds the true P(all > 0): 300 cases, 0 failures, 49 of them with F > 0.
  `o2_compat.py`: 7,801,598 pairs (m_1, m_2), 0 failures.
- **E_2 data** (`e2_consistency.py` → `e2_consistency.out`).
  - Data: every `INFEASIBLE` line in the small-prime, threshold-5 and threshold-8 folders:
    2214 members, 4 ≤ κ ≤ 16.
  - Result: F ≤ 0 at all of them (certified = 0). The largest member has Λ = 0.20 (κ = 4,
    p = 53); for κ ≥ 8 the largest Λ is ≤ 10^{−3}.
  - Theorem 1 fires only at Λ ≳ 3.4, so this agreement is automatic. It is recorded as a sanity
    check of the code, not as evidence.

## 4. The brief's four methods: what was tried, and why each stops at κ^κ

**(1) Sequential or greedy construction, with Weil counting at each step.**
- By Lemma 4, any order of the 2κ − 2 normalised unknowns ends with a decoupled unknown that
  faces κ fixed-root conditions (TH5 §3.4).
- *Uniform earlier choices.* Its mean count is < p/κ^κ. A second moment over the earlier
  choices is exactly T_A, and higher joint moments are exactly Theorem 1. For every
  certificate that reads at most κ − 1 columns at a time, the ceiling is κ^κ/2 (Remark 5).
- *Structured earlier choices.* The brief proposes β in a subgroup, α an arithmetic progression,
  or α = cβ^{−1}. Fixing structure removes the averaging, and the last step becomes a
  one-variable sum with κ fixed roots. Weil then needs p ≳ κ^{2κ} (T_W). The three ansätze in
  detail:
  - *β in a multiplicative subgroup or a root-of-unity orbit.* These are TH5's shift–scale
    families (Thm 2.2). Their first-moment exponents are ≥ (κ+1)/2 − 1/(2(κ−1)), and
    square-root methods need twice that (TH6 §6.2).
  - *Arithmetic or affine progressions without wrap-around* [proved arithmetic]. Take
    α_{j+1} = Aα_j + B and β_{i+1} = Aβ_i − B for 0 ≤ i, j ≤ κ−2, with ind A ≡ −2. Then
    M_{i+1,j+1} = A·M_{ij}, so every cell is fixed by the 2κ − 1 cells of the first row and
    first column. This is not one of TH5's families, which are cyclic. The family has 4
    parameters (α_0, β_0, A, B); translation (an orbit of size p) and Q_0-scaling (size h)
    leave about p^4/(ph) = κp² orbits, against 2κ − 1 hook conditions plus one coset condition
    on A, each of probability about 1/κ. The expected number of orbits is about p²κ^{1−2κ},
    so the first-moment exponent is κ − 1/2, and a square-root proof would need about
    κ^{2κ−1}. The family is no better than T_A even heuristically.
  - *α_j = c/β_j* [proved arithmetic]. The cell is (c + β_iβ_j)/β_j. Comparing cells (i,j) and
    (j,i) forces ind β_j to be constant. The family has κ + 1 parameters (β and c); the
    scaling β ↦ sβ, c ↦ s²c with s ∈ Q_0 has orbits of size h, and translation does not act.
    That leaves about κp^κ orbits against (κ − 1) + C(κ+1, 2) conditions, so the first-moment
    exponent is (κ+1)/2 + 1 − 2/κ > (κ+1)/2.

**(2) Lovász local lemma and Janson.**
- TH5 §3.2 proved that every local-lemma criterion fails here, because P(bad cell) = 1 − 1/κ
  ≥ 1/2 and cells share coordinates.
- TH5 §3.3 refuted Janson and every forest statistic on actual primes. The "each cell depends on
  two coordinates" structure is TH5's forest independence: the dependence lives on 4-cycles.
- Grouping the cells into column events is the column union bound. Theorem 1 replaces that
  union bound by its sharp Bonferroni form, and so it is the strongest version of this route.

**(3) Galois or Gauss-period ansätze.**
- TH5 Thms 2.2 and 2.4 classify the cell-permuting symmetries (shift–scale and transpose).
  None has a first-moment exponent below that of the full problem by more than 1/(2(κ−1)).
- By Lemma 6, restricting coordinates to cosets or unions of cosets never makes a cell
  automatic once p ≳ κ^4.
- *A Möbius-twisted ansatz* [argued]: α_j = g^j(a), β_i = −g^i(b) with g ∈ PGL_2(F_p), using
  g(x) − g(y) = det(g)(x − y)/((Cx + D)(Cy + D)). If C ≠ 0, this needs ind(Cg^n(a) + D) and
  ind(Cg^n(b) + D) to be constant along the orbits, together with ind(g^k(a) − b) = −k for
  |k| < κ. That is about 4κ conditions on about 3 parameters, an exponent near 4κ/3. If C = 0
  it is the affine family above.
- No ansatz was found that makes many cells equivalent while keeping a free-coordinate product
  structure for averaging.
- [conjecture] Any family with d parameters and n conditions has first-moment exponent
  ≥ (κ+1)/2 − o(1); otherwise its contractions would appear below the observed maximum of
  E_2. A square-root proof then needs about κ^{2n/d} ≥ κ^{κ+1−o(1)} (TH6 §6.2 [argued]).

**(4) Obstructions with few rows, combined with a construction.**
- TH8 Prop. 6 [cited] shows that r-row certificates of membership are void above
  ((r−1)κ^r + 2)².
- The converse fails on actual primes, so "no small obstruction" cannot be turned into
  existence:
  - E2row(5) = {11} (TH8 `tworow_np_k3-16.out`), yet 131 and 181 are in E_2(5).
  - TH3 §3's O2 laws are realised at κ = 4 (p = 37, 53) and κ = 5 (p = 131). There every κ − 1
    columns are jointly solvable for a positive fraction of β, and all κ never are.
- [argued] Any uniform-β existence proof below κ^κ/2 must therefore use the κ-column
  statistic E Π_j n_j (TH3 O3), or the joint law of all κ columns in some other form. That
  statistic is the count of contractions itself.

**Summary of the obstruction** [heuristic]. Below κ^κ, a typical β has some (indeed most)
n_j = 0. Existence rests on rare β for which all κ columns are solvable together;
heuristically P ≈ Λ^κ. Contractions come in Q_0-scaling orbits of size h, so existence needs
Λ^κ ≳ h/p^{κ−1}, which holds only above κ^{(κ+1)/2}. Two kinds of certificate are available,
and neither reaches the rare β:
- statistics on at most κ − 1 columns (O2, Remark 5);
- term-by-term or square-root estimates of the full count (O1, TH6 §6.2 [argued]), which stop
  at κ^κ and κ^{κ+1} respectively.

An exponent (1 − ε)κ would need either cancellation across the κ^{κ²} character tuples of the
full count, or a non-character-sum construction. It is the analogue of beating the averaging
bound log_2 p for patterned bicliques in a Paley-type graph. No method for that is known to this
pass, and no literature search was possible.

## 5. Claim gates, next question, next command

- **Gates that stay false:**
  - "exponent below κ proved" and "two-level threshold ≈ κ^{(κ+1)/2}";
  - "square gap closed";
  - any change to E_2(κ) for κ ≤ 16, to T_A, to Table `tab:app-s2-thresholds` or to Schedule 2;
  - any equivalence with Paley cliques;
  - any priority claim (Theorem 1 is a standard Brun/Bonferroni sieve applied to Weil-controlled
    moments).
  - `rees_hsp_reduction.json` and the registry are untouched.
- **What may be stated (AI-checked, pending human review):**
  - Corollary 3: p ∉ E_2(κ) for p ≥ 6κ^κ + 1 when κ ≥ 729. This relies on TH2 Theorem 5 for
    Λ ≥ √(8κ).
  - No certificate of Theorem 1's kind (Weil-controlled joint moments of at most κ − 1
    columns, uniform β) can go below κ^κ/2 (Remark 5).
- **Next hard question:** a certificate that uses all κ columns jointly in the regime Λ < 1 for
  one κ ≥ 8, for example a lower bound for E Π_j n_j with cancellation across e-tuples, valid
  below κ^κ/2. Equivalently: one prime in (Cκ^{(κ+1)/2}, κ^κ/2] certified without enumeration
  and without a symmetric ansatz.
- **Next command:** rewrite `cover.py` so each interval bounds the main polynomial part
  Σ_m (−1)^m C(rh,m)ρ_m^{κ−1} as one function of p (derivative bound on the alternating sum),
  keeping only the Weil part term by term; then
  `nice -n 10 /opt/anaconda3/bin/python cover.py 60,100,200,300,500,700 > cover2.out`.
  Separately, rerun `verify_corollary.py` with the exact (★) for 30 ≤ κ ≤ 728 instead of the
  crude closed forms.
  - Expected artifact: `cover2.out` with COVERED lines up to T_C/κ^κ.
  - Acceptance: COVERED from Λ_s ≤ 5 for κ ≥ 100, giving explicit thresholds O(κ^κ) below
    κ = 729; or a proof that (★) holds from some κ below 729.

## 6. Proposed text (AI-checked, pending human review; not applied)

### 6.1 Sentence for `main.tex`, Remark `rem:two-level-threshold-size`, after the sentence ending "the two-level threshold is at most $\kappa^{\kappa+o(1)}$."

```latex
A further AI-only report (\file{research/audits/reviews/2026-11-05-rees-threshold-9.md}, Corollary~3; pending human review) argues that bounding joint factorial moments of several column counts at once, followed by a Bonferroni inequality over columns, gives $p \notin E_2(\kappa)$ for every prime $p \equiv 1 \pmod\kappa$ with $p \ge 6\kappa^\kappa + 1$ when $\kappa \ge 729$, so the threshold is $O(\kappa^\kappa)$; it changes nothing for $\kappa \le 27$, and no certificate built only from these joint moments of at most $\kappa-1$ columns can go beneath $\kappa^\kappa/2$.
```

### 6.2 Remark for `appendix-schedule2.tex`, at the end of subsection `app:s2-TA` (after the remark on where the values of $\Delta$ and $U$ come from)

```latex
\begin{remark}[Joint moments of the column counts; AI-checked, pending human review]
\label{rem:app-s2-joint-moments}
The union bound over the $\kappa$ columns in Proposition~\ref{prop:app-s2-TA}(i) can be removed up to a constant. For a set $S$ of $r$ columns put $M_S = \sum_{j\in S} n_j$. The sets $X_j(y)$ lie in the distinct cosets $Q_{-j}$, so an $m$-subset of $\bigcup_{j\in S}X_j(y)$ is a set of $m$ distinct field elements, and Lemma~\ref{lem:app-s2-weil-count} with $\ell = m$, applied row by row, gives, the left inequality when $\eta_m < 1$,
\[
  \binom{rh}{m}\rho_m^{\kappa-1}(1-\eta_m)^{\kappa-1} \le \mathbb{E}\binom{M_S}{m} \le \binom{rh}{m}\rho_m^{\kappa-1}(1+\eta_m)^{\kappa-1},
  \qquad \rho_m = \frac{p-m}{p\kappa^m},\quad \eta_m = \frac{\kappa^m E_\kappa(m,p)}{p-m}.
\]
Since $\{M_S = 0\}$ is the event that every column in $S$ is empty, Bonferroni's inequalities in $m$ and then in $r$ bound the probability that some column is empty by an explicit expression. A report (\file{research/audits/reviews/2026-11-05-rees-threshold-9.md}) evaluates it and finds that every prime $p \equiv 1 \pmod\kappa$ with $p \ge 6\kappa^\kappa + 1$ lies outside $E_2(\kappa)$ when $\kappa \ge 729$; the range $p \ge \sqrt{8\kappa}\,\kappa^\kappa$ of that argument uses the fourth-moment bound of \file{research/audits/reviews/2026-11-02-rees-threshold-2.md}, Theorem~5. For $\kappa \le 27$ the expression is not positive at any point of a fine grid, so $T_A$ remains the threshold used here. The same report shows that no certificate built only from these brackets, for sets of at most $\kappa-1$ columns, can certify a prime $p \le \kappa^\kappa/2$.
\end{remark}
```

## 7. Artifacts (`2026-11-05-rees-threshold-9/`)

| file | content |
|---|---|
| `cert.py` | Theorem 1 certificate: `point`, `table` (pointwise windows), `interval` |
| `table_pointwise.out`, `lamstar_big.py`, `lamstar_big.out` | §3.1 |
| `cover.py`, `cover.out` | §3.2 interval covers, attempted; none completed (imports TH2 `central_moment.py`) |
| `verify_corollary.py`, `verify_corollary.out` | Corollary 3 conditions (A)–(C), κ ≤ 10^6, L_0 ∈ {6, 5.5, 5} |
| `exact_check.py`, `exact_check_k3.out`, `exact_check_k4.out` | exhaustive Lemma 2 / Bonferroni checks |
| `synthetic_check.py`, `synthetic_check.out` | algebra test on exact laws |
| `o2_compat.py`, `o2_compat.out` | Remark 5 bracket compatibility |
| `e2_consistency.py`, `e2_consistency.out` | no known E_2 member is certified |

## 8. Independent adversarial check (fresh general-purpose subagent, 5 November 2026)

**Verdict: accept with fixes.** The checker re-derived Lemma 2, Theorem 1, Corollary 3 and
Remark 5 from the appendix and TH2/TH3, and wrote its own code in
`2026-11-05-rees-threshold-9-check/`:
- `indep_F.py` (`compare.out`): an independent implementation of F, agreeing with `cert.py` to
  relative error ≤ 4·10^{−15} at κ ∈ {100, 200};
- `gap_l3.py` (`gap_l3.out`): shows that l_m is not a lower bound once η_m ≥ 1 (κ = 3,
  p = 31, m = 3: exact 0.042, formula 3.95), which motivated fix 1;
- `verify_A_L0.py` (`verify_A_L0.out`): range (A) with the exact constants, last failure 728
  at L_0 = 6 and 1676 at L_0 = 5.5;
- `scan_small.py` (`scan_small.out`): a 0.1% grid for 15 ≤ κ ≤ 29;
- `o2small.out`: the Remark 5 bracket inequalities for κ = 3, …, 7, 10117 pairs, 0 failures;
- `literal.out`: a literal reading of the certificate certifies none of 2216 known E_2
  members; `star.out`: at κ = 729, (★) and the full Theorem 1 are positive at sample points
  Λ ∈ [6, 76] of ranges (A) and (B).

None of the findings breaks the main line of proof (Lemma 2, Theorem 1's double Bonferroni,
Corollary 3's case split); finding 1 is a missing hypothesis that the code already
respected (`cert.prepare` stops at the first η_m ≥ 1). Findings and fixes:

| # | finding | fix applied |
|---|---|---|
| 1 | Theorem 1 required η_m < 1 only for even r, but U_r (odd r) also uses l_m for odd m; same in §6.2 | condition now for every r; §6.2 says "the left inequality when η_m < 1" |
| 2 | Barrier wording overclaimed: Remark 5 covers joint laws of at most κ − 1 columns, not every uniform-β argument | narrowed in §0, §1, §4(1), §4(4), §5, §6 |
| 3 | Remark 5: hypothesis R ≤ κ − 1 unnecessary; elementary inequality only checked numerically | hypothesis dropped (η_{κ−1} ≥ 1 forces K_r ≤ κ − 2, so even |S| = κ only sees ≤ κ − 2 coordinates); full proof written (superadditivity of E_κ, η_a + η_b ≤ η_m/κ, ρ-factor ≤ 0.023η_m); relabelled [proved] |
| 4 | κ > 10^6 tail: K̄_A ≤ 0.2381κ is false (16c_0 = 0.23796) | now 0.2383κ, left side ≥ 0.2617κ ln κ ≥ 3.61κ |
| 5 | L_0 = 5.5 claim used L_0 = 6's constants | constants stated (1.0041, −3.385); `verify_corollary.py` now uses c_main = 1/(1 − e^{−L_0}); result unchanged, κ ≥ 1677 |
| 6 | Corollary 3 wording: which term is < 10^{−900}; TH2's side condition (κ−1)ε* ≤ 1 unstated; "=" for "≤" in (B) | fixed; the script now checks (κ−1)ε* ≤ 1 |
| 7 | "never fires for κ ≤ 25" and "first κ between 26 and 30" imprecise; `cert.py table` usage wrong | now "no positive F for κ ≤ 27 [computed, grid]; first κ = 28 on [3.397, 4.034]"; table rows 28, 29 added; docstring fixed |
| 8 | §0 cover bullet did not match `cover.out`; RESULTS_3_2 unfilled | §3.2 filled from the rerun: no cover completed (κ = 80 covered only [4.43, 4.92]; κ = 100 stuck at the start); §0 and §5 now say the windows are pointwise only, and give the cause and the next command |
| 9 | §4 summary: "every n_j = 0" should be "some (most)"; the comparison should be Λ^κ against h/p^{κ−1} | fixed; this comparison gives exactly κ^{(κ+1)/2} |
| 10 | §4(1) exponents: affine family is κ − 1/2, not κ; α = c/β is (κ+1)/2 + 1 − 2/κ | fixed, with the orbit counts |
| 11 | §4(3) last bullet is heuristic; TH6 §6.2 is an argument, not a proof | labelled [conjecture] and [argued] |

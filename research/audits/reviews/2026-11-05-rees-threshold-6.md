# Two-level SDE threshold, round 6: a tower of coset refinements

5 November 2026 (pass run overnight 4–5 November). AI-only research pass. It is not a human
review, a Lean proof or a priority claim. **"AI-checked, pending human review" applies to every
claim below.**

Labels: **[proved]** written proof here; **[exact]** complete finite computation (script named,
every witness re-checked by an independent checker); **[float]** closed-form expressions
evaluated in 40-digit floating point; **[conjecture]**; **[argued]** heuristic.

Scripts and outputs: `2026-11-05-rees-threshold-6/` (interpreter `/opt/anaconda3/bin/python`,
C with `cc -O2`; all runs under `nice -n 10`, at most two processes). The compiled binaries
`rect`, `rectu`, `rectp` in that folder are scratch and should not be committed.

Notation as in `appendix-schedule2.tex`: p prime, κ | p − 1, ξ a coset generator for the
κ-th powers, cls(x) = ind(x) the coset index. For D | κ put P_D = (F_p^×)^D and
Q^{(D)}_m = ξ^m P_D, m ∈ Z_D, and Q^{(D)°}_m = Q^{(D)}_m ∪ {0}. Because ξ generates
F_p^×/P_κ, its image generates F_p^×/P_D, and the D-class of x is ind(x) mod D. So one ξ
and one coset test per element serve every modulus D | κ.

## 0. Verdict

- **The two-level square gap is not closed.** No proved threshold κ^A with A < κ for the
  two-level problem E_2(κ) itself was found. Routes (1), (2) and (4) of the brief fail at
  stated points (§6):
  - Kummer-type parametrisations only re-index the same character sums (Remark 6.1, proved).
  - Any family certified by square-root bounds needs p ≳ κ^{κ+1} (§6.2).
  - Fixing cells leaves a variable facing κ conditions (§6.3).
  - GRH adds nothing over Weil for complete sums. The only conditional statement that gives
    exponent (κ+1)/2 is the random-model count itself; it is stated as Conjecture 6.4, with
    its calibration on the exact data.
- **Route (3) succeeds partially: the gap can be bypassed for composite κ by changing the
  construction (§2–§4), at a price in arity.**
  - The *tower* refines the coset classes one prime factor of κ at a time.
  - Each refinement step needs a "rectangular" contraction. In it every unknown faces only
    r_t = D_t/D_{t−1} coset conditions, instead of κ.
  - **Strongest proved statement (Theorem 4.2) [proved].** Let κ ≥ 4 be composite, with
    prime factorisation κ = q_1 q_2 ⋯ q_L in nonincreasing order, so that q = q_1 is the
    largest prime factor. Let p ≡ 1 (mod κ) be prime with
    p > max( T_A(q)·[q ≥ 5], 4κ^{q+1}, 4q²κ^5 ) (an upper bound for Θ(κ) of Theorem 4.2),
    and in particular p > 4κ^{max(q+1, 7)}. Then any
    M = (a+1)·∏_{t=1}^{L}((q_t − 1)a + 1) ≤ κ(a+1)a^L
    columns in F_p^a admit a nonzero solution of Σ s_b^d λ_b = 0. The solution is computed
    from scalars that depend only on (p, κ, ξ). For κ = 2^L the threshold is
    ((κ−1)²+1)² < κ^4 and M = (a+1)^{L+1}. For 3-smooth κ it is 36κ^5.
  - So the threshold exponent drops from κ+1 to max(q+1, 7) when q < κ. That is below the
    exponent (κ+1)/2 at which the two-level construction itself first exists, once
    κ ≥ 2·max(q+1, 7) roughly. For example κ = 16 is covered from 51076 ≈ κ^{3.9}, whereas
    E_2(16) is believed to reach about κ^{8.5}.
- **Arity price [proved, elementary].** M has degree L + 1 = Ω(κ) + 1 in a. It is
  quadratic only for L = 1, which is the two-level construction itself. Route (3)'s "O(a²)"
  win is therefore **not** achieved: the tower is cubic for κ ∈ {4, 6, 9}, quartic for
  κ = 8, and of degree 1 + log_2 κ at worst. It sits strictly between Schedule 2 (degree 2)
  and Schedule 1 (degree κ⌈log_2(κ+1)⌉). For prime κ the tower is the two-level
  construction, and nothing changes.
- **Exact small-κ consequences [exact].** These combine Theorem 2.3 with complete searches
  below the proved step thresholds, and a second, independent checker re-verifies every
  witness. The tower and union chains cover every prime p ≡ 1 (mod κ) except:
  - κ = 4: {5, 13};
  - κ = 5: {11};
  - κ = 6: {7, 13, 19, 31, 43, 67};
  - κ = 7: {29, 43, 71, 113} (one verification still running, §5.4);
  - κ = 8: {17, 41, 73, 89, 137, 233};
  - κ = 9: {19, 37, 73, 109, 127, 163, 181, 199, 307, 433};
  - κ = 16: the 17 primes of §5.1.

  Union chains are a variant in which a step targets a union of cosets (§3.5). The covered
  primes include all but these few of E_2(κ), e.g. 52 of the 56 primes of E_2(7), at
  arity (a+1)(6a+1)(3a+1) instead of (a+1)(6a+1). Every uncovered prime lies in E_2(κ),
  and every claimed threshold lies above every exceptional prime found, so the known E_2
  data contradict nothing (§5.6).
- **Counterexamples found (§7).** The tower has its own exceptional primes (7.2). They all
  lie in E_2(κ). This is forced at the last step, since restricting the rows of a two-level
  contraction gives a step contraction (Lemma 7.1). It also gives a cross-check between
  independent computations: every step set at D = κ lies inside the exact E_2(κ). One of
  this pass's own claims had to be corrected. The union searches first assumed distinct β,
  but repeated β entries are allowed for union targets, and at κ = 5, p = 11 step 1 becomes
  feasible with β = (0,0,2,10,6). All union-step infeasibility claims were redone with
  repeated β allowed.
- **Paper.** §8 gives a proposed appendix subsection and a one-sentence change to
  rem:two-level-threshold-size, both marked "AI-checked, pending human review". No `.tex`
  file was edited. Nothing in Theorem thm:power-sde, the combined schedule or the tables
  changes. The tower is an additional schedule; whether it moves E_W(c) was not computed
  (§9).

## 1. The two-level construction as one refinement step

A **relation** is a vector c ∈ F_p^M with Σ_b c_b λ_b = 0. Its support is {b : c_b ≠ 0}. The
two-level construction turns arbitrary relations into a relation with every nonzero
coefficient in P_κ; κ-th roots then give the solution. Write the construction in terms of
coefficient classes:

- Level 1 gives relations c^ν on disjoint blocks, with coefficients in all classes Z_κ.
- Level 2 takes a dependence η among the per-class partial sums U_i^ν = Σ_{cls c_b = i} c_b λ_b.
- The output coefficient of b ∈ S^ν is η_ν(α_{cls η_ν} + β_{cls c_b})c_b, which lies in P_κ.

In the appendix's notation u_b^κ = C_{ij}ω'^κ_b = z_iz_j(α_j+β_i)ϖ_ν^κω_b^κ, the same
thing, since η_ν = z_jϖ_ν^κ and c_b = z_iω_b^κ.

The point of this section is that nothing forces the input classes to range over all of
Z_κ. If they range over a subgroup R of size r, the dependence costs (r−1)a + 1 relations
instead of (κ−1)a + 1, and the contraction needs only r rows. Iterating over a chain of
subgroups gives the tower.

## 2. The refinement step and the tower [proved]

**Definition 2.1 (refinement contraction).** Let D | p − 1, D ≥ 2. Let R ⊆ Z_D with 0 ∈ R
and |R| = r, and K ⊆ Z_D with 0 ∈ K. An **RC(D; R → K) contraction** is a pair
α ∈ F_p^{Z_D}, β ∈ F_p^{R} such that

- α_j + β_i ∈ Q^{(D)°}_{K−i−j} := {0} ∪ ⋃_{k∈K} Q^{(D)}_{k−i−j} for all i ∈ R, j ∈ Z_D, and
- α_0 + β_0 ∈ Q^{(D)}_0 (in particular α_0 + β_0 ≠ 0).

Write RC(D; R) for K = {0}. Then the second condition just says α_0 + β_0 ≠ 0. Let
E(D; R → K) be the set of primes p ≡ 1 (mod D) with no such pair. RC(D; Z_D) is exactly a
two-level contraction at (p, D) (Lemma lem:app-s2-normal), so E(D; Z_D) = E_2(D).

**Lemma 2.2 (refinement step).** Let (α, β) be an RC(D; R → K) contraction and N = (r−1)a + 1.
Let c^1, …, c^N be relations with pairwise disjoint supports S^ν such that

- (i) every nonzero coefficient c^ν_b has D-class in R, and
- (ii) each c^ν has a coefficient c^ν_{b_ν} of D-class 0.

Then one Gaussian elimination of size (r−1)a × N, and one coset test per coefficient,
produce a relation c' with:

- (a) support in ⋃_ν S^ν;
- (b) every nonzero coefficient of D-class in K;
- (c) c' ≠ 0, and more precisely c'_{b_{ν*}} = (α_0+β_0)c^{ν*}_{b_{ν*}} for some ν*, a coefficient of class 0.

*Proof.*

- For ν ≤ N and i ∈ R put U_i^ν = Σ_{b ∈ S^ν, cls_D(c^ν_b) = i} c^ν_b λ_b ∈ F_p^a. By (i),
  Σ_{i∈R} U_i^ν = Σ_b c^ν_b λ_b = 0.
- The N vectors V^ν = (U_i^ν)_{i ∈ R∖{0}} lie in F_p^{(r−1)a}, so there is η ≠ 0 with
  Σ_ν η_ν V^ν = 0. That is, Σ_ν η_ν U_i^ν = 0 for i ≠ 0. It also holds for i = 0, because
  U_0^ν = −Σ_{i≠0} U_i^ν.
- Pick ν* with η_{ν*} ≠ 0 and rescale η so that η_{ν*} = 1.
- For b ∈ S^ν with η_ν ≠ 0 and c^ν_b ≠ 0, put j = cls_D(η_ν), i = cls_D(c^ν_b) and
  c'_b = η_ν(α_j + β_i)c^ν_b. Put c'_b = 0 otherwise. This proves (a).
- c' is a relation:
  Σ_b c'_b λ_b = Σ_ν η_ν Σ_{i∈R}(α_{j(ν)} + β_i)U_i^ν
  = Σ_ν η_ν α_{j(ν)}·Σ_i U_i^ν + Σ_i β_i·Σ_ν η_ν U_i^ν = 0 + 0.
- (b): if c'_b ≠ 0, then α_j + β_i ∈ Q^{(D)}_{k−i−j} for some k ∈ K. So
  cls_D(c'_b) = j + (k − i − j) + i = k ∈ K.
- (c): η_{ν*} = 1 has class 0 and α_{0} + β_{0} ∈ Q^{(D)}_0. So
  c'_{b_{ν*}} = (α_0+β_0)c^{ν*}_{b_{ν*}} is nonzero, of class 0 + 0 = 0. ∎

Distinctness of the β_i is not used. For K = {0} it is forced anyway: if β_i = β_{i'}
with i ≠ i', every cell of rows i, i' must be 0, and row 0 then fails. For a union K it is
not forced (§7.3).

**Theorem 2.3 (tower).** Let κ ≥ 2 and let p ≡ 1 (mod κ) be prime. Fix a chain
1 = D_0 | D_1 | ⋯ | D_L = κ with D_{t−1} < D_t, and put r_t = D_t/D_{t−1} and
R_t = D_{t−1}Z_{D_t} ⊆ Z_{D_t}, the subgroup of order r_t. Suppose that for each t an
RC(D_t; R_t) contraction (α^{(t)}, β^{(t)}) is given; for t = 1 this is a two-level
contraction at (p, D_1). Then from any

  M = (a+1) ∏_{t=1}^{L} ((r_t − 1)a + 1)

columns λ_b ∈ F_p^a, with O(M) Gaussian eliminations of size at most (κ−1)a × ((κ−1)a+1),
O(LM) coset tests and M κ-th roots, one computes u ≠ 0 with Σ_b u_b^κ λ_b = 0. Then
s_b = u_b^t (Lemma lem:app-s2-gcd(b)) solves Σ s_b^d λ_b = 0. For L = 1 this is exactly
the two-level construction of Lemmas lem:app-s2-tensor and lem:app-s2-witness.

*Proof.*

- **Level 0.** Put M_0 = a + 1 and M_t = ((r_t−1)a+1)M_{t−1}, so M = M_L. Split the
  columns into blocks of a + 1. In each block take a nonzero dependence and scale it so
  that one coefficient equals 1. These relations have D_1-classes in Z_{D_1} = R_1, and a
  coefficient of class 0.
- **Induction hypothesis.** After step t − 1 the columns are partitioned into groups of
  M_{t−1}. Each group carries a relation whose nonzero coefficients lie in P_{D_{t−1}},
  with one coefficient equal to 1.
- **Step t.**
  - An element of P_{D_{t−1}} has index divisible by D_{t−1}, so its D_t-class lies in
    R_t. Hypothesis (i) of Lemma 2.2 at D = D_t holds.
  - The coefficient 1 has class 0, so (ii) holds.
  - Apply Lemma 2.2 with K = {0} to N_t = (r_t−1)a + 1 groups at a time. The output has
    every nonzero coefficient in P_{D_t}, and a nonzero coefficient
    (α_0^{(t)}+β_0^{(t)})·1 ∈ P_{D_t}.
  - Divide by it. Every coefficient stays in P_{D_t}, because P_{D_t} is a group, and the
    designated coefficient becomes 1.
- **Conclusion.** After step L there is a nonzero relation c with every nonzero
  coefficient in P_κ. Put u_b = c_b^{1/κ}.
- **Cost.** Step t performs M/M_t eliminations and tests each coefficient once. That gives
  at most M tests per step, plus M roots at the end.
- **L = 1.** Step 1 with R_1 = Z_κ is the two-level construction, as computed in §1. ∎

**Remark 2.4 (independence of ξ).** Whether an RC(D; R) contraction exists, for a subgroup
R and K = {0}, does not depend on ξ.

- Another coset generator is ξ' = ξ^uq with gcd(u, D) = 1 and q ∈ P_D. Then
  ξ'^mP_D = Q^{(D)}_{π(m)} with π(m) = um, and π(R) = R because R is a subgroup.
- So (α'_j, β'_i) := (α_{π(j)}, β_{π(i)}) turns an RC contraction for ξ into one for ξ',
  using −π(i)−π(j) = π(−i−j).
- For union targets K, the image is RC(D; R → π^{−1}K). The algorithm may simply use the ξ
  for which a witness was computed.

## 3. Thresholds for one step [proved]

Throughout this section D ≥ 2 divides p − 1, and R ∋ 0 has |R| = r ≥ 2. R need not be a
subgroup.

**Proposition 3.1 (Weil threshold W).** Put

- A = (r − 1 − r/D)D^r + 1,
- W(D, r) = ((A + √(A² + 4rD^{r−1}))/2)².

Let β_0 = 0, β_i = ξ^{−i} − 1 (i ∈ R∖{0}, any representative) and α_0 = 1. If p > W(D, r),
then for every j ≠ 0 the set X_j = {x : x + β_i ∈ Q^{(D)}_{−(i+j)} ∀ i ∈ R} is nonempty.
Any choice α_j ∈ X_j gives an RC(D; R) contraction with every cell nonzero. Moreover:

- W(D, D) = T_W(D);
- W(D, r) ≤ r²D^{2r};
- W(D, 2) < ((D−1)²+1)² < D^4 for D ≥ 4;
- W(D, 3) ≤ 4D^6.

*Proof.*

- **Column 0.** α_0 + β_i = ξ^{−i} ∈ Q_{−i}, and α_0 + β_0 = 1 ∈ Q_0.
- **Columns j ≠ 0.** The conditions on x prescribe cosets of x − r_i with
  r_i = 1 − ξ^{−i}. These are distinct, since the ξ^{−i} lie in distinct cosets.
  Lemma lem:app-s2-weil-count applies to the character of order D (its proof uses only
  ord χ = D ≥ 2) with ℓ = r and c_i = 1. It gives
  D^r|X_j| ≥ p − r − D^rE_D(r, p) = p − A√p − rD^{r−1},
  since D^rE_D(r,p) = A√p + rD^{r−1} − r. The right side is positive exactly when √p
  exceeds the positive root of X² − AX − rD^{r−1}.
- **r = D.** A = (D−2)D^D + 1 and rD^{r−1} = D^D, the constants of T_W.
- **W ≤ r²D^{2r}.** Use √W ≤ A + √(rD^{r−1}) ≤ rD^r, which holds because
  1 + √(rD^{r−1}) ≤ D^r + rD^{r−1}.
- **r = 2.** A = (D−1)² and rD^{r−1} = 2D. Then √W < (D−1)² + 1 is equivalent to
  √((D−1)^4 + 8D) < (D−1)² + 2, that is to D² − 4D + 2 > 0, which holds for D ≥ 4.
- **r = 3.** √W ≤ 2D³ − 3D² + 1 + √3·D ≤ 2D³ for D ≥ 1. ∎

**Proposition 3.2 (second-moment threshold T_R).** Let
Δ = ((D−1)(D−2)√p + 2(D−1))/(p−D−1) and

  E_r(Δ) = (r−1)Δ² + (1+Δ)e^{(r−1)Δ}(r−1)²Δ²/2.

If p > D + 1 and D^r p^{r−1}/(p−1)^r + E_r(Δ) < 1/(D−1), then an RC(D; R) contraction with
every cell nonzero exists. The left side is decreasing in p. Let T_R(D, r) be the infimum
of the p where it holds; then every p > T_R(D, r) works.

*Proof.*

- **Setup.** Draw β_0 = 0 and β_i (i ∈ R∖0) independently and uniformly. Let
  X_j = {x : x + β_i ∈ Q_{−(i+j)} ∀ i ∈ R} and n_j = |X_j|. If every n_j > 0, then β and any
  α_j ∈ X_j form a contraction. Indeed α_0 ∈ X_0 forces α_0 = α_0 + β_0 ∈ Q_0.
- **Moments.** The proof of Lemma lem:app-s2-moments, with the rows restricted to R and κ
  replaced by D, gives
  - E n_j = h(h/p)^{r−1}, with h = (p−1)/D;
  - E n_j² = E n_j + (h/p^{r−1})Σ_c m'_c ∏_{i∈R∖0} m_{−i−c}.

  The only change is that i runs over R∖0, so the index −(i+c) runs over −c − (R∖0).
- **Ratio.** With m_b = μ(1+δ_b), m'_c = μ(1+δ'_c) and μ = (p−D−1)/D²,

  ρ := E n_j²/(E n_j)² = D^r p^{r−1}/(p−1)^r + L·F,

  where L = ((p−D−1)/(p−1))^r (p/(p−1))^{r−1} ≤ 1, as in Proposition prop:app-s2-TA, and

  F = (1/D)Σ_c(1+δ'_c)∏_{i∈R∖0}(1+δ_{−i−c}) ≥ 0.
- **Bound on F.** By Lemma lem:app-s2-cyclo (with κ → D), |δ_b|, |δ'_c| ≤ Δ and
  Σδ_b = Σδ'_c = 0. Put s_c = Σ_{i∈R∖0}δ_{−i−c}. Then Σ_c s_c = (r−1)Σ_bδ_b = 0, since every
  b occurs exactly r − 1 times. Expand
  ∏_{i∈R∖0}(1+δ_{−i−c}) = 1 + s_c + ρ_c, where
  |ρ_c| ≤ (1+Δ)^{r−1} − 1 − (r−1)Δ ≤ e^{(r−1)Δ}((r−1)Δ)²/2.
  Then F = 1 + (1/D)Σ_c[δ'_c + s_c + δ'_cs_c + (1+δ'_c)ρ_c] ≤ 1 + E_r(Δ), using
  |δ'_cs_c| ≤ (r−1)Δ².
- **Conclusion.** So ρ ≤ D^rp^{r−1}/(p−1)^r + 1 + E_r(Δ). By Cauchy–Schwarz,
  Pr[n_j = 0] ≤ 1 − 1/ρ. The union bound over the D columns is below 1 iff ρ < D/(D−1).
- **Monotonicity.** Δ decreases in p, as in prop:app-s2-TA(ii). E_r increases in Δ ≥ 0.
  The first term has logarithmic derivative (r−1)/p − r/(p−1) < 0. ∎

**Lemma 3.3 (closed form for T_R).** For D ≥ 4 and 2 ≤ r ≤ D,
T_R(D, r) ≤ P(D, r) := max(4D^{r+1}, 4r²D^5).

*Proof.* Let p ≥ P. Then p ≥ 16D^5 ≥ 16384.

- **First term.** r/(p−1) ≤ 10^{−3}, so D^rp^{r−1}/(p−1)^r ≤ (D^r/p)e^{r/(p−1)} ≤ 1.001/(4D).
- **Δ.** (D−1)(D−2)√p + 2(D−1) ≤ D²√p, because 2(D−1) ≤ (3D−2)√p. Also
  (D+1)/p ≤ 4·10^{−4}. So Δ ≤ 1.0005D²/√p ≤ 0.5003/(r√D), using √p ≥ 2rD^{5/2}. Hence
  (r−1)Δ ≤ 0.2502 and Δ ≤ 0.1251.
- **E_r.** E_r ≤ Δ²[(r−1) + (1.1251·e^{0.2502}/2)(r−1)²] ≤ Δ²[(r−1) + 0.7225(r−1)²] ≤ 0.7225r²Δ².
  The last step is r − 1 ≤ 0.7225(2r−1). So E_r ≤ 0.7225·0.2503/D = 0.1809/D.
- **Total.** The left side is at most (0.2503 + 0.1809)/D < 1/D < 1/(D−1), and monotonicity
  finishes the proof. ∎

Numerical check [float], `tr_bound.py` → `tr_bound.out`: at p = P(D, r), D·(left side)
is at most 0.349 over all 4 ≤ D ≤ 64 and 2 ≤ r ≤ D, against 0.4312 in the proof. The bisected
T_R is 7–34% of P on the table printed.

**Proposition 3.4 (union target, Weil).** Let ℓ = |R| and K ⊆ Z_D with 0 ∈ K and |K| = k.
Let ĉ_s = D^{−1}Σ_{m∈K}ω^{−ms}, c_0 = k/D, G = Σ_{s≠0}|ĉ_s| and F = c_0 + G. Put

- B = ℓGF^{ℓ−1} − (F^ℓ − c_0^ℓ),
- C = ℓ(F^ℓ − c_0^ℓ) − ℓGF^{ℓ−1}.

With β and α_0 as in Proposition 3.1, every column j ≠ 0 has at least
c_0^ℓ(p−ℓ) − B√p − C admissible x for RC(D; R → K). In particular an RC(D; R → K)
contraction exists once this is positive. Column 0 holds since 0 ∈ K, and
α_0 + β_0 = 1 ∈ Q_0.

*Proof.*

- For y ≠ 0, [ind(y) ∈ K + t] = Σ_s ĉ_s ω^{−ts}χ(y)^s.
- Expanding the product over the ℓ rows, the term e = 0 is c_0^ℓ(p−ℓ).
- A tuple e of support size s ≥ 1 has weight of modulus c_0^{ℓ−s}∏|ĉ_{e_i}|. Its character
  sum is at most (s−1)√p + (ℓ−s), by Weil with distinct roots, as in lem:app-s2-weil-count.
- Summing over e: Σ_sC(ℓ,s)c_0^{ℓ−s}G^s = F^ℓ − c_0^ℓ and
  Σ_s s·C(ℓ,s)c_0^{ℓ−s}G^s = ℓGF^{ℓ−1}. These give B and C.
- For K = {0}: c_0 = 1/D and G = (D−1)/D. This reproduces E_D(ℓ, p) exactly; checked
  against T_W at D = 3, 4, 5 in `thresholds.out`. ∎

Values [float] (`thresholds.py` → `thresholds.out`):

| step | W | T_R | | step | W | T_R |
|---|---|---|---|---|---|---|
| (4,2) | 96.3 | 298 | | (12,2) | 14689 | 2.4e5 |
| (6,2) | 648.8 | 4061 | | (12,3) | 9.2e6 | 6.8e5 |
| (6,3) | 1.06e5 | 12022 | | (16,2) | 50689 | 1.1e6 |
| (8,2) | 2432.9 | 23293 | | (16,4) | 3.2e10 | 7.0e6 |
| (8,4) | 1.05e8 | 151114 | | (18,3) | 1.1e8 | 6.1e6 |
| (9,3) | 1.48e6 | 134723 | | (32,2) | 923649 | 4.4e7 |

Union step 1 (rows Z_D → K), Weil: D = 5, K = {0,1}: 761853; D = 5, {0,1,2}: 37246;
D = 7, {0,1,2,3}: 2.256·10^7; D = 7, {0,1}: 2.7·10^{10}. For union step 2, RC(D; K) with
R = K a non-subgroup: D = 5, R = {0,1}: W = 275.6; D = 7, R = {0,1,2,3}: T_R = 68958.

### 3.5 Union chains (Z_D → K → {0}) [proved]

Lemma 2.2 also applies when the target is a union.

- Step 1, RC(κ; Z_κ → K), is applied to the level-0 relations. Its output has classes in
  K and a designated coefficient of class 0, by Lemma 2.2(c), because
  α_0 + β_0 ∈ Q_0 is required.
- Step 2, RC(κ; K), is applied to (k−1)a + 1 such outputs. No rescaling between the two
  steps is needed.
- Arity: (a+1)((κ−1)a+1)((k−1)a+1).

## 4. Corollaries [proved]

**Corollary 4.1 (κ = 2^L).** Let κ = 2^L with L ≥ 2, and let p ≡ 1 (mod κ) with
p > ((κ−1)²+1)². Then the chain D_t = 2^t works with M = (a+1)^{L+1}.

- Step 1 needs a two-level contraction at (p, 2), and E_2(2) = ∅ (cor:app-s2-small).
- Step t ≥ 2 needs RC(2^t; {0, 2^{t−1}}). It exists for p > W(2^t, 2), and
  W(2^t, 2) < ((2^t−1)²+1)² ≤ ((κ−1)²+1)² by Proposition 3.1.
- **Finding cost.** Proposition 3.1 gives D²|X_j| ≥ p − (D−1)²√p − 2D. Once
  √p ≥ 2((D−1)² + 2D) = 2(D²+1), this is at least p/2. So a uniform draw lies in X_j with
  probability ≥ 1/(2D²). Each α_j costs O(D² log(1/ε)) draws of r = 2 coset tests.
- **Total.** For p ≥ 4(κ²+1)², all contractions together cost poly(κ)·log(1/ε) draws,
  against κ^{κ+1} for Schedule 2. Between ((κ−1)²+1)² and 4(κ²+1)², enumeration costs
  O(κp) = poly(κ) tests. ∎

**Theorem 4.2 (general κ).** Let κ ≥ 4 be composite, κ = q_1 q_2 ⋯ q_L with
q_1 ≥ q_2 ≥ ⋯ ≥ q_L primes and q = q_1. Use the chain D_t = q_1⋯q_t. For every prime
p ≡ 1 (mod κ) with

  p > Θ(κ) := max( T_A(q)·[q ≥ 5], max_{t≥2} min(W(D_t, q_t), T_R(D_t, q_t)) ),

and in particular for p > max(T_A(q)·[q ≥ 5], 4κ^{q+1}, 4q²κ^5), and hence for
p > 4κ^{max(q+1,7)}, Theorem 2.3 applies with

  M = (a+1)∏_t((q_t−1)a+1) ≤ κ(a+1)a^{L}.

*Proof.*

- **Step 1.** It needs p ∉ E_2(q). This holds for q ∈ {2, 3} by cor:app-s2-small, and for
  p > T_A(q) when q ≥ 5 by prop:app-s2-TA; also T_A(q) ≤ q^{q+1} there.
- **Steps t ≥ 2.** Here D_t ≥ 4 and 2 ≤ q_t ≤ D_t. So Proposition 3.1, Proposition 3.2 and
  Lemma 3.3 give a step contraction for
  p > min(W, T_R) ≤ P(D_t, q_t) ≤ max(4κ^{q+1}, 4q²κ^5).
- **Arity.** (q_t−1)a + 1 ≤ q_t a.
- **Last form.** q^{q+1} ≤ κ^{q+1}, and 4q²κ^5 ≤ 4κ^7. ∎

**Corollary 4.3 (3-smooth κ ≥ 4).** p > 36κ^5 suffices. The r = 3 steps need
min(W, T_R)(D, 3) ≤ max(4D^4, 36D^5) = 36D^5 (Lemma 3.3). The r = 2 steps need
W(D, 2) < D^4. Step 1 is E_2(2) = ∅ or E_2(3) = ∅.

Comparison with the two-level threshold. Theorem 4.2 has exponent max(q+1, 7) + o(1). The
proved two-level threshold has exponent κ + 1. The exceptional primes of E_2(κ) are
observed up to about 1.5κ^{(κ+1)/2}. So for every composite κ with
max(q+1, 7) < (κ+1)/2 the tower is *proved* to work at primes where the two-level
construction is believed, though not proved, to fail; and for κ = 8, 9, 16 the computed
sets in §5 make this unconditional at those κ. Examples:

- κ = 16: the tower is proved from 51076, and also at the 17 exceptional primes listed
  in §5.1. The two-level threshold is T_A(16) ≈ 2.8·10^{20}.
- κ = 2q: Θ ≤ max(T_A(q), W(2q, 2)) ≈ q^{q+1}, about the square root of the two-level
  threshold.

**Remark 4.4 (no O(a²) from towers) [proved, elementary].** M = (a+1)∏_{t=1}^L((r_t−1)a+1)
has degree L + 1 ≥ 3 in a whenever L ≥ 2, since every r_t ≥ 2. Degree 2 forces L = 1, the
two-level construction.

So route (3) of the brief ("arity O_κ(a²)") is achieved only where it is already known,
namely at p ∉ E_2(κ). The adaptive refinement of §9, item 2, would lower the constant, not the
degree.

Arity comparison (all for p ≡ 1 mod κ):

| schedule | columns | degree in a | proved range of p |
|---|---|---|---|
| Schedule 1, B_κ(a) | (κ^{κ(κ−1)/2}(a+1)^κ)^{⌈log₂(κ+1)⌉} | κ⌈log₂(κ+1)⌉ | all p |
| Schedule 2 (decoupled) | (a+1)((κ−1)a+1) | 2 | p ∉ E_2(κ); ⊇ p ≥ κ^{κ+1} |
| triangular (prop:triangular-sde) | (a+1)(a+2)/2 | 2 | same |
| tower (Thm 4.2) | (a+1)∏((q_t−1)a+1) | 1 + Ω(κ) | p > Θ(κ) ≤ 4κ^{max(q+1,7)}; κ = 2^L: p > ((κ−1)²+1)² |

At a = 10: κ = 8 gives 781 (Schedule 2), 14641 (tower) and about 10^{134} (Schedule 1).
κ = 6 gives 561, 2541 and about 10^{58}.

## 5. Finite computations [exact]

Programs:

- `rect.c` decides RC(D; mZ_D).
- `rectu.c` decides RC(D; R → K). It has a complete DFS mode (normal form β_0 = 0, α_0 = 1,
  zeros allowed) and a randomized witness mode; `ALLOWDUP=1` admits repeated β.
- `rectp.c` is a randomized witness search for large p.

`verify.py` is a sympy checker that shares no code with the C programs. For every FEASIBLE
line it re-checks p, the primitive root g and all cells. It re-decides INFEASIBLE claims by
an independent Python exhaustive search up to the stated bound, and it checks that every
prime ≡ 1 (mod D) in the covered range has a line. Outputs are in `v_*.out`: bad = 0,
disagreements = 0 and missing = 0 everywhere.

A claimed exceptional set is the set of INFEASIBLE primes from the complete search. Above
the last checked prime, the proved threshold of §3 applies, and the "checked to" bound
exceeds that threshold.

### 5.1 Step exceptional sets E(D; R) (K = {0}, zeros allowed)

| step | E(D; R) | checked to | proved threshold | witnesses | brute re-decided |
|---|---|---|---|---|---|
| RC(4,{0,2}) | {5, 13, 29} | 3000 | W = 96.3 | 208 | all 3 |
| RC(6,{0,3}) | {7,13,19,31,43,67,79,139,223} | 3000 | W = 648.8 | 198 | all 9 |
| RC(6,{0,2,4}) | {7,13,19,31,37,43,61,67,73,79,97,139} | 12100 | T_R = 12022 | 705 | all 12 |
| RC(8,{0,4}) | {17,41,73,89,137,233,761} | 6000 | W = 2432.9 | 179 | all 7 |
| RC(8,{0,2,4,6}) | 32 primes, max 929 | 152000 | T_R = 151114 | 3443 | 11 of 32 (≤ 260) |
| RC(9,{0,3,6}) | {19,37,73,109,127,163,181,199,271,307,379,433,487,523} | 135000 | T_R = 134723 | 2079 | all 14 |
| RC(16,{0,8}) | {17,97,113,193,241,257,337,353,401,433,593,881,977,1009,1201,1297,1489} | 51000 | W = 50689 | 633 | all 17 |

The 32 primes of RC(8,{0,2,4,6}) are 17, 41, 73, 89, 97, 113, 137, 193, 233, 241, 257, 281,
313, 337, 353, 401, 409, 433, 449, 457, 521, 577, 593, 601, 617, 641, 673, 761, 769, 809,
857 and 929. The 21 above 260 rest on the C DFS only.

### 5.2 Chain exceptional sets (tower, Theorem 2.3)

A prime is chain-exceptional if some step of the chain fails there.

- **κ = 4**, chain (2,4), M = (a+1)³: {5, 13, 29}. E_2(4) = {5,13,17,29,37,53}, so 17, 37
  and 53 are newly covered.
- **κ = 6**:
  - chain (3,6), steps E_2(3) = ∅ and RC(6,{0,3});
  - chain (2,6), steps E_2(2) = ∅ and RC(6,{0,2,4});
  - both chains have M = (a+1)²(2a+1);
  - a prime is lost only if both chains fail: {7,13,19,31,43,67,79,139}. This covers 45 of
    the 53 primes of E_2(6), including its maximum 859. With the union chains of §5.3 the
    count rises to 47.
- **κ = 8**, chain (2,4,8), M = (a+1)⁴: RC(4,{0,2}) fails at no prime ≡ 1 (mod 8). So the
  set is E(8;{0,4}) = {17,41,73,89,137,233,761}. The chain (4,8) gives the same set, at
  M = (a+1)(3a+1)(a+1).
- **κ = 9**, chain (3,9), M = (a+1)(2a+1)²: the 14 primes of RC(9,{0,3,6}).
- **κ = 16**, chain (2,4,8,16), M = (a+1)⁵:
  - the 17 primes of RC(16,{0,8});
  - of the lower-step exceptions, only 17 is ≡ 1 (mod 16), and it is already in that list;
  - so the tower works at every prime p ≡ 1 (mod 16) outside these 17.

### 5.3 Union chains (§3.5), with repeated β allowed

Each listed prime is covered by the chain Z_κ → K → {0} for the K given. `union_explore2.sh`
→ `union_explore2.out`; the witnesses are in `uw_k*_K*_s{1,2}.out` and are verified in
`v_uw.out` (22 witnesses over 11 step files, bad = 0).

- κ = 4: 29 (K = {0,1}).
- κ = 6: 79 and 139 (K = {0,1}).
- κ = 8: 761 (K = {0,1}).
- κ = 9: 271 (K = {0,4}), 379 (K = {0,1}), 487 (K = {0,1,3}) and 523 (K = {0,1,2}).
- κ = 7: 127, 211, 239, 337 and 631 (K = {0,1}), and 197 (K = {0,2}).

**Not covered by any K with |K| ∈ {2, 3}** (for κ = 7 also K = {0,1,2,3}), with a complete
search at both steps:

- κ = 4: 5, 13;
- κ = 5: 11;
- κ = 6: 7, 13, 19, 31, 43, 67;
- κ = 7: 29, 43, 71, 113;
- κ = 8: 17, 41, 73, 89, 137, 233;
- κ = 9: 19, 37, 73, 109, 127, 163, 181, 199, 307, 433.

See §7.3 for κ = 5, p = 11.

### 5.4 κ = 5 and κ = 7: union chains over all primes

- **κ = 5**, chain Z_5 → {0,1} → {0}, M = (a+1)(4a+1)(a+1):
  - step 1 holds for p > 761853 (Proposition 3.4) and at every p ≡ 1 (mod 5) up to 762000
    except 11. There are 15243 witnesses, `v_u5_step1.out`.
  - step 2, RC(5,{0,1}), holds for p > 275.6, and up to 3000 fails only at 11
    (`v_u5_step2.out`).
  - So the construction works at every p ≡ 1 (mod 5) except 11. That covers 8 of the 9
    primes of E_2(5).
- **κ = 7**, chain A, Z_7 → {0,1,2,3} → {0}, M = (a+1)(6a+1)(3a+1):
  - step 1 holds for p > 2.2558·10^7 (Proposition 3.4). There is a witness at every
    p ≡ 1 (mod 7) up to 2.256·10^7 (236878 witnesses, no failure; the complete search
    below 6000 finds no INFEASIBLE prime).
  - step 2, RC(7,{0,1,2,3}), holds for p > T_R = 68958. Below 69100 it fails exactly at
    {29,43,71,113,127,197,211,239,337,631} (`v_u7_step2A.out`).
  - At 127, 197, 211, 239, 337 and 631 a chain with |K| = 2 works (§5.3). So every
    p ≡ 1 (mod 7) except 29, 43, 71 and 113 is covered, at M ≤ (a+1)(6a+1)(3a+1).
  - **Pending:** the independent re-check of the 236878 step-1 witnesses (`v_u7_step1A.out`)
    was still running when this report was written. The C search output is complete. Until
    `v_u7_step1A.out` shows bad = 0 and missing = 0, the κ = 7 statement is "exact modulo
    that check".

### 5.5 End-to-end runs of Theorem 2.3 (`tower.py` → `tower_demo.out`)

`tower.py` builds the whole tower from random columns. It calls `rectu` for the step
contractions and checks four things exactly: c ≠ 0, every c_b ∈ P_κ, Σc_bλ_b = 0, and
Σu_b^κλ_b = 0 after κ-th roots.

**Runs, all OK:**

| κ | p | chains |
|---|---|---|
| 4 | 17, 37, 53 | |
| 6 | 859 | both chains |
| 8 | 11953, 11689, 9001 | |
| 9 | 17929, 17911 | |
| 5 | 181, 131 | union chain |
| 7 | 3221 | union chain A |
| 16 | 1553 | |

All of these primes except 9001 (κ = 8) and 1553 (κ = 16) are in E_2(κ), so at them
no two-level contraction exists. 9001 and 1553 are plain test primes.
Here a ranges over {1, 2, 3}, giving M up to 273.

**Adversarial mode** (zero columns, repeated columns, unit vectors): OK at κ = 4, p = 17;
κ = 8, p = 11953; κ = 9, p = 17929; κ = 5, p = 181. At κ = 4, p = 13 the tool correctly
reports that no step contraction exists.

### 5.6 Consistency with the known E_2 data

- **Thresholds.** Every proved threshold of §3–§4 lies above every prime at which the
  corresponding step was found to fail. For example 223 < W(6,2) = 648.8 and
  1489 < W(16,2) = 50689.
- **Uncovered primes.** Every prime that no chain covers lies in E_2(κ):
  - κ ≤ 7: checked against the exact lists;
  - κ = 8, 9: all are below the first feasible two-level primes, 1553 and 3529.
- **Coverage.** The towers do cover most of E_2(κ). This does not contradict E_2: it is a
  different construction, with a larger arity.

## 6. Routes (1), (2) and (4): why they do not close the two-level gap

**Remark 6.1 (Kummer covers re-index the same sums) [proved].**

- **Setup.** Let T be a spanning tree of the complete bipartite graph on rows ⊔ columns
  (2κ − 1 edges). The tree cells v_e = α_j + β_i, e = (i, j) ∈ T, determine (α, β) modulo
  translation linearly. Every other cell is a linear form L_f(v).
- **Parametrisation.** Put v_e = z_e u_e^κ, with z_e = ξ^{−(i+j)} and u ∈ (F^×)^T. This
  makes the tree cells admissible automatically.
- **Identity.** Each admissible nonzero v_e has exactly κ preimages. Hence for any function
  G of the non-tree cells,
  Σ_u G(L(z u^κ)) = κ^{2κ−1}Σ_v G(L(v))∏_{e∈T}[v_e ∈ Q_{−(i+j)}].
  Expanding the indicators,
  Σ_u G = Σ_{f ∈ Z_κ^T} ϑ_f Σ_v G(L(v))∏χ^{f_e}(v_e), with |ϑ_f| = 1.
- **Consequence.** Every character sum on the cover is a unimodular combination of
  κ^{2κ−1} character sums on the base, the tree characters reinserted, and conversely.
  So a Deligne-type bound on the cover, whose Betti numbers carry the factor κ^{2κ−1},
  is the triangle inequality applied to the base expansion. It cannot do better than the
  term-by-term certificate. That certificate is refuted below 2^{−1/(κ−1)}κ^κ
  (TH3; cited in rem:two-level-threshold-size).

**6.2 Square-root barrier for structured families [argued; exact for certificates of this
form].**

- **Certificate.** A family V of dimension D_V ≤ 2κ − 2 (after normalisation), with
  n = κ² − 1 coset conditions, has main term p^{D_V}κ^{−n}. A certificate of the form
  "main term > Σ over nontrivial character tuples of a square-root bound" has error at
  least about p^{D_V/2}, even when each of the κ^n − 1 tuples has weight κ^{−n} and a sum
  of size O(p^{D_V/2}).
- **Barrier.** So it needs p > κ^{2n/D_V} ≥ κ^{(κ²−1)/(κ−1)} = κ^{κ+1}. Lower-dimensional
  families, such as curves α_j = f(jt), β_i = g(it), are worse: they have D_V ≤ 2 and need
  p > κ^{κ²−1}. Only the full family reaches the T_A exponent.
- **Why the tower escapes.** It changes n/D_V. Step t has D_t·r_t − 1 conditions on
  D_t + r_t − 2 unknowns, and each α_j faces only r_t conditions. Fixing β (Proposition
  3.1) then gives exponent 2r_t; the second moment gives r_t + 1 up to the
  D^5 term (Lemma 3.3).

**6.3 Fixing cells (route 2) [proved, elementary].**

- In K_{κ,κ} every unknown α_j lies in κ cells, so in any order of choice the last unknown
  of each column faces κ conditions. With every β_i fixed and distinct, each point x
  outside the κ roots lies in X_j for exactly one coset pattern of its κ shifts. So the
  average of |X_j| over the κ^κ patterns is (p − κ)/κ^κ.
- So no explicit choice of β can be certified for p < κ^κ by counting. Weil certifies it
  only from about (κ−2)²κ^{2κ} (T_W).
- The algebraic choices tried here, β_i = ξ^{−i} − 1 and β_i = cξ^{ei}, change only the
  roots. They cannot lower the number of conditions.

**6.4 Conditional statements (route 4).**

- **GRH** controls incomplete sums and least non-residues. The counts here are complete
  sums over F_p, already at the Weil (RH for curves) level. GRH therefore gives nothing
  beyond Weil [argued].
- **The strongest one-variable conjecture** would say: every pattern of κ cosets on κ
  distinct shifts occurs once p ≥ Cκ^κ. With fixed β it gives threshold Cκ^κ, exponent κ,
  and by 6.3 nothing below.
- **Exponent (κ+1)/2 needs a joint statement.**

**Conjecture 6.4 (random-model count) [conjecture].** Let
μ_κ(p) = p^{2κ−2}q^{κ²−1} with q = ((p−1)/κ + 1)/p. This is the expected number of
normalised contractions with independent cells. There is an absolute c such that
μ_κ(p) ≥ c implies p ∉ E_2(κ).

- It gives max E_2(κ) ≤ c^{1/(2κ−2)}κ^{(κ+1)/2}(1+o(1)).
- It is not implied by any known theorem. It is a restatement of the problem with a
  uniform constant. Proving it for a single κ at the required precision is exactly the
  open square gap.
- **Calibration** [float], `mu.py` → `mu.out`: μ at the largest known exceptional prime is

| κ | p_max | μ_κ(p_max) |
|---|---|---|
| 4 | 53 | 47.1 |
| 5 | 181 | 32.7 |
| 6 | 859 | 155.9 |
| 7 | 3221 | 37.2 |
| 8 | 12377 | 2.6 |
| 9 | 17929 | 5·10^{−9} |

  So c ≥ 156 is forced. The κ = 8 and 9 values are not maxima, because their scans are
  still running.

## 7. Counterexamples found

### 7.1 Where tower steps can fail

**Lemma 7.1 [proved].** For every R ∋ 0 and K ∋ 0, E(κ; R → K) ⊆ E_2(κ).

*Proof.* Restricting a two-level contraction (α, β) to the rows in R gives an RC(κ; R)
contraction. Since Q°_{−(i+j)} ⊆ Q°_{K−i−j}, it is also an RC(κ; R → K) contraction. ∎

- **Consequence.** A chain can fail outside E_2(κ) only at an intermediate modulus
  D_t < κ. No such prime was found: every chain-exceptional prime computed here lies in
  E_2(κ). The chain of length 1 is the two-level construction, so taking the best chain
  never loses a prime.
- **Cross-check [exact].** Lemma 7.1 ties two independent computations together. Each of
  E(4;{0,2}), E(6;{0,3}), E(6;{0,2,4}), E(5;{0,1}) and E(7;{0,1,2,3}) was checked to lie
  inside the exact E_2 list of the earlier reports, and it does.

### 7.2 Small primes where no chain works

All of the following lie in E_2(κ):

- κ = 4: 5, 13;
- κ = 5: 11;
- κ = 6: 7, 13, 19, 31, 43, 67;
- κ = 7: 29, 43, 71, 113;
- κ = 8: 17, 41, 73, 89, 137, 233;
- κ = 9: 19, 37, 73, 109, 127, 163, 181, 199, 307, 433.

The chains tried are every subgroup chain, and union chains with |K| ≤ 3 (and
K = {0,1,2,3} at κ = 7). §5.3 gives the per-K log.

### 7.3 Repeated β matters for union targets

The first union search, `union_explore.sh`, and the u5/u7 step-1 runs searched only
distinct β. That is valid for K = {0} (remark after Lemma 2.2), but not for unions.

- At κ = 5, p = 11, RC(5; Z_5 → {0,1}) is infeasible with distinct β. It is feasible with
  β = (0, 0, 2, 10, 6), α = (1, 5, 0, 0, 9), g = 2.
- p = 11 stays uncovered: step 2 RC(5;{0,1}) fails, and so does every other K.

So "u5 step 1 fails only at 11" is true only for distinct β. The κ = 5 conclusion is
unchanged.

### 7.4 Patterns that did not survive

- **"Union chains cover every prime of E_2(κ) above a small bound."** False: κ = 7,
  p = 113, and κ = 9, p = 433.
- **"r = 2 steps never fail."** False: RC(16,{0,8}) fails at 17 primes up to 1489.

The maxima of the step exceptional sets lie near D^{2.4}–D^{3.3}: 29 ≈ 4^{2.43},
223 ≈ 6^{3.02}, 761 ≈ 8^{3.19}, 1489 ≈ 16^{2.64}, 139 ≈ 6^{2.75}, 523 ≈ 9^{2.85} and
929 ≈ 8^{3.29}. The proved step thresholds are W(D,2) ≈ D^4 and T_R ≈ D^5. So the
step-level analogue of the square gap is mild. The step thresholds (§3) are the only
uniform statements.

## 8. Proposed LaTeX (AI-checked, pending human review; not applied)

### 8.1 New subsection for `appendix-schedule2.tex`, after Corollary cor:app-s2-small and before the scope section

```latex
\subsection{A tower of coset refinements}
\label{app:s2-tower}

\noindent\textbf{Status: AI-checked, pending human review}
(\file{research/audits/reviews/2026-11-05-rees-threshold-6.md}). This subsection is not
used by Theorem~\ref{thm:power-sde}, Remark~\ref{rem:combined-schedule} or the tables.

For $D \mid \kappa$ put $P_D = (\Fp^\times)^D$ and $Q^{(D)}_m = \xi^m P_D$
($m \in \mathbb{Z}_D$); since $\xi$ generates $\Fp^\times/Q_0$, the $D$-class of $x$ is
$\operatorname{ind}(x) \bmod D$, so one coset test serves every $D \mid \kappa$. A
\emph{relation} is a vector $c \in \Fp^M$ with $\sum_b c_b\lambda_b = 0$.

\begin{definition}
Let $D \mid \kappa$, $D \ge 2$, and $0 \in R \subseteq \mathbb{Z}_D$ with $|R| = r$. A
\emph{refinement contraction} $\mathrm{RC}(D;R)$ is a pair $\alpha \in \Fp^{\mathbb{Z}_D}$,
$\beta \in \Fp^{R}$ with $\alpha_0 + \beta_0 \ne 0$ and
$\alpha_j + \beta_i \in Q^{(D)}_{-(i+j)} \cup \{0\}$ for all $i \in R$, $j \in \mathbb{Z}_D$.
For $R = \mathbb{Z}_D$ it is a two-level contraction at $(p,D)$.
\end{definition}

\begin{lemma}[refinement step]
\label{lem:app-s2-refine}
Let $(\alpha,\beta)$ be an $\mathrm{RC}(D;R)$ contraction and $N = (r-1)a+1$. Let
$c^1,\dots,c^N$ be relations with disjoint supports $S^\nu$, every nonzero coefficient of
$D$-class in $R$, and $c^\nu_{b_\nu} = 1$ for some $b_\nu$. With one Gaussian elimination
and one coset test per coefficient one computes a relation $c'$, supported in
$\bigcup_\nu S^\nu$, with every nonzero coefficient in $P_D$ and
$c'_{b_{\nu^\ast}} = \alpha_0 + \beta_0 \ne 0$ for some $\nu^\ast$.
\end{lemma}

\begin{proof}
Put $U^\nu_i = \sum_{b \in S^\nu,\ \operatorname{ind}(c^\nu_b) \equiv i} c^\nu_b\lambda_b$
for $i \in R$, so $\sum_{i \in R} U^\nu_i = 0$. The $N$ vectors
$(U^\nu_i)_{i \in R\setminus\{0\}} \in \Fp^{(r-1)a}$ have a nonzero dependence $\eta$;
then $\sum_\nu \eta_\nu U^\nu_i = 0$ for every $i \in R$, including $i = 0$. Normalise
$\eta_{\nu^\ast} = 1$ for some $\nu^\ast$ with $\eta_{\nu^\ast} \ne 0$. For $b \in S^\nu$
put $c'_b = \eta_\nu(\alpha_{j} + \beta_{i})c^\nu_b$ with $j \equiv \operatorname{ind}(\eta_\nu)$
and $i \equiv \operatorname{ind}(c^\nu_b)$ modulo $D$, and $c'_b = 0$ if $\eta_\nu c^\nu_b = 0$.
Then $\sum_b c'_b\lambda_b = \sum_\nu\eta_\nu\alpha_{j(\nu)}\sum_iU^\nu_i +
\sum_i\beta_i\sum_\nu\eta_\nu U^\nu_i = 0$. A nonzero $c'_b$ has class
$j + (-(i+j)) + i = 0$, and $c'_{b_{\nu^\ast}} = \alpha_0 + \beta_0$.
\end{proof}

\begin{theorem}[tower]
\label{thm:app-s2-tower}
Let $1 = D_0 \mid D_1 \mid \cdots \mid D_L = \kappa$ with $D_{t-1} < D_t$, put
$r_t = D_t/D_{t-1}$ and $R_t = D_{t-1}\mathbb{Z}_{D_t}$, and suppose
$\mathrm{RC}(D_t;R_t)$ contractions exist for $t = 1,\dots,L$ (for $t = 1$: $p \notin E_2(D_1)$).
Then from any $M = (a+1)\prod_{t=1}^{L}\bigl((r_t-1)a+1\bigr)$ columns in $\Fp^a$ one computes,
with $O(M)$ eliminations, $O(LM)$ coset tests and $M$ root extractions, a nonzero solution
of~\eqref{eq:app-s2-target}. For $L = 1$ this is Lemmas~\ref{lem:app-s2-tensor}
and~\ref{lem:app-s2-witness}.
\end{theorem}

\begin{proof}
Blocks of $a+1$ columns give relations with one coefficient $1$. Apply
Lemma~\ref{lem:app-s2-refine} at $D = D_t$ for $t = 1,\dots,L$: elements of
$P_{D_{t-1}}$ have $D_t$-class in $R_t$, and dividing each output by its coefficient
$\alpha^{(t)}_0+\beta^{(t)}_0 \in P_{D_t}$ restores a coefficient $1$ and keeps every
coefficient in the group $P_{D_t}$. After step $L$ every nonzero coefficient lies in
$P_\kappa = Q_0$; take $\kappa$-th roots and apply Lemma~\ref{lem:app-s2-gcd}(b).
\end{proof}

\begin{proposition}[one-step thresholds]
\label{prop:app-s2-step-threshold}
Let $D \mid \kappa$, $0 \in R \subseteq \mathbb{Z}_D$, $|R| = r \ge 2$.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item With $A = (r-1-r/D)D^r + 1$ and
  $W(D,r) = \bigl(\tfrac12(A + \sqrt{A^2 + 4rD^{r-1}})\bigr)^2$, the choice $\beta_0 = 0$,
  $\beta_i = \xi^{-i}-1$, $\alpha_0 = 1$ extends to an $\mathrm{RC}(D;R)$ contraction for
  every $p > W(D,r)$. One has $W(D,D) = T_W(D)$ and $W(D,2) < ((D-1)^2+1)^2$ for $D \ge 4$.
  \item If $D \ge 4$ and $r \le D$, an $\mathrm{RC}(D;R)$ contraction exists for every
  $p > \max(4D^{r+1}, 4r^2D^5)$.
\end{enumerate}
\end{proposition}

\begin{proof}
(i) Column $0$ holds as in Proposition~\ref{prop:app-s2-TW}. For $j \ne 0$,
Lemma~\ref{lem:app-s2-weil-count} for the character of order $D$ with $\ell = r$ gives
$D^r|X_j| \ge p - A\sqrt p - rD^{r-1}$. For $r = 2$, $A = (D-1)^2$ and the bound reduces to
$D^2 - 4D + 2 > 0$.
(ii) Draw $\beta_i$ ($i \in R\setminus\{0\}$) uniformly. The proof of
Lemma~\ref{lem:app-s2-moments} with rows restricted to $R$ gives
$\mathbb{E}n_j^2/(\mathbb{E}n_j)^2 = D^rp^{r-1}/(p-1)^r + LF$ with $0 < L \le 1$ and
$F = D^{-1}\sum_c(1+\delta'_c)\prod_{i\in R\setminus0}(1+\delta_{-i-c})$. By
Lemma~\ref{lem:app-s2-cyclo} (with $D$ for $\kappa$) and $\sum_c\sum_{i}\delta_{-i-c} = 0$,
$F \le 1 + (r-1)\Delta^2 + (1+\Delta)e^{(r-1)\Delta}(r-1)^2\Delta^2/2$. For
$p \ge \max(4D^{r+1},4r^2D^5)$ one has $D^rp^{r-1}/(p-1)^r \le 1.001/(4D)$ and
$\Delta \le 0.5003/(r\sqrt D)$, so the ratio is below $1 + 0.4312/D < D/(D-1)$, and the
union bound over the $D$ columns of Proposition~\ref{prop:app-s2-TA}(i) applies.
\end{proof}

\begin{corollary}[polynomial thresholds for composite $\kappa$]
\label{cor:app-s2-tower}
Let $\kappa = q_1\cdots q_L$ be composite with primes $q_1 \ge \cdots \ge q_L$ and
$q = q_1$, and use $D_t = q_1\cdots q_t$. For every prime $p \equiv 1 \pmod\kappa$ with
$p > \max\bigl(T_A(q)[q \ge 5],\, 4\kappa^{q+1},\, 4q^2\kappa^5\bigr)$, in particular
$p > 4\kappa^{\max(q+1,7)}$, any $(a+1)\prod_t((q_t-1)a+1)$ columns admit a solution
of~\eqref{eq:app-s2-target}. For $\kappa = 2^L$ the bound is $p > ((\kappa-1)^2+1)^2$ with
$(a+1)^{L+1}$ columns, and the scalars cost $\poly(\kappa)\log(1/\varepsilon)$ draws.
\end{corollary}

\begin{proof}
Step $1$ is $E_2(q) = \emptyset$ for $q \le 3$ (Corollary~\ref{cor:app-s2-small}) and
$p > T_A(q)$ otherwise; steps $t \ge 2$ use Proposition~\ref{prop:app-s2-step-threshold}
with $D_t \ge 4$ and $r_t = q_t$; for $\kappa = 2^L$ use (i) with $r = 2$ and
$E_2(2) = \emptyset$.
\end{proof}

\begin{remark}[arity and scope]
The arity has degree $L+1 = \Omega(\kappa)+1$ in $a$, so it is quadratic only for the
two-level construction itself; the tower does not close the square gap of
Remark~\ref{rem:two-level-threshold-size}, it bypasses it at higher arity. For prime
$\kappa$ it is the two-level construction. Exhaustive searches (finite computations,
AI-checked, pending human review) give the primes $p \equiv 1 \pmod\kappa$ at which no
tower or union-target chain was found: $\{5,13\}$ for $\kappa = 4$, $\{11\}$ for
$\kappa = 5$, $\{7,13,19,31,43,67\}$ for $\kappa = 6$, $\{29,43,71,113\}$ for $\kappa = 7$,
$\{17,41,73,89,137,233\}$ for $\kappa = 8$ and ten primes below $434$ for $\kappa = 9$;
all lie in $E_2(\kappa)$.
\end{remark}
```

(The κ = 7 entry depends on the pending re-check of §5.4. The union-target variant used
for κ = 5, 7 and some small primes is described in the report, §3.5, and is not in the
proposed text; if the integrator wants those finite statements, the Definition needs the
union target K and the condition α_0 + β_0 ∈ Q_0.)

### 8.2 Sentence in `main.tex`, Remark rem:two-level-threshold-size

Current: "… and $\kappa^{(\kappa+1)/2}$ is where the expected number of contractions crosses
one. Closing this square gap is open."

Proposed: "… and $\kappa^{(\kappa+1)/2}$ is where the expected number of contractions crosses
one. Closing this square gap is open. For composite $\kappa$ it can be bypassed at a cost in
arity (AI-checked, pending human review): refining the cosets one prime factor
$q_1 \ge \dots \ge q_L$ of $\kappa$ at a time gives a solution from
$(a+1)\prod_t((q_t-1)a+1)$ arbitrary columns for every prime $p \equiv 1 \pmod\kappa$
above $\max(T_A(q_1)[q_1 \ge 5], 4\kappa^{q_1+1}, 4q_1^2\kappa^5)$, and above
$((\kappa-1)^2+1)^2 < \kappa^4$ when $\kappa$ is a power of $2$
(Appendix~\ref{app:s2-tower}); the arity has degree $L+1$ in $a$, so this does not replace
the two-level construction."

## 9. What remains

1. **The two-level square gap itself.** It is untouched: E_2(κ) still has a proved
   threshold of exponent κ + 1, against an observed exponent of (κ+1)/2.
2. **O(a²) at poly(κ) thresholds.**
   - **Adaptive tower [conjecture; sketch only, not run].** In the triangular solver
     (prop:triangular-sde), replace "a dependence among the next a − dim U + 1 columns" by
     "a level-(t−1) tower relation modulo U_k".
   - With level-(t−1) relations of coefficients in P_{D_{t−1}}, the RC(D_t; R_t)
     contraction should play the role of (α, β).
   - This would use f_t(a) = Σ_{m≤a} f_{t−1}(m) columns with f_0(m) = m + 1, i.e.
     C(a+L+1, L+1) ≈ a^{L+1}/(L+1)!. The constant improves; the degree does not.
   - Whether any scheme with a poly(κ) threshold has arity O(a²) is the next hard
     question. No lower bound is known.
3. **Prime κ.** The tower gives nothing, and the gap for prime κ is fully open. The best
   statement remains T_A(κ) ≤ κ^{κ+1}.
4. **The paper.** It would need a decision on whether the tower enters the combined
   schedule. The worst-case exponent E_W(c) is maximised at small primes. There the tower
   also fails, e.g. p = 5, 13 at κ = 4, so E_W(c) probably does not move. This was not
   computed.
5. **Bookkeeping.** The κ = 7 step-1 re-check (§5.4) must finish. The 21 RC(8,{0,2,4,6})
   INFEASIBLE claims above 260 have only the C search; a faster independent checker would
   close that.
6. **Human review.** Lemma 2.2, Theorem 2.3, Propositions 3.1–3.4, Lemma 3.3 and
   Theorem 4.2.

## 10. Artifacts (`2026-11-05-rees-threshold-6/`)

| file | content |
|---|---|
| `rect.c` | complete/randomized RC(D; mZ_D) search; reproduces E_2(2) = E_2(3) = ∅, E_2(4), E_2(5) to 3000 and E_2(6) (`e2_k6_check.out`) |
| `rectu.c` | RC(D; R → K), complete DFS and randomized modes; `ALLOWDUP=1` admits repeated β |
| `rectp.c` | randomized witness search with exponentiation coset tests (large p) |
| `verify.py` | independent sympy checker (witnesses, brute re-decision, coverage) |
| `thresholds.py`, `thresholds.out` | W, T_R, union-Weil constants; T_W sanity check |
| `tr_bound.py`, `tr_bound.out` | numerical check of Lemma 3.3 |
| `mu.py`, `mu.out` | random-model counts for Conjecture 6.4 |
| `tower.py`, `tower_demo.out` | end-to-end tower with exact checks, including adversarial columns |
| `rc_*.out`, `v_rc_*.out` | step searches and their verifications (§5.1) |
| `u5_*.out`, `u7_*.out`, `v_u5_*.out`, `v_u7_*.out` | union chains for κ = 5, 7 (§5.4) |
| `union_explore.sh/.out` | first union search (distinct β only; superseded) |
| `union_explore2.sh/.out`, `uw_*.out`, `verify_uw.sh`, `v_uw.out` | union search with repeated β, per-K log and verified witnesses |

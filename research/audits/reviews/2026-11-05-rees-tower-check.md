# Adversarial check of the coset-refinement tower (threshold round 6)

5 November 2026. AI-only check by the tower checker (Claude Code session). It is not a
human review. **"AI-checked, pending human review" applies to every statement below and to
the text it inserted into the paper.**

Input: `2026-11-05-rees-threshold-6.md` and its folder. Paper context read: Appendix A
(`appendix-schedule2.tex`: app:s2-tensor, lem:app-s2-witness, lem:app-s2-normal,
lem:app-s2-weil-count, app:s2-TA with T_A) and `main.tex` thm:power-sde,
prop:decoupled-sde, rem:two-level-threshold-size. Scripts and outputs of this check:
`2026-11-05-rees-tower-check/` (interpreter `/opt/anaconda3/bin/python`, all runs under
`nice -n 10`, at most two processes; commands in `run_all.sh`). They share no code with the
report's `tower.py`, `rect*.c` or `verify.py`.

## 0. Verdict

- **No Error.** Lemma 2.2, Theorem 2.3, Propositions 3.1, 3.2, 3.4, Lemma 3.3, Theorem 4.2
  and Corollaries 4.1, 4.3 were re-derived independently and hold as stated. The findings
  are 2 Gaps and 5 Imprecisions. All of them are in the proposed LaTeX of §8 or in
  statements the paper does not use, and all were fixed in the inserted text.
- **Integrated.** `app:s2-tower` was inserted into `appendix-schedule2.tex`, after
  Table tab:app-s2-thresholds and before app:s2-scope. One sentence was added to
  rem:two-level-threshold-size in `main.tex`. Both say that the tower is an alternative
  construction, with a polynomial threshold at higher arity. It does not lower the
  Schedule 2 arity and changes neither E_2(κ), E_W(c) nor tab:main-regimes. The exact text
  is in §5.
- **κ = 7 row left out.** `2026-11-05-rees-threshold-6/v_u7_step1A.out` was still empty
  (0 bytes) when this check ended; the independent re-check (PID 45304) was still running.
- **Build** (copy in the scratchpad `build-tower/`): latexmk exit 0, 157 pages, 0 Overfull,
  no undefined references or citations, no "Float too large". `pytest -q
  tests/tools/test_rees_paper_numbers.py`: 2 passed. `make_numbers.py` was not run.

## 1. Re-derivation (Step 1)

### (a) Refinement step (Lemma 2.2)

- Inputs: relations c^ν with disjoint supports, D-classes in R, and one coefficient of
  class 0. Put U_i^ν = Σ_{cls_D c_b = i} c_b λ_b. Then Σ_{i∈R} U_i^ν = 0, because every
  nonzero coefficient has class in R.
- There are N = (r−1)a + 1 vectors (U_i^ν)_{i∈R∖0} in F^{(r−1)a}, so a dependence η ≠ 0
  exists. It also kills i = 0, by linearity.
- Output c'_b = η_ν(α_j + β_i)c_b with j = cls η_ν and i = cls c_b. Then
  Σ c'_b λ_b = Σ_ν η_ν α_{j(ν)} Σ_i U_i^ν + Σ_i β_i Σ_ν η_ν U_i^ν = 0. (For ν with η_ν = 0
  the terms vanish, so j(ν) does not need to be defined there.)
- A nonzero output has class j − (i + j) + i = 0. At (ν*, b_ν*) both classes are 0, so the
  value is α_0 + β_0 ∈ Q_0^{(D)}, which is nonzero.
- **Why each unknown faces only r conditions.** The rows are indexed by the input classes,
  and those lie in R. The columns are indexed by the classes of η_ν, which are arbitrary, so
  they run over all of Z_D. Hence α_j lies in exactly |R| = r cells, and β_i in D cells.
- **Classes modulo D from one ξ.** ξ = g^e with gcd(e, κ) = 1. For x = g^n, ind_κ(x) ≡
  e^{−1}n (mod κ). So x ∈ P_D iff D | n iff D | ind_κ(x), and the D-class is ind_κ(x) mod D.
- The union-target version (cells in {0} ∪ ⋃_{k∈K} Q_{k−i−j}, α_0 + β_0 ∈ Q_0, inputs with
  one class-0 coefficient) has the same proof: the output class is k ∈ K. Remark 2.4 is also
  correct. For a subgroup R, π(m) = um preserves R; for a union K, it moves K to π^{−1}K.

### (b) Composition and column count (Theorem 2.3)

- Induction: the groups after step t − 1 have coefficients in P_{D_{t−1}}, and one of them
  equals 1. An index divisible by D_{t−1} has D_t-class in D_{t−1}Z_{D_t} = R_t. So
  hypothesis (i) of the lemma holds, and the coefficient 1 gives (ii).
- The output is divided by α_0 + β_0 ∈ P_{D_t}. This keeps all coefficients in the group
  P_{D_t} and restores a 1.
- Group sizes: M_0 = a + 1 and M_t = ((r_t − 1)a + 1)M_{t−1}. So
  M = (a+1)∏_t((r_t−1)a+1) exactly. The count of eliminations is
  Σ_t M/M_t ≤ M. The largest elimination is (κ−1)a × ((κ−1)a+1).
- L = 1: with C_ij = z_iz_j(α_j+β_i), c_b = z_iω_b^κ and η_ν = z_jϖ_ν^κ, the output
  η_ν(α_j+β_i)c_b equals C_ijω'^κ_b of lem:app-s2-witness, up to the common factor
  (α_0+β_0)^{−1}. Hence "for L = 1 this is the two-level construction" holds.
- After step L the relation has coefficients in P_κ = Q_0. Taking κ-th roots and then
  lem:app-s2-gcd(b) solves (eq:app-s2-target) whenever κ = gcd(d, p−1).
- The arity bound (q_t−1)a + 1 ≤ q_t a, for a ≥ 1, gives M ≤ κ(a+1)a^L.

### (c) Thresholds

- **Prop 3.1 (W).** With ℓ = r and c_i = 1, lem:app-s2-weil-count (for the character
  χ^{κ/D}, of order D) gives D^r|X_j| ≥ p − r − D^rE_D(r,p). Here
  D^rE_D(r,p) = A√p + rD^{r−1} − r with A = (r−1−r/D)D^r + 1, which yields the stated
  quadratic in √p. The roots r_i = 1 − ξ^{−i} are distinct for distinct i mod D.
  - W(D,D) = T_W(D).
  - √W ≤ A + √(rD^{r−1}) ≤ rD^r.
  - r = 2: √W < (D−1)² + 1 ⇔ D² − 4D + 2 > 0, which needs D ≥ 4. At D = 3,
    W = 26.65 > 25, so the restriction D ≥ 4 is needed.
  - r = 3: 3D² − √3D − 1 ≥ 0.

  All of these were checked numerically for D < 2000 (`thresholds_check.out`).
- **Prop 3.2 (second moment).**
  - E n_j = h(h/p)^{r−1}.
  - The pair count gives m_{−(i+c)}. Its index runs over −c − (R∖0), r − 1 distinct
    indices.
  - ρ = D^rp^{r−1}/(p−1)^r + ΓF, with Γ = ((p−D−1)/(p−1))^r(p/(p−1))^{r−1} ≤ 1. Checked by
    expanding μ^r D p^{r−1}/h^{2r−1}.
  - Σ_c s_c = (r−1)Σδ_b = 0.
  - The remainder bound (1+Δ)^{r−1} − 1 − (r−1)Δ ≤ e^{(r−1)Δ}((r−1)Δ)²/2 is the Taylor
    bound for e^x − 1 − x.
  - Union bound: ρ < D/(D−1) ⇔ D(1 − 1/ρ) < 1.
  - Monotonicity holds as stated. No step uses that R is a subgroup.
- **Lemma 3.3 (explicit constants).** Each constant was recomputed:
  - p ≥ 16D^5 ≥ 16384, and r/(p−1) ≤ 2.5·10^{−4}.
  - D^r/p ≤ 1/(4D).
  - Δ ≤ D²/(√p(1 − 4·10^{−4})) ≤ 1.0005D²/√p ≤ 0.50025/(r√D). So (r−1)Δ ≤ 0.2501 and
    Δ ≤ 0.1251.
  - 1.1251·e^{0.2502}/2 = 0.72247.
  - r − 1 ≤ 0.7225(2r − 1).
  - E_r ≤ 0.7225·0.2503/D = 0.1808/D, and the total is 0.4312/D < 1/(D−1).

  Numerically, D·(left side) at p = P(D,r) is at most 0.3494, at (D, r) = (25, 5), over
  4 ≤ D ≤ 64 and 2 ≤ r ≤ D. This matches the report's 0.349.
- **Prop 3.4 (union Weil).** The indicator expansion Σ_s ĉ_sω^{−ts}χ^s, the weights
  c_0^{ℓ−s}∏|ĉ| and the sums Σ_s C(ℓ,s)c_0^{ℓ−s}G^s = F^ℓ − c_0^ℓ and
  Σ_s sC(ℓ,s)c_0^{ℓ−s}G^s = ℓGF^{ℓ−1} are correct. K = {0} reproduces T_W at D = 3, 4, 5.
  Recomputed thresholds:

  | D | K | threshold |
  |---|---|---|
  | 5 | {0,1} | 761852.8 |
  | 5 | {0,1,2} | 37246.4 |
  | 7 | {0,1,2,3} | 2.2558·10^7 |
  | 7 | {0,1} | 2.70·10^{10} |
- **Theorem 4.2.**
  - Step 1: E_2(q) = ∅ for q ≤ 3, and p > T_A(q) for q ≥ 5, since p ≡ 1 (mod q).
  - Steps t ≥ 2: D_t ≥ q_1q_2 ≥ 4 and r_t = q_t ≤ q_1 ≤ D_t. So Lemma 3.3 applies, and
    P(D_t, q_t) ≤ max(4κ^{q+1}, 4q²κ^5).
  - Last form: T_A(q) ≤ q^{q+1} (prop:app-s2-TA(ii), q ≥ 3) and 4q²κ^5 ≤ 4κ^7.
  - Θ(κ) was recomputed for κ ∈ {4,6,8,9,10,12,16,18,24,27,32}, and every per-step
    min(W, T_R) ≤ P(D_t, q_t) ≤ the closed form was asserted. All recomputed W, T_R values
    agree with the report's table, e.g. T_R(9,3) = 134723.2, W(8,2) = 2432.89,
    W(16,2) = 50688.98 and T_R(7,4) = 68957.6.

### (d) Special cases

- **κ = 2^L.** Every r_t = 2 and D_t = 2^t. Step 1 is E_2(2) = ∅. For t ≥ 2,
  W(2^t, 2) < ((2^t−1)²+1)² ≤ ((κ−1)²+1)². M = (a+1)^{L+1}. Holds; Θ(κ) <
  ((κ−1)²+1)² was asserted numerically for κ = 4, 8, 16, 32.
- **κ = 2^u3^v.** Since q ≤ 3, there is no T_A term and max(4κ^{q+1}, 4q²κ^5) ≤ 36κ^5.
  Holds. It is the general bound itself, not a separate argument.

### (e) Scalars and finding cost

- The scalars depend only on (p, κ, ξ) and the fixed chain. This is clear: none of them
  sees the columns.
- **poly(κ) finding cost.** Proved only for κ = 2^L (Cor 4.1), and that proof holds.
  - Above 4(κ²+1)²: D²|X_j| ≥ p/2 once √p ≥ 2(D²+1), so O(D²τ) draws per α_j.
  - Between ((κ−1)²+1)² and 4(κ²+1)²: O(κp) = O(κ^5) coset tests by enumeration.
  - Step 1 at D = 2 is covered by prop:app-s2-TW(ii) above 100.

  For general κ the report does not claim a finding cost. Theorem 4.2 and Lemma 3.3 give
  only existence. See Finding G2.

## 2. Findings

| # | grade | where | finding | fix in the inserted text |
|---|---|---|---|---|
| G1 | Gap | report §8.1, proposed `\begin{remark}[arity and scope]` | The proposed remark lists the primes not covered by a "tower or union-target chain", but the proposed text defines only K = {0}. κ = 5 and the primes 29 (κ = 4), 79, 139 (κ = 6), 761 (κ = 8) and 271, 379, 487, 523 (κ = 9) rest on union chains. The report flags this itself (after §8.1). | The remark now states the union-target version of lem:app-s2-refine: the cells lie in {0} ∪ ⋃_{k∈K}Q_{k−i−j}, α_0+β_0 ∈ Q_0 is kept, and the inputs need only a class-0 coefficient. The proof is the same (§1(a)). It also defines a union chain and its arity. |
| G2 | Gap | report Thm 4.2 / proposed corollary; the task's (e) | "Sampler cost poly(κ)" is proved only for κ = 2^L. For general κ no finding cost is given. Exhaustive search is not "constant for fixed κ" for unbounded p, so it needs an explicit sampling range. | A paragraph "Finding the scalars" says three things. Above 4((r−1)D^r+1)² the Weil β gives D^r\|X_j\| ≥ p/2, using A + rD^{r−1} = (r−1)D^r + 1, so ⌈2D^rτ⌉ draws per α_j suffice. Below that bound p is bounded in κ and exhaustive search is constant for fixed κ. For κ = 2^L the cost is poly(κ)·k draws, or O(κ^5) tests in the band. No polynomial bound is claimed for general κ; step 1 already costs O(q^{q+1} log q) draws per round. |
| I1 | Imprecision | proposed remark | "degree L+1 = Ω(κ)+1" reads as big-Omega in this paper. | "L ... is at most the number of prime factors of κ counted with multiplicity". |
| I2 | Imprecision | proposed prop:app-s2-step-threshold(ii) proof | The step E_r ≤ 0.1809/D is skipped. L is used both for the chain length and for the factor ((p−D−1)/(p−1))^r(p/(p−1))^{r−1}. The use of lem:app-s2-weil-count, lem:app-s2-moments and lem:app-s2-cyclo with D in place of κ is not justified. | The proof now gives every constant of Lemma 3.3 and renames the factor Γ. A sentence states that the three lemmas hold, with the same proofs, for the cosets of P_D and the character χ^{κ/D} of order D. |
| I3 | Imprecision | proposed corollary | It uses the Iverson bracket "T_A(q)[q ≥ 5]" and "log(1/ε)", with ε undefined in the appendix. The 3-smooth bound 36κ^5 of Cor 4.3 is missing. | Written as "and also p > T_A(q) if q ≥ 5". The cost is given as poly(κ)·k for abort probability 2^{−k}. "If κ = 2^u3^v, p > 36κ^5 suffices" is added. |
| I4 | Imprecision | proposed lemma | "one coset test per coefficient" omits the tests on the η_ν. | "one coset test for each coefficient of the c^ν and of the dependence η". |
| I5 | Imprecision | report §4 comparison and §5.2 (not used by the paper) | "κ = 2q: Θ ≈ q^{q+1}, about the square root of the two-level threshold" is only an order-of-magnitude statement: (2q)^{q+1/2} against q^{q+1}. The 21 INFEASIBLE claims of RC(8,{0,2,4,6}) above 260 rest on one program only. | Not used. The κ = 8 entries of the paper need only RC(4,{0,2}) and RC(8,{0,4}), which were both re-decided here (§3.3). |

Two further remarks, neither a finding:

- **Shortcut for the subgroup chains.** E(D;R) ⊆ E(D;R') when R ⊆ R', because
  restricting the rows of an RC(D;R') contraction gives an RC(D;R) contraction. The last
  step of every subgroup chain is RC(κ;R) with R ⊇ R_min, where R_min is a minimal nonzero
  subgroup. So to show that *every* subgroup chain fails at a prime, it suffices that each
  minimal last step fails. For κ = 6 these steps are {0,3} and {0,2,4}; for κ = 4, 8, 9 the
  single step {0,κ/2} or {0,3,6} has to fail. This is how the "no tower" half of the
  uncovered lists was re-derived.
- **Membership in E_2(κ).** Lemma 7.1 is correct. With the shortcut above, it gives the
  membership of every listed prime in E_2(κ) as a proof rather than a comparison of lists.

## 3. Numerical tests (independent code)

### 3.1 Thresholds (`thresholds_check.py` → `thresholds_check.out`)

50-digit mpmath. It recomputes every W, T_R, P, union-Weil value and Θ(κ), and asserts the
inequalities listed in §1(c), (d). All agree with the report.

### 3.2 End-to-end tower (`tower_check.py tower`, `run_towers.sh` → `towers_A.out`, `towers_B.out`)

**Implementation.**

- The tower of Theorem 2.3 is written from scratch: Gaussian elimination mod p, and coset
  classes by exponentiation x^{(p−1)/D}.
- The contraction finder uses a discrete-log table, with ξ = the least primitive root. It
  tries the Weil β of Prop 3.1 ("weil" mode), then random β, then a complete FFT search
  over β ∈ {0} × F_p^{r−1} for r ≤ 3.
- Every contraction is re-checked by exponentiation before use.

**Final check, exact:**

- u ≠ 0;
- Σ u_b^κ λ_b = 0;
- s = u^t with d = κd′, gcd(d′, (p−1)/κ) = 1, d′ random, t = d′^{−1} mod (p−1)/κ;
- s ≠ 0 and Σ s_b^d λ_b = 0.

The tower also asserts, at every step, that all input classes lie in R_t and that all output
coefficients lie in P_{D_t}.

**Columns.** Eight families per a, each shuffled:

- random;
- all zero;
- all equal;
- unit vectors;
- rank one with random scalars;
- zero/repeat/random mixed;
- cancelling pairs;
- entries in {0, ±1}.

**Results:**

| κ | chain | p | a | result |
|---|---|---|---|---|
| 4 | (2,4) | 5, 13, 29 | — | no RC(4,{0,2}) (complete search), as claimed |
| 4 | (2,4) | 17, 37, 53 (∈ E_2(4)) | 1,2,3 | OK, all families |
| 4 | (2,4) | 97, 101, 109, 113 (> W(4,2) = 96.3; 101, 109 > ((κ−1)²+1)² = 100) | 1,2,3 | OK, Weil β |
| 6 | (3,6) | 7, 13, 79, 139, 223 | — | no RC(6,{0,3}), as claimed |
| 6 | (3,6) | 37, 859 (max E_2(6)) | 1,2,3 | OK |
| 6 | (3,6) | 661, 673, 691 (> W(6,2) = 648.8) | 1,2,3 | OK, Weil β |
| 6 | (3,6) | 279949, 279967 (> 4q²κ^5 = 279936) | 1,2 | OK, Weil β |
| 6 | (2,6) | 7, 37, 61, 97, 139 | — | no RC(6,{0,2,4}), as claimed |
| 6 | (2,6) | 223, 859 | 1,2,3 | OK |
| 8 | (2,4,8) | 17, 233, 761 | — | no RC(8,{0,4}), as claimed |
| 8 | (2,4,8) | 1553, 11689 (∈ E_2(8)) | 1,2 | OK |
| 8 | (2,4,8) | 2441, 2473 (> Θ = 2432.9), 2521, 2593 (> 2500) | 1,2 | OK, Weil β at both steps |
| 9 | (3,9) | 19, 433, 523, 271 | — | no RC(9,{0,3,6}), as claimed |
| 9 | (3,9) | 17911, 17929 | 1,2 | OK |
| 9 | (3,9) | 134353, 134371 (just below T_R = 134723), 134731, 134839, 134857 (just above) | 1,2 | OK, random β |
| 9 | (3,9) | 2125801, 2125819 (> 4q²κ^5 = 2125764 > W(9,3) = 1.48·10^6) | 1,2 | OK, Weil β |

**Negative control** (`negative_control.out`). One cell of a valid last-step contraction
was corrupted. The checker then reported failures on 6/20, 5/20 and 3/20 random inputs, at
(κ, p) = (4, 101), (8, 2441) and (9, 17929). So the checks are not vacuous.

**Union chains end to end** (`union_e2e.py` → `union_e2e.out`). The report's own step
witnesses were fed into an independent union-target solver, which checked the same as above.
All runs OK:

- κ = 4, p = 29;
- κ = 6, p = 79, 139;
- κ = 8, p = 761;
- κ = 9, p = 271, 523;
- κ = 5 at the 8 primes 31, 41, 61, 71, 101, 131, 151, 181 of E_2(5)∖{11}.

The two steps of each chain use the same g (checked).

### 3.3 Exceptional sets re-decided (`tower_check.py excset` → `excsets.out`)

Each prime was searched randomly first. Every prime not settled that way got a complete FFT
search over β (normal form β_0 = 0, zeros allowed). All seven sets agree exactly with the
report's §5.1:

| step | range | result |
|---|---|---|
| E(4;{0,2}) | p ≡ 1 mod 4, ≤ 3000 | {5,13,29} |
| E(4;{0,2}) | p ≡ 1 mod 8, ≤ 6000 | ∅ |
| E(6;{0,3}) | ≤ 3000 | {7,13,19,31,43,67,79,139,223} |
| E(6;{0,2,4}) | ≤ 12100 | the 12 primes of §5.1 |
| E(8;{0,4}) | ≤ 6000 | {17,41,73,89,137,233,761} |
| E(16;{0,8}) | ≤ 51000 | the 17 primes of §5.1 |
| E(9;{0,3,6}) | every prime p ≡ 1 mod 9 up to 135000 > T_R(9,3), 2093 primes | the 14 primes of §5.1 |

Each "checked to" bound exceeds the proved threshold of that step (W or T_R).

### 3.4 Report witnesses re-checked (`witness_check.py witnesses` → `witnesses.out`)

The checker reads each line `p FEASIBLE g=… beta … alpha …`. It checks that g generates
F_p^×/P_D, and it checks every cell by exponentiation, including α_0 + β_0 ∈ Q_0. The
following files were checked in full:

- rc_4_2, rc_6_3, rc_6_2, rc_6_2b, rc_8_4, rc_8_2_lo, rc_8_2_mid, rc_9_3_low and rc_16_8;
- u5_step1_lo, u5_step2, u7_step2A_lo and u7_step1A_lo;
- all 18 uw_* files.

Random samples were checked from the large files: 400 lines each from rc_8_2_hi, rc_9_3_hi,
u5_step1_hi and u7_step2A_hi, and 1000 from u7_step1A_hi. In total 5154 witnesses were
checked, and **bad = 0**.

### 3.5 "Uncovered" primes re-decided (`witness_check.py uncovered` → `uncovered*.out`)

For each claimed uncovered prime, every K ∋ 0 with |K| ∈ {2,3} was tested.

- Step 2, RC(κ;K), was decided by the complete FFT search.
- Where step 2 is feasible, step 1, RC(κ;Z_κ → K) with repeated β allowed, was decided by
  a complete DFS with a column prune.
- Positive controls (`step1_control.out`): the DFS finds the known feasible step-1
  instances at (κ,p,K) = (4,29,{0,1}), (6,79,{0,1}) and (8,761,{0,1}). It also finds
  (5,11,{0,1}) feasible, which reproduces the repeated-β correction of report §7.3.

Results, with the "no tower" half from §2 and §3.3:

- **κ = 4** (5, 13), **κ = 5** (11), **κ = 6** (7, 13, 19, 31, 43): step 2 is infeasible
  for every K.
- **κ = 6, p = 67:** step 2 is feasible for K = {0,1}, {0,2}, {0,4}, {0,5}. Step 1 is
  infeasible for each of them.
- **κ = 8, κ = 9:** see the table below. Where a K survives step 2, step 1 fails.

| κ | p | step 2 infeasible for | K surviving step 2 (step 1 then infeasible) |
|---|---|---|---|
| 8 | 17, 41, 73 | all 28 K | none |
| 8 | 89 | 26 of 28 | {0,2}, {0,6} |
| 8 | 137 | 26 of 28 | {0,2}, {0,6} |
| 9 | 19, 37, 73 | all 36 K | none |
| 9 | 109 | 34 of 36 | {0,2}, {0,7} |
| 9 | 127 | 32 of 36 | {0,3}, {0,4}, {0,5}, {0,6} |
| 9 | 163 | 34 of 36 | {0,4}, {0,5} |
| 9 | 181 | 28 of 36 | {0,1}, …, {0,8} |
| 9 | 199 | 28 of 36 | the 8 sets {0,k} |

**Not independently re-decided:** κ = 8, p = 233, and κ = 9, p = 307, 433. My step-1 DFS
had not finished at p = 233 after 40 minutes, so I stopped both runs. The "tower" half
holds for these three primes, by §2 and §3.3. The "union chain" half rests on the
report's complete search alone (`union_explore2.out`).

Every independently re-decided claim is confirmed. Every listed prime lies in E_2(κ), by §2 (second remark); this part is proved for all of them.

## 4. What was not done

- **κ = 7.** The κ = 7 coverage row is not in the paper. `v_u7_step1A.out` is empty.
  - My checker passed all 126 lines of `u7_step1A_lo.out` and a 1000-line sample of the
    hi file.
  - The paper's κ = 7 entry needs only the witnesses at the 52 primes of E_2(7) outside
    {29, 43, 71, 113}, because E_2(7) is known exactly below 5·10^6 > T_A(7). It does not
    need all 236878 witnesses.
  - Whether to add the row once the re-check finishes is for the next integrator.
- **RC(8,{0,2,4,6}).** Its INFEASIBLE claims above 260 were not re-decided (r = 4, and my
  complete search handles r ≤ 3). The paper does not use them.
- **Prop 3.4 thresholds.** These (761853, 2.2558·10^7) are not needed by the inserted text.
  κ = 5 coverage follows from E_2(5), which is exact and cited, together with the
  union-chain witnesses at its eight other primes.
- **Nothing committed;** no git state changed.

## 5. Text inserted into the paper (exact)

### 5.1 `appendix-schedule2.tex`

Inserted after `\label{tab:app-s2-thresholds}\end{table}` and before
`\subsection{What is and is not shown}`, by exact-string replacement (count asserted 1).

```latex
\subsection{A tower of coset refinements}
\label{app:s2-tower}

\noindent\textbf{Status: AI-checked, pending human review} (\file{research/audits/reviews/2026-11-05-rees-threshold-6.md}, re-derived and tested in \file{research/audits/reviews/2026-11-05-rees-tower-check.md}). This subsection gives an alternative construction for composite $\kappa$. Its prime threshold is polynomial in $\kappa$, but its arity has higher degree in $a$. It is not used by Theorem~\ref{thm:power-sde}, Proposition~\ref{prop:decoupled-sde}, Remark~\ref{rem:combined-schedule} or the tables. It does not lower the Schedule~2 arity $(a+1)((\kappa-1)a+1)$, and it changes neither $E_2(\kappa)$ nor the exponent $E_W(c)$ nor Table~\ref{tab:main-regimes}.

For $D \mid \kappa$ put $P_D = \{x^D : x \in \Fp^\times\}$ and $Q^{(D)}_m = \xi^mP_D$ for $m \in \mathbb{Z}_D$, so that $P_\kappa = Q_0$. Since the image of $\xi$ generates $\Fp^\times/Q_0$, it generates $\Fp^\times/P_D$, and $x \in Q^{(D)}_m$ exactly when $\operatorname{ind}(x) \equiv m \pmod D$. So one coset test gives the class of $x$ modulo every $D \mid \kappa$, and $x \in P_D$ if and only if $D$ divides $\operatorname{ind}(x)$. A \emph{relation} is a vector $c \in \Fp^M$ with $\sum_b c_b\lambda_b = 0$; its \emph{$D$-classes} are the residues $\operatorname{ind}(c_b) \bmod D$ of its nonzero coefficients.

\begin{definition}
Let $D \mid \kappa$ with $D \ge 2$, and let $0 \in R \subseteq \mathbb{Z}_D$ with $|R| = r$. A \emph{refinement contraction} $\mathrm{RC}(D;R)$ is a pair $\alpha \in \Fp^{\mathbb{Z}_D}$, $\beta \in \Fp^{R}$ with $\alpha_0 + \beta_0 \ne 0$ and $\alpha_j + \beta_i \in Q^{(D)}_{-(i+j)} \cup \{0\}$ for all $i \in R$ and $j \in \mathbb{Z}_D$. For $R = \mathbb{Z}_D$ it is a two-level contraction at $(p,D)$ in the normal form of Lemma~\ref{lem:app-s2-normal}.
\end{definition}

\begin{lemma}[refinement step]
\label{lem:app-s2-refine}
Let $(\alpha,\beta)$ be an $\mathrm{RC}(D;R)$ contraction and $N = (r-1)a+1$. Let $c^1,\dots,c^N$ be relations with pairwise disjoint supports $S^\nu$, all of whose $D$-classes lie in $R$, and with $c^\nu_{b_\nu} = 1$ for some $b_\nu \in S^\nu$. One Gaussian elimination of size $(r-1)a \times N$, and one coset test for each coefficient of the $c^\nu$ and of the dependence $\eta$ below, give a relation $c'$ supported in $\bigcup_\nu S^\nu$, with every nonzero coefficient in $P_D$ and with $c'_{b_{\nu^\ast}} = \alpha_0 + \beta_0$ for some $\nu^\ast$.
\end{lemma}

\begin{proof}
For $i \in R$ put $U^\nu_i = \sum c^\nu_b\lambda_b$, the sum over the $b \in S^\nu$ with $\operatorname{ind}(c^\nu_b) \equiv i \pmod D$. Since the $D$-classes of $c^\nu$ lie in $R$, $\sum_{i\in R}U^\nu_i = \sum_b c^\nu_b\lambda_b = 0$. The $N$ vectors $(U^\nu_i)_{i \in R\setminus\{0\}} \in \Fp^{(r-1)a}$ have a nonzero dependence $\eta$, so $\sum_\nu\eta_\nu U^\nu_i = 0$ for $i \ne 0$, and also for $i = 0$ because $U^\nu_0 = -\sum_{i\ne0}U^\nu_i$. Normalise $\eta_{\nu^\ast} = 1$ for some $\nu^\ast$ with $\eta_{\nu^\ast} \ne 0$. For $b \in S^\nu$ with $\eta_\nu c^\nu_b \ne 0$ put $c'_b = \eta_\nu(\alpha_{j(\nu)} + \beta_{i(b)})c^\nu_b$, where $j(\nu) \equiv \operatorname{ind}(\eta_\nu)$ and $i(b) \equiv \operatorname{ind}(c^\nu_b)$ modulo $D$, and put $c'_b = 0$ otherwise. Then, with the sums over $\nu$ restricted to $\eta_\nu \ne 0$,
\[
  \sum_b c'_b\lambda_b = \sum_\nu\eta_\nu\alpha_{j(\nu)}\sum_{i\in R}U^\nu_i + \sum_{i\in R}\beta_i\sum_\nu\eta_\nu U^\nu_i = 0 .
\]
A nonzero $c'_b$ has $D$-class $j + (-(i+j)) + i = 0$, so it lies in $P_D$. Finally $\eta_{\nu^\ast} = c^{\nu^\ast}_{b_{\nu^\ast}} = 1$ both have class $0$, so $c'_{b_{\nu^\ast}} = \alpha_0 + \beta_0$.
\end{proof}

Each $\alpha_j$ meets only the $r$ conditions of the rows $i \in R$, because the input classes lie in $R$; the columns run over all of $\mathbb{Z}_D$, because the classes of $\eta_\nu$ are arbitrary.

\begin{theorem}[tower]
\label{thm:app-s2-tower}
Let $1 = D_0 \mid D_1 \mid \cdots \mid D_L = \kappa$ with $D_{t-1} < D_t$, put $r_t = D_t/D_{t-1}$, and let $R_t = D_{t-1}\mathbb{Z}_{D_t}$, the subgroup of $\mathbb{Z}_{D_t}$ of order $r_t$. Suppose that an $\mathrm{RC}(D_t;R_t)$ contraction $(\alpha^{(t)},\beta^{(t)})$ is given for each $t$; for $t = 1$ this means $p \notin E_2(D_1)$. Then from any
\[
  M = (a+1)\prod_{t=1}^{L}\bigl((r_t-1)a+1\bigr)
\]
columns $\lambda_b \in \Fp^a$ one computes a solution of~\eqref{eq:app-s2-target} with at most $M$ Gaussian eliminations, each of size at most $(\kappa-1)a \times ((\kappa-1)a+1)$, $O(LM)$ coset tests and $M$ root extractions. The scalars $(\alpha^{(t)},\beta^{(t)})$ depend only on $(p,\kappa,\xi)$, not on the columns. For $L = 1$ this is the construction of Lemmas~\ref{lem:app-s2-tensor} and~\ref{lem:app-s2-witness}.
\end{theorem}

\begin{proof}
Put $M_0 = a+1$ and $M_t = ((r_t-1)a+1)M_{t-1}$, so $M = M_L$. Split the columns into blocks of $a+1$; each block has a nonzero dependence, scaled so that one coefficient is $1$. Suppose that after step $t-1$ the columns are split into groups of $M_{t-1}$, each carrying a relation with every nonzero coefficient in $P_{D_{t-1}}$ (for $t = 1$, $P_1 = \Fp^\times$) and one coefficient equal to $1$. An element of $P_{D_{t-1}}$ has index divisible by $D_{t-1}$, so its $D_t$-class lies in $R_t$. Apply Lemma~\ref{lem:app-s2-refine} with $D = D_t$ and $R = R_t$ to $(r_t-1)a+1$ groups at a time. Each output has every nonzero coefficient in $P_{D_t}$ and the coefficient $\alpha^{(t)}_0+\beta^{(t)}_0 \in P_{D_t}$; dividing by it restores a coefficient $1$ and keeps every coefficient in the group $P_{D_t}$. After step $L$ there is a nonzero relation $c$ with every nonzero coefficient in $P_\kappa = Q_0$. Put $u_b = \sqrt[\kappa]{c_b}$. Then $u \ne 0$ and $\sum_b u_b^\kappa\lambda_b = 0$, and Lemma~\ref{lem:app-s2-gcd}(b) gives the solution. Step $t$ uses $M/M_t$ eliminations and one coset test per coefficient. For $L = 1$, $R_1 = \mathbb{Z}_\kappa$, and the output coefficient $\eta_\nu(\alpha_j+\beta_i)c_b$ is, up to the common factor $(\alpha_0+\beta_0)^{-1}$, the value $u_b^\kappa = C_{ij}\omega_b'^{\,\kappa}$ of Lemma~\ref{lem:app-s2-witness}, with $C_{ij} = z_iz_j(\alpha_j+\beta_i)$, $c_b = z_i\omega_b^\kappa$ and $\eta_\nu = z_j\varpi_\nu^\kappa$.
\end{proof}

\begin{proposition}[one-step thresholds]
\label{prop:app-s2-step-threshold}
Let $D \mid \kappa$ with $D \ge 2$, and let $0 \in R \subseteq \mathbb{Z}_D$ with $|R| = r \ge 2$.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item Put $A = (r-1-r/D)D^r + 1$ and $W(D,r) = \bigl(\tfrac12(A + \sqrt{A^2 + 4rD^{r-1}})\bigr)^2$. If $p > W(D,r)$, then $\beta_0 = 0$, $\beta_i = \xi^{-i}-1$ for $i \in R\setminus\{0\}$ (with $0 < i < D$) and $\alpha_0 = 1$ extend to an $\mathrm{RC}(D;R)$ contraction with every $\alpha_j + \beta_i$ nonzero. One has $W(D,D) = T_W(D)$, and $W(D,2) < ((D-1)^2+1)^2$ for $D \ge 4$.
  \item If $D \ge 4$ and $r \le D$, an $\mathrm{RC}(D;R)$ contraction exists for every $p \ge \max(4D^{r+1}, 4r^2D^5)$.
\end{enumerate}
\end{proposition}

\begin{proof}
Lemmas~\ref{lem:app-s2-weil-count}, \ref{lem:app-s2-moments} and~\ref{lem:app-s2-cyclo} hold, with the same proofs, for the cosets of $P_D$ and the character $\chi^{\kappa/D}$ of order $D$ in place of $\kappa$ and $\chi$; we use them in that form.

(i) Column $0$ holds as in Proposition~\ref{prop:app-s2-TW}: $\alpha_0 + \beta_i = \xi^{-i} \in Q^{(D)}_{-i}$ and $\alpha_0 + \beta_0 = 1$. For $j \ne 0$ let $X_j = \{x : x + \beta_i \in Q^{(D)}_{-(i+j)} \text{ for all } i \in R\}$. Its conditions prescribe cosets of $P_D$ for $x - r_i$ with the $r$ distinct roots $r_i = 1 - \xi^{-i}$. Lemma~\ref{lem:app-s2-weil-count} with $\ell = r$ and $c_i = 1$ gives $D^r|X_j| \ge p - r - D^rE_D(r,p) = p - A\sqrt p - rD^{r-1}$, which is positive when $p > W(D,r)$; any $\alpha_j \in X_j$ completes column $j$. For $r = D$ the constants are those of $T_W(D)$. For $r = 2$, $A = (D-1)^2$, and $\sqrt{W(D,2)} < (D-1)^2+1$ reduces to $D^2 - 4D + 2 > 0$.

(ii) Draw $\beta_i$, $i \in R\setminus\{0\}$, independently and uniformly, put $\beta_0 = 0$, and let $X_j$ be as in~(i), now for every $j \in \mathbb{Z}_D$, with $n_j = |X_j|$. If every $X_j$ is nonempty, any $\alpha_j \in X_j$ give an $\mathrm{RC}(D;R)$ contraction, since $\alpha_0 \in X_0$ lies in $Q^{(D)}_0$. The proof of Lemma~\ref{lem:app-s2-moments} with the rows restricted to $R$ gives $\mathbb{E}[n_j] = h_D(h_D/p)^{r-1}$ with $h_D = (p-1)/D$, and $\mathbb{E}[n_j^2] = \mathbb{E}[n_j] + (h_D/p^{r-1})\sum_c m'_c\prod_{i\in R\setminus\{0\}}m_{-(i+c)}$. Write $m_b = \mu(1+\delta_b)$ and $m'_c = \mu(1+\delta'_c)$ with $\mu = (p-D-1)/D^2$. As in the proof of Proposition~\ref{prop:app-s2-TA}(i),
\[
  \rho \coloneqq \frac{\mathbb{E}[n_j^2]}{\mathbb{E}[n_j]^2} = \frac{D^rp^{r-1}}{(p-1)^r} + \Gamma F, \qquad
  \Gamma = \Bigl(\frac{p-D-1}{p-1}\Bigr)^{r}\Bigl(\frac{p}{p-1}\Bigr)^{r-1} \in (0,1],
\]
where $F = D^{-1}\sum_c(1+\delta'_c)\prod_{i\in R\setminus\{0\}}(1+\delta_{-(i+c)})$.
By Lemma~\ref{lem:app-s2-cyclo}, $|\delta_b|, |\delta'_c| \le \Delta \coloneqq ((D-1)(D-2)\sqrt p + 2(D-1))/(p-D-1)$ and $\sum_b\delta_b = \sum_c\delta'_c = 0$, so also $\sum_c\sum_{i\in R\setminus\{0\}}\delta_{-(i+c)} = 0$. Expanding the product to first order, with remainder at most $(1+\Delta)^{r-1} - 1 - (r-1)\Delta \le e^{(r-1)\Delta}(r-1)^2\Delta^2/2$, gives $F \le 1 + E_r$ with $E_r = (r-1)\Delta^2 + (1+\Delta)e^{(r-1)\Delta}(r-1)^2\Delta^2/2$. Now let $p \ge \max(4D^{r+1},4r^2D^5)$, so $p \ge 16D^5 \ge 16384$. Then $D^rp^{r-1}/(p-1)^r \le (D^r/p)e^{r/(p-1)} \le 1.001/(4D)$. Next $2(D-1) \le (3D-2)\sqrt p$ and $(D+1)/p \le 4\cdot10^{-4}$ give $\Delta \le 1.0005\,D^2/\sqrt p \le 0.5003/(r\sqrt D)$, so $(r-1)\Delta \le 0.2502$ and $\Delta \le 0.1251$. Hence $E_r \le \Delta^2\bigl((r-1) + 0.7225(r-1)^2\bigr) \le 0.7225\,r^2\Delta^2 \le 0.1809/D$. So $\rho \le 1 + 0.4312/D < D/(D-1)$. By Cauchy--Schwarz, $\Pr[n_j = 0] \le 1 - 1/\rho$, and the union bound over the $D$ columns, as in Proposition~\ref{prop:app-s2-TA}(i), leaves a positive probability that every $X_j$ is nonempty.
\end{proof}

\begin{corollary}[polynomial thresholds for composite $\kappa$]
\label{cor:app-s2-tower}
Let $\kappa \ge 4$ be composite, $\kappa = q_1q_2\cdots q_L$ with primes $q_1 \ge q_2 \ge \cdots \ge q_L$, and put $q = q_1$ and $D_t = q_1\cdots q_t$. Let $p \equiv 1 \pmod\kappa$ be a prime with
\[
  p > \max\bigl(4\kappa^{q+1},\, 4q^2\kappa^5\bigr), \quad\text{and also } p > T_A(q) \text{ if } q \ge 5;
\]
this holds in particular when $p > 4\kappa^{\max(q+1,7)}$. Then Theorem~\ref{thm:app-s2-tower} applies to this chain: any $(a+1)\prod_{t=1}^L((q_t-1)a+1) \le \kappa(a+1)a^L$ columns admit a solution of~\eqref{eq:app-s2-target}. If $\kappa = 2^L$, the condition $p > ((\kappa-1)^2+1)^2$ suffices, with $(a+1)^{L+1}$ columns. If $\kappa = 2^u3^v$, $p > 36\kappa^5$ suffices.
\end{corollary}

\begin{proof}
Step $1$ needs $p \notin E_2(q)$: this is Corollary~\ref{cor:app-s2-small} for $q \le 3$ and Proposition~\ref{prop:app-s2-TA}(i) for $q \ge 5$. For $t \ge 2$, $D_t \ge q_1q_2 \ge 4$ and $r_t = q_t \le q_1 \le D_t$, so Proposition~\ref{prop:app-s2-step-threshold}(ii) gives an $\mathrm{RC}(D_t;R_t)$ contraction for $p \ge \max(4D_t^{q_t+1}, 4q_t^2D_t^5)$, which is at most $\max(4\kappa^{q+1},4q^2\kappa^5)$. The arity bound uses $(q_t-1)a+1 \le q_ta$, and $T_A(q) \le q^{q+1}$ (Proposition~\ref{prop:app-s2-TA}(ii)) gives the condition $p > 4\kappa^{\max(q+1,7)}$. For $\kappa = 2^L$, every $r_t = 2$; step $1$ is $E_2(2) = \emptyset$, and the steps $t \ge 2$ use Proposition~\ref{prop:app-s2-step-threshold}(i) with $W(2^t,2) < ((2^t-1)^2+1)^2 \le ((\kappa-1)^2+1)^2$. For $q \le 3$ the maximum is at most $36\kappa^5$.
\end{proof}

\paragraph{Finding the scalars.} They depend only on $(p,\kappa,\xi)$. Step~$1$ is a two-level contraction at $(p,q)$, found as in Corollary~\ref{cor:app-s2-decoupled}. For a step $t \ge 2$ with $D = D_t$ and $r = r_t$, the $\beta$ of Proposition~\ref{prop:app-s2-step-threshold}(i) gives $D^r|X_j| \ge p - A\sqrt p - rD^{r-1} \ge p/2$ once $\sqrt p \ge 2((r-1)D^r+1)$, because $A + rD^{r-1} = (r-1)D^r + 1$; then, for any $\tau > 0$, $\lceil 2D^r\tau\rceil$ uniform draws find some $\alpha_j \in X_j$ except with probability $e^{-\tau}$. Below that bound $p$ is bounded by a function of $\kappa$, and exhaustive search is a constant for fixed $\kappa$. For $\kappa = 2^L$ every $r_t = 2$, so for $p \ge 4(\kappa^2+1)^2$ the scalars and $\xi$ cost $\poly(\kappa)\cdot k$ draws for abort probability $2^{-k}$, and for $((\kappa-1)^2+1)^2 < p < 4(\kappa^2+1)^2$ enumerating $\Fp$ finds all the $\alpha_j$ with $O(\kappa p) = O(\kappa^5)$ coset tests. For general composite $\kappa$ no polynomial bound on the finding cost is claimed; step~$1$ alone uses the sampler of Proposition~\ref{prop:app-s2-TA}(iii), with $O(q^{q+1}\log q)$ draws per round.

\begin{remark}[arity, scope and small primes]
\label{rem:app-s2-tower-scope}
The arity $(a+1)\prod_t((r_t-1)a+1)$ has degree $L+1$ in $a$, where $L$, the length of the chain, is at most the number of prime factors of $\kappa$ counted with multiplicity. Since every $r_t \ge 2$, the arity is quadratic only for $L = 1$, which is the two-level construction itself; for prime $\kappa$ the tower is the two-level construction. So the tower does not close the square gap of Remark~\ref{rem:two-level-threshold-size}. For composite $\kappa$ it is an alternative construction, with a polynomial threshold at a higher arity; as stated at the start of this subsection, it changes nothing in Schedule~2, $E_W(c)$ or Table~\ref{tab:main-regimes}.

Lemma~\ref{lem:app-s2-refine} also holds, with the same proof, for a \emph{union target}. Relax the cell condition to $\alpha_j + \beta_i \in \{0\}\cup\bigcup_{k\in K}Q^{(D)}_{k-i-j}$ for a set $K \ni 0$, keep $\alpha_0 + \beta_0 \in Q^{(D)}_0$, and ask the inputs only for one coefficient of class $0$. Then the output has its $D$-classes in $K$ and one coefficient of class $0$. A \emph{union chain} applies this with $D = \kappa$, rows $\mathbb{Z}_\kappa$ and target $K$, and then Lemma~\ref{lem:app-s2-refine} with $R = K$, at arity $(a+1)((\kappa-1)a+1)((|K|-1)a+1)$. Exhaustive searches (finite computations, AI-checked, pending human review; the witnesses were re-checked, and the failing steps re-decided, by separately written programs) give the primes $p \equiv 1 \pmod\kappa$ at which neither the two-level construction, nor a tower, nor a union chain with $|K| \in \{2,3\}$ was found: $\{5,13\}$ for $\kappa = 4$, $\{11\}$ for $\kappa = 5$, $\{7,13,19,31,43,67\}$ for $\kappa = 6$, $\{17,41,73,89,137,233\}$ for $\kappa = 8$ and $\{19,37,73,109,127,163,181,199,307,433\}$ for $\kappa = 9$. At every other prime $p \equiv 1 \pmod\kappa$ one of these constructions applies: above the proved thresholds by Propositions~\ref{prop:app-s2-TA} and~\ref{prop:app-s2-step-threshold}, and below them by complete searches with checked witnesses. All the listed primes lie in $E_2(\kappa)$: restricting the rows of a two-level contraction at $(p,\kappa)$ to $R$ gives an $\mathrm{RC}(\kappa;R)$ contraction, and at each listed prime some step with $D = \kappa$ fails.
\end{remark}
```

### 5.2 `main.tex`, Remark rem:two-level-threshold-size

Inserted directly after "Closing this square gap is open." and before "The rest of this remark", by exact-string replacement (count asserted 1):

```latex
For composite $\kappa$ it can be bypassed at a cost in arity (Appendix~\ref{app:s2-tower}; AI-checked, pending human review): refining the cosets one prime factor $q_1 \ge \dots \ge q_L$ of $\kappa$ at a time gives a solution of~\eqref{eq:sde-target} from $(a+1)\prod_{t=1}^{L}((q_t-1)a+1)$ arbitrary columns for every prime $p \equiv 1 \pmod\kappa$ with $p > \max(4\kappa^{q_1+1}, 4q_1^2\kappa^5)$ and, if $q_1 \ge 5$, $p > T_A(q_1)$; when $\kappa$ is a power of $2$, $p > ((\kappa-1)^2+1)^2$ suffices. This arity has degree $L+1 \ge 3$ in $a$, so the construction is an alternative with a polynomial threshold at higher arity: it does not lower the Schedule~2 arity, and it changes neither $E_2(\kappa)$ nor $E_W(c)$ nor Table~\ref{tab:main-regimes}.
```

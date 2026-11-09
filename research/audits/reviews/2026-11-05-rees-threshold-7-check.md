# Adversarial check of threshold-7 (flexible-line chains, union steps, barrier)

5 November 2026, overnight. AI-only pass by one Claude Code session; nobody was available for
questions. It is not a human review. **Every statement below is AI-checked, pending human
review.** No git command and no network were used. `make_numbers.py` was not run.
`research/reductions/rees_hsp_reduction.json`, `docs/outreach/` and every table and `numbers.tex`
were left alone.

Object: `2026-11-05-rees-threshold-7.md` and its code. Independent code:
`2026-11-05-rees-threshold-7-check/`, which shares no code with the threshold-6 or threshold-7
scripts. Interpreter `/opt/anaconda3/bin/python`. Everything ran under `nice -n 10`, with at most
two processes.

## 0. Verdict

**No Error.** Every proof was re-derived line by line, and every number I recomputed agrees
with the report. Two findings change what the paper may say:

- **I1. Union steps depend on the coset generator.** The exact κ = 7 set {29, 43, 71} holds
  only for one generator; read correctly, the result is stronger (§2).
- **G1. The small-κ thresholds rest on T_R.** The values Θ_2(5) = 3781 and Θ_2(7) = 30823 are
  set by T_R(κ, 3), a criterion the paper did not state (§2).

Both are fixed in the integrated text. The result is integrated as subsection `app:s2-chains`
(§5).

## 1. Proofs re-derived

- **Theorem 2.2 (nested triangular recursion) [proved; holds].**
  - Induction claim C(t). The chain condition gives i(b) ∈ R_t.
  - Column count: hockey stick, Σ_{j≤m} C(j+t, t) = C(m+t+1, t+1).
  - Class of the realisation weights: n + i(b) + (K − i(b) − n) = K.
  - The stop round has weight α_0 + β_0 = 1 on b*.
  - Back substitution keeps τ_k ∈ V_k.
  - Supports are disjoint, and the final value is −τ_0 ∈ U.
  - Corollary 2.3: C(a+L+1, L+1) = ∏(a+t)/t ≤ (a+1)^{L+1}. The numbers 286, 1331, 2541, 1001,
    14641, 316251 and 6.8·10^6 are right.
  - C(a+3, 3) < (a+1)((κ−1)a+1) exactly when a < 6κ − 11.
- **Lemma 3.2 and Theorem 3.1 (barrier) [proved; holds].**
  - (a) both directions, including the nonconstancy of β and the renormalisation by y ∈ Q_{i0+j0}.
  - (b) the line argument, with |Z_S| ≤ 1 + (p^r − 1)(κ−1)/κ.
  - Theorem 3.1:
    - 1 ≤ r ≤ κ−1, and S has rank r because the differences span V.
    - Pr[Λd^j = 0 ∀j] = p^{−rm} for independent d^j.
    - The union bounds give p^{r(κ−1+h)}θ_r^n, and κp^hθ_1^n for r = 1.
  - Corollary 3.3 and Lemma 3.4 (first moment) are correct. They are not used in the paper.
- **Proposition 4.1 (union step, second moment) [proved; holds].** Checked in this order:
  - E n_j = N_1 for j ≠ 0 and N_0 for j = 0.
  - The pair formula for E n_j².
  - The character expansion of [y ∈ A_ij], with coefficients ĉ_s ω^{(i+j)s}.
  - The four kinds of sum:
    - p − 2 when s = t = 0;
    - modulus 1 when exactly one of s, t is 0;
    - −1 when s + t ≡ 0 ≢ s;
    - at most √p otherwise, by Weil for X^s(X+c)^t.
  - |N − c_0²(p−2)| ≤ 2c_0G + G²√p.
  - c_0²(p−1)²/p − c_0²(p−2) = c_0²/p, so |δ| ≤ Δ.
  - Σ_{c≠0}δ(c) = 1 − p/|A| < 0.
  - The second-order remainder satisfies (1+Δ)^r − 1 − rΔ ≤ (rΔ)²e^{rΔ}/2.
  - Column 0 is bounded crudely by (1+Δ)^{r−1}.
  - Cauchy–Schwarz gives Pr[n = 0] ≤ ρ − 1, and the union bound over the D columns gives LHS.
  - Monotonicity of Δ, E_0 and E_U.
- **Lemma 4.2 (closed form) [proved; holds].**
  - 2/(0.99·4.05) = 0.498815, so the report's "≤ 0.4988" should read 0.4989.
  - Δ ≤ 1.0203H/(c_0²√p).
  - x ≤ 0.29957/√D ≤ 0.1498.
  - e^x − 1 ≤ 0.1619 (the report uses the looser 1.162x).
  - (D−1)x²e^x/2 ≤ 0.0522.
  - Total 0.713 < 0.73.
  - Interval bound G ≤ 1 + ln D.
  - H ≤ (1.2 + ln D)², since the difference is 0.14 + 0.2 ln D ≥ 0.
- **Theorem 4.3 and Corollary 4.4 [proved; hold].**
  - Step 2 is `prop:app-s2-step-threshold`(ii). Its proof allows any 0 ∈ R. The phrase
    "r ≤ D" is redundant (referee-13 S6), and I removed it.
  - Every inequality of Corollary 4.4 was re-derived. The check values are 14.87 < 16.32 at
    κ = 16 and 27.806 < 27.972 at κ = 19; the report's "16.3" and "27.97" are right.
  - Imprecision: the report writes "Θ_2(κ) = κ^{κ lnlnκ/lnκ + O(1)}". Only the upper bound is
    proved.
- **Lemma 4.5 [proved; holds].** A union step at modulus κ is a row-restriction of a two-level
  contraction, so it can fail only at p ∈ E_2(κ).
- **Propositions 4.6 and 4.7 and Lemma 4.8 [hold as stated].**
  - The projection Q^{(D')}_m ⊆ Q^{(κ)}_{m mod κ} needs ξ to generate F_p^×/P_{D'}.
  - For extension fields, N ≡ k (mod κ). When κ | k and κ ≥ 3, the index sets meet, so α is
    constant.
  - Lemma 4.8: the recurrence solution Cμ^d + c' and f = −(c + e^{−1})^{−1}.
  - Their "argued" conclusions stay argued. None of them enters the paper.

## 2. Findings

- **I1 (Imprecision, important for the κ = 7 statement). Union steps depend on ξ.**
  - Mechanism: if ξ' = ξ^u q, then ξ'^m P_D = Q^{(D)}_{um}. So RC_{ξ'}(D; R → K) is the same as
    RC_ξ(D; uR → uK). For K = {0} and R a subgroup this changes nothing, but for union targets it
    does.
  - With ξ the least primitive root (the generator of `rectu.c`), the chain
    Z_7 → {0,1,2} → {0,1} → {0} fails exactly at {29, 43, 71}, as the report says.
  - With ξ = g², g^5 it fails exactly at {29, 71}. Equivalently, for g the chain
    Z_7 → {0,2,4} → {0,2} → {0} covers 43.
  - So no four-step chain is needed for 43. The generator-free statement is: for every coset
    generator, some chain Z_7 → u{0,1,2} → u{0,1} → {0} with u ∈ Z_7^× works at every
    p ≡ 1 (mod 7) except 29 and 71.
  - At κ = 5, the chain {0,1,2} fails at {11,31,41,61} or at {11,41,61,71}, depending on u. The
    chain {0,1} fails only at 11, for every u.
  - The "no chain exists" lists do not depend on ξ, because the family of chains is closed under
    units.
  - Fix: the integrated remark states the generator-free form and the two least-primitive-root
    sets.
- **G1 (Gap in the proposed LaTeX, overlapping referee-13 G1). The small-κ thresholds rest on
  T_R.**
  - Θ_2(5) = 3781 and Θ_2(7) = 30823 are not set by the new Proposition 4.1: step 1 needs only
    T_U = 800 and 15133. They are set by T_R(κ, 3), the second-moment criterion of threshold-6
    Prop. 3.2, which the paper never stated.
  - Fix: the integrated remark defines T_R(D, r) as the inequality ρ < D/(D−1) of the proof of
    `prop:app-s2-step-threshold`(ii), before p is bounded. It shows the left side is decreasing,
    and marks the values as numerical evaluations of a proved criterion.
  - The same definition now covers referee-13 G1 (κ = 9, with T_R(9,3) ≈ 1.347·10^5).
- **I2. The name Θ_2 was used for two different things in §7.1.** In the corollary it named the
  closed form; in the remark, the bisected thresholds. They are now Θ^cf_2(κ, k) and Θ_2(κ).
- **I3. Small fixes to the proposed LaTeX.**
  - M was undefined in the theorem.
  - "0.2266" should read ≤ 0.23. The integrated proof gives 0.1619 + 0.0522.
  - `i` was used both as the imaginary unit and as a row index; it is now ω_D.
  - The proposition is now stated for D | κ, since Q^{(D)} is defined only there.
  - The barrier statement in the remark now says that its proof is in the cited reports and is
    not reproduced, and that its reading as a statement about schemes is argued.
  - The clause "at small m such sets do contain lines" (report §5.3, not re-run here) was
    dropped.
- **I4. rem:app-s2-tower-scope had no κ = 7 entry** (referee-13 I11). My search (`twostep7.py`)
  over every K ∋ 0 with |K| ∈ {2, 3, 4}, at all 56 primes of E_2(7), gives exactly
  {29, 43, 71, 113}. Off E_2(7) the two-level construction applies, so this entry is complete.
  - It replaces threshold-6's step-1 witness check, which was never completed
    (`v_u7_step1A.out` empty).
  - The task asked for {29, 71} in that remark. That would contradict the remark's definition
    (two-level, tower, or union chains with |K| ∈ {2, 3}). So {29, 43, 71, 113} goes there, and
    the reduction to {29, 71} is stated in `rem:app-s2-chains-scope`, with a forward pointer.

## 3. Independent computations (`2026-11-05-rees-threshold-7-check/`)

| file | what | result |
|---|---|---|
| `rcdfs.c`, `rc.py` | complete bitset DFS for RC(D; R → K): zeros and repeated β allowed, no symmetry breaking; pow-based witness checker | — |
| `sanity_e2.out` | E_2(4) < 120, E_2(5) < 200, E_2(7) < 400 | {5,13,17,29,37,53}, the 9 primes, {29,…,379}: agree with the paper |
| `e2six.out` | E_2(6) below 3000 | 53 primes, max 859: agrees |
| `chains.out` | the chains of report §4.4 at E_2(5) and E_2(7), for every unit u | report sets reproduced for u = 1; generator dependence (I1); 2733 FEASIBLE verdicts pow-checked, 135 INFEASIBLE; off-E_2 spot check p < 1200 all feasible |
| `twostep7.out` | κ = 7, two-step chains, all K with \|K\| ≤ 4 | fail exactly at {29, 43, 71, 113} |
| `reach_e2.out` | reachability over all chains at every prime of E_2(κ), κ = 4, 5, 6, 7 (124 primes) | no chain exactly at {5,13}, {11}, {7,13,19,31,43}, {29,71}; all 124 primes decided (a chain exists at the other 114) |
| `reach_89.out` | κ = 8 at {17,41,73,89,137,233}; κ = 9 at the 10 listed primes | no chain at {17,41,73} and {19,37,73}; chains found at the others, with D_1 ∈ {2,4} for κ = 8 and D_1 = 3 for κ = 9 |
| `thresholds_*.out` | own T_U, W, T_R and bisection | see below |
| `momcheck.out` | Prop. 4.1: brute force over all β (p = 31, 41, 29), then exact ρ_j at p just above T_U | moment formula exact; max\|δ\| ≤ Δ, ρ_j ≤ bounds and Σ(ρ_j − 1) ≤ LHS at D = 5 (p = 811), D = 7 (p = 15149) and D = 7 middle step (p = 8849); a uniform β succeeds in 99.5–100% of trials |
| `chain_solver.out` | own implementation of Theorem 2.2, end to end; 336 runs | all OK (details below) |
| `solver_negctl.out` | corrupted contractions | 58 of 60 invalid ones caught within 5 runs |
| `barrier_check.out` | Lemma 3.2(b) brute force at κ = 4, p = 17 and 37 (r = 1); m_0 values | max\|Z_α\| = 9 ≤ 13 and 28 = 28, every Z_α misses a class; m_0 = 118, 146, 187, 368, 5398, 5450, as reported |

`chain_solver.out` covers these chains, each with a ≤ 4 and 8 column families: random, all-zero,
repeated, unit vectors, hyperplane, rank one, sparse and mixed. Every output was checked with
pow(): each weight is a κ-th power, the relation is nonzero, at most C(a+L+1, L+1) columns are
used, and Σ s_b^d λ_b = 0 for a d with gcd(d, p−1) = κ.

- κ = 5, Z_5 → {0,1,2} → {0}, at p = 3821, 3851 and 3881, just above Θ_2 = 3781. Pairs come
  from a random β.
- κ = 7, the same chain at p = 30829 and 30871, just above 30823.
- At E_2 primes, with pairs from the DFS:
  - κ = 5, p = 31 (L = 2) and p = 181 (L = 3);
  - κ = 7, p = 113 (L = 3);
  - κ = 7, p = 43, both the u = 2 three-step chain and the report's four-step chain;
  - κ = 6, p = 67, the mixed chain 2 | 6;
  - κ = 4, p = 17.

Thresholds (`thresholds_table.out`, `thresholds_parts.out`): Θ_2 and Θ_3 for κ = 4–19, 23, 31
and 47 reproduce report §4.3 to every printed digit.

- κ = 5: 3781 (k = 3), Θ_3 = 1217 at (3, 2).
- κ = 7: 30823, Θ_3 = 15133.
- κ = 11: 1.158·10^6, 3.799·10^5.
- κ = 13: 7.421·10^6, 1.055·10^6.
- Binding steps: T_R(5,3) = 3780.8 and T_R(7,3) = 30823.1. At κ = 13, T_R(13,5) = 7.42·10^6.
- Θ_2 < κ^{κ/2} exactly for κ ≥ 13. Θ_3 < κ^{κ/2} for κ ≥ 11.
- Closed form (`thresholds_closed.out`): LHS(P) < 0.73 and T_U ≤ P for 4 ≤ D ≤ 40, all
  intervals and r ∈ {2, k, D/2, D}. The maximum LHS(P) is 0.491.
- Asymptotics (`thresholds_asym.out`): the five-term bound is at most 4.05κ²(ln κ)^κ for every
  16 ≤ κ ≤ 400, and that bound is below κ^{κ/2} for 19 ≤ κ ≤ 400. The bisected Θ_2(κ, k) lies
  below the closed form at κ = 16, 32, 64, 128 and 256.

## 4. What it means for the paper

- **A new Schedule-2-type option, not a Schedule 2 change.**
  - For every κ ≥ 4, and in particular for prime κ, where the tower is empty, the union chain
    gives cubic arity C(a+3, 3) at a proved threshold of order κ^{κ lnlnκ/lnκ + O(1)}. This is
    far below T_A(κ) and 16κ^{2κ+2}.
  - The arity is cubic, so it does not lower the Schedule 2 arity. C(a+3,3) is below
    (a+1)((κ−1)a+1) only when a < 6κ − 11.
  - For κ = 5 and 7, E_2 is known exactly, so the new content is coverage of E_2 primes at
    cubic or quartic arity. The proved thresholds matter only for κ ≥ 11, where E_2 is unknown.
    Since c ≤ 9 in the paper's tables, that is outside them.
- **E_W(c), `tab:main-regimes`, other tables, `numbers.tex`: unchanged.** The combined rule does
  not use the chains, just as it does not use the tower.
- **Owner decision (not done).** Suppose the combined rule adopted chains with their proved
  guards.
  - Prime κ_d ∈ {5, 7} with guard Θ_2: E_W(c) would not change for c ≤ 9. Every maximising prime
    (3, 7, 13, 61, 421, 2521) lies below Θ_2(5) = 3781.
  - Composite κ_d = 4, through the union chain (guard Θ_2(4) = 395) or the tower (guard 100):
    e_4 would drop from 12 to 3 at p = 421 and 2521. Then E_W(7), E_W(8) and E_W(9) would
    change, and so would the equality case of `lem:tb-count-exponent`.
  - This would change `tab:main-regimes`'s black-box exponent and the E_W values. It is the
    owner's decision; I changed nothing.

## 5. Integration done

### `appendix-schedule2.tex`

- **New subsection `app:s2-chains`**, after `rem:app-s2-tower-scope` and before `app:s2-scope`.
  It is the report's §7.1, corrected as in §2, and contains:
  - the definition of RC(D; R → K), with the generator remark;
  - the definition of a chain;
  - `thm:app-s2-chain`, with full proof;
  - `prop:app-s2-union-step`, with (i) Ψ_U and T_U and (ii) the closed form, and full proof;
  - `cor:app-s2-union-chain`, with Θ^cf_2 and full proof;
  - `rem:app-s2-chains-scope`: T_R defined, Θ_2 and Θ_3 values, small-prime results, and the
    barrier.
  - Status line: proved / computed / finite computation / argued, with "AI-checked, pending
    human review".
- **Referee-13 items for this file:**
  - E1 at the status line, the corollary title and the scope sentence;
  - S1: r_i → θ_i, and 2^u3^v → 2^i3^j;
  - S6: "and r ≤ D" removed;
  - G1 and I11: the κ = 7 entry {29, 43, 71, 113} added, the E_2-only search explained, the
    κ = 9 range tied to the computed T_R(9,3) of the new remark, and a pointer to the shorter
    lists.

### `main.tex` `rem:two-level-threshold-size`

One sentence was added after the integrator's E1 sentence, read again just before the edit,
together with its no-change clause.

### Build and test

- The build ran in `$TMPDIR/rees-build-t7check`, with exit 0 and 164 pages.
- It has 0 Overfull boxes, no undefined references or citations, and no "Float too large".
- `tests/tools/test_rees_paper_numbers.py` passed (2 tests).

### Log

Row I209 was added to the integration log.

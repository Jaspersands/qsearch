# Rees headline, follow-up: proved class-9 exponent 21 → 20 (2026-11-13, late evening)

This is AI-only work (one Claude Code subagent), pending human review. No paper file, `numbers.tex`,
STATE, handoff or reductions file was edited, and `fragment.tex` is unchanged. There were no Git
commands, no network and no API calls. Every run used `nice -n 19` with one heavy process at a time;
the largest RSS was 680 MB. New material is in
`2026-11-13-rees-headline-below-38/fragment-v2.tex` and `2026-11-13-rees-headline-below-38/v2/`.

Labels: PROVED, PROVED given cited theorems, CONDITIONAL, REFUTED, UNKNOWN, NOT computed. Finite
checks can only falsify.

## 0. Verdict

**The proved class-9 headline is E_{++}(9) = 20.**
- Status: PROVED given cited theorems + exact finite computation, AI-checked, pending referee.
- The cited theorems are the same imports as Schedule 1H⁺: Weil's two-variable diagonal bound and
  Rabin root finding.
- The full vector for c = 2..9 is **3, 5, 9, 10, 14, 16, 18, 20**. Schedule 1H⁺ gave 3, 5, 9, 10, 14,
  16, 19, 21.
- **Attainers of 20 (class 9):** every prime p ≡ 1 (mod 2520), and below 2·10⁶ exactly these plus
  **37, 43, 73, 127, 181, 631** (266 primes below 2·10⁶; `v2/rule_v2.out`). Nothing exceeds 20.
- c = 8: the value 18 is attained below 2·10⁶ only at 29 and 43. The tail value is 17.
- It uses none of Lemmas S/F/HC of the 11-12 note, the R5 inputs, IS Lemma 12, the chain corollary
  via thm:app-s2-chain, or Lemma P.

**Two new ingredients. Both are load-bearing; without either one the maximum is 21 (§3).**
1. **TL6 at κ = 6.** This is the two-level contraction RC(6; Z_6 → {0}), giving degree 2.
   - It is fragment.tex's own Corollary chain + Lemma SM at (D, r, k) = (6, 6, 1).
   - T_exist = 837384 and T_samp = 40924516. The threshold was re-checked with exact rationals.
   - Certificates exist at 33258 of the 33311 primes p ≡ 1 (mod 6) below 837384, including all 114
     primes ≡ 1 (mod 2520). The other 53 primes are ≤ 859.
   - **This is the grade that drops in the 2520 class.** κ_6 goes 3 → 2, so the grade vector at
     p ≡ 1 (mod 2520) is now 2,2,2,2,2,3,3,3.
2. **ℓ-level {0}-contractions.** These are Lemmas T_ℓ and W_ℓ of the k9-below-21 note, rewritten as
   fragment-v2 Lemmas ell-tensor and ell-node.
   - They are used only through five verified finite tables, with no composition lemma:
     (9,19), (9,37), (9,73) at ℓ = 4, giving degree 4; and (4,13), (6,13) at ℓ = 3, giving degree 3.
   - Effect: E(13), E(19), E(37), E(73) go 21 → 18, 19, 20, 20.

## 1. Which grade had to drop for p ≡ 1 (mod 2520), and whether a proved route exists

Under 1H⁺, p ≡ 1 (mod 2520) has e_d = 2,2,2,2,3,3,3,3 for d = 2..9. The binding grades are
κ = 6, 7, 8, 9, each at 3.
- The three-level step does not help here: an ℓ-level node has degree ℓ ≥ 3.
- A degree-2 node is needed, and the cheapest is the two-level contraction at κ = 6. Lemma SM
  needs it only below T_exist(6) = 837384. The alternatives need 8.9·10⁶ (κ = 7), 1.5·10⁸ (κ = 8)
  and 3.3·10⁹ (κ = 9) (`thresholds.out`).
- The certificate search (`v2/run_tl6_all.py`; random β plus complete DFS for p ≤ 12000) took
  474 s, with RSS 680 MB.
- Checks:
  - every witness passed `certs.check_rc` and the separately written membership test of
    `verify_all.py`: 33258/33258 accepted (`v2/verify_tl6_all.out`);
  - end-to-end chain runs at 2521, 7561, 12601, 100801, 1009 and 837379: 216/216 (`v2/exec_tl6.out`);
  - a perturbed certificate failed 3/6 runs.
- **Tail, p > 2·10⁶ (PROVED).** e = 1,2,2,2,2,2,3,3,3 for κ = 1..9.
  - For d ∈ {2,4,6}, κ_d is even, so the grade is 2. For d ∈ {3,5} it is 2 or 1. For d ∈ {7,8,9} it
    is 3 iff κ_d = d.
  - So Σ ≤ 19, with equality iff 2520 | p−1, and E = 20 there.
  - Lower bounds at κ = 7, 8, 9 within the candidate set, as in lem:chain-exponent: κ = 7 is S1 (7)
    or a plan over U7 (≥ 3); κ = 8 is S1 (≥ 8) or a plan over H⁺⁺_4 (≥ 3); κ = 9 is S1 or the
    tower (3).
- Band preprocessing, 837384 ≤ p < 40924516 (the F5 form of the referee). One trial costs ≤ 36p
  class tests and succeeds with probability ≥ 1−Φ(837409) > 1.6·10⁻⁵ (`v2/tl6_threshold.out`).
  That is a constant.

## 2. The ℓ-level nodes (fragment-v2 §"Multi-level contractions")

- **Lemma ell-tensor (T_ℓ).** PROVED, AI-checked. I re-derived it line by line.
  - The one non-mechanical step is the claim that the dependence on off-zero cells kills every cell.
    It follows by induction on the number of zero coordinates, using z_0 = 1.
  - The arity is M_ℓ(a) = Π_t((κ−1)^t a + 1) ≤ κ^{ℓ(ℓ−1)/2}(a+1)^ℓ.
- **Lemma ell-node (W_ℓ).** PROVED. Σ x_b λ_b = Σ_y C_y T_y = 0 coordinatewise, and x_{b*} = C_0 ∈ P.
  It gives a {0}-node at modulus κ, which is a κ-solver after roots, of degree ℓ.
- **Condition (iii) is decidable.** It says that C contracted on every axis with
  x ↦ (x_m − z_m x_0)_{m≠0} vanishes, because the axis-relation space is W^{⊗ℓ}.
- **Tables (finite).** They were found by SAT in the k9-below-21 folder (read-only). I re-verified
  them with a third program, `v2/verify_ell.py`, which uses axis-by-axis contraction and
  power-character classes. All 5 VERIFIED (`v2/verify_ell.out`).
  - Negative controls:
    - perturbed tables FAIL (3/3);
    - read as class-1 tables, all FAIL (5/5);
    - with a different generator g′, 3 FAIL. 2 pass, at 73 (g′ = 11) and at 13, κ = 4 (g′ = 6). This
      is expected: there g′ = g^u with u ≡ 1 (mod κ), so the classes are identical. I checked that
      log_5 11 ≡ 1 (mod 9) and 2⁵ ≡ 6 (mod 13).
- **Independent executor.** `v2/ell_exec.py` runs Lemmas T_ℓ and W_ℓ written from the statements.
  - Dependences are random elements of the null space. In uniform runs, sub-objects with zero
    off-zero part are discarded, so the table is exercised.
  - Results: every run is ok (§5 item 4, `v2/ell_exec.out`).
- **Why the tables feed nothing else.** 6 and 9 are proper divisors of no κ ≤ 9, and at 13 the grade
  κ = 8 does not occur. So adjusting grades after the fact in `v2/rule_v2.py` is exact; this is
  asserted in the code.

## 3. Exact computation (`v2/rule_v2.py`, imports `rule.py` read-only)

The regression with the new candidates off reproduces core Schedule 1H below 26244, with 0
disagreements. Each run takes 32 s.

| variant | E(c), c = 2..9 | class-9 attainers |
|---|---|---|
| 1H⁺ (refereed) | 3,5,9,10,14,16,19,21 | 13,19,37,73 + 2520-class |
| **1H⁺⁺ = 1H⁺ + TL6 + ℓ-tables** | **3,5,9,10,14,16,18,20** | 37,43,73,127,181,631 + 2520-class |
| without TL6 (`rule_v2_noTL6.out`) | …,18,**21** | 2520-class at 21 |
| without ℓ-tables (`rule_v2_noELL.out`) | …,19,**21** | 13,19,37,73 at 21 |

Grade vectors e_d (d = 2..9) at the attainers of 20:

| p | e_d | where they come from |
|---|---|---|
| 37 | 2,2,3,1,3,1,3,4 | κ = 9 is L4 |
| 73 | 2,2,2,1,3,1,4,4 | κ = 9 is L4; κ = 8 is a Tier B stage over the {0,4} chain |
| 43 | 2,2,2,1,4,4,2,2 | κ = 6, 7 are Tier B stages |
| 127 | 2,2,2,1,3,3,2,4 | |
| 181 | 2,2,2,3,3,1,2,4 | |
| 631 | 2,2,2,2,3,3,2,3 | 631 has no TL6 witness (complete DFS: none) |
| p ≡ 1 (2520) | 2,2,2,2,2,3,3,3 | |

The other primes: 13 has 2,2,3,1,3,1,3,2 (E = 18) and 19 has 2,2,2,1,4,1,2,4 (E = 19).

**Comparison with the conditional R9 (20).** R9 reaches 20 at 37, 43, 73, 127, 181, 433, 631, 673,
1009, 2017, 2521 and 7561. The proved 1H⁺⁺ also has 20 and gives ≤ 20 at each of these primes. At
433, 673, 1009 and 2017 the proved value is 19, lower than R9's 20 (`v2/r9_attainers.out`). So the proved value now equals the
conditional R9 value, using only proved ingredients plus the Tier B tables that were already refereed.

## 4. Below 20 (fragment-v2 rem:below-20). NOT attempted; UNKNOWN

Getting below 20 would need all of the following:
- At p ≡ 1 (mod 2520): a degree-2 node at κ = 7, 8 or 9, for example TL7, with certificates for
  about 1100 primes in that class below 8.9·10⁶ plus Lemma SM above. This looks feasible.
- At 37, 43, 73, 127, 181 and 631: each needs its own drop.
  - At 37, the k9 helper's 3-level LRAT UNSAT (not rerun) makes κ = 9 = 4 optimal within ℓ-level
    contractions and chains.
  - The κ = 4 and 6 grades at 37 sit at primes with no two-level contraction.

So 19 is not cheaply reachable.

## 5. Adversarial self-check

1. **Is TL6 really already proved?**
   - In fragment.tex, candidate (c) TL is restricted to κ ∈ {3,4,5}, but the proof (Corollary chain
     with D' = 1 and Lemma SM) never uses κ ≤ 5.
   - The κ = 6 threshold row was not in tab:sm-thresholds. I recomputed it with exact rationals, but
     no referee has reproduced it yet.
   - The κ = 6 solver for the tail is the TL6 chain with the least primitive root ξ = g below 2·10⁶,
     and any ξ above T_exist (Lemma SM holds for every coset generator). F4 of the referee applies
     unchanged.
2. **Attainment claim at 2520-class.**
   - This needs lower bounds within the candidate set, not for all algorithms. I give them in §1.
     They are statements about Schedule 1H⁺⁺, not optimality claims.
   - The 21 → 20 drop is an upper-bound statement, and it does not depend on them.
3. **Tables come from another agent's SAT runs.** I did not rerun the SAT. Correctness rests only on
   the finite table check, done here by a third program, and on Lemma W_ℓ. A wrong composition
   history would not matter.
4. **Executor strength.** The first executor version exercised few cells, because of lucky sub-objects
   and sparse null vectors at a = 1. I added forced mode and random null-space elements.
   - At p = 13, a = 3: 62–64 of 64 cells (κ = 4) and 214–216 of 216 cells (κ = 6) were active, with
     all runs ok.
   - At κ = 9, a = 1 (about 0.7M columns per run): 6221–6487 of 6561 cells were active, and all runs
     at 19, 37 and 73 were ok (2/2 each, uniform; 2/2 each, degenerate). a ≥ 2 at ℓ = 4 was not run
     (≥ 6.7M columns). The run took 490 s with RSS 367 MB.
   - Negative controls:
     - perturbed B4_37: 0/2 ok;
     - perturbed B3_13_6: 0/3 ok at a = 2;
     - perturbed B3_13_4: **1/3 ok at a = 2**, because that run had only 8 active cells. At a = 3 both
       perturbed 13-tables give 0/5 ok, with 62–64 and 215–216 active cells.
   - So the executor's sensitivity depends on how many cells are active.
   - The executor is a falsifier only; the proof is Lemma W_ℓ plus the exact table check.
5. **Anchoring.** The coordinator suggested the three-level step for large p. I found that it cannot
   help in the 2520 class, since degree ≥ 3 is no better than the current 3. The binding fix is TL6,
   which is inside the already refereed framework.
6. **The 53 primes without TL6 witnesses (≤ 859)** are not claimed to lack contractions. At p ≤ 12000
   a "dfs:none" from the read-only rcdfs.c is a search result, not a proof here. That is harmless: the
   rule simply does not use TL6 there.
7. **The c = 8 value 18** is attained at 29 and 43 below 2·10⁶. Its tail is 17. The tail values for
   c = 6, 7, 8 dropped by 1 because of TL6.

Next command, for a referee:

    nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-headline-below-38/v2/rule_v2.py

Expected output: `E_new(c) = {…, 8: 18, 9: 20}`. Then rerun `verify_ell.py` and `verify_tl6_all.py`.

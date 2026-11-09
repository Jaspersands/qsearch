# Rees diagonal SDE, Q1 adversarial search: no counterexample to Conjecture 5, but the deterministic Q1 dichotomy is false

**Status: COMPLETE, AI-only computational pass, not human-reviewed.** 5 November 2026, one Claude
Code session, about 55 minutes of wall time with at most 2 processes running under `nice -n 10`.
- **Labels.** [computed] means exact and exhaustive for the stated object. [sampled] means exact
  arithmetic on random or structured samples.
- **Scope.** Finite runs can only falsify. Nothing here says Conjecture 5 is true.
- **Files.** Code and outputs are in `2026-11-05-rees-sde-q1-search/`. The algorithm under test
  is imported unchanged from `2026-11-05-rees-sde-worst-case/sss.py`, and no file there was
  modified. Only this file and that folder were written: no `.tex`, no git, no STATE, no
  handoff, no gate JSON.

## 0. Verdict

1. **No counterexample to Conjecture 5 was found.** `sss_full`, which runs (R1)–(R5) with 3
   column orders, solved every bank tried at the budget M = ⌊(a+2)²/4⌋ + a:
   - 4,050 banks in 14 structured families, κ ∈ {2,3}, p ∈ {1009, 10007, 10009}, a = 3..10;
   - 30 hand-built critical-stall banks;
   - every bank of the hyperplane, paired, nested and simulated-annealing runs.

   Every returned witness was verified by `check`.
2. **The deterministic form of Q1 is false [computed].** The families `chain4` (κ = 2, 3) and
   `chainfull` (κ = 3) are explicit, solvable banks at the budget. On the identity order they
   produce *exactly* the critical case of the worst-case report §6: q = 1, |B∖U_L| = 1, no
   unused column.
   - Neither branch of Q1 holds. (i) fails: for a ≤ 6 an exhaustive search over all flats finds
     no proper flat Y holding ≥ D_3(dim Y) + dim Y columns, and for larger a the hyperplane
     U_L holds fewer than D_3(r−1) + r − 1 columns. (ii) fails: the finishing pass (R4) returns
     `stall2`.
   - So one iteration of (R1)–(R4) **fails on these banks for a ∈ {5, 7, 8, 9, 10}** (`chain4`,
     both κ) and **a = 5..10** (`chainfull`, κ = 3). This was checked at p = 1009 and at
     p ∈ {10007, 10009}.
   - The failing bank is solved only because (R5) restarts with a random order.
   - So **any proof of Conjecture 5 must use the random restarts**, or a new repair. A dichotomy
     that holds for every column order cannot be true.
3. **Restarts rescue every bank tried [sampled].** Across all families the failure rate of one
   (R1)–(R4) iteration on a *random* order is at most 2.3% per order:
   - the worst bank is `chain4` at κ = 2, a = 5, with 7/300 failing orders;
   - the rate does not grow with a: in the `chain` rows of `hyper_scan`, 0/300 at a = 9 for both κ;
   - the simulated annealing that maximised this rate found no bank with a failing random order
     among 40.
4. **True-pool loss π [computed on the constructions].**
   - `chain4` reaches the critical stall with **π = D_3(a) − 2a + 2**, which is quadratic: π/M
     = 0.24 at a = 5 and 0.39 at a = 10, and tends to 1.
   - `chainfull` reaches it with **π = 2**, the minimum that Theorem 2(b) allows at q = 1.
   - So a large π is not needed to defeat the deterministic algorithm, and a small π is not
     sufficient for it to succeed.

## 1. Code

| file | content |
|---|---|
| `indep.py` | **Independent solvability checker, written from scratch with numpy; it does not import `sss.py`.** It tests exactly every circuit support, scans all p+1 kernel directions for supports with 2-dimensional kernel, samples 2-planes for larger kernels, and verifies the witness. Self-test against brute force over (P∪{0})^M: 600/600 agree (p ∈ {7, 13}, κ ∈ {2, 3}). |
| `q1lib.py` | Imports the algorithm. `theorem_forward` is the Theorem-2 forward pass with π, q, unused count and \|B∖U_L\|. `one_order` is one iteration of the `sss_full` loop on a given order, returning the stall certificate. Also the bank generators and SA mutations: replace a column, scale by a non-residue, project into the span of 1..a−1 columns, put on another column's line, swap positions, move into a plane. |
| `critical.py` | The `chain4` and `chainfull` constructions (§2). |
| `sweep.py` | Structured-family sweep: identity-order Theorem-2 pass, K one-iteration runs on random orders, and `sss_full` with forwards = 3 when the identity order fails. Failures are checked by `indep.py`. |
| `chain_certs.py` → `banks/*.json`, `out/chain_certs.out` | Critical banks with certificate, independent witness, dense-flat check (exhaustive for a ≤ 6), 100 random orders and `sss_full`. |
| `cert_check.py` → `out/cert_check.out` | Independent check of every certificate without `sss.py`: B is a basis, dim U_L = r−1, \|B∖U_L\| = 1, the columns are partitioned, no unused column, pool ⊆ span(B∩U_L), each round is a circuit mod U_{l−1}, and the column count in U_L is below the threshold. **ALL PASS.** |
| `sa.py`, `sa2.py`, `run_sa2.sh` → `out/sa2_*.{out,json}` | Annealing. `sa.py` is a prototype with an identity-order objective. `sa2.py` maximises the random-order failure rate (score 10·fail + 3·critical + stall + π/4), seeded from `chain4`, `chainfull`, codim-1 and flag families. |
| `hyper_scan.py`, `nested.py`, `order_diag.py` | Hyperplane-dense, paired and nested-flag banks under random orders; diagnosis of the failing random orders. |

## 2. The critical-stall constructions

**chain4(a)** [computed]. Here r = a.
- The first r columns are a basis b_1..b_r, so B = {b_1..b_r}.
- **Rounds.** Round l (l = 1..⌊(r−1)/2⌋) is a 4-circuit c_k, c_l, c_i, c_new with
  δ = (d_k, d_l, d_i, 1):
  - cls d_i = 0 and cls d_k = cls d_l = 1;
  - c_i and c_new lie in span(b_{2l−1}, b_{2l}).
- **Why U_l is forced.** The class-0 pair is the largest class group (ties go to class 0), so
  `split_blocks` cuts it into two singletons *for every random cut*. Hence
  U_l = U_{l−1} + span(b_{2l−1}, b_{2l}) deterministically.
- **Even r.** A last gain-1 round, a pair congruent modulo U inside span(U, b_{r−1}), reaches
  dim r − 1.
- **Pool.** The remaining columns are generic in span(b_1..b_{r−1}) = U_L, and each is a
  true-pool event.
- **Result.** At M = D_3(r) + r this gives π = D_3(r) − 2r + 2, q = 1, B∖U_L = {b_r}, no unused
  column, no swaps.
- **Column count.** U_L holds D_3(r) columns (a = 7: 20; a = 9: 30), below the (R3) threshold
  D_3(r−1) + r − 1 for every r ≥ 5.
- **Small and even cases.** At a = 3, 4, 6, U_L reaches the threshold and (R3) solves the bank.

**chainfull(a)**, κ = 3 [computed]. Each round is a **full** circuit mod U of q+1 columns, with all
three classes present, so the blocks are the class groups and nothing is split. The group sums are
fixed to b_{2l−1}, b_{2l} and −(b_{2l−1} + b_{2l}). This gives the greedy worst-case cost
D_3(r) − 2 for the rounds, so **π = 2** at the budget. U_L holds only r + 3 to r + 5 columns
(8 at a = 5, 15 at a = 10).

**Two explicit banks**, p = 1009, a = 5, M = 17. Full certificates are in
`banks/chain4_k2_p1009_a5.json` and `banks/chainfull_k3_p1009_a5.json`.

`chain4`, κ = 2:
- Columns:
  `[[943,797,165,541,29],[359,796,726,248,452],[1005,880,510,218,651],[934,352,922,819,398],[471,217,331,808,925],[660,935,411,690,884],[483,746,187,144,459],[375,107,568,518,53],[702,859,25,261,380],[880,229,31,257,21],[857,291,454,665,215],[43,386,199,78,692],[189,508,19,695,936],[665,843,326,559,830],[792,579,486,753,504],[156,219,68,23,155],[826,829,174,318,161]]`
- Certificate: B = {0..4}, B∖U_L = {4}, rounds {5,6,7,8} and {9,10,11,12}, pool {13,14,15,16}
  (π = 4), unused ∅.
- 12 columns lie in U_L, below the threshold of 13.
- Exhaustive over 1,891 proper flats: none is dense. No collinear triple.
- The identity order gives `stall(pool=4,codim=1)/stall2`.
- Solvable: the independent witness has support {0, 1, 8}.
- 2/100 random orders fail. `sss_full` succeeds on its second order.

`chainfull`, κ = 3:
- Columns:
  `[[855,283,557,359,756],[626,899,956,293,216],[300,347,384,973,564],[430,981,261,619,754],[166,1,397,539,77],[267,263,897,928,538],[876,368,514,173,203],[651,967,119,740,764],[601,602,873,811,662],[960,400,690,293,82],[314,659,124,805,369],[852,259,243,261,956],[950,32,999,734,868],[604,810,290,139,895],[993,271,787,166,318],[60,586,155,335,884],[327,114,434,625,496]]`
- Certificate: rounds {5..10} (6 columns) and {11..14} (4 columns), pool {15, 16} (π = 2),
  B∖U_L = {4}.
- 8 columns lie in U_L, against a threshold of 13.
- Exhaustive over 1,514 flats: none is dense.
- The identity order gives `stall(pool=2,codim=1)/stall2`.
- Solvable: the independent witness has support {0, 1, 9, 10}.
- 0/100 random orders fail.

**Independent solvability check.** Every critical bank has an `indep.py` witness, and each was
verified. For `chainfull` κ = 3, a = 10 the default search missed; a rerun with 40,000 samples
found a witness of support 13, recorded in the JSON. Every bank at the budget with κ = 2, and with
κ = 3 for a ≥ 4, is also solvable by Chevalley–Warning.

## 3. Runs

All runs are at the budget unless stated. "Solved" means `sss_full` with forwards = 3.

| family / run | κ | p | a | M | banks | solved | id-order stalls | id-order failures of (R1)–(R4) | random-order failures | max π |
|---|---|---|---|---|---|---|---|---|---|---|
| sweep, 12 non-chain families† | 2 | 1009, 10007 | 3–10, 3–9 | budget | 1800 | 1800 | 290 (codim1_2: 141; 1 critical) | 0 | 0/9000 | 12 (flag_sub, a = 10) |
| sweep, 12 non-chain families† | 3 | 1009, 10009 | 3–10, 3–9 | budget | 1800 | 1800 | 310 (codim1_2: 147) | 0 | 1/9000 (flag_sub, p = 10009, a = 6) | 12 (flag_sub) |
| sweep, `chain4` | 2, 3 | all four | 3–10 | budget | 300 | 300 | 300 (all critical) | 180 (a ∈ {5,7,8,9,10}) | 3/1500 | 18 (a = 10) |
| sweep, `chainfull` | 3 | 1009, 10009 | 3–10 | budget | 150 | 150 | 150 (all critical) | 110 (a ≥ 5) | 0/750 | 2 |
| `chain_certs` (§2), 100 random orders each | 2, 3 | all four | 3–10 | budget | 30 | 30 | 30 | 24 | 5/3000 | 18 |
| `order_diag`, `chain4` κ = 2, a = 5 | 2 | 1009 | 5 | 17 | 1 | 1 | – | – | 7/300 | 4 |
| `hyper_scan` gen: H generic with M−t columns, t = 2..a+3 outside | 2 | 1009 | 5–7 | budget | 96 | – | up to 99% (t = 2) | – | 0/2400 | – |
| `hyper_scan` paired: outside columns μw + h with μ ∈ P, t ∈ {3,5,6,7} | 2 | 1009 | 5–8 | budget | 64 | – | up to 23% critical (t = 3) | – | 4/1600 | – |
| `hyper_scan` paired | 3 | 1009 | 5–8 | budget | 64 | – | up to 32% critical (t = 3) | – | 2/1600 | – |
| `hyper_scan` chain | 2, 3 | 1009 | 5–9 | budget | 32 | – | – | – | 5/2400 | – |
| `nested` paired flags, t = (5,2), (5,6), (5,5), (5,5,5), (3,2), (5,2,2) | 3 | 1009 | 8 | 33 | 24 | 24 | up to 43% | – | 0/600 | – |
| SA (`sa2`), 6 runs, 1,200 mutations × 6–8 random orders | 2, 3 | 1009 | 5–7 | budget | ≈1200 | – | – | – | best bank 0/40 | 4 |
| **lower budgets** (`sweep --M=2a`) | 2, 3 | 1009 | 3–7 | 2a+1..budget | 2736 | 2397 | – | – | – | – |

† The 12 non-chain families are: random, lines (a, a+1 lines), pairs, planes with ≤ 5 points,
3-flats with ≤ 8 points, lines+planes, subthreshold nested flag, codim-1 with 2 or 3 outside
(plus a variant with one outside column first) and basis-dense.
- A "random-order failure" is one (R1)–(R4) iteration failing on a fresh random order. Such a
  failure does not make `sss_full` fail; that would need three failing orders in a row.

**Lower budgets [sampled].** Six families (random, lines_{a+1}, codim1_2, flag_sub, planes5,
chain4), 6 banks each per M, for M = 2a+1..budget.
- 339 `sss_full` failures, all at **M ≤ M_3(a)**, where M_3(a) = (cost of the full-circuit
  rounds) + 1 = 7, 9, 13, 16, 21 for a = 3..7.
- **None for M > M_3(a)**, which is about a below the budget.
- Every failing bank has an independent verified witness, so these are failures of the algorithm
  on solvable banks, below the budget, as expected.
- Statuses: `stall2` 247, `nosources` 90 (a stall with π = 0), and 2 others.
- Details: `out/lowM_rows.jsonl` and `out/lowM_failures.jsonl`.

**Maximum π/M per (κ, p, a)** (`out/summary_tables.txt`).

| a | M | max π / M (chain4) | max π, other families | identity order fails (R1)–(R4)? |
|---|---|---|---|---|
| 3 | 9 | 3/9 (codim1_2, κ = 2 p = 1009), else 2/9 | 2–3 | no (R3 rescues) |
| 4 | 13 | 3/13 | 2 | no |
| 5 | 17 | 4/17 = 0.24 | 3–4 | yes (κ = 2, 3; all four primes) |
| 6 | 22 | 6/22 | 3–4 | κ = 3 `chainfull` yes; `chain4` no |
| 7 | 27 | 8/27 = 0.30 | 4–5 | yes |
| 8 | 33 | 11/33 | 6 | yes |
| 9 | 39 | 14/39 = 0.36 | 9 | yes |
| 10 | 46 | 18/46 = 0.39 (p = 1009 only) | 12 | yes |

The values are identical for p = 1009 and p ≈ 10⁴, and for κ = 2 and 3, since the constructions do
not depend on p.

## 4. The strongest adversarial family and π scaling

**Strongest family: `chain4`** for a deterministic failure with large π, and **`chainfull`** for
one with minimal π.
- On the identity order, π_chain4 = D_3(a) − 2a + 2, which is **quadratic** (≈ a²/4), while the
  stall still escapes (R3), because U_L holds D_3(a) < D_3(a−1) + a − 1 columns.
- `flag_sub` (nested subthreshold flags) also grows faster than linearly: π = 4, 6, 9, 12 at
  a = 7..10. It never stalls, though.
- **Under random orders** the largest π observed was 4 (chain4, a = 5; SA). The failing random
  orders had π ∈ {2, 4} with full rounds [6, 4]: these are critical stalls created by the random
  block cut (`out/diag_chain4_k2_p1009_a5_diag.json`). The same order refailed in 0–2 of 5 reruns
  with fresh coins.

**Heuristic, not a claim.** Under a random order, true-pool events appear in quantity only when
some flat Y is dense enough to fill and then overflow, which roughly means Y is above its (R3)
threshold.
- In the paired-hyperplane scans this shows directly. With N_H ≥ D_3(r−1) + r − 1 (t = 3),
  critical stalls happen on up to 32% of orders, and every one is rescued by (R3).
- Just below the threshold (t ≥ ⌊(r+2)/2⌋ + 2) the critical-stall rate falls to about 1%.
- The constructions defeat (R3) only by putting the pool columns *last*, which a random order
  undoes.

This suggests a randomised version of Q1 rather than the deterministic one.

## 5. Claim gates (must stay false)

- "Conjecture 5 is proved", or "the arity ⌊(a+2)²/4⌋ + a is proved for arbitrary banks". Nothing
  here proves it.
- "(R1)–(R4) without restarts solve every bank at the budget." This is **refuted [computed]**
  (§2).
- "Q1 holds for every order", that is, every stall at the budget satisfies (i) or (ii). This is
  **refuted [computed]** (§2).
- "π ≤ O(a) at a critical stall". This is **refuted**: `chain4` has π = D_3(a) − 2a + 2.
- "Restarts succeed with probability ≥ 1 − O(1/a) per order." This is unproved; it is only
  sampled (§3).

## 6. Next hard question and next command

**Q1′ (randomised).** For every bank of D_3(r) + r columns of rank r, does one (R1)–(R4)
iteration on a uniformly random order succeed with probability ≥ c > 0? The data suggest
≥ 0.97. A possible route:
- show that a critical stall on a random order forces a flat above its (R3) threshold;
- or bound the probability that every pool column is scanned after the round that completes
  span(B∩U).

`chainfull` (π = 2, U_L nearly empty, order-fragile) is the natural test case for the theory
agent.

**Next command.**
```
cd research/audits/reviews/2026-11-05-rees-sde-q1-search && nice -n 10 /opt/anaconda3/bin/python -B hyper_scan.py 3 1009 11 6 100 9,10,11,12 paired 7,9,11
```
Then do the same with `chain` in place of `paired`.
- **Expected artifact:** per-order failure rates at a = 9..12, for κ = 3 at p = 1009.
- **Acceptance test:** a family whose random-order failure rate increases with a (falsifying
  Q1′'s spirit), or a rate that stays ≤ 3% (supporting it). In either case every failure is saved
  with an `indep.py` witness and a certificate that passes `cert_check.py`.

# Attack on Theorem A of `2026-11-08-rees-sde-p3-nest.md` (WNEST, m = n²/4 + O(n^{3/2}) worst case): no break found; recursion near-tight, closed form loose, four code/proof discrepancies

AI-only adversarial pass, 8 November 2026, one Claude Code session; not human-reviewed. Target:
Theorem A of `2026-11-08-rees-sde-p3-nest.md` (deterministic WNEST solves every F_3^n subset-sum
instance with m ≥ n²/4 + (8/9)(n+2)^{3/2} + 4n + 2√n + 15 columns) and its code `…-nest/wnest.py`.
Context read: `2026-11-08-rees-sde-p3.md`, `2026-11-08-rees-sde-p3-referee.md`, `research/STATE.md`
("Now"), `research/TRAPS.md`. Scripts and outputs are in `2026-11-08-rees-sde-p3-nest-break/`,
interpreter `/opt/anaconda3/bin/python -B` (cvc5 via `/opt/anaconda3/envs/qsearch-cas/bin/python`).
Only this file and that folder were written; no git, no network, `make_numbers.py` not run.

Labels: **[exact]** finite computation, script named; **[sampled]** exact arithmetic on random or
climbed instances; **[argued]**; **[read]** proof step checked by hand. Finite checks falsify only.

## 0. Verdict

1. **Not broken.** No instance at or above the bound on which WNEST fails, no run-time violation
   of any invariant the proof uses, no per-piece cost above what the proof charges. Totals: 656
   structured/random instances at m = ⌈closed form⌉ (n = 4..100, 16 families, both variants),
   ≈ 48 000 instance evaluations in annealing climbs (n = 6..30), ≈ 300 000 pool evaluations in
   pool climbs (q = 4..30) and adaptive stage climbs (n ≤ 40), ≈ 3.0 M exhaustive lemma instances
   plus 300 k sampled, 37 climbed worst pools re-run through `wnest.py` itself. Zero assertion
   failures; every witness re-summed to zero over the original vectors [exact/sampled].
2. **Every proof step re-read and found correct [read]:** Lemma P (series-class rank drop is
   exactly a−1), Lemma M (Var = (2/9)Σa_j²), Lemma D (conditional expectations, Φ exact), Lemma G
   (eight union identities, non-empty union in the dependent case), the Δ = |F| − 1.5·rank
   invariant, the window r*+2 ≤ wt ≤ 2N/3 + (2/3)√N, dim D(X) ≥ 2, the pool/return accounting,
   Lemma 1 unwinding with 0/1 realizers that are disjoint subsets of the pieces, and the analytic
   sums. The two real-arithmetic inequalities behind N(q) and the cost cap were also proved with
   cvc5 (QF_NRA, negations UNSAT) [exact, `nq_cvc5.out`].
3. **The recursion is nearly tight, the stated bound is not.** Adversarial pools push the per-piece
   cost to cap−1…cap−3 at every q tried (q = 30: 39 against the cap 42 and against q+2 = 32), and a
   stage-adaptive adversary reaches m_needed = 0.88–0.91 · guarantee(n) at n = 8..40
   (n = 40: 567 of 621). So the deterministic WNEST's n^{3/2} term is real in the worst case, as
   the note says. The closed form, however, exceeds the exact recursion by ≥ 35 columns at every
   n (min 35.06 at n = 4) and is **above KOW's recursion value for all n < 146 and above n²/3 for
   all n < 206** [exact, `bounds_check.out`]; the note's "below KOW for n ≥ 35" is true of
   `guarantee(n)`, not of the bound Theorem A states.
4. **Code/proof discrepancies (none affects the theorem):** §3 below. The material one: `wnest.py`
   runs WNEST at q = 3 (`qmin_kow=3`) while the text and `guarantee()` use KOW for q ≤ 3, so for
   odd n the code's own worst-case recursion is `guarantee(n) + 2`.

## 1. What was attacked and how

**Strict re-implementation** `strict_wnest.py` [exact]. Written from the proof text, not from
`wnest.py`; exact integers throughout (27·Φ ∈ ℤ, N(q) and the window premise checked as integer
inequalities). Invariants asserted on every stage: I0 pool columns nonzero in the quotient; I1
coloop deletion drops rank by exactly the number of coloops; I2 **Lemma P with equality** (class of
size a drops rank by exactly a−1); I3 Δ never decreases, Δ(F*) ≥ N − 1.5q; I4 after peeling no
coloop, classes ≤ 2, D(F*) ≠ 0; I5 Lemma M: Φ(∅) = (2/9)Σa² = brute-force variance over all 3^k
codewords (k ≤ 11) and ≤ 4N*/9; I6 Lemma D: Φ(prefix) is the mean of the three Φ(prefix,v), the
chosen branch never increases Φ, Φ(full) = (wt − 2N*/3)² ≤ Var, δ ≠ 0; I7 r*+2 ≤ wt ≤
⌊2N/3 + (2/3)√N⌋; I8 dim D(X) ≥ 2, δ′ independent, supp δ = X; I9 the eight gadget identities in
the quotient, realizers 0/1 subsets of X, U_(1,2) = X; I10 ⟨h₁,h₂⟩ has dim 2 or a nonempty union
is zero-sum; I11 m_needed = max over stages (consumed + pool) ≤ guarantee(n) ≤ closed form; I12
witness nonempty, distinct indices, sums to zero over the original vectors. Variant `proof`
follows the text (WNEST for q ≥ 4, KOW pool q+1); variant `code` mirrors `wnest.py`.
Cross-check against `wnest.py` on 60 instances (n = 4..61, four families): identical columns
pulled and identical 2-dim piece sequences in all 60; 13 "divergences" are bookkeeping only
(`wnest.py` logs a KOW cost tuple for a round that terminates; one witness differs by KOW
tie-breaking, both verified) [exact, `crosscheck_wnest.out`].

**Lemma-level exhaustive checks** [exact, `lemma_exhaustive.out`, `lemma_exhaustive2.out`].
- Lemma G: all 54 presence patterns of the six classes P_ab with δ′ independent of δ: for every
  α ≠ 0, U_α or U_{2α} nonempty; 2000 random numeric identity checks. 0 failures.
- Lemma M + D over **all** generator matrices k×N (bases, no coloop): (k,N) = (1,≤7), (2,≤6),
  (3,4): 703 644 bases, 0 failures; max (wt−μ)²/Var = 0.900 (k = 2, N = 3 and N = 6), i.e. the
  greedy can land at 0.95σ in tiny codes, never above 1σ.
- Lemma M + D over **all kernel-form bases** [C | I_k] (the form `kernel()` produces; complete up to
  column order within blocks): 1 361 050 bases completed when this note was written (every (k, r)
  with kr ≤ 12 for k ≤ 4; k = 5, r ≤ 2; k = 6, r = 1), 0 failures, max ratio 0.900. The cases
  (k, r) = (6, 2) and (7, 1) were still running; the `.out` file shows whatever finished since.
- Lemma P + coloop drop over **all** column multisets of F_3^q: q = 2, N ≤ 8 (all) and q = 3,
  N ≤ 6: 919 060 multisets, 0 failures; sampled 199 931 matrices q = 4..7 with forced duplicates
  and chains (series classes up to 8): 0 failures.
- Lemma P over canonical [I_r | A] for r(N−r) ≤ 12 (complete up to GL and column order): this
  block follows the M+D block in `lemma_exhaustive2.py` and had not started when this note was
  written; the file reports each (r, N) as it completes. It is not used above.
- Sampled Lemma M + D on 100 000 random codes k ≤ 8, N ≤ 24 with forced series pairs: 0
  failures; max ratio 0.9; the window premise (2N − 3r − 6)² ≥ 4N held in a subset and wt ≥ r+2
  in every one of them.

**Structured families** [sampled, `families_proof_small.out`, `families_proof_large.out`,
`families_code.out`]: random; dual-distance-exactly-3 pools (all projective points of PG(4,3)
embedded in sliding windows, signed: every weight-3 dependency forced); extended ternary Golay
columns and codewords; every column duplicated (classes of size exactly 2, Var = 4N*/9
attained); duplicated with negation; chains e_i − e_{i+1} of length 5 and n/2 (series classes
peeled every round, largest peeled 22); rank n/3; growing rank; two complementary subspaces;
weight-1/2 columns; all e_i + e_j (triangles); blocks a, b, −(a+b); 2n vectors cycled; +v,+v,−v
blocks; adversarial pool order (basis then (v, 2v) pairs). m = ⌈closed form⌉ exactly, so an
exhausted stream would refute the theorem. n ∈ {4,…,10, 12, 16, 20, 25, 30, 40} × 2 repetitions
(proof variant), n ∈ {60, 80, 100} (proof), n ≤ 40 (code variant): 656 runs, 0 failures. Worst
m_needed/guarantee = 0.884 (two_subspaces, n = 40: 549/621); random n = 100: 2967 needed,
3242 guaranteed, 3851 closed form; max |X| − q = 13 at n = 100.

**Climbs** [sampled, `climb_pool.out`, `climb_inst.out`, `adaptive.out`, `adaptive_long.out`].
- Pool annealing, q ∈ {4,…,8,10,12,14,16,20,24,30}, N = N(q), three objectives (cost wt;
  z = (wt−μ)/σ; number of peeling steps) × three starts (random, pairs, chain), 1200–3000 steps
  each, 108 runs: climbed max cost = cap − 1 at q = 5, 6, 7 and cap − 2…3 elsewhere (table at the
  end of `climb_pool.out`); max z = 0.707; peel climbs produced up to 12 peeling steps with
  seven size-3 classes (the Δ-equality case) and still satisfied every assert.
- Instance annealing, n ∈ {6, 8, 10, 12, 16, 20, 30}, three starts, 400–1500 steps (≈ 48 000
  evaluations): best m_needed = 26, 40, 56, 74, 116, 168, 333 against guarantee 30, 46, 64, 85,
  133, 191, 378.
- Stage-adaptive adversary (climbs only the fresh columns of each pool, 400 and 3000 steps per
  stage): n = 8: 38/46, 12: 74/85, 16: 118/133, 20: 170/191, 24: 233/259, 40: 567/621; every
  piece at cap−2 or cap−3; at n = 30 the run ended early by a pool column falling into the
  realized subgroup (step 0), as the proof allows.

## 2. Reproducibility of the strongest adversarial instances

No failing instance exists to report. The strongest pools (per-piece cost cap−1) are saved as
`best_pool_q{q}_{objective}_{start}_{seed}.npy` (q × N(q) matrices; e.g.
`best_pool_q7_wt_random_7134.npy`: wt 13, cap 14, N* = 18, r* = 7); the `wt` ones were re-run
through `wnest.py` with its asserts
(`crosscheck_wnest.out`). Any assertion during the climbs would have been saved as `FAIL_*.npy`;
none was.

## 3. Code / proof discrepancies in `…-nest/wnest.py` and the note

1. **WNEST threshold.** Text (§2, Theorem A, `guarantee()`): WNEST for q ≥ 4, KOW rounds for q ≤ 3.
   Code: `Run.run(qmin_kow=3)` runs WNEST at q = 3 (pool N(3) = 11, cost ≤ 9, then q = 1). For odd
   n the code's exact worst-case recursion is therefore `guarantee(n) + 2` (11 + 1 against
   4 + 3 + 2 + 1 on the last stages), so `wnest.py`'s `guarantee()` does not describe `wnest.py`'s
   own run; the closed form still holds for the code variant (min slack 35.06, n = 4..2999, both
   variants, `bounds_check.out`). Cap at q = 3: 9 ≤ q + (8/3)√q + 4 = 11.6, and N(3) = 11 ≤ 4q.
2. **KOW pool size.** Text: pool q + 1 for q ≤ 3. Code: `kow_round` uses q + ⌈log₃(q+1)⌉ (= 5 at
   q = 3). Unreachable in `wnest` mode because of (1) (q ≤ 2 gives q + 1 either way), but a reader
   who sets `qmin_kow=4` would get pool 5 at q = 3 and a recursion `guarantee(n) + 1` for odd n.
3. **Mislabelled comparison.** §3 says the hill climb at n = 8..14 stayed below "the guaranteed 63,
   84, 109, 135"; those are `bound(n)` (the crude reporting formula, labelled "formula" in
   `adversarial.out`), not `guarantee(n)` = 46, 64, 85, 109. The conclusion is unchanged (40, 55,
   75, 95 are below both), but the cited slack is overstated by ≈ 20 columns.
4. **"Below KOW for n ≥ 35" vs the stated bound.** §0 item 1 compares the exact recursion with
   KOW's; the bound in the theorem statement is the closed form, which is above KOW's recursion for
   n < 146 and above n²/3 for n < 206 (`bounds_check.out`). Theorem A's statement is correct but
   weaker than KOW's for all n < 146; the headline "constant 1/4" is about the recursion and the
   leading term.
5. Minor, unreachable: `peel` returns an empty basis when F becomes independent and
   `pick_codeword` would then raise a ValueError rather than an assertion (excluded by Δ > 0);
   `second_moment` uses floats with a 1e-12 tie tolerance (all values are multiples of 1/27, so
   the choices are exact; the integer version reproduces them on all 60 cross-checked runs).

## 4. What would break it, and what this pass did not do

A break needs one of: a code D with no coloop, classes ≤ 2 and a basis on which the greedy of
Lemma D ends outside one standard deviation (exhaustive up to k·N = 18 and kernel-form k·r ≤ 12
say no; the mean-of-three identity is asserted on every step of every run); a series class whose
deletion drops the rank by less than a−1 (exhaustive q ≤ 3, N ≤ 6 and 200 k sampled say no); or a
pool with Δ(F*) < Δ(F) (never observed, including 12-step peels with seven size-3 classes). No
such object was found, and the proofs of Lemmas P, M, D, G read correctly. Not done: a SAT/SMT
encoding of the greedy or of F_3 rank (cvc5 here has no finite-field theory); exhaustive search
over whole instances (3^{nm}); n > 100 runs; any novelty or priority check, which Theorem A still
needs before external use (the note's own gate).

## 5. Files

| file | what | result |
|---|---|---|
| `strict_wnest.py` | independent strict-mode WNEST (12 invariant groups, exact integers, two variants) | used by everything below |
| `lemma_exhaustive.py` → `.out` | Lemma G patterns; Lemma M+D over all bases (k,N) ≤ (3,4)/(2,6)/(1,7); 100 k sampled codes; Lemma P over all multisets q = 2 (N ≤ 8), q = 3 (N ≤ 6); 200 k sampled | 0 failures; max (wt−μ)²/Var = 0.9 |
| `lemma_exhaustive2.py` → `.out` | Lemma M+D over kernel-form bases [C \| I_k], kr ≤ 12; Lemma P over [I_r \| A], r(N−r) ≤ 12 | 0 failures in all completed cases |
| `nq_cvc5.py` → `.out` | cvc5 QF_NRA: N(q) ≤ 1.5q + 2√q + 6 and cost cap ≤ q + (8/3)√q + 4 | both negations UNSAT |
| `bounds_check.py` → `.out` | exact recursion vs closed form, both variants, 4 ≤ n < 3000; caps; crossovers with KOW | min slack 35.06; code variant = proof + 2 for odd n; closed form < KOW only for n ≥ 146 |
| `attack_families.py` → `families_*.out` | 16 families, n ≤ 100, m = ⌈closed form⌉, strict asserts | 656 runs, 0 failures |
| `attack_climb.py` → `climb_pool.out`, `climb_inst.out`, `best_pool_*.npy` | annealing on pools (cost, z, peeling) and on instances | cap−1 reached; z ≤ 0.707; m_needed ≤ 0.88·guarantee |
| `adaptive_adversary.py` → `adaptive.out`, `adaptive_long.out` | stage-adaptive adversary, n ≤ 40 | 0.88–0.91·guarantee; 0 failures |
| `crosscheck_wnest.py` → `.out` | `wnest.py` vs strict solver on 60 instances; 37 climbed pools through `wnest.py` | identical pulls and pieces; 0 asserts |

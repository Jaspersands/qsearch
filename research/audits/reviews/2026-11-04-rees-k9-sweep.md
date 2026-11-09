# κ = 9 sweep of (20000, 9^9/2] = (20000, 193710244] (2026-11-04)

AI-run computation (Claude Code subagent), pending human review. Local only: no git, no
network, no `.tex` edits; `research/reductions/rees_hsp_reduction.json` untouched. Code and
outputs: `2026-11-04-rees-k9-sweep/`. This is the κ = 9 analogue of
`2026-11-04-rees-t1-sweep-hi.md` (κ = 8) and Theorem 5.1 of `2026-11-04-rees-threshold-5.md`.

**Status when this note was written (2026-11-05 ~00:00 AEDT): the sweep is still running.**
The verified numbers below are a snapshot; §6 gives the command that re-derives them.
**Update 2026-11-05: the sweep has finished and the full verification has run; see
"Result (2026-11-05)" before §7. Sections 1–6 are kept as written.**

The range holds **1,791,117** primes p ≡ 1 (mod 9) (numpy sieve, cross-checked with
`sympy.primepi`): 2624 in (20000, 200000], 35352 in (200000, 3200000] and 1,753,141 in
(3200000, 193710244].

## 1. Family choice

First-moment counts (`../2026-11-04-rees-threshold-5/families.py`, log10 μ):

| p | G (full) | P (tying, κ zero cells) | T1 (strict) |
|---|---|---|---|
| 20000 | −7.5 | −2.4 | −6.6 |
| 59049 = 9^5 | 0.0 | 0.9 | −2.9 |
| 134600 | 5.7 | 3.4 | 0.0 |
| 3.2·10^6 | 27.7 | 13.0 | 11.0 |
| 1.94·10^8 | 56.1 | 25.5 | 25.2 |

- **T1** (transpose-symmetric, λ = 1; κ unknowns γ_j, conditions γ_j + γ_k ∈ Q_{b−(j+k)} for all
  j, k, so 45 conditions) gives **strict** witnesses. It is the main sweep family. Its
  crossing is p ≈ 1.35·10^5. The data show T1 is mostly empty up to about 3.5·10^5: in
  c01, 588 of 687 primes in (2·10^5, 2.5·10^5] had no T1 witness at the sweep budget, and
  only 6 of the ≈ 30,000 primes in (6·10^5, 3.2·10^6] had none (the largest is 681337).
- **P** (transpose, λ = −1, b ∈ {1..8}): M_ij = α_j − α_{i+b}. Since κ = 9 is odd,
  p − 1 = 9h forces h even, so −1 ∈ Q_0 for every p (Prop. 2.5 of threshold-5, "always if κ
  odd"). P has exponent (κ+1)/2, ties G and crosses at 43880. **But every P witness has 9
  zero cells** (j = i + b). It is a two-level contraction in the sense of E_2 (cell (0,0) =
  α_0 − α_b ≠ 0), so it shows p ∉ E_2(9). It does not show the strict count N > 0.
  P is therefore used **only as a fallback** after T1, and every P witness is counted as
  non-strict by both verifiers.
- H does not exist for odd κ. Shift families with o = 3 have exponent 26/5 > 5 and were not
  needed.

## 2. Code: `famsym9.c` and why it is sound

`famsym_direct.c` (κ = 8 sweep) is generic in K. Its arrays are sized 64, it accepts
2 ≤ K ≤ 60, and nothing hard-codes K = 8. It is copied unchanged and runs correctly at K = 9:
for 13 primes at 1.937·10^8 with win=24576, all lines were FOUND and valid. It is too slow
for κ = 9, though. The level-0 lists need W ≈ 2·10^4 before the 28 pairwise conditions
leave solutions in the window (expected solutions W^8/9^28), and every coset test is a
plain `powm`. Measured cost: 2–17 s/prime at W = 3072 to 6144, and 0.11–0.12 s at
W = 16384 to 24576 after change (5).

`famsym9.c` is `famsym_direct.c` plus four changes. The DFS, restart loop, γ_0 choice,
output normalisation and the final strict K² `check()` (plain `powm`) are unchanged.

5. **Montgomery batched coset test.** inQ(y, m) is still "y ≠ 0 and y^h = ζ^m". y^h is
   computed in Montgomery form (R = 2^32, p < 2^31), 8 independent tests at a time.
   Montgomery form is a bijection, so this is the same predicate. Every loop visits the
   same elements in the same order and appends hits in the same order, and the window
   break happens at the same element. So the lists, the rng stream and the whole search
   are unchanged. The speed-up is 2.5–3×.
6. **`fam=P`**: the P family above (K odd only). It fixes α_0 = 0 by translation and
   α_1 = g^{(b−1) mod 9} by Q_0-scaling, then runs the same MRV DFS with differences
   instead of sums. With `complete` it tries all b = 1..8 and decides whether P is empty.
   Output: β_i = −α_{i+b}, translated to β_0 = 0 and scaled by (α_0 − α_b)^{−1} ∈ Q_0.
   Each witness is re-checked by `checkP()`: every nonzero cell is in the right coset,
   cell (0,0) is nonzero, and the zero cells are counted (`zeros=9` in the line).
7. **`ints=N`** (T1 only, needs 4N < p): a different sub-search of T1. The γ_j are
   restricted to residues of integers with |n| ≤ N. γ_0 is a random integer and b is set
   to ind(2γ_0), which is allowed because b ranges over Z_9. ind(n) for 0 < |n| ≤ 2N < p/2
   comes from a per-prime table: ind(q) for every prime q ≤ 2N by exponentiation,
   additivity over a smallest-prime-factor sieve, and ind(−1) by exponentiation. Sums of two
   list entries are integers with |n| ≤ 2N, so the residue determines n and the table
   lookup *is* the predicate y ∈ Q_m. The level-0 lists are {v ∈ [−N, N] : v + γ_0 ∈
   Q_{b−k}, 2v ∈ Q_{b−2k}}. The DFS and strict `check()` are unchanged. NOTFOUND means
   only "not found". The cost is π(2N) exponentiations plus O(N) lookups per prime instead
   of 72·W exponentiations. N = 8·10^5 gives 0.030 s/prime at 1.937·10^8 (all tries = 1)
   and 0.041 s/prime in c02.
8. **`tab`**: famsym.c's full index table (one byte per residue), so inQ is a table lookup.
   Same predicate. It is used for p ≤ 2·10^7, where O(p) is cheap. With `tab` and
   neither `win=` nor `ints=`, the T1 search *is* famsym.c's.

**Soundness does not depend on any program.** Every FOUND line is re-derived from the
definition by two independent Python verifiers (§5). Equivalence (5), (8) and the window
logic are also checked line-for-line (§3).

## 3. Cross-checks (`crosscheck/`; the `secs=` field dropped)

| run | primes | result |
|---|---|---|
| κ = 9 exact, old `famsym` vs `famsym9` vs `famsym_direct`, (100001, 125000], budget 2000×5, seed 1 | 356 | **identical** (1 FOUND, 355 NOTFOUND) |
| κ = 9 exact, old `famsym` vs `famsym9`, (300001, 304867], 200000×50, seed 1 | 74 | **identical** (72 FOUND, 2 NOTFOUND) |
| κ = 9 exact, prefixes of the stopped (20001, 60000] runs vs old `famsym` | 41 / 27 | identical (`famsym9` / `famsym_direct`) |
| κ = 9 `tab` vs old `famsym`, both ranges above | 356 + 74 | **identical** |
| κ = 9 windowed W = 16384, `famsym9` vs `famsym_direct`, (5000001, 5050000], seed 3 | 542 | **identical**, all FOUND |
| κ = 9 W = 24576, `famsym9` vs `famsym_direct`, [193700000, 193702000] | 13 | identical, all FOUND |
| κ = 8 exact, `famsym9` vs the κ = 8 report's old `famsym` output, (49418, 200000], seed 1 | 3220 | **identical** (3219 FOUND, NOTFOUND 55889) |
| κ = 8 W = 3072, `famsym9` vs `famsym_direct`, [8300000, 8388608], seed 11 | 1366 | **identical** |
| `ints=N` at [193700000, 193702000], N = 1.31·10^5 … 2·10^6 | 13 each | all FOUND for N ≥ 2.6·10^5 (`calib/top9_i*.out`) |

`ints=` has no exact counterpart. Its witnesses are checked only by the verifiers, which is
the soundness argument for all modes anyway.

**Timings** (CPU s/prime, nice 10; the machine was oversubscribed by other sessions'
jobs, so each process got ≈ 55–60 % of a core):

| mode | p ≈ 3.2–10·10^6 | p ≈ 1.937·10^8 |
|---|---|---|
| `famsym_direct` W = 3072 / 6144 | | 2–17 / 0.8–29 |
| `famsym9` W = 16384 / 24576 | 0.135 (5·10^6) | 0.110 / 0.125 |
| `famsym9 ints=8e5` (used for c02–c25) | **0.041** (c02, max 0.48) | **0.030** |
| `famsym9 tab` 20000×20 (used for c01) | 0.17 mean (most of the time is spent on the T1-empty primes below 6·10^5) | |

## 4. Chunks, screens, pipeline

`chunks.txt`: c00 = (20000, 200000] (by hand, `low/`), c01 = (200000, 3200000] (`tab`), and
c02–c25 = 24 chunks of ≈ 73,048 primes each over (3200000, 193710244] (`ints=800000`).
Workers claim chunks in file order with a mkdir lock, so the finished range grows from the
bottom. Per chunk: the main pass (`famsym9 9 lo+1 hi 200000 50 (1000+i) ints=800000`, or
`20000 20 … tab` for c01), then `retry.sh` on its NOTFOUND primes, then the marker
`out/done_cNN`.

`retry.sh` (final version):
- p ≤ 2·10^7: (1) T1 tab 20000×5; (2) P tab random 20000×20; (3) P tab complete under a
  15 s cap.
- p > 2·10^7: (1) T1 ints=8e5 1e6×20; (2) T1 ints=1.2e6; (3) P win=24576.

A prime without a witness after the chain is written as `UNRESOLVED`. The exhaustive T1
search and `famsearch full` are too slow at p ≈ 2–4·10^5: T1 takes ~45 s, and famsearch
took 18 s per restart already at 59797. So they were taken out of the chain.

| screen | role | started |
|---|---|---|
| `k9sweep_0` | worker 0: c01, then further chunks, then dfs2b queue | 2026-11-04 22:36 AEDT |
| `k9sweep_1` | worker 1: c02, c03, … | 22:36 |
| `k9sweep_2` | `low/finish_low.sh` (closes c00), then worker 2: c04, … | 23:26 |

All three run at nice 10, with at most 3 of our compute processes at once. The two
calibration-time pauses were done by SIGSTOP. The 8 foreign `dfs2b` jobs were never touched.
After the chunks, workers run `dfs2b 9 p p 4000000000 print` on `dfs2b_queue.txt` (the
20 smallest candidates), writing `out/dfs2b_P.out`. The log ends with `WORKER_DONE`.

**c00 (20000, 200000], by hand** (`low/`):
- T1 random (old famsym 200000×50) on (20000, 60000]: 17 found.
- T1 complete (old famsym, all b) on (20000, 76231] (stopped there): 26 strict witnesses;
  all others COMPLETE_EMPTY.
- P random (`famsym9 fam=P tab` 20000×20) on all 2624 primes: 1369 found.
- P complete on the witness-less primes up to 99577: 839 primes, all COMPLETE_EMPTY, so P
  random had missed none of them.

Result: **1382 primes certified (26 strict, 1356 non-strict P) and 1242 candidates**
(`low/candidates.txt`). Per 20000-band: 270, 219, 183, 172, 118, 96, 73, 67, 44.

**Projection.** An ints chunk takes 42–51 min of wall time under the present load: c03
took 42 min, and c04 took 51 min including a 6 min pause. c01's retry took 39 min. At
00:26, c05–c07 were running and c08–c25 (18 chunks) were left. That is ≈ 6.5 rounds of
≈ 47 min on 3 workers, so the chunks should finish at about **05:30–06:30 AEDT on
2026-11-05** (≈ 7–8 h wall in total). The dfs2b queue comes after that. Each
dfs2b run near 2·10^4 takes 1–2 h (an INFEASIBLE at 17929 took 4000 s), so the queue needs
≈ 10–15 h more on 3 workers. A test of dfs2b at 199909 gave no verdict in 5.5 min, which is
why the queue is the smallest candidates.

## 5. Verifiers

- `verify_k9.py`: a new file adapted from `verify_hi.py`; it shares no code with the C
  programs. It uses Python ints, `gmpy2.is_prime` + `sympy.isprime`, and a numpy sieve
  cross-checked against `sympy.primepi`. For each FOUND/FEASIBLE line it checks: p prime,
  p ≡ 1 (mod 9), ζ = g^h of exact order 9, and all 81 cells. A line is STRICT when every
  cell is nonzero and in Q_{−(i+j)}. It is NON-STRICT when zeros occur, but not at (0,0),
  and every nonzero cell is right. It reads dfs2b INFEASIBLE lines and NOTFOUND/UNRESOLVED
  lines. It reports X, the largest bound such that every prime of (20000, X] has a valid
  witness or is a listed exception (no witness, but a line shows it was processed), and it
  stops at any BAD line or witness/INFEASIBLE conflict.
- `../2026-11-04-rees-threshold-5/verify_witnesses.py --zeros --cover 9 20001 X` is the
  older, separately written checker. It is also run without `--zeros`, where the strict
  mode must reject exactly the P lines.

## 6. Results so far (snapshot) and the claim

**Chunk log** (all main passes rc = 0, with a `DONE` line):

| chunk | range | primes | main pass | retry | unresolved |
|---|---|---|---|---|---|
| c00 | (20000, 200000] | 2624 | by hand, see §4 | | 1242 candidates |
| c01 | (200000, 3200000] | 35352 | 22:36–23:44, 33243 T1 found, 2109 NOTFOUND | to 00:23: 236 T1, 1742 P | **131** (all hit the P-complete cap; the largest is 424549) |
| c02 | (3200000, 10060381] | 73048 | 22:36–23:26, all T1 | – | 0 |
| c03 | (10060381, 17260543] | 73047 | 23:26–00:08, all T1 | – | 0 |
| c04 | (17260543, 24656473] | 73048 | 23:26–00:18, all T1 | – | 0 |
| c05–c07 | | | running since 00:08, 00:18 and 00:23 | | |

So far, every prime above 681337 has had a strict T1 witness on its first try in the main
pass.

**Snapshot 2026-11-05 00:23 AEDT** (`snapshot_verify.sh`; output
`snapshots/snap_20261105_002333.out`). It covers c00–c04 and the prefix of c05 up to
26863219, which has no NOTFOUND.

- `verify_k9.py`: 278,701 primes in (20000, 26863219]. 277,328 have a valid witness:
  274,230 strict and 3,098 non-strict (P) only. **Bad lines: 0**, unparsed 0, no conflicts.
  dup = 21; these are c00 primes with both a T1 and a P line, all valid. Exceptions: 1373.
  Its last line reads "CONTIGUOUS: every prime p=1 mod 9 in (20000,26863219] has a valid
  witness or is one of the 1373 listed exceptions".
- `verify_witnesses.py --zeros --cover 9 20001 26863219` (the old checker): 277,358
  witness lines, 277,328 valid distinct, **bad = 0** (strict 274,230, zero cells only
  3,098), cover: primes = 278,701, missing = 1373.
- The 1373 missing primes of the old checker are the OPEN list of `verify_k9.py` and equal
  `exceptions_20000_26863219.txt` (checked by script). That file is the 1242 primes of
  `low/candidates.txt` plus the 131 UNRESOLVED primes of `out/r_c01.out`. Per 50000-band
  from 0: 384, 460, 244, 154, 86, 28, 9, 6, 2. The smallest is 20071, the largest 424549.

**dfs2b verdicts: none yet.** The 20 smallest candidates (20071, 20089, 20107, 20143,
20161, 20269, 20287, 20323, 20341, 20359, 20521, 20593, 20719, 20773, 20809, 20899, 21061,
21169, 21187, 21277; `dfs2b_queue.txt`) are queued for `dfs2b 9 p p 4000000000 print`
after the chunks. Results will land in `out/dfs2b_P.out`, and verify.sh reads them:
INFEASIBLE lines are reported as exceptions decided in E_2(9), and FEASIBLE witnesses are
re-checked. The other 1353 exceptions are reported, not decided.

**Claim that holds now (finite computation; AI-checked, pending human review):**

> **E_2(9) ∩ (20000, 26863219] ⊆ X_1373**, the 1373 primes listed in
> `2026-11-04-rees-k9-sweep/exceptions_20000_26863219.txt` (all ≤ 424549).
> Equivalently: every prime p ≡ 1 (mod 9) in (20000, 26863219] outside that list has an
> explicit two-level contraction (g, α, β), checked by two independent verifiers; and
> **E_2(9) ∩ (424549, 26863219] = ∅**, with a strict witness (N > 0) for every prime of
> (681337, 26863219].

Notes on the claim:
- 3,098 primes are certified only by P witnesses, which have zero cells. For them,
  p ∉ E_2(9) holds, but the strict N > 0 is not shown. All of them are ≤ 651727.
- The exceptions are **not** claimed to lie in E_2(9). For 839 of the 1373, the complete P
  search proved P empty (all candidates ≤ 99577). For 633 of those, all ≤ 76231, the
  complete T1 search proved T1 empty as well. For the other 534 exceptions, only the
  randomized searches failed (P complete hit its 15 s cap on the 131 c01 primes). No
  generic (full-problem) search was run on them. Above about
  10^5, μ_G ≫ 1 (log10 μ_G = 3.7 at 10^5 and 8.5 at 2·10^5), so most of the exceptions above
  10^5 are probably not in E_2(9) **[argued]**. Below 18000, about 90 % of primes are
  INFEASIBLE in the dfs2b scans, so most exceptions near 2·10^4 probably are in E_2(9)
  **[argued]**.
- Claim gates that stay false: E_2(9) is not known exactly; max E_2(9) is not determined;
  no analytic bound; nothing for κ ≥ 10. The paper and `rees_hsp_reduction.json` are
  unchanged.

**When the sweep finishes**, the claim extends to X = 193710244 if `verify.sh` reports no
new exceptions above 3.2·10^6. That is: no UNRESOLVED in `out/r_c0[2-9].out`,
`out/r_c1*.out` or `out/r_c2*.out`, bad = 0 in both verifiers, and the last line of
verify_k9 reads "CONTIGUOUS: … (20000,193710244] … or is one of the N listed exceptions".
The total prime count must be 1791117. The old verifier's strict run must reject exactly
the P lines (it prints that count).

## Result (2026-11-05)

All chunk passes c01–c25 end with a `DONE` line; `verify.sh` was run on 2026-11-05
(console output `verify_run_20261105.txt`; files `verify_k9.out`,
`verify_witnesses_old.out`, `verify_witnesses_old_strict.out`). Every acceptance test of
"When the sweep finishes" (§6) passes.

- `verify_k9.py 20000 193710244 chunks.txt <all outputs>`: 1,791,117 primes p ≡ 1 (mod 9)
  in (20000, 193710244] (193710244 = ⌊9^9/2⌋). 1,789,744 have a valid witness: 1,786,646
  strict (every cell nonzero) and 3,098 with a zero cell only (P lines; all ≤ 651727).
  **Bad lines: 0**, unparsed 0, no witness/INFEASIBLE conflict, dup = 21 (as in §6).
  Exceptions: **1373**; of these, dfs2b INFEASIBLE: 0, so all 1373 are OPEN. Last line:
  "CONTIGUOUS: every prime p=1 mod 9 in (20000,193710244] has a valid witness or is one of
  the 1373 listed exceptions".
- Old checker, `verify_witnesses.py --zeros --cover 9 20001 193710244`: 1,789,774 witness
  lines, 1,789,744 valid distinct, **bad = 0** (strict 1,786,646, zero cells only 3,098);
  cover: primes = 1,791,117, missing = 1373 (it prints the first 300; they equal the first
  300 of the OPEN list). Strict run (no `--zeros`): bad = 3111 = the number of P lines,
  missing = 4471 = 1373 + 3098, as required.
- Retry files: `out/r_c02.out` … `out/r_c25.out` have 0 UNRESOLVED; `out/r_c01.out` has
  131, all among the 1373. No exception lies above 3.2·10^6.
- The OPEN list, parsed from `verify_k9.out`, is written to
  `2026-11-04-rees-k9-sweep/exceptions_20000_193710244.txt` (1373 lines, sorted, all prime,
  all ≡ 1 mod 9, smallest 20071, largest 424549). It is byte-identical to
  `exceptions_20000_26863219.txt`: the extension added no exception.
- dfs2b on the exceptions: `dfs2b 9 p p 4000000000 print` for p = 20071, 20089, 20107
  started 05:56–06:13; `out/dfs2b_*.out` are still empty, so no exception is decided.

**Claim (finite computation; AI-checked, pending human review):**

> **E_2(9) ∩ (20000, ⌊9^9/2⌋] ⊆ X_1373**, the primes of
> `exceptions_20000_193710244.txt` (all ≤ 424549). Every other prime p ≡ 1 (mod 9) in
> (20000, 193710244] has an explicit two-level contraction (g, α, β) accepted by two
> separately written verifiers; a strict one (N > 0) for every prime of
> (651727, 193710244]. Hence E_2(9) ∩ (424549, 193710244] = ∅.

Quantifiers and access model: a finite check, prime by prime, of explicit witnesses; no
asymptotic statement. The exceptions are OPEN (no witness found), not proved to lie in
E_2(9) (§6 notes). Since 9^9/2 < 8·9^9 < T_A(9) (appendix-schedule2.tex,
Proposition prop:app-s2-TA(ii)), the primes in (9^9/2, T_A(9)] are not covered.

**Gates that stay false:** E_2(9) is not known exactly; max E_2(9) is not determined; no
analytic threshold below T_A(9); nothing for κ ≥ 10; no claim gate in
`research/reductions/rees_hsp_reduction.json` changes (file untouched).

**Commands:** `research/audits/reviews/2026-11-04-rees-k9-sweep/verify.sh` (both verifiers;
nice 10), then the parse of the OPEN line of `verify_k9.out` into
`exceptions_20000_193710244.txt` and `cmp` with `exceptions_20000_26863219.txt`.

**Separate dfs2b snapshot (2026-11-05, files in
`2026-11-02-rees-schedules/small-prime/`, `dfs2b_*.out`; verdict lines only, LIMIT lines
ignored):** every prime p ≡ 1 (mod 8) up to 13873 and every prime p ≡ 1 (mod 9) up to
16363 has a FEASIBLE or INFEASIBLE verdict (first gaps 13913 and 16381, both running).
Largest INFEASIBLE: κ = 8, 14281 (`dfs2b_k8_hi_q3.out`; also 14177 in `dfs2b_k8_hi_q1.out`);
κ = 9, 18199 (`dfs2b_k9_17501_20000.out`; also 18181, 18127, 17929, 17911, …). No prime has
both verdicts. The old checker (`--zeros`) accepts every dfs2b FEASIBLE witness (at 06:49 AEDT: κ = 8,
216 lines, 206 distinct primes, bad 0; κ = 9, 23 lines, 23 primes, bad 0). The κ = 8 files
are still being appended to; the decided bounds and the largest INFEASIBLE values above were
the same at 06:40 and 06:49. This is what the paper's dfs2b snapshot now quotes (I223).

## 7. Next steps

- **Verify command** (both verifiers, all outputs; run it when all three logs show
  `WORKER_DONE`, or at any time, since it is safe while running):
  `/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-k9-sweep/verify.sh`
  It writes `verify_k9.out`, `verify_witnesses_old.out` and `verify_witnesses_old_strict.out`.
  A cheaper partial check is `snapshot_verify.sh`, which pauses one sweep process while it
  runs.
- **Progress:** `status.sh`, and the screens `k9sweep_0`, `k9sweep_1`, `k9sweep_2`.
- **Deferred decision pass on the exceptions** (not run; it needs free cores):
  - P complete without the cap on the 131 c01 primes and the c00 primes in (99577, 200000];
  - T1 complete on the c00 primes in (76231, 200000];
  - then a generic search (`dfs2r nosym rand` or `famsearch full`) on what remains above
    about 8·10^4.
  The bottom of the list needs `dfs2b`, at 1–2 h per prime near 2·10^4 and growing.
- Optional: a strict T1 attempt on the 3,098 P-only primes, to show N > 0 there too.
- Per the research protocol, a handoff entry and a STATE.md update are left to the
  integrator.

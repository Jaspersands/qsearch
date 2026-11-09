# κ = 8, T1 sweep of (8^8/2, T_A(8)] = (8388608, 117441563] (2026-11-04)

AI-run computation (Claude Code subagent), pending human review. Local only: no git, no
network. Code and outputs: `2026-11-04-rees-t1-sweep-hi/`. This continues §5 of
`2026-11-04-rees-threshold-5.md` (Theorem 5.1, which covered (49417, 8388608]).

**Goal.** Every prime p ≡ 1 (mod 8) with 8388608 < p ≤ 117441563 gets an explicit strict
two-level contraction (g, α, β), so p ∉ E_2(8). The range holds **1,534,715** such primes
(numpy sieve, cross-checked against `sympy.primepi` at both ends).

## 1. What changed in the code, and why it is equivalent

`famsym_direct.c` is `../2026-11-04-rees-threshold-5/famsym.c` with four changes. The DFS,
the restart loop, the choice of γ_0, the output normalization (β_0 = 0, α_0 = 1) and the
final K² cell re-check are copied unchanged.

1. **No index table.** In `famsym.c` the table `idx[y] = log_g(y) mod K` is read only
   through `inQ(y, m)`, which means y ≠ 0 and idx[y] = m (mod K). For y = g^e we have
   y^h = (g^h)^e = ζ^(e mod K), where ζ = g^h has exact order K. So inQ(y, m) holds iff
   y ≠ 0 and y^h = ζ^m. That is now computed by fast exponentiation, O(log p) per query.
   Since p < 2^32, every product fits in a u64, so a plain 64-bit `a*b % p` is exact and no
   `__uint128_t` is needed. The program refuses P1 ≥ 2^32.
2. **No coset list.** `famsym.c`'s `Qlist[m*H + t] = g^(m + K t)` is read only when the
   level-0 candidate lists are built. Q_m is now walked directly, from y = g^m in steps of
   y ← y·g^K, in the same order. The fixed element `Qlist[B*H] = g^B` becomes `powm(g, B)`.
3. **Window `win=W`.** Changes 1 and 2 alone made the program slower, not faster (see §2).
   The table was not the only O(p) cost. The level-0 lists are whole cosets, about h/8
   candidates per unknown, and every level-0 DFS node filters them all. So the sweep mode
   keeps only the first W candidates of each level-0 walk, starting at a random t_0 ∈
   [0, h). The sweep uses W = 3072. This is a sub-search of the same tree, so every
   witness it returns is a T1 witness, re-checked on all 64 cells. Without `win=`
   ("exact" mode) the whole coset is walked from t_0 = 0, no extra random numbers are
   drawn, and the run is step-for-step that of `famsym.c`.
4. A segmented sieve of [P0, P1] replaces the full sieve up to P1.

Exact mode is *equivalent* to `famsym.c`: the only changes are how inQ and Qlist are
computed, and the values are the same. Windowed mode is *sound* but not complete. Its
NOTFOUND means only "not found", and every NOTFOUND goes to `retry.sh` (§4). Correctness
of the claim does not depend on either program, because the verifier (§5) re-derives each
witness from the definition.

## 2. Cross-checks and timings

Outputs are in `crosscheck/`. The comparisons drop the `secs=` field.

| run | primes | result |
|---|---|---|
| old `famsym` vs `famsym_direct` exact, (49418, 200000], seed 1 | 3220 | **identical** FOUND/NOTFOUND lines (3219 FOUND, NOTFOUND 55889 in both, the known T1-empty prime) |
| old vs exact, [8386000, 8388608], seed 1 | 36 | **identical** |
| windowed W = 3072, (49418, 200000], seed 11 | 3220 | FOUND at every prime where the old program found one. The only NOTFOUND is 55889. `verify_hi.py`: all valid |
| windowed W = 3072, [8300000, 8388608] | 1366 | all FOUND, all valid |
| windowed W = 3072, [117400000, 117420000] | 237 | all FOUND, all valid |
| `retry.sh` on 55889 | 1 | windowed T1 NOTFOUND (as expected), then `famsearch` H witness, FOUND |

Timings (CPU seconds per prime, nice 10, with the four `dfs2b` jobs running):

| program | p ≈ 8.39·10⁶ | p ≈ 1.174·10⁸ |
|---|---|---|
| old `famsym` (table) | 0.06 (2.1 s / 36 primes) | **1.50** (5 primes) |
| `famsym_direct` exact | 0.67 (24.2 s / 36) | not run (O(p log p)) |
| windowed W = 256 | | 6.5, 20 of 25 NOTFOUND |
| W = 512 | | 1.50 |
| W = 1024 | | 0.15 |
| W = 2048 | 0.017 | 0.027 |
| **W = 3072 (used)** | **0.015** (max 0.030) | **0.023** (max 0.043) |
| W = 4096 | 0.017 | 0.027 |

With the table, the sweep would cost about 1.5·10⁶ × ~1 s ≈ 400 CPU-hours. With W = 3072
it costs about 1.53·10⁶ × 0.02 s ≈ 9 CPU-hours, roughly 65 times less at the top end.

## 3. Chunks and screen sessions

The range is split into 16 equal chunks, (lo, hi] in `chunks.txt`. Worker w runs chunks w,
w+4, w+8 and w+12, so the contiguous verified bound grows from the bottom at the speed of
worker 0. Command per chunk:
`famsym_direct 8 lo+1 hi 200000 50 (1000+i) win=3072` (budget 2·10⁵ nodes, 50 restarts).
Output is `out/cNN.out`, flushed after each prime. The log is `out/worker_w.log`.

| screen | chunks | started |
|---|---|---|
| `t1sweep_0` | c00 (8388608, 15204417], c04, c08, c12 | 2026-11-04 18:23 AEDT |
| `t1sweep_1` | c01, c05, c09, c13 | 18:23 |
| `t1sweep_2` | c02, c06, c10, c14 | 18:23 |
| `t1sweep_3` | c03, c07, c11, c15 (…, 117441563] | 18:23 |

All four run at `nice -n 10`, and the four `dfs2b` jobs still show 97–99 % CPU. The measured
rate is about 45–50 primes/s per worker, and about 383k primes per worker. **Projected
finish: about 20:50–21:05 AEDT on 2026-11-04** (≈ 2.5 h wall; measured 176 primes/s overall). When a worker finishes its
chunks, it collects its NOTFOUND primes into `out/notfound_wW.txt` and runs `retry.sh` on
them, writing `out/retry_wW.out`. The chain is: windowed T1 with W = 12288, 20 restarts of 10⁶
nodes; then `famsearch auto` (H when h is even); then the original table-based
`famsym complete`, which decides T1. A prime with no witness after all three is written
as `UNRESOLVED p=…`. The log ends with `WORKER_DONE`.

## 4. NOTFOUND primes

So far: **none** in 417,860 primes (snapshot of §5). The final list is
`cat out/notfound_w*.txt`. Its resolution is in `out/retry_w*.out`, and remaining failures
show as `grep UNRESOLVED out/retry_w*.out`.

## 5. Verifier and results so far

`verify_hi.py` shares no code with the C programs. It uses Python ints, `gmpy2.is_prime`,
`sympy.isprime`, and a numpy sieve that is cross-checked against `sympy.primepi`. For each
`FOUND` line it checks the definition used by `verify_sweep_k8` and §5:

- p is prime and p ≡ 1 (mod 8);
- ζ = g^h has exact order 8;
- for all 64 cells, v = α_j + β_i ≠ 0 and v^h = ζ^(−(i+j) mod 8). No zero cells are
  allowed (strict).

It then checks coverage: every prime p ≡ 1 (mod 8) in the range must have exactly one
valid line and no bad line. Duplicates are reported. It prints a per-chunk table (primes,
valid, bad, dup, missing) and the contiguous bound X. It was tested on a corrupted line
(flagged BAD), on duplicated files (flagged dup), and on the 55889 gap (flagged missing).

**Command:** `/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-t1-sweep-hi/verify.sh`
(it writes `verify_hi.out`). For a partial run, an incomplete last line shows as UNPARSED
and its prime as missing, which is harmless.

**Snapshot at 19:03 AEDT** (`snapshot_verify.sh`; output in
`snapshots/verify_snap_20261104_190307.out`). Chunks c00–c03 are complete. Each running chunk
is cut at the last prime it had reached. Earlier snapshots: 18:26 (34,419 primes,
X = 9000840) and 19:01 (`verify_snap_20261104_190116.out`, 400,149 primes,
X = 21984912). Both had bad = 0.

| chunk | lo | hi or reached | primes | valid | bad | dup | missing |
|---|---|---|---|---|---|---|---|
| c00 (DONE) | 8388608 | 15204417 | 104776 | 104776 | 0 | 0 | 0 |
| c01 (DONE) | 15204417 | 22020227 | 101764 | 101764 | 0 | 0 | 0 |
| c02 (DONE) | 22020227 | 28836037 | 99972 | 99972 | 0 | 0 | 0 |
| c03 (DONE) | 28836037 | 35651846 | 98460 | 98460 | 0 | 0 | 0 |
| c04 | 35651846 | 36056497 | 5784 | 5784 | 0 | 0 | 0 |
| c05 | 42467656 | 42759793 | 4134 | 4134 | 0 | 0 | 0 |
| c06 | 49283466 | 49480993 | 2784 | 2784 | 0 | 0 | 0 |
| c07 | 56099275 | 56112169 | 186 | 186 | 0 | 0 | 0 |
| total | | | 417860 | 417860 | 0 | 0 | 0 |

417,860 FOUND lines: all parse, all valid, no duplicates, and no NOTFOUND. That is 27 % of
the 1,534,715 primes. The per-chunk counts of the finished chunks match `chunks.txt`. The
first block of four chunks took 37.7–40.5 min. Three blocks remain, each slightly slower
because p is larger.

## 6. Claim that holds now

**E_2(8) ∩ (8388608, 36056592] = ∅ by explicit witnesses.** Every prime p ≡ 1 (mod 8)
in this interval (the last is 36056497) has an explicit strict two-level contraction
(g, α, β), checked by `verify_hi.py`. AI-checked, pending human review.

With Theorem 5.1 of `2026-11-04-rees-threshold-5.md` this extends to
E_2(8) ∩ (49417, 36056592] = ∅. When all four workers log `WORKER_DONE` and `verify.sh`
reports bad = 0, dup = 0, missing = 0 (after the retries), the bound becomes
X = 117441563 = T_A(8). In that case E_2(8) ⊆ [3, 20000] ∪ the 29 primes of
`gap_k8_unresolved.txt`, with no part left above 49417.

**Acceptance test for the later pass:** `verify.sh`; its last line must read
`CONTIGUOUS: every prime p=1 mod 8 in (8388608,117441563] has exactly one valid strict witness`,
with TOTAL bad = dup = missing = 0. The prime count must be 1534715, and
`grep UNRESOLVED out/retry_w*.out` must print nothing.

Gates unchanged: this is a finite computation for κ = 8 only. It gives no analytic bound and
does not touch the paper or `research/reductions/rees_hsp_reduction.json`.

## Files

All files are in `2026-11-04-rees-t1-sweep-hi/`.

- Code: `famsym_direct.c` (and its binary), `verify_hi.py`.
- Scripts: `run_worker.sh`, `retry.sh`, `verify.sh`, `snapshot_verify.sh`.
- Inputs: `chunks.txt`.
- Outputs: `out/` (sweep outputs and logs), `crosscheck/` (§2), `snapshots/`.

## Final result (integrator, 11-04 ~21:10)

All four workers printed `WORKER_DONE` with `notfound = 0` (no retries needed).

- `verify.sh` (this sweep's `verify_hi.py`): TOTAL 1534715 primes, 1534715 valid, bad = dup = missing = 0; "CONTIGUOUS: every prime p=1 mod 8 in (8388608,117441563] has exactly one valid strict witness". 96 s.
- The older, separately written verifier of the threshold-5 pass, `../2026-11-04-rees-threshold-5/verify_witnesses.py --cover 8 8388609 117441563 out/c*.out` → `verify_witnesses_old.out`: witness lines 1534715, valid distinct 1534715, bad 0; cover primes 1534715, missing 0. 181 s.

**Claim now (finite computation, AI-checked, pending human review):** E_2(8) ∩ (8388608, ⌈T_A(8)⌉] = ∅, with ⌈T_A(8)⌉ = 117441563 (T_A(8) = 117441562.03, so this end point is the ceiling). With Theorem 5.1 of `-threshold-5.md`, E_2(8) ∩ (49417, ⌈T_A(8)⌉] = ∅, hence E_2(8) ⊆ [3, 20000] ∪ X_29 (the 29 primes of `gap_k8_unresolved.txt`). Folded into the paper at I187.

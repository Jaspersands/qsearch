# Rees HSP: scaled exact end-to-end simulation (round 2, campaign item 12)

2 November 2026. AI-only session (Claude Code, Opus 5.5), plus one independent AI code-review
agent. Not human review, not Lean. Labels: **[exact]** = complete finite computation in exact
arithmetic; **[sampled]** = exact check on random samples, not exhaustive; **[argued]** =
reasoning, not machine-checked.

Files written (and nothing else): `theorems/rees_end_to_end_ext.py`,
`tests/test_rees_end_to_end_ext.py`, this report, and the run folder
`research/audits/reviews/2026-11-02-rees-e2e-scale/` (`*.json`, `*.out`, `summarize.py`,
`top_source_check.py`, `pytest.out`). Round 1's `theorems/rees_end_to_end_sim.py`, the IS solver
`theorems/rees_is_sde_solver.py` and the Schedule 2 solver `theorems/power_sde.py` are imported
read-only and unchanged.

Reproduce:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_end_to_end_ext.py
```
```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m theorems.rees_end_to_end_ext n5_11 --out n5_11_rule_w.json
```

Tests: 42 passed in 105 s on a heavily loaded machine (`2026-11-02-rees-e2e-scale/pytest.out`).
The long runs and their exact command lines are in §3. `git status --short` changed only by my
files.

## 0. Answers

- **(a) Real solver at the charged arity: done.** Every grade calls `is_sde_solve`
  (linear and Schedule 1) or `power_weights` plus the Bezout lift (Schedule 2), on blocks of
  exactly the Rule W arity M_d. That is B_{κ_d}(g_d) for Schedule 1, g_d + 1 for the linear case
  and (g_d+1)((κ_d−1)g_d+1) for Schedule 2. Brute force is gone. A second count,
  `--count deterministic`, uses G(κ_d, g_d)^{⌈log₂ t⌉}, the columns the deterministic run
  actually consumes (main.tex, Schedule 1 paragraph). Every witness is verified exactly.
- **(b) Combined rule: done, with Schedule 2 run end to end.** `rule_w(p, d, g_d)` is the
  §1 table of `2026-11-02-rees-combined-schedule.md` and uses (p, d, g_d) only. Schedule 2 is the
  existing two-level symmetric contraction (`theorems/power_sde.py`), not a substitute. It runs
  end to end on Heis(F_1031), where 1031 ≥ 16·2⁶ = 1024 clears the κ = 2 threshold: 4 subgroups,
  3 seeds, 84 Schedule-2 merges, all exact. **Substitute, labelled:** at p = 1031 the lifted
  *source* is built from H (|L| = 1.1·10⁹ is too large to evaluate f everywhere) and
  spot-checked against the oracle (§1.3). Everything after the source sees only the state, the
  labels and the cover.
- **(c) Class four: done.** The sparse backend makes covers of order p¹¹ feasible.
  - n5 over F_11 runs at full Rule W arity (M = 1024, 3, 64; 7,077,888 charged queries per run)
    for 9 subgroups.
  - n5 over F_7 and a second filiform family Q5 over F_7 ([e1,e_i] = e_{i+1}, [e2,e3] = e5)
    run at the deterministic count (M = 1024, 729, 64). At the Rule W count they would need
    1.25·10¹² queries per run, which is out of reach (§4). At the deterministic count each run is charged
    1,146,617,856 queries (S = m+1) and makes 4,478,976 solver calls at grade 4. Both algebras pass
    for 5 of their 9 subgroups: 1, ⟨e2⟩, ⟨e1⟩, ⟨e1+e3⟩ and ⟨e2+e4⟩. The four lines are
    non-normal and meet the centre trivially. I stopped the sweep at 5/9 by hand when the machine
    load reached about 200. The other four subgroups (Z(G), ⟨e2,e5⟩, ⟨e3⟩ or ⟨e3+e4⟩, and
    ⟨e1+e2+e5⟩) ran at full Rule W arity on n5(F_11), and their F_7 top sources are checked exactly.
  - Class four over F_5 is out of reach at any schedule: κ_4 = 4 = p − 1 is the zero-sum case,
    and the solver needs G(4,1)³ = 2.8·10¹⁴ columns.
- **(d) More subgroups: done.** 14 subgroups on each n4 (5 new: ⟨e2+e4⟩, ⟨e2+e3⟩, ⟨e1,e4⟩,
  ⟨e1+e2⟩, ⟨e1+2e2+e4⟩), and 9 on each class-four algebra. They include non-normal subgroups with
  H ∩ Z(G) = 1 (lines in every grade, homogeneous and not), non-normal ones containing Z(G),
  normal ones, H = 1 and H = G.
- **Acceptance.** Every completed run recovers log H exactly. Every measured label law is
  exactly uniform on K_d^⊥. Every stage output equals ρ_{H_d}, the top source equals ρ_{H_c}, and
  the grade-one law is uniform on (th)^⊥. Block sizes equal the charged arity, and queries equal
  c·S·Π_d M_d. **Caveat (from the review):** the last two hold by construction, since the
  simulator charges queries from the same arities. The real check of the arities is
  `test_rule_w_table`, which pins them against Rule W computed by hand.
- **Finding.** At the charged arities on these small fields, almost every block contains a zero
  label, and the deterministic solver then returns a unit vector. The full Ivanyos–Santha path
  (Theorem 11) supplies witnesses only where p^{a_d} is comparable to M_d. That includes
  Heis(F_5) and n4(F_5) at the deterministic count, n4(F_7) and n5(F_11) at grade 2, and a
  diagnostic witness policy (§2.3). The counts are in §3.

## 1. What runs

The algorithm is round 1's (`2026-11-02-rees-end-to-end.md` §1): lifted sources from c
evaluation points, then for each grade d = c, …, 2 the exact central instrument, an SDE witness
and the controlled-right-action channel, and S = m + 4 grade-one Fourier samples. The driver
`run_rees_ext` sees only the top source, the public cover and the labels.

### 1.1 Rule W (`rule_w`, `tree_schedules`)

| condition on (p, d, g_d) | schedule | M_d | solver called |
|---|---|---|---|
| κ_d = 1 | linear | g_d + 1 | `is_sde_solve` (nullspace, then x ↦ x^t) |
| κ_d ≥ 2, p ≥ 16κ_d^{2κ_d+2} | Schedule 2 | (g_d+1)((κ_d−1)g_d+1) | `power_weights(p, κ_d, ·)`, then s_i = w_i^t with td ≡ κ_d (mod p−1) |
| otherwise | Schedule 1 at degree κ_d | B_{κ_d}(g_d) (`--count deterministic`: G(κ_d,g_d)^{⌈log₂ t⌉}) | `is_sde_solve` |

The tests pin the table on all eight groups, the thresholds (1019 → S1, 1031 → S2 at κ = 2;
104971 → S1, 105019 → S2 at κ = 3) and M_d ≤ B_d(g_d). They also check the Schedule 2
solver with the Bezout lift at (p, d, g) = (1031, 2, 1..3), (1031, 4, 2) and (105019, 3, 2..3) on
random, repeated-basis, rank-one and zero-column families **[exact]**.

### 1.2 SparseExactBackend

It uses round 1's representation ρ = scale/|G_d| Σ_g c(g) R_g, c(g) ∈ Z[ζ_p], but stores only
the rows with c(g) ≠ 0. For p ≤ 64 a row is a canonical Z[ζ_p] vector. Above that it is a
monomial a·ζ^e (a unique representation), and a sum that is not a monomial raises. Three exact
simplifications, all stated in the module:

1. Π_λ ρ Π_λ = Π_λ ρ, because Π_λ is a central idempotent of the group algebra (round 1 forms
   both products).
2. Pure functions are memoised on exact inputs. States are *interned*: two states with the same
   exact representation become one object. The label law and post-measurement states are cached
   per object, and the channel output per sorted multiset of (post state, s_i). The multiset is
   enough because the trace function F is a product.
3. Post-measurement states are formed only where s_i ≠ 0. The others are traced out unread.
   Labels are still sampled for every source, and every source is charged c queries.

Simplification 2 is what makes class four feasible. With it, the number of distinct exact
states measured at each grade of each run was **1** in every completed run (the
`distinct_states_measured` field). So all of the millions of sources measured at a grade were
the same exact state, which is ρ_{H_d} **[exact]**.

**Cross-checks against round 1's `ExactBackend` [exact]** (tests), on Heis(F_3), Heis(F_5) and
n4(F_5) with 7 subgroups:
- source, label law, every post-measurement state and the channel output are equal at every
  grade;
- in a second test, with witnesses of support > 1 and in both poly and forced monomial mode, all
  of the above plus the complete grade-one readout law over F_p^m are equal.

The review agent also ran its own cross-check, over 3 seeds and with one evaluation point as
well as c, and found everything equal.

**Parallel trees** (`--workers`). The S descent trees are independent, so
`run_instance_parallel` runs them in separate processes with independent seeds (seed·1000 + i).
It pools the grade-one samples, ANDs every exact flag and sums the counts. Each worker grades its
own trees exactly. The F_7 class-four runs use this mode, and a test checks it on n4(F_5).

### 1.3 Lifted source: three modes

- `exhaustive` (Heis(F_3), Heis(F_5), n4(F_5), n4(F_7)): round 1's own routine. It enumerates
  the whole cover, checks the fibres exhaustively and checks that S is a subgroup.
- `level_set` (n5 and Q5 over F_7 and F_11). The routine evaluates f on all of L (p^m points,
  the information round 1 also uses). Because E_1 is the identity on grade one, it then
  enumerates {a : E_1(a) ∈ f⁻¹(f(0))} over the higher-grade digits and filters by
  f(E_s(a)) = f(0) for s = 2..c. That gives the identity fibre S exactly **[exact]**. S is
  checked to be a subgroup, in full when |S|² ≤ 4·10⁶ and on 20,000 random pairs otherwise
  **[sampled]**. The coset property of the tuple oracle is checked on 2,000 random pairs
  **[sampled]**. `top_source_check.out` confirms S = exp(Σ_k t^k(h∩γ_k)) for all 27 class-four
  (G, H) **[exact]**, and the tests check that the three modes agree on Heis(F_5) and n4(F_5).
- `substitute` (Heis(F_1031) only, labelled in every output row). S is built from H as
  exp(Σ_k t^k(h∩γ_k)). It is checked against the oracle on 3,000 points of S and on 2,000
  random coset pairs **[sampled]**. This is the only place H enters before grading.

## 2. Results

### 2.1 Completed runs (all exact; every flag of §0 "Acceptance" true in every row)

| group, cover dims, order | count | subgroups × seeds | M_d (d = 2..c) | queries per run |
|---|---|---|---|---|
| Heis(F_3), (3,1), 3⁴ | Rule W | 7 × 5 | 64 | 896 |
| Heis(F_5), (3,1), 5⁴ | Rule W | 7 × 5 (+7 × 3 diagnostic) | 64 | 896 |
| Heis(F_5) | deterministic | 7 × 5 | 8 | 112 |
| n4(F_5), (4,2,1), 5⁷ | Rule W | 14 × 5 (+14 × 3 diagnostic) | 324, 2 (S1, linear) | 15,552 |
| n4(F_5) | deterministic | 14 × 5 | 18, 2 | 864 |
| n4(F_7), (4,2,1), 7⁷ | Rule W | 4 × 1 | 324, 46656 (S1, S1 at κ = 3) | 362,797,056 |
| n4(F_7) | deterministic | 14 × 5 | 324, 216 | 1,679,616 |
| **n5(F_11), (5,3,2,1), 11¹¹** | **Rule W** | 9 × 1 | 1024, 3, 64 (S1, linear, S1) | **7,077,888** |
| n5(F_7), (5,3,2,1), 7¹¹ | deterministic, S = m+1 | 5 × 1 | 1024, 729, 64 | 1,146,617,856 |
| Q5(F_7), (5,3,2,1), 7¹¹ | deterministic, S = m+1 | 5 × 1 | 1024, 729, 64 | 1,146,617,856 |
| **Heis(F_1031), (3,1), 1031⁴** | **Rule W: Schedule 2** | 4 × 3 | 4 | 56 |

S = m + 4 unless stated. For the F_7 class-four runs, S = m + 1 is the paper's
S = m + ⌈log_p(3/ε)⌉ at ε = 1/3; its rank-failure bound is (7⁵−1)/(6·7⁶) ≈ 0.024. The subgroup
lists are in `catalogue()`. Per class-four group they are: 1, ⟨e2⟩, ⟨e1⟩, ⟨e1+e3⟩, ⟨e2+e4⟩,
⟨e3⟩ (Q5: ⟨e3+e4⟩), Z(G) = ⟨e5⟩, ⟨e2,e5⟩ and ⟨e1+e2+e5⟩. All but 1 and Z(G) are non-normal.
The six lines other than Z(G), the nonhomogeneous ⟨e1+e2+e5⟩ included, meet the centre
trivially; ⟨e2,e5⟩ is non-normal and contains Z(G). The flags are recorded in every JSON row
(`normal`, `meets_center_trivially`, `contains_center`).

### 2.2 Which solver path supplied the witnesses (`summarize.py` output)

| run | grade: schedule, M | blocks | full solver path | of which Theorem 11 calls | zero-column exit |
|---|---|---|---|---|---|
| Heis(F_3), Heis(F_5) Rule W | 2: S1, 64 | 245 each | 0 | 0 | 245 |
| Heis(F_5) deterministic | 2: S1, 8 | 245 | 40 | 40 | 205 |
| n4(F_5) Rule W | 2: S1, 324 / 3: linear, 2 | 560 / 181,440 | 0 / 74,871 | 0 / – | 560 / 106,569 |
| n4(F_5) deterministic | 2: S1, 18 | 560 | 157 | 157 | 403 |
| n4(F_7) deterministic | 2: S1, 324 / 3: S1 κ=3, 216 | 560 / 181,440 | 8 / 0 | 8 / 0 | 552 / 181,440 |
| n4(F_7) Rule W | 2: S1, 324 / 3: S1 κ=3, 46656 | 32 / 10,368 | 0 / 0 | 0 / 0 | 32 / 10,368 |
| n5(F_7), Q5(F_7) deterministic (per run) | 2: S1, 1024 / 3: S1 κ=3, 729 / 4: S1, 64 | 6 / 6,144 / 4,478,976 | 0 / 0 / 242 | 0 / 0 / 276 | 6 / 6,144 / 4,478,734 |
| n5(F_11) Rule W | 2: S1, 1024 / 3: linear, 3 / 4: S1, 64 | 81 / 82,944 / 248,832 | 36 / 76,482 / 415 | 55 / – / 488 | 45 / 6,462 / 248,417 |
| Heis(F_1031) | 2: S2, 4 | 84 | 84 (Schedule 2) | – | 0 |

The probability that a block has no zero label is (1 − p^{−a_d})^{M_d}, which is negligible
when M_d ≫ p^{a_d}: (2/3)⁶⁴ ≈ 5·10⁻¹² at Heis(F_3). So at the charged arities, most Schedule 1
witnesses on these fields are unit vectors. This is correct: any nonzero witness is valid.
But it means the run tests the solver's full path only on the blocks counted above **[exact]**.

### 2.3 Diagnostic witness policy (`--avoid-zero-columns`)

If a block has a zero label and its nonzero labels alone meet the solver's column count, the
solver runs on those. The witness is still a valid nonzero witness of the whole block. It is not
the default. On Heis(F_5) (Rule W, 7 × 3) and n4(F_5) (Rule W, 14 × 3) it made Theorem 11
supply 84 and 288 grade-2 witnesses, of support > 1 in general. All 63 runs passed every check
**[exact]**.

### 2.4 Negative controls (tests)

- A nonzero non-witness s = e_i on a nonzero label makes the channel raise "does not descend"
  (Heis(F_5) ⟨x⟩, n4(F_5) ⟨e2⟩).
- One evaluation point instead of c (Prop. `prop:single-evaluation`) on n4(F_5) ⟨e2⟩ either
  raises "does not descend" or gives wrong stage states. The test accepts nothing else.

## 3. Long runs (`2026-11-02-rees-e2e-scale/`)

| file | command arguments | wall time | result |
|---|---|---|---|
| `small_rule_w_5seeds` | `heis3 heis5 n4_5 --seeds 5` | 56 s | 140 runs, all pass |
| `small_deterministic_5seeds` | `heis5 n4_5 n4_7 --count deterministic --seeds 5` | 781 s | 175 runs, all pass |
| `small_avoid_zero_diagnostic` | `heis5 n4_5 --seeds 3 --avoid-zero-columns` | 72 s | 63 runs, all pass |
| `heis1031_schedule2_3seeds` | `heis1031 --seeds 3` | 155 s | 12 runs, all pass |
| `n5_11_rule_w` | `n5_11` | 1093 s | 9 runs, all pass |
| `n4_7_rule_w` | `n4_7 --h …` (⟨e2⟩, ⟨e1+e3⟩, Z(G), ⟨e2,e3,e4⟩) | 1811 s | 4 runs, all pass |
| `n5_7_deterministic` | `n5_7 --count deterministic --extra-samples 1 --h "<e2> non-normal" --workers 6` | 167 s | 1 run, pass (full JSON) |
| `n5_7_deterministic_all` | the same, one `--h` per subgroup | 5 × 156–3670 s | 5 runs pass; stopped by hand at 5/9 (`.out` only, no JSON) |
| `q5_7_deterministic` | as for n5_7 | 167 s | 1 run, pass (full JSON) |
| `q5_7_deterministic_all` | as for n5_7 | 5 × 156–3670 s | 5 runs pass; stopped by hand at 5/9 |
| `top_source_check` | script | ~7 min | 27/27 equal ρ_{H_c} |

Times are wall clock on a machine with load average 70–130 on 10 cores. The long runs were
started before the review fixes of §5 were added. Those fixes add checks and an overflow guard
and change no computed value. The new top-source check was run separately
(`top_source_check.out`), and the full test suite was re-run after the fixes.

## 4. What is out of reach, and why

- **n5(F_7) at Rule W:** M = (1024, 531441, 64) gives 1.25·10¹² queries per run (S = m+4). The
  label sampling alone is 3·10¹¹ draws. The deterministic count (729 instead of B₃(2) = 531441)
  is 1.5·10⁹ queries per run with S = m+1, about 4.5·10⁶ IS solver calls. At the IS solver's
  ≈ 1 ms per call here, that is the cost of the F_7 runs.
- **Class four over F_5:** κ_4 = gcd(4,4) = 4 = p−1, and t = 5 at p = 5, so Schedule 1 needs
  G(4,1)³ = 65536³ = 2.8·10¹⁴ columns at grade 4 under either count. This is the zero-sum regime
  of thm:power-sde (iii).
- **Schedule 2 on class ≥ 3:** the smallest admissible field is p ≥ 1024, and n4(F_1031) has a
  cover of order 1031⁷ > 2⁶³, which overflows the int64 index. At p = 1031 only subgroups with
  small |S| run (dim h ≤ 1, H ∩ Z = 1). Z(G) and larger H need |S| ≥ 1031² with 1031 colliding
  terms per row in monomial mode.

## 5. Independent review (one AI agent, given the code, not this report)

It found **no correctness bug** in the sparse backend, memo or interning, Rule W, the Bezout
lift or the diagnostic policy. It checked the label-law formula, Π ρ Π = Π ρ, the channel formula
and descent logic, uniqueness of the monomial representation, the readout class trick,
id-reuse safety (every state stays alive in the intern table), the absence of hidden
information in the algorithm path, and both source modes. Its findings, all addressed:

1. The query-count and block-size flags hold by construction. They are now labelled that way
   here (§0) and in the code; the arities are pinned by `test_rule_w_table`.
2. The top source was not graded. Added `top_source_equals_rho_H_c` to every row, and
   `top_source_check.py` for the class-four (G, H).
3. The monomial-mode channel had no overflow guard or content normalisation. Both added.
4. Test gaps: the single-point test accepted any ArithmeticError (now only "does not
   descend"); monomial mode and multi-state channels lacked a round-1 cross-check (now
   `test_multi_state_channel_and_mono_mode_match_round1`).
5. `run_instance` treated every RuntimeError as a Schedule 2 abort. It now catches only the
   sampler-exhaustion error.

## 6. Exact statement that now holds

**[exact, finite]** Let L be one of Heis(F_3), Heis(F_5), Heis(F_1031), n4(F_5), n4(F_7),
n5(F_11), n5(F_7) or Q5(F_7), and let H be one of the subgroups run on it (§2.1: 7 on each Heis
over F_3 and F_5, 4 on Heis(F_1031), 14 on n4(F_5), 14 on n4(F_7) at the deterministic count
and 4 at Rule W, 9 on n5(F_11), and 5 each on n5(F_7) and Q5(F_7)). Give the procedure oracle access to a left-coset
hiding function of H; at p = 1031 the source is the labelled substitute. The procedure
- prepares c-point lifted sources, c queries each;
- at each grade d = c..2, uses the exact central instrument, the Rule W schedule from
  (p, d, g_d), and the deterministic IS solver (or Schedule 2 at p = 1031) on blocks of exactly
  M_d sources, then the controlled-right-action channel;
- takes S exact grade-one Fourier samples.

It returned log H in every completed run (§2.1 counts). Every measured label law equaled the
uniform law on K_d^⊥, every stage source equaled ρ_{H_d}, and the oracle cost was
c·S·Π_d M_d: up to 7,077,888 queries per run at class four (n5(F_11), full Rule W arity) and
362,797,056 at n4(F_7). Here M_d = B_{κ_d}(g_d), g_d+1 or (g_d+1)((κ_d−1)g_d+1), except on the
rows marked "deterministic", where M_d = G(κ_d, g_d)^{⌈log₂ t⌉}.

**Still missing:** any human review; any group, prime or subgroup not run; a coherent
receiver or gate-level circuit; any asymptotic statement. Also missing: Rule W arity on
n5(F_7)/Q5(F_7) (out of reach, §4); Schedule 2 on class ≥ 3; the oracle-derived source at
p = 1031; and full-path IS witnesses at the high-arity grades, which are mostly unit vectors (§2.2).

## 7. Claim gates that must stay false

In `research/reductions/rees_hsp_reduction.json`: `coherent_receiver_implemented`,
`general_sde_implemented`, `independent_review`, `novelty_established`,
`speedup_claim_allowed` and `formal_compiler_checked`. In `rees_complete_instrument.json`:
`quantum_receiver_implemented`, `asymptotic_runtime_tested`, `independent_review` and
`formal_verification`. Also keep false any claim of polynomial time below the Schedule 2
thresholds and any claim that Schedule 2 is human-checked. This pass flips none of them.

On the IS-solver report's recommendation (`2026-11-02-rees-is-solver.md` §8): items (ii) and
(iii) are now met, since the simulator calls `is_sde_solve` at every Schedule 1 grade with κ_d,
checks every witness, and Schedule 1 supplies witnesses with κ ≥ 2 end to end. Items (i), an
independent human review, and (iv), a new flag that says what was executed, are not. I flip no
flag. A suggested flag, if the owner wants one, is
`schedule1_solver_executed_end_to_end: true`, with executed reduced degrees {1, 2, 3} and the
groups of §2.1.

## Proposed paper text

**Target:** `docs/papers/rees-hsp/main.tex`, paragraph "Exact end-to-end simulation"
(currently line 360). Append after its last sentence. **Status:** artifact, exact finite
computation, AI-checked, pending human review.

```latex
A second artifact, \file{theorems/rees_end_to_end_ext.py} (report \file{research/audits/reviews/2026-11-02-rees-e2e-scale.md}), replaces the exhaustive search by the solvers the paper charges and chooses every arity by the per-grade rule of Remark~\ref{rem:combined-schedule} from $(p,d,g_d)$ alone: the deterministic Ivanyos--Santha solver with $M_d = B_{\kappa_d}(g_d)$, the linear solver with $M_d = g_d+1$, and, on the Heisenberg group over $\mathbb{F}_{1031}$, where $p \ge 16\kappa_d^{2\kappa_d+2}$ holds for $\kappa_d = 2$, the two-level contraction of Theorem~\ref{thm:power-sde}(ii) with $M_d = 4$. It stores each state exactly on its support, which reaches covers of order $11^{11}$. On the class-four filiform group of dimension five over $\mathbb{F}_{11}$ it runs at the full charged arities $(M_2,M_3,M_4) = (1024,3,64)$, that is $7{,}077{,}888$ oracle queries per run, for nine hidden subgroups, most of them nonnormal and several meeting the center trivially; on the class-three filiform group over $\mathbb{F}_7$ it runs at $(324, 46656)$, or $362{,}797{,}056$ queries per run. Every run recovers $\log H$, every measured label law is exactly uniform on $K_d^\perp$, and every intermediate source equals $\rho_{H_d}$. On these small fields almost every block of $M_d$ labels contains a zero label, and the deterministic solver then returns a unit vector, so the full Ivanyos--Santha path supplies witnesses only where $p^{a_d}$ is comparable to $M_d$. Over $\mathbb{F}_7$ in class four the arity $B_3(2) = 531441$ puts the charged count at $1.25\cdot 10^{12}$ queries per run, beyond the simulation; class four over $\mathbb{F}_5$ is the zero-sum case $\kappa_4 = p-1$ of Theorem~\ref{thm:power-sde}(iii). The simulation is a finite exact check of exponential classical cost, not a coherent receiver, and it gives no asymptotic bound.
```

**Optional sentence, to insert before "Over $\mathbb{F}_7$ in class four" (same status):**

```latex
At the smaller count $G(\kappa_d,g_d)^{\lceil\log_2 t\rceil}$ that the deterministic solver consumes, $(M_2,M_3,M_4) = (1024,729,64)$, it runs on two class-four filiform algebras over $\mathbb{F}_7$ ($1{,}146{,}617{,}856$ queries per run with $m+1$ terminal samples) and recovers $\log H$ for the five subgroups tried on each.
```

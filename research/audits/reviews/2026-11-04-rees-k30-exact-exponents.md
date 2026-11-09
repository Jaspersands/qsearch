# Rees HSP, K30: exact instrument exponents (no floating point)

4 November 2026. AI-only pass (Claude Code, Opus 5.5). **Every claim below is AI-checked, pending
human review.** Not Lean. Nothing committed; `main.tex` untouched;
`research/reductions/rees_hsp_reduction.json` untouched.

Artifacts: folder `research/audits/reviews/2026-11-04-rees-k30-exact-exponents/`
(`run_commands.sh`, `agreement.py/.json/.out`, `compare.py/.json/.out`, `report_exact.json/.out`,
`n5_f5_exact.json/.out`, `n5_f5_exhaustive_exact.json/.out`, `pytest_fast.out`).

## 0. Answers

1. **Where the float came from.** `theorems/rees_circuit_general.py`, `instrument_semantics`
   (old lines 1064-1109; now `_instrument_semantics_float`, lines 1103-1137). For each top
   coordinate the instrument's (2b)-qubit gate block was turned into a complex matrix with
   `qiskit.quantum_info.Operator` (line 1116). The Kraus operators K_λ, the circulant symbol
   k_λ(z) and κ_λ(u) = p Σ_z k(z) conj k(z+u) were computed in complex floating point, and the
   exponent was `int(round(np.angle(kap)*p/(2*np.pi))) % p` (old line 1101, now 1129), i.e. the
   phase angle divided by 2π/p and rounded. The reason: the block contains two `qft{p}` gates,
   which are `UnitaryGate`s holding the float matrix exp(2πi jk/p)/√p, so Operator composition is
   inherently floating point. The rounding error is the accumulated error of the float QFT
   matrices: 6.8e-16 (Heis(F_3)), 7.53e-14 (n4(F_5), n5(F_5)), **2.72e-13 (n4(F_7), n5(F_7))**.
   The sparse module (`theorems/rees_circuit_sparse.py`, `SparseEngine.__init__`, line 139)
   and the arith backend (`theorems/rees_circuit_arith.py`, `instrument_semantics_arith`)
   call the same function, so all three backends had the same float step.
2. **Exact replacement (default).** `_instrument_semantics_exact` (lines 1213-1258) with helpers
   `_instrument_blocks` (1075-1089), `_cyc_conj` (1140), `_exact_permutation` (1145-1171),
   `_instrument_block_exact` (1174-1210). Each block is evaluated on the inputs |a = t, z = 0⟩
   as int64 coefficient vectors in Z[ζ_p] (canonical form of `rees_end_to_end_sim.cyc_canon`)
   times p^(-k/2), k = number of QFT gates:
   - a `qft{p}` / `qft{p}_dg` gate (the generator's `qft_gate`, F_p ⊕ 1 on padding) must sit on
     one qudit of the block and acts as |v⟩ ↦ p^(-1/2) Σ_w ζ^(±vw)|w⟩ by `np.roll` of the
     coefficient vector; any amplitude on padding at a QFT raises (exact zero test);
   - every other gate must be an exact permutation of basis states: X/CX/MCX/SWAP through the
     module's own `compile_ops` + `BitSim` (integer bit operations), or, for the arith backend's
     reduced macros, a `UnitaryGate` whose every entry is exactly 0.0 or 1.0 and which is a
     permutation matrix (an exact read, no tolerance);
   - leakage, completeness (Σ M_λ† M_λ = p^k I), circulant form and κ are integer identities in
     Z[ζ_p]; the exponent e is the unique index with Σ_z m(z) conj m(z+u) = p^(k-1) ζ^e
     (canonical forms compared entry by entry); no match, or more than one, is counted and raises.
   The info fields `leak`, `completeness_err`, `circulant_err`, `round_err` are, in exact mode,
   *mismatch counts* (all 0), with `mode: "exact"` and `qft_factors: [2, ...]`.
   The only float left anywhere near the instrument is `_qft_ok(p)`, a separate consistency
   check that the stored float matrix of `qft_gate` equals F_p ⊕ 1 to 1e-12; it is reported as
   `qft_matrix_float_consistency` and does not enter the exponents. The QFT gate itself is
   taken as the exact transform it was built to be, as the source module already does.
3. **Old path kept behind a flag.** `INSTRUMENT_EXPONENTS = "exact"` (line 1072);
   `instrument_semantics(cfg, d, exact=None)` (1092-1100) dispatches; `exact=False` or
   `INSTRUMENT_EXPONENTS = "float"` restores the old derivation. CLI: `--instrument {exact,float}`
   in `rees_circuit_general` (lines 1857-1861) and `rees_circuit_sparse` (lines 671-675).
   `instrument_semantics_arith` now passes `**kw` through (`rees_circuit_arith.py:700-704`).
   `instrument_exponent_agreement(cfg)` (1261-1277) runs both and compares every entry.
4. **The two paths are identical** on every exponent of every instrument of every backend
   checked (Section 1), and both equal the closed form e_λ(u) = λu mod p (QFT, a −= z, QFT†
   gives k_λ(z) = ζ^(−λz)/p, so κ_λ(u) = ζ^(λu)), asserted by a test on four configurations.
5. **Recoveries unchanged** (Section 2): every check row and every seeded-run record of the
   reruns is identical, field by field (timings dropped), to the 2026-11-03 float-path artifacts.

## 1. Agreement check (exact vs float, every entry)

`agreement.py` (commands in `run_commands.sh`). For each configuration and grade d it builds the
instrument circuit, partitions it into blocks, runs both derivations and compares
e_j[λ][u] for every top coordinate j, every λ and u. "gates" = gates in the instrument gate list.

| backend | instance | gates per grade | entries compared | mismatches | float round err (old) |
|---|---|---|---|---|---|
| original | Heis(F_3), c = 2 | d2: 10 | 9 | 0 | 6.8e-16 |
| original | n4(F_5), c = 3 | d2: 76, d3: 38 | 75 | 0 | 7.53e-14 |
| original | n4(F_7), c = 3 | d2: 180, d3: 90 | 147 | 0 | 2.72e-13 |
| original | n5(F_5), c = 4 | d2: 114, d3: 76, d4: 38 | 150 | 0 | 7.53e-14 |
| original | n5(F_7), c = 4 | d2: 270, d3: 180, d4: 90 | 294 | 0 | 2.72e-13 |
| arith (reduced) | Heis(F_3) | d2: 3 | 9 | 0 | 6.8e-16 |
| arith (reduced) | n4(F_5) | d2: 6, d3: 3 | 75 | 0 | 2.5e-16 |
| arith (reduced) | n4(F_7) | d2: 6, d3: 3 | 147 | 0 | 9.2e-16 |
| arith (reduced) | n5(F_5) | d2: 9, d3: 6, d4: 3 | 150 | 0 | 2.5e-16 |
| arith (reduced) | n5(F_7) | d2: 9, d3: 6, d4: 3 | 294 | 0 | 9.2e-16 |

**Total: 1350 exponent entries, 0 mismatches.** The exact path's leak, completeness, circulant
and monomial mismatch counts are 0 on every block, with k = 2 QFT factors per block.

## 2. Reruns with the exact path (default)

Two processes at a time, `nice -n 10`, one BLAS thread each, on a machine at load 70-240.
`compare.py` matches rows by instance (and seed) and compares all fields except timings.

- **Heis(F_3), c = 2** (`report_exact.json`, job `heis_f3`): 19/19 subgroups pass every check;
  38/38 seeded runs (2 seeds) recover log H. All 19 check rows and all 38 run records identical
  to `2026-11-03-rees-circuit-2/report_main.json`; merge proofs and bit-level records identical.
- **n4(F_5), c = 3** (job `n4_f5`): 9/9 subgroups pass; **18/18 seeded runs recover log H**. All 9
  check rows and all 18 run records identical to the old artifact; merge proofs and bit-level
  records identical. 377 s wall.
- **n5(F_5), c = 4, sparse** (`n5_f5_exact.json`, all nine subgroups, one seeded run each,
  `--no-gate-checks`: the merge gate proofs do not involve the instrument and were not rerun):
  9/9 subgroups pass every check (5 non-normal); **9/9 seeded runs recover log H** (2 940 oracle
  queries each). All 9 check rows and all 9 run records identical to the union of
  `2026-11-03-rees-circuit-3/n5_f5.json` and `n5_f5_b.json` (⟨e1⟩ appears in both old files and
  matches both). 4185 s wall, peak 2.08 GB.
- **n5(F_5), every label tuple and witness at grades 4 and 3** for H = 1 and H = ⟨e2⟩
  (`n5_f5_exhaustive_exact.json`): both pass; 1 952 500 + 77 500 merge cases each, all exact;
  both check rows identical to `2026-11-03-rees-circuit-3/n5_f5_exhaustive.json`. 1610 s wall.

Since the exponent arrays are equal as integer arrays, every later step (conditioning, label
laws, merges, readout, sampling with fixed seeds) is the same deterministic integer computation,
so identical results were expected; the reruns confirm it.

## 3. Tests

New tests in `tests/test_rees_circuit_general.py` (section "K30", lines 346-425):
- `test_exact_instrument_exponents_use_no_float[heis_f3, n4_f5]`: with `Operator`, `float`,
  `complex`, `round` (module globals shadowing the builtins) and `np.angle`, `np.exp`,
  `np.round`, `np.rint` all replaced by functions that raise, and `_qft_ok` stubbed, the exact
  path still derives every instrument; the exponents and the block state are integer arrays,
  the mismatch counts are Python ints equal to 0, and k = 2.
- `test_exact_exponents_equal_closed_form_and_float_path[heis_f3, n4_f5, n4_f7, n5_f5]`:
  exact exponents = (λu mod p) computed in integers, and 0 mismatches against the float path.
- `test_default_engine_uses_the_exact_path`: the default and the `Engine` use mode "exact";
  `exact=False` still gives the float path.
- `test_exact_path_reads_the_gate_list`: mutating the instrument to a += z flips the exponents
  to −λu mod p (both paths agree); dropping the inverse QFT is rejected by both paths.

Command (`pytest_fast.out`): `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10
python -B -m pytest -q -p no:cacheprovider` on every `tests/test_rees_circuit*.py` and
`tests/test_rees_end_to_end_{ext,sim}.py` (13 files):

```
1 failed, 359 passed, 25 skipped, 12 warnings in 1154.35s (0:19:14)
FAILED tests/test_rees_circuit_mono.py::test_wrong_merge_sign_detected
```

The failure is not from this change. `tests/test_rees_circuit_mono.py` and
`tests/test_rees_circuit_exhaustive.py` (with `theorems/rees_circuit_{mono,exhaustive}.py`) are
new files that another session created and was still editing during this run: the mono test
file was rewritten at 22:37 and 22:53, and the failing test name no longer exists in it (it is
now `test_broken_bennett_schedule_detected`, whose traceback was printed under the old name).
Neither file calls `instrument_semantics`. A rerun of that file after the edit
(`pytest_mono_rerun.out`): `15 passed in 36.36s`. So all instrument-related tests pass, including
the 8 new K30 tests and the existing `test_n4_instrument_gate_lists_are_complete_central_instruments`
(its `< 1e-9` asserts hold with exact counts 0), `tests/test_rees_circuit_arith.py` (which
monkeypatches `instrument_semantics` and checks old/new kernels are equal) and
`tests/test_rees_circuit_sparse.py`. Slow tests (`REES_SLOW=1`) were not rerun; the reruns of
Section 2 cover the same instances at full size.

## 4. Proposed replacement for the paper's float-rounding clause

The task brief cites "7.5e-14"; `grep -F "7.5" main.tex` finds no such number. The clause in
the paragraph "Gate-level control" (`docs/papers/rees-hsp/main.tex`, line 795) reads:

> The modules are simulated exactly in $\mathbb{Z}[\zeta_p]$ and composed through the tensor and
> Schur-product structure of Proposition~\ref{prop:descent}; the phase exponents of each
> instrument are read off its gate list in floating point and rounded (largest error below
> $10^{-13}$).

Note: "below 10^{-13}" holds for p = 3 and 5 (7.53e-14) but **not for p = 7**: the n4(F_7) run
the same paragraph cites gave 2.72e-13 (`2026-11-03-rees-circuit-2/report_n4_f7.json`,
`instrument.round_err`). The current clause is therefore inaccurate for the F_7 instance; the
replacement removes the issue.

Proposed sentence (**AI-checked, pending human review**):

> The modules are simulated exactly in $\mathbb{Z}[\zeta_p]$ and composed through the tensor and
> Schur-product structure of Proposition~\ref{prop:descent}; the phase exponents of each
> instrument are also read off its gate list exactly, by evaluating the gate list in
> $\mathbb{Z}[\zeta_p]$ with integer coefficients, each $\mathrm{QFT}_p$ gate taken as the
> exact transform, and they equal $\lambda u \bmod p$.

If a source is wanted, add
`(\file{research/audits/reviews/2026-11-04-rees-k30-exact-exponents.md})` after "exactly".
Integration-log item K30 (`2026-11-02-rees-integration-log.md`, line 594) can then be closed:
the clause it added is no longer needed.

## 5. What this does not show

- The QFT gate is identified as exact F_p ⊕ 1 by its construction (`qft_gate`); Qiskit stores
  it as a float matrix, which is checked against F_p ⊕ 1 only to 1e-12. A finite-gate QFT
  synthesis is a separate matter (the third backend's error analysis).
- Nothing asymptotic; only the configurations listed above were run.

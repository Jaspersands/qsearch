# Independent review: coherent-label class-four circuit over F_7 (2026-11-04)

AI review (Claude), pending human review. Targets: `theorems/rees_circuit_coherent_c4.py`,
`tests/test_rees_circuit_coherent_c4.py`, and the sentence of `docs/papers/rees-hsp/main.tex`,
paragraph "Gate-level control", that begins "The class-four circuits over $\mathbb{F}_7$". I formed
the verdicts below from the code, the raw run logs in
`research/audits/reviews/2026-11-04-rees-circuit-coherent-c4/` and my own checks. Only after that did
I grep the author's report for specific terms. No existing file was edited and nothing was
committed. My scripts are in the session scratchpad
(`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/`:
`count_stream.py`, `indep.py`, `mutants.py`, `paths_mut.py`, `state_mut.py`, `state_mut2.py`,
`hom.py`, `children.py`). They run with `PYTHONPATH=. /opt/anaconda3/bin/python` from the repo root,
in one process with peak memory under 0.2 GB.

**Verdict.** I found no Error. Every number in the sentence reproduces. One Gap: the "linear
algebra" source check does not cover the preparing transforms or the address register after
evaluation. Two of my mutants pass it, and only the basis-path check catches them. Seven
Imprecisions, mostly about coverage wording: in several state checks the label support is only {0}.

## Claim-by-claim

| Claim in the sentence | Status | Evidence |
|---|---|---|
| kappa_d = 2, 3, 2 | correct | gcd(4,6), gcd(3,6), gcd(2,6); `test_config_kappa_and_arities` |
| arities 3, 6, 10 (instead of 3, 7, 7) | correct | (g+1)(g+2)/2 with g = 1, 2, 3; CW arity g*kappa+1 = 3, 7, 7 |
| 20566 qubits | correct | stream count: 20566 distinct wires used = max wire + 1 = `ts.nw` |
| 83492540 gates excl. oracle and 3330 transforms | correct | every one of the 77806 macros expanded on its real wires, nothing stored: x 14483932, cx 48403448, ccx 20079212, swap 525948; 3330 qft/qft_dg calls, 720 oracle calls, 1 measure; per-component sums match `counts()` |
| 3330 transforms | correct | 180*(11+2) + 60*(10+4) + 10*(8+6) + (5+5) = 3330, includes inverse and readout transforms |
| blocks: all label triples at grade 4 | correct (sampled x, q) | log: 343*4096 inputs; my independent checker, 343*32 fresh inputs: 0 failures |
| all rank<=1 tuples and one per row space at grade 3 | correct | 941185 = 1 + 941184 rank-1 6x2 matrices; 6884860 = 1 + [6,1]_7 + [6,2]_7; I checked that the representatives are RREF of the g x M matrix |
| samples at grade 2 | correct | log; my checker: 6144 fresh inputs, 0 failures |
| source "computed ... by linear algebra rather than simulated" | correct for the evaluation macros and identity fibre; see **G1** | |
| merged outputs = rho for 8 of 9 subgroups | correct as executed; wording, see **I1** | `state_runs.log`, `state_wide.log` |
| seeded runs, two seeds each, recover log H for the eight | correct | 16/16 in log; I added 3 fresh-seed runs (<e3> seed 5, <e2,e5> seed 6, <e1+e2+e5> seed 7): all recovered |
| whole circuit checked on basis paths only | correct | 512 paths, pass |

## Independent checks run

1. **Gate and qubit counts, streamed** (`count_stream.py`, 26 s, 0.16 GB). I expanded every macro of
   the assembled terminal sample with `add_product_ops`/`add_scaled_ops` on its actual wires and
   counted the gates without storing them. The result is exactly 83492540 gates and 20566 wires,
   with only X/CX/CCX/SWAP gates. Qubits by role: oracle outputs 10800, top addresses 5940, Q
   registers 1800/240/15, labels 540/360/90, pool 752, w 15, arithmetic ancillas 14.
2. **Independent witness and block checker** (`indep.py`). I wrote my own bit simulator
   (uint8-packed) and my own degree-4 BCH series built from the structure tensor. Before using
   it, I checked it against `law.mul` at d = 2, 3, 4 and against `L_law` on 5000 random pairs:
   equal. The witness test is written directly from s != 0, s_i < p and
   sum_i s_i^d lambda_i = 0. It uses no canonical-witness reference. The check needs only the
   wire layout of the blocks.
   - U_SDE: grade 4, all 343 triples: 0 invalid. Grade 3: 131072 uniform tuples and 32768
     structured ones (zero columns, low rank, repeated columns, zero prefixes): 0 invalid.
     Grade 2: 32768 uniform and 8192 structured: 0 invalid. In every case the labels were
     restored and the workspace was clean.
   - Whole blocks (the witness from my own run of U; children compared with my BCH of
     x_i * (-s_i^deg q)): grade 4 10976, grade 3 24576 and grade 2 6144 inputs, 0 wrong
     children, 0 invalid witnesses, io unchanged and clean workspace.
3. **New mutants.**
   - Grade-2 block mutants `g_sign`, `skip_bennett`, `skip_ctrl_inv`, `skip_sde_inv`: all
     rejected by my checker (the author's block mutants are at grade 4 only).
   - Source mutants M1 (one `source_qft` deleted) and M2 (`a_0 += a_5` inserted after the last
     uncompute of the first source): **both pass `source_exact_check`** (G1). M3 (the second oracle
     call writes the first output register) is rejected by `oracle_wiring`.
   - State-check mutants: a constant witness e_1 and a rotated circuit witness are rejected at
     every grade with nonzero labels. A wrong source (the coset state for <e2,e5> with targets
     for <e2>) is rejected at grade 4 by `equals_indicator`. So the state comparison is not
     vacuous. With invalid witnesses, though, `eng.merge` usually raises (28 of 30) instead of
     returning a wrong state.
4. **Row-space invariance** of the grade-3 circuit witness (the justification for checking only
   RREF representatives). On 6860 random label matrices L and random g in GL_2(F_7), the circuit
   gives the same witness on L and on Lg (6860/6860). This is sampled support only.
5. **Exact homomorphism** (`hom.py`). For all four points s, E_s is a Lie-algebra homomorphism on
   all 11 x 11 pairs of basis vectors: (T_cover[i,j] E_s = [E_s e_i, E_s e_j]_L). Because both laws
   are the BCH laws of these tensors (checked on samples above), the group homomorphism that
   `source_exact_check` only samples follows exactly. I also recomputed dim K = 11 - rank with my
   own elimination for all nine subgroups (0, 1, 1, 2, 4, 5, 1, 7, 9), and it matches
   |exp(h~)| = 7^dim.
6. **Children of the symbolic proof** (`children.py`). `prove_controlled_merge` replays only child
   0. I checked that, at d = 2, 3, 4, the programs of children i >= 1 are exactly the child-0
   program with x_i -> x_0 and S_i -> S_0, so the symbolic proof covers every child.
7. The default test file: 23 passed, 3 skipped (slow), 28.5 s.

Monkey-patching. `kappa_dispatch` swaps exactly `sde_circuit`, `sde_reference` and
`coherent_arity` and always restores them. Every c4 path that reads them runs inside the dispatch:
`sde_check`, `K.block_check` through `chunked_block_check`, `K.assembled_basis_paths`, and the
construction of `MergeBlockK`/`TerminalSampleK`. `CircuitWitness`, `prove_controlled_merge` and
`block_structure` never read them. The `wrong`-degree mutant patches `K.sde_circuit_k` inside a
`try/finally`. I found no path that silently uses an unpatched or stale function.
`test_dispatch_restored_and_fourth_backend_still_refuses` passes.

The seeded runs do use the circuit's witnesses: `CircuitWitness` runs the emitted U_SDE gate list
bit-level. The merges are then the SparseEngine's exact BCH translations, not the block gate lists
run on states.

## Findings

### Errors

None.

### Gaps

**G1. The source check does not cover the transforms that prepare the source, or the address
register after evaluation.**
Location: `source_exact_check` (c4 lines 335-387). Its loop accepts every `("qft", ...)` item
without checking anything about it (`elif it[0] != "qft"`). It never checks that the forms of
the address registers `a` stay the identity, and the final check covers only `w`. The author's
report (section 3.6 item 1) says the replay covers "QFT_7 on 11 address registers", which the code
does not do.
Evidence: mutant M1 (one source transform deleted, so one address coordinate stays |0>) and mutant
M2 (a_0 += a_5 after the last uncompute, a permutation of the address register before the
instrument) both give `passed = True`. `assembled_basis_paths` (n = 16) catches M2 (`children_and_Q:
False`), but it catches M1 only by raising `KeyError (781, 782, 783)`, not by returning a failure.
So the coset state that the state checks and runs start from is tied to the emitted circuit through
three pieces: the evaluation forms (exact), the identity fibre (exact) and the 512 basis paths
(sampled, and crash-based for M1). `run_seeded` also ignores the source-check result (it takes
`top, _, _ = eng.source(inst)`).
Fix: in `source_exact_check`, require that, before the first evaluation macro, there is exactly one
`qft` on each address register and no other qft. Also require that every address register's final
form is its unit vector and that the oracle output registers are distinct and fresh. Make
`assembled_basis_paths` return `passed: False` when a register was never loaded. Make `run_seeded`
assert `eng.source_checks[inst.name]["passed"]`.
LaTeX: covered by the replacement below ("the preparing transforms and the address register are
checked only on the basis paths").

### Imprecisions

**I1. Coverage of the state checks is overstated by "all label tuples at grade four, all or sampled
at grades three and two".**
Evidence (`state_runs.log`, `state_wide.log`):
- At grade 4, three of the eight subgroups (Z(G), <e2,e5>, gamma_3) have label support {0}, so
  "all label tuples" is just the zero tuple.
- At grade 3, "all" applies only to Z(G) and <e2,e5> (117649 tuples, in `state_wide`) and to
  gamma_3 (support {0}, 1 tuple). The other five use 64 or 1024 samples out of 49^6.
- At grade 2 every subgroup is sampled (64 or 1024 tuples), so "all" never occurs there.
- The ninth subgroup gamma_2 gets only the source check (slow test); it gets no state check and no
  run.
- "Merged outputs" are computed by the exact measured-label SparseEngine using circuit witnesses.
  They are not the block gate lists run on states.

Fix: state this split in the sentence. See the replacement.

**I2. The qubit numbers in the same sentence come from different conventions.** The parenthetical
"$16302$ qubits" for the measured generator excludes the $3b+5=14$ arithmetic ancillas:
`measured_counts` gives 16316, and the test comment says "main.tex: 16302 (+ 3b+5 ancillas)". The
20566 includes its 14 ancillas. Also, 10800 of the 20566 qubits are oracle output registers, and no
register is reused. The class-three sentence just before it states the analogous "($648$ of them
oracle outputs; no reuse)".
Fix: see the replacement.

**I3. The homomorphism is only sampled, although an exact check is cheap.** `source_exact_check`
(iii) samples E_s(x*y) = E_s(x)*E_s(y) on 4096 pairs (256 in the tests). My basis-bracket check
(item 5) proves it for this instance in under a second, given that both laws are BCH laws.
Fix: replace (iii) with the 11 x 11 bracket check plus an assertion that the laws are BCH, or keep
the sample and add the exact check. The report's "only sampled here" can then be dropped.

**I4. One "must be rejected" mutant is not an incorrect circuit.** The grade-3 `omega_min` mutant
produces only valid witnesses (0 invalid out of 4096 by my checker). `sde_check` and `block_check`
reject it only because its witness differs from the canonical reference. The mutant list therefore
mixes correctness mutants (alpha, beta: about 30% invalid witnesses) with a mutant that only breaks
agreement with the reference.
Fix: label `d3_sde_omega_min` as "canonical-rule mutant" in `block_mutants` and in the report.

**I5. The block statement is weaker than what is proved, and the scope of the proof is unstated.**
`prove_controlled_merge` replays child 0 only. Item 6 above closes that: the other children are
renamings of child 0. With the exhaustive U_SDE check at grade 4 (343 triples, witness valid,
labels restored, clean workspace) and the footprint checks, the grade-4 block is proved on all
canonical inputs, not only on sampled (x, q). This is not an error.
Fix (optional): add the renaming check to the module, then say "proved on all inputs at grade four".

**I6. The runs are not from oracle access.** `run_seeded` builds the top source from `inst.log_h`
(through the kernel computation in `SourceFromKernel`) and reports `oracle_queries` as a nominal
count. The report heading is "Seeded runs from oracle access", and it gives "6 480 oracle queries".
The paper sentence makes no such claim, so this affects only the report and the JSON.
Fix: rename the field to `nominal_oracle_calls` and drop "from oracle access" in the report.

**I7. Two parts of the basis-path check are vacuous or fail by crash.** `assembled_basis_paths`
skips the oracle, so "oracle outputs end 0" holds trivially. A deleted preparation transform makes
it crash (`KeyError`) instead of fail (G1). `state_checks` records `label_law_uniform` as "all
positive probabilities are equal", but it does not compare the support with K_d^perp (the
class-four F_5 sentence of the paper claims uniformity on K_d^perp, though not for this instance).
Fix: drop `oracle_output` from the clean set, or note that it is vacuous. Compare
`allowed` with `G.allowed_labels(cfg, log_h, d)`.

## Proposed LaTeX replacement for the sentence

Replace the text from "The class-four circuits over $\mathbb{F}_7$" through "on classical basis
paths only." with:

```latex
The class-four circuits over $\mathbb{F}_7$ ($16302$ qubits per terminal sample, plus the $3b+5=14$ arithmetic ancillas) are generated and counted; a coherent-label version, \file{theorems/rees_circuit_coherent_c4.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-coherent-c4.md}; finite computation, AI-checked, pending human review), uses the circuits of Lemmas~\ref{lem:coherent-quadratic-sde} and~\ref{lem:coherent-power-sde} at grades four, three and two ($\kappa_d = 2, 3, 2$; merge arities $3$, $6$ and $10$ instead of $3$, $7$ and $7$), so that one terminal sample uses $20566$ qubits ($10800$ of them oracle outputs; no reuse) and $83492540$ gates excluding the oracle and $3330$ exact transforms; its merge blocks equal the right translation by $-\delta_s(\sigma(q))$ with clean workspace on all label triples at grade four and all rank-at-most-one label tuples and one tuple per row space at grade three (sampled targets and $q$), and on samples at grade two. The source state is taken to be the coset state of the identity fibre of the oracle key, which is computed by linear algebra from the evaluation program rather than simulated (the transforms that prepare the source and the address register are checked only on the basis paths below). From it, the exact measured-label simulation with witnesses computed by the circuit gives merged outputs equal to $\rho_{H_{d-1}}$ for eight of the nine hidden subgroups. These are all label tuples at grade four (only the zero tuple for three of the eight), all label tuples at grade three for three of them (only the zero tuple for one) and sampled tuples for the other five, and sampled tuples at grade two. Seeded runs of this simulation (two seeds each) recover $\log H$ for these eight; the whole circuit is checked on classical basis paths only.
```

If G1's fix lands, the parenthesis "(the transforms that prepare the source ... below)" can become
"(including the transforms that prepare it)".

## Claim gates

`coherent_receiver_implemented`, `general_instances`, `qft_synthesised`,
`whole_circuit_amplitude_simulation`, `source_from_gate_list_on_all_addresses`,
`independent_review` and `speedup_claim_allowed` are False in `STATUS`, and they should stay False.
This review is AI-only. It does not justify setting `independent_review` to True.

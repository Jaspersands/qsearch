# Review: fifth backend `theorems/rees_circuit_coherent_k3.py` (n4(F_7), kappa_3 = 3)

Date: 2026-11-04. Independent AI review, pending human review. The verdicts below were formed
before reading the author's report. Edits: none to existing files. Commits: none. Network: none.
Python: `/opt/anaconda3/bin/python`, one process, `nice -n 10`.

Targets: `theorems/rees_circuit_coherent_k3.py`, `tests/test_rees_circuit_coherent_k3.py`, and the
sentence of `docs/papers/rees-hsp/main.tex`, paragraph "Gate-level control", that begins
"A fifth backend".

**Counts: 0 Error, 2 Gap, 5 Imprecision.** Every number in the paper sentence was reproduced.
No finding invalidates the sentence. Two other sentences of the same paragraph are now stale
(I1, I2), and the sentence leaves out the scope of its state checks (I3).

## 1. What was checked independently, and the results

Scratch scripts are in
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/`
(`rev1.py` to `rev7.py`).

| Claim | Independent check | Result |
|---|---|---|
| 4832806 gates, 1629 qubits, 230 transforms | `rev1.py`: each Macro of `TerminalSampleK.items` is re-emitted with `add_product_ops` / `add_scaled_ops` on its **actual** wire arguments, without the per-(kind, coeff) count cache that `prog_counts` uses; gates are counted by type and every wire touched is recorded | 840220 X + 2799560 CX + 1162204 CCX + 30822 SWAP = **4832806**, equal to the reported total. Non-gate items: 200 `qft` + 30 `qft_dg` = **230**, 54 oracle calls, 1 measurement. All 1629 wires are touched, the largest index is 1628. A hand tally gives 18·(21+36+3) + 6·(18+6) + 12 + 14 + 12 + 367 = **1629** |
| kappa_3 = 3 witness is valid | `rev2.py`: the grade-3 coherent SDE gate list (`CircuitWitness` on the remapped block) runs on all 343 triples, and each witness is checked from the definition: s != 0, s_i in [0,7), sum_i s_i^3 lambda_i = 0 mod 7 | 343/343 valid |
| The witness is the canonical triangular one | `rev2.py`: an a = 1 solver written from scratch from the paper's text (first dependency with last entry 1, my own coset table g^nu·{1,6}, the contraction found by brute force over [0,7)^4 in lex order, the least cube root, u = 1) | Contraction ((1,0,5),(0,2,6)), the same as the module's. Circuit witness equals my solver on **343/343**. Witness values {0,1,3}; K = 0 on 175 triples, K = 1 on 168 |
| The block is the right translation by -delta_s(sigma(q)) | `rev6.py`: an independent class-3 BCH (X+Y+[X,Y]/2+[X,[X,Y]]/12-[Y,[X,Y]]/12 over the cover tensor) with my own witness and G_j = -s^deg(j) q_j, run on 4000 inputs of the grade-3 block gate list, including rank-deficient ones | All outputs equal, workspace clean. `law.mul` equals my BCH on 20000 random pairs |
| all 7^3·7^6 (label triple, q) | the artifact `all_lambda_q.json` (40353607 inputs, pass) was produced after the module's last edit. I re-ran three slices of 2^20 inputs each (start, middle, end) with the current code | pass |
| Mutants: wrong coset flag, wrong root, wrong constant | `rev3.py`: (i) swap both coset flags everywhere, (ii) swap them only on zeta (back substitution), (iii) swap them only on the first delta, (iv) keep the largest cube root, (v) beta_2 6->5, (vi) alpha_2 5->4, (vii) beta_1 2->3, (viii) S <- 2s | `block_sampled(n=512)` and `sde_exhaustive.witness_equals_canonical` catch all eight. Mutants (i)-(iii) and (v)-(vii) give **invalid** witnesses (72, 96, 96, 48, 48, 24 of 343), which `equation_holds` also catches without any reference. (iv) and (viii) give valid but non-canonical witnesses (2 is a cube mod 7), so only the reference catches them, as it should |
| Dispatch (a) | `rev5.py`: an exception inside `MergeBlockK` (sde_mutate at kappa 2) leaves the three names restored. Nested `kappa_dispatch` gives back the outer (mutated) hook and then the originals. `C.MergeBlock(cfg, 3)` outside the dispatch refuses. `C.block_sampled` on a kappa-3 block outside the dispatch raises (`canonical_witness_k2_batch`), so there is no silent fallback. `TerminalSampleK.blocks` = {2: CoherentSDEK2, 3: CoherentSDEKappa}, and every grade-3 merge of the terminal sample is a remap of `blocks[3]`. The K3 tests followed by four fourth-backend tests in one pytest process: 23 passed | pass |
| Runs use circuit witnesses (c) | `rev4.py`: spies on the witness callables and on `Engine.merge` during `run_coherent_witness` for <e2> and Z(G), seed 20261103 | Every merge (48 at grade 3, 8 at grade 2 per run) uses the `CircuitWitness` output. Every witness is valid from the definition, every merge output equals `stage_indices` of H_(d-1), and both runs recover. No classical witness path exists in `run_coherent_witness` |
| Grade-2 witness (extra) | `rev7.py`: the grade-2 coherent SDE gate list on 32768 6-tuples in F_7^2, a quarter on a line and some with zero or repeated columns, checked from the definition | all valid |
| Current-code rerun | `python -m theorems.rees_circuit_coherent_k3 --parts counts,proofs,blocks,paths,state --per-label 1024 --state-instances 0,3`, and the default pytest file (19 passed, 1 skipped, 26 s) | everything passes |

Things that rule out vacuity (b):

- `sde_exhaustive` checks `equation_holds` from s^d without the reference.
- `state_checks` recomputes witness validity from the definition and takes witnesses only from
  the gate list.
- `block_check`'s BCH reference `law.mul` shares `bch_nodes` with the circuit. Its independence
  comes from `prove_controlled_merge`, which replays against `sym_bch_reference`, and is
  confirmed by my `rev6.py`.
- The canonical reference shares `kappa_constants` with the circuit. Those constants are
  asserted by `contraction_valid` and match my brute force.

## 2. Findings

### Gap G1: `run.json` was produced by an earlier version of the module

- **Location:** `research/audits/reviews/2026-11-04-rees-circuit-coherent-k3/run.json` and
  `run.log`. The author's report (line 138) calls it the "default CLI with `--per-label 1024`".
- **Evidence:**
  - `run.json` finished at 15:15:08 after `"seconds": 730.0`, so it started at about 15:02:58.
    `theorems/rees_circuit_coherent_k3.py` was last modified at 15:08:35.
  - Its recorded `args` lack `max_all`, `state_instances` and `all_lambda_q`, which the current
    CLI always writes. It therefore came from an older parser.
  - Only `state_wide.json` (started at about 15:08:45) and `all_lambda_q.json` (started at about
    15:15:32) postdate the last edit.
  - Three things in the sentence rest only on that older file: the 12 seeded runs, the
    state-check rows for `<e1+e2,e3>` and `gamma_2` (which `state_wide` skips), and the
    grade-3 `sde_exhaustive` and `proofs` entries.
- **What I re-established with the current code:**
  - counts, proofs, `sde_exhaustive`, blocks (per_label 1024) and paths: all pass, with
    identical numbers;
  - state rows for `<e2>` and `<e2,e4>`: pass;
  - runs for `<e2>` and Z(G), seed 20261103: recovered.

  The results are very likely unchanged, but the artifact's provenance is wrong.
- **Fix:** regenerate `run.json` and `run.log` with the current CLI (command in the report,
  line 296, about 12 min), or record the module version that produced them.

### Gap G2: the default tests do not exercise kappa = 3 in a state check, and miss two mutants

- **Location:** `tests/test_rees_circuit_coherent_k3.py`.
- **Evidence:**
  - `test_state_checks_small_support_instances` uses only `insts[5]` (gamma_2). Its grade-3 label
    support is {0}, so the kappa-3 solver runs only on the all-zero triple, which gives
    s = (1,0,0). The only state check with all 343 triples is `@slow`.
  - No test mutates a coset flag, the one-hot class flags that select alpha/beta. The
    alpha/beta mutants change constants, not flags.
  - Whole-terminal-sample counts are checked only through `prog_counts`, which counts one
    emitted instance per (kind, coeff). Only the grade-3 *block* is compared with its emitted
    list (`test_gate_counts_equal_emitted_list`).

  My checks (`rev1.py`, `rev3.py`) show the code is right on all three points. The suite as
  written would not catch a regression in them.
- **Fix:**
  1. Run `state_checks` on `insts[7]` (Z(G)) or `insts[3]` by default for grade 2, and on
     `insts[0]` at grade 3 only. The 343 triples reduce to 24 distinct merges and take about
     15-20 s.
  2. Add a coset-flag-swap mutant: subclass `CoherentSDEKappa._class_flags` to return `f[::-1]`
     and monkeypatch `K.CoherentSDEKappa`. Assert that `block_sampled` fails **and** that
     `sde_exhaustive(...)["equation_holds"]` is False.
  3. Add a streaming emitted-list count of `TerminalSampleK` (`rev1.py`, about 1.5 s) that
     asserts 4832806.

### Imprecision I1: the K2 artifact sentence is stale (affects main.tex)

- **Location:** main.tex, the paragraph after Lemma `lem:coherent-quadratic-sde`: "...it is
  wired only into the fourth backend above, at its two instances."
- **Evidence:** the fifth backend also wires `CoherentSDEK2` at grade 2 of n4(F_7), at
  (p, a) = (7, 2). Test `test_config_kappa_and_arities` asserts
  `isinstance(blocks[2].sde, CoherentSDEK2)`. That artifact is checked exhaustively only at
  a = 2, p in {3,5}, so at (7, 2) the circuit is only sampled. This is consistent with "the
  grade-two block on samples".
- **LaTeX fix:** replace
  `it is wired only into the fourth backend above, at its two instances.` with
  `it is wired only into the fourth backend above, at its two instances, and into the fifth, at grade two of the class-three filiform algebra over $\mathbb{F}_7$ ($a=2$, $p=7$, checked there on samples).`

### Imprecision I2: a later parenthetical omits the fifth backend's grade-two lemma (affects main.tex)

- **Location:** the same paragraph, "(...; the fourth backend above uses the first two, at
  $\kappa_d\le2$, and the fifth uses the third at $\kappa_3=3$)".
- **Evidence:** the fifth backend uses Lemma `lem:coherent-quadratic-sde` at grade two as well.
- **LaTeX fix:** `and the fifth uses the third at $\kappa_3=3$ and the second at grade two)`.

### Imprecision I3: the sentence does not give the scope of the state checks (affects the target sentence)

- **Location:** the target sentence, "with witnesses computed by the circuit every merged output
  equals $\rho_{H_{d-1}}$ (all label tuples at grade three, all or sampled at grade two) and
  seeded runs recover $\log H$ for six hidden subgroups, four of them non-normal."
- **Evidence:**
  - The state checks cover **nine** subgroups, five of them non-normal (`run.json` and
    `state_wide.json`). The sentence names only the six of the runs, and can be read as six
    for both.
  - "All label tuples" means all tuples over the positive-probability label support. That is
    all 343 triples for `<e2>`, `<e1>`, `<e1+e3>`, `<e2,e3>` and trivial. For `<e2,e4>`,
    `<e1+e2,e3>`, gamma_2 and Z(G) the support is {0}, so only the zero triple is checked.
- **LaTeX fix:** see I4, which rewrites the same clause.

### Imprecision I4: "seeded runs" are measured-label runs, not simulations of the circuit (affects the target sentence)

- **Evidence:** `run_coherent_witness` runs the Engine's measured descent. It uses exact label
  laws and sampled labels, takes the witness of every merge from the coherent SDE gate list,
  and draws m+4 = 8 terminal samples, with two seeds per subgroup. It is the classical shadow
  given by deferred measurement (module docstring), not an execution of the assembled
  1629-qubit circuit. The fourth-backend sentence explains the deferred-measurement argument,
  so this is mild.
- **LaTeX fix (covers I3 and I4):** replace
  `and with witnesses computed by the circuit every merged output equals $\rho_{H_{d-1}}$ (all label tuples at grade three, all or sampled at grade two) and seeded runs recover $\log H$ for six hidden subgroups, four of them non-normal.`
  with
  `and, with witnesses computed by the circuit, every merged output equals $\rho_{H_{d-1}}$ for nine hidden subgroups, five of them non-normal (all label tuples of positive probability at grade three, all or sampled at grade two), and seeded runs of the measured-label simulation with these witnesses (two seeds each) recover $\log H$ for six of them, four non-normal.`

### Imprecision I5: 648 of the 1629 qubits are oracle output registers (optional)

- **Evidence:** the roles from `ts.counts()["qubits_by_role"]`: oracle_output 648
  (18 sources × 3 calls × 12 bits), address_top 378, block_workspace_pool 367, Q_grade2 108,
  label_z_grade3 54, label_z_grade2 36, arith_ancilla 14, evaluation_w 12, Q_grade1 12. There
  is no qubit reuse. "Excluding the oracle" applies to gates, not qubits. This follows the
  fourth backend's convention (1198 qubits), so it is consistent, but a reader may take it
  otherwise.
- **LaTeX fix (optional):** `$1629$ qubits ($648$ of them oracle outputs; no reuse)`.

## 3. Verdict on each item of the paper sentence

| Item | Verdict |
|---|---|
| kappa_3 = 3; Lemma power-SDE at grade 3; Lemma quadratic-SDE at grade 2 | correct. The circuit uses the "power" stop test of the lemma, and the reference uses the general test; they agree on all 343 triples |
| merge arities 3 and 6 instead of 4 and 5 | correct (`G.Config` default {2: 5, 3: 4}) |
| 1629 qubits, 4832806 gates, excluding the oracle and 230 transforms | correct, reproduced from the emitted gate lists (I5 optional) |
| grade-3 block = right translation by -delta_s(sigma(q)), clean workspace, all 7^3·7^6 (sampled targets) | correct, with one random child triple per (lambda, q). The remaining child coverage comes from the symbolic replay over F_7[s, q, x] |
| grade-2 block on samples | correct (4096 structured samples) |
| merged outputs = rho_{H_{d-1}} with circuit witnesses | correct, for nine subgroups (I3) |
| seeded runs recover log H, six subgroups, four non-normal | correct: 12 runs, 2 seeds each, on <e2>, <e1>, <e1+e3>, <e2,e4>, Z(G) and trivial. These are measured-label runs (I4), and their artifact predates the final code (G1) |

No claim gate is affected. `coherent_receiver_implemented`, `general_instances` and
`speedup_claim_allowed` stay False.

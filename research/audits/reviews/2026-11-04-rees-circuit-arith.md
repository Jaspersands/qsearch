# Rees HSP: a poly(log p) arithmetic backend for the gate-level circuit generator

4 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
**Every claim below is AI-checked, pending human review.** Labels as in
`2026-11-03-rees-circuit-2.md`: **[exact]** = complete finite computation in integer or
permutation arithmetic; **[proof-by-computation]** = exhaustive check covering ALL inputs of
the stated finite set; **[float]** = floating point, tolerance 1e-9; **[sampled]** = exact on a
stated random subset only; **[argued]** = reasoning, not machine-checked.

Files written (and nothing else): `theorems/rees_circuit_arith.py` (new),
`tests/test_rees_circuit_arith.py` (new), this report, and the folder
`research/audits/reviews/2026-11-04-rees-circuit-arith/` (JSON artifacts, logs,
`run_commands.sh`). Read-only imports: `theorems/rees_circuit_general.py`,
`theorems/rees_circuit_sparse.py`, `theorems/rees_end_to_end_sim.py`. No existing file was
edited (the hook is a context manager in the new module that rebinds module attributes for the
duration of a block and restores them); `main.tex` untouched; nothing committed or pushed.

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_arith.py            # 39 passed, 6 skipped, ~11 s
REES_SLOW=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_arith.py -k slow   # 6 passed, ~75 s
sh research/audits/reviews/2026-11-04-rees-circuit-arith/run_commands.sh     # all artifacts, ~4 min
```

The existing suites `tests/test_rees_circuit_general.py` and `tests/test_rees_circuit_sparse.py`
still pass unchanged (79 passed, 15 skipped).

## 0. Answers

1. **Built.** `ArithBuilder` (a subclass of `rees_circuit_general.Builder`) emits the same
   macros (`add_scaled`, `add_product`, `swap`, `qft`, `oracle`) with the same semantics and
   the same macro records `(kind, qudits, coeff mod p, start, end)`. The value-controlled
   increments are replaced by standard reversible binary arithmetic: a Cuccaro ripple-carry
   adder, a modular adder with comparison and conditional subtraction, constant
   multiplication by shift-and-add of doubled constants, modular doubling, and a controlled
   modular multiply-accumulate. Gate set: X, CX, CCX, SWAP (no MCX with more than two controls
   is ever emitted). Ancillas: one register of 3b+5 qubits per circuit, b = ⌈log2 p⌉,
   returned to 0 by every macro on every basis input.
2. **Correctness [proof-by-computation].** For p ∈ {3, 5, 7, 11, 13}, every coefficient
   1..p−1 and both macro kinds (2·(p−1) macro instances per p, 68 in all), the emitted gate
   list was run bit-level on ALL 2^(kb) words of its k qudits (k = 2 or 3) with ancilla 0:
   canonical map, padding behaviour, clean ancillas, operands never targeted, bijectivity.
   The building blocks (adder, modular adder, doubling, comparator) were checked separately
   on all their inputs. All pass.
3. **Integration [exact].** With the new backend, the unchanged pipeline (source from its gate
   list, instrument semantics, `prove_merge`, `merge_bitlevel`, `SparseEngine`,
   `check_instance_sparse`, `run_algorithm_sparse`) reproduces the Heis(F_3) (19 subgroups)
   and n4(F_5) (9 subgroups, 5 non-normal) recoveries. **The outputs equal those of the old
   backend state by state**: same source states, supports and flags; same top-grade label laws
   and branches; identical instrument phase exponents; identical full `check_instance_sparse`
   rows (all grades, all merge cases); identical seeded runs (2 seeds per subgroup, same
   samples, same recovered log H); and identical merge permutations at bit level (n4(F_5)
   grade 2 on all 9 765 625 inputs per s).
4. **Scaling [exact counts, not simulated].** One multiplication (`add_product`) costs exactly
   **40b²+2b Toffoli (CCX) gates** and 134b²+50b−4+(20b−4)·hw(p)+4H gates in all, where
   H = Σ_{i<b} hw(coeff·2^i mod p) ≤ b², hence **at most 158b²+46b−4 gates**. Fitted
   log-log slope against b over p = 101, 1031, 65537, 2^61−1: 2.02 (total), 2.00 (CCX); for
   whole merges 2.00–2.01. At the 61-bit prime 2^61−1 one multiplication is 590 476 gates and
   a class-four merge (n5, d = 4) is 5.7·10^7 gates on 2 994 qubits.
5. **Still missing.** QFT_p is still one exact b-qubit unitary (no poly(log p) QFT_p, the
   subject of thm:uniform-compilation(iii)); no coherent receiver; no oracle cost; no noise; no
   depth optimisation; correctness for p > 13 is [sampled] plus [argued], not exhaustive.
   All claim gates stay false (section 7).

## 1. Construction

Module: `theorems/rees_circuit_arith.py`. Encoding unchanged: qudit = b qubits, value
Σ_i q_i 2^i, words ≥ p are padding. Ancilla register `arith`, layout Y[b], P[b], r[b], e, c0,
f, g, h.

| block | gates | CCX |
|---|---|---|
| Cuccaro adder (B, e) += A on b bits, carry XORed into e | 6b+1 | 2b |
| subtraction (two's complement: X on (B,e), add, X) | 8b+3 | 2b |
| modular add t += y (t, y < p): add y, −p, CX e→f, +p ctrl f, −y, CX e→f, +y, clear f | 34b+12+4hw(p) | 10b |
| comparison g ^= [t < p] (−p, CX e→g, +p) | 14b+5+2hw(p) | 4b |
| doubling r → 2r mod p (rotate with b SWAPs, −p, CX, +p ctrl f, CX r_0→f, X f) | 15b+7+4hw(p) | 4b |

Macros (all [argued] from the block structure, and the closed forms below match the counted
gates exactly for 108 (p, coeff, kind) cases including the five primes of the table, 2^31−1
and 1 000 003; test `test_counted_gates_equal_the_closed_form`):

* `add_scaled(t, a, κ)`: g = [t<p]; for i < b load k_i = κ·2^i mod p into Y controlled on
  (g, a_i) (CCX), t += Y mod p with the p-loads controlled on g, unload; recompute g.
  34b²+40b+10+4(b+1)hw(p)+2H gates, 10b²+8b+2H CCX.
* `add_product(t, a, b, κ)`: g = [t<p]; r = κ·[b] mod p into the clean scratch r by the
  unguarded constant multiplication; for i < b: h = g∧a_i, Y = h ? r : 0 (b CCX), t += Y mod p
  (controlled on g), unload, clear h, r ← 2r mod p (i < b−1); then the b−1 doublings and
  r = κ·[b] are undone by the reversed gate list (every gate is an involution); recompute g.
  134b²+50b−4+(20b−4)hw(p)+4H gates, 40b²+2b CCX.
* `swap`, `qft`, `oracle`: emitted exactly as by the original `Builder` (so the original
  checks of those macros apply verbatim). `increment` with value controls raises
  `NotImplementedError` (it is the O(p) synthesis being replaced); without controls it is a
  guarded constant adder.

The guard g is what makes the padding behaviour clean: the modular adder's flag
uncomputation assumes t < p, so without it a padding t would leave f dirty.

## 2. Padding behaviour

What the original code promises (docstrings of `Builder.increment` and the module header,
and `check_macros`): "t's padding is fixed", every macro is a permutation of basis words, and
the macro is checked only on canonical inputs. Nothing is promised about padding operands
(its value tests may fire on them).

What the new backend satisfies, checked on **all** words for p ≤ 13 [proof-by-computation]:

* (A1) on canonical t, a, b: t += κ·a(·b) mod p;
* (A2) if t ≥ p the macro is the identity on all registers (so t's padding is fixed);
* (A3) if t < p and a, b are any words: t += κ·[a]·[b] mod p with [a] the integer value of
  the word, operands unchanged;
* (A4) the operands are never targeted and every ancilla returns to 0;
* bijective on the 2^(kb) words.

The original `Builder`, run on the same words: padding t fixed and bijective for every macro
(so it keeps its own promise), and equal to the new backend on all canonical inputs. On all
words (padding operands included) the two coincide for p = 3, 5, 7 and differ for p = 11, 13
(operand padding acts differently, as expected; nothing downstream reads it, because every
state is supported on canonical words and the merge proofs are on canonical inputs).

## 3. Exhaustive checks (p ≤ 13) — artifact `exhaustive.json`

| p | b | ancillas | macro instances | words per add_scaled / add_product | gates add_scaled (new / old) | gates add_product (new / old) | all checks |
|---|---|---|---|---|---|---|---|
| 3 | 2 | 11 | 4 | 16 / 64 | 254 / 8 | 712 / 16 | pass |
| 5 | 3 | 14 | 8 | 64 / 512 | 476 / 36 | 1 480 / 144 | pass |
| 7 | 3 | 14 | 12 | 64 / 512 | 496 / 88 | 1 544 / 528 | pass |
| 11 | 4 | 17 | 20 | 256 / 4 096 | 792 / 308 | 2 604 / 3 080 | pass |
| 13 | 4 | 17 | 24 | 256 / 4 096 | 792 / 460 | 2 604 / 5 520 | pass |

(Gate columns: maximum over coefficients. The old gates are MCX with up to 3b−1 controls; the
new ones have at most 2. In raw gate count the new multiplication is cheaper from p = 11 on;
the new add_scaled is still larger at p = 13 (792 vs 460) and far smaller at p = 101
(2 134 vs 59 156).)
Primitive checks (adder on all 2^(2b) words incl. carry, modular adder on all canonical
pairs, doubling on all r < p, comparator on all words): pass for all five primes.

## 4. Integration and backend comparison — artifacts `agree.json`, `bitlevel.json`

Hook (in the new module only): `arith_backend()` rebinds, for the duration of a `with` block,
`rees_circuit_general.Builder → ArithBuilder`, `rees_circuit_general.check_macros →
check_macros_arith` (the original has no wires for the ancilla register; the new one is the
same check with the ancillas included, plus "ancilla returns to 0" and "operand never
targeted"), and `instrument_semantics` (in both `rees_circuit_general` and
`rees_circuit_sparse`) to a wrapper that first replaces each arithmetic macro of the
instrument by the permutation it induces on its qudits with ancilla 0 (checked on all words:
ancilla clean, bijective) and then runs the ORIGINAL `instrument_semantics` unchanged (block
partition, completeness, circulant form, rounding). This reduction is exact: each macro maps
span{|w⟩|0⟩_anc} to itself by that permutation, and the QFTs touch no ancilla. The symbolic
replay (`symbolic_replay`) reads only macro records and applies unchanged.

Results [exact unless stated]:

* `prove_merge` with the new backend: proved for Heis(F_3) d=2, s=1,2 and n4(F_5) d=2,3,
  s=1..4 (macro exhaustion with ancillas + symbolic replay over F_p[q, x]; W, brackets and
  ancillas clean; q never targeted).
* Bit-level merge permutation, old vs new: identical on Heis(F_3) (all 2 187 inputs, s=1,2);
  n4(F_5) grade 2 on ALL q and all x (9 765 625 inputs, s=1..4); grade 3 on 64 evenly spaced q
  rows and all x (5 000 000 inputs, s=1..4) [sampled in q]. Ancilla clean on every input.
* Instrument phase exponents: identical arrays at every grade (Heis d=2; n4 d=2,3);
  floating errors ≤ 7·10^−16 [float].
* Sparse mode, every subgroup (19 + 9): source state (indices, Z[ζ_p] rows, scale), support S
  and all source flags identical; top-grade label law and every conditioned branch identical;
  full `check_instance_sparse` rows identical (Heis: 234 or 26 merge cases each; n4: grade 3
  all 24/120 cases, grade 2 sampled 3 124–6 044 cases); `passed` for every subgroup;
  `run_algorithm_sparse` with seeds 20261103 and 20261104 returns identical results (same
  samples, same oracle-query count, same recovered log H) and recovers log H in all 56 runs.
* Primitive counts of a terminal sample are unchanged (same macro programme): Heis(F_3)
  6 oracle calls, 12 BCH passes; n4(F_5) 30 oracle calls, 60 BCH passes, 140 bracket
  evaluations. Width grows by the ancilla register only: 82 → 93 qubits (Heis(F_3)),
  744 → 758 (n4(F_5)). Gate totals per terminal sample grow at these tiny primes: Heis(F_3)
  1 236 → 42 294 logical gates; n4(F_5) 91 240 → 1 029 220 (all ≤ 2 controls in the new one).
  The paper's "5528 CNOTs" and "gate for gate with rees_circuit.py" refer to the ORIGINAL
  backend and stay true for it only.

Large p [sampled], artifact `sampled.json`: for p = 101, 1031, 65537, 2^61−1, both macros, 5
coefficients each (1, p−1 and three random), on 3 088 / 3 136 inputs (all edge tuples from
{0,1,2,p−1}, 2 048 random canonical, 512 with padding t, 512 with padding operands): map
(A1)–(A3) and clean ancillas, all pass. Merge bit level on 3 random q × 1 024 random x with
clean ancillas and equality with the BCH law: Heis(F_101) s=1,37; n4(F_101) d=2 s=1 and d=3
s=1,58; Heis(F_1031) s=1,500; n4(F_1031) d=2 s=3, all pass. (Larger p overflows the int64
group indices of the existing simulators; the counts below need no simulation.)

## 5. Gate counts (counted, not simulated) — artifact `counts.json`

Per multiplication (`add_product`, range over the sampled coefficients) and per linear macro:

| p | b | add_product gates | add_product CCX = 40b²+2b | add_scaled gates (max) | ancillas 3b+5 | old add_product gates |
|---|---|---|---|---|---|---|
| 101 | 7 | 7 484–7 556 | 1 974 | 2 134 | 26 | 5 915 600 |
| 1031 | 11 | 17 668–17 888 | 4 862 | 4 888 | 38 | 9 873 312 200 |
| 65537 | 17 | 40 312–40 888 | 11 594 | 10 982 | 56 | not computed (~p³) |
| 2^61−1 | 61 | 576 080–590 476 | 148 962 | 151 412 | 188 | — |

Per merge (one controlled right translation x → x·(−δ_s(σ(q))), four Bennett passes, s = 1;
total gates / qubits incl. ancillas):

| p | Heis d=2 | n4 d=2 | n4 d=3 | n5 d=2 | n5 d=3 | n5 d=4 |
|---|---|---|---|---|---|---|
| 101 | 94 130 / 110 | 171 260 / 152 | 317 098 / 201 | 248 390 / 194 | 535 798 / 285 | 750 288 / 348 |
| 1031 | 219 694 / 170 | 400 564 / 236 | 743 174 / 313 | 581 434 / 302 | 1 256 898 / 445 | 1 761 148 / 544 |
| 65537 | 498 162 / 260 | 909 332 / 362 | 1 688 950 / 481 | 1 320 502 / 464 | 2 857 870 / 685 | 4 005 696 / 838 |
| 2^61−1 | 7 052 826 / 920 | 12 908 752 / 1 286 | 24 029 352 / 1 713 | 18 764 678 / 1 652 | 40 703 054 / 2 445 | 57 081 130 / 2 994 |

Macro counts per merge do not depend on p (Heis 8 add_product + 16 add_scaled; n4 d=3 32 + 36;
n5 d=4 80 + 70), so a merge costs (#add_product)·O(b²) + (#add_scaled)·O(b²) + b·width SWAPs.

Fits over p ∈ {101, 1031, 65537, 2^61−1} (b = 7, 11, 17, 61; `fit_p_ge_101_loglog` in the JSON, which also has fits over all nine primes): log-log slope of the gate count
against b: add_product 2.02, its CCX 2.00 (least squares 40.0b²+2.0b+0, i.e. exact),
add_scaled 1.98; merges Heis 2.00, n4 d=3 2.01, n5 d=4 2.01. Gates/b² stays in
[141, 159] for add_product and [1 724, 1 921], [5 844, 6 471], [13 861, 15 340] for those
merges (the spread is the hw(p) and H terms; 2^61−1 has hw(p) = 61 = b, the worst case). The
counting mode was checked equal to full emission (counts and macro records) at p = 11, 101,
1031, and the closed forms of section 1 equal the counted gates for every row of the JSON
(`formula_matches: true`).

## 6. The exact statement that now holds

**[proof-by-computation + exact counts, AI-checked, pending human review].** For every
algebra and class c < p accepted by `rees_circuit_general.Config`, `ArithBuilder` emits each
F_p multiply-accumulate t += κ·a·b with only X, CX, CCX and SWAP gates and 3b+5 ancillas,
b = ⌈log2 p⌉, using exactly 40b²+2b CCX and at most 158b²+46b−4 gates; each t += κ·a with
exactly 10b²+8b+2H ≤ 12b²+8b CCX and at most 40b²+44b+10 gates. [The counts are exact
functions of (b, hw(p), κ) derived from the block structure and confirmed by counting for 108
cases up to a 61-bit prime.] For p ∈ {3, 5, 7, 11, 13} these gate lists are, on ALL basis
words with ancilla 0, the declared map on canonical inputs, the identity when t is padding,
bijective, with clean ancillas [proof-by-computation]; for p = 101, 1031, 65537, 2^61−1 this
holds on the sampled inputs of section 4 [sampled]; for general p it is [argued] (standard
VBE/Cuccaro/Beauregard constructions, guarded). With this backend the generated merge gate
lists for Heis(F_3) and n4(F_5) are proved equal to the BCH right translation on all canonical
inputs, and the sparse simulation of Heis(F_3) (19 subgroups) and n4(F_5) (9 subgroups)
gives the same states, the same checks and the same seeded recoveries as the original backend.
Consequently the arithmetic of the generated circuits is O(log² p) gates per field
multiplication. The circuits as a whole are NOT poly(log p): each QFT_p is still one exact
b-qubit unitary.

Note on the paper's wording: the "poly(log p) of (iii)" in the Gate-level control paragraph
refers to thm:uniform-compilation(iii), which is about QFT_p, not arithmetic. Items (i)–(ii)
count field operations; a field multiplication at O(b²) gates is what makes them gate counts.
The proposed text below separates the two.

## 7. Claim gates that stay false

`ARITH_STATUS` (= the generator's STATUS plus): `coherent_receiver_implemented: False`,
`general_sde_implemented: False`, `formal_compiler_checked: False`, `independent_review: False`,
`novelty_established: False`, `speedup_claim_allowed: False`, `qft_poly_log_p_implemented:
False`; only `poly_log_p_arithmetic_implemented: True`, scoped to the arithmetic macros. No
claim about a quantum advantage, the oracle cost T_f, asymptotic query or time bounds, or a
native application follows from this work.

Still missing, in order of relevance to (iii) and to a full poly(log p) circuit:
1. a finite-gate QFT_p at poly(log p + log 1/η) (Kitaev / Cleve–Watrous with Solovay–Kitaev
   or exact Clifford+T synthesis) and its error accounting with Lemma hybrid;
2. a gate-level oracle (T_f is still a table of fully controlled MCX gates);
3. exhaustive correctness beyond p = 13 (only sampled; a symbolic or Lean proof of the
   adder/modular-adder blocks for all b would close this);
4. optimisation (Gidney-style adders halve the Toffolis; register reuse; depth was not
   measured), and a combined terminal-sample count at large p (the QFT unitary cannot be
   built there, so only per-merge counts are reported).

## 8. Proposed paper text

Replacement for the sentences "Each $\Fp$ coordinate uses ... not the $\poly(\log p)$
of~(iii)." in the paragraph "Gate-level control" of `docs/papers/rees-hsp/main.tex`
(**finite computation, AI-checked, pending human review**; not applied, the paper is
untouched):

```latex
Each $\Fp$ coordinate uses $b=\lceil\log_2 p\rceil$ qubits, and all arithmetic is built from $X$, CNOT, Toffoli or multi-controlled $X$, and SWAP gates, so each arithmetic block is an exact permutation of basis states. The original arithmetic uses value-controlled increments and costs $O(p^3\log p)$ gates per multiplication, a small-$p$ synthesis. A second backend, \file{theorems/rees_circuit_arith.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-arith.md}; finite computation, AI-checked, pending human review), emits the same arithmetic macros from a ripple-carry adder, a modular adder with comparison and conditional subtraction, constant multiplication by shift-and-add, and a controlled modular multiply-accumulate, using only $X$, CNOT, Toffoli and SWAP gates and $3b+5$ ancillas that every block returns to $0$. One multiplication $t \leftarrow t+\kappa ab$ then uses exactly $40b^2+2b$ Toffoli gates and at most $158b^2+46b$ gates, so the arithmetic costs $O(\log^2 p)$ gates per field operation; these counts are exact for the generated gate lists (counted up to a $61$-bit prime, not simulated there). The blocks of this backend are checked on all basis inputs, padding included, for $p\le 13$, and on the Heisenberg group over $\mathbb{F}_3$ and the class-three filiform algebra over $\mathbb{F}_5$ below the two backends give the same states at every step and the same recoveries. In both backends $\mathrm{QFT}_{\Fp}$ is one exact $b$-qubit unitary, so the circuits as a whole remain a small-$p$ synthesis and do not realise the $\poly(\log p)$ transform of~(iii).
```

If the paper keeps quoting "82 qubits ... 5528 CNOTs" and "gate for gate with
rees_circuit.py", those numbers are for the original backend; with the new backend the
Heis(F_3) terminal sample uses 93 qubits (82 + 11 ancillas) and the same 6 oracle calls and
12 BCH passes. Suggested insertion after "excluding the oracle)": `with the original arithmetic
backend`.

## 9. Artifacts

`research/audits/reviews/2026-11-04-rees-circuit-arith/`: `exhaustive.json` (section 3),
`agree.json` (section 4, sparse comparison), `bitlevel.json` (section 4, n4 bit level),
`sampled.json` (section 4, large p), `counts.json` (section 5), the matching `.log` files and
`run_commands.sh`.

# Rees HSP: sparse coset-support simulation of the gate-level generator, class four (campaign 3, item 4, part 3)

3 November 2026 (session started 2 November, late). AI-only session (Claude Code, Opus 5.5).
Not human review, not Lean. **Every claim below is AI-checked, pending human review.**
Labels as in `2026-11-03-rees-circuit-2.md`: **[exact]** = complete finite computation in
integer, permutation or Z[ζ_p] arithmetic; **[proof-by-computation]** = exhaustive finite check
covering ALL canonical inputs of a module; **[float]** = complex floating point, tolerance 1e-9;
**[sampled]** = exact on a stated subset only; **[argued]** = reasoning, not machine-checked.

Files written (and nothing else): `theorems/rees_circuit_sparse.py` (new),
`tests/test_rees_circuit_sparse.py` (new), this report, and the folder
`research/audits/reviews/2026-11-03-rees-circuit-3/`. Read-only imports:
`theorems/rees_circuit_general.py` (circuits, gate-list evaluation, merge proofs, instrument
semantics, the dense `Engine`, grading truth), `theorems/rees_end_to_end_sim.py` (algebras,
cyclotomic helpers). `theorems/rees_end_to_end_ext.py` was read as the model for the sparse
representation and is neither imported nor edited. No existing file was edited; `main.tex`
untouched; nothing committed.

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_sparse.py
REES_SLOW=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_sparse.py -k slow
sh research/audits/reviews/2026-11-03-rees-circuit-3/run_commands.sh   # the artifact runs (about 1 h on this machine)
```

## 0. Answers

1. **Built.** `theorems/rees_circuit_sparse.py` adds a `SparseEngine` that simulates the same
   generated circuits as the dense `Engine` of `rees_circuit_general.py`, with the same
   conventions (ρ[x,y] = φ(x⁻¹y)/|G_d|, canonical Z[ζ_p] rows), but keeps only the rows where
   φ ≠ 0. The source is evaluated from its own gate list on all |G_c| canonical addresses in
   address chunks, so no |G_c|-sized coordinate array is formed; only one int64 label key per
   address is kept.
2. **Agreement with the dense mode [exact].** On all 19 subgroups of Heis(F_3) and the 9
   n4(F_5) test subgroups (5 non-normal), with the source run in 4096-address chunks
   (16-address chunks in the Heis tests), the two modes give exactly the same group-algebra
   element at every step. Compared: the source state, its S and every source flag; every label
   law and every conditioned branch at every grade; 1 794 (Heis) and 2 578 (n4) sampled merge
   outputs; the readout distribution. Also identical: the full `check_instance` rows, which
   cover 3 198 and 42 532 merge cases, and two seeded `run_algorithm` results per subgroup (same
   samples, same recovered log H). Artifact `agree.json`, 278 s.
3. **Class four, n5(F_5) [exact / proof-by-computation / sampled where said].** Here
   [e1,e_i] = e_(i+1) for i = 2, 3, 4, the cover dimensions are (5, 3, 2, 1), |G_4| = 5^11 =
   48 828 125, points 1..4 and the Chevalley-Warning arities are M_4 = 5, M_3 = 3, M_2 = 7.
   **9 subgroups pass every check, 5 of them non-normal** (corrected 11-04; see the note at the end). For each:
   - the source built from the gate list equals the coset density of exp(h̃) exactly, with a
     clean evaluation workspace;
   - every label law at grades 4, 3 and 2 is exactly uniform on K_d^⊥;
   - every merge output checked equals ρ_{H_(d−1)};
   - the readout is uniform on h^⊥;
   - one seeded run from oracle access (7 terminal samples, 2 940 oracle queries) recovers
     log H.

   The merge gate lists are proved equal to the BCH right translation, on all canonical
   inputs, for d = 2, 3, 4 and s = 1..4. For trivial H and for <e2> (non-normal), every label
   tuple and every witness is merged at grades 4 and 3: 1 952 500 + 77 500 cases each, all exact.
4. **Tests.** Fast: 20 passed, 1 skipped (slow) in 40 s. Slow (`REES_SLOW=1 ... -k slow`, the
   n5 source from its gate list for <e1>, then all grades): 1 passed in 73 s.
5. **The memory blocker is removed.** A dense Z[ζ_5] state on G_4 would be 4.9·10^7 × 5 int64
   ≈ 1.95 GB. The largest sparse state here (H = γ_2, |exp(h̃)| = 5^9) is 1.95·10^6 rows ≈ 78 MB.
   The largest process resident set was 1.75 GB, dominated by the per-address key array and
   the chunked bit-slice buffers. One n5 source evaluation takes 50-330 s on the loaded
   machine; the time grows with |S| through the coset check.

## 1. What the sparse mode computes (and why it is the dense computation)

Every step is the dense `Engine` step of `rees_circuit_general.py`, restricted to the
support. No new formula enters.

- **Source.** The gate list is checked to start with the exact QFT_p on each address
  coordinate. The rest (X/CX/MCX/SWAP and the table oracle U_f) is evaluated bit-sliced by the
  generator's `BitSim` on ALL canonical addresses, in chunks of 2^20 (47 chunks for n5); a
  permutation acts on each input separately, so chunking is exact. Per chunk: the address
  comes back unchanged and the workspace is 0. The key of an address is its c label registers
  packed into one int64; if the workspace is dirty, the workspace joins the key, as in the
  dense fibre computation. Then come the dense checks:
  - all fibres have equal size;
  - the identity fibre S is the closure of greedily chosen generators, so S is a subgroup;
  - key(x·g) = key(x) for every address x and every generator g (chunked), so every fibre is a
    left coset of S.

  Hence ρ = 1_S(x⁻¹y)/|G_c| exactly, stored on S. The grader compares S with exp(h̃)
  (`stage_indices`).
- **Instrument.** The exponents e_j[λ][u] are the ones `instrument_semantics` derives from the
  instrument's own gate list. That derivation is float, rounded to exact exponents, with
  largest error 7.5e-14 at d = 2, 3, 4 for p = 5 [float]. Conditioning is
  φ'(g) = p^{−g_d} Σ_u ζ^{e(λ,u)} φ(g+u) on the support rows, summed per target index; the
  support grows to the central saturation S·Z_d. A label probability is the identity
  coefficient, and it is checked equal to the trace of the conditioned branch.
- **Merge.** F(g) = Π_i φ_i(δ_{s_i}(g)) is computed on the intersection of the pulled-back
  supports, starting from the smallest one. It must be constant on full central fibres
  (descent); otherwise the code raises. The output is ψ = F∘σ on G_(d−1). That the merge gate
  list implements x ↦ x·(−δ_s(σ(q))) is the generator's `prove_merge` (macro exhaustion plus
  symbolic replay over F_p[q,x] against the classical BCH polynomial), run for every d and s.
  At class four `sym_bch_reference` uses the NilGroup formula (d ≤ 4), which is written
  independently of the bracket-node derivation.
- **Readout.** P(k) = |G_1|⁻¹ Σ_{w ∈ supp} ζ^{−k·w} ψ(w) must be rational and sum to 1.

## 2. Results

### 2.1 Sparse = dense (Heis(F_3), n4(F_5))

| Instance | subgroups (non-normal) | states compared | check rows | seeded runs | result |
|---|---|---|---|---|---|
| Heis(F_3), c = 2 | 19 (12) | source, all branches, 1 794 merges, readout | identical (3 198 cases) | 38 identical | equal [exact] |
| n4(F_5), c = 3 | 9 (5) | source, all branches at d = 3, 2, 2 578 merges, readout | identical (42 532 cases) | 18 identical | equal [exact] |

Source chunking is irrelevant: on n4(F_5) <e2,e3> the source in 20 chunks equals the
one-chunk source (test).

### 2.2 n5(F_5), class four

Columns: |S| = |exp(h̃)| (identity fibre found from the gates); for each grade, |K_d^⊥|, the
tuple mode and the number of merge cases (each exact); the largest sparse state; the source
time. All rows: source = ρ_{exp h̃} with clean workspace, label laws uniform on K_d^⊥ at d = 4,
3, 2, all merge outputs = ρ_{H_(d−1)}, readout uniform on h^⊥, seeded run recovers log H.

| H | normal | \|S\| | d = 4 | d = 3 | d = 2 | largest state | source s |
|---|---|---|---|---|---|---|---|
| trivial | yes | 1 | 5; sampled, 360 | 25; sampled, 100 | 125; sampled, 360 | 125 | 49 |
| <e1> | no | 5 | 5; sampled, 360 | 25; sampled, 100 | 125; sampled, 360 | 625 | 87 |
| <e2> | no | 5 | 5; sampled, 360 | 25; sampled, 100 | 125; sampled, 360 | 625 | 96 |
| <e3> | no | 25 | 5; sampled, 360 | 25; sampled, 100 | 25; sampled, 360 | 625 | n/r |
| Z(G) = <e5> | yes | 625 | 1; sampled, 360 | 5; sampled, 180 | 25; sampled, 360 | 625 | n/r |
| <e2,e5> | no | 3 125 | 1; sampled, 360 | 5; sampled, 180 | 25; sampled, 360 | 3 125 | 237 |
| <e1+e2+e5> | no | 5 | 5; sampled, 360 | 25; sampled, 100 | 125; sampled, 360 | 625 | n/r |
| γ_3 = <e4,e5> | yes | 78 125 | 1; sampled, 360 | 1; all, 124 | 5; sampled, 360 | 78 125 | 315 |
| γ_2 = <e3,e4,e5> | yes | 1 953 125 | 1; sampled, 360 | 1; all, 124 | 1; sampled, 360 | 1 953 125 | 332 |
| trivial (exhaustive run) | yes | 1 | 5; **all, 1 952 500** | 25; **all, 77 500** | 125; sampled, 360 | 125 | 49 |
| <e2> (exhaustive run) | no | 5 | 5; **all, 1 952 500** | 25; **all, 77 500** | 125; sampled, 360 | 625 | 96 |

("n/r": that run predates the source timer. Times are from the loaded machine.)
"Sampled" means `check_instance`'s rule: the all-zero tuple, the constant tuple and 4 random
tuples, each with 60 random valid witnesses (all witnesses if fewer). When |K_d^⊥| = 1 the 6
tuples coincide (all zero), so those rows test 6 × 60 random witnesses out of p^M − 1 (3 124 at
d = 4) [sampled]. "All" means every label tuple with every valid witness [exact]. Every n5
seeded run used 735 top sources and 2 940 oracle queries. The SDE was solved by the IS solver
wherever it applies (all 49 grade-3 solves; grade-4 solves when K_4^⊥ = 0; grade 2 only for
γ_2) and by brute force elsewhere.

Merge gate lists (`merge_gate_checks`, in `n5_f5.json`): d = 2, 3, 4 with 57, 111 and 151
macros; s = 1..4 all `proved` [proof-by-computation]. Each was also run bit-level on 8 random
q × 16 384 random x (about 1.3·10^5 inputs per (d, s)) against `GroupLaw.mul`; all equal, scratch
clean, Q never targeted [sampled]. The class-four BCH node set is xy, xxy, yxy, xyxy, yxxy.
(`n5_f5_b.json` and `n5_f5_exhaustive.json` were run with `--no-gate-checks`, so their
`all_merges_proved` flag is vacuous; the proofs are in `n5_f5.json` and in the fast tests.)

### 2.3 Negative controls (tests)

| Broken variant | Result |
|---|---|
| Source without the evaluation uncompute (n4, <e2>) | workspace flagged dirty; flags and S equal to the dense mode's |
| Two evaluation points on class three (n4, trivial) | identity fibre larger than exp(h̃) = {1} |
| Non-witness scales (n4, <e1>, labels (1, 2)) | 3/3 do not give ρ_{H_2} |
| A state on two non-central points of G_3 | merge raises (does not descend) |

## 3. Exact statement that now holds (AI-checked, pending human review)

For L = n5(F_5) ([e1,e_i] = e_(i+1), i = 2, 3, 4; class 4; cover dims (5,3,2,1); |G_4| = 5^11),
points 1..4 and Chevalley-Warning arities (M_4, M_3, M_2) = (5, 3, 7), take the nine subgroups
H ∈ {1, <e1>, <e2>, <e3>, <e5>, <e2,e5>, <e1+e2+e5>, γ_3, γ_2}, five of them non-normal (corrected 11-04). The Qiskit
gate lists emitted by `theorems/rees_circuit_general.py`, simulated module by module in the
sparse mode of `theorems/rees_circuit_sparse.py`, have these properties:

- the lifted source, evaluated from its gate list on all 5^11 canonical addresses, is exactly
  the coset density of exp(h̃), with clean evaluation workspace;
- its central labels and those of every merged state are exactly uniform on K_d^⊥ at d = 4, 3, 2;
- every checked merge output is exactly ρ_{H_(d−1)}. The checked cases are every label tuple
  with every valid witness at grades 4 and 3 for H = 1 and H = <e2>, and at grade 3 for γ_3 and
  γ_2; otherwise the sampled tuples and witnesses of Section 2.2;
- the readout is uniform on h^⊥, so its annihilator is log H;
- one seeded run per subgroup from oracle access recovers log H.

Each merge gate list at d = 2, 3, 4 equals x ↦ x·(−δ_s(σ(q))) on all canonical inputs, with
scratch returned to zero (proof by computation). On Heis(F_3) (all 19 subgroups) and n4(F_5)
(9 subgroups), the sparse mode returns exactly the dense mode's states, check results and
seeded runs.

## 4. What is missing

- Grade-2 coverage at class four is sampled (360 cases per subgroup out of up to
  |K^⊥|^7·5^7/|K^⊥|), and so is grade 4 when K_4^⊥ = 0 (360 of 3 124 witnesses of the single
  tuple). Exhaustive grade 4 and grade 3 were run for two subgroups only.
- The sparse merge is the Schur-product channel of prop:descent fed by the proved merge
  permutation. The dense trace cross-check (`merge_trace_crosscheck`, which uses no BCH
  identity) was not run at class four: a full x sweep is |G_4| inputs per q row. The bit-level
  merge runs at class four are sampled.
- Only one seeded run per subgroup at class four; no n5(F_7) or other class-four algebra; no
  class five.
- Everything already listed in circuit-2: poly(log p) modular arithmetic and finite-gate QFT
  synthesis; Schedule 1 at its paper arity inside the flow; a coherent (non-feed-forward)
  receiver; a monolithic simulation; identity-on-padding arithmetic; human review.

**Claim gates that must stay false** (none was touched; `SPARSE_STATUS` keeps them false and a
test checks this): `coherent_receiver_implemented` (the SDE solve is still classical
feed-forward between quantum segments, and these are finite simulated instances),
`general_sde_implemented`, `formal_compiler_checked`, `independent_review`,
`novelty_established`, `speedup_claim_allowed`.

## 5. Proposed paper text

Target: `main.tex`, Section~\ref{sec:uniform-compilation}, paragraph "Gate-level control"
(replacing the circuit-2 proposal). Status: finite computation; AI-checked, pending human
review. Not applied (main.tex untouched). Counts are from circuit-2 Section 5 and this
report's Section 2; regenerate them rather than retyping.

```latex
\paragraph{Gate-level control.} The artifact \file{theorems/rees_circuit_general.py} (reports \file{research/audits/reviews/2026-11-03-rees-circuit-2.md} and \file{research/audits/reviews/2026-11-03-rees-circuit-3.md}; finite computation, AI-checked, pending human review) generates explicit Qiskit circuits for the whole procedure from the structure constants of $\mathcal{L}$, the evaluation points, the oracle table and the merge arities, for any class $c<p$. Each $\Fp$ coordinate uses $\lceil\log_2 p\rceil$ qubits. Arithmetic uses only $X$, CNOT, multi-controlled $X$ and SWAP gates, and $\mathrm{QFT}_{\Fp}$ is one exact unitary, so this is a small-$p$ synthesis: its arithmetic costs $O(p^3\log p)$ gates per multiplication, not the $\poly(\log p)$ of~(iii). The circuits make $c$ coherent oracle calls per source with uncomputed evaluation workspaces and apply the complete central instrument at every grade. They implement $x \mapsto x \ast (-\delta_s(\sigma(q)))$ with the class-$d$ BCH law in right-nested brackets and the four passes of~(ii), and end with abelian Fourier sampling. The diagonal equation is solved classically between quantum segments, by the deterministic solver of Section~\ref{sec:sde} where the arity reaches its column count. Each merge gate list is proved, on all canonical inputs, to equal the BCH right translation with clean scratch, by exhaustive checks of its arithmetic blocks and a symbolic replay over $\Fp[q,x]$. The modules are simulated exactly in $\mathbb{Z}[\zeta_p]$ and composed through the tensor and Schur-product structure of Proposition~\ref{prop:descent}. Every state of the procedure is supported on a set of the size of a central saturation of a coset (first $\exp(\hlift)Z_d$, then $H_dZ_d$), so the simulation stores states only on their support; on the Heisenberg group over $\mathbb{F}_3$ and the class-three filiform algebra over $\mathbb{F}_5$ this agrees exactly, state by state, with a dense simulation. On the Heisenberg group over $\mathbb{F}_3$ the generated circuits coincide gate for gate with those of \file{theorems/rees_circuit.py} ($82$ qubits, $6$ oracle calls, $12$ BCH passes and $5528$ CNOTs per terminal sample, excluding the oracle). For the class-four filiform algebra $[e_1,e_i]=e_{i+1}$ ($i=2,3,4$) over $\mathbb{F}_5$, with cover dimensions $(5,3,2,1)$, $|G_4|=5^{11}$ and arities $(M_4,M_3,M_2)=(5,3,7)$, we take nine hidden subgroups, five of them nonnormal. The source is evaluated from its gate list on all $5^{11}$ addresses and equals the coset density of $\exp(\hlift)$. Every label law is uniform on $K_d^\perp$ at grades four, three and two, and every checked merge output is $\rho_{H_{d-1}}$: all label tuples with all their witnesses at grades four and three for two subgroups, and sampled tuples and witnesses otherwise. A seeded run from oracle access recovers $\hh$ for each subgroup. These are fixed finite instances with an exact Fourier transform and a classical solve between quantum segments. They are not a coherent receiver for general $(G,H)$, and they test no asymptotic cost.
```

## 6. Artifacts (`research/audits/reviews/2026-11-03-rees-circuit-3/`)

- `run_commands.sh`: the exact commands.
- `agree.json` / `.out`: sparse vs dense, Heis(F_3) and n4(F_5), 278 s, max RSS 0.27 GB.
- `n5_f5.json` / `.out`: merge proofs and bit-level runs at d = 2, 3, 4; instrument errors; 6
  subgroups with checks and seeded runs; 547 s, max RSS 1.75 GB.
- `n5_f5_b.json` / `.out`: <e1>, <e2,e5>, γ_3, γ_2 with source times; 2 032 s, max RSS 1.52 GB.
- `n5_f5_exhaustive.json` / `.out`: trivial and <e2>, all tuples and witnesses at d = 4, 3;
  840 s, max RSS 1.55 GB.
- `pytest_fast.out`, `pytest_slow.out`: test logs.

## 7. Work log

- 23:50 Read the generator, the circuit-2 report and the ext sparse backend. Plan: a
  `SparseEngine` with the dense `Engine`'s conventions (phi(x^-1 y)/|G_d|, Z[zeta_p] canonical
  rows), states stored only on their support; the source evaluated from its own gate list in
  address chunks (no |G_c|-sized coordinate arrays); conditioning with the gate-derived
  instrument exponents; merges as the Schur product checked to descend.
- 00:05 `theorems/rees_circuit_sparse.py` written (SparseEngine, check/run/compare functions,
  class-four driver). First probe: on all 19 Heis(F_3) subgroups and the 9 n4(F_5) subgroups the
  sparse mode equals the dense mode state by state (source state and flags, every label law and
  branch, sampled merge outputs, readout), the full `check_instance` rows are identical, and
  seeded `run_algorithm` results are identical (same samples, same recovered log H), with the
  source evaluated in 4096-address chunks. Two background jobs started (niced, time-limited):
  `n5_f5` (9 subgroups) and `agree` (artifact version of the comparison).
- 00:20 First artifact `agree.json` (28 s): all 19 Heis(F_3) and all 9 n4(F_5) subgroups equal
  state by state. Relaunched with the full `check_instance` row comparison and two seeded runs
  per subgroup. Class four is running: merge proofs d = 2, 3, 4, s = 1..4 all pass (4.5 s);
  n5(F_5) trivial and <e1> (non-normal) pass every check and recover log H; one source from
  its gate list takes about 40 s over 4.9·10^7 addresses (47 chunks), RSS about 0.8 GB.
  Fast tests: 15 passed, 1 skipped (slow) in 20 s.
- 00:45 `n5_f5` finished (547 s, maximum resident set 1.75 GB): merges proved for d = 2, 3, 4 and
  s = 1..4, sampled bit-level runs agree, and 6 subgroups (trivial, <e1>, <e2>, <e3>, <e1+e2+e5>
  non-normal; Z(G) normal) pass every check and recover log H. The `--names` list was split on
  commas, so the three names containing a comma (<e2,e5>, gamma_3, gamma_2) were silently
  dropped; separator changed to ";" and they are rerun in `n5_f5_b` (with <e1> again, now
  with the source time recorded). Second job `n5_f5_exhaustive`: trivial and <e2> with every
  label tuple and every witness at grades 4 and 3. `agree.json` (278 s): all 28 subgroups
  identical, including the full `check_instance` rows (3198 + 42 532 merge cases) and two
  seeded runs each.
- 01:55 Remaining runs finished; all 9 n5(F_5) subgroups pass; fast tests 20 passed, 1 skipped (40 s); slow test passed (73 s). Report finalized.

## Correction (11-04)

The count of non-normal subgroups at n5(F_5) was wrong in three places (Answers item 3, Section 3,
and the proposed paper text): it said six, but five of the nine are non-normal. With
[e1,e_i] = e_(i+1) for i = 2, 3, 4, the ideals among the nine are 1, Z(G) = <e5>, γ_3 = <e4,e5> and
γ_2 = <e3,e4,e5>; the non-normal ones are <e1>, <e2>, <e3>, <e2,e5> and <e1+e2+e5>. This matches
the `normal` column of the table in Section 2.2, the `normal` flags (`alg.is_ideal`) recorded in
`n5_f5.json`, `n5_f5_b.json` and `n5_f5_exhaustive.json`, and an independent ideal check of the
generators of `N5_SUBGROUPS` in `theorems/rees_circuit_sparse.py`. No check result changes. Found by
`2026-11-04-rees-referee-5-circuits.md`, finding E1; `main.tex` was corrected the same day.

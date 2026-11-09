# Rees HSP: gate-level circuit generator for general (L, c, p), tested at class three (campaign 3, item 4)

3 November 2026 (session started 2 November, late). AI-only session (Claude Code, Opus 5.5).
Not human review, not Lean. **Every claim below is AI-checked, pending human review.**
Labels: **[exact]** = complete finite computation in integer, permutation or Z[ζ_p]
arithmetic; **[proof-by-computation]** = an exhaustive finite check that covers ALL
canonical inputs of a module; **[float]** = complex floating point, tolerance 1e-9;
**[sampled]** = exact on a stated subset only; **[argued]** = reasoning, not machine-checked.

Files written (and nothing else): `theorems/rees_circuit_general.py`,
`tests/test_rees_circuit_general.py`, this report, and the folder
`research/audits/reviews/2026-11-03-rees-circuit-2/` (artifacts listed in Section 9).
Read-only imports: `theorems/rees_end_to_end_sim.py` (cover construction, F_p linear algebra,
cyclotomic helpers, brute-force SDE), `theorems/rees_is_sde_solver.py` (Schedule 1 solver),
and, in the tests only, `theorems/rees_circuit.py` (the Heis(F_3) reference).

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_general.py
REES_SLOW=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_general.py -k slow
PYTHONPATH=. /opt/anaconda3/bin/python -B -m theorems.rees_circuit_general --jobs heis_f3,n4_f5,n4_f5_is_arity18 --resources --out report_main.json
PYTHONPATH=. /opt/anaconda3/bin/python -B -m theorems.rees_circuit_general --jobs n4_f7 --out report_n4_f7.json
PYTHONPATH=. /opt/anaconda3/bin/python -B research/audits/reviews/2026-11-03-rees-circuit-2/resource_table.py
```

## 0. Answers

1. **Built.** `theorems/rees_circuit_general.py` takes a Lazard Lie algebra L over F_p (structure
   constants, class c < p), evaluation points, a hidden subgroup H (only to build the oracle
   table) and per-grade merge arities M_d (default: Chevalley-Warning κ_d g_d + 1). It emits
   Qiskit circuits for the lifted source (coherent oracle calls with uncomputed evaluation
   workspaces), the complete central instrument at every grade d = c, ..., 2, the controlled
   right translation x ↦ x * (−δ_s(σ(q))) with the class-d BCH law compiled to reversible
   F_p arithmetic, Fourier readout, and the assembled circuit of one terminal sample. The SDE
   solve between quantum segments is classical feed-forward: the deterministic IS solver of
   `rees_is_sde_solver.py` whenever the arity reaches its column count, otherwise brute force.
2. **Acceptance 1 (Heis(F_3)) [exact].** Every emitted circuit (source with oracle and the
   oracle's own MCX definition, instrument, both merges and their no-Bennett variants,
   Fourier, the assembled 82-qubit terminal sample for witnesses (1,2,1), (1,0,1), (1,1,1)) is
   gate for gate, qubit for qubit and clbit for clbit the one of `rees_circuit.py`. Primitive
   counts, logical gate counts and the transpiled profile (5528 CX, 6647 u, depth 5103 for the
   assembled sample with witness (1,2,1)) are equal. All 19 subgroups pass with the same 3198
   label-tuple/witness cases, now in exact Z[ζ_3] arithmetic, and every state agrees with the
   old float simulation to 1e-12.
3. **Acceptance 2 (n4(F_5), class 3) [exact / proof-by-computation / sampled where said].**
   For the 9 test subgroups (5 non-normal), every top source equals the coset density of
   exp(h̃) exactly, with clean workspace; every label law at grades 3 and 2 is exactly uniform
   on K_d^⊥; every merged output checked (all 696 grade-3 cases, i.e. every label pair and
   every witness; 41 836 grade-2 cases, all witnesses of sampled label 5-tuples, exhaustive
   where h ⊇ γ_2) equals ρ_{H_(d−1)}; the readout is uniform on h^⊥, and 18 seeded runs from
   oracle access recover log H. Every merge gate list (d = 2, 3; s = 1..4) is proved on all
   canonical inputs to equal the BCH right translation with clean scratch.
4. **Acceptance 3.** Fast tests: 59 passed, 14 skipped (slow) in 36 s on a machine with load
   average 100-240. Slow tests (`REES_SLOW=1 ... -k slow`): 14 passed in 8 min 30 s (exhaustive
   bit-level grade-2 merges of n4(F_5), 9.8·10^6 inputs per s; 12 label tuples with all
   witnesses per n4(F_5) subgroup; one n4(F_7) subgroup end to end). There is no registered
   `slow` marker in the repo's pytest configuration, so slow tests carry a `skipif` mark that
   runs them only with REES_SLOW=1.
5. **Largest instance simulated:** n4(F_7), class 3, cover dimension 7, |G_3| = 7^7 = 823 543,
   arities M_3 = 4, M_2 = 5 (20 top sources, 60 oracle calls per terminal sample, 1404 qubits in
   the assembled circuit). All 9 subgroups pass and 9 seeded runs recover log H (Section 4.3). **Blocker for the next one** (class four, the
   smallest being n5(F_5) with |G_4| = 5^11 ≈ 4.9·10^7): the dense Z[ζ_p] group-algebra state
   vectors (≈ 2 GB each, several live) on a shared 16 GB machine. Section 7.

## 1. Input, encoding and gate synthesis

- **Input.** `Config(algebra, points=None, arities=None)`; `Hidden(name, algebra, generators)`
  builds f(x) = min index of xH (the grading truth is kept separately and only used to grade).
  The cover A = ⊕_k t^k γ_k(L), its tensor and E_s come from `make_cover` (checked there:
  Jacobi, E_s Lie homomorphism). The group law of every G_d is my `GroupLaw`, valid for any
  class < p, which agrees with `NilGroup` (class ≤ 4) on random inputs for Heis(F_5), n4(F_5),
  n4(F_7), n5(F_7) (test).
- **BCH in brackets.** log(e^x e^y) is computed in the free associative algebra to degree d,
  then written with the Dynkin-Specht-Wever map in right-nested brackets
  [a_1,[a_2,…,[x,y]]], normalised to words ending in xy; the expansion is re-expanded and
  compared exactly (it raises otherwise). Nodes: class 2: [x,y] (1/2); class 3: + [x,[x,y]]
  (1/12), [y,[x,y]] (−1/12); class 4: + [x,[y,[x,y]]] and [y,[x,[x,y]]] (−1/48 each); class 5:
  13 nodes. Each distinct suffix bracket is one workspace register, restricted to the
  coordinates its bracket can reach in G_d (nodes whose bracket vanishes are dropped).
- **Encoding.** b = ⌈log₂ p⌉ qubits per coordinate, value Σ b_i 2^i, words ≥ p padding.
  A controlled increment t += k is the product of the p − 1 transpositions of the cycle
  x ↦ x + k (for k > (p−1)/2 the reversed sequence of −k); each transposition (u, v) is a
  Gray-code-conjugated MCX (2h − 1 gates, h the Hamming distance) that fixes every other word
  of t, padding included. A control "qudit = v" tests the smallest bit set that singles v out
  among canonical words (one bit for p = 3, so this reproduces the old construction exactly).
  Macros: add_scaled t += αa = (p − 1) increments, add_product t += αab = (p − 1)² increments.
  QFT_p is one exact b-qubit unitary F_p ⊕ 1 (small p only). The oracle is a `TableOracle`
  gate whose definition is the table of fully controlled MCX gates (`rees_circuit.oracle_gate`
  generalised); it is T_f and is not counted.

## 2. The emitted circuits

Per terminal sample, depth first (N_d = Π_{k=2}^d M_k sources of grade d):

1. **Source** (N_c times): QFT_p on the D_c = n cover coordinates; for each point s: w += E_s(a),
   U_f(w, y_s), w −= E_s(a). Labels are never touched again.
2. **Instrument at grade d** on each grade-d source: per top coordinate j ancilla QFT_p,
   a_top_j −= z_j (R_z|x⟩ = |x z^{-1}⟩), inverse QFT_p; measure λ ∈ F_p^{g_d}.
3. **Classical SDE** Σ s_i^d λ_i = 0: `is_sde_solve` when M_d ≥ `columns_required(p, d, rank)`,
   else brute force over F_p^{M_d}; the merge is emitted for that record.
4. **Merge at grade d**: Q register (D_{d−1} coordinates) prepared by QFT_p; on each active
   target the four-pass schedule of thm:uniform-compilation(ii) with the class-d node set:
   compute all nodes (parents after children), copy W += x + g + Σ α_w [w], uncompute nodes in
   reverse; SWAP x, W; recompute the nodes for x_new and −g, W −= x_new − g + Σ α_w [w]', uncompute.
   σ (zero top grade) and δ_s are public and folded into the coefficients. Slots with s_i = 0
   get no gates. The Q register is the grade-(d−1) source.
5. **Readout**: QFT_p on the m grade-one coordinates, measure; nullspace = log H.

`terminal_sample_circuit` assembles this into one QuantumCircuit without register reuse
(82 qubits for Heis(F_3), 744 for n4(F_5)).

## 3. How it is simulated, and why it is exact

Every module is simulated from its own gate list; composition uses the two identities of the
2-November report (tensor product of disjoint sources; Schur-multiplier channel of a merge
that never targets Q), now in exact Z[ζ_p] arithmetic.

- **Source [exact].** The gate list must start with QFT_p on each address coordinate (checked;
  the QFT_p gate matrix equals F_p ⊕ 1 to 1e-12 [float]), and the rest is X/CX/MCX/SWAP/U_f
  (anything else raises). The rest is evaluated *bit-sliced* (64 inputs per machine word) on
  ALL |G_c| canonical addresses with zero workspace (78 125 for n4(F_5), 823 543 for n4(F_7)).
  Checked: the address is unchanged and the workspace is 0 on every input; the label fibres
  have equal size, the identity fibre S is a subgroup, every fibre is a left coset of S, and
  S = exp(h̃) (index sets compared). Hence ρ[x,y] = 1_S(x^{-1}y)/|G_c| exactly. The oracle is
  applied by its table; on n4(F_5) the expanded MCX oracle gives the identical result (test).
- **Instrument [float → exact].** The gate list is checked to split into one block per top
  coordinate (top qudit + ancilla, nothing touching lower grades). Each block's Operator
  (2b qubits) gives Kraus operators K_λ; checked to 1e-9: no padding leakage, Σ K_λ†K_λ = 1,
  K_λ = Σ_z k_λ(z) R_z (circulant), and p·Σ_z k(z) conj k(z+u) = ζ^{e(u)} (largest error
  7.5e-14). The rounded exponents then condition states exactly: φ'(g) = p^{-g_d} Σ_u ζ^{e(u)} φ(g+u).
- **Merge [proof-by-computation].** (a) Every gate lies in exactly one recorded macro, and each
  macro's gate slice is evaluated exhaustively on the canonical values of its 2-3 qudits and
  must equal its declared map (t += αa or t += αab), touching nothing else. (b) The macro
  program is replayed symbolically over F_p[q, x]; the final x must equal the classical BCH
  polynomial x * (−δ_s σ(q)) — written independently of the node derivation (the NilGroup
  formula for class ≤ 4) — and W, all node workspaces and Q must be 0 / unchanged; no gate
  targets Q. (a)+(b) prove the map on all canonical inputs. (c) Independently, the whole gate
  list is run bit-sliced: exhaustively for Heis(F_3) (2187 inputs) and n4(F_5) grade 2
  (9 765 625 inputs per s), and on 64 q-rows × all 78 125 x for n4(F_5) grade 3 (5·10^6 per s)
  [sampled], against `GroupLaw.mul`. (d) A trace check uses no BCH identity at all:
  T[q,r] = |G|^{-1} Σ_u φ(u^{-1} π_r^{-1}(π_q(u))) from the bit-level permutations equals φ(g_q g_r^{-1})
  exactly on sampled pairs.
- **States [exact].** Left-invariant ρ[x,y] = φ(x^{-1}y)/|G_d|, φ ∈ Z[ζ_p]^{G_d} with a rational
  scale. A merge output is ψ = F∘σ with F(y) = Π_i φ_i(δ_{s_i}(y)), and F is checked constant on
  central fibres (otherwise it raises), which is the descent identity of prop:descent. Readout
  P(k) = |G_1|^{-1} Σ_w ζ^{−k·w} ψ(w) must be rational and sum to 1.

## 4. Results

### 4.1 Heis(F_3), c = 2, points 1, 2, M_2 = 3 (reproduction)

| Check | Result | Label |
|---|---|---|
| All circuits identical to `rees_circuit.py` (instruction, qubit, clbit, ctrl_state; U_f definition) | yes | exact |
| Primitive counts / logical ops / transpiled profile of the assembled sample | equal: 6 oracle calls, 12 BCH passes, 12 brackets, 24 QFT_3; 5528 CX, 6647 u, depth 5103 | exact |
| Merge proved on all inputs; bit-level table = `rees_circuit.merge_table` = `bch_reference` | s = 1, 2 | proof / exact |
| 19 subgroups (12 non-normal): source = ρ_{exp h̃}, laws uniform on K_2^⊥, all 3198 cases give ρ_{H_1}, readout uniform on h^⊥ | 19/19 | exact |
| My exact states vs the old float source, branches and channel outputs | ≤ 1e-12 | float |
| Seeded runs (7 samples, 42 queries) | 38/38 recover | exact laws |

### 4.2 n4(F_5): [e1,e2] = e3, [e1,e3] = e4, c = 3, points 1, 2, 3

Cover dims (g_1, g_2, g_3) = (4, 2, 1), |G_3| = 5^7 = 78 125, |G_2| = 15 625, |G_1| = 625;
b = 3, label bits 10; CW arities M_3 = 2, M_2 = 5, so N_3 = 10 top sources (30 oracle calls)
per terminal sample. κ_3 = gcd(3, 4) = 1, so the IS solver applies at M_3 = 2 = rank + 1 and is
used for every grade-3 merge; κ_2 = 2 needs 8 (rank 1) or 18 (rank 2) columns > 5, so grade 2 is
brute force (3125 vectors) except all-zero label tuples (IS returns e_1).

| Subgroup | normal | grade 3 (|K^⊥|, tuples, cases) | grade 2 (|K^⊥|, tuples, cases) | pass |
|---|---|---|---|---|
| ⟨e2⟩ | no | 5, all, 120 | 25, 6 sampled of 25^5, 4364 | yes |
| ⟨e1⟩ | no | 5, all, 120 | 25, 6 sampled, 4364 | yes |
| ⟨e1+e3⟩ | no | 5, all, 120 | 25, 6 sampled, 4364 | yes |
| ⟨e2,e4⟩ | no | 1, all, 24 | 5, 6 sampled of 5^5, 6044 | yes |
| ⟨e1+e2,e3,e4⟩ (closure of e1+e2, e3) | yes | 1, all, 24 | 1, all, 3124 | yes |
| γ_2 = ⟨e3,e4⟩ | yes | 1, all, 24 | 1, all, 3124 | yes |
| ⟨e2,e3⟩ | no | 5, all, 120 | 5, 6 sampled, 6044 | yes |
| Z(G) = ⟨e4⟩ | yes | 1, all, 24 | 5, 6 sampled, 6044 | yes |
| trivial | yes | 5, all, 120 | 25, 6 sampled, 4364 | yes |

"Cases" are (label tuple, witness) pairs; for every tuple ALL its valid witnesses are merged.
Grade 3 is exhaustive over all label pairs [exact]; grade 2 is exhaustive for the two
subgroups with K_2^⊥ = 0 and otherwise uses the all-zero tuple, the constant tuple and 4
random tuples [sampled]. Each source law and every label law was checked in full [exact].
Note: `rees_end_to_end_sim.class_three_instances` calls the subgroup generated by e2, e3
"⟨e2,e3,e4⟩ normal"; its Lie closure is ⟨e2,e3⟩, which is NOT normal ([e1,e3] = e4). My
list renames it, so 5 of the 9 are non-normal.

Other n4(F_5) results: instrument blocks at grades 2, 3 pass with largest error 7.5e-14
[float]; merges for d = 2, 3 and s = 1..4 are proved (41 and 69 macros) [proof]; the bit-level
runs agree with BCH on every input tried (4 × 9 765 625 at d = 2, 4 × 5 000 000 at d = 3);
18 seeded runs (8 samples, 240 queries each) recover log H; with M_2 = 18 the IS solver runs
at both grades (108 grade-3 and 6 grade-2 solves per run, 648 queries) and 9/9 runs recover.

### 4.3 n4(F_7) (largest instance)

Cover dims (4, 2, 1), |G_3| = 823 543, |G_2| = 117 649, |G_1| = 2401; b = 3, label bits 12;
CW arities M_3 = gcd(3, 6)·1 + 1 = 4 and M_2 = gcd(2, 6)·2 + 1 = 5. Here κ_3 = 3 and κ_2 = 2 need
216 and 18-324 IS columns, so the solver is brute force except for all-zero label tuples.

- Sources [exact]: all 9 equal exp(h̃) (identity fibres of order 7, 7, 7, 2401, 117 649, 16 807,
  343, 343, 1 for the rows of the n4(F_5) table, in that order), clean workspaces; bit-sliced
  over all 823 543 addresses.
- Label laws [exact]: uniform on K_d^⊥ at both grades for every subgroup.
- Merges [proof-by-computation]: d = 2, 3 and s = 1..6 proved; bit-level on 16 q-rows × all x
  (1 882 384 inputs per s at d = 2, 13 176 688 at d = 3) [sampled], all equal to BCH.
- Merge outputs [sampled]: per subgroup and grade 48 (tuple, witness) cases: 4 tuples
  (all-zero, constant, 2 random; repeated when K_d^⊥ = 0) with 12 random valid witnesses each;
  864 cases in all, every one equal to ρ_{H_(d−1)}.
- Seeded runs: 9/9 recover log H (6 samples, 360 oracle queries each).
- Instrument blocks: largest rounding error 2.7e-13 [float].

This is far weaker coverage than n4(F_5) at grade 2, and is reported as such.

## 5. Resource counts as a function of (m, c, p)

Notation: m = dim L, g_d = dim γ_d, D_d = Σ_{k≤d} g_k (n = D_c ≤ cm), M_d the merge arities,
N_d = Π_{k=2}^d M_k, β_d the BCH nodes at class d (1, 3, 5 for d = 2, 3, 4), ω_d the workspace
coordinates of those nodes, b = ⌈log₂ p⌉, ℓ = ⌈log₂ p^m⌉ label bits. Per terminal sample (all
witness entries nonzero), from the circuit's own counters and tested equal to these formulas
(`primitive_formula`, `width_formula`):

| Primitive | Count |
|---|---|
| Coherent oracle calls; E_s compute; E_s uncompute | c N_c each |
| QFT_p | D_c N_c + Σ_{d=2}^c (2 g_d N_d + D_{d−1} N_{d−1}) + m |
| Central subtractions / label measurements | Σ_{d=2}^c g_d N_d |
| Controlled right actions | Σ_{d=2}^c N_d |
| BCH passes | 4 Σ_d N_d |
| Bracket evaluations | 4 Σ_d β_d N_d ≤ 4 Σ_d N_d (d−1)d(d+1)(d+2)/6 (thm:uniform-compilation(i)) |
| Qubits, no reuse | b [N_c D_c + m + Σ_{d≥2} g_d N_d + Σ_{d<c} D_d N_d + Σ_{d≥2}(D_d + ω_d)] + c ℓ N_c |

Gates. Every add_scaled macro costs exactly A_p = Σ_{k=1}^{p−1} τ(k) gates, τ(k) = Σ (2h−1) over
the transpositions of x ↦ x+k, independent of the coefficient; every add_product costs (p−1)A_p.
A_3 = 8, A_5 = 36, A_7 = 88; in general A_p ≤ (p−1)²(2b−1). Per module, the macro counts are:
source 2c·nnz(E) add_scaled (nnz(E) = Σ_k nnz of the γ_k basis ≤ nm); instrument g_d add_scaled;
merge 2(D_d + D_{d−1} + Σ_{α_w≠0}|supp w|) add_scaled and 4 Σ_w nnz_w(T) ≤ 4 β_d D_d³ add_product,
plus b D_d SWAPs. So the logical gate count is
A_p·(#add_scaled + (p−1)·#add_product) + #SWAP, i.e. poly(m, c)·Π_d M_d·O(p³ log p).
**This is a small-p synthesis: the arithmetic is exponential in log p**, unlike the
poly(log p) arithmetic assumed by thm:uniform-compilation; see Section 8.

Measured (module sums with multiplicities, all s = 1; `resource_table.json`):

| Instance | m | c | p | M_d | N_c | oracle calls | BCH passes | brackets (bound) | qubits | logical gates | CX (transpiled, module sum) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Heis(F_3) | 3 | 2 | 3 | 3 | 3 | 6 | 12 | 12 (48) | 82 | 1 224 | 5 520 (5 528 assembled, s = (1,2,1)) |
| Heis(F_5) | 3 | 2 | 5 | 3 | 3 | 6 | 12 | 12 (48) | 120 | 7 080 | 94 992 |
| Heis(F_7) | 3 | 2 | 7 | 3 | 3 | 6 | 12 | 12 (48) | 132 | 21 444 | not transpiled |
| n4(F_5) | 4 | 3 | 5 | M_3=2, M_2=5 | 10 | 30 | 60 | 140 (880) | 744 | 91 168 | 1 344 362 |
| n4(F_7) | 4 | 3 | 7 | M_3=4, M_2=5 | 20 | 60 | 100 | 260 (1 680) | 1 404 | 531 388 | not transpiled |
| n5(F_5) | 5 | 4 | 5 | M_4=5, M_3=3, M_2=7 | 105 | 420 | 532 | 2 380 (26 992) | 10 002 | 2 061 342 | not transpiled |
| n5(F_7) | 5 | 4 | 7 | M_4=3, M_3=7, M_2=7 | 147 | 588 | 812 | 3 556 (39 312) | 16 302 | 10 075 866 | not transpiled |

n4(F_5) per-module CX: source 16 113, instrument 644 (d = 2) / 322 (d = 3), merge 48 632
(d = 2) / 93 291 (d = 3), Q preparation 76 / 114, readout 76. The two n5 rows are generated
and counted, not simulated. Primitive counts depend on (m, c, p) only through D_d, g_d and the
arities; the arities (here Chevalley-Warning) dominate through N_c = Π M_d.

## 6. Negative controls (the checks can fail)

| Broken variant | Detected by | Result |
|---|---|---|
| Merge without the Bennett uncompute (Heis d = 2; n4 d = 2, 3) | symbolic replay: W, workspaces ≠ 0 | caught (x still correct) |
| Class-two BCH used on the class-three quotient G_3 of n4 | symbolic replay vs classical BCH | caught |
| Two evaluation points (1, 2) instead of c = 3 on n4, H trivial | identity fibre larger than exp(h̃) = 1 | caught |
| Evaluation workspace not uncomputed (n4, ⟨e2⟩) | workspace ≠ 0, fibre ≠ exp(h̃) | caught |
| Non-witness scales (n4, ⟨e1⟩, labels (1, 2), s ∈ {(1,1), (1,2), (2,2)}) | no descent or output ≠ ρ_{H_2} | 3/3 caught |
| One gate of an add_scaled slice replaced by an X on its target (n4 d = 3 merge) | `check_macros` exhaustive slice check | raises |

## 7. Largest instance simulated, and what blocks the next one

Largest simulated: **n4(F_7)** (Section 4.3), |G_3| = 823 543. Its run took 17.5 min on the
loaded machine (4.6 min for the merge proofs and bit-level runs, about 1 min per subgroup).

Class four is the next step. The smallest class-four Lazard algebra is the filiform n5 (dim 5,
γ dims 5, 3, 2, 1), so |G_4| = p^11 ≥ 5^11 ≈ 4.9·10^7. The generator emits and counts its
circuits (table above), and the bit-sliced source evaluation would fit (≈ 88 qubit columns of
7.6·10^5 words, ≈ 0.5 GB). What blocks it is the state representation: a dense Z[ζ_5] vector
on G_4 is 4.9·10^7 × 5 int64 ≈ 2 GB, the source, up to 5 conditioned branches and the running
Schur product are live at once, and the shared machine has 16 GB with little free. The fix is
known and not built: every state in the run is supported on a coset-sized set
(exp(h̃)·Z_d, then H_d·Z_d), so a sparse support representation costs O(|H̃| p^{g_d}) per
state instead of O(|G_d|). The second blocker, for exhaustive grade-2 tuple coverage, is the
case count (|K^⊥|^{M_d}·p^{M_d}/|K^⊥|), which is why grade 2 is sampled already at n4.

## 8. What this establishes and what it does not

Establishes, for the instances above: a single generator, driven only by structure constants,
points, the oracle table and arities, emits explicit binary gate lists for every quantum step
of the Rees algorithm at class c (here c = 2, 3 simulated; c = 4 generated). It reproduces the
fixed Heis(F_3) circuit exactly, and on n4(F_5) its simulated modules give exactly the
intermediate states and label laws of the paper and recover log H for subgroups including five
non-normal ones. Merges are proved correct on all canonical inputs by macro-level exhaustion
plus symbolic replay against the classical BCH polynomial.

Does **not** establish:
- anything asymptotic (finite instances only; the size bound is still the written argument);
- poly(log p) arithmetic: the value-controlled increments cost Θ(p² log p) gates per
  add_scaled and Θ(p³ log p) per add_product; a scalable compile needs binary modular adders
  and multipliers, and finite-gate approximate QFT_p (thm:uniform-compilation(iii));
- Schedule 1 at its paper arity B_d(g_d): the IS solver runs at its actual column count
  (2 at κ = 1, 18 at κ = 2 with rank 2 for p = 5), and grade 2 at CW arity is brute force;
- a coherent receiver: the SDE solve is classical feed-forward between quantum segments, and
  the assembled circuit is defined per classical record;
- a monolithic simulation: modules are composed by the tensor/Schur identities; the
  instrument is checked in floating point and then rounded to exact exponents;
- exhaustive grade-2 tuple coverage at n4 (sampled), or exhaustive bit-level evaluation of the
  grade-3 merge (proved symbolically; bit-level on 5·10^6 of 1.2·10^9 inputs per s);
- identity on padding words for multi-coordinate arithmetic: each target coordinate's padding
  is fixed, but controls test only distinguishing bits, so padding *controls* can fire; only
  canonical inputs are promised and checked (as in the 2-November report);
- noise, the oracle cost T_f, hardware, or human review.

## 9. Artifacts (`research/audits/reviews/2026-11-03-rees-circuit-2/`)

- `pytest_fast.out`, `pytest_slow.out`: test logs.
- `report_main.json` / `.out`: Heis(F_3), n4(F_5), n4(F_5) at M_2 = 18 (checks, merge proofs,
  bit-level flags, instrument errors, seeded runs, resource reports). Runtime 4 min 50 s.
- `report_n4_f7.json` / `.out`: n4(F_7).
- `resource_table.py`, `resource_table.json`, `resource_table.out`: Section 5 table.

## 10. Exact statement that now holds (AI-checked, pending human review)

For L ∈ {Heis(F_3), n4(F_5), n4(F_7)} with points 1, …, c and
Chevalley-Warning arities, and for every listed subgroup H (all 19 of Heis(F_3); the same 9 of n4(F_5) and of n4(F_7), 5 of them non-normal): the Qiskit gate lists emitted by `theorems/rees_circuit_general.py`, simulated
module by module as in Section 3, produce lifted sources exactly equal to the coset density of
exp(h̃) with clean evaluation workspace; their central labels are exactly uniform on K_d^⊥ at
every grade; for every checked label tuple and every one of its valid witnesses (all tuples on
Heis(F_3) and at grade 3 of n4(F_5); sampled tuples at grade 2 of n4(F_5); sampled tuples and
witnesses at both grades of n4(F_7)) the merge output is
exactly ρ_{H_(d−1)}; the readout is uniform on h^⊥, so its annihilator is log H; and seeded runs
from oracle access recover log H. Each emitted merge gate list equals
x ↦ x * (−δ_s(σ(q))) on all canonical inputs with scratch returned to zero (proof by
computation). On Heis(F_3) the emitted circuits are identical to those of
`theorems/rees_circuit.py`.

**Still missing:** poly(log p) modular arithmetic and finite-gate QFT synthesis; a sparse state
representation (to simulate class four); exhaustive grade-2 coverage at class three; Schedule 1
at its paper arity inside the flow; a coherent (non-feed-forward) receiver; identity-on-padding
arithmetic if the compilation note's convention is kept; human review.

**Claim gates that must stay false** (none was touched): `coherent_receiver_implemented` (this
is still a simulated finite instance with a classical solve), `general_sde_implemented`,
`formal_compiler_checked`, `independent_review`, `novelty_established`, `speedup_claim_allowed`.

## 11. Proposed paper text

Target: `main.tex`, Section~\ref{sec:uniform-compilation}, replacing the current paragraph
"Gate-level control" (before `\subsection{Reproducible Resource Profiles}`). Status: finite
computation; AI-checked, pending human review. If the integrator uses the counts, regenerate
them from `resource_report()` / `resource_table.py`, not by retyping.

```latex
\paragraph{Gate-level control.} The artifact \file{theorems/rees_circuit_general.py} (report \file{research/audits/reviews/2026-11-03-rees-circuit-2.md}; finite computation, AI-checked, pending human review) generates explicit Qiskit circuits for the whole procedure from the structure constants of $\mathcal{L}$, the evaluation points, the oracle table and the merge arities, for any class $c<p$. Each $\Fp$ coordinate uses $\lceil\log_2 p\rceil$ qubits; arithmetic uses only $X$, CNOT, multi-controlled $X$ and SWAP gates, and $\mathrm{QFT}_{\Fp}$ is one exact unitary, so this is a small-$p$ synthesis whose arithmetic costs $O(p^3\log p)$ gates per multiplication rather than the $\poly(\log p)$ of~(iii). The circuits make $c$ coherent oracle calls per source with uncomputed evaluation workspaces, apply the complete central instrument at every grade, implement $x \mapsto x \ast (-\delta_s(\sigma(q)))$ with the class-$d$ BCH law in right-nested brackets and the four passes of~(ii), and end with abelian Fourier sampling; the diagonal equation is solved classically between quantum segments, by the deterministic solver of Section~
ef{sec:sde} where the arity reaches its column count. On the Heisenberg group over $\mathbb{F}_3$ the generated circuits coincide gate for gate with those of \file{theorems/rees_circuit.py} ($82$ qubits, $6$ oracle calls, $12$ BCH passes, $5528$ CNOTs per terminal sample, excluding the oracle). On the class-three filiform algebra $[e_1,e_2]=e_3$, $[e_1,e_3]=e_4$ over $\mathbb{F}_5$ (cover dimensions $(4,2,1)$, arities $M_3=2$, $M_2=5$) one terminal sample uses $744$ qubits, $30$ oracle calls, $60$ BCH passes and $140$ bracket evaluations (the bound in~(i) gives $880$). Each merge gate list is proved, on all canonical inputs, to equal the BCH right translation with clean scratch, by exhaustive checks of its arithmetic blocks and a symbolic replay over $\Fp[q,x]$. The modules are simulated exactly in $\mathbb{Z}[\zeta_p]$ and composed through the tensor and Schur-product structure of Proposition~\ref{prop:descent}. For nine subgroups, five of them nonnormal, every source equals the coset density of $\exp(\hlift)$, every label law is uniform on $K_d^\perp$ at both grades, every checked merge output (all label pairs and witnesses at grade three, sampled label tuples with all their witnesses at grade two) is $\rho_{H_{d-1}}$, and seeded runs recover $\hh$. These are fixed finite instances with an exact Fourier transform and a classical solve between quantum segments; they are not a coherent receiver for general $(G,H)$ and test no asymptotic cost.
```

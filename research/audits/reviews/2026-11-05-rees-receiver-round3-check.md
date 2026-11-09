# Check of the Rees receiver round 3 (coset symmetries, exact level-0 law at c = 3)

5 November 2026. AI-only adversarial check (Claude Code, Opus 5.5), written by the integrator of
I225. Not human review. Subject: `2026-11-05-rees-receiver-round3.md` (Sections 2, 3, 5, 9, 11), its
folder, `theorems/rees_circuit_mono_c3.py`, `tests/test_rees_circuit_round3.py`. No git, no network,
`make_numbers.py` not run, no claim gate touched (`coherent_receiver_implemented` stays false in both
modules and in every JSON read). AI-checked, pending human review.

## Verdict

No Error and no Gap in the two lemmas or in the computation they reduce. Three wording problems in
the proposed paper text, fixed in the integrated version (Section 6):

1. (a) and (c) present the gamma_2 / <e1+e2,e3> law as "the exact output law of the whole circuit"
   without saying that it is exact only **through two hand proofs** whose action hypotheses partly
   rest on other reports. Fixed: "two lemmas proved by hand, not machine-checked", "through the two
   lemmas", and one sentence on where the action hypotheses come from.
2. (b) "in the other 15 the dropped gate never acts on the reachable state" is stronger than what
   was checked. It holds for the **simulated** state (one coset; one label tuple at the root), not
   for every reachable state of the unconditioned circuit. Two root mutants are caught on one tuple
   and equivalent on the other, which shows the difference. Fixed.
3. (a) would make the next, unchanged sentence of the paper ("The exact computation also compares
   ... All of these hold for all 19 subgroups") read as being about the new c = 3 computation. Fixed
   with "The exact computation over F_3 also compares". This is one extra word-level edit outside
   the three proposed sentences.

Smaller fixes: "coset" -> "left coset" (twice); "tried" -> "run"; the final transform is applied
analytically from the Gram matrices, not gate by gate (report Section 1.4), so (a) now says "up to
the final transform"; (a) states that the whole-circuit law of the other seven was not computed;
(c) names `rees_circuit_mono_c3.py` and keeps a scope sentence ("It covers no other coherent-label
circuit"), because the old sentence ended with a coverage limit.

## 1. Lemma A re-derived

Setting: source address A (values in G_c), oracle outputs Y, rest of the circuit W (gates after the
source end), readout projectors Pi_y. L_g|x> = |gx>, S = exp(h~), cosets g_k S.

By KS, |Psi> = sum_k |C_k>|kappa_k> (x) |Phi>, with |C_k> = |G_c|^{-1/2} sum_{x in g_k S}|x> =
L_{g_k}|C_0>, orthonormal |kappa_k> (distinct keys on distinct cosets), |Phi> the other wires
(clean workspace). W never touches Y, so the branches do not interfere at the readout:
P(y) = sum_k ||Pi_y W(|C_k>|Phi>)||^2.

Claim: W L_g v = L_g W v for v in the span V of basis states with canonical A and clean workspace,
along the run. Split W into gates that do not touch A (they commute with L_g as operators, since
L_g acts on A only) and the two segments that do: the instrument |x>|z> -> |x z^{-1}>|z> (z in the
central top coordinates) and the controlled merge ctrl_i, bch_i, ctrl_i^{-1}:
|x>|s>|q> -> |x t(s,q)>|s>|q>. On V both are maps of the form |x>|r> -> |x u(r)>|r'> with u
independent of x, so L_g commutes with them: g(x u) = (g x) u. L_g preserves V, and the input to each
segment is in V on every branch because each module leaves its scratch clean on all canonical
inputs. Induction over the gate list gives W L_g = L_g W on the run. Pi_y acts on neither A nor Y,
so ||Pi_y W L_{g_k}(C_0 (x) Phi)|| = ||L_{g_k} Pi_y W(C_0 (x) Phi)|| = ||Pi_y W(C_0 (x) Phi)||.
Hence P(y) = #cosets * ||Pi_y W(C_0 (x) Phi)||^2. With ||C_k||^2 = 1/#cosets, P(Y = kappa_0) =
1/#cosets and P(y | Y = kappa_0) = P(y). Any C_k works. The proof does not use normality of S, but
it needs left cosets: the reviewer's control (right coset Sg on <e2> changes rho_Q2 and fails K5_2)
confirms this.

Sequential use on 12 (resp. 18) sources is valid. A conditioned source is a projector on its Y,
which no later gate touches, so it can be moved to the end. It then acts on wires other than the
next source's A and Y, and so satisfies hypothesis (4) of the next application.

## 2. Lemma B re-derived

At the end of the grade-3 merge block of node j, the global state is a product over the six
subtrees (disjoint wires; clean shared workspace, K4). The traced wires of subtree j are never
touched again, so every later probability is Tr(Pi W (sigma_j (x) rest) W^dagger) with sigma_j = rho_j
on Q_2j. By K5_2, rho_j = c sum_k |C'_k><C'_k| = c sum_k L_{g_k}|C'_0><C'_0|L_{g_k}^dagger. Later
gates touching Q_2j are the grade-2 instrument (a central translation of the top coordinates; its
QFTs act on the label only) and the root merge of child j (a right translation by t(s, q), where
t does not depend on Q_2j). Both commute with L_g. The readout and the label projector act on other
wires. So each term gives the same law, and the law equals #cosets * c times the law with
|C'_0><C'_0|. The two are equal once both are normalised. The label projector is applied right
after the instruments in `phase_b`. It may be moved to the end, because later gates use the labels
only as controls: `block_structure` holds, and `labels_and_Q1_unchanged` is checked on the run.
K5_2 per grade-3 label tuple (the hubs are orthogonal) implies K5_2 for the total. Lemma B is
applied to the circuit already conditioned by Lemma A. That is legitimate: c > 0 absorbs the norm.

## 3. Hypotheses on the program (code read)

- KS (`M.source_coset_check`): every address once, equal amplitudes, (A, Y) in a factor with no
  other wire, workspace constant 0, and #(key, coset) pairs = #keys = #cosets (a bijection between
  key values and left cosets). This is exactly Lemma A (1).
- `condition_on_coset`: a projector on the Y bits equal to key(x0). The state is not renormalised,
  which is harmless because the law is scale-free.
- `lemma_hypotheses_check`: for each source, Y is untouched after the source end (the step before
  the first QFT on its label register); every later step touching A is in its own contiguous
  instrument run, inside its label-register instrument steps and touching no other child's
  address, or in one interval of `witness_control_grade3`/`bch_merge_grade3` steps that touches no
  other child. U_SDE (`sde_grade3`) steps may not touch A at all. Because `touched_wires` includes
  controls, U_SDE does not even read the address. The Q_2 checks are the same, with the node's own
  grade-2 instrument range and the root's merge components. The final QFT acts on Q_1 only and
  comes last. Re-run: `relabeling.json` reproduced (anatomy, relabeling, lemma hypotheses all
  True). Limitation, stated in report Section 7 and now in the paper sentence: the check certifies
  where the gates are, not what they do. That each segment acts as the stated translation on every
  input rests on `prove_controlled_merge` (child 0 of each block, symbolic over F_p[s, q, x]), on
  `block_structure`, on the `rees_circuit_arith` exhaustive macro checks (instrument on addresses
  outside the conditioned coset), and on reading the code for children i > 0. K3 and K4 check
  children i > 0 on the reachable states only.
- Relabeling (nodes 1-5 = node 0 under a wire bijection fixing the workspace, oracle calls compared
  wire by wire against the one global table): this is what transfers K5_2 from node 0 to nodes 1-5
  for the four subgroups with node 0 only. The transfer is sound, because the initial state is all
  zero and the workspace is clean between nodes (K4).
- K5_2 (`phase_a`): built from the K4-verified rows (amplitudes are fixed per row, since only
  permutation gates run after Q_2 is prepared). It requires exactly nQ*|H_2| nonzero unique
  (q, q') pairs, all inside left cosets of H_2, with one positive rational value. That is
  proportionality to rho_{H_2}, and it is not vacuous.
- Phase B needs no oracle (`table = None`). The oracle enters only through Phase A (KS, K5_2), as
  the lemmas require. The law comes from the total Gram matrix, with hubs that differ on a
  classical wire set orthogonal, and the final QFT is applied analytically.

## 4. Is the "exact law of the whole circuit" exact?

For gamma_2 and <e1+e2,e3> (K_2^perp = 0, one grade-2 label value, so `label_tuple = None`, no
projector), the Phase-B law is the exact law of the circuit in which each Q_2 is replaced by |H_2>.
It equals the law of the whole terminal sample **conditionally on** (i) Lemmas A and B (hand
proofs; I re-derived both; not machine-checked); (ii) the action hypotheses (3), which partly rest
on other reports and on code reading (Section 3); (iii) K5_2 on node 0 only, with nodes 1-5 by the
relabeling check, and for <e1+e2,e3> on three hub ranges combined by `combine_hub_ranges`
(partition, every range passes, identical signature; the identity of the signatures holds by
construction, as the report says). Given (i)-(iii), the law is exact arithmetic in Z[zeta_5], not
sampled. So it is not an unconditional direct simulation. It is "proved + finite computation", and
the paper text now says "through the two lemmas".

For the other seven subgroups the law is exact only conditionally on each of the 13 stated grade-2
label tuples. Checked from the JSONs: for each subgroup, 13 distinct tuples, all checkpoints pass,
all uniform, and one law signature. The whole-circuit law (the average over 5^6 or 25^6 tuples) is
not computed. The integrated text says this explicitly.

## 5. The 15 mutants with an unchanged final state

Read from the four negative-control JSONs: Phase A 3 (source_evaluation ccx middle,
bch_merge_grade3 cx middle and ccx middle), Phase B 6 on each tuple. Totals: 17 caught, 7 guard,
15 equivalent, 0 missed, 39 runs.

- Phase B: `state_signature` covers every wire and amplitude. The merge segment is a sequence of
  permutations after the label projector, so B G A psi = B A psi gives G A psi = A psi. The dropped
  gate acts trivially on the state reached in that conditional run.
- Phase A, merge mutants: the recorded signature covers only the child addresses. But these
  mutants pass every K4 check (labels and Q_2 unchanged, no local wire other than the addresses,
  every other hub wire zero), so the whole final state is identical, and the same argument applies.
- Phase A, source_evaluation ccx(4,16->5) middle: the dropped gate comes before the conditioning
  projector, so the argument above does not apply directly. **Own check**
  (`scratchpad/rx3/mutant_src.py`, not a repo file): the full joint state of all 51 live wires at
  the end of source 0, before conditioning, is identical with and without the gate. So the gate
  acts trivially on the reachable source state.

Conclusion: this is **not a gap in the checkpoint suite**. Identical states cannot be told apart
by any state check. The mutants are equivalent on the simulated states, which are one coset and
one or two root label tuples. Equivalence on all reachable states of the unconditioned circuit is
**not** established: sde_grade2 cx middle and witness_control_grade2 ccx middle are each caught on
one tuple and equivalent on the other. The proposed phrase "never acts on the reachable state"
was therefore reworded.

## 6. Re-runs (scratchpad `rx3/`, nice -n 10, one or two processes)

| command | recorded | re-run | RSS |
|---|---|---|---|
| `--mode relabel` | anatomy, relabeling, lemma hypotheses True | identical | 0.37 GB |
| `--mode A --names "Z(G)" --nodes 0` | pass; rho_Q2 d7799610..., final 40a618dd... | identical, 10 s | 1.48 GB |
| `--mode B --names "<e3,e4> = gamma_2"` | pass; uniform 25 points, 1/25; law 003b42d2..., state 39754d2f... | identical, 84 s | 1.35 GB |
| `--mode heis` | all_equal; 37 comparisons | identical rows, 37/37 true, 115 s | 0.86 GB |
| `--mode merge` | proved at grades 2 and 3 | identical | <0.4 GB |
| own mutant check (Section 5) | - | full source state identical | <1 GB |

`pytest -q tests/test_rees_circuit_round3.py` (nice -n 10): **23 passed, 3 skipped** (the REES_SLOW
tests) in 50 s, 0.96 GB. JSON checks: closure ranges combined (all true); 13 distinct tuples and one
signature per subgroup for the seven; f7 Phase B Z(G) has 3 tuples, uniform on 343 points, one
signature; f7 sources 54 node runs, 162 KS checks, all pass.

## 7. Verdicts on the proposed text (report Section 9)

**(a) Accept with rewording.** Integrated text:

> Over $\mathbb{F}_5$ the conditional readout law is exactly uniform on $\hh^\perp$ for all $56$ terminal samples of seven of the nine subgroups, the five nonnormal ones included, and all seven seeded runs recover $\hh$. With nothing measured before the readout, two symmetries make the exact computation fit (report \file{research/audits/reviews/2026-11-05-rees-receiver-round3.md}, check \file{research/audits/reviews/2026-11-05-rees-receiver-round3-check.md}; two lemmas proved by hand, not machine-checked, and finite computation, AI-checked, pending human review). After its oracle calls, the address of a top source is touched only by its instrument, a central translation, and by its merge, a right translation, and its oracle outputs, which determine exactly the left coset of $\exp(\hlift)$ of the address, are never touched again; both translations commute with left translation, so conditioning the oracle outputs on the key of one left coset leaves the output law unchanged. Likewise, once the reduced state of each $Q$ of grade two is $\rho_{H_2}$, that $Q$ may be replaced by the uniform state of one left coset of $H_2$. The footprint hypotheses of both lemmas are read off the program; that the instruments and merges act as these translations on every input rests on the exhaustive checks of their arithmetic blocks and on a symbolic replay of the merge of one child per block. Every gate of one subtree of grade two and of the root, up to the final transform, whose law follows exactly from the Gram matrices, then acts on one exact state over $\mathbb{Z}[\zeta_5]$, written as an orthogonal sum over the values of the labels and $Q$, at most $390625$ terms at grade three. The other five subtrees equal the first up to a bijection of wires, which is checked; for five of the subgroups they were also simulated. For $\gamma_2(\mathcal{L})$ and $\langle e_1+e_2,e_3\rangle$, whose grade-two labels are deterministic, this gives, through the two lemmas, the exact output law of the whole circuit, and it is uniform on $\hh^\perp$. For the other seven subgroups the readout law conditioned on stated grade-two labels is exactly uniform on $\hh^\perp$ for each of the $13$ label tuples run, out of $5^6$ or $25^6$; their output law of the whole circuit, the average over all label tuples, is not computed.

plus the next sentence "The exact computation also compares" -> "The exact computation over
$\mathbb{F}_3$ also compares".

**(b) Accept with rewording.** Integrated text (after "... at $H=Z(G)$ over $\mathbb{F}_3$."):

> At $c=3$ over $\mathbb{F}_5$ the same comparisons now run on the exact state of the computation above, for every hub: the source state, the instruments on the conditioned coset, the workspace at every merge component, every child after each merge block against its right translation by $-\delta_s(\sigma(q))$ with the reference witness, the reduced state of each $Q$ of grade two against $\rho_{H_2}$ for every label pair, and that of the root $Q$ against $\rho_{H_1}$; they hold for all nine subgroups, the grade-three merges on one of the six identical subtrees for four of them and on all six for the other five, and the checks at the root on every label tuple run. Of $39$ deterministic mutant runs at $c=3$ on $\langle e_2\rangle$, which change one oracle entry, drop one gate in a module or modify the merge block ($15$ in a subtree of grade two, and $12$ at the root for each of two label tuples), $17$ fail one of these checks, $7$ stop at a structural guard of the simulation, and in the other $15$ the simulated state is left unchanged, so the dropped gate acts trivially on the states reached in that run, for one coset and one label tuple (two root mutants are caught on one of the two tuples only). On the zero label tuple the four failing root mutants that reach the readout, among them the merge with the opposite sign of the translation, have an exactly uniform conditional readout law.

**(c) Accept with rewording.** Integrated text:

> Every exact simulation uses the exact Fourier transform; the monolithic simulation of \file{theorems/rees_circuit_mono.py} and \file{theorems/rees_circuit_mono_c3.py} gives the exact output law over $\mathbb{F}_3$, and over $\mathbb{F}_5$, through the two symmetry lemmas above, for the two subgroups with deterministic grade-two labels and conditionally on $13$ stated grade-two label tuples for each of the other seven; over $\mathbb{F}_7$ it covers the top sources of the fifth backend, run from their gate lists on all $7^7$ addresses for all nine subgroups, and for $H=Z(G)$ the merges at both grades (at grade three on one of the six identical subtrees), with the readout law exactly uniform on $\hh^\perp$ conditionally on three stated grade-two label tuples. It covers no other coherent-label circuit.

`core/main-core.tex` has no sentence about the receiver simulations, so it was not edited.

## 8. Not checked here

The three REES_SLOW tests; the long runs (<e1+e2,e3> Phase A ranges, <e2,e3> Phase A, f7 Phase A
and B); the `rees_circuit_arith` macro proofs (cited, not re-run). `--mode merge` was re-run
(`prove_controlled_merge` proved at grades 2 and 3, 48 and 82 macros; `block_structure` true;
identical to `merge_proofs_f5.json` apart from timings).

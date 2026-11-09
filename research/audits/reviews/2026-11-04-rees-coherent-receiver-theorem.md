# Rees HSP: a general coherent receiver at the arities of Theorem thm:main (existence theorem)

4 November 2026. AI-only session (Claude Code, Opus 5.5). Not human review, not Lean.
**Status: AI-checked, pending human review.** Labels: **[proved]** = written argument here;
**[argued]** = reasoning not written out to the end; **[cited]** = a standard result taken
from the literature.

Sources read: `docs/papers/rees-hsp/main.tex` lines 128-240 (thm:main, cost display), 343-500
(cover, lifts, instrument), 494-600 (sec:sde, prop:descent, sec:recursion, lem:hybrid, proof
of thm:main, thm:is-import, rem:is-import, Schedule 1), 599-660 (Schedules 2 and the
triangular solver), 700-806 (thm:uniform-compilation, lem:qft-mod, Gate-level control,
Binary arithmetic, Coherent-label backends, Scope, lem:coherent-linear-sde,
lem:coherent-quadratic-sde, lem:coherent-power-sde and the paragraphs after them);
`references.bib`; `research/audits/reviews/2026-11-02-rees-is-solver.md` Sections 0-3, 7-9;
`research/audits/reviews/2026-11-04-rees-circuit-coherent.md` Section 1;
`research/reductions/rees_hsp_reduction.json` (claim gates). No `.tex` file and no code was
edited. Nothing was committed.

## 0. Verdict

**Yes, at the level of theory, and fully proved conditional exactly as thm:main is
(on Theorem thm:is-import).** Under Schedule 1 every classical step that sits between
quantum segments of thm:main's algorithm is a *deterministic, total, data-independent-in-
shape* function of the measured labels. Nothing is adaptive in the number of branches,
nothing restarts, nothing aborts, and the tree shape and the instrument count N_instr are
fixed before the run (sec:recursion says so explicitly, and the solver third of the error
budget is unused). So:

- the Schedule-1 solver lambda -> s(lambda) compiles, through an oblivious Boolean circuit
  (Pippenger-Fischer) and Bennett's compute-copy-uncompute, into an exact permutation
  circuit W_d with clean workspace, whose input wires are used only as controls;
- the dilation delta_s controlled on a quantum s register costs 2(d-2+D_{d-1})
  multiply-accumulates per target, on top of the four-pass BCH right translation that the
  measured version already pays;
- the label registers, consumed targets and oracle outputs are left as garbage; the reduced
  state then equals the measured process's state (an explicit channel identity, Section 3.3,
  which is the deferred-measurement principle);
- the error analysis is unchanged: the same N_instr instruments, the same transforms, the
  same eta, the same lem:hybrid; the new blocks are exact permutations and contribute zero.

Nothing in Schedule 1 genuinely needs a measurement before the final Fourier readout. The
three things the paper lists as missing (coherent controlled dilation; composition over all
grades with error and gate analysis; grades with p in E_2(kappa_d), including kappa_d = p-1;
arities other than those of thm:main) are all supplied, because the reversible Schedule-1
solver works at every p > c and at M_d = B_d(g_d). The price is (i) the classical solver
work enters the quantum circuit with a factor O(log T) (plus a constant factor 4 for
compute/copy/uncompute twice), and (ii) the qubit count grows from the depth-first
O((sum_d M_d) n log p) of thm:uniform-compilation(iv) to O(c Q (m log p + w)), because no
garbage can be reset. Both are polynomial for fixed c.

**What it is not.** It is an existence theorem with explicit polynomial cost *in terms of
the Ivanyos-Santha running time T^IS_d*, whose exponent neither IS nor the paper states. No
code generates these circuits for general (G,H); `coherent_receiver_implemented` and
`general_sde_implemented` stay **false**.

## 1. Statement [proved, conditional on thm:is-import]

Notation as in the paper: b = ceil(log2 p); M_d = B_d(g_d); n_d = prod_{2<=d'<d} M_{d'}
(grade-d nodes per terminal sample); P = prod_{d=2}^c M_d; S = m + ceil(log_p(3/eps));
Q = cSP; D_k = sum_{j<=k} g_j; n = D_c; Gamma_x = 158 b^2 + 46 b (gates of one modular
multiply-accumulate of the second arithmetic backend); N_instr and q_max as in
sec:recursion and thm:uniform-compilation(iii).

Let T^IS_d be a bound, polynomial in (m, log p) for fixed c, on the number of steps of a
multitape Turing machine that maps any M_d g_d b-bit input (columns lambda_1..lambda_{M_d}
in F_p^{g_d}, b bits per entry) to the Schedule-1 witness s(lambda) in F_p^{M_d}: the
algorithm of thm:is-import at the exponent kappa_d, followed by the Bezout step of
rem:is-import(b). (Any polynomial time bound in a standard RAM model gives such a bound.)

**Proposition (coherent receiver).** Fix c >= 1 and assume thm:is-import. For every input of
thm:main (p > c, structure constants of L, eps, and oracle U_f or copies of rho_H) there is
a quantum circuit C such that:

1. **Measurement-free until readout.** C makes exactly the Q oracle calls of thm:main (or
   consumes its Q copies), applies otherwise only gates of a fixed finite universal gate set
   to fresh |0> qubits, and measures only at the end: S registers of m coordinates each, in
   the computational basis after QFT_p on every coordinate. No other qubit is measured or
   reset. The output is the nullspace of the S samples, as in thm:main.
2. **Exactness.** With exact transforms, the S readouts are i.i.d. uniform on hh^perp, which
   is exactly the readout law of thm:main's algorithm with exact instruments.
3. **Error.** With every QFT_p compiled as in thm:uniform-compilation(iii) at
   eta = eps/(3 N_instr q_max), the output distribution of C is within total variation
   eps/3 of the exact one; so C outputs a basis of hh with probability >= 1 - 2eps/3.
4. **Gates.**
   G_coh <= G_meas + 2 sum_{d=2}^c S n_d R_d + 2 Gamma_x sum_{d=2}^c S n_d M_d (d-2+D_{d-1})
         <= G_meas + (2Q/c) sum_{d=2}^c R_d / prod_{d'=d}^c M_{d'} + 2 Gamma_x Q (n + c),
   where G_meas is the number of gates (excluding the classical solver) that the proof of
   thm:main charges for the measured implementation with the same gate lists, and
   R_d <= C_0 T^IS_d log T^IS_d + M_d b for an absolute constant C_0 is the size of the
   reversible solver W_d. This is poly_c(m, log p, w, log 1/eps).
5. **Qubits.** At most Q((c+3) m b / 2 + w) + W, where W = O(max_d T^IS_d log T^IS_d) +
   (the clean workspace of one BCH translation and one transform) is reused by every block.
6. **Uniformity.** Given explicit polynomials T^IS_d, the gate list is computed classically
   in time polynomial in its length.

Remarks on the statement.

- Item 2 can be strengthened to exact equality with the *measured implemented* circuit if
  the latter is defined to use the same gate lists, to write its classical s into a register
  by X gates and to apply the same s-controlled dilation circuit (Section 3.3). The paper's
  measured circuits use constant multiplications for classical s instead, so only the
  comparison through the exact procedure (both within eps/3 of it) is claimed.
- The cost is "explicit" only up to T^IS_d. The IS paper and thm:is-import give
  "poly(M, log p)"; the solver report (`2026-11-02-rees-is-solver.md` Section 3) counts
  poly(a, log p) field operations with at most log2 p restarts for fixed kappa, but no
  explicit exponent has been extracted. For a uniform generator one needs it (item 6).

## 2. Inventory: every classical step of thm:main and how it is handled

Under Schedule 1 (thm:main fixes it at every grade), reading sec:sde, prop:descent,
sec:recursion, the proof of thm:main and thm:uniform-compilation:

| # | Classical step in the measured algorithm | Where | Coherent treatment |
|---|---|---|---|
| 1 | Public precomputation: bases of gamma_k(L), cover structure constants, section sigma, evaluation matrices of E_1..E_c, BCH recurrence constants (thm:uniform-compilation(i)), Bezout exponents t_d, arities M_d, N_instr, q_max, eta, QFT gate lists | thm:rees-cover, sec:recursion | Done by the circuit generator before the circuit; depends only on the input, never on a label. Not a step between quantum segments. |
| 2 | Measuring the central label lambda_i of each target | lem:central, sec:sde | Not measured. The ancilla after the inverse QFT is kept as the label register L_i. |
| 3 | Solving sum_i s_i^d lambda_i = 0 (IS at kappa_d) | thm:is-import, Schedule 1 | Reversible circuit W_d (Section 3.1), exact on every input word, input wires only as controls. |
| 4 | Bezout conversion s_i = u_i^{t_d} | rem:is-import(b) | Part of the function compiled into W_d. |
| 5 | Witness verification | sec:recursion "Solvers" item | Unnecessary: thm:is-import is deterministic and total at M_d >= B_{kappa_d}(g_d). |
| 6 | Solver retries, cut-offs, aborts (solver third of the budget) | sec:recursion | None under Schedule 1 ("this share is zero"). No repeat-until-success occurs. |
| 7 | Active-set selection: targets with s_i = 0 are discarded, delta_0 never applied | prop:descent | Automatic: delta_0(sigma(q)) = 0, so the controlled translation by -delta_0(sigma(q)) is exactly the identity (BCH(x,0) = x in the exact recurrence); the target is garbage like every other consumed target. |
| 8 | Choosing the dilation delta_{s_i} by classical s_i | prop:descent, thm:uniform-compilation(ii) | Quantum-controlled: powers s^2..s^{d-1} and G_j = -s^{k(j)} q_j by multiply-accumulates, then the same four-pass translation with G as a register, then uncompute G and the powers (Section 3.2). |
| 9 | Merge bookkeeping: which child outputs feed which node, tree shape, depth-first order | sec:recursion, thm:uniform-compilation(iv) | Data-independent (fixed arities, no restarts): hard-wired. |
| 10 | Independence of fresh disjoint preparations | prop:descent paragraph after proof | Automatic: disjoint subtrees act on disjoint registers, so the global state is a tensor product over subtrees (Section 3.3). |
| 11 | Discarding the c tuple labels of each lifted source (case a) / tracing out the c copies (case b) | after lem:homogeneous; lem:copy-lift | Same: left as garbage. |
| 12 | Final Fourier readout, rank failure, nullspace, generators of H | proof of thm:main | After the only measurement; classical post-processing. Rank failure stays in the first eps/3. |
| 13 | Uncomputing the witness after the merge | (coherent version only) | W_d^{-1}; the merge reads s and lambda but never writes them. Optional for correctness (s could stay as garbage), used to keep workspace reusable. |

**Steps that genuinely need measurement under Schedule 1: none.** The only measurements are
the final readouts.

Outside Schedule 1 (not part of the Proposition, see Section 6): Las Vegas solvers
(rem:is-import(d), Schedule 2's draws, Prop. triangular when g or roots are found at
random) need coin registers and a fixed number of attempts with flags; Schedule 3's tree
restarts consume fresh quantum sources and need a fixed number of parallel tree attempts
with coherent first-success selection. These change counts; they are not needed here.

## 3. Proof

### 3.1 The reversible solver W_d [proved, with cited ingredients]

Let F_d : {0,1}^{M_d g_d b} -> {0,1}^{M_d b} be the function computed by the multitape
machine of Section 1, clocked at exactly T = T^IS_d steps (output = the output-tape region
after T steps, so F_d is defined on every word, including non-canonical ones). On canonical
inputs F_d(lambda) = s(lambda) is nonzero with sum_i s_i^d lambda_i = 0 for every lambda,
because M_d = B_d(g_d) >= B_{kappa_d}(g_d) (rem:is-import(b)) and thm:is-import is total and
deterministic at that arity.

- [cited] Pippenger and Fischer (1979): a multitape machine with time T is simulated by an
  oblivious two-tape machine in time O(T log T), hence F_d is computed by a Boolean circuit
  over {AND, NOT} of size Sigma_d = O(T log T), constructible in time poly(T). (The simpler
  tableau construction gives O(T^2) and suffices for polynomiality.)
- [proved] Replace each AND gate by a Toffoli onto a fresh |0> qubit and each NOT by a
  CNOT onto a fresh qubit followed by X. This gives a permutation circuit
  V_d : |x>|0> -> |x>|g(x), F_d(x)> with at most 3 Sigma_d gates and Sigma_d ancillas, in
  which the input wires are used only as controls.
- [cited, Bennett 1973] W_d := V_d^{-1} (CNOT copy of the F_d(x) wires into a fresh
  M_d b-qubit register S) V_d maps |x>|0>_S|0>_anc -> |x>|F_d(x)>_S|0>_anc for **every** x,
  with R_d <= 6 Sigma_d + M_d b gates from {X, CNOT, Toffoli}, and again uses the x wires
  only as controls, so W_d = sum_x |x><x| (x) U_x is block-diagonal in the computational
  basis of the label registers.

The workspace is exactly clean on every input, so it is reused by the next block. Bennett's
1989 time-space tradeoff could cut the workspace to O(space * log T) at gates
O(T^{1+epsilon}); not needed for polynomiality.

### 3.2 The quantum-controlled dilation and translation [proved]

At a grade-d node, target i holds x_i in G_d (D_d coordinates); the fresh quotient address
q in G_{d-1} = Q (D_{d-1} coordinates, top grade zero by the section sigma). Prop:descent
applies R_{delta_{s_i}(sigma(q))}, i.e. x_i -> x_i * (-delta_{s_i}(sigma(q))) (R_g|x> =
|x g^{-1}>, inverse = negation in Lazard coordinates). Coherently, with s_i in register S_i:

1. compute s_i^2, ..., s_i^{d-1} into fresh registers (d-2 multiply-accumulates; s_i read
   only as control/multiplicand);
2. for each coordinate j of q of grade k(j) <= d-1, accumulate G_j <- G_j - s_i^{k(j)} q_j
   (D_{d-1} multiply-accumulates), so G = -delta_{s_i}(sigma(q)) exactly
   (thm:rees-cover(ii): delta_s multiplies grade k by s^k);
3. apply the clean two-register BCH right translation x_i -> x_i * G with the four passes
   of thm:uniform-compilation(ii) (compute x*G out of place by compute-copy-uncompute,
   erase x by recomputing (x*G)*(-G)); this block is the one the measured version already
   uses with G a register depending on q;
4. uncompute G and the powers by the reversed lists of 2 and 1.

Each step is an exact permutation of canonical basis states with clean workspace (the
arithmetic backend's blocks are; division in BCH is by public integers <= c, i.e.
multiplication by public constants). Extra cost against the measured version:
at most 2(d-2+D_{d-1}) multiply-accumulates, i.e. 2(d-2+D_{d-1}) Gamma_x gates, per target.
At s_i = 0, G = 0 and step 3 is the identity exactly, which is rule 7 of Section 2.

### 3.3 One merge node equals the measured channel [proved]

Fix a grade-d node. Its registers: the M_d child outputs X_1..X_{M_d} (each G_d), the
instrument ancillas L_1..L_{M_d} (each g_d coordinates), the address register A (Q), the
witness register S and workspace. Let J be the ideal complete central instrument on one
target, as an isometry: |psi>_X -> sum_lambda |lambda>_L (x) Pi_lambda|psi>_X (uniform central
ancilla by QFT on |0>, controlled central translation, inverse QFT; lem:central). For
lambda = (lambda_1..lambda_{M_d}) let U_lambda be the composite of Sections 3.1-3.2 with S
holding s(lambda): it acts on (X_1..X_{M_d}, A) by
prod_i R^{X_i}_{delta_{s_i(lambda)}(sigma(q))} (controlled on A) and leaves S and workspace
clean after W_d^{-1}. The coherent node is

  V = (sum_lambda |lambda><lambda|_L (x) U_lambda) (J^{(x) M_d} (x) (QFT-prepared |u_Q>_A)),

and its output is A after tracing out L, X_1..X_{M_d} (garbage). For any input state
omega on X_1..X_{M_d} (with a reference R),

  Tr_{L,X}[V (omega (x) |u_Q><u_Q|) V^dag]
    = sum_lambda Tr_X[ U_lambda (Pi_lambda omega Pi_lambda (x) |u_Q><u_Q|) U_lambda^dag ],

because tracing L kills the off-diagonal blocks |lambda><lambda'|, lambda != lambda', exactly
as U is block-diagonal in lambda (Section 3.1). The right side is, term by term, the
measured node of prop:descent on outcome lambda with the classical witness s(lambda),
weighted by its probability. For omega = rho_{H_d}^{(x) M_d} (independent copies),
lem:central and prop:descent give rho_{H_dZ_d/Z_d} = rho_{H_{d-1}} for
every positive-probability lambda, hence the sum is rho_{H_{d-1}}. (This is the
deferred-measurement principle written out; no citation needed.)

Composition over the tree. Every node acts only on its children's *output* registers and on
fresh registers, never on a child's garbage. Starting from |0> and the oracle (a fixed
unitary applied to disjoint registers) or from independent copies, the global pure state is
a tensor product over disjoint subtrees, and the reduced state on the set of all outputs of
one level is the tensor product of the per-subtree reduced outputs. Induction from d = c
(leaves: rho_{exp(hlift)} by lem:homogeneous or lem:copy-lift; the evaluation workspace is
uncomputed and the c labels/copies are garbage) to d = 2 gives, on the S terminal output
registers, exactly rho_{t hh}^{(x) S}, the same state as thm:main's proof. Measuring after
QFT_p^{(x) m} gives i.i.d. uniform elements of hh^perp. This proves item 2.

(Item 2's strengthening: if the measured implementation writes its classical s(lambda) into
S by X gates and uses the same U_lambda, then the whole coherent circuit followed by
end-of-circuit measurement of every L register equals the measured circuit, gate for gate,
except that the L measurements are moved later past gates that are block-diagonal in L;
the joint law of labels and readouts is unchanged, for any implementation of the
transforms.)

### 3.4 Error [proved]

Apply lem:hybrid to the coherent circuit with one step per transform (as in
thm:uniform-compilation(iii)) and all other blocks as exact steps with eta_j = 0: the oracle,
the evaluations, the controlled central translations, W_d and W_d^{-1}, the dilation and
translation blocks are exact permutations that map canonical states with clean workspace to
canonical states with clean workspace (the ideal label after the exact inverse QFT is a
canonical word; W_d returns its workspace exactly to 0 on every word). The transforms are
the same ones, in the same number, as in thm:main's count: n per lifted source, 2g_d per
complete instrument and D_{d-1} per quotient address at each grade-d node, m per readout,
so at most N_instr q_max of them, each within eta = eps/(3 N_instr q_max) on canonical
inputs. The final states are within trace distance eps/3, so the readouts are within total
variation eps/3 of the exact readouts of item 2, whose nullspace fails to be hh with
probability <= eps/3 (rank item of sec:recursion). Total failure <= 2eps/3 <= eps. The
solver third stays unused. No division by branch probabilities occurs. (The finer charge
3 pi 2^{-tau} for forward transforms on |0> of lem:qft-mod may be used verbatim.)

### 3.5 Gate count [proved, with G_meas and T^IS_d as black boxes]

Per terminal sample the coherent circuit is the measured one with three changes per
grade-d node: + W_d and W_d^{-1} (2R_d gates), + Section 3.2 steps 1, 2, 4 for each of the
M_d targets (<= 2(d-2+D_{d-1}) Gamma_x gates each), and minus the measured constant
multiplications for G (dropped in the bound). There are S n_d grade-d nodes in all. This is
the first line of item 4. For the second: S n_d M_d = S prod_{d'<=d} M_{d'} <= SP = Q/c and
d - 2 + D_{d-1} <= c + n, summed over c-1 grades; and S n_d = Q/(c prod_{d'=d}^c M_{d'}).

R_d = O(T^IS_d log T^IS_d) with T^IS_d = poly(M_d, g_d, log p) and M_d = B_d(g_d) <=
C_c'(m+1)^{d ceil(log2(d+1))}; G_meas = poly_c(m, log p, w, log 1/eps) by thm:main. So
G_coh = poly_c(m, log p, w, log 1/eps). The gate set: {X, CNOT, Toffoli, SWAP} for every
exact block, and the transforms of thm:uniform-compilation(iii) over a fixed finite gate set.

### 3.6 Qubits [proved]

No qubit is reset, so every register ever allocated, other than the reused clean
workspace, is counted once. Per run: lifted-source addresses S P n b <= Q m b; oracle
outputs S P c w = Q w; labels S sum_d n_d M_d g_d b <= S P n b <= Q m b; quotient addresses
S sum_d n_d D_{d-1} b <= S (c-1)(P/2) n b <= (c-1) Q m b / 2 (n_d <= P/M_d <= P/2).
Total <= Q((c+3) m b/2 + w) + W.

## 4. How much worse than the measured version

- **Queries:** identical, Q = c(m + ceil(log_p(3/eps))) prod_d B_d(g_d).
- **Error:** identical budget and bound (2eps/3).
- **Gates:** the measured run spends sum_d S n_d T^IS_d classical steps on solving; the
  coherent run spends 2 sum_d S n_d R_d = O(sum_d S n_d T^IS_d log T^IS_d) quantum gates on
  the same work (factor O(log T) from Pippenger-Fischer, constant 4-6 from Bennett and
  uncomputing the witness). The dilation overhead 2 Gamma_x Q (n+c) = O(Q n log^2 p) is at
  most a constant multiple of G_meas, since each target's four-pass translation already
  costs at least (d-1)d(d+1)(d+2)/6 >= 4 bracket evaluations with at least D_d products
  each **[argued]**. So: total coherent work <= O(log max_d T^IS_d) x total measured work
  (quantum gates + classical steps). Whether the solver term dominates G_meas depends on
  the unknown exponent of T^IS in M; both are polynomial in M_d.
- **Qubits:** the measured run with depth-first reuse holds at most 2 + sum_d(M_d - 1) cover
  registers (thm:uniform-compilation(iv)) plus workspace, about (sum_d B_d(g_d)) n b. The
  coherent run holds O(c Q (m b + w)): a factor of order S prod_d B_d(g_d) / sum_d B_d(g_d)
  more, because the garbage (labels, consumed targets, oracle outputs) carries coset
  information, cannot be uncomputed and must not be measured. If resetting discarded qubits
  were allowed (a trace, not a measurement whose result is used), the depth-first count plus
  W would be restored; the Proposition does not use resets.
- **Workspace:** + O(max_d T^IS_d log T^IS_d) clean ancillas for W_d (or less with Bennett
  1989 pebbling).

Scale (illustration, not a claim): Schedule-1 arities are already astronomically large at
small parameters (B_4(2) ~ 3.7e16 in thm:power-sde(iii); IS columns exceed 1e8 at
kappa_d >= 5, a = 1, per the solver report), so this is a statement about polynomial
existence, not a practical circuit.

## 5. Does any step fail? Strongest correct statement

No step fails for Schedule 1. Points checked against the text:

- prop:descent's "Targets with s_i = 0 are consumed and discarded, and delta_0 is never
  applied" is reproduced exactly by the controlled translation (identity at s = 0).
- "Classical solver retries reuse the same saved label list" (sec:recursion): no retries
  under Schedule 1, so nothing to make reversible.
- "a number fixed before the run under Schedule 1, whose arities are fixed and which has no
  restarts" (N_instr): needed for a fixed circuit; holds.
- rem:is-import(d) ("Determinism is not used in Theorem thm:main"): determinism **is** used
  here (a Las Vegas solver needs coins and attempt flags). It is part of thm:is-import as
  stated, so the Proposition is conditional on exactly the same import as thm:main. If a
  reader weakens thm:is-import to Las Vegas, item 1-6 still hold with: coin registers in
  |+> (garbage), k = ceil(log2(3 N_solver/eps)) clocked attempts per call at 2T steps each,
  each compiled by Section 3.1, coherent first-success selection by flags and controlled
  swaps, and s := 0 on the all-fail branch (output on that branch is the pure uniform address
  state, weight <= eps/(3N_solver) per call, absorbed by convexity into the solver third);
  gate cost of the solver multiplies by k. **[argued]**, not part of the Proposition.
- The uniformity in item 6 needs an explicit polynomial T^IS_d; the Proposition's existence
  of a polynomial-size family does not.

Weaker statements that are therefore *not* needed: none. The strongest correct statement
is the Proposition as given; its only soft spots are the black-box T^IS_d (exponent not
extracted) and the [argued] constant-factor comparison of the dilation overhead with G_meas
(which does not affect polynomiality).

## 6. Scope beyond Schedule 1 [argued, not claimed]

The proof of Section 3 uses only: (a) per grade, a deterministic total solver at a fixed
arity; (b) prop:descent; (c) the fixed tree. So it applies verbatim to any per-grade choice
of deterministic total solvers at fixed arities, e.g. the linear solver at kappa_d = 1
(M_d = g_d + 1; Lemma lem:coherent-linear-sde is an explicit W_d there), and Prop.
triangular-sde at p not in E_2(kappa_d) with public (g, alpha, beta) found by the circuit
generator and deterministic roots (Lemmas lem:coherent-quadratic-sde and
lem:coherent-power-sde are explicit W_d there, with sum O(a^4 b^2) Toffoli gates instead of
the black-box R_d). Rem:combined-schedule's Schedule-2 grades (randomized draws) and
Schedule 3 (rejection with tree restarts consuming fresh sources, expected count
unbounded per run) need the fixed-attempt construction of Section 5 and change the counts.
Not part of the Proposition.

## 7. What remains not implemented (code)

1. No reversible compilation of `theorems/rees_is_sde_solver.py` (a classical Python
   solver) exists: no clocked machine, no Boolean circuit, no Toffoli list, and no explicit
   T^IS_d. At kappa_d >= 4 with t >= 3, and kappa_d >= 5, even the classical solver is not
   executable at its arity (>= 4.3e9 columns), so such a circuit could not be emitted or
   checked in practice.
2. No generator wires a coherent receiver for general (G,H). The coherent backends
   (`rees_circuit_coherent.py`, `rees_circuit_coherent_k3.py`, `rees_circuit_coherent_c4.py`,
   `rees_circuit_full.py`) implement the same architecture (labels kept, witness computed and
   uncomputed, G_j = -s^{deg j} q_j, garbage untouched) on four fixed instances with the
   witness circuits of the three coherent lemmas, at arities that are not those of thm:main.
   They are finite evidence for Sections 3.2-3.3, not for Section 3.1.
3. No simulation of any circuit of this Proposition. No Lean.
4. Claim gates in `research/reductions/rees_hsp_reduction.json`:
   `coherent_receiver_implemented = false` and `general_sde_implemented = false` stay false.
   This report proves existence, not an implementation.

## 8. Proposed LaTeX (AI-checked, pending human review)

Placement: at the end of the subsection "Reversible BCH Evaluation", right after the
paragraph that follows Lemma lem:coherent-power-sde (before
`\subsection{Reproducible Resource Profiles}`). It uses only existing macros and labels plus
the new label `prop:coherent-receiver` and the new bib keys of Section 8.4.

### 8.1 Proposition and proof

```latex
\begin{proposition}[Coherent receiver at the arities of Theorem~\ref{thm:main}; conditional exactly as Theorem~\ref{thm:main}; AI-checked, pending human review]
\label{prop:coherent-receiver}
Fix $c \ge 1$ and assume Theorem~\ref{thm:is-import}. Put $b = \lceil\log_2 p\rceil$, $M_d = B_d(g_d)$, $n_d = \prod_{2\le d'<d}M_{d'}$, $P$, $S$ and $Q = cSP$ as in Section~\ref{sec:recursion}, $D_k = \sum_{j\le k}g_j$, and $\Gamma_\times = 158b^2+46b$, the number of gates of one modular multiply-accumulate of the second arithmetic backend. For $d = 2,\dots,c$ let $T^{\mathrm{IS}}_d$ be a bound, polynomial in $m$ and $\log p$ for fixed $c$, on the number of steps of a multitape Turing machine that maps any list of $M_d$ columns in $\Fp^{g_d}$, with $b$ bits per entry, to the witness $s(\lambda) \in \Fp^{M_d}$ of Schedule~1: the algorithm of Theorem~\ref{thm:is-import} at the exponent $\kappa_d$ followed by the Bezout step of Remark~\ref{rem:is-import}(b). For every input of Theorem~\ref{thm:main} there is a quantum circuit $\mathcal{C}$ with the following properties.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item $\mathcal{C}$ makes the $Q$ oracle calls of Theorem~\ref{thm:main} (or uses its $Q$ copies of $\rho_H$), applies otherwise only gates of a fixed finite universal gate set to qubits initialised to $|0\rangle$, and measures only at the end: $S$ registers of $m$ coordinates, each in the computational basis after $\mathrm{QFT}_{\Fp}$ on every coordinate. No other qubit is measured or reset. Its output is the nullspace of the $S$ samples.
  \item With exact transforms, the $S$ samples are independent and uniform on $\hh^\perp$, exactly as in the algorithm of Theorem~\ref{thm:main} with exact instruments.
  \item With every transform compiled as in Theorem~\ref{thm:uniform-compilation}(iii) at $\eta = \eps/(3N_{\mathrm{instr}}q_{\max})$, the output distribution of $\mathcal{C}$ is within total variation distance $\eps/3$ of the exact one, so $\mathcal{C}$ outputs a basis of $\hh$ with probability at least $1-2\eps/3$.
  \item Let $G_{\mathrm{meas}}$ be the number of gates, excluding the classical solver, that the proof of Theorem~\ref{thm:main} charges, and $R_d \le C_0\,T^{\mathrm{IS}}_d\log T^{\mathrm{IS}}_d + M_d b$, with $C_0$ an absolute constant. Then $\mathcal{C}$ has at most
  \[
    G_{\mathrm{meas}} + 2\sum_{d=2}^{c} S n_d R_d + 2\Gamma_\times\sum_{d=2}^{c} S n_d M_d\,(d-2+D_{d-1})
    \;\le\; G_{\mathrm{meas}} + \frac{2Q}{c}\sum_{d=2}^{c}\frac{R_d}{\prod_{d'=d}^{c}M_{d'}} + 2\Gamma_\times Q\,(n+c)
  \]
  gates, which is $\poly_c(m,\log p,w,\log(1/\eps))$, and at most $Q\bigl(\tfrac{c+3}{2}mb + w\bigr) + W$ qubits, where $W = O\bigl(\max_d T^{\mathrm{IS}}_d\log T^{\mathrm{IS}}_d\bigr)$ plus the clean workspace of one right translation and one transform.
  \item If the polynomials $T^{\mathrm{IS}}_d$ are explicit, the gate list of $\mathcal{C}$ is computed classically in time polynomial in its length.
\end{enumerate}
\end{proposition}

\begin{proof}
\emph{The solver.} Clock the machine at $T = T^{\mathrm{IS}}_d$ steps, so that it computes a function $F_d$ on all words of $M_dg_db$ bits; on canonical inputs $F_d(\lambda) = s(\lambda)$ is nonzero and solves~\eqref{eq:sde-target} for every $\lambda$, because $M_d \ge B_{\kappa_d}(g_d)$ (Remark~\ref{rem:is-import}(b)) and the solver of Theorem~\ref{thm:is-import} is deterministic and total at that arity. By the oblivious simulation of Pippenger and Fischer~\cite{PippengerFischer1979}, $F_d$ is computed by a Boolean circuit over $\{\mathrm{AND},\mathrm{NOT}\}$ of size $O(T\log T)$, constructible in time $\poly(T)$. Writing each AND by a Toffoli gate and each NOT by a CNOT and an $X$ onto fresh qubits gives a permutation circuit $V_d : |x\rangle|0\rangle \mapsto |x\rangle|\gamma(x),F_d(x)\rangle$ that uses the input wires only as controls. Bennett's compute--copy--uncompute~\cite{Bennett1973}, $W_d = V_d^{-1}\,(\text{CNOT copy of } F_d(x) \text{ into a fresh register } \mathsf{S})\,V_d$, maps $|x\rangle|0\rangle_{\mathsf S}|0\rangle \mapsto |x\rangle|F_d(x)\rangle_{\mathsf S}|0\rangle$ for every word $x$, with $R_d$ gates from $\{X,\mathrm{CNOT},\mathrm{Toffoli}\}$; it is block-diagonal in the computational basis of $x$, and its workspace returns exactly to $|0\rangle$, so it is reused.

\emph{The controlled dilation.} At a grade-$d$ node the quotient address $q$ has $D_{d-1}$ coordinates and zero top grade. For each target $x_i$, compute $s_i^2,\dots,s_i^{d-1}$ and $G_j \leftarrow G_j - s_i^{k(j)}q_j$ for every coordinate $j$ of $q$ of grade $k(j)$, by $d-2+D_{d-1}$ multiply-accumulates, so that $G = -\delta_{s_i}(\sigma(q))$ by Theorem~\ref{thm:rees-cover}(ii); apply the clean right translation $x_i \mapsto x_i \ast G$ with the four passes of Theorem~\ref{thm:uniform-compilation}(ii); and uncompute $G$ and the powers. Every block is an exact permutation of canonical basis states with clean workspace. At $s_i = 0$ we get $G = 0$ and the identity, which is the rule of Section~\ref{sec:sde} that targets with $s_i = 0$ are consumed and $\delta_0$ is never applied.

\emph{One merge.} The node keeps the ancillas of its $M_d$ complete central instruments as label registers $\mathsf{L}$ instead of measuring them, applies $W_d$ to $\mathsf{L}$, the controlled dilations and translations for $s = F_d(\lambda)$, and $W_d^{-1}$; the labels and the consumed targets are never touched again. Write $J$ for the ideal instrument isometry $|\psi\rangle \mapsto \sum_\lambda |\lambda\rangle_{\mathsf L}\otimes\Pi_\lambda|\psi\rangle$ of Section~\ref{sec:instrument} on all targets and $U_\lambda$ for the composite unitary for the label tuple $\lambda$. Since the node acts as $\sum_\lambda |\lambda\rangle\langle\lambda|_{\mathsf L}\otimes U_\lambda$ after $J$, tracing out $\mathsf{L}$ removes every block $|\lambda\rangle\langle\lambda'|$ with $\lambda \ne \lambda'$, and the output on the address register, after the targets are traced out, is
\[
  \sum_\lambda \tr_{\mathrm{targets}}\Bigl[U_\lambda\bigl(\Pi_\lambda\omega\Pi_\lambda \otimes |u_Q\rangle\langle u_Q|\bigr)U_\lambda^\dagger\Bigr]
\]
for every input $\omega$ (with any reference system), where $|u_Q\rangle$ is the uniform address state. Term by term this is the measured node of Proposition~\ref{prop:descent} on the outcome $\lambda$ with the witness $s(\lambda)$, weighted by its probability; for independent copies of $\rho_{H_d}$ every term is that probability times $\rho_{H_{d-1}}$, by Lemma~\ref{lem:central} and Proposition~\ref{prop:descent}, so the output is $\rho_{H_{d-1}}$. This is the principle of deferred measurement.

\emph{Composition.} Each node acts only on the output registers of its children and on fresh registers, never on a child's garbage, and the leaves are prepared on disjoint registers as in Lemma~\ref{lem:homogeneous} or Lemma~\ref{lem:copy-lift}. The global state is therefore a tensor product over disjoint subtrees, and the reduced state on the outputs of one level is the tensor product of the reduced outputs of its nodes. Induction from $d = c$ to $d = 2$, as in the proof of Theorem~\ref{thm:main}, gives exactly $\rho_{t\hh}^{\otimes S}$ on the $S$ terminal registers, and Fourier sampling gives~(ii).

\emph{Error.} Apply Lemma~\ref{lem:hybrid} with one step per transform and every other block as an exact step with $\eta_j = 0$: the oracle, the evaluations, the controlled central translations, $W_d^{\pm1}$ and the dilation and translation blocks map canonical states with clean workspace to such states. The transforms are those counted in Theorem~\ref{thm:uniform-compilation}(iii), at most $N_{\mathrm{instr}}q_{\max}$ of them, each within $\eta$ on canonical inputs, so the final state is within trace distance $\eps/3$ of the exact one. With the rank item of Section~\ref{sec:recursion} this gives~(iii); the solver share stays unused.

\emph{Cost.} Against the measured implementation, each of the $Sn_d$ grade-$d$ nodes adds $W_d$ and $W_d^{-1}$, and each of its $M_d$ targets adds at most $2(d-2+D_{d-1})$ multiply-accumulates. The second bound in~(iv) uses $Sn_dM_d \le SP = Q/c$, $d-2+D_{d-1} \le n+c$ and $Sn_d = Q/(c\prod_{d'\ge d}M_{d'})$. Polynomiality follows from $T^{\mathrm{IS}}_d = \poly(M_d,\log p)$, $M_d \le C_c'(m+1)^{d\lceil\log_2(d+1)\rceil}$ and Theorem~\ref{thm:main}. No qubit is reset, so every register except the reused workspace is counted once: lifted-source addresses $SPnb \le Qmb$, oracle outputs $SPcw = Qw$, labels $S\sum_dn_dM_dg_db \le SPnb \le Qmb$, and quotient addresses $S\sum_dn_dD_{d-1}b \le \tfrac{c-1}{2}Qmb$, since $n_d \le P/M_d \le P/2$. Uniformity follows because every block is generated from public data and the Pippenger--Fischer circuit is constructible.
\end{proof}

Proposition~\ref{prop:coherent-receiver} is an existence statement. It costs the same queries as Theorem~\ref{thm:main} and the same error budget, while the classical solver work enters the circuit with an extra factor $O(\log T^{\mathrm{IS}}_d)$. The qubit count grows from the depth-first count of Theorem~\ref{thm:uniform-compilation}(iv) to $O(cQ(mb+w))$, because the label registers, the consumed targets and the oracle outputs carry coset information and are neither uncomputed nor measured. It uses the determinism of Theorem~\ref{thm:is-import}, which Theorem~\ref{thm:main} does not need (Remark~\ref{rem:is-import}(d)). The same proof applies to any per-grade choice of deterministic solvers that are total at fixed arities, for example those of Lemmas~\ref{lem:coherent-linear-sde}--\ref{lem:coherent-power-sde}, which are explicit circuits $W_d$ at their arities. Schedules with random draws or restarts need a fixed number of attempts with flags and are not covered. No code generates these circuits: the Schedule~1 solver of Section~\ref{sec:sde} is a classical program, and no reversible compilation of it, and no explicit polynomial $T^{\mathrm{IS}}_d$, exists.
```

### 8.2 Minimal edit to the "Scope" paragraph

Replace its last sentence

```latex
None of these circuits is a coherent receiver for general $(G,H)$, and they test no asymptotic cost.
```

by

```latex
None of these circuits is a coherent receiver for general $(G,H)$, and they test no asymptotic cost. Proposition~\ref{prop:coherent-receiver} below shows that such a receiver exists, with the query count, arities and error of Theorem~\ref{thm:main} and an explicit polynomial gate count. That is a statement of existence: no circuit generator for it has been implemented.
```

### 8.3 Consequential edits (the two places that list what is missing)

The "Scope" paragraph itself lists nothing as missing; the list is in the paragraphs after
lem:coherent-linear-sde and lem:coherent-power-sde. Without these edits they would
contradict the Proposition.

(a) After lem:coherent-linear-sde, replace

```latex
The dilation $\delta_s$ is then controlled on a quantum register, so each grade-$k$ coordinate is multiplied by $s^k$ coherently; this cost is not counted here.
```

by

```latex
The dilation $\delta_s$ is then controlled on a quantum register, so each grade-$k$ coordinate is multiplied by $s^k$ coherently; this cost is counted in Proposition~\ref{prop:coherent-receiver}.
```

and replace

```latex
the solves at $p\in E_2(\kappa_d)$ remain classical, and only the two instances of the fourth backend, the one of the fifth and the class-four instance over $\mathbb{F}_7$ above are wired, so the receiver is coherent there, not in general.
```

by

```latex
these lemmas do not cover the solves at $p\in E_2(\kappa_d)$, which Proposition~\ref{prop:coherent-receiver} makes coherent by a reversible simulation of Schedule~1; only the two instances of the fourth backend, the one of the fifth and the class-four instance over $\mathbb{F}_7$ above are wired.
```

(b) After lem:coherent-power-sde, replace the sentence beginning
"We do not claim a general coherent receiver:" through
"... not at the arities of Theorem~\ref{thm:main} or Remark~\ref{rem:combined-schedule}." by

```latex
These lemmas alone do not give a general coherent receiver: grades with $p\in E_2(\kappa_d)$, among them every grade with $\kappa_d=p-1$ and $p\ge5$, are outside them, and their circuits run at the arity of Proposition~\ref{prop:triangular-sde}, not at the arities of Theorem~\ref{thm:main} or Remark~\ref{rem:combined-schedule}. Proposition~\ref{prop:coherent-receiver} below supplies a general receiver at the arities of Theorem~\ref{thm:main}, including the coherently controlled dilation and the composition over all grades, with its error and gate analysis. It does so by a reversible simulation of the Schedule~1 solver, and it is an existence statement; the only coherent witness circuits that have been generated are those of these lemmas.
```

Optional: in "Organization", after "coherent witness circuits for the diagonal equation
(Lemmas~\ref{lem:coherent-linear-sde}--\ref{lem:coherent-power-sde})", add ", a general
coherent receiver (Proposition~\ref{prop:coherent-receiver})"; and in tab:notation-sde add
the row `$T^{\mathrm{IS}}_d$ & running-time bound of the Schedule-1 solver at grade $d$ &
Prop.~\ref{prop:coherent-receiver}`.

### 8.4 New bib entries

`Bennett1973` exists. `PippengerFischer1979` is new and required. The next two are optional:
`Bennett1989` for a workspace remark, and `NielsenChuang2000` if a citation for deferred
measurement is wanted. The proof above writes deferred measurement out and does not need
it. These entries were written from memory without network access. Check the DOIs and pages
against the publishers before use.

```bibtex
@article{PippengerFischer1979,
  author  = {Pippenger, Nicholas and Fischer, Michael J.},
  title   = {Relations Among Complexity Measures},
  journal = {Journal of the ACM},
  volume  = {26},
  number  = {2},
  pages   = {361--381},
  year    = {1979},
  note    = {doi:10.1145/322123.322138}
}

@article{Bennett1989,
  author  = {Bennett, Charles H.},
  title   = {Time/Space Trade-Offs for Reversible Computation},
  journal = {SIAM Journal on Computing},
  volume  = {18},
  number  = {4},
  pages   = {766--776},
  year    = {1989},
  note    = {doi:10.1137/0218053}
}

@book{NielsenChuang2000,
  author    = {Nielsen, Michael A. and Chuang, Isaac L.},
  title     = {Quantum Computation and Quantum Information},
  publisher = {Cambridge University Press},
  address   = {Cambridge},
  year      = {2000}
}
```

## 9. Claim gates and next step

- Gates that must stay false: `coherent_receiver_implemented`, `general_sde_implemented`
  (and every other gate in `research/reductions/rees_hsp_reduction.json`). The Proposition is
  an existence theorem conditional on thm:is-import, AI-checked only.
- Next hard question: extract an explicit polynomial T^IS_d from IS Sections 3.1-3.3 (field
  operations, restarts <= log2 p, kernel sizes kappa^{kappa-1} a) and so make item (v)
  unconditional on an unstated exponent. Next command: an unanchored check of this report
  against the main.tex sections listed at the top. Expected artifact:
  `research/audits/reviews/2026-11-04-rees-coherent-receiver-check.md`. Acceptance test:
  no Error in Sections 3.1-3.4.
- Compile check done in this session: Sections 8.1-8.3 inserted into a scratch copy of the
  paper directory (scratchpad, not the repo), with `PippengerFischer1979` appended to its
  bib. `latexmk -pdf` exits 0, with no undefined references or citations.
- Handoff, STATE.md and MECHANICAL_FOLLOW_UP_PLAN.md were not edited by this session.
  The parent session owns them.

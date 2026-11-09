# Rees HSP coherent receiver: general coset-symmetry lemmas, and the per-label-tuple law by deferred measurement

5 November 2026. AI-only session (Claude Code, Fable 5.1). Not human review, not Lean. **AI-checked, pending
human review.** Follows `2026-11-05-rees-receiver-round3.md` (Section 2: Lemmas A and B for n4(F_5)) and its check
`2026-11-05-rees-receiver-round3-check.md`. No file other than this report was written; no .tex, code, registry,
claim gate, `AGENT_HANDOFF.md` or `STATE.md` was touched; nothing committed; no network.

Labels: **[proved]** = written proof here, not machine-checked; **[finite computation]** = exact computation on a
stated finite set, cited from the report named; **[sampled]** = exact on a stated subset only; **[argued]** =
reasoning in a cited report, neither proved there nor exhaustively checked.

The claim gate `coherent_receiver_implemented` stays false: nothing here is an implemented general circuit. The
theorems below are about any program of a stated shape; the shape is realised by the generators only for the
instances listed in Section 7.

## 0. Answers

1. **General lemmas.** Lemmas A and B of round 3 are two instances of one statement, Lemma 1 (left-translation
   invariance of the output law for a group register), which holds for every class c, every grade d, every
   subgroup H and every finite group: it uses nothing about the group but that left translation commutes with
   right translation by values held on other wires. Corollary A_c (condition any top source on one left coset)
   and Corollary B_d (replace the register of any grade-d node, 2 <= d <= c-1, by one left coset state once its
   reduced state is rho_(H_d)) follow for every class. **[proved]**, Section 2.
2. **Coherent law = measured law for every label tuple.** Theorem 2: if after its inverse transform every label
   register is used only as a control (D1), and every merge block acts on every canonical input as the
   witness-controlled right translation with clean workspace (D2), then the joint law of (all labels, readout)
   of the coherent circuit equals that of the measured receiver with the same gate lists, the same arities and
   the circuit's witness rule. This is the deferred-measurement principle of the paper's
   `prop:coherent-receiver` written at the level of the assembled gate list, with the hypotheses read off the
   program. **[proved]**, Section 3. Corollary 3: with the paper's `lem:central` and `prop:descent`, the readout
   law conditioned on **every** label tuple of positive probability is uniform on h^perp, so the output law of the
   whole circuit is uniform on h^perp. **[proved, conditional on the paper's two results]**.
3. **The sampled hypothesis.** For the seven n4(F_5) subgroups with K_2^perp != 0 the round-3 simulation verified,
   on 13 grade-2 label tuples each, checkpoint K4 at the root (the grade-2 block acts as the right translation by
   -delta_s(sigma(q)) with a valid witness s = s(lambda) for that lambda), K5 (rho_(H_1)) and the uniform
   conditional law. Of these, only K4 is a hypothesis: it is (D2) at that tuple. K5 and the uniform law are
   consequences (Corollary 3). (D2) for **all** label tuples follows from Proposition 4 (Section 4), which composes
   three label-complete facts: the witness circuit alone writes the canonical witness on every canonical label
   tuple (D2a: exhaustive on all 5^12 grade-2 tuples in `2026-11-04-rees-coherent-sde-k2.md`, and on all 25
   grade-3 tuples, rerun here), the controlled merge of one child is the right translation on all (s, q, x) (D2b:
   symbolic replay `prove_controlled_merge`, rerun here; the other children's programs are the first child's under
   a renaming of registers, checked here), and the block is U, merges, U^-1 with U never writing labels, children
   or Q (D2c: `block_structure`, and the item-level structure checked here). So the dependence on the label tuple
   is structural: labels enter every gate after their transform only as controls, and the only label-dependent
   object, the witness s(lambda), enters the merge as the control value of translations. The solver's internal
   form (linear or not) is irrelevant. **The caveat "conditional on 13 sampled label tuples" is removed as a
   theorem for n4(F_5), not as a simulation**: the exact simulation still covers 13 tuples per subgroup, and the
   other 5^6 - 13 or 25^6 - 13 are covered by Theorem 2, Corollary 3 and Proposition 4.
4. **What does not follow.** For n4(F_7) (fifth backend) and the class-four instance over F_7, (D2a) at grade 2 is
   sampled (7^12 label tuples; the kappa = 2 report's correctness beyond the checked sets is [argued]), so there
   the per-tuple statement stays conditional on (D2a). The arithmetic macro gate lists are checked on all basis
   inputs for p <= 13 only. No general coherent circuit generator exists (gate false). Lemma 1 needs left cosets
   and right translations: right cosets fail for nonnormal S (toy computation, Section 6; the round-3 reviewer's
   control on the instance).
5. **Sanity check** (Section 6, 2.1 s, < 0.5 GB): on the compiled n4(F_5) program all 24 label registers are
   used other than as a control exactly twice, by their preparation transform and their instrument's inverse
   transform, and never afterwards; all 36 oracle-output registers are written by their oracle call only; both
   blocks are U, (ctrl_i, bch_i, ctrl_i^-1)_i, U^-1 at item level with children 2 and 6; children i > 0 equal
   child 0 under register renaming; `block_structure`, `prove_controlled_merge` (both grades) and
   `sde_exhaustive` (grade 3, 25 inputs) pass; `lemma_hypotheses_check` and `measurement_schedule(level=2)` pass.

## 1. Setting

### 1.1 Groups and registers

p an odd prime, c < p. L~ the graded cover Lie algebra of the instance (grades 1..c; for n4(F_5) the cover
dimensions are (4, 2, 1)); for 1 <= d <= c, G_d is the group of class d on the coordinates of grades <= d with the
BCH law `GroupLaw.mul` of `rees_circuit_general` (truncated at grade d), elements written as canonical words
(one F_p digit per coordinate, each digit in {0, ..., p-1} on b = ceil(log_2 p) qubits). Z_d < G_d is the
top-grade layer (the grade-d coordinates), central in G_d. sigma = sigma_d : G_(d-1) -> G_d inserts zero top
coordinates. delta_s (s in F_p) multiplies the grade-k coordinates by s^k; it is an automorphism for s != 0, acts
on Z_d by s^d, and delta_0 maps everything to the identity. S = exp(h~) <= G_c is the lifted hidden subgroup;
H_d its image in G_d; K_d = H_d cap Z_d; K_d^perp the set of labels at grade d; rho_(H_d) is proportional to
sum_k |C_k><C_k| over the left cosets C_k of H_d in G_d, |C_k> the uniform superposition over C_k.

Translations on a register X with values in a group Gamma: L_g|x> = |g x>, R_t|x> = |x t|. (The paper's R_g is
|x> -> |x g^-1>; the merge translation below is x -> x * (-delta_s(sigma(q))), the paper's R_(delta_s(sigma(q))).)
t_i(s, q) := -delta_(s)(sigma(q)) = delta_s(sigma(q))^-1.

A **group register** is a tuple of digit registers holding an element of some G_d. The **canonical subspace** of
a set of registers is the span of the basis states in which every digit is < p.

### 1.2 The coherent terminal-sample program (shape S1-S6)

A **coherent terminal-sample program of class c** is a finite list of items on wires initialised to |0>, each
item one of: a permutation gate X, CX, CCX, SWAP; an exact QFT_p or QFT_p^dagger on one digit register; an oracle
call (reads the evaluation registers, writes the oracle-output registers); and one final computational-basis
measurement. It has the following shape, which is what `rees_circuit_coherent.TerminalSample` emits and
`rees_circuit_mono_c3.anatomy`, `lemma_hypotheses_check` and `TerminalSample.structure` read off:

- (S1) **Tree.** A rooted tree whose leaves (grade c) are the top sources and whose node of grade d (1 <= d <= c-1)
  has M_(d+1) children of grade d+1. Every node of grade d has a group register X (values in G_d; for a source,
  the address register A; for the root, Q_1) and, if d >= 2, a label register Lambda of g_d digits.
- (S2) **Source.** A leaf prepares A uniform (QFT_p on every digit), evaluates and calls the oracle c times,
  uncomputing the evaluation workspace, so that (KS) the joint state of (A, Y) is |G_c|^(-1/2) sum_x |x>_A
  |kappa(x)>_Y with the oracle outputs Y, kappa constant exactly on the left cosets x S with distinct values on
  distinct cosets, and clean workspace.
- (S3) **Instrument** of a node of grade d >= 2 on its register X: QFT_p on every digit of Lambda (from |0>), then
  the macro `add_scaled` with coefficient -1 from each digit of Lambda into the corresponding top coordinate of
  X, then QFT_p^dagger on every digit of Lambda. On canonical inputs the middle part is |x>|z> -> |x z^-1>|z>
  (z in Z_d, central, so x z^-1 = x - z in the top coordinates).
- (S4) **Merge** of a node of grade d <= c-1 with children X_1..X_M (M = M_(d+1)), labels Lambda_1..Lambda_M:
  prepare X uniform on G_d (QFT_p on every digit), then the **block** B = U; (ctrl_1; bch_1; ctrl_1^-1); ...;
  (ctrl_M; bch_M; ctrl_M^-1); U^-1 on (Lambda_i, X_i, X, the witness register S of M digits, workspace), where
  U = U_SDE reads the labels and writes S and its workspace, ctrl_i computes G = t_i(s_i, q) from S_i and X into
  the merge workspace, bch_i is the four-pass BCH right translation X_i <- X_i * G, and U^-1 is the inverse
  program of U (the reversed list, inverse macros = reversed gate lists of involutions).
- (S5) **Garbage and readout.** After the block of a node, the registers of its subtree other than X (children,
  their labels, oracle outputs, everything below) are never touched again. Only the root register Q_1 is
  measured, after QFT_p on every digit, as the last items.
- (S6) **Workspace.** The arithmetic ancillas, the evaluation registers, the witness register and the block
  workspace are shared; every macro and every block returns them to |0> on canonical inputs.

### 1.3 Action hypotheses

- (KS) as in (S2), for every source. [`rees_circuit_mono.source_coset_check`, on all |G_c| addresses]
- (INST) The instrument macro acts on every canonical input as the central translation |x>|z> -> |x z^-1>|z>
  with clean ancillas. [`add_scaled` on all basis inputs for p <= 13, report `2026-11-04-rees-circuit-arith.md`;
  centrality of Z_d from the grading]
- (D1) **Labels as controls.** After its instrument's QFT_p^dagger, a label register is used by no later item
  other than as a control of X/CX/CCX gates (it is a target of nothing, in no SWAP, no transform, no oracle call).
  Likewise the oracle outputs are written only by their oracle call and used by nothing else.
  [`rees_circuit_mono.measurement_schedule(level=2)` check; the script of Section 6]
- (D2) **Block action.** For every canonical (lambda, x_1..x_M, q), with S and the workspace |0>,
  B |lambda>|x_1..x_M>|q>|0>|0> = |lambda>|x_1 t_1(s_1, q), ..., x_M t_M(s_M, q)>|q>|0>|0>, where s = s(lambda)
  is a **valid witness**: s != 0 and sum_i s_i^(d+1) lambda_i = 0 (the block merges children of grade d+1, and
  delta_s acts on Z_(d+1) by s^(d+1)). It decomposes into
  - (D2a) U |lambda>|0>_S|0>_ws = |lambda>|s(lambda)>_S|0>_ws for every canonical lambda, with s(lambda) valid;
    U touches only the labels, S and its workspace;
  - (D2b) for every child i and every canonical (s_i, q, x_i): ctrl_i; bch_i; ctrl_i^-1 maps
    |x_i>|s_i>|q>|0>_work -> |x_i t_i(s_i, q)>|s_i>|q>|0>_work, reads only X_i, S_i, X and the merge workspace,
    writes only X_i and the merge workspace;
  - (D2c) the block is U, then the M child segments in order, then U^-1, the inverse program of U.
- (CLEAN) In the exact-transform run, the state before every macro and every block is supported on the
  canonical subspace with the shared workspace |0>. This follows from (KS), (INST), (D2) and (S6) by induction over
  the items, since every item maps canonical-clean basis states to canonical-clean basis states (the transforms
  are exact QFT_p on a digit register starting in a canonical state; the oracle writes fresh registers).
  [checked on the simulated states as K3 in round 3]

### 1.4 The measured receiver with the circuit's witness rule

The **measured receiver** Mea is the program with the same items, except that each label register is measured in
the computational basis right after its QFT_p^dagger, the block B is replaced by: compute s = s(lambda) classically
by the same function as U, and apply, for each child, the permutation |x_i>|q> -> |x_i t_i(s_i, q)>|q> on
(X_i, X) (implemented in any way that is exact on canonical inputs). Its arities are the coherent ones
((g_d+1)(g_d+2)/2 at kappa_d = 2, g_d+1 at kappa_d = 1), not the Chevalley-Warning arities of
`rees_circuit_general`; Proposition `prop:descent` holds for every arity and every valid witness rule, so nothing
below depends on which measured receiver is meant beyond the arity and the rule. [`heis_measured_reference(...,
witness_rule="canonical")` of `rees_circuit_coherent` is this receiver at c = 2.]

## 2. Lemma 1 and the two corollaries [proved]

**Lemma 1 (left-translation invariance).** Let X be a group register with values in a finite group Gamma, and
let W = W_m ... W_1 be a sequence of unitaries on all wires, each W_k of one of two types:

- (a) W_k acts trivially on X (its gates touch no wire of X, not even as controls);
- (b) W_k permutes basis states, maps the subspace V (canonical X, a designated set of scratch wires at |0>, the
  other wires arbitrary) into itself, and on V has the form |x>_X |r> -> |x u(r)>_X |r'(r)> with u(r) in Gamma
  and r'(r) independent of x.

Let {Pi_y} be a POVM acting trivially on X. Let omega be a density operator on all wires such that, in the run
omega_k = W_k omega_(k-1) W_k^dagger (omega_0 = omega), omega_(k-1) is supported in V whenever W_k is of type (b).
Then for every g in Gamma and every y,

  Tr(Pi_y W (L_g omega L_g^dagger) W^dagger) = Tr(Pi_y W omega W^dagger).

*Proof.* Claim: W_k ... W_1 (L_g omega L_g^dagger) W_1^dagger ... W_k^dagger = L_g omega_k L_g^dagger for all k, by
induction on k. For k = 0 it is the definition. Step: let omega'_(k-1) = L_g omega_(k-1) L_g^dagger. If W_k is of
type (a), W_k and L_g act on disjoint wires, so W_k L_g = L_g W_k as operators and W_k omega'_(k-1) W_k^dagger =
L_g omega_k L_g^dagger. If W_k is of type (b), omega_(k-1) is supported in V. L_g maps V onto V (left
multiplication of canonical words is a permutation of canonical words and does not touch the scratch wires),
so omega'_(k-1) is supported in V too. On a basis state |x, r> of V,

  W_k L_g |x, r> = W_k |g x, r> = |g x u(r), r'(r)> = L_g |x u(r), r'(r)> = L_g W_k |x, r>,

so W_k L_g = L_g W_k on V. Writing omega_(k-1) = sum c_(ab) |a><b| over basis states a, b of V,
W_k omega'_(k-1) W_k^dagger = sum c_(ab) (W_k L_g |a>)(W_k L_g |b>)^dagger = sum c_(ab) (L_g W_k |a>)
(L_g W_k |b>)^dagger = L_g omega_k L_g^dagger. This proves the claim. Finally Pi_y acts trivially on X, so
L_g^dagger Pi_y L_g = Pi_y and Tr(Pi_y L_g omega_m L_g^dagger) = Tr(L_g^dagger Pi_y L_g omega_m) =
Tr(Pi_y omega_m). QED

*Remarks.* (i) Nothing is assumed about Gamma: it need not be nilpotent, and S need not be normal. (ii) The
instrument's central translation x -> x z^-1 is of type (b) with u(r) = z^-1, r' = r (z is read from the label
register, part of r). The merge segment ctrl_i; bch_i; ctrl_i^-1 is of type (b) for X = X_i with u(r) =
t_i(s_i, q), r' = r, by (D2b); its intermediate gates read and write X_i in ways that do not commute with L_g,
which is why the lemma is stated for segments, with (CLEAN) supplying the support hypothesis at segment
boundaries. (iii) The lemma fails for right translation L_g replaced by R_g unless the segments are left
translations: a right translation x -> x u(r) does not commute with x -> x g. Section 6 has the smallest
example.

**Corollary A_c (conditioning a top source on one left coset; every class c, every H).** Fix a top source with
address A and oracle outputs Y, and the time tau right after its last oracle call and the uncomputation of its
evaluation workspace. Assume (KS) at tau, and that every later item either does not touch A or belongs to one of
the type-(b) segments for X = A: the instrument macro of this source (INST) and the segment ctrl_i; bch_i;
ctrl_i^-1 of this child in its parent's block (D2b); that Y is touched by no later item; that the readout acts on
wires other than A and Y; and (CLEAN). Then for every readout value y and every address x_0,

  P(y) = P(y | Y = kappa(x_0)),

so the oracle outputs of every top source may be conditioned on the key of any one left coset of S (one source
after another) without changing the output law.

*Proof.* Let the left cosets be C_k = g_k S, |C_k> = |G_c|^(-1/2) sum_(x in C_k) |x> = L_(g_k)|C_0> (S is a
subgroup, so g_k S = g_k g_0^-1 C_0 with C_0 = g_0 S; take g_0 = e). By (KS), the state at tau is
sum_k |C_k>_A |kappa_k>_Y (x) |Phi> with orthonormal |kappa_k>. Let W be the remaining program. Since W does not
touch Y and the readout acts trivially on Y, W = W' (x) I_Y and Pi_y = Pi'_y (x) I_Y, so the Y-branches do not
interfere: P(y) = sum_k || Pi_y W (|C_k> (x) |Phi>) ||^2. Lemma 1 with omega = |C_0><C_0| (x) |Phi><Phi| and g =
g_k gives || Pi_y W L_(g_k)(|C_0> (x) |Phi>) ||^2 = || Pi_y W (|C_0> (x) |Phi>) ||^2 (the support hypothesis holds
by (CLEAN): the states reached from any one coset branch are canonical with clean workspace at every segment
boundary, and L_(g_k) preserves this). Hence P(y) = #cosets * || Pi_y W(|C_0> (x) |Phi>) ||^2, while
P(Y = kappa_k) = || |C_k> ||^2 = 1/#cosets, so P(y | Y = kappa_k) = P(y) for every k. Conditioning several sources
in turn is legitimate: the projector onto Y = kappa_k acts on a register that no later item touches, so it may be
placed at the end, where it acts on wires other than the next source's A and Y and is a part of the readout for
the next application. QED

**Corollary B_d (replacing the register of a grade-d node by one left coset state; 2 <= d <= c-1, every class,
every H).** Fix a node of grade d with register X (values in G_d) and the time tau right after its block (U^-1
done). Let rho be the reduced state of X at tau, the other registers of its subtree traced out. Assume
rho = kappa sum_k |C'_k><C'_k| with kappa > 0, C'_k the left cosets of H_d in G_d (the conclusion of
`prop:descent` for this node; checkpoint K5 of the simulations); that the traced registers of the subtree are
never touched again (S5); that every later item touching X belongs to a type-(b) segment for X: the node's
instrument macro (INST) or the segment ctrl_j; bch_j; ctrl_j^-1 of this node as child j in its parent's block
(D2b); that the readout and any projector onto stated label values act on wires other than X; and (CLEAN). Then
the joint law of (readout, stated labels) is unchanged when the state of the whole subtree is replaced by the
pure state |C'_k> on X, for any one k.

*Proof.* At tau the global state is omega = xi (x) eta, with xi the (pure) state of the subtree and eta that of
all other wires (disjoint subtrees processed earlier are finished, later ones are still |0>, the shared workspace
is |0> by (CLEAN)). Let W be the remaining program and T the traced registers of the subtree. W and the
projectors act trivially on T, so Tr(Pi W omega W^dagger) = Tr(Pi W (rho (x) eta) W^dagger) with rho = Tr_T xi.
Now rho (x) eta = kappa sum_k L_(g_k) (|C'_0><C'_0| (x) eta) L_(g_k)^dagger with C'_k = g_k H_d, and Lemma 1
applied to each term (the support hypothesis by (CLEAN)) gives Tr(Pi W (rho (x) eta) W^dagger) = kappa * #cosets *
Tr(Pi W (|C'_0><C'_0| (x) eta) W^dagger). Normalising both sides gives the same law for every k. The projector
onto stated values of later label registers may be included in Pi because, by (D1), those registers are used only
as controls after their transforms, so measuring them commutes with every later item (Lemma 2 below). QED

Round 3's Lemma A is Corollary A_3; its Lemma B is Corollary B_2 at c = 3. Both corollaries hold at every grade of
every class, with the same footprint hypotheses: the registers' later history consists of its own instrument
macro and its own merge segment, and nothing else touches it.

## 3. Theorem 2: coherent law = measured law for every label tuple [proved]

**Lemma 2 (deferred measurement for a control-only register).** Let Lambda be a register and let W_m ... W_1
be unitaries each of which either does not touch Lambda or is a permutation gate with Lambda among its controls
only (so W_k = sum_l |l><l|_Lambda (x) W_(k,l)). Let D(omega) = sum_l (P_l (x) I) omega (P_l (x) I) be the
computational-basis dephasing of Lambda, P_l = |l><l|. Then W_k D = D W_k for every k, hence
D W_m ... W_1 = W_m ... W_1 D, and for every POVM {Pi_y} acting trivially on Lambda the joint law of (y, l) is the
same whether Lambda is measured before W_1 or after W_m:

  Tr((Pi_y (x) P_l) W omega W^dagger) = Tr(Pi_y W (P_l omega P_l) W^dagger).

*Proof.* Both kinds of W_k commute with every P_l (x) I: a gate not touching Lambda acts on other wires; a
control-only gate is block diagonal in the Lambda basis. So W_k D = D W_k. For the last identity, Pi_y (x) P_l
commutes with W (same reason), so Tr((Pi_y (x) P_l) W omega W^dagger) = Tr(Pi_y P_l W omega W^dagger P_l) =
Tr(Pi_y W P_l omega P_l W^dagger). QED

**Theorem 2 (the coherent receiver's law equals the measured receiver's law, tuple by tuple).** Let Coh be a
coherent terminal-sample program of class c of shape (S1)-(S6) satisfying (D1) and (D2) (hence (CLEAN)), and let
Mea be the measured receiver with the same items and the witness rule s(.) of (D2a) (Section 1.4). Let lambda
run over the tuples of all labels of all grades and y over the readout values. Then for every (lambda, y),

  P_Coh(labels = lambda, readout = y) = P_Mea(labels = lambda, readout = y),

where in Coh the labels are read from their registers at the end (they are garbage, never touched after their
block, so this is a measurement that commutes with everything after their transform). In particular the readout
law of Coh conditioned on any set of label values equals that of Mea conditioned on the same values.

*Proof.* Order the label registers by the position of their QFT_p^dagger. By (D1), every item after a label
register's transform either does not touch it or has it among its controls only; Lemma 2 moves the
computational-basis measurement of that register from the end of Coh to right after its transform, without
changing the joint law of (its value, everything measured later), one register at a time. The resulting program
Coh' measures every label right after its transform, as Mea does, and then applies, on the branch where the
labels have the values lambda, the block B restricted to that branch. On canonical inputs with S and the
workspace |0>, which is the case at every block by (CLEAN), B acts on the branch lambda as the permutation
|x_1..x_M>|q> -> |x_i t_i(s_i(lambda), q)>|q> of (children, X), leaving S and the workspace |0> (D2). The block
of Mea on the branch lambda is the same permutation of (children, X), with no S and no quantum workspace. Hence
after every block the states of Coh' and Mea on all non-workspace registers, conditioned on the same label
values, coincide (the S and workspace registers of Coh' are |0>, a product factor), and so do all later items
(instruments, preparations, blocks, final transform), by induction over the tree in program order. The readout
is on Q_1 in both. QED

**Corollary 3 (uniform conditional law for every label tuple; conditional on `lem:central` and `prop:descent`
of the paper).** Under the hypotheses of Theorem 2 together with (KS) and (INST), for every label tuple lambda of
positive probability, the readout law of Coh conditioned on lambda is the uniform law on h^perp. Hence the
output law of the whole circuit is uniform on h^perp, and every conditional law on a subset of the labels
(for instance the grade-2 tuple alone) is uniform on h^perp.

*Proof.* By Theorem 2 it suffices to prove the statement for Mea. In Mea, by (KS) and the fact that the oracle
outputs are never used again, each source is the mixed state rho_S on G_c (Tr_Y of the KS state). By (INST) the
gate-level instrument is the instrument {Pi_lambda} of the paper's Section `sec:instrument` (a uniform central
ancilla, a controlled central translation and an abelian Fourier transform), so `lem:central` gives: the label is
uniform on K_d^perp, and on every positive-probability outcome the target is rho_lambda. By (D2a) the classical
witness s(lambda) is defined and valid for every canonical lambda, in particular for every positive-probability
tuple. The merge of Mea on the branch lambda applies the right action R_(delta_(s_i)(sigma(q))) of
`prop:descent` to each child (x_i -> x_i * (-delta_(s_i)(sigma(q))) is the paper's R_(delta_(s_i)(sigma(q)))),
with X prepared uniform, and traces out the children (garbage, (S5)); `prop:descent` gives the output exactly
rho_(H_d) on G_d for every positive-probability label tuple and every valid witness, provided the inputs are
independent copies. Independence is the composition remark of the paper's `prop:coherent-receiver`: nodes act
only on their children's output registers and fresh registers, never on a child's garbage, so the global state
is a tensor product over disjoint subtrees. Induction from d = c to d = 2 gives: conditioned on every
positive-probability tuple of all labels, the root register Q_1 is in the state rho_(H_1) on the abelian group
G_1, and the final QFT_p on every digit followed by the measurement is abelian Fourier sampling of rho_(H_1), whose
law is uniform on h^perp (the final step of the paper's `thm:main`). Averaging over any set of labels keeps the
law uniform. QED

*What the corollary imports from the paper.* `lem:central` (the branch law and the post-measurement state of the
instrument) and `prop:descent` (pointwise quotient conversion), both proved there for every finite group, every
H and every central elementary abelian Z with the dilations preserving H and acting on Z by s^d; the standing
hypotheses of the Rees construction (h~ homogeneous, so delta_s preserves exp(h~) and its images). Nothing about
the class c, the prime p or the subgroup H is used beyond those hypotheses.

## 4. Proposition 4: (D2) from the three label-complete facts [proved]

**Proposition 4.** Assume (D2a), (D2b), (D2c) and the footprints: U touches only the labels, S and the SDE
workspace; the segment of child i reads only X_i, S_i, X and the merge workspace and writes only X_i and the
merge workspace; the merge workspace is disjoint from the labels, S, the children and X (it may share wires with
the SDE workspace). Then (D2) holds: on every canonical input with S and workspace |0>, B acts as the
witness-controlled right translation of every child, with S and all workspace returned to |0>.

*Proof.* Start from |lambda>|x>|q>|0>_S|0>_ws. U touches only (Lambda, S, SDE workspace), and by (D2a) maps
|lambda>|0>_S|0>_ws to |lambda>|s(lambda)>_S|0>_ws, so the state becomes |lambda>|x>|q>|s(lambda)>|0>. For
i = 1..M in order: the segment of child i touches only X_i, S_i, X and the merge workspace, the latter |0> at its
start (initially by hypothesis, afterwards because the previous segment returned it to |0> by (D2b)); by (D2b) it
maps |x_i>|s_i>|q>|0>_work to |x_i t_i(s_i, q)>|s_i>|q>|0>_work and leaves every other register unchanged. After
the M segments the state is |lambda>|x_1 t_1, ..., x_M t_M>|q>|s(lambda)>|0>. The registers U acts on, (Lambda,
S, SDE workspace), are now in exactly the state U|lambda>|0>|0>: the labels and S were written by no segment, and
the SDE workspace wires, whether or not they were used as merge workspace, are |0>. U^-1 is the inverse program of
U (D2c): the macros' flattened gate lists consist of X, CX, CCX and SWAP, each its own inverse, so the reversed
list of a macro is its inverse unitary and the reversed list of U with inverted macros is U^dagger. Hence U^-1
returns (Lambda, S, SDE workspace) to |lambda>|0>|0>, and the final state is |lambda>|x_i t_i(s_i, q)>_i |q>|0>|0>
with s = s(lambda) valid by (D2a). QED

*Where the three facts are label-complete for n4(F_5).* (D2a) at grade 2: `exhaustive_check(5, 2, 2)` of
`rees_coherent_sde_k2` on all 5^12 = 244 140 625 canonical label tuples (`exhaustive_p5_a2.json`: output equals
the canonical witness, inputs restored, workspace clean, witness nonzero, equation holds, 1781 s); the
block's U is `remap(CoherentSDEK2(5, 2, 2).prog)` under a wire bijection (`MergeBlock.__init__`, `sde_circuit`),
and a wire bijection preserves the action. (D2a) at grade 3: `sde_exhaustive(blocks[3])` on all 25 tuples
(rerun here). (D2b): `prove_controlled_merge` for child 0 at both grades (symbolic replay over F_5[s, q, x] against
`sym_bch_reference`: a polynomial identity over F_p implies the pointwise identity on all canonical values; the
macros are taken as their declared maps, which the `rees_circuit_arith` report checks on all basis inputs for
p <= 13), and children i > 0 equal child 0 under the renaming S_0 -> S_i, x_0 -> x_i (checked here at item level,
Section 6). (D2c) and the footprints: `block_structure` and the item-level structure check of Section 6.

**Consequence for the round-3 caveat.** For the seven n4(F_5) subgroups with K_2^perp != 0, round 3 ran the root on
13 grade-2 label tuples each and found, for each, K4 (the block acts as the translation with the reference
witness), K5 and a uniform conditional law. By Proposition 4, K4 holds for every one of the 5^6 or 25^6 tuples;
by Theorem 2 and Corollary 3, so do K5 and the uniform conditional law; so the whole-circuit law is uniform on
h^perp for all nine subgroups. The status of this statement is **proved (hand proofs: Lemma 1, Lemma 2, Theorem 2,
Corollary 3, Proposition 4) plus finite computation (KS on all addresses; D1, D2c, footprints read off the
program; D2a exhaustive on all tuples; D2b symbolic; the macro checks for p <= 13), conditional on the paper's
`lem:central` and `prop:descent`**. It is not a simulation result: the exact simulation covers 13 tuples per
subgroup (and the two subgroups with deterministic labels completely); the 13 runs are now corroboration of
Theorem 2, and Corollary 3 predicts the identical law signature they found.

## 5. Which hypothesis was sampled, and what is structural

| Checked in round 3 on 13 tuples (root, seven subgroups) | Is it a hypothesis? | Covers all tuples by |
|---|---|---|
| K2: the six grade-2 instruments equal the reference formula on the conditioned coset | consequence of (INST) + grading | (INST): `add_scaled` all basis inputs, p <= 13 |
| K3: workspace unentangled at every component boundary | consequence of (D2a), (D2b) | Proposition 4 |
| K4: every child translated by -delta_s(sigma(q)) with the reference witness; labels, Q unchanged; S, workspace 0 | **this is (D2) at that tuple** | Proposition 4 from (D2a) exhaustive 5^12, (D2b) symbolic, (D2c) structure |
| K5: reduced state of Q_1 proportional to rho_(H_1), per tuple | consequence | Corollary 3 (`prop:descent`) |
| conditional readout law uniform on h^perp | consequence | Corollary 3 |

So the only hypothesis the sampled runs verified is (D2) at the sampled tuples, and (D2) for all tuples is a
structural consequence (Proposition 4) of facts that are each complete over the labels. The structural reason
the law does not depend on the tuple beyond what `prop:descent` already says: labels enter every gate after their
transform only as controls (D1), so by Lemma 2 the coherent circuit is, branch by branch, the measured circuit;
the only label-dependent quantity, s(lambda), enters the merge as the control value of a right translation
(D2b), which is why Lemma 1 holds for every tuple. Whether the solver is linear is irrelevant: the kappa = 2
solver takes square roots and a least-non-residue; what matters is that it is a permutation on
(labels, S, workspace) that fixes the labels (D2a).

The one place where the generality in the label tuple is **not** structural but computational is (D2a): that the
gate list of U writes a valid witness on every canonical tuple. For n4(F_5) this is exhaustive at both grades.
For n4(F_7) grade 2 (7^12 tuples) and the class-four instance over F_7 at grades 3 and 2 it is sampled, and the
kappa = 2 report's Section 5 item 4 labels correctness beyond the checked sets as [argued] (Theorem 3 and Lemma 4
there are proved for all p and a; the circuit-level correctness of U given the macros is argued, not proved, and
the macros are checked for p <= 13 only). There the per-tuple statement of Corollary 3 is conditional on (D2a).

## 6. Sanity check [finite computation, 2.1 s, < 0.5 GB, nice -n 19]

Script: Appendix A (scratch file `general_lemma_check.py`, run from the repository root with
`/opt/anaconda3/bin/python -B`; it imports `theorems.rees_circuit_mono_c3`, `theorems.rees_circuit_mono` and
`theorems.rees_circuit_coherent` read-only and writes nothing). Output, verbatim pass flags:

```
setup_seconds 1.5; steps 3181; anatomy_ok true
D1_labels_noncontrol_only_prep_qft_and_instrument_qft_dg: registers 24, all_ok true
A2_oracle_outputs_written_only_by_oracle: registers 36, all_ok true
measurement_schedule_level2_check true; lemma_hypotheses_check_ok true
D2c_block_structure_item_level: grade 2: blocks 1, all_ok true, children_per_block [6]
                                grade 3: blocks 6, all_ok true, children_per_block [2]
cfg_dims [4, 2, 1]
blocks[2]: witness_circuit CoherentSDEK2, (p, g, d, M) = (5, 2, 2, 6),
           block_structure {sde_never_writes_labels_or_Q_or_children true, child_merges_local_footprint true,
           merge_workspace_wires_outside_sde_workspace 0}, prove_controlled_merge_proved true,
           children_equal_child0_under_register_renaming true
blocks[3]: witness_circuit CoherentSDE, (p, g, d, M) = (5, 1, 3, 2),
           block_structure {... true, true, 27}, prove_controlled_merge_proved true,
           sde_exhaustive {inputs 25, gates 36472, witness_equals_canonical true, witness_nonzero true,
           equation_holds true, labels_restored true, workspace_clean true},
           children_equal_child0_under_register_renaming true
toy_S3: left_cosets_equal_reduced_Q true, right_cosets_equal_reduced_Q false (3 left, 3 right cosets)
seconds 2.1
```

What each line certifies:

- **(D1)** on the compiled program (`compile_program`, whose step field `nc` is the set of wires used other than as
  a control): each of the 24 label registers (12 of grade 3, 12 of grade 2) has exactly two steps using it other
  than as a control, its preparation `qft` and its instrument's `qft_dg`, both in component `instrument_qft`, on
  exactly its wires; no later step uses it other than as a control. Each of the 36 oracle-output registers is
  written by exactly one step, its oracle call. `measurement_schedule(level=2)`'s own check agrees.
- **(D2c)** at item level: in `ts.items`, each block's `sde_grade{d}` items are a prefix and a suffix of equal
  length, the suffix equal to the reversed prefix with every macro's `inv` flag toggled (`Prog.inverse`); between
  them, per child, a `witness_control` run, a `bch_merge` run and a `witness_control` run whose first part is the
  inverse of the child's first run (the inverse of ctrl_i and ctrl_(i+1) share one component run, split by the
  length of ctrl_0); 6 children at grade 2, 2 at grade 3.
- **(D2b) for children i > 0**: ctrl_i; bch_i; ctrl_i^-1 equals child 0's program under the wire map S_0 -> S_i,
  x_0 -> x_i (identity elsewhere), item by item, at both grades. This closes the "read off the code" bullet of
  round 3, Section 7, at the item level (the macro gate lists are the same `rees_circuit_arith` lists by
  `flatten`).
- **(D2a)** at grade 3 (`sde_exhaustive`, 25 inputs) and the block identities (`block_structure`,
  `prove_controlled_merge`) rerun; grade 2 (5^12) is cited, not rerun.
- **Lemma 1 needs left cosets.** On S_3 with S = <(12)> (not normal), a register X uniform on a coset of S and a
  register Q uniform on S_3, the circuit |x>|q> -> |x q^-1>|q> gives the same reduced state of Q for all three
  left cosets, and different reduced states for the three right cosets (rho_Q[q, q'] = [S q^-1 = S q'^-1] for a
  left coset gS, independent of g; [g^-1 S g q^-1 = g^-1 S g q'^-1] for a right coset Sg). So any readout on Q that
  separates these states has a law that depends on which right coset was chosen: conditioning on a right coset is
  not allowed, as the round-3 reviewer's control on <e2> found at gate level (`rho_Q2` changes, K5_2 fails).

## 7. What remains (the gate stays false)

1. **No general circuit.** Lemma 1, Theorem 2, Corollary 3 and Proposition 4 are statements about every program
   of shape (S1)-(S6) with (KS), (INST), (D1), (D2). Programs of that shape exist only for the generated
   instances: Heis(F_3) (c = 2), n4(F_5) (c = 3, kappa <= 2), n4(F_7) (c = 3, kappa_3 = 3, fifth backend) and the
   class-four instance over F_7. No generator for general (G, H) or general c exists;
   `coherent_receiver_implemented` is and stays false. The paper's `prop:coherent-receiver` is the existence
   statement for general c, conditional on `thm:is-import`.
2. **Instance coverage of the hypotheses.**

   | instance | (D1), (D2c), footprints | (D2a) | (D2b) | result |
   |---|---|---|---|---|
   | Heis(F_3) | read off the program (round 2) | all 27 tuples; whole block on all 3^18 inputs | symbolic | exact law computed directly anyway |
   | n4(F_5) | this report, Section 6 | grade 3: all 25; grade 2: all 5^12 | symbolic + renaming | **per-tuple caveat removed as a theorem**; simulated on 13 tuples x 7 subgroups and completely on 2 |
   | n4(F_7) | `f7_relabeling.json` (round 3) | grade 3: all 7^3 label triples (kappa = 3 report); grade 2: sampled (7^12) | symbolic (`merge_proofs_f7.json`) | conditional on (D2a) at grade 2 |
   | class 4 over F_7 | not run through `anatomy` (class 3 only) | grade 4: all triples; grades 3, 2: sampled | symbolic | conditional on (D2a) at grades 3, 2 and on the footprint checks |

   The missing exhaustive run for n4(F_7) grade 2 is U alone on 7^12 ~ 1.4 x 10^10 inputs; scaled from the
   5^12 run (1781 s) it is about 28 CPU hours in the chunked mode of `rees_coherent_sde_k2`. `anatomy` and
   `lemma_hypotheses_check` are written for c = 3 and would need a class-general rewrite for the class-four
   instance.
3. **Macro correctness** (`add_scaled`, `add_product` of `rees_circuit_arith`) is proof-by-computation for
   p <= 13 only. All instances here have p <= 7, so this is not a gap for them; it is one for any larger prime.
4. **Not machine-checked.** Lemma 1, Lemma 2, Theorem 2, Corollary 3 and Proposition 4 are hand proofs by an AI
   session; so are the paper's `lem:central` and `prop:descent` (human-written, not Lean-checked, as far as this
   session knows). `prove_controlled_merge` is a symbolic computation, not a Lean proof.
5. **Explicit transforms.** Theorem 2 needs only (D1), a gate property, so the deferred-measurement equality holds
   verbatim for the circuit with the approximate transforms of `lem:qft-mod`. But Corollary 3 and Proposition 4
   need canonical label values and exact instruments: with approximate transforms the labels carry
   non-canonical components on which U is unspecified (kappa = 2 report, item 3: padding words not claimed), and
   `lem:central` is for the exact instrument. The explicit-transform circuit stays covered only by the hybrid
   bound of `2026-11-04-rees-qft-wire.md`.
6. **What the readout cannot see.** Corollary 3 proves uniformity of the law, not correctness of the circuit:
   round 3's mutants with the opposite sign of the translation also have a uniform law. Correctness is (D2),
   which is checked, not inferred from the law.
7. **The next hard question of round 3** ("is the conditional Phase-B law independent of the label tuple by a
   proved symmetry?") is answered in the affirmative by Corollary 3 without an orbit argument: the law is the
   same for every tuple because it is the measured receiver's law, which `prop:descent` makes tuple-independent.
   The proposed `--tuples orbit-reps` mode is therefore unnecessary; a cheaper acceptance test is to rerun Phase B
   on a few further random tuples and compare the law signature with the 13 (prediction: identical).

## 8. Proposed paper text (AI-checked, pending human review; not applied)

Each old sentence is quoted exactly as it stands in `docs/papers/rees-hsp/main.tex` (paragraphs "Coherent-label
backends" and "Scope" of Section `sec:uniform-compilation`; each occurs exactly once, checked at 5 November
2026). The replacements use only macros already in the file (`\hh`, `\file`, `\delta_s`, `\sigma`, `\rho_{H_1}`).

**(a) Coherent-label backends, replace**

> For the other seven subgroups the readout law conditioned on stated grade-two labels is exactly uniform on $\hh^\perp$ for each of the $13$ label tuples run, out of $5^6$ or $25^6$; their output law of the whole circuit, the average over all label tuples, is not computed.

**by**

> For the other seven subgroups the readout law conditioned on stated grade-two labels is exactly uniform on $\hh^\perp$ for each of the $13$ label tuples run, out of $5^6$ or $25^6$; their output law of the whole circuit, the average over all label tuples, is not computed by simulation. It is uniform on $\hh^\perp$ for all nine subgroups by a proof (\file{research/audits/reviews/2026-11-05-rees-receiver-general-lemma.md}; hand proofs, not machine-checked, and finite computation, AI-checked, pending human review): after its inverse transform every label register is used only as a control, which is read off the program, so by deferred measurement the joint law of the labels and the readout is that of the measured receiver at the same arities with the circuit's witness rule, and for every label tuple that law is uniform on $\hh^\perp$ by Lemma~\ref{lem:central} and Proposition~\ref{prop:descent}, provided the grade-two block acts on every label tuple as the right translation by $-\delta_s(\sigma(q))$ with a valid witness $s$; it does, because the witness circuit alone writes the canonical witness on all $5^{12}$ label tuples (the exhaustive check of Lemma~\ref{lem:coherent-quadratic-sde}), the controlled merge of each child is that translation on all $(s,q,x)$ by the symbolic replay, and the block is the witness circuit, the merges and its inverse, with the witness circuit touching no child and no $Q$. The $13$ simulated tuples corroborate this.

**(b) Coherent-label backends, replace**

> The footprint hypotheses of both lemmas are read off the program; that the instruments and merges act as these translations on every input rests on the exhaustive checks of their arithmetic blocks and on a symbolic replay of the merge of one child per block.

**by**

> The footprint hypotheses of both lemmas are read off the program; that the instruments and merges act as these translations on every input rests on the exhaustive checks of their arithmetic blocks and on a symbolic replay of the merge of one child per block, the other children's merge programs being the first child's under a renaming of registers, which is checked. Both lemmas are instances of one left-invariance statement, proved for every class, every grade and every finite group in the report \file{research/audits/reviews/2026-11-05-rees-receiver-general-lemma.md} (hand proof, AI-checked, pending human review): the output law is unchanged by a left translation of a group register whose later history consists of gates that do not touch it and of segments acting on it as right translations by values held on other wires.

**(c) Scope, replace**

> gives the exact output law over $\mathbb{F}_3$, and over $\mathbb{F}_5$, through the two symmetry lemmas above, for the two subgroups with deterministic grade-two labels and conditionally on $13$ stated grade-two label tuples for each of the other seven;

**by**

> gives the exact output law over $\mathbb{F}_3$, and over $\mathbb{F}_5$, through the two symmetry lemmas above, for the two subgroups with deterministic grade-two labels and conditionally on $13$ stated grade-two label tuples for each of the other seven, whose law on every other tuple is uniform on $\hh^\perp$ by the deferred-measurement argument of \file{research/audits/reviews/2026-11-05-rees-receiver-general-lemma.md} rather than by simulation;

No change to `core/main-core.tex` is proposed (it has no sentence about the receiver simulations, as the round-3
check recorded).

## 9. Next hard question

Make (D2a) label-complete for n4(F_7) at grade 2, or prove it. Two routes: (i) the chunked exhaustive run of
`rees_coherent_sde_k2` at (p, a, d) = (7, 2, 2) on all 7^12 inputs (about 28 CPU hours; artifact
`exhaustive_p7_a2.json`; acceptance: the five flags of `check_circuit` all true); (ii) a written proof that
`CoherentSDEK2(p, a, d)` computes `canonical_witness_k2` on every canonical input given the macros, upgrading the
kappa = 2 report's [argued] to [proved]; its acceptance test is an independent re-derivation plus the existing
exhaustive runs as controls. With either, Corollary 3 applies to the fifth backend's root for all 7^6 grade-2
tuples, where round 3 has three. A second question is the class-general rewrite of `anatomy` and
`lemma_hypotheses_check` (they are for c = 3) so that (D1) and the footprints can be read off the class-four
program over F_7; the item-level checks of Appendix A are already class-general.

## Appendix A. The sanity-check script

```python
"""Sanity check for research/audits/reviews/2026-11-05-rees-receiver-general-lemma.md.

(1) Hypothesis (D1) of Theorem 2 read off the compiled n4(F_5) coherent program:
    every label register is used other than as a control exactly twice, by its
    preparation QFT and by its instrument's inverse QFT, and never afterwards;
    every oracle-output register is written by its oracle call only.
(2) Hypothesis (D2c): in the assembled program each merge block is
    U_SDE, then per child ctrl_i, bch_i, ctrl_i^-1, then U_SDE^-1 (item level).
(3) Lemma 1 toy on S_3: for a right-translation circuit the reduced state of the
    control register is the same for every LEFT coset of a non-normal S and
    differs between RIGHT cosets.
(4) Per block: the witness circuit class, block_structure, prove_controlled_merge,
    sde_exhaustive at grade 3, and children i > 0 equal child 0 under register renaming.
"""
import itertools, json, sys, time
import numpy as np

t0 = time.time()
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
import theorems.rees_circuit_mono_c3 as R
import theorems.rees_circuit_mono as M
from theorems.rees_coherent_sde import Macro

cfg, insts, ts, steps, an = R.setup("n4_f5")
out = {"setup_seconds": round(time.time()-t0, 1), "steps": len(steps), "anatomy_ok": an["ok"]}

# ---- (1) labels and oracle outputs
regs = M._registers(ts)
label_rows, y_rows = [], []
for kind, reg in regs:
    w = set(reg)
    nc_steps = [i for i, s in enumerate(steps) if s[3] & w]
    if kind.startswith("label"):
        comps = [steps[i][2] for i in nc_steps]
        kinds = [steps[i][0] for i in nc_steps]
        ok = (len(nc_steps) == 2 and kinds == ["qft", "qft_dg"] and comps == ["instrument_qft"]*2
              and set(steps[nc_steps[0]][1]) == w and set(steps[nc_steps[1]][1]) == w)
        label_rows.append(ok)
    elif kind == "oracle_output":
        ok = len(nc_steps) == 1 and steps[nc_steps[0]][0] == "oracle"
        y_rows.append(ok)
out["D1_labels_noncontrol_only_prep_qft_and_instrument_qft_dg"] = {"registers": len(label_rows), "all_ok": all(label_rows)}
out["A2_oracle_outputs_written_only_by_oracle"] = {"registers": len(y_rows), "all_ok": all(y_rows)}
sched, ok_sched = M.measurement_schedule(ts, steps, level=2)
out["measurement_schedule_level2_check"] = bool(ok_sched)
lh = R.lemma_hypotheses_check(ts, steps, an)
out["lemma_hypotheses_check_ok"] = lh["ok"]

# ---- (2) block structure at item level
def same(a, b):
    if isinstance(a, Macro) and isinstance(b, Macro):
        return (a.kind, a.coeff, a.args, a.inv) == (b.kind, b.coeff, b.args, b.inv)
    return (not isinstance(a, Macro)) and (not isinstance(b, Macro)) and a == b

def inv(items):
    return [it.inverse() if isinstance(it, Macro) else it for it in reversed(items)]

blocks = {}
for d in (2, 3):
    comps = {f"sde_grade{d}", f"witness_control_grade{d}", f"bch_merge_grade{d}"}
    idx = [i for i, (c, _) in enumerate(ts.items) if c in comps]
    groups, g = [], [idx[0]]
    for i in idx[1:]:
        if i == g[-1]+1:
            g.append(i)
        else:
            groups.append(g); g = [i]
    groups.append(g)
    res = []
    for g in groups:
        items = [ts.items[i] for i in g]
        sde = [it for c, it in items if c == f"sde_grade{d}"]
        n = len(sde)
        ok_sde = n % 2 == 0 and all(same(a, b) for a, b in zip(sde[n//2:], inv(sde[:n//2])))
        cs = [c for c, _ in items]
        pre = len(list(itertools.takewhile(lambda c: c == f"sde_grade{d}", cs)))
        suf = len(list(itertools.takewhile(lambda c: c == f"sde_grade{d}", reversed(cs))))
        ok_pos = pre == suf == n//2
        mid = items[pre:len(items)-suf]
        # runs of equal component; ctrl_i^-1 and ctrl_{i+1} share a run, split by the length L of ctrl_0
        runs = [(c, [it for _, it in grp]) for c, grp in itertools.groupby(mid, key=lambda t: t[0])]
        ok_mid, kids = True, 0
        if not runs or runs[0][0] != f"witness_control_grade{d}":
            ok_mid = False
        else:
            L = len(runs[0][1]); cur = runs[0][1]; r = 1
            while r < len(runs):
                if runs[r][0] != f"bch_merge_grade{d}" or r+1 >= len(runs) or runs[r+1][0] != f"witness_control_grade{d}":
                    ok_mid = False; break
                wrun = runs[r+1][1]
                if len(wrun) not in (L, 2*L) or not all(same(a, b) for a, b in zip(wrun[:L], inv(cur))):
                    ok_mid = False; break
                kids += 1
                cur = wrun[L:]; r += 2
            ok_mid = ok_mid and cur == []
        res.append({"items": len(items), "sde_half": n//2, "U_then_Uinv": ok_sde, "sde_prefix_suffix": ok_pos,
                    "children_ctrl_bch_ctrlinv": ok_mid, "children": kids})
    blocks[d] = res
out["D2c_block_structure_item_level"] = {d: {"blocks": len(r), "all_ok": all(x["U_then_Uinv"] and x["sde_prefix_suffix"] and x["children_ctrl_bch_ctrlinv"] for x in r),
                                             "children_per_block": sorted({x["children"] for x in r})} for d, r in blocks.items()}

# ---- (3) Lemma 1 toy on S_3
perms = list(itertools.permutations(range(3)))
idx = {g: i for i, g in enumerate(perms)}
def mul(a, b):  # (a*b)(i) = a(b(i))
    return tuple(a[b[i]] for i in range(3))
def inv_(a):
    r = [0]*3
    for i, ai in enumerate(a): r[ai] = i
    return tuple(r)
S = [(0, 1, 2), (1, 0, 2)]           # <(12)>, not normal
def reduced_Q(coset):
    # X uniform on coset, Q uniform on S_3, |x>|q> -> |x q^-1>|q>; rho_Q[q,q'] = <C q^-1 | C q'^-1>
    n = len(perms); rho = np.zeros((n, n))
    for q in perms:
        for qq in perms:
            A = {mul(x, inv_(q)) for x in coset}; B = {mul(x, inv_(qq)) for x in coset}
            rho[idx[q], idx[qq]] = len(A & B)/len(coset)/n
    return rho
left = [sorted({mul(g, s) for s in S}) for g in perms]
right = [sorted({mul(s, g) for s in S}) for g in perms]
left = [list(t) for t in {tuple(c) for c in left}]
right = [list(t) for t in {tuple(c) for c in right}]
rl = [reduced_Q(c) for c in left]; rr = [reduced_Q(c) for c in right]
out["toy_S3"] = {"left_cosets_equal_reduced_Q": all(np.allclose(r, rl[0]) for r in rl),
                 "right_cosets_equal_reduced_Q": all(np.allclose(r, rr[0]) for r in rr),
                 "n_left": len(left), "n_right": len(right)}

# ---- (4) per-block: which witness circuit, its footprint, the symbolic merge proof, U_SDE exhaustive at grade 3
import theorems.rees_circuit_coherent as C
out["cfg_dims"] = list(map(int, cfg.dims))
out["blocks"] = {}
for d, blk in ts.blocks.items():
    row = {"witness_circuit": type(blk.sde).__name__, "p_g_d_M": [blk.p, blk.g, blk.d, blk.M],
           "block_structure": C.block_structure(blk)}
    pm = C.prove_controlled_merge(blk)
    row["prove_controlled_merge_proved"] = pm["proved"]
    if blk.p**(blk.M*blk.g) <= 10**5:
        row["sde_exhaustive"] = C.sde_exhaustive(blk)
    # children i > 0: ctrl_i + bch_i + ctrl_i^-1 equals child 0's program under S_0 -> S_i, x_0 -> x_i
    from theorems.rees_coherent_sde import Prog
    base = Prog(blk.ctrl[0]+blk.bch[0]+blk.ctrl[0].inverse())
    rel = []
    for i in range(1, blk.M):
        wmap = {w: w for w in range(blk.nw)}
        wmap.update(zip(blk.S[0], blk.S[i]))
        for j in range(blk.nx):
            wmap.update(zip(blk.x[0][j], blk.x[i][j]))
        other = Prog(blk.ctrl[i]+blk.bch[i]+blk.ctrl[i].inverse())
        rm = C.remap(base, wmap)
        rel.append(len(rm) == len(other) and all(same(a, b) for a, b in zip(rm, other)))
    row["children_equal_child0_under_register_renaming"] = all(rel)
    out["blocks"][d] = row
out["seconds"] = round(time.time()-t0, 1)
print(json.dumps(out, indent=1, default=str))
```

# Referee check: Proposition prop:coherent-receiver (Rees HSP, main.tex)

Date: 2026-11-04. AI referee session only; no human review. No `.tex` file
was edited, no commit, no network. The author's report
(`2026-11-04-rees-coherent-receiver-theorem.md`), the integration log and
`research/AGENT_HANDOFF.md` were not read before this verdict was formed.

Scope read in `docs/papers/rees-hsp/main.tex`: Theorem `thm:main` and its
proof (lines 179-200, 567-569), Section `sec:sde` (Schedule 1 and the
`s_i = 0` rule, lines 498-520, 577-597), Proposition `prop:descent`,
Lemma `lem:central`, Section `sec:instrument`, Lemma `lem:hybrid` and its
application paragraph (550-565), the error budget (540-549), Theorem
`thm:is-import` and Remark `rem:is-import`, Lemmas `lem:homogeneous` and
`lem:copy-lift`, Theorem `thm:uniform-compilation`, Lemmas
`lem:coherent-*-sde`, Proposition `prop:coherent-receiver` (807-842) and
the paragraph after it (844). Claim gates checked in
`research/reductions/rees_hsp_reduction.json`.

## Verdict

The proposition stands as a conditional existence statement, under the
same hypothesis as Theorem `thm:main` (Theorem `thm:is-import`) plus the
standard imports of Pippenger-Fischer and Bennett. I found no error in
its mathematics. The parts checked hold: the deferred-measurement
identity, the composition over the tree, the controlled dilation, the
error budget, both gate inequalities and the qubit tally.

Counts: **Error 1** (in the Scope paragraph before the proposition, not
in the proposition itself), **Gap 2** (both minor and closable in a
sentence or two), **Imprecision 9**.

Claim gates: `coherent_receiver_implemented` and `general_sde_implemented`
are both `false`. The proposition, the paragraph after it, the Scope
paragraph and the README all say that no generator exists. Nothing in the
text claims an implementation.

## Probe results (what was checked and found to hold)

1. **Adaptivity under Schedule 1.** None remains. The arities
   `M_d = B_d(g_d)` and the tree shape are fixed from public data, and
   `N_instr` is fixed before the run. The solver is deterministic and
   total for `M >= B_{kappa_d}(g_d)` (Theorem `thm:is-import` as stated:
   "given any lambda_1..lambda_M ... with M >= B_d(a)"), so it has no
   abort flag, retry or cutoff, and the solver share is zero. Every
   target is consumed, the `s_i = 0` ones included, so the count of
   consumed targets does not depend on the data. The rank item is not a
   check: the output is simply the nullspace of the samples, and a rank
   deficit only makes it wrong, which the `eps/3` rank share covers. The
   final linear algebra runs after the only measurement. Preprocessing
   (bases of `gamma_k`, eta, the Bezout exponent) is public and fixed in
   advance.
2. **Deferred measurement at one merge.** The identity is correct.
   `W_d`, the dilations and the translations use `L` only as a control,
   and `W_d^{-1}` returns `S` to `|0>`. The node is therefore
   `sum_lambda |lambda><lambda|_L (x) U_lambda` after `J`, and tracing
   `L` kills the off-diagonal blocks. Because the identity holds "for
   every input omega (with any reference system)", the children's
   garbage, which is entangled with their outputs, plays the role of the
   reference: the parent never touches it, so tracing it first commutes
   with the parent. What the parent needs is the joint reduced state of
   its `M_d` inputs. That state is `rho_{H_d}^{(x) M_d}` because disjoint
   subtrees start on disjoint `|0>` registers and act on disjoint
   registers. The `S` terminal trees are disjoint in the same way. Only
   the reduced state on the terminal registers is measured, so the
   off-diagonal `(L, output)` coherences are irrelevant. (See Gap G2 on
   reused workspace.)
3. **Reversible solver.** It is enough for `W_d` to be an exact unitary
   that is correct on canonical inputs. Lemma `lem:hybrid` needs the
   ideal steps only to be channels on the whole space that preserve
   `S_j`; leaked implemented states are handled because the implemented
   suffix is a channel. Clocking the machine at `T` steps, with the
   halting state absorbing, defines `F_d` on every word, and the
   Boolean-circuit form makes `W_d` exactly clean on every word. The
   citation of Pippenger-Fischer (JACM 26(2):361-381, 1979: multitape
   TM in time T, then an oblivious 2-tape TM in time O(T log T), then
   combinational size O(T log T)) is correct; see G1 and I8 for the
   constant and multi-output caveats. Totality: Theorem `thm:is-import`
   is stated for arbitrary columns, and `B_kappa <= B_d` because `B_d(a)`
   increases in `d`.
4. **Controlled dilation.** The coordinates of the cover are graded
   (bases of the `gamma_k`), so `delta_s` is diagonal with entries
   `s^k`. Starting from `G = 0`, the updates `G_j <- G_j - s^{k(j)} q_j`
   give `G = -delta_s(sigma(q))`, which is the group inverse of
   `delta_s(sigma(q))` in Lie coordinates. So `x * G = x
   delta_s(sigma(q))^{-1}`, which is `R_{delta_s(sigma(q))}` with
   `R_g|x> = |x g^{-1}>`. That takes `d-2` products for
   `s^2..s^{d-1}` and `D_{d-1}` multiply-accumulates. At `s = 0` all
   powers vanish, `G = 0`, and `x * 0 = x` exactly on canonical words,
   which agrees with tracing out an inactive target. Note that
   `R_{delta_0(sigma(q))} = R_1` anyway, so the rule "delta_0 is never
   applied" and the coherent identity give the same factor
   `tr(rho_lambda) = 1`. (See I2 for the squaring step.)
5. **Error.** Lemma `lem:hybrid` allows exact steps with `eta_j = 0`,
   because the ideal and implemented steps coincide and each maps
   canonical states with clean workspace to such states. The coherent
   circuit has exactly the transforms counted by
   Thm `uniform-compilation`(iii): `n` per leaf, `2 g_d` per central
   instrument, `D_{d-1}` per quotient address and `m` per readout. That
   is at most `N_instr q_max` transforms, so
   `eta = eps/(3 N_instr q_max)` gives at most `eps/3`. The rank failure
   is at most `1/((p-1)p^t) <= eps/3`. Since trace distance bounds
   total-variation distance, success is at least `1 - 2eps/3 >= 1 - eps`.
   This is correct.
6. **Counts.** The following all hold:
   - `S n_d M_d = S prod_{d'<=d} M_{d'} <= SP = Q/c`;
   - `S n_d = Q/(c prod_{d'>=d} M_{d'})`;
   - `sum_{d=2}^c S n_d M_d (d-2+D_{d-1}) <= (c-1)(Q/c)(n+c) <= Q(n+c)`;
   - `n_d <= P/M_d <= P/2`, since `B_d(g_d) >= 4` for `d >= 2`, even
     when `g_d = 0`;
   - labels: `S sum n_d M_d g_d b <= SP(n-m)b <= Qmb`;
   - quotient addresses: `S sum_d n_d D_{d-1} b <= S(c-1)(P/2)(cm)b =
     ((c-1)/2)Qmb`;
   - total `((c+3)/2)Qmb + Qw`. Every consumed target is either a leaf
     address or a child's quotient address, so none is double-counted.
7. **Claims.** Clean (see the gate values above). E1 below is an
   overstatement about how explicit the count is, not an implementation
   claim.

## Findings

### Error

**E1. Scope paragraph claims an "explicit polynomial gate count".**
Location: line 772, paragraph `Scope`.
Quote: "Proposition~\ref{prop:coherent-receiver} below shows that such a
receiver exists, with the query count, arities and error of
Theorem~\ref{thm:main} and an explicit polynomial gate count."
Why: the count in (iv) is explicit only relative to `G_meas` and
`T^IS_d`. The paragraph after the proposition says "no explicit
polynomial $T^{\mathrm{IS}}_d$ ... exists", and `G_meas` is not given as a
formula anywhere (I3). As written the sentence is false and contradicts
line 844.
Fix:
```latex
... with the query count, arities and error of Theorem~\ref{thm:main} and a
gate count that is polynomial for fixed $c$ and explicit in terms of the
measured-label gate count and the running time $T^{\mathrm{IS}}_d$ of the
Schedule~1 solver, for which no explicit polynomial is known.
```

### Gaps

**G1. The solver machine must be uniform in p for "C_0 an absolute
constant" and for polynomiality.**
Location: statement before (i), and (iv).
Quotes: "a bound ... on the number of steps of a multitape Turing machine
that maps any list of $M_d$ columns in $\Fp^{g_d}$ ... to the witness";
"$R_d \le C_0\,T^{\mathrm{IS}}_d\log T^{\mathrm{IS}}_d + M_d b$, with $C_0$
an absolute constant".
Why: the constant in Pippenger-Fischer's O(T log T) depends on the
machine: its number of tapes, its alphabet and the size of its transition
table. The statement fixes neither the machine nor what it takes as
input. If `p`, the Bezout exponent and the van de Woestijne data are
hardwired into the finite control, the machine grows with `p` and `C_0`
is not a constant. Polynomiality probably survives, since each simulated
step then costs `poly(log p)` gates, but neither "absolute" nor the
displayed bound is proved. A single machine per pair `(d, kappa_d)` that
reads `p` and its parameters from the tape, with finite control fixed
for fixed `c`, closes this.
Fix:
```latex
... let $T^{\mathrm{IS}}_d$ be a bound, polynomial in $m$ and $\log p$ for fixed
$c$, on the number of steps of a fixed multitape Turing machine $\mathcal{M}_{d}$,
whose finite control depends only on $d$ and $\kappa_d$ and which reads $p$, $g_d$,
$M_d$ and the columns from its input tape, that outputs the canonical
representatives of the witness ...
...
with $C_0$ a constant depending only on $\mathcal{M}_d$, hence only on $c$.
```

**G2. The composition step says every node acts only on fresh registers,
but the workspace is reused.**
Location: proof, paragraphs "The solver" and "Composition".
Quotes: "its workspace returns exactly to $|0\rangle$, so it is reused";
"Each node acts only on the output registers of its children and on fresh
registers ... The global state is therefore a tensor product over
disjoint subtrees".
Why: other registers are shared across all nodes too. Besides the `W_d`
workspace, the register `S`, the `G` and power registers, the
multiply-accumulate ancillas, the right-translation workspace, the
lifted-source evaluation workspace and (with compiled transforms) the
transform ancilla pool are all reused. Strictly, then, the subtrees are
not on disjoint registers, and the tensor-product claim needs one more
fact. In the exact-transform circuit, every reused register is `|0>`
before and after each block on every canonical state the ideal circuit
reaches. For `W_d` this holds on every word; for the arithmetic blocks it
holds on canonical inputs. So the global ideal state factors as (product
over subtrees) tensor `|0>` on the shared workspace. That fact is true,
but it is not stated.
Fix (append to "Composition"):
```latex
Registers that are reused (the workspace of $W_d$, the register $\mathrm{S}$,
the registers of $G$ and of the powers, the arithmetic and evaluation
ancillas) are $|0\rangle$ before and after every block on every state that
the circuit with exact transforms reaches, since each block is an exact
permutation that cleans them on canonical inputs; so the ideal global state
is the tensor product over disjoint subtrees with $|0\rangle$ on the shared
workspace.
```

### Imprecisions

**I1. "Conditional exactly as Theorem main" leaves out the imported
circuit simulation.**
Location: proposition title, and line 571 ("the steps behind
Theorem main").
Why: the proof also imports Pippenger-Fischer, which `thm:main` does not
use. Bennett is already used by `thm:uniform-compilation`(ii). The proof
also uses the determinism in Theorem `thm:is-import`, which line 844
acknowledges. Both are standard, but the title claims the conditions
match exactly.
Fix: title "...; conditional on Theorem~\ref{thm:is-import}, with the
oblivious simulation of~\cite{PippengerFischer1979} imported; AI-checked,
pending human review".

**I2. Squaring by multiply-accumulate with aliased operands; Gamma_x is a
bound, not "the number".**
Location: "The controlled dilation" ("compute $s_i^2,\dots,s_i^{d-1}$")
and the definition of `Gamma_x`.
Why: the shift-and-add multiply-accumulate `t <- t + kappa a b` of the
second backend changes its addend register temporarily (ripple-carry
MAJ/UMA, and doublings in place) while it is controlled on bits of the
other operand. For `s^2 = s*s` the two operands are the same register,
so the controls would be corrupted. A `b`-CNOT copy of `s` into a fresh
register, uncomputed afterwards, fixes this. It adds `2b` CNOTs per
target per side at `d >= 3`, so the displayed count
`2 Gamma_x (d-2+D_{d-1})` is short by `4b` per target unless
`Gamma_x` is read with slack. Line 766 also says "at most
$158b^2+46b$", whereas the proposition says "the number".
Fix: "$\Gamma_\times = 158b^2+46b$, an upper bound on the gates of one
modular multiply-accumulate ...", and "compute $s_i^2$ from a copy of
$s_i$ (b CNOTs) and $s_i^3,\dots,s_i^{d-1}$ by multiply-accumulates";
in (iv) replace $(d-2+D_{d-1})$ by $(d-2+D_{d-1}) + 2b/\Gamma_\times$,
or add $4bSP(c-1)$ CNOTs.

**I3. `G_meas` is not a defined number.**
Location: (iv), "the number of gates, excluding the classical solver,
that the proof of Theorem~\ref{thm:main} charges".
Why: the proof of `thm:main` charges no explicit gate count ("each step
runs in time polynomial in its input size"). In the measured algorithm
the quantum circuit also depends on the classical witnesses, which act
as constants in the dilation. A worst case over witnesses is needed.
Fix: "Let $G_{\mathrm{meas}}$ be the maximum, over all witness values,
of the number of quantum gates of the measured-label implementation of
Theorem~\ref{thm:main} (leaf preparations, central instruments, address
preparations, right translations by $-\delta_s(\sigma(q))$ for classical
$s$, and readouts)".

**I4. The qubit tally for coset-copy input uses `w`.**
Location: (iv), "$Q\bigl(\tfrac{c+3}{2}mb + w\bigr) + W$ qubits"; proof
"oracle outputs $SPcw = Qw$".
Why: in case (b) there are no oracle outputs. The `Q` copies of
`rho_H` occupy `Qmb` qubits, and `w` is undefined.
Fix: "... $+\,Qw$ in case~(a), or $+\,Qmb$ for the $Q$ copies in
case~(b)".

**I5. `W` leaves out several reused registers.**
Location: (iv), "$W = O(\max_d T^{\mathrm{IS}}_d\log T^{\mathrm{IS}}_d)$
plus the clean workspace of one right translation and one transform".
Why: the following are reused but not listed: the lifted-source
evaluation workspace (`m` coordinates per evaluation), the witness
register `S` (`M_d b` bits; absorbed by `O(T log T)` only if
`T >= M_d b`, which is true but unstated), the `G` register
(`D_d` coordinates), the powers (`d-2` coordinates) and the `3b+5`
arithmetic ancillas.
Fix: "plus the clean workspace of one evaluation $E_{s_i}$, one
controlled dilation ($G$, the powers and the arithmetic ancillas), one
right translation and one transform".

**I6. Paragraph after the proposition: the asymptotic qubit count and its
stated reason.**
Location: line 844.
Quote: "The qubit count grows ... to $O(cQ(mb+w))$, because the label
registers, the consumed targets and the oracle outputs carry coset
information and are neither uncomputed nor measured."
Why: (a) It drops `W`, which can dominate. `T^IS_d` is an unknown
polynomial in `M_d` and need not be below `cQ(mb+w)`. (b) The growth is
forced only by the design rule in (i) (measure only at the end, no
reset). Those garbage registers are never touched again, so measuring
and resetting each one right after its node does not change the reduced
state on the terminal registers, which is the principle of implicit
measurement. That would recover the depth-first count of
Thm `uniform-compilation`(iv) plus `W`.
Fix: "The qubit count grows to $O(cQ(mb+w)) + W$, because (i) forbids
intermediate measurement and reset: the label registers, the consumed
targets and the oracle outputs are never uncomputed. Measuring and
resetting each of them after its last use would not change the terminal
state, and it would restore the depth-first count of
Theorem~\ref{thm:uniform-compilation}(iv) plus $W$."

**I7. "The same proof applies" to Lemmas `lem:coherent-*-sde` without
their conditions.**
Location: line 844, "The same proof applies to any per-grade choice of
deterministic solvers that are total at fixed arities, for example those
of Lemmas~\ref{lem:coherent-linear-sde}--\ref{lem:coherent-power-sde}".
Why: Lemmas `lem:coherent-quadratic-sde` and `lem:coherent-power-sde`
are conditional on Prop `triangular-sde` and require
`p notin E_2(kappa_d)`. They are total only under that condition. Their
classical parameters (`m`, or `g` and `(alpha, beta)`) are found by a
search that is Las Vegas as stated ("a uniform element ..."), so either
the gate-list generator in (v) is randomized or its failure enters the
budget. At their arities `Q`, `N_instr` and `q_max` change, so (iii)
and (iv) must be re-instantiated.
Fix: "... for example those of Lemma~\ref{lem:coherent-linear-sde} and,
conditionally on Proposition~\ref{prop:triangular-sde} and at grades
with $p\notin E_2(\kappa_d)$, Lemmas~\ref{lem:coherent-quadratic-sde}
and~\ref{lem:coherent-power-sde}, whose classical parameters are found
before the circuit is generated (Las Vegas); $Q$, $N_{\mathrm{instr}}$
and $q_{\max}$ are then taken at their arities."

**I8. Item (v) and the Pippenger-Fischer step: explicit machine and
multi-bit output.**
Location: (v), and "The solver".
Why: (v) needs an explicit machine `M_d`, not only explicit polynomials.
Pippenger-Fischer is stated for acceptance (one output bit). For the
`M_d b` output bits one uses the standard fact that in the oblivious
simulation each final tape cell is a fixed wire of the circuit, and
that fact should be stated. Otherwise the size picks up a factor
`M_d b`, which is still polynomial.
Fix: (v) "If an explicit machine $\mathcal{M}_d$ with explicit time
bound $T^{\mathrm{IS}}_d$ is given, ..."; in "The solver" add "(the
oblivious simulation fixes the head schedule, so each output cell at
time $T$ is a wire of the circuit, and the $M_db$ output bits come at no
extra cost)".

**I9. Small notational slips.**
(a) "the quotient address $q$ has $D_{d-1}$ coordinates and zero top
grade": it is `sigma(q)` that has a zero top grade. Fix: "$q$ has
$D_{d-1}$ coordinates, and $\sigma(q)$ is $q$ with a zero top grade".
(b) `J` is written with `Pi_lambda`. The instrument as described (uniform
ancilla, controlled `R_z`, Fourier transform) produces `Pi_lambda` or
`Pi_{-lambda}` depending on the direction of the transform. This is
harmless, because `sum s_i^d lambda_i = 0` is invariant under
`lambda -> -lambda`, but the convention should be fixed: "with the
transform direction chosen so that outcome $\lambda$ carries
$\Pi_\lambda$". (c) `W_d` must output canonical representatives
(`< p`) for the ideal step to preserve `S_j`. This is covered by G1's
fix ("outputs the canonical representatives").

## Next check suggested

A human check of G1 (machine uniformity) and of the Pippenger-Fischer
reading. Then reconcile line 772 with line 844 (E1). None of these
changes Theorem `thm:main` or any claim gate.

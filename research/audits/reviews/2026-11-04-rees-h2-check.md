# Rees HSP: can hypothesis (H2) of prop:tb-count-gates be dropped?

4 November 2026. AI-only read of `docs/papers/rees-hsp/{appendix-torsion-blackbox,main}.tex`,
`research/audits/reviews/2026-11-04-rees-circuit-arith.md`, `2026-11-04-rees-qft-mod.md` and
`theorems/rees_circuit_arith.py`. No .tex file edited, nothing run, no commit.
**Every claim below is AI-checked, pending human review.**

## Verdict

(H2) can be dropped as a hypothesis and replaced by a citation, with one caveat about its
evidence level. Only the proof of (a) uses it, and only for field operations in the quantum
slots over the prime field F_p, p > c. Those are additions, constant multiplications and
register-times-register multiplications, which main.tex "Binary arithmetic and explicit
transforms" and the proof of lem:qft-mod construct. No quantum step needs inversion. Even if
one did, the exponents in (a)-(d) would not change.

Caveat: the 158b^2+46b count is "exact for the generated gate lists", checked by exhaustive
simulation for p <= 13 and by a closed form matched to counted lists in 108 cases. General-b
correctness of the blocks (adder, comparison, modular adder, shift-and-add multiplier) is
labelled [argued] in the arith report and in the qft-mod report, and rests on the textbook
constructions of Vedral-Barenco-Ekert and Cuccaro et al. So "discharged" means "by standard
reversible arithmetic, counts checked by computation", not "by a machine-checked theorem".

## (1) Where (H2) is invoked

Occurrences in the appendix: the statement of prop:tb-count-gates (the "Assume ... (H2)"
clause and the sentence defining (H2)), and one use, in the proof of (a) (appendix line
~1256: "$O_c(n_p^3)$ field operations, which by (H2) and $n_p\log_2 p\le\ell$ is
$O_c(\ell^3)$ gates"). Also main.tex thm:bb-envelope(iii) ("compilation hypotheses (H2) and
(H3)") and the sentence after it ("(H2)--(H3) of Proposition ...", main.tex ~986). The
"Exponents" paragraph uses (a) but not (H2) separately. (b) uses only lem:qft-mod
(transforms) and oracle multiplications. (c) uses (H3). (d) is classical bit operations
(schoolbook b_M^2 per ring operation) and never mentions (H2). The (H1) line cites
lem:qft-mod. So the only invocation is in (a), for one merge slot (and, per leaf, O(n) field
operations for E_s):

* BCH brackets: four evaluations of at most c^4 brackets, each O(n^3) field operations
  (thm:uniform-compilation(i),(ii)). A bracket is sum c_ijk x_i y_j with c_ijk classical
  structure constants. So it consists of constant multiplications (shift-and-add), additions
  (modular adder) and register-times-register products (the multiply-accumulate
  t <- t + kappa a b). Everything is in place with clean ancillas, which is what the arith
  backend's `add_scaled` / `add_product` provide. Out-of-place Bennett copies (thm (ii))
  change only constants.
* The BCH recurrence divides by integers k+1 <= c < p. These are multiplications by the
  classical constants (k+1)^{-1} mod p, computed at compile time by Euclid in poly(log p)
  classical time. Not a quantum inversion.
* sigma, delta_s, E_s: public linear maps and dilation by a classical s (labels are measured
  in the architecture of (a)). These are constant multiplications and additions.
* Group inversion in the cover is x -> -x, one modular negation, not field inversion.

## (2) Does any quantum step need modular inversion?

No, not in the architecture whose gates (a) counts.

* Diagonal-equation solvers (the only place that inverts or takes roots) are classical in
  (a)/(d): they appear only in the classical time bound Q_f (2l)^{beta_c} polylog. Inversion
  there costs classical time, poly(log p) by extended Euclid.
* Chart acquisition (lem:tb-chart; appendix ~921, ~951, ~825): inversion of units mod p^e in
  normal-form / Howell-form elimination, classical bit operations, in (d).
* Coherent-label backends (main.tex, lem:coherent-linear/quadratic/power-sde) do invert
  coherently, by Fermat u^{p-2} with ell(p-2) multiplications each, and take roots. They are
  optional backends outside (a)-(d); their gate counts (e.g. 40 g^3 b^2 + O(g b^3) Toffoli)
  already include the O(b^3) Fermat cost. Prop (a) does not use them.

## (3) If inversion were needed coherently

Fermat inversion x^{p-2} is O(b) multiplications of O(b^2) gates, so O(log^3 p) gates (out of
place with Bennett uncompute; squarings are not reversible in place, so it needs O(b^2)
extra clean qubits, not extra gates asymptotically). Then the slot would cost
O_c(n_p^3 log^3 p) = O_c((n_p log p)^3) <= O_c(l^3), because n_p log_2 p <= l. This is the
same bound (a) states, with no extra log factor. So no exponent in (a)-(d) changes, and the
final N^{E_W(c)+4+o(1)} and N^{E_W(c)+1+max(3,beta_c)+o(1)} are untouched. (With O(log^2 p)
per operation the slack is a further factor log p.)

## Moduli: is Z/p^e covered?

* Gate-level field arithmetic is only over F_p (p prime, p > c): for e_p > 1 the core calls
  of Algorithm RtF run on the F_p-Lie algebra on the socle of S_j/K_j
  (lem:tb-count-prime). So (H2) never needs Z/p^e arithmetic. The Z/p^e operations in
  chart acquisition are classical (d).
* The Z/p^e transforms in (b) use lem:qft-mod, stated for every odd N >= 3 (N = p^e
  included), with a shift-and-add modular multiplier for odd modulus N and tested at
  N = 9, 25, 27, 49. So Z/p^e is covered as a transform, for odd p.
* The arith backend `ArithBuilder` accepts any odd modulus in code (`p % 2 == 0` raises) but
  its macros are only validated for primes (p <= 13) and its docstrings say "odd prime p".
  The (H2) citation should therefore be to the multiply-accumulate over F_p, p odd prime.
* p = 2 (possible only when c = 1, since p > c): not covered by the odd-N circuits. But F_2
  operations are XOR/AND, O(1) gates, so (H2) holds trivially, and the paper already
  handles the p = 2 transform separately (standard approximate QFT over Z/2^e, noted in
  (H1)). With c = 1 there is no nontrivial BCH anyway.

## Other points for the human reviewer

* The count 134b^2+50b-4+(20b-4)hw(p)+4H, with hw(p) <= b and H <= b^2, gives
  158b^2+46b-4, matching the paper's "at most 158b^2+46b". The paper says "at most" and
  drops the -4: fine.
* The count is for `add_product` with a classical kappa; kappa-dependence is only through
  H = sum_i hw(kappa 2^i mod p) <= b^2. The paper's phrase "t <- t + kappa a b" is right.
* The gate list for the multiply-accumulate depends on p (hw(p) terms, constants), which is
  fine because p is classical. Controlled versions (slot control, s = 0) multiply by a constant.
* Without (H2) the quantifier "a field operation costs O(log^2 p) gates" should be stated for
  the three operations actually used, not for "a field operation", since inversion is not
  claimed at that cost. The replacement below does this.

## Proposed LaTeX

Appendix, prop:tb-count-gates. Replace "Assume, in addition to the results cited by
Theorem~\ref{thm:bb-envelope}, \textup{(H2)} and \textup{(H3)} below." by

```
Assume, in addition to the results cited by Theorem~\ref{thm:bb-envelope}, \textup{(H3)} below.
```

and replace the sentence "Hypothesis \textup{(H2)}: a field operation modulo $p$ costs
$O(\log^2 p)$ gates. Hypothesis \textup{(H3)}: one run of" by

```
\textup{(H2)}, that addition, multiplication by a constant and multiplication of two
registers over $\Fp$, $p$ odd, each cost $O(\log^2 p)$ gates (at most $158b^2+46b$ gates for a
multiply--accumulate $t \leftarrow t+\kappa ab$ with $b = \lceil\log_2 p\rceil$, using $3b+5$
clean ancillas and only $X$, $\mathrm{CNOT}$, $\mathrm{SWAP}$ and Toffoli gates), is not a
hypothesis: it is discharged by the ripple-carry adder of~\cite{CuccaroDraperKutinMoulton2004}
and the modular adder, comparison and shift-and-add multiplier
of~\cite{VedralBarencoEkert1996}, as built in the proof of Lemma~\ref{lem:qft-mod} and in the
paragraph ``Binary arithmetic and explicit transforms'' of Section~\ref{sec:compile}
(\file{theorems/rees_circuit_arith.py}); the gate counts are those of the generated gate
lists, and the correctness of the blocks for general $b$ is the standard one, checked
exhaustively only for $p \le 13$. For $p=2$ these operations cost $O(1)$ gates. No inversion
modulo $p$ is performed by a gate: the divisions by $k+1 \le c$ in
Theorem~\ref{thm:uniform-compilation}(i) are multiplications by constants computed
classically, and the unit inversions of Lemmas~\ref{lem:tb-chart} and~\ref{lem:tb-sylow} are
classical bit operations counted in~(d). (Were an inversion needed coherently, Fermat
exponentiation costs $O(\log^3 p)$ gates and the bound in~(a) is unchanged, since
$n_p^3\log^3 p \le \ell^3$.) Hypothesis \textup{(H3)}: one run of
```

(Replace `sec:compile` by the actual label of the section containing the paragraph; I did not
find it with certainty. If the paragraph has no section label, write "Section on uniform
compilation".) Also change "which by~(H2) and $n_p\log_2 p \le \ell$" in the proof of (a) to

```
which by the gate cost $O(\log^2 p)$ per field operation of~(H2) and $n_p\log_2 p \le \ell$
```

(optional; the existing wording still reads correctly if (H2) is kept as a labelled
statement).

main.tex, thm:bb-envelope(iii), replace "Under the compilation hypotheses (H2) and (H3) of
Proposition~\ref{prop:tb-count-gates}, and with Lemma~\ref{lem:qft-mod} for the transforms," by

```
Under the hypothesis (H3) of Proposition~\ref{prop:tb-count-gates}, with the field arithmetic
of Section~\ref{sec:compile} (its (H2), discharged there) and Lemma~\ref{lem:qft-mod} for the
transforms,
```

and the later sentence at ~986 "under the compilation hypotheses (H2)--(H3) of
Proposition~\ref{prop:tb-count-gates}, which this paper states ..." should be reworded to
name (H3) alone (I read only its start; the rest of that sentence was not inspected).

If the owner prefers not to rely on the [argued] general-b correctness, the narrower
alternative is to keep (H2) but narrow it to: "(H2) addition, multiplication by a constant and
multiplication of two registers over $\Fp$ ($p$ odd) cost $O(\log^2 p)$ gates; this holds by
the constructions of Section~\ref{sec:compile}, with counts verified by computation for
primes up to $2^{61}-1$ and correctness verified exhaustively for $p\le 13$, and no inversion
is needed."

Status: AI-checked, pending human review.

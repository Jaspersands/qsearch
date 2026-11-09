# Rees HSP referee 5: Section `sec:uniform-compilation` (circuits, QFT, coherent SDE, receiver)

Date: 2026-11-04. Referee: Claude Code subagent (AI only, pending human review). Scope:
`docs/papers/rees-hsp/main.tex`, Section `sec:uniform-compilation` up to `\section{Parameterized
Regimes}`. No .tex file was edited. No git or network was used.

**Line numbers.** `main.tex` changed while this review ran (mtime 18:14). The section moved down 9
lines, and Remark `rem:is-runtime` (line 591) plus sentences citing it were added. All line numbers
below refer to a snapshot taken at 18:15, where the section spans lines 709-927. Quotes are exact
from that snapshot.

**Counts.** 2 Errors, 3 Gaps, 16 Imprecisions, 13 Style (3 notation, 10 long sentences).

The findings of `2026-11-04-rees-coherent-receiver-check.md` were not re-reported. Their fixes in
the proof of `prop:coherent-receiver` (merge isometry, transform direction, reused workspace,
`s_i=0`, qubit count) read correctly. G1, G3 and I10 concern text added after that check.

---

## 1. Errors

### E1. Wrong count of nonnormal subgroups at class four over F_5 (line 779)

> "we take nine hidden subgroups, six of them nonnormal."

The nine subgroups, per `2026-11-03-rees-circuit-3.md` line 160, are
`{1, <e1>, <e2>, <e3>, <e5>, <e2,e5>, <e1+e2+e5>, gamma_3, gamma_2}`, with brackets `[e1,e_i]=e_{i+1}`
for i = 2, 3, 4. Here `e5` is central, so `<e5>` is normal, and `gamma_3 = <e4,e5>` and
`gamma_2 = <e3,e4,e5>` are ideals. So four are normal (1, `<e5>`, gamma_3, gamma_2) and five are
nonnormal (`<e1>`, `<e2>`, `<e3>`, `<e2,e5>`, `<e1+e2+e5>`). This matches the c4 report on the same
list over F_7: "five of the eight subgroups are non-normal", with gamma_2 left out. The miscount
comes from the circuit-3 report, which should be fixed too.

Fix:
```latex
we take nine hidden subgroups, five of them nonnormal.
```

### E2. "No code generates these circuits" contradicts the backends (line 853)

> "... Lemmas~\ref{lem:coherent-quadratic-sde} and~\ref{lem:coherent-power-sde}, which are explicit
> circuits $W_d$ at their arities once their classical parameters are found (Las Vegas) before the
> circuit is generated; ... No code generates these circuits: the Schedule~1 solver ..."

The nearest antecedent of "these circuits" is the set of lemma-based receivers. Code does generate
those circuits: `rees_coherent_sde*.py` emits the `W_d`, and the fourth and fifth backends,
`rees_circuit_full.py` and `rees_circuit_coherent_c4.py` wire them into coherent receivers on four
instances (lines 777, 781). The intended claim is that no code generates the circuit `C` of the
proposition for general inputs. Also, "no reversible compilation of it exists" states as fact
something that has only not been written.

Fix (replaces the last sentence of line 853):
```latex
No code generates the circuit $\mathcal{C}$ of Proposition~\ref{prop:coherent-receiver} for general inputs: the generated coherent-label circuits of the fourth and fifth backends, \file{theorems/rees_circuit_full.py} and \file{theorems/rees_circuit_coherent_c4.py} use the witness circuits of Lemmas~\ref{lem:coherent-linear-sde}--\ref{lem:coherent-power-sde} on fixed instances only. The Schedule~1 solver of Section~\ref{sec:sde} is a classical program, and no reversible compilation of it has been written. The explicit bound $T^{\mathrm{IS}}_d$ of Remark~\ref{rem:is-runtime} rests on a standard Turing-machine layout argument that is not written out.
```

---

## 2. Gaps

### G1. Prop (iv) now depends on an unwritten argument that its title omits (line 830)

> "By Remark~\ref{rem:is-runtime} one may take $T^{\mathrm{IS}}_d = C_1 d^3 M_d b^3(g_d^2+b^2)$, so
> that $R_d = O\bigl(d^3 M_d b^3 (g_d^2+b^2)\log(M_d b)\bigr)$."

Remark `rem:is-runtime` gives this `T` only "granting that a multitape Turing machine runs this
level-by-level computation with constant-factor overhead (a standard layout argument that is not
written out here)". The proposition's title lists only Theorem `thm:is-import` and
Pippenger-Fischer as conditions. Line 853 states the caveat, but the proposition does not.
Polynomiality itself needs only some polynomial `T`, which the statement already assumes. The
explicit `T` should carry the caveat.

Fix (item (iv), last sentence):
```latex
Granting the Turing-machine layout argument of Remark~\ref{rem:is-runtime}, which is not written out, one may take $T^{\mathrm{IS}}_d = C_1 d^3 M_d b^3(g_d^2+b^2)$, so that $R_d = O\bigl(d^3 M_d b^3 (g_d^2+b^2)\log(M_d b)\bigr)$.
```
Also add to the bracketed title, after "imported": `; the explicit $T^{\mathrm{IS}}_d$ of~(iv) also on the layout argument of Remark~\ref{rem:is-runtime}`.

### G2. Lemma `lem:coherent-power-sde` claims polynomial time for a randomized search (line 807)

> "a contraction is found by the search of Proposition~\ref{prop:decoupled-sde}, so the gate list is
> computed in time polynomial in its length for fixed $\kappa$."

For `p >= T_S(kappa)`, Proposition `prop:decoupled-sde` finds the scalars by uniform draws with
abort probability `2^{-k}`, so the search is Las Vegas. Finding `g` from uniform draws with success
probability `phi(kappa)/kappa` is also Las Vegas. The artifact takes the least `g` and the
lexicographically least contraction. That is deterministic, but no polynomial bound is known for it
in general; for the least `g` this is the least-nonresidue problem. Line 853 calls the same step Las
Vegas, so the lemma contradicts it.

Fix:
```latex
The circuit takes $g$ and $(\alpha,\beta)$ as classical parameters, found before the gate list is generated: a uniform element of $\Fp^\times$ generates $\Fp^\times/P$ with probability $\varphi(\kappa)/\kappa$, and a contraction is found by the randomized search of Proposition~\ref{prop:decoupled-sde}, so the gate list is computed in expected time polynomial in its length for fixed $\kappa$ (Las Vegas). The deterministic choice of the artifact is not claimed to be polynomial.
```

### G3. Reset count omits the label registers (line 853)

> "Measuring and resetting each of them after its last use would not change the terminal state, and
> it would restore the depth-first count of Theorem~\ref{thm:uniform-compilation}(iv) plus $W$."

Theorem (iv) counts only cover-sized group registers. `W` (Prop (iv)) holds the solver, dilation,
translation and transform workspace. Neither holds the `M_d g_d b` label qubits of the node being
merged, and `W_d` needs all of them at once. In a depth-first order only one node's labels are live
at a time, so the fix is one term.

Fix:
```latex
Measuring and resetting each of them after its last use would not change the terminal state, and it would restore the depth-first count of Theorem~\ref{thm:uniform-compilation}(iv) plus $W$ plus the $\max_d M_dg_db$ label qubits of the one node being merged.
```

---

## 3. Imprecisions

### I1. "Run that proposition" points to the wrong proposition (line 807)

> "... found by the search of Proposition~\ref{prop:decoupled-sde}, ... Run that proposition on
> $M=(a+1)(a+2)/2$ columns"

In Lemma `lem:coherent-quadratic-sde` the antecedent is `prop:triangular-sde`. Here the nearest
proposition is `prop:decoupled-sde`, whose arity is `(a+1)((kappa-1)a+1)`.

Fix: `Run Proposition~\ref{prop:triangular-sde} on $M=(a+1)(a+2)/2$ columns`

### I2. `Q_q` undefined (line 811)

> "with the fixed generator $g^{Q_q}$ of the $q$-Sylow subgroup"

Only `S_q` is defined, in the statement. The report defines `p-1 = q^{S_q} Q_q` with `q` not
dividing `Q_q`.

Fix (statement, after "where $q^{S_q}\,\|\,p-1$"): `and $Q_q=(p-1)/q^{S_q}$`. Long sentence L2 below also includes it.

### I3. Wrong paragraph cited for the arithmetic ancillas (line 756)

> "the $3b+5$ arithmetic ancillas of the second backend of the paragraph on gate-level control below"

Since the 11-04 split, the second backend is in the paragraph "Binary arithmetic and explicit
transforms", not "Gate-level control".

Fix: `the $3b+5$ arithmetic ancillas of the second backend (paragraph ``Binary arithmetic and explicit transforms'' below)`

### I4. The wiring sentence attributes Lemma `lem:coherent-linear-sde` to instances that do not use it (line 792)

> "...which Proposition~\ref{prop:coherent-receiver} makes coherent by a reversible simulation of
> Schedule~1; only the two instances of the fourth backend, the one of the fifth and the class-four
> instance over $\mathbb{F}_7$ above are wired."

This sentence follows Lemma `lem:coherent-linear-sde`, so readers take it as that lemma's wiring.
That lemma needs `kappa_d = 1`, which occurs only at grade three of the filiform algebra over F_5,
in the fourth backend. Heisenberg over F_3 has only grade 2, the fifth backend has `kappa = 3, 2`,
and class four over F_7 has `kappa = 2, 3, 2`. "Makes coherent" also overstates an existence
result.

Fix (replaces from "these lemmas do not cover" to the end of the paragraph):
```latex
these lemmas do not cover the solves at $p\in E_2(\kappa_d)$, which Proposition~\ref{prop:coherent-receiver} shows can be made coherent by a reversible simulation of Schedule~1. This lemma is wired only into the fourth backend, at grade three of the class-three filiform algebra over $\mathbb{F}_5$; the wiring of Lemmas~\ref{lem:coherent-quadratic-sde} and~\ref{lem:coherent-power-sde} is stated after each of them.
```

### I5. Parenthesis swallows a claim, and an AI-only input is not cited (line 814)

> "... in particular at every grade of every class-three instance (for example the class-three
> filiform algebra over $\mathbb{F}_7$, whose grade three has $\kappa_3=3$, and at every grade of
> every class-four instance with $p\notin E_2(4)=\{5,13,17,29,37,53\}$)."

The class-four claim sits inside "(for example ...". "Every class-three instance" uses
`E_2(3) = ∅`, which comes from the AI-only computation after `prop:decoupled-sde`. The
conditionality on `prop:triangular-sde` is also dropped. This is long sentence L10.

Fix (replaces the first sentence of line 814 from "; together with"):
```latex
. Together with Lemmas~\ref{lem:coherent-linear-sde} and~\ref{lem:coherent-quadratic-sde}, and conditionally on Proposition~\ref{prop:triangular-sde}, it makes the solve of~\eqref{eq:sde-target} coherent at every grade with $p\notin E_2(\kappa_d)$. Since $E_2(2)=E_2(3)=\emptyset$ (Lemma~\ref{lem:coherent-quadratic-sde} and the AI-only computation recorded after Proposition~\ref{prop:decoupled-sde}), this covers every grade of every class-three instance, for example the class-three filiform algebra over $\mathbb{F}_7$, whose grade three has $\kappa_3=3$, and every grade of every class-four instance with $p\notin E_2(4)=\{5,13,17,29,37,53\}$.
```

### I6. Dangling "the checks below" (line 779)

> "for nine subgroups, five of them nonnormal, the checks below pass, with all label pairs ..."

Nothing below describes checks for the class-three algebra over F_5, a leftover from the 11-04
split. The checks are in `2026-11-03-rees-circuit-2.md`, Acceptance 2.

Fix:
```latex
for nine subgroups, five of them nonnormal, every top source equals the coset density of $\exp(\hlift)$, every label law is uniform on $K_d^\perp$ and every checked merge output is $\rho_{H_{d-1}}$, with all label pairs and witnesses merged at grade three and sampled ones at grade two; the readout is uniform on $\hh^\perp$, and all $18$ seeded runs recover $\hh$;
```

### I7. Qubit counts mix conventions (line 779)

> "one terminal sample uses $744$ qubits" ... "($10002$ qubits per terminal sample without reuse)" ...
> "($16302$ qubits per terminal sample, plus the $3b+5=14$ arithmetic ancillas)"

All three numbers are from the first backend, which has value-controlled arithmetic and no
arithmetic ancillas (circuit-2 report, table at lines 249-252). Only the F_7 count says so. The
binary-arithmetic counts are 758, 10016 and 16316 (c4 report line 94). Consistency check: 835 = 744 +
14 + 77 and 154 = 82 + 11 + 61, the third backend adding `3b+5` and `4b+2t+1`.

Fix: insert `with the original arithmetic backend` after "uses $744$ qubits", after "($10002$ qubits per terminal sample", and replace the F_7 parenthesis by
```latex
($16302$ qubits per terminal sample with the original arithmetic, $16316$ with the binary arithmetic and its $3b+5=14$ ancillas)
```

### I8. Opening audit sentence is stale (line 716)

> "This section was re-audited on 31 October. Every tabulated number reproduces from its artifact,
> but several statements and labels were corrected."

The section now holds 3-4 November material, including Lemma `lem:qft-mod`, three coherent lemmas,
the proposition, five backends and `tab:fcs-budget`, whose numbers are "not macros" (line 909).
Readers will take the 31 October audit to cover all of it.

Fix:
```latex
Theorem~\ref{thm:uniform-compilation} and Tables~\ref{tab:full-grade-budget} and~\ref{tab:random-column-budget} were re-audited on 31 October; every number in those two tables reproduces from its artifact, and several statements and labels were corrected. The material added on 3 and 4 November carries its own labels. The note \file{research/REES_UNIFORM_INSTRUMENT_COMPILATION.md} gives the argument for the theorem in full.
```

### I9. Existence results phrased as constructions (lines 781, 814)

> 781: "Proposition~\ref{prop:coherent-receiver} below shows that such a receiver exists"
> 814: "Proposition~\ref{prop:coherent-receiver} below supplies a general receiver"

Neither sentence states the conditions (Theorem `thm:is-import`, Pippenger-Fischer). Line 814's
"supplies" reads as a construction. The same paragraph does call it "an existence statement".

Fix (781): `Proposition~\ref{prop:coherent-receiver} below shows, conditionally on Theorem~\ref{thm:is-import}, that such a receiver exists,`
Fix (814): `Proposition~\ref{prop:coherent-receiver} below shows, conditionally on Theorem~\ref{thm:is-import}, that a general receiver exists at the arities of Theorem~\ref{thm:main},`

### I10. `R_d` used in the statement but defined only in the proof (line 823)

> "and $R_d \le C_0\,T^{\mathrm{IS}}_d\log T^{\mathrm{IS}}_d + M_d b$"

The statement bounds `R_d` but never says that `R_d` is the gate count of `W_d`.

Fix:
```latex
and let $R_d$, the number of gates of the reversible solver $W_d$ built in the proof, satisfy $R_d \le C_0\,T^{\mathrm{IS}}_d\log T^{\mathrm{IS}}_d + M_d b$,
```

### I11. Conditionality dropped in the summary sentences (lines 803, 814)

> 803: "together with Lemma~\ref{lem:coherent-linear-sde} it makes the solve of~\eqref{eq:sde-target}
> coherent at every grade with $\kappa_d\le2$"

The lemma titles say "conditional on Proposition~\ref{prop:triangular-sde}", but these summaries
leave it out. Fixed by L6 (line 803) and I5 (line 814).

### I12. Third-backend eta and TV figures differ from the report (line 775)

> "with $\eta = 1.5\cdot10^{-3}$ ... $0.0993$ resp.\ $0.0895$"

`2026-11-04-rees-qft-wire.md` (lines 319-320) runs at eta = 1.488e-3 and 2.799e-4 and reports TV
0.0987 and 0.0894. The paper's values are valid: eta = 1.5e-3 and 2.8e-4 give the same
`(t,r,tau) = (26,19,15)` and `(32,22,18)`, and I recomputed 7 x 0.014177 = 0.0992 and
8 x 0.011178 = 0.0894. A reader comparing with the report will still see a mismatch.

Fix (append to the sentence ending "of that of the run with exact transforms"):
```latex
(the artifact generates these circuits at $\eta = 1.488\cdot10^{-3}$, resp.\ $2.799\cdot10^{-4}$, which give the same $(t,r,\tau)$; the bounds here are for the rounded $\eta$)
```

### I13. Citation does not state what it is cited for (line 838)

> "so that $G = -\delta_{s_i}(\sigma(q))$ by Theorem~\ref{thm:rees-cover}(ii)"

Theorem `thm:rees-cover`(ii) says that `delta_lambda`, `lambda` nonzero, is an automorphism. The
step uses the definition of `delta_s` (grade-k coordinates scaled by `s^k`, Section `sec:intro`) and
the fact that BCH inversion is negation, and it is also applied at `s_i = 0`.

Fix: `so that $G = -\delta_{s_i}(\sigma(q))$, by the definition of $\delta_s$ in Section~\ref{sec:intro} and since the BCH inverse of $x$ is $-x$ (at $s_i=0$ this gives $G=0$),`

### I14. Table sources sentence (line 857)

> "Tables~\ref{tab:full-grade-budget} and~\ref{tab:random-column-budget} report upper bounds, with
> padded caps, generated from ... and \file{rees_hsp_reduction.json} via \file{make_numbers.py}."

`rees_hsp_reduction.json` feeds the closing paragraph, not either table. `tab:fcs-budget` is not
mentioned here.

Fix:
```latex
Tables~\ref{tab:full-grade-budget} and~\ref{tab:random-column-budget} report upper bounds, with padded caps, generated from \file{rees_full_grade_budget.json}, \file{rees_uniform_instrument.json} and \file{random_column_rees.json} via \file{make_numbers.py}; the closing paragraph uses \file{rees_hsp_reduction.json}, and Table~\ref{tab:fcs-budget} is described in its caption.
```

### I15. The Instances paragraph has no artifact or label (line 779)

The other paragraphs name their artifact and say "finite computation, AI-checked, pending human
review". Instances names neither, though its class-four F_5 runs come from `rees_circuit_general.py`
and the circuit-3 report.

Fix (insert after "\paragraph{Instances.}"):
```latex
(\file{theorems/rees_circuit_general.py}; reports \file{research/audits/reviews/2026-11-03-rees-circuit-2.md} and \file{research/audits/reviews/2026-11-03-rees-circuit-3.md}; finite computation, AI-checked, pending human review.)
```

### I16. Lemma statements use notation defined only inside a proof (lines 796, 807)

> "the stop test $v_{k+1}\in U_k$ of round $k$", "the columns of block $k$"

`v_k`, `U_k`, the round structure (called "block k" here), `R`, `e_{k+1}` and `cos` are introduced
in the proof of `prop:triangular-sde`, not in its statement.

Fix (insert in both lemmas after "with this contraction,"): `in the notation of the proof of Proposition~\ref{prop:triangular-sde} (rounds $k$, block $k$ the columns taken in round $k$, $U_k$, $v_{k+1}$, $R$),`

---

## 4. Style

### S1. Notation clashes in the section

The section uses many symbols for two or three things at once:
- `S`: the shift and the phase gate in the proof of `lem:qft-mod`, the 2-adic exponent in
  `lem:coherent-quadratic-sde`, and the number of terminal samples in the proposition.
- `Q`: the Grover iterate, the odd part of `p-1`, the query count and the quotient `G/Z`.
- `P`: the MAC count of `lem:coherent-linear-sde`, `(F_p^x)^kappa`, and leaves per sample.
- `m`: a nonresidue and `dim L`.
- `g`: the row count of `lem:coherent-linear-sde`, the coset generator and `g_d`.
- `G`: a register and the group. `W`: a register, the workspace and `W_d`. `n`: the adder width and
  the cover dimension.

Minimal drop-ins:
- `lem:qft-mod` proof, line 756: `$\mathrm{Sh}|y\rangle = |y+1 \bmod N\rangle$ on $C_N$; then $\mathrm{Sh}\,\chi_x = \omega^{\nu}\chi_x$`. Also replace "The shift has eigenvalue" by "$\mathrm{Sh}$ has eigenvalue", and line 770 "on $n$ bits uses $6n+1$" by "on $k$ bits uses $6k+1$".
- `lem:coherent-linear-sde`, line 785: `It uses $N_\times=g^3+2g^2+5g+4g\,\ell(p-2)+2(g+1)\,\ell(e)$ modular multiply-accumulates`. In the proof, `so $N_\times = 2n_F + 2(g+1)\ell(e)$`.
- `lem:coherent-quadratic-sde`, line 796: `$p-1=2^{S_2}Q_2$ with $Q_2$ odd, $\nu$ a quadratic non-residue with $\nu-1$ a nonzero square ... $\mu=\nu-1$`. Use `$T_p\le 2b+S_2^2/2+2S_2$` and `$S_2-1$ fixed rounds`, and in the proof `$\alpha_0+\beta_1=\nu\notin P$`, `$1,\nu,\mu$`, `$\nu^{Q_2}$`. This matches `S_q, Q_q` of the next lemma.
- Proposition, line 838: write the register as `$\mathrm{G}$` (roman, like `$\mathrm{L}$` and `$\mathrm{S}$`).

### S2. Accumulator notation `t` and `kappa` (line 775)

> "One multiplication $t \leftarrow t+\kappa ab$"

Two sentences later, `t` is the phase-estimation width in "$4b+2t+1$", and `kappa` collides with
`kappa_d`.

Fix: `One multiply-accumulate $z \leftarrow z+\gamma xy$, with $\gamma\in\Fp$ a constant,`

### S3. Spelling and recovery notation (lines 777, 779)

The section writes both "non-normal" (777) and "nonnormal" (779); the paper uses each 6-8 times.
It also writes both "recover $\log H$" (777, twice) and "recover $\hh$" (779), which are the same
object.

Fix: use `nonnormal` and `recover $\hh$` throughout lines 777-779.

### S4-S13. Ten sentences over 80 words, worst first, with drop-in splits

**L1 (line 777, 162 words), fifth backend.** Replace from "A fifth backend" to "four non-normal.":
```latex
A fifth backend, \file{theorems/rees_circuit_coherent_k3.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-coherent-k3.md}; finite computation, AI-checked, pending human review), does the same on the class-three filiform algebra over $\mathbb{F}_7$, whose grade three has $\kappa_3=3$. It uses the circuit of Lemma~\ref{lem:coherent-power-sde} at grade three and that of Lemma~\ref{lem:coherent-quadratic-sde} at grade two, with merge arities $3$ and $6$ instead of $4$ and $5$. One terminal sample uses $1629$ qubits ($648$ of them oracle outputs; no reuse) and $4832806$ gates, excluding the oracle and $230$ exact transforms. The grade-three merge block equals the right translation by $-\delta_s(\sigma(q))$ with clean workspace on all $7^3\cdot7^6$ pairs of label triple and $q$ (with sampled targets), and the grade-two block does so on samples. With witnesses computed by the circuit, every merged output equals $\rho_{H_{d-1}}$ for nine hidden subgroups, five of them nonnormal (all label tuples of positive probability at grade three, all or sampled ones at grade two). Seeded runs of the measured-label simulation with these witnesses (two seeds each) recover $\hh$ for six of them, four of them nonnormal.
```

**L2 (line 811, ~130 words), proof of `lem:coherent-power-sde`.** Replace from "$F$ runs all" to "adds the result into the output and uncomputes." This also fixes I2:
```latex
$F$ runs all $a+1$ rounds obliviously. In each round it computes the first dependency by the machine of Lemma~\ref{lem:coherent-linear-sde}, the coset flags by comparing $y^h$ with the powers of $g^h$, and the constants $\alpha_{\mathrm{cos}(\zeta)}$ and $\beta_{\mathrm{cos}(\delta)}$ loaded under these flags. It then forms $v_{k+1}$, the one-hot stop flags from the flags of the $\delta_i$, the coordinates selected under the stop flags, the back substitution and the weights. $C$ computes, per column, a $\kappa$-th root by one Adleman--Manders--Miller $q$-th-root extraction for each prime factor $q$ of $\kappa$, counted with multiplicity, with the fixed generator $g^{Q_q}$ of the $q$-Sylow subgroup, where $Q_q=(p-1)/q^{S_q}$; each round uses $q-1$ equality flags and multiplications by constants loaded under them. $C$ then replaces the root by the least of its $\kappa$ multiples by powers of $g^h$ (comparators and controlled swaps), raises it to the power $u$, adds the result into the output and uncomputes.
```

**L3 (line 800, ~115 words), proof of `lem:coherent-quadratic-sde`.** Replace from "$F$ runs all" to "loaded under flags.":
```latex
$F$ runs all $a+1$ rounds obliviously. In each round it computes the first dependency by the machine of Lemma~\ref{lem:coherent-linear-sde} on $a+1$ columns, the Legendre flags by Euler's criterion and $v_{k+1}$ with masked coefficients. It then forms the one-hot stop flags from the Legendre flags, the coordinates selected under the stop flags, the back substitution with $\alpha$ masked by the Legendre flag of $\zeta$, and the weights with the constants $1,m,\mu$ loaded under flags.
```

**L4 (line 775, 124 words), third-backend TV sentence.** Replace from "On the Heisenberg group over $\mathbb{F}_3$ ($24$" to "except with probability below $0.1$.":
```latex
On the Heisenberg group over $\mathbb{F}_3$ there are $24$ transforms per terminal sample, $6$ of them on inputs other than $|0\rangle$; with $\eta = 1.5\cdot10^{-3}$, hence $(t,r,\tau) = (26,19,15)$ and $3\pi2^{-\tau} < 2.9\cdot10^{-4}$, the bound per terminal sample is below $0.0142$. On the class-three filiform algebra over $\mathbb{F}_5$ of the Instances paragraph there are $148$ transforms, $24$ of them on inputs other than $|0\rangle$; with $\eta = 2.8\cdot10^{-4}$, hence $(t,r,\tau) = (32,22,18)$ and $3\pi2^{-\tau} < 3.6\cdot10^{-5}$, the bound is below $0.0112$. So the output distribution of a run with $7$, resp.\ $8$, terminal samples is within total variation distance $0.0993$, resp.\ $0.0895$, of that of the run with exact transforms. Equivalently, there is a coupling of the two runs under which all terminal samples agree except with probability below $0.1$.
```

**L5 (line 777, 119 words), coherent class-four circuit.** Replace from "A coherent-label version" to "and on samples at grade two.":
```latex
A coherent-label version of the class-four circuits over $\mathbb{F}_7$ of the Instances paragraph, \file{theorems/rees_circuit_coherent_c4.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-coherent-c4.md}; finite computation, AI-checked, pending human review), uses the circuits of Lemmas~\ref{lem:coherent-quadratic-sde} and~\ref{lem:coherent-power-sde} at grades four, three and two ($\kappa_d = 2, 3, 2$; merge arities $3$, $6$ and $10$ instead of $3$, $7$ and $7$). One terminal sample uses $20566$ qubits ($10800$ of them oracle outputs; no reuse) and $83492540$ gates, excluding the oracle and $3330$ exact transforms. Its merge blocks equal the right translation by $-\delta_s(\sigma(q))$ with clean workspace on all label triples at grade four, on all rank-at-most-one label tuples and one tuple per row space at grade three (with sampled targets and $q$), and on samples at grade two.
```

**L6 (line 803, 116 words), k2 artifact.** Replaces the whole paragraph and fixes I11:
```latex
The artifact \file{theorems/rees_coherent_sde_k2.py} (report \file{research/audits/reviews/2026-11-04-rees-coherent-sde-k2.md}; finite computation, AI-checked, pending human review) emits this circuit and checks it on every canonical input for $a=1$, $p\le41$, and for $a=2$, $p\in\{3,5\}$, with $a\le4$ sampled. Together with Lemma~\ref{lem:coherent-linear-sde}, and conditionally on Proposition~\ref{prop:triangular-sde}, it makes the solve of~\eqref{eq:sde-target} coherent at every grade with $\kappa_d\le2$, hence at every grade when $\gcd(p-1,\operatorname{lcm}(2,\dots,c))=2$. When $\kappa_d=2$ it runs at merge arity $(g_d+1)(g_d+2)/2$, which equals the Chevalley--Warning arity $2g_d+1$ of the first three backends only for $g_d=1$. It is wired only into the fourth backend, at its two instances; into the fifth, at grade two of the class-three filiform algebra over $\mathbb{F}_7$ ($a=2$, $p=7$, checked there on samples); and into the coherent class-four circuit over $\mathbb{F}_7$, at grades four and two.
```

**L7 (line 758, 112 words), Grover step.** Replace from "With the reflection" to "$\tilde\alpha = \alpha(\tilde\theta)$.":
```latex
Let $S_\chi = I - 2\Pi_{F<N,\,a=1}$ (a comparison into a clean qubit, a controlled $Z$, the comparison again) and $S_0 = I - 2|0\rangle\langle0|$ (a Toffoli chain). One Grover iteration $Q = -A S_0 A^\dagger S_\chi$ rotates by $2\alpha$ in the plane of $|g\rangle$ and the bad part, so $QA(\tilde\theta)|0\rangle = \sin(3\tilde\alpha)|g\rangle + \cos(3\tilde\alpha)|g^\perp\rangle$, $\tilde\alpha = \alpha(\tilde\theta)$.
```

**L8 (line 777, 109 words), fourth backend.** Replace from "A fourth backend" to "by Proposition~\ref{prop:descent}.":
```latex
A fourth backend, \file{theorems/rees_circuit_coherent.py} (report \file{research/audits/reviews/2026-11-04-rees-circuit-coherent.md}; finite computation, AI-checked, pending human review), measures nothing before the final Fourier sampling on the Heisenberg group over $\mathbb{F}_3$ and the class-three filiform algebra over $\mathbb{F}_5$, where every grade has $\kappa_d\le2$. The instrument labels stay in registers, the circuits of Lemmas~\ref{lem:coherent-linear-sde} and~\ref{lem:coherent-quadratic-sde} write the witness into a register, the right translation by $-\delta_s(\sigma(q))$ is computed from that register, and the witness is then uncomputed. The labels and the consumed targets stay as garbage that no later gate touches, so by deferred measurement the reduced state is that of the measured circuit with the same witness rule, hence $\rho_{H_{d-1}}$ by Proposition~\ref{prop:descent}.
```

**L9 (line 777, 102 words), fourth-backend counts.** Replace from "With merge arity" to "all or sampled label tuples at grade two).":
```latex
The merge arity at grade two is $(g_2+1)(g_2+2)/2$: $3$ over $\mathbb{F}_3$, equal to the Chevalley--Warning arity, and $6$ instead of $5$ over $\mathbb{F}_5$. One terminal sample then uses $182$ qubits and $115282$ gates, resp.\ $1198$ qubits and $2694596$ gates, excluding the oracle and the $24$, resp.\ $176$, exact transforms. Over $\mathbb{F}_3$ the whole circuit is simulated exactly, module by module, for all $19$ subgroups, and its merge block on all $3^{18}$ basis inputs. Over $\mathbb{F}_5$ each merge is checked through the exact simulation with witnesses computed by the circuit (all label pairs at grade three, all or sampled label tuples at grade two).
```

**L10 (line 814, 97 words), kappa artifact.** Split as in I5: end the first sentence after "on samples for $a\le5$ and $\kappa\in\{2,4,5\}$" and continue with the I5 text from ". Together with".

Other sentences between 80 and 95 words (lines 724, 770, 775 "For the third backend", 779, 818) can be split the same way; they were left out to keep the list at ten.

---

## 5. Checked and consistent (no finding)

- **BCH count, Theorem (i).** `sum_{j<d}(j+1)(j+2)/2 = d(d+1)(d+2)/6`. The filiform F_5 bound
  is 40 grade-3 passes x 20 + 20 grade-2 passes x 4 = 880, as stated. Passes: 5 x 2 x 4 + 5 x 4 = 60.
  Oracle calls 10 x 3 = 30. Heisenberg F_3: 3 leaves, 6 calls, 12 passes.
- **Transform counts per terminal sample, from `q_max`.** Leaves `n`, merges `2M_d g_d + D_{d-1}`,
  readout `m`:

  | Instance | Total | Non-zero inputs |
  |---|---|---|
  | Heis F_3 (g = (3,1)) | 24 | 6 |
  | n4 F_5, arity 5 | 148 | 24 |
  | n4 F_5, arity 6 | 176 | 28 |
  | n4 F_7, arities (3,6) | 230 | – |
  | n5 F_7, arities (3,6,10) | 3330 | – |

  Every input-|0> transform is a forward one.
- **QFT parameters.** `(t,r,tau)` follows from eta: (26,19,15) at 1.5e-3, (32,22,18) at both
  2.8e-4 and 2.5e-4. Also `3 pi 2^-15 = 2.876e-4` and `3 pi 2^-18 = 3.595e-5`.
- **TV bounds.** 6 eta + 18 x 3 pi 2^-tau = 0.01418, so 0.0993 for 7 samples. 24 eta +
  124 x 3.595e-5 = 0.01118, so 0.0895 for 8. 28 x 2.5e-4 + 148 x 3.595e-5 = 0.01232, so 0.0986
  for 8.
- **Qubits and gates.** 154 = 82 + 11 + 61. 835 = 744 + 14 + 77. The full backend's count minus
  the fourth's equals the third's transform gates: 304234 - 115282 = 188952 = 24 x 7873, and
  5035924 - 2694596 = 2341328 = 176 x 13303. Per-transform counts 7873 and 13303 lie below the
  lemma's bound, 8405 and 14948. Oracle-output qubits: 54 x 12 = 648 and 720 x 15 = 10800.
  Numbers match the cited reports: qft-wire, circuit-coherent, -full, -k3, -c4, circuit-arith,
  coherent-sde, -k2, -k3.
- **Lemma `lem:qft-mod`.**
  - The gate-sum coefficients 328, 92, 2, (b+5), 26, 240 and 60 add up from the stated block
    counts.
  - With the stated bounds on `t`, `r`, `tau`, the asymptotic form `420b^2 + 187bL + 4L^2`
    follows.
  - Each error term is at most eta/3.
  - The bad-mass bound, the preparation angle bound (`d alpha/d theta <= 1` since `rho <= 1`) and
    the global phase `-e^{i theta}` times `-e^{-i theta}` = 1 are all correct.
  - The zero-input argument (each `CR_k^{-1}` meets a qubit already at |0>) and the `V^dagger`
    reduction are correct.
- **Lemma `lem:coherent-linear-sde`.** `2n_F + 2(g+1)l(e)` equals the stated `P`, and the
  per-column counts sum correctly. `e` is odd, so `-z^e = y^e`.
- **Lemma `lem:coherent-quadratic-sde`.**
  - The contraction conditions hold for all four `(i,j)` in the normalisation of
    `prop:triangular-sde`.
  - The least nonresidue `m` has `m-1` a nonzero square.
  - `gcd(d,p-1) = 2` implies `gcd(d/2,(p-1)/2) = 1`, so `u` exists.
  - The stop-test equivalence holds.
  - The `l(p-2)` coefficient `2a^2+2a` equals `(a+1)` rounds times `2a`.
- **Lemma `lem:coherent-power-sde`.**
  - The stop-test argument is correct, using `beta_nu != 0` for `nu != 0` from
    `1 + beta_nu ∈ g^{-nu}P ∪ {0}`.
  - Successive q-th roots of a kappa-th power give a kappa-th root, since `mu_q` lies in
    `(F_p^x)^{kappa/q}` when `kappa | p-1`.
  - `g^{Q_q}` generates the q-Sylow subgroup because `g` is not a q-th power, and `g^h`
    generates `mu_kappa`.
- **Arities.** All merge arities and "instead of" pairs equal `(g+1)(g+2)/2` versus
  `kappa g + 1`. `E_2(2) = E_2(3) = ∅` and `E_2(4) = {5,13,17,29,37,53}` match
  `prop:decoupled-sde`. "`p ∈ E_2(p-1)` for `p >= 5`" is in `appendix-schedule2.tex` line 471.
- **Proposition (iv).** The second inequality holds, using `Sn_dM_d <= Q/c` and
  `Sn_d = Q/(c prod M)`. The qubit total `(1 + 1 + (c-1)/2)Qmb = (c+3)/2 Qmb` holds.
- **Claim discipline.**
  - Nothing claims that a coherent receiver is implemented, a speedup, or novelty.
  - Every new lemma, the proposition, every backend artifact and `tab:fcs-budget` carry "AI-checked,
    pending human review". The Instances paragraph lacks the label (I15).
  - Scope correctly limits the explicit-QFT TV bounds to the third backend and
    `rees_circuit_full.py`.
  - Implemented and existence results are otherwise kept apart, except E2 and I9.

---

## Applied (11-04)

Applied to `docs/papers/rees-hsp/main.tex` by matching quoted text (backup in the session
scratchpad, `bak-i180/main.tex`). Totals: 26 applied, 7 modified, 1 skipped. Build: 141 pages,
0 Overfull, no "Float too large", no undefined references; `tests/tools/test_rees_paper_numbers.py`
passes (2), and `pytest -q tests -k "rees_circuit_sparse or rees_circuit_general"` passes (79 passed,
15 skipped).

- **E1. Applied.** Verified: the `normal` flags in `n5_f5.json`, `n5_f5_b.json` and
  `n5_f5_exhaustive.json` and an independent ideal check of the `N5_SUBGROUPS` generators give four
  ideals (1, <e5>, γ_3, γ_2) and five nonnormal subgroups. Paper now says "five of them nonnormal".
  `2026-11-03-rees-circuit-3.md` corrected at all three places (Answers item 3, Section 3, proposed
  text) with a "Correction (11-04)" note. Not edited (outside this pass): the same "6/six
  non-normal" count in `research/REES_FULL_CONTINUATION.md` line 390,
  `2026-11-04-rees-circuit-coherent-c4.md` line 33 (same list over F_7) and
  `2026-11-02-rees-integration-log.md` line 706.
- **E2. Modified.** Verified: `rees_coherent_sde*.py` emit the W_d and the coherent-label backends
  import them. The drop-in misnames the fourth and fifth backends (they are
  `rees_circuit_coherent.py` and `rees_circuit_coherent_k3.py`), so the new sentence lists all four
  coherent-label backends as the Scope paragraph does. Its last sentence ("not written out") is
  stale; the current wording "rests on the tape layout sketched there, which is AI-checked, pending
  human review" is kept. "No reversible compilation of it exists" became "has been written".
- **G1. Skipped (no change needed).** Remark `rem:is-runtime` now sketches the tape layout
  (labelled AI-checked, pending human review) and the discussion after the proposition says the
  bound rests on it; nothing is "granted" or "not written out" any more.
- **G2. Applied.**
- **G3. Applied.**
- **I1. Applied.**
- **I2. Applied** (in the statement; not repeated in the proof, see L2).
- **I3. Applied.**
- **I4. Modified.** Added "(and so into `theorems/rees_circuit_full.py`)", which also uses the
  kappa = 1 circuit through the fourth backend.
- **I5. Applied.**
- **I6. Applied.** The clause on the same algebra over F_7 is kept.
- **I7. Modified.** Inserted "with the original arithmetic" (shorter than "... backend") after 744
  and for 10002 ("with the original arithmetic, without reuse"); the F_7 parenthesis as proposed.
  No 758/10016 figures were added (10016 is not recorded in any report).
- **I8. Applied.**
- **I9. Applied** (both places).
- **I10. Modified.** Worded as "let R_d be the number of gates of the reversible solver W_d built in
  the proof, which satisfies R_d <= ...", so the bound reads as a property, not a hypothesis.
- **I11. Applied** (through L6 and I5).
- **I12. Applied.** Values checked against `2026-11-04-rees-qft-wire.md` Section 7.
- **I13. Modified.** The parenthesis "(at s_i=0 this gives G=0)" was dropped: the proof states
  "At s_i = 0 we get G = 0" two sentences later.
- **I14. Applied.**
- **I15. Applied** (adds the "AI-checked, pending human review" label to Instances).
- **I16. Modified.** In `lem:coherent-power-sde` the insertion reads "in the notation of its proof",
  since the same sentence now names Proposition `prop:triangular-sde` (I1).
- **S1. Applied:** `\mathrm{Sh}` for the shift and "on k bits uses 6k+1" in `lem:qft-mod`; `N_\times`
  in `lem:coherent-linear-sde`; `S_2`, `Q_2`, `\nu` in `lem:coherent-quadratic-sde`; register
  `\mathrm{G}` in the proposition.
- **S2. Applied.**
- **S3. Applied** in the Coherent-label backends and Instances paragraphs.
- **L1, L3-L9. Applied.** Each split keeps the original clauses and their order.
- **L2. Modified.** Split as proposed, without repeating the definition of Q_q (now in the
  statement, I2).
- **L10. Applied** (through I5).

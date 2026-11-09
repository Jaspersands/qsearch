# Rees HSP referee 7: front matter against body

Date: 2026-11-04. Referee: Claude Code subagent (AI only, pending human review). No .tex file was
edited. No git or network was used.

**Scope.** In `docs/papers/rees-hsp/main.tex`: the status box, the abstract, all of Section 1
(Background, Related work, Core idea, Input contract, `thm:main` and the paragraphs after it, the
regimes table `tab:main-regimes` and its caption, Organization), and the three notation tables
(lines 1-340). Also the description of the paper in `docs/papers/rees-hsp/README.md`. Each claim was
checked against the body and the appendices. The context was `research/STATE.md` (Rees lines) and
rows I163-I180 of `2026-11-02-rees-integration-log.md`.

**Snapshot.** `main.tex` mtime Nov 4 18:37:51, md5 `5a8984d0c0717498e592f98c04d6f265`; README mtime
17:04:49; `appendix-torsion-blackbox.tex` 18:26:03; `appendix-schedule2.tex` 18:07:49. All line
numbers refer to this snapshot.

**Counts.** 2 Errors, 6 Gaps, 9 Imprecisions, 6 Style. There are also 4 body-side notes, outside
scope and not counted.

**Claim discipline.** Nothing in the front matter claims a speedup, establishes novelty, says
anything was reviewed by a human, or says a coherent receiver is implemented. One phrase in the
Organization paragraph is ambiguous about the receiver (I1). The README says only "not implemented
in general" (folded into E2).

---

## 1. Errors

### E1. The black-box row of the regimes table states bounds for all primes that the body proves only for p > c (line 220, caption line 204)

Front matter (line 220):
> "Black-box, unique encoding (Thm.~\ref{thm:bb-envelope}) & all primes ($p \le c$ via~\cite[Thm.~1]{ImranIvanyos2023}) & ... & $O_c(N^{E_W(c)+1})$ queries, $O_c(N^{E_W(c)+4+o(1)})$ gates"

Caption (line 204): "it also covers the primes $p \le c$, through~\cite[Theorem~1]{ImranIvanyos2023}."

Body (line 1034):
> "the number of queries to $f$ for the primes $p > c$ is $O_c(N^{E_W(c)+1})$ ...; the primes $p \le c$ add the $\poly(\log|G|)$ queries of~\cite[Theorem~1]{ImranIvanyos2023}, whose exponent includes that of their exact abelian subroutine and is not bounded here. For the primes $p > c$, and for order finding, factoring and the charts, the number of gates is $O_c(N^{E_W(c)+4+o(1)})$ ... the gates and time of~\cite{ImranIvanyos2023} are added separately."

The row says "all primes" and then gives exponents. The body bounds only the primes p > c.

Fix (row):
```latex
Black-box, unique encoding (Thm.~\ref{thm:bb-envelope}) & all primes ($p \le c$ via~\cite[Thm.~1]{ImranIvanyos2023}) & combined rule on an acquired chart; $\le n_p$ socle rounds if $e_p > 1$ & for $p > c$: $O_c(N^{E_W(c)+1})$ queries and $O_c(N^{E_W(c)+4+o(1)})$ gates; the primes $p \le c$ add the $\poly(\log|G|)$ cost of~\cite[Thm.~1]{ImranIvanyos2023}, whose exponent is not bounded here \\
```
Fix (caption, last clause):
```latex
it also covers the primes $p \le c$, through~\cite[Theorem~1]{ImranIvanyos2023}, whose queries and gates are added separately and are not included in the displayed exponents.
```

### E2. README: stale page count and row range, and no mention of I172-I180 (README line 9)

Front matter:
> "**Update (4 November 2026).** `main.tex` (135 pages) carries integration rows I137–I171 ..."

Body and records: STATE.md line 87 gives "main.tex 141 pp., I137-I180". Rows I172-I180 added
`prop:coherent-receiver` (existence, I173/I175), `rem:is-runtime` (I177/I179), the discharge of
(H2)/(H3) and the per-c total-time exponents (I172/I174/I178), the E_2 refresh (I176) and referee 5
(I180). None of these is in the README. The README also states the coherent witness circuits
without their condition. Body line 814 says they hold "conditionally on
Proposition~\ref{prop:triangular-sde}" at grades with p ∉ E_2(κ_d).

Fix (Markdown; replace the paragraph):
```markdown
**Update (4 November 2026, evening).** `main.tex` (141 pages) carries integration rows I137–I180 of `research/audits/reviews/2026-11-02-rees-integration-log.md`. New since 2 November: an explicit QFT over Z/N for odd N (`lem:qft-mod`) and an optional circuit backend that uses it; coherent witness circuits for the diagonal-equation step at grades with κ_d = 1 and, conditionally on `prop:triangular-sde`, at grades with p ∉ E_2(κ_d) (`lem:coherent-linear-sde`, `lem:coherent-quadratic-sde`, `lem:coherent-power-sde`); coherent-label circuit backends wired on a few fixed small instances (Heis(F_3), the class-three filiform algebra over F_5 and F_7, the class-four filiform algebra over F_7), simulated or checked only in pieces; `prop:coherent-receiver`, which shows, conditionally on `thm:is-import`, that a coherent receiver with the queries, arities and error of `thm:main` exists (an existence statement: no generator for that circuit is implemented); `rem:is-runtime`, an explicit step bound T^IS_d = C_1 d^3 M_d b^3 (g_d^2 + b^2) for the Schedule 1 solver (operation count derived, Turing-machine layout sketched, C_1 not computed); hypotheses (H2) and (H3) of `prop:tb-count-gates` discharged, so the black-box gate count of `thm:bb-envelope` uses no compilation hypothesis (its total-time exponent is stated separately for c = 1, c = 2 and c ≥ 3 and rests on the AKS bound Õ(log^{21/2}); a sharper AKS exponent recalled by AI reviews is unconfirmed); refreshed E_2(8), E_2(9) data (every prime decided up to 11161 for κ = 8 and up to 13807 for κ = 9; 11161 ∈ E_2(8), 17713 ∈ E_2(9)); and the Lean section at class five (417 `#print axioms` guards for the modules of its table, 455 in `Formal/Audit.lean`; `lake build Formal.Audit` succeeded on 4 November). All of this is AI-run and AI-checked, pending human review. No general coherent receiver is implemented, and no claim gate in `research/reductions/rees_hsp_reduction.json` changed. Continuation notes: `research/REES_FULL_CONTINUATION.md`.
```

---

## 2. Gaps

### G1. Section 1 has no Contributions paragraph (lines 108-237)

The scope names a Contributions paragraph, but `grep -i contribution main.tex` finds nothing.
Section 1 has Related work (line 126) and Organization (line 227). Apart from `thm:main`, the only
summary of results is the regimes table, so the coherent-receiver proposition, the explicit solver
time and the discharges have no summary with their status. Suggested paragraph, to go just before
`\paragraph{Organization.}` (line 227):
```latex
\paragraph{Contributions.} Every statement below has been checked by AI sessions only and is pending human review; its priority has not been assessed beyond the comparison above.
\begin{enumerate}[label=(\arabic*),leftmargin=2em]
  \item \emph{Main composition.} Assuming Theorem~\ref{thm:is-import}, Theorem~\ref{thm:main} recovers an arbitrary hidden subgroup with bounded error from the tuple lift (Lemma~\ref{lem:homogeneous}), the complete central instrument (Lemma~\ref{lem:central}) and pointwise quotient conversion (Proposition~\ref{prop:descent}), with Schedule~1 at every grade. Proposition~\ref{prop:single-evaluation} shows that one evaluation does not suffice.
  \item \emph{Schedules.} The large-field two-level schedule (Theorem~\ref{thm:power-sde}(ii), conditional), the combined per-grade rule (Remark~\ref{rem:combined-schedule}), and the random-column and free-coordinate schedules (Theorems~\ref{thm:random-column} and~\ref{thm:free-coordinate}), which use the uniform label law of fresh ideal sources. Remark~\ref{rem:is-runtime} bounds the Schedule~1 solver by $T^{\mathrm{IS}}_d = C_1 d^3 M_d b^3 (g_d^2+b^2)$ steps of one fixed multitape Turing machine, with $b = \lceil\log_2 p\rceil$ and an absolute constant $C_1$ that is not computed; the field-operation count is derived and the tape layout is sketched.
  \item \emph{Compilation and coherence.} An explicit approximate Fourier transform over $\mathbb{Z}/N$ for odd $N$ (Lemma~\ref{lem:qft-mod}). Coherent witness circuits for the diagonal equation at grades with $\kappa_d = 1$ (Lemma~\ref{lem:coherent-linear-sde}) and, conditionally on Proposition~\ref{prop:triangular-sde}, at grades with $\kappa_d \ge 2$ and $p \notin E_2(\kappa_d)$, at arity $(g_d+1)(g_d+2)/2$ (Lemmas~\ref{lem:coherent-quadratic-sde} and~\ref{lem:coherent-power-sde}). These circuits are generated and wired only into circuits for a few fixed small instances, which are checked or simulated only in pieces. Proposition~\ref{prop:coherent-receiver} shows, conditionally on Theorem~\ref{thm:is-import} and importing the oblivious simulation of~\cite{PippengerFischer1979}, that a coherent receiver with the queries, arities and error budget of Theorem~\ref{thm:main} exists. This is an existence statement, and no generator for that circuit has been implemented.
  \item \emph{Parameterized and black-box regimes.} Corollaries~\ref{cor:fpt-r} and~\ref{cor:codim} and Theorem~\ref{thm:ring-to-field} (all conditional). Theorem~\ref{thm:bb-envelope} treats black-box nilpotent groups of fixed class. It is conditional on Theorem~\ref{thm:main}, on Theorem~\ref{thm:power-sde}(ii) through the combined rule and, for $e_p > 1$, on Theorem~\ref{thm:ring-to-field}(iii). Its gate count uses no compilation hypothesis, because (H1)--(H3) of Proposition~\ref{prop:tb-count-gates} are discharged by Lemma~\ref{lem:qft-mod}, the binary arithmetic of Section~\ref{sec:uniform-compilation} and an explicit order-finding circuit.
  \item \emph{Classical boundary and formalization.} The classical query bound of Proposition~\ref{prop:classical-query}; the resulting query separation, which is conditional on Theorem~\ref{thm:main} and is not a claimed speedup for any concrete problem (Remark~\ref{rem:query-separation}); and the Lean~4 boundary of Section~\ref{sec:formalization}.
\end{enumerate}
```
Each item matches the body: items 1-2 match lines 179-186, 568-571, 591-598, 613-700. Item 3
matches lines 733, 783-853, including "That is a statement of existence: no circuit generator for
it has been implemented" (line 781). Item 4 matches lines 936-1046. Item 5 matches lines
1173-1240 ("We claim no speedup for any concrete problem", line 1240).

### G2. `rem:is-runtime` is not mentioned anywhere in the front matter (lines 200 and 231)

Front matter (line 200):
> "The running time is polynomial in this count and in $m$, $\log p$, the label width and $\log(1/\eps)$."

Organization (line 231):
> "Section~\ref{sec:sde} gives the controlled-right-action quotient conversion, the recursion and the SDE schedules."

Body (lines 593-597): one fixed multitape Turing machine computes the Schedule-1 witness "within
$T^{\mathrm{IS}}_d = C_1\, d^3\, M_d\, b^3\,(g_d^2 + b^2)$ steps, for an absolute constant $C_1$ that
is not computed". The tape layout is labelled "(AI-checked, pending human review)". The same
Organization line also leaves out `prop:triangular-sde` and `thm:free-coordinate`, and the
coherent lemmas rely on the former.

Fix (append to line 200, replacing its final sentence; see S1):
```latex
Remark~\ref{rem:is-runtime} makes the classical solver term explicit: one fixed multitape Turing machine computes the Schedule~1 witness at grade $d$ within $T^{\mathrm{IS}}_d = C_1 d^3 M_d b^3 (g_d^2+b^2)$ steps, $b = \lceil\log_2 p\rceil$, for an absolute constant $C_1$ that is not computed; the field-operation count is derived and the tape layout is sketched (AI-checked, pending human review).
```
Fix (line 231):
```latex
Section~\ref{sec:sde} gives the controlled-right-action quotient conversion, the recursion and the proof of Theorem~\ref{thm:main}, an explicit running-time bound for the Schedule~1 solver (Remark~\ref{rem:is-runtime}), the triangular two-level solver (Proposition~\ref{prop:triangular-sde}) and the SDE schedules, including the free-coordinate sampler (Theorem~\ref{thm:free-coordinate}).
```

### G3. The abstract leaves out the black-box theorem, the free-coordinate schedule and the coherent-receiver result, and mislabels what it restates (line 102)

Front matter:
> "We also restate three conditional corollaries recorded in the project notes: a large-field two-level symmetric SDE schedule; a random-column schedule that exploits the uniform law of the measured labels; and a bound $2^{O(r\log(r+2))}\cdot\poly$ in the derived dimension $r$, valid for every prime $p > c$ with the class not fixed."

Body: two of the three are theorems with full appendix proofs: `thm:power-sde` (line 613; "proof in
Appendix~\ref{app:schedule2}") and `thm:random-column` (line 672). The derived-dimension bound now
rests on `thm:free-coordinate`(iii), not on the random-column schedule. Line 939 says "conditional
on the steps behind Theorem~\ref{thm:main} and on Theorem~\ref{thm:free-coordinate}(iii)". The
abstract never mentions `thm:bb-envelope` (line 1025), which the Related work paragraph presents
as a main consequence, or `prop:coherent-receiver` (line 816).

Fix (replace the sentence):
```latex
We also give proofs, checked by AI sessions only, of conditional results: a large-field two-level symmetric SDE schedule; random-column and free-coordinate schedules that exploit the uniform law of the measured labels; a bound $2^{O(r\log(r+2))}\cdot\poly$ in the derived dimension $r$, valid for every prime $p > c$ with the class not fixed; and a bounded-error algorithm for black-box nilpotent groups of fixed class with unique encoding, polynomial in the input size. Conditionally on the Ivanyos--Santha algorithm, a coherent receiver with the same queries and error also exists; this is an existence statement, and no such circuit has been implemented.
```

### G4. The coset-copy row says "any of the above", but the body says the free-coordinate extension is only argued (line 216)

Front matter:
> "Coset-copy input & all $p > c$ & any of the above & as above, $c$ copies per source"

Body (line 939, and the proof at line 947):
> "(for coset-copy input this is argued, not proved)" ... "since that theorem is stated for oracle input, this extension is argued rather than proved."

`thm:free-coordinate`(iii) (line 696) counts "$c\,S\prod_d M_d$ oracle queries".

Fix:
```latex
Coset-copy input & all $p > c$ & any of the above; for Theorem~\ref{thm:free-coordinate}, which is stated for oracle input, the extension to copies is argued, not proved (proof of Cor.~\ref{cor:fpt-r}) & as above, $c$ copies per source \\
```

### G5. Related work does not state the hypotheses of `thm:bb-envelope`, or that its gate count no longer needs (H2) and (H3) (line 126)

Front matter:
> "and gives a bounded-error algorithm for black-box nilpotent groups of fixed class with unique encoding, polynomial in the input size. That theorem is conditional and checked by AI sessions only;"

Body (line 1026): the theorem assumes "coherent multiplication and its inverse (the appendix does
not use the inverse)" and a coherent hiding function. Line 1041: "The result is conditional on
Theorem~\ref{thm:main}, on Theorem~\ref{thm:power-sde}(ii) through the combined rule, and, for
$e_p > 1$, on Theorem~\ref{thm:ring-to-field}(iii) with its stop rules." The gate counts are proved
"with no compilation hypothesis: (H1) is proved as Lemma~\ref{lem:qft-mod}, (H2) is discharged by
the binary arithmetic ..., and (H3) by Shor's order finding built from the same blocks" (I172,
I174, I178).

Fix (replace "That theorem is conditional and checked by AI sessions only;"):
```latex
That theorem assumes coherent multiplication in the black box and a coherent hiding function; it is conditional on Theorem~\ref{thm:main}, on Theorem~\ref{thm:power-sde}(ii) through the combined rule and, for Sylow subgroups of exponent above $p$, on Theorem~\ref{thm:ring-to-field}(iii), and it is checked by AI sessions only. Its gate count uses no compilation hypothesis, since (H1)--(H3) of Proposition~\ref{prop:tb-count-gates} are discharged there;
```

### G6. The notation tables leave out symbols of the new material that occur in several sections (lines 242-340)

Line 242 says the tables "list the symbols that occur in more than one section". Missing:

- $b = \lceil\log_2 p\rceil$ (rem:is-runtime line 593, Section 5 throughout, prop:coherent-receiver
  line 818). It clashes with the table's $b = \sum_i e_i$ (line 325).
- $T^{\mathrm{IS}}_d$, $C_1$ (lines 595, 818, 830).
- $D_d$ (lines 722, 818).
- $q_{\max}$, $\eta$ (lines 568, 724, 822).
- $\ell_d$ (lines 486, 593, 606).
- $M_d^{\mathrm{tri}}$ (line 646).

Fix (rows for `tab:notation-sde`):
```latex
$b$ (bits) & $\lceil\log_2 p\rceil$, bits per $\Fp$ coordinate in Sections~\ref{sec:sde} and~\ref{sec:uniform-compilation} (not the $b$ of Table~\ref{tab:notation-bb}) & Rem.~\ref{rem:is-runtime}; Sec.~\ref{sec:uniform-compilation} \\
$\ell_d$ & number of terms, at most $\kappa_d+1$, of the zero sum of $\kappa_d$-th powers computed by the Schedule~1 solver & Sec.~\ref{sec:sde} (Schedule~1); Rem.~\ref{rem:is-runtime} \\
$T^{\mathrm{IS}}_d$, $C_1$ & step bound $C_1 d^3 M_d b^3 (g_d^2+b^2)$ of one fixed multitape Turing machine for the Schedule~1 witness; an absolute constant, not computed & Rem.~\ref{rem:is-runtime}; Prop.~\ref{prop:coherent-receiver} \\
$M_d^{\mathrm{tri}}$ & triangular arity $(a+1)(a+2)/2$ & Prop.~\ref{prop:triangular-sde} \\
```
Rows for `tab:notation-instance`:
```latex
$D_d$ & $\sum_{k \le d} g_k = \dim\A^{(d)}$ & Thm.~\ref{thm:uniform-compilation}(i) \\
$q_{\max}$, $\eta$ & bound on the single-coordinate transforms in one instrument; per-transform isometry error & Thm.~\ref{thm:uniform-compilation}(iii) \\
```

---

## 3. Imprecisions

### I1. Organization calls Proposition `prop:coherent-receiver` "a general coherent receiver" without saying it is an existence result, and drops the conditions on the coherent lemmas (line 232)

Front matter:
> "coherent witness circuits for the diagonal equation (Lemmas~\ref{lem:coherent-linear-sde}--\ref{lem:coherent-power-sde}), a general coherent receiver (Proposition~\ref{prop:coherent-receiver}), finite circuit artifacts"

Body (line 853): "Proposition~\ref{prop:coherent-receiver} is an existence statement." Line 781: "no
circuit generator for it has been implemented". It is conditional on `thm:is-import` (line 816).
Lemmas `lem:coherent-quadratic-sde` and `lem:coherent-power-sde` are "conditional on
Proposition~\ref{prop:triangular-sde}" (lines 794, 805), and the last needs p ∉ E_2(κ) (line 807).

Fix:
```latex
Section~\ref{sec:uniform-compilation} discusses gate compilation, an explicit approximate Fourier transform (Lemma~\ref{lem:qft-mod}), coherent witness circuits for the diagonal equation (Lemmas~\ref{lem:coherent-linear-sde}--\ref{lem:coherent-power-sde}; the last two are conditional on Proposition~\ref{prop:triangular-sde} and limited to grades with $p \notin E_2(\kappa_d)$), finite circuit artifacts on fixed small instances, a proof, conditional on Theorem~\ref{thm:is-import}, that a coherent receiver with the queries and error of Theorem~\ref{thm:main} exists (Proposition~\ref{prop:coherent-receiver}; an existence statement, not implemented), and the benchmark resource profiles.
```

### I2. The notation table calls E_W(c) "query exponent", but the body's query exponent is E_W(c)+1 (line 335)

Front matter:
> "$E_W(c)$, $e_d(p)$ & query exponent $\max_{p>c}(1 + \sum_{d=2}^c e_d(p))$"

Body (line 927):
> "Its query exponent in the input size is $E_W(c)+1$, where $E_W(c) = \max_{p>c}\bigl(1 + \sum_{d=2}^c e_d(p)\bigr)$ ... so $E_W(9) = 143$ and the query exponent $E_W(9)+1$ is $144$ ($146$ with Schedule~1 alone)."

E_W(c) is the exponent of the dimension in one core call's query count. Remark
`rem:combined-schedule` (line 666) uses 143 in that sense.

Fix:
```latex
$E_W(c)$, $e_d(p)$ & $\max_{p>c}(1 + \sum_{d=2}^c e_d(p))$, the exponent of the dimension in the query count of one core call under the combined rule ($E_W(9) = 143$); the black-box query exponent in $N$ is $E_W(c)+1$; per-grade exponent of the combined rule & Thm.~\ref{thm:bb-envelope} \\
```

### I3. The abstract states polynomiality without the hedge that `thm:main` carries (line 101)

Front matter:
> "With the published fixed-degree SDE algorithm of Ivanyos and Santha, the procedure is bounded-error and polynomial in $m$, $\log p$, the oracle label width and $\log(1/\eps)$ for every fixed $c$"

Body: `thm:main` is titled "Proposed explicit-Lie theorem" and says "assume
Theorem~\ref{thm:is-import}" (line 181). Remark `rem:is-import`(e) (line 588) says the reading of
Ivanyos-Santha was "checked ... by AI sessions only". Line 188: "AI-checked, pending human review".

Fix:
```latex
Assuming the fixed-degree SDE algorithm of Ivanyos and Santha as we read it (Theorem~\ref{thm:is-import}), the proposed procedure is bounded-error and polynomial in $m$, $\log p$, the oracle label width and $\log(1/\eps)$ for every fixed $c$, with an exponent that depends on $c$; its proof is AI-checked, pending human review.
```

### I4. The abstract's list of what lies outside the Lean boundary is incomplete (line 102)

Front matter:
> "BCH and Lazard transport for class $c \ge 6$, solvers and running time lie outside that boundary."

Body (lines 1298-1299): "For the SDE step, Lean checks existence and algebra but no algorithm".
"Outside the boundary are ... the existence of two-level contractions ..., the arity bounds of
Schedules~1--3, preparation of the initial lifted coset source, oracle implementation,
approximation errors, the final Fourier learning step, the running time ..., Lemma~\ref{lem:qft-mod},
the coherent witness circuits ... and every generated circuit".

Fix:
```latex
For the diagonal equation, Lean checks only existence (Chevalley--Warning), the gcd reduction and the algebra of the triangular construction. BCH and Lazard transport for class $c \ge 6$, the SDE algorithms and arity bounds, the Fourier transform and all circuits, approximation errors and running time lie outside that boundary.
```

### I5. The classical lower bound is quoted without its hypotheses (line 188)

Front matter:
> "every classical randomized algorithm needs more than $\sqrt{2(1-\delta)\,p^{m-1}}$ queries to succeed with probability $1-\delta$, even for non-normal $H$ of order $p$"

Body (lines 1173-1178): "with $m \ge 2$, and let $0 \le \delta < 1/2$". Part (ii), for
non-normal H, needs "If $\mathcal{L}$ is not abelian".

Fix:
```latex
In the same oracle model with $m \ge 2$, every classical randomized algorithm that succeeds with probability $1-\delta$, $\delta < 1/2$, needs more than $\sqrt{2(1-\delta)\,p^{m-1}}$ queries, even for non-normal $H$ of order $p$ when $\mathcal{L}$ is not abelian, and $O(p^{(m-1)/2})$ queries suffice (Proposition~\ref{prop:classical-query}).
```

### I6. The table caption does not give the status of the fixed-class row (line 204)

The caption lists every other row as a conditional corollary. That suggests the fixed-class row
needs no assumption. Body: `thm:main` assumes `thm:is-import` (line 181) and is AI-checked,
pending human review (line 188).

Fix (insert after "Each lifted source costs $c$ oracle queries, or $c$ copies of $\rho_H$."):
```latex
The fixed-class row is Theorem~\ref{thm:main}, which assumes Theorem~\ref{thm:is-import} and is AI-checked, pending human review.
```

### I7. "imported conversion steps" overstates what the black-box section imports (line 176)

Front matter:
> "Section~\ref{sec:black-box} discusses black-box nilpotent groups, which need separate, imported conversion steps."

Body (line 1010): the Sylow split and the free-Lie pullback are proved in Appendix E ("Appendix
~\ref{app:torsion-blackbox} proves it, including the linear-in-$d$ chart arithmetic"), and order
finding is built explicitly ((H3), I174). Only the bounded-prime algorithm for p ≤ c ("that cost
is imported") and Lazard functoriality are imported.

Fix:
```latex
Section~\ref{sec:black-box} discusses black-box nilpotent groups, which need separate conversion steps: a Sylow split, a free-Lie pullback and chart acquisition (proved in Appendix~\ref{app:torsion-blackbox}, AI-checked, pending human review), and, for the primes $p \le c$, the imported algorithm of~\cite[Theorem~1]{ImranIvanyos2023}.
```

### I8. The table's last column offers "total time", but the black-box row gives no total time and the caption does not mention the τ_c cases (lines 204, 209, 220)

Body (line 1034): "the total time is
$O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$ for $c \ge 3$; for $c = 2$ it is
$O(N^{\max(6+\max(3,\hat\beta_2),\,23/2)+o(1)})$, and for $c = 1$ ... $O(N^{23/2+o(1)})$". Appendix
`prop:tb-count-gates` (appendix-torsion-blackbox.tex lines 1306-1310) gives the same in the form
τ_c = max(E_W(c)+1+max(3,β̂_c), 23/2). The 23/2 rests on an AKS exponent flagged "NEEDS HUMAN
VERIFICATION" in comments in both files. β̂_c is not computed.

Fix (append to the caption):
```latex
Its total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$ for $c \ge 3$, with separate forms for $c = 2$ and $c = 1$ (the latter $O(N^{23/2+o(1)})$, set by the primality certificates); here $\hat\beta_c$ is the excess time exponent of the solvers, which is not computed (Theorem~\ref{thm:bb-envelope}).
```

### I9. README: the reproduce step claims more than the body (README lines 38, 44)

Front matter:
> "Re-run all nine underlying reduction and control generators from scratch and confirm zero differences against `numbers.tex`"

Body (line 1308): the script "compares them with the $148$ macros of \file{numbers.tex} that come
from those reports. The $15$ macros of the scaled end-to-end simulation are read from its saved run
files ..., which the script does not rerun ...; it lists them as not regenerated." Line 1306: many
quoted numbers "are not macros ... and the checks below do not cover them".

Fix (Markdown, line 44):
```markdown
Re-run all nine underlying reduction and control generators from scratch and confirm zero differences against the 148 macros of `numbers.tex` that they produce (the 15 macros of the scaled end-to-end simulation are read from saved run files and are not regenerated; numbers quoted from the AI-only reports are not macros and are not checked here):
```

---

## 4. Style

- **S1 (line 200).** "A proof assembled from the steps below is at the end of
  Section~\ref{sec:recursion}." This repeats line 188 ("The proof is at the end of
  Section~\ref{sec:recursion}"). Delete it, or replace it with the G2 sentence.
- **S2 (line 215).** "(any $p$ for part~(iii))" should be:
  ```latex
  (any $p > c$ for part~(iii))
  ```
- **S3 (lines 243, 300).** The list of letters with several meanings leaves out λ (label and
  dilation scalar), δ (dilation, error, gap, triangular δ_i), s, h, q and η. Also, u needs u ≥ 2
  (thm:random-column, line 674).
  ```latex
  Several letters, for example $N$, $\ell$, $t$, $u$, $Q$, $K$, $S$, $B$, $b$, $k$, $d$, $r$, $L$, $M$, $P$, $D$, $m$, $g$, $e$, $h$, $q$, $s$, $\lambda$, $\delta$, $\eta$, $\rho$ and $\tau$,
  ```
  ```latex
  $u$ & public integer, $u \ge 2$, $c \le u$, $a_d \le u-1$, $p \ge 16u^2$ (Schedule~3) & Thm.~\ref{thm:random-column} \\
  ```
- **S4 (line 204).** The caption describes the flat-subspace source, which has no row and no
  status. The body (line 1088) says "proposed, conditional".
  ```latex
  The flat-subspace source of Corollary~\ref{cor:subspace-hsp} (proposed and conditional; it has no row here) spends $M\ell$ exterior states per lifted source, each costing at most $N+1$ raw copies, instead of $c$ copies of $\rho_H$.
  ```
- **S5 (line 236).** Section 9 also contains Reproducibility.
  ```latex
  Section~\ref{sec:formalization} states the Lean~4 boundary and the reproducibility checks.
  ```
- **S6 (README line 3).** The one-paragraph description stops at "conditional SDE schedules and a
  derived-dimension bound, and states the Lean 4 boundary". It leaves out the black-box theorem,
  the classical query bound, the compilation section and the coherent-receiver existence result.
  Append: "It also gives a conditional all-prime black-box result at fixed class, a classical
  query lower bound, explicit compilation of the Fourier transform and arithmetic, and a
  conditional existence proof (not an implementation) of a coherent receiver."

---

## 5. Checked and consistent (no finding)

- **Organization labels.** Every label cited at lines 228-237 exists and points to the right
  place: sec:notation, sec:rees-cover, sec:instrument, sec:sde, sec:uniform-compilation,
  lem:qft-mod (line 734), lem:coherent-linear-sde, lem:coherent-power-sde (784, 806, consecutive
  with lem:coherent-quadratic-sde between), prop:coherent-receiver (817), sec:parameterized,
  sec:black-box, sec:classical-landscape, sec:formalization. The appendices run from app:schedule2
  to app:codimension, in the order of the `\input`s. No `\ref` in main.tex is undefined.
- **thm:main and the paragraph after it** (lines 179-200). The arity B_d(g_d), the query count Q,
  the inequality with C_c, and the imported ingredients agree with lines 568-571 and with
  rem:is-import(b). C_c equals the K_c of thm:bb-envelope.
- **Exponents.** 1 + Σ_{d=2}^{9} d⌈log₂(d+1)⌉ = 145 = `\ReesClassNineQueryExp`.
  E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143 matches the Schedule-1 values for c ≤ 7, and the values
  for c = 8, 9 are 2 lower, as rem:combined-schedule says. The query exponent 144 (146 with
  Schedule 1) agrees between line 927 and thm:bb-envelope ("145 at c=9" for E_W with Schedule 1).
  The gate exponent E_W(c)+4 agrees with the appendix. The τ_c cases for c ≥ 3, c = 2 and c = 1
  agree between main.tex line 1034 and the appendix (see N1 for one proviso).
- **E_2 data** (body only; the front matter quotes none). Line 635 and appendix-schedule2.tex line
  470 agree: every prime decided up to 11161 (κ = 8) and 13807 (κ = 9); 11161 ∈ E_2(8) and
  17713 ∈ E_2(9); factors 0.96 (11161/8^4.5 = 0.963) and 0.29 (17713/9^5 = 0.29997);
  E_2(8) ∩ (49417, 8^8/2] = ∅; T_A(8) ≈ 1.17·10^8 is about 14 times 8^8/2.
- **Regimes table rows 1-3, 4, 5, 7-9.** They agree with thm:main, thm:power-sde,
  rem:combined-schedule, thm:random-column, thm:free-coordinate(ii)-(iii) (arity formula
  included), cor:fpt-r (zero-sum node at p = c+1, IMS Theorem 11 for oracle input), cor:codim
  (p ≥ 2k+1 versus p ≤ 2k) and thm:ring-to-field (at most b rounds).
- **Status labels.** "AI-checked, pending human review" is attached to the proof of thm:main and
  to lem:qft-mod (line 188), and to the appendices (line 237). The status box says
  "not reviewed by a human specialist". No front-matter text says anything was human-reviewed.
- **Lean in the abstract.** Class three, four and five plus a conditional general class agrees with
  the body prose (lines 1296-1297) and with formal/README.md lines 13-19.
- **README section numbers.** Proposition 2.3, Section 5, 6.2, 7.1, 7.2 and Section 8 all match the
  current numbering.

---

## 6. Body-side notes (outside scope, not counted)

- **N1.** thm:bb-envelope (main.tex line 1034) states the total time with no proviso. The appendix
  (appendix-torsion-blackbox.tex lines 1307-1308) adds "provided the degree of the normal-form
  arithmetic is at most $\tau_c$". The main statement should carry the same proviso.
- **N2.** The Lean table row `ReesGeneralMeasuredReceiver` (line 1286) says "unconditional at
  $c=4$". The prose (line 1297) and formal/README.md line 17 say the same now holds at c = 5. The
  row may be stale.
- **N3.** thm:bb-envelope(iii) (line 1031) says Ivanyos-Santha "states its solver's time only as
  polynomial". That is true of the paper, but rem:is-runtime now bounds the Schedule-1 solver
  explicitly. β̂_c could be bounded at Ivanyos-Santha grades (Schedule-2 grades remain
  non-explicit). A pointer to rem:is-runtime would help.
- **N4.** T_S is used with ">" at lines 299 and 610 and with "≥" in prop:decoupled-sde (line 632).

## Applied (11-04)

Applied by an AI integration pass on 4 November 2026 to `main.tex` and `README.md` (local only; no git). Build: 143 pages, 0 Overfull, no "Float too large", no undefined references; `tests/tools/test_rees_paper_numbers.py` passes. AI-checked, pending human review. No claim gate changed.

Counts: **17 applied, 6 modified, 0 skipped**; body notes: N1, N3, N4 applied, N2 modified.

* **E1: modified.** One fix covers this and referee 6 E3. The row reads "for p > c: … queries, … gates; plus the cost of [20, Thm. 1] for p ≤ c". The caption uses this report's wording ("added separately and … not included in the stated bounds"). The regimes table is now `\footnotesize` so that it fits the page.
* **E2: modified.** The README paragraph is replaced as proposed, but says 143 pages (final build) and rows I137–I181. It also mentions the normal-form proviso of the total time and the referee 6/7 text fixes.
* **G1: modified.** A short Contributions paragraph (8 source lines, five items) sits before Organization. Every item carries its conditions. The coherent receiver is marked as existence only, not implemented, and the circuits as checked only on fixed small instances. The header says AI-checked, pending human review, priority not assessed, no speedup claimed.
* **G2: applied.** The sentence was added to the paragraph after thm:main, and the Organization line was updated.
* **G3: applied.**
* **G4: modified.** The cell text was shortened to fit the float: "any of the above (extending Thm. 4.14, stated for oracle input, is argued, not proved)".
* **G6: modified.** All proposed rows were added, with two changes. In the D_d row, the undefined "dim A^{(d)}" became "dim G_d". The M_d^tri row was kept for parallel with M_d^sym, although the symbol occurs only in prop:triangular-sde.
* **I1: applied.**
* **I2: applied.** The row now separates "e_d(p):" with a label.
* **I3: applied.**
* **I4: applied.** Checked against the Lean prose in sec:formalization.
* **I5: applied.** Checked against prop:classical-query (m ≥ 2, δ < 1/2, (ii) needs L non-abelian).
* **I6: applied.**
* **I7: applied.**
* **I8: modified.** The sentence was shortened to fit the float: "Its total time, stated in Theorem 7.2 separately for c ≥ 3, 2, 1, involves an uncomputed solver exponent."
* **I9: applied.** The body's counts (148 and 15 macros) were checked against sec:formalization.
* **S1: applied.** The duplicate sentence was replaced by the G2 sentence.
* **S2–S6: applied.**
* **N1: applied** through referee 6 G1 (the proviso is now in thm:bb-envelope).
* **N2: modified.** The row was not stale: the c = 5 specialization is in `ReesGeneralLawClassFive` (`classFive_measured_terminal_source`), which has its own row. The row now reads "unconditional at c=4 (at c=5 via ReesGeneralLawClassFive)".
* **N3: applied.** thm:bb-envelope(iii) points to rem:is-runtime and says that β̂_c is not computed here.
* **N4: applied.** prop:decoupled-sde now says "p > T_S(κ)", matching the table and Appendix A. T_S is a minimum over primes, so the old "≥" was also true; the change only harmonizes the notation.

# Rees paper, referee 10: parameterized regimes and Appendices B, C and F (AI referee, 2026-11-04)

AI-only referee pass, not a human review. No `.tex` file was edited. No git or
network actions were taken. All claim gates stay false.

## Scope and method

Files read in full: `docs/papers/rees-hsp/appendix-schedule3.tex` (Appendix B,
including `lem:s3-law` and `prop:mixed-schedule`), `appendix-free-coordinate.tex`
(Appendix C, including `lem:fc-zero-sum` and `app:fc-split`) and
`appendix-codimension.tex` (Appendix F). In `main.tex` I read Section
`sec:parameterized` (lines 946-1017). I also read the Schedule 3 material, which
sits in Section `sec:sde` rather than in "Parameterized Regimes": `thm:random-column`
(689-698), `thm:free-coordinate` (703-717), `prop:rc-lower` (719-725) and
`rem:combined-schedule` (683). I also read `tab:fcs-budget` (924-941), the abstract
(97-103), the related-work and Contributions paragraphs (126, 227-234) and
`tab:main-regimes` (203-221). I checked definitions against `thm:main`,
`sec:recursion` and `sec:sde`, and I grepped integration rows I87-I151, mainly I145,
I147, I149 and I151.

I re-derived every displayed inequality and probability split in scope by hand.
Independent scripts (they import nothing from the repo; exact `Fraction` arithmetic)
are in the session scratchpad
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/`:
`regimes_check.py`, `misc_check.py`, `types_check.py` and `partii_check.py`. They reproduce:

- all 32 entries of `tab:fcs-budget`. That covers the combined Q, the uniform-kernel Q
  and trials (computed from the statement of `prop:mixed-schedule`), and the (iii) Q,
  per-node cap and total (least public arities under (R1)). They also reproduce the
  caption's claims about where each row uses Schedule 2, and the mixed-rule bank sum
  of at most 2^{-67} with a tree abort between 2^{-6.91} and 2^{-6.38};
- the filiform zero-sum numbers 13.2, 24.3 and 42.3 against 58.9, 155.8 and 676.8
  (computed at eps = 1/3; see finding I6);
- `app:fc-numbers`: the cap 2^{33.78} at p = 5281, d = 4, B = 40; the explicit choice
  adding 1-2 columns and 0.24-1.31 to log2 Q; the part (ii) caps (at most 2^{34.28},
  with 2^{34.27} at 5281) and the bank sum 2^{-234.9}; and the trial counts
  2^{193.9}-2^{236.0} for `thm:random-column`(ii) at u = 18 (B = 56);
- the block-splitting counterexample probability 69/325;
- for the algebra g_6 of Appendix F: Jacobi over Z, lower central ranks 6,4,3,2,1,0,
  and C(I) = I;
- the inequality x^r <= max(r^{2r}, 2^{16}, 2^x) used in the proof of `cor:fpt-r`(i)
  (grid scan, no violation; a hand proof is in finding I5).

The following were re-derived by hand and found correct:
- `lem:s3-moment`, `lem:s3-mu`, `lem:s3-root`, `lem:s3-node`, `lem:s3-tree` (including
  2^{-17} + 2^{-38}), the restart binomial, `eq:s3-ninstr` and `prop:s3-uniform`;
- `lem:fc-rref`, `lem:fc-moment`, `lem:fc-node`, `lem:fc-params` (1/12656.25 + 1/16384),
  `lem:fc-choice` and `lem:fc-forest`. The split of `thm:free-coordinate`(iii) is
  2eps/9 + eps/3 + eps/3 = 8eps/9;
- `lem:fc-zero-sum` (pairwise independence of 0/1 vectors, Chevalley-Warning, the
  reachable-sums search);
- `lem:fc-split-law`, `prop:fc-split-node`, `prop:fc-split` and `rem:fc-tradeoff`(b);
- `prop:rc-lower` (the generic event has probability at most 1/(p-1); the mean
  acceptance is (q^n - p^{-n})q^a; the oblivious union bound is Tq^a);
- `prop:mixed-schedule` (abort at most 1/64 + 1/64, then 32^{-3m'});
- the proofs of `cor:fpt-r`(i) and (ii): alpha, 2^alpha >= 16(216cS)^3c^2, the induction
  log2 n_d <= (d-2)log2(4 alpha c), M_c = g_c c + 1 <= 4 alpha c, Hoeffding with
  R = ceil(18 ln(1/eps)), and |G'| = p^r <= (r+2)^r;
- `cor:codim` and the whole of Appendix F: the self-centralizing ideal, dim <= b(b+1)/2,
  class <= 2b-1, the normalizer and transport, the error budget eps/4 + eps/4 + eps/2,
  the birthday learner's B, t and a, and the FC(iii) branch with the guard r <= k.

## Verdict

No error was found: no false statement, no wrong constant, no probability slip and no
budget that fails to sum. The `tab:fcs-budget` numbers and the zero-sum figures
reproduce exactly. Two small gaps and several imprecisions remain. They are mostly
about claim discipline: hypotheses that are derived but read as assumed, missing
"conditional" or "AI-checked" labels, and one "no conditional step" wording.

Counts: **Error 0, Gap 2, Imprecision 10, Style 6.**

---

## Gaps

### G1. `prop:fc-uniform`(b): the poly(g_d) factor is not absorbed (appendix-free-coordinate.tex, line 285 and proof line 296)

Quote (statement): "its classical time is at most
$Q\cdot\Bigl(2 + 2B\ln 2\cdot\max_{d\in\Gamma_{\mathrm F}}\kappa_d^{\,g_d}\Bigr)\cdot\poly\bigl(\max_dM_d, B, c, \log p\bigr) + Q\cdot t_{\mathrm{S1}}$".

Reason. The per-node costs in the proof are $(1+T_r)\poly(g_d,M_d,B,\kappa_d,\log p)$ and
$\poly(g_d,M_d,\log p)$. The display drops $g_d$. That needs $M_d > g_d$ at every grade.
The proof of `prop:fc-split`(ii) gives this argument (line 464), but the proof of
`prop:fc-uniform`(b) does not. `cor:fpt-r`(i) relies on (b) with $c$ not fixed, so the
absolute exponent matters. The claim is true: at an FCS grade, $\beta \le \tau_d < 1$
forces $n_0 \ge 2$ and $L \ge g_d - 1$.

Fix: append to the proof of (b), after "a linear node costs $\poly(g_d, M_d, \log p)$;":

```latex
these factors are $\poly(M_d,\dots)$ because $M_d > g_d$ at every grade: at a linear grade $M_d = g_d+1$; at a grade of $\Gamma_0$, $B_d(g_d) > g_d$ and $g_d(p-1)+1 > g_d$; and at an FCS grade $\beta(M_d,n_0^{(d)};g_d) \le \tau_d < 1$ forces $n_0^{(d)} \ge 2$ (the first term of~\eqref{eq:fc-beta} is at least $4$ when $n_0^{(d)} = 1$) and $M_d - n_0^{(d)} \ge g_d - 1$ (through its second term), so $M_d \ge g_d + 1$;
```

### G2. `rem:fc-tradeoff`(a): the failure bound and the label count leave out the span pre-step (appendix-free-coordinate.tex, line 473)

Quote: "With $K(2a-K+3)/2 + g' + n_0$ labels, a nonzero solution is found except with
probability at most $\beta(g'+n_0, n_0; g') + 5\cdot 2^{-B}$".

Reason. The parenthetical earlier in the same item says that in the recursion $a$ is
unknown. There, the intrinsic coordinates come from the span of the first
$g_d+\lceil\log_p(2/\tau)\rceil$ labels, "except with probability at most $\tau/2$, ... at
the cost of those labels". Neither that failure term nor those labels appear in the
stated count and bound. As written, the bound holds only when the label subspace is
given.

Fix: replace the quoted sentence with

```latex
With $K(2a-K+3)/2 + g' + n_0$ labels in intrinsic coordinates (plus $g_d+\lceil\log_p(2/\tau)\rceil$ labels for the span when $a$ is unknown), a nonzero solution is found except with probability at most $\beta(g'+n_0, n_0; g') + 5\cdot 2^{-B}$ (plus $\tau/2$ when the span is computed)
```

---

## Imprecisions

### I1. `thm:free-coordinate`: the preamble reads as an assumption for all three parts (main.tex, line 705)

Quote: "Assume the labels at a stage-$d$ node of the free-coordinate sampler are
independent and uniform on a subspace of dimension $a \le g_d$, and $\kappa_d < p-1$ at
every such node (part~(iii) uses other nodes at the remaining grades)."

Reason. The proof of (i) (appendix-free-coordinate.tex, line 151) says the preamble
concerns the sampler nodes, and that in (ii) and (iii) the law is derived (by
`lem:fc-forest`(a), via `lem:s3-law`), not assumed. A reader of the statement alone sees
the label law as a hypothesis on the instance. That contradicts the status paragraph of
Appendix C, and it hides the actual restriction: the guarantee holds for the i.i.d.
supply of fresh ideal sources only.

Fix: replace the preamble with

```latex
In part~(i), assume that the labels at a stage-$d$ node of the free-coordinate sampler are independent and uniform on a subspace of dimension $a \le g_d$, and that $\kappa_d < p-1$ there. In parts~(ii) and~(iii) this law is not assumed: for fresh ideal sources it is derived at every sampler node (Lemmas~\ref{lem:s3-law} and~\ref{lem:fc-forest}(a)), and the guarantees hold for that i.i.d.\ supply only. Sampler nodes require $\kappa_d < p-1$; part~(iii) uses other nodes at the remaining grades.
```

### I2. `thm:random-column` and `thm:free-coordinate` are not labelled conditional (main.tex, lines 689 and 703)

Quote: "[Random-column schedule; AI-checked, pending human review; ...]" and
"[Free-coordinate random-column schedule; AI-checked, pending human review; ...]".

Reason. Both proofs use the steps behind `thm:main`: `lem:homogeneous`, `lem:central`,
`prop:descent`, `lem:hybrid` and `thm:uniform-compilation`. These are AI-checked only.
At a grade with $\kappa_d = p-1$, part (iii) also uses `thm:is-import`. `prop:mixed-schedule`
and the paragraph after `thm:free-coordinate` say this, but the two titles do not.
`tab:main-regimes` calls these rows "conditional corollaries".

Fix: change the two titles to

```latex
\begin{theorem}[Random-column schedule; conditional on the steps behind Theorem~\ref{thm:main}; AI-checked, pending human review; proof in Appendix~\ref{app:schedule3}, which derives the label law (Lemma~\ref{lem:s3-law})]
```

```latex
\begin{theorem}[Free-coordinate random-column schedule; conditional on the steps behind Theorem~\ref{thm:main}; AI-checked, pending human review; proof in Appendix~\ref{app:free-coordinate}; the label law is derived in Appendix~\ref{app:schedule3} (Lemma~\ref{lem:s3-law})]
```

### I3. `thm:app-codim`(iii): "with no conditional step" (appendix-codimension.tex, line 48)

Quote: "For $k \le 1$ the reduction ... alone solves the problem for every $p > c$, using
only abelian Fourier sampling, in time $\poly(m,\log p,w,\log(1/\eps))$ with no
conditional step."

Reason. The k <= 1 route avoids the Rees step and `thm:is-import`. It still uses
`lem:hybrid` and the QFT compilation of `thm:uniform-compilation`(iii) (Kitaev or
`lem:qft-mod`, then Solovay-Kitaev). The paper lists these among the AI-checked "steps
behind Theorem main" (main.tex, after the proof of `thm:main`). "No conditional step"
therefore reads as an unconditional claim. Part (iii) also has no counterpart in
`cor:codim`.

Fix (appendix-codimension.tex, line 48):

```latex
  \item For $k \le 1$ the reduction of Section~\ref{app:codim-reduction} alone solves the problem for every $p > c$, using only abelian Fourier sampling, in time $\poly(m,\log p,w,\log(1/\eps))$; it uses no Rees step and not Theorem~\ref{thm:is-import}, but it does use the compilation of Theorem~\ref{thm:uniform-compilation}(iii) and Lemma~\ref{lem:hybrid}, which are AI-checked, pending human review. For $k = 2$ the reduction followed by Theorem~\ref{thm:main} at class two solves it for every $p > c$, conditional on Theorem~\ref{thm:main}.
```

Also edit the matching sentence in the Status paragraph (line 35): "Part~(iii) for $k \le 1$ uses no Rees step and no step of Theorem~\ref{thm:main} other than its compilation and Lemma~\ref{lem:hybrid}."

### I4. `cor:fpt-r` and `cor:codim`(ii): the i.i.d.-supply restriction appears only in the proofs (main.tex, lines 956-957 and 977)

Reason. Point 3 of the brief asks that Schedule 3 results be stated for the i.i.d.
ideal supply only. `cor:fpt-r` names the label law in its proof (line 964, last
sentences) but not in its statement. `cor:codim`(ii) names it in neither place; only
Appendix F does (line 315).

Fix: in `cor:fpt-r`(i), after "conditional on the steps behind Theorem~\ref{thm:main} and
on Theorem~\ref{thm:free-coordinate}(iii)", insert

```latex
(whose guarantee holds for the i.i.d.\ supply of fresh ideal sources only, Lemma~\ref{lem:s3-law})
```

In the proof of `cor:codim`(ii), after "Use Theorem~\ref{thm:free-coordinate}(iii) on it", insert

```latex
(the terminal oracle is an ordinary coherent oracle, so Lemma~\ref{lem:s3-law} gives the i.i.d.\ label law of its fresh lifted sources, and the guarantee holds for that supply only)
```

### I5. `cor:fpt-r`(i): the step to $Q_1 \le 2^{O(r\log(r+2))}S^2$ is compressed (main.tex, line 964)

Quote: "For integers $r \ge 1$ and reals $x \ge 1$, $x^r \le \max(r^{2r}, 2^{16}, 2^x)$.
Hence $Q_1 \le 2^{O(r\log(r+2))}\,S^2$."

Reason. The inequality is true. My proof: if $x \le r^2$, use $r^{2r}$. If $x \ge 16$ and
$x > r^2$, then $r\log_2 x < \sqrt{x}\log_2 x \le x$. If $r^2 < x < 16$, then $r \le 3$
and $x^r < 2^{12}$. The proof does not say how the inequality enters. The power
$(4\alpha c)^{c-1}$ of a sum must be split, and then the inequality is applied with
$x = \log_2 S$.

Fix: replace "Hence" with

```latex
Write $4\alpha c \le X + Y$ with $X = C(r+2)^2\log_2(r+2)$ and $Y = 12(r+2)\log_2 S$. Since $c-1 \le r$ and $X + Y \ge 1$, $(4\alpha c)^{c-1} \le (2X)^r + (2Y)^r$, and $(\log_2 S)^r \le \max(r^{2r}, 2^{16}, S)$ by the inequality with $x = \log_2 S \ge 1$. Hence
```

### I6. The filiform numbers do not state their parameters (main.tex, line 970)

Quote: "On the filiform profiles $r = 3, 5, 9$ at $p = c+1$ this gives $\log_2 Q = 13.2$,
$24.3$ and $42.3$, against $58.9$, $155.8$ and $676.8$ with Schedule~1".

Reason. The values depend on eps and on the arity rule. They reproduce only with
eps = 1/3, the least public FCS arities of (R1), $m = r+2$ and $g_d = r-d+2$.

Fix:

```latex
On the filiform profiles $r = 3, 5, 9$ ($m = r+2$, $c = r+1$, $g_d = r-d+2$) at $p = c+1$, with $\eps = 1/3$ and the least public arities of (R1), this gives
```

### I7. An unlabelled bound in the paragraph after `cor:fpt-r` (main.tex, line 970)

Quote: "The earlier scalar-flag bound $2^{O(r^2\log(r+2))}\cdot\poly$ of
\file{research/DERIVED\_RANK\_REES\_EXTENSION.md} needs no random-column argument."

Reason. The bound is correct. Coordinate-by-coordinate products of $(\kappa+1)$-term
scalar solutions give $\kappa$-th-power weights for every bank. But it is stated with no
status. Like everything else here, it depends on the steps behind `thm:main` and on van
de Woestijne's solver, and it has had AI checks only.

Fix: after "needs no random-column argument", insert

```latex
(conditional, like Theorem~\ref{thm:main}, on the steps behind it and on van de Woestijne's solver; AI-checked only)
```

### I8. `prop:rc-lower`: the matching claim lacks the bank-event qualifier (main.tex, line 721)

Quote: "and the free-coordinate sampler meets this within the factor $4B\ln 2$."

Reason. The proof (appendix-free-coordinate.tex, line 325) says the comparison holds only
outside the bank event $\beta(M,n_0;a)$, and it gives a generic bank on which every trial
fails. The statement should say so.

Fix:

```latex
and, outside the bank event of Theorem~\ref{thm:free-coordinate}(i) (probability at most $\beta(M,n_0;a)$), the free-coordinate sampler meets this within the factor $4B\ln 2$.
```

### I9. The zero-sum variant does not say that the budget still closes (appendix-free-coordinate.tex, line 244)

Quote: "a tree that uses it must add $S n_d\tau_d$ for each such grade to the abort bound
of Lemma~\ref{lem:fc-forest}(b)."

Reason. The reader has to check that $\varepsilon/9$ survives. It does, because
$|\Gamma_{\mathrm F}\cup\Gamma_0| \le c-1$ and each grade carries $\eps/(9(c-1))$.

Fix: append

```latex
Since $|\Gamma_{\mathrm F}\cup\Gamma_0| \le c-1$ and each such grade contributes $S n_d\tau_d = \eps/(9(c-1))$, the bound $\eps/9$ of Lemma~\ref{lem:fc-forest}(b) is unchanged.
```

### I10. The abstract omits the input restriction of the derived-dimension bound (main.tex, line 102)

Quote: "random-column and free-coordinate schedules that exploit the uniform law of the
measured labels; a bound $2^{O(r\log(r+2))}\cdot\poly$ in the derived dimension $r$,
valid for every prime $p > c$ with the class not fixed;"

Reason. `cor:fpt-r` proves the bound for oracle input. For coset copies it is "argued, not
proved", and it rests on the i.i.d. law of fresh ideal sources. `tab:main-regimes` and the
corollary say this; the abstract does not.

Fix:

```latex
random-column and free-coordinate schedules that exploit the i.i.d.\ uniform law of the labels of fresh ideal sources; a bound $2^{O(r\log(r+2))}\cdot\poly$ in the derived dimension $r$, valid for every prime $p > c$ with the class not fixed (proved for oracle input, argued for coset copies);
```

---

## Style

- **S1** (main.tex, line 972). `cor:codim` is the only result in the section without the
  label. Use `\begin{corollary}[Hidden codimension; conditional; AI-checked, pending human review]`.
- **S2** (main.tex, line 719). "AI-checked only" differs from the house label. Use
  `[Rejection cost; AI-checked, pending human review; proof in Appendix~\ref{app:free-coordinate}]`.
  Also, the proof shows the generic event fails with probability at most $1/(p-1)$, so
  "$1/(p-1) + 2p^{a-M}$" in the statement can become "$1/(p-1)$".
- **S3** (main.tex, line 989, `rem:codim`). "Each grade then needs arity at least two
  except with probability $1/p$" is garbled. Replace it with
  `A node of arity one succeeds only when its label is zero, which has probability $1/p$, so every grade needs arity at least two,`.
- **S4** (main.tex, line 985). "checked by an AI session only
  (...2026-11-02-rees-codimension.md)" predates the FC(iii) route (I145, I147). Use
  `checked by AI sessions only (\file{research/audits/reviews/2026-11-02-rees-codimension.md}; the free-coordinate route of part~(ii) in \file{research/audits/reviews/2026-11-04-rees-fcs-budget.md} and \file{research/audits/reviews/2026-11-04-rees-check-new-text.md})`.
- **S5** (main.tex, line 717). The paragraph after `thm:free-coordinate` says a grade with
  $\kappa_d = p-1$ "uses Schedule~1 at degree $d$". Since I151 it may use the zero-sum node
  instead. Use `uses Schedule~1 at degree $d$ or the zero-sum node of Lemma~\ref{lem:fc-zero-sum}`.
- **S6** (source comments, not rendered). These are stale:
  - appendix-schedule3.tex, line 29: "no new keys are \cite'd. Rabin's splitting step is
    credited inline". Line 160 now has `\cite{Rabin1980}`.
  - appendix-codimension.tex, lines 17-18: "Khukhro1998 ... currently cited inline in
    main.tex without a key". main.tex now has `\cite[Chapter~10]{Khukhro1998}`.
  - appendix-free-coordinate.tex, line 393: the new record part is called $r$, which
    clashes with the rank $r$. Rename it to $\mathcal{N}$.

---

## Consistency with the rest of the paper (brief, point 4)

- `tab:main-regimes` agrees with the section: the derived-dimension row (all p > c,
  FC(iii) with the zero-sum node at p = c+1, IMS as the oracle alternative), the
  hidden-codimension row (p >= 2k+1 against p <= 2k), the free-coordinate row
  ($\log(1/\tau_d)$, I94) and the random-column row.
- The Contributions paragraph (item 4) and the abstract present the bounds as conditional
  and AI-checked. I10 is the only gap.
- `rem:combined-schedule`, `prop:mixed-schedule` and the `tab:fcs-budget` caption agree
  on which rows depend on `thm:power-sde`(ii): grade 8 at 2^31-1 and 2^61-1, grades 8 and
  9 at 2^127-1, none at 5281, and none in the combined column at p = 11. Recomputed.
- Line 701 ("about 2^{128}", "between 2^{223.8} and 2^{236.0} at the four primes with
  p >= 16u^2") agrees with the table and with `app:fc-numbers`.
- One structural note, not a finding: `thm:random-column`, `thm:free-coordinate`,
  `prop:rc-lower` and `tab:fcs-budget` are in Sections `sec:sde` and
  `sec:uniform-compilation`, not in "Parameterized Regimes". This brief's scope description
  differs from the paper's layout.

## Conditionality (point 3) and claim discipline (point 6)

- Every corollary in scope (`cor:fpt-r`(i) and (ii), `cor:codim`(i) and (ii)) is
  conditional through `thm:main`'s steps. "Unconditional" appears nowhere in scope. The
  only near-claim is "with no conditional step" in `thm:app-codim`(iii) (I3).
- The Schedule 3 results are stated for the i.i.d. supply in the paragraphs after
  `thm:random-column` and `thm:free-coordinate`, in `prop:mixed-schedule`, and in the
  Status and Scope paragraphs of Appendices B and C. They are missing from the statements
  of `thm:free-coordinate` (I1), `cor:fpt-r` and `cor:codim`(ii) (I4).
- AI-checked labels are present everywhere except `cor:codim` (S1). `prop:rc-lower`
  carries a variant label (S2).
- No novelty or speedup claim is made. `cor:codim` and Appendix F call the bound "a gap
  between upper bounds, not a separation", say the priority of the composite has not been
  assessed, and call the birthday learner "the standard birthday baseline".

## Citations (point 5)

- **Chevalley-Warning** (`lem:fc-zero-sum`(b)), **Hoeffding** (`cor:fpt-r`, Appendix F),
  **Chebyshev** and **Markov**: used correctly.
- **Rabin 1980**: correctly credited for gcd splitting with $(x+\delta)^{(p-1)/2}-1$.
- **Lazard 1954** (subgroup form): used as in the body.
- **IvanyosMagniezSantha2001, "Theorem 11, Section 5 (numbering of the arXiv
  version)"** (`cor:fpt-r`(ii)). I recall the result itself: for black-box groups with
  unique encoding, the HSP is solvable in time polynomial in the input size plus $|G'|$,
  for arbitrary $H$. I **cannot verify the theorem and section numbers offline**; a human
  should check them against arXiv:quant-ph/0102014. The added certification and
  amplification step is sound.
- **IvanyosSanselmeSantha2012, "Section 3 of the arXiv version"** (normalizer recursion,
  cited in `cor:codim` and in Appendix F's Comparison): plausible, but **not verifiable
  offline**.
- **Khukhro1998, Chapter 10** (body only, not in scope): not verifiable offline.

## Next step

Apply G1 and G2 and I1-I10 to the text, then rerun the build. No number in the paper
changes. The scripts above can be rerun with `/opt/anaconda3/bin/python -I` to confirm
that the table entries are unchanged.

## Applied (11-04)

Applied by an AI integrator session, locally only (no git, no network), with
Edit-tool string replacements in `docs/papers/rees-hsp/`. Check scripts of this
report are archived in `research/audits/reviews/2026-11-04-rees-referee-10-regimes/`
(`regimes_check.py`, `misc_check.py`, `types_check.py`, `partii_check.py`). No number
changed, no label was removed, and no claim gate changed. Build in a separate scratch
directory: 148 pages, 0 Overfull, no "Float too large", no undefined references;
`tests/tools/test_rees_paper_numbers.py` passes (2 passed).

- **G1** applied. The drop-in is appended to the proof of `prop:fc-uniform`(b) (the
  `M_d > g_d` argument moved into (b); the statement keeps `poly(max_d M_d, ...)`).
  `cor:fpt-r`(i) still follows: it uses (b) with `max_d M_d <= 4 alpha c`, and the
  absorbed `g_d` factor leaves the exponent absolute.
- **G2** applied as proposed (`rem:fc-tradeoff`(a)).
- **I1** applied as proposed (preamble of `thm:free-coordinate`). Also changed, for
  consistency, "The hypothesis of the theorem" to "The hypothesis of part~(i)" in the
  proof of part (i) in Appendix C.
- **I2** applied, in the paper's "conditional on X; AI-checked, pending human review"
  title convention, keeping the AI-checked label. Modified: the `thm:random-column`
  title also says "(Schedule~3)", because the drop-in title gave a 7pt Overfull box.
- **I3** modified. `thm:app-codim`(iii) now says the k <= 1 route uses no Rees step and
  not `thm:is-import`, "but it is conditional on" the compilation of
  `thm:uniform-compilation`(iii) and on `lem:hybrid` (AI-checked, pending human review).
  "conditional" replaces the drop-in's "it does use", so the part is clearly not
  unconditional. The Status paragraph was edited to match ("so it too is conditional on
  those AI-checked steps"). The report names no drop-in counterpart for `cor:codim`, so
  none was added.
- **I4** applied as proposed, in both places (`cor:fpt-r`(i) statement and the proof of
  `cor:codim`(ii)).
- **I5** applied as proposed (proof of `cor:fpt-r`(i)).
- **I6** modified: drop-in applied, with "(R1) in Appendix~\ref{app:free-coordinate}"
  because (R1) is not defined in the body.
- **I7** applied as proposed.
- **I8** applied as proposed.
- **I9** modified: drop-in applied, with "(with tau_d = eps/(9(c-1)Sn_d) at the zero-sum
  grade, as at the FCS grades)" added, because tau_d is defined only at FCS grades.
- **I10** applied as proposed (abstract).
- **S1** applied (`cor:codim` title). Modified: its first sentence now opens "Let $k$ be
  given with $\codim_{\Fp}\hh \le k$", because the longer title gave a 20pt Overfull box.
- **S2** applied: house label, and the bound is now $1/(p-1)$. In Appendix C, "which is
  within the stated bound" became "which is the stated bound".
- **S3** applied, with "and a direct descent" so that the sentence does not repeat "so".
- **S4** applied as proposed.
- **S5** applied as proposed.
- **S6** applied. The Rabin comment in appendix-schedule3.tex and the Khukhro comment in
  appendix-codimension.tex now say that the keys are cited. The record part in Appendix
  C is renamed from $r$ to $\mathcal{N}$; this one is rendered text, not a comment.
- **Citations** (integrator decision): the numbers are unchanged. Source comments
  `% NEEDS HUMAN VERIFICATION` were added at IMS "Theorem~11, Section~5" (proof of
  `cor:fpt-r`(ii)), at "IMS Theorem~11" in `tab:main-regimes`, and at ISS "Section~3 of
  the arXiv version" in main.tex (`sec:ring`, quotient-oracle paragraph) and in
  appendix-torsion-blackbox.tex. That last file is outside the four listed; it was backed
  up first, and the edit is one comment line.

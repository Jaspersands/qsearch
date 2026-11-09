# Referee 15 (Fable, unanchored): text added or changed by rows I207–I221

Date: 2026-11-05. Scope: only the text that rows I207–I221 of
`research/audits/reviews/2026-11-02-rees-integration-log.md` added or changed in
`docs/papers/rees-hsp/main.tex`, `appendix-schedule2.tex`,
`appendix-free-coordinate.tex` and `core/main-core.tex`. The Gate-level control
paragraph was skipped as instructed. No repo file other than this report was
edited. No git, no network.

Method. Every displayed inequality and count in the scoped text was re-derived
by hand where feasible (listed in Section 3), and the numerical claims were
recomputed with independent code in `$TMPDIR/.../scratchpad/check.py`,
`check2.py`, `cyclo.py` (mpmath, 40 digits; sympy). The source reports were
read only as sources. Scratch copies of the current `.tex` files were built:
`main.tex` exit 0, 175 pages, 0 Overfull, no undefined references or
citations; `core/main-core.tex` exit 0, 28 pages, 0 Overfull, no undefined
references or citations. (A first build from a copy taken while another
session was writing the files showed one Overfull box in an older proof of
`prop:app-s2-cyclotomic`(iii); it is not in the current text.)

Counts: 0 Error, 2 Gap, 7 Imprecision, 3 Style.

## 1. Top three

### G1 (Gap) main.tex:767 — polynomial time needs a choice at the grade $\kappa_d = p-1$

Current text (sentence after Theorem `thm:free-coordinate`, line 767):

> If the free-coordinate nodes are replaced by the weight-doubling nodes of Remark~\ref{rem:fc-witness-h3}, which read the bank (AI-checked, pending human review; not adopted in (R1)), then for fixed $c$ and every prime $p > c$ the classical time of part~(iii) is polynomial in $m$, $\log p$ and $\log(1/\eps)$, with the same supply, conditions and error bound as part~(iii) and at a larger query count: up to factors polylogarithmic in $m$, $p$ and $1/\eps$, its exponent of $m$ is at most $19$ at $c = 9$ (Remark~\ref{rem:fc-witness-h3}(c)).

Why. Part (iii) lets a grade with $\kappa_d = p-1$ use either Schedule 1 at
degree $d$ or the zero-sum node of Lemma `lem:fc-zero-sum`, whose search costs
up to $p^{g_d}$ steps. Replacing only the free-coordinate nodes leaves that
choice open, so the sentence is not justified for the zero-sum option.
Remark `rem:fc-witness-h3`(c), which the sentence cites, uses the node of
Remark `rem:fc-zero-sum-arity`(b) at $\Gamma_0$, and its exponents $E(c)$ are
computed with that node ($E = 3, 6, 8, 10, 13, 14, 16, 19$ reproduced here by
independent code; at $c = 9$ the grade $\Gamma_0$ is empty, so the value $19$
does not depend on this choice, but the sentence's time claim does).

Replacement (line 767, the one sentence):

```latex
If the free-coordinate nodes are replaced by the weight-doubling nodes of Remark~\ref{rem:fc-witness-h3}, which read the bank, and a grade with $\kappa_d = p-1$ uses the node of Remark~\ref{rem:fc-zero-sum-arity}(b) or Schedule~1 rather than the zero-sum node (AI-checked, pending human review; not adopted in (R1)), then for fixed $c$ and every prime $p > c$ the classical time of part~(iii) is polynomial in $m$, $\log p$ and $\log(1/\eps)$, with the same supply, conditions and error bound as part~(iii) and at a larger query count: up to factors polylogarithmic in $m$, $p$ and $1/\eps$, its exponent of $m$ is at most $19$ at $c = 9$ (Remark~\ref{rem:fc-witness-h3}(c), whose exponents use the node of Remark~\ref{rem:fc-zero-sum-arity}(b) at $\kappa_d = p-1$).
```

### I1 (Imprecision) main.tex:91–99 — the version note omits most of the 5 November additions

Current text (lines 91–99):

> The version of 5 November 2026 adds the class-six and class-seven Lean modules and two Lean modules on the SDE step (\file{research/audits/reviews/2026-11-05-rees-lean-c6.md} and \file{research/audits/reviews/2026-11-05-rees-lean-c7.md}; machine-checked in Lean; AI-run, pending human review), merges the two Schedule~3 theorems into Theorem~\ref{thm:free-coordinate}, and adds Remarks~\ref{rem:fc-zero-sum-sis}, \ref{rem:sde-subquadratic} and~\ref{rem:sde-block-steered}, Appendix~\ref{app:s2-tower}, the restart variant in Remark~\ref{rem:is-runtime} and the exact instrument exponents, all from AI-only reports of 4--5 November; these are not a human review either.

Why. Rows I218–I221 added `ReesSdeSolver` and `ReesMergeReduction` (two more
Lean modules, 29 guards), Appendices `app:s2-chains` and `app:s2-local`,
Remarks `rem:app-s2-joint-moments`, `rem:sde-worst-case`,
`rem:fc-zero-sum-arity` and `rem:fc-witness-h3`, the composite-$\kappa$ run
count in `rem:is-runtime`, and the application-4 paragraph (Theorem W), none
of which the note lists. A reader using the note to find what changed, and
what is AI-only, misses them.

Replacement (lines 91–99):

```latex
The version of 5 November 2026 adds the class-six and class-seven Lean modules,
two Lean modules on the SDE step and the Lean solver and merge-identity modules
(\file{research/audits/reviews/2026-11-05-rees-lean-c6.md},
\file{research/audits/reviews/2026-11-05-rees-lean-c7.md} and
\file{research/audits/reviews/2026-11-05-rees-lean-sde-solver.md}; machine-checked in
Lean; AI-run, pending human review), merges the two
Schedule~3 theorems into Theorem~\ref{thm:free-coordinate}, and adds
Remarks~\ref{rem:fc-zero-sum-sis}, \ref{rem:fc-zero-sum-arity}, \ref{rem:fc-witness-h3},
\ref{rem:sde-subquadratic}, \ref{rem:sde-block-steered} and~\ref{rem:sde-worst-case},
Appendices~\ref{app:s2-tower}, \ref{app:s2-chains} and~\ref{app:s2-local},
Remark~\ref{rem:app-s2-joint-moments}, the restart variants and run counts in
Remark~\ref{rem:is-runtime}, the exact instrument exponents and the fourth
application search after Remark~\ref{rem:filters}, all
from AI-only reports of 4--5 November; these are not a human review either.
```

### G2 (Gap) appendix-schedule2.tex:427, 431 — the barrier step is asserted without its source

Current text (line 427, opening sentence):

> ... (\file{research/audits/reviews/2026-11-05-rees-threshold-9.md}, Lemma~2, Theorem~1 and Corollary~3; re-derived in \file{research/audits/reviews/2026-11-05-rees-threshold-9-check.md}).

and (line 431):

> The law of Benjamini, Gurel-Gurevich and Peled cited in Remark~\ref{rem:two-level-threshold-size}, which agrees on every $\kappa-1$ columns with independent copies of the law of $n_0$, therefore satisfies all of these brackets (products of the one-column brackets lie inside the brackets for $S$), and it gives probability $0$ to every column being nonempty.

Why. The parenthesis is the whole barrier argument and is not immediate: the
independent-copies law gives $\mathbb{E}\binom{M_S}{m} = \sum \prod_j
\mathbb{E}\binom{n_0}{m_j}$, and the product of one-column brackets has
$\prod_j \rho_{m_j} = \kappa^{-m}\prod_j(1 - m_j/p)$, which exceeds
$\rho_m = \kappa^{-m}(1 - m/p)$; the report (Remark 5, step 4) absorbs the
excess into a $(1 + 0.4\eta_m)$ slack and the integration check re-derived
that step. The paper's citation list names Lemma 2, Theorem 1 and
Corollary 3 only, so the barrier has no stated source, and "therefore" reads
as if it followed from the displayed brackets alone.

Replacement (line 427, inside the parenthesis):

```latex
(\file{research/audits/reviews/2026-11-05-rees-threshold-9.md}, Lemma~2, Theorem~1, Corollary~3 and Remark~5; re-derived in \file{research/audits/reviews/2026-11-05-rees-threshold-9-check.md})
```

Replacement (line 431, the one sentence):

```latex
The law of Benjamini, Gurel-Gurevich and Peled cited in Remark~\ref{rem:two-level-threshold-size}, which agrees on every $\kappa-1$ columns with independent copies of the law of $n_0$, satisfies all of these brackets (Remark~5 of the first cited report shows that the products of the one-column brackets lie inside the brackets for $S$, after a change of $\eta_m$ by a constant factor; re-derived in the second), and it gives probability $0$ to every column being nonempty.
```

## 2. Other findings

### I2 (Imprecision) core/main-core.tex:673 — chains do lower the arity at small $a$

Current text (line 673):

> ... and by chains of two refinements at arity $\binom{a+3}{3}$ for every $\kappa \ge 4$; neither lowers the Schedule~2 arity or changes the exponent $143$ below (AI-checked, pending human review).

Why. $\binom{a+3}{3} < (a+1)((\kappa-1)a+1)$ for small $a$ (at $a = 1$:
$4 < 2\kappa$ for $\kappa \ge 3$; at $a = 2$: $10 < 3(2\kappa-1)$ for $\kappa \ge 2$).
The companion says "for large $a$" (`app:s2-chains` status line and
`rem:two-level-threshold-size`); the core drops the qualifier.

Replacement:

```latex
and by chains of two refinements at arity $\binom{a+3}{3}$ for every $\kappa \ge 4$; for large $a$ neither lowers the Schedule~2 arity, and neither changes the exponent $143$ below (AI-checked, pending human review).
```

### I3 (Imprecision) core/main-core.tex:685 — Theorem W pointer omits the known weight bound

Current text (line 685):

> ... classically recovers its symmetry group in $\exp(\mathcal{L})$, for $\mathcal{L}$ strictly upper triangular of size $D \le p$, whenever $p > \max(\nu-1,2)\,\delta$, where $\nu$ is the nilpotency index of $\mathcal{L}$ and $\delta$ is the largest total base-$p$ digit sum of an exponent vector of the polynomial (proved; AI-checked, pending human review; possibly known).

Why. The algorithm of the companion (main.tex:1225) takes a bound
$\hat\delta \ge \delta(F)$ as input and evaluates $F$ over an extension with
$p^K > \deg F$; without a known bound the hypothesis cannot be checked, and
the companion says so ("Suppose that a bound $\hat\delta \ge \delta(F)$ is
known"; the promise is dropped only for polynomially bounded $p$).

Replacement:

```latex
classically recovers its symmetry group in $\exp(\mathcal{L})$, for $\mathcal{L}$ strictly upper triangular of size $D \le p$, given a bound $\hat\delta$ on the largest total base-$p$ digit sum $\delta$ of an exponent vector of the polynomial with $p > \max(\nu-1,2)\,\hat\delta$, where $\nu$ is the nilpotency index of $\mathcal{L}$; for polynomially bounded $p$ no bound need be supplied (proved; AI-checked, pending human review; possibly known).
```

### I4 (Imprecision) main.tex:1225 — "nilpotency index of $\mathcal{L}$ on the variables" is not defined

Current text:

> let $\nu \le D$ be the nilpotency index of $\mathcal{L}$ on the variables,

Why. The proof uses $\deg_t \exp(tA) \le \nu - 1$ for every $A \in
\mathcal{L}$, so $\nu$ must bound the nilpotency index of each element (or
of the associative algebra generated by $\mathcal{L}$). "On the variables" does
not say which, and the check report's own statement uses $\nu \le p$ as a
hypothesis.

Replacement:

```latex
let $\nu \le D$ be the least integer with $A^{\nu} = 0$ for every $A \in \mathcal{L}$ (the nilpotency index of $\mathcal{L}$ acting on $\Fp^D$),
```

### I5 (Imprecision) main.tex:675 — "every divisor $D$ of $\kappa$" includes $D = 1$

Current text (in `rem:two-level-threshold-size`):

> and $E_2(D) \subseteq E_2(\kappa)$ on primes $p \equiv 1 \pmod\kappa$ for every divisor $D$ of $\kappa$ (Appendix~\ref{app:s2-local}; proved, AI-checked, pending human review);

Why. $E_2(1)$ is not defined ($\kappa = 1$ has no contraction problem), and
Lemma `lem:app-s2-divisor` assumes $D \ge 2$.

Replacement:

```latex
and $E_2(D) \subseteq E_2(\kappa)$ on primes $p \equiv 1 \pmod\kappa$ for every divisor $D \ge 2$ of $\kappa$ (Appendix~\ref{app:s2-local}; proved, AI-checked, pending human review);
```

### I6 (Imprecision) core/main-core.tex:673 — the conditional threshold is now $O(\kappa^\kappa)$

Current text:

> that the existence threshold is at most $\kappa^{\kappa+o(1)}$ (argued in a report, not proved in the full version),

Why. The companion now states, conditionally on the same cited bound, the
threshold $6\kappa^\kappa+1$ for $\kappa \ge 729$ (`rem:two-level-threshold-size`,
`rem:app-s2-joint-moments`) and a barrier at $\kappa^\kappa/2$ for the method.
The core statement is still true but no longer reflects the companion.

Replacement:

```latex
that the existence threshold is at most $6\kappa^\kappa + 1$ for $\kappa \ge 729$, hence $O(\kappa^\kappa)$ (conditional on a central-moment bound argued in a report and not proved in the full version; no certificate of that kind reaches below $\kappa^\kappa/2$),
```

### I7 (Imprecision) main.tex:675 — "those moments" is wider than the appendix statement

Current text:

> an $O(\kappa^\kappa)$ threshold that no certificate built only from those moments can push below $\kappa^\kappa/2$ (Remark~\ref{rem:app-s2-joint-moments}; AI-checked, pending human review).

Why. The appendix barrier is for lower bounds valid for every law of the
column counts that satisfies the brackets for sets of at most $\kappa-1$
columns; a certificate using the joint law of all $\kappa$ columns is not
excluded (the report says so explicitly).

Replacement:

```latex
an $O(\kappa^\kappa)$ threshold that no certificate built only from such moments of at most $\kappa-1$ columns can push below $\kappa^\kappa/2$ (Remark~\ref{rem:app-s2-joint-moments}; AI-checked, pending human review).
```

### S1 (Style) main.tex:675 — missing space after a period

Current text:

> (Remark~\ref{rem:app-s2-joint-moments}; AI-checked, pending human review).For the small $\kappa$ of this paper,

Replacement:

```latex
(Remark~\ref{rem:app-s2-joint-moments}; AI-checked, pending human review). For the small $\kappa$ of this paper,
```

### S2 (Style) main.tex:632 — $\rho$ for the run count

Current text (in `rem:is-runtime`):

> For every $\kappa_d \ge 2$ the variant makes at most $\rho = \nu - \min_{q \mid \kappa_d} v_q\bigl((p-1)/\kappa_d\bigr)$ runs,

and line 628: "the bounds $\nu+1$, $e$ and $\rho$ (below)".

Why. $\rho$ denotes states ($\rho_H$, $\rho_\lambda$) throughout the paper and
$\rho_{\mathrm{pr}}$ a pair count in `rem:sde-worst-case`. A local letter
avoids the clash.

Replacement: write `$r_{\mathrm{run}}$` for `$\rho$` at both places in the
remark, that is

```latex
the bounds $\nu+1$, $e$ and $r_{\mathrm{run}}$ (below)
```

```latex
For every $\kappa_d \ge 2$ the variant makes at most $r_{\mathrm{run}} = \nu - \min_{q \mid \kappa_d} v_q\bigl((p-1)/\kappa_d\bigr)$ runs, with $q$ prime and $v_q$ the $q$-adic valuation; this is $e$ when $\kappa_d = q^e$, and $1 + \max_{q \mid \kappa_d} v_q(p-1) \le r_{\mathrm{run}} \le \nu$ when $\kappa_d$ has at least two distinct prime factors
```

and `$\rho$` to `$r_{\mathrm{run}}$` in the two later sentences of the same
remark ("use exactly $\rho$ runs", twice).

### S3 (Style) appendix-schedule2.tex:431 — "the report shows" for a mixed proof

Current text:

> With $\Lambda = (p-1)/\kappa^\kappa$, the report shows $F > 0$ for $6 \le \Lambda \le \sqrt{8\kappa}$ when $\kappa \ge 729$,

Why. The report proves this by explicit inequalities whose side conditions
are verified numerically for $729 \le \kappa \le 10^6$ and by an asymptotic
estimate beyond; saying so matches the appendix's practice elsewhere.

Replacement:

```latex
With $\Lambda = (p-1)/\kappa^\kappa$, the report shows $F > 0$ for $6 \le \Lambda \le \sqrt{8\kappa}$ when $\kappa \ge 729$ (explicit bounds whose side conditions are checked numerically for $\kappa \le 10^6$ and by an asymptotic estimate beyond),
```

## 3. Verified (no finding)

Re-derived by hand in the scoped text:

- `app:s2-chains`: the class and value bookkeeping in the proof of
  Theorem `thm:app-s2-chain` (classes of $\gamma c_b(\alpha_n+\beta_{i(b)})$ in
  $K$; $\tau_k \in V_k$; total value $-\tau_0$; designated weight $1$; column
  count $\sum_{j\le m}\binom{j+t}{t} = \binom{m+t+1}{t+1}$); the generator
  relabelling $i \mapsto ui$; Proposition `prop:app-s2-union-step` (i)
  (second moment, $|N_{ij}(c) - c_0^2(p-2)| \le 2c_0G + G^2\sqrt p$,
  $c_0^2(p-1)^2/p - c_0^2(p-2) = c_0^2/p$, negative sums, $j = 0$ bound) and
  (ii) (constants $0.4989$, $0.1619$, $0.0522$; $G \le 1+\ln D$;
  $H \le (1.2+\ln D)^2$); Corollary `cor:app-s2-union-chain` and its five
  comparisons at $\kappa = 16$ and $\kappa = 19$ ($27.81 < 27.97$); the tower
  arities $1331$, $2541$ against $286$ at $a = 10$; the barrier bound's first
  crossing at $a' = 146$ for $\kappa = 4$, $p = 17$, $h' = 2$.
- `app:s2-local`: Lemma `lem:app-s2-two-rows`; Proposition
  `prop:app-s2-cyclotomic` (i) (bijection $(b,c) \mapsto (-c,b-c)$, the two
  excluded $c$; $2\varepsilon \equiv 0$), (ii) (pair counts
  $(\kappa-1)(\kappa-2)$ and $\kappa^2-3\kappa+3$; agrees with $E_2(4), E_2(5), E_2(6), E_2(7)$
  at $5$; $11$; $7, 13, 19$; $29$), (iii) (the $3(\kappa-1)$ unit terms,
  $(\kappa-1)(\kappa-2)$ Weil terms, $(\kappa-1)(2\kappa-7)+2 > 0$; $p \ge 940$
  at $\kappa = 7$); Lemma `lem:app-s2-divisor`; the $r$-row void bound
  $W(\kappa,r) \le ((r-1)\kappa^r+2)^2$.
- `rem:app-s2-joint-moments`: the bracket from Lemma `lem:app-s2-weil-count`
  with $\ell = m$ over $\kappa-1$ independent rows; $\eta_{\kappa-1} \ge 1$ for
  $p \le \kappa^\kappa/2$ and $\kappa \ge 3$; the Vandermonde step; the
  comparisons $6 < \kappa-1$ and $6 < 4e\lceil\ln 4\kappa\rceil^2$ at $\kappa = 729$.
- `rem:is-runtime`: $\rho = e$ for $\kappa = q^e$;
  $1 + \max_q v_q(p-1) \le \rho \le \nu$ for at least two prime factors (via
  minimality of $v_{q^*} - e_{q^*}$ and $e_q \ge 1$).
- `rem:sde-worst-case`: $N(\kappa,1,p) \ge 2$ and the block-diagonal lower
  bound; the $\mathrm{Good}(\beta)$ reading of $N(\kappa,1,p) = 2$;
  $D_3(q) = \lfloor(q+2)^2/4\rfloor$ for $q \le 4$; the prime conditions
  $p \ge 20a$ and $p \ge 162a$.
- `rem:fc-zero-sum-arity`: $N_j(n) = 1 + \sigma_p\sum_{e<n}N_{j+1}(e)$ and the
  bound $(\sigma_p+1)^{j^*}\binom{n+j^*+1}{j^*+1}$ (hockey stick); $\sigma_3 = 3$
  and $N_0(n) = 1 + 3n(n+1)/2$; $\sigma_p \le p$; the non-total bank; the
  abort and arity accounting of (b); the degree comparisons $12$ vs $3$,
  $4$ vs $3$, $5$ vs $6$.
- `rem:fc-witness-h3`: Cauchy–Davenport depth bound; $D_0 - D_0 = \Fp$ for
  $\sqrt p > (\kappa-1)(\kappa-2)+3$ and the $1/(2\kappa)$ bound for
  $\sqrt p \ge 2(\kappa-1)(\kappa-2)+4$ (both via the $A(u,v)$ bound of
  `prop:app-s2-cyclotomic`(iii)); the lower bound
  $\log_2((p^{1/\varphi}-1)/(2c_h)) \le j^*_h$; the exact column count
  $1 + \lceil\log_2 p\rceil\frac{p}{p-1}\frac{n(n+1)}{2}$; the leading
  coefficient $\sigma_p^{j^*}/(1+j^*)!$; the error split $2\eps/9$ in (c); the
  union bound in (d).
- Theorem W paragraph: $\deg_t R_F(\exp(tA)u) \le (\nu-1)\hat\delta$; the
  Schwartz–Zippel origin of $p > 2\hat\delta$; $T = \lceil 4d + 16\ln(1/\eps)\rceil$
  samples of $1 + d\hat\delta$ evaluations give $O(d(d+\log(1/\eps))(\hat\delta+1))$;
  $\hat\delta = \lfloor(p-1)/\max(\nu-1,2)\rfloor$ is the largest admissible
  bound; Moore forms have weight $r$; $|G| \le p^{D(D-1)/2}$.
- Lean: `formal/Formal/Audit.lean` holds $538$ `#print axioms` guards; counts by
  namespace equal every row of `tab:lean-modules` (sum $500$) and the $38$
  unrelated guards ($25$ top-level, $9$ `BalancedSigned`, $4$ `CrossCheck`);
  `formal/Formal.lean` imports `BCHClassSeven`, `BCHClassSevenSubgroups`,
  `ReesGeneralLawClassSeven`, `ReesSdeSolver`, `ReesMergeReduction`;
  `BCHClassSevenSubgroups` assumes `p > 7`, that is $p \ge 11$; the per-batch
  guard counts $21$, $33$, $21$, $29$ match the table rows.

Recomputed with independent code (all agree with the text):

- $T_R(5,3) = 3780.8$, $T_R(7,3) = 30823.1$, $T_R(9,3) = 134723 < 135000$,
  $W(9,3) = 1.479\cdot10^6$; $\Theta_2(5) = 3780.8$ (binding $T_R(5,3)$; the
  union step gives $800$), $\Theta_2(7) = 30823$ (binding $T_R(7,3)$; union
  step $15133$), $\Theta_2(11) = 1.158\cdot10^6$, $\Theta_2(13) = 7.42\cdot10^6$;
  $\Theta_3(5) = 1217$, $\Theta_3(7) = 15133$;
  $\min_k\Theta^{\mathrm{cf}}_2(5,k) = 220539$ (at $k = 4$),
  $\min_k\Theta^{\mathrm{cf}}_2(7,k) = 1680700$ (at $k = 5$);
  $(\kappa-1)\kappa^\kappa = 1.25\cdot10^4$, $4.94\cdot10^6$, $2.85\cdot10^{12}$,
  $3.63\cdot10^{15}$.
- The complete sets of primes to which `prop:app-s2-cyclotomic`(i) applies,
  for $\kappa = 3,\dots,9$ up to the bound of (iii): empty; $\{5,13,29\}$;
  $\{11\}$; $\{7,13,19,31,37,43,67,73,79,139,223\}$; $\{29,43,71\}$;
  $\{17,41,73,89,97,137,233,761\}$; $\{19,37,73,109,127,163\}$. Largest
  elements $29, 11, 223, 71, 761, 163$ as stated, all below $15\kappa^2$, and
  each set contains the no-chain primes of `rem:app-s2-chains-scope`.
- $j^*_3 = 1,1,2,2$ at $p = 7,13,19,31$; $j^*_4 = 1,2$ at $p = 13,17$;
  $\max_{p>c}E = 3,6,8,10,13,14,16,19$ for $c = 2,\dots,9$, the last at $p = 19$.

Status wording checked: every scoped passage carries "AI-checked, pending human
review" or "machine-checked in Lean; AI-run, pending human review"; the
joint-moment threshold is stated conditionally ("If that bound is right") in
both files; no speedup, novelty, human review, implemented coherent receiver,
general SDE solver or checked formal compiler is claimed; the Lean paragraph
says "no formally checked compiler is claimed" and keeps $c \ge 8$, every
solver for $\kappa \ge 3$ and running times outside the boundary; Theorem W
and the chains and local-obstruction subsections disclaim priority.

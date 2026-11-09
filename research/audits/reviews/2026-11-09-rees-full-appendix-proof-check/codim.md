# Proof check `codim`: hidden-codimension bound (Appendix `app:codimension`, `cor:codim`, `rem:codim`)

Checker id: `codim`. Date: 2026-11-09. AI only (Claude Opus 5.5); no human review. Every verdict
below is AI-checked, pending human review. Finite checks can only falsify.

## Header

**Scope.**
- `T/appendix-codimension.tex`, all 328 lines: thm:app-codim, lem:app-codim-lazard, the spanning
  fact (l. 70), prop:app-codim-filiform, lem:app-codim-ideal, lem:app-codim-selfcentral,
  prop:app-codim-size and the g_6 paragraph, lem:app-codim-restrict, lem:app-codim-sample and the
  paragraph after it, lem:app-codim-normalizer, lem:app-codim-transport and the Heisenberg remark,
  lem:app-codim-unwind, (R1)-(R4), prop:app-codim-complete, lem:app-codim-ad, prop:app-codim-rc,
  prop:app-codim-birthday, the error budget, the proof of thm:app-codim (all three parts, both
  proofs of (ii)), the scope, comparison and exact-check paragraphs.
- `T/main.tex` lines 1155-1197: cor:fpt-r and its proof and the paragraph after it, cor:codim
  and its proof and the paragraph after it, rem:codim.
- Read for the cited statements only (not proof-checked): main.tex def:input-contract, thm:main,
  thm:rees-cover, lem:homogeneous, lem:central, prop:descent, sec:recursion, lem:hybrid (statement
  and proof), thm:free-coordinate, thm:uniform-compilation (statement and proof of (i));
  appendix-free-coordinate.tex (F1)-(F6), lem:fc-rref, lem:fc-node, (R1)-(R4) of app:fc-mixed,
  lem:fc-choice, lem:fc-zero-sum, lem:fc-forest, prop:fc-uniform; appendix-schedule3.tex
  lem:s3-law; appendix-provenance.tex items prov:pr-codim, prov:cd-main, prov:cd-checks.

**shasum.**
- `844ef46f6487fef0bbd4d0a95adbdd72a9f3a406  appendix-codimension.tex`
- `0ed1a1f82b13fef77fc94a48e35efc93f8d23ee4  main.tex`
- (cited statements) `ec9ab51739f4305beea3e64705f61d9b5370e9f6  appendix-free-coordinate.tex`,
  `4966e7646cc5737cf5bf1f0feda9f8a3e7875e04  appendix-schedule3.tex`,
  `2545e44aeb3ff7f97a204932c46f20ac8c77ec62  appendix-provenance.tex`

**Verdict: MINOR ONLY.** No stated result is false or unproved. One sentence is false
(finding 1, ERROR severity, no effect on any result); the rest are clarity and scope fixes.

Scripts and outputs: `O/codim/` (`liealg.py`, `check_examples.py`, `check_arith.py`,
`check_reduction.py`, `check_g6_terminal.py`, with `.out`/`.log` files). Compute used: about
6 core-minutes, including one 300 s run that timed out (an exhaustive Heisenberg enumeration at
p = 7; that run is UNKNOWN and was rerun at reduced scope).

## Findings (most severe first)

### 1. ERROR: the BCH recurrence does not divide "only by integers at most c"

Location: `appendix-codimension.tex:297`, proof of prop:app-codim-birthday, "Sampling and cost".

The text says the recurrence of thm:uniform-compilation(i) "divides only by integers at most
$c$". The recurrence also uses the coefficients $B_j/j!$ of $z/(1-e^{-z})$ for $j < c$, which
are $1, 1/2, 1/12, 0, -1/720, 0, 1/30240, \dots$ Reducing them mod $p$ divides by 12 at $c = 3$
and by 720 at $c = 5$ (`O/codim/check_arith.out`). The theorem it cites counts these and says
the right thing: "It divides only by integers whose prime factors are at most $d$"
(main.tex:806). The phrase probably comes from the theorem's proof (main.tex:815). That proof
says the coefficientwise recurrence "divides only by $k+1 \le d$" and treats the coefficients
separately (von Staudt-Clausen). Every prime factor is at most $c < p$, so the product is still
computable mod $p$ in $\poly(m,\log p)$ time, and the cost claim stands. The phrase came in with
fix P5 of the 3 Nov report. If the coefficients are read as precomputed constants, the sentence
is imprecise rather than false. I keep ERROR because it misstates the theorem it cites.

Fix: replace "and divides only by integers at most $c$," with "and divides only by integers
whose prime factors are at most $c < p$,".

### 2. MINOR: rem:codim needs $m \ge 4$

Location: `main.tex:1195`, rem:codim.

The appendix version (prop:app-codim-filiform) assumes $m \ge 4$; the remark does not. At
$m = 3$ (the Heisenberg algebra, $\hh = \Fp e_1$, $k = 2$) the last sentence is false.
- The ideal construction is not unique there: $\dim V_1/\mathcal{I}_1 = 2$, and $\mathcal{I}$ can
  be $\Span(x,e_2)$.
- Every run has $b = 2 \le k$, so the instance is already terminal and no abelian call is made.

`O/codim/check_examples.out` (rows `filiform m=3`) shows `ext=[1, 2, 0] unique=False`.

Fix: "Take, for $m \ge 4$, the filiform algebra with basis ...".

### 3. MINOR: (R2) uses lem:app-codim-sample outside the standing hypothesis $b > k$ and does not say what happens on rejection

Location: `appendix-codimension.tex:138` (standing assumption "with $b = \dim\mathcal{I} > k$")
and `:209` ((R2)).

At (R2) the lemma is applied with $\mathcal{I} = \mathcal{L}_j$ abelian, where
$\dim\mathcal{L}_j \le k_j$ can hold. The conclusions used there do not need $b > k$:
- $F$ hides $\iota^{-1}(\hh_j)$;
- each sample is uniform on $W^\perp$;
- acceptance implies $\widehat W = W$;
- rejection has probability at most $p^{r-T}$.

So nothing breaks. However, (R2) does not say "aborting on rejection". Both
prop:app-codim-complete (`:224`) and the error budget (`:307`) treat every call, including the
(R2) call, as aborting with probability $\le 2^{m-T}$.

Fix: in (R2), after "without the dimension condition", add "(the assumption $b > k$ of
Section~\ref{app:codim-learn} is used only by that condition), aborting on rejection".

### 4. MINOR: prop:app-codim-birthday omits its hypothesis $\codim\hh \le k$ and hides a $\log B$ factor

Location: `appendix-codimension.tex:281`, statement, and `:297`.

- The proposition's statement does not repeat $\codim\hh \le k$, which the proof uses
  ($J \le I$). It comes from the theorem's context.
- The stated time $B\cdot\poly(m,\log p,w,\log(1/\eps))$ hides the factor $\log B$ from sorting
  $B$ labels. That factor is $\poly(m,\log p)$ only when $k \le m$. Taking
  $k \leftarrow \min(k,m)$ first removes this. The final $2^{O(k\log(k+2))}$ bounds are
  unaffected.

Fix: "Let $k \ge 1$ with $\codim\hh \le k$ (we may take $k \le m$) and $I = p^k$."

### 5. MINOR: the $(6,5)$ terminal over $\mathbb{F}_3$ and $\mathbb{F}_5$ is a Lie-level computation, not an HSP instance

Location: `appendix-codimension.tex:328` and `appendix-provenance.tex:370`, item prov:cd-checks.

The separate AI check "found the extremal terminal $(\dim,\text{class}) = (6,5)$ at $k = 3$"
over $\mathbb{F}_3$ and $\mathbb{F}_5$. There $\mathfrak{g}_6$ has class $5 \ge p$, so those
pairs are not instances of def:input-contract. Line 133 correctly says $p > 5$.

My checks confirm the claim inside the Lazard range at $p = 7$ and $11$:
- `check_examples.out`: $\mathfrak{g}_6$ has class 5, every run gives
  $\mathcal{I} = \Span(e_4,e_5,e_6)$, and $C(\mathcal{I}) = \mathcal{I}$;
- `check_g6_terminal.out`: terminal at level 0 with $(6,5)$;
- `check_reduction_seed3.out`: largest $k = 3$ terminal is $(6,5)$ among random algebras with
  $c < p$.

Fix: add "(a Lie-level enumeration; at $p = 3, 5$ the class of $\mathfrak{g}_6$ is not below
$p$, and the HSP statement of line 133 needs $p \ge 7$)".

### 6. MINOR (optional): "exactly $1/p$" in prop:app-codim-filiform(ii)

Location: `appendix-codimension.tex:82` (statement). The proof at `:90` is exact: a witness
exists iff $\lambda = 0$, which has probability $1/p$.

A node of arity one succeeds with probability *at most* $1/p$: a capped sampler may fail with
small probability even when a witness exists. It is exactly $1/p$ only for a node that returns
a witness whenever $\lambda = 0$. The conclusion $M_d \ge 2$ uses only "at most". Fix
(optional): "succeeds with probability at most $1/p$ (a witness exists with probability exactly
$1/p$)".

## Checked and correct

- **lem:app-codim-lazard (a)-(d).** Checked: truncation-degree agreement for (c), which needs
  $\phi(\mathfrak g)$ to have class at most $c'$. BCH implemented by the cited recurrence;
  associativity, inverse and identity checked exactly in classes 4-5 at $p = 7, 11$
  (`check_reduction_seed*.out`).
- **Spanning fact (l. 70).** Fewer than $p^r$ hyperplanes; $p^{r-t} \le 2^{r-t}$ for $t \ge r$.
- **prop:app-codim-filiform (i)-(iii)** for $m \ge 4$. Checked by hand (Jacobi on basis
  triples, $\gamma_d$, $a_d = 1$, total codimension $m$, the ideal induction including
  $j = m-2$, $N(\hh) = \mathcal{I}$, two abelian calls). Exact for $m = 4..10$ at the least
  prime $\ge m$, and at $p = 101$ for $m \le 7$: every $V_j/\mathcal{I}_j$ is one-dimensional,
  so every run gives the same $\mathcal{I}$.
- **lem:app-codim-ideal and lem:app-codim-selfcentral.** Linear conditions, abelian ideal at
  each step, flag property; the descending-chain contradiction. Exact on 1,402 + 378 random
  constructions with 0 violations; "maximal" in main.tex follows from $C(\mathcal{I}) = \mathcal{I}$.
- **prop:app-codim-size.** Checked: $\rho$ is faithful on $\mathfrak g/\mathcal I$ into
  $\mathfrak n_b$, so $\dim \le b(b+1)/2$; $\gamma_b(\mathfrak n_b) = 0$, and
  $\gamma_{b+j+1} \subseteq \mathcal{I}_{b-j-1}$ gives class $\le 2b-1$.
- **The $\mathfrak g_6$ and five-dimensional examples.** Exact at $p = 3, 5, 7, 11, 13$, with
  Jacobi as an integer identity: class 5, filiform, $\mathcal I = \Span(e_4,e_5,e_6)$ for every
  run, the two bracket formulas, $C(\mathcal I) = \mathcal I$. For the five-dimensional algebra:
  class 4 and $\mathcal I = \Span(e_3,e_4,e_5)$. "Dimension 5 is least" checked by hand.
- **The two remarks on the filiform algebra.** "An abelian subalgebra cannot replace the ideal"
  ($\Span(x,e_{m-1})$) and the loose-$k$ example $B = \Span(e_2..e_{m-2})$ (l. 164): exact for
  $m = 4..10$.
- **lem:app-codim-restrict and lem:app-codim-sample.** Checked: Fourier law on $W^\perp$,
  one-sided test, rejection $\le p^{r-T}$ (in fact $r \le k$).
- **lem:app-codim-normalizer.** $[\hh,\mathfrak k] \subseteq \hh \cap \mathcal I$; the
  codimension identity.
- **lem:app-codim-transport for any section.** Uses $\pi^{-1}\pi(\hh) = \hh$ from
  $\mathfrak k \subseteq \hh$. Sampled exactly at every level of 1,982 runs: 14,394 hiding
  checks of $f_j = f\circ\Lambda_j$ and 2,622 checks with sections that are neither linear nor
  homomorphic, 0 failures.
- **Heisenberg no-splitting.** Correct, including the "normal subgroup meets the centre" step.
  Exact at $p = 3, 5$: no commuting lifts, and all $p+1$ subgroups of order $p^2$ contain $Z$.
- **lem:app-codim-unwind.** Linearity of $\sigma$ is used only here and in storing $\Lambda_j$
  as a matrix. The algorithm uses linear $\sigma$; main.tex now says so.
- **(R1)-(R4) and prop:app-codim-complete (i)-(iv).** Including $k = 0, 1, 2$, loose $k$,
  $J \le m$, at most $m$ calls, and the $k = 2$ Heisenberg terminal. 1,982 + 580 Lie-level runs,
  each recovering $\hh$, 0 violations.
- **lem:app-codim-ad.** Graded central intersection and
  $\gamma_d/(\hh\cap\gamma_d) \hookrightarrow \mathcal L/\hh$.
- **prop:app-codim-rc.** Hypotheses of thm:free-coordinate(ii)/(iv) with $u = 2k$
  ($c_J \le u$, $a_d \le u-1$, $p \ge 16u^2$); the query and time counts; the $u = 2k-1$ remark.
- **prop:app-codim-birthday.** Collision bound, conditional uniformity (nonnormal $H$ fine),
  recovery and sampling caps, $\eps/3 \times 3$. Small-prime bounds exact for $k \le 60$ at the
  extreme primes below $64k^2$, and for every $p \le 2k$ (`check_arith.out`, no failures).
- **Error budget.** $m\cdot 2^{m-T} \le \eps/4$; $2mN_s\eta = \eps/4$ by lem:hybrid (sum of
  per-transform errors); the terminal gets $\eps/2$; the transcript-coupling argument; caps on
  every branch (the dimension test forces a drop in dimension; $N(\widehat{\mathfrak k})/\widehat{\mathfrak k}$
  is always a well-formed algebra of class $< p$).
- **Proof of thm:app-codim.**
  - Part (i): finitely many classes up to $2k-1$; no BCH on $\mathcal L$ in the reduction.
  - Part (ii), first proof: branch at $64k^2$.
  - Part (ii), second proof: $p \le 2k$ versus $p \ge 2k+1$, which gives no $\kappa_d = p-1$.
    $S_J \le k(k+1)/2 + 2$; $\alpha_J = O(k^2\log k)$; arities $O(k^2\log(k+2))$. The guard
    "abort if $r > k$" never fires on the ideal support and gives trials
    $\le 2B\ln2\,(2k-1)^k + 1$. $B \le \log_2(81Q_J)+1$. The plurality vote with
    $R = \lceil 18\ln(2/\eps)\rceil$ has error $\le \eps/2$.
  - Part (iii).
- **cor:fpt-r and its proof** (main.tex 1157-1175).
  - No $\kappa_d = p-1$ for $p \ge c+2$; $S \le m+2$.
  - $2^\alpha \ge 16(216cS)^3c^2$ gives $\log_2(4\alpha c) \le \alpha$; the induction gives
    $M_d \le 4\alpha c$.
  - $x^r \le \max(r^{2r},2^{16},2^x)$: proved by cases, and grid-checked.
  - $Q_1 = 2^{O(r\log(r+2))}S^2$; Hoeffding; zero-sum node cost at $p = c+1$.
  - Filiform numbers: exact $\log_2 Q = 13.17, 24.29, 42.32$ against $58.85, 155.81, 676.81$,
    matching 13.2, 24.3, 42.3 / 58.9, 155.8, 676.8. The arities are in `check_arith.out`.
  - Scalar-flag factor $\le (r+2)^{r(r+1)/2}$.
- **cor:codim, its proof sketch, and the paragraph after it** (main.tex 1179-1191). They are
  consistent with the appendix. The fixes P2, P4 and P7 are in place.
- **rem:codim** for $m \ge 4$: see finding 2.

## Not checked / UNKNOWN

- The internal proofs of thm:main, thm:free-coordinate (ii)-(iv), lem:fc-node, lem:fc-forest,
  lem:fc-choice, prop:fc-uniform, lem:s3-law and lem:central. I used their statements only;
  these belong to other checkers' parts.
- The compile bound of thm:uniform-compilation(iii) (Kitaev, Solovay-Kitaev): statement only.
- The Lazard subgroup correspondence (lem:app-codim-lazard(d)) is cited, not proved.
- The IMS alternative in cor:fpt-r(ii): Theorem 11, Section 5 of quant-ph/0102014 is not
  checkable offline. It is already flagged NEEDS HUMAN VERIFICATION in the source.
- The first `check_examples.py` run (with a Heisenberg enumeration at $p = 7$) timed out at
  300 s and is UNKNOWN. The rerun at $p = 3, 5$ passed.

## For the human expert

- The cited external facts: the Lazard correspondence in its subgroup form (Khukhro, Section
  10.2 and Example 10.24), and that $\BCH_c$ has $\mathbb{Z}[1/c!]$ coefficients.
- Priority. The text calls the abelian-ideal and normalizer steps standard. It says a
  normalizer recursion of this kind appears in IvanyosSanselmeSantha2012 (`:326`,
  main.tex:1191), and that the priority of the composite (reduction plus free-coordinate Rees
  terminal plus birthday branch) has not been assessed. I did not assess it either.
- Part (ii) rests on thm:free-coordinate(iii) or (iv) and on the i.i.d. label law of fresh
  ideal sources (lem:s3-law), which only AI sessions have checked. The guard argument in the
  second proof of (ii) (`:316`) is short and worth a human read. It is correct as far as I can
  see: the guard never fires on the ideal support, so the ideal process and its error analysis
  are unchanged.
- Modelling: the bound is a gap between upper bounds. At fixed $k$ and polynomial $p$, the
  classical $p^{k/2}$ learner is also polynomial. The text says so twice.

## Comparison with the earlier report (`2026-11-03-rees-check-app-e.md`, read after my pass)

The two reports agree on every verdict. Status of its fixes P1-P8 in the current text:

- **P1** (the $\mathfrak g_6$ and five-dimensional examples, line 133): present and correct,
  confirmed independently. "Theorem random-column" is now correctly "parts (ii) and (iv) of
  Theorem free-coordinate".
- **P2** (main.tex: section $\tau$ versus linear $\sigma$, unwinding uses linearity, $b$ for
  $\dim\mathcal I$): present and correct (main.tex:1188).
- **P3** (Heisenberg step): present and correct (`:192`).
- **P4** (the codim promise bounds $a_d$, not $c$): present and correct in
  thm:free-coordinate(ii) (main.tex:778).
- **P5** (BCH citation in the birthday branch): present. The citation is right, and
  thm:uniform-compilation(i) now explicitly covers $\mathcal L$ itself. But P5's own phrase
  "divides only by integers at most $c$" is false (finding 1).
- **P6** (optional sentence "no step of the reduction evaluates BCH"): absent. That is
  harmless; the sentence would support the status claim for part (iii).
- **P7** ("Conditional on Theorem main" in cor:codim(i)): present.
- **P8** (stale header note deleted; independent-check sentence added): present, with the file
  path moved to prov:cd-checks. The Lie-level caveat is missing (finding 5).

What the earlier report missed:
- Finding 1, which its own P5 introduced.
- Finding 2: it judged rem:codim "accurate as written", but the remark fails at $m = 3$.
- Finding 5: its own $(6,5)$ enumeration over $\mathbb F_3$ and $\mathbb F_5$ lies outside
  $c < p$.
- The second proof of part (ii) (via thm:free-coordinate(iii), the guard, and the
  $p \gtrless 2k$ branch) did not exist on 3 Nov. I checked it here and found it correct.

# Referee report 3: Appendices "Schedule 3" and "Free-coordinate schedule"

Date: 2026-11-04. Scope: `docs/papers/rees-hsp/appendix-schedule3.tex`
(label `app:schedule3`) and `docs/papers/rees-hsp/appendix-free-coordinate.tex`
(label `app:free-coordinate`), with `main.tex` read only for the statements
these appendices prove or cite (Def. `def:input-contract`, Lemma `lem:central`,
Prop. `prop:descent`, Sec. `sec:recursion`, Lemma `lem:hybrid`,
Thm. `thm:uniform-compilation`, Thm. `thm:power-sde`, Rem. `rem:combined-schedule`,
Thm. `thm:random-column`, Thm. `thm:free-coordinate`, Prop. `prop:rc-lower`,
Prop. `prop:triangular-sde`, Table `tab:fcs-budget`, Cor. `cor:fpt-r`).
Unanchored: no earlier check, referee or integration report was read.
No `.tex` file was edited.

Classes: **error** (a false statement or a proof step that does not hold as
written), **gap** (a step that is plausibly true but not justified by what is
written), **imprecision** (wording, notation, stale cross-reference or a loose
constant that does not change truth), **fine** (checked, no issue).

Scripts: `research/audits/reviews/2026-11-04-rees-referee-3-appendices/`
(run with `/opt/anaconda3/bin/python -I`; exact integers/fractions unless
stated).

---

## Part A. Appendix `app:schedule3`

### A.0 Status paragraph and introduction

- **imprecision** — intro, "Corollary~\ref{cor:fpt-r} needs that uniformity, because there $c$ is not fixed."
  The proof of `cor:fpt-r` in `main.tex` now runs through
  Thm. `thm:free-coordinate`(iii); the Schedule 3 route is only "a second
  proof" (the appendix itself says so in the paragraph *Application to
  Corollary*). Replacement:
  `The second proof of Corollary~\ref{cor:fpt-r} given at the end of this appendix needs that uniformity, because there $c$ is not fixed.`
- **imprecision** — intro, "It uses no other step of the paper, apart from the gate counts of Theorem~\ref{thm:uniform-compilation}".
  Section `app:s3-mixed` (Prop. `prop:mixed-schedule`) also uses
  Thm. `thm:is-import`/Rem. `rem:is-import`(b), Thm. `thm:power-sde`(i),(ii),
  Thm. `thm:app-s2-main`, Rem. `rem:combined-schedule` and
  Lemma `lem:fc-forest`. Replacement: append
  `Section~\ref{app:s3-mixed} also uses Theorem~\ref{thm:power-sde}, Remark~\ref{rem:is-import}(b), Theorem~\ref{thm:app-s2-main} and Lemma~\ref{lem:fc-forest}.`

### A.1 Setting, capped subroutines, node procedure (`app:s3-setting`)

- **fine** — $p\ge16u^2>16u^2-1\ge c$, $p$ odd, $\kappa=\gcd(d,p-1)\le d\le c\le u$,
  $|P_\kappa|=h+1$, $P_\kappa\setminus\{0\}$ = nonzero $d$-th powers = nonzero
  $\kappa$-th powers. The Bezout identity~\eqref{eq:s3-bezout}
  $s^d=t^{\alpha d}=t^{\kappa}(t^{p-1})^{-\alpha'}$ is correct for $t\ne0$ and any
  sign of $\alpha$. The equivalence "solutions in power coordinates =
  $\ker\Lambda\cap S$" holds because every element of $P_\kappa$ is a $d$-th power.
- **fine** — capped draws: $p$ odd gives $2^{\ell-1}<p<2^\ell$, so acceptance
  $p/2^\ell>1/2$; a cap $R'$ times out with probability $<2^{-R'}$.
- **fine** — draw count $F=KM+MLR$: (N3) draws at most $M-r\le M$ values per
  trial; (N4) does at most $M$ extractions, $L$ steps each, $R$ rounds each, one
  draw per round. Per-draw cap $B+\lceil\log_2F\rceil$ gives a per-draw timeout
  $\le2^{-B}/F$.
- **fine** — tree: $n_d=M^{d-2}$ nodes of degree $d$, $T=\sum_{j=0}^{c-2}M^j\le M^{c-1}$,
  $M^{c-1}$ leaves.
- **imprecision** — "$u=\max(c,g_2+1)$ is computable from public data". True, but
  it is admissible only if also $p\ge16u^2$; the sentence reads as if any public
  $u$ of this form works. Replacement:
  `For instance, $u = \max(c, g_2 + 1)$ is computable from public data, since $a_d \le g_d \le g_2$; the theorem then applies when $p \ge 16u^2$.`

### A.2 Lemma `lem:s3-law` and the remark after it

- **fine** — the $M$ instruments act on distinct tensor factors of a product
  state, so outcomes are i.i.d. with the single-register law of
  Lemma `lem:central` and the post-measurement state is the product of the
  normalised branches $\rho_{\lambda_i}$, still in product with
  $\omega_{\mathcal X}$. The intrinsic-coordinate rewrite $\Lambda=EX$, $\ker\Lambda=\ker X$,
  $\rank\Lambda=\rank X\le a_d\le u-1$ (so the rank guard is silent on the ideal
  support) is correct.

### A.3 Lemma `lem:s3-moment`

- **fine** — (a) class structure: $ty\in S\iff t^h=1$; classes of size $h$; distinct
  classes on distinct lines. (b) Pairwise independence of $\mathbf 1[Xy=0]$ over
  class representatives (linearly independent by (a)); $\mathbb E N=h\mu$,
  $\operatorname{Var}N=h^2|\mathcal D|q(1-q)\le h\,\mathbb E N$. (c) Chebyshev.
  (d) union bound over lines of $\Fp^a$.
  Exhaustive check of (b) with equality, and of (c), in four small cases
  (`s3_checks.py`: $(p,\kappa,M,a)=(5,2,3,1),(5,2,3,2),(7,3,3,1),(5,4,3,1)$).
- **imprecision (harmless)** — (d) "$\le 2p^{a-M}$". The derivation actually gives
  $2p^{a-1-M}$; the stated bound is weaker by a factor $p$, so every downstream
  use is valid. No change required; if desired:
  `\item $\Pr[\rank X < a] \le \dfrac{p^a - 1}{p-1}\,p^{-M} \le 2p^{a-1-M} \le 2p^{a-M}$.`
- **imprecision** — hypothesis "Let $a\ge0$ and $M>a$": $M>a$ is used only in (d)
  (and not even there). Harmless.

### A.4 Lemma `lem:s3-mu`

- **fine** — (a) $\mu\ge h^{M-1}p^{-a}\ge p^{M-1-a}(2\kappa)^{-(M-1)}\ge p^{3u}(2u)^{-(4u-1)}$ and
  the identity $(16u^2)^{3u}/(2u)^{4u-1}=2^{8u+1}u^{2u+1}$ (exact, $u\le120$).
  (b) $h+1\ge p/\kappa$ and $p\ge2\kappa$ give $\ge\kappa^{-M}/4$; checked exactly at
  the least prime $\ge16u^2$ and at $2^{61}-1$ for every $\kappa\le u$ dividing $p-1$,
  $u\le25$.

### A.5 Lemma `lem:s3-root`

- **fine** — (a) $x^\kappa-y$ splits into distinct linear factors since $\kappa\mid p-1$.
  (b) the character-sum computation: for $\delta\ne-\rho_2$ the argument
  $1+(\rho_1-\rho_2)/(\delta+\rho_2)$ runs over $\Fp\setminus\{1\}$, the full sum is
  $-1$, and $s_{\neq}=(p-1)/2$. Checked exhaustively for all pairs of distinct
  roots and all odd primes $p\le101$. Conditional validity "whatever happened
  before" holds because $\delta$ is fresh and the bound is uniform in $g$.
  (c) keeping the smaller factor halves the degree; union bound over at most
  $\lceil\log_2\kappa\rceil$ steps.

### A.6 Lemma `lem:s3-node`

- **fine** — (a) union bound of `lem:s3-moment`(c),(d). (b) $w$ is uniform on
  $\ker\Lambda$; acceptance $N(\Lambda)/p^{M-r}$; on a good bank
  $\frac{h\mu_d}{2p^{M-a_d}}=\frac{(h+1)^M-1}{2p^M}\ge\frac1{4\kappa^M}$. Conditioning a capped
  draw on non-timeout leaves its value exactly uniform, so "trials whose draws do
  not time out" is correct.
  (c) $(1-1/(4\kappa^M))^K\le e^{-B}$; $ML(4/9)^{B+\lceil\log_2 ML\rceil}\le2^{-B}$ (checked
  exactly for $M\in\{8,12,72,200\}$, $L\le7$, $B<60$); draws $F\cdot2^{-B}/F$.
  The coupling argument (capped run differs from uncapped only on a timeout) is
  sound. (d) Prop. `prop:descent` applies to every positive-probability label
  tuple and every valid nonzero witness, and the record is a classical
  randomised function of $\Lambda$ and fresh coins, so the output is
  $\rho_{H_{d-1}}$ on every accepted record and $\omega_{\mathcal X}$ is untouched.
  (e) cost count is consistent.

### A.7 Remark `rem:s3-caveat`

- **fine** — $p=67$, $\kappa=2$, $M=8$, $a_d=1$ is admissible ($u=2$, $16u^2=64\le67$,
  $d=2$). $|P_2|=34$; $-1$ is a nonsquare mod $67$; $y_1=-y_2$ with both in $P_2$
  forces $y_1=y_2=0$; $N=34^7-1$ versus $34^6-1$, ratio $34.00000002$
  (`s3_checks.py`). Items (i)--(iii) correctly identify what the proof uses.

### A.8 Lemma `lem:s3-tree`

- **fine** — (a) induction over post-order, with the record plus other open
  registers as $\mathcal X$; leaf preparation preserves the product form.
  (b) first-abort decomposition, no independence between node events used.
  (c) $3T2^{-B}\le3/64$ and the two closed forms
  $\frac1{2^{6u+1}u^{u+2}}$, $\frac1{2^{10u+5}u^{5u+3}}$ (exact for $u\le120$, all
  $2\le c\le u$); at $u=2$ the sum is $2^{-17}+2^{-38}<1/64$.

### A.9 Lemma `lem:s3-hybrid` and proof of Theorem `thm:random-column`

- **fine** — the dephase-then-control argument gives a per-slot trace-norm
  bound $2\eta$ uniformly over records; Lemma `lem:hybrid` then applies. Unused
  slots are the identity branch of a controlled channel in both procedures.
- **fine** — part (i) assembles Lemmas `lem:s3-mu`, `lem:s3-node`(a)--(c),(e) and
  matches `main.tex` Theorem `thm:random-column`(i) exactly (same $\mu$, same
  $4/\mu+2p^{a_d-M}$, same $1/(4\kappa_d^M)$, same $4\kappa_d^MB$, same per-node
  $2^{-B}$ caps).
- **fine** — part (ii): trees are independent (disjoint fresh registers,
  independent coins); $\binom{4m'}{3m'}16^{-3m'}\le2^{4m'-12m'}\le2^{-2m'}\le(\eps/3)^2\le\eps/3$
  (exact for $m'\le300$); the remark that a one-tree bound $1/4$ already gives
  $2^{-2m'}$ is correct. Rank failure
  $\frac{p^k-1}{p-1}p^{-m'}\le\frac1{(p-1)p^{m'-k}}\le\eps/3$. $N_{\mathrm{instr}}\le13m'M^{c-1}$
  holds since $(M+1)/(M-1)\le2$ for $M\ge3$ (exact for all $u\le120$, $c\le u$).
  Matches `main.tex` Theorem `thm:random-column`(ii) (same $B$, same $1/16$, same
  $4m'$, same three thirds).
- **imprecision** — `lem:s3-hybrid` uses $S_j$ for the canonical subspaces while
  this appendix uses $S=P_\kappa^M\setminus\{0\}$ throughout. Suggest
  `Let $\mathcal S_j$ be the canonical subspaces` (and $\mathcal S_{j-1}$ in the
  proof).

### A.10 Proposition `prop:s3-uniform` and the application paragraph

- **fine** — (a) $\beta_d\le2^{-20}+2^{-41}<2^{-17}$ at $u=2$, decreasing in $u$
  (exact $u\le120$). (c),(d) correct. The final $2^{C_1u\log(u+2)}(\cdots)^{C_2}$ form
  matches `main.tex` Theorem `thm:random-column`(ii) ("$2^{O(u\log(u+2))}\poly(m,\log p,w,\log(1/\eps))$").
- **imprecision** — (b) states $B\le7+(u-1)\lceil\log_2(4u)\rceil$ but the proof gives
  $B\le6+(u-1)\lceil\log_2(4u)\rceil$ (exact for all $u\le120$, $c\le u$). Harmless;
  either replace $7$ by $6$ or say "at most $6+\dots\le7+\dots$".
- **imprecision** — (e) "A node applies $M$ central instruments with $g_d\le m$
  coordinate transforms each". Theorem `thm:uniform-compilation`(iii) counts
  $2g_d$ per central instrument (a transform and its inverse), and the next
  sentence's $q_{\max}\le\max(n,m,2Mm+um)$ uses $2g_d$. Replacement:
  `A node applies $M$ central instruments with $2g_d \le 2m$ coordinate transforms each,`
- **fine** — the paragraph on Schedule~1's query exponent
  $1+\sum_d d\lceil\log_2(d+1)\rceil$ is consistent with~\eqref{eq:is-arity}.
- **fine** — *Application to Corollary* `cor:fpt-r`: $c\le r+1=u$, $a_d\le r=u-1$, and
  $16(r+1)^2>c+2$; consistent with the remark after `cor:fpt-r` in `main.tex`
  that the Schedule~3 route is a second proof for oracle input.
- **fine** — *Scope*: $u^{4u}$ is polynomial in $m$ iff $u\log u=O(\log m)$, i.e.
  $u=O(\log m/\log\log m)$.

### A.11 Section `app:s3-mixed`: $\beta_d(M)$ and Proposition `prop:mixed-schedule`

- **fine** — $\beta_d(M)=4/\mu_d+\frac{p^{g_d}-1}{(p-1)p^M}$ at $a=g_d$; both terms are
  nondecreasing in $a$, so it is a public bound for every $a_d\le g_d$.
- **fine** — node analysis: (lin), (S1) never abort on arbitrary columns
  (Rem. `rem:is-import`(b) Bezout lift checked: $u^{td}=u^\kappa$ for $td/\kappa\equiv1\pmod h$);
  (S2) by Thm. `thm:app-s2-main` with $k=B$ ($M_d\ge(g_d+1)((\kappa_d-1)g_d+1)$: use the
  first $(g_d+1)((\kappa_d-1)g_d+1)$ columns, $s_i=0$ on the rest, and $g_d\ge1$ meets
  its hypothesis $a\ge1$); (S3) by Lemmas `lem:s3-moment`(c),(d) and the proof of
  `lem:s3-mu`(b), which only needs $p\ge2\kappa_d$. One-tree sum
  $\le1/64+(3n_{\mathrm{S3}}+n_{\mathrm{S2}})2^{-B}\le1/32$; restarts
  $\binom{4m'}{3m'}32^{-3m'}\le2^{-2m'}$. Instrument and query counts are right.
- **gap (statement/application mismatch)** — statement, "choose, from $p$, $d$ and $g_d$ only, a node type and an arity $M_d$".
  The instance used for Table `tab:fcs-budget` (paragraph after the proof)
  adds columns "at the grade of $\Gamma_3$ with the largest term $n_d\beta_d(M_d)$",
  i.e. it chooses $M_d$ from the arities of *other* grades (through $n_d$) and
  from the whole profile. That instance does not satisfy the hypothesis as
  written. The proof never uses the restriction; it only needs the choice to
  be independent of $H$, of the labels and of the coins. Replacement:
  `For each $d = 2,\dots,c$ choose, from the public data $p$, $c$ and $(g_{d'})_{2 \le d' \le c}$ only (never from $H$, the labels or the coins), a node type and an arity $M_d$ of one of the following kinds:`
- **gap (minor)** — *Restarts*, "Conditional on the records of all other trees, a tree acts on fresh registers with fresh coins".
  For (S2) nodes this needs every (S2) node, or at least every tree, to run
  Phase~0 of Thm. `thm:app-s2-main` (coset generator and contraction scalars)
  with its own coins. Phase~0 depends only on $(p,\kappa,k)$, so an
  implementation would naturally compute it once and share it; then tree aborts
  are correlated and the binomial bound does not apply as written. Replacement
  (add after "(S2) ... with $k = B$;"):
  `each node of type (S2) runs Phase~0 of that solver with its own coins, so that no randomness is shared between nodes;`
- **imprecision** — paragraph after the proof, "the tree-abort bound, between $2^{-6.9}$ and $2^{-6.4}$ at these primes".
  "These primes" refers to the six primes of the table, but at $p=11$ and
  $p=1031$ the instance has no (S3) node (dashes in the table). At $p=11$ it has
  no capped node at all (bound $0$), and at $p=1031$ it keeps (S2) at grades
  $2,4,6,8$ with tree-abort bound $2^{-6.14}$. At the four (S3) primes the
  recomputed range is $2^{-6.91}$ ($2^{127}-1$) to $2^{-6.38}$ ($5281$), so the
  upper end rounds to $2^{-6.4}$ only from above (`class9_checks.py`).
  Replacement:
  `At the six primes of the table no column is added. At the four primes where the instance uses a node of type (S3), \eqref{eq:s3-weighted-bank} holds with room to spare: its left side is at most $2^{-67}$, so the tree-abort bound, between $2^{-6.91}$ and $2^{-6.38}$ there, comes from the arithmetic caps.`
- **fine (recomputed)** — independent recomputation (`class9_checks.py`, written
  from the statements only) reproduces: uniform-kernel $\log_2Q=4m'cP$ of
  $50.3,50.9,52.9,49.9$ and trials $128.2,121.6,128.3,115.2$ at
  $5281,2^{31}-1,2^{61}-1,2^{127}-1$; no column added at any of the six primes;
  left side $2^{-67.2}$ at $5281$ (smaller elsewhere); Schedule~2 kept at grade
  $8$ for $2^{31}-1,2^{61}-1$ and at grades $8,9$ for $2^{127}-1$, none at $5281$;
  at $p=151$ with $M_9=12$ the left side is $2^{331.2}$ and the rule adds exactly
  $60$ columns at grade $9$; exactly $226$ primes $11\le p<3600$ get a column.

---

## Part B. Appendix `app:free-coordinate`

### B.0 Status paragraph and introduction

- **imprecision** — intro, "From Appendix~\ref{app:schedule3} it uses Lemmas~\ref{lem:s3-law}, \ref{lem:s3-root}, \ref{lem:s3-node} and~\ref{lem:s3-tree}, ...".
  The proof of part (ii) also uses Lemma `lem:s3-hybrid` (through "the proof of
  Theorem random-column(ii) ... word for word") and Remark `rem:s3-caveat`; Remark
  `rem:fc-tradeoff`(a) uses Prop. `prop:triangular-sde` and $E_2(\kappa)$ from the
  body; Section `app:fc-mixed` uses Thm. `thm:is-import` and
  Rem. `rem:combined-schedule`. Add them to the two lists.

### B.1 Setting, $\beta(M,n_0;a)$ and the node procedure (`app:fc-setting`)

- **fine** — \eqref{eq:fc-q}: $q=(p-1+\kappa)/(\kappa p)\in[1/\kappa,1]$ and
  $1/q=\kappa/(1+(\kappa-1)/p)\ge\kappa e^{-(\kappa-1)/p}$. $\kappa_d<p-1\iff h\ge2$, and it
  forces $p\ge3$. The kernel identity (row $i$ of $Ry$ is $v_i-v_i=0$) is correct.
  The irrationality remark on $2B\ln2\cdot q^{-r}$ is correct. Draws from $\Fp^\times$:
  $(p-1)/2^\ell\ge1/2$.
- **imprecision (stale text)** — "By~\eqref{eq:s3-bezout}, applied with $\beta = \alpha'$, if $\sigma^\kappa = y \ne 0$".
  \eqref{eq:s3-bezout} has no $\beta$, and $\beta$ is the name of the bank bound
  defined two lines later. Replacement:
  `By~\eqref{eq:s3-bezout}, if $\sigma^\kappa = y \ne 0$ then $s = \sigma^\alpha$ satisfies $s^d = y$.`
- **imprecision** — "Both terms increase with $a$, because $q \le 1$."
  For $\kappa=1$ (allowed in part (ii)) $q=1$ and the first term is constant.
  Replacement: `Both terms are nondecreasing in $a$, because $q \le 1$.`
- **imprecision (notation)** — the letter $R$ denotes the echelon matrix in
  (F2) and the round cap $R=2(B+\lceil\log_2(ML_\kappa)\rceil)$ in the next
  paragraph (and again in Lemma `lem:fc-node`(c),(e), where both occur). Suggest
  renaming the round cap, e.g. `$R_{\mathrm{rd}} = 2(B + \lceil\log_2(ML_\kappa)\rceil)$`.

### B.2 Lemma `lem:fc-rref`

- **fine** — (a) row space of $EX$ equals row space of $X$ since $E^{\mathsf T}$ is
  onto; (b) $\GL_M$-invariance gives a uniform row space given the rank, and the
  RREF cell of a pivot pattern is an affine space, so free entries are i.i.d.
  uniform; every entry right of $p_r$ is free; (c) $p_r>L$ forces
  $\rank X_{[L]}<r\le a$. Exhaustive checks: the law of the free block and
  (c) in several small cases (`fc_checks.py`).

### B.3 Lemma `lem:fc-moment`

- **fine** — proportional partners are exactly $t\in P_\kappa$ ($h$ of them),
  covariance $q^r-q^{2r}$; non-proportional pairs independent. Mean and variance
  verified with equality, for every pivot pattern, in five small cases
  (`fc_checks.py`). Chebyshev step correct.

### B.4 Lemma `lem:fc-node` and proof of Theorem `thm:free-coordinate`(i)

- **fine** — (a) union of $\{n'<n_0\}$ and, given $(r,\pi)$, the Chebyshev event;
  the monotone steps $h\ge2$, $n'\ge n_0$, $q\le1$, $r\le a_d$ are right. (b) $b\mapsto b^\kappa$
  has fibres of size $\kappa$, so $x$ is uniform on $P_\kappa^{n'}$. (c)
  $(1-q^r/2)^{T_r}\le2^{-B}$; root and draw caps as in A.6. (d) witness, Bezout,
  and the descent argument. (e) cost.
  The assembled statement matches `main.tex` Theorem `thm:free-coordinate`(i)
  (same $\beta$, same $q^r/2\ge1/(2\kappa_d^r)$, same $T_r$, same caps, "no condition
  on $p$ beyond $\kappa_d<p-1$").
- **imprecision (notation)** — statement, "receive the state $\rho_{H_d}^{\otimes M}\otimes\omega_X$, for any system $X$".
  $X$ is the uniform $a\times M$ matrix of Lemma `lem:fc-rref`(a), used in the
  same proof. Section `app:fc-split` already renamed the side system. Replacement:
  `receive the state $\rho_{H_d}^{\otimes M}\otimes\omega_{\mathcal X}$, for any system $\mathcal X$,` (and $\mathcal X$ in (d)).
- **imprecision (main.tex)** — Theorem `thm:free-coordinate` preamble assumes
  "$\kappa_d<p-1$", while part (iii) covers grades with $\kappa_d=p-1$. The appendix
  explains this ("in part (iii) it is not assumed at the grades with
  $\kappa_d\in\{1,p-1\}$"), but the theorem as stated reads as if (iii) were
  restricted too. Suggest in `main.tex`:
  `Assume the labels at a stage-$d$ node of the free-coordinate sampler are independent and uniform on a subspace of dimension $a \le g_d$, and $\kappa_d < p-1$ at every such node (part~(iii) uses other nodes at the remaining grades).`

### B.5 Lemma `lem:fc-params` and proof of Theorem `thm:free-coordinate`(ii)

- **fine** — $h\ge(16u^2-1)/u\ge15u$; $h^{n_0-1}q^{a_d}\ge15^{2u}u^{u+1}$; second term
  $\le2p^{a_d-2u}\le2p^{-u-1}$; closed forms $(4/225)^u/u^2$ and
  $2\cdot4^{u-1}/(16^{u+1}u^{u+3})$ (exact for $u\le120$); at $u=2$,
  $7.90\cdot10^{-5}+6.10\cdot10^{-5}<1.5\cdot10^{-4}$. Part (ii) correctly reuses
  `lem:s3-tree`(a),(b), the restarts and `lem:s3-hybrid`; it matches `main.tex`
  Theorem `thm:free-coordinate`(ii) (same $M=4u$, $n_0=2u+1$, $B$, $1/16$, trial bound).

### B.6 Section `app:fc-mixed`: (R1)--(R4), Lemma `lem:fc-choice`, the zero-sum node, Lemma `lem:fc-forest`, proof of (iii)

- **fine** — classification $\Gamma_{\mathrm F},\Gamma_1,\Gamma_0$ is a partition for $p\ge3$;
  $\Gamma_0\subseteq\{p-1\}$; at $\Gamma_0$ the combined rule is Schedule~1 at degree $d$.
- **fine** — Lemma `lem:fc-choice`: $n_0-1$ is the least $k$ with
  $h^k\ge8q^{-g_d}/\tau$; first term $\le\tau/2$, second $<\tau/(2(p-1))$; size bound via
  $\ln(1/q)\le\ln\kappa$, $\ln h\ge\frac12\ln(p/\kappa)$. Checked on 400 random
  $(p,\kappa,g_d,\tau)$ with exact $\beta$ (`fc_checks.py`).
- **fine** — Lemma `lem:fc-zero-sum`: (a) $2^M-1$ pairwise independent indicators
  (distinct nonzero $0/1$ vectors are non-proportional), Chebyshev gives
  $(p^a-1)/(2^M-1)$; checked exhaustively in five cases. (b) Chevalley--Warning
  (degree sum $g_d(p-1)<M$); exhaustive Davenport check for $C_3^2$, $C_5$, $C_3$.
  (c) the subset-sum table. (d) witness. The remark that
  $M_d=1+\lceil\log_2(p^{g_d}/\tau_d)\rceil$ gives abort $\le\tau_d$ is correct.
- **fine** — Lemma `lem:fc-forest`: (a) the induction with four node kinds;
  (b) $\sum_{\Gamma_{\mathrm F}}Sn_d\tau_d\le\eps/9$ (since $|\Gamma_{\mathrm F}|\le c-1$) and
  $3N2^{-B}\le\eps/9$.
- **fine** — proof of (iii): $2\eps/9+\eps/3+\eps/3=8\eps/9$; rank bound
  $p^{k-m-t}/(p-1)\le\eps/(3(p-1))$; instrument count; query count $cS\prod_dM_d$.
  Matches `main.tex` Theorem `thm:free-coordinate`(iii) ($\tau_d$, $B=\lceil\log_2(27N/\eps)\rceil$,
  $N$ the number of sampler nodes, zero-sum option $M_d=g_d(p-1)+1$).
- **imprecision (main.tex)** — Theorem `thm:free-coordinate`(iii), "The arity is $M_d = g_d\bigl(1 + O(\log\kappa_d/\log(p/\kappa_d))\bigr) + \dots$".
  The theorem allows "any public $M_d\ge n_0\ge1$ with $\beta\le\tau_d$", and
  the arity, query and time statements then hold only for the explicit (or the
  least) choice, as the appendix says ("With $\tau=\tau_d$, Lemma fc-choice is
  the arity statement"). Suggest: `With the explicit choice, the arity is $M_d = \dots$`.
- **imprecision** — remark after the proof of (iii), "that variant is covered by the proof above only if Theorem~\ref{thm:power-sde}(ii) is added as a hypothesis".
  Overstated. If the combined rule's arity at that grade is Schedule~1 at degree
  $\kappa_d$ (or linear), no Schedule~2 hypothesis is needed, but the Bezout lift
  of Remark `rem:is-import`(b) is. Replacement:
  `that variant is covered by the proof above if the Bezout lift of Remark~\ref{rem:is-import}(b) is added as a hypothesis and, at grades where the combined rule takes Schedule~2, also Theorem~\ref{thm:power-sde}(ii), with its Las~Vegas calls capped at total failure $\eps/9$.`
- **imprecision (main.tex consistency)** — `main.tex`, discussion after
  Theorem `thm:free-coordinate`, says (iii) "uses no Schedule~2 node and no Bezout
  lift". Every free-coordinate node converts with the Bezout exponent $\alpha$
  ((F4), via \eqref{eq:s3-bezout}). What is absent is the lift of
  Remark `rem:is-import`(b) for Schedule~1 at a reduced degree. Suggest:
  `It uses no Schedule~2 node and no Schedule~1 call at a reduced degree (the free-coordinate nodes use only the elementary identity~\eqref{eq:s3-bezout}), because ...`

### B.7 Proposition `prop:fc-uniform`

- **fine** — (a) $4\cdot15^{-4}2^{-3}+2\cdot64^{-3}=1.75\cdot10^{-5}<2^{-14}$; the other
  items follow from B.5 and A.10.
- **fine** — (b) node count $S\sum_dn_d<(c-1)SP<Q$ (every $M_d\ge2$); for fixed $c$,
  $M_d\le(1+2\log_2c)g_d+3\log_2(72(c-1)Sn_d/\eps)+3$ is the right specialisation of
  `lem:fc-choice` ($\ln(p/\kappa_d)\ge\ln h\ge\ln2$); the induction on $d$ gives
  polynomial $Q$.
- **gap (minor)** — (b), "$t_{\mathrm{S1}}$ is the time of one Schedule~1 call at the grade $d = p-1$".
  (R1) and Theorem `thm:free-coordinate`(iii) allow the zero-sum node at that
  grade instead; its cost (Lemma `lem:fc-zero-sum`(c): up to
  $M_d\min(2^{M_d},p^{g_d})$ additions) is not covered by the displayed bound,
  although it is $2^{O(g_d\log\kappa_d)}$ there and so within the theorem's
  claim. Replacement:
  `and $t_{\mathrm{S1}}$ is the time of the node at the grade $d = p-1$: one Schedule~1 call, or one zero-sum search of Lemma~\ref{lem:fc-zero-sum}(c), at most $M_d\min(2^{M_d},p^{g_d})\cdot\poly(g_d,\log p)$ (zero if $\Gamma_0 = \emptyset$, which holds whenever $p > c+1$).`

### B.8 Section `app:fc-numbers` (class-nine profile)

Recomputed independently (`class9_checks.py`, least arities by exact search over
$(M,n_0)$; no repository code imported).

- **fine** — (a) all six rows of the three (iii) columns of Table `tab:fcs-budget`
  reproduce: $\log_2Q=42.3,36.6,39.1,35.9,34.1,34.0$; trials
  $28.3,33.4,33.8,31.0,33.5,31.0$; totals $47.0,50.8,52.2,49.8,51.0,49.5$. Largest
  cap $2^{33.78}$ at $p=5281$, grade $4$, $B=40$. Explicit choice: $+1$ or $+2$
  columns per FCS grade, $\log_2Q$ up by $0.24$ to $1.31$, largest cap still
  $2^{33.8}$. No grade in $\Gamma_0$ and no Schedule~2 at these primes. The
  combined-rule column also reproduces ($202.1,167.3,852.3,944.9,555.4,61.5$).
- **fine** — (b) $u=18$, $M=72$, $n_0=37$, $B=56$; all six primes are prime; bank
  sum per tree $\le2^{-234.95}$ (at $5281$).
- **error (minor, numerical)** — (b), "the per-node cap at $a_d = g_d$ is at most $2^{34.3}$, reached at $p = 5281$".
  The maximum over the six primes is $2^{34.2786}$, reached at
  $p=194522647344910884721$ (grade $4$, $\kappa=4$); at $p=5281$ it is $2^{34.2671}$
  (`part2_cap_precise.py`). The bound $2^{34.3}$ is right; the attribution is not.
  Replacement:
  `the per-node cap at $a_d = g_d$ is at most $2^{34.3}$ (largest at $p = 194522647344910884721$, and $2^{34.27}$ at $p = 5281$), and the bank sum per tree is at most $2^{-234.9}$.`
- **imprecision (misattribution; also in `main.tex`)** — closing paragraph, "against about $2^{128}$ for the uniform-kernel sampler of Theorem~\ref{thm:random-column}".
  $2^{128}$ is the trial cap of the per-grade *mixed* instance of
  Prop. `prop:mixed-schedule` (Table `tab:fcs-budget`). Theorem
  `thm:random-column` itself, at this profile ($u=18$, $M=72$, $B=56$), has per-node
  cap $4\kappa_d^{72}B$, i.e. $2^{223.8}$ at $5281$ and $2^{236.0}$ at $2^{31}-1$,
  $2^{61}-1$, $2^{127}-1$ (`rc_thm_cap.py`). The same wording is in `main.tex`
  ("about $2^{128}$ on the class-nine profile below"). Replacement:
  `against about $2^{128}$ for the uniform-kernel nodes of the mixed instance of Proposition~\ref{prop:mixed-schedule} (Table~\ref{tab:fcs-budget}), and about $2^{224}$ or more for Theorem~\ref{thm:random-column}(ii) itself at $u = 18$.`

### B.9 Proof of Proposition `prop:rc-lower` (`app:fc-lower`)

- **fine** — the generic event (first $a$ columns invertible) fails with
  probability $\le1/(p-1)$, within the stated $1/(p-1)+2p^{a-M}$; mean acceptance
  $(q^n-p^{-n})q^a\le q^M$; Markov; the oblivious-design bound $Tq^a$ by the last
  claim of `lem:fc-moment`; the factor $4B\ln2$. The example $p=5$, $R=[1\ 2]$
  ($-2x\in\{3,2\}$, $\beta\ge1$ for $n_0\le2$) is correct. Matches `main.tex`.
- **imprecision** — "drawn from a joint law that depends on the pattern and on private coins, but not on $R'$".
  This excludes designs that adapt candidates to earlier accept/reject
  feedback (whose joint law depends on $R'$). The free-coordinate sampler is
  non-adaptive, so the comparison is right, but the scope is worth one clause.
  Suggest adding: `(in particular, not on the outcomes of earlier trials)`.

### B.10 Section `app:fc-split`: split node, Lemma `lem:fc-split-law`, Propositions `prop:fc-split-node` and `prop:fc-split`

- **fine** — Lemma `lem:fc-split-law`: (a) telescoping and $V_k=0$; (b) witness by
  induction on levels, $D\cdot D\subseteq D$, nonzero path, $\theta^\kappa=Y$; (c) the
  decomposition $V_{j-1}=V_j\oplus W$ with $\pi_j$ injective on $W$: the
  sub-solver's record is a function of $(u'',\omega)$ only, the output is
  $\sum_ly_lu'_l$, uniform on $V_j$ and independent of the other open vectors.
  This argument is correct and is the key point of the section. (d) follows.
- **fine** — the counterexample to reading full inputs: exhaustive enumeration
  of all $625$ banks gives $\Pr[z_\eta=0\mid\text{no abort}]=69/325$ over $325$
  non-aborting banks (`fc_checks.py`), as stated.
- **fine** — Prop. `prop:fc-split-node`: (a) the first-abort sum with the law of
  `lem:fc-split-law`(d); (c) $\nu=1+M_k\nu'$, $\nu\le(M-1)/(m_*-1)$,
  $\nu\le2\prod_{j\ge2}M_j$ (checked on six arity lists); $n_0^{(j)}=1\Rightarrow\beta_j\ge4$.
- **fine** — Prop. `prop:fc-split`: target~\eqref{eq:fc-split-target} chosen
  top-down so $n_{d,j}$ is known; $\sum_jn_{d,j}\tau_{d,j}=\tau_d$; abort
  $\le\eps/9+\eps/9$; $N<Q$; $M_{d,j}\ge g_{d,j}+1$ from the second term of $\beta$, and
  $\sum_jg_{d,j}\ge g_d$ from $\bigcap_j\ker\pi_j=0$. Consistent with the summary in
  `main.tex` after Prop. `prop:rc-lower` ("fewer than $M_d$ sub-solvers",
  "$2B\ln2\cdot\kappa^{\lceil g_d/k\rceil}+1$ trials").
- **imprecision (notation)** — $n_j=\prod_{i>j}M_i$ (level counts) next to
  $n_0^{(j)}$ (free-column thresholds), $n_d$ (tree node counts) and $n_{d,j}$; and
  $a_j$ (level drops) next to $a_d$ (label rank at grade $d$). Unambiguous in context,
  but $n_0$ is overloaded (level-$0$ count $=M$ vs. threshold). Suggest $N_j$ for
  the level counts or a sentence saying $n_0$ always means the threshold.

### B.11 Remark `rem:fc-tradeoff`

- **fine** — label count $\sum_{i<K}(a-i+1)=K(2a-K+3)/2$ (exact, $a<30$); (b) full
  column rank when $M_j\le a_j$ (failure except w.p. $\le p^{M_j-a_j}/(p-1)\le1/(p-1)$),
  $\prod_j(a_j+1)\ge(a_{\max}+1)(a-a_{\max}+1)$, the two-group argument (checked on a
  grid), and the dimension bound $a_{\max}>a+1-2M/a$.
- **gap** — (a), "in time $\poly(a, B, \log p)\cdot\kappa^{\,g}$".
  Prop. `prop:triangular-sde` takes a universal two-level contraction
  $(\alpha,\beta)$ as *input* (a hypothesis). Finding one is a separate step
  depending only on $(p,\kappa)$: for instance an exhaustive search over
  $\Fp^{2\kappa-2}$, or a sampler of the kind used in Phase~0 of Schedule~2, whose
  cost in `main.tex` is quoted as $O(\kappa^{\kappa+2}\log\kappa)$ coset tests per round
  for $p\ge T_S(\kappa)$. This cost is not $\poly(a,B,\log p)\cdot\kappa^{g}$
  uniformly in $\kappa$, and its failure probability (if randomised) is not in
  the $5\cdot2^{-B}$ term. Replacement:
  `in time $\poly(a, B, \log p)\cdot\kappa^{\,g}$, given the contraction $(\alpha,\beta)$, whose cost depends only on $(p,\kappa)$ and is not counted here.`
- **gap (minor)** — (a), "Apply (F2)--(F4) to the images of $g+n_0$ further labels in $\Fp^a/U_K \cong \Fp^{g}$".
  The triangular construction can stop early (when $v_{k+1}\in U_k$), and then
  $\dim U_K<K$ and the quotient is not $\Fp^g$. In that case it has already
  produced a solution. Add: `If a round stops early (Proposition~\ref{prop:triangular-sde}), its realisation is already a solution and the free-coordinate step is skipped; otherwise $\dim U_K = K$.`
- **imprecision (notation)** — (a) uses $g=a-K$ and, in the same sentence,
  "the coset generator $g$" (the generator of $\Fp^\times$ in
  Prop. `prop:triangular-sde`). Rename the dimension, e.g. $g' = a-K$.

---

## Ranked summary

No error was found in any probability bound, union bound, conditioning
step, product-state/label-law induction, abort budget, restart count or
constant that a theorem of `main.tex` relies on. Every lemma, proposition
and theorem proved in the two appendices matches the version stated in
`main.tex` (hypotheses and constants), apart from the scope imprecisions listed
under B.4 and B.6. All recomputed numbers agree except the two items flagged
in B.8 and A.11.

Counts: **1 error** (minor, numerical), **5 gaps** (none affects a headline
theorem; two concern Prop. `prop:mixed-schedule`, two concern remarks or cost
side-statements of the free-coordinate appendix), **22 imprecisions**.

Gaps and errors, most important first:

1. **Gap**: Prop. `prop:mixed-schedule`, "choose, from $p$, $d$ and $g_d$ only". The
   instance behind the uniform-kernel columns of Table `tab:fcs-budget` chooses
   arities from $n_d$, so from other grades. The proof does not need the
   restriction. Restate the hypothesis as "from public data only" (A.11).
2. **Gap**: Prop. `prop:mixed-schedule`, *Restarts*. Tree independence needs every
   (S2) node to run Schedule~2's Phase~0 with its own coins. Phase~0 depends only
   on $(p,\kappa,k)$, so sharing it is the natural implementation, and then the
   binomial restart bound does not apply as written (A.11).
3. **Gap**: Remark `rem:fc-tradeoff`(a). The time $\poly(a,B,\log p)\kappa^{g}$ omits
   the cost (and any failure probability) of obtaining the universal
   contraction that Prop. `prop:triangular-sde` takes as input (B.11).
4. **Gap**: Prop. `prop:fc-uniform`(b). The time bound covers Schedule~1 at the grade
   $d=p-1$ but not the zero-sum alternative that (R1) and Theorem
   `thm:free-coordinate`(iii) allow there. The claimed $2^{O(g_d\log\kappa_d)}$ form is
   still true (B.7).
5. **Gap (minor)**: Remark `rem:fc-tradeoff`(a). The triangular rounds can stop early,
   and then $\Fp^a/U_K\not\cong\Fp^{g}$; the remark should say that a solution is
   then already in hand (B.11).
6. **Error (minor, numerical)**: `app:fc-numbers`(b). The part-(ii) per-node cap
   $2^{34.3}$ is reached at $p=194522647344910884721$ ($2^{34.279}$), not at
   $p=5281$ ($2^{34.267}$) (B.8).

The most consequential imprecisions:

- `app:fc-numbers` closing paragraph (and `main.tex` before Theorem
  `thm:free-coordinate`): "$2^{128}$ for the uniform-kernel sampler of Theorem
  `thm:random-column`". That figure belongs to the mixed instance of
  Prop. `prop:mixed-schedule`. Theorem `thm:random-column`(ii) itself gives
  $2^{223.8}$ to $2^{236.0}$ per node at $u=18$ (B.8).
- Paragraph after Prop. `prop:mixed-schedule`: the tree-abort range "$2^{-6.9}$ to
  $2^{-6.4}$ at these primes" holds only at the four (S3) primes, where it is
  $2^{-6.91}$ to $2^{-6.38}$ (A.11).
- `main.tex` Theorem `thm:free-coordinate`: its preamble assumes $\kappa_d<p-1$
  although (iii) covers $\kappa_d=p-1$, and its arity statement applies only to
  the explicit choice. The discussion after it says "no Bezout lift", although
  free-coordinate nodes use the Bezout exponent (B.4, B.6).
- Stale "applied with $\beta=\alpha'$" in `app:fc-setting`. "$g_d$ coordinate transforms"
  should be $2g_d$ in Prop. `prop:s3-uniform`(e). $B\le7+\dots$ is provable as
  $6+\dots$ (B.1, A.10).

Scripts and outputs (all in
`research/audits/reviews/2026-11-04-rees-referee-3-appendices/`):
`s3_checks.py` → `s3_checks_out.txt`; `fc_checks.py` → `fc_checks_out.txt`;
`class9_checks.py` → `class9_checks_out.txt`; `part2_cap_precise.py` →
`part2_cap_precise_out.txt`; `rc_thm_cap.py` → `rc_thm_cap_out.txt`. All exact
checks pass. The class-nine script was written from the appendix statements
alone and imports no repository code.

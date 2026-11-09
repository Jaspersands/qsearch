# Rees block splitting: k-level free-coordinate sampling (proof for the body sentence after prop:rc-lower)

AI session only (Claude Code, 2026-11-02). No human review. Edits nothing outside this report
and `2026-11-03-rees-block-splitting/`.

Target: the sentence in `docs/papers/rees-hsp/main.tex` right after `prop:rc-lower`
("Splitting the public coordinates ..."), currently proved only in
`2026-11-02-rees-schedule3-cost.md` (Lemma 5.2, Prop 5.3).

## 0. Verdict

- **Proved (AI-checked, pending human review), with one correction to the body sentence.**
  The block-splitting refinement holds: a k-level free-coordinate node returns a valid
  nonzero witness at arity M_d = prod_j M_{d,j} on every bank; given everything read so far,
  each level-j bank is i.i.d. uniform on pi_j(K_d^perp cap ker pi_1 cap ... cap ker pi_{j-1});
  a node aborts with probability at most sum_j n_j (beta_j + 3 2^-B); and Theorem
  free-coordinate (iii) survives with split grades (Prop `prop:fc-split`).
- **Correction.** "Reduces the per-node cost to about kappa^{g_d/k}" is true per SUB-solver,
  not per node. A node runs nu_d = sum_j prod_{i>j} M_{d,i} <= M_d - 1 sub-solvers, each capped
  at 2B ln2 kappa^{ceil(g_d/k)} + 1 trials. The total classical time is
  Q (2 + 2B ln2 max_d kappa_d^{max_j g_{d,j}}) poly + Q t_S1, so the exponent does drop to
  about (g_d/k) log kappa_d; the queries rise (the arity is a product of k factors).
- **Two things the source sketch left implicit, now proved:** the conditioning for the union
  bound across sub-solvers (Lemma `lem:fc-split-law`(c): independence holds given the record of
  ALL earlier sub-solvers, other blocks included), and the order of the arity choice
  (top level first, since n_{d,j} depends on the later levels).
- **Gate found (smallest counterexample).** The law statement needs each sub-solver to read
  only the pi_j-images of its own inputs. At p = 5, kappa = 2, V = F_5^2, M_1 = 2, a sampler
  that also reads the second coordinate gives Pr[w = 0] = 69/325, not 1/5 (exact). FCS obeys
  the hypothesis, so the claim stands; the hypothesis is now explicit in the text.
- No step failed. An independent AI referee pass (one subagent, read-only) found no
  mathematical error; its wording fixes are applied (precise counterexample statement with a
  genuine split, "public data" in the arity choice, sub-bank cost O(g_j g_d M_j), M_d > g_d for
  the poly factor, conditioning on X made explicit, k_d <= g_d).

## 1. Setting and what the paper already proves

Target appendix: `docs/papers/rees-hsp/appendix-free-coordinate.tex`, label `app:free-coordinate`.
STATE.md and the free-coordinate report call it "Appendix F"; in the current `\ReesAppendix`
input order of `main.tex` it is the third appendix (lettered C). The new subsection goes at the
end of that file, after the `\paragraph{Scope.}`.

Reused by `\ref` (not repeated): Lemmas `lem:fc-rref`, `lem:fc-moment`, `lem:fc-node`,
`lem:fc-choice`, `lem:fc-forest`, Prop `prop:fc-uniform`, the procedure (F1)-(F6), (R1)-(R4),
`eq:fc-beta`, `eq:fc-q`; from Appendix `app:schedule3`: `lem:s3-law`, `eq:s3-bezout`,
`rem:s3-caveat`.

The body claim has three parts:
1. a k-level solver at a grade node produces a valid nonzero witness at arity prod_j M_j;
2. "keeps the label law at each level": each level's bank is i.i.d. uniform on a subspace,
   given everything read so far;
3. cost "about kappa^{g_d/k}" per node.

Parts 1 and 2 are exactly what the source Lemma 5.2 / Prop 5.3 sketch. The source never
writes down the conditioning needed for the union bound across sub-solvers (the record of
earlier sub-solvers, including other blocks at the same level), the order in which arities
must be chosen (n_{d,j} depends on the later levels), or the accounting of the cap exponent B.
Part 3 is imprecise as written: kappa^{g_j} is the cap per SUB-solver; a grade node runs
nu_d = sum_j prod_{i>j} M_{d,i} of them (at most M_d - 1), so its cap is about
nu_d * 2B ln2 * kappa^{max_j g_{d,j}}.

## 2. Law transfer lemma (Lemma `lem:fc-split-law`)

Full proof in the LaTeX of Section 8. Key step (c), by induction over the sub-solvers in
execution order: given the record R_t of the first t sub-solvers and no abort, the open vectors
(labels not yet read, outputs not yet read) are independent and a level-j one is uniform on
V_j = V cap ker pi_1 cap ... cap ker pi_j. For the next sub-solver, split each input
u_l = u'_l + u''_l along V_{j-1} = V_j (+) W. pi_j is injective on W, so the sub-bank determines
u'' and the sub-solver's whole record is a function of (u'', coins). Its kernel equation forces
sum y_l u''_l = 0, so the output is sum y_l u'_l, with u' independent of everything conditioned
on and y != 0. Hence the output is uniform on V_j and independent of the other open vectors.
Part (b) (witness) is deterministic: pi_i(z_eta) = 0 for i <= j by induction, the top vector lies
in the common kernel of the pi_i, which is 0, so Lambda Y = 0; D.D in D gives Y in D^M; a path
of nonzero coefficients gives Y != 0; Bezout gives s^d = Y.

## 3. k-level propositions (`prop:fc-split-node`, `prop:fc-split`)

- One node: union bound over sub-solvers, each term conditioned on E_t as in Lemma
  `lem:s3-tree`(b); the proof of Lemma `lem:fc-node`(a)-(c) uses the bank only through
  Lemmas `lem:fc-rref` and `lem:fc-moment`, whose hypothesis Lemma `lem:fc-split-law`(d)
  supplies with (g_j, M_j, n_0^(j), a_j); monotonicity of beta in a gives beta_j. Output law is
  the proof of `lem:fc-node`(d) verbatim.
- Schedule: `lem:fc-forest`(a) needs only the node's output law and that its record is a
  classical randomized function of bank and coins; (b) gets the node term
  tau_d + 3 nu_d 2^-B; N = S sum_d n_d nu_d keeps 3N 2^-B <= eps/9. Instrument count,
  tree shape and the rank step are unchanged. Explicit choice: tau_{d,j} = tau_d/(k_d n_{d,j}),
  chosen from j = k_d down, then Lemma `lem:fc-choice` (its proof uses g_d only as the
  dimension argument of beta).
- Counting: nu = 1 + M_k nu', so nu <= (M-1)/(min M_j - 1) <= M-1; beta_j <= 1 forces
  n_0 >= 2, so M_j >= 2 automatically.
- Compiled: the subsection appended to a scratch copy of `appendix-free-coordinate.tex`, with
  the body line replaced, builds with pdflatex (111 pages, no errors, no undefined references).
  It becomes subsection C.10 in the current input order (labels C.8-C.10, equation 15).

## 4. Exact checks (`2026-11-03-rees-block-splitting/`)

```bash
cd research/audits/reviews/2026-11-03-rees-block-splitting && /opt/anaconda3/bin/python -B -u block_split_check.py > block_split_check_out.txt
cd research/audits/reviews/2026-11-03-rees-block-splitting && /opt/anaconda3/bin/python -B -u block_split_check.py DF > block_split_check_DF_out.txt
```

The first takes about 6 minutes, the second 2 seconds. Independent code (imports nothing from
the 11-02 report scripts); Fractions and integers throughout, except [F].

- **[A] law transfer, exhaustive.** V a 2- or 3-dimensional subspace that is NOT a coordinate
  subspace (in F_5^3, F_7^3, F_5^4), pi a coordinate projection, M = 3, n_0 in {1, 2},
  (p, kappa) in {(5,2), (7,3), (7,2)}. For every pi-bank with an accepted draw (97 to 4897 of
  them), the law of w = sum y_i lambda_i over the labels consistent with that pi-bank and over
  the accepted draws is exactly uniform on V_1 = V cap ker pi. Passed.
- **[B] joint law of a level-2 bank, exhaustive per record pair.** Two level-1 sub-solvers on
  disjoint blocks, 12 random pairs of level-1 records: (w_1, w_2) is exactly uniform on V_1^2,
  and the level-2 bank (pi_2 w_1, pi_2 w_2) on pi_2(V_1)^2. Passed.
- **[C] gate, exhaustive.** A level-1 sampler that reads the full labels (it prefers an
  accepted y with w_2 = 0) at p = 5, kappa = 2, V = F_5^2, pi = first coordinate, M = 2:
  Pr[w = 0] = 69/325, not 1/5. So the hypothesis "each sub-solver reads only the pi_j-images of
  its own inputs" is needed for the law statement (the witness stays valid either way).
- **[D] end-to-end, random.** k = 2 and 3, coordinate blocks and a random non-coordinate split,
  (p, d) in {(13,4), (31,6), (11,2), (37,9), (13,3)}, with the trial cap of (F3) at B = 20.
  Every returned s (211 of 360 runs) is nonzero and satisfies sum s_i^d lambda_i = 0 exactly,
  Y lies in D^M, every sub-solver's y is in the kernel of its sub-bank, and the top output is 0.
  The aborts are at deliberately undersized arities (beta_j > 1 there).
- **[F] Monte Carlo (not exact).** At two parameter sets where the node abort bound
  sum_j n_j beta_j + 3 nu 2^-B is nontrivial (0.083 and 0.040), 0/150 node aborts each.
- **[E] counting.** nu = sum_j prod_{i>j} M_i <= (M-1)/(min M_j - 1) <= M-1 and
  nu <= 2 prod_{j>=2} M_j for k <= 5 and 2 <= M_j <= 6; beta(M, 1; g) > 1 for g >= 1.

These check finite cases and displayed identities, not the proposition.

## 5. Exact statement proved

Access model and hypotheses: those of `thm:free-coordinate`(iii). Fresh ideal sources, so by
`lem:s3-law` the labels at each node are i.i.d. uniform on the unknown K_d^perp, given the
earlier record. The algorithm knows only (p, d, g_d, m, c, eps) and the public split.

1. (`lem:fc-split-law`) For labels i.i.d. uniform on any subspace V of dimension a and any public
   split pi_1..pi_k (g_j >= 1, trivial common kernel):
   (a) a_j = dim pi_j(V_{j-1}) <= g_j and sum_j a_j = a;
   (b) on EVERY bank, if no sub-solver aborts, then Y in D^M \ {0}, Lambda Y = 0 and
       s^d = Y;
   (c)-(d) given the record of the first t sub-solvers and no abort, the next sub-bank has
       i.i.d. columns uniform on pi_j(V_{j-1}).
2. (`prop:fc-split-node`) At a grade with 2 <= kappa_d < p-1: node abort <=
   sum_j n_j (beta(M_j, n_0^(j); g_j) + 3 2^-B); exact output rho_{H_{d-1}} on every non-aborting
   record; trials <= sum_j n_j ceil(2B ln2 q^-g_j) <= nu (2B ln2 kappa^{max g_j} + 1), with
   nu <= M - 1.
3. (`prop:fc-split`) Theorem free-coordinate (iii) holds with any public set of split grades,
   targets sum_j n_{d,j} beta_{d,j} <= tau_d chosen top level first, and N = S sum_d n_d nu_d:
   success >= 1 - eps from c S prod_d M_d queries; explicit arities from `lem:fc-choice` with
   tau_{d,j} = tau_d/(k_d n_{d,j}); time Q (2 + 2B ln2 max_d kappa_d^{g_{d*}}) poly + Q t_S1.

Strongest baseline: unsplit FCS (k_d = 1), recovered exactly; its per-node cap is
kappa_d^{g_d}. Prop `rc-lower`'s q^{-a} bound does not apply (split nodes read the bank).

## 6. What is still missing

- Human review of the new subsection and of Appendices B and F (C in the current lettering),
  which it reuses.
- No exact query/time numbers for split schedules at the class-9 profile in this pass. The
  11-02 report's "capping trials at 2^30 per node costs +2.5 to +11 bits of queries" came from
  its own script and was not re-derived here; the proposed paper text quotes no numbers.
- The optimisation over k_d is not done. Heuristically, log Q grows like k c log m while the
  time exponent falls like (g/k) log kappa, which suggests 2^{O(sqrt(c g log kappa log m))} at the
  best k. That is NOT claimed or proved; it needs the arity bound of (i) tracked through
  n_d and tau_d.
- Splits are only analysed inside Theorem free-coordinate (iii). Part (ii) (constant arity 4u,
  tree restarts) with split nodes is not treated.
- [D] and [F] are random runs, not exhaustive; [F] is Monte Carlo.

## 7. Claim gates that must stay false

- Polynomial classical time for Schedule 3 (split or not). Split nodes still cost
  2^{Theta(ceil(g_d/k) log kappa_d)} per sub-solver, and queries grow with k.
- "Per-node cost about kappa^{g_d/k}" read as the whole node: the node cost carries the factor
  nu_d < M_d.
- Any lower bound or optimality claim for split nodes; Prop `rc-lower` covers only
  bank-oblivious designs, and the open question at arity a + O(1) is untouched.
- Any guarantee for fixed, adversarial or correlated banks; the law is for the i.i.d. supply.
- The law statement for sub-solvers that read more than the pi_j-images of their own inputs,
  or that share an input between two parents (counterexample [C]).
- Anything at the zero-sum grade kappa_d = p - 1 (h = 1).
- Rees manuscript-level gates in STATE.md (verified result, new mechanism, outreach) all stay
  false; this is an AI-only pass.

## 8. Proposed paper text

**Status label: AI-checked, pending human review.** Not applied (this pass edits no other file).

### 8.1 Target 1: new subsection at the end of Appendix F

File `docs/papers/rees-hsp/appendix-free-coordinate.tex` (label `app:free-coordinate`; called
Appendix F in STATE.md and the free-coordinate report, lettered C in the current input order).
Append after the final `\paragraph{Scope.}` paragraph. Same text as
`2026-11-03-rees-block-splitting/fc_split_subsection.tex`. Macros: only `\Fp`, `\eps`, `\poly`,
`\hh`, `\file` from main.tex, plus amsmath/enumitem as already loaded.

```latex
% Proposed new subsection for the end of appendix-free-coordinate.tex (after \paragraph{Scope.}).
% Source: research/audits/reviews/2026-11-03-rees-block-splitting.md, which re-derives
% research/audits/reviews/2026-11-02-rees-schedule3-cost.md Lemma 5.2 and Proposition 5.3.
% Exact checks: research/audits/reviews/2026-11-03-rees-block-splitting/block_split_check.py
% (law transfer and joint level-2 law exhaustively in small cases; end-to-end witnesses;
% counting identities). They check finite cases, not the proposition.
% Macros: only those defined in main.tex (\Fp, \eps, \poly, \file).

\subsection{Splitting the public coordinates}
\label{app:fc-split}

\paragraph{Status.} \emph{AI-checked, pending human review.} This subsection proves the block-splitting refinement stated after Proposition~\ref{prop:rc-lower}. It changes only the classical computation inside a node; the instruments, the conversion and the tree are those of Sections~\ref{app:fc-setting}--\ref{app:fc-mixed}.

Fix a grade $d$ with $2 \le \kappa_d < p-1$, so $h \ge 2$, and keep $\kappa$, $h$, $P_\kappa$, $D$, $q$, $\alpha$ and $\beta(\cdot,\cdot;\cdot)$ of Section~\ref{app:fc-setting}. A \emph{split} of $\Fp^{g_d}$ is a list of public linear maps $\pi_j \colon \Fp^{g_d} \to \Fp^{g_j}$, $j = 1,\dots,k$, with $k \ge 1$, every $g_j \ge 1$ and $\ker\pi_1 \cap \cdots \cap \ker\pi_k = 0$. The basic example partitions the coordinates of $\Fp^{g_d}$, that is, the public coordinates of $\gamma_d$, into $k$ blocks of sizes $g_1 + \cdots + g_k = g_d$ and lets $\pi_j$ be the projection onto block $j$. For $k = 1$ and $\pi_1$ the identity, everything below reduces to Sections~\ref{app:fc-setting}--\ref{app:fc-node}.

Fix public integers $M_j \ge n_0^{(j)} \ge 1$ and $B \ge 1$, and put
\[
  M = \prod_{j=1}^k M_j, \qquad n_j = \prod_{i=j+1}^{k} M_i \quad (n_k = 1), \qquad \nu = \sum_{j=1}^k n_j .
\]
Index the $M$ columns by tuples $\iota = (i_1,\dots,i_k)$ with $1 \le i_j \le M_j$. For $0 \le j \le k$, a \emph{level-$j$ index} is a tuple $\eta = (i_{j+1},\dots,i_k)$; level-$0$ indices are columns, and the only level-$k$ index is the empty tuple $()$. There are $n_j$ level-$j$ indices for $j \ge 1$. For a level-$j$ index $\eta$ with $j \ge 1$ and $1 \le l \le M_j$, $(l,\eta)$ is a level-$(j-1)$ index.

\paragraph{The split node.} A node of degree $d$ receives $M$ registers on $G_d$ and does the following.
\begin{enumerate}[label=(K\arabic*),leftmargin=3em]
  \item As (F1): record the bank $\lambda_\iota$, and put $z_\iota = \lambda_\iota$ for every column $\iota$.
  \item For $j = 1,\dots,k$, and for the level-$j$ indices $\eta$ in lexicographic order, run the \emph{sub-solver} $\eta$. It reads the sub-bank
  \[
    \Lambda_\eta = \bigl[\pi_j(z_{(1,\eta)}) \;\cdots\; \pi_j(z_{(M_j,\eta)})\bigr] \in \Fp^{g_j\times M_j}
  \]
  and runs (F2) (without the rank guard of part~(ii)), (F3), and the root extractions of (F4), with $(M_j, n_0^{(j)}, B)$ in place of $(M, n_0, B)$, $g_j$ in place of $g_d$, and $\Lambda_\eta$ in place of $\Lambda$, with its own caps and fresh coins. If it aborts, the node aborts. Otherwise it returns $y^\eta \in D^{M_j}$ and $\sigma^\eta \in \Fp^{M_j}$ with $(\sigma^\eta_l)^\kappa = y^\eta_l$ and $\sigma^\eta_l = 0$ exactly when $y^\eta_l = 0$. Put $z_\eta = \sum_{l=1}^{M_j} y^\eta_l\, z_{(l,\eta)} \in \Fp^{g_d}$.
  \item For each column $\iota = (i_1,\dots,i_k)$ put
  \[
    Y_\iota = \prod_{j=1}^k y^{(i_{j+1},\dots,i_k)}_{i_j}, \qquad
    \theta_\iota = \prod_{j=1}^k \sigma^{(i_{j+1},\dots,i_k)}_{i_j},
  \]
  and $s_\iota = \theta_\iota^\alpha$ if $\theta_\iota \ne 0$, $s_\iota = 0$ otherwise.
  \item As (F5): check exactly that $s \ne 0$ and $\sum_\iota s_\iota^d\lambda_\iota = 0$; abort otherwise.
  \item As (F6): apply the conversion of Proposition~\ref{prop:descent} with witness $s$ and output its register on $G_{d-1}$.
\end{enumerate}
Order the sub-solvers as in (K2), $v_1,\dots,v_\nu$; all of level $j-1$ run before any of level $j$. The vectors $z_\eta$ are computed from the measured labels, so (K2)--(K4) are a classical randomized map from the bank and fresh coins to a record, and they consume no quantum source. Each sub-solver reads only the $\pi_j$-images of its own $M_j$ inputs, and each $z_\eta$ is read by exactly one sub-solver, or by none if $j = k$. The node is not bank-oblivious in the sense of Proposition~\ref{prop:rc-lower}: the coordinates chosen at level $j \ge 2$ depend on the sub-banks of level $j-1$.

\begin{lemma}[Split banks]
\label{lem:fc-split-law}
Let the labels $\lambda_\iota$ be independent and uniform on a subspace $V \le \Fp^{g_d}$ of dimension $a$. Put $V_0 = V$, $V_j = V \cap \ker\pi_1 \cap \cdots \cap \ker\pi_j$ and $a_j = \dim V_{j-1} - \dim V_j$.
\begin{enumerate}[label=(\alph*),leftmargin=2em]
  \item $V_k = 0$, $a_j = \dim\pi_j(V_{j-1}) \le g_j$, and $a_1 + \cdots + a_k = a$.
  \item \emph{Witness, for every bank.} If no sub-solver aborts, then $\pi_i(z_\eta) = 0$ for every level-$j$ index $\eta$ and every $i \le j$, $z_{()} = \sum_\iota Y_\iota\lambda_\iota = 0$, $Y \in D^M\setminus\{0\}$, and $s_\iota^d = Y_\iota$ for every $\iota$. In particular (K4) always passes when it is reached.
  \item \emph{Law.} Let $\mathcal{R}_t$ be the record of $v_1,\dots,v_t$ (their sub-banks, coins and outcomes) and $\mathcal{E}_t$ the event that none of them aborts. Call a vector $z_\eta$ \emph{open} after $t$ steps if it has been defined and is not read by $v_1,\dots,v_t$; labels count as level-$0$ vectors. Conditional on any value of $\mathcal{R}_t$ in $\mathcal{E}_t$, the open vectors are independent, and an open vector of level $j$ is uniform on $V_j$.
  \item Consequently, conditional on any value of $\mathcal{R}_t$ in $\mathcal{E}_t$, if $v_{t+1}$ has level $j$, its sub-bank has $M_j$ independent columns, each uniform on the subspace $\pi_j(V_{j-1})$ of dimension $a_j \le g_j$, and its coins are fresh.
\end{enumerate}
\end{lemma}

\begin{proof}
(a) Since $V_j = V_{j-1} \cap \ker\pi_j$, the restriction of $\pi_j$ to $V_{j-1}$ has kernel $V_j$, so $a_j = \dim\pi_j(V_{j-1}) \le g_j$. The sum telescopes to $\dim V_0 - \dim V_k$, and $V_k \subseteq \ker\pi_1\cap\cdots\cap\ker\pi_k = 0$.

(b) Let $\eta$ be a level-$j$ sub-solver that does not abort. Its acceptance in (F3) gives $\Lambda_\eta y^\eta = 0$, as in the proof of Lemma~\ref{lem:fc-node}(d): every row of $R_\eta y^\eta$ vanishes, for the echelon form $R_\eta$ of $\Lambda_\eta$, and row operations do not change the kernel. That proof also gives $y^\eta \ne 0$, $y^\eta_l \in D$, and the stated properties of $\sigma^\eta$; none of this uses the law of the bank. Now induct on $j$; level $0$ has nothing to prove. Linearity gives
\[
  \pi_j(z_\eta) = \sum_{l} y^\eta_l\,\pi_j(z_{(l,\eta)}) = \Lambda_\eta y^\eta = 0,
\]
and $\pi_i(z_\eta) = \sum_l y^\eta_l\pi_i(z_{(l,\eta)}) = 0$ for $i < j$ by induction. Unwinding the definition of $z_\eta$ level by level gives $z_{()} = \sum_\iota Y_\iota\lambda_\iota = \Lambda Y$, and $z_{()}$ lies in every $\ker\pi_i$, hence is $0$. Each $Y_\iota$ is a product of elements of $D$, and $D\cdot D \subseteq D$ because $P_\kappa$ is a subgroup of $\Fp^\times$; so $Y \in D^M$. To see $Y \ne 0$, choose $i_k$ with $y^{()}_{i_k} \ne 0$, then $i_{k-1}$ with $y^{(i_k)}_{i_{k-1}} \ne 0$, and so on down to $i_1$; every factor of $Y_{(i_1,\dots,i_k)}$ is then nonzero. Finally $\theta_\iota^\kappa = Y_\iota$, and $\theta_\iota = 0$ exactly when $Y_\iota = 0$, so $s_\iota^d = Y_\iota$ by~\eqref{eq:s3-bezout}. Hence $\sum_\iota s_\iota^d\lambda_\iota = \Lambda Y = 0$, and $s \ne 0$.

(c) Induction on $t$. For $t = 0$ the open vectors are the labels, independent and uniform on $V_0$. Assume the claim for $t$, and let $v_{t+1}$ be the sub-solver $\eta$ of level $j$. Its inputs $u_l = z_{(l,\eta)}$, $l = 1,\dots,M_j$, are open after $t$ steps, because all of level $j-1$ precedes $v_{t+1}$ and only $v_{t+1}$ reads them. Fix a value of $\mathcal{R}_t$ in $\mathcal{E}_t$, and let $O$ be the family of the other open vectors. By hypothesis, $u_1,\dots,u_{M_j}$ and the members of $O$ are independent, and each $u_l$ is uniform on $V_{j-1}$.

Choose a complement $W$ of $V_j$ in $V_{j-1}$. Then $\pi_j$ is injective on $W$, because $W \cap \ker\pi_j \subseteq V_{j-1}\cap\ker\pi_j \cap W = V_j \cap W = 0$. The map $V_j \times W \to V_{j-1}$, $(u', u'') \mapsto u' + u''$, is a linear bijection, so writing $u_l = u'_l + u''_l$ with $u'_l \in V_j$ and $u''_l \in W$, the vectors $u'_1, u''_1, \dots, u'_{M_j}, u''_{M_j}$ and the members of $O$ are independent, and each $u'_l$ is uniform on $V_j$. The sub-bank is $\Lambda_\eta = [\pi_j(u''_1)\cdots\pi_j(u''_{M_j})]$, and it determines $u''_1,\dots,u''_{M_j}$, since $\pi_j$ is injective on $W$. The new part $r$ of the record consists of $\Lambda_\eta$, the fresh coins $\omega$ of $v_{t+1}$ and its outcome. It is a function of $(u''_1,\dots,u''_{M_j},\omega)$, it determines $(u''_1,\dots,u''_{M_j},\omega)$, and $\omega$ is independent of everything else. Condition further on a value of $r$ in which $v_{t+1}$ does not abort. This fixes $u''$, $\omega$ and $y^\eta \ne 0$, and leaves $u'_1,\dots,u'_{M_j}$ and $O$ independent with unchanged laws. Now $\sum_l y^\eta_lu''_l \in W$ and $\pi_j\bigl(\sum_ly^\eta_lu''_l\bigr) = \Lambda_\eta y^\eta = 0$, so $\sum_ly^\eta_lu''_l = 0$ and
\[
  z_\eta = \sum_l y^\eta_l\,u'_l .
\]
Choose $l_0$ with $y^\eta_{l_0} \ne 0$. Given the $u'_l$ with $l \ne l_0$ and $O$, the vector $y^\eta_{l_0}u'_{l_0}$ is uniform on $V_j$, so $z_\eta$ is uniform on $V_j$ and independent of $O$. The open vectors after $t+1$ steps are the members of $O$ and $z_\eta$, which proves the claim for $t+1$.

(d) By~(c) the inputs of $v_{t+1}$ are independent and uniform on $V_{j-1}$, conditional on $\mathcal{R}_t$. A linear map sends the uniform law on $V_{j-1}$ to the uniform law on its image, so the columns of $\Lambda_\eta$ are independent and uniform on $\pi_j(V_{j-1})$, which has dimension $a_j \le g_j$ by~(a). The coins of $v_{t+1}$ are drawn after $\mathcal{R}_t$.
\end{proof}

As in Remark~\ref{rem:s3-caveat}, a sub-bank is not i.i.d.\ given its own acceptance. The proof does not need that. Acceptance depends only on the components $u''_l$ that the sub-solver reads, while the law of its output comes from the components $u'_l$, which it never reads. The hypothesis that a sub-solver reads only the $\pi_j$-images of its inputs is needed. A sampler that also reads the full inputs can bias $z_\eta$. For example, take $p = 5$, $\kappa = 2$, $V = \Fp^2$, the split $\pi_1$, $\pi_2$ into the two coordinates, $M_1 = 2$ and $n_0^{(1)} = 1$, so that $V_1 = 0\times\Fp$. Call $y$ \emph{acceptable} for a level-$1$ sub-bank if (F3) can accept it: $y_l \in P_\kappa$ on the free columns, $y_{p_i} \in D$ on the pivots and $y_l = 0$ elsewhere. Let the sampler output the lexicographically first acceptable $y$ whose output $z_\eta$ has second coordinate $0$, and the lexicographically first acceptable $y$ if there is none. Conditional on the sub-solver not aborting, $z_\eta = 0$ then has probability $69/325 \ne 1/5$ (exact enumeration, \file{research/audits/reviews/2026-11-03-rees-block-splitting/}). So $z_\eta$ is not uniform on $V_1$. The witness of Lemma~\ref{lem:fc-split-law}(b) remains valid; only the law fails. Reusing one output in two sub-solvers would break the independence in~(c) in the same way.

\begin{proposition}[One split node]
\label{prop:fc-split-node}
Let a node of degree $d$ with $h \ge 2$ receive the state $\rho_{H_d}^{\otimes M}\otimes\omega_X$, for any system $X$, and run (K1)--(K5). Put $\beta_j = \beta(M_j, n_0^{(j)}; g_j)$.
\begin{enumerate}[label=(\alph*),leftmargin=2em]
  \item The node aborts with probability at most $\sum_{j=1}^k n_j\bigl(\beta_j + 3\cdot 2^{-B}\bigr)$.
  \item Every record that reaches (K4) passes it. On every record that does not abort, the output register is exactly $\rho_{H_{d-1}}$ on $G_{d-1}$, and the joint state of the record, the output and $X$ has the form displayed in Lemma~\ref{lem:s3-node}(d).
  \item The node uses at most $\sum_j n_j\lceil 2B\ln 2\cdot q^{-g_j}\rceil \le \nu\,(2B\ln 2\cdot\kappa^{g_*} + 1)$ trials, where $g_* = \max_jg_j$, and at most $(\nu + \sum_jn_j\lceil 2B\ln2\cdot q^{-g_j}\rceil)\cdot\poly(g_d, M, B, \kappa, \log p)$ bit operations, with an absolute exponent. It consumes no quantum source after (K1). If every $M_j \ge 2$, then $\nu \le (M-1)/(\min_jM_j - 1) \le M-1$ and $\nu \le 2\prod_{j\ge2}M_j$. Every $M_j \ge 2$ holds whenever every $\beta_j \le 1$.
\end{enumerate}
\end{proposition}

\begin{proof}
(a) By Lemma~\ref{lem:s3-law}, the labels are independent and uniform on $K_d^\perp$, which has dimension $a_d$, and independent of $X$. Apply Lemma~\ref{lem:fc-split-law} with $V = K_d^\perp$; since the labels and all coins are independent of $X$, every statement below also holds conditional on $X$. By Lemma~\ref{lem:fc-split-law}(b), the node aborts only if some sub-solver aborts. As in Lemma~\ref{lem:s3-tree}(b),
\[
  \Pr[\text{some sub-solver aborts}] \le \sum_{t=0}^{\nu-1}\Pr[v_{t+1}\ \text{aborts}\mid\mathcal{E}_t],
\]
with terms of probability zero omitted. Let $v_{t+1}$ have level $j$. By Lemma~\ref{lem:fc-split-law}(d), conditional on any value of $\mathcal{R}_t$ in $\mathcal{E}_t$, its sub-bank has $M_j$ independent columns uniform on a subspace of dimension $a_j \le g_j$, and its coins are fresh. The proofs of Lemma~\ref{lem:fc-node}(a)--(c) use nothing else about the bank. They use only Lemmas~\ref{lem:fc-rref} and~\ref{lem:fc-moment}, which assume exactly this law, and the fresh coins. Applied to $\Lambda_\eta$ with $(g_j, M_j, n_0^{(j)}, a_j)$ in place of $(g_d, M, n_0, a_d)$, and without the last two sentences of the proof of Lemma~\ref{lem:fc-node}(c), which concern (F5) and are replaced by Lemma~\ref{lem:fc-split-law}(b), they bound the conditional abort probability by $\beta(M_j, n_0^{(j)}; a_j) + 3\cdot 2^{-B}$, and $\beta(M_j, n_0^{(j)}; a_j) \le \beta_j$ because $\beta$ increases with $a$. There are $n_j$ sub-solvers of level $j$.

(b) The first claim is Lemma~\ref{lem:fc-split-law}(b). The rest is the proof of Lemma~\ref{lem:fc-node}(d) word for word. (K2)--(K4) are a classical randomized map from the bank and fresh coins to a record which, unless the node aborts, contains a valid nonzero witness $s$. Proposition~\ref{prop:descent} maps the post-measurement registers to $\rho_{H_{d-1}}$ for every positive-probability label tuple and every such witness.

(c) A level-$j$ sub-bank has $g_j$ rows, so its observed rank is $r \le g_j$ for every record, and its trial cap is $\lceil 2B\ln 2\cdot q^{-r}\rceil \le \lceil 2B\ln 2\cdot q^{-g_j}\rceil \le 2B\ln 2\cdot\kappa^{g_j} + 1$ by~\eqref{eq:fc-q}. Each sub-solver costs $(1 + T_r)\cdot\poly(g_j, M_j, B, \kappa, \log p)$ by Lemma~\ref{lem:fc-node}(e). Forming $\Lambda_\eta$ and $z_\eta$ costs $O(g_jg_dM_j + g_dM_j)$ further operations. Steps (K3) and (K4) cost $O(kM)$ multiplications, $M$ exponentiations and one $g_d\times M$ product. For the count, $\nu$ satisfies $\nu = 1$ for $k = 1$ and $\nu = 1 + M_k\,\nu'$, where $\nu'$ is the count for $(M_1,\dots,M_{k-1})$. With $m_* = \min_jM_j \ge 2$ and $M' = M/M_k$, induction gives
\[
  \nu \le 1 + M_k\,\frac{M'-1}{m_*-1} = \frac{M - 1 - (M_k - m_*)}{m_*-1} \le \frac{M-1}{m_*-1},
\]
and $n_j \le 2^{-(j-1)}\prod_{i\ge2}M_i$ gives $\nu \le 2\prod_{i\ge2}M_i$. Finally, if $n_0^{(j)} = 1$ then $\beta_j \ge 4q^{-g_j} \ge 4$. So $\beta_j \le 1$ forces $M_j \ge n_0^{(j)} \ge 2$.
\end{proof}

\begin{proposition}[Split schedule; AI-checked, pending human review]
\label{prop:fc-split}
Theorem~\ref{thm:free-coordinate}(iii) remains true with the following changes, for any public choice of the grades that are split. At a grade $d \in \Gamma_{\mathrm F}$ that is split, (R1) chooses a public split $(\pi_{d,j})_{j \le k_d}$ with output dimensions $g_{d,j} \ge 1$. It then chooses integers $M_{d,j} \ge n_0^{(d,j)} \ge 1$ in the order $j = k_d, k_d-1, \dots, 1$, from public data and the arities already chosen only, such that
\begin{equation}
  \label{eq:fc-split-target}
  \sum_{j=1}^{k_d} n_{d,j}\,\beta\bigl(M_{d,j}, n_0^{(d,j)}; g_{d,j}\bigr) \le \tau_d, \qquad n_{d,j} = \prod_{i=j+1}^{k_d}M_{d,i},
\end{equation}
and puts $M_d = \prod_jM_{d,j}$. Its nodes run (K1)--(K5). Put $\nu_d = \sum_jn_{d,j}$ at split grades and $\nu_d = 1$ at the other grades of $\Gamma_{\mathrm F}$, and let (R2) use $N = S\sum_{d\in\Gamma_{\mathrm F}}n_d\nu_d$. Then the recursion returns $\hh$ with probability at least $1-\eps$ from $Q = c\,S\prod_dM_d$ oracle queries. At split grades, (i) and~(ii) replace the arity and time statements of the theorem.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item \emph{Explicit choice.} For $j = k_d,\dots,1$, put $\tau_{d,j} = \tau_d/(k_dn_{d,j})$, and take $n_0^{(d,j)}$ and $M_{d,j}$ from Lemma~\ref{lem:fc-choice} with $(g_{d,j}, \tau_{d,j})$ in place of $(g_d, \tau)$. This satisfies~\eqref{eq:fc-split-target}, and
  \[
    M_{d,j} \le g_{d,j}\Bigl(1 + \frac{2\ln\kappa_d}{\ln(p/\kappa_d)}\Bigr) + \frac{3\ln(8/\tau_{d,j})}{\ln(p/\kappa_d)} + 3 .
  \]
  \item \emph{Cost.} Each sub-solver at a split grade uses at most $2B\ln 2\cdot\kappa_d^{\,g_{d,j}} + 1$ trials, and a node at most $\nu_d(2B\ln 2\cdot\kappa_d^{\,g_{d*}} + 1)$, where $g_{d*} = \max_jg_{d,j}$ and $\nu_d \le M_d - 1$. The classical time is at most
  \[
    Q\cdot\Bigl(2 + 2B\ln 2\cdot\max_{d\in\Gamma_{\mathrm F}}\kappa_d^{\,g_{d*}}\Bigr)\cdot\poly\bigl(\max_dM_d, B, c, \log p\bigr) + Q\cdot t_{\mathrm{S1}},
  \]
  with $B \le \log_2(27Q/\eps) + 1$, $t_{\mathrm{S1}}$ as in Proposition~\ref{prop:fc-uniform}(b), and $g_{d*} = g_d$ at unsplit grades. With $k_d \le g_d$ coordinate blocks of sizes $\lfloor g_d/k_d\rfloor$ or $\lceil g_d/k_d\rceil$, the exponent $g_{d*}\log\kappa_d$ is $\lceil g_d/k_d\rceil\log\kappa_d$ in place of $g_d\log\kappa_d$. In exchange, the arity is a product of $k_d$ factors, each bounded as in~(i).
\end{enumerate}
\end{proposition}

\begin{proof}
Lemma~\ref{lem:fc-forest}(a) is an induction over nodes. At an FCS node it uses only Lemma~\ref{lem:fc-node}(d), and the fact that the node's record is a classical randomized function of its bank and fresh coins. Proposition~\ref{prop:fc-split-node}(b) and the paragraph after (K5) give both for a split node. So Lemma~\ref{lem:fc-forest}(a) holds for the modified procedure, and in particular every split node receives $\rho_{H_d}^{\otimes M_d}$ in product with the earlier record. In Lemma~\ref{lem:fc-forest}(b), the term of a split node of grade $d$ is then at most
\[
  \sum_jn_{d,j}\beta\bigl(M_{d,j}, n_0^{(d,j)}; g_{d,j}\bigr) + 3\nu_d\cdot 2^{-B} \le \tau_d + 3\nu_d\cdot 2^{-B}
\]
by Proposition~\ref{prop:fc-split-node}(a) and~\eqref{eq:fc-split-target}. An unsplit FCS node contributes at most $\tau_d + 3\cdot 2^{-B}$, as before. There are $Sn_d$ nodes of grade $d$, so the abort probability is at most
\[
  \sum_{d\in\Gamma_{\mathrm F}}Sn_d\tau_d + 3N\cdot 2^{-B} \le \frac{\eps}{9} + \frac{\eps}{9} .
\]
Here $\tau_d = \eps/(9(c-1)Sn_d)$ with $n_d = \prod_{2\le d'<d}M_{d'}$ computed from the arities $M_{d'}$ of (R1), split or not, and $B = \lceil\log_2(27N/\eps)\rceil$. The rest of the proof of Theorem~\ref{thm:free-coordinate}(iii) is unchanged. It uses Lemma~\ref{lem:fc-forest}, the tree shape ($P = \prod_dM_d$ leaves and $Sn_d$ nodes of grade $d$) and the instrument count $N_{\mathrm{instr}} = S(P + \sum_dn_d(M_d+1) + 1)$. A split node still applies $M_d$ central instruments and one conversion, and its sub-solvers are classical. The query count is $c$ per leaf.

(i) Since $\tau_{d,j} \le \tau_d \le 1$, Lemma~\ref{lem:fc-choice} gives $\beta(M_{d,j}, n_0^{(d,j)}; g_{d,j}) \le \tau_{d,j}$ and the displayed bound. Its proof uses $g_d$ only as the dimension argument of $\beta$, so it applies with $g_{d,j}$. Each $\tau_{d,j}$ depends only on the arities $M_{d,i}$, $i > j$, which are already chosen, and $\sum_jn_{d,j}\tau_{d,j} = \tau_d$.

(ii) The trial bounds are Proposition~\ref{prop:fc-split-node}(c). Since $\tau_d < 1$, every $\beta_{d,j} \le 1$, so every $M_{d,j} \ge 2$ and $\nu_d \le M_d - 1$. Hence $n_d\nu_d < n_dM_d$, and the number of sub-solvers, unsplit FCS nodes, Schedule-1 nodes and linear nodes over the run is less than $S\sum_dn_dM_d \le (c-1)SP < Q$, using $n_dM_d \le P$. In particular $N < Q$, which gives the bound on $B$. Each sub-solver costs $(1 + T_r)\cdot\poly$ by Proposition~\ref{prop:fc-split-node}(c), and the other nodes cost as in the proof of Proposition~\ref{prop:fc-uniform}(b). The factor $\poly(g_d,\dots)$ is absorbed into $\poly(\max_dM_d,\dots)$. Indeed, $\beta_{d,j} \le 1$ forces $n_0^{(d,j)} \ge 2$ and, through the second term of~\eqref{eq:fc-beta}, $M_{d,j} - n_0^{(d,j)} \ge g_{d,j} - 1$. So $M_{d,j} \ge g_{d,j} + 1$, and $M_d \ge 1 + \sum_jg_{d,j} > g_d$, because a split has $\sum_jg_{d,j} \ge g_d$.
\end{proof}

At $k_d = 1$, Proposition~\ref{prop:fc-split} is Theorem~\ref{thm:free-coordinate}(iii). Splitting trades queries for classical time. The per-sub-solver trial cap falls from about $\kappa_d^{\,g_d}$ to about $\kappa_d^{\lceil g_d/k_d\rceil}$. The arity grows from about $g_d$ to a product of $k_d$ factors of about $g_d/k_d + O(\log(1/\tau_{d,j})/\log(p/\kappa_d))$ each. For fixed $c$ and fixed $k_d$ the query count stays polynomial in $m$ and $\log(1/\eps)$, as in Proposition~\ref{prop:fc-uniform}(b), but the bound on its degree grows with $k_d$. Proposition~\ref{prop:rc-lower} does not apply to split nodes, because they read the bank between levels. The open question stated after it concerns arity $a + O(1)$, which split nodes with $k_d \ge 2$ do not reach, so it is not addressed here.
```

### 8.2 Target 2: one-line change to the body sentence

File `docs/papers/rees-hsp/main.tex`, line 590 (the paragraph after `prop:rc-lower`, one source
line). Replace the whole line by (also in `2026-11-03-rees-block-splitting/newline590.txt`):

```latex
Algorithms that read the bank before choosing coordinates are not covered. Splitting the public coordinates of $\gamma_d$ into $k$ blocks and solving them in turn keeps the label law at each level: given everything read so far, the outputs of level $j$ are independent and uniform on $K_d^\perp \cap \ker\pi_1 \cap \dots \cap \ker\pi_j$. With blocks of sizes $\lfloor g_d/k\rfloor$ or $\lceil g_d/k\rceil$, each of the fewer than $M_d$ sub-solvers of a node then needs at most $2B\ln 2\cdot\kappa^{\lceil g_d/k\rceil} + 1$ trials, at arity $M_d = \prod_j M_j$ (Proposition~\ref{prop:fc-split} in Appendix~\ref{app:fc-split}; AI-checked, pending human review). Whether some method finds a witness in time $\kappa^{a-\Omega(a)}$ at arity $a + O(1)$ is open.
```

Differences from the current line: it names the level-j subspace exactly, says the
kappa^{ceil(g_d/k)} cap is per sub-solver (fewer than M_d of them per node), and cites
Proposition `prop:fc-split` in place of "not proved in the appendices".

Optional consistency edit (not required): `appendix-free-coordinate.tex` Section
`app:fc-numbers`(a) says "(no block splitting)"; it stays correct.

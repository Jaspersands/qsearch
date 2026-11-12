# Patch: headline class-9 exponent 145 → 53 (Schedule 1 at depth ⌈log₂ t_d⌉)

AI-prepared (2026-11-12) and NOT applied. AI-checked, pending human review.

Report: `research/audits/reviews/2026-11-12-rees-headline-53.md`.

Line numbers are those of the working tree on 2026-11-12. Part A is the core,
`docs/papers/rees-hsp/core/main-core.tex`. Part B is the full version,
`docs/papers/rees-hsp/main.tex` and its appendices.

Each item gives the exact OLD text, a substring unique in its line, and the NEW text.
"OLD … NEW" blocks are LaTeX. Apply Part A first: Part B reuses its lemma texts.

## Design

These choices are fixed throughout, and the integrator should check them before
applying anything.

1. **Arity.** The symbol `B_d(a)` is redefined with an implicit dependence on p:
   `B_d(a) = a+1` if κ_d = 1, and `G(κ_d,a)^{L_d}` otherwise, with
   L_d = ⌈log₂ t_{p,κ_d}⌉.
   - The published arity becomes `\bar B_d(a) = G(d,a)^{⌈log₂(d+1)⌉}`.
   - Every corollary that writes `B_d(L)` or "B_d is increasing" stays literally
     valid. B_d is still nondecreasing in a, and p is fixed in each call.
   - `B_d ≤ \bar B_d` keeps every old bound available as an upper bound.
2. **Import.** `thm:is-import` is cut down to IS Theorem 11, the collision step. I
   re-read its statement in `research/audits/reviews/2026-11-02-rees-linear-arity/lit/is_1503.09016.txt`,
   ll. 439–442. J may be empty and I ≠ ∅.
   - The L-round accumulation (IS §3.3) is now proved in the body as `lem:rounds`,
     including the J = ∅ stop.
   - The public depth is `lem:zero-sum-length`.
   - The exponent is `lem:exponent`, which gives E_1(9) = 53.
3. **Randomness.** All randomness sits in a classical preprocessing step, done once
   per grade, before any query, depending only on (p, κ_d).
   - Given the zero sums, Schedule 1 is deterministic. So `rem:oblivious` ("no
     restarts"), the fixed N_QFT and the coherent receiver are untouched.
   - The preprocessing abort, at most ε/3, uses the third of the budget that the
     merges leave unused. The theorem total goes from 2ε/3 to ε. The statement
     "probability at least 1−ε" is unchanged.
4. **Ivanyos.** G. Ivanyos confirmed the full-depth bound C(d,a) ≤ G^{⌈log₂(d+1)⌉}.
   That bound is now a corollary of `lem:rounds` plus van de Woestijne, and the
   confirmation still corroborates it. It does **not** cover the shortened depth. Every
   place that cites the confirmation says so.
5. **Growth in c.** "grows like c² log c" becomes "grows at least quadratically in c".
   - The lower bound c(c+1)/2 is proved (Dirichlet). The upper bound
     1+Σ d⌈log₂(d+1)⌉ is trivial.
   - A Θ(c²) statement would need the divisor bound τ(n) = n^{o(1)}, which is not in
     the core bibliography. It is offered only for the full version (B19), where
     `HardyWright2008` exists, and the theorem number there is UNVERIFIED.

New citations used: `LidlNiederreiter1997` (Chevalley–Warning, already cited; Weil's
bound) and `Rabin1980` (already in both bibliographies). No new bib entries are needed in
the core.

---

## Part A — core (`core/main-core.tex`)

### A1. Abstract, l. 60

OLD:
```
the query separation is not new, the exponent of $m$ grows like $c^2\log c$, and no application is known.
```
NEW:
```
the query separation is not new, the exponent of $m$ grows at least quadratically in $c$, and no application is known.
```

### A2. Definition of the arity, l. 162 (tail) – l. 169

OLD (end of l. 162, then ll. 163–169):
```
For integers $d \ge 1$ and $a \ge 0$ put
\begin{equation}
  \label{eq:Bd}
  G(d,a) \coloneqq d^{d(d-1)/2}(a+1)^d,
  \qquad
  B_d(a) \coloneqq G(d,a)^{\lceil \log_2(d+1)\rceil},
\end{equation}
the sufficient Ivanyos--Santha arity for $a$ diagonal equations of degree $d$ (Theorem~\ref{thm:is-import}).
```
NEW:
```
For integers $d \ge 1$ and $a \ge 0$ and a prime $p$, put $\kappa_d \coloneqq \gcd(d,p-1)$ and
\begin{equation}
  \label{eq:Bd}
  G(d,a) \coloneqq d^{d(d-1)/2}(a+1)^d,
  \qquad
  B_d(a) \coloneqq
  \begin{cases}
    a+1, & \kappa_d = 1,\\
    G(\kappa_d,a)^{L_d}, & \kappa_d \ge 2,
  \end{cases}
  \qquad
  L_d \coloneqq \lceil \log_2 t_{p,\kappa_d}\rceil ,
\end{equation}
where, for $\kappa \ge 2$ dividing $p-1$, $t_{p,\kappa}$ is the least $t$ for which $z_1^\kappa + \cdots + z_t^\kappa = 0$ has a solution $z \in \Fp^t$, $z \ne 0$. This $B_d(a)$ is the arity of Schedule~1 (Section~\ref{sec:schedule1}) for $a$ diagonal equations of degree $d$. It depends on $p$ only through $\kappa_d$ and $L_d$, is computed from $(p,d,a)$ before the run (Lemma~\ref{lem:zero-sum-length}), is nondecreasing in $a$, and is at most the arity $\bar B_d(a) \coloneqq G(d,a)^{\lceil\log_2(d+1)\rceil}$ of~\cite[proof of Theorem~3]{IvanyosSantha2015} (Lemma~\ref{lem:bezout}).
```

### A3. thm:main(3), ll. 179–183

No textual change: `Q_q = c(m+τ)∏B_d(g_d)` and "with $B_d$ as in~\eqref{eq:Bd}" now
read with the new B_d. The integrator may optionally append to l. 183, after
`\eqref{eq:Bd}`:
```
 (so $Q_{\mathrm q}$ depends on $p$ through the $\kappa_d$ and $L_d$, and $Q_{\mathrm q} \le c\,(m+\tau)\prod_{d=2}^{c}\bar B_d(g_d)$)
```

### A4. thm:main(4), ll. 184–189

OLD:
```
  \item \emph{Explicit bound.} The count satisfies
  \[
    Q_{\mathrm q} \;\le\; C_c\, c\,(m+\tau)\,(m+1)^{\sum_{d=2}^c d\lceil\log_2(d+1)\rceil},
    \qquad
    C_c = \prod_{d=2}^c d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}.
  \]
```
NEW:
```
  \item \emph{Explicit bound.} The count satisfies
  \[
    Q_{\mathrm q} \;\le\; C_c\, c\,(m+\tau)\,(m+1)^{E_1(c)-1},
    \qquad
    C_c = \prod_{d=2}^c d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2},
  \]
  where $E_1(c) \le 1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ is the exponent of Lemma~\ref{lem:exponent}; $E_1(\ReesClassNineClass) = \ReesClassNineQueryExp$.
```
After `make_numbers.py`, `\ReesClassNineQueryExp` expands to 53.

### A5. Paragraph after thm:main, l. 195

OLD:
```
with arity $M_d = B_d(g_d)$ at every grade $d = 2,\dots,c$. For fixed $c$ the count $Q_{\mathrm q}$ is polynomial in $m$, and it does not depend on $p$ once $p \ge 3/\eps$, since then $\tau = 1$.
```
NEW:
```
with arity $M_d = B_d(g_d)$ at every grade $d = 2,\dots,c$, after a classical preprocessing that computes one zero sum of $\kappa_d$-th powers per grade (Lemma~\ref{lem:zero-sum-length}). For fixed $c$ the count $Q_{\mathrm q}$ is polynomial in $m$, uniformly in $p$: it is at most $c(m+\tau)\prod_{d=2}^c\bar B_d(g_d)$, which does not depend on $p$ once $p \ge 3/\eps$, since then $\tau = 1$.
```
Reason: the old "does not depend on p" is false for the new count.

### A6. rem:main-solver, l. 199

(a) OLD:
```
for any $M_d$ label columns in $\Fp^{g_d}$ and every prime $p > c$; it is deterministic; it runs in time
```
NEW:
```
for any $M_d$ label columns in $\Fp^{g_d}$ and every prime $p > c$; given the zero sums of the preprocessing, which depend only on $(p,\kappa_d)$ and are computed before any query, it is deterministic; it runs in time
```

(b) OLD:
```
That explicit $B_d$, and hence the exponent $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$, rests on the corrected arity bound of Remark~\ref{rem:is-printed} for~\cite{IvanyosSantha2015}, which G.~Ivanyos has confirmed (same remark).
```
NEW:
```
That explicit $B_d$, and hence the exponent $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$, rests on Lemma~\ref{lem:rounds}, which accumulates the collisions of~\cite[Theorem~11]{IvanyosSantha2015} with the shortest zero sum, on Lemma~\ref{lem:zero-sum-length} and on the exact computation of Lemma~\ref{lem:exponent}. G.~Ivanyos has confirmed the full-depth bound $C(d,a) \le G(d,a)^{\lceil\log_2(d+1)\rceil}$ of Remark~\ref{rem:is-printed}, which gives the weaker exponent $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ ($145$ at $c = 9$). His confirmation does not cover the shorter depth $L_d$, which is AI-checked only, pending human review.
```

### A7. l. 202

(a) OLD:
```
The exponent of $m$ grows like $c^2\log c$, so the bound is polynomial for each fixed $c$ and is not uniform in $c$; at $c = \ReesClassNineClass$ the exponent of $m$ in $Q_{\mathrm q}$ is at most $\ReesClassNineQueryExp$.
```
NEW:
```
The exponent $E_1(c)$ of $m$ lies between $c(c+1)/2$ and $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ (Lemma~\ref{lem:exponent}), so the bound is polynomial for each fixed $c$ and is not uniform in $c$; at $c = \ReesClassNineClass$ the exponent of $m$ in $Q_{\mathrm q}$ is at most $\ReesClassNineQueryExp$, for every prime $p > \ReesClassNineClass$.
```

(b) OLD:
```
Its only imported ingredients are Theorem~\ref{thm:is-import} (which itself uses van de Woestijne's deterministic solver for a single diagonal equation~\cite{vandeWoestijne2005}), the subgroup form
```
NEW:
```
Its only imported ingredients are Theorem~\ref{thm:is-import}, the collision step of Ivanyos and Santha; three standard facts on finite fields used in Lemma~\ref{lem:zero-sum-length}, namely the Chevalley--Warning theorem, Weil's bound for diagonal equations in two variables~\cite[Chapter~6]{LidlNiederreiter1997} and Las Vegas root finding~\cite{Rabin1980}; the subgroup form
```
`vandeWoestijne2005` remains cited in Section 5 (A9), so no bib entry is orphaned.

### A8. l. 220 and l. 228

l. 220 OLD:
```
the query separation of Section~\ref{sec:classical-query} is not new, the exponent of $m$ grows like $c^2\log c$, and no application
```
NEW:
```
the query separation of Section~\ref{sec:classical-query} is not new, the exponent of $m$ grows at least quadratically in $c$, and no application
```
l. 228 OLD:
```
The Ivanyos--Santha solver supplies the solutions for arbitrary labels at arity $B_d(g_d)$.
```
NEW:
```
The Ivanyos--Santha collision step, iterated $L_d$ times and closed with the shortest zero sum of $\kappa_d$-th powers, supplies the solutions for arbitrary labels at arity $B_d(g_d)$.
```

### A9. thm:is-import and the following paragraph, ll. 520–527

OLD (l. 520):
```
\begin{theorem}[Ivanyos--Santha {\cite[Theorem~11 and the proof of Theorem~3, Sections~3.1--3.3]{IvanyosSantha2015}}; imported, as read by AI sessions only (Remark~\ref{rem:is-import}(e)), pending human review]
```
NEW:
```
\begin{theorem}[Ivanyos--Santha {\cite[Theorem~11, Sections~3.1--3.2]{IvanyosSantha2015}}; imported, as read by AI sessions only (Remark~\ref{rem:is-import}(e)), pending human review]
```
OLD (l. 522):
```
Let $d \ge 1$ be fixed and let $p$ be a prime with $d \mid p-1$. With $G(d,a)$ and $B_d(a)$ as in~\eqref{eq:Bd}, there is a deterministic classical algorithm that, given any $\lambda_1,\dots,\lambda_M \in \Fp^a$ with $M \ge B_d(a)$, outputs explicit field elements $s_1,\dots,s_M$, not all zero, with $\sum_{i} s_i^d\lambda_i = 0$, in time polynomial in $M$ and $\log p$, where the polynomial depends on $d$.
```
NEW:
```
Let $d \ge 1$ be fixed and let $p$ be a prime with $d \mid p-1$, and put $G = G(d,a)$ as in~\eqref{eq:Bd}. There is a deterministic classical algorithm that, given any $v_1,\dots,v_G \in \Fp^a$, outputs disjoint subsets $I \ne \emptyset$ and $J$ of $\{1,\dots,G\}$ and explicit nonzero $\gamma_j \in \Fp$ $(j \in I \cup J)$ with $\sum_{i\in I}\gamma_i^d v_i = \sum_{j \in J}\gamma_j^d v_j$, in time polynomial in $G$ and $\log p$, where the polynomial depends on $d$.
```
The `J` of the theorem may be empty. This is the source's statement (arXiv v2, Theorem 11,
p. 8, AI-read).

OLD (l. 525, part):
```
Its Section~3.1 classifies field elements without nonresidues, and its last step uses van de Woestijne's deterministic solver for one equation in $d+1$ variables
```
NEW:
```
Its Section~3.1 classifies field elements without nonresidues, and the last step of its proof of Theorem~3, which Lemma~\ref{lem:rounds} replaces, uses van de Woestijne's deterministic solver for one equation in $d+1$ variables
```
OLD (l. 527):
```
Only the warm-up Propositions~9 and~10 of~\cite{IvanyosSantha2015} are randomized. The statement of Theorem~3 there does not say that the algorithm is deterministic; determinism comes from the proof in Section~3 there. Theorem~11 there finds colliding representations from $G(d,a)$ vectors when $d \mid p-1$, and the proof of Theorem~3 iterates it $\lceil\log_2(d+1)\rceil$ times, concluding $C(d,a) \le G(d,a)^{\lceil\log_2(d+1)\rceil}$ for the number $C(d,a)$ of variables needed.
```
NEW:
```
Only the warm-up Propositions~9 and~10 of~\cite{IvanyosSantha2015} are randomized. The statements of Theorems~3 and~11 there do not say that the algorithm is deterministic; determinism comes from the proofs in Sections~3.1--3.2 there. The proof of Theorem~3 there iterates Theorem~11 $\lceil\log_2(d+1)\rceil$ times and closes with a zero sum of $d+1$ $d$-th powers, concluding $C(d,a) \le G(d,a)^{\lceil\log_2(d+1)\rceil}$ for the number $C(d,a)$ of variables needed. Lemma~\ref{lem:rounds} below iterates it only $\lceil\log_2 t\rceil$ times, with a zero sum of length $t$.
```

### A10. rem:is-import (a)–(d), ll. 531–534

(a) OLD:
```
\textup{(a)} The algorithm returns the scalars $s_i$ themselves, not only $s_i^d$:
```
NEW:
```
\textup{(a)} The algorithm of Lemma~\ref{lem:rounds} returns the scalars $s_i$ themselves, not only $s_i^d$:
```

(b) OLD:
```
which reduces to the exponent $\kappa = \gcd(d,p-1)$, with $\kappa \mid p-1$ and $B_\kappa(a) \le B_d(a)$.
```
NEW:
```
which reduces to the exponent $\kappa = \gcd(d,p-1)$, with $\kappa \mid p-1$; the arity $B_d(a)$ of~\eqref{eq:Bd} is already stated at the degree $\kappa_d$.
```

(c) OLD:
```
\textup{(c)} The bound used is the one the proof establishes; see Remark~\ref{rem:is-printed}.
```
NEW:
```
\textup{(c)} Theorem~\ref{thm:main} does not use the bound of the proof of~\cite[Theorem~3]{IvanyosSantha2015} (Remark~\ref{rem:is-printed}). Lemma~\ref{lem:rounds} with $t = d+1$ and van de Woestijne's zero sum recovers it, and it bounds $B_d(a)$ from above.
```

(d) OLD (whole item):
```
\textup{(d)} Determinism is not essential to Theorem~\ref{thm:main}. Suppose the solver is only Las Vegas: on every input it either reports failure or returns a solution, which is checked before use, it fails with probability at most $1/4$, and its expected running time is at most an explicit $T(M_d,\log p)$. Cut each attempt off after $4T$ steps; by Markov's inequality an attempt then fails or runs past the cut-off with probability at most $1/2$. The procedure makes $N_{\mathrm{solver}} = (m+\tau)\sum_{d=2}^{c}\prod_{d'=2}^{d-1}M_{d'}$ solver calls, one per merge, a number fixed before the run. Make up to $\lceil\log_2(3N_{\mathrm{solver}}/\eps)\rceil$ attempts per call on the same saved labels, and abort the whole procedure if all of them fail. By the union bound it aborts with probability at most $\eps/3$, the third of the error budget that Schedule~1 leaves unused (Section~\ref{sec:proof-main}); no dilation is applied before a witness is accepted, so retries consume no further quantum sources, and the running time stays polynomial when $T$ is.
```
NEW:
```
\textup{(d)} \emph{Las Vegas steps.} The preprocessing of Schedule~1 (Lemma~\ref{lem:zero-sum-length}(iv)) is Las Vegas for some pairs $(p,\kappa_d)$. It is charged to the third of the error budget that the merges leave unused (Section~\ref{sec:proof-main}). At each of the at most $c-1$ grades, make up to $\lceil\log_2(3(c-1)/\eps)\rceil$ independent attempts, each cut off after twice its expected running time, so that by Markov's inequality each fails with probability at most $1/2$. Abort the whole procedure, before any query, if every attempt at some grade fails. By the union bound it aborts with probability at most $\eps/3$.
Determinism of the merges is not essential either. Suppose a per-merge solver is only Las Vegas: on every input it either reports failure or returns a solution, which is checked before use; it fails with probability at most $1/4$; and its expected running time is at most an explicit $T(M_d,\log p)$. Cut each attempt off after $4T$ steps. The procedure makes $N_{\mathrm{solver}} = (m+\tau)\sum_{d=2}^{c}\prod_{d'=2}^{d-1}M_{d'}$ solver calls, one per merge, a number fixed before the run. Split the same third: make $\lceil\log_2(6(c-1)/\eps)\rceil$ preprocessing attempts per grade and up to $\lceil\log_2(6N_{\mathrm{solver}}/\eps)\rceil$ attempts per call on the same saved labels, and abort if all attempts of any call fail. Each part then aborts with probability at most $\eps/6$. No dilation is applied before a witness is accepted, so retries consume no further quantum sources, and the running time stays polynomial when $T$ is.
```
(e) unchanged.

### A11. rem:is-printed, l. 544 (end)

OLD:
```
which is the bound used here, and that the printed exponent $d\log d$ of $a+1$ is a mistake. The explicit arity $B_d$ of~\eqref{eq:Bd}, and with it the query count of Theorem~\ref{thm:main} and the exponent $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$, rest on this bound.
```
NEW:
```
and that the printed exponent $d\log d$ of $a+1$ is a mistake. This first inequality is the arity $\bar B_d$ of~\eqref{eq:Bd}, and Lemma~\ref{lem:rounds} with $t = d+1$ re-derives it. Theorem~\ref{thm:main} uses the smaller arity $B_d \le \bar B_d$, at depth $L_d = \lceil\log_2 t_{p,\kappa_d}\rceil$. The confirmation covers the full depth $\lceil\log_2(d+1)\rceil$, and hence the weaker exponent $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ ($145$ at $c = 9$). It does not cover the shorter depth or the exponent $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$.
```

### A12. New lemmas, to insert after `\end{remark}` of rem:is-printed (after l. 545)

```
\begin{lemma}[Accumulated collisions; after~\cite[Section~3.3]{IvanyosSantha2015}]
\label{lem:rounds}
Let $\kappa \ge 2$ be fixed and let $p$ be a prime with $\kappa \mid p-1$. Let $z_1,\dots,z_t \in \Fp$, not all zero, satisfy $z_1^\kappa+\cdots+z_t^\kappa = 0$, and put $L = \lceil\log_2 t\rceil$. Given $z$ and any $\lambda_1,\dots,\lambda_M \in \Fp^a$ with $M \ge G(\kappa,a)^L$, a deterministic classical algorithm outputs explicit $s_1,\dots,s_M \in \Fp$, not all zero, with $\sum_i s_i^\kappa\lambda_i = 0$. It makes at most $\sum_{j<L}G(\kappa,a)^j$ calls of the algorithm of Theorem~\ref{thm:is-import} at degree $\kappa$ and runs in time polynomial in $M$ and $\log p$, where the polynomial depends on $\kappa$.
\end{lemma}

\begin{proof}
Write $G = G(\kappa,a)$. Since $z^\kappa = 0$ forces $z = 0$, $t \ge 2$ and $L \ge 1$. Give every column beyond the first $G^L$ the weight $0$. We claim, for $\ell = 1,\dots,L$: from any $G^\ell$ of the columns, indexed by a set $C$, at most $\sum_{j<\ell}G^j$ calls either output a nonzero solution supported in $C$, or output a vector $u \in \Fp^a$, pairwise disjoint nonempty sets $S_1,\dots,S_{2^\ell} \subseteq C$ and explicit nonzero $\sigma_i$ $(i \in \bigcup_r S_r)$ with $u = \sum_{i \in S_r}\sigma_i^\kappa\lambda_i$ for every $r$.
For $\ell = 1$, one call on the $G$ columns returns $I$, $J$ and $\gamma$. If $J = \emptyset$, then $s_i = \gamma_i$ on $I$ and $s_i = 0$ elsewhere is a nonzero solution. Otherwise take $u = \sum_{I}\gamma_i^\kappa\lambda_i$, $S_1 = I$, $S_2 = J$ and $\sigma = \gamma$.
For $\ell \to \ell+1$, split $C$ into $G$ blocks of $G^\ell$ columns and apply the claim to each. If some block returns a solution, extend it by zeros. Otherwise block $k$ returns $u_k$, sets $S^{(k)}_r$ and scalars $\sigma$. One more call on $u_1,\dots,u_G$ returns $I'$, $J'$ and nonzero $\delta_k$ with $\sum_{I'}\delta_k^\kappa u_k = \sum_{J'}\delta_k^\kappa u_k$.
If $J' = \emptyset$, substitute the first representation of each $u_k$: then $s_i = \delta_k\sigma_i$ for $i \in S^{(k)}_1$, $k \in I'$, and $s_i = 0$ elsewhere is a nonzero solution, because the sets $S^{(k)}_1$ lie in disjoint blocks.
Otherwise put $u = \sum_{I'}\delta_k^\kappa u_k$. For $r \le 2^\ell$ put $S_r = \bigcup_{k\in I'}S^{(k)}_r$ and $S_{2^\ell+r} = \bigcup_{k\in J'}S^{(k)}_r$, with the new scalar $\delta_k\sigma_i$ at $i \in S^{(k)}_r$. These $2^{\ell+1}$ sets are nonempty, because $I'$ and $J'$ and every $S^{(k)}_r$ are. They are pairwise disjoint, because the blocks are disjoint, $I' \cap J' = \emptyset$, and the sets inside a block are disjoint. Each of them represents $u$. The number of calls is $G\sum_{j<\ell}G^j + 1 = \sum_{j<\ell+1}G^j$.
At $\ell = L$, if no solution has been output, $2^L \ge t$. Put $s_i = z_r\sigma_i$ for $i \in S_r$, $r \le t$, and $s_i = 0$ elsewhere. Then $\sum_i s_i^\kappa\lambda_i = \bigl(\sum_{r\le t}z_r^\kappa\bigr)u = 0$, and $s \ne 0$, because some $z_r \ne 0$ and $S_r \ne \emptyset$. Apart from the calls, the algorithm multiplies $O(LM)$ field elements.
\end{proof}

With $t = d+1$ and van de Woestijne's zero sum this is the proof of~\cite[Theorem~3]{IvanyosSantha2015} (Remark~\ref{rem:is-printed}). The case $J = \emptyset$ is the case ``we are done if this is the zero vector'' of~\cite[Section~3.3]{IvanyosSantha2015}.

\begin{lemma}[The shortest zero sum]
\label{lem:zero-sum-length}
Let $p$ be an odd prime, $\kappa \ge 2$ a divisor of $p-1$, $h = (p-1)/\kappa$ and $t = t_{p,\kappa}$ as in~\eqref{eq:Bd}.
\begin{enumerate}[label=\textup{(\roman*)},leftmargin=2em]
  \item $2 \le t \le \kappa+1$, so $\lceil\log_2 t\rceil \le \lceil\log_2(\kappa+1)\rceil$.
  \item $t = 2$ if and only if $h$ is even.
  \item If $p \ge 4\kappa^4$, then $t \le 3$.
  \item The value $t$, and with it $\lceil\log_2 t\rceil$, is computed deterministically from $(p,\kappa)$ in time polynomial in $\log p$, with a constant depending on $\kappa$. A zero sum of length $t$, with explicit $z_j$, is computed deterministically in the same time when $p < 4\kappa^4$ or $\kappa$ is odd. Otherwise it is computed by a Las Vegas algorithm that checks its output and runs in expected time polynomial in $\kappa$ and $\log p$.
\end{enumerate}
\end{lemma}

\begin{proof}
(i) A single term $z^\kappa$ vanishes only for $z = 0$, so $t \ge 2$. The form $x_1^\kappa+\cdots+x_{\kappa+1}^\kappa$ has more variables than its degree, so by the Chevalley--Warning theorem~\cite[Chapter~6]{LidlNiederreiter1997} its number of zeros in $\Fp^{\kappa+1}$ is divisible by $p$. Since $0$ is one of them, there is a nonzero one.
(ii) The nonzero $\kappa$-th powers form the subgroup $P$ of order $h$ of the cyclic group $\Fp^\times$. For $x, y \ne 0$, $x^\kappa + y^\kappa = 0$ if and only if $-1 = (x/y)^\kappa \in P$. Since $p$ is odd, $-1$ is the unique element of order $2$ of $\Fp^\times$, so it lies in $P$ if and only if $2 \mid h$.
(iii) Let $N$ be the number of $(x,y) \in \Fp^2$ with $x^\kappa + y^\kappa = -1$. By Weil's bound for diagonal equations~\cite[Chapter~6]{LidlNiederreiter1997}, $|N - p| \le (\kappa-1)^2\sqrt p$. Since $\sqrt p \ge 2\kappa^2$, $(\kappa-1)^2\sqrt p < p/2$, so $N > p/2 \ge 2\kappa^4$. At most $2\kappa$ of these pairs have $xy = 0$, since $X^\kappa = -1$ has at most $\kappa$ roots. So some pair has $xy \ne 0$, and $x^\kappa + y^\kappa + 1^\kappa = 0$.
(iv) Let $p < 4\kappa^4$. List $y^\kappa$ for $y \in \Fp^\times$, recording one root of each element of $P$. Dividing a zero sum $\sum_{j\le t}u_j = 0$ with $u_j \in P$ by $u_t$ shows that $t-1$ is the distance from $0$ to $-1$ in the Cayley graph of $(\Fp,+)$ with generating set $P$. A breadth-first search over its $p$ vertices and $ph < 16\kappa^7$ edges finds $t$ and a shortest path, that is, the $u_j$ with their recorded roots.
Now let $p \ge 4\kappa^4$. By~(ii) and~(iii), $t = 2$ if $h$ is even and $t = 3$ otherwise.
If $\kappa$ is odd, $h$ is even and $(1,-1)$ is a zero sum.
If $\kappa$ and $h$ are even, then $2\kappa \mid p-1$. For uniform $x \in \Fp^\times$, $y = x^{(p-1)/(2\kappa)}$ satisfies $y^\kappa = x^{(p-1)/2} = \pm1$, and it equals $-1$ exactly when $x$ is a nonresidue, that is, with probability $1/2$. Output $(1,y)$ once $y^\kappa = -1$ is checked.
If $\kappa$ is even and $h$ is odd, pick a uniform $x \in \Fp$ and put $u = -1-x^\kappa$. If $u \ne 0$ and $u^h = 1$, then $u \in P$. Find $y$ with $y^\kappa = u$ by Las Vegas root finding for $X^\kappa - u$~\cite{Rabin1980}, and output $(x,y,1)$ once it is checked. By the count in~(iii), at least $(N-2\kappa)/\kappa$ values of $x$ admit such a $y$, since each $x$ has at most $\kappa$ partners $y$. So a uniform $x$ succeeds with probability at least $1/(2\kappa) - 2/p \ge 1/(4\kappa)$, since $p \ge 8\kappa$.
\end{proof}
% NEEDS HUMAN VERIFICATION: the locator of Weil's bound |N - q^{n-1}| <= prod(d_i - 1) q^{(n-1)/2}
% for diagonal equations with nonzero right side; recalled (not checked) as Lidl--Niederreiter,
% Finite Fields, Theorem 6.37. For two variables it also follows from Jacobi sums
% (N = p + sum over nontrivial characters chi_1, chi_2 of order dividing kappa of
% chi_1 chi_2(-1) J(chi_1, chi_2), |J| <= sqrt p).
```

### A13. lem:bezout, ll. 547–554

OLD (statement, second sentence):
```
Consequently, by Theorem~\ref{thm:is-import} at degree $\kappa$, any $M \ge B_\kappa(a)$ columns admit a nonzero solution of~\eqref{eq:sde-target}, computed deterministically in time $\poly(M,\log p)$, for every prime $p$; and $B_\kappa(a) \le B_d(a)$, with $B_1(a) = a+1$.
```
NEW:
```
Consequently, any $M \ge B_d(a)$ columns admit a nonzero solution of~\eqref{eq:sde-target}, for every prime $p$. It is computed by linear algebra when $\kappa = 1$. When $\kappa \ge 2$ it is computed by Lemma~\ref{lem:rounds} at degree $\kappa$, given a zero sum of $\kappa$-th powers of length $t_{p,\kappa}$, deterministically in time $\poly(M,\log p)$. Moreover $B_d(a) \le \bar B_d(a)$.
```
OLD (proof, last sentence):
```
Finally $B_d(a)$ is increasing in $d$.
```
NEW:
```
Finally, for $\kappa \ge 2$, $B_d(a) = G(\kappa,a)^{L_d} \le G(\kappa,a)^{\lceil\log_2(\kappa+1)\rceil}$ by Lemma~\ref{lem:zero-sum-length}(i). This is at most $G(d,a)^{\lceil\log_2(d+1)\rceil} = \bar B_d(a)$, because $G(x,a)^{\lceil\log_2(x+1)\rceil}$ is increasing in $x$. For $\kappa = 1$, $a+1 \le \bar B_d(a)$.
```

### A14. rem:zero-sum, l. 558

OLD:
```
while Schedule~1 allots $B_4(2) = G(4,2)^3 \approx 3.7\cdot 10^{16}$ columns.
```
NEW:
```
while Schedule~1 allots $B_4(2) = G(4,2)^3 \approx 3.7\cdot 10^{16}$ columns (here $t_{5,4} = 5$).
```
The value is unchanged.

### A15. Schedule 1 paragraph, l. 561 (whole paragraph)

OLD:
```
\paragraph{Schedule~1.} At stage $d$, take $M_d = B_d(g_d)$ columns (if $g_d = 0$, which happens when the class of $\mathcal{L}$ is below $d$, the stage is vacuous and $M_d = 1$ would suffice; the counts below keep $B_d(0)$ for uniformity), run the algorithm of Theorem~\ref{thm:is-import} at degree $\kappa_d = \gcd(d,p-1)$ on the first $B_{\kappa_d}(g_d)$ of them, give the remaining columns the weight $0$, and convert by Lemma~\ref{lem:bezout}. This returns a nonzero solution of~\eqref{eq:sde-target} for every label tuple and every prime $p > c$. The number of lifted sources per terminal sample is $\prod_{d=2}^c B_d(g_d)$; the smaller arity $B_{\kappa_d}(g_d)$ would also suffice, so the counts that use $B_d$ are upper bounds.
```
NEW:
```
\paragraph{Schedule~1.} \emph{Preprocessing}, once per grade, before any query: compute $\kappa_d = \gcd(d,p-1)$ and, if $\kappa_d \ge 2$, $L_d$ and a zero sum of $\kappa_d$-th powers of length $t_{p,\kappa_d}$ (Lemma~\ref{lem:zero-sum-length}(iv)). Both depend only on $(p,\kappa_d)$, and the step makes no query. \emph{Merge:} at stage $d$, take $M_d = B_d(g_d)$ columns. If $g_d = 0$, which happens when the class of $\mathcal{L}$ is below $d$, the stage is vacuous and $M_d = 1$ would suffice; the counts below keep $B_d(0)$ for uniformity. Solve $\sum_i x_i^{\kappa_d}\lambda_i = 0$ by linear algebra if $\kappa_d = 1$, and otherwise by Lemma~\ref{lem:rounds} with the precomputed zero sum, and convert by Lemma~\ref{lem:bezout}. Given the preprocessing, this returns, deterministically, a nonzero solution of~\eqref{eq:sde-target} for every label tuple and every prime $p > c$. The number of lifted sources per terminal sample is $\prod_{d=2}^c B_d(g_d) \le \prod_{d=2}^c\bar B_d(g_d)$.
```

### A16. New lemma, after the Schedule 1 paragraph (after l. 561)

```
\begin{lemma}[The exponent]
\label{lem:exponent}
For a prime $p > c$ and $2 \le d \le c$, put $e_{p,d} = 1$ if $\kappa_d = 1$ and $e_{p,d} = \kappa_dL_d$ otherwise, and put $E_1(c) = 1 + \max_{p>c}\sum_{d=2}^c e_{p,d}$. Then $B_d(a) \le d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}(a+1)^{e_{p,d}}$. Moreover:
\begin{enumerate}[label=\textup{(\roman*)},leftmargin=2em]
  \item $c(c+1)/2 \le E_1(c) \le 1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ for every $c \ge 2$.
  \item $E_1(c) = 5, 8, 16, 19, 35, 36, 44, 53$ for $c = 2,\dots,9$. $E_1(9) = 53$ is attained exactly at the primes $p \equiv 2521 \pmod{5040}$.
\end{enumerate}
Part~(ii) combines the argument below with an exact computation for the primes below $4c^4$.
\end{lemma}

\begin{proof}
The maximum exists because $e_{p,d}$ is bounded. For $\kappa = \kappa_d \ge 2$, $L_d \le \lceil\log_2(\kappa+1)\rceil \le \lceil\log_2(d+1)\rceil$ by Lemma~\ref{lem:zero-sum-length}(i), and $\kappa \le d$. This gives the bound on $B_d(a)$, and the upper bound in~(i), because $x\lceil\log_2(x+1)\rceil$ is increasing.
For the lower bound, Dirichlet's theorem gives a prime $p \equiv 1 \pmod{2\operatorname{lcm}(1,\dots,c)}$. Then $\kappa_d = d$ and $(p-1)/d$ is even, so $L_d = 1$ and $e_{p,d} = d$ by Lemma~\ref{lem:zero-sum-length}(ii), and $1+\sum_{d=2}^c d = c(c+1)/2$.
(ii) For $p \ge 4c^4$, Lemma~\ref{lem:zero-sum-length}(ii)--(iii) give $e_{p,d} = \kappa_d$ when $(p-1)/\kappa_d$ is even, and $e_{p,d} = 2\kappa_d$ otherwise. This includes $\kappa_d = 1$, since $p$ is odd. The vector $(e_{p,d})_d$ therefore depends only on $p$ modulo $N_c = 2\operatorname{lcm}(1,\dots,c)$, and every unit class modulo $N_c$ contains primes $p \ge 4c^4$.
For $c = 9$ ($4c^4 = 26244$), let $v = v_2(p-1)$. Since $v_2(\kappa_d) = \min(v_2(d),v)$, the index $(p-1)/\kappa_d$ is odd exactly when $v_2(d) \ge v$. The odd grades contribute at most $3+5+7+9 = 24$.
\begin{itemize}
  \item $v = 1$: the even grades contribute at most $4+4+12+4$, since $\kappa_4, \kappa_8 \le 2$ and $\kappa_6 \le 6$, so the total is at most $49$.
  \item $v = 2$: they contribute at most $2+8+6+8$, again at most $49$.
  \item $v = 3$: they contribute at most $2+4+6+16$, at most $53$, with equality exactly when $\kappa_d = d$ for every $d \le 9$.
  \item $v \ge 4$: they contribute at most $2+4+6+8$, at most $45$.
\end{itemize}
So $53$ is attained above $26244$ exactly when $2520 \mid p-1$ and $16 \nmid p-1$, that is, $p \equiv 2521 \pmod{5040}$. An exhaustive computation of $t_{p,\kappa}$ for all primes $9 < p < 26244$ and all $\kappa \mid \gcd(p-1, \operatorname{lcm}(1,\dots,9))$, $\kappa \le 9$, gives maximum $53$, attained exactly at $p = 2521, 7561, 12601$, the primes $\equiv 2521 \pmod{5040}$ in that range. For $c \le 8$ the same computation over the primes $c < p < 4c^4$ and one prime $p \ge 4c^4$ in each unit class modulo $N_c$ gives the listed values.
\end{proof}
```
The exact-computation status should be stated in the lemma's optional argument if the
paper's convention requires it (cf. `sec:status`: "results of computer searches are marked
as exact computations"). Suggested heading: `\begin{lemma}[The exponent; part~(ii) partly an exact computation]`.

### A17. Proof of thm:main (Section `sec:proof-main`), ll. 633–650

(a) l. 633 OLD:
```
put $\tau = \lceil\log_p(3/\eps)\rceil$ and $M_d = B_d(g_d)$ for $2 \le d \le c$. Compute the structure constants of $\A$ and of the quotients $\A^{(d)}$.
```
NEW:
```
put $\tau = \lceil\log_p(3/\eps)\rceil$ and $M_d = B_d(g_d)$ for $2 \le d \le c$. Run the preprocessing of Schedule~1 (Section~\ref{sec:schedule1}) as in Remark~\ref{rem:is-import}(d), and stop with output ``fail'' if it aborts. Compute the structure constants of $\A$ and of the quotients $\A^{(d)}$.
```

(b) l. 635 OLD:
```
returns explicit scalars $s_i$, not all zero, solving~\eqref{eq:sde-target} for every label tuple, deterministically.
```
NEW:
```
returns explicit scalars $s_i$, not all zero, solving~\eqref{eq:sde-target} for every label tuple, deterministically given the preprocessing.
```
l. 635 OLD (also "Theorem is-import at degree κ_d followed by Lemma bezout"):
```
and Schedule~1, that is, Theorem~\ref{thm:is-import} at degree $\kappa_d$ followed by Lemma~\ref{lem:bezout},
```
NEW:
```
and Schedule~1, that is, Lemma~\ref{lem:rounds} (or linear algebra) at degree $\kappa_d$ followed by Lemma~\ref{lem:bezout},
```
l. 635 OLD (end):
```
So the ideal procedure fails with probability at most $\eps/3$. Schedule~1 is deterministic and total at its arity, so there is no solver failure to budget.
```
NEW:
```
So the ideal procedure, given a completed preprocessing, fails with probability at most $\eps/3$. Given the preprocessing, Schedule~1 is deterministic and total at its arity, so the merges add no failure. The preprocessing aborts with probability at most $\eps/3$ (Remark~\ref{rem:is-import}(d)), before any query.
```

(c) l. 642 OLD:
```
This number is fixed before the run, because the arities of Schedule~1 are public and fixed and there are no restarts, so the allocation below is legitimate. Compiling every transform with $\eta = \eps/(3N_{\mathrm{QFT}})$, Corollary~\ref{cor:approx} bounds the change in the output distribution by $\eps/3$. The total failure probability is therefore at most $2\eps/3 < \eps$.
```
NEW:
```
This number is fixed before the run, because the arities of Schedule~1 are computed from the public data $(p,d,g_d)$ before any query and there are no restarts, so the allocation below is legitimate. Compiling every transform with $\eta = \eps/(3N_{\mathrm{QFT}})$, Corollary~\ref{cor:approx} bounds the change in the output distribution by $\eps/3$. The total failure probability is therefore at most $\eps/3+\eps/3+\eps/3 = \eps$.
```

(d) ll. 644–648 OLD:
```
so the procedure makes $c(m+\tau)\prod_{d=2}^cB_d(g_d) = Q_{\mathrm q}$ queries. Since $g_d \le m$,
\[
  B_d(g_d) \le \bigl[d^{d(d-1)/2}(m+1)^d\bigr]^{\lceil\log_2(d+1)\rceil} = d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}\,(m+1)^{d\lceil\log_2(d+1)\rceil},
\]
and the product over $d$ gives the bound $C_c\,c\,(m+\tau)(m+1)^{\sum_{d=2}^c d\lceil\log_2(d+1)\rceil}$ of Theorem~\ref{thm:main}.
```
NEW:
```
so the procedure makes $c(m+\tau)\prod_{d=2}^cB_d(g_d) = Q_{\mathrm q}$ queries; it makes none if the preprocessing aborts. Since $g_d \le m$, Lemma~\ref{lem:exponent} gives
\[
  B_d(g_d) \le d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}\,(m+1)^{e_{p,d}},
\]
and the product over $d$ gives the bound $C_c\,c\,(m+\tau)(m+1)^{\sum_d e_{p,d}} \le C_c\,c\,(m+\tau)(m+1)^{E_1(c)-1}$ of Theorem~\ref{thm:main}.
```

(e) l. 650 OLD:
```
one call of Schedule~1, which runs in time $\poly(M_d,\log p)$ by Theorem~\ref{thm:is-import} and Lemma~\ref{lem:bezout},
```
NEW:
```
one call of Schedule~1, which runs in time $\poly(M_d,\log p)$ by Lemmas~\ref{lem:rounds} and~\ref{lem:bezout},
```
l. 650 OLD:
```
The final null space and the structure constants of $\A$ cost $\poly(m,\log p)$.
```
NEW:
```
The final null space and the structure constants of $\A$ cost $\poly(m,\log p)$. The preprocessing makes at most $(c-1)\lceil\log_2(3(c-1)/\eps)\rceil$ cut-off attempts, each of time $\poly(\log p)$ for fixed $c$ (Lemma~\ref{lem:zero-sum-length}(iv)).
```

### A18. rem:oblivious, l. 654

OLD:
```
are fixed before the run by $p$, $m$, the $g_d$ and $\eps$; there are no restarts; and Schedule~1 returns scalars for every label tuple, within the time of Theorem~\ref{thm:is-import}, which is stated for arbitrary $\lambda_i$, and of the conversion to the exponent $d$.
```
NEW:
```
are fixed before the run by $p$, $m$, the $g_d$ and $\eps$; the preprocessing of Schedule~1 depends only on $p$, $c$ and $\eps$, makes no query and is cut off; there are no restarts; and Schedule~1 returns scalars for every label tuple, within the time of Lemma~\ref{lem:rounds}, which is stated for arbitrary $\lambda_i$, and of the conversion to the exponent $d$.
```

### A19. Examples

l. 664 (Heisenberg) OLD:
```
while Schedule~1 allots $B_2(1) = 64$;
```
NEW:
```
while Schedule~1 allots $B_2(1) = G(2,1) = 8$ when $p \equiv 1 \pmod 4$ and $G(2,1)^2 = 64$ when $p \equiv 3 \pmod 4$ (Lemma~\ref{lem:zero-sum-length}(ii));
```
l. 690 (class 3, stage three) OLD:
```
Schedule~1 allots $B_3(2) = G(3,2)^2 = 729^2 = 531441$.
```
NEW:
```
Schedule~1 allots $B_3(2) = G(3,2) = 729$ when $p \equiv 1 \pmod 3$, since then $\kappa_3 = 3$ and $t_{p,3} = 2$, and $g_3+1 = 3$ when $p \equiv 2 \pmod 3$.
```
l. 692 (stage two) OLD:
```
Schedule~1 allots $B_2(3) = G(2,3)^2 = 32^2 = 1024$.
```
NEW:
```
Schedule~1 allots $B_2(3) = G(2,3) = 32$ when $p \equiv 1 \pmod 4$ and $G(2,3)^2 = 1024$ when $p \equiv 3 \pmod 4$.
```
l. 694 OLD:
```
The count of Theorem~\ref{thm:main} is $Q_{\mathrm q} = 3(5+\tau)\cdot1024\cdot531441$, about $2^{33.19}$ at $\tau = 1$.
```
NEW:
```
The count of Theorem~\ref{thm:main} is at most $Q_{\mathrm q} = 3(5+\tau)\cdot1024\cdot729$, about $2^{23.68}$ at $\tau = 1$, with equality when $p \equiv 7 \pmod{12}$.
```

### A20. Corollaries (ll. 723–774)

No change. `B_d(L)` and "$B_d$ is increasing" refer to the new B_d at the given p, which
is nondecreasing in a. Each call of Theorem main runs its own preprocessing inside its own
error parameter.

### A21. Crossover table and rem:query-separation, ll. 874–897

Caption (l. 874) OLD:
```
\caption{Query counts at $\delta = \eps = 1/3$ and $p \ge 11$, where $\tau = 1$. Here $Q_{\mathrm q}$ is the count of Theorem~\ref{thm:main}.
```
NEW:
```
\caption{Query counts at $\delta = \eps = 1/3$ and $p \ge 11$, where $\tau = 1$. Here $Q_{\mathrm q}$ is the largest value, over the primes $p \ge 11$, of the count of Theorem~\ref{thm:main}, which depends on $p$ through the $\kappa_d$ and $L_d$. The maximum is attained at $p \equiv 3 \pmod 4$ for the Heisenberg row, at $p \equiv 7 \pmod{12}$ for the class-three rows, and at $p \equiv 2521 \pmod{5040}$ for the last row.
```
Caption OLD:
```
(with $8\ell$ itself they are $86$, $121{,}497$, $42{,}773$ and $642$, so the thresholds are the primes up to $83$, $121{,}493$, $42{,}767$ and $641$)
```
NEW:
```
(with $8\ell$ itself they are $86$, $3{,}375$, $1{,}585$ and $98$, so the thresholds are the primes up to $83$, $3{,}373$, $1{,}583$ and $97$)
```
Rows (ll. 882–886) NEW (the Heisenberg row is unchanged):
```
Heisenberg & 2 & 3 & $(1)$ & $9.00$ & $443$ & $84$ & $81$ \\
filiform & 3 & 4 & $(2,1)$ & $20.00$ & $9{,}391$ & $3{,}325$ & $218$ \\
free, two generators & 3 & 5 & $(3,2)$ & $23.68$ & $3{,}413$ & $1{,}567$ & $293$ \\
Dixmier--Lister & 3 & 8 & $(4,2)$ & $25.55$ & $157$ & $97$ & $474$ \\
class-$\ReesClassNineClass$ profile & 9 & 19 & $(17,16,14,12,9,6,3,1)$ & $563.63$ & $\approx 2^{62.60}$ & $\approx 2^{62.35}$ & $22{,}548$ \\
```
The source is `2026-11-12-rees-headline-53/verify_headline.json`, key `crossover`.
`classical_lb.py` was imported read-only, and the exact-8ℓ thresholds are in
`crossover_exact8l.json`. Heisenberg is unchanged at its worst prime, p ≡ 3 mod 4.

rem:query-separation, l. 893 OLD:
```
The count $Q_{\mathrm q}$ of Theorem~\ref{thm:main} does not depend on $p$ once $p \ge 3/\eps$, and at fixed $c$ it is polynomial in $m$ with exponent at most $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$.
```
NEW:
```
The count $Q_{\mathrm q}$ of Theorem~\ref{thm:main} is at most $c(m+\tau)\prod_{d=2}^c\bar B_d(g_d)$, which does not depend on $p$ once $p \ge 3/\eps$, and at fixed $c$ it is polynomial in $m$ with exponent at most $E_1(c)$, uniformly in $p$ (Lemma~\ref{lem:exponent}).
```
l. 897 OLD:
```
an advantage needs $p > 2^{174.7}$.
```
NEW:
```
an advantage needs $p > 2^{62.6}$.
```

### A22. Outlook, ll. 909–917

"Smaller arities" (l. 909) OLD:
```
with these thresholds as stated, a per-grade choice of solver lowers the exponent of $m$ at $c = 9$ only from $\ReesClassNineQueryExp$ to $143$, because at primes such as $p = 2521$ every $\kappa_d$ equals $d$ and only the grade with $\kappa_d = 2$ meets the Schedule~2 threshold.
```
NEW:
```
with these thresholds as stated, a per-grade choice of solver does not lower the exponent $\ReesClassNineQueryExp$ of $m$ at $c = 9$ (against the full-depth Schedule~1 it would lower $145$ to $143$), because at primes such as $p = 2521$ every $\kappa_d$ equals $d$ and only the grade with $\kappa_d = 2$ meets the Schedule~2 threshold, where Schedule~1 already has exponent $2$.
```
OLD (same paragraph):
```
taking the best of these solvers at each grade, the largest exponent at $c = 9$ over all primes $p > 9$ is $37$ (finite computation over the exceptional primes).
```
NEW:
```
taking the best of these solvers at each grade, the largest exponent at $c = 9$ over all primes $p > 9$ is at most $37$ (finite computation over the exceptional primes, made with the full-depth Schedule~1 and not repeated with the depth $L_d$).
```
"Shorter zero sums in Schedule 1" (l. 911): **delete the whole paragraph.** Its content is
now `lem:rounds`, `lem:zero-sum-length`, `lem:exponent` and A6/A11.

"Black-box nilpotent groups" (l. 913): unchanged.

Open problems, l. 917 OLD:
```
(1) The exponent of $m$ in Theorem~\ref{thm:main} grows like $c^2\log c$, entirely through the arity
```
NEW:
```
(1) The exponent of $m$ in Theorem~\ref{thm:main} grows at least quadratically in $c$ (Lemma~\ref{lem:exponent}), entirely through the arity
```

### A23. Artifacts (`app:artifacts`)

"Readings of sources" (l. 941): append
```
The accumulation step of Lemma~\ref{lem:rounds} and its shortest-zero-sum depth were checked against Section~3.3 of the arXiv text in \file{research/audits/reviews/2026-11-12-rees-exponent-discharge.md} and \file{research/audits/reviews/2026-11-12-rees-exponent-discharge-referee.md}, by AI sessions only.
```
"Diagonal-equation solver" item (l. 952) OLD:
```
implements the deterministic solver of Theorem~\ref{thm:is-import} and returns
```
NEW:
```
implements Lemma~\ref{lem:rounds} with Theorem~\ref{thm:is-import} and a computed zero sum, and returns
```
New item, after it:
```
  \item Zero-sum depth and exponent (Lemmas~\ref{lem:zero-sum-length} and~\ref{lem:exponent}): \file{theorems/rees_hsp_reduction.py} (\texttt{zero\_sum\_length}, \texttt{zero\_sum\_depth\_exponent}) and, as independent code without the Weil shortcut, \file{research/audits/reviews/2026-11-12-rees-headline-53/verify_headline.py}, which compute $t_{p,\kappa}$ by exhaustive search for every prime $p < 26244$ and the values $E_1(c)$, $c \le 9$; the second also checks the Weil range $[26244, 40000]$ and the residue classes modulo $5040$.
```

### A24. Numbers

`numbers.tex` is regenerated by the integrator (`make_numbers.py`; agents may not run it).
The expected diff is `2026-11-12-rees-headline-53/numbers.tex.diff`:

| macro | old | new |
|---|---|---|
| ReesClassNineQueryExp | 145 | 53 |
| ReesClassNineSdeAttempts | 1081 | 441 |
| ReesClassNineOrigQueriesBits | 1573 | 564 |
| ReesClassNineInstCallsBits | 1570 | 561 |
| ReesOuterQueryExp | 147 | 55 |
| ReesOuterOrigQueriesBits | 2194 | 794 |

Copy the result to `core/numbers.tex` and `arxiv/numbers.tex`; the three copies are
currently identical. The core uses only ReesClassNineQueryExp and ReesClassNineClass. Every
core sentence that uses QueryExp is rewritten above (A4, A6, A7, A11, A22), so no core
sentence reads "… 1+Σ d⌈log₂(d+1)⌉ … this is 53".

---

## Part B — full version (`main.tex` and appendices)

Where the text is the same as in the core, apply the corresponding A item with the
full-version labels. Only the differences are written out.

- **B1. Status, `main.tex` ll. 66–69.**
  - OLD: `G.~Ivanyos has confirmed the corrected` / `arity bound it uses (Remark~\ref{rem:is-import}(c)), and the rest of the` / `reading has not been checked by a human.`
  - NEW: `G.~Ivanyos has confirmed the corrected full-depth arity bound of its Theorem~3 (Remark~\ref{rem:is-import}(c)); the shorter depth used here (Lemma~\ref{lem:rounds}) is not covered by that confirmation, and the rest of the reading has not been checked by a human.`
- **B2. thm:main(4), ll. 228–231.** As A4.
- **B3. l. 238.** As A5.
- **B4. rem:main-solver, l. 242.** As A6(a) and (b). In (b), keep the full-version tail
  "(same remark; Appendix~\ref{app:provenance}, item~\ref{prov:sde-is-import})" after
  "Remark~\ref{rem:is-import}(c)". Also:
  - OLD: `Of the solvers in Section~\ref{sec:schedules}, Schedule~1 has all four properties;`
  - NEW: `Of the solvers in Section~\ref{sec:schedules}, Schedule~1 has all four properties once its zero sums are precomputed (Lemma~\ref{lem:zero-sum-length}; the Las Vegas preprocessing is charged to the solver share);`
- **B5. ll. 247–252.** Replace the display `B_d(a) \coloneqq \bigl[d^{d(d-1)/2}(a+1)^d\bigr]^{\lceil \log_2(d+1)\rceil}` and l. 251 with the A2 definition. l. 252: `The exponent of $m$ grows like $c^2\log c$` → `The exponent of $m$ grows at least quadratically in $c$ (Lemma~\ref{lem:exponent})`.
- **B6. Regimes table, l. 265.**
  - OLD: `or $B_{\kappa_d}(g_d)$ respectively; at most $\prod_{d=2}^c B_d(g_d)$`
  - NEW: `or $B_d(g_d)$ respectively; at most $\prod_{d=2}^c B_d(g_d)$`
  - Under A2, B_{κ_d} = B_d, so this is cosmetic. l. 263 is unchanged.
- **B7. Notation table, l. 379.**
  - OLD: `Ivanyos--Santha arity $B_d(a) = G(d,a)^{\lceil\log_2(d+1)\rceil}$ for $a$ equations of degree $d$ (Schedule~1);`
  - NEW: `Schedule~1 arity $B_d(a) = G(\kappa_d,a)^{\lceil\log_2 t_{p,\kappa_d}\rceil}$ ($a+1$ if $\kappa_d = 1$) for $a$ equations of degree $d$; published Ivanyos--Santha arity $\bar B_d(a) = G(d,a)^{\lceil\log_2(d+1)\rceil}$; $t_{p,\kappa}$, least length of a zero sum of $\kappa$-th powers;`
- **B8. l. 425.** `($E_W(9) = 143$)` → `($E_W(9) = 53$)`. K_c (l. 424) is unchanged; it is still a valid constant.
- **B9. thm:is-import, l. 715, and rem:is-import.**
  - thm:is-import: as A9, with the title `[Theorem~11, Sections~3.1--3.2]`.
  - rem:is-import (b): append `the arity $B_d(a)$ of~\eqref{eq:Bd} is already stated at degree $\kappa_d$` in place of `and $B_\kappa(a) \le B_d(a)$`.
  - (c): append `This bound is $\bar B_d$; Theorem~\ref{thm:main} uses the smaller $B_d$ of Lemma~\ref{lem:rounds}, at depth $\lceil\log_2 t_{p,\kappa_d}\rceil$, which the confirmation does not cover.`
  - (d): as the first part of A10(d), charged to "the solver share of the error budget in Section~\ref{sec:recursion}".
  - Insert `lem:rounds`, `lem:zero-sum-length` and `lem:exponent` (A12, A16) after rem:is-import, or in `sec:schedule1`.
- **B10. rem:is-runtime, l. 726.**
  - OLD: `with $L = \lceil\log_2 \ell_d\rceil$;`
  - NEW: `with $L = L_d = \lceil\log_2 t_{p,\kappa_d}\rceil$ (the zero sum precomputed by Lemma~\ref{lem:zero-sum-length});`
  - The $b^4$ and $C_3d^4b^5$ "zero sum" terms bounded a deterministic zero sum (van de Woestijne). With precomputed zero sums they become preprocessing terms. **NOT re-derived**; flag as "the zero-sum term is the preprocessing of Lemma zero-sum-length, Las Vegas for some (p, κ_d), not included in T^IS_d".
- **B11. sec:schedule1, l. 746.** Several edits:
  - `The algorithm is deterministic by the proof in Section~3 of~\cite{IvanyosSantha2015};` → `Given the precomputed zero sums, the algorithm is deterministic by Lemma~\ref{lem:rounds} and the proof in Sections~3.1--3.2 of~\cite{IvanyosSantha2015};`
  - `Its solver term in the budget of Section~\ref{sec:recursion} is therefore zero.` → `Its only solver term in the budget of Section~\ref{sec:recursion} is the preprocessing (Remark~\ref{rem:is-import}(d)).`
  - `More precisely, the deterministic run needs only $G(\kappa_d,a)^{\lceil\log_2 \ell_d\rceil}$ columns, with $G$ as in Theorem~\ref{thm:is-import} and $\ell_d \le \kappa_d+1$ the number of terms of the computed zero sum of $\kappa_d$-th powers.` → `With the shortest zero sum, $\ell_d = t_{p,\kappa_d}$, this is the arity $B_d(a)$ of~\eqref{eq:Bd}.`
  - `With $M_d = B_d(g_d)$, the number of lifted sources per terminal sample is $\prod_{d=2}^c B_d(g_d)$. At fixed $c$, the total query count is polynomial in $m$ with exponent at most $1 + \sum_{d=2}^c d\lceil\log_2(d+1)\rceil$; this is $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$.` → `With $M_d = B_d(g_d)$, the number of lifted sources per terminal sample is $\prod_{d=2}^c B_d(g_d)$. At fixed $c$, the total query count is polynomial in $m$ with exponent at most $E_1(c)$ (Lemma~\ref{lem:exponent}); this is $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$, against $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil = 145$ at the full depth.`
  - This edit is **required**: with the new macro, the old sentence would read "1+Σ … ; this is 53", which is false.
- **B12. rem:combined-schedule, l. 813.**
  - `with $M_d = B_{\kappa_d}(g_d) \le B_d(g_d)$` → `with $M_d = B_d(g_d) \le \bar B_d(g_d)$`.
  - OLD: `The worst case over primes barely moves: at fixed $c$, the exponent of $m$ in the query count, maximized over all $p > c$, is unchanged for $c \le 7$, and it falls by two for $c = 8$ and $c = 9$, to $143$ at $c = 9$ against the bound $\ReesClassNineQueryExp$ of Schedule~1.`
  - NEW: `The worst case over primes does not move: at fixed $c \le 9$, the exponent of $m$ in the query count, maximized over all $p > c$, equals $E_1(c)$ (exact computation; against the full-depth Schedule~1 it fell by two for $c = 8$ and $c = 9$, from $145$ to $143$ at $c = 9$).`
  - **Risk to flag:** when Schedule 2 grades (Las Vegas per call) and the Schedule 1 preprocessing co-occur, the solver share ε/3 must be split as in A10(d), second part. This is not reflected in the JSON, whose per-call attempt model is conservative only up to one extra attempt per call.
- **B13. prop:coherent-receiver, l. 976.** `M_d = B_d(g_d)`: unchanged text. Add: "the machine $\mathcal{M}_d$ also reads the precomputed zero sum, a classical public input".
- **B14. Profile paragraph, l. 1085.** Required with the macro change.
  - `uses the published-arity Schedule~1.` → `uses Schedule~1 at the depth $L_d$ of~\eqref{eq:Bd}, maximized over the primes $p > 9$ (worst at $p \equiv 2521 \pmod{5040}$); the published-depth profile, with exponent $145$, is kept in \file{rees_hsp_reduction.json} as \texttt{published\_depth\_profile}.`
  - `Since the Schedule~1 solver is deterministic, these are conservative.` → `Since the Schedule~1 solver is deterministic given its precomputed zero sums, these are conservative.`
  - `so $E_W(9) = 143$ and the query exponent $E_W(9)+1$ is $144$ ($146$ with Schedule~1 alone)` → `so $E_W(9) = 53$ and the query exponent $E_W(9)+1$ is $54$, the same with Schedule~1 alone`.
  - `the new count is about $2^{2186}$ against $2^{\ReesOuterOrigQueriesBits}$. With the true composition length $n_p \le \lfloor 104/\log_2 43\rfloor = 19$ it is about $2^{1833}$, and under the combined rule $2^{603}$.` → `the new count is about $2^{786.7}$, maximized over $p$ ($2^{423.9}$ at $p = 43$), against $2^{\ReesOuterOrigQueriesBits}$. At $p = 43$, with the true composition length $n_p \le \lfloor 104/\log_2 43\rfloor = 19$, it is about $2^{324.1}$, under Schedule~1 alone and under the combined rule alike.`
  - The source is `2026-11-12-rees-headline-53/zero_sum_tables.json`, key `bb_envelope`. The controls reproduce 2186.4, 1832.8 and 602.5.
- **B15. Examples, ll. 1123–1127.** As A19. The full-version strings are `$B_3(2) = (3^3\cdot 3^3)^2 = 729^2 = 531441$` → `$B_3(2) = 3^3\cdot 3^3 = 729$ when $p \equiv 1 \pmod 3$ and $g_3+1 = 3$ when $p \equiv 2 \pmod 3$`; `$B_2(3) = (2\cdot 4^2)^2 = 32^2 = 1024$` → `$B_2(3) = 2\cdot 4^2 = 32$ when $p \equiv 1 \pmod 4$ and $32^2 = 1024$ when $p \equiv 3 \pmod 4$`; and the count as in A19.
- **B16. Table and rem:query-separation, ll. 1196–1225.** As A21.
  - Caption OLD: `Here $Q_{\mathrm q}$ is the Schedule~1 count $c(m+\tau)\prod_{d=2}^c B_d(g_d)$ of Remark~\ref{rem:query-separation}.` → NEW: `Here $Q_{\mathrm q}$ is the largest value over the primes $p \ge 11$ of the Schedule~1 count $c(m+\tau)\prod_{d=2}^c B_d(g_d)$ of Remark~\ref{rem:query-separation}`, plus the attainment sentence of A21.
  - `with $8u$ itself the thresholds are the primes up to $83$, $121{,}493$, $42{,}767$ and $641$` → `... $83$, $3{,}373$, $1{,}583$ and $97$`.
  - l. 1220: as the A21 l. 893 edit. l. 1225: `2^{174.7}` → `2^{62.6}`.
- **B17. Corollary counts, ll. 1366 and 1378.** No change (A20).
- **B18. thm:bb-envelope, l. 1443.**
  - OLD: `Here $E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143$ for $c = 2,\dots,9$; with Schedule~1 alone at every grade (at degree $\kappa_d$), $E_W$ is replaced by $E_1(c) = 1 + \sum_{d=2}^c d\lceil\log_2(d+1)\rceil$, which is $145$ at $c=9$, and the theorem then does not depend on Theorem~\ref{thm:power-sde}(ii); since $E_W(c) = E_1(c)$ for $c \le 7$ (Lemma~\ref{lem:tb-count-exponent}), the combined rule, and with it that dependence, changes the exponent only for $c \ge 8$.`
  - NEW: `Here $E_W(c) = 5, 8, 16, 19, 35, 36, 44, 53$ for $c = 2,\dots,9$; with Schedule~1 alone at every grade (at degree $\kappa_d$ and depth $L_d$), $E_W$ is replaced by $E_1(c)$ of Lemma~\ref{lem:exponent}, and the theorem then does not depend on Theorem~\ref{thm:power-sde}(ii); since $E_W(c) = E_1(c)$ for $c \le 9$ (Lemma~\ref{lem:tb-count-exponent}), the combined rule, and with it that dependence, does not change the exponent for $c \le 9$.`
  - Opportunity, an owner decision: for c ≤ 9 the exponent statement no longer needs the combined rule. `log₂(9K_9) ≈ 1206` is unchanged.
- **B19. `appendix-torsion-blackbox.tex`.**
  - lem:tb-count-grade (l. 1377): `With Schedule~1 alone the same holds with $e_d = d\lceil\log_2(d+1)\rceil$.` → `With Schedule~1 alone the same holds with $e_d = e_{p,d}$ of Lemma~\ref{lem:exponent}.`
  - Proof (ll. 1384–1385): `Schedule~1 at degree $\kappa = \kappa_d \le d$: $B_\kappa(g_d) = \kappa^{\kappa(\kappa-1)\lceil\log_2(\kappa+1)\rceil/2}(g_d+1)^{\kappa\lceil\log_2(\kappa+1)\rceil}$, and $x \mapsto x^{x(x-1)\lceil\log_2(x+1)\rceil/2}$ is nondecreasing on $x \ge 1$.` → `Schedule~1 at degree $\kappa = \kappa_d \le d$: $B_d(g_d) = \kappa^{\kappa(\kappa-1)L_d/2}(g_d+1)^{\kappa L_d}$ with $L_d \le \lceil\log_2(\kappa+1)\rceil$ (Lemma~\ref{lem:zero-sum-length}(i)), and $x \mapsto x^{x(x-1)\lceil\log_2(x+1)\rceil/2}$ is nondecreasing on $x \ge 1$.`
  - **lem:tb-count-exponent (ll. 1393–1415): replace the statement and proof** with:
    ```
    \begin{lemma}[The exponents $E_W(c)$]
    \label{lem:tb-count-exponent}
    For every prime $p > c$ and every $d \ge 2$, $e_d(p) \le e_{p,d}$, with $e_{p,d}$ as in Lemma~\ref{lem:exponent}. Consequently $E_W(c) \le E_1(c)$, and $E_W(c) = E_1(c) = 5, 8, 16, 19, 35, 36, 44, 53$ for $c = 2,\dots,9$, attained for example at $p = 3, 7, 5, 61, 31, 31, 2521, 2521$ (exact computation).
    \end{lemma}
    \begin{proof}
    $e_d(p) = 1 = e_{p,d}$ at a linear grade. At a two-level grade, $e_d(p) = 2 \le \kappa_dL_d$, since $\kappa_d \ge 2$ and $L_d \ge 1$. At a Schedule~1 grade, $e_d(p) = e_{p,d}$. At each listed prime, every grade with $\kappa_d \ge 2$ either is below the Schedule~2 threshold $16\kappa_d^{2\kappa_d+2}$, or has $\kappa_d = 2$ with $(p-1)/2$ even, where $e_{p,d} = 2$ as well (at $p = 2521$); so $1+\sum_d e_d(p) = 1+\sum_d e_{p,d} = E_1(c)$ there.
    \end{proof}
    ```
    Optional growth remark (full version only; CONDITIONAL on a citation check):
    `For $p \ge 4c^4$, $e_{p,d} \le 2\kappa_d \le 2d$, so $1+\sum_d e_{p,d} \le c^2+c-1$. For $p < 4c^4$, $\sum_{d\le c}\gcd(d,p-1) \le c\,\tau(p-1)$ and $\tau(n) = n^{o(1)}$~\cite{HardyWright2008}, so $1+\sum_d e_{p,d} \le 1 + c\,\tau(p-1)\lceil\log_2(c+1)\rceil = c^{1+o(1)}$. Hence $E_1(c) = \Theta(c^2)$.` The Hardy–Wright theorem number is NOT verified (TRAPS 10).
- **B20. `appendix-provenance.tex`.**
  - l. 45 (prov:sde-is-import): append `; the shortened depth $\lceil\log_2 t_{p,\kappa_d}\rceil$ of Lemma~\ref{lem:rounds} is not covered by that confirmation (AI-checked: \file{research/audits/reviews/2026-11-12-rees-exponent-discharge-referee.md}, verdict~(B))`.
  - l. 88 (prov:sde-combined): `($143$ at $c = 9$)` → `($53$ at $c = 9$, equal to $E_1(9)$)`.
  - prov:gc-profiles (l. 157): append `the published-depth profile (exponent $145$) is kept under \texttt{published\_depth\_profile}; the zero-sum depth is computed by \texttt{zero\_sum\_length} in \file{theorems/rees_hsp_reduction.py}`.
  - prov:cl-crossover (l. 164): append `\file{research/audits/reviews/2026-11-12-rees-headline-53/verify_headline.py} and \file{.../crossover_exact8l.py} (the rows at the zero-sum depth, maximized over $p \ge 11$)`.
  - New item `prov:zero-sum-depth` for Lemmas rounds, zero-sum-length and exponent. Status: proved given Theorem is-import, Chevalley–Warning, the Weil bound and Rabin; part (ii) of lem:exponent is an exact computation; AI-checked, pending human review. Scripts as in A23.
- **B21. Tables NOT recomputed** (outside this brief; flag to the integrator).
  - `tab:fcs-budget` (l. 1068), "combined Q" column: the combined rule falls back to Schedule 1 at p = 11, 1031 and 5281, and possibly at the others, so the values change under the new depth.
  - `tab:full-grade-budget` (l. 1020) and `tab:random-column-budget` (l. 1048), which come from `rees_full_grade_budget.json` and `random_column_rees.json`: check whether they use B_d at full depth.
  - The class-3 and class-12 resource profiles, if they use B_d.
  - All of these are NOT computed here.
- **B22. Full proof of thm:main, l. 1096.**
  - `Schedule~1 runs the algorithm of Theorem~\ref{thm:is-import} at the exponent $\kappa_d$` → `Schedule~1 runs Lemma~\ref{lem:rounds} (with the precomputed zero sum) at the exponent $\kappa_d$`.
  - `Since $M_d = B_d(g_d) \ge B_{\kappa_d}(g_d)$, it returns ... deterministically.` → `Since $M_d = B_d(g_d)$, it returns ..., deterministically given the preprocessing.`
  - `So the total error is at most $2\eps/3$.` → `The preprocessing aborts with probability at most $\eps/3$ (Remark~\ref{rem:is-import}(d)), so the total error is at most $\eps$.`
  - `(the inequality $B_d(g_d) \ge B_{\kappa_d}(g_d)$ serves only to make Schedule~1 total)` → delete.
  - In the list of steps behind Theorem main, add Lemmas `lem:rounds` and `lem:zero-sum-length` with their standard imports.

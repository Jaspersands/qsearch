import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from edlib import Ed
HERE = __file__.rsplit('/', 1)[0]
E = Ed('/Users/jaspersands/Developer/qsearch/docs/papers/rees-hsp/core/main-core.tex')

# D1 rem:is-import (a)
E.r('D1-isimport-a', r"""(Were only the $s_i^d$ returned, the $s_i$ could be recovered by Las Vegas root finding for $X^d - s_i^d$ over $\Fp$~\cite{Rabin1980}, charged as in~(d).)""",
    r"""(Were only the $s_i^d$ returned, the $s_i$ could be recovered by Las Vegas root finding for $X^d - s_i^d$ over $\Fp$~\cite{Rabin1980}, charged as in~(d).) Schedule~1H computes its roots by tables or by Las Vegas root finding (Definition~\ref{def:schedule1h}), charged as in~(d).""")

# D2 rem:is-import (d)
E.r('D2-isimport-d', r"""\textup{(d)} \emph{Las Vegas steps.} The preprocessing of Schedule~1 (Lemma~\ref{lem:zero-sum-length}(iv)) is Las Vegas for some pairs $(p,\kappa_d)$. It is charged to the third of the error budget that the merges leave unused (Section~\ref{sec:proof-main}). At each of the at most $c-1$ grades, make up to $\lceil\log_2(3(c-1)/\eps)\rceil$ independent attempts, each cut off after twice its expected running time, so that by Markov's inequality each fails with probability at most $1/2$. Abort the whole procedure, before any query, if every attempt at some grade fails. By the union bound it aborts with probability at most $\eps/3$.
Determinism of the merges is not essential either. Suppose a per-merge solver is only Las Vegas: on every input it either reports failure or returns a solution, which is checked before use; it fails with probability at most $1/4$; and its expected running time is at most an explicit $T(M_d,\log p)$. Cut each attempt off after $4T$ steps; by Markov's inequality an attempt then fails or runs past the cut-off with probability at most $1/2$. The procedure makes $N_{\mathrm{solver}} = (m+\tau)\sum_{d=2}^{c}\prod_{d'=2}^{d-1}M_{d'}$ solver calls, one per merge, a number fixed before the run. Split the same third: make $\lceil\log_2(6(c-1)/\eps)\rceil$ preprocessing attempts per grade and up to $\lceil\log_2(6N_{\mathrm{solver}}/\eps)\rceil$ attempts per call on the same saved labels, and abort if all attempts of any call fail. Each part then aborts with probability at most $\eps/6$. No dilation is applied before a witness is accepted, so retries consume no further quantum sources, and the running time stays polynomial when $T$ is.""",
    r"""\textup{(d)} \emph{Las Vegas steps.} Two kinds of step are Las Vegas, and both are charged to the third of the error budget that the merges leave unused (Section~\ref{sec:proof-main}). The first is the preprocessing: for each degree $\kappa \le c$ dividing $p-1$ at which Schedule~1H calls a solver, a zero sum of $\kappa$-th powers (Lemma~\ref{lem:zero-sum-length}(iv)) and, for even $\kappa$, an element $q$ (Definition~\ref{def:schedule1h}); these are $n_{\mathrm{pre}} \le 2(c-1)$ tasks, each depending only on $(p,\kappa)$. Each attempt at a task is cut off after twice its expected running time, so that by Markov's inequality it fails with probability at most $1/2$ (a trial for $q$ fails with probability $1/2$). The second is the merge solver. Suppose a per-merge solver is only Las Vegas: on every input it either reports failure or returns a solution, which is checked before use; it fails with probability at most $1/4$; and its expected running time is at most an explicit $T(M_d,\log p)$. Schedule~1H is such a solver, with failure probability $0$, since it repeats its random trials until they succeed (Theorem~\ref{thm:halving}(ii)). Cut each attempt off after $4T$ steps; by Markov's inequality an attempt then fails or runs past the cut-off with probability at most $1/2$. The procedure makes $N_{\mathrm{solver}} = (m+\tau)\sum_{d=2}^{c}\prod_{d'=2}^{d-1}M_{d'}$ solver calls, one per merge, a number fixed before the run. Split the third: make up to $\lceil\log_2(6n_{\mathrm{pre}}/\eps)\rceil$ attempts per preprocessing task, and abort the whole procedure, before any query, if every attempt at some task fails; make up to $\lceil\log_2(6N_{\mathrm{solver}}/\eps)\rceil$ attempts per call on the same saved labels, and abort if all attempts of any call fail. By the union bound each part aborts with probability at most $\eps/6$. No dilation is applied before a witness is accepted, so retries consume no further quantum sources, and the running time stays polynomial when $T$ is. With Schedule~1 alone, only the zero sums are Las Vegas, and $\lceil\log_2(3(c-1)/\eps)\rceil$ attempts per grade suffice.""")

# D3 rem:zero-sum
E.r('D3-zerosum', r"""while Schedule~1 allots $B_4(2) = G(4,2)^3 \approx 3.7\cdot 10^{16}$ columns (here $t_{5,4} = 5$).""",
    r"""while Schedule~1 allots $B_4(2) = G(4,2)^3 \approx 3.7\cdot 10^{16}$ columns (here $t_{5,4} = 5$) and Schedule~1H allots $A_4(2) = 243$ (Section~\ref{sec:halving}: two halving stages over $A_2(2) = 9$, then Gaussian elimination).""")

# D4 insert new subsection after lem:exponent proof
sec = open(HERE + '/halving_section.tex').read()
E.r('D4-newsection', r"""For $c \le 8$ the same computation over the primes $c < p < 4c^4$ and one prime $p \ge 4c^4$ in each unit class modulo $N_c$ gives the listed values.
\end{proof}
""", r"""For $c \le 8$ the same computation over the primes $c < p < 4c^4$ and one prime $p \ge 4c^4$ in each unit class modulo $N_c$ gives the listed values.
\end{proof}
""" + sec)

# D5 proof of thm:main, procedure
E.r('D5-proc', r"""Fix the evaluation points $1,\dots,c$ of Lemma~\ref{lem:lifted-source}, put $\tau = \lceil\log_p(3/\eps)\rceil$ and $M_d = B_d(g_d)$ for $2 \le d \le c$. Run the preprocessing of Schedule~1 (Section~\ref{sec:schedule1}) as in Remark~\ref{rem:is-import}(d), and stop with output ``fail'' if it aborts.""",
    r"""Fix the evaluation points $1,\dots,c$ of Lemma~\ref{lem:lifted-source}, put $\tau = \lceil\log_p(3/\eps)\rceil$ and $M_d = A_d(g_d)$ for $2 \le d \le c$. Run the preprocessing of Schedule~1H (Definition~\ref{def:schedule1h}) at every grade, with the cut-off attempts of Remark~\ref{rem:is-import}(d), and stop with output ``fail'' if it aborts.""")
E.r('D5-merge', r"""applies the complete central instrument of Lemma~\ref{lem:instrument} with $Z = Z_d$ to each, runs Schedule~1 (Section~\ref{sec:schedule1}) on the measured labels (with $a = g_d$), and applies the channel""",
    r"""applies the complete central instrument of Lemma~\ref{lem:instrument} with $Z = Z_d$ to each, runs Schedule~1H (Section~\ref{sec:halving}) on the measured labels (with $a = g_d$), with the cut-off attempts of Remark~\ref{rem:is-import}(d) on the saved labels, stopping with output ``fail'' if all attempts of a call fail, and applies the channel""")

# D6 correctness
E.r('D6-correct', r"""The complete central instrument applied to $M_d = B_d(g_d)$ inputs yields labels in $\Fp^{g_d}$, and Schedule~1, that is, Lemma~\ref{lem:rounds} (or linear algebra) at degree $\kappa_d$ followed by Lemma~\ref{lem:bezout}, returns explicit scalars $s_i$ (the witness scalars of~\eqref{eq:sde-target}, not the evaluation points), not all zero, solving~\eqref{eq:sde-target} for every label tuple, deterministically given the preprocessing. By Proposition~\ref{prop:descent} the output is exactly $\rho_{H_dZ_d/Z_d} = \rho_{H_{d-1}}$ for every label tuple, and since it does not depend on the record, the outputs of disjoint input blocks are independent.""",
    r"""The complete central instrument applied to $M_d = A_d(g_d)$ inputs yields labels in $\Fp^{g_d}$, and Schedule~1H, that is, $\mathcal H_{\kappa_d}$ (Theorem~\ref{thm:halving}) followed by Lemma~\ref{lem:bezout}, returns, unless the call aborts, explicit scalars $s_i$ (the witness scalars of~\eqref{eq:sde-target}, not the evaluation points), not all zero, solving~\eqref{eq:sde-target} for every label tuple; its random choices use fresh classical coins. By Proposition~\ref{prop:descent} the output is exactly $\rho_{H_dZ_d/Z_d} = \rho_{H_{d-1}}$ for every label tuple and every nonzero solution, so it depends neither on the record nor on the coins, and the outputs of disjoint input blocks are independent.""")
E.r('D6-correct-b', r"""So the ideal procedure, given a completed preprocessing, fails with probability at most $\eps/3$. Given the preprocessing, Schedule~1 is deterministic and total at its arity, so the merges add no failure. The preprocessing aborts with probability at most $\eps/3$ (Remark~\ref{rem:is-import}(d)), before any query.""",
    r"""So the ideal procedure, given a completed preprocessing and no aborted solver call, fails with probability at most $\eps/3$. The preprocessing and the solver calls together abort with probability at most $\eps/3$ (Remark~\ref{rem:is-import}(d)); the preprocessing aborts before any query.""")

# D7 approximation
E.r('D7-approx', r"""This number is fixed before the run, because the arities of Schedule~1 are computed from the public data $(p,d,g_d)$ before any query and there are no restarts, so the allocation below is legitimate.""",
    r"""This number is fixed before the run, because the arities $A_d$ are computed from the public data $(p,d,g_d)$ before any query and a repeated solver attempt reuses the saved labels of its merge, so that no quantum step is repeated; the allocation below is therefore legitimate.""")

# D8 query count
E.r('D8-query', r"""so the procedure makes $c(m+\tau)\prod_{d=2}^cB_d(g_d) = Q_{\mathrm q}$ queries; it makes none if the preprocessing aborts. Since $g_d \le m$, Lemma~\ref{lem:exponent} gives
\[
  B_d(g_d) \le d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}\,(m+1)^{e_{p,d}},
\]
and the product over $d$ gives the bound $C_c\,c\,(m+\tau)(m+1)^{\sum_d e_{p,d}} \le C_c\,c\,(m+\tau)(m+1)^{E_1(c)-1}$ of Theorem~\ref{thm:main}. This is the only step that uses the explicit form of $B_d$; the other steps use only the properties listed in Remark~\ref{rem:main-solver}.""",
    r"""so the procedure makes at most $c(m+\tau)\prod_{d=2}^cA_d(g_d) = Q_{\mathrm q}$ queries; it makes none if the preprocessing aborts. Since $g_d \le m$, Lemma~\ref{lem:halved-exponent}(iii) gives $\prod_dA_d(g_d) \le C^H_c(m+1)^{\sum_de^H_{p,d}}$, hence the bound $C^H_c\,c\,(m+\tau)(m+1)^{E_H(c)-1}$ of Theorem~\ref{thm:main}(4). Since $A_d \le B_d$, Lemma~\ref{lem:exponent} gives
\[
  A_d(g_d) \le B_d(g_d) \le d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2}\,(m+1)^{e_{p,d}},
\]
and the product over $d$ gives the second bound, $C_c\,c\,(m+\tau)(m+1)^{\sum_d e_{p,d}} \le C_c\,c\,(m+\tau)(m+1)^{E_1(c)-1}$. This is the only step that uses the explicit form of the arities; the other steps use only the properties listed in Remark~\ref{rem:main-solver}.""")

# D9 running time
E.r('D9-time', r"""one call of Schedule~1, which runs in time $\poly(M_d,\log p)$ by Lemmas~\ref{lem:rounds} and~\ref{lem:bezout}, and $M_d$ controlled right translations""",
    r"""at most $\lceil\log_2(6N_{\mathrm{solver}}/\eps)\rceil$ attempts of Schedule~1H, each cut off after $4T(M_d,\log p)$ steps with $T$ the polynomial of Theorem~\ref{thm:halving}(ii) (and $\log N_{\mathrm{solver}} = O_c(\log m + \log\tau)$), and $M_d$ controlled right translations""")
E.r('D9-time-b', r"""The preprocessing makes at most $(c-1)\lceil\log_2(3(c-1)/\eps)\rceil$ cut-off attempts, each of time $\poly(\log p)$ for fixed $c$ (Lemma~\ref{lem:zero-sum-length}(iv)).""",
    r"""The preprocessing makes at most $n_{\mathrm{pre}}\lceil\log_2(6n_{\mathrm{pre}}/\eps)\rceil$ cut-off attempts, $n_{\mathrm{pre}} \le 2(c-1)$, each of time $\poly(\log p)$ for fixed $c$ (Lemma~\ref{lem:zero-sum-length}(iv) and Definition~\ref{def:schedule1h}), and builds the tables of Definition~\ref{def:schedule1h}, needed only at degrees $\kappa$ with $p < 4\kappa^4$, in $O_c(1)$ operations.""")

# D10 rem:oblivious
E.r('D10-obl', r"""the preprocessing of Schedule~1 depends only on $p$, $c$ and $\eps$, makes no query and is cut off; apart from its cut-off classical attempts, made before the first query, there are no restarts; and Schedule~1 returns scalars for every label tuple, within the time of Lemma~\ref{lem:rounds}, which is stated for arbitrary $\lambda_i$, and of the conversion to the exponent $d$.""",
    r"""the preprocessing of Schedule~1H depends only on $p$, $c$ and $\eps$, makes no query and is cut off; apart from cut-off classical attempts (those of the preprocessing, made before the first query, and the repeated attempts of a solver call on its saved labels), there are no restarts; and within its cut-offs Schedule~1H returns scalars or reports failure for every label tuple, by Theorem~\ref{thm:halving}, which is stated for arbitrary columns, and the conversion to the exponent $d$.""")

# D11 Heisenberg example
E.r('D11-heis', r"""while Schedule~1 allots $B_2(1) = G(2,1) = 8$ when $p \equiv 1 \pmod 4$ and $G(2,1)^2 = 64$ when $p \equiv 3 \pmod 4$ (Lemma~\ref{lem:zero-sum-length}(ii)); either count makes Proposition~\ref{prop:descent} output""",
    r"""while Schedule~1 alone would allot $B_2(1) = G(2,1) = 8$ when $p \equiv 1 \pmod 4$ and $G(2,1)^2 = 64$ when $p \equiv 3 \pmod 4$ (Lemma~\ref{lem:zero-sum-length}(ii)), and Schedule~1H allots $A_2(1) = 4$ for every $p$ (Remark~\ref{rem:kappa-two}): a linear relation on each of two pairs of labels, split into its square and nonsquare coefficients, gives two vectors with two representations each, and one linear relation between these two vectors finishes. Any of these counts makes Proposition~\ref{prop:descent} output""")

# D12 rem:proof-uses
E.r('D12-proofuses', r"""The proof uses Theorem~\ref{thm:is-import} and Lemma~\ref{lem:rounds} only through their guarantees on arbitrary columns,""",
    r"""The proof uses Theorem~\ref{thm:is-import}, Lemma~\ref{lem:rounds} and Theorem~\ref{thm:halving} only through their guarantees on arbitrary columns,""")
E.r('D12-proofuses-b', r"""the witness depends only on the measured labels, the public data $(p, d, g_d)$ and the zero sums computed before any query.""",
    r"""the witness depends only on the measured labels, the public data $(p, d, g_d)$, the preprocessing done before any query and the classical coins of the solver.""")

# D13 class-3 example
E.r('D13-c3-stage3', r"""Schedule~1 allots $B_3(2) = G(3,2) = 729$ when $p \equiv 1 \pmod 3$, since then $\kappa_3 = 3$ and $t_{p,3} = 2$, and $g_3+1 = 3$ when $p \equiv 2 \pmod 3$.""",
    r"""Schedule~1H, which here is Schedule~1 because $\kappa_3$ is odd, allots $A_3(2) = B_3(2) = G(3,2) = 729$ when $p \equiv 1 \pmod 3$, since then $\kappa_3 = 3$ and $t_{p,3} = 2$, and $g_3+1 = 3$ when $p \equiv 2 \pmod 3$.""")
E.r('D13-c3-stage2', r"""Schedule~1 allots $B_2(3) = G(2,3) = 32$ when $p \equiv 1 \pmod 4$ and $G(2,3)^2 = 1024$ when $p \equiv 3 \pmod 4$.""",
    r"""Schedule~1 alone would allot $B_2(3) = G(2,3) = 32$ when $p \equiv 1 \pmod 4$ and $G(2,3)^2 = 1024$ when $p \equiv 3 \pmod 4$; Schedule~1H allots $A_2(3) = 16$ for every $p$ (Remark~\ref{rem:kappa-two}).""")
E.r('D13-c3-count', r"""The count of Theorem~\ref{thm:main} is at most $Q_{\mathrm q} = 3(5+\tau)\cdot1024\cdot729$, about $2^{23.68}$ at $\tau = 1$, with equality when $p \equiv 7 \pmod{12}$.""",
    r"""The count of Theorem~\ref{thm:main} is $Q_{\mathrm q} = 3(5+\tau)\cdot16\cdot729$, about $2^{17.68}$ at $\tau = 1$, when $p \equiv 1 \pmod 3$, and $3(5+\tau)\cdot16\cdot3$ when $p \equiv 2 \pmod 3$ (with Schedule~1 alone it would be up to $3(5+\tau)\cdot1024\cdot729 \approx 2^{23.68}$).""")

# D14 table caption and rows
E.r('D14-caption', r"""Here $Q_{\mathrm q}$ is the largest value, over the primes $p \ge 11$, of the count of Theorem~\ref{thm:main}, which depends on $p$ through the $\kappa_d$ and $L_d$. The maximum is attained at $p \equiv 3 \pmod 4$ for the Heisenberg row, at $p \equiv 7 \pmod{12}$ for the class-three rows, and at $p \equiv 2521 \pmod{5040}$ for the last row.""",
    r"""Here $Q_{\mathrm q}$ is the largest value, over the primes $p \ge 11$, of the count of Theorem~\ref{thm:main}, which depends on $p$ through the arities $A_d$ of Schedule~1H. The maximum is attained at every $p$ for the Heisenberg row, at $p \equiv 1 \pmod 3$ for the class-three rows, and at $p \equiv 1 \pmod{2520}$ for the last row.""")
E.r('D14-caption-b', r"""For $p$ below the value in the next column, the classical algorithm of Proposition~\ref{prop:classical-query}(v) uses fewer than $Q_{\mathrm q}$ queries; this column is computed with $8\ell = 8\ln 6 \approx 14.33$ rounded up to $15$, which only enlarges $Q$, so the listed values are conservative (with $8\ell$ itself they are $86$, $3{,}375$, $1{,}585$ and $98$, so the thresholds are the primes up to $83$, $3{,}373$, $1{,}583$ and $97$).""",
    r"""For $p$ below the value in the next column, the classical algorithm of Proposition~\ref{prop:classical-query}(v) uses fewer than $Q_{\mathrm q}$ queries (for the Heisenberg row it uses more at every $p \ge 11$); this column is computed with $8\ell = 8\ln 6 \approx 14.33$ rounded up to $15$, which only enlarges $Q$, so the listed values are conservative (with $8\ell$ itself they are $310$, $198$ and $27$, so the thresholds are the primes up to $307$, $197$ and $23$).""")
E.r('D14-rows', r"""Heisenberg & 2 & 3 & $(1)$ & $9.00$ & $443$ & $84$ & $81$ \\
filiform & 3 & 4 & $(2,1)$ & $20.00$ & $9{,}391$ & $3{,}325$ & $218$ \\
free, two generators & 3 & 5 & $(3,2)$ & $23.68$ & $3{,}413$ & $1{,}567$ & $293$ \\
Dixmier--Lister & 3 & 8 & $(4,2)$ & $25.55$ & $157$ & $97$ & $474$ \\
class-$\ReesClassNineClass$ profile & 9 & 19 & $(17,16,14,12,9,6,3,1)$ & $563.63$ & $\approx 2^{62.60}$ & $\approx 2^{62.35}$ & $22{,}548$ \\""",
    r"""Heisenberg & 2 & 3 & $(1)$ & $5.00$ & $29$ & none & $50$ \\
filiform & 3 & 4 & $(2,1)$ & $14.83$ & $863$ & $305$ & $163$ \\
free, two generators & 3 & 5 & $(3,2)$ & $17.68$ & $431$ & $196$ & $221$ \\
Dixmier--Lister & 3 & 8 & $(4,2)$ & $18.91$ & $41$ & $27$ & $350$ \\
class-$\ReesClassNineClass$ profile & 9 & 19 & $(17,16,14,12,9,6,3,1)$ & $314.06$ & $\approx 2^{34.87}$ & $\approx 2^{34.62}$ & $12{,}565$ \\""")

# D15 rem:query-separation (b)
E.r('D15-qsep', r"""For the class-$\ReesClassNineClass$ profile of that table, an advantage needs $p > 2^{62.6}$.""",
    r"""For the class-$\ReesClassNineClass$ profile of that table, an advantage needs $p > 2^{34.8}$.""")
E.save()

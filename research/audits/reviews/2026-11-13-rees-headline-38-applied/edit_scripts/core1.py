import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from edlib import Ed
E = Ed('/Users/jaspersands/Developer/qsearch/docs/papers/rees-hsp/core/main-core.tex')

# C1 abstract
E.r('C1-abstract', r"the query separation is not new, the exponent of $m$ is $\Omega(c^2)$, and no application is known.",
    r"the query separation is not new, the exponent of $m$ is $\Omega(c^2)$ (at most $\ReesClassNineHalvedExp$ at $c = 9$), and no application is known.")

# C2 eq:Bd paragraph
E.r('C2-Bd', r"is at most the arity $\bar B_d(a) \coloneqq G(d,a)^{\lceil\log_2(d+1)\rceil}$ of~\cite[proof of Theorem~3]{IvanyosSantha2015} (Lemma~\ref{lem:bezout}).",
    r"is at most the arity $\bar B_d(a) \coloneqq G(d,a)^{\lceil\log_2(d+1)\rceil}$ of~\cite[proof of Theorem~3]{IvanyosSantha2015} (Lemma~\ref{lem:bezout}). The algorithm uses Schedule~1H (Section~\ref{sec:halving}), which at even $\kappa_d$ may call a solver for the exponent $\kappa_d/2$ instead; its arity $A_d(a) \le B_d(a)$ is the least arity among Schedule~1 and the halving plans of Definition~\ref{def:schedule1h}, and is also computed from $(p,d,a)$ before the run.")

# C3 thm:main(3)
E.r('C3-thm3', r"""    Q_{\mathrm q} = c\,(m + \tau)\prod_{d=2}^{c} B_d(g_d)
  \]
  queries in case~\textup{(a)}, or uses at most $Q_{\mathrm q}$ copies of $\rho_H$ in case~\textup{(b)}, with $B_d$ as in~\eqref{eq:Bd} (so $Q_{\mathrm q}$ depends on $p$ through the $\kappa_d$ and $L_d$, and $Q_{\mathrm q} \le c\,(m+\tau)\prod_{d=2}^{c}\bar B_d(g_d)$).""",
    r"""    Q_{\mathrm q} = c\,(m + \tau)\prod_{d=2}^{c} A_d(g_d)
  \]
  queries in case~\textup{(a)}, or uses at most $Q_{\mathrm q}$ copies of $\rho_H$ in case~\textup{(b)}, with $A_d$ the arity of Schedule~1H (Definition~\ref{def:schedule1h}) (so $Q_{\mathrm q}$ depends on $p$ through the $\kappa_d$, the $t_{p,\kappa}$ and the sets of Section~\ref{sec:halving}, and $Q_{\mathrm q} \le c\,(m+\tau)\prod_{d=2}^{c}B_d(g_d) \le c\,(m+\tau)\prod_{d=2}^{c}\bar B_d(g_d)$, with $B_d$ and $\bar B_d$ as in~\eqref{eq:Bd}).""")

# C4 thm:main(4)
E.r('C4-thm4', r"""  \item \emph{Explicit bound.} The count satisfies
  \[
    Q_{\mathrm q} \;\le\; C_c\, c\,(m+\tau)\,(m+1)^{E_1(c)-1},
    \qquad
    C_c = \prod_{d=2}^c d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2},
  \]
  where $E_1(c) \le 1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ is the exponent of Lemma~\ref{lem:exponent}; $E_1(\ReesClassNineClass) = \ReesClassNineQueryExp$.""",
    r"""  \item \emph{Explicit bound.} The count satisfies
  \[
    Q_{\mathrm q} \;\le\; C^H_c\, c\,(m+\tau)\,(m+1)^{E_H(c)-1}
    \quad\text{and}\quad
    Q_{\mathrm q} \;\le\; C_c\, c\,(m+\tau)\,(m+1)^{E_1(c)-1},
    \qquad
    C_c = \prod_{d=2}^c d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2},
  \]
  where $E_H(c) \le E_1(c) \le 1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ are the exponents of Lemmas~\ref{lem:halved-exponent} and~\ref{lem:exponent}, and $C^H_c$ depends only on $c$, with $C^H_c = C_c$ for $c \le 9$ (Lemma~\ref{lem:halved-exponent}(iii)). In particular $E_H(\ReesClassNineClass) = \ReesClassNineHalvedExp$; Schedule~1 alone gives $E_1(\ReesClassNineClass) = \ReesClassNineQueryExp$.""")

# C5 paragraph after theorem
E.r('C5-after', r"""The algorithm is the procedure of Section~\ref{sec:proof-main}: it uses the evaluation points $1,\dots,c$ and Schedule~1 (Section~\ref{sec:schedule1}) with arity $M_d = B_d(g_d)$ at every grade $d = 2,\dots,c$, after a classical preprocessing that computes one zero sum of $\kappa_d$-th powers per grade (Lemma~\ref{lem:zero-sum-length}).""",
    r"""The algorithm is the procedure of Section~\ref{sec:proof-main}: it uses the evaluation points $1,\dots,c$ and Schedule~1H (Section~\ref{sec:halving}) with arity $M_d = A_d(g_d)$ at every grade $d = 2,\dots,c$, after a classical preprocessing that computes, for each degree it needs, a zero sum of $\kappa$-th powers (Lemma~\ref{lem:zero-sum-length}), a coset representative and finite tables (Definition~\ref{def:schedule1h}).""")

# C6 rem:main-solver
E.r('C6-mainsolver', r"""The proof (Section~\ref{sec:proof-main}) uses only four properties of Schedule~1 at grade $d$: it is total, returning the scalars $s_1,\dots,s_{M_d}$ of a nonzero solution of~\eqref{eq:sde-target} (not only their $d$-th powers; Remark~\ref{rem:is-import}(a)) for any $M_d$ label columns in $\Fp^{g_d}$ and every prime $p > c$; given the zero sums of the preprocessing, which depend only on $(p,\kappa_d)$ and are computed before any query, it is deterministic; it runs in time polynomial in $M_d$ and $\log p$; and its arity $M_d$ is polynomial in $g_d$, uniformly in $p$, and computable from the public data $(p,d,g_d)$ before the run. Any per-grade solver with these properties gives the same theorem, by the same proof, with its arity in place of $B_d(g_d)$ in $M_d$ and $Q_{\mathrm q}$; determinism may be relaxed to Las Vegas (Remark~\ref{rem:is-import}(d)). Beyond these properties, the proof uses the explicit form of $B_d$ only for the displayed upper bound on $Q_{\mathrm q}$. That explicit $B_d$, and hence the exponent $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$, rests on Lemma~\ref{lem:rounds}, which accumulates the collisions of~\cite[Theorem~11]{IvanyosSantha2015} and closes with the shortest zero sum, on Lemma~\ref{lem:zero-sum-length} and on the exact computation of Lemma~\ref{lem:exponent}. G.~Ivanyos has confirmed the full-depth bound $C(d,a) \le G(d,a)^{\lceil\log_2(d+1)\rceil}$ of Remark~\ref{rem:is-printed}, which gives the weaker exponent $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ ($145$ at $c = 9$). His confirmation does not cover the shorter depth $L_d$: Lemma~\ref{lem:rounds} is proved here and has been checked and refereed by AI only, pending human review.""",
    r"""The proof (Section~\ref{sec:proof-main}) uses only four properties of Schedule~1H at grade $d$: it is total, returning, unless it reports failure, the scalars $s_1,\dots,s_{M_d}$ of a nonzero solution of~\eqref{eq:sde-target} (not only their $d$-th powers; Remark~\ref{rem:is-import}(a)) for any $M_d$ label columns in $\Fp^{g_d}$ and every prime $p > c$, and it checks them; given the preprocessing, which depends only on $p$ and $c$ and is done before any query, it is Las Vegas, with an explicit expected running time polynomial in $M_d$ and $\log p$ (Theorem~\ref{thm:halving}), and is charged as in Remark~\ref{rem:is-import}(d); and its arity $M_d$ is polynomial in $g_d$, uniformly in $p$, and computable from the public data $(p,d,g_d)$ before the run. Any per-grade solver with these properties gives the same theorem, by the same proof, with its arity in place of $A_d(g_d)$ in $M_d$ and $Q_{\mathrm q}$. Schedule~1 alone, with arity $B_d(g_d)$, is one, and is deterministic given its zero sums. Beyond these properties, the proof uses the explicit arities only for the displayed upper bounds on $Q_{\mathrm q}$. The exponent $\ReesClassNineHalvedExp$ at $c = \ReesClassNineClass$ rests on Lemma~\ref{lem:rounds}, which accumulates the collisions of~\cite[Theorem~11]{IvanyosSantha2015} and closes with the shortest zero sum, on Lemma~\ref{lem:zero-sum-length}, on the halving of Section~\ref{sec:halving} (Lemmas~\ref{lem:stage}, \ref{lem:finish} and~\ref{lem:two-term} and Theorem~\ref{thm:halving}) and on the exact computation of Lemma~\ref{lem:halved-exponent}; without the halving, Schedule~1 gives $\ReesClassNineQueryExp$ (Lemma~\ref{lem:exponent}). G.~Ivanyos has confirmed the full-depth bound $C(d,a) \le G(d,a)^{\lceil\log_2(d+1)\rceil}$ of Remark~\ref{rem:is-printed}, which with Schedule~1 alone gives the weaker exponent $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ ($145$ at $c = 9$), and $95$ with the halving (Section~\ref{sec:outlook}). His confirmation covers neither the shorter depth $L_d$ nor the halving: Lemma~\ref{lem:rounds} and Section~\ref{sec:halving} are proved here and have been checked and refereed by AI only, pending human review.""")

# C7 exponent / imports paragraph
E.r('C7-imports-a', r"""The exponent $E_1(c)$ of $m$ lies between $c(c+1)/2$ and $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ (Lemma~\ref{lem:exponent}), so the bound is polynomial for each fixed $c$ and is not uniform in $c$; at $c = \ReesClassNineClass$ the exponent of $m$ in $Q_{\mathrm q}$ is at most $\ReesClassNineQueryExp$, for every prime $p > \ReesClassNineClass$.""",
    r"""The exponent $E_H(c)$ of $m$ lies between $\lceil c/2\rceil^2 + 2\lfloor c/2\rfloor$ and $E_1(c) \le 1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ (Lemmas~\ref{lem:halved-exponent} and~\ref{lem:exponent}), so the bound is polynomial for each fixed $c$ and is not uniform in $c$; at $c = \ReesClassNineClass$ the exponent of $m$ in $Q_{\mathrm q}$ is at most $\ReesClassNineHalvedExp$, for every prime $p > \ReesClassNineClass$ ($\ReesClassNineQueryExp$ with Schedule~1 alone).""")
E.r('C7-imports-b', r"""three standard results on finite fields used in Lemma~\ref{lem:zero-sum-length}, namely the Chevalley--Warning theorem, Weil's bound for diagonal equations in two variables~\cite[Chapter~6]{LidlNiederreiter1997} and Las Vegas root finding~\cite{Rabin1980};""",
    r"""three standard results on finite fields used in Lemmas~\ref{lem:zero-sum-length} and~\ref{lem:two-term} and Theorem~\ref{thm:halving}, namely the Chevalley--Warning theorem, Weil's bound for diagonal equations in two variables with nonzero right side~\cite[Chapter~6]{LidlNiederreiter1997} and Las Vegas root finding~\cite{Rabin1980};""")
E.r('C7-imports-c', r"""the value $E_1(\ReesClassNineClass) = \ReesClassNineQueryExp$ also uses an exact computation (Lemma~\ref{lem:exponent}).""",
    r"""the values $E_H(\ReesClassNineClass) = \ReesClassNineHalvedExp$ and $E_1(\ReesClassNineClass) = \ReesClassNineQueryExp$ also use exact computations (Lemmas~\ref{lem:halved-exponent} and~\ref{lem:exponent}).""")

# C8 what is new
E.r('C8-new', r"""The elimination and its solver are those of~\cite{IvanyosSantha2015}, the query separation""",
    r"""The elimination is that of~\cite{IvanyosSantha2015}, and the solver is built on their collision step; the halving of Section~\ref{sec:halving} keeps several representations of one vector, in the spirit of the accumulation in~\cite[Section~3.3]{IvanyosSantha2015}, and we claim no priority for it. The query separation""")

# C9 proof overview (c)
E.r('C9-overview', r"""The Ivanyos--Santha collision step, iterated $L_d$ times and closed with the shortest zero sum of $\kappa_d$-th powers, supplies the solutions for arbitrary labels at arity $B_d(g_d)$.""",
    r"""The Ivanyos--Santha collision step, iterated $L_d$ times and closed with the shortest zero sum of $\kappa_d$-th powers, and, at even $\kappa_d$, the halving of Section~\ref{sec:halving}, which turns a solver for the exponent $\kappa_d/2$ into one for $\kappa_d$ by keeping two representations of one vector, supply the solutions for arbitrary labels at arity $A_d(g_d)$.""")

# C10 status
E.r('C10-status', r"""The arity of Schedule~1, and with it the exponent $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$, rests on Lemma~\ref{lem:rounds}, which is proved here and has been checked and refereed by AI only; G.~Ivanyos has confirmed only the weaker full-depth bound of Remark~\ref{rem:is-printed}.""",
    r"""The arity of Schedule~1, and with it the exponent $\ReesClassNineQueryExp$ of Schedule~1 alone at $c = \ReesClassNineClass$, rests on Lemma~\ref{lem:rounds}, which is proved here and has been checked and refereed by AI only; G.~Ivanyos has confirmed only the weaker full-depth bound of Remark~\ref{rem:is-printed}. The stated exponent $\ReesClassNineHalvedExp$ rests on everything $\ReesClassNineQueryExp$ rests on and, in addition, on the halving of Section~\ref{sec:halving}, which was proved by one AI session and refereed by another (verdict: correct with fixes, all applied here), and on the exact computation of Lemma~\ref{lem:halved-exponent}; no human has read it.""")

# C11 organization
E.r('C11-org', r"""Section~\ref{sec:schedule1} states the diagonal-equation solver.""",
    r"""Section~\ref{sec:schedule1} states the diagonal-equation solvers, Schedule~1 and Schedule~1H.""")
E.save()

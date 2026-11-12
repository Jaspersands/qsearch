import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from edlib import Ed
E = Ed('/Users/jaspersands/Developer/qsearch/docs/papers/rees-hsp/core/main-core.tex')
E.r('F1-title', r"\begin{remark}[What the proof uses from Schedule~1]", r"\begin{remark}[What the proof uses from the solver]")
E.r('F2-bb', r"with a row-reduced complement in place of the chart lemma used there, stated with Schedule~1 alone.",
    r"with a row-reduced complement in place of the chart lemma used there, stated with the solver of Theorem~\ref{thm:main} alone (no Schedule~2).")
E.r('F3-nil', r"Corollary~\ref{cor:nilpotent} is proved in Section~\ref{sec:nilpotent} with Schedule~1 alone.",
    r"Corollary~\ref{cor:nilpotent} is proved in Section~\ref{sec:nilpotent} with Schedule~1H alone (no Schedule~2).")
E.r('F4-thmfix', r"(Definition~\ref{def:schedule1h}) (so $Q_{\mathrm q}$ depends on $p$", r"(Definition~\ref{def:schedule1h}); so $Q_{\mathrm q}$ depends on $p$")
E.r('F4b', r"with $B_d$ and $\bar B_d$ as in~\eqref{eq:Bd}).", r"with $B_d$ and $\bar B_d$ as in~\eqref{eq:Bd}.")
E.save()

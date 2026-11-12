import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from edlib import Ed
E = Ed('/Users/jaspersands/Developer/qsearch/docs/papers/rees-hsp/core/main-core.tex')
E.r('O3b', r"""With Schedule~1 at the full depth $\lceil\log_2(\kappa+1)\rceil$ instead, which the confirmation of Remark~\ref{rem:is-printed} covers and which does not use Lemma~\ref{lem:rounds}, the same halving gives""",
    r"""With Schedule~1 at the full depth $\lceil\log_2(\kappa+1)\rceil$ instead, that is, with the arity of the proof of~\cite[Theorem~3]{IvanyosSantha2015}, which the confirmation of Remark~\ref{rem:is-printed} covers, so that the shorter depth $L_d$ is not used, the same halving gives""")
E.save()

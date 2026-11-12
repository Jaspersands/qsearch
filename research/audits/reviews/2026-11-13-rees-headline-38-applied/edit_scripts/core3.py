import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from edlib import Ed
E = Ed('/Users/jaspersands/Developer/qsearch/docs/papers/rees-hsp/core/main-core.tex')

# O1 outlook preamble
E.r('O1-pre', r"""their derivations are in the full version, except for the paragraph on halving the degree, whose derivation is in research notes (Appendix~\ref{app:artifacts}).""",
    r"""their derivations are in the full version, except for the paragraph on halving at the confirmed depth, whose computation is in research notes (Appendix~\ref{app:artifacts}).""")

# O2 smaller arities: 53 is Schedule 1 alone; 40/37 do not use halving
E.r('O2-small-a', r"""choosing between Schedule~1 and Schedule~2 at each grade does not lower the exponent $\ReesClassNineQueryExp$ of $m$ at $c = 9$""",
    r"""choosing between Schedule~1 and Schedule~2 at each grade does not lower the exponent $\ReesClassNineQueryExp$ of Schedule~1 alone at $c = 9$""")
E.r('O2-small-b', r"""further constructions of the full version (coset-refinement towers and chains) would lower it to $37$ (finite computations over the exceptional primes).""",
    r"""further constructions of the full version (coset-refinement towers and chains) would lower it to $37$ (finite computations over the exceptional primes). These combinations do not use the halving of Section~\ref{sec:halving}, which by itself gives $\ReesClassNineHalvedExp$; how far the two can be combined is not claimed here.""")

# O3 replace halving paragraph
start = r"""\paragraph{Halving the degree.} A further device would lower the class-nine exponent"""
end = r"""Status: AI-proved and refereed by AI, pending human review; it is not in the full version.
"""
i = E.s.index(start); j = E.s.index(end, i) + len(end)
assert E.s.count(start) == 1
new = r"""\paragraph{Halving at the confirmed depth.} Theorem~\ref{thm:main} uses Schedule~1 at the depth $L_d$ of~\eqref{eq:Bd} inside Schedule~1H. With Schedule~1 at the full depth $\lceil\log_2(\kappa+1)\rceil$ instead, which the confirmation of Remark~\ref{rem:is-printed} covers and which does not use Lemma~\ref{lem:rounds}, the same halving gives the class-nine exponent $95$ in place of $145$ (exact computation for $p \le 30000$ and a computation over the residues modulo $2520$ above; AI-checked and refereed by AI, pending human review).
"""
E.s = E.s[:i] + new + E.s[j:]
E.log.append('O3-halving-par')

# O4 open problem (1)
E.r('O4-open', r"""(1) The exponent of $m$ in Theorem~\ref{thm:main} grows at least quadratically in $c$ (Lemma~\ref{lem:exponent}),""",
    r"""(1) The exponent of $m$ in Theorem~\ref{thm:main} grows at least quadratically in $c$ (Lemmas~\ref{lem:exponent} and~\ref{lem:halved-exponent}),""")

# A1 artifacts: halving item
E.r('A1-art', r"""  \item Halving the degree (Section~\ref{sec:outlook}): \file{research/audits/reviews/2026-11-12-rees-exponent-k8-attack.md} and its referee report \file{research/audits/reviews/2026-11-12-rees-exponent-38-referee.md}, with the scripts and outputs in the folders of the same names.""",
    r"""  \item Schedule~1H and its exponent (Section~\ref{sec:halving}, Lemma~\ref{lem:halved-exponent}, Table~\ref{tab:query-crossover}): \file{research/audits/reviews/2026-11-13-rees-headline-38-applied/halved_schedule.py}, with its outputs \file{halved_schedule.json} and \file{halved_schedule.out} in the same folder. It computes, by class sumsets and with no Weil shortcut, $t_{p,\kappa}$, the sets $T_j$, the degrees, arities and constants $K_\kappa$ of Definition~\ref{def:schedule1h} for every prime $p < 26244$ and $\kappa \le 9$ dividing $p-1$, checks $T_1 = \Fp^\times$ and $t_{p,\kappa} \le 3$ at every prime in $[4\kappa^4, 30000]$, evaluates every unit residue class modulo $5040$ above, and computes the table. An independently written program for a slightly larger family of plans (up to four stages, with an extra finish), \file{research/audits/reviews/2026-11-12-rees-exponent-38-referee/s1h_independent.py}, exact up to $30000$, gives the same values $E_H(c)$, $c \le 9$; \file{pub_hcd.py} in the same folder gives the value $95$ of Section~\ref{sec:outlook}. The derivation is \file{research/audits/reviews/2026-11-12-rees-exponent-k8-attack.md}, and its referee report is \file{research/audits/reviews/2026-11-12-rees-exponent-38-referee.md}.""")
E.r('A2-macros', r"""\file{numbers.tex} in the arXiv source is its output.""",
    r"""\file{numbers.tex} in the arXiv source is its output, except for the exponent $\ReesClassNineHalvedExp$ of Lemma~\ref{lem:halved-exponent}, which was added to it by hand from the computation above.""")
# A3 finite checks: executors
E.r('A3-exec', r"""  \item BCH recurrence: \file{theorems/uniform_bch_rees.py}""",
    r"""  \item Schedule~1H: \file{research/audits/reviews/2026-11-13-rees-headline-38-applied/halving_executor.py} runs the plans of Definition~\ref{def:schedule1h} with a brute-force inner solver for $\kappa = 2, 4, 6, 8$ at $16$ pairs $(p,\kappa)$, among them $\kappa = 6$ at $p = 7, 13, 31, 37, 61$ and $\kappa = 8$ at $p = 17, 41$, on random and adversarial columns, and \file{research/audits/reviews/2026-11-12-rees-exponent-38-referee/hcd_executor.py} runs halving plans recursively, with Gaussian elimination as the only base solver, for $\kappa = 2, 4, 8$ at primes up to $2521$; every output is an exactly verified solution.
  \item BCH recurrence: \file{theorems/uniform_bch_rees.py}""")
E.save()

"""Apply the 2026-11-13 full-version edits (tables at the zero-sum depth, preprocessing time,
prop:mixed-schedule error split). Every old string must occur exactly once; nothing is written
unless every edit of a file matches. Backups: research/audits/reviews/2026-11-09-rees-paper-pass-prep/
backup-pre-fulltables-2026-11-13/.

Run (repo root): /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-full-tables/apply_edits.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / "docs/papers/rees-hsp"

EDITS = {}

# ------------------------------------------------------------------ main.tex
EDITS["main.tex"] = [
    # E1 tab:fcs-budget combined column (zero-sum depth; recompute_fcs.py)
    ("$11$ & $202.1$ &", "$11$ & $118.7$ &"),
    ("$1031$ & $167.3$ &", "$1031$ & $83.9$ &"),
    ("$5281$ & $852.3$ &", "$5281$ & $271.5$ &"),
    ("$2^{31}-1$ & $940.3$ &", "$2^{31}-1$ & $355.0$ &"),
    ("$2^{61}-1$ & $533.4$ &", "$2^{61}-1$ & $164.1$ &"),
    # E2 caption: worst-case values and the published-depth values
    ("Without the block-steered option, that is, under the worst-case rule alone, it reads $944.9$, $555.4$ and $61.5$ at the last three rows.",
     "Without the block-steered option, that is, under the worst-case rule alone, it reads $359.6$, $186.1$ and $61.5$ at the last three rows. "
     "The combined column and these three values use Schedule~1 at the depth $L_d$ of~\\eqref{eq:Bd} (Lemma~\\ref{lem:rounds}); "
     "at the full depth $\\lceil\\log_2(\\kappa_d+1)\\rceil$ of Remark~\\ref{rem:is-import}(c), which G.~Ivanyos's confirmation covers, "
     "the combined column reads $202.1$, $167.3$, $852.3$, $940.3$, $533.4$ and $41.4$, and the worst-case rule $944.9$, $555.4$ and $61.5$ at the last three rows. "
     "No other column uses a Schedule~1 grade at these primes, so none of them depends on the depth."),
    # E3 triangular paragraph (prop:triangular-sde scope), l. 884
    ("for example, at $p=2^{61}-1$ it would lower the worst-case combined count given in the caption of Table~\\ref{tab:fcs-budget} from $2^{555.4}$ to $2^{542.0}$ (finite computation, item~\\ref{prov:sde-triangular}), while the block-steered option of Remark~\\ref{rem:combined-schedule}, which uses the label law, gives $2^{533.4}$ there.",
     "for example, at $p=2^{61}-1$ it would lower the worst-case combined count given in the caption of Table~\\ref{tab:fcs-budget} from $2^{186.1}$ to $2^{172.6}$ (finite computation, item~\\ref{prov:sde-triangular}), while the block-steered option of Remark~\\ref{rem:combined-schedule}, which uses the label law, gives $2^{164.1}$ there (at the full depth of Schedule~1: $2^{555.4}$, $2^{542.0}$ and $2^{533.4}$)."),
    # E4 rem:is-runtime: preprocessing term
    ("the term $b^4$ is the zero sum, which depends only on $p$ and $\\kappa_d$. With the zero sum precomputed by Lemma~\\ref{lem:zero-sum-length}, this term is the preprocessing, which is Las Vegas for some $(p,\\kappa_d)$; it is not included in $T^{\\mathrm{IS}}_d$, and these counts were derived for a deterministic zero sum and have not been re-derived for the precomputed one.",
     "the term $b^4$ is the zero sum, which depends only on $p$ and $\\kappa_d$. With the zero sum precomputed by Lemma~\\ref{lem:zero-sum-length}, this term is replaced by the preprocessing, which is not included in $T^{\\mathrm{IS}}_d$. "
     "These merge counts were derived with the zero sum computed inside the run and are not re-derived; they remain upper bounds when the zero sum is an input, since it is then only read. "
     "\\emph{Preprocessing.} At each grade with $\\kappa_d \\ge 2$, once and before any query, Remark~\\ref{rem:is-import}(d) makes at most $\\lceil\\log_2(3(c-1)/\\eps)\\rceil$ attempts ($\\lceil\\log_2(6(c-1)/\\eps)\\rceil$ when the solver share is split), each cut off after twice an explicit bound $E_d$ on its expected running time; where the step is deterministic, the first attempt succeeds. "
     "By the count in Appendix~\\ref{app:sde-side-tape} (sketch, constants not computed), $E_d$ is $O(\\kappa_d^2 b)$ field operations, hence $\\poly(\\kappa_d)\\,b^3$ machine steps, when $p \\ge 4\\kappa_d^4$, and it is bounded in terms of $\\kappa_d$ alone when $p < 4\\kappa_d^4$. "
     "Since $\\kappa_d \\le c$, the whole preprocessing takes $\\poly(c)\\,b^3\\log(c/\\eps)$ steps plus a term bounded in terms of $c$ alone, once per run; it is not repeated per merge."),
    # E5 proof of thm:main: running time includes the preprocessing attempts (as in the core)
    ("Each step runs in time polynomial in its input size. This assembly is AI-checked, pending human review.",
     "Each step runs in time polynomial in its input size, and the preprocessing makes at most $(c-1)\\lceil\\log_2(3(c-1)/\\eps)\\rceil$ cut-off attempts, each of time polynomial in $\\log p$ for fixed $c$ (Remark~\\ref{rem:is-runtime}). This assembly is AI-checked, pending human review."),
]

# ------------------------------------------------------------------ appendix-sde-side.tex
EDITS["appendix-sde-side.tex"] = [
    ("With the zero sum precomputed by Lemma~\\ref{lem:zero-sum-length} this term is the preprocessing, which is Las Vegas for some $(p,\\kappa)$; it is not re-derived here.",
     "With the zero sum precomputed by Lemma~\\ref{lem:zero-sum-length} this term is replaced by the preprocessing, made once per grade before any query and counted next (sketch, AI-checked, pending human review). "
     "Computing $\\kappa = \\gcd(d,p-1)$, $h = (p-1)/\\kappa$ and the parity of $h$ takes $O(b^2)$ steps. "
     "If $p < 4\\kappa^4$, the breadth-first search of Lemma~\\ref{lem:zero-sum-length}(iv) is deterministic, on fewer than $4\\kappa^4$ vertices and $16\\kappa^7$ edges, so its cost is bounded in terms of $\\kappa$ alone. "
     "If $p \\ge 4\\kappa^4$ and $\\kappa$ is odd, the zero sum is $(1,-1)$. "
     "If $p \\ge 4\\kappa^4$ and $\\kappa$ and $h$ are even, a trial is one exponentiation, $O(b)$ multiplications, and succeeds with probability at least $1/2$, so the expected cost is $O(b)$ operations. "
     "If $p \\ge 4\\kappa^4$, $\\kappa$ is even and $h$ is odd, a trial computes $x^\\kappa$ and $u^h$ with $O(b)$ multiplications and succeeds with probability at least $1/(4\\kappa)$; root finding~\\cite{Rabin1980} is called only once, on the accepted $u$, where $X^\\kappa - u$ has $\\kappa$ distinct roots in $\\Fp$. "
     "One splitting attempt on a factor of degree $n \\le \\kappa$ computes $(X+\\delta)^{(p-1)/2}$ modulo that factor with $O(n^2b)$ operations and a gcd. It separates two given roots $r_1 \\ne r_2$ with probability at least $(p-1)/(2p) \\ge 1/3$, since $\\chi((r_1+\\delta)(r_2+\\delta)) = 1$, $\\chi$ the quadratic character, for only $(p-3)/2$ values of $\\delta$, and the two roots stay together for at most two further values ($\\delta = -r_1, -r_2$). Keeping the smaller factor at least halves the degree, so one root costs $O(\\kappa^2b)$ expected operations. "
     "In every case the expected cost is $O(\\kappa^2 b)$ field operations, $O(b^2)$ steps each, and head movement over the at most $\\kappa+1$ coefficients adds a factor polynomial in $\\kappa$; this is the bound $E_d$ of Remark~\\ref{rem:is-runtime}."),
]

# ------------------------------------------------------------------ appendix-schedule3.tex
EDITS["appendix-schedule3.tex"] = [
    # (S1): charge the preprocessing in the split
    ("(the abort probability of that Las Vegas preprocessing, made before any query, is not included in the error split below; it adds at most $\\eps/6$ when the preprocessing is given $\\lceil\\log_2(6(c-1)/\\eps)\\rceil$ attempts per grade);",
     "(that preprocessing is run once, before any query, as in Remark~\\ref{rem:is-import}(d) with $\\lceil\\log_2(6(c-1)/\\eps)\\rceil$ attempts per grade, and the procedure outputs ``fail'' if it aborts; its abort probability, at most $\\eps/6$, is charged in the error split of the proof);"),
    # proof, restarts: the restart part is at most eps/6, and the total includes the preprocessing
    ("Hence fewer than $m'$ successes occur with probability at most $\\binom{4m'}{3m'}32^{-3m'} \\le 2^{-2m'} \\le \\eps/3$.",
     "Hence fewer than $m'$ successes occur with probability at most $\\binom{4m'}{3m'}32^{-3m'} \\le 2^{-2m'} \\le (\\eps/3)^2 \\le \\eps/6$, since $m' \\ge \\log_2(3/\\eps)$ and $\\eps \\le 1$."),
    ("the rank failure is at most $\\eps/3$, \nand the implementation error is at most $\\eps/3$.",
     None),  # placeholder, replaced below if the exact spacing differs
]
# the sentence with the rank and implementation errors (exact text checked in main())
SCHED3_TAIL_OLD = ("the kept outputs are i.i.d.\\ copies of $\\rho_{H_1}$, the rank failure is at most $\\eps/3$, and the implementation error is at most $\\eps/3$.")
SCHED3_TAIL_NEW = ("the kept outputs are i.i.d.\\ copies of $\\rho_{H_1}$, the rank failure is at most $\\eps/3$, and the implementation error is at most $\\eps/3$. "
                   "If some grade is of type (S1), the preprocessing aborts, before any query, with probability at most $\\eps/6$ (Remark~\\ref{rem:is-import}(d), with $\\lceil\\log_2(6(c-1)/\\eps)\\rceil$ attempts per grade). "
                   "The total error is therefore at most $\\eps/6 + \\eps/6 + \\eps/3 + \\eps/3 = \\eps$; this is the split of the proof of Theorem~\\ref{thm:main}, with its solver third shared by the preprocessing and the tree restarts.")
EDITS["appendix-schedule3.tex"][2] = (SCHED3_TAIL_OLD, SCHED3_TAIL_NEW)
EDITS["appendix-schedule3.tex"].append(
    ("because $n_9$ is a product of Schedule~1 arities, and the rule adds $60$ columns at grade~$9$ (at $226$ primes below $3600$ some column is added).",
     "because $n_9$ is a product of Schedule~1 arities, and the rule adds $32$ columns at grade~$9$ (at $152$ primes below $3600$, and at no prime between $3600$ and $200{,}000$, some column is added; at the full depth of Schedule~1 these counts were $60$ and $226$)."))

# ------------------------------------------------------------------ appendix-provenance.tex
EDITS["appendix-provenance.tex"] = [
    ("the worst-case counts $2^{542.0}$, $2^{533.4}$ finite computations;",
     "the worst-case counts $2^{172.6}$, $2^{164.1}$ (at the full depth of Schedule~1, $2^{542.0}$, $2^{533.4}$) finite computations;"),
    ("(the $226$ primes below $3600$ at which a column is added, and the $60$ columns at $p = 151$).",
     "(at the full depth of Schedule~1: the $226$ primes below $3600$ at which a column is added, and the $60$ columns at $p = 151$); at the depth $L_d$ of~\\eqref{eq:Bd}, \\file{research/audits/reviews/2026-11-13-rees-full-tables/scan_mixed.py} with outputs \\file{.../scan_mixed_200000.json} and \\file{.../scan_mixed_200000.out} ($152$ primes, $32$ columns at $p = 151$, and the unchanged instance of Table~\\ref{tab:fcs-budget})."),
    ("the second independent of the code of \\file{research/audits/reviews/2026-11-05-rees-s3-witness-h3-check/}, with which it agrees.",
     "the second independent of the code of \\file{research/audits/reviews/2026-11-05-rees-s3-witness-h3-check/}, with which it agrees. "
     "The combined column at the depth $L_d$ of~\\eqref{eq:Bd} and the triangular-variant count: \\file{research/audits/reviews/2026-11-13-rees-full-tables/recompute_fcs.py} (\\file{theorems/rees_fcs_budget.py} unchanged, with the Schedule-1 arity of~\\eqref{eq:Bd}; it first reproduces every printed full-depth value), output \\file{.../recompute_fcs.json}; "
     "checked by \\file{.../cross_check.py}, which imports no repository code and certifies each $t_{p,\\kappa_d}$ by breadth-first search or by an explicit zero sum, output \\file{.../cross_check.json}; record \\file{research/audits/reviews/2026-11-13-rees-full-tables.md}."),
]


def main(dry=False):
    out = {}
    for name, edits in EDITS.items():
        text = (PAPER / name).read_text(encoding="utf-8")
        for old, new in edits:
            n = text.count(old)
            assert n == 1, (name, n, old[:90])
            text = text.replace(old, new, 1)
        out[name] = text
    for name, text in out.items():
        if not dry:
            (PAPER / name).write_text(text, encoding="utf-8")
        print(f"{name}: {len(EDITS[name])} edits {'checked' if dry else 'applied'}")


if __name__ == "__main__":
    import sys
    main(dry="--dry" in sys.argv)

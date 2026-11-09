# Rees mixed uniform-kernel rule: a stated proposition for the uniform-kernel column of `tab:fcs-budget` (2026-11-04)

**Status:** DONE. `prop:mixed-schedule` stated and proved (conditional, as the paper's Schedule 3
results are); the uniform-kernel column of `tab:fcs-budget` reproduces exactly from it (8 numbers
+ 4 dashes, no discrepancy); the weighted bank step is load-bearing at small primes (smallest
instance p = 151). AI session only; AI-checked, pending human review.

Labels: **proved** (complete argument here, or cited by label), **exact computation**
(integer/rational arithmetic in the script of this report's folder), **float check**,
**argued** (sketch a reader must still check).

Files written by this pass (and only these): this report and
`research/audits/reviews/2026-11-04-rees-mixed-rule/` (script + JSON). No paper file, no
existing file edited; nothing committed.

## Status log

- [x] Read background (fcs-budget audit A.4), `combined_budget.py`, `theorems/rees_fcs_budget.py`,
      `tab:fcs-budget`, `rem:combined-schedule`, `thm:random-column`, `thm:power-sde`,
      Appendix `app:schedule3` (all lemmas), `thm:app-s2-main` abort clause.
- [x] Proposition and proof (Section 1).
- [x] Independent script and comparison (Section 2; scans 2.2).
- [x] Proposed paper text (Section 3); closing sections 4-7.

## 0. What the paper says now (read 2026-11-04)

- The caption of `tab:fcs-budget` already says the uniform-kernel columns are "for comparison
  only", that the mixed rule "is defined by the generating script, keeps Schedule 2 at some
  grades, and is not a result of this paper". So the caption is honest; what is missing is a
  stated result that the column is a consequence of.
- `rem:combined-schedule` still says "The rule does not mix in Schedule 3. The abort bound of
  Theorem random-column(ii) assumes 4u columns at every grade, so a tree that mixed Schedule 3
  with other grades would need a node-count-weighted bank bound instead."
- `thm:random-column` is stated for one u and M = 4u at every grade; its proof
  (`lem:s3-node`, `lem:s3-tree`, proof of (ii) in `app:schedule3`) and the mixed-tree lemma
  `lem:fc-forest` of `app:fc-mixed` contain every ingredient needed below; only the
  per-grade bookkeeping is new.

## 1. The proposition (proved, conditional on the same steps as the paper's results)

### 1.1 Statement

**Proposition (mixed per-grade schedule with uniform-kernel nodes; label `prop:mixed-schedule`).**
Fix an instance of `def:input-contract` with class c ≥ 2, a prime p > c, the public profile
g_1 = m, g_2, …, g_c, and 0 < ε ≤ 1. Write κ_d = gcd(d, p−1) and h_d = (p−1)/κ_d. Choose, from
public data only, a node type t_d and an arity M_d for each grade d = 2, …, c, with one of:

- (lin) κ_d = 1 and M_d ≥ g_d + 1 (`thm:power-sde`(i));
- (S1) M_d ≥ B_{κ_d}(g_d), Schedule 1 at degree κ_d with the Bezout lift (`thm:is-import`,
  `rem:is-import`(b));
- (S2) κ_d ≥ 2, p ≥ 16 κ_d^{2κ_d+2} and M_d ≥ (g_d+1)((κ_d−1)g_d+1), the solver of
  `thm:power-sde`(ii) (`thm:app-s2-main`) run with k = B;
- (S3) an integer u_d ≥ max(2, κ_d, g_d+1) with p ≥ 16u_d², and M_d ≥ 4u_d; the node
  (N1)–(N6) of `app:s3-setting` with M = M_d, rank guard u_d − 1 and K = 4κ_d^{M_d}B trials.

Put n_d = ∏_{2≤d'<d} M_{d'} (the number of grade-d nodes of one tree), P = ∏_{d=2}^c M_d,
Γ_3 and Γ_2 the sets of grades of type S3 and S2, n_{S3} = Σ_{d∈Γ_3} n_d,
n_{S2} = Σ_{d∈Γ_2} n_d, and

    β_d(M) = 4 h_d p^{g_d} / ((h_d+1)^M − 1)  +  (p^{g_d} − 1) / ((p−1) p^M).

Assume the **node-count-weighted bank budget**

    (W)   Σ_{d∈Γ_3} n_d β_d(M_d) ≤ 1/64,

and take B = ⌈log2(64·max(1, 3n_{S3} + n_{S2}))⌉. Let m' = m + ⌈log2(3/ε)⌉. Run 4m' trees of
shape (M_2, …, M_c) (root of degree 2, grade-d nodes with M_d inputs, P fresh lifted sources as
leaves) on fresh registers with private coins, keep the outputs of the first m' trees that do
not abort (ABORT if fewer), Fourier-sample them and return the nullspace. Then:

- (a) one tree aborts with probability at most Σ_{Γ_3} n_d β_d(M_d) + (3n_{S3}+n_{S2})2^{−B} ≤ 1/32;
- (b) the procedure returns ĥ with probability at least 1 − ε;
- (c) it makes c·4m'·P oracle queries;
- (d) a grade-d S3 node uses at most 4κ_d^{M_d}B classical trials on its saved bank and
  (1+κ_d^{M_d})·poly(g_d, M_d, B, log p) bit operations; an S2 node
  (1+κ_d^{κ_d})·poly(g_d, κ_d, log p, B); an S1 or lin node poly(M_d, log p); there are
  Σ_d n_d nodes per tree, and N_instr ≤ 4m'(P + Σ_d n_d(M_d+1)) + m' complete instruments.

The guarantee is conditional on the steps behind `thm:main`, on the label law
`lem:s3-law` at the S3 nodes (derived for the ideal i.i.d. supply of fresh sources, not for an
arbitrary bank, exactly as in `thm:random-column`), on `thm:power-sde`(ii) at S2 grades
(conditional in the paper), and on the Bezout lift at S1 grades with κ_d < d. If Γ_2 = ∅ the
dependence on `thm:power-sde`(ii) disappears.

**The rule of the table (U1)–(U4)** is one admissible choice:

- (U1) start from the combined rule of `rem:combined-schedule` at each grade; with
  u_d = max(2, κ_d, g_d+1), replace it by an S3 node of arity 4u_d when p ≥ 16u_d² and
  4u_d is strictly smaller than the combined arity;
- (U2) while Σ_{Γ_3} n_d β_d(M_d) > 1/64, raise by one the arity of the S3 grade with the
  largest term n_dβ_d(M_d) (smallest d on ties); public data only;
- (U3) B = ⌈log2(64·max(1, 3n_{S3}+n_{S2}))⌉;
- (U4) 4m' trees, m' = m + ⌈log2(3/ε)⌉; "trials" = max_{Γ_3} 4κ_d^{M_d}B,
  "Q" = c·4m'·P.

When (U2) stops, (W) holds and every type meets its hypothesis (S3: M_d ≥ 4u_d after
bumps), so the proposition applies. (U2) is not proved to terminate in general (raising
M_d lowers its own term but multiplies n_{d'} for d' > d); it terminated at every prime
scanned (Section 2.2), and the proposition does not depend on how the arities were found.

### 1.2 Proof (proved, from the cited lemmas)

*Node lemma for every type.* Let a grade-d node receive ρ_{H_d}^{⊗M_d} ⊗ ω_X. After (N1) each
type is a classical randomized map from the bank Λ and fresh coins to a record that holds
either ABORT or a nonzero s with Σ_i s_i^d λ_i = 0, checked exactly as in (N5) (for S2,
`thm:app-s2-main` never outputs an incorrect vector; for lin and S1 the witness is
deterministic). The proof of `lem:s3-node`(d) uses only `prop:descent` applied to a valid
witness for a positive-probability label tuple, so it gives, for every type, output exactly
ρ_{H_{d−1}} in product with ω_X on every non-aborting record. Abort probabilities, conditional
on ω_X:

- lin, S1: 0, for every bank (labels lie in F_p^{g_d}; `thm:power-sde`(i), `thm:is-import`).
- S2: at most 2^{−B} for every bank (`thm:app-s2-main` with k = B; arbitrary columns).
- S3: at most β_d(M_d) + 3·2^{−B}. By `lem:s3-law` the labels are i.i.d. uniform on K_d^⊥, of
  dimension a_d ≤ g_d ≤ u_d − 1 < M_d, independent of X. `lem:s3-moment`(c),(d) bound the bank
  event by 4h_d p^{a_d}/((h_d+1)^{M_d}−1) + (p^{a_d}−1)/((p−1)p^{M_d}); both terms are
  nondecreasing in a, so this is at most β_d(M_d). The rank guard never fires (r ≤ a_d ≤ u_d−1).
  `lem:s3-mu`(b) gives per-trial acceptance ≥ 1/(4κ_d^{M_d}) on a good bank: its proof uses
  only (p/κ_d)^{M} ≥ 2, which holds since p ≥ 16u_d² ≥ 2κ_d. The failure split of
  `lem:s3-node`(c) is stated for arbitrary M and B and applies with M = M_d: rejection of all
  K = 4κ_d^{M_d}B trials ≤ e^{−B}, root extraction ≤ 2^{−B}, field draws ≤ 2^{−B}.

*Tree factorization.* The induction of `lem:s3-tree`(a), in the form of `lem:fc-forest`(a)
(several node kinds): leaves are fresh ρ_{H_c} in product; node v_{j+1} of grade d consumes
M_d open registers, which are ρ_{H_d}^{⊗M_d} in product with the record and the other open
registers; the node lemma keeps the product form. Hence, at every S3 node, the bank is i.i.d.
uniform on K_d^⊥ conditional on the entire earlier record, including the acceptance of its own
children, whatever types those children had (`rem:s3-caveat`(iii)). Freshness across nodes
holds because each register is measured once and no bank is read after its node finishes.

*Node-count-weighted union bound.* As in `lem:s3-tree`(b),
Pr[tree aborts] ≤ Σ_j Pr[v_{j+1} aborts | E_j], and each term is bounded by the node lemma for
its type, conditional on E_j. One tree has n_d nodes of grade d, so

    Pr[tree aborts] ≤ Σ_{Γ_3} n_d (β_d(M_d) + 3·2^{−B}) + Σ_{Γ_2} n_d 2^{−B}
                    = Σ_{Γ_3} n_d β_d(M_d) + (3n_{S3}+n_{S2}) 2^{−B} ≤ 1/64 + 1/64 = 1/32,

by (W) and the choice of B. No independence between node events is used. This is (a).

*Restarts.* Conditional on any record of the other trees, a tree acts on fresh registers with
fresh coins, so its abort probability is still ≤ 1/32. Fewer than m' successes means some set
of 3m' trees all abort; multiplying the conditional bounds along the execution order and taking
a union over the sets gives ≤ C(4m',3m')·32^{−3m'} ≤ 2^{4m'−15m'} ≤ 2^{−2m'} ≤ (ε/3)² ≤ ε/3,
because m' ≥ log2(3/ε). The forest induction (proof of `thm:random-column`(ii)) makes the m'
kept outputs i.i.d. copies of ρ_{H_1}, since the kept set is a function of the record. The rank
failure is ≤ (p^k−1)p^{−m'}/(p−1) ≤ 2^{−(m'−m)} ≤ ε/3 (k ≤ m). Implementing each of the
N_instr ≤ 4m'(P + Σ_d n_d(M_d+1)) + m' complete instruments within ε/(3N_instr)
(`thm:uniform-compilation`(iii), `lem:s3-hybrid`) moves the joint law by at most ε/3. Total
failure ≤ ε. This is (b). Every attempted tree has P leaves of c queries: (c). (d) is
`lem:s3-node`(e) with M = M_d, the cost clause of `thm:app-s2-main`, and `thm:is-import`. ∎

**Remarks (proved).** (i) Within this proof p ≥ 16u_d² is used only for p ≥ 2κ_d, and
M_d ≥ 4u_d only for M_d > g_d; so the S3 hypothesis can be weakened to κ_d < p−1 and
M_d ≥ g_d+1, with (W) carrying all of the bank control. The table does not need this.
(ii) The bound 1/32 is stronger than the 1/16 that the restart step needs; the argument goes
through with any per-tree bound ≤ 1/4 (`app:schedule3`, after the binomial display).
(iii) The printed bank term 2p^{a−M} of `thm:random-column`(i) can replace the second term of
β_d; the table is unchanged (Section 2).

## 2. Exact recomputation of the column (exact computation)

Script: `research/audits/reviews/2026-11-04-rees-mixed-rule/mixed_rule.py`, written from the
statement in Section 1 only (imports nothing from `combined_budget.py`, `fcs_budget.py` or
`theorems/rees_fcs_budget.py`; reads `fcs_budget.json` only to compare). Exact `int`/`Fraction`
arithmetic; the one-decimal log2 is decided exactly (round(10·log2 x) = k iff
2^{2k−1} ≤ x^{20} < 2^{2k+1}). Command (repo root, ~2 s):
`nice -n 10 /opt/anaconda3/bin/python research/audits/reviews/2026-11-04-rees-mixed-rule/mixed_rule.py`
(add `--scan 200000` for Section 2.2). Output: `mixed_rule.json` in the same folder.

### 2.1 The six rows

| p | node types d = 2..9 (arity) | B | tree abort ≤ | uk Q (mine / table) | uk trials (mine / table) |
|---|---|---|---|---|---|
| 11 | no S3 grade | – | – | – / – | – / – |
| 1031 | no S3 grade | – | – | – / – | – / – |
| 5281 | S3 72, S3 68, S3 60, S3 52, S3 40, lin 7, S3 32, S3 12 | 45 | 2^{−6.38} | 50.3 / 50.3 | 128.2 / 128.2 |
| 2^31−1 | S3 72, S3 68, S3 60, lin 13, S3 40, S3 28, S2 16, S3 36 | 44 | 2^{−6.39} | 50.9 / 50.9 | 121.6 / 121.6 |
| 2^61−1 | S3 72, S3 68, S3 60, S3 52, S3 40, S3 28, S2 16, S3 36 | 46 | 2^{−6.39} | 52.9 / 52.9 | 128.3 / 128.3 |
| 2^127−1 | S3 72, S3 68, S3 60, lin 13, S3 40, S3 28, S2 16, S2 18 | 43 | 2^{−6.91} | 49.9 / 49.9 | 115.2 / 115.2 |

**All 8 numbers and 4 dashes agree** with `fcs_budget.json` (and so with `main.tex`). The exact
integers Q and max-trials, the per-grade types and arities, B, the 92 = 4·23 trees, and the bump
count 0 also agree exactly with the JSON (exact computation). Per-tree error terms (float
display of exact rationals): bank sum Σn_dβ_d = 2^{−67.2}, 2^{−546}, 2^{−1174}, 2^{−2562}; so the
tree-abort bound is dominated by the arithmetic caps (3n_{S3}+n_{S2})2^{−B} ≈ 2^{−6.4}.
Few-successes term ≤ 2^{−368}; rank failure ≤ 2^{−61.8} or smaller; all ≤ ε/3.

Sensitivity checks (exact computation):
- printed bank term 2p^{a−M} of `thm:random-column`(i) in place of `lem:s3-moment`(d): same
  rows (agrees with the JSON flag `main_tex_literal_rank_term.same_as_table`);
- charging each S2 node 2·2^{−B} (solver abort plus a fair-coin draw cap, which neither the
  paper's `thm:power-sde`(ii) nor the script charges) raises B to 44 at 2^127−1 only; the
  printed values do not change;
- N_instr: the script `combined_budget.py` counts one instrument per node
  (trees·(P + Σn_d + 1), log2 47.2/47.7/49.7/46.8); the `app:schedule3` convention used in the
  proposition counts M_d + 1 per node (log2 48.2/48.7/50.7/47.8). N_instr only sets the
  compilation precision, which the table does not print, so no entry is affected.

### 2.2 Is the weighted bank step load-bearing? Scans (exact computation)

Command: `mixed_rule.py --scan 200000` (one niced job, ~6 CPU-min; output
`2026-11-04-rees-mixed-rule/scan_out.txt` and the `scans` field of `mixed_rule.json`). For every
prime p ≤ 2·10^5 (class-nine profile) and p ≤ 2·10^4 (profiles (6,4,2), (8,5,3,1),
(10,7,5,3,1)) or p ≤ 5000 ((4,3)) at which (U1) picks an S3 node, the script ran (U1)–(U4) and
checked termination (cap 200 bumps), every node hypothesis of `prop:mixed-schedule`, tree
abort ≤ 1/16, few-successes ≤ ε/3 and rank failure ≤ ε/3.

- **No failure of the proposition's conclusion anywhere**: (U2) terminated at all 17,896
  class-nine primes with an S3 node (and at every prime of the small profiles); no hypothesis
  or error-budget check failed; the largest tree-abort bound is 2^{−5.10} < 1/32.
- **The weighted step (U2) is load-bearing.** Class nine: 226 primes need column bumps (all
  ≤ 3581; at most 178 bumps, at p = 421). At 225 of them the rule *without* (U2), i.e.
  p ≥ 16u_d² and M_d = 4u_d as in `thm:random-column`, gives a node-count-weighted
  tree-abort bound above 1/16. **Smallest failing instance: p = 151**, class nine, ε = 1/3:
  grades 2–6 and 8 take Schedule 1 (M_2 = 419904, …, M_6 ≈ 1.04·10^53, M_8 = 1024), grade 7
  linear, grade 9 an S3 node with u_9 = 3, M_9 = 12. With n_9 = ∏_{d<9} M_d, the bound
  Σ n_dβ_d + (3n_{S3}+n_{S2})2^{−B} is 2^{331.2} (vacuous). (U2) raises M_9 to 72 (60 bumps) and
  the bound becomes 2^{−6.68}. For profile (8,5,3,1) the smallest such prime is p = 67 (bound
  2^{6.26}; M_4 = 8 → 11). So the per-node bound "p ≥ 16u², M = 4u" of `thm:random-column`,
  which suffices when every grade has M = 4u (`lem:s3-tree`(c)), does **not** suffice in a mixed
  tree: n_d can be a product of Schedule 1 arities. This is exactly the warning in
  `rem:combined-schedule`; the correct condition is (W), and with it the 1/64 threshold and the
  B of (U3) are the right constants (both give 1/64, total ≤ 1/32 ≤ 1/16).
- None of these primes is in `tab:fcs-budget` (its smallest S3 prime is 5281, with 0 bumps).

## 3. Proposed paper text (not applied)

### 3.1 New subsection: end of `appendix-schedule3.tex`

Anchor: after the last paragraph of the file (the `\paragraph{Scope.}` paragraph ending
"as Remark~\ref{rem:combined-schedule} notes."). In that paragraph replace the final sentence
"The proof assumes $M = 4u$ columns at every grade of every tree, as Remark~\ref{rem:combined-schedule} notes."
by "The proof above assumes $M = 4u$ columns at every grade of every tree; Section~\ref{app:s3-mixed} drops that assumption." Then append:

```latex
\subsection{Per-grade arities and mixed trees}
\label{app:s3-mixed}

The tree of Section~\ref{app:s3-setting} may use a different node at each grade. Write $h_d = (p-1)/\kappa_d$, and for an integer $M > g_d$ put
\[
  \beta_d(M) = \frac{4h_d\,p^{g_d}}{(h_d+1)^M - 1} + \frac{p^{g_d}-1}{(p-1)\,p^{M}} .
\]

\begin{proposition}[Mixed per-grade schedule; conditional, AI-checked, pending human review]
\label{prop:mixed-schedule}
Let $c \ge 2$, let $p > c$ be prime and $0 < \eps \le 1$. For each $d = 2,\dots,c$ choose, from $p$, $d$ and $g_d$ only, a node type and an arity $M_d$ of one of the following kinds:
\textup{(lin)} $\kappa_d = 1$ and $M_d \ge g_d+1$, the solver of Theorem~\ref{thm:power-sde}(i);
\textup{(S1)} $M_d \ge B_{\kappa_d}(g_d)$, Schedule~1 at degree $\kappa_d$ with the Bezout lift of Remark~\ref{rem:is-import}(b);
\textup{(S2)} $\kappa_d \ge 2$, $p \ge 16\kappa_d^{2\kappa_d+2}$ and $M_d \ge (g_d+1)((\kappa_d-1)g_d+1)$, the solver of Theorem~\ref{thm:app-s2-main} with $k = B$;
\textup{(S3)} an integer $u_d \ge \max(2,\kappa_d,g_d+1)$ with $p \ge 16u_d^2$, and $M_d \ge 4u_d$, the node (N1)--(N6) with $M = M_d$, rank guard $u_d - 1$ and $K = 4\kappa_d^{M_d}B$.
Every node checks its witness exactly, as in (N5). Let $n_d = \prod_{2\le d'<d}M_{d'}$, $P = \prod_{d=2}^cM_d$, let $\Gamma_3$ and $\Gamma_2$ be the grades of type (S3) and (S2), $n_{\mathrm{S3}} = \sum_{d\in\Gamma_3}n_d$ and $n_{\mathrm{S2}} = \sum_{d\in\Gamma_2}n_d$. Suppose
\begin{equation}
  \label{eq:s3-weighted-bank}
  \sum_{d\in\Gamma_3} n_d\,\beta_d(M_d) \le \frac{1}{64},
\end{equation}
and put $B = \lceil\log_2(64\max(1, 3n_{\mathrm{S3}} + n_{\mathrm{S2}}))\rceil$. Run $4m'$ trees with arity $M_d$ at grade $d$, $m' = m + \lceil\log_2(3/\eps)\rceil$, on fresh leaves with private coins, and keep the first $m'$ that do not abort, as in the proof of Theorem~\ref{thm:random-column}(ii). Then one tree aborts with probability at most $\sum_{d\in\Gamma_3}n_d\beta_d(M_d) + (3n_{\mathrm{S3}}+n_{\mathrm{S2}})2^{-B} \le 1/32$, and the procedure returns $\hh$ with probability at least $1-\eps$ from $4m'cP$ oracle queries. A node of type (S3) uses at most $4\kappa_d^{M_d}B$ classical trials on its saved bank, and there are $4m'\sum_dn_d$ nodes in all. The guarantee is conditional on the steps behind Theorem~\ref{thm:main}, on Theorem~\ref{thm:power-sde}(ii) if $\Gamma_2 \ne \emptyset$, and, at the grades of $\Gamma_3$, on the label law of Lemma~\ref{lem:s3-law}, so it holds for the i.i.d.\ supply of fresh sources only.
\end{proposition}

\begin{proof}
\emph{Nodes.} After (N1), each type is a classical randomized map from the bank and fresh coins to a record that holds either an abort or an exactly checked nonzero witness. The proof of Lemma~\ref{lem:s3-node}(d) uses nothing else, so for every type the output is $\rho_{H_{d-1}}$, in product with the rest, on every record that does not abort. Conditional on any state of the other systems, a node of type (lin) or (S1) never aborts, since its solver works for arbitrary columns in $\Fp^{g_d}$; a node of type (S2) aborts with probability at most $2^{-B}$ for every bank, by Theorem~\ref{thm:app-s2-main}. At a node of type (S3), Lemma~\ref{lem:s3-law} makes the labels i.i.d.\ uniform on $K_d^\perp$, of dimension $a_d \le g_d \le u_d - 1 < M_d$. Lemma~\ref{lem:s3-moment}(c) and~(d) bound the bank event by $\beta_d(M_d)$, because both of its terms are nondecreasing in $a_d$, and the rank guard never fires. The proof of Lemma~\ref{lem:s3-mu}(b) uses only $p \ge 2\kappa_d$, which follows from $p \ge 16u_d^2$, so a trial on a good bank is accepted with probability at least $1/(4\kappa_d^{M_d})$. Lemma~\ref{lem:s3-node}(c), which holds for any $M$ and $B$, then bounds the abort probability by $\beta_d(M_d) + 3\cdot2^{-B}$.

\emph{One tree.} The induction of Lemma~\ref{lem:s3-tree}(a), with several kinds of node as in Lemma~\ref{lem:fc-forest}(a), shows that the inputs of every node are $\rho_{H_d}^{\otimes M_d}$ in product with the whole earlier record, whatever types the earlier nodes had; in particular the label law holds at every node of type (S3). As in Lemma~\ref{lem:s3-tree}(b), the abort probability is at most the sum over nodes of their conditional abort bounds. A tree has $n_d$ nodes of grade $d$, so it aborts with probability at most
\[
  \sum_{d\in\Gamma_3}n_d\bigl(\beta_d(M_d) + 3\cdot2^{-B}\bigr) + \sum_{d\in\Gamma_2}n_d\,2^{-B} \le \frac{1}{64} + \frac{1}{64} = \frac{1}{32},
\]
by~\eqref{eq:s3-weighted-bank} and the choice of $B$.

\emph{Restarts.} Conditional on the records of all other trees, a tree acts on fresh registers with fresh coins, so it aborts with probability at most $1/32$. Hence fewer than $m'$ successes occur with probability at most $\binom{4m'}{3m'}32^{-3m'} \le 2^{-2m'} \le \eps/3$. From here the proof of Theorem~\ref{thm:random-column}(ii) applies word for word, with $N_{\mathrm{instr}} \le 4m'\bigl(P + \sum_d n_d(M_d+1)\bigr) + m'$ complete instruments in place of~\eqref{eq:s3-ninstr}: the kept outputs are i.i.d.\ copies of $\rho_{H_1}$, the rank failure is at most $\eps/3$, and the implementation error is at most $\eps/3$. Each attempted tree has $P$ leaves of $c$ queries each. The trial count is Lemma~\ref{lem:s3-node}(e) with $M = M_d$.
\end{proof}

The proof uses $p \ge 16u_d^2$ only through $p \ge 2\kappa_d$, and $M_d \ge 4u_d$ only through $M_d > g_d$, so~\eqref{eq:s3-weighted-bank} carries all of the bank control. Table~\ref{tab:fcs-budget} uses the following instance. At each grade, start from the combined rule of Remark~\ref{rem:combined-schedule}; with $u_d = \max(2,\kappa_d,g_d+1)$, take a node of type (S3) with $M_d = 4u_d$ instead when $p \ge 16u_d^2$ and $4u_d$ is smaller than the combined arity. While~\eqref{eq:s3-weighted-bank} fails, add one column at the grade of $\Gamma_3$ with the largest term $n_d\beta_d(M_d)$. At the six primes of the table no column is added, and~\eqref{eq:s3-weighted-bank} holds with room to spare: its left side is at most $2^{-67}$, so the tree-abort bound, about $2^{-6.4}$, comes from the arithmetic caps. The weighted condition is not automatic in a mixed tree: at $p = 151$ on the class-nine profile, taking $M_9 = 4u_9 = 12$ with every other grade on the combined rule gives a left side of~\eqref{eq:s3-weighted-bank} far above $1$, because $n_9$ is a product of Schedule~1 arities, and the rule adds $60$ columns at grade~$9$ (at $226$ primes below $3600$ some column is added). The rows at $2^{31}-1$, $2^{61}-1$ and $2^{127}-1$ keep Schedule~2 at grade~8 (and at grade~9 for $2^{127}-1$) and so also depend on Theorem~\ref{thm:power-sde}(ii); the row at $5281$ uses no Schedule~2 node. Exact checks: \file{research/audits/reviews/2026-11-04-rees-mixed-rule/}; AI-checked, pending human review.
```

### 3.2 Replacement in `rem:combined-schedule` (main.tex)

Replace

> The rule does not mix in Schedule~3. The abort bound of Theorem~\ref{thm:random-column}(ii)
> assumes $4u$ columns at every grade, so a tree that mixed Schedule~3 with other grades would
> need a node-count-weighted bank bound instead.

by

```latex
The rule itself uses no label law and does not mix in Schedule~3. Proposition~\ref{prop:mixed-schedule} in Appendix~\ref{app:s3-mixed} mixes the uniform-kernel nodes of Theorem~\ref{thm:random-column}(i) into it, with a separate $u_d$ at each grade, the node-count-weighted bank bound $\sum_d n_d\beta_d \le 1/64$ and the tree restarts of Theorem~\ref{thm:random-column}(ii); it needs the label law at those grades, and Theorem~\ref{thm:power-sde}(ii) at any Schedule~2 grade it keeps.
```

(The following sentence, on `thm:free-coordinate`(iii), stays.)

### 3.3 Replacement in the caption of `tab:fcs-budget` (main.tex)

Replace

> For comparison only, the uniform-kernel columns mix the nodes of
> Theorem~\ref{thm:random-column}(i) into the combined rule, with node-count-weighted bank
> bounds and the tree restarts of Theorem~\ref{thm:random-column}(ii). That mixed rule is defined
> by the generating script, keeps Schedule~2 at some grades, and is not a result of this paper.

by

```latex
The uniform-kernel columns use the instance of Proposition~\ref{prop:mixed-schedule} described after it: the nodes of Theorem~\ref{thm:random-column}(i), with $u_d = \max(2,\kappa_d,g_d+1)$, mixed into the combined rule with a node-count-weighted bank bound and tree restarts. They are conditional on the label law, and at $2^{31}-1$, $2^{61}-1$ and $2^{127}-1$, where Schedule~2 is kept at grade~$8$ (and~$9$), also on Theorem~\ref{thm:power-sde}(ii).
```

and after "Exact computation by \file{theorems/rees_fcs_budget.py} (\file{…/fcs_budget.json})"
insert ", reproduced from the statement of Proposition~\ref{prop:mixed-schedule} by
\file{research/audits/reviews/2026-11-04-rees-mixed-rule/mixed_rule.py}".

Other places to touch if adopted (not drafted here): the `\paragraph{Scope.}` sentence of
`app:schedule3` (done in 3.1); the "variant" sentence at the end of `app:fc-mixed` is about
free-coordinate nodes and is unaffected.

## 4. The exact statement that now holds

**Proved here (AI-checked, pending human review), conditional on** the steps behind `thm:main`,
the label law `lem:s3-law` at uniform-kernel grades, `thm:power-sde`(ii) at any Schedule 2
grade, and the Bezout lift at Schedule 1 grades with κ_d < d: `prop:mixed-schedule` of Section 1.
For any public per-grade choice of node types (lin / S1 at degree κ_d / S2 / S3 with per-grade
u_d ≥ max(2, κ_d, g_d+1), p ≥ 16u_d², M_d ≥ 4u_d) satisfying the node-count-weighted bank
budget Σ_{Γ_3} n_d β_d(M_d) ≤ 1/64, with B = ⌈log2(64·max(1, 3n_{S3}+n_{S2}))⌉ and 4m' tree
restarts, one tree aborts with probability ≤ 1/32 and the procedure returns ĥ with probability
≥ 1 − ε from c·4m'·∏M_d queries, with ≤ 4κ_d^{M_d}B trials per S3 node.

**Exact computation:** the rule (U1)–(U4) of `combined_budget.py` (W+3) is an instance; at the
six primes of `tab:fcs-budget` it adds no column, meets every hypothesis, and reproduces all 8
uniform-kernel numbers and 4 dashes, together with the exact integers, schedules, B and tree
counts in `fcs_budget.json`. **No discrepancy with the table.** The uniform-kernel column is
therefore a consequence of `prop:mixed-schedule` once that proposition is in the paper; the row at
5281 needs no `thm:power-sde`(ii), the other three uniform-kernel rows do.

## 5. What is still missing

- Human review of the proposition and of every lemma it reuses (`lem:s3-node`, `lem:s3-tree`,
  `lem:fc-forest`, `thm:app-s2-main`, `lem:s3-hybrid`).
- A proof that the bump loop (U2) terminates for every input; only the scans of Section 2.2
  check it. The proposition does not need it (it covers any arities meeting (W)).
- The paper text of Section 3 is not applied; the integrator owns `main.tex`.
- S2 nodes draw "uniform elements of F_p" as a primitive in `thm:app-s2-main`; the fair-coin
  cap applied at S3 nodes is not charged at S2 nodes, in the paper or the script. Charging it
  (2·2^{−B} per S2 node) changes no printed value (Section 2.1), but the paper should either say
  so or keep the idealization explicit.
- Two N_instr conventions coexist (`sec:recursion` and `combined_budget.py`: one per merge;
  `app:schedule3`, `lem:fc-forest`: M_d + 1 per node). Harmless for this table; worth one
  sentence if the proposition is adopted.

## 6. Claim gates that must stay false

- Schedule 3 / `prop:mixed-schedule` is not a worst-case result: it is for the i.i.d. ideal
  supply only, not for arbitrary or correlated banks, and `thm:main` does not use it.
- No claim that the uniform-kernel column is unconditional: its rows at 2^31−1, 2^61−1, 2^127−1
  depend on the conditional `thm:power-sde`(ii).
- No polynomial-time claim: the uniform-kernel trial counts are 2^115–2^128 per node.
- No human-review, publication, outreach or registry promotion; nothing committed or pushed.

## 7. Proposed paper text

Section 3: 3.1 (new `app:s3-mixed` with `prop:mixed-schedule` and proof, appended to
`appendix-schedule3.tex`, plus a one-sentence change to its `Scope` paragraph), 3.2
(`rem:combined-schedule` sentence), 3.3 (`tab:fcs-budget` caption).

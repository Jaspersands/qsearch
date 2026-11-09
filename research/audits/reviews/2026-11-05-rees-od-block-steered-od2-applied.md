# Owner decisions applied: block-steered SDE node and OD2 (2026-11-05)

**Status: AI-checked, pending human review.** AI-only integration pass. It applies two owner
decisions. No git, no network. `make_numbers.py` was not run. `numbers.tex` and the claim gates in
`research/reductions/rees_hsp_reduction.json` were not touched, nor was `appendix-schedule2.tex`.
Every "AI-checked, pending human review" label and NEEDS HUMAN VERIFICATION flag is kept.
Scripts and outputs are in `2026-11-05-rees-od-block-steered-od2-applied/`. Backups are in the
session scratchpad, `bak_od2/`.

## Decision 1: adopt the block-steered solver (rem:sde-block-steered)

**Where the paper used the triangular count for random columns.** No query count or table in the
paper used `(a+1)(a+2)/2` for i.i.d. columns. Proposition triangular-sde was "not adopted"
(rem:triangular-scope). The only count that the block-steered solver can change is the combined
column of tab:fcs-budget. This is variant A of `2026-11-05-rees-sde-block-check.md` §4: the node
replaces the combined-rule node (Schedule 1 or 2) when it is admissible and smaller.

`rem:fc-tradeoff(a)` uses triangular rounds on uniform banks only as a trade-off curve, with no
count. Swapping in block-steered rounds there would need a new derivation, so it is not done.
The worst case keeps the triangular solver. The text still says that for arbitrary columns the
best proved arity is `(a+1)(a+2)/2`.

**How it is adopted (main.tex, rem:combined-schedule, new last paragraph).** The node is a public
option at a grade with `2 <= kappa_d < p-1`. It has `J_d = max(3,kappa_d)` blocks and arity
`M_d = M_{J_d}(g_d)`, and it is used when that arity is smaller and the following hold:

- **(G1)** `p ∉ E_cg(J_d,kappa_d)`, for example because the Weil bound
  `G^-_d = min_{2<=j<=J_d} kappa^{-j}(p-j-(kappa^j-1)(j-1)sqrt p)` is positive.
- **(G2)** `Lambda_d C(J_d,2) <= G^-_d/2`. Each back substitution then fails with probability at
  most 1/2.
- **(G3)** `(M_d + Lambda_d C(J_d,2))/(p-1) + p^{g_d-M_d}/(p-1) <= tau_d = eps/(9(c-1) S n_d)`.
  This bounds the bank and span failures, which repetition cannot remove.

The node makes at most `B` back substitutions and caps its draw loops and root extractions. It
aborts with probability at most `tau_d + 3·2^{-B}` on the i.i.d. supply, and it never returns a
wrong witness. A run with the option is a run of (R1). It has the error split of
thm:free-coordinate(iii) and needs the label law at the grades that use the node.

These results do not use the node: Theorem main, thm:bb-envelope, E_W(c), tab:main-regimes,
tab:query-crossover, the mixed instance of prop:mixed-schedule (uniform-kernel columns) and the
(iii) columns.

**Recomputation.** The command is
`nice -n 19 /opt/anaconda3/bin/python block_steered_combined.py bs_combined.json`. It imports
`theorems/rees_fcs_budget.py` read-only (the generator cited in the caption) and computes in exact
integer and rational arithmetic.

1. Old values: `combined_rule()` reproduces all six printed values (202.1, 167.3, 852.3, 944.9,
   555.4, 61.5), checked by assertion.
2. New values: variant A recomputed independently of `preview_e.py`. It agrees with that script.

| p | combined Q old | new | grades using the node | Schedule 2 grades kept | bank-abort sum |
|---|---|---|---|---|---|
| 11 | 202.1 | 202.1 | none (G2, G3 fail) | none | 0 |
| 1031 | 167.3 | 167.3 | none (G3 fails) | 2, 4, 6, 8 | 0 |
| 5281 | 852.3 | 852.3 | none (G3 fails; G1 fails at kappa >= 4) | 2 | 0 |
| 2^31-1 | **944.9** | **940.3** | 2, 3 (J = 3) | 4, 8 | 9.0e-5 |
| 2^61-1 | **555.4** | **533.4** | 2-8 (J = 3,3,3,5,6,7,3) | none | 2.5e-7 |
| 2^127-1 | **61.5** | **41.4** | 2, 3, 4, 6, 7, 8, 9 (J = 3,3,3,6,7,3,9) | none | 2.7e-26 |

Exact values: log2 Q = 940.2588, 533.4234 and 41.4323. Every bank-abort sum is at most eps/9.

The script also asserts that wherever the node is admissible, the least FCS arity of (iii) is no
larger. So the (iii) columns do not move.

The caption's conditionality changes. The combined column is now conditional on
thm:power-sde(ii) only at 1031, 5281 and 2^31-1, where Schedule 2 grades remain. It no longer is
at 2^61-1 or 2^127-1. The caption keeps the worst-case values (944.9, 555.4, 61.5).

**E_W(c) unchanged.** E_W(c) is defined by the worst-case rule, which is unchanged. In any case,
(G3) needs p to be large compared with g_d^2 and n_d, so at a fixed prime the option is
unavailable for large g_d.
`ew_preview.py` was rerun (`ew_rerun.out`) and gives [5, 11, 23, 38, 56, 77, 107, 143], equal
to the paper (asserted). **numbers.tex: no macro changes** (the table is not macros; no macro
holds a combined value).

**Text edits (main.tex).**
- rem:triangular-scope: the 555.4 -> 542.0 example now names the worst-case count in the caption
  and adds that the block-steered option gives 2^533.4; "not adopted" stays for the triangular
  solver.
- rem:sde-block-steered: "nothing else in the paper uses it" replaced by the adoption sentence;
  last sentence: the option is used in the combined column, not in Theorem main, the worst-case
  rule or the other columns; E_W unchanged.
- rem:sde-worst-case(c): last sentence rephrased (this remark changes no count).
- rem:combined-schedule: new paragraph (above).
- thm:free-coordinate(iii): block-steered node as an (R1) option at Gamma_F.
- tab:fcs-budget: caption and combined column.
- Front-matter version note: one sentence on the owner decisions.
- Core (`core/main-core.tex`, "Smaller arities"): the triangular variant is "for arbitrary
  columns". For i.i.d. labels a block-steered variant uses floor((g_d+2)^2/4)+[g_d odd] columns
  at kappa_d <= 3 and g_d^2/(2(kappa_d-1))+O(g_d) in general, at primes large compared with g_d^2
  and the node count.

## Decision 2 (OD2): zero-sum and weight-doubling nodes as public options of (R1)

Source: `2026-11-05-rees-s3-witness-h3-check.md` §6 OD2, `2026-11-05-rees-s3-arity-check.md`.

**Edits.**
- **appendix-free-coordinate.tex (R1):** tau_d is defined on Gamma_F ∪ Gamma_0. There are three
  public alternatives, together called the "optional nodes" of (R1):
  - at Gamma_0, the node of rem:fc-zero-sum-arity(b), with abort target tau_d;
  - at Gamma_F, the node of rem:fc-witness-h3(b), with abort target tau_d;
  - at Gamma_F, the block-steered node under (G1)–(G3).
- **(R3):** these nodes run with cap B.
- **lem:fc-forest(a):** these nodes are a further case of the induction (they read only their
  own bank, check exactly and convert by prop:descent).
- **lem:fc-forest(b):** the bound is now
  `sum_{Gamma_F ∪ Gamma_0} S n_d (beta_d + 3·2^{-B}[d ∈ Gamma_F]) <= eps/9 + 3N·2^{-B} <= 2eps/9`,
  with `beta_d = tau_d` at an optional-node grade, using `|Gamma_F ∪ Gamma_0| <= c-1`.
- **Paragraph after the proof of (iii):** the combined column is described as above.
- **rem:fc-zero-sum-arity, rem:fc-witness-h3:** their "unchanged / not used" first sentences now
  state the adoption. In (c), 93.0–150.8 is now "two independent implementations, last column of
  the table".
- **prop:fc-uniform(b):**
  - the old time bound is scoped to FCS nodes;
  - a new clause: with weight-doubling nodes at Gamma_F and Schedule 1 or the node of
    rem:fc-zero-sum-arity(b) at Gamma_0, the time is poly(m, log p, log 1/eps) at fixed c for
    every p > c, at a larger Q;
  - the proof cites rem:fc-witness-h3(c).
- **app:fc-numbers(a):** gives the six w.-d. values and says which grades use the tables.
- **main.tex thm:free-coordinate(iii):** a new sentence lists the options, and a new time
  sentence says that the classical time is polynomial at fixed c, at a larger query count.
- **main.tex, the paragraph after the theorem:** "not adopted in (R1)" becomes "adopted by owner
  decision as public options of (R1), and stated in part (iii)". A new sentence gives the table
  range 2^93.0–2^150.8 against 2^34.0–2^42.3, with "no speedup is claimed".
- **main.tex, the scope paragraph after prop:rc-lower:** "(not used elsewhere)" becomes "its
  node (b) is a public option of (R1)".
- **cor:fpt-r proof:** "run without its optional nodes".
- **tab:main-regimes, "Random column, free coordinates" row:** last cell gets "weight-doubling
  nodes in (iii) (Rem. fc-witness-h3): polynomial time at fixed c, more queries". The note is in
  the wide column; putting it in the 3.6 cm column caused "Float too large".
- **core "Smaller arities":** at fixed class, with weight-doubling nodes, polynomial classical
  time at every p > c, at more queries than the free-coordinate nodes; no speedup claimed.

**New column of tab:fcs-budget ("w.-d. Q").**
- Commands:
  - `nice -n 19 /opt/anaconda3/bin/python wd_budget_indep.py wd_budget_indep.json` (new
    implementation, written from the text of rem:fc-witness-h3(b) / rem:fc-zero-sum-arity(b));
  - `nice -n 19 /opt/anaconda3/bin/python ../2026-11-05-rees-s3-witness-h3-check/hcheck.py budget wd_budget_rerun.json`
    (rerun, byte-identical to that folder's `budget.json`).
- Both give **103.5, 93.0, 119.9, 127.1, 150.8, 142.0** at 11, 1031, 5281, 2^31-1, 2^61-1 and
  2^127-1, and per-grade log2 M_d agrees to 0.006. The range 93.0–150.8 is confirmed.
- Tables are used at p = 11 (every Gamma_F grade) and at p = 5281, grade 8. Every other grade
  uses the rescaled form. No row has Gamma_0 ≠ ∅.
- `fcs_vs_wd.py` checks that the FCS least arity is below the w.-d. arity at every Gamma_F grade,
  so the (iii) "least public arities" columns do not move.

**E_W(c) and numbers.tex unchanged.** Neither concerns Schedule 3.

## Build and tests

- Full paper, built in `scratchpad/build_odB` with
  `PATH=/Library/TeX/texbin:$PATH nice -n 19 latexmk -g -pdf -interaction=nonstopmode main.tex`:
  exit 0, **183 pp.**, 0 Overfull, no undefined refs or cites, no "Float too large". The first
  build overflowed tab:main-regimes by 14 pt; moving the note to the wide column fixed it.
- Core, built in `scratchpad/build_odB_core`: exit 0, **26 pp.**, 0 Overfull, no undefined refs
  or cites, no "Float too large".
- `/opt/anaconda3/bin/python -m pytest -q tests/tools/test_rees_paper_numbers.py`: **2 passed**.

## Not done / for other owners

- `appendix-schedule2.tex`: no change is needed (it has no fcs-budget number or block-steered
  text).
- `research/STATE.md` and `AGENT_HANDOFF.md` were not updated. That was not in the brief. The
  STATE line "NOT adopted (owner call) (I206)" and the OD2 line are now stale.
- rem:fc-tradeoff(a) with block-steered rounds is not derived.

## Claim gates (unchanged, must stay false)

`research/reductions/rees_hsp_reduction.json` was not touched.

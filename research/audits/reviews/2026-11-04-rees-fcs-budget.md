# Rees Schedule 3: a JSON artifact for `tab:fcs-budget`, and the parameterized corollaries at every prime (2026-11-04)

AI session only; nothing here is human-reviewed. Owner item: `research/REES_FULL_CONTINUATION.md`,
ranked item 4, "Still open" (the `tab:fcs-budget` artifact; restating the derived-dimension and
codimension corollaries at every prime via `thm:free-coordinate`(iii)).

Labels used below: **proved** (a complete argument is given here or cited by label),
**exact computation** (integer/rational arithmetic in a committed script), **argued** (a
sketch whose details a reader must still check).

Files written by this pass (and only these):

- `theorems/rees_fcs_budget.py` (new; imports nothing from the older report scripts)
- `tests/test_rees_fcs_budget.py` (new)
- `research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json` (new)
- this report

No paper file was edited.

## Status log (written incrementally)

- [x] Located the source of `tab:fcs-budget`.
- [x] Wrote and ran `theorems/rees_fcs_budget.py`; all 32 numeric entries reproduce.
- [x] Wrote `tests/test_rees_fcs_budget.py`; `9 passed`.
- [x] Corollary analysis (Part B) done.
- [x] Proposed paper text written.

## Part A. A JSON artifact for `tab:fcs-budget`

### A.1 Where the numbers came from (exact computation, provenance)

The caption cites `research/audits/reviews/2026-11-02-rees-schedule3-cost/fcs_budget_out.txt`.
That file is the output of `fcs_budget.py` in the same folder. The script imports
`../2026-11-02-rees-schedules/combined/combined_budget.py` for the combined rule (its "Rule W")
and for the uniform-kernel column (its "W+3", function `budget_restart`). The table rows are the
`W`, `W+3 (old)` and `W+FCS(T<= inf)` lines of that output at p = 11, 1031, 5281, 2^31-1,
2^61-1 and 2^127-1. `2026-11-02-rees-free-coordinate-appendix/fc_appendix_check.py` [2]
reproduced the three (iii) columns independently; the uniform-kernel and combined columns had
no independent check. Nothing under `theorems/` computed this table before this pass.

### A.2 What the new script computes (exact computation)

`theorems/rees_fcs_budget.py` imports nothing from those scripts. It uses `Fraction` and
integer arithmetic throughout. `ln 2` enters only through `ceil(2B ln2 q^{-g})`, which it
evaluates between rational bounds 1e-110 apart and asserts that both bounds give the same
ceiling. It takes log2 only at the end. The formulas are the paper's:

| column | formula (paper location) |
|---|---|
| combined Q | `rem:combined-schedule` arities (linear `g_d+1` if κ_d = 1; `(g_d+1)((κ_d−1)g_d+1)` if κ_d ≥ 2 and p ≥ 16κ_d^{2κ_d+2}; otherwise `B_{κ_d}(g_d)`), and the count after `thm:main`: Q = c·S·∏M_d with S = m + ⌈log_p(3/ε)⌉ |
| (iii) Q | `thm:free-coordinate`(iii), rule (R1) of `app:fc-mixed`: at 2 ≤ κ_d < p−1 the **least** M_d with some 1 ≤ n_0 ≤ M_d and β(M_d,n_0;g_d) ≤ τ_d = ε/(9(c−1)S n_d), β from `eq:fc-beta`; `g_d+1` at κ_d = 1; `B_d(g_d)` at κ_d = p−1; Q = c·S·∏M_d |
| (iii) trials | max over sampler grades of ⌈2B ln2 · q_d^{−g_d}⌉ with B = ⌈log2(27N/ε)⌉, N = S·Σ_{Γ_F} n_d (the cap at the worst case r = a_d = g_d, `app:fc-numbers`) |
| (iii) total | S·Σ_{Γ_F} n_d·⌈2B ln2·q_d^{−g_d}⌉ |
| uniform-kernel Q, trials | `thm:random-column`(i) node formulas (bank 4/μ + Pr[rank < a], 4κ^M B trials) and (ii) restarts (4m' trees, m' = m + ⌈log2(3/ε)⌉, Q = c·4m'·P), inside a **mixed rule that the paper does not state** (A.4) |

Output: `research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json`. Each row holds
the six printed strings (`table`), the exact integers (`exact`), the distance of each log2 from
the nearest rounding boundary, the per-grade schedule, arity, n_0, τ_d, bank bound, trial cap,
the arity of the explicit choice of `lem:fc-choice`, and the error budget. Runtime is about
0.2 s. Command: `/opt/anaconda3/bin/python -m theorems.rees_fcs_budget`.

### A.3 Result: every entry agrees (exact computation)

```
       p   combined   uk Q   uk trials   (iii) Q   (iii) trials   (iii) total
      11      202.1     --          --      42.3           28.3          47.0
    1031      167.3     --          --      36.6           33.4          50.8
    5281      852.3   50.3       128.2      39.1           33.8          52.2
  2^31-1      944.9   50.9       121.6      35.9           31.0          49.8
  2^61-1      555.4   52.9       128.3      34.1           33.5          51.0
 2^127-1       61.5   49.9       115.2      34.0           31.0          49.5
```

All 32 numeric entries and the 4 dashes match `main.tex` at the printed precision. **No entry
disagrees with the paper's formulas.** The closest rounding call is 0.0014 in log2 units
(combined Q at p = 1031), far above float error. The test parses the live `main.tex` table, so
a later edit to either side fails it.

The appendix and body claims about the table were checked against the same computation (exact
computation):

- S = 20 and t = 1 at all six primes. Γ_0 is empty, and no grade uses Schedule 2.
- Every grade with 2 ≤ κ_d < p−1 uses one FCS node per grade node, and every grade with κ_d = 1
  the linear schedule. At every sampler grade the least FCS arity is at most the combined-rule
  arity, so the "min with the combined rule" variant of the old script is never used
  (`app:fc-mixed`, last paragraph).
- The largest per-node cap is 2^33.78, at p = 5281, grade 4, B = 40. There
  log2 q_4^{−14} = 27.9885 and log2(2B ln 2) = 5.79. The largest total is 2^52.2.
- The explicit choice of `lem:fc-choice` raises each FCS arity by 1 or 2 columns and log2 Q
  by 0.235 to 1.3125. Its per-node caps are at most 2^33.78. At 2^61−1 its B is 37, not 36, so
  the cap there goes from 2^33.50 to 2^33.54. Every error budget is within ε.
- Minimality: at every sampler grade the test checks that M_d − 1 columns admit no n_0 with
  β ≤ τ_d.

### A.4 Finding: the uniform-kernel column is computed by a rule the paper does not state

The node formulas in the uniform-kernel column are those of `thm:random-column`(i). The way
they are mixed into the combined rule comes from `combined_budget.py` (W+3). That rule takes
u_d = max(2, κ_d, g_d+1) separately at each grade. It uses a node of arity 4u_d when
p ≥ 16u_d² and 4u_d is strictly smaller than the combined arity. It adds a column at the worst
grade while the node-weighted bank sum per tree, Σ_d n_d β_d, exceeds 1/64 (no column is ever
added at these six primes). It sets B = ⌈log2(64·max(1, 3n_S3 + n_S2))⌉, and it keeps
Schedule 2 nodes at some grades (grade 8 at 2^31−1 and 2^61−1; grades 8 and 9 at 2^127−1).
`rem:combined-schedule` says the opposite: "The rule does not mix in Schedule 3". It adds
that a mixed tree "would need a node-count-weighted bank bound instead". The weighted bound
is exactly what the script uses, so the computation is internally consistent. It is
**argued**, by the union bound of `lem:s3-tree`(b) node by node (as in `lem:fc-forest`(b))
plus the restarts of `thm:random-column`(ii). The paper proves no theorem for that mixed
rule, and at the Schedule 2 grades the rule also needs `thm:power-sde`(ii). These numbers do
not change when the bank term (p^a−1)p^{−M}/(p−1) of `lem:s3-moment`(d) is replaced by
the 2p^{a−M} printed in `thm:random-column`(i); the JSON records this as
`main_tex_literal_rank_term.same_as_table = true`. The caption should therefore say that
the uniform-kernel column is a script-defined comparison, not a consequence of a stated
theorem (proposed text below). This is a wording fix, not a numerical disagreement.

### A.5 Proposed wiring (not applied)

The JSON already carries the 32 `numbers_map.json` entries under
`proposed_numbers_map_entries`. Each has the form

```json
{"macro": "FcsElevenFcQ", "source": "research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json",
 "path": "rows.0.table.iii_Q", "format": "{}"}
```

The macro names are `Fcs<prime><column>`. The prime tags are `Eleven`, `TenThirtyOne`,
`FiftyTwoEightyOne`, `MersThirtyOne`, `MersSixtyOne` and `MersOneTwentySeven`. The column tags
are `CombQ`, `UkQ`, `UkTrials`, `FcQ`, `FcTrials` and `FcTotal`. All names are letters only, as
`make_numbers.py` requires. The values are the preformatted strings, so no new `kind` is
needed. A dry run of `make_numbers.render` on these 32 entries, in memory and writing nothing,
produced the expected `\newcommand` lines. The four dash cells stay literal `--`; the test
asserts that their JSON values are `null`. Integration steps for the parent:

1. Append the 32 entries to `docs/papers/rees-hsp/numbers_map.json`.
2. Run `/opt/anaconda3/bin/python docs/papers/rees-hsp/make_numbers.py`, then `--check`.
   `tests/tools/test_rees_paper_numbers.py` fails until `numbers.tex` is regenerated.
3. Replace the table body and caption (text below), and drop `tab:fcs-budget` from the
   "not macros" list of the artifact paragraph near main.tex line 1048.
4. Commit the JSON together with `numbers.tex`, since `\Fcs…` macros read it (compare K19–K21).

## Part B. The derived-dimension and codimension corollaries at every prime

### B.1 The statements as they stand

- `cor:fpt-r` (main.tex near line 699) claims every prime p > c, but its proof splits at
  p = 16(r+1)². For p ≥ 16(r+1)² it uses `thm:random-column` (the label law). For
  p < 16(r+1)² it imports Ivanyos–Magniez–Santha, Theorem 11 (IMS), at cost
  poly(input + |G'|) with |G'| = p^r.
- `cor:codim`(ii), proved as `thm:app-codim`(ii), splits at p = 64k². For p ≥ 64k² it runs the
  reduction followed by `thm:random-column` with u = 2k on the terminal
  (`prop:app-codim-rc`). For p < 64k² it runs the classical birthday learner
  (`prop:app-codim-birthday`).
- Table `tab:main-regimes`, rows "Derived dim." and "Hidden codim.", repeats both splits.

Both thresholds come from the condition p ≥ 16u², which `thm:random-column` and
`thm:free-coordinate`(ii) need. Part (iii) of `thm:free-coordinate` needs only p > c, and it
falls back to Schedule 1 at the one grade with κ_d = p−1.

### B.2 Facts used (proved; each is one step from a cited label)

**F1 (Γ_0 is empty unless p = c+1).** Γ_0 = {d ≤ c : κ_d = p−1 ≥ 2}. If d ∈ Γ_0, then p−1
divides d with d < p, so d = p−1 ≤ c. This forces p = c+1, because p > c (`app:fc-mixed`). So
for p ≥ c+2 the procedure of (iii) uses only FCS and linear nodes, and the term t_S1 of
`prop:fc-uniform`(b) is zero. **Proved.**

**F2 (arity recursion without fixed class).** Take the explicit choice of `lem:fc-choice` at
every grade of Γ_F, with ε = 1/3 and Γ_0 = ∅. Let g* = max_{d≥2} g_d, S = m + ⌈log_p 9⌉ ≤ m+2,
and

  α = (1 + 2 log2 c) g* + 3 log2(216 c S) + 3.

The proof of `prop:fc-uniform`(b) uses ln(p/κ_d) ≥ ln h ≥ ln 2, κ_d ≤ c and τ_d = ε/(9(c−1)S n_d).
It gives M_d ≤ (1+2log2 c) g_d + 3 log2(72(c−1)S n_d/ε) + 3 ≤ α + 3 log2 n_d at Γ_F grades. At Γ_1
grades M_d = g_d + 1 ≤ α. The function t ↦ 2^t/(4t) increases for t ≥ 2, and
α ≥ 3 log2(216cS) + 4 + 2 log2 c gives 2^α ≥ 16(216cS)^3 c^2 ≥ 4αc, so log2(4αc) ≤ α.
Induction on d, starting from log2 n_2 = 0, now gives log2 n_d ≤ (d−2) log2(4αc). Hence
M_d ≤ α + 3c·log2(4αc) ≤ (1+3c)α ≤ 4αc. So

  Q_1 = c·S·∏_{d=2}^c M_d ≤ c·S·(4αc)^{c−1}.

**Proved.** As a falsification check (exact computation, scratch script, not committed), this
was verified on 25 filiform profiles r = 1..25 (c = r+1) at 6 primes each, among them the least
primes ≥ c+2. The true log2 Q_1 was at most 3.19·r·log2(r+2), well under the bound.

**F3 (polylog powers).** For integers r ≥ 1 and reals x ≥ 1,
x^r ≤ max(r^{2r}, 2^{16}, 2^x). Case x ≤ r²: x^r ≤ r^{2r}. Case x > r² with x ≥ 16: r < √x and
log2 x ≤ √x, so x^r ≤ 2^{√x·log2 x} ≤ 2^x. Case x > r² with x < 16: x^r < 16^4. **Proved.**

**F4 (majority amplification).** Each run of (iii) at ε_0 = 1/3 returns the right subspace with
probability ≥ 2/3 (ABORT counts as wrong). Runs use fresh sources and coins, so they are
independent. With R = ⌈18 ln(1/ε)⌉ runs, the right answer is returned by more than R/2 of them
except with probability at most exp(−2R(1/6)²) ≤ ε (Hoeffding). The plurality output is then
correct. This works for oracle input and for copy input, and it needs no certification by f.
**Proved.** It is needed because the arities of (iii) depend on ε through τ_d. Used directly at
error ε, F2 would give a factor (log 1/ε)^{c−1}, which is not poly(log 1/ε) when c is not fixed.

**F5 (trial count from the observed rank).** The trial cap of an FCS node is
T_r = ⌈2B ln2·q^{−r}⌉ with r the observed rank ((F3) of `app:fc-setting`), and r ≤ a_d by
`lem:fc-rref`(a). So T_r ≤ 2B ln2·κ_d^{a_d} + 1. The displayed bound of `prop:fc-uniform`(b)
uses the weaker κ_d^{g_d}. The weaker form suffices for `cor:fpt-r` (g_d ≤ r). It does not
suffice for `cor:codim`, where the terminal has g_d up to k(k+1)/2 but a_d ≤ k
(`lem:app-codim-ad`). **Proved.**

### B.3 Derived dimension: restated corollary (proved, conditional)

Hypotheses: Definition `def:input-contract`, r = dim[L,L] ≥ 1, c < p, class not fixed.

- **(a) p ≥ c+2.** Conditional on the steps behind `thm:main` and on `thm:free-coordinate`(iii),
  the HSP is solved with probability ≥ 1−ε. This branch uses the label law of fresh ideal
  sources, derived in `lem:s3-law` (AI-checked); its guarantee covers the i.i.d. ideal supply
  only. It uses Q ≤ R·c·S·(4αc)^{c−1} = 2^{O(r log(r+2))}·(m+2)²·⌈18 ln(1/ε)⌉ queries, and time
  2^{O(r log(r+2))}·poly(m, log p, w, log(1/ε)).
  *Proof.* c ≤ r+1 and a_d ≤ g_d ≤ r, as in the current proof. By F1 every grade is FCS or
  linear. Apply F2 with g* ≤ r and c ≤ r+1. Then 4αc ≤ C(r+2)²log2(r+2) + 12(r+2)·log2 S, and
  (x+y)^n ≤ 2^n(x^n+y^n) with F3 at x = log2 S gives
  (4αc)^{c−1} ≤ 2^{O(r log(r+2))}·max(1, S). Repeat by F4. Classical time:
  `prop:fc-uniform`(b) with t_S1 = 0, κ_d^{g_d} ≤ (r+1)^r, B ≤ log2(81Q_1)+1 and
  max M_d ≤ 4αc. Quantum gates: N_instr ≤ 3Q_1 instruments (proof of (iii)), each of size
  poly(c, m, log p, w, log(N_instr q_max/ε)) by `thm:uniform-compilation`, with c ≤ r+1 ≤ m.
- **(b) p = c+1 (only possible when c+1 is prime).** IMS Theorem 11 as in the current proof,
  with |G'| = p^r = (c+1)^r ≤ (r+2)^r. This branch needs the oracle input (a): the current
  amplification certifies each H' by evaluating f.

Status of each piece: (a) for oracle input is **proved** from the cited labels. (a) for coset-copy
input is **argued**. `thm:free-coordinate`(iii) counts "oracle queries", and its proof
(`lem:fc-forest`(a)) uses only that the leaves are fresh lifted sources ρ_{H_c} in product,
which `lem:copy-lift` supplies from c copies each. (b) is unchanged.

Compared with the current corollary, the restatement no longer uses `thm:random-column`, and
it uses IMS at one prime, not at every p < 16(r+1)². It also makes explicit that the current
small-prime branch covers oracle input only, a point the current statement leaves implicit.
The appendix sentence "Only part (ii) gives bounds that are uniform in c in the sense of
Corollary cor:fpt-r" (`appendix-free-coordinate.tex`, after `prop:fc-uniform`) is too strong.
It is right for general profiles, where g_d ~ m makes the degree grow with c. Under g_d ≤ r,
F2–F4 give the FPT form from (iii) as well.

### B.4 Hidden codimension: restated corollary (proved, conditional)

Hypotheses: as in `thm:app-codim` (codim h ≤ k with k given, ordinary coherent oracle; coset
copies not covered; c < p; class not fixed).

- **(ii') any p > c.** Conditional on `thm:free-coordinate`(iii), and hence on the Rees
  composition: non-oracle time 2^{O(k log(k+2))}·poly(m, log p, w, log(1/ε)) and
  Q = 2^{O(k log(k+2))}·poly(m, log(1/ε)), plus Q·T_f.
  *Proof.* Branch on the public p and k.
  - *p ≤ 2k.* Use `prop:app-codim-birthday` on the original instance:
    B ≤ 4p^{k/2} ≤ 4(2k)^{k/2}, so log2 B ≤ (k/2)·log2(2k) + 2.
  - *p ≥ 2k+1.* Run the reduction. A nonabelian terminal (k ≥ 2) has class c_J ≤ 2k−1 ≤ p−2
    and dimension m_J ≤ k(k+1)/2 (`prop:app-codim-complete`(iii)), so F1 gives Γ_0 = ∅. The
    terminal is an instance of `def:input-contract` with an ordinary coherent oracle, as in the
    proof of `prop:app-codim-rc`, so `lem:s3-law` applies to its fresh lifted sources. Run (iii)
    on it R = ⌈18 ln(2/ε)⌉ times at ε_0 = 1/3 and take the plurality output (F4, error ≤ ε/2,
    as the budget of `app:codim-proof` requires). F2 with c_J ≤ 2k−1, g*_J ≤ k(k+1)/2 and
    S_J ≤ k(k+1)/2 + 2 gives α_J = O(k² log(k+2)) and
    Q_J ≤ c_J S_J (4α_J c_J)^{c_J−1} = 2^{O(k log(k+2))}, independent of m and p. By F5 and
    `lem:app-codim-ad`, every FCS node uses at most 2B ln2·(2k−1)^k + 1 trials, with fewer than
    Q_J nodes and B ≤ log2(81 Q_J) + 1. Each terminal query is one query to f plus
    poly(m, log p) arithmetic. The reduction's cost and the error budget are unchanged.
  - k ≤ 2 as in `thm:app-codim`(iii).

  **Proved**, conditional as stated. The old split (birthday below 64k², `thm:random-column`
  above) remains a valid alternative proof. With (iii) the birthday learner is needed only for
  p ≤ 2k, and the quantum route covers every p ≥ 2k+1.

### B.5 Where part (iii) does not suffice: the obstruction

1. **The zero-sum grade d = p−1 = c, which exists only at p = c+1.** There h = 1, D = {0,1} and
   β ≥ 4, so no FCS node is possible. (iii) falls back to Schedule 1 at degree c with arity
   B_c(g_c) ≥ c^{c(c−1)⌈log2(c+1)⌉/2}. When c = r+1 (filiform) this is 2^{Ω(r² log² r)}, not
   2^{O(r log r)}. Exact computations with the new script at p = c+1 on filiform profiles:
   - r = 3, c = 4, p = 5: M_4 = B_4(1) = 2^{48.0} and log2 Q = 58.9, against log2 |G'| = 7.0.
   - r = 5, p = 7: log2 Q = 155.8, against 14.0.
   - r = 9, p = 11: log2 Q = 676.8, against 31.1.

   Even the existence of a worst-case witness needs g_c(p−1)+1 columns (Davenport constant of C_p^{g_c};
   `thm:power-sde`(iii)). That count is only linear, so the
   obstacle is *finding* a witness efficiently, not existence. This is the zero-sum grade that
   the continuation brief lists as open. For `cor:fpt-r` the gap is closed by IMS at p = c+1.
   For `cor:codim` it is avoided by the birthday learner at p ≤ 2k.
2. **The source law.** Every (iii) branch rests on the i.i.d. law of fresh ideal sources
   (`lem:s3-law`, AI-checked). Like `thm:random-column`, (iii) gives nothing for a fixed,
   correlated or adversarial bank, and the procedure cannot certify the law. So the restated
   corollaries are *conditional* exactly as the current ones are. The only branches without the
   label law are IMS at p = c+1 and the classical birthday learner.
3. **The ε-dependence of the arities.** Without F4, (iii) gives (log 1/ε)^{c−1} factors when
   c is not fixed. This is not an obstruction, but the restated proofs must amplify a
   constant-error run.
4. **Codimension: g_d versus a_d.** The arity of (iii) is set from g_d, which can be k(k+1)/2 at
   the terminal. The FPT form survives only because there are at most 2k−2 grades, and because
   the trial count uses the observed rank r ≤ a_d ≤ k (F5). The displayed time bound of
   `prop:fc-uniform`(b), with κ^{g_d}, would give only 2^{O(k² log k)}.

**Optional, argued (not proposed for the paper's statements):** a zero-sum node at p = c+1
would remove IMS from `cor:fpt-r`. At grade d = p−1 a witness is a nonempty T ⊆ [M] with
Σ_{i∈T} λ_i = 0 (take s_i = 1 on T, 0 elsewhere: s_i^{p−1} ∈ {0,1}). For distinct nonempty
T and T' the vectors 1_T and 1_{T'} are linearly independent over F_p. Under the label law the
pair (Σ_T λ, Σ_{T'} λ) is therefore uniform on (K_c^⊥)², and Chebyshev gives
Pr[no zero-sum subset] ≤ p^{a}/(2^M − 1) (**proved**; exhaustive check on eight cases with
p ≤ 7, a ≤ 2, M ≤ 5, exact). With M = ⌈g_c log2 p + log2(1/τ_c)⌉ + 1 and exhaustive search
over the 2^M subsets, the node costs O(p^{g_c}/τ_c) ≤ (r+2)^r·poly(S n_c) classical time. Fitting
the node into `lem:fc-forest` as a fourth node kind is **argued** only: the induction and the
union bound are unchanged, with bank event τ_c and no capped steps. This would give
`cor:fpt-r` for both input models at every p > c from (iii) plus this node alone.

## The exact statement that now holds

All of the following is AI-checked only and pending human review. Every claim is conditional
exactly as stated.

1. **(exact computation)** `tab:fcs-budget` is reproduced in full: 32 numbers and 4 dashes, from
   `rem:combined-schedule`, `thm:free-coordinate`(iii) with rule (R1) and least public arities,
   the node formulas of `thm:random-column`, and Q = c·S·∏M_d. No entry disagrees. The
   uniform-kernel columns use a mixed rule that is defined by the script and not stated in the
   paper (A.4).
2. **(proved, conditional)** *Derived dimension.* Let r = dim[L,L] ≥ 1, let c < p, and let the
   class be free. (i) For every prime p ≥ c+2, conditional on the steps behind `thm:main` and
   on `thm:free-coordinate`(iii): the HSP of `def:input-contract` is solved with probability
   ≥ 1−ε from 2^{O(r log(r+2))}·poly(m)·⌈18 ln(1/ε)⌉ queries, in time
   2^{O(r log(r+2))}·poly(m, log p, w, log(1/ε)). The guarantee covers the i.i.d. ideal supply
   of fresh lifted sources only; coset-copy input is **argued**. (ii) At p = c+1, which is
   possible only when c+1 is prime, the same time bound holds for oracle input through IMS
   Theorem 11, with no Rees step.
3. **(proved, conditional)** *Hidden codimension.* Under the hypotheses of `thm:app-codim`
   and conditional on `thm:free-coordinate`(iii): for every prime p > c, non-oracle time is
   2^{O(k log(k+2))}·poly(m, log p, w, log(1/ε)) and Q = 2^{O(k log(k+2))}·poly(m, log(1/ε)).
   Branches: birthday at p ≤ 2k; reduction plus (iii) with plurality amplification at p ≥ 2k+1.
4. **(proved)** The obstruction to an "(iii) only" proof is the zero-sum grade d = p−1 = c at
   p = c+1. There the fallback arity B_c(g_c) is 2^{Ω(r² log² r)} for c = r+1. Exact example:
   filiform r = 9 at p = 11 needs log2 Q = 676.8, against log2 |G'| = 31.1.

## Still missing

- Human review of everything above, of `thm:free-coordinate` and of `lem:s3-law`. This is the
  binding gate.
- A theorem for the mixed uniform-kernel rule. Otherwise the caption change below suffices.
- A polynomial-time finder at the zero-sum grade κ = p−1. The optional zero-sum node in B.5 is
  exponential in g_c log p, so it serves only the FPT corollary, and its fit into
  `lem:fc-forest` is argued only.
- Integration by the parent: the `numbers_map.json` entries, regenerating `numbers.tex`, and
  committing the JSON together with `numbers.tex`.
- `tab:query-crossover` is still hand-typed.
- The current `cor:fpt-r` small-prime branch silently needs oracle input (IMS certification
  evaluates f). The restatement makes this explicit; the owner may want to say so in the
  change log.

## Claim gates (all stay false)

`speedup_claim_allowed = false`, `independent_review = false`, `novelty_established = false`,
`coherent_receiver_implemented = false`, `general_sde_implemented = false`,
`formal_compiler_checked = false`. Nothing here bears on a speedup. Query bounds are upper
bounds, and the bounded-codimension result remains a gap between upper bounds.

## Tests run

```
/opt/anaconda3/bin/python -m theorems.rees_fcs_budget          # writes fcs_budget.json, ~0.2 s
/opt/anaconda3/bin/python -m pytest -q tests/test_rees_fcs_budget.py   # 9 passed
```

The test checks: the JSON against the printed table; that the printed table equals the live
`main.tex` table, parsed; that the JSON is current; the rounding margins; the
`app:fc-numbers`(a) claims; the minimality of the least arities; the uniform-kernel flags; the
32 macro paths; and hand-checkable spot values (`B_d(a)`, the combined rule at p = 11).

## Proposed paper text

Every block is **AI-checked, pending human review**. It cites only labels that exist now
(each checked by grep to occur exactly once) and adds no new `\label`. Targets refer to the
working tree of 2026-11-04.

### T1. `main.tex`, Table `tab:fcs-budget`: replace the caption (line 672) and the six body rows (lines 679–684)

Requires the 32 `numbers_map.json` entries of A.5 and a regenerated `numbers.tex`.

```latex
\caption{Class-nine profile $g = (19,17,16,14,12,9,6,3,1)$, $\eps = 1/3$: $\log_2$ of the query count $Q$ under the worst-case combined rule of Remark~\ref{rem:combined-schedule} (no label law) and under Theorem~\ref{thm:free-coordinate}(iii) with the least public arities. For comparison only, the uniform-kernel columns mix the nodes of Theorem~\ref{thm:random-column}(i) into the combined rule, with node-count-weighted bank bounds and the tree restarts of Theorem~\ref{thm:random-column}(ii). That mixed rule is defined by the generating script, keeps Schedule~2 at some grades, and is not a result of this paper. A dash marks a prime at which it uses no uniform-kernel node. ``Trials'' is the largest $\log_2$ per-node classical trial count (a worst-case cap with $a_d = g_d$), and ``total'' is the $\log_2$ total over all nodes. Exact computation by \file{theorems/rees_fcs_budget.py}, which writes \file{research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json}; the numbers are macros generated from that file, and \file{tests/test_rees_fcs_budget.py} checks them against the formulas. AI-checked, pending human review.}
```

```latex
$11$ & $\FcsElevenCombQ$ & -- & -- & $\FcsElevenFcQ$ & $\FcsElevenFcTrials$ & $\FcsElevenFcTotal$ \\
$1031$ & $\FcsTenThirtyOneCombQ$ & -- & -- & $\FcsTenThirtyOneFcQ$ & $\FcsTenThirtyOneFcTrials$ & $\FcsTenThirtyOneFcTotal$ \\
$5281$ & $\FcsFiftyTwoEightyOneCombQ$ & $\FcsFiftyTwoEightyOneUkQ$ & $\FcsFiftyTwoEightyOneUkTrials$ & $\FcsFiftyTwoEightyOneFcQ$ & $\FcsFiftyTwoEightyOneFcTrials$ & $\FcsFiftyTwoEightyOneFcTotal$ \\
$2^{31}-1$ & $\FcsMersThirtyOneCombQ$ & $\FcsMersThirtyOneUkQ$ & $\FcsMersThirtyOneUkTrials$ & $\FcsMersThirtyOneFcQ$ & $\FcsMersThirtyOneFcTrials$ & $\FcsMersThirtyOneFcTotal$ \\
$2^{61}-1$ & $\FcsMersSixtyOneCombQ$ & $\FcsMersSixtyOneUkQ$ & $\FcsMersSixtyOneUkTrials$ & $\FcsMersSixtyOneFcQ$ & $\FcsMersSixtyOneFcTrials$ & $\FcsMersSixtyOneFcTotal$ \\
$2^{127}-1$ & $\FcsMersOneTwentySevenCombQ$ & $\FcsMersOneTwentySevenUkQ$ & $\FcsMersOneTwentySevenUkTrials$ & $\FcsMersOneTwentySevenFcQ$ & $\FcsMersOneTwentySevenFcTrials$ & $\FcsMersOneTwentySevenFcTotal$ \\
```

If the parent does not wire the macros, keep the typed numbers. They are correct. Replace only
the caption's last sentence with: "Exact computation by \file{theorems/rees_fcs_budget.py}
(\file{research/audits/reviews/2026-11-04-rees-fcs-budget/fcs_budget.json}); these numbers are
not macros. AI-checked, pending human review."

### T2. `main.tex`, artifact paragraph (line 1048)

Replace `Tables~\ref{tab:fcs-budget} and~\ref{tab:query-crossover}` with
`Table~\ref{tab:query-crossover}` (only if T1 is applied with macros).

### T3. `main.tex`, Corollary `cor:fpt-r` and its proof (lines 698–705): replace

```latex
\begin{corollary}[Bound in derived dimension for every prime $p > c$, class not fixed; conditional; AI-checked, pending human review]
\label{cor:fpt-r}
Let $r = \dim_{\Fp}[\mathcal{L},\mathcal{L}] \ge 1$ and $c < p$; the class need not be fixed.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item If $p \ge c+2$, then, conditional on the steps behind Theorem~\ref{thm:main} and on Theorem~\ref{thm:free-coordinate}(iii), the HSP of Definition~\ref{def:input-contract} is solvable with bounded error from $2^{O(r\log(r+2))}\cdot\poly(m,\log(1/\eps))$ oracle queries, or as many copies of $\rho_H$, in time $2^{O(r\log(r+2))}\cdot\poly(m,\log p,\text{label width},\log(1/\eps))$.
  \item If $p = c+1$, the HSP of Definition~\ref{def:input-contract} with a coherent oracle is solvable with bounded error in time $2^{O(r\log(r+2))}\cdot\poly(m,\log p,\text{label width},\log(1/\eps))$, by an imported algorithm and with no Rees step.
\end{enumerate}
\end{corollary}

\begin{proof}
Each nonzero $\gamma_{d+1}(\mathcal{L})$ is a proper subspace of $\gamma_d(\mathcal{L})$, so $g_2 > g_3 > \cdots > g_c \ge 1$. Hence $c \le r+1$ and $a_d \le g_d \le r$. The case $r = 0$ is abelian.

(i) If $p \ge c+2$, no grade has $\kappa_d = p-1$: otherwise $p-1$ divides $d < p$, so $d = p-1 > c$. So the procedure of Theorem~\ref{thm:free-coordinate}(iii) uses only free-coordinate and linear nodes, and $t_{\mathrm{S1}} = 0$ in Proposition~\ref{prop:fc-uniform}(b). Run it with error $1/3$ and the explicit arities of Lemma~\ref{lem:fc-choice}. Put $S = m + \lceil\log_p 9\rceil \le m+2$ and $\alpha = (1+2\log_2 c)\,r + 3\log_2(216cS) + 3$. The proof of Proposition~\ref{prop:fc-uniform}(b) gives $M_d \le \alpha + 3\log_2 n_d$ at every free-coordinate grade, and $M_d = g_d+1 \le \alpha$ at a linear grade. The map $t \mapsto 2^t/(4t)$ increases for $t \ge 2$, and $2^\alpha \ge 16(216cS)^3c^2$, so $\log_2(4\alpha c) \le \alpha$. Induction on $d$ then gives $\log_2 n_d \le (d-2)\log_2(4\alpha c)$ and $M_d \le (1+3c)\alpha \le 4\alpha c$. One run therefore makes $Q_1 = cS\prod_dM_d \le cS(4\alpha c)^{c-1}$ queries. With $c \le r+1$, $4\alpha c \le C(r+2)^2\log_2(r+2) + 12(r+2)\log_2 S$ for an absolute constant $C$. For integers $r \ge 1$ and reals $x \ge 1$, $x^r \le \max(r^{2r}, 2^{16}, 2^x)$. Hence $Q_1 \le 2^{O(r\log(r+2))}\,S^2$. Repeat the run $R = \lceil 18\ln(1/\eps)\rceil$ times (once if $\eps \ge 1/3$), and output the subspace returned most often. The runs are independent, and each returns $\hh$ with probability at least $2/3$. By Hoeffding's inequality, $\hh$ is returned by more than $R/2$ runs except with probability at most $e^{-R/18} \le \eps$. The vote evaluates no oracle, so it also applies to coset-copy input, where Lemma~\ref{lem:copy-lift} makes each lifted source from $c$ copies. Proposition~\ref{prop:fc-uniform}(b) bounds the classical time of a run, with $\kappa_d^{\,g_d} \le (r+1)^r$, $B \le \log_2(81Q_1)+1$ and $\max_dM_d \le 4\alpha c$. A run has at most $3Q_1$ complete instruments, and Theorem~\ref{thm:uniform-compilation} compiles each in time $\poly(c,m,\log p,w,\log Q_1)$ with $c \le r+1$. This branch uses the i.i.d.\ label law of fresh ideal sources (Lemma~\ref{lem:s3-law}), whose derivation has been checked by AI review only. The corollary is conditional for that reason as well, not only through the core composition.

(ii) If $p = c+1$, then $c \le r+1$ gives $|G'| = p^r \le (r+2)^r = 2^{O(r\log(r+2))}$. Use the quantum algorithm of Ivanyos, Magniez and Santha for groups with small commutator subgroup~\cite[Theorem~11, Section~5]{IvanyosMagniezSantha2001} (numbering of the arXiv version). For a black-box group with unique encoding, which the explicit chart provides, it runs in time polynomial in the input size plus $|G'|$, and it handles an arbitrary hidden subgroup. Two charges are added. First, that time counts each group-oracle call as one step, so each call is charged one reversible BCH evaluation, $\poly(m,r,\log p)$. Second, that algorithm has a fixed constant error, so it is amplified. Run it $O(\log(1/\eps))$ times, certify each returned $H' \le H$ by checking $f(x) = f(1)$ on its returned generators, compute $|H'|$ by linear algebra on the Lie subalgebra generated by their logarithms, and output the largest certified $H'$. A correct run has order $|H|$, and a certified $H' \le H$ of that order equals $H$. This certification evaluates $f$, so part~(ii) needs a coherent oracle.
\end{proof}
```

Then, in the paragraph after the proof ("The source is \file{research/RANDOM_COLUMN_REES_PARAMETER_BOUND.md}, Section~5."), add after its first sentence:

```latex
The earlier proof used Theorem~\ref{thm:random-column} for $p \ge 16(r+1)^2$ and the imported algorithm for $p < 16(r+1)^2$; that proof remains valid for oracle input. The free-coordinate branch is derived in \file{research/audits/reviews/2026-11-04-rees-fcs-budget.md}, Part~B (AI-checked, pending human review). At $p = c+1$ the grade $d = c$ has $\kappa_c = p-1$, where Theorem~\ref{thm:free-coordinate}(iii) falls back on Schedule~1 with arity $B_c(g_c) \ge c^{c(c-1)\lceil\log_2(c+1)\rceil/2}$, which is $2^{\Omega(r^2\log^2 r)}$ when $c = r+1$; this is why part~(ii) is imported.
```

### T4. `main.tex`, Table `tab:main-regimes`, lines 215–216: replace the two rows

```latex
Derived dim.\ $r$ & all $p > c$, class not fixed & free coordinates, Thm.~\ref{thm:free-coordinate}(iii) ($p \ge c+2$) / IMS Theorem~11 ($p = c+1$, oracle input) & $2^{O(r\log(r+2))}\cdot\poly$ total (Cor.~\ref{cor:fpt-r}) \\
Hidden codim.\ $k$ & all $p > c$, oracle input & abelian-ideal reduction, then free coordinates, Thm.~\ref{thm:free-coordinate}(iii) ($p \ge 2k+1$) / classical birthday ($p \le 2k$) & $2^{O(k\log(k+2))}\cdot\poly$ total (Cor.~\ref{cor:codim}) \\
```

### T5. `main.tex`, Corollary `cor:codim`(ii) and the (ii) sentences of its proof

Replace item (ii) with:

```latex
  \item Conditional also on Theorem~\ref{thm:free-coordinate}(iii), or alternatively on Theorem~\ref{thm:random-column}, it is solvable with $2^{O(k\log(k+2))}\cdot\poly(m,w,\log(1/\eps))$ oracle queries, in time $2^{O(k\log(k+2))}\cdot\poly(m,\log p,w,\log(1/\eps))$ plus the oracle's internal cost.
```

In the proof, replace the two sentences from "For~(ii), when $p \ge 64k^2$" to "suffices." with:

```latex
For~(ii), when $p \ge 2k+1$, the remainder has class at most $2k-1 \le p-2$, so none of its grades has $\kappa_d = p-1$. Use Theorem~\ref{thm:free-coordinate}(iii) on it with error $1/3$, repeated $O(\log(1/\eps))$ times with a plurality vote as in the proof of Corollary~\ref{cor:fpt-r}(i). Its arities are $O(k^2\log(k+2))$ at each of at most $2k-2$ grades, and its trial counts use the observed rank, which is at most $a_d \le k$. When $p \le 2k$, $p^{k/2} \le (2k)^{k/2} = 2^{O(k\log(k+2))}$, so the classical birthday learner, which samples uniform $x^{-1}y$ from label collisions, suffices. Alternatively, Theorem~\ref{thm:random-column} with $u = 2k$ and $M = 8k$ covers $p \ge 64k^2$, and the birthday learner covers $p < 64k^2$.
```

### T6. `appendix-codimension.tex`

(a) Status paragraph (line 35): replace "Part~(ii) is conditional on Theorem~\ref{thm:random-column}, whose proof uses" with

```latex
Part~(ii) is conditional on Theorem~\ref{thm:free-coordinate}(iii) or, by a second proof, on Theorem~\ref{thm:random-column}; both proofs use
```

(b) `thm:app-codim`(ii) (line 47): replace "Conditional on Theorem~\ref{thm:random-column}, and hence on the Rees composition its proof uses:" with

```latex
Conditional on Theorem~\ref{thm:free-coordinate}(iii), or alternatively on Theorem~\ref{thm:random-column}, and hence on the Rees composition their proofs use:
```

(c) In the proof of `thm:app-codim`, after the paragraph "\emph{Part~(ii).} …", insert:

```latex
\emph{Part~(ii) from Theorem~\ref{thm:free-coordinate}(iii).} Branch on the public integers $p$ and $k$ instead as follows. If $p \le 2k$, use Proposition~\ref{prop:app-codim-birthday} on the original instance: $B \le 4p^{k/2} \le 4(2k)^{k/2}$, so $\log_2 B \le (k/2)\log_2(2k) + 2$. If $p \ge 2k+1$, run the reduction. At a nonabelian terminal ($k \ge 2$), Proposition~\ref{prop:app-codim-complete}(iii) gives class $c_J \le 2k-1 \le p-2$ and $\dim\mathcal{L}_J \le k(k+1)/2$, so no grade of $\mathcal{L}_J$ has $\kappa_d = p-1$. The terminal is an instance of Definition~\ref{def:input-contract} with an ordinary coherent oracle, as in the proof of Proposition~\ref{prop:app-codim-rc}, so Lemma~\ref{lem:s3-law} gives the label law of its fresh lifted sources. Run the procedure of Theorem~\ref{thm:free-coordinate}(iii) on it $R = \lceil 18\ln(2/\eps)\rceil$ times with error $1/3$ and the explicit arities of Lemma~\ref{lem:fc-choice}, and output the subspace returned most often. By Hoeffding's inequality this errs with probability at most $e^{-R/18} \le \eps/2$, the terminal share of the error budget. The bound in the proof of Corollary~\ref{cor:fpt-r}(i), with $c_J \le 2k-1$, $g_d \le k(k+1)/2$ and $S_J = \dim\mathcal{L}_J + \lceil\log_p 9\rceil \le k(k+1)/2 + 2$, gives at most $c_JS_J(4\alpha_Jc_J)^{c_J-1} = 2^{O(k\log(k+2))}$ queries per run, with $\alpha_J = O(k^2\log(k+2))$; this count depends neither on $m$ nor on $p$. Each free-coordinate node draws at most $\lceil 2B\ln 2\cdot q^{-r}\rceil \le 2B\ln 2\cdot(2k-1)^k + 1$ trials, because its observed rank $r$ is at most $a_d \le k$ (Lemmas~\ref{lem:fc-rref}(a) and~\ref{lem:app-codim-ad}). There are fewer nodes than queries, and $B \le \log_2(81Q_J) + 1$. The non-oracle time of the terminal is therefore $2^{O(k\log(k+2))}\cdot\poly(\log p,w,\log(1/\eps))$, and each terminal query costs one query to $f$ plus $\poly(m,\log p)$ arithmetic. The rest is as in the first proof. The displayed time bound of Proposition~\ref{prop:fc-uniform}(b), which uses $\kappa_d^{\,g_d}$, would not suffice here.
```

(d) Scope paragraph: replace "it selects the branch $p \gtrless 64k^2$," with

```latex
it selects the branch ($p \gtrless 64k^2$, or $p \gtrless 2k$ in the proof from Theorem~\ref{thm:free-coordinate}(iii)),
```

### T7. `appendix-free-coordinate.tex`, the paragraph after the proof of `prop:fc-uniform` (line 279): replace it

```latex
At fixed $c$ the query count of part~(iii) is polynomial in $m$ and $\log(1/\eps)$. For general profiles its degree grows with $c$, as for Schedules~1 and~2, because $g_d$ can be of order $m$. Part~(ii) gives bounds that are uniform in $c$ for every profile with $a_d \le u-1$, since there every arity is the constant $4u$. When every $g_d$ is at most a parameter $r$, $c \le r+1$ and $p \ge c+2$, part~(iii) also gives $2^{O(r\log(r+2))}\cdot\poly(m)$ queries per run at error $1/3$, uniformly in $c$; see the proof of Corollary~\ref{cor:fpt-r}(i). (AI-checked, pending human review.)
```

### Dependencies among the blocks, and downstream uses

- T5, T6(c) and T7 cite `Corollary~\ref{cor:fpt-r}(i)`, so they need T3. T2 needs T1 with
  macros. T4 can be applied on its own once T3 and T5 are in.
- Downstream uses of `cor:fpt-r` (`thm:ring-to-field`(ii) and `appendix-torsion-blackbox.tex`
  near lines 43, 324 and 500) restrict an ordinary oracle f. They therefore stay inside
  part (i) or part (ii) of the restated corollary, and none of them needs changing. The use
  near line 790 says the corollary is not used there.

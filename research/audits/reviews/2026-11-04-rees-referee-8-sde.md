# Rees HSP paper, referee 8: Section `sec:sde` and Appendix `app:schedule2`

2026-11-04. Independent AI referee (Claude Code subagent). This is not a human review.
Local only: no git, no network, no `.tex` file edited. Every statement below is
AI-checked, pending human review.

**Scope.** `docs/papers/rees-hsp/main.tex`, Section `sec:sde` (lines 509–723). Within it:
`thm:is-import`, `rem:is-import`, `rem:is-runtime`, Schedules 1–3, `thm:power-sde`,
`prop:decoupled-sde`, the paragraph after it (line 650), `prop:triangular-sde` and
`rem:combined-schedule`. Also all of `docs/papers/rees-hsp/appendix-schedule2.tex`.
Data used: the `dfs2`/`dfs2b` outputs in
`research/audits/reviews/2026-11-02-rees-schedules/small-prime/`, read between 19:17 and
19:26 AEDT while four scans were still writing; `2026-11-04-rees-threshold-5.md` §5–6 and its
folder; `2026-11-04-rees-t1-sweep-hi.md`.

**Counts.** Error 2, Gap 2, Imprecision 9, Style 3.

Line numbers are those of the files as read. Main-text paragraphs are single long lines, so
"main 650" means the paragraph after `prop:decoupled-sde`.

---

## A. Data checks (what I recomputed)

### A.1 E_2(8) and E_2(9) from the scans [exact, my scripts]

Method. I parsed every `dfs2b_k{8,9}_*.out` and `dfs2_k{8,9}*.out`. I applied the stated rule
for the old `dfs2` chunks: a prime the chunk passed without printing counts as FEASIBLE if the
chunk printed a later line. `dfs2.c` calls `fflush` after every prime (line 118), so a silent
prime really was passed. The ranges used are `dfs2_k8.out` = [2442, 4057], `dfs2_k9.out` =
[3584, 5689], and the other chunks from their file names. I then required every prime
p ≡ 1 (mod κ) from the start of each range up to a bound to have exactly one verdict.

Results:

| check | κ = 8 | κ = 9 |
|---|---|---|
| conflicting verdicts (FEASIBLE and INFEASIBLE for one p, any files) | none | none |
| contiguous decided range from 2442 / 3584 | up to **11393** (first undecided: 11489) | up to **14293** (first undecided: 14347) |
| below that start (`2026-11-02-rees-small-prime-arity.md` §3) | 82 of the 83 primes ≤ 2441 in E_2(8), 1553 feasible | 82 of the 83 primes ≤ 3583 in E_2(9), 3529 feasible |
| largest INFEASIBLE in decided range | **11321** = 0.977·8^{4.5} | 14293 = 0.242·9^5 |
| largest INFEASIBLE anywhere | 11321 | **17749** = 0.3006·9^5 (`dfs2b_k9_17501_20000.out`) |
| known elements of E_2 in decided range | 270 | 256 (plus 20 above 14347) |
| paper's values | decided to 11161, 11161 ∈ E_2(8), factor 0.96 | decided to 13807, 17713 ∈ E_2(9), factor 0.29 |
| paper's values supported? | **yes** (11161/8^{4.5} = 0.9634) | **yes** (13807 is in the decided range; 17713 is INFEASIBLE; 17713/9^5 = 0.29997 ≥ 0.29) |

The paper's numbers are correct but out of date. Finding I1 gives the current values.

- **Witnesses.** I re-checked all 69 FEASIBLE witness lines of every `dfs2b_k*.out` with a
  separately written checker. It checks that p is prime, that g^h has exact order κ, that
  α_j + β_i ∈ Q°_{−(i+j)} in all κ² cells and that the (0,0) cell is nonzero. Result: 69 valid,
  0 bad. The witnesses have 124 zero cells in total, none at (0,0).
- **Family witnesses.** None of the 123 primes in
  `2026-11-04-rees-threshold-5/feasible_below20000_k8.txt` is INFEASIBLE in a scan. Every one
  of them inside the decided range is FEASIBLE there.
- **Agreement with unpruned runs.** `dfs2b_k8_6073_{plain,nosym}.out` and
  `dfs2b_k9_6067_{plain,nosym}.out` say INFEASIBLE, as the paper states.
- **Provenance below 4202 (κ = 8).** This part comes from the old unpruned `dfs2`:
  `dfs2_k8.out`, six LIMIT reruns, and `dfs2_k8_4058_6000.out` (whose last line is LIMIT 4201,
  so 4177 counts as FEASIBLE). `dfs2-prune.md` §2 reports that `dfs2b` reproduces [9, 4201].
  Its output `k8_full.out` stayed in a scratchpad and is not in the repository.
- **Provenance in [3584, 5689] (κ = 9).** This is `dfs2_k9.out` alone (dfs2, round 1).
  `dfs2b` starts at 5690 for κ = 9.
- **The (49417, 8^8/2] claim.** `verify_sweep_k8.out` reports 139,558 witnesses, bad = 0,
  missing = 0. Supported.
- **The band (20000, 49417].** `verify_band_k8_zeros.out` lists 29 missing primes, and 4
  primes (22921, 25321, 26681, 26713) with zero-cell witnesses only. The paper does not use
  this; see finding I2.
- **(8^8/2, T_A(8)].** The paper makes no claim here. At 19:26 the sweep had 651,458 FOUND
  lines and no NOTFOUND line, with no worker done. Its last verified snapshot is contiguous
  to 36,056,592. Nothing in the paper should change until `verify.sh` passes.

### A.2 T_A, T_S, T_W and the table [float, 50-digit mpmath, bisection on U_κ]

I wrote my own implementation of Δ, u_Δ, v_Δ, E_max and U_κ from appendix lines 367–376.
E_max is maximised exactly: the vertex v/(2u) if u > 0, clipped to [0, √κΔ], otherwise
an endpoint.

- **T_A(8) = 117441562.029.** U_8(117441562) = 1.1428571428920 > 8/7 and
  U_8(117441563) = 1.1428571416756 < 8/7. So the integrator's **117441563 is ⌈T_A(8)⌉**:
  the least integer p with U_8(p) < 8/7. That is the right endpoint for a sweep. Note
  T_A(8) − 7·8^8 = 1050.03. So T_A(8) exceeds the lower bound (κ−1)κ^κ of
  `prop:app-s2-TA`(ii) by a relative 9·10⁻⁶, which is why the table shows the same three
  digits in both columns for κ ≥ 7.
- **Every entry of Table `tab:app-s2-thresholds`** (16κ^{2κ+2}, T_W, T_A, (κ−1)κ^κ, T_S for
  κ = 2..9) matches to the printed precision. Examples: T_A(3) = 79.039, T_A(4) = 868.996,
  T_A(5) = 12657.6, T_S(4) = 8596.4, T_S(9) = 2.789·10^{10}.
- **The κ = 3, 4, 5 values** at κ^{κ+1}: Δ = 0.2857, 0.1943, 0.09655 and U = 1.48419,
  1.27937, 1.20238. The margins are 0.01581, 0.05397, 0.04762. All match appendix lines
  412–421.
- **T_S(κ)/κ^{κ+1} for 3 ≤ κ ≤ 40**: at most 9.075 (at κ = 3), at most 8.395 for κ ≥ 4, and
  tending to 8. This supports "T_S ≤ 10κ^{κ+1}, ≤ 9κ^{κ+1} for κ ≥ 4". T_A(κ) ≤ κ^{κ+1} and
  T_A(κ) > (κ−1)κ^κ hold for every κ in 3..40.
- **Ratios.** 16κ^{2κ+2}/T_W(κ) = 156.1 at κ = 2 and 26.449 at κ = 9 (printed "26.4").
  117441563/8388608 = 14.0001 ("a factor of about 14"). 49417/8^{4.5} = 4.27.
- **The proof constants of the κ ≥ 6 argument** (lines 406–410): Δ(P) ≤ 1.01κ^{(3−κ)/2} ≤ 0.0687,
  u_Δ ≥ 0.2815, E_max ≤ 1.1245κ^{2−κ}, and 2κ^{1−κ} + 2.4κ^{4−κ} = 0.0669 at κ = 6. All
  hold.

### A.3 Proofs read line by line (no defect beyond the findings)

These hold as written:
- Lemma `app-s2-gcd`.
- Lemma `app-s2-tensor`.
- The ξ-independence paragraph.
- Lemmas `app-s2-witness` and `app-s2-normal`, including the dimension count 2κ−1.
- Lemma `app-s2-weil-count` and its closed form. I re-derived both binomial sums.
- Lemma `app-s2-stage`.
- The abort and cost bounds of Theorem `app-s2-main` (2^{−k−3} + 2^{−k−3} + 2^{−k−1} < 2^{−k}).
- Proposition `app-s2-TW`, including κ^κE_κ(κ,p) = A_κ√p + κ^κ − κ.
- Lemma `app-s2-moments`. I re-derived the pair count h·m'_{c'+j} and the index shift
  −(i+c).
- Lemma `app-s2-cyclo`. I re-derived all four exact Jacobi-sum classes for m_b and for m'_c,
  including the (s, −s) phase ω^{cs} in m'_c.
- Proposition `app-s2-TA`:
  - the substitution giving L and F;
  - log(1+x) ≤ x − x²/2 + x³/3 on (−1, ∞) (the derivative is x³/(1+x));
  - the Cauchy–Schwarz step;
  - monotonicity, the lower bound, and Chebyshev for the sampler.
- The arity bound Π M_d^sym ≤ r!((r+1)!)² (main 643). It uses g_d = dim γ_d(L), the Rees
  grade.
- The exponent 1 + Σ_{d=2}^{9} d⌈log₂(d+1)⌉ = 145.
- B_4(2) = 331776³ ≈ 3.65·10^{16}.
- The Davenport example in `thm:power-sde`(iii).
- The proof of `prop:triangular-sde` (the back-substitution invariant τ ∈ U_{l−1}, disjoint
  supports, and weight 1 on one column of R), apart from G1 and G2.
- The prunes of `dfs2b` (`dfs2-prune.md` §1). In particular Prune 2d is sound for the
  zero-allowed definition of E_2: any solution with a zero cell has min R = 0 and survives in
  the v = 0 branch.

---

## B. Findings

### E1 (Error). The decided ranges are attributed to the pruned search, but part of them comes from older runs

*Where.* Appendix line 470, and main 650.
- Appendix: "Each such verdict is a single run of the pruned search; the prunes are proved in
  the cited report".
- Appendix parenthesis: "(an earlier search had decided the primes below $2442$ for
  $\kappa = 8$ and below $3584$ for $\kappa = 9$: [small-prime-arity] and [dfs2-prune],
  Section~2)".
- Main 650: "an exhaustive search with symmetry breaking and proved prunes decides every
  prime …".

*Why.* The data do not support "each verdict is a run of the pruned search":
- For κ = 8 on [2442, 4201] the verdicts in the repository come from the unpruned `dfs2`
  (`dfs2_k8.out`, `dfs2_k8_4058_6000.out` and the six reruns). The `dfs2b` reproduction of
  [9, 4201] is reported, but its output `k8_full.out` is not in the repository.
- For κ = 9 on [3584, 5689] the only source is `dfs2_k9.out`, which is also unpruned.
- Below 2442 and 3584 the source is the DFS of `small-prime-arity.md` §3.
- `dfs2-prune.md` §2 covers κ = 8 up to 4201. It does not cover κ = 9 below 3584.
- The prunes are proved only in an AI-only report, and main 650 calls them "proved" without
  that qualifier.

*Fix (appendix 470).* Replace the parenthesis
"(an earlier search … Section~2)" and the sentence "Each such verdict … $p = 6067$." with:

```latex
(an earlier search had decided the primes below $2442$ for $\kappa = 8$ and below $3584$ for $\kappa = 9$, finding $82$ exceptional primes among the $83$ in each range: \file{research/audits/reviews/2026-11-02-rees-small-prime-arity.md}, Section~3). Below $4202$ for $\kappa = 8$ and below $5690$ for $\kappa = 9$ the verdicts come from an unpruned depth-first search (the \texttt{dfs2} outputs in \file{research/audits/reviews/2026-11-02-rees-schedules/small-prime/}), which the pruned search reproduces for $\kappa = 8$ up to $4201$ (\file{research/audits/reviews/2026-11-03-rees-dfs2-prune.md}, Section~2). Above these bounds each verdict is a single run of the pruned search. Its prunes are proved in that report (AI-checked, pending human review), and it agrees with an unpruned run at $p = 6073$ for $\kappa = 8$ and at $p = 6067$ for $\kappa = 9$.
```

*Fix (main 650).* Replace "an exhaustive search with symmetry breaking and proved prunes
decides" with:

```latex
exhaustive searches (finite computations, AI-checked, pending human review; Section~\ref{app:s2-scope}) decide
```

### E2 (Error). The "Terms" paragraph says every quoted E_2 value is exhaustive up to a proved threshold

*Where.* Main 625: "The values of $E_2(\kappa)$ quoted below come from an exhaustive search
over $(\beta,\alpha)$ that tests all $\kappa^2$ coset conditions directly, up to an explicit
threshold above which a contraction is proved to exist".

*Why.* This is true for κ ≤ 7 only:
- For κ = 8 the search has reached 11393, against T_A(8) ≈ 1.17·10^8.
- The range (49417, 8^8/2] comes from explicit witnesses, not from an exhaustive search.
- For κ = 9 the search has reached 14293, against T_A(9) ≈ 3.1·10^9.

The paragraph after `prop:decoupled-sde` quotes κ = 8 and 9 values, so the sentence covers
them.

*Fix.* Replace the sentence with:

```latex
For $\kappa \le 7$ the values of $E_2(\kappa)$ quoted below come from an exhaustive search over $(\beta,\alpha)$ that tests all $\kappa^2$ coset conditions directly, up to an explicit threshold above which a contraction is proved to exist (Corollary~\ref{cor:app-s2-small} and the reports cited after Proposition~\ref{prop:decoupled-sde}). For $\kappa = 8$ and $9$ the search has not reached that threshold, and only partial information is quoted.
```

### I1 (Imprecision). The κ = 8, 9 numbers are correct but stale, and are not marked as snapshots

*Where.* Main 650 and appendix 470: "up to $11161$ … up to $13807$ … $11161 \in E_2(8)$ … $17713
\in E_2(9)$ … $0.96$ … $0.29$".

*Why.* The values are supported (A.1), but the scans have moved on. At 19:17 AEDT the data
support:
- κ = 8: decided to 11393, with 11321 ∈ E_2(8) (0.977·8^{4.5}). 11177, 11257, 11273 and 11321
  are INFEASIBLE.
- κ = 9: decided to 14293, with 17749 ∈ E_2(9) (0.3006·9^5).

Four scans are still running, so any value printed is a lower bound. The text should say so,
as `threshold-5` §6.3 asks. If the integrator prefers not to chase the scans, keep the old
numbers and add only "(lower bounds while the scans run)".

*Fix (main 650).* Replace from "for $\kappa = 8$ and $9$ the exceptional sets are not known
exactly, but" through "(Section~\ref{app:s2-scope}, with sources);" with:

```latex
for $\kappa = 8$ and $9$ the exceptional sets are not known exactly, but exhaustive searches (finite computations, AI-checked, pending human review) decide every prime $p \equiv 1 \pmod 8$ up to $11393$ and every prime $p \equiv 1 \pmod 9$ up to $14293$, and show $11321 \in E_2(8)$ and, by separate runs, $17749 \in E_2(9)$. So the largest exceptional prime is at least $0.97\,\kappa^{(\kappa+1)/2}$ for $\kappa = 8$ and at least $0.30\,\kappa^{(\kappa+1)/2}$ for $\kappa = 9$; these are lower bounds while the scans run. Explicit contractions give $E_2(8) \cap (49417, 8^8/2] = \emptyset$, and $E_2(8) \cap (20000, 49417]$ is contained in a list of $29$ primes (Section~\ref{app:s2-scope}, with sources);
```

*Fix (appendix 470).* In the sentence that begins "decides every prime", put $11393$ for
$11161$ and $14293$ for $13807$. Replace "shows $11161 \in E_2(8)$ and, by a separate run,
$17713 \in E_2(9)$, so the largest exceptional prime is at least $0.96\,\kappa^{(\kappa+1)/2}$
for $\kappa = 8$ and at least $0.29\,\kappa^{(\kappa+1)/2}$ for $\kappa = 9$." with:

```latex
shows $11321 \in E_2(8)$ and, by separate runs above the decided range, $17749 \in E_2(9)$. So the largest exceptional prime is at least $0.97\,\kappa^{(\kappa+1)/2}$ for $\kappa = 8$ and at least $0.30\,\kappa^{(\kappa+1)/2}$ for $\kappa = 9$. These values are a snapshot of scans that were still running on 2026-11-04 and are lower bounds only.
```

Re-run the coverage check of Appendix C before integrating, since the files keep growing.

### I2 (Imprecision). "(11161, 49417] only partly decided" leaves out what is known

*Where.* Appendix 470: "That range ends a factor of about $14$ below $T_A(8) \approx
1.17\cdot10^{8}$, and the primes in $(11161, 49417]$ are only partly decided."

*Why.* `threshold-5` §5 and `verify_band_k8_zeros.out` decide every prime of (20000, 49417]
except 29. Of the decided ones, 4 have only contractions with a zero cell, which still puts
them outside E_2(8). This gives E_2(8) ⊆ [3, 20000] ∪ X_29 ∪ (8^8/2, T_A(8)], which the paper
should state.

*Fix.* Replace that sentence with:

```latex
In $(20000, 49417]$ every prime $p \equiv 1 \pmod 8$ has an explicit contraction except $29$ primes, all $\equiv 9 \pmod{16}$ and listed in \file{research/audits/reviews/2026-11-04-rees-threshold-5/gap_k8_unresolved.txt}, which are undecided. Four of the others, $22921$, $25321$, $26681$ and $26713$, are covered only by contractions with a zero entry (\file{research/audits/reviews/2026-11-04-rees-threshold-5.md}, Section~5; finite computation, AI-checked, pending human review). In $(11393, 20000]$ only some primes are decided. Hence $E_2(8) \subseteq [3, 20000] \cup X_{29} \cup (8^8/2, T_A(8)]$, where $X_{29}$ is that list of $29$ primes, and the last interval ends a factor of about $14$ below $T_A(8) \approx 1.17\cdot10^{8}$.
```

When the T1 sweep of (8^8/2, ⌈T_A(8)⌉] passes its acceptance test (`t1-sweep-hi.md` §6),
the last interval can be dropped.

### I3 (Imprecision). In `rem:is-runtime`, the "+b⁴" term does not follow from the zero-sum count the remark displays

*Where.* Main 608. The remark says the zero sum "uses $O(\kappa^3 b^2\log\kappa + \kappa^2
b^3\log\kappa)$ field operations". It later says "and $O\bigl(M_d b^2(g_d^2+b)+b^4\bigr)$ when
$\nu$ is bounded; the term $b^4$ is the zero sum".

*Why.* For fixed κ, the displayed count is b³ field operations. At O(b²) steps each, that
is b⁵, not b⁴. The b⁴ claim is correct only because the b³ term is really ν·b². The
derivation (`2026-11-04-rees-is-runtime.md` §4) gives R_z = O(κb) rounds and a selective root
extraction of O(κω(ν+ω)b) operations per round, and the TM report states Θ_κ(b²) operations
at bounded ν. The remark as printed does not let the reader see this.

*Fix.* Replace "uses $O(\kappa^3 b^2\log\kappa + \kappa^2 b^3\log\kappa)$ field operations,
independently of $a$ and of the columns" with:

```latex
uses $O(\kappa^3 b^2\log\kappa + \kappa^2\nu\, b^2\log\kappa)$ field operations, hence $O(\kappa^3 b^2\log\kappa + \kappa^2 b^3\log\kappa)$ since $\nu \le b-1$, independently of $a$ and of the columns
```

### I4 (Imprecision). `thm:power-sde`(ii) says "returns" for a procedure that may abort

*Where.* Main 633–638: "the two-level construction … returns a nonzero solution from
$M_d^{\mathrm{sym}}$ … arbitrary columns. Its classical cost is at most … for abort probability
$2^{-k}$."

*Why.* Theorem `app-s2-main` proves a different statement: the algorithm either aborts, with
probability at most 2^{−k}, or outputs a correct solution. The main statement reads as
deterministic success.

*Fix.* Replace item (ii) after the equation with:

```latex
  arbitrary columns, run with abort parameter $k \ge 1$, either aborts, with probability at most $2^{-k}$, or returns a nonzero solution, which is checked exactly before output and is never wrong. Its classical cost is at most $(1+\kappa^\kappa)\cdot\poly(a,\kappa,\log p,k)$.
```

The sentence before the equation then reads "… returns a nonzero solution from" → "… takes".

### I5 (Imprecision). The "Terms" paragraph describes U_κ and the sampler loosely

*Where.* Main 625: "a closed-form second-moment bound $U_\kappa(p)$, decreasing in $p$, on the
number of contractions as $\beta$ varies. … the sampler … finds one within the stated number of
draws."

*Why.* U_κ bounds R = E[n_j²]/E[n_j]², where n_j = |X_j(y)| is the number of admissible values
of α_j. It is not a bound on the number of contractions. The sampler succeeds with
probability at least 3/8 per round, not with certainty within a set number of draws.

*Fix.*

```latex
from a closed-form bound $U_\kappa(p)$, decreasing in $p$, on the normalised second moment $\mathbb{E}[n_j^2]/\mathbb{E}[n_j]^2$ of the number $n_j$ of admissible values of $\alpha_j$ when $\beta$ is uniform. For $p > T_A(\kappa)$ a contraction exists, and for $p > T_S(\kappa)$ each round of the sampler of Proposition~\ref{prop:app-s2-TA}(iii) finds one with probability at least $3/8$.
```

### I6 (Imprecision). `prop:decoupled-sde` defines E_2(κ) without p ≡ 1 (mod κ)

*Where.* Main 647: "Let $E_2(\kappa)$ be the set of primes at which no universal two-level
contraction of the decoupled form … exists."

*Why.* The appendix definition (line 157) and the Terms paragraph both restrict to
p ≡ 1 (mod κ). For other p, Q_0 = F_p^× and the definition is degenerate.

*Fix.*

```latex
Let $E_2(\kappa)$ be the set of primes $p \equiv 1 \pmod\kappa$ at which no universal two-level contraction of the decoupled form $C_{ij} = z_iz_j(\alpha_j + \beta_i)$ exists, equivalently (Lemma~\ref{lem:app-s2-normal}) no two-level contraction.
```

### I7 (Imprecision). The FEASIBLE verdicts of the unpruned runs have no stored witness

*Where.* Appendix 470, the decided ranges.

*Why.* `dfs2` checks a feasible witness internally but prints nothing for it. So for κ = 8
the five FEASIBLE primes ≤ 4201 (1553, 3089, 3121, 3361, 4177) and for κ = 9 the FEASIBLE
primes in [3584, 5689] rest on silence, read under the "later line" rule. The `dfs2b` re-run
of [9, 4201] was not kept. This does not make the verdicts wrong. But a reader cannot check
them from the repository, unlike the 69 `dfs2b` witnesses, which I re-checked.

*Fix (text).* Add after the provenance sentence of E1:

```latex
The unpruned search records no witness for a feasible prime; such a prime is one it passed without printing an infeasibility or node-limit line before a later line.
```

*Mechanical follow-up (no `.tex` change).* This is about a minute of CPU in
`small-prime/`:
`./dfs2b 8 9 4201 4000000000 print > dfs2b_k8_9_4201.out` and
`./dfs2b 9 10 5689 4000000000 print > dfs2b_k9_10_5689.out`.
Acceptance test: each file ends with a DONE line with `limit=0`, and every verdict agrees
with the old runs. Then the sentence above can be deleted.

### I8 (Imprecision, conditionality dropped). `rem:triangular-scope` uses part (ii) without saying it is conditional

*Where.* Main 676: "Since $p \ge 16\kappa^{2\kappa+2}$ implies $p \notin E_2(\kappa)$, it would
lower the Schedule~2 arity of the combined rule …".

*Why.* The implication is exactly Phase 0 of the proof of `thm:power-sde`(ii). That theorem
is labelled conditional, and the paragraph after it says it stays conditional until human
review. Here the implication is stated without that label.

*Fix.*

```latex
Since $p \ge 16\kappa^{2\kappa+2}$ implies $p \notin E_2(\kappa)$ by the proof of Theorem~\ref{thm:power-sde}(ii) (conditional; see the paragraph after that theorem), it would lower the Schedule~2 arity of the combined rule to $(g_d+1)(g_d+2)/2$ under the same guard;
```

### I9 (Imprecision, conditionality dropped). Main 650 omits the status labels that the appendix gives the κ = 8, 9 computations

*Where.* Main 650: "an exhaustive search … decides …" and "explicit contractions give
$E_2(8) \cap (49417, 8^8/2] = \emptyset$".

*Why.* The appendix labels both "finite computation, AI-checked, pending human review".
Main 650 opens with "This proposition comes from two AI-only passes", but those passes are
not the κ = 8, 9 computations. The scans and the witness sweep came later and are separate.

*Fix.* The drop-in of E1 (main 650) and I1 adds the label. With only the minimal E1 fix,
also add "(finite computation, AI-checked, pending human review)" after
"$E_2(8) \cap (49417, 8^8/2] = \emptyset$".

### G1 (Gap). The normalisation α_0 = 1 is used but never justified

*Where.*
- Appendix 184 justifies only β_0 = 0: "Translating $\alpha$ by $c$ and $\beta$ by $-c$ does
  not change $C$, so one may assume $\beta_0 = 0$."
- Appendix 426 then searches "over $(\alpha,\beta) \in \Fp^{2\kappa-2}$". That needs α_0 fixed
  as well.
- Main 659 (`prop:triangular-sde`) assumes "normalised by $\alpha_0=1$, $\beta_0=0$".
- The `dfs2b` problem statement uses the same normal form.

*Why.* α_0 = 1 needs the scaling step. With β_0 = 0, we have α_0 = C_00 ∈ Q_0 \ {0}, and
multiplying α and β by α_0^{−1} ∈ Q_0 preserves every coset condition. The proposition states
this as a hypothesis, but neither the main text nor the appendix shows that it is no loss.

*Fix (appendix 184).* After "so one may assume $\beta_0 = 0$." insert:

```latex
Then $\alpha_0 = \alpha_0 + \beta_0 \in Q_0$, and multiplying $\alpha$ and $\beta$ by $\alpha_0^{-1} \in Q_0$ preserves every condition $\alpha_j + \beta_i \in Q^\circ_{-(i+j)}$, because $Q_0Q_m = Q_m$; so one may also assume $\alpha_0 = 1$. This normal form is the one searched in Corollary~\ref{cor:app-s2-decoupled} and assumed in Proposition~\ref{prop:triangular-sde}.
```

*Fix (main 659).* "normalised by $\alpha_0=1$, $\beta_0=0$" →

```latex
normalised by $\alpha_0=1$, $\beta_0=0$ (by translation and by scaling with $\alpha_0^{-1}\in P$; Appendix~\ref{app:s2-contraction})
```

### G2 (Gap, minor). The proof of `prop:triangular-sde` applies cos to zero entries

*Where.* Main 667: "put $v=\sum_{i\in S}\beta_{\mathrm{cos}(\delta_i)}\delta_i\lambda_i$ … the
weights $x_i=\zeta\,\delta_i(\alpha_n+\beta_{\mathrm{cos}(\delta_i)})$".

*Why.* cos is defined only on F_p^×, but δ may have zero entries. The intended reading (skip
those terms and give them weight 0) is harmless, but it is not written. With it, the rest of
the proof is complete; see A.3.

*Fix.*

```latex
put $v=\sum_{i\in S,\ \delta_i\ne0}\beta_{\mathrm{cos}(\delta_i)}\delta_i\lambda_i$. For $\zeta\in\Fp^\times$ with $\mathrm{cos}(\zeta)=n$, the weights $x_i=\zeta\,\delta_i(\alpha_n+\beta_{\mathrm{cos}(\delta_i)})$ for $\delta_i\ne0$ and $x_i=0$ for $\delta_i=0$
```

### S1 (Style). Notation clashes

- `prop:triangular-sde` writes g, P, cos and Z_κ for what Schedule 2 and the appendix call
  ξ, Q_0, ind and Z/κ.
- P is also P = Π_d M_d at main 555.
- B_ℓ = κ^{ℓ(ℓ−1)/2}(a+1)^ℓ in `rem:is-runtime` clashes with the arity B_d(a).
- In Theorem `app-s2-main`, t is both the Bezout exponent (s_b = u_b^t) and the Phase-0
  scalar t.

*Fix (main 659).* "where $P=(\Fp^\times)^\kappa$ and the image of $g$ generates
$\Fp^\times/P$" →

```latex
where $P=Q_0=(\Fp^\times)^\kappa$ and $g$ is a coset generator (with $g=\xi$, $g^{\nu}P=Q_\nu$ and $\mathrm{cos}=\operatorname{ind}$ of Appendix~\ref{app:s2-gcd})
```

*Fix (main 608).* "where $B_\ell = \kappa^{\ell(\ell-1)/2}(a+1)^\ell$" →
"where $G_\ell = \kappa^{\ell(\ell-1)/2}(a+1)^\ell$", and "$G/B_\ell$ nodes" →
"$G/G_\ell$ nodes".

### S2 (Style). Status labels are not uniform

`prop:decoupled-sde` says "conditional, AI-checked only". The header of `thm:power-sde` says
only "part~(ii) conditional". Both are covered in the body. For uniformity:

```latex
\begin{proposition}[Decoupled two-level contraction; conditional; AI-checked, pending human review]
```

```latex
\begin{theorem}[Two-level symmetric SDE contraction; part~(ii) conditional, AI-checked, pending human review; proof in Appendix~\ref{app:schedule2}]
```

### S3 (Style). The Davenport constant is used without a source

*Where.* Main 639: "since the Davenport constant of $C_5^2$ is $9$".

*Fix (words only; no new bibliography key).*

```latex
since the Davenport constant of $C_5^2$ is $2\cdot 5-1 = 9$ (Olson's theorem for abelian $p$-groups)
```

---

## C. Citations (from memory; nothing opened online)

- **Lidl–Niederreiter, Thm 5.41** (appendix 194). From memory, Theorem 5.41 of *Finite
  Fields* (2nd ed.) is exactly the stated bound. Its hypotheses are ψ of order m > 1 and f
  monic of positive degree, not an m-th power, with d distinct roots in its splitting field.
  Its conclusion is |Σ_c ψ(a f(c))| ≤ (d−1)q^{1/2} for every a. The paper's hedge ("that
  number was not checked against the book") should stay until someone opens the book. The
  open item is not closed by this report.
- **Applications of the bound.** Both uses fit its form: X^s(X+1)^t with s, t ∈ [1, κ−1],
  two roots; and f_e with multiplicities in [1, κ−1]. The value χ(0) = 0 is consistent with
  LN's convention.
- **Not verifiable offline.** These citations need a human with the sources:
  - Martin–Yip, arXiv 2403.04312v2, Lemma 2.2.
  - Ivanyos–Santha, arXiv 1503.09016v2: Theorem 3, Theorem 11, Lemma 12, Propositions 9–10
    and §§3.1–3.3. Also the claim that v2 "is the accepted journal version", and the claim
    that the printed Theorem 3 bound does not follow from the proof.
  - van de Woestijne (ISSAC 2005), §6 and §6.1.
  - Ivanyos–Sanselme–Santha 2012, Claim 1.
  - Kothari–O'Donnell–Wu 2026, Thm 2.2 and Lemma 3.6.
  - Kothari–Metger–O'Donnell–Shutty–Wu 2026.
  - Göös–Kamath–Sotiraki–Zampetakis 2020, Def. 6.1 (`BIS_p`).
  - Benjamini–Gurel-Gurevich–Peled 2012, Prop. 26.
- **Rabin 1980.** The bibliographic data (SIAM J. Comput. 9(2), 273–280) match my memory.
  It is cited only as a generic source, which is appropriate.

## D. Claim discipline

The section and the appendix make no speedup, novelty or priority claim. Appendix line 85
says none of the statements "is claimed as new", and the scope list says "makes no priority
claim". "AI-checked, pending human review" or an equivalent label is present on:
- `rem:is-import`(e), `rem:is-runtime`, the Terms paragraph, the paragraph after
  `thm:power-sde`, `prop:triangular-sde`, `rem:combined-schedule` and
  `rem:two-level-threshold-size`;
- the appendix status line and every finite computation in the appendix scope list.

Main 650 is the exception for the κ = 8, 9 computations (findings I9 and E1).

## E. Top five

1. **E1.** The decided ranges for κ = 8, 9 are attributed to the pruned `dfs2b`. Below 4202
   (κ = 8) and 5690 (κ = 9) they come from the unpruned `dfs2` and earlier DFS runs, and
   dfs2-prune §2 does not cover κ = 9.
2. **I1.** All of the paper's E_2 numbers are supported, but stale. The scans now decide
   κ = 8 to 11393, with 11321 ∈ E_2(8) (0.97), and κ = 9 to 14293, with 17749 ∈ E_2(9)
   (0.30). They should be labelled as lower bounds from running scans.
3. **E2.** The Terms paragraph says every quoted E_2 value is exhaustive up to a proved
   threshold. That holds only for κ ≤ 7.
4. **I3.** In `rem:is-runtime`, the bounded-ν "+b⁴" does not follow from the displayed
   zero-sum count O(κ²b³ log κ). That count should read O(κ³b² log κ + κ²νb² log κ).
5. **G1.** The normalisation α_0 = 1, used by `cor:app-s2-decoupled`,
   `prop:triangular-sde` and `dfs2b`, is never justified. It needs one sentence (scaling by
   α_0^{−1} ∈ Q_0).

T_A(8): recomputed as 117441562.029, so the integrator's 117441563 = ⌈T_A(8)⌉ is correct as
the sweep endpoint. `t1-sweep-hi.md` writes "117441563 = T_A(8)" and should write ⌈T_A(8)⌉.

---

## Appendix: scripts used (scratchpad; reproduced here because the scratchpad is temporary)

The coverage check is summarised below. The full script parses every `dfs2b_k{K}_*.out` and
`dfs2_k{K}*.out` with the regex `(FEASIBLE|INFEASIBLE|LIMIT) k=(\d+) p=(\d+)`. For old
non-rerun `dfs2` chunks it adds FEASIBLE for each unprinted prime p ≡ 1 (mod K) in
[chunk start, last printed p]. The chunk starts are 2442 and 3584 for the round-1 files and
the file name otherwise. It then reports:
- conflicts: primes with more than one verdict other than LIMIT;
- the first prime from the start that has no unique verdict;
- the largest INFEASIBLE prime.

```python
# witness check (all FEASIBLE lines of dfs2b_k*.out)
h=(p-1)//K; z=pow(g,h,p)            # require exact order K
for i in range(K):
  for j in range(K):
    v=(al[j]+be[i])%p
    if v==0: assert (i,j)!=(0,0); continue
    assert pow(v,h,p)==pow(z,(-(i+j))%K,p)
```

The T_A computation bisects U_κ(p) against κ/(κ−1) and 1 + 1/(8κ) in mpmath at 50 digits.
U_κ and E_max are implemented exactly as in appendix lines 367–376.

---

## Applied (11-04)

Applied by an integration subagent (Claude Code), local only. Files edited:
`docs/papers/rees-hsp/main.tex` and `docs/papers/rees-hsp/appendix-schedule2.tex`
(backups in the session scratchpad, `bak-i182/`). Build: 144 pages, 0 Overfull, no
"Float too large", no undefined references. `tests/tools/test_rees_paper_numbers.py`: 2 passed.
Every "AI-checked, pending human review" label kept (main 44 → 47, appendix 3 → 5).

**E_2 numbers, recomputed at 19:39 AEDT.** The method is A.1's, except that above 4202 (κ = 8)
and 5690 (κ = 9) a prime counts as decided only if some `*k{K}*.out` file prints a FEASIBLE or
INFEASIBLE line for it (no "later line" rule). No conflicts. The scans have moved on since
the report:
- κ = 8: decided contiguously to **11489** (first undecided 11497), with **11489 ∈ E_2(8)**,
  and 11489/8^{4.5} = 0.99169, so the factor is **0.99**.
- κ = 9: decided contiguously to **14347** (first undecided 14401). The largest INFEASIBLE
  anywhere is **17839** (`dfs2b_k9_17501_20000.out`), and 17839/9^5 = 0.30211, so the factor
  is **0.30**.
Both are written as lower bounds from scans still running on 2026-11-04.

**Rerun (I7 follow-up), done.** One process at a time, under `nice -n 10`, written in `small-prime/`:
- `./dfs2b 8 9 4201 4000000000 print` → `dfs2b_k8_rerun_low.out`: 31 s, `DONE … feasible=5
  infeasible=132 limit=0`.
- `./dfs2b 9 10 5689 4000000000 print` → `dfs2b_k9_rerun_low.out`: 29 s, `DONE … feasible=4
  infeasible=118 limit=0`.

All 137 and 122 verdicts agree with the old ones, which are: §3 of small-prime-arity (82 of 83
infeasible, 1553 or 3529 feasible); `dfs2_k8.out`, `dfs2_k8_4058_6000.out` and
`dfs2_k9.out` under the "later line" rule; and the six κ = 8 LIMIT reruns. The feasible primes
are 1553, 3089, 3121, 3361 and 4177 (κ = 8), and 3529, 4177, 5077 and 5527 (κ = 9). A separately
written checker accepts all 9 stored witnesses. It uses the same checks as the snippet in this
report's appendix: p is prime, g^h has exact order κ, every cell is in its coset, and (0,0) is nonzero.

| Finding | Status |
|---|---|
| E1 | **Modified.** Main 650 now reads "exhaustive searches (finite computations, AI-checked, pending human review; Section~\ref{app:s2-scope}) decide". In the appendix, "proved prunes" became "prunes", and the paragraph gives the provenance as the drop-in does. Because the rerun completed, the text also says that one pruned run per κ reproduces all the old verdicts below 4202 and 5690 and stores witnesses, so "each verdict in the decided ranges is a single run of the pruned search" is now true. The "(AI-checked, pending human review)" label on the prunes is kept. |
| E2 | Applied (Terms paragraph). |
| I1 | **Modified.** Recomputed numbers: 11489, 11489 ∈ E_2(8) and 0.99; 14347, 17839 ∈ E_2(9) and 0.30. In main 650 the clause now ends with a full stop, and "For $\kappa \ge 10$ …" starts a new sentence. |
| I2 | **Modified.** The original sentence "That range ends a factor of about 14 below T_A(8)" is kept, because the drop-in's "the last interval ends a factor of about 14 below T_A(8)" is wrong: that interval ends at T_A(8). The band sentences, the four zero-cell primes and E_2(8) ⊆ [3,20000] ∪ X_29 ∪ (8^8/2, T_A(8)] are added, with (11489, 20000]. Nothing new is said about (8^8/2, T_A(8)]. |
| I3 | Applied. §4 of `2026-11-04-rees-is-runtime.md` gives R_z = O(κb) rounds of O(κ²b log κ) (runs) + O(κω(ν+ω)b) (SRE). So Z = O(κ³b² log κ + κ²νb² log κ). At bounded ν that is Θ_κ(b²) field operations, or O(b⁴) TM steps, which matches `-tm.md` §0 and the remark's "+b⁴". The bounded-ν clause is unchanged. |
| I4 | **Modified.** Rewritten as "takes [eq] arbitrary columns and an abort parameter $k\ge1$. It either aborts … or returns a nonzero solution, which is checked exactly before output and is never wrong. Its classical cost …". The drop-in's sentence was not grammatical. |
| I5 | Applied, adding "with $\beta_0 = 0$" to match the appendix's y ∈ {0}×F_p^{κ−1}. |
| I6 | Applied. |
| I7 | **Modified.** The rerun was done (above), so the "records no witness" caveat now describes the old dfs2 runs, and the stored witnesses are cited. |
| I8 | Applied. |
| I9 | Applied, through the E1/I1 text in main 650. |
| G1 | Applied (appendix 184 and main 659). |
| G2 | Applied. |
| S1 | **Partly applied.** Main 659 now reads P = Q_0, g = ξ, cos = ind. In `rem:is-runtime`, B_ℓ → G_ℓ. **Skipped:** the clash of t (Bezout exponent against the Phase-0 scalar) in Theorem `app-s2-main`, which has no drop-in and would mean renaming the symbol throughout the proof. |
| S2 | Applied (both headers). |
| S3 | Applied. |

Not touched: `appendix-torsion-blackbox.tex`, `thm:bb-envelope`, `rees_hsp_reduction.json`,
`docs/outreach/`, `make_numbers.py`. Still open: `docs/papers/rees-hsp/README.md` line 9
quotes the old values 11161, 13807 and 17713. It is outside this pass's files.

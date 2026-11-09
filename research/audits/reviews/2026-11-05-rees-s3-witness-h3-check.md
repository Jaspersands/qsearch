# Check of the Schedule 3 witness sampler at h ≥ 3 (2026-11-05)

**Status: AI-checked, pending human review.** Overnight AI-only pass, no owner input. Object:
`2026-11-05-rees-s3-witness-h3.md` (Parts A–G, F1/F2) and its folder. Independent code and
outputs: `2026-11-05-rees-s3-witness-h3-check/` (`hcheck.py`, `test_hcheck.py`; `sp.json`,
`depth.json`, `solver.json`, `node.json`, `scaled.json`, `neg.json`, `exponent.json`,
`budget.json`, `mitm.json` and logs; `integrated_remark.tex` is the text as inserted). I wrote
the code from the report's statements without reading the report's code. Nothing committed; no
git, no network; claim gates untouched; `make_numbers.py` not run.

## Verdict

- **Theorem H, H′, Lemma 0, Lemma J (i)–(iv), Cor. H.6, Cor. H.7, B0, B5_h (as a model
  statement), the lattice form: no Error.** One Gap and several Imprecisions, fixed in the
  inserted text (§5).
- **Strong claim (i), "the open question after prop:rc-lower is answered negatively as
  stated": does not survive as a negative answer (Error of framing).** The first-moment bound
  is correct, but it shows only that the question is vacuous where it applies
  (h < κ^{o(a)}). The report itself concedes that it says nothing where the question has content
  (h ≥ κ^{Ω(a)}). Its replacement question (F2) is partly answered by a standard collision
  search (§3). **F2 was not applied**; main.tex's question is unchanged (owner decision, §6).
- **Strong claim (ii), polynomial classical time at fixed c for every p > c, exponent ≤ 19 at
  c = 9: survives, with exact scope** (§4). It is stated once, in main.tex after
  thm:free-coordinate, where the cost of (iii) is discussed. Its proof is
  `rem:fc-witness-h3`(c). It is not phrased as a speedup and not compared with 143.
- Integrated as `rem:fc-witness-h3` (Remark C.10, p. 118 of the scratch build) after
  `rem:fc-zero-sum-arity`. Builds clean; numbers test passes (§7).

## 1. What the objects are

- Grade d ∈ Γ_F: κ = gcd(d, p−1), 2 ≤ κ < p−1, h = (p−1)/κ ≥ 2, D = P_κ ∪ {0} = μ_h ∪ {0},
  q = (h+1)/p. Bank: labels i.i.d. uniform on K_d^⊥ of unknown dimension a = a_d ≤ g_d
  (`lem:fc-forest`(a)). A witness is y ∈ D^M \ {0} with Σ y_i λ_i = 0; (F4) converts it to s with
  s_i^d = y_i via σ^κ = y, s = σ^α.
- "Arity" in the paper is the number of labels (registers) a node consumes, M_d. All
  computations inside a node are classical on the saved bank. The "classical time" of
  thm:free-coordinate(iii) is the time of these computations, 2^{O(max g_d log κ_d)}·poly
  (prop:fc-uniform(b)). The quantum part (sources, instruments, conversions) is already
  polynomial in the query count c S ∏ M_d.

## 2. Theorem H re-derived

- **Input law at every level.** A call 𝒜_j(d, y) reads coordinates 1..d of fresh columns, and its
  stopping rule depends only on them (P1).
  - Every sub-call starts at a stopping time of the stream. By the strong Markov property its
    columns are i.i.d. uniform and independent of the past.
  - Condition on coordinates 1..d−1 of a switch block. Then (I_k, α_k, C_k) is fixed, and
    α_k ≠ 0, because the base kernel vector is nonzero and at d−1 = 0 the weight is 1. Coordinate
    d is still i.i.d. uniform, so β_k = Σ α_{k,i} v_{i,d} is uniform and independent of everything
    before. This is exactly what the covering loop and Wald's identity need.
  - The recursion's target depends on the past, but its columns are fresh, and its read count
    does not depend on its target (P3).
  - Level j* is reached only through switches, with target 0.
- **Correctness.** Σ_k x'_k v + Σ_{k∈T_a} α_k v = u + a e_d on coordinates 1..d, so the output sum
  is y. The weights lie in D_j by the tables and by induction. The output is nonempty, because
  the recursion's output is nonempty and disjoint from the switch blocks.
- **Exact degree.** N_{j*}(d) = d+1 and N_j(d) = 1 + s Σ_{e<d} N_{j+1}(e) give
  N_{j*−k}(d) = s^k d^{k+1}/(k+1)! + O(d^k). So the degree is exactly 1 + j*_h, with leading
  coefficient s_p^{j*}/(1+j*)!.
  - [computed] N_1(d) = 1 + 3d(d+1)/2 at s = 3.
  - [computed] Slopes of log N_0 between n = 256 and 512 are 1.997 (j* = 1) and 3.000 (j* = 2).
    The leading-coefficient ratio is 1.002 and 1.000.
- **Theorem H′.** At dimension n′, each of the K = ⌈log₂p⌉ switches costs n′·p/(p−1) columns in
  expectation (β = 0 has probability 1/p, because β is uniform given the first n′−1
  coordinates). So E R = 1 + K (p/(p−1)) n(n+1)/2, exactly. The binary digits of a ∈ [0, p) work
  because 2^K > p−1. The split cap gives a failure of at most 2^{−B}/M per entry (Lemma J(ii)),
  hence at most 2^{−B} over at most M entries.
- **Lemma 0.** |D_j| ≥ min(p, 2^j h + 1) and j*_h ≤ ⌈log₂κ⌉ follow from Cauchy–Davenport.
- **Lemma J(ii) (Weil range).** N(y) = Σ_{χ,ψ} Σ_b χ(b)ψ(b−y), and the both-nontrivial terms
  are χψ(y)ψ(−1)J(χ,ψ).
  - Of the (κ−1)² such pairs, κ−1 have |J| = 1 and (κ−1)(κ−2) have |J| = √p. This gives
    |N(y) − p| ≤ (κ−1)(κ−2)√p + κ−1.
  - At most 2κ points have x = 0 or z = 0, and the rest map κ²-to-1 onto pairs in μ_h².
  - Positivity uses 3κ² − 12κ + 16 = 3(κ−2)² + 4 > 0. The 1/(2κ) step uses
    4κ² − 15κ + 17.5 > 0.
  - All re-derived; the Jacobi-sum values are from memory (NEEDS HUMAN VERIFICATION).
- **Lemma J(iii)/(iv).** D_j ⊆ S_{2^j}. With one scalar per level, E_j ⊆ Γ_j D_j. The ℓ₁ count
  gives the lower bound. For the upper bound: a Minkowski vector v ∈ 𝔭 has ‖v‖_∞ ≤ p^{1/φ};
  the basis ζ^t v has ℓ₁-norms ≤ c_h‖v‖₁; rounding gives ρ = c_hφ²p^{1/φ}/2; D_j ⊇ S_{2^{j−1}}
  (S_{2^j} for even h). All correct.
- **Cor. H.6 / H.7.**
  - The span event is bounded by `lem:s3-moment`(d).
  - Markov on L = ⌈2N̄_0(g)⌉ ≥ 2E R, using monotonicity in the dimension.
  - The output is ρ_{H_{d−1}} as for the zero-sum node. The witness reads only the node's own
    bank, which no later step reads.
  - The abort bound τ_d + 3·2^{−B} enters `lem:fc-forest`(b), with |Γ_F ∪ Γ_0| ≤ c−1. All
    checked.

## 3. Strong claim (i): the "arity a + O(1)" question

- **What the paper says** (main.tex, paragraph after prop:rc-lower): "Whether some method finds
  a witness in time κ^{a−Ω(a)} at arity a + O(1) is open." Here a = a_d, arity is the number of
  labels, and "finds" means returns a checked witness with constant probability on the i.i.d.
  bank. The baseline is the FCS / prop:rc-lower cost of about q^{−a} ≈ κ^a trials.
- **The counting bound (B0) is right and trivial.** It is a union bound over the
  (h+1)^M − 1 nonzero y, each with Pr[Xy = 0] = p^{−a}. At arity a + k a witness exists with
  probability at most (h+1)^k q^a. Since q^{−a} ≥ (κe^{−1/h})^a ≥ κ^{0.27a}, a witness exists with
  constant probability at arity a + O(1) only if h ≥ κ^{Ω(a)}.
- **Why this is not a negative answer.** For h < κ^{o(a)} *no* method succeeds at arity
  a + O(1), the FCS included (its arity is g + g log(1/q)/log h + …, not a + O(1)). The
  question is therefore vacuous there, and "no" is the trivial answer to a question that was
  never posed in that range. Where witnesses exist (h ≥ κ^{Ω(a)}, that is p ≥ κ^{Ω(a)}), B0 is
  silent, as the report concedes (B0, "says nothing"). So the question is not answered, and the
  summary's "negative answer as literally stated" is an overstatement. What survives is an
  **Imprecision in main.tex**: the question should name its range.
- **F2 contains an Error.** F2 re-poses the question at arity O(a log p/log(h+1)) and calls it
  open. A collision (meet-in-the-middle) search answers it positively whenever h ≤ κ^{1−δ}:
  1. Take M = ⌈a log_{h+1}p + log_{h+1}(2h)⌉ + O(1), within O(1) of the existence threshold.
  2. Split the bank into halves. Tabulate the (h+1)^{M/2} D-combinations of one half, and look up
     the negatives of the other half's (D is not symmetric for odd h, so the lookup uses −Σ).
  3. This finds *every* witness. Its time is Õ((h+1)^{M/2}) = Õ(poly(h)·p^{a/2}).
  4. Witnesses y, y′ that are linearly independent give independent events. Proportional ones
     are y′ = ty with t ∈ μ_h, as in `lem:fc-moment`. So Var Z ≤ h E Z, and a witness exists
     with probability ≥ 1/2 once (h+1)^M ≥ 2h p^a.
  5. p^{a/2} = (κh+1)^{a/2} ≤ κ^{a(1−δ/2)+o(a)} for h ≤ κ^{1−δ}, and Wagner-type merging extends
     this to h ≤ κ^{O(1)}. In particular every fixed h, including the paper's h = 3 grades, is
     covered as κ → ∞.

  [computed, `mitm.json`] At (h, p, a) ∈ {(3,31,3), (3,31,4), (3,61,3), (4,41,3)}, with M within
  3–4 of the threshold, the search found an exactly checked witness on 30/30 banks each. The
  sizes are too small to show the asymptotic gap; the argument above is the proof. So F2's
  "open" is wrong, and F2 also says "time polynomial in its arity", which needs H′ for large p.
- **Decision.** (i) does not survive, so F2 is not applied and main.tex's question is unchanged.
  The remark's part (d) states only the true first-moment fact: a witness at arity a_d + O(1)
  exists with probability bounded below only if h ≥ κ^{Ω(a_d)}. It does not reinterpret the
  question.

## 4. Strong claim (ii): polynomial classical time at fixed c

- **Which time.** The time is the classical computation inside the nodes, the quantity that
  thm:free-coordinate(iii) bounds by 2^{O(max g log κ)}·poly. The whole Schedule 3 run (lifted
  sources, instruments, conversions, Fourier sampling) is quantum. Its quantum cost is
  polynomial in the query count c S ∏ M_d, and that count is polynomial at fixed c with either
  node. So "polynomial classical time" means that the witness finding, plus the echelon form,
  root extraction and conversion, takes poly(m, log p, log 1/ε) bit operations. The whole run
  is then polynomial at fixed c. Theorem main (Schedule 1) is already polynomial at fixed c, so
  this is a statement about a Schedule 3 variant only.
- **Every p > c.** The cases:
  - Γ_1: the linear node.
  - Γ_0 (only p = c+1): the node of rem:fc-zero-sum-arity(b), with time poly(M_d, p) and p ≤ c+1.
  - Γ_F with √p ≥ 2(κ−1)(κ−2)+4: H′, with time poly(n, κ, log p), no table and the exact count.
  - Γ_F otherwise: tables and the covering loop, with p < (2c²)², so p² = poly(c).

  So for fixed c every node is poly(m, log p, log 1/ε), with log(1/τ_d) = O_c(log(m/ε) +
  log log p).
  - **Gap (fixed):** Cor. H.6 and F1(b) did not say that the node *must* use H′ at large p. The
    covering loop costs Θ(p) per switch, which is exponential in log p. F1 only said "may be
    rescaled". The inserted (b) now fixes the rule: rescaled form iff √p ≥ 2(κ−1)(κ−2)+4.
- **Exponent.** E(c) = max_{p>c} [1 + Σ_d (1 + j_d)], counting g_d ≤ m and S ~ m, and ignoring
  the (log p)^{Σj_d}, log(1/τ_d) and log(1/ε) factors.
  - Beyond max_{κ≤c}((κ−1)(κ−2)+3)², every Γ_F grade has j = 1 and Γ_0 = ∅, so E ≤ 2c−1.
  - Below that bound I scanned every prime (`exponent.json`). E = 3, 6, 8, 10, 13, 14, 16,
    **19 (p = 19)**, 21, 22, 25 for c = 2..12, identical to the report.
  - Hand check at p = 19, c = 9:

    | d | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
    |---|---|---|---|---|---|---|---|---|
    | κ_d | 2 | 3 | 2 | 1 | 6 | 1 | 2 | 9 |
    | j_d | 1 | 1 | 1 | 0 | 2 | 0 | 1 | 4 (j*_2 = ⌈log₂9⌉) |

    This gives 1 + 2+2+2+1+3+1+2+5 = 19.
  - Spot check beyond the c = 9 bound (p = 3491, 3499, 4001, 5003): every Γ_F grade has j* = 1.
- **Imprecision in the report (not in the paper):** the "Schedule 1 at κ_d (reference)" row
  maximizes only over the scanned primes. For example, at c = 8 the true max over p > c is
  E_1(8) = 109, attained at p = 2521 (840 | 2520), not 95. The rows for c = 11 and 12 are
  similarly low. That row is not used in the paper.
- **Relation to E_W, 143, tab:fcs-budget, tab:main-regimes.**
  - E_W(c) is the same kind of exponent (exponent of m in the query count, max over p > c). It
    bounds a worst-case rule that never aborts and uses no label law, inside the black-box
    envelope.
  - E(c) bounds an average-case procedure with aborts, on the i.i.d. supply only. Together with
    the FCS (exponent of about c, exponential classical time) it shows a trade-off between
    queries and classical time.
  - At the class-nine profile with the arities of Cor. H.6 as stated (`budget.json`), log₂Q is
    103.5, 93.0, 119.9, 127.1, 150.8 and 142.0 at p = 11, 1031, 5281, 2^31−1, 2^61−1 and
    2^127−1. The FCS values of (iii) are 42.3, 36.6, 39.1, 35.9, 34.1 and 34.0.
  - The paper says neither "speedup" nor "beats 143"; 143 is not mentioned. The remark says
    that E is not compared with E_W(c).
- **Conclusion.** (ii) survives: conditional exactly as (iii) is, for the i.i.d. supply, with
  aborts and success ≥ 1 − ε. Not adopted in (R1).

## 5. Gaps and Imprecisions fixed in the inserted text

1. **Gap.** The rescaled form is mandatory where √p ≥ 2(κ−1)(κ−2)+4, and the tables are used
   otherwise (and then cost poly(κ)). Without this rule the time claim fails at large p.
2. **Imprecision.** B5_h's model is "one scalar per level". H′'s per-switch scalars are harmless
   only because D_1 = F_p. The remark now says that hierarchies with a separate scalar per
   switch are not covered.
3. **Imprecision.** F1(c) compared E with 143. It now says only that E is not compared with
   E_W(c), and why.
4. **Imprecision.** "3 capped steps" are now named: root extractions, field draws and splitting
   searches.
5. **Imprecision.** F1 cited only the report's own adversarial pass. This check is now cited too,
   and the remark says that only the main.tex sentence uses it.
6. **Imprecision.** The split cap needs "at most M entries" for the 2^{−B} union bound; now
   stated.
7. **Note (comment line).** σ̄_p uses the bound σ_p ≤ ⌈2log₂(p−1)⌉+4, imported in
   rem:fc-zero-sum-arity. In the tables case σ_p ≤ p (proved) suffices, since p is bounded
   there, and the rescaled case uses the exact count. So (ii) does not depend on the import.

## 6. Owner decisions (nothing changed)

- **OD1 (main.tex question).** Optionally scope the sentence after prop:rc-lower. Suggested text
  (not applied): "For independent uniform labels a witness exists at arity a + O(1) with
  probability bounded below only if h ≥ κ^{Ω(a)} (Remark rem:fc-witness-h3(d)); whether some
  method then finds one in time κ^{a−Ω(a)} is open."
- **OD2 (adopt the node).** Optionally add the node as a public option at Γ_F in (R1). That
  would change the time statement of thm:free-coordinate(iii), prop:fc-uniform(b) and the core's
  Schedule 3 sentence (polynomial classical time at fixed c). It could add a column to
  tab:fcs-budget (log₂Q 93.0–150.8 at the six rows, computed here once) and a note in the
  "Random column, free coordinates" row of tab:main-regimes. E_W(c) and numbers.tex would be
  unchanged, since neither concerns Schedule 3.

## 7. Computations (all exact output checks; `nice -n 10`, one or two processes)

- **s_p.** Exact by DP over subset-sum sets (`sp.json`):
  - 65/16 (p = 5), 1127/243 (7), 4154499115/725594112 (13) and 434896500819017/2^46 (17); the
    report's values for 7, 13 and 17 are reproduced.
  - New exact values at 19 (6.363022) and 31 (7.198781). The report's Monte Carlo values were
    6.364 and 7.197.
- **Depth.** `depth.json`:
  - Bitset and FFT agree on 623 cases.
  - Lemma 0, the ⌈log₂κ⌉ bound, Lemma J(iii)/(iv) and the Weil range hold for every prime
    p ≡ 1 (mod h): below 2·10⁴ for h = 3, 4, 6 and below 8000 for h = 5, 8, 12.
  - The Jacobi pair count holds for every y ≠ 0 in 1325 cases (κ ≤ 8, p < 3000), including the
    1/(2κ) step.
  - j*_3 = 1, 1, 2, 2 at p = 7, 13, 19, 31, and j*_4 = 1, 2 at p = 13, 17. The first primes
    with j*_3 = 1..7 are 7, 19, 61, 151, 523, 1879, 7207, as in the report.
  - j*_3 − ½log₂p ∈ [−0.85, 0.59] (1124 primes below 2·10⁴).
  - c_h = 2, 1, 4, 2, 1, 2 for h = 3, 4, 5, 6, 8, 12.
- **Solver.** `solver.json`, with random tables:
  - 21 rows at h = 3 (p = 7, 13, 19, 31) and h = 4 (p = 5, 13, 17). Every output was exact.
    Mean reads against the exact N_0 have max |z| = 2.23.
  - Inhomogeneous targets at every level j < j*: all exact.
- **Node.** `node.json`: 48 rows, 1560 trials over (p, d) = (7,2), (13,4), (13,8), (19,6),
  (31,10), (13,3), (13,9), (17,4). There were 0 wrong outputs and 1 abort (a span failure), and
  the maximum abort rate at τ = 1/20 was 1/40. Every witness was converted at the actual d and
  checked as Σ s_i^d λ_i = 0.
- **Rescaled form.** `scaled.json`: (κ, p) = (3, 2^31−1), (6, 2^61−1), (4, 101), (3, 13).
  - Every output was exact; the conversion was checked with sympy `nthroot_mod`.
  - The mean reads equal 1 + K p/(p−1) n(n+1)/2: 311 and 1117 at 2^31−1, 611 and 1282 at
    2^61−1.
  - Split trials averaged 2.97–2.99 (κ = 3) and 6.08–6.24 (κ = 6).
- **Negative controls.** `neg.json`:
  - A broken table entry (x − x′ ≠ α) was caught by the exact check in 40/40 runs.
  - With depth j* − 1 at (3, 19), all 30/30 runs were bad.
  - Biased {0,1} columns: z = 46.9 against N_0, outputs still exact.
  - The hyperplane bank (coordinate g = coordinate 1): 30/30 aborts, 0 wrong.
- **Tests.** `test_hcheck.py`: 20 passed.
- **Builds.** Scratch copies under $TMPDIR, `latexmk -g -pdf`:
  - Full: exit 0, 175 pp., 0 Overfull, no undefined refs or cites, no Float too large.
  - Core: exit 0, 28 pp., same checks clean.
  - `tests/tools/test_rees_paper_numbers.py`: 2 passed.

## 8. Edits made

- `appendix-free-coordinate.tex`:
  - new `rem:fc-witness-h3` after `rem:fc-zero-sum-arity`, before `app:fc-uniform`;
  - Scope paragraph: "block splitting" → "block splitting, and Remark rem:fc-witness-h3 another".
- `main.tex`: one sentence after "Table fcs-budget gives the resulting counts … 2^{33.8} classical
  trials per node." (statement (ii), exact scope, not adopted).
- `core/main-core.tex`: one sentence after the FCS classical-cost sentence of the Schedule 3
  paragraph (states Schedule 3 cost, so it is updated consistently; no numbers).
- `research/REES_FULL_CONTINUATION.md` item 4; integration log row I221.
- No bib, numbers.tex, table, E_W, claim-gate, handoff or STATE change. The report's mechanical
  items M1 (rerun depth/exponent and diff) and M2 (E_2(6) at p = 19, 31) are not moved to
  `MECHANICAL_FOLLOW_UP_PLAN.md`; this pass's brief did not include that file. M1 is in effect
  done here by independent code.
- Backups: the session scratchpad, `backups/`.

## 9. Claim gates that must stay false

These stay false: all Rees gates, "polynomial-time Schedule 3" (c growing; the query count is
≥ 2^{c−1}), "hardness of the witness problem", "o(a²) SDE solver", and any novelty or speedup
claim.

**Next hard question.** Is there a method with degree bounded uniformly in p for fixed h ≥ 3, or
a proof that every switch hierarchy of depth J reads n^{1+J−o(1)} columns? Also: is the
paper's question at arity a + O(1), for h ≥ κ^{Ω(a)}, open or easy?

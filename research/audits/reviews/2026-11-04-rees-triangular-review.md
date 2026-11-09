# Referee report: Proposition `prop:triangular-sde` (Triangular two-level solver)

Date: 2026-11-04. Adversarial AI referee pass; finite computations, AI-checked, pending human review.
Target: `docs/papers/rees-hsp/main.tex`, Proposition `prop:triangular-sde` (label at line 666 when
checked; proof lines 674–680; main.tex was being edited at the same time and moved by +3 lines
during this pass, but the proposition's text did not change), read with `prop:decoupled-sde`,
`eq:sde-target`, `E_2(κ)`, and `app:s2-gcd` / `app:s2-contraction` / `lem:app-s2-normal` in
`appendix-schedule2.tex`. I formed my view before reading the source,
`research/audits/reviews/2026-11-02-rees-linear-arity.md` §2. The proof there matches the paper's
proof step for step. Its statement says `x ∈ P^M`, which the paper correctly writes as
`(P∪{0})^M`.

Artifacts (all in `research/audits/reviews/2026-11-04-rees-triangular-review/`):
`tri.py` (the solver exactly as written, plus our own contraction search, families, exhaustive and
tightness runs), `tri_results.json`, `tri_full.log`, `summarize.py`, `ew_tri.py` (E_W preview),
`fcs_tri.py` (tab:fcs-budget preview). Run with `nice -n 10 /opt/anaconda3/bin/python tri.py --jobs 2`
(351 s).

## Verdict

**TRUE with gaps.** The proposition is true as stated. The proof's mathematics is correct and
complete: the realisation identity, the round structure, the column count, the back substitution,
disjointness, nonzeroness and the coset signs all check. There is no Error. The cost and
determinism claims (O(a) eliminations, O(a²) power evaluations, "deterministically") appear in the
statement but are never argued in the proof (Finding 1). The final summation step is left implicit
(Finding 2). Both need one sentence each. Everything else is an Imprecision. No test, out of
178,080 randomized and adversarial runs and 603,397 exhaustive tuples, failed.

## Findings

**1. Gap: the cost and determinism claims are not proved.** The statement claims O(a) Gaussian
eliminations, O(a²) evaluations of y ↦ y^{(p−1)/κ}, and a deterministic output. The proof says
nothing about cost. The claims are true. Each round does one elimination for δ (an a×(a+1) system:
a−k+1 block columns plus the k basis vectors of U_k) and one membership test v_{k+1} ∈ U_k. The back
substitution does one coordinate solve per l ≤ k ≤ a. That is at most 3(a+1) eliminations; we
observed at most 3a+2. Coset tests are needed for the at most M nonzero δ_i and the at most a values
ζ_l, so at most M + a; we observed exactly M + a as the maximum. Determinism needs δ chosen by a
fixed rule. *Fix:* add at the end of the proof: "Each round uses one elimination for δ and one
for the test v_{k+1} ∈ U_k, and the back substitution one coordinate solve per round, so at most
3(a+1) eliminations, each of size a×(a+1) at most; coset tests are made for the at most M nonzero
δ_i and the at most a values ζ_l. With δ chosen by a fixed rule (for instance the first dependency
in reduced echelon form) the procedure is deterministic given g and (α,β)."

**2. Gap (minor): the closing identity is implicit.** After "Finally τ ∈ U_0 = 0" the proof goes
straight to "the weights sum to a nonzero solution". The missing line is that each update
subtracts the value of the weights just added, so the final τ is −(R + Σ_l ζ_l(α_{cos ζ_l}e_l + v_l)),
which is minus the total value; τ = 0 then gives Σ x_iλ_i = 0. *Fix:* replace "Finally
τ∈U_0=0." with "Each update subtracts the value of the weights added, so at the end τ equals minus
the value of all the weights; and τ ∈ U_0 = 0."

**3. Imprecision: R stands for two things.** "Let R be the realisation with ζ=1; it lies in U_k
and has the weight … 1 on one column" uses R both for a weight vector and for a vector of F_p^a.
"Put τ = −R" needs the value. *Fix:* "let R be the realisation with ζ=1 and ρ = Σ_i R_iλ_i = e_{k+1} +
v_{k+1} ∈ U_k its value … Put τ = −ρ."

**4. Imprecision: the dimension invariant is implicit.** The count Σ_{k=0}^{a}(a−k+1) uses
dim U_k = k (from v_{k+1} ∉ U_k) and the forced stop in round a. Edge cases check out:
- a = 0: M = 1, x = (1).
- a = 1: M = 3; exhaustive at p = 3, 5, 7 (κ=2), p = 7, 13 (κ=3) and p = 41 (κ=4).

The proposition does allow a = 0, which happens when a_d = 0. The appendix assumes a ≥ 1, and
"O(a)" should read O(a+1) there. *Fix:* "Since v_{k+1} ∉ U_k, dim U_k = k, so round k takes
a−k+1 columns, and round a, if reached, takes one column and stops."

**5. Imprecision, not an error: more normalisation than needed.** The proof uses only
α_0 + β_0 ∈ P, for the weight on the normalised column. β_0 = 0 is used only in the parenthetical
about U_k = F_p^a, where v ∈ U_k holds anyway. The normalisation is correctly justified by
translation and scaling in app:s2-contraction. It should stay, because
Lemma `lem:coherent-power-sde` uses β_0 = 0 (its "entry at j* is β_0·1 = 0" step). No change
needed. At most, add a footnote.

**6. Correct: coset bookkeeping (check c).** ζδ_i ∈ g^{n+cos δ_i}P, and α_n + β_{cos δ_i} ∈
g^{−(n+cos δ_i)}P∪{0}. This is Lemma `lem:app-s2-normal` with row index i = cos δ_i (β) and column
index j = n = cos ζ (α). The condition set {α_j + β_i ∈ Q°_{−(i+j)} ∀ i,j} is the one in that
lemma, and the realisation value ζα_n e + ζv is right. No fix.

**7. Correct: disjoint supports, δ_i = 0 and nonzeroness (check b).**
- Columns with δ_i = 0 get x_i = 0. Columns with δ_i ≠ 0 can also get x_i = 0, when
  α_n + β_{cos δ_i} = 0; the proof's "∪{0}" covers this.
- Rounds use disjoint fresh columns. R lives on the stopping round, and the back-substitution
  weights live on rounds 1..k.
- The normalised column of the stopping round has weight 1·(α_0+β_0) = 1, and nothing touches it.

No fix.

**8. Imprecision: what "only the coset gP is used" means (check f).** The claim is accurate.
g enters only through the labelling ν ↦ g^νP, which gP determines. So any g′ ∈ gP gives the same
run with the same (α,β). We tested this with g′ = g·q, q ∈ P, in 89,040 runs. For κ = 2 this is
exactly "any non-residue". For κ ≥ 3, a generator of a different coset (g^u with u ≢ 1 mod κ) needs
the transformed contraction C′_{ij} = s_is_jC_{π(i)π(j)} of app:s2-contraction. Optional fix:
"(any g′ ∈ gP gives the same run; another coset generator needs the transported contraction of
Appendix app:s2-contraction)".

**9. Imprecision: the passage to eq:sde-target (check g).** It is correct. u_i is a κ-th root of
x_i ∈ P∪{0} (it exists, with 0 ↦ 0), and s_i = u_i^t with t ≥ 1 and td′ ≡ 1 (mod q′) gives
s_i^d = u_i^κ = x_i and s ≠ 0. That is Lemma `lem:app-s2-gcd`(b), but neither the statement nor
the proof cites it. *Fix:* cite Lemma `lem:app-s2-gcd`(b) at "applying a Bezout exponent". We
checked this with random d satisfying gcd(d,p−1) = κ on every run.

**10. Redundant hypothesis.** The hypothesis p ∉ E_2(κ) follows from having (α,β) at all. This
is harmless and needs no fix.

The coherent lemmas `lem:coherent-quadratic-sde` and `lem:coherent-power-sde` take δ as the first
dependency of the list (v_1..v_k, block) normalised by its *last* nonzero entry. That is a valid
instance of the proof, because the block part is nonzero since the v_l are independent. We
re-ran every "g" case with last-entry normalisation, and all passed.

## Test statistics (`tri_results.json`)

- **Contraction search (ours).** Exhaustive below 200, randomized above. It reproduces
  E_2(2) ∩ [3,200) = ∅, E_2(3) ∩ [3,120) = ∅ and E_2(4) ∩ [3,120) = {5,13,17,29,37,53}, as quoted
  after prop:decoupled-sde. A contraction was found for every tested prime.
- **Primes.** 53 per κ:
  - κ=2: 3..9973
  - κ=3: 7..9973
  - κ=4: 41..9973, excluding E_2(4)
  - In each case all small primes, then samples from 400–2000 and from 2000–10^4, and 9973.
  - The coset generator g is random, not always a primitive root.
- **Families.** a = 0..6, at exactly M = (a+1)(a+2)/2 columns:
  - random, zero, all-equal, coset multiples of one vector
  - cycled scaled units, unit blocks, rank 2, sparse
  - non-residue entries, small entries
  - a greedy adversary that keeps the column set using the most columns
  - Each family was run with g and with g′ = g·q, and once with last-entry normalisation.
- **Results.** 178,080 checked runs, 0 failures. Every output satisfies:
  - x ≠ 0, x ∈ (P∪{0})^M, Σx_iλ_i = 0, columns used ≤ M
  - the converted s solves Σ s_i^dλ_i = 0
  - rounds ≤ a+1, eliminations ≤ 3(a+1), power evaluations ≤ M+a
- **Algorithm uses all M columns.** This happened in 58,042 runs (every a: the maximum used equals
  M), so the count is exact for the procedure.

| κ | a | M | runs | used all M | max elims / 3(a+1) | max pow evals / M+a |
|---|---|---|---|---|---|---|
| 2,3,4 | 0 | 1 | 3392 each | all | 2/3 | 1/1 |
| 2,3,4 | 1 | 3 | 9328 each | 4192 / 4578 / 5960 | 5/6 | 4/4 |
| 2,3,4 | 3 | 10 | 9328 each | 1826 / 1796 / 2678 | 11/12 | 13/13 |
| 2,3,4 | 6 | 28 | 9328 each | 1424 / 2088 / 2486 | 20/21 | 34/34 |

(The full table for a = 0..6 is printed by `summarize.py`.)

- **Exhaustive** (every ordered column tuple), 0 failures:
  - (p,κ,a) = (3,2,1), (5,2,1), (7,2,1), (7,3,1), (13,3,1), (41,4,1)
  - (3,2,2): all 531,441 six-tuples over F_3²

**Tightness evidence, one fewer column.** We asked whether some M−1 columns admit no nonzero
x ∈ (P∪{0})^{M−1} with Σx_iλ_i = 0 at all, which is stronger than the solver failing. Each
counterexample was re-checked by brute force, and on each the solver correctly runs out of
columns.
- **a = 1** (M−1 = 2), counterexamples at every tested (p,κ):
  - p = 3, 5, 7 (κ=2); p = 7, 13, 19 (κ=3); p = 41, 61 (κ=4)
  - e.g. p = 3: [[2],[2]]; p = 41, κ=4: [[1],[12]]
- **(p,κ,a) = (7,3,2):** the five columns [[5,0],[2,5],[3,6],[6,3],[3,3]] have no nonzero signed
  subset sum. So (a+1)(a+2)/2 = 6 is the exact worst-case existence threshold there.
- **No counterexample found** (20,000 tries, or the 120 s cap) at:
  - (7,3,3), (13,3,2), (13,3,3), (19,3,2), (19,3,3)
  - (41,4,2), (41,4,3), (61,4,2), (61,4,3)
- **Not tight in general.** Chevalley–Warning gives a solution from κa+1 columns, so M−1 columns
  always suffice for κ=2 with a ≥ 2, κ=3 with a ≥ 4, and κ=4 with a ≥ 6. The (a+1)(a+2)/2 count
  is tight for the algorithm but not, in general, for existence.

## Mechanical preview, not a recommendation: E_W with the triangular arity

**How E_W is computed.** E_W(c) = max_{p>c}(1 + Σ_{d=2}^c e_d(p)), as in thm:bb-envelope
(main.tex ~1054) and lem:tb-count-exponent (appendix-torsion-blackbox.tex 1344–1363). Here
e_d(p) ∈ {1, 2, κ_d⌈log₂(κ_d+1)⌉}: linear, two-level (guard p ≥ 16κ_d^{2κ_d+2}), or Schedule 1.
The existing check is `research/audits/reviews/2026-11-04-rees-check-new-text/ew_values.py`.
I re-implemented it as `ew_tri.py`, with a cross-check by direct evaluation at every prime below
2·10^5.

**Result: E_W does not change.** e_d is the exponent of (g_d+1). The Schedule 2 arity
(g+1)((κ−1)g+1) and the triangular arity (g+1)(g+2)/2 both have degree 2 in g, so e_d = 2 either
way:

- E_W (paper) = 5, 11, 23, 38, 56, 77, 107, 143 (c = 2..9), at p = 3, 7, 13, 61, 61, 421, 2521, 2521
- **E_W^tri = 5, 11, 23, 38, 56, 77, 107, 143**, at the same witnesses

At every maximising prime the dominant grades are Schedule 1 grades, below every guard, and those
the triangular arity does not touch. K_c is set by Schedule 1 and is also unchanged. Only the
two-level constant changes, from C_d = κ_d − 1 to C_d = 1.

**Affected spots.** None of the E_W spots change:
- main.tex: 205 (tab:main-regimes caption), 222, 352 (E_W(9) = 143), 951 (143, 144, 146),
  1054/1056/1061, 1070 ("Here E_W(c) = 5, 11, …"), 1078 (144), 1337 (143)
- appendix-torsion-blackbox.tex: 1322–1361, 1401–1410, 1498–1561
- The abstract (main.tex 93–103) mentions neither E_W nor the Schedule 2 arity.

Spots that change if the triangular arity is adopted under the same guard (wording or numbers,
not exponents):
- main.tex 213–214 (tab:main-regimes: the Schedule 2 row and the combined-rule row M_d)
- main.tex 310 (tab:notation-sde, M_d^sym)
- main.tex 690 (rem:combined-schedule, "use Schedule 2 with M_d = (g_d+1)((κ_d−1)g_d+1)"); its
  "143" stays
- main.tex 651 (the product bound ∏M_d^sym ≤ r!((r+1)!)²)
- main.tex 633, 644, 655 (definitions and eq:power-arity; these describe Schedule 2 itself and
  stay if the triangular solver is added rather than substituted)
- appendix-torsion-blackbox.tex 1333–1334 (lem:tb-count-grade proof: "M_d ≤ (κ_d−1)(g_d+1)²,
  C_d = κ_d − 1" becomes C_d = 1); appendix-schedule3.tex 332
- **tab:fcs-budget (main.tex ~935), "combined Q" column**, recomputed by `fcs_tri.py` from
  `fcs_budget.json` (log₂ Q, table → triangular):

  | p | 11 | 1031 | 5281 | 2^31−1 | 2^61−1 | 2^127−1 |
  |---|---|---|---|---|---|---|
  | table | 202.1 | 167.3 | 852.3 | 944.9 | 555.4 | 61.5 |
  | triangular | 202.1 (unchanged) | 164.0 | 851.4 | 940.5 | 542.0 | 48.3 |

  I did not recompute its uniform-kernel column, which also mixes Schedule 2 grades.
- **tab:full-grade-budget (main.tex ~887):** its counts come from
  `research/reductions/rees_full_grade_budget.json`, which uses Schedule 2 arities, so they would
  change. Not recomputed.
- **tab:query-crossover (Schedule 1 only):** unchanged.

**Aside, a guard the paper does not adopt.** If the guard were p ∉ E_2(κ_d), using the exact
E_2(κ) for κ ≤ 5 quoted after prop:decoupled-sde, then E_W(c) for c = 2..5 would be 3, 5, 17, 22
(at p = 3, 7, 13, 31), against 5, 11, 23, 38. This is reported only because the guard is where
any exponent saving would come from. The arity change alone gives none.

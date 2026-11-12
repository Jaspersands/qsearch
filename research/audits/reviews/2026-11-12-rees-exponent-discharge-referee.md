# 2026-11-12 Referee: "which exponent of m can be proved now" (exponent discharge)

**Hostile referee report, AI-run, pending human review.** I reviewed
`2026-11-12-rees-exponent-discharge.md` and its scripts. I edited no paper, STATE, handoff
or reductions file. No git, no network, no Claude API calls.

Independent checks are in `2026-11-12-rees-exponent-discharge-referee/`:
`referee_checks.py` produces `referee_checks.out` (run with `nice -n 19`, PMAX = 12000).
They are finite computations and prove no asymptotic statement.

## 0. Why the core's Outlook says CONDITIONAL

I read core/main-core.tex §Outlook ("Smaller arities", l. 909), main.tex §§schedule1–3 and
appendix-schedule2. The label has four separate sources.

1. **Schedule 2, thm:power-sde(ii).** The label is a review-status label. It does not
   mark a missing hypothesis. main.tex (after thm:power-sde) says: "No human has read the
   proof, so part (ii) stays conditional, and Theorem main does not use it." The status
   convention in main.tex's front matter defines *conditional* as "dependence on ... an
   unproved part, in particular on Theorem power-sde(ii)". That is an owner policy, and
   it is stricter than the label thm:main carries.
   - I re-derived thm:app-s2-main. The lemmas checked are app-s2-gcd, tensor, witness,
     normal, weil-count and stage, plus the abort budget. I found no gap.
   - The proof does use only p ≥ 4κ^{2κ+2} (rem:app-s2-four is correct).
   - The columns are arbitrary. The output is checked and never wrong. The scalars are
     explicit (θ_ij·ω'_b, then u^t).
2. **Triangular variant.** prop:triangular-sde itself carries only "AI-checked", and its
   proof is complete; I re-derived the rounds and the back substitution. Its hypothesis
   p ∉ E₂(κ) is where the condition sits. That hypothesis comes from:
   - prop:decoupled-sde, which is labelled **conditional**, or prop:app-s2-TA (Weil bound
     plus second moment, unreviewed), for "outside finitely many primes";
   - finite AI searches for the actual E₂ sets. E₂(9) is **not determined**.
3. **Block-steered option and Schedule 3.** These have genuine extra hypotheses:
   - the i.i.d. label law of fresh ideal sources, which thm:main does not use;
   - for block-steered, (G1)–(G3), i.e. p large compared with g_d² and n_d.
4. **Core-level policy.** "Nothing in this section is claimed here." The proofs exist only
   in the full version.

**Consequence.** For the worst-case solvers (Schedule 2, triangular, tower, chains) I
confirm the note's finding: there is no hidden hypothesis. That covers worst-case versus
distributional labels, explicit scalars, the Bezout step (Lemma app-s2-gcd(b)), retries
on saved labels (rem:is-import(d), Phase 0 re-run per attempt) and independence (outputs
exact for every record).

The note's *discharge* of the label is not legitimate as written, however. It renames a
policy label "PROVED at the paper's standard", but the paper's standard explicitly puts
power-sde(ii) and prop:decoupled-sde below thm:main until a human reads them. The note's
own last paragraph says "CONDITIONAL ... on human review", so it contradicts its own T2,
T3 and T5 headings.

## Verdicts

### (A) E = 2c−1 — CORRECT WITH FIXES

- The arithmetic is right. With arity (a+1)((κ−1)a+1) or (a+1)(a+2)/2 when κ_d ≥ 2, and
  a+1 when κ_d = 1, we get E = 1 + Σ_{d=2}^c 2 = 2c−1. This is attained at p ≡ 1 mod
  lcm(2..c), and equals 17 at c = 9.
- I recomputed T_A from the closed form of prop:app-s2-TA:
  - T_A(9) = 3 099 365 719 < 3.10·10⁹;
  - T_A(8) = 117 441 562.03, matching ⌈T_A(8)⌉ = 117441563.

  So "p > 3.10·10⁹" is safe.

Fixes:

1. **Relabel T2 and T3 ("PROVED") as conditional.** They depend on
   thm:power-sde(ii) / prop:app-s2-TA (AI-checked; conditional in main.tex) and, below
   T_A, on finite computations (the E₂ tables). This is the same label the Outlook
   already uses.
2. **The bands T_A(κ) < p ≤ T_S(κ) and p ≤ T_A(κ).** In these bands the contraction is
   found, and E₂ membership is decided, by exhaustive search. That is O_κ(1), but at κ = 9
   it is about p^{κ}, with p up to 2.8·10¹⁰. Say so: "polynomial time" holds only with an
   astronomically large constant there.
3. **§2 T2: "decided (414 members) for p ≤ 20000" is wrong.** It is 342 members of 372
   primes for p ≤ 20000, and 414 for p ≤ 25000.
4. **"Undecided on (20000, 3.10e9)" is too coarse.** Explicit contractions cover every
   prime in (20000, 9⁹/2] except 1373 listed primes, and 78 of those are decided. The
   undecided set is the 1295 listed primes in (25000, 424549] together with
   (9⁹/2, T_A(9)].
5. **§3: "2521 ∉ E₂(κ) for κ ≤ 9" is false.**
   - 2521 lies in E₂(8) and in E₂(9) (dfs2b tables; the note's own `in_E2` agrees).
   - At p = 2521 the E₂-only rule gives 81, R3 gives 38 and R5 gives 20, not 17.
   - The "artefact" paragraph must be restated: E₂ tables alone do not make 2521
     quadratic at grades 8 and 9.
6. **§2 T2 "union chains in between".** For κ = 9 the 3·3 tower covers p > 1.347·10⁵ via
   the *numerical* T_R(9,3), and p > 2 125 764 in closed form. Complete searches cover
   p ≤ 135000 (rem:app-s2-tower-scope). State that status.

### (B) Schedule 1 at depth ⌈log₂ t⌉ — CORRECT WITH FIXES

I checked IS §3.3 (is_1503.09016.txt, ll. 577–594).
- Iterating Theorem 11 L times on G^L vectors gives one vector with 2^L representations,
  with pairwise disjoint supports and explicit d-th-power coefficients.
- Multiply representation j by z_j^d, where Σ_{j≤t} z_j^d = 0, and give the other
  representations weight 0. This kills the vector for any t ≤ 2^L.

So "Any t ≤ 2^L works" is right, and the audit statement (2026-11-02-rees-is-solver.md
§4(c)) is right.

An exact simulation of this step at (p,κ) = (7,2), (13,4), (11,2) gave 60/60 verified
witnesses (check 6). My independent zero-sum BFS reproduces E_S1t = 5, 8, 16, 19, 35, 36,
44, 53. The Weil shortcut showed no violation; t(41,8) = 5 and t(2521,8) = 3. The
analytic tail above PMAX gives a maximum of 53.

Fixes:

1. **Theorem 11 allows J = ∅.** In that case stop at once, since a solution is already
   found. Otherwise some of the 2^L representations could be empty. Add one sentence.
2. **Make the arity public.** Its depth ⌈log₂ t⌉ is computable before the run:
   - t = 2 iff (p−1)/κ is even;
   - otherwise ⌈log₂ t⌉ = 2 once p+1−(κ−1)(κ−2)√p > 3κ;
   - exhaustive search below that.

   Only *finding* the length-3 or length-4 zero sum is Las Vegas. So the core's
   "deterministic, no solver failure to budget" becomes rem:is-import(d) with ε/3.
3. **Status.** Ivanyos's confirmation covers C ≤ G^{⌈log₂(d+1)⌉}, not the t-depth
   variant. That variant is an AI reading of the same proof, at the rem:is-import(e)
   standard.

The step 145 → 53 is genuine. B_{κ_d} at full depth still gives 145 at p ≡ 1 mod 2520, so
the gain comes from the depth alone.

### (C) "Only human review remains" — CORRECT WITH FIXES

This holds for the worst-case solvers on thm:main's input. Fixes:

1. **More than review remains.** Add:
   - the finite AI computations (E₂ tables, NOSTD lists, chain searches);
   - the numerical thresholds (T_R(9,3), Θ₂ and Θ₃);
   - the O_κ(1) exhaustive-search constants noted under (A).
2. **Law-derived items** (T4, LAWMIX) hold only for the ideal i.i.d. supply of thm:main.
   They do not hold for pooled leftovers or the black-box corollaries; for the latter,
   rem:oblivious and cor:black-box-pe use branches where labels are not ideal.
3. **The pool lemma (§5.1) is mathematically sound.** A weight-0 slot is untouched,
   stays in product with everything else, and is exactly ρ_λ given λ. But it changes the
   core procedure, which "consumes and discards" weight-0 targets, and it makes the tree
   adaptive. N_QFT would then need a public upper bound. Since it gives no gain, keep it
   out.

### (D) Worst case over p > 9 at c = 9: 19 / 37 / 53 — CORRECT WITH FIXES

- **53:** verified independently.
- **37:** right as a finite computation over the quoted lists. At p = 41, κ₈ = 8: the
  8th powers are μ₅ = {1, 10, 16, 18, 37} and t = 5, so this grade costs 24. Its status is
  "finite computation + quoted NOSTD/E₂/chain data", not PROVED. The note has not re-run
  NOSTD.
- **19:** this is the paper's LAW table. It is O(m¹⁹·polylog m), not m¹⁹, and holds only
  under the label law.

## Gate bound (check 4)

The bound follows, and more sharply than the note's "UNKNOWN".
- **Controlled translations.** There are ≤ (c−1)·#sources = O(Q) of them, each
  4·(d−1)d(d+1)/2 brackets × O(D³) = O_c(m³) field operations.
- **QFTs.** There are O(Q·m) of them, each poly(log p, log(m/ε)).
- **Classical solver work, per merge:**
  - triangular: O(a) eliminations of size a×(a+1), plus O(M) coset tests and roots;
  - Schedule 2: N nullspaces plus one of size (κ−1)a×N.

  Per column this is O(a² + poly(κ, log p)), so it does not dominate.

Total: O_c(Q·m³·poly(log p, log(m/ε))) + O(Q·w), plus the O_c(1) contraction-search
constants. This is exponent E+3 = 2c+2 (20 at c = 9), up to polylog factors and the w
term.

## What could go into the core, and at what status

1. **T1 (Schedule 1 at depth ⌈log₂ t_d⌉, at degree κ_d, Las Vegas zero sum).** Status:
   same as thm:main (AI reading of IS §3.3; rem:is-import(d)). The c = 9 value 53 is a
   finite computation plus the Weil tail. Add the J = ∅ sentence. This is the only item
   that can lower the core's stated exponent (145 → 53) without Schedule 2. The macro
   change is the owner's decision.
2. **"Exponent 2c−1 for p ≥ 4c^{2c+2}".** This uses Schedule 2, or triangular with the
   symmetric contraction normalised as α = t + t₀, β = t − t₀. It can enter the core only
   if the ≈1.5-page proof of thm:app-s2-main is moved there *and* the owner lifts the
   "stays conditional" policy. Otherwise it goes in the Outlook as conditional.
3. **Outlook rewording (conditional; AI-checked; finite computations).**
   - Triangular: exponent 2c−1 for p > T_A(c) (3.10·10⁹ at c = 9), and for c ≤ 8 at
     p > 14281.
   - Law-free per-grade worst case over p > 9 at c = 9: 37.
   - The current "only from 145 to 143" holds only for the paper's specific rule.
4. **Not for the core:** the pool lemma, the two-register refutation, Theorem A, T4
   (law-derived), and the gate sketch (full version at most).

## Disposition (integrator, 2026-11-12)

- Item 1 (T1, Schedule 1 at depth ⌈log₂ t_d⌉, 145 → 53 at c = 9): added to the core Outlook
  as a new paragraph, "Shorter zero sums in Schedule 1". It includes the J = ∅ sentence, the
  public-arity rule and the Las Vegas charge via rem:is-import(d). The theorem, the macro
  ReesClassNineQueryExp = 145 and the abstract are UNCHANGED. Making 53 the stated count is
  the owner's decision, and it needs numbers.tex regenerated; make_numbers.py is not run by agents.
- Items 2–3: the core Outlook "Smaller arities" now explains the 143 figure and states
  2c−1 for primes above T_A(c) (3.10·10⁹ at c = 9) and for c ≤ 8 at p > 14281, plus the
  law-free worst case 37. All are under the paragraph's CONDITIONAL label. Schedule 2 is not
  promoted.
- The note's fixes (342 rather than 414 members, the 2521 ∈ E₂ correction, relabelling T2/T3
  as conditional) are left to the note's next revision; they are not used in the paper.

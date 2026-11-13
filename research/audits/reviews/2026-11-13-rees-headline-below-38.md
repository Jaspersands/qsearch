# Rees headline below 38: a proved class-9 exponent of 21 (2026-11-13)

AI only (one Claude Code subagent), pending human review. No paper file, numbers.tex, STATE,
handoff or reductions file was edited. No Git, no network, no API calls. Every run used `nice -n 19`,
one heavy process at a time; the largest RSS was about 0.4 GB. Scripts, outputs and the LaTeX
fragment are in `research/audits/reviews/2026-11-13-rees-headline-below-38/`.

Labels: PROVED, PROVED given cited theorems, CONDITIONAL, REFUTED, UNKNOWN, NOT computed. Finite
checks can only falsify; the exact computations below are of the same kind as the core's own
(lem:halved-exponent(ii)): exhaustive per-prime evaluation plus a residue-class argument.

## 0. Verdict

**The proved class-9 headline drops from 38 to 21** (PROVED given cited theorems, at the core's
standard). The only imports are the two the core already uses: Weil's bound for two-variable
diagonal equations [LN, Ch. 6] (as in lem:zero-sum-length(iii), lem:two-term) and Las Vegas root
finding [Rabin]. Nothing is taken from the full version's appendix or from AI tables without being
re-proved here or recomputed and checked here.

- New schedule "1H+" (fragment.tex, Def. def:schedule1hplus). Exponents E_+(c) for c = 2..9:
  **3, 5, 9, 10, 14, 16, 19, 21**. The core has 3, 6, 10, 14, 20, 25, 29, 38.
- E_+(9) = 21 is attained **exactly at p = 13, 19, 37, 73 and at every prime p ≡ 1 (mod 2520)**.
- Grade exponents at p ≡ 1 (mod 2520), d = 2..9: 2,2,2,2,3,3,3,3 (core: 2,3,3,5,4,7,4,9).
- This equals the conditional R8 value 21 of the k9-bottleneck note, with all of R8's binding
  ingredients now proved. The c = 2..9 maxima coincide with R8's row exactly.
- With the parallel helper's Lemmas K and D (linear-arity note; "proved pending referee"): the max
  stays **21**. Core + K + D alone, without the nodes here, gives **28** (at p = 73 and
  p ≡ 1 mod 2520). So K and D do not lower the max; Lemma K would only shorten the proof (it
  replaces the κ = 3 certificate table and threshold).

## 1. Where the 38 comes from (task 1)

E_H(9) = 1 + max_p Σ_{d=2}^9 e^H_{p,d}. At p ≡ 1 (mod 2520) every κ_d = d and every (p−1)/d with d
odd is even, so t = 2 at odd κ. Above 26244 the core gives:

| d | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | sum |
|---|---|---|---|---|---|---|---|---|---|
| e^H | 2 (1×F1 over GE) | 3 (S1) | 3 (1×F1 over κ=2) | 5 (S1) | 4 (1×F1 over κ=3) | 7 (S1) | 4 (1×F1 over κ=4) | 9 (S1) | 37 |

So 38 = 1 + 37. The odd grades contribute 3+5+7+9 = 24, and the even grades inherit the κ = 3 and
κ = 4 values through halving. The exact range below 26244 gives the same 38 at 2521, 7561, 12601,
15121, 20161 and nothing larger. Any improvement must therefore lower every p ≡ 1 (mod 2520), large
and small, and must not raise any other prime above the new value.

## 2. The ingredients of the conditional routes (task 2)

| ingredient | can be made self-contained? | length | used? |
|---|---|---|---|
| Schedule 2 two-level contraction (tensor + contraction) | yes: it is Lemma R (below) with L = 1 plus Lemma SM | ~1 p | κ = 3, 4, 5 |
| two-level at κ = 6..9 | proof yes, but the crude SM threshold is 8.4e5, 8.9e6, 1.5e8, 3.3e9 (certificates below it are too costly at κ ≥ 7) | — | no (not needed: p = 13 binds) |
| towers / flexible-line chains (thm:app-s2-chain) | yes, replaced by the simpler block-refinement Lemma R (same degree L+1, larger constant) | ~0.5 p | κ = 9 tower 3→9; Tier B chains |
| union targets (K_L ≠ {0} corollary) | yes: Lemma R is stated for union targets from the start | included | κ = 7 union step; Tier B |
| "third-degree collision" at 37/73 (Lemma S stage over a {0,m}-chain, Lemma F finish) | yes: Lemma S is the core's Lemma stage verbatim with P ∪ qP for q = ξ^m; Lemma F_K is the core's Lemma finish(ii) with a class-restricted relation in place of Gaussian elimination | ~0.4 p | κ = 7 (all p), κ = 9 at 19/37/73, κ = 4/6/8 at small p |
| Theorem HC (11-12 note) | = Lemma S + Lemma F_K | — | yes |
| second-moment existence (T_A, union-step Ψ_U, step thresholds) | yes, re-proved in a cruder uniform form (Lemma SM) using only the core's diagonal-equation Weil bound, no Jacobi-sum or polynomial-character Weil bound | ~0.75 p | all steps above |
| ℓ = 3 IS objects, SAT nodes | no (conditional on IS Lemma 12 at ℓ = 3) | — | no |
| E_2 tables of the full version | no: replaced by my own certificate tables | — | no |

The fragment (fragment.tex) is about 3 pages in the core's style: Definition def:k-node, Definition
def:rc, Lemma lem:refine (R), Remark rem:designated, Corollary cor:chain, Lemma lem:stage2 (S),
Lemma lem:finishK (F_K), Lemma lem:sm (SM), Table tab:sm-thresholds, Definition
def:schedule1hplus, Theorem thm:halving-plus, Lemma lem:chain-exponent. It compiles standalone
with stub macros (only references to core labels are undefined).

**Lemma SM (PROVED given the diagonal Weil bound).** For RC(D; R → K) with r = |R|, k = |K|:
ρ ≤ 1/E[n_j] + γ^{r−1}, γ = (1 + (D−1)²/√p)(p/(p−1))², and a contraction exists when
Φ = Σ_j (1 − 1/ρ_j) < 1. The pair counts are counts of ξ^{ℓ'}z^D − ξ^ℓ s^D = δ, so only the
two-variable diagonal bound enters. Thresholds (`thresholds.out`):

| step | T_exist | T_samp (sampler ≥ 3/8 per round) |
|---|---|---|
| two-level κ = 3 | 430 | 39 096 |
| two-level κ = 4 | 9 395 | 778 545 |
| two-level κ = 5 | 99 745 | 6 922 583 |
| tower RC(9; {0,3,6} → {0}) | 1 124 521 | 85 628 629 |
| union RC(7; Z_7 → {0,m}) | 1 995 734 | 149 308 802 |

## 3. The new maximum (task 3)

**Certificates** (`run_certs.py` → `certs_stage1.json`, `run_certs.out`): for every prime below
T_exist in each row, a contraction was searched (random β and column scans in `rcrand.c`; the complete
DFS `rcdfs.c` of the k9-bottleneck folder as a search engine for p ≤ 12000).

| step | primes p ≡ 1 below T_exist | found | not found |
|---|---|---|---|
| two-level 3 | 39 | 39 | none |
| two-level 4 | 577 | 571 | 5, 13, 17, 29, 37, 53 (= E_2(4)) |
| two-level 5 | 2380 | 2371 | 11, 31, 41, 61, 71, 101, 131, 151, 181 (= E_2(5)) |
| tower (9; {0,3,6}) | 14 560 | 14 546 | 19, 37, 73, 109, 127, 163, 181, 199, 271, 307, 379, 433, 487, 523 |
| union (7; Z_7 → {0,m}) | 24 732 | 24 729 | 29, 43, 113 |

"Not found" is never used as non-existence; the rule simply does not use that node there.

**Tier B** (`tierB.py` → `tierB.json`, `tierB_witnesses.json`, `tierB.out`): at the 28 primes where
the Tier A value exceeded the tail value for some c (all ≤ 523), a BFS over chains of length ≤ 3 with
|K_t| ≤ 3, starting from GE or from D-solvers.

**Rule** (`rule.py`; `ruleA.out` without Tier B, `ruleB.out` with it): exhaustive for every prime
p < 2·10⁶, using the core's class sumsets below 26244 and lem:zero-sum-length above. For
p > 2·10⁶ every step is above T_exist and p > 4·9⁴, so e⁺ = (1,2,2,2,2,3,3,3,3) for κ = 1..9. This is
monotone along divisibility, so the tail max is 21, attained exactly when 2520 | p−1.

| c | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| core E_H | 3 | 6 | 10 | 14 | 20 | 25 | 29 | 38 |
| Tier A only | 3 | 5 | 9 | 12 | 17 | 19 | 22 | 27 (p = 181) |
| **E_+ (A + B)** | **3** | **5** | **9 (5, 13)** | **10** | **14** | **16 (43)** | **19 (13)** | **21** |
| R8 (conditional) | 3 | 5 | 9 | 10 | 14 | 16 | 19 | 21 |

Binding grades at c = 9:
- 13: 2,2,4,1,4,1,4,2. The grades κ = 4 and κ = 6, where 13 has no two-level contraction and no chain.
- 19: 2,2,2,1,4,1,2,6.
- 37: 2,2,3,1,3,1,3,5. The κ = 9 grade is a stage over (1,{0}) → (3,{0}) → (9,{0,4}), then F_K to {0,2,5}.
- 73: 2,2,2,1,3,1,4,5.
- p ≡ 1 (mod 2520): 2,2,2,2,3,3,3,3.

**Checks** (all finite):
- Regression: with the new nodes off, `rule.py` reproduces the core's Schedule 1H degree at every
  (p, κ), p < 26244: 0 disagreements. So it also reproduces 38.
- `verify_all.out`: 74 536 stored certificates and witnesses re-checked by a second checker, written
  differently (coset membership (x g^{−m})^{(p−1)/D} = 1, primitive root recomputed): 0 rejected.
  They had already passed `certs.check_rc`.
- `executor.out`: an end-to-end executor written from the fragment (GE, Lemma R chains, Lemma S,
  F1). Results: 360/360 outputs verified (x ∈ (P∪0)^M, x ≠ 0, Σxλ = 0). Coverage: tower 3→9 at
  2521, 7561, 1171, 2017; two-level 5 at 1021, 3001, 9901; κ = 7 union stage + F1 at 12601, 10501,
  15121; a = 1..3; uniform, repeated, axis and zero-heavy banks.
- `negctl.out`: 30 perturbed certificates. All 30 are rejected by the checker and all 30 are caught
  by the executor.
- `crosscheck_r8.out` (p ≤ 3000, against exponents_r8.py imported read-only):
  - 1559 (κ, p) pairs agree.
  - 176 have ours > R8. These are expected, since R8 uses E_2-table two-level contractions at κ ≥ 6.
  - 93 have ours < R8, all at κ = 8: halving over a degree-2 κ = 4 solver, then F1 (T₁ ⊇ F_p^× by
    exact class sumsets), or a Tier B chain. R8's κ = 8 base value apparently does not compose halving
    with the improved κ = 4 node. Each such plan is a core halving plan with a valid inner solver.
  - c = 9 maximum: 21 for both. Ours is attained at {13, 19, 37, 73, 2521}, R8's at {13, 19, 37, 73}.
- `kd_variants.out`: the Lemma K / D bookkeeping of §0.

## 4. Adversarial self-check

- **"Attained exactly" depends on the definition of the schedule.** It holds for the fixed candidate
  list of def:schedule1hplus. Adding two-level nodes at κ ≥ 6 would lower the 2520 class, but the
  k9-bottleneck note's exhaustion says 13, 19, 37, 73 keep 21 in this calculus. So "≤ 21" is the
  robust claim, and "= 21" is a statement about this schedule.
- **Weil import.** I use the core's own form, |N − p| ≤ (D−1)²√p for a u^D + b v^D = δ with
  a, b, δ ≠ 0. The core flags its locator (LN Thm 6.37) as NEEDS HUMAN VERIFICATION; that flag now
  covers Lemma SM too.
- **Preprocessing.** Contractions are found once per (p, κ). This adds tasks to the n_pre ≤ 2(c−1)
  count of rem:is-import(d), so the paper would need a new bound there (still O_c(1)).
- **The band T_exist ≤ p < T_samp (up to 1.5·10⁸).** The finding cost there is a constant for each κ,
  but it is not computed: each β-trial succeeds with probability ≥ 1 − Φ(p) > 0, which can be small
  just above T_exist. This is honest but ugly. Fix options: extend the certificate tables to T_samp,
  or sharpen Lemma SM with first-order cancellation, as the appendix's T_A does.
- **Certificates use the least primitive root.** At run time that needs p − 1 factored. This is fine,
  because tables are used only for p < 2·10⁶. Above T_exist, Lemma SM holds for every coset
  generator.
- **Constant C^H_c.** Lemma halved-exponent(iii) asserts C^H_c = C_c. I claim only that some constant
  depending on c exists (thm:halving-plus); C_c in thm:main(4) would need re-checking.
- **Lemma R's designated coefficient.** It must have D-class 0 at the new modulus. This is handled
  by scaling to 1 (rem:designated); the executor asserts it on every step.
- **Search engine reuse.** rcdfs.c is a prior AI program. Only its witnesses are used, and they are
  checked twice by my code; no non-existence claim rests on it.
- **Scope of the exact range.** It is exhaustive for p < 2·10⁶; the tail argument covers the rest.
  The c < 9 rows use the same range plus tail.
- **Not done.** Human-style refereeing of the fragment; a full LaTeX integration; recomputation of
  numbers.tex or the crossover table.

## 5. Next question, command and paper edits (proposal only)

- Referee fragment.tex. Check first Lemma SM (the counting) and Lemma R (the class bookkeeping),
  then lem:chain-exponent against `rule.py`.
- Paper edits, if adopted:
  - thm:main(4): 38 → 21.
  - lem:halved-exponent → lem:chain-exponent.
  - rem:is-import(d): new n_pre count.
  - An artifact entry for the certificate tables.
  - The class-9 profile and crossover table need recomputation.
  - numbers.tex must not be hand-edited (TRAPS 17).
- Command to reproduce:
  `nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-headline-below-38/rule.py 2000000`
  Acceptance: `E_new(c) = {2: 3, 3: 5, 4: 9, 5: 10, 6: 14, 7: 16, 8: 19, 9: 21}` and 0 regression
  disagreements. The run needs certs_stage1.json and tierB.json; `run_certs.py` and `tierB.py`
  regenerate them.

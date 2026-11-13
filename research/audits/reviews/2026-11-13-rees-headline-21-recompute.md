# Independent recompute of the class-9 headline 21 (Schedule 1H+) — 2026-11-13

AI-checked (Claude, independent checker), pending human review. Scripts and outputs:
`research/audits/reviews/2026-11-13-rees-headline-21-recompute/`. Python `/opt/anaconda3/bin/python`;
contraction search in C (`rcsearch.c`). The helper's scripts, tables and `.out` files were not opened
until steps 1–3 below were finished (step 4 is the comparison).

## Verdict

**REPRODUCED (finite computation; CONDITIONAL on the fragment's lemmas, which I re-read and found sound
apart from the wording points below).** From `fragment.tex` and the core alone, my own implementation
gives E_+(c) = 3, 5, 9, 10, 14, 16, 19, 21 for c = 2..9. At c = 9, 21 is attained at p = 13, 19, 37, 73
and at every prime p ≡ 1 (mod 2520) checked. Nothing else attains it: I checked every prime below 2·10^6,
and every unit class mod 5040 above that. The grade-exponent vectors at 13, 19, 37, 73 and at
p ≡ 1 (mod 2520) match the fragment. The definitions are **not complete enough on their own**, because
candidate (f) "Tier B" and "availability" below T_exist both point at artifact tables. I had to make an
interpretation (finding F1). Under it the numbers come out the same.

A finite computation is not a proof. The 21 holds only for the schedule as defined, and it rests on
Lemmas refine/stage2/finishK/sm, which are proved in the fragment and still need review.

## 1. Validation on the core (PROVED-by-computation reproduction)

`core_recompute.py` implements def:schedule1h and lem:exponent directly from their text: class sumsets,
the T_j recursion, and t_{p,κ} by sumset iteration. Primes below 26244 are computed exactly; above that the
formula is applied per unit class mod 5040.
E_1 = 5, 8, 16, 19, 35, 36, 44, **53**, where 53 is attained at 2521, 7561, 12601 and at the class 2521 mod 5040.
E_H = 3, 6, 10, 14, 20, 25, 29, **38**, where 38 is attained at 2521, 7561, 12601, 15121, 20161 and at p ≡ 1 mod 2520.
Both match lem:exponent(ii) and lem:halved-exponent(ii) (`core_recompute.out`).

## 2. Schedule 1H+ (own implementation, `plus.py`)

- **Lemma sm thresholds:** recomputed in 60-digit mpmath; all five (T_exist, T_samp) rows of
  tab:sm-thresholds match exactly (`thresholds_check.out`). I re-derived the proof: the class sets A_ij,
  the second moment via the Weil count (D² preimages per point), Paley–Zygmund, the union bound, the
  Chebyshev sampler and p/μ_0 ≤ (2D)^r. No error found. It inherits the core's unverified locator for
  Weil's bound.
- **Contractions:** `rcsearch.c` finds contractions both by random search and by exhaustive DFS, using
  the WLOG β_0 = 0 and α_0 = 1 (translation and P_D-scaling).
  - Every certificate is re-checked by `rc.check_rc`, written separately. It computes classes by
    x^{(p-1)/D} against powers of ξ^{(p-1)/D}, not by log tables.
  - The exhaustive verdicts agree with an unnormalised brute force in 6778/6778 cases
    (p ∈ {7, 11, 13, 19, 31, 37, 73}; `bruteforce_rc.py`).
  - Every RC question at p ≤ 523 was resolved exactly (FOUND/NONE, 0 UNKNOWN).
  - Every certificate needed below 2·10^6 was found (0 missing; `gap_400k_2M.out`).
- **Results (variant B: Tier B = all chains with L ≤ 3 and |K_t| ≤ 3 at every p ≤ 523):**
  - p < 2·10^5 exact (`run_B_200000.out`): E_+ = 3, 5, 9, 10, 14, 16, 19, 21. The c = 9 maximum is attained at
    exactly {13, 19, 37, 73} ∪ {p ≡ 1 mod 2520} (35 primes; `residue_part.out` checks the set).
  - 2·10^5 ≤ p < 2·10^6: same maxima, with the c = 9 maximum attained only at p ≡ 1 mod 2520 (`gap_400k_2M.out`).
  - p ≥ 2·10^6: one actual prime per unit class mod 5040 gives 3, 5, 7, 9, 12, 15, 18, 21, with 21 only at
    classes 1 and 2521 mod 5040, i.e. p ≡ 1 mod 2520. This matches the fragment's proof.
- **Grade vectors:** p = 13: 2,2,4,1,4,1,4,2; p = 19: 2,2,2,1,4,1,2,6; p = 37: 2,2,3,1,3,1,3,5 (the same
  κ = 9 plan as the fragment); p = 73: 2,2,2,1,3,1,4,5. All agree with the fragment.
- **Exhaustive NONE results:** TW9 does not exist at p = 19, 37, 73, 109, 127, 163, 181, 199, 271, 307, 379, 433, 487, 523.
  TL4 does not exist at 13. The lower bounds at the four small maximisers therefore rest on exhaustive searches.

## 3. End-to-end executor (`executor.py`, `finish_coverage.py`)

The executor implements lem:refine (with rem:designated scaling), the chains, lem:stage2/lem:stage, lem:finish(i)
(F0) and lem:finishK, and checks each output from scratch: w ≠ 0, r^κ = w, Σ w λ = 0. Roots are taken from
tables in place of Las Vegas root finding. S1 is not executed because it needs the imported IS step. On each
plan's full arity it ran 10 bank types: uniform, zero, constant, rank-1 in one P_9 coset (×3), e1/e2 blocks,
sparse 0/1, zero-interleaved, ±1. **All passed:**

- **κ = 3:** p = 7, 13, 31 (TL, a ≤ 3).
- **κ = 4:**
  - p = 5: (H2)×1 with a chain-K finish.
  - p = 13: (H2)×1 with the FH2 finish.
  - p = 37: chain H2→(4,{0}).
  - p = 73: TL.
- **κ = 9:**
  - p = 19 and 37: stage over a chain, then a chain K-finish.
  - p = 73: stage, then the FH3 finish.
  - p = 181 and 433: length-2 Tier-B chain.
  - p = 397: the tower TW, at a = 1, 2.
- **κ = 6:** p = 7, (H3)×2 with the FH2 finish.

At κ = 9 almost every bank ends at the early exit J = ∅. To cover the finish path,
`finish_coverage.py` builds genuine (1, ε) objects and runs lem:finishK: 5/5 at p = 19 (K = {0,1}),
p = 37 (K = {0,2,5}, a = 1, 2) and p = 73 (K = {0,3,6}), plus κ = 4 at p = 13. These are finite checks only.

## 4. Comparison with the helper (after steps 1–3)

`compare_helper.py` imports `rule.py` read-only and compares every (p, κ) below 2·10^5:

- **Disagreements: 8, none at the helper's 28 Tier-B primes and none above 523.** All 8 are at κ = 6, with my
  value lower: (79: 3 vs 4), (139: 3 vs 4), (223: 3 vs 4), (229, 313, 337, 397, 457: 2 vs 3). Each comes from a
  Tier-B chain such as GE→RC(6;Z_6→{0}) at a prime the helper did not list. Maxima are unaffected.
- With Tier B switched off, my code gives 3, 5, 9, 12, 17, 19, 22, 27, the same as the helper's `ruleA.out`.
- The helper's U7 certificate fixes a single m; I try all m. This made no difference anywhere.

## 5. Extra task: forbid S1 at every level (`no_S1` flag)

| Tier-B variant | p < 2·10^5 | Result |
|---|---|---|
| all p ≤ 523 | exact | 0 (p, κ) without a plan; per-(p, κ) degrees identical to the S1-allowed run (0 differences) |
| the helper's 28 primes | exact to 26244 | 0 without a plan; maxima unchanged |
| none | exact to 26244 | 26 (p, κ) without a plan; the first is (11, κ = 5) |

**Confirmed: S1 is indispensable at 0 primes below 2·10^5, and the maxima are unchanged.** This holds only
with Tier B in place. The 26 (p, κ) pairs that need S1 without Tier B all lie inside the helper's list. The
only listed primes without such a pair are 5, 7 and 13.

2·10^5 ≤ p < 2·10^6 (`gap_noS1.out`): every p ≡ 1 mod 9 below 1124521 and every p ≡ 1 mod 7 below 1995734 has a TW9 / U7 certificate (33314 queries, **0 primes without a plan**), so E_+ is unchanged there. Above 2·10^6, S1 is never needed, because every
contraction exists by Lemma sm.

**For removing thm:is-import at c ≤ 9, main-core.tex still cites it or lem:rounds in:**

- line 177 (informal statement)
- line 181 (thm:main hypothesis) and thm:main(3) (Q ≤ ∏B_d, the bar-B bound and E_1, through candidate (a))
- rem:main-solver (210)
- rem:is-import and rem:is-printed (533–574)
- lem:bezout (605: "computed by Lemma rounds")
- Schedule 1 (617)
- def:schedule1h(a) (703)
- thm:halving(i) (A ≤ G^L) and (ii) (724)
- lem:halved-exponent (A_d ≤ B_d, E_H ≤ E_1)
- rem:proof-uses (873)
- the hypotheses of cor:black-box (926), cor:black-box-pe (950), cor:nilpotent (992, which also imports
  Imran–Ivanyos for p ≤ c) and cor:utz (1023)
- app:artifacts (1159)

For c ≥ 10 the IS import stays, because the fragment defines H+ only for κ ≤ 9. A conditional-free
statement at c ≤ 9 would also need the Tier-B data, or an intrinsic definition of it, inside the paper.

## Findings (definition completeness and wording)

- **F1 (material, not self-contained).** def:schedule1hplus(f) is defined by "the chains … recorded
  [in tierB.json]" at "28 primes listed". Availability below T_exist is "the certificate table of the
  artifact". Without these files the reader cannot reproduce e^+. I had to guess. My guess: all chains
  with L ≤ 3 and |K_t| ≤ 3, whose base is GE or H^+_{D_0} with D_0 < κ, all moduli dividing κ, last
  modulus = κ, used at every p ≤ 523; availability is "a contraction exists". Under that guess, degrees at the
  28 primes coincide with the helper's. Fix: state (f) intrinsically, for example "every p ≤ 523, every such chain
  for which a contraction exists", and print the certificate counts.
- **F2 (ambiguity).** It is unstated whether a chain node whose last modulus is D_L < κ (lifted K) may serve
  as an F_K node. Allowing it lowers e_8 at p = 17 from 6 to 5 (`degrees_Blift_600.json`); maxima are unchanged.
- **F3 (ambiguity).** In (e), the m of the union step RC(7;Z_7→{0,m}) is not specified (any m, or a fixed one).
  No numerical effect.
- **F4 (typo).** In the proof of lem:stage2, "P_D = P ∪ qP replaced by P ∪ qP" replaces a set with itself;
  the intended reading is "P_{κ/2} = P ∪ qP for q = ξ^{κ/2} replaced by P ∪ ξ^mP".
- **F5 (proof wording).** The proof of lem:chain-exponent says "for odd κ every candidate is (a) … or a chain".
  This is false at κ = 7, where the (e) plans exist. It is harmless because κ = 7 is treated separately.
- **F6 (statement).** lem:refine needs the designated coefficient of 𝒩 to have D-class 0, but this
  hypothesis appears only inside the proof and rem:designated. It belongs in the statement of the lemma and of
  cor:chain.
- **F7 (scope).** "Attained exactly at 13, 19, 37, 73" is a property of the schedule as defined, Tier-B list
  included. With Tier B at all p ≤ 523 the set is the same; with no Tier B the maximum becomes 27 (at 181).

## Adversarial self-check

- **Shared assumptions.** My implementation was written from the same fragment, so a conceptual error in
  the fragment (for example in lem:refine) would be reproduced, not caught. The executor checks outputs
  against the definition of a κ-solution, independently of the lemmas, but only on finite banks and small a.
- **Exhaustive NONE.** These rest on rcsearch's DFS, which agrees with the brute force only up to r = 3–6 at
  tiny p. The Z_9 cases at p ≈ 300–523 are not brute-force-checked. They affect only the lower bounds at
  p ≤ 523, not the maxima, because the maximisers are tiny primes where everything was checked.
- **Gap range.** In 4·10^5–2·10^6 I searched certificates only where a missing one could change a maximum or
  the attainment set. That is sufficient for the stated claims, but not a full per-prime table.
- **Shared ξ.** My cross-check of the helper used its `rule.py` with its certificates. Agreement shows the
  two codes compute the same function, not that the definition is the intended one. Both use the least
  primitive root as ξ. Results for another ξ were not computed (degrees could in principle depend on ξ at small p).
- **Roots.** The executor's roots come from tables, so the Las Vegas root-finding path is not exercised.
- **Nothing promoted.** "AI-checked, pending human review"; no theorem is upgraded by these checks.

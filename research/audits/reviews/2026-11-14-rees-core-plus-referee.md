# Hostile referee: core write-up of Schedule 1H+ and the headline 20 (2026-11-14)

AI only (one Claude Code referee agent), pending human review. Target:
`docs/papers/rees-hsp/core/main-core.tex`, read at about 08:45. Its sec:plus was byte-identical to
`2026-11-14-rees-schedule1hplus-draft/sec-schedule1hplus.tex`, and all 55 snippet edits of `edits.md`
were present (R6 was pasted, not `\input`); `numbers.tex` had `\ReesClassNinePlusExp{20}`.

- No existing file was edited. There were no Git commands and no network use.
- Scripts and outputs are in `research/audits/reviews/2026-11-14-rees-core-plus-referee/`. Every run used
  `nice -n 19`. The largest run took 131 s; the largest RSS was under 0.7 GB.
- `plus_mine.py` and `rcdfs.c` were written from the merged text only. I read no existing schedule
  script. I ran one existing binary, the recompute's `rcsearch`, as a black-box cross-check.

Labels: PROVED, PROVED given cited theorems, CONDITIONAL, REFUTED, UNKNOWN, NOT computed. Finite checks can
only falsify.

## Verdict: CORRECT WITH FIXES, plus one blocking file-integrity problem

**The mathematics.**
- E_+(c) = 3, 5, 9, 10, 14, 16, 18, 20 is reproduced by my own implementation, written from the text.
- The attainers of 20 are reproduced: the 260 primes ≡ 1 (mod 2520) below 2·10⁶, and 37, 43, 73, 127, 181,
  631.
- The old 38 is reproduced with the new candidates switched off.
- I found no error in any proof.

**Three fixes are material.**
- **F2. Repeated moduli.** A reader who takes the moduli of a chain to be strictly increasing gets **23**, not 20.
- **F3. The U_m gap list** is false as written per m.
- **F4. The "9 < p" range** in the proof of record is wrong for c ≤ 8.

**Blocking problem (F1).** The file was rewritten at **09:02:02** (md5 `3ccc5b99…`, 1778 lines, was 1469).
That version contains a spliced block of 309 lines, new lines ~1013–1322. In order, it holds:
- a second "Uniform Gate Compilation" section;
- a "Hybrid Error Composition" subsection, found nowhere else under `docs/papers/rees-hsp`;
- a "Black-Box Groups and UT_n(Z)" section that breaks off mid-proof into a partial second copy of sec:plus
  (Lemma plus-sm through Lemma plus-exponent).

`\label{def:plus-schedule}` now occurs twice. The 08:40 PDF predates this. It looks like another actor's
write collided with the file, or is still in progress. I did not touch it, and my review is of the pre-09:02
text. The integrator must restore the file: delete the inserted block, so that `% --- end Schedule 1H+ ---`
is followed directly by the original `\section{Uniform Gate Compilation ...}`, and recompile.

**Update after the report was written.** At 09:06 the file was back to 1469 lines (md5 `560e9f12…`).
`\label{def:plus-schedule}` occurs once, "Hybrid Error Composition" is absent, and the old snippets of F3, F4
and F6 are present at lines 953 and 997, as reviewed. So F1 looks resolved by whoever wrote the file. I did
not diff all 1469 lines against the 08:45 text, and the PDF still needs a recompile.

## (B) Own implementation of the arity recursion

**What `plus_mine.py` computes.** It implements Def. plus-schedule at the level of degrees and least constants,
for every odd prime p < 2·10⁶ and every κ ≤ 9 dividing p−1. It covers:
- candidates (a)–(e);
- plans over (f1), (f2) and (f3) with finishes F0, F1, (fΩ) and the chains of (d);
- the sets T_s for each ε = −ξ^{−m}, computed by class sumsets;
- t_{p,κ} by sumsets below 4κ⁴, and by Lemma zero-sum(ii)–(iii) above;
- ξ = g, the least primitive root.

**How availability is decided.**
- By the Lemma plus-sm thresholds above T_exist.
- By my exhaustive DFS (`rcdfs.c`, WLOG β₀ = 0, α₀ = 1) for every step at p ≤ 600, for every Tier B step,
  and at every prime that has no certificate.
- Otherwise by the saved certificates, each re-checked here against Def. plus-rc with power-test classes.
  All 75,391 checked: 0 bad, 0 missing.
- The DFS agrees with an unnormalised brute force in 15/15 small cases (`brute_rc.out`). It agrees with the
  recompute's `rcsearch` in 12/12 U_m cases (`ucheck_rcsearch.out`).
- At p = 307, three Tier B steps (9, Z₉, 3-element Ω) hit the node cap. With a cap of 3·10¹⁰ all three are
  NONE (`cap307.out`, about 1.15·10⁹ nodes each). So the run is exact, with 0 UNKNOWN.

**The five ℓ-tables** were checked against Def. plus-ell with C_y = g^{Σy}B(y):
- (i), (ii) and (iii) hold, with (iii) tested by contracting every axis with x ↦ (x_m − z_m x₀).
- Reading the stored values as C fails for all five, as G1 predicts.

**Results** (`run_full_2e6.out`, `run_var_2e5.out`, `run_30000.out`, `run_strict_30000.out`):

| variant | E(c), c = 2..9 | c = 9 attainers |
|---|---|---|
| full, p < 2·10⁶ | **3,5,9,10,14,16,18,20** | 266: the 260 primes ≡ 1 (2520) and 37,43,73,127,181,631 |
| new candidates off (= 1H), p < 30000 | **3,6,10,14,20,25,29,38** | 2521, 7561, 12601, 15121, 20161 |
| TL6 and (e) off, p < 2·10⁵ | 3,5,9,10,14,16,19,21 (as stated) | 13, 19, 37, 73 and the 2520 class |
| (a) removed at κ ≤ 9 (rem:plus-is), p < 2·10⁵ | same as full | same |
| no Tier B at all, p < 2·10⁵ | 3,5,9,12,17,19,22,**27** | 181 |
| Tier B with **strictly increasing** moduli, p < 30000 | 3,5,9,10,14,19,21,**23** | 43 |

**Other values reproduced.**
- The grade vectors at 13, 19, 37, 43, 73, 127, 181, 631 and 2521 match rem:plus-profile and the 20-referee.
  At 37 and 73, κ = 9 is candidate (e). At 631, κ = 6 is the plan over H⁺₃ with F1.
- E_+(8) = 18 is attained only at 29 and 43. E_+(4) = 9 is attained only at **p = 5**.
- The gap lists for TL3 (none), TL4, TL5, TL6 (53 primes, max 859) and TW are exactly as stated.
- The constants satisfy K⁺_κ ≤ c_κ at every prime p < 2·10⁶ and every κ ≤ 9. This recomputes Lemma
  plus-exponent(iii) for the merged schedule, which the drafter had not done.
- The degree differences between the "28-prime (d), no TL6, no (e)" variant and the full schedule occur only at
  κ = 4 at p = 13, at κ = 6 (at 13, at Tier B primes outside the 28, and wherever TL6 is available), and at κ = 9
  at 19, 37 and 73. This matches the hand argument of (iii) (`degree_change_d28_vs_full.out`).

**Thresholds** (`thresholds.out`, mpmath at 80 digits).
- Every T_exist, T_samp, p_D and 1−Φ(p_D) entry of tab:plus-thresholds is reproduced.
- The largest band constant is 3.37·10¹⁴, at U_m, below the stated 4·10¹⁴.
- The TL7, TL8 and TL9 values of rem:plus-profile are reproduced.

## (A) Line-by-line findings in sec:plus

**Proofs re-derived. PROVED, given Weil and Rabin where cited:**
- Lemmas plus-refine (including D′ = D), chain, plus-sm (second moment, Chebyshev, (2D)^r), plus-tensor,
  plus-ell-node, plus-stage and plus-finish;
- Theorem plus (i), (ii) and (iv): totality, Las Vegas, no failure report, the cost recursion, 11 searches,
  35/8 trials and 8/35;
- Lemma plus-exponent(i), the new lower bound, by hand: 19 + (⌈c/2⌉² − 25) + 2(⌊c/2⌋ − 4), plus 1. PROVED,
  given Dirichlet.

**Material fixes.**
- **F2 (could a reader implement it?).** The deciding moduli convention is implicit. Cor. plus-chain writes
  D₀ | D₁ | ⋯ | D_L, and Lemma plus-refine allows D′ = D. So repeated moduli are allowed, and they are what
  gives 20:
  - at p = 43, e⁺₇ = 4 comes from (GE; (7,Z₇,{0,1,2}); (7,{0,1,2},{0,2})) under the plan (s=1, F1);
  - strict moduli give e⁺₇ = 7, 7, 7 at 29, 43, 113 and E_+(9) = 23.

  Fix in Def. plus-schedule(d):
  - old: `whose moduli $D_1 \mid \cdots \mid D_L = \kappa$ divide $\kappa$`
  - new: `whose moduli $D_1 \mid \cdots \mid D_L = \kappa$ divide $\kappa$ (consecutive moduli may be equal; at $p = 43$ the degree $e^+_7 = 4$ uses the chain $(\text{Gaussian elimination};(7,\mathbb{Z}_7,\{0,1,2\}),(7,\{0,1,2\},\{0,2\}))$ as the node of a plan)`
- **F3 (proof of plus-exponent(ii), false per m).** By my DFS and an independent `rcsearch`, U₁ and U₆ are
  also unavailable at 71 and 197, U₃ and U₄ at 71, and U₂ and U₅ at 127. The numbers are unaffected, since
  the union over m is used.
  - old: `and $29, 43, 113$ for $\mathrm{U}_m$, for every $m$.`
  - new: `and, for $\mathrm{U}_m$, $29, 43, 113$, at which no $\mathrm{U}_m$ exists for any $m$ (for a single $m$ there are more: $\mathrm{U}_1$ and $\mathrm{U}_6$ fail also at $71$ and $197$, $\mathrm{U}_3$ and $\mathrm{U}_4$ at $71$, $\mathrm{U}_2$ and $\mathrm{U}_5$ at $127$; elsewhere a certificate exists for some $m$).`
- **F4 (proof of plus-exponent(ii)).** The c ≤ 8 values need p = 3, 5, 7. E_+(4) = 9 is attained only at 5,
  and E_+(6) = 14 at 7 and 31.
  - old: `for every prime $9 < p < 2\cdot10^6$`
  - new: `for every odd prime $p < 2\cdot10^6$`

**Minor fixes.**
- **F5 (Thm plus(iii) proof).**
  - old: `For $p \ge 2\cdot10^6$ the candidates and their constants do not depend on $p$`
  - new: `For $p \ge \max(2\cdot10^6, 4\kappa^4)$ the candidates and their constants do not depend on $p$`
  - Reason: for κ ≥ 10, plan admissibility depends on p below 4κ⁴. The finiteness conclusion is unchanged.
- **F6 (after Def. plus-schedule).**
  - old: `The definition is complete as stated; the artifacts (Appendix~\ref{app:artifacts}) contain only the five tables of Proposition~\ref{prop:plus-tables}, and certificate tables`
  - new: `The definition is complete except for the five tables of Proposition~\ref{prop:plus-tables}, which candidate~(e) reads as data (stored keyed by the digit string $y_1\cdots y_\ell$, and checkable against Definition~\ref{def:plus-ell}); the other artifacts are certificate tables`
- **F7 (rem:plus-profile).**
  - old: `which Lemma~\ref{lem:plus-sm} provides only above`
  - new: `which Lemma~\ref{lem:plus-sm} guarantees only above`
- **F8 (tie rule).**
  - old: `ties being broken by a fixed order`
  - new: `ties being broken by any fixed order (which affects the candidate run, not $A^+_\kappa(a)$)`
- **F9 (plus-exponent(iii), garbled list).**
  - old: `changes degrees only at $\kappa = 4$ and $\kappa = 6$ at $p = 13$, at $\kappa = 6$, and at $\kappa = 9$ at $p = 19, 37, 73$`
  - new: `changes degrees only at $\kappa = 4$ at $p = 13$, at $\kappa = 6$ (at $p = 13$, at primes $p \le 523$ outside the $28$, and where $\mathrm{TL}_6$ is available), and at $\kappa = 9$ at $p = 19, 37, 73$`
  - Optionally add: "recomputed directly for the merged schedule: $K^+_\kappa \le c_\kappa$ at every $p < 2\cdot10^6$ (2026-11-14 referee)".

## (C) Global consistency

**Consistent.** These were all checked:
- the abstract (20);
- thm:main(3)–(4), and the "In particular" lines for 20, 38 and 53;
- the paragraph after the theorem: the lower bound, the imports, and "four primes p ≤ 73";
- rem:main-solver: 145, 95, and the scope of the confirmation;
- rem:is-import(d): n_pre ≤ 2(c−1)+12 and 11 searches;
- Verification Status;
- proof-main: the query count and the preprocessing time;
- the Heisenberg and class-3 examples;
- tab:query-crossover;
- rem:query-separation(b);
- the outlook: "below the conditional value 37", "by itself gives 38", and 95 with "1H⁺ not computed";
- the Artifacts list.

**Numbers recomputed.**
- The class-3 count is 3·6·16·15 = 4320 = 2^{12.08}. The 1H value 2^{17.68} and the Schedule 1 value
  2^{23.68} also check.
- Table rows: 5.00 / 9.66 / 12.08 / 13.31. LB primes 29 / 79 / 61 / 17. (v) thresholds 27 / 28 / none, and
  28 / 29 / 11 with 8ℓ. Copies 50 / 108 / 153 / 269.
- The class-9 row is kept as a 1H upper bound, and the caption says so.
- No sentence states 38 as the headline. The statements of 53, 145 and 95 are unchanged and correct.

**Remaining fixes.**
- **F10 (rem:is-printed).**
  - old: `It does not cover the shorter depth, the halving of Section~\ref{sec:halving}, or the exponents $\ReesClassNineQueryExp$ and $\ReesClassNineHalvedExp$ at $c = \ReesClassNineClass$.`
  - new: `It does not cover the shorter depth, the halving of Section~\ref{sec:halving}, Section~\ref{sec:plus}, or the exponents $\ReesClassNineQueryExp$, $\ReesClassNineHalvedExp$ and $\ReesClassNinePlusExp$ at $c = \ReesClassNineClass$.`
- **F11 (style, outlook "Halving at the confirmed depth").** The two consecutive parentheticals should be merged.

## (D) rem:free23 against the free23-all-subgroups referee

**No overclaim.** The remark reflects the referee's fixes:
- fix 2: the exact QFT is assumed, and the approximate-QFT caveat is stated;
- fix 3: Theorem 5 is cited as a sketch, the right-versus-left coset convention is noted, and the query count is
  polynomial in log p rather than O(1);
- fix 4: the candidate is checked by a query;
- fix 5: the cutoff is stated.

**Claims checked against the note and the referee.**
- The error cases: hard cyclic, and IS types 8 and 10.
- s(p) ≥ (1−3/p)²(1−1/p), which is 0.128 at p = 5.
- About 4200 copies, at p = 7.
- "No automorphism preserving H".
- The scope statements.

**One addition (F12).** Fix 1, the small-p reliance on reading Lemma E as a formal identity, is stated only in
the Appendix. After `given the cited theorems named below;` add: `for small $p$ the bound $s(p)$ also rests on
reading one derivation of the notes as a polynomial identity, which a human should check;`.

## Adversarial self-check

- **My DFS and `rcsearch` use the same normalisation** (β₀ = 0, α₀ = 1), and their node counts agree, so they are
  not fully independent. Brute force without the α₀ normalisation agreed only on small cases. The WLOG is
  proved (translation, then P_D-scaling).
- **Certificates are the authors' data.** Every one used was re-checked. Above 600, availability for a given m
  of U_m was not decided when the certificate's m sufficed. That is enough for degrees, since 3 is the lower
  bound at κ = 7 for p > 523, but it does not give per-m gap lists above 600.
- **"Attained exactly" holds for the schedule as defined**, and F2 shows how sensitive it is to the reading of
  the definition. "≤ 20" is the robust content.
- **Lemma plus-sm and Weil.** I reproduced the formulas; a wrong lemma would be reproduced too. Weil's locator
  is still unverified by a human.
- **The 09:02 file.** My review is of the 08:45 text. I did not re-review whatever the 09:02 writer intended.
- Everything here is AI-checked, pending human review. No claim gate was changed.

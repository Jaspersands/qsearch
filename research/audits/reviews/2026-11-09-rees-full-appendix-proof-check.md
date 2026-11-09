# Rees HSP full version: appendix-by-appendix proof check (9 Nov 2026)

AI-only (Claude Opus 5.5: one coordinator, 12 checker subagents). Nobody has done a human
review. This check edited no paper file, no file in the prep tree and no claim gate, ran no git
command and contacted no one. Finite checks can only falsify.

**Object checked.** The integrated local prep tree
`research/audits/reviews/2026-11-09-rees-paper-pass-prep/tree/` (all passes 1-7 applied; 209 pp.).
SHA-1 prefixes: `main.tex` 0ed1a1f82b13; appendices: schedule2 8abf0e08ebeb, schedule3
4966e7646cc5, free-coordinate ec9ab51739f4, subspace f8553ee2c647, torsion-blackbox
0f89bd238639, codimension 844ef46f6487, sde-side 9b7379e908ca, backends 020a873804d1, filters
fc8a2ac43259, provenance 2545e44aeb3f. The hashes did not change during the check.

**Method.**
- There were 12 parallel checkers, each briefed only with its part, the main-text statements
  it proves, and `main.tex` ll. 161-388 (contract, results, notation). The shared brief is
  `2026-11-09-rees-full-appendix-proof-check/BRIEF-COMMON.md`.
- Schedule 2 and the torsion/black-box appendix were each split in two. A twelfth checker made
  an independent check of the new `prop:dl-central-scalars`.
- Each checker did its own line-by-line pass and tried counterexamples. It ran exact checks under
  `nice -n 19 timeout`, and read the 3-5 Nov reports only afterwards.
- `diffs/` holds the change diffs used: every change since the 5 Nov 09:20 archive, and the
  9 Nov patch split by file.
- Compute was about 1.8 core-hours in all (reported per checker; under the 4 h cap), single-threaded at nice 19.
- **The coordinator re-verified every GAP and ERROR below against the .tex (and against local
  source texts where a citation was at issue).** "V" marks a finding re-derived or re-read by the
  coordinator. "R" marks one taken from the checker's script output and checked only for
  plausibility.
- Per-part reports, with exact replacement LaTeX for every fix, are in
  `2026-11-09-rees-full-appendix-proof-check/<id>.md`, with scripts and outputs in `<id>/`.

## 0. Summary

**No BREAK.** No stated theorem, proposition, lemma or corollary was found false, and no
counterexample was found to any of them. The verdicts:

| Part (checker id) | Verdict | GAP | ERROR | MINOR |
|---|---|---|---|---|
| Schedule 2, ll. 1-482 (s2a) | MINOR ONLY | 0 | 0 | 8 |
| Schedule 2, ll. 483-729 + worst-case Theorem main (s2b) | GAPS | 1 (same as t2-1) | 2 | 6 |
| Schedule 3 (s3) | GAPS | 1 | 0 | 6 |
| Free coordinate (fc) | MINOR ONLY | 0 | 0 | 6 |
| Subspace sources (sub) | GAPS | 1 | 0 | 11 |
| Torsion/black box, ll. 1-547: Lazard, ring-to-field (t1) | MINOR ONLY | 0 | 0 | 8 |
| Torsion/black box, ll. 548-1582 + `thm:bb-envelope`, corollaries (t2) | GAPS | 1 | 1 | 7 |
| Codimension (codim) | MINOR ONLY | 0 | 1 | 5 |
| Filters + backends (fb) | MINOR ONLY | 0 | 1 | 11 |
| SDE side (sde) | GAPS | 2 | 4 | 7 |
| Provenance (prov) | MINOR ONLY (record errors) | 0 | 3 | 9 |
| `prop:dl-central-scalars` and its citing sentences (dl) | MINOR ONLY | 0 | 1 | 5 |

Totals: 5 distinct GAPs (t2-1 = s2b-1); 13 ERRORs, 12 distinct (sde-5 = s2b-2); 89 MINOR.

Severity scale:
- **GAP:** a proof step is missing or wrong, but the statement survives with a stated repair of
  a line or two.
- **ERROR:** a false sentence that does not affect any stated result.
- **MINOR:** wording, notation, status labels.

The most material items are these:
1. **t2-1 = s2b-1 (GAP).** Two checkers found this independently: t2 from the black-box side,
   s2b from the worst-case side. The "on every branch" bounds of `thm:bb-envelope` have no
   argument on the chart-failure event. There the chart may be non-nilpotent or of class above
   c, which neither `rem:oblivious` nor the time-out covers. Fix: check γ_{c+1} = 0 and the Lie
   axioms.
2. **s3-1 (GAP).** `cor:fpt-r` and its Schedule 3 route use "c ≤ r+1", which needs the true
   class. The contract's c is only an upper bound. Fix: replace c by the computed class.
3. **sub-1 (GAP).** `cor:subspace-hsp` claims polynomial cost in log p for any certified design,
   while offering S = F_p^× (T ≥ p−1). Fix: restrict the claim to the design of
   `lem:app-sub-design`(b).
4. **dl-1 (ERROR).** Contribution (1)'s "no automorphism of G supplies central scalars beyond
   ±1" is false for p ≡ 1 mod 3 in the paper's own sense of "central scalars". A ℤ/3-grading of
   L_DL acts on exp(F_p e7) by a cube root of unity. The proposition itself, a scalar on the
   whole centre, is correct.
5. **sde-1, sde-2 (GAP).** Two results are called proved or stated as fact with no proof in the
   paper: the composite-κ run bound, and the sparse count (1−1/p)a²/2.
6. **sde-3, sde-4, sde-5, s2b-2, s2b-3 (ERROR).** False or stale sentences:
   - in the SDE survey at main.tex:750;
   - in the κ = 8, 9 sentences at main.tex:695 and :721 and appendix-schedule2.tex:723 and :728.

   The E_2 items must be fixed together in the planned E2-UPDATE pass.
7. **prov-1, codim-1, t2-2, fb-1 (ERROR).** Stale or false record and side sentences.

**The 9 Nov worst-case argument survives.** s2b checked the Schedule 2 / combined-rule claim:
- per attempt: Markov at 4T plus abort ≤ 1/4 at k = 2;
- independence across attempts, with Phase 0 inside each attempt;
- the recursion tree fixed by (p, m, g_d, ε);
- labels ≥ p reduced mod p;
- hiding used only for correctness.

It found it correct, and none of the oracles it tried gives an unbounded or uncounted cost. The
one hole is not in the oracle model but in invalid charts (item 1). `cor:black-box-pe` is
unaffected, because its K' is ideal-checked.

## 1. Schedule 2, lines 1-482 (s2a): MINOR ONLY

`thm:app-s2-main` was checked "on any columns", with J = κ(k+3) and K_j = ⌈2κ^{j+1}τ⌉. Worst-case
time is bounded, the output is never wrong, and the abort probability is ≤ 0.75·2^{−k}.
- An independent implementation made 1110 adversarial runs with 0 wrong outputs.
- Every entry of `tab:app-s2-thresholds` for κ = 2..9 was recomputed (60 digits,
  interval-bracketed) and matches.
- T_W and T_A are proved.
- An independent exact search reproduces E_2(2)..E_2(5), and the all-nonzero variants.
- The main-text statements (`thm:power-sde`(ii), `prop:decoupled-sde`, E_2,
  `rem:combined-schedule`, the exponents 107 at c = 8 and 143 at c = 9) match the appendix.

Findings:
1. MINOR (V), `appendix-schedule2.tex:434,438` (`prop:app-s2-barrier`(iii) proof).
   - "η_m < 1 forces m ≤ κ−2" is false for m > p, where p−m < 0 makes η_m negative; at
     m = p, η_m is undefined. The statement is still true there, because
     binom(rh,m) = 0 = E binom(M_S,m) when m > rh = p−1.
   - "p ≥ 7" is not implied: κ = 4, p = 5 satisfies the hypotheses. The bound used still holds
     there: (9/16)(m'²/κ^{m'})p^{−3/2} ≤ 0.013 ≤ 0.02.
   - Fix: restrict η_m to 1 ≤ m < p and treat (κ,p) = (4,5) explicitly (s2a.md §1).
2. MINOR (V), `:115`. "χ(ξ) = ω" does not determine χ, because ξ only generates F_p^×/Q_0.
   Example: p = 13, κ = 2, ξ = 8 admits characters of order 6. Fix: add "trivial on Q_0".
3. MINOR, `:11`. The status line's "exact checks of every claim" overstates what finite checks
   do.
4. MINOR, `main.tex:726` (`rem:two-level-threshold-size`). "The same Weil-controlled moment
   brackets" omits the restriction η_m < 1 that the barrier needs.
5. MINOR, `main.tex:695` (Terms). The witness step is said to give a solution of the target
   directly; the Bezout conversion is missing.
6. MINOR, `:189`. The Phase 1 cut-off T_1 should be an explicit, computable bound. This is
   linked to s2b and t1-F1: see §13(c).
7. MINOR, `:215` (`prop:app-s2-TW`(ii)). τ is not quantified; "probability e^{−τ}" should read
   "at most e^{−τ}".
8. MINOR, `:13`. The appendix assumes a ≥ 1, while g_d = 0 can occur in the main text. This
   is trivial to cover.

Earlier report (`2026-11-03-rees-check-app-a.md`): all of P1-P8 are present.

## 2. Schedule 2, lines 483-729, and Theorem main on every oracle (s2b): GAPS (statements survive)

**Part 1 (appendix ll. 483-729).** Exact searches (`s2b/rcsearch*.out`, `counts.out`,
`numerics.out`, `cyclo.out`) found no error in the tower, chains, local-obstruction or scope
statements, within the ranges searched (UNKNOWN items are listed below).

**Part 2 (the 9 Nov claim).** This covers `sec:recursion` `main.tex:608-644`, `rem:oblivious`
`:1048`, the status of `thm:bb-envelope`, and `main.tex:1225`. The claim is correct in substance:
- **Per attempt.** Markov at the 4T cut-off gives ≤ 1/4, Schedule 2 at k = 2 aborts with
  probability ≤ 1/4, so an attempt fails with probability ≤ 1/2. Outputs are checked exactly, so
  an abort costs only probability.
- **Across attempts.** Attempts fail independently given the node's columns, because Phase 0 runs
  inside each attempt; a shared Phase 0 would cause a common failure of up to 1/16. With
  ⌈log₂(3N/ε)⌉ attempts and a union over nodes, the solver third is ε/3.
- **Fixed before the run.** Tree, arities, transform counts, N_solver and N_instr are fixed by
  (p, m, g_d, ε), with no restarts.
- **Hiding.** It is used only for correctness.
- **Oracle attacks tried; none succeeded:** labels ≥ p; zero, repeated and rank-deficient
  columns; non-hiding f in the rank steps; f maximizing late stop-rule firing.
- **Corollaries.** Dropping the time-out is valid for `cor:black-box-pe`.

Findings:
1. **GAP (V)**, the same gap as t2-1 (§7), found independently.
   - Locations: `main.tex:1329`, `:1310`, `:1049`, `:1225`; torsion appendix `:402-404`,
     `:442-446`, `:838-840`, `:1203-1207`, `:1308`, `:1387`, `:1445`.
   - The argument: `rem:oblivious` covers only in-contract inputs, but `thm:bb-envelope`'s (R2)
     chart on the `lem:tb-kernel` failure event can be a Lie ring that is not nilpotent.
   - Example (`s2b/chart_example.py`): Heisenberg, c = 2, e_p = 1, with [ε1,ε2] = ε1−ε2. The
     coordinator checked that this example is non-nilpotent: ad_{ε1} has eigenvalue −1 on ε1−ε2.
   - The analogy "exactly as `cor:black-box-pe` argues" does not carry over, because the
     corollary's F/K' is ideal-checked and `thm:bb-envelope`'s chart is not.
   - Fix: antisymmetry, Jacobi and γ_{c+1} = 0 before each call, O(cℓ^6) ring operations in
     all, below the existing O(ℓ^8) term. After the fix, (i), the status line and `main.tex:1225`
     follow: beyond `thm:is-import`, only `thm:power-sde`(ii) through the combined rule.
2. **ERROR (V)**, `appendix-schedule2.tex:723` and `main.tex:721`. "By separate runs above the
   decided ranges, 14281 ∈ E_2(8)" is stale: 14281 < 16993. The phrase dates from when the range
   ended at 13873. This is the same as sde-5.
3. **ERROR**, `appendix-schedule2.tex:723/728` and `main.tex:695/721`.
   - The new 9 Nov sentence says the constraint solver decided "the 145 primes p ≡ 1 (mod 8)
     in (9769, 20000] that the pruned search had not decided on 4 November". If it decided them
     all, E_2(8) is determined.
   - That contradicts "not known exactly", "In (16993, 20000] only some primes are decided",
     "Above those ranges most verdicts rest on a single run" (not flagged by an E2-UPDATE
     comment) and "does not determine E_2(κ) for κ ≥ 8".
   - "Re-decided, with the same verdicts" is meaningless for primes with no earlier verdict.
   - Fix all five places together in the E2-UPDATE pass (text in s2b.md §3).
4. MINOR, appendix `:189`, `:162`; `main.tex:620`, `:1049`.
   - The cut-off bounds T_1 and T exist only for a fixed implementation, with constants not
     computed. `rem:oblivious` says so for T; the proof of `thm:app-s2-main` does not say so for
     T_1.
   - The stated time is worst-case only if a uniform draw from F_p counts as one step; with fair
     coins, each rejection loop is unbounded.
   - Fix: cap each loop at k+2+⌈log₂ N_0⌉ tries. The abort bound stays ≤ 2^{−k}.
   - Inside the recursion the 4T cut-off already covers this, so Theorem main is unaffected.
5. MINOR, `main.tex:1312`, torsion `:1581`. "The Schedule 2 calls are not bounded here" is
   outdated: they are bounded by the unspecified polynomial of `rem:oblivious`, and only the
   exponent β̂_c is missing.
6. MINOR, `main.tex:625`. "Fixed before the run under Schedule 1" also holds under the combined
   rule.
7. MINOR, appendix `:647`. The "1 < D_1 < κ" sentence omits κ = 7 (primes 43, 113).
8. MINOR, appendix `:541`. "1 − 1/ρ" should be "1 − 1/ρ_2".
9. MINOR, appendix `:487/563/573/591`. k means |K|, an element of K, and the round index.

Not checked or UNKNOWN:
- κ = 9 at 163 and 181 (partial: 15 and 12 of 37 constructions hit the node limit);
- κ = 9 at 199, 307 and 433 (not run);
- chains with 1 < D_1 < κ for κ = 9 and κ = 8;
- the κ = 7 list {29, 43, 71, 113}, which needs E_2(7);
- κ = 10, 12 (timed out at 200 s);
- κ = 3 symmetric form above 400;
- T_R(9,3) ≈ 134723 against the search bound 135000, evaluated in floating point only: margin
  0.2%, so an interval evaluation is advised.

## 3. Schedule 3 (s3): GAPS (statements survive)

1. **GAP (V)**, `appendix-schedule3.tex:316` ("Application to `cor:fpt-r`") and `main.tex:1167`
   (proof of `cor:fpt-r`).
   - The step "c ≤ r+1" follows from g_2 > ... > g_c ≥ 1, which needs γ_c(L) ≠ 0. But
     `def:input-contract`(i) promises only "class at most c".
   - Counterexample: the Heisenberg algebra (r = 1) given with c = 5 and p = 67 is a valid
     instance with c = 5 > u = 2, so `thm:free-coordinate`(iv) does not apply as written. The
     bound (4αc)^{c−1} of `cor:fpt-r`(i) is likewise in terms of the given c.
   - Fix, in both places: "replace c by the true class c' ≤ c, computed from the structure
     constants by linear algebra". This is harmless, since p ≥ c+2 implies p ≥ c'+2, and when
     p = c+1 > c'+1 the case falls under (i).
2. MINOR, `:43`. The dependency list cites only the gate counts of `thm:uniform-compilation`,
   but its part (iii) is also used for correctness (ll. 258, 285). The mixed-schedule list also
   omits `thm:is-import`.
3. MINOR, `:258` (`lem:s3-hybrid`). The list of ideal steps leaves out lifted-source
   preparation and the final Fourier readouts. Both preserve the canonical subspace, so there is
   no gap.
4. MINOR, `:110`, `:120`, and `appendix-schedule2.tex:487`.
   - q = p^{−a} clashes with the main text's q = (h+1)/p.
   - `appendix-schedule2.tex:487` credits q = (h+1)/p to this appendix.
   - |𝒟| is used before it is defined.
5. MINOR, `:293`, `:314`. "c appears only in ..." is too narrow: c also enters B, the queries
   per leaf and the BCH cost. All are bounded by u.
6. MINOR, `main.tex:784`. "Supersedes that trial count" fails when the stated caps are
   compared: at κ_d = 1 with u ≥ 3, and at κ_d = 2 with u = 20 (59 pairs for u ≤ 40). It holds
   node by node; replacement text is in s3.md.
7. MINOR, small items.
   - `prop:s3-uniform`(d),(e) do not cover coset-copy input.
   - A source comment at l. 16 says "7+" where the text says 6+.
   - Reused symbols K, B, S, L, R.
   - The table caption does not state its rounding convention.

Earlier report (`2026-11-03-rees-check-app-b.md` §§1-3): P1-P10 are present. P2 is still
incomplete (finding 2). The earlier report missed finding 1.

## 4. Free coordinate (fc): MINOR ONLY

Every lemma and proof in `appendix-free-coordinate.tex` checks out, as does
`thm:free-coordinate`(i)-(iii). The recomputed numbers all match:
- all six rows of `tab:fcs-budget`, the part (ii) caps and the j*_h depths;
- the maxima of E for c = 2..9;
- the Jacobi bound on 2250 pairs (p,κ);
- the exact σ_p for p ≤ 19.

The weight-doubling solvers were simulated with exact output checks. The MP13 Thm 1.1
citation was checked against the local author copy (`2026-11-02-rees-linear-arity/lit/mp13_LWsE.txt`)
and is right in its parameters, norm bound and modulus.

1. MINOR (V), `:294` (`rem:fc-zero-sum-arity`(a); used at `:296` and `:317`).
   - σ_p ≤ ⌈2log₂(p−1)⌉+4 is "imported". KMOSW26 Prop. 5.3 (local text
     `lit/arxiv_2609.40321.txt` l. 1675 ff.) states only a tail bound, failure ≤ q²/2^B, for a
     different object. Yet the node labelled "proved" needs the bound for p ≥ 13.
   - Repair, re-derived by the coordinator: the 2^b − 1 nonempty subset sums are pairwise
     independent and uniform. Chebyshev and a union bound give Pr[T > b] ≤ (p−1)²/(2^b−1), so
     σ_p < ⌈2log₂(p−1)⌉ + 3. Text is in fc.md.
2. MINOR, `:279` (`rem:fc-zero-sum-sis`). "The average case of BIS_p" is loose: GKSZ Def. 6.1
   needs ≥ (g_d+1)(p−1) columns, which is p−2 more than the node's arity.
3. MINOR, `:244`. "A tree that uses it must add S n_d τ_d" should say "a run".
4. MINOR, `:506` (proof of `prop:fc-split`). The abort sum should run over Γ_F ∪ Γ₀ when the
   optional Γ₀ node is used. `:319` should say the Γ₀ node contributes ≤ τ_d. The bounds are
   unchanged.
5. MINOR, `:376`. The Scope paragraph omits the κ_d = p−1 node of `rem:fc-zero-sum-arity`(b).
6. MINOR, notation.
   - log(1/τ) vanishes at τ = 1: use log(2/τ) at `:296` and `:317`.
   - N is used for two things.

Earlier reports: every fix is present, including the removal of `thm:random-column`.

## 5. Subspace sources (sub): GAPS (statements survive)

Every recomputed number matches the paper:
- the no-recovery leaks 1/2 and 2/3;
- the falsifiers 1.732 and 1.902;
- the streaming tails and the whole p = 43 profile.

The LCU precision clauses are stated against the right objects.

1. **GAP (V)**, `main.tex:1380` (`cor:subspace-hsp`) and `appendix-subspace.tex:360/380`
   (`thm:app-sub-hsp`(iii)).
   - "For fixed c this is polynomial in m, log p, ..." is claimed for any certified design S of
     M points. The corollary itself offers S = F_p^× with M = p−1, which makes T = Mℓ B_leaf
     ≥ p−1 raw copies, exponential in log p.
   - The proof covers only the design of `lem:app-sub-design`(b) (M ≤ (c+1)!).
   - Origin: P5 of 3 Nov fixed the proof only, and referee 11's I5 then added the F_p^× option.
   - Fix: "for the design of Lemma (b) (M ≤ (c+1)!), this is polynomial ...".
2. MINOR, `main.tex:1363`. "Up to the phase det(R(g)|_V)" is undefined for g ∉ H.
3. MINOR, `main.tex:1363`. The recovery is W^†, not "the inverse of the LCU preparation".
4. MINOR, `main.tex:1358`. T and β are used before they are introduced. "Added here" assumes
   that Bene Watts et al. lack the recovery step; this is unchecked (§14).
5. MINOR, `main.tex:1380`. The precision clause omits the growth-attempt precision ε/(8TN).
6. MINOR, `main.tex:1344`. The r > 1 motivation ("distinct cosets give non-orthogonal states")
   is inaccurate.
7. MINOR (V), `appendix-subspace.tex:395`. The off-domain distance k/(k+1) holds for k ≥ 2; at
   k = 1, P_1 = I and the distance is 0.
8. MINOR (strengthening), `:257`. The leak without recovery is exactly (k−1)/k for every r, d,
   retained state and completion of J. This was derived and checked numerically.
9. MINOR. In `rem:mixed-source`, β and ε are undefined, and γ and J clash with other uses.
10. MINOR, `main.tex:1385`. It duplicates 1383.
11. MINOR. b over-provisions by p^{n/2}; this is slack only.
12. MINOR. `lem:app-sub-lcu`'s gate count omits the sign gate.

Earlier reports (`2026-11-03-rees-check-app-c.md`; referee 11): P1-P4, P6-P8 and P10 are
present, as are I1-I7, I13, S1 and S2. P5 is incomplete (finding 1). P9 (optional) was not
adopted; it was re-derived and is correct. G1 is still open.

## 6. Torsion/black box, lines 1-547: Lazard over ℤ/p^e and ring-to-field (t1): MINOR ONLY

Exact checks:
- The inverse-BCH words are exact for c = 1..6.
- 235 tests on GAP groups of order 3^4..5^5 found 0 failures; a negative control failed as it
  should.
- `prop:tb-recursion` was run on all 2021 Lie subrings of 10 rings with real coset oracles:
  9671 hiding checks passed, and no branch of 2970 adversarial branches made more than b calls.
  Three deliberately broken variants failed as predicted.

1. MINOR (constructivity), `appendix-torsion-blackbox.tex:392-398, 411-412, 424-427, 441-446`;
   `main.tex:1211`.
   - The time-out needs T_Solve as a computable function. For Solve = Theorem main the constant
     C_1 is never computed (`rem:is-runtime`), so the 9 Nov sentence "for Solve = Theorem main
     the time-out is not needed (`rem:oblivious`)" is needed, and it is correct on valid charts.
   - For Solve = part (ii) (`cor:fpt-r`), only the existence claim survives, because those
     constants are not computed either.
   - The definition also says T_Solve depends "only on the dimension", while Theorem main's
     bound depends on the g_d (bounded by m), and part (ii)'s on the derived dimension.
   - Text is in t1.md. This interacts with t2-1: see §13(c).
2. MINOR, `:402`. "Theorem main is stated for class c" should say class at most c.
3. MINOR, `main.tex:1203`. The example needs 2 ≤ e < p (at e = 1, R = 0). At `:1227`, class
   R+1 is reached by Heis_3(ℤ/p²) but not by the [x,y] = py families.
4. MINOR, `:126-130` against `:154`. `lem:tb-words` uses identities in Λ_{R_c}(X,Y), which is
   neither of the stated settings.
5. MINOR, `:218-220`. The proof uses log G = L without pointing to Lazard's uniqueness clause.
6. MINOR, notation.
   - b has three meanings and j two.
   - "Lie ring over A" should be "Lie algebra over A".
   - ℤ_p and ℤ_(p) are mixed.
   - Three cited works have no bib keys.
7. MINOR (for the expert), `main.tex:1219`. Is "is this paper's" fair to Ivanyos-Sanselme-Santha
   (ISS)?
8. MINOR, `main.tex:1211`. The call-count sentence also needs stop rule 1, and "known part of H"
   is wrong on branches where an earlier call erred.

## 7. Torsion/black box, lines 548-1582, with `thm:bb-envelope` and both corollaries (t2): GAPS (statements survive)

`cor:black-box` and `cor:black-box-pe` hold.
- No error was found. The e = 1 and e > 1 paths each stay within ε.
- Their public checks (the ideal check on K', the exponent test) make every chart a valid
  instance.
- `lem:tb-chart` Step 3 is correct as now written. The mod-p scan of the 3 Nov report fails on
  C_9 × C_3 in 198 of 198 runs, which confirms that the fix was needed.
- These were checked against brute force: the Howell primitives, (N1)-(N6) with RtF, the GAP
  count (49 of 58 groups), the E_W values, and 958 of 960 readouts.

1. **GAP (V for the text, R for the examples; found independently by s2b, §2)**: "on every branch" in `thm:bb-envelope`
   (`main.tex:1310`, `:1329`; appendix `:1196-1207`, `:1381-1383`, `:1445-1448`).
   - **What fails.** On the failure event of `lem:tb-kernel`, the rows of Y generate only a
     subgroup of (ker π)^⊥, and with approximate transforms they can be anything.
     `lem:tb-chart`'s guarantee is stated only on the success event, but it still outputs
     structure constants. They can define a non-Lie, non-nilpotent or class > c algebra.
   - **Checks.** For e_p = 1 the core call is made with no check (unlike `cor:black-box`,
     which checks that K' is an ideal of F_{s,c}). For e_p > 1 only the Lie axioms are checked,
     and the text says "possibly of class above c ... whose running time the time-out bounds".
   - **Why the cited bounds don't apply.** `rem:oblivious` is stated for every f on a valid
     instance, not for invalid structure constants. The time-out is not computable for
     Solve = Theorem main (t1-1). So no stated argument bounds a call on such a chart.
   - **Examples** (t2/failure_example.out):
     - e = 1, p = 5: Y = [[2,2,1,0,0],[0,2,2,0,0]] gives [ε0,ε1] = 3ε0+ε1. The coordinator
       checked that this is non-nilpotent: ad_{ε0} fixes [ε0,ε1].
     - e = 2: a chart passes the Lie check and is not nilpotent.
     - 2411 of 11664 RtF calls on such charts receive a socle of class > c.
   - **Effect.** Correctness and the error split are unaffected, since this happens only on the
     failure event. The query bound very likely still holds, because the recursion tree is fixed
     by public data, but no argument in the paper says so.
   - **Fix.** Check before any call, for every p > c: the Lie axioms and γ_{c+1} = 0 (c rounds of
     brackets, O(c·m^5) ring operations; it never fires on the success event). Then every call
     is on a valid instance, `lem:tb-section-rank` applies, and `rem:oblivious` bounds every call.
     Replace the time-out wording at `:1204-1207` and `:1445`. The text is in t2.md §1.
2. **ERROR (V)**, `main.tex:1337` (comparison remark).
   - "So the large primes determine the exponent of `thm:bb-envelope`" does not follow. The
     small-prime exponents are "plus the exponent of their exact abelian subroutine", which
     `main.tex:1315` says "is not bounded here".
   - "HSMC" is hidden subgroup modulo the commutator subgroup, not membership.
   - Fix: "for p > c the exponent E_W(c) is ..., while the p ≤ c term depends on the unbounded
     exponent of [II23]'s abelian subroutine".
3. MINOR, appendix `:553`, `:617`. The identity is used, but `thm:bb-envelope` does not take it
   as a hypothesis (`main.tex:1308`).
4. MINOR, `main.tex:1245` (`prop:black-box`(i)). The evaluation count is off by a factor of 2
   once cleanup is counted.
5. MINOR, `tab:tb-steps` (`:1262-1285`). The kernel row's label and sample count are wrong, and
   "2E_Φ per query" depends on s.
6. MINOR, `main.tex:1308`. `thm:bb-envelope` never introduces ε or says it is rational.
7. MINOR, `:811`, `:930`, `:1013`. e_i, t, k and φ each have clashing meanings.
8. MINOR, `:1419`. The c = 1 parenthetical holds only when every e_p = 1.
9. MINOR, `main.tex:1298`. The counts of `cor:black-box-pe` leave the precomputation of Φ on the
   basis lifts implicit.

Earlier reports (`2026-11-03-rees-check-app-d.md`, `2026-11-09-rees-blackbox-corollary-referee.md`,
`2026-11-09-rees-exponent-pe-blackbox.md`): their fixes are in the text, with one exception. The
p^e report replaced the time-out by `rem:oblivious`, and that replacement was not carried into the
proof of `thm:bb-envelope` (`:1445`). None of the earlier reports caught finding 1.

## 8. Codimension (codim): MINOR ONLY

The exact checks found no counterexample. They covered:
- g_6 and the 5-dimensional example;
- the filiform family for m = 3..10;
- Heisenberg no-splitting at p = 3, 5;
- about 2,560 random reductions, with sampled group-level hiding checks under nonlinear
  sections;
- the birthday and `cor:fpt-r` arithmetic.

1. **ERROR (V)**, `appendix-codimension.tex:297` (`prop:app-codim-birthday`, "Sampling and
   cost").
   - "Divides only by integers at most c" is false. The recurrence multiplies by B_j/j!, which
     brings in 1/12 at c = 3 and 1/720 at c = 5.
   - The theorem it cites (`main.tex:806`) correctly says "prime factors at most d". The cost
     claim stands because c < p.
   - Fix: "divides only by integers whose prime factors are at most c < p". The phrase came
     from P5 of 3 Nov.
2. MINOR (V), `main.tex:1195` (`rem:codim`). The example needs m ≥ 4; at m = 3 (Heisenberg) the
   instance is terminal at once. Fix: "Take, for m ≥ 4, ...".
3. MINOR, `:209` with `:138`. (R2) uses `lem:app-codim-sample` outside the standing assumption
   b > k, which is harmless. It omits "aborting on rejection", which `:224` and `:307` assume.
4. MINOR, `:281`. The statement omits codim h ≤ k, and the time hides a log B factor unless
   k ≤ m, which may be assumed.
5. MINOR, `:328` and `appendix-provenance.tex:370-372`. The (6,5) terminal over F_3, F_5 is a
   Lie-level computation, since class 5 ≥ p there. It is confirmed at p = 7 and 11.
6. MINOR (optional), `:82`. "Exactly 1/p" should be "at most 1/p".

Earlier report (`2026-11-03-rees-check-app-e.md`): P1-P8 are present except the optional P6.
It missed findings 1, 2 and 5.

## 9. Filters and backends (fb): MINOR ONLY

No counterexample was found to the conjugation proposition, the filter claims, any gate,
ancilla or transform count, or the TV bounds.

1. **ERROR (V)**, `appendix-backends.tex:47` (scope). The `coherent_k3` programs' output law is
   called uniform "conditionally on Lemmas homogeneous and central, Proposition descent and
   exact transforms". The preceding paragraph (`:45`) also needs three things the list omits:
   - `prop:triangular-sde`;
   - macro correctness, checked exhaustively only for p ≤ 127, and the comparator, checked for
     b ≤ 12;
   - the argued wiring properties.

   Fix: add them to the list (fb.md §1).
2. MINOR, `:45`. As implemented, `Encoding(p)` costs about p³ operations. So "for p ≤ 2·10^6
   it emits one" describes programs the generator would emit, not runs that were made.
3. MINOR, status labels.
   - The witness-circuit proofs lack "argued".
   - `appendix-filters.tex:49` says "(proved)" where `:9` and the provenance say argued.
   - The status range at `:4` omits two items.
   - The macro range is given as p ≤ 13 in one place and p ≤ 127 in another.
4. MINOR, `appendix-filters.tex:36`. With x_1..x_D, "x_{D−2}" should be x_{D−1}.
5. MINOR, `main.tex:1413`, `:1490` and `appendix-provenance.tex:237`. The merge identity is in
   `app:backends-instances`, not `sec:uniform-compilation`.
6. MINOR, `:25`. The general symmetry hypothesis must also hold on left-translated inputs.
7. MINOR, `:23`. "Used only as controls" should add "up to the final transform".
8. MINOR, `:45`. "Fifth backend" should read "fourth and fifth".
9. MINOR, `appendix-filters.tex:49`. u is undefined, and R_F takes values in F_{p^K}.
10. MINOR, `appendix-filters.tex:47`. Boucher-Fouque-Shen is not `\cite`d.
11. MINOR, `appendix-filters.tex:29`. "Matrix p-group" should say p-subgroup of GL_N(F_p).
12. MINOR, typos: a repeated "exactly" (backends `:9`) and "non-normal" (filters `:49`).

## 10. SDE side (sde): GAPS (statements survive)

1. **GAP (V)**, `appendix-sde-side.tex:15`, `:22`; `main.tex:670` (`rem:is-runtime`);
   `prov:sde-is-runtime`.
   - The Schedule 1 variant "for general κ makes at most r_run runs" is labelled proved. The
     only printed proof is for κ = q^e; the composite case is proved only in a source
     (`2026-11-05-rees-is-restarts-composite.md`).
   - Fix: insert the five-line proof in sde.md §1. It was checked against a subgroup-chain model
     on 3004 pairs (κ ≤ 60) with 0 mismatches. The coordinator checked that the paper proves only
     κ = q^e, not the inserted proof.
2. **GAP (V)**, `main.tex:750` (`rem:triangular-scope`). "Using sparse dependencies [KOW,
   Lemma 3.6] lowers the count to (1−1/p)a²/2 + O(a log a)" has no proof and no status label.
   - The local KOW text (`lit/arxiv_2510.07515.txt`, l. 591, l. 652) shows that Lemma 3.6 is
     only the sparse-dependency step. The count is KOW Remark 3.8, for (±⌊q/2⌋)-zero sums, not
     for weights in P∪{0}.
   - The adaptation is the AI-only Theorem C of `2026-11-08-rees-sde-fq-nest.md` (STATE "Now").
   - Fix: delete the sentence, or label it argued and cite Remark 3.8 (text in sde.md §2).
3. **ERROR**, `main.tex:750`. "Schemes built from a universal contraction ... cannot go below
   (a+1)² and (a+1)(a+2)/2" contradicts the sentence before it, because the sparse variant uses
   fewer columns.
   - Its source (`2026-11-02-rees-linear-arity.md` Prop. C) gives only Θ(a²). The exact
     (a+1)(a+2)/2 is a lower bound only for columns in general position
     (`rem:sde-subquadratic`(a)).
   - Fix: in sde.md §3.
4. **ERROR (stale)**, `main.tex:750`, and `appendix-sde-side.tex:46` (minor).
   - "No polynomial-time method at arity o(a²) is known for arbitrary columns and any fixed
     κ ≥ 2" is no longer true. STATE records the AI-only Theorem A (11-07): every bank at
     O(a²/log a) columns for p ≥ ~72κ²a⁶J².
   - Owner policy keeps Theorem A out of the paper, so reword without adding it: "This paper
     proves no polynomial-time method at arity o(a²) ...".
5. **ERROR (V)**, `main.tex:695` and `:721`, inside the E2-UPDATE spots (1), (2).
   - "Decide every prime ≡ 1 (mod 8) up to 16993 ... and show, by separate runs above these
     ranges, 14281 ∈ E_2(8)" is wrong: 14281 < 16993.
   - ":695 only [3,20000] remains open" should be (16993, 20000].
   - Both sentences will be rewritten with the exact E_2(8) on [3,20000] (293 members, largest
     14281; STATE). The update must remove "above these ranges".
6. **ERROR (edge case)**, `appendix-sde-side.tex:82` (`rem:sde-worst-case-q1`(i)). "U_L ≠ 0
   whenever the bank has ≥ D_3(r)+r columns" fails for banks with zero columns
   (`sde/zero_cols.py`). Fix: "nonzero columns".
7. MINOR, labels. Three claims are called proved while their proofs are only in sources, so
   they are "argued" under `main.tex:386`:
   - the exact-run constructions (`:22`, `main.tex:678`);
   - the i.i.d. bound (`:55`);
   - the q1 reduction (`:85`).
8. MINOR, `:4`, `:28`, `:30`. The blanket "argued" also covers the proved κ^κ/2 barrier
   (`prop:app-s2-barrier`).
9. MINOR, `:30`. "(κ−1)^{κ+1}" is unexplained.
10. MINOR, `:6`, `:36`. They say "three remarks"; there are four. The range at `:4` omits
    `prov:sde-worst-case-q1`.
11. MINOR, `:40`, `:60`. "Nothing else in the paper uses it" is inaccurate.
12. MINOR, `main.tex:726`. The "square gap ... open" sentence appears twice.
13. MINOR (optional), `main.tex:674`. κ_d = 1 is placed under "the variant", which is defined
    for κ ≥ 2 only.

Not checked: E_2(7). The κ = 7 search was stopped to save budget.

## 11. Provenance (prov): MINOR ONLY (three ERRORs in the record)

- All 370 labels exist.
- Every cited path resolves, except `verify_schedule2.py`, which the text itself says is not
  kept.
- No private correspondent is named, and nothing claims human review, novelty, speedup or
  hardware.

1. **ERROR (V)**, `appendix-provenance.tex:199` (`prov:bb-corollary`) and `main.tex:1277`.
   - The record says four groups, 30 subgroups and two negative controls; main.tex says "three
     small unitriangular matrix groups and the free two-generator ... group".
   - The control folder `2026-11-08-rees-blackbox-e2e/` (README table) holds five groups:
     heis5_s3, affine5, affine7, free23_5 and ut5_5 (added 9 Nov). It has 8+8+6+8+8 = 38
     subgroups, all recovered, and three negative controls, the third added 9 Nov
     (strict_subkernel, "not caught by public checks").
   - Fix: "four small unitriangular matrix groups ...", "five groups ..., 38 hidden subgroups,
     ... three negative controls (the third, K' ⊊ K, is not caught by the public checks and
     does not affect correctness)".
2. **ERROR**, wrong section pointers into cited reports.
   - `prov:s2-chains` (l. 275): §3/Thm 3.1, not 4.6.
   - `prov:fc-lower` (l. 327): §6, not §5.
   - `prov:fc-numbers` (l. 322): §9, not §6.
   - `prov:tb-evaluation` (l. 358): imprecise.
3. **ERROR**, inside E2-UPDATE (8), l. 287. The numbers 13873/16363 and 14281/18199 are credited
   to the dfs2-prune report, but they come from the 5 Nov snapshot in
   `2026-11-04-rees-k9-sweep.md` §6.
4. MINOR, `prov:sde-decoupled` (l. 57). It calls "argued" what Appendix A proves.
5. MINOR, status words.
   - `prov:s2-main`, `s2-TA`, `s3-main` and `fc-main` say "proved" where the body says
     "conditional".
   - `sde-fc` (87) and `pr-fpt-r` (174) word their conditions differently.
   - See §13(a).
6. MINOR, `prov:dl-central-scalars` (ll. 24-26). It omits the 9 Nov referee report and the p = 11
   GAP time-out.
7. MINOR, `prov:bb-chart` (ll. 193-195). It is stale after the 9 Nov `thm:bb-envelope` changes.
   The 9 Nov referee and citation-check reports are not cited, and two AI checks have no file.
8. MINOR, E2 spots (ll. 288-289).
   - The "145 primes" sentence needs its 4 Nov qualifier.
   - "The 29 primes ≡ 9 mod 16" is misleading: there are 339.
9. MINOR, `prov:sde-worst-case` (l. 75). It claims independent repetition that the check did
   not do.
10. MINOR, `prov:cd-checks` (l. 372). "400 groups" should be 400 (G,H) cases.
11. MINOR, `prov:core` (l. 20). The containment cross-check is dated 5 Nov, before the six
    statements added 9 Nov.
12. MINOR, status wording in `cl-app3` (166), `pr-ring` (178) and `bb-chart` (194).

## 12. `prop:dl-central-scalars` (dl): MINOR ONLY

Separately, the handoff entry "2026-11-09 Rees Lean Check" (another session; not re-checked here) records the proposition as Lean-proved, both sentences as stated (`formal/Formal/DixmierListerScalars.lean`, `DixmierListerGroup.lean`). That covers the proposition, not the citing sentence of finding 1.

The proposition holds as stated for every field of characteristic ≠ 2, including 3. The proof is
complete apart from two unstated clauses (finding 2). The checker ran its own gauge-fixed
Singular eliminations, without the earlier scripts.
- p = 5, 7, 11, 13 and 32003: over the algebraic closure, 36 component points, with an image on
  the centre of order 12. The scalars are only ±1, and the eigenvalues are exactly the sixth
  roots of unity.
- p = 3: the scalars are ±1, with a positive-dimensional image.
- F_p-rational counts give |Aut| = 4·5^12 and 12·7^12, matching the earlier GAP numbers.
- The characteristic-0 elimination and the p = 13 rational count timed out (UNKNOWN).

1. **ERROR (V)**, `main.tex:254` (Contributions (1)). "No automorphism of G supplies central
   scalars beyond ±1" is false for p ≡ 1 (mod 3).
   - The paper's own usage (l. 117) is "act on a central subgroup by known scalars".
   - The ℤ/3-grading with weights (e1..e8) = (2,1,1,2,0,0,1,2) respects all ten brackets; the
     coordinator checked each one. Its automorphism acts on exp(F_p e7) by ω, and composed with
     the sign map by −ω, a primitive sixth root. At p = 7 these are z ↦ z², z ↦ z⁵.
   - On the whole centre it acts by diag(ω,ω²), not a scalar, so the proposition stands. The
     abstract (l. 88) and intro (l. 116) are correct.
   - Fix: "no automorphism of G acts on its centre by a scalar other than ±1". Optionally add:
     "on a central subgroup, automorphisms give only finitely many scalars (sixth roots of
     unity)", which is AI-checked at small p only.
2. MINOR, `:480`. Two clauses should be written out: the rank-one property depends only on
   x mod γ2, and a subspace inside U+ ∪ U− lies in one of them.
3. MINOR, `:88`. "Only nilpotent derivations" needs "over F_p, p > 3": in characteristic 3, Der
   has dimension 16 and contains non-nilpotent elements.
4. MINOR, `:489`. G has no "top grade"; the intended object is γ3.
5. MINOR, `:465/:469`. Notation (Span_K; ζ ≢ ±1 mod p), plus one clause justifying the passage
   to K̄.
6. MINOR (optional), `:461`. The elementary divisors of the derivation system are {1, 3, 6}, so
   the rank is 52 for every p > 3 and the 5 ≤ p ≤ 23 finite check is redundant.

## 13. Cross-cutting issues for the integrator

a. **The status vocabulary is used two ways.**
   - `main.tex:70-72`, `:386` define "conditional" (on a stated hypothesis or an unproved part)
     and "argued" (the proof is only in a source).
   - In practice "conditional" also marks results proved in full but unread by a human
     (`main.tex:712`, `:721`).
   - Several items say "proved" where the proof is only in a source: sde-1, sde-7, fc-1, fb-3.
   - Decide one convention and sweep the labels: prov-4/5, sde-7/8, fb-3.
b. **"Class at most c" against "class c".** The contract fixes c only as an upper bound. Two
   places use c as the true class (s3-1, t1-2), and one uses class ≤ c on charts that are not
   checked (t2-1). The repairs are the same kind of one-line linear-algebra step.
c. **Uncomputed constants against literal cut-offs.** These rely on time bounds whose
   constants the paper never computes:
   - the Schedule 2 Phase 1 cut-off T_1 (s2a-6);
   - the cut-off 4T in `sec:recursion` and `rem:oblivious` (which says so);
   - the RtF time-out (t1-1).

   The paper's stance is that such an algorithm exists with valid constants. That is honest
   only if each statement whose bounds use these cut-offs is phrased as existence, or uses
   `rem:oblivious` on valid inputs instead. t2-1's fix removes the one place where neither
   applies. s2b-4 adds that the stated worst-case time of `thm:app-s2-main` assumes a
   uniform draw is one step, and gives a capped-loop repair. Inside the recursion the 4T
   cut-off covers it. s2b-5 updates "the Schedule 2 calls are not bounded here".
d. **E2-UPDATE.** sde-5 and prov-3/prov-8 are wrong now and must be fixed in the planned
   update, not separately.
e. **Later AI results contradict sentences.** sde-4 is the only sentence found that a later
   AI-only result (SDE Theorem A) makes false. sde-2 overlaps the AI-only Theorem C. Both need
   rewording that keeps those results out of the paper, as the owner decided.

## 14. What a human expert must still check

These are external theorems and imports, and the checkers could not verify them from local
sources.
1. **Ivanyos-Santha (IS15) imports:**
   - `thm:is-import`;
   - the determinism read from the proof of §3;
   - the Thm 11 / Lemma 12 node structure and the §3.1 restarts;
   - Cor 8 / Prop 7 / Thm 5 as described;
   - Fact 2 / van de Woestijne, behind the deterministic design of `lem:app-sub-design`(b).
2. **ISS 2012** (Ivanyos-Sanselme-Santha; no local copy): Theorem 2, Lemmas 2-3, the
   refined-pc-presentation model, the section numbering, Claim 1 for κ = 2, and whether
   "is this paper's" (`main.tex:1219`) is fair.
3. **Imran-Ivanyos 2023:**
   - Theorem 1's oracle model (subgroup-state unitary, inverse, exactness);
   - the numbering of Props 1, 2, 4, 5;
   - the query exponent of their exact abelian subroutine, on which t2-2 and the p ≤ c term
     depend.
4. **Lazard and Khukhro:**
   - Lazard 1954 in subgroup form and the Khukhro locators (§10.2, Ex. 10.24, Lemma 10.7,
     Remark 9.17 p. 109);
   - Trappeniers 2024 Thm 2.3;
   - that BCH_c has coefficients in ℤ[1/c!] (von Staudt-Clausen).
5. **The Weil bound** in the form used (Lidl-Niederreiter Thm 5.41, "NEEDS HUMAN VERIFICATION"),
   the Jacobi-sum bound |J| = √p, and the Chebotarev step of `prop:app-s2-chebotarev`. The
   second-moment chain of `prop:app-s2-TA`(i) deserves one human read.
6. **KOW 2026** (Thm 2.2, Lemma 3.6, Remark 3.8) and **KMOSW 2026** (Thm 1.10, Prop 5.3): what
   each states, and whether the sparse count transfers to weights in P∪{0} (sde-2).
7. **MP13 Thm 1.1** numbering in the CRYPTO version; **GKSZ** Def 6.1 and Thm 10; BGP Prop. 26
   against `prop:app-s2-barrier`; CHMT 2014 (whether its threshold covers diagonal systems).
8. **Other citations.**
   - Bene Watts et al., Algorithms 1-2: is "added here" right for the recovery step?
   - Luks 1992 Thm 3.2(5),(7) for unipotent p-subgroups of GL_N(F_p).
   - CEMM's 4/π², Shor §5, Hardy-Wright Thm 184, AKS 21/2 (and whether 15/2 is effective),
     Kitaev 1995 over ℤ/2^e.
   - The Dixmier-Lister 1957 bracket table.
9. **Delicate arguments worth a human read** (all AI-checked only):
   - the label-law bookkeeping of `lem:s3-tree`(a), and `lem:hybrid` with
     `thm:uniform-compilation`(iii) on canonical subspaces;
   - the guard argument in the second proof of `thm:app-codim`(ii);
   - `prop:dl-central-scalars`;
   - the witness-circuit and "read off the code" arguments for `coherent_k3`;
   - `rem:oblivious` and the Schedule 2 worst-case argument (found correct by s2b);
   - where the chart check of t2-1 belongs: in Theorem main or in the chart step of
     `thm:bb-envelope`. Does any other caller feed Theorem main out-of-contract inputs on
     erroneous branches?
   - whether existence-only cut-off constants are acceptable in stated theorems;
   - the randomness model (s2b-4);
   - T_R(9,3), within 0.2% of the search bound.
10. **Modelling and judgement.**
    - Whether "acts on the centre by a scalar" is the right barrier notion, given that central
      subgroups admit sixth roots (dl-1).
    - The barrier model of `prop:app-s2-barrier`.
    - The cryptographic assumption of `rem:sde-subquadratic`(b) (power-residue PRF key
      recovery; BBUV 2020, vDHI 2006).
    - The lattice assumption behind `rem:fc-zero-sum-sis`(c).
    - The i.i.d.-supply scope of Schedule 3 and of the subspace source (δ promised, r
      supplied, R linear).
    - Priority of the codimension composite.
    - Whether "(proved)" may label remarks resting on imported steps.

## 15. Not checked / UNKNOWN

- E_2(κ) for κ ≥ 6. No searches were run, per the brief; E_2(7) is UNKNOWN. The κ = 8, 9 numbers
  are left to the E2 update.
- The joint-moment and central-moment claims (`rem:app-s2-joint-moments`, argued).
- The provenance-only abort rates and the rescaled-form runs at 2^31−1 and 2^61−1.
- DL: the characteristic-0 elimination and the p = 13 F_p-rational count (timed out).
- `thm:uniform-compilation`(iii) in full (used, not checked, by s3).
- The core paper `core/main-core.tex`, which had its own hostile referee.
- The main-body sections outside the appendices' main-text counterparts.
- The PDF build.
- Every external source in §14.

## 16. Files

- Per-part reports: `2026-11-09-rees-full-appendix-proof-check/{s2a,s2b,s3,fc,sub,t1,t2,codim,fb,sde,prov,dl}.md`.
- Scripts and outputs: the same-named subfolders.
- Brief: `BRIEF-COMMON.md`. Diffs used: `diffs/`.

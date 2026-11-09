# Adversarial check of the Rees SDE worst-case report, and integration

**Status: COMPLETE, AI-checked, pending human review.** 5 November 2026, overnight AI-only pass
(one Claude Code session, independent of the session that wrote the report and of its §10 checker).
Object: `2026-11-05-rees-sde-worst-case.md` and its folder. Own code and outputs:
`2026-11-05-rees-sde-worst-case-check/`, interpreter `/opt/anaconda3/bin/python`. No git, no
network, no `make_numbers.py`, no change to tables, `numbers.tex` or claim gates.

## 0. Verdict

**No Error survives.** Proposition 1, Theorem 2 (a)–(d), the D_E counts, Corollaries 3 and 4 hold
as stated. I found no Gap in a proof. I found 7 Imprecisions, all in the report's prose or in the
proposed LaTeX, and fixed them in the inserted text (§3). The remark is now in `main.tex` as
`rem:sde-worst-case`, directly after `rem:sde-block-steered`. One sentence of `rem:triangular-scope`
was updated (§4).

**Meaning.** General position is a property of Rees labels only at primes exponential in a·log a.
It changes no table, no E_W(c), not the exponent 143 and no gate. No owner decision is needed (§5).

## 1. Line-by-line check of the proofs

**Proposition 1 [holds].**
- (i) Chevalley–Warning, as already used in the paper (κa+1 columns; Lean also checks it).
- (ii) Block-diagonal sum of a unsolvable one-dimensional banks; (1, −u) with u ∉ P is unsolvable.
- (iii) Correct reduction: with x_3 = 1, Y = (−c_1/c_2)(X + c_3/c_1), so X ∈ Good(β) for offsets
  (0, c_3/c_1), which are distinct, and classes (0, cos(−c_1/c_2)). Lemma W at e = 2 gives
  nonemptiness for p − 2 > (κ²−1)√p. The Hasse–Weil aside is right too: the Fermat curve has genus
  (κ−1)(κ−2)/2.
- (iv) Olson's Davenport constant. This is already in the paper, as `thm:power-sde`(iii), with the
  remark that small p is a finding problem, not an existence problem.

**What is already in the paper.** The upper bound κa and the κ = p−1 zero-sum case are already
there. New are the lower bound 2a ≤ a·N(κ,1,p), N(2,a,p) = 2a, N(κ,1,p) = 2 under G*_2 ≥ 1, and
the computed small values. The inserted part (a) cites the existing material and keeps only the
new content.

**Theorem 2 [holds].**
- **Circuits.** The relations of T ∪ {c} modulo U form a line, because T is independent mod U.
  So the support S of the relation is a circuit mod U.
- **Blocks.** A dependency δ has at most min(κ, |S|) classes, and min(κ, |S|) ≤ E_l = min(E, |S|)
  because E ≥ κ. So δ can be split into E_l blocks, each inside one class.
- **Ω_l.** The only relation of the W_b mod U_{l−1} is the constant one (Theorem B(i) of the
  two-relation report, re-derived). So W_1..W_{E_l−1} is independent mod U_{l−1}, and the sum is
  direct.
- **Swap invariants.**
  - B stays a basis: γ_σ ≠ 0.
  - A swapped-in c ∈ U never leaves B, because only columns σ ∉ U leave and U only grows. So
    |B ∩ U| strictly increases and there are ≤ r swaps.
  - The final B is disjoint from every round support. Round columns come from `unused`; c joins B
    without being consumed; σ leaves B to `unused`.
  - So the weights t_σ on B and the round weights never collide.
- **Values.** τ_{l−1} = Π_{l−1}τ_l − s_l e_l. The round's value is Σ_{b≥1}β_bW_b + s_l e_l.
  Telescoping gives Σ_σ t_σσ + Σ(round values) = 0, and x ≠ 0 because t_σ ∈ P.
- **Steering forms.**
  - τ_j = Π_jτ_L − Σ_{l>j} s_lΠ_j(e_l) holds because the coordinate projections of
    V = Ω_1 ⊕ … ⊕ Ω_L compose consistently and e_l ∈ U_{l−1}.
  - φ_{j,bb′} = (β_b − β_{b′})∘(Ω_j-coordinates) is a nonzero functional on V. It is a coordinate,
    or a difference of two coordinates, composed with a surjection.
  - B spans V, so φ(σ) ≠ 0 for some σ ∈ B. This holds for every bank.
- **Success bound, including 2-block rounds.**
  - Failure ⇒ Good_l = ∅ at some level ⇒ a cross-class coincidence at that level. Without one,
    same-class equal offsets merge, at most E distinct offsets remain, and |Good| ≥ G*_E(p).
  - Bound the event "no coincidence above level j, and F_{j,bb′} = 0" for each cross pair of each
    round, including 2-block rounds. A coincidence in a 2-block round forces s = −β (Good = {0} after
    translation), and that forced value can matter later. So ρ must count those pairs, as the
    report's G1 fix says.
  - Case 1: m is the least l > j with φ(e_l) ≠ 0. Then s_m is the last drawn scalar that enters F,
    it is drawn uniformly from a set of ≥ G* elements (no coincidence at m), and F is affine in s_m
    with nonzero slope: ≤ 1/G*.
  - Case 2: F = −Σt_σφ(σ) with some φ(σ) ≠ 0: ≤ 1/|P| = κ/(p−1).
  - Summing over the ρ cross pairs gives the bound.
  - ρ ≤ Σ_l C(E_l,2) ≤ (E/2)Σ(E_l − 1) = rE/2. For E = 3: ≤ r at κ = 2 (a 2+1 split has 2 cross
    pairs per 2 dimensions), and ≤ 3r/2 at κ = 3.
- **Stall count (π).** At a stall the columns are:
  - B (r of them);
  - round columns, at most D_E(r) − D_E(q) by the telescoping inequality, since every round at
    quotient q′ has k ≤ q′, gain min(E−1, k) and cost k+1;
  - pool (π), never rescanned;
  - unused columns, all independent mod U at a stall, so ≤ q.

  With D_E(q) ≥ q + 1 this gives M ≤ D_E(r) + r + π − 1.
- **General position.** A true-pool event gives c ∉ B with c ∈ span(B ∩ U) and
  |B ∩ U| ≤ dim U ≤ r−1. That is a dependent set of ≤ r distinct columns, which general position
  forbids. For r = 1, general position means no zero column.

**D_E [holds].** I re-derived the closed form D_3(q) = ⌊(q+2)²/4⌋, the bound
D_E(q) ≤ q²/(2(E−1)) + q(1/(E−1)+5/2) (the big-round sum is increasing in the number of big rounds
up to ⌊q/(E−1)⌋), and D_2. `dcheck.py` → `dcheck.out` confirms, for q ≤ 400 and E ≤ 12: the closed
forms, the bound, monotonicity, excess D_3 − (M_3 − 1) = [q even], excess ≤ 2q, and the report's
arity table.

**Corollaries [hold].**
- (3)(i): r·10/p ≤ 10a/p ≤ 1/2 at p ≥ 20a, and 2/(p−1) ≤ 10/p.
- (3)(ii): (3a/2)(54/p) = 81a/p ≤ 1/2 at p ≥ 162a.
- Corollary 4: p ≥ 8κ^{2E}E² gives (κ^E−1)(E−1)√p + E ≤ p/2, hence G* ≥ p/(2κ^E). Then
  (rE/2)(2κ^E/p) ≤ 1/2 at p ≥ 2aEκ^E. κ^E ≤ κa once a ≥ κ^κ (the E = 3, κ = 2 corner a = 4 also
  works).
- Arc caveat: through r−2 columns pass p+1 hyperplanes of V, each holding ≤ 1 further column, so
  M ≤ p + r − 1 and p ≥ ⌊(a+2)²/4⌋ + 1 at r = a.

## 2. Independent computations

These were written from the statements only. My code imports nothing from the report's folder.

| file | what | result |
|---|---|---|
| `gstar.py` → `gstar_k2.out`, `gstar_k3.out`, `gstar_summary.out`, `gstar_selftest.out` | G*_3(p), all class patterns including equal ones, e ≤ 3; FFT correlation, self-tested against direct enumeration of all offsets (p ≤ 37) and of normalised offsets (p up to 2767): 0 mismatches | κ = 2, p ≤ 6000: G* = 0 exactly at {3, 5, 7}; min G*/p on [256, 6000] = 0.1089 (p = 257, G* = 28) ≥ 1/10. κ = 3, p ≤ 12000: G* = 0 exactly at the 22 primes of E_cg(3,3); min on [2750, 12000] = 0.0253 (p = 2767, G* = 70) ≥ 1/54. Lemma W tails: ≥ p/10 for p ≥ 4930, ≥ p/54 for p ≥ 10828, so both ranges are covered |
| `nmax.py` → `nmax.out` | exact N(κ,a,p), a = 1, 2: DFS over multisets of column classes mod P, with a DP reachable-value set | all eight rows of the report reproduced: N(2,2,7) = N(2,2,13) = 4; N(3,2,7) = 5; N(3,2,13/19/31) = 4; N(4,1,13) = 3, N(4,2,13) = 6; N(4,2,17) = 5 |
| `mysss.py` | own implementation of SSS(E) with swaps (forward, backward, verification); variants with no swap and with one steering source | |
| `run_check.py gp` → `run_gp.out` | general-position banks at the budget D_3(a)+a: random banks at p = 257, 2767, 10^6+3 checked exhaustively (a ≤ 5); moment-curve banks (Vandermonde, so general position by construction; checked for a ≤ 6) with random, all-1 or all-non-residue multipliers and a random GL_a | 17 settings, κ = 2 at p ∈ {257, 263} (a ≤ 12 = ⌊257/20⌋), 10007 (a = 20), 10^6+3; κ = 3 at p ∈ {2767, 2791} (a ≤ 16). 303 banks, **0 stalls, π = 0 always**, ρ within r resp. 3r/2, every bank solved, every witness verified. Single-pass failure rates 0–2.3%, against bounds 4–43% (all ≤ 1/2) |
| `run_check.py smallp` → `run_smallp.out`; `swap_stress.py` → `swap_stress.out` | general-position banks at small p, where columns land in U often (Theorem 2(b),(d) need no admissibility) | 4,840 banks: **96 swaps, π = 0, 0 stalls**. With swaps disabled (control), each of the 96 would-be swaps is a discarded column and a stall, so the swap is what makes (d) true. At G* = 0 primes, single-pass failures of 2–47% appear (sensitivity control) |
| `run_check.py adv` → `run_adv.out` | not in general position: lines (a+1 and a+3 lines), hyperplane-dense, entries in {0, ±1, ±2}, sparse 0/1, scaled palettes; κ = 2, 3; p ∈ {13, 31, 61, 1009}; a ≤ 6; M ∈ {D+r, D+r+2, κa+1} | 3,240 banks, 858 stalls. The decomposition M ≤ D(r) − D(q) + r + π + q, rounds ≤ D(r) − D(q) and unused ≤ q hold at **every** stall. 359 stalls at M ≥ D(r)+r, **all with π ≥ 1**. The explicit §5 bank stalls with π = 1, q = 1 under my implementation too |
| `run_check.py neg` → `run_neg.out` | negative controls | Unsolvable block banks (2a columns, κ = 2, 3, a ≤ 8): always stall, never a witness. A corrupted witness is rejected. One-source steering: inconclusive at these p (rare), reported only |

Running time: every run is under 4 minutes, under `nice -n 10`, with at most 2 processes.

## 3. Findings (all Imprecisions; all fixed in the inserted text)

- **I1 (report §4, "Rees labels").** The report says "Corollary 3 does not apply to them". That is
  too strong.
  - By a union bound, i.i.d. uniform labels on K_d^⊥ are in general position except with
    probability ≤ C(M, a_d)/(p−1). For example, log₂C(M, a) = 31.9 at a = 10 and 49.9 at a = 14,
    so at p = 2^61 − 1 Corollary 3 does apply to labels with a_d ≤ 14.
  - The conclusion still stands: at such primes `rem:sde-block-steered` already gives the smaller
    arity M_3(a).
  - Part (c) of the remark now says this.
- **I2 (report §5).** The full algorithm's witness for the explicit stalled bank is
  x = (0,0,0,0,442,0,0,0,1), a proportional pair with ratio in P, not a collinear triple.
- **I3 (proposed LaTeX, (b)).** The text omitted that the reserved columns carry the weights t_σ,
  and that the blocks lie inside the classes of the dependency. Both are added.
- **I4 (proposed LaTeX, (b)).** "at least D_E(r)+r+π columns, where π is the number of true-pool
  events" is reworded as a statement about the run. The arc bound is now proved in one clause, not
  called standard. E = 3 is stated in the general-position corollary.
- **I5 (proposed LaTeX, (b)).** The planted runs were padded with uniform random columns, for
  a ∈ {4, 6, 8}, 48 trials. The text said only "padded"; it now says this.
- **I6 (proposed LaTeX, (a)).** Duplication: Chevalley–Warning is now cited as "already used in
  this section", and κ = p−1 as `thm:power-sde`(iii).
- **I7 (proposed LaTeX, preamble).** G*_E includes E′ = 1. The exact admissibility sets
  (κ = 2: p ≥ 11; κ = 3: p ∉ E_cg(3,3)) were recomputed and stated, and the check sentence names
  this report.

## 4. Integration

- **`docs/papers/rees-hsp/main.tex`.**
  - A new `\begin{remark}…\label{rem:sde-worst-case}` was inserted directly after the
    `\end{remark}` of `rem:sde-block-steered`, before `rem:combined-schedule`.
  - Statuses are marked throughout: proved parts carry the remark's "AI-checked, pending human
    review"; finite computations, the sampled computation and the open part are marked as such.
  - `rem:triangular-scope`, sentence "No polynomial-time method at arity o(a²) is known for
    arbitrary columns …": the parenthesis now reads "(Remark rem:sde-block-steered gives one for
    i.i.d. uniform columns, and Remark rem:sde-worst-case one for every bank in general position,
    both at primes p ≥ poly(a))". The claim about arbitrary columns is unchanged and still true.
- **Edit method.**
  - Exact-string edits with count asserted 1 (`scratchpad/apply_edits.py`).
  - main.tex was re-read immediately before the edit and backed up to
    `scratchpad/main.tex.bak-before-worstcase-edit`.
  - The edited file is byte-identical to the built copy.
  - No `\mathsf`, `\mathrel`, `\begingroup`, `\aa`. No new macro or citation.
- **Build** in `$TMPDIR/rees-worstcase-build` (`latexmk -g -pdf`): exit 0, 0 Overfull, no
  undefined references or citations, no "Float too large". The remark is Remark 4.14.
- **Tests.** `pytest -q tests/tools/test_rees_paper_numbers.py`: 2 passed.
- **Records.** Integration log row I211; item 3 of `research/REES_FULL_CONTINUATION.md`.

## 5. Meaning for the paper

- **General position is not a realistic worst-case hypothesis for Rees labels at the primes that
  matter.**
  - The labels are i.i.d. uniform on K_d^⊥, so general position is a probabilistic property. It
    holds with probability ≥ 1 − C(M, a_d)/(p−1), so only at p ≫ (e·a/4)^a.
  - At small and moderate p it is impossible: the arc bound needs p ≥ ⌊(a+2)²/4⌋ + 1. The worst-case
    exponents (E_W(c), 143 at c = 9) are maximised at small p.
  - Where general position does hold, `rem:sde-block-steered` (i.i.d. columns, p ≥ 64a² for κ = 2)
    already has the smaller arity M_3(a) ≤ D_3(a) + a.
- **What the remark adds.** It adds a column-deterministic guarantee for a structural class of banks,
  and it shows the existence threshold is linear.
- **What does not change.** No table, `numbers.tex`, E_W(c), the exponent 143, Theorem `thm:main`,
  or Rule W. `general_sde_implemented` stays false.
- **Owner decision: none required.** Using Corollary 3 for Rees labels would be dominated by
  `rem:sde-block-steered`, which the paper already declines to adopt.

## 6. Claim gates that stay false

- An o(a²) polynomial-time SDE solver for arbitrary columns. Conjecture 5 is unproved.
- A quadratic existence barrier. It is false by Proposition 1.
- A quadratic necessity for polynomial-time solving. It is unproved.
- Uniformity in p. The solver needs admissible p with G* ≫ a, and general position needs
  p ≳ a²/4.
- Any novelty or priority claim.

## 7. Next hard question and command

- **Question.** Q1 of the report: bound the true-pool loss on dense banks (stall at q = 1 with
  |B∖U_L| = 1).
- **Command.** `cd research/audits/reviews/2026-11-05-rees-sde-worst-case-check && nice -n 10
  /opt/anaconda3/bin/python -B run_check.py adv 1`. Extend it with a π-maximising hill climb and
  with `sss_full` from the report folder as the solver.
- **Expected artifact.** Either a solvable bank (M ≥ κa+1) on which the full algorithm fails, with
  its stall record, or a longer clean record.
- **Acceptance test.** Every reported failure is verified solvable by brute force (a ≤ 3) or by
  M ≥ κa+1.

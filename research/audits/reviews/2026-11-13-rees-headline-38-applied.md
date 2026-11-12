# 2026-11-13 Rees core paper: headline class-9 exponent 53 → 38 (Schedule 1H) applied

Integrator-writer pass for the owner decision "whichever is more impressive". AI only (one Claude
Code session), pending human review. No Git, no network, `make_numbers.py` not run, no claim gate
touched, the full version (`main.tex`, `appendix-*.tex`) not edited.

Status of what was promoted: **PROVED given cited results** (IS Theorem 11 as AI-read,
Lemma `lem:rounds`, Weil's bound for diagonal equations, Rabin root finding), plus an exact finite
computation. AI-proved (k8-attack note), AI-refereed once (38-referee: CORRECT WITH FIXES), written
up and re-derived here. **No human has read it.** 38 rests on everything 53 rests on, plus the new
lemmas. Ivanyos confirmed only the full depth (145; 95 with halving).

Backup (pre-edit): `research/audits/reviews/2026-11-09-rees-paper-pass-prep/backup-pre-headline38-2026-11-13/`
(`core/main-core.tex`, `core/numbers.tex`, `core/main-core.pdf`, `numbers.tex`, `arxiv/METADATA.md`).

Folder `research/audits/reviews/2026-11-13-rees-headline-38-applied/`:
- `edit_scripts/core1.py … core5.py`, with `edlib.py` and `halving_section.tex`. Every edit is an
  exact old→new replacement asserted to match once. All 50 applied.
- `main-core.diff`, `numbers.diff`, `METADATA.diff`: the full diffs against the backup.
- `halved_schedule.py` → `.json`, `.out`: my exact computation.
- `halving_executor.py` → `.json`, `.out`: a finite falsifier.

## 1. Mathematics written into the core (new §5.1 "Schedule 1H: Halving the Degree")

Labels are the paper's.
- **`lem:stage` (Lemma S) and `lem:finish` (Lemma F, finishes F0 and F1).**
  - Built on κ-solutions (w ∈ (P∪0)^M with explicit κ-th roots r), objects, and
    T(c) = {Σ y_k c_k : y ∈ (P∪0)^r ∖ 0}.
  - q is any element with q^{(p−1)/κ} = −1 (q = θ^{κ/2} for a nonresidue θ, or q = −1 when h is
    odd); ε = −q^{−1}. No primitive root is used (referee M1(i)).
  - The κ-th roots needed by Lemma S are explicit inputs to the lemma (M1(ii)).
- **The recursion for T_j.** T_0 = P and T_j = T_{j−1} ∪ εT_{j−1} ∪ (T_{j−1} + εT_{j−1}). It is
  independent of the choice of q, stabilizes by j ≤ κ+1, and its tables cost O(jκp + p log p).
- **`lem:two-term`.** For p ≥ 4κ⁴, η ∈ P + εP, and a uniform u succeeds with probability ≥ 1/(2κ).
  - **Change versus the attack and referee:** the proof uses *Weil's bound for diagonal equations
    with nonzero right side* (|N − p| ≤ (κ−1)²√p, the statement already imported for
    `lem:zero-sum-length`(iii), with its existing `% NEEDS HUMAN VERIFICATION` locator flag).
  - The Hasse–Weil curve bound (κ−1)(κ−2)√p + 3κ is therefore no longer used, and M3's extra
    import disappears. The threshold is 4κ⁴, the same as the zero sums use.
- **`def:schedule1h` (the rule, stated exactly).**
  - Candidates:
    - (a) Schedule 1 at κ, of arity G(κ,a)^L;
    - (H) plans (s, F), F ∈ {F0, F1}, admissible by an exact T_s check when p < 4κ⁴, and only
      (1, F1) when p ≥ 4κ⁴.
  - Arity A_κ(a) is the least arity at a (ties: (a), then smaller s, then F0). Degree e^H_κ is the
    least degree.
  - Randomness: Las Vegas only for p ≥ 4κ⁴. There it covers the q trials, Rabin roots, and u-trials
    for the representations (M1(iii),(iv)). For p < 4κ⁴, tables are used instead.
  - F2 finishes are deliberately omitted: the referee's run "S1H without F2" gives the same worst
    values.
  - The preprocessing covers the whole chain κ, κ/2, … (zero sums and q).
- **`thm:halving` (Theorem HC, relabelled "Las Vegas, output checked"; M1).**
  - (i) A_κ is computable and A_κ ≤ G(κ,a)^L.
  - (ii) It is a κ-solver, Las Vegas, with an explicit expected-time polynomial. It is deterministic
    only when every plan run sits at a degree κ′ with p < 4κ′⁴.
  - (iii) A_κ(a) ≤ K_κ(a+1)^{e^H_κ}.
- **`cor:hcd`.**
  - (i) For h odd: q = −1, ε = 1, and the plan (⌈log₂t⌉, F0) is valid for every p. I removed the
    attack's word "deterministic", because the roots still need Rabin at large p (M1).
  - (ii) For p ≥ 4κ⁴: e^H_κ ≤ e^H_{κ/2} + 1 and A_κ ≤ (a+1)A_{κ/2}.
- **`rem:kappa-two`.**
  - A_2(a) = (a+1)² for every odd p, by a hand proof (two squares).
  - Proposition F appears as a remark: every candidate has degree ≥ 2 and arity ≥ (a+1)².
- **`lem:halved-exponent`.** E_H(c) = 1 + max_p Σ_d e^H_{p,d}.
  - A_d ≤ B_d, and E_H ≤ E_1.
  - (i) ⌈c/2⌉² + 2⌊c/2⌋ ≤ E_H(c), so Ω(c²) survives.
  - (ii) E_H(c) = 3, 6, 10, 14, 20, 25, 29, 38 for c = 2..9. E_H(9) = 38 is attained exactly at
    p ≡ 1 (mod 2520).
  - (iii) A constant C^H_c exists, with C^H_c = C_c for c ≤ 9.
  - **Tail proof by hand (stronger than M5):** for p ≥ 26244, e^H is the fixed table
    ê = (1,2,3,3,5,4,7,4,9), with ê(κ) ≤ ê(d) for κ | d. So the sum is ≤ 37, with equality iff
    2520 | p−1. No residue enumeration is needed; I did one anyway as a check.
  - Exact part: p < 26244.

## 2. Exact computation (`halved_schedule.py`; 5 min, RSS < 50 MB, nice -n 19)

- **E_H(c), c = 2..9**, by class sumsets with no Weil shortcut for p < 26244, plus all 1152 units
  mod 5040 above:
  - Values: **3, 6, 10, 14, 20, 25, 29, 38**. This matches the referee's independent
    `s1h_independent.py`.
  - c = 9 attains 38 at 2521, 7561, 12601, 15121, 20161 only, and in the tail at residues {1, 2521}.
  - Control: E_1 = 5, 8, 16, 19, 35, 36, 44, 53, attained at 2521, 7561, 12601.
- **Weil falsifier:**
  - T_1 = F_p^× holds at every prime in [4κ⁴, 30000], for every even κ ≤ 8.
  - t ≤ 3 holds there too.
  - The exact rule agrees with the formula on [26244, 30000]: 0 disagreements.
- **Constants:** K_κ ≤ κ^{κ(κ−1)⌈log₂(κ+1)⌉/2}, with 0 violations, so C^H_c = C_c for c ≤ 9.
  Degree-optimal plans use ≤ 3 stages.
- **Table `tab:query-crossover`**, recomputed with `classical_lb.py`, which was imported read-only
  and is the same code path as `verify_headline.py`:

  | row | log₂Q_q old → new | LB from | (v) below | copies |
  |---|---|---|---|---|
  | Heisenberg | 9.00 → **5.00** (Q = 32, every p) | 443 → 29 | 84 → none | 81 → 50 |
  | filiform | 20.00 → 14.83 | 9,391 → 863 | 3,325 → 305 | 218 → 163 |
  | free 2-gen | 23.68 → 17.68 | 3,413 → 431 | 1,567 → 196 | 293 → 221 |
  | Dixmier–Lister | 25.55 → 18.91 | 157 → 41 | 97 → 27 | 474 → 350 |
  | class-9 profile | 563.63 → 314.06 | 2^{62.60} → 2^{34.87} | 2^{62.35} → 2^{34.62} | 22,548 → 12,565 |

  - With exact 8ℓ the (v) thresholds are 310/198/27, that is, primes up to 307/197/23. For the
    Heisenberg row there is none.
  - The maxima are attained at every p (Heisenberg), at p ≡ 1 (mod 3) (class-3 rows) and at
    p ≡ 1 (mod 2520) (class 9).
  - rem:query-separation(b): 2^{62.6} → 2^{34.8}, rounded down because the crossover is 2^{34.87}.
- **Examples:**
  - Heisenberg: A_2(1) = 4.
  - Class 3: A_2(3) = 16. Q_q = 3(5+τ)·16·729 ≈ 2^{17.68} at p ≡ 1 (mod 3).
  - rem:zero-sum: A_4(2) = 243 at p = 5 (two stages + F1). Hand-checked.
- **Executor (`halving_executor.out`):** 400/400 outputs exactly verified, over 16 cells. These
  include κ = 6 at p = 7, 13, 31, 37, 61, which the referee had not executed, and κ = 8 at 17 and 41.
  The inner solver is a brute-force D-solver, and every cell reached the finish at least twice. This
  is a falsifier only.

## 3. Edits to `core/main-core.tex` (now 55 pp.; was 50)

Theorem statements, exact old → new:
- **thm:main(3):**
  - Old: `Q_q = c(m+τ)∏ B_d(g_d)` "… with B_d as in (eq:Bd) (so Q_q depends on p through the κ_d
    and L_d, and Q_q ≤ c(m+τ)∏B̄_d(g_d))".
  - New: `Q_q = c(m+τ)∏ A_d(g_d)` "… with A_d the arity of Schedule 1H (def:schedule1h); so Q_q
    depends on p through the κ_d, the t_{p,κ} and the sets of §5.1, and
    Q_q ≤ c(m+τ)∏B_d(g_d) ≤ c(m+τ)∏B̄_d(g_d), with B_d and B̄_d as in (eq:Bd)."
- **thm:main(4):**
  - Old: "Q_q ≤ C_c c(m+τ)(m+1)^{E_1(c)−1}, C_c = …, where E_1(c) ≤ 1+Σ… is the exponent of
    Lemma exponent; E_1(9) = \ReesClassNineQueryExp."
  - New: "Q_q ≤ C^H_c c(m+τ)(m+1)^{E_H(c)−1} and Q_q ≤ C_c c(m+τ)(m+1)^{E_1(c)−1}, with C_c = …,
    where E_H(c) ≤ E_1(c) ≤ 1+Σ… are the exponents of Lemmas halved-exponent and exponent, and
    C^H_c depends only on c, with C^H_c = C_c for c ≤ 9 (Lemma halved-exponent(iii)). In particular
    E_H(9) = \ReesClassNineHalvedExp; Schedule 1 alone gives E_1(9) = \ReesClassNineQueryExp."
  - (1), (2) and (5) are unchanged.
- **rem:main-solver:** it is retitled "What the proof uses from the solver" and rewritten.
  - The four properties now concern Schedule 1H: total, checked, Las Vegas with explicit expected
    time, charged per rem:is-import(d), arity public. Schedule 1 alone is noted as another such
    solver, deterministic.
  - The status sentence now says 38 rests on lem:rounds, lem:zero-sum-length, §5.1 and
    lem:halved-exponent, with 53 without halving, and 145 and 95 at the confirmed depth.
  - "His confirmation covers neither the shorter depth L_d nor the halving."

Other edits (tag in the edit scripts):
- **Abstract (C1):** "… is Ω(c²) (at most \ReesClassNineHalvedExp at c = 9), …". The LaTeX abstract
  is 1911 characters.
- **eq:Bd paragraph (C2):** defines A_d ≤ B_d.
- **After thm:main (C5):** the procedure uses Schedule 1H.
- **C7:** the exponent sentence (bounds, 38, 53), the imports (Weil "with nonzero right side",
  used in lem:two-term and thm:halving) and the exact computations.
- **"What is new" (C8):** "the solver is built on their collision step; the halving … in the spirit
  of [IS §3.3] … no priority".
- **C9:** Proof overview (c).
- **sec:status (C10):** adds "the stated exponent 38 rests on everything 53 rests on and, in
  addition, on the halving … one AI session, refereed by another (correct with fixes, all applied)
  … no human has read it".
- **C11:** Organization.
- **rem:is-import (D1, D2):**
  - (a): the roots of Schedule 1H.
  - (d) is rewritten as two Las Vegas kinds. The preprocessing has n_pre ≤ 2(c−1) tasks (zero sums
    over the whole chain, and q). The merge solver is Schedule 1H, with failure probability 0 and a
    cut-off at 4T.
  - The split is ⌈log₂(6n_pre/ε)⌉ attempts per task and ⌈log₂(6N_solver/ε)⌉ per call, each part at
    most ε/6 (M2).
  - "Schedule 1 alone: ⌈log₂(3(c−1)/ε)⌉ per grade suffice."
- **rem:zero-sum (D3):** A_4(2) = 243.
- **D4:** the new §5.1, and one sentence after lem:exponent ("E_1 is Schedule 1 alone").
- **Proof of thm:main (D5–D9):**
  - Procedure: M_d = A_d(g_d), the Schedule 1H preprocessing, and merges with cut-off attempts on
    saved labels.
  - Correctness: random coins do not matter by prop:descent; the abort budget is ε/3 in total.
  - Approximation: no quantum step is repeated.
  - Query count: both bounds.
  - Running time: solver attempts, preprocessing attempts and tables.
- **D10:** rem:oblivious (restart wording).
- **D11:** Heisenberg example (4 for every p, with the mechanism).
- **D12:** rem:proof-uses (thm:halving; the witness also depends on the coins).
- **D13:** class-3 example (A_3(2) = B_3(2); A_2(3) = 16; Q_q ≈ 2^{17.68}).
- **D14:** table caption and rows (§2).
- **D15:** rem:query-separation(b).
- **F1–F4:** rem:main-solver title; the black-box paragraph "stated with the solver of Theorem main
  alone (no Schedule 2)"; the Outlook "Corollary nilpotent … with Schedule 1H alone (no
  Schedule 2)"; thm(3) punctuation.
- **Outlook (O1–O4):**
  - Preamble.
  - "Smaller arities": "the exponent 53 of Schedule 1 alone". It adds "These combinations do not use
    the halving …, which by itself gives 38; how far the two can be combined is not claimed". The
    values **40 and 37 are kept unchanged and conditional**, and R7 = 25 is not mentioned.
  - The "Halving the degree" paragraph is **replaced** by a short "Halving at the confirmed depth"
    paragraph (95 in place of 145, without L_d; AI-checked and refereed by AI).
  - Open problem (1) cites both lemmas.
- **Artifacts (A1–A3):**
  - The new item for `halved_schedule.py` and the referee's independent code.
  - The macro sentence now admits the hand-added 38.
  - A new finite-check item for the executors.

Black-box corollaries: their stated query bounds ∏B_d(·) remain valid upper bounds, since
A_d ≤ B_d. They were not tightened.

## 4. Numbers

- `\newcommand{\ReesClassNineHalvedExp}{38}` was hand-added after `\ReesClassNineQueryExp`, with
  the comment `% hand-added 2026-11-13, source: s1h_independent.out`. It is identical in
  `core/numbers.tex` and `numbers.tex` (`numbers.diff`).
- **Consequence: `tests/tools/test_rees_paper_numbers.py::test_rees_numbers_tex_is_up_to_date`
  now FAILS.** It compares `numbers.tex` with the `make_numbers.py` rendering. The other 57 tests in
  the 53-pass test set pass. There are two fixes, both outside my brief:
  - (a) add the value to `numbers_map.json` with a JSON source;
  - (b) remove the line from the top-level `numbers.tex`, which only the full version reads, and
    which does not use the macro.

  Also, anyone running `make_numbers.py` will delete the macro and break the core build (TRAPS 17).
- Derived macros (`SdeAttempts` 441, `OrigQueriesBits` 564, `InstCallsBits` 561, `ReesOuter*`
  55/794) are **not used in the core** (checked by grep). They remain the Schedule 1, exponent-53
  values of the full version. Nothing in the core prints a number derived from 53 except where it is
  labelled "Schedule 1 alone".
- Every core number that depended on the arities was recomputed (§2): the table, query-separation,
  examples and rem:zero-sum.

## 5. METADATA and compile

- `arxiv/METADATA.md`: the abstract gets the same phrase ("(at most 38 at $c=9$)"), giving 1,919
  characters (limit 1,920; the header is updated). **"Comments: 50 pages" was left unchanged** (it
  is outside abstract scope); it should now read 55. `arxiv/main-core.tex` and `arxiv/numbers.tex`
  are stale until `build_package.sh` is rerun.
- Compile in `core/` (nice -n 19; pdflatex, bibtex, pdflatex, pdflatex): **55 pages, 0 errors,
  0 undefined references, 0 Overfull, 0 Underfull, bibtex 0 warnings.**

## 6. Remark text for the full version (not applied; another agent owns `main.tex`)

Suggested placement: after rem:combined-schedule, or in the Schedule 1 notes.

> \begin{remark}[Halving the degree; core version]
> The core version proves (its Section~5.1, Schedule~1H) that at an even degree $\kappa_d$ a
> solver for the exponent $\kappa_d/2$ may replace Schedule~1: a relation whose coefficients are
> $(\kappa_d/2)$-th powers splits into two parts with $\kappa_d$-th-power weights and yields one
> vector with two disjoint representations, of ratio $\varepsilon = -q^{-1}$ with
> $q^{(p-1)/\kappa_d} = -1$; after $s$ such stages, a zero of the accumulated representations or one
> linear relation among $g_d+1$ such vectors closes the merge (the latter for every
> $p \ge 4\kappa_d^4$, by Weil's bound for diagonal equations). The solver is Las Vegas inside each
> merge and is charged as in the solver part of the error split. With Schedule~1 at depth $L_d$ as
> the inner solver, the class-nine exponent of $m$ drops from $\ReesClassNineQueryExp$ to $38$,
> attained exactly at $p \equiv 1 \pmod{2520}$; at the full depth $\lceil\log_2(\kappa_d+1)\rceil$,
> from $145$ to $95$. The core's main theorem uses this solver. The statements of this version,
> which use Schedule~1 (and Schedule~2), remain valid as written, since the halved arity never
> exceeds $B_d$. AI-proved and refereed by AI, pending human review.
> \end{remark}

## 7. Open items an independent referee must check

1. **§5.1 line by line.** This covers Lemmas stage, finish and two-term, Definition schedule1h,
   Theorem halving (i)–(iii), Corollary hcd and Remark kappa-two. It is **new write-up text**: the
   referee of 11-12 read the attack's version, not this one.
2. **Lemma two-term:**
   - it relies on Weil for diagonal equations with coefficients ε, η, and on the inequality chain
     at √p ≥ 2κ²;
   - the LN Thm 6.37 locator is still unverified (existing flag).
3. **Theorem halving(ii):** the expected-time bound is "explicit polynomial" with a recursion. Is
   the cut-off T well defined? The bounds of sA_κ calls and roots and s ≤ max(κ+1, log₂G^L) also
   need checking.
4. **Error accounting:**
   - rem:is-import(d): n_pre ≤ 2(c−1) and the ε/6 + ε/6 split;
   - the claim that a mid-run abort (after queries) is fine;
   - the ε/3 + ε/3 + ε/3 total in the proof.
5. **Lemma halved-exponent:**
   - the hand tail (ê table; ê(κ) ≤ ê(d) with equality only at κ = d);
   - (i) the lower bound;
   - (iii) C^H_c, where for general c the constant is only shown finite;
   - the K-check in the JSON.
6. **Independence/exactness:** the witness now uses classical coins. prop:descent gives exactness
   for every nonzero solution, so the outputs are independent of the coins. Confirm this.
7. **Recompute:** the table (`halved_schedule.json` "crossover") and the class-9 profile maximum,
   by independent code. The table is the one number set not cross-checked by a second program.
8. **The tie and argmin conventions:**
   - A_κ is min-arity, while e^H is min-degree over the same candidates;
   - check that thm(iii) really bounds the min-arity choice;
   - check that the inner solver of a plan is the min-arity H_D.
9. **Wording:** "deterministic if every plan run is at κ′ with p < 4κ′⁴", including the q table at
   small p.

## 8. Adversarial self-check

- **Did I just transcribe the attack?** No. I restated the rule differently, re-derived each proof,
  and changed three things:
  - Weil-diagonal in place of Hasse–Weil, which removes an import;
  - no F2;
  - multi-stage plans only below 4κ⁴.

  I then recomputed E_H for *my* rule with my own code; it matches the referee's code for a
  different rule. A shared conceptual error is still possible in the cost model: arity is the
  product of the inner arities. Lemma S/F and the executor make this concrete.
- **Is "38 for every p > 9" really covered?** Below 26244 it is covered by exact computation
  (finite, AI-run), and above by the hand argument. The hand argument uses lem:zero-sum-length(ii)
  and (iii), plus two-term. The upper bound needs only that each grade has *some* candidate of the
  stated degree.
- **Las Vegas versus "deterministic".** Every merge-level "deterministic" in the core now refers to
  Schedule 1 alone. I grepped for "deterministic": the procedure itself now never claims
  determinism. Should the owner require determinism, the honest fallback is 53, deterministic given
  the precomputed zero sums.
- **Table risk.** The new Q_q uses min-arity, and the maxima were found over p < 30000 plus the
  residues. For p ≥ 26244 the arity depends only on p mod 5040, as κ_d and the parity of h do, so
  the residue scan is complete. The scan is not independently reproduced.
- **Monotonicity used by the black-box corollaries.** "B_d is increasing" is still applied to B_d,
  not to A_d. Those bounds stay true as upper bounds. A_d monotonicity is not claimed.
- **Weakest points:**
  - (1) §5.1 has had no referee in this form.
  - (2) Everything still inherits lem:rounds, AI-only and unconfirmed by Ivanyos.
  - (3) The numbers test fails because of the brief's hand-added macro.
  - (4) The full version is now behind the core: its headline is 53. §6 gives the bridge remark.

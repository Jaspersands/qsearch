# Check and integration: Rees threshold round 9 (Corollary 3, Remark 5)

5 November 2026, overnight. AI-only adversarial check and integration. This is not a human review.
**AI-checked, pending human review.** Object: `2026-11-05-rees-threshold-9.md` §2.3 (Corollary 3),
§2.4 (Remark 5), §6 (proposed text) and §8 (its first checker's verdict). Own scripts are in
`2026-11-05-rees-threshold-9-check/integrator/`. That folder's parent holds the §8 checker's files,
which were left unchanged. Interpreter `/opt/anaconda3/bin/python`, mpmath 1.3, `nice -n 10`,
one process at a time, under 200 MB.

## Verdict

**No Error. Integrated as one remark plus one sentence.** Corollary 3 survives a line-by-line
re-derivation. Every constant and the κ ≥ 729 cutoff reproduce in mpmath. Remark 5 is correct
as a statement about Theorem 1's certificate. Only Corollary 3 is new relative to the paper.
The barrier is an instance of the BGP barrier the paper already states.

## 1. What TH2 Theorem 5 is, and whether the paper has it

- *What it is.* TH2 is `2026-11-02-rees-threshold-2.md`, §2. Theorem 5 is the central-moment
  certificate G_m(p) = κ[λ^{−2m}A_{2m}(λ) + W_m(λ)·max_{k≤2m} δ_k]. If G_m(p) < 1, then
  p ∉ E_2(κ). Its Corollary 5′ gives 4e⌈ln 4κ⌉²κ^κ + 1 for κ ≥ 32.
- *Whether the paper has it.* It is not proved in the paper. `rem:two-level-threshold-size`
  cites it as an AI-only argument ("this paper does not prove"), with the consequence
  κ^{κ+o(1)}.
- *My re-derivation.* I re-derived the proof: test polynomial (1 − n/λ)^{2m}, binomial
  comparison, Lemma D brackets, A_{2m} from singleton-free partitions, coefficient sum W_m, and
  the union bound. I found no error.
- *Recomputed constants.* A_4 = λ + 3λ² (S₂(4,1) = 1, S₂(4,2) = 3). W_2 = 16 + 24/λ + 11/λ² + 1/λ³
  (from the Touchard polynomials). δ_k ≤ 2(κ−1)(8κ⁴/√p + 4/p) under (κ−1)ε* ≤ 1.
- *Consequence.* Corollary 3 is unconditional only relative to that cited theorem. The paper
  text says so ("If that bound is right").

## 2. Corollary 3, line by line

- **Lemma 2.** Row 0 gives X_j ⊆ Q_{−j}, so the X_j are disjoint. An m-subset of D_S has
  P = Π_i N_i(T)/p. The Weil count with roots −x (distinct) gives N/p ∈ ρ_m(1 ± η_m). Correct,
  and it matches `lem:app-s2-weil-count` exactly, including E_κ(ℓ,p) ≤ (ℓ−1)√p + 1 for ℓ ≤ κ.
- **Theorem 1.**
  - The one-integer Bonferroni identity Σ_{m≤K}(−1)^m C(N,m) = (−1)^K C(N−1,K) is correct.
  - The parities K_r odd for r even and K_r even for r odd give the right directions. The η_m < 1
    hypothesis is needed for every r (§8 fix 1 is correct).
  - The outer Bonferroni with R odd and E C(W,r) = Σ_{|S|=r} P(M_S = 0) are correct.
  - max(L_r,0) and min(U_r,1) are valid.
- **(S1).**
  - η_m is nondecreasing in m. The derivative 1 − 1/κ − κ^{−m}ln κ is positive for κ ≥ 3, the
    constant part is nondecreasing, and E_κ ≥ 0.
  - Upper side: u_m ≤ (x^m/m!)(1+η_K)^{κ−1}, using (rh)^m κ^{−m(κ−1)} = (rΛ)^m.
  - Lower side: 1 − m²/(rh), Bernoulli for (1 − m/p)^{κ−1} and for (1 − η)^{κ−1}.
  - The steps give δ ≤ 2.1κKκ^K/√p. The report then *defines* δ = 3.1κKκ^K/√p, which is looser
    and consistent, and (κ−1)η_K ≤ δ.
- **(S2) and (★).**
  - The Lagrange remainder of e^{−x}, x^n/n! nonincreasing for n ≥ x, and K! ≥ (K/e)^K are
    correct.
  - The binomial step gives Σ_{r≤R}(−1)^r C(κ,r)u^r ≥ (1−u)^κ − C(κ,R+1)u^{R+1}. It follows from
    S_R = S_{R+1} − C(N,R+1) and S_{R+1} ≥ 1[N=0] for N ~ Bin(κ,u). Correct.
- **Range (B)** (R = 1, K = ⌈3.6Λ⌉).
  - 3.6 ln(3.6/e) = 1.01136 ≥ 1, so κ(eΛ/K)^K ≤ μ ≤ e^{−1.5}.
  - (eΛ/K)^K is nonincreasing for K ≥ Λ.
  - 1 − 2e^{−1.5} − 0.5/e = 0.3698 > 0.
  - Side conditions: K̄_B ≤ κ, and √p ≥ κ^{κ/2}.
- **Range (A).**
  - R = 2⌈2μ+2⌉ − 1 ∈ [4μ+3, 4μ+5) and K = ⌈4RΛ⌉. The main term is ≥ e^{−c_main μ}, with
    c_main = 1/(1−e^{−L_0}) = 1.00248.
  - First error: ln 3 − 4 ln(4/e) = −0.447 < 0. The report's constant 1.5448 is slightly
    conservative; the exact value is 1.5452.
  - Second error: exponent per R ≤ 4 ln(e/4)Λ + 1 − ln 4 = −0.545177Λ − 0.386294, which is
    −3.657 at Λ = 6. The report's −0.5448 and −3.655 are conservative.
  - Third error: Σ_{r≤R}C(κ,r) ≤ (eκ/R)^R, ln κ = Λ + ln μ, and μΛ ≤ c_0κ with c_0 = 6e^{−6}.
    These give K̄_A and 2RΛ as stated.
  - Condition (A) then gives each error < e^{−c_main μ}/3. All correct.
- **Range (C).** At λ = √(8κ): 3κ/λ² = 3/8, and the Weil part is < 10^{−900}. G_2 < 1 holds on
  the whole range because each part is monotone.
- **Cutoff** (`integrator/cor3_check.py conditions 1000000` → `conditions.out`; mpmath, 30 digits,
  every κ ∈ [30, 10^6], plus a sample of κ up to 3·10^15).

  | L_0 | last strict failure | last failure with margin 1 | minimum slack beyond the cutoff |
  |---|---|---|---|
  | 6 | 727, from (A) | 728 | (A) 1.74 at κ = 729; (B) and (C) never bind |
  | 5.5 | 1675 | 1676 | (A) 1.01 at κ = 1677 |

  So the stated cutoffs 729 and 1677 are the margin-1 values. They are conservative by one.
  - 16c_0 = 0.23796, so the κ > 10^6 tail with K̄_A ≤ 0.2383κ is right.
  - L_0 = 5 fails (16c_0 = 0.539 > 1/2). That is right.
- **Direct evaluation** (`integrator/star.out`).
  - (★) with the exact binomials, on Λ ∈ [6, √(8κ)] in steps of 0.01 at κ = 729: minimum 0.1638
    at Λ = 6. At κ = 1677, L_0 = 5.5: minimum 0.00104 at Λ = 5.5. Both are positive.
  - TH2's exact G_2, with its own δ_k, at p = √(8κ)κ^κ + 1: 0.3766 (κ = 729) and 0.3761
    (κ = 1677).

## 3. Remark 5 (barrier)

- **Step 1.** For p ≤ κ^κ/2, η_{κ−1} ≥ 1, so every admissible K_r ≤ κ − 2. Numerically, the
  minimum of η_{κ−1} at p = κ^κ/2 over 3 ≤ κ ≤ 400 is 1.626, at κ = 3 (`barrier.out`; η decreases
  in p). η_m is nondecreasing in m, with 0 violations (3 ≤ κ ≤ 60).
- **Steps 2–3.**
  - BGP Proposition 26 lifts: the positivity indicators are (κ−1)-wise independent
    Bernoulli(q), q = ν(n>0) ≤ E n_0 < p/κ^κ ≤ 1/2. The values are then drawn from ν
    conditionally. The result agrees with ν^{⊗S} for |S| ≤ κ−1 and gives probability 0 to all
    columns being positive.
  - By Vandermonde, an order-m moment of M_S involves ≤ m ≤ κ−2 coordinates. This holds even for
    |S| = κ.
- **Step 4.** Superadditivity of c(m) and d(m), η_a + η_b ≤ η_m/κ, and
  ρ_aρ_b/ρ_m = 1 + ab/(p(p−m)) were all re-derived. The 13/36 and 0.023 constants are correct.
  Numerically, 5841 pairs (3 ≤ κ ≤ 40, six p values ≤ κ^κ/2) gave 0 failures. The largest
  (ratio − 1)/η_m is 0.067, against the proof's bound 0.4.
- **Is it a theorem?**
  - *Yes, in the form stated in §2.4:* every F of Theorem 1, for any odd R and any admissible K_r,
    is ≤ 0 when p ≤ κ^κ/2.
  - *Also in the precise general form used in the paper:* no lower bound for P(all n_j ≥ 1) that
    is valid for every law on ℕ^κ satisfying the two-sided brackets of Lemma 2, for all S and all
    m with η_m < 1, is positive at such p.
  - *Not a theorem:* the informal phrase "every certificate built from Weil-bounded moments of at
    most κ−1 columns". It names no class of certificates. Moreover Theorem 1 uses |S| up to κ,
    restricted to orders ≤ κ−2.
- **[Gap, scope]** The proof does not cover a variant that keeps the one-sided upper brackets
  u_m for orders m ≥ κ−1, where η_m ≥ 1. Step 4(ii) uses η_m < 1. Such a variant plausibly
  fails too, since BGP only lowers E Π_j n_j, but that is not proved. The paper text is worded
  to the η_m < 1 class.
- **Positivity window.** "Never positive for κ ≤ 27" is a grid computation (`scan_small.out`, by
  the §8 checker). It was not re-run here. The paper states it as a finite computation on a
  grid, and nothing depends on it.

## 4. Consistency and novelty

- **`rem:two-level-threshold-size`** already states two things:
  - the TH2 bound 4e⌈ln 4κ⌉²κ^κ + 1, that is κ^{κ+o(1)}, as argued and not proved;
  - the BGP barrier: no argument using statements about ≤ κ−1 columns, each true under
    independence, can certify p ≤ κ^κ/2.

  Remark 5 is an instance of that barrier. Its only new point is that Theorem 1's |S| = κ terms
  stay inside it. The central-moment bound κ^{κ+o(1)} is therefore *not* superseded in kind.
- **What is new.** Corollary 3 sharpens the bound to O(κ^κ), namely 6κ^κ + 1 for κ ≥ 729. At
  κ = 729 that is a factor 4e⌈ln 4κ⌉²/6 = 116 below Cor. 5′, and with the barrier the method is
  pinned within a factor 12. Lemma 2, Lemma D for several columns at once, is also new to the
  paper.
- **`app:s2-local`** gives lower bounds on E_2, of the form p ≤ κ² − 3κ + 3, and r-row
  obstructions void above ((r−1)κ^r + 2)². These are compatible.
- **`app:s2-chains`** is a different, cubic-arity construction. There is no overlap.
- **Known members.** The largest known E_2 members (≤ 1.7κ^{(κ+1)/2}) lie far below 6κ^κ. TH3's
  O1 bound 2^{−1/(κ−1)}κ^κ is compatible.
- **`tab:app-s2-thresholds`.** Unaffected (κ ≤ 9).

## 5. Integration (applied)

- **`appendix-schedule2.tex`.** New `rem:app-s2-joint-moments`, after the remark on where the
  values of Δ and U come from, at the end of `prop:app-s2-TA`'s material and before
  `cor:app-s2-decoupled`. It contains:
  - the Lemma 2 brackets with their one-line proof;
  - the double Bonferroni idea;
  - Corollary 3, stated conditionally on TH2 Theorem 5, with the 5.5κ^κ variant;
  - "does not close the square gap";
  - T_A and the table unchanged for κ ≤ 27;
  - the barrier in its precise form.
- **`main.tex` `rem:two-level-threshold-size`.** One sentence is extended after "at most
  κ^{κ+o(1)}". It gives 6κ^κ + 1 for κ ≥ 729, O(κ^κ), not below κ^κ/2 for those moments, with
  a pointer to the remark, AI-checked, pending human review.
- **Unchanged.** No change to the table numbers, `numbers.tex`, E_W, claim gates, bib or
  `main-full-draft.tex`. No forbidden macros: `\mathsf`, `\mathrel`, `\begingroup`, `\aa`, `\ni`
  are absent from the diff.
- **Backups** are in the session scratchpad, `backups/`.
- **Build** (scratch copy in `$TMPDIR/rees-th9-build`, `latexmk -g -pdf`):
  - exit 0, 173 pages;
  - 0 Overfull, no undefined references or citations, no "Float too large";
  - 3 Underfull.
- **Tests.** `tests/tools/test_rees_paper_numbers.py`: 2 passed. `make_numbers.py` was not run.
- **Also updated.** `REES_FULL_CONTINUATION.md` item 2, and integration log row I220. No git.

## 6. Claim gates (stay false)

- Exponent below κ.
- Square gap closed.
- Any change to E_2(κ) for κ ≤ 16, to T_A, to `tab:app-s2-thresholds` or to Schedule 2.
- Any priority claim (Brun/Bonferroni on Weil-controlled moments is standard).
- Corollary 3 claimed without its dependence on TH2 Theorem 5.

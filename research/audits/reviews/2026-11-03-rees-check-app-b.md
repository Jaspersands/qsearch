# Unanchored proof check of Appendix B (Schedule 3, `thm:random-column`), and of the free-coordinate appendix

Round 4, item 2 of `research/REES_FULL_CAMPAIGN_4.md`. AI session (Claude Code), 2–3 November 2026.
No human review. Edits nothing outside this file and the folder `2026-11-03-rees-check-app-b/`.

Files checked:
- `docs/papers/rees-hsp/appendix-schedule3.tex` (sha1 `e04a1df4`), with the main.tex statements it
  uses: `def:input-contract`, `thm:rees-cover`, `lem:homogeneous`, `lem:copy-lift`, `prop:refresh`,
  `lem:central`, `prop:descent`, `sec:recursion` with `lem:hybrid`, `thm:random-column`,
  `rem:combined-schedule`, `thm:uniform-compilation`, `cor:fpt-r`, `cor:codim`.
- `docs/papers/rees-hsp/appendix-free-coordinate.tex`, snapshot sha1 `39591e85` (mtime 2 Nov 21:40,
  still being written in parallel when read), with `thm:free-coordinate` and `prop:rc-lower`.

Order of work: I read the appendix and the body statements first and formed my own verdict on each
lemma (§1–§2). Only then did I read `2026-11-02-rees-schedule3-cost.md` and the round-2 hand-over
note (§3). The free-coordinate appendix came last (§4).

Scripts (folder `2026-11-03-rees-check-app-b/`; independent code that imports nothing from the
repository; every decision uses Python integers or `fractions.Fraction` unless marked float):

```bash
cd research/audits/reviews/2026-11-03-rees-check-app-b && /opt/anaconda3/bin/python -I ineq_check.py 80 > ineq_check_out_u80.txt
cd research/audits/reviews/2026-11-03-rees-check-app-b && /opt/anaconda3/bin/python -I moment_exhaustive.py > moment_exhaustive_out.txt
cd research/audits/reviews/2026-11-03-rees-check-app-b && /opt/anaconda3/bin/python -I root_bezout_check.py > root_bezout_check_out.txt
cd research/audits/reviews/2026-11-03-rees-check-app-b && /opt/anaconda3/bin/python -I bank_event_exact.py > bank_event_exact_out.txt
cd research/audits/reviews/2026-11-03-rees-check-app-b && /opt/anaconda3/bin/python -I node_sim.py > node_sim_out.txt
cd research/audits/reviews/2026-11-03-rees-check-app-b && /opt/anaconda3/bin/python -I fc_check.py > fc_check_out.txt
```

Each runs in under two minutes. All six report 0 failures. Their outputs are in the folder.

## 0. Verdict

- **No counterexample to any statement of Appendix B. Every lemma, the proof of
  `thm:random-column` (i)–(ii), and the uniformity in c (`prop:s3-uniform`) hold as written.**
  This verdict is "proved (AI-checked, pending human review)". Each step checks out line by line,
  and the finite-checkable claims hold in exact arithmetic (§2).
- **Uniformity in c is real.** The class enters only through T ≤ M^{c−1} ≤ (4u)^{u−1}, through
  B = ⌈log₂(64(4u)^{c−1})⌉ ≤ 6 + (u−1)⌈log₂ 4u⌉, through c queries per leaf, and through the BCH
  bracket count (c−1)c(c+1)(c+2)/6 ≤ u⁴. Every probability bound uses only κ_d ≤ c ≤ u,
  a_d ≤ u−1, M = 4u and p ≥ 16u². I checked them in exact arithmetic for all 2 ≤ c ≤ u ≤ 80.
- **Label law and abort rule: sound.** The abort-sum argument (`lem:s3-tree`(b)) conditions each
  node on the event "no earlier node aborted". Under that event its inputs are still
  ρ_{H_d}^{⊗M}, in product with the record (`lem:s3-tree`(a)), because `prop:descent` outputs
  ρ_{H_{d−1}} on every accepted record and consumes every target. A bank is not i.i.d. given its
  own acceptance (`rem:s3-caveat`, numbers re-verified: N = 34⁷−1 against 34⁶−1, ratio 34.00).
  The proof never needs that, because nothing reads a bank after acceptance.
- **Findings, none of which changes a statement** (fixes in "Proposed paper text"):
  1. An arithmetic slip in the proof of `prop:s3-uniform`(a). It prints 2^{−20} + 2^{−37}; the
     second term is 2(64)^{−7} = 2^{−41}. The bound < 2^{−17} still holds.
  2. The dependency list at the start of the appendix (line 43) names three body results. The
     proof also uses `thm:rees-cover`, `lem:homogeneous` (or `lem:copy-lift` for copy input) and
     `lem:hybrid`. Line 312 lists them, so the list at line 43 is incomplete.
  3. Coset-copy input (`def:input-contract`(iii), second option) is not mentioned. A leaf is
     described only as "prepared with c oracle queries", while `lem:copy-lift` gives the same
     source from c copies.
  4. The base case of `lem:s3-tree`(a) says the open registers at j = 0 are the leaves. That
     presumes every leaf is prepared up front. With depth-first, lazy preparation, leaf
     preparations must be steps of the induction. The induction is the same either way.
  5. The proof of part (ii) applies `lem:s3-tree`(a) "to all 4m′ trees jointly". The lemma is
     stated for one tree. The forest version follows by the same induction over any
     interleaving, but it should be said.
  6. The proof of `lem:s3-hybrid` says the slot input "is block-diagonal in the record". The body's
     `lem:hybrid` instead has each slot dephase the record first. That is the cleaner hypothesis
     for a diamond-norm statement, and the appendix could simply cite `lem:hybrid`.
  7. Several symbols clash: the trial coefficients c_l against the class c; the side system X
     against the matrix X; the Bezout β against β_d; the trial count K against K_d; the generic
     attempt cap R against the round cap R; the counts s₌, s_≠ against the witness s.
  8. `thm:random-column` allows c ≤ u with no lower bound, but the tree is defined with a root
     of degree 2. For c = 1 (abelian) the theorem is vacuous or needs a sentence.
  9. Looseness, not error. `lem:s3-moment`(d) gives 2p^{a−1−M}, and the paper prints 2p^{a−M}.
     The restart bound gives 2^{−8m′}, and the paper prints 2^{−2m′}. Both are true.
- **On the theorem's title, "conditional on the label law".** Under `def:input-contract`, the
  appendix *derives* the label law (`lem:s3-law` with `lem:s3-tree`(a)) from `lem:central` and
  `prop:descent`. So it is not an extra hypothesis on instances. What is extra over Schedules
  1–2 is that the guarantee is only for the ideal i.i.d. supply, not for an arbitrary bank.
  Whether to reword the title is a status decision for the owner. I propose a clarifying
  sentence only (§6, P8) and flip nothing.
- **Free-coordinate appendix (snapshot 39591e85): no counterexample either.** I checked every
  lemma and the proofs of `thm:free-coordinate` (i)–(iii) and `prop:rc-lower` (§4), with exact
  checks in `fc_check.py`. Minor: the symbol R is both the echelon form and the round cap in the
  same lemma, and N is both the solution count and the number of sampler nodes.

## 1. Per-statement verdicts (Appendix B)

Labels: **proved** = I re-derived it and found it correct; **exact** = finite exact computation
by my scripts; **float** = floating-point or sampled statistic. "Smallest counterexample" means the
smallest instance I could find that breaks it; "none" means none exists, because the proof is
valid.

| Statement | Verdict | Checks | Smallest counterexample / fix |
|---|---|---|---|
| Setting (§B.1): κ = gcd(d,p−1), P_κ, S; image of x↦x^d is the κ-th powers; Bezout eq. `s3-bezout` | proved | exact: `root_bezout_check.py` [R4], all p ≤ 400, d ≤ 16, every t | none |
| Capped field draw: accept prob p/2^ℓ > 1/2, timeout < 2^{−R} | proved (p odd, so 2^{ℓ−1} < p) | — | none; rename R (P6) |
| Node procedure (N1)–(N6); F = KM + MLR bounds draws; (N5) always passes | proved | exact runs: `node_sim.py`, 74 banks over 7 parameter sets incl. κ = 1, 2, 3, κ < d, a = 0; all accepted and verified; a rank-2 bank at u = 2 aborts in (N2) | none |
| Tree shape: M^{c−1} leaves, T = (M^{c−1}−1)/(M−1) nodes | proved | exact: `ineq_check.py` | none; add c ≥ 2 (P7) |
| `lem:s3-law` (product form, i.i.d. uniform labels on K_d^⊥) | proved, given `lem:central` | — | none |
| Intrinsic coordinates: Λ = EX, ker Λ = ker X, (N2) never aborts on the ideal support | proved | — | none |
| `lem:s3-moment`(a) classes of size h on distinct lines | proved | exact: `moment_exhaustive.py`, 16 cases | none |
| `lem:s3-moment`(b) E N = hμ, Var N = h²\|D\|q(1−q) ≤ h E N | proved | exact equality in all 16 cases (incl. κ = p−1, κ = 1, a = 0) | none |
| `lem:s3-moment`(c) Chebyshev 4/μ | proved | exact | none |
| `lem:s3-moment`(d) rank bound | proved (loose by a factor p) | exact | none |
| `lem:s3-mu`(a) μ ≥ 2^{8u+1}u^{2u+1} | proved | exact identity u ≤ 80; exact μ at least prime ≥ 16u² and 2^61−1, every d ≤ u, a ∈ {0,u−1} | none |
| `lem:s3-mu`(b) acceptance ≥ 1/(4κ^M) | proved (uses p ≥ 2κ) | exact, same range | none |
| `lem:s3-root`(a) distinct linear factors | proved | — | none |
| `lem:s3-root`(b) split prob ≥ (p−1)/(2p) | proved (Jacobsthal-type count) | exact: [R1] s_≠ = (p−1)/2 for every odd p ≤ 401 and every ρ₁ ≠ ρ₂; [R2] every subset of ≥ 2 roots of x^κ − y, p ≤ 61, κ ≤ 8, every δ | none |
| `lem:s3-root`(c) ≤ ⌈log₂ κ⌉ steps, timeout union | proved | exact: [R3] the procedure, as implemented here, returns a root within ⌈log₂ κ⌉ steps, 9 primes up to 65537, κ ≤ 16 | none |
| `lem:s3-node`(a) bank event ≤ β_d | proved | exact at admissible parameters: `bank_event_exact.py`, a = 1, u = 2, 3, 4, 27 (u,p,d) rows; the exact Pr[bad] is 33 to 4·10⁷ times below β. For u = 2 this is every node's full bank law (a_d ≤ 1) | none |
| `lem:s3-node`(b) per-trial acceptance ≥ 1/(4κ^M) on good banks | proved | exact: same rows (least good-bank acceptance is 3.7–4.3 times the bound); exhaustive small cases | none |
| `lem:s3-node`(c) failure split β_d + 3·2^{−B} | proved | exact: the per-node unions F·2^{−cap} ≤ 2^{−B} and ML(4/9)^{B+⌈log₂ ML⌉} ≤ 2^{−B}, all κ ≤ c ≤ u ≤ 80 | none |
| `lem:s3-node`(d) output ρ_{H_{d−1}} on every accepted record | proved, given `prop:descent` | — | none |
| `lem:s3-node`(e) cost (1+κ^M)·poly | proved | — | none |
| `rem:s3-caveat` p = 67 example | proved | exact: N(e₁) = 34⁷−1, N(e₁+e₂) = 34⁶−1, ratio 34.00000002 | none |
| `lem:s3-tree`(a) factorization | proved | — | none; base-case wording (P4) |
| `lem:s3-tree`(b) abort ≤ Σ_j Pr[abort \| E_j] ≤ T(max β + 3·2^{−B}) | proved | — | none |
| `lem:s3-tree`(c) one tree aborts ≤ 1/16 | proved | exact: both closed forms, the sum < 1/64, 3T2^{−B} ≤ 3/64 and T(β+3·2^{−B}) ≤ 1/16 for all 2 ≤ c ≤ u ≤ 80 (3160 cases) | none |
| `lem:s3-hybrid` | proved | — | none; dephasing wording (P5) |
| Proof of `thm:random-column`(i) | proved | — | none |
| Proof of (ii): restart bound, i.i.d. kept outputs, rank third, N_instr ≤ 13m′M^{c−1} | proved | exact: C(4m′,3m′)·4^{−3m′} ≤ 2^{−2m′} for m′ ≤ 400; the exact Binomial(4m′, 15/16) tail < m′ is ≤ 2^{−2m′} for m′ ≤ 120; the ε-split for ε = 1/k, k ≤ 2000, and for ε ∈ (1,3) | none; forest wording (P3) |
| `prop:s3-uniform`(a)–(e) and the final cost form | proved | exact: (a) β_d ≤ 2^{−17} for u ≤ 80, also at real primes; (b) B bound | arithmetic slip 2^{−37} → 2^{−41} (P1) |
| Application to `cor:fpt-r` (u = r+1) | proved | — | none |
| Scope paragraph | accurate | — | none |

## 2. Attack log (what I tried to break)

**Probability and union bounds.**
- *Coupling of capped and uncapped draws.* The three node failures are: every uncapped trial
  rejects; a root step exceeds R rounds; a capped draw times out. The capped run differs from the
  uncapped one only on the third. The union bound over at most F potential draw slots is valid.
  F is a deterministic bound: N3 uses ≤ K(M−r) ≤ KM draws, and the root steps use
  ≤ M·L·R δ-draws. Checked.
- *Root timeout.* Each round fails with probability ≤ (p+1)/(2p) ≤ 2/3, conditional on the past,
  and each extraction has ≤ L steps. So the total is ≤ ML(2/3)^R with R = 2(B + ⌈log₂ ML⌉).
  Since (4/9) < 1/2, this is ≤ 2^{−B}. Exact for all parameters checked.
- *Trials.* (1 − 1/(4κ^M))^{4κ^M B} ≤ e^{−B} ≤ 2^{−B}. I also checked it exactly where the
  numbers are small.
- *Tree abort.* The first-abort decomposition Pr[abort] = Σ_j Pr[E_j]·Pr[v_{j+1} aborts | E_j]
  is an identity, so no independence between nodes is needed. Each conditional term is
  ≤ β_d + 3·2^{−B}, because the input of v_{j+1} given any record in E_j is the product state.
- *Restarts.* Distinct trees act on disjoint fresh registers with independent coins, so abort
  events are independent in the ideal procedure. The paper's union bound over 3m′-subsets gives
  2^{−8m′}, stronger than the 2^{−2m′} it states. The exact binomial tail confirms this.
- *Final rank.* The kept set is a function of the record. Conditional on the record, the kept
  outputs are i.i.d. ρ_{t𝔥}, so the Fourier samples are i.i.d. uniform on 𝔥^⊥. The failure
  bound is (p^k−1)/(p−1)·p^{−m′} ≤ 1/((p−1)·2^{m′−k}) ≤ ε/3, since m′−k ≥ ⌈log₂(3/ε)⌉.
- *Approximation.* N_instr counts every slot of every attempted tree. Unused slots are
  identities, and the classical steps are exact. In the implemented procedure the label law is
  only approximate, and the rank guard keeps the procedure total. Only the global TV bound is
  used, so the approximate law never needs analysis. Correct.

**Label-law hypothesis.** I tried four ways to break it, and none works:
- *Conditioning on acceptance.* This tilts the bank law (`rem:s3-caveat`), but no later step
  reads that bank.
- *Leftover registers correlated with λ.* None: `prop:descent` consumes all M targets, the zero
  ones included.
- *Coins shared across nodes.* None: the coins are fresh.
- *Approximate instruments.* These are handled by the hybrid, not by the law.

The only true precondition is the one the Scope paragraph states: fresh independent sources
(`def:input-contract`(iii)). The correlated-bank counterexample after `prop:refresh` shows that
correct marginals alone are not enough. Schedule 3 never builds such a bank.

**Abort rule.** I checked three points:
- An aborted tree's registers are never used again.
- The kept set is the first m′ non-aborted trees, which is a record-measurable choice.
- No branch is normalized by a small probability.

There is no postselection. The Theorem 1-style fallback is not needed here, because the
4m′-restart bound already covers aborts.

**Dependence on c.** I traced every occurrence of c:
- the tree depth (T, the leaves, B);
- the queries per leaf (c);
- `thm:uniform-compilation`(i) brackets, ≤ u⁴;
- the cover dimension n ≤ cm ≤ um.

Each is bounded by a function of u alone. The exponent of m stays absolute. B depends on c,
but c is public. I found no hidden c-dependence: μ, β_d and the acceptance are all c-free.

**Edge cases tried.** Each holds:

| Edge case | Result |
|---|---|
| a_d = 0 | labels all zero, N = \|S\|, no bad bank; node simulation accepted |
| κ_d = 1 | no roots needed; Bezout only (p = 149 and 257, d = 3) |
| κ_d < d | p = 263, d = 4, κ = 2 |
| κ = p−1 | outside the theorem, since κ ≤ u < p−1; included in the exhaustive moment check, where the identities still hold |
| ε ∈ (1, 3) | holds |
| m = 0 | m′ = ⌈log₂(3/ε)⌉ ≥ 1 when ε < 3 |

## 3. Comparison with `2026-11-02-rees-schedule3-cost.md` (read after §1–§2)

The prior review is about cost and a better sampler, not a line-by-line audit of Appendix B. On
the overlap:
- **Agreement.** Its Prop 6.1 says uniform-kernel rejection has mean acceptance
  (q^{M−r} − p^{−(M−r)})q^r ≤ q^M. This matches `lem:s3-mu`(b) and `rem:s3-caveat`: the factor
  κ^M is intrinsic to the sampler, not slack in the proof. My exact bank-event table shows the
  least good-bank acceptance is about 4 × 1/(4κ^M), and Pr[bad bank] is far below β. So the
  proof's constants are loose, but they are of the right order.
- **Bezout.** The review uses t ≡ (d/κ)^{−1} mod h. The appendix uses α with αd + β(p−1) = κ.
  Both are valid ([R4] checks the appendix's form exhaustively).
- **Restart bound.** The review mentions "Hoeffding on 4m′ trees". The appendix uses a union bound
  over 3m′-subsets. Both are valid, and the appendix's is elementary.
- **No conflict found.** The review flags nothing wrong in `thm:random-column`. The round-2
  hand-over note in the shared notes folder also found nothing, and it noted the 2^{−8m′} slack
  independently. It missed the 2^{−37} slip and the items under findings 2–8.

## 4. Free-coordinate appendix (`appendix-free-coordinate.tex`, snapshot 39591e85)

Read after §1–§3. It was being written in parallel; this verdict applies only to that snapshot.

| Statement | Verdict | Checks | Counterexample / fix |
|---|---|---|---|
| Setting, eq. `fc-q` (1/κ ≤ q ≤ 1, 1/q ≥ κe^{−(κ−1)/p}); β monotone in a | proved | — | none |
| (F1)–(F6), F_p^× draws (success ≥ 1/2 since p−1 ≥ 2^{ℓ−1}), F_r, irrational T_r remark | proved | — | rename the round cap R (it clashes with RREF R) |
| `lem:fc-rref`(a) RREF(Λ) = RREF(X) | proved | — | none |
| `lem:fc-rref`(b) R[:,F′] uniform given (r, π) | proved (GL_M-invariance + Grassmannian transitivity) | exact: every bank in 8 cases, every pattern; each block value occurs equally often | none |
| `lem:fc-rref`(c) pivot event | proved | exact | none |
| `lem:fc-moment` mean, Var = h^{n+1}(q^r − q^{2r}), Chebyshev, fixed-x identity | proved | exact: 6 cases, by enumerating every C | none |
| `lem:fc-node`(a)–(e) | proved | exact: Pr[not good] ≤ β, acceptance ≥ q^r/2 on good banks, every accepted y in ker X and nonzero, 8 cases (β > 1 there, so the bank bound is not tight in those tiny cases) | none |
| Proof of (i) | proved | — | none |
| `lem:fc-params` (h ≥ 15u; closed forms; tree sum < 1/64) | proved | exact u ≤ 80; u = 2 terms 4/50625 = 1/12656.25 and 1/16384 | none |
| Proof of (ii) (reuses `lem:s3-tree`, restart, hybrid) | proved | — | none |
| (R1)–(R4), Γ_F/Γ₁/Γ₀ split (Γ₀ ⊆ {p−1}, nonempty only when p = c+1) | proved | — | none |
| `lem:fc-choice` β ≤ τ, size display | proved | exact: β ≤ τ in 6840 cases (p up to 10⁶+3, κ ≤ 39, g ≤ 30, τ down to 2^{−100}); float: M_d ≤ display, max ratio 0.931 | none |
| `lem:fc-forest`(a)–(b), the 2ε/9 node budget | proved | — | none |
| Proof of (iii), 8ε/9 total | proved | — | none |
| `prop:fc-uniform`(a)–(b) | proved | exact: node bound < 2^{−14} | none |
| §fc-numbers (q₄^{−14} ≈ 2^{27.99}, 2B ln 2 ≈ 2^{5.79} at B = 40; u = 18, M = 72, n₀ = 37, B = 56) | arithmetic re-done by hand: correct | — | the table itself was not re-run here |
| Proof of `prop:rc-lower` | proved, for candidate laws fixed in advance (as stated) | exact: uniform-kernel mean over generic banks = (q^n − p^{−n})q^a in 8 cases; the p = 5 example (−2x ∈ {3,2} ∉ D) | none |

One point to keep: `prop:rc-lower` covers candidate laws that do not depend on R′. A design that
chooses its next candidate from earlier accept/reject outcomes reads the bank through them, and
the stated union bound does not cover it. The paper's wording ("drawn from any law that depends
on the pivot pattern and private coins but not on the other entries of R") excludes such designs
correctly. It should stay that way. The Scope paragraph says so.

## 5. Exact statement that now holds

Assume `def:input-contract`, with fresh independent sources. Assume also the body results
`thm:rees-cover`, `lem:homogeneous` (or `lem:copy-lift`), `lem:central`, `prop:descent`,
`lem:hybrid` and `thm:uniform-compilation`. Let u ≥ 2, 2 ≤ c ≤ u, a_d ≤ u−1 at every grade,
p ≥ 16u², and M = 4u. Then `thm:random-column` (i) and (ii) hold exactly as stated. The cost is
2^{C₁u log(u+2)}·((m+1)(w+1) log p·log(4/ε))^{C₂}, with C₁ and C₂ absolute and independent of c.
I proved this, and the AI check found no counterexample; it is pending human review.

Under the same body results, `thm:free-coordinate` (i)–(iii) and `prop:rc-lower` hold as
stated in snapshot 39591e85. Part (iii) also relies on Schedule 1 at the zero-sum grade
d = p−1 = c (only when p = c+1), and on the linear schedule at the κ_d = 1 grades. I proved
this, and the AI check found no counterexample; it is pending human review.

**Still missing:**
- Human review of both appendices and of the body results they import.
- The free-coordinate appendix was still being written. Re-check any later edits.
- I did not re-run the class-nine table (`tab:fcs-budget`) script myself. I only checked its
  arithmetic.

**Claim gates that must stay false:** every gate in `research/registry/conjectures.json` and every
`claim_gates` block. In particular these stay false: human-reviewed status of either appendix;
polynomial-time Schedule 3; worst-case (law-free) guarantees for Schedule 3; and any use of
Schedule 3 in `thm:main`. This report flips nothing.

## 6. Proposed paper text

All of it targets `docs/papers/rees-hsp/appendix-schedule3.tex`, except P10. Status of each: an
editorial or accuracy fix, AI-checked, pending human review. None changes a theorem statement or
a status label. For the integrator only.

**P1** (proof of `prop:s3-uniform`(a), line 303). Replace

```latex
which decreases in $u$ and is at most $2^{-20} + 2^{-37} < 2^{-17}$ at $u = 2$.
```
with
```latex
which decreases in $u$ and equals $2^{-20} + 2^{-41} < 2^{-17}$ at $u = 2$.
```

**P2** (line 43, dependency list). Replace

```latex
The proof uses three results from the body of the paper: Lemma~\ref{lem:central} (the branch law of the central instrument), Proposition~\ref{prop:descent} (pointwise quotient conversion) and the recursion of Section~\ref{sec:recursion}. It uses no other step of the paper, apart from the gate counts of Theorem~\ref{thm:uniform-compilation} in the cost bound of Section~\ref{app:s3-uniform}.
```
with
```latex
The proof uses the following results from the body of the paper: Theorem~\ref{thm:rees-cover} and Lemma~\ref{lem:homogeneous} (or Lemma~\ref{lem:copy-lift} for coset-copy input) for the lifted sources, Lemma~\ref{lem:central} (the branch law of the central instrument), Proposition~\ref{prop:descent} (pointwise quotient conversion), and the recursion of Section~\ref{sec:recursion} with its hybrid convention (Lemma~\ref{lem:hybrid}). It uses no other step of the paper, apart from the gate counts of Theorem~\ref{thm:uniform-compilation} in the cost bound of Section~\ref{app:s3-uniform}.
```

**P3** (proof of the theorem, part (ii), line 272). Replace

```latex
Applying Lemma~\ref{lem:s3-tree}(a) to all $4m'$ trees jointly, whose registers are in product, shows
```
with
```latex
The induction of Lemma~\ref{lem:s3-tree}(a) applies verbatim to the forest of all $4m'$ trees, executed in any interleaved order, because their leaves are fresh, their registers are disjoint and their coins are independent. It shows
```

**P4** (proof of `lem:s3-tree`(a), line 235). Replace

```latex
Induction on $j$. For $j = 0$, the open registers are leaves, each a fresh lifted source $\rho_{\exp(\hlift)} = \rho_{H_c}$ (Lemma~\ref{lem:homogeneous} and Section~\ref{sec:rees-cover}), prepared on fresh registers and therefore in product. Assume the claim for $j$.
```
with
```latex
Induction on $j$. Each leaf is a fresh lifted source $\rho_{\exp(\hlift)} = \rho_{H_c}$ (Lemma~\ref{lem:homogeneous} and Section~\ref{sec:rees-cover}, or Lemma~\ref{lem:copy-lift}), prepared on fresh registers. Whether all leaves are prepared before $v_1$ or each just before its parent runs, a new leaf is in product with the record and with every open register, so the claim is preserved by leaf preparations; at $j = 0$ the open registers are the leaves prepared so far. Assume the claim for $j$.
```

**P5** (proof of `lem:s3-hybrid`, line 260). Replace

```latex
A classically controlled channel whose branches are each within diamond distance $2\eta$ is itself within $2\eta$, because its input is block-diagonal in the record.
```
with
```latex
Let each slot first dephase the record registers it reads, as in Lemma~\ref{lem:hybrid}; on the states that occur this changes nothing, since the records are classical. A channel controlled by a dephased classical register whose branches are each within diamond distance $2\eta$ is itself within $2\eta$.
```

**P6** (notation, optional, global within the appendix). Make these renames:
- In (N3), the coefficients `c_1,\dots,c_{M-r}` and `\sum_l c_l k_l` become `\theta_1,\dots,\theta_{M-r}` and `\sum_l \theta_l k_l`.
- In §B.1, the Bezout pair `\alpha, \beta` becomes `\alpha, \alpha'`, with eq. `s3-bezout` updated to `\bigl(t^{p-1}\bigr)^{-\alpha'}`, as the free-coordinate appendix already does.
- In "Capped subroutines", "A draw with attempt cap $R$ times out with probability less than $2^{-R}$" becomes "A draw with attempt cap $R'$ times out with probability less than $2^{-R'}$".
- The side system `X` in `lem:s3-law`, `lem:s3-node` and `lem:s3-tree` becomes `\mathcal{X}` (`\omega_{\mathcal{X}}`), so that it is not confused with the intrinsic label matrix $X$.

**P7** (after "The parameters are as in the theorem.", line 50). Insert:
```latex
We assume $c \ge 2$; for $c = 1$ the group is abelian and abelian Fourier sampling alone returns $\hh$.
```

**P8** (Status paragraph, line 41, optional; owner decision, no gate change). Append:
```latex
The label law used below is not an extra hypothesis on instances of Definition~\ref{def:input-contract}: Lemmas~\ref{lem:s3-law} and~\ref{lem:s3-tree}(a) derive it from Lemma~\ref{lem:central} and Proposition~\ref{prop:descent} for fresh ideal sources. What Schedule~3 adds to the assumptions of Theorem~\ref{thm:main} is that its guarantee is for that i.i.d.\ supply only, not for an arbitrary or correlated bank.
```

**P9** (optional, `lem:s3-moment`(d)). It could state the sharper bound $\le 2p^{a-1-M}$. No downstream change is needed.

**P10** (`appendix-free-coordinate.tex`, optional). Rename the round cap `R` in (F1)–(F6) and
in `lem:fc-node`(c),(e) to `R_{\mathrm{rd}}`, and the sampler-node count `N` in (R2),
`lem:fc-forest` and `prop:fc-uniform` to `N_{\mathrm{F}}`. This avoids the clashes with the
echelon form R and the count N.

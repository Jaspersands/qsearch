# fc: proof check of the free-coordinate appendix and Theorem `thm:free-coordinate` (9 Nov 2026)

Checker `fc`, one of 12 parallel checkers. This was an AI session (Claude Code) with no human review. It wrote only this file and the folder `O/fc/`. It edited nothing else, ran no git commands and used no network.

## Header

**Scope**

- `T/appendix-free-coordinate.tex`, lines 1–527 (all of it), read line by line.
- `T/main.tex`, lines 764–793: the Schedule 3 subsection, with `thm:free-coordinate` at lines 769–782, `prop:rc-lower` at lines 786–789 and the paragraph after it.
- Also read for these:
  - `T/main.tex` lines 161–388 (contract and notation) and Table `tab:fcs-budget` (lines 985–1029).
  - The regimes-table rows at lines 236–241.
  - `T/appendix-schedule3.tex` lines 39–322, for the reused statements `lem:s3-law`, `lem:s3-moment`(d), `lem:s3-tree`, `lem:s3-node`, `lem:s3-root`, eqs. `s3-bezout`/`s3-nodes`/`s3-ninstr`, and the part (iv) restart proof.
- Literature, local texts only: MP13 Theorem 1.1 and 3.8; GKSZ Definition 6.1 and Theorem 10; KMOSW26 Proposition 5.3 and Theorem 1.10.
- Diffs: `O/diffs/appendix-free-coordinate.diff`. Its changes since 5 Nov are wording and provenance pointers only, with no mathematical change. `O/diffs/patch9nov-main.tex.diff` does not touch lines 764–793.

**shasum**

```
ec9ab51739f4305beea3e64705f61d9b5370e9f6  T/appendix-free-coordinate.tex
0ed1a1f82b13fef77fc94a48e35efc93f8d23ee4  T/main.tex
4966e7646cc5737cf5bf1f0feda9f8a3e7875e04  T/appendix-schedule3.tex   (cross-references only)
f6f5b910bd92c7d50fa5fe035820f2d034e77e3d  R/research/audits/reviews/2026-11-02-rees-linear-arity/lit/mp13_LWsE.txt
249bfd2007237bc90ae1f1df7b14ac6eb9a6caee  .../lit/gksz_1912.04467.txt
ff6a78a6694414cd6a7257dd5292ac3c86fe03d9  .../lit/arxiv_2609.40321.txt   (KMOSW26)
```

**Verdict: MINOR ONLY.** I found no BREAK, GAP or ERROR. Every stated result of the appendix and of `thm:free-coordinate` (i)–(iii) survived a line-by-line check. Every number I recomputed matches the paper. Below are six MINOR items (wording, scope and an import that is easy to prove).

**Scripts** (folder `O/fc/`; each was run as `nice -n 19 timeout T /opt/anaconda3/bin/python -I <script>`)

| Script | Run time | Output |
|---|---|---|
| `fc_exact_checks.py` | 22 s | `fc_exact_checks_out.txt` |
| `fc_numbers.py` | 1 s | `fc_numbers_out.txt` |
| `fc_depth_checks.py` | 60 s wall, 39 s user | `fc_depth_checks_out.txt` |
| `fc_sigma_tail.py` | under 1 s | `fc_sigma_tail_out.txt` |

Total compute was about 1.5 core-minutes of the 20 allowed. Finite checks can only falsify; none of them proves anything.

## Findings (most severe first; all MINOR)

**1. MINOR. The σ_p bound is imported, but the "(proved)" node depends on it**

Location: `appendix-free-coordinate.tex:294` (`rem:fc-zero-sum-arity`(a)), with consequences at :296 (b) and :317 (`rem:fc-witness-h3`(b), table form). The comment at :322 also mentions it.

The text says σ_p ≤ ⌈2log₂(p−1)⌉+4 "is imported here and is not re-derived". KMOSW26 Proposition 5.3 (local text, line 1675 ff.) states only a tail bound, Pr[subset sums cover F_q] ≥ 1−q²/2^B; it states no bound on σ_p.

The node of (b) is labelled "proved". Its Markov step needs N_0(a_d) ≤ N̄_0(g_d), where N̄_0 uses min(p, ⌈2log₂(p−1)⌉+4). For p ≥ 13 that step needs the imported bound. At p = 11 the two expressions in the min are equal, and for p ≤ 11 the step uses σ_p ≤ p, which the paper proves.

The repair takes three lines and gives a stronger bound. Let T be the covering time. For y ≠ 0, the 2^b−1 nonempty subset sums of b uniform draws are pairwise independent and uniform, because distinct nonempty 0/1 vectors are never proportional over F_p. Chebyshev with the exact variance gives Pr[y missed] ≤ (p−1)/(2^b−1), and a union bound over y ≠ 0 gives Pr[T > b] ≤ (p−1)²/(2^b−1). Summing min(1, ·) over b ≥ 0 gives σ_p ≤ b₀ + 1 + Σ_{j≥1} 1/(2^j − 2^{−b₀}) < b₀ + 3, where b₀ = ⌈2log₂(p−1)⌉ ≥ 2.

Checks:
- `fc_sigma_tail.py` [1] compares the exact tail law with this bound for p ≤ 13 and B ≤ 60. It holds.
- `fc_depth_checks.py` [1] gives the exact σ_p: 3, 4.0625, 4.638, 5.428, 5.726, 6.180 and 6.363 at p = 3, …, 19. Each is at most min(p, b₀+4).

**Fix.** At :294, replace "the bound $\sigma_p \le \lceil2\log_2(p-1)\rceil+4$ follows the Chebyshev argument of~\cite[Proposition~5.3]{KothariMetgerODonnellShuttyWu2026}, is imported here and is not re-derived." with:

> and $\sigma_p \le \lceil2\log_2(p-1)\rceil+4$ by the Chebyshev argument of~\cite[Proposition~5.3]{KothariMetgerODonnellShuttyWu2026}: for $y \ne 0$ the $2^b-1$ nonempty subset sums of $b$ uniform draws are pairwise independent and uniform, so the covering time $T$ satisfies $\Pr[T > b] \le (p-1)^2/(2^b-1)$, and summing $\min(1,\cdot)$ over $b \ge 0$ gives $\sigma_p = \mathbb{E}T < \lceil2\log_2(p-1)\rceil + 3$.

The constants and Table `tab:fcs-budget` are unchanged, and the comment at :322 can then be dropped.

**2. MINOR. "The average case of BIS_p" does not meet GKSZ's column condition**

Location: `appendix-free-coordinate.tex:279` (`rem:fc-zero-sum-sis`, preamble).

GKSZ Definition 6.1 (local text, lines 1421–1425) requires n ≥ (m+1)^{N(q)}(q−1) columns, which is (g_d+1)(p−1) for prime q = p and m = g_d rows. The zero-sum node's arity g_d(p−1)+1 is p−2 columns short of that. In addition, the labels are uniform on an unknown a_d-dimensional subspace, not on F_p^{g_d}. The BinSIS formulation in the remark itself is correct; only this cross-reference is loose.

**Fix.** Replace "This is the average case of $\mathrm{BIS}_p$~\cite[Definition~6.1]{GoosKamathSotirakiZampetakis2020};" with:

> This is the search problem of $\mathrm{BIS}_p$~\cite[Definition~6.1]{GoosKamathSotirakiZampetakis2020} on random inputs (that definition also requires at least $(g_d+1)(p-1)$ columns, $p-2$ more than the Davenport bound of Lemma~\ref{lem:fc-zero-sum}(b));

**3. MINOR. "a tree" should be "a run"**

Location: `appendix-free-coordinate.tex:244` (the variant after `lem:fc-zero-sum`).

The added term S·n_d·τ_d covers all S·n_d nodes of grade d over the S trees, so it is the addition for a run, not for one tree. The bound ε/9 is unaffected.

**Fix.** Replace "a tree that uses it must add $S n_d\tau_d$ for each such grade" with:

> a run whose trees use it must add $S n_d\tau_d$ (all $S n_d$ nodes of the grade) for each such grade

**4. MINOR. The abort sums omit or loosely bound the Γ₀ option**

Locations: `appendix-free-coordinate.tex:505–506` (proof of `prop:fc-split`, the displayed abort sum) and :319 (`rem:fc-witness-h3`(c), "It contributes at most $\tau_d + 3\cdot2^{-B}$").

The display sums only over Γ_F. When Γ₀ uses the optional node of `rem:fc-zero-sum-arity`(b), that node's term S·n_c·τ_c is missing. `lem:fc-forest`(b) states the sum correctly, over Γ_F ∪ Γ₀ with β_d. The bound ε/9 still holds, since |Γ_F ∪ Γ₀| ≤ c−1 and each term is ε/(9(c−1)).

At :319, the Γ₀ node in fact contributes at most τ_d, by (b) there; its κ = p−1, so it has no capped steps. That matters, because N counts Γ_F nodes only and so does not absorb a 3·2^{−B} term at Γ₀.

**Fix.**
- At :506, write `\sum_{d\in\Gamma_{\mathrm F}\cup\Gamma_0}Sn_d\beta_d`, with β_d as in `lem:fc-forest`(b).
- At :319, write "at most $\tau_d + 3\cdot2^{-B}$ at $\Gamma_{\mathrm F}$ and at most $\tau_d$ at $\Gamma_0$".

**5. MINOR. The Scope paragraph omits the third option at Γ₀**

Location: `appendix-free-coordinate.tex:376` (Scope paragraph).

At κ_d = p−1 it lists only "Schedule 1 or … the zero-sum node". `thm:free-coordinate`(iii) (main.tex:779) also allows the node of `rem:fc-zero-sum-arity`(b).

**Fix.** Replace "it falls back on Schedule~1 or on the zero-sum node of Lemma~\ref{lem:fc-zero-sum}, whose search costs $p^{O(g_d)}$;" with:

> it uses Schedule~1, the zero-sum node of Lemma~\ref{lem:fc-zero-sum}, whose search costs $p^{O(g_d)}$, or the node of Remark~\ref{rem:fc-zero-sum-arity}(b), whose arity has degree $1+\lceil\log_2(p-1)\rceil$ in $g_d$;

**6. MINOR (notation nits)**

- `rem:fc-zero-sum-arity`(b) (:296) allows 0 < τ ≤ 1 and states arity O_c(g^{1+⌈log₂c⌉}·log(1/τ)). This is 0 at τ = 1. The same applies at :317 (`rem:fc-witness-h3`(b)). Write log(2/τ).
- N denotes two different things: the count of `lem:fc-moment` (:100) and the number of sampler nodes in (R2), `lem:fc-forest` and the definition of B. The earlier report suggested renaming the node count to N_F (P10). That was done for the round cap (now R_rd), but not for N. Optional.

## Checked and correct

**Setting and (F1)–(F6)**
- The bounds 1/κ ≤ q ≤ 1 and 1/q ≥ κe^{−(κ−1)/p}; β is monotone in a.
- Fair-bit draws succeed with probability ≥ 1/2; T_r is irrational, so its ceiling is computable; F_r and R_rd are as stated.
- The root-extraction cap: M·L·(4/9)^{B+⌈log₂ML⌉} ≤ 2^{−B}.
- The Bezout step (eq:s3-bezout).

**Lemmas behind part (i)**
- `lem:fc-rref` (a)–(c). Checked exhaustively at (p,a,M) = (3,2,4), (5,2,3), (3,2,5), (3,3,3) and (2,2,4); RREF(EX) = RREF(X) in 3000 random cases; (c) for every n₀ (`fc_exact_checks.py` [1]).
- `lem:fc-moment`. Exact E N = h^n q^r and Var N = h^{n+1}(q^r − q^{2r}) in 8 cases; Chebyshev; the fixed-x identity ([2]).
- `lem:fc-node` (a)–(e). Exhaustive for a = 1: Pr[bad] is 0.0624, 0.0725 and 0.0564, against β of 0.549, 1.16 and 0.1465. Acceptance is ≥ q^r/2 on good banks. Monte Carlo for a = 2 gave only valid witnesses ([3]).

**Theorem 1, part (i):** the proof.

**Part (ii)**
- `lem:fc-params` (a)–(c): the identity and the bound < 1/64 for u = 2..120; at u = 2 the terms are 1/12656.25 + 1/16384. The β bound holds for u = 2..30 (`fc_numbers.py` [4]).
- The proof of (ii): C(4m′,3m′)·16^{−3m′} ≤ 2^{−2m′}; N_instr ≤ 13·m′·M^{c−1}; the reuse of `lem:s3-tree`, `lem:s3-node` and the part (iv) restart proof.

**Part (iii)**
- (R1)–(R4) and the Γ classes: Γ₀ ⊆ {p−1}, which uses p > c.
- `lem:fc-choice`: β ≤ τ, the integer form, and the size bound with constants (1, 2, 3, 3).
- `lem:fc-zero-sum` (a)–(d) and the variant arity 1 + ⌈log₂(p^g/τ)⌉. Exact (a) in 6 cases; Davenport tightness at (3,2), (5,1), (7,1) and (2,3) ([5]).
- `lem:fc-forest` (a)–(b): ε/9 + 3N·2^{−B} ≤ 2ε/9, with optional nodes handled correctly.
- The proof of (iii): span failure ≤ ε/(3(p−1)); the total is 2ε/9 + ε/3 + ε/3 = 8ε/9; τ_d depends only on M_{d′} for d′ < d, so there is no circularity.

**`rem:fc-zero-sum-sis`**
- (a): the filiform class-(p−1) construction, the H = 1 state preparation and the BinSIS reduction.
- (b): the block bound (δ + p^{g_d−t}/(p−1))^k.
- (c): checked against MP13 Theorem 1.1 and Theorem 3.8 in the local copy.
  - Parameters: n = g_d, m = M_d = poly(n), β = √M, β_∞ = 1, q = p ≥ √M·g^θ (so δ = θ).
  - γ = max{1, ββ_∞/q}·Õ(β√n) = Õ(√(M·g)).
  - The modulus condition of Theorem 3.8 (at most poly(n) divisors of q below β_∞) holds trivially.
  - The reduction is classical, so a quantum node gives a quantum algorithm.
  - "No node at arity C·g^e·p^j, j < 2" follows by taking k > (e + 2θ)/(2 − j).
- (d): the 2^{c−1} count is valid because g_d ≥ g_c ≥ 1 (main.tex:1167), and so is the p = O(log m) argument.
- The h = 2 ternary paragraph: d = κ_d = (p−1)/2 is forced by p > c.

**`rem:fc-zero-sum-arity`**
- (a): the digit identities, including the j* = 1 and j* ≥ 2 boundary cases; the Wald recurrence; the binomial bound; N₀ = 1 + 3n(n+1)/2 at p = 3. The solvers were simulated with binary digit sets at p = 3, 5, 7 and n = 2, 3: every output was checked exactly, and the mean column counts lie within 0.9 se of N₀ computed with the exact σ_p (`fc_depth_checks.py` [5]).
- (b): Markov τ/2 + τ/2; the arity O_c(g^{1+⌈log₂c⌉}); the non-totality example; the degree comparisons (4 vs 3, 5 vs 6, 12 vs 3); polynomiality iff log g·log p = O(log m).
- KMOSW26 Theorem 1.10 is cited correctly: degree 1 + ⌊(c+4)/4⌋, factor p^{p²}, failure probability 2^{−Ω(n)}.
- (c)(i)–(iv):
  - (i) γ = 2p/(p+1) and the final inequality.
  - (ii) Re-derived: union bound over ≤ (2M)^t sparse {0,±1} relations, forced dimensions L, ⌈log₂p⌉ switches per forced dimension.
  - (iii) T·(2/p)^n.
  - (iv) checked.

**`rem:fc-witness-h3`**
- (a), the depth:
  - Cauchy–Davenport gives |D_j| ≥ min(p, 2^j·h + 1).
  - The Jacobi count, re-derived from the term count: p−2, 2(κ−1) terms of modulus 1, κ−1 terms of modulus 1, (κ−1)(κ−2) terms of modulus √p. Numerically it holds for all 2250 pairs (p, κ) with p < 6000 and κ ≤ 7.
  - The 1/(2κ) claim (4κ² − 15κ + 17.5 > 0) and the j* = 1 threshold (3κ² − 12κ + 16 > 0).
  - The Minkowski and counting bounds with c₃ = c₆ = 2, c₄ = 1, c₅ = 4, on 3617 primes.
  - The stated values j*₃ = 1, 1, 2, 2 and j*₄ = 1, 2. The range of j*₃ − ½log₂p over 3014 primes is [−0.850, 0.599] ([2], [3]).
- (b), sampler and node:
  - Simulated with D_j tables at (p, κ) = (13,3), (17,4), (19,6), (13,4), (7,2), and in the rescaled form at (17,2), (29,2), (67,3), (73,3), (257,4) for n ≤ 4. All outputs were exact. The means match N₀ (10 table-form tests, all within 2.3 se) and the exact rescaled formula 1 + ⌈log₂p⌉·(p/(p−1))·n(n+1)/2.
  - The leading coefficient σ^{j*}/(1+j*)!.
  - The O in the arity bound has an absolute constant. By induction, N₀(n) ≤ (σ̄+1)^{j*}·n^{1+j*} for n ≥ 1; a grid check found maximum ratio 1 (`fc_sigma_tail.py` [2]).
  - The split cap ⌈2κ·ln2·(B + ⌈log₂M⌉)⌉; 13 ∈ E₂(4) (main.tex:721); Schedule 1 has degree 12.
- (c):
  - The formula for E; E ≤ 2c−1 above the threshold.
  - Recomputed max_{p>c} E = 3, 6, 8, 10, 13, 14, 16, 19 for c = 2..9. The smallest maximizing primes are 3, 7, 7, 11, 7, 31, 31 and 19, so c = 9 is attained at p = 19 ([4]).
  - The log₂Q range 93.0–150.8 (w.-d. column: 103.46, 92.99, 119.91, 127.09, 150.77, 142.02; `fc_numbers.py` [2]).
- (d): the union bound ((h+1)^M − 1)/p^a < (h+1)^{M−a}·q^a; the induction placing the switch hierarchy in γD_j; the Kronecker remark (for even h, μ_h ∪ {0}).

**Remaining statements**
- `prop:fc-uniform` (a)–(b): 4·15^{−4}·2^{−3} + 2·64^{−3} = 2^{−15.80} < 2^{−14}; M_d ≥ g_d + 2.
- `app:fc-numbers` and Table `tab:fcs-budget`: all six rows, (iii) columns and w.-d. column (table below).

  | p | log₂Q | max cap | total |
  |---|---|---|---|
  | 11 | 42.27 | 28.29 | 47.03 |
  | 1031 | 36.57 | 33.44 | 50.83 |
  | 5281 | 39.08 | 33.78 (grade 4, κ = 4) | 52.22 |
  | 2^31−1 | 35.89 | 31.04 | 49.82 |
  | 2^61−1 | 34.08 | 33.50 | 50.97 |
  | 2^127−1 | 33.98 | 31.00 | 49.52 |

  - The explicit choice adds 1–2 columns and 0.24–1.31 to log₂Q.
  - Part (ii) per-node caps go up to 2^34.28. The uniform-kernel exponents are 193.9–236.0, and 223.8–236.0 at the four table primes with p ≥ 5184 (as main.tex:767 states).
  - All the primes are prime (`fc_numbers.py`).
- `prop:rc-lower` and its proof:
  - The mean (q^n − p^{−n})·q^a is exact in 5 cases.
  - The singular probability is 1 − Π(1 − p^{−i}) ≤ 1/(p−1).
  - The p = 5 example. The clause "outside the bank event" is present.
- The split construction:
  - `lem:fc-split-law` (a)–(d), including the counterexample probability 69/325, which is exact (`fc_exact_checks.py` [6]).
  - `prop:fc-split-node` (a)–(c), including the ν recursion, ν ≤ (M−1)/(m_*−1) and ν ≤ 2Π_{j≥2}M_j.
  - `prop:fc-split` (i)–(ii), apart from item 4.
  - `rem:fc-tradeoff` (a)–(b).
- `thm:free-coordinate` (main.tex:769–782): each clause is matched to its proof. This covers the "for fixed c" clause, the least versus explicit arity, "N the number of sampler nodes", the weight-doubling time clause, and the rank guard in (ii).

## Not checked / UNKNOWN

- Provenance-only finite claims. I did not rerun:
  - the node with its abort rule (abort in at most 1/40 of trials at τ = 1/20, and at most 1% at τ ∈ {0.05, 0.5});
  - the rescaled form at 2^31−1 (κ = 3) and 2^61−1 (κ = 6);
  - the "within 2.7 se for p ≤ 17" statistic.
  My simulations cover the solvers, not those exact runs.
- Body and other-appendix results used here were read as statements only. These are `lem:central`, `prop:descent`, `lem:s3-law`, `lem:s3-tree`, `lem:s3-moment`(d), `rem:combined-schedule` with (G1)–(G3), `rem:sde-block-steered`, the Schedule 1 arity B_d(g), `rem:triangular-scope`, and the 2^128 figure of `prop:mixed-schedule`. They belong to other checkers' parts.
- KOW26 (arXiv 2510.07515), Section 3 and Theorem 1.2: not read.

## For the human expert

- **External theorems.**
  - |J(χ,ψ)| = √p for nontrivial χ, ψ, χψ (Ireland–Rosen, ch. 8).
  - Kronecker's theorem; Minkowski's convex body theorem; Cauchy–Davenport.
  - The Davenport constant of F_p^n and Chevalley–Warning.
  - MP13 Theorem 1.1 (author copy of 13 Feb 2013; check the numbering in the CRYPTO version).
  - KMOSW26 Theorem 1.10 and Proposition 5.3 (arXiv text).
  - GKSZ Theorem 10.
- **The "(proved)" labels on remarks.** Decide whether labels such as "(proved; AI-checked …)" are acceptable on remarks that rest on imported steps (finding 1), and on bounds "within the stated models" (`rem:fc-zero-sum-arity`(c)).
- **Lattice consequence.** `rem:fc-zero-sum-sis`(c) uses the assumption that polynomial-factor worst-case approximation is hard for quantum polynomial time. The class c = p−1 grows with g_d in that construction; that is a modelling choice worth confirming.
- **Modelling.** All Schedule 3 guarantees hold for the i.i.d. supply only (Scope paragraph). The "bank-reading" node model limits what (a)–(c) exclude.

## Comparison with the earlier reports (read after my own pass)

**`2026-11-03-rees-check-app-b.md` §4 (snapshot 39591e85)**
- Its verdicts of "proved", on the statements that existed then, agree with mine. I re-derived each of them; I did not copy them.
- Its P10 rename was half adopted: the round cap is now R_rd, but N has not become N_F (finding 6).
- Its warning about `prop:rc-lower` (candidate laws that do not depend on R′) is kept in the current statement and in the Scope paragraph.
- It did not re-run Table `tab:fcs-budget`. I did, and it matches.

**`2026-11-02-rees-free-coordinate-appendix.md`**
- Each of its fixes is present and correct:
  - §6(c), "any public M_d … least such M_d";
  - "for fixed c";
  - §6(e), "outside the bank event";
  - §6(g), log(1/τ_d) in the regimes row at main.tex:237;
  - §3 item 4, the rank guard in (ii);
  - §3 item 8, the preamble scoped to part (i);
  - §6(h), the merge: `thm:random-column` is gone, and the uniform-kernel sampler is part (iv).
- §6(f) is superseded: the block splitting is now proved in `app:fc-split`, which I checked.
- Its numbers (2^33.78 at p = 5281 grade 4; 2^34.3 under (ii)) agree with mine (33.78; 34.28).

**What they could not have checked.** Neither report covers the text added after its snapshot: `lem:fc-zero-sum`, `rem:fc-zero-sum-sis`, `rem:fc-zero-sum-arity`, `rem:fc-witness-h3`, the split section and `rem:fc-tradeoff`. Findings 1–5 are all in that later text, or in the Scope paragraph as later edited. So none of them is an item the earlier reports missed.

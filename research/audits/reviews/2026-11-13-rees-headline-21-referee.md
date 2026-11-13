# Referee report: proved class-9 headline 21 (Schedule 1H+), 2026-11-13

AI only (one Claude Code referee agent), pending human review. Hostile reading of
`2026-11-13-rees-headline-below-38/fragment.tex` (cited below as `frag:LINE`) against
`docs/papers/rees-hsp/core/main-core.tex` (sec:schedule1, sec:halving, rem:is-import, thm:main).
No file outside this report and its folder was edited. No Git, no network. Every run used `nice -n 19`,
one process at a time; the largest run took 22 s and well under 1 GB.
Scripts and outputs: `research/audits/reviews/2026-11-13-rees-headline-21-referee/`.
All referee code is new. It imports none of the author's code except `cmp_rule.py`, which imports
`rule.py` read-only to compare per-(p, κ) values. It reads the author's JSON data, re-checks every
item, and uses only what passes.

Labels: PROVED, PROVED given cited theorems, CONDITIONAL, REFUTED, UNKNOWN, NOT computed.
Finite checks can only falsify. The finite computations below are of the same kind as the core's
lem:halved-exponent(ii).

## 0. Verdict

**Headline E_+(9) = 21 (E_+(c) = 3, 5, 9, 10, 14, 16, 19, 21): PROVED WITH FIXES**, given the cited
theorems (Weil's two-variable diagonal bound, the same import and the same flagged locator as the
core; Rabin root finding) and the exact finite computation. I reproduced the computation independently.
None of the fixes changes a number. I found no gap and no error that changes a number.

| item | verdict |
|---|---|
| def:k-node, def:rc, frag:19 | PROVED WITH FIX (F1) |
| lem:refine (R) | PROVED |
| rem:designated, cor:chain | PROVED |
| lem:stage2 (S) | PROVED WITH FIX (F2, wording) |
| lem:finishK (F_K) | PROVED WITH FIX (F3) |
| lem:sm (SM) + tab:sm-thresholds | PROVED given Weil; all ten thresholds reproduced exactly |
| def:schedule1hplus | PROVED WITH FIXES (F4, F5, F6) |
| thm:halving-plus | PROVED WITH FIX (F7; the constant can be strengthened to C_c) |
| lem:chain-exponent | PROVED given the finite computation (reproduced independently) |

**Side finding (material, new; label: PROVED given the fragment's lemmas + finite computation,
AI only, needs its own referee).** Candidate S1 (Lemma rounds, the *only* use of Theorem
thm:is-import) is never needed. With S1 forbidden at every level, every (p, κ), κ ≤ 9, κ | p−1,
p < 2·10⁶ still has a candidate, and the maxima are unchanged: 3, 5, 9, 10, 14, 16, 19, 21
(`nos1_ref.py` → `nos1_2e6.out`). Above 2·10⁶ the tail values come from κ=2 (1,F1) over GE, TL3/4/5,
(1,F1) over H⁺₃ and H⁺₄, U7, and TW. None of these is S1. Combined with rem:main-solver ("any per-grade
solver with these properties gives the same theorem"), thm:main for **c ≤ 9 would no longer need
to assume Theorem thm:is-import**, with exponent 21. This bears on the paper's central caveat.
Claim gates stay false; it is not claimed in any paper file.

## 1. Line-by-line findings

**Setup, frag:12.** The class map cl_D defined from one ξ satisfies cl_{D'} ≡ cl_D (mod D'),
because x^{(p−1)/D'} = (x^{(p−1)/D})^{D/D'}. This makes Lemma R's class bookkeeping coherent across
moduli. Correct.

**F1 (frag:19).** "A D-solver ... hence a DZ_κ-node at modulus κ" holds only after scaling. A
DZ_κ-node needs one coefficient of κ-class 0, and a D-solver may return only weights in
P_D \ P. Scaling by w_b⁻¹ ∈ P_D shifts κ-classes by an element of DZ_κ, so the class set is kept.
Fix: say "after scaling by the inverse of one weight (Remark rem:designated)".

**Lemma R (frag:28–43). PROVED.**
- Every nonzero c^ν_b has its D-class in lift_D(K') ⊆ R. Then Σ_i U^ν_i = 0.
- There are (r−1)a linear conditions on n = (r−1)a+1 unknowns, so η ≠ 0 exists.
- The identity Σ_b w_b λ_b = Σ_ν η_ν α_{j(ν)} Σ_i U^ν_i + Σ_i β_i Σ_ν η_ν U^ν_i = 0 holds also
  with zero cells α_j+β_i = 0. Certificates do contain zero cells, for example p = 7, TL3, α₂ = 0.
- Nonzero outputs have class j + cl(α_j+β_i) + i ∈ K.
- Designated coefficient: η_{ν*} = 1 gives j = 0. A designated inner coefficient equal to 1 gives
  i* = 0. Then w_{b*} = α₀+β₀ ∈ P_D is nonzero.
- The normalisation in rem:designated is legitimate. Scaling a K'-relation by x⁻¹ with
  cl_{D'}(x) = 0 shifts D-classes by an element of D'Z_D. That fixes lift_D(K').
- Arity: (r−1)a+1 ≤ κ(a+1) gives degree +1 with constant factor ≤ r−1.

**Cor. chain (frag:50–55). PROVED.** Same-modulus steps (D_{t−1} = D_t) and union targets are
covered: Lemma R needs only D' | D.

**Lemma S (frag:57–64). PROVED.**
- q = ξ^m has κ-class m, so x_ν/q ∈ P for ν ∈ J.
- I ≠ ∅ by the designated coefficient.
- For the halving case m = κ/2: (ξ^{κ/2})^h = −1, so q is a valid core q.

F2: the first sentence of the proof is garbled ("with P_D = P ∪ qP replaced by P ∪ qP"). Fix: "the
proof of Lemma stage with the D-solver replaced by a {0,m}-node and q = ξ^m".

**Lemma F_K (frag:68–75). PROVED WITH FIX.** The proof is correct and needs no designated
coefficient.

F3: the statement must ask for y^{(ν)} "with roots of its entries", as F1 does, and the
preprocessing must build the T_j tables for each new ε = −ξ^{−m} used (below 4κ⁴).

**Lemma SM (frag:79–95). PROVED given Weil.**
- A_{ij}: the sizes h_D and kh_D are right. The (0,0) cell is correctly the stricter Q₀.
- E[n_j] is μ₀ for j = 0 and μ₁ otherwise. The β_i are independent.
- Pair count. Each y ∈ Q_ℓ with y+δ ∈ Q_ℓ' gives exactly D² pairs (s,z) ∈ (F_p^×)². Distinct y give
  disjoint pairs. So N_ij(δ) ≤ k²(p+(D−1)²√p)/D².
- The algebra (|A|/h_D)²(p+(D−1)²√p)/D² = γ|A|²/p checks.
- Weil hypotheses: the coefficients ξ^ℓ' and −ξ^ℓ are nonzero, δ = x'−x ≠ 0, and D | p−1. The
  bound |N−p| ≤ (D−1)²√p is the core's form, for general nonzero coefficients. Jacobi-sum check:
  - One-trivial-character terms vanish.
  - Nontrivial pairs contribute |J| = √p, or 1 when χ₁χ₂ = 1.
  - So the bound holds. Same import and same NEEDS HUMAN VERIFICATION locator as
    lem:zero-sum-length(iii).
- Second moment ≤ E + γ^{r−1}E². The Paley–Zygmund step and the union over D columns give Φ.
- Monotonicity: d log μ/dp = r/(p−1) − (r−1)/p > 0, and γ is decreasing.
- Sampler:
  - Chebyshev bounds each column by 4(ρ−1). Then n_j ≥ μ₀/2, using μ₁ = kμ₀ ≥ μ₀.
  - With ⌈(2p/μ₀)ln 4D⌉ draws per column, a column is missed with probability ≤ 1/(4D).
  - So a round succeeds with probability ≥ 3/8.
  - h_D ≥ p/(2D) gives p/μ₀ ≤ (2D)^r.
- **Thresholds.** `thr_ref.py` uses exact rationals, a rigorous lower bound for √p and integer
  bisection. It reproduces T_exist = 430, 9395, 99745, 1124521, 1995734 and T_samp = 39096, 778545,
  6922583, 85628629, 149308802 **exactly**. Φ(T−1) ≥ 1 > Φ(T) in each row.

**Definition 1H+ (frag:114–124). PROVED WITH FIXES.**
- **F4 (ξ convention).** Certificates, Tier B witnesses and the m of each U7 certificate are
  relative to the least primitive root g. The setup paragraph (frag:12) instead says "a uniform
  element". State that for p < 2·10⁶ the run uses ξ = g (p−1 factored by trial division,
  deterministic). State also that the same ξ serves every D | κ and every sub-solver of the grade.
  Above all T_exist any coset generator works (Lemma SM).
- **F5 (band preprocessing, question 5).** It does **not** break "polynomial uniformly in p". The
  band T_exist ≤ p < T_samp is a finite set of primes. A trial (uniform β, full scan of F_p per
  column) costs ≤ D·r·p class tests and succeeds with probability ≥ 1−Φ(p) ≥ 1−Φ(p_D), where
  p_D is the least prime ≡ 1 (mod D) at or above T_exist. Recomputed values:

  | node | 1−Φ(p_D) |
  |---|---|
  | TL3 | 3.5e−3 |
  | TL4 | 1.3e−4 |
  | TL5 | 7.8e−5 |
  | TW9 | 1.2e−5 |
  | U7 | 2.2e−5 |

  So the expected cost is ≤ D·r·T_samp/(1−Φ(p_D)) class tests, about 3·10¹⁴ for U7. That is an
  explicit constant, absurd but legitimate. rem:is-import(d) cuts each attempt off at twice the
  expected time, so it needs this bound written out. Fix: state it. The cosmetic alternative is to
  extend the tables to T_samp.
- **F6.** rem:is-import(d) must count the new preprocessing tasks (ξ, up to 5 contractions per
  grade, T_j tables per ε). This is still O_c(1). The descriptor "(B)" sits on enumerate item (f),
  and the text refers to "(f)". Rename it "(TB)" to avoid confusion.

**Thm halving-plus (frag:126–133). PROVED WITH FIX.**
- Each candidate is a κ-solver. Availability is decided from (p, κ) before any query. A⁺ ≤ A,
  because the core's candidates are kept with inner arities A⁺_D ≤ A_D.
- F7 (strengthening, optional). `const_ref.py` computes the least constant among degree-optimal
  candidates for every p < 2·10⁶. It gives K⁺_κ ≤ c_κ for every κ ≤ 9; the largest ratio is 0.25,
  at κ=2, p=3. Above 2·10⁶ the constants are κ−1, 4 and 6, or are inherited. So the core's
  C^H_c = C_c survives, and thm:main(4) needs no new constant. Without this computation, the
  fragment's weaker "some K⁺_κ" is correct.

**Lemma chain-exponent (frag:135–146). PROVED given the finite computation. Question 4: the logic is
complete.**
- p > 2·10⁶: all five steps are above T_exist (max 1995734), p > 4·9⁴ and t ≤ 3. Then
  e⁺ = (1,2,2,2,2,3,3,3,3) exactly:
  - Upper bound by the listed candidates.
  - Lower bound: S1 ≥ κ; chains ≥ 2; plans ≥ e_{κ/2}+1; (e) exists only for κ=7 and even κ.
- Monotone along divisibility. Equality for d ∈ {3,5,6,7,8,9} forces κ_d = d. For d = 4, κ₄ = 2
  ties harmlessly. gcd(d, p−1) depends on p mod 2520. So Σ ≤ 20, with equality iff 2520 | p−1.
- Below 2·10⁶, the exact computation uses only proved ingredients:
  - class sumsets below 26244;
  - lem:zero-sum-length(ii),(iii) and lem:two-term above 26244;
  - certificates below T_exist;
  - Lemma SM above T_exist.
- Nothing is left between the two ranges.

## 2. Independent reproduction

| check | result |
|---|---|
| `chk_ref.py`: third checker, written from def:rc. P_D test independent of g; g re-verified as least primitive root; K/R shapes asserted | 74 536 items (42 256 certificates + 32 280 Tier B witnesses), **0 rejected** |
| `coverage_ref.py` | uncovered primes below T_exist exactly as reported (TL4: 6, TL5: 9, TW9: 14, U7: 3); no stray certificates; 28 Tier B primes; 260 primes ≡ 1 (mod 2520) below 2·10⁶ |
| `rule_ref.py`: Def. 1H+ re-implemented from the fragment text, with class sumsets by cyclotomic data S_δ = {cl(1+y): y ∈ Q_δ} (a different method from halved_schedule.py) and Tier B chains rebuilt from re-checked witnesses | new candidates off: 3, 6, 10, 14, 20, 25, 29, 38 (the core). New, p < 2·10⁶: **3, 5, 9, 10, 14, 16, 19, 21**; c=9 maximum at 264 primes = {13, 19, 37, 73} ∪ {260 primes ≡ 1 mod 2520} |
| `cmp_rule.py` | 77 841 pairs (p, κ), p < 2·10⁵: 0 disagreements with the author's rule.py |
| `exec_ref.py`: new executor for the novel node types | 122 runs, 0 failures: chains with union targets; same-modulus chain (7;Z₇→{0,3,6}→{0,2}→{0}) at 43; stages over {0,m}-nodes with m ≠ κ/2; F_K by chain K-nodes. Primes and κ: 13 (κ=4, 6), 19 (6, 9), 37 (9), 73 (8, 9), 5 (4, with a 2-solver start); a = 1, 2; uniform, repeated, axis, zero-heavy and ±1 banks |

## 3. Question 6: hidden dependence on conditional material

None found:
- rule.py imports only halved_schedule.py, the core rule.
- USE_KD is False.
- rcdfs.c is used only as a search engine, and its witnesses were re-checked here.
- crosscheck_r8 reads R8 for comparison only.
- No IS Lemma 12 (ℓ=3), Theorem HC, chain corollary or E₂ table enters. Lemma R replaces them.

The fragment's remark at frag:26 attributes the "normal form" of the two-level tensor to
IvanyosSantha2015 through the full version. Drop the attribution or cite only the full version; it
is not used.

## 4. Adversarial self-check

- My rule shares design choices with the author's, such as LMAX = 3 and the BFS over the same
  witness set. So agreement is not full independence. It does catch arithmetic and bookkeeping bugs.
  Upper bounds need only that each listed plan is valid, and the executor and checkers test that.
- The class-sumset routines are different methods, yet both use the least primitive root. A wrong
  primitive root would hit both. chk_ref re-verifies g, and the P_D test does not depend on g.
- The executor covers 8 binding (p, κ) plans at a ≤ 2 only. It is a falsifier, not a proof. Lemma R
  and F_K are proved on paper above.
- The Weil locator (LN Thm 6.37) is still unverified by a human. The whole of Lemma SM, and so every
  p ≥ T_exist, rests on it, as the core's lem:two-term does.
- The S1-free side finding is the most consequential and the least reviewed claim here. It rests
  on the same certificates and Tier B witnesses, and on my code alone. Before any use it needs its
  own referee, and a check that nothing else in sec:proof-main or the corollaries touches
  Lemma rounds or van de Woestijne. grep shows thm:is-import is used only through the per-grade solver.
- "Attained exactly" in lem:chain-exponent is a statement about this candidate list. "≤ 21" is the
  robust content.
- Everything here is AI-checked, pending human review. The gates speedup_claim_allowed,
  novelty_established, etc. stay false.

## 5. Next question and command

Next: referee the S1-free observation, and if it holds, decide whether thm:main for c ≤ 9 should
drop "assume Theorem thm:is-import".
`nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-headline-21-referee/nos1_ref.py 2000000`.
Acceptance: "S1 indispensable at 0 primes" and maxima {2:3, 3:5, 4:9, 5:10, 6:14, 7:16, 8:19, 9:21}.

# Referee report: proved class-9 headline 20 (Schedule 1H⁺⁺), 2026-11-13

AI only (one Claude Code referee agent), pending human review. This is a hostile reading of
`2026-11-13-rees-headline-below-38/fragment-v2.tex` (cited as `v2tex:LINE`) and
`2026-11-13-rees-headline-below-38-v2.md` (cited as `v2md:LINE`). They were read against
`fragment.tex` (Schedule 1H⁺, refereed PROVED WITH FIXES) and `core/main-core.tex` sec:halving.

Scope and provenance:
- No existing file was edited. There were no Git commands and no network use.
- Every run used `nice -n 19`, one heavy process at a time. The largest run took 342 s; the largest
  RSS was under 200 MB.
- Scripts and outputs are in `research/audits/reviews/2026-11-13-rees-headline-20-referee/`.
- All checking code is new, with one exception: `plus2.py` and `run2.py` extend the code of the
  `-21-recompute` folder (`plus.py`, `fp.py`, `rc.py`, `rcsearch.c` and its search cache), which was
  written independently of the author.
- No author script was imported. Their JSON data (certificates, tables, the Tier B prime list) is
  read, and every item is re-checked before use.

Labels: PROVED, PROVED given cited theorems, CONDITIONAL, REFUTED, UNKNOWN, NOT computed. Finite
checks can only falsify.

## 0. Verdict

**Headline E₊₊(9) = 20, with E₊₊(c) = 3, 5, 9, 10, 14, 16, 18, 20 for c = 2..9: PROVED WITH FIXES.**
- It is PROVED given the cited theorems and the exact finite computation. The cited theorems are
  Weil's two-variable diagonal bound, with the same unverified LN locator as the core, and Rabin root
  finding.
- No fix changes a number.
- Attainers of 20: exactly the primes p ≡ 1 (mod 2520) and 37, 43, 73, 127, 181, 631. I reproduced
  this with my own code.

| item | verdict |
|---|---|
| (i) TL6 = Cor. chain + Lemma SM at (D,r,k) = (6,6,1) | PROVED given Weil. Lemma SM never uses κ ≤ 5. T_exist = 837384 and T_samp = 40924516 reproduced exactly |
| TL6 certificates | all 33258 accepted by my own checker, including all 114 primes ≡ 1 (mod 2520) below 837384. The 53 gaps are NONE by exhaustive DFS |
| lem:ell-tensor | PROVED |
| def:ell-contraction, the "(iii) is decidable" paragraph | PROVED |
| lem:ell-node | PROVED |
| prop:ell-tables | PROVED WITH FIX (G1, storage convention). All 5 tables verified |
| def:schedule1hplus2, Thm halving-plus for 1H⁺⁺ | PROVED WITH FIXES (G2, G3) |
| lem:chain-exponent-v2 | PROVED given the finite computation, which I reproduced. Wording fix G4 |
| conditional material (Lemmas S/F, Thm HC, R5, Lemma P, IS Lemma 12) | none used. thm:is-import (S1) is also never needed for 20 (§4) |

## 1. Lemma SM at κ = 6, and the thresholds (task 1)

- **Lemma SM never uses κ ≤ 5.** The statement and proof of `lem:sm` (frag:79–95) take only
  D ≥ 2 with D | p−1, R ∋ 0 and K ∋ 0. Every step is uniform in D:
  - the coset sets A_ij;
  - the D² preimage count;
  - Weil for D-th powers;
  - Paley–Zygmund, the union over D columns, Chebyshev, and p/μ₀ ≤ (2D)^r.
- **The κ ∈ {3,4,5} restriction is in the schedule only.** It sits only in the schedule item
  frag def:schedule1hplus(c).
- **Cor. chain needs nothing beyond that.** It takes D₀ = 1 (Gaussian elimination scaled to 1,
  rem:designated) and R₁ = lift₆(Z₁) = Z₆. TL6 is that case, with degree 2.
- **Exact thresholds (`thr.py` → `thr.out`).**
  - Method: Fractions throughout. √p is bracketed by isqrt(p·10⁸⁰)/10⁴⁰, and I used integer
    bisection with a tightness assertion at T−1.
  - TL6: T_exist = **837384** and T_samp = **40924516**, as claimed.
  - The five rows of tab:sm-thresholds are reproduced exactly.
  - The TL7, TL8 and TL9 rows of rem:below-20 (8933473, 146896259, 3336892478) are also reproduced.
- **Band check.**
  - The least prime ≡ 1 (mod 6) at or above T_exist is 837409, and there 1−Φ = 1.674·10⁻⁵ > 1.6·10⁻⁵.
  - 200 sampled points of the band have Φ decreasing and < 1.
  - So the expected cost of the band preprocessing is at most 36·T_samp/(1.67·10⁻⁵) ≈ 9·10¹³ class
    tests. That is a constant, but see G3.

## 2. ℓ-level lemmas, line by line (task 2)

**lem:ell-tensor (v2tex:20–33). PROVED.**
- **ℓ = 1.** Take a dependence c on a+1 columns with c_{b*} = 1. Set w_b = c_b/z_{cl(c_b)} ∈ P.
  Then Σ_m z_m T_m = Σ c_b λ_b = 0. Also b* ∈ S₀ with weight 1, since cl(1) = 0 and z₀ = 1.
- **ℓ ≥ 2.**
  - M_ℓ = N·M_{ℓ−1} with N = (κ−1)^{ℓ−1}a+1. The off-zero vectors lie in F_p^{N−1}, so θ ≠ 0 exists.
  - The Claim holds by induction on the number of zero coordinates. It uses z₀ = 1 and the linearity
    of the old axis relations in μ.
  - The new axis gives Σ_j z_j T_{(y,j)} = Σ_μ z_{j_μ}w′_μ T^μ_y = Σ θ_μ T^μ_y = 0.
  - Old axes: each is a w′-combination of the old relations.
  - Weights w′_μ w_b ∈ P. The cells are disjoint because the blocks and sub-cells are.
  - θ_{μ*} = 1 gives j = 0 and w′ = 1, so b* lies in S_{(0,0)} with weight 1.
- The cost "poly(a, κ^ℓ)" is correct for fixed ℓ. The degree of the polynomial grows with ℓ, which is
  harmless at ℓ ≤ 4.

**def:ell-contraction and the decidability paragraph (v2tex:35–41). PROVED.**
- The tensors satisfying every axis relation form ∩_r(V⊗…⊗W⊗…⊗V) = W^{⊗ℓ}.
- The vectors e_m − z_m e₀ (m ≠ 0) form a basis of W.
- (iii) is therefore orthogonality to (κ−1)^ℓ basis tensors.

**lem:ell-node (v2tex:43–50). PROVED.**
- Σ x_b λ_b = Σ_y C_y T_y vanishes coordinatewise by (iii), since each coordinate family satisfies
  the axis relations.
- Every nonzero x_b = C_y w_b has the class of C_y, which is in K. x_{b*} = C₀ ∈ P \ {0}.
- With K = {0}, all weights lie in P. κ-th roots (tables at these small p) then give a κ-solution
  exactly in the core's sense (main-core sec:halving: w ∈ (P∪0)^M, w ≠ 0, r^κ = w, Σ wλ = 0).
- The arity bound holds because (κ−1)^t a + 1 ≤ κ^t(a+1).
- The constants are 27, 125 and 2¹⁸, far below c_4 = 4¹⁸, c_6 = 6⁴⁵ and c_9 = 9¹⁴⁴. TL6 has
  constant 5. So the 21-referee's F7 strengthening C^H_c = C_c survives. This was checked by
  inspection of the new candidates only.
- **Check of the RC remark (v2tex:52).** C_{(i,j)} = z_i z_j(α_j+β_i) satisfies (i)–(iii). I checked
  this by hand.

**Executor (`ell_exec_ref.py` → `ell_exec_ref.out`). A falsifier only.** It is my own recursive
implementation of Lemmas ell-tensor and ell-node. It checks:
- the axis relations of the final T, recomputed from the cells;
- the weights lie in P, and b* has weight 1 in cell 0;
- the core κ-solution conditions.

Results:

| run | result |
|---|---|
| genuine tables, normal banks: p = 13 (κ = 4, 6; a = 1..3); 19, 37, 73 (κ = 9, a = 1, 600210 columns) | 54/54 ok |
| genuine tables, forced mode | 15/15 ok; at κ = 9, 6561/6561 cells active |
| perturbed tables, forced mode | 15/15 FAIL (good) |
| perturbed tables, normal banks | 0/8 detected |

- **Executor weakness (material for interpreting anyone's executor).**
  - On uniform, zero-heavy or repeated banks, the relation almost always comes from a degenerate
    sub-block whose off-zero T vanishes. Then the top-level T ≡ 0 and the table is never exercised.
    That is why the 8 perturbed tables went undetected on those banks.
  - Forced mode resamples degenerate blocks, so the bank stays a valid input.
  - The author saw the same effect (v2md §5.4).

## 3. Finite tables and certificates (task 3)

- **Five ℓ-tables (`verify_ell_ref.py` → `verify_ell_ref.out`). All VERIFIED.** The checks are:
  - exact contraction of C on every axis, with a W-basis pivoted at the **last** index (the
    author's programs pivot at 0);
  - 300 random rank-one W-tensor tests;
  - C_y ∈ P by power character, and C₀ ∈ P.
- ξ is the least primitive root (2, 2, 5, 2, 2).
- Controls:
  - changing one entry within P: FAIL in 5/5;
  - reading the stored values as C: FAIL in 5/5.
- **G1 (material, reproducibility).** Read literally, as C_y = the stored value, **all five tables
  FAIL**. For example, at (19, 9) there are 3748 violations of (iii) and 3078 entries not in P.
  - The JSON files store the normal form B(y) = C_y / z^y, with z^y = ξ^{Σy_r}. This convention is in
    `k9-below-21.md` and in the author's `verify_ell.py` docstring.
  - It is **not** stated in prop:ell-tables (v2tex:57: "The tables are listed in the artifact").
  - Fix: state "the artifact stores B(y), with C_y = ξ^{y₁+…+y_ℓ}B(y)", or store C.
- **Generator dependence.** The tables are valid for ξ = g and not in general for other generators
  (for example, 0 of 5 others pass at 19). So the schedule must fix ξ = g; the 21-referee's F4
  carries over.
  - The author explains the two "BAD controls" by "classes identical" (v2md:83). That reasoning is
    incomplete: ξ′ = ξπ with π ∈ P changes z_m = ξ^m, and therefore changes (iii).
  - That these controls pass is a property of those particular tables. It is not a reason.
- **TL6 certificates (`verify_tl6.py` → `verify_tl6.out`).**
  - I wrote my own checker, with its own primitive-root routine and class test.
  - All **33258/33258 were accepted**, not just a sample. All **114/114** primes ≡ 1 (mod 2520)
    below 837384 are certified and accepted.
  - 20/20 perturbed certificates were rejected.
  - In total 33311 primes ≡ 1 (mod 6) lie below 837384. The 53 missing ones are exactly the stated
    list, with maximum 859.
- **The 53 missing primes (`tl6_missing.py`).** rcsearch's exhaustive DFS (WLOG β₀ = 0, α₀ = 1)
  returns **NONE at all 53**. An unnormalised brute force agrees at 7 and 13, and the positive
  controls are FOUND. So availability by table and availability by existence coincide.
- **Other certificates (`certs_ref.py`).** All TL3/4/5, TW9 and U7 certificates were re-accepted:
  42256, with 0 rejected. Their gaps are as the 21-referee found.
- **Handling of the 53 (`run2_def.out`).** All 53 have plans. Their E(9) values range from 16 to 20,
  and the value 20 occurs exactly at 37, 43, 73, 127, 181 and 631. Every attainer outside the 2520
  class is therefore a prime without TL6, and those exhaustive NONE results are why they stay at 20.

## 4. Independent recursion (tasks 4, 5)

`plus2.py` is the `-21-recompute` plus.py with two additions:
- candidate (g), TL6. It is available for p ≥ 837384, or at a re-verified certificate;
- candidate (h), the five ℓ-pairs.

I ran it at every prime p < 2·10⁶ (`run2.py`; about 4 s per run once the search cache was warm). The
**def** variant uses Tier B at the 28 primes of tierB.json, which is the fragment's definition. The
**allB** variant uses Tier B at every p ≤ 523.

| variant | E(c), c = 2..9 | c = 9 attainers |
|---|---|---|
| def | **3,5,9,10,14,16,18,20** | 266 = 260 primes ≡1 (2520) ∪ {37,43,73,127,181,631} |
| allB | same | same |
| def, no TL6 | …,18,21 | 260 primes of the 2520 class |
| def, no ℓ-tables | …,19,21 | 13, 19, 37, 73 |
| def, neither (1H⁺ regression) | 3,5,9,10,14,16,19,21 | {13,19,37,73} ∪ the 2520 class (264), matching the refereed 1H⁺ |
| def / allB, S1 forbidden | 3,5,9,10,14,16,18,20 | same 266; 0 primes without a plan |

- **Grade vectors.** They match v2md §3 exactly:
  - 13: 2,2,3,1,3,1,3,2
  - 19: 2,2,2,1,4,1,2,4
  - 37: 2,2,3,1,3,1,3,4
  - 43: 2,2,2,1,4,4,2,2
  - 73: 2,2,2,1,3,1,4,4
  - 127: 2,2,2,1,3,3,2,4
  - 181: 2,2,2,3,3,1,2,4
  - 631: 2,2,2,2,3,3,2,3
  - 2521: 2,2,2,2,2,3,3,3
- **c = 8.** The value 18 occurs only at 29 and 43.
- **Tail (`tail_ref.py`).** The degree routine was run at one prime above 2·10⁶ in each of the 1152
  unit classes mod 5040, with searches disabled.
  - 0 mismatches with e = 1,2,2,2,2,2,3,3,3.
  - Tail maxima: 3, 5, 7, 9, 11, 14, 17, 20. At c = 9 the maximum is attained only at residues 1 and
    2521 mod 5040, that is, p ≡ 1 (mod 2520).
  - The hand argument of v2tex:83–85 is correct: the sum is ≤ 5·2 + 3·3 = 19, with equality iff
    2520 | p−1.
- **Conditional material (task 5).**
  - fragment-v2 uses only Cor. chain, Lemmas SM, ell-tensor and ell-node, and the finite tables.
  - Lemma P / composition is explicitly avoided, since only the composed tables are used.
  - The UNSAT of rem:below-20 enters only an optimality remark.
  - The author's code chain (rule_v2 → rule → halved_schedule) has USE_KD = False.
  - My run with S1 forbidden shows that thm:is-import is not needed for 20 either. It is still the
    core's import for c ≥ 10. This S1-free observation extends the 21-referee's side finding and,
    like it, needs its own referee before any paper use.

## 5. Fixes

- **G1 (material).** prop:ell-tables must state the B(y) = C_y/z^y storage convention (§3).
- **G2.** def:schedule1hplus2 should fix ξ = least primitive root (F4) and add a TL6 row to
  tab:sm-thresholds: (6,6,1), 837384, 40924516.
- **G3.** State the explicit band constant, about 36·T_samp/1.6·10⁻⁵ class tests, as F5 of the
  21-referee requires. Count TL6 among the preprocessing tasks of rem:is-import(d) (F6).
- **G4.** v2tex:87 says "Switching the new candidates off reproduces the core Schedule 1H". With
  only (g) and (h) off, the computation gives 1H⁺, not the core 1H. The core needs (c)–(h) off.
  Say both.

Fixes F1–F7 of the 21-referee are still unapplied in fragment.tex. 1H⁺⁺ inherits them.

## 6. Adversarial self-check

- **Shared code.** `plus2.py` shares its core with the `-21-recompute` code. A conceptual bug there
  would be replicated here.
  - That code reproduced the core's 38 and 53 and the refereed 1H⁺ 21, and my 1H⁺ regression matches.
  - The new candidates are only a few lines (`plus2.py`, the TL6/ELL block).
- **Shared data.** Certificates and tables are the author's data. I re-checked every item with new
  checkers, so a wrong item would be rejected, not used.
  - Availability below T_exist is by definition the author's table. My exhaustive NONE results show
    that existence agrees.
  - Those NONE results rest on rcsearch's DFS. It is brute-force-checked only at p = 7 and 13 for
    κ = 6.
- **Scope of "attained exactly".** This holds for the schedule as defined. "≤ 20" is the robust
  content.
- **Thresholds.** These are mine, but the formula is the lemma's. A wrong lemma would be reproduced.
  The lemma itself was re-read here and refereed earlier. Weil's locator is still unverified by a
  human.
- **Run time.** The 4 s runs are plausible, because the search cache was warm and the class sumsets
  are vectorised. The `none` regression reproducing 21 shows that the computation is live, not
  cached output.
- **First FAIL of the tables.** My first table check failed only because of the storage convention.
  I fixed my reader to C = z^y·B, which is the k9 note's convention. The raw-B controls then fail as
  they should.
- **Status.** Everything here is AI-checked and pending human review. All claim gates stay false.

Next command:

    nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-headline-20-referee/run2.py 2000000 def

Expected output: `E = {…, 8: 18, 9: 20}`, with the c = 9 maximum at 266 primes.

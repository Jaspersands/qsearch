# Rees SDE, p = 5: below n²/4 by sparse two-dimensional pieces (6/25), and why three-dimensional pieces from fresh blocks cannot help (2026-11-11, AI only)

AI-only pass, one Claude Code session; not human-reviewed; no novelty or priority claim (literature
only through `2026-11-07-rees-sde-subquad-lit.md`, `2026-11-08-rees-sde-lit2.md`,
`2026-11-08-rees-sde-p3-nest-lit.md`; no network). Inputs: `2026-11-08-rees-sde-fq-nest.md` §0–§1,
`2026-11-09-rees-sde-fq-nest-referee-B.md` (Theorem B′, SIMPLE5, Fact F5), `2026-11-11-rees-sde-p5-d3.md`
(Fact T3: F_5^3∖0 is infeasible, certified with the fixed lrat-check). Code and outputs:
`2026-11-11-rees-sde-p5-below-quarter/`, interpreter `/opt/anaconda3/bin/python -I`. Only this file and
that folder were written.

Labels: **[proved]** full proof here (finite inputs named); **[computed, how]**; **[argued]**;
**[conjecture]**. Problem: worst case, λ_1..λ_m ∈ F_5^n arbitrary, find x ∈ {0,±1}^m ∖ 0 with
Σ x_i λ_i = 0, deterministic poly(n, m). Notation (D(X), labels, supp W, R(Y), "gains", Lemma 1,
Lemma 2(A)/(B), feasible, weakly nondegenerate) as in `2026-11-08-rees-sde-fq-nest.md` §1.

## 0. Verdict

1. **Theorem S (SPARSE2) [proved; finite input Fact F5 only].** For every n ≥ 1 and every
   λ_1..λ_m ∈ F_5^n with
   **m ≥ (6/25) n² + (12/25) n log_5 n + 1.92 n + 3**,
   a nonzero x ∈ {0,±1}^m with Σ x_i λ_i = 0 is found deterministically in poly(n, m) time
   (O(n⁴ log n) field operations plus Fact F5 lookups). Leading constant 0.24 < 1/4 [proved]. The exact
   recursion is below Theorem B′ (n²/4 + 3n/2 + 2) for every n ≥ 29 [computed to n = 30,000; the analytic
   closed form itself beats B′ only for n ≳ 200], e.g. 242,502 vs 251,501 at
   n = 1000 and 0.2401 n² at n = 30,000 (`accounting.out`). The idea: Theorem B′ pays q + 2 for two
   dimensions because it uses the full support of two dependencies; KOW's averaging trick, applied
   to 2-dim subspaces of an r-dim dependency space (r ≈ log_5 q), finds two dependencies whose joint
   support is ≤ (24/25)(q + r) + O(1), and Fact F5 accepts any spanning label set.
2. **Lifting lemma [proved, given Fact T3].** For every k ≥ 3, F_5^k∖0 has no feasible weakly
   nondegenerate 3-dimensional realization (Φ: F_5^k∖0 → S³, γ_α ∈ F_5^k). More generally, a spanning
   L ⊆ F_5^k is 3-infeasible if more than 31 of its hyperplane sections are 3-infeasible and spanning
   in their hyperplanes (§3).
3. **Obstruction for the fresh-block family [proved, given Fact T3 and one exhaustive check].** For
   r ≥ 3, q = 5^r − 1 − r, the simplex block X_r (q + r columns in F_5^q, one per nonzero label of
   F_5^r) satisfies: no subset of X_r gains 3 dimensions or yields a witness; every piece Y ⊆ X_r
   that gains d ∈ {1, 2} costs |Y| ≥ (12/25)(q + r + 1)·d. So a method that builds each piece inside a
   block of q + r fresh columns with q + r = 5^r − 1, and is analysed by its worst-case piece cost, gets
   at best (12/25)q per dimension, i.e. leading constant ≥ 6/25 at those block sizes; SPARSE2's
   averaging bound is attained exactly on X_r (computed: |Y| = 120 = bound at q = 121, r = 3). For
   repeated simplex blocks (q + r = μ(5^r − 1)) the 2-dim cost floor holds too; the 3-dim exclusion
   there is the open multiset version of Fact T3. For a block of q + r uniformly random columns, with probability
   ≥ 1 − 5^{3r}(124/125)^{q+r}/12000, every 3-dim dependency subspace has the full label set F_5^3∖0
   [proved], so no label gadget (Lemma 2(A), Φ a function of the label) exists for any of them, however
   selected, once q + r ≥ 602r − 1169.
4. **What does not work [argued].** Pieces with ≤ 9 distinct labels (all feasible) are as hard to find
   as the problem itself in codimension q − 6 (§4.2). Selecting A so that the 3-dim label set avoids
   an infeasible pattern is a CSP over F_5^{3r}; only exhaustive search (r = O(log q)) is polynomial, and
   there the adversary makes every label set full. Beating the averaging bound for k = 2 needs a
   better-than-average 2-dim subcode, which random blocks do not allow beyond O(√(q log q)).
5. **Classical baseline [literature notes only].** Existence: pigeonhole on {0,1}-sums gives a
   {0,±1} solution for m > n log_2 5 ≈ 2.32 n; Olson/van Emde Boas–Kruyswijk give a 0/1 zero-sum for
   m ≥ 4n + 1. Constructive worst case at q = 5: KOW Thm 3.7 (0.4 n²), Theorem B′ (0.25 n²). The
   literature notes found no worst-case constant below these at p = 5 (KOMSW's 0.1022 is F_3, average
   case, unproved). This pass did not search the literature further.

Gates that stay false: "n²/6 at p = 5"; "6/25 is a lower bound for all algorithms" (§3 is a
per-piece obstruction for one family, not an instance lower bound); novelty or priority; "the
small-set and random-set infeasibility results are certified" (beyond Fact T3 and §3's proofs).

## 1. Theorem S: sparse two-dimensional pieces

**Stage (codimension q ≥ 2).** V = F_5^q is the current quotient. Let r = r(q) ∈ [2, ⌈log_5 q⌉ + 2]
minimise c(q, r) := ⌊(q + r)(1 − ρ_r)⌋, ρ_r := (5^{r−2} − 1)/(5^r − 1) (ties: smallest r; r = 2 gives
ρ = 0, i.e. Theorem B′'s piece). Take the first q + r unused columns X; if one is 0 in V it is a
witness. Their images have rank ≤ q, so dim D(X) ≥ r; fix an r-dim D0 ⊆ D(X), basis matrix G (r × |X|,
rank r), labels g_i ∈ F_5^r. For every 2-dim subspace W of the row space of G (equivalently every
codim-2 subspace K = ker A of F_5^r, W = row space of AG) compute |supp W| = #{i : g_i ∉ K}; take a
minimiser. Put Y = supp W and use the labels a_i := A g_i ∈ F_5²∖0 (i ∈ Y).

**Lemma S1 (the piece) [proved].** Y gains a 2-dim subgroup of V or yields a witness, at cost |Y|.
*Proof.* AG has rank 2 (G has rank r, A rank 2), so its nonzero columns a_i span F_5². Fact F5 gives a
feasible weakly nondegenerate (Φ, γ) on {a_i}. Set y_α(i) = ⟨α, Φ(a_i)⟩ + ⟨γ_α, a_i⟩ ∈ S (i ∈ Y),
h_j = Σ_{i∈Y} Φ_j(a_i) v_i. The vector (⟨γ_α, a_i⟩)_{i ∈ X} = γ_α^T A G is a dependency of X that vanishes
off Y, so Σ_{i∈Y} ⟨γ_α, a_i⟩ v_i = 0 and Σ_{i ∈ Y} y_α(i) v_i = α·h. If h_1, h_2 are independent, Y
gains ⟨h_1, h_2⟩. Otherwise α·h = 0 for some α ≠ 0, and weak nondegeneracy gives λ with y_{λα} ≢ 0 on
Y and Σ y_{λα}(i) v_i = 0: a witness in V. This is Lemma 2(A) with Y in place of X; multiplicities of
labels do not matter because Φ is applied per column through its label. ∎

**Lemma S2 (averaging) [proved].** min_W |supp W| ≤ (1 − ρ_r)·#{i : g_i ≠ 0} ≤ c(q, r), and
(1 − ρ_r) = (24/25)·5^r/(5^r − 1).
*Proof.* A nonzero g lies in [r−1, r−3]_5 = [r−1, 2]_5 of the [r, 2]_5 codim-2 subspaces, a fraction
[r−1,2]_5/[r,2]_5 = (5^{r−2} − 1)/(5^r − 1) = ρ_r; columns with g_i = 0 (coloops of D0) are in no support.
So the average of |supp W| over all W is (1 − ρ_r)#{g_i ≠ 0}; the minimum is at most the average and is
an integer. 1 − ρ_r = (5^r − 5^{r−2})/(5^r − 1). ∎

The number of subspaces enumerated is [r, 2]_5 < 25^r ≤ 25³q² (as r ≤ log_5 q + 3), each
evaluated in O(q r) operations, so a stage costs O(q³ log q) and the whole run O(n⁴ log n); Fact F5 is a
table of 36,090 orbit gadgets (or a 2-dim CNF, as in SIMPLE5). Everything is deterministic.

**Recursion.** After a gain, X ∖ Y returns to the pool and the algorithm continues in V/⟨h_1, h_2⟩
(codimension q − 2) with pieces disjoint, so Lemma 1 unwinds any later witness. q = 1: two columns
realize the line or give a witness ({a + bc : a, b ∈ S} = F_5 for c ≠ 0); one closing column. With
G(0) = 1, G(1) = 3, G(q) = max(q + r(q), c(q, r(q)) + G(q − 2)), m ≥ G(n) suffices.

**Closed form [proved].** For q ≥ 2 put r0 = ⌈log_5 q⌉ + 1 ≤ ⌈log_5 q⌉ + 2, so 5^{r0} ≥ 5q and
c(q, r(q)) ≤ c(q, r0) ≤ (24/25)(q + r0)(1 + 1/(5q − 1)) ≤ (24/25)(q + log_5 q + 3) (as (q + r0)/(5q − 1) ≤ 1).
Summing over q = n, n − 2, …, ≥ 2 (at most n/2 terms, Σ q ≤ (n² + 2n)/4, Σ log_5 q ≤ (n/2) log_5 n):
Σ c ≤ 0.24 n² + 0.48 n log_5 n + 1.92 n. The pool term never binds beyond the tail: at a stage
q + r − c ≤ (q + r)/25 + 1 ≤ (q − 2)/2 + 3, which is at most the cost of the later stages plus the tail 3
(c(q) ≥ (24/25)(q + r) − 1 ≥ (q − 2)/2). Tail ≤ 3. Hence G(n) ≤ 0.24 n² + 0.48 n log_5 n + 1.92 n + 3. ∎
[computed: `accounting.py` evaluates the exact recursion for all n ≤ 30,000; the stage inequality and the
closed form hold for all q, n ≤ 30,000 (re-checked with 1.92n; G(n) exceeds 0.24n² + 0.48 n log_5 n by
less than 1.92n + 3 everywhere), G(n) < B′(n) for n ≥ 29.]

**Tests [computed, `test_sparse2.out`].** SPARSE2 implemented on top of referee B's SIMPLE5 primitives
(its quotient, gadget CNF with arithmetic re-check, and `unwind`, which re-sums every returned x over the
original columns). At m = G(n) exactly, n ∈ {6, …, 50}, nine families (random; simplex blocks r = 2, 3,
direct-sum and randomly overlaid; series classes; weight-2; few distinct; low rank): 225 runs, 0
failures; every stage's |Y| ≤ c(q, r) (asserted). Pure simplex block at q = 121: first piece |Y| = 120 =
c(121, 3) (the bound is attained). Hill climb on consumption at n = 8, 10, 12 (4 starts × 150 mutations): no failure; pieces consumed up
to m − 1 (28/29, 40/41, 54/55), so the small-n recursion is tight. Total 474 s, 0 failures.

## 2. Lifting lemma (three dimensions in any number of dependencies)

**Lemma L [proved, given Fact T3].** For k ≥ 3, L_k = F_5^k∖0 admits no Φ: L_k → S³, γ_α ∈ F_5^k
(α ∈ F_5³∖0) with all y_α = ⟨α, Φ⟩ + ⟨γ_α, ·⟩ S-valued on L_k and weakly nondegenerate.
*Proof.* Induction on k; k = 3 is Fact T3. Let k ≥ 4 and suppose (Φ, γ) exists. For a hyperplane H let
K_H = {α : Σ_j α_j Φ_j|_H equals a linear functional on H}, a linear subspace of F_5³. For α ∈ K_H,
y_α|_H is a linear functional on H with values in S on H∖0, hence 0 (a nonzero functional takes the value
2). If K_H = 0 then every y_α (α ≠ 0) is nonzero on H∖0, and (Φ|_H, γ_α|_H) solves L_{k−1} ≅ H∖0 with
strong nondegeneracy (y_α ≢ 0 for every α ≠ 0, which implies weak nondegeneracy), contradicting the
induction hypothesis. So each of the (5^k − 1)/4 ≥ 156
hyperplanes has dim K_H ≥ 1, and F_5³ has 31 lines: some line ⟨α⟩ lies in K_{H1} ∩ K_{H2}, H1 ≠ H2.
For every λ ∈ F_5^*, y_{λα} vanishes on (H1 ∪ H2)∖0. Now y_{2λα} − 2y_{λα} = ⟨γ_{2λα} − 2γ_{λα}, ·⟩ is a
linear functional vanishing on H1 ∪ H2, which spans F_5^k, so y_{2λα} = 2y_{λα}; S ∩ 2S = {0} forces
y_{λα} ≡ 0. So [α] is degenerate, a contradiction. ∎

The proof only uses, for each hyperplane section, its infeasibility and that it spans its hyperplane
(so that a functional vanishing on two sections vanishes on L): **any spanning L ⊆ F_5^k with at least
32 hyperplanes H for which L ∩ H spans H and is 3-infeasible is 3-infeasible [proved]**, and d ≥ 3
dimensions are impossible whenever 3 are (restrict α to a 3-dim subspace).

## 3. Obstruction for pieces built inside a fresh block

**Simplex blocks [proved, given Fact T3 and `k1d2.out`].** For r ≥ 3 let X_r be 5^r − 1 columns in
F_5^q, q = 5^r − 1 − r, with D(X_r) = the simplex code (columns of a generator = all nonzero labels, once
each; such columns exist for every code). Then:
- (a) No Y ⊆ X_r gains a subgroup of dimension ≥ 3, and no Y ⊆ X_r carries a witness. Lemma 2(B) is
  stated for d = k; its proof gives verbatim, for any d and k with W = D(X) (here dim D(X_r) = r, since
  rank X_r = q) and one column per label: a d-dim subgroup of R(X) yields a feasible strongly
  nondegenerate (Φ: L → S^d, γ_α ∈ F_5^k). With Lemma L (d = 3, k = r) R(X_r) has no 3-dim subgroup; a
  witness would be a nonzero simplex codeword with values in S, but such a codeword takes the value 2.
  R(Y) ⊆ R(X_r).
- (b) If Y ⊆ X_r gains a 2-dim subgroup then dim D(Y) ≥ 2. dim D(Y) = 0 gives no nonzero subgroup
  (y_2α = 2y_α forces 0). dim D(Y) = 1: **one dependency never gains two dimensions at p = 5, with
  per-column Φ and arbitrary multiplicities** [computed, exact, two code paths in `k1d2.py`: a CNF over
  g = γ (one-hot) and 36 column types (Φ, w_i) is UNSAT; an exhaustive enumeration of all 244 distinct
  admissible-type families T_g finds none that makes h_1, h_2 independent; no label reduction used].
- (c) Every 2-dim subcode of the simplex code has support exactly 5^r − 5^{r−2} = 24·5^{r−2} (a label lies
  outside the support iff it lies in the codim-2 kernel), every nonzero codeword weight 4·5^{r−1}.
These bounds concern pieces that gain in the current quotient V while X_r is the current block (in
later quotients the leftover columns of X_r acquire new dependencies and the simplex structure is gone).
So a piece Y ⊆ X_r realizing d dimensions costs ≥ 24·5^{r−2} (d = 2) or ≥ 4·5^{r−1} (d = 1): at least
(12/25)·5^r = (12/25)(q + r + 1) per dimension, which is exactly c(q, r)/2 for SPARSE2 at this (q, r)
(Lemma S2 is tight; SPARSE2's argmin rule picks this very r at q = 121, 620, 3119, with c = 120, 600,
3000 = 24·5^{r−2}; the alternative rule r0 = ⌈log_5 q⌉ + 1 would take one more dependency). Pieces of q + r columns whose dependency code is a repeated simplex code (μ copies)
also have every 2-dim support equal to the averaging bound, by (b), (c); whether they admit 3-dim gains
(the multiset version of Fact T3) is **open** [conjecture: no].

**Random blocks [proved].** Let X be q + r uniformly random columns of F_5^q, conditioned on rank q, so
D(X) is a uniformly random r-dim subspace of F_5^{q+r} (the law is GL_{q+r}-invariant). The number of
3-dim subspaces W′ ⊆ F_5^N (N = q + r) whose label set is not all of F_5³∖0 is at most 124·124^N/|GL_3(F_5)|
(each such W′ has |GL_3| bases, each avoiding some label u), and P(W′ ⊆ D(X)) ≤ 5^{3(r−N)}. So
P(some 3-dim W ⊆ D(X) has a non-full label set) ≤ 5^{3r}(124/125)^N/12000, which is < 1 once
N ≥ 602 r − 1169 and tends to 0 for fixed r. On that event every 3-dim dependency subspace of X has the
label set F_5³∖0, so by Fact T3 no gadget with Φ a function of the label (Lemma 2(A)) exists for it,
whatever rule selects it. (Labels repeat here, so "Y gains no 3-dim subgroup" would need the multiset
version of Fact T3, open; see §6.) [This covers d = 3 from a 3-dim subcode; d = 3 from all r dependencies of a random block with
sparse labels in F_5^r is not covered — open.]

**Reading [argued].** Theorem B′ and SPARSE2 both analyse a piece by a worst case over the dependency
code of q + O(log q) fresh columns. In that model the adversary's simplex-type blocks force ≥ (12/25)q per
dimension and rule out 3-dim gains, so 6/25 is the best constant such an analysis can give. This is not
an instance lower bound: an algorithm may choose blocks adaptively from the whole pool (Θ(n²) columns),
and the adversary has not been shown to make every adaptively chosen block simplex-like in every quotient.

## 4. Directions tried and why they fail

1. **Bounded label count (≤ 9 labels) [argued].** Columns with equal labels up to sign (allowed, since L
   and L ∪ −L are equally feasible) appear with equal or opposite coefficients in every dependency of W,
   so W is the dependency space of r ≤ 9 signed class sums u_C = Σ_{i ∈ C} ±v_i, and these span ≤ r − 3
   dimensions. Producing them means r disjoint {0,±1}-combinations landing in a common (≤ 6)-dim space,
   i.e. solving the problem itself in codimension ≥ q − 6, at least ~f(q − 6) columns for the best known f.
   On generic blocks the q + 3 labels of a 3-dim W are spread over all 124 labels.
2. **Steering W so that its labels avoid an infeasible pattern [argued].** With labels g_i ∈ F_5^r and
   W ↔ A ∈ F_5^{3×r}, the requirement "A g_i ∉ M for all i" is a CSP; by counting, solutions exist only
   when r is a constant fraction of q, where no polynomial search is known; for r = O(log q) the random-block
   lemma (and the simplex block) kill every A. Mapping into a slab {⟨g, ·⟩ ∈ S} is the problem itself.
3. **Mixing k = 2 and k = 3 [argued].** k = 3 pieces are guaranteed only for ≤ 9 labels, i.e. q ≤ 6
   (q + 3 columns): an O(1) saving. A k = 2 piece followed by a one-dimensional sparse piece costs
   (24/25 + 4/5)q per three dimensions, worse than SPARSE2.
4. **Better than averaging for k = 2 [argued].** For random blocks, every codim-2 subspace of F_5^r
   contains (1/25)N ± O(√(N r)) labels, so the minimum support is (24/25)q − O(√(q log q)); smarter
   two-step choices (sparse w_1, then w_2 vanishing on part of the complement) give (24/25)q + 0.16 r.
5. **Larger k with d = 3 (q + k columns, gain 3) [proved negative for full label sets].** Lemma L: no
   number of dependencies rescues the full set, and blocks with r ≤ log_5(q + r + 1) can be full.

## 5. Claude research agent (advisory)

One adversarial Opus/high request (`2026-11-11-rees-sde-p5-below-quarter/claude/`, prompt and context
files there, run bundle `claude/run1/`): obligations were Theorem S (piece, averaging, recursion,
accounting, running time), Lemma L and the simplex corollary, and one idea or reason for going below
6/25. Run: stop_reason end_turn, 4,827 input / 20,322 output tokens (cost in `claude/run1/result.json`).
Verdicts: Theorem S ACCEPT WITH FIXES (no correctness gap found); Lemma L ACCEPT WITH FIXES; the
simplex cost sentence REJECT as stated. Disposition (each checked here):
- r-rule underspecified: **accepted**; the rule is the argmin of c(q, r) over r ∈ [2, ⌈log_5 q⌉ + 2] (§1),
  which the proof covers since c(q, r(q)) ≤ c(q, r0).
- Finite controls must be labelled: **accepted**. The analytic closed form beats B′ only for n ≳ 200;
  "G(n) < B′(n) for n ≥ 29" is a computation of the exact recursion. The leading constant 6/25 is proved.
- "Strongly nondegenerate" undefined: **accepted**, defined in §2.
- Lemma 2(B) used with d ≠ k: **accepted**, the d ≠ k version (W = D(X)) is stated in §3(a).
- Cost sentence: (i) relies on the one-dependency fact: **open as an input, not rejected** — it is an
  exhaustive finite enumeration with two code paths (`k1d2.out`), labelled [computed]; (ii) first stage
  only: **accepted**, scope sentence added in §3; (iii) "SPARSE2 takes r + 1 there": **rejected** for the
  implemented argmin rule (it picks r, computed above), correct for the r0 rule; (iv) framework-only
  scope: already stated.
- Its item 3 (6/25 is the floor for per-stage subcode selection inside a simplex window; the only lever
  is cross-stage, forcing a non-simplex window in a later quotient through the Φ freedom): **agrees with
  §3; taken as the next question** (§6).

## 6. Next

- Hard question (also the referee agent's suggestion): can the algorithm, through its choice of Φ (hence
  h) and of blocks, force a non-simplex window in a later quotient, or is there a recursive adversary
  keeping every window simplex-like for every choice? Equivalently: does some poly-time rule pick blocks adaptively from the Θ(n²)-column pool so that the
  label sets of 3-dim dependency spaces lie in a provably feasible family, or is there a pool-level
  adversary (every adaptively chosen block simplex-like in every quotient)?
- Cheapest finite step: decide the multiset version of Fact T3 (F_5³∖0 with every label twice, per-column
  Φ) with `labelsat.py`-style encoding plus the fixed lrat-check; if infeasible, the simplex obstruction
  extends to every block size q + r with r ≤ log_5(q + r + 1).
- Possible transfer: the same averaging applies at any p where every spanning 2-dim label set is
  feasible (only p = 5 is known); at p = 3 only nested label sets are feasible, so sparse supports need a
  new feasibility check there.

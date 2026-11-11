# Rees SDE at bounded p: a local-to-global theorem for piece gadgets; full and nested label sets give one dimension per piece at p = 7, 11 for every number of dependencies; the p = 5 / p ≥ 7 gap is real for the piece method

AI-only pass, 11 November 2026, one Claude Code session plus one Claude API adversarial check
(§7). Not human-reviewed, no novelty or priority claim. Scripts and outputs:
`2026-11-11-rees-sde-bounded-p/`, interpreter `/opt/anaconda3/bin/python -I`. Only this file
and that folder were written; no git, no STATE/handoff/plan/paper edit.

Labels: **[proved]** complete proof here (finite inputs named); **[computed]** complete finite
computation by the named program, UNSAT not LRAT-certified unless said; **[certified]** CaDiCaL
UNSAT with an LRAT proof verified by the fixed checker
`2026-11-09-lrat-checker-fix/lrat-check` (controls run first, `CONTROLS OK`); **[argued]**;
**[conjecture]**.

Problem (worst case). λ_1..λ_M ∈ F_p^a; find nonzero x ∈ S^M with Σ x_iλ_i = 0,
S = P ∪ {0}, P = (F_p^*)^κ. Known at bounded p (`2026-11-08-rees-sde-fq-nest.md` §0,
`2026-11-11-rees-sde-p5-d3.md`): p = 3, 5 (κ = 2) n²/4 + O(n); every odd p (κ = 2)
(1−1/p)a²/2 + O(a log a) (Theorem C); no two-dependency, two-dimensional gadget at p = 7, 11
(certified), 13 (CaDiCaL only); F_5^3∖0 not 3-feasible (certified). Everything below is κ = 2
unless stated.

## 0. Verdict

1. **Theorem LG (local-to-global) [proved; §2; AI-checked §7].** Let L ⊆ F_p^k∖0 be a label
   set whose *full lines* (lines F_p^*u ⊆ L) span F_p^k. If no planar section L ∩ span(u, w),
   for full lines u ≠ w, has a weakly nondegenerate 2-family, then L has none, for every
   d ≥ 2: every family on L has rank ≤ 1. A piece with such a label set, with any column
   multiplicities, realizes no 2-dimensional subgroup and contains no S-witness. Rank version
   (Theorem LG_R): if F_p^R∖0 is not R-feasible, no piece with full label set F_p^k∖0 (any k)
   realizes R dimensions. No computation enters the theorem; it needs only Lemma 2/R/N of the
   F_q note and the elementary Lemma 1 (one dependency never gives two dimensions, all p).
2. **Corollaries [proved, from certified finite inputs].**
   - p = 7 and p = 11: for **every** k ≥ 2, neither the full set F_p^k∖0 nor the nested set
     {ℓ : ℓ_1 ≠ 0} is 2-feasible (inputs: the certified nested planar UNSAT at p = 7, 11). This
     proves the conjecture of fq-nest §7 ("no k-dependency bundle gains two dimensions at
     p ≥ 7") for these two label families; the k = 3, p = 7 SAT run and any k = 4 run are now
     unnecessary. p = 13: same (input certified 11 Nov: 37/37 cases LRAT VERIFIED by the fixed checker,
     `2026-11-09-lrat-checker-fix/recheck/cases13_cases.out`; integrator's update).
   - p = 5: for every k, F_5^k∖0 is not 3-feasible (input: certified F_5^3∖0). So with full
     label sets p = 5 is capped at two dimensions per piece (Theorem B′'s n²/4), for any number
     of dependencies.
   - Pools (Corollary 2): if a pool's label set is full, every sub-piece's label set is full.
     So for a pool with full labels, no sub-piece of any size gains 2 dimensions at p = 7, 11.
3. **Planar landscape [computed; certification status in §4].** Unions of m full lines in
   F_p^2: p = 3: feasible iff m ≤ 3; p = 5: all m ≤ 6 feasible; **p = 7: feasible iff m ≤ 3**
   (m = 4: both PGL_2-orbits UNSAT, one of them LRAT-certified; m = 5..8 UNSAT); **p = 11:
   feasible iff m ≤ 4** (m = 5: both orbits, all 792 sets, UNSAT); **p = 13: every m ≤ 5
   feasible** (all orbits; larger m not run). So the line threshold grows with p (3, 3, 4, ≥ 5 at
   p = 3, 7, 11, 13; p = 5 exceptional). At p = 7 a two-dimensional piece needs a plane section
   whose labels lie on ≤ 3 full lines ("theta") or carry half-lines (labels of one P-class only).
   **Half-lines change the picture [computed, SAT models verified]:** at p = 7, 224 of the 256
   choices of one P-class on each of the 8 lines give a 2-feasible set with no S-functional (the
   other 32 have one). With no full line, S-functional-free feasibility starts at 5 half-lines;
   with 3 full lines, ≥ 3 added half-lines is always infeasible (§4).
4. **Barrier for the piece method at p ≥ 7 [argued, §5].** (a) [proved] Lemma T: if every
   nonzero dependency of the pool has weight ≥ w, a two-dependency piece whose labels lie on m
   lines has |X| ≥ m·w/(m−1); thetas (m = 3) need w ≤ (2/3)|X|, impossible when the pool's
   dependency code is near-equidistant (w ≈ (1−1/p)N), which is exactly the code that makes
   Theorem C tight. (b) [argued] On random banks with pools of l + r columns,
   r ≤ (1−ε) log_p l, pool labels are full with probability → 1, so by Corollary 2 and LG no piece
   gains two dimensions at p = 7, 11, and each one-dimensional round costs
   (1−1/p)l − O(√(l log l)): the method is stuck at (1−1/p)a²/2 − o(a²) there, against a²/4
   at p = 5. The gap between p = 5 and p ≥ 7 is therefore real for this method **with pools of
   l + O(log l) columns**. (d) [argued, first moment] It is not existential: in pools of
   ≈ 1.22·l random columns, 2-dependency pieces of ≈ 1.19·l columns whose labels form 8 feasible
   half-lines should exist (versus 2·(6/7)l ≈ 1.71·l for two Theorem C rounds, a 30% saving), but
   locating one is a search over ~2^{1.2l} subcodes. So at p = 7 the obstruction is to finding,
   not to existence. (c) [argued]
   For sparse label sets (k ≳ log_p l) LG says nothing; a first-moment count says a random
   sparse label set of n labels is 2-feasible only if k ≳ 0.2n at p = 7, i.e. gadget search
   over p^{Ω(n)} values.
5. **What is not changed.** No o(a²) and no constant-factor improvement at any fixed p ≥ 7; no
   progress on Q-loc or on p between a and a·polylog (§6). Theorem C remains the best proved
   bounded-p result for p ≥ 7. LG is a barrier for one method family, not a lower bound for
   algorithms.

## 1. Setup (from fq-nest §1, restated)

A piece X has dependency space D(X) of dimension k; fixing a basis δ^1..δ^k, column i has label
ℓ_i = (δ^1_i..δ^k_i) ∈ F_p^k; the nonzero labels span F_p^k. A **d-family** on a label set L is
y_α: L → S (α ∈ F_p^d∖0) with y_α(ℓ) = ⟨α, Φ(ℓ)⟩ + ⟨γ_α, ℓ⟩, Φ: L → S^d, γ_α ∈ F_p^k; put
y_0 = 0. **Weakly nondegenerate**: every direction [α] has some λα with y_{λα} ≢ 0 on L. Lemma 2:
a piece realizing a d-dim subgroup gives a feasible weakly nondegenerate d-family on its labels,
and conversely such a family gains d dimensions or gives a witness. Lemma R: WLOG
γ_{λα} = λγ_α (λ ∈ P), γ_{e_j} = 0. Lemma N: if L spans and has no nonzero S-valued linear
functional, [α] is degenerate iff γ_{rα} = rγ_α (r ∉ P). Elementary fact: S ∩ λS = {0} for
λ ∉ P, and a nonzero linear functional on a line takes every value in F_p^*, so it is not S-valued.

Notation. F(L) = functions L → F_p, Lin(L) = restrictions of linear functionals. Since
y_α − Σ_j α_j y_{e_j} ∈ Lin(L), the map α ↦ [y_α] ∈ F(L)/Lin(L) is linear. Its kernel is
K(L) ⊆ F_p^d and its **rank** is d − dim K(L). For a subset L′ ⊆ L, restricting gives a family on
L′ with K(L) ⊆ K(L′). For a full line u (F_p^*u ⊆ L) write K_u = K(F_p^*u).

## 2. Lemmas and Theorem LG

**Lemma K [proved].** If L has no nonzero S-valued linear functional, then
K(L) = {α : y_α ≡ 0 on L}, and the family is weakly nondegenerate iff K(L) = 0.
*Proof.* α ∈ K(L) iff y_α|_L is linear; it is S-valued, hence 0. K(L) is a subspace, so
λα ∈ K ⟺ α ∈ K. ∎

**Lemma V (vanishing) [proved].** For any feasible family and α ≠ 0 put
Δ_α = γ_{rα} − rγ_α. Then y_{rα} − r·y_α = ⟨Δ_α, ·⟩, so y_α(ℓ) = 0 wherever ⟨Δ_α, ℓ⟩ = 0; and
for a full line u, K_u = {0} ∪ {α ≠ 0 : ⟨Δ_α, u⟩ = 0}.
*Proof.* ⟨rα, Φ⟩ = r⟨α, Φ⟩. Where ⟨Δ_α, ℓ⟩ = 0, y_α(ℓ) ∈ S ∩ r^{-1}S = {0}. On a full line, the
converse uses that K_u is a subspace (Lemma K on the line). ∎
So every realizer y_α is supported inside the support of the single dependency ⟨Δ_α, ℓ_i⟩.
(In the plane: if no line is identically dead, α ↦ ker Δ_α is a bijection from the p + 1
directions to the p + 1 lines.)

**Reparametrization [proved].** For an injective linear B: F_p^{d′} → F_p^d,
y′_β := y_{Bβ} is a d′-family with Φ′(ℓ) = (y_{Be_1}(ℓ), …, y_{Be_{d′}}(ℓ)) ∈ S^{d′},
γ′_β = γ_{Bβ} − Σ_j β_jγ_{Be_j}, and kernel B^{-1}(K). (Φ′ must be taken from the y-values;
B^TΦ need not lie in S^{d′}.) If codim K ≥ 2, choosing B(F_p^2) ∩ K = 0 gives a 2-family with
trivial kernel.

**Lemma 1 (one dependency, every odd p) [proved].** For every family and every full line u,
codim K_u ≤ 1. In particular F_p^* (k = 1) is not 2-feasible.
*Proof.* Otherwise reparametrize to a 2-family on F_p^* with trivial kernel, weakly
nondegenerate by Lemma K. By Lemma N (F_p^* spans F_p^1 and has no S-functional) one may take Φ′
P-equivariant, Φ′(λℓ) = λΦ′(ℓ) for λ ∈ P; then each y′_β is P-equivariant, and P-equivariant
functions on F_p^* form a space of dimension κ = 2 containing the 1-dimensional Lin. So the rank
is ≤ 1, a contradiction. ∎ (For κ = 3 the same count allows rank 2; κ = 3 needs the computed
k = 1 cell of fq-nest §2 and is not claimed here.)

**Theorem LG [proved].** κ = 2, any odd p. Let L ⊆ F_p^k∖0 and FL its set of full lines.
Assume FL spans F_p^k and, for any two **distinct** full lines u, w, the planar section
L ∩ span(u, w), as a label set in that plane, has no weakly nondegenerate 2-family. Then every
d-family on L has codim K(L) ≤ 1. Hence for d ≥ 2 none is weakly nondegenerate, and no piece
with label set L (any multiplicities) realizes a 2-dimensional subgroup or contains an
S-witness.
*Proof.*
- L has no nonzero S-valued functional: one would vanish on each full line, and FL spans. So
  Lemma K applies to L and to every section containing two independent full lines.
- For full lines u ≠ w and W = span(u, w): K(L ∩ W) ⊆ K_u ∩ K_w. If codim K(L ∩ W) ≥ 2,
  reparametrizing gives a weakly nondegenerate 2-family on L ∩ W, excluded. So
  codim(K_u ∩ K_w) ≤ 1.
- By Lemma 1 every K_u is F_p^d or a hyperplane; two distinct hyperplanes meet in codimension 2,
  so all hyperplane K_u equal one hyperplane H (any H if there are none). H ⊆ K_u for all u.
- Let 0 ≠ α ∈ H. Then y_α and y_{rα} vanish on every full line, so ⟨Δ_α, ·⟩ = y_{rα} − r y_α
  vanishes on the full lines, which span: Δ_α = 0. So y_{rα} = r y_α on L and
  y_α ∈ S ∩ r^{-1}S = {0}. Thus H ⊆ K(L).
- Last clause: an S-witness inside X is (⟨c, ℓ_i⟩)_i for an S-valued functional c, which is 0.
  A realized 2-dim subgroup gives, by Lemma 2(B), a family with Φ per column; keeping γ and taking
  Φ from one column per label preserves feasibility, and by Lemma N the degenerate directions
  depend on γ only, so it is a weakly nondegenerate 2-family on L. ∎

**Monotonicity [proved].** If L′ ⊆ L both contain two independent full lines spanning (so
Lemma N applies to both) and L is 2-feasible, then so is L′ (degeneracy ⟺ γ_{rα} = rγ_α on both).
So infeasibility of a planar set passes to every planar superset whose full lines span.

**Theorem LG_R (rank) [proved; gap found and repaired by the §7 check].** If FL spans,
K(L) = ∩_{u∈FL} K_u (last step of LG's proof), so rank(L) = dim Σ_u K_u^⊥, each K_u^⊥ of
dimension ≤ 1. If rank(L) ≥ R, pick u_1..u_R with independent K_{u_i}^⊥. Their span may have
dimension < R (this inference was wrong in my draft); instead: if k ≥ R take any R-dimensional W′
containing them; then L ∩ W′ = W′∖0 when L = F_p^k∖0, and K(W′∖0) ⊆ ∩K_{u_i} has codim ≥ R; if
k < R, pull the family back along a coordinate projection F_p^R → F_p^k (labels in its kernel get
Φ = 0), which does not enlarge K. Either way F_p^R∖0 has a rank-R family, hence (reparametrize)
an R-feasible one. **So R*(p) := max{R : F_p^R∖0 is R-feasible} bounds the dimensions realized
by any full-label piece, for every k**, and {R : F_p^R∖0 R-feasible} is an initial segment.

## 3. Corollaries

**Corollary 1 [proved].** (i) If F_p^2∖0 is not 2-feasible, then F_p^k∖0 is not 2-feasible for
any k. (ii) Same for the nested sets N_k = {ℓ : ℓ_1 ≠ 0}: a plane spanned by two lines off
{ℓ_1 = 0} meets N_k in a nested planar set (GL_2 coordinates), and the full lines of N_k span.
(iii) A nested-planar UNSAT gives the full-planar UNSAT by Monotonicity.

Inputs and consequences:

| p | planar input | status of input | consequence for every k |
|---|---|---|---|
| 3 | F_3^2∖0 UNSAT (4 lines) | [computed] here (`lines3.out`), also fq-nest p = 3 | full sets 2-infeasible (nested planar is feasible, so N_k not covered) |
| 5 | F_5^3∖0 not 3-feasible | [certified] `2026-11-11-rees-sde-p5-d3/fullsb_m{1,2,3}.out` (+ hand-checked symmetry breaking) | R*(5) = 2: full-label pieces gain ≤ 2 |
| 7 | nested planar UNSAT | [certified] `2026-11-09-lrat-checker-fix/recheck/unsplit_7_2.out` (unsplit, no case split) | full and nested sets 2-infeasible; R*(7) = 1 |
| 11 | nested planar UNSAT | [certified] `recheck/cases11_cases.out` (30/31) + `cases11_c10.out` (1/1), Lemma U cover | full and nested 2-infeasible; R*(11) = 1 |
| 13 | nested planar UNSAT | CaDiCaL only (`2026-11-08-rees-sde-fq-nest/cases13_split.out`); recheck running | conditional |

**Corollary 2 (pools) [proved].** Let a pool have dependency code D of dimension r and full label
set F_p^r∖0. For X ⊆ pool, D(X) ≅ U^⊥ with U = span(labels outside X), and the labels of X are
the images in F_p^r/U of the labels in X; every point outside U is a label in X, so the image is
(F_p^r/U)∖0, i.e. full. (Labels in U become zero labels: weight 0.)

## 4. Planar computations

Decision procedure: `bt.py` (Python) and its C port `btc.c` (identical search and node counts;
`btc_run.py` verifies every SAT model by plain arithmetic on the P-closure, all α). Encoding uses
only Lemma R, Q, N. Cross-checks: p = 3 full UNSAT / nested SAT, p = 5 full SAT, k = 1 d = 2 UNSAT at
p = 5, 7, all as in fq-nest; p = 7 full set (8 lines) UNSAT in 74 s, agreeing with the certified
nested result. The existing CNF encoder `gadget_cnf5.py` (CaDiCaL) also gives SAT for the p = 7
3-line set (`lines7_lrat.out`).

| p | m = 2 | 3 | 4 | 5 | 6 | 7 | 8 | outputs |
|---|---|---|---|---|---|---|---|---|
| 3 | SAT | SAT | UNSAT (full) | | | | | `lines3.out` |
| 5 | SAT | SAT | SAT | SAT | SAT (full) | | | ad hoc run, §8 |
| 7 | SAT | SAT | UNSAT (2/2 orbits) | UNSAT | UNSAT | UNSAT | UNSAT (full) | `lines7.out` |
| 11 | SAT | SAT | SAT (2/2 orbits) | UNSAT (2/2 orbits, 792 sets) | UNSAT (1 orbit run) | | | `lines11.out` |
| 13 | SAT | SAT | SAT (3/3 orbits) | SAT (3/3 orbits, 2002 sets) | not run | | | `lines13.out` |

All UNSAT entries are [computed] by `btc` (no proof) except **both p = 7, m = 4 orbits (`lines7_lrat.out`, covering all $\binom{8}{4}=70$ 4-line sets): [certified]**:
- Orbit `{(1,0),(1,1),(1,2),(1,3)}` (`p7_L4a.txt`, size 42 in `lines7.out`, misstated earlier as 182 from `lines13.out`): `gadget_cnf5.py` CNF sha256 `4b0f3d4630bc917b…`, CaDiCaL UNSAT 1690 s, 12.1 GB LRAT proof, `LRAT VERIFIED` by the fixed checker in 263.7 s (proof deleted afterwards).
- Orbit `{(1,0),(1,1),(1,2),(1,4)}` (`p7_L4b.txt`, size 28 in `lines7.out`, misstated earlier as 546 from `lines13.out`): `gadget_cnf5.py` CNF sha256 `aaf08ffade180f9d…`, CaDiCaL UNSAT 1140.8 s, 12.51 GB LRAT proof (sha256 `cd15012ac621505c…`), `LRAT VERIFIED (streamed)` over FIFO into the fixed `lrat-check` (sha256 `13f28c96a0f3df28…`, `controls.sh` 14/14 OK).

Monotonicity (§2) makes m ≥ 5 follow from m = 4 (p = 7) and m ≥ 6 from m = 5 (p = 11). SAT entries are self-certifying (model verified). Full-line unions spanning the plane never carry an S-functional (f(λu) = λf(u) would put F_p^*·f(u) inside S), so every SAT entry is a genuine 2-family.

**Half-lines at p = 7** (`halflines_classify.py`, `halflines7.out`; post-processing
`halflines_post.py` → `halflines7_post.out`; 143 GL_2-orbits of P-closed sets with m ≤ 3 full
lines plus half-lines, none timed out). Verdicts by (full lines, half-lines), ignoring sets that
carry an S-functional:

| full m | feasible (SAT, no S-functional) | infeasible |
|---|---|---|
| 0 | 5 half-lines: 2 of 6 orbits; 6: 2 of 4; 7: 3 of 5; 8: 1 of 2 (224 of 256 patterns) | none; the other orbits (and all sets with ≤ 4 half-lines) are SAT only via an S-functional; the empty set is UNSAT |
| 1 | 2 half-lines: 1 of 2 orbits; 3: 3 of 5; 4: 8 of 10; 5: 9 of 10; 6: 7 of 8; 7: 3 of 5 | one orbit with 7 half-lines (size 112); the rest SAT via an S-functional; the bare line is UNSAT |
| 2 | ≤ 3 half-lines: all; 4: 9 of 12 orbits; 5: 2 of 10 | 6 half-lines: all |
| 3 | ≤ 1 half-line: all; 2: 3 of 6 orbits | ≥ 3 half-lines: all |

UNSAT here is [computed] by `btc`, not certified, and is used in no proved claim. The finding that
matters is on the SAT side: full lines are what LG uses, and half-line structures are typically
feasible.

Reading. At p = 3 and p = 7 the threshold is the same (≤ 3 lines), but at p = 3 nesting removes 1
of the 4 lines, while at p = 7 a feasible plane section must avoid 5 of the 8 lines: five
pairwise non-proportional dependencies all nowhere-zero on the section. p = 5 is the exception
(every planar set feasible). Heuristic count [argued]: on each line u and for each α, the
value ⟨γ_α, u⟩ must lie in a set of average size (p+3)/4 (it is {x ∈ S : rx + C_u·α ∈ S} shifted,
C_u = Φ(ru) − rΦ(u), and Σ over the classes of C_u·α gives (p+3)/2 per pair of classes), and
γ_α has p² values, so m lines are compatible for one α when p²((p+3)/(4p))^m ≳ 1:
m ≲ 3.8, 4.2, 4.4 at p = 7, 11, 13 and ≈ log_2 p for large p. It ignores the coupling across α
and fails at p = 5 (predicts 3.5; truth: all 6).

## 5. What this means for algorithms

**Lemma T (lines versus weight) [proved].** Let every nonzero dependency of the pool have weight
≥ w. A two-dependency piece X = supp⟨δ, δ′⟩ whose labels lie on m lines has |X| ≥ m·w/(m−1).
*Proof.* Each coordinate's label lies on one line; the codeword of the direction killing line j
has weight |X| − n_j ≥ w, where n_j counts labels on line j; Σ_j n_j = |X| over the m lines, so
|X| ≤ m(|X| − w). ∎ With |X| ≤ N (pool size) and near-equidistant pools (w ≈ (1−1/p)N), m-line
pieces need m/(m−1) ≤ p/(p−1), i.e. m ≥ p; feasible F_p^*-closed planar sets at p = 7, 11 have
m ≤ 3, 4. Thetas (m = 3) need w ≤ 2|X|/3.

**Barrier (b) [argued].** For random columns, the dependency code of an (l + r)-pool in the
quotient F_p^l is a uniform r-dimensional code; its labels are (conditioned on spanning) i.i.d.
uniform on F_p^r, so every point of F_p^r∖0 is a label with probability
≥ 1 − p^r(1 − p^{−r})^{l} → 1 when p^r ≤ l^{1−ε}. Then Corollary 2 and LG: no sub-piece gains
two dimensions at p = 7, 11, and the sparsest of the p^r − 1 dependencies has weight
(1−1/p)(l + r) − O(√(l r)). Summing over codimensions: (1−1/p)a²/2 − O(a^{3/2}√log a) for any
algorithm of the piece type that draws pools of l + O(log l) columns. Not proved: the algorithm
adapts its pools to the bank, so "every pool it may choose has full labels" is not a union-bound
statement; an algorithm that searched for a non-full pool would be solving a structured
low-weight problem. At p = 5 the same argument gives a²/4 − o(a²), which Theorem B′ attains.

**Sparse label sets (c) [argued].** With k ≳ log_p l, label sets are sparse and contain no full
lines, so LG is silent. First moment over (Φ, γ) for n i.i.d. labels in F_7^k, 16 slots (κ = 2,
d = 2): log E ≈ 2n log 4 + 16k log 7 + 16n log(4/7) = 31.1k − 6.2n, so random sparse sets are
2-feasible only if k ≳ 0.2n: then the piece has ≥ 1.25·rank columns and the γ-search is over
p^{Ω(n)} values. Heuristic only (labels of chosen pieces are not i.i.d.); consistent with
session A's p = 5, k = 3 data (random label sets infeasible from q ≈ 8).

**Half-line pieces exist in slightly larger pools (d) [argued, first moment].** Take a pool of N
random columns with dependency code of dimension r (quotient dimension l = N − r). A 2-dim subcode
has i.i.d. uniform labels in F_7^2; it gives a piece with 8 half-lines in one of the 224 feasible
patterns with probability ≈ 224·2^{−n} (each nonzero label must fall in the prescribed half of
its line; n ≈ (48/49)N nonzero labels), and there
are ≈ 7^{2(r−2)} subcodes. The expected count is ≥ 1 once 2r·log_2 7 ≳ N, i.e. r ≳ 0.178N,
N ≈ 1.22l, n ≈ 1.19l. Lemma T is not violated (m = 8 ≥ p; random codes of rate 0.18 have minimum
weight well below (6/7)N). Two Theorem C rounds cost ≈ 1.71l, so such pieces would cut the
constant by about 30% if they could be found. Locating one is a 2-dim-subcode search with a
sign-pattern (quadratic-character) constraint on every coordinate, ~2^{n} by brute force. I know no
poly-time method; it is the same flavor as the original problem. Heuristic only (subcodes are
dependent; ignores which pattern orbit is needed).

**What would beat Theorem C at p = 7 within the method.** A deterministic selection that, from
poly(l) columns, finds a piece of ≤ (2 − ε)(1−1/p)l columns with a 2-feasible label set: by LG it
must have a plane section with ≤ 3 label lines or a half-line structure (single P-class on a line).
Neither nesting (removes one line) nor sparsest-codeword selection produces this. By (d), the
half-line route exists (heuristically) but needs a search; §4 lists which half-line sets are
feasible.

## 6. Questions (1) and the p between a and a·polylog range

Not advanced. Q-loc is a statement about ALG-T's flags at large p; LG concerns the coefficient
set at small p and says nothing about fan-in. For the record, what is already known
(`2026-11-08-rees-sde-uniform-p.md` §4(a), Corollary L1, not re-derived here): o(a²) holds
whenever p/a → ∞, e.g. p = a·polylog gives J ≈ log_κ log a and O(a²/log log a); for
κ^7(7a+2) ≤ p = O(a) with p ≥ C_old(κ, 3) one gets J = 3, ⌊(a+2)²/4⌋ + 2a; below
p ≈ κ^7·7a (and at fixed p) only Theorem C (and Theorem B′ at p = 3, 5). So the open bounded-p
range is p ≤ ~κ^7·7a, where Lemma P of that note already empties Good sets of the E = 7 rounds.

## 7. Independent check (Claude API)

`claude/run_lg/` (claude-opus-5-5, effort high, 4651 input / 17223 output tokens, estimated
USD 0.36, stop end_turn). Brief: `claude/lg_prompt.md`, context `claude/lg_context.md`
(self-contained statements and proofs; no repository archive).

| item | agent verdict | disposition |
|---|---|---|
| Lemma K, V, 1 | ACCEPT (reparametrization must define Φ′ from y-values) | accepted; wording adopted |
| Theorem LG | ACCEPT WITH FIX: "distinct full lines", not distinct vectors | adopted |
| Corollary 1 | ACCEPT WITH FIX: nested → full transfer must be argued | adopted (Monotonicity, via Lemma N; the agent's argument is the same) |
| Theorem LG_R | ACCEPT WITH FIX: "span of R lines has dim R" unjustified | **real gap; repaired** as in §2 (checked by hand) |
| Corollary 2 | ACCEPT | — |
| multiplicities | no hidden one-column-per-label assumption | — |

No counterexample found; weakest step named: LG_R's span step (repaired).

## 8. Computations

All runs `nice -n 19`, at most two heavy processes of this pass at a time. Every SAT model is
verified by plain arithmetic over all α ∈ F_p^d∖0 and all labels of the P-closure.

| artifact | what | result |
|---|---|---|
| `bt.py` | Python backtracking decision procedure (Lemma R/Q/N encoding) | reproduces p = 3 full UNSAT / nested SAT, p = 5 full SAT, k = 1, d = 2 UNSAT (p = 5, 7), k = 1, d = 1 SAT (p = 7) |
| `btc.c`, `btc_run.py` | C port, same search (node counts identical to `bt.py`); later version adds the symmetry Φ(first label) ∈ {(0..0,1..1)} (coordinate permutations and P-scalings of Φ preserve feasibility, nondegeneracy and the Lemma R normalization) | same verdicts, ≈5× fewer nodes on UNSAT |
| `lines3.out`, `lines7.out` | unions of m full lines, one per PGL_2-orbit (`lines7.out` from the version without the symmetry) | §4 table |
| `lines11.out`, `lines13.out` | same at p = 11, 13 (node limit 2·10⁹) | §4 table |
| `lines7_lrat.out` | `gadget_cnf5.py` (CaDiCaL + fixed lrat-check) on the p = 7 sets with 3 and 4 lines | 3 lines SAT (cnf 43fe416c…, model verified); 4 lines, orbit 42 (`p7_L4a`) UNSAT, LRAT VERIFIED; orbit 28 (`p7_L4b`) UNSAT, LRAT VERIFIED (streamed) |
| `check_lemmas.out` | Lemma V and Lemma 1 on 7 SAT models (p = 5, 7, 11; k = 2, 3) | 0 violations: y_α = 0 on ker Δ_α, K_u = {α : ⟨Δ_α,u⟩ = 0} ∪ {0} a subspace of codim ≤ 1, global kernel 0 |
| `halflines7.out`, `halflines_post.py`, `halflines7_post.out` | P-closed planar sets at p = 7 with m ≤ 3 full lines plus half-lines (143 orbits, node limit 2·10⁸, no timeout); post-processing tallies S-functionals | §4 |
| `lines13.out` | p = 13, m ≤ 5 | all SAT, models verified |
| `claude/run_lg/` | Claude API adversarial check | §7 |

Also: F_7^3 with the 5 full lines e_1, e_2, e_3, e_1+e_2, e_1+e_2+e_3 is 2-feasible (in
`check_lemmas.out`), consistent with LG (the plane ⟨e_1, e_2⟩ meets it in 3 lines).

## 9. Claim gates, next question, next command

Gates that must stay false: "o(a²) or any constant-factor gain at fixed p ≥ 7"; "the piece method
is optimal" or "Theorem C is optimal for all algorithms" (only the argued barrier of §5 for one
method family on random banks); "every label set at p = 7 is 2-infeasible" (false: 3-line sets
are feasible); "every P-closed label set at p = 7 with ≥ 4 lines is infeasible" (false: half-line
sets with 8 lines are feasible); "p = 13 corollary certified"; "half-line pieces can be found in
poly time" or "exist" as a theorem ((d) is a first-moment heuristic); any novelty claim. (Note:
"m = 4 planar UNSAT at p = 7 certified" is now TRUE on both GL_2(F_7)-orbits via `lines7_lrat.out`.)

Next hard question. Is there a poly-time rule that, in pools of ≈ 1.2l columns at p = 7, finds a
2-dependency piece whose labels lie in one P-class per line (a feasible half-line pattern), or
a theta piece, with ≤ (2 − ε)(6/7)l columns? (d) says such pieces exist heuristically; Lemma T rules
out thetas in near-equidistant pools. A negative answer needs a reduction from a hard
structured-code problem; a positive one gives a constant-factor gain over Theorem C.

Next commands. (1) DONE (2026-11-11): `p7_L4b.txt` certified UNSAT by CaDiCaL (1140.8 s) + streamed
fixed `lrat-check` (12.51 GB LRAT proof, sha256 `cd15012ac621505c…`), recorded in `lines7_lrat.out`.
(2) Test (d) empirically at small l:
random F_7 pools of 1.2l columns, l ≤ 20, enumerate 2-dim subcodes, and count those with a
feasible half-line pattern. Acceptance: the count is within a factor of 10 of the first-moment
estimate, or the heuristic is withdrawn.

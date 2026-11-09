# Diagonal SDE worst case, pass B: a barrier for piece schemes, and no new mechanism

Date: 2026-11-07. Scope: κ ≥ 2 (κ = 2 and 3 tested), p ≡ 1 mod κ, P = (F_p^×)^κ,
Sq = P ∪ {0}, Q_ν = g^ν P. Bank λ_1..λ_M ∈ F_p^a; find nonzero x ∈ Sq^M with
Σ x_i λ_i = 0. Scripts and outputs are in `2026-11-07-rees-sde-subquad-B/`.
The flag/round J = log a absorption-load programme is not redone here.

Labels: [proved], [exact], [sampled], [argued], [conjecture], [literature].
"[literature]" also covers in-repo reports that have not been independently re-proved here.

## 0. Verdict

**Negative on the goal.** I did not find a Las Vegas poly(a, log p) algorithm that
solves every bank with M = o(a²) columns, at p ≥ poly(a) or at p ≥ 2^{poly(a)}. I also
found no mechanism that avoids the per-round "codim + 1 columns" cost. The best proved
worst-case count stays (a+1)(a+2)/2 [literature].

**What was obtained.**

1. A barrier (Theorem B) for a precise class of piece schemes. Here a piece scheme
   builds solutions as sums over disjoint pieces, and each piece's weights are a
   cell-wise affine family. On uniformly random banks at p ≥ 2^{Õ(M)}, any such scheme
   whose pieces each cost at most κ^E/2 needs

   M ≥ (a² − 4E²)/(2E) columns.

   So in poly time the scheme needs Ω(a²/log a) columns. Block-steered splitting gets
   G_{E−1}(a) = M_E(a) on the same banks [exact count, literature algorithm].
   - Within this class, a²/log a is the right target, not a².
   - The flag programme the other agent is running already sits at the optimum of the
     class, up to a factor of 1 + O(1/E).
   - An Ω(a²) barrier for this class is impossible on these hard instances.
2. The barrier's two gaps are pinned down:
   - For circuit pieces, *any* rule gaining ω dimensions solves random Legendre-pattern
     instances of size ω+1 (Proposition B′). The barrier for circuits is therefore
     conditional on that problem being hard (Assumption LP).
   - For multi-relation pieces, realizing targets is again an inhomogeneous SDE instance
     (self-similarity). The barrier there is only as strong as the cost model.
3. Each of directions 1, 2, 3 and 4 ends in a stated obstruction:
   - direction 1: Proposition D (dense-subspace dichotomy forces cubic thresholds);
   - direction 2: Lemma R;
   - direction 3: Proposition E (quadratic-form methods presuppose the quotient problem);
   - direction 4: Lemma G (no sparse dependencies mod U at large p).
4. One small structural tool, the sum lemma (Proposition C): two disjoint circuit flags
   realizing the same U turn "uniformly random targets" into "every target". This removes
   the planted non-steerability obstruction. It costs a factor 2 in columns, so it gives
   no count improvement.

## 1. The class of piece schemes

The definitions below follow the realized-subspace language of the 2026-11-05 reports
(two-relation report §1; `rem:sde-worst-case`, `rem:sde-block-steered` in
appendix-sde-side.tex).

**Run.** A run processes disjoint fresh column sets (pieces) S_1, S_2, .... After piece l
there is a realized subspace U_l ⊆ F_p^a. "Realized" means the scheme can produce, for a
target t ∈ U_l, a vector x supported on S_{≤l} with x ∈ Sq and Σ x_i λ_i = t. The target
is either uniformly random in U_l or specified, as stated in each result. The codimension
is q_l = a − dim U_l; on random banks the bank spans F_p^a. The gain of piece l is
ω_l = dim U_l − dim U_{l−1}.

**Finishing.** A run finishes in one of two ways:
- some column λ_top lies in U, and the scheme realizes −yλ_top for some y ∈ P;
- a stop piece gives Σ_{S} x_i λ_i ∈ U together with a realizable completion.

**Piece rule (table model).** Fix piece S, quotient V = F_p^a / U_{l−1}, the images λ̄_i,
the map L : F_p^S → V, x ↦ Σ x_i λ̄_i, and a target subspace W ⊆ L(F_p^S) of dimension ω.
On input w ∈ W the rule:
- evaluates F pairwise non-proportional cell forms c_1..c_F (linear forms on W), reads the
  cell σ (the class pattern of the c_j(w) in {0} ∪ Z/κ), so κ^F cells up to zeros;
- in cell σ, repeatedly draws θ uniform in F_p^d, sets x = A_σ w + B_σ θ + b_σ with
  L(x) = w identically, and accepts if x ∈ Sq^S.

**Cost.** cost(rule) := κ^F · min_σ N_σ, where N_σ is the expected number of draws in a
successful cell σ. This is the table's size times the cheapest cell's sampling cost. It
is the price of preparing and validating one affine map per cell.

**Class assumptions for Theorem B.**
- (A1) Single-stage sampling per piece, as above.
- (A2) Piece selection may depend on anything, including all columns. But U_l is
  determined by the columns of S_{≤l}, U_{l−1} and a discrete transcript of at most B bits.
  B counts combinatorial choices (pieces, cells, branches) and does not include field
  samples θ; B ≤ poly(M) is allowed.
- (A3) Finishing happens either at codim 0 with a top column, or freely once codim ≤ E.
  The free option is generous to the scheme.
- (A4) Stop pieces are chosen coset-obliviously. A candidate's dependency classes behave
  like independent uniform classes, so a stop piece at codim q costs at least κ^q/2.
- (A5) Every piece costs at most κ^E/2.

Known schemes in this class:
- the triangular solver: one circuit per round, F = 1, E_θ = 0, ω = 1 [literature,
  main.tex lines 682–705];
- block-steered splitting: a circuit split into J blocks, F = 0, E_θ = J, ω = J − 1
  [literature, two-relation report];
- the reserved-basis procedure, which is a sequence of circuit pieces [literature,
  worst-case report].

## 2. Lemmas

**Lemma N (independent pieces gain nothing) [proved].** Suppose the λ̄_i, i ∈ S, are
linearly independent in V. Then x(w) is the unique preimage of w, and x(gw) = g·x(w) for
g ∈ F_p^×. If x(w) ≠ 0, the set of g with g·x(w) ∈ Sq^S lies in one coset of P, so it has
density at most 1/κ. A rule cannot reach a 1/κ + Ω(1) fraction of any line of targets,
and a productive piece needs a dependency mod U_{l−1}.

**Lemma G (no short dependencies mod U at large p) [proved].** Take a bank of M columns
drawn uniformly from F_p^a, and a scheme satisfying (A2). Suppose

p ≥ 2^{(M+1)log₂(M+1) + 2M + B}.

Then with probability at least 1 − 2^{−M} over the bank, the following holds for every run
and every l: every fresh set T (disjoint from S_{≤l}) with |T| ≤ q_l is linearly
independent mod U_l.

*Proof.* Fix a history: an ordered sequence of disjoint pieces and a B-bit transcript.
There are at most (M+1)^{M+1}·2^B histories. Each U_l is then a function of the columns
in S_{≤l}, which are independent of the columns of T. Fix T as well (at most 2^M choices).
Conditioned on U_l, the images of T in F_p^a/U_l ≅ F_p^{q_l} are uniform and independent.
They are dependent with probability at most Σ_{j<|T|} p^{j−q_l} ≤ |T|/p (using
|T| ≤ q_l). A union bound gives failure at most (M+1)^{M+1}·2^{B+M}·M/p ≤ 2^{−M}. ∎

[sampled] `lemma_g.py` checks this on brt.forward runs, with M = arity + 20. It tests
random q-subsets, and every fresh subset of size ≤ 3, for dependence mod each intermediate
U:
- p = 2^31 − 1: 0/720 and 0/24933 (κ=2, a=10); 0/480 and 0/17466 (κ=2, a=14);
  0/480 and 0/16200 (κ=3, a=10);
- p = 13: 48/720 and 33/25566;
- p = 29: 20/660 and 7/31410;
- p = 31 (κ = 3): 13/480 and 7/17466.

So short dependencies mod U do exist at small p, and the large-p hypothesis is doing real
work. This small-p effect is also where the (1 − 1/p) factor of KOW Lemma 3.6 comes from;
see §6, direction 4.

**Lemma R (rank lemma) [proved in the table model].** Fix a cell σ. Call a coordinate x_i
*undetermined* if its class is not a function of the cell (as w ranges over the cell and θ
over F_p^d). Let E_u be the number of proportionality classes of undetermined coordinates;
it includes the E_θ classes of θ-dependent coordinates. Assume p ≥ 16E_u²κ^{2E_u}. Then:

1. ω + rank B_σ = dim X_σ ≤ F + E_u, where X_σ is the affine span of the outputs. Hence
   ω ≤ F + E_u − [E_θ ≥ 1].
2. The success probability per draw, for w uniform in the cell, is at most
   κ^{−E_u} + E_u p^{−1/2} + 2E_u²/p ≤ 2κ^{−E_u}. So cost ≥ κ^{F+E_u}/2.
3. Therefore **ω ≤ log_κ(2·cost)**.

*Proof.*
- (1) The map (w, θ) ↦ x is affine, and x determines w = L(x). So dim X_σ = ω + rank B_σ.
- dim X_σ is at most the number of proportionality classes of the non-constant coordinate
  functions on X_σ, because proportional coordinates span one dimension of the dual.
- A non-constant determined coordinate x_i = a_i·w + b_i must be a scalar multiple of some
  cell form c_j, with b_i = 0. Otherwise its linear part, or its shift, is not proportional
  to any cell form, and by Lidl–Niederreiter 5.41 its class is equidistributed given the
  cell. Then it would not be determined. This leaves at most F determined classes, and E_u
  undetermined ones.
- (2) The E_u undetermined class representatives are pairwise non-proportional affine
  forms on the cell's parameter space. By Weil (Lidl–Niederreiter 5.41, applied to a
  generic line through the parameter space), their joint class pattern is equidistributed,
  with error E_u p^{−1/2}. Degenerate w, where two representatives become proportional or
  vanish, have measure at most 2E_u²/p.
- (3) If E_θ = 0, then ω ≤ F + E_u ≤ log_κ(2 cost). If E_θ ≥ 1, then
  ω ≤ F + E_u − 1 ≤ log_κ(2 cost) − 1. ∎

The bound is attained:
- block-steered: F = 0, E_θ = J, ω = J − 1, cost about κ^J;
- triangular: F = 1, ω = 1.

Making "most coordinates constant or proportional" (direction 2) gains nothing. Constant
coordinates add no dimensions, and each proportional coordinate is a cell form charged a
factor κ in the table.

## 3. Theorem B (barrier for piece schemes)

**Theorem B [proved, given (A1)–(A5)].** Let the bank be uniformly random in (F_p^a)^M with

p ≥ max(2^{(M+1)log₂(M+1)+2M+B}, 16E²κ^{2E}).

With probability at least 1 − 2^{−M}, every piece scheme in the class that finishes uses

M ≥ LB_E(a) := Σ_{j ≥ 0, a − jE > E} (a − jE + 1) ≥ (a² − 4E²)/(2E) columns.

With poly(a) cost per piece, E = O(log a), so M = Ω(a²/log a).

*Proof.*
- By (A5) and Lemma R, every piece gains ω_l ≤ E.
- By Lemma G and Lemma N, a piece starting at codim q_{l−1} that gains anything has at
  least q_{l−1} + 1 columns.
- By (A4), a stop piece at codim q > E costs at least κ^q/2 > κ^E/2, so (A5) excludes it.
- By (A3), the run must drive the codim from a down to at most E.
- Termwise, q_l ≥ a − lE. So the column total over productive pieces starting at codim > E
  is at least LB_E(a).
- Closed form: the number of such pieces is k ≥ a/E − 1, and
  ka − Ek(k−1)/2 + k ≥ a²/(2E) − E for those k. ∎

[exact] `counts.py` / `counts_lb.out`: LB_E(a) ≥ (a² − 4E²)/(2E) holds for every
1 ≤ E < 40 and 2E ≤ a < 600 (0 violations). The bound is tight against block-steered:
G_E(a) (= M_{E+1}(a)) / LB_E(a) is 1.004 at (a, E) = (64, 3) and 1.000 at (1024, 10).

[exact] `counts.out`, comparison at a = 64:

| E | G_E (gain ≤ E, +1 finish) | G_{E−1} = M_E (block-steered) | D_E(a) + a (reserved basis, general position) | triangular |
|---|---|---|---|---|
| 3 | 738 | 1089 | 1153 | 2145 |
| 4 | 561 | 738 | 802 | 2145 |

**What Theorem B does not say.**
- It is a lower bound on random banks, not an algorithm. On those same banks block-steered
  already achieves O(a²/log a) [literature]. So the class cannot carry an Ω(a²) worst-case
  barrier on these instances.
- Any worst-case Ω(a²) lower bound would need adversarial banks where block-steered
  stalls. On the degenerate families tested (§5), the scheme instead solves directly.
- It says nothing about p = poly(a). The prime range is p ≥ 2^{Õ(a²)}, since
  M = Θ(a²/log a) appears in the exponent.

**Staged sampling inside a piece [argued].** A rule that first samples on a subset Z ⊂ S
and then on S ∖ Z needs a relation mod U that vanishes on Z. In general position (Lemma G)
that requires |S ∖ Z| ≥ q + 1. So the early stages control at most r − d_r coordinates
(r relations, d_r of them in the late stage), and the stage-wise table charges add up to
the one-stage bound. I have not written this out as a proof for adaptive multi-stage
rules.

## 4. The two gaps: circuit pieces under any rule, and multi-relation pieces

**Proposition B′ (circuit pieces reduce to Legendre patterns) [proved].** Let S be a
circuit mod U (|S| = q + 1, dependency δ with all δ_i ≠ 0, by Lemma G). The fibre of w is
the line x = x_0(w) + sδ. Write γ_i(w) = x_0(w)_i/δ_i, which is affine in w. Then
x ∈ Sq^S means

s + γ_i(w) ∈ δ_i^{−1}·Sq for all i,

which is a Legendre-pattern instance "find s with s + γ_i ∈ Q_{c_i}". Realizing an
ω-dimensional W forces at least ω + 1 distinct offset forms γ_i, since
dim X = ω + 1 ≤ #classes. With exactly ω + 1 forms and w uniform in W, the offset vector
modulo the diagonal is uniform in F_p^{ω+1}/F_p·1. Hence any rule, table-based or not,
that realizes uniform targets in W solves uniformly random LP instances of size m = ω + 1,
with the class pattern fixed by δ.

**Assumption LP [conjecture].** Random LP instances of size m need time κ^{Ω(m)} at
p ≥ κ^{2m}·poly(m).
- Solutions exist by Weil once p ≫ m²κ^{2m} [proved].
- The best method I know costs κ^{m−2} for κ = 2: parametrize the conic of two
  constraints, then pay a factor 2 per further constraint (a genus-1 curve at m = 3).
  That is two constraints for free, which matches Theorem 1 of the subquadratic report
  (a circuit's realizable set contains no 2-plane) [argued].
- LP is in the family of Legendre / power-residue PRF assumptions, but it is not
  literally one of them: the solver sees the offsets in the clear, rather than an oracle.

Under LP, circuit pieces gain O(log T) in time T, under any rule.

**Self-similarity [proved, by definition].** For a piece with r ≥ 2 relations mod U,
realizing w means finding x ∈ Sq^S with Σ x_i λ̄_i = w. This is an inhomogeneous SDE
instance with |S| columns in the (|S| − r)-dimensional space L(F_p^S). So bounding the
gain of *arbitrary* rules on multi-relation pieces is exactly as hard as the problem
itself. Only the table model (Lemma R) bounds them. Proposition A of the two-relation
report (no class collapse for multi-relation pieces in general position) [literature] is
consistent with Lemma R but does not replace it.

**Boundary example: θ-free covering rules (outside the table model).** A piece S of n
columns in V = F_p^q covers w if some basis B ⊆ S writes w with all coefficients in P. A
covering rule queries the classes of the minors det(λ_T, w) on the fly, rather than
building a κ^F table.
- [exact] For q = 2, n = 5, κ = 2 (`cone_cover.py` part 1, 40 random banks per prime):
  - For p ≡ 1 mod 4 and p ∈ {37, 41, 53, 101}, the piece covers every w off the column
    lines exactly when the graph {ij : χ(det(λ_i, λ_j)) = +1} is not a split graph.
  - For p ≡ 3 mod 4 and p ∈ {43, 103}, coverage is always partial.
  - At p ≤ 29 some split banks are also full.
  - Five columns for two dimensions is no better than block-steered.
- [exact] Small q > 2, part 2. Points on the spans of q − 1 columns are counted as
  uncovered.
  - q = 3: full coverage appears first at n = 8 (2/4 banks at p = 13 and 17; 1/4 at p = 29).
  - q = 4, p = 13: no full coverage up to n = 10. The worst uncovered fraction is 0.0008
    at n = 10.
- [sampled] p = 10^9 + 7, part 3: the fraction of random bases covering a random target
  is 0.25, 0.058, 0.013, 0.0047 and 0.0020 for q = 2, 4, 6, 8, 10 (n = 2q, 3000 trials
  each). This is about 2^{−q}.
- So the honest cost of finding a covering basis by trial is about κ^q, and covering
  rules respect ω ≤ log_κ(cost) in practice. A faster covering-basis search would be an LP
  solver (Proposition B′), so it gives no escape.

## 5. Algorithmic tool: uniform targets and the sum lemma

**Proposition C [proved].**
- (i) In a flag of circuit rounds (brt.backward), a uniformly random target in U needs no
  steering. The residual after each backward round is again uniform in the lower realized
  space. Failure is at most Σ_l C(J_l, 2)/p plus Good-set misses.
- (ii) Sum lemma. Suppose two flags on disjoint column sets both realize uniform targets
  in the same U. Then every specific t ∈ U is realizable: draw u_1 uniform, set
  u_2 = t − u_1 (also uniform), realize each, and add. The failure probability is at most
  twice the single-flag failure.

This removes the planted non-steerability obstruction (the specific target −y·λ_top) at
the price of a second flag. It is a tool and not a count improvement: 2× flag + 1 is
weaker than a reserved basis (D_J(r) + r) as a count.

[sampled] `uniform_targets.py` / `.out`: planted brt_tests.planted_top instances, "first"
split, 6 instances × 10 targets per row.

| row (p, κ, a, E) | specific target −y·top | uniform targets | two-flag split for the specific target |
|---|---|---|---|
| 1009, 2, 6, 3 | 0/60 | 60/60 | 40/40 |
| 1009, 2, 8, 3 | 0/60 | 60/60 | 60/60 |
| 1009, 3, 6, 3 | 0/60 | 60/60 | 60/60 |
| 10007, 2, 10, 4 | 0/60 | 60/60 | 40/40 |

The two-flag denominators count the instances whose second random flag reached F_p^a.

Adversarial families (repeated3, codim2, nested, proportional), at p = 1009 (κ = 2, a = 6),
p = 10007 (κ = 2, a = 8) and p = 1009 (κ = 3, a = 6):
- Every run ends in "stop": a monochromatic round was found and the bank was solved
  directly.
- The one exception is codim2 at p = 10007, κ = 2, a = 8 (rank 6). There the flag reaches
  the span and uniform targets succeed 20/20.

These are finite checks at a ≤ 10 and prove nothing about scaling.

## 6. The five directions

1. **Dense-subspace dichotomy: Proposition D [proved].**
   - The reduction "recurse into a dense W, otherwise make composites in general position
     and run rem:sde-worst-case(b)" forces a cubic threshold.
   - A composite Σ_{i∈G} x_i λ_i, with x ∈ Sq and disjoint groups G, is a valid column,
     because Sq·Sq ⊆ Sq.
   - Example bank: a hyperplane H with F(r−1) − 1 columns in general position inside H
     (just below the recursion threshold), plus Δ(r) + 1 columns outside H.
   - At most r − 1 composites in general position lie in H, and every other composite uses
     an outside column. So at most Δ(r) + r composites can be in general position, while
     D_J(r) + r ≈ r²/(2(J−1)) are needed.
   - So F(r) ≥ F(r−1) + D_J(r), which gives F(a) ≈ a³/(6(J−1)).
   - Randomizing coordinates or composites does not help: the bound is a deterministic
     matroid-union (Rado–Hall) count.
   - Subsampling does not help either: it only removes columns.
2. **Large p.** Lemma R: with large p and Weil, each tested coset condition (a cell form,
   or an undetermined class) buys at most one dimension and costs a factor κ. O(log a)
   conditions buy O(log a) dimensions, which is the block-steered rate. Proposition A is
   the multi-relation instance of this.
3. **Quadratic forms (κ = 2): Proposition E [proved, plus literature].** This uses
   Φ(v + y) = Φ(v) + 2B(v, y) + Φ(y) for the vector form Φ = (Φ_1..Φ_a).
   - A totally isotropic T mod U already contains solutions mod U. So "linearize on an
     isotropic subspace" presupposes solving the quotient problem.
   - If the restriction is to disjoint supports, the pieces are exactly composites, and a
     recursive totally isotropic build costs 2^{a+1} − 1 variables.
   - If supports overlap, the diagonal structure is lost, and we are in general MQ, where
     CHMT gives n ≥ m(m+1)/2 [literature].
   - Hyperbolic pairs (two columns with x_1λ_1 + x_2λ_2 = 0) are monochromatic 2-circuits,
     which are absent on random banks at large p by Lemma G.
   - CHMT, Thomae–Wolf and KPG stop at quadratic for two reasons: each new orthogonality
     vector costs m linear conditions, and the characteristic-2 Frobenius linearization
     fails in odd characteristic [literature].
4. **Sparse dependencies (KOW Lemma 3.6).**
   - Lemma G: on random banks at large p, every dependency mod U_l among fresh columns has
     support at least q_l + 1. So no sparsity profile beats Σ(q_l + 1), which is the
     per-round cost.
   - KOW's saving, the factor (1 − 1/p), is a small-p phenomenon. The sampled small-p
     dependencies in `lemma_g.out` are its source.
5. **Barrier.** Theorem B is unconditional in the table model. Proposition B′ is
   conditional on LP, and covers circuits for all rules. The barrier is Ω(a²/log a) and is
   tight, so Ω(a²) is unattainable for this class.

## 7. Weakest step

The cost model in Lemma R and Theorem B charges κ per queried cell form, which is the
table-preparation charge (A1). Rules that compute cells on the fly escape this charge:
- for circuit pieces, they are covered only conditionally, through LP;
- for multi-relation pieces, they are covered only by self-similarity, which is circular.

The covering rules of §4 are the explicit boundary case. They pay about κ^q in practice
[sampled], but no theorem forces that.

Secondary weak points:
- (A4) is an independence assumption on stop pieces.
- The staged-sampling remark is [argued].
- The prime range p ≥ 2^{Õ(a²)} is far above poly(a).

## 8. Claim gates that must stay false

- "o(a²) worst-case diagonal SDE algorithm" — not obtained.
- "Ω(a²) barrier" — false for the class (block-steered gives O(a²/log a) on its hard
  instances).
- "Theorem B covers all algorithms" — only (A1)–(A5).
- "Assumption LP proved" — conjecture.
- "Sum lemma improves the worst-case count" — it does not.
- "a²/log a proved for arbitrary banks" — not proved here; that is the flag programme's
  open question.
- No finite computation in §§2–5 is a scaling claim.

## 9. Next hard question and next command

**Question.** Remove the table cost model: prove ω ≤ O(log T) for *every* time-T rule on
a multi-relation piece in general position, or exhibit an on-the-fly rule that gains
ω(log T).

The most concrete sub-question is a covering-basis search for q-dimensional quotients in
time poly(q) at success 1/poly. By Proposition B′, that would also refute LP for circuits.

**Next command.**
`/opt/anaconda3/bin/python research/audits/reviews/2026-11-07-rees-sde-subquad-B/cone_cover.py 3`,
extended with a smarter basis search (greedy exchange along the minors' classes) that
replaces the random-basis trial.
- Expected artifact: `cone_cover_part4.out`, the success fraction against q.
- Acceptance test: a fraction that stays at least 1/poly(q) for q up to 20 at p = 10^9 + 7
  would contradict the [sampled] 2^{−q} trend and reopen direction 2. A 2^{−Θ(q)} decay
  confirms the barrier picture.

## 10. Files (all in `2026-11-07-rees-sde-subquad-B/`)

- `subB.py`: helpers.
  - Imports `common` and `brt` / `brt_tests` read-only from `../2026-11-05-rees-sde-two-relation`.
  - `backward_target`: realizes an arbitrary residual τ.
  - `forward_flag`, `value`.
  - `BigF`: power classes at large p, since common.F enumerates F_p.
- `counts.py`: G_E, D_J, LB_E. Outputs: `counts.out` (table), `counts_lb.out` (Theorem B
  bound check).
- `lemma_g.py` / `lemma_g.out`: Lemma G sampling.
- `uniform_targets.py` / `uniform_targets.out`: Proposition C, planted and degenerate
  banks.
- `cone_cover.py`:
  - `cone_cover_part1.out`: q = 2 split-graph criterion; `cone_cover.out` is an identical
    earlier run of part 1.
  - `cone_cover_part23.out`: parts 2 and 3.

Read only, and not modified:
- appendix-sde-side.tex and main.tex;
- the 2026-11-05 subquadratic, two-relation, worst-case and q1 reports;
- brt.py, brt_tests.py, common.py.

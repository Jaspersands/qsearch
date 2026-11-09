# Nested-dependency gadgets beyond p = 3: two dimensions per piece at p = 5 (κ = 2, worst case n²/4 + O(n^{3/2})), exact obstruction at p = 7, 11, 13; sparse one-dimensional rounds give (1−1/p) a²/2 at every p

AI-only pass, 8 November 2026, one Claude Code session; not human-reviewed; no novelty or
priority claim (literature only through `2026-11-07-rees-sde-subquad-lit.md`, `…-lit2.md`,
`…-p3-nest-lit.md`: KOW = arXiv 2510.07515, KOMSW = arXiv 2609.40321). Inputs:
`2026-11-08-rees-sde-p3-nest.md` (+ referee, break), `2026-11-08-rees-sde-p3.md`,
`2026-11-08-rees-sde-uniform-p.md`, `docs/papers/rees-hsp/main.tex` prop:triangular-sde
(lines 682–698; E_2(2) = E_2(3) = ∅ at line 674). Scripts and outputs: `2026-11-08-rees-sde-fq-nest/`,
interpreter `/opt/anaconda3/bin/python -B` (pycosat 0.6.6, z3 4.15.3 as a second engine). Only this
file and that folder were written; no git, no network, `make_numbers.py` not run.

Labels: **[proved]** full proof here; **[exact]** complete finite computation, script named;
**[sampled]** exact arithmetic on random or constructed instances; **[argued]**; **[conjecture]**;
**[literature]**. Every statement says worst or average case and names p, κ.

Problem (a). λ_1..λ_M ∈ F_p^a arbitrary (worst case); find nonzero x ∈ S^M with Σ x_i λ_i = 0,
S = P ∪ {0}, P = (F_p^*)^κ. Baseline: the paper's triangular scheme, (a+1)(a+2)/2 columns, one
dimension per round [literature/paper]. Problem (b): S = {−⌊q/4⌋..⌊q/4⌋} (KOW Thm 3.7:
((1−q^{-1})/2) n² + O(n log n) [literature]). Problem (c): S = {0,1} (KOMSW Thm 1.11:
q^{q²}(n+1)^{q−1} [literature]).

## 0. Verdict

1. **p = 5, κ = 2 (S = {0, ±1}): YES, two dimensions per piece, worst case n²/4 + O(n^{3/2})
   [proved, with two exact finite inputs].** Theorem B (§3): the deterministic algorithm WNEST₅
   solves every instance with m ≥ guarantee(n) ≤ n²/4 + 0.754 (n+2)^{3/2} + 5.75 n + √(2n) + 13
   columns (exact recursion in `closed_form_p5.out`: 0.372 n² at n = 60, 0.336 at 100, 0.271 at
   1000, 0.262 at 3000; the sparse one-dimensional recursion is 0.44, 0.43, 0.404, 0.401 n²).
   Two facts about F_5 carry it: **(i)** [exact, `enum_labels_p5.out`] every label set
   L′ ⊆ F_5²∖0 that spans F_5² and has |L′| ≥ 4 admits a two-dimensional S-realization (or a
   direct S-witness) — in particular *any* two independent dependencies, nested or not, with all
   24 joint patterns present (`p5_all_solution.out`); **(ii)** [proved, Lemma J] a support X with
   dim D(X) ≥ 3 and ≥ 4 D(X)-classes always carries a pair (δ, δ′) with ≥ 4 joint labels. The
   F_3 machinery (series-class peeling, second Pless moment, conditional expectations) transfers
   with the constant 1−1/p in place of 2/3. Every witness in every run was re-summed over the
   original columns (`wnest_p5.out`, `adversarial_p5.out`: 11 structured families and hill climbs,
   4284 distinct label sets met, none infeasible). Since S = {0,±1} = {−⌊5/4⌋..⌊5/4⌋}, this is also
   question (b) at q = 5: nesting halves KOW's constant 0.4 to 0.25 there.
2. **p = 7, 11, 13 with κ = 2, and p = 7, 13 with κ = 3: NO two-dimensional gadget from two
   dependencies [exact].** With all nested patterns F_p^* × F_p present (the worst case the
   adversary can realize with one column per pattern), no realization of a 2-dimensional
   subgroup with S-weights exists: p = 7 both for the nested set and for all 48 patterns
   (`cases7.out`, `cases7_all.out`), κ = 3 at p = 7 (`big_7_k3_nest.out`), [p = 11, 13: see §2 —
   filled from `cases11.out`, `cases13.out`, `cases13k3.out`]. One dependency never gives two
   dimensions at any of these (p, κ) (`table_small.out`). The decision procedure is a CNF with
   two exact reductions (Lemma R: γ_{λα} = λγ_α for λ ∈ P; Lemma Q: labels up to P-scaling) and an
   exact case split on the two unit-direction functionals (Lemma U; covering verified in
   `cases_cover.out`). Interpretation [argued]: at p = 5 the coefficient set is an interval
   {−1,0,1} and −1 ∈ P, which is what the F_3 gadget also used (−1 = 1 + 1); for p ≥ 7 the
   squares are not an interval and the realizers of a full 2-dimensional subgroup cannot be kept
   inside S. This is an obstruction for the piece framework with k = 2 dependencies, not for all
   algorithms; k = 3 at p = 7 is reported in §2 if finished.
3. **Every odd p, κ ∈ {2, 3}: a proved constant below 1/2 by one-dimensional sparse rounds
   [proved].** Theorem C (§4): KOW's sparse-dependency selection (support ≤ (1−1/p)(l+r)/(1−p^{−r})
   from l + r columns, r = ⌈log_p(l+1)⌉) composed with the paper's contraction weights realizes a
   full line per round, so m ≥ (1−1/p) a²/2 + O(a log a) suffices deterministically (given the
   contraction, which exists for κ = 2, 3 at every p). Checked at (p,κ) ∈ {(5,2),(7,2),(11,2),
   (13,2),(7,3),(13,3)}, a ≤ 40, four families, every witness verified (`sparse_tri.out`); the
   O(a log a) term makes the gain over (a+1)(a+2)/2 small below a ≈ 40.
4. **(b) KOW small coefficients.** q = 5: yes (item 1). q = 7, 11: no nested two-dimensional
   gadget [exact, `big_7_int_nest.out`, `big_11_int_nest.out`]; q = 13: §2. The one-dimensional
   KOW round is reproduced as a feasibility fact at q = 5, 7, 11, 13 [exact, `table_small.out`].
5. **(c) 0/1 subset sum at q = 5, 7.** Nothing of lower degree from this framework [proved,
   Lemma Z]: a 0/1 realization of even one dimension forces the label set into four parallel
   hyperplanes {⟨γ, ℓ⟩ ∈ {−2,−1,0,1}}, which no pattern set that support nesting or weight
   selection can force satisfies; k = 1, 2, 3 nested and all-pattern sets are UNSAT at p = 5, 7
   [exact]. KOMSW's exponent q − 1 is untouched.
6. **Weakest step.** Theorem B rests on two finite exact inputs (the 36 096-orbit classification
   and the per-instance CNF, both re-verified by brute force on every model) and on Lemma J; its
   lower-order term is O(n^{3/2}) as at p = 3. The negative results are exact CNF verdicts; their
   only non-mechanical part is Lemma U (the case split), proved in §1 and checked by enumeration.

## 1. Setup and exact reductions

Columns live in V = F_p^q (the original space modulo the realized subgroup U). For X ⊆ [M],
D(X) = {c ∈ F_p^X : Σ c_i v_i = 0}, k = dim D(X), and a basis matrix B (k × |X|) has columns
ℓ_i ∈ F_p^k, the **labels**; L(X) = {ℓ_i} ⊆ F_p^k ∖ 0 spans F_p^k, and D(X) = {(⟨μ, ℓ_i⟩)_i : μ ∈ F_p^k}.
R(X) = {Σ y_i v_i : y ∈ S^X}. X **gains** d if R(X) contains a d-dimensional subgroup H; a
**witness** is a nonzero y ∈ S^X with Σ y_i v_i = 0.

**Lemma 1 (recursion) [proved; the p = 3 note's Lemma 1 with S in place of {0,1}].** If X gains H
and T ⊆ [M]∖X carries y_T ∈ S^T∖0 with Σ_T y_i v_i ∈ H, then some y_X ∈ S^X has Σ_X y_i v_i =
−Σ_T y_i v_i, and (y_T, y_X) is a nonzero S-solution. Iterating over a chain of realized subgroups
until codimension 0 and taking any remaining column (weight 1 ∈ S) solves the instance. ∎

**Lemma 2 (label formulation) [proved].** Fix X with labels L. A family (y_α)_{α ∈ F_p^d} ⊆ S^X with
Σ_i y_α(i) v_i = α_1 h_1 + … + α_d h_d for some h_1..h_d ∈ V exists iff there are Φ_i ∈ S^d (i ∈ X)
and γ_α ∈ F_p^k with y_α(i) = ⟨α, Φ_i⟩ + ⟨γ_α, ℓ_i⟩ ∈ S for all α, i. Hence: (A) if a function
Φ: L → S^d and vectors γ_α satisfy ⟨α, Φ(ℓ)⟩ + ⟨γ_α, ℓ⟩ ∈ S for all α ≠ 0, ℓ ∈ L (**feasible**) and
for every projective direction [α] some λα has a realizer that is nonzero on L (**weakly
nondegenerate**), then X gains 2 or yields a witness; (B) if X has one column per label and no
such (Φ, γ) exists, then R(X) contains no d-dimensional subgroup and 0 has no nonzero S-realizer.
*Proof.* y_α − Σ_j α_j y_{e_j} ∈ D(X) is exactly y_α(i) = ⟨α, Φ_i⟩ + ⟨γ_α, ℓ_i⟩ with Φ_i := (y_{e_j}(i))_j.
(A): put Φ_i = Φ(ℓ_i), h_j = Σ_i Φ_j(ℓ_i) v_i; then Σ_i y_α(i) v_i = α·h because Σ_i ⟨γ, ℓ_i⟩ v_i = 0.
If h_1..h_d are independent, X gains d; else α·h = 0 for some α ≠ 0, and for all λ, λα·h = 0, so the
nonzero realizer y_{λα} of the direction is a witness. (B): a d-dimensional H ⊆ R(X) gives
realizers with all y_α ≠ 0 for α ≠ 0 (strong nondegeneracy), hence a feasible nondegenerate (Φ, γ)
on the labels (one column per label); a nonzero S-realizer y of 0 gives one with Φ_1 = y,
Φ_j = 0 (j ≥ 2), γ_α := (1−α_1)μ where y = (⟨μ, ℓ_i⟩)_i, which is feasible and weakly nondegenerate. ∎
The decision problem "is L d-feasible with weak nondegeneracy" is finite; `gadget_cnf4.py` decides
it (one-hot CNF, every model re-verified over all α and all labels by `gadget_cnf.verify`).

**Lemma R (coset reduction) [proved].** If (Φ, γ) is feasible and weakly nondegenerate, so is
(Φ, γ′) with γ′_{λα} := λγ_α for λ ∈ P and α in a fixed set of representatives of F_p^d∖0 modulo P.
*Proof.* y′_{λα} = λ(⟨α, Φ⟩ + ⟨γ_α, ·⟩) = λ y_α ∈ λS = S, nonzero iff y_α is. ∎ So the free data are
γ_α for α in a set of (p^d − 1)/|P| representatives: for d = 2 and κ = 2, (p+1) directions × 2
cosets minus the two unit directions at coset 0 (where γ = 0 because Φ_j := y_{e_j}).

**Lemma Q (label scaling) [proved].** For λ ∈ P the constraints at λℓ with Φ(λℓ) := λΦ(ℓ) are those
at ℓ; a solution on L extends to the P-closure of L with the same γ; weak nondegeneracy is
unchanged. ∎ So labels are taken up to P-scaling.

**Lemma U (unit functionals; case split) [proved].** Let S = P ∪ {0}, κ ≥ 2, L ⊇ F_p^*×F_p (nested),
d = k = 2, r ∉ P. In every weakly nondegenerate solution γ_{(r,0)} ≠ 0 and γ_{(0,r)} ≠ 0.
*Proof.* If γ_{(r,0)} = 0 then rΦ_1(ℓ) ∈ S ∩ rS = {0}, so Φ_1 ≡ 0, and the realizers of direction
[(1,0)] are the linear functionals ⟨γ_{(λ,0)}, ℓ⟩, which take the value set S only if they vanish
on F_p^*×F_p: a functional (g, g′) with g′ ≠ 0 takes every value on a line a = const, and (g, 0)
takes all of F_p^* on it; so all realizers vanish — contradiction. Same for Φ_2. ∎ The maps
σ(a,b) = (λa, μb + νa) (λ, μ ∈ F_p^*, ν ∈ F_p) preserve the nested label set and send solutions to
solutions (Φ∘σ, σ^Tγ); together with the swap of the two unit directions they act on the pair of
functionals (w_1, w_2) = (γ_{(r,0)}/r, γ_{(0,r)}/r), and every pair of nonzero functionals is
equivalent to one of (a, b), (a, g·a), (b, g·b), (b, a + g·b), g ∈ F_p^* — 3p − 2 cases
[proved by orbit computation for p = 7, 11, 13: `cases_cover.out`, 0 missing pairs]. Each case is
a CNF with those two slots fixed.

## 2. Feasibility table [exact]

d = dimension realized, k = dependencies, "nest" = labels F_p^*×F_p^{k−1} (δ¹ of full support,
the others inside it), "all" = F_p^k∖0. SAT = feasible with weak nondegeneracy (a gadget exists);
UNSAT = none exists. Scripts: `gadget_cnf4.py` (reduced CNF, `table_small.out`, `big_*.out`),
case splits (`cases*.out`), p = 3 sanity in `table_old_encoding.out` (KOW SAT, NEST SAT, all-8 UNSAT).

| S | k=1, d=1 | k=1, d=2 | k=2, d=2 nest | k=2, d=2 all |
|---|---|---|---|---|
| κ=2, p=5 ({0,±1}) | SAT | UNSAT | **SAT** | **SAT** (24 patterns) |
| κ=2, p=7 ({0,1,2,4}) | SAT | UNSAT | UNSAT (19 cases, ≤ 4.5 s each; also unsplit, CaDiCaL 1436 s, 12.3 GB LRAT proof verified) | UNSAT (19 cases) |
| κ=2, p=11 | SAT | UNSAT | UNSAT (31 Lemma U cases × 121 values of γ_(1,1); 3751 sub-cases, CaDiCaL, every one LRAT-verified; `cases11_split.out`) | — |
| κ=2, p=13 | SAT | UNSAT | FILL13 | — |
| κ=3, p=7 ({0,±1}) | SAT | UNSAT | UNSAT (1.3 s) | — |
| κ=3, p=13 ({0,1,5,8,12}) | SAT | UNSAT | UNSAT (unsplit, 2807 s, `big_13_k3_nest.out`; and 37/37 cases, `cases13k3.out`; PicoSAT, no proof) | — |
| (b) q=7, {0,±1} | SAT | UNSAT | UNSAT | — |
| (b) q=11, {0,±1,±2} | SAT | UNSAT | UNSAT (581 s) | — |
| (b) q=13, {0,…,±3} | SAT | UNSAT (69 s) | FILLINT13 | — |
| (c) {0,1}, p=5,7, d=1 | UNSAT | — | UNSAT (k=2,3) | UNSAT (k=2) |

The k = 1, d = 1 rows are the paper's contraction (κ = 2: Φ(a) = a for a ∈ P, νa for a ∉ P, ν the
least non-residue) and KOW's small-coefficient round, re-derived as feasibility facts.

## 3. p = 5, κ = 2: Theorem B

Here S = {0, 1, 4} = {0, ±1}, P = {±1}, and for a ∉ P (a = ±2) aS ∩ S = {0}.

**Fact F5 [exact; `enum_labels_p5.py` → `enum_labels_p5.out`].** GL_2(F_5) (order 480) has 36 096
orbits on subsets of F_5²∖0. For **every** orbit whose set L′ spans F_5² (all 36 096 orbits were
decided; the spanning ones number 1, 7, 30, 105, 313, 766, 1600, 2814, 4200, 5322, 5768, 5322,
4200, 2814, 1600, 766, 313, 105, 31, 8, 3, 1, 1 for |L′| = 2, …, 24), L′ is 2-feasible with weak
nondegeneracy, so by Lemma 2(A) a column set with these labels gains 2 or yields a witness
(0 infeasible orbits). For |L′| ≤ 7 the verdict was cross-checked by direct enumeration of the
image of S^{L′} in F_5^{L′}/⟨r_1, r_2⟩ (a 2-dimensional subspace inside it, or a nonzero S-vector
in ⟨r_1, r_2⟩), 0 disagreements. Label sets with |L′| ≤ 3 cannot gain 2 (the class sums span
c − k ≤ 1 dimensions), so for them the verdict means a witness: a nonzero {0,±1}-vector in the
row space of the labels, i.e. an S-valued dependency. Consequently Lemma J and the "+3" in the
window below are not needed at p = 5 (any δ′ ∈ D(X) independent of δ serves, and dim D(X) ≥ 2
suffices); the implementation and the proof keep them, which only costs O(1) per piece.

**Lemma J (four labels) [proved for every p ≥ 5].** Let X have k = dim D(X) ≥ 2 and c ≥ 4
**genuine classes** (columns with equal D(X)-functionals), and let δ ∈ D(X) have full support and
take ≥ 2 values. Then some δ′ ∈ D(X) independent of δ gives ≥ 4 distinct joint labels (δ_i, δ′_i).
*Proof.* Group the classes by the value of δ. For classes b ≠ b′, H_{bb′} = {z ∈ D(X): z_b = z_{b′}} is a
proper hyperplane (genuine classes are separated by D(X)). If δ takes ≥ 4 values we are done with
any δ′ ∉ ⟨δ⟩. If δ takes 3 values, some group has two classes b, b′; any δ′ ∉ H_{bb′} works (and
δ ∈ H_{bb′}, so δ′ ∉ ⟨δ⟩). If δ takes 2 values: either both groups have ≥ 2 classes (avoid two
hyperplanes) or one group has ≥ 3 classes b, b′, b″ (avoid three); t < p hyperplanes never cover
D(X) (t·p^{k−1} < p^k), so δ′ exists. ∎ (Sampled cross-check, 131 862 cases, 0 failures:
`lemma_j_check.out`.) If δ takes one value, X itself is a zero-sum (weights 1). If c ≤ k, the k × c
label matrix is invertible, so every class sum is 0: each class is a witness.

**Lemmas P, M, D over F_p [proved; the p = 3 proofs with 2/3 → 1−1/p].** P: deleting a
proportionality class of size a from a coloop-free F drops the rank by exactly a − 1 (the proof is
field-free). M: for δ uniform in a code D ⊆ F_p^N with nonzero coordinate functionals and
proportionality classes a_1..a_c, E[wt δ] = (1−1/p)N and Var[wt δ] = ((p−1)/p²) Σ a_j² (P(δ_i ≠ 0) =
1−1/p; proportional pairs are nonzero together, covariance (1−1/p) − (1−1/p)² = (p−1)/p²;
non-proportional pairs are jointly uniform). D: a codeword with (wt − (1−1/p)N)² ≤ Var is found
by conditional expectations; Φ(prefix) is computed exactly by grouping coordinates by the
projective class of the free part g_i (within a class f_i = c_i + s_i t, t uniform in F_p;
classes independent and centred), `wnest_p.py: pick_codeword`, asserted on every piece.

**Algorithm WNEST₅ at codimension q ≥ 3.** Pool = first N(q) unused columns, N(q) = min{N :
N − (5/4)q ≥ 15/4 + √N} (N(q) ≤ (5/4)q + √(2q) + 7 [proved: with N = ⌈(5/4)q + √(2q) + 7⌉,
√N ≤ √(2q+10) ≤ √(2q) + 3 for q ≥ 2; checked exactly for q < 5000, `closed_form_p5.out`]).
0. A pool column that is 0 in V lies in U: finish by Lemma 1.
1. Peel: delete coloops; delete the largest proportionality class of D(F) while its size is ≥ 5.
   Result F*, N* = |F*|, r* = rank(F*); all classes have size ≤ 4.
2. Select δ by Lemma D; X = supp δ. 3. Compute D(X) (dim k) and its classes. If δ is constant or
   c ≤ k: witness. Else choose δ′ by Lemma J, form L′ = {(δ_i, δ′_i)} (|L′| ≥ 4), solve the CNF for L′
   (constant size; cached), and apply Lemma 2(A) with the pair (δ, δ′): gain ⟨h_1, h_2⟩ (continue in
   V/⟨h_1, h_2⟩, returning F∖X to the front of the pool) or output a witness.
For q ≤ 2: one contraction round (pool q + 1, any dependency, a full line) per dimension.

**Theorem B [proved, given F5].** For every n ≥ 3 and every instance with m ≥ guarantee(n) ≤
n²/4 + 0.754 (n+2)^{3/2} + 5.75 n + √(2n) + 13 columns in F_5^n, WNEST₅ outputs a nonzero
{0,±1}-solution in deterministic poly(n, m) time, plus the time of ≤ n/2 constant-size CNF solves.
*Proof.* **Invariant.** Δ(F) = |F| − (5/4) rank F. A coloop deletion changes Δ by −1 + 5/4 > 0; a
class of size a ≥ 5 by −a + (5/4)(a−1) ≥ 0 (Lemma P). So Δ(F*) ≥ Δ(pool) ≥ 15/4 + √N ≥ 15/4 + √N*,
i.e. (4/5)N* ≥ r* + 3 + (4/5)√N*. **Window.** All classes ≤ 4 give Var ≤ (4/25)·4N*, σ ≤ (4/5)√N*;
Lemma D gives wt δ ≥ (4/5)N* − σ ≥ r* + 3 and wt δ ≤ (4/5)N + (4/5)√N. **Gain.** dim D(X) ≥
|X| − r* ≥ 3; by Lemma J and Fact F5 the piece gains 2 or yields a witness, or a witness is found
at step 3. **Cost.** |X| ≤ (4/5)(5q/4 + √(2q) + 7) + (4/5)(√(2q) + 3) = q + (8/5)√(2q) + 8.
**Accounting.** Stages q = n, n−2, …, ≥ 3 (≤ n/2 of them), Σ q ≤ n²/4 + n/2, Σ √q ≤ (n+2)^{3/2}/3,
then ≤ 2 one-dimensional rounds (≤ 5 columns), one closing column, and the first pool N(n); every
other column returns to the pool. Total ≤ n²/4 + n/2 + (8√2/15)(n+2)^{3/2} + 4n + 6 + (5/4)n +
√(2n) + 7. **Correctness.** Lemmas 1, 2(A); the output is re-summed (`wnest_p.py`). **Time.**
Per stage O(1) eliminations on q × N matrices, O(N²) class tests, O(k·p·N·k) for Lemma D, Lemma J's
candidate search (basis vectors, pair sums, then random combinations; existence proved), one
constant-size CNF. ∎

**Measured [sampled; `wnest_p5.out`, `adversarial_p5.out`].** Random/low-rank/few-distinct/sparse
instances at m = guarantee(n): n = 20: ≤ 178 of 210; 40: ≤ 579 of 661; 60: ≤ 1192 of 1340 (0.33 n²
consumed; KOW-type sparse one-dimensional recursion 1585, triangular 1891). Pieces cost q + 8..11.
Eleven structured families at n = 30 (series classes of size 3 and 4, which are *not* peeled;
duplicates; three blocks with proportional sums — the k = 2 degenerate structure; rank-3
columns; sparse; projective; signed; block-diagonal) consumed ≤ 350 of 407; hill climbs at
n = 8..14 reached 44/52, 61/72, 80/95, 101/120 and never violated an assertion. 4284 distinct
label sets were met, none infeasible. Finite checks falsify only; Theorem B does not rest on them.

## 4. p ≥ 7: obstruction, and the one-dimensional sparse fallback

**Obstruction [exact].** For (p, κ) = (7, 2): every one of the 19 cases of Lemma U is UNSAT, both
for the nested set (42 labels) and for all 48 patterns; (7, 3): UNSAT (unsplit, pycosat 1.3 s and
z3 35.5 s); FILLOBS. By Lemma 2(B), a column set with one column per nested pattern in general
position (q ≥ p(p−1) − 2) has R(X) ⊇ no 2-dimensional subgroup and no S-witness. Any piece gaining
2 from two dependencies therefore needs a *missing* pattern, and the only patterns a selection
rule controls (support nesting: ℓ_1 ≠ 0) are present. This closes the k = 2 route at these p;
k ≥ 3 bundles (labels in F_p^3) remain open except as noted in §2.

**Theorem C (sparse one-dimensional rounds) [proved].** Let p ∉ E_2(κ) (all p for κ = 2, 3) with a
normalized contraction (α, β) (α_j + β_i ∈ g^{−(i+j)}P ∪ {0}). At codimension l take the next l + r
columns, r = ⌈log_p(l+1)⌉, an r-dimensional space of dependencies of their images mod U, and the
sparsest of its p^r − 1 nonzero codewords δ; X = supp δ. The weights x_i = ζδ_i(α_{cos ζ} + β_{cos δ_i})
lie in S and realize ζv mod U for every ζ ∈ F_p^*, v = Σ β_{cos δ_i} δ_i λ_i (paper, prop:triangular-sde,
whose proof never uses that δ has full support on the block), so each round realizes a line at
cost |X| ≤ ⌊(l + r)(1−1/p)/(1−p^{−r})⌋ (a uniform nonzero codeword is nonzero at a given
non-identically-zero coordinate with probability (p^r − p^{r−1})/(p^r − 1); the minimum is at most
the mean). Unused block columns return to the pool. The recursion m_l = max{l + r, m_{l−1} + w_l},
m_0 = 1, gives m_a = (1−1/p) a²/2 + O(a log a) [proved: w_l ≤ (1−1/p)(l + r) + (l+r)/(p^r − 1) + 1 ≤
(1−1/p)l + 2r + 2 with p^r ≥ l + 1]. Every output is verified; `sparse_tri.out`: (p, κ) as in §0.3,
a ∈ {6, 10, 20, 40}, 20/20/20/6 instances per a from four families at the recursion budget, 0
failures; the budget is 0.46–0.51 a² at a = 40 (p = 5: 732 vs triangular 861). ∎ The contraction is
found by brute force for p ≤ 13 (`sparse_tri.py: find_contraction`).

## 5. Questions (b) and (c)

**(b)** [exact]. S_q = {−⌊q/4⌋..⌊q/4⌋}, P = {±1}. q = 5: S_5 = {0,±1} is the κ = 2 set, so Theorem
B applies verbatim: nesting halves (1−1/5)/2 = 0.4 to 1/4 in the worst case. q = 7, 11: the nested
two-dependency set is UNSAT; q = 13: §2. KOW's one-dimensional round is feasible at q = 5, 7, 11,
13 (k = 1, d = 1) and two dimensions never come from one dependency (k = 1, d = 2 UNSAT).

**(c) Lemma Z [proved].** Let p ≥ 5, S = {0,1}, and let (Φ, γ) realize one dimension from k
dependencies with labels L. Then with γ := γ_2: Φ(ℓ) = 0 ⟹ ⟨γ, ℓ⟩ ∈ {0,1} and Φ(ℓ) = 1 ⟹ ⟨γ, ℓ⟩ ∈
{−2,−1}; so L ⊆ γ^{-1}({−2,−1,0,1}), four parallel hyperplanes, and γ ≠ 0 unless Φ ≡ 0. The nested
sets F_p^*×F_p^{k−1} and F_p^k∖0 meet every nonzero functional in ≥ p − 1 ≥ 4 values with 2 among
them (for γ = (g, 0, …, 0) the values g·F_p^*), so they are infeasible for every k and every p ≥ 5
(for p = 3 the four values are all of F_3, which is KOW's gadget). ∎ Exact confirmation: k = 1, 2, 3
at p = 5, 7 UNSAT (`table_small.out`). A one-dimensional 0/1 piece thus needs a label set confined
to four hyperplanes — a pattern gap that neither support nesting nor weight selection produces —
so the framework gives no polynomial of degree below q − 1 here; it does not say that KOMSW's
degree is optimal.

## 6. Computations

All exact over F_p (numpy int64 / Python ints); every SAT model re-verified by brute force; every
solver output re-summed.

| artifact | what | result |
|---|---|---|
| `gadget_sat.py`, `gadget_cnf.py` | z3 / naive CNF feasibility (first encodings; p = 3 sanity, p = 5 discovery) | p = 3 reproduces KOW, NEST, all-8 UNSAT; p = 5 all-24 SAT |
| `gadget_cnf3.py`, `gadget_dfs.py`, `gadget_cnf2.py` | intermediate encodings (coset reduction; DFS) | superseded; agree where they finished |
| `gadget_cnf4.py` → `table_small.out`, `big_*.out`, `cases*.out`, `k3_7_*.out` | reduced binary-clause CNF, d ∈ {1,2,3}, case splits | §2 table |
| `gadget_z3.py` → `z3_7_int_nest.out` | second engine | agrees (UNSAT) |
| `cases_gen.py`, `cases_cover.py` → `cases_cover.out` | Lemma U case lists and covering | 0 missing pairs at p = 7, 11, 13 |
| `verify_gadget.py` → `verify_p5_all.out`, `verify_p3_nest.out` | gadgets on real column sets | exposed label-dependence of nondegeneracy (§1) |
| `enum_labels_p5.py` → `enum_labels_p5.out` | all 36 096 GL_2(F_5)-orbits of label sets | Fact F5 |
| `lemma_j_check.py` → `.out` | Lemma J sampled | 131 862 cases, 0 failures |
| `wnest_p.py` → `wnest_p5.out`; `adversarial_p5.py` → `.out`; `closed_form_p5.out`, `guarantee_p5.out`, `tables_p5.out` | WNEST₅, families, hill climbs, recursion vs closed form | §3 |
| `sparse_tri.py` → `sparse_tri.out` | Theorem C at six (p, κ) | 0 failures |
| `p5_all_solution.out`, `p5_nest_solution.out` | explicit F_5 gadgets (Φ, γ tables) | — |

## 7. Claim gates, next question, next command

Gates that must stay false: "Theorem B or C is new / has priority" (not checked beyond the local
literature notes; human review and a search are required before any external statement);
"c < 1/4 at p = 5" (no: a two-dependency piece costs ≥ rank + 2 ≥ q + 2 in general position, as at
p = 3); "the p ≥ 7 obstruction is an algorithmic lower bound" (it bounds the k = 2 piece
framework only); "k ≥ 3 bundles are excluded at p ≥ 7" (open unless §2 says otherwise);
"Theorem B's O(n^{3/2}) is O(n log n)" (not shown); finite checks are not scaling evidence.

Next hard question. At p = 7 (κ = 2), does a bundle of k ≥ 3 dependencies with the full nested
pattern set F_7^*×F_7^{k−1} gain two dimensions (the k = 3 CNF has 294 labels and γ ∈ F_7³; the
Lemma U split applies to the first slot)? A SAT answer plus the Lemma J/P/M/D machinery would give
a²/4 at p = 7; UNSAT for all k is the natural conjecture given Lemma Z's style of argument.

Next command. `cd research/audits/reviews/2026-11-08-rees-sde-fq-nest && /opt/anaconda3/bin/python -B gadget_cnf4.py 7 pow:2 3 2 nest --quiet --fix "1,0,1:3,0,0"` and the same with `--fix "1,0,1:0,3,0"`;
expected artifact `k3_7_nest_a.out`, `k3_7_nest_b.out`; acceptance: both UNSAT (closing k = 3 at
p = 7 for the nested set) or a SAT model, which must then be re-verified on random column sets with
`verify_gadget.py` before anything is built on it.

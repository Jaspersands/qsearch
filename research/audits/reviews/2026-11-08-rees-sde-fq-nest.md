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

0. **Referee update (2026-11-09): Theorem B′, p = 5 worst case n²/4 + 3n/2 + 2 [proved, refereed
   by AI (referee B), checked by the integrator; one finite input, Fact F5].** Every spanning label
   set in F_5²∖0 (all 36,090 GL_2(F_5)-orbits, any size, re-verified independently by referee B with
   a different CNF and plain-arithmetic checks) has a weakly nondegenerate S-realization. So at
   codimension q ≥ 2, the first q + 2 columns and *any* two independent dependencies gain two
   dimensions or give a witness (SIMPLE5, `2026-11-09-rees-sde-fq-nest-referee-B/simple5.py`); q = 1
   costs 2 columns. Deterministic poly(n, m) time for every m ≥ n²/4 + 3n/2 + 2 (exact recursion
   ≤ n²/4 + 3n/2 + 1.25, checked to n = 5000). The peeling, Lemma D and Lemma J below are not
   needed at p = 5; they remain the template where only nested label sets are feasible (p = 3).
1. **p = 5, κ = 2 (S = {0, ±1}): YES, two dimensions per piece, worst case n²/4 + O(n^{3/2})
   [proved, with two exact finite inputs; superseded in its error term by item 0].** Theorem B (§3): the deterministic algorithm WNEST₅
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
   algorithms. k = 3 at p = 7 (κ = 2, nested set F_7^*×F_7^2, 294 labels): also UNSAT [exact, given
   the two-case split of the first slot, `cases7k3.txt`; re-verified with the fixed checker, 9 Nov, case
   by case: each of the 2 cases solved as one CNF without the γ_(1,1) split, CaDiCaL UNSAT with its LRAT
   proof VERIFIED by the fixed lrat-check (`2026-11-09-lrat-checker-fix/recheck/k3_7_cases.out`). The
   original split, 2 cases × 343 values of γ_(1,1) = 686 sub-cases in `k3_7_split.out`, is CaDiCaL UNSAT;
   its proofs were not re-checked (checker was unsound, 9 Nov)].
3. **Every odd p (κ = 2) and every p ≡ 1 mod 3 (κ = 3): a proved constant below 1/2 by one-dimensional sparse rounds
   [proved].** Theorem C (§4): KOW's sparse-dependency selection (support ≤ (1−1/p)(l+r)/(1−p^{−r})
   from l + r columns, r = ⌈log_p(l+1)⌉) composed with the paper's contraction weights realizes a
   full line per round, so m ≥ (1−1/p) a²/2 + O(a log a) suffices deterministically given g and (α, β) (given the
   contraction, which exists for κ = 2, 3 at every p). Checked at (p,κ) ∈ {(5,2),(7,2),(11,2),
   (13,2),(7,3),(13,3)}, a ≤ 40, four families, every witness verified (`sparse_tri.out`); the
   O(a log a) term makes the gain over (a+1)(a+2)/2 small below a ≈ 40.
4. **(b) KOW small coefficients.** q = 5: yes (item 1). q = 7, 11: no nested two-dimensional
   gadget [exact at q = 7, `big_7_int_nest.out`; q = 11 only for the P-equivariant problem,
   `big_11_int_nest.out` (referee C finding 2: Lemma Q is not shown exact for S = {0,±1,±2})]; q = 13: open (§2). The one-dimensional
   KOW round is reproduced as a feasibility fact at q = 5, 7, 11, 13 [exact, `table_small.out`].
5. **(c) 0/1 subset sum at q = 5, 7.** Nothing of lower degree from this framework [argued; Lemma Z
   proves the four-hyperplane confinement and the infeasibility of nested and full label sets]: a 0/1 realization of even one dimension forces the label set into four parallel
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

**Lemma R (coset reduction) [proved; restated 9 Nov in the per-slot existence form of referee B
finding 3].** Call {λα : λ ∈ cP} (a projective direction [α] and a coset cP of P in F_p^*) a *slot*.
If a feasible, weakly nondegenerate (Φ, γ) exists, then a feasible, weakly nondegenerate (Φ′, γ′)
exists that is P-equivariant, γ′_{λα} = λγ′_α for all λ ∈ P and α ≠ 0, and normalised,
γ′_{e_j} = 0 (j = 1..d). On a slot, equivariance says γ′_{νβ} = νγ′_β (ν ∈ P) for any member β; the
proof builds γ′ from a member chosen per slot, depending on the solution, and the CNF places the slot's
free γ-value at a fixed representative. (The earlier statement, which took γ′_{λα} := λγ_α
from the original γ at a fixed set of representatives α, is false in general: if the only nonzero
realizer of a direction sits at a non-representative multiple, it can make that direction degenerate.)
*Proof (referee B finding 3).* In each slot pick a member β with y_β ≢ 0 on L if there is one (any member
otherwise) and set ỹ_{νβ} := ν y_β (ν ∈ P), i.e. γ̃_{νβ} := νγ_β with the same Φ. These values lie in
νS = S, and ỹ vanishes on a slot only if y vanishes on all of it, so every direction keeps a nonzero
realizer. In the slot Pe_j, with chosen member μ_j e_j (μ_j ∈ P), put Φ′_j := μ_j^{-1} y_{μ_j e_j} ∈ S. Then
Φ′_j − Φ_j = ⟨μ_j^{-1}γ_{μ_j e_j}, ℓ⟩ is a row-space term, so with γ′_α := γ̃_α − Σ_j α_j μ_j^{-1}γ_{μ_j e_j}
every realizer is unchanged, ỹ_α = ⟨α, Φ′⟩ + ⟨γ′_α, ℓ⟩; γ′ is P-equivariant (the correction is linear
in α) and γ′_{e_j} = 0. The choices are per slot, so they never conflict (unlike Lemma Q). ∎ So the free
data are one γ-value per slot, (p^d − 1)/|P| of them: for d = 2 and κ = 2, (p+1) directions × 2
cosets minus the two unit directions at coset 0 (where γ = 0 because Φ_j := y_{e_j}).

**Lemma Q (label scaling) [proved].** For λ ∈ P the constraints at λℓ with Φ(λℓ) := λΦ(ℓ) are those
at ℓ; a solution on L extends to the P-closure of L with the same γ; weak nondegeneracy is
unchanged. ∎ So labels are taken up to P-scaling.
*Referee C correction (2026-11-09).* The proof above shows only that a P-equivariant solution
extends; the UNSAT verdicts need the converse. **Lemma N [proved, referee C; checked by hand]:**
let S = P ∪ {0}, r ∉ P, and let L span F_p^k with no nonzero linear functional S-valued on L (true
for F_p^*×F_p^{k−1} and F_p^k∖0). In every feasible (Φ, γ), for any column multiplicities, the
direction [α] is degenerate iff γ_{rα} = rγ_α. (If γ_{rα} = rγ_α then y_α, r·y_α ∈ S force y_α = 0,
and each y_{λα} = ⟨γ_{λα} − λγ_α, ·⟩ is an S-valued linear functional on L, hence 0; conversely
y_{rα} − r y_α = ⟨γ_{rα} − rγ_α, ·⟩ vanishes on a spanning L.) So nondegeneracy depends on γ alone
and Lemma Q is exact for S = P ∪ {0}. It is not shown for interval S (q = 11 cell).

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
case splits (`cases*.out`); from 2026-11-09 `gadget_cnf5.py` (same encoding, CaDiCaL with LRAT proofs
checked by lrat-check; UNSAT is accepted only on a verified proof) with `run_split.sh` / `run_split_k.sh`
[**9 Nov correction:** the lrat-check build used for every run of 9 Nov accepted an empty clause without a
conflict, so its "LRAT VERIFIED" certified nothing (`2026-11-09-lrat-and-audit-fixes.md`). Runs re-done
with the fixed build `2026-11-09-lrat-checker-fix/lrat-check` are marked "re-verified with the fixed checker,
9 Nov"; the others are "CaDiCaL UNSAT, not independently proof-checked". The (11, 2) and k = 3 cells were
re-done case by case: each case of the case file was solved as one CNF, without the γ_(1,1) split. That CNF
is a clause prefix of each of its sub-case CNFs (checked on one recorded sub-case per case, whose regenerated
CNF matches the recorded cnf_sha256), so one verified proof per case covers the case, and the case cover
covers the cell. `gadget_cnf5.py` now defaults to the fixed build and refuses a checker that verifies a bogus
proof]
(each case split further over all values of γ_(1,1), an exact cover; coverage of every `*_split.out`
was checked against its case file); p = 3 sanity in `table_old_encoding.out` (KOW SAT, NEST SAT, all-8 UNSAT).

| S | k=1, d=1 | k=1, d=2 | k=2, d=2 nest | k=2, d=2 all |
|---|---|---|---|---|
| κ=2, p=5 ({0,±1}) | SAT | UNSAT | **SAT** | **SAT** (24 patterns) |
| κ=2, p=7 ({0,1,2,4}) | SAT | UNSAT | UNSAT (19 cases, ≤ 4.5 s each; also unsplit, CaDiCaL 1436 s, 12.3 GB LRAT proof, re-verified with the fixed checker, 9 Nov, `2026-11-09-lrat-checker-fix/recheck/unsplit_7_2.out`) | UNSAT (19 cases) |
| κ=2, p=11 | SAT | UNSAT | UNSAT (31 Lemma U cases, each solved without the γ_(1,1) split, LRAT proof re-verified with the fixed checker, 9 Nov, `2026-11-09-lrat-checker-fix/recheck/cases11_cases.out` and `cases11_c10.out`; the earlier 31 × 121 = 3751 sub-case split `cases11_split.out` is CaDiCaL UNSAT, not independently proof-checked) | — |
| κ=2, p=13 | SAT | UNSAT | UNSAT (37 Lemma U cases × 169 values of γ_(1,1); 6253 sub-cases, CaDiCaL UNSAT on every one, not independently proof-checked (checker was unsound, 9 Nov); `cases13_split.out`) | — |
| κ=3, p=7 ({0,±1}) | SAT | UNSAT | UNSAT (1.3 s) | — |
| κ=2, p=7, **k=3**, d=2 nest | — | — | UNSAT (2 cases, each solved without the γ_(1,1) split, LRAT proof re-verified with the fixed checker, 9 Nov, `2026-11-09-lrat-checker-fix/recheck/k3_7_cases.out`; the earlier 2 × 343 sub-case split `k3_7_split.out` is CaDiCaL UNSAT, not independently proof-checked) | — |
| κ=3, p=13 ({0,1,5,8,12}) | SAT | UNSAT | UNSAT (unsplit, 2807 s, `big_13_k3_nest.out`; and 37/37 cases, `cases13k3.out`; PicoSAT, no proof) | — |
| (b) q=7, {0,±1} | SAT | UNSAT | UNSAT | — |
| (b) q=11, {0,±1,±2} | SAT | UNSAT | UNSAT (581 s) **for the P-equivariant problem only**; the free problem is not established (Lemma N needs S ∩ 2S = {0}) | — |
| (b) q=13, {0,…,±3} | SAT | UNSAT (69 s) | **open**: Lemma U does not apply (S ≠ P∪{0}); unsplit PicoSAT > 17 h, one-slot split > 4.5 h on its first sub-case, two-slot sub-cases > 9 min each (28561 of them); stopped | — |
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
N − (5/4)q ≥ 15/4 + √N} (N(q) ≤ (5/4)q + √(2q) + 7 [proved: N₀ = ⌈(5/4)q + √(2q) + 6⌉ is feasible for all q ≥ 1, because
(√(2q) + 9/4)² ≥ (5/4)q + √(2q) + 7 ⟸ (3/4)q + 3.5√(2q) ≥ 31/16, and N₀ < (5/4)q + √(2q) + 7
(referee B finding 6: the earlier argument with N = ⌈(5/4)q + √(2q) + 7⌉ gave only + 8); checked exactly
for q < 5000, `closed_form_p5.out`, and for q < 10⁵ by referee B]).
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
Eleven structured families at n = 30 (chain3/chain4: proportional columns v, 2v, 3v, …, i.e. parallel
classes of the column matroid, not series classes; those runs end with an immediate witness, 38 columns
(referee B finding 9);
duplicates; three blocks with proportional sums — the k = 2 degenerate structure; rank-3
columns; sparse; projective; signed; block-diagonal) consumed ≤ 350 of 407; hill climbs at
n = 8..14 reached 44/52, 61/72, 80/95, 101/120 and never violated an assertion. 4284 distinct
label sets were met, none infeasible. Finite checks falsify only; Theorem B does not rest on them.

## 4. p ≥ 7: obstruction, and the one-dimensional sparse fallback

**Obstruction [exact].** For (p, κ) = (7, 2): every one of the 19 cases of Lemma U is UNSAT, both
for the nested set (42 labels) and for all 48 patterns; (7, 3): UNSAT (unsplit, pycosat 1.3 s and
z3 35.5 s); (7, 2) unsplit, independent of Lemma U: UNSAT by CaDiCaL (1436 s, 12.3 GB LRAT proof;
re-verified with the fixed checker, 9 Nov: regenerated CNF with the same 1134 vars and 106100 clauses,
a CaDiCaL proof of the same 12,293,854,888 bytes, verified by the fixed lrat-check in 224 s,
`2026-11-09-lrat-checker-fix/recheck/unsplit_7_2.out`); (11, 2): UNSAT on all 31 Lemma U cases, each solved as one CNF without the γ_(1,1) split (re-verified
with the fixed checker, 9 Nov, `2026-11-09-lrat-checker-fix/recheck/cases11_cases.out` and `cases11_c10.out`; the earlier split into 3751
sub-cases is CaDiCaL UNSAT, not independently proof-checked); (13, 3): UNSAT (PicoSAT, no proof); (13, 2): UNSAT on all 6253
sub-cases (CaDiCaL UNSAT, not independently proof-checked (checker was unsound, 9 Nov)). By Lemma 2(B), a column set with one column per nested pattern in general
position (q ≥ p(p−1) − 2) has R(X) ⊇ no 2-dimensional subgroup and no S-witness. Any piece gaining
2 from two dependencies therefore needs a *missing* pattern [argued; proved is only the
infeasibility of the full nested label set and its supersets, for any column multiplicities by Lemma N], and the only patterns a selection
rule controls (support nesting: ℓ_1 ≠ 0) are present. This closes the k = 2 route at these p [argued];
k ≥ 3 bundles (labels in F_p^3) remain open except k = 3 at p = 7, nested set: UNSAT (§2).

**Theorem C (sparse one-dimensional rounds) [proved].** Let κ ∈ {2, 3}, p ≡ 1 (mod κ) prime (for κ = 3 this
needs p ≡ 1 mod 3: otherwise every element is a cube and the problem is trivial), and p ∉ E_2(κ) (all such p
for κ = 2, 3), with a normalized contraction (α, β) (α_j + β_i ∈ g^{−(i+j)}P ∪ {0}). At codimension l take the next l + r
columns, r = ⌈log_p(l+1)⌉, an r-dimensional space of dependencies of their images mod U, and the
sparsest of its p^r − 1 nonzero codewords δ; X = supp δ. The weights x_i = ζδ_i(α_{cos ζ} + β_{cos δ_i})
lie in S and realize ζv mod U for every ζ ∈ F_p^*, v = Σ β_{cos δ_i} δ_i λ_i (paper, prop:triangular-sde,
whose proof never uses that δ has full support on the block), so each round realizes a line at
cost |X| ≤ ⌊(l + r)(1−1/p)/(1−p^{−r})⌋ (a uniform nonzero codeword is nonzero at a given
non-identically-zero coordinate with probability (p^r − p^{r−1})/(p^r − 1); the minimum is at most
the mean). Unused block columns return to the pool. The recursion m_l = max{l + r, m_{l−1} + w_l},
m_0 = 1, gives m_a = (1−1/p) a²/2 + O(a log a) [proved: w_l ≤ (1−1/p)(l + r) + (l+r)/(p^r − 1) + 1 ≤
(1−1/p)l + 2r + 2 with p^r ≥ l + 1]. **Running time** poly(a, log p): enumerate the dependency space
projectively, (p^r − 1)/(p − 1) < 1.5(l + 1) codewords per round. **Gain** over (a+1)(a+2)/2: a²/(2p) − O(a log a),
positive only when a ≫ p log a. Every output is verified; `sparse_tri.out`: (p, κ) as in §0.3,
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
sets F_p^*×F_p^{k−1} and F_p^k∖0 meet every nonzero functional in ≥ p − 1 ≥ 4 nonzero values, while the allowed nonzero values of ⟨γ, ℓ⟩ are
{−2, −1, 1}, only 3 (for γ = (g, 0, …, 0) the values g·F_p^*; any other nonzero functional takes all p values on
these sets), so they are infeasible for every k and every p ≥ 5
(for p = 3 the four values are all of F_3, which is KOW's gadget). ∎ Exact confirmation: k = 1, 2, 3
at p = 5, 7 UNSAT (`table_small.out`). A one-dimensional 0/1 piece thus needs a label set confined
to four hyperplanes — a pattern gap that neither support nesting nor weight selection produces —
so the framework gives no polynomial of degree below q − 1 here [argued]; it does not say that KOMSW's
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
"the p = 5 error term is o(n)" (Theorem B′ gives O(n); nothing better shown); finite checks are not scaling evidence.

Next hard question. k = 3 at p = 7 (nested set) is now UNSAT (§2), so the natural conjecture
"no k-dependency bundle gains two dimensions at p ≥ 7" survives its first test. Is there a proof of
it for all k (a Lemma Z style argument on the label hyperplanes), or a k = 4 SAT model at p = 7?

Next command. Referee §3 (Theorem B, Lemma J, the 36,096-orbit classification) and §4 (Theorem C)
first; the finite cells are done except q = 13 small coefficients, which needs a symmetry split
for interval S before it is worth more CPU. For k = 4 at p = 7: `run_split_k.sh 7 pow:2 4 cases7k4.txt 9
k4_7_split.out` after deriving the first-slot cover for k = 4 (the k = 3 two-case cover in
`cases7k3.txt` is the draft's claim and must be checked by the referee).

## 8. Referee dispositions (2026-11-09)

Referee C (`2026-11-09-rees-sde-fq-nest-referee-C.md`, scripts in the folder of that name):
A Theorem C ACCEPT WITH FIXES (κ = 3 needs p ≡ 1 mod 3; deterministic given g and (α, β);
running time poly(a, log p); gain over (a+1)(a+2)/2 is a²/(2p) − O(a log a), positive only for
a ≫ p log a); B Lemmas R, Q, U ACCEPT WITH FIXES (Lemma Q repaired by Lemma N, adopted above;
Lemma U's 3p − 2 cover proved for every p); C the k = 3 two-case cover ACCEPT (two orbits of the
first slot under σ(a, b) = (λa, Mb + av), proof in the report; k = 4 uses `1,0,1:3,0,0,0` and
`1,0,1:0,3,0,0`); D encoding and γ_(1,1) splits exact, all certificates re-checked [9 Nov: coverage only; the "LRAT
VERIFIED" lines it counted came from the unsound checker, see the correction in §2], **GAP for the
q = 11 interval cell** (adopted: downgraded); E Lemma Z ACCEPT (wording). An independent encoding
without Lemma Q (`free_cnf.py`) re-derives the p = 7 cells (58 runs; their LRAT proofs were re-verified
with the fixed checker, 9 Nov, `2026-11-09-lrat-checker-fix/recheck/refC_compare.out`). Verified by
the integrator by hand: Lemma N, and the two-orbit claim for the k = 3 first slot (w_b ≠ 0 maps to
(0, e_1) by M^T w_b = e_1, ⟨w_b, v⟩ = −λw_a; w_b = 0 maps to (1, 0) by λ = w_a^{-1}; σ acts on labels only).

Referee B (`2026-11-09-rees-sde-fq-nest-referee-B.md`, scripts in the folder of that name):
ACCEPT WITH FIXES. Orbit count 36,096 re-derived (direct GL_2 action and Burnside), Fact F5
re-verified on all 36,090 spanning orbits with an independent CNF, end-to-end run on real column
sets for every orbit, Lemma J exhaustive at p = 5, guarantee(n) matches the code, KOW Thm 3.7 at
q = 5 (constant 0.4, coefficients {0,±1}) cited correctly. M1 (adopted as Theorem B′, item 0):
error term O(n). M2 (Lemma Q only half proved): same as referee C finding 1, resolved by Lemma N for
S = P ∪ {0}. Minor: Lemma R proof wording; the Lemma 2(B) witness breaks the CNF normalisation;
N(q) argument gives +8 as written (fixable to +7); WNEST₅'s δ′ choice is randomised (SIMPLE5 is
not); Lemma J also holds at p = 3; "chain3/chain4" are proportional columns; two outputs lack a
generating script. Theorem B's explicit bound beats KOW's only for n ≥ 59; Theorem B′ beats it for
every tested 3 ≤ n ≤ 5000. Next question (referee B): do all spanning k = 3 label sets at p = 5
realize three dimensions? That would give n²/6 + O(n); decide it without Lemma Q unless Lemma N's
hypothesis is checked for that label set (it holds for any spanning set with no S-valued
functional).


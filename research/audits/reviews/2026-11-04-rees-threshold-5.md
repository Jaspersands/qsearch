# Two-level SDE threshold, round 5: non-character-sum routes

4 November 2026. AI-only research pass. It is not a human review, a Lean proof or a
priority claim. **"AI-checked, pending human review" applies to every claim below.**
Written incrementally: sections are appended as they are finished; §0 was written last.

Labels: **[proved]** written proof here; **[exact]** complete finite computation (script
named; every witness re-checked independently); **[float]** exact formulas evaluated in
floating point; **[argued]** heuristic.

Notation as in `2026-11-03-rees-threshold-3.md` (TH3) and `2026-11-03-rees-threshold-4.md`
(TH4): p ≡ 1 (mod κ), h = (p−1)/κ, Q_m = g^m Q_0 the cosets of the κ-th powers,
A_m = Q_m ∪ {0}. A *contraction* is (α, β) ∈ F_p^{2κ} with α_j + β_i ∈ A_{−(i+j)}
for all i, j ∈ Z_κ and α_0 + β_0 ≠ 0; it is *strict* if every cell is nonzero. E_2(κ) is
the set of p with no contraction; N is the number of strict normalised ones (β_0 = 0,
α_0 = 1). M_ij = α_j + β_i is the cell matrix. Scripts and outputs are in
`2026-11-04-rees-threshold-5/`, interpreter `/opt/anaconda3/bin/python`, C with `cc -O2`.
The running `dfs2b` scans and their `.out` files were only read, never touched.

## 0. Verdict

- **No analytic route works.** None of the brief's routes proves N > 0 below T_A by an
  argument. Each fails at a stated point:
  - (a) Symmetric ansätze. All of them are classified (Theorems 2.2 and 2.4). None improves
    a square-root method's exponent by more than 1/(κ−1).
  - (b) The local lemma is impossible in principle (3.2). Janson and forest-statistics
    certificates are refuted by μ_G ≫ 1 at exceptional primes (3.3). Sequential extension
    needs κ-column information (3.4).
  - (c) Patterned Kővári–Sós–Turán reduces to the column union bound (4.1).
- **The target sub-question is answered for κ = 8 by explicit certificates.** Every prime
  p ≡ 1 (mod 8) in (49417, 8^8/2] = (4.27·κ^{(κ+1)/2}, κ^κ/2] has a strict two-level
  contraction (Theorem 5.1 [exact]): 139,558 primes, each witness re-checked independently.
  The tool is route (a) used as a search: the transpose-symmetric family T1 has κ unknowns
  and is solved in milliseconds. In the band (20000, 49417], 661 of the 690 primes have witnesses: 657 strict, and 4 with zero cells. The remaining 29 primes, all ≡ 9 (mod 16), are undecided.
- **A structural finding.** The only symmetric families with first-moment threshold at most
  that of the full problem, H and P, need −1 ∈ Q_0 when κ is even. This explains why
  exceptional primes cluster at h odd (Fisher p = 5·10⁻⁴ at κ = 8).

Everything here is AI-checked, pending human review. §6 lists what holds, what is missing,
the claim gates and the proposed paper text.

## 1. Route (a), step 1: structure of the known witnesses [exact]

**Data.** 385 witnesses, all from the complete canonical search `dfs2b` (TH4's successor,
`2026-11-02-rees-schedules/small-prime/dfs2b.c`, copied unchanged to `dfs2b_copy.c`):
κ = 4, 5, 6 for p < 1000 and κ = 5 (p < 2000), 6 (p < 3000), 7 (3222 < p < 6500) from new
runs (`e2_k{4,5,6}.out`, `wit_k{5,6,7}.out`), and the 25 witnesses for κ = 8, 9 that the
running scans had printed when read on 4 November around 13:30 (`dfs2b_k8_*.out`,
`dfs2b_k9_*.out`; 31 witnesses, the scans are still adding more).

**Tests** (`witness_structure.py`, `witness_table.py`, `witness_generic_stats.py`;
outputs `witness_structure.out`, `witness_table.out`, `witness_generic_stats.out`). Each
witness is re-checked on all κ² cells, then tested for
- a *shift-scale symmetry*: λ ∈ F_p^×, (r,t) ≠ (0,0) with λ·M_{i+r, j+t} = M_ij for all i, j;
- a *transpose symmetry*: λ·M_{j+a, i+b} = M_ij for all i, j;
- arithmetic or geometric progressions (also after an affine shift) of {α_j} or {−β_i}
  along j ↦ j + t, t a unit;
- multiplicative orders of all ratios of nonzero cells (subgroup structure).

These properties are invariant under the recentring and transposition maps that `dfs2b`
uses for its canonical form (a symmetry of M is carried to one of M′_{ij} = M_{i+s,j+t}/M_{st}
with the same λ), so the canonical restriction does not hide them.

**Result.**

| κ | band p/κ^{(κ+1)/2} | h parity | witnesses | generic | half-shift H | Paley P | other symmetric |
|---|---|---|---|---|---|---|---|
| 4 | ≤ 2 | even / odd | 1 / 1 | 0 / 1 | 1 / – | – | – |
| 4 | > 2 | even / odd | 35 / 37 | 32 / 37 | 2 / – | – | 1 T1, 1 T* |
| 5 | ≤ 2 / > 2 | even | 3 / 61 | 2 / 61 | – | 1 / 0 | – |
| 6 | ≤ 2 | even / odd | 19 / 13 | 11 / 12 | 2 / – | 5 / – | 3 T1, 1 S*, 2 T* / 1 S* |
| 6 | > 2 | even / odd | 60 / 62 | all / all | – | – | – |
| 7 | ≤ 2 / > 2 | even | 30 / 32 | all / all | – | – | – |
| 8 | ≤ 2 | even / odd | 16 / 3 | 9 / 3 | 6 / – | 1 / – | 2 S*, 1 T* (with H) |
| 9 | ≤ 2 | even | 12 | 7 | – | 4 | 1 T1 |

Types (defined and classified in §2): **H** = shift (κ/2, κ/2) with λ = −1;
**P** = transpose with λ = −1, a + b ≡ 0 (κ zero cells, TH2 §3.4's coloured-clique family);
**T1** = transpose with λ = 1, a + b ≡ 0; S*, T* = other shift / transpose symmetries.

- **Generic witnesses have no detectable structure.** Over the 359 generic witnesses the
  number of cell-ratio pairs of order dividing 2κ is 1223 against 1224.3 expected for
  independent uniform nonzero values. No progression occurs for κ ≥ 6; the 6 at κ ≤ 5
  are 3-parameter affine fits of 4- or 5-term sequences and look like canonical-form
  artefacts. No subfield or multiplicative pattern is visible.
- **Structured witnesses occur only near the threshold.** Above 2κ^{(κ+1)/2}, 285 of 287
  witnesses are generic (the 3 exceptions are at κ = 4). At or below it, 23 of 98 are
  symmetric, all with h even (−1 ∈ Q_0) except a single S* witness at κ = 6.
- **At κ = 8 the witnesses closest to the threshold are dominated by symmetric ones**:
  of the 8 witnesses with p ≤ 0.61κ^{4.5}, 5 lie in H and 1 in P; 2 of the H ones also have
  a quarter-shift symmetry (λ of order 4), which implies H.

So the witnesses give no ansatz that captures generic solutions, but they do point to the
symmetric families of §2, which carry the existence near the threshold.

## 2. Route (a), step 2: every linear ansatz, classified

The constraint system is invariant under the maps that move a cell matrix M to
λ·M_{i+r, j+t} (shift and scale) or to λ·M_{j+a, i+b} (transpose), provided the coset
indices match. A solution fixed by such a map is a solution of a smaller system. This
section finds all of them.

**Lemma 2.1 (distinct entries) [proved].** In every contraction (zero cells allowed) the
α_j are pairwise distinct and the β_i are pairwise distinct.
*Proof.* If β_i = β_{i′} with i ≠ i′, then M_ij = M_{i′j} ∈ A_{−(i+j)} ∩ A_{−(i′+j)} = {0} for
every j, so all α_j equal −β_i. Row 0 then has the single value α_0 + β_0 in the κ different
sets A_{−j}, so it is 0, contradicting M_00 ≠ 0. The case α_j = α_{j′} is the same with
rows and columns exchanged. ∎ (This is `dfs2b`'s prune 2d, stated for α as well.)

**Theorem 2.2 (shift-scale ansätze) [proved].** Let M be a contraction with
λ·M_{i+r, j+t} = M_ij for all i, j, where (r,t) ≠ (0,0). Then
1. λ ≠ 1, and o := ord(λ) equals the additive orders of r and of t in Z_κ (so o ≥ 2, o | κ);
2. ind(λ) ≡ r + t (mod κ);
3. after a translation (α, β) ↦ (α − x*, β + x*), α_{j+t} = λ^{−1}α_j and β_{i+r} = λ^{−1}β_i.

Conversely, if (r, t, λ) satisfies 1–2 and M = (α_j + β_i) satisfies 3, then M is a
contraction iff its cell conditions hold on one cell of each orbit of
(i,j) ↦ (i+r, j+t) and M_00 ≠ 0. There are κ²/o orbits, and M depends on
g = κ/o column amplitudes and g row amplitudes.

*Proof.* λ(α_{j+t} + β_{i+r}) = α_j + β_i for all i, j means λα_{j+t} − α_j = β_i − λβ_{i+r},
so both sides equal a constant c. If λ = 1, iterating α_{j+t} = α_j + c a total of ord(t) ≤ κ < p
times gives c = 0, so α_{j+t} = α_j and β_{i+r} = β_i; Lemma 2.1 forces t = r = 0. So λ ≠ 1,
and φ(x) = (x + c)/λ has the unique fixed point x* = c/(λ − 1), with
φ^k(x) − x* = λ^{−k}(x − x*). If t = 0, every α_j equals x*, which Lemma 2.1 forbids; so t ≠ 0,
and likewise r ≠ 0, and α_j ≠ x*. Along the orbit j, j+t, … the values α are distinct
(Lemma 2.1) and return after ord(t) steps, so ord(λ) = ord(t). The same argument with
ψ(y) = (y − c)/λ, fixed point −x*, gives ord(λ) = ord(r). This proves 1 and 3. For 2, take
a nonzero cell (M_00 is one): M_{i+r,j+t} = λ^{−1}M_ij lies in Q_{−(i+j)−r−t} and in
Q_{−(i+j)−ind λ}. For the converse, under 2 the map M_ij ↦ λ^{−1}M_ij carries A_{−(i+j)} onto
A_{−(i+j)−r−t}, so one cell per orbit decides the orbit. ∎

**Corollary 2.3 (when the ansatz exists) [proved].** For o | κ with o ≥ 2, a triple
(r, t, λ) with properties 1–2 exists iff o is odd or h is even.
*Proof.* λ has order o iff λ = g^{(p−1)u/o} with u a unit mod o; then
ind λ ≡ (κ/o)·hu (mod κ). Elements of additive order o are r = (κ/o)r′, t = (κ/o)t′
with r′, t′ units mod o. So the condition is r′ + t′ ≡ hu (mod o). If o is even, r′ and t′
are odd and u is odd, so h must be even. If o is odd, or h is even, take u = 1 and choose r′
prime-power by prime-power (Chinese remainder theorem): for an odd prime q | o pick
r′ ≢ 0, h (mod q), possible since q ≥ 3, and for q = 2 pick r′ odd, so t′ = h − r′ is odd. ∎

**Theorem 2.4 (transpose ansätze) [proved].** Let M be a contraction with
λ·M_{j+a, i+b} = M_ij for all i, j, and put s = a + b. Then ind λ ≡ s, and exactly one
of the following holds:
- **T1**: λ = 1 and s ≡ 0. Then M_ij = γ_j + γ_{i+b} for some γ ∈ F_p^κ, and the
  conditions read γ_j + γ_k ∈ A_{b−(j+k)} for all j, k (j = k included): the symmetric
  form of the appendix after relabelling.
- **P**: λ = −1 and s ≡ 0, which needs −1 ∈ Q_0, i.e. h even. Then
  M_ij = α_j − α_{i+b}: the κ cells with j = i + b are zero, and the conditions read
  α_j − α_k ∈ Q_{b−(j+k)} for j ≠ k (TH2 §3.4's coloured clique).
- λ² ≠ 1 and ord(λ²) = ord(s) ≥ 2.

*Proof.* As before, α_j − λβ_{j+a} = λα_{i+b} − β_i = c, so β_i = λα_{i+b} − c and
α_j = λ²α_{j+s} + c(1 − λ). If λ² = 1, iteration gives c(1 − λ) = 0 and α_{j+s} = α_j, so
s = 0 by Lemma 2.1. Then λ = 1 gives T1 with γ = α − c/2, and λ = −1 gives 2c = 0, so c = 0 and P.
The coset statement follows from a nonzero cell as in Theorem 2.2. ind(−1) = κh/2 mod κ
is 0 iff h is even. If λ² ≠ 1, the orbit argument of Theorem 2.2 applied to
x ↦ λ²x + c(1 − λ) gives ord(λ²) = ord(s). ∎

These are all the maps M ↦ λ·(M ∘ π) with π a row permutation σ times a column permutation τ,
possibly composed with the transposition, that respect the pattern: σ(i) + τ(j) ≡ i + j + c
for all i, j forces σ and τ to be shifts **[proved]**. Field automorphisms of F_p are trivial.
Maps that do not permute cells are not considered **[scope]**.

**Proposition 2.5 (first-moment exponents) [proved arithmetic].** Under the
independent-cell count, a family with d free normalised parameters and n remaining cell
conditions has μ ≈ p^d κ^{−n}, which crosses 1 at p ≈ κ^{n/d}.

| family | exists when | d | n | e = n/d |
|---|---|---|---|---|
| full problem G | always | 2κ−2 | κ²−1 | (κ+1)/2 |
| shift family, orbit length o, g = κ/o | o odd or h even (Cor. 2.3) | 2g−1 | κg−1 | (κg−1)/(2g−1) |
| H = shift, o = 2, λ = −1 | κ even, h even | κ−1 | κ²/2 − 1 | (κ+1)/2 − 1/(2(κ−1)) |
| P (transpose, λ = −1), κ − 1 choices of b | h even (always if κ odd) | κ−2 | C(κ,2) − 1 | (κ+1)/2 |
| T1 (transpose, λ = 1), κ choices of b | always | κ−1 | C(κ+1,2) − 1 | (κ+2)/2 |
| transpose with ord(λ²) = o ≥ 2 | – | κ/o − 1 | ≥ κ²/(2o) − 1 | ≥ (κ²−2o)/(2κ−2o) > (κ+1)/2 |

Since (κg−1)/(2g−1) < (κ+1)/2 ⟺ 2g > κ − 1, **H is the only family whose exponent is
below the full problem's, and P is the only one that ties it.** For κ even both need h even.
For κ even and h odd, only T1 and the shift families with odd o are available, and both have
exponent ≥ (κ+2)/2. The last row uses (κ²−2o) − (κ+1)(κ−o) = κ(o−1) − o > 0. The crossing
points with exact h/p factors and multiplicities are in `families.py` / `families.out`
**[float]**:

| κ | κ^{(κ+1)/2} | p* of G | p* of H | p* of P | p* of T1 |
|---|---|---|---|---|---|
| 6 | 529 | 533 (1.01) | 446 (0.84) | 357 (0.68) | 910 (1.72) |
| 7 | 2401 | 2405 (1.00) | – | 1682 (0.70) | 4597 (1.91) |
| 8 | 11585 | 11585 (1.00) | 9991 (0.86) | 8381 (0.72) | 24350 (2.10) |
| 9 | 59049 | 59049 (1.00) | – | 43880 (0.74) | 134600 (2.28) |
| 10 | 316228 | 316200 (1.00) | 278300 (0.88) | 240300 (0.76) | 774300 (2.45) |

**Consequence: E_2 depends on h mod 2 [exact counts; argued mechanism].** For κ even, the two
families that win near the threshold need h even (p ≡ 1 mod 2κ). The exact searches show the
predicted asymmetry (`parity_table.py`, `parity_table.out`, from `e2_k*.out` and the
read-only `dfs2b_k8_*` outputs as of 13:40):

| κ | h even: largest exceptional | h odd: largest exceptional | decided h even / h odd | exceptional h even / h odd |
|---|---|---|---|---|
| 4 | 17 | 53 | 37 / 43 | 1 / 5 |
| 6 | 757 | 859 | 36 / 44 | 20 / 33 |
| 8 (p ∈ [4217, 8737], scan running) | ≥ 8641 | ≥ 8713 | 63 / 65 | 46 / 62 |

At κ = 8 the feasible fraction is 17/63 for h even and 3/65 for h odd (Fisher exact
two-sided p = 5·10⁻⁴). The witnesses of §1 show the mechanism directly: near the threshold
the h-even witnesses are mostly in H or P.

**Prediction [argued].** For κ = 8 the largest exceptional prime has h odd, i.e. p ≡ 9 (mod 16).
Below about 1.7κ^{(κ+1)/2} the h-odd primes have no competitive symmetric family, so they
behave like the bare full problem, whose largest exceptional prime has been
1.3–1.7·κ^{(κ+1)/2} for κ ≤ 7.

**Why the ansätze give no proof [proved for the stated methods].**
- *G, H, P, T1 by iterated one-variable Weil.* Each family has a last variable that faces
  ≥ κ coset conditions alone: a column of the full problem, a column a_j of H with its
  2·(κ/2) conditions, a vertex of P or T1. The per-tuple Weil threshold for κ conditions on
  one variable is ≈ κ^{2κ}, the T_W regime.
- *H by a T_A-type second moment.* Average over the κ/2 row amplitudes b and union-bound
  over the κ/2 column orbits. A pair x, x′ in one column puts 4 conditions on each b_i
  (x ± b_i, x′ ± b_i), whose count depends on x′/x, not only on a coset index as in the full
  problem (appendix Lemma `lem:app-s2-moments`). With Weil, each such factor carries a
  relative error 3κ⁴/√p, and κ/2 of them multiply, so R − 1 picks up ≈ 1.5κ⁵/√p. The union
  bound over κ/2 columns needs R − 1 < 2/(κ − 2), hence p ≳ 0.56κ^{12}, which is above
  T_A(κ) ≈ (κ−1)κ^κ for every κ ≤ 11. Beating this needs cancellation in the sum over x′/x,
  i.e. a 3-variable estimate, which is the square-root problem again. Even with these errors
  removed, κ/2 columns instead of κ improve T_A by at most a factor ≈ 2
  (p ≳ (κ/2 − 1)κ^κ) **[argued]**, and only for h even.
- *Square-root heuristic.* A family with d parameters and n conditions certifies by
  term-by-term square-root bounds only for p ≳ κ^{2n/d}. That is κ^{κ+1−1/(κ−1)} for H and
  κ^{κ+1} for P, against κ^{κ+1} for G. No family changes the exponent of a square-root
  method by more than 1/(κ−1).

So route (a) **fails as a proof route**. It succeeds as a *search* route: H and T1 are tiny
systems that a randomized search solves in milliseconds above their own thresholds (§5).

## 3. Route (b): sequential extension, local lemma, Janson

Model: (α, β) uniform on F_p^{2κ}; the good events are G_ij = {M_ij ∈ Q_{−(i+j)}}, each of
probability q = h/p ≈ 1/κ; B_ij is the complement. A strict contraction is ∩ G_ij (together
with M_00 ∈ Q_0, which is G_00).

**Lemma 3.1 (forest independence) [proved].** For a set E of cells, the values (M_ij)_{(i,j)∈E}
are independent and uniform on F_p iff E, as an edge set of K_{κ,κ}, is a forest. In
particular the events G_ij are pairwise independent, and also independent along every path,
star and tree. The first dependence is on 4-cycles.
*Proof.* The linear forms α_j + β_i for (i,j) ∈ E have rank |V(E)| − c(E) (unsigned bipartite
incidence matrix, c = number of components), which equals |E| iff E is a forest. A
surjective linear map from a uniform vector gives uniform independent outputs. ∎

**3.2 Local lemma: impossible [proved].** P(B_ij) = 1 − q ≥ 1/2 for κ ≥ 2, and two cells in
one row share the variable β_i. Any local-lemma criterion that sees only which variables each
event depends on and the event probabilities must also cover the family where B and B′ depend
on the shared variable alone and B ∪ B′ is everything, which exists when
P(B) + P(B′) ≥ 1. Hence no such criterion certifies ∩ G_ij ≠ ∅. This covers Shearer's
optimal dependency-graph bound, the lopsided and variable versions, and resampling
(Moser–Tardos) conditions. Grouping cells into events "column j fails given β" turns the local
lemma into the column union bound, which TH3's O2 already excludes below κ^κ/2.

**3.3 Janson, Harris, and all forest information: refuted on actual primes [proved + exact].**
By Lemma 3.1, every statistic of the cell events supported on forests coincides at every prime
with the independent model, where P(all good) = q^{κ²}. Any certificate that uses only such
statistics, together with p and κ, can therefore depend on the instance only through
μ_G = p^{2κ−2} q^{κ²−1}, the independent-cell first moment of N (e.g. Janson's inequality,
whose Δ vanishes for pairwise independent events, or a Harris/FKG-type bound N ≥ c·μ_G).
At exceptional primes, μ_G is far above 1 (`families.out` **[float]**):

| κ | largest exceptional p | μ_G at that p | strict N |
|---|---|---|---|
| 4 | 53 | 15.5 | 0 |
| 5 | 181 | 16.9 | 0 |
| 6 | 859 | 122 | 0 |
| 7 | 3221 | 33.5 | 0 |

So no inequality of the form N ≥ c·μ_G (c > 0 absolute), and no certificate built only on
forest statistics, can hold below μ_G ≈ 122 at κ = 6. The obstruction lives in the 4-cycle
correlations, which are character sums over the graphic arrangement (TH3 §2).

**3.4 Sequential extension with exact one-column statistics [proved].** Order the 2κ − 2
normalised unknowns. The last unknown always faces κ conditions: it is a column against all κ
rows, or a row against all κ columns. Its candidate count is
n = #{x : x + r_i ∈ Q_{m_i}, i = 1..κ}, and over uniform earlier unknowns
E n = h^κ/p^{κ−1} < p/κ^κ (appendix Lemma `lem:app-s2-moments`). For p < κ^κ the last step
therefore fails on a fraction > 1 − p/κ^κ of prefixes. A sequential certificate must steer the
earlier choices into the rare prefixes where the final count is positive. That is a statement
about all κ columns at once (TH3 O2/O3), not a one-column statistic. Certifying each step by
a second moment over the previous choices is the T_A argument itself. So route (b) cannot go
below about κ^κ/2 unless it carries κ-column information.

*Numeric check.* At the κ = 8 exceptional primes found by `dfs2b`, the complete tree
explores 3.5·10⁵ (p = 4217) to 2.6·10⁷ (p = 8017) nodes. Each node is a prefix of rows with
every column still nonempty, so these primes have many prefixes that survive every
one-column test and none that completes.

## 4. Route (c) additive combinatorics, and (d) literature

**4.1 Kővári–Sós–Turán [proved].** The colour-0 graph {(x, y) : x + y ∈ Q_0} on F_p × F_p
has density q. KST gives a monochromatic K_{t,t} (all sums in Q_0) once
p^{1/t} > κ·t^{1/t}, i.e. p ≳ tκ^t. At t = κ that is the T_A scale, and it is a
combinatorial, non-character-sum proof, but for the wrong pattern. KST's convexity step
bounds Σ_y C(d(y), t) from below by a single degree function. In the Rees pattern each
column label j has its own function n_j(β), and the needed inequality
E[Π_j n_j] ≥ c·Π_j E[n_j] is exactly what TH3's O2 law violates. Real instances violate it
too: every E n_j > 0 while N = 0 at E_2 primes. So the patterned KST is the single-column
union bound again.

**4.2 Sum sets of cosets [argued].** The available theorems give upper bounds on structured
sums inside one coset (Hanson–Petridis: A + B ⊆ Q_0 ∪ {0} ⇒ |A||B| ≤ h + |B ∩ (−A)|, read
in TH3), or covering statements (Q_a + Q_b ⊇ F_p^× for p ≳ κ⁴), which are proved with
characters. For κ × κ rectangles with κ² ≪ h they impose nothing, and none gives existence
of a prescribed non-monochromatic pattern. No reduction of the Rees pattern to a
monochromatic one was found: substitutions α_j ∈ Q_{u_j} move the label dependence into
ind(1 + β_i/α_j) and do not remove it.

**4.3 Literature [scope].** No network was used. The repository's offline literature cache
(`research/literature_cache/`, `tmp/pdfs/`) contains nothing on Paley-type cliques,
character patterns or coset sum sets, beyond what TH2/TH3 read (Kunisky–Yu,
Benjamini–Gurel-Gurevich–Peled, Katz IMRN 2002, Hanson–Petridis). Nothing new was read.

## 5. Route (d): an explicit construction for every prime, κ = 8 [exact]

The ansätze of §2 do not give proofs, but they make the search tiny. T1 has κ unknowns
instead of 2κ − 2, and its conditions γ_j + γ_k ∈ Q_{b−(j+k)} form a clique-type system that
a most-constrained-first search solves at once when solutions exist. H is the same for h even.
So positivity can be certified one prime at a time, with an explicit witness, across the
whole range the brief names.

**Tools** (all in `2026-11-04-rees-threshold-5/`):
- `famsym.c`: T1 search, valid for every p. Its `complete` mode tries all b ∈ Z_κ with no
  node limit. γ_0 is fixed by Q_0-scaling, and the search branches on every candidate of the
  most constrained unknown, so it decides whether T1 has a strict solution.
- `famsearch.c`: H search (h even), randomized over b_0, so it is incomplete. It also has a
  `full` mode, which is too slow above 2·10⁴ and was not used for results.
- `dfs2r.c`: `dfs2b` with candidate lists shuffled and restarts. It reports only
  witnesses, never infeasibility. It is used for primes where no family has a solution.
- `verify_witnesses.py`: an independent checker (Python/sympy, no shared code). Strict by
  default. `--zeros` also accepts zero cells off (0,0), which is the definition of E_2. It checks
  that p is prime, p ≡ 1 (mod κ) and ζ = g^h has exact order κ, and then
  (α_j + β_i)^h = ζ^{−(i+j)} with α_j + β_i ≠ 0 for all κ² cells. With `--cover` it lists
  every prime p ≡ 1 (mod κ) in a range that has no valid witness. Existence does not depend
  on the coset generator (appendix, paragraph after the definition of E_2), so any g with
  ζ of order κ is a valid labelling.

**Cross-checks.**
- `famsym complete` against an independent pure-Python backtracking (`xcheck_t1.py`): all
  77 primes agree, for κ = 4 (p < 400), 5 (p < 300) and 6 (p < 250).
- No family search ever produced a witness at a prime that a complete search puts in
  E_2. This covers κ = 4, 6 with p < 1000 (`famsearch full`) and the κ = 8 primes that
  `dfs2b` declared INFEASIBLE, searched again with `famsearch half` at 20000 restarts
  (`h_k8_retry_4000_20800.out`). The H witnesses it found at 5233, 5297, 6481, 6961 and 7057
  are exactly the primes where `dfs2b`'s own witness lies in H (§1).
- Every witness was re-checked twice: inside the C program by exponentiation, and by
  `verify_witnesses.py`. No check failed.

**Family exceptional sets [exact for T1; incomplete search for H].**
- κ = 4..7, T1 complete (`t1_k{4,5,6,7}_complete.out`). The largest prime where T1 has no
  strict solution is 109, 691, 2011, 11383, which is 2.5, 3.6, 2.2, 2.5 times T1's
  first-moment crossing.
- κ = 8, h odd, T1 complete on [8000, 80000] (`t1_k8_hodd_8000_80000.out`): 260 empty
  primes, the largest **49417 = 4.27·κ^{4.5}**, and every h-odd prime in (49417, 80000] has a
  T1 solution. With h even, T1 is also empty at 55889 (`fix_k8_55889.out`), where H has a
  solution.
- κ = 8, h even, H randomized: a witness was found for every h-even prime in
  (20000, 49418]. For 20849, 20929 and 22769 this took up to 20000 restarts
  (`h_k8_heven_8000_40000.out`, `h_k8_heven_40000_49418.out`, `h_k8_retry_20800_22800.out`).

**Theorem 5.1 (κ = 8, finite computation) [exact].** Every prime p ≡ 1 (mod 8) with

    49417 < p ≤ 8^8/2 = 8388608

has a strict two-level contraction. So the strict count N is positive and p ∉ E_2(8). The
range is (4.27·κ^{(κ+1)/2}, κ^κ/2], which answers TH3 §7(i)'s sub-question for κ = 8 with
C = 4.27.

*Certificate.* There is one explicit witness (g, α, β) per prime: 139,558 primes, in
`sweep_k8_{a,a1,a2,b,b1,b2,c,c1,c2}.out` (the parts a, b, c were stopped part-way and
re-split, so the files overlap only at their seams), plus `fix_k8_55889.out` for the one
prime where the randomized T1 search missed. `verify_witnesses.py --cover 8 49418 8388608`
re-checks all 139,558 witnesses independently and lists every prime of the range:
`verify_sweep_k8.out` reports bad = 0 and missing = 0. All witnesses except 55889 lie in T1.
The sweep took ≈ 2 CPU-hours, dominated by building the index table, which is O(p) per prime.

**The band (20000, 49417] [exact where stated].** It contains 690 primes p ≡ 1 (mod 8),
351 with h even and 339 with h odd.
- Every h-even prime (p ≡ 1 mod 16) has an H witness.
- Every h-odd prime has a T1 witness, except the 121 primes listed in
  `gap_k8_hodd_T1empty.txt` (20089 to 49417), where `famsym complete` proves T1 empty.
- For those 121 no family of §2 applies (H and P need h even), so only a generic search can
  help. `dfs2r` was run on them from both ends of the list (`gap_part{1,2,3,1r,2r}.txt`,
  `gap_run.sh`, outputs `gap_k8_part*.out`), with each prime taking 2 s to 10 min.
  I stopped the runners after about an hour, keeping to a bounded window. At that point 92 of
  the 121 had witnesses (`verify_band_k8_zeros.out`):
  - 88 are strict.
  - 4 (22921, 25321, 26681, 26713) have one or two zero cells, none at (0,0). In `nosym`
    mode `dfs2r` drops `dfs2b`'s zero-cell prune 2d. Such a witness is a contraction in the
    sense of E_2, so these primes are outside E_2(8), but it does not show the strict
    N > 0. `verify_witnesses.py --zeros` checks this case and reports it separately. The
    strict check, `verify_band_k8.out`, rejects exactly these 8 lines.
  - The other 29 primes (`gap_k8_unresolved.txt`, 22937 to 43177, all ≡ 9 mod 16) are
    **undecided**. They have no witness, and there is no infeasibility claim, since `dfs2r`
    never makes one.
- This is §2's mechanism in action. For h even the half-shift family alone covers the band.
  For h odd, the primes left without a symmetric witness are exactly the ones near the
  threshold that are hard.

**Below 20000 (overlap with the running `dfs2b` scan).** H and T1 witnesses exist for 115 of
the 313 primes p ≡ 1 (mod 8) in [8000, 20000], and for 8 primes below 8000
(`feasible_below20000_k8.txt`, 123 primes; `verify_below20000_k8.out`). When this was read,
the scan had decided every prime up to 9001. The 11 listed primes ≤ 9001 agree with it: none
of them is on an INFEASIBLE line. The other 112 are FEASIBLE decisions that the scan has not
reached yet. The rest of [9001, 20000] is left to the scan.

**Why the range stops at κ^κ/2.** The upper end is the target of TH3 §7(i). Beyond it the
cost per prime grows like p (index table), and the gap (8388608, T_A(8) ≈ 1.17·10⁸] holds
about 1.5·10⁶ primes. At the measured rate that is ≈ 10⁵–10⁶ CPU-seconds: mechanical, but
not run here.

## 6. What holds, what is missing, gates, proposed text

**6.1 Statement that now holds.**
- *κ = 8, finite computation [exact; AI-checked, pending human review].*
  1. No prime p ≡ 1 (mod 8) with 49417 < p ≤ 8388608 = 8^8/2 lies in E_2(8). Each has an
     explicit strict witness (Theorem 5.1).
  2. In (20000, 49417], E_2(8) is contained in the 29 primes of `gap_k8_unresolved.txt`.
  3. In (9001, 20000], the 112 primes of `feasible_below20000_k8.txt` above 9001 are not in
     E_2(8).
  4. Below 9001, E_2(8) is decided by the running `dfs2b` scan together with the
     appendix's search up to 4201: every prime p ≡ 1 (mod 8) up to 9001 has a FEASIBLE or
     INFEASIBLE line, and none has both. The largest element so far is 9001 ≈ 0.78·κ^{4.5},
     which is the scan's result, not this pass's. The largest h-even one is 8641.
  5. Together with T_A: E_2(8) ⊆ [3, 20000] ∪ the 29 primes of `gap_k8_unresolved.txt` ∪ (8388608, T_A(8)], with
     T_A(8) ≈ 1.17·10⁸.
- *Any κ [proved].*
  - Lemma 2.1 (distinct entries).
  - Theorems 2.2 and 2.4, with Corollary 2.3: the complete list of shift, scale and
    transpose symmetric ansätze, and when each exists.
  - Proposition 2.5: H is the only family with first-moment exponent below (κ+1)/2. It and
    the tying family P both need h even when κ is even.
  - Lemma 3.1 (forest independence).
  - The no-go statements 3.2 (no local-lemma criterion), 3.3 (no forest-statistics
    certificate, refuted by μ_G ≫ 1 at exceptional primes), 3.4 (sequential extension
    needs κ-column information) and 4.1 (patterned KST reduces to the column union bound).
- *The parity mechanism [exact counts, argued mechanism].*
  - At κ = 8, exceptional primes skew to h odd (Fisher p = 5·10⁻⁴ on the data of §2).
  - The three exceptional primes the scan decided after §2 was written, 8761, 8969 and 9001,
    all have h odd.
  - The prediction that max E_2(8) ≡ 9 (mod 16) still stands. It is a heuristic, not a
    theorem.

**6.2 Still missing.**
- *An analytic proof.* No route of the brief yields a proof of N > 0 below T_A for any
  κ ≥ 5. Routes (a), (b) and (c) fail at the points stated in §§2–4. The κ = 8 result is a
  finite computation, not a method. It does not extend to other κ without new runs, and
  it gives no exponent.
- *κ = 8, the remaining ranges.*
  - (20000, 49417]: the 29 primes of `gap_k8_unresolved.txt`, all ≡ 9 (mod 16). Each needs a
    witness or a complete `dfs2b` run, which at p ≈ 2·10⁴ costs hours per prime. Four more
    primes (22921, 25321, 26681, 26713) are outside E_2(8) by non-strict witnesses, but the
    strict N > 0 is not shown for them.
  - (9001, 20000]: 173 of its 285 primes p ≡ 1 (mod 8) have no family witness. They are left to the running scan.
  - (8388608, T_A(8)]: about 1.5·10⁶ primes. T1 almost surely covers them, since its
    exceptional set ends far below this range, but they were not run. This is mechanical,
    at about 10⁵–10⁶ CPU-seconds.
  Only when all three are closed is E_2(8) known exactly.
- *κ ≥ 9.* Not run. For κ = 9 (odd) the P family exists for every p and has exponent
  (κ+1)/2 (Proposition 2.5). A T1/P sweep over (C·9^5, 9^9/2] is the analogue of
  Theorem 5.1, with about 10⁷ primes, and is much more expensive.
- *Review.* Human review of §2's proofs and an independent re-run of
  `verify_witnesses.py` are both still needed.

**6.3 Claim gates that must stay false.**
- The threshold for E_2(κ) is of order κ^{(κ+1)/2}, as a theorem for any κ. Theorem 5.1 is
  one finite range at one κ.
- Any proved exponent below κ (T_A's) for general κ.
- E_2(8) is known exactly. The ranges listed in 6.2 are still open.
- A character-sum-free proof of positivity below T_A for some κ ≥ 5 in the analytic sense.
  Theorem 5.1 is a computer certificate.
- Schedule 2's arity, or its two-level contraction, is optimal.
- Any novelty or priority claim. Nothing from the literature was checked online.
- "max E_2(8) ≡ 9 (mod 16)" stated as a theorem.
- The H searches (`famsearch half`) or the `dfs2r` runs certify emptiness. Only
  `famsym complete` decides its family, and only `dfs2b` decides the full problem.
- The scan lower bounds as final. 9001 ∈ E_2(8) and 17551 ∈ E_2(9) are lower bounds on
  max E_2 while the scans run.

`research/reductions/rees_hsp_reduction.json` was not edited, and no gate was flipped.

**6.4 Proposed paper text (not applied; `.tex` files untouched).**
- *`appendix-schedule2.tex`, remark on the size of E_2.* Replace the sentence beginning "For
  $\kappa = 8$ and $9$ the exceptional sets are not known exactly" with:

  > For $\kappa = 8$ and $9$ the exceptional sets are not known exactly. An exhaustive search
  > with symmetry breaking (\file{research/audits/reviews/2026-11-03-rees-dfs2-prune.md},
  > continued in \file{research/audits/reviews/2026-11-02-rees-schedules/small-prime/};
  > finite computation, AI-checked, pending human review) decides every prime
  > $p \equiv 1 \pmod 8$ up to $9001$ and every prime $p \equiv 1 \pmod 9$ up to $5689$, and
  > shows $9001 \in E_2(8)$ and $17551 \in E_2(9)$. So the largest exceptional prime is at
  > least $0.77\,\kappa^{(\kappa+1)/2}$ for $\kappa = 8$ and at least
  > $0.29\,\kappa^{(\kappa+1)/2}$ for $\kappa = 9$. In the other direction, an explicit
  > two-level contraction with every entry nonzero, each checked independently, exists for
  > every prime $p \equiv 1 \pmod 8$ with $49417 < p \le 8^8/2$
  > (\file{research/audits/reviews/2026-11-04-rees-threshold-5.md}, Theorem~5.1; finite
  > computation, AI-checked, pending human review). Hence
  > $E_2(8) \cap (49417, 8^8/2] = \emptyset$, which is below $T_A(8) \approx 1.17\cdot10^8$
  > by a factor $14$. For $\kappa \ge 10$ only bounds on $E_2(\kappa)$ are known.

  The integrator should re-read the scan before using this text. If the scan has reached
  a larger INFEASIBLE prime, put that prime in place of 9001 and recompute the constant
  0.77.
- *Optional sentence, same remark, after the observed-threshold discussion.*

  > The witnesses near the observed threshold are mostly invariant under
  > $M_{ij} \mapsto -M_{i+\kappa/2,\,j+\kappa/2}$ or under transposition. For even $\kappa$,
  > the only such families whose first-moment threshold is at most that of the full problem
  > require $-1$ to be a $\kappa$-th power. In line with this, for $\kappa \in \{4,6,8\}$ the
  > exceptional primes are more frequent when $(p-1)/\kappa$ is odd
  > (\file{research/audits/reviews/2026-11-04-rees-threshold-5.md}, Section~2).
- *Consistency note, not a change of claim.* The "Not shown" item says the appendix "does
  not determine $E_2(\kappa)$ for $\kappa \ge 7$", while the item before it gives
  $E_2(7)$ exactly by a finite computation. "Does not determine, other than by finite
  computation, …" would remove the apparent conflict.

**6.5 Artifacts** (`2026-11-04-rees-threshold-5/`).

| file | role |
|---|---|
| `witness_structure.py`, `witness_table.py`, `witness_generic_stats.py` (+ `.out`) | §1 witness tests |
| `families.py`, `parity_table.py` (+ `.out`) | §2 crossing points, μ_G table, parity table |
| `dfs2b_copy.c`, `e2_k{4,5,6}.out`, `wit_k{5,6,7}.out` | complete-search data for §1 |
| `famsym.c`, `t1_k*_complete.out`, `t1_k8_hodd_8000_80000.out`, `xcheck_t1.py` | T1 search, complete mode, cross-check |
| `famsearch.c`, `h_k8_*.out` | H search (incomplete) |
| `dfs2r.c`, `gap_run.sh`, `gap_part*.txt`, `gap_k8_part*.out`, `gap_k8_hodd_T1empty.txt` | generic witnesses for the 121 T1-empty primes |
| `sweep_k8_*.out` (24 MB), `fix_k8_55889.out`, `verify_sweep_k8.out` | Theorem 5.1 certificate |
| `feasible_below20000_k8.txt`, `verify_below20000_k8.out` | family witnesses below 20000 |
| `verify_band_k8.out`, `verify_band_k8_zeros.out`, `gap_k8_unresolved.txt` | band (20000, 49417]: strict and non-strict checks; the 29 undecided primes |
| `verify_witnesses.py` | independent checker (sympy) |

The compiled binaries (`dfs2b_copy`, `dfs2r`, `famsym`, `famsearch`) and
`dfs2r_k8_gap_test_truncated.out` are scratch and should not be committed. It is worth
compressing the 24 MB of sweep output before any commit, because the repository is public.

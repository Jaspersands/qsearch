# Rees open problem (1): linear arity for the diagonal κ-solution problem (2026-11-13)

AI only (one Claude Code subagent), pending human review. No paper, STATE, handoff, registry or
reductions file was edited. No Git, no network, no API calls. Every run used `nice -n 19`, one at a
time, largest RSS about 0.1 GB, longest run a few minutes. Scripts and outputs are in
`research/audits/reviews/2026-11-13-rees-linear-arity/`, run with `/opt/anaconda3/bin/python`
(the lattice probe with `/opt/anaconda3/envs/qsearch-cas/bin/python` for fpylll).

Labels: PROVED, PROVED given cited results, CONDITIONAL, REFUTED, UNKNOWN, NOT computed, ARGUED.
Finite checks only falsify.

Inputs read: core `main-core.tex` §5 (lines 527–766: thm:is-import, lem:rounds,
lem:zero-sum-length, Schedule 1H, rem:kappa-two) and §10 (sec:outlook, open problem (1));
`main.tex` prop:decoupled-sde, prop:triangular-sde, rem:triangular-scope;
`appendix-sde-side.tex` rem:sde-subquadratic, rem:sde-block-steered, rem:sde-worst-case(-q1);
`appendix-schedule2.tex` line 375 (κ = 3 small primes); the verdicts (§0) of the prior repo
reports on this exact question: 2026-11-02 linear-arity, 2026-11-07 subquad-A/B/lit,
2026-11-08 near-linear, uniform-p, fq-nest, 2026-11-11 bounded-p, near-linear-total,
2026-11-12 exponent-k8-attack (Lemma S/F, Theorem HC), 2026-11-13 k9-bottleneck; STATE "Now";
TRAPS.

Notation. κ ≥ 2, p ≡ 1 (mod κ) prime, g a primitive root, P = (F_p^×)^κ, P0 = P ∪ {0},
C_ν = g^ν P, cos(y) = ν for y ∈ C_ν, h = (p−1)/κ. A bank is λ_1..λ_n ∈ F_p^a; a solution is
x ∈ P0^n ∖ 0 with Σ x_i λ_i = 0. SDE(κ,p,a,n) is "given any bank, find a solution". Arity = n.

## 0. Verdict

**Linear arity is not reached, and none of the three routes tried gets below quadratic.** That
agrees with the ten earlier repo passes on this question. This pass adds four things, two of
them usable in the core:

1. **Lemma K (explicit contraction at κ = 3), PROVED.** α = (1, 0, −b), β = (0, b, −1), with
   b ∈ C_1 and 1 + b ∈ C_2, is a universal two-level contraction at every prime p ≡ 1 (mod 3).
   Such a b exists because #{b} = (1,2)_3 = (p+1+L)/9 ≥ 1 (Jacobi sums, §4). So the triangular
   solver (prop:triangular-sde) runs at κ = 3 with (a+1)(a+2)/2 columns at **every** prime. The
   core has 27(a+1)³ there (degree 3 → 2). This removes the T_A(3) bound and the three
   exhaustive searches the full version needs for 7 ≤ p ≤ 79. For κ = 2 the analogue
   (α = (1,0), β = (0, ν−1), with ν the least non-square) is one line, and the core uses
   (a+1)² there.
2. **Lemma D (coset-doubling tower), PROVED given core lem:two-term.** For every κ ≥ 2 and every
   prime p ≡ 1 (mod κ) with p ≥ 4κ⁴, a law-free Las Vegas κ-solver has arity
   **(a+1)^{⌈log₂κ⌉+1}**. The degree drops from κ (IS / Schedule 1H at odd κ) to
   ⌈log₂ κ⌉ + 1: 5 → 4, 7 → 4, 9 → 5, and in general κ → O(log κ). It is the 11-12 Lemma S/F
   calculus with K-weighted representations. An exact table gives every exception below 4κ⁴
   for κ ≤ 12 (§5). It is superseded by the triangular degree 2 wherever p ∉ E_2(κ), and for
   κ ≤ 9 by the R8 calculus. Its new content is uniformity in κ with a threshold polynomial in κ.
3. **Reductions, PROVED (§1).**
   - In the paper's regime, κ_d = p−1 (the case BIS_p) happens exactly at p = c+1, d = c.
   - At κ = 2 the regime contains p = 3, so a solver at arity f(a) uniform in p solves
     worst-case F_3^a subset sum with f(a) vectors. KOW §5.1 asks for even o(a²) there.
   - An exponent c independent of κ, uniform in p, would give BIS_q at n^c for every prime q.
     The best known (KMOSW Thm 1.11) has exponent q−1.
   - The IS collision step (thm:is-import) is the solution problem for P ∪ −P (Lemma C). So
     "a better collision step" is the same open problem at κ or κ/2.
4. **Barrier for approach (i), PROVED (Lemma W).** Suppose an algorithm's output entries always
   lie in a fixed finite set W ⊂ Z (small integers, i.e. lattice-short vectors). Then it fails on
   some bank whenever |W|^n < p^a. So it cannot have arity O_κ(a) uniformly in p. With
   W = {0, ±1} it is ternary SIS. The lattice experiments behave as predicted: BKZ succeeds
   exactly when small integers such as ±1, ±2, ±4 happen to be κ-th powers mod p (§6).

What stays open: arity o(a²) for arbitrary banks at any fixed κ ≥ 2 uniformly in p, and
a^{O(1)} with exponent independent of κ at primes p < 4κ⁴. The core's open problem (1) is
unchanged.

## 1. Problem, regimes and reductions

**(1a) The regime the paper needs.** At grade d of thm:main, κ = κ_d = gcd(d, p−1) ≤ d ≤ c with
c fixed; p ranges over **all** primes p > c (p near c, and p of cryptographic size, are both
allowed). The label dimension is a = g_d ≤ m, polynomial in the input, and the input size is
poly(a, n, log p). The exponent of m in thm:main is a max over all p > c of the arity degrees.
So a degree bound counts only if it holds at every prime p > c, or has a fallback with the same
degree at the remaining primes.

**(1b) κ = p − 1 is BIS_p, and it occurs once per c (PROVED).** If κ = p−1, then P = {1},
P0 = {0,1}, and SDE is homogeneous binary SIS mod p: a nonempty zero-sum subsequence of a
sequence in F_p^a (BIS_p of GKSZ Def. 6.1; existence at n ≥ (p−1)a+1 by Olson). In the regime,
κ_d = p−1 forces p−1 | d ≤ c < p, so p − 1 = d = c. So BIS_p arises only at p = c+1, grade
d = c (core rem:zero-sum example: p = 5, d = 4). In particular **(κ, p) = (2, 3) is in the regime
(c = 2)**, and there SDE is worst-case F_3^a subset sum.

*Consequence (PROVED, trivial embedding).* A solver at κ = 2 of arity f(a) that works at every
prime solves F_3^a subset sum with f(a) vectors. Known (repo lit note 11-07, verified sources):
- (a+1)(a+2)/2: ISS Claim 1, KOW Thm 2.2;
- a²/3 + O(a log a): KOW Thm 1.2;
- a²/4 + O(a^{3/2}): repo 11-08, AI-refereed;
- KOW §5.1 asks for o(a²);
- KOMSW (2026) report that at n = Θ(a) every known attack is exponential, even on average;
  F_3^n subset sum at linear size is their candidate for quantum advantage.

So **uniform-in-p linear arity at κ = 2 is at least as hard as an open problem the field
considers hard.** The same embedding at κ = q−1 shows: a uniform a^c with c independent of κ
gives worst-case BIS_q at n^{c} for every prime q. KMOSW Thm 1.11 gives exponent q−1; no
exponent independent of q is known (lit note §1.1). This is evidence of difficulty, not hardness.

**(1c) Fixed p, large a.** Here κ | p−1 is bounded and P0 is a fixed finite subset of F_p. SDE is
"S-subset-sum over F_p^a" with S = P0, the KOW/KOMSW framework:
- existence threshold N(κ,a,p) ∈ [2a+1, κa+1] (rem:sde-worst-case(a));
- best polynomial counts are quadratic: (a+1)(a+2)/2 for p ∉ E_2(κ); (1−1/p)a²/2 + O(a log a)
  for κ = 2, 3 (repo Theorem C, 11-08/11-09); 0.24a² at p = 5;
- at the finitely many p ∈ E_2(κ), the L-level fallback has degree L* > 2.

**(1d) p growing, fixed κ.**
- P0 ⊇ {0,1}, so SDE reduces to BIS_p (any BIS_p solver is an SDE solver). But BIS_p needs
  n > a log₂ p even to exist (Lemma W), so this reduction never gives O_κ(a).
- Existence is near-linear: N(κ,a,p) ≤ (2 + O(log(κa)/log p))a, and N = 2a+1 for
  p > (2κ−2)^{4a+2} (repo 11-11 Theorem E).
- The promise version (solve whenever solvable) is Legendre/power-residue-PRF-hard up to
  n ≈ 2a − log_κ p (repo 11-08 Theorem H; rem:sde-subquadratic(b) at n = a+2).
- Padding cannot carry that hardness into the total regime (11-11 Prop. L*).
- At h = (p−1)/κ ∈ {1, 2} (κ growing with p, outside the paper's fixed-κ regime) SDE is
  binary/ternary SIS and is SIVP-hard on random banks (11-02 Prop. D, 11-11 P2, via GPV/MP13
  as recorded there; not rechecked).

**(1e) κ = 2 is not special for linear arity (REFUTED: "diagonalisation gives a + O(1)").**
- Existence already needs 2a+1. The bank of a dead pairs (e_j, −u e_j), u ∉ P, has 2a columns
  and no solution, because (x − u y)e_j = 0 with x, y ∈ P0 not both 0 forces u = x/y ∈ P.
  Chevalley–Warning gives 2a+1, so **N(2,a,p) = 2a exactly** at every odd p (PROVED; in the full
  version as rem:sde-worst-case(a); brute-force check `check_triangular.py` (D): dead banks
  unsolvable at p ≤ 13, a ≤ 3; every 3-column bank in F_p, and 9000 random 5-column banks in
  F_p², solvable).
- The forms Σ_i λ_{ij} x_i² are already diagonal. The difficulty is a common isotropic vector of
  a diagonal forms. Recursion through totally isotropic subspaces costs 2^{a+1}−1 variables,
  and the published underdetermined-MQ thresholds are about m(m+1)/2 (rem:sde-subquadratic(c)).
- **In the core**, κ = 2 is Schedule 1H's plan (1,F1): A_2(a) = (a+1)², degree 2
  (rem:kappa-two). The core says Schedule 1H never reaches O(a) at κ ≥ 2. It does not use the
  triangular (a+1)(a+2)/2 (ISS Claim 1, full version) or Theorem C's (1−1/p)a²/2 + O(a log a).

## 2. Lemma C: the collision step is the solution problem for P ∪ −P (PROVED)

**Statement.** Let P' = P ∪ (−P).
- The output of IS Theorem 11 (disjoint I ≠ ∅, J and γ with Σ_I γ_i^κ v_i = Σ_J γ_j^κ v_j)
  gives the P'-solution x_i = γ_i^κ (i ∈ I), x_j = −γ_j^κ (j ∈ J).
- Conversely, a P'-solution x gives a collision with I = {x_i ∈ P}, J = {x_i ∈ −P ∖ P}. When
  J = ∅ or I = ∅, it gives a P-solution after a sign.
- P' = P iff −1 ∈ P iff h is even (always the case for odd κ). Otherwise P' = P_{κ/2}.

*Proof.* Rearrange the identity. −P = P iff −1 ∈ P. If −1 ∉ P, then κ is even and −1 =
g^{κh/2} ∈ P_{κ/2} ∖ P, so P ∪ −P = P_{κ/2}. ∎

**Consequences.**
- When h is even, t_{p,κ} = 2 and lem:rounds is one collision call, which is already a
  κ-solution.
- When h is odd, every collision is a κ/2-solution. lem:rounds is then plan (L, F0) of Schedule
  1H with the IS collision as its κ/2-node. This is cor:hcd(i), so it is already in the core.
- So "a better collision step" (brief item (iii)) is exactly a better κ- or κ/2-solver. The
  multiplicative round structure G^L is the product composition of Theorem HC (11-12 note). Any
  plan made of node calls on disjoint blocks has arity equal to the product of the node arities.
  Every node at degree ≥ 2 and every F1 finish has arity ≥ a+1, so any such plan with a stage
  has arity ≥ (a+1)² (rem:kappa-two).
- Check (`check_triangular.py` (C)): collision-solvable equals P'-solvable on 780 random tiny
  banks (p ≤ 29, κ ∈ {2,3,4,6}), 780/780.

## 3. The three constructive approaches

| approach | outcome | best arity obtained | status |
|---|---|---|---|
| (i) lattice / LLL–BKZ on {x ∈ Z^n : Λx ≡ 0} | works only when small integers are κ-th powers; no uniform guarantee | none uniform; heuristically n ≈ a log_{|W|} p with W = P0 ∩ [−B,B] | REFUTED as an O_κ(a) route (Lemma W, §6) |
| (ii) sumsets of P (Cauchy–Davenport, two-term Weil) | sumsets turn coset unions into free lines; gives Lemma D | (a+1)^{⌈log₂κ⌉+1} at p ≥ 4κ⁴ | PROVED given lem:two-term (§5); not below (a+1)² |
| (iii) recursive splitting / better collision | the collision is the κ' problem (Lemma C); product composition forces (a+1)²; additive (triangular) composition gives (a+1)(a+2)/2 with Lemma K at κ = 3 | (a+1)(a+2)/2 at κ ∈ {2,3} at every prime | PROVED (§4) |

Below a²/2 the known routes are:
- sparse dependencies: (1−1/p)a²/2;
- Rado-flat steering: O(a²/log a) at p ≳ a⁶ (11-07 Theorem A).

Below that, the piece-scheme barrier Θ(a²/log a) applies (11-07 B, argued/proved for its class),
and so does the "one circuit gives one dimension" bound (rem:sde-subquadratic(a)). This pass
found no way around either. One fresh variant of (iii) was considered and rejected (ARGUED):
manufacturing objects that lie in a prescribed low-dimensional subspace mod U, to get circuits
shorter than codim+1. That needs a homogeneous solve of the quotient problem of dimension a − w
for each such object, so it composes multiplicatively again.

## 4. Lemma K: explicit two-level contractions at κ = 2, 3 (PROVED)

A universal two-level contraction (normalised as in prop:triangular-sde) is (α, β) ∈ F_p^κ × F_p^κ
with α_0 = 1, β_0 = 0 and α_j + β_i ∈ C_{−(i+j)} ∪ {0} for all i, j ∈ Z_κ.

**(i) κ = 2, every odd p.** Let ν be the least quadratic non-residue in [2, p−1]. Then ν − 1 is
a nonzero square, by minimality, since 1 is a square. Take α = (1, 0), β = (0, ν−1): the four
values are 1, 0, ν, ν−1, in classes 0, –, 1, 0 as required. This is the contraction of
lem:coherent-quadratic-sde in the full version.

**(ii) κ = 3, every p ≡ 1 (mod 3).** Take b ∈ C_1 with 1 + b ∈ C_2, and α = (1, 0, −b),
β = (0, b, −1). Since −1 = (−1)³ ∈ P, the nine values α_j + β_i are:

| (i,j) | value | required class C_{−(i+j)} | holds because |
|---|---|---|---|
| (0,0) | 1 | C_0 | |
| (0,1) | 0 | — | zero allowed |
| (0,2) | −b | C_1 | −1 ∈ P |
| (1,0) | 1+b | C_2 | choice of b |
| (1,1) | b | C_1 | choice of b |
| (1,2) | 0 | — | |
| (2,0) | 0 | — | |
| (2,1) | −1 | C_0 | −1 ∈ P |
| (2,2) | −1−b | C_2 | −1 ∈ P |

The construction is the "zero-diagonal" form β_i = −α_{i+1}: α_j − α_k ∈ C_{1−j−k} for j ≠ k.

*Existence of b.* N = #{x ∈ C_1 : 1+x ∈ C_2}. With χ the cubic character, χ(g) = ω:

9N = Σ_{s,t∈Z_3} ω^{−s−2t} Σ_{x≠0,−1} χ^s(x)χ^t(1+x).

- The (0,0) term is p − 2.
- The four terms with exactly one of s, t zero have modulus 1 (χ(−1) = 1).
- (s,t) = (1,2) and (2,1) are J(χ^s, χ^{−s}), of modulus 1.
- (1,1) and (2,2) are Jacobi sums of modulus √p.

So 9N ≥ p − 8 − 2√p > 0 for p ≥ 19. At p = 7 and 13, direct counting gives N = 1. Exactly,
N = (1,2)_3 = (p+1+L)/9 with 4p = L² + 27M², L ≡ 1 (mod 3) (Gauss). Swapping the generator
swaps C_1 and C_2, but (2,1)_3 = (1,2)_3. ∎

*Checks.*
- `check_contractions.py 30000` → `check_contractions.out`: every odd prime ≤ 30000 (κ = 2, 3244
  primes) and every p ≡ 1 (mod 3) ≤ 30000 (κ = 3, 1610 primes) gives a contraction that passes
  all κ² conditions; the count equals (p+1+L)/9 at all 1610 primes; min N/p = 1/13.
- `check_triangular.py 1` → `check_triangular.out`: an independent implementation of
  prop:triangular-sde, from its proof, with these contractions on exactly (a+1)(a+2)/2 columns.
  It ran at every prime p ≤ 101 with κ ∈ {2,3} dividing p−1, every a ≤ 6, 4 repetitions, on six
  bank families (random, low rank, proportional by non-κ-th powers, a dead pairs plus filler,
  zero columns, sparse). 5184 runs, 0 failures; every output re-verified (κ-th powers by
  Euler's criterion, sum zero).

**Consequence for the core (PROVED given prop:triangular-sde; AI-checked here, not adopted
anywhere).**

| κ | core (Schedule 1H) | with Lemma K + triangular |
|---|---|---|
| 2 | (a+1)² | (a+1)(a+2)/2, deterministic given ν |
| 3 | G(3,a) = 27(a+1)³ (t = 2, L = 1) | (a+1)(a+2)/2 at every prime |
| 6, p ≥ 4·6⁴ (halving over κ = 3) | degree e_3 + 1 = 4 | degree 3, so the halving rule gains one |

The κ = 3 node is deterministic given b and a cubic non-residue g; both come from O(p) tables at
small p, or Las Vegas with success probability ≥ 1/13 and 2/3 per draw. The roots of the output
weights need Las Vegas cube roots, as in Schedule 1H. Whether this lowers E_H(9) = 38 is a
question for the R8 calculus, which already uses κ = 3 relations. At the maximising primes of
the R8 rule (13, 19, 37, 73) the κ = 3 grade is not binding, so no headline claim is made here.

## 5. Lemma D: the coset-doubling tower (PROVED given lem:two-term)

**Setting.** For a union K = ∪_{ν∈A} C_ν (A ⊆ Z_κ, P-stable):
- a K-solution is x ≠ 0 with Σ x_i λ_i = 0 and every nonzero x_i in K;
- a K-rep of v is a support with K-weights and value v.

Choose shifts e_1, ..., e_m with A_1 = {0}, A_{j+1} = A_j ∪ (A_j + e_j) and A_{m+1} = Z_κ.
Let K_j = ∪_{A_j} C_ν, and c_j = −g^{−e_j}.

**Lemma D.** Suppose P0 + c_j P0 ⊇ F_p^× for every j. Then there is a K_1 = P solver of arity
(a+1)^{m+1}, Las Vegas, with expected time poly(a^{m+1}, log p) for fixed κ.

At p ≥ 4κ⁴ the hypothesis holds for every c (core lem:two-term), and e_j = 2^{j−1} gives
m = ⌈log₂ κ⌉. So the arity is (a+1)^{⌈log₂κ⌉+1}.

*Proof.* Induct downward on the level.
- K_{m+1} = F_p^×: Gaussian elimination on a+1 columns.
- Step from K_{j+1} to K_j: run the K_{j+1}-solver on a+1 disjoint blocks. Split each output
  into I = {x_i ∈ K_j} and J (the rest, so x_i ∈ g^{e_j}K_j).
  - If J = ∅, or I = ∅ after dividing by g^{e_j}, this is already a K_j-solution.
  - Otherwise u = Σ_I x_i λ_i has a K_j-rep, and Σ_J (x_i/g^{e_j}) λ_i = c_j u is a K_j-rep of
    c_j u: an object of type (1, c_j).
- Finish F1 with the a+1 vectors u_ν. Gaussian elimination gives η ≠ 0 with Σ η_ν u_ν = 0.
  Write each η_ν ≠ 0 as y_1 + c_j y_2 with y_1, y_2 ∈ P0. Scale the two reps by y_1 and y_2
  (K_j·P = K_j). The union is a nonempty K_j-solution on disjoint supports.
- Arities multiply: (a+1) per level.
- Final weights lie in P. Roots come from Las Vegas root finding, and the two-term draws succeed
  with probability ≥ 1/(2κ), both as in Def. schedule1h. ∎

This is Lemma S/F and Theorem HC of the 11-12 note (`2026-11-12-rees-exponent-k8-attack.md`),
with {0,m}-nodes replaced by (K ∪ (K+e))-nodes and P-reps by K-reps. The proofs are word for word
the same. No priority claim.

**Degrees at p ≥ 4κ⁴.**

| κ | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 16 | 2^r | odd prime κ |
|---|---|---|---|---|---|---|---|---|---|---|
| IS/S1 (h even) | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 16 | 2^r | κ |
| core 1H ê(κ) | 3 | 3 | 5 | 4 | 7 | 4 | 9 | 5 | r+1 | κ |
| Lemma D | 3 | 3 | 4 | 4 | 4 | 4 | 5 | 5 | r+1 | ⌈log₂κ⌉+1 |
| triangular (p ∉ E_2(κ)) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

Lemma D adds to the full version in one window: 4κ⁴ ≤ p where p ∈ E_2(κ) is possible and the
chains do not apply. The chains (cubic) need p ≳ κ²(ln κ)^κ; the largest elements of E_2(κ)
lie near κ^{(κ+1)/2}. In that window the uniform degree drops from κ to ⌈log₂κ⌉+1. For the
class-c exponent this shrinks the range of primes with degree above O(log c) per grade to
p < 4c⁴, polynomial in c. For κ ≤ 9 the R8 calculus of the k9-bottleneck note already does at
least as well at every prime it lists (for example 4 at 127, 181, 433, where Lemma D gives 5).

**Exact small primes** (`tower.py coverage 12 0` → `tower_coverage.out`). For each κ ≤ 12 and
every prime p ≡ 1 (mod κ) below 4κ⁴, the exact minimal m* comes from a BFS over coset unions,
with the per-level test computed exactly through P-invariance (cross-checked against the full
sumset table below 3000). Results: the doubling degree ⌈log₂κ⌉+1 holds at every prime p ≡ 1 (mod κ) except those listed
(— = no tower plan at all; otherwise the larger exact m*+1).

| κ | primes < 4κ⁴ checked | exceptions (p: degree) | largest exception |
|---|---|---|---|
| 2, 3 | 17, 30 | none | — |
| 4 | 83 | 5: —, 13: —, 29: 4 | 29 |
| 5 | 89 | 11: — | 11 |
| 6 | 340 | 7, 13, 19, 31, 43: — | 43 |
| 7 | 195 | 29: —, 71: —, 43: 7 | 71 |
| 8 | 464 | six primes ≤ 137: —, 233: 5, 761: 5 | 761 |
| 9 | 480 | 19, 37, 73: —, 109: 9, 163: 9 | 163 |
| 10 | 1044 | 8 with —, 6 with degree 6 or 10, largest 331 | 331 |
| 11 | 586 | 23, 67, 89: —, 199: 11, 419: 6 | 419 |
| 12 | 1996 | 12 with —, 3 with degree 6, largest 541 | 541 |

So for κ ≤ 12, Lemma D gives (a+1)^{⌈log₂κ⌉+1} at every prime p ≡ 1 (mod κ) above
29, 11, 43, 71, 761, 163, 331, 419, 541 (κ = 4..12). That is below 15κ² in each case: an exact
finite computation below 4κ⁴, plus lem:two-term above. The κ = 9 exceptions 19, 37, 73 are the
R8 binding primes. There the R8 calculus does better (degrees 6, 5, 5), so Lemma D adds nothing.

`tower.py run 3` → `tower_run.out`: the solver itself was run on random, proportional-heavy and
sparse banks at the full arity (a+1)^{m*+1} at 16 (κ, p) pairs, including p ≥ 4κ⁴ for
κ = 3, 5, 7, 9 (p = 331, 337, 2521, 9661, 26263). 192 runs, 0 failures; every output
re-verified. A first version mis-scaled the two-term decomposition (it used the table for
g^{cos c} instead of c). The checks caught it (69 failures), and it was fixed before the runs
reported here.

## 6. Approach (i): lattices, and the restricted-output barrier

**Lemma W (PROVED).** Let W ⊂ Z be finite and let an algorithm output, on every bank, a solution
with all entries in W (read mod p). If |W|^n < p^a, the algorithm fails on some bank in
F_p^{a×n}. More precisely, at most a (|W|^n − 1)/p^a fraction of banks have any nonzero
W-solution.

*Proof.* A fixed x ≢ 0 (mod p) lies in the kernel of exactly p^{a(n−1)} matrices. Sum over the
fewer than |W|^n candidate vectors. ∎

So the arity of a restricted-output solver is ≥ a log_{|W|} p, which is not O_κ(a) uniformly in
p. W = {0,1} gives BIS_p; W = {0,±1} gives ternary SIS (when −1 ∈ P), which on random banks at
n ≳ a log p is SIVP-hard by MP13 as recorded in 11-11 P2. A lattice-short vector has entries in
W = [−B, B] with (2B+1)^n ≳ p^a. For it to be a solution, every entry must lie in P0 ∩ [−B, B].
For worst-case p (2 ∉ P, −1 ∉ P) that set is only {0, 1, 4, 9, ...}-type perfect powers, and in
general it is a residuosity-pseudorandom set without additive structure (ARGUED; Burgess-type
equidistribution, not proved here).

**Experiment** (`lattice_probe.py 11` → `lattice_probe.out`; heuristic, random banks only). Setup:
BKZ-10 on the kernel lattice, then scan basis vectors and pairwise ± sums. Control: the same
number of uniform kernel vectors. 20 banks per cell.
- κ = 3, p = 31, a = 4, 6, n ≥ 2a+1: lattice 20/20, random 0/20. Here
  P ∩ [−10,10] = {±1, ±2, ±4, ±8} (`small_ints_in_P.out`).
- κ = 3, p = 97: lattice 0/20 in every cell, n ≤ 3a+1. Here P ∩ [−10,10] = {±1, ±8}.
- κ = 2, p = 101 (P ∋ ±1, ±4, ±5, ±6, ±9) and p = 31 (−1 ∉ P): lattice beats random
  (e.g. 6/20 vs 0/20 at a = 4, n = 13), but success falls with a (1/20 at a = 6, n = 19).
- (B1) κ = 2, p = 101, a = 2: binary solutions exist in 2/200 banks at n = 5 and 165/200 at
  n = 14, tracking (2^n − 1)/p², while CW guarantees a P0-solution at n = 5 in every bank.

So the lattice route exploits arithmetic accidents of P ∩ small integers. It gives no
worst-case or uniform statement. REFUTED as a route to O_κ(a); this matches 11-02 item 8.

## 7. Barriers (brief item 3)

- **B1 (PROVED) restricted outputs:** Lemma W.
- **B2 (PROVED reductions; difficulty, not hardness):** §1b. Uniform linear arity at κ = 2
  implies F_3^a subset sum at O(a) vectors, open even at o(a²) (KOW §5.1) and believed hard
  (KOMSW). A uniform κ-independent exponent implies BIS_q at n^c for every q, beyond KMOSW's
  q − 1.
- **B3 (PROVED in the cited repo notes, conditional on the PRF):** the promise problem is hard
  below about 2a − log_κ p (Theorem H, 11-08). Padding cannot reach the total regime (Prop. L*,
  11-11). So any near-linear algorithm must use totality in an essential way.
- **B4 (PROVED for the stated classes):**
  - product composition (Theorem HC / rem:kappa-two) forces ≥ (a+1)², and Lemmas C and D live
    there;
  - one circuit with a dependency meeting two cosets realises no plane (rem:sde-subquadratic(a)),
    so circuit-at-a-time schemes in general position need (a+1)(a+2)/2;
  - piece schemes need Θ(a²/log a) (11-07 B).
- **Not obtained:** a lower bound for a "generic linear algebra + κ-th-root oracle" model. In
  any honest version of that model χ = cos is computable (x ↦ x^h), so the model is all
  algorithms, and a superlinear lower bound would be an unconditional lower bound for a total
  search problem (rem:sde-worst-case(a)). Every restriction that makes it provable is one of
  B1–B4. UNKNOWN.

## 8. Item (4): best proved improvement over G(κ,a)^{⌈log₂ t⌉}

| κ | primes | arity | degree | status |
|---|---|---|---|---|
| 2 | every odd p | (a+1)(a+2)/2 (Lemma K(i) + prop:triangular-sde); (1−1/p)a²/2 + O(a log a) (repo Thm C) | 2 | PROVED given prop:triangular-sde (AI-checked, re-implemented here); Thm C AI-refereed |
| 3 | every p ≡ 1 (3) | (a+1)(a+2)/2 (Lemma K(ii)) | 2 (core: 3) | PROVED given prop:triangular-sde |
| any κ | p ≥ 4κ⁴ | (a+1)^{⌈log₂κ⌉+1} (Lemma D) | ⌈log₂κ⌉+1 | PROVED given lem:two-term |
| any κ | p ∉ E_2(κ) | (a+1)(a+2)/2 (full version) | 2 | AI-checked, pending human review |

Linear or a^{1+o(1)} arity: UNKNOWN for every κ ≥ 2 (no algorithm, no hardness).

Exponent independent of κ, uniformly in p:
- PROVED with degree 2 for κ ∈ {2, 3};
- PROVED for p ∉ E_2(κ) via the full version;
- otherwise UNKNOWN at the primes p < 4κ⁴ that are exceptional for both Lemma D and the
  triangular (BIS_q included).

## 9. Adversarial self-check

- *Is Lemma K new?* The full version already has E_2(3) = ∅. Lemma K only replaces its proof
  (T_A(3) plus three exhaustive searches) by a one-line contraction and a Jacobi-sum count. Its
  value is that a human can check it. The 2026-11-02 note says the κ ≥ 3 triangular is "a short
  combination of ISS with the repo's coset contraction". No priority claim.
- *Is Lemma K's table right?* The script checks all κ² conditions directly, at 1610 primes, and
  separately the count against Gauss's formula. The algebra uses only −1 ∈ P, which holds since
  κ = 3 is odd. The step that most needs a human eye is that the Jacobi-sum error has exactly
  six unit terms and two √p terms.
- *Does Lemma D really give K_j-weights?* The J-weights divided by g^{e_j} lie in K_j because
  J ⊆ g^{e_j}K_j by the choice of A_{j+1}. The overlap case (a weight in both K_j and
  g^{e_j}K_j) is sent to I. The F1 scaling uses y ∈ P0 only. The bug found in testing was in the
  implementation (decomposition table), not the lemma; after the fix, 192/192 runs pass,
  including p ≥ 4κ⁴. Still, the finite runs only falsify.
- *Is Lemma D subsumed?* For κ ≤ 9, yes, by the R8 calculus at every prime examined there. For
  2-power κ it equals Schedule 1H. Its only claim is the uniform-in-κ statement at p ≥ 4κ⁴. The
  full version's prime-factor tower has degree Ω(κ)+1 (Ω = number of prime factors with
  multiplicity), which is smaller for smooth κ, at threshold κ^{q_1+O(1)}. Lemma D wins for κ
  prime or with a large prime factor.
- *Reductions §1b:* the embedding is literal (κ = p−1 makes P0 = {0,1}). The claim that
  KOW/KOMSW consider linear-size F_3 subset sum hard rests on the repo's 11-07 literature note
  (sources read there), not re-read here.
- *Lemma W* is a counting statement over random banks. It says nothing about algorithms whose
  outputs use large field elements, which is exactly why it is only a barrier for approach (i).
- *Lattice experiments:* 20 random banks per cell, a ≤ 6. Average case only.
- *What could falsify the verdict:* a poly-time algorithm at o(a²) arity for arbitrary banks at
  fixed κ uniformly in p. None was found here or in ten earlier passes. The verdict is the
  absence of such an algorithm, not a proof that none exists.

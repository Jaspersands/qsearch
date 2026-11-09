# Two-level SDE threshold, round 8: local obstructions, the coloured-clique family, and the constant 1.5

5 November 2026 (overnight pass). AI-only research pass, not a human review, not a Lean proof,
not a priority claim. **"AI-checked, pending human review" applies to every claim below.**

Labels: **[proved]** full proof written here; **[computed]** complete finite computation (script
named; cross-checks named); **[cited]** proved in an earlier report or the appendix;
**[conjecture]** heuristic or model statement.

Scripts and outputs: `2026-11-05-rees-threshold-8/` (interpreter `/opt/anaconda3/bin/python`;
all runs under `nice -n 10`, at most two processes at a time). Notation as in
`docs/papers/rees-hsp/appendix-schedule2.tex`: p prime, κ | p − 1, h = (p−1)/κ, ξ a coset
generator, Q_m = ξ^m Q_0, Q°_m = Q_m ∪ {0}, ind(x) the coset index, ε = ind(−1)
(ε = 0 iff −1 ∈ Q_0), and a two-level contraction is (α, β) ∈ F_p^κ × F_p^κ with
α_0 + β_0 ≠ 0 and α_j + β_i ∈ Q°_{−(i+j)} for all i, j ∈ Z_κ. C_{ij} = z_i z_j(α_j + β_i).
TH2, …, TH7 are the earlier threshold reports (`2026-11-02-rees-threshold-2.md`, …,
`2026-11-05-rees-threshold-7.md`).

## 0. Verdict

- **Goal (A), a proved quadratic-arity threshold well below T_A: not reached.** Nothing here
  lowers the proved two-level threshold min(T_A, T_C) = κ^{κ+o(1)}. The square gap stays open.
- **Goal (B), an explicit infinite family in E_2(κ) above κ^{(κ+1)/2}: not reached.**
  - What is proved (Proposition 6): any certificate that p ∈ E_2(κ) obtained by restricting
    to r rows (or r columns) is void once p ≥ ((r−1)κ^r + 2)².
  - So a certificate near κ^{(κ+1)/2} needs r ≥ (κ+1)/4 − log_κ r rows.
  - Proposition 6 does not exclude a structured certificate with r ≈ κ/4 rows.
- **What is new and proved.**
  1. *Zero cells (Theorem 1).* A contraction has at most κ zero cells. It has exactly κ iff
     −1 ∈ Q_0 and it is a member of TH2's coloured-clique family with some shift c ≠ 0.
     That family is nonempty, for one shift or for all, iff there are y_m ∈ Q_m (m ≠ 0)
     with all pairwise differences in Q_0 (a "transversal clique"). This is the exact
     statement behind the interrupted pass's `clique.py`.
  2. *Two-row obstruction (Theorem 2, Corollary 3; elementary and likely classical in
     cyclotomy).* A contraction forces
     Q°_0 − Q°_b ⊇ F_p^× for every b ≠ 0. Equivalently, p ∈ E_2(κ) as soon as one cyclotomic
     number A(u, v) = #{w ∈ Q_u : w − 1 ∈ Q_v} with u ≠ 0, v ≠ ε, u ≠ v vanishes.
     **Every prime p ≡ 1 (mod κ) with p ≤ κ² − 3κ + 3 lies in E_2(κ)** (pigeonhole). The
     criterion is vacuous above about κ^4 (Weil).
  3. *Coprime divisors (Lemma 5).* If D | κ and gcd(D, κ/D) = 1, then E_2(D) ∩ {p ≡ 1 (mod κ)}
     ⊆ E_2(κ).
  4. *Locality barrier (Proposition 6)*, as above.
- **Computed [computed].**
  - The complete two-row exceptional sets E2row(κ) ⊆ E_2(κ) for 3 ≤ κ ≤ 16, from two
    independent codes for κ ≤ 9. They are consistent with every E_2 datum in the repo, and
    they contain every prime at which TH7's chains fail.
  - Complete `dfs2b` decisions for κ = 10..16 on small ranges, re-decided by TH7-check's
    independent `rcdfs.c`. They give the first exact E_2 data for κ ≥ 10. For example, every
    prime p ≡ 1 (mod 10) below 3361 lies in E_2(10), and 3361 does not (§3.3).
  - The coloured-clique (P) family is decided for κ = 4..9 by `clique.py`. It agrees with the
    κ = 9 sweep's independent P search on all 168 primes of (20000, 30000], and with a third,
    brute-force search on 384 primes.
- **Heuristic [conjecture].** The Poisson model with orbit size 2κ² and *no fitted constant*
  predicts max E_2(κ) ≈ 1.47–1.57·κ^{(κ+1)/2} for κ = 5..10. The observed values are
  1.34–1.66 for κ = 4..7. So the constant 1.5 of the observed law is what the model predicts.
  The model also predicts that the ratio falls to 1 slowly (1.34 at κ = 16, 1.29 at κ = 20).
  Below about κ^4 the cyclotomic graph is far from random: at κ = 9, transversal cliques occur
  at 45 of 540 primes below 3·10^4, where the uniform model expects about 10^{−9}..10^{−2} per
  prime (§3.4). Per-prime predictions are unreliable there.

## 1. The interrupted pass: what it was doing, and what is reused

The previous agent (stopped by an API error, no report) had:

- `clique.py`: a complete bitset DFS for "transversal cliques" y_1, …, y_{κ−1}, y_i ∈ Q_i,
  y_i − y_k ∈ Q_0 (−1 ∈ Q_0 required). It maps each clique to a contraction with κ zero cells
  and re-checks all κ² cells with pow(). Outputs `clique_k{4..9}.out`; witnesses re-verified in
  `verify_cliques.out` (2597 lines, bad = 0, all with zero cells, as they must be).
- `crosscheck_clique.py`: an independent plain recursion. It is now finished:
  κ = 4..7 agree on 311 primes (`crosscheck_clique.out`); κ = 8 (p ≤ 2000) and κ = 9
  (p ≤ 1600) agree on 34 + 39 primes (`crosscheck_clique_k8k9.out`, run in this pass).
- `heuristic.py`: a Poisson model with a constant c fitted per κ (unstable: c = 0.67 … 13.1).
  It is superseded by `heuristic2.py` (§4), which fixes c = 1.
- `probe_mobius.py`, `mobius_sym.py`: stabilisers in PGL_2(F_p) of the κ-point set
  {∞} ∪ Y of κ = 9 cliques. They are exploratory. They show no single symmetry type
  (orders 1, 2, 3, 6, 8; 29 of 45 trivial), and they are not used below.
- `compare_e2.py`, `undecided.py`: bookkeeping against the dfs2/dfs2b data.

The clique family is TH2 §3.4's coloured-clique family and TH5's "P" ansatz; the κ = 9 sweep
already used it as a fallback certificate. The interrupted pass had apparently set out to
prove a threshold by a second-moment count over cliques. That cannot beat exponent κ: in the
clique system the last unknown still faces κ − 1 coset conditions (TH5 §3.4's sequential
barrier, unchanged by the zero cells). This pass therefore reuses its code and data, proves the
statement the code relies on (Theorem 1), and turns to what can be proved: obstructions.

## 2. Proved results

Throughout, (α, β) is a two-level contraction at (p, κ), κ ≥ 2.

**Lemma 0 (distinct entries) [cited: TH5 Lemma 2.1; proof repeated].** The β_i are pairwise
distinct, and so are the α_j.
*Proof.* If β_i = β_k with i ≠ k, then for each j the cell value α_j + β_i lies in
Q°_{−(i+j)} ∩ Q°_{−(k+j)} = {0}, so α_j = −β_i for all j. Row 0 then has the single value
α_0 + β_0 = β_0 − β_i in every Q°_{−j}, so it is 0 (κ ≥ 2), contradicting α_0 + β_0 ≠ 0.
Columns are symmetric. ∎

### 2.1 Zero cells and the coloured-clique family

**Theorem 1 [proved].** Let κ ≥ 3.
1. Every row and every column of C has at most one zero cell, and C_00 ≠ 0. Hence C has at
   most κ zero cells.
2. If C has exactly κ zero cells, then ε = 0 (that is, −1 ∈ Q_0), and there is c ∈ Z_κ \ {0}
   with zero cells exactly at (j + c, j), j ∈ Z_κ. Then α_j = −β_{j+c} and
   (P_c)  β_i − β_k ∈ Q_{c−(i+k)} for all i ≠ k.
   Conversely, if β has distinct entries and satisfies (P_c) for some c ≠ 0, then
   α_j := −β_{j+c} gives a contraction with exactly κ zero cells.
3. For any fixed c ≠ 0, (P_c) has a solution iff ε = 0 and there are y_m ∈ Q_m,
   m ∈ Z_κ \ {0}, with y_m − y_{m'} ∈ Q_0 for all m ≠ m' (a *transversal clique*). In
   particular solvability of (P_c) does not depend on c.

*Proof.* (1) A zero at (i, j) and at (k, j) with i ≠ k gives β_i = −α_j = β_k, against
Lemma 0; columns likewise. C_00 ≠ 0 by definition.

(2) By (1), the κ zeros form a permutation matrix. Let σ(j) be the row of the zero in
column j, and τ = σ^{−1}. Then α_{τ(k)} = −β_k for every k. Let i ≠ k. The cells (i, τ(k)) and
(k, τ(i)) are not zero (their zero rows are k and i). Their values are β_i − β_k and
β_k − β_i. So
ind(β_i − β_k) ≡ −(i + τ(k)) and ind(β_k − β_i) ≡ −(k + τ(i)).
Since β_k − β_i = −(β_i − β_k), the second index is ε + the first. With f(i) = i − τ(i),
this reads f(i) − f(k) ≡ ε for all ordered pairs i ≠ k. Exchanging i and k gives 2ε ≡ 0. For
three distinct i, k, l (here κ ≥ 3 is used), f(i) − f(l) = (f(i) − f(k)) + (f(k) − f(l))
gives ε ≡ 2ε, so ε ≡ 0. Then f is constant, say c, so τ(i) = i − c and σ(j) = j + c, and
c ≠ 0 because C_00 ≠ 0. The cell conditions for i ≠ k become β_i − β_k ∈ Q_{−(i+k−c)}, which is
(P_c). Conversely, with α_j = −β_{j+c}, cell (i, j) is β_i − β_{j+c}. It is 0 iff i = j + c,
and otherwise it lies in Q_{c−i−(j+c)} = Q_{−(i+j)} by (P_c). Cell (0,0) is β_0 − β_c ≠ 0.

(3) Let β solve (P_c). Since (P_c) involves only differences, we may translate so that
β_c = 0. Applying (P_c) to both orders of a pair forces ε = 0, as in (2). For m ≠ 0,
β_{m+c} = β_{m+c} − β_c ∈ Q_{c−(m+c)−c} = Q_{−m−c} is nonzero. Put
y_m = (ξ^c β_{m+c})^{−1} ∈ Q_m. For m ≠ m',
y_m − y_{m'} = (β_{m'+c} − β_{m+c}) / (ξ^c β_{m+c} β_{m'+c}).
The numerator lies in Q_{c−(m+c)−(m'+c)} = Q_{−m−m'−c}, and the denominator in
Q_{c+(−m−c)+(−m'−c)} = Q_{−m−m'−c}. So the quotient lies in Q_0. Conversely, given a
transversal clique and ε = 0, put β_c = 0 and β_{m+c} = (ξ^c y_m)^{−1}. The same computation,
read backwards, gives (P_c) on pairs avoiding c. For pairs (m + c, c),
β_{m+c} − 0 ∈ Q_{−m−c} = Q_{c−(m+c)−c}, and the reverse order holds because ε = 0. The β's are
distinct: β_{m+c} ≠ 0 = β_c, and y_m ≠ y_{m'}. ∎

*Remarks.*
- For c = 1 and ξ = g, (3) is exactly `clique.py`'s map β_i = 1/(g y_{i−1}) (i ≠ 1), β_1 = 0,
  α_j = −β_{j+1}. So a NOCLIQUE verdict of `clique.py` means that **no contraction with κ zero
  cells exists**, for any shift.
- TH5 Theorem 2.4 obtained the same family as the transpose-symmetric ansatz with λ = −1.
  Theorem 1 adds the converse: every contraction with the maximal number of zero cells is of
  this form.
- Writing v_i = λ_i(β_i, 1) with ind λ_i = i + const, (P_c) says that the κ vectors
  v_i ∈ F_p² have all pairwise determinants in one fixed coset. So the family is
  SL_2(F_p)-invariant, and it is an orbit-counting problem on κ-point configurations of P^1.
  This is noted only. It gave nothing provable below κ^κ, because the last point still faces
  κ − 1 conditions.

### 2.2 Two rows: a cyclotomic obstruction

**Theorem 2 [proved].** If a two-level contraction exists at (p, κ), then for all distinct
i, k ∈ Z_κ,
  Q°_{−i} − Q°_{−k} ⊇ F_p^×,
and in particular S_b := Q°_0 − Q°_b ⊇ F_p^× for every b ∈ Z_κ \ {0}. The same holds with
columns in place of rows.

*Proof.* Let d = β_i − β_k. It is nonzero by Lemma 0. For each column j,
d = (α_j + β_i) − (α_j + β_k) ∈ Q°_{−(i+j)} − Q°_{−(k+j)} = ξ^{−j}(Q°_{−i} − Q°_{−k}),
since Q°_{m−j} = ξ^{−j}Q°_m. So ξ^j d ∈ S := Q°_{−i} − Q°_{−k} for every j ∈ Z_κ. Also
Q_0 S = S, because Q_0 Q°_m = Q°_m. Hence S contains ∪_j ξ^j d Q_0 = F_p^×. Multiplying by
ξ^i gives S_{i−k} ⊇ F_p^×, and b = i − k runs over all nonzero residues. For columns use
α_j − α_l = (α_j + β_i) − (α_l + β_i). ∎

**Corollary 3 (cyclotomic criterion) [proved].** Put A(u, v) = #{w ∈ Q_u : w − 1 ∈ Q_v} and
𝒫 = {(u, v) ∈ Z_κ² : u ≠ 0, v ≠ ε, u ≠ v}.
1. ∀ b ≠ 0: S_b ⊇ F_p^×  ⟺  A(u, v) ≥ 1 for all (u, v) ∈ 𝒫. Hence, **if A(u, v) = 0 for
   some (u, v) ∈ 𝒫, then p ∈ E_2(κ)**. This holds for any choice of the coset generator ξ.
2. **Every prime p ≡ 1 (mod κ) with p ≤ κ² − 3κ + 3 lies in E_2(κ).**
3. If p − 2 > (κ−1)(κ−2)√p + 3(κ−1), then every A(u, v) ≥ 1, so the criterion never applies.
   This happens for all p ≥ W_2(κ), the least such integer; W_2(κ) < ((κ−1)(κ−2) + 2)² for
   κ ≥ 4 (not for κ = 2, 3: W_2(3) = 17); W_2(4) = 56, W_2(8) = 1810,
   W_2(16) = 44194.

*Proof.* (1) Fix b ≠ 0 and z ∈ Q_c. There are three ways to write z = x − y with
x ∈ Q°_0 and y ∈ Q°_b.
- x = 0 works iff −z ∈ Q_b, that is iff c ≡ b − ε.
- y = 0 works iff z ∈ Q_0, that is iff c ≡ 0.
- x, y ≠ 0: write x = zw with w ∉ {0, 1}. Then x ∈ Q_0 iff w ∈ Q_{−c}, and
  y = z(w−1) ∈ Q_b iff w − 1 ∈ Q_{b−c}. So this works iff A(−c, b−c) ≥ 1.

Membership of z depends only on c, since Q_0 S_b = S_b. So S_b ⊇ F_p^× iff A(−c, b−c) ≥ 1
for every c ∉ {0, b − ε}. The substitution (u, v) = (−c, b − c) is a bijection from pairs
(b, c) with b ≠ 0 onto pairs with u ≠ v. Under it, c ≠ 0 ⟺ u ≠ 0 and c ≠ b − ε ⟺ v ≠ ε.
This proves the equivalence, and the implication follows from Theorem 2. Nothing used the
choice of ξ.

(2) Every w ∈ F_p \ {0, 1} is counted by exactly one A(u, v), so Σ_{u,v} A(u, v) = p − 2.
Count 𝒫 by inclusion–exclusion on the three excluded lines u = 0, v = ε and u = v. For
ε = 0 they meet only in (0, 0), so |𝒫| = κ² − (3κ − 2) = (κ−1)(κ−2). For ε ≠ 0 they meet
pairwise in three distinct points, so |𝒫| = κ² − 3κ + 3. If all A on 𝒫 were ≥ 1, then
p − 2 ≥ |𝒫| ≥ (κ−1)(κ−2). So p ≤ (κ−1)(κ−2) + 1 = κ² − 3κ + 3 forces a zero on 𝒫.

(3) As in the proof of `lem:app-s2-cyclo`, κ²A(u, v) = Σ_{s,t} ω^{−us−vt}K(s, t), with
K(s, t) = Σ_{w≠0,1} χ^s(w)χ^t(w−1). The values are:
- K(0, 0) = p − 2;
- K(s, 0) = −1 and K(0, t) = −χ^t(−1) for s, t ≠ 0;
- K(s, −s) = −1 for s ≠ 0, because w ↦ w/(w−1) permutes F_p \ {0, 1};
- |K(s, t)| ≤ √p on the (κ−1)(κ−2) pairs with s, t, s + t ≠ 0, by the Weil bound for
  X^s(X−1)^t (two distinct roots), as in that lemma.

So |κ²A(u, v) − (p−2)| ≤ 3(κ−1) + (κ−1)(κ−2)√p. ∎

**Remark (exactness).** Corollary 3(1) is also an exact description of a sub-problem. The
two-row system "β_0 = 0, β_b ≠ 0, α_j + β_i ∈ Q°_{−(i+j)} for i ∈ {0, b} and all j, and
α_0 ≠ 0" has a solution iff S_{−b} ⊇ F_p^×. (Take β_b = −d. Column j needs d ∈ ξ^{−j}S_{−b}.
Column 0 is met by α_0 = d ∈ Q_0 when d ∈ Q_0.) So E2row(κ) := {p : some A on 𝒫 vanishes} is
exactly the set of primes at which some two-row restriction of the problem is infeasible.

**Lemma 4 (h = 1) [proved].** For κ ≥ 4 with κ + 1 prime, p = κ + 1 ∈ E_2(κ). This is the
case p ≤ κ² − 3κ + 3 of Corollary 3(2). Directly: with h = 1 every A(u, v) is 0 or 1 and
Σ A = κ − 1 < |𝒫|.

### 2.3 Coprime divisors

**Lemma 5 [proved].** Let D | κ with gcd(D, κ/D) = 1, and let p ≡ 1 (mod κ). If
p ∉ E_2(κ), then p ∉ E_2(D). Equivalently, E_2(D) ∩ {p ≡ 1 (mod κ)} ⊆ E_2(κ).

*Proof.* Put m = κ/D, and let (α, β) be a contraction at (p, κ) for ξ. Set
α'_{j'} = α_{mj'} and β'_{i'} = β_{mi'} for i', j' ∈ Z_D. These are well defined, since
m(i' + D) ≡ mi' (mod κ).
- ξ' := ξ^m is a coset generator for D. Indeed ζ = ξ^{(p−1)/κ} has order κ, and
  ξ'^{(p−1)/D} = ζ^{m²} has order κ/gcd(κ, m²) = mD/(m·gcd(D, m)) = D.
- Let P_D = (F_p^×)^D ⊇ Q_0. If x ∈ Q_{e} (index mod κ), then x ∈ ξ^e P_D. Moreover
  x ∈ ξ'^t P_D iff mt ≡ e (mod D), i.e. t ≡ m^{−1}e (mod D).
- So α'_{j'} + β'_{i'} ∈ Q°_{−m(i'+j')} lies in ξ'^{t}P_D ∪ {0} with
  t ≡ m^{−1}·(−m(i'+j')) ≡ −(i'+j') (mod D).
- Cell (0,0) is unchanged.

So (α', β') is a two-level contraction at (p, D) for ξ'. Existence does not depend on the
generator (paragraph after the definition of E_2 in the appendix). ∎

*Check.* The case gcd > 1 is not covered: the substitution needs m invertible mod D. The data
are consistent with the lemma: E_2(7) ∩ [1, 3300] ⊆ E_2(14) (in fact all 75 primes
p ≡ 1 (mod 14) below 3300 are in E_2(14), §3.3), and E_2(5) ⊆ E_2(10).

### 2.4 Locality barrier for membership certificates

**Proposition 6 [proved].** Let R ⊆ Z_κ with |R| = r, 2 ≤ r ≤ κ, and let
p ≥ ((r−1)κ^r + 2)² be a prime ≡ 1 (mod κ). Then there are α ∈ F_p^κ and pairwise distinct
β_i (i ∈ R) with α_j + β_i ∈ Q°_{−(i+j)} for all i ∈ R and j ∈ Z_κ. Every cell in column 0
is nonzero. The same holds for column sets.

*Proof.* Take β_i = ξ^{−i} − 1 (i ∈ R) and α_0 = 1, so column 0 has the cells
ξ^{−i} ∈ Q_{−i}. For j ≠ 0, let X_j = {x : x + β_i ∈ Q_{−(i+j)} ∀ i ∈ R}. The roots
1 − ξ^{−i} are distinct because the ξ^{−i} lie in distinct cosets. By
`lem:app-s2-weil-count` with ℓ = r ≤ κ,
κ^r|X_j| ≥ p − r − κ^r − (r−1)κ^r√p.
With s = √p ≥ (r−1)κ^r + 2,
s² − (r−1)κ^r s ≥ 2s ≥ 2(r−1)κ^r + 4 > κ^r + r,
since (2r−3)κ^r ≥ κ^r ≥ r for r ≥ 2. So X_j ≠ ∅. The β_i are distinct. ∎

**Consequence.** A proof that p ∈ E_2(κ) by exhibiting r rows (or columns) on which no
partial contraction with distinct entries exists can only work for
p < ((r−1)κ^r + 2)² < r²κ^{2r}. This includes Theorem 2 (r = 2, consistent with W_2 ≈ κ^4) and
TH6/TH7's step exceptional sets E(κ; R). At p ≈ κ^{(κ+1)/2}, any such certificate needs
r ≥ (κ+1)/4 − log_κ r. Heuristically, an exhaustive search for such a certificate scans about
p^{r−2} lines (one β up to scaling, by Theorem 2's argument), that is p^{(κ−7)/4 − log_κ r}
[conjecture: that no shortcut exists]. So restrictions to few rows cannot produce goal (B).
A structured certificate with r ≈ κ/4 rows is not excluded.
Strongest counterexample to "E_2 is explained by two-row obstructions": κ = 7, p = 3221 lies in
E_2(7) (exact; in the paper), while p > W_2(7) = 940, so every two-row restriction is
feasible. Likewise 859 ∈ E_2(6) with W_2(6) = 434. With only one search behind it,
p = 14177 ∈ E_2(8) (`dfs2b_k8_hi_q1.out`) is a further example [computed, single code]. At κ = 4, E_2(4) = {5, 13, 17, 29, 37, 53} but E2row(4) = {5, 13, 29}.

## 3. Computations [computed]

### 3.1 The coloured-clique (P) family, κ = 4..9 (`clique.py`, interrupted pass)

| κ | range | CLIQUE | NOCLIQUE | SKIP (h odd) | largest NOCLIQUE |
|---|---|---|---|---|---|
| 4 | ≤ 19997 | 553 | 3 (17, 41, 97) | 569 | 97 |
| 5 | ≤ 19991 | 543 | 20 | 0 | 941 |
| 6 | ≤ 19993 | 503 | 52 | 569 | 6673 |
| 7 | ≤ 59921 | 808 | 197 | 0 | 35281 |
| 8 | ≤ 29921 | 145 | 254 | 397 | 29537 |
| 9 | ≤ 29989 | 45 | 495 | 0 | 29989 |

Checks:
- Every CLIQUE line was re-verified on all κ² cells by `clique.py` itself, by
  `verify_cliques.out` (2597 witnesses, bad = 0) and, for κ = 9, by a third pow() check in
  this pass.
- NOCLIQUE/CLIQUE verdicts agree with `crosscheck_clique.py` (plain recursion, different
  generator, no shared code) on 311 + 73 primes.
- They agree with the κ = 9 sweep's independent `famsym9.c` P search (complete mode,
  `2026-11-04-rees-k9-sweep/low/Pc.out`, `P_rand_20001_200000.out`) on all 168 primes of
  (20000, 30000]: 147 COMPLETE_EMPTY are NOCLIQUE, 21 FOUND are CLIQUE, no conflict.
- No CLIQUE prime is in any E_2 list.
- TH2's κ = 4 observation (no zero-cell solution at 17, 41, 97) is reproduced. By Theorem 1,
  P is empty there for every shift.

### 3.2 Two-row exceptional sets (Corollary 3), complete

`tworow.py` builds S_b from the definition with bitsets. `tworow_np.py` uses the cyclotomic
numbers A(u, v) (numpy discrete logs) and scans every prime up to W_2(κ), beyond which E2row is
empty by Corollary 3(3). The two codes agree for κ = 4..9 (`tworow_k4-9.out`,
`tworow_np_k3-16.out`).

| κ | W_2(κ) | primes scanned | E2row(κ) | max | max/κ² |
|---|---|---|---|---|---|
| 3 | 17 | 2 | ∅ | – | – |
| 4 | 56 | 7 | 5, 13, 29 | 29 | 1.8 |
| 5 | 171 | 8 | 11 | 11 | 0.4 |
| 6 | 434 | 40 | 7, 13, 19, 31, 37, 43, 67, 73, 79, 139, 223 | 223 | 6.2 |
| 7 | 940 | 26 | 29, 43, 71 | 71 | 1.4 |
| 8 | 1810 | 64 | 17, 41, 73, 89, 97, 137, 233, 761 | 761 | 11.9 |
| 9 | 3188 | 75 | 19, 37, 73, 109, 127, 163 | 163 | 2.0 |
| 10 | 5242 | 170 | 19 primes (11 … 911) | 911 | 9.1 |
| 11 | 8164 | 103 | 23, 67, 89, 199, 419 | 419 | 3.5 |
| 12 | 12170 | 351 | 28 primes (13 … 1741) | 1741 | 12.1 |
| 13 | 17500 | 166 | 53, 79, 131, 157, 313, 547 | 547 | 3.2 |
| 14 | 24418 | 442 | 25 primes (29 … 2927) | 2927 | 14.9 |
| 15 | 33212 | 437 | 16 primes (31 … 1531) | 1531 | 6.8 |
| 16 | 44194 | 572 | 22 primes (17 … 1489) | 1489 | 5.8 |

- **Consistency.** E2row(κ) ⊆ E_2(κ) holds against every datum: E_2(4), E_2(5) and E_2(7)
  exact; xval_k6; every dfs2/dfs2b INFEASIBLE line for κ = 8, 9; no E2row prime is FEASIBLE or
  CLIQUE anywhere.
- **Chains.** TH7-check's primes where no chain exists ({5, 13} for κ = 4, {11}, {7, 13, 19,
  31, 43}, {29, 71}, {17, 41, 73}, {19, 37, 73}) all lie in E2row(κ). This is containment
  only; that the two-row obstruction is why chains fail is an interpretation.
- **Pattern.** max E2row(κ)/κ² stays below 15 up to κ = 16. It is larger for κ with many small
  divisors (6, 8, 10, 12, 14), which have h-parity and subgroup coincidences. This is
  consistent with a heuristic max E2row ≈ κ²·O(log κ) [conjecture].

### 3.3 Exact E_2 data for κ = 10..16 (`dfs2b`, existing code), cross-checked

`run_dfs2b_k10_16.sh` runs `2026-11-02-rees-schedules/small-prime/dfs2b K 3 40000 3e7 print`
for 240 s per κ. INFEASIBLE means p ∈ E_2(κ); every FEASIBLE witness is re-checked by dfs2b.
`xcheck_dfs2b.py` re-decides the verdicts with TH7-check's `rcdfs.c` (complete DFS written
from the definition, no shared code) and re-checks its own witnesses with pow(). dfs2b's three κ = 10 witnesses are pow-checked on
all κ² cells in `lemma5_check.py`.

Each run stopped at its 240 s cap. Every prime p ≡ 1 (mod κ) up to the last printed one has a
verdict (checked for gaps); the interrupted prime is dropped.

| κ | decided range | primes | in E_2(κ) | not in E_2(κ) | κ^{(κ+1)/2} |
|---|---|---|---|---|---|
| 10 | ≤ 8311 | 257 | 254 | 3361, 3761, 5821 | 3.2·10^5 |
| 11 | ≤ 11551 | 139 | 139 (all) | – | 1.8·10^6 |
| 12 | ≤ 10453 | 312 | 312 (all) | – | 1.0·10^7 |
| 13 | ≤ 13859 | 134 | 134 (all) | – | 6.3·10^7 |
| 14 | ≤ 13399 | 263 | 263 (all) | – | 3.9·10^8 |
| 15 | ≤ 15271 | 216 | 216 (all) | – | 2.6·10^9 |
| 16 | ≤ 15937 | 229 | 229 (all) | – | 1.7·10^10 |

- **Cross-checks.**
  - `xcheck_dfs2b.py` (rcdfs.c) re-decided 623 primes with 0 disagreements and 0 undecided:
    κ = 10 up to 3800 (129 primes, including the feasible 3361 and 3761), κ = 11 up to 8000
    (101), and κ = 12..16 up to 4000 (131, 44, 89, 65, 64). Output: `xcheck_dfs2b.out`. The rest
    of each range has only dfs2b's verdict.
  - Lemma 5's restriction map was tested mechanically (`lemma5_check.py` → `lemma5_check.out`):
    each of the three κ = 10 witnesses, restricted to even indices with generator g² (D = 5),
    and to multiples of 5 with generator g^5 (D = 2), is a D-contraction.
  - Every E2row(κ) prime in these ranges is INFEASIBLE, as Corollary 3 requires.
- **Reading.** These are the first exact E_2 data for κ ≥ 10. They are lower bounds only, e.g.
  max E_2(16) ≥ 15937. They agree with the model, which puts the end of E_2(κ) near
  1.4κ^{(κ+1)/2}, far beyond these ranges. The first non-member of E_2(10) is 3361.
- `dfs2b_k14_3300.out` (separate run, no cap): all 75 primes p ≡ 1 (mod 14) below 3300 are in
  E_2(14). This includes the 56 primes of E_2(7) up to 3221, as Lemma 5 predicts.

### 3.4 Non-randomness of the cyclotomic graph below κ^4 (κ = 9)

- `count_clique.py`: all transversal cliques (y_1 = g fixed by Q_0-scaling). Counts against the
  uniform-model expectation μ_P = p^{κ−2}κ^{1−κ(κ−1)/2}:

| p | 3529 | 4177 | 5077 | 6607 | 9397 | 11953 |
|---|---|---|---|---|---|---|
| transversal cliques | 21 | 504 | 6012 | 27 | 18 | 549 |
| μ_P | 2.7e−9 | 8.9e−9 | 3.5e−8 | 2.2e−7 | 2.6e−6 | 1.4e−5 |

- `maxclique.py`: the clique number of Cay(F_p, Q_0) is 8, 9, 9, 8 at p = 3529, 4177, 5077,
  6607. It is 3, 5, 5 at p = 4159, 5023, 7507. The random-graph value is about 2log_9 p ≈ 7.6.
- The common neighbourhood of {0, 1}, which is the cyclotomic number A(0,0) plus boundary
  terms, has size 32 to 108 against a mean h/9 ≈ 44–93 (p = 4159: 32 vs 51; p = 5077: 104
  vs 63). At κ = 9 and p ≈ 5000 the Weil error bound (κ−1)(κ−2)√p/κ² ≈ 0.69√p ≈ 49 is of
  the same size as the mean, so these graphs are far from random.
- So at κ = 9 the first non-member of E_2 is 3529 = 0.06·κ^5, carried by a structured
  clique. The P family is far more frequent below about κ^4 than the uniform model says.
- At p ≈ κ^{(κ+1)/2} the relative fluctuation κ²/√p = κ^{2−(κ+1)/4} is 0.33 at κ = 9 and tends
  to 0. So the uniform model is reasonable at the top of E_2 for large κ, but not near κ^4.
- A weak correlation exists: members have lower z_00 = (A'(0,0) − p/κ²)/√p (rank AUC 0.64 for
  κ = 7, 8; `cyclo_stats.py`). Its V column is a near-deterministic Parseval quantity and
  carries no information.

### 3.5 First non-member

Every prime below the first non-member f(κ) is a member (κ = 4..10, all data). For κ = 11..16,
f(κ) exceeds the decided ranges of §3.3.

| κ | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|
| f(κ) | 41 | 191 | 229 | 967 | 1553 | 3529 | 3361 |
| f/κ² | 2.6 | 7.6 | 6.4 | 19.7 | 24.3 | 43.6 | 33.6 |
| f/κ^{(κ+1)/2} | 1.28 | 1.53 | 0.43 | 0.40 | 0.13 | 0.06 | 0.011 |

Corollary 3(2) proves f(κ) > κ² − 3κ + 3 for every κ. The observed f(κ) lies between κ² and
κ^4.

## 4. Heuristic for the observed law [conjecture]

Model (TH6 Conjecture 6.4 made quantitative): normalised contractions occur in orbits of size
2κ² under recentring and transposition (dfs2b PRUNE 2). The number of orbits is Poisson with
mean μ_G(p)/(2κ²), where μ_G = p^{2κ−2}q^{κ²−1} and q = (h+1)/p. **No constant is fitted.**
`heuristic2.py` → `heuristic2.out`: the predicted largest member p* is the largest p with
Σ_{p' ≥ p} Pr[p' ∈ E_2] ≥ 1/2.

| κ | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 16 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| p*/κ^{(κ+1)/2} | 1.28 | 1.53 | 1.57 | 1.51 | 1.53 | 1.49 | 1.47 | 1.42 | 1.34 | 1.29 |
| observed max/κ^{(κ+1)/2} | 1.66 | 1.45 | 1.62 | 1.34 | ≥ 1.22 | ≥ 0.31 | – | – | – | – |

- **Explanation of the law.** μ_G(p) = (p/κ^{(κ+1)/2})^{2κ−2}(1 + (κ−1)/p)^{κ²−1}, and the last factor is ≈ e^{κ³/p}, close to 1 near the top for κ ≥ 6 (2.3 at κ = 4, p = 53; `heuristic2.py` uses the exact q). So
  p* ≈ κ^{(κ+1)/2}·(2κ²·L)^{1/(2κ−2)}, where L ≈ ln of the number of primes in the window in
  which μ_G changes by a constant factor.
  - That factor is ≈ 1.5 for 5 ≤ κ ≤ 10.
  - It tends to 1 like exp(O(ln κ/κ)).
  - This is the "observed law ~1.5κ^{(κ+1)/2}" with its constant explained.
- **Forecasts.**
  - κ = 8: max E_2(8) ≈ 1.8·10^4. The known member 14177 = 1.22κ^{4.5} fits; the queue on
    (11897, 20000] is still running.
  - κ = 9: max E_2(9) ≈ 8.8·10^4. This is consistent with the κ = 9 sweep's list of 1373
    unresolved primes up to 424549, 839 of them with P empty up to 99577.
- **Limits of the model.**
  - It is wrong per prime below about κ^4, where structured solutions dominate (§3.4).
  - It treats orbits as independent.
  - Nothing in it is proved. Proving it for one κ at this precision is the square gap (TH6 §6).
  - O1/O2 (TH3), the forest/Janson/local-lemma refutations (TH5 §3) and the square-root
    barrier (TH6 §6.2) explain why the standard tools cannot reach it.

## 5. Why (A) and (B) were not reached

- **(A).** Every certificate family studied so far faces one of four barriers: O1, O2
  (≤ κ−1 columns, BGP Prop. 26), TH5 §3.4 (sequential extension, the last unknown faces κ
  conditions) or TH6 §6.2 (square-root bounds need p ≳ κ^{2n/D_V} ≥ κ^{κ+1}).
  - The clique family has κ − 2 free parameters and (κ−2)(κ+1)/2 conditions. That is the same
    ratio as the full problem, and its last point faces κ − 1 conditions. A second moment over
    the other points needs those points to form a random clique, so the bipartite averaging
    that gives T_A is unavailable. No proof below exponent κ was found.
  - The SL_2 (determinant) form and the λ-line form of TH2 §3.5 re-index the same sums.
  - Getting below κ^κ/2 requires joint control of all κ columns (O2/O3). That is the
    analogue of beating the (1/2)log_2 p Ramsey bound for Paley cliques by a constant factor,
    for which no method is known (TH2 §3.4, read from Kunisky–Yu §1).
- **(B).** By Proposition 6, no local certificate works above ((r−1)κ^r + 2)². The model
  predicts no members above (1.3–1.6)κ^{(κ+1)/2}. And for fixed κ, E_2(κ) is finite
  (below T_A). So an "infinite family above κ^{(κ+1)/2}" can only mean growing κ, with members
  certified globally. None is known, and the model says the observed law is the truth up to
  the factor (2κ²L)^{1/(2κ−2)}.
- **Proved lower bounds instead.**
  - max E_2(κ) ≥ the largest prime ≡ 1 (mod κ) that is ≤ κ² − 3κ + 3, whenever one exists
    (Corollary 3(2)).
  - max E_2(κ) ≥ max E2row(κ) (§3.2).
  - max E_2(κ) ≥ max E_2(D) for coprime-cofactor divisors D (Lemma 5); e.g.
    max E_2(18) ≥ 18181 [computed: it rests on a single dfs2b INFEASIBLE verdict at κ = 9].
    For κ = 14, §3.3 already gives more: every prime up to 13399 is in E_2(14).

## 6. Proposed text (AI-checked, pending human review; not applied)

### 6.1 New subsection for `appendix-schedule2.tex`

Insert after Table `tab:app-s2-thresholds` and before `\subsection{A tower of coset refinements}`.
It uses only notation of the appendix up to that point.

```latex
\subsection{Local obstructions and small exceptional primes}
\label{app:s2-local}

\noindent\textbf{Status: AI-checked, pending human review} (\file{research/audits/reviews/2026-11-05-rees-threshold-8.md}). This subsection gives lower bounds for $E_2(\kappa)$, not upper bounds; it changes no threshold, schedule or table. Put $\varepsilon = \operatorname{ind}(-1)$, so $\varepsilon = 0$ exactly when $-1 \in Q_0$, and $A(u,v) = \#\{w \in Q_u : w - 1 \in Q_v\}$ for $u,v \in \mathbb{Z}_\kappa$.

\begin{lemma}[two rows]
\label{lem:app-s2-two-rows}
Let $(\alpha,\beta)$ be a two-level contraction at $(p,\kappa)$ written as in Lemma~\ref{lem:app-s2-normal}. Then the $\beta_i$ are pairwise distinct, the $\alpha_j$ are pairwise distinct, and $Q^\circ_{-i} - Q^\circ_{-k} \supseteq \Fp^\times$ for all distinct $i,k \in \mathbb{Z}_\kappa$.
\end{lemma}

\begin{proof}
If $\beta_i = \beta_k$ with $i \ne k$, then $\alpha_j + \beta_i \in Q^\circ_{-(i+j)} \cap Q^\circ_{-(k+j)} = \{0\}$ for every $j$, so every $\alpha_j$ equals $-\beta_i$; then $\alpha_j + \beta_0 = \beta_0 - \beta_i$ lies in $Q^\circ_{-j}$ for every $j$, so it is $0$, contradicting $\alpha_0 + \beta_0 \ne 0$. The $\alpha_j$ are treated in the same way. Now let $d = \beta_i - \beta_k \ne 0$. For every $j$, $d = (\alpha_j + \beta_i) - (\alpha_j + \beta_k)$ lies in $Q^\circ_{-(i+j)} - Q^\circ_{-(k+j)} = \xi^{-j}S$ with $S = Q^\circ_{-i} - Q^\circ_{-k}$, so $\xi^j d \in S$ for all $j \in \mathbb{Z}_\kappa$. Since $Q_0 S = S$, the set $S$ contains $\bigcup_j \xi^j d\,Q_0 = \Fp^\times$.
\end{proof}

\begin{proposition}[cyclotomic criterion]
\label{prop:app-s2-cyclotomic}
Let $\kappa \ge 2$ and let $p \equiv 1 \pmod\kappa$ be prime.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item If $A(u,v) = 0$ for some $u,v \in \mathbb{Z}_\kappa$ with $u \ne 0$, $v \ne \varepsilon$ and $u \ne v$, then $p \in E_2(\kappa)$.
  \item Every prime $p \equiv 1 \pmod\kappa$ with $p \le \kappa^2 - 3\kappa + 3$ lies in $E_2(\kappa)$.
  \item If $p - 2 > (\kappa-1)(\kappa-2)\sqrt p + 3(\kappa-1)$, then $A(u,v) \ge 1$ for all $u, v$, so (i) does not apply.
\end{enumerate}
\end{proposition}

\begin{proof}
(i) Let $b \ne 0$ and $z \in Q_c$. Writing $z = x - y$ with $x \in Q^\circ_0$ and $y \in Q^\circ_b$ is possible with $x = 0$ exactly when $c = b - \varepsilon$, with $y = 0$ exactly when $c = 0$, and with $x, y \ne 0$ exactly when $A(-c, b-c) \ge 1$: put $x = zw$, so that $x \in Q_0$ if and only if $w \in Q_{-c}$, and $y = z(w-1) \in Q_b$ if and only if $w - 1 \in Q_{b-c}$. Since $Q_0(Q^\circ_0 - Q^\circ_b) = Q^\circ_0 - Q^\circ_b$, this set contains $\Fp^\times$ if and only if $A(-c, b-c) \ge 1$ for every $c \notin \{0, b - \varepsilon\}$. The map $(b,c) \mapsto (u,v) = (-c, b-c)$ is a bijection from pairs with $b \ne 0$ onto pairs with $u \ne v$, and it turns $c \ne 0$ into $u \ne 0$ and $c \ne b - \varepsilon$ into $v \ne \varepsilon$. So a vanishing $A(u,v)$ as in (i) gives $b \ne 0$ with $Q^\circ_0 - Q^\circ_b \not\supseteq \Fp^\times$; multiplying by $\xi^{-i}$ shows that rows $i$ and $i - b$ violate Lemma~\ref{lem:app-s2-two-rows}, so no contraction exists.

(ii) Each $w \in \Fp \setminus \{0,1\}$ is counted by exactly one $A(u,v)$, so $\sum_{u,v}A(u,v) = p - 2$. The pairs in (i) number $(\kappa-1)(\kappa-2)$ if $\varepsilon = 0$ and $\kappa^2 - 3\kappa + 3$ otherwise. If all of them had $A(u,v) \ge 1$, then $p - 2 \ge (\kappa-1)(\kappa-2)$, that is $p \ge \kappa^2 - 3\kappa + 4$.

(iii) As in the proof of Lemma~\ref{lem:app-s2-cyclo}, $\kappa^2 A(u,v) = \sum_{s,t}\omega^{-us-vt}K'(s,t)$ with $K'(s,t) = \sum_{w \ne 0,1}\chi^s(w)\chi^t(w-1)$, the sum $K'$ of that proof. Here $K'(0,0) = p-2$; $K'(s,0) = -1$, $K'(0,t) = -\chi^t(-1)$ and $K'(s,-s) = -1$ for $s,t \ne 0$, the last because $w \mapsto w/(w-1)$ permutes $\Fp\setminus\{0,1\}$; and $|K'(s,t)| \le \sqrt p$ for the $(\kappa-1)(\kappa-2)$ pairs with $s,t,s+t \ne 0$, by the Weil bound for $X^s(X-1)^t$. Hence $|\kappa^2A(u,v) - (p-2)| \le 3(\kappa-1) + (\kappa-1)(\kappa-2)\sqrt p$.
\end{proof}

\begin{lemma}[coprime divisors]
\label{lem:app-s2-coprime}
Let $D \mid \kappa$ with $\gcd(D,\kappa/D) = 1$, and let $p \equiv 1 \pmod\kappa$ be prime. If $p \in E_2(D)$, then $p \in E_2(\kappa)$.
\end{lemma}

\begin{proof}
Put $m = \kappa/D$ and let $(\alpha,\beta)$ be a two-level contraction at $(p,\kappa)$ for $\xi$. Then $\alpha'_{j} = \alpha_{mj}$ and $\beta'_{i} = \beta_{mi}$, for $i,j \in \mathbb{Z}_D$, are well defined. The element $\xi' = \xi^m$ is a coset generator for $D$, because $\xi'^{(p-1)/D} = \zeta^{m^2}$ has order $\kappa/\gcd(\kappa,m^2) = D$. An element of $Q_e$ lies in $\xi'^{t}P_D$, where $P_D = \{x^D : x \in \Fp^\times\}$, exactly when $t \equiv m^{-1}e \pmod D$. So $\alpha'_j + \beta'_i \in Q^\circ_{-m(i+j)}$ lies in $\xi'^{-(i+j)}P_D \cup \{0\}$, and $\alpha'_0 + \beta'_0 = \alpha_0 + \beta_0 \ne 0$. Hence $(\alpha',\beta')$ is a two-level contraction at $(p,D)$ for $\xi'$, and $p \notin E_2(D)$, since the existence of a contraction does not depend on the coset generator.
\end{proof}

\begin{remark}[scope of local obstructions]
\label{rem:app-s2-local-scope}
The same counting as in Proposition~\ref{prop:app-s2-TW}, with $\beta_i = \xi^{-i} - 1$ and Lemma~\ref{lem:app-s2-weil-count} for $\ell = r$, shows that for every set $R$ of $r \ge 2$ rows and every prime $p \ge ((r-1)\kappa^r + 2)^2$ there are $\alpha$ and pairwise distinct $\beta_i$, $i \in R$, with $\alpha_j + \beta_i \in Q^\circ_{-(i+j)}$ for all $i \in R$ and $j \in \mathbb{Z}_\kappa$. So an obstruction confined to $r$ rows, such as Lemma~\ref{lem:app-s2-two-rows}, can only certify $p \in E_2(\kappa)$ for $p < ((r-1)\kappa^r+2)^2$; for $r = 2$ this is consistent with Proposition~\ref{prop:app-s2-cyclotomic}(iii). The largest exceptional primes found by exhaustive search (Remark~\ref{rem:two-level-threshold-size}) are not explained by two-row obstructions for any $\kappa \le 9$; for example $p = 3221 \in E_2(7)$ lies above the bound $940$ of Proposition~\ref{prop:app-s2-cyclotomic}(iii). A finite computation (AI-checked, pending human review) lists, for every $3 \le \kappa \le 16$, the complete set of primes to which Proposition~\ref{prop:app-s2-cyclotomic}(i) applies; its largest element is $29, 11, 223, 71, 761, 163$ for $\kappa = 4,\dots,9$ and at most $15\kappa^2$ for every $\kappa \le 16$ (the set is empty for $\kappa = 3$), and it contains every prime at which no chain of Subsection~\ref{app:s2-chains} exists in the computed ranges.
\end{remark}
```

Notes for the integrator:
- `\Fp`, `\file`, `\operatorname`, the enumerate options and all cited labels are as in the
  current appendix.
- The remark refers forward to `app:s2-chains`. If the subsection is placed after
  `app:s2-chains` instead, nothing else changes.
- The zero-cell statement (Theorem 1) is not proposed for the paper. It could go into
  `rem:two-level-threshold-size` as the precise form of the coloured-clique sentence; see 6.2.

### 6.2 Sentence for `main.tex`, Remark `rem:two-level-threshold-size`

Insert before its last sentence ("A sub-family of the problem is a coloured-clique question …"):

```latex
In the other direction, a contraction forces $(Q_0 \cup \{0\}) - (Q_b \cup \{0\}) \supseteq \Fp^\times$ for every $b \ne 0$, so every prime $p \equiv 1 \pmod\kappa$ with $p \le \kappa^2 - 3\kappa + 3$ lies in $E_2(\kappa)$, and $E_2(D) \subseteq E_2(\kappa)$ on primes $p \equiv 1 \pmod\kappa$ when $D \mid \kappa$ and $\gcd(D,\kappa/D) = 1$ (Appendix~\ref{app:s2-local}; AI-checked, pending human review); obstructions confined to $r$ rows stop below $((r-1)\kappa^r+2)^2$, so for fixed $r$ they cannot reach the square gap once $\kappa$ is large.
```

Optional replacement of the last sentence (Theorem 1, proved here):

```latex
The contractions with the largest possible number $\kappa$ of zero cells exist only when $-1 \in Q_0$, and then exactly when there are $y_m \in Q_m$, $m \ne 0$, with all differences $y_m - y_{m'}$ in $Q_0$; this coloured-clique sub-family is a question in $\Fp$ of the same type as the clique number of the Paley graph, where the analogous gap is a long-standing open problem.
```

## 7. Claim gates, next question, next command

- **Gates that stay false:**
  - "two-level threshold ≈ κ^{(κ+1)/2}" or "exponent below κ" proved;
  - "E_2(κ) known for κ ≥ 8" (κ = 10..16 are known only on the small ranges of §3.3);
  - "max E_2(κ) determined" for κ ≥ 8;
  - any equivalence with Paley cliques;
  - Conjecture 6.4 / the §4 model proved;
  - any priority claim. Theorem 2 is an elementary covering argument and may be classical in
    cyclotomy; no literature search was possible.
  - `rees_hsp_reduction.json` and all registry gates are untouched.
- **Next hard question:** a statement that uses all κ columns jointly (O2/O3) and certifies one
  prime p ∈ (Cκ^{(κ+1)/2}, κ^κ/2] for one κ ≥ 8 without enumeration.
- **Cheap next command:** extend §3.3 with `dfs2b 10 8312 20000 3e8 print` on a free core.
  The expected artifact is the exact E_2(10) on (8311, 2·10^4] (the model predicts members
  throughout). Acceptance: every FEASIBLE line pow()-verified, and a 20-prime sample re-decided
  by `xcheck_dfs2b.py 10 20000 1e9`.

## 8. Artifacts (`2026-11-05-rees-threshold-8/`)

| file | content |
|---|---|
| `clique.py`, `clique_k{4..9}.out` | (interrupted pass) complete transversal-clique (P-family) search; Theorem 1 |
| `crosscheck_clique.py`, `crosscheck_clique.out`, `crosscheck_clique_k8k9.out` | independent recursion, all agree |
| `clique_witnesses_found.txt`, `verify_cliques.out` | witnesses and their independent verification (bad = 0) |
| `count_clique.py` | exact transversal-clique counts (§3.4) |
| `maxclique.py` | clique numbers of Cay(F_p, Q_0) (§3.4) |
| `cyclo_stats.py` | cyclotomic statistics of members vs non-members (§3.4) |
| `tworow.py`, `tworow_k4-9.out` | two-row criterion from the definition (bitsets) |
| `tworow_np.py`, `tworow_np_k3-16.out` | complete E2row(κ) via cyclotomic numbers up to W_2(κ) |
| `run_dfs2b_k10_16.sh`, `run_dfs2b_k10_16.log`, `dfs2b_k1{0..6}.out`, `dfs2b_k14_3300.out` | exact E_2 decisions, κ = 10..16 |
| `xcheck_dfs2b.py`, `xcheck_dfs2b.out` | independent re-decision with `rcdfs.c` (TH7-check) |
| `heuristic.py`, `heuristic.out` | (interrupted pass) fitted Poisson model; superseded |
| `heuristic2.py`, `heuristic2.out` | unfitted Poisson-orbit model (§4) |
| `probe_mobius.py`, `mobius_sym.py`, `mobius_sym_k9.out` | (interrupted pass) PGL_2 stabilisers; exploratory |
| `compare_e2.py`, `undecided.py` | (interrupted pass) bookkeeping |

## 9. Independent adversarial check (fresh general-purpose subagent, 5 November 2026)

The checker was given only this report and the code paths. Its scratch code is in
`2026-11-05-rees-threshold-8/check/` and shares nothing with the scripts above.

**Verdict: no Error.** Every proof in §2 was checked line by line and found correct: Lemma 0,
Theorem 1 (1)–(3), Theorem 2, Corollary 3 (1)–(3) including the count of 𝒫 and the pigeonhole
bound, Lemma 4, Lemma 5 and Proposition 6.

**Own-code tests, all agreeing.**
- Two-row criterion, κ = 3..12:
  - the direct difference-set test equals the A(u, v) test at every prime below 1200;
  - the verdict is the same for two coset generators;
  - the Weil deviation bound and |𝒫| hold;
  - every pigeonhole prime has a zero on 𝒫;
  - the E2row lists are reproduced.
- An independent bitset E_2 search reproduces:
  - E_2(2) = E_2(3) = ∅;
  - E_2(4) and E_2(5);
  - E_2(6), 53 primes up to 859;
  - E_2(7) ∩ [1, 1000];
  - f(4..7) = 41, 191, 229, 967;
  - E2row ⊆ E_2 throughout.
- Theorem 1, by enumerating every normalised contraction for κ = 3, 4, 5:
  - zero-cell structure and zeros at (j + c, j) when there are κ zeros;
  - κ-zero contraction ⟺ transversal clique;
  - (P_c) solvable for every c iff a clique exists (κ = 4, 5, 6, p < 400), with 0 mismatches.
- Lemma 5 on κ = 6 witnesses with D = 2, 3.
- Proposition 6 never fails above its bound for (κ, r) ∈ {(3,2), (4,2), (5,2), (3,3), (4,3)}.
  The bound is very loose: the largest failures are 7, 29, 61, 79, 373.
- The κ = 9 clique counts at 3529, 6607 and 9397 are reproduced.
- All quoted table numbers match the output files.

**Gaps and imprecisions raised, all fixed in the text above:**
- (7) W_2 < ((κ−1)(κ−2)+2)² only for κ ≥ 4.
- (8) The −log_κ r term was dropped, and the p^{r−2} search size was not marked heuristic.
- (9) §0 and §2.4 overstated Proposition 6 as "route closed"; they now state exactly what is
  proved.
- (10) §6.2's "cannot reach the square gap" was too strong; it is now qualified by r and κ.
- (11) The example 14177 ∈ E_2(8) rests on a single code. It was replaced by 3221 ∈ E_2(7)
  (and 859 ∈ E_2(6)) in the LaTeX and in §2.4.
- (12) 18181 is now labelled [computed, single code], and the superseded κ = 14 bound was
  removed.
- (13) The correction factor in §4 is now stated as (1 + (κ−1)/p)^{κ²−1} ≈ e^{κ³/p}.
- (14) The chains statement is now containment only.
- (15) LaTeX fixes:
  - K renamed K′ to match `lem:app-s2-cyclo`;
  - "written as in";
  - 3 ≤ κ ≤ 16;
  - "Subsection".
- (17) The `xcheck_dfs2b.py` docstring now says which witnesses it checks.
- (18) Theorem 2 and Corollary 3 are now flagged "likely classical".

No forbidden macros were found. All cited labels exist and the new labels are unused elsewhere.


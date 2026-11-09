# Rees SDE arity at small primes: thresholds, exact tables, lower bounds

2 November 2026. AI-only research pass (one session plus one literature
helper). It is not human review, a Lean proof, or a priority claim. Each claim
is labelled **[proved]** (a written proof here or a cited theorem),
**[exact]** (a complete finite computation with the script named) or
**[argued]** (a heuristic or partial check). Scripts are in
`2026-11-02-rees-schedules/small-prime/`, interpreter `/opt/anaconda3/bin/python`.
Nothing outside this file and that folder was edited.

Problem. Columns λ_1..λ_M ∈ F_p^a are arbitrary. Find s ≠ 0 with
Σ_i s_i^d λ_i = 0. With κ = gcd(d, p−1) ≥ 2, H = (F_p^*)^κ (order
h = (p−1)/κ) and P = H ∪ {0}, this is equivalent to finding x ∈ P^M, x ≠ 0,
with Σ x_i λ_i = 0 (then take κ-th roots and convert by a Bezout exponent).
Write M*(p, κ, a) for the least M at which EVERY column tuple has a witness.

## 0. Answers

1. **Existence is never the obstacle.** Chevalley–Warning gives
   M*(p, κ, a) ≤ κa + 1 at every prime **[proved]**. So no regime needs more
   than linear arity for a witness to exist. Every bound above κa + 1,
   including Schedule 2's (a+1)((κ−1)a+1) and Schedule 1's product of
   arities of about 2^1565 at the class-9 profile, is the price of a
   particular *finding* method.
2. **Lower bounds.** M*(p, κ, a) ≥ a·(M*(p, κ, 1) − 1) + 1 ≥ 2a + 1
   **[proved]**. At κ = p − 1, M* = (p−1)a + 1 = κa + 1, so
   Chevalley–Warning is exact there (Olson) **[proved]**. Exact values of
   M* for p ≤ 31 at a = 1 and for small p at a = 2 are in §5 **[exact]**.
   The "κ = p−1 forces a(p−1)+1 columns" bound is therefore linear. It does
   not rule out any poly(a, κ) arity.
3. **Weil step, tightened.** Using a decoupled form of the two-level
   contraction (C_ij = z_i z_j(α_j + β_i), not only α = β) and the exact
   character-sum error, the two-level arity (a+1)((κ−1)a+1) works for every
   p > T_W(κ) = ((A + √(A² + 4κ^κ))/2)², A = (κ−2)κ^κ + 1 **[proved]**.
   This is 26 to 156 times below 16κ^{2κ+2} for κ ≤ 9. The β are explicit,
   and the α_j are found by sampling (§2).
4. **Exact two-level thresholds.** A universal two-level contraction exists
   for every prime when κ = 2 or 3. For κ = 4 it fails exactly at
   p ∈ {5, 13, 17, 29, 37, 53}, and for κ = 5 exactly at
   p ∈ {11, 31, 41, 61, 71, 101, 131, 151, 181} **[exact + proved]**. For
   κ = 6 the failing primes up to 1.5·10⁶ are 53 primes ≤ 859. For κ = 7,
   8, 9 the largest proven exceptional primes are 1583, 2441 and 3583, and
   feasible primes begin at 967, 1553 and 3529.
   The exceptional sets are not known beyond the computed range (§3). The
   observed threshold is about 1.5κ^{(κ+1)/2}, far below T_W **[argued]**.
5. **New all-prime fallback.** An L-level collision tensor has a universal
   contraction at EVERY prime once κ^L > κ(κ−1)^L **[proved, §4]**. This
   follows from Chevalley–Warning on a constant-size instance plus a coset-shift
   lemma. Arity is Π_{ℓ<L}((κ−1)^ℓ a + 1) = O_κ(a^L) with
   L_CW(κ) ≈ κ ln κ, against Ivanyos–Santha's exponent κ⌈log₂(κ+1)⌉. At the
   tested exceptional primes with κ < p − 1, SAT finds 3-level contractions
   (five κ = 4 primes and five κ = 5 primes). The zero-sum cases κ = p − 1
   at p = 5, 7, 11 have none at 3 levels, and p = 5 has one at 4
   **[exact]**.
6. **Gap.** Efficient finding is known at arity O(a²) for p ∉ E_2(κ) (all p > T_W(κ)), and at
   O_κ(a^{L}) for every p. Existence holds at κa + 1. No efficient algorithm
   at linear arity is known even for p = 3, and no hardness result for this
   diagonal/zero-sum search is known either (§6).

## 1. Setup: what a two-level contraction is

This follows `POWER_SDE_SYMMETRIC_CONTRACTION.md` ("Two-Level Collision
Tensor"). Fix a generator g, cosets Q_m = g^m H and A_m = Q_m ∪ {0}. Pick
representatives z_i ∈ Q_i with z_0 = 1, and let W = ker(z^T) ⊂ F_p^κ.
After two levels, the cell tensor (T_ij) lies in W ⊗ W ⊗ F_p^a, and T_00
has nonempty support. A *universal two-level contraction* is a κ×κ matrix
C with entries in P, C_00 ≠ 0 and ⟨C, W⊗W⟩ = 0. Then Σ C_ij T_ij = 0, and
rooting C_ij gives a witness that is nonzero on T_00's support.

**Lemma 1 (normal form) [proved].** Ann(W⊗W) = {z a^T + b z^T}. This is
the note's lemma: both sides have dimension 2κ−1. Put α_j = a_j/z_j and
β_i = b_i/z_i, so C_ij = z_i z_j(α_j + β_i). Since z_i z_j ∈ Q_{i+j}, we
have C_ij ∈ P iff α_j + β_i ∈ A_{−(i+j)}. **The choice of representatives
z_i is irrelevant; only the coset labelling matters.** WLOG β_0 = 0
(translate α by c and β by −c) and α_0 = 1 (scale by an element of H). The
note's symmetric form is the special case α = β = t. Zero entries of C are
allowed: a zero cell just gets weight 0, and C_00 ≠ 0 still protects T_00.

## 2. The Weil step: what it needs, and a tighter threshold

**What the note's step uses.** At stage j (k = j+1 ≤ κ conditions) the
note's sampler needs t with prescribed cosets for 2z_j²t and for
z_i z_j(t + t_i), i < j. The character expansion has κ^k − 1 nontrivial
sums Σ_x χ(Π_{i∈S}(x − r_i)^{e_i}), one for each nonzero e ∈ Z_κ^k. Each
has s = |supp e| distinct roots and multiplicities in [1, κ−1], so the
polynomial is not a constant times a κ-th power. The Weil bound
(Lidl–Niederreiter Thm 5.41; see §7) gives (s−1)√p. Uniformity over
prefixes holds because the affine roots {0, −t_0, …} are distinct, which is
why the note excludes old values. Its threshold √p ≥ 4κ^{κ+1} comes from
(i) bounding the error by (k−1)√p + k and (ii) asking N_k ≥ p/(2κ^k), so
that a UNIFORM t succeeds with probability ≥ 1/(2κ^k).

**Exact error constant [proved].** Sum over supports with
#{e : |supp e| = s} = C(k,s)(κ−1)^s, using Σ_s C(k,s)(κ−1)^s s = k(κ−1)κ^{k−1}.
The total error is at most

    κ^{-k} Σ_{s≥1} C(k,s)(κ−1)^s [(s−1)√p + (k−s)]
      = (k − 1 − k/κ + κ^{-k})·√p + k/κ − k·κ^{-k},

against the note's (1 − κ^{-k})(k−1)√p. At k = 1 the error is 0: a single
coset condition has exactly h solutions.

**Decoupled construction (Theorem 2) [proved].** Fix β_0 = 0 and
β_i = g^{−i} − 1 (i ≥ 1). Then 1 + β_i ∈ Q_{−i}, and the roots
{0, −β_1, …, −β_{κ−1}} are distinct because the 1 + β_i lie in different
cosets. Take α_0 = 1. For each j ≥ 1, α_j must satisfy the κ conditions
x ∈ Q_{−j} and x + β_i ∈ Q_{−(i+j)}. These conditions involve only the fixed
explicit β, so there is no prefix dependence at all. With k = κ the count of
valid nonzero x is

    N_j ≥ (p − κ)/κ^κ − (κ − 2 + κ^{−κ})√p − (1 − κ^{1−κ}),

which is positive iff p − A√p − κ^κ > 0 with A = (κ−2)κ^κ + 1, i.e. for
**p > T_W(κ) = ((A + √(A² + 4κ^κ))/2)²**. Then C_ij = z_i z_j(α_j + β_i) is
a universal two-level contraction, and arity (a+1)((κ−1)a+1) suffices.
Finding α_j: when √p ≥ 2A + 2κ^κ, i.e. p ≥ 4((κ−1)κ^κ + 1)², a uniform x
succeeds with probability ≥ 1/(2κ^κ). So 2κ^κB trials fail with probability
≤ 2^{−B} per j, as in the note. In the band T_W < p < 4((κ−1)κ^κ+1)², p is
bounded by a function of κ, and α_j is found by enumerating F_p
deterministically in O(κ² p log p) operations.

| κ | T_W(κ) (arity proved above it) | sampler bound 4((κ−1)κ^κ+1)² | note's 16κ^{2κ+2} | ratio note/T_W |
|---|---|---|---|---|
| 2 | 6 | 100 | 1024 | 156 |
| 3 | 837 | 1.21e4 | 1.05e5 | 125 |
| 4 | 263,680 | 2.37e6 | 1.68e7 | 64 |
| 5 | 87,915,625 | 6.25e8 | 3.91e9 | 44 |
| 6 | 3.48e10 | 2.18e11 | 1.25e12 | 36 |
| 7 | 1.70e13 | 9.77e13 | 5.32e14 | 31 |
| 8 | 1.01e16 | 5.52e16 | 2.88e17 | 28 |
| 9 | 7.36e18 | 3.84e19 | 1.95e20 | 26 |

Asymptotically T_W ≈ (κ−2)²κ^{2κ}. The ratio tends to 16 as κ grows. Any
argument that needs one variable to satisfy κ independent coset conditions
through Weil will stay at order κ^{2κ}. §3 shows that the true threshold is
far lower.

## 3. Exact two-level thresholds

Call (p, κ) *two-level exceptional* when no universal two-level
contraction exists, and write E_2(κ) for the set of such p. Three methods
combine: complete DFS (`two_level.py`, `dfs2.c`, which agree prime by prime
on [3, 3000] for κ ≤ 6), witness scans (`scan2.c`, with every witness's κ²
conditions re-checked), and Theorem 2 above T_W(κ).

| κ | E_2(κ) | how settled |
|---|---|---|
| 2 | ∅ | DFS p ≤ 3000; Theorem 2 for p ≥ 7 **[exact + proved]** |
| 3 | ∅ | DFS p ≤ 3000 > T_W = 837 **[exact + proved]** |
| 4 | {5, 13, 17, 29, 37, 53} | DFS ≤ 3000; scan [3000, 263683] (11,327 primes); Theorem 2 above 263,680 **[exact + proved]** |
| 5 | {11, 31, 41, 61, 71, 101, 131, 151, 181} | DFS ≤ 3000; scan [3000, 87,930,000] (≈1.27M primes, 0 unresolved); Theorem 2 above 87,915,625 **[exact + proved]** |
| 6 | 53 primes, the largest 859 (7, 13, 19, …, 787, 859) | complete for p ≤ 1.5·10⁶ (DFS, 56,804 feasible primes in [3000, 1.5·10⁶]); unknown on (1.5·10⁶, 3.48·10¹⁰]; Theorem 2 above |
| 7 | contains 37 proven primes (29 … 1583); 22 primes in [1597, 4621] unresolved (node limit) | first feasible prime 967; every prime in (4621, 2·10⁵] feasible; unknown up to 1.70·10¹³ |
| 8 | contains 82 proven primes (17 … 2441) | first feasible 1553; DFS stopped at 8353 (159 unresolved); unknown beyond |
| 9 | contains 82 proven primes (19 … 3583) | first feasible 3529; DFS stopped at 10333 (115 unresolved); unknown beyond |

Above T_W(κ) the scanner's canonical β never failed. In the scanned ranges
it typically worked from about 3000 for κ = 4, and from below 2·10⁵ for
κ = 5.

The note's symmetric form α = β = t is strictly weaker, even with zero
entries allowed **[exact, `two_level.py … sym`]**. For κ = 3 it fails at
{7, 13, 19, 61}, while the general form works at every prime. For κ = 4
its largest failure is 109 (general: 53). For κ = 5 its largest failure
is 691 (general: 181). The note's all-nonzero version (`symnz`) also
fails at κ = 2 for p ∈ {3, 5}.

**What this means for Schedule 2 [proved + exact].** Arity
(a+1)((κ−1)a+1) holds for every prime p ∉ E_2(κ). That covers every prime
for κ ≤ 3, all but 6 primes for κ = 4 and all but 9 for κ = 5. The paper's
hypothesis p ≥ 16κ^{2κ+2} can be replaced by p ∉ E_2(κ) for κ ≤ 5, and by
p > T_W(κ) in general. At p ≤ T_W(κ), the solver finds (α, β) by DFS, a
constant for fixed κ. Note that κ = gcd(d, p−1) ≤ d ≤ c < p, so each listed
exceptional prime matters only for classes c with κ ≤ c < p. For example
(5, 4) needs c = 4.

## 4. All primes: L-level tensors with a Chevalley–Warning contraction

**Construction [proved].** A level-ℓ object is a family of cell vectors
T_I ∈ F_p^a, I ∈ Z_κ^ℓ, with disjoint column supports, nonzero root
weights, nonempty cell 0, and T ∈ W^{⊗ℓ} ⊗ F_p^a. A level-0 object is one
column with weight 1. Projecting onto the interior cells (all indices ≥ 1)
is injective on W^{⊗ℓ}, since W → F_p^{κ−1} (drop coordinate 0) is
injective when z_0 ≠ 0. So any (κ−1)^ℓ a + 1 level-ℓ objects have a linear
dependence α. Scale α so that one nonzero coefficient equals 1, and write
α_β = z_i b^κ. Appending axis index i gives a level-(ℓ+1) object. The old
axis relations are preserved because they are linear, and the new axis
relation is the dependence itself. These are the note's two levels,
iterated. The arity is

    M_L(a) = Π_{ℓ=0}^{L−1} ((κ−1)^ℓ a + 1) ≤ (κ−1)^{L(L−1)/2} (a+1)^L.

A *universal L-level contraction* is C ∈ P^{Z_κ^L} with C_0 ≠ 0 and
⟨C, W^{⊗L}⟩ = 0. With the basis e_m − u_m e_0 of W (u_m = z_m/z_0), the
condition is that every interior entry is forced by the border:
C_m = Σ_{∅≠S⊆[L]} (−1)^{|S|+1} Π_{t∈S} u_{m_t} C_{m|S→0}. At L = 2 this is
the note's border formula.

**Lemma 3 (coset shift) [proved].** For any axis t and shift j, let
(A w)_i = λ_i w_{i+j} with λ_i = g^{−j} z_{i+j}/z_i. Then λ_i ∈ H, and A
maps W onto W, since z^T A w = g^{−j} z^T w. Applying A on axis t sends an
annihilating P-valued C to the annihilating P-valued C'_I =
λ_{I_t − j} C_{I − j e_t}. So if C ≠ 0 with C_J ≠ 0, shifting each axis by
J_t gives a contraction with C'_0 ≠ 0.

**Theorem 4 [proved].** For every prime p, every κ | p−1 with κ ≥ 2, and
every L with κ^L > κ(κ−1)^L, a universal L-level contraction exists. Hence
the L-level scheme finds a witness for every tuple of M_L(a) columns.
*Proof.* Put C_I = y_I^κ. The conditions ⟨C, ⊗_t (e_{m_t} − u_{m_t} e_0)⟩ = 0,
m ∈ [1, κ−1]^L, form (κ−1)^L diagonal equations of degree κ in κ^L
unknowns y. By Chevalley–Warning there is a nonzero solution when
κ(κ−1)^L < κ^L. Lemma 3 moves a nonzero entry to cell 0. ∎

The contraction depends only on (p, κ, L, z), not on a or on the input. The
solver is linear algebra plus κ-th roots, poly(M_L(a), log p). For
p ∉ E_2(κ), use L = 2 (§2–3). For the finitely many primes p ≤ T_W(κ) where
two levels fail, the contraction is a constant-size precomputation. Brute
force over border entries costs at most (h+1)^{κ^L−(κ−1)^L}. That is
constant for fixed κ but astronomically large, so it is a theoretical
guarantee. The SAT solver found the small cases in seconds to minutes.

| κ | L_CW(κ) = min L with (κ/(κ−1))^L > κ | M_{L_CW}(a) ≤ | Ivanyos–Santha B_κ(a) | IS exponent κ⌈log₂(κ+1)⌉ |
|---|---|---|---|---|
| 2 | 2 | (a+1)² | 2^2.0 (a+1)^4 | 4 |
| 3 | 3 | 2^3.0 (a+1)^3 | 2^9.5 (a+1)^6 | 6 |
| 4 | 5 | 2^15.8 (a+1)^5 | 2^36.0 (a+1)^12 | 12 |
| 5 | 8 | 2^56.0 (a+1)^8 | 2^69.7 (a+1)^15 | 15 |
| 6 | 10 | 2^104.5 (a+1)^10 | 2^116.3 (a+1)^18 | 18 |
| 7 | 13 | 2^201.6 (a+1)^13 | 2^176.9 (a+1)^21 | 21 |
| 8 | 16 | 2^336.9 (a+1)^16 | 2^336.0 (a+1)^32 | 32 |
| 9 | 19 | 2^513.0 (a+1)^19 | 2^456.5 (a+1)^36 | 36 |

L_CW(κ) = ⌊ln κ / ln(κ/(κ−1))⌋ + 1 ≈ κ ln κ, against κ log₂ κ for
Ivanyos–Santha: the exponent shrinks by about ln 2. For κ ≤ 3 this is
moot, since two levels work at every prime (§3). At the class-9 reference
profile (grade dimensions a_d = 17, 16, 14, 12, 9, 6, 3, 1 for d = 2..9, all
κ_d = d), Σ_d log₂ B_d(a_d) = 1565 bits for Schedule 1. The worst-case
all-prime L_CW fallback gives 1392 bits. Taking the per-grade minimum of the
two (Schedule 1 is smaller at d = 9, a = 1) gives 1370 bits. Two levels give
64 bits wherever p ∉ E_2(κ_d) for all d **[exact arithmetic; script
in §8]**. So the real lever is the two-level threshold, not the fallback.

## 5. Lower bounds: where small arity is impossible

M*(p, κ, a) is the weighted Davenport constant D_H(C_p^a) with weight set H.
Everything below M* is impossible for every algorithm, and nothing at or
above it is.

- **Upper bound [proved].** M* ≤ κa + 1 by Chevalley–Warning
  (Ivanyos–Santha p. 2; Göös et al. Thm 10 Part 1 for the zero-sum form).
  The Thangadurai bound D_A(G) ≤ ⌈D(G)/|A|⌉, as restated by
  Adhikari–Grynkiewicz–Sun after their Thm 1.1, gives the same value
  ⌈(a(p−1)+1)/h⌉ = κa + 1.
- **Product lower bound [proved].** M*(p,κ,a) ≥ a(M*(p,κ,1) − 1) + 1. This
  is Marchan–Ordaz–Schmid Lemma 2.4 iterated, or directly: place a
  zero-sum-free sequence of C_p in each coordinate. Since κ ≥ 2, two columns
  λ, μλ with −μ ∉ H have no witness, so M*(p,κ,1) ≥ 3 and M* ≥ 2a + 1.
- **κ = p − 1 [proved].** Here H = {1}, so this is the plain Davenport
  constant, and Olson's theorem gives M* = a(p−1) + 1 = κa + 1. Chevalley–
  Warning is exact. (The theorem was taken from Adhikari–Grynkiewicz–Sun
  ref. [18]; Olson 1969 itself was not opened.) The paper's p = 5, a = 2
  example is the extremal sequence: 9 = D(C_5²).
- **κ = 2 [proved].** M* = 2a + 1 exactly: Adhikari–Rath Thm 3 gives
  D_A(Z_p) = 3 for quadratic-residue weights at every odd p, and with the
  two bounds above this is exact for every a. κ = 3 at a = 1: D_A(Z_p) = 3
  for all p ≡ 1 mod 3 (Mondal–Paul–Paul Thm 7, relying on cited sumset
  facts the helper did not check).

**Exact values [exact; `davenport.py`, exhaustive DFS over class
multisets, Chevalley–Warning cap].** a = 1, every κ | p−1 with κ ≥ 2 and
p ≤ 31:

| p | M*(p,κ,1) by κ (κa+1 = κ+1 in brackets) |
|---|---|
| 5 | κ2: 3 [3], κ4: 5 [5] |
| 7 | κ2: 3, κ3: 3 [4], κ6: 7 [7] |
| 11 | κ2: 3, κ5: 4 [6], κ10: 11 |
| 13 | κ2: 3, κ3: 3, κ4: 4 [5], κ6: 4 [7], κ12: 13 |
| 17 | κ2: 3, κ4: 3, κ8: 5 [9], κ16: 17 |
| 19 | κ2: 3, κ3: 3, κ6: 4, κ9: 5 [10], κ18: 19 |
| 23 | κ2: 3, κ11: 5 [12], κ22: 23 |
| 29 | κ2: 3, κ4: 4, κ7: 4 [8], κ14: 5 [15], κ28: 29 |
| 31 | κ2: 3, κ3: 3, κ5: 3 [6], κ6: 5, κ10: 5, κ15: 5 [16], κ30: 31 |

At h = 2 (H = {±1}) every value equals ⌊log₂ p⌋ + 1, the ±-weighted
Davenport bound (Marchan–Ordaz–Schmid (1)). a = 2:

| p | M*(p,κ,2) | κa+1 | Schedule 2 arity |
|---|---|---|---|
| 3 | κ2: 5 | 5 | 9 |
| 5 | κ2: 5; κ4: 9 | 5; 9 | 9; 21 |
| 7 | κ2: 5; κ3: 6; κ6: 13 | 5; 7; 13 | 9; 15; 33 |
| 11 | κ2: 5; κ5: 7; κ10: 21 (Olson; search timed out at ≥ 21) | 5; 11; 21 | 9; 27; 57 |
| 13 | κ2: 5; κ3: 5; κ4: 7; κ6: 8; κ12: 25 (Olson) | 5; 7; 9; 13; 25 | 9; 15; 21; 33; 69 |
| 17 | κ2: 5; κ4: 6; κ8: 9†; κ16: 33 (Olson) | 5; 9; 17; 33 | 9; 21; 45; 93 |
| 19 | κ2: 5; κ3: 5; κ6: ≥ 8 (timeout); κ9: 9†; κ18: 37 (Olson) | 5; 7; 13; 19; 37 | 9; 15; 33; 51; 105 |

† The search timed out at the lower bound 9. The upper bound below matches
it, so the value is exact.

**Pigeonhole upper bound when −1 ∈ H (h even) [proved].** Among
2^M > p^a subset sums of the columns, two coincide, and their difference is
a nonzero x ∈ {0, ±1}^M ⊂ P^M. So M* ≤ ⌊a log₂ p⌋ + 1, which is
Marchan–Ordaz–Schmid (1) when H = {±1}. This bound is non-constructive.
p = 7, κ = 3, a = 2 has M* = 6 > 2a + 1 = 5, so the product bound is not
always tight. At h = 2 every computed value equals ⌊a log₂ p⌋ + 1.

**Conclusion [proved + exact].** Impossibility lives only below
M* ∈ [max(2a+1, a(M*(p,κ,1)−1)+1), κa+1]. M* is linear in a for every
(p, κ). It is near κa + 1 only when h is tiny, and equal to it only when
h = 1. No (p, κ, a) needs super-linear arity for existence. The task's
"κ = p−1 forces about a(p−1)+1 columns" is this h = 1 case, and it is
κa + 1, so it is also linear.

**Lower bounds for METHODS [exact].** Universal contractions are a method,
and they can fail where witnesses exist. Two levels: the note proves none
exists at κ = p−1, p ≥ 5. The exact sets in §3 extend this to all listed
exceptional primes. SAT results by level count
(`llevel.py sat`; every SAT answer passed the direct check against a basis
of W^{⊗L}):

| L | SAT (contraction exists) | UNSAT | timed out (40 min) |
|---|---|---|---|
| 2 | (7,3), (41,4), (191,5) | (5,4), (7,6), (13,4), (17,4), (181,5) | — |
| 3 | (13,4), (17,4), (29,4), (37,4), (53,4), (11,5), (31,5), (41,5), (61,5), (181,5), (13,6) | (5,4), (7,6), (11,10) | (19,6) |
| 4 | (5,4) | — | (7,6) |

So every κ = 4 exceptional prime has L* = 3, except p = 5 with L* = 4.
The tested κ = 5 exceptional primes (11, 31, 41, 61, 181) have L* = 3.
The UNSAT cases at L = 3 are all κ = p − 1 (the zero-sum case). Chevalley–
Warning guarantees L_CW = 5, 10, 22 for these three.
These are statements about universal contractions only. They do not rule
out instance-adaptive contractions or other algorithms.

## 6. Existence versus efficient finding

At small p, the obstacle to Schedule 2's arity is not existence. Since
(a+1)((κ−1)a+1) ≥ κa + 1 always, a witness exists for every tuple at that
arity at every prime (also noted in the 11-01 check §5.2). What fails at
the exceptional primes is the universal two-level contraction. §4 repairs
this: L levels with a precomputed constant-size contraction.

On brute force when p ≤ f(κ):
- Brute force over the witness s ∈ P^M costs (h+1)^M ≥ 2^M. It is
  exponential in a at any arity ≥ a + 1, so it never gives a poly-time
  solver, even at constant p **[proved, trivially]**.
- Brute force over objects that do not depend on a does work. Examples are
  the two-level scalars (α, β), with search ≤ (h+1)^{κ−1} κ² p, and the
  L-level contraction, with search ≤ (h+1)^{κ^L}. When p ≤ T_W(κ) these
  cost a constant for fixed κ. This is exactly how §3–4 turn "small p" into
  a polynomial solver **[proved]**.
- Linear arity, κa + 1 ≤ M ≤ O(a), needs a genuinely different idea. At
  κ = p − 1 this is the search problem BIS_p of Göös–Kamath–Sotiraki–
  Zampetakis (Def. 6.1, n ≥ (m+1)(p−1)). At h = 2 it is SIS_p (Def. 6.2).
  Both are in PPA_p via Chevalley (their Thm 10), and no hardness is
  known. Their Open Problem 6 asks whether BIS_q has *any* non-trivial
  polynomial-time regime. For prime q, Ivanyos–Santha Thm 3 (d = q−1, not
  cited there) and Theorem 4 here give regimes with n = poly_q(m). A regime
  with n = O_q(m) is open as far as this pass found. Ivanyos–Santha §1 say
  they do not know how to find a solution under only the Chevalley–Warning
  condition when m > 1 **[literature, full texts read]**.

So the regimes are as follows. Existence holds at linear arity everywhere.
Efficient finding is known at arity (a+1)((κ−1)a+1) for p outside a finite
exceptional set E_2(κ). On E_2(κ) it is known at O_κ(a^{L*}), with L* the
least level count that has a universal contraction (3 or 4 in every tested
case, ≤ L_CW(κ) always). Nothing efficient is known below quadratic arity.
That is a gap of a factor about (κ−1)a/κ between the proven existence
threshold and the best efficient arity in the good regime, and a gap of
order a^{L*−1} on E_2(κ).

## 7. Literature used (helper read full texts unless marked)

- Weil bound: Martin–Yip, arXiv:2403.04312v2, Lemma 2.2 (read). It cites
  Lidl–Niederreiter, *Finite Fields*, Thm 5.41 (not opened). Hypotheses: χ
  of order d > 1; f monic, not a d-th power; m distinct roots; the bound
  |Σ_z χ(a f(z))| ≤ (m−1)√q holds for all a.
- Adhikari–Rath, Integers 6 (2006) A30, Thm 3 (read). Mondal–Paul–Paul,
  arXiv:2110.02539v4, Thm 7 (read).
- Adhikari–Grynkiewicz–Sun, arXiv:1003.2186, Thm 1.1 (read).
  Marchan–Ordaz–Schmid, arXiv:1308.3316, Lemma 2.4 and bound (1) (read).
  Thangadurai and Olson 1969: not opened, cited via AGS.
- Göös–Kamath–Sotiraki–Zampetakis, arXiv:1912.04467v2 (CCC 2020): Thm 2
  (only ChevalleyWithSymmetry_p is PPA_p-complete), Defs 6.1–6.2, Thm 10,
  Open Problems 5–6 (read; OP 6 wording checked in the text by me).
- Ivanyos–Santha, arXiv:1503.09016v2: §1, Fact 2, Thm 3, Props 9–10,
  Thm 11 (read).

## 8. Artifacts and reproduction

All in `2026-11-02-rees-schedules/small-prime/`. Build the C programs with
`cc -O2 -o <name> <name>.c`; run Python with `/opt/anaconda3/bin/python`.

| script | what it does | key runs (this pass) |
|---|---|---|
| `two_level.py` | complete DFS for the two-level (α, β) contraction; modes `general`, `sym` (α = β, zeros allowed), `symnz` (the note's all-nonzero form); `list k sec p…` runs listed primes with a time limit | `2 3 1000 {general,sym,symnz}`; `4 6 3000 general` |
| `dfs2.c` | the same complete DFS in C with bitsets; prints INFEASIBLE / LIMIT, re-checks every κ² condition of each witness | κ = 2..6 on [3, 3000] reproduce `two_level.py` exactly; κ = 6..9 ranges in §3 |
| `scan2.c` | witness scan for large p (explicit β_i = g^{−i} − 1 first, then random β; α_j sampled) with exact re-check | κ = 4 on [3000, 263683]; κ = 5 on [3000, 87,930,000] in 9 chunks (a κ = 6 run on [3·10⁶, 10⁷] timed out with no unresolved prime but an unrecorded endpoint, so it is not counted) |
| `llevel.py` | L-level objects, border-form contraction, direct annihilator check against a basis of W^{⊗L}, SAT search (pycosat), end-to-end solver with exact witness check | §4–5 SAT table; `solve` runs below |
| `davenport.py` | exhaustive M*(p, κ, a) | `1 31`, `2 19 200` |

End-to-end exact witnesses (random, repeated-basis and scaled two-column
families), each from a contraction that passed the direct check:
- p=7, κ=3, L=2, a=2, M=15: 9/9. (The note's symmetric form has no
  solution at this prime.)
- p=3, κ=2, L=2, a=3, M=16: 6/6.
- p=41, κ=4, L=2, a=3, M=40: 6/6.
- p=191, κ=5, L=2, a=2, M=27: 6/6.
- p=13, κ=4, L=3, a=2, M=399: 6/6.
- p=11, κ=5, L=3, a=1, M=170: 6/6.
- p=5, κ=4, L=4, a=1, M=2240: 6/6.
- p=5, κ=4, L=4, a=2, M=21945: 3/3.

Cross-validation: SAT (border form) and DFS ((α, β) form) agree at L = 2 on
(5,4), (7,6), (13,4), (17,4), (181,5) UNSAT and on (7,3), (41,4), (191,5)
SAT. The C and Python DFS agree on every prime ≤ 3000 for κ = 2..6. Above
T_W(4) and T_W(5) the canonical β never failed in `scan2` (0 failed β
attempts on [3000, 263683] for κ = 4 and on [2·10⁵, 8.79·10⁷] for κ = 5),
as Theorem 2 requires above T_W.

## 9. Claim gates, open questions, next step

Must stay false: "Schedule 2 is optimal"; "small arity is impossible at
small primes"; "BIS_p/SIS_p (zero-sum search) is hard"; any priority or
novelty claim for Theorems 2 and 4. Theorem 4 is a short combination of
Chevalley–Warning with the Ivanyos–Santha/note collision scaffold, and it
has had no expert or literature-priority review. Also false: "the
exceptional sets for κ ≥ 6 are known", and "the L-level fallback is
practical" (its precomputation bound is astronomical).

Open:
1. Prove a two-level threshold near the observed one. The observed largest
   exceptional prime is 1.45–1.66 κ^{(κ+1)/2} for κ = 4, 5, 6, while the proof gives about
   κ^{2κ}(κ−2)². The heuristic is that (h+1)^{κ−1} choices of β each
   succeed with chance about (p/κ^κ)^{κ−1} **[argued]**. A proof would have
   to use the freedom in β, which Weil applied per α_j does not.
2. The exact E_2(κ) for κ ≥ 6, and the minimal level count L*(p, κ) on it.
   In particular, is L* ≤ 4 for every κ = p − 1?
3. Any polynomial-time algorithm at arity o(a²) for fixed κ ≥ 2, or at
   O(a) for fixed p. The latter is Göös et al. Open Problem 6 for BIS_p.
4. M*(p, κ, a) beyond the tables. For h = 2, does M* equal the ±-Davenport
   upper bound ⌊a log₂ p⌋ + 1 for all a? It does at a ≤ 2, p ≤ 13. That is
   too little data for a conjecture.

Next command (mechanical; not added to `MECHANICAL_FOLLOW_UP_PLAN.md`
because this pass may edit only this note):
`./dfs2 7 1597 20000 5000000`, and the same for κ = 8, 9. Expected
artifact: the INFEASIBLE/LIMIT lines. Acceptance: every LIMIT is resolved to
INFEASIBLE or FEASIBLE, and the largest INFEASIBLE prime is reported per κ.
If the authors want Schedule 2's hypothesis in `main.tex` replaced, the
candidate is "p > T_W(κ), or (p, κ) outside the listed exceptional sets for
κ ≤ 5". That is the paper owner's call, and nothing here was changed.

# Rees diagonal SDE: average-case arity (i.i.d. uniform columns)

**Status: COMPLETE (negative result). No o(a²) average-case method found; the isotropic-merge recursion is exponential (3^a, or Θ(2^a) adaptively). All sweeps finished.**
4 November 2026. AI-only pass (one session, restarted once). AI-checked, pending
human review. Labels: **[proved]** (proof written here, or a cited theorem of the
paper), **[exact]** (complete finite computation, script named), **[float]**
(sampling), **[argued]**. Scripts and outputs are in `2026-11-04-rees-avg-case-arity/`;
the interpreter is `/opt/anaconda3/bin/python`. Only this file and that folder were
written. The worst-case o(a²) question belongs to another session and is not
treated here.

**Problem.** Columns v_1..v_M are i.i.d. uniform in F_p^a (this is what Schedule 3
supplies: labels i.i.d. uniform on K_d^⊥, `lem:s3-law`; by `lem:fc-rref`(a) a uniform
law on an a-dimensional subspace is the same problem). Fix κ = gcd(d, p−1) with
2 ≤ κ < p−1, h = (p−1)/κ, P = P_κ (nonzero κ-th powers), D = P ∪ {0}, q = (h+1)/p ≈ 1/κ.
Find x ∈ D^M, x ≠ 0, with Σ x_j v_j = 0 (then s_j = x_j^{1/κ} and a Bezout exponent).
Question: is there a poly(a, log p) (or poly(a)·κ^{o(a)}) algorithm at M = o(a²)?

## 0. Answers

1. **No o(a²) average-case method was found, for κ = 2 or κ = 3 [argued].** Every
   approach tried lies on one trade-off: M columns cost time about κ^{a − M/a}. The
   approaches are merge trees, two-level contractions on random columns, the
   triangular/free-coordinate hybrid and block splitting. So poly(a) time needs
   M ≥ a²/2 − O(a log a / log κ), and κ^{o(a)} time needs M = Ω(a²). This is a
   frontier of known methods, **not** a lower bound.
2. **The "merge by isotropic vectors" recursion is exponential [proved + exact].**
   Merged columns do stay uniform and independent (Proposition 1, the argument of
   `lem:fc-split-law`). But one merge kills one coordinate, so the tree is a product.
   - Fan-in 3 (κ = 2 isotropic ternary forms; κ = 3 points on diagonal cubic curves)
     uses exactly **3^a** columns.
   - Adaptive pairing needs at least **½·(2/(1+1/p))^a** columns for success ≥ 1/2
     (Proposition 2). The observed count is about 3·2^a at κ = 2 and 2·2^a at κ = 3.
   - The tree size is neither a^{log 3} nor a²; it is exponential. Already at
     **a = 2** the fan-in-3 tree uses 9 columns, against 6 for the triangular
     solver. The pairing lower bound beats (a+1)(a+2)/2 from **a = 6** on.
3. **Trees cannot beat one level [proved].** Take a public-split tree (the
   `app:fc-split` design with any public maps π_j, any per-level solver) with level
   dimension drops a_j, success probability σ > 1/(p−1), M columns and time T.
   - Its column count is at least Π(a_j+1) ≥ (a_max+1)(a − a_max + 1).
   - If M < (a/2+1)(a/4+1), its largest level solves the same i.i.d.-uniform problem
     in dimension a' ≥ a + 1 − 2M/a, with at most M columns, success σ and time T.
   - So a tree with M = o(a²) is an o(a'²) solver for a' = a − o(a) in disguise.
     Merging cannot create an o(a²) method (Proposition 3).
4. **Random columns save nothing in the two-level contraction [proved].** First-level
   dependencies and the flexible vectors v_l of Lemma 1 / `prop:triangular-sde` are
   again i.i.d. uniform (Proposition 4). So each level still needs dimension + 1
   objects, except with probability at most 1/(p−1) per level. The product scheme
   needs (a+1)² columns and the triangular one (a+1)(a+2)/2 − O(1) in expectation.
5. **Hybrid trade-off [proved + exact].** Run K triangular rounds, then the
   free-coordinate sampler of `thm:free-coordinate` in the quotient F_p^a/U_K.
   - Columns: K(2a−K+3)/2 + (a−K) + n_0, i.e. about Ka.
   - Time: poly(a, log p)·κ^{a−K}, valid for κ = 2 and for κ ≥ 3 with p ∉ E_2(κ)
     (Proposition 5).
   - Exact witnesses at p = 2^31 − 1: κ = 2, a = 16, K = 0..16; κ = 3, a = 10.
     Measured trials match q^{−(a−K)}.
   - It interpolates between the free-coordinate theorem (K = 0) and the triangular
     solver (K = a). Block splitting with two blocks (a−K, K) sits on the same
     frontier.
6. **Smallest hard-looking instance [argued].** At M = a+2 (κ = 2) the kernel is a
   projective line. Witnesses with a zero entry are found by checking a+2 values
   of t. The other witnesses are the t with all a+2 values χ(α_j + tβ_j) equal,
   where χ is the Legendre symbol. Equivalently, they are the F_p-points of one of
   two fibre products of a+2 double covers of P¹, of genus 1 + 2^a(a−1) by
   Riemann–Hurwitz. This pass did not search
   the literature for a subexponential algorithm; UNKNOWN (trap 10).

## 1. Setting and elementary facts

- **(E1) Generic-rank facts [proved].** An m-tuple of i.i.d. uniform vectors in
  F_p^c with m ≤ c is linearly independent with probability
  Π_{i=0}^{m−1}(1 − p^{i−c}) ≥ 1 − 1/(p−1). Then the only x ∈ F_p^m with
  Σ x_l u_l = 0 is x = 0, so no witness exists. Hence a solver step that must
  annihilate c coordinates of fresh uniform vectors needs at least c+1 of them,
  except with probability at most 1/(p−1).
- **(E2) Existence [proved, `lem:fc-moment`].** For M = a + n, the expected number
  of witnesses with prescribed pivots is h^n q^a. So witnesses exist once
  n ≳ a·log κ/log(p/κ). For large p this is arity a + O(1). The gap between
  existence (≈ a) and efficient finding (≈ a²/2 in poly time) is the subject here.
- **(E3) Free coordinates [paper].** `thm:free-coordinate` finds a witness at
  arity a + O(1) with about 2B ln 2·q^{−r} ≤ 2B ln 2·κ^a trials, r ≤ a.
  `prop:rc-lower`: no bank-oblivious design does better than about q^{−a} trials,
  at any arity.

## 2. Proposition 1: merged columns stay uniform

**Proposition 1 [proved].** Let V_{j−1} ≤ F_p^a and let π_j be a public linear map
with V_j = V_{j−1} ∩ ker π_j. Let z_1..z_N be independent and uniform on V_{j−1}, and
independent of a record ℛ. A merge step reads ℛ, the images π_j(z_l) and fresh coins.
It partitions a subset of [N] into disjoint groups G_1..G_s and outputs, for each
group, y^{(g)} ∈ D^{G_g} \ {0} with Σ_{l∈G_g} y_l π_j(z_l) = 0, and
w_g = Σ_{l∈G_g} y_l z_l. Pass-through is the group {l} with π_j(z_l) = 0 and y = 1.
This covers fixed fan-in and adaptive pairing. Then, conditional on ℛ, on all
π_j(z_l), on the coins and on the groups and y's, the outputs w_1..w_s are
independent and uniform on V_j.

*Proof.* Choose a complement W of V_j in V_{j−1}; π_j is injective on W. Write
z_l = ω_l + ρ_l with ω_l ∈ W, ρ_l ∈ V_j. For z_l uniform on V_{j−1}, ω_l and ρ_l are
independent and uniform, and ω_l is a function of π_j(z_l). So, given everything
the step reads, the ρ_l are still i.i.d. uniform on V_j. In each group,
Σ y_l ω_l ∈ W and π_j(Σ y_l ω_l) = Σ y_l π_j(z_l) = 0, so Σ y_l ω_l = 0 and
w_g = Σ_{l∈G_g} y_l ρ_l. Since y^{(g)} ≠ 0, this is a surjective linear image of
independent uniform vectors, hence uniform on V_j. The groups are disjoint, so the
w_g are independent. ∎

This is the induction step of `lem:fc-split-law`(c), extended to adaptive groupings.
**Exact check** [exact; `uniformity_exact.py`, output `uniformity_exact.out`]. Take
p ∈ {7, 11, 13} with κ = 2, and p ∈ {7, 13} with κ = 3, a = 2, and fan-in 2 and 3
with a deterministic first-solution rule. All p^m × p^m configurations were
enumerated. For every non-aborting record the residual coordinate is exactly
uniform; there were 0 exceptions. Pair aborts occur at rate
(κ−1)/κ·(1−1/p)² + O(1/p), e.g. 96/169 at (13, 3); triple aborts at rate 0.

## 3. Proposition 2: the isotropic merge tree, κ = 2 (and κ = 3)

The tree: level j kills coordinate j (π_j = j-th coordinate, a_j = 1). A raw column's
weight is the product of the y's on its root path, which lies in D because D is
closed under products. The root is the zero vector, with a nonzero weight
vector. This is the paper's split design with k = a blocks of size 1.

**Proposition 2 [proved].**
(a) *Fan-in 3.* For κ = 2 every node succeeds: c_1x_1 + c_2x_2 + c_3x_3 = 0 has a
solution x ∈ D³ \ 0. If some c_i = 0, take x = e_i. Otherwise the ternary form
Σ c_i s_i² is isotropic. The randomized step draws x_1, x_2 ∈ P and tests
x_3 = −(c_1x_1 + c_2x_2)/c_3 ∈ D. It succeeds with probability at least
(p² − 4p)/(2(p−1)²) ≥ 1/2 − 2/(p−1).
- *Count.* A nondegenerate ternary form has exactly p² affine zeros. At most
  2(2p−1) of them have s_1 s_2 = 0. Each admissible (x_1, x_2) corresponds to at
  most 8 zeros.

The tree uses exactly 3^a columns, and (3^a − 1)/2 nodes, each of expected cost
O(1)·poly(log p).
- For κ = 3 a node succeeds iff the plane cubic Σ c_i X_i³ has an F_p-point, which
  Hasse–Weil guarantees (p ≡ 1 mod 3, p > 3, all c_i ≠ 0). The per-try success is
  1/3 + O(p^{−1/2}) [argued].

(b) *Adaptive pairs.* At each level, vectors with zero j-th coordinate pass up alone,
and the other vectors are grouped in pairs. Let N_j be the number of vectors
entering level j+1, and Z the number of pass-throughs. Then N_{j+1} ≤ (N_j + Z)/2,
and E[Z | N_j] = N_j/p (each coordinate is uniform and independent of the
record, by Proposition 1). So E N_{j+1} ≤ ((1+1/p)/2)·E N_j. The tree succeeds only
if N_a ≥ 1, so Pr[success] ≤ E N_a ≤ N_0((1+1/p)/2)^a. Success probability 1/2
therefore needs N_0 ≥ ½(2/(1+1/p))^a. ∎

(c) *Uniformity* holds at every node, by Proposition 1. **The recursion is valid,
but its size is exponential.** It is the k = a, all-blocks-of-size-1 case of
`prop:fc-split`, whose arity is a product of k factors ≥ 2.

**Exact/float data** (`merge_tree.py`, outputs `merge_triple.out`, `merge_pair.out`,
p = 2^31 − 1; every witness checked exactly mod p, with x_j^h = 1 on its support):

| κ | a | fan-in 3: columns | mean tries/node | adaptive pairs: pool for success ≥ 1/2 | 2^a | triangular (a+1)(a+2)/2 |
|---|---|---|---|---|---|---|
| 2 | 2 | 9 | 2.00 | 6 | 4 | 6 |
| 2 | 4 | 81 | 1.97 | 34 | 16 | 15 |
| 2 | 6 | 729 | 1.96 | 176 | 64 | 28 |
| 2 | 8 | 6561 | 2.01 | 768 | 256 | 45 |
| 2 | 10 | — | — | 2816 | 1024 | 66 |
| 2 | 12 | — | — | 12032 | 4096 | 91 |
| 3 | 4 | 81 | 3.08 | 29 | 16 | 15 |
| 3 | 8 | 6561 | 2.99 | 496 | 256 | 45 |

The pool column is [float]: a doubling-and-bisection search, 40 instances per test,
resolution about 1/64 of the pool size. The fan-in-3 rows are [exact] (3/3
witnesses each, a ≤ 9 at κ = 2 and a ≤ 8 at κ = 3). At κ = 2 the pool/2^a ratio
levels off near 3. At p ≡ 3 mod 4, pairs must come from opposite square classes,
so min(|A|, |B|) loses O(√N) per level. At κ = 3, −1 is a cube and pairs form
inside a class, giving a ratio near 2.

## 4. Proposition 3: trees reduce to a single level

**Lemma T [proved; exact check `tree_bound.py` for all partitions of a ≤ 40].**
For integers a_j ≥ 1 with Σ a_j = a:
(T1) Π(a_j+1) ≥ (a_max+1)(a − a_max + 1);
(T2) if a_max ≤ a/2, then Π(a_j+1) ≥ (a/2+1)(a/4+1) ≥ a²/8.
*Proof.* (x+1)(y+1) ≥ x+y+1 gives Π_{j∈S}(a_j+1) ≥ 1 + Σ_{j∈S}a_j for every S. For
(T1), take S = all levels but the largest. For (T2), greedy balancing splits the
levels into two groups whose sums differ by at most a_max ≤ a/2. The groups then
have sums ≥ a/2 and ≥ a/4. ∎

**Proposition 3 [proved].** Consider a public-split tree in the sense of
`app:fc-split`: public maps π_j, level drops a_j = dim V_{j−1} − dim V_j ≥ 1, M_j
children per node at level j, and any per-node solver. Suppose it returns a witness
with probability σ > 1/(p−1) on M = Π M_j i.i.d. uniform columns in F_p^a, in time T.
(i) M_j ≥ a_j + 1 for all j, so M ≥ (a_max+1)(a − a_max + 1).
(ii) If M < (a/2+1)(a/4+1), let j* be the largest level. Its sub-solver is an
algorithm for the same problem: M_{j*} ≤ M/(a − a_max + 1) i.i.d. uniform columns in
dimension a' = a_{j*} ≥ a + 1 − 2M/a. It succeeds with probability at least σ, in
time at most T.
*Proof.* (i) A node's sub-bank is M_j i.i.d. uniform vectors in π_j(V_{j−1}), of
dimension a_j (Proposition 1). If M_j ≤ a_j, (E1) shows the node fails with
probability ≥ 1 − 1/(p−1). The tree fails whenever one node fails. Then use (T1).
(ii) By (T2), a_max > a/2. By (T1), a − a_max + 1 ≤ M/(a_max+1) < 2M/a. Every node
must succeed for the tree to succeed, and by Proposition 1 the sub-bank of any
level-j* node is an i.i.d.-uniform instance of dimension a_{j*}. ∎

So for M = o(a²) the tree contains a solver for dimension a − o(a) with o(a²)
columns: exactly the open question, one size down. The examples M = a^{1.5} and
M = a^{log₂3} force a_max ≥ a + 1 − 2a^{0.5} and a_max ≥ a + 1 − 2a^{0.585}. The
exact minima are in `tree_bound.out`; e.g. at a = 40 the least a_max with
Π(a_j+1) ≤ a^{1.585} is 30. In particular there is **no** tree of size a^{log 3}
whose levels all have dimension o(a). Scope: trees whose subspaces V_j are chosen
from the data are not covered by Proposition 1. (The triangular solver is of that
kind; see Proposition 4.)

## 5. Proposition 4: random columns do not shorten contraction levels

**Proposition 4 [proved].** Let κ ≥ 2 and p ∉ E_2(κ), with (α, β) normalised as in
`prop:triangular-sde`. Run the round of `prop:triangular-sde` on m fresh i.i.d.
uniform columns modulo a subspace U of dimension k, where U is independent of the
fresh columns, and put c = a − k.
(a) If m ≤ c, there is no dependency modulo U, except with probability ≤ 1/(p−1)
(E1, applied to the images in F_p^a/U).
(b) Take m = c+1 and let E′ be the event that the images ū_1..ū_{c+1} in F_p^a/U have a
1-dimensional dependency space; Pr[E′] ≥ 1 − 1/(p−1), by (E1) on the first c images.
Condition on E′, on the normalised dependency δ (first nonzero entry 1) and on
N = {i : cos(δ_i) ≠ 0}. If N ≠ ∅, the flexible vector v = Σ β_{cos δ_i}δ_i u_i is
uniform on (F_p^a/U) \ {0} modulo U, and independent of U and of earlier rounds. If
N = ∅, then v = 0 and the round stops the solver. This happens with probability
≤ q^c + 1/p ≤ (κ^{−1} + 1/p)^c + 1/p, since the dependency line is uniform among lines.
*Proof of (b).* Given U, the images are i.i.d. uniform on F_p^a/U ≅ F_p^c, so their law
restricted to S_δ = {(ū): dependency space = F_p δ} is uniform. Left multiplication by
g ∈ GL_c(F_p) maps S_δ to itself and sends v̄ to g v̄. So the law of v̄ given (δ, N) is
GL_c-invariant, i.e. uniform on F_p^c \ {0}, with some mass at 0. That mass is zero
when N ≠ ∅. Indeed β_m ≠ 0 for m ≠ 0, because 1 + β_m ∈ A_{−m} and 1 ∉ A_{−m}. So the
coefficient vector (β_{cos δ_i}δ_i·1[i∈N])_i is nonzero. It vanishes at the first
entry of δ, which has coset 0, so it is not proportional to δ. Then v̄ = 0 would be a
second, independent dependency, which contradicts S_δ. The fresh columns are
independent of U and of earlier rounds. Finally, the law of a uniform c × (c+1)
matrix is invariant under right multiplication by GL_{c+1}, so the dependency line
is uniform among lines. With probability ≥ 1 − 1/p its first coordinate is nonzero.
Then δ = (1, w) with w uniform on F_p^c, and all entries lie in D with probability
q^c. ∎

*Consequences.*
- In Schedule 2's product form, the second level faces i.i.d. uniform vectors in
  F_p^a and needs a+1 of them. The first level needs a+1 columns per object. So
  the count is (a+1)², with no average-case saving.
- In the triangular solver every round with c ≥ 1 needs c+1 columns. The expected
  saving from early stops is Σ_c κ^{−c}·O(c²) = O(1). So the average-case count is
  (a+1)(a+2)/2 − O(1).
- The randomness of the supply cannot shrink the levels of the two-level
  contraction. Any saving must come from a different mechanism, such as the
  free-coordinate gamble below.

## 6. Proposition 5: the triangular/free-coordinate hybrid

**Proposition 5 [proved].** Let κ = 2 with p ≥ 5, or κ ≥ 3 with p ∉ E_2(κ) (every p
with κ < p−1 when κ = 3). Let 0 ≤ K ≤ a, n_0 ≥ 1, B ≥ 1, and put g = a − K. Let
the columns be i.i.d. uniform in F_p^a, with
  M_K = Σ_{i<K}(a−i+1) + g + n_0 = K(2a − K + 3)/2 + a − K + n_0.
1. Run K rounds of `prop:triangular-sde` on the first Σ_{i<K}(a−i+1) columns. They
   are deterministic and valid for every input. If a round stops early, go
   straight to back-substitution.
2. Let Φ: F_p^a → F_p^g be a surjection with kernel U_K. Run (F2)–(F4) of
   `thm:free-coordinate` (sampler only) on the images Φ(v_j) of the remaining
   g + n_0 columns. This gives y ∈ D^{g+n_0} \ 0 with Σ y_j v_j ∈ U_K.
3. Back-substitute τ = −Σ y_j v_j through the K flexible vectors.

The result is a nonzero witness, except with probability at most
β(g + n_0, n_0; g) + 2^{−B} (eq. `fc-beta`). It uses at most 2B ln 2·q^{−g} + 1
trials, and time poly(a, B, log p)·(1 + κ^g).

*Proof.* The rounds and the back-substitution are the proof of
`prop:triangular-sde`, verbatim. The only change is that the final object is the
free-coordinate one: its sum lies in U_K, its weights lie in D, and it is nonzero
on its own columns. Supports are disjoint. Φ is a function of the round columns
only, so the remaining columns are independent of Φ. Φ is surjective, so their
images are i.i.d. uniform on F_p^g. Now `lem:fc-node`(a)–(c) and `lem:fc-rref` apply
with a = g: the bank is bad with probability ≤ β, and on a good bank the T_r trials
all fail with probability ≤ 2^{−B}, with r ≤ g. ∎

*Choice of n_0.* `lem:fc-choice` with g in place of g_d gives the arity of the
free-coordinate part,
  g(1 + 2 ln κ/ln(p/κ)) + 3 ln(8/τ)/ln(p/κ) + 3,
for bank failure ≤ τ. For p ≥ κ^{Ω(a)} this is g + O(1).

*Trade-off.* M ≈ Ka + O(a) buys time κ^{a−K}. So poly(a) time forces
K ≥ a − O(log a/log κ), i.e. M ≥ a²/2 − O(a log a). Arity a^{1+ε} costs κ^{a − a^ε}.
Block splitting `prop:fc-split` with two blocks (a−K, K) has arity
(a − K + O(1))(K + O(1)) ≈ Ka and time κ^{a−K}: the same frontier to leading order.
The hybrid needs uniformity only in its last g + n_0 columns.

**Exact data** (`hybrid_fc.py`, p = 2^31 − 1, n_0 = 3, 10 instances per row; every
witness checked exactly; outputs `hybrid_k2.out`, `hybrid_k3.out`):

| κ | a | K | columns M_K | (a+1)(a+2)/2 | witnesses | mean trials | q^{−(a−K)} |
|---|---|---|---|---|---|---|---|
| 2 | 16 | 0 | 19 | 153 | 10/10 | 53567 | 65536 |
| 2 | 16 | 4 | 77 | 153 | 10/10 | 4477 | 4096 |
| 2 | 16 | 8 | 119 | 153 | 10/10 | 250 | 256 |
| 2 | 16 | 12 | 145 | 153 | 10/10 | 11.6 | 16 |
| 2 | 16 | 16 | 155 | 153 | 10/10 | 0.4 | 1 |
| 3 | 10 | 0 | 13 | 66 | 10/10 | 57949 | 59049 |
| 3 | 10 | 4 | 47 | 66 | 10/10 | 479 | 729 |
| 3 | 10 | 8 | 65 | 66 | 10/10 | 9.7 | 9 |
| 3 | 10 | 10 | 68 | 66 | 10/10 | 0.8 | 1 |

All rows are in the output files (κ = 2: K = 0, 2, …, 16; κ = 3: K = 0, 2, …, 10).
- Trial counts track q^{−(a−K)} within the sampling noise of 10 runs (ratios
  0.4–1.3). Values below 1 at large K come from early stops of the triangular
  rounds, which skip the free-coordinate step.
- At K = a the hybrid uses n_0 − 1 = 2 more columns than the triangular solver,
  because its last object is a free-coordinate bank rather than a single column.
- Pre-sweep smoke tests at p = 10007 (κ = 2, a = 8) and p = 10009 (κ = 3, a = 6)
  also passed; they were run in the terminal and not saved.

## 7. Other ideas, and why they fail

- **Random kernel vector [proved].** A uniform kernel vector lies in D^M with
  probability about q^M. `prop:rc-lower`: any bank-oblivious candidate stream needs
  about q^{−a} candidates, at every arity.
- **Isotropic merges that keep the conic parameter [argued].** Keeping the rational
  parameter t of the conic, instead of fixing a point, postpones the solve. A
  family built from m raw columns has m parameters. Killing c coordinates leaves
  m − c of them, and the root still needs Σ(parameters) ≥ a + 1, i.e. ≥ a + 1 raw
  columns. Solving the merged system is then the original system of a diagonal
  quadrics in its leaves. The second-level varieties are no longer rational
  (fibre products of conics, of positive genus), so no parametrisation survives.
  Polynomial-system cost grows like (degree)^{#equations}, which is exponential
  once a node kills Θ(a) coordinates.
- **"Recursive squaring" / substitution s = Tt [argued + literature recalled].**
  Writing s = Tt turns the diagonal system into a general system of a quadratic
  forms in fewer variables. That discards the diagonal structure and lands in
  underdetermined MQ. As recalled (Kipnis–Patarin–Goubin, Thomae–Wolf,
  Miura–Hashimoto–Takagi; **not re-read in this pass**), the polynomial-time
  threshold there is about n ≥ m²/2 variables, and below it the known methods
  reduce m equations to m − ⌊n/m⌋ + O(1) and then search exhaustively. That is the
  same κ^{a − M/a} shape as Proposition 5. Diagonal MQ is a special case, so these
  algorithms apply, but they give nothing better.
- **Lattices / linearisation [argued].** For fixed κ and large p, D = P_κ ∪ {0} has
  about p/κ elements spread over all of F_p. It has no short-vector description,
  so the BKZ probe of the 2026-11-02 report (h ≤ 2 only) does not transfer.
  Linearising x ∈ D needs x^{h+1} = x, of degree (p+1)/κ.
  - KOW 2026 (arXiv:2510.07515, Definition 1.10, Theorems 1.12–1.13) treats
    average-case A-CIS only for |A| = p − k + 1 with k constant. Our |A| = h+1 has
    k ≈ p(1 − 1/κ), so it does not apply.
  - Their remark that the problem "seems quite hard unless |A| is close to q"
    (the paper's q, our p) is consistent with this pass.
- **Wagner/birthday on the free coordinates [argued].** The acceptance condition
  χ(v_i) ∈ {0, 1} for v = R_A x_A + R_B x_B does not split as a condition on one
  list against the other, because D is not an additive subgroup. Using common
  scalars on blocks of free coordinates reduces to the one-variable
  Legendre-pattern search of §0(6), at the same 2^{−r} density.
- **Literature context.** At p = 5, κ = 2 (D = {0, ±1}) the problem is average-case
  signed F_5-subset-sum / SIS_5. KMOSW (arXiv:2609.40321, §1.3) report that every
  known attack at linear m = Θ(n) is still exponential. The large-p, κ = 2 case is not
  covered by that statement, and no reduction between the two was found.

## 8. Artifacts (`2026-11-04-rees-avg-case-arity/`)

| file | content |
|---|---|
| `common.py` | field, coset and D tests; mod-p linear algebra; quotient maps; (α, β) search; exact witness check |
| `merge_tree.py` | fan-in-3 isotropic tree and adaptive pair tree (§3) |
| `uniformity_exact.py` → `uniformity_exact.out` | exhaustive law check of merged columns (§2) |
| `tree_bound.py` → `tree_bound.out` | Lemma T over all partitions of a ≤ 40 (§4) |
| `hybrid_fc.py` | Proposition 5 solver (§6) |
| `run_all.sh` → `merge_triple.out`, `merge_pair.out`, `hybrid_k2.out`, `hybrid_k3.out` | the §3 and §6 tables |

Reproduce: `cd 2026-11-04-rees-avg-case-arity && nice -n 10 ./run_all.sh` (about
3 minutes on a loaded machine). Run `/opt/anaconda3/bin/python uniformity_exact.py p κ`
and `tree_bound.py 40` separately.

## 9. Status

**Exact statement that now holds** (AI-checked, pending human review; i.i.d. uniform
columns in F_p^a, 2 ≤ κ < p−1):
- *Proposition 1 [proved].* Any merge step that reads only π_j-images (and coins),
  and outputs D-combinations of disjoint groups that vanish under π_j, produces
  outputs that are i.i.d. uniform on V_j, independent of the record. Adaptive
  grouping is included.
- *Proposition 2 [proved].* The coordinate-by-coordinate isotropic merge tree uses
  exactly 3^a columns (κ = 2; κ = 3 via Hasse–Weil), and each node costs expected
  O(κ) tries. Adaptive pairing succeeds with probability ≤ N_0((1+1/p)/2)^a.
- *Proposition 3 [proved].* A public-split tree with success > 1/(p−1) has
  M ≥ (a_max+1)(a − a_max + 1). If M < (a/2+1)(a/4+1), it contains a single-level
  solver for the same problem in dimension ≥ a + 1 − 2M/a with ≤ M columns, the
  same success probability and the same time.
- *Proposition 4 [proved].* In the two-level contraction, first-level dependencies
  need c+1 columns in a c-dimensional quotient, and flexible vectors are uniform on
  the nonzero vectors of the quotient. So random columns give no saving: (a+1)²
  (product) and (a+1)(a+2)/2 − O(1) (triangular).
- *Proposition 5 [proved].* For κ = 2 (p ≥ 5), or κ ≥ 3 with p ∉ E_2(κ):
  M_K = K(2a−K+3)/2 + a − K + n_0 columns give a witness except with probability
  β(a−K+n_0, n_0; a−K) + 2^{−B}, in time poly(a, B, log p)·κ^{a−K}.
- *Frontier [argued].* Every method examined needs time ≈ κ^{a − M/a}. Nothing here
  is a lower bound.

**Still missing.**
- Any o(a²)-arity average-case algorithm in time poly(a)·κ^{o(a)}, for any fixed κ,
  or any evidence of hardness for fixed κ and large p. Proposition D of the
  2026-11-02 report covers only growing κ.
- Trees whose subspaces depend on the data (beyond the triangular solver) are not
  covered by Proposition 3.
- The one-variable Legendre-pattern problem of §0(6) (arity a+2) has not been
  checked against the literature: Legendre-PRF key recovery, and point finding on
  high-genus curves. UNKNOWN.
- The MQ literature of §7 (Thomae–Wolf, Miura–Hashimoto–Takagi, Furue–Nakamura–Takagi)
  was recalled, not re-read. Before anything is cited from it, the full texts
  must be checked.
- κ = 3 isotropy uses Hasse–Weil and the per-try rate 1/3 + O(p^{−1/2}); these were
  argued, not written out.

**Claim gates that must stay false.**
- "An efficient linear-arity (or o(a²)) SDE solver exists". Unchanged. This pass
  found none for the average case; the worst case is another session's question.
- "The average-case SDE is hard for fixed κ" or "requires Ω(a²) columns".
  Proposition 3 and the frontier are about method families, not lower bounds.
- "Merge/isotropic trees give subquadratic arity". They are exponential
  (Proposition 2).
- "Schedule 2 / the triangular solver is optimal".
- Any novelty claim for Proposition 5. It is a direct combination of
  `prop:triangular-sde` with `thm:free-coordinate`, and the same shape as the
  underdetermined-MQ hybrid trade-off.

**Next hard question.** Does the one-variable problem "find t ∈ F_p with
χ(α_j + tβ_j) = 1 for j = 1..n" (random α, β, p ≥ 2^{n+O(1)}) have a 2^{o(n)}
algorithm? If not, is there any reduction from it to the arity-(a+2) SDE, or back?
- Next command: a literature helper on Legendre-PRF key recovery and on
  quadratic-residue-pattern search (Beullens et al.; Kaluđerović–Kleinjung–Kostić),
  full texts only.
- Expected artifact: `lit/` notes in a new folder.
- Acceptance test: a cited theorem, read in full, giving the best known exponent,
  or UNKNOWN.

## Proposed paper text

**None for an o(a²) result** (none was found). The following remark is optional. It
records Propositions 3 and 5 for the i.i.d. uniform supply only. Target: the end of
`app:fc-split` in `appendix-free-coordinate.tex`. It uses only labels and macros
present there and in main.tex (`\Fp`, `\poly`). The owner decides whether to adopt it.

```latex
\begin{remark}[Arity--time trade-off for uniform banks; AI-checked, pending human review]
\label{rem:fc-tradeoff}
Let the labels be independent and uniform on a subspace of dimension $a$, and let $2 \le \kappa < p-1$.
\begin{enumerate}[label=(\alph*),leftmargin=2em]
  \item \emph{Hybrid.} Suppose $\kappa = 2$, or $p \notin E_2(\kappa)$. Let $0 \le K \le a$ and $g = a-K$. Run $K$ rounds of the construction in the proof of Proposition~\ref{prop:triangular-sde} on the first $\sum_{i<K}(a-i+1)$ labels. Apply (F2)--(F4) to the images of $g+n_0$ further labels in $\Fp^a/U_K \cong \Fp^{g}$, and back-substitute as in that proof. The images are independent and uniform on $\Fp^{g}$, because $U_K$ depends only on the earlier labels. So Lemma~\ref{lem:fc-node}(a)--(c) apply with $a = g$. With $K(2a-K+3)/2 + g + n_0$ labels, a nonzero solution is found except with probability $\beta(g+n_0, n_0; g) + 2^{-B}$, in time $\poly(a, B, \log p)\cdot\kappa^{\,g}$. Thus $K = 0$ is the free-coordinate node and $K = a$ is Proposition~\ref{prop:triangular-sde}. Arity about $Ka$ costs about $\kappa^{a-K}$ trials, as for block splitting with blocks of sizes $a-K$ and $K$.
  \item \emph{Splitting does not lower the arity by itself.} In the split node of Section~\ref{app:fc-split}, with level drops $a_j = \dim V_{j-1} - \dim V_j$, a sub-solver with $M_j \le a_j$ inputs fails except with probability at most $1/(p-1)$, because its sub-bank then has full column rank. Hence a split node that succeeds with probability above $1/(p-1)$ has $M \ge \prod_j(a_j+1) \ge (a_{\max}+1)(a-a_{\max}+1)$. If $M < (a/2+1)(a/4+1)$, then $a_{\max} > a/2$, and by Lemma~\ref{lem:fc-split-law}(c) its largest sub-solver solves an instance of the same problem in dimension at least $a + 1 - 2M/a$ from at most $M$ uniform labels. In particular, one-coordinate merges ($a_j = 1$ for all $j$) need $\prod_j M_j \ge 2^a$.
\end{enumerate}
Neither part gives a polynomial-time solver at arity $o(a^2)$. Whether one exists for uniform banks is open.
\end{remark}
```

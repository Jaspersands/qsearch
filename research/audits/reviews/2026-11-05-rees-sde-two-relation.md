# Rees diagonal SDE: two-relation objects, coset-generic flexibility, and a steered block-refined solver

**Status: COMPLETE. Mixed: a conditional positive result (random or non-degenerate columns), no change
to the worst case.** 5 November 2026, overnight AI-only pass (one Claude Code session, no helper
agents). Not human-reviewed, not in Lean, no novelty or priority claim. **AI-checked, pending human
review.** Labels: **[proved]** (full proof here), **[exact]** (complete finite computation, script
named), **[sampled]** (exact arithmetic on random samples), **[argued]**, **[conjecture]**,
**[literature]**. Scripts and outputs are in `2026-11-05-rees-sde-two-relation/`; interpreter
`/opt/anaconda3/bin/python`. Only this file and that folder were written (no `.tex`, no git, no
handoff/STATE edits, `rees_hsp_reduction.json` untouched).

**Problem and notation** (as in `2026-11-05-rees-sde-subquadratic.md`, "the subquadratic report").
Columns λ_1..λ_M ∈ F_p^a, κ = gcd(d, p−1) ≥ 2, P = (F_p^×)^κ, Sq = P ∪ {0}, Q_ν = g^ν P,
cos(y) = ν for y ∈ Q_ν, Q_ν° = Q_ν ∪ {0}. Find x ∈ Sq^M ∖ {0} with Σ x_iλ_i = 0. For a column set S
and U ≤ F_p^a, Λ(y) = Σ_{i∈S} y_iλ_i and R_U(S) = {Λx + U : x ∈ Sq^S}. Known polynomial arity:
(a+1)(a+2)/2 (`prop:triangular-sde`, p ∉ E_2(κ)). Chevalley–Warning (CW): κa + 1.

## 0. Verdict

1. **The question as posed (exact two-direction flexibility of a two-relation object in polynomial
   time with O(1) columns per direction) gets a negative structural answer and is the wrong target
   [proved].**
   - A two-relation object in general position admits no class collapse at all on a 2-dimensional
     family of realizations (Proposition A: every collapse class is a single coordinate). So every
     efficient "collapse" realization uses one kernel direction at a time, and the second relation
     buys nothing.
   - Exact two-direction flexibility does occur in the sampled small cases (q ≤ 4, p ≤ 43; e.g. every
     sample at κ = 2, q = 3, p ≥ 13 and at κ = 3, q = 3, p ∈ {19, 31}), found by exhaustive search
     (§2.3), but the collapse rule finds a second direction only at κ = 3, q = 2. No structure an
     algorithm could use was found [exact on samples; no general claim].
2. **What does work: coset-generic flexibility from a single circuit [proved].** Split the support of
   a circuit's dependency δ into E blocks, each inside one coset class of δ (not just the κ class
   sets). Then R_U(S) contains every point of the (E−1)-dimensional block span Ω, except points on at
   most C(E,2) "cross-class coincidence" hyperplanes. A target is realized by drawing a scalar s
   uniformly until E coset tests pass, about κ^E draws (Theorem B). This needs p ∉ E_cg(E, κ), a new
   exceptional set (item 4).
   - Theorem 1 of the subquadratic report is not contradicted: R_U(S) still contains no plane. The
     bad hyperplanes are exactly where Theorem 1 bites.
   - So the minimal cost of t coset-generic directions is a circuit, q + 1 columns, the minimum for
     any object. No second relation is needed.
3. **Steering makes the triangular recursion run on coset-generic pieces [proved].** Back-substitution
   has a free scalar s at every level, and it moves the next residual along the defect vector e_l.
   This steers residuals off the bad hyperplanes.
   - **Theorem C.** If p ∉ E_cg(E, κ) with E ≥ κ, every round is a circuit (H1) and no steering form
     vanishes identically (ND′), then a Las Vegas algorithm runs in time poly(a, log p)·κ^E. It uses
     M_E(a) = 1 + m(a+1) − (E−1)m(m−1)/2 + [r>0](r+1) columns, where a = m(E−1) + r. Each run
     succeeds with probability ≥ 1 − L·C(E,2)/G_E(p), with G_E(p) ≥ κ^{−E}(p − E − (κ^E−1)(E−1)√p).
     The hypotheses (H1) and (ND′) are checkable in polynomial time.
   - **Exact arities.** M_2 = (a+1)(a+2)/2 (the triangular solver). M_3 = ⌊(a+2)²/4⌋ + [a odd].
     M_E = a²/(2(E−1)) + O(a).
   - **Corollary C (i.i.d. uniform columns).** (H1) and (ND′) hold with probability at least
     1 − (M_E(a) + L·C(E,2))/(p−1). For κ = 2 and p ≥ 64a²:
     - E = 3 gives ⌊(a+2)²/4⌋ + [a odd] columns, about a²/4, in randomized polynomial time, with
       no exceptional primes (E_cg(3,2) = ∅);
     - any fixed E gives about a²/(2(E−1));
     - E = ⌈log_κ a⌉ gives O(a²/log a) in polynomial time once p ≥ poly(a).
4. **Exceptional sets, the analogue of E_2(κ) [exact + Weil].** These are complete, because the
   exhaustive scans reach the Weil bound p_W:
   - E_cg(3, 2) = ∅ (scan to 257 > p_W = 202);
   - E_cg(3, 3) = {7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127, 139, 151, 157, 163, 181,
     193, 211, 241} (scan to 2750 > p_W = 2710);
   - E_cg(4, 2) = {5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 59} (scan to 2040 > p_W = 2033,
     `good_k2_E4.out`, final line "complete=yes").

   Unlike E_2(3) = ∅, E_cg(3, 3) is not empty.
5. **Worst case unchanged [proved by example + exact].** For every split rule there are solvable
   inputs on which Theorem C's algorithm fails deterministically (κ = 3; for κ = 2 under a fixed
   split), because (ND′) fails (§6). **Best proved arity for arbitrary columns: still (a+1)(a+2)/2**
   (p ∉ E_2(κ)). Best proved polynomial-time arity:
   - for i.i.d. uniform columns (the label law) at p ≥ 64a² (κ = 2) or p ≥ max(2750, 1000a²)
     (κ = 3; see the example in §5), or for any columns satisfying the
     checkable hypotheses (H1) and (ND′) with G_3(p) > L·C(3,2) (so a pass succeeds with positive
     probability; G_3(p) ≥ p/10 for κ = 2 and p ≥ 256, so p ≥ 64a² suffices):
     **⌊(a+2)²/4⌋ + [a odd]** (E = 3) at κ = 2 (no exceptional p), and for p ∉ E_cg(3,3) at κ = 3;
   - in general a²/(2(E−1)) + O(a) for fixed E, and O(a²/log a) at E = log_κ a.
6. **CHMT check (coordinator lead) [proved + literature].** No method can reach a(a+1)/2 + 1 on
   every diagonal instance:
   - at a ∈ {1, 2} that count is ≤ 2a, below CW, and the explicit instance (e_j, −g·e_j)_{j≤a} with
     g a non-residue has no solution (`test_below_cw_instance_unsolvable`);
   - so a statement "every system with n ≥ m(m+1)/2" cannot hold for these systems, and CHMT's
     "class" must exclude them;
   - for a ≥ 3 nothing follows. The full CHMT text was not obtainable (paywalled, no preprint
     found), so their exact hypotheses could not be checked or implemented;
   - for random columns, Theorem C at E = 3 already matches a(a+1)/2 + 1 at a = 3 (7 vs 7) and
     beats it for every a ≥ 4 (e.g. 9 vs 11 at a = 4, 49 vs 79 at a = 12).

## 1. Definitions

Fix U ≤ F_p^a. Put q = a − dim U and S a column set whose images in F_p^a/U span it.

- **Relations.** r(S) = dim K, where K = {y ∈ F_p^S : Λy ∈ U}. S is in **general position (GP)**
  if every q of its columns are independent modulo U. For GP S, |S| = q + r.
- **Exactly flexible in t directions:** R_U(S) contains a t-dimensional subspace T of F_p^a/U. For
  t = 1 this is the subquadratic report's "flexible line".
- **Coset-generic flexible in t directions with defect h:** there are a t-dimensional T and h linear
  hyperplanes H_1..H_h of T with T ∖ (H_1 ∪ … ∪ H_h) ⊆ R_U(S). (The user's "coset-generic family".)
- **Realization algorithm** for such a T: a Las Vegas procedure that, given w ∈ T outside the H_j,
  returns x ∈ Sq^S with Λx ≡ w (mod U), in expected time poly(|S|, log p)·C. C is the *search
  cost*.
- **Steerable:** the realizations of w are indexed by a parameter s ranging over a set Good(w) of
  known size, and their exact values Λx ∈ F_p^a are w̃ + s·e for a fixed defect vector e ∈ U.
- **Class collapse.** Let A = z + K′ be an affine family of realizations (z with Λz ≡ w, K′ ≤ K of
  dimension d). Coordinates i, j **collapse on A** if x_i = μx_j for all x ∈ A and some μ ≠ 0. A
  collapse class with known μ-cosets turns |class| coset conditions into one, which is the mechanism
  of every efficient rule known (the contraction of `prop:triangular-sde`, and Theorem B below).

## 2. Two-relation objects

### 2.1 Lemma 2.1 (general position) [proved]
Let S be GP with r relations. Then every nonzero k ∈ K has at most r − 1 zeros. For G ⊆ S with
|G| ≤ r, dim{k ∈ K : k|_G = 0} = r − |G|.

*Proof.* The vectors of K vanishing on G are the dependencies (mod U) of the q + r − |G| ≥ q columns
outside G. By GP these span the q-dimensional quotient, so the dependencies form a space of
dimension (q + r − |G|) − q. If k ≠ 0 had r zeros, it would be a dependency among q columns, which
GP forbids. ∎

For r = 2, the coordinate functionals φ_i|_K (i ∈ S) are nonzero and pairwise non-proportional. So
q + 2 ≤ p + 1: GP two-relation objects exist only for q ≤ p − 1.

### 2.2 Proposition A (no collapse on a family of dimension ≥ 2) [proved]
Let S be GP with r relations, and let A = z + K′ with dim K′ = d ≥ 2. Then:
- every collapse class on A that contains a coordinate non-constant on A has size ≤ r − d + 1;
- at most r − d coordinates are constant on A;
- hence the number m of collapse classes satisfies m ≥ (q + d)/(r − d + 1).

For r = d = 2 every class is a single coordinate: m = q + 2 = |S|.

*Proof.*
- If i and j collapse and φ_i|_{K′} ≠ 0, then φ_i|_{K′} and φ_j|_{K′} are proportional, so they have
  a common kernel of dimension d − 1 in K′. For a class G, that common kernel is a (d−1)-dimensional
  space of kernel vectors vanishing on G. Lemma 2.1 gives r − |G| ≥ d − 1.
- The constant coordinates Z_0 satisfy K′ ⊆ {k : k|_{Z_0} = 0}, so r − |Z_0| ≥ d.
- Count the remaining q + r − |Z_0| ≥ q + d coordinates in classes of size ≤ r − d + 1. ∎

**Consequence [proved / argued].**
- For a uniformly random point of A, the m class conditions are those of m pairwise distinct linear
  forms. A search over A therefore succeeds with probability ≈ κ^{−m}, by the same Weil argument as
  Lemma W [argued for general A; proved in Lemma W for d = 1].
- So efficient collapse-search on a GP two-relation object is possible only along a kernel line
  (d = 1). Along a kernel line k the collapse classes are exactly the blocks of Theorem B (the
  coordinates i with equal z_i/k_i), so the object behaves as the circuit supp(k).
- A "two-dimensional contraction", meaning a κ×κ×κ or (κ×κ)² coset pattern that collapses a 2-dim
  kernel family, therefore does not exist for GP two-relation objects. Making the relation count r
  large enough for m classes at d = 2 needs r ≥ (q + 2)/m + 1, so m = O(1) costs Ω(q) extra
  columns per object. The circuit route of Theorem B gets the same directions with one relation.

### 2.3 Exact flexibility data [exact]
`two_relation.py` → `two_relation.out`. These are GP objects of q + 2 uniform columns in F_p^q. Each
row gives the exact largest subspace inside R(S) ("flex") and inside the kernel-line collapse set
∪_k{targets realizable by collapse along k} ("cflex"), as counts over samples.

| p | κ | q | flex counts | cflex counts | note |
|---|---|---|---|---|---|
| 5–29 | 2 | 2 | all 2 | all 1 | R(S) = F_p² in every sample |
| 7 | 3 | 2 | all 1 | all 1 | |
| 13 | 3 | 2 | 2 ×5, 1 ×3 | 2 ×2, 1 ×6 | |
| 19, 31, 37, 43 | 3 | 2 | all 2 | all 2 | union over the p+1 kernel lines of 2-dim block spans fills F_p² |
| 7 | 2 | 3 | all 2 | all 1 | |
| 11 | 2 | 3 | 3 ×5, 2 ×1 | all 1 | |
| 13, 17, 19 | 2 | 3 | all 3 (R(S) = F_p³) | all 1 | exact planes exist, never from collapse |
| 13 | 3 | 3 | all 1 | all 1 | |
| 19 | 3 | 3 | all 2 | 1 ×3, 2 ×1 | |
| 31 | 3 | 3 | all 2 | all 1 | density ≥ 0.998, no exact 3-space |
| 7 | 2 | 4 | all 2 | all 1 | density 0.88 |
| 11 | 2 | 4 | 3 ×2, 2 ×1 | all 1 | density ≈ 0.98 |
| 13 | 3 | 4 | all 1 | not computed (p^q > 30000) | density ≈ 0.44 |

All 23 rows of `two_relation.py` finished (`two_relation.out`). In no sample does the collapse
rule give more than one direction except at κ = 3, q = 2.

Reading:
- At κ = 2 the collapse rule never gives more than one direction. Exact two-dimensional flexibility,
  when present, comes from realizations with no collapse structure, found only by exhaustive search
  over the p² points of a fiber.
- At κ = 3 and q = 2 the union of the p + 1 kernel-line planes covers F_p². This is a q = 2
  coincidence: every block span is the whole quotient.
- At fixed p the realizable set thins out as q and κ grow (κ = 3, p = 13: density 1.0 or 0.95–0.98
  at q = 2, against 0.78–0.82 at q = 3), as counting predicts: p² points per fiber against κ^{q+2}
  coset conditions. So exact flexibility of GP two-relation objects is a small-q phenomenon
  (q ≲ 2 log_κ p) [argued from counting, consistent with the data].

## 3. Theorem B: a circuit is coset-generic flexible in E − 1 directions

Let S be a circuit modulo U with dependency δ, and let C = {cos δ_i} with |C| ≥ 2. Let G_1, …, G_E
partition S, each G_b inside one class set, and let c_b = cos δ_i for i ∈ G_b. Put
W_b = Σ_{i∈G_b} δ_iλ_i, Ω = span(W_b mod U), and for β ∈ F_p^E

  Good(β) = {s ∈ F_p : β_b + s ∈ Q_{−c_b}° for all b}.

**Theorem B [proved; exact on 84 objects, `block_check.out`].**
- (i) dim Ω = E − 1, and the only relation among the W_b modulo U is Σ_b W_b ≡ 0. More precisely,
  Σ_b W_b = Λδ =: e ∈ U.
- (ii) R_U(S) ∩ Ω = {Σ_b β_bW_b : Good(β) ≠ ∅}. For s ∈ Good(β) the weights x_i = δ_i(β_{b(i)} + s)
  lie in Sq and have exact value Λx = Σ_b β_bW_b + s·e.
- (iii) If p ∉ E_cg(E, κ), every β with β_b ≠ β_{b′} whenever c_b ≠ c_{b′} has Good(β) ≠ ∅. So
  R_U(S) ⊇ Ω ∖ ∪_{c_b≠c_{b′}} H_{bb′}, where H_{bb′} = {β_b = β_{b′}}. This is coset-generic
  flexibility in E − 1 directions with defect ≤ C(E,2).
- (iv) Drawing s uniformly from F_p until s ∈ Good(β) takes p/|Good(β)| ≤ p/G_E(p) expected draws,
  each costing E coset tests.

*Proof.*
- (i) A relation Σμ_bW_b ∈ U gives the column relation (μ_{b(i)}δ_i)_i, which must be a multiple of
  δ because S is a circuit. Hence μ is constant.
- (ii) If Λx ≡ Σβ_bW_b = Λ(δ∘β_{b(·)}), then x − δ∘β_{b(·)} ∈ Fδ, so x = δ∘(β_{b(·)} + s).
  Since δ_i ∈ Q_{c_b}, x_i ∈ Sq iff β_b + s ∈ Q_{−c_b}°. The value is
  Σ_b(β_b + s)W_b = Σβ_bW_b + s·e.
- (iii) Blocks of the same class with equal β merge into one block with the same condition. So Good
  is the Good set of E′ ≤ E pairwise distinct offsets with ≥ 2 classes, and the definition of E_cg
  applies.
- (iv) Immediate. ∎

When β has a cross-class coincidence β_b = β_{b′}, Q_{−c_b}° ∩ Q_{−c_{b′}}° = {0} forces
s = −β_b. The target is then realizable iff the other offsets have the right classes. For E = 2 this
means β constant, the target is 0 and it is realized, so the triangular line is exactly flexible.
That is the E = 2 case of the paper.

**Relation to Theorem 1.** The hyperplanes H_{bb′} are where Theorem 1's "one class per line"
applies, so R_U(S) never contains a plane. Coset-generic flexibility escapes Theorem 1 and
Corollary 1 of the subquadratic report, because they assume each U_l is contained in
U_{l−1} + R(S_l) exactly.

## 4. Lemma W and the exceptional sets E_cg(E, κ)

**Definition.** E_cg(E, κ) is the set of primes p ≡ 1 (mod κ) for which there are e ≤ E, classes
c_1..c_e (at least two distinct) and pairwise distinct β_1..β_e ∈ F_p with Good(β) = ∅.
G_E(p) = min |Good(β)| over all such data.

**Lemma W [proved].** For e distinct offsets,

  |{s : β_b + s ∈ Q_{−c_b} ∀b}| ≥ κ^{−e}[(p − e) − (κ^e − 1)(e − 1)√p].

So p ∉ E_cg(E, κ) as soon as p − e > (κ^e − 1)(e − 1)√p for all e ≤ E. Call the least such prime
bound p_W(E, κ). Then G_E(p) ≥ min_{e≤E} of the right-hand side.

*Proof.*
- Let ψ be a multiplicative character of order κ with ψ(g) = ζ_κ. For y ≠ 0,
  1[y ∈ Q_c] = κ^{−1}Σ_{t∈Z_κ} ζ^{−tc}ψ^t(y).
- Expand the product over s ∉ Z = {−β_b}. The t = 0 term is p − e. For t ≠ 0 with support J,
  |J| = w:
  - Σ_{s∈F_p} Π_{b∈J}ψ^{t_b}(s + β_b) has modulus ≤ (w − 1)√p. This is Weil's bound in Lidl–Niederreiter,
    Thm 5.41: the β_b are distinct and 0 < t_b < κ, so the polynomial is not a constant times a κ-th
    power.
  - Removing s ∈ Z changes the sum by at most e − w.
  - Since (w − 1)√p + e − w ≤ (e − 1)√p, each such term is at most (e − 1)√p, and there are
    κ^e − 1 of them. ∎

**Exact sets [exact].** `good_threshold.py` normalises c_1 = 0, β_1 = 0 and β_2 ∈ {g^0..g^{κ−1}}
(exact symmetries) and handles the last offset for all values at once by FFT correlation, which
returns |Good| exactly. It was cross-checked against plain enumeration (`bf_good.py` → `bf_good.out`:
21 (κ, E, p) cases, 0 mismatches).

| κ | E | p_W | scanned to | E_cg(E, κ) | G_E(p) examples |
|---|---|---|---|---|---|
| 2 | 3 | 202 | 257; 5000 (`good_k2_E3_5000.out`) | ∅ | G = 1 (p ≤ 13), 2 (17–23), 29 (257), 608 (4999); min G/p over 256 ≤ p ≤ 5000 is 0.110 (p = 263) |
| 3 | 3 | 2710 | 2750; 11000 (`good_k3_E3_11000.out`) | 22 primes, max 241 (list in §0) | 74 at p = 2713; min G/p is 0.0065 (G = 2 at p = 307) over 271 ≤ p ≤ 11000 and 0.0253 (p = 2767) over 2750 ≤ p ≤ 11000 |
| 2 | 4 | 2033 | 2040 | {5, …, 59} (14 primes) | 71 at p = 1453, 103 at p = 2039; min G/p over 1000 ≤ p ≤ 2040 is 0.045 |
| 3 | 4 | 57608 | — | not computed | |
| 2 | 5 | 15386 | — | not computed (Theorem C at E = 5 still ran in all sampled cases, §9) | |

E_cg(E, κ) ⊇ E_cg(E′, κ) for E′ ≤ E by definition. E_cg(2, κ) is the class-restricted part of the
E_2-type condition: for κ = 2 it is empty, and κ = 2, E = 2 is the triangular solver.

## 5. Theorem C: the steered block-refined triangular solver

**Algorithm BRT(E)** (`brt.py`).

*Forward pass.*
- Start with U_0 = 0. Round l takes the next q_l + 1 columns, q_l = a − dim U_{l−1}, and a
  dependency δ^{(l)} modulo U_{l−1}, with defect e_l = Λδ^{(l)} ∈ U_{l−1}.
- If δ^{(l)} is monochromatic, round l is the **stop round**.
- Otherwise split its support into E_l = min(max(E, |C_l|), q_l + 1) blocks, each inside a class
  set, and add W^{(l)}_b, b ≠ 0, to the basis: U_l = U_{l−1} ⊕ Ω_l.
- If U = F_p^a, one more column is the **top round**.

*Backward pass.*
- Start with τ = −yλ_top (y uniform in P), or τ = −ζe_stop (ζ uniform in Q_{−c}, where c is the
  stop round's single class).
- For l = L, …, 1:
  - write τ = Σ_bβ_bW^{(l)}_b + τ′ with β_0 = 0 and τ′ ∈ U_{l−1};
  - draw s_l uniformly from Good_l(β);
  - put x_i = δ_i(β_{b(i)} + s_l) on round l;
  - set τ ← τ′ − s_l e_l.
- If some Good_l(β) is empty, restart the backward pass.

**Steering forms.** By induction, the level-j residual τ_j is linear in (y or ζ, s_L, …, s_{j+1})
with coefficients fixed by the forward pass. For a cross-class pair (b, b′) of round j put
F_{j,b,b′} = β_b(τ_j) − β_{b′}(τ_j), a linear form in those variables.

**(ND′)** holds if no F_{j,b,b′} with c_b ≠ c_{b′} is identically zero. **(H1)** holds if every
non-stop round's q_l + 1 columns form a circuit modulo U_{l−1}.

**Theorem C [proved; sampled on 840 random and 90 adversarial runs, exact on 256 small cases].**
Hypotheses:
- κ ≥ 2, E ≥ κ, p ≡ 1 (mod κ) prime, p ∉ E_cg(E, κ);
- λ_1, …, λ_M ∈ F_p^a with M ≥ M_E(a);
- (H1) and (ND′) hold.

Conclusions:
- (a) The forward pass uses at most M_E(a) columns, where
  M_E(a) = 1 + m(a+1) − (E−1)m(m−1)/2 + [r>0](r+1) with a = m(E−1) + r, 0 ≤ r < E − 1.
- (b) Each backward pass returns a nonzero x ∈ Sq^M with Σx_iλ_i = 0, with probability at least
  1 − Σ_j N_j / G_E(p) ≥ 1 − L·C(E,2)/G_E(p). Here L ≤ ⌈a/(E−1)⌉ is the number of levels, and N_j is
  the number of cross-class pairs (b, b′) of round j whose form F_{j,b,b′} involves some s_l.
- (c) Cost: O(L) Gaussian eliminations of size ≤ a × (2a + 1), plus per pass an expected
  Σ_l p/G_E(p) draws of E coset tests. Computing (H1) and (ND′) takes O(L·E²) further linear solves.
  Everything is deterministic except the draws of y, ζ and s_l, and outputs are verified.

*Proof.*
- **(a), column count.** Under (H1) round l gains E_l − 1 ≥ min(E − 1, q_l) dimensions, by
  Theorem B(i). Let f_E(q) = q + 1 + f_E(q − min(E−1, q)), with f_E(0) = 1. Then f_E is
  nondecreasing. If a run gains g ≥ min(E−1, q) at each step, its count f satisfies f(q) ≤ f_E(q) by
  induction, since f(q) = q + 1 + f(q − g) ≤ q + 1 + f_E(q − min(E−1,q)). Unrolling f_E(a) gives the
  closed form, which is checked in `test_arity_formula`. A stop round only shortens the run.
- **(b), correctness of the values.** By Theorem B(ii), round l's weights lie in Sq and have value
  (τ_l − τ′_l) + s_le_l = τ_l − τ_{l−1}. The values telescope:
  Σ_l (values) + (top or stop value) = −τ_0 = 0, since τ_0 ∈ U_0 = 0. The top or stop weight is
  nonzero, so x ≠ 0.
- **(b), the only failure is an empty Good set.** If τ_j's offsets have no cross-class coincidence,
  Good_j ≠ ∅ by p ∉ E_cg(E, κ) and Theorem B(iii). So a pass fails only if some F_{j,b,b′} vanishes
  at the drawn point.
  - If F_{j,b,b′} involves no s_l, then F = c·y (or c·ζ) with c ≠ 0 by (ND′), and it never vanishes.
  - Otherwise let s_m (m > j) be the last-drawn variable with a nonzero coefficient. Consider the
    event that the first cross-class coincidence of the pass, scanning levels downward, is at
    (j, b, b′). On that event level m had no coincidence, so s_m was drawn uniformly from
    Good_m(β^{(m)}), a set of size ≥ G_E(p). Conditioned on all earlier draws, F is affine in s_m
    with nonzero slope, and later draws do not enter F. So the event has probability ≤ 1/G_E(p).
    (Conditioning on "no earlier coincidence" is needed: after a coincidence, Good may be a single
    forced value.)
  - A pass fails only if some coincidence occurs. A union bound over the possible first
    coincidences (j, b, b′) gives the bound.
- **(c).** Immediate. ∎

**Corollary C (i.i.d. uniform columns) [proved].** Let the λ_i be i.i.d. uniform on F_p^a, with
κ ≥ 2, E ≥ κ and p ∉ E_cg(E, κ). Then with probability at least
1 − (M_E(a) + L·C(E,2))/(p − 1) over the columns, the run stops early with success or satisfies (H1)
and (ND′). Conditioned on that, Theorem C applies.

*Proof.*
- **(H1).** U_{l−1} depends only on earlier columns and coins. So the q + 1 fresh columns are i.i.d.
  uniform modulo U_{l−1}. The first q are a basis except with probability ≤ 1/(p−1). Given that, the
  last has uniform coordinates, and some coordinate is 0 with probability ≤ q/p. A zero column
  modulo U gives a stop round, which is a success.
- **(ND′).** Fix a complement of U_j depending only on U_j. Split the fresh columns of round j + 1
  into quotient parts (which fix δ^{(j+1)}) and U_j-parts u_i, i.i.d. uniform. Then
  e_{j+1} = Σδ_iu_i is uniform on U_j. Its Ω_j-offset difference for (b, b′), which is the
  coefficient in F_{j,b,b′} of the variable introduced by round j + 1, is therefore uniform on F_p,
  and so zero with probability 1/p.
  - The same holds when round j + 1 is the stop round (e_stop) or the top round (λ_top uniform).
- **Total.** A union bound over the rounds and the pairs gives the stated probability. ∎

**Parameter choices [proved, from Theorem C, Corollary C and §4].**

| setting | columns | per-pass failure | time |
|---|---|---|---|
| κ = 2, E = 3, every odd p | ⌊(a+2)²/4⌋ + [a odd] | ≤ 2L/G_3(p), G_3 ≈ p/9 (exact table) | poly |
| κ = 3, E = 3, p ∉ E_cg(3,3) (p ≥ 271 suffices) | same | ≤ 3L/G_3(p) | poly |
| fixed E ≥ κ, p ≥ p_W(E,κ) | a²/(2(E−1)) + O(a) | ≤ L·C(E,2)·κ^E/(p − O(Eκ^E√p)) | κ^E·poly |
| E = ⌈log_κ a⌉, p ≥ C·κ²a²log²a (≥ p_W) | O(a²/log a) | o(1) once p ≫ a·log²a·κ^E | poly(a, log p) |

**Example (κ = 2, E = 3, i.i.d. columns, p ≥ 64a², a ≥ 2) [proved + exact].**
- Each round has blocks of classes (0,0,1) or (0,1,1), hence 2 cross pairs, and L ≤ (a+1)/2.
- Column-side failure: ≤ (M_3(a) + 2L)/(p − 1) ≤ ((a+2)²/4 + a + 2)/(64a² − 1) ≤ 1/16.
- Per-pass failure: ≤ 2L/G_3(p) ≤ (a+1)/G_3(p). We have G_3(p) ≥ p/10 for every prime p ≥ 256:
  exact for p ≤ 5000 (`good_k2_E3_5000.out`), and by Lemma W, (p − 3 − 14√p)/8 ≥ p/10, for
  p ≥ 4930. So the per-pass failure is ≤ 10(a+1)/(64a²) ≤ 1/8.
- For κ = 3 the exact minimum is G_3(p) ≥ p/154 on 271 ≤ p ≤ 2750, about p/37 for large p
  (`good_k3_E3.out`). G_3(p) ≥ p/40 for 2750 ≤ p ≤ 11000 [exact, `good_k3_E3_11000.out`], and
  Lemma W gives G_3(p) ≥ (p − 3 − 52√p)/27 ≥ p/54 for p ≥ 10829 [proved]. So G_3(p) ≥ p/54 for
  every prime p ≥ 2750, and for κ = 3 take p ≥ max(2750, 1000a²): then p ∉ E_cg(3,3), the
  per-pass failure is ≤ 3L·54/p ≤ 81(a+1)/(1000a²) ≤ 0.17, and the column-side failure is
  ≤ (M_3(a) + 3L)/(p − 1) ≤ 0.01 [proved + exact].

Some numbers (`brt.arity`):

| a | triang. | CHMT count a(a+1)/2+1 | M_3 | M_4 | M_5 | M_7 | CW 2a+1 |
|---|---|---|---|---|---|---|---|
| 6 | 28 | 22 | 16 | 12 | 11 | 8 | 13 |
| 12 | 91 | 79 | 49 | 35 | 28 | 21 | 25 |
| 20 | 231 | 211 | 121 | 85 | 66 | 49 | 41 |
| 50 | 1326 | 1276 | 676 | 460 | 352 | 244 | 101 |
| 100 | 5151 | 5051 | 2601 | 1752 | 1326 | 902 | 201 |

For a < 4, M_3(a) < 2a + 1, which is below CW. Such instances are solvable only with high
probability, not always. Theorem C is consistent with this: the hypotheses fail on the CW-tight
instance (§6).

## 6. Limits: the worst case

1. **Below CW.** At a = 2, M_3(2) = 4 < 5. On the instance (1,0), (g,0), (0,1), (0,g), unsolvable
   at p = 1009 because p ≡ 1 mod 4 makes −g a non-residue for κ = 2 (for κ = 3, −g is a non-cube
   for every p), the
   solver reports "budget": round 1's dependency has support 2, (H1) fails and only one dimension is
   gained (`brt_adversarial.out`). This is consistent: no algorithm can succeed there.
2. **Planted non-steerable instances [exact on 24 instances].** `brt_tests.py planted_top` builds
   solvable inputs (M = M_E(a) ≥ 2a + 1) as follows:
   - every round after the first is an exactly dependent set of columns, so e_l = 0 and no s_l
     steers;
   - the top column is chosen so that the level-1 residual has a cross-class coincidence whose
     forced s fails the remaining class conditions;
   - y ∈ P only rescales offsets, so it cannot steer either.

   Results:
   - (ND′) fails in 24/24 instances, and the deterministic-split solver fails in 24/24;
   - for κ = 2, random splits rescue 18/18 (the planting targets a specific split);
   - for κ = 3, E = 3 the blocks are the class sets, so there is no split freedom, and random splits
     fail 6/6.

   So Theorem C's hypothesis (ND′) is genuinely needed, and the method does not give a worst-case
   arity.
3. **Structured inputs.** These are repeated columns, and columns in a subspace of codimension 2.
   After the built-in rank reduction (`brt.reduce_rank`): 39/40 successes and 1 empty Good set
   (`brt_adversarial.out`).
4. **Consistency with known barriers [argued].**
   - **Theorem 3 of the subquadratic report** (PRF hardness) is at M = a + 2. Theorem C needs
     M_E(a) ≫ a, and at E − 1 ≥ a it costs κ^{a+1}.
   - **KMOSW (p = 3) and Proposition 4.** Theorem C needs G_E(p) ≫ L, so p ≫ a, and says nothing at
     p = 3 or any fixed p. The "uniform in p" question stays open.
   - **Proposition D of the linear-arity report** (SIS-hardness) concerns h = (p−1)/κ ≤ 2. There
     E ≥ κ forces κ^E ≥ p^{p/3}, outside the poly regime.
   - **Corollary 1** (circuit schemes need (a+1)(a+2)/2 under GP) assumes exact realizable
     subspaces. Theorem C uses circuits but realizes only coset-generic pieces and pays with
     steering.

## 7. The questions of the task, answered

1. **Definitions:** §1. Exact flexibility is T ⊆ R_U(S). Coset-generic flexibility is
   T ∖ (h hyperplanes) ⊆ R_U(S), together with a Las Vegas realization and steering.
2. **Minimal columns per object for t = 2.**
   - *Exact:* a circuit (q+1 columns) cannot do it (Theorem 1). q + 2 columns sometimes can,
     information-theoretically (§2.3), but not through any collapse rule (Proposition A), and no
     polynomial-time realization was found. The existence threshold in p for exact planes at q = 2
     is in `two_relation.out`: κ = 2, always; κ = 3, from p = 19 on, in the samples.
   - *Coset-generic:* q + 1 columns, which is minimal, using a circuit with 3 blocks. The
     realization is explicit (Theorem B), with search cost κ³ coset-test rounds. The
     "two-dimensional contraction" condition is Good(β) ≠ ∅ for all coincidence-free β, and its
     exceptional set is E_cg(3, κ): ∅ for κ = 2, 22 primes ≤ 241 for κ = 3.
3. **Arity with t directions per round:** Theorem C, M_{t+1}(a) = a²/(2t) + O(a), exactly as in (a),
   with the exceptional set E_cg(t+1, κ) and hypotheses (H1) and (ND′).
4. **Obstruction:** for the exact version, Proposition A plus Theorem 1. For the coset-generic
   version, only (ND′) stands between Theorem C and a worst-case result (§6.2). Whether (ND′) can be
   enforced by choosing the round structure adaptively is the next hard question.

## 8. CHMT check (coordinator lead)

**Claim to check.** Cheng–Hashimoto–Miura–Takagi (PQCrypto 2014, LNCS 8772, 40–58) solve "a class
of" underdetermined MQ systems over odd q with n ≥ m(m+1)/2 variables. Through the normalisation
s_M = 1 this would give κ = 2 at M = a(a+1)/2 + 1, if it applied to every diagonal system.

**Proposition H [proved].**
- (a) For a ∈ {1, 2} and every odd p, no algorithm solves every diagonal instance at
  M = a(a+1)/2 + 1. That count is ≤ 2a, and the instance (e_j, −g·e_j)_{j≤a} with g a non-residue
  (padded by repeating a column when a = 1) has no nonzero x ∈ Sq^M with Σx_iλ_i = 0, since
  s² − g t² = 0 forces s = t = 0. (The sign matters: with (e_j, g·e_j) the instance is solvable
  when p ≡ 3 mod 4, because then −g is a residue; the first version of the test used that
  instance and failed at p = 7, 11, which is how the sign was caught.)
  - In MQ terms, m = 1, n = 1 is λ_1 s² = −λ_2, unsolvable when −λ_2/λ_1 is a non-residue; and
    m = 2, n = 3 is unsolvable as above.
  - So CHMT's polynomial-time statement cannot cover every system of this diagonal shape: their
    "class" must be a genericity condition or a restricted shape.
- (b) For a ≥ 3, a(a+1)/2 + 1 ≥ 2a + 1, so solutions exist by CW. Whether a polynomial method reaches
  that count on every instance is not settled here.

**Literature status [literature].**
- The full text of CHMT was not obtainable (Springer paywall, no preprint found). The abstract
  (via the Kyushu and CGU repository pages) says the MHT range is improved "essentially for free"
  with polynomial running time in odd characteristic, and gives no inequality.
- Hashimoto (JSIAM Letters 15, 2023, `../2026-11-05-rees-sde-subquadratic/lit/hashimoto_jsiaml2023.txt`)
  lists CHMT as n ≥ m(m+1)/2. Huang–Bao (arXiv:1507.03674) list Miura–Hashimoto–Takagi at
  n ≥ m(m+3)/2 with cost exponential in m for odd q (square roots exist with probability about 1/2
  per step).
- m(m+3)/2 is exactly the triangular count in the s_M = 1 normalisation, (a+1)(a+2)/2 − 1. So
  `prop:triangular-sde` already gives MHT's range in odd characteristic deterministically, given g
  and the roots.
- Without the text, the CHMT method could not be implemented. Proposition H(a) shows that a uniform
  version is false at m ≤ 2.

**Comparison.** For i.i.d. columns, Theorem C at E = 3 already uses fewer columns than a(a+1)/2 + 1
for every a ≥ 4, and ties at a = 3: a = 3: 7 vs 7; a = 4: 9 vs 11; a = 12: 49 vs 79.

**Recommendation.** Keep the paper's citation as a statement about a class of systems. Do not cite
CHMT as an improvement of `prop:triangular-sde` for arbitrary columns.

## 9. Computations and tests

`pytest` (8 tests) command, run in the folder:
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider test_two_relation.py`

| check | script → output | result |
|---|---|---|
| E_cg scans | `good_threshold.py` → `good_k2_E3.out`, `good_k2_E3_5000.out`, `good_k3_E3.out`, `good_k3_E3_11000.out`, `good_k2_E4.out` | §4 table; all scans complete |
| scan vs plain enumeration | `bf_good.py` → `bf_good.out` | 21 cases, 0 mismatches |
| Theorem B (i)–(iii) exactly against R(S) | `block_check.py` → `block_check.out` | 16 (p, κ, q, E) rows, 84 objects. dim Ω = E−1 in all; (ii) 0 mismatches; (iii) coincidence-free β realizable at every non-exceptional p, and fails at exceptional p as predicted |
| BRT vs exhaustive kernel search | `brt_tests.py brute` → `brt_brute.out` | 256 instances (p ≤ 61, a ≤ 4): 210 solved; all 33 "empty Good" outcomes are on unsolvable instances; 13 "budget" (10 solvable, 3 unsolvable): the forward pass ran out of columns because some round was not a circuit, which at these small p has probability about (q+1)/p per round (H1 fails); 11 of the 13 are at a = 2, below CW. Every returned witness is valid |
| BRT random columns | `brt_tests.py random` → `brt_random.out` | 840 runs, κ ∈ {2,3}, p ∈ {1009, 10007, 10009, 65537}, a ≤ 14, E ≤ 5, budget M_E(a): 836 ok, 2 budget, 2 empty Good (κ = 3, E ∈ {4, 5} at p = 1009, below p_W(4,3)) |
| BRT adversarial | `brt_tests.py adversarial` → `brt_adversarial.out` | §6 |
| BRT at scale | `brt_scale.py` → `brt_scale.out` | 16 runs: p ∈ {10⁹+7, 10⁹+9} (κ = 2, 3; a ∈ {20, 40}; E ∈ {3, 4, 6}) and p = 10⁶+3 (κ = 2, a = 30, E = 8). All ok, every witness valid, (ND′) failures 0, (H1) held. Columns used, e.g. a = 40: 441 (E = 3), 302 (E = 4), 189 (E = 6) vs 861 triangular; a = 30, E = 8: 86 vs 496. At most 2.6 s per run |
| pytest | `test_two_relation.py` → `pytest.out` | 8 passed. The first run failed `test_below_cw_instance_unsolvable` at p = 7, 11 (sign error in the instance, fixed to (e_j, −g·e_j); see §8) |
| two-relation exact flexibility | `two_relation.py` → `two_relation.out` | §2.3 |

## 10. Proposed LaTeX insertion

**Location.** `docs/papers/rees-hsp/main.tex`, immediately after `\end{remark}` of
`rem:triangular-scope`, or after `rem:sde-subquadratic` if that remark from the subquadratic report
is adopted (it is not in main.tex as of this pass). **Status: AI-checked, pending human review.**
Nothing else in the paper changes. It cites `LidlNiederreiter1997`, which is already in
references.bib.

```latex
\begin{remark}[Steered block-refined triangular solver; conditional; AI-checked, pending human review]
\label{rem:sde-block-steered}
This remark comes from an AI-only pass (\file{research/audits/reviews/2026-11-05-rees-sde-two-relation.md}); no human has checked it, it changes no other statement, and it gives no worst-case improvement. Keep the notation of Proposition~\ref{prop:triangular-sde}, with $Q_\nu=g^{\nu}P$ and $Q_\nu^\circ=Q_\nu\cup\{0\}$. Let $S$ be a circuit modulo $U$ with dependency $\delta$, and split $S$ into blocks $G_1,\dots,G_E$, each contained in one set $\{i:\mathrm{cos}(\delta_i)=c_b\}$, where $\delta$ meets at least two cosets; put $W_b=\sum_{i\in G_b}\delta_i\lambda_i$. Then the classes of the $W_b$ modulo $U$ span a space $\Omega$ of dimension $E-1$, their only relation is $\sum_bW_b=e:=\sum_{i\in S}\delta_i\lambda_i\in U$, and the weights $x_i=\delta_i(\beta_b+s)$ for $i\in G_b$ lie in $P\cup\{0\}$ exactly when $s\in\mathrm{Good}(\beta)=\{s:\beta_b+s\in Q_{-c_b}^\circ\text{ for all }b\}$, with value $\sum_b\beta_bW_b+s\,e$. By the Weil bound~\cite[Theorem~5.41]{LidlNiederreiter1997}, $|\mathrm{Good}(\beta)|\ge\kappa^{-E}\bigl(p-E-(\kappa^E-1)(E-1)\sqrt p\bigr)$ whenever the $\beta_b$ are pairwise distinct; let $E_{\mathrm{cg}}(E,\kappa)$ be the primes at which some such $\beta$ (with at most $E$ blocks) has $\mathrm{Good}(\beta)=\emptyset$. Exhaustive computations up to the Weil bound (finite computations, AI-checked, pending human review) give $E_{\mathrm{cg}}(3,2)=\emptyset$ and $E_{\mathrm{cg}}(3,3)=\{7,13,19,31,37,43,61,67,73,79,97,103,109,127,139,151,157,163,181,193,211,241\}$. So for $p\notin E_{\mathrm{cg}}(E,\kappa)$ a circuit realises every point of $\Omega$ off the at most $\binom{E}{2}$ hyperplanes $\{\beta_b=\beta_{b'}\}$ with $c_b\ne c_{b'}$, by drawing $s$ until $E$ coset tests pass; by part~(a) of Remark~\ref{rem:sde-subquadratic} it never realises a whole plane. Running the triangular recursion with these blocks, and drawing the free scalar $s$ of each round uniformly from $\mathrm{Good}(\beta)$ in the back substitution, moves the next residual along $e$ and steers it off the bad hyperplanes. If $E\ge\kappa$, $p\notin E_{\mathrm{cg}}(E,\kappa)$, every round's columns form a circuit modulo the current space, and no residual offset difference $\beta_b-\beta_{b'}$ with $c_b\ne c_{b'}$ is identically zero as a linear function of the drawn scalars (both conditions can be checked in polynomial time), then each back substitution returns a nonzero solution with probability at least $1-L\binom{E}{2}/\min_\beta|\mathrm{Good}(\beta)|$, where $L\le\lceil a/(E-1)\rceil$ is the number of rounds, and the recursion uses
\[
  M_E(a)=1+m(a+1)-\tfrac{(E-1)m(m-1)}{2}+[r>0](r+1),\qquad a=m(E-1)+r,\ 0\le r<E-1,
\]
columns, which is $(a+1)(a+2)/2$ for $E=2$, $\lfloor(a+2)^2/4\rfloor+[a\text{ odd}]$ for $E=3$, and $a^2/(2(E-1))+O(a)$ in general; the time is polynomial in $a$ and $\log p$ times $\kappa^E$. For i.i.d.\ uniform columns both conditions hold with probability at least $1-\bigl(M_E(a)+L\binom{E}{2}\bigr)/(p-1)$. Hence, for i.i.d.\ uniform columns and $a\ge2$, a randomised polynomial-time solver uses about $a^2/4$ columns for $\kappa=2$ at every prime $p\ge 64a^2$, and for $\kappa=3$ at every prime $p\ge\max(2750,1000a^2)$ (the second range uses an exhaustive computation of $\min_\beta|\mathrm{Good}(\beta)|$ for $p\le 11000$); with $E=\lceil\log_\kappa a\rceil$ and $p\ge\poly(a)$ it uses $O(a^2/\log a)$. The steering condition is genuinely needed: there are solvable column sets with $M_E(a)\ge2a+1$ columns on which it fails and the procedure does not succeed (for $\kappa=3$, $E=3$ whatever blocks are chosen), so for arbitrary columns the best arity proved in this paper remains $(a+1)(a+2)/2$.
\end{remark}
```

If `rem:sde-subquadratic` is not adopted, replace "by part (a) of Remark~\ref{rem:sde-subquadratic}"
with "by the argument of the subquadratic report" (cite the file) or drop that clause. The
parenthesis "(for κ = 3, E = 3 whatever blocks are chosen)" rests on the planted family of §6.2: at
κ = 3, E = 3 the blocks are forced to be the class sets. The failure there is exact on 6 instances,
and the mechanism (e_l = 0 and a forced s) is proved.

## 11. Status, claim gates, next

**Holds:** Lemma 2.1, Proposition A, Theorem B, Lemma W, Theorem C, Corollary C, Proposition H
[proved]; the E_cg tables [exact]; the solver runs [sampled/exact].

**Claim gates that must stay false:**
- "An o(a²), or (a+2)²/4, polynomial SDE solver exists for arbitrary columns." Theorem C needs (ND′)
  and (H1), which hold for random columns, not in the worst case (§6.2).
- "Two-relation objects give two exact directions efficiently." Not shown; Proposition A is evidence
  against it.
- "The result is uniform in p." Theorem C needs G_E(p) ≫ a, i.e. p ≫ a·κ^E.
- "CHMT gives a(a+1)/2 + 1 for every diagonal instance." This is false at a ≤ 2 and unverified for
  a ≥ 3.
- Any novelty claim. The block-refinement and steering idea is simple, and the literature on large-p
  diagonal systems was not searched in depth this pass.

**Next hard question.** Can (ND′) be enforced for arbitrary columns by adaptive choices: column
order, block splits, a few slack columns per round, or a two-relation round providing two defect
directions? Doing so would give a worst-case (a+2)²/4 for p ≫ a. The obstruction to beat is the
planted instance of §6.2 (exactly dependent rounds, so all defects are e_l = 0).

**Next command:** `brt_tests.py adversarial` extended with a `repair` mode that:
- (i) permutes columns at random;
- (ii) adds one slack column per round, using its second dependency as an extra defect direction;
- (iii) retries the forward pass when (ND′) fails.

Expected artifact: a failure rate on the planted family, and a proof or counterexample that one
slack column per round makes (ND′) hold for all inputs with M ≥ M_E(a) + L.

## 12. Artifacts

| file | content |
|---|---|
| `common.py` | copy of the subquadratic pass's exact arithmetic |
| `good_threshold.py` (→ `good_k2_E3.out`, `good_k2_E3_5000.out`, `good_k3_E3.out`, `good_k3_E3_11000.out`, `good_k2_E4.out`) | exact E_cg(E, κ), G_E(p), Weil bound |
| `bf_good.py` (→ `bf_good.out`) | plain enumeration cross-check of the scan |
| `block_check.py` (→ `block_check.out`) | Theorem B against exhaustive R(S) |
| `brt.py` | the solver BRT(E), (ND′) report, arity M_E(a), rank reduction |
| `brt_tests.py` (→ `brt_random.out`, `brt_brute.out`, `brt_adversarial.out`) | random, exhaustive and adversarial runs |
| `brt_scale.py` (→ `brt_scale.out`) | p ≈ 10⁹ runs |
| `two_relation.py` (→ `two_relation.out`) | exact flexibility of two-relation objects and of the collapse rule |
| `test_two_relation.py` (→ `pytest.out`) | pytest checks (8 passed) |

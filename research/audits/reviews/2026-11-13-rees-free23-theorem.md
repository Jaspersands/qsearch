# free23 without a cover: a theorem, G1, G4 and prior art (2026-11-13)

**Status: AI-checked, pending human review.** One AI session (Claude), acting as a hostile helper on the candidate of
`2026-11-13-rees-free23-pair-measurement.md` §9 and its referee `2026-11-13-rees-free23-triples-referee.md`. Scripts and
outputs are in `2026-11-13-rees-free23-theorem/`. No other file was edited. Finite checks only falsify (TRAPS 7).
Citations marked "(memory)" were not re-read (TRAPS 10).

## Verdict

* **G1 is closed, in two ways.**
  * **Lemma W (PROVED by hand; 30/30 computer checks).** The level-2 weight variety has a closed form. Put
    P_k(T) = Σ_i s_i^k λ_i ∈ F_p² for a triple T with labels λ_i and relation s (so P_1 = 0). Then the weight variety
    is exactly
    C = {u ∈ P^{m−1} : Σ_j u_j³ P_3(T_j) = 0, Σ_j u_j² P_2(T_j) = 0}.
    Once these equations hold, the public cubic Q_3 is unique. This explains the referee's "rank 2 after eliminating
    Q_3".
  * **Route A (PROVED, no genericity).**
    * Allow zero weights and take m = 9·g² triples per level-2 state, with g = 2 if p ≡ 2 mod 3 and g = 4 otherwise.
    * A block recursion then finds nonzero weights for **every** label configuration, in expected poly(log p) time.
      This is the (d+1)^ℓ recursion in Ivanyos–Santha's introduction.
    * Cost: at most 1296 copies per run instead of 54.
  * **Route B (PROVED given cited theorems, with a crude constant).**
    * For m = 6 and p > 3, C is a smooth complete-intersection curve, of degree 36 and genus 73, outside a set of
      labels of probability at most 2.27·10⁶/(p − 24).
    * Proof ingredients: an incidence count (hand proof), dominance of the label map (a computer-verified Smith form),
      and Heintz–Bézout with Schwartz–Zippel.
    * The Weil bound and a fibre solver then find weights in poly(log p).
    * The bad-label rate actually observed is about 20–36/p, from 22 expected components.
* **G4 is closed (PROVED).**
  * Apply a uniformly random automorphism of free23 to every copy, once per run (Lemma R).
  * Given the labels, a run is spoiled with probability exactly |B|/(p+1). Here B is the set of distinct special lines
    of the copies used, so |B| ≤ 3·(number of triples used).
* **The proportional-equation issue is closed (PROVED).**
  * The level-3 weights can always be chosen so that the e_3-coefficient C of the equation is nonzero, except with
    probability ≤ 3/p (Lemma C).
  * With Lemma R, two such runs then give proportional equations with probability **exactly 1/p**.
* **Theorem F23 (§5).** Bounded-error, cover-free algorithm for hard cyclic H in free23 from labelled copies.
  * For p ≥ 5000: success per attempt ≥ 0.548. An attempt uses ≤ 2600 + 4 copies (expected), O(log² p) gates times a
    constant, and expected O(log⁴ p) classical bit operations.
  * For 5 ≤ p < 5000: brute force with ≤ 6p³(p+1) copies, a constant.
  * Label: **PROVED given cited theorems**, namely root finding, approximate QFT and the IS normal form of §2 of the
    target, whose phase polynomial is re-derived here.
* **Prior art.**
  * IS Cor 8 does not cover free23: free23 has no abelian subgroup of index p. Nor does any published result we know
    of.
  * Two internal, never-reviewed proposals (`BOUNDED_CLASS_METABELIAN_HSP.md`, `CLASS_THREE_HSP_THEOREM_DRAFT.md`,
    October 2026) claim cover-free algorithms for classes that contain free23. Their relation to Theorem R and to
    this result is **UNKNOWN**. They must be checked before any priority claim (§7).
* **Claim gates stay false:** "exit (ii) closed", "cover unnecessary", novelty. They wait for human review.

## 0. Setting and input model

* **Group.** L is the free 2-generator class-3 Lie algebra over F_p, p > 3, with basis X_0, X_1, Z = [X_0,X_1],
  U = [X_0,Z], W = [X_1,Z]. G = (L, BCH) has order p⁵. For v ∈ V = L/γ_2 we have [v,Z] = v_0U + v_1W.
* **Labels.** A label is λ ∈ γ_3^* ≅ F_p². Write λ·v := λ([v,Z]) = λ_0v_0 + λ_1v_1.
* **Hidden subgroup.** H = ⟨exp η⟩, with η = e_0X_0 + e_1X_1 + e_3Z + η_c, η_c ∈ γ_3 and e = (e_0,e_1) ≠ 0 ("hard"). It
  is determined by η up to F_p^*. Put ε = (e_0, e_1, e_3), η_V = η − η_c and K = exp(F_pη_V)·γ_3, which is abelian.
* **Input** (the two-copy report §1, ρ form). An unlimited supply of i.i.d. labelled copies (λ, ρ_{K,χ_λ}).
  * λ is uniform on γ_3^*.
  * ρ_{K,χ_λ} is the coset state ρ_H after the γ_3-character measurement with outcome λ.
  * χ_λ(exp(tη_V)c) = ω^{λ(c) − tλ(η_c)}.
  * Copies are consumed. The input includes no oracle for H.
* **Output.** η up to F_p^*.
* **Operations.**
  * All classical computations are over F_p: labels, relations, power sums, weights, Q_3, R, μ, and square and cube
    roots.
  * All quantum operations are reversible F_p-arithmetic, QFT_p, and measurements of public functions.
  * In route B, the curve C is defined over F_p; its geometry is taken over F̄_p and its points are sought in F_p.

## 1. The per-copy phase (Lemma 0)

**Setup for one copy** with label λ ≠ 0:
* g_0 = (λ_1, −λ_0), and x' with n = λ·x' ≠ 0;
* δ = det(g_0,x'), f(v) = λ·v/n and h(v) = det(x',v)/det(x',g_0), so that v ≡ f(v)x' + h(v)g_0 mod γ_2.

**Lemma 0** (§2 of the target: PROVED there, and re-checked exactly by the referee's independent code). Suppose
λ·e ≠ 0. After promotion to G/ker λ and the QFT over N_λ, the outcome y = (j,k) in sector l = −1 leaves the pure state
p^{−1/2} Σ_x ω^{P(x)}|x⟩. The phase is independent of the base point, up to a global phase, and

f(e)·P(x) = A_1x + A_2x² + A_3x³, with A_3 = −(nδ/6)h(e), A_2 = (kδ/2)h(e) + (n/2)e_3, A_1 = −j·h(e) − k·e_3 + λ(η_c).

* **Re-derived here from BCH.** Take ν = log(exp(xη')exp(−xx')), with η' = η/f(e) and P = −jν_{g_0} − kν_z +
  λ(ν_{γ_3}), as in the referee's `f23.closed_form`. The derivation uses λ([g_0,Z]) = 0 and λ([Z,x']) = −n.
* **Sign conventions.** They differ from the target's κ by a sign. Nothing below depends on that sign.
* **Each A_i is linear** in the hidden vector (h(e), e_3, η_c), with public coefficients. Here h(e) is linear in e.

**Lemma L (expansion along a line; PROVED, elementary).** Let x = Y + τv with v = c·s·f(e), c a public scalar. Then

P(Y + τv) = P(Y) + τ·cs(A_1 + 2A_2Y + 3A_3Y²) + τ²·c²s²f(e)(A_2 + 3A_3Y) + τ³·c³s³f(e)²A_3.

Every coefficient of τ^{≥1} is a polynomial in e with **no pole**. Each is linear in (h(e), e_3, η_c).

## 2. The pipeline as polynomial identities (writes out G3)

These proofs use only Lemmas 0 and L. Index the copies (j,i) for triple j = 1..m and i = 1..3.

**Triples (level 1).**
* Labels in a triple are nonzero and pairwise independent.
* s = (det(λ_2,λ_3), det(λ_3,λ_1), det(λ_1,λ_2)). All entries are nonzero, and P_1 = Σ s_iλ_i = 0 (Cramer).
* Measure S = Σ_i n_ix_i. The hidden direction φ(e) = (s_if_i(e))_i lies in the plane {Σ n_ix_i = 0}, because
  Σ n_is_if_i(e) = P_1·e = 0.
* The referee's code normalises s to (s_1, s_2, 1). That rescales P_k(T) by det(λ_1,λ_2)^{−k}, which is absorbed by
  u_j ↦ det(λ_1,λ_2)u_j.

**Level 2.**
* Take public u ∈ F_p^m \ {0}; zero entries are allowed, and a triple with u_j = 0 is measured out and discarded.
* Fix an invertible public M and put ε = M^{−1}w. Measure the coset of {(u_jφ_j(ε))_j : w ∈ F_p²}, then add a public
  cubic phase Q_3(w).
* For fixed H, the result is the pure state ω^{Φ(w)}, where Φ(w) = Σ_{j,i} P_{ji}(X_{ji} + u_js_{ji}f_{ji}(ε)) + Q_3(w)
  and the X are public base coordinates.
* Along w = w_0 + τMe, every copy moves as in Lemma L, with c = u_j.

**Lemma W (structure of the level-2 conditions; PROVED).**
* The target's (S) says that the directional derivative ∂_{Me} of the cubic part of Φ vanishes for all e. (W) follows
  from (S) by polarisation.
* **Claim 1.** A Q_3 satisfying (S) exists iff Σ_j u_j³P_3(T_j) = 0, and it is then unique.
* **Claim 2.** The e_3-terms vanish, both in the τ²-coefficient and in the bilinear form B below, iff
  Σ_j u_j²P_2(T_j) = 0. This is (E3).

*Proof.*
1. The (S)-tensor of the cubic part, in (e; ε, ε) coordinates, is 3Σ_j u_j³Σ_i κ_{ji}s_{ji}³h_{ji}(e)f_{ji}(ε)²,
   where κh(e)f(ε)² = ∓ℓ(e)m(ε)²/6 with ℓ = det(x',·)/n and m = λ·(·).
2. ∂_{Me}Q_3 is totally symmetric. Q_3 ↦ its symmetric tensor is a bijection onto Sym³ (dimension 4, p > 3).
3. So (S) is solvable iff the non-symmetric part of the first tensor vanishes.
4. For ℓ⊗m⊗m that part is (2/3)m(ε)(ℓ∧m)(e,ε), with (ℓ∧m)(e,ε) := ℓ(e)m(ε) − m(e)ℓ(ε) = −det(e,ε), because the
   coefficient vectors of ℓ and m have determinant −(λ·x')/n = −1. Hence the non-symmetric part is a nonzero
   constant times det(e,ε)·(Σ_j u_j³P_3(T_j))·ε.
5. This proves Claim 1. The choice of chart x' changes ℓ by a multiple of m, which changes only the symmetric part.
6. For Claim 2, the e_3-part of A_2 is (n/2)e_3. It contributes (e_3/2)Σ_{j,i}u_j²s_{ji}²n_{ji}f_{ji}(·) =
   (e_3/2)(Σ_j u_j²P_2(T_j))·(·). ∎

**Computer check** (`structure_check.py`, `structure_check.out`): row space of K = row space of [P_3(T_j)], and row
space of E = row space of [P_2(T_j)], in **30/30** of the referee's numerically built configurations (p = 101, 227, 503,
10007, 30011). Inside the full pipeline, the Q_3 solve was consistent in all 123 level-2 states of §6.

**After level 2, along every line w_0 + τMe (PROVED from Lemma L, (S), (W), (E3)):**
* the τ³-coefficient is 0;
* the τ²-coefficient is B(e,e), and does not depend on w_0, by (W);
* the w_0-dependent part of the τ-coefficient is 2B(ε_0, e).
Here B(ε, e) = Σ u_j²s_{ji}²f_{ji}(ε)(A_2 + 3A_3X)_{ji} is a **public** bilinear form, because its e_3-part vanishes by
(E3). The η_c-part of every τ-coefficient is −Σ_j u_jP_1(T_j)(η_c) = 0.

**Level 3.**
* Merge three level-2 states with weights u' ≠ 0 (zeros allowed), aligned to the same M, and add a public quadratic
  R.
* Condition: Σ_l u_l'²B_l + B_R ≡ 0.
* B_R is an arbitrary symmetric form, so this is **one** linear condition, Σ_l c_l u_l'² = 0, where c_l is the
  antisymmetric part of B_l. This is a diagonal conic.
* When it holds, the τ- and τ²-coefficients have no w_0-dependence, and the τ²-coefficient (Σu'²B_l + B_R)(e,e) is 0.

**Lemma E (PROVED).**
* After level 3, the phase along every line w_0 + τMe is c_0(w_0) + μτ.
* μ = a·e + C·e_3 is a linear form with public coefficients and no η_c.
* A QFT over F_p² therefore returns z with z·Me = μ, **with certainty** (translation by Me multiplies the state by
  ω^μ).
* Each run gives the equation ℓ·ε = 0, with ℓ = (Mᵀz − a, −C).

**Lemma C0 (closed form of C; PROVED; checked in 123/123 states).** C = Σ_l u_l'D_l, where

D_l = Σ_j u_j Σ_i s_{ji}(n_{ji}X_{ji} − k_{ji})

evaluated at the base point w = 0 of state l, and k_{ji} is the second entry of copy (j,i)'s front-end outcome.
* This is the e_3-part of Lemma L's τ-coefficient: cs(−k + nY)e_3.
* By (E3) it does not depend on the level-3 offset.

## 3. G1: existence and computation of the level-2 weights

### 3.1 Route A: constructive weights for every label configuration (Lemma B, PROVED)

**Lemma B.** Let d ∈ {2,3} and c_1, …, c_N ∈ F_p, with p > 3.
1. **One equation.**
   * If N ≥ 3 (d = 2), or N ≥ 4 (d = 3, p ≡ 1 mod 3), or N ≥ 2 (d = 3, p ≡ 2 mod 3), a nonzero v with
     Σc_iv_i^d = 0 can be found in expected poly(log p) time.
   * If some c_i = 0, take e_i.
   * If d = 3, use pigeonhole on the three cube classes (−1 is a cube), then one cube root.
   * If d = 2, first try two-term solutions. Otherwise fix v_3 = 1 and draw v_1 at random. Then
     (−c_3 − c_1v_1²)/c_2 is a square with probability ≥ (p−1)/(2p), because the conic has p ± 1 affine points and
     each v_1 carries at most two of them.
2. **Two equations** (columns c_i ∈ F_p²) from N = g² variables, with g = 3 for d = 2 and g = g_3 ∈ {2,4} for d = 3.
   * Split into g blocks of g. Solve the first coordinate in each block, giving w^(b).
   * Then solve the second coordinate for the block sums Σ_{i∈b}(w_i^(b))^d c_i, giving e.
   * Put v = Σ_b e_b w^(b).
3. **Level 2.**
   * Take m = 9g_3² triples, in R = g_3² groups of 9.
   * Apply step 2 with d = 2 to the columns P_2 in each group, giving v^(k).
   * Apply step 2 with d = 3 to the columns A_k = Σ_{j∈k}(v_j^(k))³P_3(T_j), giving c.
   * Put u = Σ_k c_kv^(k). Then u ≠ 0, Σu_j²P_2 = Σ_k c_k²·0 = 0 and Σu_j³P_3 = Σ_k c_k³A_k = 0.

So m = 36 triples for p ≡ 2 mod 3 and m = 144 for p ≡ 1 mod 3. The cost is O(m) field operations plus O(m) square or
cube roots: Tonelli–Shanks and Adleman–Manders–Miller, which are Las Vegas because they need non-residues (memory).
**No genericity is used.** Lemma B is the recursion "n ≥ (d+1)^m ⇒ SDE solvable" that Ivanyos and Santha state in their
introduction (with m = 2: 3² = 9, 4² = 16), applied once per degree. It is not new.

### 3.2 Route B: the m = 6 curve (Lemma G)

Write A = [P_3(T_j)] and B = [P_2(T_j)], both 2×6, and X(A,B) for C ⊂ P⁵.

**Lemma G1 (generic smoothness; PROVED by hand).** For every algebraically closed k of characteristic > 3, the set
Z ⊂ A²⁴ of (A,B) for which X(A,B) is not a smooth curve is a proper closed subset.
1. **Singular points.** Take u ∈ X with support J. It is singular (Jacobian rank < 4) iff there is (α,β) ≠ 0 with
   3u_jα·a_j + 2β·b_j = 0 for all j ∈ J.
2. **Fibres.** For fixed (u,α,β), these |J| conditions and the 4 equations of X are linear in (A,B). They have
   exactly one dependency, Σ_j u_j²·(…) = 3α·F_cub + 2β·F_quad (Euler), so their rank is |J| + 3.
3. **Dimension count.** The stratum of (u,α,β) has dimension |J| + 2. So the incidence over support J has dimension
   24 − (|J|+3) + (|J|+2) = 23 < 24. Projecting from P⁵ × P³ is proper, so Z is closed.
4. **Dimension one.** A component of dimension ≥ 2 has Jacobian rank ≤ 3, so it is included in Z.
5. **Off Z.** X is a smooth complete intersection curve: degree 36, K = O(4), and genus 73 by adjunction. It is
   connected (Hartshorne III Ex. 5.5, memory), hence geometrically irreducible, and it is not contained in any
   hyperplane.

**Lemma G2 (dominance; computer-verified identity).** The per-triple map ψ: (λ_1,λ_2,λ_3) ↦ (P_2, P_3) ∈ A⁴ is
dominant over F̄_p for every odd p.
* `psi_dominance.sage`: the integer Jacobian of ψ at λ = ((1,0),(0,1),(1,2)) has elementary divisors [1,1,2,2]. So it
  has rank 4 mod every odd p.
* A morphism whose differential is surjective at some point is dominant (use the generic smoothness of the image).

**Lemma G3 (explicit bad-label bound; PROVED given Heintz 1983, memory).**
1. **Cover Z by three families.**
   * Z_J for |J| = 6 and |J| = 5: singular points of exact support J.
   * Y_J for |J| = 4: X ∩ P^J ≠ ∅. Every point of support size ≤ 4 is singular by Euler, so the smaller supports are
     covered.
2. **Degree bounds.**
   * Work in the chart u_{j_0} = 1 with one generic linear normalisation of (α,β). The equations have degrees 4,4
     (cubics), 3,3 (quadrics), 3 (each G'_j) and 1.
   * Heintz's Bézout inequality and "linear images do not raise degree" give deg Z_J ≤ 144·3^{|J|}.
   * They also give deg Y_J ≤ 4·144.
   * Total: deg Z ≤ 104,976 + 6·34,992 + 15·576 = 323,568.
3. **A hypersurface.** For each component, a generic projection to A^{dim+1} gives a hypersurface. Pulling it back
   gives R ≢ 0 with Z ⊆ V(R) and deg R ≤ 323,568.
4. **Pullback to labels.** Each entry of A has label-degree 7 and each entry of B has degree 5. So R∘Φ has degree
   ≤ 2,264,976. It is ≢ 0 by Lemma G2.
5. **Schwartz–Zippel.** With admissible labels (probability ≥ 1 − 24/p),

   Pr[C singular or not a curve] ≤ 2,264,976/(p − 24).

**Observed** (`badfrac.out`, `badfrac_400.out`, labels → A, B through Lemma W):

| p | bad configurations |
|---|---|
| 101 | 81/400 |
| 401 | 22/400 |
| 1601 | 9/400 |
| 6007 | 0/400 |

* This is p·(fraction) ≈ 20–36. Uniform (A,B) gives 12–20.
* That matches 15 + 6 + 1 = 22 hypersurface components (Y_J, Z_J with |J| = 5, and Z_main), each contributing about
  1/p by Lang–Weil.
* **Char 0 (`smooth_QQ.out`).** One integer configuration over QQ: C is a curve with Hilbert polynomial 36t − 72, so
  degree 36 and arithmetic genus 73, as Lemma G1 predicts. The singular-locus computation (minors of the 4×6 Jacobian)
  did not finish within 900 s in the first run. **Addendum (11-13 evening):** rerun in Singular (modStd, char 0;
  `2026-11-13-rees-long-runs/smooth_QQ.sing`, `.out`): dim of the cone 2, dim of the singular cone 0, and the
  singular-locus radical contains the irrelevant ideal, so C is **smooth over QQ** for this configuration
  (2347 s, 0.77 GB). Exact computation for one configuration only; it agrees with Lemma G1 and with the mod-32003 check
  (`smooth_F32003.out`). Nothing in G1–G4 depends on it.
* The proved constant is therefore pessimistic by about 10⁵. This explains the referee's 4/6 singular configurations
  at p = 101.

**Lemma G4 (fibre solver; PROVED given Weil and standard zero-dimensional solving).**
1. If C is smooth, then #C(F_p) ≥ p + 1 − 146√p by the Weil bound for genus 73.
2. **Zero weights are allowed.** So the torus is not needed, but u_1 ≠ 0 is needed for the chart. At most 36 points
   have u_1 = 0, because C is not contained in a hyperplane.
3. **The fibres** C ∩ {u_6 = tu_1} are finite of size ≤ 36, and they partition the points with u_1 ≠ 0.
4. **So for random t,** Pr[the fibre has an F_p-point] ≥ (p − 146√p − 35)/(36p). That is ≥ 0.027 for p ≥ 10⁸.
5. **Solving one fibre** is a zero-dimensional system of bounded shape: Macaulay-matrix Gröbner basis, then
   Cantor–Zassenhaus root finding. This is O(1) field operations plus poly(log p) (memory).

Route B therefore costs 54 copies per run but needs p ≥ ~10⁸ for its proved constants. Route A needs p ≥ 5000.

## 4. G4 and the proportional equations

**Lemma R (automorphism randomisation; PROVED).**
* **The automorphisms.** Any images y_0, y_1 of X_0, X_1 that are independent modulo γ_2 define an automorphism σ
  (L is free).
* **Action on ε.** σ acts on ε by the linear map T_σ: e' = Ae and e_3' = α·e + det(A)e_3. Here A ∈ GL_2 is the V-part
  of σ, and α holds the Z-components of y_0 and y_1.
* **Action on copies.** U_σ: |g⟩ ↦ |σ(g)⟩ maps a labelled copy (λ, ρ) of H to a labelled copy (λ∘σ^{−1}, ·) of σ(H),
  and uniform labels stay uniform.
* **The algorithm.** Draw σ uniformly once per run, apply U_σ to the run's copies, run the pipeline on σ(H) to get ℓ,
  and output ℓ' = T_σᵀℓ. Then ℓ'·ε = 0.

*Claims and proofs.*

**(a) Spoiled runs.**
* Given σ(H), σ is uniform on a coset of Stab(H). The labels λ' seen by the algorithm are independent of A, and
  e' = Ae is uniform on F_p² \ 0 given λ'.
* A copy is spoiled iff λ'·e' = 0, the referee's G4 event.
* The supports of the level-2 weights are chosen from λ' alone; the copies actually used are a subset of them. Labels
  within a triple are pairwise independent. So, given the labels,

  Pr[some copy in the level-2 supports is spoiled] = |B|/(p+1),

  where B is the set of distinct lines ker(λ'·) over those copies, and |B| ≤ 3·#(triples in the supports).

**(b) Independence of the equations.**
* Conditional on (σ(H), A), α is uniform on an affine line α_0 + F_p(−e_1,e_0). Each α has the same number p² of
  γ_3-completions.
* T_σᵀℓ = (Aᵀℓ_e + ℓ_3α, det(A)·ℓ_3). If ℓ_3 = −C ≠ 0, the class [ℓ'] is uniform on the p points of P(ε^⊥) other
  than [(−e_1, e_0, 0)].
* This holds independently for each run, because each run uses a fresh σ and its outputs are a function of σ(H) and of
  the run's own randomness.
* So two runs with C ≠ 0 give proportional equations with probability **exactly 1/p**. Otherwise ℓ'_1 × ℓ'_2 ∝ ε.

**Lemma C (C ≠ 0 can be enforced; PROVED).**
* The algorithm knows D = (D_1, D_2, D_3) before level 3. It chooses u' on the conic Σc_lu_l'² = 0 with u'·D ≠ 0.
* Such a u' exists unless some D_l = 0:
  * smooth conic: p + 1 points, and the line u'·D = 0 meets it at most twice;
  * c_l = 0 for some l: e_l is on the conic, and e_l·D = D_l.
* For a smooth conic, a good point is found by the rational parametrisation from one random point.
* **D_l has a uniform part.** D_l = Σ_j u_js_{j1}r_j + (terms independent of r). Here r_j is triple j's S-outcome,
  through the public representative x_r = (r/n_1, 0, 0). The r_j are uniform and independent of the labels, the
  outcomes k, the level-2 outcomes and u. And some u_js_{j1} ≠ 0.
* So Pr[D_l = 0] = 1/p, and Pr[no good u'] ≤ 3/p.

**Exact per-attempt success.** An attempt is two runs, plus 2 copies for η_c and 2 for verification. In route A, N_T
= #used triples ≤ 27g_3² (432 or 108). Then

s(p) ≥ E[(1 − |B_1|/(p+1))(1 − |B_2|/(p+1))]·(1 − 3/p)²·(1 − 1/p) ≥ (1 − 3N_T/(p+1))²(1 − 3/p)²(1 − 1/p).

* This is ≥ 0.548 at p = 5003 (p ≡ 1 mod 3), and ≥ 0.507 from p ≈ 4500.
* It is ≥ 0.873 at p = 5003 for p ≡ 2 mod 3.
* Route B (N_T = 18, plus the bad-label and fibre terms) gives s ≥ 0.867 at p = 10⁸.

## 5. Theorem F23

**Theorem F23 (PROVED given cited theorems; AI-checked, pending human review).**

*Hypotheses.*
* Let p ≥ 5 be prime, and let G = free23 over F_p, given by Lie coordinates and BCH multiplication.
* Let H = ⟨exp η⟩ be any hard cyclic subgroup, that is, one with e ≠ 0.
* Input: i.i.d. labelled copies (λ, ρ_{K,χ_λ}) with λ uniform (§0). No other access to H.

*Conclusions.*
1. **p ≥ p_0 = 5000.** Algorithm A outputs a generator of H with probability ≥ 1 − 0.452^R − R/p². Each of its at
   most R attempts consists of:
   * two runs (route A: each run draws 3·m admissible triples, uses ≤ 3m, m ∈ {36, 144}, and applies a fresh
     automorphism);
   * a solve ε ∝ ℓ'_1 × ℓ'_2;
   * the η_c step: restrict 2 copies with independent labels to cosets of K and Fourier-sample K ≅ F_p³, which returns
     λ(η_c) deterministically;
   * verification: phase-estimate R_ĥ on 2 fresh copies. A correct ĥ passes with certainty; a wrong ĥ passes with
     probability ≤ 1/p per copy.

   Copies per attempt: 18m/q_adm + 4/(1 − 1/p) in expectation, where q_adm ≥ 0.9994 is the probability that a
   batch of 3 labels is admissible. That is ≤ 2600 + 4 for m = 144 and ≤ 650 + 4 for m = 36.
2. **Quantum cost per attempt.** O(N_copies) F_p-arithmetic operations and QFT_p's, hence O(log² p) gates with an
   absolute constant times ≈2600 (not computed exactly). The approximate-QFT error is additive by a hybrid argument
   (memory, G5).
3. **Classical cost.** O(m) field operations and roots per run: expected O(log⁴ p) bit operations.
4. **5 ≤ p < 5000.** Test every hard cyclic subgroup (p³(p+1) of them) with v = 6 fresh copies each, and output the
   first that passes. The error is ≤ p³(p+1)/p⁶ ≤ 2/p². This uses ≤ 6p³(p+1) copies, a constant (≈ 3.75·10¹⁵ at the
   threshold). It is cover-free and useless in practice.
5. **Route B variant.** Same statement with 54 copies per run, for p ≥ 10⁸, using the m = 6 fibre solver (§3.2).

*Dependencies.*
* **Cited theorems:**
  * Lemma 0 (target §2; re-derived phase);
  * Las Vegas square and cube roots in F_p;
  * QFT_p;
  * for route B only: Weil, Heintz–Bézout, Schwartz–Zippel, connectedness of smooth complete intersections, and
    zero-dimensional solving.
* **Hand proofs:** Lemmas L, W, B, C, C0, E, G1, G3 and R (§§1–4).
* **Computer-verified identity:** the Smith form in Lemma G2.
* **Finite falsification checks only** (not used in the proofs): the 30 Lemma-W configurations, §6, and badfrac.

## 6. Simulation (falsification only; `theorem_pipeline.py`, outputs `tp_11.out`, `tp_13.out`, `tp_17.out`)

**What was simulated.**
* The states are true group-level states from the referee's `f23.py`: random base points, exact sampling of y, S,
  the coset measurements and z.
* New here: the Lemma-B weights, Lemma C's choice of u', and Lemma R's random automorphism with pull-back.
* Copies of σ(H) were generated directly rather than by applying U_σ. The two are equal in distribution.
* Labels were conditioned to avoid the true special line. This is H-dependent conditioning, and G4 is handled
  analytically instead.

| p (m) | runs | equations correct | Lemma-W Q_3 solve fails | C closed form fails | support violations | C forced 0 | proportional pairs | recovery from disjoint pairs |
|---|---|---|---|---|---|---|---|---|
| 11 (36) | 30 | 29/29 | 0 | 0 | 0 | 1 (bound 3/p) | 39/406 = 0.096 (1/p = 0.091) | 12/14 |
| 13 (144) | 6 | 6/6 | 0 | 0 | 0 | 0 | 1/15 | 2/3 |
| 17 (36) | 6 | 6/6 | 0 | 0 | 0 | 0 | 0/15 | 3/3 |

* Every recovery failure is a proportional pair.
* Used copies per run averaged 92.
* D_l matched its closed form, with the sign (−k + nX), in 123/123 level-2 states.

## 7. Prior art (Task 4)

* **Ivanyos–Santha** (`…/lit/is_1503.09016.txt`; Prop 7, Cor 8, Thm 5, Thm 3, and the introduction's (d+1)^m remark).
  * Cor 8 solves the HSP in F_p ⋉ F_p^m of constant class, for subgroups of order p not in F_p^m.
  * free23 is not of this form. Every maximal subgroup is non-abelian (core paper, l. 226; example at l. 875ff). IS therefore applies only
    to the quotients fil4_λ = G/ker λ, and only with copies from one quotient. That costs Θ(√p) uniform labels (target
    §1).
  * What the present procedure takes from IS:
    * the per-copy front end (their §4.1/§5);
    * the power-weight idea, as Σ s^kλ = 0 for k = 1, 2, 3, but across quotients;
    * the diagonal-system recursion (Lemma B).
  * What is new relative to IS, if it is new at all: the cross-quotient aligned plane merges, with a public cubic and
    quadratic correction (Lemma W, level 3), and the automorphism randomisation.
* **Other published results** (as surveyed in core §related, l. 222): Bacon–Childs–van Dam (constant m), ISS (class 2),
  FIMSS (bounded exponent), Imran–Ivanyos (bounded primes, or conditional on zero sums), Decker et al. None covers
  free23 with p growing. The core paper says "we know of no earlier method" for free23 (l. 222). It also says it does
  not claim the cover is necessary (l. 228). Theorem F23 would be the first written cover-free route. **Novelty is
  unchecked beyond this local reading.**
* **Internal, unreviewed proposals that would overlap** (not read in full):
  * `research/BOUNDED_CLASS_METABELIAN_HSP.md` (2026-10-21) proposes a cover-free algorithm for every fixed-class
    metabelian group. free23 is metabelian, since γ_2 is abelian.
  * `research/CLASS_THREE_HSP_THEOREM_DRAFT.md` makes the analogous class-three proposal, through an "unknown-support
    Kraus instrument" and SDE weights.
  * The 11-01 priority check lists both as unreviewed (`2026-11-01-rees-priority-check.md` P7).
  * A false shortcut through metabelian quotients was refuted in `2026-11-02-rees-application.md` §5. That refutes the
    quotient step, not the instrument itself.
  * Whether these drafts are correct, and whether Theorem R of the 11-12 note excludes them, is **UNKNOWN**. They
    are internal, so they do not affect priority against the literature. They do bear on the internal consistency of
    the claim "Theorem R forces binary weights in SOT(Aut)".

## 8. Claim gates, next question

**Gates.** These stay false until human review: "exit (ii) closed", "a poly-time non-binary merge exists", "the cover
is unnecessary for free23", and any novelty or priority. If a human confirms Lemma 0 and §2, the core paper's sentence
"we do not claim that the cover is necessary" (l. 228) could be strengthened for free23. That is not done here.

**Next hard question.** Is Theorem F23 an instance of a general cover-free method for graded class-3 Lazard groups?
Equivalently: does the power-sum structure (P_1, P_2, P_3 cancelled at three levels) generalise to class c with levels
P_1, …, P_c?
* Next command: rerun `structure_check.py`-style derivations for the free 3-generator class-3 algebra (γ_3 of dimension
  8).
* Expected artifact: `…-free33-structure.md`.
* Acceptance test: the level-2 conditions are again power sums of the labels.

Separately, a reviewer should adjudicate `BOUNDED_CLASS_METABELIAN_HSP.md` against Theorem R.

## 9. Adversarial self-check

* **Is Lemma W too clean?** It was derived by hand and then tested against the referee's numerically built K and E,
  which were built without this formula: 30/30. It was also tested inside the pipeline: 123 consistent Q_3 solves. A
  sign error in κ would not change the zero sets.
* **Does allowing zero weights break anything?** A triple or state with weight 0 is measured out. Every identity in §2
  sums only over the support. The simulation used weights with zeros and found 0 violations.
* **Lemma R needs U_σ applied to the copies.** The simulation generated copies of σ(H) directly. The two agree in
  distribution (§4), but the circuit for U_σ was not simulated.
* **Pr[D_l = 0] = 1/p** depends on the S-representative convention. With x_r = (r/n_1, 0, 0), the coefficient is
  s_{j1} ≠ 0. A different public representative ξ needs s·ξ ≠ 0. This is stated, not hidden.
* **Spoiled copies** were conditioned away in the simulation. The analytic bound |B|/(p+1) uses only the uniformity
  of e' given the labels, which holds because σ is fresh per run. With no randomisation, the bound 3N_T/(p+1) still
  holds per run, but the 1/p proportionality claim would not.
* **Route B's constant** (2.27·10⁶) is proved but absurd. The observed rate is about 22/p. The degree bounds use
  Heintz from memory. Route A avoids all of this.
* **Cited from memory:** Heintz (Bézout inequality, linear images), Hartshorne III Ex. 5.5, the Weil bound,
  Tonelli–Shanks, Adleman–Manders–Miller, Cantor–Zassenhaus, and approximate QFT. IS statements were read from the
  local text.
* **Not done:**
  * the exact gate constants;
  * the approximate-QFT error budget (G5);
  * a full reading of the two internal metabelian drafts;
  * an external literature search (no network);
  * an end-to-end simulation at p ≥ 5000 (falsification only, at p ≤ 17).
* **Lemma 0 is inherited.** The phase polynomial is re-derived here. The mechanics of the IS front end (pure state,
  base point only a global phase) rest on the target's §2 proof and the referee's exact checks (174 copies). If
  Lemma 0 failed, everything would fail. It is the first thing to review.
* **Overclaim risk.** "Theorem" here means a written AI proof, checked only by falsification tests. It does not move
  any STATE row without human review.

## Reproduce (from the folder; python = /opt/anaconda3/bin/python, sage = /opt/anaconda3/envs/qsearch-cas/bin/sage, all under nice -n 19)

```
python structure_check.py > structure_check.out          # Lemma W vs the referee's curve_*.json, <1 s
sage psi_dominance.sage > psi_dominance.out               # Lemma G2 Smith form, ~15 s
sage badfrac.sage labels 400 101,401,1601,6007 > badfrac_400.out; sage badfrac.sage uniformAB 400 101,401,1601 >> badfrac_400.out   # ~4 min
sage smooth_QQ.sage > smooth_QQ.out                       # char-0 cross-check of one configuration: dim/Hilbert poly 36t-72 only; singular locus timed out at 900 s; Singular rerun in 2026-11-13-rees-long-runs/smooth_QQ.out: smooth over QQ
./queue.sh                                                # theorem_pipeline.py at p = 11 (30 runs), 13, 17 (6 runs each); < 10 min, < 0.2 GB
```

Acceptance:
* 30/30 row-space equalities;
* elementary divisors [1,1,2,2];
* p·(bad fraction) bounded as p grows;
* in `tp_*.out`: every pulled-back equation holds, and lemmaW_q_fail = C_formula_fail = supp_viol = 0.

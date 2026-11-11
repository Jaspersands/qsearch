# Context: worst-case {0,±1}-zero-sums over F_5 (AI-only research; advisory)

## Problem and prior proved inputs (from repository notes, AI-refereed)

Problem. Given arbitrary (adversarial) λ_1..λ_m ∈ F_5^n, find nonzero x ∈ S^m, S = {0, ±1}, with
Σ x_i λ_i = 0, deterministically in poly(n, m) time. Known: KOW (arXiv 2510.07515) Thm 3.7 at q = 5:
m ≥ ((1−1/5)/(1−5^{−r})) n(n+1)/2 + r(n+1) (leading 0.4 n²). Repository Theorem B′ (AI-refereed):
m ≥ n²/4 + 3n/2 + 2.

Setup. Work in V = F_5^q (original space modulo an already-realized subgroup U). For a set X of
columns (images v_i ∈ V), D(X) = {c ∈ F_5^X : Σ c_i v_i = 0}. For a k-dim subspace W ⊆ D(X) with
basis rows w_1..w_k, the label of column i is ℓ_i = (w_1(i), …, w_k(i)) ∈ F_5^k; supp W = {i : ℓ_i ≠ 0}.
R(Y) = {Σ_{i∈Y} y_i v_i : y ∈ S^Y}. Y gains H if R(Y) contains the subgroup H.

Lemma 1 (recursion). If Y gains H and T is disjoint from Y with y_T ∈ S^T∖0, Σ_T y_i v_i ∈ H, then some
y_Y ∈ S^Y gives Σ_T + Σ_Y = 0. Iterating along a chain of realized subgroups (each piece realizes its
subgroup modulo the earlier ones, pieces disjoint) until codimension 0, then any remaining column
(weight 1), solves the instance.

Lemma 2 (label formulation). (A) Let L ⊆ F_5^d∖0 be the label set of W (d = k here). If Φ: L → S^d and
γ_α ∈ F_5^d (α ∈ F_5^d∖0) satisfy y_α(ℓ) := ⟨α, Φ(ℓ)⟩ + ⟨γ_α, ℓ⟩ ∈ S for all α, ℓ ∈ L ("feasible"), and for
every projective direction [α] some λα has y_{λα} ≢ 0 on L ("weakly nondegenerate"), then with
h_j = Σ_{i ∈ supp W} Φ_j(ℓ_i) v_i the realizers y_α(ℓ_i) give Σ_i y_α(ℓ_i) v_i = α·h (because
Σ_i ⟨γ_α, ℓ_i⟩ v_i = 0, a dependency in W); so supp W gains ⟨h_1..h_d⟩ if the h_j are independent, else
some nonzero realizer is an S-witness. Multiplicities of labels are irrelevant. (B) If X has exactly one
column per label and no feasible weakly nondegenerate (Φ, γ) exists, then R(X) contains no d-dim
subgroup and 0 has no nonzero S-realizer. Proof of (B): a d-dim H ⊆ R(X) gives realizers y_α with
Σ y_α(i) v_i = α·h; Φ_i := (y_{e_j}(i))_j; y_α − Σ α_j y_{e_j} ∈ D(X), i.e. equals ⟨γ_α, ℓ_i⟩.

Fact F5 (finite, certified two ways). Every label set L ⊆ F_5²∖0 spanning F_5² (any size) admits a
feasible weakly nondegenerate (Φ, γ) with d = 2. (Table of 36,090 GL_2(F_5)-orbits.)

Fact T3 (finite, CaDiCaL UNSAT + fixed LRAT checker). L = F_5^3∖0 (all 124 labels) admits no feasible
weakly nondegenerate (Φ, γ) with d = k = 3.

Theorem B′ proof sketch: at codimension q take q+2 columns, any two independent dependencies, Fact F5:
cost ≤ q+2 per 2 dims; Σ_{q=n,n−2,…}(q+2) ≈ n²/4.

## Claim 1 (new): SPARSE2, m ≥ (6/25) n² + (12/25) n log_5 n + 3n + 3 suffices

Algorithm, stage at codimension q ≥ 2: choose r = r(q) ∈ [2, ⌈log_5 q⌉ + 2] (deterministic rule).
Take the first q + r unused columns X (images in V). dim D(X) ≥ r; fix an r-dim D0 ⊆ D(X) with basis
matrix G (r × (q+r)), labels g_i ∈ F_5^r (columns of G; G has rank r). Enumerate all 2-dim subspaces
W of the row space of G (equivalently all rank-2 A: F_5^r → F_5^2 up to GL_2, W = row space of AG;
[r,2]_5 = O(25^r) = O(q²) of them), and take W minimizing |supp W| = #{i : A g_i ≠ 0}. Labels A g_i
(i ∈ supp W) span F_5^2 (AG has rank 2). Fact F5 → gain 2 or witness. Columns of X ∖ supp W return to
the pool. Cost of the stage = |supp W|.

Averaging bound: a fixed nonzero g ∈ F_5^r lies in the kernel K = ker A, a codim-2 subspace, for a
fraction ρ_r = [r−1,2]_5/[r,2]_5 = (5^{r−2} − 1)/(5^r − 1) of all codim-2 subspaces K. Hence
min_W |supp W| ≤ (1 − ρ_r)·#{i : g_i ≠ 0} ≤ (q + r)(1 − ρ_r) = (q + r)·(24/25)·5^r/(5^r − 1).
With r0 = ⌈log_5 q⌉ + 1 (5^{r0} ≥ 5q): cost ≤ (24/25)(q + r0)(1 + 1/(5q − 1)) ≤ (24/25)(q + log_5 q + 3).
q = 1: 2 columns realize the line ({a + bc : a,b ∈ S} = F_5 for c ≠ 0) or give a witness; then one
closing column. Pool: at codimension q the algorithm needs q + r unused columns. Recursion
G(0) = 1, G(1) = 3, G(q) = max(q + r, c(q) + G(q − 2)), c(q) = ⌊(q + r)(1 − ρ_r)⌋.
Sum: Σ_{q = n, n−2, …, ≥2} (24/25)(q + log_5 q + 3) ≤ (24/25)[(n² + 2n)/4 + (n/2) log_5 n + 3n/2]
= 0.24 n² + 0.48 n log_5 n + 1.92 n. Pool term: at a stage, q + r − c(q) ≤ (q + r)/25 + 1, which is at most
the cost of the remaining stages plus the tail 3 (c(q) ≥ (24/25)(q+r) − 1 ≥ (q−2)/2), so G(n) ≤ Σ c + 3. Exact recursion checked numerically ≤ 0.24 n² + 0.48 n log_5 n +
3n + 3 for all n ≤ 30000, and below Theorem B′ for all n ≥ 29.

## Claim 2 (new): full label sets in any dimension are not 3-feasible

Lemma (lifting). For k ≥ 3, L_k = F_5^k∖0 admits no feasible weakly nondegenerate (Φ: L_k → S^3,
γ_α ∈ F_5^k, α ∈ F_5^3∖0). Proof by induction on k, base k = 3 is Fact T3. Step k ≥ 4: suppose (Φ, γ)
exists; y_α = ⟨α, Φ⟩ + ⟨γ_α, ·⟩. For a hyperplane H ⊂ F_5^k let K_H = {α ∈ F_5^3 : Σ_j α_j Φ_j|_H is the
restriction of a linear functional}. K_H is a linear subspace; for α ∈ K_H every realizer y_{α} (and any
S-valued function congruent to Σ α_j Φ_j modulo linear functionals) restricted to H is an S-valued
linear functional on H, hence 0 (a nonzero functional on H∖0 takes the value 2). If K_H = 0, the
restriction (Φ|_H, γ_α|_H) is a strongly nondegenerate solution on H∖0 ≅ L_{k−1}, contradicting
induction. So dim K_H ≥ 1 for each of the (5^k − 1)/4 ≥ 156 hyperplanes, while F_5^3 has 31 lines: some
line ⟨α⟩ ⊆ K_{H1} ∩ K_{H2}, H1 ≠ H2. Then y_α and y_{2α} vanish on H1 ∪ H2; y_{2α} − 2y_α =
⟨γ_{2α} − 2γ_α, ·⟩ is linear and vanishes on H1 + H2 = F_5^k, so y_{2α} = 2y_α; both S-valued ⇒ y_α ≡ 0;
likewise for every λα. So [α] is degenerate, contradiction. ∎

Corollary (simplex blocks). For r ≥ 3 let X_r be 5^r − 1 columns in F_5^q, q = 5^r − 1 − r, whose
dependency code is the simplex code (one column for each nonzero label in F_5^r). By Lemma 2(B) and
the lifting lemma, R(X_r) contains no 3-dim subgroup and no witness, so no Y ⊆ X_r gains 3. Every 2-dim
subcode of the simplex code has support exactly 5^r − 5^{r−2} = (24/25)·5^r. A separate exhaustive
finite check shows that one dependency never gains two dimensions at p = 5 (per-column Φ, arbitrary
multiplicities). Hence each piece inside X_r costs ≥ (12/25)·5^r = (12/25)(q + r + 1) per realized
dimension, which equals SPARSE2's averaging bound at that (q, r).

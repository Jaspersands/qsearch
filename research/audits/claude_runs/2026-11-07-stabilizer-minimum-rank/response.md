# Verdict: Claims A and B hold. The result is real but narrow.

I could not break Claim A. I checked fields, functionals, complex spans, phases and normalization, and each step closes. Claim B follows. The result is an exact statement about exact stabilizer rank. It has essentially no operational or robust content, for the reason given in the "Cheapest falsifier" section below.

## Claim A: checked step by step

**A1. Stabilizer states have B-rational representatives.**
- Up to global phase, a stabilizer amplitude is 2^{-k/2}·i^{l(x)}·(−1)^{q(x)} on an affine support.
- √2 = ζ8 + ζ8⁻¹ lies in B, so every coordinate lies in B. Even unnormalized representatives would suffice.
- The complex span W does not depend on which phase representatives you choose. Global phases and arbitrary complex coefficients are therefore harmless. ✔

**A2. A B-rational separating functional exists.**
- W is the complex span of finitely many vectors in B^N, so W is defined over B.
- Row-reducing over B gives a basis of W's annihilator consisting of functionals with B coefficients.
- If V ⊄ W, some s_j lies outside W. Since W is the common kernel of that annihilator basis, some basis functional ℓ has ℓ(s_j) ≠ 0. ✔
- This step needs no subfield or Galois subtlety, because the spanning vectors themselves lie in B^N.

**A3. The resulting relation.**
- Since v ∈ W, we have ℓ(z) = 0.
- This gives ℓ(R)·θ⁰ + Σ_{j=0}^{K−1} ε0·ℓ(s_j)·θ^{j+1} = 0.
- ℓ(R) ∈ B because R has 0/1 coordinates. ε0 is rational. ℓ(s_j) ∈ B. So every coefficient lies in B.
- The exponents run over 0,…,K, which is K+1 powers. ✔

**A4. Degree argument.**
- x^p − 2 is Eisenstein at 2, so [Q(θ):Q] = p.
- [B:Q] = 4.
- [B(θ):Q] is divisible by both 4 and p and is at most 4p. Since gcd(4,p) = 1, it equals 4p, so [B(θ):B] = p.
- 1, θ, …, θ^K are therefore B-independent exactly when K+1 ≤ p, i.e. p > K. ✔
- Hence ℓ(s_j) = 0 for all j, which contradicts A2. ✔

**A5. Consequences.**
- The original states are independent: p0 is the only one supported on E, and the cell states have disjoint supports. So dim V = K.
- z ∈ V, so χ(v) ≤ K.
- Any stabilizer decomposition of any length spans a W ⊇ V, so it has at least K terms.
- A K-term decomposition therefore spans exactly V, and all its atoms lie in V. ✔

A small strengthening: A shows that every stabilizer decomposition's span contains V, not just the minimal ones. Only the minimal ones are forced to have their atoms inside V.

**Mechanism, to be clear about what does the work.** u alone has χ(u) ≤ m. For n ≥ 4, m < K, so u's rank-minimal decompositions need not lie in V. The θ-perturbation makes v "B-generic" inside V. This lifts the rank to K and pins every minimal decomposition to V. Any coefficient vector that is B-independent in the s_j basis would serve the same purpose; 2^{1/p} is one convenient choice.

## Claim B: checked

**Overlap set {0, r}.** Re-derived:
- Every vector in V has constant amplitude on E.
- Take a stabilizer state s in V with nonzero E-amplitude. Its support contains E. Its support is affine, and the affine span of E is the whole cube, so the support is the whole cube.
- So |amplitude| = 2^{−n/2} everywhere and the amplitudes are equal on E. This gives |⟨u,s⟩|² = m²·2^{−n}/m = r.
- Otherwise s vanishes on E and ⟨u,s⟩ = 0. ✔

**Perturbation bound.**
- The s_j are normalized and θ^{j+1} ≤ θ^K = 2^{K/p} < 2.
- So ‖z−R‖ ≤ 2K·ε0 = 2^{−2n}/4.
- Normalization step: ‖z/‖z‖ − R/‖R‖‖ ≤ ‖z−R‖/‖R‖ + |‖R‖−‖z‖|/‖R‖ ≤ 2‖z−R‖/‖R‖.
- Hence ‖v−u‖ ≤ 2^{−2n}/(2√m), which is far below √r = √m·2^{−n/2}. ✔

**Lower bound on any V-supported decomposition.**
- Write v = Σ c_k t_k with every t_k in V.
- Then 1 = Σ c_k⟨v,t_k⟩ ≤ (Σ|c_k|)·2√r.
- So (Σ|c|)² ≥ 1/(4r) = 2^n/(4(n+1)). ✔
- This holds for any decomposition with all atoms in V, of any length. A routes every rank-minimal decomposition there.

**Upper bound on extent.**
- Use the |x⟩ for x ∈ E plus the ε0θ^{j+1}s_j: m + K terms, all of them stabilizer states.
- ℓ1 ≤ (m + 2Kε0)/(√m − 2Kε0) ≤ 2√m, so the extent is at most 4(n+1). ✔

**When the bounds bite (finite control by hand).**
- The lower bound 1/(4r) exceeds 1 only for n ≥ 5.
- It exceeds the extent bound 4m only for n ≥ 12 (4096 > 16·13² = 2704; n = 11 fails, 2048 < 2304).
- Any small-n numerical check (n ≤ 11) would show no separation and would neither confirm nor refute the claim. The separation is purely asymptotic.

## Claim C: plausible but loosely stated

**Succinct description, not explicit coordinates.** There are 2^n coordinates, so "polynomial algebraic description" must mean a succinct description. Each z_x is a function of x computable in poly(n) time with exact B(θ) arithmetic. Each x lies in E or in exactly one cell, so z_x has at most two θ-terms.

**Exact Gram data.**
- ⟨p0, c_ij⟩ = 2^{−j/2}, since |C_ij| = 2^{n−j}.
- ⟨R, p0⟩ = m·2^{−n/2}.
- ⟨R, c_ij⟩ = 0.
- So ‖z‖² ∈ B(θ)∩ℝ is exactly computable from a K×K Gram matrix with poly(n)-bit entries.
- The square root at most doubles the degree, to at most 8p.
- Proof obligation: state the cell phase convention (all + is fine) and the bit-height bound explicitly. ε0 contributes O(n + log K) bits. The θ-powers contribute O(K) in exponents, not bits. Nothing here endangers A or B.

## Cheapest falsifier of the significance: the gap is an exact-rank artifact

‖v − u‖ ≤ 2^{−2n}/(2√m). So u, with an m-term computational decomposition and ℓ1 = √m, is a 2^{−2n}-approximation to v.

**Approximate rank collapses.** At any approximation error δ ≥ 2^{−2n}/(2√m), v has a stabilizer decomposition of rank at most m = n+1 with ℓ1 = √m. This is not V-constrained. The rank-K pinning in A exists only at error exactly 0. Exact rank is discontinuous, and A exploits exactly that discontinuity.

**No distinguishable state.** At any precision achievable with poly(n) bits, the "ill-conditioned" state cannot be told apart from a well-conditioned one. Preparing u already prepares v to infidelity at most about 2^{−4n}.

**Preparation cost, fully charged.**
- Exact preparation of v is impossible with a finite gate set: θ is irrational, and the normalization is algebraic of degree up to 8p.
- Approximate preparation to error δ via the outside LCU:
  - Coefficient-state loading at polylog(1/δ) precision.
  - Atoms: computational basis states, H^{⊗n}, and the cell states, which are X/H on affine coordinates, all Clifford.
  - Postselection success probability ‖z‖²/ℓ1² ≥ 1/(4m), so O(√m) amplitude-amplification rounds.
- The ε0 terms are below poly precision unless δ < 2^{−2n}. Then the LCU over u alone suffices.

**What is established, as an exact theorem.** For n ≥ 12 there is an explicit, succinctly described state v_n with:
- exact stabilizer rank K = C(n,2)+1;
- every rank-K decomposition has ℓ1² ≥ 2^n/(4(n+1));
- stabilizer extent ξ(v_n) ≤ 4(n+1).

So the minimizers of rank and of extent can be exponentially separated in ℓ1 cost, even when rank is polynomial. That is a correct counterexample to any claim of the form "every rank-minimal decomposition has ℓ1 within poly of √ξ."

**What is not established:**
- Anything about approximate rank, or about decompositions robust to 2^{−poly(n)} error. The construction is designed so that this fails.
- Hardness of computing or optimizing extent, of learning, or of simulation.
- That rank-minimizing algorithms are "inherently" expensive in any operational or robust sense. A δ-tolerant rank minimizer returns u's decomposition.
- Gram-matrix ill-conditioning of the minimal atom set. Only ℓ1 blow-up and cancellation are proved; the condition number of the K atoms in V would need a separate argument.

**Novelty.** Unknown; I cannot verify the literature here. Exact stabilizer rank, approximate stabilizer rank and stabilizer extent are standard notions, and the non-robustness of exact rank is a widely recognized theme. Whether this explicit ℓ1 separation for rank minimizers appears in prior work is something you should check against the relevant papers yourself. Claim no novelty until you have.

## Proof obligations to write down explicitly

1. Define C_ij precisely: x_1..x_{i−1} = 0, x_i = 1, x_{i+1..j−1} = 0, x_j = 1, the rest free. Show these cells are affine and partition {weight ≥ 2}.
2. Prove dim V = K by the support argument.
3. Prove the stabilizer amplitude normal form and that B-representatives exist.
4. Prove W is defined over B and the separating functional exists (A2).
5. Prove [B(θ):B] = p via gcd(4,p) = 1, and that p > K is needed for K+1 powers.
6. Prove the {0, r} overlap lemma, including the argument that full support forces uniform magnitude.
7. Prove the normalization inequality and the n-range where the bounds are nontrivial (n ≥ 5 for >1, n ≥ 12 for the separation).
8. State explicitly that the theorem concerns exact decompositions. Add the remark that at δ ≥ 2^{−2n} it fails, i.e. approximate rank is at most n+1.

## Falsifiers to keep in view

- A stabilizer state in V vanishing on E but not lying in the span of cell states would not break B, since its overlap with u is still 0. So this is not a falsifier. A falsifier would be an error in the "constant on E" property of V. Check this directly: it holds because p0 is constant and the cell states vanish on E.
- A cell definition that is not affine for some (i, j) would break the stabilizer status of the s_j, and with it A1 and the extent bound.
- K ≥ p would break A4. Bertrand's postulate gives p ≤ 2K+1, which is fine.

**Bottom line.** A and B are correct exact mathematics, and the separation (rank-minimal ℓ1² ≥ 2^n/(4(n+1)) versus ξ ≤ 4(n+1)) holds for n ≥ 12. It rules out universally cheap exact rank-minimizing decompositions. It is fragile by construction: it disappears at error 2^{−2n}. It therefore says nothing about robust or approximate decompositions, polynomial optimized extent, learning, or hardness.
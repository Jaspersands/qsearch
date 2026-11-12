# Wave-positive-source-frame: Gram lower bound under the separated nonnegative-weight promise

## 0. Decisive result

**The promise fails, including at inverse-polynomial strength.**

The promise is: nonnegative rational weights, distinct sites, and pairwise torus distance at least a fixed R0. For every fixed R0, I give an explicit family of sources (Theorem 3) satisfying it with:

- integer weights w_j ≥ 1,
- m = O(n²) sites,
- total bit length B = O(n³),

and an exponentially small ratio:

  Z / (Σ_j w_j² · Z0) ≤ C_{R0} / L = C_{R0} · 2^(−n).

For R0 ≤ 2 the constants are fully explicit: spacing d = 2, M = 26, and the ratio is at most 651 / 2^n for n ≥ 10.

Consequences:

- **Uniform constant c > 0:** false.
- **c ≥ 1/poly(n, m, B):** false.
- **Contract attacks 1 and 2:** the LCU success probability and the matched-mixture rejection success are both exponentially small on this family.
- **Ring-supported resonant preparation:** the field mass in the neighbourhood |1−λ| ≤ δ/2 of the resonant curve is an exponentially small fraction. So any ring-supported preparation of this state has error near 1.

The mechanism is Bragg cancellation plus apodization. A periodic array has its Fourier transform F concentrated at reciprocal-lattice (Bragg) points. Those points provably never lie on the lattice curve λ = 1 (Lemma 2). A nonnegative binomial-type taper then suppresses the sidelobes of F on the curve geometrically in the taper order.

**What this is not.** It is not a hardness statement. It only shows that this source promise does not make the Gram/LCU interface work.

**Stronger promise.** I give one checkable geometric promise (separation growing like m², plus m ≲ √L). It has a proved Gershgorin lower bound conditional on one stated, unproved, uniform-in-L Green-function decay lemma. I leave that lemma open.

## 1. Setup and exact identities (proved)

**Notation.**
- N = L², θ_k = 2πk/L, λ(θ) = 4 − 2cos θx − 2cos θy, a = 1 − λ + i/L, η = 1/L.
- F(θ) = Σ_j w_j e^{−iθ·x_j}.
- With the unitary DFT:
  - Z0 = ‖G‖² = (1/N) Σ_k |a(k)|^(−2)
  - Z = ‖u‖² = (1/N) Σ_k |F(θ_k)|² / |a(k)|²
  - Σ_j |w_j|² = (1/N) Σ_k |F(θ_k)|² (Parseval)

**(I1) Energy / optical identity.**
1. Since I − K is Hermitian, Im⟨u, Au⟩ = η‖u‖².
2. Since Au = f, this gives ‖u‖² = L · Im⟨u, f⟩.
3. Equivalently, (A*A)^(−1) = −(1/η) Im(A^(−1)), where Im X := (X − X*)/(2i).

Hence the Gram matrix has the form

  Γ_jk = ⟨T_{x_j}G, T_{x_k}G⟩ = −L · Im G(x_j − x_k), with Γ_jj = Z0 = −L · Im G(0).

So the Gram form is exactly L times the imaginary part of the lattice Green function at the source differences. In particular, Z is computable from m² Green-function values. This is a classical normalizer reduction, not a poly(n) algorithm.

**(I2) Aside (marked, verify the sign convention).** The y-sum can be done in closed form via the 1-D periodic resolvent:

  Σ_{ky} e^{iθy·y} / (2cos θy − b) = L (z^y + z^(L−y)) / ((z − z^(−1))(1 − z^L)), where z + 1/z = b and |z| < 1.

This makes G(y) evaluable in O(L · poly(n, bits)) operations. That is sublinear in L² but not poly(n).

**Theorem 1 (Z0 ≥ cL).** For L ≥ 12:

  Z0 ≥ L / (4(4π² + 1)).

*Proof.*
1. For an integer kx with |kx| ≤ L/6, set t = 2cos θx − 1 ∈ [0, 1].
2. Let g(ky) = 2 − 2cos θy. Then g(0) = 0 and g(L/2) = 4, and successive steps satisfy |Δg| ≤ 4π/L.
3. So some ky ∈ [0, L/2] has |1 − λ| = |t − g(ky)| ≤ 2π/L.
4. This yields at least L/3 − 1 ≥ L/4 distinct k with |a|² ≤ (4π² + 1)/L².
5. Therefore Z0 ≥ (1/L²)(L/4) · L²/(4π² + 1). ∎

Also, trivially, Z0 ≤ L², because |a| ≥ 1/L.

## 2. Bragg points avoid the lattice resonant curve (proved)

**Lemma 2.** Let d = 2^s ≥ 2 and p, q ∈ Z. Then

  λ(2πp/d, 2πq/d) ≠ 1, and δ_d := min_{p,q} |1 − λ_pq| ≥ 7^(−(d/4 − 1)) for d ≥ 4, with δ_2 = 1.

*Proof.*
1. Let ζ = e^{2πi/d} and S = ζ^p + ζ^(−p) + ζ^q + ζ^(−q). Then 1 − λ_pq = −(3 − S) =: −α, with α ∈ Z[ζ].
2. In Z[ζ] (2-power cyclotomic), (1 − ζ) is the unique prime above 2, and Z[ζ]/(1 − ζ) ≅ F₂.
3. Modulo (1 − ζ) we have ζ ≡ 1, so S ≡ 4 ≡ 0 and α ≡ 3 ≡ 1. Hence α ≠ 0.
4. α is a real algebraic integer in Q(ζ)⁺, which has degree d/4 for d ≥ 4.
5. Every conjugate satisfies |σ(α)| ≤ 3 + 4 = 7, and |N(α)| ≥ 1.
6. So |α| ≥ 7^(−(d/4 − 1)).
7. For d = 2 the values are λ ∈ {0, 4, 4, 8}, so |1 − λ| ∈ {1, 3, 3, 7}. ∎

## 3. Counterfamily (exact, proved)

**Parameters.**
- Fix R0. Let d = 2^⌈log₂ max(R0, 2)⌉ and δ = δ_d.
- s := (2/π) · min(dδ/16, π/2), M := ⌈2/s⌉, r := 2n.
- Let b_j ≥ 1 (j = 0, …, J−1, with J = r(M−1) + 1) be the coefficients of (1 + z + … + z^(M−1))^r.

**Sources.**
- Sites x = d·(j1, j2) with 0 ≤ j1, j2 < J. Weights w = b_{j1} · b_{j2}.
- Requirements: dJ ≤ L and L ≥ 12.
- Since d | L, the sites are distinct and pairwise torus distance is ≥ d ≥ R0.
- m = J² = O(n²). Each weight is ≤ M^(2r), so B = O(m · n log M) = O(n³).

**Theorem 3.**

  Z / (Σ w² · Z0) ≤ 16(4π² + 1) / (δ² L) + 4n²M² / L⁴.

*Proof.*
1. **Factorization.** F(θ) = f1(θx) · f1(θy), where f1(φ) = D(φ)^r and |D(φ)| = |sin(Mdφ/2) / sin(dφ/2)|.
2. **Split k-space.** Let S_near = {k : |1 − λ| ≤ δ/2}.
3. **Far region.** Here |a| ≥ δ/2, so its contribution is ≤ (4/δ²)(1/N) Σ |F|² = (4/δ²) Σ w². Dividing by Σw² · Z0 and using Theorem 1 gives the first term.
4. **Near region: distance from Bragg points.**
   - |∇_θ λ| ≤ 2√2, and |1 − λ| ≥ δ at every Bragg point (2π/d)Z² by Lemma 2.
   - So θ ∈ S_near has Euclidean distance ≥ δ/(4√2) from the Bragg set.
   - Hence some coordinate, say θx, is at distance ≥ δ/8 from (2π/d)Z.
   - Therefore dist(dθx/2, πZ) ≥ dδ/16, which gives |sin(dθx/2)| ≥ s.
5. **Near region: size of F.** From step 4, |f1(θx)| ≤ s^(−r). Also |f1(θy)| ≤ f1(0) = M^r. So |F|² ≤ M^(2r) s^(−2r) on S_near.
6. **Near-region contribution.** It is ≤ max_{S_near} |F|² · Z0.
7. **Lower bound on Σw².** By Cauchy–Schwarz, Σ w² = (Σ_j b_j²)² ≥ (M^(2r)/J)².
8. **Near ratio.** Dividing, the near contribution over Σw² · Z0 is ≤ J² (Ms)^(−2r) ≤ (rM)² 4^(−r) = 4n²M²/L⁴, using Ms ≥ 2 and r = 2n. ∎

**Explicit case R0 ≤ 2.** Here d = 2, δ = 1, s = 1/(4π), M = 26, J = 50n + 1, and n ≥ 10. The ratio is at most 650/L + 2704n²/L⁴ ≤ 651/2^n, since 16(4π² + 1) ≈ 647.6.

**Corollaries (proved).**
- **(a) LCU success.** Z/(‖w‖₁² Z0) ≤ Z/(Σw² · Z0) = O(2^(−n)).
- **(b) Mixture success.** It is smaller still, by a factor of m.
- **(c) Near-shell mass fraction.**
  - The norm bound is ‖u‖² ≥ Σw²/50, since |a|² ≤ 49 + L^(−2).
  - Combining this with the near-region bound from Theorem 3 and Z0 ≤ L², the near-shell mass fraction is ≤ 50(rM)² 4^(−r) · L² = 200n²M²/L².
  - So a preparation supported on the band |1 − λ| ≤ δ/2 has overlap error near 1. The field is almost entirely off-shell (near field).

**Separate weaker remark: full periodic array.**
- Take all w = 1, d = 2, m = L²/4.
- Exact formula: Z/(mZ0) = (1/(4Z0)) Σ_{p,q∈{0,1}} 1/((1 − λ_pq)² + L^(−2)) = Θ(1/L).
- This kills the uniform constant c, but only as Θ(m^(−1/2)). It is therefore **not** an inverse-polynomial falsifier.
- The taper in Theorem 3 is what converts the loss to exponential at polynomial m.

## 4. One stronger geometric promise (conditional; left open)

**Proved conditional statement (Gershgorin plus I1).** Define

  ρ_L(R) := max_{|y|_torus ≥ R} |Im G_L(y)| / |Im G_L(0)|.

If the sites are R-separated and (m − 1) ρ_L(R) ≤ 1/2, then for **arbitrary complex** weights

  Z ≥ ½ Σ_j |w_j|² · Z0.

**Missing lemma (unproved here).** There exists a computable K such that ρ_L(R) ≤ K (R^(−1/2) + L^(−1/2)) uniformly in L.

- *Heuristic support.* The infinite-lattice limiting-absorption value Im G is the Fourier transform of a smooth density on the curve cos θx + cos θy = 3/2. That curve is strictly convex: the Hessian is diag(−cos θx, −cos θy) with both cosines ≥ 1/2. So standard stationary phase gives |y|^(−1/2) decay.
- *Not supplied.* Uniformity in η = 1/L on the torus (periodization images, energy smoothing near the van Hove singularity) is not proved. The naive Combes–Thomas bound has a 1/η prefactor and fails.

**Promise (checkable in O(m² n) time).** Pairwise separation R ≥ (4Km)², and m ≤ √L / (4K). Under the missing lemma this gives c = 1/2.

**Consistency.** This promise is not contradicted by Theorem 3, because that family has fixed spacing while m grows.

## 5. Proof obligations and falsifiers

**Open obligation.** The uniform-in-L decay bound for Im G_L stated in §4.

**Falsifiers of the conditional promise.**
- A sequence (L, y) with |y| ≥ R_L and |Im G_L(y)|/|Im G_L(0)| ≫ |y|^(−1/2) + L^(−1/2).
- Natural first tests are arithmetic torus directions, for example y = (L/2, 0), (L/2, L/2), (L/4, 0).
- Finite scans can only falsify; they cannot prove the bound.

**Even if the promise held**, an algorithm would still need to pay for:
- the single-source sampler/evaluator, or resonant preparation with all off-shell tails,
- finite-bit trigonometry,
- coherent uncompute, readout, and the clock.

The Gram bound only fixes the source-register success probability.

**Status of each claim.**
- Proved: Theorems 1 and 3, Lemma 2, identity I1, and the Gershgorin statement.
- Conditional: §4.
- Not claimed: hardness, a speedup, or a full-rank conclusion from finite data.
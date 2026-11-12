# Audit of the explicit majorants through Z(v) in SURFACE_RECONSTRUCTION_PRECISION_LEDGER

*Advisory review. No tools, code, or new sources were used. The only evidence is the supplied ledger, the merkl-log-atlas review, and the primary excerpts.*

## 0. Verdict

The scoped numerical majorants survive an independent rederivation. These include:

- the Whitney counts and sphere areas,
- N ≤ 2^42(r+1)d(d+L),
- c1 = d² and log M ≤ 9d,
- the 2^16·N·d² Merkl constant at both radii,
- L0 and Λ,
- the 1/800 differential bound,
- Z(v).

Every constant has large slack. No hidden asymptotic C remains, provided three explicit assumptions are stated (§5).

There is one concrete defect, and it concerns scope rather than arithmetic. As written, Z(v) is asserted for every positive integer v. The proof does not cover v that is a branch value, and the existence sentence for v ≤ v0 omits this exclusion. The repair is free: the count behind v0 = g³ + r + 1 already pays for it.

## 1. Cheapest decisive attack: the domain of Z(v)

The ledger states: "For a positive integer v define Z(v) … bounds h_Z(b) ≤ Z(v) … for π(b) = v." It later says only "Some v ≤ v0 has no Weierstrass point above it."

**Failure mode.** Suppose v ∈ B and b is a ramification point above v. Then:

- The section π*dt vanishes at b. So b lies in the horizontal support of K_{Y'} = div(π*dt).
- The hypothesis of source Proposition 4.2.4 ("the image of P′ is not contained in the support of K_{Y′}") fails.
- On the archimedean side, the differential bound degenerates. Its lower bound |dt/du| ≥ δ_ch(v,B)/800 becomes 0, and −log‖π*dt‖_Ar(b) = +∞ as written.

The argument therefore proves nothing at such b. I do not claim h(b) > Z(v) there. I claim only that the stated domain is unproved.

**Repair (safe, explicit).** Define Z(v) only for positive integers v ∉ B. Replace the existence sentence by:

> Some integer 1 ≤ v ≤ v0 satisfies v ∉ B and has no Weierstrass point above it.

**Proof of the repaired sentence.**

- A curve of genus g ≥ 2 has at most (g−1)g(g+1) = g³ − g Weierstrass points. Genus 1 has none, which is consistent with the source's g ≥ 1 statement.
- These points have at most g³ − g images in P¹.
- B contributes at most r values.
- So at most g³ − g + r ≤ g³ + r of the v0 = g³ + r + 1 integers are excluded.

Since Z is increasing in v, Z(v0) still dominates Z(v) for the chosen v. The monotonicity remark in the ledger is unaffected.

**Additional requirement.** v must be finite, which holds for integers. Then (Q, ∞)_fin = 0, so the horizontal part −2π*(∞) of div(π*dt) contributes nothing. This is the real reason v is taken to be an integer, and it should be stated.

## 2. Whitney net, sphere areas, dyadic count, N

I use the review's construction: ε = 1/100, ρ = a/100, a = min(1/4, θ(·,B)) with angular θ, and θ0 = (δ/100)(3/4)^d.

**Disjointness of the balls B_θ(s, ρ(s)/16).**

- An intersection gives θ(s,t) < (ρ_s + ρ_t)/16.
- Since a is 1-Lipschitz, |ρ_s − ρ_t| ≤ ε·θ(s,t) < (ε/16)(ρ_s + ρ_t). Hence the ratio of the two radii is below 1.002.
- Then θ(s,t) < (3/16)·min(ρ_s, ρ_t) < (1/4)·min(ρ_s, ρ_t).
- This contradicts the separation rule. ✔

**Ball area lower bound.** The cap radius is α = a/1600 ≥ t/1600. The cap area is 4π·sin²(α/2) ≥ 4α²/π > α² ≥ t²/1600². ✔

**Layer containment.** In an uncapped layer, a < 1/4, so a = θ(s,B) < 2t. Each ball lies within 2t + 2t/1600 < 3t of some b ∈ B. Also t < 1/4, so 3t < 3/4. Each cap has area 2π(1 − cos 3t) ≤ 9πt² < 28.3t² ≤ 36t². Overlapping caps only reduce the union's area, so no cluster hypothesis is needed. ✔

**Count per uncapped layer.** At most 36·1600²·r = 92,160,000·r < 2^27·r = 134,217,728·r. ✔

**Capped layer.** Here α = 1/6400. The count is at most 4π/(4α²/π) = π²·6400² ≈ 4.04·10^8 < 2^29 ≈ 5.37·10^8. ✔

**Number of layers.** Take t = 2^(−k)/4, so uncapped layers number ⌈log₂(1/(4θ0))⌉. With natural-log L and log₂(100) ≈ 6.644:

- log₂(1/(4θ0)) = (L − 1)/ln 2 + 6.644 − 2 + 0.415d.
- Adding one for rounding and one for the capped layer gives at most 1.443L + 0.415d + 6.2 < 2L + d + 10. ✔
- This uses L ≥ 1, which holds because chordal distance is ≤ 1.

**Total chart count.**

- Since d ≥ 2 and L ≥ 1, we have d + L ≥ 3, so 2L + d + 10 < 6(d+L).
- Then |S| < 6·2^27·r·(d+L) + 2^29.
- N ≤ rd + d·|S| < 2^30·r·d(d+L) + 2^29·d(d+L)/3 + r·d(d+L)/3 < 2^31(r+1)d(d+L).
- So the ledger's 2^42 carries a factor of about 2^11 in slack. ✔

**Coverage.** The coverage argument (maximality on E, plus branch inner disks for θ < θ0, using |w| < r1^(d/e) ≤ r1) is correct as reviewed. Boundary points of E belong to E. ✔

## 3. c1, M, and the Merkl constant at 7/8 and 3/4

**Normalisation of c1.** The inner product is (i/2)∫ω∧η̄ and i·dz∧dz̄ = 2·dx dy. So an orthonormal f·dz satisfies ∫|f|² dx dy ≤ 1 on any embedded chart. Then μ_Ar = i·F·dz∧dz̄ with F = (2g)^(−1)·Σ|f_ν|².

**Density bounds.**

- The mean-value inequality on a disk of radius R − 1 gives F ≤ 1/(2π(R−1)²) on the full unit disk.
- Whitney charts (R = 3/2): F ≤ 2/π.
- Branch charts (R = 2^(1/e), so R − 1 ≥ (ln 2)/e
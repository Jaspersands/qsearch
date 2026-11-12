# Wave-sparse-deflation: exact division of a sparse Laurent source by P = −3 + X + X⁻¹ + Y + Y⁻¹

## 0. Verdict

Labels used throughout:

- **[P]** proved here.
- **[S]** quoted from the supplied AKS 2006 excerpt and not re-proved; its internal proof depends on Cor. 1.2 and Lemma 2.3, which were not supplied.
- **[A]** an assumption the parent must still check.
- **[X]** not proved.

Findings:

1. **Division test and quotient.**
   - There is a deterministic division test with an explicit sparse quotient. Its bit cost is polynomial in m, B and E (E = exponent bit length).
   - The quotient support satisfies |supp H| ≤ (m−1)²(Δ−1)², with Δ = 288000·B.
   - This rests on AKS Cor. 2.5 [S] plus two unverified details [A]: the definition of h₁ and the log base.
2. **The output-size claim survives the counterexample attempt,** but only through the height parameter. The bound is poly(m, B), not poly(m).
3. **Unexpected consequence, a falsifier.**
   - For any torus source f = (I−K)h with s = |supp h|, I prove TV(P_u, |h|²/‖h‖²) ≤ 2√(3s)·L^{−1/5}.
   - Combined with a full-grid fallback when L is small, the forced subclass therefore has a **classical poly(m, B, n, 1/ε) same-output sampler**.
   - So this subclass is closed classically. It is not a quantum-advantage candidate.
   - This is an extra lemma, not something division alone gives (see §8).

## 1. Counterexample attempt on the output-size claim (done first)

The claim under test: if F has m terms and P | F, then H = F/P has poly(m, B) terms, even when exponents are around 2ⁿ.

Attempts:

- **Geometric-series analogue.** (Xᴺ−1)/(X−1) has N terms. That divisor is a binomial/cyclotomic factor, which Cor. 2.5 excludes. P is not of that form (§2).
- **Single-row H.** If H ∈ Q(i)[X^±], then F contains Y·H and Y⁻¹·H as separate rows. So H has at most m terms.
- **Top-down recursion.** Take h₀ = 1 and h_{j+1} = −(X+X⁻¹−3)h_j − h_{j−1}. This kills the interior rows of F, but the top rows of F become h_M and h_{M+1}. Those are dense (2M+1 terms) with exponentially growing coefficients, so this F is not sparse.

Outcome:

- No counterexample was found.
- The proved bound depends on the height through Δ ∝ B. I did not construct an example showing |supp H| ≫ m, so I make no claim either way about poly(m) alone.
- **[P] Necessity of the hypothesis.** Without irreducibility and the non-binomial condition, the claim is false (X−1 dividing Xᴺ−1).

## 2. Algebraic facts about P [P]

Clearing monomials gives p := XY·P = x²y + xy² − 3xy + x + y ∈ Z[x,y].

Basic properties:

- Total degree d = 3, deg_x = deg_y = 2.
- p(x,y) = p(y,x).
- x ∤ p, since p(0,y) = y. Likewise y ∤ p.

**Absolute irreducibility.**

1. The Newton polygon is the diamond with vertices (1,0), (2,1), (1,2), (0,1), and (1,1) is interior. Its edges are the primitive vectors ±(1,1) and ±(1,−1).
2. Ostrowski: N(gh) = N(g) + N(h).
3. Lattice edge lengths add under Minkowski sums, and each edge here has length 1. So each edge direction goes wholly to one summand.
4. A summand's edge vectors must sum to zero. The only nontrivial split is therefore a segment along (1,1) plus a segment along (1,−1).
5. If a summand is a point, that factor is c·xᵃyᵇ. This forces a = b = 0 because x, y ∤ p, so the factor is a unit.
6. A primitive segment has no interior lattice points. So g = x^a y^b(α + βxy) and h = x^c y^d(γy + δx), with all four coefficients nonzero.
7. Then gh has support at relative exponents (0,1), (1,0), (1,2), (2,1), and nothing at (1,1). But p has coefficient −3 at xy. Contradiction.

Hence p is irreducible over C, and in particular over Q(i).

**Not in the excluded families of Cor. 2.5.**

- Suppose p = ∏(x^α − ω_i y^β) or ∏(x^α y^β − ω_i), with nonconstant factors.
- Irreducibility forces exactly one factor, which has at most 2 terms. But p has 5 terms.
- So p is not in either family, and in particular not cyclotomic.

**Monomial cancellation.** p is prime in the UFD K[x,y] and not associate to x or y. Hence p | xᵃyᵇg ⇔ p | g.

## 3. Hypotheses of Cor. 2.5 with K = Q(i), [K:Q] = 2

| Hypothesis | Status |
|---|---|
| f, r, q ∈ K[x,y] | [P] |
| p irreducible in K[x,y], deg_y p ≥ 1, p ≠ y | [P] |
| Not in the excluded product forms | [P] |
| d = deg p | Use 3. If "deg" means max partial degree it is 2; the threshold increases with d, so 3 is safe. |
| Threshold 56·2·3·log³(96)·h₁(f) = 336·log³(96)·h₁(f) | [A] log base not shown. Using log₂ (6.585³·336 ≈ 95,962 ≤ 96,000) is safe for natural log or log₂. |
| A computable c ≥ h₁(f) | [A]: definition of h₁ not in excerpt (see below). |

**Assumption H (definition of h₁).**

- H says: h₁ is the projective Weil height of the coefficient vector, with the ℓ₁ norm at archimedean places and the max norm at finite places.
- Under H, write the coefficients as Gaussian integers using a common denominator D_den ≤ 2^B. Then:
  - h₁(f) ≤ ln‖D_den f‖₁ ≤ ln m + (B + ½)·ln 2 ≤ 3B.
  - The same bound holds for every sub-sum and every monomial shift of f.
- Set c := 3B and Δ := 96000·c = 288000·B.
- The source asserts that c is poly-time computable via [Len99b, Prop 3.6]; that is [S], not verified.

## 4. Algorithm (deterministic)

**Input.** F = Σⱼ wⱼ X^{αⱼ} Y^{βⱼ}, with distinct integer exponents of at most E bits and wⱼ ∈ Q(i)*.

**Step 0 (shift).**

- Set f := X^{−α_min} Y^{−β_min} F. This is a polynomial not divisible by x or y.
- Scale by D_den, so coefficients become Gaussian integers with |coef| ≤ G := √2·2^B.

**Step 1 (gap split, as in AKS §3.2).**

- Sort the terms by β. Cut wherever consecutive β differ by at least Δ. This gives y-blocks with tⱼ terms each.
- Inside each y-block, sort by α and cut at gaps of at least Δ.
- Normalise each final piece by a monomial so that it is a polynomial g_i with minimum exponents 0.
- Degree bounds:
  - deg_x g_i ≤ (s_i − 1)(Δ − 1), where s_i is the number of terms in the piece.
  - deg_y g_i ≤ (t_j − 1)(Δ − 1).
- There are at most m pieces.

**Step 2 (dense division of each piece).**

- If deg_x g_i < 2 or deg_y g_i < 2, reject.
- Otherwise, on the box [0, deg_x g_i − 2] × [0, deg_y g_i − 2], compute q in decreasing lexicographic order (x first):

  q_{a,b} = g_{a+2,b+1} − q_{a+1,b−1} + 3·q_{a+1,b} − q_{a+1,b+1} − q_{a+2,b}

  with q := 0 outside the box.
- Verify that p·q_i = g_i exactly on the full box. If verification fails, reject.

**Step 3 (assembly).** If every piece verifies:

H = D_den⁻¹ · Σ_i X^{α_min + γ_i + 1} · Y^{β_min + δ_i + 1} · q_i.

## 5. Correctness [P, given S and A]

**(a) Laurent vs. polynomial divisibility.**

- If F = PH, write XY·x^{−α_min}... more precisely, f = p·g with g = X^{−α_min−1} Y^{−β_min−1} H.
- Write g = x^{−s} y^{−t} g₀ with x, y ∤ g₀. Then x^s y^t f = p g₀.
- If s > 0, then x divides p·g₀, which is impossible since x ∤ p and x ∤ g₀. So s ≤ 0, likewise t ≤ 0, and g is a polynomial.
- So P | F ⇔ p | f.

**(b) Splitting.**

- Write f = r₀ + y^{b₁} q with b₁ − deg_y r₀ ≥ Δ ≥ threshold. Cor. 2.5 gives p | f ⇔ p | r₀ and p | q.
- Induct on the number of y-blocks. The bound c is valid for every sub-sum under H.
- For the x-cuts, apply the same corollary to swapped variables. This is valid because p(x,y) = p(y,x).
- Remove monomials using §2.
- Result: p | f ⇔ p | g_i for all i.

**(c) The quotient box.** If g = pq:

- deg_x q = deg_x g − 2 and deg_y q = deg_y g − 2 (leading parts multiply in a domain).
- The lowest-x part of g is y·(lowest-x part of q), so min_x q = 0. Similarly min_y q = 0.

**(d) The recurrence.**

- The lex-leading monomial of p is x²y with coefficient 1.
- The coefficient equation at monomial x^{a+2}y^{b+1} involves q_{a,b} with coefficient 1, plus only lex-larger entries of q.
- So the system is unit-triangular, the solution is unique, and verification decides divisibility.

**(e) Assembly.**

- F = X^{α_min} Y^{β_min} Σ x^{γ_i} y^{δ_i} p q_i = P·H.
- Each q_i lies strictly inside the bounding box of its piece (after the +1 shift).
- Piece boxes are pairwise disjoint: different y-blocks have disjoint y-ranges, and same-block pieces have disjoint x-ranges.
- So the q_i supports never collide.

## 6. Finite inequalities [P, with Δ from A]

**Support of H.**

|supp H| ≤ Σ_i (s_i − 1)(t_j − 1)(Δ − 1)² ≤ (m−1)²(Δ−1)² < 8.3·10¹⁰ · m²B².

**Coefficient size.**

- Let K_j be the maximum |q| over the top j+1 x-levels. Then K_j ≤ G + 6·K_{j−1}.
- Hence |q| ≤ G·6^{deg_x g − 1}.
- Numerator bits of H are at most B + 1 + 2.585·(m−1)(Δ−1) ≤ B + 1 + 744,480·m·B, over a common denominator D_den ≤ 2^B.

**Exponents.** Exponents of H fit in E + 2 bits. Nothing in the procedure scales with 2ⁿ.

**Bit operations.**

- The boxes have at most Σ s_i t_j Δ² ≤ m²Δ² cells in total.
- Each cell costs at most about 12 additions or scalings on numbers of at most b_max = O(B + mΔ) bits.
- Total: O(m²Δ²·(B + mΔ) + m·E·log m) = O(m³B³ + mE log m) with an explicit, very large constant (about 2·10¹⁶).
- This is deterministic.

**Multiplicity.** Not needed. One division suffices for the field identity below. Repeating the division on H would compound its size and is not costed here.

## 7. Torus interface and the exact subclass closed

Ordinary division is never replaced by division modulo (X^L − 1, Y^L − 1). The torus enters only through how sources are lifted.

**Soundness [P].**

- Reduction Q(i)[Z²] → Q(i)[(Z/L)²] is a ring homomorphism mapping P to I − K.
- So if some lift F̃ satisfies F̃ = P·H̃, then f = (I−K)h on the torus with h := H̃ mod L, h ≠ 0, and |supp h| ≤ |supp H̃|.

**The canonical lift can fail [P].**

- Take f = (I−K)δ₀. In the [0,L)² lift its terms sit at X^{L−1} and Y^{L−1}.
- The gap split then isolates the piece −3 + X + Y, whose degree is too small to be divisible by p. So the canonical lift is rejected.

**Completeness under a promise [P].**

- Promise S: there exists h with |supp h| ≤ S and (I−K)h = f.
- If h avoids torus columns c and c+1 and rows c′ and c′+1, then P·(h lifted into window [c+1, c+L] × [c′+1, c′+L]) is supported in that window. So it equals the window lift of f, because reduction is injective on the window.
- Each occupied column eliminates at most 2 choices of c. So among any 2S+1 values of c, at least one works; likewise for c′.
- Trying all (2S+1)² windows is deterministic and complete when L ≥ 2S+2.
- The quotient returned equals the lift of h (Laurent quotients are unique).

**The subclass closed, exactly.** Torus inputs with f = (I−K)h and |supp h| ≤ S (S polynomial and given). For these:

u = A⁻¹(A − iη)h = h − iη·A⁻¹h.

Here h can be any solution; uniqueness is not needed because A is invertible.

## 8. Why exact division alone does not pay, and the extra lemma that does on this subclass

Division alone only rewrites u. The remainder iη·A⁻¹h is again a sparse-source Helmholtz field, which is the original problem. The following separate lemma is what makes it negligible.

**Lemma [P].** Let Z₀ = ‖A⁻¹δ₀‖² = L⁻² Σ_k |a(k)|⁻². Then η²Z₀ ≤ 3·L^{−2/5}.

Proof.

1. Write N(δ) = #{k : |1 − λ(k)| < δ}. Terms with |1−λ| ≥ δ contribute at most η²/δ² to the average, and every term is at most 1. So:

   η²Z₀ ≤ η²/δ² + N(δ)/L².

2. Fix k_x. The condition becomes cos θ_y ∈ (c − δ/2, c + δ/2), an interval of length δ.

3. The integrand 1/√(1−x²) is convex and symmetric, so an interval of length t is worst at an endpoint. Its preimage in [0, π] has measure at most arccos(1−t) ≤ (π/√2)·√t. The last step holds because φ/sin(φ/2) is increasing, with maximum π at φ = π.

4. Counting the two mirror arcs in [0, 2π), the number of k_y is at most L·√(δ/2) + 2. Summing over k_x:

   N(δ) ≤ L²·√(δ/2) + 2L.

5. Take δ = L^{−4/5} and use L ≥ 4:

   η²Z₀ ≤ (1 + 2^{−1/2})·L^{−2/5} + 2·L⁻¹ ≤ 3·L^{−2/5}.

**Corollary [P].**

- By the triangle inequality, ‖A⁻¹h‖ = ‖Σ_x h(x)·T_x G‖ ≤ ‖h‖₁·√Z₀.
- Write s = |supp h|. Then r := ‖ηA⁻¹h‖/‖h‖ ≤ √(3s)·L^{−1/5}.
- Using ‖u/‖u‖ − h/‖h‖‖ ≤ 2r and TV ≤ ½·‖a−b‖·‖a+b‖:

  TV(P_u, |h|²/‖h‖²) ≤ 2√(3s)·L^{−1/5}.

**Classical sampler for the subclass.**

- If L ≥ (4√(3s)/ε)⁵: sample exactly from the explicit |h|², with TV ≤ ε/2 from rounding. The cost is poly(s, bits), with no dependence on L.
- Otherwise L² ≤ (48s/ε²)⁵: do an exact full-grid solve, which is poly(L, B).
- Either way the cost is poly(m, B, n, 1/ε). This is a same-output classical falsifier for advantage on this subclass.
- It also settles parent item 3 for this family. For f = (I−K)δ₀: P_u(0) ≥ 1 − 2√3·L^{−1/5}. The mass does not leak into the shell.
- LCU success is bounded below by (1−r)²·‖h‖² / (‖f‖₁²·3L^{8/5}). Whether it is exponentially small is open [X], because that needs a lower bound on Z₀, which is not proved.

**What is not paid.**

- **Approximate cancellation.** For f = (I−K)h + e with e ≠ 0, exact division returns "no" and supplies nothing. I can prove the perturbation bound

  ‖u − h‖ ≤ √(3s)·L^{−1/5}·‖h‖ + √3·L^{4/5}·‖e‖₁

  (using Z₀ ≤ 3L^{8/5}). But finding a sparse h with small residual e is an approximate sparse-division problem that remains unpaid [X]. The L^{4/5} factor is also not shown to be tight.
- **Sources outside the subclass.** Sources with Fourier transform merely small near λ = 1, a shifted wave number, and general sparse f are untouched.
- **The general sampler.** Nothing here gives a single-source sampler, normalisers, or a sampler for general f.

## 9. Proof obligations for the parent, and falsifiers

1. Verify the AKS definition of h₁ against assumption H, the log base, and that Cor. 2.5's d means total degree.
   - If h₁ differs, recompute c. The structure of the algorithm is unchanged provided c = poly(B, log m).
2. Cor. 2.5 [S] depends on Cor. 1.2 and Lemma 2.3, which were not supplied. Any counterexample to it falsifies the splitting step.
3. Check the arccos modulus lemma and the lattice-point count in §8 independently. This is the step the subclass's classical easiness rests on.
4. Torus completeness is proved only under the promise |supp h| ≤ S. Without that promise, a source that is divisible on the torus may be missed [X].
5. **Falsifier for §6.** Any m-term F over Q(i) with P | F and |supp(F/P)| > (m−1)²(Δ−1)² would refute Cor. 2.5 as applied here, or assumption H.

No novelty, hardness or advantage claim is made. The net effect on the advantage target is negative for this subclass: it is classically easy.
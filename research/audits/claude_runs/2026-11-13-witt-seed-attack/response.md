# Attack on the fixed-length Witt seed for unramified dyadic ternaries

**Scope.** The question is whether the reduction in `UNRAMIFIED_DYADIC_SEED.md` produces a complete local seed for e=1 and arbitrary f in poly(input bits, f, log 1/η). The test assumes an explicit randomized SEARCH primitive.

**Hypothesis S (assumed, not supplied).** Fix constants n, m, d. Given a system of m polynomials in n variables of degree ≤ d over F_q, presented densely in an explicit model F_2[x]/(g), the algorithm does two things:

- If a solution in F_q^n exists, it returns one with probability ≥ 1−η.
- Otherwise it returns NONE.

It runs in poly(log q, log 1/η) bit operations. The constants may depend arbitrarily on (n, m, d), and the algorithm must cover all q, including small q.

**Bottom line.** I did not find a counterexample. The implication holds under S, with the corrections and obligations listed below. Section 1 gives the cheapest decisive attack, Section 2 the proof, Section 3 the failed attacks, Section 4 the residual obligations, and Section 5 the opinion label.

---

## 1. Cheapest decisive attack: the Frobenius twist (hand computation)

I took k = F_4 = {0, 1, ω, ω²} and R = W(F_4) = Z_2[ζ], with ζ³ = 1 and τ(ω) = ζ.

**Universal formulas.** The ghost recurrence w_1 = x_0² + 2x_1 gives:

- S_1 = x_1 + y_1 − x_0y_0, which is x_1 + y_1 + x_0y_0 mod 2.
- M_1 = x_0²y_1 + x_1y_0² + 2x_1y_1, which is x_0²y_1 + x_1y_0² mod 2.

These agree with Rabinoff Example 2.12.

**Twisted map Φ(a_0, a_1) = τ(a_0) + 2τ(a_1^{1/2}).** In F_4, ω^{1/2} = ω².

- Take x = (ω, 0) and y = (0, 1). The Witt product is (0, ω²·1 + 0) = (0, ω²).
- Φ(x)Φ(y) = ζ·2 = 2ζ.
- Φ(0, ω²) = 2τ(ω) = 2ζ. ✓

**Negative control (untwisted Φ′ = Σ 2^i τ(a_i)).**

- Φ′(x)Φ′(y) = 2ζ.
- Φ′(0, ω²) = 2ζ² ≢ 2ζ (mod 4). ✗

**Addition check.** (1,0) + (1,0) = (0, 1), and Φ(0,1) = 2 ✓.

**Digit extraction.** For 2ζ, the Teichmüller digits are c_0 = 0 and c_1 = ω. The rule a_1 = c_1² = ω² gives Φ(0, ω²) = 2ζ ✓.

So equation (1), the a_i = c_i^{2^i} rule, and the claim that untwisted digits are false are all correct at length 2. This is a finite control, not the proof. The proof is Theorem 2.13 together with the truncation lemma L1 below.

---

## 2. Proof of the conditional implication

**L1 (truncated identification).** Rabinoff Theorem 1.2 and Example 1.3 give O_P ≅ R, the strict 2-ring with residue field k, where O_P is the completion at P and e=1.

- Theorem 2.13 gives a ring isomorphism Φ: W(k) → R.
- Φ maps V⁹W(k), the vectors whose coordinates 0..8 vanish, onto Σ_{n≥9} τ(·)2^n R = 2⁹R. Surjectivity holds because Φ is bijective and the digit expansion is unique.
- Hence W_9(k) ≅ R/2⁹R ≅ O_P/P⁹ ≅ O_K/P⁹.

The doc cites Theorem 2.13 but not this truncation step. It is elementary but should be written down, since everything mod 2⁹ depends on it.

**L2 (polynomial encoding is exact).** Truncated Witt operations are given by S_j, M_j ∈ Z[x_{≤j}, y_{≤j}] reduced mod 2 (Corollary 2.10, valid for any ring A, here A = k). Equality in W_9(k) is equality of coordinates 0..8, so no Witt subtraction or negation polynomial is needed.

- The zeroth-coordinate map W_9(k) → k is a ring homomorphism, so (det X)_0 = det(X_0).
- A Witt vector is a unit iff its zeroth coordinate is nonzero.
- Therefore the affine system E_C,D (coordinates 0..8 of (XᵗCX)_{ab} equal those of D_{ab} for a ≤ b, plus h·det(X_0) = 1) has the following solution set: pairs (X, h) where X is a seed and h = det(X_0)^{-1} is determined. This is a bijection.
- Using only a ≤ b is valid because XᵗCX is symmetric over a commutative ring.

**L3 (degree independent of f, with a sharper bound than the doc).** Give coordinate i weight 2^i.

- S_j is weighted-homogeneous of weight 2^j.
- M_j has weight 2^j separately in x and in y.
- In Σ_{c,d} X_{ca}C_{cd}X_{db}, each product has coordinate j of X-weighted degree ≤ 2^j + 2^j. The C-coordinates are constants in k.
- Applying S keeps the invariant "coordinate i has X-weighted degree ≤ 2·2^i". A monomial ∏T_i^{e_i} with Σe_i 2^i = 2^j has X-weight ≤ 2^{j+1}.
- Total degree is at most weighted degree.

So the system has n ≤ 82 variables, m ≤ 55 equations, and degree d ≤ 2⁹ = 512. The determinant equation has degree r+1 ≤ 4. All three bounds are independent of f.

The coefficients are fixed integer polynomials, mod 2, in the 9·6 + 9·6 Witt coordinates of C and D. Computing them costs N·poly(f), where N is an absolute constant (dense monomial count; astronomically large, but fixed).

**L4 (paid input conversion).**

- The cluster entries are in O_K/P⁹, reached through the P-integral Jordan basis with guard digits for denominators (see the cluster discussion in Section 3).
- Teichmüller lifts come from Newton iteration on t^q − t. The derivative is ≡ −1 mod P. Each step costs f squarings in O_K/P^L, and there are O(log L) steps.
- Division by 2 inside O_K/P^L is valid because P/P^L = 2(O_K/P^L) when e=1.
- Digit c_i needs precision 9−i, so L = 9 plus the Jordan guard suffices.
- Coordinates are a_i = c_i^{2^i}, costing i squarings.
- On output, a^{2^{−i}} = a^{2^{f−i}}, costing at most f squarings.

Every step is poly(n, input bits, f).

**L5 (completeness of the mod-2⁹ test).**

- Any O_P-isometry reduces to a solution, so the test never misses a true isometry.
- Conversely, take a seed X and set E = D^{-1}(XᵗCX − D). Then v(E) ≥ 9 − 4 = 5, because the cluster inverse has poles ≤ 4.
- DE is symmetric, so E is D-self-adjoint, and so is any power series in E.
- Since v(binom(1/2, n)) ≥ −2n + s_2(n), the series (I+E)^{−1/2} converges integrally whenever v(E) ≥ 3. This is unchanged for e=1 at any f, because v(2) = 1.
- X(I+E)^{−1/2} is then an exact isometry.

**L6 (cluster separation for e=1).** I re-derived it.

- From A1·Y = 2^h(U^{−t})_{12}B2 we get v(Y) ≥ h−a ≥ 3.
- Then U is block upper-triangular mod 2, so X and T are invertible.
- The first-block relative error B1^{-1}2^h ZᵗA2Z, and E = 2^h Z X^{−1}A1^{−1}X^{−t}ZᵗA2, both have valuation ≥ 3 and are self-adjoint for the relevant form.
- So the square-root corrections apply.

The Jordan step works for any residue field. A diagonal pivot of minimal valuation splits a line. Otherwise there is an off-diagonal unit-normalized β with normalized determinant 4α′γ′ − β² ≡ β² ≢ 0 (mod 2), which splits a binary block. Clusters with gaps ≤ 2 in rank ≤ 3 have diameter ≤ 4 and inverse poles ≤ 4. I found no step that uses f = 1.

**Theorem (conditional).** Assume S, e = 1, the prime P is given, and there is a 2-maximal order. The algorithm is:

1. Run Jordan decomposition and clustering.
2. Encode each cluster with E_C,D.
3. Call S with error budget η/(number of clusters).
4. Map a returned point through Φ and verify natively in O_K/P⁹.
5. Lift the seed.

It outputs a local integral isometry, or localNO with false-NO probability ≤ η. It never returns a false YES, because of the native verification and L5. Its bit cost is poly(input bits, f, L, log 1/η).

*Proof.* L1–L6 give exactness of the encoding. L3 makes S applicable with fixed (n, m, d). L4 bounds the conversion cost. ∎

---

## 3. Attacks on the requested points

- **Witt coordinates vs. Teichmüller digits; Frobenius twist.** Correct (Section 1 and L1). Note that the native verification protects only soundness. If the Witt formulas were wrong, the result would be silent false NOs, which no verification catches. Completeness therefore rests on the proof (Corollary 2.10, Theorem 2.13, L1), not on controls.
- **Degree independent of f.** Correct; L3 sharpens it to d ≤ 512. "Dividing by 2 over Z and then reducing mod 2" is the right procedure.
- **Input access and Teichmüller extraction.** Correct as stated, with two charges the doc should make explicit:
  - The input contract must supply P, or at least a 2-maximal order. Full O_K computation needs discriminant factoring, but the local ring only needs 2-maximality, which is poly-time.
  - S presumably requires an explicit model F_2[x]/(g) of k. The doc's k is a multiplication-table algebra O_K/P. Converting needs a generating element (random elements fail with probability ≤ Σ_{d|f, d<f} 2^d / 2^f), its minimal polynomial (linear algebra), and a change-of-basis map. This is randomized poly(f) and must be charged to η.
- **Guard digits.** The only content is that the Jordan basis W is P-unimodular and that P-integral entries with P-divisible denominators are reduced from enough precision. Three pivots give polynomial heights. This is an obligation, not a refutation (see Section 4).
- **Determinant-unit encoding.** Correct (L2), including clusters whose C itself is singular mod 2.
- **Gaps ≥ 3.** Correct (L6). Modulus 2⁹ is more than needed; 2⁷ would suffice.

**What a decision theorem does not give.** Coordinate-by-coordinate self-reduction over k needs either q trials per coordinate, or Weil restriction to 82f variables over F_2. Both destroy fixed-n poly(log q) behavior. So the doc is right that Kayal Theorem 6.3.8 does not pay X. I am not attempting the separate SEARCH proof.

---

## 4. Residual obligations and falsifiers

1. **(Gate, unchanged.)** Hypothesis S must be proved with exactly these parameters:
   - n = 82, m = 55, d = 512;
   - coefficients in F_q, not only in F_2;
   - all q, with an explicit computable small-q regime (brute force q⁸² is a constant only once q is bounded);
   - reducible, singular, and positive-dimensional varieties, and isolated k-points.
   
   Falsifier: a family of bounded (n, d) systems with rare isolated F_q-points on which the proposed chart/sampling method has success probability → 0 as q grows.
2. **Write L1 explicitly** (V⁹W ↔ 2⁹R), plus the L3 weight argument.
3. **Charge the field-model conversion and P / 2-maximal-order input** to the contract and to η.
4. **Prove P-unimodularity of the Jordan transforms** and give an explicit guard bound in terms of input heights. Falsifier: an input whose pivot denominator valuation exceeds the stated guard, so that C mod P⁹ is computed incorrectly.
5. **Run the doc's proposed F_4 length-3 test** against Z_2[ζ_3]/8, including M_2 and a carry-heavy S_2, plus the untwisted control. This is a regression check on generated code, not proof.
6. **Accept the honest cost.** N (dense monomials in 82 variables at degree 512) is an absolute but astronomically large constant. "Polynomial" here is purely asymptotic in f, and no practical claim follows. Passing to straight-line encodings would require S to accept such encodings, which is a different hypothesis.
7. **Out of scope.** Ramified extensions, integral global witnesses, novelty, speedup, and spinor/global steps are untouched by this argument.

---

## 5. Opinion label

**CONDITIONAL IMPLICATION HOLDS; NO CONCRETE MISTAKE FOUND.** Under Hypothesis S, the reduction pays the full local seed for e = 1 and arbitrary growing f, with obligations 2–4 added as bookkeeping corrections. The twist, degree, determinant, extraction, and gap-3 cluster steps survived direct attack. The native endpoint remains blocked solely on the separate SEARCH proof, so it stays CONDITIONAL.
# Audit: conditional residue-normalization lemma (Section 3)

## Verdict: **REPAIRABLE**

I found **no counterexample** for any odd prime ell. Every algebraic step checks out:

- action signs;
- unit-root ambiguity;
- modulo-pi phase uniqueness;
- squared-reduction isomorphism;
- norm-one lift;
- the lambda-to-lambda² upgrade;
- equation (6).

The lemma is not fully acceptable *as stated*, for three reasons:

1. The phase step uses two analytic operations (Gauss-sum phase and arg L(1, χ̄^j)). Neither is in the stated paid-input list, and "O(1/ell)" has no explicit constant.
2. Reducing compact elements modulo P is used silently.
3. The χ^j ↔ ζ^j labelling convention between formula (2) and the numerically computed modes is an unstated compatibility condition. If it is wrong, the algorithm fails silently.

All three are repairs to the hypotheses and wording, not to the mathematics.

## Setting inferred (needed to check the steps)

- K is the degree-ell subfield of Q(ζ_p).
- Any cyclic field of odd degree is totally real. Complex conjugation has order ≤ 2 in a group of odd order, so it is trivial. The claim "all field elements of K were real" is therefore automatic.
- P is the totally ramified prime above p, so σ(P) = P.
- δ = σ(α)/α is therefore a norm-one **unit**, and c is a unit with c² = δ.
- R = Z[ζ_ell] acts on E/{±1}. The norm element N acts trivially because units have norm ±1.
- T_j(x) = Σ_i ζ^{ij} log|σ^i x| is the log-mode. Then T_j(σx) = ζ^{-j} T_j(x), which matches T_j(c0^u) = u(ζ^{-j}) T_j(c0).

## Step-by-step derivation

**(a) The unit relating generators exists.**
- If c0 ≠ ±1, then Ann_R(c0) = 0. Otherwise R·c0 ≅ R/I would be a finite subgroup of the torsion-free group E/±1, hence zero.
- So C ≅ R. Two generators therefore differ by u ∈ R^*.
- Signs are immaterial because T_j uses |·|, and every later use is squared.

**(b) Unit-root ambiguity.**
- Q(ζ) is CM, so |φ(u/ū)| = 1 at every embedding φ. By Kronecker, u/ū is a root of unity ±ζ^m.
- Conjugation is trivial on R/λ = F_ell, so u/ū ≡ 1 mod λ.
- For the minus sign, −ζ^m ≡ −1 ≢ 1 because ell is odd. Hence u/ū = ζ^m.
- Take a = m(ell+1)/2. Then v = ζ^{-a}u satisfies v̄ = ζ^{a} ū = ζ^{a} ζ^{-2a} u = v.
- **Correct.**

**(c) Mode lower bound.**
- T_0(c0) = log|N c0| = 0.
- If every |T_j| < (log 2)/2, inversion gives |log|σ^i c0|| ≤ ((ell−1)/ell)·max|T_j| < (log 2)/2.
- Every real conjugate then satisfies (σ^i c0)² ∈ (1/2, 2), so |(σ^i c0)² − 1| < 1.
- c0 is a unit with c0² ≠ 1, so N(c0² − 1) is a nonzero integer of absolute value < 1. Contradiction.
- This uses that c0 is an algebraic integer, which holds because C consists of units, and that K is real, which holds by the setting above.
- **Correct.**

**(d) Phase uniqueness.**
- arg[T_j(c)/T_j(c0)] = arg u(ζ^{-j}) = −2πaj/ell + arg v(ζ^{-j}).
- v is real and nonzero under every embedding, so its argument is 0 or π.
- Modulo π, the candidates 2πn/ell (n mod ell) are distinct because ell ∤ 2(n − n'). They form the grid πk/ell, with spacing π/ell.
- j ≠ 0 is invertible mod ell, so a is unique.
- Then c = c0^{ζ^a v} = c1^{v} with c1 = σ^a(c0), and v real.
- **Correct.**

**(e) Squared residue.**
- σ acts trivially on O/P = F_p (total ramification), so x^y mod P = (x mod P)^{y(1)} for y ∈ Z[G].
- c1 = c^{v^{-1}} gives c1² ≡ r^{b} with b ≡ v^{-1} mod λ, so b ≠ 0.
- On norm-one elements, y(1) only matters mod ell, so the R/λ-action on μ_ell(F_p) is well defined.
- η_{a0} = (ζ^{a0/2} − ζ^{−a0/2})/(ζ^{1/2} − ζ^{−1/2}), with half exponents taken mod ell. It is a real cyclotomic unit for a0 ≢ 0 and satisfies η_{a0} ≡ a0 mod λ.
- Hence c2 = c^{w} with w = v^{-1}η_{a0}, which is real, a unit, and w ≡ b·a0 ≡ 1 mod λ.
- **Correct.**

**(f) Isomorphism (5) on U = E/±1.**
- U is a rank-one locally free R-module, so |U/λU| = N(λ) = ell.
- The map w ↦ w² mod P is well defined. Squaring kills ±1, and (σx/x)² ≡ 1.
- Its image lies in μ_ell because w^{2ell} ≡ N(w²) = 1 mod P.
- It is a homomorphism between groups of order ell, and it is surjective given the imported fact r ≠ 1. So it is an isomorphism.
- σ(β)/β ≡ r: since β = αε0, we have σβ/β = δ·σε0/ε0 ≡ r. Equivalently, σ(π)/π mod P does not depend on the uniformizer π.
- x := δ2/(σβ/β) is a norm-one unit with x ≡ 1, so x² ≡ 1 and [x] ∈ λU. Hence x = ±σε/ε.
- The sign is +, because N(x) = 1 while N(−1) = −1 for odd ell. As a cross-check, −1 ≢ 1 mod P for odd p.
- Replacing ε by −ε leaves σε/ε unchanged and flips N(ε). So orienting to N(ε) = 1 loses nothing.
- α2 = βε then has norm p and σ(α2)/α2 = δ2.
- **Correct.**

**(g) Lifting w ≡ 1 mod λ to mod λ².**
- Write w = 1 + λt. Since λ̄ = −ζ^{-1}λ ≡ −λ mod λ², the condition w = w̄ gives λt ≡ −λt̄ mod λ².
- So t ≡ −t̄ ≡ −t mod λ, i.e. 2t ≡ 0, hence t ≡ 0 (ell odd).
- Therefore b' = (w − 1)/λ ∈ λR.
- **Correct.**

**(h) Equation (6).**
- Set γ = α2/α, a norm-one unit. Then σγ/γ = δ2/δ = δ^{w−1} = (δ^{b'})^{σ−1}.
- δ^{y} is an exact element (not just modulo sign) for y ∈ Z[G], since changing the lift by N multiplies by N(δ) = 1.
- So γ/δ^{b'} is σ-fixed, hence a rational unit ±1. Comparing norms (both 1, ell odd) forces +1.
- With b' = λs, we get δ^{b'} = σ(δ^s)/δ^s ≡ 1 mod P.
- (7) then follows: α2/τ(χ̄) = γ·α/τ(χ̄) ≡ k!·1 mod P_L, since P·O_L ⊂ P_L. This uses the imported Taylor facts.
- **Correct.**

**Small cases.** ell = 3 works: the spacing is π/3, η_{1} = 1, and η_{2} is a genuine real unit. No step needs ell > 3. I found nothing that fails for small p either; r ≠ 1 is imported.

## Why the phase step is not removable (sanity check on necessity)

Suppose the phase step is skipped and c0 is used directly. Then w = ζ^{-a}·(real unit) with w ≡ 1 mod λ, so w − 1 ≡ −aλ mod λ². That gives b' ≢ 0 mod λ and α2/α ≡ r^{(nonzero)} mod P. The factorial is then fixed only up to an ell-th root of unity. The phase step therefore carries real weight, and it is exactly where the unpaid costs sit.

## Gaps (the reason for REPAIRABLE)

**G1. Phase oracle not in the paid list.**
- The section calls "Gauss-phase estimation" and "the classical nonquadratic L1 estimator" *proposed* paid operations. The stated already-paid inputs are only c0, the units, β, and the field/embedding.
- The precision itself is cheap: O(log ell) bits.
  - Quantum Gauss-sum phase estimation to error ε is generally cited with cost poly(log p, 1/ε). I have not re-verified the source, so treat this as an import.
  - For arg L(1, χ̄^j) to absolute error ≲ π/(8ell), the needed relative precision is about 1/ell. Nonreal χ gives an effective lower bound |L(1,χ)| ≫ 1/log p (standard; imported).
- **Speculation, flagged:** I am not aware of an unconditional poly(log p, ell) classical method for L(1,χ) at relative precision 1/ell.
  - Partial sums with Pólya–Vinogradov tails need roughly √p·ell terms.
  - Truncated Euler products achieve it under GRH.
  - So the L(1) step plausibly carries either a GRH assumption or exp(log p)-type cost. That cost is not charged anywhere in this section.

**G2. Constants.**
- "Certified absolute log-mode error O(1/ell)" must be explicit.
- Since |T_j(c0)| ≥ (log 2)/2 ≈ 0.347, an absolute error e gives phase error ≤ arcsin(e/0.347).
- Correct rounding to the π/ell grid needs total error (c0 side plus formula-(2) side) < π/(2ell). For example, e ≤ 0.347·sin(π/(8ell)) on the c0 side, and π/(8ell) on the Gauss-phase plus L-phase side.

**G3. Convention compatibility.**
- The numerical modes must satisfy T_j(σx) = ζ^{-j}T_j(x) under the *same* χ^j ↔ ζ^j pairing and embedding used in (2).
- If instead the computation compares (2)'s T_j with the numerical T_{−j}, the ratio is not u(ζ^{-j}). A garbage a then makes α2/α a nontrivial ell-th root of unity, with no visible error.

**G4. Compact reduction mod P.**
- Computing c1² mod P, and solving for the unit coordinates of x, requires the compact factors to be P-integral, or a certified P-adic/valuation-aware reduction.
- "Certified evaluation of compact elements" must explicitly cover reduction modulo P, not just archimedean evaluation.

## Minimal repair

Add the following to the hypothesis list:

- **H_phase:** an oracle returning arg τ(χ^j) + arg L(1, χ̄^j) mod π with error ≤ π/(8ell), for the selected j, with its cost stated. The cost is either GRH-conditional classical, or must be separately justified unconditionally.
- **H_conv:** (2) and the numerical T_j share the labelling T_j(σx) = ζ^{-j}T_j(x).
- **H_red:** certified reduction of compact representations modulo P.

Then replace "O(1/ell)" with the explicit bounds in G2. With these, the lemma is proved as written for every odd prime ell.

## Cheap falsifier/certificate to add

1. **Cross-mode consistency.** Run the phase identification for two modes j and 2j (both have |T| > 0 since u is a unit; use any mode with certified magnitude). Both must return the same a mod ell. A mismatch exposes a G3 convention error or an oracle error. Agreement does not *prove* correctness; it is a consistency check.
2. **Residue check.** Verify c2² ≡ r directly and σ(α2)/α2 = δ2 exactly. Both are cheap given H_red.

Neither check certifies α2/α ≡ 1 mod P on its own, because α is never exposed. That conclusion rests on the proof in (g)–(h) together with a correct a.
# Audit of §8.1 with P > dV+2: squareclass coordinates in L = Q_p[X]/(f)

## Verdict

**Conditional yes, but not as written.** With four repairs, the procedure is a polynomial-bit Las Vegas algorithm, given two inputs:

- the accepted bound V on all local valuations, with V polynomial in the input size, and
- the cited p-integral-basis complexity claim, which the excerpt states only informally.

**Concrete flaw (cheapest decisive):** the hypothesis "p > d" allows d = 1, p = 2. Take f = X, so L = Q_2, and compare a = 3 with a = 1.

- Both are units, so m = 0.
- Both have residue 1 in F_2, so the quadratic character is trivial.
- §8.1 therefore assigns identical coordinates (0, 1) to both.
- But 3 is not a square in Q_2, and Q_2^×/Q_2^{×2} has order 8, not 4.

So the "two squareclass bits" claim is false under the stated hypothesis. **Fix:** require p odd, i.e. p > max(d, 2). For odd p, each component group L_i^×/L_i^{×2} ≅ (Z/2)², and (m_i mod 2, χ(ρ_i(a/π_i^{m_i}))) is a complete invariant (Hensel). This is a deduction.

The other gaps are specification gaps, not falsifications:

- component bases are never constructed;
- the field splitting has no termination test;
- the coordinates depend on the choice of uniformizer.

## Source facts vs. deductions

**Source facts** (from the excerpt):

- The setting is f ∈ A[x] monic, separable and **irreducible**. A = Z uses the Boolean RAM model.
- Theorem 1 gives a triangular basis with a_1 | … | a_{d−1} and D = u·a_1⋯a_{d−1}.
- The intro paragraph says a p-integral basis at a given p has "similar complexity estimates", with h_D and h_red replaced by v_p(D)·h(p) and h(p). It also says no discriminant factorization is needed.
- Δ = D²·Δ_{L/K}.

**Scope caveat:** the local result in the excerpt is an informal one-sentence statement. Its proof and the MaxMin step are in omitted lines. §8 calls it "the local version of Theorem 1". That overstates what the supplied text shows; it is a stated claim, not a displayed theorem.

**Deductions** I accept:

- Factoring over Q first is required, because of the irreducibility hypothesis. Monic integer factors stay monic integer (Gauss).
- Each a_i has v_p(a_i) ≤ v_p(D_j) ≤ v_p(disc f_j)/2 ≤ Δ/2, using disc f = ∏ disc f_j · ∏ Res².
- The p-maximal order of ∏ Q[X]/f_j is the product of the factor orders.
- Z_p[θ] ⊆ O, so converting power-basis input to O-coordinates is integral and loses no precision.
- The structure constants are p-integral rationals. Reduction mod p^P only inverts p-units.
- A stated time bound implies a polynomial output size. Hence the numerators have polynomial bit size, given the source claim.

## Step checks

1. **Nilradical.** On R = O/pO, Frobenius is F_p-linear. Each nilpotent element satisfies x^{e_i} = 0 with e_i ≤ d < p. So ker(a ↦ a^p) = N, and s = 1 suffices. **Correct.**

2. **Splitting R/N.** The "collide with probability ≤ 1/p … logarithmic trials" argument is vague and has no stopping rule.
   - **Repair:** the number of field factors equals dim_{F_p}{x : x^p = x}, the Berlekamp subalgebra.
   - Refine with random elements until that count is reached, giving Las Vegas behaviour. Cap the clock and abort on failure.

3. **Idempotent lifting.** Lifts of idempotents in a commutative ring modulo a nil ideal are unique. So the lifts are automatically orthogonal and sum to 1. The radical J of O/p^P satisfies J^{dP} = 0, so O(log(dP)) Newton steps suffice. **Correct.**

4. **Component basis (gap).** "Multiplication determinant in an integral basis" of O_i requires a Z/p^P-basis of e_i·O/p^P. None is constructed.
   - **Simplest repair:** avoid component bases entirely. Use the full d×d matrix of multiplication by a_i^* := a·e_i + (1−e_i). Its determinant is N_{L_i/Q_p}(a), and v_p(det) = f_i·v_i(a).
   - **Alternative:** select those e_i·b_j whose images mod p are F_p-independent, which gives a basis by Nakayama.

5. **Uniformizer.** For e_i > 1, N_i = πO_i/π^{e_i}. Any lift of a class in N_i∖N_i² has valuation exactly 1. **Correct.**
   - The bit χ(ρ_i(a/π_i^{m})) depends on π_i when m is odd: replacing π_i by π_i·w changes it by χ(ρ_i(w)). The coordinates are relative to a basis.
   - **Repair:** label components canonically, e.g. by lexicographic order of the unique lifted idempotents. Choose π_i by a deterministic echelon rule, fix it once, and reuse it everywhere.
   - Any downstream formula must use the same basis or be basis-invariant. I have not audited that.

6. **Determinant and precision.**
   - v_p(det) = f_i·m_i < f_i·V ≤ dV < P, so the valuation is read exactly. Use valuation-pivoted elimination or Smith form over Z/p^P.
   - Divide by π_i^{m}: solve M x = a_i^*, where M is the matrix of π_i^{m}e_i + (1−e_i).
   - Cramer gives adj(M)·a_i^* ≡ det·x (mod p^P). Dividing leaves precision P − f_i·m_i ≥ 3.
   - Reducing x mod p determines ρ_i(x). **Correct.** The bound is generous; the true loss is about ⌈m/e_i⌉ digits.

7. **Character.** Compute x^{(p^{f_i}−1)/2} in R_i/N_i by square-and-multiply on its multiplication table. This takes O(f_i·log p) steps, and the result is ±e_i. No field model is needed.

8. **Cost.**
   - Ring elements take O(dP·log p) bits, and P > dV is polynomial if V is.
   - Linear algebra, powering and Newton lifting are polynomial.
   - Factoring over Q (LLL) is polynomial.
   - The p-integral basis is polynomial per the source claim. Its cost depends on v_p(D) ≤ Δ/2 and log p, and Δ ≤ log_p|disc f| is polynomial.
   - Polynomial factoring over F_p is randomized; it is charged and capped.

## Proof obligations

1. Exhibit the local p-integral-basis theorem: its statement, output format, and Boolean bound from the omitted text. Otherwise substitute a cited polynomial-time alternative.
2. Prove the Berlekamp-count termination for the refinement loop.
3. Fix the uniformizer and labeling rule, and prove the downstream use is consistent with it.
4. Confirm that the d×d twisted-determinant identity is used rather than unconstructed component bases.

## Falsifiers

- d = 1, p = 2, a = 3: already decisive against the hypothesis as stated.
- Any input whose valuation reaches ≥ V would contradict the accepted bound. Out of scope here.
- A run on the same input that yields two different π_i classes, with coordinates compared across runs.

Agreement with this repaired lemma establishes neither a speedup nor the correctness of the surrounding descent algorithm.
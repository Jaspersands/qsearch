# Classical counterpart search: rational norm image vs. complete S-units

## Verdict

- **Decision.** For a large, classically certifiable subclass of fields, I can classically match the draft's decision step in polynomial time using integer factoring, with no units, class group or S-units. This depends on Hasse-norm-principle theorems that I cite from memory and that you must verify. Outside that subclass, the general decision remains open.
- **Construction.** I found no polynomial classical method. I can name the exact operation a classical shortcut still lacks. I can also give a simplified classical construction: heuristic and subexponential, Las Vegas, with a certified stopping rule. It avoids class groups and regulators, and its only expensive step is that missing operation.
- **General question.** UNKNOWN. Nothing below is a hardness claim.

## 1. Exact reductions (proved)

**R1. The target only matters modulo n-th powers.** For c ∈ Q*, N(c) = cⁿ, and for y ∈ L*, N(yⁿ) = N(y)ⁿ ∈ Q*ⁿ. Therefore:

- If N(x₀) = a·cⁿ with c ∈ Q*, then x = x₀/c is a valid output.
- x₀ only needs to be found modulo L*ⁿ·Q*.
- For S containing the primes dividing a·D (D = |disc L|) and a prime base, the required image is a subgroup of Z[S⁻¹]*/(Z[S⁻¹]*)ⁿ. That group is Z/n on each prime in S plus one sign coordinate, and the sign coordinate is trivial when n is odd.
- So the draft's full Z-HNF over the norm rows can be replaced by (Z/n)-linear algebra of dimension |S|+1. Only representatives are needed, not a complete free basis.

**R2. Tensor-square correspondences contribute nothing to the norm image.** By the draft's own §1, every y_j(b) has N_{L/Q}(y_j(b)) = 1 exactly. Consequences:

- These correspondences can move support but cannot realize any nontrivial class in Q*/N(L*).
- The shortcut "small tensor-square correspondences suffice" is therefore false as a construction method. It always needs an independent x₀ with N(x₀) ≡ a.
- The draft's support theorem (1) is a reduction to N(O_S*). It is not a source of norm values.

**R3. Rational-point parametrization does not supply the missing point.** {N(x) = a} is a torsor under the norm-one torus T. A parametrization of T(Q) helps only after one point x₀ is known. Finding that first point is the whole constructive problem.

## 2. Classical decision on an HNP-certified subclass

**Step A: local test at each relevant place.** Only p | a·D and ∞ matter.

1. *Primes p ∤ a·D.* Local norms from unramified factors are surjective on units, so these primes impose no condition.
2. *Unramified p | a.* The norm group is Z_p* × p^{gcd(f_i)·Z}. The condition is gcd_i f_i | v_p(a). The residue degrees f_i come from factoring the finite algebra O_L/p.
3. *Ramified p.* Write H_p = ⟨N(L_{P_i}*)⟩. Since Q_p*ⁿ ⊆ H_p, work in the finite group Q_p*/Q_p*ⁿ, whose size is polynomial in n.
   - Generators of L_P*/L_P*ⁿ are: a uniformizer, a residue-field generator, and 1+P^j for j ≤ e_P·(v_p(n) + 1/(p−1)) + 1. Above that level, the n-th power map is onto 1+P^j.
   - Their norms are computed by multiplication determinants modulo a polynomial power of p.
   - Discrete logs in F_p*/F_p*^m with m = gcd(n, p−1) ≤ n are done by raising to the power (p−1)/m and searching μ_m. This needs no factoring of p−1.
   - Membership of a is then finite abelian linear algebra.
4. *Infinite place.* If r₁ = 0 (totally complex), require a > 0. Compute r₁ by Sturm sequences on a primitive element.

A local failure is an **unconditional, classically checkable NO certificate**. The draft's quantum NO is only bounded-error.

*Proof obligation:* write out the explicit filtration bound and the precision bounds. This is routine, but I have not done it line by line.

**Step B: certify that the Hasse norm principle holds.** Recalled theorems, to be verified before use:

- HNP holds for extensions of prime degree (Bartels).
- HNP holds when the Galois closure has group Sₙ (Voskresenskiĭ–Kunyavskiĭ).

Prime n is trivial to check. Galois group Sₙ can be certified classically without computing the Galois closure, as follows:

1. Factor O_L/ℓ at unramified primes ℓ. The residue degrees give the cycle type of a Frobenius element of G.
2. Look for a Frobenius whose cycle type contains a cycle of prime length p with n/2 < p ≤ n−3. The other cycles have lengths below p, so a suitable power of this element is a pure p-cycle.
3. **Lemma (proved here):** a transitive G containing a p-cycle with p > n/2 is primitive.
   - Proof: suppose blocks of size b exist, with 1 < b < n. The p-cycle g permutes the n/b ≤ n/2 < p blocks with order dividing p, so g fixes every block.
   - Then the block meeting the p-orbit contains that whole orbit, so b ≥ p > n/2.
   - But b divides n and b < n, which forces b ≤ n/2. Contradiction.
4. Jordan's theorem then gives G ⊇ Aₙ. One Frobenius with odd sign gives G = Sₙ.
5. Transitivity is automatic because L is a field.

Each witness ℓ is an unconditional certificate. GRH (effective Chebotarev) is needed only for the expected polynomial search time, since the relevant densities are about 1/p and 1/2.

**Status.** On certified fields, YES/NO = Step A. The result is randomized polynomial time given the factorizations of D and a. It is conditional on the cited HNP theorems and the Step A obligations. It is not conditional on any S-unit, class-group or principalization data.

## 3. Falsifiers for tempting shortcuts

1. **"Local tests decide in general" — false.** Take L = Q(√13, √17) and a = 25. My recollection is that this is the textbook Hasse counterexample. My own check of the local half:
   - 2 is unramified, since 13 ≡ 17 ≡ 1 (mod 4).
   - At 5, 13 and 17 the local degree is 2: 5 is inert in Q(√13) and in Q(√17), 17 ≡ 4² (mod 13), and 13 is a square mod 17.
   - So every local degree is at most 2 and 25 is a square, hence a local norm everywhere.
   - The claim that 25 is not a global norm is recalled, not re-proved here. Run a CAS check.

   L is Galois, but it lies in the native input class, so the shortcut fails for that class. A non-Galois instance is plausible among quartics with closure group A₄ (recalled, Kunyavskiĭ), but I have no verified instance.
2. **"Ideal-norm solvability plus relation saturation suffices" — false.** In Q(√−5), 2 = N(P₂), yet x² + 5y² = 2z² has no nontrivial rational solution:
   - Reducing mod 5 gives x² ≡ 2z², and 2 is a non-residue mod 5, so 5 | x and 5 | z.
   - Substituting x = 5X, z = 5Z gives 5X² + y² = 10Z², so 5 | y. Infinite descent follows.

   Local symbol (genus) data must supplement ideal relations.
3. **Tensor-square shortcut:** fails by R2.

## 4. Classical construction and the exact missing operation

**Algorithm.**

1. Run §2 to decide (on certified fields), and stop with NO if appropriate.
2. Sample small y ∈ O_L, using LLL-reduced bases of random ideals.
3. Keep y whose norm is B-smooth over a rational prime base, by trial division. No factoring oracle is needed here.
4. Record exponent vectors mod n over rational primes, plus the sign row.
5. Stop as soon as a's vector lies in the span. This stopping rule is certifiable because §2 already proved a is a norm.
6. Output x = ∏ y_i^{e_i}/c with 0 ≤ e_i < n. This is an explicit compact power product, and N(x) = a is verified by the draft's gcd-free method.

**Correctness and completeness.**

- Correctness of any output is unconditional.
- Termination needs a's class to lie in the span of N(O_{S_B}*) mod n. This follows from the draft's support theorem under GRH, plus the heuristic that smooth samples generate that span.
- No class group, regulator, unit basis or principalization is used. The lattice has dimension about |S| over Z/n, not the n·|S| ideal coordinates of a class-group computation.

**Uncharged operation 1 (constructive).** Generate field elements whose norms are smooth over a polynomial-size rational base, enough to span the target class mod n.

- Small elements have norms of size about D^{1/2}·2^{O(n²)}.
- With B polynomial, u = log N / log B grows like log D / log log D.
- Heuristic Dickman-type smoothness then gives superpolynomial cost.
- This is exactly what the quantum complete S-unit step pays for. It is a heuristic cost estimate, not a lower bound.

**Uncharged operation 2 (general decision).** Detect a knot-group obstruction for fields not certified HNP. Known descriptions of the knot group use the Galois group of the closure and its decomposition groups, which is exactly what BS §8.6 avoids. I know of no polynomial classical route; status UNKNOWN.

**Principalization view.** The construction is equivalent to finding a principal ideal (x) in I·K·I_Lⁿ, where N(I) = |a| and K is the group of ideals of norm 1, with the correct sign. Done naively, this needs discrete logs in Cl(L), n-th roots in Cl(L), and one compact PIP generator. The index-calculus route above merges these into smooth-relation generation.

## 5. Consequences for the draft

1. Its decision contribution is narrowed to non-HNP-certified fields. Its constructive contribution is replacing heuristic relation generation (operation 1) by a proven polynomial bound.
2. The draft should state the §2 algorithm and the §4 Las Vegas algorithm as its classical comparators.
3. It should replace the Z-HNF with Z/n linear algebra (R1). This is a simplification, not an error.

**Decisive next controls:**

1. CAS: check that 25 is not a norm from Q(√13, √17), and search A₄ quartics for a knot-obstructed a.
2. Degree 7–11 random fields: run the Sₙ certificate and the Step A tests.
3. Measure smooth-norm yield against B, to test the heuristic cost of operation 1.
4. Verify the Bartels and Voskresenskiĭ–Kunyavskiĭ statements before relying on §2.
# Audit: Bosma–Stevenhagen 1996, Sections 3, 5, 6 and 7, as the source for strict 2‑Sylow generators feeding the Selmer T‑prime step

## Verdict

The source survives the decisive falsifiers. It does **not** need negative Pell, the fundamental unit, or the ambiguous relation. It outputs **explicit reduced forms**, not just invariants, for **both signs** of D.

- **Generation.** The output forms map to a basis of C/2C. By the Frattini argument this means they generate the strict 2‑Sylow C. Lemma 3.5 also gives their exact orders.
- **Projection to the ordinary class group.** The map from the strict to the ordinary class group is a surjection, so it carries C onto the ordinary 2‑Sylow. The images of the output forms therefore generate it, without deciding whether the class of (√D) is trivial.
- **Remaining gap.** The *bit‑complexity* of ternary reduction is not proved in this source. It is cited to Lagarias [8], and one step is explicitly omitted. So the source alone gives correctness, plus polynomial complexity only modulo that citation.

This gap does not threaten the parent's use, because the property the parent needs is deterministically **certifiable** from the output (Section 4 below).

## 1. Falsifiers, cheapest and decisive first

**F1. The real case quietly needs ε_D or the ambiguous relation.** Refuted.
- Pp. 292–293 say explicitly that for D > 0 the algorithm starts with a *generating set* S₀ of C[2], not a basis.
- Invariant (1) on p. 294 only requires that C[2] be *generated* by the elements 2^{j−1}a_j and 2^i s.
- The termination proof on p. 295 uses only (1) and (2). Its test, X_i = X, is a character‑matrix rank condition.
- The relation among the elements of S₀ is an optional by‑product (p. 296).
- No Pell decision and no equivalence test of forms is used.

**F2. The source outputs invariants, not representatives.** Refuted.
- B = ⊔A_j is a set of reduced forms in Φ_D.
- Forms in B have pairwise distinct character vectors (p. 294), so B injects into C.
- Lemma 3.5: B maps to a basis of G/2G, so B generates G, and elements of A_j have exact order 2^j.
- Caveat: this is a basis of C. It is not a basis of the ordinary group, which may have one extra relation.

**F3. Arbitrary halving breaks the invariant.** Refuted, by a check I carried out independently.
- Algorithm 3.4 returns P only up to an element of C[2] (p. 292).
- Invariant (1) uses 2^{i+1}[s_{i+1}] = 2^i[s′]. This value does not depend on the halving choice, since 2^{i+1}t = 0 for t ∈ C[2].
- Composing s ∈ S_i with a ∈ A_j for j ≤ i leaves 2^i[s] unchanged, because 2^j a = 0.
- Different halving choices change which forms are output, not correctness.

**F4. Genus membership is unreliable.** Refuted, but subject to an OCR check.
- Membership is decided by the genus characters, evaluated by (3.3). This is deterministic Jacobi‑symbol arithmetic and needs only the factorization of D.
- Formula (3.3), and the 2‑power conductor definitions (3.1) and (3.2), are missing from the OCR (pp. 290–291).

**F5. Polynomial time is not proved in this source.** This gap **survives**.
- Section 5 alternates binary reductions of F and F\*, but gives no step‑count or coefficient‑size bound. The bounds (5.2)–(5.5) are missing from the OCR (pp. 302–303).
- Lemma 5.8 states that the final map to y² − 2xz is "an explicit transformation that we did not bother to write down". It is a finite table covering 9 forms, so it is recoverable, but it is not in the source.
- Polynomial time is attributed to "Lagarias [8]" (p. 305).
- The p. 284 citation "Lagarias [ ]", for the complexity analysis, has a blank bracket. The parent should identify which of the two Lagarias 1980 papers is meant there.
- **Obligation:** read Lagarias, J. Algorithms 1 (1980), for (i) indefinite binary reduction and (ii) ternary reduction, with polynomial bounds on the entries of M. The size of (p, q, r), and hence of P before binary reduction, depends on this.

**F6. Odd D.** This is a gap in exposition, not in the mathematics.
- Section 6 assumes even D and asserts that C(4D) → C(D) is an isomorphism (p. 305). The source gives no proof and no form‑level map.
- **Independent argument.** The kernel of Cl⁺(4D) → Cl⁺(D) is a quotient of (O_D/2O_D)\*/(Z/2Z)\*, which has order 1 or 3. So the map is an isomorphism on 2‑Sylows.
- Lifting is also fine: since the kernel K is odd, K ⊂ 2Cl(4D), so a lift of a principal‑genus class is again in the principal genus.
- **Obligation:** give an explicit polynomial map from forms (A, 2β, C) with A odd to forms of discriminant D. Do not take it from this source.

**F7. Stopping.** No hard cap is stated in the source.
- The division count (3.6) is missing from the OCR (p. 297).
- **Independent bound.** Each stage performs at most |S₀| ≤ u + 1 divisions, and there are N = log₂(exponent of C) ≤ log₂ h⁺(D) stages. The standard unconditional bound h⁺ ≤ O(√|D| log|D|) gives N ≤ ½·log₂|D| + O(log log|D|).
- So at most (u + 1)·N divisions are needed. This bound is not in the source.
- **Recommendation:** enforce the cap N_max explicitly and abort if rank is not reached. Reaching the cap would falsify an input or a step.

**F8. Randomness.** Benign.
- The only random step is finding a quadratic non‑residue for square roots modulo odd prime powers dividing D (p. 307). Each trial succeeds with probability about ½ and the result is checkable; the 2‑adic case is deterministic.
- Treat the algorithm as Las Vegas.
- For bounded confidence, cap trials at τ per root. The failure probability is then at most R·2^{−τ}, where R ≤ (u + 1)·N·u is the number of roots, and failure is always detected.
- Section 7 is timing data only, a finite control with no asymptotic force.

## 2. Further source dependencies

- **S₀ generates the strict C[2].** The source calls this a "well known fact" (p. 292) and does not prove it. It is true for the *strict* group but can fail in the wide sense. The certificate in Section 4 makes it non‑critical for the parent.
- **Section 6 identities.** Lemma 6.1 needs a ≠ 0, which holds for non‑square D. It uses either a or γ as the unit modulo each p^e. Its congruences, matrix A and identity (6.2) are missing from the OCR (p. 306).
- **Theorem 6.7.** The definition of P (p. 308) and the bilinear relations used with Lemma 2.8 (p. 309) are missing from the OCR. Correctness of halving rests on these. Do not reconstruct them.

## 3. Projection from the strict to the ordinary class group

- A form (a, b, c) maps to the ideal |a|Z + ((−b + √D)/2)Z. Its ordinary class does not depend on the orientation factor that the paper's map attaches (displayed at the top of p. 286, missing from the OCR).
- The p‑Sylow image of a surjection is surjective, so the images of B generate Cl(K)₍₂₎.
- Do not read the ordinary group's structure off the strict output without N(ε). Generation does not need it.

## 4. Strengthening for the parent: certification without trusting Section 6

The parent needs only that Cl(K)/⟨T⟩ has odd order. Suppose forms f_k have classes whose genus‑character matrix has full rank r = dim C/2C. Then:

1. ⟨f_k⟩ + 2Cl = Cl.
2. So H = Cl/⟨f_k⟩ satisfies H = 2H.
3. Multiplication by 2 is therefore surjective on the finite group H, hence injective, so |H| is odd.

The rank is checked deterministically from the factorization of D. This needs (3.1)–(3.3) or a standard genus theory source, plus the equality #C/2C = 2^{dim}; the p. 292 display is missing from the OCR.

So the correctness of Section 6 affects **running time and termination only**, not the validity of the output. Exact orders and membership in C are not needed by the parent.

## 5. Minimal native interface

**Input.**
- The fundamental discriminant d of a quadratic factor, of either sign.
- The full factorization of d. This costs one Shor call plus a deterministic primality certificate, charged.

**Output.**
- Reduced primitive forms (a_k, b_k, c_k) of discriminant d, with |a_k| ≤ √(|d|/3) (stated in the text on p. 286), for k ≤ r ≤ ω(d).
- The nonsingular genus matrix, serving as the certificate.
- Exact orders 2^{j_k}: optional.

**T extraction.**
1. Factor each |a_k| using r Shor calls, each verified.
2. For each prime ℓ dividing a_k, take P = ℓZ + ((−b_k + √d)/2)Z. Primitivity of the form means only one prime above each split ℓ occurs.
3. This gives |T| ≤ r·½·log₂|d|, so the prime support stays polynomial.

**Charges.**
- At most (u + 1)·N_max divisions, each consisting of at most u modular square roots, one ternary reduction (polynomial per Lagarias [8], pending the obligation in F5), and compositions with reduction.
- Character evaluation takes O(r·u) Jacobi symbols.
- Edge cases d = −3 and −4 give r = 0, so T is empty.
- The complete T‑units remain a separate charge in the parent.

## 6. Open obligations

1. Lagarias bounds for ternary and indefinite binary reduction.
2. The Lemma 5.8 final transformation table.
3. The explicit 4D → D form map.
4. An explicit cap N_max with abort.
5. Page‑image checks for pp. 286, 290–292, 297, 302–304, 306 and 308–309.

No novelty or speedup is claimed. A classical counterpart given factorization still needs units, so this does not settle the comparator question.
# Simon (2006) dimension-4 bit clock: proof-quality report

## 0. Verdict

**Does the supplied source prove the clock?** No. The cheapest test settles this: search the supplied text for a complexity proof.

- The starred sentence in the Introduction ("we are able to prove … polynomial") has no proof anywhere in the paper.
- Section 8 says only "It should not be difficult to prove that it runs in polynomial time." It then gives GP timings, which are finite controls and not evidence of a bit bound.
- The source therefore asserts the clock but does not prove it.
- I do not have Kutas 2018's text. To the extent Fact 1 cites Simon for "polynomial time given the factorization of det", it rests on that unproved sentence. **It is not fully justified by the cited proof.**

**Is the claim nevertheless true?** Yes, in the Las Vegas sense, for fixed n. The repair below:

- replaces Simon's Algorithm 1/2 with a definite-LLL-on-a-majorant routine;
- adds explicit size control to the minimization step;
- gives a direct clock for the Bosma–Stevenhagen (B–S) backend.

**Deterministic version.** Not established. It needs deterministic square roots modulo primes p | Δ0. GRH would suffice; nothing else does here.

## 1. Missing lemmas in the source (exact list)

- **M1. Size control in Algorithm 3.**
  - Neither the iteration count nor coefficient growth of Q and of the transform M is bounded.
  - The source's only remark is that LLL "may be interesting".
  - The control flow is also ambiguous: is Lemma 7 iterated? Does Algorithm 3 loop?
- **M2. Clock of the indefinite reduction of [8] (Simon 2005).** Algorithm 1, step 2, imports it. Its proof is not in the packet.
- **M3. A correctness dependency, not only a clock dependency.**
  - Algorithm 1 is valid for n ≤ 9 only through the unpublished preprint [10] ("a solution must be found at Step 5").
  - Algorithm 5, step 10, runs Algorithm 2, hence Algorithm 1, on a 6-dimensional unimodular form.
  - If [10] failed, the fallback (steps 6–7) would call Algorithm 6 in dimension 5. That needs fresh factorizations of the d_k and Algorithm 1 in dimension 7, again via [10].
- **M4. Step 6 cites B–S as "polynomial time".**
  - B–S itself claims only *random* polynomial time.
  - B–S defers its ternary-reduction clock to Lagarias [8 in B–S], which is not supplied.
  - Simon needs the real case (D > 0), which arises from signature (2,2).
- **M5. Randomness.** Lemmas 1, 8 and 9 need square roots or isotropic vectors mod p. The word "polynomial" in the starred claim can only mean randomized.

There is also a minor typo: in Step 8, "discriminant of g is 4δ" should read δ = 4Δ. It has no effect on the clock.

## 2. Independent fixed-n proof

Throughout, n is fixed, entries satisfy ‖Q0‖ ≤ 2^B, and log|Δ0| ≤ n(B + log n).

### L1 (minimization clock and size)

**Setup.** Represent the current form as Q = c·Bᵀ Q0 B, where c ∈ Q_{>0} and B is a basis of a lattice L ⊂ Qⁿ.

- Lemma 4: c ← c/p.
- Lemmas 5, 7, 8: superlattice step, L ⊂ L′ ⊂ p⁻¹L.
- Lemmas 6, 9: sublattice step, pL ⊂ L′ ⊂ L, followed by c ← c/p.

**Count.** Each of Lemmas 4, 5, 7, 8, 9 lowers v_p(det) by at least 1. Lemma 6 (odd n only) raises it by at most n − 4, and runs at most once per call of Algorithm 3. Every step changes det only by a power of p, so v_q is unaffected for q ≠ p. Hence:
- the number of lemma applications is at most Σ_p (v_p(Δ0) + n);
- this holds under any reading of the control flow that executes Lemma 6 once;
- the stopping test ("no lemma applies") is computable from d, v, m and a Legendre symbol.

**Size.** By induction, N1·Zⁿ ⊂ L ⊂ N2⁻¹·Zⁿ, where N1 N2 ≤ ∏ p^{v_p(Δ0)+n} ≤ |Δ0|^{n+1}.

- After each step, replace B by the HNF basis of N2·L, divided by N2. The HNF entries lie in [0, N1N2).
- This is a GL_n(Z) change of basis. The lemma hypotheses are recomputed in the new basis, so correctness is untouched.
- Since c ≤ 1 and Q is integral, |Q_ij| ≤ n²·2^B·(N1N2)².
- So Q and the cumulative M = B have poly(B) bits.

**Primitive operations and imports.**
- Each step uses F_p linear algebra plus one square root or isotropic vector mod p. These are Las Vegas; the source's Lemma 1 already says so.
- Imports: HNF (standard), and Simon's Lemmas 4–9 / Proposition 10 (correctness, taken as given).

### L2 (unimodular isotropic vector; replaces Algorithms 1 and 2, removing M2 and M3)

**Input.** Q ∈ M_n(Z), det Q = ±1, indefinite.

1. **Leading minors.** Compute the leading minors d_k (Bareiss).
   - If some d_k = 0 with k < n, a kernel vector of the leading k×k block is isotropic, with poly bits. Stop.
2. **Majorant.** Otherwise Q = Lᵀ D L over Q with D = diag(d_k/d_{k−1}). Set P = Lᵀ |D| L.
   - P is rational positive definite with poly bits and det P = 1.
   - |Q(x,y)| ≤ √(P(x)·P(y)) by Cauchy–Schwarz in the coordinates Lx.
3. **Definite LLL.** Run LLL (factor 3/4) on P, after scaling to an integral Gram matrix. This is the classical definite-LLL theorem, an import.
   - If P(b₁) < 1, then Q(b₁) is an integer with |Q(b₁)| < 1, so Q(b₁) = 0. Stop.
   - Otherwise the Lovász condition gives P(b_i*) ≥ 2^{−(i−1)}.
   - Since ∏ P(b_i*) = 1, each P(b_i*) ≤ 2^{n(n−1)/2}.
   - Hence P(b_i) ≤ n·2^{n(n−1)/2}, so every |Q(b_i, b_j)| ≤ C(n) := n·2^{n(n−1)/2}.
4. **Bounded search.** The new Gram matrix G lies in a finite set depending only on n: integral, entries bounded by C(n), det ±1, indefinite.
   - Each such G is isotropic. This is Serre Ch. V Th. 3, as cited by the source itself.
   - So a constant R(n) exists with an isotropic vector of sup-norm ≤ R(n).
   - Search boxes of increasing radius. This terminates in O_n(1) time and is rigorous even without knowing R(n).
   - Cassels' bound (external, not in the packet) would make R(n) explicit; it is not needed.
5. **Deterministic.** The whole routine runs in poly(B) time with no randomness.

**Splitting.** Let v be primitive isotropic.
- Since Q is unimodular, Qv is primitive, so extended gcd gives w with vᵀQw = 1.
- Replace w by w − ⌊Q(w)/2⌋·v, so the Gram matrix of ⟨v, w⟩ is [[0,1],[1,ε]] with ε ∈ {0,1}.
- This plane is unimodular, so Zⁿ = ⟨v, w⟩ ⊕ ⟨v, w⟩^⊥, with an integral projection.
- Recurse on the complement, at depth ≤ n/2.
- This yields a totally isotropic subspace of dimension min(r, s) in poly(B) bits.

**Practicality.** The constants are astronomically large, so this is a proof device, not a practical replacement for Simon's reduction.

### L3 (Steps 1, 4, 5, 7, 8, 11)

- **Signature and diagonalization:** Bareiss. A vanishing minor already yields a solution.
- **ε_p for p | 2Δ:** p-adic valuations plus Jacobi symbols. No new factorization is needed.
- **Step 7:** ε_p(g) = (a, δ)_p is a genus-character homomorphism. The step is two F₂ linear systems (cases 1 and 2) of size O(ω(Δ)), followed by at most r compositions with reduction.
  - There is no enumeration of Cl₂.
  - Only representatives spanning Cl/2Cl are needed.
- **Step 11:** rational linear algebra, then pull back through the L1 transform M.

### L4 (B–S clock; closes M4 given B–S correctness)

**Stage count.** Every primitive class (D nonsquare) contains a form with |b| ≤ |a| ≤ |c|. Then |a| ≤ √(|D|/3) for D < 0, and |a| ≤ √D/2 for D > 0 (ac > 0 is impossible). So the strict class number satisfies h⁺(D) ≤ 9|D|, and the exponent of C(D) is 2^N with N ≤ log₂|D| + 4. Termination at X_i = X occurs by stage N; this is B–S's own argument, a correctness import. No unit or Pell computation is involved: the extra real-case generator is carried along, never tested.

**Work per stage.** |S_i| ≤ u + 1 with u = ω(D). Each stage costs:
- O(u²) compositions with binary reduction;
- O(u³) F₂ elimination;
- at most u + 1 divisions by 2.

So the total is O(log²|D|) divisions.

**Composition and reduction.** Composition plus reduction is polynomial, with forms kept at size ≤ |D|. For the indefinite case: if |a| > √D and |b| ≤ |a|, then |c| ≤ |a|/4. So O(log size) rounds suffice.

**Character values.** These do not need the OCR-missing formula (3.3). Primitivity forces a or c to be prime to p (and a or c odd at p = 2), so evaluate χ on that coefficient.

**Division by 2 (Lemma 6.1 / Theorem 6.7), derived without the missing displays.** Let Q = (a, 2β, γ) and δ₀ = aγ − β².
1. Put Q₁ = [[a, β, m′], [β, γ, n′], [m′, n′, t]]. Then det Q₁ = t·δ₀ − (γm′² − 2βm′n′ + an′²).
2. So det Q₁ = −1 if and only if the adjoint form (γ, −2β, a), which is SL₂-equivalent to Q, takes a value ≡ 1 mod |δ₀|. This is the principal-genus condition.
3. Solve for m′, n′ by CRT plus square roots mod p^e (Las Vegas; deterministic at p = 2). This gives entries O(|D|²).
4. Q₁ is indefinite whenever Q is not negative definite.
5. Apply L2 with n = 3: find an isotropic vector, split as H_ε ⊕ ⟨1⟩, then apply a fixed constant matrix to reach φ = y² − 2xz. Fix the determinant with −I. This gives M ∈ SL₃(Z) with poly bits.
6. Theorem 6.7 quantifies over any such M, so its correctness carries over.
7. The OCR loses the exact formula for P and the row/column convention for M. These are correctness details for the parent to check on the page images; the clock is unaffected.

This replaces Lagarias' ternary clock and B–S's own complexity claim.

## 3. Admitted result (conditional interface)

**Theorem.** Fix n ∈ {4, 6}. There is a Las Vegas algorithm with the following behaviour.

- **Input:**
  - a symmetric Q0 ∈ M_n(Z) with entries ≤ 2^B and det Δ0 ≠ 0;
  - the complete factorization of |Δ0|.
- **Output:** either a certificate of local insolubility, or a nonzero x ∈ Zⁿ with xᵀQ0x = 0 and bit-length poly_n(B).
- **Expected cost:** poly_n(B) bit operations.
- **No other integer is factored.** Δ, δ = 4Δ (or −8|Δ|), and the augmented determinants all have primes among those of Δ0.
- **No prime search** and **no GRH** are used. Randomness enters only through square roots and isotropic vectors modulo primes p | Δ0.

**Paths covered.**
- n = 4: Algorithm 5 (minimization in dimension 4, B–S in the real or imaginary case, L1 and L2 in dimension 6), or Algorithm 4 if |Δ0| is a square.
- n = 6: Algorithm 7, which augments to dimension 7, then runs Algorithm 6 with δ = −8|Δ| (imaginary B–S) and L2 in dimension 9. One isotropic vector (g ≥ 1) suffices.

**Imports.**
- Definite LLL and HNF clocks (standard).
- Binary composition and reduction (sketched above).
- Serre V.3.
- Correctness of Simon's Lemmas 4–9 and Propositions 10–15 and of the Algorithm 5/7 logic, as allowed.
- Correctness of B–S Lemma 3.5, termination, Lemma 6.1 and Theorem 6.7, as allowed.

**Not imported:** Simon 2005's clock, preprint [10], Lagarias' ternary clock, B–S's complexity statement.

**Not claimed:** deterministic time; anything about growing n (C(n) and R(n) blow up).

## 4. Proof obligations and falsifiers

1. **v_p accounting.** Check the determinant factors on the page:
   - Lemma 9: p^{2(n−d−m)−n} = p^{−d};
   - Lemma 6: p^{n−2d};
   - Lemma 7: p^{−2}.
   
   **Falsifier:** any lemma that does not strictly lower v_p (other than Lemma 6), or Lemma 6 re-entering within one call.
2. **Majorant bound.** **Falsifier:** an indefinite unimodular G with entries ≤ C(n) that is anisotropic. This would contradict Serre V.3.
3. **B–S stage bound.** **Falsifier:** a run exceeding N ≤ log₂(9|D|) stages, or |S_i| > u + 1.
4. **Las Vegas.** Every square root is verified on output. Expected trials are O(1) per root, over O(n·log|Δ0|) roots.
5. **Interface consistency.** Simon's Step 7 needs only a spanning set of Cl/2Cl, which Cl₂ provides. **Falsifier:** a target genus vector outside the span after B–S terminates. That would refute Simon Proposition 12 or B–S Lemma 3.5, not the clock.

## 5. Consequence for the quartic square-class attack

Given one factorization of |Δ0|, the dimension-4 step is a genuine randomized polynomial-time, factoring-only algorithm under the interface above. It is not proved by Simon's paper; it is proved by L1–L4.

**How to cite it:** cite it as "Simon's algorithm with the repairs L1–L4", not as "Simon 2006, proved polynomial".

**What Kutas Fact 1 can support:**
- If Fact 1 asserts deterministic time, it is unsupported.
- If it asserts polynomial time citing Simon alone, it rests on an unproved remark. It is true only via this repair.

I did not use the allowed conic baseline. For non-diagonal unimodular ternaries, a diagonal Cremona–Rusin solver would require factoring leading minors. L2 avoids that.
**Verdict.** The lemma is TRUE and the proposed construction is sound; it is in fact deterministic. I could not build a counterexample. Below: the attacks tried, the corrected proof with every cost charged, and the standard interfaces that must be explicitly invoked.

---

### 1. Falsification attempts (all failed)

| Attack | Outcome |
|---|---|
| Empty real set / empty finite set / both | x = u0/D, resp. x = z/M, resp. x = 0. Trivial. |
| Totally complex K | Only finite side; trivial. |
| Degree 1, K = Q | Reduces to rational CRT + one real approximation; fine. |
| Huge m_j, huge P, huge targets a_σ | All are charged in the input size (Σ m_j log N p_j, P, target bits), so log N(I), P, and ‖t‖ are poly. No blow-up. |
| Wildly ramified p_j, D divisible by high powers | v_{p_j}(D) ≤ n·v_p(D) ≤ n log₂D, so exponent stays poly. |
| Ill-conditioned Minkowski matrix | Rigorous bound σ_min(A) ≥ \|det A\|/‖A‖^{n−1} ≥ 2^{−r2}/‖A‖^{n−1} = 2^{−poly}; adversary cannot make ‖A‖ exceed 2^{poly(B, log N I)}. |
| Integral basis with huge coordinates | Bounded by B by hypothesis. |

No instance breaks the bound; the only things an adversary can inflate are already in the charged input size.

---

### 2. Corrected proof

**Setup.** ω₁,…,ω_n integral basis, each ω_k = Σ_l q_{kl}θ^l with rational q_{kl} of ≤ B bits (if only the multiplication table is given, see interface (d)). θ root of monic f; by the Cauchy bound |σ(θ)| ≤ 1 + max|f-coeff| ≤ 2^{B+1}, so

 |σ(ω_k)| ≤ n·2^{B}·2^{(n−1)(B+1)} =: W = 2^{O(nB)}  for every embedding σ.  (1)

**Step 1 (finite side, exact).** D = product (or lcm) of denominators of all y_j-coordinates; log D = poly. Put e_j := m_j + n·v_p(D) where p is the rational prime below p_j (this avoids computing the ramification index; e_j ≥ m_j + v_{p_j}(D) since v_{p_j}(p) ≤ n). Then

 log N(I) = Σ_j e_j log N(p_j) ≤ Σ_j m_j log N(p_j) + n²·log D·Σ_j log p_j = poly.

Compute p_j^{e_j} by binary exponentiation with HNF reduction after each ideal product (every intermediate ideal has norm ≤ N(p_j)^{e_j}; HNF entries w.r.t. the integral basis are ≤ the ideal norm), then I = ∏ p_j^{e_j}, with HNF basis b₁,…,b_n, all entries ≤ N(I). Distinct primes are pairwise coprime, so CRT (via HNF of sums to get 1 = a + b, a ∈ 𝔞, b ∈ 𝔟, then standard idempotent assembly) yields u0 ∈ O_K, reduced mod I so coordinates ≤ N(I), with u0 ≡ D·y_j (mod p_j^{e_j}) for all j. Everything is exact integer linear algebra on poly-bit matrices: poly time.

**Step 2 (unit scalar).** R = ∏ p (rational primes below the p_j; R = 1 if none). For any M ≡ 1 (mod R): M − 1 ∈ pO_K ⊂ p_j, so M ∉ p_j, i.e. v_{p_j}(M) = 0. Choose k so that M = 1 + kR ≥ 2^{P+2}·n²·N(I)·W / D; then log M = poly and, by (1) and the HNF bound,

 (Σ_i max_σ |σ(b_i)|)/(D·M) ≤ n²·N(I)·W/(D·M) ≤ 2^{−P−2}.  (2)

**Step 3 (real side).** Let A ∈ ℝ^{n×n} have columns (σ₁(b_i),…,σ_{r1}(b_i), Re τ₁(b_i), Im τ₁(b_i),…) over the r1 real embeddings and one representative τ of each complex pair. A is invertible (b_i is a ℚ-basis), with |det A| = 2^{−r2}√|d_K|·N(I) ≥ 2^{−r2}. Only this lower bound is used, so the normalization convention is irrelevant. Target vector t: real components D·a_σ − σ(u0), complex components 0; ‖t‖ ≤ √n(D·max|a_σ| + n·N(I)·W) = 2^{poly}. Exact solution c = A^{−1}t ∈ ℝ^n exists and is unique. Since ‖A‖₂ ≤ n·n·N(I)·W =: Λ = 2^{poly},

 σ_min(A) ≥ |det A|/Λ^{n−1} ≥ 2^{−r2}Λ^{−(n−1)} =: 2^{−L}, L = poly,

so ‖c‖ ≤ 2^{L}‖t‖ = 2^{poly}.

**Precision accounting.** Isolate all n roots of f (polynomial-time complex root isolation; real roots certified by the supplied intervals/real root isolation), refine each to absolute error δ by Newton/bisection (poly time in log(1/δ)). Evaluate each σ(b_i) = Σ_k b_{ik} Σ_l q_{kl} σ(θ)^l from the refined root: error ≤ 2^{poly}·δ. Choose δ = 2^{−poly} so that ‖ΔA‖ ≤ 2^{−L−1}·min(1, 1/(8M·n·‖t‖·2^{L}))-ish, i.e. by standard perturbation

 ‖Δc‖ ≤ ‖A^{−1}‖‖ΔA‖‖c‖/(1 − ‖A^{−1}‖‖ΔA‖) < 1/(4M).

Solve the perturbed system exactly over ℚ (dyadic entries of poly bit length, Gaussian elimination / Bareiss): poly time. Output c̃ with |c̃_i − c_i| < 1/(4M).

**Step 4 (rounding and output).** k_i = round(M·c̃_i), so |k_i/M − c_i| ≤ 1/(2M) + 1/(4M) = 3/(4M) and |k_i| ≤ M·2^{poly} + 1: poly bits. z = Σ k_i b_i, x = (M·u0 + z)/(D·M): coordinates have poly bit length (numerators ≤ n·M·N(I)·2^{poly}, denominator DM).

*Finite constraints.* x − y_j = (u0 − D y_j)/D + z/(DM). First term: v ≥ e_j − v_{p_j}(D) ≥ m_j. Second: v ≥ e_j − v_{p_j}(D) − 0 ≥ m_j. Hence v_{p_j}(x − y_j) ≥ m_j. (Exact; no approximation involved.)

*Real constraints.* For real σ, using Σ c_i σ(b_i) = D a_σ − σ(u0):

 |σ(x) − a_σ| = (1/D)·|Σ_i (k_i/M − c_i) σ(b_i)| ≤ (3/(4M D))·Σ_i max_σ|σ(b_i)| ≤ (3/4)·2^{−P−2} < 2^{−P}  by (2).

Every step is polynomial in the charged input size; no randomness is used. ∎

**Optional verification.** Finite side: check M(u0 − D y_j) + z ∈ p_j^{e_j} exactly (HNF membership). Real side: interval arithmetic at the final precision. So the algorithm can be made self-certifying.

---

### 3. Necessary corrections to the submitted argument (all minor, none fatal)

1. **v_{p_j}(D)** is not free from the inputs; either compute the ramification index (largest k ≤ n with p ∈ p_j^k, poly time) or, simpler, replace it by the bound n·v_p(D) as above. The exponent inflation stays poly because D has poly bits.
2. **Why HNF basis and u0 are poly-bit**: not merely "because log N(I) is poly" — one must say HNF entries ≤ N(I) *and* that intermediate powers/products are HNF-reduced; and u0 must be reduced mod I.
3. **Embedding magnitudes**: the bound |σ(b_i)| ≤ exp(poly) needs (1), i.e. the power-basis expression of the integral basis plus the Cauchy root bound; the statement "entries have exp(poly) magnitude" is true but was unjustified.
4. **Conditioning**: the determinant formula is correct but only |det A| ≥ 2^{−r2} is needed; the chain σ_min ≥ |det|/‖A‖^{n−1} should be stated explicitly, together with the perturbation bound translating root/evaluation precision δ into the 1/(4M) accuracy on c. The two-stage approximation (approximate A, then round) must be bounded as 1/(2M) + 1/(4M); the submitted text has this right.
5. **Fractional targets**: no issue; rational a_σ only enter t, and the rounding handles it. The *exact* c is irrational in general but never needs to be represented.
6. **"Randomized"** can be strengthened to deterministic; randomness would only enter if one chose to verify the primality promise (polynomial-time factorization of pO_K uses randomized polynomial factoring over F_p). Correctness of the output statement "D M(x−y_j) ∈ p_j^{e_j}" needs only pairwise coprimality, which the CRT step detects exactly (HNF of the sum ≠ O_K ⇒ reject).
7. Choice of M must use a *computable upper bound* for Σ|σ(b_i)| (e.g. n²N(I)W), not the exact value; done above.

---

### 4. Standard interfaces that must be explicitly paid (not hidden)

(a) Ideal HNF, ideal multiplication, CRT in O_K with the entry bound ≤ ideal norm — standard (Cohen-style), polynomial; cited as assumption, not re-proved.
(b) Polynomial-time complex root isolation of f plus certified refinement to 2^{−poly} bits (Schönhage/Pan-type; I did not re-derive the exact exponent). The lemma needs *all* embeddings, not only the designated real ones; if the input designates only a subset of real roots, the remaining real roots are found here and assigned arbitrary targets (e.g. 0).
(c) Exact rational Gaussian elimination on an n×n dyadic matrix of poly bit length — polynomial (Bareiss/Edmonds).
(d) If the integral basis is supplied *only* via a multiplication table without the power-basis coordinates, σ(ω_k) must be obtained e.g. as simultaneous eigenvectors of the multiplication matrices; this is still polynomial but the bound (1) must then be re-derived from B through that route. Flag: the statement "all expanded with total binary length B" is read here as including the ω_k ↔ θ change of basis; if not, this is an unpaid step.
(e) The promise that the p_j are distinct primes: not checked; the algorithm only needs pairwise coprimality, which it certifies.

Nothing beyond these standard polynomial-time primitives is invoked; in particular no weak approximation, class group, units, or principal generators are used, consistent with the constraints.
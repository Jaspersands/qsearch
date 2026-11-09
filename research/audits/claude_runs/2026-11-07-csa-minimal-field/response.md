# Verdict on the §2 minimal-degree splitting-field construction

## Bottom line

- **No counterexample found.** The §2 construction is correct. Below it is restated as a complete proof with finite clocks. I can only see the pasted `context.md` text; I cannot check its SHA256 or open any referenced repository note.
- **No Grunwald–Wang obstruction or norm condition.** Grunwald–Wang only arises if F must be cyclic or abelian with prescribed local degrees. A norm condition only arises if a coefficient, such as the constant term, must equal a prescribed norm. §2 imposes neither. It only asks for a degree-d field with prescribed local behaviour at finitely many places, which is purely local.
- **Simplicity of Fⁿ is proved.** If [F:K]=d, the KM map is a unital K-algebra embedding A → Mₙ(F), and d is the true index, then Fⁿ is a simple A-module. This is a dimension argument, not a sampled observation.

Everything below is conditional on three paid contracts:
1. **(C1)** d is the Schur index.
2. **(C2)** S contains every finite place where A ramifies, and every q∈S is supplied as an explicit prime ideal with an explicit residue map O_K → O_K/q and a lifting section.
3. **(C3)** KM returns a unital F-algebra isomorphism ρ: A⊗_K F → Mₙ(F).

## 1. Proof that F = K[X]/(P) has degree d and splits A (case d ≥ 2)

**Splitting criterion.** For a finite extension F/K: inv_w(A⊗F) = [F_w:K_v]·inv_v(A) at every place w|v. By Albert–Brauer–Hasse–Noether, F splits A if and only if the local index d_v divides [F_w:K_v] for every w|v.

- This is the standard Hasse-principle and restriction argument. It does not need the cited "Goldstein–Schacher Lemma 1", whose exact content I cannot check from here.
- Because index equals period over number fields and d = lcm_v d_v, a degree-d splitting field is a maximal subfield of D. No embedding question remains.

**(a) Finite-field density.** Let Q = |O_K/q|. An element of F_{Q^d} has degree exactly d unless it lies in a proper subfield. Those subfields have at most Σ_{e≤⌊d/2⌋} Q^e < 2Q^{⌊d/2⌋} elements in total.

- 2Q^{⌊d/2⌋} ≤ Q^d/2 holds whenever Q^{⌈d/2⌉} ≥ 4.
- The only exceptions are (Q,d) = (2,2) and (3,2). Checking directly: 4−2 = 2 ≥ 2 and 9−3 = 6 ≥ 4.5.
- So there are at least Q^d/(2d) monic irreducibles out of Q^d monic polynomials. A uniform sample is irreducible with probability ≥ 1/(2d).
- Wild primes (residue characteristic 2 or dividing d) are not special here.

**(b) CRT step.** The primes in S are distinct, so I = ∏q is squarefree and O_K/I ≅ ∏ O_K/q.

- Norm(I) ∈ I, so M·O_K ⊆ I.
- Write T = 1 + M·2^s. Then T ≡ 1 mod p for every rational prime p under S, so T is a q-unit and N_i/T ≡ N_i mod q.
- Therefore P is q-integral and P mod q equals the chosen irreducible polynomial.

**(c) Local degree d at every q ∈ S.** By Hensel, K_q[X]/P is the unramified field extension of degree d.

- So there is exactly one place w|q, with [F_w:K_q] = d, and d_q | d.
- S is nonempty because it contains the primes above 2. Irreducibility over one K_q forces P to be irreducible over K, so [F:K] = d.

**(d) Real places.** If some real place is nonsplit, then 2 | d. In that case the bound below is applied at every real σ, so no real-place identification is needed.

- |σ(N_i)| ≤ U and T ≥ 4dU give |σ(N_i/T)| ≤ 1/(4d).
- Hence for all real x: P^σ(x) ≥ x^d + 1 − ¼·max(1, x^d) ≥ 3/4 > 0.
- So every w over a real place is complex, and [F_w:ℝ] = 2 = d_v.
- If d is odd, no real place ramifies, so no real condition is needed.

**(e) All other places.** At every place outside S and the real places, d_v = 1, so there is nothing to check.

- Primes ramifying in F because of the denominator T are irrelevant.
- No cyclicity, prescribed constant term, normal closure, or global norm equation is used.

**(f) Heights.** All sizes are polynomial in m, d, |S| and the log-norms of the primes in S.

- **N_i:** HNF reduction modulo I gives coordinates bounded by M.
- **U:** U ≤ Σ_j |n_ij|·max|σ(ω_j)|, using power-basis coordinates of the integral basis and a root bound B for K's polynomial. So log U is polynomial.
- **s:** take s = max(0, ⌈log₂(4dU/M)⌉).
- **Absolute polynomial of F:** the minimal polynomial of β + tα comes from Res_y(g(y), P_y(X − ty)).
  - Here g is K's defining polynomial, α a root of g, β a root of P, and P_y is P with its K-coefficients written as polynomials in y.
  - Choose t ≤ (md)² so that the result is squarefree.
  - Its degree is md and its height is polynomial in log T, log M, m, d and K's coefficient height.
  - Computing O_F requires factoring disc(F), which is a paid quantum-factoring contract.

## 2. Simplicity of the module Fⁿ

Let A act on V = Fⁿ by a ↦ ρ(a⊗1). This is a unital, injective K-algebra map, so V ≠ 0. Write A = M_r(D) with r = n/d.

- The simple A-module S₀ = D^r has dim_K = r·d² = nd.
- dim_K V = n·[F:K] = nd. Every A-module is a direct sum of copies of S₀, so V ≅ S₀.
- With [F:K] = n instead, dim_K V = n² = dim_K A. That gives the regular module (r copies of S₀), as the file states.
- **Remaining obligation:** if ρ is only compact, the proof needs a verified certificate that ρ is a unital homomorphism.

## 3. Uniform clocks (error budget η/5 for this stage)

| Step | Clock |
|---|---|
| Residue-field arithmetic per q | F_p-basis of O_K/q from its HNF; dimension f ≤ m |
| Irreducibility tests | ⌈2d·ln(5\|S\|/η)⌉ trials per q; Rabin/Ben-Or, poly(d, f, log p) each. Union bound gives total failure ≤ η/5. Exhausting the cap is ABORT. |
| CRT, HNF reduction, computing U, s, T | Deterministic, polynomial |
| d = 1 | Set F = K; V = Kⁿ, of dimension n = nd |

## 4. Finite controls (consistency checks, not proof)

**K = ℚ, A = (−1,−1)_ℚ.**
- Index d = 2; S = {2}. Mod 2, choose X² + X + 1, giving N₁ = 1, N₀ = 0.
- U = 1 and M = 2, so T = 9 (s = 2) and P = X² + X/9 + 1.
- disc(P) = −323/81, so F = ℚ(√−323) is imaginary. Since −323 ≡ 5 mod 8, the prime 2 is inert in F.
- F therefore splits the Hamilton quaternions. The new ramification at 17 and 19 is harmless.

**K = ℚ(√2), A = (−1,−1)_K.**
- A is ramified only at the two real places (and split at the finite place (√2)).
- S = {(√2)} is still nonempty because the primes above 2 are included, and the real bound handles the real places.

## 5. Proof obligations and falsifiers that remain

1. **Contract C1/C2 failure is silent in §2.** If d is too small or S misses a ramified prime, F may fail to split A. Only a non-split KM outcome or a failed homomorphism check would reveal this. Either should be reported as ABORT, not as a result.
2. **Contract C3.** A compact ρ needs an exact certificate that it is a unital homomorphism. Otherwise the simplicity argument does not apply to the object actually produced.
3. **Cost of O_F.** Factoring disc(F) and computing O_F are charged as new factoring calls on degree-md fields. The denominators T enlarge the discriminant only polynomially in bits.
4. **§3 extraction (checked only briefly).**
   - If x ∈ L and lx = l for all l ∈ L, then x² = x and Ax = L, so any solution is a primitive idempotent.
   - In M_r(D), the kernel of e ↦ (l_j e)_j on L is {y ∈ L : Ly = 0}, of K-dimension (r−1)d². The rank is therefore m·d², matching the file.
   - This is not a full audit of §3's compact certificates.
5. **Out of scope.** Nothing here bears on a quantum speedup, novelty, or classical prior art. A classical all-degree splitting-field or minimal-ideal algorithm would remove any advantage, and §2 itself is entirely classical.
# Audit report: local residue evaluation lemma (`residue_lemma.md`, SHA256 23718b…f72a)

## Verdict
No counterexample found. The procedure is correct and polynomial in all input bits, **conditional on the stated input promises** (O is the maximal order; the supplied factorization a = ∏ P_j^{k_j} is correct with distinct P_j). Below I give the rigorous proof the write‑up only sketches, list exactly which steps the write‑up left as unproved obligations, and state the falsifiers. The cheapest decisive attacks (ramified/dyadic prime, P‑unit with p‑divisible rational denominator, superpolynomial |v_i|, non‑uniformizer π, CRT) all fail for the reasons recorded.

## Setting and conventions
K of degree n given by defining polynomial; O given by a Z‑basis ω_1..ω_n and integer structure constants (bits counted in the input size B ≥ n). Elements of K are rational coordinate vectors. For a nonzero prime P and x ∈ K^×, v_P is the usual discrete valuation (O Dedekind — **assumption A1**, supplied, not verified by this lemma). “Residue of α in O/a” means the image of α in S^{-1}O / a·S^{-1}O ≅ O/a, S = O \ ⋃_j P_j; this is the semilocal reading the write‑up states, and it is the only reading under which the output is well defined when α ∉ O at primes not dividing a.

## Proof (per prime power P^k, then CRT)

**L1 (valuations are polynomially bounded and computable).** Write x_i = y_i/d_i, y_i ∈ O, d_i ∈ Z_{>0} (d_i = lcm of coordinate denominators). Then v_P(x_i) = v_P(y_i) − e(P/p)·v_p(d_i). Bounds: v_p(d_i) ≤ log₂ d_i; e(P/p) ≤ n; v_P(y_i) ≤ v_p(N(y_iO)) ≤ log₂ |N_{K/Q}(y_i)|, and |N(y_i)| = |det M_{y_i}| ≤ (n·C·H_i)^n where C bounds structure constants and H_i the coordinate height of y_i. Hence |v_i| ≤ poly(B), independent of e_i. Computation: v_p(d_i) by repeated division by p (no factoring); v_P(y_i) = max{m : y_iO ⊆ P^m}, decided by HNF containment for m ≤ the bound above (P^m computed iteratively; HNF entries ≤ N(P^m)). All poly(B). *(Write‑up asserted but did not derive the bound; this closes it.)*

**L2 (uniformizer).** P ≠ P² in a Dedekind domain (else P = O by unique factorization). If every Z‑basis element of P lay in P², then P ⊆ P², contradiction. So a basis element π with π ∉ P² exists; v_P(π) = 1. Test: HNF membership in P² (P² = HNF of the n² pairwise products). π may have positive valuation at other primes; this is irrelevant since every subsequent step for this P only uses v_P and O/P^k, and each prime uses its own π. Heights poly(B).

**L3 (height of u_i).** π^{-1} = π̃/N(π) with π̃ = product of the other conjugates ∈ O, computable as the adjugate column of M_π; height poly(B). π^{-v_i} has coordinate bit size ≤ |v_i|·poly(B). Hence u_i = x_i π^{-v_i} has height poly(B) and v_P(u_i) = 0 exactly (identity in K).

**L4 (denominator ideal escapes P).** Let u_iO = A·B^{-1} with A, B coprime integral ideals (unique). Then D_i := {b ∈ O : b u_i ∈ O} = u_i^{-1}O ∩ O = A^{-1}B ∩ O = B, because for every prime Q, max(v_Q(B) − v_Q(A), 0) = v_Q(B) by coprimality. Since v_P(u_i) = 0, v_P(B) = 0, so D_i ⊄ P, and as in L2 some Z‑basis element b_i of D_i lies outside P. Computation: with u_i = y/d, D_i = {b ∈ Z^n : M_y b ∈ dZ^n}, a kernel/HNF computation over Z, poly(B). Put a_i = b_i u_i ∈ O; a_i ∉ P (since v_P(a_i) = v_P(b_i) = 0). *(Write‑up asserted D_i ⊄ P; the coprime‑factorization argument is the missing proof.)*

**L5 (residues of local units mod P^k).** b_i ∉ P ⇒ b_iO + P = O ⇒ b_iO + P^k = O (any maximal ideal containing b_iO + P^k contains P^k, hence equals P, contradicting b_i ∉ P). An inverse b_i^{-1} mod P^k is obtained from s b_i + t = 1, t ∈ P^k, via HNF of the lattice b_iO + P^k (poly(B)). Define ū_i := a_i · b_i^{-1} ∈ O/P^k. Well‑defined: if a/b = a'/b' with b, b' ∉ P then ab' = a'b in O, so ab'^{-1} ≡ a'b^{-1}. This is the image of u_i under O_P → O_P/P^kO_P ≅ O/P^k. Since a_i ∉ P, ū_i is a unit, so negative exponents are handled by inverting a_i the same way. Binary powering uses O(log|e_i|) ring operations in O/P^k; elements are kept reduced mod HNF(P^k), coordinates ≤ N(P^k) ≤ N(a) ≤ 2^B. *(This is the step the Q(√2) and Q(i) controls target; it is exactly why integer‑denominator clearing is insufficient and why leaves are normalized before reduction.)*

**L6 (assembly).** In K, exactly: α = ∏ x_i^{e_i} = ∏ (u_i π^{v_i})^{e_i} = U · π^{v}, U := ∏ u_i^{e_i}, v := Σ e_i v_i. v_P(U) = 0 and v_P(π^v) = v, so v_P(α) = v; v is a binary integer of poly(B) bits. If v < 0, P is a prime of negative valuation (correct output). If v ≥ 0 then α ∈ O_P and its image in O/P^k is Ū·π̄^v, with Ū = ∏ ū_i^{e_i} and π̄^v = 0 for v ≥ k, else computed by powering with v < k ≤ log₂ N(P^k) ≤ B.

**L7 (CRT).** For distinct P_j, the P_j^{k_j} are pairwise coprime, so O/a ≅ ∏ O/P_j^{k_j}; idempotents from 1 = s_j + t_j with s_j ∈ P_j^{k_j}, t_j ∈ ∏_{l≠j} P_l^{k_l}, again HNF. The combined class, reduced mod HNF(a), equals the image of α in S^{-1}O/aS^{-1}O ≅ O/a, because the latter isomorphism factors through the localizations. Output bits poly(B).

**Cost.** Every step is HNF/linear algebra over Z on matrices of dimension ≤ n² with entries of poly(B) bits, plus O(Σ_i log|e_i|) ring operations per prime; total poly(B). Nothing depends on tameness, residue characteristic, or e(P/p) beyond the factor ≤ n in L1 — ramified and dyadic primes are covered. No GRH; unconditional.

## Finite controls (not proofs)
- Q(√2), P = (√2), α = 2^E (√2)^{-2E}: v₁ = 2, v₂ = 1, v = 2E − 2E = 0; with π = √2, u₁ = u₂ = 1, α ≡ 1 mod P^k. Correct for all E.
- Q(i), P = (2+i), u = (2+i)/5: v_P(u) = 0 but rational denominator 5 ∈ P. D(u) = (2−i)O, b = 2−i ∉ P, a = 1; ū = (2−i)^{-1} mod P^k. Integer‑denominator clearing would have attempted to invert 5 mod P^k and failed. Confirms the need for L4, not a counterexample.

## Assumptions the lemma does not prove
- **A1** O is genuinely maximal (Dedekind). If not, L2/L4/L6 fail (non‑invertible primes, no valuations). Verifying maximality unconditionally requires factoring disc(O); correctly charged to the caller.
- **A2** The supplied factorization is correct and the P_j distinct. Correctness of each P_j being prime and of ∏ P_j^{k_j} = a can be *verified* in poly(B) (primality of N(P_j) via AKS, field test on O/P_j as an F_p‑algebra, ideal product/HNF compare, pairwise HNF distinctness); the write‑up does not say it does this, so either verify or state the promise.
- **A3** All x_i ≠ 0 (stated).

## Residual proof obligations in the write‑up (all discharged above)
(i) explicit polynomial bound on |v_i| (L1); (ii) D_i ⊄ P (L4); (iii) well‑definedness and invertibility of ū_i, inverse computation mod P^k (L5); (iv) identity α = Uπ^v in K and the v ≥ k ⇒ 0 case (L6); (v) semilocal interpretation of “residue in O/a” and CRT idempotent construction (L7).

## Falsifiers
1. A nonzero u ∈ K with v_P(u) = 0 whose denominator ideal lies in P — would contradict unique factorization; impossible under A1.
2. A choice of π from a Z‑basis of P with π ∈ P² for every basis element — impossible (L2).
3. An input family with |v_P(x_i)| superpolynomial in B — contradicts the norm bound in L1.
4. HNF/kernel blow‑up beyond poly(B) on any step — no step involves unbounded exponents; the only exponent ever expanded is |v_i|.
5. A non‑maximal O or incorrect factorization producing a wrong residue — a violation of A1/A2, not of the lemma.

## Scope note
This audit covers only the residue lemma. It makes no claim about the BHJ integral‑similarity repair, compact units, or any speedup; the lemma’s correctness is necessary but not sufficient for that application.
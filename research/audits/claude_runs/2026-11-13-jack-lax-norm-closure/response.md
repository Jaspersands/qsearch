# Can the Lax hierarchy make adaptive derivative norms polynomial? Review of a uniform hierarchy closure

## Verdict

**No successful candidate.**

- **What is proved here:**
  - The requested elimination always exists formally in each fixed degree. It therefore has no content beyond the cost of evaluating a function of λ.
  - The full family of requested norms contains the Born probabilities themselves.
  - Under a uniform finite hierarchy closure, the expectation of every word would be a polynomial on two-row shapes. The single word V_{-1} on the shapes (a,1) already rules this out.
  - At α=3, power-sum multiplication has no ribbon (Murnaghan–Nakayama) locality. The α=1 shortcut for single derivatives therefore does not transfer.
- **What is not proved:** that no polynomial method exists. No hardness claim is made.

## 1. Exact reformulation (proved)

Let A = ∏_k V_{-k}^{n_k}, so ν = (1^{n_1} 2^{n_2} …) is the removed multiset. All V_{-k} commute, so A†A = (∏V_k^{n_k})(∏V_{-k}^{n_k}).

This operator is diagonal in the power-sum basis: on p_μ its eigenvalue is ∏_k (3k)^{n_k} (m_k(μ))_{n_k}, a product of falling factorials of the multiplicities. Hence

  ⟨J_λ, A†A J_λ⟩ / H_λ = E_{μ∼π_λ} [ w_ν(μ) ],  where w_ν(μ) = ∏_k (3k)^{n_k} (m_k(μ))_{n_k}.

These are joint factorial moments of the part multiplicities of the Born random partition μ. They are not moments of τ_λ. τ_λ is a measure on at most O(√D) addable corners, and its moments are the eigenvalues of T_l.

Two consequences follow.

1. **The adaptive conditional is a posterior expectation.** At history ν, the probability of removing k is
   E[w_ν · 3k(m_k − n_k)] / (3(D−|ν|) · E[w_ν]).
   This is the conditional expectation of k(m_k − n_k)/d under π_λ reweighted by w_ν.
2. **The top layer is the Born law itself.** If |ν| = D, then w_ν(μ) is nonzero only at μ = ν. This gives
   ‖V_{-ν} J_λ‖² / H_λ = π_λ(ν) · ∏_k (3k)^{n_k} n_k!.
   - The derivation: V_{-ν} J_λ is the scalar θ_ν ∏(3k)^{n_k} n_k!, and z_ν 3^{ℓ(ν)} = ∏ (3k)^{n_k} n_k!.
   - So exact polynomial computation of *all* adaptive norms implies exact evaluation of |θ_μ(λ)| for every pair (λ, μ). At α=1 this is |χ^λ(μ)|.
   - No hardness result is imported here, since none is supplied. The point is only that "all adaptive norms exactly" is a much stronger goal than sampling.
   - Sampling within TV ε needs only additive accuracy about ε/D² on the normalized conditionals, along reached histories.

**Sanity check: T_2 is the depth-one sum rule.** At ε = ε1+ε2 = 2, the top-left entry of L² is (L²)₀₀ = Σ_k V_k V_{-k}. Its eigenvalue on p_μ is Σ 3k·m_k = 3D, so T_2 = 3·degree. This is exactly the sum rule Σ_k ‖V_{-k}J‖² = 3D·H. The hierarchy fixes only this sum, never the individual terms.

## 2. Why the formal elimination is empty (proved)

**Commutators with a hierarchy element have zero expectation.** For T Jack-diagonal with eigenvalue t_λ,
  ⟨J_λ, [X,T] J_λ⟩ = t_λ⟨J_λ, X J_λ⟩ − t_λ⟨J_λ, X J_λ⟩ = 0.

**Every off-diagonal part is such a commutator.** On F_D the hierarchy separates partitions: by (2∨), T_λ(u) determines A_λ and R⁺_λ, hence λ. So the Jack-off-diagonal part of any O is a sum of terms [X,T].

**The diagonal part is always some polynomial in the T_l.** The diagonal part of O is the function λ ↦ ⟨J_λ, O J_λ⟩ / H_λ. It is a polynomial in the T_l by interpolation over the p(D) partitions.

So "normally ordered A†A = diagonal hierarchy part + zero-expectation commutators" always holds. The entire question is the size of a representation of f_ν(λ) = E_λ[w_ν]. Since λ is given explicitly, the Lax language adds no leverage unless f_ν lies in a compact spectral class.

## 3. Falsifier of a uniform finite closure (proved)

**Claim tested.** Diag(V_1 V_{-1}) = P(T_1, …, T_L), with P fixed independently of λ (and hence of D).

**Step 1: T_l eigenvalues are polynomials on shapes (a,1).**
- Take log of the product formula (2∨) and expand in 1/u. Each coefficient is a sum over boxes of a polynomial in box contents.
- For the shapes (a,1), Faulhaber's formulas make each such sum a polynomial in a.
- Each T_l is a finite expression in these coefficients, so P(T) restricted to (a,1) is a polynomial in a.

**Step 2: compute F(λ) = ‖V_{-1}J_λ‖²/H_λ.**
- By adjointness, F(λ) = Σ_{r∈R_λ} τ_{λ−r,r}² H_λ/H_{λ−r}.
- The inputs are the Pieri weights (1.18) at ε1=3, ε2=−1 and the hook-norm formula H.
- For λ = (a,b), write d = a−b. Then
  F = 3d(3d−1)(3a+1) / ((3d−2)(3a−1)(3d+1)) + 9b(d+1)(3d+2) / ((3d+4)(3b−2)(3d+1)).
- At d=0 the first term vanishes, which is consistent with a single removable corner.

**Step 3: check against direct expansion.**

| λ | Formula value | Direct check |
|---|---|---|
| (1,1) | 9/2 | J = p1² − p2, H = 24 |
| (2,1) | 186/35 | J = p1³ + 2p1p2 − 3p3, H = 315 |
| (3,1) | 1239/280 | J = p1⁴ + 8p1²p2 − 3p2² + 12p1p3 − 18p4, H = 17280 |

- The (3,1) Jack was built from p1·J_3 via Pieri with τ = 1/10 and 9/10.
- For (3,1), E[3m_1] = 3·25488/17280 = 4.425 = 1239/280.

**Step 4: conclude.** As a → ∞, F(a,1) → 1 + 3 = 4, and F is not constant. A polynomial in a that is bounded on ℕ must be constant. So no λ-uniform finite closure exists, already for the single word V_{-1}.

**Scope.** This does not exclude closures whose coefficients depend on D. For those, the obligation is an explicit poly(D)-size representation.

## 4. No ribbon locality at α=3 (proved)

Expanding p_2 J_1 = p_1 p_2 in the degree-3 Jacks gives

  p_2 J_1 = (1/28) J_3 + (4/35) J_21 − (3/20) J_111.

The skew shape (2,1)/(1) is disconnected, yet its coefficient is nonzero. At α=1 this coefficient is 0 (p_2 s_1 = s_3 − s_111).

- **Consequence:** the Murnaghan–Nakayama argument, which makes single-p_k derivative norms polynomial at α=1, fails at α=3.
- **OPEN:** whether p_k J_ν generically has full support on {λ ⊇ ν : |λ/ν| = k}. If it does, the single word V_{-⌊D/2⌋} already sums over exponentially many ν on worst-case shapes.

## 5. What survives, and the remaining obligation

**Bounded depth j is cheap.**
- Depth j=1 with k=1 is a sum over corners of local rational functions of corner data. This is shown explicitly for two-row shapes.
- General corner-locality of H_λ/H_{λ−r}, and its residue form via T_λ(u), is OPEN here.
- A word of total degree j touches at most (D+1)^j subshapes, so its cost is D^{O(j)}.
- Adaptive histories reach depth ~D/2, and there this is the downset again. No improvement over poly(D)·M².

**A real solution would need:** for every multiset ν with |ν| ≤ D, a poly(D)-size circuit or recursion for E_λ[w_ν], or for the normalized conditionals to additive accuracy ε/D². Its inputs may only be the corner data of λ (equivalently T_λ(u)). It must:
- reproduce F(a,b) above;
- reproduce the p_2 J_1 support fact;
- reproduce one-row behavior: the Born law of (D) is exactly Ewens(1/3), since π(μ) = D!·3^{D−ℓ} / (z_μ ∏_{a<D}(3a+1)).

## 6. Parent claim A_D 1 = binom(2D−1, D) J_(D)

**Status: OPEN, not checked.** The definitions of B_∞ and Γ are not in the evidence supplied here; only Mickler–Moll is. So I cannot verify the claim.

**Cheapest falsifier.** Using J_(n) = Σ_μ n!·3^{n−ℓ(μ)}/z_μ · p_μ (verified for n ≤ 3), the claim requires:
- A_1 1 = p_1;
- A_2 1 = 3p_1² + 9p_2.

Even if true, the claim concerns only the one-row shape, which is trivial (Ewens(1/3)).

## Disposition

**Established:**
- (a) The requested quantities are factorial moments of Born multiplicities. Their top layer is |θ_μ(λ)|²·(known factors), so "all norms exactly" overreaches the sampling task.
- (b) The commutator-plus-diagonal decomposition is formally automatic.
- (c) No λ-uniform finite polynomial hierarchy closure exists. The falsifier is the word V_{-1} on shapes (a,1).
- (d) α=3 Pieri-type multiplication by p_2 is non-ribbon.

**Not established:**
- any polynomial classical method for unrestricted shapes;
- any hardness result;
- the parent's A_D identity.

The matched classical baseline remains poly(D)·M².
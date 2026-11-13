# Uniform spectral gap of the bosonic parent Hamiltonian H_P: proved reductions, open core

## Verdict

I could **neither prove nor disprove** the uniform polynomial gap statement.

- I have no explicit sequence with a superpolynomially small first positive eigenvalue. Without one, nothing is killed.
- I have no polynomial gap bound valid for all P with spectrum in [1/2,1]. Without one, no adiabatic or normalization algorithm is paid for, and **no algorithmic claim is made**.

What follows separates:

- lemmas I prove completely (some settle sub-questions in the contract);
- one proved negative result about a proof *technique*;
- the exact open inequality, stated as a weighted Poincaré / Fischer-norm problem;
- the precise form a falsifier must take.

Notation:

- 𝓗_N = Sym^N(ℂ^N), the fixed-N, N-mode sector.
- e = |1^N⟩.
- S = Γ(P)|_{𝓗_N}.
- D_j = n_j − 1.
- G = P†P = P² (P is Hermitian positive definite with spectrum in [1/2,1]).
- M = Γ(G)|_{𝓗_N} = S†S.

## Proved lemmas

**L0 (intertwining).**
- The identities are Γ(P) a_u† Γ(P)⁻¹ = Σ_v P_{vu} a_v† and Γ(P) a_u Γ(P)⁻¹ = Σ_v (P⁻¹)_{uv} a_v.
- Hence b_j†c_j = Γ(P) n_j Γ(P)⁻¹ and K_j = S D_j S⁻¹.
- In first quantization, K_j = dΓ(Π_j) − 1, with Π_j = P e_j e_jᵀ P⁻¹ a rank-one oblique projector, ‖Π_j‖ ≤ κ(P) ≤ 2, and Σ_j Π_j = I.

**L1 (invariances).** Let U be unitary and D diagonal and invertible (any complex entries).
- Replacing P by UPD gives b_j† → d_j·Γ(U)b_j†Γ(U)† and c_j → d_j⁻¹·Γ(U)c_jΓ(U)†.
- Hence H_{UPD} = Γ(U) H_P Γ(U)†, and the spectrum of H_A equals the spectrum of H_P.
- The spectrum depends only on the column-rescaling class of P, i.e. on G modulo diagonal congruence.
- **Corollary:** for every diagonal P, H_P = H_I = Σ_j (n_j−1)², whose gap is exactly 2. The diagonal half-loss example is spectrally trivial, consistent with the contract's warning.

**L2 (no multiple-zero issue).** For every invertible A, ker H_A on 𝓗_N is exactly one-dimensional.
- Proof: Hψ = 0 iff K_jψ = 0 for all j, iff D_j S⁻¹ψ = 0 for all j.
- The only Fock state with all n_j = 1 is e, so ker H_A = ℂ·S e = ℂ·ψ_P.

**L3 (exact variational form).** Write ψ = Sφ.
- Then ⟨ψ,Hψ⟩ = Σ_j ⟨D_jφ, M D_jφ⟩, ‖ψ‖² = ⟨φ,Mφ⟩, and ψ ⊥ ψ_P iff ⟨φ, M e⟩ = 0.
- Hence

  λ₁(H_P) = min over φ ≠ 0 with ⟨φ,Me⟩ = 0 of Σ_j ‖D_jφ‖²_M / ‖φ‖²_M.

- In the Fock basis, M_{nm} = per(G[n|m]) / √(n! m!). The numerator is Σ_{n,m} φ̄_n φ_m M_{nm} ⟨w(n),w(m)⟩ with w(n) = n − 1.
- So the gap is the second eigenvalue of the pencil (L, M), where L = Σ_j D_j M D_j.

**L4 (rigorous but exponential lower bound).**
- Statement: λ₁(H_P) ≥ λ₁(L) ≥ 2·σ_min(P)^{2N} ≥ 2·4^{−N}.
- Step 1: H = X†LX with X = S⁻¹. By Ostrowski's theorem, λ_k(H) = θ_k λ_k(L) with θ_k ≥ σ_min(S⁻¹)² = ‖S‖⁻² ≥ 1, since ‖P‖ ≤ 1.
- Step 2: L ≥ λ_min(M) Σ_j D_j², and λ_min(M) = σ_min(P)^{2N}.
- Step 3: on e^⊥, Σ_j D_j² ≥ 2, because w(n) is a nonzero integer vector with zero sum, so ‖w(n)‖² ≥ 2.
- Step 4: L and Σ_j D_j² have the same kernel ℂe.
- With column scaling (L1) the bound improves to 2·min_D κ(PD)^{−2N}. It is still exponential. This is only the "generic conditioning" bound the contract already flags.

**L5 (perturbative polynomial gap near the start of the path).**
- Let δ = max_j ‖Π_j − e_je_jᵀ‖ and F_j = dΓ(Π_j − e_je_jᵀ).
- On 𝓗_N, ‖F_j‖ ≤ Nδ and ‖D_j‖ ≤ N.
- Then ‖K_j†K_j − D_j²‖ ≤ 2N²δ + N²δ² ≤ 3N²δ, so ‖H_P − H_I‖ ≤ 3N³δ.
- By Weyl's inequality and L2, λ₁(H_P) ≥ 2 − 3N³δ.
- So the gap is ≥ 1 whenever δ ≤ 1/(3N³). On the path P(s) = (1−s)I + sP this covers only s = O(N⁻³). It is a valid quantified statement, but useless for the full path.

**L6 (block-diagonal families reduce to their blocks).** Let P = P₁ ⊕ P₂ with block sizes N₁ + N₂ = N.
- H = H⁽¹⁾ + H⁽²⁾, and Γ(P) preserves each block's particle number n⁽ⁱ⁾.
- Inside block i, Σ_{j∈block i} K_j = n⁽ⁱ⁾ − N_i.
- Operator Cauchy–Schwarz gives Σ_{j=1}^m X_j†X_j ≥ (1/m)(Σ_j X_j)†(Σ_j X_j). So H⁽ⁱ⁾ ≥ (n⁽ⁱ⁾ − N_i)²/N_i on the n⁽ⁱ⁾ sector.
- Hence gap(H_P) ≥ min(gap H⁽¹⁾_{N₁}, gap H⁽²⁾_{N₂}, 1/N).
- **Consequence: a block-diagonal family cannot be a falsifier unless one of its blocks already is.**

## Proved negative result about a technique

**L7 (the congruence route cannot work, with an explicit example).** Take the rank-one family P = I − ½uu*, u = 𝟙/√N. Then G = I − ¾uu* and M = 4^{−n_U}, where U is the mode u.

- Take φ = |u^N⟩. Since a_j† = u_j a_U† + a_{w_j}† with w_j = e_j − u/√N, one computes D_j|u^N⟩ = a_{w_j}†|u^{N−1}⟩, which lies entirely in the n_U = N−1 sector.
- Therefore Σ_j ⟨D_jφ, D_jφ⟩_{weighted by M} = (N−1)·4^{−(N−1)}.
- Project out e. The overlap is √(N!/N^N), which is exponentially small, and D_j e = 0. This gives λ₁(L) ≤ 2(N−1)·4^{−(N−1)}.

So L4's chain is exponentially lossy on this family. Any polynomial proof must use the M-weighted orthogonality of L3, not Ostrowski or Sylvester congruence.

The *same* direction is not low-energy for H itself:

- S|u^N⟩ = 2^{−N}|u^N⟩ and S a_{w_j}†|u^{N−1}⟩ = 2^{−(N−1)}(·).
- So K_j|u^N⟩ = 2·a_{w_j}†|u^{N−1}⟩, and Σ_j ‖K_j|u^N⟩‖² = 4(N−1).
- After removing the ψ_P component (killed by every K_j), the Rayleigh quotient is ≥ 4(N−1).

The exponential conditioning of S cancels along coherent directions. A low-energy vector of H would have to mix sectors with exponentially different S-weights while keeping all D_jφ small in M-norm.

Related observation (sketched, not a full proof): for a single oblique term K_j, the obvious "ill-conditioned ladder" vectors (binomial-tail truncations of the ground state) give Rayleigh quotients Θ(N), not exponentially small. In each case the large-norm recursion solution is essentially the kernel vector itself. The heuristic is that smallness would need a genuine bottleneck in ψ_P. That is a Cheeger-type intuition only; H is not stoquastic, so no theorem is invoked.

## The exact open inequality

The full contract reduces exactly to the following (L1 and L3).

Identify 𝓗_N with homogeneous degree-N polynomials in z ∈ ℂ^N under the Fischer (Bargmann) norm ‖·‖_F. Let y = Pᵀz, so the y-coordinates are the linear forms ℓ_j(z) = Σ_u P_{uj} z_u. Let E_j = y_j ∂/∂y_j, the Euler operator in the oblique coordinate y_j.

**Conjecture (UNPROVED).** There exist constants C, c > 0 such that for all N, all Hermitian P with spec(P) ⊂ [1/2,1], and all g ⊥_F ℓ₁⋯ℓ_N:

  Σ_j ‖(E_j − 1) g‖²_F ≥ c·N^{−C}·‖g‖²_F.

- Each y-monomial y^n is an eigenvector of every E_j with integer eigenvalue n_j.
- The Gram matrix of the y-monomials in Fischer norm is M = Γ(G).
- This is a weighted Poincaré inequality in which the "gradients" D_j are multiplication operators and the measure is the permanent kernel M.

Neither representation theory nor frustration-freeness alone gives it. L4 is the best bound I can prove, and L7 shows that the congruence method behind it is sharp-to-exponential.

The rank-one family is S_N-mode-symmetric, since P commutes with mode permutations. So H block-diagonalizes over S_N irreps. That reduction, plus the M = 4^{−n_U} sector structure, is the cheapest place to attempt either a proof or a falsifier. I did not complete it.

## Path and coefficient conditioning (only if the gap were proved)

- P(s) = (1−s)I + sP stays Hermitian with spectrum in [1/2,1], so the conjecture covers the path uniformly.
- ‖dP/ds‖ ≤ 1/2 and ‖d(P⁻¹)/ds‖ ≤ 4·(1/2) = 2. Hence ‖H'‖ and ‖H''‖ are poly(N).
- The classical step computing P = (A†A)^{1/2} to B' bits introduces ‖ΔH‖ ≤ poly(N)·2^{−B'}. The required B' is O(log(poly(N)/gap)), which is polynomial only if the gap is polynomial.
- The Γ(U) step and output sampling are standard.
- None of this is paid until the conjecture is proved.

## What would decide the question

**Falsifier.** An explicit, efficiently described sequence (P_N, φ_N) with:
- ⟨φ_N, M e⟩ = 0, and
- Σ_j ‖D_jφ_N‖²_M / ‖φ_N‖²_M ≤ N^{−ω(1)},
- **proved asymptotically**, for example via closed-form permanent or sector sums.

Exact diagonalization is limited to dim 𝓗_N = C(2N−1, N), roughly N ≤ 10. Fitted numerics prove nothing. L1 and L6 exclude diagonal and block-diagonal candidates, and L7 excludes the coherent |u^N⟩ direction.

**Proof.** The conjecture above, with all quantifiers as stated. Together with L2 (unique zero), L5 (start of path), and the path bounds, it would pay for adiabatic preparation of ψ_P. That would give a poly(N, B, 1/η) sampler from the normalized output.

Until one of these exists, the parent compiler's normalization blocker stands exactly as the contract describes it.
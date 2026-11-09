# Audit of identity (3): C = Fitt_R(Cl(K))·U

## 0. Reduction (proved)

R = Z[ζ_ℓ] = Z[G]/(N) is Dedekind; U is R-torsion-free of rank one (U⊗Q is the augmentation representation), hence invertible; C = R·c ≅ R. Both sides of (3) are R-submodules of U, so (3) holds iff it holds after localizing at every prime 𝔮 of R. Over the DVR R_𝔮, U_𝔮 is free of rank one, C_𝔮 = 𝔮^n U_𝔮 with n = length_𝔮(U/C), and Fitt_{R_𝔮}(Cl(K)_𝔮) = 𝔮^{length_𝔮(Cl(K))} (Fitting ideals commute with localization; over a DVR they equal π^{length}). Therefore

(3) ⇔ for every prime 𝔮 of R: length_𝔮(U/C) = length_𝔮(Cl(K)), with the same ζ↦σ structure on both sides.

The scalar index [U:C] = h_K (from (2)) only gives Σ_{𝔮|q} f_𝔮·length_𝔮(U/C) = v_q(h_K) = Σ_{𝔮|q} f_𝔮·length_𝔮(Cl(K)); it decides a prime q only when R has a single prime above q. I treat (2) ⇒ [U:C]=h_K as an unaudited input (finite control: for p=7, ℓ=3, K=Q(ζ_7)^+, one checks ξ_3·σ_3(ξ_3)=ξ_2, so C=U, consistent with h^+=1; this is not a proof of (2)).

## 1. Primes not above 2 — ACCEPT

**(a) q ∤ 2ℓ (All, Thm 1.2, d=1).** From the supplied definition, δ_{n,1} = N_{Q(ζ_n)/k_n}(1−ζ_n). For K of prime conductor p: if p∤n, k_n = Q and δ_{n,1} = Φ_n(1) ∈ {ℓ′, 1}; if n = p^k m, the distribution relation N_{Q(ζ_{pm})/Q(ζ_p)}(1−ζ_{pm}) = (1−ζ_p)^{∏_{ℓ′|m}(1−Frob_{ℓ′}^{-1})} (and N_{Q(ζ_{p^k})/Q(ζ_p)}(1−ζ_{p^k}) = 1−ζ_p) shows δ_{n,1} is a product of Galois conjugates of α = N_{Q(ζ_p)/K}(1−ζ_p). Since (α) = 𝔓 is G-invariant while the ideals ℓ′O_K are not, the units of D(1) are E∩D(1) = ⟨σ^t(α)/α⟩ = Z[G]·δ, δ = σ(α)/α = c² (roots of unity die under N_{Q(ζ_p)/K} because Σ_{h∈H} h ≡ 0 mod p when |H|>1). So All's C_1 is the totally positive Sinnott group, and E_1/C_1 → U/2C is surjective with kernel of order ≤ 2. For odd q, Syl_q(E_1/C_1) = Syl_q(U/2C) = Syl_q(U/C) because C/2C is 2-torsion. All's ρ are Gal(Q_q(ζ_ℓ)/Q_q)-orbits of nontrivial characters, i.e. exactly the primes 𝔮|q of R, and |ε_ρ M| = |R/𝔮|^{length_𝔮 M}. 𝒞_1 = (1−e_1)Syl_q C(1) = Syl_q Cl(K) since N kills Cl(K). Hypotheses: q ∤ 2|G| ✓; e(p)=ℓ ≤ (p−1)/2 < p−1 ✓; e=1 elsewhere ✓. The theorem (per the abstract) is an equality of orders of ε_ρ-components with the **same** ρ on both sides, so there is no conjugation twist. In particular the odd split characters (q ≡ 1 mod ℓ, orbits of size one, 𝔮_χ = ker(R→Z_q[χ]) distinct from 𝔮_{χ^{-1}}) are handled with the correct action. ACCEPT, conditional on the theorem being as excerpted.

**(b) q = ℓ.** R has the single prime λ = (1−ζ) with residue field F_ℓ; both U/C⊗Z_ℓ and Cl(K)_ℓ are R_λ-modules, lengths = v_ℓ(orders), equal by [U:C] = h_K. ACCEPT given (2).

**(c) q = 2 with 2 inert in R** (ord_ℓ(2) = ℓ−1: ℓ = 3, 5, 11, 13, 19, 29, 37, 53, 59, 61, 67, 83, …): the same scalar argument works; Greither is not needed. ACCEPT given (2). The gate does not use this simplification but it is available.

## 2. Primes above 2 when 2 splits in Z[ζ_ℓ] — the contested case

Relevant ℓ: ord_ℓ(2) < ℓ−1, i.e. ℓ = 7, 17, 23, 31, 41, 43, 47, 71, 73, 79, 89, 97, …; smallest is ℓ = 7 (f = 3, two primes λ_1, λ_2).

**The cancellation, if its premises hold, is formally correct.** 0 → C/2C → U/2C → U/C → 0 is exact and remains exact after ⊗Z_2; C/2C ≅ R/2R ≅ F_2[C_ℓ]/(N) = e′F_2[C_ℓ] = ⊕_{λ|2} R/λ. So (4) with C_{small,2} = 2C_2 gives [U_2/C_2] = [Cl(K)_2] in K_0(finite Z_2[C_ℓ]-mod), hence equal λ-lengths, hence (3) at each λ|2 by §0. Also, since e′-components of E/C_F and U/\bar C_F agree whether or not −1 ∈ C_F, and (R:U)_{χ′} is prime-to-2 for odd degree, those two side issues are har
# Report: polynomial bound on 2-saturation steps at p=2

**Verdict.** The step count is an exact, model-independent quantity: v₂[J(Q₂):H₀]. I split it into three terms. Two are proved polynomial (explicitly: ≤ Ng²+O(g²)+3g with N=2). The third and fourth — the Néron-vs-standard differential index δ and the 2-part of the component group |Φ(F₂)| — are NOT controlled by the near-infinity determinant and require a conductor–discriminant-type theorem at p=2 that I cannot cite as proved for general g. The near-infinity determinant alone cannot control [J:H] because Ω_Ner ⊂ Ω_std always holds in the *wrong* direction for an upper bound. Below: proofs, the precise missing statements, and falsifiers.

## 1. Step count = v₂ of initial index (proved)

Let H₀ = closure⟨P₁,…,P_g⟩ + J(Q₂)[2]. Kummer kernel on H/2H is (H∩2J)/2H. A nonzero class with zero label gives P∈H∩2J∖2H; a half Q has Q∉H (else P∈2H), so H grows by index exactly 2 (2Q∈H). Termination at Kummer rank g+r−1 means H+2J=J and H∩2J=2H, so J/H has odd order. Hence

**steps = v₂[J(Q₂):H₀]**, provided rank_{Z₂}⟨P_i⟩=g (shown in §2 via det≠0).

Obligations used: |J(Q₂)/2J(Q₂)|=2^{g}·|J(Q₂)[2]| (standard, e=1), J(Q₂)[2]≅(Z/2)^{r−1} for odd-degree f (standard).

## 2. Decomposition

Notation: K_m Stoll's higher kernels (w.r.t. the Néron model, which exists but is not given), μ=2, log_Ner: K₂ ≅ (4Z₂)^g. Ω_Ner = Z₂-dual of Lie(J̃) ⊂ H⁰(C,Ω¹); Ω_std = ⊕Z₂·x^k dx/(2y).

**(a) P_i ∈ K_{N+v₂(i)} ⊂ K₂.** Projective Weierstrass model W (weighted) has ∞ smooth on the special fibre: in u=1/x, v=y/x^{g+1}, v²=F(u)=u(1+…) since f monic, ∂_u≠0 mod 2. W^{sm} is smooth over Z₂, so [P−∞] extends to W^{sm}→J̃ (Néron mapping property). The disk parameter v satisfies v=t(1+Σc_m t^{2m}) with v₂(c_m)≥−2m, so for t∈4Z₂, v(v)=v(t). A morphism of smooth Z₂-schemes sends a point ≡0 mod 2^m in a fibre coordinate into K_m. ∎

**(b) Standard determinant (proved exact for N≥2).** Write L_k(t_i) = −t_i Σ_m C_{m,k} t_i^{2m}, C_{m,k}=c_{m−k}(2k+1)/(2m+1). Cauchy–Binet over column sets S: term S has valuation ≥ v(Vandermonde)+2N|λ_S|−2|λ_S| with |λ_S|=ΣS−Σ{0..g−1} (Schur polynomial monomials give 2N|λ|; det C_S gives ≥−2|λ|). For N≥2 all S≠{0..g−1} are strictly larger, so

v₂ det L_std(P) = Ng² + Σ_i v₂(i) + Σ_{i<j} v₂(j²−i²). Nonzero ⇒ rank g. With N=2: ≤ 2g²+O(g²). ∎

**(c) Ω_Ner ⊂ Ω_std (proved modulo two standard facts).** W is normal: special fibre y²=f̄(x) is reduced because f̄ has odd degree hence is not a square; W is a hypersurface (CM), R1 holds. Pullback of a Néron invariant differential along W^{sm}→J̃ is regular on W^{sm}; by normality/S₂ of ω_{W/Z₂} it extends to a global section of ω_{W/Z₂}, whose Z₂-basis is x^k dx/(2y), k<g (standard fact about Weierstrass models; unverified page citation). So A:=change of basis std→Ner has v₂(det A) = −δ with **δ := log₂[Ω_std:Ω_Ner] ≥ 0**.

**(d) Index formula.** Since P_i∈K₂, log_Ner(⟨P_i⟩) has index 2^{v₂det log_Ner(P)−2g} in (4Z₂)^g, and det log_Ner = det A^{−1}·det L_std. Hence

[K₂:⟨P_i⟩] = 2^{v₂det L_std(P) − 2g + δ}.

Using [J:H₀] ≤ [J:K₂]·[K₂:⟨P_i⟩]:

**steps ≤ (v₂|J̃⁰(F₂)| + v₂|Φ(F₂)| + g) + (v₂ det L_std − 2g) + δ.**

Here [J:K₁]=|J̃(F₂)| (Hensel), [K₁:K₂]=2^g (formal group), v₂|J̃⁰(F₂)| ≤ u+2.55a ≤ 2.6g (point counts of unipotent/torus/abelian parts over F₂). Everything is explicitly polynomial **except δ and v₂|Φ(F₂)|.**

## 3. Why the near-infinity determinant cannot control δ or Φ

- The determinant is computed in Ω_std, and (c) gives only Ω_Ner ⊂ Ω_std, i.e. the *true* index is ≥ the std estimate by 2^δ. Non-minimality example (any p, g=1): X=u²x, Y=u³y turns y²=f₀ into Y²=f_u with dX/(2Y)=u^{−1}dx/(2y); the near-∞ point with std parameter t has Néron parameter ut. General g: δ = g²·v₂(u), v₂(disc f_u)=v₂(disc f₀)+4g(2g+1)v₂(u). So steps genuinely grow with δ, and the disk computation sees none of it.
- Φ: elliptic I_{2^k} at 2 has |Φ|=2^k while J[2] is tiny and P∈K₂; steps ≥ k−O(1). Only a discriminant-type bound can control this; nothing local-at-∞ can.

So the two missing theorems are necessary, not artifacts of the proof.

## 4. Missing theorems (precise statements)

**(A) Néron-index bound.** For monic squarefree f∈Z₂[x], deg 2g+1: δ(f) ≤ α·v₂(disc f)+β(g), with α,β polynomial. The scaling family forces α ≥ g/(4(2g+1)) ≈ 1/8. Leads (unverified from memory, no browsing): Liu, *Conducteur et discriminant minimal de courbes de genre 2* (Compositio 1994) relates Weierstrass discriminant, Artin conductor and the index between H⁰(X_min,ω) and H
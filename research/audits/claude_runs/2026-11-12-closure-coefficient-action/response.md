# Scalar normalization of the Sp coefficient module from one fibre: algorithm and obstruction

## 0. Verdict

The scalar normalization reduces to two separate pieces.

1. **Proved part.** Assume the hypothesis **H_link** below: the supplied cover C is, geometrically, the symplectic level cover of the family's actual local system L = R¹f_*μ_ℓ. Then the following hold.
   - The genuine intertwiner A lies on a computable line F_ℓ^*·A0.
   - The Weil-pairing multiplier cuts this line down to ±A_*.
   - One fibre Frobenius over a closed point of odd degree e decides the sign whenever that fibre is *decisive*. Decisive means its characteristic polynomial mod ℓ has a nonzero coefficient in odd degree.
   - This step needs **no torsion frame**. It needs only P_{t0}(T) mod ℓ for the fibre.
   - A full symplectic frame adds only a GSp-conjugacy refinement, which matters only in degenerate Jordan-type cases.
   - Algorithms are given below at small numerical P, and at the original p with charged inputs.

2. **Open part.** Neither a frame nor any fibre-local data certifies H_link. Without H_link, "genuine A" has no meaning relative to the family: every L_{cA0} is a legitimate arithmetic local system.

So the one-fibre computation **removes the scalar**. It also **relocates** the remaining advice into H_link, which belongs to the open native-cover task.

At the original p it also relocates into a supplied, charged F_p-model of the cover's t0-fibre. The residual sign is a quadratic twist. It can vary with p, for example as χ_d(p) when a characteristic-zero model is twisted. It is therefore not a fixed-X constant and must be paid per prime. The one-fibre test pays it.

**Correction to the state file.** "With constant G and constant coefficient module over the working base, A=I" is a convention, not the genuine normalization. Over k0 = F_{q^b} with deck maps defined over k0, the genuine A_b equals λI with λ² ≡ q^b (mod ℓ). So A_b = I is false whenever q^b ≢ 1 (mod ℓ). When q^b ≡ 1 it is still off by an undetermined sign.

This does not affect E or the restriction F_E produced in SURFACE_NATIVE_TORSION_MODULE.md. It does affect every eigenvalue of F_W (§7).

Status labels used below: PROVED (argued here), ASSUMPTION (cited, not reproved), CHARGED INPUT, OPEN.

---

## 1. Objects, quantifiers, conventions

**Base and family.**
- Fix a smooth quintic surface X ⊂ P³ over F_q (q a power of the characteristic P, or q = p), and a Lefschetz pencil of hyperplane sections.
- Fibres are plane quintics, so g = 6 and n = 2g = 12.
- The standard count of singular fibres is d(d−1)² = 80 = r.
- U = P¹ minus the r critical values.
- L is the étale local system on U with fibre J_t[ℓ] and its Weil pairing into μ_ℓ.
- ℓ is an odd prime, ℓ ≠ P, p, and ℓ ∤ |G| relative to the characteristic.

**Cover.** CHARGED INPUT:
- C/P¹ is geometrically connected over F_q and given by a separable model f(t,y) = 0 of degree D = |G|, where G = Sp_n(F_ℓ).
- Deck generators g_1,…,g_s (s = O(n²)) are rational maps with coefficients in k0 = F_{q^b}.
- Each generator comes with a matrix M_i ∈ Sp_n(F_ℓ).
- S = F_ℓ^n carries the standard form J.
- G acts on the left on C.
- F_C denotes the arithmetic q-Frobenius of the F_q-model, acting on F̄_q-points by coordinatewise q-th powers.

Riemann–Hurwitz with tame ramification over r points gives g_C ≤ 1 + |G|(r−2)/2.

**H_link (hypothesis, not certified here).** There is an isomorphism of local systems over U_{F̄_q}

  Θ : C̄ ×^G S → L̄,

using the supplied matrices M_i and the same base coordinate t. Equivalently, C is an F_q-form of a geometric component of the frame scheme of L.

**Frobenius on L_A.** Define

  α(g) := F_C g F_C^{-1}.

This is again a deck transformation because π∘F_C = Frob_{P¹}∘π. An *intertwiner* is A ∈ GL(S) with A g A^{-1} = α(g) for all g ∈ G.

For such A, let L_A = C ×^G S with fibre P_t ×^G S, where (gx, gs) ~ (x, s), and Frobenius

  (x, s) ↦ (F_C x, A s).

This is well defined: (gx, gs) ↦ (α(g)F_C x, α(g)As) ~ (F_C x, As).

On V = J_C[ℓ] we have F_V g_* = α(g)_* F_V. Hence the map F_W(φ) = F_V φ A^{-1} preserves W = Hom_G(S,V):

  F_V φ(A^{-1}gs) = F_V φ(α^{-1}(g)A^{-1}s) = g F_V φ(A^{-1}s).

So F_W is the Frobenius of Hom_G(S,V) with S carrying A. This is the formula used in the state file.

**Frame model (reference only).** Let Fr_t be the set of linear isomorphisms c : S → J_t[ℓ] with e(cx, cy) = ζ^{xᵀJy}, for a fixed primitive ζ. The group acts by g·c = c∘g^{-1}. The arithmetic Frobenius sends c to Fr_J∘c, which has pairing ζ^q.

For h ∈ GSp_n(F_ℓ) with multiplier mult(h) ≡ q (mod ℓ), set σ_h(c) = Fr_J∘c∘h^{-1}. Then σ_h preserves the ζ-component:
- e(Fr c h^{-1}x, Fr c h^{-1}y) = ζ^{q·q^{-1}xᵀJy}.
- α_h(g) = h g h^{-1}, since σ_h(g·c) = Fr c g^{-1}h^{-1} = (hgh^{-1})·σ_h(c).

Finally, (c, s) ↦ c(s) identifies L_h with L arithmetically: (σ_h c, hs) ↦ Fr c h^{-1}hs = Fr(c(s)).

This is the precise sense in which "Frobenius changes the Weil pairing by q" forces the genuine A to have multiplier q.

**Cyclotomic components.** If q ≢ 1 (mod ℓ), no geometric component of Fr is an F_q-subscheme: F_q sends the ζ-component to the ζ^q-component. A geometrically connected F_q-model exists only as a twisted form σ_h. Then α is outer exactly when q is a nonsquare mod ℓ.

If instead one is handed a component defined only over F_q(μ_ℓ) = F_{q^o}, then only F_q^o acts. The original F_q-action on W requires choosing a twist h, which is the same problem again.

---

## 2. Intertwiner line and multiplier (PROVED)

**Lemma 2.1.** End_G(S) = F_ℓ, and the F_ℓ-span of G is End(S).

*Proof.*
- Let T_v(x) = x + ⟨v,x⟩v be the symplectic transvection.
- If X commutes with T_v, then ⟨v,x⟩Xv = ⟨v,Xx⟩v for all x.
- Choosing x with ⟨v,x⟩ = 1 gives Xv ∈ F_ℓ v for every v, so X is scalar. This proves absolute irreducibility.
- The image of F_ℓ[G] is a primitive finite-dimensional algebra with commutant F_ℓ. By the density theorem it is End(S). ∎

**Lemma 2.2.** The intertwiner space {A : A M_i = M(α(g_i)) A for all i} is one-dimensional. A nonzero solution A0 is invertible and lies in GSp, with multiplier μ0. The intertwiners are exactly F_ℓ^*·A0.

*Proof.*
- One-dimensionality: two intertwiners differ by an element of End_G(S) = F_ℓ.
- Existence: α is conjugation by h in the model of §1. For an abstract C, α is an automorphism of G that preserves the isomorphism class of S under H_link, because S∘α ≅ S via Frobenius transport of Θ.
- Similitude: B(x,y) = (A0x)ᵀJ(A0y) is G-invariant because α(g) ∈ Sp. G-invariant bilinear forms form Hom_G(S,S^∨) ≅ F_ℓ, so B = μ0 J. ∎

**Proposition 2.3 (genuine A exists and is unique under H_link).**
1. There is a unique κ ∈ F_ℓ^* with L_{κA0} ≅ L arithmetically.
2. mult(κA0) ≡ q, i.e. κ²μ0 ≡ q (mod ℓ).

*Proof of existence.*
- Let ρ0 and ρ be the monodromy representations of π1(U_{F_q}) for L_{A0} and L. Let φ be a Frobenius lift, and identify both on geometric π1 by Θ.
- For geometric γ, X := ρ(φ)^{-1}Θρ0(φ)Θ^{-1} commutes with ρ(γ). This follows by expanding ρ(φγφ^{-1}) both ways.
- By Lemma 2.1, X is a scalar κ^{-1}.
- Note L_{cA0} = L_{A0} ⊗ χ_c, where χ_c(Frob_q) = c, since the Frobenius (x,s) ↦ (F_C x, cA0 s) is c times that of L_{A0}.
- Hence ρ ≅ ρ0 ⊗ χ_κ.

*Proof of uniqueness.* An arithmetic isomorphism L_{cA0} → L_{c'A0} is a geometric automorphism, hence a scalar, and must intertwine cF with c'F. So c = c'.

*Proof of the multiplier.* At a rational t0 the isomorphism Θ_{t0} is a similitude, since it pulls back the Weil pairing to a G-invariant form. So it preserves multipliers. Fr_J has multiplier q, and the Frobenius of L_{κA0} in x-coordinates is γ^{-1}κA0 with γ ∈ Sp (§3). ∎

**Corollary 2.4.** Under H_link:
- q/μ0 is a square mod ℓ; this is a falsifier if it fails.
- The candidates are exactly ±A_*, where A_*² is determined.
- The residual ambiguity is the unramified quadratic twist L ↔ L ⊗ χ_{−1}. This is the central deck element −1 ∈ G changing the F_q-structure of C: replacing F_C by (−1)F_C leaves α unchanged.

So the conjugation automorphism α alone can never fix the sign. **Without H_link the multiplier constraint is unavailable, and the ambiguity is the full F_ℓ^*.**

---

## 3. One-fibre formula (PROVED)

**Lemma 3.1.** Let t0 be a closed point of U of degree e, unramified for C, with smooth fibre. Take x ∈ P_{t0}, and let γ_x ∈ G be defined by F_C^e x = γ_x x. Then the Frobenius of L_A at t0 is represented, in the basis given by x, by

  N_x(A) = γ_x^{-1} A^e,

where A^e is the composite (F_C^e acts on L_A by A^e). Its G-conjugacy class does not depend on x.

*Proof.*
- (x,s) ↦ (F_C^e x, A^e s) = (γ_x x, A^e s) ~ (x, γ_x
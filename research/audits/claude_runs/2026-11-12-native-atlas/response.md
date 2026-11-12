# Review: exact native Jacobian bridge for a smooth (5,3) complete-intersection curve over K=Q(t) via Anderson's abeliant construction

## Verdict (one line)
**Conditional construction, not refuted.** The interpolation-then-expand descent route survives attack: I prove below that every nonzero K-expansion of an extension-defined chart is a valid chart for the same projective law and that coverage is inherited. The bridge is a deterministic poly(B+T) (in fact linear-in-(B+T) with format constants) algorithm **provided** three explicitly listed obligations are discharged (Anderson §2 explicit abeliant formulas, fixed-variable radicalization, scheme-level identification with Jac). All format constants are explicit but astronomically large; this is an existence/pipeline bridge, not a practical object, and nothing here transfers to growing genus.

## 0. Numerics (all checked from the format)
- C ⊂ P³, CI of degrees (5,3): deg 15, K_C = 4H, g = 31. Anderson needs deg E ≥ 2g+1 = 63; **E = 4H (60) fails; E = 5H (75) is minimal.**
- E := 5·H₀, H₀ = C ∩ {x₀=0}. n = ℓ(E) = 75−30 = 45 (≥2 ✓). dim L(2E)=120, L(4E)=270, L(8E)=570.
- Hypotheses of Prop 4.3.3 / Lemma 4.3.5 / Prop 4.3.7 / Lemma 4.4.4 with G=2E, 4E: ½degG−degE = 75 ≥ 2g = 62 and > 2g−2 = 60; Mumford (50) needs 75 ≥ 63 ✓.
- Ambient space: by (42) and Mumford, Z₁₂ ∈ V := L(2E)⊗L(2E)⊗L(2E)⊗L(4E)^{⊗43}⊗L(2E) (slots 0,1,2,3..n,n+1); dim V = 120⁴·270⁴³. Working space for charts: V' = L(4E)⁴⊗L(8E)^{⊗43}.
- Degrees: ∆ (47) is a product of 2n−1 = 89 entries ⇒ degree 89 in Z; (46) homogeneous forces deg(abel) = 2n = 90 in the array (I deduce this from k-proportionality invariance of (46)/(47); the explicit formula is in §2, not supplied — see O1).

## 1. Construction (steps, each tagged)

**A. Riemann–Roch spaces over K (PROVED, standard).** CI is projectively normal, so L(mE) = L(5mH₀) = {q/x₀^{5m} : q ∈ S_{5m}} / (F₅S_{5m−5}+F₃S_{5m−3}). K-bases and multiplication tables L(aE)×L(bE)→L((a+b)E) for a+b ≤ 8·90 are constant-size linear algebra over Q(t) (fraction-free Bareiss). No K-point of C used.

**B. E over K, auxiliary linear form (PROVED).** H₀ need not be reduced; E = Σ5m_P P is effective and K-rational. Choose a linear form ℓ nonvanishing on supp H₀ (≤15 geometric points; a K-rational ℓ exists among a 16⁴ grid since each point excludes one hyperplane in the dual space); test deterministically.

**C. Compression functional ρ over K (PROVED from Lemmas 4.3.4–4.3.5).** O_E := (S/(F₅,F₃,x₀⁵))_{20} is the coordinate algebra of the 0-dim CI scheme E (Hilbert function constant = 75 for d ≥ 10), Gorenstein, so Hom_K(O_E,K) is free of rank 1 over O_E; a generator σ (perfect pairing (a,b)↦σ(ab)) is found deterministically on a constant grid with a determinant test. With f_G = (x₀/ℓ)^{20}, ρ(q/x₀^{20}) := σ(class of q in O_E) (= σ(f_G·x), since f_G x = q/ℓ^{20}). Lemma 4.3.5's proof uses only perfectness of (51), so ρ is an E-compression functional on L(4E), defined over K, simultaneously good for all D.

**D. Identity, inversion (PROVED).** X₀ = u·uᵀ, u a K-basis of L(E), is a 2E-form representing E (D=0); Z₀ := abel(X₀^{(0)},…,X₀^{(n+1)}) ∈ V is a K-point. Inversion: Z ↦ h0|n+1i_*Z = Zᵀ (Lemma 4.4.3, catalogue (4)): a K-linear coordinate permutation of V.

**E. Finite specialization set detecting all nonzero discriminants (PROVED, no quasi-compactness).** Per slot ∆ ∈ L(4·89·E) = L(356E) (each of the 89 factors contributes ≤ L·L per slot by (23) and slot swaps; slot i=j is empty). A nonzero f ∈ L(356E) has ≤ 26700 zeros. Let π = (x₀:ℓ): C → P¹ (degree 15; the line {x₀=ℓ=0} misses C by B). Ramification degree 2·15+2g−2 = 90, so ≤ 90 branch values. Let Σ := π⁻¹({1,…,1871}) ⊂ (C∖supp E)(K̄): ≥ 1781 reduced fibres ⇒ |Σ| ≥ 26715 > 26700. Evaluation L(356E) → K̄^Σ is injective, hence so is ⊗_{ℓ=1}^{46}L(356E) → K̄^{Σ^{46}} (tensor product of injective maps). **Therefore for every Jacobi matrix Z some s ∈ Σ^{46} has ∆_Z‖s ≠ 0**, and the open sets J_s cover J geometrically. Branch values are detected deterministically (trace-form determinant of the degree-15 fibre algebra).

**F. Charts (SOURCE Lemma 4.4.5 + PROVED supplement).** For s,s' ∈ Σ^{46}, and a choice (P,Q) of ordered 75-subset and 45-subset of row and column indices of the 2025×2025 Kronecker product (only these choices matter: permutations within blocks change z by signs or k-equivalence, hence Z'' by a scalar), define Φ_{s,s',P,Q}(Z,Z') := proj_V(Z''₁₂) computed in V'. Supplement (needed because Anderson's (ii) states its premise only as "Z''≠0"): z carries the prefactor ∆‖s·∆'‖s'·det ρa and is a block of a rank ≤1 matrix; abel is homogeneous of positive degree; so Z''≠0 ⇒ all prefactors nonzero and z k-general (Prop 3.4.3) ⇒ (Lemma 4.4.4(ii)) z ∈ L(2E)^{n×n} ⇒ Z'' ∈ V. Hence proj_V(Z'') ≠ 0 ⇔ Z'' ≠ 0 ⇔ chart valid, and then it represents Z_{D+D'}. **Do not project z to L(2E) before abel** (would create nonzero wrong outputs; REFUTED variant). Completeness at every geometric pair: by E, choose s,s' with nonzero discriminants; by Lemma 4.4.4(i) some (P,Q) makes z k-general. Bidegree of each chart: z has degree 89+75+75+1+75 = 315 in each of Z,Z'; Z'' has bidegree (90·315, 90·315) = (28350, 28350).

**G. Descent of charts to K (PROVED — the attacked route).** Charts have coefficients in K(s,s') (ρ, bases, multiplication tables, abel are over K; abel over Q by O1). Let K' = K(s,s') (char 0 ⇒ separable), e₁..e_d a K-basis, Φ_s = Σ e_i Φ_i with Φ_i over K. For σ ∈ Hom_K(K',K̄): σ(Φ_s) = Φ_{σ(s),σ(s')} because all other data are K-rational, and (σ(s),σ(s')) is again a geometric tuple in (C∖supp E)^{92}, so σ(Φ_s) is valid by Lemma 4.4.5 applied to C_{K̄}. The matrix (σ(e_i)) is invertible (Dedekind), so Φ_i = Σ_σ c_{iσ} σ(Φ_s) with c_{iσ} ∈ K̄. At a geometric pair with fixed representative w of Z+Z', each σ(Φ_s)(Z,Z') = λ_σ w (λ_σ possibly 0), hence Φ_i(Z,Z') = (Σ c_{iσ}λ_σ)·w: **nonzero expansions define the same projective addition.** Coverage: Φ_s(Z,Z') ≠ 0 ⇒ some Φ_i(Z,Z') ≠ 0. No Galois-equivariance of the group law is needed. Equivalent reduced-algebra version: expand in a K-basis of O_Σ^{⊗92} (reduced since fibres reduced, char 0); the evaluation matrix has full row rank, same conclusion. **Explicit missing condition for the naive route:** the expansion basis must come from a separable field/reduced algebra and every non-s datum must be K-rational; with a non-reduced fibre algebra or a K'-dependent ρ the conjugation step fails. (Also REFUTED: specializing at K-points of C — C(K) may be empty.)

**H. Presentation.** Projective: J ⊂ P(V) by (43)–(47) expanded in tensor bases (equations of degree ≤ 90, finitely many, format-constant count); affine patches J_s = {∆‖s ≠ 0}, s ∈ Σ^{46}, isomorphic (Prop 3.5.5, Remark 3.7.7) to U_s ⊂ L(2E)^{45×45} (243000 coordinates; 2×2 minors expanded in L(4E) = quadrics; normalization (32)–(33) linear), with explicit rational gluing. Both are set-theoretic; radicalization is O2.

## 2. Cost / coefficient growth (PROVED, linear)
All steps are a format-bounded number c_fmt of ring operations in Q(t) on constant-size arrays. Recurrences: sum (δ,h)→(δ,h+1); product →(2δ, 2h+log(δ+1)); c×c determinant →(cδ, c·h + c·log c + c·log(δ+1)) (Hadamard). Constant depth ⇒ t-degree ≤ c₁T, height ≤ c₂(B+T+1). Radicalization (O2) with a bounded operation count adds a further constant factor. Counts: charts over K ≤ [K':K]·|Σ|^{92}·(C(2025,75)C(1950,45))² — explicit, astronomically large but format-only.

## 3. Proof obligations (exact)
- **O1 (source gap).** Packet lacks Anderson §2 (lines 70–560): the polynomial definition of abel and ∆, identities (3),(4),(8),(10),(11),(14)–(16),(19)–(23), and the statement that abel is a universal polynomial over Z (needed for "polynomial rule for any commutative ring" and for σ(Φ_s)=Φ_{σs}). Degree 2n is my deduction from (46)–(47), to be checked against §2.
- **O2 (radicality).** Reducedness of the Jacobi/U_s schemes is not proved by Anderson; a deterministic radical algorithm in a fixed number of variables over Q(t) with bounded operation count is required (standard Gröbner-based methods exist; none is in the packet, so this is an import to be verified, not a quoted result).
- **O3 (identification).** Lemma 4.4.5/Thm 4.4.6 give an algebraic group bijective to Pic⁰(C_K̄). For "the Jacobian over K" one needs: Abel map Pic⁰_{C/K} → J_red is a K-morphism (Galois-equivariance via abel over Q; algebraicity in families), then bijective morphism of smooth varieties in char 0 ⇒ isomorphism (ZMT). Downstream users needing only a K-group with Galois-compatible bijection to Pic⁰(K̄) can skip this.
- **O4.** Mumford's theorem (50) and CI projective normality are accepted as standard sources (not in packet).

## 4. Falsifiers / finite controls
- Any geometric pair (Z,Z') and descended Φ_i with Φ_i(Z,Z') ≠ 0 not proportional to Z_{D+D'}: refutes G.
- Any Jacobi Z with ∆_Z‖s = 0 for all s ∈ Σ^{46}: refutes E (would contradict injectivity — check the per-slot bound 356).
- A nonzero Z'' computed in V' with a component outside V: refutes the supplement in F (hence Lemma 4.4.4(ii) usage).
- abel inhomogeneous or abel(0) ≠ 0: breaks F's "Z''≠0 ⇒ valid".
- Small-genus control (g=1, E of degree 3, n=3; or g=2): compute J, Z₀, two Σ-charts and their K-expansions, verify agreement with a known group law; failure refutes the pipeline, success proves nothing beyond the control.

## 5. Summary table
| Item | Status |
|---|---|
| E=5H satisfies all Anderson hypotheses; E=4H does not | PROVED |
| K-rational RR spaces, ρ, identity, inversion | PROVED |
| Finite set Σ^{46} detecting all nonzero ∆ (|Σ|≥26701) | PROVED |
| Finite atlas covering every geometric pair | PROVED modulo O1 |
| Descent of charts to K with same law + coverage | PROVED |
| Radical patch ideals | OBLIGATION O2 |
| J ≅ Jac_{C/K} as K-group scheme | OBLIGATION O3 |
| poly(B+T) deterministic with format constants | PROVED (linear), constants explicit but astronomical |
| Any speedup/hardness implication | NONE claimed |
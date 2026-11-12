# Verdict

**The uniform atlas claim is VERIFIED** (conditional only on Theorem 3.1.2 as supplied). I found no failing step; every assertion in MERKL_LOG_COLLISION_ATLAS.md that was marked CHECK (packing/coverage at clusters and hole boundaries, enlarged branch charts, density on the full unit disk, transitions on full overlaps) goes through with explicit absolute constants. The resulting bound, with r₁ = 3/4, is

  sup_{Y×Y∖Δ} gr_Y ≤ C_r · d³(d + L), with C_r ≤ 2·10¹⁰ · r (not optimized),

for every finite holomorphic π: Y → P¹(C) of degree d ≥ 2, Y compact connected of genus g ≥ 1, branched only inside an r-point set B. Below is a complete argument; constants are chosen for verifiability, not sharpness.

What is **not** established here: Bruin's appendix (proof of Theorem 3.1.2) is taken as the supplied input and not re-derived; nothing arithmetic (Faltings height, finite places, divisor heights, CRT) follows.

---

## 0. Conventions and normalizations

- **Sphere and coordinates.** P¹(C) = unit sphere S² ⊂ R³ via stereographic projection. For x ∈ P¹, φ_x denotes a unitary Möbius coordinate (element of PSU(2)) with φ_x(x) = 0; it is determined up to rotation, and |φ_x(y)| is well defined. Writing θ(x,y) ∈ [0,π] for the great-circle (angular) distance, one has |φ_x(y)| = tan(θ(x,y)/2); in particular |φ_x(y)| = |φ_y(x)|. Define τ(x,y) := |φ_x(y)|.
- **Elementary facts used** (all on [0,π/2] for θ): (i) θ/2 ≤ tan(θ/2) ≤ θ; (ii) d/dθ tan(θ/2) ∈ [1/2, 1]; (iii) tan u ≤ u(1+tan²u); (iv) a unitary Möbius map g with g(a) = 0 is g(ζ) = e^{iα}(ζ−a)/(1+āζ), so |g′(ζ)| = (1+|a|²)/|1+āζ|²; (v) the area of an angular ball of radius σ on S² is 2π(1−cos σ) ∈ [3σ², πσ²] for σ ≤ 0.7.
- **Separation.** δ := min(1, min_{b≠b′∈B} τ(b,b′)), L := 1 + log(1/δ). (The chordal normalization in the claim differs by a factor ≤ 2, i.e. by an additive constant ≤ log 2 in L; absorbed in C_r.)
- **Fixed parameters.** r₁ = 3/4, ε = 1/20, h = δ/200, hole scale ρ₀ := h r₁^d.
- **Distance to B and Whitney radius.** m(x) := min(1/2, τ(x,B)) with τ(x,B) := min_{b∈B} τ(x,b); ρ(x) := ε·m(x) ≤ 1/40.
- **Canonical measure.** With ω₁,…,ω_g a basis of H⁰(Y,Ω¹) orthonormal for (i/2)∫ω_ν∧ω̄_μ = δ_{νμ}, μ_Ar = (i/2g)Σ_ν ω_ν∧ω̄_ν. In a chart z with ω_ν = f_ν dz: μ_Ar = i F dz∧dz̄ with **F = (1/2g)Σ_ν|f_ν|²**. Check of mass: i dz∧dz̄ = 2 dA, so ∫μ_Ar = (1/g)Σ∫|f_ν|²dA = 1. (μ_Ar is convention-independent, being 1/g times the trace of the Bergman kernel; only "mass 1" is used.)
- d ≥ 2 is automatic (d = 1 forces g = 0); r ≥ 3 is automatic by Riemann–Hurwitz but only r ≥ 2 is used.

## 1. Three elementary lemmas

**Lemma A (Lipschitz comparability of ρ).** If t := τ(x,y) ≤ 1.1(ρ(x)+ρ(y)), then ρ(y) ≤ (5/4)ρ(x) and ρ(x) ≤ (5/4)ρ(y).

*Proof.* t ≤ 0.055, so θ(x,y) ≤ 2t ≤ 0.11. WLOG m(x) ≤ m(y); if m(x) = 1/2 done. Else m(x) = τ(x,b) ≤ 1/2 for some b, so θ(x,b) ≤ 2 arctan(1/2) < 0.93 and θ(y,b) ≤ 1.04 < π/2. By fact (ii), τ(y,b) ≤ τ(x,b) + θ(x,y) ≤ m(x) + 2t, hence m(y) ≤ m(x)+2t and |ρ(x)−ρ(y)| ≤ 2εt ≤ 0.11(ρ(x)+ρ(y)); thus ρ(y) ≤ (1.11/0.89)ρ(x) < (5/4)ρ(x), symmetrically. ∎

**Lemma B (branch disks).** Put D_b := {|φ_b| < 2h}. (a) The D_b, b ∈ B, are pairwise disjoint. (b) If τ(x,b) < 1.2h for some b ∈ B, then τ(x,B) = τ(x,b).

*Proof.* (a) If y ∈ D_b ∩ D_{b′}, then θ(b,b′) ≤ θ(b,y)+θ(y,b′) < 4·(2h) = δ/25, so τ(b,b′) = tan(θ/2) ≤ θ < δ, contradicting the definition of δ (δ ≤ 1 keeps angles ≤ π/2). (b) If τ(x,b′) ≤ τ(x,b) < 1.2h for b′ ≠ b, then θ(b,b′) < 2(2·1.2h) = 4.8h < δ/40, so τ(b,b′) < δ, contradiction. ∎

**Lemma C (lifting).** If D ⊂ P¹ is a coordinate disk (simply connected) with D ∩ B = ∅, then π^{-1}(D) is a disjoint union of exactly d components, each mapped biholomorphically onto D by π.

*Proof.* π: π^{-1}(P¹∖B) → P¹∖B is an unramified d-sheeted covering; a covering of a simply connected space is trivial. ∎

## 2. The charts

**(B) Branch charts.** For b ∈ B and each connected component V of π^{-1}(D_b): π|_V: V → D_b is proper, ramified at most over 0, of degree e = e_V ∈ [1,d]. V∖π^{-1}(0) → D_b∖{0} is a connected finite covering of a punctured disk, hence isomorphic to u ↦ u^e; filling the puncture, V is a disk with a coordinate u, u^e = φ_b∘π. Set w := h^{-1/e}u, so

  φ_b∘π = h·w^e on V, w: V ≅ {|w| < 2^{1/e}} =: V⁺.

Chart: U_V := {|w| < 1} (= points of V over |φ_b| < h), z_V := w. Since V is a disk and w is a global coordinate on it, z_V: U_V → unit disk is a biholomorphism (Definition 3.1.1(1)). Each V contains exactly one point over b, so the number of branch charts is Σ_b #π^{-1}(b) ≤ rd.

**Inner disk:** U_V^{r₁} = {|w| < r₁} = points of V over |φ_b| < h r₁^{e} ⊇ points of V over |φ_b| < ρ₀ (as e ≤ d, r₁ < 1).

**(W) Whitney charts.** E := {x ∈ P¹ : τ(x,B) ≥ ρ₀}. Choose S ⊂ E maximal with respect to: for s ≠ s′ ∈ S, τ(s,s′) ≥ (3/8)·min(ρ(s),ρ(s′)) (Zorn/compactness; finiteness is proved in §3). For s ∈ S set

  D_s := {|φ_s| < ρ(s)}, D_s⁺ := {|φ_s| < (3/2)ρ(s)}.

D_s⁺ ∩ B = ∅, because for b ∈ B, τ(s,b) ≥ m(s) = ρ(s)/ε = 20ρ(s) > 1.5ρ(s). By Lemma C, π^{-1}(D_s⁺) has d components Ṽ, each ≅ D_s⁺; chart U := Ṽ ∩ π^{-1}(D_s), z := (φ_s∘π)/ρ(s), a biholomorphism onto the unit disk, extending to Ṽ ≅ {|z| < 3/2}. Number of Whitney charts: d·|S|.

## 3. Dyadic packing count (uniform in clusters)

**Separation ⇒ disjoint angular balls.** Let σ(s) := (3/32)ρ(s) and A_s := angular ball of radius σ(s) about s. Claim: the A_s are pairwise disjoint. If y ∈ A_s ∩ A_{s′}, then θ(s,s′) < σ(s)+σ(s′) = (3/32)(ρ(s)+ρ(s′)), so τ(s,s′) ≤ θ(s,s′) < 0.094(ρ(s)+ρ(s′)) ≤ 1.1(ρ(s)+ρ(s′)); Lemma A gives max(ρ(s),ρ(s′)) ≤ (5/4)min, hence the net condition gives τ(s,s′) ≥ (3/8)min ≥ (3/8)(4/5)max ≥ 0.15(ρ(s)+ρ(s′)) > 0.094(ρ(s)+ρ(s′)), contradiction.

**Scales.** For k ≥ 1 let S_k := {s ∈ S : 2^{-k} ≤ m(s) < 2^{-k+1}}. For s ∈ S_k, σ(s) ≥ (3/32)ε2^{-k} = (3/640)2^{-k}, so area(A_s) ≥ 3σ(s)² ≥ 3(3/640)²4^{-k}.
- k = 1: ΣA_s ⊂ S², so |S₁| ≤ 4π/(3(3/1280)²) < 8·10⁵.
- k ≥ 2: m(s) = τ(s,b_s) < 2^{-k+1} ≤ 1/2 for some b_s, so θ(s,b_s) ≤ 2τ < 2^{-k+2}, and A_s ⊂ Ball_θ(b_s, 5·2^{-k}), of area ≤ 25π4^{-k}. Summing over the r possible b_s (overlapping caps only help the bound): |S_k|·3(3/640)²4^{-k} ≤ 25πr4^{-k}, i.e. |S_k| ≤ 1.2·10⁶ r.

This per-scale bound is **independent of clustering**: it uses only the union of r caps, not disjointness of caps.

**Number of scales.** s ∈ E ⇒ m(s) ≥ ρ₀ = h r₁^d, so S_k = ∅ unless 2^{-k+1} > ρ₀, i.e. k ≤ 1 + log₂(200/δ) + d log₂(4/3) ≤ 8.7 + 1.45 log(1/δ) + 0.42d. Hence the number of nonempty scales K ≤ 10(L + d) (using L ≥ 1).

**Total:** |S| ≤ 1.2·10⁶ r · 10(L+d), and

  **N ≤ rd + d|S| ≤ 1.3·10⁷ · r · d(d + L).**

## 4. Covering property (Definition 3.1.1(2))

Let y ∈ Y, x = π(y).
- If τ(x,B) < ρ₀: pick b with τ(x,b) = |φ_b(x)| < ρ₀ < 2h; y lies in some component V of π^{-1}(D_b), and |w(y)|^e = |φ_b(x)|/h < r₁^d ≤ r₁^e, so y ∈ U_V^{r₁}.
- If τ(x,B) ≥ ρ₀: x ∈ E. By maximality of S, either x ∈ S or some s ∈ S has τ(s,x) < (3/8)min(ρ(s),ρ(x)) ≤ (3/8)ρ(s) < r₁ρ(s); in both cases x ∈ D_s^{r₁} := {|φ_s| < r₁ρ(s)}, and y lies in the r₁-inner part of the Whitney chart on the component of π^{-1}(D_s⁺) containing y.

Hence the U_j^{r₁} cover Y. (Hole boundaries are handled exactly: the base hole radius ρ₀ is dictated by the worst ramification index e ≤ d, which is why r₁^d, not r₁^e, appears.)

## 5. Canonical density (Definition 3.1.1(4)): c₁ ≤ 0.332 d²

Let (U,z) be a chart whose coordinate extends to an embedded disk U⁺ ≅ {|z| < R} in Y (R = 3/2 for Whitney charts, R = 2^{1/e} for branch charts; embedding holds since w resp. the lifted φ_s is a biholomorphism of the whole component). For p ∈ U, the Euclidean z-disk D(p, R−1) lies in U⁺. By subharmonicity of |f_ν|²,

  |f_ν(p)|² ≤ (1/(π(R−1)²)) ∫_{D(p,R−1)} |f_ν|² dA ≤ (1/(π(R−1)²)) ∫_{U⁺} |f_ν|² dA ≤ 1/(π(R−1)²),

the last step because ∫_{U⁺}|f_ν|²dA = (i/2)∫_{U⁺}ω_ν∧ω̄_ν ≤ (i/2)∫_Y ω_ν∧ω̄_ν = 1 (U⁺ is embedded, so no multiple counting). Summing over ν and dividing by 2g:

  F(p) ≤ 1/(2π(R−1)²), **uniformly on the whole unit disk U**, with F ≥ 0 trivially.

- Whitney: R−1 = 1/2 ⇒ F ≤ 2/π < 0.64.
- Branch, index e: R−1 = 2^{1/e}−1 = e^{(ln2)/e}−1 ≥ (ln 2)/e, so F ≤ e²/(2π(ln2)²) ≤ 0.332 e² ≤ 0.332 d².

Thus c₁ := 0.332 d² works (d ≥ 2 gives 0.332d² ≥ 1.33 > 0.64). The enlarged branch disk is indeed what makes the bound hold up to |w| = 1; this confirms the memo's "ENTIRE unit disk" remark.

## 6. Transitions on all overlaps (Definition 3.1.1(3)): M = 26 d (4/3)^d, log M ≤ 4d

Both directions |dz_j/dz_{j′}| and |dz_{j′}/dz_j| are bounded, as required for all ordered pairs.

**(B–B).** Components over the same b are disjoint; for b ≠ b′, D_b ∩ D_{b′} = ∅ (Lemma B(a)), so their preimages are disjoint. No overlap.

**(W–W).** Charts z = φ_s∘π/ρ(s), z′ = φ_{s′}∘π/ρ(s′). A common point y of the two unit charts gives θ(s,s′) < 2ρ(s)+2ρ(s′) ≤ 0.1, so by fact (iii) τ(s,s′) ≤ (ρ(s)+ρ(s′))(1+0.0025) ≤ 1.1(ρ(s)+ρ(s′)); Lemma A gives ρ(s′)/ρ(s) ≤ 5/4. On the overlap (which lies in a single sheet), z = g(ρ(s′)z′)/ρ(s) with g = φ_s∘φ_{s′}^{-1} ∈ PSU(2), g(a) = 0, a = φ_{s′}(s), |a| ≤ 0.055, and the argument ζ satisfies |ζ| < ρ(s′) ≤ 1/40. By fact (iv), |g′(ζ)| ∈ [0.99, 1.02]. Hence |dz/dz′| = (ρ(s′)/ρ(s))|g′| ≤ (5/4)(1.02) < 1.3, symmetrically. (Capped vs. uncapped radii are covered by Lemma A automatically, since m includes the cap.)

**(W–B).** Chart z_W = φ_s∘π/ρ(s) on a sheet over D_s, branch chart w on V ⊂ π^{-1}(D_b) with U_V = {|w|<1} ↔ |φ_b| < h. If the unit charts meet, D_s ∩ {|φ_b|<h} ≠ ∅, so as in (W–W) τ(s,b) < 1.1(ρ(s)+h) ≤ 1.1h + 0.055m(s). If the nearest branch point to s were b′ ≠ b, then m(s) ≤ τ(s,b) gives m(s) < 1.17h, contradicting Lemma B(b). Hence t := τ(s,b) = m(s), ρ(s) = εt, and

  ρ₀ = h r₁^d ≤ t < 1.17h < 2h (s ∈ E; and t < 1.1h/(1−0.055)).

Let y be in the overlap, x = π(y). Then τ(s,x) < ρ(s) = εt, so θ(s,x) ≤ 2.02εt, and by fact (ii) |τ(x,b) − t| ≤ 0.101t. Since τ(x,b) = h|w(y)|^e:

  0.899 t ≤ h|w|^e ≤ 1.101 t, hence |w|^e ≥ 0.899 r₁^d, so **|w| ≥ 0.899^{1/e} r₁^{d/e} ≥ 0.89·(3/4)^d** on the whole overlap.

(This is exactly the memo's "small relative radius keeps |w| ≥ c r₁^{d/e} ≥ c r₁^d".) Now z_W = g(φ_b)/ρ(s) with g = φ_s∘φ_b^{-1}, g(φ_b(s)) = 0, |φ_b(s)| = t < 2h ≤ 1/100, |φ_b| < 1.2h on the overlap, so |g′| ∈ [0.99, 1.01]. By the chain rule dφ_b = h e w^{e−1}dw:

  |dz_W/dw| = |g′| · h e |w|^{e−1}/(εt) = |g′| e (h|w|^e)/(ε t |w|) ≤ 1.01·1.101·20·e/(0.89(3/4)^d) ≤ 26 e (4/3)^d ≤ 26 d (4/3)^d,
  |dw/dz_W| = εt|w|/(|g′| e h|w|^e) ≤ (1/0.99)(1/20)(1/0.899)|w|/e ≤ 0.06.

**Conclusion.** M := 26 d (4/3)^d ≥ 1 bounds every |dz_j/dz_{j′}| on every U_j ∩ U_{j′}. For d ≥ 2, log M = log 26 + log d + d·log(4/3) ≤ 3.26 + 0.37d + 0.29d ≤ 4d. M is exponential in d but, as the memo notes, Theorem 3.1.2 charges only log M.

## 7. Assembling Theorem 3.1.2

With r₁ = 3/4: 330/(1−r₁)^{3/2}·log(1/(1−r₁)) = 330·8·log 4 < 3660; 13.2c₁ ≤ 4.39d²; log M ≤ 4d. Hence

  sup gr_Y ≤ n(3660 + 4.39d² + 4d) ≤ 922·n·d² (d ≥ 2),

and with n = N ≤ 1.3·10⁷ r d(d+L):

  **sup_{Y×Y∖Δ} gr_Y ≤ 1.2·10¹⁰ · r · d³(d + L).**

The same right-hand side bounds |gr_Y(x,y) − log|z_j(x)−z_j(y)|| on each U_j^{r₁} (second statement of Theorem 3.1.2). All constants are absolute; nothing depends on monodromy, irreducibility of a defining equation, real structure, or any supplied charts. The dependence on branch positions is only through L = 1 + log(1/δ) and enters only via the chart count (number of dyadic scales); c₁ and M are independent of δ.

Each memo assertion checked: branch chart extension to |w|<2^{1/e} ✓; ≤ rd branch charts ✓; Whitney doubled disks avoid B ✓ (factor 20 margin); O_r(1) disks per scale, uniformly in clusters ✓; smallest scale ≍ h r₁^d ✓; d disjoint lifts with 3/2 extension ✓; c₁ ≤ Cd² on the full unit branch disk ✓; W–W bounded factors ✓; W–B derivative ≍ e/|w| with |w| ≥ c r₁^d ✓; B–B no overlap ✓.

## 8. Epistemic status, obligations, falsifiers

**Proved (unconditionally, elementary):** existence of a Merkl atlas for μ_Ar with (r₁, N, c₁, M) as above, for every cover in the class.

**Assumed (supplied input, not re-verified here):** Theorem 3.1.2 with its displayed constants (Bruin's appendix). If its constants or r₁-dependence are off, only the numerical prefactor changes, not the form d³(d+L), provided the theorem's shape "a·n·f(r₁) + b·n·c₁ + (n−1)log M" survives; the audit summary notes the retained source had a false displayed Theorem 4.1 elsewhere, so this input should be independently checked before relying on the numeric prefactor.

**Remaining proof obligations:** none for the geometric statement. Optional sharpening (not needed): C_r can be reduced by orders of magnitude by optimizing ε, the net constants, and using a per-scale count only for scales below δ.

**Falsifiers (decisive, in order of cost):**
1. Exhibit any cover in the class with sup gr_Y > 1.2·10¹⁰ r d³(d+L); this would refute either §1–§7 (a specific lemma must then fail — the only candidates with any room are Lemma A's hypothesis range and the |w| lower bound in §6) or Theorem 3.1.2 itself.
2. Exhibit an overlap point of a Whitney unit chart and a branch unit chart with |w| < 0.89(3/4)^d; this would break §6 (I proved it impossible via Lemma B(b) and Lemma A).
3. Exhibit a component V of π^{-1}(D_b) on which w fails to be injective up to |w| = 2^{1/e}; impossible by the classification of covers of the punctured disk.

**Consistency flag (not evidence):** for fixed B (L = O(1)) this gives d⁴, better in d than the source's Belyi-cover bound; this is explained by the Whitney refinement down to scale h r₁^d, which keeps log M linear in d, and is not a contradiction with any lower bound known to me.

**Non-consequences (explicit):** no stable Faltings height bound, no finite-place intersection estimate, no bound on supplied-coordinate divisor heights, no uniform CRT reconstruction, no quantum algorithm, no speedup, no hardness. The twist family y² = a·x(x−1)(x−2) still forces charging model height. For algebraic B, replacing L by C_r(1+h_B) requires the separate product-formula inequality for averaged log-chordal collision over the Galois orbit; that is a distinct (easy but unproved-here) obligation, and only then does the exponential-in-h_B factor in the Green term specifically disappear — not in the other steps of the source's height argument.
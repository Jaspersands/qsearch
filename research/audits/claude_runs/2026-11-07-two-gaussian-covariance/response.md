# Report: covariance pair-block identity and the "small gap ⇒ near-degenerate-manifold" hope

## 1. Identity check (all proved, complex α,β allowed)

Hidden frame: unnormalized φ = α|0^m⟩ + β⊗_j χ_j, χ_j = c_j|0⟩+s_j|1⟩, x_j=c_j², P=∏x, P_j=∏_{l≠j}x_l, N=|α|²+|β|²+2Re(α*β)√P. Write **a=|α|²/N, b=|β|²/N** (both can be ≫1 near cancellation; only their product and minimum appear below).

- **Local det.** Tracing all pairs ≠ j gives Nρ_j = |α|²|0⟩⟨0| + |β|²|χ_j⟩⟨χ_j| + (αβ*√P_j |0⟩⟨χ_j| + h.c.). In the {|0⟩,|1⟩} basis the off-diagonal is β*s_j(βc_j+α√P_j); direct expansion gives N²det ρ_j = |β|²s_j²[|α|²+|β|²c_j²+2Re(αβ*)c_j√P_j − |βc_j+α√P_j|²] = |αβ|²(1−x_j)(1−P_j). ✓ (phases cancel exactly; no overlap/sign assumption).
- **Bloch length.** ν_j² = 1−4det ρ_j (eigenvalues λ,1−λ). ✓
- **Pair block.** The reduced pair state is even (each branch is even on every pair), so the 6 quadratics restricted to the even sector collapse to 3 Paulis (iγ₁γ₂=iγ₃γ₄, etc.), giving the quaternionic 4×4 block M with MMᵀ=ν_j²·1₄: eigenvalues ±iν_j, each twice (contract's "two identical singular values" = two canonical values; all four singular values equal ν_j). ✓ Cross-pair blocks vanish (⟨even|odd|even⟩=0), so the lab-frame spectrum is ⋃_j{±iν_j (×2)} ∪ {±i for inactive modes}; eigenvalues are 1-Lipschitz (Weyl) in the estimation error of C, eigenvectors are not.
- **Difference identity.** With Q=∏_{l≠j,k}x_l: h_j−h_k = (1−x_j)(1−x_kQ)−(1−x_k)(1−x_jQ) = −(x_j−x_k)(1−Q). Hence
 **ν_j²−ν_k² = 4ab(x_j−x_k)(1−Q).** ✓ Denominator-free apart from N>0 (automatic for an existing normalized state).
- **Endpoints.** x_j=0 (zero overlap): P=0, N=|α|²+|β|², fine. Cancellation α→−β, P→1: ab→∞ but (1−x_j)(1−P_j)→0, det→p_j(1−p_j) with p_j=s_j²/Σs², i.e. the W-state limit; det ≤1/4 preserved. Exact degeneracy ν_j=ν_k ⇔ x_j=x_k, or Q=1 (≤2 active pairs), or αβ=0; ν_j=1 ⇔ x_j=1 or P_j=1 or αβ=0. Even relative parity (both branches even) guarantees the Bloch–Messiah pairing with no unpaired fully-occupied mode; the physical parity label of the code is frame-dependent and must be learned, as stated.

Verdict: the contract's identity is exact as written. No counterexample.

## 2. The robust hope — proved, with explicit inequality (no counterexample found)

**Claim (proved).** Let D_M = min‖ψ−ψ_merged‖ over states of the model with the angle groups J∋j, K∋k set equal (all other data unchanged), D_2 = min‖ψ−ψ_2act‖ over model states with every pair outside {j,k} inactive, and Δ_jk = |ν_j²−ν_k²|. Then
 **D_M² · D_2² ≤ 2π² |J|² Δ_jk**, hence **min(D_M, D_2) ≤ (2π²|J|²Δ_jk)^{1/4} ≤ (4π²n²·sep_jk)^{1/4}**,
where sep_jk = min(|ν_j−ν_k|, ν_j+ν_k) is the spectral separation of the two 4-dimensional eigenspaces (Δ_jk ≤ 2·sep_jk since ν≤1). Constants are polynomial in n; no promise on α,β, overlaps, N, or gaps. Trace distance ≤ Euclidean distance for pure states.

**Proof.** (i) Branch-modification lemma: for u=α|0⟩+β|χ⟩, v=α|0⟩+β|χ'⟩, ‖u/‖u‖−v/‖v‖‖ ≤ 2‖u−v‖/‖u‖ = 2√b‖χ−χ'‖. Symmetrically, modifying the |0^m⟩ branch (written in the χ-frame as ⊗(c_jχ_j−s_jχ_j^⊥), same angles) costs 2√a‖0−0'‖, and the modified branch is still an even Gaussian product on the same pairs with the desired relative angles. So every bound below holds with m:=min(a,b).
(ii) Merge: moving the |J| angles θ_j→θ_k changes the branch by ≤ Σ 2|sin(Δθ/2)| ≤ |J||Δθ|, and |x_j−x_k| = sin(θ_j+θ_k)|sin(θ_j−θ_k)| ≥ (4/π²)Δθ² on [0,π/2]², so D_M² ≤ π²|J|² m |x_j−x_k|.
(iii) Two-active: setting all other pairs to vacuum changes the branch by √(2−2√Q) ≤ √(2(1−Q)), so D_2² ≤ 8 m (1−Q).
(iv) Multiply: D_M²D_2² ≤ 8π²|J|² m² |x_j−x_k|(1−Q) ≤ 2π²|J|² · 4ab|x_j−x_k|(1−Q) = 2π²|J|²Δ_jk, using m² ≤ ab. ∎

The m²≤ab step is exactly what neutralizes the α/β ill-conditioning: near cancellation a,b→∞ individually, but Δ_jk already contains the factor ab (in the W limit Δ_jk → 4q²|p_j−p_k||1−p_j−p_k|, D_M² ≲ 4q|p_j−p_k|, D_2² ≲ 8q(1−p_j−p_k), consistent).

**Same-structure corollary (degeneracy with the inactive block ν=1):** 1−ν_j² = 4ab(1−x_j)(1−P_j), and D_{j inactive}² · D_{only j active}² ≤ 2π²(1−ν_j²).

**Both alternatives are necessary (explicit family, α=β=1):**
 (a) m=3, x=(0.2, 0.7, 1−ε): Δ_12 = 4ab·0.5·ε, D_M=Θ(1), D_2=O(√ε). 
 (b) m=3, x=(0.5+ε, 0.5, 0.5): Δ_12 = 4ab·ε·0.5, D_2=Θ(1), D_M=O(√ε).
**Tightness:** exponent 1/4 is what the product bound gives; in all regimes I checked the true behaviour is ≤Δ^{1/2} (small |p_j−p_k| and small 1−p_j−p_k cannot both coincide with small p's), so 1/2 is plausible but not proved; it does not affect polynomiality.

## 3. What this does and does not establish; remaining obligations and falsifiers

- Established: exponentially small ν-separation forces ψ within poly(n)·sep^{1/4} of the degenerate manifold (merged or ≤2-active). An algorithm that *treats* a sub-threshold gap as a merged group loses at most this much per decision; to reach ε one needs threshold sep ≲ ε⁴/(4π²n²), i.e. ν estimated to that precision (poly copies via Weyl, since eigenvalues are stable).
- Not established (open obligations): (1) the learner must still *recover* the merged-group subspaces and angles via the paid quartic extractor; the inequality says nothing about its conditioning. (2) It does not decide which alternative holds; the ≤2-active alternative is exactly the regime the contract flags as unresolved by covariance. (3) Multi-group chains of near-degeneracies: the bound is pairwise; simultaneous merging of a cluster of width w in θ costs ≤2√m·n·w, but a chain alternating between the two alternatives has not been bounded — proof obligation. (4) Eigenvector (Davis–Kahan) error for groups that are *above* threshold still scales as (C-error)/sep, so the required C precision is poly(1/ε, n) but with exponent set by the threshold choice; compounding across the sequential tomography is unproved.
- Falsifiers: any model state with sep_jk ≤ 2^{-n} and min(D_M,D_2) ≥ 1/poly(n) would contradict the proved inequality — by the proof it cannot exist; a falsifier of the *algorithmic* hope would be a family where the quartic extractor on a merged group is itself exponentially ill-conditioned while the state is far from any cheaper structure (not analysed here, per instruction).
# Review: positive/variational alternatives for succinct periodic effective conductivity

**Verdict.** The proposed operation "shared random spatial hierarchy + local Schur complements ⇒ upper/lower bounds within ε at poly(B,n,1/ε) cost for EVERY medium" is **falsified** by an O(1)-size circuit family (scale-L structure). The Green–Kubo/resolvent route with polynomial time truncation or shrinking domains is falsified by the same family (Mourrat's (3.5) fails explicitly). Positivity (squared-semigroup form of even moments) does **not** reduce the H^{O(r)} variance. One concrete positive estimator survives as a **conditional** tool: a sampled low-Fourier-mode Galerkin bracket (primal upper + Thomson/Legendre lower bound), certified, cost poly(B,n,p,1/ε,log1/δ), tight exactly when the correctors are coarse. No polynomial-in-both-parameters estimator for all media is found; nothing here is a hardness or separation statement.

## 1. Cheapest falsifier: window / hierarchy bounds (proved)

Family A (B=O(1)): a_e=ρ iff the top bit of x_j equals 1 (two layers of thickness L/2 perpendicular to direction j). Exact: K_j = harmonic mean 2ρ/(1+ρ) (series); mean over direction-j edges ā=(1+ρ)/2.

Any bound of the form "average over cells of a hierarchy level of cell-Dirichlet energies" is a valid upper bound (glue cell minimizers with corrector 0 on cell boundaries). For cells of side ℓ<L/4, at least a (1−4ℓ/L) fraction lie inside a constant layer, where the cell energy is exactly the local conductivity; the remaining cells have energy ≥1. Hence
 Upper(ℓ) ≥ (1−4ℓ/L)(1+ρ)/2 + 4ℓ/L·1, so Upper(ℓ) − K_j ≥ (ρ−1)²/(2(1+ρ)) − O(ρℓ/L).
Family B (B=O(1)): 2×2 checkerboard, a=ρ iff top bits of x_1,x_2 differ. Same computation gives Upper(ℓ) ≥ (1+ρ)/2−O(ρℓ/L) and the glued-Neumann lower bound ≤ 2ρ/(1+ρ)+O(ρℓ/L). The bracket width is ≥ (ρ−1)²/(2(1+ρ)) − O(ρℓ/L) = Ω_ρ(1) for every ℓ ≤ L/c. Randomizing offsets or sharing randomness across levels changes nothing: the bound is a property of the glued trial field. Reaching width ε needs ℓ=Ω(L), i.e. Ω(N) work.

Hierarchical Schur complements without sampling cost ≥ N (every level-m window needs all its descendants; summing one window at the top level is N). Sampling windows at level m estimates the *average* over windows of a level-m quantity; converting that into the Schur complement of an *unsampled* parent requires a decay/mixing hypothesis. That hypothesis is exactly what Families A/B violate. So: proved failure for the window-average bounds; conditional (hypothesis-dependent) status for any sampled hierarchy, with the hypothesis falsified on an explicit native family.

## 2. Green–Kubo / resolvent chain with polynomial time (proved)

ENERGY in Mourrat's form: K_j = ā_j − 2∫_0^∞⟨f,e^{−tL}f⟩dt with f=D^*(a η̃_j) (η̃_j unnormalized indicator), L=D^*aD, ⟨f,e^{−tL}f⟩ ≥ 0 by reversibility. For Family A, f is supported on the two interface rows: ‖f‖² ≤ 2(ρ−1)²/L (normalized by 1/N). Hence
 ∫_0^T⟨f,e^{−tL}f⟩dt ≤ T‖f‖² ≤ 2T(ρ−1)²/L,
while ∫_0^∞ = (ā−K_j)/2 = (ρ−1)²/(4(1+ρ)). Any truncation at T=poly(n)≪L returns (1+ρ)/2 up to O(T/L), error (ρ−1)²/(2(1+ρ)). Equivalently, with f normalized, ⟨f,e^{−tL}f⟩ decays only like t^{−1/2} for 1≪t≪L² (1D diffusion across an interface), so Mourrat's (3.5) with α>1 fails; his Theorem 1.2 rate and the shrinking domains r_k are not available. Reaching t~L² by simulating the variable-conductivity walk costs ~4^n circuit evaluations per path (rates ≤4ρ, one step = O(B)). The dyadic resolvent chain needs k up to 2n and, without (3.5)/CLT, each term averaged over the full torus: Ω(N). This is a proved failure of the truncation mechanism, not of the instance (Family A is trivially solvable by other means).

## 3. Positivity does not cut variance (proved lemma + restricted lower bound)

Using Π²=Π and (ΣΠ)^{m*}=(ΠΣ)^m: T_{2m} = ‖Π(ΣΠ)^mΣη_j‖² ≥ 0 (squared-semigroup analogue), and T_{2m+1} = ⟨g_m,Σ g_m⟩ with g_m=Π(ΣΠ)^mΣη_j. Estimating ‖g_m‖² requires two independent unbiased estimates of g_m at a common sampled edge; their product has second moment ≤ H^{2(m+1)}·H^{2(m+1)} = H^{2(r+2)} — no better than the signed chain. Computing g_m(e) exactly is a dense sum (Ω(N) per Π application).

Restricted lemma: any estimator applying Π one sampled column at a time (weight Π_{ee'}u_{e'}/p(e')) has, by Cauchy–Schwarz, per-step second moment ≥ (Σ_{e'}|Π_{ee'}u_{e'}|)², which for a sign vector u equals the row ℓ¹ norm squared = Θ(log²L)=Θ(n²) (2D dipole kernel ~|x|^{−2}). So "per-step C independent of n" is impossible in this estimator class; the quasi-polynomial H^{O(k)} is intrinsic to single-column importance sampling. This is a lower bound for a restricted class only.

## 4. Positive construction: certified low-mode Galerkin bracket (conditional theorem)

Definitions. ψ_k(x) = (L/(2π|k|)) e^{2πik·x/L}, S_p={k: 0<|k|_∞≤p}, |S_p|=(2p+1)²−1. Edge gradients satisfy |(Dψ_k)_e|≤1 and (1/N)Σ_e|Dψ_k|_e² ∈ [4/π²,1], distinct k orthogonal.

Upper bound. E(θ)=(1/N)Σ_e a_e(1_{dir=j}+Σ_kθ_k(Dψ_k)_e)² = m_j+2Re⟨θ,b⟩+θ^*Aθ with (4/π²)I ⪯ A ⪯ ρI. K_j ≤ U_p := min_θ E(θ). Gap (proved): U_p − K_j ≤ ρ·(gradient energy of the exact corrector φ* in modes |k|_∞>p)/N, by E(φ*−χ)=K_j+(1/N)⟨aDχ,Dχ⟩ with χ=high-mode part of φ*.

Lower bound (proved, no symmetry assumed). For every edge current J with D^*J=0: K_j ≥ 2⟨J⟩_j − (1/N)⟨a^{−1}J,J⟩, equality at J=a(e_j+Dφ*). Proof: ⟨J,Dφ*⟩=0 and 0≤(1/N)⟨a^{−1}(J−aF),J−aF⟩, F=e_j+Dφ*. Parametrize J=v+Cψ, v∈R², ψ=Σ_{k∈S_p}θ_kψ_k on faces, C the lattice curl (automatically divergence-free). The form is concave with quadratic part in [4/(π²ρ),1]·I. L_p := max value. Gap: K_j−L_p ≤ ρ·(curl energy of the exact flux's stream function above mode p)/N.

Sampling. Draw M uniform edges, evaluate the circuit (O(B) each), accumulate all |S_p|² entries of A, b, m_j and the dual Gram from the same samples (entries are bounded by ρ, Hoeffding + union bound). Minimizer norms are bounded by C_ρ²≤π²ρ/4 (primal) and π²ρ²/4 (dual), so entrywise error τ=ε/(8C_ρ²|S_p|) gives |Ũ_p−U_p|,|L̃_p−L_p|≤ε/2 w.p. 1−δ with M=O(ρ⁴p⁴ε^{−2}log(p/δ)). Linear solves: |S_p|-dimensional, condition ≤ρπ²/4·(1+o(1)), O(log(ρ/ε)) bits suffice. Total cost poly(B,n,p,1/ε,log1/δ), independent of N. Output: certified [L̃_p−ε/2, Ũ_p+ε/2]; if its width ≤ε, done; else fall back to the written H^{O(k)} series estimator.

When it is tight (sufficient condition, explicit): both correctors have ≤ε/(2ρ) gradient energy above mode p. Family A: φ* is piecewise linear in x_j, gradient Fourier tail ~1/p, so p=O(ρ/ε) certifies within ε — the family that kills window bounds is handled in poly(B,n,1/ε). Family B: expected p=poly(1/ε) from a corner-singularity tail p^{−2α(ρ)}; this rate is NOT proved here (obligation).

Explicit falsifier for the bracket (proved): the period-2 checkerboard, or more generally the mid-scale checkerboard a=ρ iff bit ⌊n/2⌋ of x_1 and x_2 differ (B=O(1)). Its coefficient has Fourier support on 2^{n−⌊n/2⌋−1}Z², so for p<2^{⌊n/2⌋−1} the Galerkin matrices are diagonal and the bracket is exactly [harmonic mean, arithmetic mean], width Ω_ρ(1); simultaneously windows of side ℓ≤poly(n) see a constant medium, so Section 1's bounds also have width Ω(1). A union subspace (modes ⊕ cell-local functions) is still blind to this scale — sketched, not proved (obligation: show the cell correction of a mode-p function inside a constant cell gains ≤O((pℓ/L)²) energy).

## 5. Proof obligations, resources, next falsifier

Obligations: (i) Family B exact value sqrt(ρ)+o(1) via discrete Keller duality + 90° symmetry (interface edges are O(1/L) of all edges; needs a discrete Meyers estimate to convert to o(1) energy) — used only for commentary, not for any falsifier above; (ii) Fourier tail exponent for corner singularities (Section 4); (iii) the union-subspace blindness sketch.

Resources: pure derivation; no tools, code, or sources beyond the packet. No numerics run.

Next falsifier (one frozen fixture, exact rational, L≤64, ρ=2): (a) mid-scale checkerboard with squares of side 8, p=3 — predicted bracket exactly [4/3,3/2]; (b) Family A thick layers, p=1..8 — predicted upper gap decaying ~1/p toward 4/3; (c) 2×2 checkerboard, p=1..16 — record gap decay to probe obligation (ii). Any observed bracket violating K_j∈[L̃_p−ε/2,Ũ_p+ε/2] falsifies the construction; a gap not decaying in p on (b) falsifies the tail bound. No scaling claim, speedup, or hardness follows from these controls.
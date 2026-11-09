# Review: constant-degree Bell support gap for an arbitrary Pauli π/8 rotation

## Verdict

I found no counterexample for weights above a fixed cutoff. The argument survives with the following corrections:

1. **The cutoff.** For the bound ν[f=1] ≥ 1/1024, the cutoff is w ≥ 25, not 32. The value 32 is valid but loose. For the weaker statement K₃(actual) = K₃(S_p), w ≥ 22 suffices.
2. **The cutoff is necessary.** Take w = 1, P = Y. Then ψ is a computational basis state, so ν = {I: 1/2, Z: 1/2}, while S_p = {I, X, Z}. The indicator of X is x(1+z), which has degree 2. It vanishes on supp ν but not on S_p. So below the cutoff, interference genuinely shrinks the support. This is an exact small case. It does not contradict the large-w claim.
3. **The affine-equivalence step is unnecessary.** It transports only supports, not μ, ρ or ν. It sends a q(p)=1 translation to q(Z^w)=0, so it cannot be used to argue that the odd-Y case "behaves like" the canonical case at the level of measures. The direct proof below never uses it.

Everything else checks out exactly: the amplitude formula, odd Y counts, signed P, phases, normalization, the support identity, the 4^{-D} lemma, and the 2^{-2D-3} envelope gap.

## Exact derivation (proved)

**Setup.** Let φ = |H⟩^{⊗w} (real), c = cos(π/8), s = sin(π/8). Then ψ = cφ − i s Pφ, with P = ±P₀ Hermitian. The Bell amplitude is A_v = ψᵀσ_vψ / 2^{w/2}. Changing labelling conventions only changes phases per outcome.

**(a) Base amplitudes.** β_v = ∏ b(v_i), with b(I) = 1/√2, b(X) = b(Z) = 1/2, b(Y) = 0, because HᵀYH = 0. So β is real and supported on B, and β_v² = μ(v).

**(b) Transposes and Y parity.**
- Pᵀ = (−1)^k P. The sign ±1 cancels.
- k ≡ q(p) mod 2, since x_i z_i = 1 exactly at the Y positions.

**(c) Expanding ψᵀσ_vψ.**
- PᵀσvP = (−1)^{k+[p,v]} σ_v = (−1)^{ℓ(v)} σ_v.
- The two cross terms carry the factor (1 + (−1)^{ℓ(v)}).

Hence:
- ψᵀσ_vψ = (c² − s²(−1)^{ℓ}) φᵀσ_vφ − 2i·cs·[ℓ=0]·φᵀσ_vPφ.
- On ℓ = 1, the coefficient is c² + s² = 1, so ν = μ.
- On ℓ = 0, the coefficient is c² − s² = 1/√2 and 2cs = 1/√2.

With σ_vP = θ(v,p)σ_{v+p}, the ℓ = 0 amplitude is (β_v − iθβ_{v+p})/√2. This confirms the hypothesis. The overall sign of P multiplies θ by ±1.

**(d) The cross term.**
- On ℓ = 0, ν(v) = (β_v² + β_{v+p}²)/2 + β_vβ_{v+p}·Im θ.
- θ is real when σ_v and σ_p commute and imaginary when they anticommute.
- On ℓ = 0, [p,v] = q(p). So the cross term vanishes identically when q(p) = 0.
- When q(p) = 1, the cross term is nonzero only where β_vβ_{v+p} ≠ 0, i.e. on O ∩ {ℓ=0}.
- Off O, ν = ρ exactly. On O, 0 ≤ ν ≤ 2ρ, and exact zeros occur (as in the w = 1 case).

**(e) Normalization.**
- θ(v+p, p) = θ̄(v, p), and ℓ(v+p) = ℓ(v) because [p,p] = 0. So the cross terms cancel in pairs v ↔ v+p.
- Σρ = μ(ℓ=1) + μ(ℓ=0) = 1, since translation by p preserves {ℓ=0}.
- Because translation by p preserves both O and ℓ, ρ(O) = μ(O) = ν(O).
- Locally, if p_i = Y then v_i ∈ {X, Z} (mass 1/2); otherwise v_i ∈ {I, p_i} (mass 3/4). So μ(O) = 2^{-k}(3/4)^r. Note that O is empty unless k ≤ w, which always holds.

**(f) Support.**
- The identity q(u+p) = q(u) + ℓ(u) gives q = ℓ on B+p, and q = 0 on B.
- Therefore supp ρ = B ∪ ((B+p) ∩ {ℓ=0}) = (B ∪ (B+p)) ∩ {q=0} = S_p.
- Also ν ≤ 2ρ, so supp ν ⊆ S_p.

## Theorem (self-contained)

**Convention (assumption about the intended setting).** "Degree" means F₂-degree in the 2w variables (x, z). Here f: F₂^{2w} → F₂, and "f nonzero on S" means f(v) = 1 for some v ∈ S.

**Lemma 1.** Let λ be any product measure on B whose local masses on I, X, Z are all at least 1/4. If deg f ≤ D and f is not identically 0 on B, then λ[f=1] ≥ 4^{-D}.

*Proof.*
1. On B, x_i z_i = 0. Functions on B have a unique reduced form spanned by monomials using at most one of x_i, z_i per qubit. This holds because each local function space {1, x, z} has dimension 3 = |{I, X, Z}|.
2. Pick a reduced monomial M of maximal degree d ≤ D, on a qubit set T.
3. Fix all qubits outside T. The coefficient of M stays equal to 1, because any other contribution would need a monomial of degree greater than d.
4. So the restricted function on {I,X,Z}^T is nonzero. It takes the value 1 at some point, which has λ-mass at least 4^{-d}. ∎

**Lemma 2 (envelope gap).** If deg f ≤ D and f is nonzero on S_p, then ρ[f=1] ≥ 2^{-2D-3}.

*Proof.*
- **Case: f is nonzero on B.** On B, ρ ≥ μ/2. Lemma 1 gives ρ[f=1] ≥ 4^{-D}/2.
- **Case: f vanishes on B.** Then f(v) = 1 for some v ∈ (B+p) with ℓ(v) = 0.
  1. Define g(u) = (1 + ℓ(u))·f(u+p). This has degree at most D+1, since ℓ is affine.
  2. g is nonzero on B at u = v+p.
  3. For every u ∈ B with g(u) = 1, the point u+p has f = 1, ℓ = 0, and ρ(u+p) ≥ μ(u)/2.
  4. The map u ↦ u+p is injective. So ρ[f=1] ≥ 4^{-(D+1)}/2 = 2^{-2D-3}. ∎

**Theorem.** For every P (any sign, any k) and every f with deg f ≤ D that is nonzero on S_p:

  ν[f=1] ≥ ρ[f \ O] ≥ 2^{-2D-3} − 2^{-k}(3/4)^{w-k} ≥ 2^{-2D-3} − (3/4)^w.

- If k is even, ν = ρ, and the bound 2^{-2D-3} holds for every w with no cutoff.
- For D = 3, using log₂(4/3) ≈ 0.41504:
  - ν[f=1] ≥ 1/1024 for all w ≥ 25. At w = 24, (3/4)^w ≈ 2^{-9.96} > 2^{-10}, so this argument fails there.
  - ν[f=1] > 0, and hence K₃(supp ν) = K₃(S_p), for all w ≥ 22.
  - Using k ≥ 1 in the odd case gives μ(O) ≤ (2/3)(3/4)^w. This tightens the cutoffs to w ≥ 23 and w ≥ 21 respectively.
- For general constant D, the cutoff is w > (2D+3)/log₂(4/3). It depends on D but not on P.

## Status and remaining obligations

**Exact:** items (a)–(f), Lemmas 1–2, and the Theorem. These hold under ideal fresh copies, an exact Bell measurement, and the F₂-degree convention.

**Assumptions:**
- P is Hermitian, so its sign is ±1. A sign of ±i makes exp(−iπP/8) non-unitary and is out of scope.
- K₃ means the degree-≤3 vanishing ideal of the support.

**Not shown:** whether K₃(actual) differs from K₃(S_p) for odd k with 2 ≤ w ≤ 21. The w = 1 case shows that it can differ for small w.

**Cost (not part of the proof):**
- Each sample consumes 2 copies.
- A gap γ = 1/1024 per nonvanishing f does not by itself certify the whole ideal.
- A union bound over the F₂-space of degree-≤3 polynomials (dimension N ≈ (2w)³/6) gives roughly N·ln2/γ samples. This is a crude bound, not an optimized one.

**Falsifier:** any degree-≤3 f that is nonzero on S_p with ν[f=1] < 1/1024 at w ≥ 25. That would refute the amplitude formula in (c). The cheapest check is to recompute (c) by hand at w = 2 with P = YX.
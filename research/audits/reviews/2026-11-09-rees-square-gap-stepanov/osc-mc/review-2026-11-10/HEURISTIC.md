# Heuristic weight of projectively structured (C1) families (draft for §12; heuristic, not proved)

> Superseded (2026-11-10): this is the version the referee reviewed. §3's factor e_κ = 2 at even κ is wrong. A
> non-split involution never gives a rank-1 block at even κ, so R₂₊₂ = N_inv²κ⁴/p² at every κ (κ = 6: 2.62·10⁶/p²).
> The corrected text is in the topic note §12.5; see `REPORT.md`.

Setting. κ ≥ 4, p ≡ 1 (mod κ), H = κ-th powers, ind(x) mod κ. A (C1) configuration is a pair of disjoint
κ-sets (S, T) in P¹(F_p) whose κ×κ index matrix M[s,t] = ind(s − t) mod κ is rank-1 additively
(M = α_s + β_t). A generic pair is a configuration with probability κ^{−(κ−1)²}; that defines μ₁.

1. Involutions. An involution ι of P¹ is fixed by two of its 2-cycles: the Möbius map with a ↦ a′, a′ ↦ a,
   b ↦ b′ is an involution and is unique. So a κ-set S has exactly N_inv(κ) = C(κ,2)C(κ−2,2)/2 involutions
   that swap two disjoint pairs of S (45 at κ = 6, 105 at κ = 7), distinct unless S has three ι-pairs.
   Involutions form a 2-dimensional family (the conjugacy class of x ↦ −x; centraliser = a torus).

2. The 4×4 block. Normalise ι to x ↦ −x, rows (a, −a, b, −b), columns (x, −x, y, −y), h = ind(−1).
   Write P_{ix} = ind(r_i − x), Q_{ix} = ind(r_i + x). Then M[r_i, x] = P, M[r_i, −x] = Q,
   M[−r_i, x] = h + Q, M[−r_i, −x] = h + P. Rank-1 forces P − Q = β_x − β_{−x} = Q − P, so
   2(P − Q) ≡ 0, and comparing rows a, b and columns x, y, P_{ix} − Q_{ix} = c for one c with 2c ≡ 0
   (c ∈ {0, κ/2} for even κ, c = 0 for odd κ). P itself must be rank-1 (one condition). Probability
   e_κ κ^{−5} (e_κ = 2 for even κ, 1 for odd), against κ^{−9} generic: enhancement e_κ κ⁴.
   Checked numerically at κ = 6, 11 primes, 4·10⁶ samples each (block_rate.py): observed/heuristic
   0.87–1.03, with no spike dependence.

3. The 2+2 family. Call (S, T) structured if some ι swapping two pairs of S has two ι-pairs inside T.
   For uniform T and a fixed ι, P(T contains two ι-pairs) ≈ N_inv(κ)/p². If the remaining (κ−1)² − 9
   conditions behave independently, the structured configurations have rate
       R₂₊₂(κ, p) = N_inv(κ)² · e_κ κ⁴ / p²      (relative to μ₁).
   κ = 6: 5.25·10⁶/p² (2.0 at p = 1621, 1.4 at 1933, 0.95 at 2347, 0.35 at 3877; = 1 at p ≈ 2290).
   κ = 7: 2.65·10⁷/p² (0.021 at p = 35281).
   Along the tabulated thresholds T(κ) (§11.8, typical group constants): 0.0099 (κ = 7, p ≈ 5.1·10⁴),
   0.0025 (κ = 8), 1.1·10⁻⁴ (κ = 9), 1.5·10⁻⁵ (κ = 10).

4. General families. Let g ∈ PGL₂ have order m (non-identity conjugacy classes have dimension 2), and
   let S contain a g-orbits and T contain b g-orbits, x = am/κ, y = bm/κ ∈ (0, 1]. Codimension in
   (S, T): c = (a + b)(m − 1) − 2. The am × bm block has E = (m − 1)(abm − a − b) fewer rank-1
   conditions than a generic one (E = 4 for the 2+2 involution block, κ²/2 − κ for full involution
   symmetry), i.e. E = κ²xy(1 − 1/m) − κ(x + y)(1 − 1/m). The number of ways to place the orbits is
   κ^{O(κ)}. At p = κ^{γκ}:
       log_κ R = κ²(1 − 1/m)[xy − γ(x + y)] + O(κ).
   Since xy ≤ (x + y)/2 with equality only at x = y = 1, every family is negligible once
   γ > 1/2 + O(1/κ); the fully symmetric ones (x = y = 1) are the last to go.
   Exact full-involution case (even κ): R_full = ((κ−1)!!)² κ^{κ²/2−κ} p^{2−κ} (κ = 6: 4.9·10¹¹/p⁴),
   which is < 1 once p > κ^{κ/2 + 1 − 1/ln κ + o(1)}.
   The exponent statement needs OSC′ at p ≈ T = κ^{κ/2 + κ/(2 ln κ) + O(1)}, where R_full ≈
   κ^{−κ²/(2 ln κ) + O(κ)} and R₂₊₂ ≈ κ^{12 − κ − κ/ln κ + O(1)}.

5. What this does and does not say. It is a first-moment count with an independence assumption; the
   measured structured rate at κ = 6 is F(p)·R₂₊₂ with F between 0.15 (1621) and 1.4 (1597), so the
   arithmetic factor F is not predicted. The heuristic says projectively structured families of bounded
   orbit type lose weight like p^{−c}; it does not bound their class values, and it does not exclude other
   (non-projective) structure.

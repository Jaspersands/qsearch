### 12.12 What controls the 2+2 family's effect: G, not F·B (10 Nov) [elementary; computed]

- **Correction to §12.11.** §12.11 says that at κ = 6 "is F bounded?" is the question whether (N)'s B is bounded at
  spike primes. That is backwards. (N) is the lower bound N₁ ≥ μ₁/B, so B controls μ₁/N₁, which is small at spike
  primes (N₁/μ₁ 2.6–4.5 at the κ = 6 spikes). Spike primes do not stress (N). Its worst case in the survey is 1741
  (N₁/μ₁ 0.37).
- **The parameter.** Let s be the 2+2 share of the (C1) measure, and G := s/R₂₊₂ = F·μ₁/N₁, the family's share over
  its heuristic weight R₂₊₂ = N_inv²κ⁴/p². Then F = G·N₁/μ₁ exactly.
- **§12.5 item 6 without (N)** [elementary].
  - V is linear in the measure, so V_all = s·V_fam + (1 − s)·V_rest. The weighted rms is a norm, so
    ρ_G ≤ (1 − s)ρ_G,rest + s·v_G for either group G.
  - |Q| ≤ n, so v_G ≤ n; and s = G·R₂₊₂ by definition.
  - Hence the family adds at most G·R₂₊₂·n·p/κ² = G·N_inv²κ²·(n/p) < G·N_inv²κ² to B_D (κ²/p units), and at most
    G·R₂₊₂·n < G·N_inv²κ⁴/p to B_L.
  - N_inv = C(κ,2)C(κ−2,2)/2 < κ⁴/8, so N_inv²κ² = κ^{O(1)}: it is κ^{6.8}, κ^{7.1}, κ^{7.4}, κ^{7.6} at κ = 7–10.
  - So the 2+2 family can spoil the (1/2+o(1))κ exponent only if G = κ^{Ω(κ)} at some p ≥ p₀ near the threshold
    path. This replaces item 6's "F·B = κ^{Ω(κ)}". The old form bounded s by F·R₂₊₂·B, using (N); the new form uses s
    itself, needs no lower bound on N₁, and is never weaker (F·B ≥ F·μ₁/N₁ = G whenever (N) holds).
  - The rest still enters through (1 − s)ρ_rest, which this does not bound.
- **G in the data** [computed; `survey/score_F.out`, §12.6].
  - κ = 6, λ ≤ 0.25 (29 primes): G is 0.58–1.05 (median 0.74). This is no test: R₂₊₂ is 0.70–1.12 there, so s ≤ 1
    already caps G at 0.89–1.42.
  - κ = 7: G is 2.0 (35281), 0.51 (35099), 1.5 (36037, from its split), 0.95 (34693) and 1.3 (23549), against trivial
    caps of 21–49. These rest on 5–185 structured configurations, and the pairsym values are clustered.
  - So wherever it is measured the family's share is its heuristic weight to within 2×, at spike and typical primes
    alike. F's large values at the κ = 6 spikes are N₁/μ₁'s.
- **What a proof would need.**
  - G ≤ κ^{o(κ)} uniformly would follow from (a) an upper bound #2+2 ≤ κ^{o(κ)}·R₂₊₂·μ₁ together with (b) (N) with
    B = κ^{o(κ)}, or from a direct bound on the ratio.
  - Both (a) and (b) count configurations defined by κ-th power residue conditions on about κ² shifted values of one
    variable set, at p = κ^{(1+o(1))κ} near the thresholds.
  - Weil (Deligne) gives these counts with error κ^{O(κ²)}√p. That exceeds the main term unless p ≥ κ^{cκ²}.
  - This is the regime of power-residue patterns of length about log p/log log p, beyond square-root cancellation.
    The methods known there (Weil, Burgess, Graham–Ringrose, the Hanson–Petridis clique bound for Paley graphs) do not
    reach it. This describes the obstacle; no formal reduction to a named conjecture is claimed.
  - The κ = 3 method (exact cyclotomic numbers, §11.2) does not apply: two disjoint pairs need κ ≥ 4. At κ = 4 every
    such ι preserves S and permutes the buckets, so the 2+2 count is a sum over ι-invariant buckets, computable by
    cyclotomic numbers of order 4. That gives κ = 4 values, not a bound uniform in κ.
  - No counterexample family is known: no measured prime has G above 2.
- **Consequence.** Unless G grows with κ, the 2+2 family is harmless for the exponent, and obstruction (c) is the rest:
  ρ_rest at spike primes, the part that 36037 shows lifted at κ = 7. That is OSC′ itself for the not-2+2 part, and
  nothing here bounds it.
- **Claim gates stay false:** G bounded or κ^{o(κ)}; any bound on ρ_rest; obstruction (c) resolved.

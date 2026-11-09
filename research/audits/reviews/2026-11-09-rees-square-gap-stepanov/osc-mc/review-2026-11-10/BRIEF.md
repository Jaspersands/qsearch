# Review brief: κ = 6 spike survey and the partial-involution structure of (C1) configurations

You are an independent referee. Try to break each claim below: find coding errors, wrong counts, statistics that
do not support the wording, and overstated conclusions. Reports are advisory; the author verifies every point.

## Context (read only what you need)
- `research/STATE.md` lines 24–51 (the square-gap block) for the state before this work.
- Topic note `research/audits/reviews/2026-11-09-rees-square-gap-stepanov.md` §11.3–§11.8 (lines 394–720) for
  the definitions: (C1) configurations (S, T) (T a k-subset of one S-bucket = points with equal profile
  ind(s_j − x) mod k modulo the diagonal), class values V(R,C), the group constants B_L, B_D, PW_pair, the noise
  law, OSC′ and the exponent statement.
- Code and outputs are in `research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc/`:
  - `mc_classes.py` (the established sampler; do not re-review it), `k6_spike_survey.py` (survey analysis; the new
    part is the C_sym / symR columns and Spearman lines), `sym_rate.py` (rate of involution-symmetric S),
    `pairsym.py` + `sym_confs_lib.py` (partial involution symmetry of configurations), `mc_split.py` (class values
    split into structured / unstructured configurations; must reproduce mc_classes.py exactly at equal seed),
    `split_report.py`, `block_rate.py` (rank-1 rate of a symmetric 4×4 block), `bucket_stats.py`.
  - Outputs: `survey/sym_rate_k6.out`, `sym/sym_rate_k7*.out`, `pairsym/*.out`, `split/*.log` and npz,
    `blocks/block_rate_k6.out`, `buckets/bucket_k7_*.out`, `survey/mc_k6_p*_s13.log`.
- The heuristic derivation is in `HEURISTIC.md` next to this brief.

## Claims to check
1. [computed] N1/μ1 (configuration rate of uniform S relative to the random model) is predicted by the
   involution-symmetric rate symR of `sym_rate.py`: over the κ = 6 survey primes finished so far, Spearman
   ρ(symR, N1/μ1) ≈ 0.95, and log N1/μ1 = −0.14 + 0.98 log symR + 1.93 log λ fits with residual sd ≈ 0.2 (fit on
   14 primes; it predicted the earlier runs 1933, 2347, 4219 at 2.54/0.78/0.89 against 2.63/0.76/1.03).
   Check `sym_rate.py` (sampling of S = {±r_i}, the fixed-bucket test, the share f) and whether the statistics
   support "predicted".
2. [computed] At κ = 6, λ ≈ 0.21, 67–86% of (C1) configurations are "2+2 structured": some involution ι of P¹
   that swaps two disjoint pairs of S has two ι-pairs {t, ι(t)} inside T. This holds at typical (1621: 72%) and
   spike primes (1597, 1627, 1657: 67–86%); the share falls to 56% (1933, λ 0.25), 43% (2347, λ 0.30), ≈16%
   (3877, λ 0.50); random b-sets in place of buckets give 0%. Check `pairsym.py`: the involution construction
   (`mob_from((a, a′, b), (a′, a, b′))`), the pair counting, the exact count of k-subsets with ≥ 2 whole pairs,
   the null mode, and whether "max over ι" undercounts.
3. [computed] `mc_split.py` reproduces `mc_classes.py` configuration by configuration at equal (k, p, nconf,
   seed) (verified: max |ΔS1| = 0 at 1657, 300 configurations) and its parts sum to the total. At the spikes
   1657 and 1597 both parts have elevated group constants (structured B_D 11.6 / 4.3, unstructured 5.8 / 2.6,
   typical primes 0.4–0.9), so the spike is not carried by the 2+2 family alone. Check the split logic and
   that `k6_spike_survey.analyse` is applicable to a part (N_unl scaled by the part's share; N1 likewise).
4. [heuristic] `HEURISTIC.md` §1–§4: N_inv(κ) = C(κ,2)C(κ−2,2)/2 involutions per κ-set; the 4×4 symmetric block
   is rank-1 with probability e_κ κ^{−5} (e_κ = 2 even, 1 odd) against κ^{−9}; the 2+2 family weight
   R₂₊₂ = N_inv² e_κ κ⁴/p² relative to μ₁; the general family estimate
   log_κ R = κ²(1 − 1/m)[xy − γ(x + y)] + O(κ) at p = κ^{γκ}, so all bounded-type projective families are
   negligible once γ > 1/2 + O(1/κ); R_full for full involution symmetry; the values at the thresholds
   T(κ). Re-derive the codimensions (involutions form a 2-dimensional family), the condition counts and the
   asymptotics. `block_rate.py` checks the block probability numerically (0.87–1.03 of the heuristic).
5. [computed] At κ = 7, λ = 0.30 (p = 35281), bucket occupancy is Poisson (var/mean 0.999; b = 7, 8 at Poisson
   rates) and N1/μ1 ≈ 0.90, unlike κ = 6 at λ 0.25 (b = 8 21×, b = 10 690× Poisson). symR at κ = 7, λ ≈ 0.3
   still varies 9.4–44 over 13 primes. (More κ = 7 results will follow by message.)

## Rules
- The machine is heavily loaded: any computation `nice -n 19 /opt/anaconda3/bin/python -I ...`, at most
  15 CPU-minutes in total, small sizes. Do not start long runs.
- No git commands. Do not edit existing files. Write your report to `REPORT.md` in this folder; scratch files
  in a subfolder `scratch/` here.
- For each claim: verdict (confirmed / wrong / overstated / unclear), the evidence, and the corrected wording if
  needed. Then list anything else you found.

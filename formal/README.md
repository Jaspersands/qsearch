# Lean formalization: exterior-power cycle indicator

This folder holds a Lean 4 + Mathlib project. It checks parts of
`research/PRIME_CHARACTER_EXTERIOR_BOUND.md` (called "the note" below) and of
its Python mirror `exterior_characters`
(`theorems/prime_character_exterior_bound.py`, line 33).

Nothing here uses `sorry`. `Formal/Audit.lean` checks that every theorem listed
below depends only on Lean's three standard axioms, so `lake build` fails if a
`sorry` gets into one of them or into anything they use. A `sorry` in some other
theorem only produces a warning, so CI builds with `lake build --wfail`, which
fails on any warning. On 2026-10-19 both checks were tested: a `sorry` in
`ceilSqrt_le_sqrt_add_one` failed `lake build`, and a `sorry` in a new,
unlisted theorem passed `lake build` but failed `lake build --wfail`.

## How to build

Versions are pinned: Lean `v4.35.0` (`lean-toolchain`) and Mathlib `v4.35.0`
(commit `56a0058`, in `lake-manifest.json`).

1. Install elan from https://github.com/leanprover/elan.
2. From this folder (`formal/`), run:

```text
lake exe cache get    # downloads prebuilt Mathlib; never build Mathlib yourself
lake build --wfail
```

The build output (about 7 GB, mostly Mathlib) goes in `formal/.lake/`, which
git ignores. If the checkout is in a folder that iCloud or another service syncs,
exclude `formal/.lake/`. CI runs the same steps in `.github/workflows/lean.yml`.
A clean local build took about 5 minutes after the cache download; a rebuild with
nothing changed takes seconds.

To regenerate the Python values after `exterior_characters` changes, run
`python formal/scripts/gen_crosscheck.py` from the repository root. Add
`--check` to check the file without rewriting it.

## What is proved

In the table, z stands for −t: the code's `∏(1 − (−z)^ℓ)` is the note's
`∏(1 − t^ℓ)`. L is the list of cycle lengths, and n is their sum.

| Lean name | Statement | Note |
|---|---|---|
| `permDet_eq_mul_stdDet`, `one_add_X_dvd_permDet` | `∏(1 − (−z)^ℓᵢ) = (1 + z)·stdDet L` in `ℤ[z]`. So `1 + z` divides the product. | 47, 56-57 |
| `stdDet_unique` | The quotient is unique. | 56-57 |
| `stdDet_eval_neg_one` | At `z = −1` (that is, `t = 1`) the quotient is `n` for one cycle and `0` for two or more. | 49 |
| `cycle_indicator`, `cycle_indicator_of_eq` | `∑_{j<n} (−1)^j χ_j = n·[c = 1]` for the integer coefficients `χ_j`, with all `ℓᵢ ≥ 1`. | 52-54 |
| `stdDet_coeff_zero` | `χ₀ = 1`. | 52-54 |
| `perm_cycle_indicator` | The same identity for any `σ : Perm (Fin n)`, using `σ.partition` (cycle lengths, fixed points included). | 44-54 |
| `ofCoeffList_extCharsList`, `stdDet_coeff_eq`, `altSum_extCharsList` | A computable list version of the Python algorithm, proved equal to the polynomial's coefficients. | 56-58 |
| `exterior_std_no_invariants`, `extStdRep_invariants_eq_bot`, `sum_map_stdRep_eq_zero` | Over any characteristic-zero field and for every `j ≥ 1`, `Λ^j V_std` has no nonzero `S_n`-invariant vector. | 60-66 |
| `trace_stdRep`, `stdDet_coeff_one`, `quotient_coeff_one_eq_trace` | Only the `j = 1` case of milestone 2: `χ₁` equals the trace of `σ` on `V_std`, which is the number of fixed points minus 1. | 52-56 |
| `traceBound_ge_inv_two_n`, `exterior_threshold_suffices` | If `p > 0`, `p ≥ 16A²` and `p ≥ 4(R + A)`, then `max(0, (p + 1 − R − A⌈√p⌉)/(n p)) ≥ 1/(2n)`. The second theorem takes `R = n + b` and `A = (R − 2)(2^(n−1) − 1)`. | 104-106, 119-121 |
| `A_mul_sqrt_le`, `four_A_mul_ceilSqrt_le` | The intermediate steps `A√p ≤ p/4` and `A⌈√p⌉ ≤ p/4 + A`. | 123 |
| `ceilSqrt_eq_ceil_sqrt` | Python's `isqrt(p) + [isqrt(p)² ≠ p]` is exactly `⌈√p⌉`. | 106, 110 |
| `sum_choose_Ico` | `∑_{j=1}^{n−1} C(n−1, j) = 2^(n−1) − 1`, the Python `rank_sum`. | 105 |
| `irreducible_rate_ge_traceBound` | The summation step: `I/p ≥` the trace bound, **if** the imported inputs are taken as hypotheses (the indicator summed over fibers, `#U ≥ p + 1 − R`, and `|S_j| ≤ (R − 2)C(n−1, j)√p`). | 99-106 |

The milestone-3 proof averages over `S_n` instead of extracting
coefficients. On a wedge of distinct basis vectors `bᵢ = eᵢ − e_n`, some
transposition acts by −1. For `j ≥ 2` it swaps two factors. For `j = 1` it is
`(i n)`. So the operator `∑_σ Λ^j(σ)` is zero, and an invariant `x` satisfies
`n!·x = 0`.

## What is not proved, and why

- **Milestone 2 in full is not proved.** The missing statement is that
  `det(1 + zσ)` on the permutation representation equals `∏(1 − (−z)^ℓ)` over
  `σ`'s cycle type, together with `χ_j = Tr(σ | Λ^j V_std)` for every `j`.
  Only `j = 1` is done (above). Mathlib `v4.35.0` has no lemma for any of these
  three pieces:
  1. the determinant or characteristic polynomial of a permutation matrix in
     terms of `cycleType`. Mathlib has only `det_permutation`
     (det = sign) and `trace_permutation` (trace = number of fixed points);
  2. `det(1 + z f) = ∑_j tr(Λ^j f) z^j`, which links the determinant to traces
     on exterior powers. The pieces exist (`Module.Basis.exteriorPower` and
     `Matrix.charpoly_coeff_eq_sum_minors`), but they are not connected;
  3. a `LinearMap` version of "charpoly = charpoly on an invariant subspace ×
     charpoly on the quotient". Only matrix block versions exist
     (`Matrix.charpoly_fromBlocks_zero₂₁`, `BlockTriangular.charpoly`).

  A workable plan is to decompose by orbits and compute one cycle's
  determinant (by Laplace expansion, or by the minimal polynomial `X^ℓ − 1`).
  That is several hundred lines, beyond this spike.
- **The A_n countermodel (note, lines 68-70)** is not formalized.
- **The étale-cohomology trace bound (note, lines 74-97)** was out of scope. In
  `irreducible_rate_ge_traceBound` its consequences are hypotheses, not
  theorems.
- **The `p ≥ 2·D_bad` part of the Python threshold (note, line 124)** is about
  the number of geometry trials, not about the trace bound. It is not
  formalized.

## Cross-check against the Python code

`scripts/gen_crosscheck.py` reads `exterior_characters` from
`theorems/prime_character_exterior_bound.py` with Python's `ast` module and
runs only that one function. The script does not import the module. It writes
`Formal/CrossCheck.lean` with the Python output for **all 44 cycle types of
n = 1, …, 7**, and records the source file's SHA-256 (`a935cb08…`).

The Lean side checks the data in three ways:

- `extCharsList_eq_python` (`by decide`, checked by the kernel): the Lean list
  algorithm gives exactly the Python lists for all 44 cycle types.
- `stdDet_eq_python` and `stdDet_coeff_eq_python`: therefore each Python
  `chars[j]` is the `j`-th coefficient of the polynomial `stdDet L` that the
  theorems above are about.
- `python_cycle_indicator` (`by decide`): every Python row has alternating sum
  `n` for one cycle and `0` otherwise.

A compiled `#eval` of the same comparison prints `true` during the build.

Result: all 44 rows agree, with no mismatches. Some sample rows:
`[3,2,1] ↦ [1,0,-1,1,0,-1]`, `[2,2,2,1] ↦ [1,0,-3,0,3,0,-1]`,
`[7] ↦ [1,-1,1,-1,1,-1,1]`.

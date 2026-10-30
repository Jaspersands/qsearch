# Bezout Exponent-Reduced Higher-Degree SDE Solver and Two-Stage Weighted-to-Ordinary Phase-Erasure Cascade

2026-10-28 update. **Public classical controller and exact reference controls;
not a coherent quantum compiler, all-prime SDE backend, novelty claim, or
accepted speedup candidate.**

Reduced degree3 uses [two-level cubic contraction](CUBIC_TWO_LEVEL_CONTRACTION.md).
For any reduced g>=2, [symmetric contraction](POWER_SDE_SYMMETRIC_CONTRACTION.md)
provides `(r+1)*((g-1)*r+1)` columns when `p>=16*g**(2*g+2)`.
It is selected for g>=4 and g=2,p=1 mod4; existing cubic and p=3 mod4
quadratic backends retain their broader regimes. Odd g>=5 also has the
[exterior fallback](ODD_POWER_EXTERIOR_SDE.md) when
`p>=4*((g-1)*(g-2))**2`. Other nonzero-rank regimes fail closed.
Sampling bounds require uniform draws; FLINT root runtime is not clocked.
Explicit `bounded_randomness_bits` opts into a whole-run large-field budget
including root splitting and bit rejection; other nontrivial regimes reject
that option. See [the budget proof](POWER_SDE_RANDOMNESS_BUDGET.md).

## 1. Summary and Mechanical Gaps Closed

This note documents `theorems/weighted_two_erasure_cascade.py` and `tests/test_weighted_two_erasure_cascade.py`, closing the higher-degree and two-stage weighted-to-ordinary phase-erasure controller gaps identified in `research/NONLINEAR_JET_HSP_RECEIVER.md` (Sections 6–10), `research/CLASS_THREE_MONOMIAL_FULL_JET.md` (Sections 6–7), and `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Bezout Exponent-Reduced Fixed-Degree SDE Solver (`bezout_reduced_exponent`, `solve_bezout_sde_weights`, `verify_general_degree_witness`)**:
   - Implements the Section 3 exponent reduction of [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016): for any degree $d \ge 1$ and odd prime $p$, sets $g = \gcd(d, p - 1)$ and $u = (d / g)^{-1} \bmod ((p - 1) / g)$ so $(y^u)^d \equiv y^g \pmod p$ for all $y \in \mathbb{F}_p$.
   - Solves $\sum_i s_i^d v_i \equiv 0 \pmod p$ in $r + 1$ columns when $g = 1$ and in $(r + 1)^2$ columns via `square_weights_capped` when $g = 2$ and $p \equiv 3 \pmod 4$, deterministically verifying the witness on the original uncompressed columns (`verify_general_degree_witness`).
   - Supports higher original degrees only when their reduced exponent and field regime are covered. New controls include genuine reduced degrees4 and5, Bezout lifts, and weighted unknown-phase erasure. The large-prime controls in this report below still reduce to g=1 or2; the separate power-SDE reports exercise the new regimes.
2. **Provenance-Pinned Weighted Erasure & Two-Stage Cascade (`PinnedWeightedPacket`, `weighted_erasure_stage`, `transition_to_fourier_residual`, `ordinary_higher_degree_erasure_stage`)**:
   - Enforces distinct wrapper instances, pinned `(instance_id, chart_id, chart, parameter_basis)`, and single-use consumption across all weighted merges.
   - Enforces `weighted_degree == 0` before allowing negative $t$-Fourier readout (`transition_to_fourier_residual`), and executes Stage-2 ordinary degree erasure from $D$ down to $0$.

## 2. Stage-1 Weighted Erasure Cascade ($p = 23$, `FullTaylorJetChart` $D = 3$)

| Stage Weighted Degree $d$ | $g = \gcd(d, p-1)$ | Active Equations | Compressed Rank $r$ | Output Weighted Degree |
| :--- | :--- | :--- | :--- | :--- |
| `5` | `1` | `2` | `2` | `4` |
| `4` | `2` | `2` | `2` | `3` |
| `3` | `1` | `1` | `1` | `1` |
| `2` | `2` | `1` | `1` | `1` |
| `1` | `1` | `1` | `1` | `0` |

## 3. Negative $t$-Fourier Transition, Stage-2 Ordinary Erasure & 127-Bit Prime Controls

| Verification Control | Result |
| :--- | :--- |
| Full-jet residual initial ordinary degree ($D = 3$) | `3` |
| Stage-$D$ ordinary erasure active equations / rank | `1` / `1` |
| Ordinary degree after Stage-$D$ erasure | `1` |
| 127-bit prime ($p = 2^{127} - 1$) degree-4 SDE ($g=2$) | Verified (`rank = 1`, `9` cols) |
| 127-bit prime ($p = 2^{127} - 1$) degree-5 SDE ($g=1$) | Verified (`rank = 1`, `3` cols) |

## 4. Explicit Scope Boundaries

- `evaluate_fixture` is never called by any solver or cascade function.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.

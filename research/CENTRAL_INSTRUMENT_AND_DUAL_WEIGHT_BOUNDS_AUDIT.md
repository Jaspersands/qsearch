# Complete Central Fourier Instrument, Nontrivial $H \cap C$ Zero-Mass Falsifier, and Dual-Weight Class-Three Phase Bounds Audit

2026-10-21. **Standalone finite controls for `Formal/CentralRegularSource.lean` and `Formal/ClassThreePhaseBounds.lean`; not formal Python refinement, an admitted speedup candidate, or a novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/central_instrument_and_dual_weight_bounds_audit.py` and `tests/test_central_instrument_and_dual_weight_bounds_audit.py`, covering `## 2026-10-21 Complete Central Instrument Contract` in `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Complete Central Instrument & Group-Inversion vs Lie-Coordinate Negation Equivalence (`verify_central_regular_instrument_and_inversion_equivalence`)**:
   - Uses the actual direct product $G = \mathbb{F}_5 \times \text{Heis}_3(\mathbb{F}_5)$ ($|N| = 125, |T| = 25, |C| = 5$), a verified cyclic transverse subgroup, and a nonlinear PUBLIC normal-first chart.
   - Constructs the density matrix from equality of independently assigned ordinary $gH$ labels: `125` fibers of size `5`. Checks subgroup closure, trivial normal intersection, chart inverses and `3125` right-action identities. The potential is derived from the shared section word only AFTER the oracle equality table is built.
   - Exact Frobenius difference between normal group inversion $n \mapsto n^{-1}$ + positive central Fourier (`CentralRegularSource.amplitude`) and negative central Fourier + logarithmic coordinate negation $(a, b) \mapsto (-a, -b)$: `0.0`.
   - Instrument completeness Frobenius error: `2.31e-15`; regular branch error: `1.00e-15`; oracle source contraction error: `6.94e-18`.
   - Every central label $\lambda \in \mathbb{F}_5$ (including $\lambda = 0$) has numerical mass `0.20000000000000004`, agreeing with the exact theoretical value $1/|C|$. The reducible carrier expression $|T|^2/|N| = 5.0$ is invalid.
2. **Nontrivial $H \cap C$ Zero-Mass Label Falsifier (`verify_nontrivial_central_intersection_zero_mass_obstruction`)**:
   - When $H \cap C = \langle (1, 2) \rangle \le \mathbb{F}_5^2$ is nontrivial (bypassing recursive intersection learning), `20/25` central labels have zero branch mass (`max_probability = 4.63e-34`), while only the `5` labels in $(H \cap C)^\perp$ survive with mass `0.2`.
3. **Dual-Weight Filtered-Polynomial Compiler Bounds (`verify_dual_weight_class_three_phase_bounds`)**:
   - Pins `compile_full_jet_phase` to `QSearch.ClassThreePhaseBounds.operational_bound` ($\le \max(c, 3D)$) and `parameter_bound` ($\le 2$) (`formal/Formal/ClassThreePhaseBounds.lean`) across $p \in \{11, 17, 2^{127} - 1\}$.

## 2. Dual-Weight Compiler Bounds Summary Table

| Prime Bits | Jet Degree $D$ | Central Degree $c$ | Attained / Bound Operational Weight $\max(c, 3D)$ | Attained Parameter Weights $w_{\text{param}}$ | Central Params in Degree-2 Lifts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `4` | `2` | `4` | `6 / 6` | `[1, 2]` (max `2`) | `False` |
| `5` | `3` | `5` | `9 / 9` | `[1, 2]` (max `2`) | `False` |
| `127` | `2` | `4` | `6 / 6` | `[1, 2]` (max `2`) | `False` |

## 3. Explicit Scope Boundaries

- Version 1 built its purported ordinary source directly from a chosen nonlinear potential, without specifying a compatible group/subgroup/chart. Its matrix agreement was only a potential-kernel contraction check. Version 2 replaces that circular source fixture with actual group cosets; no theorem is inferred from the old fixture.
- A nonlinear potential is allowed after a verified public section change. Its graph in the STANDARD direct-product coordinates need not be a subgroup. The regression test distinguishes these statements; it does not ban nonlinear potentials.
- This nonlinear public section does NOT satisfy the linear Lie-section premise used to derive the full algorithm's ambient degree bounds. The general central-instrument theorem permits it, but this fixture does not verify the full-jet algorithm's input premises.
- This source control uses class-two Heisenberg N. It is not a class-three/vector-center source-to-B-Fourier composition theorem. The existing independent class-three controls and the universal Lean results retain their separate scopes.
- Related literature context: [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016) for fixed-degree polynomial phase erasure; [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2) for state-symmetry reductions.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.

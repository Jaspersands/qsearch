# Public Full-Jet Complement Pullback and Weighted Triangular Matrix Law Audit

2026-10-21. **Standalone executable verification of `Formal/FullJetAlignment.lean`, `Formal/WeightedPhaseErasure.lean`, and `Formal/FullJetWeightedErasure.lean` contracts; not an admitted speedup candidate or novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/full_jet_complement_and_weighted_pullback_audit.py` and `tests/test_full_jet_complement_and_weighted_pullback_audit.py`, covering the newly added contracts in `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Public Left-Inverse Split & Changed-Complement Phase Pullback (`verify_full_jet_complement_and_phase_pullback_law`)**:
   - Verifies at $p = 11$ (`4` bits) and $p = 2^{127} - 1$ (`127` bits) that `split(T, P)` decomposes $\mathbb{F}_p^R = T(\mathbb{F}_p^J) \oplus \ker P$ ($R = 12, J = 6, S = 6$).
   - Verifies that changing the public complement basis on $\ker P$ (or updating the left inverse $P$) requires evaluating $\gamma$ at the **updated** inverse $L_2^{-1}(t, \zeta)$: stale phases compiled with $L_1^{-1}$ fail on `13/16` ($p=11$) and `16/16` ($127$-bit) trials, whereas re-indexed phases match `16/16`.
2. **Weighted Triangular Matrix Law & Equal-Weight Perturbation Falsifier (`verify_weighted_triangular_matrix_and_merged_character_law`)**:
   - Verifies `hdiag` ($M_{i,i} = s^{w_i}$), `hupper` ($M_{i,j} = 0$ for $i \ne j, w_i \le w_j$), `entry_on_or_above`, `merged_character`, and `constant_after_weight_one` at $p = 17, D = 2$ and $p = 2^{127} - 1, D = 3$.
   - Confirms that a diagonal-only check (`equal_weight_perturbation_diagonal_matches = True`) is insufficient when an equal-weight off-diagonal entry $M_{i,j} \ne 0$ ($w_i = w_j$) is present (`equal_weight_perturbation_rejected_by_merge = True`).

## 2. Control Summary Table

| Control Check | Small Prime ($p = 11 / 17$) | 127-Bit Prime ($p = 2^{127} - 1$) |
| :--- | :--- | :--- |
| Residual $\ker P$ projection checks passed | `10/10` | `10/10` |
| Stale-complement phase mismatches vs updated matches | `13/16` vs `16/16` | `16/16` vs `16/16` |
| `hdiag` & `hupper` & `entry_on_or_above` verified | `True` ($D=2$) | `True` ($D=3$) |
| `merged_character` & `constant_after_weight_one` verified | `12/12`, `True` | `12/12`, `True` |
| Equal-weight off-diagonal perturbation rejected | `True` | `True` |

## 3. Explicit Scope Boundaries

- Related literature context: [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016) for fixed-degree polynomial phase erasure; [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2) for quantum symmetry reductions.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.

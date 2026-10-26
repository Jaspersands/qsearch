# Arbitrary-$H$ Black-Box Oracle Pullback, Representative Cleanup vs Leaked-Workspace Verifier, and Total Recursive Resource Audit

2026-10-22. **Standalone executable verification of `Formal/RecursiveOracleReduction.lean`, advice-free black-box oracle pullback recursion, and multi-call arbitrary-$H$ resource composition; not an admitted speedup candidate or novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/arbitrary_h_recursive_oracle_and_resource_audit.py` and `tests/test_arbitrary_h_recursive_oracle_and_resource_audit.py`, addressing the next-step obligations in `research/CENTRAL_CHARACTER_DESCENT.md` (Section 6), `research/MECHANICAL_FOLLOW_UP_PLAN.md` (`## 2026-10-22 Mixed Central Descent Contract`), and `formal/Formal/RecursiveOracleReduction.lean`:

1. **Reversible Representative Cleanup vs Leaked-Workspace Falsifier (`verify_representative_cleanup_vs_leaked_workspace`)**:
   - Pins concrete $25 \times 25$ quotient density matrices on $Q = \text{UT}_3(\mathbb{F}_5) / K_0$ to `QSearch.RecursiveOracleReduction.cleaned_kernel`, `leaked_kernel`, `section_labels_equal`, and `clean_basis` (`formal/Formal/RecursiveOracleReduction.lean`).
   - Uncomputing the section representative $s(q)$ via `clean_oracle_step` returns scratch workspace to `0` and matches `groupEntry(H.map pi)` with Frobenius error `0.0`.
   - Two distinct non-homomorphic right-inverse sections $s_1, s_2 : Q \to G$ produce identical oracle labels across all $q \in Q$ (`section_labels_equal = True`).
   - Omitting the uncompute step (`leaked_kernel`) zeroes out every off-diagonal coset entry (`off_diagonal_frobenius_norm = 0.0`), collapsing the state to $I_Q / |Q|$ (`frobenius_error_vs_target = 0.4`).
2. **Advice-Free Black-Box Oracle Pullback Recursion (`solve_arbitrary_h_from_black_box_oracle`)**:
   - Takes **only** the black-box function `original_oracle(log_g)` (`target_h_advice_passed_to_solver = False`) and pulls it back through subalgebra restrictions and normalizer quotients $S = M / K_0$ via `clean_oracle_step`.
   - On $\mathfrak{ut}_4(\mathbb{F}_5)$ ($c = 3 < p = 5$) with non-transverse $H = \langle E_{01}, E_{02} \rangle$ ($H \cap \mathfrak{ut}_4' = \langle E_{02} \rangle \ne 0$, `n_in_normalizer_flags = [True]`), recovers $H$ exactly in `1` rebuilt tuple-oracle steps and `2` abelian base steps (`776` cleaned queries, `0` cleanup failures, max nested section depth `2`).
3. **Complete Arbitrary-$H$ Recursive Resource & `tree_budget` Audit (`audit_arbitrary_h_recursive_resource_and_tree_budget`)**:
   - Combines `deterministic_resource_profile` and `tree_budget` across all `5` sequential image steps on $\mathfrak{ut}_7(\mathbb{F}_p)$ ($p = 43$ and $p = 2^{127} - 1$), charging nested section compute/uncompute operations (`2 * depth * ell`) and bounding total additive queries by `ceil_log2 <= 256` ($p=43$) and `256` ($127$-bit), plus complete-instrument `tree_budget` trace distance `53/10000` (`269` total instrument calls).

## 2. Multi-Step Arbitrary-$H$ Recursion Resource Table on $\mathfrak{ut}_7(\mathbb{F}_p)$

| Recursion Step | Class $c$ | $\dim V$ ($m$) | $\dim J$ | Simplex Queries $\ell$ | Cleanup Ops $2 \cdot \text{depth} \cdot \ell$ | Step Query $\lceil \log_2 Q \rceil$ ($p=43$ / $127$-bit) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `N_derived_top` | `3` | `9` | `121` | `66` | `132` | `47` / `48` |
| `N_derived_restricted` | `2` | `6` | `8` | `8` | `32` | `14` / `17` |
| `M_mod_K0_top` | `5` | `6` | `710` | `330` | `1320` | `253` / `253` |
| `M_mod_K0_mid` | `3` | `7` | `72` | `45` | `180` | `44` / `45` |
| `M_mod_K0_bot` | `2` | `4` | `6` | `6` | `24` | `13` / `16` |

## 3. Explicit Scope Boundaries

- Related literature context: [Imran and Ivanyos (2023)](https://arxiv.org/pdf/2304.08376) for central subgroup-state conversion and recursive quotient descent; [Ivanyos and Santha (2015)](https://arxiv.org/pdf/1503.09016) for fixed-degree diagonal equations; [Decker, Ivanyos, Santha, and Wocjan (2011)](https://arxiv.org/abs/1107.2189) for tuple-query reductions; [Morales (2026)](https://arxiv.org/abs/2608.05321) for scalar-action semidirect products.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.

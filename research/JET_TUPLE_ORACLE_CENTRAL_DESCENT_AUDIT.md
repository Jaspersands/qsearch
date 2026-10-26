# Deterministic Tuple-Oracle to Nondestructive Central-Character Descent and Arbitrary-$H$ Filtered-Chart Rebuild Audit

2026-10-22. **Standalone executable verification of `Formal/JetOracleHomogenization.lean`, `Formal/CentralCharacterDescent.lean`, and `JET_ORACLE_HOMOGENIZATION.md` contracts; not an admitted speedup candidate or novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/jet_tuple_oracle_central_descent_audit.py` and `tests/test_jet_tuple_oracle_central_descent_audit.py`:

1. **Nondestructive Central-Character Instrument vs Phase-Dropping Quotient Fallacy (`verify_nondestructive_central_instrument_vs_dropped_phase`)**:
   - Pins concrete $343 \times 343$ density matrices on $G = Q \times Z_d$ ($p = 7, d = 2$) to `QSearch.CentralCharacterDescent` (`formal/Formal/CentralCharacterDescent.lean`).
   - Exact Frobenius error of nondestructive full-register central projection (`projectedEntry` + `actionOutput` + `cancelled_tensor` with `1` zero-scale slot discarded) against the target $U$-coset state on $Q$: `2.46e-15`; Frobenius difference against the equivalent phase-aware twisted quotient action: `2.58e-15`.
   - Dropping the central coordinate $Z_d$ and applying plain unphased quotient multiplication fails with Frobenius error `0.34992711`.
   - Applying the same cancelling SDE scales to a non-dilation-invariant subgroup $H_{\text{bad}}$ collapses the surviving coset support from `7` to `1`.
2. **Tuple-Oracle to Grade-1 Abelian Recovery (`verify_tuple_oracle_to_abelian_recovery`)**:
   - On $\mathfrak{ut}_3(\mathbb{F}_5)$ ($c = 2 < p = 5$), `make_oracle_plan` uses $\ell = 4$ deterministic simplex queries (`jet_dimension = 4`).
   - After erasing grade-2 central coordinates ($r_2 = 1$), the terminal grade-1 abelian group $V \oplus J_1$ has dimension $m + r_1 = 5$, recovering generator `[1, 2, 3, 2, 1]` and projecting onto $V$ to recover $U = \langle [1, 2] \rangle$.
3. **Unrolled Arbitrary-$H$ Normalizer Quotient & Mandatory Filtered-Chart Rebuild (`unrolled_tuple_oracle_arbitrary_h_solve`)**:
   - Recovers non-transverse $H = \langle E_{01}, E_{02} \rangle \le \mathfrak{ut}_7(\mathbb{F}_{19})$ ($H \cap \mathfrak{ut}_7' = \langle E_{02} \rangle \ne 0$, `n_in_normalizer_flags = [True, False]`) in `5` rebuilt `make_oracle_plan` image calls and `3` abelian base calls, enforcing Lie-subalgebra closure on `5` subgroup outputs and certifying $H_S \cap S' = 0$ on every rebuilt chart.

## 2. Rebuilt Filtered-Chart Log Across $\mathfrak{ut}_7(\mathbb{F}_{19})$ Recursion

| Step | $\dim S$ | Class Drop | $\dim V$ ($m$) | Rebuilt Normal Weights $w_i$ | $\dim J$ | Simplex Queries $\ell$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `1` | `15` | `3 -> 2` | `9` | `[3, 2, 2, 2, 2, 2]` | `121` | `66` |
| `2` | `7` | `2 -> 1` | `6` | `[2]` | `8` | `8` |
| `3` | `16` | `5 -> 3` | `6` | `[5, 4, 4, 3, 3, 3, 2, 2, 2, 2]` | `710` | `330` |
| `4` | `11` | `3 -> 2` | `7` | `[3, 2, 2, 2]` | `72` | `45` |
| `5` | `5` | `2 -> 1` | `4` | `[2]` | `6` | `6` |

## 3. Explicit Scope Boundaries

- Related literature context: [Decker, Ivanyos, Santha, and Wocjan (2011)](https://arxiv.org/abs/1107.2189) for tuple-query reductions and function-graph semidirect products; [Ivanyos, Sanselme, and Santha (2007)](https://arxiv.org/abs/0707.1260) for automorphism-twisted cancellation; [Imran and Ivanyos (2023)](https://arxiv.org/abs/2304.08376) for central subgroup-state conversion; [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016) for fixed-degree diagonal equations.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.

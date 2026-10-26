# Composed Full-Jet Erasure, Terminal Unit-Character Kernel, Non-Homomorphic Section Pullback, and Adaptive Resource Composition Audit

2026-10-21. **Standalone executable verification of `Formal/FullJetWeightedErasure.lean` (`degree_reduced_branch`, `terminal_kernel`), non-homomorphic section pullback right-invariance, and adaptive resource composition; not an admitted speedup candidate or novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/composed_full_jet_erasure_and_section_pullback_audit.py` and `tests/test_composed_full_jet_erasure_and_section_pullback_audit.py`:

1. **Composed Full-Jet Degree-Reduced Branch & Terminal Unit-Character Kernel (`verify_composed_degree_reduced_branch_and_terminal_kernel`)**:
   - Pins $625 \times 625$ density matrices on $\mathbb{F}_5 \times \text{Jets}(D=2)$ to `QSearch.FullJetWeightedErasure.degree_reduced_branch` and `terminal_kernel` (`formal/Formal/FullJetWeightedErasure.lean`).
   - Stage-2 weighted merge reduces weighted degree from `2` to `1` with branch Frobenius error `4.13e-23`; Stage-1 merge reduces weighted degree to `0` with nonzero outcome-dependent constant residual $c_0 = 3 \pmod 5$.
   - Verifies `terminal_kernel`: unit-modulus character $\chi(r) = \omega^r$ cancels $c_0$ identically (`frobenius_error = 1.37e-18`), whereas a non-unit character fails to cancel $c_0$ (`frobenius_error = 0.92936575`).
2. **Non-Homomorphic Quotient Section Pullback Audit (`verify_non_homomorphic_section_pullback_invariance`)**:
   - On $\text{UT}_4(\mathbb{F}_{11})$, a linear section $\sigma: M/K \to M$ fails the homomorphism law on `23/25` random pairs, yet when $K \le H$, the pulled-back oracle $f_S(s) = f(\sigma(s))$ is strictly right-$H_S$-invariant on `30/30` trials.
   - When $K \not\le H$ (erroneous recursive output), the non-homomorphic section defect escapes $H$ and breaks right-$H_S$ invariance on `24/30` trials.
3. **Twisted Non-Homomorphic Section Character Covariance (`verify_twisted_section_character_covariance`)**:
   - On $S = M_\chi / K_0$, verifies that when $K_0 = \ker \chi_K \subseteq \ker \chi_H$, the non-homomorphic section defect in $K_0$ cancels from $\chi_H(\sigma(s)^{-1} \sigma(s \cdot_S \bar{h})) = \chi_H(\sigma(\bar{h}))$ across `25/25` trials, whereas a mislearned character $\tilde{\chi}_K$ fails on `25/25` trials.
4. **Adaptive Resource Composition Ledger (`audit_adaptive_recursion_resource_composition`)**:
   - Verifies multiplicative arity composition within each step's two-stage phase-erasure tree and additive summation across sequential image steps (`log2_queries <= 36556.805` vs `49877.79` if erroneously multiplied across steps), while charging $2 \cdot C_{\text{lift}}$ reversible compute/uncompute gates per oracle call.

## 2. Adaptive Two-Stage Tree & Reversible Lift Ledger ($p = 19$)

| Step | Ambient Class $c$ | Jet Degree $D$ | Weighted Degree $e$ | Batch Sources $b_0$ | $\log_2$ Within-Tree Matrix Leaves $M$ | Reversible Lift Gates / $b_0$ Batch |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `1` | `6` | `4` | `12` | `607` | `36530.82` | `50988` |
| `2` | `5` | `3` | `9` | `112` | `10947.16` | `7616` |
| `3` | `4` | `2` | `6` | `32` | `2338.99` | `1792` |

## 3. Explicit Scope Boundaries

- Related literature context: [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016) for fixed-degree polynomial phase erasure; [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2) for state-symmetry reductions.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.

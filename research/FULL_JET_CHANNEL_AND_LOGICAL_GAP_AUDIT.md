# Full-Jet Hilbert-Space Channel Contraction Verifier and Logical-Gate Population-Gap / Baseline Audit

2026-10-21. **Concrete Hilbert-space density-matrix verification of the formal full-jet channel theorems and access-matched logical-gate gap audit; not an admitted speedup candidate or novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/full_jet_channel_and_logical_gap_audit.py` and `tests/test_full_jet_channel_and_logical_gap_audit.py`:

1. **Class-Three Monomial Partial Fourier Contraction (`verify_class_three_partial_fourier_density_contraction`)**:
   - Pins concrete $p^4 \times p^4$ density-matrix contractions ($p = 5$) to `QSearch.ClassThreeMonomial.partial_fourier_identity` (`formal/Formal/ClassThreeMonomial.lean`).
   - Max sector action Frobenius error: `3.39e-15`; max cross-sector leakage: `1.32e-15`; marginal probability per $\lambda \in \mathbb{F}_p^z$ (including $\lambda = 0$): `0.2`; $\mu$-traced off-diagonal norm for $\lambda \ne 0$: `4.42e-16`.
2. **Full-Jet Alignment Spectator Branch (`verify_full_jet_alignment_spectator_density_branch`)**:
   - Pins concrete $625 \times 625$ post-measurement branch density matrices ($p = 5, m = 1, D = 2, J = 3, R = 4, S = 1$, retaining $k = D$) to `QSearch.FullJetAlignment.fullJet_source_to_scalar` (`formal/Formal/FullJetAlignment.lean`), and verifies `align_full_jet` on `ClassThreeStructure` ($R = 8, J = 6$).
   - Spectator branch trace per outcome $u_0 \in \ker P$: `0.200000` ($p^{-S} = 1/5$); max Frobenius error against `curveRho(U, vectorJet(Q), scalarPhase)`: `0.00e+00`.
3. **Full Taylor Transport Mixed Branch & Negative $t$-Fourier Residual (`verify_full_taylor_transport_mixed_branch_density_contraction`)**:
   - Pins concrete $625 \times 625$ density matrices on $\mathbb{F}_p^m \times \text{Jets}(D=2)$ ($p = 5$) to `QSearch.FullTaylorTransport.fullJet_mixed_branch` (`formal/Formal/FullTaylorTransport.lean`).
   - Mixed-branch Frobenius error: `3.25e-23`; post-erasure negative $t$-Fourier residual Frobenius error: `1.86e-17`; maximum residual ordinary degree `2` (attaining $D = 2$ on the $k = D$ character: `True`).
4. **Logical-Gate Population-Gap & Access-Matched Baseline Audit (`certify_population_singular_value_gap`, `audit_logical_gate_access_matched_baselines`)**:
   - Verifies $\min_{|u|=1} \|A(a)V - u V B(b)\|_F^2 / d = 2(1 - |z(a, b)|) \ge \alpha \eta^2 / 2$ across marked ($\alpha = 1/d$, decaying as $O(1/(d p^2))$) vs balanced population-separated ($\alpha = 1/2$, constant $\gamma$ across $d$) encoders, alongside classical forward-encoder basis tomography ($d$ forward calls to $V|x\rangle$) and Pauli conjugation nilpotency invariance ($c = 2$).

## 2. Marked vs Balanced Population-Gap and Classical Basis Probing Table ($p = 5$)

| Logical $\dim d$ | Marked Exact $\gamma$ ($\alpha = 1/d$) | Marked Pop. Bound $\alpha \eta^2 / 2$ | Marked IID Choi Lower Bound ($s=2/3$) | Balanced Exact $\gamma$ ($\alpha = 1/2$) | Balanced Pop. Bound $\alpha \eta^2 / 2$ | Classical Basis Probing Forward Calls |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `4` | `0.139255` | `0.097169` | `1` | `0.190983` | `0.086373` | `4` |
| `8` | `0.078671` | `0.066129` | `1` | `0.190983` | `0.086373` | `8` |
| `16` | `0.041342` | `0.037957` | `1` | `0.190983` | `0.086373` | `16` |

## 3. Explicit Scope Boundaries

- Related literature context: [Bennett, Bernstein, Brassard, and Vazirani (1997)](https://arxiv.org/abs/quant-ph/9701001) for the $\Omega(\sqrt{d})$ oracle query lower bound; [Knill and Laflamme (1997)](https://arxiv.org/abs/quant-ph/9604034) for isometric subcode error-correction inheritance; [Cao and Lackey (2026)](https://arxiv.org/html/2603.03542v1) and [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2#S10) for encoding-tensor and state-symmetry reductions.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.

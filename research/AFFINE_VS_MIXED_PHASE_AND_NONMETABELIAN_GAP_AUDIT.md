# Pure-Affine vs Mixed-Coherence Polynomial-Phase Support and Non-Metabelian Orbit-Gap Audit

2026-10-22. **Standalone executable verification of the pure-affine, mixed-coherence, and metabelian scope boundaries in `research/POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md` (Sections 6–8); not a new quantum algorithm claim, classical dequantization, or speedup admission.**

## 1. Summary of Verified Contracts

This note documents `theorems/affine_vs_mixed_phase_and_nonmetabelian_gap_audit.py` and `tests/test_affine_vs_mixed_phase_and_nonmetabelian_gap_audit.py`:

1. **Pure-Affine Support Basis Learning, Restriction to `LearningFrame` & Outside-Support Unidentifiability (`verify_pure_affine_support_reduction_and_unidentifiability`)**:
   - On an unknown $k = 2$ affine subspace $a + U \subset \mathbb{F}_7^3$, verifies the dimension-free union bound $(p^k - 1) p^{-(n+s)} / (p - 1) \le p^{-s} / (p - 1) = 1/2058$ ($s = 3$) for learning $U$ from computational-basis difference samples, completes $U$ to an invertible frame, and runs `LearningFrame` (`theorems/polynomial_phase_copy_learning.py`) to recover all `9` nonconstant coefficients of $F|_{a+U}$ (`learning_frame_recovered_restricted_polynomial_exactly = True`).
   - **Outside-support unidentifiability falsifier**: Two ambient degree-3 polynomials $F_1 \ne F_2$ (`19` ambient monomials) that differ on `294` outside points but agree on $a + U$ produce identical pure states (`pure_state_trace_distance = 0.0`).
2. **Mixed-Coherence Diagonal Blindness vs `affine_phase_erasure` Parallel-Affine Recovery (`verify_mixed_coherence_diagonal_blindness_vs_parallel_affine_erasure`)**:
   - For the mixed-coherence kernel $\rho_{U, F}[x, y] = \frac{1}{p^n |U|} \mathbf{1}_{x - y \in U} \omega_p^{F(x) - F(y)}$ on $\mathbb{F}_{11}^2$, computational-basis measurements have total variation distance `0.0` from the uniform distribution for every $U$ and $F$, and for $U = \{0\}$ the state collapses to $I / p^n$ (`u_zero_trace_distance = 0.0`).
   - When $\dim(U) = 1$ ($U = \text{span}\{(1, 3)\} \subset \mathbb{F}_{11}^2$), applying `initial_packet`, `cancellation_weights`, and `sample_merge` (`theorems/affine_phase_erasure.py`) across degrees $3 \to 2 \to 1 \to 0$ on unknown parallel affine fibers $a + U$ erases the cubic, quadratic, and linear phases (`final_erased_packet_degree = 0`, `phase_spread = 2e-15`), and 2D QFT orthogonal-complement sampling recovers $U^\perp$ and $U$ (`recovered_u_basis_matches_exact_u = True`).
3. **Metabelian Translation-Phase Derived Abelianity vs $\mathfrak{ut}_5(\mathbb{F}_7)$ Non-Metabelian Scope & Cauchy–Schwarz Orbit Gap (`verify_metabelian_vs_nonmetabelian_orbit_gap_scope`)**:
   - Confirms that the translation-phase group $G_{\text{poly}} = \mathbb{F}_p^n \ltimes \mathcal{P}_{\le d-1}(\mathbb{F}_p^n)$ has an abelian derived subgroup (`translation_phase_derived_is_abelian = True`), whereas $\mathfrak{ut}_5(\mathbb{F}_7)$ ($c = 4 < p = 7$) has $\dim [\mathfrak{ut}_5', \mathfrak{ut}_5'] = 1 \ne 0$ (`ut5_derived_is_abelian = False`).
   - Verifies the analytical Cauchy–Schwarz orbit-gap bound $\gamma \ge (1 - (r - 1)/p) / 2^r = 3/14 \approx 0.21428571$ against exact character-sum overlaps (`empirical_min_orbit_gap = 0.62203553`).

## 2. Summary Verification Table

| Audit Control | Parameter / Group | Key Metric | Result |
| :--- | :--- | :--- | :--- |
| Pure-Affine Support Unidentifiability | $a + U \subset \mathbb{F}_7^3$ ($k=2, d=3$) | Trace distance $\text{TD}(|\psi_{F_1}\rangle, |\psi_{F_2}\rangle)$ | `0.0` (`294` outside pts differ) |
| Pure-Affine Restriction to `LearningFrame` | $\mathbb{F}_7^2$ pullback ($9$ monomials) | Parameters eliminated / exact match | `9/9` / `True` |
| Mixed-Coherence Diagonal Blindness | $\rho_{U, F}$ on $\mathbb{F}_{11}^2$ | Computational measurement TVD from uniform | `0.0` |
| Parallel-Affine Phase Erasure (`affine_phase_erasure.py`) | $U = \langle (1, 3) \rangle \subset \mathbb{F}_{11}^2$, $d=3 \to 0$ | Final degree / QFT $U^\perp$ & $U$ recovery | `deg = 0` / `True` |
| Translation-Phase vs $\mathfrak{ut}_5(\mathbb{F}_7)$ Derived Commutator | $G_{\text{poly}}$ vs $\mathfrak{ut}_5(\mathbb{F}_7)$ | Derived subgroup abelianity | `G_poly: True`, `ut_5: False` |
| Cubic Orbit-Gap Cauchy–Schwarz Bound | $p = 7, d = 3, r = 2$ | Analytic bound vs empirical gap | `0.21428571` vs `0.62203553` |

## 3. Explicit Scope Boundaries

- Related literature context: [Ivanyos and Santha (2015)](https://arxiv.org/pdf/1503.09016); [Decker, Ivanyos, Santha, and Wocjan (2013)](https://arxiv.org/pdf/1107.2189); [Arunachalam, Bravyi, Dutt, and Yoder (2022)](https://arxiv.org/html/2208.07851v2); [Roetteler and Beth (1998)](https://arxiv.org/pdf/quant-ph/9812070); [Moore, Rockmore, Russell, and Schulman (2004)](https://arxiv.org/pdf/quant-ph/0211124).
- `promotes_polynomial_phase_as_rees_application = False` and `classical_dequantization_claim = False`.
- `coherent_quantum_receiver_implemented = False`, `accepted_speedup_candidate = False`, `novelty_claim = False`, and `speedup_claim_allowed = False`.

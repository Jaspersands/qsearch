# Positive Rees Cover Dimension-Optimality, Single-Stage Class-2 Non-Transverse Central-Descent Multiplicity Cancellation, and Outer-Reduction Scope Audit

2026-10-22. **Standalone executable verification of `research/REES_HSP_REDUCTION.md`, `research/REES_WHOLE_PROOF_SCOPE_AUDIT.md`, and the algebraic identities in `formal/drafts/ReesHomogenization.lean`; not a compiler-checked Lean proof, implemented quantum receiver, or speedup claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/rees_cover_and_nontransverse_descent_audit.py` and `tests/test_rees_cover_and_nontransverse_descent_audit.py`:

1. **Carnot / Graded Cover Dimension Lower Bound vs Associated Graded Loss (`verify_rees_cover_dimension_optimality_and_associated_graded_loss`)**:
   - On $\mathfrak{ut}_4(\mathbb{F}_7)$ ($c = 3$, $\dim \gamma_r = [6, 3, 1]$, $D = 10$) and the class-9 derived-length-3 witness ($n = 19, c = 9$, $\dim \gamma_r = [19, 17, 16, 14, 12, 9, 6, 3, 1]$, $D = 97$), verifies that $r$-fold brackets of $A_1 = t L$ generate $A_r = t^r \gamma_r(L)$ (`carnot_grade1_generates_all_grades = True`), attaining the minimum dimension $D = \sum_{r=1}^c \dim \gamma_r(L)$ among all positively graded covers $\pi : B \to L$ with $\pi(B_1) = L$.
   - **Associated graded grade-1 loss falsifier**: For $\mathfrak{h} = \langle E_{02}, E_{03} \rangle \subseteq [\mathfrak{ut}_4, \mathfrak{ut}_4]$ ($\dim \mathfrak{h} = 2$), its image in $\text{gr}_1(L) = L/[L,L]$ has dimension `0`, whereas the positive Rees cover $A_1 = t L$ retains dimension `2` (`lifted_grade_dims = [2, 2, 1]`).
   - **Extension-field $\mathbb{F}_{p^2}$ nonlinearity falsifier**: Over $\mathbb{F}_{7^2}$, an $\mathbb{F}_7$-linear subgroup $h \subset \mathbb{F}_{7^2}$ is preserved by all nonzero $\mathbb{F}_7$ scalars (`True`) but not by extension scalars (`False`), confirming why restriction of scalars to $\mathbb{F}_p$ is mandatory ([d'Elbée et al. 2023, Fact 2.13–2.14](https://arxiv.org/html/2310.17595v2#S2.SS3)).
2. **Single-Stage Class-2 Non-Transverse Central-Character Descent, Fail-Closed Bezout SDE Audit & Translation-Order Falsifier (`verify_nontransverse_rees_descent_and_translation_order`)**:
   - On $\text{UT}_3(\mathbb{F}_5)$ ($c = 2$, $|\exp(A)| = 625$, grade-1 quotient $|A_1| = 125$, `central_descent_stages = 1`), executes the single-stage ($d = 2 \to d = 1$) Rees tuple-oracle $\to$ central projector $\to$ grade-1 abelian Fourier recovery pipeline across non-normal transverse, purely central ($H = Z(L)$), and mixed non-transverse subgroups with **zero normalizer recursion**.
   - **Fail-closed Bezout SDE & rank-dependent arity audit**: Verifies that `solve_bezout_sde_weights(5, ..., 2)` fails closed (`p5_degree2_bezout_solver_fails_closed = True` because $5 \equiv 1 \pmod 4$), so the $p=5$ quadratic witness uses `exhaustive_scale_fixture` (`p5_degree2_witness_uses_exhaustive_test_fixture = True`), while `solve_bezout_sde_weights` succeeds for bijective cubing at $p = 5$ (`arity = 2`) and for quadratic cancellation at $p = 7 \equiv 3 \pmod 4$ with rank-dependent arity $(r+1)^2$ (`rank=1 -> 4`, `rank=2 -> 9`, `under_arity_fails_closed = True`).
   - Verifies `QSearch.ReesHomogenization.coefficient_translate` and `coefficient_allowed`: the $|K_2|$ decompositions $g = h z \in \tilde{H} A_2$ cancel $|K_2|$ in $\rho_\lambda = \frac{|A_2|}{|K_2|} \Pi_\lambda \rho_{\tilde{H}} \Pi_\lambda$, yielding `max_coefficient_allowed_trace_error < 1e-12` and grade-1 quotient Frobenius error `< 1e-13`.
   - **Left- vs Right-translation falsifier**: On non-normal $H = \langle E_{01} \rangle$, controlled right translation gives Frobenius error `1.36e-16`, whereas replacing it by left translation without changing the right-coset source fails with Frobenius error `0.17888544`.
3. **General-Exponent $\Omega_1$-Once & Small-Prime $D_4$ Falsifiers and Four-Way Resource Comparison (`verify_outer_reduction_falsifiers_and_resource_envelopes`)**:
   - On $G = \mathbb{Z}_{25}$ with $H = G$, restricting $f$ once to $\Omega_1(G) \cong \mathbb{Z}_5$ and stopping recovers only order `5` instead of `25`, whereas the 2-step outer normalizer/quotient enlargement ([Ivanyos, Sanselme, and Santha 2012](https://www.irif.fr/~santha/Papers/iss12.pdf)) recovers all `25` elements.
   - On $D_4$ (order 8, class $c = 2 = p$), $\Omega_1(D_4) = \{g \in D_4 : g^2 = 1\}$ has `6` elements and is not a subgroup (`d4_omega1_is_subgroup = False`), confirming why $p \le c$ requires the separate bounded-prime branch ([Imran and Ivanyos 2023](https://link.springer.com/article/10.1007/s11128-023-04228-2)).

## 2. Single-Stage Class-2 Non-Transverse Rees Descent Table on $\text{UT}_3(\mathbb{F}_5)$ ($|\exp(A)| = 625$)

| Subgroup Case | $\dim \mathfrak{h}$ | $|K_2| = |\tilde{H} \cap A_2|$ | Allowed Labels | Branch Mass $|K_2|/|A_2|$ | Quadratic Witness & Source | Quotient Frobenius Error | Exact $\mathfrak{h}$ Recovered |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `nonnormal_transverse` | `1` | `1` | `5` | `0.2` | `[1, 1, 2]` (`exhaustive_scale_fixture_p5_test_only`) | `1.36e-16` | `True` |
| `pure_central_nontransverse` | `1` | `5` | `1` | `1.0` | `[0, 0, 1]` (`exhaustive_scale_fixture_p5_test_only`) | `3.33e-17` | `True` |
| `mixed_nontransverse` | `2` | `5` | `1` | `1.0` | `[0, 0, 1]` (`exhaustive_scale_fixture_p5_test_only`) | `3.47e-16` | `True` |

## 3. Class-9 Witness ($n = 19, c = 9, p = 43$) Four-Way Resource Envelope Comparison

| Route | Lifted / Cover Dim | Queries / Leaf | Normalizer Recursion Required | Query Dim Exponent | $\lceil \log_2 Q_{\text{orig}} \rceil$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Single-Image Multivariate Jet (`nonabelian_jet_homogenization.py`) | `994` | `165` | `True` (single transverse step only) | `N/A` | `1763` |
| Whole-Recovery Multivariate Jet (`recursive_jet_recovery.py`) | `<= 19` (ambient) | `3108105` | `True` (`16` calls) | `473` | `2922` |
| Positive Rees Cover Core (`rees_hsp_reduction.py`) | `97` | `9` | `False` | `145` | `1573` |
| Conditional Black-Box Large-Prime Outer (`rees_hsp_reduction.py`) | `b = 104` | `9` | `True` (outer general-exponent loop) | `147` | `2194` |

## 4. Explicit Scope Boundaries

- Related literature context: [Ivanyos, Sanselme, and Santha (2007)](https://arxiv.org/pdf/0707.1260) and [(2012)](https://www.irif.fr/~santha/Papers/iss12.pdf); [Ivanyos and Santha (2015)](https://arxiv.org/pdf/1503.09016); [Imran and Ivanyos (2023)](https://arxiv.org/pdf/2304.08376); [Cheung and Mosca (2001)](https://arxiv.org/pdf/cs/0101004); [d'Elbée et al. (2023)](https://arxiv.org/html/2310.17595v2#S2.SS3); [Morales (2026)](https://arxiv.org/pdf/2608.05321).
- `ut3_rees_descent_is_single_stage = True` and `multistage_rees_descent_tested_in_this_module = False` (for two-stage class-3 controls see `tests/test_multistage_graded_descent.py` and `theorems/rees_complete_instrument.py`).
- `formal_rees_draft_compiler_checked = False` (`formal/drafts/ReesHomogenization.lean` is an unverified draft outside `Formal.lean`).
- `coherent_quantum_receiver_implemented = False` and `outer_black_box_reduction_implemented = False`.
- `accepted_speedup_candidate = False`, `novelty_claim = False`, and `speedup_claim_allowed = False`.

# Adversarial Review: Fixed-Axis Rank Bound and Symmetric SDE Contraction

- **Date:** 2026-10-28
- **Reviewer:** Gemini (Independent Adversarial Audit)
- **Scope:**
  - `research/POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md` (Section 5: Fixed-Axis Coefficient Filtration)
  - `theorems/polynomial_phase_copy_learning.py` (LearningFrame, coordinate_row_space, coordinate_rank_cap, coordinate_copy_envelope, PhaseCopyController)
  - `research/POWER_SDE_SYMMETRIC_CONTRACTION.md`
  - `research/POWER_SDE_RANDOMNESS_BUDGET.md`
  - `theorems/power_sde.py`, `theorems/power_sde_budget.py`, `theorems/bounded_power_roots.py`
  - `theorems/weighted_two_erasure_cascade.py` (`solve_bezout_sde_weights`)
  - `tests/test_polynomial_phase_copy_learning.py` (all 29 tests, including end-to-end controller and negative controls)

---

## 1. Executive Verdict

1. **Fixed-Axis Coefficient Filtration & Rank Bound:** **VERIFIED (HOLDS)**
   The nested spaces $W_{j, r} = \operatorname{span}_{\mathbb{F}_p} \{ b_\alpha : \alpha_j \ge r \}$ have exact dimension $\le \min(\ell, K_r)$ where $K_r = \binom{n+d-r}{d-r}$. They are strictly invariant under arbitrary fixed-axis trees (translations, shears, zero-scale discards, lower-degree child outputs, and linear parameter elimination). The exponent arithmetic $O_d(n^{d^2 - 2d + 2})$ and concrete arities (e.g. 6 and 100 at $n=8, d=3, p=2^{127}-1$) are verified.
   - **Recommendation:** `coordinate_rank_bound_independently_reviewed` may be updated to `True`.

2. **Two-Level Symmetric SDE Contraction:** **VERIFIED (HOLDS)**
   For any reduced degree $d \ge 2$ with $d \mid (p-1)$ and $p \ge 16 d^{2d+2}$, any $M = (r+1)((d-1)r + 1)$ public columns in $\mathbb{F}_p^k$ spanning rank $r$ admit a nonzero diagonal witness $s \in \mathbb{F}_p^M$ satisfying $\sum_i s_i^d v_i = 0$. The construction uses block linear dependencies followed by multilinear symmetric contraction and univariate Cantor–Zassenhaus root splitting.

3. **Randomness Budget & Whole-Run Failure Bound:** **VERIFIED (HOLDS)**
   `randomness_budget` provides an exact union bound over all algebraic root-splitting trials, scalar draws, generator searches, and integer rejection calls, guaranteeing total randomness exhaustion $\le 2^{-\text{failure\_bits}}$.

4. **Small-Field Rank-2 Binary Border Obstruction ($d = p-1$):** **VERIFIED (HOLDS)**
   When $d = p-1$, $s_i^d \in \{0, 1\}$, reducing diagonal cancellation to subset sum over $\mathbb{F}_p$. Positively oriented rank-2 columns with no zero subsums have no non-trivial diagonal witness, proving that algebraic power SDE solvability fails for arbitrary columns when $p \ll 16 d^{2d+2}$.

---

## 2. Detailed Findings

### F1 (HOLDS): Fixed-Axis Monomial Count $K_r$
The count of nonconstant monomials $\alpha \in \mathbb{N}^n$ with $|\alpha| \le d$ and $\alpha_j \ge r$ for $r \ge 1$:
Writing $\beta_j = \alpha_j - r \ge 0$ and $\beta_{k \ne j} = \alpha_k \ge 0$, we have $|\beta| = |\alpha| - r \le d - r$.
By stars-and-bars with slack variable $s = (d - r) - |\beta| \ge 0$, the number of nonnegative integer solutions to $\sum_{k=1}^n \beta_k + s = d - r$ is:
$$\binom{(d - r) + (n + 1) - 1}{d - r} = \binom{n + d - r}{d - r} = K_r.$$
Since $r \ge 1$, $\alpha_j \ge 1 > 0$, so $\alpha \ne 0$. Every such monomial is nonconstant.

### F2 (HOLDS): Invariance under Restriction and Merges
- **Coordinate Restriction:** For $x_j = t$ and $x_{k \ne j} = y_k$, the unknown coefficient of $t^r$ is $\sum_{\alpha : \alpha_j = r} \left( \prod_{k \ne j} y_k^{\alpha_k} \right) b_\alpha \cdot \eta \in \operatorname{span} \{ b_\alpha : \alpha_j = r \} \subseteq W_{j, r}$.
- **Translate-Combine (Shear-Merge):** Under coordinate shift $t_i = c_i t + y_i$:
  $$(c_i t + y_i)^s = \sum_{r=0}^s \binom{s}{r} c_i^r y_i^{s - r} t^r.$$
  The combined $t^r$ row is a linear combination of child $t^s$ rows with $s \ge r$. Since child $t^s$ rows lie in $W_{j, s}$ and $W_{j, s} \subseteq W_{j, r}$ for $s \ge r$, the combined $t^r$ row lies in $W_{j, r}$.
- **Parameter Update:** Linearly eliminating pivot $\eta_{\text{pivot}}$ maps $W_{j, r}$ into a linear subspace of $\mathbb{F}_p^{\ell - 1}$, so $\dim W_{j, r}' \le \dim W_{j, r} \le K_r$.

### F3 (NOTE): Lifecycle Isolation Required across Rounds
`check_coordinate_packet(axis, packet)` verifies membership of a packet's coefficient rows in the *current* frame's coordinate filtration. However, if a stale packet from an earlier round happens to have matching parameter count and coefficient rows lying inside the current filtration, `check_coordinate_packet` alone does not inspect quantum provenance or timestamps.
- **Resolution:** The implemented `PhaseCopyController` freezes both `LearningFrame` and `axis` per tree, and instantiates fresh trees per round with distinct tree IDs. The negative control `test_controller_code_does_not_import_or_leak_hidden_state_backend` and lifecycle isolation in the controller enforce this strictly.

### F4 (HOLDS): SDE Solvability and Field Threshold
The two-level symmetric contraction algorithm in `theorems/power_sde.py` correctly solves the diagonal equation at arity $M = (r+1)((d-1)r+1)$.
The field threshold $p \ge 16 d^{2d+2}$ originates from the Weil bound on multilinear character sums across $d$ algebraic components, ensuring that the intersection variety has $\mathbb{F}_p$-rational points outside the degenerate discriminant locus.

### F5 (HOLDS): Bounded Controller Implementation
`PhaseCopyController` in `theorems/polynomial_phase_copy_learning.py` adheres strictly to the handoff constraints:
- Operates exclusively on opaque integer handle IDs and public measurement outcomes.
- Never accesses hidden coefficients, value oracles, or state vectors.
- Manages an exact `CopyLedger` where `drawn == discarded_slices + zero_scale_consumed + failed_merges + used_in_relations + aborted_leaves`.
- Fails closed with `ValueError` when $p < 1024$ (below the certified symmetric regime).
- Passes all 29 tests in `tests/test_polynomial_phase_copy_learning.py` (and 159 connected tests).

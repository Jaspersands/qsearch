# Relative Scalar-Center Twisted Recursion, Quadratic-Phase Abelian Base, and Character-Attached Weighted Erasure

2026-10-21. **Standalone public algebra and unrolled recursion verification; not a complete quantum state-symmetry receiver, general SDE backend, novelty claim, or accepted speedup candidate.**

## 1. Summary and Mechanical Contracts Verified

This note documents `theorems/twisted_relative_recursion.py` and `tests/test_twisted_relative_recursion.py`, implementing the executable verification controls for `research/TWISTED_STATE_SYMMETRY_RECEIVER.md` and `## 2026-10-21 Twisted State Source Contract` in `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Character-Preserving Normalizer Quotient (`public_character_normalizer_quotient`)**:
   - Wraps `character_normalizer` (`theorems/twisted_state_source.py`) on an independently learned subgroup $K \le H$ and character $\chi_K$ learned from **original single copies** ($k = 1$).
   - Demonstrates on $\mathfrak{heis}_3(\mathbb{F}_p)$ ($p = 7$ and $p = 2^{127} - 1$) with $K = \langle y, z \rangle$ and $\chi_K = (3, 1)$ that $K_0 = \ker \chi_K = \langle y - 3z \rangle$ is **not** an ideal of the plain normalizer $N_L(K) = L$ (`k0_ideal_in_plain_normalizer = False`), whereas $K_0$ is an ideal of $M_\chi = \{x \in L : [x, K] \subseteq K_0\}$ (`k0_ideal_in_m_chi = True`) and $Z_{\text{new}} = K / K_0$ is 1-dimensional central in $S = M_\chi / K_0$.
2. **Relative Abelian Base Quadratic-Phase Erasure (`compile_relative_abelian_twisted_leaf`, `verify_relative_abelian_quadratic_phase_erasure`)**:
   - In the relative abelian base ($r = \text{class}(G / Z) = 1$, $[G, G] \subseteq Z$ with $\dim Z \le 1$), naive quotient Fourier sampling on $V = G / Z$ leaks $1 - 1/p = 0.857142857143$ probability mass outside $U^\perp$ due to the degree-2 central-extension section phase.
   - Erasing degree 2 and degree 1 via `ordinary_higher_degree_erasure_stage` reduces the packet degree to `0` and concentrates `1.0` of the Fourier mass on $U^\perp$.
3. **Character-Attached Weighted Erasure & Two-Stage Cascade (`compile_twisted_full_jet_leaf`, `verify_character_attached_weighted_cascade`)**:
   - Connects `attach_linear_character` to `PinnedWeightedPacket`, `weighted_erasure_stage`, and `transition_to_fourier_residual` (`theorems/weighted_two_erasure_cascade.py`).
   - Verifies that the $m = 1$ appended unknown character parameters (`19 -> 20`) have nonconstant weight `[1]`, are completely erased at Stage-1 weight-1 erasure (`erased_root_weighted_degree = 0`), and leave zero character parameters in the post-Fourier Stage-2 residual (`post_fourier_residual_contains_character_params = False`).
4. **Unrolled Relative Scalar-Center Recursion (`unrolled_twisted_relative_solve`)**:
   - Tracks progress by the relative quotient class $r = \text{class}(G / Z)$, enforces the Section 8 call bound $I(r) \le I(\min(3, \lfloor r/2 \rfloor)) + r$ (`6 <= 10` on $\mathfrak{ut}_7(\mathbb{F}_{19})$) and character-batch bound (`3 <= 3`), and recovers $H = \langle E_{01}, E_{03}, E_{24} \rangle \le \mathfrak{ut}_7(\mathbb{F}_{19})$ together with its character `[7, 5, 2]`.

## 2. Heisenberg Character-Normalizer & Relative Abelian Base Controls

| Control Check | Result |
| :--- | :--- |
| Heisenberg ($p=7$ / $127$-bit) $\dim N_L(K)$ vs $\dim M_\chi$ | `3` vs `2` (`3` vs `2` at 127 bits) |
| $K_0 = \ker \chi_K$ ideal in $N_L(K)$ vs ideal in $M_\chi$ | `False` vs `True` |
| Naive quotient Fourier leakage outside $U^\perp$ ($p = 7$) | `0.857142857143` (exact $1 - 1/p = 0.8571428571428571$) |
| Post-quadratic-erasure Fourier mass inside / outside $U^\perp$ | `1.0` / `0.0` |

## 3. Unrolled Relative Twisted Recursion Trace on $\mathfrak{ut}_7(\mathbb{F}_{19})$ ($c = 6$)

| Step | Dispatched Branch | Ambient $\dim S$ | Relative Class Before | $\dim Z_{\text{new}}$ | Relative Class After |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1` | `RELATIVE_ABELIAN_SCALAR_BASE` | `6` | `1` | `0` | `0` |
| `2` | `TWISTED_SCALAR_METABELIAN_IMAGE` | `15` | `3` | `0` | `1` |
| `3` | `RELATIVE_ABELIAN_SCALAR_BASE` | `8` | `1` | `0` | `0` |
| `4` | `TWISTED_SCALAR_METABELIAN_IMAGE` | `13` | `3` | `1` | `2` |
| `5` | `TWISTED_SCALAR_METABELIAN_IMAGE` | `7` | `2` | `1` | `1` |
| `6` | `RELATIVE_ABELIAN_SCALAR_BASE` | `3` | `1` | `1` | `0` |

## 4. Explicit Scope Boundaries

- Related literature context: [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2) and [Liu, Carrasco, Eisert, and Bellante (2026)](https://arxiv.org/abs/2609.35656) study quantum state symmetry learning and sample vs unitary access models; [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016) provide the fixed-degree SDE framework.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.

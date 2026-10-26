# Sparse Symbolic-Scalar Phase-Erasure Adapter and Certified Class-Descent Controller

2026-10-21. **Standalone public classical controller and finite reference verification; not a coherent quantum circuit compiler, general-prime SDE backend, novelty claim, or accepted speedup candidate.**

## 1. Summary and Mechanical Gaps Closed

This note documents `theorems/symbolic_scalar_phase_erasure.py` and `tests/test_symbolic_scalar_phase_erasure.py`, closing two bounded mechanical gaps identified in `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Sparse `SymbolicScalarPacket` Adapter to Public Scalar Phase Erasure**:
   - Connects both `ut5_scalar_phase_compiler.compile_scalar_packet` and `class_four_scalar_phase_compiler.compile_variable_scalar_packet` (`SymbolicScalarPacket`) to cubic, quadratic, and linear phase erasure (`sparse_leading_columns`, `verify_diagonal_witness`, `sparse_cancellation_weights`, `sparse_translate_combine`, `sparse_degree_erasure_stage`) without materializing dense `1 + h + h(h+1)/2` lifted parameter tables or calling `evaluate_fixture`.
   - Checks declared provenance (`PinnedSymbolicPacket(instance_id, chart_id, packet, consumed)`), rejecting mismatched instances, charts, parameter bases, repeated wrapper objects within a merge and previously consumed wrappers. These checks cannot establish that the declared physical sources are fresh, independent or from the claimed oracle/chart; that remains a protocol obligation.
   - Uses arbitrary-precision `fmpz_mod_mat` row compression (`independent_columns_exact`) and capped conic square solving (`square_weights_capped`), supporting 127-bit primes ($p = 2^{127} - 1$) without machine-word overflow and verifying every diagonal witness against the original uncompressed equation columns.
2. **Standalone Certified Class-Descent Controller**:
   - Implements `PublicLieAlgebra`, `certified_class_descent_step`, and `certified_class_descent_controller` following Section 4 of `research/BOUNDED_CLASS_METABELIAN_HSP.md`.
   - Computes public derived charts $N = [S, S]$ (rejecting nonabelian derived ideals) and exact lower central series via `fmpz_mod_mat` over $\mathbb{F}_p$, accepting a subgroup restriction $\hat{T} = N + \hat{U}$ **if and only if** $\text{class}(\hat{T}) < \text{class}(S)$ (permitting valid strict support overestimates $\hat{U} \supsetneq U$ while rejecting dimension-only reductions that leave the nilpotency class unchanged).
   - Rotates `chart_id` at every accepted descent level so no phase packets carry across levels, and finishes in the terminal abelian ambient with a fixed abelian Fourier batch, original-oracle membership verification $f(g) = f(1)$ on every basis generator of $\hat{R}$, and inclusion of the verified initial normal intersection $K$.

## 2. Sparse Symbolic Erasure Verification

| Metric | Value |
| :--- | :--- |
| UT5 $(p=7, r=1, m=4)$ packet width $m + D$ | `14` |
| Base parameter count $h$ | `185` |
| Lifted parameter count $1 + h + h(h+1)/2$ | `17391` |
| Dense cubic equation count $P \cdot \binom{width+2}{3}$ | `9738960` |
| Active sparse cubic equations | `348` |
| Sparse equation compression ratio | `27985.52x` |
| Full $3 \to 2 \to 1 \to 0$ tree leaves ($p=11$) | `8281` |
| Erased root degree / remaining nonconstant terms | `0` / `0` |

## 3. Certified Class-Descent Verification (`class4-free-metabelian-p7`)

| Attribute | Value |
| :--- | :--- |
| Status | `SUCCESS` |
| Dimension trajectory | `[8, 7, 4, 3]` |
| Nilpotency class trajectory | `[4, 3, 2, 1]` |
| Chart trajectory | `['class4-free-metabelian-p7:level-0:dim-8:class-4', 'class4-free-metabelian-p7:level-1:dim-7:class-3', 'class4-free-metabelian-p7:level-2:dim-4:class-2', 'class4-free-metabelian-p7:level-3:dim-3:class-1']` |
| Quotient Fourier samples per level | `[1, 3, 1]` |
| Terminal abelian Fourier samples | `5` |
| Original-oracle membership queries | `2` |
| Recovered hidden generator basis | `[[1, 0, 1, 0, 0, 0, 0, 0]]` |
| Ideal-model certificate only | `True` |
| Unconditional noisy certificate | `False` |

## 4. Explicit Scope Boundaries

- `evaluate_fixture` is never called by `sparse_leading_columns`, `sparse_cancellation_weights`, `sparse_translate_combine`, or `certified_class_descent_controller`.
- The report's class-descent samplers use hidden fixture data to supply ideal Fourier rows. The erasure tree processes public polynomial descriptors, not quantum states. Neither is an end-to-end oracle-to-Fourier execution.
- Terminal membership verification certifies completeness only in the exact-source ideal model where $\hat{R} \supseteq H$; approximate-source underestimates that lose $H$ while still dropping class can return a proper subgroup of $H$. Accordingly, `unconditional_noisy_certificate` is `False`.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.

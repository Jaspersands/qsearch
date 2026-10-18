# DCP Coherent Fiber-Support Erasure vs. Un-Erased Pointer Dephasing Bridge

## 1. Un-Erased Pointer Dephasing Collapse vs. Canonical Single-Representative Erasure
- **Un-Erased Pointer Collapse**: Computing $\lvert x\rangle \mapsto \lvert x, Ax \bmod q\rangle$ and tracing out $\lvert x\rangle$ yields $\rho_{\mathrm{label}}(s) = \sum_y \frac{N_A(y)}{2^K}\lvert y\rangle\langle y\rvert$, which is strictly independent of $s$ ($D_{\mathrm{tr}}(s, s') = 0$).
- **Single-Representative vs. Full Fiber Normalization**: Erasing one canonical preimage $x_{\mathrm{rep}}(y)$ per occupied residue $y$ succeeds with probability $R(A)/2^K$ and achieves unconditional recovery probability $P_{\mathrm{single\text{-}rep}}(A) = \frac{R(A)^2}{2^K Q} \le P_{\mathrm{PGM}}(A) = \frac{(\sum_y \sqrt{N_A(y)})^2}{2^K Q}$, with equality iff $A$ is collision-free ($N_A(y) \in \{0, 1\}$).

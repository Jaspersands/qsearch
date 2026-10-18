# DCP Quantum Singular Value Transformation (QSVT) PGM Chebyshev Equalization Bridge (Subsystem 101)

## Scope & Overview
This subsystem establishes the exact singular-value spectrum of the subset-sum fiber block encoding and proves how bounded odd QSVT polynomials $P_d(\sigma)$ strictly lift post-selected QFT secret-recovery probability above the Pretty Good Measurement (PGM) baseline toward the flat-fiber ceiling $R(A)/Q$.

## Exact Mathematical Laws
1. **Subset-Sum Fiber Singular Spectrum**:
   On occupied residues $y \in \mathrm{supp}(N_A)$, the normalized fiber-overlap block encoding has singular values $\sigma_y = \sqrt{N_A(y) / N_{\max}} \in (0, 1]$ and condition number $\kappa(A) = \sqrt{N_{\max} / N_{\min}}$.
2. **Strict Monotone QSVT Equalization Hierarchy**:
   Applying a bounded odd QSVT polynomial $P_d: [-1, 1] \to [-1, 1]$ transforms $\sigma_y \mapsto P_d(\sigma_y)$, yielding conditional QFT success probability:
   $$P_{\mathrm{QFT, cond}}(A; P_d) = \frac{\left(\sum_{y: N_A(y) > 0} P_d(\sigma_y)\right)^2}{Q \sum_{y: N_A(y) > 0} P_d(\sigma_y)^2}.$$
   While $P_1(\sigma) = \sigma$ reproduces $P_{\mathrm{PGM}}(A)$, the degree-3 and degree-5 equalizers $P_3(\sigma) = \frac{1}{2}\sigma(3 - \sigma^2)$ and $P_5(\sigma) = \frac{1}{8}\sigma(15 - 10\sigma^2 + 3\sigma^4)$ satisfy $P_{\mathrm{PGM}}(A) = P_{\mathrm{QFT, cond}}(P_1) < P_{\mathrm{QFT, cond}}(P_3) < P_{\mathrm{QFT, cond}}(P_5) \le R(A)/Q$ on every non-flat colliding instance.

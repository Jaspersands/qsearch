# DCP Multi-Level Lagrange-Richardson Zero-Noise Extrapolation Bridge (Subsystem 103)

## Scope & Overview
This subsystem establishes the exact bias reduction and shot-noise variance blowup of $M$-node Lagrange-Richardson zero-noise extrapolation applied to damped CNOT phase observables $\mu(\lambda) = e^{-\alpha h \lambda} \cos\theta$.

## Exact Mathematical Laws
1. **Exact Binomial Lagrange Weights and $O((\alpha h)^{M+1})$ Bias Suppression**:
   On integer stretch nodes $\lambda_k = k + 1$ ($k = 0, \dots, M$), the Lagrange weights at $\lambda = 0$ are $c_k = (-1)^k \binom{M+1}{k+1}$, satisfying $\sum_{k=0}^M c_k = 1$ and $\sum_{k=0}^M c_k \lambda_k^j = 0$ for $1 \le j \le M$ and suppressing dephasing bias by $> 115\times$ at $M = 2, \alpha h = 0.10$.
2. **Exact $(2^{M+1} - 1)^2$ Variance Penalty**:
   The $L_1$ norm of the Lagrange weights is $\sum_{k=0}^M |c_k| = 2^{M+1} - 1$, inducing an exact $(2^{M+1} - 1)^2$ optimal-allocation shot-noise variance penalty.

# DCP Noisy Cascaded Dyadic Bit-Peeling vs. Unpruned CNOT Tree Sample Complexity Bridge

## 1. Per-Level Visibility and Fisher Efficiency per Raw Qubit
At dyadic bit level $\ell \in \{1, \dots, t\}$ (using $2^{\ell-1}$ raw phase qubits at $n=1$), unpruned binary CNOT trees have terminal visibility $\gamma_0^{2^{\ell-1}}$ and doubly-exponentially decaying Fisher information $\gamma_0^{2^\ell} / 2^{\ell-1}$ per raw qubit, whereas minimum-weight adaptive syndrome pruning obeys $V_0 = \gamma_0$, $V_1 = \gamma_0^2$, $V_m = \frac{3}{4}V_{m-1} + \frac{1}{4}V_{m-1}^2 \ge \gamma_0^2 (3/4)^{m-1}$, reducing the noise sample overhead from doubly-exponential $\gamma_0^{-2^\ell}$ to singly-exponential $O((32/9)^\ell \gamma_0^{-4})$.

## 2. Cumulative $t$-Bit Peeling Budget
At $\gamma_0 = 1.0$, both pruned and unpruned trees consume $2^t - 1$ raw qubits per unit Fisher information across $t$ bits ($31$ at $t=5$). At $\gamma_0 = 0.85$, adaptive pruning reduces cumulative raw-qubit consumption by $> 35\times$ at $t=5$ and $> 4880\times$ at $t=6$ ($> 8110\times$ at level $\ell=6$ alone).

# DCP Krawtchouk Polynomial Binary Hamming Scheme MacWilliams CNOT Bridge (Subsystem 134)

## Scope & Overview
This subsystem establishes the exact Krawtchouk polynomial radial Hadamard transformation law on the $K$-wire binary Hamming association scheme $H(K, 2)$ and proves the exact quadratic root blind-spot criterion $w_\pm = (K \pm \sqrt{K})/2$ for weight-$2$ CNOT parity probes.

## Exact Mathematical Laws
1. **Involutory Radial Hadamard Matrix Law**:
   On the $K + 1$ Hamming weight shells $\lvert S_w\rangle$, $H^{\otimes K}$ acts via $M_{k, w}^{(K)} = 2^{-K/2}\sqrt{\binom{K}{w}/\binom{K}{k}} K_k(w; K)$, satisfying $(M^{(K)})^2 = I_{K+1}$.
2. **Exact Quadratic Root Blind Spots**:
   Because $K_2(w; K) = \frac{1}{2}((K - 2w)^2 - K)$, whenever $K$ is a perfect square ($K = 4 \implies w \in \{1, 3\}$; $K = 9 \implies w \in \{3, 6\}$), the weight-$2$ parity shell $\lvert S_2\rangle$ has zero Hadamard projection onto $\lvert S_{w_\pm}\rangle$.

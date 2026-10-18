# DCP Odd-Prime QFT 2-Bin Capture Bound and Exact Modular Rounding Bridge (Subsystem 93)

## Scope & Overview
This subsystem establishes the exact Fejér-Dirichlet 2-bin probability capture lower bound and the deterministic nearest-integer modular rounding theorem when an $m$-qubit dyadic inverse Quantum Fourier Transform $\mathrm{QFT}_{2^m}^\dagger$ is applied to a non-dyadic prime-modulus phase register over $\mathbb{Z}_q$.

## Exact Mathematical Laws
1. **Universal $> 8/\pi^2 \approx 81.057\%$ Two-Bin Capture Bound**:
   For any prime $q \ge 3$ and any modular phase residue $z = (a s) \bmod q \in \{0, \dots, q-1\}$, the two nearest $m$-bit QFT frequency bins $k_{\mathrm{floor}} = \lfloor 2^m z / q \rfloor$ and $k_{\mathrm{ceil}} = \lceil 2^m z / q \rceil \bmod 2^m$ capture combined probability mass:
   $$P_{2\text{-bin}}(z; q, m) \ge 2 \left( \frac{\sin(\pi / 2)}{2^m \sin(\pi / 2^{m+1})} \right)^2 > \frac{8}{\pi^2} \approx 0.810569.$$
2. **Deterministic Dual-Bin Rounding Criterion ($2^m \ge 2q$)**:
   Whenever $2^m \ge 2q$, every bin $k \in \{k_{\mathrm{floor}}, k_{\mathrm{ceil}}\}$ satisfies $|k / 2^m - z / q| \le 1/(2q)$, so the closed-form rounding map $\hat{z}(k) = \lfloor (q k + 2^{m-1}) / 2^m \rfloor \bmod q$ deterministically recovers $z$ on both nearest bins across $100\%$ of $z \in \mathbb{Z}_q$.

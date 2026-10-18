# DCP Quantum $Z$-Error-Detection $\llbracket 2m+2, 2m, 2 \rrbracket$ Iceberg Stabilizer Code Bridge (Subsystem 113)

## Scope & Overview
This subsystem establishes the exact single-fault detection and $O(p^2)$ post-selected phase-error suppression law when $2m$ compressed DCP survivor wires are encoded into the $\llbracket 2m + 2, 2m, 2 \rrbracket$ Iceberg stabilizer code using $2$ ancilla qubits.

## Exact Mathematical Laws
1. **Weight-2 Logical Phase Rotations & $100\%$ Single-Fault Detection**:
   Each logical phase operator $\bar{Z}_j = Z_0 Z_j$ ($1 \le j \le 2m$) commutes with $S_X = X^{\otimes (2m+2)}$ and $S_Z = Z^{\otimes (2m+2)}$, while every single-qubit Pauli fault anticommutes with at least one stabilizer.
2. **Exact Post-Selected Logical Error Formula**:
   Under independent phase-flip rate $p$, post-selecting on $S_X = +1$ accepts with probability $P_{\mathrm{acc}}(p) = \frac{1}{2}(1 + (1 - 2p)^{2m+2})$ and reduces logical error from $1 - (1-p)^{2m}$ to $1 - \frac{(1-p)^{2m+2} + p^{2m+2}}{P_{\mathrm{acc}}(p)} = \binom{2m+2}{2}p^2 + O(p^3)$ ($> 26.5\times$ suppression at $p = 0.01$ on $\llbracket 6, 4, 2 \rrbracket$).

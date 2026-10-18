# DCP Clifford Stabilizer Rényi-2 Magic Monotone Carry Injection Bridge (Subsystem 95)

## Scope & Overview
This subsystem quantifies the exact stabilizer Rényi-2 magic $M_2(\lvert \psi\rangle) = -\log_2(2^{-m}\sum_{P \in \mathcal{P}_m} |\langle \psi \rvert P \lvert \psi\rangle|^4)$ injected by binary-XOR carries across the modulo-$2^t$ hierarchy on $m$ overlapping CNOT wires.

## Exact Mathematical Laws
1. **Exact Stabilizer Invariance ($M_2 = 0$) at $t = 1$ ($\bmod 2$) and $t = 2$ ($\bmod 4$)**:
   At $t = 1$ and $t = 2$, the state $\lvert \psi_{t, m}\rangle = 2^{-m/2}\sum_{u \in \{0,1\}^m} e^{2\pi i (u_1 \oplus \dots \oplus u_m)/2^t}\lvert u\rangle$ is a pure stabilizer state ($Z$-product state at $t=1$; $\mathrm{CZ}$-graph state at $t=2$) with $M_2 = 0$ for all $m \ge 1$.
2. **Strict Non-Clifford Magic Injection at $t = 3$ ($\bmod 8$)**:
   At $t = 3$ ($\bmod 8$), $\lvert \psi_{3, m}\rangle$ injects exact stabilizer Rényi-2 magic $M_2 = \log_2(4/3) \approx 0.415037$ bits, while the isolated 3-body carry state $\mathrm{CCZ}\lvert +\rangle^{\otimes 3}$ carries $M_2 = \log_2(16/9) \approx 0.830075$ bits.

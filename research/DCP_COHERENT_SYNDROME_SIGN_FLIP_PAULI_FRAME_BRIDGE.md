# DCP Coherent Pauli-$X$ Label-Negation and Multi-Stage Sign-Rectified CNOT Routing Bridge

## 1. Exact Density-Matrix Label-Negation Identity
Conjugating any single-qubit DCP phase state $\rho(\theta, \gamma)$ by the secret-independent Pauli-$X$ gate cancels the pure-state global phase $e^{i\theta}$ and negates the phase angle identically:
$$X \, \rho(a, s, \gamma) \, X = \rho(-a \bmod q, s, \gamma).$$

## 2. Sign-Rectified Stage-2 CNOT Alignment at Level $k = 3$ ($\bmod 8$)
For two Stage-1 wires with $\tilde{A}_1(y_1), \tilde{A}_2(y_2) \in \{2, 6\} \pmod 8$, applying a syndrome-conditioned Pauli-$X$ gate on Wire 2 whenever $\tilde{A}_1(y_1) \equiv \tilde{A}_2(y_2) \pmod 8$ negates $\tilde{A}_2 \mapsto -\tilde{A}_2 \pmod{2^t}$ and aligns the $d_2 = 0$ Stage-2 CNOT branch to $\tilde{A}_1 + (-\tilde{A}_2) \equiv 0 \pmod 8$ across $100\%$ of pairs (vs. $50\%$ without Pauli-$X$ rectification).

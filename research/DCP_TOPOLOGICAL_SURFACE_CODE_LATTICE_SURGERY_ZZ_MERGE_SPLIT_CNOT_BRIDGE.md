# Subsystem 155: Topological Surface Code Lattice Surgery $ZZ$-Merge & $XX$-Split CNOT Bridge

## 1. Mathematical Formulation
Starting from an arbitrary two-qubit input $|\psi\rangle_{CT}$ and ancilla $|+\rangle_A$, logical CNOT via lattice surgery performs three projective measurements with outcomes $(m_{ZZ}, m_{XX}, m_Z) \in \{0,1\}^3$:
1. Rough boundary merge measuring $Z_C Z_A$ ($m_{ZZ} \in \{0,1\}$),
2. Smooth boundary split measuring $X_A X_T$ ($m_{XX} \in \{0,1\}$),
3. Destructive ancilla readout measuring $Z_A$ ($m_Z \in \{0,1\}$).

Direct evaluation of the 8 Kraus operators $K(m_{ZZ}, m_{XX}, m_Z) = \langle m_Z|_A P_{XX}(m_{XX}) P_{ZZ}(m_{ZZ}) |+\rangle_A$ yields:
$$K(m_{ZZ}, m_{XX}, m_Z) = \frac{1}{2\sqrt{2}} (-1)^{m_{XX}(m_{ZZ} \oplus m_Z)} Z_C^{m_{XX}} X_T^{m_{ZZ} \oplus m_Z} \mathrm{CNOT}_{C \to T}.$$
Thus the exact Pauli byproduct correction is $Z_C^{m_{XX}} X_T^{m_{ZZ} \oplus m_Z}$ (up to the deterministic global sign $(-1)^{m_{XX}(m_{ZZ} \oplus m_Z)}$), whereas the naive two-bit formula $Z_C^{m_{ZZ}} X_T^{m_{XX}}$ fails on $6/8$ measurement branches.

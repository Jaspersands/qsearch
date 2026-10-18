# DCP Coherent $M$-Representative Fiber Concentration and Monotone PGM Interpolation Bridge (Subsystem 85)

## Scope & Overview
This subsystem generalizes single-representative subset-sum fiber erasure (Subsystem 82) to a coherent $M$-representative concentrator $W_y^{(M)}$ on the $K$-wire pointer + $n$-dit label state:
$$\lvert \Psi(s) \rangle = 2^{-K/2} \sum_{x \in \{0,1\}^K} e^{2\pi i \langle Ax, s \rangle / q} \lvert x \rangle_K \lvert Ax \bmod q \rangle_Y.$$

## Exact Mathematical Laws
1. **Coherent $M$-Representative Amplitude Concentration**:
   For each occupied residue $y \in \mathbb{Z}_q^n$ with fiber $F_A(y) = \{x \in \{0,1\}^K : Ax \equiv y \pmod q\}$ of size $N_A(y) \ge 1$, coherently rotating the uniform superposition over $m_y = \min(M, N_A(y))$ known representatives $\{x_1(y), \dots, x_{m_y}(y)\} \subseteq F_A(y)$ into $\lvert 0^K \rangle_K$ transfers exact amplitude $\sqrt{m_y / 2^K} e^{2\pi i \langle y, s \rangle / q}$ into the unentangled branch $\lvert 0^K \rangle_K \lvert y \rangle_Y$.
2. **Exact Monotone Interpolation Law**:
   Measuring the label register in the $\mathrm{QFT}_Q^\dagger$ basis on the erased branch yields exact secret-recovery probability:
   $$P_{\mathrm{QFT}}^{(M)}(A) = \frac{1}{2^K Q} \left( \sum_{y \in \mathbb{Z}_q^n} \sqrt{\min(M, N_A(y))} \right)^2,$$
   which monotonically interpolates between single-representative erasure ($M=1$: $R(A)^2 / (2^K Q)$) and the information-theoretic Pretty Good Measurement optimum ($M \ge \max_y N_A(y)$: $P_{\mathrm{PGM}}(A)$).
3. **Constant-Multiplicity Staircase**:
   On the multiplicity-$4$ surjective instance $A = [[1, 1, 2, 2]] \bmod 4$ ($N_A(y) = 4$ for all $y \in \mathbb{Z}_4$), $P_{\mathrm{QFT}}^{(M)}(A) = \min(M, 4)/4$ steps linearly through $0.25, 0.50, 0.75, 1.00$ for $M = 1, 2, 3, 4$.

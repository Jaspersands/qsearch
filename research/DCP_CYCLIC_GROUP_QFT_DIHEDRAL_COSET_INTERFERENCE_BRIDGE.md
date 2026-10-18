# DCP Cyclic-Group $\mathrm{QFT}_{2^m}$ Dihedral Coset Interference Bridge

## 1. Exact Closed-Form Product Identity
For any $m$-wire product phase state $|\psi(\theta_0, \dots, \theta_{m-1})\rangle$ interpreted as a state over $\mathbb{Z}_{2^m}$ via $U = \sum_{j=0}^{m-1} u_j 2^j$, applying $\mathrm{QFT}_{2^m}^\dagger$ produces the exact outcome distribution:
$$P_{\mathrm{QFT}_{2^m}}(K \mid \theta) = \prod_{j=0}^{m-1} \cos^2\!\left(\frac{\theta_j}{2} - \frac{\pi K}{2^{m-j}}\right), \qquad K \in \{0, \dots, 2^m - 1\}.$$
- **Dyadic Progression Constructive Control**: When $\theta_j = 2\pi \cdot 2^j K_0 / 2^m \pmod{2\pi}$, $P_{\mathrm{QFT}_{2^m}}(K_0) = 1.0$.
- **Non-Dyadic Conflict**: For $\theta = (\pi, \pi, \pi)$, wire $j=2$ forces $K$ odd while wire $j=1$ forces $K \equiv 2 \pmod 4$, preventing unit concentration.

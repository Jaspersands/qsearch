# DCP Coset-Subspace $H^{\otimes m}$ Concentration and Leakage Bridge

## 1. Exact Product Readout & Total-Variation Law
For $|\psi(s; \tilde{A})\rangle = 2^{-m/2} \sum_{u \in \{0,1\}^m} \exp(\frac{2\pi i}{2^t}\langle \tilde{A} u, s \rangle) |u\rangle$ with $\theta_j(s) = \frac{2\pi}{2^t}\langle \tilde{A}_j, s \rangle$:
$$P_{H^{\otimes m}}(z \mid \tilde{A}, s) = \prod_{j=1}^m \cos^2\!\left(\frac{\theta_j(s) - \pi z_j}{2}\right), \qquad D_{\mathrm{TV}}\left(P_{H^{\otimes m}}(\cdot \mid \tilde{A}, s), \delta_{0^m}\right) = 1 - \prod_{j=1}^m \cos^2\!\left(\frac{\theta_j(s)}{2}\right).$$
- **Half-Period Constructive Control**: When $\langle \tilde{A}_j, s \rangle \equiv 2^{t-1} b_j \pmod{2^t}$, $H^{\otimes m}$ outputs $z = b \in \{0,1\}^m$ with probability $1.0$.
- **Carry-Leakage Regime**: Non-half-period phases $\theta_j(s) \notin \{0, \pi\}$ factor into independent Bernoulli coin flips with bias $\cos(\theta_j(s))$.

# Subsystem 143: Quantum Linear Systems (HHL) Condition Number vs. Exact Modular $\mathbb{Z}_q$ Inversion Bridge

## 1. Mathematical Formulation
Embedding a modular syndrome system $H s \equiv b \pmod q$ into a continuous linear system $H s = b + q k$ ($k \in \mathbb{Z}^m$) for Harrow-Hassidim-Lloyd (HHL) inversion encounters two obstructions:
1. **Wrap-Around Ambiguity**: Computing $H^{-1} b$ over $\mathbb{R}$ fails whenever $k \neq 0$ (failing on $78.1\%$ of secrets for $H = \begin{pmatrix}1 & 5 \\ 1 & 6\end{pmatrix} \bmod 8$).
2. **Condition Number Penalty**: Even unimodular matrices ($\det H = 1$) exhibit arbitrarily large singular-value condition numbers $\kappa(H) = \sigma_{\max}/\sigma_{\min}$ ($\kappa \approx 62.98$, $P_{\text{succ}} \sim \kappa^{-2} \approx 2.52 \times 10^{-4}$), whereas reversible modular peeling $|b\rangle \mapsto |H^{-1} b \bmod q\rangle$ is a permutation unitary with $\kappa(U_H) = 1$.

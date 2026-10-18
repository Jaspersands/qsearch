# DCP Multi-Copy Distinct-Header Cyclic-Swap and Schur-Weyl Bipartite Even-Flip Interference Bridge

## 1. Bipartite Even-Flip Cycle Theorem and $\lfloor r/2 \rfloor$ Degree Ceiling
Because every closed cyclic walk $x_1 \to x_2 \to \dots \to x_r \to x_1$ on $\{0, 1\}$ alternates $0 \leftrightarrow 1$ an even number of times $2m \le 2\lfloor r/2 \rfloor$, the $r$-cycle trace $\mathrm{Tr}\!\big(C_r (\rho_1 \otimes \dots \otimes \rho_r)\big)$ is strictly real, invariant under $s \mapsto -s \pmod q$, and expands purely over $2m$-element alternating subsets:
$$\mathrm{Tr}\!\big(C_r (\rho_1 \otimes \dots \otimes \rho_r)\big) = \frac{1}{2^{r-1}}\left[1 + \sum_{m=1}^{\lfloor r/2 \rfloor} \sum_{1 \le j_1 < k_1 < \dots < j_m < k_m \le r} \left(\prod_{l=1}^m \gamma_{j_l}\gamma_{k_l}\right) \cos\!\left(\sum_{l=1}^m (\theta_{j_l} - \theta_{k_l})\right)\right].$$

## 2. Three-Copy Pairwise Collapse ($r=3$) vs. Weight-Changing GHZ Escape
Since $\lfloor 3/2 \rfloor = 1$, projecting $3$ distinct headers onto $\mathrm{Sym}^3(\mathbb{C}^2)$ yields $\mathrm{Tr}(\Pi_{\mathrm{Sym}^3}\rho_{123}) = \frac{1}{2} + \frac{1}{6}\sum_{1 \le j < k \le 3}\gamma_j\gamma_k\cos(\theta_j - \theta_k)$, which is strictly invariant under common phase shifts $\theta_j \mapsto \theta_j + \delta$ and contains zero 3-body sum harmonics $\theta_1 + \theta_2 + \theta_3$ (unlike weight-changing CNOT/GHZ observables outside $\mathbb{C}[S_r]$).

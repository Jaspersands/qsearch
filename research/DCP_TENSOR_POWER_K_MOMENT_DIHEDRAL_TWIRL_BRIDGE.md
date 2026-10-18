# DCP $r$-Copy Secret-Twirled Tensor-Power Density Matrix and Ternary Kernel Moment Bridge

## 1. Exact Ternary Zero-Sum Frobenius Law
For the secret-twirled $r$-copy state $\bar{\rho}^{(r)}(A) = \mathbb{E}_{s \sim \mathrm{Unif}(\mathbb{Z}_q^n)}[\bigotimes_{j=1}^r \rho(a_j, s, \gamma_j)]$:
$$\left\| \bar{\rho}^{(r)}(A) - \frac{I_{2^r}}{2^r} \right\|_F^2 = \frac{1}{2^r} \sum_{\substack{0 \ne \delta \in \{-1, 0, +1\}^r \\ A \delta \equiv 0 \pmod q}} \prod_{j : \delta_j \ne 0} \left(\frac{\gamma_j^2}{2}\right).$$

## 2. Universal Unit-Entry Ensemble Identity Across All Moduli $q \ge 2$
Because every non-zero coordinate of $\delta \in \{-1, 0, +1\}^r \setminus \{0^r\}$ is $\pm 1 \in \mathbb{Z}_q^\times$, $\mathbb{P}_A[A\delta \equiv 0 \pmod q] = q^{-n}$ holds for all $3^r - 1$ non-zero ternary vectors across both dyadic and odd-prime moduli, yielding:
$$\mathbb{E}_{A \sim \mathrm{Unif}(\mathbb{Z}_q^{n \times r})}\!\left[\left\| \bar{\rho}^{(r)}(A) - \frac{I_{2^r}}{2^r} \right\|_F^2\right] = \frac{\prod_{j=1}^r (1 + \gamma_j^2) - 1}{2^r \, q^n}.$$

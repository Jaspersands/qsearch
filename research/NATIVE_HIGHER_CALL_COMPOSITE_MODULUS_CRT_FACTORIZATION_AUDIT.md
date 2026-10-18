# Native Higher-Call Composite-Modulus CRT Factorization Audit

## 1. Exact Results
1. **Twisted Frequency CRT Factorization**:
   For coprime $q = q_1 q_2$ ($\gcd(q_1, q_2) = 1$), $\omega_q^{y z} = \omega_{q_1}^{y_1 z_1} \omega_{q_2}^{y_2 z_2}$ with $z_i = z \bmod q_i$ and $y_1 = y (q_2^{-1} \bmod q_1) \bmod q_1$, $y_2 = y (q_1^{-1} \bmod q_2) \bmod q_2$.
2. **Product-Channel Valid-Check Factorization**:
   When $P_q(e) = P_{q_1}(e \bmod q_1) P_{q_2}(e \bmod q_2)$, both $\hat{P}_q(y) = \hat{P}_{q_1}(y_1) \hat{P}_{q_2}(y_2)$ and $P_{\mathrm{valid}}^{(q)}(B) = P_{\mathrm{valid}}^{(q_1)}(B \bmod q_1) P_{\mathrm{valid}}^{(q_2)}(B \bmod q_2)$ factor identically.
3. **Archimedean Contiguous-Window Coupling Control**:
   When $P_q(e)$ is supported on a contiguous archimedean window $W = \{0, 1\} \subset \mathbb{Z}_6$ whose size is not divisible by $q_1=2$ and $q_2=3$ simultaneously, $(e \bmod 2, e \bmod 3)$ are statistically coupled ($D_{\mathrm{TV}} > 0$) and $\hat{P}_6(1) \neq \hat{P}_2(y_1)\hat{P}_3(y_2)$.

# Subsystem 152: Expander Graph Ramanujan Spectral Gap & Tanner Arithmetic Audit

## 1. Mathematical Formulation
For a $d$-regular Ramanujan graph with $|\lambda_2| \le 2\sqrt{d-1}$, Tanner's eigenvalue bound gives vertex expansion:
$$\frac{|N(S)|}{|S|} \ge \frac{d^2}{\lambda_2^2 + (d^2 - \lambda_2^2)\alpha}.$$
At $d=10$, $\lambda_2 = 2\sqrt{9} = 6$ and the unnormalized spectral gap is $d - \lambda_2 = 4.0$. Because $d^2/\lambda_2^2 = d^2/(4(d-1)) < d/2$ for all $d \ge 3$, this naive one-sided Tanner bound is strictly below the $> d/2$ majority-peeling threshold on every evaluated row (`guarantees_linear_time_peeling = False`); no peeling decoding guarantee is claimed.

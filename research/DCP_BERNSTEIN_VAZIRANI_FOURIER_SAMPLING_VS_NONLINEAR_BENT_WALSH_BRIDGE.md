# Subsystem 156: Bernstein-Vazirani 1-Query Fourier Sampling vs. Nonlinear Carry Dilution Bridge

## 1. Mathematical Formulation
For $f(x) = (s \cdot x) \oplus c(x)$ on $\mathbb{F}_2^n$, the single-query Bernstein-Vazirani success probability at target $s$ is:
$$P_{\text{BV}}(s) = |\hat{F}(s)|^2 = \left(1 - \frac{2\,\mathrm{wt}(c)}{2^n}\right)^2,$$
evaluating to $1.0$ after CNOT carry peeling ($\mathrm{wt}(c)=0$), $1/4$ for a single quadratic carry $c(x)=x_0 x_1$, $2^{-n}$ for a bent carry cascade, and $0$ for a balanced defect.

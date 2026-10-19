# Subsystem 144: Floquet Dynamical Decoupling (CPMG vs. Uhrig UDD) Filter Function Bridge

## 1. Mathematical Formulation
For an $N$-pulse sequence with normalized pulse instants $t_j/\tau \in (0, 1)$, the phase-noise filter function is:
$$F_N(\omega\tau) = \left|1 + (-1)^{N+1}e^{i\omega\tau} + 2\sum_{j=1}^N (-1)^j e^{i\omega t_j}\right|^2.$$
Uhrig Dynamical Decoupling chooses $t_j = \tau \sin^2\!\left(\frac{\pi j}{2N+2}\right)$, cancelling the first $N$ Taylor derivatives at $\omega=0$ so that $F_{\text{UDD}_N}(\omega\tau) = \mathcal{O}((\omega\tau)^{2N+2})$.

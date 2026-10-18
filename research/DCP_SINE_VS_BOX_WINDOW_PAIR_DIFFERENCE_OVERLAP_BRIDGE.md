# DCP Discrete Sine vs. Flat Box Window Shift-Autocorrelation and Quadratic Dephasing Bridge

## 1. Exact Closed-Form Shift Autocorrelation and Unit-Shift Identity
For the discrete sine window $\psi_{\mathrm{sin}}(z) = \sqrt{\frac{2}{P}}\sin\!\left(\frac{\pi(z + 1/2)}{P}\right)$ on $z \in \{0, \dots, P-1\}$ ($0 \le \Delta \le P$):
$$\gamma_{\mathrm{sin}}(\Delta; P) = \left(1 - \frac{\Delta}{P}\right)\cos\!\left(\frac{\pi \Delta}{P}\right) + \frac{1}{P}\frac{\sin(\pi \Delta / P)}{\sin(\pi / P)}, \quad \gamma_{\mathrm{sin}}(1; P) = \left(1 - \frac{1}{P}\right)\cos\!\left(\frac{\pi}{P}\right) + \frac{1}{P}.$$
The linear $\Delta / P$ dephasing loss cancels identically, reducing unit-shift dephasing loss from $1/P$ (box window) to $2(1 - 1/P)\sin^2(\pi/2P) \sim \frac{\pi^2}{2P^2}$, while near the boundary ($\Delta = P - 1$) the box window retains larger overlap $1/P > \frac{2}{P}\sin^2(\pi/2P)$.

# DCP Sine-Window Three-Dirichlet-Kernel Decomposition and Cutoff Bridge

## 1. Exact Three-Dirichlet-Kernel Identity
For $w_{\sin}(z) = \frac{2}{P}\sin^2\!\left(\frac{\pi(z + 1/2)}{P}\right)$ on $z \in \{0, \dots, P - 1\}$ and centered Dirichlet kernel $D_P(\phi) = \frac{1}{P}\sum_{z=0}^{P-1} e^{i\phi(z - (P-1)/2)}$:
$$\tilde{\gamma}_{\sin}(\phi; P) = D_P(\phi) + \frac{1}{2} D_P\!\left(\phi + \frac{2\pi}{P}\right) + \frac{1}{2} D_P\!\left(\phi - \frac{2\pi}{P}\right).$$
- **First-Harmonic Constructive Survival Control**: At $\phi = 2\pi / P$, the box kernel vanishes ($D_P(2\pi/P) = 0$) while the sine window retains $\tilde{\gamma}_{\sin}(2\pi/P; P) = 1/2$ for all $P \ge 3$.
- **Principal-Period Sidelobe Bound**: Reduce to $\delta=\mathrm{dist}(\phi,2\pi\mathbb Z)\in[0,\pi]$. For $P\ge4$ and $4\pi/P\le\delta\le\pi$,
  $$|\tilde\gamma_{\sin}(\phi;P)|\le \frac{2\sin^2(\pi/P)}{P\sin^3(\delta/2)}\le\frac{2\pi^5}{(P\delta)^3}.$$

## 2. Unrestricted Decay Claim Retracted

Magnitudes are periodic. Large absolute frequency is NOT evidence of
suppression: it may alias to the main lobe. At $P=8$, $\phi=2\pi\cdot7.5/8$,
the sine magnitude is about0.848596, exceeding the box magnitude0.640729.
V2 retains this counterexample and checks the corrected principal bound.
It does not claim strict suppression at all harmonic zeros (both kernels
can vanish there), nor an unrestricted bound in $|\phi|$.

For the local derivation write $x=\delta/2$, $d=\pi/P$. Away from removable
zeros the three-kernel identity gives magnitude ratio
$(1-\cos d)(1+\cos d-\sin^2x)/(\sin^2x-\sin^2d)$.
In the specified range $\sin^2x\ge\sin^2(2d)\ge2\sin^2d$.
The numerator is at most $\sin^2d$, and $|D_P|\le1/(P\sin x)$,
giving the first bound; $\sin x\ge\delta/\pi$ gives the second.
Removable zeros follow by continuity. Numerical controls are float
calibrations, not interval or formal proof certificates. Local review is
pending. This repairs a diagnostic, not a DCP algorithm or general no-go.

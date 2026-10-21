# Subsystem 141: Quantum Ziv-Zakai Bayesian Phase Estimation Lower Bound Bridge

## 1. Mathematical Formulation
For $K$ copies of a dephased DCP phase witness $\rho(\theta) = \frac{1-v}{2}I + v|\psi(\theta)\rangle\langle\psi(\theta)|$ with $|\psi(\theta)\rangle = \frac{|0\rangle + e^{i\theta}|1\rangle}{\sqrt{2}}$, the single-copy Uhlmann fidelity at lag $h$ is:
$$F(\rho(0), \rho(h)) = 1 - v^2 \sin^2(h/2).$$
The Quantum Ziv-Zakai Bound (QZZB) on $[-\pi/2, \pi/2]$ (width $W=\pi$) bounds the mean-squared error of any estimator via the two-point Helstrom error $P_e(h; K, v) \ge \frac{1}{2}\left(1 - \sqrt{1 - F(\rho(0),\rho(h))^K}\right)$:
$$\mathrm{MSE}_{\mathrm{QZZB}}(K, v) = \frac{1}{2}\int_0^\pi h\left(1 - \frac{h}{\pi}\right) 2P_e(h; K, v)\,dh.$$

## 2. Key Certified Results
- **Prior Ceiling Saturation ($v \to 0$)**: When $v=0$, $P_e(h) = 1/2$ and $\mathrm{MSE}_{\mathrm{QZZB}} = \pi^2/12 \approx 0.822467$, matching the uniform prior variance.
- **Low-Copy Validity**: At $K=1, v=0.85$, the local Quantum Cramér-Rao Bound $1/(Kv^2) \approx 1.3841$ exceeds the entire prior variance $\pi^2/12$, whereas $\mathrm{MSE}_{\mathrm{QZZB}}(1, 0.85) \approx 0.3694$ remains strictly physical.

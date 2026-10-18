# DCP Single-Shot Quantum Rejection Sampling Box-to-Sine Window Bridge (Subsystem 98)

## Scope & Overview
This subsystem establishes the exact maximum acceptance probability $P_{\mathrm{accept}}^*(\mathrm{box} \to f)$ for reshaping a uniform box-window superposition on $\{0, \dots, P-1\}$ into the Dirichlet-optimal sine window vs. a peaked Lorentzian window via a single diagonal ancilla measurement.

## Exact Mathematical Laws
1. **Exact Sup-Norm Acceptance Law**:
   The maximum physical acceptance probability of a trace-non-increasing diagonal reshaping operator $M_{\mathrm{acc}}$ is $P_{\mathrm{accept}}^*(\mathrm{box} \to f) = \frac{\|\psi_f\|_2^2}{P \|\psi_f\|_\infty^2}$.
2. **Universal $> 50\%$ Acceptance for the Optimal Sine Window**:
   For $\psi_{\mathrm{sin}}^*(x) = \sqrt{\frac{2}{P+1}}\sin(\frac{\pi(x+1)}{P+1})$, $P_{\mathrm{accept}}^*(\mathrm{box} \to \mathrm{sin}^*) \ge \frac{P+1}{2P} > \frac{1}{2}$ for every finite window size $P \ge 1$, strictly dominating peaked Lorentzian windows in both acceptance rate and unit-shift coherence $\gamma(1)$.

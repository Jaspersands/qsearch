# DCP Multi-Wire Correlated $Z$-Fault Syndrome-Parity Walsh-Hadamard Twirl Bridge

## 1. Exact Global-Parity Walsh-Hadamard Visibility Law
Under an arbitrary $h$-wire $Z$-error distribution $p(e)$ on $\{0, 1\}^h$, every syndrome branch $d \in \{0, 1\}^{h-1}$ of the $h$-wire CNOT star couples $x^{(0)} = (0, d)$ and $x^{(1)} = (1, \bar{d})$ with $x^{(0)} \oplus x^{(1)} = 1^h$, so the exact conditional visibility on the target wire is the global-parity Walsh-Hadamard coefficient $\gamma_{\mathrm{cond}}(p) = \mathbb{E}_{e \sim p}[(-1)^{e_0 \oplus \dots \oplus e_{h-1}}] = \widehat{p}(1^h)$.

## 2. Even-Weight Fault Immunity vs. Single-Fault Collapse
- **Even-Weight Immunity**: Any $Z$-fault distribution supported on even Hamming weights $\mathrm{wt}(e) \equiv 0 \pmod 2$ achieves $\gamma_{\mathrm{cond}}(p) = 1.0$ even when every single-wire marginal visibility vanishes ($\gamma_{\mathrm{marg}, j} = 0$).
- **Single-Fault Collapse**: A $50/50$ mixture of $e = 0^h$ and uniform weight-$1$ faults has $\gamma_{\mathrm{cond}}(p) = 0.0$ despite high single-wire marginals $\gamma_{\mathrm{marg}, j} = 1 - 1/h$.

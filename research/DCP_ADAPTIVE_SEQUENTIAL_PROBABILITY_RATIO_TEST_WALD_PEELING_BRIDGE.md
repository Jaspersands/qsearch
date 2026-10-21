# DCP Adaptive Sequential Probability Ratio Test (Wald SPRT) Peeling Bridge (Subsystem 123)

## Scope & Overview
This subsystem establishes the exact Gambler's Ruin / Wald stopping-time and bit-error laws when each stage of dyadic bit peeling uses an adaptive Sequential Probability Ratio Test (stopping as soon as the running Pauli-$X$ sum reaches $\pm M$) instead of a fixed-size batch $N_{\mathrm{fixed}}$.

## Exact Mathematical Laws
1. **Exact Gambler's Ruin Error & Expected Quantum Copies**:
   With step bias $\gamma = p - q \in (0, 1)$, stopping at $\pm M$ achieves exact error rate $\delta_{\mathrm{SPRT}}(M, \gamma) = \frac{1}{1 + ((1+\gamma)/(1-\gamma))^M}$ and expected copies:
   $$\mathbb{E}[T_{\mathrm{SPRT}}(M, \gamma)] = \frac{M}{\gamma}\tanh\!\left(M \operatorname{atanh}(\gamma)\right).$$
2. **$> 2.2\times$ Expected Copy Savings Over Fixed-Batch Majority Voting**:
   At $M = 3, \gamma = 0.75$, $\mathbb{E}[T_{\mathrm{SPRT}}] = 3.9918$ copies vs. $N_{\mathrm{fixed}}^* = 9$ copies required by a fixed odd batch for the same error threshold (a $2.255\times$ reduction).

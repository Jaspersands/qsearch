# DCP Hidden-Shift Bent-Function Rötteler Involutory Dual Bridge (Subsystem 136)

## Scope & Overview
This subsystem establishes that when $2k$ overlapping CNOT survivor wires carry both a quadratic bent carry phase $(-1)^{f(u \oplus s)}$ and a hidden shift $s \in \{0, 1\}^{2k}$, Rötteler's 2-query quantum hidden-shift algorithm uncomputes the dual bent carry phase and recovers $s$ with $100\%$ single-shot probability ($P(s) = 1.0$).

## Exact Mathematical Laws
1. **1-Query Uniform Dephasing vs. 2-Query Deterministic Recovery**:
   Single-query Bernstein-Vazirani Hadamard sampling yields the flat distribution $P(w) = 2^{-2k}$, whereas applying $H^{\otimes 2k} U_{\tilde{f}} H^{\otimes 2k} U_{f_s} H^{\otimes 2k}\lvert 0^{2k}\rangle$ cancels $(-1)^{2\tilde{f}(w)} = +1$ and outputs $\lvert s\rangle$ with probability $1.00$ across all $2^{2k}$ shifts.

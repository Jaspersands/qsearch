# DCP Bravyi-Kitaev 15-to-1 Reed-Muller Magic State Distillation Cost Bridge (Subsystem 128)

## Scope & Overview
This subsystem quantifies the fault-tolerant raw magic-state factory savings achieved by replacing an $m$-qubit coherent inverse $\mathrm{QFT}_{2^m}^\dagger$ with adaptive $R_Z(-\phi_{\mathrm{known}})$ dyadic bit peeling under concatenated Bravyi-Kitaev $\llbracket 15, 1, 3 \rrbracket$ 15-to-1 magic state distillation.

## Exact Mathematical Laws
1. **Cubic Error Compression & Distillation Level Step-Down**:
   Each 15-to-1 level compresses error as $p_{\mathrm{out}} = \frac{35 p_{\mathrm{in}}^3}{(1-p_{\mathrm{in}})^{15} + 35 p_{\mathrm{in}}^3}$ at a $15\times$ raw state multiplier.
2. **$> 451\times$ Raw Magic-State Reduction at the $L=1 \to L=2$ Threshold**:
   At $m = 32, p_{\mathrm{raw}} = 10^{-3}, \epsilon_{\mathrm{target}} = 10^{-4}$, adaptive peeling requires $L = 1$ level ($18{,}000$ raw $T$-states) while $\mathrm{QFT}_{2^{32}}^\dagger$ requires $L = 2$ levels ($8{,}120{,}925$ raw $T$-states, a $451.16\times$ reduction).

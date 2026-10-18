# Clean DCP Dyadic Prefix-Peeling Reduction: Exact Truncation Uniformity, Incorrect-Prefix Character Depolarization, and Binomial Majority-Verifier Bounds

## 1. Motivation and Scope

In `theorems/dcp_native_parity_bridge.py` (`research/DCP_NATIVE_PARITY_BRIDGE.md`), Section 3 reduces scalar cyclic-DCP recovery of $s \in \mathbb{Z}_{2^t}$ to single-bit parity prediction across $T_{\text{stages}} = t - t_{\text{term}}$ adaptive prefix-peeling stages, followed by exhaustive $X$-basis verification of the $2^{t_{\text{term}}}$ terminal suffix candidates.

At stage $k \in \{1, \dots, T_{\text{stages}} - 1\}$, given a recovered $k$-bit prefix $\hat{p}_k \in \{0, \dots, 2^k - 1\}$, the adapter (`prefix_rescale_plan`) takes a fresh original sample $(a, |\psi_a(s)\rangle)$ ($a \sim \mathrm{Unif}(\mathbb{Z}_{2^t})$), applies the known single-wire phase gate $R_Z(-2\pi a \hat{p}_k / 2^t)$, and passes only the **truncated label** $\tilde{a} := a \bmod 2^{t-k} \in \mathbb{Z}_{2^{t-k}}$ to the stage-$k$ lift and predictor (discarding the high $k$ bits $h_a := \lfloor a / 2^{t-k} \rfloor \in \mathbb{Z}_{2^k}$).

This note proves three exact theorems governing this dyadic prefix-peeling reduction:
1. **Correct-Prefix Phase Reduction and Exact Fiber Uniformity**: When $\hat{p}_k = s \bmod 2^k$, the discarded high bits $h_a$ contribute an integer multiple of $2\pi$ to the phase, leaving an exact uniform clean sample $(\tilde{a}, |\psi_{\tilde{a}}(\lfloor s / 2^k\rfloor)\rangle)$ at modulus $2^{t-k}$.
2. **Incorrect-Prefix Character Depolarization Theorem**: Whenever $\hat{p}_k \not\equiv s \pmod{2^k}$, averaging over the unobserved high label bits $h_a \sim \mathrm{Unif}(\mathbb{Z}_{2^k})$ annihilates the off-diagonal coherence identically ($\bar{\rho}_{\tilde{a}}(s, \hat{p}_k) = \frac{1}{2}I_2$ for every $\tilde{a} \in \mathbb{Z}_{2^{t-k}}$), proving that any prefix error at stage $< k$ completely depolarizes the stage-$k$ input channel.
3. **Exact Binomial Majority-Vote Tail and Non-Primitive Verifier Orthogonality**: Tight finite-sample comparison of the exact binomial majority error against the Chernoff/Hoeffding bound $\exp(-2 R \epsilon^2)$, paired with exact character orthogonality of the terminal $X$-basis verifier across all non-zero errors $\delta = (s - c) \bmod 2^t$ of arbitrary 2-adic valuation $v_2(\delta) \in \{0, \dots, t-1\}$.

## 2. Theorem 1 — Correct-Prefix Phase Reduction and Exact Fiber Uniformity

Decompose each original label $a \in \mathbb{Z}_{2^t}$ uniquely as
$$
a \;=\; \tilde{a} \;+\; 2^{t-k}\,h_a, \qquad \tilde{a} := a \bmod 2^{t-k} \in \mathbb{Z}_{2^{t-k}}, \quad h_a := \left\lfloor \frac{a}{2^{t-k}} \right\rfloor \in \mathbb{Z}_{2^k}.
$$

**Theorem 1 (Correct-Prefix Independence of High Label Bits).**
If $\hat{p}_k = s \bmod 2^k$, write $s = \hat{p}_k + 2^k s^{(k)}$ with $s^{(k)} = \lfloor s / 2^k \rfloor \in \mathbb{Z}_{2^{t-k}}$. Then for every $a = \tilde{a} + 2^{t-k} h_a \in \mathbb{Z}_{2^t}$:
$$
\omega_{2^t}^{a(s - \hat{p}_k)} \;=\; \omega_{2^t}^{(\tilde{a} + 2^{t-k} h_a)\,2^k s^{(k)}}
\;=\; \omega_{2^{t-k}}^{\tilde{a}\,s^{(k)}} \cdot \underbrace{\omega_{2^t}^{2^t h_a s^{(k)}}}_{=\,1}
\;=\; \omega_{2^{t-k}}^{\tilde{a}\,s^{(k)}}.
$$
Consequently, when $a \sim \mathrm{Unif}(\mathbb{Z}_{2^t})$, $\tilde{a}$ is uniformly distributed on $\mathbb{Z}_{2^{t-k}}$ (each fiber having exact size $2^k$), and conditioned on $\tilde{a}$, the adapted qubit is in the pure state $|\psi_{\tilde{a}}(s^{(k)})\rangle = \frac{1}{\sqrt{2}}(|0\rangle + \omega_{2^{t-k}}^{\tilde{a} s^{(k)}}|1\rangle)$ with visibility $1$.

## 3. Theorem 2 — Incorrect-Prefix Character Depolarization Theorem

Suppose an earlier stage made an error so $\hat{p}_k \not\equiv s \pmod{2^k}$, and let $\delta := (s - \hat{p}_k) \bmod 2^t$. Then $\delta \not\equiv 0 \pmod{2^k}$, so its 2-adic valuation satisfies $r := v_2(\delta) \in \{0, 1, \dots, k-1\}$.

**Theorem 2 (Exact Conditional Depolarization Under Incorrect Prefix).**
Because the stage-$k$ predictor receives only $\tilde{a} = a \bmod 2^{t-k}$ while $h_a = \lfloor a / 2^{t-k} \rfloor \sim \mathrm{Unif}(\mathbb{Z}_{2^k})$ is unobserved, the conditional density matrix of each adapted phase qubit given $\tilde{a} \in \mathbb{Z}_{2^{t-k}}$ is
$$
\bar{\rho}_{\tilde{a}}(s, \hat{p}_k)
\;:=\; \frac{1}{2^k}\sum_{h_a = 0}^{2^k - 1} |\psi_{\tilde{a} + 2^{t-k} h_a}(s - \hat{p}_k)\rangle\langle\psi_{\tilde{a} + 2^{t-k} h_a}(s - \hat{p}_k)|.
$$
Its off-diagonal entry is
$$
\bar{\rho}_{\tilde{a}}(s, \hat{p}_k)[0, 1]
\;=\; \frac{1}{2}\omega_{2^t}^{-\tilde{a}\,\delta}\left(\frac{1}{2^k}\sum_{h_a = 0}^{2^k - 1} \omega_{2^k}^{-h_a(\delta \bmod 2^k)}\right)
\;=\; \begin{cases}
\frac{1}{2}\omega_{2^{t-k}}^{-\tilde{a}(\delta / 2^k)} & \text{if } \delta \equiv 0 \pmod{2^k}\;(\hat{p}_k \equiv s \pmod{2^k}), \\[4pt]
0 & \text{if } \delta \not\equiv 0 \pmod{2^k}\;(\hat{p}_k \not\equiv s \pmod{2^k}).
\end{cases}
$$
Thus, for all $2^k - 1$ incorrect prefixes $\hat{p}_k \not\equiv s \pmod{2^k}$, $\bar{\rho}_{\tilde{a}}(s, \hat{p}_k) = \frac{1}{2}I_2$ for **every** $\tilde{a} \in \mathbb{Z}_{2^{t-k}}$, so any stage-$k$ predictor has exact zero advantage ($\mathrm{Adv}_k = 0$) once a single earlier prefix bit is wrong.

## 4. Theorem 3 — Exact Binomial Majority-Vote Tail and Terminal Verifier Orthogonality

**Theorem 3 (Majority Amplification & Terminal Candidate Verification).**
1. **Binomial Majority Error Bound**: For odd $R = 2 m + 1$ independent invocations with per-invocation success $p = \frac{1}{2} + \epsilon$ ($\epsilon \in (0, 1/2]$), the exact majority-vote failure probability satisfies
   $$
   P_{\text{maj-err}}(R, \epsilon) \;=\; \sum_{j=0}^{m} \binom{R}{j}\left(\frac{1}{2} + \epsilon\right)^j\left(\frac{1}{2} - \epsilon\right)^{R - j}
   \;\le\; \left(1 - 4\epsilon^2\right)^{R/2} \;\le\; \exp\bigl(-2 R \epsilon^2\bigr).
   $$
2. **Terminal $X$-Verifier Exact $1/2$ False Survival Across All 2-Adic Valuations**: For any complete candidate $c \in \mathbb{Z}_{2^t}$ and secret $s \in \mathbb{Z}_{2^t}$, rotating a clean sample $(a, |\psi_a(s)\rangle)$ by $-2\pi a c / 2^t$ and measuring in the $X$ basis yields outcome $|+\rangle$ with single-sample source-averaged probability
   $$
   P_{+}(s, c) \;=\; \frac{1}{2^t}\sum_{a=0}^{2^t - 1} \frac{1 + \cos(2\pi a(s - c)/2^t)}{2}
   \;=\; \begin{cases}
   1 & \text{if } c \equiv s \pmod{2^t}, \\
   \frac{1}{2} & \text{if } c \not\equiv s \pmod{2^t},
   \end{cases}
   $$
   regardless of the 2-adic valuation $v_2(s - c) \in \{0, \dots, t-1\}$. Across $L_{\text{ver}}$ independent tests, every false candidate survives all-$|+\rangle$ verification with probability exactly $2^{-L_{\text{ver}}}$.

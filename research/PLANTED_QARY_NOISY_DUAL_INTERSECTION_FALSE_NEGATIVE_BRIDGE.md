# Planted $q$-ary Noisy Dual-Intersection False-Negative Bridge: Weight-Stratified True-Codeword Survival, Universal Spurious Noise-Invariance, and Primal Minimum-Distance Scaling

## 1. Motivation and Scope

In `theorems/planted_qary_dual_intersection_cascade_bridge.py` (Subsystem 30), $m$ noiseless $\mathrm{QFT}_q^{\otimes n}$ dual samples $u^{(1)}, \dots, u^{(m)} \sim \operatorname{Unif}(B^\perp)$ were shown to retain every planted codeword $b \in B$ with probability $1$ while suppressing every non-planted vector $x \in \mathbb{F}_q^n \setminus B$ as $q^{-m}$.

When the planted subspace state undergoes i.i.d. coordinate dephasing/depolarizing noise of rate $\gamma \in [0, 1]$ prior to $\mathrm{QFT}_q^{\otimes n}$ readout, each measured dual sample takes the form $u = (v + \xi) \bmod q$ with $v \sim \operatorname{Unif}(B^\perp)$ and $\xi \sim \mathcal{D}_\gamma^{\otimes n}$. If an algorithm applies the standard intersection cascade $\widehat{B}_{m, \gamma} := \{x \in \mathbb{F}_q^n : \forall j \in \{1, \dots, m\},\; \langle x, u^{(j)}\rangle = 0\}$, how do true planted codewords $b \in B \setminus \{0\}$ and spurious non-planted vectors $x \in \mathbb{F}_q^n \setminus B$ behave? This note proves three exact theorems resolving the noisy dual-intersection cascade.

## 2. Theorem 1 — Exact Weight-Stratified True-Codeword Survival Law on $B$

For any planted codeword $b \in B$, $\langle b, v\rangle = 0$ for every $v \in B^\perp$, so $\langle b, v + \xi\rangle = \langle b, \xi\rangle \bmod q$.

**Theorem 1 (Exact Weight-Power Survival Law and False-Negative Rate on $B$).**
Under $m \ge 1$ i.i.d. noisy $\mathrm{QFT}_q^{\otimes n}$ samples $u^{(1)}, \dots, u^{(m)}$ at noise rate $\gamma \in [0, 1]$:
1. For any planted codeword $b \in B$ of Hamming weight $\mathrm{wt}_H(b) \in \{0, 1, \dots, n\}$, the single-sample zero-syndrome survival probability is
   $$
   \Pr_{u \sim P_{\text{QFT}}(\cdot \mid B, \gamma)}\!\bigl[\langle b, u\rangle = 0\bigr] \;=\; \frac{1}{q} \;+\; \frac{q - 1}{q}(1 - \gamma)^{\mathrm{wt}_H(b)},
   $$
   and the $m$-sample cascade survival probability is
   $$
   S_{\text{planted}}\bigl(\mathrm{wt}_H(b);\, q, \gamma, m\bigr) \;:=\; \Pr\!\bigl[b \in \widehat{B}_{m, \gamma}\bigr] \;=\; \left(\frac{1}{q} \;+\; \frac{q - 1}{q}(1 - \gamma)^{\mathrm{wt}_H(b)}\right)^m.
   $$
2. For every $\gamma \in (0, 1]$ and every non-zero codeword $b \in B \setminus \{0\}$, $S_{\text{planted}}(\mathrm{wt}_H(b); q, \gamma, m) < 1$ decays exponentially to $0$ as $m \to \infty$, inducing a positive false-negative pruning probability $1 - S_{\text{planted}}(\mathrm{wt}_H(b); q, \gamma, m)$ that increases strictly with $\mathrm{wt}_H(b)$.

## 3. Theorem 2 — Universal Noise-Invariance of Non-Planted Spurious Survival on $\mathbb{F}_q^n \setminus B$

**Theorem 2 (Exact Noise-Invariance of Spurious Candidate Survival).**
For every non-planted vector $x \in \mathbb{F}_q^n \setminus B$, every noise rate $\gamma \in [0, 1]$, and every sample count $m \ge 1$, the probability that $x$ survives in $\widehat{B}_{m, \gamma}$ is **identically independent of $\gamma$ and of $\mathrm{wt}_H(x)$**:
$$
\Pr\!\bigl[x \in \widehat{B}_{m, \gamma}\bigr] \;=\; q^{-m} \qquad \forall x \in \mathbb{F}_q^n \setminus B,\;\forall \gamma \in [0, 1],
$$
so the expected number of spurious non-planted survivors is universally
$$
\mathbb{E}\!\left[\bigl|\widehat{B}_{m, \gamma} \setminus B\bigr|\right] \;=\; \bigl(q^n - q^d\bigr)\,q^{-m} \qquad \forall \gamma \in [0, 1].
$$

*Proof.*
For any $x \in \mathbb{F}_q^n \setminus B = \mathbb{F}_q^n \setminus (B^\perp)^\perp$ and any fixed dual noise vector $\xi \in \mathbb{F}_q^n$, the linear functional $v \mapsto \langle x, v\rangle$ on $B^\perp$ is non-zero and hence surjective ($q^{n-d-1}$-to-$1$) onto $\mathbb{F}_q$. Thus $\Pr_{v \sim B^\perp}[\langle x, v\rangle \equiv -\langle x, \xi\rangle \pmod q] = 1/q$ for every $\xi$, and independence across the $m$ samples yields $q^{-m}$. $\square$

## 4. Theorem 3 — Primal Minimum Distance $d_{\min}(B)$ Controls the Survival-to-Spurious Ratio

Let $d_{\min}(B) := \min_{b \in B \setminus \{0\}} \mathrm{wt}_H(b)$ denote the primal minimum Hamming distance of the planted subspace $B$.

**Theorem 3 (Primal Minimum-Distance Survival Frontier).**
For any non-zero planted codeword $b \in B \setminus \{0\}$ and any noise rate $\gamma \in (0, 1)$, the $m$-sample survival-to-spurious ratio
$$
\mathrm{SSR}\bigl(\mathrm{wt}_H(b);\, q, \gamma, m\bigr) \;:=\; \frac{\Pr[b \in \widehat{B}_{m, \gamma}]}{\Pr[x_{\notin B} \in \widehat{B}_{m, \gamma}]}
\;=\; \Bigl(1 \;+\; (q - 1)(1 - \gamma)^{\mathrm{wt}_H(b)}\Bigr)^m
$$
is maximized over $B \setminus \{0\}$ at minimum-weight planted codewords $\mathrm{wt}_H(b) = d_{\min}(B)$, where it equals $\bigl(1 + (q-1)(1-\gamma)^{d_{\min}(B)}\bigr)^m$.

# Native Higher-Call Prime-Power Divisibility Hierarchy Audit: $p$-Adic Subgroup Pinching Filtration, Telescoping Valuation Shells, and Zero-Sum Shell Increments

## 1. Motivation and Scope

In `theorems/native_mp12_prime_power_search_to_decision_audit.py` (Subsystem 4) and `theorems/native_higher_call_prime_power_survival_closed_form.py` (Subsystem 14), prime-power LWE over $q = p^r$ ($p \ge 3$ odd prime, $r \ge 2$) was shown to decompose via the $p$-adic tower $\mathbb{Z}_{p^r} \supset p\mathbb{Z}_{p^r} \supset \dots \supset p^{r-1}\mathbb{Z}_{p^r} \supset \{0\}$. Meanwhile, `theorems/native_higher_call_weighted_fourier_pinching_audit.py` (Subsystem 17) proved that averaging a general $k$-call schedule over the full secret group $\mathbb{Z}_q^n$ pinches the double trajectory sum onto the full collision variety $\tau_\epsilon(w) \equiv \tau_\epsilon(w') \pmod{p^r}$.

When high base-$p$ digits of the secret $s \in \mathbb{Z}_{p^r}^n$ are conditioned or restricted to the $p$-adic subgroup $H_j := p^{r-j}\mathbb{Z}_{p^r}^n \cong \mathbb{Z}_{p^j}^n$ ($0 \le j \le r$), how does the $k$-call unitary path integral pinch across the $p$-adic filtration levels $j = 0, 1, \dots, r$? This note proves three exact theorems establishing the $p$-adic subgroup pinching filtration and its telescoping shell decomposition.

## 2. Theorem 1 — Exact $p$-Adic Subgroup Secret-Pinching Filtration Across Moduli $p^j$

Let $q = p^r$ ($p \ge 3, r \ge 2$), $D = p^M$, and for each $j \in \{0, 1, \dots, r\}$ define the $p$-adic secret subgroup
$$
H_j \;:=\; p^{r-j}\mathbb{Z}_{p^r}^n \;=\; \bigl\{\, p^{r-j} s' \bmod p^r : s' \in \{0, \dots, p^j - 1\}^n \,\bigr\}, \qquad |H_j| \;=\; p^{j n}.
$$
Define the **level-$j$ congruence collision variety**
$$
\mathcal{V}_\epsilon^{(j)}(f) \;:=\; \bigl\{\, (w, w') \in \{0, \dots, D-1\}^k \times \{0, \dots, D-1\}^k : \tau_\epsilon(w) \equiv \tau_\epsilon(w') \pmod{p^j} \,\bigr\}.
$$

**Theorem 1 (Exact Level-$j$ Subgroup Pinching Identity).**
For every $j \in \{0, 1, \dots, r\}$, every $(\epsilon, \sigma) \in \{-1, +1\}^k \times \{-1, +1\}^k$, and every readout outcome $x \in \{0, \dots, D-1\}$, averaging the $k$-call Born probability $P_{\epsilon, \sigma}(x \mid s)$ over $s \sim \operatorname{Unif}(H_j)$ pinches the trajectory pair sum onto $\mathcal{V}_\epsilon^{(j)}(f)$:
$$
\bar{P}_{\epsilon, \sigma}^{(j)}(x) \;:=\; \mathbb{E}_{s \sim \operatorname{Unif}(H_j)}\bigl[P_{\epsilon, \sigma}(x \mid s)\bigr]
\;=\; \frac{1}{D^{k+1}} \sum_{\bar{\tau} \in \mathbb{Z}_{p^j}^n} \left|\sum_{\substack{w \in \{0, \dots, D-1\}^k \\ \tau_\epsilon(w) \bmod p^j = \bar{\tau}}} \exp\!\left(\frac{2\pi i}{p^r} E_\epsilon(w) + \frac{2\pi i}{D}\Phi_\sigma(w; x)\right)\right|^2.
$$

*Proof.*
For $s = p^{r-j} s'$ with $s' \in \mathbb{Z}_{p^j}^n$, the secret-dependent phase factor for a trajectory pair $(w, w')$ is
$$
\exp\!\left(\frac{2\pi i}{p^r}\langle \tau_\epsilon(w) - \tau_\epsilon(w'),\, p^{r-j} s'\rangle\right)
\;=\; \exp\!\left(\frac{2\pi i}{p^j}\langle \tau_\epsilon(w) - \tau_\epsilon(w'),\, s'\rangle\right).
$$
By character orthogonality on $\mathbb{Z}_{p^j}^n$, averaging over $s' \in \mathbb{Z}_{p^j}^n$ equals $1$ if and only if $\tau_\epsilon(w) \equiv \tau_\epsilon(w') \pmod{p^j}$ and $0$ otherwise. Partitioning $\{0, \dots, D-1\}^k$ into residue classes $\bar{\tau} = \tau_\epsilon(w) \bmod p^j \in \mathbb{Z}_{p^j}^n$ yields the sum of squared moduli. $\square$

## 3. Theorem 2 — Monotone $p$-Adic Collision Filtration and Telescoping Valuation Shells

For any trajectory pair $(w, w')$, let $v_p(\tau_\epsilon(w) - \tau_\epsilon(w')) \in \{0, 1, \dots, r\}$ denote the $p$-adic valuation of their signed frequency difference modulo $p^r$ (with $v_p(0) := r$). Define the **exact valuation-difference shell** at level $j \in \{0, \dots, r-1\}$:
$$
\mathcal{D}_\epsilon^{(j)}(f) \;:=\; \mathcal{V}_\epsilon^{(j)}(f) \setminus \mathcal{V}_\epsilon^{(j+1)}(f)
\;=\; \bigl\{\, (w, w') : v_p(\tau_\epsilon(w) - \tau_\epsilon(w')) = j \,\bigr\}.
$$

**Theorem 2 (Monotone Filtration and Exact Telescoping Shell Decomposition).**
1. The varieties $\mathcal{V}_\epsilon^{(j)}(f)$ form a monotone decreasing filtration
   $$
   \{0, \dots, D-1\}^{2k} = \mathcal{V}_\epsilon^{(0)}(f) \;\supseteq\; \mathcal{V}_\epsilon^{(1)}(f) \;\supseteq\; \cdots \;\supseteq\; \mathcal{V}_\epsilon^{(r)}(f) \;\supseteq\; \Delta_k,
   $$
   so $D^{2k} = |\mathcal{V}_\epsilon^{(0)}(f)| \ge |\mathcal{V}_\epsilon^{(1)}(f)| \ge \dots \ge |\mathcal{V}_\epsilon^{(r)}(f)| \ge D^k$.
2. The shells $\mathcal{D}_\epsilon^{(0)}(f), \dots, \mathcal{D}_\epsilon^{(r-1)}(f)$ together with $\mathcal{V}_\epsilon^{(r)}(f)$ form a disjoint partition of $\{0, \dots, D-1\}^{2k}$:
   $$
   D^{2k} \;=\; |\mathcal{V}_\epsilon^{(r)}(f)| \;+\; \sum_{j=0}^{r-1} |\mathcal{D}_\epsilon^{(j)}(f)|.
   $$

## 4. Theorem 3 — Diagonal Cancelation and Zero-Sum Conservation of $p$-Adic Shell Increments

**Theorem 3 (Zero-Sum Oscillatory Shell Increments).**
For each $j \in \{0, \dots, r-1\}$, define the level-$j$ probability shell increment
$$
\Delta \bar{P}_{\epsilon, \sigma}^{(j \to j+1)}(x) \;:=\; \bar{P}_{\epsilon, \sigma}^{(j)}(x) - \bar{P}_{\epsilon, \sigma}^{(j+1)}(x).
$$
1. Because every diagonal pair $(w, w) \in \Delta_k$ satisfies $\tau_\epsilon(w) - \tau_\epsilon(w) = 0 \equiv 0 \pmod{p^r}$ and therefore lies in $\mathcal{V}_\epsilon^{(r)}(f)$, all diagonal terms cancel identically in $\Delta \bar{P}_{\epsilon, \sigma}^{(j \to j+1)}(x)$, which is supported exclusively on the off-diagonal valuation shell $\mathcal{D}_\epsilon^{(j)}(f)$:
   $$
   \Delta \bar{P}_{\epsilon, \sigma}^{(j \to j+1)}(x)
   \;=\; \frac{1}{D^{k+1}} \sum_{(w, w') \in \mathcal{D}_\epsilon^{(j)}(f)} \exp\!\left(\frac{2\pi i}{p^r}\bigl(E_\epsilon(w) - E_\epsilon(w')\bigr) + \frac{2\pi i}{D}\bigl(\Phi_\sigma(w; x) - \Phi_\sigma(w'; x)\bigr)\right).
   $$
2. Summing over all readout outcomes $x \in \{0, \dots, D-1\}$ annihilates every shell increment:
   $$
   \sum_{x=0}^{D-1} \Delta \bar{P}_{\epsilon, \sigma}^{(j \to j+1)}(x) \;=\; 0, \qquad \text{and} \qquad \bar{P}_{\epsilon, \sigma}^{(0)}(x) \;=\; \bar{P}_{\epsilon, \sigma}^{(r)}(x) + \sum_{j=0}^{r-1} \Delta \bar{P}_{\epsilon, \sigma}^{(j \to j+1)}(x).
   $$

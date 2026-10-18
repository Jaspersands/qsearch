# Native Higher-Call Secret-Subspace Restriction Audit: Projected Variety Pinching, Coset Harmonic Folding, and Fourier-Space Law of Total Variance

## 1. Motivation and Scope

When a classical or hybrid preprocessing stage learns $n - r$ linear relations on an LWE secret $s \in \mathbb{F}_q^n$ ($q$ prime), the remaining uncertainty is restricted to an $r$-dimensional subspace $W_S = \operatorname{colspan}(G_S) \subseteq \mathbb{F}_q^n$ ($G_S \in \mathbb{F}_q^{n \times r}$ of rank $r$) or its affine cosets $W_S + a \in \mathbb{F}_q^n / W_S$.

This note proves three exact theorems governing $k$-call interleaved Fourier-response schedules under secret-subspace restriction: projected collision-variety pinching onto $\tau_\epsilon(w) - \tau_\epsilon(w') \in W_S^\perp$, harmonic coset folding of within-subspace variance, and the exact Fourier-space Law of Total Variance partitioning $\mathbb{F}_q^n \setminus \{0\} = (W_S^\perp \setminus \{0\}) \sqcup (\mathbb{F}_q^n \setminus W_S^\perp)$.

## 2. Theorem 1 — Exact Projected Collision-Variety Pinching on $W_S$

Let $W_S = \{G_S z \bmod q : z \in \mathbb{F}_q^r\} \subseteq \mathbb{F}_q^n$ be an $r$-dimensional subspace with orthogonal complement $W_S^\perp = \{\delta \in \mathbb{F}_q^n : G_S^T \delta \equiv 0 \pmod q\}$ of dimension $n - r$. Define the **projected signed frequency collision variety**:
$$
\mathcal{V}_\epsilon(f; W_S) \;:=\; \bigl\{\, (w, w') \in \{0, \dots, D-1\}^{2k} : \tau_\epsilon(w) - \tau_\epsilon(w') \in W_S^\perp \,\bigr\} \;\supseteq\; \mathcal{V}_\epsilon(f).
$$

**Theorem 1 (Exact Subspace-Pinched Born Distribution).**
Averaging the $k$-call Born probability $P_{\epsilon, \sigma}(x \mid s)$ over $s \sim \operatorname{Unif}(W_S)$ pinches the double trajectory sum onto $\mathcal{V}_\epsilon(f; W_S)$:
$$
\mathbb{E}_{s \sim \operatorname{Unif}(W_S)}\bigl[P_{\epsilon, \sigma}(x \mid s)\bigr]
\;=\; \frac{1}{D^{k+1}} \sum_{\bar{\tau} \in \mathbb{F}_q^r} \left|\sum_{\substack{w \in \{0, \dots, D-1\}^k \\ G_S^T \tau_\epsilon(w) \equiv \bar{\tau} \pmod q}} \exp\!\left(\frac{2\pi i}{q}E_\epsilon(w) + \frac{2\pi i}{D}\Phi_\sigma(w; x)\right)\right|^2
\;=\; \sum_{\delta \in W_S^\perp} C_{\epsilon, \sigma}(\delta; x).
$$

## 3. Theorem 2 — Harmonic Coset Folding for Within-Subspace Secret Variance

For each projected difference $\bar{\delta} \in \mathbb{F}_q^r$, define the folded harmonic
$$
C_{\epsilon, \sigma}^{(W_S)}(\bar{\delta}; x) \;:=\; \sum_{\substack{\delta \in \mathbb{F}_q^n \\ G_S^T \delta \equiv \bar{\delta} \pmod q}} C_{\epsilon, \sigma}(\delta; x).
$$

**Theorem 2 (Exact Folded Parseval Identity on $W_S$).**
For every readout outcome $x \in \{0, \dots, D-1\}$, the variance of $P_{\epsilon, \sigma}(x \mid s)$ over $s \sim \operatorname{Unif}(W_S)$ equals the sum of squared moduli of the non-zero folded harmonics:
$$
\operatorname{Var}_{s \sim \operatorname{Unif}(W_S)}\bigl[P_{\epsilon, \sigma}(x \mid s)\bigr] \;=\; \sum_{\bar{\delta} \in \mathbb{F}_q^r \setminus \{0\}} \bigl|C_{\epsilon, \sigma}^{(W_S)}(\bar{\delta}; x)\bigr|^2.
$$

## 4. Theorem 3 — Exact Fourier-Space Law of Total Variance Across $\mathbb{F}_q^n / W_S$

Partition $\mathbb{F}_q^n$ into the $q^{n-r}$ affine cosets $W_S + a$ ($a \in \mathbb{F}_q^n / W_S$).

**Theorem 3 (Disjoint Harmonic Partition of Between-Coset and Within-Coset Variance).**
For every readout outcome $x \in \{0, \dots, D-1\}$:
1. **Between-Coset Variance ($W_S^\perp \setminus \{0\}$)**: For each coset $W_S + a$, $\mathbb{E}_{s \sim W_S + a}[P_{\epsilon, \sigma}(x \mid s)] = \sum_{\delta \in W_S^\perp} C_{\epsilon, \sigma}(\delta; x)\,\omega_q^{\langle \delta, a\rangle}$, so the variance of the coset means across $a \sim \operatorname{Unif}(\mathbb{F}_q^n / W_S)$ is supported exclusively on $W_S^\perp \setminus \{0\}$:
   $$
   \operatorname{Var}_{a \sim \mathbb{F}_q^n / W_S}\!\Bigl[\mathbb{E}_{s \sim W_S + a}\bigl[P_{\epsilon, \sigma}(x \mid s)\bigr]\Bigr]
   \;=\; \sum_{\delta \in W_S^\perp \setminus \{0\}} \bigl|C_{\epsilon, \sigma}(\delta; x)\bigr|^2.
   $$
2. **Expected Within-Coset Variance ($\mathbb{F}_q^n \setminus W_S^\perp$)**: Averaging the within-coset variance $\operatorname{Var}_{s \sim W_S + a}[P_{\epsilon, \sigma}(x \mid s)]$ over $a \sim \operatorname{Unif}(\mathbb{F}_q^n / W_S)$ annihilates cross-terms between distinct $\delta \equiv \delta' \pmod{W_S^\perp}$ inside each folded harmonic, leaving the exact sum over $\mathbb{F}_q^n \setminus W_S^\perp$:
   $$
   \mathbb{E}_{a \sim \mathbb{F}_q^n / W_S}\!\Bigl[\operatorname{Var}_{s \sim W_S + a}\bigl[P_{\epsilon, \sigma}(x \mid s)\bigr]\Bigr]
   \;=\; \sum_{\delta \in \mathbb{F}_q^n \setminus W_S^\perp} \bigl|C_{\epsilon, \sigma}(\delta; x)\bigr|^2,
   $$
   recovering $\operatorname{Var}_{s \sim \mathbb{F}_q^n}[P_{\epsilon, \sigma}(x \mid s)] = \sum_{\delta \in W_S^\perp \setminus \{0\}}|C(\delta; x)|^2 + \sum_{\delta \notin W_S^\perp}|C(\delta; x)|^2$.

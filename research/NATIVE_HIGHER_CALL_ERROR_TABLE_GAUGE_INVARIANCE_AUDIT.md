# Native Higher-Call Error-Table Gauge-Invariance Audit: Affine-Secret Gauge Covariance, Injective-Frequency Purity Pinning, and Universal Word-Multiplicity Pinching

## 1. Motivation and Scope

In a general $k$-call interleaved Fourier-response schedule $|\Psi_{\epsilon, \sigma}(y(s))\rangle = F_D^{\sigma_k} D_{y(s)}^{\epsilon_k} \cdots F_D^{\sigma_1} D_{y(s)}^{\epsilon_1} |+_D\rangle$, the public oracle phases $y_w(s) \equiv \langle f(w), s\rangle + e(w) \pmod q$ depend on both the public frequency table $f : \{0, \dots, D-1\} \to \mathbb{Z}_q^n$ and the public error phase table $e \in \mathbb{Z}_q^D$.

This note proves three exact theorems characterizing how $k$-call quantum observables transform under affine secret-gauge shifts of the error table $e$, when the secret-averaged state is completely independent of $e$, and how averaging over $e \sim \operatorname{Unif}(\mathbb{Z}_q^D)$ pinches $\mathcal{V}_\epsilon(f)$ onto the frequency-independent **signed word-multiplicity variety** $\mathcal{W}_\epsilon$.

## 2. Theorem 1 — Exact Affine-Secret Gauge Covariance and Invariance of Ensemble Moment Metrics

For any error table $e \in \mathbb{Z}_q^D$, secret gauge shift $\Delta s \in \mathbb{Z}_q^n$, and global phase offset $c_0 \in \mathbb{Z}_q$, define the gauge-transformed error table
$$
\tilde{e}(w) \;:=\; \bigl(e(w) + \langle f(w), \Delta s\rangle + c_0\bigr) \bmod q, \qquad w \in \{0, \dots, D-1\}.
$$

**Theorem 1 (Exact Affine-Secret Gauge Covariance and Moment Invariance).**
For every $k \ge 1$, every schedule $(\epsilon, \sigma) \in \{-1, +1\}^k \times \{-1, +1\}^k$, and every $(\Delta s, c_0) \in \mathbb{Z}_q^n \times \mathbb{Z}_q$:
1. **Statevector Global Phase and Density-Matrix Shift Covariance**: For each secret $s \in \mathbb{Z}_q^n$, $y_{\tilde{e}}(s)_w \equiv y_e(s + \Delta s)_w + c_0 \pmod q$, so
   $$
   |\Psi_{\epsilon, \sigma}(y_{\tilde{e}}(s))\rangle \;=\; \omega_q^{c_0 \sum_{\ell=1}^k \epsilon_\ell}\,|\Psi_{\epsilon, \sigma}(y_e(s + \Delta s))\rangle,
   \qquad
   \rho_{\epsilon, \sigma}^{(\tilde{e})}(s) \;=\; \rho_{\epsilon, \sigma}^{(e)}\bigl((s + \Delta s) \bmod q\bigr).
   $$
2. **Harmonic Phase Twist and Exact Moment Invariance**: Every matrix secret-Fourier harmonic transforms by the character phase $\widehat{\rho}_{\epsilon, \sigma}^{(\tilde{e})}(\delta) = \omega_q^{-\langle \delta, \Delta s\rangle}\,\widehat{\rho}_{\epsilon, \sigma}^{(e)}(\delta)$. Consequently, $\bar{\rho}_{\epsilon, \sigma}^{(\tilde{e})} = \bar{\rho}_{\epsilon, \sigma}^{(e)}$, $\mathbb{E}_s[P_{\epsilon, \sigma}^{(\tilde{e})}(x \mid s)] = \mathbb{E}_s[P_{\epsilon, \sigma}^{(e)}(x \mid s)]$, $\mathcal{E}_{\epsilon, \sigma}(\tilde{e}) = \mathcal{E}_{\epsilon, \sigma}(e)$, and $\mathcal{V}_{\text{HS}}(\epsilon, \sigma; \tilde{e}) = \mathcal{V}_{\text{HS}}(\epsilon, \sigma; e)$ are **identically invariant**.

## 3. Theorem 2 — Exact Error-Table Independence Under Injective Signed Frequency Maps

**Theorem 2 (Universal Error-Table Independence When $|\mathcal{V}_\epsilon(f)| = D^k$).**
Suppose the signed frequency map $\tau_\epsilon : \{0, \dots, D-1\}^k \to \mathbb{Z}_q^n$ is injective, so $\mathcal{V}_\epsilon(f) = \Delta_k = \{(w, w) : w \in \{0, \dots, D-1\}^k\}$ ($|\mathcal{V}_\epsilon(f)| = D^k$). Then for **every** error table $e \in \mathbb{Z}_q^D$:
1. On $\Delta_k$, $E_\epsilon(w) - E_\epsilon(w) = 0$ identically, so the secret-averaged density operator is maximally mixed:
   $$
   \bar{\rho}_{\epsilon, \sigma}^{(e)} \;=\; \frac{1}{D}I_D \qquad \forall e \in \mathbb{Z}_q^D,
   $$
   and $\mathbb{E}_{s \sim \mathbb{Z}_q^n}[P_{\epsilon, \sigma}^{(e)}(x \mid s)] = 1/D$ for all $x \in \{0, \dots, D-1\}$.
2. The operator Hilbert–Schmidt variance is pinned at its universal maximum for every $e \in \mathbb{Z}_q^D$:
   $$
   \mathcal{V}_{\text{HS}}(\epsilon, \sigma; e) \;=\; 1 - \operatorname{Tr}\!\left((\bar{\rho}_{\epsilon, \sigma}^{(e)})^2\right) \;=\; 1 - \frac{1}{D} \qquad \forall e \in \mathbb{Z}_q^D.
   $$

## 4. Theorem 3 — Universal Word-Multiplicity Variety Pinching Under Uniform Error Tables

For each trajectory $w = (w_1, \dots, w_k) \in \{0, \dots, D-1\}^k$, define its **signed word-multiplicity vector** $\mu_\epsilon(w) \in \mathbb{Z}_q^D$ by
$$
\bigl[\mu_\epsilon(w)\bigr]_u \;:=\; \sum_{\substack{\ell=1 \\ w_\ell = u}}^{k} \epsilon_\ell \bmod q, \qquad u \in \{0, \dots, D-1\},
$$
so that $E_\epsilon(w) \equiv \langle \mu_\epsilon(w), e\rangle \pmod q$ and $\tau_\epsilon(w) \equiv \sum_{u=0}^{D-1} [\mu_\epsilon(w)]_u f(u) \pmod q$. Define the **word-multiplicity collision variety**:
$$
\mathcal{W}_\epsilon \;:=\; \bigl\{\, (w, w') \in \{0, \dots, D-1\}^{2k} : \mu_\epsilon(w) \equiv \mu_\epsilon(w') \pmod q \,\bigr\}.
$$

**Theorem 3 (Subvariety Inclusion $\mathcal{W}_\epsilon \subseteq \mathcal{V}_\epsilon(f)$ and Frequency-Table Independence of Error-Averaged Readout).**
1. Because $\mu_\epsilon(w) \equiv \mu_\epsilon(w') \pmod q \implies \tau_\epsilon(w) \equiv \tau_\epsilon(w') \pmod q$ for **every** frequency map $f : \{0, \dots, D-1\} \to \mathbb{Z}_q^n$, $\Delta_k \subseteq \mathcal{W}_\epsilon \subseteq \mathcal{V}_\epsilon(f)$ holds universally.
2. Averaging $\mathbb{E}_{s \sim \mathbb{Z}_q^n}[P_{\epsilon, \sigma}^{(e)}(x \mid s)]$ over a uniform error table $e \sim \operatorname{Unif}(\mathbb{Z}_q^D)$ annihilates all pairs in $\mathcal{V}_\epsilon(f) \setminus \mathcal{W}_\epsilon$ by character orthogonality on $\mathbb{Z}_q^D$, yielding
   $$
   \mathbb{E}_{e \sim \mathbb{Z}_q^D}\,\mathbb{E}_{s \sim \mathbb{Z}_q^n}\!\left[P_{\epsilon, \sigma}^{(e)}(x \mid s)\right]
   \;=\; \frac{1}{D^{k+1}} \sum_{(w, w') \in \mathcal{W}_\epsilon} \exp\!\left(\frac{2\pi i}{D}\bigl(\Phi_\sigma(w; x) - \Phi_\sigma(w'; x)\bigr)\right),
   $$
   which is **identically independent of the frequency table $f$**!

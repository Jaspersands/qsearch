# Native Higher-Call Two-Copy SWAP Purity Bridge: Coherent SWAP Excess vs Classical Coincidence Excess, 1-Call Variety Purity Law, and CNOT Autocorrelation Equivalence

## 1. Motivation and Scope

In `theorems/native_higher_call_kronecker_moment_rank_bridge.py` (Subsystem 23) and `theorems/native_higher_call_commutant_trace_orthogonality_audit.py` (Subsystem 26), we distinguished the computational-basis $L_2$ readout variance $\mathcal{E}_{\epsilon, \sigma} = \sum_{x=0}^{D-1}\operatorname{Var}_s[P_{\epsilon, \sigma}(x \mid s)]$ from the full operator Hilbert–Schmidt variance $\mathcal{V}_{\text{HS}}(\epsilon, \sigma) = 1 - \operatorname{Tr}(\bar{\rho}_{\epsilon, \sigma}^2)$.

When two copies of the $k$-call output state $|\Psi_{\epsilon, \sigma}(y(s))\rangle^{\otimes 2}$ are available for the same secret $s \in \mathbb{Z}_q^n$, how do two-copy quantum operations—specifically the coherent two-register SWAP test and the post-$F_D^{\sigma_k}$ modular CNOT difference measurement—compare against two independent single-copy measurements? This note proves three exact theorems resolving two-copy SWAP purity and CNOT difference readout.

## 2. Theorem 1 — Exact Coherent SWAP Excess vs Independent-Secret Purity

Let $S_D \in U(D^2)$ denote the two-register SWAP unitary $S_D(|x_1\rangle \otimes |x_2\rangle) = |x_2\rangle \otimes |x_1\rangle$, and let $\Pi_{\text{sym}} = \frac{1}{2}(I_{D^2} + S_D)$ and $\Pi_{\text{anti}} = \frac{1}{2}(I_{D^2} - S_D)$ be the symmetric and antisymmetric projectors.

**Theorem 1 (Coherent Same-Secret vs Independent-Secret SWAP Identity).**
1. **Same-Secret Coherent Pair ($\rho_{\text{same}}^{(2)} := \mathbb{E}_{s \sim \mathbb{Z}_q^n}[\rho_{\epsilon, \sigma}(s) \otimes \rho_{\epsilon, \sigma}(s)]$)**: Because $|\Psi_{\epsilon, \sigma}(y(s))\rangle^{\otimes 2}$ lies strictly in the symmetric subspace for every $s \in \mathbb{Z}_q^n$,
   $$
   \operatorname{Tr}\!\left(S_D\,\rho_{\text{same}}^{(2)}\right) \;=\; 1, \qquad
   \operatorname{Tr}\!\left(\Pi_{\text{anti}}\,\rho_{\text{same}}^{(2)}\right) \;=\; 0.
   $$
2. **Independent-Secret Pair ($\rho_{\text{ind}}^{(2)} := \bar{\rho}_{\epsilon, \sigma} \otimes \bar{\rho}_{\epsilon, \sigma}$)**: Drawing two copies from independent secrets $s, s' \stackrel{\text{i.i.d.}}{\sim} \operatorname{Unif}(\mathbb{Z}_q^n)$ yields
   $$
   \operatorname{Tr}\!\left(S_D\,\rho_{\text{ind}}^{(2)}\right) \;=\; \mathbb{E}_{s, s'}\!\left[\bigl|\langle \Psi_{\epsilon, \sigma}(y(s)) \mid \Psi_{\epsilon, \sigma}(y(s'))\rangle\bigr|^2\right] \;=\; \operatorname{Tr}\!\left(\bar{\rho}_{\epsilon, \sigma}^2\right),
   $$
   so the coherent SWAP expectation gap between same-secret and independent-secret pairs equals the **exact operator Hilbert–Schmidt variance** $\mathcal{V}_{\text{HS}}(\epsilon, \sigma)$:
   $$
   \operatorname{Tr}\!\left(S_D\,(\rho_{\text{same}}^{(2)} - \rho_{\text{ind}}^{(2)})\right) \;=\; 1 - \operatorname{Tr}\!\left(\bar{\rho}_{\epsilon, \sigma}^2\right) \;=\; \mathcal{V}_{\text{HS}}(\epsilon, \sigma),
   $$
   and the antisymmetric SWAP-rejection probability on $\rho_{\text{ind}}^{(2)}$ is $\operatorname{Tr}(\Pi_{\text{anti}}\,\rho_{\text{ind}}^{(2)}) = \frac{1}{2}\mathcal{V}_{\text{HS}}(\epsilon, \sigma)$.

## 3. Theorem 2 — Final-Fourier Direction Invariance of Purity and the 1-Call Collision Variety Law

**Theorem 2 (Pre-Fourier Frobenius Identity and Exact 1-Call Rational Purity).**
1. Because $\bar{\rho}_{\epsilon, \sigma} = F_D^{\sigma_k}\widehat{M}_{\epsilon, \sigma}(0)(F_D^{\sigma_k})^\dagger$ with $F_D^{\sigma_k}$ unitary, the ensemble purity $\operatorname{Tr}(\bar{\rho}_{\epsilon, \sigma}^2) = \|\widehat{M}_{\epsilon, \sigma}(0)\|_F^2$ is **identically invariant** under flipping the final Fourier direction $\sigma_k \mapsto -\sigma_k$.
2. For $k = 1$ ($\epsilon = (\epsilon_1), \sigma = (\sigma_1)$), $\bigl[\widehat{M}_{\epsilon_1, \sigma_1}(0)\bigr]_{u, v} = \frac{1}{D}\exp(\frac{2\pi i}{q}\epsilon_1(e(u) - e(v)))\,\mathbf{1}_{f(u) \equiv f(v) \pmod q}$, so $\bigl|\bigl[\widehat{M}_{\epsilon_1, \sigma_1}(0)\bigr]_{u, v}\bigr|^2 = \frac{1}{D^2}\mathbf{1}_{f(u) \equiv f(v) \pmod q}$ is independent of the error table $e$ and yields the exact rational purity formula:
   $$
   \operatorname{Tr}\!\left(\bar{\rho}_{\epsilon_1, \sigma_1}^2\right) \;=\; \frac{|\mathcal{V}_{\epsilon_1}(f)|}{D^2}, \qquad
   \mathcal{V}_{\text{HS}}(\epsilon_1, \sigma_1) \;=\; 1 - \frac{|\mathcal{V}_{\epsilon_1}(f)|}{D^2}.
   $$

## 4. Theorem 3 — Two-Copy Modular CNOT Difference Readout and Coincidence Excess Identity

For two copies prepared under the same secret $s \in \mathbb{Z}_q^n$, applying the modular subtraction gate $|x_1, x_2\rangle \mapsto |x_1, (x_2 - x_1) \bmod D\rangle$ after $F_D^{\sigma_k} \otimes F_D^{\sigma_k}$ and measuring the second register produces the difference distribution
$$
P_{\text{diff}}(\Delta \mid s) \;=\; \sum_{x=0}^{D-1} P_{\epsilon, \sigma}(x \mid s)\,P_{\epsilon, \sigma}\bigl((x + \Delta) \bmod D \;\big|\; s\bigr), \qquad \Delta \in \{0, \dots, D-1\}.
$$

**Theorem 3 (Exact Harmonic Autocorrelation Law and Coincidence Excess Identity).**
1. Averaging $P_{\text{diff}}(\Delta \mid s)$ over $s \sim \operatorname{Unif}(\mathbb{Z}_q^n)$ yields the exact harmonic autocorrelation decomposition:
   $$
   \mathbb{E}_{s \sim \mathbb{Z}_q^n}\bigl[P_{\text{diff}}(\Delta \mid s)\bigr]
   \;=\; \sum_{x=0}^{D-1} C_{\epsilon, \sigma}(0; x)\,C_{\epsilon, \sigma}(0; (x + \Delta) \bmod D)
   \;+\; \sum_{\delta \in \mathbb{Z}_q^n \setminus \{0\}} \sum_{x=0}^{D-1} C_{\epsilon, \sigma}(\delta; x)\,\overline{C_{\epsilon, \sigma}(\delta; (x + \Delta) \bmod D)}.
   $$
2. At $\Delta = 0$ (the two-copy computational coincidence event $x_1 = x_2$), the excess coincidence probability between same-secret pairs and independent-secret pairs equals the **exact computational-basis $L_2$ signal energy** $\mathcal{E}_{\epsilon, \sigma}$:
   $$
   \mathbb{E}_{s \sim \mathbb{Z}_q^n}\bigl[P_{\text{diff}}(0 \mid s)\bigr] \;-\; \sum_{x=0}^{D-1} C_{\epsilon, \sigma}(0; x)^2
   \;=\; \sum_{\delta \in \mathbb{Z}_q^n \setminus \{0\}} \sum_{x=0}^{D-1} \bigl|C_{\epsilon, \sigma}(\delta; x)\bigr|^2
   \;=\; \mathcal{E}_{\epsilon, \sigma} \;\le\; \mathcal{V}_{\text{HS}}(\epsilon, \sigma).
   $$

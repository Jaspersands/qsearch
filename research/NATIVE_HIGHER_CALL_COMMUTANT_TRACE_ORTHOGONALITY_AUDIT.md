# Native Higher-Call Commutant Trace-Orthogonality Audit: Operator Harmonic Zero-Trace Conservation, Purity-Deficit Parseval Identity, and Universal Unitary Readout Bounds

## 1. Motivation and Scope

In `theorems/native_higher_call_kronecker_moment_rank_bridge.py` (Subsystem 23), we established the Parseval identity for the computational-basis readout variance $\mathcal{E}_{\epsilon, \sigma} = \sum_{x=0}^{D-1}\operatorname{Var}_{s \sim \mathbb{Z}_q^n}[P_{\epsilon, \sigma}(x \mid s)]$. A central question for quantum algorithm design is whether replacing the final computational-basis measurement after $F_D^{\sigma_k}$ with an arbitrary unitary basis change $V \in U(D)$ (or general projective measurement) can unlock substantially larger secret-dependent variance from the **off-diagonal matrix elements** of the $k$-call density operator
$$
\rho_{\epsilon, \sigma}(s) \;:=\; |\Psi_{\epsilon, \sigma}(y(s))\rangle\langle\Psi_{\epsilon, \sigma}(y(s))| \;\in\; \mathbb{C}^{D \times D}.
$$
This note proves three exact operator-level theorems governing the matrix secret-Fourier harmonics $\widehat{\rho}_{\epsilon, \sigma}(\delta)$, their trace orthogonality, the exact purity-deficit Parseval identity, and the universal Frobenius upper bound over all readout unitaries $V \in U(D)$.

## 2. Theorem 1 — Matrix Secret-Fourier Harmonics and Exact Zero-Trace Orthogonality

Expand the $k$-call pure-state density matrix $\rho_{\epsilon, \sigma}(s)$ into its matrix secret-Fourier harmonics on $\mathbb{Z}_q^n$:
$$
\rho_{\epsilon, \sigma}(s) \;=\; \sum_{\delta \in \mathbb{Z}_q^n} \widehat{\rho}_{\epsilon, \sigma}(\delta)\,\omega_q^{\langle \delta, s\rangle}, \qquad
\widehat{\rho}_{\epsilon, \sigma}(\delta) \;:=\; \mathbb{E}_{s \sim \mathbb{Z}_q^n}\!\left[\rho_{\epsilon, \sigma}(s)\,\omega_q^{-\langle \delta, s\rangle}\right] \;\in\; \mathbb{C}^{D \times D}.
$$

**Theorem 1 (Operator Harmonic Adjoint Symmetry and Trace Orthogonality).**
For every $k \ge 1$, every schedule $(\epsilon, \sigma) \in \{-1, +1\}^k \times \{-1, +1\}^k$, and every difference frequency $\delta \in \mathbb{Z}_q^n$:
1. **Operator Hermitian Conjugation**: $\widehat{\rho}_{\epsilon, \sigma}(-\delta \bmod q) = \widehat{\rho}_{\epsilon, \sigma}(\delta)^\dagger$, and $\bar{\rho}_{\epsilon, \sigma} := \widehat{\rho}_{\epsilon, \sigma}(0)$ is a positive semidefinite density operator of unit trace.
2. **Exact Zero-Trace Conservation on All Non-Zero Harmonics**:
   $$
   \operatorname{Tr}\bigl(\widehat{\rho}_{\epsilon, \sigma}(0)\bigr) \;=\; 1, \qquad
   \operatorname{Tr}\bigl(\widehat{\rho}_{\epsilon, \sigma}(\delta)\bigr) \;=\; 0 \quad \forall \delta \in \mathbb{Z}_q^n \setminus \{0\}.
   $$
3. **Endpoint-Pinned Pre-Fourier Matrix Representation**: Conjugating by $F_D^{\sigma_k}$ defines $\widehat{M}_{\epsilon, \sigma}(\delta) := (F_D^{\sigma_k})^\dagger \widehat{\rho}_{\epsilon, \sigma}(\delta) F_D^{\sigma_k}$, whose $(u, v)$ entry is the sum over trajectory pairs $(w, w') \in \{0, \dots, D-1\}^{2k}$ pinned at final endpoints $w_k = u, w'_k = v$ with $\Delta\tau_\epsilon(w, w') = \delta$.

## 3. Theorem 2 — Exact Purity-Deficit Parseval Identity for Hilbert–Schmidt Variance

Define the full operator Hilbert–Schmidt variance across secrets $s \sim \operatorname{Unif}(\mathbb{Z}_q^n)$:
$$
\mathcal{V}_{\text{HS}}(\epsilon, \sigma) \;:=\; \mathbb{E}_{s \sim \mathbb{Z}_q^n}\!\left[\bigl\|\rho_{\epsilon, \sigma}(s) - \bar{\rho}_{\epsilon, \sigma}\bigr\|_F^2\right].
$$

**Theorem 2 (Exact Purity-Deficit Parseval Identity).**
Because $\rho_{\epsilon, \sigma}(s)$ is a pure state ($\operatorname{Tr}(\rho_{\epsilon, \sigma}(s)^2) = 1$) for every $s \in \mathbb{Z}_q^n$ and the characters $\{\omega_q^{\langle \delta, s\rangle}\}_{\delta \in \mathbb{Z}_q^n}$ are orthonormal in $L^2(\mathbb{Z}_q^n)$,
$$
\mathcal{V}_{\text{HS}}(\epsilon, \sigma)
\;=\; 1 - \operatorname{Tr}\!\left(\bar{\rho}_{\epsilon, \sigma}^2\right)
\;=\; \sum_{\delta \in \mathbb{Z}_q^n \setminus \{0\}} \bigl\|\widehat{\rho}_{\epsilon, \sigma}(\delta)\bigr\|_F^2
\;=\; \sum_{\delta \in \mathbb{Z}_q^n \setminus \{0\}} \bigl\|\widehat{M}_{\epsilon, \sigma}(\delta)\bigr\|_F^2
\;\le\; 1 - \frac{1}{D}.
$$

## 4. Theorem 3 — Universal Schur–Horn Upper Bound Over All Post-Circuit Readout Unitaries $V \in U(D)$

For any post-circuit unitary $V \in U(D)$, let $P_{\epsilon, \sigma}^{(V)}(x \mid s) := \langle x | V \rho_{\epsilon, \sigma}(s) V^\dagger | x \rangle$ denote the Born distribution in the rotated basis $\{V^\dagger |x\rangle\}_{x=0}^{D-1}$, with total $L_2$ signal energy
$$
\mathcal{E}_{\epsilon, \sigma}(V) \;:=\; \sum_{x=0}^{D-1} \operatorname{Var}_{s \sim \mathbb{Z}_q^n}\!\left[P_{\epsilon, \sigma}^{(V)}(x \mid s)\right].
$$

**Theorem 3 (Exact Diagonal/Off-Diagonal Decomposition and Universal Unitary Bound).**
1. For every post-circuit unitary $V \in U(D)$, splitting $V \widehat{\rho}_{\epsilon, \sigma}(\delta) V^\dagger$ into its diagonal and off-diagonal parts yields the exact conservation law
   $$
   \mathcal{E}_{\epsilon, \sigma}(V) \;+\; \sum_{\delta \in \mathbb{Z}_q^n \setminus \{0\}} \sum_{\substack{x, x' = 0 \\ x \ne x'}}^{D-1} \bigl|\langle x | V \widehat{\rho}_{\epsilon, \sigma}(\delta) V^\dagger | x'\rangle\bigr|^2
   \;=\; \mathcal{V}_{\text{HS}}(\epsilon, \sigma) \;=\; 1 - \operatorname{Tr}\!\left(\bar{\rho}_{\epsilon, \sigma}^2\right).
   $$
2. Consequently, for **every** unitary basis change $V \in U(D)$,
   $$
   \mathcal{E}_{\epsilon, \sigma}(V) \;\le\; 1 - \operatorname{Tr}\!\left(\bar{\rho}_{\epsilon, \sigma}^2\right) \;\le\; 1 - \frac{1}{D},
   $$
   proving that no unitary basis rotation after the $k$-call circuit can extract more total $L_2$ variance than the purity deficit $1 - \operatorname{Tr}(\bar{\rho}_{\epsilon, \sigma}^2)$ of the secret-averaged state.

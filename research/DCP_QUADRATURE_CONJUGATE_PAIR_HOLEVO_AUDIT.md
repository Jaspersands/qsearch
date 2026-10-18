# DCP Quadrature Conjugate-Pair Holevo Audit: Exact Bloch-Disk Holevo Capacity, Randomized $X/Y$ Fisher Isotropization Bounds, and Singlet Phase-Independence

## 1. Motivation and Scope

In the Dihedral Coset Problem (DCP) under symmetric modular phase noise $e \sim K_\eta$ on $\mathbb{Z}_q$ ($K_\eta(-e) = K_\eta(e)$), a pair state $|x\rangle + \omega_q^{d(s+e)}|x+d\rangle$ with known non-zero difference $d \in \{1, \dots, q-1\}$ reduces on $\operatorname{span}(|x\rangle, |x+d\rangle) \cong \mathbb{C}^2$ to the equatorial Bloch-disk density matrix
$$
\rho_d(s; K_\eta) \;=\; \frac{1}{2}\begin{pmatrix} 1 & \lambda_d\,e^{-i\theta_d(s)} \\ \lambda_d\,e^{i\theta_d(s)} & 1 \end{pmatrix}
\;=\; \frac{1}{2}\bigl(I_2 + \lambda_d\cos\theta_d(s)\,\sigma_X + \lambda_d\sin\theta_d(s)\,\sigma_Y\bigr),
$$
where $\theta_d(s) := \frac{2\pi d s}{q}$ and $\lambda_d := \sum_{e \in \mathbb{Z}_q} K_\eta(e)\cos\!\left(\frac{2\pi d e}{q}\right) \in [-1, 1]$ is the $d$-th harmonic visibility.

This note proves three exact theorems governing the single-pair Holevo capacity $\chi_d(K_\eta)$, the classical vs SLD quantum Fisher information of conjugate $\sigma_X / \sigma_Y$ quadrature readout, and the secret-phase independence of the two-copy singlet projection.

## 2. Theorem 1 — Exact Single-Pair Holevo Capacity on $\mathbb{Z}_q$

**Theorem 1 (Exact Closed-Form Holevo Information per Difference $d \in \{1, \dots, q-1\}$).**
For every $q \ge 2$, every symmetric noise kernel $K_\eta$ on $\mathbb{Z}_q$, and every non-zero difference $d \in \{1, \dots, q-1\}$:
1. For each secret $s \in \mathbb{Z}_q$, $\rho_d(s; K_\eta)$ has eigenvalues $\frac{1 \pm |\lambda_d|}{2}$ and von Neumann entropy $S(\rho_d(s; K_\eta)) = h_2\!\left(\frac{1 + |\lambda_d|}{2}\right)$ bits, where $h_2(p) := -p\log_2 p - (1-p)\log_2(1-p)$.
2. Because $\sum_{s=0}^{q-1} e^{\pm i 2\pi d s / q} = 0$ for every $d \in \{1, \dots, q-1\}$, the uniform secret average is the maximally mixed state $\bar{\rho}_d(K_\eta) := \frac{1}{q}\sum_{s=0}^{q-1} \rho_d(s; K_\eta) = \frac{1}{2}I_2$ with entropy $S(\bar{\rho}_d(K_\eta)) = 1$ bit.
3. Consequently, the exact Holevo information between a uniform secret $s \sim \operatorname{Unif}(\mathbb{Z}_q)$ and $\rho_d(s; K_\eta)$ is
   $$
   \chi_d(K_\eta) \;:=\; S\bigl(\bar{\rho}_d(K_\eta)\bigr) \;-\; \frac{1}{q}\sum_{s=0}^{q-1} S\bigl(\rho_d(s; K_\eta)\bigr) \;=\; 1 \;-\; h_2\!\left(\frac{1 + |\lambda_d|}{2}\right)\text{ bits}.
   $$

## 3. Theorem 2 — Exact SLD Quantum Fisher Information vs Conjugate $X/Y$ Quadrature Fisher Envelope

Parameterizing $\rho_d(\theta; \lambda_d) = \frac{1}{2}(I_2 + \lambda_d\cos\theta\,\sigma_X + \lambda_d\sin\theta\,\sigma_Y)$ by the continuous phase angle $\theta = \theta_d(s) \in [0, 2\pi)$:

**Theorem 2 (Exact SLD Quantum Fisher Information and Conjugate $X/Y$ Classical Fisher Envelope).**
For any $\lambda_d \in (-1, 1)$ and any phase angle $\theta \in [0, 2\pi)$:
1. **Constant SLD Quantum Fisher Information**: The Symmetric Logarithmic Derivative (SLD) operator is $L_\theta = -\lambda_d\sin\theta\,\sigma_X + \lambda_d\cos\theta\,\sigma_Y$, yielding constant quantum Fisher information across all $\theta \in [0, 2\pi)$:
   $$
   \mathcal{I}_Q(\theta; \lambda_d) \;:=\; \operatorname{Tr}\!\bigl(\rho_d(\theta; \lambda_d)\,L_\theta^2\bigr) \;=\; \lambda_d^2.
   $$
2. **Conjugate $X/Y$ Quadrature Classical Fisher Information**: Measuring $\sigma_X$ with probability $1/2$ and $\sigma_Y$ with probability $1/2$ achieves classical Fisher information
   $$
   \mathcal{I}_{XY}(\theta; \lambda_d)
   \;:=\; \frac{1}{2}\frac{\lambda_d^2\sin^2\theta}{1 - \lambda_d^2\cos^2\theta} \;+\; \frac{1}{2}\frac{\lambda_d^2\cos^2\theta}{1 - \lambda_d^2\sin^2\theta}
   \;=\; \frac{\lambda_d^2\bigl(1 - \lambda_d^2(\cos^4\theta + \sin^4\theta)\bigr)}{2(1 - \lambda_d^2\cos^2\theta)(1 - \lambda_d^2\sin^2\theta)},
   $$
   which eliminates the individual quadrature blind spots ($\mathcal{I}_X(0)=0, \mathcal{I}_Y(\pi/2)=0$) and satisfies the exact two-sided envelope across all $\theta \in [0, 2\pi)$:
   $$
   \frac{1}{2}\lambda_d^2 \;=\; \mathcal{I}_{XY}(0; \lambda_d) \;\le\; \mathcal{I}_{XY}(\theta; \lambda_d) \;\le\; \mathcal{I}_{XY}\!\left(\frac{\pi}{4}; \lambda_d\right) \;=\; \frac{\lambda_d^2}{2 - \lambda_d^2} \;<\; \lambda_d^2 \;=\; \mathcal{I}_Q(\theta; \lambda_d).
   $$

## 4. Theorem 3 — Two-Copy Singlet Phase Independence and Triplet Coherence Localization

Given two independent copies $\rho_d(\theta; \lambda_d) \otimes \rho_d(\theta; \lambda_d)$ at the same difference $d$, let $|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}$ be the antisymmetric singlet state and $\Pi_{\text{triplet}} = I_4 - |\Psi^-\rangle\langle\Psi^-|$ be the symmetric triplet projector.

**Theorem 3 (Exact Singlet Phase Independence and Noise-Purity Estimation).**
For every $\theta \in [0, 2\pi)$ and every $\lambda_d \in [-1, 1]$,
$$
P_{\text{singlet}}(\theta; \lambda_d) \;:=\; \langle \Psi^- | \bigl(\rho_d(\theta; \lambda_d) \otimes \rho_d(\theta; \lambda_d)\bigr) | \Psi^- \rangle \;=\; \frac{1 - \lambda_d^2}{4},
$$
$$
P_{\text{triplet}}(\theta; \lambda_d) \;:=\; \operatorname{Tr}\!\Bigl(\Pi_{\text{triplet}}\bigl(\rho_d(\theta; \lambda_d) \otimes \rho_d(\theta; \lambda_d)\bigr)\Bigr) \;=\; \frac{3 + \lambda_d^2}{4},
$$
both of which are **identically independent of the secret phase $\theta = 2\pi d s / q$** (carrying zero Fisher information about $s$), while all $\theta$-dependence is localized inside the symmetric triplet block with doubled-harmonic coherence $\langle 00 | (\rho_d \otimes \rho_d) | 11\rangle = \frac{1}{4}\lambda_d^2 e^{-2 i \theta}$.

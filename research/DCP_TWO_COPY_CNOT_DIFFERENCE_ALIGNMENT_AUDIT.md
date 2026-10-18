# DCP Two-Copy CNOT Difference-Alignment Audit: Exact Sum/Difference Branch Bifurcation, Diagonal/Anti-Diagonal Phase Annihilation, and Off-Diagonal Visibility Yield

## 1. Motivation and Scope

In standard Kuperberg-style Dihedral Coset Problem (DCP) sieving, two pair states with known differences $d_1, d_2 \in \{1, \dots, q-1\}$ are combined via a two-register CNOT gate $|b_1, b_2\rangle \mapsto |b_1, b_1 \oplus b_2\rangle$ followed by computational-basis measurement of the target syndrome bit $z = b_1 \oplus b_2 \in \{0, 1\}$.

When each input pair state $\rho_{d_j}(s; K_\eta) = \frac{1}{2}\begin{pmatrix} 1 & \lambda_{d_j}\omega_q^{-d_j s} \\ \lambda_{d_j}\omega_q^{d_j s} & 1 \end{pmatrix}$ ($j \in \{1, 2\}$) carries harmonic visibility $\lambda_{d_j} = \sum_{e \in \mathbb{Z}_q} K_\eta(e)\cos(2\pi d_j e / q)$ under a symmetric modular noise kernel $K_\eta$, how does the CNOT parity projection transform the state for arbitrary pairs $(d_1, d_2) \in \{1, \dots, q-1\}^2$, and what is the exact ensemble-averaged active quadratic visibility across all $(q-1)^2$ difference pairs? This note proves three exact theorems resolving two-copy CNOT difference alignment.

## 2. Theorem 1 — Exact Sum/Difference Frequency Bifurcation Under Two-Copy CNOT Projection

Apply $\mathrm{CNOT}_{1 \to 2}$ to $\rho_{d_1}(s; K_\eta) \otimes \rho_{d_2}(s; K_\eta)$ and measure the second register in the computational basis $\{|0\rangle, |1\rangle\}$ with outcome $z \in \{0, 1\}$.

**Theorem 1 (Equiprobable Syndrome Branches and Exact Sum/Difference State Bifurcation).**
For every $q \ge 3$, every symmetric noise kernel $K_\eta$, every secret $s \in \mathbb{Z}_q$, and every pair $(d_1, d_2) \in \{1, \dots, q-1\}^2$:
1. **Universal Equiprobable Syndromes**: Both syndrome outcomes occur with exact probability
   $$
   \Pr(z = 0 \mid d_1, d_2, s) \;=\; \Pr(z = 1 \mid d_1, d_2, s) \;=\; \frac{1}{2}.
   $$
2. **Exact Post-Measurement Branch States**: The reduced state on the first register conditioned on $z \in \{0, 1\}$ is
   $$
   \rho_{d_1, d_2}^{(z=0)}(s; K_\eta) \;=\; \frac{1}{2}\begin{pmatrix} 1 & \lambda_{d_1}\lambda_{d_2}\,\omega_q^{-(d_1 + d_2) s} \\ \lambda_{d_1}\lambda_{d_2}\,\omega_q^{(d_1 + d_2) s} & 1 \end{pmatrix},
   $$
   $$
   \rho_{d_1, d_2}^{(z=1)}(s; K_\eta) \;=\; \frac{1}{2}\begin{pmatrix} 1 & \lambda_{d_1}\lambda_{d_2}\,\omega_q^{-(d_1 - d_2) s} \\ \lambda_{d_1}\lambda_{d_2}\,\omega_q^{(d_1 - d_2) s} & 1 \end{pmatrix},
   $$
   producing effective difference $d_+ := (d_1 + d_2) \bmod q$ on $z = 0$ and $d_- := (d_1 - d_2) \bmod q$ on $z = 1$, both with product coherence amplitude $\lambda_{d_1}\lambda_{d_2}$.

## 3. Theorem 2 — Diagonal and Anti-Diagonal Phase Annihilation Loci

For a branch state with effective difference $d_{\text{eff}} \in \mathbb{Z}_q$ and coherence $\Lambda = \lambda_{d_1}\lambda_{d_2}$, the ensemble over all $s\in\mathbb{Z}_q$ carries secret information if and only if BOTH $d_{\text{eff}} \not\equiv 0 \pmod q$ AND $\Lambda\ne0$. A zero effective difference makes the phase secret-independent; zero coherence gives $I/2$ for every secret even at a nonzero effective difference. Both cases have zero Holevo information. An SLD Fisher interpretation requires specifying a continuous parameter extension and is not itself a discrete-secret recovery guarantee.

**Theorem 2 (Exact Active Quadratic Visibility per Pair $(d_1, d_2)$).**
Define the syndrome-averaged active quadratic visibility of a pair $(d_1, d_2) \in \{1, \dots, q-1\}^2$:
$$
\mathcal{Y}(d_1, d_2; K_\eta) \;:=\; \frac{1}{2}\,\mathbf{1}_{d_1 + d_2 \not\equiv 0 \pmod q}\,\lambda_{d_1}^2\lambda_{d_2}^2 \;+\; \frac{1}{2}\,\mathbf{1}_{d_1 - d_2 \not\equiv 0 \pmod q}\,\lambda_{d_1}^2\lambda_{d_2}^2.
$$
1. On the **anti-diagonal locus** $d_1 + d_2 \equiv 0 \pmod q$ ($d_2 = q - d_1$), the $z = 0$ sum branch is secret-independent ($d_+ = 0$), while the $z = 1$ difference branch has doubled frequency $2 d_1 \bmod q$.
2. On the **diagonal locus** $d_1 = d_2$, the $z = 1$ difference branch is secret-independent ($d_- = 0$), while the $z = 0$ sum branch has doubled frequency $2 d_1 \bmod q$.

## 4. Theorem 3 — Exact Off-Diagonal Pair Formula for Ensemble-Averaged Active Visibility

**Theorem 3 (Exact Cancellation of Diagonal and Anti-Diagonal Fourth-Moment Losses).**
Because $K_\eta(-e) = K_\eta(e)$ is symmetric, $\lambda_{q - d} = \lambda_d$ for all $d \in \{1, \dots, q-1\}$. Therefore, the $z = 0$ anti-diagonal loss $\frac{1}{2}\sum_{d=1}^{q-1} \lambda_d^2 \lambda_{q-d}^2 = \frac{1}{2}\sum_{d=1}^{q-1} \lambda_d^4$ and the $z = 1$ diagonal loss $\frac{1}{2}\sum_{d=1}^{q-1} \lambda_d^4$ sum to **exactly** $\sum_{d=1}^{q-1} \lambda_d^4$ for every $q \ge 3$ (even or odd). Averaging $\mathcal{Y}(d_1, d_2; K_\eta)$ over uniform $(d_1, d_2) \in \{1, \dots, q-1\}^2$ yields the exact closed-form identity:
$$
\mathbb{E}_{d_1, d_2 \in \{1, \dots, q-1\}}\!\bigl[\mathcal{Y}(d_1, d_2; K_\eta)\bigr]
\;=\; \frac{\bigl(\sum_{d=1}^{q-1}\lambda_d^2\bigr)^2 - \sum_{d=1}^{q-1}\lambda_d^4}{(q - 1)^2}
\;=\; \frac{\bigl(q\|K_\eta\|_2^2 - 1\bigr)^2 - \sum_{d=1}^{q-1}\lambda_d^4}{(q - 1)^2}
\;=\; \frac{1}{(q - 1)^2}\sum_{\substack{1 \le d_1, d_2 \le q-1 \\ d_1 \ne d_2}} \lambda_{d_1}^2\lambda_{d_2}^2.
$$

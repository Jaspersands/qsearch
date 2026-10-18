# DCP Subset-Sum Modular Collision-Entropy Audit: Cosine-Product Parseval Formula, Universal Boolean-Difference Surjectivity, and Exact Ensemble Collision Law

## 1. Motivation and Scope

In subset-sum and lattice-based reductions to the Dihedral Coset Problem (DCP), a public weight vector $\mathbf{a} = (a_1, \dots, a_m) \in \mathbb{Z}_q^m$ defines the modular subset-sum map $f_{\mathbf{a}}(x) := \sum_{j=1}^m a_j x_j \bmod q$ on the Boolean hypercube $\{0, 1\}^m$. Preparing $2^{-m/2}\sum_{x \in \{0, 1\}^m}|x\rangle|f_{\mathbf{a}}(x)\rangle$ and measuring the sum register $|z\rangle$ ($z \in \mathbb{Z}_q$) projects the index register onto the subset-sum fiber $f_{\mathbf{a}}^{-1}(z)$ with probability $P_{\mathbf{a}}(z) = 2^{-m}|f_{\mathbf{a}}^{-1}(z)|$.

The collision probability (Rényi-2 purity) $C(\mathbf{a}) := \sum_{z \in \mathbb{Z}_q} P_{\mathbf{a}}(z)^2$ and the off-diagonal collision probability $C_{\text{off}}(\mathbf{a}) := C(\mathbf{a}) - 2^{-m}$ govern the probability of obtaining multi-element fibers $|f_{\mathbf{a}}^{-1}(z)| \ge 2$. This note proves three exact theorems characterizing $C(\mathbf{a})$ for every fixed $\mathbf{a} \in \mathbb{Z}_q^m$ and its exact expectation over $\mathbf{a} \sim \operatorname{Unif}(\mathbb{Z}_q^m)$ for all prime and composite moduli $q \ge 2$.

## 2. Theorem 1 — Exact Cosine-Product Parseval Formula for Subset-Sum Collision Probability

**Theorem 1 (Exact Cosine-Squared Product Identity for $C(\mathbf{a})$).**
For every modulus $q \ge 2$, every dimension $m \ge 1$, and every weight vector $\mathbf{a} = (a_1, \dots, a_m) \in \mathbb{Z}_q^m$:
1. The discrete Fourier transform $\widehat{P}_{\mathbf{a}}(u) := \sum_{z \in \mathbb{Z}_q} P_{\mathbf{a}}(z)\,\omega_q^{-u z}$ satisfies
   $$
   \bigl|\widehat{P}_{\mathbf{a}}(u)\bigr|^2 \;=\; \prod_{j=1}^m \left|\frac{1 + \omega_q^{-u a_j}}{2}\right|^2 \;=\; \prod_{j=1}^m \cos^2\!\left(\frac{\pi u a_j}{q}\right), \qquad u \in \mathbb{Z}_q.
   $$
2. By Parseval's theorem on $\mathbb{Z}_q$, the subset-sum collision probability and off-diagonal collision probability equal
   $$
   C(\mathbf{a}) \;:=\; \sum_{z \in \mathbb{Z}_q} P_{\mathbf{a}}(z)^2 \;=\; \frac{1}{q}\sum_{u=0}^{q-1} \prod_{j=1}^m \cos^2\!\left(\frac{\pi u a_j}{q}\right),
   \qquad
   C_{\text{off}}(\mathbf{a}) \;=\; C(\mathbf{a}) - 2^{-m}.
   $$

## 3. Theorem 2 — Universal Boolean-Difference Unit Property and Exact Quenched Collision Expectation

**Theorem 2 (Universal $\mathbb{Z}_q$-Surjectivity of Non-Zero Boolean Differences and Exact Mean Collision Law).**
For **every** integer modulus $q \ge 2$ (whether prime, prime-power, or composite) and every $m \ge 1$:
1. For any two distinct Boolean vectors $x \ne x' \in \{0, 1\}^m$, the difference $\delta = x - x' \in \{-1, 0, +1\}^m \setminus \{0\}$ has at least one coordinate $\delta_{j^*} \in \{-1, +1\} \subseteq \mathbb{Z}_q^\times$ (a unit modulo $q$ for every $q \ge 2$). Consequently, $\mathbf{a} \mapsto \langle \mathbf{a}, x - x'\rangle \bmod q$ is a $q^{m-1}$-to-$1$ surjection onto $\mathbb{Z}_q$, and
   $$
   \Pr_{\mathbf{a} \sim \operatorname{Unif}(\mathbb{Z}_q^m)}\!\bigl[f_{\mathbf{a}}(x) \equiv f_{\mathbf{a}}(x') \pmod q\bigr] \;=\; \frac{1}{q} \qquad \forall x \ne x' \in \{0, 1\}^m.
   $$
2. Averaging over all $2^{2m}$ pairs $(x, x') \in \{0, 1\}^{2m}$ yields the exact modulus-universal ensemble collision laws:
   $$
   \mathbb{E}_{\mathbf{a} \sim \mathbb{Z}_q^m}\bigl[C(\mathbf{a})\bigr] \;=\; 2^{-m} \;+\; \bigl(1 - 2^{-m}\bigr)\frac{1}{q} \;=\; \frac{1}{q} \;+\; \left(1 - \frac{1}{q}\right)2^{-m},
   $$
   $$
   \mathbb{E}_{\mathbf{a} \sim \mathbb{Z}_q^m}\bigl[C_{\text{off}}(\mathbf{a})\bigr] \;=\; \frac{1 - 2^{-m}}{q}.
   $$

## 4. Theorem 3 — Exact Single-Coordinate Cosine-Squared Character Average

**Theorem 3 (Exact Orthogonality of $\cos^2(\pi u a / q)$ on $\mathbb{Z}_q$).**
For every modulus $q \ge 2$ and every frequency $u \in \{0, 1, \dots, q-1\}$, writing $\cos^2(\pi u a / q) = \frac{1 + \cos(2\pi u a / q)}{2}$ and applying character orthogonality $\sum_{a=0}^{q-1} \cos(2\pi u a / q) = q\,\mathbf{1}_{u = 0}$ yields
$$
\frac{1}{q}\sum_{a=0}^{q-1} \cos^2\!\left(\frac{\pi u a}{q}\right) \;=\;
\begin{cases}
1, & u = 0, \\
\frac{1}{2}, & u \in \{1, \dots, q-1\},
\end{cases}
$$
so that factoring the expectation over independent coordinates $a_1, \dots, a_m \sim \operatorname{Unif}(\mathbb{Z}_q)$ gives
$$
\mathbb{E}_{\mathbf{a} \sim \mathbb{Z}_q^m}\bigl[C(\mathbf{a})\bigr]
\;=\; \frac{1}{q}\sum_{u=0}^{q-1} \prod_{j=1}^m \mathbb{E}_{a_j}\!\left[\cos^2\!\left(\frac{\pi u a_j}{q}\right)\right]
\;=\; \frac{1}{q}\Bigl(1 + (q - 1)\,2^{-m}\Bigr)
\;=\; \frac{1}{q} \;+\; \left(1 - \frac{1}{q}\right)2^{-m}.
$$

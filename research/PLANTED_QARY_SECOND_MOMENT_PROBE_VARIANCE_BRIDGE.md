# Planted $q$-ary Second-Moment Probe-Variance Bridge: Exact Two-Point Variance Law, Projective-Ray Covariance Localization, and Dual-Spike Concentration

## 1. Motivation and Scope

In `theorems/planted_qary_multiprobe_gl_rank_saturation_bridge.py` (Subsystem 18), we proved that for any dimension-$d$ planted subspace $B = \operatorname{rowspan}(M) \subset \mathbb{F}_q^n$ and any zero-free window $W \subset \mathbb{F}_q \setminus \{0\}$ of size $R = |W|$, the first moment $\mathbb{E}_{u \sim \mathbb{F}_q^n}[N_W(u; B)] = (q^d - 1)(R/q)$ is identical to that of any subset $S \subset \mathbb{F}_q^n \setminus \{0\}$ of cardinality $q^d - 1$.

This raises the natural second-moment question: how does the **variance** $\operatorname{Var}_{u \sim \mathbb{F}_q^n}[N_W(u; B)]$ of a planted subspace compare to that of a ray-free subset $S \subset \mathbb{F}_q^n \setminus \{0\}$ (containing at most one vector per projective line in $\mathbb{P}(\mathbb{F}_q^n)$), and where is the variance of $N_W(u; B)$ localized in probe space $\mathbb{F}_q^n$? This note proves three exact theorems resolving the second moment of linear-probe window counts.

## 2. Theorem 1 — Exact Two-Point Distribution and Variance Law for Planted Subspaces

For a dimension-$d$ subspace $B \subset \mathbb{F}_q^n$ ($1 \le d \le n$) and window $W \subset \mathbb{F}_q$ of size $R = |W|$, let $N_W(u; B) := |\{b \in B : \langle b, u\rangle \in W\}|$.

**Theorem 1 (Exact Two-Point Probe Variance Law).**
Under a uniform probe $u \sim \operatorname{Unif}(\mathbb{F}_q^n)$, $N_W(u; B)$ is a two-valued random variable taking value $q^{d-1} R$ on $\mathbb{F}_q^n \setminus B^\perp$ (probability $1 - q^{-d}$) and value $q^d\,\mathbf{1}_{0 \in W}$ on $B^\perp$ (probability $q^{-d}$). Consequently, its exact mean and variance are
$$
\mathbb{E}_{u \sim \mathbb{F}_q^n}\bigl[N_W(u; B)\bigr] \;=\; \mathbf{1}_{0 \in W} \;+\; (q^d - 1)\frac{R}{q},
$$
$$
\operatorname{Var}_{u \sim \mathbb{F}_q^n}\bigl[N_W(u; B)\bigr]
\;=\; q^{-d}(1 - q^{-d})\,\bigl(q^d\,\mathbf{1}_{0 \in W} - q^{d-1} R\bigr)^2
\;=\; (q^d - 1)\left(\mathbf{1}_{0 \in W} - \frac{R}{q}\right)^2.
$$

*Proof.*
For any $u \notin B^\perp$, $b \mapsto \langle b, u\rangle$ is a $q^{d-1}$-to-$1$ surjection onto $\mathbb{F}_q$, so $N_W(u; B) = q^{d-1}R$. For $u \in B^\perp$, $\langle b, u\rangle = 0$ for all $b \in B$, so $N_W(u; B) = q^d\,\mathbf{1}_{0 \in W}$. A two-valued random variable taking values $v_1, v_0$ with probabilities $p, 1-p$ has variance $p(1-p)(v_1 - v_0)^2 = q^{-d}(1 - q^{-d}) q^{2d}(\mathbf{1}_{0 \in W} - R/q)^2 = (q^d - 1)(\mathbf{1}_{0 \in W} - R/q)^2$. $\square$

## 3. Theorem 2 — Projective-Ray Covariance Localization and Zero Off-Ray Covariance

Partition $B \setminus \{0\}$ into $L_d := \frac{q^d - 1}{q - 1}$ projective rays $\mathcal{R}_1, \dots, \mathcal{R}_{L_d}$, where each ray $\mathcal{R}_i = \{\lambda b_i : \lambda \in \mathbb{F}_q^\times\}$ has size $q - 1$.

**Theorem 2 (Pairwise Independence Across Distinct Projective Rays).**
1. **Zero Off-Ray Covariance**: For any two vectors $b, b' \in \mathbb{F}_q^n \setminus \{0\}$ lying on distinct projective rays ($b' \notin \mathbb{F}_q^\times b$), the pair $(\langle b, u\rangle, \langle b', u\rangle)$ is uniformly distributed on $\mathbb{F}_q^2$ as $u \sim \operatorname{Unif}(\mathbb{F}_q^n)$, so
   $$
   \operatorname{Cov}_{u \sim \mathbb{F}_q^n}\bigl(\mathbf{1}_{\langle b, u\rangle \in W},\; \mathbf{1}_{\langle b', u\rangle \in W}\bigr) \;=\; 0.
   $$
2. **Exact Within-Ray Variance Decomposition**: Let $Y_i(u) := \sum_{b \in \mathcal{R}_i} \mathbf{1}_{\langle b, u\rangle \in W}$ denote the window count on ray $\mathcal{R}_i$. Because distinct rays are pairwise uncorrelated ($\operatorname{Cov}_u(Y_i, Y_j) = 0$ for $i \ne j$), the variance of $N_W(u; B) = \mathbf{1}_{0 \in W} + \sum_{i=1}^{L_d} Y_i(u)$ is the sum of the $L_d$ individual ray variances:
   $$
   \operatorname{Var}_{u \sim \mathbb{F}_q^n}\bigl[N_W(u; B)\bigr] \;=\; \sum_{i=1}^{L_d} \operatorname{Var}_{u \sim \mathbb{F}_q^n}\bigl[Y_i(u)\bigr] \;=\; \frac{q^d - 1}{q - 1}\,\operatorname{Var}_u\bigl[Y_1(u)\bigr].
   $$
   Specifically, for a zero-free window $W \subset \mathbb{F}_q \setminus \{0\}$ of size $R$, each ray count $Y_i(u)$ equals $R$ when $\langle b_i, u\rangle \ne 0$ (probability $\frac{q-1}{q}$) and $0$ when $\langle b_i, u\rangle = 0$ (probability $\frac{1}{q}$), giving $\operatorname{Var}_u[Y_i(u)] = \frac{q-1}{q^2} R^2$ and
   $$
   \sum_{i=1}^{L_d} \operatorname{Var}_u\bigl[Y_i(u)\bigr] \;=\; \frac{q^d - 1}{q - 1}\cdot\frac{q - 1}{q^2} R^2 \;=\; (q^d - 1)\left(\frac{R}{q}\right)^2.
   $$

## 4. Theorem 3 — Variance Ratio Between Planted Subspaces and Ray-Free Unstructured Sets

**Theorem 3 (Subspace vs Ray-Free Subset Variance Ratio and Off-Dual Flatness).**
Let $S \subset \mathbb{F}_q^n \setminus \{0\}$ be any ray-free subset of cardinality $|S| = q^d - 1$ (containing at most one vector per projective ray in $\mathbb{P}(\mathbb{F}_q^n)$, whenever $q^d - 1 \le \frac{q^n - 1}{q - 1}$), and let $W \subset \mathbb{F}_q \setminus \{0\}$ be any zero-free window of size $R \in \{1, \dots, q - 1\}$.
1. By Theorem 2(1), the indicators $\{\mathbf{1}_{\langle x, u\rangle \in W}\}_{x \in S}$ are pairwise independent Bernoulli($R/q$) variables, so
   $$
   \operatorname{Var}_{u \sim \mathbb{F}_q^n}\bigl[N_W(u; S)\bigr] \;=\; (q^d - 1)\frac{R}{q}\left(1 - \frac{R}{q}\right),
   $$
   and the exact variance ratio between the planted subspace $B$ and any ray-free subset $S$ of the same non-zero size is
   $$
   \frac{\operatorname{Var}_u\bigl[N_W(u; B)\bigr]}{\operatorname{Var}_u\bigl[N_W(u; S)\bigr]} \;=\; \frac{R}{q - R}.
   $$
2. Conditioned on the off-dual event $u \notin B^\perp$ (probability $1 - q^{-d}$), $\operatorname{Var}_{u \sim \mathbb{F}_q^n \setminus B^\perp}[N_W(u; B)] = 0$ identically, proving that 100% of the probe variance of a planted subspace is generated by the $q^{-d}$-rare dual collapse at $u \in B^\perp$.

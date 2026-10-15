# Planted $q$-ary Multiprobe $GL_d(\mathbb{F}_q)$ Rank-Saturation Bridge: Exact $k$-Probe Acceptance Laws, First-Moment Indistinguishability, and $q$-Binomial Rank Stratification

## 1. Motivation and Scope

In `theorems/planted_qary_offset_pair_mass_frontier_audit.py`, the 2-probe offset-pair mass law $M_{\text{pair}}(q, R, B) = R(R-1)/q^2$ was established for non-collinear probe pairs $(u_1, u_2)$ against a 2-dimensional planted subspace $B \subset \mathbb{F}_q^n$. A natural algorithmic question is whether querying $k \ge 2$ linear probes $(u_1, \dots, u_k) \in (\mathbb{F}_q^n)^k$ simultaneously against a dimension-$d$ planted subspace $B = \operatorname{rowspan}(M) \subset \mathbb{F}_q^n$ ($|B| = q^d$) with an acceptance window $W \subset \mathbb{F}_q$ of size $R = |W|$ creates a first-moment statistical signal that distinguishes $B \setminus \{0\}$ from an unstructured subset of size $q^d$, or how the acceptance distribution stratifies by the projected rank $r = \operatorname{rank}([M u_1, \dots, M u_k]) \in \{0, \dots, \min(d, k)\}$.

This note proves three exact theorems resolving the $k$-probe acceptance distribution across all $(q, d, k, R)$.

## 2. Theorem 1 — Exact $GL_d(\mathbb{F}_q)$ Full-Rank $k$-Probe Acceptance Law and Universal First Moment

Let $M \in \mathbb{F}_q^{d \times n}$ have full row rank $d$ ($1 \le d \le n$), and let $B = \{c^T M : c \in \mathbb{F}_q^d\} \subset \mathbb{F}_q^n$ be the planted subspace of cardinality $|B| = q^d$. For any $k$-probe tuple $U = (u_1, \dots, u_k) \in (\mathbb{F}_q^n)^k$, define the projected probe matrix
$$
P(U) \;:=\; \bigl[\, M u_1,\; M u_2,\; \dots,\; M u_k \,\bigr] \;\in\; \mathbb{F}_q^{d \times k},
$$
and for any window $W \subset \mathbb{F}_q$ of size $R = |W|$, define the $k$-probe acceptance count
$$
N_W(U; B) \;:=\; \bigl|\bigl\{\, b \in B : \forall \ell \in \{1, \dots, k\},\; \langle b, u_\ell \rangle \in W \,\bigr\}\bigr|.
$$

**Theorem 1 (Full-Rank Exact Count and Universal First-Moment Law).**
1. **Deterministic Full-Rank Law ($k \le d$)**: Whenever $\operatorname{rank}(P(U)) = k \le d$, the linear evaluation map $c \mapsto c^T P(U)$ from $\mathbb{F}_q^d$ to $\mathbb{F}_q^k$ is surjective with kernel dimension $d - k$. Consequently, for every window $W \subset \mathbb{F}_q$ of size $R = |W|$,
   $$
   N_W(U; B) \;=\; q^{d - k} R^k, \qquad \frac{N_W(U; B)}{|B|} \;=\; \left(\frac{R}{q}\right)^k.
   $$
2. **Universal First-Moment Law (All $k \ge 1, d \ge 1$)**: Averaging over a uniform $k$-tuple $U = (u_1, \dots, u_k) \sim \operatorname{Unif}((\mathbb{F}_q^n)^k)$, every non-zero planted vector $b \in B \setminus \{0\}$ has i.i.d. uniform inner products $(\langle b, u_1\rangle, \dots, \langle b, u_k\rangle) \sim \operatorname{Unif}(\mathbb{F}_q^k)$, while $b = 0$ evaluates deterministically to $(0, \dots, 0)$. Therefore:
   $$
   \mathbb{E}_{U}\bigl[N_W(U; B)\bigr] \;=\; \mathbf{1}_{0 \in W} \;+\; (q^d - 1)\left(\frac{R}{q}\right)^k.
   $$

## 3. Theorem 2 — Zero-Free First-Moment Indistinguishability and Rank-Saturation Variance

**Theorem 2 (First-Moment Indistinguishability on $B \setminus \{0\}$).**
1. For any zero-free window $W \subset \mathbb{F}_q \setminus \{0\}$ ($0 \notin W$, $|W| = R$), the zero vector $b = 0$ is excluded for every probe tuple $U$, and the normalized first-moment $k$-probe mass on $B$ is
   $$
   M_k^{\text{zero-free}}(q, d, R) \;:=\; \frac{1}{q^d}\,\mathbb{E}_{U}\bigl[N_W(U; B)\bigr] \;=\; \frac{q^d - 1}{q^d}\left(\frac{R}{q}\right)^k,
   $$
   which coincides identically with the expected normalized acceptance count of an unstructured subset $S \subset \mathbb{F}_q^n \setminus \{0\}$ of size $q^d - 1$.
2. When $k \le d$ and $0 \notin W$, any full-rank probe tuple $\operatorname{rank}(P(U)) = k$ yields $N_W(U; B) = q^{d-k} R^k$ (since $0 \notin W^k$ automatically excludes the $\ker(P(U)^T)$ zero-evaluation fiber). Thus any fluctuation of $N_W(U; B)$ away from $q^{d-k} R^k$ is supported exclusively on the rank-deficient locus $\operatorname{rank}(P(U)) < k$.

## 4. Theorem 3 — Exact $q$-Binomial Rank Stratification of Projected $k$-Probe Matrices

**Theorem 3 ($q$-Gaussian Rank Distribution).**
Because $M \in \mathbb{F}_q^{d \times n}$ has full row rank $d$, $P(U) = [M u_1, \dots, M u_k]$ is uniformly distributed over $\mathbb{F}_q^{d \times k}$ when $U \sim \operatorname{Unif}((\mathbb{F}_q^n)^k)$. For each $r \in \{0, 1, \dots, \min(d, k)\}$, the exact probability that $\operatorname{rank}(P(U)) = r$ is
$$
P_{\text{rank}}(r \mid q, d, k) \;=\; q^{-d k} \binom{d}{r}_q \prod_{j=0}^{r-1} \bigl(q^k - q^j\bigr),
$$
where $\binom{d}{r}_q = \prod_{i=0}^{r-1} \frac{q^{d-i}-1}{q^{r-i}-1}$ is the Gaussian $q$-binomial coefficient, and $\sum_{r=0}^{\min(d, k)} P_{\text{rank}}(r \mid q, d, k) = 1$.

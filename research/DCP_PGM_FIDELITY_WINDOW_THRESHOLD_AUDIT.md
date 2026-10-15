# DCP PGM Fidelity Window-Threshold Audit: Exact Bhattacharyya Convolution Formula, Flat-Window Optimality, and Contiguous Support Copy Lower Bounds

## 1. Motivation and Scope

For any shift-covariant quantum state family $\{|\psi_s\rangle\}_{s \in \mathbb{Z}_q}$ where $|\psi_s\rangle = \sum_{u \in \mathbb{Z}_q} \sqrt{p_u}\,\omega_q^{-s u}|u\rangle$ has Fourier probability profile $p = (p_0, \dots, p_{q-1})$ on $\mathbb{Z}_q$, the $K$-copy state $|\psi_s\rangle^{\otimes K}$ decomposes into weight fibers indexed by total modular frequency $m \equiv u_1 + \dots + u_K \pmod q$, whose total weight is the $K$-fold cyclic convolution
$$
W_K(m) \;:=\; p^{*K}(m) \;=\; \sum_{\substack{(u_1, \dots, u_K) \in \mathbb{Z}_q^K \\ u_1 + \dots + u_K \equiv m \pmod q}} p_{u_1}\cdots p_{u_K}.
$$
When the Fourier profile $p$ is band-limited or restricted to a window of size $R = |\operatorname{supp}(p)| \le q$, how many copies $K$ are required for the Pretty Good Measurement (PGM) to identify $s \in \mathbb{Z}_q$ with success probability at least $\tau$? This note proves three exact theorems governing the $K$-copy covariant PGM success probability.

## 2. Theorem 1 — Exact Bhattacharyya Convolution Formula for $K$-Copy Covariant PGM Success

**Theorem 1 (Exact $K$-Copy PGM Success Probability via Cyclic Convolution).**
For any Fourier weight distribution $p$ on $\mathbb{Z}_q$ and any copy count $K \ge 1$, the optimal shift-covariant POVM (Pretty Good Measurement) for identifying a uniform secret $s \sim \operatorname{Unif}(\mathbb{Z}_q)$ from $|\psi_s\rangle^{\otimes K}$ achieves exact success probability
$$
P_{\text{PGM}}^{\text{succ}}(K; p) \;=\; \frac{1}{q}\left(\sum_{m=0}^{q-1} \sqrt{W_K(m)}\right)^2 \;=\; \left(\sum_{m=0}^{q-1} \sqrt{\frac{1}{q}\,W_K(m)}\right)^2,
$$
where $W_K = p^{*K}$ is the $K$-fold cyclic convolution of $p$ on $\mathbb{Z}_q$. Equivalently, calling $\rho_{\text{avg}}^{(K)} = \frac{1}{q}\sum_{s=0}^{q-1} (|\psi_s\rangle\langle\psi_s|)^{\otimes K}$, the non-zero eigenvalues of $\rho_{\text{avg}}^{(K)}$ are precisely $\{W_K(m) : m \in \operatorname{supp}(W_K)\}$, and $\operatorname{Tr}\bigl(\sqrt{\rho_{\text{avg}}^{(K)}}\bigr)^2 / q = P_{\text{PGM}}^{\text{succ}}(K; p)$.

## 3. Theorem 2 — Support-Rank Upper Bound and Flat-Window Optimality

**Theorem 2 (Exact Support-Ratio Upper Bound and Flat-Window Saturation).**
1. For any $K \ge 1$ and any Fourier distribution $p$ on $\mathbb{Z}_q$, let $S_K := \operatorname{supp}(W_K) = \{m \in \mathbb{Z}_q : W_K(m) > 0\}$. By Cauchy–Schwarz on $S_K$,
   $$
   P_{\text{PGM}}^{\text{succ}}(K; p) \;=\; \frac{1}{q}\left(\sum_{m \in S_K} 1 \cdot \sqrt{W_K(m)}\right)^2 \;\le\; \frac{|S_K|}{q} \sum_{m \in S_K} W_K(m) \;=\; \frac{|S_K|}{q}.
   $$
2. At $K = 1$, $P_{\text{PGM}}^{\text{succ}}(1; p) \le |\operatorname{supp}(p)| / q = R / q$, with equality if and only if $p_u = 1/R$ for all $u \in \operatorname{supp}(p)$ (a flat window distribution).

## 4. Theorem 3 — Contiguous Window Support-Growth Law and Copy Complexity Lower Bound

**Theorem 3 (Contiguous Window Sumset Growth and Minimum Copy Threshold).**
Suppose $\operatorname{supp}(p) = \{0, 1, \dots, R - 1\} \subset \mathbb{Z}_q$ is a contiguous window of width $R \in \{2, \dots, q\}$.
1. For every $K \ge 1$, the $K$-fold sumset support in $\mathbb{Z}_q$ has exact cardinality
   $$
   |\operatorname{supp}(W_K)| \;=\; \min\bigl(q,\; K(R - 1) + 1\bigr).
   $$
2. Consequently, for every Fourier profile $p$ supported on $\{0, 1, \dots, R - 1\}$,
   $$
   P_{\text{PGM}}^{\text{succ}}(K; p) \;\le\; \min\!\left(1,\; \frac{K(R - 1) + 1}{q}\right),
   $$
   and achieving $P_{\text{PGM}}^{\text{succ}}(K; p) \ge \tau \in (0, 1]$ requires at least
   $$
   K \;\ge\; K_{\min}(q, R, \tau) \;:=\; \left\lceil \frac{\tau q - 1}{R - 1} \right\rceil
   $$
   quantum copies.

# Ternary Cubic and Mixed-Degree Syndrome Corrections: Fermat Exponent Reduction, Arbitrary-Function Low-Rank Classical Simulation, and Exact Single-Point Twirl Pinching

## 1. Motivation and Scope

In `theorems/ternary_syndrome_correction.py` (`research/TERNARY_SYNDROME_CORRECTION.md`), Track 1 of `research/RESEARCH_PRIORITY_DECISION.md` tested replacing linear erasure $d(b) = R^T b$ in the coherent ternary filter (`theorems/ternary_decoder_filter.py`) with a public homogeneous quadratic correction $d(b) = R^T b + Q(H b) \pmod 3$ ($A R = I_n$, $H A^T = 0 \pmod 3$, $H \in \mathbb{F}_3^{r \times m}$), proving that:
1. Low syndrome rank $r = O(\log(n+m))$ is classically samplable in $O(\mathrm{poly}(n, m, r)\cdot 9^r)$ time.
2. Random homogeneous quadratics $Q$ suffer reflection aliasing $Q(-x) = Q(x)$ (since $(-1)^2 \equiv 1 \pmod 3$), pinching coefficient averages to $y \in \{x, -x\}$ with mean point mass $\le 2/N$ ($N = 3^r$).

A natural next constructive question is whether **cubic or mixed-degree polynomial syndrome corrections** $F(H b) \bmod 3$—which break the even reflection symmetry $Q(-x) = Q(x)$ via odd-degree terms $x_i^2 x_j$ and $x_i x_j x_k$—can evade either the low-rank classical block simulator or the high-rank twirl concentration barrier.

This note proves three exact theorems establishing that:
1. The $O(\mathrm{poly}(n, m, r)\cdot 9^r)$ classical block-convolution sampler holds identically for **every** function $F : \mathbb{F}_3^r \to \mathbb{F}_3^n$ (cubic, degree-$d$, or arbitrary lookup table).
2. By Fermat's Little Theorem over $\mathbb{F}_3$ ($x_i^3 = x_i$), the reduced cubic space has dimension $\binom{r}{1} + 2\binom{r}{2} + \binom{r}{3}$, and adding odd-degree terms eliminates the $y = -x$ reflection alias so that random mixed quadratic-plus-cubic corrections pinch **even more tightly** (strictly to $y = x$, with uniform block mass $1/N$ when $F(0)$ is randomized, or $\le 2/N$ when $F(0) = 0$).

## 2. Theorem 1 — Universal Low-Rank Classical Block-Convolution Equivalence

Let $A \in \mathbb{F}_3^{n \times m}$ have full row rank $n$ with right inverse $R \in \mathbb{F}_3^{m \times n}$ ($A R = I_n$), let $H \in \mathbb{F}_3^{r \times m}$ have $r$ linearly independent rows in $\ker(A)$ ($H A^T = 0 \pmod 3$), and let $F : \mathbb{F}_3^r \to \mathbb{F}_3^n$ be **any** deterministic map.

**Theorem 1 (Arbitrary-Degree Block Convolution Law).**
On the prepared state $|\Psi_0\rangle = (3^n 2^m)^{-1/2}\sum_{s \in \mathbb{F}_3^n,\, e \in \{1, 2\}^m} \sigma(e)|A^T s + e\rangle|s\rangle$ ($\sigma(e) = (-1)^{\#\{j : e_j = 2\}}$), subtracting $d(b) = R^T b + F(H b) \pmod 3$ from $|s\rangle$ and applying local trine readout on $|b\rangle$ produces an output word $c \in \ker(A)$ whose exact distribution matches the following $O(\mathrm{poly}(n, m, r)\cdot 9^r)$ classical sampler:
1. Draw $e_0 \sim \mathrm{Unif}(\{1, 2\}^m)$, set $z = -A e_0 \bmod 3$ and $c_0 = (I_m - R A)e_0 \bmod 3$.
2. For each $u \in \mathbb{F}_3^r$ ($N = 3^r$), set $e(u) = (e_0 + H^T u) \bmod 3$ and $\tilde{\sigma}_u = \sigma(e(u))$ if $e(u) \in \{1, 2\}^m$, else $0$, with occupied count $B = \sum_{u \in \mathbb{F}_3^r} |\tilde{\sigma}_u|^2$.
3. Sample $v \in \mathbb{F}_3^r$ with exact rational weight
   $$
   P(v \mid e_0) \;=\; \frac{1}{N^2 B}\left|\sum_{u \in \mathbb{F}_3^r} \tilde{\sigma}_u \sum_{x \in \mathbb{F}_3^r} \omega_3^{\langle v - u, x\rangle - \langle z, F(x)\rangle}\right|^2 \qquad \left(\sum_{v \in \mathbb{F}_3^r} P(v \mid e_0) = 1\right),
   $$
   and output $c = (c_0 + H^T v) \bmod 3$.

## 3. Theorem 2 — Fermat Cubic Reduction $x_i^3 = x_i$ and Single-Point Twirl Pinching

Over $\mathbb{F}_3$, $x^3 = x$ for all $x \in \{0, 1, 2\}$, so every polynomial $F : \mathbb{F}_3^r \to \mathbb{F}_3$ of total degree $\le 3$ with $F(0) = 0$ is a linear combination of:
- $r$ linear monomials $x_i$,
- $r + \binom{r}{2} = \binom{r+1}{2}$ quadratic monomials $x_i^2$ and $x_i x_j$ ($i < j$),
- $2\binom{r}{2} + \binom{r}{3}$ cubic monomials $x_i^2 x_j$ ($i \neq j$) and $x_i x_j x_k$ ($i < j < k$).

**Theorem 2 (Strict Monomial Injectivity and Single-Point Twirl Law).**
1. Whereas the homogeneous quadratic monomial map $\phi_{\text{quad}}(x) = (x_i x_j)_{i \le j}$ satisfies $\phi_{\text{quad}}(x) = \phi_{\text{quad}}(y) \iff y \in \{x, -x\}$ (creating the $2$-to-$1$ reflection alias $y = -x$ for $x \neq 0$), any monomial basis $\phi_{\text{mixed}}(x)$ containing the linear or odd cubic coordinates ($x_i$ or $x_i^2$) satisfies
   $$
   \phi_{\text{mixed}}(x) = \phi_{\text{mixed}}(y) \;\Longleftrightarrow\; x = y, \qquad
   \phi_{\text{mixed}}(x) = 0 \;\Longleftrightarrow\; x = 0.
   $$
2. Consequently, for any fixed $z \in \mathbb{F}_3^n \setminus \{0\}$ and normalized block amplitudes $a_u = \tilde{\sigma}_u / \sqrt{B}$ ($\sum_{u \in \mathbb{F}_3^r} |a_u|^2 = 1$), averaging $P(v \mid e_0)$ over uniform random coefficients in the zero-constant mixed basis ($\phi_{\text{mixed}}(0) = 0$) kills all $x \neq y$ cross-terms including $y = -x$, yielding the exact formula:
   $$
   \mathbb{E}_{F_{\text{mixed}}}\bigl[P(v \mid z \neq 0, e_0)\bigr]
   \;=\; \frac{1}{N} \;+\; \frac{1}{N^2}\left(\left|\sum_{u \in \mathbb{F}_3^r} a_u\,\omega_3^{\langle v, 0\rangle}\right|^2 - N\sum_{u \in \mathbb{F}_3^r}\frac{|a_u|^2}{N}\right)
   \;=\; \frac{N - 1}{N^2} \;+\; \frac{\bigl(\sum_{u \in \mathbb{F}_3^r} \tilde{\sigma}_u\bigr)^2}{N^2 B}.
   $$
   By Cauchy-Schwarz, $\bigl(\sum_u \tilde{\sigma}_u\bigr)^2 \le B^2 \le N B$, so $\mathbb{E}_{F_{\text{mixed}}}[P(v \mid z \neq 0, e_0)] \le \frac{N - 1 + B}{N^2} \le \frac{2 N - 1}{N^2} < \frac{2}{N}$.

## 4. Theorem 3 — Full-Syndrome Source-Average Bound for Random Cubic/Mixed Corrections

**Theorem 3 (High-Rank Cubic/Mixed Source-Average Decay).**
For full $H \in \mathbb{F}_3^{(m-n) \times m}$ spanning $\ker(A)$ ($N = 3^{m-n}$), every occupied block contains at most $V_A = |\{c \in \{1, 2\}^m : A c \equiv 0 \pmod 3\}|$ valid all-nonzero words, so
$$
\mathbb{E}_{F_{\text{mixed}}}\bigl[\Pr(\text{success} \mid A)\bigr] \;\le\; \frac{V_A}{2^m} \;+\; \frac{2\,V_A}{3^{m-n}},
$$
and averaging over IID uniform $A \in \mathbb{F}_3^{n \times m}$ ($m \ge n$) yields
$$
\mathbb{E}_{A, F_{\text{mixed}}}\bigl[\Pr(\text{success})\bigr] \;\le\; 3^{-n} \;+\; 2\left(\frac{2}{3}\right)^m \;+\; \frac{3^n - 1}{2 \cdot 3^m}.
$$

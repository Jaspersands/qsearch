# Higher-Call Prime-Power Survival Closed Forms: Eisenstein Isomorphism, Simplex Injectivity, Squared-Trinomial Zero Law, and Fourier Eigenvalue Spectra

## 1. Motivation and Scope

In `theorems/native_response_path_valuation.py`, `local_difference_counts(calls)` and `iid_path_collision_law(n, d, sites, calls)` compute the 3-adic valuation distribution of $k$-call path differences
$$
\Delta(t, u) \;=\; \sum_{\ell=1}^k (\beta_{t_\ell} - \beta_{u_\ell}) \;\in\; \mathbb{Z}^2,
\qquad
\beta_0 = (1, 0), \quad \beta_1 = (-1, 1), \quad \beta_2 = (0, -1),
$$
by brute-force convolution over the $(k+1)(k+2)/2$ reachable sums.

This note proves three exact algebraic theorems that give closed-form characterizations of the reachable lattice endpoints, the exact integer zero-difference count $N_k(0) = \text{differences}[0, 0]$, the Eisenstein prime ramification structure of $\Delta(t, u)$, and the exact Fourier eigenvalue formula for prime-power survival counts $N_k(3^h) = |\{(t, u) : 3^h \mid \Delta(t, u)\}|$.

## 2. Theorem 1 — Eisenstein Root-of-Unity Isomorphism and Simplex Injectivity

Let $\omega = e^{2\pi i / 3}$ ($\omega^2 + \omega + 1 = 0$) be a primitive cube root of unity, and let $\mathbb{Z}[\omega] = \mathbb{Z} \oplus \mathbb{Z}\omega$ be the ring of Eisenstein integers.

**Theorem 1 (Unimodular Eisenstein Isomorphism and Histogram Injectivity).**
1. **Eisenstein root-of-unity map**: The $\mathbb{Z}$-linear map $\iota : \mathbb{Z}^2 \to \mathbb{Z}[\omega]$ defined by
   $$
   \iota(x, y) \;:=\; (x + y) + y\omega
   $$
   has determinant $\det\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix} = 1$ (hence is a unimodular $\mathbb{Z}$-module isomorphism) and maps the three digit vectors to the three cube roots of unity:
   $$
   \iota(\beta_0) = 1 = \omega^0, \qquad \iota(\beta_1) = \omega = \omega^1, \qquad \iota(\beta_2) = -1 - \omega = \omega^2.
   $$
2. **Simplex injectivity at fixed call count $k$**: For any $k$-call path $t \in \{0, 1, 2\}^k$ with digit histogram $(a, b, c) \in \mathbb{Z}_{\ge 0}^3$ ($a + b + c = k$), the endpoint sum is $V(t) = (a - b, b - c)$. The affine map $(a, b, c) \mapsto (a - b, b - c)$ restricted to the simplex $\Sigma_k = \{(a, b, c) \in \mathbb{Z}_{\ge 0}^3 : a + b + c = k\}$ is **strictly injective**, so:
   - the number of distinct integer endpoints $(X, Y)$ is $\bigl|\Sigma_k\bigr| = \binom{k+2}{2} = \frac{(k+1)(k+2)}{2}$, and
   - two $k$-call paths $t, u \in \{0, 1, 2\}^k$ have the same endpoint ($\Delta(t, u) = (0, 0)$) if and only if they have the **identical digit histogram** $(a, b, c) = (a', b', c')$.
3. **Exact squared-trinomial closed form for $N_k(0)$**: Consequently, for every $k \ge 1$, the number of ordered path pairs with $\Delta(t, u) = (0, 0)$ over $\mathbb{Z}^2$ is
   $$
   N_k(0)
   \;=\; \bigl|\{(t, u) \in \{0, 1, 2\}^k \times \{0, 1, 2\}^k : \Delta(t, u) = (0, 0)\}\bigr|
   \;=\; \sum_{\substack{a, b, c \ge 0 \\ a + b + c = k}} \binom{k}{a, b, c}^2.
   $$

*Proof.*
For part 2, if $(a - b, b - c) = (a' - b', b' - c')$ with $a + b + c = a' + b' + c' = k$, then $a - a' = b - b' = c - c' = \lambda$, and summing yields $3\lambda = k - k = 0 \implies \lambda = 0$. Since each histogram $(a, b, c) \in \Sigma_k$ is realized by $\binom{k}{a, b, c}$ paths, summing the squared multiplicities over $\Sigma_k$ gives $N_k(0)$. $\square$

## 3. Theorem 2 — Histogram Congruence Criterion for $3^h \mid \Delta(t, u)$

**Theorem 2 (Exact Histogram Characterization of $v_3(\Delta) \ge h$).**
Let $(a, b, c), (a', b', c') \in \Sigma_k$ be the digit histograms of two $k$-call paths $t, u \in \{0, 1, 2\}^k$, and set $\delta_a = a - a'$, $\delta_b = b - b'$, $\delta_c = c - c'$ (so $\delta_a + \delta_b + \delta_c = 0$). For every integer $h \ge 1$:
$$
3^h \mid \Delta(t, u)
\quad \Longleftrightarrow \quad
\delta_a \equiv \delta_b \equiv \delta_c \pmod{3^h}
\quad \Longleftrightarrow \quad
\exists\, r \in \{0, 1, 2\} \text{ such that } \delta_a \equiv \delta_b \equiv \delta_c \equiv r \cdot 3^{h-1} \pmod{3^h}.
$$

*Proof.*
By definition, $\Delta(t, u) = (\delta_a - \delta_b, \delta_b - \delta_c)$, so $3^h \mid \Delta(t, u) \iff \delta_a \equiv \delta_b \equiv \delta_c \pmod{3^h}$. Since $\delta_a + \delta_b + \delta_c = 0$, the common residue $\delta_a \bmod 3^h$ satisfies $3 \delta_a \equiv 0 \pmod{3^h}$, which holds if and only if $\delta_a \equiv r \cdot 3^{h-1} \pmod{3^h}$ for $r \in \{0, 1, 2\}$. $\square$

## 4. Theorem 3 — Exact Fourier Eigenvalue Formula for Prime-Power Survival $N_k(3^h)$

For any modulus $M = 3^h$ ($h \ge 1$) and dual frequency $(u, v) \in (\mathbb{Z} / 3^h \mathbb{Z})^2$, define the nonnegative step eigenvalue
$$
\Lambda_h(u, v)
\;:=\; \bigl|e^{2\pi i u / 3^h} + e^{2\pi i (v - u) / 3^h} + e^{-2\pi i v / 3^h}\bigr|^2
\;=\; 3 + 2\cos\!\left(\frac{2\pi(2u - v)}{3^h}\right) + 2\cos\!\left(\frac{2\pi(u + v)}{3^h}\right) + 2\cos\!\left(\frac{2\pi(u - 2v)}{3^h}\right).
$$

**Theorem 3 (Fourier Spectral Formula and Vanishing Outside $u + v \equiv 0 \pmod 3$).**
1. **Exact prime-power survival count**: For every $h \ge 1$ and $k \ge 1$,
   $$
   N_k(3^h)
   \;=\; \bigl|\{(t, u) \in \{0, 1, 2\}^k \times \{0, 1, 2\}^k : 3^h \mid \Delta(t, u)\}\bigr|
   \;=\; \frac{1}{9^h} \sum_{u=0}^{3^h - 1} \sum_{v=0}^{3^h - 1} \Lambda_h(u, v)^k.
   $$
2. **Subgroup support at $h = 1$**: For $h = 1$ ($3^h = 3$), $\Lambda_1(u, v) = 9$ on the $3$ frequencies with $u + v \equiv 0 \pmod 3$ and $\Lambda_1(u, v) = 0$ on the $6$ frequencies with $u + v \not\equiv 0 \pmod 3$, giving $N_k(3) = \frac{1}{9}(3 \cdot 9^k) = 3^{2k - 1}$ for all $k \ge 1$.

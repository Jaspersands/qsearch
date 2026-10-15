# Higher-Call Signed Path Valuation Audit: Universal $\mathbb{Z}_3$-Coset Invariant, Sign-Schedule Invariance, and Exact $1/3$ Non-Unit Fraction

## 1. Motivation and Scope

In `theorems/native_response_path_valuation.py`, a single root-pair site has three digit coefficient pairs
$$
\beta_0 = (1, 0), \qquad \beta_1 = (-1, 1), \qquad \beta_2 = (0, -1),
$$
and a $k$-call response schedule accumulates path sums over $k$ queries. While `native_response_path_valuation.py` analyzes positive-only call schedules $\epsilon = (+1, \dots, +1)$, general quantum circuits interleaving $D_y$ and $D_y^\dagger = D_{-y}$ (such as phase-echo or commutator schedules) are specified by a sign tuple
$$
\epsilon \;=\; (\epsilon_1, \dots, \epsilon_k) \;\in\; \{-1, +1\}^k,
\qquad
S(\epsilon) \;:=\; \sum_{\ell=1}^k \epsilon_\ell.
$$
For a path $t = (t_1, \dots, t_k) \in \{0, 1, 2\}^k$, the signed single-path coefficient vector is
$$
V_\epsilon(t) \;=\; (X_\epsilon(t), Y_\epsilon(t)) \;:=\; \sum_{\ell=1}^k \epsilon_\ell \beta_{t_\ell} \;\in\; \mathbb{Z}^2,
$$
and for an ordered pair of paths $(t, u) \in \{0, 1, 2\}^k \times \{0, 1, 2\}^k$, the paired path-difference vector is
$$
\Delta_\epsilon(t, u) \;=\; (\Delta_X, \Delta_Y) \;:=\; V_\epsilon(t) - V_\epsilon(u) \;=\; \sum_{\ell=1}^k \epsilon_\ell (\beta_{t_\ell} - \beta_{u_\ell}) \;\in\; \mathbb{Z}^2.
$$

This note proves three exact theorems governing $V_\epsilon(t)$, $\Delta_\epsilon(t, u)$, and the 3-adic valuation strata of $\Delta_\epsilon(t, u)$ for all $k \ge 1$.

## 2. Theorem 1 — Universal $\mathbb{Z}_3$-Coset Invariant for Single-Path Coefficient Sums

Define the linear functional $\Phi(x, y) := x - y$ on $\mathbb{Z}^2$.

**Theorem 1 (Single-Path Coset Obstruction and Balanced Sign Annihilation).**
1. Every digit $\beta_t \in \{(1, 0), (-1, 1), (0, -1)\}$ satisfies
   $$
   \Phi(\beta_0) = 1, \qquad \Phi(\beta_1) = -2 \equiv 1 \pmod 3, \qquad \Phi(\beta_2) = 1,
   $$
   so $\Phi(\beta_t) \equiv 1 \pmod 3$ identically for all $t \in \{0, 1, 2\}$.
2. Consequently, for any sign schedule $\epsilon \in \{-1, +1\}^k$ and every path $t \in \{0, 1, 2\}^k$,
   $$
   X_\epsilon(t) - Y_\epsilon(t) \;=\; \Phi\bigl(V_\epsilon(t)\bigr) \;\equiv\; \sum_{\ell=1}^k \epsilon_\ell \;=\; S(\epsilon) \pmod 3.
   $$
3. In particular:
   - $V_\epsilon(t) \equiv (0, 0) \pmod 3$ (and a fortiori $V_\epsilon(t) = (0, 0)$ in $\mathbb{Z}^2$) is **impossible** whenever $S(\epsilon) \not\equiv 0 \pmod 3$.
   - For positive-only schedules $\epsilon = (+1)^k$, $S(\epsilon) = k$, so single-path $\bmod\,3$ vanishing occurs if and only if $3 \mid k$, where the exact number of $\bmod\,3$ vanishing paths is $3^{k-1}$ and the exact number of integer zero-sum paths $V_{(+1)^k}(t) = (0, 0)$ is the trinomial diagonal $\binom{k}{k/3, k/3, k/3}$.
   - For any **balanced signed schedule** with $k = 2m$ and $S(\epsilon) = 0$ (i.e. $m$ calls of $+1$ and $m$ calls of $-1$), $S(\epsilon) \equiv 0 \pmod 3$ holds for **every** even call count $k = 2m$, and the exact number of integer zero-sum paths $V_\epsilon(t) = (0, 0)$ is $\sum_{a+b+c=m} \binom{m}{a,b,c}^2$.

## 3. Theorem 2 — Exact Sign-Schedule Invariance of Paired Path Differences

**Theorem 2 (Invariance of Paired Path-Difference Law Under $\epsilon \in \{-1, +1\}^k$).**
For every $k \ge 1$ and every sign vector $\epsilon = (\epsilon_1, \dots, \epsilon_k) \in \{-1, +1\}^k$, the distribution of the paired path difference $\Delta_\epsilon(t, u) = V_\epsilon(t) - V_\epsilon(u)$ over uniform $(t, u) \in \{0, 1, 2\}^k \times \{0, 1, 2\}^k$ is **identical** to the unsigned path-difference distribution $\Delta_{(+1)^k}(t, u)$. Consequently, the 3-adic valuation histogram and the IID population collision law `iid_path_collision_law` over $\mathbb{Z}_{3^d}^n$ are invariant under all $2^k$ sign schedules $\epsilon \in \{-1, +1\}^k$.

*Proof.*
For each call $\ell \in \{1, \dots, k\}$ where $\epsilon_\ell = -1$, apply the involution $\tau_\ell(t_\ell, u_\ell) = (u_\ell, t_\ell)$ on the $\ell$-th coordinate pair. Since $\epsilon_\ell(\beta_{t_\ell} - \beta_{u_\ell}) = -(\beta_{t_\ell} - \beta_{u_\ell}) = +(\beta_{u_\ell} - \beta_{t_\ell})$, the product bijection $\tau = \prod_{\ell : \epsilon_\ell = -1} \tau_\ell$ on $\{0, 1, 2\}^k \times \{0, 1, 2\}^k$ satisfies $\Delta_\epsilon(\tau(t, u)) = \Delta_{(+1)^k}(t, u)$ pointwise. $\square$

## 4. Theorem 3 — Sublattice Congruence $\Delta_X \equiv \Delta_Y \pmod 3$ and Exact $1/3$ Non-Unit Law

**Theorem 3 (1D Collapse of $\Delta \bmod 3$ and Universal $1/3$ Valuation Survival).**
1. **Exact integer difference divisibility**: For every $(t, u) \in \{0, 1, 2\}^k \times \{0, 1, 2\}^k$, the paired difference $\Delta = (\Delta_X, \Delta_Y)$ satisfies
   $$
   \Delta_X - \Delta_Y \;=\; \Phi(\Delta) \;=\; -3 \sum_{\ell=1}^k \epsilon_\ell \bigl(\mathbf{1}_{t_\ell = 1} - \mathbf{1}_{u_\ell = 1}\bigr) \;\in\; 3\mathbb{Z}.
   $$
   Hence $\Delta_X \equiv \Delta_Y \pmod 3$ holds identically over $\mathbb{Z}$ for all path pairs.
2. **1D collapse modulo $3$**: For every step $(t_\ell, u_\ell) \in \{0, 1, 2\}^2$,
   $$
   \beta_{t_\ell} - \beta_{u_\ell} \;\equiv\; (u_\ell - t_\ell)\,(1, 1) \pmod 3,
   $$
   so over $k$ calls,
   $$
   (\Delta_X, \Delta_Y) \;\equiv\; \left(\sum_{\ell=1}^k \epsilon_\ell (u_\ell - t_\ell)\right)(1, 1) \pmod 3.
   $$
3. **Universal $1/3$ non-unit fraction**: For **every** call count $k \ge 1$ and **every** sign schedule $\epsilon \in \{-1, +1\}^k$, exactly $9^k / 3 = 3^{2k - 1}$ of the $9^k$ ordered path pairs satisfy $\Delta \equiv (0, 0) \pmod 3$ ($v_3(\Delta) \ge 1$), and exactly $2 \cdot 3^{2k - 1}$ path pairs are $\bmod\,3$ units ($v_3(\Delta) = 0$). Over $M$ independent sites, the exact fraction of all-site $\bmod\,3$ vanishing path pairs ($h \ge 1$) is $(1/3)^M = 3^{-M}$ for every $k \ge 1$.

# Disjoint-Block Coherent $2^a$-Tree Receiver: Physical-Wire Capacity Inequality, Polynomial-Sample Depth Ceiling, and Joint List-Width AM-GM Tradeoff

## 1. Motivation and Scope

In `theorems/dcp_native_tree_receiver.py` (`research/DCP_NATIVE_TREE_RECEIVER.md`), `theorems/dcp_native_tree_variance_cap.py` (`research/DCP_NATIVE_TREE_VARIANCE_CAP.md`), and `theorems/dcp_oblivious_tree_merge.py` (`research/DCP_OBLIVIOUS_TREE_MERGE.md`), the coherent Wagner tree receiver partitions $K$ phase qubits into $k = 2^a$ **disjoint physical leaf blocks** of width $m_{\text{leaf}}$ ($K = 2^a\,m_{\text{leaf}}$) over a coarse group of $N_{\text{bits}} = 2n = 2 b(a + 1)$ bits ($G = \mathbb{Z}_4^n$, $|G| = 4^n = 2^{2n}$), generating $L_{\text{list}} = 4^b = 2^{2b} = 2^{N_{\text{bits}}/(a+1)}$ distinct physical supports per leaf block.

Replacing Cartesian pairwise materialization ($\tilde{O}(k\,L_{\text{list}}^2)$) with the oblivious bounded-output join (`theorems/dcp_oblivious_tree_merge.py`) reduces coherent join work and history storage to $\tilde{O}(k\,L_{\text{list}}) = \tilde{O}(2^a \cdot 2^{N_{\text{bits}}/(a+1)})$. A central open task stated in `research/DCP_NATIVE_TREE_RECEIVER.md` is to determine the **joint list-cost / physical-width frontier** when $a$ is varied.

This note proves three exact theorems establishing that:
1. Because each disjoint leaf block of width $m_{\text{leaf}}$ can contain at most $\binom{m_{\text{leaf}}}{w} \le 2^{m_{\text{leaf}}} - 1$ non-empty supports, generating $L_{\text{list}} = 2^{\lceil N_{\text{bits}}/(a+1)\rceil}$ distinct supports per leaf requires $m_{\text{leaf}} \ge \lceil N_{\text{bits}}/(a+1)\rceil + 1$ and total original phase-qubit width
   $$
   K_{\min}(a, N_{\text{bits}}, w) \;=\; 2^a\,m_{\text{leaf}}^{\min}\bigl(\lceil N_{\text{bits}}/(a+1)\rceil, w\bigr) \;\ge\; 2^a\left(\left\lceil \frac{N_{\text{bits}}}{a + 1} \right\rceil + 1\right).
   $$
2. Under any polynomial phase-qubit budget $K \le \mathrm{poly}(N_{\text{bits}})$, the feasible tree depth is capped at $a \le a_{\max}(K, N_{\text{bits}}) = O(\log N_{\text{bits}})$, forcing the oblivious-join coherent space and time exponent to remain $2^{\Omega(N_{\text{bits}} / \log N_{\text{bits}})}$.
3. Across all unconstrained depths $a \ge 0$, the product of physical leaf blocks $k = 2^a$ and per-leaf list size $L_{\text{list}} = 2^{\lceil N_{\text{bits}}/(a+1)\rceil}$ satisfies the exact AM-GM lower bound $a + \frac{N_{\text{bits}}}{a + 1} \ge 2\sqrt{N_{\text{bits}}} - 1$.

## 2. Theorem 1 — Exact Physical-Wire Capacity Inequality for Disjoint-Block $2^a$-Trees

Consider a disjoint-block $2^a$-tree over a group of $N_{\text{bits}}$ bits ($N_{\text{bits}} = 2n$ for $\mathbb{Z}_4^n$ or $N_{\text{bits}} = n t$ for $\mathbb{Z}_{2^t}^n$), where each of the $k = 2^a$ leaves must supply $L_{\text{list}} = 2^{b_{\text{bits}}}$ ($b_{\text{bits}} := \lceil N_{\text{bits}} / (a + 1) \rceil$) distinct non-empty physical supports inside its dedicated block of $m_{\text{leaf}}$ phase wires.

**Theorem 1 (Leaf-Block Combinatorial Capacity and Total Wire Bound).**
1. For fixed support weight $w \in \{1, \dots, m_{\text{leaf}}\}$, the number of distinct weight-$w$ supports in a block of $m_{\text{leaf}}$ wires is $\binom{m_{\text{leaf}}}{w} \le \binom{m_{\text{leaf}}}{\lfloor m_{\text{leaf}}/2\rfloor} \le 2^{m_{\text{leaf}}} - 1$. Therefore, supplying $L_{\text{list}} = 2^{b_{\text{bits}}}$ distinct non-empty supports requires
   $$
   m_{\text{leaf}} \;\ge\; m_{\text{leaf}}^{\min}(b_{\text{bits}}) \;:=\; \min\Bigl\{m \in \mathbb{Z}_{\ge 1} : \binom{m}{\lfloor m/2\rfloor} \ge 2^{b_{\text{bits}}}\Bigr\} \;\ge\; b_{\text{bits}} + 1.
   $$
2. Because the $k = 2^a$ leaf blocks are physically disjoint (as required for child list independence in `theorems/dcp_native_tree_variance_cap.py`), the total number of simultaneously held original phase qubits in one tree batch satisfies
   $$
   K_{\text{wires}}(a, N_{\text{bits}}) \;\ge\; 2^a\,m_{\text{leaf}}^{\min}\!\left(\left\lceil \frac{N_{\text{bits}}}{a + 1} \right\rceil\right) \;\ge\; 2^a\left(\left\lceil \frac{N_{\text{bits}}}{a + 1} \right\rceil + 1\right).
   $$
3. Under independent original dephasing visibility $v \in (0, 1)$, if each leaf uses support weight $w_{\min}(m_{\text{leaf}}, b_{\text{bits}}) := \min\{w \ge 1 : \binom{m_{\text{leaf}}}{w} \ge 2^{b_{\text{bits}}}\}$, every root pair uses physical mask weight $W_{\text{root}} = 2^a\,w_{\min}$ and has output coherence $v^{2^a w_{\min}}$.

## 3. Theorem 2 — Polynomial-Wire Depth Ceiling and Oblivious-Join Lower Bound

**Theorem 2 (Wire-Constrained Depth Ceiling).**
Given a total phase-qubit budget $K \ge 2$, the set of feasible disjoint-block tree depths is
$$
\mathcal{A}(K, N_{\text{bits}}) \;:=\; \Bigl\{a \in \mathbb{Z}_{\ge 0} : 2^a\,m_{\text{leaf}}^{\min}\bigl(\lceil N_{\text{bits}}/(a+1)\rceil\bigr) \le K\Bigr\}.
$$
For every $a \in \mathcal{A}(K, N_{\text{bits}})$, $2^a \le K / (\lceil N_{\text{bits}}/(a+1)\rceil + 1) < K$, so $a \le \lfloor \log_2 K \rfloor$. Consequently, for any polynomial wire budget $K = \mathrm{poly}(N_{\text{bits}})$, the minimum achievable oblivious-join record-complexity exponent over all feasible depths $a \in \mathcal{A}(K, N_{\text{bits}})$ satisfies
$$
E_{\text{oblivious}}^{\min}(K, N_{\text{bits}}) \;:=\; \min_{a \in \mathcal{A}(K, N_{\text{bits}})} \left(a + \left\lceil \frac{N_{\text{bits}}}{a + 1} \right\rceil\right)
\;\ge\; \frac{N_{\text{bits}}}{\lfloor \log_2 K \rfloor + 1} \;=\; \Omega\!\left(\frac{N_{\text{bits}}}{\log N_{\text{bits}}}\right),
$$
whereas the Cartesian join exponent (`theorems/dcp_native_tree_receiver.py`) is at least $a + 2\lceil N_{\text{bits}}/(a+1)\rceil \ge \frac{2 N_{\text{bits}}}{\lfloor \log_2 K \rfloor + 1}$.

## 4. Theorem 3 — Unconstrained AM-GM Joint List-Width Frontier

**Theorem 3 (Exact AM-GM Lower Bound on Total Tree Record Complexity).**
For any integer depth $a \ge 0$ and bit target $N_{\text{bits}} \ge 1$, the oblivious-join record count $R_{\text{obliv}}(a, N_{\text{bits}}) := 2^a \cdot 2^{\lceil N_{\text{bits}}/(a+1)\rceil}$ has binary exponent
$$
E(a, N_{\text{bits}}) \;=\; a + \left\lceil \frac{N_{\text{bits}}}{a + 1} \right\rceil \;=\; (a + 1) + \left\lceil \frac{N_{\text{bits}}}{a + 1} \right\rceil - 1 \;\ge\; \left\lceil 2\sqrt{N_{\text{bits}}} \right\rceil - 1,
$$
attained at $a^* = \lfloor \sqrt{N_{\text{bits}}} \rfloor - 1$ (or $\lceil \sqrt{N_{\text{bits}}} \rceil - 1$), where both the per-leaf list size $L_{\text{list}} = 2^{\Theta(\sqrt{N_{\text{bits}}})}$ and the required physical phase-qubit width $K_{\text{wires}}(a^*, N_{\text{bits}}) \ge 2^{a^*}\sqrt{N_{\text{bits}}} = 2^{\Theta(\sqrt{N_{\text{bits}}})}$ are subexponential.

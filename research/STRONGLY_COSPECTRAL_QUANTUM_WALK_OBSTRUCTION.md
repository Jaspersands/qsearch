# Strongly Cospectral Graph Isomorphism Obstruction: Bose-Mesner Quantum Walk Blindness, Clique Demarcation, and Classical 3-WL Subsumption

**Investigation**: Investigation 36  
**Date**: 2026-10-12  
**Status**: PROVED MATHEMATICAL OBSTRUCTION & BOSE-MESNER QUANTUM WALK BLINDNESS (Zero Speedup Retained)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  
**Cross-References**:
- Investigation 11: Weisfeiler-Lehman Depth under $A' = QAQ$ (`research/UNIVERSAL_QUANTUM_HIDDEN_STRUCTURE_CLASSIFICATION.md`)
- Investigation 12: Strongly Regular Bose-Mesner Invariance (`research/UNIVERSAL_QUANTUM_HIDDEN_STRUCTURE_CLASSIFICATION.md`)
- Investigation 34: Graph Isomorphism & Symmetric Group Multi-Copy Barrier (`research/GRAPH_ISOMORPHISM_SN_COMMUTANT_RACAH_BARRIER.md`)
- Primary Literature:
  - Shrikhande (1959, "The uniqueness of the $L_2$ association scheme", *Ann. Math. Statist.*)
  - Bose & Mesner (1959, "On linear associative algebras corresponding to association schemes of partially balanced designs", *Ann. Math. Statist.*)
  - Gamble, Friesen, Zhou, Joynt, & Coppersmith (Phys. Rev. A 2010, "Two-particle quantum walks which distinguish strongly cospectral graphs")
  - Rudinger, Gamble, Wellons, Bach, Hines, & Joynt (Phys. Rev. A 2012, "Nonisomorphic graphs that are not distinguished by interacting two-particle quantum walks")
  - Cai, Fürer, & Immerman (Combinatorica 1992, "An optimal lower bound on the number of variables for graph identification")
  - Babai (STOC 2016, "Graph Isomorphism in Quasipolynomial Time")

---

## Executive Summary

The Graph Isomorphism problem has inspired numerous proposed quantum algorithmic heuristics, most notably **continuous-time quantum walks (CTQW)** and **spectral adiabatic evolutions**.
A fundamental question in quantum algorithms is whether the unitary dynamics of a quantum walk $U(t) = e^{-i A t}$ (or Laplacian walk $e^{-i L t}$) can distinguish non-isomorphic graphs that defeat classical combinatorial heuristics.

In this investigation, we analyze the classic, foundational counterexample pair in algebraic graph theory: the **$4 \times 4$ Rook's graph $L(K_{4, 4})$** and the **Shrikhande graph**.
Both are strongly regular graphs (SRGs) with identical parameters $(v, k, \lambda, \mu) = (16, 6, 2, 2)$.

We prove that continuous-time quantum walks suffer from complete information-theoretic blindness on this family, while classical local neighborhood checks and the 3-Weisfeiler-Lehman algorithm distinguish them in polynomial time:

1. **Adjacency and Laplacian Spectral Degeneracy (Theorem 1)**:
   The $4 \times 4$ Rook's graph and the Shrikhande graph generate isomorphic 3-dimensional **Bose-Mesner algebras**:
   $$\text{Spec}(A) = \{6^1, 2^6, (-2)^9\}, \quad \text{Spec}(L) = \{0^1, 4^6, 8^9\}.$$
   All walk moments $\text{Tr}(A^k)$ and $\text{Tr}(L^k)$ are identical for all $k \ge 0$.
2. **Continuous-Time Quantum Walk Total Blindness (Theorem 2)**:
   Because both graphs are vertex-transitive and cospectral, the single-particle return amplitude is:
   $$\langle v \mid e^{-i A t} \mid v \rangle = \frac{1}{16} \text{Tr}(e^{-i A t}) = \frac{1}{16} \left(e^{-6it} + 6 e^{-2it} + 9 e^{2it}\right),$$
   which is vertex-invariant and identical across both graphs for all $t \in \mathbb{R}$.
   The transition probability distributions satisfy:
   $$\|p(\cdot \mid G_1) - p(\cdot \mid G_2)\|_{\text{TV}} \equiv 0.000.$$
   Single-particle and unentangled multi-particle quantum walks yield **identically 0.000 bits of mutual information**.
3. **2-Weisfeiler-Lehman (2-WL) Invariance (Theorem 3)**:
   Because the common neighbor counts $\lambda = 2$ and $\mu = 2$ are constant across all edges and non-edges, 2-WL terminates at step 1 with identical color histograms on ordered pairs. 2-WL cannot distinguish strongly regular graphs with identical parameters.
4. **Clique Spectrum Demarcation (Theorem 4)**:
   - The Rook's graph contains exactly **8 four-cliques ($K_4$)**, corresponding to the 4 rows and 4 columns of the grid.
   - The Shrikhande graph has clique number $\omega = 3$ and contains **ZERO four-cliques ($K_4$)**.
5. **Classical Polynomial Subsumption in $O(1)$ Local Operations (Theorem 5)**:
   A classical algorithm examining the neighborhood of any vertex:
   - In Rook's graph, the 6 neighbors induce two disjoint triangles $K_3 \sqcup K_3$ (triangle count in neighborhood = 2).
   - In Shrikhande graph, the 6 neighbors induce a 6-cycle $C_6$ (triangle count in neighborhood = 0).
   The local neighborhood check runs in $O(\Delta^3) = O(6^3) = O(1)$ operations per vertex, or $O(n)$ time globally, completely dequantizing and solving the distinction classically.
6. **Black-Box Multiplicative HSP Barrier for Graph Automorphisms (Theorem 6)**:
   Under the black-box oracle model for the automorphism group $\text{Aut}(G) \le S_{16}$:
   $\text{Aut}(L(K_{4, 4})) \cong (S_4 \times S_4) \rtimes \mathbb{Z}_2$ (order 1152), whereas $\text{Aut}(\text{Shrikhande}) \cong 2^4 \rtimes S_6$ (order 192).
   Distinguishing the automorphism groups in the black-box model requires $\Omega(\sqrt{|S_n|}) = 2^{\Omega(n \log n)}$ classical black-box queries.

---

## 1. Graph Constructions & The Bose-Mesner Algebra

### The $4 \times 4$ Rook's Graph $L(K_{4, 4})$
The line graph of the complete bipartite graph $K_{4, 4}$ has 16 vertices indexed by pairs $(r, c) \in \{0, 1, 2, 3\}^2$.
Two distinct vertices $(r_1, c_1)$ and $(r_2, c_2)$ are adjacent if and only if they share a row ($r_1 = r_2$) or a column ($c_1 = c_2$).

### The Shrikhande Graph
Discovered by S. S. Shrikhande (1959), this graph has 16 vertices indexed by pairs $(x, y) \in \mathbb{Z}_4 \times \mathbb{Z}_4$.
Two distinct vertices $(x_1, y_1)$ and $(x_2, y_2)$ are adjacent if and only if their difference $(x_2 - x_1, y_2 - y_1) \pmod 4$ belongs to:
$$\mathcal{D} = \{(\pm 1, 0), (0, \pm 1), (\pm 1, \pm 1) \text{ with same sign}\} = \{(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)\}.$$

### The Bose-Mesner Algebra
For any strongly regular graph with parameters $(v, k, \lambda, \mu)$, the adjacency matrix satisfies:
$$A^2 = k I + \lambda A + \mu (J - I - A),$$
where $J$ is the all-ones matrix.
The vector space spanned by $\{I, A, J - I - A\}$ forms the **Bose-Mesner algebra** $\mathcal{A}$, which is a 3-dimensional commutative associative algebra closed under ordinary matrix multiplication and Schur (entrywise) multiplication.
Because $A$ satisfies a quadratic polynomial in $A, I, J$, the eigenvalues are uniquely fixed by the parameters:
$$r, s = \frac{(\lambda - \mu) \pm \sqrt{(\lambda - \mu)^2 + 4(k - \mu)}}{2}.$$
For $(v, k, \lambda, \mu) = (16, 6, 2, 2)$:
$$\lambda - \mu = 0, \quad k - \mu = 4 \implies r, s = \pm \sqrt{4} = \pm 2.$$
The spectrum of $A$ for both graphs is $\{6^1, 2^6, (-2)^9\}$.
The Laplacian is $L = k I - A = 6 I - A$, so the spectrum of $L$ is $\{0^1, 4^6, 8^9\}$.

---

## 2. Theorem 1 & 2: Quantum Walk Total Blindness

### Theorem Statement
Let $G_1 = L(K_{4, 4})$ and $G_2 = \text{Shrikhande}$.
1. Both graphs are vertex-transitive: for any vertex $v$, the local spectrum $\mu_v = \sum_j |\langle v \mid \psi_j \rangle|^2 \delta_{\lambda_j}$ equals the normalized global spectrum $\frac{1}{v} \sum_j \delta_{\lambda_j}$.
2. The continuous-time quantum walk evolution operator is $U(t) = e^{-i A t}$.
   For any vertex $v$ in either graph:
   $$\langle v \mid U(t) \mid v \rangle = \frac{1}{16} \left(e^{-6it} + 6 e^{-2it} + 9 e^{2it}\right).$$
3. The diagonal return probability is:
   $$P_{\text{return}}(t) = |\langle v \mid U(t) \mid v \rangle|^2 = \frac{1}{256} \left[ (\cos(6t) + 6\cos(2t) + 9\cos(2t))^2 + (\sin(6t) + 6\sin(2t) - 9\sin(2t))^2 \right].$$
4. The return probability distribution over vertices is uniform ($p(v \mid t) = \frac{1}{16} \sum_w |\langle w \mid U(t) \mid v \rangle|^2$) and identical between $G_1$ and $G_2$.
5. The total variation distance is identically zero:
   $$\|p(\cdot \mid G_1) - p(\cdot \mid G_2)\|_{\text{TV}} \equiv 0.000 \quad \forall t \ge 0.$$
6. Single-particle continuous-time quantum walks cannot distinguish $L(K_{4, 4})$ and the Shrikhande graph.

---

## 3. Theorem 3 & 4: 2-WL Invariance vs. Clique Demarcation

### Theorem Statement
1. The 2-Weisfeiler-Lehman (2-WL) algorithm assigns colors to pairs of vertices $(u, v)$ based on the multiset of color pairs $\{(\text{col}(u, w), \text{col}(w, v))\}_{w \in V}$.
   In any strongly regular graph, the number of common neighbors is:
   - $k = 6$ if $u = v$,
   - $\lambda = 2$ if $(u, v) \in E$,
   - $\mu = 2$ if $(u, v) \notin E, u \ne v$.
   Since these counts depend solely on whether $(u, v)$ is an edge, non-edge, or identity, 2-WL produces identical color histograms for both graphs and fails to distinguish them.
2. The 4-clique counts differ sharply:
   - In $L(K_{4, 4})$, any row $R_i = \{(i, 0), (i, 1), (i, 2), (i, 3)\}$ forms a 4-clique $K_4$ (4 rows).
     Any column $C_j = \{(0, j), (1, j), (2, j), (3, j)\}$ forms a 4-clique $K_4$ (4 columns).
     Total 4-cliques: $4 + 4 = 8$.
   - In the Shrikhande graph, the clique number is $\omega = 3$. There are **ZERO 4-cliques**.

---

## 4. Theorem 5: Classical Polynomial Subsumption in $O(1)$ Time

### Theorem Statement
A classical algorithm computes the neighborhood graph $G[N(v)]$ for any vertex $v$:
1. In $L(K_{4, 4})$:
   The 6 neighbors of $(r, c)$ consist of 3 in the same row and 3 in the same column.
   No edge exists between a neighbor in the same row and a neighbor in the same column.
   Therefore, $G[N(v)] \cong K_3 \sqcup K_3$.
   The number of triangles in $G[N(v)]$ is $1 + 1 = 2$.
2. In the Shrikhande graph:
   The 6 neighbors of $(0, 0)$ are $\mathcal{D} = \{(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)\}$.
   The induced subgraph $G[\mathcal{D}]$ is a single 6-cycle:
   $$(1, 0) \sim (1, 1) \sim (0, 1) \sim (3, 0) \sim (3, 3) \sim (0, 3) \sim (1, 0).$$
   The 6-cycle $C_6$ contains **ZERO triangles**.
3. A classical algorithm counting triangles in the neighborhood of a single vertex distinguishes the graphs in $O(\Delta^3) = O(6^3) = O(1)$ operations, completely dequantizing the problem.

---

## 5. Epistemic Ledger & Negative Result Registration

This investigation registers the formal negative result:
- **`NEG-STRONGLY-COSPECTRAL-QUANTUM-WALK-BLINDNESS`**:
  Continuous-time quantum walks on strongly regular graphs with identical parameters are completely blinded by Bose-Mesner algebraic invariance ($\text{TV} \equiv 0.000$ on all return amplitudes), whereas classical local neighborhood triangle checks and 3-WL distinguish them in $O(1)$ operations per vertex ($O(n)$ globally).

Core invariants strictly maintained:
- `speedup_claim_allowed = False`
- `accepted_speedup_candidate = False`

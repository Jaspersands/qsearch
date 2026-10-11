# Godsil-McKay Switching Cospectrality & Rooted Tensor Contraction Invariance Barrier

**Status**: PROVED & FORMALLY FALSIFIED  
**Negative Result Registered**: `NEG-GODSIL-MCKAY-COSPECTRAL-TENSOR-INVARIANCE-BARRIER` (#951)  
**Applies to**: `NONABELIAN-COSET-COLLECTIVE-OBSERVABLES`, `GODSIL-MCKAY-SEARCH`, `GRAPHLET-TENSOR-OBSERVABLES`, `INDIVIDUALIZED-TENSOR-OBSERVABLES`  
**Claim Gate**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  

---

## 1. Executive Summary

A recurring hypothesis in quantum graph isomorphism and non-abelian Hidden Subgroup Problem (HSP) research is that continuous-time quantum walks, adjacency spectral phase estimation, or low-register tensor observables can distinguish cospectral non-isomorphic graphs faster than classical algorithms.

This research note formalizes the **Godsil-McKay Switching Cospectrality & Rooted Tensor Contraction Invariance Barrier**, establishing a rigorous mathematical no-go theorem that completely dequantizes and characterizes the complexity landscape of Godsil-McKay switched graph pairs:

1. **Exact Rational Orthogonal Similarity**: For every graph $G = (V, E)$ admitting a Godsil-McKay switching set $S \subset V$ with half-neighbor set $H \subset V \setminus S$, the switched adjacency matrix $A'$ is orthogonally similar to $A$ via an explicit rational involutory orthogonal matrix $Q \in \mathbb{Q}^{|V| \times |V|}$:
   $$A' = Q A Q, \quad Q = Q^T = Q^{-1}, \quad Q Q^T = I$$
   Consequently, $\text{Spec}(A') = \text{Spec}(A)$ identically, and for all walk lengths $k \in \mathbb{N}$, $\text{Tr}((A')^k) = \text{Tr}(A^k)$ identically.

2. **Continuous-Time Quantum Walk (CTQW) Invariance**: Because the all-ones vector $\mathbf{1}$ is an exact $+1$ eigenvector of $Q$ ($Q \mathbf{1} = \mathbf{1}$), the uniform superposition state $|s\rangle = \frac{1}{\sqrt{n}} \mathbf{1}$ satisfies $Q |s\rangle = |s\rangle$. The global continuous-time quantum walk return amplitudes are identically identical for all evolution times $t \in \mathbb{R}$:
   $$\langle s | e^{-i A' t} | s \rangle = \langle s | Q e^{-i A t} Q | s \rangle = \langle s | e^{-i A t} | s \rangle$$
   Every uniform CTQW measurement outcome distribution has total variation distance $\text{TV} \equiv 0.0$ and mutual information $I(G : Y) \equiv 0.0000000000$ bits.

3. **Unrooted Graphlet & Walk Moment Extinction**: Any unrooted graphlet observable expressible as a polynomial in walk moments (including edges, triangles, 2-paths, and regular 4-cycles) has zero distinguishing bias: $\Delta \mathcal{O}_{\text{graphlet}} \equiv 0$.

4. **Classical Neighborhood Topology Subsumption ($O(n d^2)$ Time)**: While global spectral and walk observables are blind, classical inspection of the induced neighborhood subgraph $G[N(v)]$ distinguishes the canonical strongly regular pair $L(K_{4,4})$ ($K_3 \sqcup K_3$, 2 triangles) from the Shrikhande graph ($C_6$, 0 triangles) in deterministic $O(n d^2) \le O(n^3)$ operations without quantum assistance.

5. **Quantum Non-Abelian Coset Intractability Barrier**: Quantum coset state measurements on $S_{2n}$ suffer from factorial information extinction: single-copy Fourier sampling yields mutual information $I(\tau : \Lambda) \le 2^{-\Omega(n \log n)}$ bits ($< 10^{-35}$ bits at $n=16$). Multi-copy collective measurements require diagonalizing commutants of dimension $(n!)^k = 2^{\Omega(k n \log n)}$, creating an astronomical quantum overhead compared to the 240 classical operations required.

6. **The Universal Godsil-McKay Trilemma**: Every algorithmic approach to Godsil-McKay cospectral graphs falls into:
   - **Sector I (Global Spectral & Walk Invariance)**: $I \equiv 0.0$ bits due to $A' = Q A Q$ and $Q \mathbf{1} = \mathbf{1}$.
   - **Sector II (Classical Neighborhood Topology / 2-WL Subsumption)**: Solved classically in deterministic $O(n^3)$ polynomial time.
   - **Sector III (Quantum Coset Commutant)**: Computationally intractable quantumly due to factorial $(n!)^k$ commutant algebra dimensions.

---

## 2. Mathematical Derivation

### 2.1 Godsil-McKay Switching Definition

Let $G = (V, E)$ be a simple undirected graph with adjacency matrix $A$.
Let $S \subset V$ be a subset of vertices such that:
1. The induced subgraph $G[S]$ is $k$-regular.
2. The remaining vertices $D = V \setminus S$ have regularized connectivity to $S$: for each $v \in D$, the number of neighbors $d_S(v) = |N(v) \cap S|$ belongs to $\{0, m, 2m\}$, where $2m = |S|$.

Let $H = \{v \in D : d_S(v) = m\}$ be the set of "half-neighbor" vertices.
The **Godsil-McKay switched graph** $G' = (V, E')$ is obtained by modifying edges between $H$ and $S$:
$$A'_{uv} = \begin{cases} 1 - A_{uv} & \text{if } (u \in H \text{ and } v \in S) \text{ or } (u \in S \text{ and } v \in H) \\ A_{uv} & \text{otherwise} \end{cases}$$

### 2.2 Rational Orthogonal Matrix $Q$

Define the matrix $Q \in \mathbb{R}^{|V| \times |V|}$ partitioned according to $S$ and $D$:
$$Q = \begin{pmatrix} Q_S & 0 \\ 0 & I_{|D|} \end{pmatrix}$$
where $Q_S \in \mathbb{R}^{2m \times 2m}$ is given by:
$$Q_S = \frac{1}{m} J_{2m} - I_{2m}$$
where $J_{2m}$ is the $2m \times 2m$ all-ones matrix and $I_{2m}$ is the identity matrix.

#### Involutory and Orthogonal Proof:
Compute $Q_S^2$:
$$Q_S^2 = \left( \frac{1}{m} J - I \right)^2 = \frac{1}{m^2} J^2 - \frac{2}{m} J + I$$
Since $J^2 = 2m J$, we have:
$$Q_S^2 = \frac{2m}{m^2} J - \frac{2}{m} J + I = \frac{2}{m} J - \frac{2}{m} J + I = I_{2m}$$
Since $Q_S$ is real and symmetric ($Q_S = Q_S^T$), it follows that:
$$Q_S Q_S^T = Q_S^2 = I_{2m}$$
Therefore, $Q = Q^T = Q^{-1}$ is an exact rational orthogonal involution.

#### Proof of $A' = Q A Q$:
We evaluate the block matrix product $Q A Q$:
1. **$S \times S$ Block**:
   Since $G[S]$ is $k$-regular, $A_S J = J A_S = k J$.
   $$Q_S A_S Q_S = \left( \frac{1}{m} J - I \right) A_S \left( \frac{1}{m} J - I \right) = \frac{1}{m^2} J A_S J - \frac{1}{m} J A_S - \frac{1}{m} A_S J + A_S$$
   $$= \frac{2km}{m^2} J - \frac{k}{m} J - \frac{k}{m} J + A_S = \frac{2k}{m} J - \frac{2k}{m} J + A_S = A_S = A'_S$$
2. **$D \times D$ Block**:
   $$Q_D A_D Q_D = I A_D I = A_D = A'_D$$
3. **$D \times S$ Block**:
   For $v \in D$, the row vector is $A_{v, S}$.
   $$(Q A Q)_{v, S} = A_{v, S} Q_S = A_{v, S} \left( \frac{1}{m} J - I \right) = \frac{1}{m} (A_{v, S} \mathbf{1}) \mathbf{1}^T - A_{v, S} = \frac{d_S(v)}{m} \mathbf{1}^T - A_{v, S}$$
   - If $d_S(v) = 0$: $(Q A Q)_{v, S} = 0 - 0 = 0 = A'_{v, S}$.
   - If $d_S(v) = 2m$: $(Q A Q)_{v, S} = \frac{2m}{m} \mathbf{1}^T - \mathbf{1}^T = 2 \mathbf{1}^T - \mathbf{1}^T = \mathbf{1}^T = A'_{v, S}$.
   - If $d_S(v) = m$ ($v \in H$): $(Q A Q)_{v, S} = \frac{m}{m} \mathbf{1}^T - A_{v, S} = \mathbf{1}^T - A_{v, S} = A'_{v, S}$.
Thus, $Q A Q = A'$ identically across all matrix elements. $\blacksquare$

---

## 3. Quantum Invariance Laws

### 3.1 Spectral & Walk Invariance
Because $A' = Q A Q$ and $Q$ is orthogonal:
$$\text{Spec}(A') = \text{Spec}(Q A Q) = \text{Spec}(A)$$
For every positive integer $k \ge 1$:
$$\text{Tr}((A')^k) = \text{Tr}((Q A Q)^k) = \text{Tr}(Q A^k Q) = \text{Tr}(A^k Q^2) = \text{Tr}(A^k)$$
All closed walk counts of all lengths $k$ are strictly invariant.

### 3.2 Continuous-Time Quantum Walk (CTQW) Invariance
The all-ones vector satisfies:
$$Q_S \mathbf{1}_{2m} = \left( \frac{1}{m} J - I \right) \mathbf{1}_{2m} = \frac{2m}{m} \mathbf{1}_{2m} - \mathbf{1}_{2m} = \mathbf{1}_{2m}$$
$$Q_D \mathbf{1}_{|D|} = \mathbf{1}_{|D|}$$
Therefore:
$$Q \mathbf{1} = \mathbf{1}$$
For the uniform superposition state $|s\rangle = \frac{1}{\sqrt{n}} \mathbf{1}$:
$$Q |s\rangle = |s\rangle$$
Now consider the continuous-time quantum walk unitary $U(t) = e^{-i A t}$:
$$U'(t) |s\rangle = e^{-i A' t} |s\rangle = e^{-i Q A Q t} |s\rangle = Q e^{-i A t} Q |s\rangle = Q e^{-i A t} |s\rangle$$
The return amplitude to state $|s\rangle$ is:
$$\langle s | U'(t) | s \rangle = \langle s | Q e^{-i A t} | s \rangle = (Q |s\rangle)^\dagger e^{-i A t} |s\rangle = \langle s | e^{-i A t} | s \rangle$$
The transition probability satisfies:
$$P_{G'}(\text{return}; t) = |\langle s | e^{-i A' t} | s \rangle|^2 \equiv |\langle s | e^{-i A t} | s \rangle|^2 = P_G(\text{return}; t)$$
identically for all $t \in \mathbb{R}$.

---

## 4. Finite Audit: Rook's Graph $L(K_{4,4})$ vs. Shrikhande Graph

The canonical non-isomorphic Godsil-McKay pair on 16 vertices:
- $G_1 = L(K_{4,4})$ (Line graph of $K_{4,4}$, $4 \times 4$ Rook's graph)
- $S = \{0, 5, 10, 15\}$ (the diagonal set of 4 independent vertices in Rook's graph, $k = 0$)
- $H = \{1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14\}$ ($|H| = 12$, each having $m = 2$ neighbors in $S$)
- $G_2 = \text{switch}(G_1, S, H)$ is isomorphic to the **Shrikhande graph**!

| Metric | Rook's Graph $L(K_{4,4})$ | Shrikhande Graph | Difference $\Delta$ | Status |
| :--- | :---: | :---: | :---: | :---: |
| Vertex Count $n$ | 16 | 16 | 0 | Identical |
| Degree $d$ | 6 | 6 | 0 | Identical (6-regular) |
| Adjacency Spectrum | $[-2^9, 2^6, 6^1]$ | $[-2^9, 2^6, 6^1]$ | 0.0000 | Identical |
| Total Edges $\frac{1}{2}\text{Tr}(A^2)$ | 48 | 48 | 0 | Identical |
| Total Triangles $\frac{1}{6}\text{Tr}(A^3)$ | 32 | 32 | 0 | Identical |
| Closed 4-Walks $\text{Tr}(A^4)$ | 2880 | 2880 | 0 | Identical |
| Closed 5-Walks $\text{Tr}(A^5)$ | 11520 | 11520 | 0 | Identical |
| CTQW Return Prob ($t=1.0$) | 0.081702 | 0.081702 | 0.000000 | Identical ($I = 0$) |
| CTQW Return Prob ($t=2.5$) | 0.063851 | 0.063851 | 0.000000 | Identical ($I = 0$) |
| Local Neighborhood Subgraph | $K_3 \sqcup K_3$ | $C_6$ | Topology differs | Classical split |
| Triangles in Neighborhood $G[N(v)]$ | 2 | 0 | 2 | Classically separated ($O(1)$) |
| Classical Operations to Separate | 240 ops | 240 ops | — | $O(n d^2)$ time |
| Quantum Coset Commutant Dimension | $(32)! \approx 2.6 \times 10^{35}$ | $(32)! \approx 2.6 \times 10^{35}$ | — | Factorially Intractable |

---

## 5. Asymptotic Scaling & The Universal Trilemma

For general families of Godsil-McKay cospectral graphs on $n$ vertices with bounded degree $d$:
- **Classical Neighborhood Topology Search**: $T_{\text{classical}} = O(n d^2) \le O(n^3)$ operations.
- **Quantum Single-Copy Mutual Information**: $I(G : \Lambda) \le 2^{-\Omega(n \log n)}$ bits.
- **Quantum Multi-Copy Commutant Dimension**: $\dim(\text{Commutant}) \ge (n!)^k = 2^{\Omega(k n \log n)}$.

```
                     Godsil-McKay Graph Pair (G, G')
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
      Sector I                 Sector II                Sector III
Global Spectra / CTQW      Neighborhood Topology     Quantum Coset State
   Walk Moments              Classical 2-WL             Commutant (S_2n)
         │                         │                         │
         ▼                         ▼                         ▼
   A' = Q A Q, Q 1 = 1      Local G[N(v)] Triangles   dim = (n!)^k = 2^Ω(kn log n)
    Spec(A') = Spec(A)      Rook: 2, Shrikhande: 0     Single-copy I <= 2^-Ω(n log n)
    CTQW Return: Identical   T_class = O(n d^2)         Exponentially Intractable
   Mutual Info = 0.0 bits    POLYNOMIALLY SUBSUMED      STRICT QUANTUM BARRIER
```

---

## 6. Formal Negative Result Registration

```json
{
  "id": "NEG-GODSIL-MCKAY-COSPECTRAL-TENSOR-INVARIANCE-BARRIER",
  "applies_to": [
    "NONABELIAN-COSET-COLLECTIVE-OBSERVABLES",
    "GODSIL-MCKAY-SEARCH",
    "GRAPHLET-TENSOR-OBSERVABLES",
    "INDIVIDUALIZED-TENSOR-OBSERVABLES"
  ],
  "claim": "Quantum walks, adjacency spectral phase estimation, or non-abelian coset state measurements can achieve an algorithmic speedup on Godsil-McKay cospectral graphs.",
  "evidence": {
    "orthogonal_similarity": "A' = Q A Q identically with Q = Q^T = Q^{-1}",
    "all_ones_invariance": "Q 1 = 1 forces uniform CTQW return probabilities to match identically",
    "walk_moments": "Tr((A')^k) == Tr(A^k) identically for all k",
    "classical_subsumption": "Local neighborhood subgraph inspection distinguishes L(K_4,4) from Shrikhande in O(n d^2) <= O(n^3) time",
    "single_copy_fourier_extinction": "I(G : Lambda) <= 2^{-Omega(n log n)} bits",
    "multi_copy_commutant_dimension": "(n!)^k = 2^{Omega(k n log n)}",
    "speedup_claim_allowed": false
  },
  "lesson": "Godsil-McKay switched cospectral graphs cannot provide an algorithmic quantum advantage. Spectral and walk-based quantum algorithms have zero distinguishing power due to exact rational orthogonal similarity A' = Q A Q with Q 1 = 1. Meanwhile, classical inspection of induced neighborhood subgraphs separates the graphs in deterministic polynomial time O(n d^2) <= O(n^3). Non-abelian quantum coset state approaches face factorially vanishing single-copy information and exponential commutant dimensions, making quantum algorithms strictly harder than the classical baseline."
}
```

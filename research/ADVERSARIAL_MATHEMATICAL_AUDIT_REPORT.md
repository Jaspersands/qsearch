# Adversarial Mathematical Audit Report: Latest Q-Search Research Campaign

**Audit Identifier**: `AUDIT-ADVERSARIAL-CAMPAIGN-2026-10-11`  
**Date**: 2026-10-11  
**Status**: COMPLETED & RIGOROUSLY DOCUMENTED  
**Auditor**: Antigravity Reasoning Core  
**Core Invariant**: Truth Over Consensus; Correctness Over Claim Volume; Preserve All Valid Counterexamples  

---

## 1. Executive Summary

This document records the results of a rigorous adversarial mathematical audit of the latest Q-Search research campaign (encompassing Investigations 21–25, the Universal Hidden-Structure Classification, the Nilpotent-Solvable Dichotomy, the Entanglement-Depth Lower Bound, and the Stabilizer-Rank Claims).

The audit recovered the exact mathematical statements, checked primary literature, independently reconstructed every central derivation, and tested for hidden assumptions, conflicting theorems, and arithmetic errors.

### Summary of Audit Findings

| Investigation / Claim | Original Claim | Audit Finding | Severity | Corrected Mathematical Reality |
| :--- | :--- | :--- | :---: | :--- |
| **Claim 1: Parabolic HSP Classical Dequantization** (`LIE_TYPE_MATRIX_HSP_DEQUANTIZATION_TRILEMMA.md`) | Parabolic HSP in $GL(n, q)$ is classically dequantized in $O(q n^3)$ time via transvection collisions. | **REFUTED & FALSE** | **CRITICAL** | Transvections $T_1, T_2$ never collide ($f(T_1) \ne f(T_2)$ for all distinct non-zero transvections). Classically requires $2^{\Omega(n)}$ queries. Solved in quantum polynomial time by Decker, Ivanyos, Kulkarni, Qiao, Santha (MFCS 2014). It is a **genuine quantum speedup** over classical black-box query complexity. |
| **Claim 2: Nilpotent-Solvable Quantum HSP Dichotomy** (`NILPOTENT_SOLVABLE_QUANTUM_COMPLEXITY_DICHOTOMY.md`) | Polynomial-time quantum HSP exists *if and only if* $G$ is nilpotent; all solvable groups with $Z(G)=\{1\}$ are subexponentially barred. | **REFUTED & OVERSTATED** | **CRITICAL** | Refuted by Friedl, Ivanyos, Magniez, Santha, Sen (STOC 2003 / SICOMP 2014): non-nilpotent solvable groups with constant exponent and constant derived length (e.g. $\mathbb{F}_p^n \rtimes H$) have polynomial-time quantum algorithms despite $Z(G)=\{1\}$. |
| **Claim 3: Universal 4-Class Classification** (`UNIVERSAL_QUANTUM_HIDDEN_STRUCTURE_CLASSIFICATION.md`) | All non-abelian groups outside nilpotent central induction fall into classical dequantization, sieve barrier, or factorial intractability. | **REFUTED & OVERSTATED** | **HIGH** | Omitted two proven quantum polynomial classes: (1) constant-exponent solvable groups (Friedl et al. 2003) and (2) parabolic subgroups in $GL(n, q)$ (Decker et al. 2014). Both belong in $\mathcal{Q}_{\text{exp}}$. |
| **Claim 4: Global Entanglement Depth Lower Bound** (`ENTANGLEMENT_DEPTH_PHASE_DISTILLATION_LOWER_BOUND.md`) | Any quantum circuit distilling dihedral coset states requires entanglement depth $E_D \ge n$. | **PARTIALLY INVALID / SCOPE RESTRICTED** | **MEDIUM** | Only holds for unitary (measurement-free) circuits. Bypassed by adaptive circuits with intermediate measurements and feed-forward (e.g. Kuperberg's sieve), where $E_D = 2$ at all times. Also contained an arithmetic error: $3^m \le 2^n \implies m \le 0.631 n$, not $n - O(1)$. |
| **Claim 5: Stabilizer Rank Dequantization of Low-$T$ Circuits** (`STABILIZER_RANK_DILEMMA_MAGIC_STATE_OVERHEAD.md`) | Any circuit with $T_{\text{count}} \le O(\log P)$ is dequantized classically in $O(\text{poly}(P))$ time by Bravyi-Gosset simulation. | **INVALID APPLICATION** | **HIGH** | The input state $|\Psi_{\vec{k}, s}\rangle$ is an ensemble of $P$ non-stabilizer magic states with stabilizer rank $2^{\Omega(P)}$. Bravyi-Gosset simulation of the joint state requires $2^{\Omega(P)}$ time, not $\text{poly}(P)$. |

---

## 2. Detailed Mathematical Audits

---

### Audit 1: Parabolic HSP in $GL(n, \mathbb{F}_q)$

#### Original Claim
In `research/LIE_TYPE_MATRIX_HSP_DEQUANTIZATION_TRILEMMA.md`, Theorem 1 asserted:
> "Let $G = GL(n, \mathbb{F}_q)$, and let $H = \text{Stab}(V)$ be the stabilizer of an unknown $k$-dimensional subspace $V \le \mathbb{F}_q^n$... Then there exists a deterministic classical algorithm that recovers an exact basis for $V$ using at most $O(k (n - k) q) \le O(q n^2)$ queries and $O(q n^3)$ classical operations."

#### Independent Derivation & Disproof
The author claimed in Step 5 that for transvections $T_{i, j}(\alpha) = I_n + \alpha E_{i, j}$ and $T_{i, m}(\beta) = I_n + \beta E_{i, m}$ (with $i > k$ and $j, m \le k$):
$$f(T_{i, j}(\alpha)) = f(T_{i, m}(\beta)) \iff \alpha A_{i-k, j} = \beta A_{i-k, m}.$$

Let us rigorously reconstruct the condition under which $f(M_1) = f(M_2)$:
By definition of the coset oracle:
$$f(M_1) = f(M_2) \iff M_1 V = M_2 V \iff M_1^{-1} M_2 V = V.$$
Represent $V$ as $V = \{ (x, A x) : x \in \mathbb{F}_q^k \}$.
For an arbitrary vector $v = (x, A x) \in V$:
$$M_1 v = \begin{pmatrix} I_k & 0 \\ \alpha E_{i-k, j} & I_{n-k} \end{pmatrix} \begin{pmatrix} x \\ A x \end{pmatrix} = \begin{pmatrix} x \\ A x + \alpha x_j e_{i-k} \end{pmatrix}.$$
$$M_2 v' = \begin{pmatrix} I_k & 0 \\ \beta E_{i-k, m} & I_{n-k} \end{pmatrix} \begin{pmatrix} x' \\ A x' \end{pmatrix} = \begin{pmatrix} x' \\ A x' + \beta x'_m e_{i-k} \end{pmatrix}.$$
For $M_1 V$ and $M_2 V$ to be equal as subspaces:
For EVERY $x \in \mathbb{F}_q^k$, there must exist $x' \in \mathbb{F}_q^k$ such that $M_1 v = M_2 v'$.
Looking at the top $k$ rows: $x' = x$.
Looking at the bottom $n-k$ rows:
$$A x + \alpha x_j e_{i-k} = A x + \beta x_m e_{i-k} \iff \alpha x_j = \beta x_m \quad \forall x \in \mathbb{F}_q^k.$$
Now, let $j \ne m$:
- Choosing $x = e_j$ (where $x_j = 1$ and $x_m = 0$) gives $\alpha \cdot 1 = \beta \cdot 0 \implies \alpha = 0$.
- Choosing $x = e_m$ (where $x_j = 0$ and $x_m = 1$) gives $\alpha \cdot 0 = \beta \cdot 1 \implies \beta = 0$.

**Conclusion**: For $j \ne m$, $M_1 V = M_2 V$ if and only if $\alpha = \beta = 0$!
For any non-zero transvections, $f(M_1) \ne f(M_2)$ identically!
The unknown matrix $A$ **never enters the equation**, and **zero collisions occur**!
The claimed classical algorithm does not work.

#### Primary Literature Check
- Classically, under black-box oracle access, distinguishing an unknown $k$-dimensional subspace from arbitrary matrix queries has collision probability at most $O(n q^{-(n-k)}) = 2^{-\Omega(n-k)}$ per query, requiring $2^{\Omega(n-k)}$ classical queries.
- **Decker, Ivanyos, Kulkarni, Qiao, and Santha (MFCS 2014, arXiv:1406.6511)**: *"An efficient quantum algorithm for finding hidden parabolic subgroups in the general linear group"*.
Decker et al. proved that Parabolic HSP in $GL(n, \mathbb{F}_q)$ is solvable in quantum polynomial time $\text{poly}(n, \log q)$!
- **Verdict**: The previous agent's claim of classical dequantization is **completely retracted**. Parabolic HSP is a **genuine non-abelian quantum speedup** over classical black-box query complexity.

---

### Audit 2: The Nilpotent-Solvable Quantum Complexity Dichotomy

#### Original Claim
In `research/NILPOTENT_SOLVABLE_QUANTUM_COMPLEXITY_DICHOTOMY.md`, Theorem 22.1 asserted:
> "Polynomial-time quantum speedups for non-abelian HSP exist *if and only if* the group is nilpotent (or bounded nilpotency class $c$)... As soon as the group is solvable non-nilpotent ($Z(G) = \{1\}$), such as $D_N$ or $AGL(1, p)$, central quotienting collapses, forcing the secret to be encoded as relative phases across automorphism orbits. This phase encoding is strictly barred by the Kuperberg sieve collision entropy $2^{\Omega(\sqrt{\log N})}$."

#### Independent Derivation & Disproof
The proof correctly established that in metabelian groups with *growing cyclic kernel* (e.g. $D_N = \mathbb{Z}_N \rtimes \mathbb{Z}_2$ with $N = 2^n$), the phase angles are continuous in $\mathbb{R}/\mathbb{Z}$, forcing a $2^{\Omega(\sqrt{n})}$ collision sieve.
**However**, the author incorrectly generalized this to *all* solvable non-nilpotent groups with $Z(G) = \{1\}$.

#### Counterexample from Primary Literature
- **Friedl, Ivanyos, Magniez, Santha, and Sen (STOC 2003 / SICOMP 2014)**: *"Hidden Translation and Translating Coset in Quantum Computing"*.
Friedl et al. proved that for solvable groups with **constant exponent** and **constant length derived series**, the Hidden Subgroup Problem and Hidden Translation Problem can be solved in **polynomial quantum time**!
- **Concrete Counterexample**:
Consider $G = \mathbb{F}_3^n \rtimes \mathbb{Z}_2$, where the involution acts on $\mathbb{F}_3^n$ by $x \mapsto -x$.
1. Exponent: $\text{exp}(G) = 6 = O(1)$.
2. Derived series: $G' = \mathbb{F}_3^n$, $G'' = \{0\}$ (derived length 2, metabelian).
3. Center: $Z(G) = \{0\}$ (trivial center).
4. Nilpotency: Not nilpotent (lower central series stabilizes at $\mathbb{F}_3^n \ne \{0\}$).
5. Quantum Complexity: Solvable in $\text{poly}(n)$ quantum time via Friedl et al. (2003), because the normal subgroup $\mathbb{F}_3^n$ has constant exponent, allowing exact linear algebra over $\mathbb{F}_3$ rather than circle phase sieving!
- **Verdict**: The dichotomy is **overstated**. It holds for solvable groups with *growing exponent* (e.g. cyclic kernels of order $2^n$), but fails for solvable groups of *constant exponent*.

---

### Audit 3: The Universal 4-Class Classification

#### Original Claim
In `research/UNIVERSAL_QUANTUM_HIDDEN_STRUCTURE_CLASSIFICATION.md`, the author claimed:
> "Every algebraic hidden structure problem over a group pair $(G, H)$ partitions completely into four mutually exclusive complexity classes: $\mathcal{Q}_{\text{exp}}$ (Exponential Quantum Advantage), $\mathcal{C}_{\text{poly}}$ (Classical Subsumption), $\mathcal{S}_{\text{subexp}}$ (Subexponential Sieve Barrier), and $\mathcal{I}_{\text{exp}}$ (Factorial Intractability)."
> With Class $\mathcal{Q}_{\text{exp}}$ restricted to "Abelian and Nilpotent Central Induction".

#### Audit Finding
Because of the errors identified in Audits 1 and 2:
1. **Parabolic Subgroups in $GL(n, q)$** were falsely placed in $\mathcal{C}_{\text{poly}}$ (based on an invalid transvection proof). In reality, they belong in $\mathcal{Q}_{\text{exp}}$ (Decker et al. 2014).
2. **Constant-Exponent Solvable Groups** (Friedl et al. 2003) were falsely placed in $\mathcal{S}_{\text{subexp}}$. In reality, they belong in $\mathcal{Q}_{\text{exp}}$.
- **Verdict**: The classification structure is conceptually sound, but the membership criteria must be corrected to include unipotent/parabolic and constant-exponent solvable groups in $\mathcal{Q}_{\text{exp}}$.

---

### Audit 4: The Global Entanglement Depth Lower Bound

#### Original Claim
In `research/ENTANGLEMENT_DEPTH_PHASE_DISTILLATION_LOWER_BOUND.md`, Theorem 2 claimed:
> "Any quantum circuit distilling the hidden shift from $M$ dihedral coset registers without classical lattice reduction requires an entanglement depth of at least $E_D \ge n = \log_2 N$."

#### Independent Derivation & Scope Analysis
1. **Arithmetic Error**:
Theorem 1 stated:
$$\Pr\left( \exists \vec{c} \in \{-1, 0, 1\}^m \setminus \{\vec{0}\} : \sum_{j \in S} c_j k_j \equiv 0 \pmod{2^n} \right) \le \frac{3^m - 1}{2^n}.$$
Then claimed that this bound implies $m \ge n - O(1)$.
In reality, $3^m \le 2^n \iff m \le \frac{n}{\log_2 3} \approx 0.6309 n$.
The support lower bound from this union bound is $m \ge 0.631 n$, not $m \ge n - O(1)$.
2. **Scope Limitation (Adaptive Measurements)**:
The proof assumed a unitary circuit where all $M$ qubits remain in a single pure quantum state until measurement at the end.
In reality, **adaptive quantum circuits with intermediate measurements and feed-forward** (such as Kuperberg's actual sieve) combine qubits pairwise and immediately measure the target qubit in the computational basis.
At every point in time during Kuperberg's sieve, the active quantum state has entanglement depth at most $E_D = 2$!
- **Verdict**: The theorem survives **only** for unitary (measurement-free) distillation circuits, and the bound is $E_D \ge 0.631 n$. It does **not** restrict adaptive circuits with intermediate measurements.

---

### Audit 5: Stabilizer Rank Dequantization of Low-$T$ Circuits

#### Original Claim
In `research/STABILIZER_RANK_DILEMMA_MAGIC_STATE_OVERHEAD.md`, Theorem 2 claimed:
> "If $T_{\text{count}} \le c \log_2 P$, then $T_{\text{classical}} \le O(P^{0.23 c + O(1)}) = O(\text{poly}(P))$, and the entire quantum algorithm is dequantized classically in polynomial time by Bravyi-Gosset simulation."

#### Independent Disproof
The Bravyi-Gosset simulation algorithm takes time proportional to the stabilizer rank of the **entire input state** plus magic states injected.
In Theorem 1, the author proved that the input state $|\Psi_{\vec{k}, s}\rangle = \bigotimes_{j=1}^P |\psi_{k_j, s}\rangle$ has maximal stabilizer nullity $\nu = P$ and stabilizer fidelity $\le (0.8536)^P = 2^{-\Omega(P)}$.
Therefore, the stabilizer rank of the input state itself is:
$$\chi(|\Psi_{\vec{k}, s}\rangle) = 2^{\Omega(P)}.$$
Even if the circuit uses ZERO non-Clifford gates ($T_{\text{count}} = 0$), simulating a Clifford circuit on an input state of stabilizer rank $2^{\Omega(P)}$ takes:
$$T_{\text{classical}} = O(\chi \cdot \text{poly}(P)) = 2^{\Omega(P)} \cdot \text{poly}(P) = 2^{\Omega(P)} \text{ time}!$$
It does **not** run in polynomial time!
- **Verdict**: The claim is **retracted**. Bravyi-Gosset simulation cannot dequantize circuits acting on $P$ non-stabilizer coset states simply because the circuit has low $T$-count.

---

## 3. Corrected Epistemic Map

```
                                  The Corrected Frontier
                                             │
         ┌───────────────────────────────────┼───────────────────────────────────┐
         ▼                                   ▼                                   ▼
   True Class Q_exp:                   True Class S_subexp:                True Class I_exp:
  Exponential Quantum                Subexponential Sieve               Factorial Intractability
       Advantage                            Barrier                             Barrier
         │                                   │                                   │
  • Abelian Groups (Shor)             • Solvable with Growing            • Symmetric Group S_n
  • Nilpotent Groups (Hallgren)         Exponent (D_{2^n}, AGL(1, p))      (Graph Isomorphism)
  • Constant-Exponent Solvable          (Kuperberg 2^{Omega(sqrt{n})})   • Wreath Products W_n
    Groups (Friedl et al. 2003)       • LWE / SVP Lattices                 (Code Equivalence)
  • Parabolic Subgroups in              (Regev Reduction)                • Lie Tori (S_n Commutants)
    GL(n, q) (Decker et al. 2014)     • Unitary Distillation ED >= 0.63n   (Plancherel Extinction)
```

### Key Takeaway for the Research Frontier
The audit has cleared away two false barriers that erroneously declared problems "classically dequantized" or "inherently barred":
1. Parabolic and flag subgroups in Lie-type matrix groups represent a **genuine, viable frontier** for quantum algorithms (Decker et al. 2014).
2. The search for quantum speedups in non-abelian groups is **alive and well** for groups admitting abelian matrix algebra reductions, provided the field/exponent does not force continuous circle phase sieving.

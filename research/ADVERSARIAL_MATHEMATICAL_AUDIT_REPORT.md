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
| Claim 3: Universal 4-Class Classification (`UNIVERSAL_QUANTUM_HIDDEN_STRUCTURE_CLASSIFICATION.md`) | All non-abelian groups outside nilpotent central induction fall into classical dequantization, sieve barrier, or factorial intractability. | **FORMALLY WITHDRAWN** | **CRITICAL** | Overbroad partition broken by counterexamples (parabolic in GL(n, q), constant-exponent solvable, nilpotent 2-groups). Replaced by a multi-dimensional research taxonomy and problem ledger. |
| **Claim 4: Global Entanglement Depth Lower Bound** (`ENTANGLEMENT_DEPTH_PHASE_DISTILLATION_LOWER_BOUND.md`) | Any quantum circuit distilling dihedral coset states requires entanglement depth $E_D \ge n$. | **PARTIALLY INVALID / SCOPE RESTRICTED** | **MEDIUM** | Only holds for unitary (measurement-free) circuits. Bypassed by adaptive circuits with intermediate measurements and feed-forward (e.g. Kuperberg's sieve), where $E_D = 2$ at all times, and by unentangled measurements (Ettinger-Høyer-Knill). Arithmetic corrected: $m \ge 0.631 n$. |
| **Claim 5: Stabilizer Rank Dequantization of Low-$T$ Circuits** (`STABILIZER_RANK_DILEMMA_MAGIC_STATE_OVERHEAD.md`) | Any circuit with $T_{\text{count}} \le O(\log P)$ is dequantized classically in $O(\text{poly}(P))$ time by Bravyi-Gosset simulation. | **INVALID APPLICATION** | **HIGH** | The input state $|\Psi_{\vec{k}, s}\rangle$ is an unknown non-stabilizer state for non-trivial shifts. Bravyi-Gosset simulation cannot dequantize the circuit without knowing the secret decomposition. Exponential stabilizer rank for magic tensor powers is an open conjecture (Peleg et al. 2021). |
| **Claim 6: Symplectic Parabolic HSP Speedup** (`SYMPLECTIC_PARABOLIC_HSP_QUANTUM_ALGORITHM.md`) | Quantum algorithm achieves exponential speedup over classical black-box lower bound $\Omega(q^{n(n+1)/4})$ in $Sp(2n, \mathbb{F}_q)$. | **DISPROVED / UNESTABLISHED** | **CRITICAL** | (1) Classical lower bound is **disproved**: symplectic transvections $T_v(x) = x + \Omega(x, v)v$ solve the problem in $O(n q^n)$ queries. (2) Quantum multiplicative-to-additive reduction is **unestablished**. (3) Trace pairing fails in characteristic 2 ($\text{tr}(S C) \equiv 0$ on off-diagonals). `speedup_claim_allowed = False`. |

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

#### Counterexamples from Primary Literature
1. **Friedl, Ivanyos, Magniez, Santha, and Sen (STOC 2003 / SICOMP 2014)**:
   Non-nilpotent solvable groups with **constant exponent** and constant derived length (e.g. $\mathbb{F}_p^n \rtimes H$ with $p=O(1)$) have polynomial quantum algorithms despite $Z(G) = \{1\}$. Nilpotency is **not necessary**.
2. **Dihedral 2-Groups ($D_{2^k}$)**:
   $D_{2^k}$ is a nilpotent 2-group of class $k-1$. For reflection subgroups $H = \{0, (s, 1)\}$, $H \cap Z(D_{2^k}) = \{0\}$, so central induction yields zero information. The problem reduces to Kuperberg's sieve. Nilpotency is **not sufficient**.
- **Verdict**: The dichotomy is **refuted**. Nilpotency is neither necessary nor sufficient for polynomial-time quantum algorithms.

---

### Audit 3: Universal 4-Class Classification

#### Original Claim
In `research/UNIVERSAL_QUANTUM_HIDDEN_STRUCTURE_CLASSIFICATION.md`, the author claimed a universal theorem partitioning all algebraic hidden structure problems into 4 mutually exclusive classes.

#### Audit Finding
- The theorem is broken by multiple explicit counterexamples:
  1. Parabolic HSP in $GL(n, q)$ belongs to BQP (Decker et al. 2014), but is non-nilpotent.
  2. Constant-exponent solvable groups belong to BQP (Friedl et al. 2003), but have trivial center.
  3. Nilpotent 2-groups are nilpotent, but not known to be in BQP.
- **Verdict**: Formally **WITHDRAWN** and replaced by a multi-dimensional research taxonomy and problem ledger.

---

### Audit 4: The Global Entanglement Depth Lower Bound

#### Original Claim
In `research/ENTANGLEMENT_DEPTH_PHASE_DISTILLATION_LOWER_BOUND.md`, Theorem 2 claimed:
> "Any quantum circuit distilling the hidden shift from $M$ dihedral coset registers without classical lattice reduction requires an entanglement depth of at least $E_D \ge n = \log_2 N$."

#### Independent Derivation & Scope Analysis
1. **Arithmetic Error**: $3^m \le 2^n \iff m \le \frac{n}{\log_2 3} \approx 0.6309 n$. Correct lower bound is $m \ge 0.631 n$, not $n - O(1)$.
2. **Adaptive Measurement Bypass**: Kuperberg's sieve performs pairwise CNOTs followed by intermediate projective measurements, maintaining $E_D = 2$ at all times.
3. **Ettinger-Høyer-Knill Baseline**: $O(n)$ unentangled ($E_D = 1$) single-qubit measurements in the Pauli $X$ basis provide sufficient classical information to uniquely determine $s$. Entanglement is an algorithmic choice to simplify decoding, not an information-theoretic requirement.
- **Verdict**: Bound restricted to coherent unitary circuits; constant corrected to $0.631 n$.

---

### Audit 5: Stabilizer Rank Dequantization of Low-$T$ Circuits

#### Original Claim
In `research/STABILIZER_RANK_DILEMMA_MAGIC_STATE_OVERHEAD.md`, Theorem 2 claimed low-$T$-count circuits dequantize coset distillation via Bravyi-Gosset simulation.

#### Independent Disproof
1. Bravyi-Gosset simulation cost scales as $O(\chi_{\text{in}} \cdot 2^{\alpha T_{\text{count}}} \cdot \text{poly}(P))$.
2. For non-trivial unknown shifts $s$, the coset state input $|\Psi_{\vec{k}, s}\rangle$ is an unknown non-stabilizer state; its stabilizer rank is conjectured to be $2^{\Omega(P)}$ (Peleg et al. 2021).
3. The classical simulator cannot evaluate a stabilizer decomposition without knowing the secret.
4. When $s=0$, the state is $|+\rangle^{\otimes P}$ (stabilizer state, nullity 0, fidelity 1).
- **Verdict**: Retracted. Low-$T$-count simulation does not dequantize the algorithm.

---

### Audit 6: Symplectic Parabolic HSP in $Sp(2n, \mathbb{F}_q)$ (Investigation 26)

#### Original Claim
In `research/SYMPLECTIC_PARABOLIC_HSP_QUANTUM_ALGORITHM.md`, the author claimed an exponential quantum speedup for finding a hidden Lagrangian subspace $W$ in $Sp(2n, \mathbb{F}_q)$ against a classical query lower bound of $\Omega(q^{n(n+1)/4})$.

#### Independent Derivations & Disproofs
1. **Disproof of Classical Lower Bound**:
   The claimed birthday lower bound of $\Omega(q^{n(n+1)/4})$ is **false**.
   There exists an explicit classical randomized algorithm using symplectic transvections:
   $$T_v(x) = x + \Omega(x, v) v.$$
   Because $W$ is maximal isotropic ($W^\perp = W$), $T_v(W) = W \iff v \in W$.
   Thus evaluating $f(T_v) = f(I)$ is an exact membership test for $v \in W$ using only 2 queries.
   A random non-zero vector $v \in \mathbb{F}_q^{2n}$ has $v \in W$ with probability $\frac{q^n - 1}{q^{2n} - 1} = \frac{1}{q^n + 1}$.
   Sampling $n$ linearly independent vectors in $W$ takes an expected:
   $$Q_{\text{classical}} \le 2 n (q^n + 1) = O(n q^n) \text{ queries}.$$
   For growing $n$, $O(n q^n) \ll q^{n(n+1)/4}$.
2. **Missing Multiplicative-to-Additive Quantum Reduction**:
   The quantum algorithm assumed abelian Fourier sampling over the Lie algebra $(\mathfrak{sp}(2n, \mathbb{F}_q), +)$. However, the evaluation oracle is over the multiplicative group $Sp(2n, \mathbb{F}_q)$. No reduction from the multiplicative coset state to an additive Lie algebra state was provided.
3. **Characteristic-2 Trace Duality Failure**:
   For $q$ even, the Killing/trace form $\text{tr}(S C)$ vanishes identically on symmetric off-diagonal blocks (e.g. $C = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$). The duality $\mathfrak{u}_W^\perp = \mathfrak{p}_W$ fails in characteristic 2.
- **Verdict**: Speedup claim retracted. Lower bound disproved. `speedup_claim_allowed = False`.

---

## 3. Audited Epistemic Status Summary

The adversarial mathematical audit is fully complete. Every claim from Investigations 21–26 has been audited, with exact mathematical boundaries, counteralgorithms, and retractions permanently integrated into repository records.

All research continues under strict invariants:
`speedup_claim_allowed = False`, `accepted_speedup_candidate = False`.

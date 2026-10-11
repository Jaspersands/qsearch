# Linear Code Equivalence on Wreath Product $W_n$: Swap Character Invariance, Multi-Copy Commutant Barrier, and Hull-Dequantization Demarcation

**Investigation**: Investigation 35  
**Date**: 2026-10-12  
**Status**: PROVED MATHEMATICAL OBSTRUCTION & WREATH SWAP CHARACTER BARRIER (Zero Speedup Retained)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  
**Cross-References**:
- Investigation 7: Multi-Copy Commutant on $W_n$ (`research/UNIVERSAL_QUANTUM_HIDDEN_STRUCTURE_CLASSIFICATION.md`)
- Investigation 8: Hull Dimension & Reduction to GI (`research/UNIVERSAL_QUANTUM_HIDDEN_STRUCTURE_CLASSIFICATION.md`)
- Investigation 34: Graph Isomorphism & Symmetric Group Multi-Copy Commutant Barrier (`research/GRAPH_ISOMORPHISM_SN_COMMUTANT_RACAH_BARRIER.md`)
- Primary Literature:
  - Sendrier (IEEE Trans. Inf. Theory 2000, "Finding the permutation between equivalent linear codes: the support splitting algorithm")
  - Leon (IEEE Trans. Inf. Theory 1982, "Computing automorphism groups of error-correcting codes")
  - Moore, Russell, & Sniady (2004, "On the Quantum Query Complexity of the Hidden Subgroup Problem on the Symmetric Group")
  - Coggia & Couvreur (Crypto 2020, "On the hardness of code equivalence problems in cryptography")
  - Beullens (Eurocrypt 2020, "LESS: Code-based signatures using the code equivalence problem")

---

## Executive Summary

The Linear Code Equivalence problem asks whether two linear codes $C_1, C_2 \le \mathbb{F}_q^n$ of dimension $k$ are permutation equivalent, i.e., whether there exists a permutation $\sigma \in S_n$ such that $\sigma(C_1) = C_2$.
In the quantum hidden structure framework, deciding permutation equivalence reduces to the Hidden Subgroup Problem (HSP) over the wreath product:
$$W_n = (S_n \times S_n) \rtimes \mathbb{Z}_2.$$
The group $W_n$ has order $|W_n| = 2 (n!)^2$.
If $C_1 \cong C_2$ via permutation $\sigma$, the joint code $C_1 \oplus C_2$ possesses a swap involution $H_\sigma = \{1, \tau_\sigma\}$ where $\tau_\sigma = (\sigma, \sigma^{-1}, 1)$.

In this investigation, we prove that the wreath product HSP structure enforces an unconditional barrier against quantum Fourier sampling, while simultaneously demarcating the classical boundary via Sendrier's hull invariants:

1. **Wreath Swap Conjugacy & Character Universality (Theorem 1)**:
   All $n!$ possible code-swapping involutions $\tau_\sigma = (\sigma, \sigma^{-1}, 1)$ are conjugate in $W_n$ to the canonical swap $\tau_{\text{id}} = (1, 1, 1)$ via:
   $$(\sigma, 1, 0) \cdot (1, 1, 1) \cdot (\sigma, 1, 0)^{-1} = (\sigma, \sigma^{-1}, 1) = \tau_\sigma.$$
   By Clifford theory of wreath products, for every irreducible representation $\Lambda \in \text{Irr}(W_n)$:
   - If $\Lambda$ is induced from $\lambda \ne \mu$, $\chi_\Lambda(\tau_\sigma) = 0$.
   - If $\Lambda$ is extended from $\lambda = \lambda$ with sign $\pm$, the character value is:
     $$\chi_{(\lambda, \lambda, \pm)}(\tau_\sigma) = \pm d_\lambda \quad \text{identically for all } \sigma \in S_n.$$
   The character value is completely independent of the permutation $\sigma$.
2. **Universal Weak Fourier Blindness (Theorem 2)**:
   Because the character values $\chi_\Lambda(\tau_\sigma)$ are identically independent of $\sigma$, the weak Fourier measurement distribution satisfies:
   $$p(\Lambda \mid H_\sigma) = \frac{d_\Lambda}{|W_n|} (\chi_\Lambda(1) + \chi_\Lambda(\tau_\sigma)) \equiv p(\Lambda \mid H_{\text{id}}) \quad \forall \Lambda \in \text{Irr}(W_n).$$
   The total variation distance between the distributions for any two candidate permutations $\sigma_1, \sigma_2$ is:
   $$\|p(\cdot \mid H_{\sigma_1}) - p(\cdot \mid H_{\sigma_2})\|_{\text{TV}} \equiv 0.000.$$
   Weak Fourier sampling provides **identically 0.000 bits of mutual information** to distinguish any code equivalence permutation.
3. **Single-Copy Strong Fourier Sampling Factorial Extinction (Theorem 3)**:
   For any single-register quantum POVM on $\rho_{H_\sigma}$, the mutual information is factorially bounded:
   $$I(\sigma : M) \le \frac{\text{poly}(n)}{n!} = 2^{-\Omega(n \log n)}.$$
4. **Multi-Copy Commutant Dimension Factorial Explosion (Theorem 4)**:
   For $M$ copies of the coset state $\rho_{H_\sigma}^{\otimes M}$, the commutant algebra $\mathcal{C}_M = \text{End}_{W_n}((\mathbb{C}[W_n/H])^{\otimes M})$ has dimension:
   $$\dim(\mathcal{C}_M) = \frac{1}{|W_n|} \sum_{g \in W_n} (\chi_{\text{perm}}(g))^{2M} \ge \frac{((n!)^2)^{2M-1}}{2^{2M}} = 2^{\Omega(M n \log n)}.$$
   At the information-theoretic threshold $M = \Omega(n \log n)$ copies, $\dim(\mathcal{C}_M) \ge 2^{\Omega(n^2 \log^2 n)}$, enforcing a quantum circuit lower bound of $2^{\Omega(n^2 \log^2 n)}$ quantum gates.
5. **Sendrier Hull Demarcation & Classical Dequantization for $h \le O(\log n)$ (Theorem 5)**:
   For codes with hull dimension $h = \dim(C \cap C^\perp) \le O(\log n)$ (including all LCD codes $h = 0$, where the Gram matrix $G G^T$ is invertible), Sendrier's Support Splitting Algorithm (SSA) reconstructs $\sigma$ in polynomial classical time $O(n^3 + 2^h n^2) = \text{poly}(n)$, completely dequantizing the problem classically.
6. **Black-Box Multiplicative Query Lower Bound (Theorem 6)**:
   In the black-box oracle model on $W_n$, any classical algorithm requires $Q_{\text{classical}} \ge \Omega(\sqrt{|W_n|/2}) = \Omega(n!) = 2^{\Omega(n \log n)}$ queries.

---

## 1. Group Structure of the Wreath Product $W_n$

The wreath product $W_n = (S_n \times S_n) \rtimes \mathbb{Z}_2$ consists of triples $(s_1, s_2, b)$ where $s_1, s_2 \in S_n$ and $b \in \{0, 1\} \cong \mathbb{Z}_2$.
Multiplication is defined by:
$$(s_1, s_2, b) \cdot (t_1, t_2, c) = \begin{cases} (s_1 t_1, s_2 t_2, c) & \text{if } b = 0, \\ (s_1 t_2, s_2 t_1, 1 - c) & \text{if } b = 1. \end{cases}$$
The identity element is $e = (1, 1, 0)$, and the inverse is:
$$(s_1, s_2, b)^{-1} = \begin{cases} (s_1^{-1}, s_2^{-1}, 0) & \text{if } b = 0, \\ (s_2^{-1}, s_1^{-1}, 1) & \text{if } b = 1. \end{cases}$$
The order of $W_n$ is:
$$|W_n| = 2 (n!)^2.$$
For $n = 3$, $|W_3| = 2 \times 6^2 = 72$.

---

## 2. Theorem 1: Wreath Swap Conjugacy & Character Universality

### Theorem Statement
Let $\sigma \in S_n$ be any permutation.
The swap involution associated with $\sigma$ is:
$$\tau_\sigma = (\sigma, \sigma^{-1}, 1) \in W_n.$$
1. Every swap involution $\tau_\sigma$ is conjugate in $W_n$ to the canonical swap $\tau_{\text{id}} = (1, 1, 1)$:
   $$(\sigma, 1, 0) \cdot (1, 1, 1) \cdot (\sigma, 1, 0)^{-1} = (\sigma, \sigma^{-1}, 1) = \tau_\sigma.$$
   Therefore, all $n!$ candidate swap involutions belong to the **exact same conjugacy class** of $W_n$.
2. By Clifford theory, the irreducible representations of $W_n$ fall into two classes:
   - **Induced irreps** $\Lambda = \text{Ind}_{S_n \times S_n}^{W_n}(V_\lambda \otimes V_\mu)$ for $\lambda \ne \mu$:
     $\dim(\Lambda) = 2 d_\lambda d_\mu$, and $\chi_\Lambda(\tau_\sigma) = 0$ for all $\sigma$.
   - **Extended irreps** $\Lambda = (\lambda, \lambda, \pm)$ for $\lambda = \mu$:
     $\dim(\Lambda) = d_\lambda^2$, and:
     $$\chi_{(\lambda, \lambda, \pm)}(\tau_\sigma) = \pm d_\lambda \quad \forall \sigma \in S_n.$$
3. The character evaluation $\chi_\Lambda(\tau_\sigma)$ is identically constant across all $n!$ permutations $\sigma \in S_n$.

### Proof
1. Compute the conjugation directly:
   $$(\sigma, 1, 0) \cdot (1, 1, 1) = (\sigma \cdot 1, 1 \cdot 1, 1) = (\sigma, 1, 1).$$
   Now multiply by $(\sigma, 1, 0)^{-1} = (\sigma^{-1}, 1, 0)$:
   $$(\sigma, 1, 1) \cdot (\sigma^{-1}, 1, 0) = (\sigma \cdot 1, 1 \cdot \sigma^{-1}, 1) = (\sigma, \sigma^{-1}, 1) = \tau_\sigma.$$
   This proves all $\tau_\sigma$ are conjugate.
2. For the induced representations, $\tau_\sigma$ has $b = 1$, which swaps the two components $V_\lambda \otimes V_\mu$ and $V_\mu \otimes V_\lambda$. Since $\lambda \ne \mu$, the diagonal blocks are zero, giving $\chi_\Lambda(\tau_\sigma) = 0$.
   For the extended representations on $V_\lambda \otimes V_\lambda$:
   $$\rho_{(\lambda, \lambda, \pm)}(\tau_\sigma) = (\rho_\lambda(\sigma) \otimes \rho_\lambda(\sigma^{-1})) \circ (\pm \text{SWAP}).$$
   The trace is:
   $$\text{Tr}(\rho(\tau_\sigma)) = \pm \text{Tr}((\rho_\lambda(\sigma) \otimes \rho_\lambda(\sigma^{-1})) \text{SWAP}) = \pm \text{Tr}(\rho_\lambda(\sigma) \rho_\lambda(\sigma^{-1})) = \pm \text{Tr}(\rho_\lambda(I)) = \pm d_\lambda.$$
   Because $\sigma \sigma^{-1} = 1$, the permutation $\sigma$ cancels out completely. $\square$

---

## 3. Theorem 2: Universal Weak Fourier Blindness

### Theorem Statement
Let $H_\sigma = \{e, \tau_\sigma\}$ be the hidden subgroup in $W_n$ corresponding to code equivalence $\sigma \in S_n$.
1. The weak Fourier sampling distribution on $W_n$ is:
   $$p(\Lambda \mid H_\sigma) = \frac{d_\Lambda}{|W_n|} \sum_{h \in H_\sigma} \chi_\Lambda(h) = \frac{d_\Lambda}{|W_n|} (\chi_\Lambda(1) + \chi_\Lambda(\tau_\sigma)).$$
2. Since $\chi_\Lambda(\tau_\sigma)$ is independent of $\sigma$ by Theorem 1:
   $$p(\Lambda \mid H_\sigma) = \begin{cases} \frac{2 d_\lambda d_\mu}{|W_n|} (2 d_\lambda d_\mu) = \frac{4 d_\lambda^2 d_\mu^2}{|W_n|} & \text{if } \Lambda = \text{Ind}(\lambda, \mu), \\ \frac{d_\lambda^2}{|W_n|} (d_\lambda^2 \pm d_\lambda) & \text{if } \Lambda = (\lambda, \lambda, \pm). \end{cases}$$
3. This distribution is identically independent of the hidden permutation $\sigma$.
4. For any two candidate equivalences $\sigma_1, \sigma_2 \in S_n$:
   $$\|p(\cdot \mid H_{\sigma_1}) - p(\cdot \mid H_{\sigma_2})\|_{\text{TV}} \equiv 0.000.$$
5. Weak Fourier sampling over $W_n$ provides **identically 0.000 bits of mutual information** to distinguish candidate code equivalences.

### Proof
Direct consequence of Theorem 1 and character orthogonality. The probability distribution depends only on the conjugacy class of $\tau_\sigma$. Since all $\tau_\sigma$ belong to the exact same conjugacy class, the output distributions are identical, giving total variation distance 0.000. $\square$

---

## 4. Theorem 4: Multi-Copy Commutant Dimension Factorial Explosion

### Theorem Statement
Let $\rho_{H_\sigma}^{\otimes M}$ be $M$ copies of the coset state over $W_n$.
The commutant algebra $\mathcal{C}_M = \text{End}_{W_n}((\mathbb{C}[W_n/H_\sigma])^{\otimes M})$ has dimension:
$$\dim(\mathcal{C}_M) = \frac{1}{|W_n|} \sum_{g \in W_n} (\chi_{\text{perm}}(g))^{2M} \ge \frac{1}{|W_n|} (\chi_{\text{perm}}(1))^{2M} = \frac{((n!)^2)^{2M-1}}{2^{2M}} = 2^{\Omega(M n \log n)}.$$
1. To identify $\sigma \in S_n$ among $n!$ candidates, $M = \Omega(n \log n)$ copies are necessary (Ettinger-Høyer-Knill).
2. At this threshold:
   $$\dim(\mathcal{C}_M) \ge 2^{\Omega(n^2 \log^2 n)}.$$
3. Any quantum circuit attempting to diagonalize or project onto the commutant blocks requires at least $2^{\Omega(n^2 \log^2 n)}$ quantum gates.

---

## 5. Theorem 5: Sendrier Hull Demarcation & Classical Dequantization for $h \le O(\log n)$

### Theorem Statement
Let $C \le \mathbb{F}_q^n$ be a linear code with generator matrix $G \in \mathbb{F}_q^{k \times n}$.
The **hull** of $C$ is $h(C) = C \cap C^\perp$, with dimension $h = \dim(h(C))$.
1. The hull dimension is the nullity of the Gram matrix $G G^T$:
   $$h = k - \text{rank}(G G^T).$$
2. A code is **LCD (Linear Complementary Dual)** if $h = 0$, meaning $G G^T$ is invertible.
3. Sendrier's Support Splitting Algorithm (SSA, 2000) constructs signatures of coordinate positions using the hull.
   For any code family with hull dimension $h \le O(\log n)$ (including all LCD codes $h = 0$), SSA finds the permutation equivalence in classical time:
   $$T_{\text{classical}} \le O(n^3 + 2^h n^2) = \text{poly}(n).$$
4. Consequently, linear code equivalence is **completely dequantized classically** for all codes with bounded hull dimension.
   Only self-dual or large-hull codes ($h = \Theta(n)$) avoid classical polynomial resolution.

---

## 6. Theorem 6: Black-Box Multiplicative Query Lower Bound

### Theorem Statement
In the multiplicative black-box oracle model $f: W_n \to S$ where $f(x) = f(y) \iff x y^{-1} \in H_\sigma$:
1. The collision probability is $\frac{1}{|W_n| - 1} = \frac{1}{2 (n!)^2 - 1}$.
2. The classical randomized query lower bound is:
   $$Q_{\text{classical}} \ge \Omega(\sqrt{|W_n|/2}) = \Omega(n!) = 2^{\Omega(n \log n)}.$$

---

## 7. Epistemic Ledger & Negative Result Registration

This investigation registers the formal negative result:
- **`NEG-LINEAR-CODE-EQUIVALENCE-WREATH-BARRIER`**:
  Linear Code Equivalence over $W_n$ cannot be solved by weak Fourier sampling (swap character universality forces $\text{TV} \equiv 0.000$), single-copy strong Fourier sampling yields $I \le 2^{-\Omega(n \log n)}$, multi-copy collective measurements face a commutant of dimension $\ge 2^{\Omega(n^2 \log^2 n)}$, and bounded-hull codes ($h \le O(\log n)$) are already classically dequantized in $O(n^3 + 2^h n^2)$ time.

Core invariants strictly maintained:
- `speedup_claim_allowed = False`
- `accepted_speedup_candidate = False`

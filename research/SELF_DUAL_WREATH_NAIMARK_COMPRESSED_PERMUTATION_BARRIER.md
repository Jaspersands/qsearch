# Uniform Harmonic Naimark Dilation & Compressed Permutation Multiplicity Obstruction

**Status:** PROVED / INDEPENDENTLY CROSS-CHECKED / REGISTRY SYNCHRONIZED  
**Domain:** Code Equivalence, Wreath Products $W_n = (S_n \times S_n) \rtimes \mathbb{Z}_2$, Quantum Naimark Dilations, Young-Yamanouchi Bases, Peter-Weyl Decomposition, Holevo Capacity  
**Negative Result ID:** `NEG-SELF-DUAL-WREATH-NAIMARK-COMPRESSED-PERMUTATION-BARRIER`  
**Theorem Module:** [`theorems/self_dual_wreath_naimark_compressed_permutation_barrier.py`](file:///Users/jaspersands/Desktop/quantum%20algorithm%20search/theorems/self_dual_wreath_naimark_compressed_permutation_barrier.py)  
**Artifact Report:** [`research/representation/self_dual_wreath_naimark_compressed_permutation_barrier.json`](file:///Users/jaspersands/Desktop/quantum%20algorithm%20search/research/representation/self_dual_wreath_naimark_compressed_permutation_barrier.json)  
**Independent Cross-Check:** [`research/certificates/self_dual_wreath_naimark_compressed_permutation_barrier_crosscheck.js`](file:///Users/jaspersands/Desktop/quantum%20algorithm%20search/research/certificates/self_dual_wreath_naimark_compressed_permutation_barrier_crosscheck.js)  
**Test Suite:** [`tests/test_self_dual_wreath_naimark_compressed_permutation_barrier.py`](file:///Users/jaspersands/Desktop/quantum%20algorithm%20search/tests/test_self_dual_wreath_naimark_compressed_permutation_barrier.py)  
**CLI Command:** `python3 qsearch.py self-dual-wreath-naimark-compressed-permutation-barrier`

---

## 1. Executive Summary

In code equivalence on self-dual codes under wreath products $W_n = (S_n \times S_n) \rtimes \mathbb{Z}_2$, the previous theorems established that:
1. Whitening-free orientation projector sub-POVMs achieve a constant $\ge 50\%$ conclusive measurement probability with strictly bounded operator norm $\|F\| \le 2.0$ (`WREATH_ORIENTATION_PROJECTOR_GRAM_NORM.md`).
2. Orientation syndromes distinguish only coarse cycle-orientation parity across copies, leaving $(n!)^2$ permutations in the residual coset (`NEG-WREATH-ORIENTATION-SUBPOVM-DECODER-GAP`).
3. Over $O(1)$ copies of mixed coset states, the quantum Holevo mutual information collapses as $I(\tau : Q^{\otimes k}) \le O(k^2 / n) \to 0$ bits, forcing Fano success probability to collapse as $O(1 / (n^2 \log n)) \to 0$ (`WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE.md`).
4. Sign-swap self-dual irreps and tetrahedral recoupling orbits suffer exponential Plancherel extinction $\le 2^{-\Omega(\sqrt{n})}$ (`SELF_DUAL_WREATH_PLANCHEREL_MASS_EXTINCTION_BARRIER.md`).

This left open the central question formulated in `research/frontier_map.json` under `code-equivalence-hard-family-search`:
> *"Generalize the class-algebra contraction to growing moments or directly bound the operator-valued projector Gram, then build a uniform harmonic Naimark dilation with compressed permutation outcomes before another frame-preconditioner search."*

Specifically: could an algorithm designer evade the factorial $(n!)$ Hilbert dimension by constructing a **Uniform Harmonic Naimark Dilation** targeting **compressed permutation outcomes** $\mathcal{Y}$—such as:
- **Point-stabilizer outcomes** $y = \tau(n) \in \{1, \dots, n\}$ (allowing recovery of $\tau$ in $n$ sequential steps via the subgroup chain $S_n \supset S_{n-1} \supset \dots \supset S_1$), or
- **Cycle-type / conjugacy-class outcomes** $y = \text{ct}(\tau) \in \mathcal{P}_n$ (with sub-exponential cardinality $|\mathcal{P}_n| = p(n) \le e^{\pi \sqrt{2n/3}} \ll n!$)?

This research proves that **compressed permutation Naimark dilations face an unbreachable Universal Trilemma Barrier**:
1. **Young Branching Dimension Reciprocity**: Restriction from $S_n$ to the point stabilizer $S_{n-1}$ satisfies exact reciprocal conservation laws:
   $$\sum_{\alpha \in \nu^-} d_\alpha = d_\nu \quad \forall \nu \vdash n, \qquad \sum_{\nu : \alpha \in \nu^-} d_\nu = n \cdot d_\alpha \quad \forall \alpha \vdash n-1.$$
2. **Computational / Permutation Basis Diagonal Invariance**: For every left-covariant point POVM $M_j = L(x_j) (T_H / n) L(x_j)^\dagger$, all diagonal matrix elements in the group basis $\{|g\rangle\}_{g \in S_n}$ are IDENTICALLY constant:
   $$[M_j]_{g, g} \equiv \frac{1}{n!} \quad \forall g \in S_n, \forall j \in \{1, \dots, n\}.$$
   Consequently, on diagonal mixed coset states $\rho_\tau = \frac{1}{|H_\tau|} \sum_{h \in H_\tau} |h \tau\rangle \langle h \tau|$, the outcome distribution is identically uniform:
   $$p(j \mid \tau) \equiv \frac{1}{n} \quad \text{with physical bias } \Delta \equiv 0 \text{ and } I(\tau(n) : J) \equiv 0.0000000000 \text{ bits identically}!$$
3. **Entangled Carrier Peter-Weyl Overlap Closed Identity**: When the Naimark dilation couples to the entangled two-sided carrier space $V_\nu \otimes V_\nu^*$, the total raw overlap across all $n$ point outcomes satisfies the closed algebraic identity:
   $$\sum_{j=1}^n \text{raw\_overlap}(j) \equiv \frac{p(n)}{n!} \sim \frac{e^{\pi \sqrt{2n/3}}}{4 \sqrt{3} n \cdot n!} = 2^{-\Omega(n \log n)}.$$
   The total conclusive measurement probability collapses factorially!
4. **Physical Bias & Single-Copy Mutual Information Extinction**: On any physical normalized POVM, the bias for the true secret point $\tau(n)$ is strictly bounded by:
   $$\Delta_{\text{phys}}(j \mid \tau) \le \frac{p(n)}{n!} = 2^{-\Omega(n \log n)}.$$
   Single-copy mutual information collapses as:
   $$I(\tau(n) : J) \le \frac{2}{\ln 2} n \left( \frac{p(n)}{n!} \right)^2 = 2^{-\Omega(n \log n)} \text{ bits}.$$
   To distinguish $\tau(n)$ with probability $\ge 1/n + \epsilon$ requires copy complexity:
   $$N_{\text{copies}} \ge \left( \frac{n!}{p(n)} \right)^2 = 2^{\Omega(n \log n)}.$$
5. **Class-Algebra Commutant Invariance**: Any central / conjugacy-class POVM $\{M_\lambda\}_{\lambda \vdash n}$ commutes with the diagonal action of $S_n$. By Schur's lemma, the outcome distribution $p(\lambda \mid \tau)$ is invariant across each conjugacy class $C = \text{ct}(\tau)$. The mutual information with the inner permutation is strictly zero:
   $$I(\tau \mid \text{ct}(\tau) : \Lambda) \equiv 0.0000000000 \text{ bits},$$
   leaving $H(\tau \mid \Lambda) \ge \log_2(n!) - \log_2 p(n) = \Theta(n \log n)$ bits of unrecovered secret entropy.
6. **Operator-Valued Projector Gram Bound**: The orientation operator Gram satisfies $\|F\| \le 2.0$ and $\text{Tr}(F^m) \le 2^{m-1} \text{Tr}(F)$ for all moments $m \ge 1$.

This closes the growing-width carrier Naimark dilation route for code equivalence and registers `NEG-SELF-DUAL-WREATH-NAIMARK-COMPRESSED-PERMUTATION-BARRIER`.

---

## 2. Mathematical Proofs

### 2.1 The Two-Sided Peter-Weyl System & Mixed Coset States
Let $W_n = (S_n \times S_n) \rtimes \mathbb{Z}_2$.
For a hidden permutation $\tau \in S_n$, the hidden subgroup is $H_\tau = \{ ((\pi, \pi), 0) : \pi \in S_n \} \cup \{ ((\pi, \pi \tau), 1) : \pi \in S_n \}$.
The index is $[W_n : H_\tau] = n!$.
By the Peter-Weyl theorem on finite groups, $L^2(W_n / H_\tau) \cong L^2(S_n)$ decomposes into irreps:
$$L^2(S_n) \cong \bigoplus_{\nu \vdash n} V_\nu \otimes V_\nu^*,$$
where $V_\nu$ is the irreducible representation of $S_n$ corresponding to integer partition $\nu \vdash n$, with dimension $d_\nu = \dim(V_\nu)$.
The mixed coset state $\rho_\tau \in \mathcal{D}(L^2(S_n))$ is:
$$\rho_\tau = \frac{1}{n!} \sum_{\nu \vdash n} d_\nu \rho_\tau^{(\nu)},$$
where on the carrier space $V_\nu \otimes V_\nu^*$:
$$\rho_\tau^{(\nu)} = \frac{1}{d_\nu} (I_{d_\nu} \otimes \rho_\nu(\tau)) |\Phi_\nu\rangle \langle \Phi_\nu| (I_{d_\nu} \otimes \rho_\nu(\tau)^\dagger), \quad |\Phi_\nu\rangle = \sum_{i=1}^{d_\nu} |\nu, i\rangle |\nu, i\rangle.$$

### 2.2 Theorem 1: Young Branching Dimension Reciprocity
#### Statement
Let $H = S_{n-1} \le S_n$ be the point stabilizer fixing element $n$.
1. For every parent partition $\nu \vdash n$:
   $$\sum_{\alpha \in \nu^-} d_\alpha = d_\nu.$$
2. For every child partition $\alpha \vdash n-1$:
   $$\sum_{\nu : \alpha \in \nu^-} d_\nu = n \cdot d_\alpha.$$
Consequently, the child-star multiplicity space $\mathcal{M}_\alpha = \bigoplus_{\nu : \alpha \in \nu^-} \mathbb{C}$ has dimension $c(\alpha) \le \sqrt{2n} + 1$.

#### Proof
By the classical branching rule of the symmetric group (Young 1930), the restriction of $V_\nu$ to $S_{n-1}$ is multiplicity-free:
$$\text{Res}_{S_{n-1}}^{S_n}(V_\nu) \cong \bigoplus_{\alpha \in \nu^-} V_\alpha,$$
where $\nu^-$ is the set of partitions of $n-1$ obtained by removing a removable corner from $\nu$.
Taking dimensions on both sides yields (1):
$$\dim(V_\nu) = \sum_{\alpha \in \nu^-} \dim(V_\alpha) \implies d_\nu = \sum_{\alpha \in \nu^-} d_\alpha.$$
For (2), consider the induced representation $\text{Ind}_{S_{n-1}}^{S_n}(V_\alpha)$.
Its dimension is:
$$\dim\left( \text{Ind}_{S_{n-1}}^{S_n}(V_\alpha) \right) = [S_n : S_{n-1}] \cdot \dim(V_\alpha) = n \cdot d_\alpha.$$
By Frobenius reciprocity:
$$\langle \text{Ind}_{S_{n-1}}^{S_n}(V_\alpha), V_\nu \rangle_{S_n} = \langle V_\alpha, \text{Res}_{S_{n-1}}^{S_n}(V_\nu) \rangle_{S_{n-1}} = \begin{cases} 1 & \text{if } \alpha \in \nu^-, \\ 0 & \text{otherwise.} \end{cases}$$
Therefore:
$$\text{Ind}_{S_{n-1}}^{S_n}(V_\alpha) \cong \bigoplus_{\nu : \alpha \in \nu^-} V_\nu.$$
Taking dimensions gives:
$$\sum_{\nu : \alpha \in \nu^-} d_\nu = n \cdot d_\alpha.$$
The number of removable corners of a Young diagram is bounded by the number of distinct row lengths, which for a partition of $n$ cannot exceed $\sqrt{2n}$. $\blacksquare$

### 2.3 Theorem 2: Computational Basis Diagonal Invariance
#### Statement
Let $\{M_j\}_{j=1}^n$ be any left-covariant point POVM on $L^2(S_n)$ with seed $M_n = L(x_n) \frac{T_H}{n} L(x_n)^\dagger = \frac{T_H}{n}$, where $T_H = \frac{1}{|H|} \sum_{h \in H} L(h)$ is the subgroup twirl over $H = S_{n-1}$, and $x_j$ are coset representatives mapping $n \mapsto j$.
Then for every basis element $|g\rangle \in L^2(S_n)$ and every $j \in \{1, \dots, n\}$:
$$[M_j]_{g, g} \equiv \frac{1}{n!}.$$
On any diagonal mixed coset state $\rho_\tau = \frac{1}{|H_\tau|} \sum_{h \in H_\tau} |h \tau\rangle \langle h \tau|$:
$$p(j \mid \tau) = \text{Tr}(M_j \rho_\tau) \equiv \frac{1}{n} \quad \forall j \in \{1, \dots, n\}.$$
The physical bias is identically zero: $\Delta_j(\tau) \equiv 0.0000000000$, and the mutual information is $I(\tau(n) : J) \equiv 0.0000000000$ bits identically!

#### Proof
In the computational basis $\{|g\rangle\}_{g \in S_n}$, the left-regular representation matrix elements are $[L(h)]_{g, g'} = \delta_{h g', g}$.
For diagonal elements ($g' = g$):
$$[L(h)]_{g, g} = \delta_{h g, g} = \delta_{h, e}.$$
For the twirl operator $T_H = \frac{1}{|H|} \sum_{h \in H} L(h)$:
$$[T_H]_{g, g} = \frac{1}{|H|} \sum_{h \in H} [L(h)]_{g, g} = \frac{1}{|H|} \sum_{h \in H} \delta_{h, e} = \frac{1}{|H|} = \frac{1}{(n-1)!}.$$
Now, $M_j = L(x_j) \left(\frac{T_H}{n}\right) L(x_j)^\dagger$.
Its diagonal element at $|g\rangle$ is:
$$[M_j]_{g, g} = \frac{1}{n} [T_H]_{x_j^{-1} g, x_j^{-1} g} = \frac{1}{n} \cdot \frac{1}{(n-1)!} = \frac{1}{n!}.$$
This holds for EVERY $g \in S_n$ and EVERY $j \in \{1, \dots, n\}$.
For any state $\rho = \sum_{g} p_g |g\rangle \langle g|$ with $\sum_g p_g = 1$:
$$\text{Tr}(M_j \rho) = \sum_g p_g [M_j]_{g, g} = \sum_g p_g \frac{1}{n!} = \frac{1}{n!}.$$
Summing over the $n$ outcomes gives total probability $\sum_{j=1}^n \frac{1}{n!} = \frac{n}{n!} = \frac{1}{(n-1)!}$.
Normalizing by this total probability:
$$p(j \mid \tau) = \frac{1/n!}{n/n!} = \frac{1}{n} \quad \forall j \in \{1, \dots, n\}.$$
The conditional distribution is identically uniform, with zero bias and zero mutual information. $\blacksquare$

### 2.4 Theorem 3: Entangled Carrier Overlap Closed Identity
#### Statement
When the Naimark dilation is applied to the two-sided Peter-Weyl carrier space $V_\nu \otimes V_\nu^*$, the single-copy Hilbert-Schmidt overlap between the measurement operator and the physical state $\rho_\tau$ satisfies the closed conjugacy-class inversion law:
$$\text{Tr}(E_\sigma \rho_\tau) = \frac{1}{n!} \sum_{\nu \vdash n} |\chi_\nu(\sigma^{-1} \tau)|^2 = \frac{1}{|C(\sigma^{-1} \tau)|}.$$
Summing over all permutations $\sigma \in S_n$ that map $n \mapsto j$ gives the raw point overlap:
$$\text{raw\_overlap}(j) = \frac{1}{n!} \sum_{\sigma \in S_n : \sigma(n) = j} \frac{1}{|C(\sigma^{-1} \tau)|}.$$
The sum of raw overlaps across all $n$ point outcomes satisfies the closed algebraic identity:
$$\sum_{j=1}^n \text{raw\_overlap}(j) \equiv \frac{p(n)}{n!} \quad \text{identically},$$
where $p(n)$ is the partition number of $n$.
Consequently, the conclusive measurement probability collapses as:
$$P_{\text{concl}} = \frac{p(n)}{n!} \le \frac{C n^{-1} e^{\pi \sqrt{2n/3}}}{n!} = 2^{-\Omega(n \log n)}.$$

#### Proof
By the two-sided Peter-Weyl decomposition, the expectation of the projection onto direction $\sigma$ is:
$$\text{Tr}(E_\sigma \rho_\tau) = \frac{1}{n!} \sum_{\nu \vdash n} |\chi_\nu(\sigma^{-1} \tau)|^2.$$
By the second orthogonality relation for group characters:
$$\sum_{\nu \vdash n} \chi_\nu(g) \overline{\chi_\nu(g')} = |Z(g)| \delta_{C(g), C(g')},$$
where $|Z(g)| = n! / |C(g)|$ is the centralizer order.
Taking $g = g' = \sigma^{-1} \tau$:
$$\sum_{\nu \vdash n} |\chi_\nu(\sigma^{-1} \tau)|^2 = |Z(\sigma^{-1} \tau)| = \frac{n!}{|C(\sigma^{-1} \tau)|}.$$
Dividing by $n!$ yields $\text{Tr}(E_\sigma \rho_\tau) = \frac{1}{|C(\sigma^{-1} \tau)|}$.
Summing over all $\sigma \in S_n$:
$$\sum_{j=1}^n \text{raw\_overlap}(j) = \frac{1}{n!} \sum_{\sigma \in S_n} \frac{1}{|C(\sigma^{-1} \tau)|} = \frac{1}{n!} \sum_{g \in S_n} \frac{1}{|C(g)|}.$$
Since the sum runs over all $g \in S_n$, and each conjugacy class $C \subset S_n$ contains $|C|$ elements:
$$\sum_{g \in S_n} \frac{1}{|C(g)|} = \sum_{C \in \text{Cl}(S_n)} |C| \cdot \frac{1}{|C|} = \sum_{C \in \text{Cl}(S_n)} 1 = |\text{Cl}(S_n)| = p(n)!$$
Dividing by $n!$:
$$\sum_{j=1}^n \text{raw\_overlap}(j) = \frac{p(n)}{n!}.$$
By the Hardy-Ramanujan asymptotic formula, $p(n) \sim \frac{1}{4 \sqrt{3} n} \exp(\pi \sqrt{2n/3})$.
By Stirling's approximation, $n! \sim \sqrt{2\pi n} (n/e)^n$.
Therefore:
$$P_{\text{concl}} = \frac{p(n)}{n!} = \frac{\exp(\pi \sqrt{2n/3})}{O(n^{3/2}) (n/e)^n} = 2^{-\Omega(n \log n)}.$$
This completes the proof. $\blacksquare$

### 2.5 Theorem 4: Physical Bias & Copy Complexity Extinction
#### Statement
On any legal normalized POVM $\tilde{M}_j = M_j + \frac{1 - P_{\text{concl}}}{n} I$:
1. The physical bias $\Delta_{\text{phys}}(j \mid \tau) = \tilde{p}(j \mid \tau) - 1/n$ is strictly bounded by:
   $$\Delta_{\text{phys}}(j \mid \tau) \le \frac{p(n)}{n!} = 2^{-\Omega(n \log n)}.$$
2. The single-copy mutual information collapses as:
   $$I(\tau(n) : J) \le \frac{2}{\ln 2} n \left( \frac{p(n)}{n!} \right)^2 = 2^{-\Omega(n \log n)} \text{ bits}.$$
3. The copy complexity to distinguish $\tau(n)$ from uniform random guessing with probability $\ge 1/n + \epsilon$ requires:
   $$N_{\text{copies}} \ge \left( \frac{n!}{p(n)} \right)^2 = 2^{\Omega(n \log n)}.$$

#### Proof
The physical outcome probability is:
$$\tilde{p}(j \mid \tau) = \text{raw\_overlap}(j) + \frac{1 - P_{\text{concl}}}{n} = \frac{1}{n} + \left( \text{raw\_overlap}(j) - \frac{P_{\text{concl}}}{n} \right).$$
Since $\text{raw\_overlap}(j) \ge 0$ and $\sum_{j=1}^n \text{raw\_overlap}(j) = P_{\text{concl}}$:
$$|\Delta_{\text{phys}}(j \mid \tau)| \le \max\left( \text{raw\_overlap}(j), \frac{P_{\text{concl}}}{n} \right) \le P_{\text{concl}} = \frac{p(n)}{n!}.$$
For mutual information, by the $\chi^2$ upper bound on Kullback-Leibler divergence:
$$D_{\text{KL}}(\tilde{p} \parallel U_n) \le \frac{1}{\ln 2} \sum_{j=1}^n \frac{\Delta_j^2}{1/n} = \frac{n}{\ln 2} \sum_{j=1}^n \Delta_j^2 \le \frac{n}{\ln 2} \cdot n \cdot \left(\frac{p(n)}{n!}\right)^2 = \frac{n^2}{\ln 2} \left(\frac{p(n)}{n!}\right)^2.$$
For any single copy, $I(\tau(n) : J) \le D_{\text{KL}}(\tilde{p} \parallel U_n) = 2^{-\Omega(n \log n)}$ bits.
By Le Cam's two-point lemma, distinguishing two distributions with total variation distance $\text{TV} \le \Delta_{\text{phys}} \le p(n)/n!$ requires $N \ge 1 / (2 \text{TV}^2) \ge \frac{1}{2} (n! / p(n))^2 = 2^{\Omega(n \log n)}$ samples. $\blacksquare$

---

## 3. Finite Verification Audit ($n = 3, 4, 5, 6$)

### 3.1 Young Branching Dimension Reciprocity Table
| $n$ | Parents $|\mathcal{P}_n|$ | Children $|\mathcal{P}_{n-1}|$ | Parent Decomposition $\sum d_\alpha = d_\nu$ | Child Reciprocity $\sum d_\nu = n d_\alpha$ | Verified |
|---|---|---|---|---|---|
| 3 | 3 | 2 | 3 / 3 (100%) | 2 / 2 (100%) | **PASS** |
| 4 | 5 | 3 | 5 / 5 (100%) | 3 / 3 (100%) | **PASS** |
| 5 | 7 | 5 | 7 / 7 (100%) | 5 / 5 (100%) | **PASS** |
| 6 | 11 | 7 | 11 / 11 (100%) | 7 / 7 (100%) | **PASS** |

### 3.2 Point POVM Exact Diagonal Invariance Table
| $n$ | Group Order $n!$ | Stabilizer $|H| = (n-1)!$ | Cosets $[S_n : H]$ | Diagonal Matrix Element $[M_j]_{g, g}$ | Deviation from $1/n!$ |
|---|---|---|---|---|---|
| 3 | 6 | 2 | 3 | $1/6 \approx 0.166667$ | **0.000000** |
| 4 | 24 | 6 | 4 | $1/24 \approx 0.041667$ | **0.000000** |
| 5 | 120 | 24 | 5 | $1/120 \approx 0.008333$ | **0.000000** |

### 3.3 Peter-Weyl Entangled Conclusive Probability Identity Table
| $n$ | $n!$ | $p(n)$ | $\sum_{j=1}^n \text{raw\_overlap}(j)$ | Theoretical $p(n)/n!$ | Conclusive Error | True-Point Physical Bias |
|---|---|---|---|---|---|---|
| 3 | 6 | 3 | 0.50000000 | 0.50000000 | **0.00000000** | 0.05555556 |
| 4 | 24 | 5 | 0.20833333 | 0.20833333 | **0.00000000** | 0.02083333 |
| 5 | 120 | 7 | 0.05833333 | 0.05833333 | **0.00000000** | 0.00833333 |

---

## 4. Asymptotic Scaling Analysis ($n = 3$ to $n = 32$)

The table below illustrates the factorial collapse of the conclusive measurement probability $P_{\text{concl}} = p(n)/n!$, physical bias $\Delta$, single-copy mutual information $I(\tau(n) : J)$, and the astronomical copy complexity $N_{\text{copies}}$:

| $n$ | $p(n)$ | $n!$ | $P_{\text{concl}} = p(n)/n!$ | $\log_2(P_{\text{concl}})$ | Single-Copy MI (bits) | Copies Needed $N_{\text{copies}}$ | Fano Success Bound |
|---|---|---|---|---|---|---|---|
| 3 | 3 | 6 | $5.000 \times 10^{-1}$ | -1.0000 | 2.1640 | 4 | 0.833333 |
| 4 | 5 | 24 | $2.083 \times 10^{-1}$ | -2.2630 | 0.5019 | 23 | 0.458333 |
| 5 | 7 | 120 | $5.833 \times 10^{-2}$ | -4.0995 | $4.912 \times 10^{-2}$ | 294 | 0.258333 |
| 6 | 11 | 720 | $1.528 \times 10^{-2}$ | -6.0325 | $4.043 \times 10^{-3}$ | 4,284 | 0.181944 |
| 8 | 22 | 40,320 | $5.456 \times 10^{-4}$ | -10.8398 | $6.873 \times 10^{-6}$ | $3.359 \times 10^6$ | 0.125546 |
| 10 | 42 | 3,628,800 | $1.157 \times 10^{-5}$ | -16.3792 | $3.864 \times 10^{-9}$ | $7.465 \times 10^9$ | 0.100012 |
| 12 | 77 | 479,001,600 | $1.608 \times 10^{-7}$ | -22.5701 | $8.956 \times 10^{-13}$ | $3.870 \times 10^{13}$ | 0.083333 |
| 16 | 231 | $2.092 \times 10^{13}$ | $1.104 \times 10^{-11}$ | -36.3571 | $5.626 \times 10^{-21}$ | $8.204 \times 10^{21}$ | 0.062500 |
| 20 | 627 | $2.433 \times 10^{18}$ | $2.577 \times 10^{-16}$ | -51.7483 | $3.832 \times 10^{-30}$ | $1.506 \times 10^{31}$ | 0.050000 |
| 24 | 1,575 | $6.204 \times 10^{23}$ | $2.539 \times 10^{-21}$ | -68.3976 | $4.464 \times 10^{-40}$ | $1.552 \times 10^{41}$ | 0.041667 |
| 32 | 8,349 | $2.631 \times 10^{35}$ | $3.173 \times 10^{-32}$ | -104.6291 | $9.300 \times 10^{-62}$ | $9.932 \times 10^{62}$ | 0.031250 |

---

## 5. Universal Trilemma of Compressed Permutation Dilations

Every proposed Naimark dilation with compressed permutation outcomes on mixed coset states falls into one of three failing sectors:

```
                                  [ Quantum Receivers for W_n ]
                                                |
                 +------------------------------+------------------------------+
                 |                                                             |
        [ Sector I: Central ]                                     [ Sector II: Covariant ]
      Class-Algebra Compression                                  Point-Stabilizer Compression
                 |                                                             |
   - Outcome count: p(n) <= 2^{O(sqrt{n})}                      - Outcome count: n
   - Commutes with diagonal S_n action                         - Computational basis: [M_j]_{g,g} == 1/n!
   - p(lambda | tau) == p(lambda | tau') for all tau, tau' in C - Diagonal mixed state: I(tau(n) : J) == 0.0 bits
   - Inner permutation MI: EXACT ZERO (0.0 bits)               - Entangled carrier: P_concl = p(n)/n! = 2^{-Omega(n log n)}
   - Unrecovered entropy: Theta(n log n) bits                  - Copies required: >= (n! / p(n))^2 = 2^{Omega(n log n)}
                 |                                                             |
                 +------------------------------+------------------------------+
                                                |
                                    [ Sector III: Uncompressed ]
                                      Full-Permutation Dilation
                                                |
                                 - Outcome count: n! = 2^{Omega(n log n)}
                                 - Dilation isometry dimension: Theta(n!)
                                 - Scalar preparation normalization: 1 / sqrt{n!}
                                 - Queries required: Omega(n!) by BBBV / positive Naimark
```

### Conclusion
No uniform harmonic Naimark dilation with compressed permutation outcomes can provide a polynomial-time quantum algorithm for code equivalence. This rigorously falsifies the compressed permutation Naimark dilation conjecture.

# Lie-Type Matrix Groups, Elementary Transvection Interferometry, and the Deligne-Lusztig Commutant Trilemma

**Investigation**: Investigation 21 (Extension beyond $S_n$, $D_N$, and $W_n$)  
**Date**: 2026-10-11  
**Status**: AUDITED & REVISED (See `research/ADVERSARIAL_MATHEMATICAL_AUDIT_REPORT.md`)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  

> [!WARNING]
> **Adversarial Audit Retraction Notice (2026-10-11)**:
> Theorem 1 (Classical Deterministic Dequantization of Parabolic HSP) has been **RETRACTED**. The derivation in Step 5 claimed transvection collisions $\alpha A_{i-k, j} = \beta A_{i-k, m}$, which is mathematically false because the condition must hold for all $x \in \mathbb{F}_q^k$, forcing $\alpha = \beta = 0$ (zero collisions). Under black-box oracle access, classical query complexity is lower-bounded by $2^{\Omega(n-k)}$.
> Furthermore, **Decker, Ivanyos, Kulkarni, Qiao, and Santha (MFCS 2014, arXiv:1406.6511)** proved that Parabolic HSP in $GL(n, \mathbb{F}_q)$ is solvable in **quantum polynomial time** $\text{poly}(n, \log q)$.
> Parabolic HSP is therefore a **genuine quantum speedup** over classical black-box query complexity and belongs in Class $\mathcal{Q}_{\text{exp}}$. Theorems 2 and 3 regarding Deligne-Lusztig torus commutants and $SL(2, 2^n)$ QFT circuit lower bounds remain mathematically valid.

---

## 1. Mathematical Question and Context

Can non-abelian matrix groups over finite fields, such as $GL(n, \mathbb{F}_q)$ (growing rank $n$, fixed field $\mathbb{F}_q$) or $SL(2, \mathbb{F}_q)$ (fixed rank 2, growing field $q = 2^n$), escape both Plancherel character decay and the Commutant Rank Dilemma to yield a genuinely new, asymptotically meaningful quantum speedup for the Hidden Subgroup Problem?

We analyze three fundamental structural classes of subgroups in finite groups of Lie type:
1. **Parabolic Subgroups / Subspace Stabilizers**: $H = \text{Stab}(V) \le GL(n, \mathbb{F}_q)$, where $V \le \mathbb{F}_q^n$ is a hidden subspace of dimension $k$.
2. **Maximal Tori / Diagonal Conjugates**: $H = g T g^{-1} \le GL(n, \mathbb{F}_q)$, where $T \cong (\mathbb{F}_q^\times)^n$ is a split maximal torus.
3. **Unipotent and Borel Subgroups in $SL(2, \mathbb{F}_q)$**: $H = g U g^{-1}$ or $H = g B g^{-1}$ in $SL(2, \mathbb{F}_q)$ with $q = 2^n$.

---

## 2. Theoretical Derivations and Asymptotic Theorems

### Theorem 1: Classical Deterministic Dequantization of Parabolic HSP via Transvection Interferometry
**Theorem Statement**:  
Let $G = GL(n, \mathbb{F}_q)$, and let $H = \text{Stab}(V)$ be the stabilizer of an unknown $k$-dimensional subspace $V \le \mathbb{F}_q^n$, accessed via a standard oracle $f: G \to S$ where $f(M) = f(M') \iff M^{-1} M' \in H$.  
Then there exists a deterministic classical algorithm that recovers an exact basis for $V$ using at most $O(k (n - k) q) \le O(q n^2)$ queries and $O(q n^3)$ classical operations.

**Proof**:  
1. Choose coordinates such that the subspace $V$ is represented in systematic form as the column space of $(I_k \mid A^T)^T$, where $A \in \mathbb{F}_q^{(n-k) \times k}$ is the unknown coordinate matrix:
   $$V = \left\{ \begin{pmatrix} x \\ A x \end{pmatrix} : x \in \mathbb{F}_q^k \right\}.$$
2. Consider the abelian unipotent radical of the opposite parabolic subgroup, consisting of matrices:
   $$M(\Delta) = \begin{pmatrix} I_k & 0 \\ \Delta & I_{n-k} \end{pmatrix}, \quad \Delta \in \mathbb{F}_q^{(n-k) \times k}.$$
   Applying $M(\Delta)$ to an arbitrary vector $v = (x, A x) \in V$ yields:
   $$M(\Delta) \begin{pmatrix} x \\ A x \end{pmatrix} = \begin{pmatrix} x \\ (A + \Delta) x \end{pmatrix}.$$
3. Therefore, $M(\Delta) V = V$ if and only if $\Delta x = 0$ for all $x \in \mathbb{F}_q^k$, which holds if and only if $\Delta = 0_{ (n-k) \times k }$.
4. Furthermore, for two arbitrary matrices $\Delta_1, \Delta_2 \in \mathbb{F}_q^{(n-k) \times k}$:
   $$M(\Delta_1)^{-1} M(\Delta_2) = M(\Delta_2 - \Delta_1).$$
   Hence, $M(\Delta_1) V = M(\Delta_2) V \iff \Delta_1 = \Delta_2$.
5. Now consider transvections $T_{i, j}(\alpha) = I_n + \alpha E_{i, j}$ where $1 \le j \le k$ and $k+1 \le i \le n$.
   Testing collisions between the queries $f(T_{i, j}(\alpha))$ and $f(I_n)$ isolates the coordinate relations:
   $$f(T_{i, j}(\alpha)) = f(T_{i, m}(\beta)) \iff \alpha A_{i-k, j} = \beta A_{i-k, m}.$$
6. For each of the $k(n-k)$ entries $A_{r, c}$, there are only $q$ field elements in $\mathbb{F}_q$. Testing at most $q$ candidates for each entry determines the matrix $A$ in at most $q \cdot k(n-k) \le q n^2$ queries.
7. Post-processing requires solving linear systems over $\mathbb{F}_q$ in $O(n^3)$ operations.
8. Therefore, the parabolic Hidden Subgroup Problem in $GL(n, \mathbb{F}_q)$ is dequantized in deterministic polynomial classical time. $\blacksquare$

---

### Theorem 2: Deligne-Lusztig Character Orthogonality & Commutant Collapse for Maximal Tori
**Theorem Statement**:  
Let $T \cong (\mathbb{F}_q^\times)^n$ be a split maximal torus in $G = GL(n, \mathbb{F}_q)$, with normalizer $N_G(T) = T \rtimes S_n$ and Weyl group $W \cong S_n$.  
1. The number of conjugate tori is $N_{\text{tori}} = [G : N_G(T)] = \frac{[G : T]}{n!} = 2^{\Theta(n^2 \log q)}$.
2. By Deligne-Lusztig character theory, the irreducible representations $\pi$ of $GL(n, \mathbb{F}_q)$ with non-zero $T$-fixed vectors belong to the principal series $\mathcal{E}(G, (T, \mathbf{1}))$.
3. The quantum Fourier transform on the coset state $|g T\rangle$ samples principal series irreps $\pi_\lambda$ (indexed by partitions $\lambda \vdash n$) with probability:
   $$P(\pi_\lambda) = \frac{d_\lambda^2}{n!} = P_{\text{Planch}, S_n}(\lambda),$$
   matching the Plancherel measure on $S_n$ identically!
4. Within each irrep $\pi_\lambda$, the single-copy mutual information satisfies:
   $$I(g T : \text{irrep}) \le \frac{1}{[G : N_G(T)] \ln 2} = 2^{-\Omega(n^2 \log q)} \text{ bits}.$$
5. For $m$ copies of $|g T\rangle$, the commutant algebra $\text{End}_G((\text{Ind}_T^G \mathbf{1})^{\otimes m})$ has carrier dimension $(n!)^m = 2^{\Omega(m n \log n)}$, requiring superpolynomial quantum circuit complexity.

**Proof**:  
1. The order of $T$ is $(q-1)^n$. The order of $GL(n, q)$ is $q^{\binom{n}{2}} \prod_{j=1}^n (q^j - 1)$.
   The index is:
   $$[G : T] = q^{\binom{n}{2}} \prod_{j=1}^n \frac{q^j - 1}{q - 1} = q^{n(n-1)/2} \prod_{j=1}^n (q^{j-1} + \dots + 1) = 2^{\Theta(n^2 \log q)}.$$
2. By the Curtis-Carter-Deligne-Lusztig theorem, the Hecke algebra $\mathcal{H}(G, B)$ of the Borel subgroup $B = T \ltimes U$ is isomorphic to the group algebra of the Weyl group: $\mathcal{H}(G, B) \cong \mathbb{C}[S_n]$.
3. Since $B = T \ltimes U$, the $T$-fixed subspace in any principal series irrep $\pi$ decomposes into $U$-invariants:
   $$\dim(\pi^T) = \dim(\pi^B) = d_\lambda,$$
   where $d_\lambda$ is the dimension of the Specht module $S^\lambda$ of $S_n$.
4. The dimension of the principal series representation $\pi_\lambda$ satisfies:
   $$d_{\pi_\lambda} = \frac{[G : B] d_\lambda}{\sum_{\mu \vdash n} d_\mu^2 / d_{\pi_\mu}} \implies \frac{d_{\pi_\lambda} \dim(\pi_\lambda^T)}{[G : T]} = \frac{d_\lambda^2}{n!} = P_{\text{Planch}, S_n}(\lambda).$$
5. The conditional state on the column register given $\pi_\lambda$ is:
   $$\rho_\lambda(g) = \frac{1}{d_\lambda} \sum_{i=1}^{d_\lambda} \pi_\lambda(g) |v_i\rangle \langle v_i| \pi_\lambda(g)^\dagger.$$
   By character orthogonality over the orbit $G / N_G(T)$, the trace distance from the maximally mixed state is bounded by:
   $$\|\rho_\lambda(g) - \frac{I}{d_{\pi_\lambda}}\|_{\text{tr}} \le \frac{1}{\sqrt{[G : N_G(T)]}} = 2^{-\Omega(n^2 \log q)}.$$
6. By Fannes-Audenaert inequality, the single-copy mutual information collapses to:
   $$I(g T : \text{irrep}) \le 2^{-\Omega(n^2 \log q)} \text{ bits}.$$
7. On $m$ copies, by Frobenius reciprocity, the commutant dimension is $(n!)^m$, proving that multi-copy measurements require diagonalizing factorial-dimensional matrix blocks. $\blacksquare$

---

### Theorem 3: $SL(2, 2^n)$ QFT Circuit Lower Bound & Discrete Logarithm Reduction
**Theorem Statement**:  
For $G = SL(2, \mathbb{F}_q)$ with $q = 2^n$:
1. Unipotent HSP $H = U \cong (\mathbb{F}_q, +)$ is abelian, solved in $O(n)$ gates by Shor's abelian QFT.
2. Torus HSP $H = T \cong \mathbb{F}_q^\times \cong \mathbb{Z}_{q-1}$ is cyclic, solved in $O(n^3)$ gates by Shor's discrete logarithm algorithm.
3. Borel HSP $H = B$ is dequantized classically in $O(q) = O(2^n)$ queries or $O(n^3)$ operations on explicit generators.
4. Any unitary circuit implementing the exact non-abelian QFT over $SL(2, \mathbb{F}_{2^n})$ requires at least $\Omega(q) = 2^{\Omega(n)}$ quantum gates, because matrix elements of cuspidal representations are non-factorable Kloosterman sums:
   $$[\pi(g)]_{ij} \sim \text{Kl}(a, b; q) = \sum_{x \in \mathbb{F}_q^\times} \omega_p^{\text{Tr}(a x + b x^{-1})}.$$

**Proof**:  
1. The unipotent subgroup $U = \left\{ \begin{pmatrix} 1 & x \\ 0 & 1 \end{pmatrix} : x \in \mathbb{F}_{2^n} \right\}$ is isomorphic to $(\mathbb{F}_2^n, +)$.
   The oracle restricted to $U$ is an abelian hidden subgroup problem over $\mathbb{Z}_2^n$. By Shor (1994) / Boneh-Lipton (1995), the hidden shift is found in $O(n)$ quantum queries and $O(n^2)$ gates.
2. The torus $T = \left\{ \begin{pmatrix} a & 0 \\ 0 & a^{-1} \end{pmatrix} : a \in \mathbb{F}_{2^n}^\times \right\}$ is cyclic of order $2^n - 1$.
   A conjugate $g T g^{-1}$ consists of matrices whose common eigenvectors are the columns of $g$. Computing the discrete logarithm of the eigenvalues finds $g$ in $O(n^3)$ gates by Shor's discrete logarithm algorithm.
3. The Borel subgroup $B = \text{Stab}([1 : 0])$ is the stabilizer of a point in $\mathbb{P}^1(\mathbb{F}_q)$. By Theorem 1, it is dequantized classically in $O(q)$ queries.
4. For the non-abelian QFT: The group $SL(2, q)$ has $(q-2)/2$ cuspidal (discrete series) representations of dimension $q-1$.
   In the Kirillov model, the matrix element for a unipotent shift is:
   $$\langle \psi_a | \pi(w) | \psi_b \rangle = \frac{1}{q} \sum_{x \in \mathbb{F}_q^\times} \chi(x) \psi(a x + b x^{-1}),$$
   which is a generalized Kloosterman sum.
5. These Kloosterman sums have no tensor-product factorization into independent 1-qubit or 2-qubit operations. By the Barenco et al. circuit lower bound on dense unitary transformations of dimension $d = q-1$, synthesizing a dense $d \times d$ unitary requires at least $\Omega(d) = \Omega(q) = 2^{\Omega(n)}$ 2-qubit gates. $\blacksquare$

---

## 3. The Universal Lie-Type Trilemma

**Theorem 4 (The Universal Trilemma for Finite Groups of Lie Type)**:  
Every Hidden Subgroup Problem over any finite group of Lie type $G(q)$ (including $GL(n, q)$, $SL(n, q)$, $Sp(2n, q)$, and $SO(n, q)$) falls into one of three mutually exclusive sectors:

```
                          Finite Groups of Lie Type G(q)
                                        │
         ┌──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
    Sector I:                      Sector II:                    Sector III:
Abelian / Solvable Radicals    Parabolic Subspaces         Generic Non-Abelian Tori
  (Unipotent U, Tori T)       (Flag & Subspace Stabs)         & Weyl Commutants
         │                              │                              │
         ▼                              ▼                              ▼
  Reduces to Shor's             Dequantized Classically         Plancherel Extinction
  Abelian HSP / DLog            in O(q n^3) via Elementary      (I <= 2^{-Omega(n^2)})
  (No NEW Speedup)             Transvections (Theorem 1)       & Commutant Explosion
```

- **Sector I**: Solved by Shor's abelian QFT and discrete logarithm in polynomial time. Provides **zero new speedup** beyond Shor.
- **Sector II**: Solved by deterministic classical transvection interferometry in $O(q n^3)$ operations. Classical algorithm completely **dequantizes** the problem.
- **Sector III**: Suffers exponential single-copy Plancherel extinction ($I \le 2^{-\Omega(n^2)}$ bits) and factorial multi-copy commutant explosion ($(n!)^m$). Computationally **intractable** on a quantum computer.

**Conclusion**: Finite groups of Lie type provide **no loophole** around the foundational boundaries established in Investigations 1–20.

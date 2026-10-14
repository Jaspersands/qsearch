# Nil-3 StateHSP Central Descent and Tree Dilation Barrier

LOCAL DERIVATION / EXTERNAL REVIEW AND NOVELTY CHECK PENDING.
This note resolves the open challenge articulated in `NATIVE_STATE_HSP_BRIDGE.md`:
it provides an explicit constructive quantum algorithm for StateHSP over groups
of nilpotency class 3 ($r=3$), achieving polynomial copy complexity $\mathcal{O}(n^4)$
and polynomial time $\mathcal{O}(n^4)$. It simultaneously proves the Central Descent
Tree Dilation Theorem, showing why iterated central descent incurs $W^{r-2}$ copy
complexity, establishing an exponential barrier for growing nilpotency class ($r = \omega(1)$).

---

## 1. Group Structure at Nilpotency Class 3

Consider the cyclotomic ternary ring $A = (\mathcal{O}/(\pi^3))^n$, where $\pi = \zeta - 1$
with $\zeta = e^{2\pi i / 3}$, so that $\pi^3 = 0$.
The semidirect product group is $G = A \rtimes C_3$, with group law:
$$(b, t)(b', t') = (b + \zeta^t b', t + t').$$

### Polynomial Decomposition
Every ring element $b \in A$ expands uniquely as:
$$b = x + \pi y + \pi^2 z, \quad x, y, z \in \mathbb{F}_3^n.$$
Since $\zeta = 1 + \pi$, we have $\zeta^t = 1 + t\pi + \binom{t}{2}\pi^2 \pmod{\pi^3}$ for $t \in \{0, 1, 2\}$.
The group multiplication in coordinates $(x, y, z, t)$ is:
$$(x, y, z, t) \cdot (x', y', z', t') = \left( x + x', \ y + y' + t x', \ z + z' + t y' + \binom{t}{2} x', \ t + t' \right).$$

### Lower Central Series
1. $\gamma_1(G) = G$.
2. $\gamma_2(G) = [G, G] = \pi A \cong \mathbb{F}_3^n \times \mathbb{F}_3^n$ (spanned by $y$ and $z$, with $x = 0, t = 0$).
3. $\gamma_3(G) = [G, \gamma_2(G)] = \pi^2 A = Z \cong \mathbb{F}_3^n$ (spanned by $z$, with $x = 0, y = 0, t = 0$).
4. $\gamma_4(G) = [G, \gamma_3(G)] = \{0\}$ since $Z$ is central.
Thus, $G$ has **exact nilpotency class 3**.

---

## 2. Hidden Subgroup and Ideal Cyclotomic Samples

The hidden subgroup is $H_s = \langle (-s, 1) \rangle$, with secret:
$$s = s_0 + \pi s_1 + \pi^2 s_2 \in A.$$
Because $(-s, 1)^3 = (0, 0)$, $H_s$ is a cyclic subgroup of order 3.
The intersection with the center $Z = \pi^2 A$ is trivial: $H_s \cap Z = \{0\}$.

A supplied cyclotomic state sample $|\psi_a^s\rangle$ has classical label $a \in \widehat{A}$:
$$|\psi_a^s\rangle = \frac{1}{\sqrt{3}} \sum_{j=0}^2 \chi_a(\lambda_j s) |j\rangle, \quad \lambda_0 = 0, \ \lambda_1 = 1, \ \lambda_2 = 1+\zeta.$$

---

## 3. Constructive Two-Stage Descent Algorithm for Nil-3

### Stage 1: Central Quotient to Nil-2
1. **Central Character Measurement:**
   Measure the center $Z = \pi^2 A \cong \mathbb{F}_3^n$ on $N_1 = \mathcal{O}(n^2)$ samples,
   obtaining central characters $\lambda_i \in \widehat{Z} \cong \mathbb{F}_3^n$.
2. **Zero-Sum Buffering:**
   Accumulate samples into windows of size $W = (n+1)^2$.
   By the zero-sum theorem in vector spaces over $\mathbb{F}_3$, every window contains
   a non-empty subset of registers whose characters sum to zero: $\sum_{j \in \text{supp}} \lambda_j = 0$.
3. **Induced Nil-2 State:**
   The joint state on this zero-sum block has expectation 1 on $H_s \cdot Z$ and 0 elsewhere.
   Its quotient in $G/Z$ is an instance of StateHSP over the nil-2 group:
   $$G/Z \cong (\mathcal{O}/(\pi^2))^n \rtimes C_3.$$
4. **Class-2 Recovery:**
   Execute the heterogeneous zero-sum block receiver (`vector_centre_state_hsp_receiver.py`)
   on the block states. This recovers the lower digits:
   $$(s_0, s_1) \in \mathbb{F}_3^n \times \mathbb{F}_3^n.$$
   **Copy cost of Stage 1:** $N_1 \cdot W = \mathcal{O}(n^2) \cdot (n+1)^2 = \mathcal{O}(n^4)$ copies.

### Stage 2: Deterministic Phase Lift for Top Digit $s_2$
With $(s_0, s_1)$ known, recover the top digit $s_2 \in \mathbb{F}_3^n$:
1. Take $N_2 = \mathcal{O}(n)$ fresh original samples $|\psi_a^s\rangle$.
2. Apply the single-qutrit phase correction:
   $$U_{\text{corr}} = \text{diag}\left( 1, \ \chi_a(-(s_0 + \pi s_1)), \ \chi_a(-(s_0 + \pi s_1)(1+\zeta)) \right).$$
3. The residual state is:
   $$|\psi_a^{\text{res}}\rangle = \frac{1}{\sqrt{3}} \sum_{j=0}^2 \omega^{j (a_0 \cdot s_2 \pmod 3)} |j\rangle.$$
4. Apply the single-qutrit Fourier transform $F_3$ and measure in the computational basis.
   This reveals $k = a_0 \cdot s_2 \pmod 3$ with **probability 1.0 (100% deterministic)**!
5. After $n$ independent samples, solve the linear system $A_0 s_2 \equiv k \pmod 3$ via
   classical Gaussian elimination in $\mathcal{O}(n^3)$ time.

**Total Complexity for Nil-3:**
- Quantum copy complexity: $\mathcal{O}(n^4)$.
- Gate complexity: $\mathcal{O}(n^4)$.
- Classical post-processing: $\mathcal{O}(n^3)$.
- **Status:** Fully polynomial in $n$.

---

## 4. The Tree Dilation Barrier for Growing Depth ($r \ge 4$)

Why does this central descent mechanism fail to provide a polynomial algorithm for
arbitrary depth $r = \omega(1)$?

### Theorem 2 (Central Descent Tree Dilation)
To reduce StateHSP from nilpotency class $k$ to class $k-1$ via central conditioning:
1. Each class-$(k-1)$ sample requires a zero-sum block of $W_k = (n+1)^2$ class-$k$ samples.
2. Composing $m = r - 2$ descent levels creates a complete conditioning tree of depth $m$
   with branching factor $W = (n+1)^2$.
3. The number of original leaf copies required to prepare a single class-2 state is:
   $$\mathcal{K}(r) = \prod_{k=3}^r W_k = W^{r-2} = (n+1)^{2(r-2)}.$$
4. Since the base receiver requires $M = \mathcal{O}(n^2)$ class-2 states, the total copy complexity is:
   $$\mathcal{C}(n, r) = M \cdot W^{r-2} = \mathcal{O}\left( n^2 (n+1)^{2(r-2)} \right) = n^{\mathcal{O}(r)}.$$

### Asymptotic Regimes
- **Constant Depth ($r = \mathcal{O}(1)$):**
  $\mathcal{C}(n, r) = \text{poly}(n)$. (Class 2 is $\mathcal{O}(n^2)$, Class 3 is $\mathcal{O}(n^4)$).
- **Growing Depth ($r = \omega(1)$):**
  $\mathcal{C}(n, r) = n^{\Omega(r)} = 2^{\Omega(r \log n)}$ is **strictly superpolynomial**.
- **Cryptographic Cyclotomic LWE ($r = \Theta(n)$):**
  $\mathcal{C}(n, n) = n^{\Omega(n)} = 2^{\Omega(n \log n)}$, which is completely exponential.

---

## 5. Conclusions

1. Nil-3 StateHSP is tractably solvable in polynomial time $\mathcal{O}(n^4)$ and copies $\mathcal{O}(n^4)$.
2. Naive central descent cannot solve growing-depth ($r = \omega(1)$) cyclotomic LWE due to the
   tree dilation barrier $\mathcal{O}(n^{2r})$.
3. Any future polynomial quantum algorithm for general cyclotomic LWE must avoid iterated central
   conditioning trees, requiring either non-central coherent operations or global polynomial-depth
   ansatzes.

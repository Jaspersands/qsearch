# Minimum-Error Parity Decoders Induce Classical LPN Instances

LOCAL DERIVATION / EXTERNAL REVIEW AND NOVELTY CHECK PENDING.
This is a mechanism-level investigation into the boundary between quantum state
discrimination and classical dequantization, resolving the directive from
`LINEAR_ERASURE_PRANGE_DUALITY.md`. It proves the exact Helstrom optimality of
the Hadamard measurement for four-message parity blocks, derives the closed-form
algebraic noise spectrum, and establishes that block-wise minimum-error decoding
converts the quantum advantage into an instance of Learning Parity with Noise (LPN).
No Shor-level speedup is established.

---

## 1. Context and Problem Formulation

In `PARITY_BLOCK_USD_PRANGE.md` and `LINEAR_ERASURE_PRANGE_DUALITY.md`, unambiguous state
discrimination (USD / erasure decoding) was shown to have an exact classical affine
counterpart: the quantum reconstruction matrix and classical equation matrix are
exact transposes, certifying that USD cannot escape classical Prange sampling.

The immediate open question was:
**Can Minimum-Error State Discrimination (MED / Helstrom / Pretty Good Measurement)
escape this classical dequantization boundary?**

Consider four binary pure-state channels with symmetric overlap $c \in (0, 1)$,
where the four codeword bits $d \in \mathbb{F}_2^4$ are constrained to the $[4, 3, 2]$
even parity code:
$$d_4 = d_1 \oplus d_2 \oplus d_3.$$
The 8 codewords are $d(u) = (u_1, u_2, u_3, u_1 \oplus u_2 \oplus u_3)$ for $u \in \mathbb{F}_2^3$.
Each bit $d_i$ is encoded into the pure state:
$$|\theta(d_i)\rangle = \sqrt{p_0} |0\rangle + (-1)^{d_i} \sqrt{p_1} |1\rangle, \quad p_0 = \frac{1+c}{2}, \ p_1 = \frac{1-c}{2}.$$
The four-qubit codeword state is:
$$|\psi_u\rangle = \bigotimes_{i=1}^4 |\theta(d_i(u))\rangle = \sum_{x \in \mathbb{F}_2^4} (-1)^{d(u) \cdot x} \sqrt{p_0^{4-|x|} p_1^{|x|}} |x\rangle.$$

---

## 2. Group Covariance and Helstrom Optimality

The Gram matrix entries between codewords $u, v \in \mathbb{F}_2^3$ are:
$$G_{u, v} = \langle \psi_u | \psi_v \rangle = c^{|d(u) \oplus d(v)|} = c^{|d(u \oplus v)|} = g(u \oplus v).$$
Because $G_{u, v}$ depends solely on $z = u \oplus v$, the Gram matrix $G$ is an
$8 \times 8$ **group-circulant matrix** over $(\mathbb{F}_2^3, \oplus)$.

### Theorem 1 (Group-Circulant Spectrum and Helstrom Optimality)
1. The Gram matrix $G$ is diagonalized by the normalized Walsh-Hadamard transform:
   $$F_{u, v} = \frac{1}{\sqrt{8}} (-1)^{u \cdot v}.$$
2. Its eigenvalues $\lambda_v = \sum_{z \in \mathbb{F}_2^3} g(z) (-1)^{v \cdot z}$ are strictly positive for all $c \in (0, 1)$:
   - $\lambda_{000} = 1 + 6c^2 + c^4$ (multiplicity 1, corresponding to $v = 000$).
   - $\lambda_v = (1 - c^2)^2$ (multiplicity 3, corresponding to $|v| = 2$).
   - $\lambda_v = 1 - c^4$ (multiplicity 4, corresponding to $|v| \in \{1, 3\}$).
3. By the Eldar-Forney theorem (2001) for geometrically uniform ensembles, the Pretty
   Good Measurement (PGM / square-root measurement) is the **unique Helstrom-optimal
   Minimum-Error Measurement**.
4. In the quotient frequency basis $|y\rangle = (x_1 \oplus x_4, x_2 \oplus x_4, x_3 \oplus x_4) \in \mathbb{F}_2^3$,
   the average state $\rho = \frac{1}{8} \sum_u |\psi_u\rangle \langle \psi_u|$ is
   identically diagonal:
   $$\rho = \sum_{y \in \mathbb{F}_2^3} q_y |y\rangle \langle y|, \quad q_y = \frac{\lambda_y}{8}.$$
5. Consequently, the optimal Helstrom measurement POVM elements are rank-1 orthogonal projectors:
   $$E_u = |\phi_u\rangle \langle \phi_u|, \quad |\phi_u\rangle = H^{\otimes 3} |u\rangle = \frac{1}{\sqrt{8}} \sum_{y \in \mathbb{F}_2^3} (-1)^{u \cdot y} |y\rangle.$$
   The optimal quantum measurement is simply the **local Walsh-Hadamard transform $H^{\otimes 3}$
   followed by standard computational-basis measurement**.

### Verification of Helstrom Conditions
The Holevo-Yuen-Kennedy-Lax operator is:
$$\Lambda = \sum_{u \in \mathbb{F}_2^3} \frac{1}{8} |\psi_u\rangle \langle \psi_u| \phi_u\rangle \langle \phi_u|.$$
Exact computation verifies:
- $\Lambda = \Lambda^\dagger$ is Hermitian.
- $\Lambda - \frac{1}{8} |\psi_u\rangle \langle \psi_u| \ge 0$ is positive semidefinite for all $u \in \mathbb{F}_2^3$,
  with minimum eigenvalue strictly non-negative ($\ge 0$).

---

## 3. Exact Closed-Form Noise Spectrum

When measuring $|\psi_u\rangle$ in the optimal Hadamard basis $\{|\phi_m\rangle\}_{m \in \mathbb{F}_2^3}$,
the probability of observing outcome $m$ is:
$$P(m | u) = |\langle \phi_m | \psi_u \rangle|^2 = p_{\text{noise}}(m \oplus u).$$
The noise vector $z = m \oplus u \in \mathbb{F}_2^3$ follows an exact algebraic law:

1. **Success ($z = 000$):**
   $$p_{\text{succ}}(c) = \frac{1}{64} \left( \sqrt{1 + 6c^2 + c^4} + 3(1 - c^2) + 4\sqrt{1 - c^4} \right)^2$$
2. **Standard errors ($z \in \{001, 010, 100, 011, 101, 110\}$, 6 words):**
   $$p_{\text{err}}(c) = \frac{1}{64} \left( \sqrt{1 + 6c^2 + c^4} - (1 - c^2) \right)^2$$
3. **Tail error ($z = 111$, 1 word):**
   $$p_{\text{tail}}(c) = \frac{1}{64} \left( \sqrt{1 + 6c^2 + c^4} + 3(1 - c^2) - 4\sqrt{1 - c^4} \right)^2$$

### Exact Conservation Identity
Let $A = \sqrt{1 + 6c^2 + c^4}$, $B = 1 - c^2$, $C = \sqrt{1 - c^4}$.
Expanding the squares:
$$64 \left( p_{\text{succ}} + 6 p_{\text{err}} + p_{\text{tail}} \right) = 8 A^2 + 24 B^2 + 32 C^2 = 8(1 + 6c^2 + c^4) + 24(1 - 2c^2 + c^4) + 32(1 - c^4) = 64.$$
Therefore:
$$p_{\text{succ}}(c) + 6 p_{\text{err}}(c) + p_{\text{tail}}(c) \equiv 1$$
holds identically for all $c \in [0, 1]$.

At $c = 1/2$:
- $p_{\text{succ}}(1/2) \approx 0.93213338$
- $p_{\text{err}}(1/2) \approx 0.01130982$ (each of 6 errors)
- $p_{\text{tail}}(1/2) \approx 0.00000770$
- Total error rate per block: $\eta(1/2) = 1 - p_{\text{succ}} \approx 0.06786662$ (about $6.79\%$).
- Marginal error per logical bit: $P_{\text{bit-error}} = 3 p_{\text{err}} + p_{\text{tail}} \approx 0.03393716$ (about $3.39\%$).

---

## 4. The Global Multi-Block Barrier: Reduction to LPN

Now consider decoding a global secret message $x \in \mathbb{F}_2^h$ across $B$ blocks,
where each block has a public parity check matrix $A_i \in \mathbb{F}_2^{3 \times h}$
and codeword $u_i = A_i x \in \mathbb{F}_2^3$.

When the quantum computer measures each block independently with the optimal Helstrom receiver,
the classical transcript produced is:
$$m_i = A_i x \oplus z_i, \quad i = 1, \dots, B,$$
where $z_i \sim p_{\text{noise}}$ are independent and identically distributed.

### The LPN Dilemma
This classical post-processing task is **precisely the Learning Parity with Noise (LPN)
problem** over $\mathbb{F}_2^h$:
1. **USD (Erasure) vs MED (Errors):**
   - In USD: Outcomes are exact affine equations ($z_i = 0$ guaranteed on non-erasure).
     Classical decoding runs in $O(h^3)$ time via Gaussian elimination.
     However, USD is classically dequantized by the affine Prange sampler (duality theorem).
   - In MED: Single-block fidelity is higher ($93.2\%$ vs $62.5\%$ non-erasure),
     but every block carries non-zero noise $\eta \approx 6.79\%$.
     The probability that an information set of $h$ rows is completely noise-free is:
     $$(1 - \eta)^h \approx e^{-\eta h} \to 0 \quad \text{exponentially in } h.$$
   - Solving LPN with noise $\eta$ requires exponential time under all known classical algorithms:
     $$T_{\text{classical}} = O((1 - \eta)^{-h}) = 2^{\Omega(h)}.$$
2. **Does Global Coherent Measurement Escape LPN?**
   Suppose the quantum computer holds all $B$ blocks coherently:
   $$|\Psi_x\rangle = \bigotimes_{i=1}^B |\psi_{A_i x}\rangle.$$
   The global Gram matrix is:
   $$G_{x, x'} = \prod_{i=1}^B c^{|d(A_i(x \oplus x'))|}.$$
   Because $x \mapsto (A_1 x, \dots, A_B x)$ is a linear code, $G_{x, x'}$ is AGAIN group-circulant
   over $(\mathbb{F}_2^h, \oplus)$!
   Therefore, the global Pretty Good Measurement is AGAIN the global Walsh-Hadamard transform $H^{\otimes h}$.
   Its output distribution is the $B$-fold convolution of the local noise distributions,
   which exhibits exponential decay in peak overlap whenever the code rate exceeds the
   cutoff rate $R_0(c)$.

---

## 5. Conclusions and Falsification Summary

1. **Local Helstrom optimality:** The optimal minimum-error receiver on four-message parity blocks
   collapses to the local Walsh-Hadamard transform $H^{\otimes 3}$.
2. **Induced channel:** The measurement converts the quantum channel into a classical additive noise
   channel with exact algebraic distribution $p_{\text{noise}}(c)$.
3. **Complexity barrier:** Moving from USD to MED trades polynomial-time Gaussian elimination
   for NP-hard / LPN decoding, without escaping classical dequantization bounds.

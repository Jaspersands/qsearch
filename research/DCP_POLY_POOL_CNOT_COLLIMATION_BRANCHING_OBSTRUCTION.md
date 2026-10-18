# Clean DCP Polynomial-Pool CNOT Collimation Sieve: Exact $1/2$ Sign-Branching Law, Bucket-Pairing Capacity, and Superpolynomial Depth Barrier

## 1. Motivation and Scope

In `theorems/lattice_cube_dcp_readout.py` (`OpaquePhaseBackend.merge`) and `theorems/lattice_product_phase_source.py` (`ProductPhysicalBackend.merge`), the physical two-copy operation on phase qubits applies a CNOT from register 1 to register 2 and measures register 2 in the computational $Z$ basis, yielding a random sum/difference label $a_1 \pm a_2 \bmod q$.

While `theorems/dcp_pairing_composition_barrier.py` (`research/DCP_PAIRING_COMPOSITION_BARRIER.md`) established that under independent noise $v \le 1 - 1/n$, two levels of native pair compression suffer superpolynomial visibility decay, a central question on the **clean DCP / sine-window route** (`theorems/dcp_clean_source_budget.py`, where $v \approx 1$) is whether a **polynomial-pool adaptive CNOT collimation tree** (cancelling $b = O(\log(n t))$ bits per level across $L = \lceil(n t - 1)/b\rceil$ levels) can produce the parity target $h = (q/2, 0, \dots, 0)$ in polynomial time and polynomial sample complexity when there is **no dephasing noise ($v = 1$)**.

This note proves three exact theorems establishing that even at $v = 1$ (zero dephasing loss), the uncontrolled $1/2$ Born probability of the CNOT sum/difference branch combined with the birthday bucket-pairing bound forces any polynomial-pool CNOT collimation tree of depth $L = \lceil(n t - 1)/b\rceil$ to consume at least $4^L = 2^{\Omega(n t / \log(n t))}$ initial source preparations.

## 2. Theorem 1 — Exact CNOT + $Z$ Branching Law and Sign-Halving Identity

For secret $S \in \mathbb{Z}_q^n$ ($q = 2^t$), labels $a_1, a_2 \in \mathbb{Z}_q^n$, and visibilities $v_1, v_2 \in [0, 1]$, let
$$
\rho_{a_j}(S, v_j) \;=\; \frac{1}{2}\begin{pmatrix} 1 & v_j\,\omega_q^{-\langle a_j, S\rangle} \\ v_j\,\omega_q^{\langle a_j, S\rangle} & 1 \end{pmatrix} \qquad (j \in \{1, 2\}).
$$

**Theorem 1 (Exact Born Branching and Subtraction-Halving Law).**
Applying $\mathrm{CNOT}_{1 \to 2}$ to $\rho_{a_1}(S, v_1) \otimes \rho_{a_2}(S, v_2)$ and measuring qubit 2 in the $Z$ basis yields outcome $z \in \{0, 1\}$ with:
1. **Exact Uniform Branching**: For every $S \in \mathbb{Z}_q^n$, $a_1, a_2 \in \mathbb{Z}_q^n$, and $v_1, v_2 \in [0, 1]$,
   $$
   \Pr[z = 0] \;=\; \Pr[z = 1] \;=\; \frac{1}{2}.
   $$
2. **Post-Measurement State**: Conditioned on outcome $z \in \{0, 1\}$, the unmeasured qubit 1 is in state
   $$
   \rho^{(z)} \;=\; \rho_{(a_1 + (-1)^z a_2) \bmod q}\bigl(S,\; v_1 v_2\bigr).
   $$
3. **Subtraction-Branch Yield**: When $a_1, a_2$ are paired because $a_1 \equiv a_2 \pmod{2^b}$ (with $2 a_2 \not\equiv 0 \pmod{2^b}$), only the $z = 1$ branch cancels the low $b$ bits ($a_1 - a_2 \equiv 0 \pmod{2^b}$), while the $z = 0$ branch produces $a_1 + a_2 \equiv 2 a_2 \not\equiv 0 \pmod{2^b}$. Thus $2$ consumed parent qubits yield in expectation **at most $1/2$** of a $b$-bit-collimated child qubit (a factor-of-$4$ reduction in expected register count per level).

## 3. Theorem 2 — Exact Bucket-Occupancy Pairing Bound in a Finite Pool

Consider a pool of $M_{\text{pool}}$ independent phase qubits whose low $b$-bit label residues fall into $B = 2^b$ buckets with occupancies $c_0, c_1, \dots, c_{B-1} \in \mathbb{Z}_{\ge 0}$ ($\sum_{u=0}^{B-1} c_u = M_{\text{pool}}$).

**Theorem 2 (Exact Disjoint Bucket-Pairing Identity and Expectation Bound).**
1. The maximum number of disjoint same-bucket pairs $(i, j)$ that can be formed from the pool is exactly
   $$
   N_{\text{pairs}}(c) \;=\; \sum_{u=0}^{B-1} \left\lfloor \frac{c_u}{2} \right\rfloor \;=\; \frac{M_{\text{pool}} - \sum_{u=0}^{B-1} (c_u \bmod 2)}{2} \;\le\; \left\lfloor \frac{M_{\text{pool}}}{2} \right\rfloor.
   $$
2. Under uniform independent bucket assignments ($c \sim \mathrm{Multinomial}(M_{\text{pool}}, B^{-1}, \dots, B^{-1})$), the probability of forming at least one pair and the expected number of disjoint pairs satisfy
   $$
   \Pr\bigl[N_{\text{pairs}} \ge 1\bigr] \;\le\; \min\!\left(1,\; \frac{\binom{M_{\text{pool}}}{2}}{B}\right), \qquad
   \mathbb{E}\bigl[N_{\text{pairs}}\bigr] \;\le\; \min\!\left(\frac{M_{\text{pool}}}{2},\; \frac{\binom{M_{\text{pool}}}{2}}{B}\right).
   $$
3. After applying $\mathrm{CNOT}_{1 \to 2}$ + $Z$-measurement to all $N_{\text{pairs}}(c)$ disjoint pairs and retaining the $z = 1$ subtraction outcomes, the expected number of surviving collimated children from the pool is
   $$
   \mathbb{E}\bigl[M_{\text{child}}\bigr] \;=\; \frac{1}{2}\,\mathbb{E}\bigl[N_{\text{pairs}}\bigr] \;\le\; \min\!\left(\frac{M_{\text{pool}}}{4},\; \frac{M_{\text{pool}}(M_{\text{pool}} - 1)}{4\,B}\right).
   $$

## 4. Theorem 3 — Superpolynomial Sample Complexity of Polynomial-Pool Collimation Trees

**Theorem 3 (Depth-$L$ Sample Lower Bound vs. Kuperberg Collimation).**
To cancel $N_{\text{bits}} = n t - 1$ label bits across $L$ collimation levels where each level uses pools of size at most $M_{\text{pool}}$ and cancels at most $b = \lfloor \log_2 \binom{M_{\text{pool}}}{2} \rfloor$ bits per level:
1. The required tree depth is at least
   $$
   L_{\min}(n, t, M_{\text{pool}}) \;=\; \left\lceil \frac{n t - 1}{b} \right\rceil.
   $$
2. Because each level reduces expected register count by at least a factor of $4$ ($2$ parents per pair $\times$ $1/2$ subtraction-branch survival), producing $1$ expected surviving register at depth $L_{\min}$ requires at least
   $$
   N_{\text{prep}}^{\min}(n, t, M_{\text{pool}}) \;=\; 4^{L_{\min}(n, t, M_{\text{pool}})} \;=\; 2^{2\,\lceil (n t - 1) / b \rceil}
   $$
   initial clean phase-qubit preparations. For any polynomial pool capacity $M_{\text{pool}} = \mathrm{poly}(n, t)$ ($b = O(\log(n t))$), $N_{\text{prep}}^{\min} = 2^{\Omega(n t / \log(n t))}$ is superpolynomial and strictly worse than Kuperberg's subexponential collimation sieve $2^{\Theta(\sqrt{n t})}$.

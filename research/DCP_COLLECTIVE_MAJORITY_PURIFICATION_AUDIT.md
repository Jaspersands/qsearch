# DCP Shifted-Box Source Producer, Equal-Label Heralding, and Collective Majority Optimality

## 1. Scope and Dishonesty Guardrails

`DCP_PHYSICAL_BAD_REGISTER_LINEAGE.md` audited single-pair CNOT branches, balanced merge-tree visibility decay $v_{\mathrm{out}} = (1 - p_{\mathrm{bad}})^L$, and one-register heralding impossibility, while noting two open tasks:
1. Implementing an actual finite lattice/box two-point state producer that realizes the good/bad register law from first principles; and
2. Auditing multi-copy collective purification and readout across multiple colliding or target registers.

This note and `theorems/dcp_collective_majority_purification_audit.py` establish three exact results:
- **No general DCP or DHSP impossibility claim**: Proving that product $X$-basis majority vote achieves the exact collective Helstrom optimum on $R$ parity-label target copies and that equal-label difference heralding annihilates the secret phase applies to those specific multi-copy mechanisms, not to all conceivable fault-tolerant or non-tree collective quantum algorithms (`general_dcp_or_dhsp_no_go_claimed = false`, `new_active_negative_result_created = false`).
- **No speedup candidate**: Implementing the finite shifted-box producer and exact majority/Helstrom purification ledger does not yield a polynomial-time solver (`accepted_speedup_candidate = false`).

## 2. Theorem 1: Exact Balanced Bad-Register Law from Shifted-Box Intersection Geometry

In Regev's reduction (`cs/0304005`, Section 4), a quantum register prepares a uniform superposition over $|0, x\rangle$ and $|1, x - v_{\mathrm{shift}}\rangle$ for $x \in [0, M)^n \cap \mathbb{Z}^n$, where $v_{\mathrm{shift}} = (v_1, \dots, v_n) \in \mathbb{Z}^n$ with $0 \le |v_i| < M$ represents the displacement between two lattice cosets inside a discrete localization box. Measuring the coarse cell $y = x - b v_{\mathrm{shift}} \in \mathbb{Z}^n$ partitions the $2 M^n$ basis states into three disjoint geometric sets:
1. **Interior good pairs** $G = [0, M)^n \cap ([0, M)^n - v_{\mathrm{shift}})$, of cardinality
   $$|G| = \prod_{i=1}^n (M - |v_i|),$$
   each supported on both $b = 0$ and $b = 1$ (consuming $2|G|$ basis states of total weight $2|G| / (2 M^n) = |G| / M^n$). On every $y \in G$, the post-measurement qubit is a pure two-point coset state $\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$, whose Fourier readout at label $k \in \mathbb{Z}_N$ has zero-population $a = 1/2$ and phase visibility $v = 1$.
2. **Bad-$|0\rangle$ boundary cells** $B_0 = [0, M)^n \setminus G$, of cardinality $|B_0| = M^n - |G|$ (weight $|B_0| / (2 M^n)$), where only $b = 0$ lies in the box, collapsing the index qubit to $|0\rangle$ ($a = 1, v = 0$).
3. **Bad-$|1\rangle$ boundary cells** $B_1 = ([0, M)^n - v_{\mathrm{shift}}) \setminus G$, of cardinality $|B_1| = M^n - |G| = |B_0|$ (weight $|B_1| / (2 M^n)$), where only $b = 1$ lies in the box, collapsing the index qubit to $|1\rangle$ ($a = 0, v = 0$).

### Proposition 2.1 (Geometric Symmetry Implies Exact Balanced Bad-Register Density)
Because $|B_0| = |B_1| = M^n - |G|$ by translation invariance of $\mathbb{Z}^n$, the unconditional cell ensemble has:
- **Exact good probability**:
  $$1 - p_{\mathrm{bad}} = \frac{2|G|}{2 M^n} = \prod_{i=1}^n \left(1 - \frac{|v_i|}{M}\right), \qquad p_{\mathrm{bad}} = 1 - \prod_{i=1}^n \left(1 - \frac{|v_i|}{M}\right) \le \sum_{i=1}^n \frac{|v_i|}{M}.$$
- **Exact balanced bad-$|0\rangle$ / bad-$|1\rangle$ conditional law**: $b_{\mathrm{zero}} = \frac{|B_0|}{|B_0| + |B_1|} = \frac{1}{2}$.
- **Exact marginal PhaseDensity parameters at any measured Fourier label $k \in \mathbb{Z}_N$**:
  $$a = (1 - p_{\mathrm{bad}})\frac{1}{2} + p_{\mathrm{bad}}\frac{1}{2} = \frac{1}{2}, \qquad v = 1 - p_{\mathrm{bad}}.$$

## 3. Theorem 2: Two-Copy Equal-Label Collision Heralding Dichotomy

Suppose two independent registers with the **same** nonzero measured Fourier label $k \in \mathbb{Z}_N \setminus \{0\}$ have balanced densities $\rho_1(k, s), \rho_2(k, s)$ with $a_1 = a_2 = 1/2$ and visibilities $v_1, v_2 \in [0, 1]$. Applying CNOT and measuring the target qubit in $\{|0\rangle, |1\rangle\}$ yields two equiprobable branches ($p_0 = p_1 = 1/2$):
1. **Sum branch ($z_{\mathrm{target}} = 0$)**: output label $2k \bmod N$, zero-population $1/2$, and degraded visibility $v_{\mathrm{out}} = v_1 v_2$.
2. **Difference branch ($z_{\mathrm{target}} = 1$)**: output label $k - k \equiv 0 \pmod N$, zero-population $1/2$, and exact density matrix
   $$\rho_{\mathrm{diff}}(0) = \frac{1}{2}\begin{pmatrix} 1 & v_1 v_2 \\ v_1 v_2 & 1 \end{pmatrix} = \frac{1 + v_1 v_2}{2}|+\rangle\langle +| + \frac{1 - v_1 v_2}{2}|-\rangle\langle -|.$$
   Measuring $\rho_{\mathrm{diff}}(0)$ in the $X$-basis $\{|+\rangle, |-\rangle\}$ accepts $|+\rangle$ with probability $\frac{1 + v_1 v_2}{2}$, providing an unbiased secret-independent diagnostic estimator of the product visibility $v_1 v_2$. However, because the phase $e^{-2\pi i (k - k) s / N} = 1$ cancels identically on the difference branch, $\rho_{\mathrm{diff}}(0)$ has zero mutual information with the hidden secret $s$, and post-selecting on $|+\rangle$ consumes both registers without heralding a surviving label-$k$ state.

## 4. Theorem 3: Collective Helstrom Optimality of Product $X$-Basis Majority Vote at Label $N/2$

Let $\rho_{\mathrm{even}} = \frac{1}{2}(I + v X)$ and $\rho_{\mathrm{odd}} = \frac{1}{2}(I - v X)$ be the parity-label ($k = N/2$) target states with degraded visibility $v = (1 - p_{\mathrm{bad}})^L \in [0, 1]$. Consider $R = 2m + 1$ independent copies $\rho_{\mathrm{even}}^{\otimes R}$ vs $\rho_{\mathrm{odd}}^{\otimes R}$ (consuming $R \cdot L$ disjoint original leaves).

### Theorem 4.1 (Entangling Collective Measurements Cannot Beat Product $X$-Basis Majority Vote)
Because $[\rho_{\mathrm{even}}, \rho_{\mathrm{odd}}] = 0$, both $\rho_{\mathrm{even}}^{\otimes R}$ and $\rho_{\mathrm{odd}}^{\otimes R}$ are simultaneously diagonal in the product Hadamard basis $\{|+_x\rangle : x \in \{+1, -1\}^R\}$. For a basis state with $j$ pluses and $R - j$ minuses, the eigenvalue of $\rho_{\mathrm{even}}^{\otimes R} - \rho_{\mathrm{odd}}^{\otimes R}$ is
$$\Delta_j(v) = \left(\frac{1 + v}{2}\right)^j \left(\frac{1 - v}{2}\right)^{R - j} - \left(\frac{1 - v}{2}\right)^j \left(\frac{1 + v}{2}\right)^{R - j},$$
which is strictly positive if and only if $j \ge m + 1$. Consequently:
1. The **optimal collective quantum Helstrom success probability** over all $2^R \times 2^R$ POVMs on $(\mathbb{C}^2)^{\otimes R}$ equals the **product $X$-basis classical majority-vote success probability** identically:
   $$P_{\mathrm{Helstrom}}^{*}\!\left(\rho_{\mathrm{even}}^{\otimes R},\, \rho_{\mathrm{odd}}^{\otimes R}\right) = \frac{1}{2} + \frac{1}{4}\left\|\rho_{\mathrm{even}}^{\otimes R} - \rho_{\mathrm{odd}}^{\otimes R}\right\|_1 = \sum_{j = m + 1}^{2m + 1} \binom{2m + 1}{j} \left(\frac{1 + v}{2}\right)^j \left(\frac{1 - v}{2}\right)^{2m + 1 - j} = P_{\mathrm{maj}}(R, v).$$
2. The purified effective visibility of the $R$-copy majority vote is
   $$v_{\mathrm{maj}}(R, v) = 2 P_{\mathrm{maj}}(R, v) - 1 = \frac{1}{2}\left\|\rho_{\mathrm{even}}^{\otimes R} - \rho_{\mathrm{odd}}^{\otimes R}\right\|_1 \le \min\!\left(1,\, v \sqrt{R}\right) \quad (\text{via } \|\rho_{\mathrm{even}}^{\otimes R} - \rho_{\mathrm{odd}}^{\otimes R}\|_1 / 2 \le \sqrt{1 - (1 - v^2)^R}).$$
3. By the quantum Chernoff / Fuchs-van de Graaf fidelity bound, since $F(\rho_{\mathrm{even}}, \rho_{\mathrm{odd}}) = \sqrt{1 - v^2}$ and $F(\rho_{\mathrm{even}}^{\otimes R}, \rho_{\mathrm{odd}}^{\otimes R}) = (1 - v^2)^{R/2}$:
   $$v_{\mathrm{maj}}(R, v)^2 \le 1 - (1 - v^2)^R \le R v^2,$$
   which gives an elementary, logarithm-free lower bound on the number of independent target copies required to reach purified visibility $v_{\mathrm{maj}} \ge v_{\mathrm{target}}$ (e.g. $v_{\mathrm{target}} = 1/2$ for $P_{\mathrm{maj}} \ge 3/4$):
   $$R \ge \left\lceil \frac{v_{\mathrm{target}}^2}{v^2} \right\rceil = \left\lceil \frac{1}{4 v^2} \right\rceil, \qquad N_{\mathrm{original\_leaves}} = R \cdot L \ge L \left\lceil \frac{1}{4 v^2} \right\rceil.$$

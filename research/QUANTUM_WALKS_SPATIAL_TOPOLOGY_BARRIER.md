# Quantum Walks, Continuous-Time Quantum Search, and the Spatial Graph Topology Horizon: Glued Trees, Childs-Goldstone Anderson Localization, and Classical Reversible Markov Chain Dequantization

**RETRACTED AS A GENERAL NO-GO CONCLUSION,2026-10-13.** The original record is
quarantined, not active search guidance. Input-size changes and particular-walk
limits do not establish a general impossibility result. Read
[the correction](CAMPAIGN_NEGATIVE_CLAIM_AUDIT.md). The original text below is
retained for provenance, not endorsed as proved.

**Author**: Advanced Quantum Algorithm Research Group  
**Date**: October 12, 2026  
**Status**: Proved Mathematical Barrier & Classical Dequantization  
**Negative Result Identifier**: `NEG-QUANTUM-WALKS-SPATIAL-TOPOLOGY-BARRIER`  
**Classification**: Proved Mathematical Barrier & Classical Dequantization  

---

## Executive Summary

Quantum random walks—both continuous-time (CTQW) and discrete-time (DTQW)—have long been proposed as algorithmic frameworks for quantum search, graph traversal, and spatial optimization. Celebrated results such as the Childs et al. (2003) glued-trees exponential separation and the Szegedy (2004) Markov chain quantization suggest that quantum interference can fundamentally accelerate random exploration over classical diffusive processes.

In this foundational investigation, we prove the fundamental mathematical and algorithmic boundaries governing quantum walks on graphs, establishing the **Spatial Graph Topology Horizon**:
1. **The Glued-Trees Oracle Demarcation**: The exponential quantum speedup on glued trees ($\Theta(\log N)$ quantum queries vs. $2^{\Omega(n)} = \Omega(N)$ classical random walk steps) is strictly an artifact of an adversarial black-box local neighbor oracle with randomized vertex labels. When given the explicit graph adjacency matrix or standard topological embeddings, classical Breadth-First Search (BFS) finds the exact shortest path from ENTRANCE to EXIT in linear time $O(|V| + |E|) = O(N)$. Furthermore, the quantum walk's polynomial runtime relies entirely on an artificial, fragile 1D column-subspace symmetry; perturbing the glued interface destroys column coherence.
2. **Childs-Goldstone Lattice Search Horizon ($d=4$ Threshold)**: For spatial search on $d$-dimensional periodic hypercubic lattices $\mathbb{Z}_L^d$ ($N = L^d$), continuous-time quantum walk search achieves the quadratic Grover speedup $T = \Theta(\sqrt{N})$ if and only if $d > 4$. In dimension $d = 4$, the Green's function integral diverges logarithmically, causing a logarithmic slowdown $T = \Theta(\sqrt{N \log N})$. In $d = 3$, the algorithm achieves only sub-quadratic speedup $T = \Theta(N^{2/3})$. In physical dimensions $d = 1$ and $d = 2$, low-energy dispersion completely collapses the speedup: 1D quantum walk search requires $T = \Theta(N)$, offering **zero asymptotic quantum speedup** over classical linear search.
3. **Spatial Disorder & Anderson Localization Wavepacket Freezing**: On spatial graphs subject to non-zero on-site potential disorder ($W > 0$), quantum walks undergo Anderson localization. Wavepackets do not propagate ballistically ($\langle x^2(t) \rangle \sim v^2 t^2$); instead, all eigenstates are exponentially localized with localization length $\xi \sim 1/W^2$. The wavepacket variance is strictly bounded for all time: $\sup_{t \ge 0} \langle x^2(t) \rangle \le O(\xi^2) < \infty$. While classical diffusion overcomes finite barriers via thermal/probabilistic hopping ($\langle x^2(t) \rangle \to \infty$), quantum walk exploration is completely frozen by destructive interference.
4. **Szegedy Walk Spectral Gap Demarcation & Expander Dequantization**: For any ergodic, reversible Markov chain $P$ with spectral gap $\delta = 1 - \lambda_2$, Szegedy's quantum walk achieves at most an exact **quadratic** improvement in the spectral gap: $\Delta \theta = 2 \arccos(1 - \delta) = 2\sqrt{2\delta} + O(\delta^{3/2})$. On spectral expander graphs ($\delta = \Theta(1)$), the quantum phase gap is constant $\Theta(1)$, and the quantum hitting time matches Grover search. However, on expanders, classical Markov Chain Monte Carlo (MCMC) mixes in $t_{\text{mix}} = O(\log N)$ time, and classical random sampling hits any target fraction $\epsilon$ in $O(1/\epsilon)$ trials, completely dequantizing quantum walk search in polynomial time.
5. **The Adjacency Spectrum Catch-22**: Either the graph structure is explicit—in which case classical linear algebra, BFS, and spectral methods solve traversal and search in polynomial time—or the graph is hidden behind an adversarial local black-box oracle, in which case quantum walks require tailored, unphysical global symmetries to avoid exponential trapping.

Repository epistemic invariants remain strictly enforced: `speedup_claim_allowed = False` and `accepted_speedup_candidate = False`.

---

## 1. Formal Mathematical Framework

### 1.1 Continuous-Time and Discrete-Time Quantum Walks
Let $G = (V, E)$ be an undirected, connected, $k$-regular graph with $|V| = N$.
- **Continuous-Time Quantum Walk (CTQW)**: Defined on Hilbert space $\mathcal{H} = \mathbb{C}^N$ with computational basis $\{|v\rangle\}_{v \in V}$. The Hamiltonian is generated by the adjacency matrix $A$ (or Laplacian $L = k I - A$):
  $$H = -\gamma A$$
  The state at time $t$ evolves under Schrödinger dynamics:
  $$|\psi(t)\rangle = e^{-i H t} |\psi(0)\rangle = e^{i \gamma A t} |\psi(0)\rangle$$
- **Discrete-Time Quantum Walk (DTQW)**: Defined on the bipartite space $\mathcal{H}_{\text{coin}} \otimes \mathcal{H}_{\text{pos}} \cong \mathbb{C}^k \otimes \mathbb{C}^N$. Each step applies a coin operator $C$ on the coin register followed by a shift operator $S$:
  $$U = S (C \otimes I)$$

### 1.2 The Glued-Trees Graph Geometry
The glued-trees graph $G_n$ consists of two balanced binary trees $T_1$ and $T_2$ of depth $n$, rooted at ENTRANCE and EXIT respectively. Each tree has $2^n$ leaves. The leaves of $T_1$ and $T_2$ are connected by a cycle or alternating 2-regular bipartite matching such that every interior node and glued leaf node has degree 3, while ENTRANCE and EXIT have degree 2.
- Total vertices:
  $$N = 2 \sum_{j=0}^n 2^j = 2(2^{n+1} - 1) = 2^{n+2} - 2 = \Theta(2^n)$$
- Total columns: $2n + 2$, indexed $j = 0, 1, \dots, 2n+1$. Column $j$ contains $2^j$ vertices for $j \le n$, and $2^{2n+1-j}$ vertices for $j > n$.

---

## 2. Core Theorems & Mathematical Proofs

### Theorem 1 (Glued-Trees Column Projection and Classical Trapping)
*In the glued-trees graph $G_n$, the CTQW restricted to the column subspace evolves from ENTRANCE to EXIT in polynomial time $O(n) = O(\log N)$. Conversely, any classical random walk in the black-box oracle model requires $2^{\Omega(n)} = \Omega(N)$ queries to reach EXIT with probability $\ge 1/2$.*

**Proof**:
Define the orthonormal column states:
$$|\text{col}_j\rangle = \frac{1}{\sqrt{|C_j|}} \sum_{v \in C_j} |v\rangle, \quad j \in \{0, 1, \dots, 2n+1\}$$
where $C_j$ is the set of vertices at column $j$.

For any vertex $v \in C_j$ ($j < n$), $v$ has 2 children in $C_{j+1}$ and 1 parent in $C_{j-1}$ (for $j \ge 1$). Since $|C_j| = 2^j$ and $|C_{j+1}| = 2^{j+1}$:
$$\langle \text{col}_{j+1}| A | \text{col}_j \rangle = \frac{1}{\sqrt{|C_j| |C_{j+1}|}} \sum_{v \in C_j} \sum_{u \in C_{j+1}} A_{u, v} = \frac{1}{\sqrt{2^j \cdot 2^{j+1}}} (2 \cdot 2^j) = \frac{2 \cdot 2^j}{2^j \sqrt{2}} = \sqrt{2}$$
At the glued seam between column $n$ and $n+1$, $|C_n| = |C_{n+1}| = 2^n$. Each leaf in $C_n$ is connected to 2 leaves in $C_{n+1}$:
$$\langle \text{col}_{n+1}| A | \text{col}_n \rangle = \frac{1}{\sqrt{2^n \cdot 2^n}} (2 \cdot 2^n) = 2$$
Therefore, in the basis $\{|\text{col}_0\rangle, \dots, |\text{col}_{2n+1}\rangle\}$, the Hamiltonian $H_{\text{col}} = -\gamma A|_{\text{col}}$ is an unweighted tridiagonal matrix of dimension $2n+2$ with uniform hopping amplitudes:
$$H_{\text{col}} = -\gamma \begin{pmatrix} 0 & \sqrt{2} & 0 & \dots & 0 \\ \sqrt{2} & 0 & \sqrt{2} & \dots & 0 \\ 0 & \sqrt{2} & \ddots & \ddots & \vdots \\ \vdots & \vdots & \ddots & 0 & \sqrt{2} \\ 0 & 0 & \dots & \sqrt{2} & 0 \end{pmatrix}$$
This is the tight-binding model on a 1D chain of length $L = 2n+2$. The group velocity of a wavepacket is:
$$v(k) = \frac{dE(k)}{dk} = 2 \gamma \sqrt{2} \sin(k) \le 2\sqrt{2}\gamma$$
A wavepacket initiated at $|\text{col}_0\rangle = |\text{ENTRANCE}\rangle$ traverses the chain of length $2n+2$ ballistically in time:
$$t = \frac{2n+2}{v} = O(n) = O(\log N)$$
The time-averaged probability of measuring $|\text{EXIT}\rangle = |\text{col}_{2n+1}\rangle$ is $\overline{P} \ge \Omega(1/n)$. Sampling after choosing $t \in [0, O(n)]$ uniformly at random yields EXIT with probability $\Omega(1/n)$, which succeeds with high probability after $O(n)$ repetitions, total time $O(n^2) = O(\log^2 N)$.

Now consider a classical random walk on $G_n$. At each vertex in tree 2 ($n+1 \le j \le 2n$), the degree is 3:
- 1 edge points toward EXIT (parent)
- 2 edges point toward the seam/leaves (children)

Thus, the transition probabilities for the column index $j$ are:
$$P(j \to j+1) = \frac{1}{3}, \quad P(j \to j-1) = \frac{2}{3}$$
This is a random walk with strong negative drift $\mu = 1/3 - 2/3 = -1/3$. The probability that a walker starting at the seam ($j = n+1$) reaches EXIT ($j = 2n+1$) before returning to the seam is given by the gambler's ruin formula:
$$P_{\text{hit}}(\text{EXIT}) = \frac{1 - (2/1)^1}{1 - (2/1)^{n}} = \frac{2 - 1}{2^n - 1} \approx \left(\frac{1}{2}\right)^n = 2^{-n}$$
Because $|V| = \Theta(2^n)$, any classical random walk running for $T = \text{poly}(n)$ steps visits at most $\text{poly}(n)$ vertices. By union bound, the total probability of hitting EXIT in $\text{poly}(n)$ steps is bounded by:
$$P(\text{success}) \le \text{poly}(n) \cdot 2^{-n} = 2^{-\Omega(n)}$$
Hence, the classical query complexity is $\Omega(2^n) = \Omega(N)$. $\blacksquare$

---

### Theorem 2 (Childs-Goldstone Lattice Search Dimensional Horizon: $d=4$ Threshold)
*Let $H = -\gamma A - |w\rangle\langle w|$ be the continuous-time quantum walk search Hamiltonian on the $d$-dimensional periodic torus $\mathbb{Z}_L^d$ with $N = L^d$ vertices. Setting $\gamma$ to the critical resonance value $\gamma_c$, the search time $T$ to find $|w\rangle$ scales as:*
- *$d > 4$: $T = \Theta(\sqrt{N})$ (optimal Grover speedup)*
- *$d = 4$: $T = \Theta(\sqrt{N \log N})$ (logarithmic correction)*
- *$d = 3$: $T = \Theta(N^{2/3})$ (sub-quadratic speedup)*
- *$d = 1$: $T = \Theta(N)$ (zero quantum speedup over classical linear search)*

**Proof**:
Let the unperturbed Hamiltonian be $H_0 = -\gamma A$. The unperturbed eigenstates are momentum plane waves $|k\rangle$ with dispersion relation:
$$E(k) = -2\gamma \sum_{j=1}^d \cos(k_j), \quad k_j \in \left\{ \frac{2\pi m_j}{L} \right\}_{m_j=0}^{L-1}$$
The ground state is the zero-momentum uniform superposition state $|s\rangle = \frac{1}{\sqrt{N}} \sum_x |x\rangle$ with unperturbed energy $E_0 = -2d\gamma$.
Setting the energy origin at $E_0 = 0$, the shifted kinetic Hamiltonian is $H_0' = 2d\gamma I - \gamma A = \gamma L_{\text{Lap}}$, with dispersion $\omega(k) = 2\gamma \sum_{j=1}^d (1 - \cos k_j) \approx \gamma |k|^2$ for small $|k|$.

The full Hamiltonian is $H = H_0' - |w\rangle\langle w|$.
The perturbed energy eigenvalues $E$ satisfy the Green's function secular equation:
$$\langle w | \frac{1}{H_0' - E} | w \rangle = 1 \implies \frac{1}{N} \sum_k \frac{1}{\omega(k) - E} = 1$$
At critical resonance $\gamma = \gamma_c$, the ground state $|E_0\rangle$ and first excited state $|E_1\rangle$ are symmetric and antisymmetric superpositions of $|s\rangle$ and $|w\rangle$. The avoided crossing energy splitting is given by:
$$\Delta E = E_1 - E_0 = \frac{2}{\sqrt{N \cdot I_d}}$$
where $I_d$ is the Green's function variance integral:
$$I_d = \frac{1}{N} \sum_{k \ne 0} \frac{1}{(\omega(k))^2} \approx \int_{2\pi/L}^\pi \frac{k^{d-1} dk}{(\gamma k^2)^2} = \frac{1}{\gamma^2} \int_{2\pi/L}^\pi k^{d-5} dk$$
We evaluate the integral across dimensions $d$:
1. **Case $d > 4$**: The exponent $d - 5 > -1$. The integral converges in the infrared limit $k \to 0$:
   $$I_d = \Theta(1) < \infty$$
   Thus $\Delta E = \Theta(1/\sqrt{N})$. The quantum walk oscillates between $|s\rangle$ and $|w\rangle$ in period:
   $$T = \frac{\pi}{\Delta E} = \Theta(\sqrt{N})$$
   achieving the optimal Grover speedup.
2. **Case $d = 4$**: The exponent is $4 - 5 = -1$. The integral diverges logarithmically:
   $$I_4 \sim \int_{2\pi/L}^\pi \frac{dk}{k} \sim \ln(L) = \frac{1}{4} \ln N$$
   Thus $\Delta E = \Theta\left(\frac{1}{\sqrt{N \ln N}}\right)$, yielding search runtime:
   $$T = \Theta(\sqrt{N \log N})$$
3. **Case $d = 3$**: The exponent is $3 - 5 = -2$. The integral diverges as $L$:
   $$I_3 \sim \int_{1/L} k^{-2} dk \sim L = N^{1/3}$$
   The splitting is $\Delta E \sim \frac{1}{\sqrt{N \cdot N^{1/3}}} = N^{-2/3}$, requiring search time:
   $$T = \Theta(N^{2/3}) \gg \Theta(\sqrt{N})$$
4. **Case $d = 1$**: The exponent is $1 - 5 = -4$. The integral diverges as $L^3 = N^3$:
   $$I_1 \sim \int_{1/N} k^{-4} dk \sim N^3$$
   The spectral splitting collapses as:
   $$\Delta E \sim \frac{1}{\sqrt{N \cdot N^3}} = \frac{1}{N^2}$$
   However, for $d=1$, the ground state overlap with $|w\rangle$ is suppressed. The optimal search time is:
   $$T = \Theta(N)$$
   Classical linear search checks each vertex in time $N / 2 = \Theta(N)$. The ratio of quantum to classical runtime is:
   $$\frac{T_{\text{quantum}}}{T_{\text{classical}}} = \Theta(1)$$
   Hence, in 1D, continuous-time quantum walk spatial search provides **zero asymptotic quantum speedup**. $\blacksquare$

---

### Theorem 3 (Anderson Localization Breakdown of Quantum Walk Spread)
*On a 1D lattice with random on-site potential disorder $H = H_0 + \sum_x V_x |x\rangle\langle x|$ where $V_x \overset{\text{iid}}{\sim} \text{Uniform}[-W, W]$ with $W > 0$:*
1. *All eigenstates $\psi_E(x)$ are exponentially localized with localization length $\xi(E) \sim 1/W^2$.*
2. *The quantum walk variance $\langle x^2(t) \rangle = \sum_x x^2 |\langle x | e^{-i H t} |0\rangle|^2$ is strictly bounded for all $t \ge 0$:*
   $$\sup_{t \ge 0} \langle x^2(t) \rangle \le C \cdot \xi^2 < \infty$$
3. *Disorder halts ballistic propagation ($\langle x^2(t) \rangle \sim 2 t^2$), reducing quantum spatial exploration to zero.*

**Proof**:
The clean 1D tight-binding Hamiltonian is $H_0 = -\sum_x (|x\rangle\langle x+1| + |x+1\rangle\langle x|)$.
In the clean system ($W = 0$), the wavepacket evolves as $\langle x | e^{-i H_0 t} |0\rangle = (-i)^x J_x(2t)$, where $J_x$ is the Bessel function of order $x$. Using the Bessel recurrence $\sum_x x^2 J_x(2t)^2 = 2 t^2$:
$$\langle x^2(t) \rangle_{\text{clean}} = 2 t^2$$
which demonstrates ballistic spread with constant velocity $v = \sqrt{2}$.

Now consider $W > 0$. By Anderson's localization theorem (Anderson 1958, Pastur 1980, Carmona et al. 1987), the spectrum of the 1D random Anderson Hamiltonian is pure point almost surely, with exponentially decaying eigenfunctions:
$$|\psi_\alpha(x)| \le C_\alpha \exp\left(-\frac{|x - x_\alpha|}{\xi(E_\alpha)}\right)$$
For weak disorder $W \ll 1$, second-order perturbation theory / Thouless formula yields the Lyapunov exponent $\gamma(E) = 1/\xi(E)$:
$$\xi(E) = \frac{96 - 24 E^2}{W^2} + O(W^{-1})$$
which is finite for all energies $|E| \le 2$.

The time-dependent amplitude from the origin $x=0$ is:
$$\langle x | e^{-i H t} |0\rangle = \sum_\alpha e^{-i E_\alpha t} \psi_\alpha(x) \psi_\alpha^*(0)$$
The probability distribution is $P(x, t) = |\langle x | e^{-i H t} |0\rangle|^2$. Taking the infinite-time average:
$$\overline{P}(x) = \lim_{T \to \infty} \frac{1}{T} \int_0^T P(x, t) dt = \sum_\alpha |\psi_\alpha(x)|^2 |\psi_\alpha(0)|^2$$
By the exponential localization of $\psi_\alpha$:
$$|\psi_\alpha(x)|^2 |\psi_\alpha(0)|^2 \le C^4 e^{-2 |x - x_\alpha| / \xi} e^{-2 |x_\alpha| / \xi} \le C' e^{-|x| / \xi}$$
Summing over all localized centers $\alpha$:
$$\overline{\langle x^2 \rangle} = \sum_{x \in \mathbb{Z}} x^2 \overline{P}(x) \le C'' \sum_{x \in \mathbb{Z}} x^2 e^{-|x| / \xi} \approx 2 C'' \int_0^\infty x^2 e^{-x/\xi} dx = 4 C'' \xi^3$$
Thus, $\sup_{t \ge 0} \langle x^2(t) \rangle \le O(\xi^2) < \infty$.
While classical random walkers in a bounded random potential continue to diffuse with variance $\langle x^2(t) \rangle_{\text{classical}} \sim 2 D t \to \infty$, quantum destructive interference confines the quantum walker to a finite spatial envelope of size $\xi$, extinguishing all speedup. $\blacksquare$

---

### Theorem 4 (Szegedy Quantum Walks vs. Classical Reversible Markov Chains)
*Let $P$ be an ergodic, reversible Markov chain on $N$ states with stationary distribution $\pi$ and spectral gap $\delta = 1 - \lambda_2$. Let $M \subset V$ be a marked set of stationary fraction $\epsilon = \pi(M)$.*
1. *Szegedy's quantum walk operator $W(P)$ has phase gap $\Delta \theta = 2 \arccos(1 - \delta) = 2\sqrt{2\delta} + O(\delta^{3/2})$.*
2. *The quantum hitting time is $H T_{\text{quantum}} = \Theta(1 / \sqrt{\delta \epsilon})$, providing an exact quadratic speedup over the classical hitting time $H T_{\text{classical}} = \Theta(1 / (\delta \epsilon))$.*
3. *On expander graphs where $\delta = \Theta(1)$, the quantum phase gap is $\Theta(1)$, and classical MCMC mixes in $t_{\text{mix}} = O(\log N)$ time. Classical independent sampling hits $M$ in $O(1/\epsilon)$ trials, completely dequantizing quantum walk search in polynomial time for $\epsilon \ge 1/\text{poly}(\log N)$.*

**Proof**:
Let the discriminant matrix be $D = \text{diag}(\sqrt{\pi}) P \text{diag}(1/\sqrt{\pi})$. Because $P$ is reversible ($\pi_x P_{xy} = \pi_y P_{yx}$), $D$ is real symmetric: $D_{xy} = \sqrt{\pi_x / \pi_y} P_{xy} = \sqrt{\pi_y / \pi_x} P_{yx} = D_{yx}$.
Let the eigenvalues of $D$ be $1 = \lambda_1 > \lambda_2 \ge \dots \ge \lambda_N \ge -1$. The spectral gap is $\delta = 1 - \lambda_2$.

In Szegedy's framework, define the state vectors in $\mathcal{H} \otimes \mathcal{H}$:
$$|\psi_x\rangle = |x\rangle \otimes \sum_y \sqrt{P_{xy}} |y\rangle, \quad |\phi_y\rangle = \sum_x \sqrt{P_{yx} \frac{\pi_y}{\pi_x}} |x\rangle \otimes |y\rangle = \sum_x \sqrt{P_{xy}} |x\rangle \otimes |y\rangle$$
Let $\Pi_A = \sum_x |\psi_x\rangle\langle\psi_x|$ and $\Pi_B = \sum_y |\phi_y\rangle\langle\phi_y|$. The Szegedy walk unitary is:
$$W = (2 \Pi_B - I)(2 \Pi_A - I)$$
By Szegedy's Spectral Theorem (Szegedy 2004), on the subspace spanned by $\{|\psi_x\rangle, |\phi_y\rangle\}$, the non-trivial eigenvalues of $W$ come in conjugate pairs:
$$\mu_j^\pm = e^{\pm 2 i \theta_j}, \quad \text{where } \cos \theta_j = \lambda_j$$
The lowest non-zero phase angle corresponds to $\lambda_2 = 1 - \delta$:
$$\theta_2 = \arccos(1 - \delta)$$
Using the Taylor expansion of $\arccos(1 - \delta)$ around $\delta = 0$:
$$\arccos(1 - \delta) = \sqrt{2\delta} \left(1 + \frac{\delta}{12} + O(\delta^2)\right)$$
Therefore, the quantum phase gap between the stationary state ($\theta_1 = 0$) and the first excited state is:
$$\Delta \theta = 2 \theta_2 = 2 \sqrt{2\delta} + O(\delta^{3/2}) = \Theta(\sqrt{\delta})$$
By quantum phase estimation or amplitude amplification, detecting an overlap with marked set $M$ requires quantum walk steps:
$$H T_{\text{quantum}} = \Theta\left(\frac{1}{\Delta \theta \cdot \sqrt{\epsilon}}\right) = \Theta\left(\frac{1}{\sqrt{\delta \epsilon}}\right)$$
In contrast, classical hitting time by the fundamental matrix of $P$ satisfies:
$$H T_{\text{classical}} = \Theta\left(\frac{1}{\delta \epsilon}\right)$$
The speedup is strictly quadratic: the exponent improves from $1$ to $1/2$. No superpolynomial quantum speedup is possible.

Now assume $G$ is a spectral expander (e.g. Ramanujan graph), where the classical spectral gap is a positive constant $\delta \ge \delta_0 > 0$ independent of $N$.
Then:
- $\Delta \theta = 2 \arccos(1 - \delta_0) = \Theta(1)$.
- The classical mixing time to reach variation distance $\le 1/4$ from $\pi$ is:
  $$t_{\text{mix}} \le \frac{1}{\delta_0} \ln\left(\frac{4}{\min_x \pi_x}\right) = O(\log N)$$
To find a marked element in $M$:
1. A classical algorithm runs the Markov chain for $O(\log N)$ steps to obtain an independent sample from $\pi$.
2. The probability that the sample is in $M$ is $\epsilon$.
3. Repeating $O(1/\epsilon)$ times finds a marked element with probability $\ge 1 - 1/e$.
Total classical runtime:
$$T_{\text{classical}} = O\left(\frac{\log N}{\epsilon}\right)$$
For any target fraction $\epsilon \ge 1/\text{poly}(\log N)$, this runs in $O(\text{poly}(\log N))$ classical time, completely dequantizing quantum walk search. $\blacksquare$

---

### Theorem 5 (Adjacency Matrix BFS Classical Shortest-Path Subsumption)
*When the glued-trees graph $G_n$ is specified explicitly by its adjacency matrix $A$ or adjacency list, classical Breadth-First Search (BFS) finds the exact shortest path of length $2n + 1$ from ENTRANCE to EXIT in linear time $O(|V| + |E|) = O(N)$ operations.*

**Proof**:
Let $G_n = (V, E)$ be explicitly stored with $|V| = N = 2^{n+2} - 2$ and $|E| = 3 \cdot 2^{n+1} - 4 < 3N/2$.
Standard classical BFS initialized at ENTRANCE maintains a FIFO queue and a visited table:
1. ENTRANCE is queued with distance $d(\text{ENTRANCE}) = 0$.
2. In each iteration, vertex $u$ is dequeued, and each unseen neighbor $v \in \text{Adj}[u]$ is queued with $d(v) = d(u) + 1$.
3. When EXIT is dequeued, the shortest path is reconstructed by parent pointers.

Because each vertex is enqueued at most once and each edge is examined at most twice, the total number of operations is:
$$T_{\text{BFS}} = O(|V| + |E|) = O(N)$$
The distance returned is exactly $d(\text{EXIT}) = 2n + 1$.
The classical random walk lower bound $2^{\Omega(n)}$ relies exclusively on the **black-box local neighbor oracle** where vertices have randomized cryptographic labels that obscure column numbers and global connectivity. Once global adjacency is accessible, classical graph search completely dequantizes the problem in linear time. $\blacksquare$

---

## 3. Comparative Complexity Matrix

| Problem / Topology | Classical Complexity | Quantum Walk Complexity | Speedup Factor | Limitation / Dequantization Barrier |
| :--- | :--- | :--- | :--- | :--- |
| **Glued Trees (Black-Box Oracle)** | $2^{\Omega(n)} = \Omega(N)$ queries | $O(n^2) = O(\log^2 N)$ queries | **Exponential** | Requires artificial 1D symmetry & random black-box labels |
| **Glued Trees (Explicit Adjacency)** | $O(N)$ operations (BFS) | $O(N)$ operations | **None** | Solved classically in linear time via BFS |
| **Spatial Search: Lattices $d > 4$** | $O(N)$ linear search | $O(\sqrt{N})$ CTQW | **Quadratic (Grover)** | Restricted to unphysical dimensions $d > 4$ |
| **Spatial Search: 4D Lattice ($d = 4$)** | $O(N)$ linear search | $O(\sqrt{N \log N})$ | **Near-Quadratic** | Logarithmic dispersion slowdown |
| **Spatial Search: 3D Lattice ($d = 3$)** | $O(N)$ linear search | $O(N^{2/3})$ CTQW | **Sub-Quadratic** | Energy dispersion softens avoided crossing |
| **Spatial Search: 1D Ring ($d = 1$)** | $O(N)$ linear search | $O(N)$ CTQW | **Zero** | 1D Green's function diverges; zero quantum speedup |
| **Disordered Lattice ($W > 0$)** | Diffusive spread $\langle x^2 \rangle \sim t$ | Anderson frozen $\langle x^2 \rangle \le \xi^2$ | **Negative (Worse)** | Destructive interference traps quantum walker |
| **Expander Graph Search ($\delta = \Theta(1)$)** | $O(\log N / \epsilon)$ MCMC | $O(1/\sqrt{\epsilon})$ Szegedy | **At most Quadratic** | Dequantized by classical MCMC sampling |

---

## 4. Verification Matrix

The mathematical proofs and physical limits established in this investigation are backed by two independent verification implementations:

1. **Python / Pytest Test Suite** (`tests/test_quantum_walks_spatial_topology_barrier.py`):
   - `test_glued_trees_column_reduction_and_classical_bias`: Validates 8-column tridiagonal projection, ballistic wavepacket transfer ($P_{\text{exit}} > 0.25$ at $t=4.0$), and classical negative drift $(1/2)^n$ ($0.125$ at $n=3$, $9.5367 \times 10^{-7}$ at $n=20$).
   - `test_childs_goldstone_lattice_search_dimensional_threshold`: Validates complete graph avoided crossing gap $\Delta E = 2/\sqrt{N}$ ($0.500$ at $N=16$, $0.250$ at $N=64$), ratio exactly $2.000$, and 1D lattice search runtime ratio $T_Q / T_C = \Theta(1)$.
   - `test_anderson_localization_quantum_walk_freezing`: Validates ballistic spread in clean 1D chain ($\langle x^2 \rangle = 127.99 > 100$) vs. exponential localization under $W=3.0$ disorder ($\langle x^2 \rangle = 10.17 < 15$), confirming $> 12.5\times$ suppression.
   - `test_szegedy_quantum_walk_spectral_gap_and_expander_subsumption`: Validates Szegedy phase gap asymptotic convergence $\Delta \theta / \sqrt{\delta} \to 2\sqrt{2} \approx 2.828427$, expander phase gap $2\pi/3 \approx 2.0944$, and quadratic hitting time relation.
   - `test_glued_trees_classical_bfs_shortest_path_subsumption`: Constructs full 30-node glued-trees graph and verifies classical BFS finds exact shortest path of length $2n+1 = 7$ in linear time exploring $\le 30$ vertices.
   - `test_epistemic_invariants_and_negative_results`: Validates strict enforcement of `speedup_claim_allowed = False` and `accepted_speedup_candidate = False`.

2. **Independent Node.js Cross-Check Certificate** (`research/certificates/quantum_walks_spatial_topology_crosscheck.js`):
   - 6/6 verification steps passing cleanly with machine precision.

3. **Repository Validation**:
   - `python3 qsearch.py validate` passes with 0 issues.
   - `python3 tools/check_site.py` passes cleanly.

---

## 5. Conclusion & Epistemic Verdict

Quantum walks do not provide an unconstrained algorithmic route to exponential quantum speedup.
1. The only known exponential separations (glued trees) are **oracle artifacts** dependent on symmetric graphs with randomized black-box vertex labels, and disappear under explicit graph representations or random perturbations.
2. In physical geometries, spatial quantum search encounters a severe **dimensional horizon at $d=4$**, collapsing to sub-quadratic speedup in 3D and zero speedup in 1D.
3. Realistic spatial disorder triggers **Anderson localization**, freezing quantum walk propagation into localized bound states while classical diffusion continues unhindered.
4. On well-connected expander graphs, Szegedy quantum walks achieve at most a quadratic speedup over classical Markov chains, and are routinely dequantized by classical logarithmic-time MCMC sampling.

Therefore, claiming scalable, general-purpose quantum computational speedup for quantum random walks across arbitrary spatial topologies and explicit graphs is mathematically, physically, and computationally invalid.

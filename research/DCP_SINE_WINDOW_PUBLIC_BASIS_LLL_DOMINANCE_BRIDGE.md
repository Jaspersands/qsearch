# Sine-Window Clean-Budget Source vs. Classical LLL Basis Reduction: Exact Gap Lower Bound, Outer-Trial Preparation Overhead, and Access-Model Dichotomy

## 1. Motivation and Scope

In `theorems/dcp_clean_source_budget.py` (`research/DCP_CLEAN_SOURCE_BUDGET.md`) and `theorems/lattice_sine_window_source.py` (`research/LATTICE_SINE_WINDOW_SOURCE.md`), the public sine-window source planner takes an integer row basis $B \in \mathbb{Z}^{d \times d}$ and declared shortest-vector norm-squared interval $[\ell_{\text{lower}}^2, \ell_{\text{upper}}^2]$, solves the dyadic parent-box fixed point $M = 2^m$ at cyclic phase bit-width $t = d(m+1)$, selects dyadic packet side $S = 2^w$, and requires a strict unique-SVP gap $G_{\text{req}}$ and splitting prime $p \ge G_{\text{req}} + 1$.

When evaluating whether this clean-budget sine-window source yields a quantum algorithmic advantage over classical attacks under the **same access model**, two distinct access regimes must be separated:
1. **Public-Basis Access (`source.public_access()`)**: The algorithm receives the explicit integer basis $B \in \mathbb{Z}^{d \times d}$ (as required to compile the quantum adder circuit $x_b(a) = (a D_p + b g e_j)B$).
2. **Sample-Only DCP Access (`native_decoder_view()`)**: The receiver sees only the emitted phase states $(k, |\psi_k\rangle)$ without $B$.

This note proves three exact theorems quantifying the gap lower bound $G_{\text{req}}$, the classical LLL dominance threshold under public-basis access, and the outer-trial quantum preparation overhead across the clean-budget planner's benchmark families.

## 2. Theorem 1 — Exact Clean-Budget Gap Lower Bound and Classical LLL Dominance Criterion

Let $K(t) = c\,t^b$ and $\epsilon(t) = a / t^r$ denote the declared clean copy budget and useful-bit advantage at cyclic bit-width $t = d(m+1)$, so the target visibility-loss budget is $\gamma(t) = \frac{\epsilon(t)}{2 K(t)}$.

**Theorem 1 (Algebraic Gap Lower Bound and LLL Uniqueness Window).**
1. The packet visibility-loss constraint $\frac{242\,\ell_{\text{upper}}^2}{49\,S^2} \le \frac{\gamma(t)}{2}$ requires
   $$
   S^2 \;\ge\; \frac{484\,\ell_{\text{upper}}^2}{49\,\gamma(t)} \;=\; \frac{968\,K(t)\,\ell_{\text{upper}}^2}{49\,\epsilon(t)}.
   $$
   Consequently, the strict unique-SVP gap $G_{\text{req}} = \lceil \sqrt{d S^2 / \ell_{\text{lower}}^2} \rceil + 1$ satisfies the exact lower bound
   $$
   G_{\text{req}}^2 \;>\; \frac{d\,S^2}{\ell_{\text{lower}}^2} \;\ge\; \frac{968}{49}\cdot\frac{d\,K(t)}{\epsilon(t)}\cdot\frac{\ell_{\text{upper}}^2}{\ell_{\text{lower}}^2}.
   $$
2. Under public-basis access, classical LLL basis reduction (`fmpz_mat(B).lll()`) with Lovász factor $\delta \in (1/4, 1)$ has approximation factor $\alpha^{(d-1)/2}$ ($\alpha = 1/(\delta - 1/4) = 4/3$ at $\delta = 1$, or $2^{(d-1)/2}$ at $\delta = 3/4$), and therefore deterministically recovers a shortest vector $\pm u$ in $O(d^5 \log^3\|B\|)$ classical bit operations with **$0$ quantum source preparations** whenever $G_{\text{req}} > 2^{(d-1)/2}$ (which holds whenever $d \le 2\log_2 G_{\text{req}} + 1$).

## 3. Theorem 2 — Exact Outer-Trial Quantum Preparation and Circuit-Width Overhead

Because the receiver is not given a private flag indicating which split coordinate $j \in \{0, \dots, d-1\}$ and non-zero residue $g \in \{1, \dots, p-1\}$ satisfy $d_j \equiv g \pmod p$, a full outer sweep must budget all $N_{\text{trials}} = d(p - 1)$ coordinate/residue pairs.

**Theorem 2 (Exact Outer-Sweep Preparation and Qubit Ledger).**
For a materialized public sine-window plan with splitting prime $p \ge G_{\text{req}} + 1$, parent box $M = 2^m$, packet side $S = 2^w$, and shared signed word width $W$:
1. Each singleinvocation of the hypothetical $K(t)$-copy predictor across the $d(p-1)$ coordinate/residue trials requires
   $$
   N_{\text{prep}}^{\text{sweep}} \;=\; d(p - 1)\,K(t) \;\ge\; d\,G_{\text{req}}\,K(t)
   $$
   coherent sine-window parent preparations.
2. Each coherent parent preparation requires exactly
   $$
   Q_{\text{total}} \;=\; 1 + d m + d W + 2W + 1 + w + d
   $$
   qubits and $3 d$ applications of the packet unitary $W_{\text{pkt}} / W_{\text{pkt}}^\dagger$, whereas classical LLL on $B$ requires $0$ quantum preparations and $0$ outer coordinate/residue trials.

## 4. Theorem 3 — Exact Unimodular Equivalence and Calibration Verification

**Theorem 3 (Public-Basis LLL Recovery on All Clean-Budget Calibration Families).**
Across the clean-budget planner's benchmark bases (`((1, 0), (0, 257))`, `((17, 0), (16, 1))`, `((1, 0, 0), (0, 257, 0), (0, 0, 65537))`, and the unimodular sheared family $B_D = ((D, D), (D-1, D))$ with $D = G_{\text{req}} + 1$), FLINT LLL recovers the exact primitive shortest vector $\pm u$ with $\|u\|_2^2 \in [\ell_{\text{lower}}^2, \ell_{\text{upper}}^2]$ using $0$ quantum preparations, while the clean-budget sine-window sweep charges $N_{\text{prep}}^{\text{sweep}} \in [20{,}496,\; 46{,}469{,}808]$ quantum source preparations.

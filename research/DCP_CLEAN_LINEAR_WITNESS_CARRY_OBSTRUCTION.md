# Clean DCP Linear Witness Identities and Conditioned-Label Audit

## Correction, 2026-10-16

The disjoint-kernel source-average decay claim is RETRACTED: the generated
effective columns are even and are NOT IID uniform over the original group.
The fixed-free-coordinate pivot obstruction and carry-parity identity remain
scoped statements. Carry constraints are not necessarily independent, and
their number alone proves no exponential failure probability. Nothing here
rules out general polynomial-time DCP algorithms. Local derivations remain
review pending; passing finite tests is not mathematical peer review.

## 1. Motivation and Scope

In `theorems/dcp_clean_source_budget.py` (`research/DCP_CLEAN_SOURCE_BUDGET.md`), `theorems/dcp_native_parity_bridge.py` (`research/DCP_NATIVE_PARITY_BRIDGE.md`), `theorems/dcp_direct_witness_filter.py` (`research/DCP_DIRECT_WITNESS_FILTER.md`), and `theorems/dcp_forward_sampler_swap.py` (`research/DCP_FORWARD_SAMPLER_SWAP.md`), the end-to-end clean DCP / sine-window route reduces to constructing an explicit uniform polynomial-time target-controlled unitary
$$
U_t |0\rangle \;=\; \sum_{w \in \{0, 1\}^K,\, g} \alpha_{t, w, g} |w, g\rangle
$$
for a public label matrix $A \in \mathbb{Z}_{2^t}^{n \times K}$ ($q = 2^t$, $K = n t + \Delta$) such that:
- In the **direct witness filter** (`dcp_direct_witness_filter.py`), verified coverage $\beta_A = q^{-n}\sum_{t \in \mathbb{Z}_q^n} \sum_{x \in F_t} |\alpha_{t, x}|^2$ yields full-secret recovery with unconditional probability $\ge 2^{-\Delta}\beta_A^2$.
- In the **forward-sampler SWAP predictor** (`dcp_forward_sampler_swap.py`), phase-aligned witness pairs across $F_f$ and $F_{f + h}$ ($h = (q/2, 0, \dots, 0)$) yield first-bit parity prediction advantage
  $$
  \mathrm{Adv}_{\text{SWAP}}(A) \;=\; \frac{1}{2^{K+1}}\sum_{x, y \in \{0,1\}^K : A(x-y) \equiv h} \operatorname{Re}\!\left(\sum_g \alpha_{Ax, x, g}\overline{\alpha_{Ay, y, g}}\right).
  $$

This module tests these particular constructions and records their identities:
1. **$\mathbb{Z}_{2^t}$-Linear / 2-Adic Hensel Right-Inverse Synthesis** ($U_t$ computed via modular Gauss-Jordan / Newton-Hensel inversion over $\mathbb{Z}_{2^t}$).
2. **Bitwise $\mathbb{F}_2$-Linear RREF Synthesis** ($U_t$ computed by stacking all $n t$ bit layers of $A$ over $\mathbb{F}_2$ and applying a CNOT right-inverse).
3. **Disjoint-Support Kernel Linearization** (eliminating quadratic and higher-degree carry cross-terms on the layer-0 $\mathbb{F}_2$-kernel via pairwise-disjoint kernel supports).

## 2. Theorem 1 — 2-Adic Hensel Disjoint Boolean Translate Theorem

Let $A \in \mathbb{Z}_{2^t}^{n \times K}$ ($t \ge 2$, $K \ge n$) have an $n \times n$ pivot block $A_P \in \mathrm{GL}_n(\mathbb{Z}_{2^t})$ ($\det(A_P) \equiv 1 \pmod 2$). For any fixed Boolean assignment $u_0 \in \{0, 1\}^{K-n}$ on the non-pivot coordinates $\bar{P}$, define the deterministic polynomial-time 2-adic witness map $w(t) \in \mathbb{Z}_{2^t}^K$ by
$$
w_P(t) \;:=\; A_P^{-1}(t - A_{\bar{P}} u_0) \bmod 2^t, \qquad w_{\bar{P}}(t) \;:=\; u_0.
$$

**Theorem 1 (Exponential Coverage Decay and Exact Zero SWAP Parity Advantage).**
For every $t \ge 2$ and every invertible pivot block $A_P \in \mathrm{GL}_n(\mathbb{Z}_{2^t})$:
1. **Exact Verified Coverage**: The map $t \mapsto w_P(t)$ is a bijection on $\mathbb{Z}_{2^t}^n$, so $w(t) \in \{0, 1\}^K$ holds if and only if $w_P(t) \in \{0, 1\}^n$. Exactly $2^n$ of the $2^{n t}$ targets satisfy $w(t) \in \{0, 1\}^K$, giving exact verified coverage and direct-filter full-secret success:
   $$
   \beta_A \;=\; \frac{2^n}{2^{n t}} \;=\; 2^{-n(t-1)}, \qquad
   P_{\text{direct-filter}}(\text{correct } S \wedge \text{herald}) \;=\; 2^{-(K - n t)}\,2^{-2n(t-1)}.
   $$
2. **Disjoint Boolean Translates ($T_{\text{valid}} \cap (T_{\text{valid}} + h) = \emptyset$)**: For the parity target $h = (2^{t-1}, 0, \dots, 0)^T \in \mathbb{Z}_{2^t}^n$, the pivot shift is
   $$
   w_P(t + h) - w_P(t) \;\equiv\; A_P^{-1} h \;\equiv\; 2^{t-1}\bigl(A_P^{-1} e_1 \bmod 2\bigr) \pmod{2^t}.
   $$
   Because $\det(A_P) \equiv 1 \pmod 2$, the first column $A_P^{-1} e_1 \bmod 2 \in \mathbb{F}_2^n$ is non-zero, so at least one pivot coordinate $i \in P$ shifts by $2^{t-1} \pmod{2^t}$. Since $(x_i + 2^{t-1}) \bmod 2^t \in \{2^{t-1}, 2^{t-1}+1\}$ is disjoint from $\{0, 1\}$ for every $t \ge 2$ and $x_i \in \{0, 1\}$, no target $t \in \mathbb{Z}_{2^t}^n$ can have both $w(t) \in \{0, 1\}^K$ and $w(t + h) \in \{0, 1\}^K$. Consequently, the forward-SWAP observable $O = V^\dagger P W P V$ is **identically the zero matrix ($O \equiv 0$)** and $\mathrm{Adv}_{\text{SWAP}}(A) = 0$ for every secret $S \in \mathbb{Z}_{2^t}^n$.

## 3. Theorem 2 — Exact Carry-Parity Vanishing Criterion for Bitwise $\mathbb{F}_2$-RREF Synthesis

Write each entry of $A \in \mathbb{Z}_{2^t}^{n \times K}$ in binary as $A_{\ell, r} = \sum_{b=0}^{t-1} A^{(b)}_{\ell, r} 2^b$ with $A^{(b)} \in \mathbb{F}_2^{n \times K}$, and stack the $n t$ binary rows into $M_{\mathbb{F}_2} \in \mathbb{F}_2^{(n t) \times K}$ ($K \ge n t$). Given a full-row-rank $M_{\mathbb{F}_2}$ and an $\mathbb{F}_2$-right inverse $R_{\mathbb{F}_2} \in \mathbb{F}_2^{K \times (n t)}$ satisfying $M_{\mathbb{F}_2} R_{\mathbb{F}_2} = I_{n t} \pmod 2$, define the reversible CNOT witness circuit
$$
w(t) \;:=\; R_{\mathbb{F}_2}\,\mathrm{bits}(t) \bmod 2 \;\in\; \{0, 1\}^K.
$$
For any $w \in \{0, 1\}^K$ and coordinate $\ell \in \{0, \dots, n-1\}$, define the carry sequence recursively by $c_\ell^{(0)}(w) := 0$ and
$$
s_\ell^{(b)}(w) \;:=\; \sum_{r=0}^{K-1} A^{(b)}_{\ell, r} w_r \;+\; c_\ell^{(b)}(w), \qquad
c_\ell^{(b+1)}(w) \;:=\; \left\lfloor \frac{s_\ell^{(b)}(w)}{2} \right\rfloor \qquad (b = 0, \dots, t-1).
$$

**Theorem 2 (Carry-Parity Vanishing Equivalence).**
For every target $t \in \mathbb{Z}_{2^t}^n$, the bitwise $\mathbb{F}_2$-linear candidate $w(t) = R_{\mathbb{F}_2}\mathrm{bits}(t) \bmod 2$ satisfies
$$
(A w(t))_\ell^{(b)} \;=\; t_\ell^{(b)} \oplus \bigl(c_\ell^{(b)}(w(t)) \bmod 2\bigr) \qquad \forall \ell \in \{0, \dots, n-1\},\; b \in \{0, \dots, t-1\}.
$$
Consequently, $A w(t) \equiv t \pmod{2^t}$ holds **if and only if** all $n(t - 1)$ intermediate carry parities vanish simultaneously:
$$
A w(t) \equiv t \pmod{2^t} \;\Longleftrightarrow\; c_\ell^{(b)}(w(t)) \equiv 0 \pmod 2 \quad \forall \ell \in \{0, \dots, n-1\},\; \forall b \in \{1, \dots, t-1\}.
$$

## 4. Identity 3: Disjoint-Support Linearization and the Actual Label Law

On the layer-0 kernel $x(u)=x_0\oplus\bigoplus_j u_jV_j$, overlaps can
introduce nonlinear carry constraints. Their degree can be bounded in
particular constructions but need not equal $2^b$ or even be nonzero.

**Disjoint-support identity.**
If $V_1, \dots, V_m \in \ker(A^{(0)}) \setminus \{0\}$ are chosen with pairwise-disjoint supports $\mathrm{supp}(V_i) \cap \mathrm{supp}(V_j) = \emptyset$ ($i \neq j$) to eliminate carry cross-terms, then:
1. Since every nonzero kernel vector $V_j \in \ker(A^{(0)})$ without zero columns in $A^{(0)}$ has $\mathrm{wt}_H(V_j) \ge 2$, the number of disjoint-support directions satisfies $m \le \lfloor K / 2 \rfloor$.
2. For all $u \in \{0, 1\}^m$, the modular sum linearizes in integer arithmetic to an affine $0$-$1$ subset sum of width $m$:
   $$
   A\left(x_0 \oplus \bigoplus_{j=1}^m u_j V_j\right) \;\equiv\; A x_0 \;+\; \sum_{j=1}^m u_j \tilde{A}_j \pmod{2^t}, \qquad
   \tilde{A}_j \;:=\; \sum_{r \in \mathrm{supp}(V_j)} (1 - 2(x_0)_r) A_{\cdot, r} \bmod 2^t.
   $$
3. Since signs are 1 modulo two,
$\widetilde A_j\bmod2=A^{(0)}V_j=0$. Thus the actual effective columns
live in $2\mathbb Z_q^n$. Even uniformity within that subgroup is not
automatic when supports are selected from the observed labels. The old
bound using $q^n$ is inapplicable. Merely replacing $q$ with $q/2$ is not
valid without proving the conditioned source law and paying selection costs.

## 5. Exact Conditional Readout and Paid Branch Probability

For specified effective columns, let $c_f$ count Boolean words with sum $f$,
$N=2^m$, and $h=(q/2,0,\ldots,0)$. With a uniform secret the optimal
parity advantage is

$$\mathrm{Adv}=\frac{1}{2N}\sum_f\sqrt{c_f c_{f+h}}.$$

This is the clean subset-sum block calculation underlying the known
[Bacon-Childs-van Dam measurement analysis](https://arxiv.org/abs/quant-ph/0501044),
not a new efficient decoder. The producer evaluates the finite expression
without assuming a random-label law; integer square-root enclosures provide
exact rational endpoints. Tests independently average physical pure-state
density matrices over all small secrets and check their Helstrom trace norm.
Enumerating $2^m$ words is explicitly charged and capped, not claimed scalable.

Countercontrol: $A=(1,q/2-1)$, $V=(1,1)$ gives one effective label $q/2$.
One compressed qubit then reveals parity perfectly, advantage $1/2$, for
every $t\ge2$. If the two original labels are independently uniform ODD
numbers, their sum is uniform EVEN and mean conditional advantage is $1/q$,
twice the old $1/(2q)$ bound. This is a deliberately specified conditioned
ensemble, not a claim about arbitrarily adapted kernel supports.

The original flat $K$-qubit state enters ONE chosen affine Boolean subspace
with probability $p=2^{m-K}$. Random guessing on all failures gives only
$p\,\mathrm{Adv}$ unconditional advantage from that branch. In the two-wire
countercontrol $p=1/2$, so its contribution is $1/4$, not $1/2$. Measuring
and using OTHER syndromes is a different complete instrument, not forbidden
by this selected-branch ledger. Source-label selection itself is also paid.

No source-average compressed decay is currently proved. The report leaves
that field null rather than supplying an IID exponent. A new algorithm must
give a uniform public support-selection rule, its actual native label law,
all branch probabilities, polynomial readout construction and total cost.

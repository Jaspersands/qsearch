# Clean DCP Coordinate Rounding: Coverage Identities, Not an Impossibility Theorem

## Correction, 2026-10-16

The earlier volume/shearing obstruction is RETRACTED. The half-integer
dichotomy and coverage identities remain valid but do not imply overflow or
asymptotic decay. The implemented map is rounding BASIS COORDINATES, not the
Gram-Schmidt nearest-plane algorithm; its results cannot reject all Babai
methods, LLL preprocessing, or quantum DCP receivers. These are local,
review-pending derivations and finite calibrations, not a new algorithm.

## 1. Motivation and Scope

In `theorems/dcp_clean_linear_witness_carry_obstruction.py` (`research/DCP_CLEAN_LINEAR_WITNESS_CARRY_OBSTRUCTION.md`), we proved that naive $\mathbb{Z}_{2^t}$-linear right-inverse witness synthesis ($w_P(t) = A_P^{-1} t \bmod 2^t$) lands in $\{0, 1\}^K$ for only $2^n$ of $2^{nt}$ targets ($\beta_A = 2^{-n(t-1)}$) and achieves identically zero forward-SWAP parity advantage ($\mathrm{Adv}_{\text{SWAP}} = 0$) for all $t \ge 2$.

A natural polynomial-time geometric refinement is to use **LLL lattice basis reduction and Babai rounding** on the $q$-ary modular kernel lattice
$$
\Lambda_q(A) \;:=\; \bigl\{z \in \mathbb{Z}^K : A z \equiv 0 \pmod{2^t}\bigr\} \;\subset\; \mathbb{Z}^K
$$
to reduce an initial integer solution $z_0(t) \in \mathbb{Z}^K$ ($A z_0(t) \equiv t \pmod{2^t}$) into a fundamental parallelepiped centered at the midpoint $c := (\frac{1}{2}, \dots, \frac{1}{2})^T \in \mathbb{R}^K$ of the Boolean hypercube $\{0, 1\}^K$:
$$
z_{\text{Babai}}(t) \;:=\; z_0(t) \;-\; B_{\text{LLL}}\,\bigl\lfloor B_{\text{LLL}}^{-1}\bigl(z_0(t) - c\bigr)\bigr\rceil \;\in\; \mathbb{Z}^K,
$$
where the fractional residual after rounding lies in $[-1/2,1/2)$.
The identities below characterize this particular output map. The producer
enumerates all targets and Boolean vertices only for finite calibration;
this enumeration is not a polynomial-time implementation or a scaling proof.

## 2. Theorem 1 — Exact Coset Bijection and Fundamental Parallelepiped Vertex Identity

Suppose $A \in \mathbb{Z}_{2^t}^{n \times K}$ ($K \ge n$) has an $n \times n$ pivot block $A_P \in \mathrm{GL}_n(\mathbb{Z}_{2^t})$ ($\det(A_P) \equiv 1 \pmod 2$). Then the homomorphism $\phi_A : \mathbb{Z}^K \to \mathbb{Z}_{2^t}^n$, $\phi_A(z) = A z \bmod 2^t$, is surjective with kernel $\Lambda_q(A)$ of index $[\mathbb{Z}^K : \Lambda_q(A)] = \det(\Lambda_q(A)) = 2^{n t}$.

**Theorem 1 (Coset Bijection and Fundamental Parallelepiped Intersection Identity).**
For any full-rank basis $B_{\text{red}} \in \mathbb{Z}^{K \times K}$ of $\Lambda_q(A)$ (where Columns of $B_{\text{red}}$ generate $\Lambda_q(A)$) and center $c = (\frac{1}{2}, \dots, \frac{1}{2})^T$:
1. **Unique Coset Representative**: The half-open fundamental parallelepiped $\mathcal{P}_c(B_{\text{red}}) := c + B_{\text{red}}[-1/2, 1/2)^K$ contains **uniquely one** integer point $z_{\text{Babai}}(t) \in \mathbb{Z}^K \cap \mathcal{P}_c(B_{\text{red}})$ in each of the $2^{n t}$ cosets $\{z \in \mathbb{Z}^K : A z \equiv t \pmod{2^t}\}$ ($t \in \mathbb{Z}_{2^t}^n$), independent of the choice of initial representative $z_0(t)$.
2. **Exact Vertex Count Identity**: Because every $x \in \{0, 1\}^K \cap \mathcal{P}_c(B_{\text{red}})$ is the unique representative of its target $t = A x \bmod 2^t$, the number of targets $t \in \mathbb{Z}_{2^t}^n$ for which $z_{\text{Babai}}(t) \in \{0, 1\}^K$ is **identically equal** to the number of Boolean hypercube vertices inside $\mathcal{P}_c(B_{\text{red}})$:
   $$
   \bigl|\{t \in \mathbb{Z}_{2^t}^n : z_{\text{Babai}}(t) \in \{0, 1\}^K\}\bigr|
   \;=\; \bigl|\{0, 1\}^K \cap \mathcal{P}_c(B_{\text{red}})\bigr|.
   $$

## 3. Identity 2: Half-Integer Dichotomy, Not a Volume Barrier

For each target $t \in \mathbb{Z}_{2^t}^n$, define the centered rounding residual
$$
e(t) \;:=\; z_{\text{Babai}}(t) - c \;\in\; \left(\mathbb{Z} - \frac{1}{2}\right)^K \cap B_{\text{red}}\!\left[-\frac{1}{2}, \frac{1}{2}\right)^K.
$$

**Theorem 2 (Exact Half-Integer $\ell_\infty$ Dichotomy and Volume Ratio).**
1. Because $z_{\text{Babai}}(t) \in \mathbb{Z}^K$ and $c = (1/2, \dots, 1/2)^T$, every coordinate $e_r(t)$ belongs to the half-integer lattice $\mathbb{Z} + 1/2 = \{\pm 1/2, \pm 3/2, \pm 5/2, \dots\}$. Therefore:
   $$
   z_{\text{Babai}}(t) \in \{0, 1\}^K \;\Longleftrightarrow\; \|e(t)\|_\infty = \frac{1}{2}, \qquad
   z_{\text{Babai}}(t) \notin \{0, 1\}^K \;\Longleftrightarrow\; \|e(t)\|_\infty \ge \frac{3}{2}.
   $$
2. At $K=nt$, the determinant is $2^K$ and the centered unit cube has
volume 1. That volume ratio is NOT the fraction of integer representatives
that lie on Boolean vertices. No decay estimate follows from it.

Exact counterexample: $q=4,n=1,K=2,A=(2,1)$. The actual FLINT LLL basis
has columns $(-2,0)^T,(1,2)^T$. Its inverse is
$((-1/2,1/4),(0,1/2))$. For every Boolean vertex $x$, all coordinates
of $B^{-1}(x-(1/2,1/2))$ have magnitude at most $3/8$.
All four vertices are strictly in the fundamental parallelepiped, so
$\beta=1$, overflow is zero and forward-SWAP advantage is $1/2$ despite
the basis entry 1. The corrected test must PASS this identity, not demand
failure of a successful finder.

More generally $A=(1,2,\ldots,2^{t-1})$ has the public binary-digit inverse.
The live producer includes a $t=6$ control; tests check $2\le t\le8$.
These easy structured labels are not an IID native-source algorithm.
Requesting that ordered label list from fresh uniform labels would itself
cost $q^t$ trials in expectation if the entire tuple is rejected and redrawn.
Other selection strategies require their own sample costs and cannot assume
the structured source is free.

## 4. Identity 3: Direct-Filter and Forward-SWAP Formulas

**Theorem 3 (Exact Coverage and Forward-SWAP Observable Formula).**
When $U_t|0\rangle = |z_{\text{Babai}}(t)\rangle$ is executed inside the direct witness filter (`dcp_direct_witness_filter.py`) and forward-SWAP parity predictor (`dcp_forward_sampler_swap.py`) on $K = n t + \Delta$ clean phase qubits:
$$
\beta_{\text{Babai}}(A) \;=\; \frac{\bigl|\{0, 1\}^K \cap \mathcal{P}_c(B_{\text{LLL}})\bigr|}{2^{n t}}, \qquad
P_{\text{direct-filter}}^{\text{Babai}}(\text{correct } S \wedge \text{herald}) \;=\; 2^{-\Delta}\,\beta_{\text{Babai}}(A)^2,
$$
and for $h = (2^{t-1}, 0, \dots, 0)^T \in \mathbb{Z}_{2^t}^n$,
$$
\mathrm{Adv}_{\text{SWAP}}^{\text{Babai}}(A) \;=\; \frac{\bigl|\{t \in \mathbb{Z}_{2^t}^n : \|e(t)\|_\infty = \frac{1}{2} \;\wedge\; \|e((t+h)\bmod 2^t)\|_\infty = \frac{1}{2}\}\bigr|}{2 \cdot 2^K}.
$$

## 5. Concrete Constructive Rule: Native-Label Controls

Scientific question: does this PUBLIC polynomial-time classical witness
finder have enough coverage and reciprocal pairing on the actual uniform
label distribution to make the existing coherent filter useful?

- Input: explicit public labels $A\in\mathbb Z_q^{n\times K}$, uniform unknown
  secret in the supplied clean phase states, and public target $f$. No secret,
  witness table or favorable source-selection advice is given to the finder.
- Mechanism: mod-two RREF chooses an invertible pivot block in polynomial
  time; Hensel lifting, q-ary kernel construction, LLL and exact coordinate
  rounding produce one candidate. The direct filter would use its coherent
  implementation and inverse. That quantum circuit has NOT been compiled.
- Desired advantage: polynomial native-source cost would require a suitable
  coverage/paired-target guarantee at polynomial resource cost. None is known.
  Every attempted quantum filter consumes K ORIGINAL phase qubits; rank
  failures and verification failures are not discarded for free.
- Baselines: the fixed-free-coordinate pivot finder has exact coverage
  $2^{-n(t-1)}$; full Boolean enumeration/meet-in-the-middle costs must be paid,
  and known quantum sieves remain the benchmark for actual DCP recovery.
  A classical witness finder inside a quantum filter does not by itself
  classically recover an unknown secret supplied only in phase states.
- Falsifiers: vanishing coverage or paired mass under the native law,
  exponential finder/circuit cost, uncharged label selection, or success
  restricted to designed binary-weight labels.

Run `python theorems/dcp_babai_lattice_rounding_witness_obstruction.py
--native-controls --write` (one command). The saved artifact is
`research/phase_workbench/dcp_coordinate_rounding_native_controls.json`.
Default replay: n=1, K=t, four UNFILTERED public matrices per bit size, seed
20261016. All targets are exhausted for t<=8; otherwise each matrix uses 128
targets, their parity translates and 128 independently drawn second targets.
Second targets estimate beta squared without squaring a noisy first estimate.
The seed is reproducibility, NOT an IID confidence certificate.

| Bits t | Mean observed coverage over four matrices | Target calculation |
| --- | --- | --- |
| 4 | 21/32 | All targets, exact conditional on those matrices |
| 8 | 15/32 | All targets, exact conditional on those matrices |
| 12 | 53/256 | Fixed-seed replay |
| 16 | 1/16 | Fixed-seed replay |
| 24 | 3/512 | Fixed-seed replay |
| 32 | 0/512 accepted sampled targets | Fixed-seed replay |

This makes the rule unattractive as currently specified, but zero observations
do NOT prove zero success, exponential decay or failure at all larger sizes.
Only four matrices were tested at each size; it is not a source-average
performance certificate or the growing-vector-dimension lattice reduction.
Do not extend the scan by inertia. A different constructive rounding/support
rule needs a stated reason it could preserve mass and a decisive matched test.

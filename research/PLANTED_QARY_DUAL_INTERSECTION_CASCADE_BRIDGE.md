# Planted $q$-ary Dual-Intersection Cascade Bridge: Exact Candidate Subspace Size Law, Spurious Survivor Decay, and Oversampling Recovery Probability

## 1. Motivation and Scope

### Recovery Baseline And Source Boundary (2026-10-16)

The cascade is not a new algorithmic advantage for recovering a homogeneous
hidden linear subspace from copies of its uniform state. Measuring those SAME
copies in the computational basis gives IID uniform elements of B. The new
`recover_measured_span` receiver takes ONLY these measured vectors, q and n,
then performs exact finite-field elimination with FLINT. No hidden generator,
offset, density matrix, membership oracle or exponential group enumeration is
passed to it. Its output is an observed span, not a certificate of completeness.

For m copies and dimension d its exact recovery probability is
`prod_(j=0)^(d-1) (1-q^(j-m))` when m>=d, and zero otherwise. Conditional
on any fixed first sample, subtracting that observed anchor from the other
m-1 samples of a SHARED unknown affine coset gives IID uniform elements of B.
The affine baseline therefore uses the same formula with m-1 effective rows.
No inverse or unitary state preparation is needed after measurement. Naive
elimination costs O(m*n*min(m,n)) field operations and O(m*n) field elements;
source-copy preparation/acquisition is a separate unresolved input cost.

This baseline survives arbitrary computational-basis PHASE noise: diagonal
probabilities are unchanged. It does not automatically survive translation
or depolarizing noise. The attached tests execute actual phase Kraus mixtures,
computational measurement and QFT, and count every transcript in small controls.
They do not infer this statement from a green status flag.

IMPORTANT COUNTERCONTROL: if every copy has an independently fresh UNIFORM
affine offset, direct outcomes are IID uniform on the ambient space and reveal
no B at any transcript length. Coherent Fourier outcomes still lie in B^perp.
Shared-offset and fresh-offset sources have the same one-copy computational
marginal under a uniform offset prior, but different multi-copy correlations.
The K-copy shared-offset identity must not be applied to independent offsets.

Thus the fixed-coset recovery task has a polynomial sample-only baseline, but
this is NOT a dequantization of an arbitrary classical source instance, a noisy
hidden-subgroup oracle, code equivalence, shortest-vector search, DCP, or the
fresh-coset coherent-state problem. Quantum source acquisition may itself be
the significant resource in another input model. The live report now includes
both primal and dual recovery probabilities and these restrictions per case.
No candidate or active negative is created. The next experiment must name a
harder input/target and show why this baseline is unavailable or insufficient.

When a quantum algorithm applies $\mathrm{QFT}_q^{\otimes n}$ to $m \ge 1$ copies of a dimension-$d$ planted subspace state $|\psi_B\rangle = q^{-d/2}\sum_{b \in B}|b\rangle$ in $\mathbb{F}_q^n$, computational-basis readout yields $m$ i.i.d. uniform dual samples $U_\perp = (u^{(1)}, \dots, u^{(m)}) \sim \operatorname{Unif}((B^\perp)^m)$, where $\dim(B^\perp) = n - d$ and $|B^\perp| = q^{n-d}$. The planted subspace $B = (B^\perp)^\perp$ is then reconstructed via the orthogonal complement intersection cascade:
$$
\widehat{B}_m(U_\perp) \;:=\; \bigl\{\, x \in \mathbb{F}_q^n : \forall j \in \{1, \dots, m\},\; \langle x, u^{(j)}\rangle = 0 \,\bigr\} \;=\; \bigl(\operatorname{span}(u^{(1)}, \dots, u^{(m)})\bigr)^\perp \;\supseteq\; B.
$$
This note proves three exact theorems governing the candidate subspace dimension, the expected number of spurious survivors $|\widehat{B}_m(U_\perp) \setminus B|$, and the exact full-recovery probability as a function of the oversampling margin $\Delta m = m - (n - d)$.

## 2. Theorem 1 — Exact Dual-Span Rank Filtration and Candidate Subspace Cardinality

For any $m$-tuple $U_\perp = (u^{(1)}, \dots, u^{(m)}) \in (B^\perp)^m$, let $r_\perp(U_\perp) := \dim(\operatorname{span}(u^{(1)}, \dots, u^{(m)})) \in \{0, 1, \dots, \min(n - d, m)\}$.

**Theorem 1 (Deterministic Rank-Cardinality Law and Recovery Criterion).**
For every $U_\perp \in (B^\perp)^m$:
1. $B \subseteq \widehat{B}_m(U_\perp)$, $\dim(\widehat{B}_m(U_\perp)) = n - r_\perp(U_\perp)$, and
   $$
   \bigl|\widehat{B}_m(U_\perp)\bigr| \;=\; q^{n - r_\perp(U_\perp)} \;=\; q^d \cdot q^{(n - d) - r_\perp(U_\perp)}, \qquad
   \bigl|\widehat{B}_m(U_\perp) \setminus B\bigr| \;=\; q^{n - r_\perp(U_\perp)} - q^d.
   $$
2. Exact recovery $\widehat{B}_m(U_\perp) = B$ holds if and only if $r_\perp(U_\perp) = n - d$ (requiring $m \ge n - d$).

## 3. Theorem 2 — Exact Closed-Form Expectation of Candidate Subspace Size and Spurious Survivors

**Theorem 2 (Exact Exponential Decay of Expected Spurious Survivors).**
For every $m \ge 1$ and every dimension-$d$ subspace $B \subset \mathbb{F}_q^n$:
1. Every non-planted vector $x \in \mathbb{F}_q^n \setminus B$ satisfies $x \notin (B^\perp)^\perp$, so $u \mapsto \langle x, u\rangle$ is a surjective linear form on $B^\perp$ with kernel of size $q^{n-d-1}$. Hence for independent $u^{(1)}, \dots, u^{(m)} \sim \operatorname{Unif}(B^\perp)$,
   $$
   \Pr_{U_\perp \sim (B^\perp)^m}\!\bigl[x \in \widehat{B}_m(U_\perp)\bigr] \;=\; q^{-m} \qquad \forall x \in \mathbb{F}_q^n \setminus B.
   $$
2. By linearity of expectation (and equivalently by the $q$-Gaussian rank-sum identity $\sum_{r=0}^{\min(n-d, m)} q^{n-r} P_{\text{rank}}(r \mid q, n - d, m)$), the expected candidate subspace cardinality and expected spurious survivor count are
   $$
   \mathbb{E}_{U_\perp \sim (B^\perp)^m}\!\left[\bigl|\widehat{B}_m(U_\perp)\bigr|\right] \;=\; q^d \;+\; \bigl(q^n - q^d\bigr)\,q^{-m},
   $$
   $$
   \mathbb{E}_{U_\perp \sim (B^\perp)^m}\!\left[\bigl|\widehat{B}_m(U_\perp) \setminus B\bigr|\right] \;=\; \bigl(q^n - q^d\bigr)\,q^{-m}.
   $$

## 4. Theorem 3 — Exact Full-Recovery Probability and Two-Sided Oversampling Bounds

**Theorem 3 (Exact Full-Recovery Probability Law for $m \ge n - d$).**
For any $m \ge n - d$ with oversampling margin $\Delta m := m - (n - d) \ge 0$, the exact probability that $m$ i.i.d. uniform dual samples span $B^\perp$ ($\widehat{B}_m(U_\perp) = B$) is
$$
P_{\text{recover}}(q, n - d, m) \;:=\; \Pr_{U_\perp \sim (B^\perp)^m}\!\bigl[\widehat{B}_m(U_\perp) = B\bigr]
\;=\; \prod_{j=0}^{n-d-1} \left(1 - q^{j - m}\right)
\;=\; \prod_{i=1}^{n-d} \left(1 - q^{-(\Delta m + i)}\right),
$$
which obeys the two-sided bounds
$$
1 - \sum_{i=1}^{n-d} q^{-(\Delta m + i)} \;\le\; P_{\text{recover}}(q, n - d, m) \;\le\; 1 - q^{-(\Delta m + 1)}.
$$

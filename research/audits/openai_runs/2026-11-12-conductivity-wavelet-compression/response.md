## Finding

**A uniformly \(\ell^1\)-summable representation of \(\Pi\), even if efficiently sampleable, is not sufficient by itself.** The missing operation is cancellation-preserving multiplication/contraction with the native material circuit.

Below are two exact obstructions:

1. One coarse Haar wavelet becomes an exponentially large, flat collection of finest-scale coefficients under an extremely small material circuit.
2. For the actual native moments, an ungrouped Haar-index importance sampler can have optimal second moment \((n-1)^r\), even where \(\Pi\) is diagonal and the conductivity is analytically easy.

These falsify particular proposed operations—not all wavelet or randomized-block algorithms. No complete classical polynomial match is established here.

## 1. Cheapest test: one coarse wavelet times an oscillatory circuit

Use counting-measure normalization on edges, take \(j=1\), and assume \(L\ge4\). Define the normalized coarse horizontal Haar wavelet
\[
w(x,1)=\frac{s(x_1)}L,\qquad
s(x_1)=
\begin{cases}
1,&x_1<L/2,\\
-1,&x_1\ge L/2,
\end{cases}
\qquad w(x,2)=0.
\]

Take the material sign
\[
\sigma(x,j)=(-1)^{x_1}.
\]
This uses only the least significant coordinate bit; allowing input handling, its circuit size is \(O(n)\).

For every dyadic \(2\times2\) cell \(Q\), let
\[
\psi_Q(x,1)=\tfrac12(-1)^{x_1}\mathbf1_Q(x),\qquad
\psi_Q(x,2)=0.
\]
These are normalized, mutually orthogonal finest horizontal Haar wavelets. Since \(s\) is constant on each \(Q\),
\[
\langle\psi_Q,\Sigma w\rangle=\frac{2s_Q}{L}.
\]
Moreover, these are **all** the nonzero coefficients of \(\Sigma w\). Consequently,
\[
\sum_Q|\langle\psi_Q,\Sigma w\rangle|=\frac L2,
\qquad
\sum_Q|\langle\psi_Q,\Sigma w\rangle|^2=1.
\]

Thus the material multiplier has a coarse-to-fine column with \(\ell^1\) norm \(L/2=2^{n-1}\), despite having operator norm one and a tiny circuit.

This oscillation is not removed by the projection:
\[
\Pi\Sigma w=\Sigma w.
\]
Indeed, \(\Sigma w\) is a mean-zero direction-1 field depending only on \(x_1\), hence is a periodic gradient.

### Consequence for coefficient sampling

Suppose the column \(c_Q=\langle\psi_Q,\Sigma w\rangle\) is represented by sampling one coefficient:
\[
Y=\frac{c_Q}{p_Q}e_Q.
\]
For every choice of probabilities,
\[
\mathbb E\|Y\|_2^2
=\sum_Q\frac{|c_Q|^2}{p_Q}
\ge\left(\sum_Q|c_Q|\right)^2
=\frac N4.
\]

This falsifies a constant-second-moment, one-wavelet-output implementation of this material step. **It is not yet a scalar-estimation lower bound:** paired contractions can avoid constructing that random vector.

The dense coefficient vector also has a tiny pointwise description. The obstruction is therefore not evaluating \(\Sigma w(x)\); it is converting that description into the cancellation-preserving wavelet access needed by subsequent operations.

### The overlapping coarse/fine block is not low rank

Let \(\mathcal C\) be the direction-1 fields constant on each \(2\times2\) cell, and let \(\mathcal F\) be the finest horizontal-detail space. Both have dimension \(m=N/4\). More generally, take
\[
\sigma_g(x,j)=(-1)^{x_1}
g\!\left(\lfloor x_1/2\rfloor,\lfloor x_2/2\rfloor\right),
\qquad g\in\{\pm1\}.
\]
Then \(\Sigma_g:\mathcal C\to\mathcal F\) is an isometry. Its matrix in any orthonormal bases of these spaces has all \(m\) singular values equal to one. A rank-\(q<m\) approximation therefore has operator error at least one.

Even applying \(\Pi\) does not permit a constant-rank replacement of this entire interaction. For \(f\in\mathcal F\),
\[
\|\Pi f\|_2^2
=\langle D^*f,K_0^+D^*f\rangle
\ge \tfrac18\|D^*f\|_2^2
\ge \tfrac14\|f\|_2^2.
\]
Here \(\lambda_{\max}(K_0)\le8\), and the differences inside each horizontal pair alone give
\(\|D^*f\|_2^2\ge2\|f\|_2^2\).
Thus every rank-\(q<m\) approximation to
\[
\Pi\Sigma_g|_{\mathcal C}
\]
has error at least \(1/2\).

**Scope:** this rejects low-rank substitution for the whole overlapping coarse/fine sector. It does not reject low rank for spatially separated blocks of \(\Pi\), nor imply that a full-rank operator lacks a succinct factorization.

## 2. A scalar-moment obstruction for ungrouped Haar paths

A stronger, estimator-specific result uses the actual \(T_r\), not just a random vector.

Consider the invariant subspace
\[
\mathcal H=\{f(x_1)e_1/\sqrt L\}.
\]
On this subspace,
\[
\Pi=I-|\phi_L\rangle\langle\phi_L|,
\qquad \phi_L=L^{-1/2}\mathbf1.
\]
In the separable two-dimensional Haar basis, \(\mathcal H\) is a basis subspace. Both \(\Pi\) and the parity multiplier preserve it, so no omitted wavelet paths leave this subspace.

Let \(m=L/2\). Split its one-dimensional Haar basis into:

- \(\mathcal C_1\): the constant and all wavelets coarser than adjacent pairs;
- \(\mathcal F_1\): the \(m\) adjacent-pair wavelets.

Let \(U\) be the \(m\times m\) Haar synthesis matrix on the pair grid. Its first column is
\[
u=m^{-1/2}\mathbf1.
\]
Multiplication by \((-1)^{x_1}\) exchanges pair-constant and pair-antisymmetric functions, so its Haar matrix is exactly
\[
G=
\begin{pmatrix}
0&U^T\\
U&0
\end{pmatrix}.
\]

Remove the constant column from \(U\), obtaining \(U_0\). On the nonconstant sector,
\[
R=\Pi\Sigma\Pi=
\begin{pmatrix}
0&U_0^T\\
U_0&0
\end{pmatrix}.
\]
The moment endpoints are \(v=(0,u)\), giving
\[
T_r=v^TR^rv.
\]
Since \(U_0^Tu=0\),
\[
T_0=1,\qquad T_r=0\quad(r\ge1).
\]

Nevertheless, the absolute sum of the individual Haar-index terms grows with depth. For \(r=2s\),
\[
\sum_{\gamma}|t_\gamma|
=u^T\bigl(|U_0||U_0|^T\bigr)^su.
\]
At scale \(\ell\), the absolute Haar columns contribute the dyadic block-averaging projection \(E_\ell\). Hence
\[
|U_0||U_0|^T=\sum_{\ell=1}^{n-1}E_\ell,
\qquad E_\ell u=u,
\]
and therefore
\[
\boxed{\ \sum_{\gamma}|t_\gamma|=(n-1)^s.\ }
\]

For any single-term importance estimator that samples a complete index path \(\gamma\) with probability \(p_\gamma\) and returns \(t_\gamma/p_\gamma\),
\[
\boxed{\quad
\mathbb E Z_r^2
=\sum_\gamma\frac{t_\gamma^2}{p_\gamma}
\ge\left(\sum_\gamma|t_\gamma|\right)^2
=(n-1)^r,\qquad r\ \text{even}.
\quad}
\]

This allows **arbitrary joint importance probabilities over complete paths**, not just independent step choices. All coefficients are already available exactly; evaluating them faster cannot fix the bound.

For even \(r=\Theta(\log n)\), this exceeds
\(\operatorname{poly}(n,r)C^r\) for every fixed polynomial and fixed \(C\). Also,
\[
\rho(|R|)=\sqrt{n-1},
\]
so positive diagonal reweighting cannot give this transition a uniformly bounded induced \(\ell^1\) norm.

### What this does—and does not—prove

This is an exact obstruction to the **ungrouped Haar-index expansion**. Grouping cancellations before sampling can evade it: here \(U_0^Tu=0\) collapses the whole calculation.

Indeed, this native input is easy:
\[
K_1=\frac{2\rho}{\rho+1}.
\]
Thus the result is explicitly **not** conductivity hardness, a separation, or a lower bound against circuit-aware preprocessing or other wavelet bases.

## 3. What material access can actually be paid

Individual Haar material entries need not be obtained by a dense exact sum.

For two Haar wavelets, define
\[
q_{\alpha\beta}=\sum_x|w_\alpha(x)w_\beta(x)|\le1.
\]
Their magnitudes are constant on their overlapping support \(I\). If \(I\ne\varnothing\), sample \(X\) uniformly from \(I\) and return
\[
Z=q_{\alpha\beta}\,
\sigma(X)\,
\operatorname{sgn}\!\bigl(w_\alpha(X)w_\beta(X)\bigr).
\]
Then
\[
\mathbb EZ=\langle w_\alpha,\Sigma w_\beta\rangle,
\qquad
\mathbb EZ^2=q_{\alpha\beta}^2.
\]

**Paid resources per draw:**

- one native material-circuit evaluation, \(O(B)\) Boolean work;
- \(O(n)\) random bits for a dyadic overlap;
- polynomial \((n,p)\) arithmetic for \(p\)-bit Haar factors and output.

Accuracy \(\theta q_{\alpha\beta}\) with failure \(\xi\) costs
\(O(\theta^{-2}\log(1/\xi))\) draws. This is accuracy relative to the known envelope, **not** relative to the possibly vanishing matrix element.

What this does not supply is:

- a sampler proportional to the unknown \(|\langle w_\alpha,\Sigma w_\beta\rangle|\);
- its normalization;
- an exact conditional block contraction;
- a reusable representation after many alternating operations.

Calling the entry routine for \(m\) entries must be charged \(m\) times unless a separate aggregation argument is supplied.

### Far-field compression: a valid ingredient, but an unpaid contraction remains

Multiplying a fixed low-rank block by \(\Sigma\) does **not** itself increase its rank. However, composing compressed blocks introduces material-dependent matrices such as
\[
G_{\ell k}
=\sum_{x\in Q}\overline{v_\ell(x)}\,\sigma(x)\,u_k(x).
\]
Every such contraction, its sampling envelope, precision, and conditional use must be paid. Low rank of the homogeneous kernel supplies neither these sums for free nor a bound on the variance after summing over blocks and scales.

## 4. Remaining constructive obligation and exact falsifiers

A sufficient new lemma would provide a **closed, efficiently manipulable sketch representation** containing \(\eta_j\), with paid \(\Sigma\) and \(\Pi\) operations satisfying, conditionally on the current represented vector \(X\),
\[
\mathbb E[X'\mid X]=OX,\qquad
\mathbb E[\|X'\|_2^2\mid X]\le C\|X\|_2^2,
\]
for \(O=\Sigma,\Pi\), with \(C\) independent of \(n\). All representation updates, conditional sampling, scalar readout, and finite-precision bias control must cost polynomially in \(B,n,r\) and the required precision bits. The tower property would then give the desired \(C^{O(r)}\) second moment.

Wavelet almost-diagonality of \(\Pi\) alone does not establish this closure.

**Exact tests for a proposed implementation:**

- **Individual coefficient/path sampling:** parity material gives the bounds \(N/4\) for the one-column vector sampler and \((n-1)^{2s}\) for the even moment \(r=2s\).
- **Fixed-rank coarse/fine replacement:** \(\Sigma_g\) gives operator error at least \(1/2\) after projection whenever the retained rank is below \(N/4\).
- **A genuinely grouped repair:** next test the same \(\Sigma_g\) with a nonlayered succinct sign, for example
  \[
  g(b_1,b_2)=(-1)^{\sum_t b_{1,t}b_{2,t}\bmod2}.
  \]
  It has an \(O(n)\)-size circuit, while the flat coarse-to-fine coefficients and rank obstruction persist. A claimed repair must specify its conditional computations and prove the joint variance bound—not extrapolate from the solvable parity case.

**Status:** explicit constructions and restricted-estimator counterexamples are proved above. Cancellation-aware randomized block contraction remains unresolved. No finite-grid evidence, hardness claim, or quantum–classical separation is inferred.
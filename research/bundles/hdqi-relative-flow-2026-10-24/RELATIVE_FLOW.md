# A Degree-Scale Relative Bound For The HDQI Real-Time Flow

Date: 2026-10-24. Status: local, unreviewed deductions and finite checks.
This removes a total-mass factor from a specific real-time gradient
estimate. It does NOT establish the filtered-parent gap, state preparation,
novelty, or a quantum advantage. Do not admit it as a solved candidate.

## Scientific Question And Public Model

The current target remains polynomial preparation of the canonical HDQI
pilot at small beta^2(d+1), on large connected graphs where beta^2 sum J_i^2
can be superlogarithmic. The earlier mass-gap certificate and direct
spectral-clipping preparation comparator do not settle that regime.

Use the canonical independent Pauli generators O_i from the existing
bundles, H=sum J_i O_i, real |J_i|<=1, and the algebra A with orthonormal
ordered-word basis P(y). All inner products here are normalized
Hilbert-Schmidt inner products, identified with Euclidean coefficient
inner products. Let

    n_i|y> = y_i|y>, N=sum_i n_i,
    Delta = max_j sum_{i~j} J_i^2,
    H_R = D_G H D_G, L = H-H_R.

L represents ad_H on A. It is Hermitian on coefficient space and has the
vacuum/identity in its kernel. It is NOT the thermal parent F_beta, and it
is NOT the anti-Hermitian rotation named `k` in the older model code.

The public graph and couplings determine every operator. No thermal
state, eigenbasis, unknown reflection, or imaginary-time oracle is supplied.
The code's diagonalizations are exponentially expensive finite references.

## 1. Exact Gradient-Defect Identity

Set P_i=product_{j~i} Z_j and p_i=(I-P_i)/2. Right multiplication by O_i
is represented by O_i P_i. Consequently

    L = sum_i J_i O_i (I-P_i).

Only O_i fails to commute with n_i. Since [n_i,O_i]=-O_i Z_i and P_i
does not contain Z_i,

    [n_i,L] = -J_i O_i Z_i (I-P_i),
    [n_i,L]^dagger [n_i,L] = 4 J_i^2 p_i.

All p_i are diagonal. Odd neighbor parity implies at least one occupied
neighbor, so p_i <= sum_{j~i} n_j as an operator inequality. Therefore

    sum_i [n_i,L]^dagger[n_i,L]
      = 4 sum_i J_i^2 p_i <= 4 Delta N.                 (1)

This is an ALL-SIZE operator identity/inequality, not a Taylor expansion.
Let D be the row stack of n_i. Then D^dagger D=N and (1) says

    || (D L - diag(L,...,L) D) X || <= 2 sqrt(Delta) ||D X||.  (2)

The seminorm kernel is respected: both sides vanish on the identity.
No unrestricted block-Jacobian bound on arbitrary vector-valued fields
is asserted. The bound acts on gradients of one common coefficient vector.

### Tagged Sector Needed For The Actual Filter

The jump Z_a lies in Z_a A, not A. Multiplication on the left by Z_a
identifies that sector with A, where ad_H is represented by

    L_a = L - 2 J_a O_a.

The exact defect Gram matrix now replaces the a-th odd projector by its
even complement:

    sum_i [n_i,L_a]^dagger[n_i,L_a]
      = 4 sum_{i!=a} J_i^2 p_i + 4 J_a^2 (I-p_a)
      <= 4 Delta N + 4 J_a^2 I.

Use D_+=(I,n_1,...,n_m)^T and rho_a=max(Delta,J_a^2). Its weight is N+I,
and the analogue of (2) has constant 2 sqrt(rho_a). The self-coupling
cannot be omitted: with no edges, L=0 but L_a=-2J_a O_a is nonzero.
Since rho_a<=d+1, the natural dimensionless parameter is at most beta^2(d+1).

## 2. Real-Time Propagation And Commutator Bound

The following argument applies to either (D,L,rho=Delta) or
(D_+,L_a,rho=rho_a). Write C=D L-diag(L)D and g=2sqrt(rho).
For U_t=exp(itL), w(t)=D U_t X satisfies

    w'(t)=i diag(L) w(t)+i C U_t X.

The first term preserves its norm. Equation (2) gives
|d||w||/dt|<=g||w||, interpreted by continuity at zero. Gronwall, also
applied backwards in time, yields

    ||D U_t X|| <= exp(g|t|) ||D X||.                   (3)

Duhamel and (3) additionally give

    ||(D U_t-diag(U_t)D)X||
       <= [exp(g|t|)-1] ||D X||.                       (4)

No total mass M=sum J_i^2 occurs. The proof uses the Hilbert-Schmidt
geometry, real-time unitarity, and the exact graph-parity structure.

## 3. Transfer Through The Actual Gaussian Filter

The earlier bounded parent uses

    f_s(u)=exp(-u^2/8-u/4+i s u),
    f_s(beta L)=C0 E_V exp(iV) U_{beta(V+s)},
    C0=exp(1/8), V~Normal(0,1/4).

Applying (4) inside this real-time integral gives the relative bound

    ||[D,f_s(beta L)] X|| <= b_s ||DX||,
    b_s = C0 [M_V(a) exp(a|s|)-1],
    a=2 beta sqrt(rho),
    M_V(t)=E exp(t|V|)=2 exp(t^2/8) Phi(t/2).            (5)

Here the bracket denotes D f-diag(f)D, not an ordinary square-matrix
commutator. The phase exp(iV) has modulus one; it is not dropped from the
actual filter, only from its norm upper bound.

For the outer density w(s)=2 sech(2pi s), define lambda=2pi, A0=4/pi.
Its absolute-value survival probability is at most A0 exp(-lambda s).
For 0<=t<lambda this implies upper bounds

    M_S(t) <= U0(t)=1+A0 t/(lambda-t),
    M_S'(t) <= U1(t)=A0 lambda/(lambda-t)^2,
    M_S''(t) <= U2(t)=2 A0 lambda/(lambda-t)^3.

These derivative bounds follow by integration of the survival probability,
not by differentiating an inequality without justification. Also

    M_V'(t)=t M_V(t)/4 + 1/sqrt(2pi),
    M_V''(t)=(1/4+t^2/16) M_V(t)+t/[4sqrt(2pi)].

Jensen followed by (exp(a y)-1)^2<=a^2 y^2 exp(2ay), y>=0, gives

    integral w(s) ||[D,f_s(beta L)]X||^2 ds
      <= B(a) ||DX||^2,                               (6)

    B(a)=C0^2 a^2 [M_V''(2a) U0(2a)
                   +2 M_V'(2a) U1(2a)+M_V(2a) U2(2a)].

This bound is finite for 2a<2pi, equivalently beta^2 rho<pi^2/4, and
B(a)=O(beta^2 rho) near zero. At and beyond that threshold the code
returns INCONCLUSIVE for this bound; it does not claim the actual filter
or parent diverges. The formula is an analytic upper bound, not an
outward-rounded floating-point certificate at adversarial thresholds.

The same real-time argument applies to the Gaussian without the linear
thermal factor, with C0=1 and without the exp(iV) phase.

### Direct Link To Jump Coefficients

For L_a, f_s(beta L_a)|0> is exactly the coefficient vector of Z_a L_a(s),
where L_a(s) denotes the operator-valued thermal jump of the older bundle.
This notation collision is restricted to this sentence: the code uses
`ell` for the coefficient Liouvillian and `left` for the operator jump.
The equality follows by applying ad_H to Z_a X and is checked independently
against the dense energy-basis construction.

Apply (5)-(6) with D_+ to the vacuum. Its first component cancels in the
commutator and its other components are n_i f_s(beta L_a)|0>. Hence the
integrated, UNNORMALIZED squared coefficient word weight is at most B(a).
This is a trace/Euclidean influence bound. It is not an operator-norm
bound on a truncated Pauli expansion and not a thermal Poincare inequality.

## 4. Two Falsifiers Against Invalid Upgrades

### Real Time Is Essential

Take r disjoint edges with unit couplings. Each two-generator block has
Hamiltonian spectrum +/-sqrt(2), so its commutator Liouvillian has an
eigenoperator with eigenvalue 2sqrt(2). Tensor r such eigenoperators to
obtain X with L X=2sqrt(2) r X and DX!=0. Then

    ||D exp(tau L)X||/||DX||=exp(2sqrt(2) tau r).

Delta remains one. Thus replacing it by exp(2tau sqrt(Delta)) would be
false. Analytic continuation does not preserve a real-time norm estimate.
This is not a mixing lower bound and not a hard instance: the example
factors into independent two-generator blocks.

### Thermal Metric Transfer Is Not Free

Even the degree-zero commuting model H=sum_i X_i obstructs a naive
dimension-independent comparison of trace and thermal Dirichlet forms.
Let P_- be the projector onto all X_i=-1, and let

    partial_i(X)=(X-Z_i X Z_i)/2,
    E_0(X)=sum_i tau(partial_i(X)^dagger partial_i(X)),
    E_beta(X)=sum_i Tr(rho_beta partial_i(X)^dagger partial_i(X)).

For P_-, E_0=m/2^(m+1). Each squared derivative has equal weight on the
all-minus configuration and the configuration with just site i flipped.
Their thermal probability ratio is exp(-2beta). Consequently

    E_beta(P_-)/E_0(P_-)=[exp(beta)/cosh(beta)]^(m-1).

For the all-plus projector the ratio is
[exp(-beta)/cosh(beta)]^(m-1). Both comparisons deteriorate exponentially
with m at any fixed beta>0, including beta=0.1.

For the KMS norm ||Y||_KMS^2=Tr(sqrt(rho)Y^dagger sqrt(rho)Y) and the
commutator gradient Y_i=[Z_i,P_-], the ratio to its normalized-trace
Dirichlet form is exp(beta(m-1))/cosh(beta)^m. The all-plus version has
exp(-beta(m-1))/cosh(beta)^m. Thus using the actual balanced thermal
geometry instead of a one-sided weight does not repair a blanket norm
comparison. This is an easy product Gibbs state with a gap; it falsifies
the proposed shortcut, NOT the desired preparation claim.

## 5. The Missing Inequality, Stated Precisely

Let S=exp(-beta H/2), B_i(s)=exp(i beta s H)
exp(-beta^2 ad_H^2/8)(Z_i) exp(-i beta s H), and put

    ||Y||_S^2 = tau(S Y^dagger S Y).

For T in A write T=S^(1/2) X S^(1/2), also with X in A. The existing
parent row before harmless left multiplication by Z_i equals

    [L_i(s)T-T L_i(s)^dagger]/2
       = S^(1/2)[B_i(s),X]S^(1/2)/2.

The sought global gap is therefore equivalent to the weighted inequality

    (1/4) sum_i integral w(s) ||[B_i(s),X]||_S^2 ds
       >= gamma inf_c ||X-cI||_S^2,                    (7)

uniformly over X in A along the temperature path. The new trace-metric
bounds (1)-(6) do NOT prove (7). The product-state falsifier forbids merely
changing metrics with a constant factor. What is needed is a genuine
thermal gradient/curvature or approximate-tensorization argument, with
the product-field contribution handled nonperturbatively. A computable
pilot-preparing unitary must not be assumed to establish that comparison.

## Research Leverage, Comparators And Limits

The new identity supplies a square-root weighted-degree control in the
real-time language already used to implement the parent. It holds on
large connected graphs outside the earlier mass regime, including the
explicit circulant families in the parameter ledger. Those rows do not
construct or diagonalize huge instances. A small value of B(a) is not an
algorithm admission. No exponential classical hardness follows either.

The prior classical partition-function algorithm and direct quantum
spectral-clipping preparation remain mandatory comparators. A useful
physical output and priced decoder are still required after preparation.
We do not claim a newly proved degree-gap theorem or a known hard output.

Relevant primary context:

- [Hastings--Schmidhuber](https://arxiv.org/html/2610.03697v1), Sections VI-VII,
  supplies the pilot-preparation target and leaves the degree-scale gap
  open. Their convergence/partition-function results are not gap proofs.
- [Cai--Zhan--Zlokapa](https://arxiv.org/html/2610.05953v1), Sections 1-3,
  motivates relative gradient reasoning through fermionic Jacobians.
  Its SYK disorder, Clifford derivative and parity assumptions have NOT
  been transferred to commuting Z_i jumps or arbitrary graphs.
- [Leng--Jiang--Lin](https://arxiv.org/html/2604.22996v1) supplies the
  filtered-parent machinery already adapted in the preceding bundle.
  The filter is prior art; the elementary graph-parity estimate here has
  not undergone independent review or a comprehensive novelty search.

Next decisive task: prove or falsify (7) with degree-scale constants, or
derive a valid thermal-relative substitute for (6). Do not spend the next
pass generating more finite spectra or treating these unweighted bounds
as if they solved that task.

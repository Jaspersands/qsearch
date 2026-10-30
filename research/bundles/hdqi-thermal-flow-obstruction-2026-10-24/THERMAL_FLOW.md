# Thermal Real-Time Gradient Control Fails At Small Squared Degree

2026-10-24. LOCAL UNREVIEWED ANALYTIC COUNTEREXAMPLE. This falsifies a
particular proposed proof route, NOT the HDQI parent gap or preparation
conjecture. The example is classically easy. No new algorithm or oracle
task is admitted.

## Portfolio Decision And Precise Question

The previous cubic pass transfers its current guarantee to known scalar
OPI. Rees has an independently reviewed core but no established new hard
application; its explicit-action and succinct-circuit classical filters
remain active. The surface-isogeny route still lacks executed geometry
under its weak input model. None is advanced by another parameter variant.

The independent HDQI branch has a specific constructive bottleneck:
polynomial coherent pilot preparation at small beta^2(d+1), beyond small
total mass. [Hastings--Schmidhuber, Section VII.2](https://arxiv.org/html/2610.03697v1#S7.SS2)
leaves a related degree-scale parent-gap conjecture open. The existing
local filtered-parent construction supplies priced public access but not
the desired all-size gap. Its Pauli-readout classical comparators remain
mandatory; preparation alone would not establish a useful speedup.

`../hdqi-relative-flow-2026-10-24/RELATIVE_FLOW.md` proves an unweighted
real-time gradient estimate. A suggested next step was a direct thermal
version, avoiding the already-falsified blanket comparison of thermal and
trace norms. We now test THAT stronger suggestion, not the old comparison.

**Hypothesis rejected:** replacing the trace gradient norm by its KMS
version preserves a bound of the form

    ||D exp(it ad_H) X||_beta
        <= exp(C(kappa)*sqrt(d)*|t|) ||D X||_beta,
    kappa=beta^2(d+1),

with finite C(kappa) independent of d and size. The corresponding defect
bound with squared constant O_kappa(d) also fails. The source, algebra and
derivatives below are exactly those of the existing canonical pilot.

## 1. Model, Metric And Compact Witness

Take the anticommutation star with center0 and leaves1,...,d, d>=2,
unit couplings, and m=d+1. Its independent involutions obey

    A=O0, B_j=Oj,  A B_j=-B_j A,  [B_j,B_k]=0,
    H=A+sum_j B_j.

The existing canonical realization is A=X0, B_j=Z0 X_j. Ordered words
span the same redundancy-free coefficient algebra used by the pilot.
Let alpha_i be the sign automorphism flipping O_i and fixing the other
generators. On the canonical qubits alpha_i(X)=Z_i X Z_i. Define

    partial_i=(I-alpha_i)/2, L=ad_H,
    S=exp(-beta H/2),
    ||X||_beta^2=tau(S X^dagger S X),
    E_beta(X)=sum_i ||partial_i X||_beta^2,
    B_beta(X)=sum_i ||[partial_i,L]X||_beta^2.

tau is normalized trace. Dividing these norms by tau(S^2) would use the
normalized Gibbs KMS metric and would leave EVERY ratio below unchanged.
The identity has zero gradient. The earlier trace-metric bound is
B_0(X)<=4d E_0(X). H-generated real-time conjugation is unitary in the
KMS norm, because H commutes with S; that fact alone does not control D.

The d-1 independent central involutions C_j=B_1 B_j, j>=2, give a projector

    P=product_(j=2)^d (I+C_j)/2,     tau(P)=w=2^(-(d-1)).

This is an explicitly described length-O(d) product of public operators,
not a supplied hidden state or a new oracle. Put

    Y=i A B_1,     X=P Y.

X is a nonzero Hermitian member of the original algebra. Its thermal mean
is zero. It is supported on a rare central sector, but a uniform operator
inequality must hold there as well. No sampling of that sector is assumed.

## 2. Two-By-Two Sector Calculation

In sector C_j=sigma_j, choose A=Pauli X, B_1=Pauli Z and
B_j=sigma_j Pauli Z. Then

    H_sigma=Pauli X+a_sigma Pauli Z,
    a_sigma=1+sum_(j>=2) sigma_j.

The all-plus sector selected by P has a=d. Flipping any leaf moves it to
a sector unitarily equivalent to a=d-2. Flipping B_1 also conjugates the
two-by-two block by Pauli X; forgetting this conjugation gives wrong signs.
Flipping the center is conjugation by Pauli Z within the same sector.

Let r_a=sqrt(1+a^2). For Hermitian T=t_x X+t_y Y+t_z Z, direct Pauli algebra
gives

    ||T||_(beta,a)^2 = t_x^2+t_y^2+t_z^2
        + (t_x+a*t_z)^2/(1+a^2) * [cosh(beta*r_a)-1].       (1)

In particular, Y has norm1 at every a. Define

    K_Z(a)=1+a^2/(1+a^2)*[cosh(beta*r_a)-1],
    K_X(a)=1+1/(1+a^2)*[cosh(beta*r_a)-1].

The center derivative of X is X itself. Each leaf derivative has two
orthogonal sector components of magnitude1/2, with a possible irrelevant
sign. Consequently

    E_beta(X)=w*(1+d/2).                                  (2)

The superoperator identity

    [partial_i,ad_H](X)=[O_i,alpha_i(X)]

holds for these unit couplings. The center contributes4w K_Z(d). Each
leaf contributes4w K_X(d-2), located in its flipped sector. Thus

    B_beta(X)/E_beta(X)
      =4*[K_Z(d)+d*K_X(d-2)]/(1+d/2).                      (3)

The common exponentially small weight w CANCELS. It cannot be used to
excuse the operator-norm failure or converted into an algorithmic cost.

Fix c>0 and beta=c/sqrt(d+1), so kappa=c^2 is constant, arbitrarily small.
Equation(3) grows as exp(c*sqrt(d))/d, up to constant factors. Its ratio
to the trace-bound scale4d diverges. No replacement4d*C(kappa) is valid
uniformly in d, for ANY finite function C at this fixed kappa.

## 3. The Actual Flow Also Violates Degree-Scale Gronwall

Failure of the defect estimate does not alone prove failure of the flow
estimate. The same witness gives a direct calculation, removing that gap.
Set r=sqrt(d^2+1) and t_star=pi/(4r). In the selected sector,

    exp(it_star H) X exp(-it_star H)
        =P*(d A-B_1)/r.                                  (4)

This is a quarter rotation of the Pauli vector Y. Applying(1) separately
to the center and every flipped leaf gives

    E_beta(exp(it_star L)X)/w
      = d/2 + d^2/(d^2+1)
        + d^2/[d^2+1]^2 * [cosh(beta*r)-1]
        + d/[(d^2+1)*((d-2)^2+1)]
          * [cosh(beta*sqrt((d-2)^2+1))-1].                (5)

At beta=0 this is slightly LESS than the initial value1+d/2, a useful
opposite control. At beta=c/sqrt(d+1), its ratio to(2) grows as
exp(c*sqrt(d))/d^3. But sqrt(d)*t_star tends to zero. The proposed
degree-scale exponential bound therefore tends to1 while the actual
squared gradient amplification diverges. This falsifies the flow bound
itself, not merely a sufficient proof of it.

## 4. A Strict Rational Certificate, Not A Floating Fit

Use d=65536 and beta=1/2056. Then beta^2(d+1)<1/64. Since r>=d,

    cosh(beta*r) >= sum_(k=0)^24 (beta*d)^(2k)/(2k)!.

Dropping the last nonnegative term in(5) gives an exact rational lower
bound on the squared amplification. Meanwhile pi<22/7, r>=d and
exp(x)<=1/(1-x) for0<=x<1 give

    exp(4sqrt(d)*t_star) <= 1/[1-22/(7sqrt(d))].

The producer compares these rational bounds STRICTLY. It also checks
the defect lower bound against4d, retains all fractions, and reports
inconclusive small examples honestly. No65537-qubit matrix is built.
The growing-d conclusion rests on(3)-(5), not on numerical extrapolation.

## 5. Why This Is NOT A Gap Or Preparation Counterexample

First, the SAME star has total squared coupling mass M=d+1. Therefore
beta^2 M<=1/64 lies inside the existing total-mass gap lemma in
`../hdqi-gap-baseline-2026-10-24/GAP_AND_BASELINE.md`. Its perturbation
radius obeys

    radius^2=(5/4)*exp(1/4)*beta^2*M <=5/192<1/36.

Hence that EXISTING local lemma gives the filtered-parent gap at least
25/36 throughout this temperature path. The upper estimate exp(1/4)<4/3
uses the same elementary geometric bound. This is a reused gap result,
not a new gap proof, and remains subject to the earlier lemma's scope.

Second, the existing signed-word classical comparator has

    C=Z_commuting/Z <=exp(beta^2 M/2)<=128/127.

Thus this is also inside its polynomial-envelope regime. It is not a
classically hard output family or evidence of any quantum advantage.

Third, the Gaussian filter can cancel what a pointwise real-time bound
cannot. X has only Liouvillian frequencies +/-2r. For the ACTUAL filter

    f_s(u)=exp(-u^2/8-u/4+i*s*u),

the maximum multiplier magnitude on X is exp(-v^2/2+v/2), v=beta*r.
Write R_flow for the exact squared amplification ratio in(5). Expanding
the two frequency components and using the triangle inequality gives

    E_beta(f_s(beta L)X)/E_beta(X)
       <=2*exp(-v^2+v)*(1+R_flow),                        (6)

uniformly in real s. For fixed c>0 this upper bound tends to ZERO.
This is an IMAGE estimate on this witness, not a general filtered
commutator bound, a thermal Poincare inequality, or a new gap theorem.

There is a stronger warning against discarding phases before integration.
The two Pauli directions Y and (d A-B_1)/r have purely imaginary cross
gradient inner product, so their real-time squared gradient is

    E_beta(exp(it L)X)/E_beta(X)
        =cos^2(2rt)+R_flow*sin^2(2rt).

For V~Normal(0,1/4), the ACTUAL LCU Gaussian time average is therefore

    A_s=E_V E_beta(exp(i beta(V+s)L)X)/E_beta(X)
       =1+(R_flow-1)/2*[1-exp(-2v^2)*cos(4vs)].            (7)

At fixed c and growing d, A_s diverges uniformly in s, whereas(6) tends
to zero. The phase-forgotten mean-square REAL-TIME commutator also obeys

    E_V ||(D U_(beta(V+s))-diag(U_(beta(V+s)))D)X||_beta^2
          / E_beta(X) >= (sqrt(A_s)-1)^2.

Indeed diag(U) preserves the product KMS norm of DX; Cauchy--Schwarz
bounds the cross term by2sqrt(A_s). Thus even Gaussian averaging AFTER
discarding the coherent phases does not restore a degree-only bound.
This does not compute or lower-bound the COHERENT filtered commutator.

The new obstruction is therefore sharply scoped: one cannot transport
the earlier trace-gradient Gronwall argument into the KMS geometry with
degree-only constants, even by proving the thermal estimate directly.
It leaves a frequency-resolved, Gaussian-filtered argument open.

## Verification, Falsifiers And Revised Next Step

The finite reference builds ORIGINAL canonical Pauli operators, their
central projector, physical matrix exponentials, KMS traces, commutators
and real-time evolution independently of the sector formula. It checks
both identities, including the B_1 conjugation and all zero-beta controls.
It also computes the actual energy-basis Gaussian image and checks(6).
Dense controls are capped at eight coefficient qubits; larger parameters
are analytical ledgers and exact rational certificates only.

A wrong sector multiplicity, wrong sign automorphism, omission of a flipped
sector, or confusion between image and commutator bounds would invalidate
the conclusion. The independent physical calculations target these errors.
No independent reviewer or proof assistant has checked the new derivation.

Do not infer that the general degree-scale gap is false, or spend a pass
on more star spectra. If returning to this preparation problem, attack the
FILTERED KMS Dirichlet form directly, retaining its Gaussian frequency
suppression and the same-input classical comparators. A proof that still
takes absolute values before the frequency integral must explicitly show
why it avoids(3)-(5). The prior real-time trace result remains correct.

# Mixed Gaussian pair: uniform composition and resource review

7 November 2026. **ACCEPT the full native composition with the explicit
thresholds and error allocation below.** These replace the working note's
qualitative threshold bands and close its numerical exponent gate. No
counterexample or remaining polynomial-bit obstruction was found. This is a
written copy-only learner for the entire stated two-component class, not a
novelty, classical-input separation, practical-cost or execution claim.

Read current STATE/TRAPS, MIXED_GAUSSIAN_PAIR_LEARNING.md, the independent
core/low-rank review and actual Theorem1 Eq(9) of 2409.17953. The separately
audited Gaussian CJ convention is retained, including its output-reference
parity circuit and reference correction. No new numerical experiment, Git,
network/API or implementation was used. Finite controls are not the basis of
the uniform bounds below.

## Concrete algorithm and estimation event

For n>=3 and 0<epsilon<=1/10 use exactly

    k=epsilon/[10^6(n+1)], tau=k,
    h=k^8, ell=k^40, zeta=k^10000.

Thus k<10^-7 and n<k^-1. Treat n<=2 by constant-dimensional tomography;
replace larger requested epsilon by min(epsilon,1/10). The empty system is
trivial. All density errors below are RAW trace norm, not trace distance.

Estimate every degree2/4/6 Hermitian Majorana moment to additive zeta,
simultaneously with failure at most eta/4. Independent Pauli measurements
cost O(n^6 zeta^-2 log(n/eta)) copies and polynomial gates per copy. Rescale
degree2j by (1-tau)^j; this is the exact moment law of common attenuation,
not a request for a new unknown-state source. Its error relative to the
original mixture is at most n*k, by applying Gaussian continuity separately
to the two branches.

Build the skew covariance, exterior forms H,J and contraction Gram. On the
estimation event, their operator/exterior Euclidean errors, and all H
restrictions used below, can simultaneously be bounded by

    delta0=k^9900.

For example H and J coefficient errors are constant multiples of zeta;
their Euclidean norms cost O(n^2) and O(n^3), the Gram costs another
polynomial factor, and four Rademacher columns cost at most (2n)^2.
These fixed-degree factors are much smaller than the 100-power reserve.
Use sufficiently accurate classical arithmetic, for example working
roundoff k^12000, to retain delta0 for the constructed data. Its BIT
precision is still O(log(n/epsilon)) with an absolute constant multiplier.

Use the following deterministic branch rule:

1. If the estimated ||H|| is at most 2h, use SMALL H.
2. Otherwise, if the estimated fifth Gram eigenvalue is at most 2ell,
   use LOW THIRD.
3. Otherwise use HIGH THIRD.

On the estimation event these imply respectively ||H||<=3h;
||H||>=h and lambda5<=3ell; or lambda5>=ell. No promise about distance
from a threshold is necessary. Eigenvalue and spectral-projector
computations use certified numerical tolerances within delta0.

## Small H, including vanishing weights

If min(p,q)<=sqrt(h), convexity plus the Gaussian trace bound gives distance
from the mixture to the mean Gaussian at most 2(n+1)sqrt(h). Otherwise
pq>=sqrt(h)/2. From ||H||<=3h and ||H||^2>=4a2^4,

    a2<=sqrt(3h/2),
    ||Delta-Delta_rank2||op <= sqrt(3)*h^(1/4).

Deleting the tail while retaining the SAME mean changes each branch by
less than tau/2 and therefore preserves physicality. The modified mixture
is exactly the mean Gaussian. The weighted, branchwise continuity error
is at most n*a2, not an error divided by a small mixture weight. Thus
4(n+1)k^4 is a conservative raw error for both cases. Estimated mean
covariance and Gaussian preparation add only their separately budgeted
errors. This also covers p=0 or1 without defining t or dividing by pq.

## High third: explicit inverse ledger

The Gram formula and S<=n give

    a3^2 >= ell/(4n),  a3>=k^21,
    pq >= ell/(16n)>=k^42,
    ||E^3|| >= 6*a1*a2*a3 >= k^63.

The restriction argument in the note is correct. For six independent
Rademacher columns, Pf(W^T E W) is a multilinear polynomial of degree6,
with second moment 6! sum_I Pf(E_I)^2. Hypercontractivity and Paley-Zygmund
give a good restriction with probability at least c=1/(4*3^12), for which
|Pf(A)|>=k^63 and det(B)>=k^252. This probability is a fixed, very small
constant, not an asymptotic efficiency claim about practical constants.

Try ceil(c^-1 log(4/eta)) independent restrictions and accept the first
whose ESTIMATED det(B) is at least k^300. The same estimated H is reused
classically; no fresh unknown-state copies or postselection are hidden.
All restrictions have uniformly bounded coefficients, so the estimation
event controls every trial, including the selected one. Good restrictions
pass. For EVERY accepted restriction, true det(B)>=k^301.

Both ||A|| and ||B|| are at most k^-10, a deliberately loose bound from
||W||<=sqrt(12n) and ||H||<=sqrt(2)n. The following table gives sufficient
bounds; all errors are absolute operator/Euclidean errors.

| Step | Bound or retained accuracy |
|---|---|
| True B | sigma_min(B)>=k^351; ||B^-1||<=k^-351 |
| Determinant perturbation | <=k^-60 delta0 |
| Fourth-root perturbation | <=k^-287 delta0 |
| Inverse perturbation | <=k^-703 delta0 |
| A0=-(det B)^(1/4) B^-1 | error <=k^-720 delta0=k^9180 |
| True restriction A | det(A)>=k^151; sigma_min(A)>=k^201, hence >=k^210 |
| Selected largest-magnitude A entry | true magnitude >=k^211 |
| Least-squares recovery of all alpha | error per vector <=k^8950 |
| Full E, with one common sign | matrix/form error <=k^8600 |
| t and p | absolute errors <=k^8300 |
| Each reconstructed branch covariance | operator error <=k^8000 |

Here are the conditioning details behind the table. The determinant bound
uses det(B)/||B||^5. The fourth-root derivative is bounded using true and
estimated determinants at least a constant times k^300; the inverse
identity bounds inverse perturbation by twice ||B^-1||^2 times input error.
The fourth root itself is at most k^-15. These give the stated 720-power
loss for A, including a constant reserve.

Also det(A)=sqrt(det B), and ||A||<=k^-10, proving the lower singular-value
bound. The map alpha -> A wedge alpha has minimum singular value at least
sigma_min(A), while ||alpha||<=sqrt(12n). Least squares is therefore stable.
The displayed formula for E(v,w) only divides by the selected A entry;
bounding its numerator products and summing over O(n^2) entries gives the
generous k^8600 error. The exact A0 is either A or -A; the recovered alpha
and E have the SAME sign, so this only swaps mixture labels.

For Q=E^3, fixed-degree exterior multiplication gives estimated error
<=k^8590. Use ||Q||>=k^63, ||Q||<=k^-4 and |t|<=k^-21 in
t=<J,Q>/||Q||^2. Quotient perturbation gives error <=k^8400, hence the
looser table bound. The derivative of
p=(1-t/sqrt(t^2+4))/2 has magnitude at most1/4. True p,q>=k^42 and
estimated p,q>=k^43; the derivatives of sqrt(q/p), sqrt(p/q) are bounded
by k^-70. These facts pay the final covariance reconstruction. Stable
evaluation or the supplied working precision handles cancellation in p.

All together this ledger loses fewer than2000 powers, not merely an
unspecified polynomial factor. The 10000-power moment precision is adequate.
Spectral clipping of a skew covariance to the operator unit ball is its
Frobenius projection. It cannot increase its Frobenius error relative to a
physical true covariance. Branchwise Gaussian continuity and the weight
error then bound the mixture error by, conservatively, k^7990.

If a capped restriction run finds no accepted matrix, return ABORT within
the learning failure budget. A failed numerical safety check may do the
same; the proved bounds ensure that none fails on the good event.

## Low third: use the estimated support as the reference

With ||H||>=h and lambda5<=3ell, the exact Gram identities imply

    pq>=h/(4 sqrt(2)n),  a1^2>=h/(sqrt(2)n),
    a3^2<=2n ell/h.

The gap between the fourth and fifth Majorana Gram eigenvalues is at least
h^2/n^2>=k^18. Davis--Kahan therefore bounds the distance between the true
top-four projector P and the estimated orthogonal projector P_hat by
gamma<=k^9881. Degeneracy WITHIN the four-dimensional subspace is harmless.
A stable orthogonal basis can be obtained by pivoted QR; since the rank is
four, selecting a well-conditioned coordinate minor costs only polynomial
factors in n. Complete it by Householder transformations. No eigenvector
gap inside the subspace is required.

Define the IDEAL nearby state using Delta'=P_hat Delta P_hat and exactly
the original attenuated mean covariance. Then

    ||Delta-Delta'||op <=4n sqrt(ell)/h+4gamma <=k^10.

Both nearby branches retain physical margin at least tau/2, not tau.
Weighted Gaussian continuity gives raw state error at most

    sqrt(2)n^(3/2)sqrt(ell/h)+2n gamma <=k^14.

Most importantly, P_hat^(wedge4)H=pq(P_hat Delta P_hat)^2 EXACTLY.
The measured projected moments therefore describe this nearby state
directly. The k^14 truncation error is never multiplied by an inverse
condition number. Only the delta0 measurement/arithmetic errors enter
the channel/core reconstruction.

For this reference, ||B||<=1-tau/2,
I+B^2 >=(tau/2)I and R>=(tau/2)I. Thus
||(I+B^2)^-1||<=2/k and ||R^-1/2||<=sqrt(2/k).
Estimated B and R retain margins at least k/4. The inverse identity bounds
the D perturbation by k^-6 delta0; successive products give R error
<=k^-8 delta0 and A0 error <=k^-9 delta0. The positive-matrix square-root
and inverse-square-root integral/Sylvester bounds then give errors at most
k^-10 delta0 and k^-11 delta0. Fixed-degree exterior products, mean-core
coordinates, and the constant-dimensional density reconstruction lose
fewer than30 further powers. It is sufficient to retain the looser bound
k^9800 for both the physical clipped core and the channel's Gaussian CJ
state. These estimates also include polynomial dimension factors.

The channel defined by the estimated C,B and its exact formulas for R,A0
is CP: its Schur complement is identically zero. Numerical rounding of
its CJ covariance can be clipped to the physical covariance ball and
charged by Gaussian continuity. One need not assume a positive minimum
eigenvalue for the CJ state. Parity-block PSD clipping and normalization
of the 4x4 core have only constant-dimensional trace error. Neither step
requires fitting an unknown Gaussian branch decomposition.

## Mixed-state output and finite clocks

For a corrected normalized ordinary CJ state and core of dimension d<=4,
the identity Bell outcome has ideal probability p0=1/d^2>=1/16. If their
prepared product differs by raw trace norm delta, the unnormalized
successful outputs differ by at most delta and the probabilities differ
by at most delta. For delta<=p0/2 the success probability is at least1/32,
and conditional output error is at most4d^2 delta<=64delta. This is a
constant amplification, valid for mixed states.

Budget epsilon/10^6 raw error for each known core/CJ preparation and for
the fixed corrections; the algebraic k^9800 errors are much smaller.
Use ceil(32 log(100/epsilon)) independent prepared-resource trials, stopping
on success, and a fixed fallback on total failure. Failure probability is
at most epsilon/100 and contributes at most epsilon/50 RAW error. The
whole circuit is finite and trace preserving. The resulting output error
from the preparation stage is below epsilon/20. Its retries consume only
fresh KNOWN prepared resources, never retained unknown input copies.

In the high and small branches, diagonal thermal-state preparation and a
known Gaussian unitary also admit a raw epsilon/20 budget. Classical
covariance diagonalization is used to reconstruct a matrix, not to infer
a separated eigenbasis; degeneracies and boundary eigenvalues introduce
no uncharged gap. Gate approximation is budgeted by the usual finite
circuit hybrid bound. The two-mode core is constant-dimensional.

In every branch, n*k plus its listed approximation error plus the
preparation budget is less than epsilon in raw norm, and hence more than
sufficient for the requested trace distance epsilon. Moment estimation
fails with probability at most eta/4 and the high-rank restriction clock
with probability at most eta/4. Other numerical routines can be capped
deterministically at the prescribed precision. Thus total learning failure
is at most eta/2, leaving slack; output retry failures are already charged
as state error rather than hidden postselection.

All arrays have polynomial dimension, every numerical precision and
intermediate magnitude has polynomial BIT length, and every copy/gate
count is polynomial in n,1/epsilon,log(1/eta), with very large fixed
exponents/constants. The result is restricted to the exact IID two-mixed-
Gaussian promise and ordinary qubit circuits. It does not establish
off-model robustness, more components, parity-restricted implementation,
classical hardness, novelty, or an executed full learner.

## Final addendum: direct preparation as at most four Gaussians

**ACCEPT this simplification as the preferred endpoint.** It supersedes the
physical CJ/Bell implementation above; that implementation remains a valid
alternative but is unnecessary. The statistical, branching, truncation and
inverse ledgers are unchanged, and the final preparation error only improves.

The reconstructed two-mode core commutes with parity. Diagonalize its two
2x2 parity blocks separately, obtaining

    sigma_hat=sum_(a<=4) w_a |v_a><v_a|.

Each vector in the even block is u|00>+v|11>, a pure BCS Gaussian, including
the vacuum and fully occupied endpoints. Each vector in the odd block is
u|01>+v|10>, a one-particle Slater determinant and hence also a pure Gaussian.
Here a Gaussian density operator may have odd parity support; the native
word EVEN means parity COMMUTING. No parity-sector state is excluded.

Compute their 4x4 core covariances G_a directly. The already proved abstract
CP/TP Gaussian channel sends them to the known n-mode Gaussian covariances

    Gamma_a=L G_a L^T+Z.

Linearity therefore identifies the desired output with the convex mixture
of these at most four Gaussian states. Prepare it by a classical random
choice of a followed by ordinary Gaussian-state preparation. No physical
channel dilation, CJ state, tensor-identification correction, Bell outcome,
retry, or conditional success is required in this implementation.

The quantitative comparison is direct. For fixed exact channel E,
||E(sigma_hat)-E(sigma)||_1<=||sigma_hat-sigma||_1. For the estimated
channel use R_hat=I-C_hat D_hat C_hat^T, so 0<R_hat<=I and ||L_hat||<=1;
the same bound holds for L. Uniformly over every physical G_a,

    ||Gamma_hat_a-Gamma_a||op
       <= ||Z_hat-Z||op+2||L_hat-L||op.

Gaussian continuity then bounds the channel-parameter contribution to the
mixture's raw trace error by
n*(||Z_hat-Z||op+2||L_hat-L||op). The preceding low-branch bounds put this
and the core error below the retained k^9800 allowance. Numerical covariance
clipping is charged as before. Approximate mixture weights contribute at
most their l1 error; a single raw epsilon/20 budget covers all output
weights, Gaussian branches and their gate approximations.

No spectral gap or positive weight is needed for the core decomposition.
Use a backward-accurate parity-block eigendecomposition and regard the
returned nonnegative weights and normalized vectors as defining a nearby
density matrix. Only its trace error matters; unstable individual
eigenvectors inside a degenerate block do not enter the proof. Zero-weight
vectors can be discarded. The matrices are constant-dimensional, and all
subsequent covariance and gate calculations have the polynomial BIT costs
already established.

The n<=2 direct-tomography branch admits the same parity-block decomposition
(at most four terms), the high branch uses at most two Gaussians, and the
small branch uses one. Thus the entire learner can return an explicit
known mixture of at most FOUR Gaussian states with the same uniform copy,
BIT and trace-distance guarantees. This does not claim recovery of the
original component parameters. It removes, rather than adds, an endpoint
assumption and leaves no new proof gate.

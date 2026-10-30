# Quaternion Receiver: Classical Readout Filters

2026-10-30. Continuation of QUATERNION_COVARIANT_RECEIVER.md. These are
scoped mathematical deductions and bounded controls, not an implemented
quantum receiver, a general lower bound, or a new speedup. Independent
automated review is not human peer review or proof-assistant certification.

## 1. The Scientific Decision

The native problem remains exact norm-q principalization of an explicitly
given left ideal over a totally definite quaternion algebra with growing
totally real center degree. On YES inputs its public normalized lattice
is L_I=O*a. The objective is to recover H*a, H=O^1, to the previously
derived rounding radius. Do not replace the input by hidden rotations
acting on arbitrary chosen probes or by a free orthogonal coset oracle.

The previous pass supplied polynomial-size informative Clifford records,
but only exhaustive decoding. This pass tests two cheaper proposals:
adaptive orbit-overlap optimization and bounded Hermite/parity statistics.
Both must beat classical algorithms with the SAME public basis and source
parameters. A hard-to-simulate measurement alone is not a useful decoder.

## 2. The Specified Finite Source Has Classical Sample And Query Access

Use the specified finite positive preparation, not an arbitrary circuit
that happens to approximately prepare a related ideal state. Write

```text
phi(k) = sqrt(P(z)*p_z(k))
```

when the grid cell k belongs to the packet of coefficient z, and zero
otherwise. Here P is the actual finite sequential coefficient law and
p_z is the normalized full-cell packet law. The packet supports are
disjoint. Neither law is silently replaced by an ideal lattice Gaussian
with an unavailable partition function.

Classical sampling uses the same conditional Gaussian integrals as the
preparation. To evaluate an amplitude, recover z by approximate inverse-
basis rounding of M^-1(h*k), then check the coefficient windows and the
packet's dyadic cell window. Occupied cells obey

```text
||M^-1(h*k)-z||_infinity <= 1/8.
```

Approximating this RESULTING vector within 1/64 leaves a rounding margin
9/64<1/2. Matrix entries alone accurate to 1/64 are insufficient: charge
conditioning and coordinate magnitudes. Off-support ties can be resolved
deterministically because candidate membership is checked afterward.

Freeze all finite arithmetic, support and padding choices. Increasing
evaluation precision must not change the state being evaluated. In the
native input the Gram entries are rational trace expressions:

```text
<b_i,b_j> = (1/2)*Tr_(F/Q)(trd(b_i*conjugate(b_j))/q).
```

For the order lattice use q=1. Thus Gram--Schmidt coefficients and the
coefficient centers can be evaluated as rationals; their floors need not
be floors of an arbitrary approximate real. Physical packet centers use
the already specified fixed dyadic approximations.

Centered coefficient windows and full packet cells give a conservative
lower bound on every positive joint probability of the form

```text
(product_i r_i^-1)*(h/nu)^N
    * exp(-pi*N*((K+4)^2+(T+4)^2)).
```

Its negative logarithm is polynomial in the charged source parameters.
Products, square roots and conditional integrals therefore admit relative
evaluation with polynomially many precision bits. Empty branches remain
exactly empty; rounded nonempty conditional probabilities must be defined
by normalized branch rules. A sampler using b decisions, each accurate
in conditional TV to tau/b, has total TV error at most tau.

This establishes approximate computational tractability (CT) for the
specified construction. It does not certify a compiled source backend.
The general simulation principle is established prior work:
[Van den Nest 2011, Lemma 3 and Theorem 3](https://www.rintonpress.com/xxqic11/qic-11-910/0784-0812.pdf)
give additive overlap estimation for CT states and matrix elements of
efficiently computable sparse operators. The input-specific contribution
here is verifying its access hypotheses for this source.

## 3. Overlap Optimization Has A Matched Classical Baseline

For two normalized CT states phi and psi, sample k from

```text
r(k)=(|phi(k)|^2+|psi(k)|^2)/2,
Y(k)=2*conjugate(phi(k))*psi(k)/(|phi(k)|^2+|psi(k)|^2).
```

Set Y=0 at a zero denominator, which has zero sampling probability.
Then E[Y]=<phi|psi> and |Y|<=1. This symmetric mixture avoids an unbounded
importance ratio. For complex additive error a and failure delta,
`m>=4*a^-2*log(4/delta)` samples suffice by two real Hoeffding bounds.

Use exact support detection and relative amplitude error eta<=1/8.
The induced score error is at most 6eta before final arithmetic error.
Project the computed score onto the complex unit disk. If its uniform
error is gamma, the sampler has TV error tau and the compared physical
states have ket errors e_phi,e_psi, the total additive error is at most

```text
a + gamma + 2*tau + e_phi + e_psi.
```

There is also a direct weak simulation of a fresh-copy Hadamard test:
after drawing k, output a bit with probability (1+Re(Y(k)))/2, or use
Im(Y). Independent scores Y_1,Y_2 give the SWAP-test mean through
Re(Y_1*conjugate(Y_2)). Uniform per-query errors accumulate linearly over
polynomially many classically adaptive queries. This does NOT cover a
coherent superposition of queries or retained postmeasurement systems.

Consequently a purported exponential speedup obtained solely by
polynomially many inverse-polynomial-accuracy orbit-overlap evaluations
followed by classical optimization already has a matched classical
baseline. The source's useful separation gap survives; its VALUE can
be queried classically. Finding the correct narrow region remains the
search problem for both approaches.

## 4. Matching-Width Passive Parity Means Are Also Estimable

This analysis concerns the continuous Gaussian source, with a separate
error budget for its finite approximation. Set oscillator vacuum width
equal to the packet width nu. A real packet center x corresponds to
the coherent amplitude `alpha_x=sqrt(pi/2)*x/nu`. For a known passive
mode transformation P=A+iB, P unitary, its exact packet kernel is

```text
K_P(y,x) = exp(-pi*(||x||^2+||y||^2-2*y^T*A*x)/(4*nu^2))
           * exp(i*pi*y^T*B*x/(2*nu^2)).
```

It follows from <alpha_y|Gamma(P)|alpha_x>, using the standard passive
coherent-state rule, for example
[Arrazola--Lutkenhaus, Section II](https://arxiv.org/pdf/1406.7189).
Here Gamma denotes the number-preserving action with its vacuum phase
fixed. Its magnitude is

```text
exp(-pi*(||y-A*x||^2+||B*x||^2)/(4*nu^2)).
```

This includes a product of selected output mode parities after a known
passive rotation V: take P=V^dagger*diag(+/-1)*V. Complex P must NOT be
treated as an ordinary real-coordinate reflection. It can mix position
and momentum. Total mode parity, in contrast, has P=-I and is identically
one on the centrosymmetric lattice source, hence reveals no orientation.

### One-Neighbor Classical Estimator

Use w(x)=exp(-pi*||x||^2/s^2), Z=sum_x w(x)^2, and draw x from w(x)^2/Z
using the public broad-Gaussian sampler. Choose R so its outside mass
is at most tau. Return zero for ||x||>R; do not condition away that mass.
For a retained x, approximately round M^-1(A*x) and let y be the
resulting lattice point. Return

```text
F(x) = (w(y)/w(x))*K_P(y,x).
```

Choose `0<r<=1/(8*||M^-1||)`. Accurate vector rounding finds any lattice
point at distance less than r from A*x, and there is at most one. If no
such point exists, the chosen point may be far away; this is harmless.
All omitted lattice points are at distance at least r. No CVP oracle,
hidden reduced basis, or exact near-half rounding operation is supplied.

Completing the square in y gives the UNIFORM bound

```text
|F(x)| <= exp(4*pi*nu^2*R^2/(s^2*(s^2+4*nu^2))) <= 2,
```

where the final inequality is an explicit additional width requirement.
It holds even if the selected y is not near A*x; no discontinuous
distance threshold or unbounded importance weight is needed.

The public minimum-distance lower bound is lambda>=1/||M^-1||>=8r.
Packing around an arbitrary center bounds the omitted Gaussian by

```text
sum_(k>=1) (k+2)^N * exp(-a*k^2)
 <= 2*exp(-a+N*log(3)),
a=pi*r^2/(4*nu^2),   a-N*log(3)>=log(2).
```

Multiplying by 1/w(x)<=exp(pi*R^2/s^2) shows that omitted terms in F
have magnitude at most epsilon_tail if

```text
a >= N*log(3)+pi*R^2/s^2+log(2/epsilon_tail).
```

This requires only polynomially many additional width bits. The previous
Gaussian Gram bound gives ||A_L||^2 in [1,1+eta]. Removing the x tail
changes <A_L|Gamma(P)|A_L> by at most (1+eta)*sqrt(tau). Ignoring the
remaining physical normalization changes the expectation by at most eta.
Thus, before sampling and arithmetic errors,

```text
|E[F] - <Psi_L|Gamma(P)|Psi_L>|
 <= epsilon_tail + (1+eta)*sqrt(tau) + eta.
```

Sampling variance is bounded by 4. Bounded-score numerical clipping and
the broad sampler's TV error can be budgeted in addition. Phase evaluation
must charge the R^2/nu^2 scale: polynomial precision BITS suffice, but
constant-precision mode matrices do not. Preparation ket error e adds at
most 2e to bounded-observable expectations. No finite Hermite transform
or alias/truncation implementation is certified by this calculation.

### Stronger Parity-Specific Simulator Without A Radius Cutoff

For the parity case P=P^dagger=P^-1, there is a simpler uniformly bounded
estimator. A=Re(P) is symmetric, so
`d_P(x,y)^2=||x||^2+||y||^2-2*y^T*A*x` is symmetric. Define the same
deterministic approximate-rounding map t(x) on every input. Retain a
pair only when y=t(x) and t(y)=x, including fixed points. If d_P(x,y)<r,
both coordinate distances are less than r, so both roundings must find
the pair. Therefore every omitted pair has d_P(x,y)>=r.

Split its Gaussian exponent in half. The absolute omitted row sum is
at most

```text
beta = exp(-pi*r^2/(8*nu^2))*rho_(sqrt(8)*nu)(L).
```

Indeed, the other half is bounded by the Gaussian centered at A*x,
and the shifted theta sum is at most the centered theta sum by Poisson
summation. Symmetry gives the same column bound. Schur's bound therefore
controls the omitted quadratic form by beta with NO coefficient-l1 or
radius factor.

Draw x from w(x)^2/Z. For a retained mutual pair, return

```text
Y(x)=2*w(x)*w(y)*Re(K_P(y,x))/(w(x)^2+w(y)^2);
```

otherwise return zero. Then |Y|<=1. Summing the two probabilities in a
two-cycle gives exactly its two ordered quadratic-form terms; a fixed
point also has the correct weight. Correcting the overlapping-source
normalization as above gives

```text
|E[Y]-<Psi_L|Gamma(P)|Psi_L>| <= eta+beta.
```

A coin with probability (1+Y)/2 simulates ONE product-parity outcome
to TV error at most (eta+beta)/2 before arithmetic, source and sampler
errors. Compute the weight ratio in a stable bounded form; do not divide
two numerically underflowed Gaussians. The approximation policy for t
must be fixed, with INPUT-DEPENDENT precision, and must approximate the
resulting inverse-coordinate vector accurately enough to preserve the
r-neighbor guarantee. One fixed-precision matrix does not give uniform
accuracy on an unbounded lattice. The stable weight factor is
`sech(pi*(||x||^2-||y||^2)/s^2)`. Sampler TV error sigma, clipped-score
error gamma and source ket error e add `2*sigma+gamma+2e` to the
expectation error. Half the total error bounds the one-bit TV distance.

The mutual-pair argument specifically uses Hermitian P. The preceding
radius-truncated estimator covers general passive P; do not silently
transfer the symmetric-pair proof to a nonsymmetric transformation.

### Scope Of This Falsifier

It simulates any specified polynomial collection of these bounded means,
including a joint parity involving every embedding. It does NOT sample
the full vector of number or parity outcomes from its exponentially many
Fourier coefficients. It does not cover arbitrary squeezing, a different
oscillator vacuum width, or coherent reuse of a measurement apparatus.
If widening/squeezing changes the source's packet covariance, rederive
the kernel and resource bounds; do not extrapolate this theorem.

## 5. Discarding An Embedding Removes The Useful Branch Coherence

This is an input-specific trace-distance bound, not an arbitrary local
measurement simulator. For distinct points x,y of the native normalized
ideal lattice, the reduced-norm ideal inclusion gives

```text
product_sigma ||x_sigma-y_sigma||^2
 = Norm_(F/Q)(nrd(u-v)/q) >= 1,       u,v in I.
```

The quotient is a nonzero totally positive algebraic integer. Normalized
coordinates need not themselves be integral. The same conclusion holds
without a hidden generator when the verified norm-ideal inclusion holds.
For ||x||,||y||<=R, every four-real-coordinate embedding block therefore
has separation at least `Delta_R=(2R)^(-(d-1))`. Without a radius cutoff,
units can make one embedding arbitrarily small. An arbitrary fractional
rescaling needs its own certified product lower bound; do not reuse 1.

Let j be any entire embedding block, let p_x=w(x)^2/Z and define

```text
Sigma_j=sum_x p_x |phi_(x_without_j)><phi_(x_without_j)|,
Theta=rho_(2nu)(L),
tau_R=2^(N/2)*exp(-pi*R^2/s^2).
```

With trace distance D(rho,sigma)=||rho-sigma||_1/2, the conclusion is

```text
D(Tr_j |Psi_L><Psi_L|, Sigma_j)
 <= sqrt(Theta*tau_R)+eta+tau_R,
```

provided `pi*Delta_R^2/(4nu^2)>=4*log(5)+log(2/eta)`, 0<eta<=1.
To see this without paying the number of lattice points, first truncate
coefficients at R. The full packet Gram norm is at most Theta, so the
discarded vector norm is at most sqrt(Theta*tau_R). The angle to the
normalized truncated ket has sine no larger than this quantity.

On the truncated set, the discarded-block packet centers are separated
in FOUR dimensions. Their off-diagonal Gram row sums are bounded by
`sum_(k>=1)(2k+3)^4*exp(-pi*k^2*Delta_R^2/(4nu^2))<=eta`.
For normalized positive coefficient vector c, Schur's bound controls
the sum of absolute cross-term coefficients by eta. Every remaining
rank-one packet operator has trace norm one. If E is the cross operator
and gamma=Tr(E), then ||E||_1<=eta and 0<=gamma<=eta. Correct normalization
gives distance at most `(eta+gamma)/(2*(1+gamma))<=eta` from the truncated
mixture. Restoring its classical coefficient tail costs at most tau_R.

For epsilon<=1, Theta<=2, tau_R<=epsilon^2/32 and eta<=epsilon/2 make
the total less than epsilon. These widths use polynomially many bits;
they must also satisfy the source's finite-encoding constraints. The
mixture's label law is the same PUBLIC broad lattice Gaussian, whose
sampling condition must be checked separately from shrinking nu.

Independent t-copy reductions differ from the product mixture by at
most t*epsilon. A classical simulator follows only for measurements
that can themselves be simulated on the sampled Gaussian packets (or
their products). Arbitrary circuits on known packets are not free to
simulate. Fresh-copy adaptive protocols sum uniform errors; retained
postmeasurement systems need a conditional-instrument simulator, and
postselection charges its success probability.

This does not cover all-embedding correlations, prior access to the
discarded block, coherent query superpositions, or discarding just one
real scalar coordinate. It explains why separate local reconstruction
is an unattractive next receiver without proving a general impossibility.

## 6. Clifford Records And Nonlinear Decoding Remain Distinct

For any fixed Clifford C and Boolean parity Z_S, C^dagger*Z_S*C is a
classically computable monomial Pauli. Its expectation on a CT source
is additively estimable. If a postprocessing statistic has an accessible
Fourier expansion

```text
g(b)=sum_S g_hat(S)*(-1)^(S.b),
L_g=sum_S |g_hat(S)|,
```

then coefficient sampling proportional to |g_hat(S)| gives additive
estimation in O(L_g^2/epsilon^2) trials, up to confidence factors. An
explicit polynomial list is sufficient; polynomial L_g alone does not
supply a coefficient-access algorithm. An accessible approximation with
small discarded Fourier l1 mass also suffices. For many source copies,
the promise must cover the whole joint-record statistic, not individual
bits in isolation.

An efficient classical decoder need not have small L_g. The elementary
quadratic sign product `(-1)^sum_j b_(2j)*b_(2j+1)` is computable in linear
time but has Fourier l1 norm 2^m on 2m bits. This is a countercontrol for
an invalid inference, not a new oracle problem or algorithm proposal.

Likewise the shadow score `(D+1)*|<phi|stabilizer>|^2-1` demands probability
accuracy of order 1/D. The overlap lemma gives polynomial cost in the
inverse ADDITIVE error, not its bit length. An O(1/sqrt(D)) amplitude
perturbation at a typical 1/sqrt(D) amplitude changes the score by a
constant. No exponential shadow-scoring lower bound follows, but neither
does an efficient decoder follow from the CT overlap lemma.

The remaining constructive target must exploit entire records through
an affordable nonlinear decoder, or a receiver outside the scoped
simulation classes. Merely adding more overlap, low-order moment, or
matching-width parity features does not remove the algorithmic blocker.

## 7. Dense Scores: Carries, Proxies And An Arithmetic Alternative

A binary stabilizer has support `b_0 XOR T*t`, t in F_2^r, with phase
`i^ell(t)*(-1)^Q(t)` and amplitude 2^(-r/2). Thus its overlap is a
weighted sum of the ACTUAL finite amplitudes a_g at these grid labels.
For full support, the shadow score is

```text
(1+1/D)*|sum_k a_g(k)*conjugate(phase(k))|^2-1.
```

The phases do not become ordinary arithmetic quadratics in lattice
coefficients. Take the native Lipschitz order, a=(3+4i)/5 and on-grid
straddle spacing 1/(5*2^t). On coefficient ray (n,0,0,0), a Z phase on
coordinate bit t+j pulls back to bit_j(3n). Binary addition gives

```text
c_2=n_0*n_1,
c_(j+1)=n_j*n_(j-1)+c_j*(n_j+n_(j-1)),
bit_j(3n)=n_j+n_(j-1)+c_j.
```

In the Boolean ring c_j contains the unique full degree-j monomial
product_(i<j)n_i. Only n_j*c_j creates the next full monomial, proving
degree exactly j for j>=2. Also, XOR-affine support need not be an
integer lattice coset: {0,3,5,6} is XOR-closed but not addition-closed
modulo 8. Keeping bits as variables instead gives a weighted Boolean
partition sum, not a free quadratic Gauss-sum algorithm. This refutes
one shortcut, not every carry automaton or tensor contraction.

Polynomial occupied support is a genuine efficient subclass: enumerate
its K labels and sum their stabilizer amplitudes with polynomially many
precision bits. K need not equal D. The test fixture O*5 versus
O*(3+4i), with finite broad-bin coefficients and on-grid straddles, is
orientation-informative but classically easy. Its rotated probability
of an integral point is close to 1/25, versus one in the unrotated case.
It is a countercontrol against a blanket scoring obstruction, not a
candidate problem; growing center degree destroys this support bound.

There is also an important statistical relaxation. For close normalized
target proxies phi,phi_tilde, let Delta=P_phi-P_phi_tilde. Global-Clifford
third moments give

```text
E_Born[(X_phi-X_phi_tilde)^2]
 = (D+1)/(D+2) * (Tr(Delta^2)+2*Tr(rho*Delta^2))
 <= 4*||phi-phi_tilde||^2.
```

An efficiently scored close proxy could therefore suffice without
uniformly accurate individual scores. No such general proxy with a
polynomial scoring algorithm is supplied. A Gaussian COMB is not a
single Gaussian state.

Changing measurement ensembles is not free. For a uniform complete-MUB
ensemble containing the computational basis and rho=P_phi, that basis
alone contributes

```text
E[X^2] >= (D+1)*sum_k p_k^3-2*sum_k p_k^2+1/(D+1).
Var(X) >= (D+1)/K^2-3   when support size <= K.
```

The legitimate finite straddle fixture, encoded in four large-prime
coordinate registers, violates a dimension-independent bound by over
10^40. This is NOT a result for the full multiqudit Clifford ensemble.

A concrete alternative is available in existing literature:
[Mao--Yi--Zhu, Theorem 4 and Appendix B](https://arxiv.org/html/2410.13572v2)
use a full random n-qudit Clifford, then one cubic phase gate and a
Fourier gate on that qudit. For prime p>=5 the gate has a nonzero cubic
coefficient over F_p. Their centered rank-one shadow bound is at most
15/2, independent of p and n; the Clifford-only general bound grows
with p. This repairs variance for that arithmetic ensemble, not decoding.

NEXT CONSTRUCTIVE CONTRACT: derive an explicitly charged contraction of
the actual lattice-weighted arithmetic quadratic-plus-cubic sums, with
prime-register compilation, support/wrap errors and score accuracy paid.
Naively expanding the extra cubic variable takes p terms, exponential
in log(p). Even efficient scoring would still leave orientation search.
Do not build another measurement wrapper or call this a solver before
one of those computational tasks is resolved.

## 8. Independent Direction Challenge And Verification

An independent reviewer initially ranked inverse-trace complete-cell
counting first, then withdrew that ranking after examining an actual
recurrence. In the original accepted-root coordinates put
`f_j(v)=inv0(b_j*c+V*v)`, `x_I=a+sum_j D_j*f_j(u_j)`. With hash blocks
M_j, the natural exact prefix table obeys

```text
R_(j+1)(tau,z)=sum_v R_j(tau+M_(j+1)*v, z+D_(j+1)*f_(j+1)(v)).
```

For r<=K the Vandermonde-derived columns D_j are independent, and each
f_j is bijective on its accepted alphabet. Distinct prefixes therefore
have distinct pivot contribution z: the unpruned table has 2^((n-1)*j)
states. For a full-row-rank k-by-B saved hash, feasibility pruning leaves
prefix dimension `(n-1)*j-k+rank(M_remaining)`. Parent recomputation on
all three cells in each frozen file gives n11 dimensions 0,10,15,15 and
n17 fixed/anchored dimensions 0,16,32,36,36. The terminal count precedes
nonlinear predicate pruning; it is not a solver lower bound.

The actual hash law includes deficient matrices; conditioning on full
rank changes collision probabilities and is not an authorized algorithm
change. Existing RS cubic identities are already identities after the
Vandermonde substitution, not additional independent constraints.
Thus no new hash-cell solver or higher closure sweep is commissioned.

Five focused agents contributed parity analysis/controls, marginal
coherence analysis/controls, shadow structure/controls, direction
selection, and independent CT/parity proof review. Review repaired the
rounding/precision/access wording and strengthened parity estimation to
mutual matching. The direction recommendation was revised rather than
retained because it initially sounded promising.

New files contain 32 controls: 5 CT, 8 marginal, 11 oscillator parity,
and 8 shadow structure. A combined 463 selected tests passed under
`-W error` with pytest plugin/cache autoload disabled. Four new Python
files compile; all 12 site JavaScript syntax checks pass; `qsearch.py
validate` reports valid=true with no issues. These are not a full-suite
certification. The earlier corpus SQLite lifecycle warnings remain a
separate mechanical task; they were not suppressed or repaired here.

All 13 central registry JSONs remain unchanged. No source/receiver
backend, CLI, UI, candidate promotion, quantum execution or Git write
was performed. No general dequantization or novelty claim is made.

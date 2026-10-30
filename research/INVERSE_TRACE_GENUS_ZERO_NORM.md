# Trace-Affine Targets: A Genus-Zero Classical Norm Algorithm

30 October 2026. Constructive classical progress, not a quantum speedup.
Newton developed the progression-specific success argument; Banach
independently challenged it and found no fatal gap. The parent checked
the primary divisor estimate and implemented exact finite controls.
This is automated mathematical review, not human peer review, a novelty
certificate, or proof-assistant verification.

## Result And Scope

Let q=2^n, N=n^2, K=floor(N/8), and let the N public evaluation points
alpha_i be distinct. Keep the original problem:

```
sum_i alpha_i^j x_i = 0,  0 <= j < K;
Tr(inv0(x_i)) = b_i,      inv0(0)=0.
```

If the public targets satisfy b_i=Tr(c*alpha_i+d0) for c!=0, there is an
expected-polynomial classical search algorithm for every odd n>=15.
Its conservative per-trial bound is greater than
1/[8*binom(e+3,3)], where e=2(N-K-1)+1. Thus the expected number of trials
is O(n^6), with polynomial-cost field/polynomial operations and standard
expected-polynomial finite-field factorization. A trace-affine realization
can itself be found or refuted by binary linear algebra in n+1 variables;
the replay implementation takes c,d0 explicitly and verifies the promise.

This covers some sparse patterns excluded by the existing dense-support
norm construction. It is NOT an arbitrary-target solver, uniform native
witness sampler, deterministic runtime guarantee, or efficient quantum
algorithm. Novelty relative to all classical coding literature is not
established. The polynomial guarantee is mathematical; a seeded PRNG run
is a reproducible control, not a proof of an IID probability statement.

## Construction Without Changing The Input

Put P(X)=prod_i(X-alpha_i), D=P', r=N-K-1, e=2r+1, and s=e-N.
Sample a uniform monic polynomial T of degree s and set

```
F = (D^2 mod P) + P*T.
```

There are q^s equally likely monic F of degree e in this progression.
Since P is squarefree, D is invertible modulo P. No target or evaluation
point is resampled after observing a trial.

The curve Y^2+Y=cX+d0 is rational:
X=(Y^2+Y+d0)/c. Form G(Y)=F((Y^2+Y+d0)/c), of degree 2e and leading
coefficient c^(-e). Its involution is sigma(Y)=Y+1.

Factor G over F_q. Every sigma-fixed irreducible factor must have even
multiplicity. For each exchanged pair with common multiplicity v, draw
j uniformly from {0,...,v}; put exponents j,v-j in h. Fixed factors get
half their multiplicity. Multiply the resulting monic h by the unique
square root of c^(-e). Then h(Y)h(Y+1)=G(Y).

All these allocations must be available, including interior exponents
for repeated factors. Choosing a canonical side is NOT the algorithm
covered by the success theorem. The implementation first factors F and
rejects odd inert valuations, avoiding composition/factorization of G
on rejected trials. A monic irreducible f of degree m splits exactly when
Tr(c*f_(m-1)+(m mod2)*d0)=0. This is the trace criterion for its residue
field Artin-Schreier polynomial, not a heuristic factor test.

Uniquely decompose h=U(X)+A(X)Y. Opposite degree parities give

```
deg U <= r,  deg A = r,  leading(A) = c^(-1/2),
U^2 + U*A + (cX+d0)*A^2 = F.
```

The notation c^(-1/2) means the unique square root of c^(-1).
The implementation obtains U,A by Horner reduction using Y^2=Y+cX+d0;
it checks the polynomial identity exactly, including its scalar.

Return x_i=A(alpha_i)/D(alpha_i), rejecting if A(alpha_i)=0 at any
one-target. Weighted interpolation gives every native parity equation.
At a nonzero coordinate, division of the norm identity by A_i^2 gives

```
x_i^(-2) = (U_i/A_i)^2 + U_i/A_i + c*alpha_i+d0.
```

Taking trace proves the target bit, since Tr(t^2)=Tr(t). A zero output
is valid precisely at zero-targets. This uses the original points and
does not square the output; the older constant-extension construction
has a different parameterization. An unrestricted native lift may need
deg U<N, so this restricted norm family is not the whole witness set.

## First Moment: Good Lifts Including Nonvanishing

For a trial F let R(F) count all normalized norm lifts, and J(F) those
satisfying every one-site exclusion. These are proof variables, not
quantities that the algorithm enumerates.

Use local coordinates a=A_i/D_i, v=U_i/D_i and C=c*alpha_i+d0. The conic
v^2+a*v+C*a^2=1 has q-1 points when Tr(C)=0, and q+1 when Tr(C)=1.
Delete (a,v)=(0,1) only in the latter case, leaving q allowed points.
Write psi(t)=(-1)^Tr(t) and Kl(t)=sum_(z!=0) psi(z+t/z). Exactly,

```
sum_(v^2+av+Ca^2=1) psi(xi*a+zeta*v)
  = q*1_((xi,zeta)=(0,0)) + psi(C)*Kl(xi^2+xi*zeta+C*zeta^2).
```

To derive it, introduce the constraint character lambda. At lambda!=0,
sum over v using psi(lambda*v^2)=psi(sqrt(lambda)*v). This forces
a=(sqrt(lambda)+zeta)/lambda; substitution gives the displayed dual
quadratic expression. Deleting (0,1) subtracts psi(zeta).

For nonzero Kl argument, the curve w^2+w=z+t/z has genus one and two
rational ramified points. Its point count is q+1+Kl(t), so the Weil
bound gives |Kl(t)|<=2sqrt(q); Kl(0)=-1. This is a standard application
of the characteristic-two curve bound, as stated in
[Carmon, Theorem 3.1](https://arxiv.org/html/1409.3694v1#S3).
Every nontrivial allowed-local-set Fourier coefficient is consequently
bounded by 2sqrt(q)+1.

The affine coefficient space deg U<=r, deg A<=r with A_r=c^(-1/2)
has codimension 2K+1 in F_q^(2N). Its two direction codes have dimensions
N-K and N-K-1. Their dual minimum supports are N-K+1 and N-K, so every
nonzero paired dual frequency touches at least N-K coordinate blocks.
Scaling by each nonzero D_i does not change these facts.

Set z=#{i:b_i=0} and

```
rho = (2sqrt(q)+1)/(q-1),
eta = (q^(2K+1)-1)*rho^(N-K),
L = (1-1/q)^z*(1-eta).
```

Fourier orthogonality counts at least q^s L good normalized lifts, hence
E[J]>=L. Require rho<1 and eta<1 for this positive certificate. The count
already excludes ALL forbidden zeros; it assumes neither independent
residues nor good allocations for every individual norm F.

## Second Moment And Algorithmic Acceptance

The affine coordinate ring is F_q[Y], a UFD. If all inert valuations are
even, R(F)=prod_(split primes f)(v_f(F)+1); otherwise R(F)=0. There is
no q+1 scalar factor: the norm of a constant is its square, whose square
root is unique. Locally (v+1)^2<=binom(v+3,3), so R(F)^2<=d_4(F).

Apply [Sawin, Lemma 8.7, printed page 59](https://arxiv.org/pdf/2102.09730#page=59)
with degree e, squarefree modulus P of degree N, invertible residue D^2,
and divisor parameter 4. This is the ORIGINAL progression, not a reversed
polynomial or a modulus with an extra infinity constraint. Define

```
C1 = (4^N-binom(N+3,3))*binom(3N-4,s),
C2 = 4^(N-1)*binom(3N-3,s+1),
B  = (q/(q-1))^N*binom(e+3,3)
     + 2*C1*q^(-s/2) + 2*C2*q^(-(s-1)/2).
```

The unrestricted total of d_4 on degree-e monics is q^e*binom(e+3,3).
Using it to upper-bound the coprime total in that lemma gives E[R^2]<=B.
Uniform independent choices j in the factor allocations sample exactly
one of the R(F) normalized lifts uniformly, without enumerating them.
With J/R defined as zero when R=0, Cauchy-Schwarz gives

```
(E[J])^2 <= E[J/R]*E[J*R] <= Pr[valid output]*E[R^2],
Pr[valid output] >= L^2/B.
```

This pays both polynomial rejection and invalid local zeros. A first
moment alone would not give this algorithmic guarantee. The necessary
leading-coefficient trace condition is automatic for norm lifts:
c*f_(e-1)+d0=(sqrt(c)*U_r)^2+sqrt(c)*U_r; no constraint was forgotten.

## Uniform Native Asymptotics

For odd n>=15, N=n^2, K=(N-1)/8, s=3(N-1)/4 and e=(7N-3)/4.
Let M=binom(e+3,3). The following bounds are analytic, not a finite sweep.

Since rho<=3/sqrt(q)<4/sqrt(q),

```
eta <= 2^(((28-3n)N+11n+4)/16) <= 2^(-N).
```

For the last inequality use 28-3n<=-17 and 11n+4<=N. Bounding each
binomial coefficient by its row sum gives C1<=2^(5N-4), C2<=2^(5N-5).
The two divisor error exponents are
((40-3n)N+3n-24)/8 and ((40-3n)N+7n-32)/8; each is <=-N/2.
Their sum is therefore at most 2^(1-N/2)<1/2.

Also N/q<=225/32768<1/4, since n^2/2^n decreases for n>=3.
Bernoulli's inequality yields L>9/16>1/2 and B<(4/3)M+1/2<2M.
Thus Pr[valid output]>1/(8M)=Omega(n^-6). Expected-polynomial factoring,
field arithmetic, interpolation, allocation sampling and verification
complete the classical expected-polynomial search bound.

At n17, N289,K36,e505,s216, exact rational bounds using ceil(sqrt(q))=363
give eta<2^-655 and divisor error<2^-551. Even with worst-case z=N,
the implemented certificate gives success >=1/21864708. This is a
conservative lower bound, NOT a prediction of observed trial counts.

## Failed Shortcut And General-Target Boundary

The parent initially proposed a derivative-root reciprocal-linear attack.
Heisenberg correctly refuted it: for S_j(a)=sum_i alpha_i^j/(alpha_i-a),
S_0=P'(a)/P(a), but S_1=N+a*S_0. At odd N, a derivative root still leaves
S_1=1. Omitting the polynomial quotient term was an error. The original
checks are unweighted; a weighted partial-fraction identity cannot be
substituted. The fixed n17 input additionally has no rational roots of P'.

A more general exact falsifier: if sum_i b_i is odd and
b_i=Tr(c*alpha_i+d0), no solution has x_i=inv0(g(alpha_i)) with
deg(g)+1<K. Test the code parity against (cX+d0)*g(X) and take trace.
The result is sum over nonzero coordinates of b_i=1, contradicting zero
syndrome; zero coordinates of a valid word have b_i=0. This includes
exceptional poles rather than silently assuming full support.

The constructive theorem cannot be generalized by merely optimizing the
trace interpolant for every sparse target. Points 0,...,N-1 contain the
binary subspace V={0,...,m-1}, where m is the largest power of two <=N.
For deg C<m-1, weighted interpolation on V (whose vanishing polynomial
has constant nonzero derivative) gives sum_(v in V) C(v)=0. Thus the
singleton trace target b_0=1, b_i=0 otherwise forces deg C>=m-1 for EVERY
trace-matching polynomial, including every Artin-Schreier gauge change.
For reduced odd degree 2g+1 this means g>=(m-2)/2. At n17, g>=127.

The earlier high-genus uniform-monic norm-proposal bound then gives at
most 2^289*(2^17)^(-127)=2^-1870 for its specified maximal-degree proposal
law, even after trace-only interpolation optimization. This is NOT a
lower bound for arbitrary algorithms, rational models with other poles,
nonuniform proposals, or the genus-zero target family established here.

## Implementation And Replay

Implementation: `theorems/inverse_trace_genus_zero.py`; controls:
`tests/test_inverse_trace_genus_zero.py`. The primary n17 artifact is
`research/classical_baselines/inverse_trace_genus_zero_n17.json`.
It preserves the complete public input, c,d0, both seeds, all failed
trial signatures, parameter hashes, successful polynomials and witness.
Original-instance verification is mandatory, not inferred from the bound.

The fixed n17 run used polynomial seed 1030, allocation seed 1031 and an
outer cap of 32. It returned a native witness on trial 15 in 158.27s.
The input has 33 one-targets, below K=36; the older zero-on-zero-target
dense norm method is inapplicable. The actual z=256 certificate is
1/21853701. These observed trials and seconds are not a scaling result.
A separate binary-polynomial arithmetic control verifies all 36 field
syndromes and all 289 reciprocal traces from the saved word, without
calling FLINT or the construction's verifier.

Before this protocol was finalized, an exploratory canonical-allocation
probe tried the same first eight polynomials and rejected all eight for
odd inert valuations. It produced no witness, did not test the required
allocation law, and supplies no hardness or probability estimate.

```
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -B -m pytest -q -p no:cacheprovider tests/test_inverse_trace_genus_zero.py
python -c 'from theorems.inverse_trace_genus_zero import *; p,c,d=trace_bit_instance(); r=run_experiment(p,c,d,max_trials=32); print(r["status"], len(r["trials"]), r["success_certificate"])'
```

The outer trial cap is not a wall-clock cap or a cap on FLINT's internal
factorization randomness. No field table, hidden witness advice, altered
target, quantum candidate admission, or production CLI is introduced.
Mechanical registry/CLI integration is a separate Gemini task and must
retain the trace-affine scope and randomized-allocation requirement.

# Native Measured Recovery Reduces To Near-Exact CVP

LOCAL DERIVATION / REVIEW PENDING. A source-specific reduction with a charged
polynomial copy surplus. NO near-exact CVP solver, scalable secret decoder,
source dequantization, cryptographic attack or novelty claim is supplied.

## Why The Metric Counterexample Is Not A Dead End

The paired lattice baseline correctly shows that Euclidean distance is not
maximum likelihood on each record. That does NOT imply that the nearest
code point cannot identify the planted secret over many IID records. This
pass derives the latter property for ORDINARY, unweighted Euclidean CVP.
The earlier paired metric is different; do not transfer this margin to it.

Use the exact covariant records y=(a.s+e1,c.s+e2) modq, q=3^r, with full
IID uniform labels a,c and the correlated noise law in
`TERNARY_COVARIANT_NOISE.md`. One pair is one original supplied qutrit. All
outcomes are retained. No narrow/Gaussian error or chosen labels are assumed.

## Wrong Secrets Have Exactly Uniform Residual Pairs

For fixed t!=s, let Delta=s-t and H be the image of a -> a.Delta.
This subgroup has order d=q/gcd(q,Delta_1,...,Delta_n)>=3, even when Delta
is nonprimitive. The two label shifts are independent uniform elements of H.
The error characteristic has support

    {0,+/-(1,0),+/-(0,1),+/-(1,-1)},

with coefficients1 and1/3. Convolution with uniform H^2 retains only dual
indices divisible by d in BOTH coordinates. None of the six nonzero indices
qualifies. Thus the wrong-secret residual pair is EXACT uniform on Z_q^2.
This averages over original labels; conditional on pinned labels it need
not be uniform. IID original pairs give IID wrong-secret costs. Different
wrong secrets' costs need not be independent; the union bound does not need
them to be. Original trace-distance error is charged separately.

## An Explicit Mean Gap For Euclidean Distance

Let c(x) be the centered representative in[-(q-1)/2,(q-1)/2] and

    W_t=[c(y1-a.t)^2+c(y2-c.t)^2]/q^2 in[0,1/2].

For every wrong t,

    B=E W_t=(q^2-1)/(6*q^2).

Each true marginal has density [1+(2/3)cos(2*pi*x/q)]/q. The finite odd-q
Dirichlet-kernel second derivative gives

    (1/q) sum_centered x^2*cos(2*pi*x/q)
        =-cos(pi/q)/(2*sin(pi/q)^2).

Consequently the true mean is A=B-delta, where

    delta=2*cos(pi/q)/(3*q^2*sin(pi/q)^2) >=4/81.

At q=3 the gap is exactly4/81. At q>=9 use cos(x)>=1-x^2/2,
sin(x)<=x and pi^2<10 to obtain delta>76/1215>4/81. Roots are powers
of3, so these cases exhaust the source. This improves a weaker1/30 bound.
No Gaussian covariance assumption or independence WITHIN a pair is needed.
The formula is a local derivation; bounded direct Born-law summation checks
q3/9/27, not a substitute for the algebra or external review.

For clarity, the summation identity can be derived without taking a fitted
limit. Put h=(q-1)/2 and D(theta)=sum_(x=-h)^h exp(i*x*theta)
=sin(q*theta/2)/sin(theta/2). At theta=2*pi/q, its numerator vanishes,
the numerator derivative is -q/2 and its second derivative is0. The quotient
rule gives D''=q*cos(pi/q)/(2*sin(pi/q)^2). Since
D''=-sum x^2 exp(i*x*theta), taking real parts and dividing by q gives the
displayed finite sum.

## Uniform Statistical Guarantee And Approximation Factor

Set eta=1/128. Hoeffding for M independent costs of range at most1/2 gives
each one-sided deviation probability <=exp(-8*M*eta^2)=exp(-M/2048).
With N=q^n secrets, union over the true upper tail and every wrong lower
tail establishes simultaneously

    true squared distance <= M*q^2*(A+eta),
    every wrong secret's best wrapped squared distance >= M*q^2*(B-eta).

Failure is at most N*exp(-M/2048). The conservative integer budget

    M=2048*(2*n*r+kappa+1)

is sufficient for failure<=2^-kappa, using3^(nr)<2^(2nr) and e>2.
This is original-qutrit consumption, not free extra records. Constants are
conservative, not fitted to the twelve small baseline controls.

Moreover delta-2eta>=175/5184 and A+eta<=1297/10368. Therefore

    (B-eta)/(A+eta) >= 1647/1297.

Any CVP solver with a NORM approximation factor gamma satisfying
gamma^2<1647/1297 must return a point in the true-secret code coset on this
event. In particular gamma=9/8 works, since81*1297<64*1647. The distinction
between norm and squared-norm factors matters. This does NOT make ordinary
LLL/Babai a sufficiently good approximation solver.

## Actual Reduction And Public Output Check

Stack ALL2M equations in A and compile the public lattice

    L=A Z^n+q Z^(2M), target y.

The existing systematic basis has determinant q^(2M-n) when A has unit
rank. The good uniform event implies injectivity: an aliased secret would
have identical costs and contradict the displayed strict separation.
An implementation retains rank failure as UNKNOWN; it is not conditioned
away in the probability derivation. The complete lattice uses ordinary
Euclidean rows, NOT the paired A2 embedding from the other baseline.

Since q Z^(2M) is included, the minimum distance in each secret coset is
exactly the sum of centered modular residual squares. Convert the returned
lattice point to its secret using the public unit-basis inverse, and verify
every equation. The target/lattice bit representation is polynomial, but
its dimension2M is large and no efficient9/8-CVP solver is granted.

A second public check does not pretend to certify approximation quality:
any candidate whose nearest wrapped squared distance is STRICTLY below

    M*(61*q^2-64)/384 = M*q^2*(B-eta)

is correct on the same uniform event. This covers adaptive candidate search
on the training records because the event already covers ALL wrong secrets.
Below-budget experiments do not inherit this confidence theorem. Membership,
distance and the threshold can be checked without finding the nearest point;
a declared CVP approximation factor cannot be verified from one point alone.

The approximation/copy tradeoff is explicit, not an arbitrary fixed target.
For rational0<eta<2/81, the squared factor must be strictly below
(1/6-eta)/(19/162+eta). Use ceil(1/(8*eta^2))*(2nr+kappa+1) originals.
The report retains three legal profiles: eta1/81 with norm13/12, eta1/128
with norm9/8, and eta1/4096 with norm19/16. The last allows a looser CVP
approximation but has an enormous, explicitly charged copy multiplier.
No finite surplus can cross the limiting squared factor27/19 using THIS
mean-gap bound. These constants are sufficient, not optimal or necessary.

For original batches at joint trace distance epsilon from the ideal source,
add epsilon to the complete failure bound. Preparation, QFT implementation
and approximate-CVP solver failures require their own additional accounting.

## Interpretation And Falsifiers

This replaces an unspecified likelihood optimizer with a concrete near-exact
CVP problem on an explicit random code lattice. It does not prove that this
special CVP family is easy, hard, or equivalent to worst-case lattice problems.
The [EDCP/LWE literature](https://arxiv.org/abs/1710.08223) has separate source
and parameter promises; this broad finite-envelope error is not Gaussian LWE.

Falsifiers: a nonprimitive difference retains a nonzero error Fourier mode;
the finite centered second moment disagrees with the formula; wrong labels
are secretly chosen/conditioned instead of IID; the code lattice is a proper
sublattice; a squared factor is passed off as a norm factor; a below-budget
control is certified; or an approximation oracle is called an implementation.
No hardness conclusion follows from the existing small Babai failures.

Next research should test a source-aware CVP algorithm, random-code geometry
or a global quantum receiver with a better cost than this reduction. Do not
implement more statistical-identifiability infrastructure without an actual
optimizer. External theorem review and novelty comparison remain required.

```
python theorems/ternary_native_cvp_reduction.py --write
node research/certificates/ternary_native_cvp_reduction_crosscheck.js
python -m pytest -q tests/test_ternary_native_cvp_reduction.py
```

Gemini/Antigravity owns routine CLI, registry, production validation and Git.
The complete reduction is a conditional algorithm specification, not an
accepted speedup candidate and not an implemented near-exact CVP solver.

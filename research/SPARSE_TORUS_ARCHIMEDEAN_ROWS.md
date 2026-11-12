# Certified archimedean rows for sparse function fields

2026-11-13. REVIEWED WRITTEN compiler, with the completed Claude report
and full308line independent derivation parent-read. It computes certified
ALL-branch archimedean logarithm rows in polynomial sparse-BIT time,
uniformly in growing variables, extension degree, atoms and binary
exponents. Every accepted output is correct; ABORT probability<=eta
after polynomially many independent trials. No finite-place or fullRel
algorithm follows from this result.

Input is the unchanged native monic irreducible f of degree n=delta,
with nonzero original Y-basis atoms u_i and explicitly sparse rational
coefficient functions. No root isolation, constant field, conjugate labels
or huge cyclotomic field is supplied. Requested row accuracy is2^-p.

The complete proof and explicit implementation-independent precision
schedule are in `audits/reviews/2026-11-13-sparse-torus-arch-clock.md`.
Actual primary source: Mehlhorn-Sagraloff-Wang1301.4870v2, Corollary1,
https://arxiv.org/pdf/1301.4870v2. It is applied to an EXPLICIT monic dyadic
approximation of the specialized polynomial at a fixed factorization
precision. The distinct-root-count premise of its later isolation
theorems is not used. Native coefficient approximation is paid separately.

## Mechanism and resource account

Use reviewed bounds H=2^b, d0=(L_d+1)beta,
U=[2(n+1)(d0+1)H]^(2n+4), e0=(n+1)d0, V=n!U^n.
The nonzero integer polynomials D,detJ,detA_i have l1norm<=V and
totaldegree<=Delta=n e0. They remain implicit. Write v=ceil(log2 V),
q=k+2, t=16q(v+1)+4 and

 N=t+v+ceil(log2(max(1,Delta)))+4.

Choose each torus angle uniformly on an N-bit dyadic grid. Iterated
Jensen gives nonnegative logarithmic Mahler measure, whence
E log^-|P|<=log||P||_1. Markov and coupling each grid cell to the
continuous torus give
 Pr(all |P(z)|>=2^-t)>=15/16.
The coupling error is at most2pi Delta V 2^-N<2^-t. Total degree
already pays the sum over variables; no numerical-degree loop occurs.

On this good event coefficient bounds and Cauchy's root bound put all
roots in |y|<=R=2^(b+t+1). Nonzero determinant/norm lower bounds, divided
by the upper bounds for OTHER branches, bound each |u_i(y_j)| away from
zero. The discriminant supplies separation>=2^-S for an explicit
polynomial S. Thus ALL branches, not merely a norm average, are controlled.

Compute each monomial's binary exponent dot dyadic angle exactly modulo1,
then approximate its complex exponential by certified rational series.
Common-denominator products are evaluated as circuits, not expanded in T.
A fixed denominator precheck either ABORTs or gives a lower bound that
pays all divisions on every subsequent sample, including bad samples.
The independent proof gives explicit native precision Q+E_nat and
fixed factorization accuracy b_fac, both polynomial in native bits and p.

Form the returned dense-in-Y dyadic root product exactly. Rational tests
check centers within2R, pairwise separation, and a coefficient-error
bound smaller than the product bound on disjoint circles. ROUCHE then
certifies one true root per disk and every root is covered. The same
disks and original-atom derivative bounds certify nonzero values and
logarithms with error<2^-p. Certified log/exp series and all rational
intermediates have polynomial bit cost. The n=1 and constant-polynomial
cases are explicit. No adaptive precision loop or root-count oracle is
hidden in bad-sample handling. Repeat at most ceil(log2(1/eta))+1 trials.

## Joint constants and normalization

Every accepted simple root extends to a holomorphic germ at the SAME
torus point. These give all n embeddings of F into a meromorphic germ
field. Algebraic constants map to constant complex roots, so for every
e in Alg each row evaluates the entire product u^e under one consistent
constant-field embedding. If its degree is c, each embedding occurs
n/c times. No computed constant field or conjugate grouping is needed.

Consequently (1/n)sum max(0,log|u^e|) is its archimedean Weil-height
contribution, whereas (1/n)sum |log|u^e|| is its absolute-log norm.
These must not be conflated. Multiplying the original row matrix by an
Alg basis bounded by Balg amplifies error by at most kBalg; increase p
by ceil(log2(max(1,kBalg)))+3 to pay it without expanding any products.

## Falsifiers and disposition

For f=Y^2+1 and atoms((3+4Y)/5,Y,T), every torus arch row is zero.
Alg=Z^2 x{0}, but Rel={(0,4m,0)}. The first constant has nonzero finite
valuations above5; the second is order4 torsion; T is nonconstant.
Thus arch rows replace neither Alg, finite places nor the identity step.

For f=Y^2-T with atom1/(T^(2^M)-1), every dyadic grid with N<=M is
singular. The logarithmic degree term in the paid grid prevents this
aliasing; ignoring it is not a valid precision shortcut.

The paid report's unverified root-finding import and unspecified accuracy
constant are now repaired by the actual source and independent schedule.
Its height terminology is corrected above. The growing-degree full
relation endpoint remains OPEN at complete finite support (or an exact
specialization substitute); supplied-prime rows and final log-lattice
recovery are separately reviewed. No quantum execution, practical runtime,
novelty, hardness or asymptotic separation is claimed.

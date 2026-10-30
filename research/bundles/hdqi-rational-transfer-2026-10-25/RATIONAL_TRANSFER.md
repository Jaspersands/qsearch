# Rational Thermal Compression: A Classical Attack

2026-10-25. Local constructive upper-bound argument, NOT independently
reviewed or formally checked. No novelty claim: pole/multipole approximation,
transfer matrices, root isolation and matrix-product-state sampling are
established techniques. This pass connects them to the exact SAME canonical
native-word output, with explicit approximation and normalization costs.

Implemented: exact rational uniform approximation certificates, polynomial
export, and a root-precision specification. Not implemented: certified
complex root disks and the complex-factor end-to-end sampler. The previous
bundle implements the real-rational finite-product sampler only. Keep that
boundary explicit when reporting progress.

## The Native Problem

Use the path-power input and native words of the preceding two bundles:
O_i=X_i product_{max(0,i-R)<=j<i} Z_j, H=sum J_i O_i, explicit rational
nonzero |J_i|<=1. The target is the distribution obtained by measuring

    exp(-beta H/2)|0> / sqrt(tau(exp(-beta H))),

optionally after local Hadamards. No thermal/eigenmode/amplitude oracle is
provided. Arbitrary coherent downstream decoding remains outside scope.

For alpha=ceil(m/(R+1)) hidden modes, the standard ECF transfer identities
give T(u)=product_k(I-u epsilon_k Z_k), with all occupation sectors equally
weighted by the canonical trace. See the preceding TRANSFER_WORD_SAMPLER.md
for the cited transfer construction and its native trace argument. Polynomial
identities extend from generic couplings by continuity; degenerate spectra
do not introduce a gap or overlap promise into the classical construction.

The central difference from quantum mode filtering is that this construction
does NOT resolve individual epsilon_k or divide by a probe overlap.

## 1. A Uniform Rational Tanh Certificate

The starting partial-fraction identity and dyadic multipole strategy are
classical prior art: [Lin, Lu, Ying and E, Section 3](https://arxiv.org/html/0906.1319).
We use a real, paired-pole variant so every finite certificate is rational:

    tanh(x)=sum_{n>=0} 2x/[x^2+c_*(2n+1)^2],   c_*=pi^2/4.

Fix A>0 and 0<delta<=1/4; require uniform error on [-A,A]. The following
bounds and rationalization are an explicit local derivation.

### Rational Constant

Use the alternating series for atan(1/5) and atan(1/239) to enclose
pi=16 atan(1/5)-4 atan(1/239). The identity follows from
(5+i)^4=(239+i)(2+2i) and the appropriate first-quadrant arguments.
Alternating-series remainders give exact rational endpoints. Square the
positive endpoints and divide by four to enclose c_*.

Choose the midpoint c>=2 with |c-c_*|/c_*<=eta<=delta/16. Replacing c_* by
c changes the infinite sum by at most eta/(1-eta): compare each denominator
with its (1-eta)-scaled exact denominator and sum the positive terms for
x>=0. Oddness handles negative x. The approximate infinite sum is <=2.

### Dyadic Blocks And Truncation

Block b contains n=2^b-1,...,2^(b+1)-2. Put q_n=(2n+1)^2 and let d_b be
the midpoint of its smallest and largest q_n. Then

    |q_n-d_b|/d_b <= 3/5.

Writing C_b=c d_b, expand 1/[x^2+c q_n] about x^2+C_b to K terms. The
relative remainder of this geometric series is at most (3/5)^K. Summing
the nonnegative original pole terms therefore gives total absolute error
at most 2(3/5)^K over ALL retained blocks, not that bound times their size.

Retain G blocks, N=2^G-1 pole terms. The tail is bounded, uniformly for
0<=x<=A, by

    (2A/c) sum_{n=N}^infinity (2n+1)^-2
        <= A/[c(2N-1)].

Choose K with 2(3/5)^K<=delta/4 and N>=2A/delta. Because c>=2 and N>=1,
the tail is <=delta/4. The constant error is <delta/8. The sum of all three
exact rational bounds is checked against delta before returning a record.

### No Enumeration Of Exponentially Many Poles

For each block compute moments mu_(b,k)=sum_n(q_n-d_b)^k. Expanding this
degree-2k polynomial reduces them to power sums. The recursion

    S_k(M)=[M^(k+1)-sum_{j<k} binom(k+1,j) S_j(M)]/(k+1)

computes sum_{n=0}^{M-1} n^k in polynomially many arithmetic operations
in k and log M, even when M is enormous. The implementation never iterates
over the effective pole count.

The final odd rational function is

    r(x)=x sum_b sum_{k=0}^{K-1}
                  2(-c)^k mu_(b,k)/(x^2+C_b)^(k+1).

Take E(y)=product_b(y+C_b)^K and combine numerators into B(y), so
r(x)=x B(x^2)/E(x^2). E(y)>0 for y>=0. The degrees and rational coefficient
bit lengths are polynomial in G,K and the input bit lengths; moments grow
only in bit length O(K log N). Here

    G=O(log(2+A/delta)), K=O(log(1/delta)).

These are conservative bounds, not best rational approximants. Large
constants are visible in the live degree records. Exact arithmetic certifies
the written inequalities; sampled grids alone would not certify uniformity.

## 2. Convert Approximation Error Into FULL Native State Error

Set A=beta*sum_i |J_i|/2, so A bounds beta epsilon_k/2 without finding the
energies. Choose delta=error/(4 alpha). Define

    p(z)=E((beta z/2)^2)-(beta z/2)B((beta z/2)^2).

This is an explicit rational polynomial with positive constant term. Clear
denominators and remove positive content to obtain integer coefficients.
Its degree L is at most 2GK. The even part of p has strictly positive
coefficients as a polynomial in z^2. In particular p(z)+p(-z)>0 for real z.

Factor p(z)=p(0) product_{j=1}^L(1-u_j z), counting multiplicities. The
transfer product A_p=product_j T(u_j) has kth occupation factor

    p(epsilon_k Z_k)/p(0)
        = [E((beta epsilon_k/2)^2)/E(0)]
                       [I-r(beta epsilon_k/2) Z_k].

The even-part ratio is a POSITIVE scalar independent of that occupation
bit. After normalization the mode angle is atan(r), whereas the true angle
is atan(tanh). Since atan is 1-Lipschitz, each angle error is <=delta.
Canonical trace orthogonality gives overlap product_k cos(angle_error_k),
so full normalized vector distance is <=sqrt(alpha)*delta<=error/4.
The native word map is an isometry because P(y)|0>=|y>. Therefore the bound
applies to the actual native pilot, not just a thermal density matrix or
occupation probabilities. Measurement TV distance cannot increase it.

## 3. Root Access And Normalization Are Not Free

The roots u_j are those of z^L p(1/z)/p(0). They can be complex or repeated.
Use square-free factorization to retain multiplicities and certified complex
root isolation/refinement, not an unverified floating `roots` call. Such
algorithms have polynomial bit complexity in degree, coefficient size and
requested refinement; see [Mehlhorn, Sagraloff and Wang](https://arxiv.org/abs/1301.4870).
No quantum mode separation or probe residues enter this calculation.

Let p(z)=sum a_j z^j. Cauchy's bound gives

    |u_j| <= U=1+max_{j>=1}|a_j/a_0|.

Crucially, normalization is well conditioned in the relevant absolute
sense. Since every C_b>0,

    E((beta epsilon_k/2)^2)/E(0) >= 1,
    ||A_p|0>||^2
      =product_k [E_k^2+O_k^2]/E(0)^2 >=1.

The product formula has one denominator E(0)^2 PER MODE. It follows from
the equally weighted faithful occupation trace, not a supplied success
probability. Both signs of a mode cannot be annihilated because its even
part is positive. Thus the exact reference product is nonzero. This lower
bound would be false for an arbitrary supplied polynomial; the code rebuilds
the native approximation record before issuing its rounding specification.

Round each u_j to a Gaussian rational within zeta<=1. Conjugate rounding
can preserve real final coefficients. For B0=U+2,

    ||T(u)|| <= (1+|u|)^m,
    ||T(u)-T(v)|| <= m |u-v| B0^(m-1),
    ||A_p-A_rounded|| <= L m zeta B0^(mL).

The first two inequalities follow by bounding the independent-set sums by
the corresponding unrestricted subsets, using |J_i|<=1. Telescoping the
product proves the third. Since the reference norm is >=1, normalized
state distance is at most twice this operator error. It suffices to choose

    zeta <= error/[8 L m B0^(mL)].

The root precision is O(mL log B0+log(Lm/error)) BITS, not B0^(mL) bits.
`root_rounding_plan` records a conservative integer bit target and explicitly
reports that it has NOT produced any root disks. Complex rounding error is
bounded in modulus; coordinate rectangles need a diameter meeting this bound.

The previous signed automaton extends algebraically to Gaussian-rational
parameters by conjugating the second factor of each right-environment
contraction. Squared amplitudes and branch probabilities are then exactly
rational; exact random-bit sampling applies. That extension and certified
root refinement are not yet implemented here. No random root sampling or
unpaid amplitude loading is allowed.

## 4. Asymptotic Consequence And Its Limit

The written construction combines L=O(log(2+beta*Lambda*alpha/error)
log(alpha/error)) factors with bond D=(R+1)^L. Arithmetic on the tensors
has polynomial bit length after the stated certified root rounding.
For polynomial beta and inverse output error in the explicit input length,
this gives a LOCAL ARGUMENT for a quasipolynomial classical upper bound:

    exp(O(log^3(input_length))) times polynomial bit arithmetic.

This is not polynomial dequantization, a best-known bound claim, an
independently checked theorem, or a completed executable full sampler.
It sharply narrows the quantum comparison: even a polynomial quantum mode
compiler would have to be compared with this quasipolynomial construction,
not exhaustive enumeration of 2^m native words. Fixed-range models also
have other strong tensor-network baselines. No implication about arbitrary
non-path ECF graphs or coherent downstream decoding follows.

The conservative degree is already 1104 for m=1024,R=31,beta=1,error=.01.
The associated formal bond is 32^1104. This is an asymptotic research
bound, not a practical classical simulation at that size. A source that
replaces this enormous bond with a tiny measured rank must prove the
approximation error and uniform rank claim separately.

## 5. Adversarial Audit And Next Decision

- No pole enumeration: test huge effective N using exact power sums.
- No numerical uniformity inference: all three error budgets are rational.
- No denominator sign assumption: E is explicitly a product of positive
  factors on the real axis, and polynomial export is tested exactly.
- No state/distribution substitution: dense controls compare the actual
  native pilot, including signs, with the full thermal vector.
- No free normalization: the faithful trace and positive even part give
  the explicit norm bound. Tampered approximation records are rejected.
- No free roots: multiplicities, complex disks, precision and bit complexity
  are charged. The code has not executed this remaining stage.
- No independence between different probe families is needed; this classical
  attack never constructs the hidden Majoranas.

Next: independently scrutinize the transfer-factor/trace/norm composition;
then implement certified complex factors and conjugate exact sampling only
if it remains useful. First optimize the rational approximation constants
with certified a-posteriori error, not uncontrolled bond truncation. If the
upper-bound argument survives, deprioritize this path-power family as a
major-advantage target and revisit native applications or structures not
covered by its signed finite-memory transfer construction.

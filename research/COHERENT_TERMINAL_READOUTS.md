# Coherent Terminal Readouts

Status: explicit polynomial-time terminal rules, finite verified outcome laws,
and a review-pending obstruction for fixed parities and source-uniform bounded
Fourier envelopes. No scalable advantage or novelty is established. This
extends the [coherent subset-phase workbench](COHERENT_SUBSET_PHASE_QUERY.md).

## Actual Rules, Not Optimal Tables

`coherent_walsh_terminal_decision` consumes actual source labels lambda_i and
observed Walsh bits y_i. It computes parity or compares their Hamming weight
with a declared threshold. Optional correction replaces

    y_i by z_i = y_i xor 1[chi_lambda_i(h)<0].

This uses the known singleton phase of the negative-character reflection;
zero characters do not flip. Character arithmetic is polynomial in symmetric-
group degree and bit processing is O(k). This does not obtain the labels or
replace the quantum front end. It adds up to k classical character evaluations
to the separately charged phase-query computation/uncomputation.

The experiment evaluates odd parity, all-zero acceptance and strict majority,
with and without correction. All-zero is threshold one with the accepting
orientation explicitly complemented. The evaluator never silently reverses
a rule whose acceptance gap is negative. Thresholds are fixed formulas, not
fitted per source. These are analysis-driven calibration choices, not a
preregistered or held-out discovery claim.

For each rule it records the signed acceptance gap, equal-prior success,
the stronger joint source/decision Bayes-table distance, and the disjoint-pair
baseline. The joint table is NOT used by the executable rule. In S3 the
partial-involution controls are finite diagnostics; the exported polynomial
arithmetic interface is for even-degree fixed-point-free inputs.

| Control | Declared Corrected Rule | Signed Gap | Disjoint-Pair Gap |
| --- | --- | ---: | ---: |
| S3, k=12 | All zero | 0.947241 | 0.960600 |
| S3, k=12 | Strict majority | -0.205366 | 0.960600 |
| S4, k=8 | All zero | 0.919075 | 0.847412 |
| S4, k=8 | Strict majority | -0.239891 | 0.847412 |

The S4 all-zero rule attains the full finite Walsh distance, but its phase
has commuting V4 support. The growing-degree bound below supplies an
independent reason not to extrapolate this calibration into an algorithm.

## Random Two-Subset Representation

The full-mask selector state conditioned on source labels and a hidden h is

    sigma[S,T] = 2^-k Tr(rho_(lambda,h) U_T^dagger U_S).

For fixed positions B, Walsh-output parity chi_B(y)=(-1)^(sum_(i in B) y_i)
has expectation

    mu_B = 2^-k sum_S Tr(rho_(lambda,h) U_(S xor B)^dagger U_S).

The average is real: the term with S xor B is the conjugate of the term with
S. Choose S uniformly with classical randomness independent of the input,
perform a Hadamard test of the unitary U_(S xor B)^dagger U_S, and report its
bit. Its probabilities (1 +/- Re mu_B)/2 exactly reproduce the coherent
parity law, for EACH source and EACH h. This preserves the complete joint
law with all original source labels after natural source weighting.

The verifier independently constructs the actual physical unitary products
and compares their averaged Hadamard expectations with parity sums of the
direct Walsh probability law. It checks full parity and overlapping/partial
positions, complex phases, zero-alternative-mass sectors and every hidden
member. It never inserts independent h values in different copies.

This representation uses two subset-phase operations, not a classical solver.
Known clean-GPE circuits allow a controlled phase predicate followed by full
uncomputation; no generic ability to control an unknown black-box unitary is
assumed. The source-extraction cost remains. Each fixed S execution lies in
the algebra of the at most three nonzero membership-pattern cells of S and
S xor B. Full parity uses just two disjoint cells.

## Uniform Cell Bound

Invoke the earlier [source-conditioned lifting bound](SOURCE_CONDITIONED_PALETTE.md),
not exact copy compression with source labels silently removed. Write
G=n!, M=(n-1)!! and a=ceil(4n/3). Retain each cell of width below a as FULL raw
inputs and lift each larger cell. With at most c cells, retained raw copies r
and lifted cells ell obey r+ell <= c(a-1). Hence every fixed S output has
distance at most

    delta_c <= k/(2 sqrt(M))
       + (1/2) sqrt((2^(c(a-1))-1)/M)
       + (c/2) sqrt((G-1)/n^a)
       + (c/2) sqrt((G-2)(9/n)^a).

Clip individual comparison distances and the final bound at one. For n>=10
the cell errors decrease with width; n=8 remains vacuous. Maxima in this
conservative sum need not be simultaneously attained. Also take the minimum
with the raw-copy bound sqrt((2^k-1)/(4M)). Empty parity needs only the source
prior term. Exact integer outward dyadic rounding prevents underflow.

Because the random S distribution is identical under both hypotheses, the
mixture pays an AVERAGE bounded by the uniform maximum delta_c, not an
exponential catalogue cardinality. This is different from choosing a subset
based on measured source or quantum outcomes. For polynomial k and c<=3,
all four terms vanish superpolynomially as n grows. At S1024,k=17528 the
generic nonempty parity bound is T<=2^-141; the full-parity specialization
gives T<=2^-278. The S128 generic profile estimate is vacuous, not a positive
signal. The earlier few-bit marginal bound can be stronger where applicable.

This does not reproduce a JOINT VECTOR of parities from separately executed
Hadamard tests. It does not cover source-selected B, arbitrary subsequent
joint selector processing, retained physical outputs or multiple coherent
queries. The source-conditioned lifting derivation is still review-pending;
these consequences are not independently certified theorems.

## Fourier Transfer and Its Source Condition

For a specified binary decision f_lambda(y) in {-1,+1}, expand

    f_lambda(y) = sum_B c_B(lambda) chi_B(y).
    A = sum_B sup_lambda |c_B(lambda)|.

Since the parity bound retains all source labels, each coefficient-weighted
expectation difference is at most 2 sup_lambda|c_B(lambda)| delta_B. Therefore
the absolute acceptance-probability gap is at most A max_B delta_B.

The supremum belongs INSIDE the sum. A small norm separately for each source
does not suffice: a source can select a different parity B for each label,
giving norm one in every source sector but an arbitrarily large common
envelope. A regression test keeps this counterexample explicit.

For source-blind functions A is the ordinary Fourier l1 norm. Source-dependent
BIT FLIPS multiply each fixed Fourier coefficient by a source-dependent sign,
so they preserve this common envelope. The signed all-zero/any-one function
has A=3-2^(2-k)<3. Thus source-phase-corrected all-zero acceptance is also
obstructed; the S1024 control gives absolute gap <=2^-139. This is a bound on
the specified terminal decision, not a free optimal source-conditioned table.

Source-blind thresholds were already covered by the earlier discarded-label
selector bound, regardless of their Fourier norm. The genuinely unresolved
case here uses source information, for example corrected majority or a
different source-aware collective decision.

## Why Cheap Majority Is Not Disposed Of

The audit computes exact symmetric Walsh coefficients by the recurrence for
the coefficients K_w(d) of (1-z)^d(1+z)^(k-d):

    K_0=1, K_1=k-2d,
    (w+1)K_(w+1)=(k-2d)K_w-(k-w+1)K_(w-1).
    c_d=2^-k sum_w f(w)K_w(d),
    A=sum_d binomial(k,d)|c_d|.

Independent binomial expansion reconstructs every Hamming-weight value in
the tests. For odd majority k=2m+1, even-degree coefficients vanish and

    |c_(2j+1)| = [binomial(2m,m)/4^m]
                  * binomial(m,j)/binomial(2m,2j).

To derive this, take a discrete derivative in one coordinate: it is nonzero
only when the remaining 2m coordinates are balanced. Their even-product
moment is the coefficient of z^(2j) in (1-z^2)^m, divided by binomial(2m,2j).
Consequently

    A = [binomial(2m,m)/4^m]
          * sum_j [(2m+1)/(2j+1)] binomial(m,j)
      >= binomial(2m,m)/2^m >= 2^m/(2m+1).

Majority therefore has exponential norm despite linear-time evaluation.
At k=127 its exact norm exceeds 2^60. Parity, conversely, has degree k and
norm one. Degree, coefficient norm and evaluation time are distinct costs.
Nor can one simply approximate an arbitrary majority by a low-degree
polynomial: its constant-error uniform approximate degree is linear in k,
as established by [Paturi, Theorem 1](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/Paturi_1992_stoc.pdf).
That prior-art fact is not a claim about our hypothesis-specific distributions.

## Research Decision

Cut fixed-parity and source-uniform polynomial-envelope readouts as positive
one-query routes. Keep the all-zero control precisely because it gives a
large finite success rate while failing the growing-degree argument.

Do not claim the entire coherent measurement is dead. Source-aware majority
and other genuinely collective large-envelope rules are not ruled out here,
but the implemented majority rules are weak in the available controls. The
next useful work is a source-conditioned Hamming-weight generating-function
or conjugacy-word contraction at growing degree, with a specified terminal
rule and declared measurement costs. Do not extend the S4 V4 exception or
replace correlated source/selector laws with product marginals.

Reproduce with `python qsearch.py run EXP-COSET-BINARY-CARRIER-INSTRUMENTS`,
then `dequantize`, `proofs`, and `validate`. The existing experiment and
proof tracker retain both the obstruction and its explicit nonextensions.

Normal registry bootstrap now inserts missing seed experiments without
overwriting existing protocols, statuses or metrics. Previously, later CLI
commands could silently replace the writer's research record with seed
defaults. Definition updates must be explicit, for example by the owning
experiment writer; a normal read/validation command must not perform them.

# A Uniform Clock For The Conditional Geometric Source

2026-10-26. Written composition argument, not an implemented coherent source.
This addresses the uniformity part of review Finding 3 at fixed dimension.
It has not received independent review. It retains the exact published PPAV
model algorithms as imported dependencies, and does not repair native
reference-curve/dictionary preprocessing (Finding 1).

## Contract

Use the augmented suborder input of SUBORDER_TRANSCRIPT.md: supplied curves
E0,E in characteristic p>3; evaluable full source order O0; genuine global
dictionary theta into an evaluable target suborder; and N with theta(N O0)
contained in that suborder. Set m=N/p^v_p(N). Factorization, native evaluator
lengths/running times, finite-field encodings and their embeddings are paid.
The m=1 branch needs no hidden-kernel oracle.

Fix g=16. The geometric dependency is the explicit proto-efficient theta
model of [Corte-Real Santos, Piasecki and Wesolowski](https://eprint.iacr.org/2026/1142),
Theorem 6.25, with its always-correct expected-time algorithms on represented
objects. A1 is UNIFORM over inputs of a given length, not an average over
group queries. Compact object encodings, point arithmetic, additive-length
morphism composition and finite theta-coordinate orbits supply the bounds
below. This is an application of that model theorem, not a verification of
every proof within the paper.

The new genus-one algorithm supplies the original endpoint models and point
conversion maps after the existing fixed elliptic field normalization and,
if necessary, a further degree-four normalization-root extension. The latter
gives the conservative common base F_(q^48) and preserves scalar Frobenius.
Keep one base field k=F_Q and its embeddings fixed for the whole instance.
All maps in the source construction and all geometric homomorphisms between
its scalar-Frobenius objects are defined over this base. Do not change the
coefficient field or minimize over its Galois orbit during label computation.

## 1. Global Plan Before Any Group Query

Let L bound the native input lengths, log(p), log(N), the explicit base-field
description, source-basis heights, and the known evaluator descriptions.
Let E_eval(L,z) be the charged polynomial cost of those fixed evaluators on
z-bit points. L must not be replaced by log(m) alone.

The actual double-level compiler has at most 36 elementary matrix factors,
expanded to at most 144 quaternion factors with coefficients bounded by m.
For S0=sum_i Norm(b_i), its public trace bound is

    T=(2+4*m^2*S0)^144.

Hence log(T)=O(L), uniformly for EVERY query in Sp4(Z/m). Choose one odd
squarefree quotient multiplier Delta>T^2 from successive primes avoiding
pN. Choose disjoint marking primes with product Rmark satisfying

    Rmark^2 > 8*16^3*(p*m)^2.

The p*m bound is essential; the actual unknown degree need not be m.
Let s be the total number of auxiliary primes and R their maximum. Both
are polynomial in L. For example, Chebyshev bounds on the product of primes
give a polynomial cutoff in log(T)+log(pN); omitted primes have total
logarithmic mass at most log(pN). Trial division/primality checking at these
polynomially bounded integers is already polynomial in L. The large prime
factors of m are NOT auxiliary point orders.

Freeze this plan, endpoint theta frames, per-level fields, torsion bases and
projective intertwiner transcripts before coherent queries. They are paid
classical preprocessing, not query-dependent advice or samples of a maximum
trace. The new source splitter constructs the abstract split at m separately.

## 2. Bounds That Do Not Grow By Repeated Polynomial Composition

For each auxiliary prime r, scalar Frobenius gives a point field k_r/k of
degree at most r-1. Keep each k_r as a separate represented extension of k.
At each quotient stage the kernel list contains exactly r^16 points. Every
intermediate object is a dimension-16 PPAV over k, not over the compositum
of previously visited point fields.

Object coordinates have O(4^g log(Q)) bits; a point at level r has at most
O(4^g R log(Q)) bits after canonical conversion back to its fixed field.
The whole collection of s kernel lists has size at most

    O_g(s R^17 log(Q)).

Each atomic quotient encoding has this kind of bound. Prefix morphisms are
flattened chains; the additive encoding-length guarantee prevents duplicating
the previous chain recursively. Logarithms of norm bounds add. The bit lengths
of all four-square coefficients and arithmetic lift data are polynomial in L.

Thus there is a uniform polynomial M(L) bounding every interface input. One
may take a conservative sum of the original input, elementary/coin arithmetic,
s R^17 log(Q), marking tuples, and flattened morphism encodings, with constants
depending only on g. Do NOT argue merely that a polynomial-time routine is
called polynomially many times: without these size bounds, iterating a
length-expanding routine could produce L^(c^s).

### Temporary fields must be normalized between calls

When evaluating a quotient encoded using its kernel field k_r at a point in
k_t, temporary arithmetic may use the joint field of degree at most
lcm(r-1,t-1)<=R^2 over k. Because the map is defined over k, its output lies
in the fixed point field k_t. Normalize projective coordinates and descend
them through the specified embedding after EACH stage. The same applies to
other temporary field presentations. Inverse embedding is finite-field
linear algebra on polynomial-size representations; check Frobenius membership
and never replace a value by an arbitrary conjugate.

Alternatively the imported model's field-preserving routines may compute
directly in k_t. Either implementation must enforce the same bound. Letting
every temporary field become the next base is not this algorithm. A full
field-tower implementation and this normalization policy have not run here.

## 3. One Expected Polynomial Bound For The Whole Label

Let P_g(z) bound the finite suite of imported model routines on z-bit inputs;
g is fixed. Such a uniform polynomial is the A1/theta-model dependency. Let
P_field bound specified-embedding construction/descent and scalar arithmetic.
The number J(L) of model invocations is polynomial: a conservative count
includes O_g(s^2 R^16) point transports, O(s) quotients, and the constant-size
theta-coordinate/automorphism orbit times O(sR) marking comparisons. The
two r^2 transcript tables and all evaluator calls are charged in preprocessing.

Consequently a bound of the following form applies uniformly to every query:

    B(L) = P_arithmetic(L)
           + J(L) * [P_g(M(L)) + P_field(P_g(M(L)))],

with the fixed evaluator costs included wherever not precomputed. This is a
polynomial because the nesting depth is FIXED, not the number of stages.
Conditional expectation and summation suffice for adaptive intermediate
choices: each stage has the same input-size envelope. Independence between
subroutine running times is unnecessary.

The symbols P_g and P_field stand for the bounds of explicit imported
algorithms. This is a theorem-level uniform polynomial bound, not a numerical
runtime estimate for an implemented geometry backend. Selecting constants
and compiling these routines into actual circuits remains implementation
work; no measured Python runtime is substituted for B.

## 4. Bounded Reversible Evaluation

For any valid query x, run the complete always-correct classical label
algorithm for at most 2B(L) steps. Markov's inequality gives timeout probability
at most 1/2. Repeat with h independent random tapes, choosing the first
successful result; on total timeout return a fixed padded failure flag.
Every successful result is the SAME canonical marked label, independent of
random choices, auxiliary coordinate representatives or retries.

The query domain satisfies |Sp4(Z/m)|<m^10. With

    h = ceil(10*log2(m)+log2(1/delta)),

a union bound over ALL queries makes the probability of any timeout at most
delta. No independence across queries is needed. Sample the master tape ONCE
classically and reuse it for the quantum computation. With probability at
least 1-delta, this one bounded deterministic program computes the exact
hiding label on the entire query domain. This is stronger than pointwise
accuracy for the queries seen in a classical test run.

Compile the fixed-tape bounded classical program reversibly, copy the padded
canonical label, and reverse every work register, including branch choices,
field construction, point normalization and timeout records. Output width is
bounded by M(L). On a good tape this is an exact oracle for every superposed
query. On a bad tape no advantage claim is made; its total classical mixture
weight is at most delta. There is no extra factor for the number of oracle
calls when the good-tape event already covers the whole domain.

This is a standard reversible-simulation/probability argument. It is not a
constructed dimension-16 source circuit, and does not apply to an algorithm
that sometimes accepts incorrect labels. Failed/capped computations must
remain failures; guessing a label would invalidate the argument.

## Scope After This Pass

The former represented-endpoint assumption now has a concrete genus-one
conversion, and the uniform-clock obligation has the size and probability
argument above, conditional on the imported geometric-model theorem. These
are subsequent proposed repairs of Finding 3, not a second independent review.

Still unexecuted: finite-field tower integration, dimension-16 kernels and
quotients, complete canonical marked labels, a coherent circuit, quantum
kernel recovery and effective target endomorphism output. Native-suborder-only
preprocessing (Finding 1), novelty, and advantage over the strongest native
classical methods also remain unsettled. No unconditional full native solver
or Shor-level result follows from the conversion tests.

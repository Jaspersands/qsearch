# Native Inverse-Trace As A Modular Norm Problem

Status: written deductions with exact executable controls, not independently
reviewed or proof-assistant formalized. No new native search algorithm,
quantum algorithm, hardness proof, or novelty claim is established.

## Scientific Question And Answer

Can the SAME native inverse-trace relation be put into a coding-theoretic
key-equation form without discarding most codewords or supplying the answer?

There is a lossless modular norm formulation for the all-one, odd-degree
native family. For ONE supplied carry polynomial, norm factorization and a
two-variable linear system give an exact existence test, unless the charged
factor-orientation cap is exceeded. The carry is missing input, not free
advice. Uniform carry guessing is provably a poor proposed acquisition
method: success per draw is at most 2^-((n-1)(K-1)).

The preceding low-degree-square/global-identity obstruction remains true
in its restricted scope. It does NOT exclude this lossless formulation.
The frozen native witness has P degree 42 with 21 nonzero odd coefficients,
Q degree 48, and nonzero carry degree 47. Thus its P is not a polynomial
square, although P = Q^2 mod F. No different oracle problem is introduced.

## Native Input

Let n >= 5 be odd, q = 2^n, N = n^2, K = floor(N/8). Input consists of an
explicit verified binary-field presentation and N distinct elements alpha_i
of F_q. The targets are ALL ONE. Find x_i in F_q satisfying

    sum_i alpha_i^j x_i = 0,  0 <= j < K;
    Tr(inv0(x_i)) = 1,       0 <= i < N.

Here inv0(0)=0, so every accepted x_i is nonzero. Mixed targets, even n,
uniform witness sampling, and arbitrary parity matrices are out of scope.
The implementation uses the predecessor's independent integer-field
verifier; FLINT supplies polynomial operations, not the acceptance test.

## Lossless Reduction

Put F(X)=product_i(X-alpha_i). It is squarefree and F'=D^2 with D(alpha_i)
nonzero. All parity-valid words, not just a convenient subfamily, have

    x_i = P(alpha_i)/F'(alpha_i),  deg P < N-K.

The forward implication follows by taking the X^(N-1) coefficient in
Lagrange interpolation of X^j P. The reverse follows from equality of
dimensions: these evaluations inject an (N-K)-dimensional polynomial
space into the kernel of a rank-K Vandermonde matrix.

There is a unique Q of degree < N whose values are sqrt(P(alpha_i));
equivalently Q^2 mod F = P. Do NOT impose deg Q < (N-K)/2. Then

    x_i = (Q(alpha_i)/D(alpha_i))^2,
    Tr(1/x_i) = Tr(D(alpha_i)/Q(alpha_i)).

Since Tr(1)=1 for odd n, the trace condition is equivalent to existence
of U_i with U_i^2+U_i Q_i+Q_i^2=D_i Q_i. Interpolate U with degree < N
and set A=U+D. This gives the EXACT polynomial identity

    A^2 + A Q + Q^2 = D^2 + F W,          (1)
    deg A, deg Q < N,  deg W <= N-2,
    deg(Q^2 mod F) < N-K,  Q(alpha_i) != 0.

Conversely, (1) with these side conditions implies the original parity and
trace conditions. Reversing A=U+D and dividing by Q_i^2 proves the trace
statement; the code condition proves parity. This is an equivalence, not
an efficient algorithm for choosing A,Q,W. The witness-to-carry routine is
explicitly marked as a correctness control using an already known witness.

## Exact Search For One Supplied W

Take the constant extension E=F_q(theta), theta^2+theta+1=0. Because n is
odd, conjugation sends theta to theta+1 and

    Norm(A+theta Q) = A^2+A Q+Q^2.

Set R=D^2+F W. R is nonzero and never vanishes at an original evaluation
point. Its degree must be even: the leading norm form is anisotropic, so
deg Norm(B)=2 deg B. Factor R in E[X], checking irreducibility and complete
reconstruction. A conjugation-fixed factor of odd multiplicity forbids a
norm. For each nonfixed pair f,bar(f), occurring with equal multiplicity e,
every possible B allocates j copies to f and e-j to bar(f), 0 <= j <= e.
Fixed factors contribute half their multiplicity. The leading scalar may
be chosen as sqrt(lc R) in F_q, whose norm is lc R.

This exhausts B up to multiplication by a norm-one scalar. The number of
factor orientations is product(e+1); it can be exponential. The code checks
the cap BEFORE searching and returns UNKNOWN_ORIENTATION_CAP, never a
negative result, if this count is too large. Factorization is delegated to
FLINT; no deterministic worst-case complexity certificate is claimed.

### No Exponential Scalar Loop

Write B=A+theta Q. Multiplication by a norm-one scalar transforms

    Q' = r A+s Q,  A' = (s+r)A+rQ,  r^2+rs+s^2=1.

If a_j,b_j are coefficients of A^2 mod F,Q^2 mod F, the code constraints
are exactly the F_q-linear equations

    sqrt(a_j) r + sqrt(b_j) s = 0,  N-K <= j < N.

Rank two has no unit solution. Rank one has a one-dimensional kernel;
anisotropy and bijectivity of squaring give exactly one norm-one point on
that line. Rank zero allows every unit. A coordinate Q'(alpha_i)=0 then
excludes one projective line, because (A_i,Q_i) is never (0,0). Each such
line contains exactly one norm-one point. Thus at most N units are bad.

Use N+1 distinct units, explicitly

    (r,s)=(0,1),
    (r,s)=(1,t^2)/(t^2+t+1) for N distinct canonical t in F_q.

The denominator never vanishes for odd n, and the parameterization is
injective. Since N <= q, these suffice. In rank zero this is a hitting set
for EXISTENCE, not enumeration of every answer. The scalar work is
polynomial in N and n; no loop over all q+1 units is used by the solver.
Every output is independently checked against the original native relation.

## Exact Falsifier For Uniform Carry Guessing

For a fixed native witness, Q is unique. Each coordinate has exactly two
Artin-Schreier lifts, giving 2^N distinct A of degree < N. Two such A,A'
have the same carry exactly when

    (A+A')(A+A'+Q)=0

as a polynomial. The polynomial ring is an integral domain, so A'=A or
A'=A+Q. Nonzero Q_i make these exactly the identical/complementary choices
of coordinate lifts. Consequently each witness has EXACTLY 2^(N-1)
distinct carries, all in the degree <= N-2 domain.

Projection of the parity code onto any N-K free coordinates is injective,
because the complementary K Vandermonde columns are invertible. There are
q/2 allowed trace-one inverse values per coordinate. Therefore

    #native witnesses <= (q/2)^(N-K).

Counting witness/carry pairs bounds the number of good carries, allowing
overcounting when different witnesses share a carry. The full carry space
has q^(N-1) elements. Thus for a UNIFORM draw from that space,

    Pr[any native witness exists for W]
        <= (q/2)^(N-K) * 2^(N-1) / q^(N-1)
         = (2/q)^(K-1) = 2^-((n-1)(K-1)).

For T uniform draws, the union bound is min(1,T*2^-((n-1)(K-1))). Under IID
sampling with replacement, expected draws until a good carry are at least
2^((n-1)(K-1)) if one exists, and infinite otherwise. This is a rigorous
failure mode for that sampling strategy, NOT a lower bound for structured
or adaptive carry construction, the native problem, or quantum algorithms.

Examples: n=7 gives at most 2^-30, n=17 gives 2^-560, n=31 gives 2^-3570.
Conditioning on norm-feasible carries changes the distribution; this bound
must not be reused for that sampler without a separate argument. Likewise,
a witness-derived carry is heavily biased advice, not a uniform experiment.

## Why Patterson Is Not Yet A Solver Here

The primary [Beelen-Hoholdt-Nielsen-Wu paper](https://arxiv.org/html/1211.0122v2)
develops rational-interpolation decoding from known key-equation data and
specified degree/evaluation constraints, and treats binary Goppa decoding
within its decoding radius. Here there is no supplied received word,
corresponding syndrome, or proved reduction satisfying those constraints.
Our missing carry and unrestricted modular square root cannot simply be
declared low degree. This comparison is a scope check, not an impossibility
theorem for future coding-theoretic reductions. The original Patterson
journal page could not be read (HTTP 403); no claims are based on its text.

## Adversarial Assessment And Next Decision

Useful: a lossless mathematical target, an exact supplied-carry oracle with
explicit exponential orientation cost, removal of a spurious q-sized
scalar search, and a decisive uniform-carry falsifier.

Likely failure: this just relocates the nonlinear search into W. A good W
derived from a witness is circular. Factor orientations can independently
explode. Even a practical native classical solver would dequantize this
candidate family, not itself establish quantum advantage. The all-one
restriction does not cover the full mixed-target frontier.

Next valuable question: can a PUBLIC, structured algorithm construct W
together with favorable orientations while enforcing the high-coefficient
code constraints, without already solving for x? Its input must be only
the field, original points, and all-one targets. Compare every charged
operation against the existing systematic-root baseline on the SAME input.
Alternatively produce an explicit key-equation/list-recovery reduction
whose promised degrees and decoding radius can actually be proved.

Reject: uniform carry campaigns, larger witness-derived fixtures, low-Q
restrictions presented as complete, or cap exhaustion recorded as a native
negative. If no constructive acquisition mechanism emerges, pivot rather
than add adjacent norm infrastructure.

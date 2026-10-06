# Nonlinear Pointed Triples And A Coherent Cover Target

LOCAL DERIVATION / REVIEW PENDING. Constructive public arithmetic and source
geometry, NOT a polynomial quantum receiver or a new full-depth algorithm.
This pass opens a nonlinear route outside affine Schur restrictions.

## Constructive Finder

Original even-level native states at L=2r have independent uniform frequency
vectors a_i,c_i in Z_Q^n, Q=3^r. Their product phase on x in F3^m is F(x),
the sum of the native tables(0,a_i,c_i). Nothing here queries the unknown
s-weighted phase; only public component tables are evaluated.

For ANY classical anchor x, define the low difference columns

```text
d_i = f_i(x_i+1)-f_i(x_i) mod3.
D_x = [d_1 ... d_m].
```

For m>=n+2, RREF has at least two free coordinates. Set its first two free
coefficients to1, the others to0, and solve the pivot coefficients to obtain
w in ker D_x. There are at least two1 entries. Decompose w=u+v over F3 using
binary masks: each2 entry belongs to both; the first1 belongs to u; all
other1 entries belong to v. Both masks are nonzero and distinct. Then

```text
(x, x+u, x+v) are three distinct words;
F(x)+F(x+u)+F(x+v)=0 mod3 in EVERY secret component.
```

The identity follows from3F(x)=0 mod3 and D_x(u+v)=0. These are generally
nonaffine triples; coordinate values can repeat. Gaussian elimination and
O(nm) modular arithmetic suffice. No assignment search, secret enumeration,
planted oracle, state cloning or unknown preparation/inverse is used.

Their relative full-Q frequencies satisfy g2=2*g1 mod3. Inverse native
coordinates therefore give a genuine ODD-level L-1 label at the SAME Q.
This is not a low-digit shadow replacing higher phases. Nonzero low output
g1 supplies a relative phase of full order Q. Low-zero branches can have
smaller actual phase order; a modulus ledger must not hide that distinction.

## Exact Pointed Source Law

Take a uniform independent classical anchor and IID unfiltered native labels.
Each d_i is an independent uniform F3^n vector: it is a nonzero unit linear
combination of that coordinate's independent low a_i,c_i. Conditional on
all low labels and the anchor, each full-Q local difference has an independent
uniform high lift in Z_(Q/3)^n.

The mask columns contain(1,0) and(0,1) at different coordinates, giving an
integer unit minor. Hence the two output high frequency vectors are jointly
independent uniform, conditional on their lows. This holds at arbitrary r,
not just a small field or a numeric phase sample.

The kernel selection and mask split depend only on ker D_x, invariant under
left multiplication by GL_n(F3). Output g1 transforms covariantly. Thus its
law is a mixture of zero and uniform on F3^n minus0. If g1=0 then both distinct
nonzero binary masks u,v belong to ker D_x. They are linearly independent
over F3. Each fixed pair has probability3^-2n. For m=n+2,

```text
p0 <= b_n=min(1,[(2^m-1)(2^m-2)]/3^(2n)).
TV(pointed odd label, uniform odd label) <= max(b_n,3^-n).
```

High lifts supply the exact conditional native odd label distribution. At
growing n the low bias is exponentially small. This is a source law for a
uniform INDEPENDENT CLASSICAL anchor, not an already implemented quantum
sampler. Selecting anchors through arbitrary quantum readout needs its own
Born-weighted source argument.

## Why This Is Not Yet A Receiver

Projecting the supplied product state onto one independently found triple
succeeds with probability3/3^m. Charge that exponential failure rate.
Computing the anchor-dependent triple coherently preserves its anchor
workspace. Measuring that pointer usually separates its three endpoints:
the finder is not constant on its own triples. Its endpoint maps are not
generally bijections, so they cannot simply be applied in place as unitaries.
Recorded native collision witnesses demonstrate both issues.

A perfect disjoint partition is NOT mandatory. Let E_x be the anchored triple
and give it nonnegative Kraus weight w_x. The map

```text
K_x = sqrt(w_x) * sum_(j=0,1,2) |j><E_x[j]|
```

is a valid partial measurement whenever, for EVERY vertex z,
sum_(x:z in E_x) w_x<=1. Add the diagonal failure operator with entries
sqrt(1-sum_incident w_x). Every accepted branch of the actual flat native
source is an exact flat odd qutrit, with probability3*w_x/3^m; every failure
is charged. Overlapping edge covers are allowed.

An implementation needs coherent incident-edge access/normalization or a
different explicit Naimark circuit. Efficient outgoing edges are not that
access. A forward-only function does not grant its coherent inverse.

## Incoming Access Reduced To Fixed-Modulus Arithmetic

Use m=n+2 and keep only anchors for which D_x has full row rank. There are
two free indices. For a proposed endpoint z enumerate their possible pair,
and the possible location p of the first1 (a pivot before the first free,
or that first free). There are at most C=m*binomial(m,2) cases per endpoint.

Write d_cur=f(z+1)-f(z), d_prev=f(z)-f(z-1) coordinatewise. Free coefficients
are1; if p is a pivot it is fixed to1. All other pivot coefficients are
unknown w_i; before p they may only be0 or2.

For endpoint x+u, the variable contribution choices are

```text
w_i=0:0; w_i=1:d_cur; w_i=2:-d_prev.
```

For endpoint x+v they are

```text
w_i=0:0; w_i=1:d_prev; w_i=2:-d_prev.
```

Known free/forced contributions determine the target. The second endpoint
therefore gives LINEAR equations with coefficient-domain restrictions. The
first is a THREE-CHOICE modular witness problem over F3, not ordinary linear
elimination. Reconstruct x, then check actual RREF pivots/free coordinates,
kernel word and endpoint. The module compiles these cases without enumerating
assignments; bounded tests enumerate solutions to verify exact equivalence.
General rank-deficient inverse cases are not supplied by this reduction.

There is no assertion that the three-choice cases are generically hard OR
already easy. Their input is explicitly available, with fixed small modulus
and no growing-root arithmetic. A fast complete reversible solution is a
concrete missing primitive, not an assumed oracle.

## Polynomial Source Geometry, Conditional On A Real Compiler

Here d(z) counts incidences of FULL-RANK anchored edges, with repeated edge
instances retained. For each fixed vertex and inverse case under the original
IID native low source, its target contains an independent uniform contribution
from the second free coordinate. Variable choice tables are independent of
that target. Distinct assignments have uniform differences because a changed
coordinate has a nonzero unit coefficient on an independent low vector.

If M<=3^n is the case's allowed assignment count, its UNFILTERED solution
count eta obeys EXACTLY

```text
E eta^2=M/3^n+M(M-1)/3^(2n)<=2.
```

Canonical-kernel checks only discard solutions. Consequently

```text
d(z)<=1+sum_(2C cases) eta;
E d(z)^2 <= B=(1+2C)(1+4C)=O(m^6).
```

This averages the original native labels, not source-conditioned independent
matrices. The projective left-null union bound gives full-rank anchor mass
gamma>=17/18 for n-by-(n+2) IID D_x. Choose
Delta=ceil(2B/(17/18)); discard every edge incident to a vertex with degree
greater than Delta. The expected fraction of discarded edges is at most
B/Delta, since sum_(d>Delta)d <= sum_z d(z)^2/Delta. Thus at least gamma/2
of all anchors remain IN SOURCE AVERAGE.

Give each surviving edge constant weight1/Delta. This is pointwise a valid
Kraus frame, with native-average acceptance at least3*gamma/(2Delta), an
inverse polynomial. No maximum-degree theorem or favorable individual matrix
is silently assumed. Full-rank and truncation failures remain charged.

For this precise constant-weight cover, accepted anchors have low-zero mass
at most2*b_n/gamma: the factor1/Delta cancels between zero-output and accepted
mass. GL equivariance survives full-rank and true-degree predicates; high
lifts remain uniform. Thus accepted odd labels have TV at most
max(2*b_n/gamma,3^-n), clipped to1. Fresh independent attempts give IID samples
of this law. This is CONDITIONAL ON compiling this actual cover with complete
incoming access. Geometry/existence does not implement the circuit.

## Executed Evidence

The explicit compiler enumerates3^m words, constructs all pointed triples,
deduplicates their unordered edges, and optimizes nonnegative cover weights
with a bounded LP. Solver floats only propose certificates: exact rational
primal feasibility and dual edge prices establish lower/upper bounds.
This LP reference includes rank-deficient anchors and is NOT the truncated
full-rank cover in the source theorem. Do not transfer the theorem's source
distribution to its differently weighted output without another proof.

Native level4 controls, n1,2,3, have certified acceptance32/33,
2842/3093 and2084503/2340171. Full branch phases at Q=9 and failure mass are
replayed; arbitrary-input Naimark norm preservation is tested. Larger controls
through n6 enumerate up to6,561 words; they are bounded geometry diagnostics,
not asymptotic runtime or degree evidence. Scalable pointed controls retain
full native roots through L16 without enumerating their input cube.
The independent JavaScript certificate reconstructs the native integer
frequency recurrence, Gaussian triples and exact rational cover bounds.
Sixteen focused tests and a fourteen-file related regression323 pass.

## Research Decision And Required Falsifiers

The opening is efficient POINTED three-witness arithmetic and polynomial
SOURCE-AVERAGE cover geometry. The remaining issue is coherent compilation,
not the existence of small low-zero-sum triples. Require complete incoming
access, source-aware normalization and a physical circuit. Reject any use of
free inverse maps, rank/fiber tables, QRAM or unknown-state preparation.

Even a perfectly compiled ONE-output stage consumes n+2 inputs. Repeating
such stages alone still gives growing-depth quasi-polynomial throughput,
not a Shor-level result. Before a full implementation campaign, investigate
multi-output, correlated-output or coherent-edge-label receivers that retain
useful phase information instead of discarding almost all registers.

Comparator: [Boucher, Fouque and Shen, Sections4.2-4.3](https://arxiv.org/html/2609.34996v1)
give a charged native zero-sum sieve. This construction uses nonlinear,
word-dependent integer-secret frequency triples, not their uniform affine
merger. No novelty or improved complete complexity is claimed.

Falsifiers: a native triple violates the low-zero-sum or full-root chart;
incoming cases omit a full-rank preimage; measured source violates the exact
second moment; the proposed compiler loses endpoint coherence; or the claimed
breakthrough is only a one-output quasi-polynomial stage improvement.

Gemini owns routine CLI/registry integration and production validation.
GPT NEXT: resolve the coherent inverse/normalization target, or exploit the
linearly invertible endpoint as a noncommuting, phase-retaining collective
primitive. Do not replace that task with more tiny cover plots.

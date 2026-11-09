# Classical source boundary and linear-to-quadratic reduction

2026-11-05. Scoped independent review. Read the local primary-source texts
`pandey_extension_2604_04833.txt` (v3, 21 May 2026),
`kkk_2020_published.txt`, and `beullens_2020.txt`, plus the native contract
in `LEGENDRE_RESULTANT_HYPERPLANE_READOUT.md`. No network, Git, finite sweep,
registry change, or quantum implementation was used.

## Findings from theorem bodies

**Pandey does not give a poly(log p) classical algorithm for the original
prime-field fixed-degree irreducible-polynomial oracle. It also does not
implement or anticipate the coefficient-space quantum receiver in these
sources.** This is a statement about the audited sources, not a novelty or
classical-hardness claim.

Pandey Sections 1.2--1.3 and Theorems 2--3 concern the LINEAR shift
`A -> chi_q(A+K)` over the entire known field `F_q`, `q=p^r`, represented
modulo a public irreducible polynomial. The passive theorem observes M
counter queries encoded by base-p digits. The active theorem chooses M
geometric inputs `g^i`, where g is a primitive generator of `F_q^*`.
Neither theorem receives only the base-field restriction
`x -> chi_p(Q(x))` for an unknown irreducible Q. Writing such values as
extension-field norm characters does not supply arbitrary extension-field
shift queries, the hidden root, or its field representation.

Theorem 2 advertises expected search `O(Uq/M)`, where `2^U >> q` is its
unicity prescription. Its proof first extracts `M-U+1` windows, partitions
them by signatures, builds a hash table, and then searches. The advertised
expression omits collection/table work and does not separately charge U
character evaluations for each reference window. The claimed maximally
populated class size approximately M/U is not established by its preceding
signature-count bound `p^ceil(log_p U)` alone. These are limitations of the
advertised accounting, not needed assumptions for the reduction below.

Theorem 3 advertises `O(q/M)` operations and even that many character
evaluations. Its proof stores approximately M U-bit windows, samples
reference windows, and looks up each window and its complement. At least
M oracle replies must be collected; straightforward generation of a new
reference window costs U public character evaluations, in addition to
field exponentiation/hash work. The elementary collision-search tradeoff,
even if granted without its logarithmic factors, therefore costs at least
`Omega(M+q/M)`, optimized at `Omega(sqrt(q))`. Taking M approximately q to
make the SEARCH polylogarithmic leaves exponential input collection in
log q. Construction of the primitive generator is uncharged; the source
does not give a poly(log q) classical method for it. The proof also divides
by K and so omits K=0. Its binary convention pads character zero to +1;
the displayed exact multiplicative factoring identity then has an
exception at `g^i=-K` when chi_q(K)=-1. A repaired collision analysis may
handle these exceptions, but the printed identity is not literally exact
with that convention.

Section 5 explicitly calls higher-degree cryptanalysis future work. Its
degree-2 expression contains two unknown coefficients; no decoder is
given. The asserted approximate `q^floor(d/2)` meet-in-the-middle cost is
preliminary, not a proved uniform theorem. Claims of necessary exponential
security for higher degrees do not establish a lower bound. Nothing in
these classical collision constructions is a native coherent quantum
coefficient readout.

KKK 2020 really does use the native prime-field polynomial character
oracle. Section 4 and Table 1 require p queries for the full-table action
attack. For good degree-d polynomials the search cost is
`O(p^(d-3) d log p)` AFTER `O(p^3 d log p)` preprocessing and comparable
memory; the search alone is not total complexity. Section 4D trades these
for roughly `p^(d/2)` table/search costs for degrees 3--5. Section 4F gives
a deterministic O(p) quadratic algorithm. Section 5's limited-query
algorithm explicitly charges M queries, approximately M^2/L extracted
sequences and approximately `p^d L/M^2` search trials. The paper's short
sequence uniqueness at logarithmic L is an assumption (Section 2A), not a
proved worst-case guarantee; it records only an exponential provable
upper bound for universal uniqueness. These algorithms are not polylog.

Beullens et al. Section 4.2 likewise uses M consecutive original
prime-field queries, `O(M^2/m)` sequence extractions,
`O(p^d d^2 log^2(p)/M^2)` public character evaluations and O(M^2) memory,
with `m=d ceil(log p)`. The candidate-count guarantee invokes Assumption
1. Section 5's factor-splitting weak-key attacks require a genuine proper
factor and therefore do not apply to the original irreducible promise.
The occasional quantum algorithms discussed there concern generic
collision/k-list methods, not this coefficient-hyperplane receiver.

## Exact randomized reduction for classical TRIT access

Let p be any odd prime and let `L_s(y)=chi_p(y+s)` with the standard
three values, including chi_p(0)=0. Suppose a classical algorithm D
reconstructs EVERY monic irreducible quadratic from chosen native
character queries, with a specified resource bound and failure delta.
Sample uniform independent r until

`chi_p(-1) L_s(r) = -1`.

Set `a=s+r` and `Q_r(X)=X^2+a`. The test excludes a=0 and is exactly
`chi_p(-a)=-1`, so Q_r is irreducible. There are `(p-1)/2` accepting r;
acceptance is `(p-1)/(2p)>=1/3`, uniformly in s and p. Every requested
native query is simulated exactly by

`chi_p(Q_r(x)) = L_s(x^2+r)`.

This uses one original query and poly(log p) public arithmetic. If D
returns constant coefficient c, return `s=c-r` (the linear coefficient
must be zero for the true polynomial). With a cap N, the sampling abort
probability is at most `(2/3)^N`; taking
`N=ceil(log(2/eta)/log(3/2))` and delta<=eta/2 gives total error<=eta.
No extension-field or hidden-root access is supplied. The reduction
therefore transfers a hypothetical worst-case classical polylog quadratic
decoder to classical linear Legendre hidden-shift recovery, including
chosen queries and total native-access overhead. It is a conditional
algorithmic implication, not evidence of hardness.

## Binary zero-padding correction, with a uniform bound

Let `lambda_s(y)=chi_p(y+s)` away from `y=-s`, and
`lambda_s(-s)=+1`, the bit-zero convention in the sources. The same
acceptance test can accept r=-s when chi_p(-1)=-1, so the preceding proof
CANNOT be copied verbatim: Q_r would be X^2 and violate irreducibility.

Use the FIRST accepted r. When chi_p(-1)=+1 the zero is rejected and
no correction is needed. When chi_p(-1)=-1, draw k fresh independent
uniform `t in F_p^*`, query `lambda_s(r+t)`, and compare with the PUBLIC
standard `chi_p(t)`. If all k comparisons agree, return `s=-r` directly.
If any comparison disagrees, r cannot be -s; keep this certified nonzero
r and run D with the exact simulation above. For this branch the
quadratic is irreducible, so no padded-zero value is ever queried during
native simulation.

For a=s+r=0 every comparison agrees. For any fixed a!=0, the exact
correlation is

`sum_(t!=0) lambda_0(t+a) chi_p(t) = -1 + chi_p(-a)`.

Indeed the standard two-shift quadratic-character correlation over all
t is -1, the t=0 term vanishes, and padding adds only chi_p(-a) at t=-a.
Both compared values are signs, so one-test agreement probability is

`1/2 + (-1+chi_p(-a))/(2(p-1)) <= 1/2`.

Fresh independence gives false-zero probability at most `2^-k` for EVERY
nonzero a, including a chosen after the initial acceptance queries. Test
the first accepted r only: this costs k, not k per sampled candidate.
Acceptance probability is `(p+1)/(2p)` when chi_p(-1)=-1 and
`(p-1)/(2p)` otherwise, always at least 1/3. Use sampling abort budget
eta/3, `k=ceil(log_2(3/eta))`, and decoder failure<=eta/3. Total failure
is at most eta and extra native queries are deterministically
`O(log(1/eta))`; all extra arithmetic is polynomial in log p and
log(1/eta). This is a classical BIT-access reduction only.

## Claim boundaries and next hard question

Keep all classical-hardness, asymptotic-separation, quantum-implementation
and novelty gates false. This note does not compile a raw quantum phase
oracle into controlled queries or extend the reduction to phase copies.
It assumes a worst-case decoder on every promised quadratic; a merely
average-over-all-quadratics decoder is insufficient because this reduction
produces the subfamily with zero linear coefficient.

The next hard source question is whether any PRIMARY theorem actually
reconstructs fixed-degree irreducible Q classically in poly(log p) TOTAL
time from the original character-only oracle. Exact receiver priority is
a separate question. No mechanical sweep is requested. Acceptance for
this note is checking the displayed correlations, irreducibility test,
and resource budget against the three local source theorem bodies.

## Added primary baseline: Kopparty, arXiv:2601.07137

The local full text `kopparty_noisy_2601_07137.txt`, Theorem 1,
Algorithm A and Theorem 3.1, supplies a substantially more general
CLASSICAL FULL-TABLE baseline. In particular it handles squarefree
polynomials with base-field roots and adversarial errors. It does not
give a classical poly(log q) native-oracle decoder, and it does not
implement the quantum coefficient receiver. The introduction explicitly
distinguishes Russell--Shparlinski's O(d) quantum QUERY result from a fast
quantum algorithm, which it says does not follow as far as the author
understands.

The directly audited, explicit sufficient parameter regime from Theorem
3.1 is: q any odd prime power, epsilon>0, degree bound
`d <= (epsilon/16) sqrt(q)`, and an integer error bound
`e <= (1/8-epsilon) q`. The unknown g is monic and squarefree, with degree
at most d. The input is the WHOLE received word
`r:F_q -> {0,+1,-1}`, satisfying Hamming distance
`Delta(r,chi_q o g)<=e`. The algorithm returns g for EVERY such g and r;
this is not a random-key assumption. Theorem 1 states the asymptotic
`d=O(epsilon sqrt(q))`, constant-fraction-error result at the introduction
level; for exact constants use Theorem 3.1's displayed sufficient bound.

Algorithm A takes `M=16d/epsilon`, `c=M/2`, `h=2e`,
`u=2e+dM`, and

`D=d((q-1)/2+M)+(M/2)q`.

With the harmless integer/divisibility parameter choices needed for these
formulae, it solves qM homogeneous linear equations over F_q for the
coefficients of F and `U_0,...,U_(M-1)`:

`F^[ell](alpha)=r(alpha) U_ell(alpha)`

for EVERY alpha in F_q and `0<=ell<M`, with `deg F<=D` and
`deg U_ell<=u`; the derivatives are Hasse derivatives. It then factors F
and recovers g by selecting irreducible factors whose multiplicities
modulo q lie in the displayed interval `[3q/8,7q/8]`. The proof shows that
EVERY nonzero solution to the linear system works, not only a hidden
intended solution. The crucial identity is obtained from
`G=g^((q-1)/2+M)`: low-order derivatives of G on F_q factor as chi(g)
times low-degree public-form polynomials. High-multiplicity error-locator
pseudopolynomials account for corruptions.

The native cost is q queries to acquire r. There are qM equations and
`(D+1)+M(u+1)=O(dq/epsilon)` unknowns under the theorem's degree bound;
`D=O(dq/epsilon)`. For fixed d and fixed positive epsilon the matrix and
factored polynomial therefore have order q dimensions/degree. Dense
linear algebra gives a conventional polynomial bound (at most cubic in
these dimensions in field operations), followed by univariate
factorization of degree D in poly(q,D) time as charged by the paper.
The paper does not give a polylogarithmic TOTAL-time bound or a sublinear
query version of this construction. The q native queries alone cost
`2^Theta(log q)`; no search/preprocessing split removes them.

Zeros are explicitly part of the standard source character, not ignored
in Theorem 3.1. A monic squarefree degree-at-most-d g has at most d
base-field roots. If native BIT access instead pads character zero to +1
(or to any sign), its full table differs from the source table in at
most d positions. Treating these as adversarial errors makes the theorem
apply whenever `e_other+d <= (1/8-epsilon)q` and the degree bound holds.
Thus every fixed-degree monic squarefree prime-field Q is covered for
sufficiently large p, with p padded-BIT queries and poly(p) classical
time. For example epsilon=1/16 and `p >= (256d)^2` suffice for a noiseless
padded table. No root locations, zero detector or hidden factorization
are provided as extra input. This observation transfers the baseline to
padded classical BIT values, not to quantum phase copies: copies do not
provide the full classical received word for free.

For general monic g the source recovers its squarefree core, not its
original perfect-square factors. The theorem therefore closes no
identifiability gap beyond its explicit squarefree promise. Relative to
our original irreducible problem this is a valid stronger input-family
baseline, with noise robustness and degree growing as o(sqrt(q)); it is
not a matching classical polylog algorithm. For noiseless cubics, it does
not supersede the sharper existing p-query near-linear field-work bound
in the project note.

### Why its list-recovery interpretation does not dequantize native OPI

The source's explicit list-recovery section sets
`S_alpha=chi_q^(-1)(r(alpha))`. Every list is one of the SAME global
quadratic-residue fiber, nonresidue fiber, or zero singleton. The key gain
over general Guruswami--Sudan list recovery is precisely this extra
algebraic structure, which supplies the character-power and derivative
identities above. Its near-perfect agreement promise is also specific:
the theorem allows fewer than approximately q/8 inconsistent rows.

Native scalar OPI supplies independently drawn arbitrary halfsets at
each row, over F_(2^t), with an optimization target. Equal cardinality
does not turn those lists into fibers of one public odd-field quadratic
character. Row-dependent relabelings that make the sets look like fibers
do not preserve polynomial evaluations. No such paid conversion is
provided by this source. The source's characteristic-two analogue uses
the SAME fixed trace predicate, again not arbitrary independent
halfsets. Consequently this audited result supplies no direct classical
dequantization of native random-table OPI without changing its input and
promise. It supplies no OPI hardness statement either.

No implementation or additional finite sweep is requested. The next
acceptance check is source-level: retain q acquisition cost, monic
squarefree scope, the displayed degree/error bound, and the root-padding
error budget whenever this baseline is cited.

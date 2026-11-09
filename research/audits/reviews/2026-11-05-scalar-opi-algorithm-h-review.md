# Scalar OPI Algorithm H: Independent Scoped Review

5 November 2026. AI mathematical/code review; no novelty, hardness,
DQI-matching guarantee or asymptotic advantage is established. Reviewed
`research/classical_baselines/scalar_opi_fourier_elimination.py` and its
native field helpers. No implementation changes were made.

## Exact algorithm

No invalidating correctness error was found. If z contains the kt binary
monomial-coefficient bits and E_i is evaluation at the i-th nonzero field
point, integer table Walsh coefficients c_i(u) give exactly

    q F(z) = sum_(i,u) c_i(u) (-1)^((E_i^T u) dot z).

The code uses the same binary polynomial basis for table symbols,
coefficient bits and field multiplication. It sums signed duplicate
frequencies. Restricting a nonzero current parity a to the favorable bit
raises the uniform affine-section mean by |C_a|/q. Pivot substitution
preserves every other term, including destructive collisions between
rows. The selected parity involves only free bits, so the section remains
nonempty and one free bit is removed. Reverse backsubstitution satisfies
all imposed parities and returns a degree-<k native polynomial. Stopping
when no nonconstant aggregate term remains means the TOTAL score is
constant on the remaining section; it need not make every row constant.
There are at most kt restrictions and the resulting integer score is at
least ceil(m/2). There is no proved DQI-quality guarantee for this greedy
selection rule.

## Early-row lemma and its precise limit

Let W=F_2^(kt), V_i=im(E_i^T) <= W*, and let the current affine section
have normal space S. For any set of at most k distinct evaluation points,
RS interpolation makes the joint evaluation map onto. Consequently those
V_i form a direct sum, each of dimension t.

Suppose T is a set of r touched rows and

    S = direct_sum_(i in T) S_i, with S_i <= V_i.

If r<=k-2, the images of any distinct V_i,V_j in W*/S intersect only at
zero. Indeed, an intersection gives a in V_i and b in V_j with a+b in S.
The row spaces indexed by T union {i,j} are a direct sum, because their
number is at most k. Comparing components shows a and b have zero images
in the quotient. For an index outside T this forces its original
component to be zero; for an index in T it forces membership in S_i.

Before any selected nonzero coefficient has multiple row owners, its
frequency has a representative in a unique V_i modulo S. Adding its
constraint enlarges S by that representative, preserving the displayed
rowwise direct-sum form while the touched row spaces remain independent.
This explains the invariant for the early greedy trajectory. Distinguish
collision of full row spaces from collision of currently nonzero Fourier
support; cancellation can hide a structural collision.

If r<=k-1, every untouched V_j has V_j intersect S = {0}. Thus E_j maps
the section direction S-perp onto F_2^t. Uniform points in the affine
section have exactly uniform j-th symbols. For balanced accepted tables,
every untouched row contributes exactly 1/2 to the section mean, and every
touched row contributes at most 1. Therefore

    section mean <= m/2 + r/2.

This statement is deterministic and survives adaptive choices based on
all tables. It does not assert independence of the row symbols, nor bound
the final greedy score after further restrictions.

The no-alias threshold is sharp as a uniform statement. At r=k-1, take
S=direct_sum_(i in T) V_i, corresponding to fixing those entire symbols.
The quotient W*/S has dimension t. Every untouched V_j maps isomorphically
onto that quotient, so all untouched row-space images coincide, although
each untouched marginal is still uniform.

## Counterexample to completing a row before moving on

Use the native F_16 binary basis with four symbol bits (x,y1,y2,y3).
Let one balanced table accept OR3(y) when x=0 and AND3(y) when x=1.
Its two branches have seven and one accepted symbols, respectively. Its
largest normalized Walsh coefficient is 6/16 on x; every other
nonconstant coefficient has magnitude at most 2/16. Favorably fixing x=0
leaves the OR3 branch, whose nonconstant coefficients have magnitude
2/16 with the retained denominator 16.

For every other row, use majority3 on three symbol bits, ignoring the
fourth. These are balanced tables with largest nonconstant coefficient
4/16. For k>=3, the early-row lemma prevents cross-row aliases after the
first restriction. Greedy selection therefore starts with the special
row and then selects another row: 4/16 exceeds 2/16. Thus a universal
row-completion or monotone row-focus argument is false. This is an
explicit balanced-table counterexample, not an IID-source performance
claim and not a statement about the six saved instances.

## Executed verification and resources

Executed only `exact_controls()` using `/opt/anaconda3/bin/python`.
It passed 16 native assignments, all 307 nonempty affine sections of the
four coefficient bits, 1530 signed restriction transitions, 352
negative-weight cases, distinct-row sum/cancellation, and native witness
backsubstitution. No six-instance run, broad test suite or independent
Sage verification was performed by this reviewer.

O(kt*m*q) bounds the core greedy dictionary visits, with at most m*q
initial entries and at most kt restrictions. It is not a complete
bit-operation or wall-time count: masks have kt bits, coefficient merges
use integers, and preprocessing constructs the field maps and Walsh
transforms. The imported `arithmetic(t)` additionally constructs a q-by-q
multiplication table, additive-FFT basis polynomials and scales unused by
Algorithm H. Native verification uses O(m*k) field operations. These are
polynomial costs, but the JSON counters omit preprocessing. Keep counters
and runtime comparisons explicitly scoped.

## Follow-up: low initial spectrum is not a gain bound

For t=2s+1, write the native field-symbol bits as (x,y1,...,y_(2s))
and consider the balanced accepted table

    h(x,y) = 1[x + sum_(j=1)^s y_(2j-1)y_(2j) = 0].

Its nonconstant integer Walsh coefficients are zero when the x-frequency
is zero, and have magnitude 2^s=sqrt(q/2) when that frequency is one.
To see this, write h=(1+(-1)^(x+Q(y)))/2, sum over x, then factor the
remaining Walsh sum into s two-bit quadratic sums, each of magnitude 2.

For ANY single balanced Boolean table, favorable-parity elimination ends
with that indicator constant on the remaining affine section after at
most t restrictions. The terminal constant is either zero or one; since
the mean strictly increases from 1/2, it must be one. Its total numerator
gain is therefore q/2, and some selected coefficient has magnitude at
least q/(2t). For the displayed table this eventually greatly exceeds the
initial sqrt(q/2) maximum. Consequently an initial Walsh bound cannot
simply be multiplied by the number of restrictions to upper-bound later
adaptive gains. This is a counterexample to that proposed argument, not
a fixed-rate RS performance theorem or an IID-source claim.

## Follow-up: next-size evidence and allocation decision

The parent reported the unchanged procedure on the first fixed-seed
continuation q512,k128,seed3101: Algorithm H scored 396/511, compared with
Prange32's 347 and the retained rational DQI-filter mean lower bound
414.0369687457006. At q256,k64,seed3101 the corresponding scores were
206/255, Prange32's 171, and DQI lower bound 203.636 (rounded). Thus the
q256 crossing did not persist on this particular next-size instance.
The parent was independently verifying the q512 witness in Sage when
this addendum was written; this reviewer did not rerun or independently
verify either reported native experiment.

The proposed decision is appropriately scoped: stop further unmotivated
sweeps, retain Algorithm H as a competitive finite classical baseline,
and leave both its asymptotic behavior and the full-input scalar-OPI
question UNKNOWN. A single next-size miss does not refute average-case
or asymptotic matching, establish hardness, or close the direction. A
single earlier crossing likewise does not match the quantum algorithm's
output law, expected performance, or runtime. The DQI number is a mean
lower bound, not a claim about every quantum output.

A further research pass should require a concrete constructive operation
or a source-correct theorem with potential to resolve the native question;
it should not merely tune the greedy tie rule or extend the size sweep.
Comparing independently motivated high-upside directions is a reasonable
allocation decision here. This recommendation concerns the value of the
next experiment, not a mathematical rejection of Algorithm H.

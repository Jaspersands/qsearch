# Sparse Translation Frames For Classical Interval Search

Local constructive theorem and executed attack; independent research review
pending. No novelty claim. This strengthens the dense character comparator
in INTERVAL_CHARACTER_ROUNDING.md, not the quantum receiver.

2026-10-19: the SAME producer also implements nonsplit norm-one torus trace
frames for ell|p+1. Their derivation and paid fiber/denominator costs are below;
the original split construction and its proof remain intact.

## Question And Mechanism

Can native low-moment kernel rows be sparse, reducing the rounding variance
from the block length p to a parameter comparable to the target codimension?

For a proper divisor ell of p-1, YES. Let H be the multiplicative subgroup
of size ell, g a primitive generator, and

```text
w(x) = 1_H(x) - 1_(gH)(x),   x=0,...,p-1.
```

This waveform has entries0,+/-1, support2ell and sum0. Take the constant row
plus the p-1 cyclic translates w(x-t), t0..p-2. These form a full-real-rank
integer lattice subbasis in the native RS kernel of any codimension d<=ell.
Independent unbiased rounding in this basis gives, for EVERY public target,

```text
Pr[||e||inf > u] <= min(1, 2p exp(-2(u+1)^2/(2ell+1))).
```

Thus interval width O(sqrt(ell log p)) has expected polynomial classical
search time. The existence of a proper divisor ell>=d is an EXPLICIT parameter
condition, not a claim about smoothness of all primes. At ell=(p-1)/2 the row
is the quadratic character and recovers the dense construction's parameter p.

Input is the exact same full-support prime-field problem: N=p, native
H_d[j,x]=x^j, arbitrary public syndrome/particular word, centered modular
interval. No free oracle, planted short solution, subset of constraints,
rerolled target, extension-field integer encoding or prescribed sampling law.

## Native Kernel, Sharp Boundary And Real Rank

For 1<=j<ell, the sum of x^j on H vanishes by character orthogonality in the
cyclic multiplicative group. The other coset's sum is multiplied by g^j.
At j0 the two cardinalities cancel. At the FIRST excluded moment,

```text
sum_x x^ell w(x) = ell*(1-g^ell) != 0 mod p.
```

Translation preserves all moments below ell by the binomial theorem.
The API rejects d>ell; it does not infer more parity checks from a good witness.

To prove rank, encode w as the rational position polynomial W(X). Its cyclic
convolution eigenvalues are W(zeta) at the p-th roots of unity. W(1)=0.
For any nontrivial p-th root zeta, W(zeta) cannot vanish: its minimal polynomial
is Phi_p=1+X+...+X^(p-1), irreducible because Phi_p(X+1) is Eisenstein at p.
If Phi_p divided W of degree at most p-1, W would be a constant multiple of
Phi_p, contradicting W(1)=0 and W!=0. Hence the p translates have exactly
one relation, their all-ones sum. Omitting any one leaves p-1 independent
mean-zero rows; the constant row supplies the missing direction.

This proves a full-rank sublattice, NOT necessarily a basis of the ENTIRE
Construction-A lattice. Its determinant is nonzero and divisible by p^ell,
but is not assumed to equal p^ell. A sublattice is sufficient for preserving
the affine target, and the larger rational denominators are actually charged.
Composite support cardinalities do not inherit this irreducibility argument.

## Exact Coordinates, Not An Inverse Oracle

Let Y(X) encode the public word, mean=sum(y)/p, and J=Phi_p. Put

```text
W=(X-1)V
T=Y-mean*J=(X-1)U
C = U * V^(-1) mod Phi_p   over Q.
```

The inverse is COMPUTED by exact polynomial extended Euclid in FLINT and
verified by multiplication modulo Phi_p. C has degree <=p-2. Since
`(X-1)*Phi_p=X^p-1`, the cyclic convolution `CW mod(X^p-1)` is exactly T.
Thus the constant coordinate is mean and the other p-1 coordinates are C's
coefficients. The producer converts them to a common denominator D, and
independently verifies `a B=D y` with integers and a sparse streamed product.

These are POSITION polynomials for cyclic inversion. They are NOT the RS
value polynomial used to validate the final word. That second polynomial
is independently interpolated from p-ell values and checked at every field
point, with degree <p-ell<=p-d.

Unbiased rounding uses the actual remainders modulo D, not modulo p. D can be
much larger than p: the p1021 public-word control uses107 bits. Every attempt
checks the ORIGINAL moments, including failures. Integer coefficients are
stored as decimal strings using FLINT to avoid Python's large-int JSON digit
limit; none is truncated. A zero-width nonzero-syndrome test keeps both failed
rounds and does not turn budget exhaustion into a hardness claim.

## Tail Proof And Resource Accounting

In a column of B, at most2ell retained translates are nonzero, plus the
constant row. Their entries have magnitude1. The raw residual is a sum of
independent, centered rounding errors with total squared range <=2ell+1.
Hoeffding and a column union bound give the displayed all-target bound.
Failure of an integer interval requires a raw coordinate of magnitude at
least u+1, and modular centering never increases that magnitude.

The rational certificate uses
`E=floor(2(u+1)^2/(2ell+1))`, `delta=min(1,2p/2^E)` and rounds probabilities
UP to128-bit dyadics. The full interval has failure0 directly. With fresh
independent exact coins on a FIXED target, t attempts fail with probability
<=delta^t; expected attempts <=1/(1-delta) when nontrivial. Seeded executions
are witness replays, not evidence about ideal random-source independence.

The subgroup/generator setup and rational polynomial inverse are paid.
They are polynomial in the EXPLICIT block length p, not asserted polynomial
in log p alone. A brute-force generator/factorization search is already
polynomial in p; SymPy's existing primitive-root routine is used in code.
Hadamard bounds on the integer row norms sqrt(p),sqrt(2ell), together with
cofactor formulas, bound coordinate numerator/denominator bit lengths by
O(p log(ell+1)+log p). Exact inversion therefore does not hide exponential
input bit lengths. Actual sizes are saved rather than assumed small.
Sparse multiplication costs O(p*ell) such integer operations, native moments
O(p*d), and independent interpolation is separately polynomial. Storage is
O(p) big coordinates plus polynomial-in-p inverse/transcript storage.

## Executed Results

Run `python theorems/interval_subgroup_rounding.py --write`.
For each row below the producer uses a seeded uniform PUBLIC word and a
quarter-field spike; no target is planted or rerolled. All ten have witnesses.

|p|d=ell|sparse certified radius|dense radius|failure upper per attempt|public-word norm|
|---:|---:|---:|---:|---:|---:|
|31|5|6|10|31/128|3|
|61|5|6|15|61/128|4|
|127|7|8|23|127/512|5|
|257|16|13|37|257/1024|7|
|1021|17|14|78|1021/2048|8|

All five choices also satisfy the previously implemented uniform-interval
sufficient soft-decoder inequality d/p<C_KV, checked with exact rationals.
They therefore confront the same candidate quantum search window, rather
than merely solving a different planted task. No quantum experiment is run.
The general theorem is justified by the derivation, not the ten seeds.

Independent tests construct full small integer matrices, check determinant
divisibility and every native moment, compare coordinates against a DIFFERENT
rational MATRIX inverse, exhaust small rounding distributions, verify real
denominator coins, enumerate small syndromes and replay all polynomial outputs.
The final milestone is17 new sparse checks,43 combined sparse/dense checks,
and208 connected tests INCLUDING those43, passing in64.81s with runtime
warnings as errors. This is not a full-repository run or independent formal
proof. Both live producers, Python compilation, site JavaScript syntax,
strict finite JSON, source/dependency replays and registry validation pass.

## Attempts To Disprove It And Remaining Scope

- The sparse row might not lie in the intended kernel: verified at every
  moment and with the sharp ell-th countercontrol. d>ell is rejected.
- Sparsity alone does not imply rank: prime cyclotomic irreducibility is
  required, and separate exact determinant controls check bounded cases.
- W is NOT invertible modulo X^p-1. Dividing the zero-mean factors before
  inverting V modulo Phi_p is essential; exact reconstruction and an independent
  matrix inverse test it. No precomputed short-witness oracle is supplied.
- Rational denominators might hide cost or biased coins: their sizes and full
  coefficients are retained, and an injected coin source verifies that D,
  rather than the field modulus, is used on every draw.
- Success does not imply a uniform/weighted sampler, arbitrary acceptance-set
  algorithm, or attack on punctured N<<p instances. None is claimed.
- Missing useful divisors on BOTH p-1 and p+1 can destroy the improvement.
  Safe-prime weakness of the split construction alone is not sufficient to
  exclude the nonsplit attack below. Do not silently change a fixed modulus.
- No logarithmic factor is removed by this rounding proof, and classical
  attacks may do better still. The local derivation needs independent review;
  no absence of search hits or certificate hash establishes novelty.

The [soft-decoder paper](https://arxiv.org/abs/2411.12553) supplies the target
task, [Bennett-Peikert](https://arxiv.org/abs/2202.07736) relevant RS lattice
context, and [Hoeffding](https://doi.org/10.1080/01621459.1963.10500830) the
tail inequality. The sparse translation-frame application here is a local
derivation, not a statement attributed to those papers.

## Nonsplit Norm-One Torus: Executed Extension

This removes the PARTICULAR p-1 divisor restriction when p+1 has a useful
divisor. It does NOT remove every arithmetic restriction on the prime.

Let T be the norm-one subgroup of F_(p^2)^*, of order p+1, with generator g.
For a subgroup H of size ell and coset g^a H, push its COUNTING measure to F_p
by `Tr(z)=z+z^p=z+z^-1`. Input and output remain length-p vectors over the
original PRIME field; the extension is only an internal classical primitive.

For any j<ell,

```text
sum_(h in H) Tr(g^a h)^j
  = sum_(r=0..j) binom(j,r) g^(a*(j-2r)) sum_(h in H) h^(j-2r).
```

The inner sum vanishes unless ell divides j-2r. Only exponent0 can survive
in this range; for even j its contribution is ell*binom(j,j/2), independent
of a. Differences of two coset trace measures therefore have all native
moments below ell equal to0. At the first excluded moment the difference is
`ell*(Tr(g^(a*ell))-Tr(g^(b*ell)))`. It is nonzero for the choices below.
Translation, prime circulant rank and exact Q-polynomial inversion apply as
before. No moment conclusion is transferred without native verification.

### Trace Fibers Are Not Free

On T, equal traces identify z and z^-1: both solve `Z^2-Tr(z) Z+1=0`.
With quotient index m=(p+1)/ell>=5, choose a=1,b=2. Inverse coset classes
{1,-1} and {2,-2} are disjoint and non-self-inverse, so both trace maps are
injective and their images disjoint. The waveform has entries0,+/-1, support
2ell and squared norm2ell. At degree ell equal traces would imply
2=+/-1 mod m, impossible here.

For index3, blindly taking these same classes gives the ZERO waveform:
g^2 H=(gH)^-1, hence identical trace multisets. For indices3/4 the producer
instead uses a=0,b=1. The H measure has multiplicity2 except at its
f=gcd(ell,2) fixed points +/-1; gH is injective and its image disjoint. Thus

```text
sum_x w_x^2 = (2ell-f) + ell = 3ell-gcd(ell,2).
```

The first excluded moment is `ell*(2-Tr(g^ell))!=0`: trace2/norm1 forces the
element to be1, whereas g^ell has order m>1. Every column's squared-range
sum adds1 for the constant row. Using support cardinality or pretending all
trace fibers have size1 would undercharge the variance. At very small ell
the exact formula can have no multiplicity2; the formula governs, not a
blanket assertion about fibers. Index2 is excluded by ell<=floor(p/2).

### Actual Setup, Costs And Results

The existing verified helper constructs `F_p[u]/(u^2-nu)` with a checked
nonsquare nu. Deterministic Cayley search tests `g_s=(1+s*u)/(1-s*u)` and
verifies exact order p+1 by its prime factors. This chart contains all norm-one
elements except -1, so it contains a primitive generator. Factorization,
candidates and degree-two field operations are charged, polynomial in explicit
p; none is assumed to cost only polynomial in log p or supplied as advice.

Exact cyclic inversion and denominator-aware rounding are reused. The same
command now saves eighteen witnesses: ten split, eight nonsplit. Each new
parameter has a seeded public word and quarter-field spike, without target
rerolls or planted answers:

|p|d=ell|nonsplit radius|best split radius at same d|public-word norm|denominator bits|
|---:|---:|---:|---:|---:|---:|
|47|6|7|13|4|16|
|107|9|9|21|4|141|
|509|15|13|37|7|954|
|1019|17|14|78|8|2060|

Best split uses the smallest divisor of p-1 at least d. Its certificate is
uniform over the SAME target family, not an unmatched favorable trial. All
four new choices satisfy the known uniform-interval sufficient KV inequality
and have all-target classical failure certificates <=1/2. No quantum execution
or speedup is claimed. The general bound still requires independent review.

Quotient controls at p47,ell12/16 retain squared norms34/46, NOT24/32.
Independent tests implement field elements as PAIRS of integers, enumerate
generator order, rebuild trace counts, check moments, compare exact matrix
inverses and validate native polynomial outputs. Failed zero-width targets
and all their rounds remain in the record. The larger rational denominators
are paid in coin bit lengths and arithmetic, not treated as field-sized.

The trace/Dickson background is standard; see Shparlinski-Voloch,
[On the Waring problem with Dickson polynomials modulo a prime](https://doi.org/10.53733/579),
Section2.2. This RS translation-frame attack and its accounting are LOCAL
applications, not a theorem attributed to that paper or a novelty claim.

## Deterministic Sparse Nearest Bound

The producer now also executes nearest row-coordinate rounding. For all present
waveforms the L1 mass is2ell, including the weighted trace fallback, and at
least one coordinate is zero. Every column has L1 sum at most2ell+1, including
the constant row. Coordinate errors<=1/2 imply raw INTEGER radius<=ell for
EVERY target. The implementation computes this bound from the actual waveform
and checks the output against it. No rounding coins are used. At low degree
this is stronger than the independent tail bound, although not at all rates.
The report labels random tail values as comparison-only in nearest mode;
it does not pretend the independent-coin proof applies to deterministic choices.
Two extra native nearest controls at p61,ell5 andp47,ell6 bring the current
torus report to20 witnesses. The earlier dense nearest-rounding spike falsifier
is still valid in its dense regime and is not a general sparse-frame barrier.

## Next Scientific Question

Seek bounded sparse integer waveforms with vanishing moments WITHOUT the
subgroup divisibility condition, even after allowing BOTH tori. A candidate is a Prouhet finite-difference
product `W(X)=product_j(1-X^(2^j))`: order-d zero at1 gives d vanishing power
moments, support2^d while2^d<p. Its variance cost is exponential in d, which
may make it uncompetitive; do not promote it without the actual cost and
same-parameter comparison. General near-linear-support moment matching is
NOT provided by this suggestion. A stronger divisor-free two-split-fiber
construction has now been implemented in INTERVAL_SPLIT_FIBERS.md, including
a uniform setup criterion, real setup failures and native witnesses. Read it
before adding another waveform interface or another batch of named bridges.

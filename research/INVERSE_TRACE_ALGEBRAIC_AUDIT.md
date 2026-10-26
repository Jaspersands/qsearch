# Inverse Trace: Exact Algebraic Models, Not Automatic Solvers

2026-10-22. Local mathematical audit, REVIEW PENDING. Known algebraic
representations and a scoped linearization countercertificate. No new
quantum mechanism, general classical lower bound, or cryptosystem attack.

## Research Decision

The earlier n17/n31 classical witnesses are real, but the guaranteed local
flats do not yet supply an asymptotic fixed-rate solver. The suggested next
step was to investigate inverse-trace algebraic immunity. That investigation
changes the priority: obtaining low-degree equations is NOT the missing
capability. A zero-complete quadratic description already exists after a
small lift. The missing capability is solving its globally coupled system.

This pass supplies an exact model, countercontrols for lossy alternatives,
and a proof that adding ONLY local equations to an independent-monomial
linearization cannot constrain its original variables. The next algebraic
attack must exploit cross-block relations, actual product consistency, or
a target-adaptive construction. Do not build a larger local relation miner.

## Literature Checked And Limits

- [Nawaz, Gong and Gupta, Sections 3-4](https://cacr.uwaterloo.ca/techreports/2006/cacr2006-09.pdf)
  explicitly construct low-degree multipliers for inverse-trace functions.
  Their use of trace polynomials, Frobenius and binary exponent weights is
  prior art; it is not a new technique discovered by this repository.
- [Feng and Gong, ePrint record](https://eprint.iacr.org/2013/585) states the
  exact algebraic immunity ceil(2*sqrt(n))-2. The record is accessible; its
  PDF returned403 in this pass. The exact lower-bound proof is NOT locally
  reviewed or needed for the certificates below.
- [Nawaz, Gupta and Gong, Sections 2-3](https://cacr.uwaterloo.ca/techreports/2006/cacr2006-34.pdf)
  analyze low-degree relations of power-map S-boxes. Such relations are old
  cryptanalytic tools. Neither their existence nor a historical XSL-style
  equation count establishes a fast solver for this repository's task.

The code independently verifies the simple identities it actually uses.
It does not import an unreviewed attack-complexity estimate, transfer stream
cipher data assumptions, or identify this task with AES key recovery.

## 1. A Sparse Multiplier And Its Missing Zero Constraint

Write f(x)=Tr(inv0(x)), q=2^n, and n>=3. Choose an exponent r whose n-bit
cyclic representation has m>=2, m<n set bits, with largest cyclic gap g.
The field-valued identity, valid also at zero, is

    x^r f(x) = sum_(j=0)^(n-1) x^((r-2^j) mod(q-1)).

Every exponent on the right is positive, because r is not a power of two.
Thus both sides vanish at zero. For a positive exponent below q, its binary
weight bounds the Boolean degree of its coordinate functions: each Frobenius
power is binary linear, and multiplying the indicated powers gives that
many linear factors. No truth table is necessary.

Subtracting a set bit lowers the weight by one. Subtracting from a zero run
borrows from the next cyclic set bit, so the weight is at most m+g-2. Place
the set bits at floor(j*n/m), then optimize m. The executable certificate
also checks every resulting exponent rather than relying on that bound.
For n17/31/61 it obtains equation degrees7/10/14. This is a field-valued
variant of the known multiplier idea, not a novelty claim.

The equation x^r(f(x)+b)=0 is equivalent to f(x)=b ONLY for x!=0, or when
b=0. For b=1 it admits the false value x=0. In the full code-constrained
system Hx=0, the all-zero vector consequently satisfies every multiplied
equation for EVERY target if the missing nonzero constraints are forgotten.
That would be a fake dequantization. On b=1 coordinates one must enforce
nonzero explicitly, for example by an inverse witness with xy=1.

Using only one Boolean component Tr(lambda*x^r) as the multiplier loses
additional nonzero inputs on which that component vanishes. The code's
field equation means ALL its binary components, not one selected trace.
Low algebraic immunity is not an input-preserving reduction to linear
algebra, nor does it bound the solving degree of the coupled system.

## 2. A Smaller-Degree, Zero-Complete Model

Introduce y_i as a field variable for each coordinate. The EXACT local
inverse graph, including inv0(0)=0, is

    x_i^2 y_i = x_i,
    x_i y_i^2 = y_i.

If x_i!=0, the first equation forces y_i=1/x_i. If x_i=0, the second
forces y_i=0. Conversely every native inverse pair satisfies both.
Retaining only the first equation allows x=0,y arbitrary; retaining only
the second allows y=0,x arbitrary. Requiring xy=1 everywhere incorrectly
removes legal zero coordinates.

These two equations are quadratic OVER F_2, not degree-two polynomials
in the field variables: Frobenius squaring is binary linear. Together with

    Hx=0,  Tr(y_i)=b_i,

they are an exact existential formulation of the native task. There are
2nN binary variables and nK+N independent binary linear constraints, leaving
(2N-K)n-N variables after linear elimination. The raw count of quadratic
component equations is 2nN; that count is NOT an independence claim.

The compiler additionally supplies three valid quadratic field identities:

    x^4 y = x^3,
    x y^4 = y^3,
    (xy)^2 = xy.

Each is still Boolean-quadratic, and all hold at zero. They may strengthen
a particular algebraic solving procedure, but are redundant as native
constraints. Their actual coefficient rank is computed, not assumed to be
5n or used to infer semiregularity. Public field moduli are retained.
The local compiler uses only polynomially many basis arithmetic operations;
it does not learn equations from exponentially many S-box values.

## 3. Full Affine Hull Of The Inverse Graph

For n>=3, the graph G={(x,inv0(x)):x in F_q} affinely spans F_2^(2n).
Proof: any affine relation can be written

    Tr(alpha*x + beta*inv0(x))=c.

At x=0 it forces c=0. The two trace polynomials have exponents respectively
2^j and q-1-2^j. The latter have binary weight n-1>=2, so the two exponent
sets are disjoint. They are all below q. A degree-below-q polynomial
vanishing on the entire field is zero; its coefficients force alpha=beta=0.
The n=2 exception is real: inversion on F_4 is the binary-linear square map.

Thus every pair (x,y), including a false inverse pair, is an ODD binary sum
of genuine graph points. Equivalently the augmented vectors (1,x,y) have
full linear span of dimension2n+1. This is a proof for all n>=3, not an
extrapolation from a sampled rank.

## 4. Why Purely Local Linearization Is Vacuous

Lift a local pair to a vector of its monomials, including a constant1 and
all original x/y bits. Allow the lifted coordinates to become independent
binary variables. Impose ANY collection of linear constraints valid on all
genuine local lifts: these may encode the five quadratic identities, all
local quadratics, or arbitrary further local polynomial identities.

An odd sum of genuine lifted points satisfies every such affine linear
constraint, since its constant coordinate remains1. By Section3 its
projection can be ANY original pair (x,y). Consequently the projection
of this block-local linear relaxation is the ENTIRE F_2^(2n).

For the global code task, choose x_i=0 everywhere, and choose y_i with
Tr(y_i)=b_i. Each block has a relaxed lift of that pair; Hx=0 and all raw
trace equations hold. For any nonzero target this projected word is NOT
a native solution. Therefore even all valid local equations plus the
original unmultiplied global linear equations cannot distinguish these
false projected words. Increasing local relation degree ALONE does not
repair the problem.

This is deliberately restricted. It does NOT cover enforcing lifted
variables as actual products, multiplying global checks by variables,
cross-block XL/Macaulay closure, Groebner elimination, branching, convex
relaxations over another coefficient field, or adaptive flat algorithms.
No generic algebraic-attack lower bound follows. The independent-monomial
relaxation is not the native quadratic system in Section2.

## 5. Short, Replayable Countercertificates

At n17/31/61 the workflow samples a fixed capped set of genuine graph points
using the public inverse evaluator. Binary elimination attempts to express
(1,0,y*) with Tr(y*)=1 as an odd sum. A failed rank acquisition reports
UNKNOWN; it does not regenerate the original input or count as evidence.

The report retains the selected genuine graph points, public modulus,
projected false pair and XOR of their full quadratic lifts. It checks:

1. Every selected point satisfies the exact native inverse graph.
2. The number of selected points is odd and their projection is (0,y*).
3. Every compiled linearized quadratic residual is zero on the XOR lift.
4. The projected pair violates the native inverse graph, and its true
   monomial lift differs from the recorded relaxed lift.

Odd sums also certify satisfaction of ALL local polynomial identities,
not just the compiled examples, by the argument in Section4. The finite
certificates do not replace the all-n affine-hull proof.

## Next Decisive Work

Do not run a larger local-annihilator campaign. The useful classical target
is now explicit: exploit the structured, globally coupled quadratic system
while keeping both inverse equations and all Boolean product consistency.
A specific cross-block elimination rule needs a proven or measured solving
degree with full costs, not a surplus-of-equations argument. Native witness
verification remains mandatory after ANY relaxation or multiplier solve.

The proposed quantum construction is neither disproved nor strengthened by
the failure of this weak relaxation. Classical hardness remains unresolved.
Independent scrutiny of its support-mask/coherent-composition proof remains
at least as important as pursuing another classical solver implementation.

Replay: `python -m theorems.inverse_trace_algebraic_audit --write` and
`tests/test_inverse_trace_algebraic_audit.py`. Standalone artifact:
`research/classical_baselines/inverse_trace_algebraic_audit.json`.
No qsearch/UI/registry admission or general-purpose solver is added.

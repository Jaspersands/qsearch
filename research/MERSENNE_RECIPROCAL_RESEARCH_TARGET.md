# Growing Mersenne Reciprocal-Trace Target

2026-10-29. A NEW explicitly described relation, not a solution or an
equivalent reformulation of the original inverse-trace problem. No novelty,
classical hardness, practical advantage, or Shor-level result is claimed.
The motivation is to retain a paid quantum source while making the
fixed-genus classical Fourier-access shortcut inapplicable as stated.
That is a reason to investigate classical algorithms, not evidence that
they fail.

**2026-10-29 update:** the [reviewed carry construction](MERSENNE_CARRY_WALSH_DRAFT.md)
now gives a theoretical polynomial-time signed Walsh evaluator for THIS
fixed family, with a capped reference implementation. Combined with the
[clipped sampler](MERSENNE_CLASSICAL_ACCESS_AUDIT.md), it removes local
Fourier sample/query access as an asymptotic classical obstacle. It does
not solve the coupled relation, establish practical runtime, or justify
moving to another exponent merely to evade a successful baseline.

**2026-10-30 decision:** the [direct scalar-flat classical attack](MERSENNE_SCALAR_FLAT_ATTACK.md)
found independently verified witnesses on the fixed n17 all-one, n17 mixed
target, and n31 all-one inputs, using the original predicates and parity
equations. This is a finite search result, not a general asymptotic solver or
uniform sampler. The [independent research-value audit](audits/reviews/2026-10-30-mersenne-research-value.md)
recommends shelving this specialization as a priority quantum-breakthrough
track after the bounded triage. Preserve its valid mathematics; reopen the
track only for a concrete new algorithmic mechanism or meaningful reduction,
not a larger benchmark, different exponent, or another failed attack.

## 1. Public Input And Exact Task

Let q=2^n, n an odd prime at least17, N=n^2, K=floor(N/8), and choose

    s=floor((n-3)/4), d=2^s-1,
    f_s(x)=Tr(inv0(x)^d), inv0(0)=0.

The input gives N distinct field points alpha_i and N target bits b_i.
The field representation is public and part of the checked instance.
Find x satisfying

    sum_i alpha_i^j*x_i=0 for 0<=j<K,
    f_s(x_i)=b_i for every i.

The stronger sampling task asks for the uniform distribution on this exact
fiber, with a separately accounted failure flag. Arbitrary public points
and target bits are allowed; the consecutive-point all-one instance is
only the reproducible budget fixture. Field arithmetic, input reading,
verification and source construction are charged. There is no table,
hidden truth function, supplied witness, or oracle hardness assumption.

The implementation uses the strict tag `mersenne_reciprocal_trace_v1`
and binds s, the modulus, points and targets. Untagged legacy instances
are rejected. Its broader arithmetic API allows other odd coprime (n,s)
for controls; these are not automatically covered by the prime-degree
research rationale. s=1 is precisely the old predicate. s=2 is inverse
cubic. Neither an old witness nor an old spectral certificate transfers
to s>1 without checking the new equations.

## 2. Efficient Local Roots, Not A Native Classical Solver

The identity gcd(2^s-1,2^n-1)=2^gcd(s,n)-1 shows that d is invertible
modulo q-1. Put e=-d^(-1) mod(q-1). Then

    u -> x=u^e, with 0->0,

is a bijection from Tr(u)=b onto f_s(x)=b. Each local accepted set has
exactly q/2 elements. A uniform (n-1)-bit seed gives a uniform trace
hyperplane element: because Tr(1)=1, the constant basis coefficient can
be set to repair the trace of the other coefficients. The inverse seed
is recovered from inv0(x)^d. Thus an ideal reversible implementation can
uncompute the seed; merely evaluating a many-to-one map would not suffice.

Binary exponentiation takes O(n) field operations per coordinate, even
when d and e are exponentially large as integers. Schoolbook arithmetic
gives a polynomial Boolean-gate construction (for example O(N*n^3)
for these powers, before other protocol work). The additive Fourier
transform uses the explicit trace pairing and binary linear operations.
No genus-sized curve representation is needed for this quantum source.
The module implements classical arithmetic primitives, NOT the coherent
decoder or a compiled quantum circuit.

This also gives classical uniform LOCAL roots. It does not couple them
to Hx=0, give classical Fourier amplitudes, or sample the native fiber.

## 3. Reject The Misleading Low-Degree Parameter Choice

For k=s^(-1) mod n with 1<=k<n, define

    I=sum_(0<=j<k) 2^(j*s mod n).

The exponents are distinct. Telescoping gives (2^s-1)I=1 mod(q-1),
so I=d^(-1), its binary weight is k, and e=(q-1)-I has binary weight
n-k. The vector power map u->u^e has Boolean degree n-k. Separately,
f_s(x)=Tr(x^(q-2^s)) has Boolean degree n-s. Its exponent has a full
length-n Frobenius orbit, so no trace-term cancellation lowers that degree.

Choosing s=floor(n/4) would give a degree-four root map whenever n=4s+1.
For instance n17,s4 has root degree4, not a generic high-degree source.
This control remains visible rather than being silently discarded.

For the revised prime-degree choice, n=4s+c where c is3 or5. Writing
w=n-k, we have c*w=4 mod n, hence

    w=(j*n+4)/c for some 1<=j<=c-1.

In particular w grows at least linearly as n/5. Both displayed degrees
grow, but HIGH DEGREE IS NOT A HARDNESS ARGUMENT. The graph still has a
compact quadratic description below.

An even more explicit warning emerged independently from Huygens and
Pauli. Put sigma(t)=t^(2^s), r=n-4s in {3,5}, and

    Phi(t)=(t*sigma(t)*sigma^2(t)*sigma^3(t))^(2^r).

This is a permutation of Boolean degree4, including zero. Telescoping
gives inv0(Phi(t))^d=t^(2^r-1), and hence

    f_s(Phi(t))=Tr(t^(2^r-1)).

The entire problem therefore has an exact reparameterization with
quartic parity equations H*Phi(t)=0 and cubic (r=3) or quintic (r=5)
local predicates. It does NOT preserve the original linear parity system.
Equivalently, the root graph x=u^e obeys x^(2^r-1)=Phi(u), a graph of
degree at most5. Large degree of the explicit inverse function must not
be confused with absence of low-degree graph equations. Nor have we
proved a degree lower bound after restriction to one trace hyperplane.

## 4. Spectral Bound With The Correct Growing Genus

Define W_s(v)=sum_x (-1)^(f_s(x)+Tr(v*x)). Balance gives W_s(0)=0.
For v!=0, the Artin-Schreier curve

    y^2+y=x^(-d)+v*x

has two odd-order poles, d at0 and1 at infinity. Its smooth completion
has genus g=(d+1)/2=2^(s-1), with one rational point above each pole.
Counting the remaining fibers gives #curve=q+W_s(v), including the
zero-extension term of W. Consequently

    |W_s(v)-1|<=2^s*sqrt(q),
    |W_s(v)|/q<=beta=min(1,(1+2^s*ceil(sqrt(q)))/q).

The standard pole/genus and Weil ingredients are stated in
[Carmon, Theorem3.1 and equation3.6](https://arxiv.org/html/1409.3694v1).
The point-count identity here is the direct specialization just derived.
The old inverse-trace bound 1+2*sqrt(q) is WRONG for general s; neither
that bound nor its squared Fourier point-mass envelope is reused.
v=0 is not a two-pole curve and is handled by balance instead.

In the proposed regime g=2^Theta(n) while beta=2^(-n/4+O(1)). Thus
generic algorithms polynomial in g and n do not give a polynomial-in-n
Walsh evaluation guarantee. For comparison,
[Hubrechts's characteristic-two point-counting algorithms](https://arxiv.org/abs/math/0607346)
are polynomial in genus. This observation does NOT rule out a specialized
algorithm exploiting these particular exponents or sparse equations.

## 5. Conditional Paid Quantum Guarantee

Use the existing full-list protocol, not a new circuit-search heuristic.
For C=ker H and D=rowspan H, write Omega_b for the native fiber and

    lambda_b=2^N*|Omega_b|/q^(N-K),
    eta=min((q^K-1)*beta^(N-K+1),
            q^K*(beta+(1-beta)/q)^N).

Character orthogonality and the MDS weight bound give
|lambda_b-1|<=eta for EVERY input target and set of distinct points.
For w=floor(3N/5), put tau=2^-N*sum_(j<=w) binom(N,j). The strict
Johnson inequality (N-w)^2>N*(K-1) permits complete polynomial-size
Reed-Solomon lists, padded to one public power-of-two size P.

The exact IDEAL probability, per full attempt, is

    p_native=lambda_b*tau^2/P >= max(0,1-eta)*tau^2/P.

Conditioned on native success, the output is exactly uniform on Omega_b.
All failed mask/projection/verification outcomes are retained as ABORT.
With independent full attempts and a fixed cap T, failure is (1-p)^T.
This is the unnormalized radius-filter protocol; normalizing a ball at
source preparation changes the probability ledger and is a different
implementation.

The proof is the already recorded
[exact predicate channel](EXACT_PREDICATE_CHANNEL.md). It requires an
actual clean root source, complete reversible list decoding, fixed public
padding, erasure of message/list/index/work registers, and final native
verification. Finite gate/source/decoder errors require their own total
variation and failure budget. None of these compiled operations is newly
implemented here, and an analytic certificate is not a runtime measurement.

For s=n/4+O(1), the distance estimate alone gives
log2(eta)<=-3*n^3/32+O(n^2); the binomial bound may improve it.
In fact for n>=17 the rounded beta obeys beta+1/q<q^(-1/4), directly
from s<=(n-3)/4 and ceil(sqrt(q))<=sqrt(q)+1. The binomial expression
therefore gives eta<q^(-N/8), since K<=N/8.
The binomial tail is 2^-Omega(N), the Johnson gap is Theta(N^2),
and P is constant. This yields a conditional ideal polynomial-time
uniform sampler for this explicitly defined relation, not a separation.

Exact rational arithmetic gives these replay controls:

| n | s | g | Root degree | Predicate degree | eta upper | Tail upper | P |
|---|---|---|---|---|---|---|---|
|17|3|4|11|14|2^-976|2^-11|8|
|31|7|64|22|24|2^-4448|2^-31|8|
|61|14|8192|13|47|2^-33031|2^-112|8|

Each ideal success lower bound exceeds1/9. These are parameter-bound
mathematical budgets, not large-field quantum executions or a hardness
benchmark. At n17 the genus is still only4; small controls cannot support
an asymptotic classical-access obstruction.

## 6. Serious Classical Comparators

**Systematic accepted completion.** Choose N-K free coordinates uniformly
from their accepted local sets, solve K pivot coordinates by Vandermonde
elimination, and verify all targets. Each native witness has exactly one
free-coordinate preimage. Therefore accepted outputs are EXACTLY uniform,
and the per-attempt success probability is

    |Omega_b|/(q/2)^(N-K)=lambda_b*2^-K.

The expected number of attempts is between 2^K/(1+eta) and
2^K/(1-eta) when eta<1. This is an explicit exponential BASELINE, not a
lower bound on other classical algorithms. Comparing per-attempt
probabilities without their work costs is not a speedup demonstration.

**Binary quadratic structure.** Set h=2^(s-1). For x!=0, the local
predicate is equivalent to existence of v satisfying

    v^2+x^h*v+b*x^(2h)=x.

Indeed divide by x^(2h) and set y=v/x^h; then
y^2+y+b=x^(-d), whose trace is the required condition because n is odd.
At x=0 the equation forces v=0 for BOTH b values. That branch must be
excluded for b=1 or the lifted system acquires false witnesses. Nonzero
accepted x has two v lifts; accepted zero has one. Uniform lifted
solutions therefore do not automatically give uniform native solutions.

Frobenius powers and squaring are binary-linear. The only nonlinear term
is x^h*v, so the full problem has a polynomial-size, highly structured
binary quadratic representation despite its exponential formal genus.
Fixing v makes the equations linear in x; coupling those choices to H
is the unresolved part. Generic MQ hardness cannot be imported.

Equivalently, with sigma(x)=x^(2^s),

    f_s(x)=Tr(x/sigma(x)) for x!=0,
    u*sigma(x)=x, Tr(u)=b.

Since sigma has fixed field F2, the nonzero solution x is unique for
each nonzero u. This is a special cyclic Frobenius-ratio graph, not a
random nonlinear predicate. Hilbert-90-type structure and norm identities
are attack targets. The zero conventions must still be enforced.

**What a lifted-flat argument actually proves.** For s>=3, polarization
of the lifted equation on an affine F2-space gives
a^h*c'+a'^h*c=0 for all direction pairs. A nonzero vertical direction
forces the whole direction space to be vertical, of dimension at most1.
Otherwise all directions have c=alpha*a^h for one alpha. The containing
graph is v=C+alpha*x^h, and its exact intersection with the lifted locus is

    L(x)=C^2,
    L(X)=A*X^(2^s)+C*X^(2^(s-1))+X,
    A=alpha^2+alpha+b.

The coefficient of X is1, so L is nonzero and the flat dimension is at
most s. This includes degenerate A or C. Conversely Tr(A)=b and
C^2 in im(L) supply alpha and a basepoint by binary linear solves;
the solution dimension is dim ker(L), with the b=1 zero guard retained.
This gives a concrete classical construction interface, not just a filter.

Two important limitations prevent a false negative result. First, s is
about n/4, so the preceding coarse bound alone would not obstruct a
large-flat approach. A stronger bound below does. Second, affine x-sets
need not have affine lifts. Halley's independently found and
parent-replayed F_(2^17) counterexample uses modulus X^17+X^3+1,
offset0x9579 and basis {0x3377,0x3451,0x87b1,0x136af}. All16 points
satisfy f_3(x)=1, although dimension4 exceeds s=3. It is a LOCAL accepted
set, not a native parity witness or an asymptotic construction. The test
suite preserves it specifically to prevent extending the lifted bound
to all local affine search methods.

**Stronger constant lifted-flat bound.** Pauli and Halley independently
derived a sharper bound for the canonical n=4s+r. The trace adjoint of
L, postcomposed with the 2^s-Frobenius, is

    M(z)=z^(2^s)+C^2*z^2+A*z,

with the same kernel dimension. For a root, sigma(z)=C^2*z^2+A*z.
Iterate this relation four times: sigma^4(z)=P_4(z), where P_4 is a
linearized polynomial of ordinary degree at most16 (Frobenius acts on
its coefficients at each step). Since 4s+r=n, every root satisfies

    P_4(z)^(2^r)+z=0.

This is a NONZERO polynomial of degree at most2^(r+4): the isolated
linear term cannot cancel terms of degree at least2^r. Thus

    dim ker L <= min(s,r+4) = min(s,7 or9).

An independent derivation rewrites Frobenius using the generator
tau=Frob^(4^(-1) mod n); the operator then has tau-degree r+4.
[Csajbok--Marino--Polverino--Zullo, Result1.1](https://arxiv.org/pdf/1806.05962)
supplies the corresponding kernel bound. The bound above is our explicit
specialization, not a quoted theorem about this research family.

One product of affine lifted flats therefore has at most7N or9N binary
parameters. Eventually this is less than the nK parity equations, so
an automatic full-row-rank construction cannot work. This is NOT a
proof of inconsistency: target-adaptive flats, unions, nonlinear lifts,
and specially consistent lower-rank systems remain possible. In
particular the projected-flat counterexample is unaffected.

**Independent fixed-auxiliary trials.** Choose each v_i uniformly from
F_q, excluding zero at one-target sites, then solve the binary LINEAR
system in x consisting of Hx=0 and all lifted equations. A consistent
solution passes the native predicate, with the zero guard supplied by
the nonzero v_i at one-sites. If m targets are one, counting at most
2^N lifts for each native witness gives

    Pr[consistent] <= (1+eta)*q^(-K)*(q/(q-1))^m < 2*q^(-K).

The last inequality uses the canonical n>=17 regime, eta<q^(-N/8),
and m<=n^2. This counts the probability that ANY completion exists,
even granting the entire linear solve for free; it is not just the
success rate of one arbitrary solution selector. Independence and the
specified uniform choice are essential. Correlated, target-adaptive
auxiliary values are not excluded. The resulting trial is worse than
the already available systematic completion baseline, which costs
about2^K attempts rather than at least order q^K attempts.

For all-one targets, a single common auxiliary value v_i=v is impossible.
Summing all lifted equations, using the j=0 parity row and odd N, forces
v=0. Then x_i^(2^s)=x_i, so the nonzero guard and gcd(s,n)=1 force every
x_i=1, contradicting that same parity row. This is a deterministic
falsifier for the common-value construction, not all coordinated choices.

**A constrained norm problem remains.** At an all-one site choose rho
with rho^2+rho+1=0 in F_(q^2), put a=x^h and w=v+rho*a. The lift says

    Norm(w)=x,  Norm(w)^h=Trace_(q^2/q)(w).

A norm-construction attack must enforce this Frobenius relation between
norm and relative trace, retain nonzero norms, AND solve H*Norm(w)=0.
Ordinary norm factorization alone supplies neither condition. This
specific coupled system remains a plausible constructive attack target.

**Easy subcases.** For s=n-1, f_s(x)=Tr(x), so the whole search relation
is a binary linear system. In particular the n3,s2 cubic control is
dequantized, not a favorable small example. Composite n admits subfields
that the prime-degree proposal avoids; the permissive arithmetic API does
not erase those attacks. Fixed-s source access and large-degree
source access must not be conflated.

## 7. Prior Art And What Would Actually Matter

This uses existing decoding/Fourier-sampling machinery.
[Jo, Theorem5.2 and Remark5.3](https://arxiv.org/html/2607.16541v2)
already supplies the fixed-length complete-list projection and its
probability cost. The prime-field optimization conclusions in that paper
are not automatically characteristic-two results. The prime-power generic
framework is separately discussed in
[Horinaga--Yamakawa](https://arxiv.org/pdf/2607.14650).
Our specialization needs its explicit source and fiber-count arguments;
growing-characteristic conclusions cannot simply be imported into F_(2^n).

[Blondeau--Canteaut--Charpin](https://arxiv.org/html/1108.4753v2) study
the Mersenne monomial family itself. Their differential counts reduce to
linearized trinomials; the exponent-index symmetry takes t=n-s to s+1,
not s. These are relevant algebraic attack tools, not a signed-Walsh
evaluation oracle or a coupled native sampler. The inspected sources did
not provide such a polynomial backend for the proposed growing regime;
this is a bounded literature finding, not a nonexistence result.

There is currently no reduction from a standard hard problem, no
classical lower bound, and no claim that the family itself is new.
An exponent search, a small SAT timeout, or the genus formula alone would
not materially change that assessment.

Historical ranked tasks (superseded by the 30 October decision above;
local Fourier access in item2 is now available in writing):

1. Exploit the coupled quadratic/Frobenius-ratio representation to produce
   a classical completion or sampler with a proved cost. Preserve H,
   arbitrary public points, target bits, and zero handling. Prioritize
   target-adaptive auxiliary values or the quartic partial-norm system,
   not independent uniform or common auxiliary values already excluded.
2. Determine whether specialized Weil-sum formulas give efficient
   classical Fourier evaluation AND sampling. Exact amplitudes alone
   need a charged proposal/rejection or conditional-sampling mechanism.
3. Extend or break the old norm-construction attack for this actual new
   predicate. A nonlinear coordinate power changes H and is not a valid
   transfer by itself.
4. Identify a natural application or reduction with explicit input size,
   distribution, success, verification and access costs. A reduction that
   supplies the missing witness or exponential table is rejected.
5. Only after these attacks, invest in a scalable coherent receiver or
   sharpen constants. The main gap is scientific, not UI or circuit polish.

A polynomial classical search algorithm would end the SEARCH-separation
hypothesis, but a biased witness construction would not end the uniform
sampling question. A polynomial native sampler would end both. A special
Fourier algorithm would defeat the proposed access rationale but would
still need to be connected to native completion. A broken source/list/
cleanup assumption would invalidate the quantum bound. Each outcome is
useful; none should be hidden by changing the problem mid-comparison.

## 8. Implemented Scope And Replay

`theorems/mersenne_reciprocal_curve.py` implements strict tagged instances,
local predicate/root bijections, independent native verification, rational
ideal budgets, and explicitly capped Walsh/curve/Boolean-degree controls.
It does not implement the lifted-flat search, a native classical solver,
or a coherent quantum receiver. The exact quartic partial-norm map is
implemented as an attack interface, without pretending it preserves H.
The separate `mersenne_scalar_flats.py` now implements direct accepted-flat
search with the fixed native witnesses above; it makes no general-input
success guarantee or uniform-sampling claim.
The live certificate records input and
source hashes, conservative dyadic bounds and unresolved obligations:

```sh
python -m theorems.mersenne_reciprocal_curve --output research/reductions/mersenne_reciprocal_curve.json
python -m pytest tests/test_mersenne_reciprocal_curve.py -q -W error
```

The report's default mode writes JSON to stdout, not the registry. No
candidate is promoted by this budget. Exhaustive curve controls are
capped at n<=5, functional controls at n<=7; native budgets enumerate
neither field elements, curves, codewords nor witnesses. Regression tests
also check the quadratic zero trap and a concrete coordinate-power map
that transfers predicates but breaks the original parity equations,
the partial-norm identities, and linearized-operator/adjoint ranks.

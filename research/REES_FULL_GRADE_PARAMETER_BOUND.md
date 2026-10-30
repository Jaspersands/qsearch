# Whole-Grade Rees Parameter Bound

29 October 2026. Proposed resource corollaries of the existing Rees lift
and pointwise central-descent argument. Bernoulli independently checked
the growing-degree arithmetic and source composition; Epicurus checked
the separate published fixed-degree branch. These are AI reviews, not
human endorsement, formal verification, or a novelty assessment. No
useful native application or quantum speedup is established.

## Result And Input Model

For an explicit genuine n-dimensional nilpotent Lie algebra L over a
supplied verified prime F_p, use its ACTUAL class c<p and put

    r = dim[L,L],       r_d = dim gamma_d(L),
    g_d = gcd(d,p-1),   D = n + sum_(d=2..c) r_d.

The ordinary coherent hiding-oracle contract, or the separately justified
independent coset-copy contract, is unchanged. All public algebra, label
width, queries/copies, arithmetic and physical approximation remain paid.
This is not a growing-class opaque-group input conversion or an extension
to arbitrary prime-power Lie rings. The zero algebra is trivial; r=0 uses
the abelian algorithm. Positive lower-central terms strictly decrease, so

    c <= r+1,       r_d <= r-d+2,       D <= n+r(r+1)/2.

The old scalar-flag schedule gives
`2^O(r^2 log(r+2))*poly(n,log p,access width,log(1/epsilon))`.
Two whole-grade schedules give a sharper bound:

1. **Large fields:** if p>=16*g_d^(2*g_d+2) for every g_d>=2, use the
   local symmetric SDE. The bound becomes
   `2^O(r log(r+2))*poly(n,log p,access width,log(1/epsilon))`, with an
   absolute polynomial exponent. The simpler p>=16*c^(2*c+2) suffices.
   No requirement that c or each original d divide p-1 is imposed.
2. **Bounded effective degrees:** for FIXED b with every g_d<=b, use the
   published vector SDE. The bound is
   `2^O_b(r log(r+2))*poly_b(n,log p,access width,log(1/epsilon))`.
   This needs no large-field guard, but its constants and polynomial
   exponent can depend on b. It cannot be asserted uniformly for growing b.

These are sharper deductions from existing ingredients. The second was
already implicit in the manuscript's full-grade and gcd formulas. Neither
is a new SDE primitive or a proof of priority for the Rees composition.
Outside these regimes the old arbitrary-prime bound remains available;
the numerical symmetric certificate deliberately rejects instead of
silently invoking an unbudgeted fallback.

## 1. Remove Whole Grades

After higher grades are removed, the central grade A_d has dimension r_d
and dilation acts by s^d. Measure vector labels lambda_i in F_p^(r_d),
solve the simultaneous reduced-power system

    sum_i x_i^(g_d)*lambda_i = 0,       x != 0,

and lift its nonzero entries by a public Bezout exponent u satisfying
`d*u = g_d mod (p-1)`. Set s_i=x_i^u for x_i!=0 and s_i=0 otherwise.
Thus s_i^d=x_i^(g_d), with a nonzero witness and no accidental 0^0=1.

The existing pointwise central conversion already accepts arbitrary
vector labels and any valid nonzero witness. No basis of the unknown
central intersection, random-label assumption or favorable measurement
postselection is introduced. Zero-scale targets are consumed/discarded;
Delta_0 is never applied. A vector witness removes one entire grade,
instead of invoking a scalar merge separately for every central line.

The effective degree changes only the CLASSICAL equations. The cover
still has dimension D, the initial lift still costs c original inputs,
and its group arithmetic still uses class c, not b or max g_d.

## 2. Explicit Large-Field Source Bound

Write a=r_d and g=g_d. Use arity a+1 when g=1; otherwise the symmetric
construction uses

    M_d = (a+1)*((g-1)*a+1).

In both cases M_d<= (d-1)*(r_d+1)^2. Hence

    P = product_(d=2..c) M_d
      <= (c-1)! * [(r+1)!/(r-c+2)!]^2
      <= r!*((r+1)!)^2
      = 2^O(r log(r+2)).

For a simpler envelope, P<=(r+1)^(3r), including the empty product at r=0.
This improves an asymptotic guarantee, not every small profile: at rank
one and g=2, full-grade arity is4 while scalar flags need3. A hybrid can
choose smaller schedules, but is unnecessary for this theorem or report.

The [symmetric construction](POWER_SDE_SYMMETRIC_CONTRACTION.md) has only
two collision levels and g^2 cells. Its character expansion proves a
counting estimate; the implementation does not enumerate its g^g terms.

## 3. Growing-Degree Arithmetic Is Charged

Do not infer a uniform running-time bound merely from the fixed-degree
statement. Use the explicit [finite-randomness budgets](POWER_SDE_RANDOMNESS_BUDGET.md).
For one positive-rank invocation with local abort allowance2^-k, put

    h = (g-1)*a+1,
    R = h*(a+3)+g*(g+1)/2,
    U = g+R*(g-1),
    B = k+1+ceil(log2 U),
    J = g*B,                K = 3*B,
    Q = J + sum_(j=1..g-1) 2*g^(j+1)*B + R*g*(g-1)*K,
    L = k+1+ceil(log2 Q).

These respectively bound root requests, failure-union terms, coset
generator trials, root-split trials, uniform field draws and bit-rejection
attempts. They give total abort at most2^-k and fair bits at most
`Q*L*ceil(log2 p)`. In particular

    Q <= g^g * poly(a,g,k),
    one invocation <= (1+g^g)*poly(a,g,log p,k)

bit operations for ordinary polynomial-time arithmetic, with an absolute
polynomial exponent. Details closing possible hidden costs:

- Trial division factors g, not p-1. Its cost is polynomial in numerical g.
- A scalar proposal checks at most g modular powers; exponent bit length
  is O(log p). The g^g rejection overhead is explicitly retained.
- A root request uses at most3B(g-1) polynomial power/gcd pairs, of degree
  at most g. Dense modular polynomial arithmetic has a fixed polynomial
  exponent in g and log p; no field enumeration or unbounded root routine
  is needed for this mathematical bound.
- Relation finding, rank compression, two-level support bookkeeping and
  original-witness verification are polynomial in a,g,log p.
- A verified-prime promise, or a polynomial-time primality algorithm, is
  required. The existing library's validation is NOT certified here to
  the entire executable's bit complexity or wall-clock behavior.

Since g<=c<=r+1, even the g^g term is2^O(r log(r+2)). Crucially, classical
work is the SUM of costs over merge nodes, bounded by the number of nodes
times the maximum invocation cost. Multiplying g^g overheads over every
grade would incorrectly charge public retries as recursive source calls.

## 4. Whole-Forest Failure And Precision

For epsilon in (0,1), let m=n+ceil(log2(3/epsilon)). The scheduled forest
has L_src=mP lifted leaves, c*mP original inputs, T<=mP-m merge nodes, and
I=L_src+T+m<=2mP complete instruments including leaves and final readout.
The terminal rank-failure bound is `1/((p-1)*p^(m-n))<=epsilon/3`.

Let T_rand count only nonlinear SDE invocations. If positive, assign

    k = ceil(log2(3*T_rand/epsilon))

to each bounded SDE. Their union abort bound is at most epsilon/3. If
T_rand=0 no random SDE allowance is needed. This improves a harmless
conservative allocation over all T nodes, without changing the theorem.
The exact report sums ALL stage calls and root/bit caps, not just depth.

Classical retries retain the measured label bank and happen BEFORE
conversion. Exhaustion emits ABORT; it does not redraw quantum inputs.
Because the successful ideal conversion is pointwise in labels and
witnesses, label-dependent acceptance does not change its target state.
Its abort probability still counts toward error. This is a paper-level
composition, not an instantiation of the current Lean total-policy premise.

Allocate epsilon/(3I) trace/flagged-instrument error per complete operation.
The precision logarithm is O(r log(r+2)+log m+log(1/epsilon)). Internal
gate counts must also enter synthesis tolerances; polynomial-size uniform
arithmetic adds only logarithmic overhead. Joint source errors must obey
the original source-bank contract. Marginal fidelity or separability alone
does not justify replacing independent inputs.

Uniform class-c BCH uses the existing O(c^4)-bracket ODE recurrence; each
dense bracket has polynomial cost in D. This avoids hidden free-Lie-word
expansion. `ReesCover.multiply` now actually uses this recurrence. This
public classical implementation does not compile reversible arithmetic,
source instruments or a full quantum receiver.

## 5. Published Bounded-Index Branch

The [Ivanyos--Santha accepted paper, Theorem11 and Section3.3](https://arxiv.org/html/1503.09016v2#S3)
supplies fixed-degree vector SDE algorithms. Its sufficient arity is

    B_1(a)=a+1,
    B_e(a)=[e^(e*(e-1)/2)*(a+1)^e]^ceil(log2(e+1)),   e>=2.

For fixed b>=2 set ell_b=ceil(log2(b+1)), E_b=b*ell_b and
C_b=b^(b*(b-1)*ell_b/2). For every e<=b,

    B_e(a) <= C_b*(a+1)^E_b,
    P <= C_b^r*((r+1)!)^E_b = 2^O_b(r log(r+2)).

The published final algorithm is deterministic and polynomial in arity
and log p at fixed degree. Its randomized quadratic warm-up, Proposition9,
also suffices for b=2 with arities a+1 and(a+1)^2, giving
`P<=((r+1)!)^2`. Uniformly bounded preprocessing failures can be allocated
over the forest without resampling sources. These are imported algorithms,
not newly implemented solvers or random-label heuristics.

Supplied primes p=2q+1 with q prime and q>c give g_d in{1,2}. No safe-prime
generation algorithm, density assumption or all-prime conclusion follows.
The old2^O_b(r^2) scalar-flag estimate is valid but unnecessarily loose on
this regime. For either new branch the sufficient polynomial regime is
`r log(r+2)=O(log I_input)`, with b fixed in the second. Abelian padding
can manufacture this regime and is not a meaningful native application.

## 6. Executable Certificate And Falsifiers

    python qsearch.py power-sde --rees-budget --write

The separate artifact `research/reductions/rees_full_grade_budget.json`
contains exact forest, rank-error, complete-instrument allocation and
bounded randomness counts for three profiles. It executes NO quantum
receiver. It does not certify profile realizability or primality; those
are caller promises, stated explicitly in its metadata. It covers the
symmetric branch, not the imported bounded-index solver.

For the class12 profile(13,11,10,...,1), supplied p=2^127-1 and epsilon1/3,
the full-grade source factor is7,640,436,342,325,248,000, versus
371,209,638,446,513,340,737,559,399,141,212,160,000 for scalar flags at the
SAME prime. There are17 terminal samples and
1,558,649,013,834,350,592,000 original inputs. This is still astronomically
impractical; a large ratio between sufficient bounds is not an experiment
or evidence of a useful quantum advantage.

Decisive boundaries and remaining work:

- Failure of the underlying Rees pointwise/source argument invalidates
  the corollaries. These numerical controls do not independently prove it.
- The [uniform compilation follow-up](REES_UNIFORM_INSTRUMENT_COMPILATION.md)
  now supplies the missing complete-instrument circuit-existence argument,
  including canonical encodings, finite-gate precision and primitive counts.
  It is not an emitted circuit backend or a physical gate estimate.
- The symmetric field guard is essential for this proof; do not extrapolate
  the branch to small primes. The budget has an explicit rejection test.
- Check a proposed native application against same-input classical attacks.
  [Exposed scalar wrappers and uniform full-support norm proposals](CONSTRUCTIVE_ROUTE_FILTERS.md)
  were rejected in the same pass. Neither a succinct circuit nor high
  written degree provides a surviving application.
- A general failure-aware formal instrument, specialist review, priority
  checking and an end-to-end useful application remain unresolved. The
  reviewed manuscript snapshot is not silently replaced by this addendum.

The existing small-commutator bound polynomial in p^r is a comparison,
not a hardness or novelty proof. Class-two HSP and its quadratic arithmetic
already have published polynomial algorithms at unrestricted derived rank.

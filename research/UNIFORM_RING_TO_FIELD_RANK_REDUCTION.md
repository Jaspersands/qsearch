# Uniform Ring-To-Field Derived-Rank Reduction

30 October 2026. Conditional mathematical corollary and public arithmetic
controls. Not a proved new HSP theorem, a novelty certificate, or a useful
application-level speedup. Independent automated reviews by Bernoulli and
Hooke checked complementary prior-art/uniform-cost and rank/channel claims.
No external researcher was contacted.

## Research Decision

Do not promote the recent direct prime-power cancellation constructions as
opening a new end-to-end input regime. A simpler outer reduction was
overlooked: restrict only the appropriate LOCAL order-at-most-p problem to
p-torsion, then apply the existing field algorithm. Derived additive rank
survives the reduction. This can be stronger than carrying the original
class through a direct mixed-order Rees tree.

The small-prime subset/Hensel method remains valid conditional arithmetic
and may be useful for direct receivers or narrower source models. Its
failure to enumerate the original large commutator does not distinguish
it from algorithms that first reduce the exponent. The two approaches
must not be compared using only the ORIGINAL commutator order.

An unintegrated direct-recovery budget draft was removed during this pass
after this comparison. Its first-M-successes counting argument was sound,
but duplicating that machinery was no longer the best next task. The
existing field schedule already includes paid repeated trees and final
recovery. Exact mixed-abelian terminal readout was retained as useful,
independently tested arithmetic.

## Conditional Claim And Input

Let L be a genuine finite nilpotent Lie ring with explicit additive
coordinates direct_sum_i Z/p^e_i, compatible structure constants, and
actual class c<p, for supplied verified odd prime p. Put

    n = number of additive cyclic factors,
    b = sum_i e_i = log_p |L|,
    R = d_add([L,L]).

If b=0, return the trivial subgroup immediately, before any error-budget
division. The nontrivial case below has b>=1.

B denotes the FULL explicit bit length, including e_i*log2(p) coordinate
precision, bracket constants and oracle label width. It is not log(e_i).
Access is the ordinary reversible hiding-label oracle on exp(L), with
its runtime T_f charged. No opaque-group chart acquisition, source inverse,
hidden coordinates, or field-sized table is free.

Conditional on the repository's all-prime field/Rees recovery theorem,
[RANDOM_COLUMN_REES_PARAMETER_BOUND.md](RANDOM_COLUMN_REES_PARAMETER_BOUND.md),
the following bound extends to this explicit ring input:

    2^O(R log(R+2)) * poly(B, log(1/epsilon)),

with an absolute polynomial exponent. Oracle work is Q*T_f in addition
to the stated public computation, with Q bounded by the same expression.
There is no exponential dependence on c or the additive exponents outside
B. This is NOT a claim that c<=R+1 in the original ring.

The uniform outer reduction below is a written construction, not a
complete implemented solver. In particular, the field Rees theorem and
uniform quantum receiver remain substantive inherited obligations. The
code in this pass implements p-torsion/bracket and annihilator arithmetic,
not the oracle algorithm.

## 1. Rank Is Preserved By The Actual Local Sections

For a finite abelian p-group A,

    d_add(A) = dim_Fp(A/pA) = dim_Fp(A[p]).

Subgroup rank cannot increase because U[p] embeds in A[p]; quotient rank
cannot increase because images of generators generate the quotient.
This is an ADDITIVE abelian rank argument, not a statement about generator
rank in arbitrary nonabelian groups.

Every local Lie object has the form M=S/K, with S a Lie subring of L and
K an ideal in S. Then

    M' = ([S,S]+K)/K
       isomorphic to [S,S]/([S,S] intersect K),
    [S,S] <= L'.

Thus d_add(M')<=R. Nested sections still have this property. No enlarged
free Lie cover may be substituted while retaining this rank bound.

Let Omega=M[p]. Bilinearity makes it an ideal of M. It is an F_p Lie
algebra, and

    Omega' <= M'[p],
    r_local = dim_Fp Omega' <= R,
    dim_Fp Omega <= n.

The first inclusion need not be equality. The nonzero lower-central terms
of a nilpotent FIELD algebra strictly decrease in dimension, hence

    class(Omega) <= min(c, r_local+1) <= min(c,R+1) < p.

Do not infer R+1<p: that need not hold. The original c<p supplies the
characteristic guard when R is large.

## 2. Uniform Reconstruction Of The Outer Algorithm

The normalizer/order-p recursion is prior art: see
[Ivanyos--Sanselme--Santha, Section 3](https://arxiv.org/html/0707.1260v1#S3).
Their published black-box theorem assumes constant class. The argument
here replaces the fixed-class collection implementation with explicit
integer-module arithmetic; it does not silently extend the quoted theorem.

Maintain a known Lie subring K<=h=log H in the ORIGINAL ambient L.
Initially K=0. At each round:

1. Compute N=N_L(K), then M=N/K with its public mixed-order coordinates.
2. Construct an ascending central flag 0=I_0<I_1<...<I_s=M with factors
   of order p. A flag is constructed in the quotient currently supplied,
   not from an assumed basis of h.
3. Scan upward. Invoke the field solver on I_i[p] with the restricted
   hiding oracle. Before the first nontrivial answer, the hidden
   intersection with I_i injects into I_i/I_(i-1), so its order is <=p.
   Therefore restricting THIS problem to I_i[p] loses no hidden element.
4. A nonzero recovered element lifts to x in N. Replace K by K+Z*x and
   restart in the ORIGINAL L. The extension is already a Lie subring
   because x normalizes K. Its order is p times the previous order.
5. If the whole flag yields trivial intersections, N_H(exp K)=exp K.
   The normalizer condition in a finite p-group forces exp K=H.

At |K|=p^k the flag length is <=b-k. Thus there are at most
b(b+1)/2 local solver invocations, including the last unsuccessful scan.
This cap is imposed even on erroneous branches. Previously correct local
answers justify the next order-p promise; an error is charged when it
first occurs, not retrospectively excused because a later input was invalid.

### Public Operations Have Fixed Polynomial Degree

Known submodules are represented by full integer relation lattices.
HNF/SNF WITH transformation maps supplies membership, intersections,
quotients, embeddings, and public sections. Keep coordinates reduced
modulo their actual ambient orders; invariant factors alone are not maps.
The matrices and their canonical transforms have polynomial bit length.
In original coordinates, each full preimage lattice lies between
D*Z^n and Z^n; its HNF entries are bounded by its determinant, at most
p^b. Canonical reduction and polynomial-bit transformation algorithms
prevent coefficient growth from accumulating through nested sections.

For x in L put D=ad(x). Since D^c=0, the finite exponential and logarithm
give the exact equivalence

    exp(x) normalizes exp(K)  iff  [x,K] subset K.

Both implications follow from exp(D) and log(1+(exp(D)-1)); all divisors
are prime to p because c<p. Their inverses are integer scalar operations
on the finite module and preserve every additive subgroup. Consequently
N_L(K) is found by linear congruences on brackets with generators of K.
This is not an enumeration of candidate normalizing elements.

A central flag can be built by computing the center of each remaining
quotient using linear congruences, extracting one order-p element with its
invariant-factor coordinates, and adjoining a lift. There are at most b
steps. Alternatively refine the elementary central factors of
P_(j+1)=p*P_j+[M,P_j]. Both use polynomially many module operations.

In a cyclic coordinate of order p^a, an order-p basis element is p^(a-1)
times that coordinate generator. Use EACH coordinate's exponent, not a
single common maximum exponent. Compute brackets on this basis in M,
then divide their known integer coordinate multiples by p^(a-1) to obtain
the F_p structure tensor. This is not inversion of p in a torsion ring.

Group arithmetic is the existing uniform BCH recurrence over Z[1/c!],
not a free-Lie word expansion. It uses O(c^4) bracket calls; the same
finite recurrence works on mixed modules with unit inversions. Actual
class c<=b<=B, so this is polynomial in B with an absolute degree, even
when c grows. A callback-only implementation does not certify this cost;
the supplied explicit structure tensor does.

No oracle or unknown subgroup is needed for these public operations.
They need not factor p-1, solve a discrete logarithm, or learn an opaque
Lie chart. Those claims would change the input model.

### One Original Query Per Local Oracle Query

For a local torsion subalgebra T<=N/K, use a fixed normal-form section
sigma:N/K -> N and its embedding in original L. Define

    f_local(t) = f(exp(sigma(t))).

K is normal in N and K<=h, so this function hides the correct local
subgroup. The section need not be a homomorphism. Reversibly compute the
representative, call the original U_f ONCE, and uncompute the public
workspace while retaining input and output label. Local quotient nesting
does not multiply original oracle calls; public map composition is paid.

In lifted coordinates local torsion means p*x lies in K, NOT p*x=0 in L.
The original normalizer is recomputed after each extension. Freezing the
first normalizer is already falsified by the tower in
[CLASS_THREE_HSP_THEOREM_DRAFT.md](CLASS_THREE_HSP_THEOREM_DRAFT.md).

## 3. Core Selection, Error And Prior-Art Comparison

On each genuine local field input, compute r_local rather than assigning
it the original class. If r_local=0 use abelian HSP. If r_local<=1 the
class is <=2, so the published nil-2 algorithm already suffices. For
general r_local<=R use the existing all-prime field bound.

In particular, when p<16(R+1)^2, every field core has derived subgroup
of order <=p^R. The published small-commutator algorithm costs polynomial
time in explicit input size plus that order:
[Ivanyos--Magniez--Santha, Theorem 11](https://arxiv.org/html/quant-ph/0102014v1#S5).
Thus it gives 2^O(R log(R+2))*poly(B) after exponent reduction. This does
NOT set the original |exp(L)'| equal to p^R. Its order can be exponentially
larger in the additive exponents.

For larger p the repository's random-column Rees field result supplies
the same parameter dependence, conditionally. The resulting ring bound
therefore inherits the FIELD proof/novelty questions. Arbitrarily large
prime-power exponents are also already allowed by the bounded-prime,
constant-class theorem of
[Imran--Ivanyos](https://arxiv.org/html/2304.08376v1); they are not by
themselves a new problem regime.

For total failure epsilon, allocate at most epsilon/[b(b+1)/2] to each
local solver, including its own failed source trees, final readout and
complete circuit approximation. A first-error union bound handles
adaptive calls. The field solver's precision overhead grows only by
O(log b+log(1/epsilon)); the outer polynomial factor and local input sizes
do not change the 2^O(R log(R+2)) dependence.

The exact explicit input has no shared stochastic chart setup. Any noisy
oracle, unverified shared preprocessing, or correlated source-bank error
must be charged separately and cannot be amplified away by reusing it.
This pass makes no new copy-only complexity claim; the ordinary-label
oracle supplies the cleanest complete input contract.

## 4. Classical Comparator And Falsifiers

The same public outer reduction is classical. An order-1-or-p hidden
subgroup in a local m-dimensional field group can be tested by uniform
samples, label hashing and collisions. A nontrivial collision supplies a
generator. Up to polynomial amplification, the local query scale is
p^((m-1)/2), with m<=n. Index detection, group reconstruction and label
costs remain paid. This is an upper bound, not an optimality claim.

Therefore use p^((n-1)/2)*poly(B,log(1/epsilon)) as a comparator where
appropriate, not enumeration of the huge original prime-power group.
Unrestricted-label abelian hidden lines already give oracle separations;
they do not make this a new nonabelian computational application. No
succinct native source with a new proved classical time separation is
established here.

Decisive controls and failure boundaries:

- Heisenberg over Z/p^2 has abelian L[p]=pL, but L'[p] is nonzero.
  The quotient L/pL is nonabelian. Thus Omega'=M'[p] is false, and taking
  original torsion ONCE is not a recovery algorithm.
- [x,y]=p*y on (Z/p^E)^2 has derived cyclic rank1 and classE<p.
  Local torsion has much smaller class. This falsifies c<=R+1 in L while
  illustrating why a direct class-dependent ring bound can be inferior.
- Distinct exponents require coordinate-specific torsion extraction;
  a common top power can kill short factors.
- A false-trivial local answer can invalidate a later order-p promise.
  Only a first-error argument with fixed clocks is legitimate.
- Successful cancellation or correct label frequencies do not certify
  the physical source instrument. The independent review retained the
  complete-channel, private-coins and joint-source premises.

## 5. Executable Boundary

`theorems/lie_torsion_reduction.py` validates a supplied mixed-module Lie
tensor, computes its lower-central profile and actual class, and compiles
its p-torsion field tensor. It is public arithmetic, not the full outer
normalizer recursion. The report refuses to certify hidden recovery.

`theorems/mixed_abelian_readout.py` recovers the exact annihilator of
SUPPLIED Fourier labels, using all prime-power denominators. If H is the
column basis of the observed label lattice and D the ambient diagonal,
the dual lattice basis is D*H^(-T), not H^(-T)*D. An exact certificate
checks duality, unimodular canonicalization, ambient containment and
determinant orders. Canonical full-preimage HNF tokens include aborts in
voting. An incomplete observed span can overestimate the hidden subgroup;
neither the source law nor complete hidden recovery is certified by this
arithmetic.

Run `python qsearch.py prime-power-sde --rank-reduction --write` for these
public controls. The report is not a quantum execution or a newly admitted
candidate. The next high-value question is the residual FIELD theorem and
a native application, not further general-exponent receiver infrastructure.

## 6. Review And Validation Receipt

Bernoulli identified the exponent-reduction/small-commutator overlap, then
checked the uniform explicit-coordinate reconstruction and triangular call
cap. Hooke independently checked rank transport, normalizer equivalence,
the completed written reduction, adaptive error and oracle transport. No
blocking mathematical finding remained within those review scopes. The
trivial b=0 endpoint was made explicit. Curie implemented the two arithmetic
modules and their independent controls; parent reviewed and integrated them.
All three agents finished and were closed. This is automated review, not
external expert endorsement or formal verification of the whole theorem.

The live report has seven torsion controls and four readout controls:

| Ring control | Original class | Derived rank | Torsion class |
| --- | ---: | ---: | ---: |
| Heisenberg over Z/9 | 2 | 1 | 1 |
| Its quotient modulo 3 | 2 | 1 | 2 |
| Short-factor mixed module | 2 | 1 | 2 |
| [x,y]=5y, exponents (4,4) | 4 | 1 | 1 |
| [x,y]=131y, exponents (128,128) | 128 | 1 | 1 |
| Class-three field control, p5 | 3 | 2 | 3 |
| Class-three field control, p163 | 3 | 2 | 3 |

For the exponent128 control, the bound of32,896 local calls is a SYMBOLIC
outer cap, not a quantum execution count. Its proposed section solvers
are already covered by published nil-2 HSP. The p5 class-three control
falls under the published small-commutator branch; the p163 control keeps
the conditional field/Rees obligation visible.

In the readout control on Z/3 x Z/9, an incomplete Fourier span returns
an annihilator of order9, versus order3 for the complete supplied span.
Both correctly refuse to certify unknown hidden-subgroup recovery. The
other controls retain phases invisible modulo ambient p and handle
exponent128 without enumeration.

Final verification:642 tests passed across15 connected files in9.80s,
using /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider -W error:

- tests/test_lie_torsion_reduction.py
- tests/test_mixed_abelian_readout.py
- tests/test_regular_subset_sum.py
- tests/test_small_prime_module.py
- tests/test_cli_parser_integrity.py
- tests/test_prime_power_rees_descent.py
- tests/test_pilot_submodule.py
- tests/test_pilot_module_descent.py
- tests/test_pilot_receiver_policy.py
- tests/test_unit_power_kernel.py
- tests/test_unit_power_module.py
- tests/test_span_regular_sde.py
- tests/test_random_regular_sde.py
- tests/test_random_column_power_sde.py
- tests/test_random_column_rees_budget.py

Six changed Python files passed py_compile; all12 site JavaScript files
passed node --check; qsearch.py validate returned valid=true, issues=[].
The rank-reduction artifact binds nine source/proof/test files by SHA-256;
the older subset artifact was regenerated after its priority note changed.
No full repository suite, Lean rebuild or hardware experiment was run.
No candidates/proof statuses were promoted, and no commits, pushes,
installations, outreach or UI changes were made.

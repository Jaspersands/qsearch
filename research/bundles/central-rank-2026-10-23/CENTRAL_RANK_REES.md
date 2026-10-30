# Hidden-Codimension Rank Compression In The Rees Receiver

2026-10-23. Proposed improvement to the existing explicit-Lie parameter bound.
Local proof and exact arithmetic controls; independent review pending. Not
an implemented quantum receiver, complete general-degree scalar solver,
novelty certification, natural hard application, or admitted quantum speedup.

## Decision And What Changes

The existing bounded-codimension reduction leaves an explicit terminal Lie
algebra of dimension at most k(k+1)/2 and class at most 2k-1. Its scalar-line
Rees cost budgets every central coordinate, giving the conservative bound
`2^O(k^3 log(k+2))`. That is unnecessary: the observed central characters
occupy a subspace of dimension at most k-1. Their span can be compressed
without learning or guessing the hidden subgroup.

Processing a WHOLE grade using these compressed public equations gives the
conditional explicit-input bound

    2^O(k^2 log(k+2)) * poly(input size, log p, log(1/epsilon)).

This is a change to the algorithmic resource argument, not merely a more
favorable fit of existing finite results. It still relies on the proposed
Rees receiver and the bounded-codimension reduction being correct. The
all-prime, opaque-group normalizer extension in the separate local bundle
has not been audited to this uniform parameter bound.

The initial proof review found no new contradiction in the Rees cover,
conditional central-state formula, or published SDE scope. That observation
is not independent validation. Rather than repeat the same finite HSP
examples, this pass changes the terminal cancellation schedule and tests
the specific new rank/composition obligations.

## 1. Exact Input And Access

Use the explicit-Lie contract of
`research/BOUNDED_CODIMENSION_HSP_REDUCTION.md`: an n-dimensional nilpotent
Lie algebra L over a caller-verified odd prime F_p, actual class c<p,
genuine public structure constants, coherent ordinary HSP access hiding
H=exp(h), and codim_L h<=k. Or use the independently justified copy-source
interface, with its public operations and joint-source promises intact.

Here k is a public upper bound, not necessarily the exact codimension.
All source calls, unused targets, labels, arithmetic and gate errors count.
No hidden intersections, h-basis, annihilator basis, source inverse, or
oracle table is supplied to the new arithmetic routine.

First perform the existing abelian-ideal/normalizer reduction. Its complete
intersection-learning obligation is UNCHANGED. Only the terminal Rees part
is replaced. The actual terminal class, not its loose upper bound, must
remain below p. k=0 and an abelian terminal case need no nonabelian descent.

## 2. A Stronger Bound Than codimension k

Let k_0=codim_L h. For every d>=2 put

    r_d = dim gamma_d(L),
    e_d = dim gamma_d(L) - dim(h intersect gamma_d(L)).

If h=L, all e_d=0. Otherwise

    e_d <= k_0-1 <= k-1.

Proof: a proper subalgebra h of a nilpotent L cannot satisfy
`h+[L,L]=L`. If it did, induction gives L=h+gamma_j(L) for every j:
from L=h+gamma_j, expand [L,L] to obtain
`[L,L] subset h+gamma_(j+1)`, since [h,h] subset h. Nilpotence eventually
gives L=h, a contradiction. Therefore L/(h+[L,L]) has dimension at least
one. Since gamma_d subset [L,L],

    e_d = dim((h+gamma_d)/h)
        <= dim((h+[L,L])/h)
        = k_0 - dim(L/(h+[L,L])) <= k_0-1.

This uses subalgebra closure and nilpotence, not a characteristic-zero
argument. It is the elementary Frattini/generating-subalgebra fact, not
claimed as new group theory. For a codimension-one subgroup it correctly
forces all higher central layers into h.

## 3. Which Rank Is Actually Available To The Algorithm?

In the positive Rees cover, after quotienting grades above d,

    Z_d = t^d gamma_d(L),
    K_d = Z_d intersect H_tilde = t^d(h intersect gamma_d(L)).

The existing full central measurement has positive outcomes exactly in
K_d-perp; its allowed character distribution is uniform there. Hence ANY
matrix whose columns are observed labels lambda_i in F_p^(r_d) has rank
at most e_d, and therefore at most

    kappa_d = min(r_d, max(0,k-1)).

Uniformity is not needed for this rank implication. Independence is still
needed later for the product-state central-descent identity.

Compute an ordinary F_p row basis C of the observed equation matrix Lambda.
This is public Gaussian elimination. For EVERY coefficient vector w,

    Lambda w=0  iff  C w=0.

No knowledge of K_d is required. An observed span smaller than K_d-perp is
harmless: we need to cancel these particular measured labels, not learn the
entire annihilator. This sharply differs from the outer normalizer reduction,
where an incomplete learned intersection can discard genuine hidden elements.
Do not transfer this argument to that outer learner.

The bank is sized using public kappa_d BEFORE looking at labels. A favorable
empirical rank never refunds copies already acquired. If rank exceeds the
public cap, abort on that history; do not enlarge a promised-complexity bank
without accounting for it. Such an abort is impossible on the exact promised
source, but can expose a bad promise or implementation error.

## 4. Uniform Cancellation On The Compressed Equations

Let delta_d=gcd(d,p-1). Use bank arity

    A(delta,kappa) = kappa+1             if delta=1,
                     (delta+1)^kappa   otherwise.

For an observed rank r<=kappa, a prefix of A(delta,r) columns suffices.
The other columns receive zero scales and are CONSUMED/DISCARDED. Prefix
equations can have still smaller rank; no spanning premise is needed.

At delta=1, find a nonzero kernel vector by linear algebra. Otherwise use
the standard recursive reduction of r diagonal equations to scalar ones:
partition (delta+1)^r coordinates into delta+1 equal disjoint blocks; solve
the first r-1 equations in each; the last equation becomes one scalar
diagonal equation on their delta+1 multipliers. A nonzero scalar solution
and disjoint nonzero child solutions give a nonzero full witness. There
are at most `((delta+1)^r-1)/delta` scalar calls.

The required scalar solver on delta+1 inputs has deterministic time
polynomial in delta and log p, as quoted in
[Ivanyos--Santha, Fact 2](https://arxiv.org/html/1503.09016). The recursion
immediately after that fact is also prior art. We do not extrapolate their
fixed-degree multi-equation theorem into a uniform-in-degree claim.

To recover degree-d scales, choose u with d*u=delta modulo p-1; set
s_i=x_i^u for NONZERO x_i, and s_i=0 for x_i=0. When the reduced modulus
is one, u=0 is legal only on nonzero entries. Then

    sum_i lambda_i s_i^d = sum_i lambda_i x_i^delta = 0,

with at least one active scale. Check this exact equation on ALL ORIGINAL
rows, not only on the compressed matrix. `central_rank.py` implements this
composer and verification. Its scalar callback is an explicit dependency;
passing a function does not certify that function's complexity.

## 5. Why The Same Quantum Descent Still Applies

The change is only how a verified scale witness is found. The receiver still
measures the entire central layer, retains each conditioned source on the
full group register, and uses controlled right translations through nonzero
graded dilations. For every positive-mass label tuple, the existing trace
identity gives zero correlation outside HZ_d, and inside HZ_d gives

    product_i chi_(lambda_i)(s_i^d z)
       = chi_(sum_i s_i^d lambda_i)(z) = 1.

Therefore the retained quotient source is exactly rho_(HZ_d/Z_d), regardless
of the tuple's observed rank or the scalar solver's choice of a valid witness.
An active scale exists, so support is not accidentally enlarged to the whole
group. Rank-zero tuples are legitimate: a unit witness works and the other
already acquired sources remain paid. This argument does not remeasure a
source, replace it by an expected answer, or clone a selected branch.

Fresh disjoint banks at every node preserve the original induction. Nothing
here repairs a correlated bank with merely correct marginals, a wrong action
orientation, uncleaned workspace, a non-Lie input, or an invalid quotient.

## 6. New Parameter Bound And Complete Counts

For a terminal class c_*<=2k-1, the fresh lifted-source multiplier is

    P_rank = product_(d=2..c_*) A(delta_d,kappa_d)
           <= product_(d=2..c_*) (d+1)^(k-1)
           <= (2k)^[(2k-2)(k-1)]
            = (2k)^[2(k-1)^2].

The earlier scalar-line bound was
`P_old=product_d (delta_d+1)^r_d`; the old degree-only envelope was
`(2k)^[(2k-2)k(k+1)/2]`. These remain valid upper bounds, not incorrect past
results. Taking the better existing route when useful is allowed, but no
generic general-degree implementation is being asserted.

For M terminal Fourier samples, count backward from degree one. Initialize
demand=M. At d=2,...,c_*, add demand to the central-node count, then multiply
demand by A(delta_d,kappa_d). The final demand is L=M P_rank lifted leaves.
Original source calls are c_* L. Complete instruments include L lifted
preparations, every central merge, and M final readouts. Each central merge
includes ALL its character measurements and their records. All-history caps
and first-error bounds from the prior proof remain mandatory.

Uniform public BCH and cover arithmetic have polynomial cost in the explicit
dimensions, c_* and log p. The scalar recursion is polynomial in its bank
size and degree with a uniform exponent, using the cited scalar theorem.
Logarithmic precision/amplification overhead is charged across the full tree.
Together with at most n outer abelian-intersection calls, this yields the
proposed `2^O(k^2 log(k+2))*poly(input,log(1/epsilon))` bound. It does not
upgrade an unreviewed whole algorithm to a proved theorem.

## 7. Adversarial Tests And Scope

- Exhaustively enumerate all 19 Lie subalgebras of the three-dimensional
  Heisenberg algebra over F3. Check the stronger k-1 bound and the actual
  central annihilator ranks, including full and trivial subalgebras.
- Test the original-equation witness under nonbijective square, cube,
  fourth- and sixth-power maps, and coprime-power lifting. Verify every
  witness, unused index, recursive scalar call count and row-kernel equality.
- A 127-bit prime quadratic control uses capped modular square-root arithmetic,
  not a field table. The general scalar solver is NOT implemented. Tiny
  exhaustive scalar backends are explicitly test-only and reject large primes.
- An empirical rank-one packet under a rank-two cap still pays its entire
  bank. Rank-zero packets cannot call the scalar solver. Wrong rank promises,
  missing bank inputs, invalid scalar outputs and backend failures fail closed.
- A codimension-two subalgebra in filiform algebras excludes the final central
  line at arbitrarily high class. Thus small k does NOT by itself allow us to
  stop after k grades. The preceding abelian-ideal reduction remains essential
  to the displayed FPT bound; applying it directly to unreduced growing class
  would be an error.
- The free class-three rank-two algebra has lower-central dimensions 5,3,2.
  For h=<X,U>, actual deficits are 2,1. At p7 and public k3, the conservative
  bank multiplier changes from 432 to 144. This is an arithmetic/source-count
  control, not a hard problem or evidence of a speedup.
- One initially chosen upper-envelope test profile at k2 included a zero
  lower-central layer. The validator rejected it. The fixture was corrected
  to respect actual positive lower-central ranks; no group with that malformed
  profile is claimed to exist.

## 8. Classical Comparison And Research Value

The matched birthday-collision upper bound from the existing audit remains
`p^(k/2)*poly(input)` with paid storage and independent repetitions. The new
quantum parameter envelope permits the sufficient regime
`k^2 log(k+2)=O(log input_size)` rather than the old cubic condition.
This is a comparison of algorithmic upper bounds, not a classical lower bound.
Padding, small p, numerical labels or known explicit actions may eliminate any
interesting advantage. The existing semantic polynomial-family attacks remain.

What this pass establishes locally is a sharper resource argument and a
checked composer for its public arithmetic. What it does NOT establish is
an efficient general physical implementation, correctness of every imported
outer theorem, a novel asymptotic separation for a natural problem, or a
Shor-level discovery. A published scalar routine and an independent review
of the whole proposed HSP theorem are still needed for stronger claims.

## 9. Migration-Safe Handoff

Verification: 32 dedicated tests PASS in 0.05 seconds. The combined isolated
normalizer, quotient, inverse-trace residual, spectral-source and central-rank
suite has 172 tests PASS in 15.63 seconds. All three new Python files pass
py_compile, receipt source hashes match, and the whitespace check is clean.
The live replay verifies all original moments for three packets, including a
127-bit prime and nonbijective fourth powers. These are arithmetic checks,
not a quantum-source run. No full-repository validation was attempted while
the migration worker remained live.

The replay's formal upper-envelope profiles at p127 have old/new multiplier
ceil-log2 values (17,12), (153,66), (792,193), (2981,458) for k=3,5,8,12.
Those profiles are NOT claimed to occur in a valid terminal Lie family and
are not empirical scaling results. They only make the two formulas auditable.

Reproduce from this standalone folder:

```
PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q test_central_rank.py
PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python -m py_compile central_rank.py test_central_rank.py replay.py
PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python replay.py --output central_rank_receipt.json
```

This bundle is outside both the actively copied Desktop repository and its
staging directory. Do not integrate until migration is verified complete.
Gemini can then move the module/tests into the appropriate theorem/control
locations, add this proposed alternative to the bounded-codimension note,
and run the connected Rees/normalizer suites plus repository validation.
Do not overwrite the old route or central-registry status flags. No qsearch/UI
expansion, commit, push, source hydration, or new search campaign is requested.

Next main-model work should independently check this rank argument together
with the whole receiver, or supply a meaningful input family. Implementing
an entire general SDE backend is a mechanical dependency, not evidence for
the missing natural application.

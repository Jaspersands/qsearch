# Folded Balanced Filter: A Different Explicit Relation

2026-10-22. Local constructive proof and exact regression controls;
INDEPENDENT MATHEMATICAL REVIEW PENDING. No novelty, classical hardness,
practical quantum execution, or quantum speedup is established.

## Research Decision

The paid full-list projection permits a larger decoder rate in this analysis, not
just a new decoder benchmark. For a DIFFERENT block-balanced inverse-trace
relation, the argument below reaches every fixed decoder rate R<1/2, whereas
the ordinary-RS Johnson route required R<1/4. This does not improve the old
scalar-input problem: the local constraints and coordinate grouping change.

The projection primitive is PRIOR ART, not new here: Jo arXiv2607.16541v2,
Theorem5.2/Remark5.3. See EXACT_PREDICATE_CHANNEL.md for that correction,
the exact uniform-output law and fixed-syndrome extension. The folded
predicate/count specialization remains review-pending, not certified novelty.
NATIVE_LATENT_SAMPLER.md gives a constructive moderate-temperature classical
competitor and the precise rare-native-event failure of its TV guarantee.

There is already a folded decoder and prime-character source in this repo;
see FOLDED_NORM_SOURCE_DECISION.md. Do not duplicate that infrastructure.
Its randomized pruning is not a complete deterministic list on every input.
This note supplies the needed completeness argument, the block-source norm
bound, a sharper literature-linked list cap, and a classical counterexample.
The standalone module is a proof certificate, NOT a replacement decoder.

## Exact Input And Output

Public input: q=2^n, a verified representation of E=F_(q^s), its embedded
F_q, an F_q basis B=(b_0,...,b_(s-1)), N, K<sN, gamma in F_q with at least
sN distinct consecutive powers, and arbitrary target bits t_i. Field/basis
validation and all conversions are charged polynomial-bit computations.

Find x_(i,j) in F_q satisfying, for 0<=k<K,

    sum_(i,j) gamma^((si+j)k) x_(i,j) = 0,
    X_i = sum_j b_j x_(i,j),
    Tr_(E/F2)(inv0(X_i)) = t_i, for every i.

Zero inversion is zero. There are N Boolean predicates, NOT sN independent
scalar predicates. No membership oracle, hidden shift, secret field advice,
or arbitrary-amplitude access is supplied. The scalar parity rank is K and
the decoder rate is R=K/(sN), not K/N. The native solution space before the
predicates has n(sN-K) binary dimensions.

Compute the trace-dual basis B* by inverting the s-by-s relative-trace Gram
matrix. Encode degree<K polynomials f over F_q as

    d_i = sum_j b*_j f(gamma^(si+j)).

This additive code D has q^K words and is generally NOT E-linear. Under the
pairing Tr_(E/F2)(sum_i d_i X_i), its annihilator is exactly the native parity
space above. F_q-linearity makes absolute-trace annihilation equivalent to
each full F_q parity equation; one trace equation per parity row would not
suffice. Using B instead of B* silently changes the problem.

## Source And Norm Proof

Each local accepted set has size |E|/2. Its normalized root state is prepared
by a uniform affine absolute-trace hyperplane, followed by reversible inv0.
This needs binary linear algebra, Hadamards and field arithmetic, not a table.
Fourier transformation yields a real signed source a_i with a_i(0)=1/sqrt(2).
Grouping s old scalar sources instead would give zero probability 2^-s.

For nonzero d, balance gives the exact cancellation

    sum_(u != 0,d) a_i(u) a_i(u+d) = 0.

The inverse character-sum bound gives beta=(1+2*ceil(sqrt(|E|)))/|E| as
an upper bound on the absolute full translation correlation. Thus the
existing support-mask proof applies to this additive code without E-linearity:
for every support-dependent mask of magnitude at most one, its coalesced
squared norm differs from its ordinary squared norm by at most

    eta = sum_(d in D, d != 0) beta^block_weight(d).

Fixing t whole zero blocks imposes st DISTINCT RS roots. Exactly
q^max(K-st,0)-1 nonzero messages survive. Expanding the weight product gives

    eta = sum_(0 <= t <= floor((K-1)/s)) binom(N,t)
              (1-beta)^t beta^(N-t) (q^(K-st)-1)
        <= q^K (beta+(1-beta)/q^s)^N.

The exact expression holds for any beta in [0,1]. Unlike treating D as an
E-linear code of rounded dimension, it handles K not divisible by s. For
fixed R<1/2 and increasing n, its envelope is exponentially small in nsN.
The module uses the looser but outward-safe exponent

    eta <= 2^[nK + N*(3-floor(ns/2))].

When this is tiny, the recorded rational upper bound is rounded UP to 2^-256,
not zero. No asymptotic claim is made when the exponent is nonnegative.

## Complete List, Not A Sampled Affine Space

The known [Guruswami--Wang construction](https://eccc.weizmann.ac.il/report/2012/073/)
uses interpolation order r<=s, W=s-r+1, and D0=floor((NW-K+1)/(r+1)).
Interpolate Q=A0+sum_(j=1)^r Aj Yj, with degrees D0+K-1 and D0 respectively.
If a=N-w whole blocks agree and aW>D0+K-1, substitution of f,gamma-shifted f
gives the zero polynomial. Solve ALL coefficient equations, not only a
length-K prefix. Removing common X content leaves a nonzero leading relation
sum_j Aj(0)T^(j-1), with at most r-1 exceptional values gamma^ell. Hence the
affine solution space has dimension d<=r-1. An inconsistent system means
an empty list. Order at least sN suffices for this root-count argument.

For completeness, derandomize the existing
[received-block pruning argument](https://eccc.weizmann.ac.il/report/2018/091/):
enumerate every sequence of r-1 block indices. Intersect the affine space
with the received values at each chosen block. Reject inconsistent branches;
freeze a dimension-zero branch and verify its full distance. Deduplicate
and sort the valid messages. No F_q^d enumeration occurs.

A nonzero degree<K direction vanishes on at most Z=floor((K-1)/s) blocks.
For each actual close message, at least a-Z of its agreeing blocks strictly
reduce any surviving positive-dimensional affine space. A uniform sequence
therefore recovers that message with probability at least p^(r-1), where
p=(a-Z)/N>0. Distinct outputs have disjoint successful sequences. Consequently

    complete list size <= floor(p^(-(r-1))).

This is constant for fixed agreement/rate gaps. Enumerating N^(r-1) sequences
is polynomial in N and log(q) for fixed r, but potentially enormous. It is
a sufficiency argument for a known decoder component, not a new decoder.
No random-seed advice or typical-list-completeness premise is used.
Cap this bound by q^K before padding; a projection list cannot have more
distinct messages than the entire message space.

### Sharper Literature Cap

[Chen--Zhang](https://arxiv.org/html/2408.15925v3) proves list size at most r
at radius r/(r+1)*(1-sR/(s-r+1)) for the stated folded codes. We require a
STRICT inequality for the integer radius. We conservatively require a
verified primitive gamma when invoking this cap, matching their definition;
we do not silently weaken that assumption using small controls. Without it,
use the larger independent pruning cap above.

[Ashvinkumar--Habib--Srivastava](https://arxiv.org/html/2508.12548v2),
Theorem3.5, also gives a deterministic pruning procedure with polynomial
log(q) dependence and a large gap-dependent constant. This is a known
alternative to exhaustive block sequences, not implemented here. Their
randomized decoder is not substituted for an exact coherent payload.

Field generation must not hide factoring q-1. For n=17,31,61 the module
verifies q-1 prime by Lucas--Lehmer. Any root of a public degree-n irreducible
binary polynomial is then primitive. For general inputs require a verified
primitivity certificate, or use the long-order fallback cap. A deterministic
long-order search can test O((sN)^2) labels once q exceeds that bound: elements
of order below sN are covered by the roots of X^j-1, j<sN. This is polynomial
in sN,n and needs no factorization. Field irreducibility and tower/basis
validity are still required; the budgets do not instantiate a large tower.

## Paid Receiver And Concrete Rate

Use the exact full-list projection from BALANCED_FILTER_CHANNEL_AUDIT.md.
Choose ONE public power of two P covering the complete list cap. The accepted
state is A(1_(weight<=w) a)/sqrt(P); reject every other projection outcome.
Uniform code preparation costs nK Hadamards plus encoding; source registers
contain nsN bits. Run the deterministic decoder reversibly with bounded
workspace, canonical lists and full cleanup. No retained message, support,
weight or list record is allowed on the successful branch.

Let delta=Pr[Bin(N,1/2)>w]. The previously derived triangle bound gives

    Pr[full native witness per attempt] >= (1-2delta-3eta)/(2P).

This remains valid, but the later EXACT_PREDICATE_CHANNEL.md supplies the
stronger exact identity lambda_target*(1-delta)^2/P. The current artifact uses

    native success >= max(0,1-eta)*(1-delta)^2/P,
    invalid projected mass <= (1+eta)*delta*(1-delta)/P.

The ideal output conditional on native verification is EXACTLY uniform over
the target fiber. This applies to the ADDITIVE folded code with its correct
trace-dual basis; E-linearity is not required. Always run the native verifier.
Fresh attempts include all failures. Approximation errors
must be bounded in total variation relative to this per-attempt lower bound;
poly-bit precision suffices for a fixed positive gap and polynomial P.

Take s=67, r=8, N=n^2, K=floor(3sN/8), w=floor(.51N). The limiting permitted
error radius is 31/60>.51; R tends to3/8, beyond the old1/4 ceiling. The sharp
cap gives P=8. Exact certificates at n17/31/61 respectively yield:

| n | Success lower bound, approximate | eta upper exponent | Raw value bits |
| --- | --- | --- | --- |
| 17 | .0508646 | -40137 | 329171 |
| 31 | .0685570 | -246140 | 1995997 |
| 61 | .0984480 | -1887950 | 15207727 |

All three success floors exceed1/20. These are ideal arithmetic bounds,
NOT native quantum runs, compiled gate counts or practical devices. The
fallback remains polynomial but has a much worse projection constant.

## Classical Counterattack And Revised Choice

Even folding has a concrete weakness. Choose a native basis whose first s/2
vectors span F_(q^(s/2)). Every element of this subfield has absolute inverse
trace zero in E, including zero. Fix one accepted value on each target-one
block and leave s/2 scalar coordinates free on every target-zero block.
Those free columns form an ordinary Vandermonde submatrix, so if

    (number of zero targets)*s/2 >= K,

linear algebra completes the SAME native parity equations with all predicates
satisfied. This is a polynomial classical algorithm for that input subclass.
Accepted one-values are sampled by affine-trace preparation and inversion;
no exponential accepted-set search is needed by the general attack. The
bounded reference enumerates a field only to supply an exact witness.

At R=3/8 it covers target-one density at most1/4 in the aligned basis. For
arbitrary public bases, the corresponding restricted matrix must actually
be rank-checked; counting variables alone is not a guarantee. This is not
a solver for all targets. A q8,s2,N3,K2 control solves all three placements
of one target-one block and rechecks the ORIGINAL parity and predicates.

This motivates replacing the previous even s64 sketch by odd s67 and odd
n. It removes the automatic quadratic-subfield zero-flat, NOT general
subfield/rational/affine-flat attacks. Target-all-zero remains trivial.
Ordinary inverse-trace affine-flat completion, coupled low-degree solving,
received-value interpolation and Gibbs first-hitting attacks remain live.
The scalar small-block mixing obstruction does not transfer automatically.

Uniform rejection on the native parity space succeeds with probability
2^-N*(1+/-eta), but this is only ONE baseline. Classical local source sampling
and signed-amplitude queries are not assumed hard. No lower bound against
the strongest classical algorithm is known; no standard cryptographic or
natural search problem is reduced to this relation.

### Stronger Classical Baseline: Accepted-Set Completion

Uniform rejection is not the right comparison even among simple algorithms.
Let m=ceil(K/s). Make the first K scalar coordinates pivots. Every K-column
Vandermonde submatrix is invertible. Sample an accepted X_i independently
on each of the last N-m WHOLE blocks, using the trace hyperplane and inv0.
Sample the other nonpivot coordinates in the partial pivot block uniformly.
Solve the parity equations for the K pivot coordinates, then check the first
m block predicates. Repeat on failure. This is a classical algorithm on the
SAME inputs with polynomial work per attempt.

Projection of the native linear space onto the nonsolved scalar coordinates
is a bijection. Hence this samples uniformly from the native space conditioned
on the last N-m predicates. Those full-block values are independent uniform
before conditioning, so that event has probability exactly2^-(N-m).
The full solution count from the Fourier norm gives

    Pr[classical completion succeeds] = 2^-m ||Aa||^2,
    (1-eta)2^-m <= Pr[success] <= (1+eta)2^-m.

Thus expected classical attempts are at most2^m/(1-eta) when eta<1. This is
about2^(3N/8), not2^N, for the revised family. All remaining predicates and
every failed attempt are charged. The finite reference directly counts the
conditioned codewords and valid answers, independently checking this equality
for all10 targets, including K not divisible by s. It does NOT run an
exponentially long native rejection process. This known-style completion
baseline still does not rule out polynomial classical algorithms.

## Falsifiers, Validation, And Next Decision

Stop this construction if the signed support-mask lemma fails for additive
block codes, field duality changes the input, the list is incomplete, decoder
cost is polynomial in q rather than log(q), or the quantum probability ledger
omits the1/P factor. A complete classical solver on the same inputs defeats
a speedup claim even if every quantum step is correct.

The independent finite reference checks all targets for three bounded field/
code configurations, the native annihilator, the exact block enumerator,
projection probability and an explicitly WRONG-basis countercontrol. These
are exponential proof fixtures, not candidate circuits or scalable decoding.
An ambiguous binary-field pruning control enumerates all27 block sequences,
charges rank failures, and independently compares the output with all512
messages. Enumeration is outside the pruner and is not an efficient decoder.
The suite also checks strict-radius boundary failures, Lucas--Lehmer controls,
native budgets and the mixed-target classical witnesses.

Run with PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache:

    python -m theorems.folded_balanced_filter --write
    python -m pytest -q tests/test_folded_balanced_filter.py

The old folded decoder and shared native backend are currently iCloud
placeholders; their integration has NOT been replayed. Do not hydrate or
replace them to make this pass appear complete. No qsearch/UI/central
registry changes or quantum compiler work are justified by this result.

NEXT SCIENTIFIC PRIORITY: find a constructive classical completion for the
odd-folded arbitrary-target relation, or a meaningful reduction/application.
Do not keep increasing a rate or cataloguing nearby conditional variants.
The quantum construction is now sufficiently explicit that natural relevance
and classical difficulty, not another decoder wrapper, are the main deficits.

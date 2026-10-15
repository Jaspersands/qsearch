# Native Nonlinear Fibre Pairing: Existence, Compilation And Source Law

LOCAL DERIVATION / REVIEW PENDING. No novelty, efficient native receiver,
hardware gate export, classical hardness or Shor-level speedup is claimed.

Subsequent [disjoint-kernel work](DCP_DISJOINT_KERNEL_PAIRING.md) supplies a
polynomial coarse-only evaluator at quadratic input supply, plus actual
elementary gates and a cheaper measured controller. It does not supply the
linear-input near-unit matching sought by THIS frontier, or improve known
Gaussian/isotropic sieve asymptotics.

Run `python qsearch.py dcp-nonlinear-fiber-pairing` and
`node research/certificates/dcp_nonlinear_fiber_pairing_crosscheck.js`.
The live phase_workbench artifact binds the earlier affine receiver by SHA256.

## Research Decision

The affine receiver's selected n2,m6,q16 counterexample has useful-descent
optimum9/16, versus11/16 for arbitrary basis pairing. The new reference
actually compiles the latter pairing's reversible BASIS-WIRE maps and checks
its unknown-state instrument. It attains11/16 with all failed branches paid
and clean temporary workspace. This is an EXPONENTIAL reference program, not
an efficient quantum algorithm: its64-row table costs64 address comparisons
per coherent XOR evaluation under the declared naive implementation.

More important than this finite gain is the separation below. Native fibres
can support almost perfect descent with only linearly many supplied qubits.
The unresolved work is an efficient PROGRAM, output/source lineage and noise,
not necessarily the existence of enough pairs. Counting hardness is not a
general obstruction to such a program.

## Relation And Physical Compiler

Let A be n by m public labels modulo q=2^t, and choose1<=h<t, K=2^h. Define
F_A(x)=Ax modq for Boolean x. Native input is the flat unknown phase state

    2^(-m/2) sum_x exp(2 pi i <s,F_A(x)>/q)|x>.

A useful pair x,y satisfies F_A(x)=F_A(y) modK, but F_A(x)!=F_A(y) modq.
Its relative phase is a nonzero vector label

    lambda=(A(y-x)/K) mod(q/K).

Thus a retained pair is one unknown phase qubit at modulus q/K, not a
measurement/recovery of the secret. Zero labels never receive useful credit.

Reuse the [existing reciprocal-program construction](DCP_PAIRING_PROGRAMS.md).
A deterministic public valid-or-failure proposal F is accepted only when
F(F(x))=x and the useful relation holds. Compute two encoded proposals, toggle
the acceptance flag, and uncompute both: four XOR-F calls on EVERY attempt.
On acceptance, two more XOR-F calls order the endpoints into(min,max), retain
the orientation bit and clear the second endpoint/validity workspace. Both
orientations leave identical auxiliary registers; retaining a copied endpoint
instead would destroy the unknown phase when that register is discarded.

The module implements these gates as exact permutations on
x[m],u[m+1],v[m+1],accept,orientation. Each primitive is an XOR update or a
controlled swap, hence is a full-space permutation, including dirty workspace.
Acceptance and ordering inverses are implemented. Finite tests compare the
special scalar case with the existing compiler and test all625 partial
functions on four assignments. Original mixed-state tests check the complete
accepted isometry, every output label, Born mass and noise visibility.

Six calls do NOT mean constant cost. The reference explicitly enumerates2^m
assignments, may testO(4^m) potential edges and runs classical matching.
Lookup implementation costs2^m address comparisons per XOR-F, plus reversible
arithmetic. A future uniform bounded classical F can be reversibly compiled,
with that cost and cleanup paid. Hardware gate export is NOT implemented.
No source reset, unknown preparation inverse, same-A resupply or free oracle
is supplied. Every attempt consumes m original unknown qubits.

## All Fibres Become Even At A Sharp Threshold

This is classical characteristic-two group algebra, not a new algorithm.
For ANY A modK consider

    product_i (1+X^(A_i)) in F_2[(Z_K)^n].

The coefficient of X^b is the parity of the number of Boolean assignments
with Ax=b modK. Put Y_j=X_j+1. Since K is a power of two, the algebra is

    F_2[Y_1,...,Y_n]/(Y_1^K,...,Y_n^K).

Every factor has zero constant term and belongs to the augmentation ideal.
A product of m factors has degree at least m if nonzero, but every surviving
monomial has degree at most n(K-1). Hence if m>n(K-1), ALL coarse fibres
have even cardinality, for EVERY A. No rank/IID/secret premise is needed.

The threshold is sharp: take K-1 copies of each standard basis column.
The product is product_j Y_j^(K-1); its X expansion has every coefficient
odd. For K4 this is exactly m3n versus m3n+1. This does not make the useful
pairing automatic: if these full labels have no higher bits, equal coarse
sums can already be identical full sums. All-zero A is another explicit
even-fibre but useless-output control.

The finite producer multiplies sparse Y polynomials and compares them with
original integer subset counts. JS independently transforms the X-parity
polynomial back to Y. Symbolic large-n threshold rows enumerate no states.

## Coarse-Only Selection Gives A Fresh-Label Law

Fix B=A modK, write A=B+KZ with Z IID uniform modulo R=q/K, and fix a
reciprocal pairing program using ONLY B and the Boolean assignment. The
program may be computationally expensive; independence from Z is essential.
For any selected distinct pair x,y,

    lambda=B(y-x)/K+Z(y-x) modR

is uniform in(Z_R)^n: at least one coordinate of y-x is+/-1, a unit. This
holds conditional on B and the particular pair, not conditional on full A.
Born mass of each pair is2/2^m independently of the secret and higher labels.

Therefore, before a zero-label filter, coarse admission emits uniform labels.
The charged zero rejection has probability R^-n; afterward labels are uniform
NONZERO. With pure inputs, injecting a known label-zero|+> qubit with public
probability R^-n restores the full uniform source. This simple conditional
wrapper needs no unknown-state preparation inverse. The live workflow proves
the law but does not execute a hardware injection channel.

The effective native interface must DISCARD the original higher-label
transcript after computing the new label. Keeping full A and asserting that
lambda is uniform conditional on it would be false. Coarse B/pair records
may remain: the higher-label uniformity holds conditional on those records.
Fresh independent batches are required for IID outputs across attempts.
Full-label-optimized matchers DO NOT inherit this theorem.

For dephased inputs, pairing width changes visibility. Pure zero injection
does not automatically reproduce that same noise at label0. A separate noisy
source claim is required; the proof does not silently grant it.
The subsequent [noise-matched channel](DCP_NOISE_MATCHED_SOURCE.md) supplies
that repair under an independent balanced-product promise: retain visibility
and inject a matching dephased zero state. It still does not establish the
actual natural source's joint noise law.

## Native Mean Coverage: Stronger Than Pair Existence Alone

A maximal coarse-only pairing leaves exactly one assignment per odd coarse
fibre. Let O=min(1,2^(hn-m)) be a universal unmatched FRACTION bound, or O=0
when the augmentation theorem forces all fibres even. Averaging over IID
higher labels gives

    E_A[optimal useful coverage] >= (1-O)*(1-2^(-(t-h)n)).

When m>n(K-1), ANY perfect coarse-only pairing has EXACT native mean useful
coverage1-2^(-(t-h)n), even if it is computationally intractable to find.
At n64,t64,h2,m193 this equals1-2^-3968. It is a SOURCE-MEAN theorem, not
a guarantee for each full A, and it does not construct the program.

An independent weaker check uses full-sum collisions: for x!=y, A(x-y)=0
modq has probability q^-n because one signed coefficient is a unit. Expected
fraction of endpoints with a full collision is at most(2^m-1)/q^n. In each
coarse fibre, the useful graph is complete multipartite by full value; its
unmatched count is max(N mod2,2L-N), where L is its largest full-value part.
Summing bounds gives1-O-(2^m-1)/q^n. Both derivations are recorded and checked;
the coarse-only uniformity bound dominates this deletion bound.

The report separates fixed-t slices from JOINTLY growing t=n. Constant-class
oracle HSP is already known territory; none of these rows is a new algorithm
or an executed large-instance experiment. See the previous access audit and
[Imran--Ivanyos](https://arxiv.org/html/2304.08376v1) for known nilpotent context.

## Try To Kill It With Width And Noise

For any x and nonzero width-w support S, the signed coarse sum is uniform in
(Z_K)^n under native IID labels. Union over supports, even for an unlimited
A/x-adaptive selector, gives

    E p_w <= binom(m,w)/2^(hn),  sum_w E p_w<=1.

With independent balanced ORIGINAL-register visibility v, a pair's coherence
is v^w. Reuse the existing EXACT fractional-knapsack relaxation from
core/dcp_pairing_programs.py with target bits hn. Fill shortest widths first.
It is a bound, not an attainable pairing or a general quantum-receiver no-go.

For m3n,h2 and v1/4, the still looser full-capacity sum is less than

    ((1+v)^3/4)^n = (125/256)^n <2^-n.

Thus finite quarter-visibility improvements cannot scale within this pairing
architecture. More generally put r=floor(m/32). The short contribution is at
most sum_(w<=r)binom(m,w)/2^(2n), and the tail is at most v^(r+1).
Taking z=1/31 in the binomial generating function bounds the short count by
31^(m/32)*(32/31)^m<2^(m/2); the fixed integer inequality
32^32<2^16*31^31 certifies the last step. For m3n the short fraction is
<2^(-n/2). Every fixed v<1 then gives exponential suppression as n grows.

Conversely, for the joint growing schedule t=n,v=1-1/n,m3n, the constructive
EXISTENCE bound for maximum pairing's retained visibility is

    v^m*(1-O)*(1-2^(-(t-h)n)),

which exceeds1/25 on the recorded n32..512 rows. This is not an implemented
efficient program. Inter-level composition can worsen visibility; output
lineage cannot be assumed native for full-label matchers. Correlated faults,
error correction, non-basis measurements and coherent multi-output receivers
are outside the independent-product width theorem.

## Counting Hardness Is Not A General Pairing Barrier

A positive exact-one constraint on three Boolean occurrences is exactly
sum x_i=1 mod4, since the sum is between0 and3. The incidence matrix with
multiplicities gives a count-preserving reduction to one prescribed coarse
fibre. The relation has three satisfying triples, so is not affine over F2.
The [Creignou--Hermann counting dichotomy](https://www.sciencedirect.com/science/article/pii/S0890540196900164)
therefore supplies the WORST-CASE counting classification. It does not prove
native average-case hardness or hardness of an arbitrary pairing routine.

The distinction has a scalable counterexample. Add enough coarse-zero columns
to force m>3n, giving a known2^padding multiplier to the original count. Give
one such column full label4e_1 modulo8. Flipping that public bit is a perfect
USEFUL pairing for every assignment, regardless of the original constraint
system's solution count. Its XOR-F circuit uses m CNOTs and2 X gates, no table.
The encoder and basis-wire compiler handle a193-input control without any
truth table. Counting can remain hard while this pairing is trivial.

These are reduction/falsifier controls, not proposed oracle problems or
candidate quantum algorithms. The pairing does NOT solve the counting
problem; it only retains one already accessible phase component. Do not
require global canonical ranking of every future matcher, and do not infer
all pairing is impossible from the difficulty of that stronger task.

## What Must Be Built Next

1. A uniform polynomial reversible coarse-only involution/partial proposal
   with native-average useful coverage, rather than its exponential table.
2. A proof of its low-bit selection lineage, cleanup and source supply costs.
   The conditional fresh-label theorem then removes an output-distribution
   obligation instead of assuming it away.
3. A growing-phase-level composition that preserves noise/information and
   avoids multiplying a large source cost at every descent. Retaining packets
   or using collective operations may be essential; this is not a universal
   requirement that all algorithms reduce to pairing.
4. Actual natural-source geometry/noise promises, matched classical attacks,
   independent theorem review and a final efficient decoder.

No central candidate or broad negative theorem is promoted by these controls.

# Balanced Predicates: A Per-Instance Codeword Filter

2026-10-22. Local mathematical derivation, REVIEW PENDING. Known quantum
decoding/interference framework, not a new framework, a hardness proof, a
verified speedup, or a compiled quantum receiver. No registry admission.

Update, 2026-10-22: BINARY_GS_DECODER.md now supplies a deterministic
binary-field decoder route, complete-list executable controls and a clean
coherent-compilation argument. Randomized factorization is NOT necessary
in this characteristic-two setting. The actual reversible circuit and large
native decoder have not been executed; the whole proof remains review-pending.

## Decision And Input

The Rees receiver still lacks an established natural application outside
the existing classical filters. More arithmetic backends and low-degree
Frobenius corollaries do not fix that. This pass investigates a separate,
explicit-input route with a concrete coherent-error obligation.

Let q=2^n, with a supplied irreducible field polynomial and binary basis.
Choose N distinct public evaluation points and the ordinary [N,K] RS code
D over F_q. The native answer code is C=D^perp, of dimension N-K. The
input also contains an arbitrary vector b in F_2^N. Find x satisfying

    H x = 0,                 H[j,i] = alpha_i^j, 0 <= j < K,
    Tr(inv0(x_i)) = b_i,      inv0(0)=0.

There is no hidden oracle, truth table, secret decoder, sampled polynomial
ensemble or supplied witness. Inversion and absolute trace are explicit
polynomial-time finite-field computations. The all-zero target has the
obvious all-zero answer and is NOT a hardness instance.

The proposed result below is an efficient quantum construction for every
target in a large-field, low-decoder-rate regime. Whether the SAME task
has an efficient classical algorithm remains open in this audit. Do not
market an explicitly manufactured task as a cryptanalytic application.

## Prior Art And The New Obligation

[Briaud et al., Sections 3-4](https://arxiv.org/html/2509.07276v1)
use the Regev/Yamakawa-Zhandry framework to solve code-constrained local
polynomial equations. Their specified input distribution and Fourier-error
analysis are substantive. Their quadratic case has a classical attack;
their cubic hardness is conjectural. The repository already audits that
case in CUBIC_RS_AFFINE_FLATS.md and CUBIC_DEGREE_REDUCTION.md.

Here the question is different: can a deterministic per-instance Fourier
bound replace an ensemble premise, INCLUDING coherent truncation error?
Small ordinary decoding-failure probability alone does not answer this.
PRIME_CHARACTER_CAPACITY_SOURCE.md already shows why coalescing amplitudes
can amplify a small failed-source mass. We explicitly pay that effect.
No novelty claim follows from not finding this exact specialization in
the corpus or the targeted literature searches.

## 1. Exact Balanced-Source Identity

For any balanced Boolean predicate f_i:F_q->F_2, let
S_i={x:f_i(x)=b_i}, |S_i|=q/2. Use the real additive Fourier transform
with character (-1)^Tr(ux). Put

    B_i(u) = sum_(x in S_i) (-1)^Tr(ux),
    a_i(u) = sqrt(2)/q * B_i(u).

Thus a_i is the NORMALIZED Fourier transform of the uniform root state,
a_i(0)=1/sqrt(2), and sum_u a_i(u)^2=1. Indicator idempotency gives

    sum_u B_i(u) B_i(u+d) = q B_i(d).

For d!=0, the terms u=0,d already sum to q B_i(d). Consequently

    sum_(u != 0,d) a_i(u) a_i(u+d) = 0.             (1)

This exact signed cancellation is the useful observation. It fails for
unbalanced sets or when the Fourier amplitudes are replaced by their
absolute values. A random nonzero-label distribution is NOT assumed.

Let beta bound |2 B_i(d)/q| for every i and every d!=0. Define the
normalized product source a(e)=prod_i a_i(e_i), and the code-coalescing map

    A = |D|^(-1/2) sum_(d in D) T_d.

This map is not a free physical operation; A^*A=sum_(d in D)T_d. A decoder
will implement its injective part below.

## 2. Support-Mask Near-Isometry

Let m(e) be ANY complex mask of magnitude at most one depending ONLY on
the set {i:e_i!=0}. It may distinguish positions and need not be radial.
For minimum distance Delta of D, set

    eta = (|D|-1) beta^Delta.

Then

    abs( ||A(m a)||^2 - ||m a||^2 ) <= eta.          (2)

Proof: expand A^*A. The zero codeword gives ||m a||^2. For each nonzero
d, partition each coordinate of the remaining correlation according to
whether e_i and e_i+d_i vanish. If d_i!=0, the both-zero case is empty;
the both-nonzero sum vanishes by (1). The two remaining cases each have
absolute local contribution |a_i(0)a_i(d_i)|. Their total is at most
beta. If d_i=0, the sum of absolute local contributions is one. The mask
is constant within each such zero-pattern cell, so the cancellation
remains legal and its two mask factors have magnitude at most one.
The absolute correlation is therefore at most beta^wt(d). Sum over D\0.

The dependence restriction is ESSENTIAL: a label-dependent phase mask
can remove all signs and violate (2). This is not a claim that A is an
isometry on arbitrary vectors or that all low-mass errors remain small.

For the Hamming tail wt(e)>w, independence of product-state measurement
probabilities and a_i(0)^2=1/2 give EXACT mass

    delta_tail = 2^(-N) sum_(j=w+1)^N binom(N,j).

Equation (2) bounds its squared COHERENT image norm by delta_tail+eta,
without multiplying delta_tail by q^K. This is stronger than using a
worst-case full-fiber bound on this particular structured tail.

## 3. A Paid, Finite List-Decoder Interface

Write a=N-w and assume a^2>N(K-1). A complete GS list decoder returns
all D-codewords within radius w. Its known polynomial-time construction
now has a deterministic binary-field backend and capped dense-interpolation
control in binary_gs_decoder.py; the state-map reference below still uses
exhaustive lists and is not that decoder or a compiled circuit.
[Guruswami-Sudan decoder description, Sections III-V](https://ipnpr.jpl.nasa.gov/progress_report/42-153/153F.pdf).
Finite-field factorization/randomness, runtime clocks, reversible work and
list completeness must be charged in a compiled implementation.

A direct pairwise-agreement count gives the list cap

    L = floor( N(a-K+1) / (a^2-N(K-1)) ).

Indeed choose exactly a agreements for each of ell codewords. Cauchy-
Schwarz on their N position counts and pairwise intersection <=K-1 give
ell(a^2-N(K-1)) <= N(a-K+1). This also controls amplitude coalescence
WITHIN the retained ball; it does not control the omitted tail by itself.

For K>=2 the budget also supplies an explicit GS interpolation witness:
s=floor(N(K-1)/(a^2-N(K-1)))+1 and weighted degree s*a-1. The number of
monomials X^i Y^j with i+(K-1)j<=s*a-1 exceeds N*s*(s+1)/2, the complete
multiplicity-constraint count. These integers are checked, not inferred
from an asymptotic radius. K=1 is direct repetition-code list recovery.

Suppose each nonzero error symbol has probability at most mu. A wrong
codeword differs from the correct one at all but at most K-1 positions.
To enter the radius-w list it needs at least t=a-K+1 matches at nonzero
differences. Product source probabilities and a union bound give

    delta_amb <= min(1, (q^K-1) binom(N,t) mu^t).     (3)

This bounds ambiguous input mass in the radius-w ball. It includes ALL
wrong codewords and all their possible zero positions, not just a sampled
competitor or an equal-weight collision.

Physical recipe:

1. Prepare the product of root states and Fourier transform it. Prepare
   a uniform D-codeword register by public linear algebra. Erase its
   message workspace with a public left inverse of the injective encoder.
2. Measure the error-weight predicate wt(e)<=w. Charge every rejection.
3. Reversibly add the codeword to e. Compute the COMPLETE radius-w list;
   retain only a singleton list. It then contains the original codeword.
4. Erase the original codeword register using that singleton, uncompute
   decoder workspace, and inverse Fourier transform the retained register.
5. Measure x and check BOTH Hx=0 and every original trace constraint.
   Reject and retry on failure. No output is accepted on a surrogate score.

Let U be the retained, uniquely decodable errors, B the ambiguous retained
errors and T the omitted weight tail. The unnormalized heralded output
before inverse QFT is g=A(1_U a), with

    ||g||^2 = Pr[U] >= 1-delta_tail-delta_amb.

This identity holds because U contains at most one error per D-coset.
The full vector v=Aa, which need not be normalized, Fourier-transforms
to a vector supported ONLY on native valid answers. Moreover

    ||v-g|| <= sqrt(delta_tail+eta) + sqrt(L delta_amb).

The first term is (2); the second is the retained-ball list-size bound.
Thus the probability of invalid readout AND successful herald is at most
2(delta_tail+eta+L delta_amb). A conservative per-attempt failure bound is

    3 delta_tail + (2L+1) delta_amb + 2 eta.          (4)

No renormalized rare-sector assumption or free inverse source is used.
Gate/source/decoder approximation error is ADDITIONAL to (4). A missing
list element is a decoder failure, not evidence of unique decodability.
For a randomized list backend, use a worst-input failure guarantee with
a bounded clock on every branch and charge its coherent implementation
error, not just tests on sampled classical words. Only the singleton FLAG
is measured: reading the actual codeword/list would destroy the required
superposition. The predicate, list and arithmetic workspaces are cleaned.
Likewise measure only the weight THRESHOLD, not the exact weight or error
support: retaining those records would destroy interference between weights.

## 4. Reciprocal Trace Supplies The Premises Explicitly

Inversion extended by inv0(0)=0 is a permutation. Hence Tr(inv0(x)) is
balanced. The root state is prepared by a uniform affine trace hyperplane
followed by reversible inversion: no amplitude oracle, table or rejection
sampling is needed. Public field construction and a dual-basis Fourier
transform are paid polynomial-time operations in n.

For d!=0, the Walsh coefficient is

    W(d) = 1 + sum_(x!=0) (-1)^Tr(inv(x)+d*x).

The classical Kloosterman/Weil bound gives |W(d)|<=1+2 sqrt(q).
The zero-extension convention matters; the code retains its extra 1.
See the definition and convention discussion in
[Gologlu-McGuire-Moloney, Section 1](https://citeseerx.ist.psu.edu/document?doi=9637143f00e231ae8db58b149a2b08fdba414f68&repid=rep1&type=pdf).
Use conservative bounds beta<=(1+2 ceil(sqrt(q)))/q and mu<=4/q, capped
by their trivial bounds. Targets b only change signs away from zero.

For any fixed R=K/N<1/4 choose agreement fraction A with
sqrt(R)<A<1/2. Then A>2R. At N=n^2, q=2^n and a approximately AN:
delta_tail is exp(-Omega(N)); (3) is q^(-Omega(N)); and eta is
q^(-Omega(N)), since R<1/3. The list cap is constant at a fixed margin.
This gives a proposed polynomial-time quantum solving construction for
EVERY native target, by composing known operations with the above proof.
It does NOT give a classical lower bound or a practical gate estimate.

The recorded budgets use K=floor(N/8), w=floor(3N/5), n=17,31,61.
They evaluate exact rational inequalities only. No large state, field
table, codeword enumeration or large quantum decoder is run.

The sufficient ideal-arithmetic failure bounds are respectively <=2^-10,
<=2^-30 and <=2^-111. All three use multiplicity s=4. These are NOT gate
error budgets or measured success rates. Large fractions are reported as
rigorous dyadic upper bounds with reproducible input parameters; floating
logarithms are diagnostic only.

The complete bounded reference gives much weaker finite performance:

| field | N | K | radius | herald | valid conditional on herald |
|---|---|---|---|---|---|
| F8 | 4 | 1 | 1 | 5/16 | 25/64 |
| F8 | 4 | 1 | 2 | 19/32 | 377/608 |
| F8 | 4 | 1 | 3 | 1/16 | 5/64 |
| F16 | 3 | 1 | 1 | 1/2 | 3/8 |

These exact state-map controls enumerate 4096 error words each and all
decoder codewords. They preserve all failed probability mass. They are not
the GS implementation, hardware runs, or evidence of a finite speedup.
The F16 sign-stripped countercontrol has squared norm 97/32, exceeding
the illegal label-mask extension's proposed cap 1+15/8. The F8 fixture
only saturates that cap, so it is not used as a strict counterexample.

## 5. Try To Kill The Application

**A matched classical attack is already available.** Given any public
nonzero v in C, try x=t*v. For u=1/t, its constraints are the BINARY
LINEAR equations Tr(u*inv0(v_i))=b_i. A zero v_i enforces b_i=0. Solve
by linear algebra and require u!=0; then verify the native witness.
For a fixed direction at most 2^n target strings are attainable, but this
count is NOT a lower bound on an adaptive or multi-direction attack.
Failure on one line says nothing about global solvability. All-zero
targets are easy even if the particular nonzero line has no witness.

**Other serious attacks remain open here.** Rewrite nonzero coordinates
using x_i*y_i=1, Tr(y_i)=b_i and Hx=0. Try rational interpolation and
bilinear-system algorithms, not generic brute force alone. Zero coordinates
need separate legal branches. Even extension degrees admit subfield
structures; odd prime n removes proper intermediate fields, not all
algebraic attacks. Large local zero flats or structured global restrictions
could destroy any advantage. No hardness follows from high Boolean degree.

**The Fourier guarantee is not automatically a new algorithm.** The
framework and GS decoding are prior art. The local support-mask lemma and
this deterministic specialization need independent comparison/review.
The initial pass did not implement a general decoder. BINARY_GS_DECODER.md
subsequently closes its deterministic algorithmic dependency using known
methods and supplies capped executable controls. An actual coherent circuit,
practical gate count and general classical rational attack remain absent.

**Falsifiers retained in tests:** an unbalanced predicate; replacing signed
amplitudes by magnitudes; label-dependent masks; the zero-extended Weil
constant; wrong RS rate/Johnson radius; ambiguous records treated as unique; wrong
native code direction; and incorrectly treating u=0 as an inverse scalar.
Finite controls are explicitly exponential and do not support scaling claims.

## Reproduction And Next Work

    python -m theorems.balanced_codeword_filter --write
    python -m pytest -q tests/test_balanced_codeword_filter.py

Read research/reductions/balanced_codeword_filter.json for exact controls
and sufficient budgets. Prioritize adversarial proof review and a classical
rational-interpolation attack. A replay or GS adapter is mechanical work;
do not start a seed campaign, dashboard feature or speedup registry entry.

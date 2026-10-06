# Conditional Carry Features And Pivot-Pencil Coverage

LOCAL DERIVATION / REVIEW PENDING. No independently reviewed theorem, efficient
growing-modulus decoder, accepted candidate, novelty or speedup. This extends
`DCP_LOWBIT_FIBER_NORMALIZER.md` with the correct next-layer source representation
and an actual-packet matrix-pencil extractor, not another circuit search.

## The Conditional Source That Actually Survives

Suppose a public injective physical Boolean map g(r) describes a complete
parameterized low-residue domain. It was selected using only label bits below
2^ell, and satisfies A_low g(r)=v mod2^ell for every r. Write

    A = A_low + 2^ell H + 2^(ell+1) J,
    c(r) = (A_low g(r)-v)/2^ell mod2.

Conditional on all lower data, native H mod2 is a fresh IID uniform n by m
binary matrix. The NEXT residue bit is exactly

    b_H(r) = c(r) XOR H g(r).                         (1)

The unused J does not enter this bit. The randomness is in the span of the
PHYSICAL Boolean features, NOT fresh independent ANF coefficients or a fresh
native quadratic parity chart. Every output row has exactly 2^rank(g) possible
functions, each with fresh-label multiplicity 2^(m-rank(g)). The function rank
is computed from explicit sparse ANF coefficients, not an assignment table.

The module also solves for linear combinations of physical features recovering
each input coordinate. When found, this proves injectivity symbolically.
Failure to find such a linear recovery is NOT proof of noninjectivity.
For an injective g on the full uniform input cube of size N=2^d, every distinct
pair has a nonzero feature difference. Hence its fresh-H bit-vector difference
is uniform regardless of c, and

    E_H chi_squared(histogram(b_H),uniform_F2^n) = (2^n-1)/N.   (2)

This is only a collision/occupancy identity. It neither normalizes a fiber nor
implements an inverse. A truncated or conditioned domain must have its actual
size, measure and source law charged instead. Source lineage remains a proof
obligation; a Boolean declaration cannot prove that a map preceded H.

Countercontrol: on a one-bit input, choose a nonzero physical direction in the
kernel of the CURRENT two-bit H. Each selected feature map is injective, but
H g(r) is identically zero for every H. Actual mean chi-squared is1, not the
fixed-map formula1/2. Adaptive feature selection therefore cannot borrow (2).
It can still be a legal algorithm; it needs its joint pushforward source law.

## Exact Affine-Restriction Source Gate

For fixed independent retained directions u_i selected before H, affineness on
EVERY background is equivalent to vanishing mixed XOR derivatives:

    D_(u_i) D_(u_j) c(r)
      = sum_a H_a D_(u_i) D_(u_j) g_a(r), for all r.    (3)

Equating sparse ANF coefficients gives a binary linear system in the fresh
label bits. The gate solves it for each output row. If consistent, its exact
source mass is 2^(-sum_l rank_l); otherwise it is zero. This includes the
nonzero carry right-hand side, all backgrounds and every source outcome.
There is no assumption of independent background events. A direction search
using H must charge its selection/menu or derive a different joint law.

Sparse derivative translation has an explicit expansion cap. It is polynomial
at fixed bounded ANF degree, not at unbounded degree. An expansion-cap failure
is a tooling limit, not a mathematical negative result. Compact evaluator
circuits remain the long-term representation for genuinely higher layers.

## The Quartic Is Not Only Adaptive-Pivot Damage

Fix the lower row A_low=(1,1,3,1,1,3), the low residue v=0 mod4, and q16.
Choose isotropic logical directions (31,6,24), complemented by (2,8).
The coefficient of direction31 is1 on EVERY background. Keep its pivot and
the other input coordinates fixed; no background-dependent pivot selection
is used. The inverse graph has quadratic physical features with nonlinear
function-space rank ONE. It is exactly reversible on the full original cube.

On the four remaining coordinates, the lower carry c has ANF masks

    1,2,4,14,15.

All64 fresh next-bit label tables give32 distinct functions, each twice. EVERY
function has degree4: the quadratic physical features cannot cancel mask15.
The exact next-bit Hamming-weight histogram over these64 tables is

    weight1:2, weight5:8, weight7:28, weight9:22, weight11:4.

Their mean histogram chi-squared is1/16, agreeing with (2), despite none being
quadratic. Near-uniform second moments do not certify algebraic closure.

A nonzero full-degree Boolean coefficient is the parity of all function values
and is invariant under invertible affine coordinate changes. For any two
independent directions, change them to the first two coordinate axes. Their
mixed derivative retains the full-degree product of the remaining coordinates.
It is nonzero. Consequently all105 two-direction affine-restriction gates
have source mass zero here, even if the directions were chosen after H.
All64 functions also have odd weight, so none is balanced. A full-basis
permutation cannot turn any into an EXACT balanced coordinate on this domain.

This excludes this exact quadratic restart and all-background linear-affine
restriction shortcut, NOT alternative nonlinear graphs, approximate transport,
favorable-background protocols with charged mass, added states or general
quantum readout. It is a scoped counterexample, not a new oracle candidate.

## Constant Pivot Matrix Versus Nonsingular Pencil

In a common-isotropic chart U with complement V, a pivot direction has a
globally CONSTANT coefficient vector only if its quadratic polar forms vanish
on V. Isotropy already makes them vanish on U, so it belongs to the common
quadratic radical on the whole kernel. Thus n independent constant pivot
columns require radical dimension at least n. The existing conductor primitive
computes that radical. A connected fundamental graph bounds it by one.

Crucially this is NOT a no-go for a fixed pivot BLOCK with a VARYING but always
invertible matrix. The native fixed low signature

    B = [[1,0,1,0,1], [0,1,0,1,1]]

with specific labels [[1,0,3,2,1],[0,1,2,1,1]] has zero common radical, yet its
two background pivot matrices are

    C=[[0,1],[1,1]], C+I=[[1,1],[1,0]].

Both are invertible. The first plane is exactly normalized on every background.
Abstract binary nonsingular pencils are established matrix-space structure;
see [de Seguins Pazzis, Sections5.2-5.3](https://arxiv.org/pdf/1405.1575).
There is no novelty claim for this algebraic mechanism.

Complete enumeration of the1,024 middle-label tables for this low signature
gives0,1,2 good backgrounds with multiplicities384,512,128. Conditional
all-background success is1/8. The specified systematic low signature itself
has mass1/64. Extending R=[I_n|1] naively has mass2^(-n(n+1)); this is not a
scalable native-source decoder. Low-bit source geometry may be selected in
more sophisticated ways, but its actual prevalence and higher-carry law remain
unproved. Do not promote a small positive control to a candidate.

## Polynomial Pencil Coverage Certificate

The extractor builds the actual chosen n-column pivot pencil

    M(y)=M0 + sum_j y_j M_j

from public packet evaluations at the low chart's direction/background basis.
It never enumerates 2^k physical assignments or 2^background_bits backgrounds.
The associated matrix-space image and each column projection have computable
binary ranks. Equality between image rank and the sum of column ranks means
the image is the Cartesian product of its column spaces.

For that COLUMN-SEPARABLE case with invertible M0, normalize by M0^-1. Draw an
edge j->i when column j can have a1 in row i. If the graph is acyclic, a
topological ordering makes every perturbation strictly triangular, so every
background matrix is invertible. This is a positive exact certificate.

If there is a cycle, choose a shortest one. It has no smaller-cycle chord.
Choose each involved column variation with a1 on its cycle edge, and set
other columns to zero. The cycle principal block makes I+variation singular.
Column separability makes this desired combination reachable by a background.
A binary solve returns that background AND a verified nonzero kernel vector.
If every column varies, a finite directed graph has a cycle for EVERY M0;
no constant part can make that separable variation space globally nonsingular.

For a FULL n-by-n matrix image, uniform background gives the exact invertible
fraction product_(j=1)^n(1-2^-j), independent of M0. This is different from
merely finding one rare bad background. Otherwise the checker does not invent
a failure-fraction estimate. Correlated pencil images are left open, not rejected
by a column-separable criterion. Mixing the basis inside an already rejected
pivot SPACE does not repair it: invertible rebasing preserves singularity.
Search new spans or new operations, not cosmetic correlations from rebasing.

Three generated systematic chart profiles use n2,3,4 and q=2^(4n+1),
k=4n^2+16. Their selected pivot-image ranks are0,7,8. These are algebraic
profiles, not secret-state experiments or evidence of typical large-n behavior.
Small n has many low-label zero columns; it can overstate easy directions.
Even exact small-profile pencil failures do not close other pivot spans.
Subsequent `DCP_SYSTEMATIC_SOURCE_TRANSPORT.md` proves that a low-only row
transform realizes this identity-binary-prefix/higher-IID source at constant
native acceptance cost. The profile counts still do not prove typical scaling
or a decoder, and specially selected tail signatures remain separately charged.

## Literature And Next Decision

The curated source audit deliberately sits OUTSIDE active hypothesis seeds.
The advertised [quantum-MQ advantage paper](https://arxiv.org/abs/2411.14697)
was withdrawn after the authors learned of a classical attack. This does not
show its quantum proofs were wrong, but its separation cannot support this
project. The attack itself has not been reconstructed in this pass.

[Huang and Bao's MQ preprint](https://arxiv.org/abs/1507.03674) describes a
characteristic-two polynomial regime with sufficiently many variables. It is
a relevant FIRST-layer classical baseline, not a theorem for our quartic
quotients. Only its abstract was checked here; proof applicability is pending.
Also do not import matrix-space classifications stated for fields with at least
three elements into F2 without the appropriate binary theorem.

Next high-impact task: construct low-source-valid pivot spans or richer
nonlinear lifts whose CORRELATED variation has an efficiently certified useful
inverse and survives (1)-(3). Test actual source coverage and the higher carry,
not just the pencil rank. If only classical transport is supplied, retain the
exact independent-target two-call arithmetic comparator from the dense note.
Reject hidden fiber oracles, exponential signature selection and determinant
tests on only favorable backgrounds. Independent theorem review remains needed.

## Verification

Eighteen focused tests include all4,096 two-by-two two-generator pencils,
source RHS/rank accounting, polynomial linear feature recovery, inverse-source
countercontrols, quartic persistence, and actual packet-pencil extraction.
The independent Node checker recomputes physical arithmetic, all source counts,
all105 affine gates, common radicals, the1,024-table positive pencil control,
pencil coverage/witness formulas, actual systematic profiles and four hashes.
This is implementation crosschecking, NOT theorem peer review or full production
validation. CLI/registry integration and production regressions remain Gemini.

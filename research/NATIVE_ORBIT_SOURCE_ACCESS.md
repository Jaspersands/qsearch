# Native Copy-To-Coset Compilation And The Relative-Inverse Trap

LOCAL DERIVATION / REVIEW PENDING. Actual source conversion, no full-depth
solver, exact preparation oracle, novelty claim or general catalytic no-go.

## A Real Source Compiler Using One Original Copy

The ideal native mixed source has Tr(R(g)rho)=1[g in H], with a PUBLIC
efficient induced action. Prepare the group register uniformly and apply
controlled R. The known relative preparation is

    V|v> = |G|^(-1/2) sum_g |g> R(g)|v>.

This is an isometry on the ENTIRE seed space, V^dagger V=I. Its physical
unitary extension is controlled-R composed with uniform group preparation.
That extension AND its inverse are known. Its inverse returns the ORIGINAL
unknown input seed, not a known all-zero register. Do not say all reversible
orbit preparation is missing just because an input state is unknown.

Discarding the seed gives group-register entries

    Xi(g,h)=Tr(R(h^-1*g)rho)/|G|=1[h^-1*g in H]/|G|.

This is exactly the ordinary uniform coset mixed state for left cosets gH.
One IID native copy yields one IID coset mixed state. A mathematical
purification can be used to prove this; it is NOT an accessible extra
environment or a supplied purification-creation unitary. Conditional on
every observed frequency label, the single conditional source need not
already have this exact density. The unconditioned source promise is needed.

For native level r and vector dimension n, public uniform group coordinates
use nr+1 trits; one known controlled-R call performs the compiler. Its ring
phase arithmetic is secret-independent. Gate precision and input error need
an aggregate certificate; exact small matrices are not a hardware compiler.
The recipe does not enumerate |G| to implement the known action.

## What The Primary Nilpotent Result Actually Supplies

[Imran--Ivanyos v1, Theorem1 and Section2.3](https://arxiv.org/pdf/2304.08376)
uses a fixed purification-creation unitary on zero input and its inverse.
Its Proposition3 is a NON-EXACT variant without calls to that inverse.
Both the bounded-class regime and its class-dependent conversion cost
remain important. Section4's central conversion takes fresh subgroup states;
the non-exact alternative is relevant to copy-only sources, but does not
turn a growing-class native instance into a polynomial algorithm.

The new compiler provides genuine subgroup-state COPIES. It does not provide
the stronger exact oracle. A paper-to-source comparison should separate
these statements rather than write one blanket inverse-access rejection.
The precise circuit use of general forward preparation must still be checked
when importing a theorem, not inferred from the word 'oracle'.

## Why The Obvious Oblivious-Amplification Repair Fails

The cheap transported zero-GROUP-register reflection is about

    Q=V V^dagger,

whose rank is the full seed dimension. It is not a reflection about one
fixed prepared purification. Let T(k)|g>=|g*k^-1> be the right-regular action.
Then T(k)V=V R(k). For ANY whole Fourier-irrep-label projector P_lambda,

    P_lambda V=V P_lambda^(R),
    [P_lambda,Q]=0,
    V^dagger P_lambda V=P_lambda^(R).

The compressed filter is an exact SEED isotypic projector, not a scalar
known success amplitude. Therefore alternating arbitrary phase reflections
about Q and a subset of whole Fourier labels preserves that subset's Born
mass. No number of these relative-Grover iterations amplifies it. This also
covers every Fourier-character filter in an abelian group. It does not cover
filters on noncentral matrix indices or additional operations moving between
seed isotypes, and is not a lower bound on all catalytic algorithms.

For the trivial label, compressed filter=(1/|G|)sum_g R(g), the invariant-seed
projector. Its native probability is1/3^(nr). At bounded n1 levels1/2, the
public partial reflection leaves probabilities1/3 and1/9 unchanged for all
tested iteration counts. A COUNTERFACTUAL reflection about the full fixed
purification would give, after one Grover iteration,

    p*(3-4*p)^2,

namely25/27 and529/729. That stronger operation is NOT supplied. The contrast
prevents confusing a reversible relative circuit with a blank-state oracle.

## Revised Research Consequence

The orbit compiler removes a source-format issue. It does not remove the
growing-class copy recurrence, supply a cloning/preparation oracle or repair
exact amplification. Use genuine copy-only/non-exact theorems where their
class and cost assumptions match. Stop trying to amplify whole irrep-label
events using only the cheap relative reflection. A constructive catalytic
proposal must identify a NEW seed-isotype-changing or noncentral joint
operation and prove it preserves the useful source promise, rather than
replacing an unavailable projector with a larger available subspace.

The producer executes four complete actual native orbit sources, their
inverse return, every group-density entry, every irreplabel projector at
levels1/2, partial-reflection histories and fixed-purification contrasts.
The source/model/error scope remains explicit. External review is required.

## Noncentral Countercontrol And The Actual Next Operator Target

The scope is essential: a computational-coordinate projector P=|e><e|
has compressed filter C=V^dagger P V=I/|G|, NOT a projector. The same
available relative reflection raises its raw probability from1/|G| to
(1/|G|)*(3-4/|G|)^2 in one iteration. Conditioned on that outcome the seed
is precisely the original unknown seed, even with an arbitrary entangled
reference. For any other public coordinate, the seed is R(g)rho R(g)^dagger
and a known inverse restores it. Neither event probability reveals the secret.
Thus amplification is possible; useful information extraction is not supplied.

For ANY group-register projector P define C=V^dagger P V. One relative
Grover iteration has good component

    P V (3I-4C)|seed>,

with raw probability Tr(rho C(3I-4C)^2). This identity holds for mixed seeds
and inaccessible reference systems too. Whole-irrep filters have projector
C and cannot amplify. Coordinate filters have scalar C and amplify an
uninformative event. A new noncentral proposal must give an implementable
P, its actual SOURCE-WEIGHTED compressed operator, and an informative final
measurement; a growing scalar success probability is not enough.

The independent checker reconstructs the original induced representations
and source phases in Q(zeta_3), all1620 density entries and all40 irreplabel
compressions/intertwining identities. Four noncentral countercontrols and
ten forged artifact classes test the source-access boundary. Small numerical
matrices are calibration evidence, not a growing-instance implementation.

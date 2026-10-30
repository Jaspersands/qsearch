# Lean Formalization: Checked Research Claims

The default build now checks the concrete positive lower-central Rees Lie
algebra, its evaluation and dilation maps, its hidden-subalgebra
interpolation, and canonical prime-power-ring interpolation. At class at
most three it also constructs the actual BCH group and transports the
concrete Rees maps into the group-level hiding theorem. It now constructs
the actual central quotients and instantiates the full-register central
measurements and their two-stage fresh-bank composition, retaining all of
log(H) at the terminal additive quotient. Total valid SDE policies remain
supplied inputs. General-class BCH/Lazard transport, original-oracle-to-
recovery/error integration and a polynomial-time receiver theorem remain
outside this verification.

This folder holds a Lean 4 + Mathlib project. It checks the mixed affine-support
Kraus identity, conditional scalar and matrix group-coset Fourier conversions,
the abstract tuple-oracle reduction to a nonabelian cocycle graph subgroup,
the conditional mixed central-character descent Kraus contraction,
quotient hiding-oracle inheritance and reversible representative cleanup,
a complete right-abelian-character instrument for reducible regular sources,
including noncentral fibers and its additive-quotient scalar-channel composition, the universal
commuting-adjoint specialization and truncation rules for the induced cocycle,
class-three Lie chart/potential identities, the class-three-normal monomial
action, complete coherent retained-frequency Fourier basis and its actual
BCH-source contraction, ambient Lie-word filtration and symbolic
source-phase degree bounds, a conditional Weyl-matrix
source scalarization, a nonlinear-jet measurement channel and full Taylor
transport on its actual finite coefficient space, public full-jet source
alignment from feature rank, coefficientwise weighted phase cancellation
and its composition with the full-jet merge channel, the balanced
signed rational-separation algebra below, and parts of
`research/PRIME_CHARACTER_EXTERIOR_BOUND.md` (called "the note" below) and of
its Python mirror `exterior_characters`
(`theorems/prime_character_exterior_bound.py`, line 33).

Nothing here uses `sorry`. The guards in `Formal/Audit.lean` and the local
guards in `Formal/AffineSupportErasure.lean`, `Formal/CosetSourceFourier.lean`,
`Formal/ClassThreePotential.lean`, `Formal/ClassThreeMonomial.lean`, `Formal/CosetMatrixSource.lean`,
`Formal/JetOracleHomogenization.lean`,
`Formal/ReesHomogenization.lean`,
`Formal/ReesPrimePowerInterpolation.lean`,
`Formal/ReesLieConstruction.lean`,
`Formal/ReesLieInterpolation.lean`,
`Formal/BCHClassThree.lean`,
`Formal/BCHClassThreeSubgroups.lean`,
`Formal/ReesGroupClassThree.lean`,
`Formal/ReesCentralQuotient.lean`,
`Formal/ReesCentralQuotientBCH.lean`,
`Formal/ReesClassThreeReceiver.lean`,
`Formal/CentralCharacterDescent.lean`,
`Formal/CentralQuotientReceiver.lean`,
`Formal/CentralSpectralProjector.lean`,
`Formal/CentralDescentRecords.lean`,
`Formal/CentralDescentPolicy.lean`,
`Formal/ReesMeasuredReceiver.lean`,
`Formal/RecursiveOracleReduction.lean`,
`Formal/CentralRegularSource.lean`,
`Formal/RetainedFourier.lean`,
`Formal/VectorCentralSource.lean`,
`Formal/InducedRegularSource.lean`,
`Formal/InducedCocycleOperators.lean`,
`Formal/ClassThreePhaseBounds.lean`,
`Formal/AmbientPotentialFiltration.lean`,
`Formal/WeylSourceScalarization.lean`, `Formal/MatrixBatchShear.lean`, and
`Formal/CommonQuadraticJet.lean`, `Formal/NonlinearJetChannel.lean`,
`Formal/FullTaylorTransport.lean`, `Formal/FullJetAlignment.lean`,
`Formal/WeightedPhaseErasure.lean`, `Formal/FullJetWeightedErasure.lean`, and
`Formal/EquivariantLabelSelection.lean`
check the listed headline theorems against subsets of Lean's three standard
axioms, so `lake build` fails if a
`sorry` gets into one of them or into anything they use. A `sorry` in some other
theorem only produces a warning, so CI builds with `lake build --wfail`, which
fails on any warning. On 2026-10-19 both checks were tested: a `sorry` in
`ceilSqrt_le_sqrt_add_one` failed `lake build`, and a `sorry` in a new,
unlisted theorem passed `lake build` but failed `lake build --wfail`.

## How to build

Versions are pinned: Lean `v4.35.0` (`lean-toolchain`) and Mathlib `v4.35.0`
(commit `56a0058`, in `lake-manifest.json`).

1. Install elan from https://github.com/leanprover/elan.
2. From this folder (`formal/`), run:

```text
lake exe cache get    # downloads prebuilt Mathlib; never build Mathlib yourself
lake build --wfail
```

The build output (about 7 GB, mostly Mathlib) goes in `formal/.lake/`, which
git ignores. If the checkout is in a folder that iCloud or another service syncs,
exclude `formal/.lake/`. CI runs the same steps in `.github/workflows/lean.yml`.
A clean local build took about 5 minutes after the cache download; a rebuild with
nothing changed takes seconds.

To regenerate the Python values after `exterior_characters` changes, run
`python formal/scripts/gen_crosscheck.py` from the repository root. Add
`--check` to check the file without rewriting it.

## Rees Interfaces and Nontransverse Central Descent

The promoted module is imported by `Formal.lean`. Its guarded theorems in
`QSearch.ReesHomogenization` are:

| Theorem | Checked statement |
|---|---|
| `coefficientwise_iff` | With no constant term, evaluation at n distinct nonzero field points lies in a linear submodule exactly when all n coefficients do. The submodule need not be homogeneous. |
| `tuple_hides` | An ordered tuple of original oracle evaluations has exactly the coefficientwise hiding relation, assuming the evaluation homomorphisms, their log/coefficient identity, and the original oracle hiding relation. |
| `coefficient_translate` | The finite central coefficient at h * embed(z), for h in H, is the character sum over embed's preimage of H times chi(z). |
| `coefficient_allowed` | If chi is trivial on that preimage, the coefficient is its actual cardinality times chi(z). |

These are interface lemmas. The concrete Lie construction and its
interpolation identity are now supplied by the separate modules below.
The class-three group bridge below now supplies BCH/group transport and
the group-level log/coefficient identity in that scope. General-class
transport, oracle implementation, sampling/SDE algorithms, recursion,
complexity and the polynomial-time receiver theorem remain outside this
formalization.

### Concrete Lie Cover And Ring Bridge

`Formal/ReesLieConstruction.lean` works over any commutative ring, with
actual Mathlib Lie axioms. Its ambient algebra is the ordinary polynomial
current algebra `AddMonoidAlgebra R Nat` tensor `L`, not a truncated
quotient or a supplied bracket table with unverified laws.

| Definition/theorem | Checked statement |
|---|---|
| `gamma_bracket_le`, `rees` | Jacobi and the actual lower central series prove untruncated closure of the positive Rees span. |
| `mem_rees_iff`, `nilpotent_cutoff` | Exactly the positive lower-central coefficients occur; above an explicit class bound they and the corresponding brackets are actually zero. |
| `evaluation`, `evaluation_formula` | Evaluation is an actual Lie homomorphism with its actual coefficient sum, independent of the hidden subalgebra. |
| `scaling_coeff`, `dilation` | Scalar substitution scales grade r by a^r; unit scalars give Lie automorphisms. |
| `grade_one_retention` | Evaluation at one splits the grade-one LINEAR embedding of all L, including derived directions. This embedding is not asserted to be a Lie homomorphism. |
| `rees_class_bound` | The cover inherits the supplied nilpotence class bound of L. |

`Formal/ReesLieInterpolation.lean` connects these actual evaluation sums to
the finite interpolation matrix, using the proved coefficient cutoff.
Its `hiddenCover` is an actual Lie subalgebra defined by evaluation
preimages. `mem_hiddenCover_iff` identifies it with coefficientwise
membership in the ambient hidden subalgebra; `dilation_mem_iff` proves
unit-scale invariance in BOTH directions. No original grading, hidden
ideal assumption, or supplied invariance equation is required. This is
the ambient intersection construction, not the generally smaller Rees
cover of the hidden algebra's intrinsic lower central series.

`Formal/ReesPrimePowerInterpolation.lean` proves the canonical points
1,...,c have unit evaluation determinant modulo p^e, for prime p, e>0,
c<p. The generalized ring interface in `ReesHomogenization` needs no
freeness of the coefficient module or quotient. A kernel-checked Z/9
counterexample shows why distinct unit points and a nonzero determinant
do not suffice: 6t+3t^2 vanishes at both 1 and 4.

The hidden subalgebra is a correctness parameter, not an input to
`evaluation` or `dilation`. These noncomputable mathematical definitions
do not extract executable circuits or resource bounds. In particular,
proving a Lie homomorphism alone does not instantiate the group homomorphism
argument of `tuple_hides`. The separate class-three construction below now
does so in its stated scope. See `research/REES_CONCRETE_FORMALIZATION.md`
for the earlier Lie-level checkpoint.

### Actual Class-Three Group Layer

`Formal/BCHClassThree.lean` constructs a group with multiplication
`x+y+[x,y]/2+([x,[x,y]]+[y,[y,x]])/12`, identity zero and inverse negation.
It proves associativity from Jacobi and the actual lower-central bound
`lowerCentralSeries F L L 3 = bottom`. The coefficient field must have
nonzero 2 and 3, so prime fields of characteristic greater than three are
included; characteristic zero is not required. No original grading or
supplied associativity identity is assumed.

`lieHom` and `lieEquiv` turn actual Lie maps into group maps and equivalences.
`val_pow` and `val_zpow` prove the group-power/logarithmic-scalar formulas.
`Formal/ReesGroupClassThree.lean` specializes these to the concrete Rees
evaluation and dilation. Its `evaluation_identity` instantiates the old
interpolation interface, and `tuple_hides_subgroup` proves exact hiding of
the actual lifted subgroup. The canonical points 1,2,3 have unit determinant
12. No hidden ideal or homogeneity premise is added.

`Formal/BCHClassThreeSubgroups.lean` derives a Lie subalgebra from ANY
subgroup of the prime-field BCH group using explicit powers and commutator
words. It proves both round trips, rather than assuming additive or bracket
closure. `ReesGroupClassThree.tuple_hides_arbitrary_subgroup` composes this
correspondence with the canonical evaluation maps. No supplied log-H space,
hidden ideal, grading or normality premise remains in that theorem.
`dilation_arbitrary_subgroup` proves invariance of the actual hidden lift.

An arbitrary subgroup's logarithm is not assumed linear over a general
extension field. See `research/REES_CLASS_THREE_GROUP_FORMALIZATION.md` for
scope, counterexamples and final verification. This is not general-class or
prime-power-ring BCH, executable circuit extraction, or whole-receiver proof.

`QSearch.CentralCharacterDescent.coefficient_allowed` applies the promoted
coefficient lemma to the existing source definition. Write
`K = H.comap embed` and `k = Fintype.card K`, so K is the **full preimage**
of H in C. For an allowed character (`embed z` in H implies `chi z = 1`):

* `twisted_trace_allowed`: the raw `twistedEntry` has trace k.
* `label_probability_allowed`: the actual one-sided `projectedEntry` has
  trace k / |C|. `label_probability_allowed_ne_zero` proves it is nonzero.
* `normalizedEntry` divides `twistedEntry` by k. `normalized_source`
  identifies it with `projectedEntry` divided by the latter's actual trace;
  `normalized_trace` proves trace one.
* `normalized_correlation` retains the factor 1/k explicitly;
  `normalized_correlation_at` cancels it using `coefficient_allowed`, giving
  chi(z) on h * embed(z), while `normalized_correlation_off` gives zero
  outside that support.
* `mem_saturation_iff` uses explicit centrality of embed's image to identify
  membership in `H ⊔ embed.range` with a decomposition h * embed(z).
* `normalized_descent_output` invokes the existing `descent_output` on the
  independent tensor of these normalized sources, giving the literal
  controlled-action Kraus output for the saturated subgroup.

The last theorem requires a **nonempty** finite active tensor, allowed
characters for every factor, centrality, homomorphic actions preserving
membership in `H ⊔ embed.range` in both directions, central decomposition
witnesses on support, and cancellation of their character product. The
witness `centralPart` appears only in correctness premises, not in the
controlled-action Kraus operators. Independence is represented by an
explicit product source; it is not inferred from its marginals. To read
the resulting matrix as a quotient coset source, representatives must be
an appropriate quotient transversal; the theorem itself accepts any map.

No injectivity of `embed` is needed for these identities: k counts the
preimage, including the kernel, rather than merely the image intersection.
Identifying k with |H intersect image(embed)| requires injectivity. Allowed
characters, not arbitrary labels, are the scope of normalization; the
distribution over all labels and rejection of disallowed labels are not
proved in that older module. The new quotient-receiver module below proves
zero-source rejection and identifies all nonzero-trace branches. The old
transverse lemmas remain available as special cases.
The one-sided matrix identity alone is not a proof of spectral-projector
idempotence, two-sided projection, positivity or instrument completeness.
`action_complete` separately proves completeness of the controlled-action
Kraus family for a nonempty control type.

The local headline `#guard_msgs` / `#print axioms` checks and the global
`Formal/Audit.lean` guards permit only subsets of `propext`,
`Classical.choice` and `Quot.sound`. The global audit explicitly covers all
nine promoted Rees theorems and all eleven new central-descent theorems,
including the normalization and support helper lemmas. The concrete-cover
pass adds 30 global guards for the ring interface, concrete Lie maps,
interpolation bridge and ring countercontrols. With installed
dependencies, validation without build-cache downloads from `formal/` uses:

```text
lake --no-cache build Formal.ReesHomogenization Formal.CentralCharacterDescent --wfail
lake --no-cache build Formal.ReesLieConstruction Formal.ReesLieInterpolation Formal.ReesPrimePowerInterpolation --wfail
lake --no-cache env lean -DwarningAsError=true Formal/ReesHomogenization.lean
lake --no-cache env lean -DwarningAsError=true Formal/CentralCharacterDescent.lean
lake --no-cache env lean -DwarningAsError=true Formal/Audit.lean
lake --no-cache build --wfail
```

`--no-cache` prevents Lake build-cache downloads; this validation assumes
the pinned toolchain, dependencies and their compiled artifacts already
exist. It does not request installation or dependency updates.

### Actual Quotient Coset Output

`Formal/CentralQuotientReceiver.lean` connects the normalized source to an
actual homomorphic quotient map `pi`, with `pi.ker = embed.range`. It does
not require the hidden H to contain the kernel or be normal, and its public
right inverse need not preserve multiplication.

* `disallowed_projected_source` proves the entire projected matrix is zero
  for a character nontrivial on `H.comap embed`.
* `nonzero_branch_iff_allowed` derives character admissibility from the
  nonzero trace of the actual projected matrix.
* `dilation_preserves_saturation` derives saturation preservation from
  automorphisms preserving H and acting by automorphisms on the center.
* `quotient_coset_output` derives the required correlations and proves the
  controlled-discard output is exactly `groupEntry (H.map pi)`.
* `scalar_quotient_coset_output` replaces the phase-cancellation premise
  with the vector SDE `sum_i s_i^d lambda_i = 0` and takes actual nonzero
  branch traces, not a separately assumed admissible-label predicate.
* `active_sde` and `active_nonempty` justify the active-target restriction
  from a nonzero SDE witness; removing zero scales requires positive degree.

The source remains an explicit independent tensor. This older module alone does not certify
spectral projector physics, the distribution of complete label records,
fresh-copy recursion, a solver, a circuit, or its running time. The concrete
class-three bridge below now instantiates the quotient/scaling premises.
The new coupled Python control uses a nonnormal H with a proper nontrivial
central intersection and nonlinear quotient section. Incorrect transverse
normalization gives output trace nine instead of one; this is an arithmetic
falsifier, not evidence of an algorithmic speedup.

### Concrete Class-Three Quotient Steps

`Formal/ReesCentralQuotient.lean` constructs the actual tail ideals and
their Lie quotients. It proves centrality of successive kernels, identifies
each kernel with the corresponding lower-central coefficient space, derives
its dilation weight, and proves finiteness from retained coordinates.
`Formal/ReesCentralQuotientBCH.lean` transports these to actual BCH group
projections with central kernels, derives hidden-image preservation, and
identifies the terminal group with ADDITIVE L, not L/[L,L].

`Formal/ReesClassThreeReceiver.lean` supplies explicit H-independent sections
by inserting zero top coefficients. Its `degree_three_output` and
`degree_two_output` instantiate the generic channel theorem for arbitrary
prime-field hidden H, including nonnormal H and nontrivial central
intersections. `terminal_source` retains exactly all of log(H).

In that branchwise module, the source tensor is independently normalized, the measured branches
must have nonzero trace, and a nonzero active SDE witness is supplied. No
complete measurement, fresh-source recursion, solver or runtime is extracted.
The branchwise theorem allows any base character; a complete linear-label
spectral instrument on a nontrivial center requires a nontrivial one. A
Python countercontrol shows why repeated trivial-character projectors fail.

All four new modules are in the default build, with 44 local headline axiom
guards repeated in `Formal/Audit.lean`. The full build and five strict
file checks passed on 2026-10-27. See
`research/REES_CENTRAL_QUOTIENT_FORMALIZATION.md` for exact scope, independent
semantic review, reproducible commands and source hashes.

### Complete Measured Class-Three Descent

`Formal/CentralSpectralProjector.lean` derives the actual full-register
projector Kraus operators from a central ancilla permutation and Fourier
amplitudes. Orthogonality, idempotence and completeness hold over all
additive characters. Its two-sided branch equals the source used by the
earlier descent module for arbitrary H and arbitrary central intersection.

`Formal/CentralDescentRecords.lean` proves tensor measurement factorization
and the unnormalized output law for every record. Impossible labels give
zero matrices. Zero-scale targets use identity controls and retain their
branch-mass factors when traced out; an all-zero witness is excluded.

`Formal/ReesMeasuredReceiver.lean` reuses the existing nontrivial-base
linear-character equivalence. It derives the actual measured cubic and
quadratic steps, sums all records, and composes the two H-independent
operations on fresh banks. `measured_terminal_source` recovers the additive
coset matrix of all log(H). No desired normalized source is assumed at an
intermediate stage. Fresh tensor powers are supplied copies, not cloning.

Total valid SDE witness policies and exact initial lifted coset sources
remain inputs. There is no extracted solver, gate implementation, runtime
bound, approximate error proof, final Fourier learning theorem or new
application. The three modules add 31 local/global axiom guards. Independent
automated semantic review found no defect in this scoped composition.
The full Lean build, four strict checks and 130 selected Python tests pass;
the new finite control covers all 59,049 five-label records. See
`research/REES_MEASURED_RECEIVER_FORMALIZATION.md` for details and provenance.

## General Induced-Cocycle Operator Algebra

### Bounded Label-Dependent Policies

`Formal/CentralDescentPolicy.lean` generalizes padded receiver actions to
automorphisms of any finite central abelian group. Sixteen guarded policy
theorems derive the independent tensor output, including zero-mass
records, accepted-record factorization, actual discarded packet traces,
and conservation for nonnegative normalized choice weights that may
depend on labels. The abstract relation to a supplied input explicitly
assumes measured-ensemble completeness; it does not assume the desired
output. Eight further guarded theorems derive that completeness from the
actual product ancilla-Kraus measurement over the full character dual,
then prove the measured accepted/abort trace is one. This bridge needs
no field structure on the finite additive abelian center, and retains
every zero-mass record.

This is matrix/trace algebra, not extracted positivity/CPTP machinery,
an efficient mixed-ring measurement, a Python-to-Lean policy compiler,
or physical source independence. Subgroup preservation, character
cancellation and valid accepted witnesses remain explicit premises.
See `research/PILOT_RECEIVER_POLICY.md` for the fixed fully charged bank,
failure-aware composition, error promises and decisive source falsifiers.

### Existing Operator Results

`Formal/RecursiveOracleReduction.lean` proves inheritance of hiding
functions through quotient sections with kernel contained in H, nested
section composition, and a reversible compute/query/uncompute identity.
It also proves that discarding the uncomputed section workspace makes
the source diagonal. Full Lie recursion, resource bounds and limitations
are written in `research/RECURSIVE_JET_RECOVERY.md`, not fully formalized.

`Formal/CentralCharacterDescent.lean` derives the one-sided central
projection from the original coset matrix, its normalized right correlation
and branch trace, literal controlled-action Kraus completeness/output, and
the independent tensor quotient kernel, including normalization by the
full hidden central preimage for nontransverse intersections. Subgroup
preservation and phase cancellation remain explicit premises. Projector completeness and the
recursive error argument are written, not fully formalized, in
`research/CENTRAL_CHARACTER_DESCENT.md`. No hidden source is inferred
from marginals and no general quantum receiver is extracted.

`Formal/JetOracleHomogenization.lean` proves a separate deterministic
oracle interface: a cocycle defines a graph subgroup in Mathlib's actual
semidirect product, and injective public evaluation plus the component
hiding relations imply that the public label tuple hides precisely that
subgroup. The operational tuple definition takes no hidden cocycle or
potential. The theorem is not a full Lie/polynomial instantiation, simplex
unisolvence proof, quantum circuit or central-descent theorem. See
`research/JET_ORACLE_HOMOGENIZATION.md` for its exact premises and the
distinction between ordinary-function and state-only input access.

The ambient-filtered refinement is in
`research/AMBIENT_FILTERED_INDUCED_RECEIVER.md`.
`AmbientPotentialFiltration.KillsAboveWeight` requires a coordinate to
annihilate the actual ambient gamma_(w+1). New word, monomial and sum
lemmas prove its section-potential degree is at most w. Two new headline
guards allow only `propext`, `Classical.choice` and `Quot.sound`. This
checks the individual degree origin, not a complete formalized filtered
compiler, heterogeneous quantum instrument or adaptive HSP receiver.

`Formal/InducedCocycleOperators.lean` proves the universal specialization
rules used in `research/INDUCED_COCYCLE_UNIVERSAL_REFINEMENT.md`. Its
`AbelianIdealData` requires an abelian ideal containing all Lie brackets.
For arbitrary A,X, the restricted adjoints commute on this ideal; the
normal-form basis has the stated A/X action, zero internal brackets and
the full coordinate bracket. Iterated ad(A+B) on X reduces to powers of
ad(A) on [A,X]-[X,B]. Lower-central-series membership proves the exact
degree truncation, including the sharper cutoff for a derived-ideal seed.

Six headline guards depend only on `propext` and `Quot.sound`. These
are general Lie-algebra theorems, not finite matrix tests. They do not
formalize exponential differentiation, Lazard correspondence, the Python
rational certificate checker or compiler extraction, and do not establish
a complete HSP receiver or quantum speedup. The separate coefficient
artifact checks whole universal identities through class seven.

## Class-Three Monomial Source Algebra

`Formal/ClassThreeMonomial.lean` is in the normal build. Its bundled
structure maps are alternating beta:A x A->B and gamma:A x A->F, and
bilinear delta:A x B->F, with the class-three Jacobi identity. Gamma and
delta have already been composed with the selected central character.
There is no nonzero-character, positive-B-dimension or irreducibility
premise. The group/action laws are conclusions, not hypotheses.

| Guarded theorem in `QSearch.ClassThreeMonomial` | Statement |
|---|---|
| `product_assoc` | The displayed class-three BCH coordinate product is associative. Identity and coordinate-negation inverse laws are also checked. |
| `phase_comp` | The exact scalar phase obeys Phi(h,t)+Phi(g,T_h t)=Phi(g*h,t), using Jacobi. |
| `displacement_bijective` | The carrier map is an invertible translation on A x dual(B). |
| `phase_inverse` | Applying the inverse element cancels the phase at the translated carrier. |
| `amplitude_comp` | Applying an additive character gives the corresponding complex monomial-amplitude composition. |
| `quadratic_parameter_decomposition` | Phi is a bundled linear map plus diagonal evaluation of a bundled bilinear map in the unknown group coordinates. |
| `partial_fourier_identity` | The actual two-sum contraction F_- W F_-^dag shifts mu to mu+ell and contributes alpha*conjugate((mu+ell)(d)). |

All seven guards allow only Lean's standard three axioms. The field laws
exclude characteristics two and three explicitly; the full algorithm's
stronger p>3D restriction is NOT removed. The Fourier identity uses finite
additive-character orthogonality, not a supplied cancellation equation.
It keeps the frequency register coherent and assumes unit-modulus output
characters. It does not prove completeness/circuit synthesis for a chosen
character indexing scheme or the whole central-source density instrument.
The separate CentralRegularSource module below proves the latter from
public central-fiber and normal-first charts, not from these scalar maps alone.
Group elements, modulations and hidden potentials in these statements are
proof variables, not extra classical inputs supplied to a receiver.

Still outside this module: deriving the structure chart from an actual
ambient Lie algebra with C=Z(N), the ambient polynomial degree bound,
full Taylor transport/GL/rank arguments, weighted polynomial erasure,
uniform SDE implementation, recursion, and full quantum composition.
The Python source/compiler is not formally refined into Lean; six added
small/127-bit regression cases pin its formula to the checked parameter
decomposition. See `research/CLASS_THREE_MONOMIAL_FULL_JET.md`.

```text
lake env lean -DwarningAsError=true Formal/ClassThreeMonomial.lean
```

## Ambient Potential Filtration

`Formal/AmbientPotentialFiltration.lean` derives the projected potential
degree bound from the actual lower central series. A length-k nested word
belongs to gamma_k; when class(L)<=c, words of length >=c-1 commute with
the entire derived space. A coordinate map killing Z([L,L]) therefore
annihilates those high-degree coefficients. Linear input expansion makes
word length equal to quotient-monomial degree.

| Guarded theorem in `QSearch.AmbientPotentialFiltration` | Statement |
|---|---|
| `nested_mem` | A nested word belongs to its actual lower-central filtration space. |
| `high_centralizes_derived` | gamma_(c-1) centralizes the span of all brackets when gamma_(c+1)=0. |
| `long_word_central` | Long words belong to the derived algebra AND its full center. |
| `projected_polynomial_bound` | Scalar coordinates vanishing on that center have degree at most c-2 after linear-input expansion. |
| `unprojected_polynomial_bound` | A Lie-word polynomial truncated at length c has coordinate degree at most c. |

The exact BCH identification of the original source word is a separate
published dependency, with universal rational coefficient certificates
checked by `theorems/ambient_section_potential.py`, not Lean. Its 17 tests
include independent matrix exp/log comparisons, wrong-center and wrong-
class counterexamples, and malformed-certificate rejection. No extra
hidden-potential oracle is supplied. See `research/AMBIENT_SECTION_POTENTIAL.md`.
The input must satisfy the Lie axioms and the class bound; an unchecked
Python bracket callable is not evidence of either.

## Symbolic Class-Three Source Phase Bounds

`Formal/ClassThreePhaseBounds.lean` lifts the actual public bilinear maps
coefficientwise to multivariate polynomials. Evaluation recovers the exact
`ClassThreeMonomial.phase`, including the shifted-frequency correction.
It does not assume the desired phase degree as an input.

The variable space is `Q + J + H`: quotient variables, jet registers, and
one fixed set of formal hidden coefficients. Public source components are
finite sums `coefficient[h] * theta[h] * (Y+s*q)^exponents[h]`. Public
carrier rows are `offset + sum row[j]*t[j]`; the offset includes spectators.
Different blocks may use different public labels, scales, rows and outcomes,
but evaluation uses one assignment of the shared hidden coefficient names.

| Guarded theorem in `QSearch.ClassThreePhaseBounds` | Statement |
|---|---|
| `eval_bilinear` | The coefficient tensor lift evaluates to the original bundled bilinear map. |
| `eval_sourcePhase` | The expanded polynomial evaluates to the exact BCH/shifted-frequency phase. |
| `operational_bound` | Source components a,b and carrier x,mu bounded by D, and c bounded by cdeg, imply phase weight at most max(cdeg,3D). |
| `parameter_bound` | Components linear in hidden parameters and public carriers imply parameter degree at most two. |
| `potential_operational` | Public shifted monomial expansion preserves its input degree bound. |
| `potential_parameter` | The same expansion remains linear in the shared hidden coefficients, for any quotient degree. |
| `compileBatch_bounds` | The actual negative sum of compiled block phases obeys both bounds simultaneously. |
| `compileBatch_evaluation` | The batch equals negative sum Phi(g(Y+s*q),L^-1(t,zeta)) for every parameter assignment. |

No rank or invertibility premise is needed just to bound public affine
rows; their status as a physical GL alignment remains the separate
`FullJetAlignment` obligation. The generic scalar identity even makes
sense in small characteristics with Lean's inverse convention; it is NOT
permission to drop the source/algorithm's characteristic restrictions.

The bounds in this module are conditional on supplied potential degrees.
The separate ambient filtration result above supplies the Lie-word degree
argument; construction of the full-center chart remains a distinct interface.
This module is not an SDE solver, a Python refinement, a composed quantum
algorithm, or a novelty claim. Eight independent SymPy controls compare
the full compiler expression without a degree cutoff, exhibit tight 3D
and central-degree terms, and show that hidden-dependent carriers can
violate the quadratic-parameter bound. See `tests/test_class_three_phase_bounds.py`.

```text
lake env lean -DwarningAsError=true Formal/ClassThreePhaseBounds.lean
```

## Nonlinear Jet Measurement Channel

`Formal/NonlinearJetChannel.lean` is in the normal build. Unlike the affine
modules, it allows an arbitrary curve `F: V -> J`. Its normalized kernel is
`(|V| |J|)^-1 [q-q' in U] [F(q)+t=F(q')+t'] phase(q,t) conjugate(phase(q',t'))`.
There is no assumption that this support is linear or known to the receiver.

Public maps send `(q,t)` to `(Y+c*q,Z+A(Y)*t)`. The support-preservation
theorems require nonzero c, injective A(Y), and the transport identity
`F(Y+c*q)=F(Y)+A(Y)*F(q)`. These are hypotheses, not a formal proof of
Taylor closure within this generic module. `FullTaylorTransport.lean`
now discharges these premises for the full polynomial jet (see below).
The Kraus operators contain neither F nor U. Their
normalization uses a fresh uniform register on `V x J` and their branch
definition contains the actual two matrix-contraction sums.

| Guarded theorem in `QSearch.NonlinearJetChannel` | Statement |
|---|---|
| `public_support_iff` | Public transport preserves and reflects the nonlinear coherence relation. |
| `kraus_complete` | Summing all outcomes gives the identity, even without invertible maps or nonzero scales. |
| `mixed_branch_identity` | A tensor product of independent, same-curve sources contracts to the same nonlinear support with pulled-back product phase. |
| `branch_probability` | Every joint outcome has trace `(|V| |J|)^(-number of inputs)` for unit phases and active inputs. |
| `nonlinear_source_to_scalar` | Existing spectator Kraus sums give this kernel from monomial displacement `(a+F(q),b)`, without assuming F linear. |
| `fourier_residual` | Negative-character readout of the phase-free jet leaves `|J|^-1 rho(U,chi composed with F)` for every unit additive character. |
| `fourier_probability` | Each such Fourier block has trace `|J|^-1`. |
| `trivial_support_hides_curve` | For U=0 the source is maximally mixed, independently of F and the unit phase. |
| `coset_gauge_invariance` | Adding any offset constant on U-cosets leaves the source unchanged. |

All nine guards allow only the standard three Lean axioms. No `sorry`,
extra axiom or `native_decide` is used. The last two theorems delimit the
abstract source interface; they do not rule out all HSP-to-HPGP reductions.
Every batch input in `mixed_branch_identity` must be active. Zero-scale
inputs must be discarded before invoking it.

This does NOT formalize polynomial degree/cancellation, the Taylor identity,
rank/SDE selection, preparation of independent sources in one hidden chart,
the complete normal-group Fourier transform, complete character-family
orthogonality, efficient gate synthesis or the entire HSP algorithm.
Positivity is not separately proved in a general density-operator framework;
trace and Kraus completeness alone must not be cited as its proof.
These noncomputable kernels are mathematical specifications, not executable
quantum circuits. See `research/NONLINEAR_JET_HSP_RECEIVER.md` for the
conditional two-erasure proposal and its remaining obligations.

```text
lake env lean -DwarningAsError=true Formal/NonlinearJetChannel.lean
```

## Full Taylor Transport

`Formal/FullTaylorTransport.lean` is in the normal build. For a hidden
polynomial Q of degree at most D, it defines the full jet by the coefficients
of `Q(Y+s*q)-Q(Y)`. Public transport is substitution
`P(Y,s) -> P(Y+s*z,s*t)`. Neither Q nor its coefficients is an input to
this linear operator or its explicit inverse.

| Guarded theorem in `QSearch.FullTaylorTransport` | Statement |
|---|---|
| `transport_comp` | A(z,t) A(w,u) = A(z+t*w,t*u), with composition order fixed. |
| `jet_transport` | F(z+t*q)=F(z)+A(z,t)F(q), derived from polynomial substitution. |
| `jetSpace_eq_support` | The invariant space has exactly monomials Y^alpha s^k with k>0 and \|alpha\|+k<=D. |
| `transportEquiv` | Nonzero t gives an explicit linear equivalence of that same space; inverse parameters are (-z/t,1/t). |
| `fullJet_public_support` | The existing nonlinear channel preserves and reflects support without assuming the Taylor law or injectivity. |
| `fullJet_mixed_branch` | Vector-valued bounded-degree polynomials instantiate the actual mixed-channel contraction with neither transport premise left open. |

Total-degree preservation, finite dimensionality, the zero-s coefficient
projection, and the componentwise vector extension are also checked.
The six axiom guards allow only Lean's standard three axioms. This algebra
works over any field and for every D; that does NOT waive the stronger
prime/degree restrictions required by rank, source and erasure arguments.
Classical choice in the mathematical finite-type instance is not a circuit
implementation or permission to evaluate a hidden Q.

The monomial indices identify the existing chart, with
`r*binom(m+D,m+1)` coordinates. The closed binomial count and expanded
matrix-entry formula are explained in the research note, not separately
kernel-checked here. The later full-jet erasure module derives the needed
diagonal/triangular pattern directly from substitution, without assuming
that closed formula. 22 original Python controls compare every matrix basis column
to independent coefficient substitution at degrees 2,3,4 and small/127-bit
primes, check the hidden-coefficient schema, inverse/composition and weight
triangularity, and reject the transpose convention. These are not a formal
refinement of Python into Lean.

The next module derives source-to-common-jet GL alignment from feature
injectivity. The weighted-cancellation module below proves the universal
algebraic law, conditional on generator triangularity. Still open: random
rank probability, executable SDE and quantum circuits, complete recursion
and error composition, independent novelty review, and a useful hard
application. This module proves no speedup.

```text
lake env lean -DwarningAsError=true Formal/FullTaylorTransport.lean
```

## Full-Jet Source Alignment

`Formal/FullJetAlignment.lean` is in the normal build. It evaluates the
auxiliary jet polynomial at public measured Y and chosen s, derives the
full displacement decomposition, and proves that scalar-feature injectivity
lifts through every source map `a -> (a,ell_i(a))`. No nonzero or uniform
central-label premise is needed. This is rank lifting, NOT the probability
of obtaining scalar-feature rank.

| Guarded theorem in `QSearch.FullJetAlignment` | Statement |
|---|---|
| `feature_jet` | Public evaluation of the jet is Q(Y+s*q)-Q(Y). |
| `lift_injective` | Scalar-feature injectivity implies injectivity of the stacked carrier map, for arbitrary ell_i. |
| `split_columns` | A verified public P*T=I gives the exact linear splitting x -> (P*x,x-T*P*x), with T*j -> (j,0). |
| `fullJet_alignment_exists` | Feature injectivity guarantees a left inverse of the full carrier map; neither this map nor the proof uses Q. |
| `fullJet_aligned_displacement` | The split displacement has the SAME hidden jet in its first component and constant spectator component. |
| `conjugation_source` | Actual two-sum density conjugation by the public permutation has exactly the pulled-back phase and correct normalization. |
| `fullJet_source_to_scalar` | Combining that permutation and spectator measurement yields the nonlinear common-jet density for every outcome. |

The splitting is an explicit formula GIVEN a verified left inverse P;
its inverse is `(j,k)->T*j+k`. The existence proof uses standard linear
algebra and classical choice. It is not a formally extracted Gaussian
elimination algorithm. The existing Python pivot-minor implementation
supplies a concrete public certificate, but its equivalence to Lean is
not formally proved. Nor is an unknown polynomial evaluator supplied by
the use of Q as a proof witness.

Six additional exact-arithmetic Python cases check kernel residuals,
alternative public complements, zero/fixed labels, and phase pullback at
small/127-bit primes. A translation-correct alternative alignment with
the old phase is explicitly falsified. These are implementation controls,
not experimental quantum advantage. All seven guards use only standard
Lean axioms; no sorry, custom axiom or native_decide is used.

Remaining: the random feature-rank bound and full probability composition,
SDE execution, complete normal-source/gate
construction and recursive HSP theorem. The connection to the already
checked batch-shear theorem is a written composition, not a single formally
composed theorem starting at the ordinary hiding oracle. No speedup or
useful application is established by this component.

```text
lake env lean -DwarningAsError=true Formal/FullJetAlignment.lean
```

## Weighted Phase Erasure

`Formal/WeightedPhaseErasure.lean` proves the universal filtered-polynomial
law over any commutative coefficient ring R. R can itself contain formal
unknown parameters. A substituted variable of weight w_j must equal
`s^w_j X_j` plus terms of STRICTLY lower weight. For a phase P of weight
at most d, its weight-d coefficients then transform by the common factor
s^d. Offsets and lower-weight terms can vary independently by outcome.

| Guarded theorem in `QSearch.WeightedPhaseErasure` | Statement |
|---|---|
| `pullback_agree` | Substitution agrees with pure diagonal scaling modulo weight <d and preserves the degree bound. |
| `leading_coefficient` | Every weight-d coefficient becomes s^d times the original coefficient. |
| `parameter_relation` | Cancelling every public parameter-lift column cancels their linear combination for ALL parameter values. Products of parameters are allowed. |
| `diagonal_cancellation` | Verified coefficientwise diagonal relations imply the summed pullback has weight <d. |
| `triangular_lower` | An explicitly strictly lower-weight affine substitution meets the generator hypothesis. |
| `triangular_cancellation` | The corresponding family of affine pullbacks cancels at weight d. |
| `affine_cancellation` | The same result from directly checkable matrix conditions: diagonal s^w_j and zero off-diagonal entries at equal or higher column weight. |
| `constant_after_weight_one` | With positive variable weights, weight <1 leaves only a constant phase. |
| `merged_character` | The product of evaluated additive-character phases is exactly the character of the sum of polynomial pullbacks. |

These are algebraic implications, not a new SDE solver or a proof that
fresh independent quantum sources are available. A diagonal relation that
holds only at fitted hidden parameters is insufficient. Matrix triangularity
does not permit equal-weight off-diagonal mixing. Six new exact Python
tests cover full-jet transports at small/127-bit primes with all linear
and quadratic parameter lifts, zero-scale discards, and an equal-weight
mixing counterexample that must fail the degree-reduction check. Hidden
parameter evaluation is forbidden in these controls.

The next module connects actual full Taylor coefficient transport to this
law and to the mixed-channel branch. Physical merge inputs must have
nonzero scales and be fresh independent same-curve sources; the algebra
also allows zero scales, which does not authorize physical zero-scale
transport. Sequential source consumption, SDE selection BEFORE outcomes,
rank probability, efficient implementation and end-to-end composition
remain separate obligations. No algorithm or speedup follows from these
local results. The nine guards permit only standard Lean axioms.

```text
lake env lean -DwarningAsError=true Formal/WeightedPhaseErasure.lean
```

## Full-Jet Erasure Channel

`Formal/FullJetWeightedErasure.lean` removes the matrix premise between
the two previous modules. For an auxiliary monomial Y^alpha s^k,
transport minus t^k times that monomial has only terms with scale power
STRICTLY greater than k. This follows by factoring s^k and applying the
zero-scale projection to the correction of the remaining polynomial.
No finite-field interpolation or closed binomial formula is assumed.

Hence a coordinate of weight k receives only lower-weight coordinates
and itself, with diagonal t^k. The finite index type is EXACTLY the
positive-scale monomials of total degree <=D, not a rectangular degree
box. Reconstruction and coefficient extraction are inverse on this space.
The matrix action is identified with the existing finiteTransport for
ARBITRARY register contents; it is not merely equality on hidden jets.

| Guarded theorem in `QSearch.FullJetWeightedErasure` | Statement |
|---|---|
| `entry_on_or_above` | At equal/higher input weight, the only nonzero matrix entry is the original coordinate scaled by t^k. |
| `reconstruct_coordinates` | The finite coefficient vector reconstructs every element of the actual jet space. |
| `coordinates_transport` | Coefficient extraction of the existing transport equals the derived finite matrix action. |
| `coordinate_point` | Quotient plus vector-jet coordinates give exactly the public affine point used by the channel. |
| `fullJet_cancellation` | Verified leading-coefficient relations reduce weight under the actual Taylor coordinate substitution, with no triangularity premise. |
| `fullJet_lift_cancellation` | Public lift-column relations imply that conclusion for every assignment of unknown parameter values. |
| `degree_reduced_branch` | The actual tensor-input Kraus contraction has the SAME hidden curve, the original normalization, and the strictly degree-reduced polynomial phase. |
| `terminal_kernel` | Weight <1 leaves a constant; for unit additive characters this phase cancels exactly from the density kernel. |
| `active_relation` | At positive degree, restricting a diagonal relation to nonzero scales leaves its sum unchanged. |
| `active_degree_reduced_branch` | A nonzero vector, including zero entries, gives a reduced branch on its nonempty active subtype; normalization uses the active count. |

The original eight guards and the two active-support guards allow only
standard Lean axioms. Two further guards cover
`NonlinearJetChannel.tensor_curve_trace_one` and
`NonlinearJetChannel.discard_independent_curve_sources`: tracing discarded
independent, normalized factors leaves the retained kernel unchanged,
including an empty discarded tensor. This bridges the published solver's
nonzero-VECTOR guarantee to the invertible Taylor channel. No guarantee
that every solver coordinate is nonzero is needed.

Four additional Python
controls independently reconstruct arbitrary register vectors, substitute
their auxiliary polynomials, and compare the ENTIRE symbolic phase
pullback, including lower terms and all parameter-lift types. Hidden
parameter evaluation is disabled. The full-Taylor test file now has 26
cases. These checks are not a formal Python refinement or quantum execution.

The original branch theorem requires a nonempty collection of active
nonzero scales; the new theorem constructs that collection from a nonzero
vector. Both take a tensor product of same-curve sources as their input.
It does not certify their preparation or ownership. Rank probability,
adaptive freshness, all-stage source/error budgets, executable SDE,
efficient gate extraction, recursion, novelty and a useful hard application
remain separate. The finite-type constructions are mathematical, not
instructions to enumerate exponentially many field-valued register states.
The published diagonal-equation solver remains an external dependency,
not a theorem supplied by this bridge. No speedup claim follows.

`tests/test_induced_receiver_composition.py` gives ten independent controls,
including a separable shared-randomness source with correct marginals and
correct branch probabilities but WRONG final Fourier law. Thus those
checks cannot replace the conditional tensor premise. See
`research/INDUCED_RECEIVER_COMPOSITION_THEOREM.md` for the complete written
procedure and explicit boundaries between proof and implementation.

```text
lake env lean -DwarningAsError=true Formal/FullJetWeightedErasure.lean
```

## Equivariant Label Selection

`Formal/EquivariantLabelSelection.lean` checks the conditional label-balance
step used in the class-four source argument, not the entire rank theorem.
It treats finite weighted experiments, so independent solver randomness
need not be uniform and zero-mass acceptance events remain explicit.

| Guarded theorem in `QSearch.EquivariantLabelSelection` | Statement |
|---|---|
| `selected_mass_transport` | Invariant weights/acceptance and an equivariant selector preserve accepted mass under the action. |
| `invariant_event_balance` | Transitivity makes every label's accepted mass equal to total accepted mass divided by label count, in an unnormalized identity. |
| `conditional_label_uniform` | For nonzero accepted mass, the conditional probability is exactly inverse label count. |
| `invariant_record_balance` | Additional record conditioning is valid when the record is itself invariant. |
| `separate_postselection_product` | Product input weights and separate acceptance events factor the joint selected-label mass. |
| `postcompose_kernel` | Invertible postcomposition preserves a linear map's relation kernel. |
| `selected_column_equivariant` | Selecting a column using only that kernel and a seed is equivariant. |
| `block_schedule_bound` | For p>=5, `(p^L-1)*(2/p)^(2L+2)<=1/p`. |

All eight have axiom guards; only standard Lean axioms occur. This does
not establish transitivity of the particular GL action, the hyperplane
count, SDE success/runtime, fresh-source preparation or full quantum
composition. In particular, arbitrary label/rank-dependent postselection
and correlated blocks do not satisfy these theorems' hypotheses. The full
physical transcript is not an invariant record; the rank estimate averages
fresh labels while the source proof retains their actual records.

## Mixed Affine-Support Erasure

`Formal/AffineSupportErasure.lean` formalizes the core channel identity in
`research/CLASS_THREE_HSP_THEOREM_DRAFT.md`. It is imported by `Formal.lean`
and has local axiom guards. The formal objects are finite matrix kernels;
the proof starts from the two sums defining `K_y rho K_y^dagger`.

For a finite vector space V over a field F, a submodule U, and complex
phase functions u_i, define
`rho(U,u)[x,x'] = |V|^-1 [x-x' in U] u(x) conjugate(u(x'))`.
The source in the theorem is explicitly the tensor product of these
kernels. The Kraus operators depend on public scales c and outcomes y,
not on U or the phases.

| Lean name (under `QSearch.AffineSupportErasure`) | Statement |
|---|---|
| `mixed_branch_identity` | If some scale is nonzero, each branch equals `|V|^-k rho(U, product_i u_i(y_i+c_i*x))`, for arbitrary phases and every outcome. |
| `branch_probability` | Unit-modulus phases give the uniform branch trace `|V|^-k`. |
| `kraus_complete` | Summing `K_y^dagger K_y` over all y gives the identity, for every scale tuple, including the all-zero tuple. |
| `all_zero_scale_branch` | With all scales zero, the output has full uniform coherence regardless of U; it does not preserve a proper hidden support. |

All four depend only on `propext`, `Classical.choice`, and `Quot.sound`.
There is no `sorry`, extra axiom, or `native_decide` in this module.
The field and submodule assumptions are essential: this is not a theorem
for arbitrary nonzero multipliers modulo a composite integer.

This is **not** a formal proof of the complete quantum algorithm.
Transport from finite-group presentations to the formal source hypotheses,
polynomial cancellation, independence of the produced sources, recursive HSP
reduction, complexity and circuit compilation are not formalized here.
The kernel's positivity/coset-mixture representation is also not separately
formalized. Normalized traces and algebraic Kraus completeness are proved;
no general density-operator framework is assumed to supply missing claims.
The noncomputable definitions are mathematical specifications, not an
executable quantum implementation. Novelty and applications remain open.

Standalone check:

```text
lake env lean -DwarningAsError=true Formal/AffineSupportErasure.lean
```

## Nonabelian Normal-Group Source

`Formal/CosetMatrixSource.lean` is imported by the normal library build.
The normal coordinate N is a group, not assumed abelian or class two.
Its nine guarded headlines cover the following chain.

| Lean name (under `QSearch.CosetMatrixSource`) | Statement |
|---|---|
| `hiding_output_trace` | The finite output trace of a uniform ordinary query to a coset-separating f gives `|G|^-1 [g^-1*g' in H]`. |
| `section_word_action` | The potential `s(q-pi(q)) h(pi(q)) s(q)^-1` has the required right-action increment for every hidden direction. |
| `potential_in_normal_kernel` | A quotient-compatible section and hidden lift put that potential in the normal kernel. |
| `coordinate_action` | A normal-first chart transports the group-word identity to `(q,n) -> (q+u,n*F(q)^-1*F(q+u))`. |
| `coset_relation` | Actual same-H-coset membership is equivalent to the resulting normal-coordinate relation. |
| `mixed_matrix_identity` | Conjugated Fourier amplitudes and a traced row give `d/|G| [q'-q in U] rho(F(q)^-1 F(q'))`. |
| `normalized_matrix_identity` | Dividing by `d^2/|N|` gives `(|V|d)^-1 [q-q' in U] W(q)^dagger W(q')`. |
| `source_from_normal_chart` | Composes the normal-first chart and hidden homomorphism with the normalized identity; the action law is derived. |
| `sector_trace` | The fixed-sector trace is `d^2/|N|`. |

The section, retraction pi and hidden homomorphism are quantified proof
witnesses, not receiver inputs. The coordinate equivalence and whole-H
parametrization are genuine hypotheses; merely knowing some generators
would not satisfy them. Multiplication order is not interchangeable.

The row-traced proof simplifies to
`sum_i conjugate(rho(n)[i,j]) rho(n*t)[i,k] = rho(t)[j,k]`.
Only representation multiplication and unitarity are needed at this stage.
It does not assume Schur orthogonality, nor claim a maximally mixed row
before the trace. Four purely group-theoretic guards use `propext` and
`Quot.sound`; the five matrix/oracle guards use the standard three axioms.
No `sorry`, extra axiom or `native_decide` is used.

IMPORTANT: a fixed-sector formula does NOT prove that the chosen complete
Fourier family is a valid unitary. A reducible unitary representation can
give d^2/|N|>1 with these coefficients; its putative sector is then not even
a valid Kraus branch. A separate full-QFT completeness/implementation
certificate is required before calling this number a probability.

`tests/test_coset_matrix_source.py` constructs actual cosets in a finite
group with a nonabelian normal subgroup and proper quotient support,
checks a complete QFT and every traced sector, and rejects reversed
multiplication, a conditioned single-coset substitution and a reducible
non-QFT sector. These are reference falsifiers, not algorithm candidates.

Remaining scope: no efficient group-presentation/coordinate compiler,
existence theorem for all required explicit HSP input structures, general
normal QFT circuit or completeness proof, class-four polynomial-degree
certificate, full adaptive composition, runtime or new
algorithm is formalized. The scalar phase source is not assumed, but the
representation/coordinate interfaces must still be instantiated correctly.

```text
lake env lean -DwarningAsError=true Formal/CosetMatrixSource.lean
```

## Complete Right-Abelian Regular Source

`Formal/CentralRegularSource.lean` supplies the different source used by
the full-jet proposal. It does NOT reuse d^2/|N| for a reducible sector.
The historical namespace now uses a public RightAbelianChart identifying
N with T x C, where C is finite abelian and n=section(x)*fiber(z).
The fiber need not be central or normal. Left multiplication's carrier
motion and additive fiber phase are derived from this chart; no
representation law is assumed. CentralChart has an explicit conversion
to a right-fiber chart. The concrete vector-center source now directly
constructs the right chart; no implicit chart coercion is used.

Invert the normal coordinate and use the Kraus amplitudes
`K_chi[x,n]=|C|^(-1/2) [x=pr_T(n^-1)] chi(pr_C(n^-1))`.
The instrument includes ALL complex additive characters of C. Mathlib's
finite-abelian dual orthogonality proves completeness; a full nonabelian
Fourier transform, Schur orthogonality and irreducibility are unnecessary.

| Guarded theorem in `QSearch.CentralRegularSource` | Statement |
|---|---|
| `coordinate_action` | Public right-abelian-fiber coordinates determine the actual left action and additive fiber phase, without centrality. |
| `fourier_complete` | Sum over every character and retained carrier gives the identity on T x C. |
| `instrument_complete` | Completeness still holds after normal-coordinate inversion. |
| `regular_branch` | The actual two-sum Fourier contraction of the right-regular kernel equals the left-action monomial sector, with the correct sign/order. |
| `potential_gauge` | The derived sector is a unitary representation and W(a^-1 b)=W(a)^dag W(b). |
| `sector_trace` | Every fiber-character branch of the transverse ordinary source has mass 1/\|C\|, including the trivial character. |
| `oracle_source_from_normal_chart` | Actual hiding-output trace, the shared section-word potential and right-fiber instrument yield the normalized regular-sector source; the coordinate action is derived. |

The operational side of the last theorem uses only the ordinary hiding
function, public charts, inversion and Fourier amplitudes. The hidden
subgroup parametrization, linear retraction and shared potential are proof
witnesses. The theorem still requires those witnesses to describe the
entire transverse hidden subgroup and the verified normal-first chart.
It does not turn hidden potential evaluation into available advice.

Three new tests construct actual coset labels with a nonlinear public
section and proper quotient support, then compare transformed equality
tables at two different hidden retractions. They cover class-three,
vector-center and abelian controls, every central character, cross-sector
zeros and normalization. Omitting inversion or using d^2/|N| is rejected.
A fourth test shows that a nontrivial hidden central intersection destroys
uniform label probabilities. Transverse preprocessing is not optional.
These are finite correctness controls, not new oracle candidates.

`Formal/InducedRegularSource.lean` adds the exact interface to the new
induced-phase compiler. An AdditiveChart supplies the public quotient
homomorphism and its coordinate projection, not a homomorphic section.
Its translation law, cocycle composition and phase unitarity follow.
`oracle_to_matrix` matches the actual ordinary-oracle branch to
WeylSourceScalarization.matrixSource, keeping the factor 1/|C|.
`oracle_aligned_to_scalar` includes the public GL permutation and actual
spectator Kraus sums; it derives the NEGATIVE cocycle phase and factor
1/(|C|*|spectator|). Hidden potentials are theorem witnesses only.

The module has a genuinely noncentral vector-BCH instantiation with
fiber B+C, coordinates (a,(b,c-delta(a,b)/2)), and an explicit noncentrality
witness whenever delta(a,b) is nonzero. This is distinct from the older
central-only source. Exact Python phase-count tests additionally compose
original hiding labels, independent-copy batch shear and the public
higher-degree compiler. See research/RIGHT_FIBER_SOURCE_REFINEMENT.md.
General Lie/Lazard compiler refinement, the full adaptive receiver,
resource guarantees and coherent synthesis remain separate obligations.

Seven guards allow only standard Lean axioms; coordinate_action needs
only propext and Quot.sound. No general positivity library or extracted
gate implementation is supplied. Completeness is an exact amplitude
identity. For the intended explicit F_p^z center, efficient approximate
Fourier gates and their joint error budget are separate implementation
obligations. The abstract finite-character type is not a proposal to
enumerate all field elements at runtime.

Remaining: deriving all public charts and polynomial/parameter-degree
bounds from the input Lie algebra, the combined extra-B-Fourier/compiler
bridge, rank probability, adaptive source ownership and the complete
resource/error/recursion theorem. This does not certify the older
irreducible-family QFT or the whole HSP algorithm. Coset-state Fourier
analysis is prior art, not a discovery attributed to this formalization.

```text
lake env lean -DwarningAsError=true Formal/CentralRegularSource.lean
```

## Complete Retained B Fourier Transform

`Formal/RetainedFourier.lean` identifies the compiler's linear frequencies
mu:B->F with ALL complex additive characters of B. A fixed nontrivial
base character chi suffices: equality at t*y for all t and character
primitivity prove injectivity, then finite dual cardinalities give
surjectivity. Pointwise injectivity of chi is not assumed, so this also
works over extension fields. Zero-dimensional B is allowed.

The amplitudes `K[mu,y]=|B|^(-1/2)*conjugate(chi(mu(y)))` have both row
and column orthogonality. The actual two-sum conjugation of the BCH
coordinate product yields precisely the class-three compiler's translation
and phase. In particular the scalar correction uses OUTPUT frequency
nu=mu+delta(a,-)/2, not mu. This is a coherent basis change, not a
measurement or postselection on a useful frequency.

| Guarded theorem in `QSearch.RetainedFourier` | Statement |
|---|---|
| `linearCharacter_injective` | Nontrivial field character separates linear functionals via scaled inputs. |
| `linearCharacter_bijective` | Every additive character occurs exactly once. |
| `columns_orthonormal` | Full-frequency transform preserves all input inner products. |
| `rows_orthonormal` | Its coherent output basis is orthonormal. |
| `coordinate_action` | Modulation and B translation follow from actual BCH multiplication. |
| `branch_formula` | Actual two-sum conjugation has shifted-frequency phase. |
| `classThree_formula` | The BCH-source contraction equals the existing compiler's displacement and phase. |
| `trivial_character_columns_equal` | A trivial Fourier base character collapses columns. |

The fixed base character chi is NOT the measured central label lambda.
Lambda=0 stays valid; it simply zeros scalar-projected structure maps.
No characteristic premise of the physical HSP proposal is weakened.
Seven independent Python controls include actual gH sources with class-three
N and one- or two-dimensional centers, all-coherent C/B transformations,
zero central labels, dropped-frequency and wrong-phase mutations. Measuring
mu changes a genuine source block. These are finite checks, not Python
refinement proofs or input-model certification for the full proposal.

See `research/RETAINED_FOURIER_SOURCE.md` for scope and the correction to
the earlier circular potential-kernel source fixture. Still missing is
the batch-shear/GL/phase-compiler composition, adaptive
freshness/rank/error/resource composition, effective SDE execution, and
a useful hard application or independent novelty validation.

```text
lake env lean -DwarningAsError=true Formal/RetainedFourier.lean
```

## Vector-Center Original Source Composition

`Formal/VectorCentralSource.lean` constructs the actual group A x B x C
from vector-valued structure maps and Jacobi. Scalar projection through
lambda preserves multiplication, but is NOT assumed faithful. All linear
functionals together separate vectors, allowing reuse of the checked
scalar associativity theorem. Identity and inverse are checked directly.

The public central chart, section and central embedding are constructed,
not supplied as an unverified promise. Projected sectors agree with their
scalar BCH formulas, and the complete physical central instrument is
reindexed by all linear labels, including zero. The coherent B contraction
is a derived unitary representation with the correct potential gauge.

`original_source` starts with the actual hiding-output trace and composes
the central and B transforms. Its result is
`|C|^-1 [r-q in U] (|V||A||B|)^-1 (W(g(q))^dag W(g(r)))[t,t']`.
The operational definition contains neither the hidden subgroup nor the
potential. The common retraction/lift/potential remain correctness witnesses
for the ambient normal-first chart. The prefactor retains the FULL C even
at lambda=0. `carrier_card` proves |A x B*|=|A x B|.

Ten standard-axiom guards cover scalar product/separation, cardinality,
group associativity, sector projection, the retained formula, complete
central indexing, representation unitarity, potential gauge and the
original-source theorem. Four exact Python controls include vector-center
projection at small/127-bit primes and a bad Jacobi tensor hidden by its
zero-character projection. Existing genuine-coset controls are reused.

This does not certify that an arbitrary ambient Lie input has this chart,
that C is its full Z(N), or that the chosen N is L'. Those are distinct
input/degree obligations. Neither full adaptive protocol composition nor
an efficient executable receiver is established. See
`research/VECTOR_CENTRAL_ORACLE_SOURCE.md` for the precise boundary.

```text
lake env lean -DwarningAsError=true Formal/VectorCentralSource.lean
```

## Weyl-Matrix Source Scalarization

`Formal/WeylSourceScalarization.lean` checks the measurement interface in
`research/CLASS_FOUR_VARIABLE_RADICAL_SOURCE.md`. It is imported by the
normal library build and carries seven local axiom guards.

For a quotient space Q and carrier C, define the monomial gauge explicitly:
`W(q)[r,t] = [r=A(q)+t] gamma(q,t)`. The unit-modulus phase gamma includes
the symmetric-Weyl scalar and Z action, not just the central character.
The matrix source is
`(|Q| |C|)^-1 [q-q' in U] (W(q)^dagger W(q'))[t,t']`.

Split C=J x S, where J is retained and S is measured. The critical hypothesis
is `A(q)=(a+Tq,b)` for a linear T and CONSTANT spectator displacement b.
The source and branch are defined using actual finite matrix products and
the two sums of `K_s rho K_s^dagger`; the target scalar identity is not
assumed. The measurement operators contain neither U nor gamma nor T.

| Lean name (under `QSearch.WeylSourceScalarization`) | Statement |
|---|---|
| `gauge_isometry` | The explicit monomial W satisfies W^dagger W=I when gamma has unit modulus. |
| `matrix_source_to_scalar` | Every branch is `|S|^-1 rho(graph(-T on U), conjugate gamma restricted to s)`. |
| `matrix_source_with_leakage` | If spectator displacement is b+Lq instead, the support becomes graph(-T on U intersect ker L). |
| `spectator_probability` | Every spectator outcome has probability `|S|^-1`, including nonzero outcomes. |
| `spectator_complete` | The spectator Kraus family is complete, independently of the source. |
| `full_carrier_support` | Measuring the entire affine carrier preserves only U intersect ker T, not generally U. |
| `full_carrier_measurement_dephases` | An injective X displacement makes full-carrier readout entirely diagonal on Q. |

All seven guards permit only `propext`, `Classical.choice`, and `Quot.sound`.
No `sorry`, extra axiom or `native_decide` is used. There is no small-prime,
bounded-dimension or full-support hypothesis. The phases need not be
polynomials. The normalized output has exactly the `rho` type consumed by
`AffineSupportErasure`; its graph support depends on U,T, not on spectator
outcome, carrier width, affine constants or gamma. Across separate packets,
the SAME U,T remains a protocol premise, not a result of compatible types.

The theorem starts from the displayed matrix source and affine displacement.
It does NOT formalize the normal-group QFT/Schur conversion, the batch shear,
the Clifford realization or its covariance phases, the common hidden
polynomial potential, degree bounds, diagonal solvers or end-to-end runtime.
Positivity and the full group-source transport are not separately proved
here. The preceding matrix-source module checks the row-traced group
conversion under its explicit coordinate/representation hypotheses; the
complete pipeline is not composed in Lean. No new algorithm, novelty or
external application is certified.

Independent Python controls include a proper hidden support and a leaking
spectator. Leakage can destroy the entire hidden direction while all outcome
probabilities remain uniform: normalization alone is not a validity test.
The generalized formal identity makes the exact condition explicit:
the measured displacement must vanish along U. Global L=0 is a sufficient
publicly certified condition; claiming merely that L has low rank is not.

```text
lake env lean -DwarningAsError=true Formal/WeylSourceScalarization.lean
```

## Matrix Batch Shear And Alignment Interface

`Formal/MatrixBatchShear.lean` is in the normal build with eight axiom
guards. It generalizes the scalar shear to independent matrix sources
with one common U and arbitrary DIFFERENT finite carrier types C_i.
The Kraus operator is the fresh uniform-Q preparation, quotient shear,
measurement of all old quotients and identity on all carrier registers.
It contains no U, gauge matrices or hidden coefficients.

| Lean name (under `QSearch.MatrixBatchShear`) | Statement |
|---|---|
| `mixed_branch_identity` | The two Kraus sums give `|Q|^-n matrixSource(U, tensor_i W_i(y_i+c_i q))` for every y, if some c_i is nonzero. |
| `branch_probability` | Every full outcome has probability `|Q|^-n` for unitary input gauges; thus the recorded y_i are independent uniform conditional on a fixed product-source transcript. |
| `kraus_complete` | The entire instrument is trace-preserving, even for all-zero weights and arbitrary input states. |
| `all_zero_scale_branch` | All-zero weights produce full-support uniform quotient coherence tensored with the mixed carrier, not the unknown U. |
| `combined_isometry` | The tensor gauge is an isometry when each input gauge is. |
| `aligned_branch_identity` | Actual carrier conjugation after the batch gives the conjugated tensor-gauge source, with the same branch factor. |
| `carrier_conjugation_identity` | Physical double-sum conjugation by C is represented by W(q) -> C W(q) C^dagger. |
| `conjugation_to_scalar` | Given the EXACT aligned monomial gauge, carrier conjugation and spectator Kraus sums compose to the existing scalar graph-support kernel. |

The shared generic kernel is exactly `W(q)^dagger W(q')`; a definitional
bridge identifies the monomial source with `WeylSourceScalarization`.
`zero_weight_kernel` shows that an inactive input contributes an identity
carrier factor. Discard it or measure it as specified; it is not reusable
source material. If inactive inputs are discarded before the shear, n in
the outcome law counts only the active inputs.

All eight guards allow only `propext`, `Classical.choice`, `Quot.sound`.
The aligned-gauge equality is an explicit hypothesis, NOT inferred from
the public finite-field symplectic matrix or a rank check. This module
does not construct that Clifford, establish its Weyl phases or synthesize
gates. Padding, carrier-index reordering, degree cancellation, common
hidden-parameter provenance and the complete adaptive algorithm are not
all composed in Lean. No algorithm or speedup claim is admitted.

Outside Lean, `theorems/prime_clifford_realization.py` now constructs an
O(R^2)-primitive public gate plan with exact symmetric-Weyl covariance;
see `research/PRIME_CLIFFORD_REALIZATION.md` for the universal argument
and independent finite controls. This does not discharge the formal
premise by itself and is not a certified native-qubit compiler.

`tests/test_matrix_batch_shear.py` independently contracts sparse Kraus
operators and checks the physical three-stage composition. Countercontrols
show that correct marginals do not imply independent copies; differing
supports intersect; a mixed rather than coherent fresh register destroys
support despite uniform outcomes; and a reused old pivot has a different
outcome law. These reject incorrect interfaces, not the intended algorithm.

```text
lake env lean -DwarningAsError=true Formal/MatrixBatchShear.lean
python -m pytest -q ../tests/test_matrix_batch_shear.py
```

## Common Quadratic Jet Across Batches

`Formal/CommonQuadraticJet.lean` derives the shared hidden support needed
when scalar packets from different variable-radical batches are merged.
For one fixed proof-only potential Q(q)=a+L(q)+B(q,q), define
T(q)=(L(q), B(q,-)+B(-,q)). The second component is a linear map, not an
exponential function table; in a fixed m-dimensional basis it has m blocks.

| Lean name (under `QSearch.CommonQuadraticJet`) | Statement |
|---|---|
| `quadratic_translation` | Expands Q(y+s*q) into its constant, linear-jet and s^2 quadratic pieces for any bilinear B. |
| `displacement_decomposition` | The actual sum of shifted public carrier maps equals v(0)+J(Tq)+K(B(q,q)). |
| `aligned_displacement` | Public AK=0 and AJ=E imply A(v(q))=A(v(0))+E(Tq); the target affine law is derived. |
| `aligned_difference` | Displacement differences depend only on T and the fixed embedding E. |
| `different_batches_same_jet` | Different transcripts, source counts and carrier spaces give the same derivative. |
| `retained_and_spectator` | For E(j)=(j,0), the retained map is T and spectator displacement is constant. |
| `quadratic_source_to_scalar` | Composes that derived law with the spectator Kraus theorem, giving the same graph(-T on U). |

Seven local guards restrict axioms to subsets of propext, Classical.choice,
Quot.sound. The unknown L/B/T are proof witnesses, not controller inputs.
The scalarization result uses exactly the prior kernel definitions. It
still assumes a common quadratic potential and the public alignment
identities. It does not derive them from the hiding oracle, construct the
Clifford unitary, prove a polynomial-degree erasure theorem, or establish
independence of physical sources from packet metadata. Those are distinct
obligations. No full HSP algorithm or novelty is certified.

Independent Python controls cover mixed multivariate terms, variable
carrier sizes and a 127-bit prime. Changing the hidden chart while keeping
the entire public transcript fixed changes the graph support. A second
countercontrol rejects a cancellation valid at only one truth assignment.

```text
lake env lean -DwarningAsError=true Formal/CommonQuadraticJet.lean
python -m pytest -q ../tests/test_common_quadratic_jet.py
```

## Group-Coset Fourier Source

`Formal/CosetSourceFourier.lean` is also imported by `Formal.lean`.
It does NOT assume the desired phase-kernel density formula. Its explicit
input hypotheses are a coordinate equivalence `G ~= V x N`, a bijective
parametrization of the whole hidden subgroup by a submodule `U`, and
the right-action identity

```text
coordinates(coordinates^-1(q,a) * h(u))
  = (q+u, a+Q(q+u)-Q(q)).
```

Starting from `|G|^-1 [g^-1*g' in H]`, the two normal-register Fourier
sums are evaluated using a unit-modulus additive character, with the
positive Fourier sign and all normalization factors retained.

| Lean name (under `QSearch.CosetSourceFourier`) | Statement |
|---|---|
| `coset_relation` | Actual same-H-coset membership is equivalent to `q'-q in U` and `b-a=Q(q')-Q(q)`. |
| `mixed_source_identity` | Each unnormalized character block equals `|N|^-1 rho(U, chi composed with Q)`. |
| `label_probability` | Each block has trace `|N|^-1`, including the trivial character. |

The first theorem uses only `propext` and `Quot.sound`; the other two
use the standard three axioms. All have local guards. There is no
`sorry`, extra axiom, or `native_decide`.

This certifies the GROUP-RELATION-TO-KERNEL calculation under the stated
action law. The next module proves its class-three Lie-algebra mechanism,
but the finite-group/Lazard transport and construction of the concrete
coordinate equivalence and hidden parametrization are not yet composed
in Lean. This also does not certify physical source preparation, positivity
representation, the complete character QFT, complexity, or a full
arbitrary-H dispatcher. `Q` need not be polynomial for this identity.
The unknown parametrization and potential are proof witnesses, not
efficiently supplied receiver data. The full general-H reduction and
its finite controls remain separate.

Standalone check:

```text
lake env lean -DwarningAsError=true Formal/CosetSourceFourier.lean
```

## Universal Class-Three Potential

`Formal/ClassThreePotential.lean` uses Mathlib's ordinary `LieRing` and
`LieAlgebra` axioms over a field. The class-three premise is
`[x,[y,[z,w]]]=0` for every four inputs. The normal space is DEFINED
as the linear span of all brackets. Its abelianness and the vanishing
of `[L,[L,N]]` are proved, not assumed.

| Lean name (under `QSearch.ClassThreePotential`) | Statement |
|---|---|
| `chart_product` | The truncated BCH expression gives the normal-first chart product with the stated `Phi` and cubic cocycle. Requires `2 != 0` and `3 != 0` in the field. |
| `potential_increment` | For commuting lifts `u+a` and `v+b`, the explicit potential has exactly the required increment. Projected `u,v` need not commute. |
| `section_right_action` | A single pair of proof-only linear maps, projecting onto U and lifting its normal coordinates, gives the log-coordinate right-action law for every ambient point and hidden direction. |
| `section_cubic_decomposition` | The potential equals a linear map plus diagonal evaluations of BUNDLED bilinear and trilinear maps. This is a structural polynomial-degree certificate, not finite interpolation or a scaling test. |

All four headline theorems have local guards permitting exactly
`propext`, `Classical.choice`, and `Quot.sound`. There is no `sorry`,
extra axiom, or `native_decide`. Characteristic restrictions are explicit;
this is not a characteristic-zero proof being silently reused modulo p.

The projection fixes U, the normal lift takes U into the derived space,
and the lifted elements commute. These are declared structural premises.
The source theorem's increment identity is now a CONCLUSION of the Lie
calculation, not one of these premises. The degree certificate does not
formalize a particular monomial-coordinate encoding or its resource cost.

Remaining formal boundary: no BCH group instance/Lazard equivalence is
constructed here; nor are the public normal-word conversion, existence
of the hidden linear graph from an actual group H, normalizer reduction,
diagonal solvers, or full quantum algorithm machine-checked. These are
not excused by the successful library build. The existing finite
controls separately test that genuine non-split, higher-rank examples
satisfy the structural premises.

```text
lake env lean -DwarningAsError=true Formal/ClassThreePotential.lean
```

## Balanced Signed MPI

`Formal/BalancedSigned.lean` checks the algebraic core of
`research/BALANCED_SIGNED_MPI.md`. It is included in the normal library build
and in `Formal/Audit.lean`. No change to the pinned toolchain is needed.

| Lean name (under `QSearch.BalancedSigned`) | Statement |
|---|---|
| `rational_separation` | Two ratios of root products with equal values at more points than either cross-product degree have the same signed root multiplicities. |
| `box_injective` | Positive/negative root budgets `(a,b)` give injectivity at more than `a+b` distinct, pole-free evaluation points. |
| `positive_readout_separation`, `negative_readout_separation` | Adding one positive or negative frequency is safe at more than `a+b+1` evaluation points, including repeated roots and cancellation. |
| `integer_label_encoding`, `integer_label_separation` | Injective support points encode actual integer arrays, not merely an abstract ratio; asymmetric budgets give the corresponding separation theorem. |
| `budget_guard_iff` | The implementation's integer guard `a+b+moment+1 <= n` is equivalent to the strict root-count bound. |
| `readout_guard_counterexample`, `counterexample_points_valid` | A concrete repeated-root readout alias over `ZMod 11` at three distinct, pole-free evaluation points. The extra coordinate cannot simply be dropped. |

All nine listed theorems depend only on the standard three axioms checked
by the existing audit. This is **not** a formal proof of the full quantum
algorithm. The discrete-log/syndrome bridge, cyclic Fourier orthogonality,
state preparation, numerical mean certificate, decoder implementation and
complexity are not formalized here. In particular, this build does not
establish a quantum speedup or a classical lower bound.

## Exterior-Power Results

In the table, z stands for −t: the code's `∏(1 − (−z)^ℓ)` is the note's
`∏(1 − t^ℓ)`. L is the list of cycle lengths, and n is their sum.

| Lean name | Statement | Note |
|---|---|---|
| `permDet_eq_mul_stdDet`, `one_add_X_dvd_permDet` | `∏(1 − (−z)^ℓᵢ) = (1 + z)·stdDet L` in `ℤ[z]`. So `1 + z` divides the product. | 47, 56-57 |
| `stdDet_unique` | The quotient is unique. | 56-57 |
| `stdDet_eval_neg_one` | At `z = −1` (that is, `t = 1`) the quotient is `n` for one cycle and `0` for two or more. | 49 |
| `cycle_indicator`, `cycle_indicator_of_eq` | `∑_{j<n} (−1)^j χ_j = n·[c = 1]` for the integer coefficients `χ_j`, with all `ℓᵢ ≥ 1`. | 52-54 |
| `stdDet_coeff_zero` | `χ₀ = 1`. | 52-54 |
| `perm_cycle_indicator` | The same identity for any `σ : Perm (Fin n)`, using `σ.partition` (cycle lengths, fixed points included). | 44-54 |
| `ofCoeffList_extCharsList`, `stdDet_coeff_eq`, `altSum_extCharsList` | A computable list version of the Python algorithm, proved equal to the polynomial's coefficients. | 56-58 |
| `exterior_std_no_invariants`, `extStdRep_invariants_eq_bot`, `sum_map_stdRep_eq_zero` | Over any characteristic-zero field and for every `j ≥ 1`, `Λ^j V_std` has no nonzero `S_n`-invariant vector. | 60-66 |
| `trace_stdRep`, `stdDet_coeff_one`, `quotient_coeff_one_eq_trace` | Only the `j = 1` case of milestone 2: `χ₁` equals the trace of `σ` on `V_std`, which is the number of fixed points minus 1. | 52-56 |
| `traceBound_ge_inv_two_n`, `exterior_threshold_suffices` | If `p > 0`, `p ≥ 16A²` and `p ≥ 4(R + A)`, then `max(0, (p + 1 − R − A⌈√p⌉)/(n p)) ≥ 1/(2n)`. The second theorem takes `R = n + b` and `A = (R − 2)(2^(n−1) − 1)`. | 104-106, 119-121 |
| `A_mul_sqrt_le`, `four_A_mul_ceilSqrt_le` | The intermediate steps `A√p ≤ p/4` and `A⌈√p⌉ ≤ p/4 + A`. | 123 |
| `ceilSqrt_eq_ceil_sqrt` | Python's `isqrt(p) + [isqrt(p)² ≠ p]` is exactly `⌈√p⌉`. | 106, 110 |
| `sum_choose_Ico` | `∑_{j=1}^{n−1} C(n−1, j) = 2^(n−1) − 1`, the Python `rank_sum`. | 105 |
| `irreducible_rate_ge_traceBound` | The summation step: `I/p ≥` the trace bound, **if** the imported inputs are taken as hypotheses (the indicator summed over fibers, `#U ≥ p + 1 − R`, and `|S_j| ≤ (R − 2)C(n−1, j)√p`). | 99-106 |

The milestone-3 proof averages over `S_n` instead of extracting
coefficients. On a wedge of distinct basis vectors `bᵢ = eᵢ − e_n`, some
transposition acts by −1. For `j ≥ 2` it swaps two factors. For `j = 1` it is
`(i n)`. So the operator `∑_σ Λ^j(σ)` is zero, and an invariant `x` satisfies
`n!·x = 0`.

## What is not proved, and why

- **Milestone 2 in full is not proved.** The missing statement is that
  `det(1 + zσ)` on the permutation representation equals `∏(1 − (−z)^ℓ)` over
  `σ`'s cycle type, together with `χ_j = Tr(σ | Λ^j V_std)` for every `j`.
  Only `j = 1` is done (above). Mathlib `v4.35.0` has no lemma for any of these
  three pieces:
  1. the determinant or characteristic polynomial of a permutation matrix in
     terms of `cycleType`. Mathlib has only `det_permutation`
     (det = sign) and `trace_permutation` (trace = number of fixed points);
  2. `det(1 + z f) = ∑_j tr(Λ^j f) z^j`, which links the determinant to traces
     on exterior powers. The pieces exist (`Module.Basis.exteriorPower` and
     `Matrix.charpoly_coeff_eq_sum_minors`), but they are not connected;
  3. a `LinearMap` version of "charpoly = charpoly on an invariant subspace ×
     charpoly on the quotient". Only matrix block versions exist
     (`Matrix.charpoly_fromBlocks_zero₂₁`, `BlockTriangular.charpoly`).

  A workable plan is to decompose by orbits and compute one cycle's
  determinant (by Laplace expansion, or by the minimal polynomial `X^ℓ − 1`).
  That is several hundred lines, beyond this spike.
- **The A_n countermodel (note, lines 68-70)** is not formalized.
- **The étale-cohomology trace bound (note, lines 74-97)** was out of scope. In
  `irreducible_rate_ge_traceBound` its consequences are hypotheses, not
  theorems.
- **The `p ≥ 2·D_bad` part of the Python threshold (note, line 124)** is about
  the number of geometry trials, not about the trace bound. It is not
  formalized.

## Cross-check against the Python code

`scripts/gen_crosscheck.py` reads `exterior_characters` from
`theorems/prime_character_exterior_bound.py` with Python's `ast` module and
runs only that one function. The script does not import the module. It writes
`Formal/CrossCheck.lean` with the Python output for **all 44 cycle types of
n = 1, …, 7**, and records the source file's SHA-256 (`a935cb08…`).

The Lean side checks the data in three ways:

- `extCharsList_eq_python` (`by decide`, checked by the kernel): the Lean list
  algorithm gives exactly the Python lists for all 44 cycle types.
- `stdDet_eq_python` and `stdDet_coeff_eq_python`: therefore each Python
  `chars[j]` is the `j`-th coefficient of the polynomial `stdDet L` that the
  theorems above are about.
- `python_cycle_indicator` (`by decide`): every Python row has alternating sum
  `n` for one cycle and `0` otherwise.

A compiled `#eval` of the same comparison prints `true` during the build.

Result: all 44 rows agree, with no mismatches. Some sample rows:
`[3,2,1] ↦ [1,0,-1,1,0,-1]`, `[2,2,2,1] ↦ [1,0,-3,0,3,0,-1]`,
`[7] ↦ [1,-1,1,-1,1,-1,1]`.

# Rees Recursive Source Conversion

2026-10-24. A conditional mathematical source-conversion theorem, not an
executed quantum algorithm, an efficiency certificate or a novelty claim.

## Scientific Question

The quotient-chain pass constructed real public groups and sections, but
did not establish that the measured output of each stage could actually
feed the next. The independent review required complete measurement
records, fresh independent packets, and multiplicative source costs. A
correct single-register marginal was explicitly insufficient.

This pass closes that specific composition gap. It does not substitute
another assumed cancellation certificate for the actual Rees geometry.

## Checked Construction

Write A_d for the original Rees cover modulo grades above d, H_d for the
actual image of its hidden subgroup, and rho_d for its normalized mixed
coset source. The ambient input is still a finite Lie algebra with a
supplied compatible polynomial group law. The intended prime-field Lazard
application needs the separate subgroup-correspondence promise.

`ReesStageInstrument.lean` constructs the additive central-kernel embedding
for A_(d+1) -> A_d and proves its image is exactly the factor-map kernel.
It proves that the quotient relation induced by the public zero-padding
section is membership in H_d. Kernel scaling, hidden-image preservation
and nonzero moment cancellation construct the previous generic certificate.
Zero scales use identity actions, never a zero dilation automorphism.

The physical formula first measures each target on BOTH sides by its
central-character projector. A fresh uniform address then controls the
appropriate right-regular target permutation, and the targets are traced
out. Inputs are explicitly a tensor product of separately prepared target
states. The operational functions contain no hidden-subgroup parameter.

For every label tuple ell, including zero-probability tuples, the output is

    output_ell = mass_ell * rho_d.

`mass_ell` is the product of the actual measured branch traces, not an
assumed reciprocal character count. The complete family sums to total mass
one. No division by a rare branch probability appears in any proof.

`ReesRecursiveSource.lean` applies these ACTUAL Rees maps at every node of
a fresh-source tree. It checks both:

- every fixed complete transcript gives rho_d times the product of its
  actual unnormalized branch weights;
- summing outcomes at each node gives exactly rho_d recursively.

The recorded and averaged statements are separate exact matrix-entry
identities. There is no claim that arbitrary correlated source banks or
record-dependent register reuse are valid. Fixed public measurement plans
are used; a more general adaptive scheduler is not formalized.

## Charged Resources

For packet arities M_k, one source at stage d prepared from stage top needs

    L(d,top) = product_(d <= k < top) M_k

fresh top-stage copies. This is machine-checked, including nonempty packets
derived from the plan's nonzero-witness requirement. Identical subtrees
still pay separately; algebraic equality of density matrices is not cloning.

For top=n and d=1, an original Rees source costing n original source
preparations gives n * product_(1 <= k < n) M_k original preparations per
terminal copy. This last substitution uses the separately specified native
source protocol, not a newly formalized native-to-top channel. Final
Fourier recovery needs additional independent terminal copies.

Polynomial arities at fixed depth would give a polynomial copy bound. This
is not a proof of polynomial total time: it leaves the actual arity bounds,
solver implementation, reversible arithmetic, measurement realization,
coherent workspace, and error/abort accounting to discharge. Growing class
must not be treated as fixed class.

## Imported Obligations

`MeasurementPlan` is public data, not a procedure proven to construct it.
It explicitly requires a unitary additive character, a complete central
character family and, for every label tuple, a NONZERO vector of scales
whose degree-(d+1) moment vanishes. These are genuine remaining algorithmic
obligations. No complete solver or Fourier transform is extracted by Lean.

The plan does NOT assume the desired source/channel identity, hidden
subgroup, allowed-label set, or cancellation certificate. Those conclusions
are derived from the imported data and the constructed geometry.

The actual source at the tree's top is supplied. The native hiding-function
or mixed-coset acquisition channel, final annihilator sampling/nullspace
recovery, base BCH theorem and coherent compiler are not formalized by this
pass. Classical.choice/propext/Quot.sound are permitted foundations; all
other axiom dependencies, including sorryAx, fail the scoped verifier.

Primary dependencies remain [Ivanyos--Santha](https://arxiv.org/abs/1503.09016)
for fixed-degree diagonal systems and [Imran--Ivanyos](https://arxiv.org/abs/2304.08376)
for the existing central-quotient HSP strategy with its bounded-prime
qualification. These citations are dependencies, not a novelty certificate
for our construction. A fresh independent review of these new Lean modules
has not occurred; the prior review supplied the requirements.

## Adversarial Assessment

The new counterexample has two target sources with identical I/2 marginals.
One is independent; the other has shared classical phase records (or can
instead be entangled). The same controlled X tensor X operation produces
address outputs at trace distance 1/2. Thus even separable correlation can
break the product-source argument. This is a falsifier of an invalid
interface, not a candidate oracle problem or a quantum advantage experiment.

The central danger is still a correct conditional construction with no
efficient, new and useful application. Existing exposed-polynomial,
power-product and pencil-norm classical attacks remain in force. Passing
this proof audit establishes neither classical hardness nor Shor-level
significance. More theorem counts are not the research objective.

Next mathematical priorities: review the total resource bound against the
precise diagonal-system theorem; close native-to-top acquisition and final
recovery without hiding access costs; then revisit an explicit natural
application under the same-input classical attacks. Do not extend this
formalization indefinitely without that application/novelty comparison.

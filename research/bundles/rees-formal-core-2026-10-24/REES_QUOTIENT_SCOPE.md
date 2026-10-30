# Concrete Rees Quotient Chain

2026-10-24. Local machine-checked algebra supporting the proposed HSP
reduction, not a new executed quantum algorithm or novelty certificate.

## Question And Decision

Can the first verified central conversion be repeated on genuine public
quotients, with the correct hidden images and a final copy of ALL original
hidden directions? Or does the argument quietly reuse invalid evaluation
maps or recover only the abelianization?

The preceding cancellation pass made progress but checked one top layer.
This pass inspected its code, the earlier independent review, the current
research-priority record and the HDQI/OPI/BPQM alternatives. Those other
routes still need a surviving native source/output or must avoid established
classical/published reductions. The concrete Rees quotient interface was
selected as the next missing part of an actual end-to-end proposal, not as
a standalone theorem-count target.

Input: an explicit finite prime-field nilpotent Lie algebra of class below
the characteristic, with the supplied base BCH law and a genuine coherent
hiding-function evaluator or the separately specified independent mixed
coset-state supply. A hidden Lie subalgebra h is proof data, never supplied
to operational maps. The intended advantage is the still-conditional
fixed-class polynomial-resource HSP reduction in dimension and log p.

Existing classical filters still apply to any proposed explicit application:
small orbit modules, exposed low-degree polynomials, power products and
guarded pencil norms are not hard merely because an orbit or formal degree
is large. This proof supplies no classical lower bound or natural hard input.

## Actual Objects And Theorems

Let A be the ORIGINAL evaluation realization of the Rees cover. Define
J_(>d) by vanishing coefficient grades 1 through d. Indices in Lean are
zero-based, so lowKernel d tests coefficient index j < d.

- tailIdeal constructs J_(>d) as a Lie ideal of A. bracket_tail_raise proves
  [A,J_(>d)] is contained in J_(>d+1). The ideals run from all of A at d=0
  to zero at d=n. This is not assumed as a graded-algebra interface.
- Actual quotient Lie algebras A/J_(>d) and their surjective factor maps are
  constructed. Factor maps compose and carry the actual hidden image to
  the next actual hidden image.
- Quotient equality is exactly equality of retained coefficients. A public
  section zero-pads the higher coefficients. Quotient.lift proves it is
  well-defined without selecting arbitrary representatives or using hidden
  data. Imported interpolation may still depend on Classical.choice in Lean;
  no efficient program extraction is claimed. The section is not asserted
  to be a group homomorphism.
- Graded dilations descend to actual Lie automorphisms, preserving every
  hidden image. The kernel of each adjacent factor is central and the
  dilation acts on it by the correct scalar a^(d+1).
- imageGroup constructs a group law on any surjective Lie image of the
  supplied polynomial group law. Associativity, identity and inversion are
  derived through the surjection. The quotient group laws therefore do NOT
  require a fresh BCH existence assumption at every stage.
- stageGroupProjection, stageGroupFactor and stageGroupDilation are actual
  group homomorphisms/equivalences. The stage group laws have the same
  finite Lie expression as the supplied base law. Hidden group images,
  central group kernels and their scalar action are checked.
- The terminal stage has additive group multiplication. Grade-one inclusion
  gives a bijection from the WHOLE original L, and its hidden image contains
  that image of v exactly when v belongs to h. It does not replace h with
  its image modulo [L,L].

The new module contains 38 theorem declarations and26 explicit definitions.
These are universal symbolic checks, not extrapolations from finite fields.

## Decisive Falsifier

truncated_evaluation_impossible rules out reusing nonzero evaluation on the
degree-one quotient of a nonabelian input. That quotient is abelian. A Lie
homomorphism taking every grade-one v to a*v would force
a^2*[x,y]=0 for all x,y. Nonzero a over a field contradicts any nonzero
bracket. Thus the valid original evaluation lift must not be confused with
later truncated stages. The implementation uses quotient projections there.

## Assumptions And Remaining Work

The original PolynomialGroupLaw is still supplied. Nothing here derives
the base Lazard/BCH theorem from raw structure constants in arbitrary
characteristic. Identifying an arbitrary hidden subgroup with a Lie
subalgebra is also part of the imported Lazard contract: the existence of
a polynomial group law alone does not prove that correspondence.
The zero-algebra case is separate; terminal recovery uses
n>0. Distinct nonzero evaluation points remain explicit where interpolation
is used. Nonzero field scales, not arbitrary nonunits over rings, supply
invertibility.

The algebraic chain is now constructed, but the full recursive quantum
instrument is NOT composed in Lean. The previous module checks the first
central instrument. Next, instantiate its generic certificate with the
adjacent kernel's additive coordinates, the current hidden group image and
the new public section at EVERY stage. Relate the resulting address kernel
to the next stage's source density, including retained classical records.
Then prove tensor-product source propagation for fresh disjoint packets and
the final Fourier-sampling/nullspace recovery statement.

The diagonal witness finder and complete Fourier family remain imported
algorithmic obligations. Relevant primary dependencies are
[Ivanyos--Santha](https://arxiv.org/abs/1503.09016) for fixed-degree diagonal
systems and [Imran--Ivanyos](https://arxiv.org/abs/2304.08376) for an existing
central-quotient strategy with its stated bounded-prime qualification. Search
did not certify a new theorem or remove qualifications from either source.

Each original Rees source still pays for all evaluation components. Recursive
packet arities multiply, and the cost of sections, reversible arithmetic,
central Fourier measurement, source errors and solver aborts must be counted.
Lean's noncomputable algebra is not a complexity theorem or an executable
quantum circuit. In the intended coordinate implementation, zero-padding and
linear maps are public operations, not a hidden-subgroup oracle.

## Adversarial Checks

- Quotienting the original L by its lower central series would lose hidden
  directions. The terminal bijection and membership theorem explicitly
  preserve L and h instead.
- A central Lie kernel does not itself assert a compatible group law. The
  law is now derived from the original group, and group centrality is proved.
- Dilation invariance of the ambient tail does not by itself imply hidden
  image invariance. Both are proved separately, in both directions.
- Surjective stage maps do not automatically give a computable public
  section. The checked section is the explicit coefficient zero-padding
  construction, not an existential hidden lift.
- Correct one-stage marginals do not justify correlated input packets or
  ignoring adaptive records. That quantum-composition obligation stays open.
- A checked chain says nothing about novelty or a classically hard useful
  input. No candidate admission or speedup claim follows from this pass.

No counterexample to the scoped chain statement emerged. Do not treat that
as evidence for the remaining quantum composition or classical hardness.

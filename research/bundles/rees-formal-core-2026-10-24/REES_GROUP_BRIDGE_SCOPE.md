# A Constructed Group Bridge, Relative To The Explicit Base BCH Law

2026-10-24. This pass adds a checked bridge to the existing Rees formal
modules. It is not a new quantum algorithm, a novelty claim, a new
independent review, or a proof of the Lazard correspondence from scratch.
Its exact input boundary is part of the result, not hidden in the axiom
audit. Compilation and final verification are recorded separately in
GROUP_BRIDGE_VERIFICATION.md.

## Why This Was Selected

The preceding two passes excluded explicit high-degree application
families. Repeating nearby examples would not manufacture a hard natural
problem. Comparing the current alternatives found: the custom cubic OPI
guarantee already transfers from known scalar OPI; HDQI still lacks both a
global degree-scale preparation guarantee and a specified surviving hard
output; and the local binary BPQM certificate cannot certify crossing its
dual reconstruction threshold. None supplies an immediate new algorithm.

Rees remains a concrete proposed end-to-end theorem, with one completed
independent AI review and unresolved novelty/application questions. Its
formal source theorem still accepted arbitrary group homomorphisms and
an evaluation identity as premises. The Lie construction and dilation
were already checked, but the connection between those files and the
operational group maps had not been constructed. This pass closes that
particular dependency, relative to an explicit base group law.

## The Remaining Base Assumption

The input is a field F, Lie algebra L, and a GROUP structure on the same
underlying type L. A `PolynomialGroupLaw F L` supplies:

1. A concrete finite binary Lie expression W, using zero, its two inputs,
   addition, field scalar multiplication and brackets.
2. For every x,y, group multiplication x*y equals W(x,y).
3. The group identity is the additive zero; group inverse is additive negation.

For the intended nilpotent Lie algebra of class c<p over F_p, W is the
finite BCH polynomial. The existence and correctness of this base group,
the admissibility of its denominators, and the subgroup/Lie-subalgebra
correspondence remain imported Lazard/BCH mathematics. This module does
NOT obtain them from raw structure constants. In particular it does not
claim a construction in arbitrary characteristic just because its bridge
is stated over any field admitting the supplied law.

That is a sharper boundary than assuming the REES homomorphisms: only the
original base group and its explicit law are inputs. The cover group,
evaluation maps, dilation automorphism, and their actual hiding identity
are derived. The standard naturality of Lie polynomials, not a new BCH
theorem, is the mathematical mechanism.

For context, the nilpotent-group algorithmic reductions remain those in
the existing manuscript and its cited primary sources, including
[Ivanyos--Sanselme--Santha](https://www.irif.fr/~santha/Papers/iss12.pdf)
and [Imran--Ivanyos](https://arxiv.org/abs/2304.08376).
Their algorithms and restrictions are not enlarged by this formal check.

## What Is Constructed And Proved

`Expression` and `interpret` encode finite Lie expressions. Structural
induction proves that every Lie homomorphism preserves their evaluation,
and every Lie subalgebra is closed under them. No special BCH coefficients
or unproved cover associativity are needed for those induction steps.

`subgroup` takes any Lie subalgebra S of the supplied base group and makes
it a genuine subgroup. Closure under multiplication follows from W;
identity and inverse use the two explicit base-law conditions. Its group
laws are inherited from the already supplied ambient group, not asserted
as extra axioms. `toLie_mul` relates the actual subgroup product back to W.
`liftLieEquiv` then converts a concrete Lie automorphism of S into a group
automorphism of that actual subgroup.

`piLaw` proves that the pointwise product group L^c has the same expression
W. Applying `subgroup` to the PREVIOUSLY constructed evaluation realization
of the positive lower-central Rees Lie cover constructs `groupCover`.
The following maps are real objects, not new theorem premises:

- `evaluationGroupHom`: projection from that subgroup onto a base coordinate.
- `dilationGroupEquiv`: the previously checked graded Lie dilation, now
  transported to the actual cover group with multiplication preservation.
- `highestGroupElement`: the top-grade monomial as an element of that group.

`group_hidden_membership` identifies simultaneous hidden membership with
the recovered coefficients. `dilationGroup_hidden` proves that the actual
group dilation preserves it without assuming a homogeneous original h.
`actual_tuple_hides` instantiates the earlier interface with these specific
homomorphisms and proves its evaluation identity from interpolation. Its
conclusion is about coefficients of the actual group difference a^-1*b,
not an additive difference substituted while the group is nonabelian.

The original oracle promise and the submodule h corresponding to the
hidden subgroup remain explicit mathematical hypotheses. Definitions of
the public cover and maps do not depend on h. A proof mentioning h is not
permission for the algorithm to query a basis of h.

## Centrality Is Derived Too

`linearPart` records the two linear coefficients of any Lie expression.
On commuting x,y every bracket term vanishes, so the expression equals
its linear part. In particular

    W(x,y) = W(x,0) + W(0,y),       when [x,y]=0.

The supplied base group identity forces W(x,0)=x and W(0,y)=y. Hence
Lie-commuting elements multiply additively and commute in the base group.
No blanket Lie-to-group centrality premise was added.

`highestGroup_central` combines that deduction with the previous top-grade
bracket theorem to prove centrality inside the constructed cover group.
`highestGroup_scaled` proves its a^c scalar scaling under the actual group
automorphism. This checks the group meaning of the scalar exponent used
in the first central cancellation step. The later graded quotient chain
and complete cancellation certificate are separate obligations.

## Resources And Evidence Boundaries

This is a proof-assistant check, not executable quantum compilation.
`noncomputable` is used for ordinary mathematical structures and inverses;
no extracted runtime is inferred. The manuscript's public interpolation,
field arithmetic, BCH evaluation, controlled translations, source copies,
SDE solvers and approximation budgets remain separately charged.

Relative to the same public ordinary coset oracle, the proposed fixed-class
Rees algorithm's hoped-for advantage is still polynomial quantum cost in
the coordinate input versus exponential classical oracle-query cost in
specific growing-prime families. The existing random-label lower bound
does not provide a natural efficiently evaluable application. This pass
changes neither that comparison nor the state-source access promise.

The new file has 14 theorems and 12 explicit definitions/types. Together
with the frozen four-module base this is 89 theorems and 125 audited
declarations. An axiom report using only standard foundations does NOT
erase assumptions in theorem statements. The verifier therefore records
the base group law as a hypothesis and keeps full-algorithm, base-BCH,
quotient-chain, quantum-execution and novelty flags false.

## Attempts To Overclaim, And Next Decisive Step

- "The whole BCH theorem is now formalized." False: the base law is supplied.
- "Any Lie algebra over any field gives this group." False: existence of the
  compatible base group is a substantive premise, not proved universally.
- "The first central layer proves every quotient stage." False: the quotient
  chain, its descended automorphisms and final recovery are not constructed here.
- "The instrument no longer needs a cancellation certificate." False: support
  preservation, nonempty active scales and the diagonal moment equation must
  still supply that certificate. No efficient SDE implementation follows.
- "Kernel-checked maps prove a speedup." False: resource composition, imported
  arithmetic, natural application and novelty are independent obligations.
- "Generic tests certify the new proof." False: only actual Lean compilation
  and axiom checking support its formal claims. Python tests check verifier
  failure behavior; old finite controls cover different scopes.

The next proof step worth taking is to construct the central cancellation
certificate from the actual automorphisms and an explicitly verified
nonzero scalar witness, then join it to the existing all-record instrument.
That would replace a meaningful conditional interface, unlike adding more
finite group examples. A general Lazard formalization is a separate major
project; this pass does not silently start or claim to finish it.

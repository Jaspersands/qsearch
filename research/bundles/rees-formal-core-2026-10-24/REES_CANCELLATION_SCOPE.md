# Constructed Rees Central Cancellation

2026-10-24. This pass removes the assumed CancellationCertificate from the
first central Rees step. It does not formalize the entire algorithm or
establish a new speedup. Previous five modules and their receipts are frozen.

## Scientific Question

Do the actual Rees automorphisms and a nonzero diagonal moment witness
implement the desired quotient-source channel, for every central measurement
record, or does the source argument still assume its desired result?

The native proposal takes an explicit finite prime-field nilpotent Lie
algebra, a coherent hiding-function evaluator on its BCH group, and actual
independent coset sources derived from that evaluator. Fixed class below
the characteristic is the intended regime. Public lower-central spaces,
Rees interpolation and graded dilations require no hidden subgroup basis.
The mathematical hidden subalgebra is used only in the correctness proof.

The proposed advantage remains conditional: fixed-class polynomial resources
in the input dimension and log p, using the published fixed-degree diagonal
solver. No classical lower bound or natural hard application is proved.
Existing public polynomial stabilizer, power-product and pencil-norm
classical filters still rule out their covered application families.

## Checked Construction

ReesCancellation.lean has 15 theorems and 13 explicit definitions.

1. For actual group automorphisms delta_i, center automorphisms alpha_i and
   delta_i(H)=H, derive preservation of H times the central image in BOTH
   directions. Invertibility is essential for the outside-support argument.
2. The public controlled action is delta_i(sigma(q)) on active coordinates
   and identity on inactive coordinates. It has no hidden decomposition
   argument. Its difference is delta_i(sigma(r)^-1 sigma(q)), not an
   additive difference and not a homomorphic-section assumption.
3. Choose h,z decompositions only inside the correctness proof, then derive
   the certificate's inside support, outside zero and phase product.
4. For linear forms lambda_i and an additive character psi, the actual
   linear equation sum_i s_i^d lambda_i=0 implies the character product is
   one for every central vector. Positive degree handles zero scales
   correctly. Existence of at least one nonzero s_i is required separately.
5. Construct the hidden Rees subgroup as the intersection of evaluation
   preimages, and the actual injective top-grade central group embedding.
   Instantiate delta_i with the previous constructed graded automorphisms,
   deriving their H preservation and s_i^n action on the center.
6. reesCertificate has no CancellationCertificate input. Its mathematical
   inputs are the base law, actual interpolation hypotheses, hidden
   subalgebra, public section, character labels, nonzero scales and the
   verified moment equation.
7. rees_instrument invokes the earlier physical two-sided measurement and
   controlled-discard theorem with that constructed certificate. It proves
   an exact identity on every address/reference matrix, including all
   measurement records. There is no favorable-character postselection.
8. central_range_normal, hiddenCenter_quotient and quotientRelation_iff
   identify the predicate with coset equality in the ACTUAL quotient by
   the central image, when sigma is a right inverse of its projection.
   No normality of H is assumed.

The all-record equation is rho[(q,a),(r,b)] times the indicator that
sigma(r)^-1 sigma(q) belongs to H times the central image. On a uniform
quotient address it is the desired quotient coset density. The theorem
keeps an arbitrary reference, so it is stronger than a basis-state check.

## Dependencies And Costs Still Open

- PolynomialGroupLaw supplies the base BCH group and its finite Lie
  expression. This is not a proof of Lazard/BCH from raw structure constants.
- The additive character is supplied with unitarity, and its full family
  with Fourier completeness. Their efficient finite-field implementation
  is not constructed in Lean here.
- Scales are an explicit function of measured labels with nonzero and
  moment guarantees. No arithmetic solver is implemented by this proof.
  The intended dependency is [Ivanyos--Santha](https://arxiv.org/abs/1503.09016),
  with fixed degree and sufficient arity, not arbitrary diagonal systems.
- Every stage consumes its full packet of independent sources, including
  zero-scale targets. Across stages the packet arities multiply. Each
  original Rees source pays for the full tuple of base-oracle evaluations.
- Controlled translations, public section computation, Fourier transforms,
  fresh sources and approximation errors must be charged in an executable
  algorithm. Fintype and noncomputable Lean definitions are not runtime bounds.
- This is the first/top layer. Constructing compatible graded quotient
  objects and their hidden images, composing the full descent, and proving
  final abelian recovery remain formal work. The generic quotient predicate
  theorem is NOT that full chain.
- No novelty certification follows. The iterative central-quotient strategy
  is existing literature; [Imran--Ivanyos](https://arxiv.org/abs/2304.08376)
  states a fixed-class, bounded-prime result. This pass does not remove
  that qualification from their theorem or establish a new application.

## Attempts To Disprove The Step

- All-zero scales solve the moment equation but erase the outside signal.
  The certificate requires a nonempty active set; the earlier physical
  control explicitly shows identity action retains unwanted coherence.
- Nonunit ring scalars can cancel phases while losing support. The active
  maps here are actual equivalences over a field. This is not an extension
  to arbitrary prime-power rings.
- Uniform rescaling of a nonabelian Lie algebra is generally not a Lie
  homomorphism. This construction uses the previously checked graded
  dilation, not ordinary scalar multiplication on the full group.
- An arbitrary section can carry central twists. The proof retains the
  exact group difference; it never assumes sigma(q*r)=sigma(q)*sigma(r).
- A hidden h,z factorization could conceal advice. It is absent from
  controlledAction and publicDilation and used only to prove their behavior.
- A favorable branch could conceal exponential postselection. Every record
  is summed, forbidden records have zero unnormalized mass, and the earlier
  proof supplies the complete mass-one identity.
- Correct marginals do not imply independent targets. The physical source
  remains an explicit tensor product. Correlated replacement is not allowed.

No counterexample to this scoped statement emerged. That is not evidence
for asymptotic hardness or for the still-unformalized complete algorithm.

## Next Decisive Step

Construct the compatible truncated graded quotients and their induced
dilations/hidden images, then compose this channel without inventing new
independence or source-access assumptions. Reconsider the portfolio before
starting: do not expand verifier infrastructure or finite examples merely
to accumulate checked declarations.

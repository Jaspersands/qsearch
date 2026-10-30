# Next Theoretical Gate: A Source-Matched Plane Presentation

UPDATE2026-10-26: the adapter below now has a constructive consecutive-pole
reduction and positive independent review. Read
`../one-point-plane-adapter-2026-10-26/REVIEW_RESOLUTION.md`. The original
open-item wording below is historical. Exact-order access is resolved at
the theorem level for the fixed-p promised-input family under the reviewed
compact module, not yet implemented or measured on the native input.

Date: 2026-10-26. Literature correction and next question, not a completed
order computation. This is separate from the reviewed sampler relaxation.

## Known Result To Use

[Lauder--Wan, Corollary3 and the end of Section6.3](https://library.slmath.org/books/Book44/files/18lauder.pdf)
gives a deterministic algorithm for the order of the Jacobian of the smooth
projective model of an explicitly presented geometrically irreducible affine
curve. With a bivariate plane equation of degree Delta, its bit complexity
is polynomial in Delta, the characteristic p, and the finite-field extension
degree. Singularities in the supplied plane model are allowed; the proof
extracts the weight-one factor from its zeta function. This does not require
that the supplied plane equation itself be smooth.

For our fixed p=100003 family this is a theoretical polynomial-order route
ONCE a degree-polynomial plane equation over the original field is obtained
with a charged construction. It is not polynomial in log(p) uniformly as p
varies, and it is not a practical-runtime assertion. Applying the general
many-variable bound directly to a growing number of curve quadrics does not
give the desired conclusion. The presentation parameters matter.

## What Is Still To Prove Or Build

The unresolved adapter is from the recovered true quadratic ideal or the
proposed compact multiplication module to a certified birational plane model
over F_100003, with polynomial degree and bit cost. A generic projection slogan
does not supply that adapter. Generic polynomial solving is not an acceptable
complexity argument either.

Useful ingredients already available or proposed:

- The selected-point tangent gives a rational function with a simple zero
  at a known smooth point. Such a function is not a p-th power, so it is a
  candidate separating function. Its pole degree is bounded by the embedding
  degree. This does not yet construct a function-field multiplication table.
- If a finite separable function-field presentation over F_q(x) is built,
  a primitive element and its minimal polynomial provide a candidate plane
  equation. Record its degree, coefficient sizes, and inverse expressions
  for original coordinate functions, not only a vanishing polynomial.
- The compressed graded module is a possible way to obtain those finite
  multiplication tables; the construction and all-degree certificate must
  first survive its independent review and native implementation.

Avoid these false shortcuts:

- A polynomial relation between two functions is not a proof that they
  generate the original function field. A map of degree>1 counts a different
  curve's Jacobian.
- Counting the curve over F_(q^b) does not generally determine its original
  F_q zeta polynomial. A field extension used to choose a pencil must be
  descended with certified Frobenius/base-field structure before asserting
  the native group order, or replaced by a base-field construction.
- Finite degree-eight experiments do not construct every later tower field.
  Even a polynomial algorithm given B does not generate those B inputs.
- Closing exact-order access still leaves the auxiliary effective-coset
  search exponential in the current r_2 bound; it does not dequantize every
  generic AG class or establish a remaining quantum separation.

The next reasoning pass should prove or falsify this specific adapter rather
than treating order finding as an unexplained oracle or reimplementing an
entire point-counting library. Gemini's immediate bounded work remains the
matrix-to-graded-algebra handoff, with native round-trip checks.

# Fixed Fields, Geometric Labels, And The Frobenius Escape Test

2026-10-23. SOURCE AUDIT; INDEPENDENT REVIEW PENDING.

This pass audits the existing weak-isogeny surface source. It does not add
another oracle problem. No geometric label generator or coherent quotient
circuit was executed. The two curve point counts below are actual finite
field computations; the larger-dimensional conclusions are deductions
under the stated source and model promises.

## Decision

The source's paid common-definition-field promise gives a stronger and more
useful conclusion than merely bounding each intermediate field: after ONE
quadratic base extension, every intermediate quotient, level-4 theta model,
and polarized isomorphism needed by the proposed construction can be kept
over one fixed base field. Auxiliary torsion coordinates still require
separate, charged small extensions. This does not implement descent.

Canonicalization must preserve the fixed embedding of that base field.
Replacing coefficients by their minimal polynomials, or minimizing over
their Frobenius conjugates, changes the equivalence relation. An exact
supersingular-curve countercontrol falsifies that shortcut. It is a
regression requirement for the future backend, NOT a bug found in an
already implemented geometric backend.

The same example also rules out treating polarized Frobenius self-conjugacy
as automatic. A different tempting escape, routing Frobenius through the
known source and weak isogeny, is eliminated by an exact naturality identity.

## 1. Contract And Uniform Base

Keep the source of SMOOTH_REPOLARIZATION.md unchanged:

- E is supersingular in characteristic p>3; A=E^2.
- The full supplied source order and phi:A->B are defined over a paid
  common field k. The old polarized B is modeled. No target order is given.
- phi is ell-polarized, ell is an odd prime different from p, and auxiliary
  weak evaluations share one scalar at each order for a single global phi.
- All auxiliary orders and their bounds are fixed before oracle evaluation.

As proved in PRIME_SQUARE_FLAGS.md, Frobenius of E commutes with its full
quaternion order, and is therefore an integer scalar c. Write

    k = F_(p^(2m)),    c = +/- p^m.

Naturality and surjectivity of phi give pi_B=[c]. Every geometric subgroup
of prime-to-p torsion is then k-stable. Every k-rational quotient of B^8,
including EACH correctly refined prime-square stage, inherits pi=[c].

Now replace k ONCE by k_star=F_(p^(4m)). Its Frobenius is [c^2], and

    c^2 = 1 mod 8.

Consequently all 8-torsion of every such intermediate variety is rational
over the same k_star. The theta-model representability construction in
2026/1142, Proposition 6.3, uses rational 8-torsion for symmetric level-4
theta coordinates. The quotient primitive A26 is expressly required to
output over the subgroup's definition field. With those effective model
primitives, no new base extension is needed at successive stages.

This is NOT an appeal to A3 as an algorithm for arbitrary repolarization.
The actual modeled quotients are still constructed by the smooth source;
this argument bounds their fields and the model primitives they call.

### Geometric isomorphisms also descend

For any geometric group homomorphism u:X->Y between two intermediate
varieties with the same scalar Frobenius [c^2], naturality gives

    pi_Y u = u^(|k_star|) pi_X.

The left side is [c^2]u=u[c^2]. Surjectivity of [c^2] implies
u^(|k_star|)=u, so u is k_star-rational. This applies to polarized
isomorphisms and automorphisms, not just to the quotient maps. Cancellation
uses surjectivity, not separability: p divides c.

The canonicalization algorithm must enumerate theta-coordinate changes
and allowed translations inside this fixed-field realization. It does NOT
enumerate automorphisms of the coefficient field. The finite theta orbit
has a bound depending on geometric dimension; dimension 16 remains an
enormous fixed cost, not an efficient practical representation.

## 2. Separate Auxiliary Fields, Not Their Compositum

For an auxiliary prime r != p, the r^2-torsion Frobenius over k_star is the
scalar c^2 modulo r^2. Euler's theorem supplies the explicit bound

    d_r = r(r-1),       (c^2)^d_r = 1 mod r^2.

For prime-only marking level s use d_s=s-1. These bounds need no large
discrete logarithm and do not factor a large unknown integer. They are
polynomial in SMALL auxiliary primes, not in their bit lengths. They give
absolute field degrees at most 4m*r(r-1) for the prime-square inputs.

Construct each field as a separate extension of ONE fixed representation
of k_star. Embed all data at that level into it, consistently with the
already paid embedding of the original k. Arithmetic at different levels
never requires a simultaneous torsion-coordinate field. Every geometric
map being evaluated is over k_star. Applying it to a point at level r is
done in that point's extension; the next level uses its own extension.

In particular, comparing canonically marked outputs means comparing the
ordered tuple of encodings in their fixed level fields. It does not mean
forming a field of degree lcm(d_r : all r). A model that retains each
temporary point field as its next base and repeats this operation has not
implemented the required bounded-field source.

For fixed dimension d, model coordinate length is O(4^d*log|k_star|).
The corresponding point-coordinate bound is multiplied by at most d_r.
Thus fixed-width output registers can be chosen from the public auxiliary
plan, independent of the group query. This supplies the representation
part of coherent compilation, NOT reversible circuits or verified clocks
for the actual geometric primitives.

## 3. Actual Geometric Counterexample To Galois Labels

Work in k=F_37[u]/(u^2-15); 15 is a nonsquare. Set

    E: y^2 = x^3 + (11-u)x + (-5-13u),
    j(E) = 3+u.

Its 37-power conjugate has coefficients 11+u and -5+13u and j=3-u.
Both j-invariants satisfy j^2-6j-6=0, but they are different elements of
the chosen algebraic closure. In characteristic greater than 3, different
j-invariants exclude even a geometric isomorphism of elliptic curves.

The implementation independently checks the coefficient of x^36 in
(x^3+a*x+b)^18 is zero for BOTH curves, the Hasse criterion for
supersingularity. It also enumerates both actual point sets over k via
square membership and obtains 1444=(37+1)^2 points for each. Their
q-Frobenius is [-37]. Thus this is not an ordinary-curve counterexample
being mislabeled as supersingular. Both have scalar q-Frobenius, yet
neither the shared minimal polynomial nor the Galois orbit is a valid
geometric j-label. Extending k does not repair that collision.

This control separates THREE operations:

1. A change of field presentation with a specified embedding is legal.
   If v is represented by -u, the SAME j is 3-v in the second presentation.
2. Replacing j=3+u by the different point 3-u is a field automorphism, not
   an isomorphism of the two elliptic curves over the fixed closure.
3. Ordinary q-Frobenius of E is an endomorphism, but p-Frobenius has
   codomain E^(p), which is not geometrically isomorphic to E here.

The control is a backend falsifier, not a new hard problem or an algorithm
for the surface source. No hidden-kernel data are extracted from it.

## 4. A Frobenius Route That Cannot Escape The Deficient Ring

The earlier product/mixing attack needs a genuinely additional integral
endomorphism gamma of B with L+gamma(L)=B[ell], where L=ker(phi^dagger).
One proposed geometric source is an actual polarized isomorphism
u:B^(p)->B, followed by p-Frobenius. It must be computed and tested. The
curve example above shows why existence cannot be assumed automatically.

Could one replace u using the known SOURCE order and the weak phi? Suppose
an integral map rho:A^(p)->A is available. Consider

    gamma = phi rho (phi^(p))^dagger Frob_B.

Frobenius naturality for phi^dagger gives

    (phi^(p))^dagger Frob_B = Frob_A phi^dagger,
    gamma = phi (rho Frob_A) phi^dagger.

Thus gamma is just another transported source endomorphism F_a. In
particular gamma(L)=0, not a complementary Lagrangian. Its high degree,
non-scalar appearance, or explicit Frobenius factor does not change this.
The same conclusion holds with iterated Frobenius and an appropriately
typed rho. Division by ell is NOT free: proving that the quotient is
integral is exactly an additional kernel-stability condition.

Four local Tate-module controls verify the identity on all 16 matrix units
and check annihilation of im(phi mod ell). Their arbitrary local
similitudes are not claimed to arise from the displayed p=37 curves.
The geometric conclusion rests on naturality, not those finite examples.

## 5. Adversarial Review And Remaining Blockers

- Missing common field: if phi or the full source order is not defined
  over the paid field, the scalar argument is unavailable. Keep the source
  blocked; do not infer the promise from passing arithmetic controls.
- Abstract descent is insufficient: a backend returning temporary-field
  theta coordinates must implement compatible descent and point transport.
  Neither field accounting nor the existence of a model does that for it.
- Independent conjugation of levels is forbidden. Use one geometric
  automorphism for the whole marking tuple and the permitted common scalar
  at each level, as in the preceding rigidity audit.
- The p=37 example rejects a shortcut; it does not falsify the correctly
  embedded source or establish hardness of any surface target.
- The wrapped-Frobenius obstruction excludes one attempted source of an
  extra map. It does not exclude a genuine geometric self-conjugacy map,
  a paid small-degree splitting, or another classical attack.
- No polynomial-time classical recovery of the full general target order
  follows from having scalar Frobenius. Knowing where endomorphisms are
  defined is not knowing the endomorphisms.
- No scalable quotient, canonical marked label, or coherent source has
  been executed. The complete algorithm and its significance still need
  independent mathematical review and exact prior-art comparison.

The next decisive task remains an actual geometric source or an attack on
the SAME weak input for an indecomposable target not killed by the known
product/mixing tests. Do not substitute more opaque-label receiver tests.

## Sources Checked

- Corte-Real Santos, Piasecki, Wesolowski,
  [2026/1142](https://eprint.iacr.org/2026/1142), retained 44-page version:
  A7/A22/A25/A26, Proposition 6.3, Lemmas 6.17 and 6.22. Its coordinate
  canonicalization is geometric, not a quotient by coefficient-field
  automorphisms. The exact model implementation is still a dependency.
- Finotti, [A Formula for the Supersingular Polynomial](https://web.math.utk.edu/~lfinotti/papers/sspol.pdf),
  Hasse criterion used in the independently computed p=37 control.
- Montessinos, [Equivalent computational problems for superspecial abelian surfaces](https://arxiv.org/html/2601.18050),
  Theorem 3.5 and Lemma 5.1: the conversion results require appropriate
  target-order/IKO data, or a known small kernel and source orders.
  They do not justify granting an unpolarized target splitting as free
  advice in our unknown-ell-kernel source.

No novelty claim is made for field descent, Frobenius naturality, or these
standard elliptic invariants. Their role is to prevent invalid reductions.

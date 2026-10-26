# Public Induced-Phase Compiler

Status: a public coefficient compiler and exact falsifiers for the
right-fiber source proposed in METABELIAN_DERIVED_HSP.md. This is not a
quantum receiver, a new algorithm announcement, or an admitted speedup.
The compiler pass added no Lean theorem. The subsequent
RIGHT_FIBER_SOURCE_REFINEMENT.md pass formalizes the general right-fiber
instrument and its additive-quotient source-to-scalar composition; the
general Lie-to-symbolic-polynomial refinement was a separate gap.
INDUCED_COCYCLE_UNIVERSAL_REFINEMENT.md now gives a written universal
cocycle/substitution proof, complete rational normal-form certificates
and Lean operator-specialization lemmas. It is not one machine-checked
Lazard-to-controller theorem.

## Contract

The input is an explicit nilpotent Lie algebra N over F_p, a public
decomposition N=A+I with N' contained in I and I abelian, and a linear
section A -> N. A need not be a subalgebra. The structure schema checks
alternation, Jacobi, the ideal conditions and actual nilpotency class k.
It does not certify an embedding N=L' in an ambient HSP instance.

For g=exp(Q), write Q=A0+B0 and X=s(x). The source cocycle is

```
kappa(g,x) = log(exp(-A0-X) exp(A0+B0) exp(X)).
```

`cocycle_template` now uses the closed commuting-adjoint formula in
INDUCED_COCYCLE_UNIVERSAL_REFINEMENT.md, with k^2 operator terms.
`lie_word_cocycle_template` retains the independent universal section-word
reference at (-A0-X,A0,B0). Every coefficient remains formal in log-Q
coordinates and public carrier x. The rational certificate compares the
entire word and closed formula in a universal module, not at sampled
hidden values. No interpolation or fitted hidden polynomial is used.

The public full-jet alignment uses identity A translations for every
Fourier label. Zero labels are retained. It verifies the GL matrices and
the complete scalar feature rank. The compiler subsequently verifies
that the transformed nonconstant displacement is exactly the shared
Taylor jet, not merely that its degree is bounded.

Given full potential degree D and p>kD, the fixed parameter basis is every
coefficient of every log-Q component through degree D. For the proposed
ambient route the conservative choice is D=c. The output is the entire
polynomial

```
P(q,t) = -sum_i lambda_i kappa(exp(Q(Y_i+s_i*q)), L^-1(t,zeta)_i).
```

The sign, constant terms, zero labels and measured spectators are all
retained. Operational functions receive no values of Q or its unknown
coefficients. The separately named evaluation fixture does receive known
values for tests and is not called by the compiler.

## Parameter Support

The safe total degree in (Q,x) is k. After substitution the weighted
degree is at most kD, with q weight one and a Taylor coordinate its
Taylor weight. The hidden-parameter degree is at most k. The old quadratic
multiplier still raises on cubic products; it was not weakened or reused.

There is a stronger support restriction than the generic degree-k lift:

1. A nonzero Lie word contains at most one B0. A word containing two
   I entries has a bracket of two I-valued subwords and vanishes because
   I is an abelian ideal. Thus the phase is linear in the I coefficients.
2. With B0=0 and X=0, the entire word is log(exp(-A0)exp(A0))=0.
   Every pure-A0 term therefore has at least one carrier factor. Its
   hidden-parameter degree is at most k-1.
3. Public affine carrier substitution and Taylor pullback do not introduce
   hidden parameters. Phase addition also preserves both restrictions.

Set hA=dim(A)*binom(m+D,m), hI=dim(I)*binom(m+D,m). An upper bound on
supported parameter monomials, including the harmless constant, is

```
(1+hI)*binom(hA+k-1,k-1),
```

instead of binom(hA+hI+k,k). Both counts are exposed; no resource claim
is inferred from a count alone. Template compilation and packet validation
check this support. Multiplication exceeding the declared degree raises;
it never drops terms.

If I=N', every B0 has lower-central degree at least two, giving a further
hidden-parameter bound k-1 for k>=2. For I=N'+Z(N), split B0 into derived
and central parts; central parts contribute only linearly. This refinement
is a written observation, not a separately optimized compiler envelope.
The current packet retains the safe general k bound and kD weight bound.
These two bounds must not be conflated when tightening the implementation.

## Exact Falsifiers

The tests compare all cocycle coefficients against an independent rational
semidirect exp/section calculation through normal class seven, then reduce
coefficients into prime fields. They do not infer identities from sampled
evaluations. Class-four tests use both p=17 and p=2^127-1.

For the class-four filiform group, two choices of abelian ideal matter:

- I=N' gives a two-coordinate carrier, cubic hidden-parameter dependence,
  and carrier degree above two. The full aligned phase, including nonzero
  spectators and shared coefficients across sources, is compared with an
  independently expanded polynomial.
- The larger noncentral ideal span(Y0,...,Y3) gives a one-coordinate
  carrier and genuine quartic hidden-parameter terms. Its independent
  cocycle is exp(-(a+x)J)*F(a)*B, F(a)=sum a^j J^j/(j+1)!.

The actual affine Taylor pullback is checked coefficientwise, not only
at known parameter values. A supplied valid leading-column relation
strictly lowers weighted degree while retaining cubic/quartic terms in
the declared lift. Cancellation only at one hidden parameter assignment
is rejected. Zero-scale inputs contribute nothing to the algebra; their
physical consumption remains the controller's separate obligation.

The strict larger-scope ambient witness is also checked: in the c9 Lie
algebra generated inside ut_10, N=L' has dimension17, class4 and an
abelian derived ideal of dimension10. Its public structure tensor passes
Jacobi/nilpotency checks. The compiler's universal cocycle template agrees
with actual matrix exp/log on known inputs at p43 and p2^127-1. This last
test is sampled diagnostic evaluation; the universal Lie-word coefficient
certificate, not those samples, supplies the general algebraic identity.

The small full-alignment tests use degree-two arbitrary formal potentials.
They are coefficient tests, not evidence that those potentials come from
an ambient HSP. Conversely the c9 witness verifies a genuine ambient
derived algebra, but its entire D9 aligned packet has not been expanded.
Do not merge these different evidence roles into an end-to-end claim.

## Remaining Obligations

- Specialize the now-formal right-fiber instrument to the general explicit
  Lie/Lazard chart. InducedRegularSource.lean covers the abstract additive
  quotient and an explicit noncentral vector-BCH example.
- Complete the machine-checked source-to-symbolic-compiler refinement
  from the new universal algebraic proof, and compose all outcomes,
  physical records and disjoint source consumption.
- Supply an executable all-input fixed-degree SDE backend. The current
  partial g<=2 solver is not enough; these tests verify supplied witnesses.
- Implement the conditional adaptive schedule documented in
  INDUCED_END_TO_END_RESOURCE_AUDIT.md. Its separate single-call resource
  certificate is now available; the old quadratic report remains invalid
  for this enlarged scope.
- Establish prior-art scope independently and find a useful hard
  application with matched source access. Neither has been established.

The test result is progress on one public-algebra obstruction. It does
not demonstrate a Shor-level result, a classical separation, or practical
runtime. Stop this route if source composition, uniform resource bounds,
or an access-matched classical algorithm invalidates the intended claim.

## Reproduce

```
python -m pytest -q tests/test_metabelian_induced_phase.py -W error::RuntimeWarning
python -m theorems.metabelian_induced_phase --write
```

The standalone JSON is research evidence only. No central registry,
qsearch command, UI, or admission status is changed.

Validation on 2026-10-22: 500 connected Python tests passed in 180.07s,
including 16 new tests; RuntimeWarning was fatal. The full cached Lean
build passed (3465 jobs), with no Lean source edits. Python syntax,
formal crosscheck, site JavaScript syntax, site checks, registry validation
and whitespace checks passed. The full repository Python suite was not
run. All owned runs completed; no background work was started.

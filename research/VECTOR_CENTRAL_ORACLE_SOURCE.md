# Vector-Center Oracle Source Composition

2026-10-21. A source-composition proof inside the class-three-normal HSP
proposal, not an executed quantum algorithm, new speedup, or novelty claim.

## Question And Scope

Can the original hiding query, complete central instrument and coherent B
Fourier transform be composed without assuming the desired prepared state,
or replacing the physical vector center C by a one-dimensional image?

`formal/Formal/VectorCentralSource.lean` addresses that exact question.
The input is public alternating bilinear beta:A x A->B and gamma:A x A->C,
bilinear delta:A x B->C, and their class-three Jacobi identity. The field
has characteristic different from two and three; finite-register results
assume finite coordinate types. The physical group is A x B x C with
the actual class-three BCH multiplication. Its group laws are proved.

The generic source theorem does not require C to be the FULL group center.
The proposed ambient degree bound DOES require that additional premise.
Likewise, the theorem does not certify that this coordinate group is the
derived subgroup of a supplied ambient Lie algebra merely because a
Python object has that name. The public embedding/chart must be valid.
The main algorithm's stronger p>max(c,3(c-2)) restriction is unchanged.

## One Physical Group, Many Scalar Projections

For each linear label lambda:C->F, compose gamma and delta with lambda.
This gives the existing scalar structure maps and the projection

```
P_lambda(a,b,c) = (a,b,lambda(c)).
P_lambda(g*h) = P_lambda(g) *_lambda P_lambda(h).
```

The projection need not be injective, and lambda=0 is allowed. To derive
the VECTOR group's associativity from the scalar theorem, the proof uses
ALL linear functionals, which separate vectors, not one sampled character.
The A and B coordinates are retained even for the zero functional.

The public central chart sends (a,b,c) to ((a,b),c); its section is
(a,b,0), and its central embedding is (0,0,c). The chart identity and
centrality are proved from the multiplication. This instantiates the
earlier generic CentralRegularSource instrument with the actual group.

Linear labels enumerate all additive central characters under a fixed
nontrivial base character chi, by RetainedFourier.characterEquiv. Thus
central_complete reindexes the full physical instrument without omitting
zero labels. This is not a faithful one-dimensional encoding of N.

## Actual Oracle To Monomial Matrix Source

The operational definition oracleBranch contains only the public normal-
first chart, original hiding function f, normal inversion, central Fourier
and coherent B Fourier. It has no subgroup, projection onto the unknown
support, potential, or secret polynomial coefficients as operational data.

Given a valid hiding function for H, a whole-H parametrization by U, a
common proof-only retraction pi and hidden lift, and the previously derived
section-word potential g(q), original_source proves

```
oracleBranch_lambda[(q,t),(r,t')]
  = |C|^-1 [r-q in U] (|V| |A| |B|)^-1
      (W_lambda(g(q))^dag W_lambda(g(r)))[t,t'].
```

The hidden data occur only as correctness witnesses. The theorem reuses
the already checked hiding-output trace and common section-word action;
it does not assume a polynomial-state oracle.

Here W is itself the actual two-sum B Fourier contraction of the physical
central sector. retained_sector_formula gives its exact displacement and
phase from BCH multiplication. Its representation law and unitarity are
derived, so the W(g(q))^dag W(g(r)) gauge is a conclusion rather than an
assumed matrix-state ansatz. The phase retains the shifted output frequency.

The final carrier is A x B*, with |B*|=|B| checked by carrier_card.
The physical central normalization is always 1/|C|, including lambda=0;
using |lambda(C)| would be wrong. Nothing here samples or measures mu.
This is reducible central Fourier analysis, not an irreducible nonabelian
QFT. Fourier analysis of ordinary coset states is established prior art,
for example [Krovi and Roetteler](https://arxiv.org/abs/0810.3695); it is
not a discovery attributed to this composition proof.

## Falsification And Boundaries

`tests/test_vector_central_source.py` checks exact scalar projection and
vector associativity with nonzero beta, two-dimensional center, several
labels including zero, and primes 5, 17 and 2^127-1. It explicitly exhibits
distinct physical group elements with the SAME scalar projection.

Another control rejects an invalid Jacobi tensor even though its zero-
character scalar projection is valid. Checking only a chosen projected
branch cannot certify the physical group. The preceding actual-coset
controls remain the independent oracle-level finite checks, including
wrong-phase, dephasing and scalar-image-normalization mutations.

These controls are not asymptotic evidence or a classical lower bound.
The source theorem does not establish hardness of natural applications;
the existing classical stabilizer/dequantization audits remain in force.
It also does not instantiate the full ambient input-to-chart refinement,
derive a useful external reduction, or prove novelty of the whole proposal.

## What This Changes

The central/vector/B-Fourier interface is no longer merely several
compatible formulas. One theorem starts with the original hiding-output
trace and ends with the correct monomial matrix source, preserving the
physical center and deriving its unitary representation.

The remaining steps are the matrix batch-shear/full-jet alignment and
phase compiler composition, plus the probabilistic/adaptive rank,
freshness, rejection, resource and precision arguments. Their separate
lemmas do not by themselves certify a complete controller. Generic SDE
execution and a useful hard application remain absent.

The expected asymptotic claim remains only the main proposal's conditional
polynomial bound for FIXED ambient class. This module introduces no new
oracle access, postselection advantage, field enumeration algorithm or
new parameter regime. No CLI/UI or registry admission follows from it.

## Verification

- 413 connected tests passed with RuntimeWarning fatal (93.15s).
- 11 focused vector/retained-Fourier controls passed (4.89s).
- Full `lake build --wfail` passed: 3465 jobs, ten new standard-axiom
  guards, cached Mathlib; module 47s and aggregate 50s. No new axioms or sorry.
- Syntax, generated crosscheck, site JS/site checks, registry validation
  (valid=true, issues=[]), and whitespace pass.
- All owned processes terminated. Full Python suite not run. No commits,
  CLI/UI changes, registry admission, agents, or outreach.

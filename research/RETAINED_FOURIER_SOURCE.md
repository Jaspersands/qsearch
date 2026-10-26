# Retained Fourier Source Bridge

2026-10-21. Local proof and falsification work inside the class-three-normal
HSP proposal. This is not a new HSP algorithm, novelty claim, hard application,
or permission to replace a hiding oracle with a potential evaluator.

## Scientific Question

The earlier central-source theorem indexes all characters of the center.
The class-three partial-Fourier identity indexes all additive characters
of B, but the compiler uses F-linear functionals mu:B->F instead. Does
that compiler register really implement the complete B Fourier transform,
including the zero frequency, with the claimed shifted-frequency phase?

Yes at the finite-field algebraic interface, provided the fixed base
character chi:F->C is nontrivial. This assumption is independent of the
MEASURED central label lambda; lambda=0 remains valid. The Fourier output
mu stays coherent. Measuring it is a different, generally destructive,
channel.

## Character Identification

The map mu -> chi o mu is injective: if two such characters agree, evaluate
their equality at t*y for every t in F. Primitivity of a nontrivial field
character implies mu(y)=nu(y). Cardinality of the finite linear dual and
finite-abelian character dual then gives surjectivity.

Pointwise injectivity of chi is NOT required. In extension fields a
nontrivial additive character can have a nonzero kernel; the scaled-input
argument still works. This is standard finite-field harmonic analysis,
not a new algorithmic ingredient. The proof reuses Mathlib's
[primitive-character results](https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/LegendreSymbol/AddCharacter.html)
and finite-abelian Pontryagin duality.

With K[mu,y]=|B|^(-1/2) conjugate(chi(mu(y))), both row and column
orthogonality hold. Every frequency occurs exactly once, including zero.
B=0 is permitted: the transform is the one-dimensional identity.

For M[z,y]=[z=y+d] alpha chi(ell(y)), actual conjugation gives

```
(K M K^dag)[nu,mu] = [nu=mu+ell] alpha conjugate(chi(nu(d))).
```

The phase uses the output frequency nu=mu+ell, not the input mu. For the
class-three BCH action, ell=delta(a,-)/2, d=b+beta(a,x)/2 and
alpha=chi(rawPhase(g,x)). This yields exactly the displacement and phase
used by the existing compiler, with no irreducibility premise.

`formal/Formal/RetainedFourier.lean` is the proof source. It is a bridge
between complete harmonic-analysis indexing and the compiler formula,
not a proof of the entire adaptive quantum protocol.

## Independent Source Controls

`tests/test_retained_fourier.py` starts from actual gH labels in
G=F_5 x N with a verified cyclic transverse H. N is class three, with
either a one-dimensional center or an extra independent central factor.
The public section and H are specified before the potential is derived.
The direct physical amplitude applies normal inversion, positive central
Fourier and negative B Fourier. It never reads the potential.

Matching genuine oracle labels contracts the original equality kernel.
The result agrees with W(g(q))^dag W(g(r)), including zero central labels,
vector-center labels, and branch mass 1/|C|. Wrong old-frequency phases
and dephasing mu change at least one real source block. Separate controls
check complete Fourier bases in dimensions zero through two, deletion of
zero frequency, and collapse under a trivial base character.

Scalar character projection is a representation calculation, NOT a
replacement of the physical center C by its image lambda(C). Such a
replacement gives the wrong branch mass, especially at lambda=0. The
vector-center tests explicitly reject normalization by that scalar image.

These small direct-product sources test the generic normal-subgroup
interface. Their chosen N is NOT asserted to equal the ambient derived
algebra. They do not certify all premises of the full HSP proposal, nor
do their dimensions or runtime support a speedup claim.

## Corrected Earlier Audit

Version 1 of `central_instrument_and_dual_weight_bounds_audit.py` filled a
density matrix directly from a nonlinear potential and called it an
ordinary HSP source, without specifying the compatible subgroup/chart.
That agreement only checked the supplied potential kernel.

Version 2 instead constructs actual direct-product group cosets, verifies
H, applies an explicit public chart, and only then derives the common
potential. Its old class-three/semidirect-product source description is
corrected to a class-two direct-product control. Its nonlinear section
is valid for the generic instrument but NOT the linear-section degree
argument. The report explicitly leaves full algorithm input premises
unverified. A negative control rejects the nonlinear graph as a subgroup
in standard coordinates without claiming that nonlinear chart potentials
are intrinsically invalid.

## Remaining Obligations

- Instantiate the actual vector-center BCH chart and central character
  projection in the universal original-oracle theorem, then compose it
  with this B transform and GL alignment in one source theorem.
  Preserve the original |C| even when the projected scalar maps vanish.
- Retain the SAME hidden projection/lift across source blocks. None is
  operational advice, and none may be estimated by fitting secret values.
- Establish the probabilistic full-rank batch guarantee, fresh-source
  ownership under adaptive control, and joint rejection/error budgets.
- Extract efficient approximate Fourier gates rather than enumerate the
  finite index sets used in the mathematical proof.
- Supply or explicitly charge the fixed-degree SDE dependency; complete
  recursion and useful hard-application/novelty checks remain separate.

The next task is substantive composition or an independent falsification
of the proposed algorithm, not another small Fourier benchmark.

## Verification

- 409 connected Python tests passed with RuntimeWarning fatal (120.83s).
- Final seven focused controls passed (3.86s), including scalar-image
  normalization rejection added after the connected run.
- Full `lake build --wfail` passed: 3464 jobs, eight new standard-axiom
  guards, cached Mathlib; no new axioms or `sorry`.
- Python syntax, generated crosscheck, site JS/site checks,
  `python qsearch.py validate` (valid=true, issues=[]), and whitespace pass.
- All owned processes terminated normally. Full Python suite not run.
  No commits, CLI/UI changes, central admission, agents or outreach.

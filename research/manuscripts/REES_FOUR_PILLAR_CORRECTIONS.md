# Corrections To The Four-Pillar Rees Review

30 October 2026. Read this alongside, not as a replacement for,
REES_INDEPENDENT_FOUR_PILLAR_AUDIT.md. That external AI-assisted review
is preserved unchanged. Reviewed snapshot SHA-256:

`57b51315fcbe9423cd0bf1093d6cce50f11f17301a80dd3b0304c24d56ef2ab7`.

The previous arithmetic-receiver pass was progress, but supplied no
decoder. This pass checks whether the newly supplied review is a valid
basis for research decisions. It is NOT reliable as written: it contains
false formalization claims, stale scope restrictions, and unjustified
necessary conditions for applications. None of these corrections proves
the entire Rees theorem, establishes novelty, or supplies a useful native
application. Do not promote a candidate on the strength of this response.

## 1. The Formal Hypothesis Is Not A Hidden Axiom

The review names `total_sde_policy_hyp` as an unverified axiom in
CentralCharacterDescent.lean. No such declaration is present in the
current Formal sources. The actual measured receiver takes explicit
parameters `policy`, `active`, and `sde` in
formal/Formal/ReesMeasuredReceiver.lean. Their meaning is a total witness
function, a nonzero active coordinate for every record, and the required
diagonal identity. These are THEOREM HYPOTHESES, not an extra global axiom.

The current `measured_terminal_source` axiom guard allows only propext,
Classical.choice and Quot.sound. This does not discharge the policy
hypotheses: there is still no formal construction/runtime proof for the
required solver. The accurate statement is a kernel-checked conditional
matrix identity, not either an axiom-free end-to-end algorithm or an
algorithm accepted through an invented axiom.

The file-level boundary also needs correction:

- ReesLieConstruction.lean and ReesLieInterpolation.lean supply the
  general Lie-level construction/interpolation. ReesHomogenization.lean
  supplies the distinct-nonzero-point Vandermonde determinant argument;
  it is not the sole construction file.
- CentralSpectralProjector.lean proves an IDEAL ancilla Kraus realization,
  completeness and two-sided projection. Physical gate synthesis and
  approximation error are still outside the result. Calling all ideal
  ancilla realization unverified is stale.
- CentralCharacterDescent.lean proves nontransverse normalization and
  cancellation. Its precise cardinality is |H.comap embed|; identifying
  this with the image intersection uses injectivity of the embedding.
- The class-three BCH group construction assumes 2 and 3 nonzero in the
  field. Its concrete prime-field receiver has p>3. It does not cover
  every p>c case such as c=2,p=3, nor general-class BCH group transport.
- ReesMeasuredReceiver.lean already composes the two measured descent
  stages, sums records, and obtains the additive coset matrix of ALL
  log(H), given exact lifted input and valid policies. It does not prove
  original-oracle preparation through final subgroup learning, runtime,
  approximate errors, or a compiled quantum implementation.

The current formal/README.md states these limits more accurately than
the incoming review's table. Exact-source matrix theorems should not be
reported as proving an unrestricted noisy/projective-source extension.

## 2. Existing Costs Are Upper Bounds, Not Impossibility Theorems

The incoming review's class12 count is reproducible for the SPECIFIED
symmetric schedule:

```text
profile=(13,11,10,9,8,7,6,5,4,3,2,1)
p=2^127-1, error=1/3
leaves per terminal=7,640,436,342,325,248,000
terminal samples=17
original inputs=1,558,649,013,834,350,592,000
```

This is astronomically expensive. It does not prove a necessary source
count, exclude improved algorithms, or rule out every other profile.
Say: this sufficient construction establishes NO practical advantage.
The native application and physical gate model are still missing.

For the manuscript's generic published collision arity, the coarse
query exponent is

```text
E(c)=1+sum_(d=2..c) d*ceil(log2(d+1)).
```

At c=2,3,4,6,8,12 it is 5,11,23,56,109,277, not the review's mixed
table. A separate quadratic algorithm gives the better class2 exponent3;
label that substitution instead of silently mixing constructions. The
symmetric 2c-1 expression is a coarse QUERY upper exponent, not a gate
exponent or lower bound. At fixed derived profile the source factor is
constant in ambient n apart from the terminal samples. Benchmark rows
must retain profile, dimension, prime, error and branch, not only c,r.

The proposed class-six cutoff also fails as a universal use of its own
10^12-query threshold. A genuine class-eight filiform algebra has
profile (9,7,6,5,4,3,2,1). At p=1103 and error=1/100 the existing
symmetric schedule gives arities (64,7,36,5,16,3,4), 18 terminal
samples and 2,229,534,720 original inputs, below that cutoff. The new
control verifies Jacobi and the actual lower-central profile, not just
a supplied dimension list. This is still a large CONDITIONAL upper
budget and no practical application or hardware-time estimate.

The stated distinction cannot be merely polynomial query complexity:
[Ettinger--Hoyer--Knill](https://arxiv.org/abs/quant-ph/0401083) already
give polynomial oracle query complexity for arbitrary finite-group HSP,
with exponential computation. The proposed contribution would instead
be efficient TIME on its specific input regime, conditional on the
complete reduction and uniform compilation arguments. No new result is
certified by that comparison.

## 3. Do Not Reintroduce Superseded Scope Restrictions

The direct prime-power descent's FPT(c,r) accounting is not the strongest
current proposal. The written
[ring-to-field reduction](../UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md),
conditional on the field/Rees theorem, gives
`2^O(R*log(R+2))*poly(B,log(1/epsilon))` for explicit prime-power Lie
rings of class c<p with an ordinary coherent hiding oracle. Additive
derived rank does not increase in its local sections; local torsion
field algebras have class bounded by their derived dimension plus one.
This does NOT assert c<=R+1 in the original ring. The original-ring
counterexample remains valid but does not refute the outer reduction.

Likewise the symmetric solver's large-prime threshold is construction-
specific. The newer
[random-column argument](../RANDOM_COLUMN_REES_PARAMETER_BOUND.md)
has a conditional all-prime parameter bound for c<p, using the actual
IID character-label law and a small-prime fallback. Both notes retain
their inherited source, receiver and complexity obligations. They are
not fully implemented solvers or copy-only scope claims.

The black-box elementary-abelianization counterexample remains useful.
But it does not make supplied Lazard relation-lattice coordinates the
only possible torsion algorithm. The manuscript separates the published
group-presentation route from the additive-coordinate route. Charge
the s^c free-Lie dimension if choosing that pullback; do not charge it
to a different route that acquires the target chart directly.

## 4. Fresh Tensor Banks Are A Contract, Not A Universal Necessity

The pointwise matrix-product proof needs the stated joint-state law.
Equal marginals or arbitrary separability do not supply it. Consumed
quantum targets cannot be cloned or used again as fresh copies.

Nevertheless, the manuscript already gives a valid repair for banks
with correlated COSET CENTERS and side information:

```text
Omega=sum_a (tensor_j |a_j H><a_j H|) tensor E_a,  E_a>=0.
```

Independent uniform left translations, with randomization records
discarded, give `rho_H^tensor(M) tensor sum_a E_a`. This follows by
twirling each fixed coset projector and linearity, without new copies.
It does not repair arbitrary coherent packet correlations. Also,
classical SDE retries can reuse already measured labels without paying
new source copies. The review's blanket prohibition confuses these
operations. Preserve the exact joint-state requirements instead.

## 5. The Ten Features Are Not Necessary Admission Conditions

The review's instruction to reject every application failing any of its
ten criteria is unsupported. Existing classical attacks are SUFFICIENT
algorithms under precise hypotheses. Negating a vague feature is not a
proof that one of those algorithms applies. In particular:

- Formal degree, syntactic degree, orbit-parameter degree and exposed
  Frobenius-reduced degree are different quantities. The white-box
  derivative guard is `p>max(D,(D-1)*Delta)`, not merely Delta<p.
- Polynomial orbit rank yields the stated classical reduction only with
  its public circuit/extension-field evaluation access. An unclosed
  rank-capped run is not a superpolynomial-rank theorem or hardness proof.
- Split jets, fixed anchors, exposed Frobenius gates and a semantic
  Moore form each have their own extraction/recognition and completion
  contracts. Their absence or presence is not a universal classification
  of succinct symmetry problems.
- Ramified iteration and unknown affine support are proposed mechanisms,
  not necessary features of every useful application. 'Non-linear Lie
  radical' is not a specified mathematical test in this review; a
  nilpotent Lie algebra's solvable radical is the whole algebra. The
  tensor-train filter needs explicit cores and sitewise actions, not
  a test for unknown computational-basis affine support.
- c<=6 is an arbitrary practical preference, not a tractability theorem.
  For fixed c the proposed bound is polynomial; actual profiles and all
  resources, not an invented universal threshold, determine viability.
- A normal hidden subgroup can be quantum-useful through a new native
  reduction, even if its quantum primitive is already known. Known
  solvability does not imply classical solvability. Non-normality and
  c>=3 are relevance checks for using THIS Rees extension, not universal
  requirements for a Shor-level contribution.
- Efficient coherent oracle access is necessary for the stated ORACLE
  route, but a separately justified copy-source reduction has a different
  contract. Its absence alone proves no quantum intractability. Promised
  known trivial H and testing whether an unknown H is trivial are also
  different tasks.

Likewise the Moore recognizer includes an independent full identity
test for its specified family; it does not invert arbitrary semantic
polynomial labels. These scope restrictions must survive summaries.

### Exact Countercontrol Below The Prime

Let p=5, Gamma=UT_4(F_5), N=E_01+E_12+E_23, and

```text
F=x_0*x_1*x_3+2*x_0*x_2^2-x_1^2*x_2,
g(t)=I+t*N+3*t^2*N^2+t^3*N^3.
```

The ambient group has class3<p and exponent5; g(t+u)=g(t)g(u).
The polynomial has degree3<p, but

```text
D_N(F)=5*x_0*x_2*x_3=0 over F_5,
F(g(t)x)-F(x)=t^5*x_3^3.
```

Thus N lies in the infinitesimal kernel, while g(t) preserves F only
for t=0. This is a FORMAL polynomial identity; no base-field aliasing
or opaque oracle is used. The actual orbit-degree guard correctly
rejects the unsafe inference because (D-1)*degree=9>=5.

This example is NOT hard: its cyclic orbit spans {F,x_3^3}; its full
cubic orbit lies in a 20-dimensional space. The independent orbit-module
classical baseline still applies. The point is to correct the derivative
claim, not to claim that failure of one attack creates an advantage.

Syntactic degree is also presentation-dependent. The public circuit
`x_0+(P-P)`, P=x_0^(2^130), has syntactic bound2^130 but computes x_0
over F_(2^127-1). It has only135 ordinary circuit nodes. The existing
guard can legitimately fail on that supplied upper bound without making
the function hard. A new exact control checks the existing circuit
evaluation/gradient API without expanding P. No production guard is
weakened or replaced by an unsound test.

### Incomplete Jets Without Characteristic-P Iteration

Take Gamma=UT_4(F_11), P=(x_0,x_1^2,x_2,x_3), T=2, ell selecting
coordinate1. Then F=ell(P^2)=x_1^4. Every group-fixed anchor is a*e_0,
and every anchored two-jet vanishes. The implemented filter correctly
returns the full six-dimensional group as an UPPER bound and leaves
the full stabilizer UNKNOWN. Nevertheless, its actual stabilizer is the
proper subgroup with g_12=g_13=0: coefficients of x_1^3*x_2 and
x_1^3*x_3 in (x_1+g_12*x_2+g_13*x_3)^4 force those equalities.
This is another easy algebraic control, not a quantum candidate. It
shows that incomplete jets need not arise from p-power iteration and
must not be declared complete because a speculative mechanism is absent.

## 6. Prior-Art And Research Disposition

The review's universal claim that codimension-one normal subgroups in
class>=3 are nonabelian is false. In the class-three filiform algebra
`[x,y]=z, [x,z]=w`, the codimension-one ideal span(y,z,w) is abelian.
[Ivanyos--Santha](https://arxiv.org/html/1503.09016v2) already cover
special constant-class semidirect families. The correct question is
whether those results subsume the GENERAL proposed regime, not whether
every higher-class example evades them.

The directive to call this a closed longstanding open problem is not
supported by the inspected evidence and conflicts with the manuscript's
own novelty caveat. Use 'proposed fixed-class, growing-prime polynomial-
time composition, pending independent correctness and priority review'.
Do not substitute either a novelty claim or a general impossibility claim
for that unresolved assessment. Keep a useful native application open.

The corrected search contract is: specify a motivated native input and
verifiable output; give a paid coherent reduction with fixed promises;
choose the strongest applicable quantum upper bound; run each classical
attack only under its actual hypotheses; and leave unmatched cases
UNKNOWN, not hard. A new candidate needs an end-to-end advantage argument.
More criterion-driven degree inflation, Abelian padding, random oracle
planting, or parameter sweeps are not the next substantive experiment.

A legitimate constructive option remains partial CLASSICAL reduction:
if a certified filter gives H<=K, restrict the SAME fixed hiding oracle
to the explicit subgroup K, recompute its class/ranks, and analyze the
residual higher-order action. A failed completion certificate is not a
hardness claim. The pre-existing iterated-jet note already states this
hybrid; it is not newly discovered here. A worthwhile next experiment
needs a motivated native residual family and an actual reconstruction
mechanism, not another planted instance or a fabricated ten-feature gate.

## 7. Verification Scope

Three independent focused agents audited formalization, scope/resources,
and application filters. The parent derived and implemented the cubic
and presentation countercontrols and replayed the stated schedule. This
is automated review of specific claims, not a new full-theorem audit.

The formal reviewer ran fresh strict checks of Formal/Audit.lean and
the current Formal/ReesMeasuredReceiver.lean against installed compiled
dependencies, including axiom guards; fourteen relevant source hashes
matched recorded checkpoints. This was NOT a fresh full-project rebuild.
Current source declarations were also inspected by the parent.

Python controls extend tests/test_succinct_polynomial_stabilizer.py,
test_frobenius_circuit_lift.py, test_rees_full_grade_budget.py and
test_iterated_quadratic_jet.py. No quantum source, receiver, solver
runtime or claimed hard instance is executed by these tests.

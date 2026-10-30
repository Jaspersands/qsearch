# Four-Agent Direction Selection

30 October 2026. Bounded comparison outside the recent Rees receiver work.
Four focused AI agents: Faraday (multiplicative polynomial intersection),
Mill (noncommuting dynamics), Schrodinger (streaming DQI), and Herschel
(classical scalar-flat sampling). Parent checked existing work, primary
sources, the quantitative controls, and the distinctions below. This is
not human peer review or a novelty certificate.

## Decision

No new end-to-end quantum candidate survived this comparison. Do not open
another receiver or benchmark module on the strength of these reviews.
The useful new result is an exact obstruction to one proposed local
sampling repair, preserved as a regression control. The dynamics comparison
also supplies a concrete matched classical estimator, not a blanket
dequantization theorem.

The initially selected DQI papers were already represented in this repo.
Existing notes take precedence over re-extracting the same mechanism:
NATIVE_LATENT_SAMPLER.md, BALANCED_SIGNED_MPI.md,
BALANCED_MPI_PRODUCT_TARGET.md, HERMITE_DECODER_PRIOR_ART.md, and
HERMITE_PARAMETER_THEOREM.md. No new literature novelty is claimed.

## Scalar Flats: No Regular Cover On This Support

Use the SAME local predicate as MERSENNE_SCALAR_FLAT_ATTACK.md, in the
explicit arithmetic control

    F = F_2[t]/(t^5+t^2+1), d=3,
    A = {x: Tr(inv0(x)^3)=1}, V=span_F2{1,t}.

Polynomial-basis integer labels give

    A = {1,6,8,9,10,11,14,15,18,19,20,22,25,29,30,31}.

Enumerating all 992 pairs (o,u), with o in F and u nonzero, gives 248
distinct affine images o+uV. Exactly 12 are contained in A:

    {1,6,8,15}   {1,10,22,29}  {1,15,19,29}
    {6,10,18,30} {6,11,18,31}  {6,11,19,30}
    {6,14,22,30} {6,15,20,29}  {8,9,10,11}
    {8,15,25,30} {9,11,20,22}  {14,15,18,19}

The independent enumeration through the actual scalar construction
Tr(mu*(a+v)^(-3))=1 yields the same support. All successful systems have
rank four and two scalar solutions; conditional on acceptance the current
construction gives the uniform law on these 12 planes.

Define the integer function

    h = 1_{1,14,20,25} - 1_{15,22}.

Every accepted plane P has sum_(x in P) h(x)=0, but sum_(x in A) h(x)=2.
Consequently NO weights, even signed weights, can satisfy

    sum_(P containing x) w_P = c > 0 for every x in A.

Multiplying these equations by h(x) and summing would give 0=2c.
Thus merely changing the distribution over these flats cannot make
uniform-within-flat sampling uniform on A. Equal local ranks do not help.
Any probability mixture of these uniform-plane laws has E h=0, whereas
the uniform alphabet has E h=1/8. Since |h|<=1, its local TV is at least
1/16. For the actual uniform-plane law, exact local TV is 7/48.

Important positive control: if d(x) counts incident planes, this law has
point probability d(x)/48. Accepting a drawn point with probability 1/d(x)
gives probability 1/48 to each accepted point, total acceptance 1/3, and an
exactly uniform CONDITIONAL local output. Thus the obstruction excludes
flat-only reweighting, NOT point-dependent correction. Enumerating all
incidences is not a scalable native algorithm.

Scope: target one, so missing zero is not the cause; fixed n=5 control,
not a theorem for canonical n>=17; no global codeword-fiber TV conclusion;
no exclusion of other subspaces, correlated proposals, or other samplers.
The earlier menu result concerned a different proposal distribution.
This support obstruction is not a new toy-oracle candidate.

Persisted exact control: tests/test_scalar_flat_cover_obstruction.py.
Parent independently reproduced all 12 planes, incidences, the integer
certificate, TV, and the corrected acceptance using the existing FLINT
field/predicate helpers. The test uses independent polynomial arithmetic.

## Noncommuting Dynamics: A Matched Classical Estimator

[Yang, Onwunta and An](https://arxiv.org/html/2508.15170) use dissipation
to shorten the relevant simulation history. The
[nonlinear extension](https://arxiv.org/html/2608.25822v1) retains
normalization and forcing costs. These are existing quantum primitives.
Mill tested the following concrete scalar application, rather than claiming
that adding a noncommuting term to an easy model creates an advantage.

On an N=2^n ring, let S be the shift, Q=kappa*(S+S^dagger-2I),
V=diag(v_x), s=1/sqrt(N), and kappa,eta>0. The v_x have a public efficient
evaluator. Consider

    u' = (Q-eta*I-iV)u + eta*s, u(0)=s,
    m(T) = Re <s,u(T)>.

Usually [Q,V] is nonzero. Nevertheless Duhamel and the Markov semigroup
give the exact identity

    m(T) = E cos(integral_0^min(T,E) v_(X_t) dt),
    E ~ Exp(eta), X_0 uniform, X jumps left/right at rate kappa each.

The two factors 1/sqrt(N) give a uniform average, not an extra dimension
factor. Every sample is in [-1,1]. The expected jump count is at most
2*kappa/eta, independently of T. For r=2*kappa/(eta+2*kappa), the chance
of at least L jumps before stopping is at most r^L. Abort on the L-th
jump and return zero, retaining those zeros in the denominator: the bias
is at most r^L, with at most L event draws. Finite-bit clock/phase errors
require a separate arithmetic allowance; this pass does not implement a
certified finite-bit sampler. No empirical trajectory is a proof of the
identity or of another dynamics model's complexity.

For polynomial kappa/eta and efficient v_x, this is a concrete classical
additive-error competitor with polynomial event work. Rapid oscillations
alone do not create a variance explosion for this bounded scalar. A known
amplitude-estimation precision improvement would not be a new mechanism.
Preparing the full normalized quantum solution is a DIFFERENT task.

Parent control: N=8, kappa=.7, eta=.9, T=2.3,
v=(.1,.4,-.7,1.2,-.3,.6,-1.1,.2). Direct matrix evolution and the
stopped-semigroup mixture differ by 2.5e-16; m=0.876325670188026 and
||[Q,V]||_F=3.508389944119667. This is a floating consistency check only.
Exact rational r=14/23 and L=14 give overflow bound
11112006825558016/11592836324538749809 < 1/1000.

## MPI: A Failed Transfer, Not Hardness

The [MPI paper](https://arxiv.org/html/2610.06753v1) already gives the
public log-Cauchy construction and rational decoder. The repository's
balanced signed extension is stronger than the paper's original radial
source. Neither a fresh log table nor another decoder reconstruction is a
new algorithm. Both sides must receive the same public matrix and centers.

Faraday checked whether the existing interval-rounding attack transfers.
At M=8191,m=6000,n=420 and independent uniform public centers, a union
bound over M^n assignments shows

    Pr[exists x: every centered (Bx-c)_i in [-2047,2047]]
        <= M^n*(4095/M)^m = 2^(-541.1308257...).

The interval is precisely the all-coordinate nonnegative-cosine region.
That strong guarantee is generally unavailable. It says nothing against
high MEAN cosine, which permits bad coordinates. Also the optimizer lattice
{v in Z^m: v mod M in im B} has determinant M^(m-n) when B has rank n.
Hadamard then forces the largest entry of any integer basis to be at least
M^(1-n/m)/sqrt(m)=56.27658..., blocking a bounded-entry basis transplant.
Neither observation is a classical hardness result.

A concrete classical target is public-input lattice rounding with paid
normalized squared residual D=||center(Bx-c)||_2^2/(m*M^2).
The inequality cos(u)>=1-u^2/2 gives Q(x)>=1-2*pi^2*D POINTWISE.
D<=0.7/(2*pi^2) certifies an individual score>=0.30. An EXPECTED bound
E D<=0.7/(2*pi^2) gives only E Q>=0.30, not a useful probability of
reaching 0.30. This distinction corrected the initial agent recommendation.
To match the balanced pilot's mean 0.3421279344361546 via this sufficient
inequality needs E D<=0.03332818818407923, and still does not match its
output law. No new optimizer or such certificate was supplied.

## Streaming And Gibbs: No New Mechanism

Schrodinger compared [Wu--Yang v2](https://arxiv.org/html/2610.01902v2)
with v1 and the existing Hermite notes. Its mathematical claims are unchanged;
the differences found concern related work and a citation. Its explicit
membership stream has n*q^ell entries. Small memory and cheap work per entry
do not eliminate total stream-reading cost or provide unrestricted classical
time hardness. Existing Hermite decoder/resource refinements are not a new
native reduction. Reopen only with a consequential problem and a reduction
that pays access, full runtime, and output verification on both sides.

Parent rechecked [Zhou et al., Appendix B](https://arxiv.org/html/2609.40345v1).
The Prange/Gibbs mixture and its volume tilt are already used in
NATIVE_LATENT_SAMPLER.md. Re-deriving that mixture would not supply the
missing near-complete inverse-trace conditional sampler. No new module.

## Follow-Up Gate

These reviews select NO new leading quantum direction. Do not interpret
that as a theorem that every direction is exhausted, or keep producing
neighboring negative controls as a substitute for an algorithm. A renewed
proposal needs an explicit native input and a paid construction removing
one current blocker: a genuine residual sampler, an MPI optimizer or new
receiver with a changed asymptotic guarantee, or a natural nonabelian source
outside the established classical filters. A failed baseline is insufficient.

No central candidate, negative-result entry, or proof status is promoted.
Only the scoped counterexample and this selection record are new research
artifacts; production behavior is unchanged. No commits, pushes, installs,
outside contacts, or UI changes were made in this pass.

## Verification

Final connected suite: 195 tests passed in 25.03s, with warnings treated as
errors and the pytest cache disabled. Files under tests/:

    test_balanced_signed_mpi.py
    test_balanced_mpi_product_target.py
    test_balanced_mpi_heatbath_trap.py
    test_native_latent_sampler.py
    test_mersenne_scalar_flats.py
    test_inverse_trace_menu_refresh.py
    test_hermite_parameter_theorem.py
    test_hermite_reversible_workspace.py
    test_conditional_boson_dynamics_physics.py
    test_scalar_flat_cover_obstruction.py

Command prefix: /opt/anaconda3/bin/python -B -m pytest -q
-p no:cacheprovider -W error. The seven new tests also passed separately
in the worker's run. The new test file passes py_compile; all 12 site/js
JavaScript files pass node --check. qsearch.py validate returns valid=true,
issues=[], with the same 8 candidates, 796 experiments, 807 results, and
973 negative results. git diff --check passes. This is not a full-repository
test run, Lean rebuild, certified dynamics-sampler execution, or quantum run.

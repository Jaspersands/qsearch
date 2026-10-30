# PPAV Source: Full-Paper Dependency Audit

2026-10-23. Published dependencies inspected; source-specific deductions below
remain REVIEW PENDING. No geometric interpolator, new quantum receiver, full
kernel attack, speedup or novelty claim. Work is isolated while the repository
is being migrated; neither source nor staging was edited.

## Decision

The inaccessible-paper bottleneck is now resolved, but the mathematical source
bottleneck is NOT. Normal browser access successfully downloaded the full
44-page paper by Maria Corte-Real Santos, Etienne Piasecki and Benjamin
Wesolowski, [ePrint 2026/1142](https://eprint.iacr.org/2026/1142).

- Theorem 7.1 does not provide the missing repolarization converter: both
  polarized domain and codomain must ALREADY have model representations.
- Once those models and transported points exist, joint marked-object
  canonicalization follows from the paper's algorithms. It should no longer
  be listed as a separate unexplained algorithmic primitive at fixed dimension.
- Weak scalar ambiguity has a concrete classical baseline: pairings reduce it
  to one sign per odd prime level. Enumerating these signs and applying the
  published interpolator reconstructs a compact isogeny representation in a
  subexponential, NOT polynomial, number of branches for the small-prime plan.
- There is also a polynomial classical test for whether a supplied polarized
  endomorphism descends through the hidden isogeny. This needs no full End(B)
  basis. It is a membership test, not a coset-separating hiding function.

The two latter statements are deductions under the stated geometric input
contracts, not implemented geometric algorithms. Their arithmetic components
are tested separately. Do not read a receipt of small integer calculations as
successful theta arithmetic.

Later same-day update: the adjacent `smooth-repolarization-2026-10-23` bundle
proposes an explicit stabilized converter in ORIGINAL dimension two, using
small prime-square torsion and a dimension-16 quotient. That new deduction
is review pending, not supplied directly by Theorem 7.1, not geometrically
executed, and not a general converter for all dimensions.

## 1. What Was Actually Read

The verified download is `/Users/jaspersands/Downloads/2026-1142.pdf`; an
identical copy is retained as `2026-1142.pdf` in this isolated bundle. SHA256:
`4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318`.
The relevant complete pages are 10-15, 33-40. Page 36 was additionally rendered
and visually checked to disambiguate the square-root bound. The public record
lists a CC BY license; credit the authors if retaining the PDF in the project.

The paper distinguishes representations from existence: Remark 3.2 says the
semantic maps are not algorithms. Axiom A3 guarantees representability, not a
converter for every informal description. Axioms A7, A22 and A25 supply
canonical models, isomorphisms and automorphisms for already represented PPAVs;
Section 6 establishes these for the theta model. Theorem 7.1 takes two such
PPAVs, a multiplier N, a coprime smooth auxiliary order M>N, and exact full-basis
images. Its time is (input length + largest prime factor of M)^poly(g).
Uniqueness holds for M>2 sqrt(2gN). Theorem 7.5 adds canonical representations
of polarized morphisms, not arbitrary new polarizations on varieties.

These imported algorithms are expected-time and dimension-sensitive. Fix g;
do not describe their bounds as uniformly polynomial in g. Nor does a compact
isogeny encoding constitute an explicit large-prime kernel basis.

## 2. Why The Existing Source Still Cannot Invoke Interpolation Directly

The repository supplies an original modeled (B, lambda_B) and a positive
integral symmetric automorphism

    H_M = I + phi T_M phi^dagger,
    lambda_M = lambda_B H_M.

It has a norm bound and paid, scalar-cancelled actions on selected small
torsion groups. What is missing is an actual geometric representation of
(B, lambda_M) together with point transport into that representation.

Calling Theorem 7.1 with that new PPAV as the codomain assumes the missing
object. Calling it with the OLD model changes the polarization condition.
Even an explicit program for H_M would not by itself be the claimed converter.
The formal possibility of encoding all PPAVs in A3 does not resolve this.

Concrete falsifier of the old-model shortcut: on a product E^2 with its
product polarization, set

    sigma = [[1,1],[0,1]],
    H = sigma^dagger sigma = [[1,1],[1,2]].

H is integral, positive, symmetric, determinant one and geometric degree one.
Thus lambda H is a principal polarization. Nevertheless

    H^dagger H = [[2,3],[3,5]]

is not [N] for ANY N, so H is not a polarized N-isogeny between the two OLD
product-polarized models. Degree one is not sufficient. At torsion level 3
the off-diagonal failure is invisible; level 5 detects it. In this example
sigma is known, so the new polarization is easy to model. It refutes the
shortcut, NOT the existence of a general converter.

## 3. Joint Canonicalization Is Available After Conversion

Assume every (B, lambda_M) and every marked point is already in the paper's
model, over compatible field presentations with the fixed embeddings required
by the source contract. For one object:

1. Compute the canonical polarized model C using A7.
2. Find ONE polarized isomorphism u:B->C using A22 and transport ALL levels
   with that same u.
3. Enumerate Aut(C) using A25. For each v, transform all marks with v.
4. At each small auxiliary order r, minimize the canonical ordered point tuple
   over ONE common unit multiplying that whole tuple. Do not scale each point
   independently. Orders may use different units.
5. Minimize the concatenation of these per-order tuples over the ONE v chosen
   in step 3, and include C in the label.

Changing u only permutes the outer finite automorphism orbit. Equal labels
give one common polarized isomorphism and the permitted per-order scalars;
conversely such an equivalence gives equal labels. This is exactly the joint
equivalence relation required in SIEGEL_MARKED_SOURCE_RIGIDITY.md.

At fixed g, the model's complete automorphism list and arithmetic are paid by
its complexity bound. Brute force over units costs O(sum r) at prime levels,
not O(product r). Canonical point encodings are essential. Independent
automorphism minimization at each order is still wrong. Quotienting points by
unrelated field Frobenius maps or unpolarized isomorphisms is still wrong.

For an eventual coherent source, compile and cap the complete classical
algorithm, including all field/model operations and failure records. One
cannot assume a coherent unitary from the expected-time statement alone.
Canonical outputs and verified Las Vegas retries would permit fixed random
tapes and a union bound over the finite query domain; that implementation and
its global clock have not been supplied here.

## 4. Classical Weak-Scalar Reconstruction Baseline

Assume A,B are already modeled PPAVs of fixed dimension g, and a polarized
isogeny phi:A->B has multiplier ell, coprime to the odd characteristic.
For each selected small odd prime r, coprime to ell and the characteristic,
the weak evaluator gives

    Q_(r,j) = [a_r] phi(P_(r,j)),

where a_r is ONE unknown nonzero scalar for the complete ordered basis.
The underlying phi is the same for every level. Pay for constructing these
points and for each weak call. Do not assume an oracle on secret ell-torsion.

Use the known polarizations and a pair with primitive Weil pairing. Relative
to its value, a small-r discrete logarithm of the image pairing yields

    e_r(Q_i,Q_j) = e_r(P_i,P_j)^(ell*a_r^2).

Consequently a_r^2 is computable. Its two roots are a_r and -a_r. Normalize
by one deterministically chosen root: the tuple is now either phi(P_j) or
-phi(P_j), with one COMMON sign at that level. Check all pairing entries,
not one alone; compatibility is necessary, not global-isogeny certification.

With s levels there are 2^(s-1) sign assignments modulo simultaneous global
negation. The discarded global negation is harmless because -phi has the same
kernel and multiplier. For each assignment invoke Theorem 7.1 on the original
modeled A,B. Use

    M = product r > ell,    M^2 > 8*g^3*ell^2.

The first condition is the interpolation algorithm's actual input condition.
The second is the repository's projective rigidity bound. A true assignment
exists; every successful assignment yields an isogeny with the original
kernel by that rigidity argument. The exact interpolator verifies the entire
geometric map, not merely the local pairing tables.

Taking successive small odd primes while omitting divisors of ell and the
characteristic, at fixed g one can use

    s = O(log ell / log log ell),   max r = O(log ell).

Thus sign enumeration costs exp(O(log ell / log log ell)) times the paid
fixed-dimension arithmetic/interpolation cost. This is subexponential in ell
but still superpolynomial in its BIT LENGTH. It is a source-upgrade baseline,
not a Shor-level algorithm and not an explicit kernel-coordinate solver.
Its novelty has not been established; related elliptic weak-representation
results must remain part of any later novelty comparison.

Failure modes: arbitrary per-point scalars do not satisfy this derivation;
prime powers may have more than two square roots and require separate handling;
the auxiliary point costs or number of branches can be prohibitive in practice;
pairing-compatible sign data can still fail global interpolation; a timeout
must remain UNKNOWN, not evidence that the input violates the geometric promise.

## 5. A Polynomial Descent Test Without End(B) Advice

There is a useful stronger deduction which avoids sign enumeration entirely.
In addition to the weak data above, supply an efficiently evaluable polarized
endomorphism a:A->A with multiplier N, coprime to the characteristic. Set

    gamma = phi a phi^(-1) = phi a phi^dagger / ell

in the rational endomorphism algebra of B. It satisfies gamma^dagger gamma=N.
It is integral if and only if a preserves K=ker(phi), by the universal
property of the quotient A/K. This is containment, not necessarily equality
if a is not invertible on K.

On B[r], write the known action of a in the supplied basis as A_r. In the
weak image basis Q_r, the predicted action of gamma is exactly A_r: the
unknown common scalar cancels. Thus exact candidate images gamma(Q_r) can be
computed using only point arithmetic. No basis of End(B) is supplied.

Choose smooth auxiliary M coprime to ell*N*characteristic with

    M > N,    M^2 > 8*g*ell^2*N.

Apply Theorem 7.1 to these candidate images between the OLD modeled B and B,
with multiplier N. If gamma is integral, the interpolator finds it. Conversely,
if it finds gamma_0, consider the INTEGRAL map

    Delta = ell*gamma_0 - phi a phi^dagger.

It kills B[M], hence Delta=M*theta for an integral theta. Both terms have
Rosati norm ell*sqrt(2gN), so ||Delta|| <= 2*ell*sqrt(2gN) < M. Integral
Rosati positivity forces theta=0. Therefore gamma_0=gamma and a preserves K.
This proves the test, including the false-positive exclusion at finite level.

The construction is polynomial in log(ell), log(N), and the paid input
length at fixed g, with the published expected-time arithmetic. It tests a
supplied POLARIZED a; an arbitrary degree-one unpolarized sigma is not such
an input. It also requires new enough auxiliary levels: insufficient original
marking data must not be silently enlarged without evaluator access.

Importantly, this produces only a membership answer for a stabilizer. Returning
one identical failure symbol outside it does not distinguish its other cosets.
Nor do the successful gamma encodings remain constant inside that stabilizer.
It is NOT the ordinary hiding oracle needed by the Rees or Siegel algorithms.
It also does not supply a saturated End(B) lattice. These are different tasks.

### An Actual False Positive At Insufficient Auxiliary Level

The strengthened M bound cannot be replaced by the interpolator's own
uniqueness threshold. On the elliptic curve E:y^2=x^3-x in characteristic 101,
let i^2=-1, s=6+5i, t=6-5i and Phi=diag(s,t) on E^2. Its multiplier is 61.
This curve is ordinary, not supersingular (101=1 mod 4); supersingularity
is unnecessary for this counterexample. The earlier adjective was incorrect.
Let a be the polarized automorphism swapping the two factors. Then

    gamma = Phi a Phi^-1 = [[0,s/t],[t/s,0]],
    s/t = (11+60i)/61.

This is not integral: the off-diagonal endomorphism would have nonintegral
Tate trace 22/61. At auxiliary level 5, however, gamma equals the factor swap
a. The latter is a genuine 1-isogeny between the original modeled E^2 and
itself. M=5 meets both M>N=1 and M>2 sqrt(2gN)=4, so even a correct, unique
published interpolation result would be a FALSE POSITIVE for descent.

The integral difference 61*a-Phi*a*Phi^dagger is nonzero but divisible by 5;
its squared Rosati norm is 24400. Our stronger condition M^2>8*g*ell^2*N
fails, as it should. This exact isogeny identity is an adversarial control,
not an executed geometric interpolation or an isogeny hardness benchmark.

## 6. Research Decision After Self-Critique

The new full text removes uncertainty about what this particular theorem
provides. Do not keep retrying the abstract or assume a conversion theorem
from its title. It does not prove the missing conversion impossible: another
construction from its quotient/product primitives might work.

The next constructive geometric question is specific: can a positive symmetric
H_M, available through bounded exact auxiliary actions, be turned into the
new principal-polarization model using explicit smooth-kernel quotients and
point transport, without assuming an End(B) lattice? An attempted product or
four-square construction must exhibit its actual isotropic kernel generators
and pay their torsion orders. The factorization/completion and point-transport
steps cannot be renamed as a model conversion.

If that succeeds, re-test classical attacks using the descent membership test
above and the already-established full-Hom/full-End advice attacks. If it does
not, pivot to another actual input mechanism rather than extending conditional
receiver parameter bounds. Prime-degree inverse-trace search also remains
unresolved: this pass did not find a new residual solver, and the 2025 vectorial
degree-stability paper [2504.03307](https://arxiv.org/html/2504.03307v2) does not
bound the normality of every scalar trace component.

## 7. Verification Boundary

`weak_marks.py` checks only exact pairing-exponent algebra, sign coverage,
resource thresholds and the E^2 matrix countercontrol. The Gaussian matrix
6+5i, multiplier 61, is used as an independently checked torsion-action control.
The factor-swap example separately checks a false-positive descent result at
insufficient auxiliary level, including its exact multiplier and Rosati norm.
No elliptic points, theta varieties, geometric interpolator, changed PPAV,
quantum circuit or secret kernel were computed. `replay.py` emits parameter
budgets and file hashes with those limitations explicit.

Run from this directory:

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q
    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python replay.py

The repository's qsearch/registry/UI and whole-repository validation are not
run or changed during migration. This is a research audit, not a new admission.

Verification: all ten isolated bundles passed in separate processes (333 tests
at that checkpoint); after adding the two descent countercontrols, this bundle
was rerun with 37 passing tests, giving 335 verified controls across unchanged
older bundles plus this final version. New Python syntax checks and the live
receipt replay pass. A single-process aggregate run previously had 332 passes
and one import failure because older standalone directories both name modules
`replay.py`; do not mistake that namespace collision for a failed scientific
identity or silently claim the aggregate invocation passed. Keep process
isolation until these standalone bundles are deliberately packaged.

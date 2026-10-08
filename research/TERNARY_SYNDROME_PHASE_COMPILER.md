# Initial Polynomial Frequency Chirps: Constructive Risk Equivalence

LOCAL DERIVATION / REVIEW PENDING. This removes a specific initial phase
operation for uniform-secret least-trit performance. It is NOT a generic
quantum/measurement lower bound, efficient decoder or novelty claim.

## Source, Prior And Nuisance Syndrome

Use the original full-root native source

    |psi_s>=3^(-M/2) sum_x chi_q(F(x).s)|x>, q=3^r.

Target t=s_j mod3 and average over ALL uniform secrets. Set Q=q/3. Define
S(x) to retain every OTHER frequency coordinate in full and only F_j modQ.
Write F(x)=S+Q*h(x)*e_j inside an occupied syndrome fiber, h in F3.
The fiber Born mass is C_S/3^M, independent of every secret. Conditional on S,
the source state, up to a common phase, is

    |v_(S,t)>=C_S^(-1/2) sum_(x:S(x)=S) omega^(t*h(x))|x>.

Thus it depends only on t. Uniform t remains uniform conditional on S. The
uniform-secret trit ensemble is ALREADY block diagonal in S: averaging over
all other coordinates and the high digits of s_j removes different-syndrome
matrix elements. Inserting a nuisance-syndrome measurement cannot alter this
ensemble's subsequent average score. This is not a statement about preserving
every individual pure secret state or pointwise algorithm success.

## Square-Zero Taylor Identity

Let P be any modular polynomial in the frequency coordinates with INTEGER
coefficients moduloq. Coefficients may be arbitrary known functions of public
labels; evaluating P is charged to its program size and arithmetic complexity.
Unit denominators such as2^-1 are represented by their integer modular inverses.
For r>=2, q dividesQ^2. Binomial expansion, over the composite ring itself,
therefore gives EXACTLY

    P(S+Q*h*e_j)=P(S)+Q*h*partial_j P(S) modq.

All higher-order terms have a factorQ^2 and vanish. No field replacement,
analytic approximation or assumption of low polynomial degree is needed.
For the initial known diagonal D_P|x>=chi_q(P(F(x)))|x>, this implies

    D_P |v_(S,t)> = chi_q(P(S))*|v_(S,t+g(S))>,
    g(S)=partial_j P(S) mod3.

In particular, a full-modulus quadratic chirp, even one entangling many word
registers, only translates the logical least-trit phase within each fiber.
Computing that initial chirp is not the missing frequency-fiber transform.

## Explicit Receiver Compilation

Consider ANY remaining receiver R, possibly label-dependent and collective,
and ANY trit decision rule d. The original pipeline starts with D_P then R.
Replace it by:

1. Reversibly compute public F(x) into clean scratch.
2. Copy ONLY S(x) to a separate register.
3. Uncompute FULL F scratch, including its target high trit.
4. Measure S; keep its classical value.
5. Run R unchanged on the original word registers, without D_P.
6. Return d+g(S) mod3.

The extra operations are polynomial public arithmetic, use no extra original
source copies and require no unknown-state preparation inverse or count table.
Measuring FULL F instead, or leaving its high trit in dirty scratch, destroys
the relevant phase and is not this compiler. Hardware gate export is not
supplied by a known arithmetic recipe.

For a branch S, chirped output probability at original t is the unchirped
probability at u=t+g(S). Change variables in the uniform t sum. The original
condition d=t becomes d+g(S)=u. Consequently the complete raw correctness
scores are equal, including every branch and failure outcome. This holds
for EVERY fixed public label matrix, not just IID population averages.
It preserves uniform-secret mean success, not success for each fixed secret.
If the original d ignores S, the replacement still uses S for its final shift.
If the original d already receives S, apply the same translation branchwise.

## Stronger One-Trit Compiler

It is unnecessary to measure full S. Since Q is divisible by3 at r>=2,
g(S)=partial_j P(S) mod3 equals g(F)=partial_j P(F mod3) mod3. Group the
already block-diagonal trit ensemble by this one-trit value. Within each group,
the same translation t->t+g applies to EVERY syndrome block; their individual
constant phases disappear. The minimal replacement therefore computes public
F mod3, copies the derivative trit, UNCOMPUTES its scratch, measures ONLY that
trit, runs R and adds the observed value to its decision. It does not compute
or retain full F or S. Only n low-frequency scratch trits and one output trit
are needed, plus arithmetic workspace charged to the phase program.

The source pure state may retain cross-syndrome coherence in an individual
run; the equivalence is for the uniform-secret ENSEMBLE, not a pure-state
identity. Complete secret-prior physical controls test the minimal measurement
directly, rather than claiming the stronger compiler from full-S runs alone.
Public coefficients need only be reduced modulo3, although their values may
still be functions of high labels. For a fixed quadratic P, all added quantum
control uses low labels. High-label circuit dependence alone is not the reason
that such an initial chirp would help least-trit inference.

The COMPLETE source batch used by R must be represented in F. R may use
public ancillas, but not additional same-secret source states, correlated
secret-bearing workspace or an unknown oracle absent from this ensemble.
Their frequencies would change the true nuisance blocks, invalidating the
measurement argument. This limitation is fundamental, not an implementation
detail. A partial-block P(F_A) is not generally a polynomial of TOTAL F and
is a genuine exception even when it is a simple quadratic in its own block.

No coherent frequency-fiber basis, witness solver or efficient R/d is created.
Exact MAP tables in finite controls are explicitly exponential references.
This is a constructive reduction of one search direction, not an algorithm.

## Genuine Exceptions, Not Blanket Phase Exclusion

- At r=1, Q^2 is not zero moduloq. P(F)=F^2 already violates the translation
  condition. The known final-field decoder is a separate fact; do not apply
  this Taylor compiler to the field root.
- A public top-digit phase P(F)=Q*(floor(F_j/Q))^2 modq is polynomial-time
  arithmetic but NOT a modular integer polynomial. Its three class values
  are0,Q,Q, which are not an affine trit character. The compiler correctly
  rejects it. This supplies a precise surviving phase primitive, not evidence
  of speedup or a solution to logical class-basis access.
- Polynomial phases interleaved AFTER a noncommuting mixing operation need
  not preserve the original syndrome fibers. They are not removed here.
- A phase depending on the original word beyond F(x), or a different secret
  promise/prior, needs a different argument.
- A quadratic on a PARTIAL frequency sum is outside the compilation. The
  native q81 control has words(0,0),(1,1),(2,2) with total frequencies0,27,54
  in one nuisance fiber, but first-block quadratic phases0,41,2. These cannot
  be a known affine trit shift. Do not mistake an initial partial-block chirp
  plus subsequent joint readout for the removable total-frequency chirp.
- Arbitrary initial public diagonal functions are not excluded. Their exact
  three-class phase test determines whether this particular relabeling applies.

Thus "high-label dependence" and "entangles the words" are not sufficient
reasons to promote an initial smooth frequency chirp. Nonpolynomial carry/
top-digit phases or a prior noncommuting collective operation are more precise
constructive targets. They still must supply useful readout and costed decoding.
Partial-block collective phases are another concrete surviving target.

## Evidence And Refutation

The producer records exact three-class certificates through r64 and genuine
native full-frequency controls, including the prespecified q81 correlation
source and an unfiltered random q729 source. Exact syndrome/output probabilities
use cubic character counts, not floating inference or selected heralds. The
chirped MAP reference and compiled unchirped rule have IDENTICAL rational
uniform-trit correctness. Actual full-root phases and Fourier readout are
replayed for zero, primitive, nonprimitive and full secrets. Word/output and
source counts are charged as finite calibration, not scalable execution.
The one-trit compiler additionally replays ALL uniform secrets, not only those
four controls. Dirty full-frequency scratch is physically checked to erase
trit dependence. A constant-decision countercontrol shows why equal mean
success must not be promoted to equal success for each secret trit.

Falsifiers: a polynomial violates square-zero Taylor at r>=2; true Born branch
weights differ from C_S/3^M; class laws disagree with the physical projection;
the compiled risk changes; the recipe retains target-high tags; or root-one/
top-digit exceptions are falsely accepted. Independent review of the prior,
decoder translation and physical clean-workspace construction remains owed.

The standalone verifier reconstructs the native ideal chart, all occupied
syndrome words, 38,664 exact cubic-character probabilities and both decoder
risks. It checks bounded physical replay residuals but does NOT independently
reexecute those floating gate controls. Python tests separately replay the
complete secret ensemble, including a multivariate source. Root-one, top-digit,
partial-block and pointwise-guarantee mutations must be rejected.

```
python theorems/ternary_syndrome_phase_compiler.py --write
node research/certificates/ternary_syndrome_phase_compiler_crosscheck.js
python -m pytest -q tests/test_ternary_syndrome_phase_compiler.py
```

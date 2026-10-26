# Biased Ternary Decoding For Prescribed Types

WRITTEN DERIVATION, INDEPENDENT REVIEW PENDING. No new quantum advantage,
native quantum execution, or novelty claim. The explicit calibration is
classically easy. This is a constructive extension of the preceding
[balanced transfer](TERNARY_TYPE_TRANSFER.md), not a type-parameter sweep.

## Scientific Question

Can a quantum product decoder handle a prescribed ternary histogram that
is exponentially rare under its original uniform source? Directly applying
its independent local measurements to an entangled fixed-type source is
invalid. Instead, change the product source and pay for a different decoder.

[Ragavan and Shutty](https://arxiv.org/html/2610.00502v1), Sections2.1,5
and1.4, provide the two-fold multiplication decoder and motivate combining
quantum decoding with global constraints. Their classical three-fold
algorithm remains a mandatory baseline. Below is our written biased-source
extension of this framework, not a claim that its ingredients are new.

Input: explicit independent rows of a ternary code D, dimension k, length m,
with Schur square W=D*D of dimension s2. Require a proved bound

    wt(d-a*1) >= dstar, for every nonzero d in D and every a in F3.

In particular, D excludes the constant direction. The output is a full-support
vector y with Dy=0 and exactly h entries +1. Here Dy denotes multiplication
by the supplied generator matrix. If a constant row is appended, its RHS
must be (2h-m) mod3. A pre-existing homogeneous constant row is compatible
ONLY when that value is zero. We do not change an incompatible problem.

No oracle, secret advice, or free minimum-distance test is granted. Numerical
parameter input to the ledger does not certify an arbitrary code.

## Local Decoder With Retained Erasures

Let p=h/m in (0,1), q=min(p,1-p), rho=2q, and omega=exp(2*pi*i/3).
The local input with codeword symbol c is

    |psi_c> = sqrt(p)*omega^c|+> + sqrt(1-p)*omega^-c|->.

Apply the label-independent filter

    K = diag(sqrt(rho/(2p)), sqrt(rho/(2(1-p)))).

Its success probability is rho for EVERY classical c. On success it gives
the uniform trine state. Measure with the exclusion POVM
E_a=(2/3)|v_a><v_a|, v_a=(omega^a,-omega^-a)/sqrt(2).
Outcome a excludes a; its pair F3\\{a} always contains c. Each of the two
possible exclusions occurs with unconditional probability q. The remaining
probability 1-2q is an erasure. No failed coordinate is replaced for free.

The producer gives the explicit four-outcome isometry and a unitary
completion. On failure, the surviving dominant-symbol state has a
c-dependent global phase. Retaining that phase and all workspace is
essential to coherent inversion. The classical-c law above is NOT assumed
to hold independently on a coherent sum of codewords.

## Projected Schur-Square Recovery

For a conclusive pair {a_i,b_i}, solve the linear equations

    w_i - (a_i+b_i)*v_i + a_i*b_i = 0,    v in D, w in W.

Erased coordinates supply no equation. The true pair (c,c*c) satisfies
every equation. Recover v only when its projection is unique. Requiring
the auxiliary w to be unique is unnecessarily restrictive and is NOT
justified by a distance bound on D. A test explicitly leaves one auxiliary
degree of freedom while recovering v uniquely.

For a wrong v=c+e, e!=0, put u=w-c*c-2c*e in W. At a conclusive coordinate,
write the pair as {c_i,t_i}; the equation is

    u_i = e_i*(t_i-c_i).

Where e_i!=0, at most one of the two equally likely false entries can
satisfy a fixed u_i. With erasures retained, the coordinate passes with
probability at most (1-2q)+q=1-q. Conditional on a classical codeword,
coordinates are independent. A union bound over e and u gives

    delta <= min(1, 3^(k+s2)*(1-q)^dstar).                 (1)

This bounds decoding failure uniformly in c; it is deliberately loose.
Solutions with e=0 and ambiguous u are NOT failures. The implementation
uses Gaussian elimination and projected-nullspace uniqueness, not an
enumeration over codewords. Reversible elimination, deterministic fallback,
and its inverse have polynomial Boolean circuit size.

## Weighted Sampler And Type Probability

Prepare a uniform coherent code label, its controlled product phase state,
apply the decoder U, subtract the decoded label, then apply U inverse.
Retain all failures. The same norm estimate as the balanced transfer gives
output TV distance at most

    eta = min(1, 4*sqrt(3^k*delta) + epsilon_circuit)       (2)

from the weighted kernel law

    mu_p(y) proportional to p^(#plus)*(1-p)^(m-#plus),
    supported on Dy=0, y in {+1,-1}^m.

The 3^k coherence factor and ideal-state normalization cannot be omitted.
Indeed, the unnormalized ideal state has norm squared 3^k times the
unconditioned product probability of Dy=0. A small classical-codeword
decoder error does not itself imply a useful sampler.

For counting, put L=3^k, r=min(floor(m/2),dstar),
beta=sqrt(1-3p(1-p)), alpha=1-p(1-p), and

    mass_h = binom(m,h)*p^h*(1-p)^(m-h).
    e_full = (L-1)*beta^dstar.
    e_type = (L-1)*alpha^r.

Every nonzero character has magnitude at most beta at a nonzero coordinate.
For two unequal symbols, the product of the weighted character-factor
magnitudes on the unit circle is at most alpha. To check the latter, set
A=1-2p(1-p), B=2p(1-p). The squared product is

    A^2 - A*B*z + B^2*(z^2-3/4),  -1<=z<=1.

It is convex and maximized at z=-1, giving (A+B/2)^2=alpha^2.
One can match r unequal-symbol pairs in every nonzero codeword: the maximum
matching size in its complete multipartite symbol graph is
min(floor(m/2),m-max_symbol_count). Cauchy's coefficient bound therefore
gives e_type, without enumerating codewords or assuming a random matrix.
Character orthogonality now yields

    mu_p(exact type h) >= p0 = max(0,(mass_h-e_type)/(1+e_full)).

Verify both constraints on every output. If a=p0-eta>0, at most ceil(b/a)
fresh full sampler calls give failure <=exp(-b)<=2^-b. On acceptance, the
TV error to the uniform fixed-type solution law is at most min(1,2eta/a).
The cap is computed from the displayed outward-rounded lower bound.
No amplification, free retry, or success-only runtime is claimed.

For p bounded away from0 and1 and h=pm, mass_h=Theta(m^-1/2).
Sufficient margins are e_full=O(1), e_type=o(m^-1/2) and eta=o(m^-1/2).
Equations(1)-(2) make the lost decoding exponent explicit; bias is not free.
In this regime the overhead is O(sqrt(m)*b) FULL base calls, even when the
same type is exponentially rare under the uniform product source.
State preparation, coherent linear algebra, verification, and compilation
to total error epsilon_circuit are all charged polynomial costs.

## Executed Controls

The growing calibration evaluates linear forms on nonzero points of F3^6:
m=728, k=6, s2=21 (matrix rank checked), dstar=485, h=243, p=243/728.
All nonzero words have profile (242,243,243). Exact integer character
coefficients and rational weighted counts give:

| Quantity | Value |
| --- | --- |
| Uniform-source prescribed-type probability | 4.907581228743153e-20 |
| Biased-source prescribed-type probability | 0.03134208662555295 |
| Full sampler call cap, failure <=2^-40 | 1277 |
| Assumed compiled-circuit TV budget | 2^-64 |
| Appended constant-row RHS | 1, not0 |

These are theorem-ledger values, NOT measured quantum sampler outcomes.
This family has 3^k=m+1 classical syndromes; exact syndrome-and-count
dynamic programming samples its fixed-type solutions in polynomial time.
It therefore supplies NO advantage evidence.

An actual four-coordinate coherent control uses the local isometry,
Schur-square decoder, label subtraction and inverse, retaining all256
work dimensions. The always-zero decoder returns the original product
law and has TV16/27 from the desired weighted kernel law. Dense unitary
completion here is an identity control, not a growing hardware compiler.

## Adversarial Assessment And Next Decision

- Extreme bias makes erasures common and the decoder bound useless. The
  checked h=1 ledger blocks the claim. This is not a solution for all types.
- Cheap exact counting is special to the calibration. There is no general
  counting oracle or classical hardness conclusion.
- The two-fold/three-fold distinction may collapse under stronger classical
  algorithms. A biased sampler does not establish a separation.
- Homogeneous constant constraints can make the requested type impossible.
  The native control flags this rather than changing the RHS silently.
- The proof does not apply independent local outcome probabilities to an
  entangled fixed-type input or a coherent codeword sum.
- No finite test proves the asymptotic decoder or coefficient estimates.
  Both written arguments require independent mathematical review.
- Tilting, filtering, coherent decoding and rejection are established ideas.
  Novelty of this combination has not been established.

DECISION: prescribed interior ternary types are no longer, by themselves,
a reason to build a new entangled-decoder subsystem when these margins hold.
Do not follow this with a histogram/tilt sweep. The meaningful next task is
a useful explicit problem family in a two-fold decoding regime that survives
the classical three-fold algorithm and other concrete samplers, or an
external reduction with a useful output. Independent review of this transfer
is also warranted. Larger easy calibrations would not address either need.

## Reproduce

    python -m theorems.ternary_tilted_type
    python -m pytest -q tests/test_ternary_tilted_type.py \
      tests/test_ternary_type_transfer.py tests/test_ternary_decoder_filter.py \
      tests/test_ternary_quotient_decoder.py -W error::RuntimeWarning

Artifacts: `theorems/ternary_tilted_type.py`,
`tests/test_ternary_tilted_type.py`,
`research/reductions/ternary_tilted_type.json`. No central admission or
CLI/UI wiring; no previous producer or report was overwritten.

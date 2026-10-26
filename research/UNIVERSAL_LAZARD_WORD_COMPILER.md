# Universal Lazard Word Compiler

2026-10-22. Known inverse-BCH construction with exact public certificates.
This removes the class-four word-backend limit from the free Lazard input
bridge. It is not a new quantum algorithm or a novelty claim.

## Contract And Prior Art

Input: opaque uniquely encoded x,y in an exponent-p group of class at most
a FIXED c, known odd prime p>c, identity and public group multiplication.
Compute exp(log x+log y) and exp([log x,log y]). No target Lie coordinates,
decoder, relation kernel, root oracle, hidden source or enumeration is used.
The group, class and exponent promises are external, not compiler-certified.

Effective inverse BCH is established machinery; the
[Cicalo--de Graaf--Vaughan-Lee publisher abstract](https://www.sciencedirect.com/science/article/pii/S0021869311007009)
describes inverse-formula algorithms. Its full paper was unavailable, so no
unread complexity details are imported. BOUNDED_CLASS_METABELIAN_HSP.md
records inspected GAP LieRing code and stored tables through weight14.
This implementation neither copies them nor extrapolates a finite table.

## Construction And Proof

Work in the public free associative algebra on X,Y over Q, retaining words
through length c, with exact truncated exp/log. Addition starts at
W=exp X exp Y; bracket starts at exp X exp Y exp(-X) exp(-Y).
The group commutator convention here is xyx^-1y^-1.

If log W agrees with target P through degree k-1, its degree-k residual R
is a homogeneous Lie polynomial. Dynkin--Specht--Wever gives

```
R = (1/k) sum_(length-k words w) coeff_w(R) * nested_bracket(w).
```

This is the standard projection identity; see the
[Laue survey, DSW criterion](https://radon.mat.univie.ac.at/~slc/s/s29laue.pdf).
The implementation also expands every nested bracket and checks the
identity coefficientwise. It does not treat an arbitrary polynomial as Lie.

The corresponding right-nested GROUP commutator C_w has logarithm equal
to nested_bracket(w) modulo degrees greater than k. Append the factors
C_w^(-coeff_w(R)/k). They have degree at least k, so their cross terms with
the current logarithm have degree greater than k. The degree-k error is
canceled without changing earlier degrees. After k=1,...,c, log W=P in
the free class-c Lie algebra, hence in every promised target by substitution.
The target need not itself be supplied as a nilpotent associative algebra.

Coefficients remain in Z[1/c!]: exp/log only divide by integers with prime
factors at most c, and projection divides by k<=c. No arbitrary rational
matrix inversion adds denominators. Each rational power a/b becomes the
ordinary integer power a*b^(-1) modulo p. It is not a root or discrete-log
oracle. The condition p>c is essential.

A certificate is a straight-line program of multiplication and rational
powering with earlier-value references. Its verifier replays exact rational
arithmetic, checks denominator support and every filtration stage, and
compares the full final expansion with exp(X+Y) or exp([X,Y]). This is a
replayable algebraic certificate, not a proof-assistant-verified theorem.

## Costs And Integration

M multiplication and P powering instructions cost at most
M+2*bit_length(p)*P public multiplications. Coefficient arithmetic is paid.
Symbolic preprocessing, word length and coefficient bit sizes depend only
on c, potentially very badly. There is NO uniform polynomial-in-c claim.
All runtime branches depend on public exponents, not opaque element values.
Reversible evaluation must still pay for workspaces and cleanup; no native
quantum circuit or hidden-subgroup receiver is synthesized here.

`theorems/universal_lazard_words.py` supplies compilation, verification and
opaque evaluation. `OpaqueFreePullback` uses it for c>4 or p=3, retaining
the shorter class-four formulas on c<=4,p>4. The old formulas are an explicit
classical implementation baseline and are cheaper on their valid range.
Free dimension and the subsequent Rees recovery costs are still paid.

## Falsifiers And Tested Scope

- Exact certificates for both operations through class eight. General c
  follows the construction argument, not extrapolation from finite tests.
- Opaque unitriangular matrices at classes one through six, close-boundary
  primes, and a 127-bit class-five case. Independent matrix multiplication
  and matrix exponential give ground truth, not the compiler's own BCH.
- A genuine class-five free pullback, with nonzero top-degree images and
  homomorphism tests, plus the p=3,class-two fallback. No target coordinates
  are passed to the compiler.
- Altered powers, outputs, stages and forbidden denominator primes fail
  verification. An inadequate class-four word fails on a class-five target.
- The first run exposed a cache-key type collision accepting a noninteger
  class after a cached valid call. Typed caching fixes it. This was an input
  validation bug, not a failed algebraic identity.

Run `python -m theorems.universal_lazard_words --write` for standalone
certificates through class six in research/reductions/universal_lazard_words.json.
Tests are in tests/test_universal_lazard_words.py. No registry admission.

## Remaining Scientific Work

This closes a local public-word implementation gap. It does not validate
the Rees composition, implement its general SDE solver, remove outer
reductions, establish novelty, or supply a natural hard application.
Next prioritize adversarial scrutiny of that universal composition and
comparison to existing algorithms, not optimization of known word formulas
or another small-group benchmark campaign.

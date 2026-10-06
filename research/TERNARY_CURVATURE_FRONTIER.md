# Multi-Output Curvature Frontier

LOCAL DERIVATIONS / REVIEW PENDING. Exact optimal F3 curvature compiler and
full-root source falsifiers; no accepted candidate or full-depth decoder.

## The Question

The exact cyclic extractor fixed the reversible partition but exposed a
single-output recursion cost. Can an affine native coordinate change retain
many logical registers rather than one? Yes at the LOW phase level; no automatic
claim of independent full-root outputs survives. This pass makes both statements
precise and testable.

## Necessary And Sufficient Low-Phase Criterion

Original even-native qutrit frequencies are `f_i(0)=0,f_i(1)=a_i,f_i(2)=c_i`
at `q=3^r`. For `B_i=a_i+c_i mod3`, their component polynomial is

```text
f_i(x) = (a_i+B_i)*x + 2*B_i*x^2 mod3.
```

Let an affine branch have original word `x=anchor+S*z mod3`, where columns
of `S` are independent. For EVERY secret component l, the retained low phase
is affine in z if and only if

```text
S^T diag(B_1l,...,B_Ml) S = 0 over F3.
```

This is simultaneous total isotropy, not just zero curvature on each column:
cross-column polar terms must vanish too. The criterion holds for every measured
complement. Affine translations and arbitrary tangent values only change linear
and constant terms, not this Gram matrix.

The coordinate compiler completes S to an invertible F3 basis and explicitly
decomposes its inverse into SWAP, SCALE and SUM gates. All original words are
mapped bijectively. Only complements are measured; every outcome is accepted.
If pointers stay coherent, their unknown anchor phases must remain.

## Sharp Scalar Geometry

The finite-field classification is established mathematics, not a new theorem;
see [Casselman, Theorem 1.6](https://personal.math.ubc.ca/~cass/research/pdf/FiniteFields.pdf).
A nondegenerate odd-rank form has one anisotropic dimension; an even-rank form
is either split or has an anisotropic plane. Add the radical dimension for
degenerate diagonal forms.

For a scalar curvature array, let z be the zero count, R the nonzero count,
and t the count of twos. The exact maximum is

```text
z+floor(R/2),                                      R odd or zero;
z+R/2,                                            R>0 even, R/2+t even;
z+R/2-1,                                          R>0 even, R/2+t odd.
```

The local compiler attains it without search: retain zero wires; pair one with
two; on each remaining same-sign four-block use columns `(1,1,1,0)` and
`(1,2,0,1)`; a final same-sign three-block supplies one column `(1,1,1)`.
One- and two-site same-sign tails supply none. Rank and determinant parity
give the matching upper bound. This is polynomial public label arithmetic,
not an inverse of an unknown quantum state.

For multiple secret components, every scalar combination of curvature forms
gives a necessary bound. The implemented screen checks basis and pair directions
in polynomial time. It exhausts projective directions only for n<=2 and does
NOT construct an optimal simultaneous frame in general.

## Exact Fresh-Source Average

With fresh IID native labels, one curvature coordinate is uniform F3. Its rank
is `Binomial(M,2/3)`. Conditional on positive even rank, the two determinant
types are equally likely. The conditional expected maximum is therefore
`M-R/2-1/2` for every positive R, and M at R=0. Thus

```text
E maximum low-affine width = 2M/3 - (1-3^(-M))/2.
```

Any simultaneous frame has at most this expected width. This is a bound on a
SPECIFIC affine, complement-measured, low-affine representation. It does not
bound arbitrary quantum algorithms or computational-basis nonlinear maps.
Do NOT multiply this fraction across root levels unless the required fresh
conditional IID curvature law has actually been proved. The retained joint
state generally does not have that law or independent native factors.

## Full-Root Counterexample

Use four ORIGINAL native q9 inputs with frequencies `(a_i,c_i)=(0,1)`.
These are legal deterministic source controls, not claimed fresh random data.
All curvatures equal one. The optimal two-column frame above is totally
isotropic. After an actual gate recipe and pointer-zero measurement, the FULL
frequency table on logical `(z1,z2)` is

```text
0 1 2
0 1 2
3 1 2
```

It is affine mod3, but its full-root mixed defects at `(2,1)` and `(2,2)`
equal six mod9. A product phase would require BOTH defects to vanish.
At secret1 the first-register purity is EXACTLY `19/27`, strictly below one.
This is not numerical evidence alone: independent cube-root Gram arithmetic
gives `57/81=19/27`. At secret0 the calibration state is product, which does
not repair the unknown-all-secret source promise.

This purity is computed with a KNOWN calibration secret, not estimated by an
implemented unknown-secret receiver. A SWAP test requires identical labeled
input states; fresh random sources do not supply those, and cloning is not
available. Any proposed entanglement-based readout must supply and charge its
matching-copy/instrument requirements instead of treating this diagnostic as
a free weak-trit oracle.

The gate implementation replays ALL nine complement branches, each with
probability1/9. No favorable branch is singled out for acceptance. A separate
zero-curvature identity-frame control retains all four product qutrits and
passes full-root separability. The system does not declare all compression
impossible or the easy control classically hard.

## What This Kills And Leaves Open

- Killed: treating a curvature-free logical coordinate list as independent
  full-root native phase samples. Both individual isotropy and total isotropy
  are insufficient for that higher-root product claim.
- Killed: advertising an affine low-phase compiler as lossless on generic
  fresh original labels, or iterating a fresh-source average without a source law.
- Still open: process the entangled full-root phase state directly, retaining
  its mixed terms, or use genuinely nonlinear source-valid instruments.
- Still open: exploit correlations across logical outputs without calling
  them IID samples, with a computable secret estimator and recursive resource law.
- Not supplied: coherent full-root inverse, unknown preparation, cloning,
  natural-problem acquisition, qubit synthesis/error accounting, speedup proof.

The next valuable object is a JOINT phase transducer with a controlled growing-
depth mixed-phase representation and an actual information-preserving decoder.
Another acceptance sweep, dense optimum plot, or simple tensor count is not
the missing algorithm.

## Verification

36 focused tests: all 81 four-wire curvature arrays times all 212 subspaces;
exact low-affine criterion; scaled optimal frames through M512; whole-basis gate
inverses; full-root entanglement and product controls; multi-component screens;
complete IID averages through M6; invalid-source and bounded-replay guards.
The original n4/L16/M100 parent control also receives all 16 polynomial
basis/pair scalar screens, with 6,400 public multiply-adds. No dense quantum
output, simultaneous optimum, or secret estimator is claimed for this control.

```sh
python theorems/ternary_curvature_frontier.py --write
python -m pytest -q tests/test_ternary_curvature_frontier.py
node research/certificates/ternary_curvature_frontier_crosscheck.js
```

Gemini/Antigravity owns routine CLI/registry/site/full-suite wiring. Register
the failed curvature-to-product implication as a negative result, not this
entire source family as dequantized or a generic algorithm no-go.

# Native Affine-Line Extraction: Clean Implementation, Typical Coverage Barrier

LOCAL DERIVATION / REVIEW PENDING. No novelty or speedup claim. This tests a
constructive NONLEXICOGRAPHIC alternative to the batch-fiber reference. It
does not rule out nonlinear partitions, source-state approximations or
coherent interference between direction registers.

## A Real Implementable Partial Instrument

Use the original even-native integer-secret model with parent q=3^r, r>=2,
M input qutrits and n frequency coordinates. Reduce the two full frequency
rows a_i,c_i modulo3 and write

    A_i=c_i-a_i, B_i=2*a_i-c_i, F(x) mod3=A*x+B*x^2.

Squaring and addition in this section are coordinatewise over F3. The
transformation (a_i,c_i)->(A_i,B_i) is invertible; under IID full native
labels, A and B are independent uniform n-by-M matrices over F3.

Choose a NONZERO direction v from LOW labels only, normalized to have its
first nonzero coordinate p equal to1. Then

    F(x+t*v)-F(x) mod3
      =t*(A*v+2*B*diag(v)*x)+t^2*B*v^2.

An entire three-word line has the same prefix iff BOTH B*v^2=0 and
A*v+2*B*diag(v)*x=0. A single equal pair does NOT certify the third word.

There is a clean O(n*M) finite-field circuit for a supplied v: replace x by
u=x-x_p*v and t=x_p, omit u_p=0, compute the success predicate on u, copy ONE
success bit and uncompute all arithmetic scratch. Measure that bit. On
success measure the M-1 coordinates of u, leaving t. The map x<->(u,t) is
an explicit linear bijection, not a table, counting oracle or guessed inverse.
Computing a favorable direction is a SEPARATE cost; no efficient direction
finder is supplied here. The audit exhaustively enumerates directions only
in bounded calibration cases.

Every accepted u has three equally weighted original words. Its raw Born
mass is3/3^M independently of every secret. The remaining qutrit has child
root q/3 and rows (F(u+v)-F(u))/3, (F(u+2v)-F(u))/3 modulo q/3, after taking
the parent differences modulo q. It is ONE child per successful actual batch.
Under low-only selection and fresh IID high lifts, the pointed unit-minor
argument from the batch audit gives the independent uniform child-row law.
It is not a histogram claim for a fixed full label instance.

## Exact Coverage, Not Just Existence

Let S be the support of v and R=rank(B_S)=rank(B*diag(v)). If B*v^2!=0 or
A*v is outside the column space of B_S, coverage is ZERO. Otherwise the good
set is an affine subspace of dimension M-R, and its raw probability is

    alpha(v)=3^(-R).

Goodness is constant along each v-line since B*v^2=0. The good set therefore
has exactly3^(M-R-1) accepted tags. Solving the linear predicate is easy,
but preparing only its good words would be ungranted postselection unless
the actual probability is charged. Measuring many predicate values or
declaring every potential tag an output does not improve coverage.

An all-zero B gives an easy positive control: kernel directions of A can
have coverage1. Such labels are allowed, but not representative of IID
native frequency pairs. Even finding a nonzero diagonal-equation solution
B*v^2=0 is insufficient: its support rank controls extraction probability.

The EXISTING curvature-only even-to-odd extractor produces precisely the
structured promise B=0 modulo3 for its odd children. Its following kernel
line can therefore lower the root with acceptance1. This audit does NOT
exclude that baseline or call its odd inputs IID original even inputs. The
baseline's repeated source fan-in, not its per-step acceptance, is the gap
identified in the [cyclic extractor audit](TERNARY_CYCLIC_EXTRACTOR.md).

The [word-dependent invariant-kernel action](TERNARY_SHALLOW_KERNEL_CYCLE.md)
now implements that baseline coherently. Its direction can vary with an
original word's orbit-invariant tangent records, realizing exponentially
many implicit choices with a polynomial program. The explicit-menu theorem
must NOT be applied to that larger class.

## Uniform Barrier For Polynomial Direction Menus

For an IID uniform n-by-M B, any fixed nonzero coefficient vector w has
Pr[B*w=0]=3^(-n). The exact union bound for a nonzero kernel vector of weight
at most s is

    eta_s <= min(1, 3^(-n)*sum_(k=1)^s binom(M,k)*2^k).

Outside that event, EVERY feasible direction v has support rank at least s:
B_S*1=0 gives a dependent support. If R<s, a minimal dependent subset of
its columns has size at most R+1<=s, contradicting the event's complement.
This uses general coefficients in F3, not the false assertion that a short
positive-sum subset must exist.

Thus ANY menu of at most T directions chosen AFTER inspecting ALL low
labels, and any success set consisting of their good original lines, obeys

    E[raw accepted probability] <= min(1, eta_s+T*3^(-s)).

On good instances the union bound is over source-word measure, not over
independent directions. Dependence between menu choices is harmless. On the
exceptional label instances use probability<=1. Additional rank-consistency
failures only strengthen the upper bound. For the relevant M>=n batches with
M and T polynomial in n,
choose s=Theta(n/log n) small enough that eta_s decays exponentially; then
T*3^(-s) is superpolynomially small. More polynomial input qutrits do NOT
turn this specific simple instrument into a polynomial-supply extractor.
The report supplies exact rational bounds rather than extrapolated fits.

This is NOT an exclusion of coherent direction superpositions, noncommuting
receivers, nonlinear triple partitions, arbitrary adaptive state reshaping
or average-case approximate compilation. A menu is a set of classical
directions whose success words form a union of original affine lines. A
clean priority partition of overlapping lines is itself not automatically
available. Its best possible coverage is still no larger than that union.
No source-preparation inverse is granted, so amplitude amplification is not
a free repair. No generic quantum lower bound or classical dequantization
of original unknown input states is asserted.

## Revised Research Decision And Falsifiers

Keep the affine instrument as a constructive benchmark, NOT the principal
compiler target. A viable next mechanism must avoid the low-rank-menu
barrier: a costed nonlinear partition, interference between directions, or
a source-state-specific transform with an explicit error/output-law proof.

Falsifiers: a supplied native line violates the true prefix equation; any
word is dropped by the linear coordinate map; actual success differs from
0 or3^(-R); an accepted branch has the wrong child phase; a claimed sparse
kernel-free matrix admits a feasible direction of rank below s; or a menu
claim exceeds its exact bound while retaining the stated original-line model.
The small positive and negative controls are calibration, not novel oracle
problems or accepted candidates.

```
python theorems/ternary_affine_line_extractor.py --write
node research/certificates/ternary_affine_line_extractor_crosscheck.js
python -m pytest -q tests/test_ternary_affine_line_extractor.py
```

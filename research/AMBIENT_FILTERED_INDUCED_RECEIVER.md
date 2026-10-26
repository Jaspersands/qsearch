# Ambient-Filtered Induced Receiver

2026-10-22. Constructive refinement of the provisional receiver, with
public coordinate certification, coefficient algebra and conditional
resource accounting. Not an executed quantum algorithm, independent
end-to-end verification, novelty certificate, or demonstrated speedup.

## 1. The Change

The old induced route bounds every potential coordinate by ambient class
c, and every cocycle by normal class k, producing phase degree kc.
That ignores the ambient lower-central filtration. A deep potential
coordinate cannot interact with arbitrarily many other deep coordinates
in a class-c Lie algebra: the resulting bracket is zero.

Choose public coordinates adapted simultaneously to that filtration and
the abelian fiber I=N', where N=L'. Give each coordinate its ambient
weight w. Its potential degree is at most w. Retain full Taylor jets of
these DIFFERENT degrees in the A=N/I coordinates. The scalar phase then
has weighted degree at most c, not kc. The ordinary readout phase has
degree at most the largest A weight, not necessarily c.

For the actual class-nine/derived-class-four witness:

| Quantity | Previous Support Bound | Ambient-Filtered Bound |
| --- | ---: | ---: |
| A coordinate degree cap | 9 uniformly | (6,5,4,4,3,3,2) |
| Weighted erasure degree | 36 | 9 |
| Ordinary erasure degree | 9 | 6 |
| Total erasure stages | 45 | 15 |
| Retained jet width, m=2 | 1155 | 155 |
| Scalar feature count | 165 | 56 |
| Formal potential coefficients | 935 | 456 |
| Sufficient query ceil-log2, p=43 | 333018 | 4496 |
| Sufficient query ceil-log2, p=2^127-1 | 333022 | 4501 |

The query numbers are CEIL logarithms of sufficient upper bounds for one
transverse image call, at epsilon=1/8. They are not measured costs or
lower bounds. Even the smaller bound is impractical. Both erasure trees
remain; this is not a constant-copy, all-at-once cancellation technique.

## 2. Input And Public Filtration

Use the explicit Lie/ordinary-oracle model of
INDUCED_RECEIVER_COMPOSITION_THEOREM.md: finite-dimensional L over F_p,
fixed class c, N=L' with nonzero abelian N', and initial transverse H.
No hidden potential coefficients, subgroup basis, projection onto its
image, or coherent potential evaluator is supplied. Scalar/abelian
branches and arbitrary-H recursion retain their existing roles.

The filtered image construction uses the conservative condition p>2c.
This implies the Lazard requirement and the feature-rank condition below.
Its source/degree argument does not require p>kc. The old uniform-degree
compiler keeps its stricter guard: supplying new integers to that old
path is NOT an implementation of the filtered construction.

Let gamma_j=gamma_j(L), I=N'. Construct a basis of I adapted to
I intersect gamma_j, by descending j and extending a basis. Then choose
A vectors by descending gamma_j and extending modulo ALL of I. Order
the result as A followed by I, recording weight j when a vector is added.
The resulting basis e_i satisfies

```
gamma_j = span{e_i : w_i >= j},       j>=2,
[e_i,e_l] has components only of weight >= w_i+w_l.
```

Thus N=A+I is a FILTERED vector-space splitting. A need not be a Lie
subalgebra, and L need not be graded. Nonzero brackets may have weight
STRICTLY greater than the sum. The construction uses public finite-field
linear algebra and actual Lie brackets, with no H-dependent choices.

ambient_filtration_certificate verifies the actual flag equalities,
N', its abelianness, and every normal structure constant. Its ambient
bracket must already be a genuine bilinear Lie bracket; an arbitrary
Python callable does not certify Lie axioms. The matrix controls supply
those axioms independently. FilteredNormalChart alone checks the weighted
normal tensor, NOT its embedding or the degree origin of Q.

## 3. Origin Of Every Coordinate Degree

The proof-only section potential is the existing word

```
Q(q)=log(exp(X(q)) exp(Y(q)+Z(q)) exp(-X(q)-Y(q))),
```

with X,Y,Z linear in q and Z valued in N. Each homogeneous term of
quotient degree d is a sum of length-d Lie words and lies in gamma_d.
The linear term is Z, so the whole polynomial is valued in N.
The coordinate functional of e_i kills gamma_(w_i+1). Therefore

```
degree(Q_i) <= w_i.
```

This holds coefficientwise as a formal polynomial, not just as a
function on F_p. All original hidden retraction/lift constraints are
still needed to derive the source; the compiler overestimates by allowing
arbitrary formal coefficients within these bounds.

AmbientPotentialFiltration.lean now has KillsAboveWeight,
filtered_word_projection_zero, filtered_term_bound and
filtered_polynomial_bound. They derive the coordinate bound from actual
lower-central membership and annihilation. The existing universal
section-word certificate and published BCH/Lazard identification remain
the input-to-Lie-polynomial dependency; no complete Lean quantum receiver
or extracted compiler is claimed.

**Necessary premise.** In ut_5, both E14 of ambient weight3 and E24 of
weight2 centralize N. Replace E14 in a normal basis by E14+E24, leaving
E24 unchanged, while keeping the old weight labels. The normal bracket
tensor can still pass its weighted checks, but the ambient flag fails.
For X=q0*(E23+E34+E45), Y=q1*E12, Z=0, the section potential has the
degree-three coefficient E14/3. In the changed coordinates its E24
coordinate has degree3, exceeding its advertised weight2. This is an
actual source-word falsifier, not merely inconsistent dimension metadata.

## 4. Why The Cocycle Degree Becomes c

In the same right-fiber chart r(x)exp(i), the cocycle is

```
kappa(Q,x)=log(exp(-Q_A-X) exp(Q_A+Q_I) exp(X)), X=sum_a x_a e_a.
```

The public projections onto A and I preserve the ambient filtration.
Each term is a Lie word; a nonzero coefficient in output coordinate j
has input coordinate weight sum at most w_j<=c. Equivalently, for a
template monomial x^beta times a product of Q coordinates,

```
sum_a beta_a*w_a + sum_(Q factors i) w_i <= w_j <= c.
```

Replacing Q_i by a polynomial of degree<=w_i and assigning x_a weight
w_a gives total weighted degree<=c. Existing constraints remain useful:
parameter count<=k, at most one I parameter, and a pure-A term has fewer
than k parameters. These follow from the abelian-ideal cocycle, not from
the new ambient flag alone. Every formal cocycle coefficient is checked
against the output-coordinate weight by verify_cocycle_support.

No source label is rejected. Zero and nonzero Fourier labels follow the
same right-fiber contraction. Multiplication by observed labels and
addition across independent sources do not increase weighted degree.

## 5. Heterogeneous Full Taylor Jets And The Instrument

For each A coordinate a retain indices (alpha,l,a) with
1<=l<=w_a and |alpha|+l<=w_a. Give the corresponding jet coordinate
weight l. The jet width is

```
J = sum_a binom(m+w_a,m+1).
```

The feature matrix has row (s^l Y^alpha delta_(a,b)) indexed by a source
copy and its carrier component b. Complete these columns with standard
coordinate columns as in the existing GL alignment. Thus every original
carrier component x_a is a linear combination of retained jets of the
SAME component a, plus measured spectator constants. All its jet weights
are <=w_a. This establishes the substitution bound required in Section 4.
Arbitrary mixing of the retained jet coordinates would not suffice.

Let D=max_a w_a and ell=binom(m+D,m+1). Full rank of the scalar
degree-D feature design implies full rank of all component subdesigns;
at least one component has that maximal degree. Therefore the prior rank
argument applies with ell, NOT J/dim(A), which need not be an integer.
Use B=(ell+1)*bit_length(p)+2 independent rows. With p>2c>=2D, the
conditional rank-failure bound remains <=1/(4p).

The retained density kernel has exactly the old form

```
(|V| p^J)^-1 [q'-q in U] [t+F(q)=t'+F(q')]
                 omega^(P(q,t)-P(q',t')),
```

but now weight(P)<=c. The componentwise full-Taylor transport remains
invertible for nonzero scale, weight triangular with diagonal s^l, and
satisfies F(Y+s q)=F(Y)+A(Y,s)F(q). For each component the retained index
set is closed under the transport formula. Hence the existing nonlinear
support/channel proof applies with these direct-sum jets: branch masses
are (|V|p^J)^(-active count), and no unknown support is projected away.

Erase weights c,...,1 with public diagonal relations. Fourier-read ALL
retained jets with the existing negative sign. The residual eta.F(q)
is linear in A-potential coefficients, whose individual degree bounds
are w_a. Ordinary erasure therefore needs only degrees D,...,1.
The full classical record, independent children, zero-scale discards,
first-error argument and rejection costs are unchanged.

## 6. Invariant Support And Recomputed Schedule

For a formal parameter monomial let h be its number of factors and
W the sum of their coordinate weights. For a jet monomial let t be its
number of factors, V the sum of their COMPONENT weights w_a, and v the
sum of their actual Taylor weights l. The invariant overestimate is

```
1<=h<=k; at most one I parameter; pure-A h<k;
W+V<=c; t<=k-h; quotient degree q<=W;
actual phase weight = q+v.
```

Affine substitution in q cannot raise q. Taylor transport never changes
the component of a jet; constants can only remove factors. Thus W+V
and the factor constraints persist at every weighted merge. This is why
a filtration constraint on the initial template alone is not sufficient.

The generating-function DP counts parameter monomials by (h,W,I-count)
and jet monomials by (t,V,v), using multiplicities of equal-weight variables
and combinations with repetition. At weighted stage d it sums the
allowed pairs times binom(m+d-v-1,d-v), where 0<=d-v<=W. These are safe
equation counts, not claims that unknown coefficients are independent.
An independent direct enumeration agrees on a small complete support.

At ordinary stage d the bound is

```
Eo_d = binom(m+d-1,d) * sum_(a:w_a>=d) binom(m+w_a,m).
```

Use the existing fixed-degree SDE arity and actual products of stage
arities. Roots, rank retries, field sampling, instrument precision and
tree-node counts are recomputed with the new B,J and stage lists; no
formerly expensive source is silently reclassified as one free copy.
The sufficient total error remains <=3*epsilon/4 under the same physical
implementation contracts. The code checks the exact integer/rational
clock identities. Across arbitrary-H recursion, recompute the filtration
inside each current ambient quotient; do not reuse original weight labels.
The earlier additive recursion-call accounting is separate and unchanged.

The [published fixed-degree diagonal solver](https://arxiv.org/pdf/1503.09016)
remains the all-input dependency; reducing its largest degree from kc to
c is the main source of the improvement. No better SDE algorithm was
invented or implemented. The
[Lazard correspondence](https://arxiv.org/abs/1405.4654)
remains the group/Lie identification. Neither source is claimed to prove
this entire receiver or its novelty.

## 7. Evidence, Critique, And Next Decision

New tests cover actual class-nine matrix groups at p19, p43 and a 127-bit
prime; every cocycle-template coefficient agrees with the independent
Lie-word compiler. Actual section coefficients satisfy individual degree
bounds; the unadapted-central-coordinate counterexample fails. Unequal
jets satisfy transport and composition, the full compiled phase matches
an independent semidirect-product expression, and weighted merges retain
the filtered schema. Invalid carrier mixing and filtered supports fail.

A separate live coefficient diagnostic uses the actual class-nine chart,
m=2, a rank-complete 57-source transcript, zero spectators and only one
nonzero source label. It compiles 393009 nonzero formal terms, all of
weight<=9, over456 formal parameters and155 jet variables. This is a
coefficient stress test, not a probability estimate for that transcript,
an implemented source, or a receiver simulation.

Verification:561 connected Python tests passed in156.72s with RuntimeWarning
fatal. Final coefficient-count and feature-rank interface changes passed
46 and66 focused tests respectively. Full cached `lake build --wfail`
passed3467 jobs. Python syntax, formal generated crosscheck, qsearch
validation, site JavaScript/site checks and whitespace checks passed.
The live workflow was rerun. Full repository Python suite was not run;
all owned processes finished before handoff.

This refinement fails if projections do not respect the actual ambient
flag, if potential inputs are nonlinear beyond their proven bounds, if
alignment or transport mixes carrier components without weight control,
or if a controller treats only matching marginal kernels as independent
physical copies. The new compiler guards several of these interfaces;
it cannot certify hidden-instance provenance or physical freshness.

Code: theorems/ambient_filtered_induced.py, with narrow shared-compiler
changes in metabelian_induced_phase.py. The original uniform support path
is retained as an independent conservative comparator. Live resource
artifact: research/reductions/ambient_filtered_induced.json.

```
python -m theorems.ambient_filtered_induced --write
python -m pytest -q tests/test_ambient_filtered_induced.py -W error::RuntimeWarning
```

Do not call this practical, extend it to growing c/DCP, or infer a hard
application. Public-circuit and small-orbit-module classical filters remain
unchanged. The next substantive questions are independent whole-receiver
verification and whether the degree-dependent SDE tree can be replaced
by a different mechanism. Further bookkeeping reductions are lower
priority than that scientific question. General SDE execution, physical
synthesis and full controller implementation remain mechanical work.

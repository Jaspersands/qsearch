# Cubic Polarization Gives A Stronger Classical Flat Attack

Status: exact identities and native witnesses; proof review and novelty
assessment pending. This extends `CUBIC_RS_AFFINE_FLATS.md`, using the SAME
published input family and the SAME two saved native instances.

## Exact Extension Test

Write D_u f(x)=f(x+u)+f(x), with all arithmetic here over F_2. Let

    A = a + span(u_1,...,u_k)

be an already verified zero flat of a degree-at-most-three Boolean polynomial
f. Its third derivative

    T(u,v,w)=D_u D_v D_w f(0)

is a translation-independent alternating trilinear form. Lower-degree
coefficients disappear. To extend A by a new direction w, first impose

    T(u_i,u_j,w)=0, 1<=i<j<=k.

These are at most binom(k,2) HOMOGENEOUS LINEAR equations in w. Their kernel
K contains the existing direction space U. Let D=dim(K); in particular,
D>=n-binom(k,2).

For w in K, consider f(a+w+sum_i t_i u_i) as a polynomial in t. Its cubic
part equals that of f restricted to A, hence is zero. Its quadratic
coefficients differ from those on A by exactly T(u_i,u_j,w), hence are
zero too. The restriction is affine. It vanishes identically if and only if
it vanishes at t=0 and the k unit vectors:

    f(a+w)=0 and f(a+w+u_i)=0 for every i.

Thus one extension needs a linear solve and k+1 evaluations per proposal,
not a blind search satisfying all 2^k point constraints. Accepted w must
also lie outside U. A full final flat is independently replayed in tests
and the larger local controls.

The implementation contracts the stored cubic ANF tensor directly into a
binary row. A separate eight-term derivative checks this contraction,
including translated origins and individual monomials. Exhaustive small
kernel tests check BOTH directions of the extension equivalence.

This uses standard finite-difference and Boolean polynomial identities.
No novelty claim is made for the algorithmic idea.

Follow-up prior-art check: the structural method is covered by
[Cohen and Tal, Sections 4 and B](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2015.680).
`CUBIC_DEGREE_REDUCTION.md` implements the polynomial-time degree-reduction
route and distinguishes its guaranteed, smaller flats from this
rejection-based constructor. Neither local primitive is a project discovery.

## A Conservative Success Bound

The following derivation removes the need to assume a convenient random
density for the remaining conditions. It is still review pending.

Choose coordinates on K. The extension conditions can be expressed as one
cubic c(w)=f(a+w) and k quadratics q_i(w)=D_(u_i) f(a+w). Their common-zero
indicator is the Boolean polynomial

    G(w) = (1+c(w)) product_i (1+q_i(w)).

It has degree at most d=2k+3 and is nonzero, since G(0)=1. A nonzero
degree-at-most-d Boolean polynomial on D variables has weight at least
2^(D-d). For completeness: split G=g+x_D h. If h=0, induction on g
applies to both slices. Otherwise the sum of the two slice weights is at
least the weight of h, whose degree is at most d-1. This proves the bound
by induction (the bound is merely fractional/vacuous if d>D).

At most 2^k of these solutions lie in U. A uniform draw from K therefore
extends the flat with probability at least

    p_k = max(0, 2^(-2k-3) - 2^(k-D))
        >= max(0, 2^(-2k-3) - 2^(k-n+binom(k,2))).

This bound holds for EVERY accepted partial flat, not just a fresh
unconditioned random cubic. It does not assume independent quadratic
equations or uniform restriction coefficients after adaptive search.

For the initial accepted point, every f other than the constant-one
function has acceptance density at least 1/8, by the same minimum-weight
argument applied to 1+f. The constant-one input has probability 2^-S(n)
in the uniform ANF ensemble, S(n)=sum_(j=0)^3 binom(n,j).

With T draws per stage, failure is at most (1-p)^T<=exp(-Tp). The report
uses only rational arithmetic and the conservative bound

    exp(-Tp) <= 2^(-floor(10Tp/7)).

Indeed ln(2)<7/10; already the degree-four Taylor lower bound for exp(7/10)
exceeds two. No floating-point tail extrapolation is used.

Union-bound the constant-one inputs, all m local capped searches, and the
conditional global MDS rank failure from `CUBIC_RS_AFFINE_FLATS.md`.
Uniform sampling in K makes the transition LAW affine-equivariant even
though an echelon kernel basis itself is basis-dependent. Therefore the
conditional uniform-flat rank argument still applies.

For T=4096 and the predeclared cases:

| n | m | r | target k | certified ensemble success lower bound |
|---|---|---|---|---|
| 16 | 256 | 30 | 3 | 999/1000 |
| 32 | 1024 | 120 | 4 | 499/1000 |

Bounds are rounded DOWN to thousandths with exact rational arithmetic.
They include failed searches, constant-one input blocks, and global
inconsistency. They concern ideal independent input/randomness, NOT the
recorded PRNG seed. They do not certify practical quantum success or give
a polynomial-time asymptotic classical algorithm.

At n=64, k=8 and the same cap, this conservative global lower bound is ZERO.
Successful local runs must not override that fact.

## Live Evidence

Both original complete instances produce valid classical witnesses again.
All original cubic ANFs and field syndromes replay independently.

| n | naive search evaluations | polarized search evaluations | polar contractions | local linear solves |
|---|---|---|---|---|
| 16 | 9941 | 6271 | 256 | 768 |
| 32 | 304774 | 56995 | 3072 | 4096 |

These counts do not hide the new linear-algebra work. On the initial
polarized run, complete native execution took approximately 0.27 and
13.75 seconds respectively; timing is machine/load dependent. No matched
quantum wall-time comparison was performed.

A separate PREDECLARED local check generated 16 independent cubic ANFs on
64 bits, seeking zero flats of dimension eight. All 16 succeeded. Every
one of the resulting 256 points per flat was independently evaluated from
the original ANF. There were 16981 search evaluations and 336 polar
contractions. At the last extension, all 16 polar systems had rank 21 and
kernel dimension 43.

This is NOT a full n=64 instance: such an instance has 4096 blocks and
30720 binary code constraints. Those global constraints were not solved
in this local control. No incomplete output is counted as a native witness.

## Self-Critique And Falsifiers

- Greedy search really can get stuck. Small regression controls retain
  budget failures and a cubic with no extension of the selected flat.
  None of these failures establishes original-system unsatisfiability.
- The minimum-weight bound is conservative; it may become vacuous well
  before local search becomes impractical. Improving a bound alone is not
  an algorithmic breakthrough.
- The zero-flat counting obstruction from the preceding note still applies.
  Cubic polarization reduces search cost; it cannot create large zero flats
  when almost none exist.
- A sparse/easy cubic ensemble would silently change the task. The producer
  retains full independent dense ANF coefficients, including lower degrees.
- Classical success does not simulate the entire quantum output distribution.
  It solves the native search relation, which is the relevant comparator here.
- Neither this result nor the paper supplies a reduction from a broadly
  useful hard problem or a cryptosystem attack. Do not import general MQ
  hardness, ECDSA relevance, or oracle lower bounds.

Next high-reasoning work: independent review of the combined probability
argument and a substantive route beyond one flat per block, or a reduction
giving the quantum relation broader significance. Do not consume the main
model on endless successful seed sweeps.

## Reproduction

    python theorems/cubic_rs_affine_flats.py
    python theorems/cubic_flat_polarization.py
    python -m pytest -q tests/test_cubic_rs_affine_flats.py tests/test_cubic_flat_polarization.py

The second producer records the hash of the first report. Regenerating the
first report changes diagnostic timestamps/timings and requires regenerating
the second; do not delete this dependency check. No producer or dependency
may be edited while either command is running.

Mechanical follow-up is specified in `MECHANICAL_FOLLOW_UP_PLAN.md`.
No qsearch/UI changes, central admission, commits, or pushes were made.

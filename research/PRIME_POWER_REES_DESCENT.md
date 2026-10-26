# Direct Prime-Power Rees Descent

2026-10-23. Proposed constructive extension, review pending. Not a new
scalar-equation solver, independent validation of the Rees composition,
quantum receiver execution, novelty certificate, or useful hard application.

## Decision And Scope

The existing outer reduction ALREADY proposes polynomial-time HSP at every
fixed nilpotency class, without bounding the exponent. This note does not
expand that unrestricted-rank fixed-class claim. Its distinct question is:
can explicit prime-power Lie input be handled DIRECTLY, with parameter cost
in class and derived additive generator rank, rather than repeated hidden
subgroup restriction or an exponent-p replacement?

The answer below is a proposed algorithm using the actual central-label
distribution, a known scalar field solver and ordinary Hensel lifting.
It does NOT solve arbitrary diagonal equations over a torsion ring.
In particular, some legal label tuples have no admissible unit-scale solution.
They are rejected, with every consumed source and failed batch charged.

**Input.** A finite nilpotent Lie ring L whose additive group is explicitly
direct_sum_i Z/p^a_i, a supplied verified odd prime p, genuine compatible
bracket constants, actual class c<p, and an ordinary coherent HSP oracle
on exp(L), or the separately justified mixed coset-copy source. Orders are
encoded with their full binary bit lengths; a_i log p bits of coordinates
are paid. Let n be the additive generator count and r the minimum additive
generator count of [L,L]. No opaque-to-Lie chart acquisition is free.

**Proposed bound, conditional on the Rees lemmas:**

    [4(c+1)]^((c-1)r) * poly(explicit input bits, log(1/epsilon)).

The polynomial exponent is independent of c,r and the additive exponents.
This is fixed-parameter time in (c,r), NOT in r alone. It is an alternative
to the prior algorithm, not a uniform improvement over it. For large r at
fixed c, the earlier field-vector solver plus outer reduction is preferable.

## 1. Homogenization Over The Actual Module

Let p^E annihilate L, R=Z/p^E, and form the genuine positive Rees Lie ring

    A = direct_sum_(d=1..c) t^d gamma_d(L) subset L[t].

The components are finite R-modules, not assumed free. Additive subgroup
coordinates, intersections, images and quotients are computed using complete
integer relation lattices and Smith/Hermite normal forms. Replacing them
by vector spaces modulo p can erase real hidden elements.

The Lazard correspondence for finite p-groups and Lie rings of class<p
is standard; see [Cicalo--de Graaf--Vaughan-Lee](https://doi.org/10.1016/j.jalgebra.2011.11.031).
The inspected primary statement [Garaialde Ocana--Gonzalez-Sanchez,
Theorem1(c)](https://arxiv.org/html/1405.4654) explicitly preserves
subgroup/Lie-subring correspondence. No complexity from the unavailable
full Cicalo paper is imported. The BCH rational
identities only divide by integers prime to p. The uniform differential
recurrence in DERIVED_RANK_REES_EXTENSION.md is an identity over
Z[1/c!], hence also works on these modules with unit inversions. This is
a mathematical arithmetic argument; the existing bch_via_ode API explicitly
requires a PRIME field and must not be called with p^E as its prime.

Evaluation E_s is a Lie and BCH homomorphism. Choose s=1,...,c. The
Vandermonde determinant is a unit modulo p, hence modulo p^E. Its inverse
uses only integer/unit scalar operations, which preserve any additive
hidden Lie subring h. The same proof therefore gives

    h_tilde = direct_sum_d t^d (h intersect gamma_d(L)).

Each lifted source costs c original queries or copies. For every UNIT s,
Delta_s scales grade d by s^d and preserves h_tilde. A nonzero nonunit s
does not generally define an automorphism and is never an active scale.

## 2. A Cyclic Central Factor Has An Exact Label Law

Once all higher grades are removed, choose a cyclic direct summand
Z=<z> of the highest remaining grade, of order p^a. It is central and
preserved by unit dilation. Quotient it out, then continue through the
other cyclic factors. The unknown hidden image need not contain or avoid Z.

The old central-projector calculation works for every finite abelian Z,
not only elementary ones. If K=H intersect Z has order p^b, the positive
character labels are exactly

    lambda = p^b u mod p^a,   u uniform in Z/p^(a-b).

Each has probability p^b/p^a. Conditional right-action correlations are
chi_lambda(z0) on g=h*z0 in HZ and zero otherwise, with the same |G||K|
normalization as before. These are independent labels only for independent
ideal input sources (or the specified successful bank refresh).

Let d be the dilation degree, delta=gcd(d,p-1), and B=delta+1<=d+1<=p.
Consume B fresh sources and measure all B labels. Use this complete policy:

1. If some lambda_i=0, choose its scale1 and all other scales0.
2. If all labels are nonzero and have the same p-adic valuation v, apply
   the lifting construction below.
3. Otherwise discard the WHOLE measured batch and restart. Do not reuse it
   as fresh input, condition away the loss, or assert it had no other witness.

If b<a, each label has valuation b with probability 1-1/p. Thus an accepted
batch occurs with probability at least (1-1/p)^B>=1/4, uniformly in a,b.
If b=a every label is zero and acceptance is certain. No knowledge of b is
needed. The more precise acceptance probability, with m=a-b>0, is

    1-(1-p^(-m))^B + [(p-1)^B/(p^B-1)]*(1-p^(-mB)).

This counts disjoint zero-containing batches and all-equal nonzero valuation
batches. It is a theorem about the source law, not arbitrary label lists.

## 3. Lift A Regular Scalar Witness, Not A Field Routine By Substitution

In an equal-valuation batch put A_i=lambda_i/p^v, units modulo p^(a-v).
This is integer division of measured labels, not division of a group
element or quantum source by the nonunit p.
The published scalar theorem gives a nonzero solution x over F_p of

    sum_i (A_i mod p) x_i^delta = 0

using B=delta+1 labels, in time polynomial in delta and log p. This is
[Ivanyos--Santha Fact2](https://arxiv.org/html/1503.09016), quoting van de
Woestijne; delta=1 is just a linear equation. Convert it to degree d by
the earlier modular exponent lift, keeping zeros exactly zero.

Choose a coordinate j with s_j!=0 modulo p. The derivative

    d*A_j*s_j^(d-1)

is a unit modulo p because d<p. Keep every other s_i fixed and Hensel-lift
this one coordinate through modulus p^(a-v). At precision p^k, let
F(s)=sum A_i s_i^d; it is divisible by p^k. The correction is

    s_j <- s_j + p^k*t,
    t = -(F(s)/p^k) / (d*A_j*s_j^(d-1)) mod p.

Taylor terms of order>=2 vanish modulo p^(k+1), for k>=1. Every correction
preserves s_j modulo p, so it stays a unit. Other active scales remain
units and all inactive entries remain zero. At termination,

    sum lambda_i s_i^d = 0 mod p^a,

with at least one active unit. Work is polynomial in a,d,log p, not p^a.
The implementation verifies the finite-field witness and final congruence.

For each active unit, Delta_s preserves HZ and its complement. Therefore
the previous controlled-right-action contraction gives the EXACT quotient
coset state, for every accepted label tuple and every valid lifted witness.
The output density is independent of its label/retry records. Rejected
batches emit no quotient sample. This proves both a legal restart and the
fresh-source induction; marginal label statistics alone are insufficient.

## 4. Account For The Entire Random Tree

Let r_d be the number of cyclic factors of gamma_d(L) and
T=sum_(d=2..c) r_d. A subgroup of a finite abelian p-group with r additive
generators has at most r such generators. Hence T<=(c-1)r. This inequality
follows directly from B[p] subset A[p] for additive subgroups B subset A
and d(B)=dim_Fp B[p]. It uses neither vector-space subtraction of ranks
nor freeness. It
does NOT imply c<=r+1: over Z/5^4 the Lie ring [x,y]=5y has r=1 and class4.

For one terminal additive-L sample, the expected lifted-leaf count is at most

    Q = product_(d=2..c) [4*(gcd(d,p-1)+1)]^r_d
      <= [4(c+1)]^((c-1)r).

This follows inductively: each attempted cyclic conversion consumes B
fresh predecessor outputs, and its number of attempts is dominated by a
geometric variable with mean4. Disjoint preparation and all-record output
independence justify repeating the same predecessor process. This is not
the successful-tree count; failed subtrees are included.

Take M=n+3 terminal samples for one base run. The finite abelian annihilator
needs at most n generators. Its uniform samples generate it iff their images
generate its quotient by p, so ideal rank failure is <p^-3/(p-1)<1/16.
Let L0=M*Q. A GLOBAL cap of16*L0 lifted leaves has ideal abort probability
at most1/16 by Markov. Check the cap before starting a new c-input lift.
The original query/copy cap is16*c*L0. Do not put a constant retry cap at
each node and ignore the accumulated probability of many local aborts.

Under the global cap, successful and failed conversion trees form a forest:
each target has only one parent and every conversion consumes at least two
targets. Thus the number of conversion attempts is at most the number of
leaves. Including leaf instruments and M final readouts, a safe instrument
count is32*L0+M. Include all branches, discarded targets and ABORT records.
Per-instrument half-diamond error 1/[16*(32*L0+M)] adds at most1/16 error.
Precision overhead is logarithmic in this count. Source-bank error is a
separate JOINT trace-distance budget, never a per-marginal assertion.

One base run therefore succeeds with probability at least13/16 under the
ideal input contract. Recover h as an additive submodule and encode it by
the canonical Hermite normal form of its full preimage lattice in Z^n.
Repeat independent complete runs an odd O(log(1/epsilon)) number of times
and take the modal CANONICAL output, counting abort as its own token.
Hoeffding bounds failure by exp(-25*R/128). Voting on arbitrary Smith bases
would be invalid. Charge any approximate JOINT input-bank error additively
to the final epsilon, rather than assuming repetition removes correlations.

Arithmetic per capped forest node is polynomial in the explicit input,
c and log p, including mixed-order module sections, BCH and the scalar
solver. This proves the stated joint parameter bound, subject to the
whole-composition review. There is no native receiver or general ring
coordinate compiler execution behind this symbolic clock.

## 5. Adversarial Checks And What Remains Unproved

- **Nonunits can fake success.** In Z/9 x Z/9, with degrees1,2 and hidden
  subgroup 3Z/9 x{0}, the phase witness(lambda,s)=(1,3) cancels modulo9,
  but the induced quotient output is the whole-group pure state. Its trace
  distance from the intended coset state is2/3. Unit checks are essential.
- **Some batches have no legal witness.** Labels(1,3,9) modulo27 at degree2
  have distinct valuations. Any nonempty choice of units/zeros has a unique
  lowest-valuation term, so its sum is nonzero. A nonzero nonunit solution
  is irrelevant. Replaying this fixed bank never succeeds.
- **Mod-p reduction alone loses the phase.** Labels(3,6,3) modulo9 all
  reduce to zero; picking the first source leaves phase3, not phase0.
  Divide by their actual common valuation before finding the field witness.
- **The cover is not a free module.** The exact control [x,y]=3z overZ/9
  has grade-two order3. Its nonnormal h=<x+z,3y> survives the two-evaluation
  reduction. Using evaluation points1,4 instead of1,2 gives a false collision:
  different ring elements need not have different residues modulo p.
- **Novelty and advantage remain open.** The previous outer reduction already
  covered general exponent at fixed class. Hensel lifting, cyclic Fourier
  measurement and scalar equation solving are old ingredients. This is a
  direct composition with a different parameter bound, not an automatic
  new quantum speedup or evidence that an explicit application is hard.

The native fixed-numerator attack examined earlier in this pass is still
unresolved. Patterson-style decoding uses a known syndrome and a special
locator/derivative identity; those are not supplied by the native congruence.
No reconstruction algorithm or negative-result claim was produced by that
analogy. Do not replace that missing algorithm with this unrelated extension.

## 6. Verification And Handoff

NEW theorems/prime_power_rees_descent.py implements batch planning, verified
Hensel lifting, exact ideal batch probabilities and a conservative clock.
It does NOT find scalar field witnesses or execute the quantum receiver.
NEW tests/test_prime_power_rees_descent.py has27 tests; combined with the
previous scalar-line and source-bank controls,75 pass(0.59s). Python syntax
and targeted whitespace checks pass. The manuscript compiled successfully
on retry after one stale-project result; compilation is not formal proof.
Exhaustive tiny-ring controls check every batch and every central
intersection for three parameter sets. Large-modulus controls use a127-bit
prime raised to exponent32, without enumeration. Full density contractions
include a nonlinear section, zero labels and full/nontrivial/trivial K.

The first run's only failure was passing Fraction(2,3) to NumPy's floating
comparison; the computed distance was2/3. The comparison now uses a float.
The full old receiver integration is not validated while its dependencies
remain cloud-offloaded. No file was hydrated or moved; no Git write,
qsearch/UI/central-registry admission, agent or outreach action occurred.

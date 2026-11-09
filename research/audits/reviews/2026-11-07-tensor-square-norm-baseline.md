# Tensor-square rational norm equations: classical and output audit

2026-11-07. ACCEPT the compact norm-coordinate and witness-verification
interface below, conditional on the separately reviewed tensor-square
support-moving theorem and the complete compact S-unit primitive. This
review does not establish novelty, a classical lower bound, execution or
the support theorem itself. No Git/network/API action or finite sweep.
Interpreter: `/opt/anaconda3/bin/python`.

STATE/TRAPS and focused corpus been-tried/baselines were checked first.
Actual Biasse--Song2510.02280v2 Section8.6 and its references were read in
`/tmp/qsearch-sunit-v2.txt`; the durable source is
`research/literature_cache/arxiv_2510_02280v2.pdf`.

## Native problem and strongest applicable comparison

The problem is to decide, for explicit L/Q of growing degree n and
nonzero rational a, whether N_(L/Q)(x)=a has x in L*, and to return such
an x in COMPACT representation when it exists. It is not an integral
norm-equation algorithm, a short-element algorithm or a list of solutions.
Support-moving corrections can introduce denominators at S. Expanded
coordinates of the resulting x need not have polynomial size.

Actual BS Section8.6 supplies polynomial quantum norm-equation computation
directly for arbitrary-degree GALOIS extensions. It says its cited general
Simon reduction goes through the Galois closure, whose degree can be
exponential. This is a precise source boundary, not proof of novelty for
the proposed tensor replacement. Priority comparison must include Denis
Simon, "Solving norm equations in relative number fields using S-units",
Math. Comp.71(239),1287--1305(2002), and Fieker--Jurk--Pohst, "On solving
relative norm equations in algebraic number fields", Math. Comp.66(217),
399--410(1997). The source's omission does not exclude another published
support theorem.

The proposed support theorem is itself a CLASSICAL reduction: once the
explicit rational support has been chosen and a complete compact S-unit
basis in L is supplied, norm-image membership and witness construction
are polynomial classical integer/rational arithmetic. No new quantum
primitive occurs in the final image computation. The quantum composition
uses existing S-unit computation and initially charged factorization.
The retained classical baseline is complete S-unit/class-unit computation,
including index-calculus methods under their actual hypotheses. This audit
found no polynomial classical algorithm for that missing native arithmetic
and proves no lower bound against one.

The proposed support cutoff uses the parent's source-checked constant48
with the tensor discriminant bound, not an unverified replacement by12.
Factoring a and the selected field/order discriminant remains charged for
support and maximal-order preprocessing. No factorization of compact-leaf
norms is required in either the image computation or the final verifier.

## Exact rational norm coordinates without integer factorization

Suppose the complete free S-unit generators are compact products

    beta_i = product_j alpha_j^(e_ji),

with polynomially many explicitly represented nonzero leaves alpha_j,
polynomial-bit signed binary exponents, and polynomial total representation
size. Shared leaves can be reused. Each rational leaf norm

    r_j=N_(L/Q)(alpha_j)

is the determinant of its n-by-n multiplication matrix. Its numerator and
denominator have polynomial bit length in the explicit field and leaf
data, and are computed by exact rational linear algebra. This never
expands beta_i or a large exponent.

Form a gcd-free basis of the absolute numerators and denominators of EVERY
r_j and of a. This is a family b_1,...,b_t of pairwise-coprime integers>1,
together with exact exponent representations of all the inputs. The b_l
need not be prime or power-free.

A direct polynomial algorithm suffices. Initially list all input integers>1
as factors with their representation columns. If two factors u,v have
g=gcd(u,v)>1, replace them by the nontrivial factors g,u/g,v/g and update
each representation column using u^e v^f=g^(e+f)(u/g)^e(v/g)^f. Merge
equal factors. Each step decreases the sum of logarithms of the listed
factor values by at least log2; there are polynomially many such steps.
Representation exponents for any original positive integer never exceed
its binary length, since every factor is>1. All arithmetic and repeated
gcd comparisons therefore have polynomial bit cost.

The resulting coordinates are

    r_j = (-1)^(s_j) product_l b_l^(c_lj),
    a   = (-1)^(s_a) product_l b_l^(t_l),

with signed exponents for denominators. Pairwise coprimeness implies that
product_l b_l^(z_l)=1 with integer z_l holds exactly when every z_l=0.
Hence these are exact multiplicative coordinates on the subgroup needed
by this computation. They do not approximate valuations or assume away
prime factors outside S.

For beta_i, compute A_li=sum_j c_lj e_ji and
sigma_i=sum_j s_j e_ji mod2. Their binary sizes remain polynomial even
if the represented rational norms are enormous.

## Torsion, integer solution and compact witness

A complete FREE S-unit basis modulo roots of unity plus the element -1
suffices for ABSOLUTE rational norm images. Every root of unity other than
1,-1 has rational norm+1: its cyclotomic minimal polynomial has constant
term1 and even degree. The remaining value is N(-1)=(-1)^n. Thus no large
root-of-unity enumeration is needed; adjoining -1 handles the only possible
missing norm sign. This does not replace full torsion handling for other
relative-norm targets.

Add its norm column and solve the integer system

    A z = t,
    sigma*z - 2h = s_a,

where h is one additional integer variable. HNF/SNF with transformations
decides exact membership and produces polynomial-bit integer exponents
when the system is solvable. Completeness of the S-unit basis, together
with the support-moving theorem, is what makes an unsolvable system a
valid NO answer on the arithmetic primitive's success event.

Return x=product_i beta_i^(z_i), retaining the compact representation.
Flattening its exponent products still uses polynomial bits and polynomially
many leaves. No expanded unit, fundamental-unit height bound, bounded
coefficient generator or exponential-size rational norm is requested.

Verify the returned witness classically by recomputing its leaf norms and
gcd-free product-of-powers coordinates, including its sign, and comparing
with a. The verifier works independently of an assertion that x is an
S-unit: outside-S factors are present in the gcd-free basis and must cancel.
Checking only selected S-valuations of an unverified compact output would
not provide this guarantee. A malformed zero leaf or inconsistent exact
representation is rejected. A valid witness is not a certificate of
nonexistence; NO still depends on the complete-basis success guarantee.

## Disposition

No cheap classical collapse, hidden norm oracle or output-size flaw was
found in this interface. The support-moving proof is the substantive new
gate to audit against the literature; the remaining compact norm-image
algorithm is classical and fully paid. Keep GRH, explicit field/order
preprocessing, the complete S-unit success event and COMPACT rational-field
output in the final contract. Do not promote it to integral solutions,
short solutions, novelty or a proved quantum/classical separation.

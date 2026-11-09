# Cubic Gauss phase: elliptic product admission

2026-11-06. Independently actual-text reviewed source admission and elementary
identities; no new
quantum algorithm, classical polynomial-time algorithm, hardness result or
novelty claim. A CM full-kernel product does not by itself complete the
proposed classical computation. Ito already evaluates the canonical elliptic
factor; the remaining factor is a finite-field product of representatives.

## Native task and proposed mechanism

Input: a primary Eisenstein prime pi=a+b*rho, rho=exp(2pi*i/3), with
pi congruent to1 modulo3 and prime norm p>3. This specifies the embedding
rho -> r=-a/b in F_p and the cubic character chi(x)=rho^e when
x^((p-1)/3)=r^e; chi(0)=0. The additive character is the FIXED standard
exp(2pi*i*x/p). Output the complex phase of

    tau(pi)=sum_x chi(x) exp(2pi*i*x/p),

to constant angular accuracy, or its exact branch among the three roots
of tau^3=-p*pi. Input size is O(logp); pi is explicit, not hidden advice.
Changing the additive character is a different input, not a free branch
choice. Exact algebraic output must include the intended complex embedding.

The tested classical mechanism was fast CM endomorphism/division-polynomial
evaluation of Matthews's elliptic product. If this paid the entire formula
in poly(logp) bit time, it would match the known constant-accuracy quantum
algorithm for this fixed-order case. This is a test of an existing native
Gauss-sum task, not a newly invented cryptographic application.

Resources to charge: construction of representatives, their modular product,
every elliptic operation and its precision, and selection of the complex
branch. A short evaluation circuit for a multiplication map does not give
its exponentially long coefficient list or a selected-root product for free.

## Prior work and actual sources

The corpus been-tried lookup for `cubic Gauss sums Matthews elliptic product
formula division polynomial phase sign` finds nearby Gauss/Legendre work,
but no paid implementation of this product. The matching baselines lookup
has no catalog match; this is not evidence of classical hardness.

Primary texts read:

- [Ito, Acta Arithmetica152 (2012)](https://www.impan.pl/shop/en/publication/transaction/download/product/83640),
  equations1.2/2.1, Theorems1/2 and Section4. This primary paper states and
  uses Matthews's formula; Matthews's original proof was not independently
  audited. Local `audits/sources/ito_cubic_gauss_product_2012.pdf` and `.txt`.
- [van Dam--Seroussi](https://sites.cs.ucsb.edu/~vandam/gausssumdlog.pdf),
  Algorithm3, Theorem1 and Lemma2/Section6.1. Local
  `audits/sources/van_dam_seroussi_gauss_2002.pdf` and `.txt`.
- [Tal, ECCC TR26-211](https://eccc.weizmann.ac.il/report/2026/211/),
  the already audited exact-Jacobi result and the refreshed Theorem1.1
  modular-factorial cost. Local `audits/sources/jacobi_classical_eccc_2026_211.*`.
  See `JACOBI_GROUP_RING_RECOVERY.md` for the preceding full source review.

The established quantum algorithm estimates Gauss phase in
O(epsilon^-1 poly(logp)) time. For fixed cubic order the character can also
be evaluated by ordinary modular powering and comparison with1,r,r²;
general discrete logarithms are unnecessary for that evaluation. The known
algorithm is the comparator, not a new result of this pass.

The classical comparators include direct O(p) summation, exact Jacobi
reconstruction and the elliptic product formula itself. Tal computes exact
Jacobi sums in poly(q,logp), but its arbitrary factorial Theorem1.1 costs
soft-O(q^c+sqrt(p/q)) for q dividing p-1. Neither statement is a uniform
poly(logp) algorithm for the polygon product below. Failure to obtain a
reduction is not a lower bound on that product or on fixed-order Gauss sums.

## What the formula actually requires

Let S contain one representative from each orbit of multiplication by rho
on (Z[rho]/pi)^*. Thus |S|=(p-1)/3. Let alpha(S) be the unique cube root
of -1 whose residue modulo pi is product_(s in S) s. Wilson's theorem
makes this definition valid. With the period and Weierstrass function
normalized exactly as in Ito, put P_S=product_(s in S) wp(s*theta/pi).
Matthews's formula as stated there is

    tau = p^(1/3) pi alpha(S)^(-1) P_S.                 (1)

Ito constructs a particular geometric S_pi and proves

    pi P_(S_pi) = zeta_pi principal_cuberoot(pi),        (2)

where zeta_pi is a cube root of unity determined by pi modulo9 and the
angular sector floor(6 arg(pi)/pi_math). Section4 gives its explicit
integer formula. Thus the canonical elliptic product and its branch are
ALREADY explicit. The remaining factor in (1) is alpha(S_pi), not P_S.

For completeness, write pi=(-rho)^n pi0, pi0=c-d*rho^sigma,
|arg(pi0)|<pi_math/6, 0<d<c, sigma in{+1,-1}, and
m=3(arg(pi)-arg(pi0))/pi_math, an integer with the actual principal angles.
Set sgn=sign(arg(pi0)), k=floor((c-1)/3), and

    q=floor(d/3)         if c+2d=1 mod3,
    q=floor((d+1)/3)     if c+2d=-1 mod3,
    l=1 or2             if c=0 mod3 and sgn=+1 or-1,
    l=0                 otherwise.

Then Section4 gives zeta_pi=exp(2pi*i*A/9), with

    A=p*m+(p-1)+sgn*c*d-3(q+k)-2*l.

Here A is divisible by3. Exact sector selection uses comparisons of
quadratic real numbers; these computations use poly(logp) bit work.
Reducing n modulo6 without tracking the principal-angle wrap would be an
incorrect branch shortcut. The formula is source-derived, not executed
as a new large-prime pipeline in this pass.

Combining (1) and (2) gives

    tau = p^(1/3) alpha(S_pi)^(-1) zeta_pi principal_cuberoot(pi).

Consequently exact alpha(S_pi) and the constant-accuracy Gauss branch are
mutually reducible with polynomial additional bit work. For the reverse
direction the three normalized candidates have angular separation2pi/3;
error less than pi/3 selects the unique branch (use a smaller fixed margin
for numerical approximation). Repeating the known bounded-error quantum
phase procedure pays any requested failure probability. This combination
is not claimed novel and does not supply a new classical product algorithm.

## Cheap exact falsifiers and scope

Replace one representative s by rho*s. Then

    alpha(S')=rho*alpha(S),   P_(S')=rho*P_S,

since wp(rho*z)=rho^(-2)wp(z)=rho*wp(z). Their ratio in(1) is invariant.
The complete nonzero-kernel product is

    product_(t !=0 modpi) wp(t*theta/pi)=P_S^3=pi^(-2).

The first equality follows orbit by orbit; the second follows by cubing
(1), using tau^3=-p*pi and alpha^3=-1. A full-kernel determinant or norm
that returns only this product has erased the required cube-root choice.
Even a correct evaluation of Ito's P_S leaves alpha to be computed.
This rejects that claimed completion step, not arbitrary CM algorithms.

Likewise, the general discrete-log reduction in van Dam--Seroussi Lemma2
uses a character of order p-1 (or p^r-1), not order3. For a cubic character,

    tau_beta/tau_1=chi(beta)^(-1)

depends only on beta's cubic class, which is classically computable by
modular powering. The cited reduction therefore supplies no fixed-order
classical-hardness conclusion. This does not classically determine tau_1.

Knowing pi or tau³ does mathematically specify the original native task;
we are not claiming information-theoretic ambiguity of its full input.
The three-root ambiguity is a missing computational step in the proposed
operation. Arbitrary additive-character controls must not be mistaken for
three different answers to the SAME fixed standard-character input.

## Decision and next decisive test

No quantum subsystem, CM circuit, division-polynomial coefficient expansion,
larger-prime sweep or new registry barrier is admitted. Only an explicit
paid algorithm for alpha(S_pi), or a reduction to an already fast classical
operation with exact input/size bounds, would reopen this proposal. Row-wise
factorial rewriting without bounding the number and sizes of rows does not
meet that gate. An independent comparison finds only O(sqrt(p)) geometric
rows, each with O(1) intervals; after rho->r each interval is a factorial
ratio modulo p. This is not a polylogarithmic number of calls, and Tal is
not a polylogarithmic arbitrary-factorial subroutine. No cancellation was
established. The polynomial-in-degree native character reconstruction
question remains the higher-priority unresolved algorithmic target.

The finite control `classical_baselines/cubic_gauss_branch_control.py/.json`
completed in Sage exact CyclotomicField(3p) arithmetic; the parent inspected
its actual code and saved output. For p=7,13,19,31 it verifies tau_1³=-p*pi,
the three additive twists' exact ratios1,rho²,rho and their equal cubes,
and alpha's exact rotation under a representative change. The diagnostic
principal-root branch indices are0,2,2,0, computed at160-bit precision,
with absolute residual below3.4e-47. Algebraic identities are exact;
this branch comparison alone is numerical. Products modulo p change
3->5,4->10,8->12,30->6, respectively. These representatives are arbitrary
least-integer orbit representatives, NOT Ito's geometric system. Direct
summation enumerates3(p-1) terms per prime, and the cyclotomic field degree
is2(p-1). This is no efficient large-p implementation. No elliptic or
quantum execution; no asymptotic inference from these finite cases.

Independent actual-text review accepted the formula A, principal-angle
wrap, branch equivalence and computational scope. A separate independent
comparison checked the factorial cost. The source-based result and exact
controls do not establish hardness, novelty or a new speedup.

# Structured EDCP: Module Decomposition Does Not Remove Integral Gluing

Date: 2026-09-27. LOCAL DERIVATION / REVIEW PENDING.

## 1. Decision

Quantum principal-ideal algorithms do not currently supply our missing
few-block Gaussian decoder. The native one-block ideal already has the known
generator q-X. Orthogonalizing the module over its number field leaves a
finite-index integral coupling between the lines. Solving the separate ideal
problems does not solve that coupling.

FOLLOW-UP: section 8 constructs an exact principal-ideal encoding of the
WHOLE module in a larger field, rather than dismissing that alternative.
Its generator is already known and nearly canonical-shortest. The label-
dependent Gaussian metric remains the problem; replacing that metric erases
the multi-block information gain. This is not a blanket rejection of quantum
unit-group methods for a genuinely new metric-aware operation.

This pass has two concrete outputs:

- An exact balanced counterfamily to the orthogonal direct-sum inference in
  equation (70), and hence the stated diagonal-only bound in Theorem 5.8, of
  [Luo, arXiv:2604.22900v2](https://arxiv.org/html/2604.22900v2#S5.E70).
- A source-weighted fidelity bound for constructors supported on too few
  cosets of the native diagonal submodule. The bound allows the selected
  cosets to depend on the requested frequency and does not assume random
  labels. It is NOT a quantum gate lower bound.

Do not turn either result into a claim about all module algorithms, all of
that paper's statements, or deployed cryptographic security. Independent
review is still needed. No author contact, publication or novelty claim.

## 2. An Exactly Balanced Counterfamily

Use our notation: ring degree d, module rank L, R=Z[X]/(X^d+1), with d a
power of two. Fix an integer p>=3 and the free R-module with basis

    b_1=p*e_1,
    b_j=-e_1+e_j,  2<=j<=L.

Equivalently,

    M={c in R^L : sum_j c_j is in p*R}.

Its coefficient lattice has determinant p^d. K-Hermitian Gram-Schmidt gives
p*e_1,e_2,...,e_L. Every vector has identical lengths at all embeddings, so
the Galois balance constant in the paper's Definition 5.1 is EXACTLY C=1.
This is not an assumption that the different module lines have equal lengths.

Nevertheless the intersections with those K-lines are

    M_j=M intersect K*e_j=p*R*e_j,
    D=direct_sum_j M_j=(p*R)^L,
    det_coeff(D)=p^(d*L),
    [M:D]=p^(d*(L-1)).                                      (1)

Orthogonality holds, but D is a proper submodule of M. For example
(-1,1,0,...) belongs to M, has coefficient norm sqrt(2), and is not in D.
Any nonzero vector on one of the M_j has coefficient norm at least p.

In the full-embedding convention, canonical norms multiply coefficient
norms by sqrt(d), and covolumes multiply by d^(d*L/2). Thus any algorithm
returning a nonzero vector from one M_j has norm at least p*sqrt(d), while
the claimed determinant bound with C=1 would require

    p*sqrt(d) <= gamma(d)*sqrt(d)*p^(1/L).

For fixed d,L>=2, no modulus-independent gamma(d) can satisfy this for all p.
One can fix d=2, R=Z[i], so class-number assumptions do not rescue the
counterexample. Even PERFECT rank-one ideal solvers cannot meet the stated
bound for this diagonal-only algorithm. Ordinary coefficient size reduction
does nothing: the only nonzero reduction coefficients are -1/p, rounding
to zero. Swapping/reducing the basis could solve this easy example, but is
an additional operation, not a consequence of orthogonal decomposition.

The correct covolume identity for any full-rank orthogonal submodule is

    product_j det(M_j) = [M:D]*det(M).

If the separate line guarantees used in that argument hold, their product
therefore gives a factor [M:D]^(1/(d*L)) in the module determinant bound.
Dropping it is exactly the error. Here it restores the necessary
p^((L-1)/L) factor. This correction does not validate other premises of the
external argument, which have not all been audited.

## 3. The Native Phase Kernel Has The Same Coupling

Let Q=q^d+1 and E(c)=c(q) mod Q. The evaluation ideal is

    I=ker E=(q-X),  det_coeff(I)=Q.

Normalize the first scalar label to one only on its separately charged UNIT
event. Let a_j also denote an explicitly chosen polynomial lift when it
appears in an R-basis. Then

    M={c in R^L : E(c_1)+sum_(j>=2) a_j*E(c_j)=0 mod Q},
    b_1=(q-X)*e_1,  b_j=-a_j*e_1+e_j,
    det_coeff(M)=Q.                                        (2)

K-Gram-Schmidt again leaves the coordinate axes, with vectors
(q-X)*e_1,e_2,...,e_L. Their Galois balance constant is

    C=max(1,(q^2+1)/Q^(2/d)) <= 1+1/q^2.

The balance is nearly perfect for every choice of the other labels, including
dense random ones. It says nothing about saturation across module lines.

If ALL labels are units modulo Q, the line intersections are I*e_j, so

    D_0=I^L,  det_coeff(D_0)=Q^L,  [M:D_0]=Q^(L-1).          (3)

In fact D_0 is contained in M and (3)'s index holds even when the other
labels are not units; it just need not be the entire direct sum of the line
intersections. More generally that direct sum is

    D_diag=direct_sum_j I_(Q/gcd(a_j,Q))*e_j,
    [M:D_diag]=Q^(L-1)/product_(j>=2) gcd(a_j,Q),              (4)

where a_1=1 and I_t=ker(E mod t). Thus an all-unit assertion is a real
restriction, not a synonym for the binary-rank event used in the information
certificate. In the easy control a_2=...=a_L=0, D_diag=M.

The multiplication matrix of q-X is B=q*I-S, where S is the orthogonal
negacyclic shift. Its smallest singular value is at least q-1. Hence every
nonzero vector in I has coefficient norm at least q-1. Unit balancing cannot
move a vector from one coordinate line to another or restore the missing
cosets. A principal-ideal oracle has no undiscovered generator to provide
for I: q-X is already explicit.

The native loss is not by itself a contradiction of every weak asymptotic
ideal approximation factor: for q polynomial in d, an exp(O-tilde(sqrt(d)))
factor can exceed the polynomial loss. The constant-degree/unbounded-p
family in section 2 is the general counterexample. Our decoder additionally
requires a weighted conditional state, not just one short vector.

## 4. Fidelity Cost Of Discarding The Cosets

Use the finite product Gaussian with probability width s=s_G=sigma/sqrt(2),
coefficient box [-R,R]^N, N=d*L, and scalar normalizer

    Z_R=sum_(|z|<=R) exp(-pi*z^2/s^2).

For f(c)=sum_j a_j*E(c_j) mod Q, let r(u)=Pr[f(C)=u] and

    |phi_u> = sum_(f(c)=u) sqrt(mu(c)/r(u))*|c>.

Only frequencies with r(u)>0 matter. Suppose each returned state, on a given
classical branch, has coefficient support in at most J cosets of D_0=I^L
inside this fiber. The chosen cosets may depend arbitrarily on u and public
labels. Their amplitudes and phases may be optimized perfectly.

If 2R<=q-1, E is injective on each coefficient box. To see this, a difference
has digits of magnitude at most q-1 and evaluation of magnitude at most
q^d-1<Q. Zero evaluation modulo Q would be zero as an integer, impossible
for a nonzero such base-q digit vector by its leading nonzero digit.
Thus each D_0-coset contains at most ONE point of the full product box.

Projection/Cauchy-Schwarz bounds squared fidelity by the target probability
mass on the chosen support. Each point has unnormalized mass at most one.
After averaging using the ACTUAL frequency law r, this proves

    F_bar=sum_u r(u)*<phi_u|rho_u|phi_u>
        <= min(1, J*Q/Z_R^N).                              (5)

The cancellation of r(u) is why (5) needs neither a uniform-frequency
assumption nor a typical-label heuristic. Randomized selections and mixtures
obey the same bound by convexity. For heralded branches the same statement
holds for SUCCESS-WEIGHTED fidelity using subnormalized rho_u; a normalized
postselected branch alone is not bounded without its success probability.

Crucial scope: the final output support must satisfy the J-coset restriction.
An algorithm that coherently combines many branches into a larger support
does not satisfy it merely because each intermediate branch was simple.
Exponential support can be prepared by a small quantum circuit in other
settings; (5) is not a gate-count or unrestricted algorithm lower bound.

There is also an untruncated version. Gaussian mass on any translate of a
lattice is at most its mass at the origin, by Poisson summation. Since
||B*z||>=(q-1)*||z||,

    rho_s(D_0+t) <= rho_s(D_0)
                 <= theta(s/(q-1))^N,
    F_bar <= min(1, J*Q*[theta(s/(q-1))/theta(s)]^N).          (6)

No injective-box premise is needed for (6). Conversely (5) cannot be extended
past its premise: at q=3,d=2,L=2,R=2,s=100, optimal one-coset-per-frequency
fidelity is about 0.16952, exceeding the invalid J*Q/Z_R^N value 0.01604.
Here several coefficient points share a coset. This countercontrol prevents
misusing point support as coset support.

## 5. Consequence At The Three-Block Source Widths

Use EXACTLY the L=3,n=1,K=4,phase-budget=0.001 moment-source recipe from
`STRUCTURED_EDCP_IDEAL_COLLISION_CORE.md` and set R=ceil(sigma*sqrt(d)).
For an explicit finite bound, let

    eta = s/(pi*R)*exp(-pi*R^2/s^2),
    Z_R >= s*(1-eta).

This follows from theta(s)>=s and the integral bound on the omitted discrete
Gaussian tail. All three rows meet 2R<=q-1.

| d | log10 upper F_bar, J=1 | log10 eta reference |
|---:|---:|---:|
| 64 | -199.008958348 | -176.190928155 |
| 256 | -2966.04292032 | -700.412478020 |
| 1024 | -20812.6609836 | -2796.39558752 |

For general J add log10 J and cap at zero. To have constant mean squared
fidelity under this support restriction requires at least exponentially many
cosets in d at these widths. The state may have polynomial circuit complexity
despite that count; the missing task is coherent, correctly weighted gluing.
The full-Gaussian bound (6), using an elementary theta-series upper bound,
agrees to the shown digits.

These are 140-digit formula references, NOT interval certificates or large
quantum executions. Small positive tails have not been declared exact zero.
The existing source/primality/reduction qualifications still apply. The
target-state bound is exact under its premises; transferring a physical
source requires its complete trace-distance/preparation error ledger.

## 6. What Remains Algorithmic

The group M/D_0 is easy to describe: evaluation identifies it with

    {t in Z_Q^L : t_1+sum_(j>=2) a_j*t_j=0}.

Uniform superposition over this known group has an elementary linear
constructor. It is not a hidden subgroup that needs discovering. The needed
Gaussian weights are the difficult part. For an affine frequency u, define
the one-block evaluation law p(t) and normalized one-block state |g_t>.
Then the exact target factorization is

    |phi_u> = sum_(sum_j a_j*t_j=u)
        sqrt(product_j p(t_j)/r(u)) * tensor_j |g_(t_j)>.

This equation identifies the correct gluing problem; it is not a preparation
algorithm or permission to assume a weighted-coset oracle. In the injective
box each nonempty |g_t> has only one coefficient point, yet finding the
appropriately weighted joint residues is still not supplied by ideal PIP.

Algebraic normal forms can certify the quotient and its index. They do not
automatically preserve the Gaussian metric or give an efficient conditional
sampler. Likewise, one short module vector and its rotations span at most d
of the L*d dimensions. Even L independent vectors must have their generated
submodule's index checked; independence is not saturation. A usable full
basis must also pass the profile/classical-decoder audit in
`STRUCTURED_EDCP_PROFILE_LIST_DECODER.md`.

Literature checks informing this decision:

- [Biasse and Song, SODA 2016](https://fangsong.info/files/pubs/BS_SODA16.pdf)
  provide quantum principal-ideal/unit-group algorithms, not a general short
  module basis or this conditional Gaussian map.
- [Cramer, Ducas, Peikert and Regev](https://eprint.iacr.org/2015/313.pdf)
  distinguish recovering a promised typical short generator from the weaker
  general principal-ideal approximation guarantee. Neither implies rank-L
  Gaussian preparation.
- [A fully classical LLL algorithm for modules](https://eprint.iacr.org/2022/1356.pdf)
  retains a fixed-field CVP oracle while removing quantum computation. The
  field degree grows here, so that oracle's cost cannot be hidden as constant
  preprocessing. An oracle-based module-LLL wrapper alone is no separation.

## 7. Verification And Gemini Contract

Targeted checks actually run, independently of production modules:

- 27 exact counterfamily coefficient lattices: d=2,4,8; L=2,3,4; p=3,7,19.
  Determinants, integral inclusion matrices, indices and off-axis short
  vectors were checked. At d=2, explicit mod-p enumeration counted 115
  quotient members over (p,L)=(3,2),(3,3),(5,2), matching the formula.
- 18 native exact integer/rational lattice controls: d=2,4,8; q=3,5,7;
  L=2,3, random unit labels with seed 20260927. Checked every basis column's
  frequency, determinant Q, diagonal determinant Q^L, integral inclusion,
  index, and a native vector outside D_0.
- 36 adaptive finite-support controls covered four boxes, three label choices
  including zeros, and J=1,2,5. Direct optimal selected mass respected (5).
  The excluded injectivity example above violated the deliberately misapplied
  finite formula as expected.
- Nine independently summed two-dimensional Gaussian-coset references at
  q=3,5,7 and s=0.7,1.2,2.5 checked the origin maximum and singular-value
  theta bound. Sums cut at ceil(7*s) are numerical references, not proofs
  of infinite-series enclosures.
- Three growing source references evaluated (5)-(6) at 140-digit precision.

Gemini implementation tasks, after the existing upstream numerical repair:

1. Record ambient module rank, ring degree, input basis, actual output
   submodule, exact index, and metric normalization separately. Never infer
   lattice equality from field-span equality or orthogonality.
2. Add the balanced counterfamily as an exact regression and the native
   index formula as a sanity check. Distinguish D_0 from D_diag for nonunits.
3. Track a constructor's FINAL supported cosets, adaptive selection,
   heralding probability and squared fidelity. Apply (5) only with digit
   injectivity and (6) only with its actual Gaussian/ideal geometry.
4. Treat source sufficiency, short-vector finding, saturated basis finding
   and coherent Gaussian conditioning as DIFFERENT proof obligations.
5. Reject proposals whose sole new step is PIP on the already generated
   ideal I. Keep genuinely new cross-line quantum operations open.

No CLI/registry wiring, full-suite run or commit in this theory pass. The
next theory target is weighted coherent gluing or an operation outside the
measured-shear family, with a matched classical algorithm and explicit costs.

## 8. Whole-Module Principal-Ideal Encoding And Its Metric

### An Explicit Field, Ideal And Isomorphism

Could one encode the coupled module as ONE ideal in a larger number field,
then use quantum principal-ideal or unit-group algorithms? There is a simple
exact encoding. It is useful precisely because it exposes what that proposal
would still need to solve. No novelty claim for the algebraic construction.

Assume q odd, d>=2 a power of two, B=q-X in R, and module rank L>=2. Define

    F(Y)=(q-Y^L)^d+1,
    O=Z[Y]/(F(Y)) = R[Y]/(Y^L-B),
    J=Y*O.

F is Eisenstein at 2: every nonleading coefficient is even, while its
constant q^d+1 is 2 modulo 4. Thus its fraction algebra is genuinely a
number FIELD of degree d*L, not an assumed irreducible quotient. O is an
explicit order; it is not asserted to be the maximal order. The bases
{X^i Y^j:0<=i<d,0<=j<L} and {Y^k:0<=k<d*L} differ by an integer unimodular
matrix, since X=q-Y^L. Also O/J=Z_Q and Norm(Y)=Q.

For normalized scalar labels 1,a_1,...,a_(L-1), with polynomial lifts a_j,
use the R-basis of O

    e_0=1,  e_j=Y^j+a_j,  1<=j<L.

Its change from the ordinary R-power basis is the unimodular shear

    w_0=c_0+sum_j a_j*c_j,  w_j=c_j.

Reduction modulo J evaluates X at q and Y at zero. Therefore this map
identifies the ORIGINAL coefficient kernel with J exactly, and every affine
frequency fiber with the corresponding ideal coset. No finite-index pieces
are omitted. This is the larger-field alternative to the incorrect diagonal
decomposition, not a repeat of that error.

The field, order, ideal and principal generator Y are independent of the
random labels. Only the chosen basis/metric depends on them. A call to PIP
on J has no unknown generator left to discover. Enlarging J to the maximal
order without checking return membership can introduce elements outside the
original integer kernel; order/saturation checks remain mandatory.

### The Generator Is Already Nearly Canonical-Shortest

For each embedding sigma of R let beta_sigma^L=q-sigma(X). The L extensions
send Y to beta_sigma*zeta_L^k. Hence

    ||Sigma(Y)||^2 = L*sum_sigma |q-sigma(X)|^(2/L).

Every nonzero z=Y*h in J has integral nonzero Norm(h), so |Norm(z)|>=Q.
AM-GM in the full canonical embedding gives

    lambda_1(Sigma(J)) >= sqrt(d*L)*Q^(1/(d*L)),
    ||Sigma(Y)||/lambda_1(Sigma(J)) <= (1+1/q)^(1/L).        (7)

Thus Y is a KNOWN, nearly optimal shortest vector in that metric. In the
original module coordinates it is (-a_1,1,0,...), which need not be short.

An exact counterfamily makes the distinction concrete. Set L=2 and choose
a_1=(q-1)/2. The module contains v=(1-X,2), of coefficient norm sqrt(6),
whereas Y pulls back to norm sqrt(((q-1)/2)^2+1). Their ratio is unbounded.
The image of v is Y*(Y+2); its multiplier has norm (q-4)^d+1>1, so it is
NOT a principal generator. Canonical-shortest generator guarantees cannot
silently replace coefficient-short-vector guarantees. These deliberately
structured labels are a transfer counterexample, not a natural hard source
or a new algorithm candidate.

### The Exact Pullback Metric

Root-of-unity orthogonality gives, for the element corresponding to c,

    ||Sigma(sum_j c_j*e_j)||^2
      = L*sum_sigma [ |sigma(c_0+sum_(j>=1) a_j*c_j)|^2
               +sum_(j>=1) |sigma(B)|^(2*j/L)*|sigma(c_j)|^2 ]. (8)

This is a label-dependent sheared metric, not L*d times the original
coefficient norm. Simply writing the module as a principal ideal does not
make the native Gaussian a canonical ideal Gaussian.

Even arbitrary POSITIVE diagonal weights on the field embeddings cannot
in general fix this exact mismatch. At a fixed base embedding, write those
weights as w_k>0 and W=sum_k w_k. Orthogonality between 1 and Y^j+a_j in
the desired input metric would require

    W*sigma(a_j)+beta_sigma^j*sum_k w_k*zeta_L^(j*k)=0.

The triangle inequality gives the necessary condition

    |sigma(a_j)| <= |sigma(B)|^(j/L).                       (9)

It applies also to the positive weights produced by multiplication by a
fixed unit. It does NOT rule out all uses of units, a different integer
basis, controlled distortion, or an algorithm optimizing the original metric.

For a uniform label a_1 and any deterministic injective polynomial lifting,
if (9) holds at every base embedding, Parseval implies its coefficient norm
is at most (q+1)^(1/L). Counting the containing integer box therefore bounds
the probability that exact diagonal metric matching is even possible by

    min(1,(2*floor((q+1)^(1/L))+1)^d/Q).                    (10)

No random-matrix heuristic or modulus factorization is used. For L=3 and
the current q=nextprime(d^12), its log10 values are approximately -905.4982,
-4855.0118,-24352.1225 at d=64,256,1024. The underlying probability bound is
an exact rational expression; the displayed logarithms are numerical
references. The initial unit-label normalization remains a charged event.
This is the IDEAL uniform-label law. An actual label-distribution TV error
adds to the event bound and can dominate the displayed tiny probabilities.

### Changing The Source Does Not Solve The Original Decoder

An honest change of coordinates preserves the old Gaussian weight
exp(-pi*||U^(-1)w||^2/s_G^2) and its integer coupling. Suppose instead one
REPLACES it by the convenient canonical Gaussian on O with probability width
S=sqrt(L*d)*s_G. In the power coordinates w, (8) has no cross-block terms:
the w_j blocks are independent and only w_0 survives evaluation modulo J.
The hidden phase is consequently carried by ONE block, while the other
blocks are secret-independent ancillas. This is an exact factorization for
the full Gaussian (or a product truncation in power coordinates), not for a
truncation in the original sheared coordinate box.

The w_0 law is D_(Z,s_G)^d. For a UNIFORM hidden residue its optimal success
is at most

    P_one <= [theta(sqrt(2)*s_G)^2/theta(s_G)]^d / Q.         (11)

This follows from the one-block covariant-state bound and merging evaluation
fibers; it does not assume injectivity. At the current three-block widths,
log10 upper references are -839.1619,-3866.3308,-17414.5689. Thus this metric
replacement loses precisely the multi-block information sought earlier.
Nonuniform secret priors require their own information calculation, and
widening w_0 requires a NEW source-error analysis. Neither is a free repair.

### What Is Still Worth Investigating

[Biasse and Song's expanded S-unit algorithm](https://arxiv.org/html/2510.02280v1)
provides a genuine quantum number-theoretic primitive. It does not by itself
optimize our label-dependent metric or prepare the weighted ideal coset.
Computing a unit group and choosing useful unit combinations are different
tasks, as are finding one generator and a good full lattice basis.

The sharpened target is now explicit: in this fixed degree-d*L field/order,
find a saturated basis or coherent conditional map for the INPUT metric in
(8)'s inverse coordinates, for naturally distributed labels, with a proved
profile and bit complexity. A proposed unit-lattice optimizer must specify
its integer optimization, phase/precision and order-membership costs. It
cannot assume a CVP, short-generator or Gaussian-preimage oracle that already
solves the desired operation. The earlier adaptive-basis extraction result
still supplies the matched classical comparison when applicable.

Checks actually run:

- 18 exact encodings at d=2,4,8; q=3,5,7; L=2,3 checked Eisenstein,
  multiplication-by-Y, its L-th power, determinant Q, full-kernel equality
  and integral unimodular changes. Ninety complex embedding identities
  checked (8), with maximum relative discrepancy 6.34e-16.
- Nine wrong-metric counterfamilies at d=2,4,8 and q=17,101,1009 checked
  the short vector and exact nonunit multiplier norm. 120 positive-weight
  controls checked the triangle obstruction; twelve complete small-label
  enumerations checked (10)'s necessary-event count.
- Twelve finite quantum-source Gram-matrix comparisons at q=3,d=2,L=2,
  labels 1,3,7,9 and widths 0.8,1.4,3 verified that canonical-metric
  replacement has exactly the one-block secret Gram matrix. Maximum
  absolute discrepancy was 1.89e-15. No growing statevector simulation.
- Three exact-expression probability references for (10) and three
  140-digit information references for (11) were evaluated.

Before implementing a unit optimizer, the next mathematical test is whether
unit multiples of Y can even supply a sufficiently short full basis in the
label-dependent metric on the natural ensemble. A single short generator,
compact but enormous units, or a conditional CVP-oracle construction is not
that result. If this representational family fails, retain the exact encoding
as a falsifier and move to a different cross-block operation.

Gemini should add this as an extension of the module/metric audit, not a
new PIP search pipeline. Preserve the field polynomial, explicit order,
label-dependent basis, input-versus-canonical metric, known generator, and
source-change flag. A canonical short-vector certificate with the wrong
metric must not discharge the native decoder's obligation. No production
wiring, routine full test pass or new quantum algorithm in this extension.

## 9. Unit Multiplication Does Not Fix A B-First Basis

Follow-up 2026-09-27. LOCAL DERIVATION / REVIEW PENDING. Write B=q-X,
O=R[Y]/(Y^L-B), J=Y*O, and let U be the label shear from Section 8.
The natural R-basis of J ordered as B,Y,...,Y^(L-1) pulls back to the
native input basis K_0=U^(-1)*diag(B,I,...,I).

Let u be ANY unit of O, not merely an inherited unit of R. Multiply every
basis vector by u, retaining that B-first block order, and set

    w=U^(-1)*coefficients_O(u) in R^L.

This is a nonzero integral vector. Its d negacyclic rotations form a
rank-d integer matrix W: a nonzero R component and the field property of
Frac(R) give injectivity. Thus det(W^T*W) is a positive integer. The first
d coefficient columns of the transformed basis are the rotations of B*w.
Multiplication by B on their R-span has determinant Norm_R(B)=Q, so

    volume(first d columns)=Q*sqrt(det(W^T*W)) >= Q.          (12)

Consequently, if g_i are the sequential Gram--Schmidt lengths of the FULL
coefficient basis and D=d*L, its universal-envelope profile obeys

    H=(s_G/theta(s_G))^D * product_i theta(g_i/s_G)
      >= (s_G/theta(s_G))^D * Q/s_G^d.                     (13)

Use theta(x)>=max(1,x) and the first-d volume identity. This retains the
ambient normalization factor; it is not exactly Q/s_G^d at arbitrary width.
At our growing wide-source parameters the factor is near one and the
bound remains exponential. The theorem-linked spherical source has
log H >= (11/4+o(1))*d*log d, and the elliptical source has the earlier
(5/2+o(1))*d*log d coefficient, at constant phase-error budget.

This obstruction holds even if a quantum algorithm finds the unit for free.
It is a statement about this OUTPUT BASIS and envelope, not a quantum gate
lower bound. It does NOT cover another R-block placed first, integer column
operations mixing blocks, special non-envelope samplers, or arbitrary
coherent conditional maps. Classical LLL is already outside its restriction.

For a unit v inherited from R, a second exact observation is useful. Every
prefix consisting of r WHOLE R-blocks is right-multiplied by r copies of
multiplication-by-v, whose determinant is Norm_R(v)^r=+/-1. Such prefix
volumes are unchanged. Individual Gram--Schmidt lengths and theta products
need not be unchanged. Do not overstate this as a unit-orbit impossibility.

### Bounded Controls Against Classical Reduction

In R=Z[i], L=3, use the genuine extension units

    q=3:  u=-1+Y+i*Y^2,
    q=5:  u=-1+(-1+i)*Y-Y^2,
    q=17: u=-1+(2-i)*Y-i*Y^2.

Their 6-by-6 integer multiplication matrices have determinant 1 and integral
inverses. At each q, five label pairs were drawn with Python Random seed
20260927, sampling residues uniformly from 0,...,Q-1 and using nonnegative
base-q lifts except q^2=-1. Test every u^k, -2<=k<=2, and all six R-block
orders at s_G=sqrt(q). These are small exact-algebra controls, not samples
at the growing hardness-linked source parameters.

Across 450 profiles, no tested unit power improved log J against the SAME
block order without that power. Here J=product_i theta(g_i/s_G), a natural
log is reported, and Gram--Schmidt squared lengths came from exact rational
prefix Gram determinants. The tiny theta tails were evaluated numerically.
The native and ordinary SymPy LLL reference ranges were:

| q | native log J | classical LLL log J range |
|---:|---:|---:|
| 3 | 1.2047316214 | 0.1613831385 to 0.2667851431 |
| 5 | 1.6486601528 | 0.0643864812 to 0.5884106242 |
| 17 | 2.8366675789 | 0.0047183378 to 0.0982179869 |

Seventy-five first-block Gram identities checked (12); 78 determinant checks
covered the three units and transformed bases. Eighteen exact complete-block
prefix identities checked the inherited unit 1+X+X^2 at d=4,8 and q=3,5,17.
No asymptotic LLL guarantee follows from these low-dimensional profiles.

Decision: do not build a unit-enumeration subsystem around the B-first
universal-envelope basis. A useful unit proposal must explicitly change the
block/basis construction or the quantum operation, prove a profile bound on
natural labels, and beat matched classical reduction. In particular, access
to an S-unit algorithm alone does not meet that requirement. The source
hardness contracts are now separated in
`STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT.md`.

FOLLOW-UP (2026-09-28): `STRUCTURED_EDCP_ARCHIMEDEAN_GAUSSIAN_AUDIT.md`
audits APPROXIMATE Gaussian replacement under arbitrary positive embedding
weights. It combines a natural-label correlation bound with a finite-integer
broad/narrow precision split. Ambient overlap only transfers to conditional
fibers with an additional frequency-marginal premise; do not discard that
scope restriction or call this a universal ideal-sampler impossibility.
